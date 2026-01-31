---
description: Display Solution Architecture generation status and progress
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-status started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-status ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-status instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

This command displays the current status of Solution Architecture generation, including completed checkpoints, pending phases, and any validation issues.

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` (auto-detected from config if not provided)

## Usage

```bash
/solarch-status
/solarch-status InventorySystem
```

## Execution Steps

### Step 1: Execute

```
DETECT system:
  IF $ARGUMENTS provided:
    SYSTEM_NAME = $ARGUMENTS
  ELSE IF _state/solarch_config.json exists:
    SYSTEM_NAME = config.system_name
  ELSE:
    DISPLAY "No active Solution Architecture session found"
    RETURN

LOAD _state/solarch_config.json
LOAD _state/solarch_progress.json

DISPLAY status:
  System: {SYSTEM_NAME}
  Started: {progress.started_at}
  Last Updated: {progress.updated_at}

  Current Checkpoint: {progress.current_checkpoint}
  Current Phase: {progress.current_phase}

  Phase Status:
  ┌─────────────────────────────────────────────────────────────┐
  │ CP  │ Phase            │ Status      │ Completed At        │
  ├─────────────────────────────────────────────────────────────┤
  │ 0   │ Initialize       │ ✅/⏳/❌    │ timestamp           │
  │ 1   │ Validate [BLOCK] │ ✅/⏳/❌    │ timestamp           │
  │ 2   │ Context & Goals  │ ✅/⏳/❌    │ timestamp           │
  │ 3   │ Strategy         │ ✅/⏳/❌    │ timestamp           │
  │ 4   │ Building Blocks  │ ✅/⏳/❌    │ timestamp           │
  │ 5   │ Runtime          │ ✅/⏳/❌    │ timestamp           │
  │ 6   │ Quality          │ ✅/⏳/❌    │ timestamp           │
  │ 7   │ Deployment       │ ✅/⏳/❌    │ timestamp           │
  │ 8   │ Decisions        │ ✅/⏳/❌    │ timestamp           │
  │ 9   │ Risks            │ ✅/⏳/❌    │ timestamp           │
  │ 10  │ Documentation    │ ✅/⏳/❌    │ timestamp           │
  │ 11  │ Trace [BLOCK]    │ ✅/⏳/❌    │ timestamp           │
  │ 12  │ Finalize         │ ✅/⏳/❌    │ timestamp           │
  └─────────────────────────────────────────────────────────────┘

  Legend: ✅ Completed │ ⏳ Pending │ ❌ Failed │ [BLOCK] = Blocking

IF validation_history exists:
  DISPLAY recent validations:
    Last 5 validation runs with results

IF failures exist in FAILURES_LOG.md:
  DISPLAY warning:
    ⚠️ {N} failures logged - check _state/FAILURES_LOG.md

SUGGEST next action:
  IF all phases completed:
    "Solution Architecture generation complete!"
    "Output: SolArch_{SYSTEM_NAME}/"
  ELSE:
    "Next: /solarch-{next_phase} {SYSTEM_NAME}"
```

### Step 2: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-status" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Output Format

### Active Session

```
═══════════════════════════════════════════════════════════════
 SOLUTION ARCHITECTURE STATUS
═══════════════════════════════════════════════════════════════

System: InventorySystem
Started: 2025-12-22T10:00:00Z
Updated: 2025-12-22T11:30:00Z

Current Checkpoint: 8
Current Phase: decisions

Phase Progress:
┌────┬───────────────────┬───────────┬─────────────────────┐
│ CP │ Phase             │ Status    │ Completed           │
├────┼───────────────────┼───────────┼─────────────────────┤
│ 0  │ Initialize        │ ✅ Passed │ 2025-12-22T10:00:00 │
│ 1  │ Validate [BLOCK]  │ ✅ Passed │ 2025-12-22T10:05:00 │
│ 2  │ Context & Goals   │ ✅ Passed │ 2025-12-22T10:15:00 │
│ 3  │ Strategy          │ ✅ Passed │ 2025-12-22T10:25:00 │
│ 4  │ Building Blocks   │ ✅ Passed │ 2025-12-22T10:40:00 │
│ 5  │ Runtime           │ ✅ Passed │ 2025-12-22T10:55:00 │
│ 6  │ Quality           │ ✅ Passed │ 2025-12-22T11:05:00 │
│ 7  │ Deployment        │ ✅ Passed │ 2025-12-22T11:20:00 │
│ 8  │ Decisions         │ ⏳ Active │ -                   │
│ 9  │ Risks             │ ⏳ Pending│ -                   │
│ 10 │ Documentation     │ ⏳ Pending│ -                   │
│ 11 │ Trace [BLOCK]     │ ⏳ Pending│ -                   │
│ 12 │ Finalize          │ ⏳ Pending│ -                   │
└────┴───────────────────┴───────────┴─────────────────────┘

Artifacts Generated:
├─ ADRs: 7 of 10+
├─ C4 Diagrams: 4
├─ arc42 Sections: 8 of 11
└─ Components: 5

Next: /solarch-decisions InventorySystem

═══════════════════════════════════════════════════════════════
```

### No Active Session

```
═══════════════════════════════════════════════════════════════
 SOLUTION ARCHITECTURE STATUS
═══════════════════════════════════════════════════════════════

No active Solution Architecture session found.

To start a new session:
  /solarch <SystemName>

Or initialize manually:
  /solarch-init <SystemName>

═══════════════════════════════════════════════════════════════
```

### With Failures

```
═══════════════════════════════════════════════════════════════
 SOLUTION ARCHITECTURE STATUS
═══════════════════════════════════════════════════════════════

System: InventorySystem
Current Checkpoint: 4

⚠️ WARNINGS:

3 failures logged:
├─ ADR-003 generation incomplete
├─ C4 container diagram missing external systems
└─ Component registration failed

Check: _state/FAILURES_LOG.md

Current phase can continue - failures are non-blocking.

Next: /solarch-runtime InventorySystem

═══════════════════════════════════════════════════════════════
```

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch` | Start full orchestration |
| `/solarch-resume` | Resume from current checkpoint |
| `/solarch-reset` | Reset state |
