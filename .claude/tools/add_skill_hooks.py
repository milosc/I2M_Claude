#!/usr/bin/env python3
"""
Add Frontmatter Hooks to Skills

This script adds category-specific hooks to skill frontmatter based on the
Frontmatter_Hooks_Implementation_Plan.md.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List

# Hook Templates by Skill Category
HOOK_TEMPLATES = {
    "orchestration": """hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
      once: true
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "multiagent-parallel": """hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "audit-validation": """hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
      once: true
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "feedback": """hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "documentation": """hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
      once: true
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "state-management": """hooks:
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "utility": """hooks:
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
"""
}

# Skill Categorization
ORCHESTRATION_SKILLS = [
    "discovery", "discovery-multiagent", "prototype", "prototype-multiagent",
    "productspecs", "solarch", "htec-sdd-tasks", "htec-sdd-implement", "htec-sdd-review"
]

MULTIAGENT_PARALLEL_SKILLS = ["discovery-multiagent", "prototype-multiagent"]

AUDIT_VALIDATION_SKILLS = [
    "discovery-audit", "discovery-validate", "prototype-validate",
    "productspecs-validate", "solarch-validate", "integrity-check"
]

FEEDBACK_SKILLS = [
    "discovery-feedback", "prototype-feedback", "productspecs-feedback",
    "solarch-feedback", "htec-sdd-changerequest"
]

DOCUMENTATION_SKILLS = [
    "discovery-docs-all", "discovery-vision", "discovery-strategy", "discovery-roadmap",
    "discovery-kpis", "prototype-export", "productspecs-jira", "solarch-docs"
]

STATE_MANAGEMENT_SKILLS = [
    "discovery-init", "discovery-resume", "discovery-reset",
    "prototype-init", "prototype-resume", "prototype-reset",
    "productspecs-init", "productspecs-resume", "productspecs-reset",
    "solarch-init", "solarch-resume", "solarch-reset"
]

UTILITY_SKILLS = [
    "discovery-status", "prototype-status", "productspecs-status", "solarch-status",
    "discovery-files-created", "agent-status", "agent-cleanup", "traceability-status"
]


def detect_skill_category(skill_name: str) -> str:
    """Detect skill category based on name patterns."""
    if skill_name in MULTIAGENT_PARALLEL_SKILLS:
        return "multiagent-parallel"
    if skill_name in ORCHESTRATION_SKILLS:
        return "orchestration"
    if skill_name in AUDIT_VALIDATION_SKILLS:
        return "audit-validation"
    if skill_name in FEEDBACK_SKILLS:
        return "feedback"
    if skill_name in DOCUMENTATION_SKILLS:
        return "documentation"
    if skill_name in STATE_MANAGEMENT_SKILLS:
        return "state-management"
    if skill_name in UTILITY_SKILLS:
        return "utility"

    # Default to utility for unknown skills
    return "utility"


def add_hooks_to_skill(skill_file: Path, dry_run: bool = False) -> bool:
    """Add hooks to skill frontmatter if not already present."""

    skill_dir = skill_file.parent
    skill_name = skill_dir.name

    # Read file
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)

    if not match:
        # No frontmatter - skip (skills should always have frontmatter)
        print(f"⚠️  No frontmatter: {skill_name}")
        return False

    frontmatter = match.group(1)
    body = match.group(2)

    # Check if hooks already exist
    if 'hooks:' in frontmatter:
        print(f"✅ Already has hooks: {skill_name}")
        return True

    # Detect category
    category = detect_skill_category(skill_name)
    hooks_yaml = HOOK_TEMPLATES.get(category, HOOK_TEMPLATES["utility"])

    # Add hooks to frontmatter
    new_frontmatter = frontmatter.rstrip() + '\n' + hooks_yaml.rstrip()
    new_content = f"---\n{new_frontmatter}\n---\n{body}"

    if dry_run:
        print(f"🔍 [DRY RUN] Would add {category} hooks to: {skill_name}")
        return True

    # Write back
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Added {category} hooks to: {skill_name}")
    return True


def main():
    """Process all skills or specific skill."""
    import argparse

    parser = argparse.ArgumentParser(description="Add frontmatter hooks to skills")
    parser.add_argument("--skill", help="Specific skill directory to process")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--category", help="Only process skills in this category")

    args = parser.parse_args()

    skills_dir = Path(".claude/skills")

    if args.skill:
        # Single skill
        skill_file = skills_dir / args.skill / "SKILL.md"
        if not skill_file.exists():
            print(f"❌ Skill not found: {args.skill}")
            return 1
        add_hooks_to_skill(skill_file, args.dry_run)
        return 0

    # All skills (including nested plugin skills)
    success = 0
    skipped = 0
    failed = 0

    for skill_file in sorted(skills_dir.glob("**/SKILL.md")):
        # Skip copy directories (backups)
        if "/copy" in str(skill_file) or " copy" in str(skill_file):
            continue
        skill_name = skill_file.parent.name

        if args.category:
            if detect_skill_category(skill_name) != args.category:
                continue

        try:
            if add_hooks_to_skill(skill_file, args.dry_run):
                success += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"❌ Error processing {skill_name}: {e}")
            failed += 1

    print(f"\n📊 Summary: {success} successful, {skipped} skipped, {failed} failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
