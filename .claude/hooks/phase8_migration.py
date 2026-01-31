#!/usr/bin/env python3
"""
Phase 8 Migration Script - Migrate all remaining skills
Excludes: Phase 2 (30) + Phase 4 (6) = 36 skills already done
"""

import re
from pathlib import Path

SKILLS_DIR = Path(".claude/skills")

# Already migrated skill directories
SKIP_SKILLS = {
    # Phase 2
    "code-review-bug-hunter", "code-review-security-auditor", "code-review-code-quality",
    "code-review-contracts", "code-review-test-coverage", "code-review-historical",
    "ddd-software-architecture", "executing-plans", "condition-based-waiting",
    "dispatching-parallel-agents", "frontend-design", "generate-image", "canvas-design",
    "doc-coauthoring", "audio-transcription-summarization", "csv-excel-data-wrangler",
    "docx", "pdf", "pptx", "xlsx", "image-ocr-table-extraction",
    "markdown-knowledge-base-composer", "json-schema-validation-transformation",
    "rest-api-client-harness", "theme-factory", "webapp-testing", "sharing-skills",
    "kaizen", "sdd-tech-lead", "sdd-developer",
    # Phase 4
    "Discovery_FactAuditor", "Discovery_FeedbackAnalyzer", "Discovery_FeedbackImplementer",
    "Discovery_FeedbackPlanner", "Discovery_FeedbackRegister", "Discovery_FeedbackValidator",
}

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
    """Migrate a skill file"""

    with open(filepath, 'r') as f:
        content = f.read()

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

    # Skip if already has new hooks
    if "PreToolUse:" in frontmatter_raw or "log-lifecycle.sh" in frontmatter_raw:
        return True

    skill_name = get_skill_name_from_file(frontmatter_raw)
    if not skill_name:
        raise ValueError("No skill name found")

    description = extract_yaml_field(frontmatter_raw, "description")
    model = extract_yaml_field(frontmatter_raw, "model") or "haiku"
    allowed_tools = extract_yaml_field(frontmatter_raw, "allowed-tools") or "All tools"

    # Determine stage
    if "Discovery" in frontmatter_raw or "Discovery" in filepath.parent.name:
        stage = "discovery"
    elif "Prototype" in filepath.parent.name:
        stage = "prototype"
    elif "SolArch" in filepath.parent.name:
        stage = "solarch"
    else:
        stage = "utility"

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
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill {skill_name} started '{{"stage": "{stage}"}}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill {skill_name} ended '{{"stage": "{stage}"}}'"""

    if "## FIRST ACTION" not in body_raw:
        first_action = f"""## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill {skill_name} instruction_start '{{"stage": "{stage}", "method": "instruction-based"}}'
```

---

"""
        body = first_action + body_raw.strip()
    else:
        body = body_raw.strip()

    final_content = f"---\n{new_frontmatter}\n---\n\n{body}\n"

    with open(filepath, 'w') as f:
        f.write(final_content)

    return True

def main():
    migrated = []
    failed = []
    skipped = []

    # Get all skill directories
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name in SKIP_SKILLS:
            skipped.append(skill_dir.name)
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        try:
            migrate_skill(skill_file)
            print(f"✅ {skill_dir.name}")
            migrated.append(skill_dir.name)
        except Exception as e:
            print(f"❌ {skill_dir.name}: {str(e)}")
            failed.append((skill_dir.name, str(e)))

    print(f"\n✅ Migrated: {len(migrated)}")
    print(f"⏭️  Skipped (already done): {len(skipped)}")
    print(f"❌ Failed: {len(failed)}")

if __name__ == "__main__":
    main()
