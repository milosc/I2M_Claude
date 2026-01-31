#!/usr/bin/env python3
"""
Phase 5 Migration Script - Migrate 10 prototype agents
"""

import re
from pathlib import Path

AGENTS_DIR = Path(".claude/agents")

# Phase 5 prototype agents
PHASE5_AGENTS = [
    "prototype-accessibility-auditor.md",
    "prototype-api-contract-specifier.md",
    "prototype-component-specifier.md",
    "prototype-component-validator.md",
    "prototype-data-model-specifier.md",
    "prototype-design-token-generator.md",
    "prototype-screen-specifier.md",
    "prototype-screen-validator.md",
    "prototype-ux-validator.md",
    "prototype-visual-qa-tester.md",
]

def get_agent_name_from_file(content):
    """Extract agent name from YAML"""
    match = re.search(r"^name:\s*(.+?)$", content, re.MULTILINE)
    return match.group(1).strip() if match else None

def migrate_agent(filepath):
    """Migrate an agent file"""

    with open(filepath, 'r') as f:
        content = f.read()

    # Parse frontmatter
    if not content.startswith("---"):
        raise ValueError("No frontmatter")

    try:
        end_marker = content.find("---", 3)
        if end_marker == -1:
            raise ValueError("No closing ---")

        body = content[end_marker+3:].lstrip()
    except:
        raise ValueError("Parse failed")

    # Extract agent name
    match = re.search(r"^name:\s*(.+?)$", content, re.MULTILINE)
    agent_name = match.group(1).strip() if match else None

    if not agent_name:
        raise ValueError("No agent name found")

    # Add FIRST ACTION if not present
    if "## FIRST ACTION" not in body:
        first_action = f"""## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" subagent {agent_name} started '{{"stage": "prototype", "method": "instruction-based"}}'
```

---

"""
        body = first_action + body

    # Reconstruct file with updated body
    final_content = content[:end_marker+3] + "\n" + body

    with open(filepath, 'w') as f:
        f.write(final_content)

    return True

def main():
    migrated = []
    failed = []

    for agent_file in PHASE5_AGENTS:
        filepath = AGENTS_DIR / agent_file

        if not filepath.exists():
            failed.append((agent_file, "Not found"))
            continue

        try:
            migrate_agent(filepath)
            print(f"✅ {agent_file.replace('.md', '')}")
            migrated.append(agent_file)
        except Exception as e:
            print(f"❌ {agent_file.replace('.md', '')}: {str(e)}")
            failed.append((agent_file, str(e)))

    print(f"\n✅ Migrated: {len(migrated)}/10")
    print(f"❌ Failed: {len(failed)}/10")

if __name__ == "__main__":
    main()
