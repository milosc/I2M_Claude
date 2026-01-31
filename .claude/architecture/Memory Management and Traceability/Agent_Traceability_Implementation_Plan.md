# Agent Traceability Implementation Plan

**Version**: 1.0.0
**Date**: 2026-01-26
**Objective**: Implement complete hierarchical agent execution tracing using Claude Code's native hooks mechanism

---

## Executive Summary

This plan ports the multi-agent observability approach from the sample project to the HTEC framework, providing:

1. **Complete call hierarchy** - Command → Agent → Skill → Nested Agent
2. **Full context capture** - Tool inputs, outputs, transcripts, model names
3. **Standardized logging** - Using Claude Code's official hook events
4. **Real-time visibility** - Optional server/UI for live monitoring
5. **Zero hallucination** - All names extracted from actual tool inputs, not inferred

**Key Insight**: The sample project uses `source_app + session_id` to uniquely identify agents, and Claude Code's native hook events provide **all the context we need** without manual logging.

---

## Current State Analysis

### What Works
- ✅ Basic lifecycle logging to `_state/lifecycle.json`
- ✅ SessionStart hook captures session initialization
- ✅ PreToolUse/PostToolUse hooks for Task and Skill tools
- ✅ SubagentStop hook for agent completion
- ✅ Bash script with `--from-input` extraction

### Critical Gaps
- ❌ **Agent names are "unknown"** - extraction from CLAUDE_TOOL_INPUT is failing
- ❌ **No hierarchy/call stack** - can't trace Command → Agent → Skill chains
- ❌ **Missing context** - no tool inputs, outputs, or transcripts captured
- ❌ **No parent tracking** - can't determine which agent spawned which subagent
- ❌ **Limited hook coverage** - missing UserPromptSubmit, PreCompact, SessionEnd
- ❌ **No real-time visibility** - just append-only JSON file

### Root Cause
The bash script approach is **too limited**:
- Can't parse complex JSON structures reliably
- Can't capture full tool inputs/outputs (size limits)
- Can't maintain parent-child relationships
- Can't send events to external systems

---

## Proposed Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     HTEC TRACEABILITY ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Claude Code Session                                                    │
│       │                                                                 │
│       │  USER PROMPT                                                    │
│       ├──────────────────────────────────────────────────────────────┐  │
│       │  UserPromptSubmit hook → capture_event.py                    │  │
│       │    - Store prompt text                                       │  │
│       │    - Extract command/intent                                  │  │
│       │    - Log to events.db + lifecycle.json                       │  │
│       └──────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       │  COMMAND EXECUTION (via Skill tool)                             │
│       ├──────────────────────────────────────────────────────────────┐  │
│       │  PreToolUse(Skill) → capture_event.py                        │  │
│       │    - Extract skill name from CLAUDE_TOOL_INPUT.skill         │  │
│       │    - Capture full tool_input JSON                            │  │
│       │    - Mark parent_session = CLAUDE_SESSION_ID                 │  │
│       │  PostToolUse(Skill) → capture_event.py                       │  │
│       │    - Capture tool_output                                     │  │
│       │    - Link to PreToolUse event by timestamp                   │  │
│       └──────────────────────────────────────────────────────────────┘  │
│       │                                                                 │
│       │  AGENT SPAWN (via Task tool)                                    │
│       ├──────────────────────────────────────────────────────────────┐  │
│       │  PreToolUse(Task) → capture_event.py                         │  │
│       │    - Extract agent name from prompt ("Agent: name")          │  │
│       │    - Extract subagent_type, model, description               │  │
│       │    - Capture full prompt text                                │  │
│       │    - Mark parent_session = CLAUDE_SESSION_ID                 │  │
│       │    - Store in pending_spawns registry                        │  │
│       └──────────────────────────────────────────────────────────────┘  │
│                ↓                                                        │
│       ┌────────────────────────────────────────────────────────────────┐│
│       │  SUBAGENT SESSION STARTS                                       ││
│       │  SessionStart hook (subagent context)                          ││
│       │    - Capture subagent session_id                               ││
│       │    - Link to parent_session from pending_spawns                ││
│       │    - Build call stack: parent.stack + [current]                ││
│       └────────────────────────────────────────────────────────────────┘│
│                │                                                        │
│                │  SUBAGENT TOOL USE                                     │
│                ├──────────────────────────────────────────────────────┐ │
│                │  PreToolUse/PostToolUse (any tool)                   │ │
│                │    - Tag with subagent session_id                    │ │
│                │    - Inherit call_stack from session                 │ │
│                │    - Full tool context captured                      │ │
│                └──────────────────────────────────────────────────────┘ │
│                │                                                        │
│                │  SUBAGENT COMPLETES                                    │
│                ├──────────────────────────────────────────────────────┐ │
│                │  SubagentStop hook → capture_event.py                │ │
│                │    - Capture result/outputs                          │ │
│                │    - Mark end time                                   │ │
│                │    - Link to PostToolUse(Task) in parent session     │ │
│                └──────────────────────────────────────────────────────┘ │
│                ↓                                                        │
│       ┌────────────────────────────────────────────────────────────────┐│
│       │  PostToolUse(Task) → capture_event.py                          ││
│       │    - Capture agent completion status                           ││
│       │    - Link to PreToolUse(Task) and SubagentStop                 ││
│       └────────────────────────────────────────────────────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Input
    ↓ UserPromptSubmit
lifecycle.json + events.db ← {type: "user_prompt", text: "...", session: "main-123"}
    ↓
Skill Execution (/discovery)
    ↓ PreToolUse(Skill)
lifecycle.json + events.db ← {type: "skill_start", name: "discovery", parent_session: "main-123"}
    ↓ Skill spawns Task()
Task() call
    ↓ PreToolUse(Task)
lifecycle.json + events.db ← {type: "agent_spawn", name: "discovery-orchestrator", parent_session: "main-123"}
    ↓ Agent session starts
SubagentStart
    ↓ SessionStart (subagent)
lifecycle.json + events.db ← {type: "session_start", session: "sub-456", parent: "main-123", call_stack: ["main-123", "discovery", "discovery-orchestrator"]}
    ↓ Agent uses tools
PreToolUse/PostToolUse (Read, Write, etc.)
    ↓
lifecycle.json + events.db ← {type: "tool_use", tool: "Write", session: "sub-456", call_stack: [...]}
    ↓ Agent completes
SubagentStop
    ↓
lifecycle.json + events.db ← {type: "agent_complete", session: "sub-456", result: {...}}
    ↓ PostToolUse(Task) fires in parent
PostToolUse(Task)
    ↓
lifecycle.json + events.db ← {type: "agent_result", name: "discovery-orchestrator", parent_session: "main-123"}
```

---

## Implementation Steps

### Phase 1: Python Hook Scripts (Week 1)

#### 1.1 Create Core Hook Scripts

**File**: `.claude/hooks/capture_event.py`

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["python-dotenv"]
# ///

"""
Universal event capture script for HTEC framework.
Captures all Claude Code hook events with full context.
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def get_project_dir():
    """Get project directory from environment or current directory."""
    return os.getenv('CLAUDE_PROJECT_DIR', os.getcwd())

def ensure_state_dir():
    """Ensure _state directory exists."""
    state_dir = Path(get_project_dir()) / '_state'
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir

def load_session_context():
    """Load session context from _state/session.json."""
    session_file = Path(get_project_dir()) / '_state' / 'session.json'
    if session_file.exists():
        with open(session_file, 'r') as f:
            return json.load(f)
    return {}

def save_call_stack(session_id, call_stack):
    """Save call stack for session."""
    state_dir = ensure_state_dir()
    stack_file = state_dir / f'call_stack_{session_id}.json'
    with open(stack_file, 'w') as f:
        json.dump({'session_id': session_id, 'stack': call_stack}, f, indent=2)

def load_call_stack(session_id):
    """Load call stack for session."""
    state_dir = ensure_state_dir()
    stack_file = state_dir / f'call_stack_{session_id}.json'
    if stack_file.exists():
        with open(stack_file, 'r') as f:
            data = json.load(f)
            return data.get('stack', [])
    return []

def extract_agent_name(tool_input):
    """
    Extract agent name from Task tool input.
    Looks for patterns:
    1. "Agent: agent-name" in prompt
    2. "Read: .claude/agents/agent-name.md" in prompt
    3. Falls back to subagent_type
    """
    if 'prompt' in tool_input:
        prompt = tool_input['prompt']

        # Pattern 1: "Agent: name"
        import re
        match = re.search(r'Agent:\s*([a-zA-Z0-9_-]+)', prompt, re.IGNORECASE)
        if match:
            return match.group(1)

        # Pattern 2: "Read: .claude/agents/name.md"
        match = re.search(r'Read:\s*\.claude/agents/([a-zA-Z0-9_-]+)\.md', prompt, re.IGNORECASE)
        if match:
            return match.group(1)

    # Pattern 3: subagent_type
    return tool_input.get('subagent_type', 'unknown')

def capture_event(event_type, input_data):
    """
    Capture event with full context.

    event_type: PreToolUse, PostToolUse, UserPromptSubmit, SubagentStop, etc.
    input_data: JSON from stdin
    """
    state_dir = ensure_state_dir()
    lifecycle_file = state_dir / 'lifecycle.json'

    # Get session context
    session_context = load_session_context()
    session_id = input_data.get('session_id', os.getenv('CLAUDE_SESSION_ID', 'unknown'))
    project_name = session_context.get('project', 'unknown')
    stage = session_context.get('stage', 'unknown')

    # Load call stack for this session
    call_stack = load_call_stack(session_id)

    # Build event entry
    event = {
        'event_type': event_type,
        'timestamp': datetime.now().isoformat(),
        'session_id': session_id,
        'project': project_name,
        'stage': stage,
        'call_stack': call_stack,
        'payload': input_data
    }

    # Event-specific processing
    if event_type == 'PreToolUse':
        tool_name = input_data.get('tool_name', 'unknown')
        event['tool_name'] = tool_name

        if tool_name == 'Task':
            # Agent spawn
            tool_input = input_data.get('tool_input', {})
            agent_name = extract_agent_name(tool_input)
            event['component'] = 'agent'
            event['name'] = agent_name
            event['event'] = 'pre_spawn'
            event['model'] = tool_input.get('model', 'unknown')
            event['subagent_type'] = tool_input.get('subagent_type', 'unknown')

            # Store in pending spawns for linking
            pending_file = state_dir / 'pending_spawns.json'
            pending = []
            if pending_file.exists():
                with open(pending_file, 'r') as f:
                    pending = json.load(f)
            pending.append({
                'agent_name': agent_name,
                'parent_session': session_id,
                'timestamp': event['timestamp'],
                'call_stack': call_stack + [agent_name]
            })
            with open(pending_file, 'w') as f:
                json.dump(pending, f, indent=2)

        elif tool_name == 'Skill':
            # Skill invocation
            tool_input = input_data.get('tool_input', {})
            skill_name = tool_input.get('skill', 'unknown')
            event['component'] = 'skill'
            event['name'] = skill_name
            event['event'] = 'pre_invoke'

    elif event_type == 'PostToolUse':
        tool_name = input_data.get('tool_name', 'unknown')
        event['tool_name'] = tool_name

        if tool_name == 'Task':
            # Agent completion
            tool_input = input_data.get('tool_input', {})
            agent_name = extract_agent_name(tool_input)
            event['component'] = 'agent'
            event['name'] = agent_name
            event['event'] = 'post_spawn'

        elif tool_name == 'Skill':
            # Skill completion
            tool_input = input_data.get('tool_input', {})
            skill_name = tool_input.get('skill', 'unknown')
            event['component'] = 'skill'
            event['name'] = skill_name
            event['event'] = 'post_invoke'

    elif event_type == 'SessionStart':
        # Check if this is a subagent session
        pending_file = state_dir / 'pending_spawns.json'
        if pending_file.exists():
            with open(pending_file, 'r') as f:
                pending = json.load(f)

            # Find matching spawn (most recent)
            if pending:
                spawn = pending[-1]  # Most recent spawn
                parent_session = spawn['parent_session']
                call_stack = spawn['call_stack']

                # Update this session's call stack
                save_call_stack(session_id, call_stack)
                event['parent_session'] = parent_session
                event['call_stack'] = call_stack
                event['component'] = 'session'
                event['name'] = 'subagent'
                event['event'] = 'started'

                # Remove from pending
                pending.pop()
                with open(pending_file, 'w') as f:
                    json.dump(pending, f, indent=2)
        else:
            # Main session
            event['component'] = 'session'
            event['name'] = 'main'
            event['event'] = 'started'

    elif event_type == 'SubagentStop':
        event['component'] = 'subagent'
        event['name'] = 'unknown'  # TODO: extract from context
        event['event'] = 'stopped'

    elif event_type == 'UserPromptSubmit':
        prompt = input_data.get('prompt', '')
        event['component'] = 'user_prompt'
        event['name'] = 'prompt'
        event['event'] = 'submitted'
        event['prompt_text'] = prompt[:200]  # Truncate for readability

    # Append to lifecycle.json
    with open(lifecycle_file, 'a') as f:
        f.write(json.dumps(event) + '\n')

    # Optionally send to observability server (if running)
    try:
        import urllib.request
        server_url = 'http://localhost:4000/events'
        req = urllib.request.Request(
            server_url,
            data=json.dumps(event).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req, timeout=1)
    except:
        pass  # Fail silently if server not running

    return event

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--event-type', required=True, help='Hook event type')
    args = parser.parse_args()

    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Capture event
    event = capture_event(args.event_type, input_data)

    # Output confirmation
    print(f"CAPTURED: {event.get('component', 'event')}:{event.get('name', 'unknown')}:{event.get('event', args.event_type)}")

    sys.exit(0)

if __name__ == '__main__':
    main()
```

#### 1.2 Update Hook Configuration

**File**: `.claude/settings.json` (Updated)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-init.sh\""
          },
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type SessionStart"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type SessionEnd"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type UserPromptSubmit"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type PreToolUse"
          }
        ]
      },
      {
        "matcher": "Skill",
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type PreToolUse"
          }
        ]
      },
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type PreToolUse"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type PostToolUse"
          }
        ]
      },
      {
        "matcher": "Skill",
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type PostToolUse"
          }
        ]
      },
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type PostToolUse"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type SubagentStop"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type Stop"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type PreCompact"
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type Notification"
          }
        ]
      }
    ]
  }
}
```

---

### Phase 2: Agent/Skill/Command Frontmatter (Week 2)

#### 2.1 Agent Frontmatter Standards

**No changes needed** - Agent names are extracted from the Task() prompt, not from frontmatter.

The key is that commands **must** include the agent name in the Task() prompt:

```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Orchestrate Discovery analysis",
  prompt: `Agent: discovery-orchestrator  # ← THIS IS CRITICAL
    Read: .claude/agents/discovery-orchestrator.md

    Execute complete Discovery analysis for Inventory System.
    ...`
})
```

**Action Items**:
- ✅ Review all commands that spawn agents
- ✅ Ensure `Agent: <name>` or `Read: .claude/agents/<name>.md` in prompt
- ✅ Document this pattern in command templates

#### 2.2 Skill Frontmatter Standards

**Current frontmatter** is sufficient:

```yaml
---
name: discovery
description: Complete Discovery orchestration
context: fork
agent: general-purpose
---
```

**No changes needed** - Skill name is extracted from Skill tool's `.skill` field automatically.

#### 2.3 Command Frontmatter Standards

**Current frontmatter** is sufficient:

```yaml
---
name: /discovery
description: Complete Discovery orchestration
---
```

Commands are invoked via Skill tool, so the skill name is sufficient.

---

### Phase 3: Call Stack Visualization (Week 3)

#### 3.1 Create Call Stack Viewer Script

**File**: `.claude/tools/view_call_stack.py`

```python
#!/usr/bin/env python3
"""
View hierarchical call stack from lifecycle.json
"""

import json
from pathlib import Path
from collections import defaultdict

def load_lifecycle():
    lifecycle_file = Path('_state/lifecycle.json')
    events = []
    with open(lifecycle_file, 'r') as f:
        for line in f:
            events.append(json.loads(line))
    return events

def build_hierarchy(events):
    """Build hierarchical tree from events."""
    tree = defaultdict(list)

    for event in events:
        session = event.get('session_id', 'unknown')
        parent = event.get('parent_session')

        if parent:
            tree[parent].append(event)
        else:
            tree['root'].append(event)

    return tree

def print_tree(tree, node='root', indent=0):
    """Recursively print tree."""
    prefix = "  " * indent

    for event in tree.get(node, []):
        event_type = event.get('event', event.get('event_type', 'unknown'))
        component = event.get('component', 'unknown')
        name = event.get('name', 'unknown')
        timestamp = event.get('timestamp', '')

        # Format based on event type
        if event_type in ['started', 'pre_spawn', 'pre_invoke']:
            symbol = "├─"
        elif event_type in ['stopped', 'post_spawn', 'post_invoke']:
            symbol = "└─"
        else:
            symbol = "│ "

        print(f"{prefix}{symbol} [{timestamp}] {component}:{name} ({event_type})")

        # Recurse for child sessions
        session = event.get('session_id')
        if session:
            print_tree(tree, session, indent + 1)

def main():
    events = load_lifecycle()
    tree = build_hierarchy(events)

    print("=" * 80)
    print("HTEC FRAMEWORK CALL STACK")
    print("=" * 80)
    print_tree(tree)

if __name__ == '__main__':
    main()
```

**Usage**:
```bash
python3 .claude/tools/view_call_stack.py
```

**Output Example**:
```
================================================================================
HTEC FRAMEWORK CALL STACK
================================================================================
├─ [2026-01-26T10:00:00] session:main (started)
│  ├─ [2026-01-26T10:00:05] user_prompt:prompt (submitted) "/discovery InventorySystem Client_Materials/"
│  ├─ [2026-01-26T10:00:06] skill:discovery (pre_invoke)
│  │  ├─ [2026-01-26T10:00:07] agent:discovery-orchestrator (pre_spawn)
│  │  │  ├─ [2026-01-26T10:00:08] session:subagent (started) [parent: main-123]
│  │  │  │  ├─ [2026-01-26T10:00:10] agent:discovery-interview-analyst (pre_spawn)
│  │  │  │  │  ├─ [2026-01-26T10:00:11] session:subagent (started) [parent: sub-456]
│  │  │  │  │  │  ├─ [2026-01-26T10:00:12] tool:Read (pre_use)
│  │  │  │  │  │  └─ [2026-01-26T10:00:13] tool:Read (post_use)
│  │  │  │  │  └─ [2026-01-26T10:00:14] subagent:discovery-interview-analyst (stopped)
│  │  │  │  └─ [2026-01-26T10:00:15] agent:discovery-interview-analyst (post_spawn)
│  │  │  └─ [2026-01-26T10:00:20] subagent:discovery-orchestrator (stopped)
│  │  └─ [2026-01-26T10:00:21] agent:discovery-orchestrator (post_spawn)
│  └─ [2026-01-26T10:00:22] skill:discovery (post_invoke)
```

---

### Phase 4: Optional Observability Server (Week 4)

#### 4.1 Port Sample Server

Copy the server from the sample project:

```bash
# Copy server
cp -R sample/claude-code-hooks-multi-agent-observability-main/apps/server .claude/observability/

# Copy client
cp -R sample/claude-code-hooks-multi-agent-observability-main/apps/client .claude/observability/

# Update capture_event.py to send events to server
# (Already included in Phase 1 script)
```

#### 4.2 Start Observability System

```bash
# Start server + client
cd .claude/observability
./start-system.sh

# Open http://localhost:5173
```

**Benefits**:
- Real-time event streaming
- Visual call stack graph
- Session filtering
- Event timeline
- Chat transcript viewer

---

## Frontmatter Changes Summary

### ✅ NO CHANGES NEEDED

**Agents**: No frontmatter changes needed. Agent names are extracted from Task() prompt.

**Skills**: No frontmatter changes needed. Skill names are extracted from Skill tool's `.skill` field.

**Commands**: No frontmatter changes needed. Commands are invoked via Skill tool.

### ✅ ONLY CHANGE: Task() Prompt Pattern

**Commands that spawn agents MUST include agent name in prompt:**

```javascript
// ✅ CORRECT - Agent name extractable
Task({
  prompt: `Agent: discovery-orchestrator
    Read: .claude/agents/discovery-orchestrator.md
    ...`
})

// ❌ WRONG - Agent name not extractable
Task({
  prompt: `Execute Discovery analysis for InventorySystem.
    Use the orchestrator agent to coordinate.
    ...`
})
```

**Action**: Audit all commands that spawn agents and ensure pattern compliance.

---

## Testing Strategy

### Test Case 1: Single Agent Spawn

```bash
# User prompt
/discovery InventorySystem Client_Materials/

# Expected lifecycle.json entries
{"event_type": "UserPromptSubmit", "prompt_text": "/discovery InventorySystem...", ...}
{"event_type": "PreToolUse", "tool_name": "Skill", "name": "discovery", ...}
{"event_type": "PreToolUse", "tool_name": "Task", "name": "discovery-orchestrator", ...}
{"event_type": "SessionStart", "parent_session": "main-123", "call_stack": ["main-123", "discovery", "discovery-orchestrator"], ...}
{"event_type": "SubagentStop", "session_id": "sub-456", ...}
{"event_type": "PostToolUse", "tool_name": "Task", "name": "discovery-orchestrator", ...}
{"event_type": "PostToolUse", "tool_name": "Skill", "name": "discovery", ...}
```

### Test Case 2: Nested Agent Spawns

```bash
# Orchestrator spawns 3 agents in parallel
/discovery-multiagent InventorySystem Client_Materials/

# Expected: 3 parallel call stacks
# Stack 1: main → discovery-multiagent → discovery-interview-analyst
# Stack 2: main → discovery-multiagent → discovery-pdf-analyst
# Stack 3: main → discovery-multiagent → discovery-design-analyst
```

---

## Migration Checklist

### Week 1: Core Hooks
- [ ] Create `capture_event.py` script
- [ ] Update `.claude/settings.json` with all hooks
- [ ] Test SessionStart, PreToolUse, PostToolUse, SubagentStop
- [ ] Verify lifecycle.json format

### Week 2: Agent Name Extraction
- [ ] Audit all commands that spawn agents
- [ ] Ensure `Agent: <name>` pattern in all Task() prompts
- [ ] Test agent name extraction with discovery-orchestrator
- [ ] Test nested agent spawns (orchestrator → analysts)

### Week 3: Call Stack Visualization
- [ ] Create `view_call_stack.py` script
- [ ] Test hierarchical display
- [ ] Add filtering by session/stage
- [ ] Document usage in CLAUDE.md

### Week 4: Observability Server (Optional)
- [ ] Copy server + client from sample project
- [ ] Update source_app identifier for HTEC framework
- [ ] Test real-time event streaming
- [ ] Document setup in architecture docs

---

## Success Metrics

1. **Zero "unknown" agents** - All agent names correctly extracted
2. **Complete call stacks** - Every subagent linked to parent
3. **Full context capture** - Tool inputs/outputs, timestamps, models
4. **Hierarchical visualization** - Clear command → agent → skill chains
5. **Real-time visibility** - Events stream to UI within 1 second

---

## Rollback Plan

If implementation causes issues:

```bash
# Restore old settings.json
cp .claude/settings.json.backup .claude/settings.json

# Use old bash hook
git checkout HEAD -- .claude/hooks/log-lifecycle.sh

# Revert lifecycle.json format (keep old entries, new entries will be ignored)
```

---

## References

- **Sample Project**: `sample/claude-code-hooks-multi-agent-observability-main/`
- **Claude Code Hooks Docs**: https://code.claude.com/docs/en/hooks
- **Hook Event Types**: PreToolUse, PostToolUse, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, Notification, PreCompact, Stop

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-26 | Initial plan - Python hooks, call stack tracking, observability server |
