---
name: prototype-status
description: Display Prototype generation status and progress
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-status started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-status ended '{"stage": "prototype"}'
---


# /prototype-status - Show Prototype Progress

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-status instruction_start '{"stage": "prototype", "method": "instruction-based"}'
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
  - If not provided: Auto-detect from current directory or list available

## Execution Steps

### Step 1: Locate Prototype

```
If $ARGUMENTS provided:
  - Use Prototype_<SystemName>/ or provided path
Else:
  - List all Prototype_*/ folders
  - If one found: Use it
  - If multiple: Ask user to specify
  - If none: Display "No prototype found"
```

### Step 2: Read State Files

Read the following files:

1. `_state/prototype_config.json` - Configuration
2. `_state/prototype_progress.json` - Phase progress
3. `_state/FAILURES_LOG.md` - Failures count

### Step 3: Calculate Statistics

```python
# Phase counts
completed = count phases where status == "completed"
in_progress = count phases where status == "in_progress"
pending = count phases where status == "pending"
failed = count phases where status == "failed"

# Checkpoint status
last_checkpoint = max(validation_history.checkpoint where result == "pass")

# Duration
started = prototype_progress.started_at
elapsed = now - started
```

### Step 4: Read Traceability (if exists)

Read `traceability/prototype_traceability_register.json`:
- Pain points addressed
- Coverage percentage

### Step 5: Display Status

```
═══════════════════════════════════════════════════════
  PROTOTYPE STATUS
═══════════════════════════════════════════════════════

  System:              <SystemName>
  Discovery Source:    ClientAnalysis_<SystemName>/
  Output:              Prototype_<SystemName>/

  Started:             <YYYY-MM-DD HH:MM:SS>
  Elapsed:             <duration>
  Last Updated:        <YYYY-MM-DD HH:MM:SS>

───────────────────────────────────────────────────────
  PHASE PROGRESS
───────────────────────────────────────────────────────

  Phase 0:  Initialize           ✅ Completed
  Phase 1:  Validate Discovery   ✅ Completed
  Phase 2:  Requirements         ✅ Completed
  Phase 3:  Data Model           ✅ Completed
  Phase 4:  API Contracts        🔄 In Progress  ← CURRENT
  Phase 5:  Test Data            ⏳ Pending
  Phase 6:  Design Brief         ⏳ Pending
  Phase 7:  Design Tokens        ⏳ Pending
  Phase 8:  Components           ⏳ Pending
  Phase 9:  Screens              ⏳ Pending
  Phase 10: Interactions         ⏳ Pending
  Phase 11: Sequencer            ⏳ Pending
  Phase 12: Code Generation      ⏳ Pending
  Phase 13: QA Testing           ⏳ Pending
  Phase 14: UI Audit             ⏳ Pending

  Progress: ████████░░░░░░░░░░░░ 4/14 phases (28%)

───────────────────────────────────────────────────────
  CHECKPOINTS
───────────────────────────────────────────────────────

  Last Passed:         Checkpoint 3 (Data Model)
  Next Required:       Checkpoint 4 (API Contracts)

───────────────────────────────────────────────────────
  TRACEABILITY
───────────────────────────────────────────────────────

  Pain Points:         12/15 addressed (80%)
  Requirements:        24 linked
  Components:          8 specified
  Screens:             5 specified
  Test Cases:          0 defined

───────────────────────────────────────────────────────
  FAILURES
───────────────────────────────────────────────────────

  Skipped Items:       3

  Recent:
  • Phase 1: interview_3.md - File read error
  • Phase 3: entity_legacy.md - Schema validation failed
  • Phase 5: test_edge_case.json - Generation failed

═══════════════════════════════════════════════════════

  Commands:
  • /prototype-resume            - Continue from Phase 4
  • /prototype-feedback          - Process change request
  • /prototype-reset             - Reset progress

═══════════════════════════════════════════════════════
```

### Phase Status Icons

| Status | Icon | Meaning |
|--------|------|---------|
| completed | ✅ | Phase finished successfully |
| in_progress | 🔄 | Currently executing |
| pending | ⏳ | Not yet started |
| failed | ❌ | Failed (needs intervention) |

### Detailed View (--verbose)

If `--verbose` flag is passed, also show:

```
───────────────────────────────────────────────────────
  PHASE DETAILS
───────────────────────────────────────────────────────

  Phase 3: Data Model
  ├── Status:      ✅ Completed
  ├── Started:     2024-01-15 10:30:00
  ├── Completed:   2024-01-15 10:45:00
  ├── Duration:    15 minutes
  └── Outputs:
      • 04-implementation/data-model.md

  Phase 4: API Contracts
  ├── Status:      🔄 In Progress
  ├── Started:     2024-01-15 10:45:00
  └── Outputs:     (none yet)
```

### JSON Output (--json)

If `--json` flag is passed, output raw JSON:

```json
{
  "system_name": "<SystemName>",
  "status": "in_progress",
  "current_phase": 4,
  "last_checkpoint": 3,
  "progress": {
    "completed": 4,
    "in_progress": 1,
    "pending": 10,
    "failed": 0,
    "total": 15,
    "percent": 28
  },
  "traceability": {
    "pain_points_addressed": 12,
    "pain_points_total": 15,
    "coverage_percent": 80
  },
  "failures_count": 3
}
```

## Error Handling

| Error | Action |
|-------|--------|
| No Prototype folder found | Display "No prototype found. Run /prototype-init first." |
| State files missing | Display partial status with warnings |
| JSON parse error | Display error, suggest /prototype-reset |

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype` | Run full prototype generation |
| `/prototype-resume` | Resume from current phase |
| `/prototype-reset` | Reset progress |
