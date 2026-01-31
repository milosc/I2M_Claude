#!/usr/bin/env python3
"""
Phase 6 Migration Script - Migrate 18 SolArch agents
"""

import re
from pathlib import Path

AGENTS_DIR = Path(".claude/agents")

# Phase 6 SolArch agents (18 files)
PHASE6_AGENTS = [
    "solarch-adr-communication-writer.md",
    "solarch-adr-foundation-writer.md",
    "solarch-adr-operational-writer.md",
    "solarch-adr-validator.md",
    "solarch-arch-evaluator.md",
    "solarch-c4-component-generator.md",
    "solarch-c4-container-generator.md",
    "solarch-c4-context-generator.md",
    "solarch-c4-deployment-generator.md",
    "solarch-cost-estimator.md",
    "solarch-integration-analyst.md",
    "solarch-performance-scenarios.md",
    "solarch-reliability-scenarios.md",
    "solarch-risk-scorer.md",
    "solarch-security-scenarios.md",
    "solarch-tech-researcher.md",
    "solarch-usability-scenarios.md",
    "README.md",
]

def get_agent_name_from_file(content):
    """Extract agent name from YAML (for non-README files)"""
    match = re.search(r"^name:\s*(.+?)$", content, re.MULTILINE)
    return match.group(1).strip() if match else None

def migrate_agent(filepath, agent_file):
    """Migrate an agent file"""

    with open(filepath, 'r') as f:
        content = f.read()

    # Handle README.md separately (it's not an agent, just documentation)
    if agent_file == "README.md":
        # For README, just add FIRST ACTION if needed (optional for documentation)
        if "## FIRST ACTION" not in content:
            # README doesn't need FIRST ACTION, skip it
            return True
        return True

    # Parse frontmatter for agent files
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
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" subagent {agent_name} started '{{"stage": "solarch", "method": "instruction-based"}}'
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

    for agent_file in PHASE6_AGENTS:
        filepath = AGENTS_DIR / agent_file

        if not filepath.exists():
            failed.append((agent_file, "Not found"))
            continue

        try:
            migrate_agent(filepath, agent_file)
            print(f"✅ {agent_file.replace('.md', '')}")
            migrated.append(agent_file)
        except Exception as e:
            print(f"❌ {agent_file.replace('.md', '')}: {str(e)}")
            failed.append((agent_file, str(e)))

    print(f"\n✅ Migrated: {len(migrated)}/18")
    print(f"❌ Failed: {len(failed)}/18")

if __name__ == "__main__":
    main()
