---
name: PROTOTYPE_COMMAND_REFERENCE
description: Complete reference for Prototype stage commands
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /PROTOTYPE_COMMAND_REFERENCE started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /PROTOTYPE_COMMAND_REFERENCE ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /PROTOTYPE_COMMAND_REFERENCE instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Prototype Command Reference

Complete reference for all prototype slash commands.

## Quick Reference

### Main Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `/prototype` | Full prototype generation (all 14 phases) | `<SystemName>` |
| `/prototype-resume` | Resume from last checkpoint | `[SystemName]` |
| `/prototype-status` | Show current progress | `[SystemName]` |

### Phase Commands

| Command | Phases | Description |
|---------|--------|-------------|
| `/prototype-init` | 0 | Initialize folders and state |
| `/prototype-validate` | 1 | Validate Discovery completeness |
| `/prototype-requirements` | 2 | Extract hierarchical requirements |
| `/prototype-data` | 3-5 | Data model, API contracts, test data |
| `/prototype-design` | 6-7 | Design brief and tokens |
| `/prototype-components` | 8 | Component library specs |
| `/prototype-screens` | 9 | Screen specifications |
| `/prototype-interactions` | 10 | Motion, accessibility, responsive |
| `/prototype-build` | 11-12 | Build sequence and code generation |
| `/prototype-qa` | 13-14 | QA testing and UI audit |

### Utility Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `/prototype-feedback` | Process change requests | `[text\|file\|resume CR-NNN]` |
| `/prototype-reset` | Reset progress or delete all | `--soft\|--hard\|--phase N` |
| `/prototype-export` | Export prototype package | `--format full\|specs\|code` |
| `/presentation-slidev` | Generate web-based Slidev presentation | Interactive configuration |

---

## Command Details

### /prototype

Full prototype generation from Discovery outputs.

```
/prototype <SystemName>
/prototype ClientAnalysis_InventorySystem/
```

**Arguments:**
- `<SystemName>` (required) - System name or path to ClientAnalysis folder

**Prerequisites:**
- Completed Discovery: `ClientAnalysis_<SystemName>/` exists
- Dependencies installed: `/htec-libraries-init`
- **Execution Blueprint**: `_state/agent_spawn_manifest.json` must be generated/updated before multi-agent phases.

**Execution Pattern (Plan-First):**
1. **Planning**: Generate `agent_spawn_manifest.json` describing all agents to be spawned.
2. **Orchestration**: Launch agents according to the manifest.
3. **Monitoring**: View "Plan vs Actual" on the i2m Conductor.

**Phases Executed:**
1. Initialize (Checkpoint 0)
2. Validate Discovery (Checkpoint 1)
3. Extract Requirements (Checkpoint 2)
4. Data Model (Checkpoint 3)
5. API Contracts (Checkpoint 4)
6. Test Data (Checkpoint 5)
7. Design Brief (Checkpoint 6)
8. Design Tokens (Checkpoint 7)
9. Components (Checkpoint 8)
10. Screens (Checkpoint 9)
11. Interactions (Checkpoint 10)
12. Build Sequence (Checkpoint 11)
13. Code Generation (Checkpoint 12)
14. QA Testing (Checkpoint 13)
15. UI Audit (Checkpoint 14)

**Outputs:**
- `Prototype_<SystemName>/` with complete prototype

---

### /prototype-init

Initialize prototype folder structure and state files.

```
/prototype-init InventorySystem
```

**Creates:**
```
Prototype_<SystemName>/
├── _state/
│   ├── prototype_config.json
│   ├── prototype_progress.json
│   └── FAILURES_LOG.md
├── 00-foundation/
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
│   └── test-data/
├── 05-validation/
│   └── screenshots/
├── 06-change-requests/
├── prototype/
│   ├── src/
│   └── public/
└── reports/
```

---

### /prototype-status

Display current progress status.

```
/prototype-status
/prototype-status InventorySystem
/prototype-status --verbose
/prototype-status --json
```

**Output:**
- Completed/in-progress/pending phases
- Checkpoint validation status
- Traceability coverage
- Failure count

---

### /prototype-validate

Validate Discovery completeness (Phase 1).

```
/prototype-validate InventorySystem
```

**Validates:**
- Required Discovery files exist
- Personas defined
- Pain points documented
- JTBDs linked
- Screens specified

**Output:**
- `_state/discovery_summary.json`

---

### /prototype-requirements

Extract hierarchical requirements (Phase 2).

```
/prototype-requirements InventorySystem
```

**Transforms:**
- Pain point clusters → Epics
- JTBDs → User Stories
- Links to personas, screens

**Output:**
- `_state/requirements_registry.json`

---

### /prototype-data

Generate data model, API contracts, and test data (Phases 3-5).

```
/prototype-data InventorySystem
```

**Generates:**
- Entity schemas and relationships
- OpenAPI specification
- Test data files (catalog, core, transactional)

**Outputs:**
- `04-implementation/data-model.md`
- `04-implementation/api-contracts.json`
- `04-implementation/test-data/`

---

### /prototype-design

Generate design brief and tokens (Phases 6-7).

```
/prototype-design InventorySystem
```

**Generates:**
- Visual direction and principles
- Color system
- Typography scale
- Spacing system

**Outputs:**
- `00-foundation/design-brief.md`
- `00-foundation/design-principles.md`
- `00-foundation/design-tokens.json`
- `00-foundation/color-system.md`
- `00-foundation/typography.md`
- `00-foundation/spacing-layout.md`

---

### /prototype-components

Generate component library specifications (Phase 8).

```
/prototype-components InventorySystem
```

**Component Categories:**
- Primitives (button, input, select, etc.)
- Data Display (table, card, list, etc.)
- Feedback (alert, toast, progress, etc.)
- Navigation (sidebar, header, tabs, etc.)
- Overlays (modal, drawer, dropdown, etc.)
- Patterns (form, search, data-table, etc.)

**Outputs:**
- `01-components/component-index.md`
- `01-components/[category]/[component].md`

---

### /prototype-screens

Generate screen specifications (Phase 9).

```
/prototype-screens InventorySystem
```

**Per Screen:**
- Layout structure
- Component mapping
- Data requirements
- Interaction flows

**Outputs:**
- `02-screens/screen-index.md`
- `02-screens/[screen]/layout.md`
- `02-screens/[screen]/components.md`
- `02-screens/[screen]/data-requirements.md`
- `02-screens/[screen]/interactions.md`

---

### /prototype-interactions

Generate interaction specifications (Phase 10).

```
/prototype-interactions InventorySystem
```

**Generates:**
- Motion system (animations, transitions)
- Accessibility specification (WCAG AA)
- Responsive behavior

**Outputs:**
- `03-interactions/motion-system.md`
- `03-interactions/accessibility-spec.md`
- `03-interactions/responsive-behavior.md`

---

### /prototype-build

Generate build sequence and code (Phases 11-12).

```
/prototype-build InventorySystem
```

**Phase 11 - Sequencer:**
- Analyze dependencies
- Create build order (DAG)
- Generate implementation prompts

**Phase 12 - Code Generation:**
- Initialize React + Vite project
- Generate component code
- Generate screen code
- Wire up routing

**Outputs:**
- `04-implementation/build-sequence.md`
- `prototype/` (working React app)

---

### /prototype-qa

Run QA testing and UI audit (Phases 13-14).

```
/prototype-qa InventorySystem
```

**Phase 13 - QA Testing:**
- Build verification
- Functional tests
- Requirements coverage
- Accessibility testing

**Phase 14 - UI Audit:**
- Screenshot capture
- Design compliance check
- Generate final reports

**Outputs:**
- `05-validation/qa-report.md`
- `05-validation/ui-audit-report.md`
- `05-validation/screenshots/`
- `reports/ARCHITECTURE.md`
- `reports/README.md`
- `reports/TRACEABILITY_MATRIX.md`

---

### /prototype-feedback

Process change requests with systematic debugging.

```
/prototype-feedback
/prototype-feedback "The stat cards show undefined"
/prototype-feedback ./feedback.md
/prototype-feedback resume CR-003
```

**Workflow:**
1. Input Collection - Receive feedback
2. Impact Analysis - Identify affected files
3. Root Cause Analysis - For bugs (NO FIXES WITHOUT ROOT CAUSE)
4. Approval Gate - User approves or rejects
5. Implementation Planning - Generate options
6. Implementation - Execute changes
7. Validation - Verify fix
8. Closure - Update registry

**Session Outputs:**
```
06-change-requests/<YYYY-MM-DD>_CR_<NNN>/
├── FEEDBACK_ORIGINAL.md
├── IMPACT_ANALYSIS.md
├── ROOT_CAUSE_ANALYSIS.md
├── IMPLEMENTATION_PLAN.md
├── IMPLEMENTATION_LOG.md
├── VALIDATION_REPORT.md
└── CR_SUMMARY.md
```

---

### /prototype-resume

Resume from last checkpoint.

```
/prototype-resume
/prototype-resume InventorySystem
```

**Options:**
- Continue - Resume from failed phase
- Restart Phase - Clear and restart phase
- Skip Phase - Mark as skipped, continue
- Abort - Exit without changes

---

### /prototype-reset

Reset prototype state.

```
/prototype-reset InventorySystem              # Soft reset (default)
/prototype-reset InventorySystem --soft       # Reset progress, keep outputs
/prototype-reset InventorySystem --hard       # Delete everything
/prototype-reset InventorySystem --phase 8    # Reset specific phase
```

**Modes:**
- `--soft` - Reset progress file, keep generated outputs
- `--hard` - Delete entire Prototype folder
- `--phase N` - Reset specific phase only

---

### /prototype-export

Export prototype package for handoff.

```
/prototype-export InventorySystem
/prototype-export InventorySystem --format specs
/prototype-export InventorySystem --format code
/prototype-export InventorySystem --format reports
/prototype-export InventorySystem --output ~/Deliverables/
```

**Formats:**
- `full` - Complete package (default)
- `specs` - Specifications only
- `code` - Working code only
- `reports` - Validation reports only

**Output:**
- `exports/Prototype_<SystemName>_<YYYYMMDD>/`

---

## Quality Gates

Checkpoint validation via hook:

```bash
# List checkpoints
python3 .claude/hooks/prototype_quality_gates.py --list-checkpoints

# Validate checkpoint
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 8 --dir Prototype_X/

# Validate file
python3 .claude/hooks/prototype_quality_gates.py --validate-file path/to/file.json

# Validate traceability
python3 .claude/hooks/prototype_quality_gates.py --validate-traceability --dir Prototype_X/
```

---

## State Files (ROOT Level)

> **⚠️ IMPORTANT**: All state files are stored at **ROOT level** `_state/` folder, NOT inside `Prototype_<SystemName>/`. This is a shared folder used by all pipeline stages.

### _state/prototype_config.json (ROOT)

```json
{
  "schema_version": "1.0.0",
  "system_name": "<SystemName>",
  "created_at": "<YYYY-MM-DD>",
  "discovery_source": "ClientAnalysis_<SystemName>/",
  "output_path": "Prototype_<SystemName>/",
  "framework": "react",
  "styling": "tailwind"
}
```

### _state/prototype_progress.json (ROOT)

```json
{
  "schema_version": "2.3",
  "current_phase": 0,
  "current_checkpoint": 0,
  "phases": {
    "initialize": {"status": "pending", ...},
    "validate_discovery": {"status": "pending", ...},
    ...
  },
  "validation_history": []
}
```

---

## Traceability

### Pain Point → Prototype Chain

```
Discovery                      Prototype
─────────                      ─────────
PP-1.1 (Pain Point)    →    REQ-001 (Requirement)
JTBD-1.1 (Job)         →    US-001 (User Story)
S-1.1 (Screen)         →    SCR-001 (Screen Spec)
                       →    prototype/src/pages/
```

### Traceability Files

- `traceability/prototype_traceability_register.json`
- `_state/requirements_registry.json`
- `reports/TRACEABILITY_MATRIX.md`

---

## Error Handling

**Global Rule:** `ERROR → SKIP → CONTINUE → NEVER RETRY`

| Error | Action |
|-------|--------|
| File read failure | Log `⛔ SKIPPED`, continue |
| Checkpoint fails | Block until fixed |
| Code generation fails | Log, provide manual steps |
| npm build fails | Log in QA report |

**BANNED Actions:**
- ❌ pip install anything
- ❌ Retry failed operations
- ❌ Ask user what to do on error
- ❌ Wait for input after error
