---
description: Reset ProductSpecs session by removing all generated files and state
argument-hint: <SystemName>
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-reset started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-reset ended '{"stage": "productspecs"}'
---


# /productspecs-reset - Reset ProductSpecs State

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs-reset instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for module/test ID management:

```bash
# Load Traceability rules (includes module ID format MOD-XXX-XXX-NN)
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Required: `<SystemName>` followed by optional flags:
  - `--soft` - Reset state files only, keep generated outputs (default)
  - `--hard` - Delete everything including generated outputs
  - `--phase <N>` - Reset to specific phase (0-8)

## Examples

```bash
/productspecs-reset InventorySystem             # Soft reset
/productspecs-reset InventorySystem --soft      # Same as above
/productspecs-reset InventorySystem --hard      # Delete all outputs
/productspecs-reset InventorySystem --phase 3   # Reset to phase 3
```

## Execution Steps

### Step 1: Parse Arguments

```
Extract:
  - SystemName (required)
  - Reset mode: soft | hard | phase
  - Phase number (if --phase)
```

### Step 2: Confirm Action

**For --hard reset:**

```
⚠️  WARNING: Hard Reset

This will DELETE all ProductSpecs outputs:
  ProductSpecs_<SystemName>/
  _state/productspecs_*.json
  traceability/productspecs_traceability_register.json

Type 'DELETE' to confirm, or 'cancel' to abort:
```

**For --soft or --phase:**

```
ProductSpecs Reset: <SystemName>

Mode: Soft Reset
  • State files will be reset
  • Generated outputs will be preserved
  • You can resume from Phase 0

Proceed? (y/n):
```

### Step 3: Execute Reset

#### Soft Reset (`--soft`)

Reset state files only:

```bash
# Reset progress file
# Set all phases to "pending"
# Clear validation_history
# Reset current_phase to 0

# Update _state/productspecs_progress.json
{
  "current_phase": 0,
  "phases": {
    "init": { "status": "pending", ... },
    "validate": { "status": "pending", ... },
    ...
  },
  "validation_history": []
}
```

#### Hard Reset (`--hard`)

Delete everything:

```bash
# Delete ProductSpecs folder
rm -rf ProductSpecs_<SystemName>/

# Delete state files (from ROOT _state/)
rm -f _state/productspecs_config.json
rm -f _state/productspecs_progress.json

# Delete traceability register
rm -f traceability/productspecs_traceability_register.json
```

#### Phase Reset (`--phase <N>`)

Reset to specific phase:

```bash
# Mark phases N+ as pending
# Keep phases 0 to N-1 as completed
# Set current_phase to N

# For example, --phase 3:
"phases": {
  "init": { "status": "completed" },
  "validate": { "status": "completed" },
  "extract": { "status": "completed" },
  "modules_core": { "status": "pending" },  # Phase 3+
  "modules_extended": { "status": "pending" },
  "contracts": { "status": "pending" },
  "tests": { "status": "pending" },
  "traceability": { "status": "pending" },
  "export": { "status": "pending" }
}
```

### Step 4: Clean Up (for --hard)

If doing hard reset, also:

1. Remove any orphaned registry entries in `traceability/spec_registry.json`
2. Clean up any references in other traceability files

### Step 5: Display Summary

**Soft Reset:**
```
═══════════════════════════════════════════════════════
  PRODUCTSPECS RESET COMPLETE
═══════════════════════════════════════════════════════

  System:      <SystemName>
  Mode:        Soft Reset
  Reset To:    Phase 0

  State Files: ✅ Reset
  Outputs:     ✅ Preserved

═══════════════════════════════════════════════════════

  Next Steps:
  • /productspecs <SystemName>     - Start fresh
  • /productspecs-status           - View current state

═══════════════════════════════════════════════════════
```

**Hard Reset:**
```
═══════════════════════════════════════════════════════
  PRODUCTSPECS DELETED
═══════════════════════════════════════════════════════

  System:      <SystemName>

  Deleted:
  ✅ ProductSpecs_<SystemName>/
  ✅ _state/productspecs_*.json
  ✅ traceability/productspecs_traceability_register.json

═══════════════════════════════════════════════════════

  To regenerate:
  • /productspecs-init <SystemName>

═══════════════════════════════════════════════════════
```

**Phase Reset:**
```
═══════════════════════════════════════════════════════
  PRODUCTSPECS RESET TO PHASE 3
═══════════════════════════════════════════════════════

  System:      <SystemName>
  Reset To:    Phase 3 - Modules Core

  Phases Preserved:   0-2 (✅)
  Phases Reset:       3-8 (⏳)

═══════════════════════════════════════════════════════

  Next Steps:
  • /productspecs-modules <SystemName>  - Continue from Phase 3
  • /productspecs-resume               - Auto-resume

═══════════════════════════════════════════════════════
```

## Reset Modes Summary

| Mode | State Files | Outputs | Use Case |
|------|-------------|---------|----------|
| `--soft` | Reset | Keep | Re-run with existing outputs |
| `--hard` | Delete | Delete | Start completely fresh |
| `--phase N` | Partial | Keep | Redo specific phases |

## Error Handling

| Error | Action |
|-------|--------|
| SystemName not provided | Show usage and exit |
| ProductSpecs folder doesn't exist | Show warning, clean state files anyway |
| State file missing | Skip, continue with others |
| Invalid phase number | Show valid range (0-8), exit |

## Safety Features

1. **Confirmation required** for `--hard` reset
2. **Backup suggestion** before hard reset:
   ```
   Tip: Create a backup before hard reset:
   cp -r ProductSpecs_<SystemName>/ ProductSpecs_<SystemName>_backup/
   ```
3. **Phase reset preserves work** - doesn't delete outputs

## Related Commands

| Command | Description |
|---------|-------------|
| `/productspecs-init` | Reinitialize after hard reset |
| `/productspecs-status` | Check current state |
| `/productspecs-resume` | Continue after soft/phase reset |
