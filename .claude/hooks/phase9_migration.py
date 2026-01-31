#!/usr/bin/env python3
"""
Phase 9 Migration Script - Handle 2 edge cases
Edge case: productspecs-contracts.md (has PreExecution + FIRST ACTION)
"""

import re
from pathlib import Path

COMMANDS_DIR = Path(".claude/commands")

def migrate_edge_case(filepath):
    """Migrate an edge case file that has both legacy and partial new logging"""

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

    # Remove legacy hooks if present
    frontmatter_raw = re.sub(
        r"hooks:\s+PreExecution:.*?PostExecution:.*?--status completed\n",
        "",
        frontmatter_raw,
        flags=re.MULTILINE | re.DOTALL
    )

    description = frontmatter_raw.split("description:")[1].split("\n")[0].strip() if "description:" in frontmatter_raw else "ProductSpecs management"
    argument_hint = "Optional" if "argument-hint:" not in frontmatter_raw else frontmatter_raw.split("argument-hint:")[1].split("\n")[0].strip()
    model = "claude-sonnet-4-5-20250929"
    allowed_tools = "Read, Write, Edit, Bash, Grep, Glob"

    cmd_name = "/productspecs-contracts"

    new_hooks = f"""hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} started '{{"stage": "productspecs"}}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command {cmd_name} ended '{{"stage": "productspecs"}}'
"""

    frontmatter = frontmatter_raw.rstrip() + "\n" + new_hooks

    body = body_raw.strip()

    # Reconstruct
    final_content = f"---\n{frontmatter}\n---\n\n{body}\n"

    with open(filepath, 'w') as f:
        f.write(final_content)

    return True

def main():
    print("Phase 9: Processing edge cases...")

    # Edge case: productspecs-contracts.md
    edge_case_file = COMMANDS_DIR / "productspecs-contracts.md"

    if edge_case_file.exists():
        try:
            migrate_edge_case(edge_case_file)
            print(f"✅ productspecs-contracts.md")
        except Exception as e:
            print(f"❌ productspecs-contracts.md: {str(e)}")
    else:
        print(f"⏭️  productspecs-contracts.md (not found, skipped)")

    print(f"\n✅ Phase 9 complete")

if __name__ == "__main__":
    main()
