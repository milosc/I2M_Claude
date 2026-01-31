---
description: Reset Discovery session by removing all generated files and state
argument-hint: <SystemName>
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-reset started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-reset ended '{"stage": "discovery"}'
---


# /discovery-reset - Reset Discovery Session

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-reset instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Discovery-specific rules. Load them now:

```bash
# Load Discovery rules (includes PDF handling, input processing, output structure)
/rules-discovery

# Load Traceability rules (includes ID formats, source linking)
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Optional: `--hard` to delete all generated files (default: soft reset)

## Prerequisites

- Existing discovery session (state files exist)

## Skills Used

None - utility command managing state

## Execution Steps

### Soft Reset (Default)

Resets state files but preserves generated outputs.

1. **Confirm Reset**
   ```
   ⚠️  SOFT RESET WARNING

   This will reset discovery state files:
   • _state/discovery_config.json
   • _state/discovery_progress.json
   • _state/discovery_context.json
   • _state/discovery_materials_inventory.json
   • _state/discovery_error_log.md

   Generated outputs in ClientAnalysis_<SystemName>/ will be PRESERVED.
   Traceability registries will be PRESERVED.

   Continue? [Proceeding...]
   ```

2. **Reset State Files**
   - Reset `discovery_config.json`:
     - status: "not_started"
     - current_phase: 0
     - current_checkpoint: null
   - Reset `discovery_progress.json`:
     - All phases to "pending"
     - overall_progress: 0
   - Clear `discovery_context.json`:
     - Keep system_name
     - Clear session_history
     - Add reset note
   - Clear `discovery_materials_inventory.json`
   - Clear `discovery_error_log.md`

3. **Report Reset**
   ```
   ✅ Soft reset complete

   State files reset. Generated outputs preserved.
   Run /discovery-init to reinitialize.
   ```

### Hard Reset (--hard flag)

Deletes everything and starts completely fresh.

1. **Confirm Hard Reset**
   ```
   ⚠️  HARD RESET WARNING

   This will DELETE:
   • All state files in _state/discovery_*
   • All outputs in ClientAnalysis_<SystemName>/
   • All traceability data (registries will be reset)

   Raw materials in <InputPath>/ will be PRESERVED.

   This action is IRREVERSIBLE.

   Continue? [Proceeding...]
   ```

2. **Delete Files**
   - Delete `_state/discovery_*.json` and `_state/discovery_*.md`
   - Delete `ClientAnalysis_<SystemName>/` folder
   - Reset traceability registries to empty:
     - `traceability/trace_matrix.json` → empty chains
     - `traceability/pain_point_registry.json` → empty items
     - `traceability/user_type_registry.json` → empty items
     - `traceability/jtbd_registry.json` → empty items
     - `traceability/requirements_registry.json` → empty items
     - `traceability/screen_registry.json` → empty items
   - Keep `traceability/TRACEABILITY_MATRIX_MASTER.md` as template

3. **Report Hard Reset**
   ```
   ✅ Hard reset complete

   All discovery state and outputs deleted.
   Traceability registries reset to empty.
   Raw materials preserved.

   Run /discovery <SystemName> <InputPath> to start fresh.
   ```

## Reset Options

| Option | State Files | Outputs | Traceability |
|--------|-------------|---------|--------------|
| Soft (default) | Reset | Preserved | Preserved |
| Hard (--hard) | Deleted | Deleted | Reset to empty |

## Safety Checks

Before reset:
- Check for uncommitted changes
- Warn about data loss
- Require confirmation (implicit in command execution)

## What's Preserved

| Item | Soft Reset | Hard Reset |
|------|------------|------------|
| Raw materials | ✅ | ✅ |
| Generated outputs | ✅ | ❌ |
| State files | ❌ (reset) | ❌ (deleted) |
| Traceability registries | ✅ | ❌ (emptied) |
| Pipeline config | ✅ | ✅ |

## Example Usage

```bash
# Soft reset - keep outputs, reset progress
/discovery-reset

# Hard reset - delete everything, start fresh
/discovery-reset --hard
```

## Recovery Note

After reset, you can:
1. Run `/discovery-init` to reinitialize (soft reset)
2. Run `/discovery <SystemName> <InputPath>` to start fresh (hard reset)

## Outputs

Soft reset:
- State files reset to initial values
- Generated files preserved

Hard reset:
- State files deleted
- Output folder deleted
- Traceability registries emptied

## What's Preserved## Next Command

After reset:
- `/discovery-init <SystemName> <InputPath>` - Reinitialize
- `/discovery <SystemName> <InputPath>` - Full run from start
