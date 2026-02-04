---
name: prototype-resume
description: Resume Prototype generation from last completed checkpoint
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-resume started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: |
            SYSTEM_NAME=$(cat _state/session.json 2>/dev/null | grep -o '"project"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"project"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//' || echo "")
            if [ -n "$SYSTEM_NAME" ] && [ "$SYSTEM_NAME" != "pending" ]; then
              uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_prototype_output.py" --system-name "$SYSTEM_NAME" --quick
            else
              echo '{"result": "skip", "reason": "System name not found in session"}'
              exit 0
            fi
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-resume ended '{"stage": "prototype"}'
---


# /prototype-resume - Resume Prototype Generation

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-resume instruction_start '{"stage": "prototype", "method": "instruction-based"}'
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

- `$ARGUMENTS` - Optional: `<SystemName>` or path to `Prototype_<SystemName>/`
  - If not provided: Auto-detect or list available

## Prerequisites

- Prototype initialized: `Prototype_<SystemName>/` exists
- Progress file: `_state/prototype_progress.json` exists

## Execution Steps

### Step 1: Locate Prototype

```
If $ARGUMENTS provided:
  - Use Prototype_<SystemName>/ or provided path
Else:
  - List all Prototype_*/ folders
  - If one found: Use it
  - If multiple: Ask user to specify
  - If none: Display error
```

### Step 2: Read Progress State

Read `_state/prototype_progress.json`:

```json
{
  "current_phase": 5,
  "phases": {
    "initialize": { "status": "completed" },
    "validate_discovery": { "status": "completed" },
    "requirements": { "status": "completed" },
    "data_model": { "status": "completed" },
    "api_contracts": { "status": "failed" },  // <-- Resume from here
    "test_data": { "status": "pending" }
  }
}
```

### Step 3: Determine Resume Point

Logic:
1. Find first phase with status `in_progress` or `failed`
2. If none found, find first `pending` phase
3. If all `completed`, display "Nothing to resume"

```
Resume Point Detection:

✅ completed → Skip
✅ completed → Skip
✅ completed → Skip
❌ failed    → RESUME FROM HERE
⏳ pending   → Continue after
⏳ pending   → Continue after
```

### Step 4: Display Resume Information

```
═══════════════════════════════════════════════════════
  PROTOTYPE RESUME
═══════════════════════════════════════════════════════

  System:              <SystemName>
  Progress File:       _state/prototype_progress.json

  Completed Phases:
  ├── Phase 0:  Initialize           ✅
  ├── Phase 1:  Validate Discovery   ✅
  ├── Phase 2:  Requirements         ✅
  ├── Phase 3:  Data Model           ✅
  └── Phase 4:  API Contracts        ❌ Failed

  Resume Point:        Phase 4 (API Contracts)
  Last Error:          <error message if available>

  Pending Phases:      10 remaining

═══════════════════════════════════════════════════════

  Options:
  [C] Continue - Resume from Phase 4
  [R] Restart Phase - Clear Phase 4 and restart
  [S] Skip Phase - Mark as skipped, continue to Phase 5
  [A] Abort - Exit without changes

═══════════════════════════════════════════════════════
```

### Step 5: Execute Based on Choice

#### Option C: Continue

1. Re-read skill for failed phase
2. Execute phase with same inputs
3. On success: Update progress, continue to next phase
4. On failure: Offer same options again

#### Option R: Restart Phase

1. Clear phase state:
   ```json
   {
     "api_contracts": {
       "status": "pending",
       "started_at": null,
       "completed_at": null,
       "outputs": []
     }
   }
   ```
2. Execute phase fresh
3. Continue normally

#### Option S: Skip Phase

1. Mark phase as skipped:
   ```json
   {
     "api_contracts": {
       "status": "skipped",
       "skipped_at": "<timestamp>",
       "reason": "User requested skip"
     }
   }
   ```
2. Log to FAILURES_LOG.md
3. Continue to next phase

#### Option A: Abort

1. Display current state
2. Exit without changes

### Step 6: Continue Execution

After resuming, execute remaining phases in order:

```
Resuming from Phase 4...

Phase 4: API Contracts
├── Reading skill...
├── Executing...
├── Validating checkpoint 4...
└── ✅ Complete

Phase 5: Test Data
├── Reading skill...
├── Executing...
├── Validating checkpoint 5...
└── ✅ Complete

...continuing to Phase 14
```

### Step 7: Completion

Same as `/prototype` completion output.

---

## State File Updates

### On Resume

```json
{
  "resume_history": [
    {
      "timestamp": "<YYYY-MM-DD HH:MM:SS>",
      "from_phase": 4,
      "reason": "Manual resume",
      "previous_status": "failed"
    }
  ]
}
```

### On Skip

```json
{
  "phases": {
    "api_contracts": {
      "status": "skipped",
      "skipped_at": "<timestamp>",
      "reason": "User requested skip"
    }
  }
}
```

---

## Error Recovery

### Corrupted Progress File

If `prototype_progress.json` is corrupted:

```
ERROR: Progress file corrupted or invalid.

Options:
[R] Reset - Reinitialize progress tracking
[V] View - Attempt to display raw content
[A] Abort - Exit without changes
```

### Missing State Files

If state files are missing:

```
ERROR: State files incomplete.

Missing:
- _state/prototype_config.json
- _state/discovery_summary.json

Recommendation: Run /prototype-init to reinitialize.
```

---

## Examples

### Example 1: Resume After Failure

```
/prototype-resume InventorySystem

> Detecting resume point...
> Found: Phase 4 failed at 10:30:00
> Resuming from Phase 4: API Contracts
```

### Example 2: Resume Specific Prototype

```
/prototype-resume Prototype_WarehouseApp/

> Loading progress...
> Resume point: Phase 8 (Components)
```

### Example 3: Nothing to Resume

```
/prototype-resume

> All phases completed. Nothing to resume.
> Use /prototype-feedback to process changes.
```

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype` | Run full prototype |
| `/prototype-status` | Check current status |
| `/prototype-reset` | Reset progress |
