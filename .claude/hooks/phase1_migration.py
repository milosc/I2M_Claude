#!/usr/bin/env python3
"""
Phase 1 Migration Script - Migrate 18 remaining high-traffic commands
to deterministic lifecycle logging.
"""

import os
import re
from pathlib import Path

COMMANDS_DIR = Path(".claude/commands")

# Phase 1 high-traffic commands (minus commit.md and create-pr.md already done)
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
    """Convert filename to command name (e.g., create-skill.md -> /create-skill)"""
    return "/" + filename.replace(".md", "")

def migrate_command(filepath):
    """Migrate a single command file to deterministic logging"""

    with open(filepath, 'r') as f:
        content = f.read()

    # Extract command name from filename
    cmd_name = get_command_name_from_filename(filepath.name)

    # Pattern 1: Replace legacy hooks
    legacy_hooks_pattern = r"hooks:\s+PreExecution:.*?--command-name\s+\S+[^\n]*\n\s+PostExecution:.*?--status completed"
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
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} ended '{{"stage": "utility"}}'"""

    content = re.sub(legacy_hooks_pattern, new_hooks, content, flags=re.MULTILINE | re.DOTALL)

    # Pattern 2: Add FIRST ACTION section after frontmatter, before first h1
    if "---" in content:
        parts = content.split("---", 2)  # Split on first 2 occurrences of ---
        if len(parts) >= 3:
            frontmatter = parts[1]
            rest = "---".join(parts[2:])

            first_action = f"""## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} instruction_start '{{"stage": "utility", "method": "instruction-based"}}'
```

---

"""

            # Only add if not already present
            if "## FIRST ACTION" not in rest:
                rest = first_action + rest

            content = f"---{frontmatter}---{rest}"

    # Pattern 3: Remove legacy Step 0 logging section
    step0_pattern = r"### Step 0: Log Command Start \(MANDATORY\).*?```\n\necho\s+\"📝[^\"]*\"\n```\n\n"
    content = re.sub(step0_pattern, "", content, flags=re.MULTILINE | re.DOTALL)

    # Pattern 4: Remove legacy Step Final logging section
    step_final_pattern = r"### Step Final: Log Command End \(MANDATORY\).*?echo\s+\"✅[^\"]*\"\n```$"
    content = re.sub(step_final_pattern, "", content, flags=re.MULTILINE | re.DOTALL)

    # Write back
    with open(filepath, 'w') as f:
        f.write(content)

    return True

def main():
    migrated = []
    failed = []

    for cmd_file in PHASE1_COMMANDS:
        filepath = COMMANDS_DIR / cmd_file

        if not filepath.exists():
            print(f"⚠️  SKIPPED: {cmd_file} - File not found")
            failed.append(cmd_file)
            continue

        try:
            migrate_command(filepath)
            print(f"✅ MIGRATED: {cmd_file}")
            migrated.append(cmd_file)
        except Exception as e:
            print(f"❌ FAILED: {cmd_file} - {str(e)}")
            failed.append(cmd_file)

    print(f"\n{'='*60}")
    print(f"Phase 1 Migration Summary")
    print(f"{'='*60}")
    print(f"✅ Migrated: {len(migrated)}/18")
    print(f"❌ Failed: {len(failed)}/18")

    if failed:
        print(f"\nFailed files:")
        for f in failed:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
