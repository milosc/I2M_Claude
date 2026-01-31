---
description: Validate ProductSpecs checkpoint requirements and P0 coverage
argument-hint: --checkpoint <N>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-validate started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-validate ended '{"stage": "productspecs"}'
---


# /productspecs-validate - Validate Sources

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs-validate instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for module/test ID management:

```bash
# Load Traceability rules (includes module ID format MOD-XXX-XXX-NN)
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Required: `<SystemName>`

## Prerequisites

- `/productspecs-init <SystemName>` completed (Checkpoint 0 passed)

## Skills Used

Read BEFORE execution:
- `.claude/skills/ProductSpecs_Validate/SKILL.md`

## Execution Steps

### Step 1: Load State

```bash
# Read config from shared _state/
cat _state/productspecs_config.json
```

Extract:
- `system_name`
- `prototype_path`
- `discovery_path`

### Step 2: Validate Discovery

Check `ClientAnalysis_<SystemName>/` has required outputs:

| File | Required |
|------|----------|
| `01-analysis/ANALYSIS_SUMMARY.md` | Yes |
| `01-analysis/PAIN_POINTS.md` | Yes |
| `02-research/personas/` | At least 1 persona |
| `02-research/JOBS_TO_BE_DONE.md` | Yes |
| `04-design-specs/screen-definitions.md` | Yes |
| `04-design-specs/data-fields.md` | Yes |

### Step 3: Validate Prototype

Check `Prototype_<SystemName>/` has required outputs:

| File | Required |
|------|----------|
| `_state/prototype_progress.json` | Yes |
| `_state/discovery_summary.json` | Yes |
| `_state/requirements_registry.json` | Yes |
| `traceability/screen_registry.json` | Yes |
| `00-foundation/data-model/DATA_MODEL_SUMMARY.md` | Yes |
| `00-foundation/api-contracts/API_CONTRACTS_SUMMARY.md` | Yes |
| `01-components/component-index.md` | Yes |
| `02-screens/screen-index.md` | Yes |

### Step 4: Check Prototype Progress

```python
# Prototype should have at least 12 phases complete
progress = json.load("_state/prototype_progress.json")
completed = count(p.status == "completed" for p in progress.phases)
if completed < 12:
    warn("Prototype only has {completed}/14 phases complete")
```

### Step 5: Load Registry Data

Load from `_state/`:
- `discovery_summary.json` - Personas, pain points, screens, entities
- `requirements_registry.json` - Requirements by type and priority
- `screen_registry.json` - Screen tracking

### Step 6: Calculate Readiness

| Check | Pass Criteria |
|-------|---------------|
| Discovery Complete | All required files exist |
| Prototype Complete | ≥12 phases completed |
| Personas Defined | At least 1 persona |
| Pain Points Defined | At least 1 pain point |
| Requirements Extracted | At least 1 requirement |
| Screens Defined | At least 1 screen |
| Data Model Defined | DATA_MODEL_SUMMARY.md exists |
| API Contracts Defined | API_CONTRACTS_SUMMARY.md exists |

**Readiness Score** = (Checks Passed / Total Checks) * 100%

### Step 7: Generate Report

Write `ProductSpecs_<SystemName>/00-overview/VALIDATION_REPORT.md`:

```markdown
# ProductSpecs Validation Report

**System**: <SystemName>
**Generated**: <TIMESTAMP>
**Status**: ✅ Ready | ❌ Not Ready

## Readiness Score: 100%

| Check | Status |
|-------|--------|
| Discovery Complete | ✅ |
| Prototype Complete | ✅ |
...

## Source Statistics

### Discovery
- Personas: 3
- Pain Points: 12
- JTBDs: 8
- Screens: 15

### Prototype
- Requirements: 45 (P0: 18, P1: 20, P2: 7)
- Components: 28
- API Endpoints: 12
```

### Step 8: Update Progress

Update `_state/productspecs_progress.json`:
- Set `phases.validate.status` = "completed"
- Set `phases.validate.completed_at` = current timestamp
- Set `phases.validate.outputs` = ["00-overview/VALIDATION_REPORT.md"]
- Set `current_phase` = 2

### Step 9: Validate Checkpoint

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 1 --dir ProductSpecs_<SystemName>/
```

### Step 10: Display Summary

**If Ready:**
```
═══════════════════════════════════════════════════════
  VALIDATION PASSED
═══════════════════════════════════════════════════════

  System:          <SystemName>
  Readiness:       100%

  Discovery:       ✅ Complete
  Prototype:       ✅ Complete (12/14 phases)

  Statistics:
  • Personas:      3
  • Pain Points:   12
  • Requirements:  45 (P0: 18)
  • Screens:       15

  Checkpoint 1:    ✅ PASSED

═══════════════════════════════════════════════════════

  Next Steps:
  • /productspecs-extract    - Extract requirements
  • /productspecs            - Run full generation

═══════════════════════════════════════════════════════
```

**If Not Ready:**
```
═══════════════════════════════════════════════════════
  VALIDATION FAILED
═══════════════════════════════════════════════════════

  System:          <SystemName>
  Readiness:       75%

  Missing:
  ❌ requirements_registry.json not found
  ❌ Prototype has only 8/14 phases complete

  Recommendations:
  1. Run /prototype-resume <SystemName>
  2. Ensure phases 0-12 complete
  3. Re-run /productspecs-validate

═══════════════════════════════════════════════════════
```

## Outputs

| File | Location |
|------|----------|
| `VALIDATION_REPORT.md` | `ProductSpecs_<SystemName>/00-overview/` |

## Error Handling

| Error | Action |
|-------|--------|
| Discovery missing | **BLOCK** - Show error |
| Prototype missing | **BLOCK** - Show error |
| State files missing | **BLOCK** - Run /productspecs-init first |

## Related Commands

| Command | Description |
|---------|-------------|
| `/productspecs-init` | Initialize first |
| `/productspecs-extract` | Next phase |
| `/productspecs` | Full generation |
