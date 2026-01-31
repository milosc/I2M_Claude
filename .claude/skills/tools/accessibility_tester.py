#!/usr/bin/env python3
"""
Accessibility Tester Tool

A CLI utility for running WCAG 2.1 AA accessibility audits using Playwright
with axe-core integration. Generates compliance reports and remediation guides.

Usage:
    python accessibility_tester.py audit <url> <output_dir> [--wcag-level AA]
    python accessibility_tester.py page <url> <output_file>
    python accessibility_tester.py report <audit_dir> <output_file>

Requirements:
    pip install playwright
    playwright install chromium
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

try:
    from playwright.sync_api import sync_playwright, Page, Browser
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


@dataclass
class A11yViolation:
    """Represents an accessibility violation."""
    id: str
    impact: str  # critical, serious, moderate, minor
    description: str
    help: str
    help_url: str
    nodes: List[Dict]
    wcag_tags: List[str]


@dataclass
class A11yResult:
    """Result of an accessibility audit."""
    url: str
    timestamp: str
    violations: List[A11yViolation]
    passes: int
    incomplete: int
    inapplicable: int


# axe-core script to inject (minified version reference)
AXE_SCRIPT_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.2/axe.min.js"

# WCAG tag mappings
WCAG_TAGS = {
    "A": ["wcag2a", "wcag21a"],
    "AA": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"],
    "AAA": ["wcag2a", "wcag2aa", "wcag2aaa", "wcag21a", "wcag21aa", "wcag21aaa"],
}

# Impact severity order
IMPACT_ORDER = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}


def ensure_dir(path: str) -> None:
    """Ensure directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)


def inject_axe(page: Page) -> bool:
    """Inject axe-core into the page."""
    try:
        # Check if axe is already loaded
        has_axe = page.evaluate("typeof axe !== 'undefined'")
        if has_axe:
            return True

        # Inject axe-core
        page.add_script_tag(url=AXE_SCRIPT_URL)
        page.wait_for_function("typeof axe !== 'undefined'", timeout=10000)
        return True
    except Exception as e:
        print(f"  Warning: Failed to inject axe-core: {e}")
        return False


def run_axe_audit(page: Page, wcag_level: str = "AA") -> Dict:
    """Run axe-core accessibility audit on the page."""
    tags = WCAG_TAGS.get(wcag_level, WCAG_TAGS["AA"])

    # Configure and run axe
    result = page.evaluate(f"""
        async () => {{
            const results = await axe.run(document, {{
                runOnly: {{
                    type: 'tag',
                    values: {json.dumps(tags + ['best-practice'])}
                }},
                resultTypes: ['violations', 'passes', 'incomplete', 'inapplicable']
            }});
            return results;
        }}
    """)

    return result


def parse_violations(axe_result: Dict) -> List[A11yViolation]:
    """Parse axe-core violations into structured format."""
    violations = []

    for v in axe_result.get('violations', []):
        # Extract WCAG tags
        wcag_tags = [tag for tag in v.get('tags', []) if tag.startswith('wcag')]

        violations.append(A11yViolation(
            id=v.get('id', ''),
            impact=v.get('impact', 'unknown'),
            description=v.get('description', ''),
            help=v.get('help', ''),
            help_url=v.get('helpUrl', ''),
            nodes=[{
                'html': node.get('html', ''),
                'target': node.get('target', []),
                'failure_summary': node.get('failureSummary', ''),
            } for node in v.get('nodes', [])],
            wcag_tags=wcag_tags,
        ))

    # Sort by impact severity
    violations.sort(key=lambda x: IMPACT_ORDER.get(x.impact, 4))

    return violations


def audit_page(url: str, wcag_level: str = "AA") -> A11yResult:
    """Run accessibility audit on a single page."""
    if not HAS_PLAYWRIGHT:
        print("Error: Playwright not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    timestamp = datetime.now().isoformat()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navigate to page
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(1000)  # Wait for JS to settle

            # Inject and run axe
            if not inject_axe(page):
                return A11yResult(
                    url=url,
                    timestamp=timestamp,
                    violations=[],
                    passes=0,
                    incomplete=0,
                    inapplicable=0,
                )

            axe_result = run_axe_audit(page, wcag_level)
            violations = parse_violations(axe_result)

            return A11yResult(
                url=url,
                timestamp=timestamp,
                violations=violations,
                passes=len(axe_result.get('passes', [])),
                incomplete=len(axe_result.get('incomplete', [])),
                inapplicable=len(axe_result.get('inapplicable', [])),
            )
        finally:
            browser.close()


def audit_multiple_pages(
    base_url: str,
    pages: List[Dict],
    output_dir: str,
    wcag_level: str = "AA"
) -> Dict:
    """Run accessibility audit on multiple pages."""
    if not HAS_PLAYWRIGHT:
        print("Error: Playwright not installed.")
        sys.exit(1)

    results = {
        "audit_date": datetime.now().isoformat(),
        "base_url": base_url,
        "wcag_level": wcag_level,
        "pages": [],
        "summary": {
            "total_pages": len(pages),
            "total_violations": 0,
            "critical": 0,
            "serious": 0,
            "moderate": 0,
            "minor": 0,
        }
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_config in pages:
            url = f"{base_url}{page_config.get('path', '/')}"
            name = page_config.get('name', page_config.get('path', '/'))

            print(f"  Auditing: {name}")

            try:
                page.goto(url, wait_until="networkidle")
                page.wait_for_timeout(1000)

                # Wait for specific selector if provided
                if page_config.get('wait_selector'):
                    page.wait_for_selector(page_config['wait_selector'], timeout=5000)

                if not inject_axe(page):
                    continue

                axe_result = run_axe_audit(page, wcag_level)
                violations = parse_violations(axe_result)

                # Count by impact
                impact_counts = {"critical": 0, "serious": 0, "moderate": 0, "minor": 0}
                for v in violations:
                    if v.impact in impact_counts:
                        impact_counts[v.impact] += 1

                page_result = {
                    "name": name,
                    "url": url,
                    "violations": [asdict(v) for v in violations],
                    "violation_count": len(violations),
                    "impact_counts": impact_counts,
                    "passes": len(axe_result.get('passes', [])),
                }

                results["pages"].append(page_result)
                results["summary"]["total_violations"] += len(violations)
                for impact, count in impact_counts.items():
                    results["summary"][impact] += count

                status = "PASS" if len(violations) == 0 else f"FAIL ({len(violations)} issues)"
                print(f"    {status}")

            except Exception as e:
                print(f"    Error: {e}")
                results["pages"].append({
                    "name": name,
                    "url": url,
                    "error": str(e),
                })

        browser.close()

    return results


def generate_a11y_report(results: Dict, output_path: str) -> None:
    """Generate markdown accessibility report."""
    summary = results.get("summary", {})
    pages = results.get("pages", [])

    report_lines = [
        "# Accessibility Audit Report",
        "",
        f"**Generated:** {results.get('audit_date', datetime.now().isoformat())}",
        f"**WCAG Level:** {results.get('wcag_level', 'AA')}",
        f"**Base URL:** {results.get('base_url', 'N/A')}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Metric | Value | Target | Status |",
        "|--------|-------|--------|--------|",
        f"| **Total Pages Audited** | {summary.get('total_pages', 0)} | - | - |",
        f"| **Critical Issues** | {summary.get('critical', 0)} | 0 | {'PASS' if summary.get('critical', 0) == 0 else 'FAIL'} |",
        f"| **Serious Issues** | {summary.get('serious', 0)} | 0 | {'PASS' if summary.get('serious', 0) == 0 else 'FAIL'} |",
        f"| **Moderate Issues** | {summary.get('moderate', 0)} | 5 | {'PASS' if summary.get('moderate', 0) <= 5 else 'WARN'} |",
        f"| **Minor Issues** | {summary.get('minor', 0)} | 10 | {'PASS' if summary.get('minor', 0) <= 10 else 'WARN'} |",
        "",
    ]

    # Overall status
    if summary.get('critical', 0) == 0 and summary.get('serious', 0) == 0:
        overall_status = "COMPLIANT"
    else:
        overall_status = "NON-COMPLIANT"

    report_lines.extend([
        f"## Overall Status: {overall_status}",
        "",
        "---",
        "",
        "## Results by Page",
        "",
    ])

    # Page results
    for page_result in pages:
        name = page_result.get('name', 'Unknown')
        url = page_result.get('url', '')
        violations = page_result.get('violations', [])
        error = page_result.get('error')

        report_lines.append(f"### {name}")
        report_lines.append("")

        if error:
            report_lines.append(f"**Error:** {error}")
            report_lines.append("")
            continue

        violation_count = len(violations)
        status = "PASS" if violation_count == 0 else f"FAIL ({violation_count} issues)"
        report_lines.append(f"**URL:** `{url}`")
        report_lines.append(f"**Status:** {status}")
        report_lines.append("")

        if violations:
            report_lines.append("#### Violations")
            report_lines.append("")

            # Group by impact
            by_impact = {}
            for v in violations:
                impact = v.get('impact', 'unknown')
                if impact not in by_impact:
                    by_impact[impact] = []
                by_impact[impact].append(v)

            for impact in ["critical", "serious", "moderate", "minor"]:
                if impact not in by_impact:
                    continue

                impact_violations = by_impact[impact]
                icon = {
                    "critical": ":red_circle:",
                    "serious": ":orange_circle:",
                    "moderate": ":yellow_circle:",
                    "minor": ":white_circle:",
                }.get(impact, "")

                report_lines.append(f"##### {icon} {impact.upper()} ({len(impact_violations)})")
                report_lines.append("")

                for v in impact_violations:
                    report_lines.append(f"**[{v.get('id', 'unknown')}]** {v.get('description', '')}")
                    report_lines.append("")
                    report_lines.append(f"- **Help:** {v.get('help', '')}")
                    report_lines.append(f"- **WCAG:** {', '.join(v.get('wcag_tags', []))}")
                    report_lines.append(f"- **More info:** [{v.get('id')}]({v.get('help_url', '')})")
                    report_lines.append("")

                    # Show affected elements (limit to 3)
                    nodes = v.get('nodes', [])[:3]
                    if nodes:
                        report_lines.append("**Affected elements:**")
                        report_lines.append("```html")
                        for node in nodes:
                            report_lines.append(node.get('html', ''))
                        report_lines.append("```")
                        if len(v.get('nodes', [])) > 3:
                            report_lines.append(f"*...and {len(v.get('nodes', [])) - 3} more*")
                    report_lines.append("")

        report_lines.append("---")
        report_lines.append("")

    # WCAG Checklist
    report_lines.extend([
        "## WCAG 2.1 AA Checklist",
        "",
        "### Perceivable",
        "",
        "| Criterion | Status | Notes |",
        "|-----------|--------|-------|",
        "| 1.1.1 Non-text Content | - | Check images have alt text |",
        "| 1.3.1 Info and Relationships | - | Semantic HTML used |",
        "| 1.4.1 Use of Color | - | Color not sole indicator |",
        "| 1.4.3 Contrast (Minimum) | - | 4.5:1 for text |",
        "| 1.4.11 Non-text Contrast | - | 3:1 for UI components |",
        "",
        "### Operable",
        "",
        "| Criterion | Status | Notes |",
        "|-----------|--------|-------|",
        "| 2.1.1 Keyboard | - | All interactive elements accessible |",
        "| 2.1.2 No Keyboard Trap | - | Focus can move freely |",
        "| 2.4.1 Bypass Blocks | - | Skip link present |",
        "| 2.4.3 Focus Order | - | Logical tab order |",
        "| 2.4.7 Focus Visible | - | Focus indicator present |",
        "",
        "### Understandable",
        "",
        "| Criterion | Status | Notes |",
        "|-----------|--------|-------|",
        "| 3.1.1 Language of Page | - | lang attribute set |",
        "| 3.2.1 On Focus | - | No unexpected changes |",
        "| 3.3.1 Error Identification | - | Errors clearly indicated |",
        "| 3.3.2 Labels or Instructions | - | All inputs labeled |",
        "",
        "### Robust",
        "",
        "| Criterion | Status | Notes |",
        "|-----------|--------|-------|",
        "| 4.1.1 Parsing | - | Valid HTML |",
        "| 4.1.2 Name, Role, Value | - | ARIA properly used |",
        "",
        "---",
        "",
        "*Generated by accessibility_tester.py using axe-core*",
    ])

    ensure_dir(os.path.dirname(output_path))
    with open(output_path, 'w') as f:
        f.write('\n'.join(report_lines))

    print(f"\nReport generated: {output_path}")


def generate_remediation_guide(results: Dict, output_path: str) -> None:
    """Generate remediation guide with fix suggestions."""
    report_lines = [
        "# Accessibility Remediation Guide",
        "",
        f"**Generated:** {datetime.now().isoformat()}",
        "",
        "This guide provides fix suggestions for accessibility issues found in the audit.",
        "",
        "---",
        "",
    ]

    # Collect all unique violations
    all_violations = {}
    for page in results.get("pages", []):
        for v in page.get("violations", []):
            vid = v.get("id")
            if vid not in all_violations:
                all_violations[vid] = v
                all_violations[vid]["pages"] = []
            all_violations[vid]["pages"].append(page.get("name", ""))

    # Sort by impact
    sorted_violations = sorted(
        all_violations.values(),
        key=lambda x: IMPACT_ORDER.get(x.get("impact", ""), 4)
    )

    # Group by impact
    report_lines.append("## Issues by Priority")
    report_lines.append("")

    for impact in ["critical", "serious", "moderate", "minor"]:
        impact_violations = [v for v in sorted_violations if v.get("impact") == impact]
        if not impact_violations:
            continue

        report_lines.append(f"### {impact.upper()} ({len(impact_violations)} unique issues)")
        report_lines.append("")

        for v in impact_violations:
            report_lines.extend([
                f"#### [{v.get('id')}] {v.get('description', '')}",
                "",
                f"**Pages affected:** {', '.join(v.get('pages', []))}",
                "",
                f"**Problem:** {v.get('help', '')}",
                "",
                f"**WCAG Criteria:** {', '.join(v.get('wcag_tags', []))}",
                "",
                "**Fix suggestion:**",
                "",
            ])

            # Add fix suggestions based on violation ID
            fix = get_fix_suggestion(v.get('id', ''))
            report_lines.append(fix)
            report_lines.append("")

            report_lines.append(f"**Learn more:** [{v.get('id')}]({v.get('help_url', '')})")
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

    ensure_dir(os.path.dirname(output_path))
    with open(output_path, 'w') as f:
        f.write('\n'.join(report_lines))

    print(f"Remediation guide generated: {output_path}")


def get_fix_suggestion(violation_id: str) -> str:
    """Get fix suggestion for common violations."""
    fixes = {
        "color-contrast": """
```css
/* Ensure text has sufficient contrast */
/* Normal text: 4.5:1 ratio */
/* Large text (18px+ or 14px+ bold): 3:1 ratio */

/* Bad */
.text-gray-400 { color: #9ca3af; } /* Too light */

/* Good */
.text-gray-600 { color: #4b5563; } /* 5.7:1 ratio */
```
""",
        "button-name": """
```html
<!-- Bad: No accessible name -->
<button class="icon-btn">
  <svg>...</svg>
</button>

<!-- Good: Add aria-label -->
<button class="icon-btn" aria-label="Close dialog">
  <svg aria-hidden="true">...</svg>
</button>
```
""",
        "link-name": """
```html
<!-- Bad: No accessible name -->
<a href="/profile"><img src="avatar.png"></a>

<!-- Good: Add aria-label or text -->
<a href="/profile" aria-label="View profile">
  <img src="avatar.png" alt="">
</a>
```
""",
        "image-alt": """
```html
<!-- Bad: Missing alt -->
<img src="chart.png">

<!-- Good: Descriptive alt -->
<img src="chart.png" alt="Sales chart showing 20% growth">

<!-- Good: Decorative image -->
<img src="decoration.png" alt="" role="presentation">
```
""",
        "label": """
```html
<!-- Bad: Input without label -->
<input type="text" placeholder="Email">

<!-- Good: Explicit label -->
<label for="email">Email</label>
<input type="text" id="email" placeholder="email@example.com">

<!-- Good: aria-label -->
<input type="text" aria-label="Email address">
```
""",
        "heading-order": """
```html
<!-- Bad: Skipping heading levels -->
<h1>Title</h1>
<h3>Subtitle</h3>  <!-- Skipped h2 -->

<!-- Good: Proper hierarchy -->
<h1>Title</h1>
<h2>Subtitle</h2>
<h3>Section</h3>
```
""",
        "region": """
```html
<!-- Bad: Content not in landmarks -->
<div>Main content here</div>

<!-- Good: Use landmarks -->
<main>Main content here</main>
<nav>Navigation</nav>
<aside>Sidebar</aside>
```
""",
        "aria-hidden-focus": """
```html
<!-- Bad: Hidden element contains focusable -->
<div aria-hidden="true">
  <button>Click me</button>  <!-- Still focusable! -->
</div>

<!-- Good: Also disable focus -->
<div aria-hidden="true">
  <button tabindex="-1">Click me</button>
</div>
```
""",
    }

    return fixes.get(violation_id, "Refer to the help URL for specific fix guidance.")


def cmd_audit(args):
    """Handle audit command for multiple pages."""
    print(f"\nRunning accessibility audit")
    print(f"Base URL: {args.url}")
    print(f"WCAG Level: {args.wcag_level}")
    print("")

    # Default pages if not specified
    pages = [
        {"name": "Home", "path": "/"},
        {"name": "Dashboard", "path": "/dashboard"},
    ]

    if args.pages:
        with open(args.pages, 'r') as f:
            pages = json.load(f).get('pages', pages)

    print(f"Pages to audit: {len(pages)}")
    print("")

    results = audit_multiple_pages(args.url, pages, args.output, args.wcag_level)

    # Save results
    ensure_dir(args.output)
    results_path = os.path.join(args.output, "a11y-results.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

    # Generate reports
    report_path = os.path.join(args.output, "accessibility-report.md")
    generate_a11y_report(results, report_path)

    remediation_path = os.path.join(args.output, "a11y-remediation.md")
    generate_remediation_guide(results, remediation_path)

    print(f"\nAudit complete!")
    print(f"  Critical: {results['summary']['critical']}")
    print(f"  Serious: {results['summary']['serious']}")
    print(f"  Moderate: {results['summary']['moderate']}")
    print(f"  Minor: {results['summary']['minor']}")


def cmd_page(args):
    """Handle single page audit."""
    print(f"\nAuditing: {args.url}")

    result = audit_page(args.url, args.wcag_level)

    # Output
    output_data = {
        "url": result.url,
        "timestamp": result.timestamp,
        "summary": {
            "violations": len(result.violations),
            "passes": result.passes,
            "incomplete": result.incomplete,
        },
        "violations": [asdict(v) for v in result.violations],
    }

    if args.output.endswith('.json'):
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
    else:
        generate_a11y_report({
            "audit_date": result.timestamp,
            "wcag_level": args.wcag_level,
            "base_url": args.url,
            "pages": [{
                "name": "Page",
                "url": args.url,
                "violations": [asdict(v) for v in result.violations],
            }],
            "summary": {
                "total_pages": 1,
                "total_violations": len(result.violations),
                "critical": sum(1 for v in result.violations if v.impact == "critical"),
                "serious": sum(1 for v in result.violations if v.impact == "serious"),
                "moderate": sum(1 for v in result.violations if v.impact == "moderate"),
                "minor": sum(1 for v in result.violations if v.impact == "minor"),
            }
        }, args.output)

    print(f"\nResults saved to: {args.output}")
    print(f"Violations found: {len(result.violations)}")


def cmd_report(args):
    """Handle report generation from existing audit."""
    results_path = os.path.join(args.audit_dir, "a11y-results.json")

    if not os.path.exists(results_path):
        print(f"Error: No audit results found at {results_path}")
        sys.exit(1)

    with open(results_path, 'r') as f:
        results = json.load(f)

    generate_a11y_report(results, args.output)


def main():
    parser = argparse.ArgumentParser(
        description="Accessibility Tester Tool using axe-core",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Audit multiple pages
  python accessibility_tester.py audit http://localhost:3000 ./a11y-audit

  # Audit single page
  python accessibility_tester.py page http://localhost:3000/ ./report.md

  # Generate report from existing audit
  python accessibility_tester.py report ./a11y-audit ./report.md
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Audit command
    audit_parser = subparsers.add_parser("audit", help="Audit multiple pages")
    audit_parser.add_argument("url", help="Base URL of the prototype")
    audit_parser.add_argument("output", help="Output directory")
    audit_parser.add_argument("--wcag-level", default="AA", choices=["A", "AA", "AAA"])
    audit_parser.add_argument("--pages", help="JSON file with pages to audit")

    # Page command
    page_parser = subparsers.add_parser("page", help="Audit single page")
    page_parser.add_argument("url", help="URL to audit")
    page_parser.add_argument("output", help="Output file (.json or .md)")
    page_parser.add_argument("--wcag-level", default="AA", choices=["A", "AA", "AAA"])

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate report")
    report_parser.add_argument("audit_dir", help="Directory with audit results")
    report_parser.add_argument("output", help="Output report path (.md)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "audit": cmd_audit,
        "page": cmd_page,
        "report": cmd_report,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
