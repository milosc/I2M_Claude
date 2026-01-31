# Stage 5: Implementation Architecture Plan

**Version**: 1.0.0
**Created**: 2025-12-24
**Author**: Claude Code
**Status**: PROPOSED
**Purpose**: Extend HTEC ClaudeCode Accelerators Framework with Implementation stage using adapted SDD patterns

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Updated Pipeline Architecture](#2-updated-pipeline-architecture)
3. [Stage 5 Design](#3-stage-5-design)
4. [Command Structure](#4-command-structure)
5. [Agent Architecture](#5-agent-architecture)
6. [Skills Framework](#6-skills-framework)
7. [Hooks and Quality Gates](#7-hooks-and-quality-gates)
8. [State Management](#8-state-management)
9. [Traceability Integration](#9-traceability-integration)
10. [Implementation Roadmap](#10-implementation-roadmap)
11. [Risk Assessment](#11-risk-assessment)

---

## 1. Executive Summary

### 1.1 Problem Statement

The current HTEC ClaudeCode Accelerators framework covers four stages:
1. **Discovery** - Raw materials → Structured documentation
2. **Prototype** - Documentation → Working React demo
3. **ProductSpecs** - Demo → JIRA-ready specifications
4. **SolArch** - Specifications → Architecture documentation (arc42, C4, ADRs)

**The gap**: After SolArch, there is no automated path to production code implementation and testing.

### 1.2 Proposed Solution

Add **Stage 5: Implementation** that:
- Picks up from ProductSpecs modules and SolArch architecture
- Breaks specifications into executable tasks
- Implements features using TDD with parallel agent execution
- Maintains full traceability from Discovery through to deployed code

### 1.3 Design Principles

1. **Registry-First**: All artifacts reference existing traceability registries
2. **Checkpoint-Driven**: Blocking gates at critical transitions
3. **Parallel-Safe**: Tasks marked for parallel execution
4. **TDD-Mandatory**: Tests before implementation
5. **Memory-Augmented**: Learn from each implementation cycle

---

## 2. Updated Pipeline Architecture

### 2.1 Five-Stage Pipeline

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  DISCOVERY   │───▶│  PROTOTYPE   │───▶│ PRODUCT SPEC │───▶│  SOLUTION    │───▶│IMPLEMENTATION│
│   Stage 1    │    │   Stage 2    │    │   Stage 3    │    │ ARCHITECTURE │    │   Stage 5    │
│              │    │              │    │              │    │   Stage 4    │    │              │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
  Raw Materials      Working Demo       Detailed Specs      Tech Blueprint       Production Code
       │                  │                   │                   │                    │
       ▼                  ▼                   ▼                   ▼                    ▼
   ClientAnalysis_*   Prototype_*      ProductSpecs_*       SolArch_*          Implementation_*
```

### 2.2 Stage Handoff Points

| From Stage | To Stage | Handoff Artifacts |
|------------|----------|-------------------|
| Discovery → Prototype | `_state/discovery_summary.json`, `traceability/*.json` |
| Prototype → ProductSpecs | `traceability/screen_registry.json`, `traceability/requirements_registry.json` |
| ProductSpecs → SolArch | `traceability/module_registry.json`, `01-modules/MOD-*.md` |
| **SolArch → Implementation** | `traceability/component_registry.json`, `09-decisions/ADR-*.md`, `ProductSpecs_*/01-modules/MOD-*.md` |

### 2.3 Shared Infrastructure

```
project_root/
├── _state/                              # SHARED (ROOT LEVEL)
│   ├── discovery_config.json
│   ├── prototype_config.json
│   ├── productspecs_config.json
│   ├── solarch_config.json
│   ├── implementation_config.json       # NEW
│   ├── implementation_progress.json     # NEW
│   └── FAILURES_LOG.md
│
├── traceability/                        # SHARED (ROOT LEVEL)
│   ├── ... existing registries ...
│   ├── task_registry.json               # NEW: Implementation tasks
│   ├── implementation_registry.json     # NEW: Code artifacts
│   └── test_registry.json               # NEW: Test results
│
├── ClientAnalysis_<SystemName>/         # Stage 1
├── Prototype_<SystemName>/              # Stage 2
├── ProductSpecs_<SystemName>/           # Stage 3
├── SolArch_<SystemName>/                # Stage 4
└── Implementation_<SystemName>/         # Stage 5 (NEW)
```

---

## 3. Stage 5 Design

### 3.1 Stage Overview

**Input Requirements**:
- ProductSpecs Stage 3 completed (CP8+)
- SolArch Stage 4 completed (CP12+)
- All P0 requirements traced (100% coverage)

**Output Artifacts**:
- Production-ready source code
- Test suites with 100% P0 coverage
- Build artifacts
- Deployment configuration
- Implementation documentation

### 3.2 Checkpoint Structure

| CP | Phase | Required Outputs | Blocking |
|----|-------|------------------|----------|
| 0 | Initialize | `implementation_config.json`, folder structure | No |
| 1 | Validate Inputs | Input validation report | **YES** |
| 2 | Setup Project | Project scaffolding, dependencies | No |
| 3 | Generate Tasks | `tasks/` folder with phase-ordered tasks | No |
| 4 | Review Tasks | Risk assessment, user approval | **YES** |
| 5-N | Implement Phases | Per-phase code + tests | No |
| N+1 | Code Review | Multi-agent review report | No |
| N+2 | Integration Test | E2E test results | No |
| N+3 | Build & Package | Build artifacts | **YES** |
| N+4 | Documentation | Implementation docs | No |
| N+5 | Finalize | Validation report, traceability matrix | No |

### 3.3 Output Structure

```
Implementation_<SystemName>/
├── 00-setup/
│   ├── _readme.md                       # PLACEHOLDER: Explains folder purpose
│   ├── project-scaffold.md              # Project structure decisions
│   ├── dependency-manifest.json         # All dependencies with versions
│   └── environment-config.md            # Environment setup guide
│
├── 01-tasks/
│   ├── _readme.md                       # PLACEHOLDER: Explains folder purpose
│   ├── task-index.md                    # Master task list
│   ├── phase-1-setup/
│   │   └── T001-T00N.md                 # Individual task specs
│   ├── phase-2-foundation/
│   │   └── T0XX-T0XX.md
│   ├── phase-3-US1/                     # One folder per user story
│   │   └── T0XX-T0XX.md
│   ├── phase-N-polish/
│   │   └── T0XX-T0XX.md
│   └── TASK_EXECUTION_LOG.md            # Execution history
│
├── 02-implementation/
│   ├── _readme.md                       # PLACEHOLDER: Explains folder purpose
│   ├── src/                             # Production source code
│   │   ├── components/
│   │   ├── screens/
│   │   ├── services/
│   │   ├── models/
│   │   └── utils/
│   ├── tests/                           # Test suites
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   └── config/                          # Configuration files
│
├── 03-tests/                            # Note: May be 03-review/ in some versions
│   ├── _readme.md                       # PLACEHOLDER: Explains folder purpose
│   ├── code-review-report.md            # Multi-agent review
│   ├── security-audit.md                # Security findings
│   ├── test-coverage-report.md          # Coverage analysis
│   └── refactoring-suggestions.md       # Quality improvements
│
├── 04-reports/                          # Note: May be 04-build/ in some versions
│   ├── _readme.md                       # PLACEHOLDER: Explains folder purpose
│   ├── build-log.md                     # Build execution log
│   ├── artifacts/                       # Build outputs
│   └── deployment-config/               # Deployment manifests
│
├── 05-documentation/
│   ├── _readme.md                       # PLACEHOLDER: Explains folder purpose
│   ├── IMPLEMENTATION_GUIDE.md          # Developer guide
│   ├── API_REFERENCE.md                 # Generated API docs
│   ├── TEST_PLAN.md                     # Test strategy
│   └── RUNBOOK.md                       # Operations guide
│
├── pr-metadata/
│   ├── _readme.md                       # PLACEHOLDER: Explains folder purpose
│   └── PR-{N}-description.md            # PR descriptions with traceability
│
├── reports/
│   ├── _readme.md                       # PLACEHOLDER: Explains folder purpose
│   ├── VALIDATION_REPORT.md
│   ├── TRACEABILITY_MATRIX.md
│   └── IMPLEMENTATION_SUMMARY.md
│
└── feedback-sessions/
    ├── _readme.md                       # PLACEHOLDER: Explains folder purpose
    └── implementation_feedback_registry.json
```

### 3.4 Placeholder Files Convention (MANDATORY)

**Every folder MUST contain a `_readme.md` file**, even if the folder is empty or uses alternative content locations. This ensures:

1. **Discoverability**: Developers can understand what belongs in each folder
2. **Traceability**: Explains which command/phase generates the content
3. **Monorepo Support**: Explains when content lives elsewhere (e.g., `packages/`)

#### Placeholder Generation

**Option 1: At Init Time**
```bash
/htec-sdd-init <SystemName>
# Creates folders and _readme.md placeholders automatically
```

**Option 2: At Checkpoint Validation (Auto)**
```bash
python3 .claude/hooks/implementation_quality_gates.py --validate-checkpoint 0 --dir Implementation_X/
# Auto-creates missing _readme.md files during validation
```

**Option 3: On Demand**
```bash
python3 .claude/hooks/implementation_quality_gates.py --ensure-placeholders --dir Implementation_X/
# Creates placeholders for all empty folders
```

#### Placeholder Content

Each `_readme.md` includes:
- **Status**: Empty reason (e.g., "Pending - Generated by /htec-sdd-implement")
- **Purpose**: What content belongs in this folder
- **Expected Content**: Table of files/folders with generators
- **Generation Command**: How to generate the content
- **Monorepo Note**: Where content lives in monorepo projects

#### Monorepo Pattern

For projects using monorepo structure (e.g., `packages/api`, `packages/web`):

```
Implementation_<SystemName>/
├── 02-implementation/
│   └── _readme.md                       # Explains: "See packages/"
├── packages/
│   ├── api/                             # Backend code
│   │   ├── src/
│   │   └── tests/
│   ├── web/                             # Frontend code
│   │   ├── src/
│   │   └── tests/
│   └── shared/                          # Shared types
└── docker-compose.yml
```

The `02-implementation/_readme.md` placeholder explains where code actually lives.

#### Validation

Check for empty folders without placeholders:
```bash
python3 .claude/hooks/implementation_quality_gates.py --check-empty-folders --dir Implementation_X/
```
```

---

## 4. Command Structure

### 4.1 Command Naming Convention

All Stage 5 commands use the `/htec-sdd-*` prefix to indicate:
- **htec**: HTEC framework namespace
- **sdd**: Spec-Driven Development methodology

### 4.2 Command Hierarchy

```
/htec-sdd                    # Full orchestration (all phases)
├── /htec-sdd-init           # CP0: Initialize
├── /htec-sdd-validate       # CP1: Validate inputs [BLOCKING]
├── /htec-sdd-setup          # CP2: Project setup
├── /htec-sdd-tasks          # CP3: Generate tasks
├── /htec-sdd-review-tasks   # CP4: Review & approve [BLOCKING]
├── /htec-sdd-implement      # CP5-N: Execute implementation
├── /htec-sdd-code-review    # CPN+1: Multi-agent review
├── /htec-sdd-test           # CPN+2: Integration testing
├── /htec-sdd-build          # CPN+3: Build & package [BLOCKING]
├── /htec-sdd-docs           # CPN+4: Documentation
├── /htec-sdd-finalize       # CPN+5: Validation & summary
├── /htec-sdd-status         # Show progress
├── /htec-sdd-resume         # Resume from checkpoint
├── /htec-sdd-reset          # Reset (--soft/--hard/--phase)
└── /htec-sdd-feedback       # Process change requests
```

### 4.3 Command Specifications

#### `/htec-sdd <SystemName>`

**Purpose**: Complete end-to-end implementation pipeline

**Prerequisites**:
- `ProductSpecs_<SystemName>/` exists with CP8+ completed
- `SolArch_<SystemName>/` exists with CP12+ completed

**Execution Flow**:
```
1. Initialize (CP0)
2. Validate Inputs (CP1) [BLOCKING]
3. Setup Project (CP2)
4. Generate Tasks (CP3)
5. Review Tasks (CP4) [BLOCKING - User Approval]
6. For each implementation phase (CP5-N):
   a. Execute phase tasks (parallel where possible)
   b. Run reflexion after phase
   c. Validate phase checkpoint
7. Code Review (CPN+1)
8. Integration Test (CPN+2)
9. Build & Package (CPN+3) [BLOCKING]
10. Documentation (CPN+4)
11. Finalize (CPN+5)
```

---

#### `/htec-sdd-init <SystemName>`

**Purpose**: Initialize implementation session

**Creates**:
```
Implementation_<SystemName>/
├── 00-setup/
├── 01-tasks/
├── 02-implementation/
├── 03-review/
├── 04-build/
├── 05-documentation/
├── reports/
└── feedback-sessions/

_state/
├── implementation_config.json
└── implementation_progress.json
```

**Config Schema**:
```json
{
  "system_name": "InventorySystem",
  "created_at": "2025-12-24T10:00:00Z",
  "source": {
    "productspecs_path": "ProductSpecs_InventorySystem/",
    "solarch_path": "SolArch_InventorySystem/"
  },
  "target": {
    "framework": "react",
    "runtime": "node",
    "test_framework": "vitest"
  },
  "execution": {
    "parallel_enabled": true,
    "max_parallel_agents": 3,
    "tdd_required": true,
    "reflexion_enabled": true
  },
  "current_checkpoint": 0
}
```

---

#### `/htec-sdd-tasks`

**Purpose**: Generate executable task breakdown from module specs

**Input Sources**:
- `ProductSpecs_*/01-modules/MOD-*.md` (module specifications)
- `SolArch_*/09-decisions/ADR-*.md` (architectural decisions)
- `traceability/module_registry.json` (module metadata)
- `traceability/requirements_registry.json` (requirements)

**Task Generation Strategy**:

1. **Phase 1: Setup**
   - Project scaffolding
   - Dependency installation
   - Configuration files
   - Test infrastructure

2. **Phase 2: Foundation**
   - Shared utilities (from ADR-002 tech stack)
   - Base components (from component_registry)
   - Data models (from data-contracts.md)
   - API client setup

3. **Phase 3+: User Stories** (ordered by P0 → P1 → P2)
   - One phase per module priority group
   - Within each phase: Tests → Models → Services → UI → Integration
   - Parallel tasks marked with `[P]`

4. **Final Phase: Polish**
   - Cross-cutting concerns
   - Performance optimization
   - Accessibility compliance
   - Documentation

**Task Format**:
```markdown
# T001: [P] [Setup] Create project structure

## Traceability
- Module: N/A (Infrastructure)
- ADR: ADR-002 (Technology Stack)
- Component: N/A

## Description
Initialize project with Vite + React + TypeScript template

## Acceptance Criteria
- [ ] Project builds successfully
- [ ] TypeScript configured with strict mode
- [ ] ESLint + Prettier configured
- [ ] Test runner (Vitest) configured

## Technical Approach
- Use `npm create vite@latest`
- Add ESLint config from SolArch guidelines
- Configure path aliases from ADR-003

## Dependencies
- None (first task)

## Complexity: Low
## Uncertainty: Low
## Estimated Points: 2

## Definition of Done
- [ ] All AC items checked
- [ ] Build passes
- [ ] Tests pass (if applicable)
- [ ] Code committed
```

---

#### `/htec-sdd-implement [--phase N] [--task T001]`

**Purpose**: Execute implementation tasks

**Modes**:
1. **Full execution**: Run all phases in sequence
2. **Phase execution**: `--phase 3` runs only phase 3
3. **Single task**: `--task T015` runs only that task

**Execution Algorithm**:

```python
for phase in phases:
    # Extract tasks for this phase
    tasks = get_phase_tasks(phase)

    # Separate parallel and sequential tasks
    parallel_tasks = [t for t in tasks if t.has_marker('[P]')]
    sequential_tasks = [t for t in tasks if not t.has_marker('[P]')]

    # Execute sequential tasks first (dependencies)
    for task in sequential_tasks:
        execute_task(task)  # Single developer agent
        mark_complete(task)

    # Execute parallel tasks concurrently
    agents = spawn_parallel_agents(parallel_tasks, max=3)
    wait_for_all(agents)
    for task in parallel_tasks:
        mark_complete(task)

    # Run reflexion after phase
    run_reflexion(phase)

    # Validate phase checkpoint
    validate_checkpoint(phase)
```

**Developer Agent Protocol**:

1. **Load Context**:
   - Read task specification
   - Load relevant module spec (MOD-*.md)
   - Load API contracts
   - Load existing code patterns

2. **TDD Implementation**:
   ```
   For each acceptance criterion:
     1. Write failing test
     2. Implement minimum code to pass
     3. Refactor if needed
     4. Mark AC as complete
   ```

3. **Completion Validation**:
   ```
   - All tests pass (existing + new)
   - All AC items checked
   - No linter errors
   - Code follows project conventions
   ```

4. **Output**:
   ```markdown
   ## Task T015 Complete

   ✅ Implemented: User authentication service
   📁 Files Changed:
     - src/services/auth.ts (created)
     - src/services/auth.test.ts (created)
     - src/types/user.ts (modified)
   ✅ All Tests Passing: 8/8 (100%)
   ✅ Linter Clean: No errors

   ### Acceptance Criteria
   [AC-1] ✅ JWT token generation - auth.ts:45-67
   [AC-2] ✅ Token validation - auth.ts:70-95
   [AC-3] ✅ Refresh token flow - auth.ts:98-130
   ```

---

#### `/htec-sdd-code-review`

**Purpose**: Multi-agent parallel code review

**Agent Team** (6 specialized reviewers):

| Agent | Focus | Weight |
|-------|-------|--------|
| `bug-hunter` | Logic errors, edge cases, null handling | 25% |
| `security-auditor` | OWASP Top 10, auth, secrets | 25% |
| `code-quality` | SOLID, DRY, conventions | 15% |
| `test-coverage` | Missing tests, assertion quality | 15% |
| `contracts-reviewer` | API compliance, type safety | 10% |
| `accessibility-auditor` | WCAG 2.1 AA compliance | 10% |

**Execution**:
```
1. Launch all 6 agents in parallel
2. Each agent reviews all changed files
3. Each returns findings with:
   - Severity (Critical/High/Medium/Low)
   - Location (file:line)
   - Evidence (code snippet)
   - Fix suggestion
   - Confidence score (0-100)

4. Consolidation:
   - Apply confidence threshold (severity-based)
   - Deduplicate cross-agent findings
   - Generate prioritized report

5. Quality Gate:
   - Critical issues = FAIL (must fix)
   - High issues = WARNING (should fix)
   - Medium/Low = INFO (consider)
```

**Output**: `03-review/code-review-report.md`

---

#### `/htec-sdd-feedback`

**Purpose**: Process implementation feedback/change requests

**Workflow**:
```
1. Input: Feedback text/file
2. Impact Analysis:
   - Which tasks affected?
   - Which modules impacted?
   - Traceability chain analysis
3. Root Cause Analysis (for bugs):
   - Five Whys technique
   - Trace through execution path
4. Approval Gate
5. Implementation Planning (2+ options)
6. Execute selected plan
7. Validation & verification
8. Update traceability
```

**Feedback Registry Schema**:
```json
{
  "id": "IF-001",
  "created": "2025-12-24T14:30:00Z",
  "type": "Bug|Feature|Refactor|Performance",
  "status": "Registered|Analyzing|Approved|Implementing|Validating|Completed|Rejected",
  "source": "stakeholder|qa|automated",
  "impact": {
    "tasks_affected": ["T015", "T016"],
    "modules_affected": ["MOD-MOB-TASK-01"],
    "files_affected": ["src/services/auth.ts"]
  },
  "root_cause": "...",
  "selected_plan": "A|B|Custom",
  "implementation_log": []
}
```

---

## 5. Agent Architecture

### 5.1 Agent Categories

| Category | Purpose | Coordination | Model |
|----------|---------|--------------|-------|
| **Planning** | Strategy, research, task breakdown | Sequential within, parallel across | Sonnet |
| **Implementation** | TDD development, E2E testing | Parallel with file locking | Sonnet |
| **Quality** | Code review, security audit | Parallel read-only | Sonnet |
| **Process Integrity** | Continuous monitoring, compliance | Read-only, veto power | Haiku |
| **Reflexion** | Self-assessment, improvement | Sequential per-task | Sonnet |

### 5.2 Agent Taxonomy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATION LAYER                                   │
│    /htec-sdd commands invoke skills which spawn agents                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
     ┌──────────────────────────────┼──────────────────────────────┐
     ▼                              ▼                              ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────────┐
│    PLANNING     │       │ IMPLEMENTATION  │       │      QUALITY        │
│     AGENTS      │       │     AGENTS      │       │      AGENTS         │
├─────────────────┤       ├─────────────────┤       ├─────────────────────┤
│ tech-lead       │       │ developer (x3)  │       │ bug-hunter          │
│ product-        │       │ test-automation-│       │ security-auditor    │
│   researcher    │       │   engineer      │       │ code-quality        │
│ hfe-ux-         │       │                 │       │ test-coverage       │
│   researcher    │       │                 │       │ contracts-reviewer  │
│ code-explorer   │       │                 │       │ a11y-auditor        │
└─────────────────┘       └─────────────────┘       └─────────────────────┘
         │                         │                         │
         └─────────────────────────┼─────────────────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         │               MONITORING LAYER [C]                 │
         │         (Continuous Background Monitoring)         │
         ├───────────────────────────────────────────────────┤
         │  ┌─────────────────┐    ┌─────────────────────┐   │
         │  │PROCESS INTEGRITY│    │    REFLEXION        │   │
         │  │     AGENTS      │    │     JUDGES          │   │
         │  ├─────────────────┤    ├─────────────────────┤   │
         │  │traceability-    │    │ actor               │   │
         │  │  guardian       │    │ evaluator           │   │
         │  │state-watchdog   │    │ self-refiner        │   │
         │  │checkpoint-      │    │                     │   │
         │  │  auditor        │    │                     │   │
         │  │playbook-        │    │                     │   │
         │  │  enforcer       │    │                     │   │
         │  └─────────────────┘    └─────────────────────┘   │
         └───────────────────────────────────────────────────┘
```

### 5.3 Agent Specifications

#### Planning Agents

| Agent | Purpose | Tools | Output |
|-------|---------|-------|--------|
| `tech-lead` | Task decomposition, phase organization | Read, Grep, Write | task_registry.json, T-*.md |
| `product-researcher` | Market analysis, competitor research | WebSearch, WebFetch, Read | MARKET_ANALYSIS.md, COMPETITOR_MATRIX.md |
| `hfe-ux-researcher` | UX patterns, accessibility research | WebSearch, WebFetch, Read | UX_PATTERNS.md, ACCESSIBILITY_GUIDE.md |
| `code-explorer` | Codebase analysis, pattern detection | Grep, Read, Glob | CODEBASE_ANALYSIS.md |

#### Implementation Agents

| Agent | Purpose | Tools | Output |
|-------|---------|-------|--------|
| `developer` | TDD implementation (RED-GREEN-REFACTOR) | Read, Write, Edit, Bash | src/*.ts, tests/*.test.ts |
| `test-automation-engineer` | E2E framework setup, Playwright tests | Read, Write, Bash | tests/e2e/*.spec.ts, playwright.config.ts |

#### Quality Agents

| Agent | Focus | Severity Weight | Tools |
|-------|-------|-----------------|-------|
| `bug-hunter` | Logic errors, null handling, edge cases | 25% | Read, Grep |
| `security-auditor` | OWASP Top 10, auth, secrets | 25% | Read, Grep |
| `code-quality` | SOLID, DRY, complexity | 15% | Read |
| `test-coverage` | Missing tests, assertion quality | 15% | Read, Bash |
| `contracts-reviewer` | API compliance, type safety | 10% | Read, Grep |
| `a11y-auditor` | WCAG 2.1 AA compliance | 10% | Read |

#### Process Integrity Agents

| Agent | Monitors | Frequency | Action on Violation |
|-------|----------|-----------|---------------------|
| `traceability-guardian` | task_registry.json, implementation_registry.json | Real-time | Block write, alert |
| `state-watchdog` | agent_lock.json, agent_sessions.json | Every 60s | Clean stale, alert |
| `checkpoint-auditor` | implementation_progress.json | On transition | Block if incomplete |
| `playbook-enforcer` | TDD compliance, patterns | Per-task | Veto phase advance |

#### Reflexion Judges

| Agent | Purpose | When Invoked |
|-------|---------|--------------|
| `actor` | Generate initial implementation | Start of task |
| `evaluator` | Critique against acceptance criteria | After implementation |
| `self-refiner` | Improve based on evaluation | If evaluation < 7/10 |

### 5.4 Agent Coordination Model

**Phase Execution with Process Integrity Monitoring**:
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PHASE EXECUTION WITH MONITORING                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Phase Start                                                                │
│      │                                                                      │
│      ├─ [I] Process Integrity Pre-Check                                     │
│      │       └─ Verify state files, traceability, lock availability         │
│      │                                                                      │
│      ├─ Sequential Tasks (dependencies)                                     │
│      │   └─ Single developer agent per task                                 │
│      │       └─ [C] Continuous monitoring by state-watchdog                 │
│      │                                                                      │
│      ├─ Parallel Tasks [P]                                                  │
│      │   ├─ Agent 1 ─┐                                                      │
│      │   ├─ Agent 2 ─┼─ Concurrent execution                                │
│      │   └─ Agent 3 ─┘                                                      │
│      │       ├─ File-based locking (agent_lock.json)                        │
│      │       └─ [C] traceability-guardian monitors all writes               │
│      │                                                                      │
│      ├─ Wait for all tasks                                                  │
│      │                                                                      │
│      ├─ [I] playbook-enforcer validates TDD compliance                      │
│      │                                                                      │
│      ├─ Reflexion (self-review of phase output)                             │
│      │                                                                      │
│      └─ [I] checkpoint-auditor validates phase completion                   │
│                                                                             │
│  Legend: [P] Parallel  [I] Integrity Check  [C] Continuous Monitoring       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Parallel Execution Rules**:
1. Tasks marked `[P]` can run in parallel
2. Tasks touching same files must acquire lock first (agent_lock.json)
3. Maximum 3 concurrent developer agents
4. Failure in sequential task = halt phase
5. Failure in parallel task = continue others, report failure
6. Process Integrity agents monitor all phases continuously

**Lock Acquisition Protocol**:
```
1. READ agent_lock.json
2. CHECK for existing lock on target files
3. IF no conflict → ACQUIRE lock (atomic write)
4. IF conflict → WAIT or SKIP based on priority
5. ON completion → RELEASE lock
6. state-watchdog cleans stale locks every 60s
```

### 5.5 Agent Context Inheritance

Each agent receives:
```
1. Project Context:
   - CLAUDE.md (project standards)
   - implementation_config.json
   - Relevant ADRs

2. Task Context:
   - Task specification (T001.md)
   - Module specification (MOD-*.md)
   - API contracts (data-contracts.md)

3. Code Context:
   - Existing source files
   - Test patterns
   - Type definitions

4. Traceability Context:
   - Which pain points this addresses
   - Which requirements this implements
   - Which components this relates to
```

---

## 6. Skills Framework

### 6.1 New Skills for Stage 5

```
.claude/skills/
├── Implementation_Orchestrator/         # Master coordinator
│   └── SKILL.md
├── Implementation_TaskGenerator/        # Task decomposition
│   └── SKILL.md
├── Implementation_Developer/            # TDD implementation
│   └── SKILL.md
├── Implementation_Reviewer/             # Code review orchestration
│   └── SKILL.md
├── Implementation_Reflexion/            # Self-reflection loops
│   └── SKILL.md
├── Implementation_Memorize/             # CLAUDE.md updates
│   └── SKILL.md
├── Implementation_DebugAnalyzer/        # Root cause analysis
│   └── SKILL.md
├── Implementation_FeedbackRegister/     # Feedback management
│   └── SKILL.md
├── Implementation_FeedbackAnalyzer/     # Impact analysis
│   └── SKILL.md
├── Implementation_FeedbackImplementer/  # Change execution
│   └── SKILL.md
├── Implementation_Validator/            # Checkpoint validation
│   └── SKILL.md
│
│ # NEW: Research Agents Skills
├── ProductResearch_MarketAnalysis/      # Market research and trends
│   └── SKILL.md
├── ProductResearch_CompetitorAnalysis/  # Competitor feature matrix
│   └── SKILL.md
├── HFE_UXPatterns/                      # UX pattern research
│   └── SKILL.md
├── HFE_AccessibilityResearch/           # WCAG best practices
│   └── SKILL.md
│
│ # NEW: Test Automation Skills
├── TestAutomation_E2EFramework/         # E2E test framework setup
│   └── SKILL.md
├── TestAutomation_PlaywrightSetup/      # Playwright configuration
│   └── SKILL.md
│
│ # NEW: Process Integrity Skills
├── ProcessIntegrity_TraceabilityGuard/  # Traceability monitoring
│   └── SKILL.md
├── ProcessIntegrity_StateValidation/    # State file validation
│   └── SKILL.md
├── ProcessIntegrity_CheckpointAudit/    # Checkpoint validation
│   └── SKILL.md
└── ProcessIntegrity_PlaybookEnforce/    # Playbook compliance
    └── SKILL.md
```

### 6.2 Skill Specifications

#### `Implementation_TaskGenerator`

**Purpose**: Transform module specs into executable tasks

**Input**:
- `ProductSpecs_*/01-modules/MOD-*.md`
- `SolArch_*/09-decisions/ADR-*.md`
- `traceability/module_registry.json`

**Output**:
- `01-tasks/task-index.md`
- `01-tasks/phase-*/T*.md`
- `traceability/task_registry.json`

**Algorithm**:
```
1. Load all modules ordered by priority (P0 → P1 → P2)
2. Extract user stories from each module
3. For each user story:
   a. Identify data models needed
   b. Identify services needed
   c. Identify UI components needed
   d. Identify API integrations needed
4. Organize into phases:
   - Setup (project init, deps)
   - Foundation (shared code)
   - User Stories (grouped by priority)
   - Polish (cross-cutting)
5. Within each phase:
   - Order by dependency
   - Mark parallelizable tasks with [P]
   - Estimate complexity/uncertainty
6. Generate task specifications
7. Update task_registry.json
```

---

#### `Implementation_Developer`

**Purpose**: Execute individual implementation tasks with TDD

**Protocol**:
```markdown
## Pre-Implementation Checklist
- [ ] Task specification loaded
- [ ] Module spec understood
- [ ] API contracts available
- [ ] Existing patterns identified
- [ ] Test infrastructure ready

## TDD Cycle (per acceptance criterion)
1. RED: Write failing test for AC
2. GREEN: Implement minimum code to pass
3. REFACTOR: Improve without changing behavior
4. VERIFY: All tests pass
5. MARK: AC complete with code reference

## Post-Implementation Checklist
- [ ] All AC items checked with file:line references
- [ ] All tests passing (existing + new)
- [ ] No linter errors
- [ ] Follows project conventions (CLAUDE.md)
- [ ] Traceability updated
```

**Zero Hallucination Rules**:
1. Never invent APIs not in contracts
2. Never assume methods exist - verify with grep
3. Use existing patterns even if suboptimal
4. Ask for clarification rather than guess
5. Cite specific file:line for all claims

---

#### `Implementation_Reflexion`

**Purpose**: Self-review and improve after each phase

**Three-Phase Reflection**:

```markdown
## Phase 1: Assessment
- [ ] Completeness: All tasks in phase done?
- [ ] Quality: Appropriate complexity?
- [ ] Correctness: Logic verified?
- [ ] Facts: Claims supported?

## Phase 2: Refinement (if needed)
- Identify specific issues
- Propose solutions
- Prioritize: Critical → Performance → Style

## Phase 3: Memory Update
- Extract learnable patterns
- Update CLAUDE.md if warranted
- Log lessons in TASK_EXECUTION_LOG.md
```

**Triggers for Deep Reflection**:
- Cyclomatic complexity > 10
- Nested depth > 3 levels
- Function > 50 lines
- Duplicate code detected
- Missing error handling
- Missing tests for critical path

---

#### `Implementation_Reviewer`

**Purpose**: Orchestrate multi-agent code review

**Agent Dispatch**:
```python
def run_code_review():
    # Launch 6 agents in parallel
    agents = [
        spawn_agent("bug-hunter", focus="logic_errors"),
        spawn_agent("security-auditor", focus="vulnerabilities"),
        spawn_agent("code-quality", focus="maintainability"),
        spawn_agent("test-coverage", focus="test_completeness"),
        spawn_agent("contracts-reviewer", focus="api_compliance"),
        spawn_agent("accessibility-auditor", focus="wcag_compliance")
    ]

    # Wait for all to complete
    findings = gather_results(agents)

    # Filter by confidence threshold
    filtered = apply_confidence_filter(findings)

    # Deduplicate cross-agent findings
    deduplicated = deduplicate(filtered)

    # Generate consolidated report
    return generate_report(deduplicated)
```

**Confidence Threshold Table**:
| Severity | Min Confidence |
|----------|----------------|
| Critical | 50% |
| High | 65% |
| Medium | 75% |
| Low | 85% |

---

### 6.3 New Agent Skill Specifications

#### `ProductResearch_MarketAnalysis`

**Purpose**: Research market trends, industry standards, and emerging technologies

**Protocol**:
```markdown
## Research Workflow
1. Identify research topics from module specifications
2. Execute web searches for:
   - Industry best practices
   - Competitor features
   - Market trends
   - Technology comparisons
3. Synthesize findings into structured report
4. Link insights to specific modules/requirements
```

**Output**: `Implementation_*/research/MARKET_ANALYSIS.md`

---

#### `HFE_UXPatterns`

**Purpose**: Research UX patterns and propose human-centered solutions

**Protocol**:
```markdown
## UX Research Workflow
1. Analyze screen specifications from Prototype
2. Research UX patterns for each interaction type:
   - Form patterns
   - Navigation patterns
   - Data visualization
   - Error handling UX
3. Propose multiple solution options per screen
4. Include accessibility considerations
```

**Output**: `Implementation_*/research/UX_PATTERNS.md`, `ACCESSIBILITY_GUIDE.md`

---

#### `TestAutomation_E2EFramework`

**Purpose**: Set up end-to-end testing framework after TDD unit tests complete

**Protocol**:
```markdown
## E2E Framework Setup
1. Analyze completed features and user flows
2. Configure Playwright with project settings
3. Create page object models
4. Generate E2E test scenarios from:
   - User stories (US-*)
   - Acceptance criteria
   - Critical paths
5. Integrate with CI/CD pipeline
```

**Output**: `tests/e2e/*.spec.ts`, `playwright.config.ts`, `pages/*.ts`

---

#### `ProcessIntegrity_TraceabilityGuard`

**Purpose**: Continuously monitor traceability files for compliance

**Protocol**:
```markdown
## Monitoring Rules
1. WATCH: traceability/*.json for changes
2. VALIDATE on each write:
   - Schema compliance
   - ID uniqueness
   - Reference integrity (no orphans)
   - Backward compatibility
3. ON violation:
   - Block the write operation
   - Alert orchestrator
   - Log to VIOLATIONS_LOG.md
```

**Violation Severity**:
| Violation | Severity | Action |
|-----------|----------|--------|
| Schema failure | CRITICAL | Block, halt |
| Duplicate ID | HIGH | Block, alert |
| Orphan reference | MEDIUM | Warn, log |
| Missing optional field | LOW | Log only |

---

#### `ProcessIntegrity_PlaybookEnforce`

**Purpose**: Ensure all agents follow TDD and playbook patterns

**Protocol**:
```markdown
## Enforcement Rules
1. TDD Compliance:
   - Test file MUST exist before production code
   - Test MUST fail first (RED phase logged)
   - Production code MUST make test pass (GREEN phase logged)

2. Pattern Compliance:
   - File naming conventions
   - Import ordering
   - Error handling patterns

3. ON violation:
   - Veto phase advancement
   - Require remediation before proceeding
```

---

### 6.4 Existing Skills Integration

These existing skills are reused:

| Skill | Usage in Stage 5 |
|-------|------------------|
| `systematic-debugging` | Root cause analysis in feedback |
| `root-cause-tracing` | Data flow analysis for bugs |
| `executing-plans` | Controlled batch execution |
| `verification-before-completion` | Final validation |
| `test-driven-development` | TDD enforcement |

---

## 7. Hooks and Quality Gates

### 7.1 Quality Gate Script

**File**: `.claude/hooks/implementation_quality_gates.py`

```python
#!/usr/bin/env python3
"""
Implementation Stage Quality Gates
Validates checkpoints for Stage 5
"""

import argparse
import json
import os
from pathlib import Path

CHECKPOINTS = {
    0: {
        "name": "Initialize",
        "required_files": [
            "_state/implementation_config.json",
            "_state/implementation_progress.json"
        ],
        "blocking": False
    },
    1: {
        "name": "Validate Inputs",
        "required_files": [
            "Implementation_{system}/00-setup/input-validation.md"
        ],
        "validations": [
            "productspecs_complete",
            "solarch_complete",
            "p0_coverage_100"
        ],
        "blocking": True
    },
    2: {
        "name": "Setup Project",
        "required_files": [
            "Implementation_{system}/02-implementation/package.json",
            "Implementation_{system}/00-setup/project-scaffold.md"
        ],
        "validations": ["build_passes"],
        "blocking": False
    },
    3: {
        "name": "Generate Tasks",
        "required_files": [
            "Implementation_{system}/01-tasks/task-index.md",
            "traceability/task_registry.json"
        ],
        "validations": ["all_modules_have_tasks"],
        "blocking": False
    },
    4: {
        "name": "Review Tasks",
        "required_files": [
            "Implementation_{system}/01-tasks/TASK_REVIEW.md"
        ],
        "validations": ["user_approved"],
        "blocking": True
    },
    # Phase checkpoints (5-N) are dynamic
    "build": {
        "name": "Build & Package",
        "required_files": [
            "Implementation_{system}/04-build/build-log.md"
        ],
        "validations": [
            "build_passes",
            "tests_pass",
            "coverage_threshold"
        ],
        "blocking": True
    },
    "final": {
        "name": "Finalize",
        "required_files": [
            "Implementation_{system}/reports/VALIDATION_REPORT.md",
            "Implementation_{system}/reports/TRACEABILITY_MATRIX.md"
        ],
        "validations": ["full_traceability"],
        "blocking": False
    }
}

def validate_checkpoint(checkpoint, system_name, impl_dir):
    """Validate a specific checkpoint"""
    # Implementation details...
    pass

def validate_phase(phase_num, system_name, impl_dir):
    """Validate a phase checkpoint"""
    # Check all tasks in phase are complete
    # Check tests pass
    # Check reflexion ran
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-checkpoint", type=str)
    parser.add_argument("--validate-phase", type=int)
    parser.add_argument("--dir", type=str, required=True)
    parser.add_argument("--system", type=str, required=True)
    parser.add_argument("--list-checkpoints", action="store_true")
    args = parser.parse_args()

    # Execute validation...
```

### 7.2 Checkpoint Validation Rules

**CP1: Validate Inputs (BLOCKING)**
```
Required:
  ✓ ProductSpecs_*/01-modules/ contains at least 1 MOD-*.md
  ✓ SolArch_*/09-decisions/ contains at least 9 ADR-*.md
  ✓ traceability/module_registry.json exists and valid
  ✓ All P0 requirements have module assignment

Blocking: Cannot proceed if any check fails
```

**CP4: Review Tasks (BLOCKING)**
```
Required:
  ✓ task-index.md generated
  ✓ User reviewed high-risk tasks
  ✓ User approved task breakdown
  ✓ Approval recorded in TASK_REVIEW.md

Blocking: Implementation cannot start without approval
```

**Build Checkpoint (BLOCKING)**
```
Required:
  ✓ `npm run build` succeeds
  ✓ All tests pass
  ✓ Test coverage >= 80% (P0 = 100%)
  ✓ No critical linter errors

Blocking: Cannot deploy without successful build
```

### 7.3 Pre-Commit Hook

**File**: `.claude/hooks/pre-commit-implementation.sh`

```bash
#!/bin/bash
# Pre-commit hook for implementation stage

# Run linter
npm run lint || exit 1

# Run tests
npm run test || exit 1

# Check for hardcoded secrets
grep -r "password=" src/ && exit 1
grep -r "api_key=" src/ && exit 1

# Verify traceability comments
# Each file should have traceability header

echo "Pre-commit checks passed"
```

### 7.4 Parallel Agent Coordination Hooks

**File**: `.claude/hooks/agent_coordination.py`

```python
#!/usr/bin/env python3
"""
Parallel Agent Coordination Hooks
Manages file locking and session tracking for multi-agent execution
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

STATE_DIR = Path("_state")
LOCK_FILE = STATE_DIR / "agent_lock.json"
SESSIONS_FILE = STATE_DIR / "agent_sessions.json"

# Timeout configuration (minutes)
LOCK_TIMEOUTS = {
    "developer": 15,
    "code-reviewer": 10,
    "test-automation-engineer": 20,
    "tech-lead": 5,
    "default": 10
}

def pre_agent_spawn(agent_type: str, task_id: str, target_files: list) -> dict:
    """
    Called before spawning any execution agent.
    Returns: {"allowed": bool, "reason": str, "locks_acquired": list}
    """
    # 1. Check active session count
    sessions = load_sessions()
    active_count = sum(1 for s in sessions["active_sessions"]
                       if s["agent_type"] == agent_type and s["status"] == "active")

    max_concurrent = {"developer": 3, "code-reviewer": 6, "default": 2}
    limit = max_concurrent.get(agent_type, max_concurrent["default"])

    if active_count >= limit:
        return {"allowed": False, "reason": f"Max {agent_type} agents reached ({limit})", "locks_acquired": []}

    # 2. Check file locks
    locks = load_locks()
    conflicts = []
    for file_path in target_files:
        existing = find_lock(locks, file_path)
        if existing and not is_expired(existing):
            conflicts.append(f"{file_path} locked by {existing['agent_id']}")

    if conflicts:
        return {"allowed": False, "reason": f"Lock conflicts: {conflicts}", "locks_acquired": []}

    # 3. Check Process Integrity status
    if get_integrity_status() == "BLOCKED":
        return {"allowed": False, "reason": "Process Integrity has blocked execution", "locks_acquired": []}

    # 4. Acquire locks
    acquired = acquire_locks(agent_type, task_id, target_files)

    # 5. Register session
    register_session(agent_type, task_id, target_files)

    return {"allowed": True, "reason": "OK", "locks_acquired": acquired}


def post_task_completion(agent_id: str, task_id: str, result: dict) -> None:
    """
    Called after any agent completes a task.
    """
    # 1. Release all locks held by agent
    release_agent_locks(agent_id)

    # 2. Update session status
    close_session(agent_id, result["status"])

    # 3. Trigger Process Integrity validation
    validate_task_completion(task_id, result)

    # 4. Log completion
    log_task_completion(task_id, result)


def integrity_phase_transition(from_phase: str, to_phase: str) -> dict:
    """
    Called at blocking checkpoints (CP1, CP6).
    Returns: {"allowed": bool, "violations": list, "report": str}
    """
    violations = []

    # 1. Check traceability guardian
    trace_report = check_traceability_integrity()
    if trace_report["violations"]:
        violations.extend(trace_report["violations"])

    # 2. Check playbook enforcer (TDD compliance)
    playbook_report = check_playbook_compliance()
    if playbook_report["violations"]:
        violations.extend(playbook_report["violations"])

    # 3. Check checkpoint auditor
    checkpoint_report = check_checkpoint_requirements(to_phase)
    if checkpoint_report["missing"]:
        violations.extend([f"Missing: {m}" for m in checkpoint_report["missing"]])

    # 4. Determine if blocking
    blocking_severities = ["CRITICAL", "HIGH"]
    blocking_violations = [v for v in violations if v.get("severity") in blocking_severities]

    if blocking_violations:
        return {
            "allowed": False,
            "violations": blocking_violations,
            "report": generate_violation_report(blocking_violations)
        }

    return {"allowed": True, "violations": violations, "report": ""}


def stale_lock_cleanup() -> dict:
    """
    Called every 60 seconds by state-watchdog.
    Returns: {"cleaned": int, "details": list}
    """
    locks = load_locks()
    cleaned = []

    for lock in locks.get("locks", []):
        if is_expired(lock):
            # Check if session is still active
            session = find_session(lock["agent_id"])
            if not session or session["status"] != "active":
                release_lock(lock["file_path"])
                cleaned.append({
                    "file": lock["file_path"],
                    "agent": lock["agent_id"],
                    "reason": "expired_or_orphaned"
                })

    return {"cleaned": len(cleaned), "details": cleaned}

# Helper functions omitted for brevity...
```

### 7.5 Process Integrity Monitoring Hook

**File**: `.claude/hooks/process_integrity_monitor.py`

```python
#!/usr/bin/env python3
"""
Process Integrity Continuous Monitoring
Runs as background process during implementation phase
"""

import time
import json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class TraceabilityGuardian(FileSystemEventHandler):
    """Monitors traceability/*.json for compliance"""

    WATCHED_FILES = [
        "task_registry.json",
        "implementation_registry.json",
        "review_registry.json"
    ]

    def on_modified(self, event):
        if event.is_directory:
            return

        filename = Path(event.src_path).name
        if filename in self.WATCHED_FILES:
            violations = self.validate_file(event.src_path)
            if violations:
                self.report_violations(filename, violations)

    def validate_file(self, file_path):
        """Validate file against schema and integrity rules"""
        violations = []

        try:
            with open(file_path) as f:
                data = json.load(f)

            # Schema validation
            if not self.validate_schema(file_path, data):
                violations.append({"severity": "CRITICAL", "message": "Schema validation failed"})

            # ID uniqueness
            if not self.validate_unique_ids(data):
                violations.append({"severity": "HIGH", "message": "Duplicate IDs detected"})

            # Reference integrity
            orphans = self.find_orphan_references(data)
            if orphans:
                violations.append({"severity": "MEDIUM", "message": f"Orphan refs: {orphans}"})

        except json.JSONDecodeError:
            violations.append({"severity": "CRITICAL", "message": "Invalid JSON"})

        return violations


class StateWatchdog:
    """Monitors agent_lock.json and agent_sessions.json"""

    def run_cleanup_cycle(self):
        """Execute every 60 seconds"""
        # Clean stale locks
        cleaned_locks = self.clean_stale_locks()

        # Clean dead sessions
        cleaned_sessions = self.clean_dead_sessions()

        # Report if any cleanup occurred
        if cleaned_locks or cleaned_sessions:
            self.log_cleanup(cleaned_locks, cleaned_sessions)


class PlaybookEnforcer:
    """Validates TDD compliance per task"""

    def validate_task(self, task_id: str) -> dict:
        """Check task followed TDD protocol"""
        violations = []

        # Get task execution log
        log = self.get_task_log(task_id)

        # Check TDD phases were followed
        if not log.get("red_phase_logged"):
            violations.append({
                "severity": "HIGH",
                "message": f"Task {task_id}: RED phase not logged (test-first violation)"
            })

        if not log.get("green_phase_logged"):
            violations.append({
                "severity": "HIGH",
                "message": f"Task {task_id}: GREEN phase not logged"
            })

        # Check test exists before production code
        if log.get("production_before_test"):
            violations.append({
                "severity": "CRITICAL",
                "message": f"Task {task_id}: Production code written before test"
            })

        return {"task_id": task_id, "compliant": len(violations) == 0, "violations": violations}


def start_monitoring():
    """Start all Process Integrity monitors"""
    observer = Observer()

    # Traceability Guardian
    guardian = TraceabilityGuardian()
    observer.schedule(guardian, "traceability/", recursive=False)

    # Start observer
    observer.start()

    # State Watchdog (runs on timer)
    watchdog = StateWatchdog()

    try:
        while True:
            watchdog.run_cleanup_cycle()
            time.sleep(60)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == "__main__":
    start_monitoring()
```

---

## 8. State Management

### 8.1 Configuration Schema

**`_state/implementation_config.json`**:
```json
{
  "schema_version": "1.0.0",
  "system_name": "InventorySystem",
  "created_at": "2025-12-24T10:00:00Z",
  "updated_at": "2025-12-24T14:30:00Z",

  "source": {
    "productspecs_path": "ProductSpecs_InventorySystem/",
    "productspecs_checkpoint": 8,
    "solarch_path": "SolArch_InventorySystem/",
    "solarch_checkpoint": 12
  },

  "target": {
    "output_path": "Implementation_InventorySystem/",
    "framework": "react",
    "framework_version": "18.2.0",
    "runtime": "node",
    "runtime_version": "20.x",
    "test_framework": "vitest",
    "build_tool": "vite"
  },

  "execution": {
    "parallel_enabled": true,
    "max_parallel_agents": 3,
    "tdd_required": true,
    "reflexion_enabled": true,
    "code_review_enabled": true,
    "min_test_coverage": 80,
    "p0_test_coverage": 100
  },

  "phases": {
    "total": 8,
    "current": 3,
    "completed": [1, 2],
    "phase_names": {
      "1": "Setup",
      "2": "Foundation",
      "3": "US-P0-Core",
      "4": "US-P0-Dashboard",
      "5": "US-P1-Inventory",
      "6": "US-P1-Shipping",
      "7": "US-P2-Config",
      "8": "Polish"
    }
  }
}
```

### 8.2 Progress Tracking

**`_state/implementation_progress.json`**:
```json
{
  "current_checkpoint": 5,
  "current_phase": 3,
  "current_task": "T045",

  "checkpoints": {
    "0": {"status": "completed", "timestamp": "2025-12-24T10:00:00Z"},
    "1": {"status": "completed", "timestamp": "2025-12-24T10:05:00Z"},
    "2": {"status": "completed", "timestamp": "2025-12-24T10:30:00Z"},
    "3": {"status": "completed", "timestamp": "2025-12-24T11:00:00Z"},
    "4": {"status": "completed", "timestamp": "2025-12-24T11:15:00Z"},
    "5": {"status": "in_progress", "started": "2025-12-24T11:20:00Z"}
  },

  "phases": {
    "1": {
      "status": "completed",
      "tasks_total": 10,
      "tasks_completed": 10,
      "tests_passed": 15,
      "tests_failed": 0,
      "reflexion_ran": true
    },
    "2": {
      "status": "completed",
      "tasks_total": 15,
      "tasks_completed": 15,
      "tests_passed": 45,
      "tests_failed": 0,
      "reflexion_ran": true
    },
    "3": {
      "status": "in_progress",
      "tasks_total": 20,
      "tasks_completed": 12,
      "tests_passed": 38,
      "tests_failed": 2,
      "reflexion_ran": false
    }
  },

  "metrics": {
    "total_tasks": 95,
    "completed_tasks": 37,
    "total_tests": 98,
    "passing_tests": 98,
    "test_coverage": 72.5,
    "p0_coverage": 100,
    "lines_of_code": 4523,
    "files_created": 67
  }
}
```

### 8.3 Multi-Agent Coordination Files

#### Agent Lock Registry

**`_state/agent_lock.json`**:
```json
{
  "schema_version": "1.0.0",
  "locks": [
    {
      "file_path": "src/features/inventory/InventoryList.tsx",
      "agent_id": "developer-001",
      "agent_type": "developer",
      "task_id": "T-015",
      "acquired_at": "2025-12-27T10:30:00Z",
      "expires_at": "2025-12-27T10:45:00Z",
      "lock_type": "exclusive"
    }
  ],
  "global_locks": [
    {
      "resource": "traceability/task_registry.json",
      "agent_id": "tech-lead-001",
      "reason": "task_decomposition",
      "acquired_at": "2025-12-27T10:25:00Z"
    }
  ]
}
```

#### Agent Sessions Registry

**`_state/agent_sessions.json`**:
```json
{
  "schema_version": "1.0.0",
  "active_sessions": [
    {
      "session_id": "sess-20251227-001",
      "agent_type": "developer",
      "agent_id": "developer-001",
      "started_at": "2025-12-27T10:00:00Z",
      "current_task": "T-015",
      "current_phase": "GREEN",
      "files_touched": [
        "src/features/inventory/InventoryList.tsx",
        "tests/unit/InventoryList.test.tsx"
      ],
      "status": "active"
    }
  ],
  "completed_sessions": [],
  "failed_sessions": []
}
```

#### Coordination Configuration

**`_state/coordination_config.json`**:
```json
{
  "schema_version": "1.0.0",
  "concurrency": {
    "max_parallel_developers": 3,
    "max_parallel_reviewers": 6,
    "max_total_agents": 12
  },
  "timeouts": {
    "lock_default_minutes": 15,
    "lock_max_minutes": 45,
    "session_max_hours": 4,
    "cleanup_interval_seconds": 60
  },
  "integrity": {
    "monitoring_enabled": true,
    "blocking_severities": ["CRITICAL", "HIGH"],
    "checkpoint_validation": true
  },
  "recovery": {
    "auto_cleanup_enabled": true,
    "backup_interval_minutes": 5,
    "max_retry_attempts": 3
  }
}
```

#### Process Integrity Violations Log

**`_state/VIOLATIONS_LOG.md`**:
```markdown
# Process Integrity Violations Log

## Format
| Timestamp | Agent | Severity | Violation | Action Taken |

## Entries
| 2025-12-27T10:35:00Z | developer-002 | HIGH | TDD RED phase skipped | Task blocked, remediation required |
| 2025-12-27T10:40:00Z | developer-001 | MEDIUM | Orphan reference PP-99 | Warning logged |
```

---

### 8.4 Task Registry

**`traceability/task_registry.json`**:
```json
{
  "schema_version": "1.0.0",
  "total_tasks": 95,
  "tasks": {
    "T001": {
      "id": "T001",
      "phase": 1,
      "name": "Create project structure",
      "status": "completed",
      "parallel": false,
      "user_story": null,
      "module_refs": [],
      "files_created": ["package.json", "vite.config.ts", "tsconfig.json"],
      "tests_created": [],
      "completed_at": "2025-12-24T10:35:00Z",
      "completed_by": "developer-agent-1"
    },
    "T015": {
      "id": "T015",
      "phase": 3,
      "name": "Implement AuthService",
      "status": "completed",
      "parallel": true,
      "user_story": "US-001",
      "module_refs": ["MOD-MOB-AUTH-01"],
      "requirement_refs": ["REQ-001"],
      "pain_point_refs": ["PP-1.1"],
      "files_created": ["src/services/auth.ts", "src/services/auth.test.ts"],
      "tests_created": ["auth.test.ts:8"],
      "acceptance_criteria": {
        "AC-1": {"status": "passed", "location": "auth.ts:45-67"},
        "AC-2": {"status": "passed", "location": "auth.ts:70-95"},
        "AC-3": {"status": "passed", "location": "auth.ts:98-130"}
      },
      "completed_at": "2025-12-24T12:15:00Z",
      "completed_by": "developer-agent-2"
    }
  }
}
```

---

## 9. Traceability Integration

### 9.1 End-to-End Traceability Chain

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        COMPLETE TRACEABILITY CHAIN                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DISCOVERY          PROTOTYPE        PRODUCTSPECS      SOLARCH              │
│  ─────────          ─────────        ────────────      ───────              │
│  CM-XXX ──────────▶ Screen ────────▶ MOD-XXX ────────▶ ADR-XXX             │
│  (Client Material)  (Prototype)      (Module Spec)     (Decision)           │
│       │                │                  │                │                │
│       ▼                ▼                  ▼                ▼                │
│  PP-X.X ──────────▶ REQ-XXX ────────▶ US-XXX ─────────▶ COMP-XXX           │
│  (Pain Point)       (Requirement)    (User Story)      (Component)          │
│       │                │                  │                │                │
│       ▼                ▼                  ▼                ▼                │
│  JTBD-X.X             │             TC-XXX                │                 │
│  (Job-to-be-Done)     │             (Test Case)           │                 │
│                       │                  │                │                │
├───────────────────────┼──────────────────┼────────────────┼─────────────────┤
│                       │                  │                │                │
│  IMPLEMENTATION       │                  ▼                ▼                │
│  ──────────────       │                                                     │
│                       │              ┌───────────────────────┐              │
│                       └─────────────▶│        T-XXX          │              │
│                                      │   (Implementation     │              │
│                                      │        Task)          │              │
│                                      └───────────┬───────────┘              │
│                                                  │                          │
│                                      ┌───────────┴───────────┐              │
│                                      ▼                       ▼              │
│                              ┌───────────────┐     ┌─────────────────┐      │
│                              │   CODE FILE   │     │   TEST FILE     │      │
│                              │ src/*.ts      │     │ *.test.ts       │      │
│                              └───────────────┘     └─────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Traceability in Code

Every source file includes traceability header:

```typescript
/**
 * @file AuthService - User authentication service
 * @module MOD-MOB-AUTH-01
 * @task T015
 * @requirements REQ-001
 * @user-story US-001
 * @pain-points PP-1.1, PP-1.2
 * @adr ADR-007 (Security Architecture)
 * @component COMP-AUTH-001
 */

// Implementation...
```

### 9.3 Implementation Registry

**`traceability/implementation_registry.json`**:
```json
{
  "schema_version": "1.0.0",
  "system_name": "InventorySystem",
  "artifacts": {
    "src/services/auth.ts": {
      "type": "service",
      "task_id": "T015",
      "module_refs": ["MOD-MOB-AUTH-01"],
      "requirement_refs": ["REQ-001"],
      "user_story_refs": ["US-001"],
      "pain_point_refs": ["PP-1.1", "PP-1.2"],
      "adr_refs": ["ADR-007"],
      "component_refs": ["COMP-AUTH-001"],
      "test_files": ["src/services/auth.test.ts"],
      "created_at": "2025-12-24T12:15:00Z",
      "lines_of_code": 145
    }
  },
  "coverage": {
    "pain_points": {
      "total": 21,
      "implemented": 18,
      "percentage": 85.7
    },
    "requirements": {
      "total": 35,
      "implemented": 28,
      "percentage": 80.0
    },
    "p0_requirements": {
      "total": 12,
      "implemented": 12,
      "percentage": 100.0
    }
  }
}
```

### 9.4 Traceability Validation

At each checkpoint, validate:

1. **Forward Traceability** (Discovery → Code):
   - Every P0 pain point has at least one code file
   - Every P0 requirement has implementation
   - Every module has task coverage

2. **Backward Traceability** (Code → Discovery):
   - Every code file references a task
   - Every task references a module/requirement
   - Every test maps to acceptance criteria

3. **Test Traceability**:
   - Every acceptance criterion has a test
   - Every test references its AC
   - P0 test coverage = 100%

---

## 10. Implementation Roadmap

### 10.1 Phase 1: Foundation (Week 1)

**Deliverables**:
- [ ] Create command files in `.claude/commands/`
  - `htec-sdd.md`
  - `htec-sdd-init.md`
  - `htec-sdd-validate.md`
  - `htec-sdd-setup.md`
  - `htec-sdd-tasks.md`
  - `htec-sdd-review-tasks.md`
  - `htec-sdd-status.md`
  - `htec-sdd-reset.md`
  - `htec-sdd-resume.md`

- [ ] Create core skills in `.claude/skills/`
  - `Implementation_Orchestrator/SKILL.md`
  - `Implementation_TaskGenerator/SKILL.md`
  - `Implementation_Validator/SKILL.md`

- [ ] Create quality gate hook
  - `.claude/hooks/implementation_quality_gates.py`

- [ ] Create rule file
  - `.claude/rules/implementation.md`

### 10.2 Phase 2: Implementation Engine (Week 2)

**Deliverables**:
- [ ] Create implementation commands
  - `htec-sdd-implement.md`
  - `htec-sdd-code-review.md`
  - `htec-sdd-test.md`
  - `htec-sdd-build.md`

- [ ] Create implementation skills
  - `Implementation_Developer/SKILL.md`
  - `Implementation_Reviewer/SKILL.md`
  - `Implementation_Reflexion/SKILL.md`
  - `Implementation_Memorize/SKILL.md`

- [ ] Define agent configurations
  - Developer agent template
  - Review agent templates (6 types)

### 10.3 Phase 3: Feedback & Documentation (Week 3)

**Deliverables**:
- [ ] Create feedback commands
  - `htec-sdd-feedback.md`
  - `htec-sdd-docs.md`
  - `htec-sdd-finalize.md`

- [ ] Create feedback skills
  - `Implementation_FeedbackRegister/SKILL.md`
  - `Implementation_FeedbackAnalyzer/SKILL.md`
  - `Implementation_FeedbackImplementer/SKILL.md`
  - `Implementation_DebugAnalyzer/SKILL.md`

### 10.4 Phase 4: Integration & Testing (Week 4)

**Deliverables**:
- [ ] Test with `InventorySystem` data
- [ ] Validate traceability chain
- [ ] Performance optimization
- [ ] Documentation updates
- [ ] Update `HTEC_ClaudeCode_Accelerators_Architecture.md`

---

## 11. Risk Assessment

### 11.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Parallel agent coordination failures | Medium | High | File-based locking, retry logic |
| Task dependency cycles | Low | High | DAG validation in task generator |
| Test infrastructure incompatibility | Medium | Medium | Abstract test runner interface |
| Large codebase context overflow | High | Medium | Chunked processing, summarization |
| Build failures blocking progress | Medium | High | Incremental builds, fallback modes |

### 11.2 Process Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| User approval bottleneck at CP4 | Medium | Medium | Async approval, default approve timer |
| Scope creep during implementation | High | Medium | Strict task boundaries, change request process |
| Traceability gaps | Medium | High | Automated validation at every checkpoint |
| Quality regression | Medium | High | Mandatory code review, test coverage gates |

### 11.3 Integration Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ProductSpecs format changes | Low | Medium | Version check, migration scripts |
| SolArch structure incompatibility | Low | Medium | Adapter layer for ADR/component reading |
| Existing registry corruption | Low | High | Backup before modification, atomic writes |

---

## Appendix A: Command Quick Reference

```bash
# Full pipeline
/htec-sdd InventorySystem

# Individual phases
/htec-sdd-init InventorySystem
/htec-sdd-validate
/htec-sdd-setup
/htec-sdd-tasks
/htec-sdd-review-tasks
/htec-sdd-implement
/htec-sdd-implement --phase 3
/htec-sdd-implement --task T015
/htec-sdd-code-review
/htec-sdd-test
/htec-sdd-build
/htec-sdd-docs
/htec-sdd-finalize

# Utilities
/htec-sdd-status
/htec-sdd-resume
/htec-sdd-reset --soft
/htec-sdd-reset --hard
/htec-sdd-reset --phase 3

# Feedback
/htec-sdd-feedback "Bug description..."
/htec-sdd-feedback ./feedback.md
/htec-sdd-feedback resume IF-001
```

---

## Appendix B: File Structure Summary

```
.claude/
├── commands/
│   ├── htec-sdd.md
│   ├── htec-sdd-init.md
│   ├── htec-sdd-validate.md
│   ├── htec-sdd-setup.md
│   ├── htec-sdd-tasks.md
│   ├── htec-sdd-review-tasks.md
│   ├── htec-sdd-implement.md
│   ├── htec-sdd-code-review.md
│   ├── htec-sdd-test.md
│   ├── htec-sdd-build.md
│   ├── htec-sdd-docs.md
│   ├── htec-sdd-finalize.md
│   ├── htec-sdd-status.md
│   ├── htec-sdd-resume.md
│   ├── htec-sdd-reset.md
│   └── htec-sdd-feedback.md
│
├── skills/
│   ├── Implementation_Orchestrator/
│   ├── Implementation_TaskGenerator/
│   ├── Implementation_Developer/
│   ├── Implementation_Reviewer/
│   ├── Implementation_Reflexion/
│   ├── Implementation_Memorize/
│   ├── Implementation_DebugAnalyzer/
│   ├── Implementation_FeedbackRegister/
│   ├── Implementation_FeedbackAnalyzer/
│   ├── Implementation_FeedbackImplementer/
│   └── Implementation_Validator/
│
├── hooks/
│   └── implementation_quality_gates.py
│
└── rules/
    └── implementation.md
```

---

**Document Version**: 2.0.0
**Last Updated**: 2025-12-27
**Status**: UPDATED - Multi-Agent Architecture Added

---

## Related Documents

| Document | Description |
|----------|-------------|
| `Subagent_Architecture.md` | Master agent taxonomy and coordination patterns |
| `Parallel_Agent_Coordination.md` | Detailed multi-agent coordination protocols |
| `Stage5_Implementation_Diagrams.md` | Visual representations of architecture |
| `Stage5_Implementation_Traceability_Map.md` | Source material traceability |
