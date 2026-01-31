#!/usr/bin/env python3
"""
Phase 1 Migration Script v3 - Clean reconstruction approach
"""

import re
from pathlib import Path

COMMANDS_DIR = Path(".claude/commands")

PHASE1_COMMANDS = [
    "create-skill.md",
    "create-command.md",
    "create-hook.md",
    "htec-libraries-init.md",
    "htec-sdd-changerequest.md",
    "htec-sdd-implement.md",
    "htec-sdd-init.md",
    "agent-spawn.md",
    "agent-status.md",
    "agent-cleanup.md",
    "document.md",
    "fix-tests.md",
    "critique.md",
    "analyze-issue.md",
    "attach-review-to-pr.md",
    "build-mcp.md",
    "apply-anthropic-skill-best-practices.md",
    "add-typescript-best-practices.md",
]

def get_command_name(filename):
    return "/" + filename.replace(".md", "")

def extract_yaml_field(text, field):
    """Extract a specific field from YAML frontmatter"""
    pattern = rf"^{field}:\s*(.*)$"
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else None

def migrate_command(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Parse: extract frontmatter
    if not content.startswith("---"):
        raise ValueError("No frontmatter")

    try:
        end_marker = content.find("---", 3)
        if end_marker == -1:
            raise ValueError("No closing ---")

        frontmatter_raw = content[3:end_marker].strip()
        body_raw = content[end_marker+3:].lstrip()
    except:
        raise ValueError("Failed to parse")

    # Extract YAML fields
    description = extract_yaml_field(frontmatter_raw, "description")
    argument_hint = extract_yaml_field(frontmatter_raw, "argument-hint")
    model = extract_yaml_field(frontmatter_raw, "model") or "claude-sonnet-4-5-20250929"
    allowed_tools = extract_yaml_field(frontmatter_raw, "allowed-tools") or "Read, Write, Edit, Bash, Grep, Glob"

    cmd_name = get_command_name(filepath.name)

    # Build new frontmatter
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
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} started '{{"stage": "utility"}}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} ended '{{"stage": "utility"}}'"""

    # Clean body: remove legacy logging sections
    body = body_raw

    # Remove Step 0 and Step Final sections
    body = re.sub(
        r"### Step 0: Log Command Start.*?```\n\n",
        "",
        body,
        flags=re.MULTILINE | re.DOTALL
    )
    body = re.sub(
        r"### Step Final: Log Command End.*?```\s*$",
        "",
        body,
        flags=re.MULTILINE | re.DOTALL
    )

    # Remove duplicate FIRST ACTION sections if they exist
    body = re.sub(
        r"## FIRST ACTION \(MANDATORY\).*?---\n\n+",
        "",
        body,
        flags=re.MULTILINE | re.DOTALL
    )

    body = body.strip()

    # Add FIRST ACTION section at beginning
    first_action = f"""## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} instruction_start '{{"stage": "utility", "method": "instruction-based"}}'
```

---

"""

    body = first_action + body

    # Reconstruct file
    final_content = f"---\n{new_frontmatter}\n---\n\n{body}\n"

    with open(filepath, 'w') as f:
        f.write(final_content)

    return True

def main():
    migrated = []
    failed = []

    for cmd_file in PHASE1_COMMANDS:
        filepath = COMMANDS_DIR / cmd_file

        if not filepath.exists():
            failed.append((cmd_file, "Not found"))
            continue

        try:
            migrate_command(filepath)
            print(f"✅ {cmd_file}")
            migrated.append(cmd_file)
        except Exception as e:
            print(f"❌ {cmd_file}: {str(e)}")
            failed.append((cmd_file, str(e)))

    print(f"\n✅ Migrated: {len(migrated)}/18")
    print(f"❌ Failed: {len(failed)}/18")

if __name__ == "__main__":
    main()
