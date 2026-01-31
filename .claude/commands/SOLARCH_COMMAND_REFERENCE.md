---
description: Complete reference for Solution Architecture stage commands
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /SOLARCH_COMMAND_REFERENCE started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /SOLARCH_COMMAND_REFERENCE ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /SOLARCH_COMMAND_REFERENCE instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Solution Architecture Command Reference

> **Version**: 3.0.0 (Hierarchical Architecture with Architecture Board)
> **Stage**: 4 (Discovery → Prototype → ProductSpecs → **SolArch**)
> **Updated**: 2026-01-27

---

## Overview

The Solution Architecture command system transforms ProductSpecs and Prototype outputs into production-ready architecture documentation following the arc42 template with C4 diagrams, ADRs, and full traceability.

### Pipeline Position

```
Discovery (Stage 1) → Prototype (Stage 2) → ProductSpecs (Stage 3) → SolArch (Stage 4)
        ↓                    ↓                      ↓                      ↓
ClientAnalysis_X/     Prototype_X/          ProductSpecs_X/          SolArch_X/
```

### Prerequisites

- **Prototype Complete**: `Prototype_<SystemName>/` with Checkpoint 14 passed
- **ProductSpecs Complete**: `ProductSpecs_<SystemName>/` with Checkpoint 8 passed
- **Dependencies**: Run `/htec-libraries-init` once

---

## v3.0 Architecture

SolArch v3.0 introduces a **hierarchical multi-agent system** with:

- **Architecture Board**: 3 Architect personas (Pragmatist, Perfectionist, Skeptic)
- **Weighted Voting Consensus**: Decisions with confidence scores
- **Self-Validation**: Per-ADR quality checks (15-point checklist, <15s)
- **4 Entry Points**: System, subsystem, layer, single-ADR
- **Auto-Rework**: Max 2 attempts with OBVIOUS user notification

**Documentation**: `.claude/architecture/workflows/Solution Architecture Phase/SolArch_MultiAgent_Architecture.md`

---

## Quick Start

```bash
# RECOMMENDED: Multi-Agent Mode (35-50% faster, +23% quality)
/solarch-multiagent InventorySystem

# Multi-Agent with entry points
/solarch-multiagent InventorySystem --subsystem authentication  # 66% time savings
/solarch-multiagent InventorySystem --adr ADR-007              # 91% time savings
/solarch-multiagent InventorySystem --quality critical         # All ADRs reviewed

# Sequential Mode (fallback)
/solarch InventorySystem

# Resume from last checkpoint
/solarch-resume
/solarch-multiagent InventorySystem --resume

# Check current progress
/solarch-status
```

---

## Command Summary

### Full Orchestration

| Command | Mode | Description |
|---------|------|-------------|
| **`/solarch-multiagent <SystemName>`** | **Multi-Agent** | **RECOMMENDED: Parallel execution with Architecture Board (35-50% faster, +23% quality)** |
| `/solarch <SystemName>` | Sequential | Complete end-to-end generation (all checkpoints in main session) |
| `/solarch-resume` | Both | Resume from last completed checkpoint |

### Multi-Agent vs Sequential Comparison

| Aspect | `/solarch` (Sequential) | `/solarch-multiagent` (Multi-Agent) |
|--------|-------------------------|-------------------------------------|
| Context Usage | HIGH (all in main session) | LOW (distributed to 28 agents) |
| Execution Time | ~68 min (12 ADRs) | ~35-45 min (-35-50%) |
| Parallelism | None | CP-3 (3 agents), CP-4-9 (board), CP-10 (4 validators) |
| Quality | Good | Better (+23% via Architecture Board) |
| Architecture Board | No | Yes (3 architects vote on each ADR) |
| Auto-Rework | No | Yes (max 2 attempts) |
| User Escalation | No | Yes (when consensus fails) |

### Phase Commands

| Command | Checkpoint | Description |
|---------|------------|-------------|
| `/solarch-init` | 0 | Initialize folders and state |
| `/solarch-validate` | 1 | Validate input completeness **[BLOCKING]** |
| `/solarch-context` | 2 | Generate introduction, constraints, context |
| `/solarch-strategy` | 3 | Generate solution strategy and foundation ADRs |
| `/solarch-blocks` | 4 | Generate building blocks and C4 diagrams |
| `/solarch-runtime` | 5 | Generate runtime scenarios and API design |
| `/solarch-quality` | 6 | Generate quality requirements and security |
| `/solarch-deploy` | 7 | Generate deployment view and operations guide |
| `/solarch-decisions` | 8 | Complete all Architecture Decision Records |
| `/solarch-risks` | 9 | Generate risks and technical debt analysis |
| `/solarch-docs` | 10 | Generate glossary and documentation |
| `/solarch-trace` | 11 | Validate traceability **[BLOCKING]** |
| `/solarch-finalize` | 12 | Generate validation report and summary |

### Utility Commands

| Command | Description |
|---------|-------------|
| `/solarch-status` | Show current progress and state |
| `/solarch-reset` | Reset state (`--soft`, `--hard`, `--phase N`) |
| `/solarch-feedback` | Process stakeholder feedback with impact analysis |

---

## Entry Points (v3.0)

### Four Entry Point Types

| Entry Point | Flag | Example | Scope | Time Savings |
|-------------|------|---------|-------|--------------|
| **System-Level** | (default) | `/solarch InventorySystem` | All ADRs | 0% (baseline) |
| **Subsystem-Level** | `--subsystem` | `--subsystem authentication` | Subsystem ADRs | 66% |
| **Layer-Level** | `--layer` | `--layer frontend` | Layer ADRs | 75% |
| **ADR-Level** | `--adr` | `--adr ADR-007` | Single ADR | 91% |

### Quality Modes

| Mode | Flag | Board Reviews | Use Case |
|------|------|---------------|----------|
| Standard | `--quality standard` | P0 ADRs only | Default, balanced |
| Critical | `--quality critical` | ALL ADRs | High-stakes projects |

### Usage Examples

```bash
# RECOMMENDED: Multi-Agent Mode
# System-level (all ADRs) - spawns 28 agents across checkpoints
/solarch-multiagent InventorySystem

# Multi-Agent: Subsystem-level (66% time savings)
/solarch-multiagent InventorySystem --subsystem authentication

# Multi-Agent: Layer-level (75% time savings)
/solarch-multiagent InventorySystem --layer frontend

# Multi-Agent: Single ADR (91% time savings)
/solarch-multiagent InventorySystem --adr ADR-007

# Multi-Agent: Quality critical (all ADRs get board review)
/solarch-multiagent InventorySystem --quality critical

# Multi-Agent: Combined
/solarch-multiagent InventorySystem --subsystem authentication --quality critical

# Multi-Agent: Resume from failure
/solarch-multiagent InventorySystem --resume

# Multi-Agent: Resume from specific checkpoint
/solarch-multiagent InventorySystem --resume --checkpoint 5

# Sequential Mode (fallback - runs in main session)
/solarch InventorySystem
/solarch InventorySystem --subsystem authentication
/solarch InventorySystem --adr ADR-007
```

---

## Architecture Board (v3.0)

### Three Architect Personas

| Architect | Focus | Personality | Criteria |
|-----------|-------|-------------|----------|
| **Pragmatist** | Scalability, cost, delivery | Practical, cost-conscious | Scalability 30%, Cost 25%, Delivery 25%, Ops 20% |
| **Perfectionist** | Security, compliance | Thorough, risk-averse | OWASP 35%, Data 30%, Auth 20%, Audit 15% |
| **Skeptic** | Maintainability, tech debt | Questions assumptions | Maintainability 35%, Debug 25%, Deps 25%, Principle 15% |

### Consensus Thresholds

- **Confidence threshold**: >= 60% average confidence
- **Dissent threshold**: <= 40% dissent score
- **Escalation trigger**: Either threshold violated → AskUserQuestion

### Auto-Rework Protocol

1. ADR fails self-validation (score < 70)
2. Auto-rework (max 2 attempts)
3. OBVIOUS notification displayed to user
4. If still failing → Escalate to user

### OBVIOUS Notification

When auto-rework occurs:
```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!! AUTO-REWORK ALERT                                  !!
!!                                                   !!
!! ADR-007 required automatic rework (1/2 attempts)  !!
!!                                                   !!
!! Original Issues:                                  !!
!! - Missing decision rationale                      !!
!! - Only 1 alternative considered                   !!
!!                                                   !!
!! Fixes Applied:                                    !!
!! - Added detailed rationale section                !!
!! - Added 2 additional alternatives                 !!
!!                                                   !!
!! PLEASE REVIEW THIS DECISION CAREFULLY             !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

---

## Output Structure

```
project_root/
├── _state/                              # SHARED (ROOT)
│   ├── solarch_config.json
│   ├── solarch_progress.json
│   ├── solarch_input_validation.json
│   └── FAILURES_LOG.md
│
├── traceability/                        # SHARED (ROOT)
│   └── solarch_traceability_register.json
│
└── SolArch_<SystemName>/                # OUTPUT
    ├── 01-introduction-goals/
    │   ├── introduction.md
    │   └── stakeholders.md
    │
    ├── 02-constraints/
    │   ├── business-constraints.md
    │   ├── technical-constraints.md
    │   └── regulatory-constraints.md
    │
    ├── 03-context-scope/
    │   ├── business-context.md
    │   └── technical-context.md
    │
    ├── 04-solution-strategy/
    │   └── solution-strategy.md
    │
    ├── 05-building-blocks/
    │   ├── overview.md
    │   ├── cross-cutting.md
    │   ├── data-model/
    │   │   └── README.md
    │   └── modules/
    │       └── <module-slug>/
    │           ├── README.md
    │           └── c4-component.mermaid
    │
    ├── 06-runtime/
    │   ├── api-design.md
    │   ├── event-communication.md
    │   └── security-architecture.md
    │
    ├── 07-quality/
    │   ├── quality-requirements.md
    │   └── testing-strategy.md
    │
    ├── 08-deployment/
    │   ├── deployment-view.md
    │   ├── operations-guide.md
    │   └── runbooks/
    │       └── RB-*.md
    │
    ├── 09-decisions/
    │   ├── ADR-001-architecture-style.md
    │   ├── ADR-002-technology-stack.md
    │   ├── ADR-003-module-structure.md
    │   ├── ADR-004-data-storage.md
    │   ├── ADR-005-api-design.md
    │   ├── ADR-006-event-communication.md
    │   ├── ADR-007-security-architecture.md
    │   ├── ADR-008-caching-strategy.md
    │   └── ADR-009-observability.md
    │
    ├── 10-risks/
    │   └── risks-technical-debt.md
    │
    ├── 11-glossary/
    │   └── glossary.md
    │
    ├── reports/                            # v3.0: Reports folder
    │   ├── VALIDATION_REPORT.md
    │   └── GENERATION_SUMMARY.md
    │
    │ # NOTE (v3.0): _registry/ DEPRECATED - registries now at ROOT traceability/
    │ # - components.json → traceability/component_registry.json
    │ # - decisions.json → traceability/adr_registry.json
    │ # - architecture-traceability.json → traceability/traceability_matrix_master.json
    │
    ├── diagrams/
    │   ├── c4-context.mermaid
    │   ├── c4-container.mermaid
    │   └── c4-deployment.mermaid
    │
    └── feedback-sessions/
        ├── solarch_feedback_registry.json
        └── <YYYY-MM-DD>_SolArchFeedback-<ID>/
```

---

## Checkpoint Requirements

| CP | Phase | Required Files | Validation | Blocking |
|----|-------|----------------|------------|----------|
| 0 | Init | Config, folders | Structure | No |
| 1 | Validate | Input validation | Complete check | **YES** |
| 2 | Context | Introduction, constraints, context | Content | No |
| 3 | Strategy | Solution strategy, ADR-001, ADR-002 | Content | No |
| 4 | Blocks | Building blocks, modules, C4 | Coverage | No |
| 5 | Runtime | API design, events | Content | No |
| 6 | Quality | Quality reqs, security | Content | No |
| 7 | Deploy | Deployment view, ops guide | Content | No |
| 8 | Decisions | All ADRs, decisions.json | Min 9 ADRs | No |
| 9 | Risks | Risks doc | Content | No |
| 10 | Docs | Glossary | Content | No |
| 11 | Trace | Traceability | 100% coverage | **YES** |
| 12 | Final | Validation report | Complete | No |

### Blocking Checkpoints

**Checkpoint 1 (Validate)**: Cannot proceed without valid inputs from ProductSpecs (CP 8+) and Prototype (CP 14+).

**Checkpoint 11 (Trace)**: Requires:
- 100% Pain Point coverage (all PP-X.X traced to ADRs/components)
- 100% P0 Requirement coverage (all P0 requirements traced)
- 100% Module architecture coverage (all MOD-X traced to components)

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
MOD-XXX (Module Spec)
    ↓
ADR-XXX (Architecture Decision)
    ↓
COMP-XXX (Component)
    ↓
QS-XXX (Quality Scenario)
```

---

## Quality Gates

```bash
# List all checkpoints
python3 .claude/hooks/solarch_quality_gates.py --list-checkpoints

# Validate specific checkpoint
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint N --dir SolArch_X/

# Validate specific file
python3 .claude/hooks/solarch_quality_gates.py --validate-file SolArch_X/09-decisions/ADR-001.md

# Validate traceability
python3 .claude/hooks/solarch_quality_gates.py --validate-traceability --dir SolArch_X/
```

---

## State Management

### Configuration File: `_state/solarch_config.json`

```json
{
  "$schema": "solarch-config-v1",
  "$metadata": {
    "created_at": "ISO8601",
    "updated_at": "ISO8601",
    "version": "1.0.0"
  },
  "system_name": "InventorySystem",
  "prototype_path": "Prototype_InventorySystem",
  "productspecs_path": "ProductSpecs_InventorySystem",
  "output_path": "SolArch_InventorySystem",
  "stage": 4
}
```

### Progress File: `_state/solarch_progress.json`

```json
{
  "$schema": "solarch-progress-v1",
  "$metadata": {
    "created_at": "ISO8601",
    "updated_at": "ISO8601"
  },
  "current_checkpoint": 0,
  "current_phase": "init",
  "started_at": "ISO8601",
  "phases": {
    "init": { "status": "pending", "checkpoint": 0 },
    "validate": { "status": "pending", "checkpoint": 1 },
    "context": { "status": "pending", "checkpoint": 2 },
    "strategy": { "status": "pending", "checkpoint": 3 },
    "blocks": { "status": "pending", "checkpoint": 4 },
    "runtime": { "status": "pending", "checkpoint": 5 },
    "quality": { "status": "pending", "checkpoint": 6 },
    "deploy": { "status": "pending", "checkpoint": 7 },
    "decisions": { "status": "pending", "checkpoint": 8 },
    "risks": { "status": "pending", "checkpoint": 9 },
    "docs": { "status": "pending", "checkpoint": 10 },
    "trace": { "status": "pending", "checkpoint": 11 },
    "final": { "status": "pending", "checkpoint": 12 }
  },
  "validation_history": []
}
```

---

## Detailed Command Reference

### `/solarch <SystemName> [OPTIONS]`

**Purpose**: Complete end-to-end Solution Architecture generation with Architecture Board.

**Arguments**:
- `<SystemName>` - Required. System name (e.g., `InventorySystem`)

**Options (v3.0)**:
| Flag | Description | Example |
|------|-------------|---------|
| `--subsystem <name>` | Filter to subsystem ADRs | `--subsystem authentication` |
| `--layer <name>` | Filter to layer ADRs | `--layer frontend` |
| `--adr <id>` | Single ADR mode | `--adr ADR-007` |
| `--quality <mode>` | Quality mode (`standard`, `critical`) | `--quality critical` |

**Execution (v3.0)**:
1. Parse entry point flags and filter scope
2. Validate prerequisites (Prototype CP 14, ProductSpecs CP 8)
3. Execute checkpoints with Architecture Board review for ADRs
4. Self-validation per ADR (15-point checklist)
5. Weighted voting consensus (escalate to user if needed)
6. Global validation (100% coverage required)

**Examples**:
```bash
# System-level (all ADRs)
/solarch InventorySystem

# Subsystem-level (66% time savings)
/solarch InventorySystem --subsystem authentication

# Single ADR (91% time savings)
/solarch InventorySystem --adr ADR-007

# Quality critical mode
/solarch InventorySystem --quality critical
```

---

### `/solarch-resume`

**Purpose**: Resume generation from last completed checkpoint.

**Arguments**: None (reads from `_state/solarch_config.json`)

**Behavior**:
1. Reads current progress from state files
2. Identifies last completed checkpoint
3. Resumes from next pending checkpoint
4. Supports recovery from failures

**Example**:
```bash
/solarch-resume
```

---

### `/solarch-init <SystemName>`

**Purpose**: Initialize folder structure and state files (Checkpoint 0).

**Prerequisites**: Input folders exist

**Creates**:
- 11 numbered arc42 folders
- `_registry/` with JSON files
- `_state/solarch_config.json`
- `_state/solarch_progress.json`

**Example**:
```bash
/solarch-init InventorySystem
```

---

### `/solarch-validate [SystemName]`

**Purpose**: Validate input completeness (Checkpoint 1) **[BLOCKING]**.

**Validates**:
- ProductSpecs checkpoint >= 8
- Prototype checkpoint >= 14
- Required registry files exist
- Traceability chains present

**Output**: `_state/solarch_input_validation.json`

**Example**:
```bash
/solarch-validate InventorySystem
```

---

### `/solarch-context [SystemName]`

**Purpose**: Generate arc42 sections 1-3 (Checkpoint 2).

**Generates**:
- `01-introduction-goals/` - Introduction, stakeholders
- `02-constraints/` - Business, technical, regulatory constraints
- `03-context-scope/` - Business and technical context

**Example**:
```bash
/solarch-context InventorySystem
```

---

### `/solarch-strategy [SystemName]`

**Purpose**: Generate solution strategy and foundation ADRs (Checkpoint 3).

**Generates**:
- `04-solution-strategy/solution-strategy.md`
- `09-decisions/ADR-001-architecture-style.md`
- `09-decisions/ADR-002-technology-stack.md`

**Skills Used**:
- `SolutionArchitecture_AdrGenerator`

**Example**:
```bash
/solarch-strategy InventorySystem
```

---

### `/solarch-blocks [SystemName]`

**Purpose**: Generate building blocks and C4 diagrams (Checkpoint 4).

**Generates**:
- `05-building-blocks/overview.md`
- `05-building-blocks/modules/<module-slug>/`
- `diagrams/c4-context.mermaid`
- `diagrams/c4-container.mermaid`
- Module-level C4 component diagrams

**Skills Used**:
- `SolutionArchitecture_C4Generator`
- `SolutionArchitecture_InformationDesignGenerator`

**Example**:
```bash
/solarch-blocks InventorySystem
```

---

### `/solarch-runtime [SystemName]`

**Purpose**: Generate runtime scenarios and API design (Checkpoint 5).

**Generates**:
- `06-runtime/api-design.md`
- `06-runtime/event-communication.md`
- `06-runtime/security-architecture.md`

**Skills Used**:
- `SolutionArchitecture_InformationDesignGenerator`
- `SolutionArchitecture_AdrGenerator` (ADR-005, ADR-006, ADR-007)

**Example**:
```bash
/solarch-runtime InventorySystem
```

---

### `/solarch-quality [SystemName]`

**Purpose**: Generate quality requirements and cross-cutting concerns (Checkpoint 6).

**Generates**:
- `07-quality/quality-requirements.md`
- `07-quality/testing-strategy.md`

**Skills Used**:
- `SolutionArchitecture_AdrGenerator` (ADR-008, ADR-009)

**Example**:
```bash
/solarch-quality InventorySystem
```

---

### `/solarch-deploy [SystemName]`

**Purpose**: Generate deployment view and operations guide (Checkpoint 7).

**Generates**:
- `08-deployment/deployment-view.md`
- `08-deployment/operations-guide.md`
- `08-deployment/runbooks/RB-*.md`
- `diagrams/c4-deployment.mermaid`

**Skills Used**:
- `SolutionArchitecture_C4Generator`
- `SolutionArchitecture_AdrGenerator` (ADR-010)

**Example**:
```bash
/solarch-deploy InventorySystem
```

---

### `/solarch-decisions [SystemName]`

**Purpose**: Complete all Architecture Decision Records (Checkpoint 8).

**Generates**:
- Complete set of ADRs (minimum 9)
- `_registry/decisions.json`

**ADR Requirements**:
- Every ADR must trace to at least one Pain Point
- P0 requirements must appear in ADRs
- All modules must be architecturally addressed

**Skills Used**:
- `SolutionArchitecture_AdrGenerator`

**Example**:
```bash
/solarch-decisions InventorySystem
```

---

### `/solarch-risks [SystemName]`

**Purpose**: Generate risks and technical debt analysis (Checkpoint 9).

**Generates**:
- `10-risks/risks-technical-debt.md`

**Example**:
```bash
/solarch-risks InventorySystem
```

---

### `/solarch-docs [SystemName]`

**Purpose**: Generate glossary and documentation (Checkpoint 10).

**Generates**:
- `11-glossary/glossary.md`

**Example**:
```bash
/solarch-docs InventorySystem
```

---

### `/solarch-trace [SystemName]`

**Purpose**: Validate end-to-end traceability (Checkpoint 11) **[BLOCKING]**.

**Validates**:
- 100% Pain Point coverage
- 100% P0 Requirement coverage
- 100% Module architecture coverage

**Skills Used**:
- `SolutionArchitecture_E2ETraceabilityAnalyzer`

**Output**:
- `traceability/solarch_traceability_register.json`
- `_registry/architecture-traceability.json`

**Example**:
```bash
/solarch-trace InventorySystem
```

---

### `/solarch-finalize [SystemName]`

**Purpose**: Generate final validation report and summary (Checkpoint 12).

**Generates**:
- `_registry/VALIDATION_REPORT.md`
- `_registry/GENERATION_SUMMARY.md`

**Example**:
```bash
/solarch-finalize InventorySystem
```

---

### `/solarch-status`

**Purpose**: Display current progress and state.

**Shows**:
- Current checkpoint
- Phase completion status
- Blocking issues
- Next recommended action

**Example**:
```bash
/solarch-status
```

---

### `/solarch-reset [options]`

**Purpose**: Reset state and allow re-generation.

**Options**:
- `--soft` - Reset progress only, keep output files
- `--hard` - Delete all output files and state
- `--phase N` - Reset from checkpoint N onwards

**Example**:
```bash
/solarch-reset --soft
/solarch-reset --hard
/solarch-reset --phase 5
```

---

### `/solarch-feedback`

**Purpose**: Process stakeholder feedback with impact analysis and controlled implementation.

**Workflow**:
1. Input Collection - Receive feedback text or file
2. Impact Analysis - Scan all outputs, classify changes
3. Registration - Assign ID (SF-NNN), create session folder
4. Approval Gate - Approve / Reject / Modify
5. Implementation Planning - Generate 2+ options
6. Implementation - Execute with version tracking
7. Validation - Verify changes and traceability
8. Completion - Generate summary

**Usage**:
```bash
/solarch-feedback                    # Interactive mode
/solarch-feedback "<text>"           # Inline feedback
/solarch-feedback <file.md>          # From file
/solarch-feedback resume SF-001      # Resume failed implementation
```

**Session Structure**:
```
SolArch_X/feedback-sessions/
├── solarch_feedback_registry.json
└── <YYYY-MM-DD>_SolArchFeedback-<ID>/
    ├── FEEDBACK_ORIGINAL.md
    ├── impact_analysis.md
    ├── implementation_options.md
    ├── implementation_plan.md
    ├── implementation_log.md
    ├── files_changed.md
    ├── VALIDATION_REPORT.md
    └── FEEDBACK_SUMMARY.md
```

---

## Skills Reference

### Core Skills

| Skill | Purpose |
|-------|---------|
| `SolutionArchitecture_Generator` | Main orchestration and arc42 generation |
| `SolutionArchitecture_C4Generator` | C4 diagrams (Context, Container, Component, Deployment) |
| `SolutionArchitecture_AdrGenerator` | Architecture Decision Records with traceability |
| `SolutionArchitecture_Arc42Generator` | arc42 section templates and structure |
| `SolutionArchitecture_InformationDesignGenerator` | API contracts, data models, events |
| `SolutionArchitecture_E2ETraceabilityAnalyzer` | End-to-end traceability validation |

### Feedback Skills

| Skill | Purpose |
|-------|---------|
| `SolArch_FeedbackRegister` | Registry management, ID assignment |
| `SolArch_FeedbackAnalyzer` | Impact analysis across outputs |
| `SolArch_FeedbackImplementer` | Change execution with versioning |
| `SolArch_FeedbackValidator` | Implementation validation |

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

## arc42 Section Mapping

| arc42 Section | Folder | Checkpoint | Command |
|---------------|--------|------------|---------|
| 1. Introduction & Goals | `01-introduction-goals/` | 2 | `/solarch-context` |
| 2. Constraints | `02-constraints/` | 2 | `/solarch-context` |
| 3. Context & Scope | `03-context-scope/` | 2 | `/solarch-context` |
| 4. Solution Strategy | `04-solution-strategy/` | 3 | `/solarch-strategy` |
| 5. Building Block View | `05-building-blocks/` | 4 | `/solarch-blocks` |
| 6. Runtime View | `06-runtime/` | 5 | `/solarch-runtime` |
| 7. Deployment View | `08-deployment/` | 7 | `/solarch-deploy` |
| 8. Cross-cutting Concepts | `05-building-blocks/cross-cutting.md` | 6 | `/solarch-quality` |
| 9. Architecture Decisions | `09-decisions/` | 8 | `/solarch-decisions` |
| 10. Quality Requirements | `07-quality/` | 6 | `/solarch-quality` |
| 11. Risks & Technical Debt | `10-risks/` | 9 | `/solarch-risks` |
| 12. Glossary | `11-glossary/` | 10 | `/solarch-docs` |

---

## C4 Diagram Outputs

| Diagram | Location | Generated By |
|---------|----------|--------------|
| Context | `diagrams/c4-context.mermaid` | `/solarch-context`, `/solarch-blocks` |
| Container | `diagrams/c4-container.mermaid` | `/solarch-blocks` |
| Component | `05-building-blocks/modules/<mod>/c4-component.mermaid` | `/solarch-blocks` |
| Deployment | `diagrams/c4-deployment.mermaid` | `/solarch-deploy` |

---

## ADR Catalog

### Foundation ADRs (Always Generated)

| ADR | Title | Checkpoint |
|-----|-------|------------|
| ADR-001 | Architecture Style | 3 |
| ADR-002 | Technology Stack | 3 |
| ADR-003 | Module Structure | 4 |
| ADR-004 | Data Storage | 4 |
| ADR-005 | API Design | 5 |
| ADR-006 | Event Communication | 5 |
| ADR-007 | Security Architecture | 5 |
| ADR-008 | Caching Strategy | 6 |
| ADR-009 | Observability | 6 |
| ADR-010 | Deployment Strategy | 7 |

### Conditional ADRs

| ADR | Trigger | Checkpoint |
|-----|---------|------------|
| ADR-011 | Approval workflows exist | 8 |
| ADR-012 | External integrations | 8 |
| ADR-013 | Real-time requirements | 8 |
| ADR-014 | Offline capability | 8 |
| ADR-015 | Multi-tenancy | 8 |

---

## Examples

### Full Generation

```bash
# Complete Solution Architecture for InventorySystem
/solarch InventorySystem

# Output:
# - SolArch_InventorySystem/ with 11 arc42 sections
# - 9+ ADRs with full traceability
# - C4 diagrams (Context, Container, Component, Deployment)
# - 100% traceability coverage
```

### Incremental Generation

```bash
# Initialize
/solarch-init InventorySystem

# Validate inputs
/solarch-validate

# Generate context (can do multiple runs)
/solarch-context

# Check progress
/solarch-status

# Continue from where you left off
/solarch-resume
```

### Feedback Processing

```bash
# Process feedback interactively
/solarch-feedback

# Process feedback from text
/solarch-feedback "Need to add support for multi-region deployment"

# Process feedback from file
/solarch-feedback architecture-review.md

# Resume failed feedback implementation
/solarch-feedback resume SF-001
```

### Reset and Redo

```bash
# Soft reset (keep files, reset progress)
/solarch-reset --soft

# Hard reset (delete everything)
/solarch-reset --hard

# Reset from specific checkpoint
/solarch-reset --phase 5
```

---

## Troubleshooting

### Blocking at Checkpoint 1

**Cause**: ProductSpecs or Prototype incomplete.

**Fix**:
1. Check ProductSpecs: Must be at Checkpoint 8+
2. Check Prototype: Must be at Checkpoint 14+
3. Complete upstream stages first:
   ```bash
   /productspecs InventorySystem
   /solarch-validate
   ```

### Blocking at Checkpoint 11

**Cause**: Traceability coverage below 100%.

**Fix**:
1. Run `/solarch-trace` to see coverage report
2. Identify missing traces
3. Add ADR/component references for uncovered items
4. Re-run traceability validation

### Missing Dependencies

**Fix**: Run dependency installer:
```bash
/htec-libraries-init
```

### State Corruption

**Fix**: Reset state files:
```bash
/solarch-reset --soft
/solarch-resume
```

---

## Integration with Downstream

Solution Architecture outputs are the final stage before development:

- **ADRs** → Technical decisions for development teams
- **C4 Diagrams** → Visual architecture reference
- **Component Specs** → Implementation guidance
- **API Design** → Interface contracts
- **Deployment View** → Infrastructure requirements

---

## Related Documentation

| Document | Location |
|----------|----------|
| Discovery Commands | `.claude/commands/DISCOVERY_COMMAND_REFERENCE.md` |
| Prototype Commands | `.claude/commands/PROTOTYPE_COMMAND_REFERENCE.md` |
| ProductSpecs Commands | `.claude/commands/PRODUCTSPECS_COMMAND_REFERENCE.md` |
| Error Handling | `helperFils/errorHandling.md` |

---

## Related Documentation (v3.0)

| Document | Location |
|----------|----------|
| Multi-Agent Architecture | `.claude/architecture/workflows/Solution Architecture Phase/SolArch_MultiAgent_Architecture.md` |
| Master Orchestrator | `.claude/agents/solarch-orchestrator.md` |
| ADR Board Orchestrator | `.claude/agents/solarch-adr-board-orchestrator.md` |
| Validation Orchestrator | `.claude/agents/solarch-validation-orchestrator.md` |
| Architect Agents | `.claude/agents/solarch-architect-*.md` |
| Self-Validator | `.claude/agents/solarch-self-validator.md` |
| Agent Registry | `.claude/skills/SOLARCH_AGENT_REGISTRY.json` |

---

**Document Status**: Complete
**Version**: 3.0.0
**Last Updated**: 2026-01-27
