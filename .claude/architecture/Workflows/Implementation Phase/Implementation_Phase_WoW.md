# Implementation Phase - Ways of Working (WoW)

**Version**: 2.1.0
**Last Updated**: 2026-01-30
**Status**: Active

---

## Table of Contents

1. [Overview](#1-overview)
2. [Phase Structure](#2-phase-structure)
3. [Command Reference](#3-command-reference)
4. [Agent Architecture](#4-agent-architecture)
5. [TDD Methodology](#5-tdd-methodology)
6. [Multi-Agent Coordination](#6-multi-agent-coordination)
7. [Task Isolation Mode](#7-task-isolation-mode) *(NEW in v2.1)*
8. [Git Worktree Workflow](#8-git-worktree-workflow)
9. [PR Grouping Strategy](#9-pr-grouping-strategy)
10. [Quality Gates](#10-quality-gates)
11. [Change Request Workflow](#11-change-request-workflow)
12. [Traceability Requirements](#12-traceability-requirements)
13. [Best Practices](#13-best-practices)

---

## 1. Overview

### 1.1 Purpose

The Implementation Phase (Stage 5) transforms ProductSpecs module specifications and SolArch architecture decisions into production-ready code using a Test-Driven Development (TDD) approach with multi-agent parallel execution and continuous Process Integrity monitoring.

### 1.2 Key Principles

```
┌────────────────────────────────────────────────────────────────────┐
│                    IMPLEMENTATION PRINCIPLES                       │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  1. REGISTRY-FIRST: All artifacts reference existing traceability  │
│  2. CHECKPOINT-DRIVEN: Blocking gates at critical transitions      │
│  3. PARALLEL-SAFE: Tasks marked for parallel execution             │
│  4. TDD-MANDATORY: Tests before implementation (RED-GREEN-REFACTOR)│
│  5. MEMORY-AUGMENTED: Learn from each implementation cycle         │
│  6. INTEGRITY-MONITORED: Continuous compliance validation          │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 1.3 Prerequisites

**🚀 Framework Initialization (REQUIRED)**

If this is your first time using the HTEC framework:

📖 **Read**: `.claude/architecture/Workflows/FRAMEWORK_ONBOARDING.md`

**Quick setup**:
```bash
# Step 1: Install dependencies
/htec-libraries-init

# Step 2: Initialize project metadata
/project-init

# Step 3: Verify
python3 .claude/hooks/validate_session.py
# Expected: ✅ Session validation passed
```

---

**Before starting Implementation**:
- ✅ **Framework initialized** (session valid, not "pending"/"system")
- ✅ **ProductSpecs Stage 3 completed** (CP8+)
- ✅ **SolArch Stage 4 completed** (CP12+)
- ✅ **All P0 requirements traced** (100% coverage)
- ✅ **Dependencies installed** via `/htec-libraries-init`

### 1.4 Output Artifacts

```
Implementation_<SystemName>/
├── 00-setup/                    # Project scaffolding
├── 01-tasks/                    # Task breakdown & execution log
│   └── <T-ID>/                  # Per-task folder (v2.1+)
│       └── results/             # Task execution results
│           ├── execution.json   # Full execution record
│           ├── implementation_plan.md
│           ├── test_spec.md
│           ├── build.log
│           ├── test.log
│           ├── e2e_test.log
│           ├── quality_report.json
│           └── pr_description.md
├── 02-implementation/           # Source code & tests
├── 03-review/                   # Code review reports
├── 04-build/                    # Build artifacts
├── 05-documentation/            # Implementation docs
├── reports/                     # Validation & traceability
└── feedback-sessions/           # Change request tracking
```

---

## 2. Phase Structure

### 2.1 Checkpoint Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│   CP0    │────▶│   CP1    │────▶│   CP2    │────▶│   CP3    │
│  INIT    │     │ VALIDATE │     │  SETUP   │     │  TASKS   │
│          │     │ [B] [I]  │     │          │     │          │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                      ⚠️  🛡️                             │
                MUST PASS:                              │
                - ProductSpecs CP8+                     │
                - SolArch CP12+                         │
                - P0 Coverage 100%                      │
                                                        ▼
┌──────────┐     ┌──────────────────────────────────────────┐
│   CP4    │◀────│  TASK GENERATION & REVIEW                │
│ APPROVE  │     │  • Phase ordering                        │
│ [B] [I]  │     │  • Dependency mapping                    │
└──────────┘     │  • Parallel markers [P]                  │
    ⚠️  🛡️        │  • Risk assessment                       │
USER APPROVAL    └──────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│         IMPLEMENTATION PHASES (CP5-N)                       │
│         [C] Process Integrity Monitoring Active             │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐      │
│  │ Phase 1 │──▶│ Phase 2 │──▶│ Phase 3 │──▶│ Phase N │      │
│  │ Setup   │   │ Found.  │   │ US-P0   │   │ US-P2   │      │
│  └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘      │
│       │             │             │             │           │
│       ▼             ▼             ▼             ▼           │
│  PER-PHASE WORKFLOW: Execute → Tests → Reflexion            │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  CODE    │────▶│  INTEG   │────▶│  BUILD   │────▶│   DOCS   │
│  REVIEW  │     │   TEST   │     │ [B] [I]  │     │          │
│ [B] [I]  │     │   [I]    │     │          │     │          │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
    ⚠️  🛡️                              ⚠️  🛡️            │
MUST PASS:                        MUST PASS:             │
- No CRITICAL                     - Build success        ▼
- Coverage >80%                   - Tests pass      ┌──────────┐
                                  - Coverage ≥80%   │ FINALIZE │
                                                    │   [I]    │
                                                    └──────────┘

Legend: [B] Blocking  [I] Integrity Check  [C] Continuous Monitoring
```

### 2.2 Phase Breakdown

| Phase | Purpose | Duration | Parallelization |
|-------|---------|----------|-----------------|
| **CP0-CP4** | Initialization & Planning | 30-60 min | Sequential |
| **CP5-N** | Implementation Phases | Variable | High (3 parallel developers) |
| **Code Review** | Multi-agent quality check | 20-30 min | High (6 parallel reviewers) |
| **Integration** | E2E & integration tests | Variable | Sequential |
| **Build & Docs** | Package & document | 20-30 min | Sequential |

---

## 3. Command Reference

### 3.1 Implementation Philosophy

**Narrow Scope, Comprehensive Process**: `/htec-sdd-implement` orchestrates a complete implementation workflow (research → planning → testing → coding → review → documentation → PR prep) but operates on a **narrow scope** (single task or PR group).

**Why Narrow Scope?**
- Fine-grained control over what gets implemented
- Enables parallel development across multiple PRs
- Allows incremental testing and validation
- Supports worktree-based isolation
- Provides clear checkpoint progression

**Comprehensive Orchestration** (within narrow scope):
```
/htec-sdd-implement orchestrates 8 phases per task:
  Phase 1: Codebase Research (planning-code-explorer)
  Phase 2: Implementation Planning (planning-tech-lead)
  Phase 3: Test Design (implementation-test-designer)
  Phase 4: TDD Implementation (implementation-developer)
  Phase 5: Test Automation (implementation-test-automation-engineer)
  Phase 6: Quality Review (5 agents in parallel)
  Phase 7: Documentation & PR Prep (documenter, pr-preparer)
  Phase 8: Finalization (registry updates, traceability)
```

**Typical Workflow (Greenfield Project with ProductSpecs)**:
```bash
# Stage 3: ProductSpecs generates JIRA tasks (Epics, Stories, Sub-tasks)
/productspecs InventorySystem
# Output: ProductSpecs_InventorySystem/04-jira/jira-import.json

# Stage 5 Setup: Reuse ProductSpecs tasks (CP0-CP4)
/htec-sdd-tasks InventorySystem
# Detects jira-import.json → Reuses Epics/Stories/Sub-tasks as T-NNN tasks
# Creates: traceability/task_registry.json

# OR (Brownfield/No ProductSpecs): Generate tasks from scratch
/htec-sdd-tasks InventorySystem
# No jira-import.json → Generates tasks from ProductSpecs_*/01-modules/MOD-*.md
# Creates: traceability/task_registry.json

# Setup worktrees for parallel development
/htec-sdd-worktree-setup InventorySystem

# Comprehensive implementation (CP5-N, all 8 phases)
cd ../worktrees/pr-001-auth
/htec-sdd-implement InventorySystem --task T-001  # Single task, full orchestration
/htec-sdd-implement InventorySystem --pr-group PR-001  # PR group, full orchestration
/htec-sdd-implement InventorySystem  # Auto-detects PR-001, full orchestration

# Additional integration tests (if needed)
/htec-sdd-integrate
```

**Typical Command Sequence**:
```
/productspecs <SystemName>           # Stage 3: Generate specifications & JIRA tasks
    ↓
/htec-sdd-tasks <SystemName>         # Stage 5 CP0-CP4: Task registry (reuse or generate)
    ↓
/htec-sdd-implement <SystemName>     # Stage 5 CP5-N: Execute implementation
    --task T-001                     # (granular: single task)
    --pr-group PR-001                # (grouped: PR scope)
```

**CP0-CP4 vs CP5-N**:
- **CP0-CP4**: Prerequisites handled by `/htec-sdd-tasks` (task registry creation)
  - Reuses ProductSpecs JIRA export if available (recommended)
  - Falls back to module decomposition if no JIRA export exists
- **CP5-N**: Implementation phases where **`/htec-sdd-implement` operates**
- **Post-implementation**: Additional integration, build, docs (separate commands if needed)

**For detailed execution flow**, see: [Task_Execution_Flow_Detailed.md](./Task_Execution_Flow_Detailed.md)

---

### 3.2 Primary Commands


#### `/htec-sdd-tasks <SystemName>`
**Purpose**: Generate executable task breakdown with interactive strategy selection
**Duration**: 15-30 minutes

**Input Sources**:
- `ProductSpecs_*/01-modules/MOD-*.md`
- `SolArch_*/09-decisions/ADR-*.md`
- `traceability/module_registry.json`

**Interactive Strategy Selection** (via planning-tech-lead):
1. **Decomposition approach**: Vertical slicing / Layer-by-layer / Feature-by-feature / Hybrid
2. **PR grouping**: Per-task / Per-story / Per-epic / Per-phase
3. **Worktree strategy**: Single branch / Per-task worktrees / Per-PR worktrees
4. **Review strategy**: Per-PR / Batch review / Milestone review

**Output**:
- `01-tasks/task-index.md`
- `01-tasks/phase-*/T*.md`
- `traceability/task_registry.json` (with `pr_groups` section)
- `scripts/setup-worktrees.sh` (executable worktree setup script)
- `pr-metadata/PR-NNN.md` (traceability for each PR group)

**Task Organization**:
1. **Phase 1**: Setup (project init, deps)
2. **Phase 2**: Foundation (shared code, models, base components)
3. **Phase 3+**: User Stories (grouped by priority P0 → P1 → P2)
4. **Final Phase**: Polish (cross-cutting concerns)

**Example**:
```bash
/htec-sdd-tasks InventorySystem
# Interactive prompts appear
# User selects: "Vertical slicing", "Per-story", "Per-PR worktrees", "Per-PR"
```

---

#### `/htec-sdd-worktree-setup <SystemName>`
**Purpose**: Create git worktrees for parallel PR development
**Duration**: 2-5 minutes
**Prerequisites**: `/htec-sdd-tasks` completed with PR groups generated

**What it does**:
1. Validates task registry has PR groups
2. Checks git working directory is clean
3. Executes generated `scripts/setup-worktrees.sh`
4. Creates worktrees in `../worktrees/pr-NNN-name/`
5. Creates feature branches for each PR group

**Output**:
```
../worktrees/
├── pr-001-auth/          (branch: feature/pr-001-auth)
├── pr-002-inventory/     (branch: feature/pr-002-inventory)
├── pr-003-reports/       (branch: feature/pr-003-reports)
└── pr-004-settings/      (branch: feature/pr-004-settings)
```

**Example**:
```bash
/htec-sdd-worktree-setup InventorySystem
# Or with custom base branch:
/htec-sdd-worktree-setup InventorySystem --base develop
```

**See Also**: [Git Worktree Workflow](#7-git-worktree-workflow)

---

#### `/htec-sdd-implement <SystemName> [--pr-group PR-NNN] [--phase N] [--task T001]`
**Purpose**: Execute implementation tasks (worktree-aware, with task isolation)
**Duration**: Variable (hours to days)

**Options** (v2.1+):

| Option | Description | Default |
|--------|-------------|---------|
| `--task <T-ID>` | Execute specific task only | All pending |
| `--pr-group <PR-ID>` | Execute PR group | Auto-detect or all |
| `--batch <N>` | Max concurrent task agents | 2 |
| `--parallel` | Enable parallel agent execution | true |
| `--isolate-tasks` | Spawn agent per task (prevents context rot) | **true** |
| `--priority <P0\|P1\|P2>` | Filter by priority | All |
| `--phase <N>` | Target specific phase | All phases |
| `--skip-research` | Skip codebase research | false |
| `--skip-review` | Skip quality review | false |

**Task Isolation Mode** (v2.1+, default enabled):
- Spawns separate `implementation-task-orchestrator` agent per task
- Prevents context memory rot in main orchestrator
- Each task runs in isolated context with fresh memory
- Results saved to `Implementation_<System>/01-tasks/<T-ID>/results/`
- See [Section 7: Task Isolation Mode](#7-task-isolation-mode)

**Worktree Detection**:
- Auto-detects PR group from current worktree path or branch name
- Filters tasks to only those in the detected/specified PR group
- Uses worktree-scoped file locking for parallel development

**Modes**:
- Full execution: Run all phases in sequence
- PR-scoped: `--pr-group PR-001` or auto-detected from worktree
- Phase execution: `--phase 3` runs only phase 3
- Single task: `--task T015` runs only that task
- Batch execution: `--batch 3` runs 3 tasks concurrently

**Example**:
```bash
# Standard (single-branch) with task isolation
/htec-sdd-implement InventorySystem

# Worktree workflow (auto-detect)
cd ../worktrees/pr-001-auth
/htec-sdd-implement InventorySystem  # Auto-detects PR-001

# Explicit PR group with batch concurrency
/htec-sdd-implement InventorySystem --pr-group PR-001 --batch=3

# Legacy mode (no task isolation, not recommended for multi-task)
/htec-sdd-implement InventorySystem --isolate-tasks=false
```

**Execution Algorithm** (Isolation Mode):
```
Main Dispatcher (lightweight):
  1. Build task execution queue
  2. For each task (up to --batch concurrent):
     - Spawn implementation-task-orchestrator agent
     - Agent runs full 8-phase workflow in isolated context
     - Agent saves results to 01-tasks/<T-ID>/results/
     - Agent returns compact JSON summary
  3. Consolidate summaries
  4. Report completion
```

**Example**:
```bash
# Run all phases (with task isolation)
/htec-sdd-implement

# Run specific phase
/htec-sdd-implement --phase 3

# Run specific task
/htec-sdd-implement --task T015
```

---

#### `/htec-sdd-review`
**Purpose**: Multi-agent parallel code review
**Duration**: 20-30 minutes

**Agent Team** (6 specialized reviewers):
- `bug-hunter` (25% weight)
- `security-auditor` (25% weight)
- `code-quality` (15% weight)
- `test-coverage` (15% weight)
- `contracts-reviewer` (10% weight)
- `accessibility-auditor` (10% weight)

**Quality Gate**:
- Critical issues = FAIL (must fix)
- High issues = WARNING (should fix)
- Medium/Low = INFO (consider)

**Example**:
```bash
/htec-sdd-review
```

---

#### `/htec-sdd-integrate`
**Purpose**: Run integration and E2E tests
**Duration**: Variable (depends on test suite)

**Test Types**:
- Integration tests (API contracts, service mesh)
- E2E tests (critical user journeys)
- Performance tests (response time validation)
- Visual regression tests (screenshot comparison)

**Example**:
```bash
/htec-sdd-integrate
```

---

#### `/htec-sdd-changerequest <Description>`
**Purpose**: Process implementation feedback/change requests
**Duration**: Variable (depends on complexity)

**Workflow**:
1. Input: Feedback text/file
2. Impact Analysis: Which tasks/modules affected?
3. Root Cause Analysis: Five Whys, Fishbone, A3, PDCA
4. Approval Gate
5. Implementation Planning (2+ options)
6. Execute selected plan
7. Validation & verification
8. Update traceability

**Example**:
```bash
/htec-sdd-changerequest "Login form validation not working for special characters"
```

---

#### `/htec-sdd-status`
**Purpose**: Show implementation progress
**Duration**: < 1 minute

**Displays**:
- Current checkpoint
- Phase progress
- Task completion metrics
- Test coverage
- Active agents

**Example**:
```bash
/htec-sdd-status
```

---

#### `/htec-sdd-resume`
**Purpose**: Resume from last checkpoint
**Duration**: Variable

**Use When**:
- Session interrupted
- Quality gate failed (after fixes)
- Manual halt requested

**Example**:
```bash
/htec-sdd-resume
```

---

#### `/htec-sdd-reset [--soft|--hard|--phase N]`
**Purpose**: Reset implementation state
**Duration**: 1-2 minutes

**Modes**:
- `--soft`: Reset from last checkpoint
- `--hard`: Complete reset (delete all outputs)
- `--phase N`: Reset from specific phase

**Example**:
```bash
# Soft reset
/htec-sdd-reset --soft

# Hard reset (use with caution!)
/htec-sdd-reset --hard

# Reset from phase 3
/htec-sdd-reset --phase 3
```

---

## 4. Agent Architecture

### 4.1 Agent Taxonomy

```
┌─────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER (v2.1)                      │
│  /htec-sdd-implement dispatches to task-orchestrator agents          │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Task Isolation Mode (default)
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TASK ORCHESTRATOR LAYER (NEW in v2.1)                               │
│  implementation-task-orchestrator (1 per task, isolated context)     │
│  • Runs full 8-phase workflow per task                               │
│  • Prevents context rot across multiple tasks                        │
│  • Saves results to 01-tasks/<T-ID>/results/                         │
└─────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        ▼                           ▼                           ▼
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│  PLANNING           │   │  IMPLEMENTATION     │   │  QUALITY            │
│  AGENTS             │   │  AGENTS             │   │  AGENTS             │
│  (Phases 1-2)       │   │  (Phases 3-5)       │   │  (Phase 6)          │
├─────────────────────┤   ├─────────────────────┤   ├─────────────────────┤
│ • code-explorer     │   │ • test-designer     │   │ • bug-hunter        │
│ • tech-lead         │   │ • developer         │   │ • security-auditor  │
│                     │   │ • test-automation   │   │ • code-quality      │
│                     │   │   -engineer         │   │ • test-coverage     │
│                     │   │                     │   │ • contracts-rev     │
│                     │   │                     │   │ • a11y-auditor      │
└─────────────────────┘   └─────────────────────┘   └─────────────────────┘
         │                          │                          │
         │                          │                          │
         └──────────────────────────┴──────────────────────────┘
                                    │
        ┌───────────────────────────┴───────────────────────────┐
        ▼                                                       ▼
┌───────────────────────────┐           ┌──────────────────────────────┐
│  DOCUMENTATION AGENTS     │           │  PROCESS INTEGRITY AGENTS    │
│  (Phase 7)                │           │  (Continuous Monitoring)     │
├───────────────────────────┤           ├──────────────────────────────┤
│ • documenter              │           │ • traceability-guardian      │
│ • pr-preparer             │           │ • state-watchdog             │
│                           │           │ • checkpoint-auditor         │
│                           │           │ • playbook-enforcer          │
└───────────────────────────┘           └──────────────────────────────┘
```

### 4.2 Agent Roles

#### Task Orchestrator Agent (NEW in v2.1)

| Agent | Purpose | Model | Spawned By | Concurrency |
|-------|---------|-------|------------|-------------|
| `implementation-task-orchestrator` | Full 8-phase workflow per task in isolated context | Sonnet | `/htec-sdd-implement` | Up to `--batch` (default: 2) |

**Key Features**:
- Prevents context memory rot by running each task in isolated agent context
- Spawns all phase agents (1-8) internally
- Saves all results to `Implementation_<System>/01-tasks/<T-ID>/results/`
- Returns compact JSON summary to parent dispatcher

**Results Structure** (per task):
```
Implementation_<System>/01-tasks/<T-ID>/results/
├── execution.json          # Full execution record with phases
├── implementation_plan.md  # Phase 2 output
├── test_spec.md            # Phase 3 output
├── build.log               # Phase 4 build output
├── test.log                # Phase 4 test output
├── e2e_test.log            # Phase 5 E2E output
├── quality_report.json     # Phase 6 findings
└── pr_description.md       # Phase 7 PR prep
```

#### Planning Agents (Phases 1-2)

| Agent | Purpose | Model | Phase | Timing |
|-------|---------|-------|-------|--------|
| `planning-code-explorer` | Codebase analysis, pattern detection | Sonnet | 1 | Sequential |
| `planning-tech-lead` | Detailed implementation plan generation | Sonnet | 2 | Sequential |

**Note**: All requirements come from ProductSpecs and SolArch outputs. Planning agents provide codebase research and detailed implementation plans before coding begins.

#### Implementation Agents (Phases 3-5)

| Agent | Purpose | Model | Phase | Concurrency |
|-------|---------|-------|-------|-------------|
| `implementation-test-designer` | BDD scenarios & TDD specs (before coding) | Sonnet | 3 | Sequential |
| `implementation-developer` | TDD implementation (RED-GREEN-REFACTOR) | Sonnet | 4 | Sequential (1 dev) |
| `implementation-test-automation-engineer` | E2E tests, integration tests, Playwright | Sonnet | 5 | Sequential |

**Important**: V2.0 uses **1 developer per task** (not 3), enabling fine-grained task control with the comprehensive orchestration model.

#### Quality Agents (Phase 6)

| Agent | Focus | Model | Phase | Concurrency |
|-------|-------|-------|-------|-------------|
| `quality-bug-hunter` | Logic errors, null handling, edge cases | Sonnet | 6 | Parallel (6 agents) |
| `quality-security-auditor` | OWASP Top 10, injection, auth vulnerabilities | Sonnet | 6 | Parallel |
| `quality-code-quality` | SOLID, DRY, complexity, maintainability | Sonnet | 6 | Parallel |
| `quality-test-coverage` | Missing tests, edge cases, AC coverage | Sonnet | 6 | Parallel |
| `quality-contracts-reviewer` | API compliance, type safety, schemas | Sonnet | 6 | Parallel |
| `quality-accessibility-auditor` | WCAG 2.1 AA, ARIA, keyboard nav, screen readers | Sonnet | 6 | Parallel |

#### Documentation Agents (Phase 7)

| Agent | Purpose | Model | Phase | Timing |
|-------|---------|-------|-------|--------|
| `implementation-documenter` | Inline docs, READMEs, API docs, diagrams | Sonnet | 7 | Sequential |
| `implementation-pr-preparer` | PR description, traceability, review guidance | Sonnet | 7 | Sequential |

#### Process Integrity Agents

| Agent | Monitors | Model | Frequency |
|-------|----------|-------|-----------|
| `traceability-guardian` | ID chains, registry integrity | Haiku | Real-time on change |
| `state-watchdog` | Lock validity, session health | Haiku | Every 60 seconds |
| `checkpoint-auditor` | Gate criteria, blocking conditions | Haiku | On transition |
| `playbook-enforcer` | TDD compliance, patterns | Haiku | Per-task completion |

#### Reflexion Judges

| Agent | Evaluation Focus | Model | Timing |
|-------|------------------|-------|--------|
| `actor` | Generate initial implementation | Opus | Start of task |
| `evaluator` | Critique against acceptance criteria | Opus | After implementation |
| `self-refiner` | Improve based on evaluation | Opus | If score < 7/10 |

### 4.3 Agent Spawning Pattern

All agents are spawned via Claude Code's native `Task` tool:

```javascript
Task({
  subagent_type: "general-purpose",  // Native Claude Code type
  model: "sonnet",                   // or "opus" or "haiku"
  description: "Brief description",
  prompt: `Agent: {agent-name}
    Read: .claude/agents/{agent-name}.md
    SESSION: {session_id} | TASK: {task_id}
    [compact instructions]
    RETURN: JSON { status, files_written, issues }`
})
```

---

## 5. TDD Methodology

### 5.1 The RED-GREEN-REFACTOR Cycle

```
┌────────────────────────────────────────────────────────────────────┐
│                    TDD IMPLEMENTATION PROTOCOL                     │
│                  (Per Acceptance Criterion)                        │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│    ┌────────────────┐                                              │
│    │    1. RED      │  Write failing test for AC                   │
│    │   (Test First) │                                              │
│    └───────┬────────┘                                              │
│            │                                                        │
│            │  test('should validate JWT token', () => {            │
│            │    const result = validateToken(invalidToken);        │
│            │    expect(result.valid).toBe(false);  // FAILS        │
│            │  });                                                   │
│            │                                                        │
│            ▼                                                        │
│    ┌────────────────┐                                              │
│    │   2. GREEN     │  Write minimum code to pass                  │
│    │  (Make Pass)   │                                              │
│    └───────┬────────┘                                              │
│            │                                                        │
│            │  function validateToken(token: string) {              │
│            │    if (!token || token.split('.').length !== 3) {    │
│            │      return { valid: false };                         │
│            │    }                                                   │
│            │    // ... minimal implementation                      │
│            │  }                                                     │
│            │                                                        │
│            ▼                                                        │
│    ┌────────────────┐                                              │
│    │  3. REFACTOR   │  Improve without changing behavior           │
│    │  (Clean Up)    │                                              │
│    └───────┬────────┘                                              │
│            │                                                        │
│            │  • Extract constants                                  │
│            │  • Improve naming                                     │
│            │  • Remove duplication                                 │
│            │                                                        │
│            ▼                                                        │
│    ┌────────────────┐                                              │
│    │   4. VERIFY    │  All tests pass (existing + new)             │
│    │  (Confirm)     │                                              │
│    └───────┬────────┘                                              │
│            │                                                        │
│            │  ✅ 45/45 tests passing                               │
│            │                                                        │
│            ▼                                                        │
│    ┌────────────────┐                                              │
│    │    5. MARK     │  AC complete with code reference             │
│    │  (Document)    │                                              │
│    └────────────────┘                                              │
│                                                                    │
│            [AC-2] ✅ Token validation - auth.ts:70-95              │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 5.2 TDD Iron Law

**RULE**: Never write production code without a failing test

**Enforcement**: `playbook-enforcer` agent monitors:
- Test file MUST exist before production code
- Test MUST fail first (RED phase logged)
- Production code MUST make test pass (GREEN phase logged)

**Violation**: CRITICAL - Phase advancement blocked until remediated

### 5.3 Zero Hallucination Development

**Rules**:
1. Never invent APIs not in contracts
2. Never assume methods exist - verify with grep
3. Use existing patterns even if suboptimal
4. Ask for clarification rather than guess
5. Cite specific file:line for all claims

---

## 6. Multi-Agent Coordination

### 6.1 File Locking Protocol

**Location**: `_state/agent_lock.json`

**Lock Acquisition**:
```
1. READ agent_lock.json
2. CHECK existing locks for target file(s)
3. IF no conflict → ACQUIRE lock (atomic write)
4. IF conflict → WAIT or SKIP based on priority
5. ON completion → RELEASE lock
```

**Lock Types**:
- `exclusive`: Single agent access (code files during implementation)
- `shared_read`: Multiple read, no write (code review phase)
- `global`: Entire resource locked (registry updates)

**Lock Timeouts**:
| Agent Type | Default | Max Extension |
|------------|---------|---------------|
| developer | 15 min | 30 min |
| code-reviewer | 10 min | 20 min |
| test-automation-engineer | 20 min | 45 min |
| tech-lead | 5 min | 10 min |

### 6.2 Session Management

**Location**: `_state/agent_sessions.json`

**Session Lifecycle**:
```
SPAWN → REGISTER → ACQUIRE_LOCKS → EXECUTE → RELEASE → END
```

**State Synchronization Rules**:
1. **Read Before Write**: Always read current state before modifications
2. **Atomic Updates**: Use JSON merge patches for partial updates
3. **Conflict Detection**: Check `last_modified` timestamp before write
4. **Retry on Conflict**: If conflict detected, re-read and retry (max 3)

### 6.3 Parallel Execution Pattern

**Phase Execution**:
```
1. SEQUENTIAL PHASE (Research & Planning, Phases 1-2)
   [S] code-explorer: Analyze codebase patterns
   [S] tech-lead: Generate implementation plan

   INTEGRITY CHECK: checkpoint-auditor validates

2. SEQUENTIAL PHASE (Test Design & Implementation, Phases 3-5)
   [S] test-designer: Create BDD scenarios & TDD specs
   [S] developer: Implement via TDD (RED-GREEN-REFACTOR)
   [S] test-automation-engineer: Create E2E & integration tests

   INTEGRITY CHECK: traceability-guardian validates

3. PARALLEL PHASE (Quality Review, Phase 6)
   [P] bug-hunter: Logic errors, edge cases
   [P] security-auditor: OWASP Top 10, vulnerabilities
   [P] code-quality: SOLID, DRY, maintainability
   [P] test-coverage: Test completeness, AC coverage
   [P] contracts-reviewer: API compliance, type safety
   [P] accessibility-auditor: WCAG 2.1 AA, ARIA, keyboard nav

   BARRIER: Wait for all 6 quality agents
   INTEGRITY CHECK: state-watchdog validates

4. SEQUENTIAL PHASE (Documentation & PR Prep, Phase 7)
   [S] documenter: Inline docs, READMEs, API docs
   [S] pr-preparer: PR description, traceability

   INTEGRITY CHECK: traceability-guardian validates
```

**Task Markers**:
- `[P]` - Parallel: Can run concurrently
- `[S]` - Sequential: Must wait for predecessors
- `[B]` - Blocking: Stops pipeline on failure
- `[C]` - Continuous: Background monitoring

### 6.4 Conflict Resolution

**Priority Matrix**:
| Agent A | Agent B | Winner | Reason |
|---------|---------|--------|--------|
| developer | developer | First arrival | FIFO |
| developer | code-reviewer | developer | Active implementation |
| tech-lead | developer | tech-lead | Planning priority |
| process-integrity | any | process-integrity | Monitoring priority |

**Deadlock Prevention**:
1. Ordered acquisition (alphabetical by file path)
2. Timeout enforcement (no indefinite locks)
3. Single global lock per agent
4. Preemption for integrity violations
5. Watchdog monitoring (stale lock cleanup)

---

## 7. Task Isolation Mode

*(NEW in v2.1.0)*

### 7.1 Overview

Task Isolation Mode prevents **context memory rot** when processing multiple tasks by spawning a separate `implementation-task-orchestrator` agent for each task. This ensures each task runs in a fresh, isolated context without accumulated state from previous tasks.

### 7.2 The Problem: Context Memory Rot

When running `/htec-sdd-implement` with `--pr-group` or `--batch`, the main orchestrator traditionally accumulated context across all tasks:

```
BEFORE (Legacy Mode - Context Accumulation):
┌─────────────────────────────────────────────────────────────┐
│ Main Orchestrator Session                                    │
├─────────────────────────────────────────────────────────────┤
│ Task T-001: Phases 1-8 → results accumulated in context     │
│ Task T-002: Phases 1-8 → more context accumulated           │
│ Task T-003: Phases 1-8 → context rot begins                 │
│ ...                                                          │
│ Task T-N:   Phases 1-8 → severe quality degradation         │
└─────────────────────────────────────────────────────────────┘
```

**Impact**:
- Quality degradation in later tasks
- Increased latency as context window fills
- Risk of truncation or lost context
- Inconsistent behavior across tasks

### 7.3 The Solution: Two-Tier Orchestration

Task Isolation Mode uses a lightweight dispatcher that spawns isolated orchestrator agents:

```
AFTER (Isolation Mode - Fresh Context Per Task):
┌─────────────────────────────────────────────────────────────┐
│ Lightweight Dispatcher (Main Session)                        │
│ Only accumulates: [{task: "T-001", status: "completed"}, ...]│
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ T-001 → Spawn: task-orchestrator (isolated context)         │
│         └── Phases 1-8 in isolated context                  │
│         └── Returns: compact JSON summary                   │
│                                                              │
│ T-002 → Spawn: task-orchestrator (isolated context)         │
│         └── Phases 1-8 in isolated context                  │
│         └── Returns: compact JSON summary                   │
│                                                              │
│ T-N   → Spawn: task-orchestrator (isolated context)         │
│         └── Phases 1-8 in isolated context                  │
│         └── Returns: compact JSON summary                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 7.4 How It Works

**Default Behavior** (`--isolate-tasks=true`):

```bash
# Each task gets its own isolated agent context
/htec-sdd-implement ERTriage --pr-group PR-003

# With batch concurrency limit (default: 2 concurrent)
/htec-sdd-implement ERTriage --pr-group PR-003 --batch=3
```

**Execution Flow**:

1. **Main Dispatcher** (lightweight):
   - Builds task execution queue
   - Tracks up to `--batch` concurrent agents
   - Spawns `implementation-task-orchestrator` per task
   - Collects compact JSON summaries
   - Consolidates final report

2. **Task Orchestrator** (per task, isolated):
   - Runs full 8-phase workflow
   - Saves all results to `01-tasks/<T-ID>/results/`
   - Returns only compact summary to parent

### 7.5 Results Storage

Each task's build/test results are saved to a dedicated folder:

```
Implementation_<System>/01-tasks/<T-ID>/results/
├── execution.json          # Full execution record with all phases
├── implementation_plan.md  # Phase 2: Planning output
├── test_spec.md            # Phase 3: Test design output
├── build.log               # Phase 4: Build output
├── test.log                # Phase 4: Test output
├── e2e_test.log            # Phase 5: E2E test output
├── quality_report.json     # Phase 6: Quality findings
├── pr_description.md       # Phase 7: PR description
└── error.log               # Only if task failed
```

**execution.json Schema**:
```json
{
  "task_id": "T-001",
  "system_name": "ERTriage",
  "pr_group": "PR-003",
  "started_at": "2026-01-30T10:00:00Z",
  "completed_at": "2026-01-30T10:23:47Z",
  "status": "completed",
  "duration_seconds": 1427,
  "phases": {
    "phase_1_research": { "status": "completed", "duration_seconds": 135 },
    "phase_2_planning": { "status": "completed", "duration_seconds": 222 },
    "phase_3_test_design": { "status": "completed", "duration_seconds": 268 },
    "phase_4_implementation": {
      "status": "completed",
      "test_results": { "passing": 12, "failing": 0, "coverage": 87 }
    },
    "phase_5_test_automation": { "status": "completed" },
    "phase_6_quality": { "critical_count": 0, "high_count": 2 },
    "phase_7_documentation": { "status": "completed" },
    "phase_8_finalization": { "status": "completed" }
  },
  "summary": {
    "files_created": ["src/features/auth/auth-service.ts"],
    "tests": { "passing": 17, "failing": 0, "coverage": 87 },
    "quality": { "critical": 0, "high": 2, "medium": 5 }
  }
}
```

### 7.6 Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `--isolate-tasks` | Enable task isolation mode | `true` |
| `--batch <N>` | Max concurrent task orchestrator agents | `2` |
| `--isolate-tasks=false` | Legacy mode (shared context) | - |

### 7.7 Memory Model Comparison

| Mode | Tasks | Main Session Context | Task Context |
|------|-------|---------------------|--------------|
| Legacy (no isolation) | 5 | ~500K tokens (accumulated) | N/A |
| **Isolation (default)** | 5 | ~10K tokens (summaries only) | ~100K each (isolated) |

### 7.8 Legacy Mode

To run in legacy mode (shared context, not recommended for multi-task):

```bash
/htec-sdd-implement ERTriage --pr-group PR-003 --isolate-tasks=false
```

**Warning**: Legacy mode may cause context degradation on multi-task runs. Only use for:
- Debugging
- Single-task execution
- Comparing behavior

### 7.9 Quality Gate Propagation

Quality gates are enforced within each isolated task orchestrator:

- **CRITICAL findings** → Task marked as `blocked`, reported to parent
- **Parent receives** → `{ "status": "blocked", "error": "Quality gate failed" }`
- **Parent behavior** → Stops PR group processing if any task blocked

### 7.10 Related Files

| File | Purpose |
|------|---------|
| `.claude/agents/implementation-task-orchestrator.md` | Task orchestrator agent definition |
| `.claude/skills/IMPLEMENTATION_AGENT_REGISTRY.json` | Agent registry |
| `.claude/architecture/plans/PLAN_task_level_agent_isolation.md` | Design document |

---

## 8. Git Worktree Workflow

### 8.1 Overview

Git worktrees enable parallel PR development by creating isolated working directories that share the same git repository but have different branches checked out. This allows multiple developers or agents to work on "the same" files simultaneously without conflicts.

### 8.2 Setup Process

**Step 1: Generate Tasks with PR Grouping**
```bash
/htec-sdd-tasks InventorySystem
```
User selects PR grouping strategy (e.g., "Per-story") and worktree strategy ("Per-PR worktrees").

**Output**:
- `traceability/task_registry.json` with `pr_groups` section
- `Implementation_InventorySystem/scripts/setup-worktrees.sh`
- `Implementation_InventorySystem/pr-metadata/PR-*.md` files

**Step 2: Create Worktrees**
```bash
/htec-sdd-worktree-setup InventorySystem
```

**Creates**:
```
../worktrees/
├── pr-001-auth/          # feature/pr-001-auth
├── pr-002-inventory/     # feature/pr-002-inventory
├── pr-003-reports/       # feature/pr-003-reports
└── pr-004-settings/      # feature/pr-004-settings
```

### 8.3 Development Workflow

**Parallel Development** (different terminals/sessions):

```bash
# Terminal 1: Work on PR-001
cd ../worktrees/pr-001-auth
/htec-sdd-implement InventorySystem
# Auto-detects PR-001, executes T-001, T-002, T-003

# Terminal 2: Work on PR-002 (parallel)
cd ../worktrees/pr-002-inventory
/htec-sdd-implement InventorySystem
# Auto-detects PR-002, executes T-010..T-017
```

**Key Point**: Both can run simultaneously because worktree-scoped file locks prevent false conflicts.

### 8.4 File Locking Scopes

#### Worktree-Scoped Locks
- **Files**: `src/**/*`, `tests/**/*`, `public/**/*`
- **Lock Key Format**: `{worktree_path}:{file_path}`
- **Example**: `../worktrees/pr-001-auth:src/models/User.ts`
- **Behavior**: Different worktrees can lock the "same" file independently

#### Global-Scoped Locks
- **Files**: `_state/**/*`, `traceability/**/*`, `.claude/**/*`
- **Lock Key Format**: `{file_path}`
- **Example**: `traceability/task_registry.json`
- **Behavior**: All agents must coordinate sequentially (single lock across all worktrees)

### 8.5 PR-Scoped Quality Review

Quality agents support PR-scoped review mode:

```bash
cd ../worktrees/pr-001-auth
/htec-sdd-review InventorySystem --pr-group PR-001
```

**Benefits**:
- Reviews only files in PR-001 metadata (faster)
- Findings tagged with `pr_group: "PR-001"`
- Multiple PR reviews can run in parallel

### 8.6 Creating Pull Requests

```bash
cd ../worktrees/pr-001-auth
git add .
git commit -m "feat(auth): User authentication system"
git push -u origin feature/pr-001-auth

# Use PR metadata for description
gh pr create \
  --title "feat(auth): User authentication system" \
  --body "$(cat ../../Implementation_InventorySystem/pr-metadata/PR-001.md)"
```

### 8.7 Cleanup After Merge

```bash
cd /path/to/main/project
git worktree remove ../worktrees/pr-001-auth
git branch -d feature/pr-001-auth
```

Or use cleanup script:
```bash
/htec-sdd-worktree-setup InventorySystem --clean
```

### 8.8 Benefits

| Benefit | Description |
|---------|-------------|
| **True Parallelism** | Multiple developers/agents modify "same" files in different worktrees |
| **Clean PRs** | Each PR has isolated branch and changes |
| **Fast Reviews** | PR-scoped quality checks review only changed files |
| **Registry Safety** | Shared files remain sequentially coordinated |
| **Easy Isolation** | Each feature developed independently |

---

## 9. PR Grouping Strategy

### 9.1 Overview

PR grouping determines how tasks are bundled into pull requests. The strategy affects PR size, review complexity, and deployment granularity.

### 9.2 Available Strategies

#### Per-Task Grouping
**Pattern**: 1 task = 1 PR

**Pros**:
- Smallest PR size (easiest review)
- Fastest feedback loop
- Maximum isolation

**Cons**:
- Many PRs to manage
- Overhead for small tasks
- May break up cohesive features

**Best For**: Large teams, strict review processes, high-risk changes

#### Per-Story Grouping (Recommended)
**Pattern**: 1 user story = 1 PR (multiple tasks)

**Pros**:
- Feature-complete PRs
- Logical review scope
- Balanced PR size
- Traces back to user value

**Cons**:
- Larger than per-task
- May have task dependencies

**Best For**: Most projects, agile workflows, feature-based development

#### Per-Epic Grouping
**Pattern**: 1 epic = 1 PR (multiple stories/tasks)

**Pros**:
- Complete feature sets
- Fewer PRs to manage
- Comprehensive testing

**Cons**:
- Large PR size (harder review)
- Longer feedback cycles
- Merge conflicts more likely

**Best For**: Small teams, rapid prototyping, tightly coupled features

#### Per-Phase Grouping
**Pattern**: 1 phase = 1 PR (e.g., all infrastructure, all features)

**Pros**:
- Milestone-based delivery
- Natural checkpoint boundaries
- Simplest grouping logic

**Cons**:
- Very large PRs
- Difficult to review
- High merge risk

**Best For**: Solo developers, proof-of-concept projects, time-boxed sprints

### 9.3 Selection Criteria

Consider these factors when choosing a PR grouping strategy:

| Factor | Per-Task | Per-Story | Per-Epic | Per-Phase |
|--------|----------|-----------|----------|-----------|
| **Team Size** | Large (5+) | Medium (3-5) | Small (2-3) | Solo |
| **PR Review Time** | 10-15 min | 30-45 min | 1-2 hours | 2-4 hours |
| **Avg LOC/PR** | 50-150 | 200-400 | 500-1000 | 1000+ |
| **Merge Frequency** | Very High | High | Medium | Low |
| **Feature Cohesion** | Low | High | Very High | Complete |

### 9.4 Implementation

**Interactive Selection** (during `/htec-sdd-tasks`):

```
PR Grouping Strategy:
1. Per-task (1 task = 1 PR, fine-grained)
2. Per-story (1 user story = 1 PR, feature-complete) [Recommended]
3. Per-epic (1 epic = 1 PR, larger scope)
4. Per-phase (1 phase = 1 PR, milestone-based)

Select: 2
```

**Output** (`traceability/task_registry.json`):
```json
{
  "implementation_strategy": {
    "pr_grouping": "per-story"
  },
  "pr_groups": {
    "PR-001": {
      "id": "PR-001",
      "title": "feat(auth): User authentication system",
      "tasks": ["T-001", "T-002", "T-003"],
      "user_story": "US-001",
      "module_refs": ["MOD-AUTH-01"],
      "estimated_loc": 350
    }
  }
}
```

### 9.5 Best Practices

1. **Start Conservative**: Use per-story grouping by default
2. **Measure & Adjust**: Track PR review time and quality
3. **Consider Team Capacity**: Smaller PRs for distributed teams
4. **Respect Module Boundaries**: Don't split cohesive modules
5. **Priority Alignment**: Group P0 tasks together when possible

---

## 10. Quality Gates

### 10.1 Understanding "Blocking"

**Blocking** indicates that a checkpoint or phase acts as a **mandatory quality gate** that:

1. **STOPS execution** if validation criteria are not met
2. **Requires remediation** before proceeding to the next phase
3. **Cannot be bypassed** - enforcement is mandatory
4. **Ensures critical quality/integrity** standards are met

#### Checkpoint Markers

Throughout the phase flow diagrams, you'll see these markers:

```
[B] = Blocking       # Stops pipeline on failure
[I] = Integrity Check # Validation checkpoint
[C] = Continuous     # Background monitoring
[P] = Parallel       # Can run concurrently
[S] = Sequential     # Must wait for predecessors
```

#### What Happens at a Blocking Gate?

**If validation PASSES** ✅:
- Execution continues to next phase
- Progress is logged
- Checkpoint marked complete

**If validation FAILS** ❌:
- Execution HALTS immediately
- Error report generated with specific failures
- Fix instructions provided
- Must remediate issues before proceeding
- Re-run validation after fixes

#### Example Scenario

At **CP6 (Code Review)**, if the security-auditor finds CRITICAL vulnerabilities:
- **Blocking = YES** → Execution stops
- Developer must fix the security issues
- Re-run `/htec-sdd-review`
- Only after passing can you proceed to CP7 (Integration)

This ensures that critical quality standards (security, test coverage, architecture compliance) are enforced and cannot be skipped.

---

### 10.2 Blocking Gates

| Checkpoint | Validation | Blocking |
|------------|------------|----------|
| **CP1** | ProductSpecs CP8+, SolArch CP12+, P0 coverage 100% | YES |
| **CP4** | User approval of task breakdown | YES |
| **CP6** | No CRITICAL findings, coverage > 80% | YES |
| **CP9** | Build success, tests pass, coverage ≥ 80% | YES |

### 10.3 Process Integrity Monitoring

**Continuous Monitoring Layer**:
```
┌────────────────────────────────────────────────────────────────────┐
│              PROCESS INTEGRITY MONITORING (Continuous)             │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  traceability-guardian: ID chains, registry integrity              │
│  ├─ Watches: traceability/*.json                                  │
│  ├─ Validates: Schema, ID uniqueness, reference integrity         │
│  └─ Action on violation: Block write, alert                       │
│                                                                    │
│  state-watchdog: Lock validity, session health, state consistency  │
│  ├─ Watches: _state/*.json, agent_lock.json, agent_sessions.json  │
│  ├─ Validates: Lock timeouts, session heartbeats, state checksums │
│  └─ Action on violation: Clean stale, alert                       │
│                                                                    │
│  checkpoint-auditor: Gate criteria, artifact completeness          │
│  ├─ Watches: Checkpoint transitions                               │
│  ├─ Validates: Required files, quality gates, dependencies        │
│  └─ Action on violation: Block transition                         │
│                                                                    │
│  playbook-enforcer: TDD compliance, pattern adherence              │
│  ├─ Watches: Implementation code, test files                      │
│  ├─ Validates: RED-GREEN-REFACTOR sequence, AC coverage           │
│  └─ Action on violation: Veto phase advance                       │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 10.4 Violation Severity Matrix

| Severity | Response | Examples |
|----------|----------|----------|
| **CRITICAL** | Immediate halt, veto execution | Security vuln, data loss, test suite failure |
| **HIGH** | Block at next gate, require fix | Missing trace link, TDD violation |
| **MEDIUM** | Warning + log, continue allowed | Low coverage file, minor pattern deviation |
| **LOW** | Log only, no action needed | Style inconsistency, documentation gap |

### 10.5 Code Review Quality Gate

**Agent Team Findings**:
- Each agent returns findings with confidence score
- Confidence thresholds determine blocking:
  - CRITICAL: 50% threshold → Always blocks
  - HIGH: 65% threshold → Blocks if > 80%
  - MEDIUM: 75% threshold → Review recommended
  - LOW: 85% threshold → Informational

**Consolidated Report**:
- Critical issues → FAIL (must fix)
- High issues (>80% confidence) → FAIL
- Medium/Low → PASS with recommendations

---

## 11. Change Request Workflow

### 11.1 Kaizen-Based Change Management

**Command**: `/htec-sdd-changerequest <Description>`

**Workflow**:
```
1. REGISTER
   └─ Create CR-XXX in change_request_registry.json

2. ANALYZE (Implementation_ChangeAnalyzer)
   ├─ Quick Check: Simple, obvious cause
   ├─ 5 Whys: Moderate complexity
   ├─ Fishbone: Multiple contributing factors
   └─ A3 Full: Critical issues

3. IMPLEMENT (Implementation_ChangeImplementer)
   ├─ PDCA Cycle:
   │   ├─ PLAN: 2+ options
   │   ├─ DO: Execute selected plan (TDD)
   │   ├─ CHECK: Validation
   │   └─ ACT: Update traceability
   └─ Reflexion: Self-refinement loops

4. MEMORIZE
   └─ Update CLAUDE.md with learnings
```

### 11.2 Analysis Methods

**Method Selection**:
| Complexity | Method | Duration |
|------------|--------|----------|
| Simple | Quick Check | 5-10 min |
| Moderate | 5 Whys | 15-20 min |
| Complex | Fishbone | 30-45 min |
| Critical | A3 Full | 1-2 hours |

**5 Whys Example**:
```
Problem: Login form validation failing
Why #1: Validation regex not matching special characters
Why #2: Regex pattern copied from old codebase
Why #3: No validation test for special characters
Why #4: Test coverage gap in acceptance criteria
Why #5: Acceptance criteria didn't specify edge cases

Root Cause: Incomplete acceptance criteria definition
```

### 11.3 PDCA Implementation Cycle

```
┌────────────────────────────────────────────────────────────────────┐
│                         PDCA CYCLE                                 │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  1. PLAN                                                           │
│     ├─ Generate 2+ implementation options                         │
│     ├─ Evaluate pros/cons/effort for each                         │
│     └─ Select approach (user approval if HIGH complexity)         │
│                                                                    │
│  2. DO                                                             │
│     ├─ Execute TDD implementation (RED-GREEN-REFACTOR)            │
│     ├─ Update traceability                                        │
│     └─ Log progress                                               │
│                                                                    │
│  3. CHECK                                                          │
│     ├─ Run all tests (unit + integration + E2E)                   │
│     ├─ Validate acceptance criteria                               │
│     └─ Reflexion self-review (if score < 7, iterate)              │
│                                                                    │
│  4. ACT                                                            │
│     ├─ Update task registry                                       │
│     ├─ Update implementation registry                             │
│     ├─ Update CLAUDE.md with learnings                            │
│     └─ Close CR-XXX                                               │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 12. Traceability Requirements

### 12.1 End-to-End Traceability Chain

```
DISCOVERY → PROTOTYPE → PRODUCTSPECS → SOLARCH → IMPLEMENTATION

CM-XXX ──▶ PP-X.X ──▶ JTBD-X.X ──▶ REQ-XXX ──▶ MOD-XXX ──▶ T-XXX
(Material) (Pain)    (Job)        (Req)       (Module)    (Task)
                                                              │
                                                              ▼
                                                  ┌─────────────────────┐
                                                  │  CODE + TESTS       │
                                                  │  src/*.ts           │
                                                  │  tests/*.test.ts    │
                                                  └─────────────────────┘
```

### 12.2 Traceability in Code

**Every source file MUST include**:
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
```

### 12.3 Registry Updates

**After every file creation/modification/deletion**:
```bash
python3 .claude/hooks/version_history_logger.py \
  "traceability/" \
  "{system_name}" \
  "implementation" \
  "Claude" \
  "{version}" \
  "{reason}" \
  "{refs_comma_separated}" \
  "{file_path}" \
  "{action}"
```

**Parameters**:
- `action`: `creation`, `modification`, `deletion`
- `refs_comma_separated`: IDs this change traces to (e.g., `T-010,REQ-003`)

### 12.4 Coverage Requirements

| Coverage Type | P0 Requirement | P1/P2 Requirement |
|---------------|----------------|-------------------|
| Pain Points | 100% | 80% |
| Requirements | 100% | 80% |
| Test Coverage | 100% | 80% |
| Traceability Chain | 100% (no broken links) | 100% |

---

## 13. Best Practices

### 13.1 DO's

✅ **Always read files before editing**
✅ **Follow TDD strictly** (RED-GREEN-REFACTOR)
✅ **Mark tasks with [P] or [S]** for proper coordination
✅ **Update traceability** after every change
✅ **Log execution** via hooks (command_start.py, command_end.py)
✅ **Use existing patterns** from codebase
✅ **Cite file:line references** for all claims
✅ **Run reflexion** after each phase
✅ **Monitor Process Integrity** violations
✅ **Update CLAUDE.md** with learnings

### 13.2 DON'Ts

❌ **Never write code without a failing test**
❌ **Never skip traceability logging**
❌ **Never invent APIs** not in contracts
❌ **Never ignore Process Integrity violations**
❌ **Never bypass blocking quality gates**
❌ **Never commit without code review**
❌ **Never push to main without approval**
❌ **Never modify _state/*.json directly** (use hooks)
❌ **Never skip user approval** at CP4
❌ **Never create duplicate tasks** without checking task_registry.json

### 13.3 Anti-Patterns

🚫 **Over-Engineering**
- Don't add features beyond acceptance criteria
- Don't create abstractions for one-time operations
- Don't design for hypothetical future requirements

🚫 **Premature Optimization**
- Don't optimize before profiling
- Don't sacrifice readability for performance
- Don't add complexity without evidence

🚫 **Test-Last Development**
- Don't write production code before tests
- Don't skip failing test verification (RED phase)
- Don't commit without test coverage

🚫 **Broken Traceability**
- Don't create orphan artifacts (no parent ID)
- Don't reference non-existent IDs
- Don't skip version history logging

🚫 **Lock Mismanagement**
- Don't hold locks indefinitely
- Don't acquire multiple locks out of order
- Don't skip lock release on error

### 13.4 Performance Tips

⚡ **Maximize Parallelization**
- Mark independent tasks with `[P]`
- Use parallel code review (6 agents)
- Spawn multiple developers when possible

⚡ **Minimize Wait Time**
- Release locks immediately after write
- Use atomic updates for state changes
- Batch registry updates when possible

⚡ **Optimize Agent Usage**
- Use Haiku for simple validations
- Use Sonnet for implementation
- Use Opus only for complex reasoning

### 13.5 Recovery Procedures

**Agent Failure**:
1. Mark session as "failed" in agent_sessions.json
2. Release all locks held by failed agent
3. Assess task state (rollback if partial)
4. Log failure to FAILURES_LOG.md
5. Spawn replacement agent if needed

**Stale Lock Cleanup**:
- Runs every 60 seconds via state-watchdog
- Cleans locks older than timeout
- Checks session status before cleanup
- Logs cleanup actions

**State Corruption**:
1. Detect: Checksum mismatch or JSON parse failure
2. Isolate: Stop all agents writing to corrupted file
3. Recover: Restore from `_state/backups/` (every 5 min)
4. Verify: Validate restored state with Process Integrity
5. Resume: Restart affected agents from last known good state

---

## Appendix A: Quick Command Reference

```bash
# Setup and Planning
/htec-sdd-tasks InventorySystem          # Interactive task generation
/htec-sdd-worktree-setup InventorySystem # Create PR worktrees

# Implementation (Narrow Execution)
/htec-sdd-implement InventorySystem --task T-001         # Single task
/htec-sdd-implement InventorySystem --pr-group PR-001    # PR group
/htec-sdd-implement InventorySystem --priority P0        # Priority filter
cd ../worktrees/pr-001-auth
/htec-sdd-implement InventorySystem                      # Auto-detect PR

# Quality and Integration
/htec-sdd-review                         # Multi-agent code review
/htec-sdd-integrate                      # Integration tests
/htec-sdd-finalize                       # Documentation

# Utilities
/htec-sdd-status                         # Progress check
/htec-sdd-resume                         # Resume from checkpoint
/htec-sdd-reset --soft                   # Soft reset
/htec-sdd-changerequest "Description..."  # Change management
```

**Detailed Flow**: See [Task_Execution_Flow_Detailed.md](./Task_Execution_Flow_Detailed.md)

---

## Appendix B: File Structure Summary

```
.claude/
├── commands/
│   ├── htec-sdd.md
│   ├── htec-sdd-init.md
│   ├── htec-sdd-validate.md
│   ├── htec-sdd-tasks.md
│   ├── htec-sdd-implement.md
│   ├── htec-sdd-review.md
│   ├── htec-sdd-integrate.md
│   ├── htec-sdd-finalize.md
│   ├── htec-sdd-status.md
│   ├── htec-sdd-resume.md
│   ├── htec-sdd-reset.md
│   └── htec-sdd-changerequest.md
│
├── agents/
│   ├── implementation-developer.md
│   ├── implementation-test-automation-engineer.md
│   ├── process-integrity-traceability-guardian.md
│   ├── process-integrity-state-watchdog.md
│   ├── process-integrity-checkpoint-auditor.md
│   └── process-integrity-playbook-enforcer.md
│
└── hooks/
    ├── implementation_quality_gates.py
    ├── agent_coordination.py
    └── process_integrity_monitor.py
```

---

## Appendix C: Related Documents

| Document | Description |
|----------|-------------|
| `Implementation_Architecture.md` | Detailed architecture specification |
| `Implementation_Diagrams.md` | Visual representations of flows |
| `Implementation_Traceability_Map.md` | Source material traceability |
| `Parallel_Agent_Coordination.md` | Multi-agent coordination protocols |
| `Subagent_Architecture.md` | Master agent taxonomy |

---

**Document Version**: 2.1.0
**Last Updated**: 2026-01-30
**Status**: Active
