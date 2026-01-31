---
description: Reset Prototype session by removing all generated files and state
argument-hint: <SystemName>
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-reset started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-reset ended '{"stage": "prototype"}'
---


# /prototype-reset - Reset Prototype State

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-reset instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Assembly-First and traceability rules:

```bash
# Assembly-First rules (loaded automatically in Prototype stage)
/_assembly_first_rules

# Traceability rules for ID management
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Optional flags and system name:
  - `<SystemName>` - Target prototype (required if multiple exist)
  - `--soft` - Reset progress only, keep outputs (default)
  - `--hard` - Delete all prototype outputs
  - `--phase <N>` - Reset specific phase only

## Prerequisites

- Prototype exists: `Prototype_<SystemName>/`

## Modes

### Soft Reset (Default)

Resets progress tracking while preserving generated outputs.

```
/prototype-reset InventorySystem
/prototype-reset InventorySystem --soft
```

**Actions:**
- Reset `_state/prototype_progress.json` to initial state
- Clear `_state/FAILURES_LOG.md`
- Keep all generated files in `00-foundation/`, `01-components/`, etc.

**Use Case:**
- Re-run phases with existing outputs
- Fix progress file corruption
- Start over without regenerating everything

### Hard Reset

Deletes all prototype outputs and state.

```
/prototype-reset InventorySystem --hard
```

**Actions:**
- Delete entire `Prototype_<SystemName>/` folder
- Remove from `traceability/prototype_traceability_register.json`

**Use Case:**
- Complete fresh start
- Change Discovery source
- Major restructuring needed

### Phase Reset

Reset a specific phase to re-run it.

```
/prototype-reset InventorySystem --phase 8
```

**Actions:**
- Reset phase 8 (components) status to "pending"
- Delete outputs from phase 8 only
- Keep all other phases intact

**Use Case:**
- Re-run specific phase after changes
- Fix issue in one phase without full reset

---

## Modes

### Soft Reset (Default)

```
If $ARGUMENTS includes SystemName:
  - Use Prototype_<SystemName>/
Else:
  - List all Prototype_*/ folders
  - If one: Use it
  - If multiple: Ask user
  - If none: Error
```

### Step 2: Confirm Action

```
═══════════════════════════════════════════════════════
  PROTOTYPE RESET
═══════════════════════════════════════════════════════

  System:              <SystemName>
  Mode:                <Soft/Hard/Phase>

  Current State:
  ├── Phases Completed: 8/14
  ├── Output Files:     45
  └── Change Requests:  2

═══════════════════════════════════════════════════════

  ⚠️  WARNING: This action cannot be undone.

  [Soft Reset]
  - Progress will be reset to Phase 0
  - All 45 output files will be KEPT
  - Change requests will be KEPT

  [Hard Reset]
  - Entire Prototype_<SystemName>/ will be DELETED
  - All 45 output files will be DELETED
  - 2 change requests will be DELETED

  [Phase 8 Reset]
  - Phase 8 (Components) will be reset
  - 15 component files will be DELETED
  - Other phases unaffected

═══════════════════════════════════════════════════════

  Type 'CONFIRM' to proceed or 'cancel' to abort:
```

### Step 3: Execute Reset

#### Soft Reset

```python
# Reset progress file
progress = {
  "schema_version": "2.3",
  "current_phase": 0,
  "current_checkpoint": 0,
  "started_at": "<new_timestamp>",
  "updated_at": "<new_timestamp>",
  "phases": {
    "initialize": {"phase_number": 0, "status": "pending", ...},
    "validate_discovery": {"phase_number": 1, "status": "pending", ...},
    # ... all phases reset to pending
  },
  "validation_history": [],
  "reset_history": [
    {
      "timestamp": "<timestamp>",
      "mode": "soft",
      "previous_phase": 8
    }
  ]
}

# Clear failures log
write "_state/FAILURES_LOG.md" with empty template
```

#### Hard Reset

```bash
# Remove prototype folder
rm -rf Prototype_<SystemName>/

# Update traceability
# Remove entry from prototype_traceability_register.json
```

#### Phase Reset

```python
# Reset specific phase
progress["phases"]["components"] = {
  "phase_number": 8,
  "status": "pending",
  "started_at": null,
  "completed_at": null,
  "outputs": []
}

# Delete phase outputs
# For phase 8 (components):
rm -rf Prototype_<SystemName>/01-components/*

# Update current_phase if needed
if progress["current_phase"] > 8:
  progress["current_phase"] = 8
```

### Step 4: Display Confirmation

```
═══════════════════════════════════════════════════════
  RESET COMPLETE
═══════════════════════════════════════════════════════

  Mode:                Soft Reset
  System:              <SystemName>

  Actions Taken:
  ├── Progress reset to Phase 0
  ├── Failures log cleared
  └── Output files preserved (45 files)

═══════════════════════════════════════════════════════

  Next Steps:
  • /prototype <SystemName>     - Run from beginning
  • /prototype-resume           - Resume (will start at Phase 0)

═══════════════════════════════════════════════════════
```

---

## Phase Mapping

For `--phase <N>` option:

| Phase | Name | Outputs Deleted |
|-------|------|-----------------|
| 0 | Initialize | `_state/*` (except config) |
| 1 | Validate Discovery | `_state/discovery_summary.json` |
| 2 | Requirements | `_state/requirements_registry.json` |
| 3 | Data Model | `04-implementation/data-model.md` |
| 4 | API Contracts | `04-implementation/api-contracts.json` |
| 5 | Test Data | `04-implementation/test-data/*` |
| 6 | Design Brief | `00-foundation/design-brief.md`, `design-principles.md` |
| 7 | Design Tokens | `00-foundation/design-tokens.json`, `color-system.md`, etc. |
| 8 | Components | `01-components/*` |
| 9 | Screens | `02-screens/*` |
| 10 | Interactions | `03-interactions/*` |
| 11 | Sequencer | `04-implementation/build-sequence.md`, `prompts/*` |
| 12 | Code Gen | `prototype/*` |
| 13 | QA | `05-validation/qa-report.md` |
| 14 | UI Audit | `05-validation/ui-audit-report.md`, `screenshots/*`, `reports/*` |

---

## Safety Features

1. **Confirmation Required**: All resets require typing 'CONFIRM'
2. **Reset History**: Soft resets log to `reset_history` array
3. **No Accidental Hard Reset**: Hard reset requires explicit `--hard` flag
4. **Traceability Preserved**: Soft reset keeps traceability links

---

## Error Handling

| Error | Action |
|-------|--------|
| Prototype not found | Display error, list available |
| Permission denied | Display error, suggest fix |
| Phase number invalid | Display valid range (0-14) |

---

## Examples

### Example 1: Soft Reset

```
/prototype-reset InventorySystem

> Resetting progress for Prototype_InventorySystem/
> Mode: Soft (preserve outputs)
> Type 'CONFIRM': CONFIRM
> ✅ Progress reset to Phase 0
```

### Example 2: Hard Reset

```
/prototype-reset InventorySystem --hard

> ⚠️ HARD RESET: All outputs will be deleted!
> Type 'CONFIRM': CONFIRM
> ✅ Deleted Prototype_InventorySystem/
> ✅ Removed from traceability register
```

### Example 3: Phase Reset

```
/prototype-reset InventorySystem --phase 8

> Resetting Phase 8 (Components)
> Files to delete: 15
> Type 'CONFIRM': CONFIRM
> ✅ Phase 8 reset
> ✅ Current phase set to 8
```

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype` | Run full prototype |
| `/prototype-init` | Initialize new prototype |
| `/prototype-status` | Check current status |
| `/prototype-resume` | Resume from checkpoint |
