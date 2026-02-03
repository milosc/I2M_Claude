---
name: productspecs-resume
description: Resume ProductSpecs generation from last completed checkpoint
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-resume started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-resume ended '{"stage": "productspecs"}'
---


# /productspecs-resume - Resume ProductSpecs Generation

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs-resume instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for module/test ID management:

```bash
# Load Traceability rules (includes module ID format MOD-XXX-XXX-NN)
/rules-traceability
```

## Description

This command reads the progress state and resumes generation from where it left off. Use this when:
- Generation was interrupted
- A session ended before completion
- You need to continue after fixing a blocking error

## Arguments

- `$ARGUMENTS` - Optional: `[SystemName] [--from-checkpoint N]`

## Options

| Option | Description |
|--------|-------------|
| `--from-checkpoint N` | Force resume from specific checkpoint |
| `--validate-only` | Just validate current state, don't execute |
| `--skip-validation` | Skip checkpoint validation (use with caution) |

## Execution Steps

### Step 1: Detect Active ProductSpecs Session

```python
# Check for existing progress file
progress_file = "_state/productspecs_progress.json"

if not exists(progress_file):
    print("No active ProductSpecs session found.")
    print("Run /productspecs <SystemName> to start a new session.")
    exit(1)

progress = json.load(progress_file)
system_name = progress.get("system_name")
current_phase = progress.get("current_phase", 0)
```

### Step 2: Display Current State

```
═══════════════════════════════════════════════════════════════
  PRODUCTSPECS RESUME
═══════════════════════════════════════════════════════════════

  System:           InventorySystem
  Last Activity:    2024-01-15 14:30:00
  Current Phase:    4 (Modules Extended)
  Next Checkpoint:  5

  Phase Status:
  ──────────────────────────────────────────────────────────────
  │ Phase               │ Status     │ Completed At          │
  │─────────────────────│────────────│───────────────────────│
  │ 0: Initialize       │ ✅ Complete │ 2024-01-15 13:00:00   │
  │ 1: Validate         │ ✅ Complete │ 2024-01-15 13:05:00   │
  │ 2: Extract          │ ✅ Complete │ 2024-01-15 13:15:00   │
  │ 3: Modules Core     │ ✅ Complete │ 2024-01-15 13:45:00   │
  │ 4: Modules Extended │ ▶ Running  │ -                     │
  │ 5: Contracts        │ ⬜ Pending │ -                     │
  │ 6: Tests            │ ⬜ Pending │ -                     │
  │ 7: Traceability     │ ⬜ Pending │ -                     │
  │ 8: Export           │ ⬜ Pending │ -                     │

═══════════════════════════════════════════════════════════════
```

### Step 3: Validate Last Checkpoint

```bash
# Validate the last completed checkpoint
last_completed = get_last_completed_phase(progress)
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint {last_completed} --dir ProductSpecs_{system_name}/
```

If validation fails:
```
⚠️  Warning: Checkpoint {last_completed} validation failed.

Reason: Missing file: 01-modules/module-index.md

Options:
1. Run /productspecs-reset --phase {last_completed} to reset and re-run
2. Use --skip-validation to continue anyway (not recommended)
3. Fix the issue manually and retry
```

### Step 4: Determine Resume Point

```python
def get_resume_phase(progress, args):
    if args.from_checkpoint is not None:
        return args.from_checkpoint

    # Find first incomplete phase
    phases = progress["phases"]
    for phase_name, phase_data in phases.items():
        if phase_data["status"] in ["pending", "in_progress"]:
            return phase_data["phase_number"]

    # All complete
    return None

resume_from = get_resume_phase(progress, args)

if resume_from is None:
    print("All phases complete! Nothing to resume.")
    print("Run /productspecs-status to view final state.")
    exit(0)
```

### Step 5: Execute Remaining Phases

```python
# Map phase numbers to commands
PHASE_COMMANDS = {
    0: "/productspecs-init",
    1: "/productspecs-validate",
    2: "/productspecs-extract",
    3: "/productspecs-modules",  # Handles 3-4
    4: "/productspecs-modules",  # Skip if 3 ran
    5: "/productspecs-contracts",
    6: "/productspecs-tests",
    7: "/productspecs-finalize",
    8: "/productspecs-export"
}

# Execute from resume point
for phase in range(resume_from, 9):
    if phase == 4 and progress["phases"]["modules_core"]["status"] == "completed":
        continue  # modules command handles both 3-4

    command = PHASE_COMMANDS[phase]
    print(f"Executing: {command} {system_name}")
    execute_command(command, system_name)

    # Validate checkpoint
    validate_checkpoint(phase, system_name)
```

### Step 6: Update Progress

```python
# Progress is updated by each phase command
# Resume just orchestrates the execution
```

## Examples

### Basic Resume

```bash
# Resume from last checkpoint automatically
/productspecs-resume
```

### Resume Specific System

```bash
# Resume with explicit system name
/productspecs-resume InventorySystem
```

### Resume from Specific Checkpoint

```bash
# Force resume from checkpoint 5
/productspecs-resume InventorySystem --from-checkpoint 5
```

### Validate Only

```bash
# Just check current state without executing
/productspecs-resume --validate-only
```

### Skip Validation

```bash
# Resume without checkpoint validation (use with caution)
/productspecs-resume --skip-validation
```

## Phase Recovery Strategies

### Phase 0-1 Failures (Initialize/Validate)

```bash
# Reset completely and start fresh
/productspecs-reset --hard
/productspecs <SystemName>
```

### Phase 2 Failures (Extract)

```bash
# Reset to phase 2 and re-extract
/productspecs-reset --phase 2
/productspecs-resume
```

### Phase 3-4 Failures (Modules)

```bash
# Reset to phase 3 and regenerate modules
/productspecs-reset --phase 3
/productspecs-resume
```

### Phase 5-6 Failures (Contracts/Tests)

```bash
# These phases are additive - often can just resume
/productspecs-resume --from-checkpoint 5
```

### Phase 7 Failures (Traceability)

```bash
# Usually means P0 gaps - fix gaps first
/productspecs-status  # See what's missing
# Fix the gaps manually or re-run previous phases
/productspecs-resume --from-checkpoint 7
```

### Phase 8 Failures (Export)

```bash
# JIRA export is isolated - can retry safely
/productspecs-resume --from-checkpoint 8
# Or just regenerate JIRA files
/productspecs-jira <SystemName> --reconfigure
```

## Progress File Structure

`_state/productspecs_progress.json`:

```json
{
  "schema_version": "1.0.0",
  "system_name": "InventorySystem",
  "current_phase": 4,
  "current_checkpoint": "productspecs-modules",
  "started_at": "2024-01-15T13:00:00Z",
  "updated_at": "2024-01-15T14:30:00Z",
  "phases": {
    "init": {
      "status": "completed",
      "phase_number": 0,
      "completed_at": "2024-01-15T13:00:00Z",
      "outputs": ["folder structure", "config.json"]
    },
    "validate": {
      "status": "completed",
      "phase_number": 1,
      "completed_at": "2024-01-15T13:05:00Z",
      "outputs": ["validation_report.md"]
    },
    "extract": {
      "status": "completed",
      "phase_number": 2,
      "completed_at": "2024-01-15T13:15:00Z",
      "outputs": ["requirements.json"]
    },
    "modules_core": {
      "status": "completed",
      "phase_number": 3,
      "completed_at": "2024-01-15T13:45:00Z",
      "outputs": ["module-index.md"]
    },
    "modules_extended": {
      "status": "in_progress",
      "phase_number": 4,
      "started_at": "2024-01-15T13:46:00Z",
      "outputs": []
    },
    "contracts": {
      "status": "pending",
      "phase_number": 5
    },
    "tests": {
      "status": "pending",
      "phase_number": 6
    },
    "traceability": {
      "status": "pending",
      "phase_number": 7
    },
    "export": {
      "status": "pending",
      "phase_number": 8
    }
  },
  "validation_history": [
    {"checkpoint": 0, "passed": true, "timestamp": "..."},
    {"checkpoint": 1, "passed": true, "timestamp": "..."},
    {"checkpoint": 2, "passed": true, "timestamp": "..."},
    {"checkpoint": 3, "passed": true, "timestamp": "..."}
  ]
}
```

## Error Handling

| Error | Action |
|-------|--------|
| No progress file | Instruct to run /productspecs first |
| Checkpoint validation fails | Show fix instructions |
| Phase command fails | Log error, stop |
| All phases complete | Show completion message |

## Related Commands

| Command | Description |
|---------|-------------|
| `/productspecs` | Start new generation |
| `/productspecs-status` | View current progress |
| `/productspecs-reset` | Reset state |
| `/productspecs-reset --phase N` | Reset to specific phase |
