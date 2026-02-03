---
name: solarch-reset
description: Reset Solution Architecture session by removing all generated files and state
argument-hint: <SystemName>
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-reset started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-reset ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-reset instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

This command resets the Solution Architecture generation state, allowing you to restart from a specific checkpoint or completely start over.

## Arguments

- `$ARGUMENTS` - Optional flags:
  - `--soft` (default): Reset state files only, keep generated outputs
  - `--hard`: Delete all generated files and state
  - `--phase N`: Reset to specific checkpoint N
  - `<SystemName>`: Specify which system to reset (auto-detected if not provided)

## Usage

```bash
/solarch-reset                      # Soft reset (keep files, reset state)
/solarch-reset --soft               # Same as above
/solarch-reset --hard               # Delete everything
/solarch-reset --phase 4            # Reset to checkpoint 4
/solarch-reset --phase 4 InventorySystem
```

## Execution Steps

### Soft Reset (Default)

```
LOAD _state/solarch_config.json
SYSTEM_NAME = config.system_name

BACKUP current state:
  COPY _state/solarch_progress.json → _state/solarch_progress.backup.json

RESET _state/solarch_progress.json:
  {
    "schema_version": "1.0.0",
    "current_checkpoint": 0,
    "current_phase": "init",
    "started_at": "{original_start}",
    "updated_at": NOW(),
    "reset_history": [
      {
        "reset_at": NOW(),
        "reset_type": "soft",
        "previous_checkpoint": N
      }
    ],
    "phases": { ... all reset to "pending" ... }
  }

DISPLAY:
  "State reset to checkpoint 0"
  "Generated files preserved in SolArch_{SYSTEM_NAME}/"
  "Run /solarch-resume or /solarch-init to continue"
```

### Hard Reset

```
CONFIRM with user:
  "This will DELETE all generated files. Continue? (y/n)"

IF confirmed:
  DELETE SolArch_{SYSTEM_NAME}/ (entire folder)
  DELETE _state/solarch_config.json
  DELETE _state/solarch_progress.json
  DELETE _state/solarch_input_validation.json
  DELETE traceability/solarch_traceability_register.json

  DISPLAY:
    "All Solution Architecture files deleted"
    "Run /solarch <SystemName> to start fresh"
```

### Phase Reset

```
VALIDATE checkpoint N is valid (0-12)

LOAD _state/solarch_progress.json

RESET phases after checkpoint N:
  FOR each phase WHERE phase_number > N:
    phase.status = "pending"
    phase.completed_at = null

UPDATE current_checkpoint = N
UPDATE current_phase = phase_name_for(N)

OPTIONALLY delete files generated after checkpoint N:
  IF --delete-files flag:
    DELETE files created in phases > N

DISPLAY:
  "Reset to checkpoint {N}"
  "Phases {N+1} through 12 marked as pending"
  "Run /solarch-resume to continue from checkpoint {N}"
```

### Step 1: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-reset" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Output Format

### Soft Reset

```
═══════════════════════════════════════════════════════════════
 SOLUTION ARCHITECTURE RESET - SOFT
═══════════════════════════════════════════════════════════════

System: InventorySystem

Previous State:
├─ Checkpoint: 8
└─ Phase: decisions

Reset Actions:
├─ State backed up to solarch_progress.backup.json
├─ Progress reset to checkpoint 0
└─ Generated files preserved

Files Preserved:
└─ SolArch_InventorySystem/ (all contents)

Next Steps:
├─ /solarch-resume - Continue from existing files
└─ /solarch InventorySystem - Full regeneration

═══════════════════════════════════════════════════════════════
```

### Hard Reset

```
═══════════════════════════════════════════════════════════════
 SOLUTION ARCHITECTURE RESET - HARD
═══════════════════════════════════════════════════════════════

⚠️ WARNING: This will permanently delete all generated files!

System: InventorySystem

Files to be deleted:
├─ SolArch_InventorySystem/ (45 files)
├─ _state/solarch_*.json (3 files)
└─ traceability/solarch_traceability_register.json

Confirm deletion? [y/N]: y

Deleted:
├─ SolArch_InventorySystem/ ✅
├─ _state/solarch_config.json ✅
├─ _state/solarch_progress.json ✅
├─ _state/solarch_input_validation.json ✅
└─ traceability/solarch_traceability_register.json ✅

Ready for fresh start:
  /solarch <SystemName>

═══════════════════════════════════════════════════════════════
```

### Phase Reset

```
═══════════════════════════════════════════════════════════════
 SOLUTION ARCHITECTURE RESET - PHASE 4
═══════════════════════════════════════════════════════════════

System: InventorySystem

Previous State:
├─ Checkpoint: 8
└─ Phase: decisions

Reset to Checkpoint: 4 (Building Blocks)

Phases Reset:
├─ 5: Runtime → pending
├─ 6: Quality → pending
├─ 7: Deployment → pending
├─ 8: Decisions → pending
├─ 9: Risks → pending
├─ 10: Documentation → pending
├─ 11: Traceability → pending
└─ 12: Finalize → pending

Files Status:
└─ Generated files preserved (re-run phases to regenerate)

Next: /solarch-runtime InventorySystem

═══════════════════════════════════════════════════════════════
```

## Reset Levels

| Level | State Files | Generated Files | Use Case |
|-------|-------------|-----------------|----------|
| `--soft` | Reset | Preserved | Restart validation |
| `--hard` | Deleted | Deleted | Complete restart |
| `--phase N` | Partial reset | Preserved | Redo specific phases |

## Safety Features

1. **Backup on soft reset**: Previous progress saved to `.backup.json`
2. **Confirmation on hard reset**: Requires explicit confirmation
3. **Reset history tracking**: All resets logged in progress file
4. **File preservation by default**: Only `--hard` deletes files

## Error Handling

| Error | Action |
|-------|--------|
| No active session | Display "Nothing to reset" |
| Invalid phase number | Show valid range (0-12) |
| File deletion fails | Log error, continue with others |

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch-status` | Check current state before reset |
| `/solarch-resume` | Resume after soft/phase reset |
| `/solarch` | Start fresh after hard reset |
