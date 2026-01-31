#!/usr/bin/env python3
"""
Phase 7 Migration Script - Migrate 72 remaining commands
Excludes: Phase 1 (20), Phase 3 (7) = 27 commands already done
"""

import re
from pathlib import Path

COMMANDS_DIR = Path(".claude/commands")

# Already migrated
SKIP_COMMANDS = {
    # Phase 1
    "commit.md", "create-pr.md", "create-skill.md", "create-command.md",
    "create-hook.md", "htec-libraries-init.md", "htec-sdd-changerequest.md",
    "htec-sdd-implement.md", "htec-sdd-init.md", "agent-spawn.md",
    "agent-status.md", "agent-cleanup.md", "document.md", "fix-tests.md",
    "critique.md", "analyze-issue.md", "attach-review-to-pr.md",
    "build-mcp.md", "apply-anthropic-skill-best-practices.md",
    "add-typescript-best-practices.md",
    # Phase 3
    "discovery-readme.md", "discovery-sample-data.md", "discovery-summary.md",
    "discovery-trace.md", "discovery-validate.md", "discovery-validation.md",
    "discovery-vision.md",
}

def get_command_name(filename):
    return "/" + filename.replace(".md", "")

def extract_yaml_field(text, field):
    """Extract a specific field from YAML"""
    pattern = rf"^{field}:\s*(.*)$"
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else None

def migrate_command(filepath):
    """Migrate a command file"""

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
        return True  # Already migrated

    description = extract_yaml_field(frontmatter_raw, "description")
    argument_hint = extract_yaml_field(frontmatter_raw, "argument-hint")
    model = extract_yaml_field(frontmatter_raw, "model") or "claude-sonnet-4-5-20250929"
    allowed_tools = extract_yaml_field(frontmatter_raw, "allowed-tools") or "Read, Write, Edit, Bash, Grep, Glob"

    cmd_name = get_command_name(filepath.name)

    # Determine stage
    if "discovery" in str(filepath):
        stage = "discovery"
    elif "prototype" in str(filepath):
        stage = "prototype"
    elif "solarch" in str(filepath) or "solarch-" in filepath.name:
        stage = "solarch"
    elif "htec-sdd" in filepath.name or "productspecs" in str(filepath):
        stage = "implementation"
    else:
        stage = "utility"

    new_frontmatter = f"""description: {description}
argument-hint: {argument_hint}
model: {model}
allowed-tools: {allowed_tools}
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} started '{{"stage": "{stage}"}}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} ended '{{"stage": "{stage}"}}'"""

    body = body_raw
    body = re.sub(r"### Step 0: Log Command Start.*?```\n\n", "", body, flags=re.MULTILINE | re.DOTALL)
    body = re.sub(r"### Step Final: Log Command End.*?```\s*$", "", body, flags=re.MULTILINE | re.DOTALL)
    body = re.sub(r"## FIRST ACTION \(MANDATORY\).*?---\n\n+", "", body, flags=re.MULTILINE | re.DOTALL)
    body = body.strip()

    first_action = f"""## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} instruction_start '{{"stage": "{stage}", "method": "instruction-based"}}'
```

---

"""

    body = first_action + body
    final_content = f"---\n{new_frontmatter}\n---\n\n{body}\n"

    with open(filepath, 'w') as f:
        f.write(final_content)

    return True

def main():
    migrated = []
    failed = []
    skipped = []

    # Get all .md files in commands dir
    for cmd_file in sorted(COMMANDS_DIR.glob("*.md")):
        if cmd_file.name in SKIP_COMMANDS:
            skipped.append(cmd_file.name)
            continue

        try:
            migrate_command(cmd_file)
            print(f"✅ {cmd_file.name}")
            migrated.append(cmd_file.name)
        except Exception as e:
            print(f"❌ {cmd_file.name}: {str(e)}")
            failed.append((cmd_file.name, str(e)))

    print(f"\n✅ Migrated: {len(migrated)}")
    print(f"⏭️  Skipped (already done): {len(skipped)}")
    print(f"❌ Failed: {len(failed)}")

if __name__ == "__main__":
    main()
