---
name: prototype-init
description: Initialize Prototype folder structure and state files from Discovery
argument-hint: <SystemName>
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-init started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-init ended '{"stage": "prototype"}'
---


# /prototype-init - Initialize Prototype

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-init instruction_start '{"stage": "prototype", "method": "instruction-based"}'
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

- `$ARGUMENTS` - Required: `<SystemName>` or path to `ClientAnalysis_<SystemName>/`

## Prerequisites

- Completed Discovery: `ClientAnalysis_<SystemName>/` exists
- Dependencies installed: `/htec-libraries-init`

## Skills Used

- `.claude/skills/theme-factory/SKILL.md`

## Execution Steps

### Step 1: Parse Arguments

```
If $ARGUMENTS is a path:
  - Extract SystemName from ClientAnalysis_<SystemName>/
If $ARGUMENTS is a name:
  - Use as SystemName
  - Discovery path = ClientAnalysis_<SystemName>/
```

### Step 2: Validate Discovery Exists

Check that Discovery folder exists and contains required files:

```bash
ls ClientAnalysis_<SystemName>/
```

**Required Files** (block if missing):

| File | Purpose |
|------|---------|
| `01-analysis/ANALYSIS_SUMMARY.md` | Analysis outputs |
| `01-analysis/PAIN_POINTS.md` | User pain points |
| `02-research/personas/` | At least one PERSONA_*.md |
| `02-research/JOBS_TO_BE_DONE.md` | JTBD statements |
| `04-design-specs/screen-definitions.md` | Screen specs |
| `04-design-specs/data-fields.md` | Data fields |

If any required file is missing:
```
ERROR: Discovery incomplete. Missing files:
- [list missing files]

Run /discovery-validate on ClientAnalysis_<SystemName>/ first.
```

### Step 3: Create Folder Structure

Create `Prototype_<SystemName>/` with all required folders:

```bash
# NOTE: State files go to ROOT _state/ folder (shared across all phases)
# No local _state/ folder created - all state is centralized

# Foundation with nested structure (data-model, api-contracts, test-data)
mkdir -p Prototype_<SystemName>/00-foundation/data-model/entities
mkdir -p Prototype_<SystemName>/00-foundation/data-model/dictionaries
mkdir -p Prototype_<SystemName>/00-foundation/data-model/constraints
mkdir -p Prototype_<SystemName>/00-foundation/api-contracts/endpoints
mkdir -p Prototype_<SystemName>/00-foundation/api-contracts/examples
mkdir -p Prototype_<SystemName>/00-foundation/api-contracts/mocks
mkdir -p Prototype_<SystemName>/00-foundation/test-data/datasets/catalog
mkdir -p Prototype_<SystemName>/00-foundation/test-data/datasets/core
mkdir -p Prototype_<SystemName>/00-foundation/test-data/datasets/junction
mkdir -p Prototype_<SystemName>/00-foundation/test-data/datasets/transactional
mkdir -p Prototype_<SystemName>/00-foundation/test-data/datasets/personas
mkdir -p Prototype_<SystemName>/00-foundation/test-data/datasets/scenarios
mkdir -p Prototype_<SystemName>/00-foundation/test-data/datasets/combined
mkdir -p Prototype_<SystemName>/00-foundation/test-data/personas

# Components
mkdir -p Prototype_<SystemName>/01-components/primitives
mkdir -p Prototype_<SystemName>/01-components/data-display
mkdir -p Prototype_<SystemName>/01-components/feedback
mkdir -p Prototype_<SystemName>/01-components/navigation
mkdir -p Prototype_<SystemName>/01-components/overlays
mkdir -p Prototype_<SystemName>/01-components/patterns

# Screens
mkdir -p Prototype_<SystemName>/02-screens

# Interactions
mkdir -p Prototype_<SystemName>/03-interactions

# Implementation with phase/checkpoint/prompt structure
mkdir -p Prototype_<SystemName>/04-implementation/sequence
mkdir -p Prototype_<SystemName>/04-implementation/checkpoints
mkdir -p Prototype_<SystemName>/04-implementation/prompts

# Validation with accessibility subfolder
mkdir -p Prototype_<SystemName>/05-validation/screenshots
mkdir -p Prototype_<SystemName>/05-validation/accessibility

# Change requests
mkdir -p Prototype_<SystemName>/06-change-requests

# Prototype code
mkdir -p Prototype_<SystemName>/prototype/src
mkdir -p Prototype_<SystemName>/prototype/public

# Reports
mkdir -p Prototype_<SystemName>/reports
```

### Step 3.5: Select Theme

Use the `theme-factory` skill to help the user select a visual theme for the prototype.

1. **Invoke Theme Factory**:
   - Read `.claude/skills/theme-factory/SKILL.md`
   - Show `theme-showcase.pdf` to the user (if possible/requested)
   - List available themes: Ocean Depths, Sunset Boulevard, Forest Canopy, etc.

2. **Ask User for Theme Selection**:

   USE AskUserQuestion:
     question: "Which visual theme should be applied to this prototype?"
     header: "Theme"
     options:
       - label: "Ocean Depths (Recommended)"
         description: "Professional and calming maritime theme"
       - label: "Modern Minimalist"
         description: "Clean and contemporary grayscale"
       - label: "Tech Innovation"
         description: "Bold and modern tech aesthetic"
       - label: "Botanical Garden"
         description: "Fresh and organic garden colors"

3. **Store Selection**:
   - The selected theme name will be stored in `_state/prototype_config.json` in Step 4.

### Step 3.6: Select Framework

Determine the frontend framework for the prototype.

1. **Check Discovery**:
   - Read Discovery design specs for framework mentions
   - Check if client has specified technology preferences

2. **If no framework specified**, ask user:

   USE AskUserQuestion:
     question: "Which frontend framework should the prototype use?"
     header: "Framework"
     options:
       - label: "React (Recommended)"
         description: "Industry standard, component library support, large ecosystem"
       - label: "Vue"
         description: "Simpler learning curve, good for smaller teams"
       - label: "Vanilla HTML/CSS/JS"
         description: "No framework overhead, maximum simplicity"

3. **Store Selection**:
   - The selected framework will be stored in `_state/prototype_config.json` in Step 4.

### Step 3.7: Select Accessibility Level

Determine the target accessibility compliance level.

1. **Check Industry Context**:
   - Healthcare, government, finance typically require higher standards

2. **Ask user for accessibility target**:

   IF industry in ["healthcare", "government", "finance", "education"]:
     USE AskUserQuestion:
       question: "What WCAG accessibility level should the prototype target?"
       header: "Accessibility"
       options:
         - label: "WCAG 2.1 AA (Recommended)"
           description: "Standard compliance, required by most regulations"
         - label: "WCAG 2.1 AAA"
           description: "Maximum accessibility, longer development time"
         - label: "WCAG 2.1 A (Minimum)"
           description: "Basic compliance only, faster development"
   ELSE:
     DEFAULT to "AA"

3. **Store Selection**:
   - The selected level will be stored in `_state/prototype_config.json` in Step 4.

### Step 4: Initialize State Files

> **⚠️ IMPORTANT**: All state files are stored at **ROOT level** `_state/` folder, NOT inside `Prototype_<SystemName>/`. This is a shared folder used by all pipeline stages (Discovery, Prototype, ProductSpecs, SolArch).

#### `_state/prototype_config.json` (ROOT level)

```json
{
  "schema_version": "1.0.0",
  "system_name": "<SystemName>",
  "created_at": "<YYYY-MM-DD>",
  "discovery_source": "ClientAnalysis_<SystemName>/",
  "output_path": "Prototype_<SystemName>/",
  "framework": "react",
  "styling": "tailwind",
  "theme": "Unspecified",
  "settings": {
    "skip_failures": true,
    "generate_tests": true,
    "accessibility_level": "AA"
  }
}
```

#### `_state/prototype_progress.json`

```json
{
  "schema_version": "2.3",
  "current_phase": 0,
  "current_checkpoint": 0,
  "started_at": "<YYYY-MM-DD HH:MM:SS>",
  "updated_at": "<YYYY-MM-DD HH:MM:SS>",
  "phases": {
    "initialize": {
      "phase_number": 0,
      "status": "in_progress",
      "started_at": "<YYYY-MM-DD HH:MM:SS>",
      "completed_at": null,
      "outputs": []
    },
    "validate_discovery": {
      "phase_number": 1,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "requirements": {
      "phase_number": 2,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "data_model": {
      "phase_number": 3,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "api_contracts": {
      "phase_number": 4,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "test_data": {
      "phase_number": 5,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "design_brief": {
      "phase_number": 6,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "design_tokens": {
      "phase_number": 7,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "components": {
      "phase_number": 8,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "screens": {
      "phase_number": 9,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "interactions": {
      "phase_number": 10,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "sequencer": {
      "phase_number": 11,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "codegen": {
      "phase_number": 12,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "qa": {
      "phase_number": 13,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    },
    "ui_audit": {
      "phase_number": 14,
      "status": "pending",
      "started_at": null,
      "completed_at": null,
      "outputs": []
    }
  },
  "validation_history": []
}
```

#### `_state/FAILURES_LOG.md`

```markdown
# Prototype Failures Log

This file tracks all skipped items during prototype generation.

## Log Format

| Timestamp | Phase | Item | Reason |
|-----------|-------|------|--------|
```

#### `_state/README.md`

Copy from `.claude/skills/Prototype_Builder/state-templates/README.md.template`

This file documents the state file lifecycle and usage for all skills.

#### `_state/requirements_index.json` (Empty Template)

```json
{
  "$schema": "requirements-index-v1",
  "$metadata": {
    "created_at": null,
    "updated_at": null,
    "created_by": "Prototype_Requirements"
  },
  "by_id": {},
  "by_type": {},
  "by_priority": {},
  "by_screen": {},
  "statistics": {}
}
```

#### `_state/jtbd_map.json` (Empty Template)

```json
{
  "$schema": "jtbd-map-v1",
  "$metadata": {
    "created_at": null,
    "created_by": "Prototype_Requirements"
  },
  "jtbd_to_screens": {},
  "coverage": {}
}
```

#### `_state/screen_requirements_map.json` (Empty Template)

```json
{
  "$schema": "screen-requirements-map-v1",
  "$metadata": {
    "created_at": null,
    "created_by": "Prototype_Screens"
  },
  "mappings": {},
  "coverage": {}
}
```

#### `_state/data_model.json` (Empty Template)

```json
{
  "$schema": "data-model-v1",
  "$metadata": {
    "created_at": null,
    "created_by": "Prototype_DataModel"
  },
  "entities": {},
  "relationships": [],
  "statistics": {}
}
```

#### `_state/api_contracts.json` (Empty Template)

```json
{
  "$schema": "api-contracts-v1",
  "$metadata": {
    "created_at": null,
    "created_by": "Prototype_ApiContracts"
  },
  "endpoints": [],
  "statistics": {}
}
```

#### `_state/test_data_manifest.json` (Empty Template)

```json
{
  "$schema": "test-data-manifest-v1",
  "$metadata": {
    "created_at": null,
    "created_by": "Prototype_TestData"
  },
  "datasets": {},
  "statistics": {}
}
```

#### `_state/implementation_sequence.json` (Empty Template)

```json
{
  "$schema": "implementation-sequence-v1",
  "$metadata": {
    "created_at": null,
    "created_by": "Prototype_Sequencer"
  },
  "phases": [],
  "checkpoints": [],
  "build_order": {}
}
```

#### `_state/codegen_state.json` (Empty Template)

```json
{
  "$schema": "codegen-state-v1",
  "$metadata": {
    "created_at": null,
    "created_by": "Prototype_CodeGen"
  },
  "status": "pending",
  "generated": {},
  "pending": {},
  "statistics": {}
}
```

#### `_state/qa_validation_state.json` (Empty Template)

```json
{
  "$schema": "qa-validation-state-v1",
  "$metadata": {
    "created_at": null,
    "created_by": "Prototype_QA"
  },
  "status": "pending",
  "tests": {},
  "coverage": {},
  "issues": {}
}
```

#### `_state/ui_audit_state.json` (Empty Template)

```json
{
  "$schema": "ui-audit-state-v1",
  "$metadata": {
    "created_at": null,
    "created_by": "Prototype_UIAudit"
  },
  "status": "pending",
  "score": 0,
  "issues": []
}
```

#### `_state/change_requests.json` (Empty Template)

```json
{
  "$schema": "change-requests-v1",
  "$metadata": {
    "created_at": null,
    "created_by": "Prototype_ChangeManager"
  },
  "active": [],
  "completed": [],
  "next_id": 1
}
```

#### `_state/PROGRESS.md` (Human Readable)

```markdown
# Prototype Progress: <SystemName>

> Generated: <TIMESTAMP>

## Overall Progress

```
[          ] 0%
```

**Status**: Initializing
**Current Phase**: 0 - Initialize
**Next Action**: Run /prototype-validate

---

## Phase Status

| Phase | Status |
|-------|--------|
| 0. Initialize | ✅ Complete |
| 1. Validate Discovery | ⏳ Pending |
| 2. Requirements | ⏳ Pending |
| ... | ... |

---
```

#### `_state/REQUIREMENTS_REGISTRY.md` (Human Readable)

```markdown
# Requirements Registry

> Generated: <TIMESTAMP>

## Summary

| Type | Count |
|------|-------|
| User Stories | 0 |
| Functional | 0 |
| Non-Functional | 0 |
| Total | 0 |

---

## Requirements by Priority

### P0 (Must Have)
*No requirements extracted yet*

### P1 (Should Have)
*No requirements extracted yet*

### P2 (Nice to Have)
*No requirements extracted yet*

---
```

### Step 5: Initialize Traceability

Create or update `traceability/prototype_traceability_register.json`:

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
  "trace_chains": [],
  "artifacts": {
    "requirements": [],
    "components": [],
    "screens": [],
    "tests": []
  },
  "coverage": {
    "pain_points_addressed": 0,
    "pain_points_total": 0,
    "coverage_percent": 0
  }
}
```

### Step 6: Validate Checkpoint 0

```bash
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 0 --dir Prototype_<SystemName>/
```

**Validation Criteria**:
- All folders exist
- `_state/prototype_config.json` exists and valid JSON
- `_state/prototype_progress.json` exists and valid JSON
- `_state/FAILURES_LOG.md` exists
- `traceability/prototype_traceability_register.json` exists

### Step 7: Update Progress

Update `_state/prototype_progress.json`:
- Set `phases.initialize.status` = "completed"
- Set `phases.initialize.completed_at` = current timestamp
- Set `phases.initialize.outputs` = list of created files
- Set `current_phase` = 1
- Add validation result to `validation_history`

### Step 8: Display Summary

```
═══════════════════════════════════════════════════════
  PROTOTYPE INITIALIZED
═══════════════════════════════════════════════════════

  System:              <SystemName>
  Discovery Source:    ClientAnalysis_<SystemName>/
  Output:              Prototype_<SystemName>/

  Folders Created:     9
  State Files:         3
  Traceability:        Linked

  Checkpoint 0:        ✅ PASSED

═══════════════════════════════════════════════════════

  Next Steps:
  • /prototype <SystemName>      - Run full prototype generation
  • /prototype-validate          - Run Phase 1 only

═══════════════════════════════════════════════════════
```

## Outputs

### Folders Created

```
# ROOT level (shared)
_state/                           ← State files (prototype_config.json, etc.)
traceability/                     ← Traceability registers

# Prototype folder
Prototype_<SystemName>/
├── 00-foundation/
│   ├── data-model/
│   │   ├── entities/
│   │   ├── dictionaries/
│   │   └── constraints/
│   ├── api-contracts/
│   │   ├── endpoints/
│   │   ├── examples/
│   │   └── mocks/
│   └── test-data/
│       ├── datasets/
│       │   ├── catalog/
│       │   ├── core/
│       │   ├── junction/
│       │   ├── transactional/
│       │   ├── personas/
│       │   ├── scenarios/
│       │   └── combined/
│       └── personas/
├── 01-components/
│   ├── primitives/
│   ├── data-display/
│   ├── feedback/
│   ├── navigation/
│   ├── overlays/
│   └── patterns/
├── 02-screens/
├── 03-interactions/
├── 04-implementation/
│   ├── sequence/
│   ├── checkpoints/
│   └── prompts/
├── 05-validation/
│   ├── screenshots/
│   └── accessibility/
├── 06-change-requests/
├── prototype/
│   ├── src/
│   └── public/
└── reports/
```

### State Files Created (ROOT `_state/` folder)

> All state files are at **ROOT level**, shared across all pipeline stages.

| File | Purpose | Populated By |
|------|---------|--------------|
| `_state/README.md` | State file documentation | Initialize |
| `_state/prototype_config.json` | System configuration | Initialize |
| `_state/prototype_progress.json` | Phase progress tracking | All skills |
| `_state/FAILURES_LOG.md` | Skipped items log | All skills |
| `_state/PROGRESS.md` | Human-readable progress | All skills |
| `_state/discovery_summary.json` | Discovery extraction | ValidateDiscovery |
| `traceability/screen_registry.json` | Master screen tracking | ValidateDiscovery |
| `_state/requirements_registry.json` | Requirements registry | Requirements |
| `_state/requirements_index.json` | Fast requirement lookups | Requirements |
| `_state/jtbd_map.json` | JTBD → Screen mapping | Requirements |
| `_state/REQUIREMENTS_REGISTRY.md` | Human-readable registry | Requirements |
| `_state/screen_requirements_map.json` | Screen → Requirements | Screens |
| `_state/data_model.json` | Entity definitions | DataModel |
| `_state/api_contracts.json` | Endpoint registry | ApiContracts |
| `_state/test_data_manifest.json` | Dataset inventory | TestData |
| `_state/implementation_sequence.json` | Build order | Sequencer |
| `_state/codegen_state.json` | Code generation status | CodeGen |
| `_state/qa_validation_state.json` | QA results | QA |
| `_state/ui_audit_state.json` | Visual audit results | UIAudit |
| `_state/change_requests.json` | Active change requests | ChangeManager |

### Traceability Updated

| File | Purpose |
|------|---------|
| `traceability/prototype_traceability_register.json` | Prototype artifacts registry |

## Error Handling

| Error | Action |
|-------|--------|
| Discovery folder missing | **BLOCK** - Display error, exit |
| Required Discovery file missing | **BLOCK** - List missing files, exit |
| Folder creation fails | Log failure, continue with others |
| JSON write fails | **BLOCK** - Cannot proceed without state |

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype` | Run full prototype generation |
| `/prototype-status` | Show current progress |
| `/prototype-reset` | Reset and reinitialize |

## Outputs
