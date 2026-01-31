---
description: Export ProductSpecs outputs for Implementation stage
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-export started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-export ended '{"stage": "productspecs"}'
---


# /productspecs-export - Generate JIRA Export & Documentation

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs-export instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
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

- `/productspecs-finalize <SystemName>` completed (Checkpoint 7 passed)

## Skills Used

Read BEFORE execution:
- `.claude/skills/ProductSpecs_JIRAExporter/SKILL.md`

## Execution Steps

### Step 1: Verify Checkpoint 7

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 7 --dir ProductSpecs_<SystemName>/
```

If not passed, show error and exit.

### Step 2: Load Configuration

```python
# From shared _state/ at ROOT level
config = json.load("_state/productspecs_config.json")
system_name = config["system_name"]
output_path = config["output_path"]

# Load registries
modules = json.load(f"{output_path}/_registry/modules.json")
requirements = json.load(f"{output_path}/_registry/requirements.json")
nfrs = json.load(f"{output_path}/_registry/nfrs.json")
traceability = json.load(f"{output_path}/_registry/traceability.json")
test_cases = json.load(f"{output_path}/_registry/test-cases.json")
discovery_summary = json.load("_state/discovery_summary.json")
```

### Step 3: Collect JIRA Configuration

If `ProductSpecs_<SystemName>/04-jira/jira_config.json` does not exist, prompt:

```
╔══════════════════════════════════════════════════════════════╗
║  JIRA EXPORT CONFIGURATION                                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Please provide JIRA project details:                        ║
║                                                              ║
║  1. Project Key (e.g., INV):                                ║
║  2. Project Name (e.g., Inventory Management System):       ║
║  3. Sub-task Strategy:                                       ║
║     a) by-discipline (Frontend, Backend, Testing, A11Y...)  ║
║     b) by-component (per UI component)                      ║
║     c) by-acceptance-criteria (per AC)                      ║
║     d) comprehensive (all of the above)                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

Save configuration to `ProductSpecs_<SystemName>/04-jira/jira_config.json`:

```json
{
  "project_key": "INV",
  "project_name": "Inventory Management System",
  "subtask_strategy": "by-discipline",
  "generate_subtasks": true,
  "configured_at": "ISO8601"
}
```

### Step 4: Create JIRA Folder Structure

```
ProductSpecs_<SystemName>/04-jira/
├── jira_config.json
├── IMPORT_GUIDE.md
├── full-hierarchy.csv
├── epics-and-stories.csv
├── subtasks-only.csv
└── jira-import.json
```

### Step 5: Generate JIRA Hierarchy

Build hierarchy from registries:

```python
jira_hierarchy = {
    "project_key": jira_config["project_key"],
    "generated_at": timestamp,
    "epics": [],
    "stories": [],
    "subtasks": []
}

# Generate Epics from Modules
for module in modules["modules"]:
    epic = {
        "key": f"{project_key}-{next_epic_id()}",
        "type": "Epic",
        "summary": module["title"],
        "description": module["description"],
        "labels": [module["app"], module["feature"]],
        "priority": module.get("priority", "Medium"),
        "module_ref": module["id"],
        "requirements": module.get("requirements", []),
        "acceptance_criteria": generate_epic_ac(module)
    }
    jira_hierarchy["epics"].append(epic)

# Generate Stories from Requirements
for req in requirements["requirements"]:
    story = {
        "key": f"{project_key}-{next_story_id()}",
        "type": "Story",
        "summary": req["title"],
        "description": req["description"],
        "epic_link": find_epic_for_requirement(req["id"]),
        "priority": convert_priority(req["priority"]),
        "story_points": estimate_points(req),
        "requirement_ref": req["id"],
        "pain_point_refs": req.get("pain_point_refs", []),
        "jtbd_refs": req.get("jtbd_refs", []),
        "acceptance_criteria": req.get("acceptance_criteria", []),
        "test_refs": find_tests_for_requirement(req["id"])
    }
    jira_hierarchy["stories"].append(story)

# Generate Sub-tasks based on strategy
if jira_config["generate_subtasks"]:
    subtasks = generate_subtasks(
        stories=jira_hierarchy["stories"],
        strategy=jira_config["subtask_strategy"],
        test_cases=test_cases,
        nfrs=nfrs
    )
    jira_hierarchy["subtasks"] = subtasks
```

### Step 6: Generate Sub-tasks by Strategy

#### Strategy: by-discipline (Default)

```python
DISCIPLINES = [
    {"name": "Frontend", "prefix": "FE", "tasks": ["Implement UI components", "Add styling", "Handle state"]},
    {"name": "Backend", "prefix": "BE", "tasks": ["Implement API endpoint", "Add validation", "Database queries"]},
    {"name": "Testing", "prefix": "QA", "tasks": ["Write unit tests", "Write integration tests", "E2E scenarios"]},
    {"name": "Accessibility", "prefix": "A11Y", "tasks": ["WCAG compliance", "Screen reader testing", "Keyboard nav"]},
    {"name": "Documentation", "prefix": "DOC", "tasks": ["Update API docs", "User guide section"]},
    {"name": "Review", "prefix": "REV", "tasks": ["Code review", "Design review", "Security review"]}
]

for story in stories:
    for discipline in DISCIPLINES:
        subtask = {
            "type": "Sub-task",
            "parent": story["key"],
            "summary": f"[{discipline['prefix']}] {story['summary']}",
            "description": generate_discipline_description(discipline, story),
            "labels": [discipline["name"].lower()]
        }
        subtasks.append(subtask)
```

#### Strategy: by-component

```python
for story in stories:
    components = find_components_for_story(story)
    for component in components:
        subtask = {
            "type": "Sub-task",
            "parent": story["key"],
            "summary": f"Implement {component['name']}",
            "description": f"Component: {component['id']}\n\n{component['description']}",
            "labels": ["component", component["category"]]
        }
        subtasks.append(subtask)
```

#### Strategy: by-acceptance-criteria

```python
for story in stories:
    for i, ac in enumerate(story["acceptance_criteria"], 1):
        subtask = {
            "type": "Sub-task",
            "parent": story["key"],
            "summary": f"AC-{i}: {ac['title']}",
            "description": ac["description"],
            "labels": ["acceptance-criteria"]
        }
        subtasks.append(subtask)
```

#### Strategy: comprehensive

```python
# Combine all strategies
subtasks = []
subtasks.extend(generate_by_discipline(stories))
subtasks.extend(generate_by_component(stories))
subtasks.extend(generate_by_acceptance_criteria(stories))
# De-duplicate and merge similar subtasks
subtasks = deduplicate_subtasks(subtasks)
```

### Step 7: Write CSV Files

#### `full-hierarchy.csv`

```csv
Issue Type,Summary,Description,Epic Link,Priority,Labels,Story Points,Parent,Acceptance Criteria
Epic,Stock Adjustment Module,"Complete stock adjustment functionality",,,inv|adjust,,,"AC1: User can adjust quantity\nAC2: Adjustment requires approval"
Story,Search inventory items,"As a warehouse operator, I want to search items",INV-1,High,search|p0,5,,"Given search screen\nWhen I enter criteria\nThen results display"
Sub-task,[FE] Search inventory items,"Implement frontend components",,Medium,frontend,,INV-2,
Sub-task,[BE] Search inventory items,"Implement API endpoint",,Medium,backend,,INV-2,
```

#### `epics-and-stories.csv`

```csv
Issue Type,Summary,Description,Epic Link,Priority,Labels,Story Points,Acceptance Criteria
Epic,Stock Adjustment Module,"Complete stock adjustment functionality",,,"inv|adjust",,"AC1: User can adjust..."
Story,Search inventory items,"As a warehouse operator...",INV-1,High,"search|p0",5,"Given search screen..."
```

#### `subtasks-only.csv`

```csv
Issue Type,Summary,Description,Parent,Labels
Sub-task,[FE] Search inventory items,"Implement frontend components",INV-2,frontend
Sub-task,[BE] Search inventory items,"Implement API endpoint",INV-2,backend
Sub-task,[QA] Search inventory items,"Write test cases",INV-2,testing
```

### Step 8: Write JSON Export

Write `ProductSpecs_<SystemName>/04-jira/jira-import.json`:

```json
{
  "$schema": "jira-import-v1",
  "$metadata": {
    "project_key": "INV",
    "project_name": "Inventory Management System",
    "generated_at": "ISO8601",
    "source": "ProductSpecs_JIRAExporter",
    "version": "2.0.0"
  },
  "statistics": {
    "epics": 12,
    "stories": 45,
    "subtasks": 180,
    "total": 237
  },
  "hierarchy": {
    "epics": [...],
    "stories": [...],
    "subtasks": [...]
  },
  "traceability": {
    "requirements_mapped": 45,
    "requirements_total": 45,
    "modules_mapped": 12,
    "modules_total": 12,
    "tests_linked": 107,
    "tests_total": 107
  }
}
```

### Step 9: Generate Import Guide

Write `ProductSpecs_<SystemName>/04-jira/IMPORT_GUIDE.md`:

```markdown
# JIRA Import Guide

**Project**: <SystemName>
**Generated**: <TIMESTAMP>

---

## Import Options

### Option 1: Full Hierarchy (Recommended)

Import `full-hierarchy.csv` to create complete structure:
- Epics
- Stories linked to Epics
- Sub-tasks linked to Stories

**Steps**:
1. Go to Project Settings → External System Import
2. Select CSV import
3. Upload `full-hierarchy.csv`
4. Map fields as shown below

### Option 2: Two-Phase Import

For large projects or complex hierarchies:

**Phase 1**: Import `epics-and-stories.csv`
- Creates Epics and Stories
- Establishes Epic links

**Phase 2**: Import `subtasks-only.csv`
- Creates Sub-tasks
- Links to parent Stories

---

## Field Mapping

| CSV Column | JIRA Field |
|------------|------------|
| Issue Type | Issue Type |
| Summary | Summary |
| Description | Description |
| Epic Link | Epic Link |
| Priority | Priority |
| Labels | Labels |
| Story Points | Story Points |
| Parent | Parent |
| Acceptance Criteria | Custom: Acceptance Criteria |

---

## Post-Import Checklist

- [ ] Verify Epic count: <N> epics
- [ ] Verify Story count: <N> stories
- [ ] Verify Sub-task count: <N> sub-tasks
- [ ] Check Epic links are correct
- [ ] Check Parent links for sub-tasks
- [ ] Review priority assignments
- [ ] Add team members to stories
- [ ] Set sprint assignments

---

## Traceability Reference

This export maintains full traceability:

| Discovery ID | ProductSpecs ID | JIRA Key |
|--------------|-----------------|----------|
| PP-1.1 | REQ-001 | INV-2 |
| JTBD-1.1 | REQ-001 | INV-2 |
| ... | ... | ... |

See `TRACEABILITY_MATRIX.md` for complete mapping.
```

### Step 10: Generate Final Summary

Write `ProductSpecs_<SystemName>/00-overview/GENERATION_SUMMARY.md`:

```markdown
# ProductSpecs Generation Summary

**System**: <SystemName>
**Generated**: <TIMESTAMP>
**Status**: ✅ COMPLETE

---

## Generation Statistics

| Metric | Count |
|--------|-------|
| Modules Generated | 12 |
| Requirements Mapped | 45 |
| NFRs Defined | 25 |
| Test Cases Specified | 107 |
| API Endpoints Documented | 14 |
| JIRA Items Created | 237 |

---

## Traceability Coverage

| Chain | Coverage |
|-------|----------|
| Pain Points → Requirements | 100% |
| JTBDs → Requirements | 100% |
| Requirements → Modules | 100% |
| Modules → Tests | 100% |
| P0 End-to-End | 100% |

---

## Output Files

### Module Specifications
- `01-modules/module-index.md`
- `01-modules/MOD-*.md` (12 files)

### API & NFRs
- `02-api/api-index.md`
- `02-api/NFR_SPECIFICATIONS.md`
- `02-api/data-contracts.md`

### Test Specifications
- `03-tests/test-case-registry.md`
- `03-tests/e2e-scenarios.md`
- `03-tests/accessibility-checklist.md`

### JIRA Export
- `04-jira/full-hierarchy.csv`
- `04-jira/epics-and-stories.csv`
- `04-jira/subtasks-only.csv`
- `04-jira/jira-import.json`
- `04-jira/IMPORT_GUIDE.md`

### Validation
- `00-overview/TRACEABILITY_MATRIX.md`
- `00-overview/VALIDATION_REPORT.md`

---

## Next Steps

1. Review JIRA import files
2. Import to JIRA using IMPORT_GUIDE.md
3. Assign team members
4. Set sprint schedule
5. Begin development

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Owner | | | |
| Tech Lead | | | |
| QA Lead | | | |
```

### Step 11: Update Progress

Update `_state/productspecs_progress.json`:

```python
progress["phases"]["export"]["status"] = "completed"
progress["phases"]["export"]["completed_at"] = timestamp
progress["phases"]["export"]["outputs"] = [
    "04-jira/IMPORT_GUIDE.md",
    "04-jira/full-hierarchy.csv",
    "04-jira/epics-and-stories.csv",
    "04-jira/subtasks-only.csv",
    "04-jira/jira-import.json",
    "00-overview/GENERATION_SUMMARY.md"
]
progress["current_phase"] = 9  # Complete
progress["completed_at"] = timestamp
```

### Step 12: Validate Checkpoint 8

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 8 --dir ProductSpecs_<SystemName>/
```

### Step 13: Display Final Summary

```
═══════════════════════════════════════════════════════════════
  PRODUCTSPECS GENERATION COMPLETE
═══════════════════════════════════════════════════════════════

  System:          <SystemName>
  Completed:       <TIMESTAMP>

  Generation Summary:
  ──────────────────────────────────────────────────────────────
  │ Artifact          │ Count │ Coverage │
  │───────────────────│───────│──────────│
  │ Module Specs      │ 12    │ 100%     │
  │ Requirements      │ 45    │ 100%     │
  │ NFRs              │ 25    │ 100%     │
  │ Test Cases        │ 107   │ 100%     │
  │ API Endpoints     │ 14    │ 100%     │

  JIRA Export:
  ──────────────────────────────────────────────────────────────
  │ Type              │ Count │
  │───────────────────│───────│
  │ Epics             │ 12    │
  │ Stories           │ 45    │
  │ Sub-tasks         │ 180   │
  │ Total Items       │ 237   │

  Checkpoint 8:      ✅ PASSED

  Output Location:   ProductSpecs_<SystemName>/

═══════════════════════════════════════════════════════════════

  Export Files Ready:
  • 04-jira/full-hierarchy.csv      - Complete hierarchy
  • 04-jira/epics-and-stories.csv   - Epics and Stories only
  • 04-jira/subtasks-only.csv       - Sub-tasks only
  • 04-jira/IMPORT_GUIDE.md         - Import instructions

  All Checkpoints:   ✅ 0-8 PASSED

═══════════════════════════════════════════════════════════════

  🎉 ProductSpecs generation is complete!

  Next Steps:
  1. Review JIRA import files in 04-jira/
  2. Follow IMPORT_GUIDE.md to import to JIRA
  3. Assign team members and set sprints

═══════════════════════════════════════════════════════════════
```

## Outputs

| File | Location |
|------|----------|
| `IMPORT_GUIDE.md` | `ProductSpecs_<SystemName>/04-jira/` |
| `full-hierarchy.csv` | `ProductSpecs_<SystemName>/04-jira/` |
| `epics-and-stories.csv` | `ProductSpecs_<SystemName>/04-jira/` |
| `subtasks-only.csv` | `ProductSpecs_<SystemName>/04-jira/` |
| `jira-import.json` | `ProductSpecs_<SystemName>/04-jira/` |
| `jira_config.json` | `ProductSpecs_<SystemName>/04-jira/` |
| `GENERATION_SUMMARY.md` | `ProductSpecs_<SystemName>/00-overview/` |

## Error Handling

| Error | Action |
|-------|--------|
| Checkpoint 7 not passed | **BLOCK** - Run /productspecs-finalize |
| Missing JIRA config | Prompt user for configuration |
| CSV generation fails | **WARN** - Generate JSON only |
| Large hierarchy (>500 items) | **WARN** - Suggest phased import |

## Outputs

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/productspecs-finalize` | Previous phase |
| `/productspecs-jira` | JIRA export only (no validation) |
| `/productspecs` | Full generation |
| `/productspecs-status` | Show progress |
