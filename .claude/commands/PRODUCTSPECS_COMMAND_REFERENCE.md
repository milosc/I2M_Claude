---
description: Complete reference for ProductSpecs stage commands
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /PRODUCTSPECS_COMMAND_REFERENCE started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /PRODUCTSPECS_COMMAND_REFERENCE ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /PRODUCTSPECS_COMMAND_REFERENCE instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# ProductSpecs Command Reference

Complete reference for all ProductSpecs slash commands (Stage 3 of the pipeline).

## Overview

ProductSpecs transforms completed Discovery and Prototype outputs into production-ready specifications with full traceability and JIRA export files.

```
Discovery (Stage 1) → Prototype (Stage 2) → ProductSpecs (Stage 3)
        ↓                    ↓                      ↓
ClientAnalysis_X/     Prototype_X/          ProductSpecs_X/
                                                   ↓
                                            JIRA Import Files
```

## Quick Start

```bash
# Complete ProductSpecs generation
/productspecs InventorySystem

# Or run individual phases
/productspecs-init InventorySystem
/productspecs-validate InventorySystem
/productspecs-extract InventorySystem
/productspecs-modules InventorySystem
/productspecs-contracts InventorySystem
/productspecs-tests InventorySystem
/productspecs-finalize InventorySystem
/productspecs-export InventorySystem
```

---

## Command Index

### Main Orchestration

| Command | Description |
|---------|-------------|
| `/productspecs <SystemName>` | Complete end-to-end generation (all phases) |
| `/productspecs-resume` | Resume from last checkpoint |

### Phase Commands

| Command | Phase | Description |
|---------|-------|-------------|
| `/productspecs-init` | 0 | Initialize folders and state |
| `/productspecs-validate` | 1 | Validate Discovery & Prototype completeness |
| `/productspecs-extract` | 2 | Extract requirements hierarchy |
| `/productspecs-modules` | 3-4 | Generate module specifications |
| `/productspecs-contracts` | 5 | Generate API contracts & NFRs |
| `/productspecs-tests` | 6 | Generate test specifications |
| `/productspecs-finalize` | 7 | Validate traceability chains |
| `/productspecs-export` | 8 | Generate JIRA export & documentation |

### Utility Commands

| Command | Description |
|---------|-------------|
| `/productspecs-status` | Show current progress |
| `/productspecs-reset` | Reset state (--soft/--hard/--phase N) |
| `/productspecs-jira` | JIRA export only (quick regeneration) |
| `/productspecs-feedback` | Process change requests |

---

## Detailed Command Reference

### /productspecs

**Full ProductSpecs generation with v2.0 hierarchical orchestration**

```bash
/productspecs <SystemName> [OPTIONS]
```

**Arguments:**
- `SystemName` (required): Name of the system (e.g., InventorySystem)

**Options (v2.0 - Scope Filtering):**
- `--module MOD-XXX` - Process single module
- `--feature FEATURE_NAME` - Process all modules in feature (fuzzy matching supported)
- `--screen SCR-XXX` - Process all modules linked to screen
- `--persona PERSONA_NAME` - Process all modules for persona
- `--subsystem SUBSYSTEM` - Process all modules in subsystem
- `--layer LAYER` - Process all modules in layer (frontend/backend/middleware/database)
- `--quality critical` - Enable VP review for ALL modules (per-module reviews)
- `--from-checkpoint N` - Resume from specific checkpoint

**Prerequisites:**
- Completed Discovery: `ClientAnalysis_<SystemName>/` with Checkpoint 11 passed
- Completed Prototype: `Prototype_<SystemName>/` with Checkpoint 14 passed
- **Execution Blueprint**: `_state/agent_spawn_manifest.json` updated before multi-agent spec generation.

**Execution Pattern (Plan-First with Hierarchical Orchestration):**
1. **Scope Filtering**: Master orchestrator filters modules based on flags
2. **Planning**: Generate manifest of agents for module/test spec generation
3. **Sub-Orchestration**: Delegate to 3 sub-orchestrators (module, test, validation)
4. **Self-Validation**: Each agent validates output with Haiku validator (15 checks)
5. **VP Review**: Auto-trigger for P0 modules and score < 70
6. **Monitoring**: Track "Plan vs Actual" in Conductor

**Outputs:**
- `ProductSpecs_<SystemName>/` folder with all specifications
- JIRA export files ready for import
- Full traceability matrix
- VP review reports for P0 modules (in `_state/vp_reviews/`)

**Examples:**
```bash
# System-level (default) - all modules
/productspecs InventorySystem

# Module-level - single module (80% time savings)
/productspecs InventorySystem --module MOD-INV-SEARCH-01

# Feature-level - all search modules (60-70% savings)
/productspecs InventorySystem --feature SEARCH

# Screen-level - all modules for screen
/productspecs InventorySystem --screen SCR-003

# Persona-level - all modules for admin persona
/productspecs InventorySystem --persona admin

# Layer-level - all frontend modules
/productspecs InventorySystem --layer frontend

# Quality critical - VP review for ALL modules
/productspecs InventorySystem --quality critical

# Resume from checkpoint
/productspecs InventorySystem --from-checkpoint 5
```

**Performance (v2.0):**
| System Size | Time (v1.0) | Time (v2.0) | VP Reviews | Quality Score |
|-------------|-------------|-------------|------------|---------------|
| 10 modules | 12 min | 14 min (+17%) | 0 | 85 (+13%) |
| 20 modules | 16 min | 18 min (+12%) | 0 | 85 (+13%) |
| 50 modules | 21 min | 24 min (+14%) | 0 | 85 (+13%) |

**With Auto-Reflexion (P0 + score < 70):**
| System Size | Time | VP Reviews | Quality Score |
|-------------|------|------------|---------------|
| 10 modules | 17 min | 2 P0 | 92 (+23%) |
| 20 modules | 24 min | 5 P0 + batch | 92 (+23%) |
| 50 modules | 36 min | 10 P0 + batch | 92 (+23%) |

**With --quality critical:**
| System Size | Time | VP Reviews | Quality Score |
|-------------|------|------------|---------------|
| 10 modules | 25 min | 10 per-module | 96 (+28%) |
| 20 modules | 35 min | 20 per-module | 96 (+28%) |
| 50 modules | 60 min | 50 per-module | 96 (+28%) |

---

### /productspecs-resume

**Resume from last checkpoint**

```bash
/productspecs-resume [SystemName] [--from-checkpoint N]
```

**Options:**
- `--from-checkpoint N`: Force resume from specific checkpoint
- `--validate-only`: Just validate current state
- `--skip-validation`: Skip checkpoint validation

**Example:**
```bash
/productspecs-resume
/productspecs-resume InventorySystem --from-checkpoint 5
```

---

### /productspecs-init

**Initialize ProductSpecs folders and state (Phase 0)**

```bash
/productspecs-init <SystemName>
```

**Prerequisites:**
- Project folder initialized: `/htec-traceability-init`
- Prototype Stage complete: `_state/prototype_progress.json` status is "completed"
- **Execution Blueprint**: `_state/agent_spawn_manifest.json` updated for multi-agent spec generation.

**Execution Pattern (Plan-First):**
1. **Planning**: Generate manifest of agents for module/test spec generation.
2. **Orchestration**: Launch ProductSpecs agents.
3. **Monitoring**: Track "Plan vs Actual" in Conductor.

**Checkpoint:** 0

---

### /productspecs-validate

**Validate Discovery & Prototype completeness (Phase 1)**

```bash
/productspecs-validate <SystemName>
```

**Prerequisites:**
- Checkpoint 0 passed

**Validates:**
- Discovery checkpoint 11 passed
- Prototype checkpoint 14 passed
- Required state files exist

**Checkpoint:** 1

---

### /productspecs-extract

**Extract requirements hierarchy (Phase 2)**

```bash
/productspecs-extract <SystemName>
```

**Prerequisites:**
- Checkpoint 1 passed

**Creates:**
- `_registry/requirements.json`
- Requirements with P0/P1/P2 priorities
- Traceability links to Discovery

**Checkpoint:** 2

---

### /productspecs-modules

**Generate module specifications (Phases 3-4)**

```bash
/productspecs-modules <SystemName>
```

**Prerequisites:**
- Checkpoint 2 passed

**Creates:**
- `01-modules/module-index.md`
- `01-modules/MOD-*.md` specifications
- `_registry/modules.json`

**Checkpoints:** 3, 4

---

### /productspecs-contracts

**Generate API contracts & NFRs (Phase 5)**

```bash
/productspecs-contracts <SystemName>
```

**Prerequisites:**
- Checkpoint 4 passed

**Creates:**
- `02-api/api-index.md`
- `02-api/NFR_SPECIFICATIONS.md`
- `02-api/data-contracts.md`
- `_registry/nfrs.json`

**Checkpoint:** 5

---

### /productspecs-tests

**Generate test specifications (Phase 6)**

```bash
/productspecs-tests <SystemName>
```

**Prerequisites:**
- Checkpoint 5 passed

**Creates:**
- `03-tests/test-case-registry.md`
- `03-tests/e2e-scenarios.md`
- `03-tests/accessibility-checklist.md`
- `_registry/test-cases.json`

**Checkpoint:** 6

---

### /productspecs-finalize

**Validate traceability chains (Phase 7)**

```bash
/productspecs-finalize <SystemName>
```

**Prerequisites:**
- Checkpoint 6 passed

**Validates:**
- Complete traceability chains (CM → PP → JTBD → REQ → Screen → Module → Test)
- P0 coverage = 100% (BLOCKING)
- All cross-references valid

**Creates:**
- `00-overview/TRACEABILITY_MATRIX.md`
- `00-overview/VALIDATION_REPORT.md`
- Updated `_registry/traceability.json`

**Checkpoint:** 7 (BLOCKS if P0 < 100%)

---

### /productspecs-export

**Generate JIRA export & documentation (Phase 8)**

```bash
/productspecs-export <SystemName>
```

**Prerequisites:**
- Checkpoint 7 passed

**Prompts for:**
- JIRA Project Key (e.g., INV)
- Project Name
- Sub-task Strategy

**Creates:**
- `04-jira/full-hierarchy.csv`
- `04-jira/epics-and-stories.csv`
- `04-jira/subtasks-only.csv`
- `04-jira/jira-import.json`
- `04-jira/IMPORT_GUIDE.md`
- `00-overview/GENERATION_SUMMARY.md`

**Checkpoint:** 8

---

### /productspecs-status

**Show current progress**

```bash
/productspecs-status [SystemName]
```

**Displays:**
- Current phase and checkpoint
- Phase completion status
- Generated artifacts count
- Validation status

---

### /productspecs-reset

**Reset state**

```bash
/productspecs-reset [SystemName] [options]
```

**Options:**
- `--soft`: Reset progress tracking only (default)
- `--hard`: Delete all ProductSpecs outputs
- `--phase N`: Reset to specific phase

**Examples:**
```bash
/productspecs-reset InventorySystem
/productspecs-reset InventorySystem --hard
/productspecs-reset InventorySystem --phase 5
```

---

### /productspecs-jira

**JIRA export utility (quick regeneration)**

```bash
/productspecs-jira <SystemName> [options]
```

**Options:**
- `--reconfigure`: Force reconfiguration
- `--strategy <strategy>`: Override sub-task strategy
- `--no-subtasks`: Generate without sub-tasks
- `--epics-only`: Generate only epics
- `--priority <P0|P1|P2>`: Filter by priority

**Sub-task Strategies:**
- `by-discipline`: FE, BE, QA, A11Y, DOC, REV (default)
- `by-component`: One per UI component
- `by-acceptance-criteria`: One per AC
- `comprehensive`: All combined

**Examples:**
```bash
/productspecs-jira InventorySystem
/productspecs-jira InventorySystem --reconfigure
/productspecs-jira InventorySystem --strategy by-component
/productspecs-jira InventorySystem --priority P0
```

---

### /productspecs-feedback

**Process change requests**

```bash
/productspecs-feedback [text | file.md | resume PSF-NNN | status | list]
```

**Usage:**
- Interactive: `/productspecs-feedback`
- Inline: `/productspecs-feedback "feedback text"`
- From file: `/productspecs-feedback feedback.md`
- Resume: `/productspecs-feedback resume PSF-001`
- Validate: `/productspecs-feedback validate PSF-001`
- Status: `/productspecs-feedback status`
- List: `/productspecs-feedback list`

**Workflow:**
1. Input Collection
2. Impact Analysis
3. Registration (PSF-NNN)
4. Approval Gate
5. Implementation Planning
6. Implementation
7. Validation
8. Completion

---

## Checkpoint Requirements

| CP | Phase | Required Files | Validation |
|----|-------|----------------|------------|
| 0 | Init | `_state/productspecs_config.json`, folders | JSON schema |
| 1 | Validate | validation report, discovery_summary | Content check |
| 2 | Extract | `_registry/requirements.json` | JSON min items |
| 3 | Modules Core | `01-modules/module-index.md` | File exists |
| 4 | Modules Extended | All screens have module specs | Coverage check |
| 5 | Contracts | `02-api/api-index.md`, NFRs | Content check |
| 6 | Tests | `03-tests/test-case-registry.md` | Content check |
| 7 | Traceability | P0 requirements 100% traced | **BLOCKING** |
| 8 | Export | `04-jira/full-hierarchy.csv` | File exists |

---

## Quality Gates

```bash
# List checkpoints
python3 .claude/hooks/productspecs_quality_gates.py --list-checkpoints

# Validate checkpoint
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint N --dir ProductSpecs_X/

# Validate file
python3 .claude/hooks/productspecs_quality_gates.py --validate-file ProductSpecs_X/01-modules/MOD-INV-SEARCH-01.md

# Validate traceability
python3 .claude/hooks/productspecs_quality_gates.py --validate-traceability --dir ProductSpecs_X/
```

---

## Output Structure

```
project_root/
├── _state/                              # SHARED (ROOT)
│   ├── productspecs_config.json
│   ├── productspecs_progress.json
│   └── FAILURES_LOG.md
│
├── traceability/                        # SHARED (ROOT)
│   └── productspecs_traceability_register.json
│
└── ProductSpecs_<SystemName>/           # OUTPUT
    ├── 00-overview/
    │   ├── MASTER_DEVELOPMENT_PLAN.md
    │   ├── GENERATION_SUMMARY.md
    │   ├── TRACEABILITY_MATRIX.md
    │   └── VALIDATION_REPORT.md
    │
    ├── 01-modules/
    │   ├── module-index.md
    │   └── MOD-<APP>-<FEAT>-<NN>.md
    │
    ├── 02-api/
    │   ├── api-index.md
    │   ├── NFR_SPECIFICATIONS.md
    │   └── data-contracts.md
    │
    ├── 03-tests/
    │   ├── test-case-registry.md
    │   ├── e2e-scenarios.md
    │   └── accessibility-checklist.md
    │
    ├── 04-jira/
    │   ├── jira_config.json
    │   ├── IMPORT_GUIDE.md
    │   ├── full-hierarchy.csv
    │   ├── epics-and-stories.csv
    │   ├── subtasks-only.csv
    │   └── jira-import.json
    │
    ├── _registry/
    │   ├── modules.json
    │   ├── requirements.json
    │   ├── nfrs.json
    │   ├── traceability.json
    │   └── test-cases.json
    │
    └── feedback-sessions/
        ├── productspecs_feedback_registry.json
        └── <YYYY-MM-DD>_ProductSpecsFeedback-<ID>/
```

---

## Traceability Chain

```
CM-XXX (Client Material)
    ↓
PP-X.X (Pain Point)
    ↓
JTBD-X.X (Job To Be Done)
    ↓
REQ-XXX (Requirement)
    ↓
SCR-XXX (Screen)
    ↓
MOD-XXX (Module)
    ↓
TC-XXX (Test Case)
    ↓
INV-XXX (JIRA Item)
```

---

## Skills Reference

| Skill | Purpose |
|-------|---------|
| `ProductSpecs_Validate` | Input validation |
| `ProductSpecs_ExtractRequirements` | Requirements extraction |
| `ProductSpecs_Generator` | Module specification generation |
| `ProductSpecs_NFRGenerator` | SMART NFR generation |
| `ProductSpecs_TestSpecGenerator` | Test specification generation |
| `ProductSpecs_JIRAExporter` | JIRA export generation |
| `ProductSpecs_FeedbackRegister` | Feedback registry management |
| `ProductSpecs_FeedbackAnalyzer` | Impact analysis |
| `ProductSpecs_FeedbackImplementer` | Change implementation |
| `ProductSpecs_FeedbackValidator` | Implementation validation |

---

## Error Handling

```
ERROR → SKIP → CONTINUE → NEVER RETRY
```

- File read fails → Log to `_state/FAILURES_LOG.md`, continue
- Phase fails blocking checkpoint → Stop, require fix
- Phase fails non-blocking → Continue with warnings
- Never pip install, never retry, never ask

---

## Integration with Pipeline

| Stage | Command | Output |
|-------|---------|--------|
| 1. Discovery | `/discovery` | `ClientAnalysis_<SystemName>/` |
| 2. Prototype | `/prototype` | `Prototype_<SystemName>/` |
| 3. ProductSpecs | `/productspecs` | `ProductSpecs_<SystemName>/` |

All stages share:
- `_state/` folder at ROOT level
- `traceability/` folder at ROOT level
- Consistent ID formats
- Cross-stage validation
