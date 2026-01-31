#!/usr/bin/env python3
"""
Phase 1 Migration Script v2 - Improved version with better handling
"""

import os
import re
from pathlib import Path

COMMANDS_DIR = Path(".claude/commands")

# Phase 1 high-traffic commands
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

def get_command_name_from_filename(filename):
    """Convert filename to command name"""
    return "/" + filename.replace(".md", "")

def migrate_command(filepath):
    """Migrate a single command file"""

    with open(filepath, 'r') as f:
        content = f.read()

    cmd_name = get_command_name_from_filename(filepath.name)

    # Step 1: Extract frontmatter
    if not content.startswith("---"):
        raise ValueError(f"File doesn't start with ---")

    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"Invalid frontmatter")

    frontmatter = parts[1]
    body = parts[2]

    # Step 2: Replace hooks in frontmatter
    # Remove old hooks section if exists
    frontmatter = re.sub(
        r"hooks:\s+PreExecution:.*?PostExecution:.*?--status completed\n",
        "",
        frontmatter,
        flags=re.MULTILINE | re.DOTALL
    )

    # Add new hooks
    new_hooks = f"""hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} started '{{"stage": "utility"}}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} ended '{{"stage": "utility"}}'
"""

    # Insert hooks at the end of frontmatter
    frontmatter = frontmatter.rstrip() + "\n" + new_hooks

    # Step 3: Clean up body - remove legacy logging sections
    # Remove Step 0 logging section
    body = re.sub(
        r"### Step 0: Log Command Start \(MANDATORY\)\n\n```bash\n#.*?\necho\s+\"📝[^\"]*\"\n```\n+",
        "",
        body,
        flags=re.MULTILINE | re.DOTALL
    )

    # Remove Step Final logging section
    body = re.sub(
        r"### Step Final: Log Command End \(MANDATORY\)\n\n```bash\n#.*?echo\s+\"✅[^\"]*\"\n```\n*",
        "",
        body,
        flags=re.MULTILINE | re.DOTALL
    )

    # Step 4: Add FIRST ACTION section if not already present
    if "## FIRST ACTION" not in body:
        first_action = f"""## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} instruction_start '{{"stage": "utility", "method": "instruction-based"}}'
```

---

"""
        # Insert after initial newlines
        body = body.lstrip() + "\n"
        body = first_action + body

    # Step 5: Reconstruct file
    final_content = f"---{frontmatter}---{body}"

    with open(filepath, 'w') as f:
        f.write(final_content)

    return True

def main():
    migrated = []
    failed = []

    for cmd_file in PHASE1_COMMANDS:
        filepath = COMMANDS_DIR / cmd_file

        if not filepath.exists():
            failed.append((cmd_file, "File not found"))
            continue

        try:
            migrate_command(filepath)
            print(f"✅ MIGRATED: {cmd_file}")
            migrated.append(cmd_file)
        except Exception as e:
            print(f"❌ FAILED: {cmd_file} - {str(e)}")
            failed.append((cmd_file, str(e)))

    print(f"\n{'='*60}")
    print(f"Phase 1 Migration v2 Summary")
    print(f"{'='*60}")
    print(f"✅ Migrated: {len(migrated)}/18")
    print(f"❌ Failed: {len(failed)}/18")

if __name__ == "__main__":
    main()
