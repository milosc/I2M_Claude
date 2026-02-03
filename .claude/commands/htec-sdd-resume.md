---
name: htec-sdd-resume
description: Resume Implementation from last completed checkpoint
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-resume started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-resume ended '{"stage": "implementation"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "implementation"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /htec-sdd-resume instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Implementation stage rules:

```bash
# Load TDD and quality gate rules
/rules-process-integrity

# Load multi-agent coordination rules (if spawning agents)
/rules-agent-coordination

# Load Traceability rules for task IDs
/rules-traceability
```

## Usage

```
/htec-sdd-resume
/htec-sdd-resume --from 3
```

## Options

| Option | Description |
|--------|-------------|
| `--from <N>` | Resume from specific checkpoint |

## Procedure

### 1. Determine Resume Point

```
READ _state/implementation_progress.json

DETERMINE last_checkpoint:
    IF --from specified:
        last_checkpoint = --from
    ELSE:
        last_checkpoint = progress.current_checkpoint

VALIDATE checkpoint state:
    - Check required files exist
    - Check task registry integrity
    - Check for blocked tasks

CONTINUE from last_checkpoint + 1:
    INVOKE /htec-sdd with starting checkpoint
```

## Output

```
Resuming Implementation
═══════════════════════════════════════

System: InventorySystem
Last checkpoint: 4 (Features 50%+)
Last activity: 2024-01-17 14:32

Progress snapshot:
  Tasks: 32/47 completed
  Coverage: 84%
  Blocked: 0

Resuming from: Checkpoint 5 (P0 Complete)

[Continues with normal execution output...]
```

## Error Handling

If state is corrupted:

```
Resume Failed
═══════════════════════════════════════

Issue: Task registry inconsistent

Details:
  - T-033 marked complete but no test file
  - T-034 dependencies not met

Options:
  1. Run /htec-sdd-reset --checkpoint 4 to reset
  2. Run /htec-sdd-status --verbose to investigate
  3. Manually fix traceability/task_registry.json
```


---

## Related Commands

- `/htec-sdd-status` - Check current state
- `/htec-sdd-reset` - Reset if needed
- `/htec-sdd` - Full execution
