#!/usr/bin/env python3
"""
Validate skill references in agent and command frontmatter.

This script checks that:
1. All skills referenced in frontmatter exist in .claude/skills/
2. Skills are properly categorized as 'required' or 'optional'
3. Generates a report of missing skills and validation errors

Usage:
    python3 .claude/hooks/validate_skill_references.py [--fix] [--report]

Options:
    --fix       Attempt to auto-fix common issues
    --report    Generate detailed markdown report
    --json      Output results as JSON
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict

# Try to import yaml, fall back to simple regex parsing
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# Find project root (directory containing .claude)
def find_project_root() -> Path:
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / '.claude').exists():
            return current
        current = current.parent
    # Fallback
    return Path(__file__).resolve().parent.parent.parent

PROJECT_ROOT = find_project_root()
CLAUDE_DIR = PROJECT_ROOT / '.claude'
AGENTS_DIR = CLAUDE_DIR / 'agents'
COMMANDS_DIR = CLAUDE_DIR / 'commands'
SKILLS_DIR = CLAUDE_DIR / 'skills'


@dataclass
class SkillReference:
    """A skill reference found in an agent or command."""
    name: str
    category: str  # 'required', 'optional', or 'unknown'
    source: str    # 'frontmatter' or 'prose'
    exists: bool = False


@dataclass
class ValidationResult:
    """Validation result for a single file."""
    file_path: str
    file_type: str  # 'agent' or 'command'
    has_frontmatter_skills: bool = False
    frontmatter_skills: List[SkillReference] = field(default_factory=list)
    prose_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0 and len(self.missing_skills) == 0


@dataclass
class ValidationReport:
    """Complete validation report."""
    total_files: int = 0
    valid_files: int = 0
    invalid_files: int = 0
    files_needing_update: int = 0
    missing_frontmatter_skills: List[str] = field(default_factory=list)
    results: List[ValidationResult] = field(default_factory=list)
    all_skills: List[str] = field(default_factory=list)


def get_available_skills() -> List[str]:
    """Get list of all available skills from .claude/skills/."""
    skills = []
    if not SKILLS_DIR.exists():
        return skills

    for item in SKILLS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            # Check if it has a SKILL.md
            if (item / 'SKILL.md').exists():
                skills.append(item.name)

    return sorted(skills)


def parse_frontmatter(content: str) -> Tuple[Optional[dict], str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return None, content

    # Find the closing ---
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return None, content

    yaml_content = content[3:end_match.start() + 3]
    rest_content = content[end_match.end() + 3:]

    if HAS_YAML:
        try:
            frontmatter = yaml.safe_load(yaml_content)
            return frontmatter, rest_content
        except yaml.YAMLError:
            return None, content
    else:
        # Simple regex-based parsing for skills field
        frontmatter = {}

        # Check for skills field
        skills_match = re.search(r'^skills:\s*(.+?)(?=\n[a-z_-]+:|$)', yaml_content, re.MULTILINE | re.DOTALL)
        if skills_match:
            skills_content = skills_match.group(1).strip()

            # Check if it's a nested structure (required/optional)
            required_match = re.search(r'required:\s*\n((?:\s+-\s+.+\n?)+)', skills_content)
            optional_match = re.search(r'optional:\s*\n((?:\s+-\s+.+\n?)+)', skills_content)

            if required_match or optional_match:
                frontmatter['skills'] = {}
                if required_match:
                    skills_list = re.findall(r'-\s+([^\n]+)', required_match.group(1))
                    frontmatter['skills']['required'] = [s.strip() for s in skills_list]
                if optional_match:
                    skills_list = re.findall(r'-\s+([^\n]+)', optional_match.group(1))
                    frontmatter['skills']['optional'] = [s.strip() for s in skills_list]
            else:
                # Simple string or comma-separated
                frontmatter['skills'] = skills_content

        return frontmatter, rest_content


def extract_prose_skills(content: str) -> List[str]:
    """Extract skill references from prose content."""
    skills = set()

    # Pattern 1: /skill-name invocations
    for match in re.finditer(r'/([a-zA-Z][a-zA-Z0-9_-]+)', content):
        skill_name = match.group(1)
        # Filter out common non-skill patterns
        if not any(x in skill_name.lower() for x in ['discovery-', 'prototype-', 'productspecs-', 'solarch-', 'htec-']):
            if len(skill_name) > 3:
                skills.add(skill_name)

    # Pattern 2: .claude/skills/skill-name references
    for match in re.finditer(r'\.claude/skills/([a-zA-Z][a-zA-Z0-9_-]+)', content):
        skills.add(match.group(1))

    # Pattern 3: Skill tool usage with skill name
    for match in re.finditer(r'[Ss]kill[:\s]+["\']?([a-zA-Z][a-zA-Z0-9_-]+)["\']?', content):
        skills.add(match.group(1))

    # Pattern 4: Discovery_*, Prototype_*, etc. skill names
    for match in re.finditer(r'\b(Discovery_[A-Za-z]+|Prototype_[A-Za-z]+|ProductSpecs_[A-Za-z]+|SolutionArchitecture_[A-Za-z]+|GRC_[a-z-]+|Shared_[A-Za-z_]+)\b', content):
        skills.add(match.group(1))

    return list(skills)


def validate_file(file_path: Path, file_type: str, available_skills: List[str]) -> ValidationResult:
    """Validate a single agent or command file."""
    result = ValidationResult(
        file_path=str(file_path.relative_to(CLAUDE_DIR)),
        file_type=file_type
    )

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        result.errors.append(f"Failed to read file: {e}")
        return result

    # Parse frontmatter
    frontmatter, body = parse_frontmatter(content)

    if frontmatter and 'skills' in frontmatter:
        result.has_frontmatter_skills = True
        skills_data = frontmatter['skills']

        # Handle different formats
        if isinstance(skills_data, dict):
            # New format: {required: [...], optional: [...]}
            for category in ['required', 'optional']:
                if category in skills_data:
                    skill_list = skills_data[category]
                    if isinstance(skill_list, list):
                        for skill in skill_list:
                            exists = skill in available_skills
                            result.frontmatter_skills.append(
                                SkillReference(name=skill, category=category, source='frontmatter', exists=exists)
                            )
                            if not exists:
                                result.missing_skills.append(skill)
        elif isinstance(skills_data, str):
            # Old format: comma-separated string
            result.warnings.append("Skills in frontmatter use old string format. Convert to {required: [], optional: []} format.")
            for skill in skills_data.split(','):
                skill = skill.strip()
                if skill:
                    exists = skill in available_skills
                    result.frontmatter_skills.append(
                        SkillReference(name=skill, category='unknown', source='frontmatter', exists=exists)
                    )
                    if not exists:
                        result.missing_skills.append(skill)
        elif isinstance(skills_data, list):
            # List format without categories
            result.warnings.append("Skills in frontmatter missing required/optional categories.")
            for skill in skills_data:
                exists = skill in available_skills
                result.frontmatter_skills.append(
                    SkillReference(name=skill, category='unknown', source='frontmatter', exists=exists)
                )
                if not exists:
                    result.missing_skills.append(skill)

    # Extract prose skills
    result.prose_skills = extract_prose_skills(body)

    # Check for prose skills not in frontmatter
    frontmatter_skill_names = {s.name for s in result.frontmatter_skills}
    for skill in result.prose_skills:
        if skill not in frontmatter_skill_names:
            # Check if it's a valid skill
            if skill in available_skills:
                result.warnings.append(f"Skill '{skill}' referenced in prose but not in frontmatter")

    return result


def validate_all() -> ValidationReport:
    """Validate all agents and commands."""
    report = ValidationReport()
    available_skills = get_available_skills()
    report.all_skills = available_skills

    # Validate agents
    if AGENTS_DIR.exists():
        for file_path in AGENTS_DIR.glob('*.md'):
            if file_path.name == 'README.md':
                continue
            result = validate_file(file_path, 'agent', available_skills)
            report.results.append(result)
            report.total_files += 1
            if result.is_valid:
                report.valid_files += 1
            else:
                report.invalid_files += 1
            if not result.has_frontmatter_skills and result.prose_skills:
                report.files_needing_update += 1
                report.missing_frontmatter_skills.append(result.file_path)

    # Validate commands
    if COMMANDS_DIR.exists():
        for file_path in COMMANDS_DIR.glob('*.md'):
            if file_path.name.endswith('_REFERENCE.md'):
                continue
            result = validate_file(file_path, 'command', available_skills)
            report.results.append(result)
            report.total_files += 1
            if result.is_valid:
                report.valid_files += 1
            else:
                report.invalid_files += 1
            if not result.has_frontmatter_skills and result.prose_skills:
                report.files_needing_update += 1
                report.missing_frontmatter_skills.append(result.file_path)

    return report


def generate_markdown_report(report: ValidationReport) -> str:
    """Generate a markdown report."""
    lines = [
        "# Skill Reference Validation Report",
        "",
        f"**Generated**: {__import__('datetime').datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total files scanned | {report.total_files} |",
        f"| Valid files | {report.valid_files} |",
        f"| Invalid files | {report.invalid_files} |",
        f"| Files needing frontmatter skills | {report.files_needing_update} |",
        f"| Available skills | {len(report.all_skills)} |",
        "",
    ]

    # Files needing update
    if report.missing_frontmatter_skills:
        lines.extend([
            "## Files Needing Frontmatter Skills",
            "",
            "These files reference skills in prose but don't have a `skills:` field in frontmatter:",
            "",
        ])

        # Group by type
        agents = [f for f in report.missing_frontmatter_skills if f.startswith('agents/')]
        commands = [f for f in report.missing_frontmatter_skills if f.startswith('commands/')]

        if agents:
            lines.append("### Agents")
            lines.append("")
            for f in sorted(agents):
                result = next((r for r in report.results if r.file_path == f), None)
                if result:
                    skills_str = ', '.join(result.prose_skills[:5])
                    if len(result.prose_skills) > 5:
                        skills_str += f" (+{len(result.prose_skills) - 5} more)"
                    lines.append(f"- `{f}`: {skills_str}")
            lines.append("")

        if commands:
            lines.append("### Commands")
            lines.append("")
            for f in sorted(commands):
                result = next((r for r in report.results if r.file_path == f), None)
                if result:
                    skills_str = ', '.join(result.prose_skills[:5])
                    if len(result.prose_skills) > 5:
                        skills_str += f" (+{len(result.prose_skills) - 5} more)"
                    lines.append(f"- `{f}`: {skills_str}")
            lines.append("")

    # Validation errors
    errors = [(r.file_path, r.errors) for r in report.results if r.errors]
    if errors:
        lines.extend([
            "## Validation Errors",
            "",
        ])
        for file_path, file_errors in errors:
            lines.append(f"### `{file_path}`")
            for error in file_errors:
                lines.append(f"- ❌ {error}")
            lines.append("")

    # Missing skills
    missing = [(r.file_path, r.missing_skills) for r in report.results if r.missing_skills]
    if missing:
        lines.extend([
            "## Missing Skills",
            "",
            "These skills are referenced but don't exist in `.claude/skills/`:",
            "",
        ])
        all_missing = set()
        for file_path, skills in missing:
            for skill in skills:
                all_missing.add(skill)
        for skill in sorted(all_missing):
            lines.append(f"- `{skill}`")
        lines.append("")

    # Warnings
    warnings = [(r.file_path, r.warnings) for r in report.results if r.warnings]
    if warnings:
        lines.extend([
            "## Warnings",
            "",
        ])
        for file_path, file_warnings in warnings:
            lines.append(f"### `{file_path}`")
            for warning in file_warnings:
                lines.append(f"- ⚠️ {warning}")
            lines.append("")

    return '\n'.join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Validate skill references in agents and commands')
    parser.add_argument('--report', action='store_true', help='Generate markdown report')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--list-needed', action='store_true', help='List files needing frontmatter skills')
    args = parser.parse_args()

    report = validate_all()

    if args.json:
        # Convert to JSON-serializable format
        output = {
            'total_files': report.total_files,
            'valid_files': report.valid_files,
            'invalid_files': report.invalid_files,
            'files_needing_update': report.files_needing_update,
            'missing_frontmatter_skills': report.missing_frontmatter_skills,
            'results': [
                {
                    'file_path': r.file_path,
                    'file_type': r.file_type,
                    'has_frontmatter_skills': r.has_frontmatter_skills,
                    'frontmatter_skills': [asdict(s) for s in r.frontmatter_skills],
                    'prose_skills': r.prose_skills,
                    'missing_skills': r.missing_skills,
                    'errors': r.errors,
                    'warnings': r.warnings,
                    'is_valid': r.is_valid
                }
                for r in report.results
            ]
        }
        print(json.dumps(output, indent=2))
    elif args.report:
        print(generate_markdown_report(report))
    elif args.list_needed:
        print("Files needing frontmatter skills update:")
        print("=" * 50)
        for f in sorted(report.missing_frontmatter_skills):
            print(f"  {f}")
        print(f"\nTotal: {len(report.missing_frontmatter_skills)} files")
    else:
        # Default: summary output
        print(f"Skill Reference Validation")
        print(f"=" * 40)
        print(f"Total files:           {report.total_files}")
        print(f"Valid:                 {report.valid_files}")
        print(f"Invalid:               {report.invalid_files}")
        print(f"Needing update:        {report.files_needing_update}")
        print()

        if report.invalid_files > 0:
            print("Run with --report for details")
            sys.exit(1)
        else:
            print("✅ All skill references valid")


if __name__ == '__main__':
    main()
