---
description: Validate Prototype checkpoint requirements and build status
argument-hint: --checkpoint <N>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-validate started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-validate ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-validate instruction_start '{"stage": "prototype", "method": "instruction-based"}'
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

- Prototype initialized: `Prototype_<SystemName>/` exists, ROOT `_state/` has prototype files
- Discovery complete: `ClientAnalysis_<SystemName>/` has all required outputs

## Skills Used

Read BEFORE execution:
- `.claude/skills/Prototype_ValidateDiscovery/SKILL.md`

## Execution Steps

### Step 1: Load Configuration

Read `_state/prototype_config.json` (ROOT level):
- Get `discovery_source` path
- Validate configuration is valid

### Step 2: Update Progress

Update `_state/prototype_progress.json`:
```json
{
  "current_phase": 1,
  "phases": {
    "validate_discovery": {
      "status": "in_progress",
      "started_at": "<timestamp>"
    }
  }
}
```

### Step 3: Execute Prototype_ValidateDiscovery Skill

Read and execute `.claude/skills/Prototype_ValidateDiscovery/SKILL.md`:

1. **Validate Required Files Exist**:

   | Category | Required Files |
   |----------|----------------|
   | Analysis | `01-analysis/ANALYSIS_SUMMARY.md`, `01-analysis/PAIN_POINTS.md` |
   | Research | `02-research/personas/PERSONA_*.md`, `02-research/JOBS_TO_BE_DONE.md` |
   | Strategy | `03-strategy/PRODUCT_VISION.md` |
   | Design | `04-design-specs/screen-definitions.md`, `04-design-specs/data-fields.md` |

2. **Extract Discovery Data**:

   From `PAIN_POINTS.md`:
   - Extract all PP-X.X identifiers
   - Extract severity levels
   - Extract persona associations

   From `personas/PERSONA_*.md`:
   - Extract persona names and IDs
   - Extract key characteristics

   From `JOBS_TO_BE_DONE.md`:
   - Extract all JTBD-X.X identifiers
   - Extract pain point references

   From `screen-definitions.md`:
   - Extract all S-X.X screen identifiers
   - Extract screen names and types

   From `data-fields.md`:
   - Extract entity names
   - Extract field definitions

3. **Identify Gaps**:
   - Missing persona references in pain points
   - Orphan JTBDs (not linked to pain points)
   - Screens without data requirements
   - Data fields without screen references

4. **Fill Gaps via Brainstorming** (if needed):
   - Generate missing linkages
   - Add placeholder data where safe
   - Document assumptions

### Step 4: Generate Discovery Summary

Create `_state/discovery_summary.json`:

```json
{
  "schema_version": "1.0.0",
  "extracted_from": "ClientAnalysis_<SystemName>/",
  "extracted_at": "<YYYY-MM-DD>",
  "validation_status": "complete|partial|failed",
  "personas": [
    {
      "id": "PERSONA_WAREHOUSE_OPERATOR",
      "name": "Warehouse Operator",
      "file": "02-research/personas/PERSONA_WAREHOUSE_OPERATOR.md",
      "pain_point_count": 5
    }
  ],
  "pain_points": [
    {
      "id": "PP-1.1",
      "title": "Manual inventory counts",
      "severity": "high",
      "persona_refs": ["PERSONA_WAREHOUSE_OPERATOR"],
      "jtbd_refs": ["JTBD-1.1"]
    }
  ],
  "jtbd": [
    {
      "id": "JTBD-1.1",
      "statement": "When I need to count inventory...",
      "pain_point_refs": ["PP-1.1"],
      "persona_refs": ["PERSONA_WAREHOUSE_OPERATOR"]
    }
  ],
  "screens": [
    {
      "id": "S-1.1",
      "name": "Dashboard",
      "type": "overview",
      "file": "04-design-specs/screen-definitions.md#dashboard"
    }
  ],
  "data_entities": [
    {
      "name": "Inventory Item",
      "file": "04-design-specs/data-fields.md",
      "field_count": 12
    }
  ],
  "statistics": {
    "personas_count": 0,
    "pain_points_count": 0,
    "jtbd_count": 0,
    "screens_count": 0,
    "entities_count": 0
  },
  "gaps": [],
  "assumptions": []
}
```

### Step 5: Update Traceability

Update `traceability/prototype_traceability_register.json`:
- Add extracted pain points to trace_chains
- Update coverage.pain_points_total

### Step 6: Run Checkpoint Validation

```bash
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 1 --dir Prototype_<SystemName>/
```

**Validation Criteria**:
- `_state/discovery_summary.json` exists
- Contains at least 1 persona
- Contains at least 1 pain point
- Contains at least 1 screen
- All pain points have severity
- All JTBDs have pain_point_refs

### Step 7: Update Progress

Update `_state/prototype_progress.json`:
```json
{
  "current_phase": 2,
  "phases": {
    "validate_discovery": {
      "status": "completed",
      "completed_at": "<timestamp>",
      "outputs": ["_state/discovery_summary.json"]
    }
  },
  "validation_history": [
    {
      "checkpoint": 1,
      "timestamp": "<timestamp>",
      "result": "pass",
      "details": {}
    }
  ]
}
```

### Step 8: Display Summary

```
═══════════════════════════════════════════════════════
  DISCOVERY VALIDATION COMPLETE
═══════════════════════════════════════════════════════

  Discovery Source:    ClientAnalysis_<SystemName>/

  Extracted:
  ├── Personas:        <N>
  ├── Pain Points:     <N>
  ├── JTBDs:           <N>
  ├── Screens:         <N>
  └── Data Entities:   <N>

  Gaps Found:          <N>
  Assumptions Made:    <N>

  Checkpoint 1:        ✅ PASSED

═══════════════════════════════════════════════════════

  Output: _state/discovery_summary.json

  Next: /prototype-requirements or /prototype <SystemName>

═══════════════════════════════════════════════════════
```

## Outputs

| File | Purpose |
|------|---------|
| `_state/discovery_summary.json` | Extracted Discovery data |

## Error Handling

| Error | Action |
|-------|--------|
| Discovery folder missing | **BLOCK** - Cannot proceed |
| Required file missing | Log gap, continue extraction |
| Parse error in Discovery file | Log `⛔ SKIPPED`, continue |
| Checkpoint validation fails | Display issues, suggest fixes |


---

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype` | Run full prototype |
| `/prototype-requirements` | Run Phase 2 |
| `/prototype-status` | Check progress |
