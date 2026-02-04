#!/usr/bin/env python3
"""
Verify skills frontmatter in agents and commands.

This script validates that:
1. All agents/commands have skills: field in frontmatter
2. Skills use required/optional structure
3. All referenced skills exist in .claude/skills/
4. No duplicate skills within a file
5. Generates pass/fail report

Usage:
    python3 .claude/hooks/verify_skills_frontmatter.py              # Full verification
    python3 .claude/hooks/verify_skills_frontmatter.py --batch 1    # Verify specific batch
    python3 .claude/hooks/verify_skills_frontmatter.py --file PATH  # Verify single file
    python3 .claude/hooks/verify_skills_frontmatter.py --summary    # Summary only
"""

import os
import sys
import json
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set

# Find project root
def find_project_root() -> Path:
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / '.claude').exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent.parent

PROJECT_ROOT = find_project_root()
CLAUDE_DIR = PROJECT_ROOT / '.claude'
AGENTS_DIR = CLAUDE_DIR / 'agents'
COMMANDS_DIR = CLAUDE_DIR / 'commands'
SKILLS_DIR = CLAUDE_DIR / 'skills'

# Batch definitions
BATCHES = {
    1: {
        "name": "Orchestrators",
        "files": [
            "agents/discovery-orchestrator.md",
            "agents/prototype-orchestrator.md",
            "agents/productspecs-orchestrator.md",
            "agents/solarch-orchestrator.md",
        ]
    },
    2: {
        "name": "Available Skills Agents",
        "files": [
            "agents/implementation-developer.md",
            "agents/implementation-test-automation-engineer.md",
            "agents/quality-bug-hunter.md",
            "agents/discovery-kpis-generator.md",
            "agents/productspecs-api-module-specifier.md",
            "agents/solarch-c4-context-generator.md",
            "agents/solarch-c4-container-generator.md",
            "agents/solarch-c4-component-generator.md",
            "agents/solarch-c4-deployment-generator.md",
        ]
    },
    3: {
        "name": "Format Update",
        "files": [
            "agents/discovery-persona-generator.md",
            "agents/discovery-vp-pm-reviewer.md",
        ]
    },
    4: {
        "name": "Key Commands",
        "files": [
            "commands/discovery.md",
            "commands/prototype.md",
            "commands/productspecs.md",
            "commands/solarch.md",
            "commands/discovery-feedback.md",
            "commands/prototype-feedback.md",
            "commands/productspecs-feedback.md",
            "commands/solarch-feedback.md",
            "commands/compliance-check.md",
            "commands/discovery-analyze.md",
            "commands/discovery-personas.md",
            "commands/discovery-jtbd.md",
            "commands/discovery-kpis.md",
            "commands/discovery-screens.md",
            "commands/discovery-components.md",
            "commands/discovery-data-fields.md",
            "commands/prototype-build.md",
            "commands/prototype-components.md",
            "commands/prototype-screens.md",
            "commands/productspecs-modules.md",
            "commands/productspecs-tests.md",
            "commands/solarch-blocks.md",
            "commands/solarch-decisions.md",
        ]
    },
}


@dataclass
class VerificationResult:
    file_path: str
    passed: bool = True
    has_skills_field: bool = False
    has_required_optional: bool = False
    required_skills: List[str] = field(default_factory=list)
    optional_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    duplicate_skills: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


def get_available_skills() -> Set[str]:
    """Get set of all available skill folder names."""
    skills = set()
    if SKILLS_DIR.exists():
        for item in SKILLS_DIR.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                if (item / 'SKILL.md').exists():
                    skills.add(item.name)
    return skills


def parse_yaml_frontmatter(content: str) -> Optional[Dict]:
    """Parse YAML frontmatter using regex (no yaml dependency)."""
    if not content.startswith('---'):
        return None

    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return None

    yaml_content = content[3:end_match.start() + 3]
    result = {}

    # Check for skills field
    skills_match = re.search(r'^skills:\s*\n((?:\s+.+\n)*)', yaml_content, re.MULTILINE)
    if skills_match:
        skills_block = skills_match.group(1)
        result['skills'] = {}

        # Parse required
        required_match = re.search(r'required:\s*\n((?:\s+-\s+.+\n)*)', skills_block)
        if required_match:
            skills_list = re.findall(r'-\s+([^\n#]+)', required_match.group(1))
            result['skills']['required'] = [s.strip() for s in skills_list if s.strip()]
        elif re.search(r'required:\s*\[\s*\]', skills_block):
            result['skills']['required'] = []

        # Parse optional
        optional_match = re.search(r'optional:\s*\n((?:\s+-\s+.+\n)*)', skills_block)
        if optional_match:
            skills_list = re.findall(r'-\s+([^\n#]+)', optional_match.group(1))
            result['skills']['optional'] = [s.strip() for s in skills_list if s.strip()]
        elif re.search(r'optional:\s*\[\s*\]', skills_block):
            result['skills']['optional'] = []

    # Check for old format (comma-separated string)
    old_skills_match = re.search(r'^skills:\s*([^\n]+)$', yaml_content, re.MULTILINE)
    if old_skills_match and 'skills' not in result:
        skills_str = old_skills_match.group(1).strip()
        if skills_str and not skills_str.startswith('{'):
            result['skills'] = skills_str  # Old format

    return result


def verify_file(file_path: Path, available_skills: Set[str]) -> VerificationResult:
    """Verify a single file's skills frontmatter."""
    rel_path = str(file_path.relative_to(CLAUDE_DIR))
    result = VerificationResult(file_path=rel_path)

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        result.passed = False
        result.errors.append(f"Cannot read file: {e}")
        return result

    frontmatter = parse_yaml_frontmatter(content)

    # Check 1: Has frontmatter
    if frontmatter is None:
        result.passed = False
        result.errors.append("No YAML frontmatter found")
        return result

    # Check 2: Has skills field
    if 'skills' not in frontmatter:
        result.passed = False
        result.errors.append("Missing 'skills:' field in frontmatter")
        return result

    result.has_skills_field = True
    skills_data = frontmatter['skills']

    # Check 3: Has required/optional structure
    if isinstance(skills_data, dict):
        if 'required' in skills_data or 'optional' in skills_data:
            result.has_required_optional = True
            result.required_skills = skills_data.get('required', [])
            result.optional_skills = skills_data.get('optional', [])
        else:
            result.passed = False
            result.errors.append("skills: must have 'required:' and/or 'optional:' keys")
    elif isinstance(skills_data, str):
        result.passed = False
        result.errors.append("Old format detected: skills should use required/optional structure, not comma-separated string")
        result.warnings.append(f"Current value: {skills_data}")
    elif isinstance(skills_data, list):
        result.passed = False
        result.errors.append("skills: must use required/optional structure, not a flat list")
    else:
        result.passed = False
        result.errors.append(f"Invalid skills format: {type(skills_data)}")

    if not result.has_required_optional:
        return result

    # Check 4: All skills exist
    all_skills = result.required_skills + result.optional_skills
    for skill in all_skills:
        if skill not in available_skills:
            result.missing_skills.append(skill)
            result.passed = False

    if result.missing_skills:
        result.errors.append(f"Skills not found in .claude/skills/: {', '.join(result.missing_skills)}")

    # Check 5: No duplicates
    seen = set()
    for skill in all_skills:
        if skill in seen:
            result.duplicate_skills.append(skill)
        seen.add(skill)

    if result.duplicate_skills:
        result.warnings.append(f"Duplicate skills: {', '.join(result.duplicate_skills)}")

    return result


def verify_batch(batch_num: int, available_skills: Set[str]) -> List[VerificationResult]:
    """Verify all files in a batch."""
    if batch_num not in BATCHES:
        print(f"Error: Batch {batch_num} not defined")
        sys.exit(1)

    batch = BATCHES[batch_num]
    results = []

    for rel_path in batch['files']:
        file_path = CLAUDE_DIR / rel_path
        if file_path.exists():
            results.append(verify_file(file_path, available_skills))
        else:
            result = VerificationResult(file_path=rel_path, passed=False)
            result.errors.append("File not found")
            results.append(result)

    return results


def verify_all(available_skills: Set[str]) -> List[VerificationResult]:
    """Verify all agents and commands."""
    results = []

    # Verify agents
    if AGENTS_DIR.exists():
        for file_path in sorted(AGENTS_DIR.glob('*.md')):
            if file_path.name == 'README.md':
                continue
            results.append(verify_file(file_path, available_skills))

    # Verify commands
    if COMMANDS_DIR.exists():
        for file_path in sorted(COMMANDS_DIR.glob('*.md')):
            if file_path.name.endswith('_REFERENCE.md'):
                continue
            results.append(verify_file(file_path, available_skills))

    return results


def print_results(results: List[VerificationResult], verbose: bool = True):
    """Print verification results."""
    passed = [r for r in results if r.passed]
    failed = [r for r in results if not r.passed]

    print("=" * 60)
    print("SKILLS FRONTMATTER VERIFICATION REPORT")
    print("=" * 60)
    print()
    print(f"Total files:  {len(results)}")
    print(f"Passed:       {len(passed)} ✅")
    print(f"Failed:       {len(failed)} ❌")
    print()

    if failed and verbose:
        print("-" * 60)
        print("FAILED FILES:")
        print("-" * 60)
        for r in failed:
            print(f"\n📁 {r.file_path}")
            for error in r.errors:
                print(f"   ❌ {error}")
            for warning in r.warnings:
                print(f"   ⚠️  {warning}")

    if passed and verbose:
        print()
        print("-" * 60)
        print("PASSED FILES:")
        print("-" * 60)
        for r in passed:
            req_count = len(r.required_skills)
            opt_count = len(r.optional_skills)
            print(f"   ✅ {r.file_path} (required: {req_count}, optional: {opt_count})")

    print()
    print("=" * 60)
    if len(failed) == 0:
        print("✅ ALL VERIFICATIONS PASSED")
    else:
        print(f"❌ {len(failed)} FILES NEED ATTENTION")
    print("=" * 60)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Verify skills frontmatter')
    parser.add_argument('--batch', type=int, help='Verify specific batch (1-4)')
    parser.add_argument('--file', type=str, help='Verify single file')
    parser.add_argument('--summary', action='store_true', help='Summary only (no details)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--list-batches', action='store_true', help='List batch definitions')
    args = parser.parse_args()

    if args.list_batches:
        print("Batch Definitions:")
        print("-" * 40)
        for num, batch in BATCHES.items():
            print(f"\nBatch {num}: {batch['name']}")
            for f in batch['files']:
                print(f"  - {f}")
        sys.exit(0)

    available_skills = get_available_skills()
    print(f"Found {len(available_skills)} skills in .claude/skills/")
    print()

    if args.file:
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = CLAUDE_DIR / args.file
        results = [verify_file(file_path, available_skills)]
    elif args.batch:
        print(f"Verifying Batch {args.batch}: {BATCHES[args.batch]['name']}")
        results = verify_batch(args.batch, available_skills)
    else:
        print("Verifying all agents and commands...")
        results = verify_all(available_skills)

    if args.json:
        output = {
            "total": len(results),
            "passed": len([r for r in results if r.passed]),
            "failed": len([r for r in results if not r.passed]),
            "results": [
                {
                    "file": r.file_path,
                    "passed": r.passed,
                    "has_skills_field": r.has_skills_field,
                    "has_required_optional": r.has_required_optional,
                    "required_skills": r.required_skills,
                    "optional_skills": r.optional_skills,
                    "missing_skills": r.missing_skills,
                    "errors": r.errors,
                    "warnings": r.warnings,
                }
                for r in results
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print_results(results, verbose=not args.summary)

    # Exit code
    failed_count = len([r for r in results if not r.passed])
    sys.exit(0 if failed_count == 0 else 1)


if __name__ == '__main__':
    main()
