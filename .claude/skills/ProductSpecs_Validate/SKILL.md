---
name: validating-productspecs-inputs
description: Use when you need to validate that Discovery and Prototype outputs are complete and ready for ProductSpecs generation.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-productspecs-inputs started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-productspecs-inputs ended '{"stage": "productspecs"}'
---

# ProductSpecs_Validate

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill validating-productspecs-inputs instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

**Purpose**: Validate that Discovery and Prototype outputs are complete and ready for ProductSpecs generation.

**Version**: 1.0.0
**Created**: 2025-12-22
**Phase**: 1 of ProductSpecs pipeline

---

## Overview

This skill validates the upstream inputs (Discovery and Prototype) before ProductSpecs generation begins. It ensures:
- Discovery outputs are complete
- Prototype outputs are sufficient
- All required traceability data is available
- Screen and requirement registries are populated

---

## Prerequisites

### Required State Files

Location: `_state/` (at PROJECT ROOT)

| File | Purpose |
|------|---------|
| `productspecs_config.json` | ProductSpecs configuration |
| `discovery_summary.json` | Discovery extraction (from Prototype) |
| `screen_registry.json` | Screen tracking |
| `requirements_registry.json` | Requirements registry |

### Required Source Folders

| Folder | Required Files |
|--------|----------------|
| `ClientAnalysis_<SystemName>/` | Discovery outputs |
| `Prototype_<SystemName>/` | Prototype outputs |

---

## Execution Flow

### Phase 1.1: Load Configuration

```python
# Read ProductSpecs config from shared _state/
config_path = "_state/productspecs_config.json"
config = json.load(config_path)

system_name = config["system_name"]
prototype_path = config["prototype_path"]
discovery_path = config["discovery_path"]
```

### Phase 1.2: Validate Discovery Completeness

Check `ClientAnalysis_<SystemName>/` has required outputs:

**Required Files**:

| File | Purpose | Required |
|------|---------|----------|
| `01-analysis/ANALYSIS_SUMMARY.md` | Analysis outputs | Yes |
| `01-analysis/PAIN_POINTS.md` | User pain points | Yes |
| `02-research/personas/` | At least 1 persona | Yes |
| `02-research/JOBS_TO_BE_DONE.md` | JTBD statements | Yes |
| `04-design-specs/screen-definitions.md` | Screen specs | Yes |
| `04-design-specs/data-fields.md` | Data fields | Yes |

**Validation Output**:

```python
discovery_validation = {
    "status": "pass" | "fail",
    "files_found": [...],
    "files_missing": [...],
    "personas_count": int,
    "screens_count": int,
    "pain_points_count": int
}
```

### Phase 1.3: Validate Prototype Completeness

Check `Prototype_<SystemName>/` has required outputs:

**Required Files**:

| File | Purpose | Required |
|------|---------|----------|
| `_state/prototype_progress.json` | Prototype state | Yes |
| `_state/discovery_summary.json` | Discovery extraction | Yes |
| `_state/requirements_registry.json` | Requirements | Yes |
| `traceability/screen_registry.json` | Screen tracking | Yes |
| `00-foundation/data-model/DATA_MODEL_SUMMARY.md` | Data model | Yes |
| `00-foundation/api-contracts/API_CONTRACTS_SUMMARY.md` | API contracts | Yes |
| `01-components/component-index.md` | Components | Yes |
| `02-screens/screen-index.md` | Screens | Yes |

**Check Prototype Progress**:

```python
# Prototype should have at least phases 0-12 complete
progress_path = "_state/prototype_progress.json"
progress = json.load(progress_path)

completed_phases = sum(
    1 for p in progress["phases"].values()
    if p["status"] == "completed"
)

# Minimum: 12 phases completed (Init through CodeGen)
if completed_phases < 12:
    log_warning(f"Prototype only has {completed_phases}/14 phases complete")
```

### Phase 1.4: Load and Validate Registries

#### Load Discovery Summary

```python
# From shared _state/
discovery_summary_path = "_state/discovery_summary.json"
discovery_summary = json.load(discovery_summary_path)

# Extract key counts
personas = discovery_summary.get("personas", [])
pain_points = discovery_summary.get("pain_points", [])
screens = discovery_summary.get("screens", [])
entities = discovery_summary.get("entities", [])
workflows = discovery_summary.get("workflows", [])
```

#### Load Requirements Registry

```python
# From shared _state/
requirements_path = "_state/requirements_registry.json"
requirements = json.load(requirements_path)

# Count by priority
p0_count = sum(1 for r in requirements["requirements"] if r.get("priority") == "P0")
p1_count = sum(1 for r in requirements["requirements"] if r.get("priority") == "P1")
p2_count = sum(1 for r in requirements["requirements"] if r.get("priority") == "P2")
```

#### Load Screen Registry

```python
# From shared _state/
screen_registry_path = "traceability/screen_registry.json"
screen_registry = json.load(screen_registry_path)

discovery_screens = screen_registry.get("discovery_screens", [])
screen_coverage = screen_registry.get("screen_coverage", {})
```

### Phase 1.5: Calculate Readiness Score

```python
readiness = {
    "discovery_complete": discovery_validation["status"] == "pass",
    "prototype_complete": completed_phases >= 12,
    "personas_defined": len(personas) > 0,
    "pain_points_defined": len(pain_points) > 0,
    "requirements_extracted": len(requirements["requirements"]) > 0,
    "screens_defined": len(discovery_screens) > 0,
    "data_model_defined": data_model_exists,
    "api_contracts_defined": api_contracts_exist
}

# Calculate score
score = sum(readiness.values()) / len(readiness) * 100
status = "ready" if score == 100 else "not_ready"
```

### Phase 1.6: Generate Validation Report

Write validation report to `ProductSpecs_<SystemName>/00-overview/VALIDATION_REPORT.md`:

```markdown
# ProductSpecs Validation Report

**System**: <SystemName>
**Generated**: <TIMESTAMP>
**Status**: ✅ Ready for Generation | ❌ Not Ready

---

## Readiness Score: 100%

| Check | Status |
|-------|--------|
| Discovery Complete | ✅ |
| Prototype Complete | ✅ |
| Personas Defined | ✅ (3 personas) |
| Pain Points Defined | ✅ (12 pain points) |
| Requirements Extracted | ✅ (45 requirements) |
| Screens Defined | ✅ (15 screens) |
| Data Model Defined | ✅ |
| API Contracts Defined | ✅ |

---

## Source Statistics

### Discovery

| Metric | Count |
|--------|-------|
| Personas | 3 |
| Pain Points | 12 |
| JTBDs | 8 |
| Screens | 15 |

### Prototype

| Metric | Count |
|--------|-------|
| Requirements | 45 |
| Components | 28 |
| API Endpoints | 12 |
| Test Data Files | 6 |

---

## Requirements Breakdown

| Priority | Count | Percentage |
|----------|-------|------------|
| P0 (Must Have) | 18 | 40% |
| P1 (Should Have) | 20 | 44% |
| P2 (Nice to Have) | 7 | 16% |

---

## Screen Coverage

| App | Screens | Priority |
|-----|---------|----------|
| Mobile | 10 | P0: 8, P1: 2 |
| Desktop | 5 | P0: 3, P1: 2 |

---

## Recommendations

1. ✅ Ready for ProductSpecs generation
2. Consider reviewing 7 P2 requirements for scope
3. 2 screens have incomplete acceptance criteria
```

### Phase 1.7: Update State Files

#### Update `_state/productspecs_progress.json`

```json
{
  "phases": {
    "validate": {
      "status": "completed",
      "completed_at": "<TIMESTAMP>",
      "outputs": [
        "00-overview/VALIDATION_REPORT.md"
      ]
    }
  },
  "current_phase": 2
}
```

#### Update `traceability/program_registry.json` (ROOT level - single source of truth)

```json
{
  "$metadata": {
    "updated_at": "<TIMESTAMP>"
  },
  "statistics": {
    "total_screens": 15,
    "total_requirements": 45,
    "p0_requirements": 18,
    "p1_requirements": 20,
    "p2_requirements": 7
  }
}
```

### Phase 1.8: Validate Checkpoint 1

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 1 --dir ProductSpecs_<SystemName>/
```

---

## Outputs

| File | Location | Purpose |
|------|----------|---------|
| `VALIDATION_REPORT.md` | `ProductSpecs_<SystemName>/00-overview/` | Human-readable report |
| `program_registry.json` | `traceability/` (ROOT) | Updated statistics (single source of truth) |
| `productspecs_progress.json` | `_state/` | Phase status |

---

## Error Handling

| Error | Action |
|-------|--------|
| Discovery folder missing | **BLOCK** - Cannot proceed |
| Prototype folder missing | **BLOCK** - Cannot proceed |
| Missing registry files | **BLOCK** - Run Prototype first |
| Incomplete Prototype | **WARN** - Log and continue |

---

## Traceability

This skill links:
- **Upstream**: Discovery outputs, Prototype outputs
- **Downstream**: All ProductSpecs generation phases

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `ProductSpecs_ExtractRequirements` | Next phase - extract requirements |
| `Prototype_ValidateDiscovery` | Similar validation in Prototype |
