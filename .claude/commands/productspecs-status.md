---
name: productspecs-status
description: Display ProductSpecs generation status and progress
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-status started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-status ended '{"stage": "productspecs"}'
---


# /productspecs-status - Show ProductSpecs Progress

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs-status instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for module/test ID management:

```bash
# Load Traceability rules (includes module ID format MOD-XXX-XXX-NN)
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` or path to `ProductSpecs_<SystemName>/`
  - If not provided, auto-detects from current directory

## Execution Steps

### Step 1: Locate ProductSpecs Folder

```
If $ARGUMENTS provided:
  - Use as SystemName or path
Else:
  - Look for ProductSpecs_*/ in current directory
  - If multiple found, list them and exit
  - If none found, show error
```

### Step 2: Load State Files

Read from `_state/` (at project ROOT):
- `productspecs_config.json`
- `productspecs_progress.json`

### Step 3: Calculate Progress

```python
completed_phases = count(phase.status == "completed")
total_phases = 9  # 0-8
progress_percent = (completed_phases / total_phases) * 100
```

### Step 4: Load Coverage Stats

From `ProductSpecs_<SystemName>/_registry/`:
- `modules.json` - Module count
- `requirements.json` - Requirements breakdown
- `traceability.json` - Chain coverage

### Step 5: Display Progress

```
═══════════════════════════════════════════════════════
  PRODUCTSPECS STATUS: <SystemName>
═══════════════════════════════════════════════════════

  Overall Progress
  ────────────────────────────────────────────────────
  [████████████░░░░░░░░] 60%  (6/9 phases)

  Sources
  ────────────────────────────────────────────────────
  Discovery:   ClientAnalysis_<SystemName>/  ✅
  Prototype:   Prototype_<SystemName>/       ✅

  Phase Status
  ────────────────────────────────────────────────────
  │ Phase │ Name              │ Status      │
  │───────│───────────────────│─────────────│
  │ 0     │ Initialize        │ ✅ Complete │
  │ 1     │ Validate Sources  │ ✅ Complete │
  │ 2     │ Extract Reqs      │ ✅ Complete │
  │ 3     │ Modules Core      │ ✅ Complete │
  │ 4     │ Modules Extended  │ ✅ Complete │
  │ 5     │ API Contracts     │ ✅ Complete │
  │ 6     │ Test Specs        │ 🔄 In Progress │
  │ 7     │ Traceability      │ ⏳ Pending  │
  │ 8     │ Export            │ ⏳ Pending  │

  Coverage Metrics
  ────────────────────────────────────────────────────
  Modules:        12 generated
  Requirements:   45 (P0: 18, P1: 20, P2: 7)
  Test Cases:     72 defined
  P0 Traced:      100% (18/18)

  Recent Activity
  ────────────────────────────────────────────────────
  Last Updated:   2025-12-22 14:30:00
  Current Phase:  6 - Test Specifications
  Duration:       2h 15m

═══════════════════════════════════════════════════════

  Next Actions:
  • /productspecs-resume   - Continue from current phase
  • /productspecs-tests    - Complete test specifications

═══════════════════════════════════════════════════════
```

### Step 6: Show Failures (if any)

If `_state/FAILURES_LOG.md` has entries:

```
  Failures (3 items skipped)
  ────────────────────────────────────────────────────
  • Phase 3: MOD-INV-LEGACY - Source file missing
  • Phase 5: API-INT-003 - Endpoint undefined
  • Phase 6: TC-E2E-BATCH - Scenario incomplete

  See _state/FAILURES_LOG.md for details
```

## Output Format

### Compact Mode (`--compact`)

```
ProductSpecs_<SystemName>: 60% complete (6/9 phases)
  Current: Phase 6 - Test Specifications
  Modules: 12 | Requirements: 45 | Test Cases: 72
  Next: /productspecs-resume
```

### JSON Mode (`--json`)

```json
{
  "system_name": "<SystemName>",
  "progress_percent": 60,
  "phases_completed": 6,
  "phases_total": 9,
  "current_phase": 6,
  "current_phase_name": "tests",
  "coverage": {
    "modules": 12,
    "requirements": 45,
    "test_cases": 72,
    "p0_traced_percent": 100
  },
  "last_updated": "2025-12-22T14:30:00",
  "failures_count": 3
}
```

## Error Handling

| Error | Action |
|-------|--------|
| No ProductSpecs folder found | Show instructions to run `/productspecs-init` |
| State files missing | Show warning, display partial info |
| Multiple folders found | List all and ask user to specify |

## Related Commands

| Command | Description |
|---------|-------------|
| `/productspecs` | Run full generation |
| `/productspecs-resume` | Continue from last checkpoint |
| `/productspecs-reset` | Reset state |
