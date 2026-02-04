---
name: solarch-validate
description: Validate Solution Architecture checkpoint requirements and coverage
argument-hint: --checkpoint <N>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-validate started '{"stage": "solarch"}'
  Stop:
    - hooks:
        # VALIDATION: Comprehensive SolArch validation
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_solarch_output.py"
            --system-name "$(cat _state/session.json 2>/dev/null | grep -o '"project"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"project"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//')"
            --phase validate
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-validate ended '{"stage": "solarch", "validated": true}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-validate instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

This command validates that all required inputs from upstream stages are available and complete. This is Checkpoint 1 of the pipeline and is **BLOCKING** - generation cannot proceed without passing this checkpoint.

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` (auto-detected from config if not provided)

## Usage

```bash
/solarch-validate InventorySystem
```

## Prerequisites

- Checkpoint 0 passed (`/solarch-init` completed)
- `Prototype_<SystemName>/` exists with Checkpoint 14 passed
- `ProductSpecs_<SystemName>/` exists with Checkpoint 8 passed

## Skills Used

None required - this performs validation checks.

## Execution Steps

### Step 1: Execute

```
LOAD _state/solarch_config.json
SYSTEM_NAME = config.system_name OR $ARGUMENTS[0]

SET paths:
  PROTOTYPE_PATH = config.prototype_path
  PRODUCTSPECS_PATH = config.productspecs_path

VALIDATE ProductSpecs:
  CHECK ProductSpecs_X/ exists
  CHECK _state/productspecs_progress.json exists
  READ progress → current_checkpoint >= 8

  IF checkpoint < 8:
    ERROR: "ProductSpecs not complete (checkpoint {checkpoint}, required: 8)"
    BLOCK: true

  EXTRACT from ProductSpecs:
    - modules.json → module list
    - requirements.json → requirements
    - traceability.json → chains
    - NFR_SPECIFICATIONS.md → NFRs

VALIDATE Prototype:
  CHECK Prototype_X/ exists
  CHECK _state/prototype_progress.json exists
  READ progress → current_checkpoint >= 14

  IF checkpoint < 14:
    ERROR: "Prototype not complete (checkpoint {checkpoint}, required: 14)"
    BLOCK: true

  EXTRACT from Prototype:
    - discovery_summary.json → personas, pain points
    - screen_registry.json → screens
    - design-tokens.json → design system

VALIDATE Traceability:
  LOAD traceability/discovery_traceability_register.json
  LOAD traceability/prototype_traceability_register.json

  VERIFY chains exist and are complete

CREATE _state/solarch_input_validation.json:
  {
    "$schema": "solarch-input-validation-v1",
    "$metadata": {
      "created_at": "ISO8601",
      "validated_at": "ISO8601"
    },
    "productspecs_valid": true/false,
    "productspecs_checkpoint": N,
    "productspecs_modules": [...],
    "productspecs_requirements_count": N,
    "prototype_valid": true/false,
    "prototype_checkpoint": N,
    "prototype_screens_count": N,
    "discovery_personas": [...],
    "discovery_pain_points": [...],
    "validation_passed": true/false,
    "validation_errors": [...]
  }

UPDATE _state/solarch_progress.json:
  phases.validate.status = "completed"
  phases.validate.completed_at = NOW()
  current_checkpoint = 1

RUN quality gate:
  python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 1 --dir {OUTPUT_PATH}/

IF validation fails:
  DISPLAY blocking error
  STOP execution

DISPLAY checkpoint 1 summary
```

### Step 2: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-validate" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Validation Checks

### ProductSpecs Validation

| Check | Requirement | Blocking |
|-------|-------------|----------|
| Folder exists | `ProductSpecs_<SystemName>/` | YES |
| Progress file | `_state/productspecs_progress.json` | YES |
| Checkpoint | >= 8 | YES |
| Modules registry | `_registry/modules.json` with items | YES |
| Requirements | `_registry/requirements.json` with items | YES |
| Traceability | `_registry/traceability.json` | YES |

### Prototype Validation

| Check | Requirement | Blocking |
|-------|-------------|----------|
| Folder exists | `Prototype_<SystemName>/` | YES |
| Progress file | `_state/prototype_progress.json` | YES |
| Checkpoint | >= 14 | YES |
| Screens | `traceability/screen_registry.json` | YES |
| Discovery summary | `_state/discovery_summary.json` | YES |

### Data Extraction

From ProductSpecs:
- Module specifications (MOD-*.md)
- Requirements hierarchy
- NFR specifications
- Test specifications

From Prototype:
- Personas and pain points
- Screen definitions
- Design tokens
- API contracts

## Output Format

### Success

```
═══════════════════════════════════════════════════════════════
 CHECKPOINT 1: VALIDATE INPUTS - PASSED [BLOCKING]
═══════════════════════════════════════════════════════════════

ProductSpecs Validation:
├─ Folder: ProductSpecs_InventorySystem/ ✅
├─ Checkpoint: 8/8 ✅
├─ Modules: 5 found ✅
├─ Requirements: 26 found ✅
└─ NFRs: 12 found ✅

Prototype Validation:
├─ Folder: Prototype_InventorySystem/ ✅
├─ Checkpoint: 14/14 ✅
├─ Screens: 15 found ✅
└─ Components: 42 found ✅

Discovery Data:
├─ Personas: 4 found ✅
├─ Pain Points: 10 found ✅
└─ JTBDs: 8 found ✅

Traceability Chains: 10 complete ✅

Quality Gate: ✅ PASSED

Next: /solarch-context InventorySystem
═══════════════════════════════════════════════════════════════
```

### Failure (Blocking)

```
═══════════════════════════════════════════════════════════════
 CHECKPOINT 1: VALIDATE INPUTS - FAILED [BLOCKING]
═══════════════════════════════════════════════════════════════

ProductSpecs Validation:
├─ Folder: ProductSpecs_InventorySystem/ ✅
├─ Checkpoint: 6/8 ❌ (required: 8)
└─ ERROR: ProductSpecs incomplete

[BLOCKING] Cannot proceed until ProductSpecs reaches Checkpoint 8.

To fix:
1. Complete ProductSpecs generation: /productspecs InventorySystem
2. Re-run validation: /solarch-validate InventorySystem

═══════════════════════════════════════════════════════════════
```

## Checkpoint Validation

```bash
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 1 --dir SolArch_InventorySystem/
```

**Required for Checkpoint 1:**
- `_state/solarch_input_validation.json` exists
- `productspecs_valid: true`
- `prototype_valid: true`

## Error Handling

| Error | Action |
|-------|--------|
| ProductSpecs incomplete | BLOCK, show fix instructions |
| Prototype incomplete | BLOCK, show fix instructions |
| Missing registry files | BLOCK, show which files needed |
| Missing traceability | BLOCK, suggest regeneration |

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch-init` | Previous phase (Checkpoint 0) |
| `/solarch-context` | Next phase (Checkpoint 2) |
| `/productspecs` | Complete ProductSpecs if needed |
| `/prototype` | Complete Prototype if needed |
