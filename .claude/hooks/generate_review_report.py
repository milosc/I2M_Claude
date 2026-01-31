#!/usr/bin/env python3
"""
Generate Code Review Reports

Generates CODE_REVIEW.md and review-findings.json from agent findings.
Part of /htec-sdd-review command output.

Usage:
    python3 generate_review_report.py <system_name> <findings_json_path> [options]

Options:
    --output-dir PATH    Output directory (default: Implementation_<System>/reports/)
    --review-id ID       Review ID (default: auto-generated REV-NNN)
    --scope SCOPE        Review scope: all|changed|module (default: all)
    --update-progress    Update implementation_progress.json
    --update-registry    Update traceability/review_registry.json

Example:
    python3 generate_review_report.py ERTriage /tmp/review_findings.json --update-progress
"""

import json
import os
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def get_project_root() -> Path:
    """Find project root by looking for .claude directory."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / '.claude').exists():
            return current
        current = current.parent
    return Path.cwd()


def load_json_file(path: Path) -> dict:
    """Load JSON file safely."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_json_file(path: Path, data: dict):
    """Save JSON file with proper formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_next_review_id(registry_path: Path) -> str:
    """Get next available review ID from registry."""
    registry = load_json_file(registry_path)
    reviews = registry.get('reviews', [])
    if not reviews:
        return 'REV-001'

    max_num = 0
    for review in reviews:
        rid = review.get('id', '')
        if rid.startswith('REV-'):
            try:
                num = int(rid.split('-')[1])
                max_num = max(max_num, num)
            except (ValueError, IndexError):
                pass
    return f'REV-{max_num + 1:03d}'


def calculate_blocking_status(findings: list, test_coverage: int = 0) -> tuple[str, list]:
    """
    Determine if review passes blocking criteria.

    Returns:
        (status, blocking_issues)
        status: 'passed' | 'failed'
    """
    blocking_issues = []

    # Count by severity
    critical_count = sum(1 for f in findings if f.get('severity', '').lower() == 'critical')
    high_blocking = [
        f for f in findings
        if f.get('severity', '').lower() == 'high'
        and f.get('confidence', 0) > 90
    ]

    # Check blocking criteria
    if critical_count > 0:
        blocking_issues.append(f"{critical_count} CRITICAL finding(s)")

    if high_blocking:
        for f in high_blocking:
            blocking_issues.append(
                f"{f.get('id')}: {f.get('issue', 'Unknown issue')} (HIGH, {f.get('confidence')}% confidence)"
            )

    # Coverage check - warning only, not blocking by default
    # if test_coverage < 80:
    #     blocking_issues.append(f"Test coverage {test_coverage}% below 80% threshold")

    status = 'failed' if blocking_issues else 'passed'
    return status, blocking_issues


def count_findings_by_severity(findings: list) -> dict:
    """Count findings by severity level."""
    counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    for f in findings:
        severity = f.get('severity', 'low').lower()
        if severity in counts:
            counts[severity] += 1
    counts['total'] = sum(counts.values())
    return counts


def generate_markdown_report(
    system_name: str,
    review_id: str,
    findings: list,
    metrics: dict,
    scope: str,
    blocking_status: str,
    blocking_issues: list,
    agents_summary: dict,
    positive_findings: dict,
    recommendations: dict
) -> str:
    """Generate CODE_REVIEW.md content."""

    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    counts = count_findings_by_severity(findings)

    # Group findings by agent
    findings_by_agent = {}
    for f in findings:
        agent = f.get('agent', 'unknown')
        if agent not in findings_by_agent:
            findings_by_agent[agent] = []
        findings_by_agent[agent].append(f)

    # Build markdown
    md = f"""# Code Review Report

## System: {system_name}
## Date: {timestamp}
## Scope: {scope} ({metrics.get('files_reviewed', 0)} files)
## Review ID: {review_id}

---

## Summary

| Severity | Count | Blocking |
|----------|-------|----------|
| CRITICAL | {counts['critical']} | Yes |
| HIGH | {counts['high']} | If confidence > 90% |
| MEDIUM | {counts['medium']} | No |
| LOW | {counts['low']} | No |

**BLOCKING STATUS: {blocking_status.upper()}** {'✅' if blocking_status == 'passed' else '❌'}

"""

    # Add blocking issues if failed
    if blocking_status == 'failed':
        md += "### Blocking Issues\n\n"
        for issue in blocking_issues:
            md += f"- ❌ {issue}\n"
        md += "\n"
    else:
        md += """- ✅ No CRITICAL findings
- ✅ No HIGH findings with confidence > 90% that are blocking
"""
        if metrics.get('test_coverage'):
            coverage = metrics['test_coverage']
            status = '✅' if coverage >= 80 else '⚠️'
            md += f"- {status} Test coverage ~{coverage}% (target: 80%)\n"
        if metrics.get('tests_passing'):
            md += f"- ✅ All tests passing ({metrics['tests_passing']} passed"
            if metrics.get('tests_skipped'):
                md += f", {metrics['tests_skipped']} skipped"
            md += ")\n"
        md += "\n"

    md += "---\n\n## Findings by Agent\n\n"

    # Agent-specific sections
    agent_order = ['security', 'code_quality', 'test_coverage', 'accessibility', 'bug_hunter', 'contracts_reviewer']
    agent_display_names = {
        'security': 'Security Auditor',
        'security-auditor': 'Security Auditor',
        'code_quality': 'Code Quality',
        'code-quality': 'Code Quality',
        'test_coverage': 'Test Coverage',
        'test-coverage': 'Test Coverage',
        'accessibility': 'Accessibility Auditor',
        'accessibility-auditor': 'Accessibility Auditor',
        'bug_hunter': 'Bug Hunter',
        'bug-hunter': 'Bug Hunter',
        'contracts_reviewer': 'Contracts Reviewer',
        'contracts-reviewer': 'Contracts Reviewer'
    }

    # Sort agents to maintain consistent order
    sorted_agents = sorted(
        findings_by_agent.keys(),
        key=lambda a: agent_order.index(a.replace('-', '_')) if a.replace('-', '_') in agent_order else 99
    )

    for agent in sorted_agents:
        agent_findings = findings_by_agent[agent]
        display_name = agent_display_names.get(agent, agent.replace('_', ' ').replace('-', ' ').title())
        count = len(agent_findings)

        md += f"### {display_name} ({count} findings)\n\n"

        if count == 0:
            md += "No issues found.\n\n"
            continue

        for finding in agent_findings:
            fid = finding.get('id', 'N/A')
            severity = finding.get('severity', 'unknown').upper()
            confidence = finding.get('confidence', 0)
            file_path = finding.get('file', 'N/A')
            line = finding.get('line')
            issue = finding.get('issue', 'No description')
            remediation = finding.get('remediation', '')

            location = f"`{file_path}"
            if line:
                location += f":{line}"
            location += "`"

            md += f"#### {fid}: {issue[:60]}{'...' if len(issue) > 60 else ''} ({severity}, {confidence}% confidence)\n"
            md += f"**File:** {location}\n"

            # Add category/WCAG/OWASP if available
            if finding.get('category'):
                md += f"**Category:** {finding['category']}\n"
            if finding.get('wcag'):
                md += f"**WCAG:** {finding['wcag']}\n"
            if finding.get('owasp'):
                md += f"**OWASP:** {finding['owasp']}\n"

            md += f"**Issue:** {issue}\n"

            if remediation:
                md += f"**Remediation:** {remediation}\n"

            md += f"**Status:** [ ] Fixed\n\n"

    # Positive findings section
    if positive_findings:
        md += "---\n\n## Positive Findings\n\n"
        for category, items in positive_findings.items():
            if items:
                md += f"### {category.replace('_', ' ').title()}\n"
                for item in items:
                    md += f"- ✅ {item}\n"
                md += "\n"

    # Metrics section
    md += "---\n\n## Metrics\n\n"
    md += "| Metric | Value | Target | Status |\n"
    md += "|--------|-------|--------|--------|\n"
    md += f"| Files reviewed | {metrics.get('files_reviewed', 'N/A')} | N/A | ✅ |\n"
    md += f"| Total findings | {counts['total']} | <50 | {'✅' if counts['total'] < 50 else '⚠️'} |\n"
    md += f"| Critical findings | {counts['critical']} | 0 | {'✅' if counts['critical'] == 0 else '❌'} |\n"
    if metrics.get('test_coverage'):
        coverage = metrics['test_coverage']
        md += f"| Test coverage | {coverage}% | 80% | {'✅' if coverage >= 80 else '⚠️'} |\n"
    if metrics.get('tests_passing'):
        md += f"| Tests passing | {metrics['tests_passing']} | All | ✅ |\n"
    if metrics.get('code_quality_score'):
        score = metrics['code_quality_score']
        md += f"| Code quality score | {score} | 70 | {'✅' if score >= 70 else '⚠️'} |\n"
    if metrics.get('accessibility_score'):
        score = metrics['accessibility_score']
        md += f"| Accessibility score | {score}% | 75% | {'✅' if score >= 75 else '⚠️'} |\n"

    # Recommendations section
    if recommendations:
        md += "\n---\n\n## Recommendations\n\n"
        for priority, items in recommendations.items():
            if items:
                md += f"### {priority} ({['Must Fix', 'Should Fix', 'Fix Next Sprint', 'Technical Debt'][['P0', 'P1', 'P2', 'P3'].index(priority)] if priority in ['P0', 'P1', 'P2', 'P3'] else priority})\n"
                for i, item in enumerate(items, 1):
                    md += f"{i}. {item}\n"
                md += "\n"

    # Next steps
    md += """---

## Next Steps

"""
    if blocking_status == 'passed':
        md += f"""1. Review HIGH priority findings (optional)
2. Run `/htec-sdd-status {system_name} --finalize` to complete implementation
3. Or run `/htec-sdd-implement {system_name} --task T-NEW` to address findings

"""
    else:
        md += """1. Fix blocking issues listed above
2. Run `/htec-sdd-review` again to verify fixes
3. Repeat until all blocking criteria are met

"""

    md += f"""---

**Report Generated:** {datetime.now(timezone.utc).isoformat()}Z
**Framework Version:** HTEC SDD v3.0.0
"""

    return md


def load_init_template(project_root: Path) -> dict:
    """Load the review_findings.init.json template."""
    template_path = project_root / ".claude" / "templates" / "traceability" / "init" / "review_findings.init.json"
    if template_path.exists():
        return load_json_file(template_path)
    # Fallback minimal structure if template not found
    return {}


def generate_json_report(
    system_name: str,
    review_id: str,
    findings: list,
    metrics: dict,
    scope: str,
    blocking_status: str,
    agents_summary: dict,
    positive_findings: dict,
    recommendations: dict,
    project_root: Path = None
) -> dict:
    """Generate review-findings.json content following the init template pattern."""

    timestamp = datetime.now(timezone.utc).isoformat() + 'Z'
    counts = count_findings_by_severity(findings)

    # Load template for $documentation
    template = load_init_template(project_root) if project_root else {}
    documentation = template.get('$documentation', {
        "purpose": "Consolidated findings from multi-agent code review at Checkpoint 4 (Code Review). Contains all issues found by specialized reviewer agents with severity classification, remediation guidance, and resolution status.",
        "stage": "Implementation",
        "phase_position": "Checkpoint 4 - validates code quality before integration testing",
        "upstream": [
            "task_registry.json",
            "review_registry.json",
            "Source code files (packages/*/src/)"
        ],
        "downstream": [
            "implementation_traceability_register.json",
            "CODE_REVIEW.md"
        ],
        "commands": ["/htec-sdd-review"],
        "skills": ["Implementation_CodeReview"],
        "agents": [
            "quality-security-auditor",
            "quality-code-quality",
            "quality-test-coverage",
            "quality-accessibility-auditor"
        ]
    })

    return {
        "$documentation": documentation,
        "schema_version": "1.0.0",
        "system_name": system_name,
        "review_id": review_id,
        "generated_at": timestamp,
        "scope": scope,
        "traceability_chain": {
            "upstream": [
                "traceability/task_registry.json",
                "traceability/review_registry.json"
            ],
            "downstream": [
                "traceability/implementation_traceability_register.json",
                f"Implementation_{system_name}/reports/CODE_REVIEW.md"
            ]
        },
        "findings": findings,
        "metrics": {
            "files_reviewed": metrics.get('files_reviewed', 0),
            "test_coverage": metrics.get('test_coverage'),
            "tests_passing": metrics.get('tests_passing'),
            "tests_failing": metrics.get('tests_failing', 0),
            "tests_skipped": metrics.get('tests_skipped', 0),
            "code_quality_score": metrics.get('code_quality_score'),
            "accessibility_score": metrics.get('accessibility_score'),
            "security_risk_level": metrics.get('security_risk_level')
        },
        "agents": agents_summary,
        "positive_findings": positive_findings,
        "recommendations": recommendations
    }


def update_review_registry(
    registry_path: Path,
    review_id: str,
    system_name: str,
    findings: list,
    metrics: dict,
    blocking_status: str
):
    """Update traceability/review_registry.json with new review."""

    registry = load_json_file(registry_path)
    if not registry:
        # Initialize from template
        registry = {
            "schema_version": "1.0.0",
            "system_name": system_name,
            "reviews": [],
            "findings_by_category": {
                "bug": [],
                "security": [],
                "code_quality": [],
                "test_coverage": [],
                "contracts": [],
                "accessibility": []
            },
            "p0_blockers": {
                "must_fix_before_production": []
            }
        }

    # Count findings by agent
    agent_counts = {}
    for f in findings:
        agent = f.get('agent', 'unknown')
        if agent not in agent_counts:
            agent_counts[agent] = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        severity = f.get('severity', 'low').lower()
        if severity in agent_counts[agent]:
            agent_counts[agent][severity] += 1

    counts = count_findings_by_severity(findings)

    # Create review entry
    review_entry = {
        "id": review_id,
        "checkpoint": 4,
        "timestamp": datetime.now(timezone.utc).isoformat() + 'Z',
        "status": "PASSED" if blocking_status == 'passed' else "FAILED",
        "files_reviewed": metrics.get('files_reviewed', 0),
        "agents": agent_counts,
        "totals": counts,
        "metrics": {
            "test_coverage": metrics.get('test_coverage'),
            "code_quality_score": metrics.get('code_quality_score')
        }
    }

    registry['reviews'].append(review_entry)

    # Update findings by category
    for f in findings:
        fid = f.get('id', '')
        agent = f.get('agent', '').replace('-', '_')
        category_map = {
            'security': 'security',
            'security_auditor': 'security',
            'code_quality': 'code_quality',
            'test_coverage': 'test_coverage',
            'accessibility': 'accessibility',
            'accessibility_auditor': 'accessibility',
            'bug_hunter': 'bug',
            'contracts_reviewer': 'contracts'
        }
        category = category_map.get(agent, 'code_quality')
        if fid and fid not in registry['findings_by_category'].get(category, []):
            if category not in registry['findings_by_category']:
                registry['findings_by_category'][category] = []
            registry['findings_by_category'][category].append(fid)

    # Update P0 blockers
    p0_findings = [
        f.get('id') for f in findings
        if f.get('priority') == 'P0' or f.get('severity', '').lower() == 'critical'
    ]
    registry['p0_blockers']['must_fix_before_production'] = list(set(
        registry['p0_blockers'].get('must_fix_before_production', []) + p0_findings
    ))

    save_json_file(registry_path, registry)
    print(f"✅ Updated {registry_path}")


def update_implementation_progress(
    progress_path: Path,
    review_id: str,
    blocking_status: str,
    metrics: dict,
    output_files: list
):
    """Update _state/implementation_progress.json with review completion."""

    progress = load_json_file(progress_path)
    if not progress:
        print(f"⚠️ Could not load {progress_path}")
        return

    timestamp = datetime.now(timezone.utc).isoformat() + 'Z'

    # Update checkpoint 4 (Code Review)
    if 'checkpoints' in progress:
        if '4' in progress['checkpoints']:
            progress['checkpoints']['4'] = {
                "status": "completed",
                "name": "Code Review",
                "started_at": progress['checkpoints']['4'].get('started_at', timestamp),
                "completed_at": timestamp,
                "outputs": output_files,
                "metrics": {
                    "review_id": review_id,
                    "agents_completed": 4,
                    "total_findings": metrics.get('total_findings', 0),
                    "critical_findings": metrics.get('critical_findings', 0),
                    "high_findings": metrics.get('high_findings', 0),
                    "blocking_status": blocking_status
                }
            }

    # Update current checkpoint
    if blocking_status == 'passed':
        progress['current_checkpoint'] = max(progress.get('current_checkpoint', 4), 5)

    progress['last_updated'] = timestamp

    save_json_file(progress_path, progress)
    print(f"✅ Updated {progress_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate code review reports')
    parser.add_argument('system_name', help='System name (e.g., ERTriage)')
    parser.add_argument('findings_json', help='Path to JSON file with agent findings')
    parser.add_argument('--output-dir', help='Output directory for reports')
    parser.add_argument('--review-id', help='Review ID (auto-generated if not provided)')
    parser.add_argument('--scope', default='all', help='Review scope: all|changed|module')
    parser.add_argument('--update-progress', action='store_true', help='Update implementation_progress.json')
    parser.add_argument('--update-registry', action='store_true', help='Update review_registry.json')

    args = parser.parse_args()

    project_root = get_project_root()

    # Load findings
    findings_path = Path(args.findings_json)
    if not findings_path.exists():
        print(f"❌ Findings file not found: {findings_path}")
        sys.exit(1)

    data = load_json_file(findings_path)

    # Extract data from input JSON
    findings = data.get('findings', [])
    metrics = data.get('metrics', {})
    agents_summary = data.get('agents', {})
    positive_findings = data.get('positive_findings', {})
    recommendations = data.get('recommendations', {})

    # Set output directory
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = project_root / f"Implementation_{args.system_name}" / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get review ID
    registry_path = project_root / "traceability" / "review_registry.json"
    review_id = args.review_id or get_next_review_id(registry_path)

    # Calculate blocking status
    test_coverage = metrics.get('test_coverage', 0)
    blocking_status, blocking_issues = calculate_blocking_status(findings, test_coverage)

    # Generate reports
    md_content = generate_markdown_report(
        system_name=args.system_name,
        review_id=review_id,
        findings=findings,
        metrics=metrics,
        scope=args.scope,
        blocking_status=blocking_status,
        blocking_issues=blocking_issues,
        agents_summary=agents_summary,
        positive_findings=positive_findings,
        recommendations=recommendations
    )

    json_content = generate_json_report(
        system_name=args.system_name,
        review_id=review_id,
        findings=findings,
        metrics=metrics,
        scope=args.scope,
        blocking_status=blocking_status,
        agents_summary=agents_summary,
        positive_findings=positive_findings,
        recommendations=recommendations,
        project_root=project_root
    )

    # Write reports
    md_path = output_dir / "CODE_REVIEW.md"
    json_path = output_dir / "review-findings.json"

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"✅ Generated {md_path}")

    save_json_file(json_path, json_content)
    print(f"✅ Generated {json_path}")

    # Update registries if requested
    output_files = [str(md_path), str(json_path)]

    if args.update_registry:
        update_review_registry(
            registry_path=registry_path,
            review_id=review_id,
            system_name=args.system_name,
            findings=findings,
            metrics=metrics,
            blocking_status=blocking_status
        )

    if args.update_progress:
        progress_path = project_root / "_state" / "implementation_progress.json"
        counts = count_findings_by_severity(findings)
        update_implementation_progress(
            progress_path=progress_path,
            review_id=review_id,
            blocking_status=blocking_status,
            metrics={
                'total_findings': counts['total'],
                'critical_findings': counts['critical'],
                'high_findings': counts['high'],
                **metrics
            },
            output_files=output_files
        )

    # Print summary
    counts = count_findings_by_severity(findings)
    print(f"\n{'='*50}")
    print(f"Code Review: {blocking_status.upper()} {'✅' if blocking_status == 'passed' else '❌'}")
    print(f"{'='*50}")
    print(f"Review ID: {review_id}")
    print(f"Findings: {counts['total']} total ({counts['critical']} CRITICAL, {counts['high']} HIGH)")
    print(f"Reports: {output_dir}/")
    print(f"  - CODE_REVIEW.md")
    print(f"  - review-findings.json")

    if blocking_status == 'failed':
        print(f"\n❌ Blocking issues:")
        for issue in blocking_issues:
            print(f"   - {issue}")
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
