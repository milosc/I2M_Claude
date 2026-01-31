---
description: Extract and structure requirements from discovery
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-requirements started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-requirements ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-requirements instruction_start '{"stage": "prototype", "method": "instruction-based"}'
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

- `$ARGUMENTS` - Required: `<SystemName>` or path to `Prototype_<SystemName>/`

## Prerequisites

- Phase 1 completed: `_state/discovery_summary.json` exists
- Checkpoint 1 passed

## Skills Used

Read BEFORE execution:
- `.claude/skills/Prototype_Requirements/SKILL.md`

## Execution Steps

### Step 1: Load Discovery Summary

Read `_state/discovery_summary.json`:
- Get pain_points array
- Get jtbd array
- Get screens array
- Get personas array

### Step 2: Update Progress

Update `_state/prototype_progress.json`:
```json
{
  "current_phase": 2,
  "phases": {
    "requirements": {
      "status": "in_progress",
      "started_at": "<timestamp>"
    }
  }
}
```

### Step 3: Execute Prototype_Requirements Skill

Read and execute `.claude/skills/Prototype_Requirements/SKILL.md`:

1. **Transform Pain Points to Epics**:

   For each pain point cluster:
   ```json
   {
     "id": "EPIC-001",
     "type": "epic",
     "title": "Real-time Inventory Visibility",
     "description": "Enable operators to see inventory levels in real-time",
     "pain_point_refs": ["PP-1.1", "PP-1.2"],
     "persona_refs": ["PERSONA_WAREHOUSE_OPERATOR"],
     "priority": "P0"
   }
   ```

2. **Transform JTBDs to User Stories**:

   For each JTBD:
   ```json
   {
     "id": "US-001",
     "type": "story",
     "title": "View current stock levels",
     "description": "As a warehouse operator, I want to see current stock levels so that I can make informed decisions",
     "parent_id": "EPIC-001",
     "jtbd_refs": ["JTBD-1.1"],
     "pain_point_refs": ["PP-1.1"],
     "persona_refs": ["PERSONA_WAREHOUSE_OPERATOR"],
     "acceptance_criteria": [
       "Stock levels update within 5 seconds",
       "Levels show for all warehouse locations",
       "Color coding for low stock alerts"
     ],
     "screen_refs": ["S-1.1"],
     "priority": "P0"
   }
   ```

3. **Assign Priority**:

   | Priority | Criteria |
   |----------|----------|
   | P0 | High severity pain points, core user flows |
   | P1 | Medium severity, secondary features |
   | P2 | Low severity, nice-to-have features |

4. **Create Traceability Links**:

   Every requirement MUST have:
   - At least one `pain_point_refs`
   - At least one `persona_refs`
   - Linked `jtbd_refs` where applicable
   - Associated `screen_refs` where applicable

### Step 4: Generate Requirements Registry

Create `_state/requirements_registry.json`:

```json
{
  "schema_version": "1.0.0",
  "generated_at": "<YYYY-MM-DD>",
  "discovery_source": "ClientAnalysis_<SystemName>/",
  "requirements": [
    {
      "id": "EPIC-001",
      "type": "epic",
      "title": "Real-time Inventory Visibility",
      "description": "...",
      "priority": "P0",
      "pain_point_refs": ["PP-1.1", "PP-1.2"],
      "jtbd_refs": [],
      "persona_refs": ["PERSONA_WAREHOUSE_OPERATOR"],
      "screen_refs": [],
      "acceptance_criteria": [],
      "children": ["US-001", "US-002"],
      "status": "pending"
    },
    {
      "id": "US-001",
      "type": "story",
      "title": "View current stock levels",
      "description": "As a warehouse operator...",
      "priority": "P0",
      "parent_id": "EPIC-001",
      "pain_point_refs": ["PP-1.1"],
      "jtbd_refs": ["JTBD-1.1"],
      "persona_refs": ["PERSONA_WAREHOUSE_OPERATOR"],
      "screen_refs": ["S-1.1"],
      "acceptance_criteria": [
        "Stock levels update within 5 seconds",
        "Levels show for all warehouse locations"
      ],
      "component_refs": [],
      "status": "pending"
    }
  ],
  "statistics": {
    "total": 0,
    "by_type": {
      "epic": 0,
      "story": 0,
      "task": 0
    },
    "by_priority": {
      "P0": 0,
      "P1": 0,
      "P2": 0
    },
    "by_status": {
      "pending": 0,
      "in_progress": 0,
      "completed": 0
    }
  },
  "traceability": {
    "pain_points_covered": [],
    "pain_points_uncovered": [],
    "coverage_percent": 0
  }
}
```

### Step 5: Update Traceability

Update `traceability/prototype_traceability_register.json`:
- Add requirements to artifacts.requirements
- Create trace_chains linking pain_point → jtbd → requirement
- Update coverage metrics

### Step 6: Run Checkpoint Validation

```bash
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 2 --dir Prototype_<SystemName>/
```

**Validation Criteria**:
- `_state/requirements_registry.json` exists
- At least 1 requirement defined
- Every requirement has `pain_point_refs`
- Every requirement has `priority`
- P0 requirements have acceptance criteria

### Step 7: Update Progress

Update `_state/prototype_progress.json`:
```json
{
  "current_phase": 3,
  "phases": {
    "requirements": {
      "status": "completed",
      "completed_at": "<timestamp>",
      "outputs": ["_state/requirements_registry.json"]
    }
  }
}
```

### Step 8: Display Summary

```
═══════════════════════════════════════════════════════
  REQUIREMENTS EXTRACTION COMPLETE
═══════════════════════════════════════════════════════

  Requirements Generated:
  ├── Epics:           <N>
  ├── User Stories:    <N>
  └── Tasks:           <N>

  By Priority:
  ├── P0 (Critical):   <N>
  ├── P1 (Important):  <N>
  └── P2 (Nice-to-have): <N>

  Traceability:
  ├── Pain Points:     <N>/<M> covered (<P>%)
  └── JTBDs Linked:    <N>

  Checkpoint 2:        ✅ PASSED

═══════════════════════════════════════════════════════

  Output: _state/requirements_registry.json

  Next: /prototype-data or /prototype <SystemName>

═══════════════════════════════════════════════════════
```

## Outputs

| File | Purpose |
|------|---------|
| `_state/requirements_registry.json` | Hierarchical requirements with traceability |

## Error Handling

| Error | Action |
|-------|--------|
| discovery_summary.json missing | **BLOCK** - Run /prototype-validate first |
| No pain points found | Generate placeholder, log warning |
| Traceability gap | Log warning, continue |


---

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype-validate` | Run Phase 1 |
| `/prototype-data` | Run Phases 3-5 |
| `/prototype` | Run full prototype |
