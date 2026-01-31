#!/usr/bin/env python3
"""
Skill Frontmatter Validation Script

Validates YAML frontmatter in skill files for completeness and correctness.
Part of the Skill Optimization Plan (architecture/skill_optimization_plan.md).

Usage:
    python3 validate_skill_frontmatter.py [--skill <path>] [--all] [--report]
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Valid values for frontmatter fields
VALID_MODELS = {'sonnet', 'haiku', 'opus'}
VALID_AGENTS = {'general-purpose', 'Explore', 'Plan', 'Bash'}
VALID_TOOLS = {
    'Read', 'Write', 'Edit', 'Glob', 'Grep', 'Bash',
    'Task', 'WebFetch', 'WebSearch', 'LSP', 'NotebookEdit',
    'TodoWrite', 'AskUserQuestion', 'Skill'
}

# Fields configuration
REQUIRED_FIELDS = {'name', 'description'}
OPTIONAL_FIELDS = {'model', 'allowed-tools', 'context', 'agent', 'disable-model-invocation', 'mode', 'version', 'license'}
OPTIMIZATION_FIELDS = {'model', 'allowed-tools', 'context', 'agent'}  # Fields we're adding in optimization


class ValidationResult:
    """Stores validation results for a single skill."""

    def __init__(self, skill_path: str):
        self.skill_path = skill_path
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.frontmatter: Optional[Dict] = None

    def add_error(self, msg: str):
        self.errors.append(msg)

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def add_info(self, msg: str):
        self.info.append(msg)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    @property
    def is_optimized(self) -> bool:
        """Check if skill has optimization fields populated."""
        if not self.frontmatter:
            return False
        return all(field in self.frontmatter for field in OPTIMIZATION_FIELDS)


def extract_frontmatter(file_path: str) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Extract YAML frontmatter from skill file.

    Parses simple YAML frontmatter (key: value pairs) without requiring PyYAML.

    Returns:
        (frontmatter_dict, error_message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match YAML frontmatter (--- ... ---)
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None, "No YAML frontmatter found"

        frontmatter_str = match.group(1)

        # Parse simple YAML (key: value pairs)
        frontmatter = {}
        for line in frontmatter_str.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # Match "key: value" pattern
            key_value_match = re.match(r'^([a-zA-Z0-9_-]+):\s*(.*)$', line)
            if key_value_match:
                key = key_value_match.group(1)
                value = key_value_match.group(2).strip()
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                frontmatter[key] = value

        if not frontmatter:
            return None, "Frontmatter is empty or invalid"

        return frontmatter, None

    except FileNotFoundError:
        return None, f"File not found: {file_path}"
    except Exception as e:
        return None, f"Unexpected error: {e}"


def validate_skill(skill_path: str) -> ValidationResult:
    """
    Validate a single skill file.

    Args:
        skill_path: Path to SKILL.md file

    Returns:
        ValidationResult object
    """
    result = ValidationResult(skill_path)

    # Extract frontmatter
    frontmatter, error = extract_frontmatter(skill_path)
    if error:
        result.add_error(error)
        return result

    result.frontmatter = frontmatter

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            result.add_error(f"Missing required field: {field}")
        elif not frontmatter[field]:
            result.add_error(f"Required field is empty: {field}")

    # Validate model field
    if 'model' in frontmatter:
        model = frontmatter['model']
        if model not in VALID_MODELS:
            result.add_error(f"Invalid model value: '{model}'. Must be one of {VALID_MODELS}")
    else:
        result.add_warning("Missing 'model' field (optimization target)")

    # Validate allowed-tools field
    if 'allowed-tools' in frontmatter:
        tools_str = frontmatter['allowed-tools']
        if tools_str:
            tools = [t.strip() for t in tools_str.split(',')]
            invalid_tools = [t for t in tools if t not in VALID_TOOLS]
            if invalid_tools:
                result.add_error(f"Invalid tools: {invalid_tools}. Valid tools: {VALID_TOOLS}")
        else:
            result.add_warning("'allowed-tools' field is empty")
    else:
        result.add_warning("Missing 'allowed-tools' field (optimization target)")

    # Validate context field
    if 'context' in frontmatter:
        context = frontmatter['context']
        if context and context != 'fork':
            result.add_error(f"Invalid context value: '{context}'. Must be 'fork' or empty")
    else:
        result.add_info("Missing 'context' field (may be intentional for Tier 2 skills)")

    # Validate agent field
    if 'agent' in frontmatter:
        agent = frontmatter['agent']
        if agent not in VALID_AGENTS:
            result.add_error(f"Invalid agent value: '{agent}'. Must be one of {VALID_AGENTS}")
    else:
        result.add_warning("Missing 'agent' field (optimization target)")

    # Check for unknown fields
    all_known_fields = REQUIRED_FIELDS | OPTIONAL_FIELDS
    unknown_fields = set(frontmatter.keys()) - all_known_fields
    if unknown_fields:
        result.add_warning(f"Unknown fields: {unknown_fields}")

    # Info about optimization status
    if result.is_optimized:
        result.add_info("✅ Skill is fully optimized")
    else:
        missing = [f for f in OPTIMIZATION_FIELDS if f not in frontmatter]
        result.add_info(f"⏳ Optimization fields missing: {missing}")

    return result


def find_all_skills(base_dir: str = '.claude/skills') -> List[str]:
    """
    Find all SKILL.md files in the skills directory.

    Args:
        base_dir: Base directory to search

    Returns:
        List of paths to SKILL.md files
    """
    skills = []
    skills_path = Path(base_dir)

    if not skills_path.exists():
        print(f"Error: Skills directory not found: {base_dir}")
        return []

    for skill_dir in skills_path.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / 'SKILL.md'
            if skill_file.exists():
                skills.append(str(skill_file))

    return sorted(skills)


def print_result(result: ValidationResult, verbose: bool = False):
    """Print validation result for a single skill."""
    skill_name = Path(result.skill_path).parent.name

    # Status symbol
    if not result.is_valid:
        status = "❌"
    elif result.warnings:
        status = "⚠️"
    elif result.is_optimized:
        status = "✅"
    else:
        status = "⏳"

    print(f"\n{status} {skill_name}")
    print(f"   Path: {result.skill_path}")

    # Errors
    for error in result.errors:
        print(f"   ❌ ERROR: {error}")

    # Warnings
    if verbose or not result.is_valid:
        for warning in result.warnings:
            print(f"   ⚠️  WARNING: {warning}")

    # Info
    if verbose:
        for info in result.info:
            print(f"   ℹ️  INFO: {info}")


def generate_report(results: List[ValidationResult]) -> Dict:
    """Generate summary report."""
    total = len(results)
    valid = sum(1 for r in results if r.is_valid)
    optimized = sum(1 for r in results if r.is_optimized)
    with_errors = sum(1 for r in results if r.errors)
    with_warnings = sum(1 for r in results if r.warnings and r.is_valid)

    report = {
        'total_skills': total,
        'valid': valid,
        'invalid': with_errors,
        'with_warnings': with_warnings,
        'optimized': optimized,
        'pending_optimization': total - optimized,
        'optimization_progress': f"{(optimized/total*100):.1f}%" if total > 0 else "0%"
    }

    return report


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Validate skill frontmatter')
    parser.add_argument('--skill', help='Path to specific SKILL.md file')
    parser.add_argument('--all', action='store_true', help='Validate all skills')
    parser.add_argument('--report', action='store_true', help='Generate summary report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--base-dir', default='.claude/skills', help='Base skills directory')

    args = parser.parse_args()

    # Collect skills to validate
    skills_to_validate = []

    if args.skill:
        skills_to_validate = [args.skill]
    elif args.all:
        skills_to_validate = find_all_skills(args.base_dir)
        if not skills_to_validate:
            print("No skills found!")
            return 1
    else:
        parser.print_help()
        return 0

    # Validate skills
    results = []
    for skill_path in skills_to_validate:
        result = validate_skill(skill_path)
        results.append(result)

        if not args.json and not args.report:
            print_result(result, verbose=args.verbose)

    # Generate report
    if args.report or args.all:
        report = generate_report(results)

        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print("\n" + "="*60)
            print("VALIDATION SUMMARY")
            print("="*60)
            print(f"Total Skills:            {report['total_skills']}")
            print(f"Valid:                   {report['valid']} ✅")
            print(f"Invalid:                 {report['invalid']} ❌")
            print(f"With Warnings:           {report['with_warnings']} ⚠️")
            print(f"Fully Optimized:         {report['optimized']} ✅")
            print(f"Pending Optimization:    {report['pending_optimization']} ⏳")
            print(f"Optimization Progress:   {report['optimization_progress']}")
            print("="*60)

    # Exit code
    invalid_count = sum(1 for r in results if not r.is_valid)
    return 1 if invalid_count > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
