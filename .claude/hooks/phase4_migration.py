#!/usr/bin/env python3
"""
Phase 4 Migration Script - Migrate 6 discovery skills
"""

import re
from pathlib import Path

SKILLS_DIR = Path(".claude/skills")

# Phase 4 discovery skills
PHASE4_SKILLS = [
    "Discovery_FactAuditor",
    "Discovery_FeedbackAnalyzer",
    "Discovery_FeedbackImplementer",
    "Discovery_FeedbackPlanner",
    "Discovery_FeedbackRegister",
    "Discovery_FeedbackValidator",
]

def get_skill_name_from_file(content):
    """Extract skill name from YAML"""
    match = re.search(r"^name:\s*(.+?)$", content, re.MULTILINE)
    return match.group(1).strip() if match else None

def extract_yaml_field(text, field):
    """Extract a specific field from YAML"""
    pattern = rf"^{field}:\s*(.*)$"
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else None

def migrate_skill(filepath):
    """Migrate a discovery skill file"""

    with open(filepath, 'r') as f:
        content = f.read()

    # Parse frontmatter
    if not content.startswith("---"):
        raise ValueError("No frontmatter")

    try:
        end_marker = content.find("---", 3)
        if end_marker == -1:
            raise ValueError("No closing ---")

        frontmatter_raw = content[3:end_marker].strip()
        body_raw = content[end_marker+3:].lstrip()
    except:
        raise ValueError("Parse failed")

    # Extract fields
    skill_name = get_skill_name_from_file(frontmatter_raw)
    if not skill_name:
        raise ValueError("No skill name found")

    description = extract_yaml_field(frontmatter_raw, "description")
    model = extract_yaml_field(frontmatter_raw, "model") or "haiku"
    allowed_tools = extract_yaml_field(frontmatter_raw, "allowed-tools") or "Read, Grep, Glob"

    # Build new frontmatter with hooks
    new_frontmatter = f"""name: {skill_name}
description: {description}
model: {model}
allowed-tools: {allowed_tools}
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill {skill_name} started '{{"stage": "discovery"}}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill {skill_name} ended '{{"stage": "discovery"}}'"""

    # Add FIRST ACTION if not present
    if "## FIRST ACTION" not in body_raw:
        first_action = f"""## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill {skill_name} instruction_start '{{"stage": "discovery", "method": "instruction-based"}}'
```

---

"""
        body = first_action + body_raw.strip()
    else:
        body = body_raw.strip()

    # Reconstruct file
    final_content = f"---\n{new_frontmatter}\n---\n\n{body}\n"

    with open(filepath, 'w') as f:
        f.write(final_content)

    return True

def main():
    migrated = []
    failed = []

    for skill_dir in PHASE4_SKILLS:
        skill_path = SKILLS_DIR / skill_dir / "SKILL.md"

        if not skill_path.exists():
            failed.append((skill_dir, "SKILL.md not found"))
            continue

        try:
            migrate_skill(skill_path)
            print(f"✅ {skill_dir}")
            migrated.append(skill_dir)
        except Exception as e:
            print(f"❌ {skill_dir}: {str(e)}")
            failed.append((skill_dir, str(e)))

    print(f"\n✅ Migrated: {len(migrated)}/6")
    print(f"❌ Failed: {len(failed)}/6")

if __name__ == "__main__":
    main()
