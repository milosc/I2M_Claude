#!/usr/bin/env python3
"""
Update skill frontmatter to conform to logging standards.
Generated: 2026-01-30

This script updates SKILL.md files to include:
- model: haiku or sonnet
- allowed-tools: appropriate tools for the skill
- hooks: PreToolUse and Stop lifecycle logging hooks
"""

import os
import re
import sys
from pathlib import Path

SKILLS_DIR = Path(".claude/skills")

# Skill configurations: skill_name -> (model, stage, allowed_tools)
SKILL_CONFIGS = {
    # SECURITY skills (8)
    "SECURITY_vulnerability-scanner": ("sonnet", "utility", "Read, Grep, Glob, Bash"),
    "SECURITY_api-security-best-practices": ("sonnet", "utility", "Read, Grep, Glob"),
    "SECURITY_top-web-vulnerabilities": ("sonnet", "utility", "Read, Grep, Glob"),
    "SECURITY_broken-authentication": ("sonnet", "utility", "Read, Grep, Glob, Bash"),
    "SECURITY_sql-injection-testing": ("sonnet", "utility", "Read, Grep, Glob, Bash"),
    "SECURITY_xss-html-injection": ("sonnet", "utility", "Read, Grep, Glob"),
    "SECURITY_idor-testing": ("sonnet", "utility", "Read, Grep, Glob"),
    "SECURITY_file-uploads": ("sonnet", "utility", "Read, Grep, Glob"),

    # GRC skills (13)
    "GRC_capa-officer": ("sonnet", "utility", "Read, Grep, Glob, Write"),
    "GRC_data-privacy-compliance": ("sonnet", "utility", "Read, Grep, Glob, Write"),
    "GRC_fda-consultant-specialist": ("sonnet", "utility", "Read, Grep, Glob, Write"),
    "GRC_gdpr-dsgvo-expert": ("sonnet", "utility", "Read, Grep, Glob, Write"),
    "GRC_information-security-manager-iso27001": ("sonnet", "utility", "Read, Grep, Glob, Write"),
    "GRC_isms-audit-expert": ("sonnet", "utility", "Read, Grep, Glob, Write"),
    "GRC_mdr-745-specialist": ("sonnet", "utility", "Read, Grep, Glob, Write"),
    "GRC_qms-audit-expert": ("sonnet", "utility", "Read, Grep, Glob, Write"),
    "GRC_quality-documentation-manager": ("sonnet", "utility", "Read, Grep, Glob, Write"),
    "GRC_quality-manager-qmr": ("sonnet", "utility", "Read, Grep, Glob, Write"),
    "GRC_quality-manager-qms-iso13485": ("sonnet", "utility", "Read, Grep, Glob, Write"),
    "GRC_regulatory-affairs-head": ("sonnet", "utility", "Read, Grep, Glob, Write"),
    "GRC_risk-management-specialist": ("sonnet", "utility", "Read, Grep, Glob, Write"),

    # API skills (2)
    "api-documentation-generator": ("sonnet", "prototype", "Read, Grep, Glob, Write"),
    "api-integration-specialist": ("sonnet", "prototype", "Read, Grep, Glob, Write, Bash"),

    # Design/UI skills (5)
    "ui-design-system": ("sonnet", "prototype", "Read, Grep, Glob, Write"),
    "ui-ux-pro-max": ("sonnet", "prototype", "Read, Grep, Glob, Write"),
    "web-design-guidelines": ("sonnet", "prototype", "Read, Grep, Glob"),
    "mobile-design": ("sonnet", "prototype", "Read, Grep, Glob"),
    "tailwind-patterns": ("sonnet", "prototype", "Read, Grep, Glob, Write"),

    # GitHub skills (5)
    "github_finishing-a-development-branch": ("haiku", "implementation", "Read, Bash, Grep"),
    "github_git-pushing": ("haiku", "implementation", "Read, Bash"),
    "github_github-workflow-automation": ("haiku", "implementation", "Read, Write, Bash, Grep"),
    "github_address-github-comments": ("haiku", "implementation", "Read, Bash, Grep"),
    "github_create-worktree-skill": ("haiku", "implementation", "Read, Bash"),

    # Database skills (2)
    "database-schema-designer": ("sonnet", "prototype", "Read, Grep, Glob, Write"),
    "postgres-best-practices": ("sonnet", "prototype", "Read, Grep, Glob"),

    # Utility skills (17)
    "changelog-generator": ("haiku", "utility", "Read, Grep, Glob, Write"),
    "requirements-clarity": ("sonnet", "discovery", "Read, Grep, Glob, Write"),
    "plugin-forge": ("haiku", "utility", "Read, Write, Bash, Glob"),
    "plugin-structure": ("haiku", "utility", "Read, Glob"),
    "plugin-settings": ("haiku", "utility", "Read, Glob"),
    "architecture": ("sonnet", "solarch", "Read, Grep, Glob, Write"),
    "frontend-design": ("sonnet", "prototype", "Read, Grep, Glob"),
    "ux-researcher-designer": ("sonnet", "discovery", "Read, Grep, Glob, Write"),
    "lint-and-validate": ("haiku", "utility", "Read, Bash, Grep, Glob"),
    "planning-with-files": ("sonnet", "utility", "Read, Write, Glob"),
    "draw-io": ("haiku", "utility", "Read, Write"),
    "error-resolver": ("sonnet", "utility", "Read, Grep, Glob, Bash"),
    "clean-code": ("haiku", "utility", "Read, Grep, Glob"),
}


def generate_frontmatter(skill_name: str, description: str, model: str, stage: str, allowed_tools: str) -> str:
    """Generate YAML frontmatter with lifecycle logging hooks."""
    return f'''---
name: {skill_name}
description: {description}
model: {model}
allowed-tools: {allowed_tools}
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill {skill_name} started '{{"stage": "{stage}"}}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill {skill_name} ended '{{"stage": "{stage}"}}'
---'''


def update_skill_frontmatter(skill_path: Path, model: str, stage: str, allowed_tools: str) -> bool:
    """Update a skill's frontmatter with conformant logging hooks."""
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        print(f"  ⚠️  SKILL.md not found: {skill_path}")
        return False

    content = skill_file.read_text()
    skill_name = skill_path.name

    # Extract existing frontmatter and body
    fm_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not fm_match:
        print(f"  ⚠️  No frontmatter found: {skill_path}")
        return False

    fm_content = fm_match.group(1)
    body = fm_match.group(2)

    # Extract existing name and description
    name_match = re.search(r'^name:\s*(.+)$', fm_content, re.MULTILINE)
    desc_match = re.search(r'^description:\s*(.+)$', fm_content, re.MULTILINE)

    existing_name = name_match.group(1).strip() if name_match else skill_name
    existing_desc = desc_match.group(1).strip() if desc_match else f"Skill for {skill_name}"

    # Generate new frontmatter
    new_frontmatter = generate_frontmatter(
        skill_name=existing_name,
        description=existing_desc,
        model=model,
        stage=stage,
        allowed_tools=allowed_tools
    )

    # Write updated file
    new_content = f"{new_frontmatter}\n{body}"
    skill_file.write_text(new_content)
    print(f"  ✅ Updated: {skill_name} (model={model}, stage={stage})")
    return True


def main():
    print("=" * 60)
    print("  Updating Skill Frontmatter for Lifecycle Logging")
    print("=" * 60)
    print()

    if not SKILLS_DIR.exists():
        print(f"ERROR: Skills directory not found: {SKILLS_DIR}")
        sys.exit(1)

    updated = 0
    failed = 0
    not_found = 0

    for skill_name, (model, stage, allowed_tools) in SKILL_CONFIGS.items():
        skill_path = SKILLS_DIR / skill_name
        if skill_path.exists():
            if update_skill_frontmatter(skill_path, model, stage, allowed_tools):
                updated += 1
            else:
                failed += 1
        else:
            print(f"  ⚠️  Skill folder not found: {skill_name}")
            not_found += 1

    print()
    print("=" * 60)
    print(f"  Results: {updated} updated, {failed} failed, {not_found} not found")
    print("=" * 60)

    if failed > 0 or not_found > 0:
        print("\nWARNING: Some skills could not be updated.")
        print("This may be expected if skills were already deleted.")


if __name__ == "__main__":
    main()
