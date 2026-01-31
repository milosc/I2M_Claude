#!/usr/bin/env python3
"""
Add Frontmatter Hooks to Agents

This script adds role-specific hooks to agent frontmatter based on the
Frontmatter_Hooks_Implementation_Plan.md.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List

# Hook Templates by Agent Category
HOOK_TEMPLATES = {
    "orchestrator": """hooks:
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

    "analyst": """hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "validator": """hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "generator": """hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "implementation": """hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/file_lock_acquire.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
    - matcher: "Bash"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/tdd_compliance_check.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/file_lock_release.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
    - matcher: "Bash"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "quality": """hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "planning": """hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "reflexion": """hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
""",

    "process-integrity": """hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
"""
}

# Agent Categorization based on naming patterns
AGENT_CATEGORIES = {
    "orchestrator": ["orchestrator"],
    "analyst": ["analyst"],
    "validator": ["validator", "auditor", "reviewer"],
    "generator": ["generator", "specifier"],
    "implementation": ["developer", "test-automation", "test-designer", "documenter", "pr-preparer"],
    "quality": ["quality-"],
    "planning": ["planning-", "code-explorer", "tech-lead"],
    "reflexion": ["reflexion-"],
    "process-integrity": ["process-integrity-"]
}


def detect_category(agent_name: str) -> str:
    """Detect agent category based on name patterns."""
    # Process-integrity has highest priority (check first)
    if "process-integrity-" in agent_name:
        return "process-integrity"

    for category, patterns in AGENT_CATEGORIES.items():
        if category == "process-integrity":
            continue  # Already checked above
        for pattern in patterns:
            if pattern in agent_name:
                return category

    # Default to generator for most agents
    return "generator"


def add_hooks_to_agent(agent_file: Path, dry_run: bool = False) -> bool:
    """Add hooks to agent frontmatter if not already present."""

    agent_name = agent_file.stem

    # Read file
    with open(agent_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)

    if not match:
        # No frontmatter - create minimal frontmatter with hooks
        print(f"📝 Creating frontmatter for: {agent_name}")

        # Detect category
        category = detect_category(agent_name)
        hooks_yaml = HOOK_TEMPLATES.get(category, HOOK_TEMPLATES["generator"])

        # Extract description from markdown title
        first_line = content.split('\n')[0]
        description = first_line.strip('#').strip() if first_line.startswith('#') else f"{agent_name} agent"

        # Create frontmatter
        frontmatter = f"""name: {agent_name}
description: {description}
model: sonnet
{hooks_yaml.rstrip()}"""

        new_content = f"---\n{frontmatter}\n---\n{content}"

        if dry_run:
            print(f"🔍 [DRY RUN] Would create frontmatter with {category} hooks for: {agent_name}")
            return True

        # Write back
        with open(agent_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ Created frontmatter with {category} hooks for: {agent_name}")
        return True

    frontmatter = match.group(1)
    body = match.group(2)

    # Check if hooks already exist
    if 'hooks:' in frontmatter:
        print(f"✅ Already has hooks: {agent_name}")
        return True

    # Detect category
    category = detect_category(agent_name)
    hooks_yaml = HOOK_TEMPLATES.get(category, HOOK_TEMPLATES["generator"])

    # Add hooks to frontmatter
    new_frontmatter = frontmatter.rstrip() + '\n' + hooks_yaml.rstrip()
    new_content = f"---\n{new_frontmatter}\n---\n{body}"

    if dry_run:
        print(f"🔍 [DRY RUN] Would add {category} hooks to: {agent_name}")
        return True

    # Write back
    with open(agent_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Added {category} hooks to: {agent_name}")
    return True


def main():
    """Process all agents or specific agent."""
    import argparse

    parser = argparse.ArgumentParser(description="Add frontmatter hooks to agents")
    parser.add_argument("--agent", help="Specific agent file to process")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    parser.add_argument("--category", help="Only process agents in this category")
    parser.add_argument("--priority", help="Priority group: process-integrity, implementation, orchestrator, all")

    args = parser.parse_args()

    agents_dir = Path(".claude/agents")

    if args.agent:
        # Single agent
        agent_file = agents_dir / f"{args.agent}.md"
        if not agent_file.exists():
            print(f"❌ Agent not found: {args.agent}")
            return 1
        add_hooks_to_agent(agent_file, args.dry_run)
        return 0

    # Priority groups
    if args.priority:
        priority_groups = {
            "process-integrity": ["process-integrity-traceability-guardian", "process-integrity-state-watchdog",
                                   "process-integrity-checkpoint-auditor", "process-integrity-playbook-enforcer"],
            "implementation": ["implementation-developer", "implementation-test-automation-engineer",
                              "implementation-test-designer", "implementation-documenter", "implementation-pr-preparer"],
            "orchestrator": ["discovery-orchestrator", "prototype-orchestrator", "productspecs-orchestrator",
                            "solarch-orchestrator", "project-orchestrator"]
        }

        agents_to_process = priority_groups.get(args.priority, [])
        if args.priority == "all":
            agents_to_process = [f.stem for f in agents_dir.glob("*.md")]

        for agent_name in agents_to_process:
            agent_file = agents_dir / f"{agent_name}.md"
            if agent_file.exists():
                add_hooks_to_agent(agent_file, args.dry_run)

        return 0

    # All agents
    success = 0
    skipped = 0
    failed = 0

    for agent_file in sorted(agents_dir.glob("*.md")):
        # Skip README.md
        if agent_file.stem == "README":
            continue

        if args.category:
            if detect_category(agent_file.stem) != args.category:
                continue

        try:
            if add_hooks_to_agent(agent_file, args.dry_run):
                success += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"❌ Error processing {agent_file.stem}: {e}")
            failed += 1

    print(f"\n📊 Summary: {success} successful, {skipped} skipped, {failed} failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
