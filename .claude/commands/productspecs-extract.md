---
description: Extract module specifications from prototype
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-extract started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-extract ended '{"stage": "productspecs"}'
---


# /productspecs-extract - Extract Requirements

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs-extract instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
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

- `/productspecs-validate <SystemName>` completed (Checkpoint 1 passed)

## Skills Used

Read BEFORE execution:
- `.claude/skills/ProductSpecs_ExtractRequirements/SKILL.md`

## Execution Steps

### Step 1: Verify Checkpoint 1

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 1 --dir ProductSpecs_<SystemName>/
```

If not passed, show error and exit.

### Step 2: Load Source Data

Load from `_state/` (at project ROOT):

```python
discovery_summary = json.load("_state/discovery_summary.json")
requirements_registry = json.load("_state/requirements_registry.json")
screen_registry = json.load("traceability/screen_registry.json")
```

Extract:
- `pain_points` - List of pain point objects
- `jtbds` - List of JTBD objects
- `personas` - List of persona objects
- `screens` - List of screen definitions
- `requirements` - List of requirements

### Step 3: Build Indexes

Create lookup tables for efficient traceability:

```python
# Pain point index: PP-X.X -> object
pain_point_index = {pp["id"]: pp for pp in pain_points}

# JTBD index: JTBD-X.X -> object
jtbd_index = {jtbd["id"]: jtbd for jtbd in jtbds}

# Screen index: M-XX or D-XX -> object
screen_index = {s["id"]: s for s in screens}
```

### Step 4: Enrich Requirements

For each requirement, add complete traceability:

| Field | Source |
|-------|--------|
| `id` | From requirements_registry |
| `type` | user_story, functional, non_functional, accessibility |
| `priority` | P0, P1, P2 |
| `title` | From requirements_registry |
| `description` | From requirements_registry |
| `acceptance_criteria` | Gherkin scenarios |
| `pain_point_refs` | Links to PP-X.X |
| `jtbd_refs` | Links to JTBD-X.X |
| `screen_refs` | Links to M-XX, D-XX |
| `persona_refs` | Links to PERSONA_* |
| `pain_points` | Full pain point objects |
| `jtbds` | Full JTBD objects |
| `traceability_complete` | Boolean |
| `missing_links` | Array of missing link types |

### Step 5: Group Requirements

Group by multiple dimensions:

```python
by_priority = {
    "P0": [...],  # Must have
    "P1": [...],  # Should have
    "P2": [...]   # Nice to have
}

by_type = {
    "user_story": [...],
    "functional": [...],
    "non_functional": [...],
    "accessibility": [...]
}

by_screen = {
    "M-01": ["REQ-001", "REQ-010"],
    "M-02": ["REQ-002", "REQ-011"],
    ...
}
```

### Step 6: Calculate Statistics

```python
statistics = {
    "total": len(requirements),
    "by_priority": {"P0": 18, "P1": 20, "P2": 7},
    "by_type": {"user_story": 25, "functional": 15, ...},
    "traceability": {
        "complete": 40,
        "incomplete": 5,
        "p0_complete": 18  # All P0 should be complete
    }
}
```

### Step 7: Build Traceability Chains

Create chains linking pain points to requirements:

```python
chains = []
for pp in pain_points:
    chain = {
        "chain_id": f"CHAIN-{pp['id']}",
        "pain_point": pp["id"],
        "jtbd": find_jtbd_for_pain_point(pp["id"]),
        "requirements": find_requirements_for_pain_point(pp["id"]),
        "screens": find_screens_for_requirements(...),
        "modules": [],  # Filled in Phase 3-4
        "tests": [],    # Filled in Phase 6
        "complete": False
    }
    chains.append(chain)
```

### Step 8: Write Registry Files

#### `_registry/requirements.json`

```json
{
  "$schema": "productspecs-requirements-v1",
  "$metadata": {
    "created_at": "<TIMESTAMP>",
    "updated_at": "<TIMESTAMP>",
    "source": "ProductSpecs_ExtractRequirements"
  },
  "requirements": [...],
  "by_priority": {...},
  "by_type": {...},
  "by_screen": {...},
  "statistics": {...}
}
```

#### `_registry/traceability.json`

```json
{
  "$schema": "productspecs-traceability-v1",
  "$metadata": {
    "created_at": "<TIMESTAMP>",
    "updated_at": "<TIMESTAMP>"
  },
  "requirements": [...],
  "chains": [...],
  "coverage": {
    "pain_points_addressed": 10,
    "pain_points_total": 12,
    "coverage_percent": 83,
    "p0_traced": 18,
    "p0_total": 18,
    "p0_coverage_percent": 100
  }
}
```

### Step 9: Update Progress

Update `_state/productspecs_progress.json`:
- Set `phases.extract.status` = "completed"
- Set `phases.extract.completed_at` = current timestamp
- Set `phases.extract.outputs` = ["_registry/requirements.json", "_registry/traceability.json"]
- Set `current_phase` = 3

### Step 10: Validate Checkpoint

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 2 --dir ProductSpecs_<SystemName>/
```

### Step 11: Display Summary

```
═══════════════════════════════════════════════════════
  REQUIREMENTS EXTRACTED
═══════════════════════════════════════════════════════

  System:          <SystemName>

  Requirements:    45 total
  ────────────────────────────────────────────────────
  │ Priority │ Count │ Traced │
  │──────────│───────│────────│
  │ P0       │ 18    │ 18/18 ✅│
  │ P1       │ 20    │ 18/20  │
  │ P2       │ 7     │ 4/7    │

  Types:
  • User Stories:       25
  • Functional:         15
  • Non-Functional:     5

  Traceability:
  • Complete chains:    40/45 (89%)
  • P0 coverage:        100%

  Checkpoint 2:    ✅ PASSED

═══════════════════════════════════════════════════════

  Next Steps:
  • /productspecs-modules    - Generate module specs
  • /productspecs            - Continue full generation

═══════════════════════════════════════════════════════
```

## Outputs

| File | Location |
|------|----------|
| `requirements.json` | `ProductSpecs_<SystemName>/_registry/` |
| `traceability.json` | `ProductSpecs_<SystemName>/_registry/` |

## Error Handling

| Error | Action |
|-------|--------|
| Checkpoint 1 not passed | **BLOCK** - Run /productspecs-validate |
| Missing registry files | **BLOCK** - Run Prototype first |
| Requirement without traceability | **WARN** - Log, continue |

## Outputs

| Command | Description |
|---------|-------------|
| `/productspecs-validate` | Previous phase |
| `/productspecs-modules` | Next phase |
| `/productspecs` | Full generation |
