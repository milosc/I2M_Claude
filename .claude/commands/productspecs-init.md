---
name: productspecs-init
description: Initialize ProductSpecs folder structure and state files from Prototype
argument-hint: <SystemName>
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-init started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-init ended '{"stage": "productspecs"}'
---

# /productspecs-init - Initialize ProductSpecs

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs-init instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for module/test ID management:

```bash
# Load Traceability rules (includes module ID format MOD-XXX-XXX-NN)
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Required: `<SystemName>` or path to `Prototype_<SystemName>/`

## Prerequisites

- Completed Discovery: `ClientAnalysis_<SystemName>/` exists
- Completed Prototype: `Prototype_<SystemName>/` exists with phases 0-12 complete
- Dependencies installed: `/htec-libraries-init`

## Execution Steps

### Step 1: Parse Arguments

```
If $ARGUMENTS is a path:
  - Extract SystemName from Prototype_<SystemName>/
If $ARGUMENTS is a name:
  - Use as SystemName
  - Prototype path = Prototype_<SystemName>/
  - Discovery path = ClientAnalysis_<SystemName>/
```

### Step 2: Validate Prototype Exists

Check that Prototype folder exists and is sufficiently complete:

```bash
ls Prototype_<SystemName>/
```

**Required Files** (block if missing):

| File | Purpose |
|------|---------|
| `_state/prototype_progress.json` | Prototype phase tracking |
| `_state/discovery_summary.json` | Discovery extraction |
| `_state/requirements_registry.json` | Requirements registry |
| `traceability/screen_registry.json` | Screen tracking |
| `00-foundation/data-model/DATA_MODEL_SUMMARY.md` | Data model |
| `00-foundation/api-contracts/API_CONTRACTS_SUMMARY.md` | API contracts |
| `01-components/component-index.md` | Component library |
| `02-screens/screen-index.md` | Screen specifications |

If any required file is missing:
```
ERROR: Prototype incomplete. Missing files:
- [list missing files]

Run /prototype-status on Prototype_<SystemName>/ to check progress.
```

### Step 3: Create Folder Structure

Create `ProductSpecs_<SystemName>/` with all required folders:

```bash
# Overview
mkdir -p ProductSpecs_<SystemName>/00-overview

# Modules
mkdir -p ProductSpecs_<SystemName>/01-modules

# API
mkdir -p ProductSpecs_<SystemName>/02-api

# Tests
mkdir -p ProductSpecs_<SystemName>/03-tests

# JIRA Export
mkdir -p ProductSpecs_<SystemName>/04-jira

# Feedback sessions
mkdir -p ProductSpecs_<SystemName>/feedback-sessions

# Reports
mkdir -p ProductSpecs_<SystemName>/reports

# NOTE (v3.0): No local _registry/ folder - all registries in traceability/ at ROOT level
```

### Step 3.5: Select Module Decomposition Strategy

Determine how modules should be broken down into implementation tasks.

1. **Ask User**:

   USE AskUserQuestion:
     question: "How should modules be decomposed into tasks?"
     header: "Task Strategy"
     options:
       - label: "By Discipline (Recommended)"
         description: "FE, BE, QA subtasks per module. Best for: specialized teams"
       - label: "By Feature"
         description: "Full-stack tasks per feature. Best for: full-stack devs"
       - label: "By Phase"
         description: "All FE first, then BE, then QA. Best for: sequential delivery"

2. **Store Selection**:
   - The selected strategy will be stored in `_state/productspecs_config.json` in Step 4.

### Step 4: Initialize State Files

#### `_state/productspecs_config.json`

```json
{
  "schema_version": "1.0.0",
  "system_name": "<SystemName>",
  "created_at": "<YYYY-MM-DD>",
  "updated_at": "<YYYY-MM-DD>",
  "prototype_path": "Prototype_<SystemName>/",
  "discovery_path": "ClientAnalysis_<SystemName>/",
  "output_path": "ProductSpecs_<SystemName>/",
  "settings": {
    "skip_failures": true,
    "default_subtask_strategy": "{selected_strategy}"
  }
}
```

#### `_state/productspecs_progress.json`

```json
{
  "schema_version": "1.0.0",
  "current_phase": 0,
  "current_checkpoint": "productspecs-init",
  "started_at": "<YYYY-MM-DD HH:MM:SS>",
  "updated_at": "<YYYY-MM-DD HH:MM:SS>",
  "phases": {
    "init": {
      "phase_number": 0,
      "status": "in_progress",
      "started_at": "<YYYY-MM-DD HH:MM:SS>",
      "completed_at": null,
      "outputs": []
    },
    "validate": {
      "phase_number": 1,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "extract": {
      "phase_number": 2,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "modules_core": {
      "phase_number": 3,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "modules_extended": {
      "phase_number": 4,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "contracts": {
      "phase_number": 5,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "tests": {
      "phase_number": 6,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "traceability": {
      "phase_number": 7,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "export": {
      "phase_number": 8,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    }
  },
  "validation_history": []
}
```

### Step 5: Initialize ROOT-Level Registries (v3.0 - Single Source of Truth)

> **NOTE**: All registries are now in `traceability/` at ROOT level. No local `_registry/` folder.

#### Initialize `traceability/program_registry.json` (if not exists)

```json
{
  "version": "1.0.0",
  "schema_version": "1.0",
  "description": "Master program registry for ProductSpecs",
  "stage": "ProductSpecs",
  "checkpoint": 0,
  "system_name": "<SystemName>",
  "created_at": "<YYYY-MM-DD>",
  "updated_at": "<YYYY-MM-DD>",
  "statistics": {
    "total_modules": 0,
    "total_screens": 0,
    "total_requirements": 0,
    "p0_requirements": 0,
    "p1_requirements": 0,
    "p2_requirements": 0
  }
}
```

#### Initialize `traceability/module_registry.json` (if not exists)

```json
{
  "version": "1.0.0",
  "schema_version": "1.0",
  "description": "Registry of Module Specifications with traceability",
  "stage": "ProductSpecs",
  "checkpoint": 4,
  "system_name": "<SystemName>",
  "created_at": "<YYYY-MM-DD>",
  "updated_at": "<YYYY-MM-DD>",
  "traceability_chain": {
    "upstream": ["requirements_registry.json", "screen_registry.json", "component_registry.json"],
    "downstream": ["nfr_registry.json", "adr_registry.json", "test_case_registry.json", "user_story_registry.json"]
  },
  "items": [],
  "summary": {
    "total_modules": 0,
    "by_app": {},
    "by_priority": {},
    "by_phase": {},
    "total_effort": {"fe": 0, "be": 0, "qa": 0, "total": 0}
  }
}
```

#### Initialize `traceability/nfr_registry.json` (if not exists)

```json
{
  "version": "1.0.0",
  "schema_version": "1.0",
  "description": "Registry of Non-Functional Requirements with traceability",
  "stage": "ProductSpecs",
  "checkpoint": 5,
  "system_name": "<SystemName>",
  "created_at": "<YYYY-MM-DD>",
  "updated_at": "<YYYY-MM-DD>",
  "traceability_chain": {
    "upstream": ["requirements_registry.json", "module_registry.json"],
    "downstream": ["adr_registry.json", "test_case_registry.json"]
  },
  "items": [],
  "summary": {
    "total_nfrs": 0,
    "by_category": {},
    "by_priority": {}
  }
}
```

#### Initialize `traceability/test_case_registry.json` (if not exists)

```json
{
  "version": "1.0.0",
  "schema_version": "1.0",
  "description": "Registry of Test Cases with traceability",
  "stage": "ProductSpecs",
  "checkpoint": 6,
  "system_name": "<SystemName>",
  "created_at": "<YYYY-MM-DD>",
  "updated_at": "<YYYY-MM-DD>",
  "traceability_chain": {
    "upstream": ["requirements_registry.json", "module_registry.json", "nfr_registry.json"],
    "downstream": ["jira_registry.json"]
  },
  "items": [],
  "summary": {
    "total_test_cases": 0,
    "by_type": {},
    "by_module": {}
  }
}
```

### Step 6: Initialize Traceability Register

Create or update `traceability/productspecs_traceability_register.json`:

```json
{
  "schema_version": "1.0.0",
  "system_name": "<SystemName>",
  "created_at": "<YYYY-MM-DD>",
  "updated_at": "<YYYY-MM-DD>",
  "discovery_link": {
    "folder": "ClientAnalysis_<SystemName>/",
    "register": "traceability/discovery_traceability_register.json"
  },
  "prototype_link": {
    "folder": "Prototype_<SystemName>/",
    "register": "traceability/prototype_traceability_register.json"
  },
  "artifacts": {
    "modules": [],
    "requirements": [],
    "test_cases": [],
    "api_endpoints": []
  },
  "coverage": {
    "pain_points_addressed": 0,
    "pain_points_total": 0,
    "coverage_percent": 0
  }
}
```

### Step 7: Validate Checkpoint 0

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 0 --dir ProductSpecs_<SystemName>/
```

**Validation Criteria**:
- All folders exist (00-overview, 01-modules, 02-api, 03-tests, 04-jira, feedback-sessions, reports)
- `_state/productspecs_config.json` exists and valid JSON
- `_state/productspecs_progress.json` exists and valid JSON
- ROOT-level `traceability/` folder has registry templates initialized

### Step 8: Update Progress

Update `_state/productspecs_progress.json`:
- Set `phases.init.status` = "completed"
- Set `phases.init.completed_at` = current timestamp
- Set `phases.init.outputs` = list of created files
- Set `current_phase` = 1
- Add validation result to `validation_history`

### Step 9: Display Summary

```
═══════════════════════════════════════════════════════
  PRODUCTSPECS INITIALIZED
═══════════════════════════════════════════════════════

  System:              <SystemName>
  Discovery Source:    ClientAnalysis_<SystemName>/
  Prototype Source:    Prototype_<SystemName>/
  Output:              ProductSpecs_<SystemName>/

  Folders Created:     7
  Registry Files:      4 (in traceability/)
  Traceability:        Linked

  Checkpoint 0:        ✅ PASSED

═══════════════════════════════════════════════════════

  Next Steps:
  • /productspecs <SystemName>     - Run full spec generation
  • /productspecs-validate         - Run Phase 1 only

═══════════════════════════════════════════════════════
```

## Outputs

### Folders Created

```
ProductSpecs_<SystemName>/
├── 00-overview/
├── 01-modules/
├── 02-api/
├── 03-tests/
├── 04-jira/
├── feedback-sessions/
└── reports/
```

### ROOT-Level Registries Initialized (v3.0)

```
traceability/
├── program_registry.json
├── module_registry.json
├── nfr_registry.json
├── test_case_registry.json
└── productspecs_traceability_register.json
```

### State Files Created

| File | Purpose | Location |
|------|---------|----------|
| `productspecs_config.json` | System configuration | `_state/` (ROOT) |
| `productspecs_progress.json` | Phase progress tracking | `_state/` (ROOT) |

### Traceability Updated

| File | Purpose |
|------|---------|
| `traceability/productspecs_traceability_register.json` | ProductSpecs artifacts registry |

## Error Handling

| Error | Action |
|-------|--------|
| Prototype folder missing | **BLOCK** - Display error, exit |
| Required Prototype file missing | **BLOCK** - List missing files, exit |
| Folder creation fails | Log failure, continue with others |
| JSON write fails | **BLOCK** - Cannot proceed without state |

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/productspecs` | Run full spec generation |
| `/productspecs-status` | Show current progress |
| `/productspecs-reset` | Reset and reinitialize |
| `/productspecs-validate` | Validate sources (Phase 1) |
