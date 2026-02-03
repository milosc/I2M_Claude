---
name: verify-agents
description: Verify all agent definitions and validate agent coordination rules
argument-hint: None
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /verify-agents started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /verify-agents ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /verify-agents instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## Execution

# /verify-agents - Check Multi-Agent Execution

Verify if agents were spawned during prototype generation.

## Usage

```bash
# Check agent sessions
cat _state/agent_sessions.json 2>/dev/null || echo "❌ No agents were spawned"

# Check file locks
cat _state/agent_lock.json 2>/dev/null || echo "No active locks"

# View agent status
python3 .claude/hooks/agent_coordinator.py --status
```

## What to Look For

### `agent_sessions.json` Structure:

```json
{
  "active_sessions": [
    {
      "session_id": "sess-001",
      "agent_id": "prototype-data-model-specifier",
      "agent_type": "prototype-data-model-specifier",
      "task_id": "CP-3",
      "started_at": "2026-01-02T14:00:00Z",
      "heartbeat": "2026-01-02T14:05:00Z",
      "status": "running"
    }
  ],
  "completed_sessions": [
    {
      "session_id": "sess-002",
      "agent_id": "prototype-design-token-generator",
      "completed_at": "2026-01-02T14:15:00Z",
      "status": "completed"
    }
  ]
}
```

### `agent_lock.json` Structure:

```json
{
  "locks": [
    {
      "lock_id": "lock-abc123",
      "file_path": "Prototype_X/00-foundation/design-tokens.json",
      "agent_id": "prototype-design-token-generator",
      "task_id": "CP-6",
      "acquired_at": "2026-01-02T14:10:00Z",
      "expires_at": "2026-01-02T14:25:00Z"
    }
  ]
}
```

## Agent Count by Stage

| Stage | Expected Agents |
|-------|-----------------|
| Discovery | 9 agents |
| Prototype | 11 agents |
| ProductSpecs | 11 agents |
| SolArch | 17 agents |
| Implementation | 20+ agents |

## Verification Script

```bash
#!/bin/bash
# verify_multi_agent.sh

echo "🔍 Multi-Agent Execution Verification"
echo "======================================"

# Check agent sessions
if [ -f "_state/agent_sessions.json" ]; then
  active=$(jq '.active_sessions | length' _state/agent_sessions.json 2>/dev/null)
  completed=$(jq '.completed_sessions | length' _state/agent_sessions.json 2>/dev/null)
  failed=$(jq '.failed_sessions | length' _state/agent_sessions.json 2>/dev/null)

  echo "✅ Agent sessions file exists"
  echo "   Active: $active"
  echo "   Completed: $completed"
  echo "   Failed: $failed"

  if [ "$completed" -gt 0 ]; then
    echo ""
    echo "📋 Completed Agents:"
    jq -r '.completed_sessions[] | "   - \(.agent_id) (\(.session_id))"' _state/agent_sessions.json
  fi
else
  echo "❌ No agent sessions found"
  echo "   → Agents were NOT spawned"
  echo "   → Main session executed everything"
fi

# Check locks
echo ""
if [ -f "_state/agent_lock.json" ]; then
  locks=$(jq '.locks | length' _state/agent_lock.json 2>/dev/null)
  echo "🔒 Active file locks: $locks"
else
  echo "🔒 No file locks (no parallel execution)"
fi

# Check integrity status
echo ""
if [ -f "_state/integrity_status.json" ]; then
  status=$(jq -r '.status' _state/integrity_status.json)
  echo "🛡️ Process integrity: $status"
else
  echo "🛡️ No process integrity monitoring"
fi

echo ""
echo "======================================"
```
