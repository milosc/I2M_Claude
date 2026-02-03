---
name: HTEC_SDD_COMMAND_REFERENCE
description: Complete reference for Implementation stage commands
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /HTEC_SDD_COMMAND_REFERENCE started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /HTEC_SDD_COMMAND_REFERENCE ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /HTEC_SDD_COMMAND_REFERENCE instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# HTEC-SDD Command Reference

Stage 5: Implementation - Transforms ProductSpecs and SolArch outputs into working, tested code.

## Overview

The `/htec-sdd-*` commands implement a Spec-Driven Development workflow that:
- Decomposes module specifications into executable tasks
- Supports parallel AI agent execution
- Enforces Test-Driven Development (TDD)
- Maintains full traceability from pain points to deployed code
- Integrates multi-agent code review

## Command Summary

| Command | CP | Description |
|---------|----|----|
| `/htec-sdd-init` | 0 | Initialize implementation state |
| `/htec-sdd-validate` | 1 | Validate ProductSpecs/SolArch inputs **[BLOCKING]** |
| `/htec-sdd-tasks` | 2 | Decompose modules into tasks (interactive with PR grouping) |
| `/htec-sdd-worktree-setup` | - | Create git worktrees for parallel PR development |
| `/htec-sdd-implement` | 3-5 | Execute implementation with TDD (worktree-aware, granular) |
| `/htec-sdd-review` | 6 | Multi-agent code review **[BLOCKING]** |
| `/htec-sdd-integrate` | 7 | Integration testing |
| `/htec-sdd-finalize` | 8-9 | Documentation and validation |
| `/htec-sdd-status` | - | Show current progress |
| `/htec-sdd-resume` | - | Resume from last checkpoint |
| `/htec-sdd-reset` | - | Reset state |
| `/htec-sdd-changerequest` | - | Process change requests with Kaizen analysis |

## Implementation Philosophy

**Narrow Execution Model**: Implementation is always **task-based** or **PR-based**, never full-pipeline automation.

**Why?**
- Provides fine-grained control over what gets implemented
- Enables parallel development across multiple PRs
- Allows incremental testing and validation
- Supports worktree-based isolation

**Typical Workflow:**
1. `/htec-sdd-tasks` - Generate task breakdown with interactive strategy selection
2. `/htec-sdd-worktree-setup` - Create worktrees for parallel PRs
3. `/htec-sdd-implement --task T-001` - Implement specific tasks
4. `/htec-sdd-review` - Quality check after batch
5. `/htec-sdd-integrate` - Integration tests

**For detailed execution flow**, see: `.claude/architecture/workflows/Implementation Phase/Task_Execution_Flow_Detailed.md`

### Prerequisites
- Completed ProductSpecs: `_state/productspecs_progress.json` status is "completed"
- Completed SolArch: `_state/solarch_progress.json` status is "completed"
- Task Registry: Generated via `/htec-sdd-tasks`

### Resume Interrupted Work

```bash
/htec-sdd-resume
```

Reads `_state/implementation_progress.json` and continues from last completed checkpoint.

## Phase Commands

### `/htec-sdd-init` (Checkpoint 0)

Initializes the implementation stage:

```bash
/htec-sdd-init InventorySystem
```

**Creates:**
- `_state/implementation_config.json` - Configuration
- `_state/implementation_progress.json` - Progress tracking
- `Implementation_InventorySystem/` - Output folder structure
- `traceability/task_registry.json` - Task tracking registry

**Folder Structure Created:**
```
Implementation_InventorySystem/
├── src/
│   ├── components/
│   ├── features/
│   ├── services/
│   └── utils/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
└── reports/
```

---

### `/htec-sdd-validate` (Checkpoint 1) **[BLOCKING]**

Validates that ProductSpecs and SolArch outputs meet minimum requirements:

```bash
/htec-sdd-validate InventorySystem
```

**Validation Criteria:**
| Check | Requirement |
|-------|-------------|
| ProductSpecs checkpoint | Must be 8+ |
| SolArch checkpoint | Must be 12+ |
| Module specs exist | At least 1 MOD-*.md file |
| ADRs exist | At least 9 ADR-*.md files |
| Traceability | 100% P0 pain point coverage |

**Outputs:**
- `_state/implementation_input_validation.json`

**If validation fails:** Execution stops with clear guidance on what's missing.

---

### `/htec-sdd-tasks` (Checkpoint 2)

Decomposes module specifications into executable tasks:

```bash
/htec-sdd-tasks InventorySystem
/htec-sdd-tasks InventorySystem --module MOD-MOB-INV-01
/htec-sdd-tasks InventorySystem --priority P0
```

**Options:**
| Option | Description |
|--------|-------------|
| `--module <MOD-ID>` | Decompose specific module only |
| `--priority <P0\|P1\|P2>` | Filter by priority |
| `--parallel` | Enable parallel task markers (default: true) |

**Generates:**
- `traceability/task_registry.json` - All tasks with dependencies
- `Implementation_X/tasks/TASK_INDEX.md` - Human-readable task list
- `Implementation_X/tasks/T-XXX.md` - Individual task specifications

**Task Structure:**
```json
{
  "id": "T-015",
  "title": "Implement barcode scanning service",
  "module_ref": "MOD-MOB-INV-01",
  "user_story": "US-003",
  "jira_ref": "INV-015",
  "parallel": true,
  "dependencies": ["T-012", "T-014"],
  "acceptance_criteria": [
    {"id": "AC-1", "description": "Scan EAN-13 barcodes"},
    {"id": "AC-2", "description": "Handle invalid barcodes gracefully"}
  ],
  "tdd_spec": {
    "test_file": "tests/unit/barcode-scanner.test.ts",
    "test_cases": ["should scan valid EAN-13", "should reject invalid format"]
  }
}
```

**Parallel Markers:**
Tasks marked with `"parallel": true` can be executed concurrently. Dependencies are respected.

---

### `/htec-sdd-implement` (Checkpoints 3-5)

Executes implementation using TDD protocol:

```bash
/htec-sdd-implement InventorySystem
/htec-sdd-implement InventorySystem --task T-015
/htec-sdd-implement InventorySystem --batch 5
/htec-sdd-implement InventorySystem --parallel
```

**Options:**
| Option | Description |
|--------|-------------|
| `--task <T-ID>` | Implement specific task |
| `--batch <N>` | Process N tasks per batch (default: 3) |
| `--parallel` | Enable parallel agent execution |
| `--no-tdd` | Skip TDD (not recommended) |

**TDD Protocol (per task):**

```
1. RED    - Write failing test based on AC
2. GREEN  - Write minimal code to pass
3. REFACTOR - Clean up while keeping green
4. VERIFY - Run full test suite
5. MARK   - Update task_registry.json status
```

**Checkpoints:**
- **CP3**: Core infrastructure tasks complete
- **CP4**: Feature tasks 50%+ complete
- **CP5**: All P0 tasks complete

**Outputs:**
- Source code in `Implementation_X/src/`
- Tests in `Implementation_X/tests/`
- Updated `traceability/task_registry.json`

---

### `/htec-sdd-review` (Checkpoint 6) **[BLOCKING]**

Multi-agent code review with 4 specialized reviewers (run in parallel):

```bash
/htec-sdd-review InventorySystem
/htec-sdd-review InventorySystem --scope changed
/htec-sdd-review InventorySystem --agent security
/htec-sdd-review InventorySystem --threshold 80
```

**Options:**
| Option | Description |
|--------|-------------|
| `--scope <all\|changed\|module>` | Review scope (default: all) |
| `--agent <name>` | Run specific agent only |
| `--threshold <0-100>` | Minimum confidence for findings (default: 70) |
| `--fix` | Auto-fix low-risk issues |

**Review Agents (run in parallel):**

| Agent | Focus | Severity Weight |
|-------|-------|-----------------|
| `quality-security-auditor` | OWASP Top 10, injection, auth, data exposure | CRITICAL |
| `quality-code-quality` | SOLID, DRY, complexity, naming, patterns | MEDIUM |
| `quality-test-coverage` | Missing tests, edge cases, mocking issues | HIGH |
| `quality-accessibility-auditor` | WCAG 2.1 compliance, a11y patterns | MEDIUM |

**Blocking Criteria:**
- No CRITICAL findings
- No HIGH findings with confidence > 90%
- Test coverage >= 80% (warning only)

**Output Files (ALWAYS Generated):**

| File | Format | Description |
|------|--------|-------------|
| `Implementation_X/reports/CODE_REVIEW.md` | Markdown | Human-readable report with all findings, severity, remediation steps |
| `Implementation_X/reports/review-findings.json` | JSON | Machine-readable findings for CI/CD integration, filtering, analysis |

**JSON Schema:** `.claude/templates/implementation/review_findings.schema.json`

**Registry Updates:**
- `_state/implementation_progress.json` - Sets CP4 to completed, records metrics
- `traceability/review_registry.json` - Adds review entry with REV-XXX ID
- `traceability/<SystemName>_version_history.json` - Logs report file creation

**Report Generation Hook:**
```bash
# Called automatically at end of review
python3 .claude/hooks/generate_review_report.py \
  "<SystemName>" \
  "/tmp/review_findings_<SystemName>.json" \
  --scope "<scope>" \
  --update-progress \
  --update-registry
```

---

### `/htec-sdd-integrate` (Checkpoint 7)

Integration testing across modules:

```bash
/htec-sdd-integrate InventorySystem
```

**Executes:**
1. Cross-module integration tests
2. API contract validation
3. E2E smoke tests
4. Performance baseline

**Outputs:**
- `Implementation_X/reports/INTEGRATION_REPORT.md`
- `Implementation_X/tests/e2e/` - E2E test files

---

### `/htec-sdd-finalize` (Checkpoints 8-9)

Documentation and final validation:

```bash
/htec-sdd-finalize InventorySystem
```

**CP8 - Documentation:**
- Generate API documentation
- Update README files
- Create deployment guide

**CP9 - Validation:**
- Full traceability verification
- Test coverage report
- Quality metrics summary

**Outputs:**
- `Implementation_X/docs/API_DOCUMENTATION.md`
- `Implementation_X/docs/DEPLOYMENT_GUIDE.md`
- `Implementation_X/reports/VALIDATION_REPORT.md`
- `Implementation_X/reports/IMPLEMENTATION_SUMMARY.md`

---

## Utility Commands

### `/htec-sdd-status`

Shows current implementation progress:

```bash
/htec-sdd-status
/htec-sdd-status InventorySystem
```

**Output:**
```
Implementation Status: InventorySystem
═══════════════════════════════════════
Current Checkpoint: 5 (Implementation - P0 Complete)
Progress: 67% (42/63 tasks)

Tasks by Status:
  ✓ Completed: 42
  ◐ In Progress: 3
  ○ Pending: 18

Test Coverage: 84%
Review Status: Pending (CP6)

Next: Run /htec-sdd-review to proceed
```

### `/htec-sdd-reset`

Reset implementation state:

```bash
/htec-sdd-reset              # Soft reset (keep code, reset state)
/htec-sdd-reset --hard       # Delete all implementation outputs
/htec-sdd-reset --checkpoint 3  # Reset to specific checkpoint
```

---

## Quality Gates

```bash
# List all checkpoints
python3 .claude/hooks/implementation_quality_gates.py --list-checkpoints

# Validate specific checkpoint
python3 .claude/hooks/implementation_quality_gates.py --validate-checkpoint 6 --dir Implementation_X/

# Validate task completion
python3 .claude/hooks/implementation_quality_gates.py --validate-task T-015 --dir Implementation_X/
```

---

## State Files

All state files are at **PROJECT ROOT** level in `_state/`:

| File | Purpose |
|------|---------|
| `implementation_config.json` | Configuration and settings |
| `implementation_progress.json` | Checkpoint progress |
| `implementation_input_validation.json` | Input validation results |

---

## Traceability

Implementation maintains full traceability:

```
PP-1.1 (Pain Point)
    ↓
JTBD-1.1 (Job To Be Done)
    ↓
REQ-001 (Requirement)
    ↓
MOD-MOB-INV-01 (Module Spec)
    ↓
T-015 (Implementation Task)
    ↓
barcode-scanner.ts:45 (Code Location)
    ↓
barcode-scanner.test.ts (Test File)
```

**Registry:** `traceability/task_registry.json`

---

## Integration with JIRA

Tasks include `jira_ref` field linking to JIRA items:

```json
{
  "id": "T-015",
  "jira_ref": "INV-015",
  "module_ref": "MOD-MOB-INV-01"
}
```

This enables:
- Human tracking via JIRA
- AI execution via htec-sdd
- Unified reporting

---

## Parallel Execution

Tasks marked with `[P]` can run in parallel:

```
Phase 3 (Infrastructure):
  T-001 [P] Setup project structure
  T-002 [P] Configure TypeScript
  T-003 [P] Setup testing framework
  T-004 [P] Configure linting
  ─────────────────────────────────
  T-005     Setup CI/CD (depends: T-001..T-004)
```

**Coordination:**
- File-based locking prevents conflicts
- Dependency graph ensures correct order
- Max 3 parallel agents by default

---

## Skills Used

| Skill | Purpose |
|-------|---------|
| `Implementation_TaskDecomposer` | Module → Task breakdown |
| `Implementation_Developer` | TDD implementation |
| `Implementation_CodeReview` | Multi-agent review |
| `Implementation_Integrator` | Integration testing |
| `Implementation_Documenter` | API/deployment docs |

---

## Example Workflow

```bash
# 1. Initialize
/htec-sdd-init InventorySystem

# 2. Validate inputs (blocking)
/htec-sdd-validate InventorySystem

# 3. Decompose into tasks
/htec-sdd-tasks InventorySystem

# 4. Implement with TDD
/htec-sdd-implement InventorySystem --parallel

# 5. Code review (blocking)
/htec-sdd-review InventorySystem

# 6. Integration tests
/htec-sdd-integrate InventorySystem

# 7. Finalize
/htec-sdd-finalize InventorySystem
```

Or run everything:

```bash
/htec-sdd InventorySystem
```

---

## Worktree Workflow Example

**Goal**: Parallel PR-based development with isolated worktrees.

### Step 1: Generate Tasks with PR Grouping

```bash
/htec-sdd-tasks InventorySystem
```

**Interactive prompts** (presented by planning-tech-lead):
1. **Decomposition approach**: Vertical slicing / Layer-by-layer / Feature-by-feature / Hybrid
2. **PR grouping**: Per-task / Per-story / Per-epic / Per-phase
3. **Worktree strategy**: Single branch / Per-task worktrees / Per-PR worktrees
4. **Review strategy**: Per-PR / Batch review / Milestone review

**User selects**: "Vertical slicing", "Per-story", "Per-PR worktrees", "Per-PR"

**Output**:
- `traceability/task_registry.json` - Tasks grouped into PR groups
- `Implementation_InventorySystem/scripts/setup-worktrees.sh` - Executable script
- `Implementation_InventorySystem/pr-metadata/PR-001.md` through `PR-008.md`

### Step 2: Create Worktrees

```bash
/htec-sdd-worktree-setup InventorySystem
# Or with custom base branch:
/htec-sdd-worktree-setup InventorySystem --base develop
```

**Creates worktrees**:
```
../worktrees/
├── pr-001-auth/          (feature/pr-001-auth)
├── pr-002-inventory/     (feature/pr-002-inventory)
├── pr-003-reports/       (feature/pr-003-reports)
└── pr-004-settings/      (feature/pr-004-settings)
```

### Step 3: Parallel Implementation

**Terminal 1** (PR-001):
```bash
cd ../worktrees/pr-001-auth
/htec-sdd-implement InventorySystem
# Auto-detects: PR-001, executes T-001, T-002, T-003
```

**Terminal 2** (PR-002, parallel):
```bash
cd ../worktrees/pr-002-inventory
/htec-sdd-implement InventorySystem
# Auto-detects: PR-002, executes T-010..T-017
```

**Both can run simultaneously** - worktree-scoped file locks prevent false conflicts.

### Step 4: PR-Scoped Quality Review

```bash
cd ../worktrees/pr-001-auth
/htec-sdd-review InventorySystem --pr-group PR-001
# Spawns 6 quality agents (bug-hunter, security, etc.)
# Reviews only files in PR-001 metadata
```

### Step 5: Create Pull Request

```bash
cd ../worktrees/pr-001-auth
git add .
git commit -m "feat(auth): User authentication system"
git push -u origin feature/pr-001-auth

# Create PR with traceability
gh pr create --title "feat(auth): User authentication system" \
  --body "$(cat ../../Implementation_InventorySystem/pr-metadata/PR-001.md)"
```

### Benefits

| Benefit | Description |
|---------|-------------|
| **True Parallelism** | Multiple developers/agents modify "same" files in different worktrees |
| **Clean PRs** | Each PR has isolated branch and changes |
| **Fast Reviews** | PR-scoped quality checks review only changed files |
| **Registry Safety** | Shared files (_state/, traceability/) remain sequentially coordinated |
| **Easy Cleanup** | `git worktree remove` after merge |

### Cleanup After Merge

```bash
# After PR is merged
cd /path/to/main/project
git worktree remove ../worktrees/pr-001-auth
git branch -d feature/pr-001-auth
```

---
