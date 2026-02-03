---
name: agent-status
description: Display active agent sessions and coordination status
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /agent-status started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /agent-status ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /agent-status instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## Usage

```
/agent-status              # Full status report
/agent-status --brief      # Quick summary
/agent-status --locks      # Lock status only
/agent-status --sessions   # Session status only
/agent-status --integrity  # Process integrity status only
```

## Execution

### Step 1: Get Status

```python
# Get overall coordination status
result = python3 .claude/hooks/agent_coordinator.py --status --json

# Parse and display
```

## Output Format

### Full Status Report

```markdown
# Agent Coordination Status

## Overview
- **System Health**: {HEALTHY | WARNING | CRITICAL}
- **Active Agents**: {count} / {max}
- **Capacity Remaining**: {count}

## Active Sessions

| Session | Agent Type | Task | Started | Duration |
|---------|------------|------|---------|----------|
| session-abc123 | implementation-developer | T-015 | 10:30 | 15m |
| session-def456 | quality-bug-hunter | review | 10:35 | 10m |

## Active Locks

| File | Locked By | Task | Expires In |
|------|-----------|------|------------|
| src/services/OrderService.ts | developer-001 | T-015 | 10m |

## Process Integrity

| Monitor | Status | Last Check | Issues |
|---------|--------|------------|--------|
| Traceability Guardian | HEALTHY | 2m ago | 0 |
| State Watchdog | HEALTHY | 30s ago | 0 |
| Playbook Enforcer | WARNING | 5m ago | 2 |

### Active Violations
- TRC-001 (HIGH): Task T-023 missing module_ref

### Veto Status
{None active | ACTIVE: {details}}

## Recent Completions (last hour)

| Session | Agent | Task | Status | Duration |
|---------|-------|------|--------|----------|
| session-111 | implementation-developer | T-012 | completed | 25m |
| session-222 | implementation-developer | T-013 | completed | 18m |

---
*Status as of {timestamp}*
```

### Brief Summary

```
AGENTS: 3/12 active | LOCKS: 2 | INTEGRITY: HEALTHY
```



---

## Related

- **Agent Coordinator**: `.claude/hooks/agent_coordinator.py`
- **Coordination Rule**: `.claude/rules/agent-coordination.md`
