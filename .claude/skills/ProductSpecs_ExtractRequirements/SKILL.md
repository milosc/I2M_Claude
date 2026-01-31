---
name: extracting-productspecs-requirements
description: Use when you need to extract and organize requirements hierarchy with full traceability from Discovery through Prototype.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-productspecs-requirements started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-productspecs-requirements ended '{"stage": "productspecs"}'
---

# ProductSpecs_ExtractRequirements

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill extracting-productspecs-requirements instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

**Purpose**: Extract and organize requirements hierarchy with full traceability from Discovery through Prototype.

**Version**: 1.0.0
**Created**: 2025-12-22
**Phase**: 2 of ProductSpecs pipeline

---

## Overview

This skill extracts requirements from Prototype outputs and organizes them into a hierarchical structure with complete traceability chains. Each requirement is linked back to:
- Original pain point (from Discovery)
- JTBD (from Discovery)
- Screen (from Discovery/Prototype)
- Component (from Prototype)

---

## Prerequisites

### Required State Files

Location: `_state/` (at PROJECT ROOT)

| File | Purpose |
|------|---------|
| `productspecs_config.json` | ProductSpecs configuration |
| `productspecs_progress.json` | Phase tracking |
| `discovery_summary.json` | Discovery data |
| `requirements_registry.json` | Prototype requirements |
| `screen_registry.json` | Screen tracking |

### Checkpoint 1 Must Pass

Run `ProductSpecs_Validate` first.

---

## Execution Flow

### Phase 2.1: Load Source Data

```python
# Load from shared _state/
discovery_summary = json.load("_state/discovery_summary.json")
requirements_registry = json.load("_state/requirements_registry.json")
screen_registry = json.load("traceability/screen_registry.json")

# Extract key data
pain_points = discovery_summary.get("pain_points", [])
jtbds = discovery_summary.get("jtbds", [])
personas = discovery_summary.get("personas", [])
screens = discovery_summary.get("screens", [])
requirements = requirements_registry.get("requirements", [])
```

### Phase 2.2: Build Pain Point Index

```python
# Create lookup for pain points
pain_point_index = {}
for pp in pain_points:
    pp_id = pp.get("id")
    pain_point_index[pp_id] = {
        "id": pp_id,
        "title": pp.get("title"),
        "description": pp.get("description"),
        "severity": pp.get("severity"),
        "affected_users": pp.get("affected_users", []),
        "source": pp.get("source")  # Link to client material
    }
```

### Phase 2.3: Build JTBD Index

```python
# Create lookup for JTBDs
jtbd_index = {}
for jtbd in jtbds:
    jtbd_id = jtbd.get("id")
    jtbd_index[jtbd_id] = {
        "id": jtbd_id,
        "statement": jtbd.get("statement"),
        "persona": jtbd.get("persona"),
        "pain_point_refs": jtbd.get("pain_point_refs", []),
        "success_criteria": jtbd.get("success_criteria", [])
    }
```

### Phase 2.4: Enrich Requirements

For each requirement, add complete traceability:

```python
enriched_requirements = []

for req in requirements:
    enriched = {
        # Base requirement data
        "id": req.get("id"),
        "type": req.get("type"),  # user_story | functional | non_functional | accessibility
        "priority": req.get("priority"),  # P0 | P1 | P2
        "title": req.get("title"),
        "description": req.get("description"),
        "acceptance_criteria": req.get("acceptance_criteria", []),

        # Traceability links
        "pain_point_refs": req.get("pain_point_refs", []),
        "jtbd_refs": req.get("jtbd_refs", []),
        "screen_refs": req.get("screen_refs", []),
        "persona_refs": req.get("persona_refs", []),

        # Enriched data
        "pain_points": [],  # Full pain point objects
        "jtbds": [],        # Full JTBD objects
        "screens": [],      # Full screen objects

        # Computed fields
        "traceability_complete": False,
        "missing_links": []
    }

    # Enrich with pain point details
    for pp_ref in enriched["pain_point_refs"]:
        if pp_ref in pain_point_index:
            enriched["pain_points"].append(pain_point_index[pp_ref])

    # Enrich with JTBD details
    for jtbd_ref in enriched["jtbd_refs"]:
        if jtbd_ref in jtbd_index:
            enriched["jtbds"].append(jtbd_index[jtbd_ref])

    # Check traceability completeness
    if not enriched["pain_point_refs"]:
        enriched["missing_links"].append("pain_point")
    if not enriched["jtbd_refs"]:
        enriched["missing_links"].append("jtbd")
    if not enriched["screen_refs"]:
        enriched["missing_links"].append("screen")

    enriched["traceability_complete"] = len(enriched["missing_links"]) == 0

    enriched_requirements.append(enriched)
```

### Phase 2.5: Group Requirements

#### By Priority

```python
by_priority = {
    "P0": [r for r in enriched_requirements if r["priority"] == "P0"],
    "P1": [r for r in enriched_requirements if r["priority"] == "P1"],
    "P2": [r for r in enriched_requirements if r["priority"] == "P2"]
}
```

#### By Type

```python
by_type = {
    "user_story": [r for r in enriched_requirements if r["type"] == "user_story"],
    "functional": [r for r in enriched_requirements if r["type"] == "functional"],
    "non_functional": [r for r in enriched_requirements if r["type"] == "non_functional"],
    "accessibility": [r for r in enriched_requirements if r["type"] == "accessibility"]
}
```

#### By Screen

```python
by_screen = {}
for req in enriched_requirements:
    for screen_ref in req["screen_refs"]:
        if screen_ref not in by_screen:
            by_screen[screen_ref] = []
        by_screen[screen_ref].append(req["id"])
```

### Phase 2.6: Calculate Statistics

```python
statistics = {
    "total": len(enriched_requirements),
    "by_priority": {
        "P0": len(by_priority["P0"]),
        "P1": len(by_priority["P1"]),
        "P2": len(by_priority["P2"])
    },
    "by_type": {
        "user_story": len(by_type["user_story"]),
        "functional": len(by_type["functional"]),
        "non_functional": len(by_type["non_functional"]),
        "accessibility": len(by_type["accessibility"])
    },
    "traceability": {
        "complete": sum(1 for r in enriched_requirements if r["traceability_complete"]),
        "incomplete": sum(1 for r in enriched_requirements if not r["traceability_complete"]),
        "p0_complete": sum(1 for r in by_priority["P0"] if r["traceability_complete"])
    }
}
```

### Phase 2.7: Write Registry Files

#### `traceability/requirements_registry.json` (ROOT level - single source of truth)

```json
{
  "$schema": "productspecs-requirements-v1",
  "$metadata": {
    "created_at": "<TIMESTAMP>",
    "updated_at": "<TIMESTAMP>",
    "source": "ProductSpecs_ExtractRequirements"
  },
  "requirements": [
    {
      "id": "REQ-001",
      "type": "user_story",
      "priority": "P0",
      "title": "Search inventory items",
      "description": "As a warehouse operator, I need to search for items...",
      "acceptance_criteria": [
        "Given I am on the search screen, When I enter an item code...",
        "Given search results are displayed, When I tap an item..."
      ],
      "pain_point_refs": ["PP-1.1"],
      "jtbd_refs": ["JTBD-1.1"],
      "screen_refs": ["M-01"],
      "persona_refs": ["PERSONA_WAREHOUSE_OPERATOR"],
      "traceability_complete": true,
      "missing_links": []
    }
  ],
  "by_priority": {
    "P0": ["REQ-001", "REQ-002"],
    "P1": ["REQ-010", "REQ-011"],
    "P2": ["REQ-020"]
  },
  "by_type": {
    "user_story": ["REQ-001", "REQ-002"],
    "functional": ["REQ-010"],
    "non_functional": ["REQ-020"]
  },
  "by_screen": {
    "M-01": ["REQ-001", "REQ-010"],
    "M-02": ["REQ-002", "REQ-011"]
  },
  "statistics": {
    "total": 45,
    "by_priority": { "P0": 18, "P1": 20, "P2": 7 },
    "by_type": { "user_story": 25, "functional": 15, "non_functional": 5 },
    "traceability": { "complete": 40, "incomplete": 5, "p0_complete": 18 }
  }
}
```

### Phase 2.8: Write Traceability File

#### `traceability/productspecs_traceability_register.json` (ROOT level - single source of truth)

```json
{
  "$schema": "productspecs-traceability-v1",
  "$metadata": {
    "created_at": "<TIMESTAMP>",
    "updated_at": "<TIMESTAMP>"
  },
  "requirements": [
    {
      "id": "REQ-001",
      "priority": "P0",
      "pain_point_refs": ["PP-1.1"],
      "jtbd_refs": ["JTBD-1.1"],
      "screen_refs": ["M-01"],
      "module_refs": [],  // To be filled by modules phase
      "test_refs": []     // To be filled by tests phase
    }
  ],
  "chains": [
    {
      "chain_id": "CHAIN-001",
      "pain_point": "PP-1.1",
      "jtbd": "JTBD-1.1",
      "requirements": ["REQ-001", "REQ-002"],
      "screens": ["M-01", "M-02"],
      "modules": [],
      "tests": [],
      "complete": false
    }
  ],
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

### Phase 2.9: Update State

#### Update `_state/productspecs_progress.json`

```json
{
  "phases": {
    "extract": {
      "status": "completed",
      "completed_at": "<TIMESTAMP>",
      "outputs": [
        "_registry/requirements.json",
        "_registry/traceability.json"
      ]
    }
  },
  "current_phase": 3
}
```

### Phase 2.10: Validate Checkpoint 2

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 2 --dir ProductSpecs_<SystemName>/
```

---

## Outputs

| File | Location | Purpose |
|------|----------|---------|
| `requirements_registry.json` | `traceability/` (ROOT) | Requirements with traceability |
| `productspecs_traceability_register.json` | `traceability/` (ROOT) | Traceability chains |
| `productspecs_progress.json` | `_state/` | Phase status |

---

## Traceability Chain Structure

```
Pain Point (PP-X.X)
    ↓
JTBD (JTBD-X.X)
    ↓
Requirement (REQ-XXX)
    ↓
Screen (M-XX / D-XX)
    ↓
Module (MOD-XXX-YYY-ZZ)  [Added in Phase 3-4]
    ↓
Test Case (TC-XXX)       [Added in Phase 6]
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Missing discovery_summary.json | **BLOCK** - Run ProductSpecs_Validate |
| Missing requirements_registry.json | **BLOCK** - Run Prototype first |
| Requirement without pain_point | **WARN** - Log, continue |
| Invalid reference | **WARN** - Log, continue |

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `ProductSpecs_Validate` | Previous phase |
| `ProductSpecs_Generator` | Next phase - generates modules |
