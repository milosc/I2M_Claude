---
description: Reset Implementation session by removing all generated files and state
argument-hint: <SystemName>
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-reset started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-reset ended '{"stage": "implementation"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "implementation"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /htec-sdd-reset instruction_start '{"stage": "implementation", "method": "instruction-based"}'
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
/htec-sdd-reset
/htec-sdd-reset --soft
/htec-sdd-reset --hard
/htec-sdd-reset --checkpoint 3
```

## Options

| Option | Description |
|--------|-------------|
| `--soft` | Reset state files only, keep code (default) |
| `--hard` | Delete all implementation outputs |
| `--checkpoint <N>` | Reset to specific checkpoint |
| `--tasks` | Reset task registry only |

## Reset Modes

### Soft Reset (default)

Resets state files while preserving generated code:

```
RESET:
  _state/implementation_progress.json → checkpoint 0
  traceability/task_registry.json → all tasks pending

PRESERVE:
  Implementation_<System>/src/*
  Implementation_<System>/tests/*
  Implementation_<System>/docs/*
```

### Hard Reset

Deletes all implementation outputs:

```
DELETE:
  Implementation_<System>/  (entire folder)
  _state/implementation_config.json
  _state/implementation_progress.json
  _state/implementation_input_validation.json
  traceability/task_registry.json
  traceability/review_registry.json
```

### Checkpoint Reset

Resets to a specific checkpoint:

```
/htec-sdd-reset --checkpoint 3

RESET tasks after checkpoint 3:
  - Phase 4 tasks → pending
  - Phase 5 tasks → pending

PRESERVE:
  - Phase 3 tasks → completed
  - Generated infrastructure code
```

## Procedure

### 1. Execute Reset

```
READ _state/implementation_config.json
DETERMINE reset mode from options

IF --hard:
    CONFIRM with user: "Delete all implementation outputs?"
    IF confirmed:
        DELETE Implementation_<System>/
        DELETE state files
        LOG "Hard reset complete"

ELIF --checkpoint N:
    READ traceability/task_registry.json
    FOR EACH task WHERE task.phase > N:
        task.status = "pending"
        task.implementation = null
    UPDATE _state/implementation_progress.json:
        current_checkpoint = N
    LOG "Reset to checkpoint {N}"

ELSE:  # soft reset
    RESET _state/implementation_progress.json
    RESET traceability/task_registry.json (status only)
    LOG "Soft reset complete"
```

## Output

### Soft Reset

```
Implementation Reset (Soft)
═══════════════════════════════════════

Reset:
  ✓ _state/implementation_progress.json
  ✓ traceability/task_registry.json (47 tasks → pending)

Preserved:
  • Implementation_InventorySystem/src/ (67 files)
  • Implementation_InventorySystem/tests/ (89 files)

To continue: /htec-sdd-implement
```

### Hard Reset

```
Implementation Reset (Hard)
═══════════════════════════════════════

Deleted:
  ✓ Implementation_InventorySystem/ (156 files)
  ✓ _state/implementation_*.json (3 files)
  ✓ traceability/task_registry.json
  ✓ traceability/review_registry.json

To start fresh: /htec-sdd-init InventorySystem
```

### Checkpoint Reset

```
Implementation Reset (Checkpoint 3)
═══════════════════════════════════════

Reset to: Checkpoint 3 (Infrastructure Complete)

Tasks reset: 39 (Phase 4 + Phase 5)
Tasks preserved: 8 (Phase 3)

Preserved code:
  • src/config/*
  • src/lib/*
  • tests/setup/*

To continue: /htec-sdd-implement
```

## Confirmation

Hard reset requires explicit confirmation:

```
⚠️  WARNING: Hard reset will delete all implementation outputs.

This will delete:
  - 156 source files
  - 89 test files
  - All task progress

Type 'DELETE' to confirm:
```


---

## Related Commands

- `/htec-sdd-init` - Reinitialize after hard reset
- `/htec-sdd-resume` - Resume from checkpoint
- `/htec-sdd-status` - Check current state
