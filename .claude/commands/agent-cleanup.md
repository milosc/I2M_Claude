---
description: Clean up stale agent sessions and locks
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /agent-cleanup started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /agent-cleanup ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /agent-cleanup instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## Usage

```
/agent-cleanup                    # Clean stale resources (safe)
/agent-cleanup --force            # Force cleanup all (use with caution)
/agent-cleanup --agent <id>       # Clean specific agent resources
/agent-cleanup --session <id>     # Terminate specific session
/agent-cleanup --lock <file>      # Force release specific lock
```

## Execution

### Safe Cleanup (Default)

```bash
# Clean stale locks and unresponsive sessions
python3 .claude/hooks/agent_coordinator.py --cleanup-stale
```

This will:
- Release locks that have expired
- Terminate sessions that haven't sent heartbeats
- Reset tasks that were stuck in_progress

### Force Cleanup

```bash
# Force cleanup for specific agent
python3 .claude/hooks/post_task_completion.py --cleanup-all --agent-id <id>
```

### Session Termination

```bash
# End a specific session
python3 .claude/hooks/post_task_completion.py --session-id <id> --status terminated
```

### Lock Release

```bash
# Check lock status first
python3 .claude/hooks/agent_coordinator.py --check-lock <file_path>

# Force release (requires agent-id that owns the lock, or use admin override)
python3 .claude/hooks/agent_coordinator.py --release-lock <agent_id> <file_path>
```

## Output Format

```markdown
# Agent Cleanup Report

## Summary
- **Locks Released**: {count}
- **Sessions Terminated**: {count}
- **Tasks Reset**: {count}

## Details

### Released Locks
| File | Was Held By | Duration | Reason |
|------|-------------|----------|--------|
| src/OrderService.ts | developer-001 | 45m | expired |

### Terminated Sessions
| Session | Agent | Reason |
|---------|-------|--------|
| session-abc123 | developer-001 | heartbeat_timeout |

### Reset Tasks
| Task | Previous Status | Reset To |
|------|-----------------|----------|
| T-015 | in_progress | pending |

---
*Cleanup completed at {timestamp}*
```

## Safety Notes

1. **Default cleanup is safe** - Only affects expired/stale resources
2. **Force cleanup** may interrupt active work - Use only when necessary
3. **Lock release** should match the owning agent - Admin override for emergencies
4. **Task reset** marks incomplete tasks as pending for retry

## When to Use

| Scenario | Command |
|----------|---------|
| Routine maintenance | `/agent-cleanup` |
| Stuck session | `/agent-cleanup --session <id>` |
| File locked by crashed agent | `/agent-cleanup --lock <file>` |
| Agent went rogue | `/agent-cleanup --agent <id>` |
| System reset | `/agent-cleanup --force` |



---

## Related

- **Agent Status**: `/agent-status`
- **Agent Coordinator**: `.claude/hooks/agent_coordinator.py`
- **Post-Completion Hook**: `.claude/hooks/post_task_completion.py`
