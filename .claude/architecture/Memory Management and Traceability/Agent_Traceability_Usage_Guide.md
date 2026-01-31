# Agent Traceability System - Usage Guide

**Version**: 1.0.0
**Date**: 2026-01-26
**Status**: ✅ Implemented (Phase 1 & 3)

---

## Overview

The HTEC framework now captures complete hierarchical agent execution traces using Python-based hooks. This provides:

1. **Complete call hierarchy** - Command → Agent → Skill → Nested Agent
2. **Full context capture** - Tool inputs, outputs, timestamps, model names
3. **Zero hallucination** - All names extracted from actual tool inputs
4. **Real-time logging** - Every hook event captured to `_state/lifecycle.json`

---

## What's Been Implemented

### ✅ Phase 1: Python Hook Scripts (Complete)

**New Files**:
- `.claude/hooks/capture_event.py` - Universal event capture script
- `.claude/tools/view_call_stack.py` - Call stack visualization

**Updated Files**:
- `.claude/settings.json` - Now uses Python hooks for all events

**Backup Files** (for rollback):
- `.claude/hooks/log-lifecycle.sh.backup` - Old bash implementation
- `.claude/settings.json.backup` - Old settings

### ✅ Phase 3: Call Stack Visualization (Complete)

**Script**: `.claude/tools/view_call_stack.py`

---

## How It Works

### Event Capture Flow

```
User Input
    ↓ UserPromptSubmit hook
capture_event.py → lifecycle.json
    ↓
Skill Execution (/discovery)
    ↓ PreToolUse(Skill) hook
capture_event.py → lifecycle.json (extracts skill name)
    ↓
Agent Spawn (Task tool)
    ↓ PreToolUse(Task) hook
capture_event.py → lifecycle.json (extracts agent name, creates pending_spawn)
    ↓
Subagent Session Starts
    ↓ SessionStart hook (in subagent context)
capture_event.py → lifecycle.json (links to parent, builds call stack)
    ↓
Subagent Uses Tools
    ↓ PreToolUse/PostToolUse hooks
capture_event.py → lifecycle.json (captures tool context)
    ↓
Subagent Completes
    ↓ SubagentStop hook
capture_event.py → lifecycle.json (marks completion)
    ↓
Task Completes
    ↓ PostToolUse(Task) hook
capture_event.py → lifecycle.json (marks agent result)
```

### Agent Name Extraction

The script extracts agent names from Task tool prompts using these patterns:

1. **Pattern 1**: `Agent: agent-name` in prompt
2. **Pattern 2**: `Read: .claude/agents/agent-name.md` in prompt
3. **Fallback**: Uses `subagent_type` field

**Example**:
```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Orchestrate Discovery analysis",
  prompt: `Agent: discovery-orchestrator  // ← Extracted from here
    Read: .claude/agents/discovery-orchestrator.md

    Execute complete Discovery analysis for Inventory System.
    ...`
})
```

### Call Stack Tracking

Each session maintains a call stack stored in `_state/call_stack_{session_id}.json`:

```json
{
  "session_id": "sub-456",
  "stack": [
    "main-123",
    "discovery",
    "discovery-orchestrator"
  ]
}
```

Parent-child relationships are tracked via `pending_spawns.json`:

```json
[
  {
    "agent_name": "discovery-orchestrator",
    "parent_session": "main-123",
    "timestamp": "2026-01-26T20:00:00",
    "call_stack": ["main-123", "discovery", "discovery-orchestrator"]
  }
]
```

---

## Usage

### View Call Stack

```bash
python3 .claude/tools/view_call_stack.py
```

**Output Example**:
```
================================================================================
HTEC FRAMEWORK CALL STACK
================================================================================
├─ [2026-01-26T10:00:00] session:main (started)
│  ├─ [2026-01-26T10:00:05] user_prompt:prompt (submitted)
│  ├─ [2026-01-26T10:00:06] skill:discovery (pre_invoke)
│  │  ├─ [2026-01-26T10:00:07] agent:discovery-orchestrator (pre_spawn)
│  │  │  ├─ [2026-01-26T10:00:08] session:subagent (started)
│  │  │  │  ├─ [2026-01-26T10:00:10] agent:discovery-interview-analyst (pre_spawn)
│  │  │  │  │  ├─ [2026-01-26T10:00:11] session:subagent (started)
│  │  │  │  │  │  ├─ [2026-01-26T10:00:12] tool:Read (pre_use)
│  │  │  │  │  │  └─ [2026-01-26T10:00:13] tool:Read (post_use)
│  │  │  │  │  └─ [2026-01-26T10:00:14] subagent:discovery-interview-analyst (stopped)
│  │  │  │  └─ [2026-01-26T10:00:15] agent:discovery-interview-analyst (post_spawn)
│  │  │  └─ [2026-01-26T10:00:20] subagent:discovery-orchestrator (stopped)
│  │  └─ [2026-01-26T10:00:21] agent:discovery-orchestrator (post_spawn)
│  └─ [2026-01-26T10:00:22] skill:discovery (post_invoke)
```

### View Raw Lifecycle Events

```bash
# View all events
cat _state/lifecycle.json | jq .

# View recent events
tail -20 _state/lifecycle.json | jq .

# Filter by component
cat _state/lifecycle.json | jq 'select(.component == "agent")'

# Filter by session
cat _state/lifecycle.json | jq 'select(.session_id == "main-123")'
```

### Check Pending Spawns

```bash
cat _state/pending_spawns.json | jq .
```

### Check Session Call Stack

```bash
cat _state/call_stack_{session_id}.json | jq .
```

---

## Event Schema

### lifecycle.json Entry

```json
{
  "event_type": "PreToolUse",
  "timestamp": "2026-01-26T20:00:00",
  "session_id": "main-123",
  "project": "InventorySystem",
  "stage": "discovery",
  "call_stack": ["main-123", "discovery", "discovery-orchestrator"],
  "tool_name": "Task",
  "component": "agent",
  "name": "discovery-orchestrator",
  "event": "pre_spawn",
  "model": "sonnet",
  "subagent_type": "general-purpose",
  "payload": {
    "tool_name": "Task",
    "tool_input": {
      "prompt": "Agent: discovery-orchestrator\n...",
      "subagent_type": "general-purpose",
      "model": "sonnet"
    }
  }
}
```

### Event Types

| Hook | event_type | component | event | name |
|------|-----------|-----------|-------|------|
| UserPromptSubmit | UserPromptSubmit | user_prompt | submitted | prompt |
| PreToolUse(Skill) | PreToolUse | skill | pre_invoke | {skill_name} |
| PostToolUse(Skill) | PostToolUse | skill | post_invoke | {skill_name} |
| PreToolUse(Task) | PreToolUse | agent | pre_spawn | {agent_name} |
| PostToolUse(Task) | PostToolUse | agent | post_spawn | {agent_name} |
| SessionStart | SessionStart | session | started | main/subagent |
| SessionEnd | SessionEnd | session | ended | main/subagent |
| SubagentStop | SubagentStop | subagent | stopped | unknown |
| PreCompact | PreCompact | system | pre_compact | unknown |
| Stop | Stop | system | stopped | unknown |
| Notification | Notification | system | notification | unknown |

---

## Phase 2: Agent Name Pattern Compliance

### Requirements

All commands that spawn agents MUST include agent name in the Task() prompt:

✅ **CORRECT** - Agent name extractable:
```javascript
Task({
  prompt: `Agent: discovery-orchestrator
    Read: .claude/agents/discovery-orchestrator.md
    ...`
})
```

❌ **WRONG** - Agent name not extractable:
```javascript
Task({
  prompt: `Execute Discovery analysis for InventorySystem.
    Use the orchestrator agent to coordinate.
    ...`
})
```

### Action Items

- [ ] Audit all commands that spawn agents (`.claude/commands/*.md`)
- [ ] Ensure `Agent: <name>` pattern in all Task() prompts
- [ ] Test agent name extraction with real commands
- [ ] Document pattern in command templates

---

## Phase 4: Optional Observability Server

**Status**: Not yet implemented

The plan includes an optional real-time observability server with:
- Event streaming (WebSocket)
- Visual call stack graph
- Session filtering
- Timeline view
- Chat transcript viewer

**To implement**: Copy server from `sample/claude-code-hooks-multi-agent-observability-main/apps/server`

---

## Troubleshooting

### Agent Names Show "unknown"

**Check**:
1. Does the Task() prompt include `Agent: <name>` or `Read: .claude/agents/<name>.md`?
2. Is the pattern correctly formatted (no extra characters)?
3. Check `_state/lifecycle.json` to see the raw prompt captured

**Fix**: Update command to include agent name in prompt

### Call Stack Not Building

**Check**:
1. Is `_state/pending_spawns.json` being created?
2. Are SessionStart hooks firing in subagent context?
3. Check `_state/call_stack_{session_id}.json` files

**Debug**:
```bash
# Check pending spawns
cat _state/pending_spawns.json | jq .

# Check call stacks
ls -la _state/call_stack_*.json

# Watch events in real-time
tail -f _state/lifecycle.json | jq .
```

### Hook Not Firing

**Check**:
1. Is `uv` installed? (`which uv`)
2. Is capture_event.py executable? (`ls -la .claude/hooks/capture_event.py`)
3. Check Claude Code logs for hook errors

**Debug**:
```bash
# Test capture_event.py manually
echo '{"tool_name": "Task", "tool_input": {"prompt": "Agent: test-agent"}}' | \
  uv run .claude/hooks/capture_event.py --event-type PreToolUse
```

---

## Rollback Plan

If the new system causes issues:

```bash
# Restore old settings.json
cp .claude/settings.json.backup .claude/settings.json

# Use old bash hook
mv .claude/hooks/log-lifecycle.sh.backup .claude/hooks/log-lifecycle.sh

# Restart Claude Code
```

**Note**: Old lifecycle.json entries remain valid, new entries will be ignored.

---

## Related Documentation

- **Implementation Plan**: `.claude/architecture/Agent_Traceability_Implementation_Plan.md`
- **Hook Reference**: `.claude/architecture/Hooks_Quick_Reference.md`
- **Agent Spawning**: `.claude/architecture/agentsSpawningTech.md`

---

## Success Metrics

1. ✅ **Python hooks implemented** - capture_event.py in use
2. ✅ **Visualization working** - view_call_stack.py generates hierarchy
3. ⏳ **Zero "unknown" agents** - Requires Phase 2 audit
4. ⏳ **Complete call stacks** - Requires testing with real commands
5. ⏳ **Full context capture** - Requires validation with real workflows

---

## Next Steps

1. **Test the implementation** with a real command (e.g., `/discovery`)
2. **Phase 2 Audit**: Review commands for agent name patterns
3. **Validate call stacks** are building correctly
4. **Optional**: Implement observability server (Phase 4)
