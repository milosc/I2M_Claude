# Code Review Architecture - Two-Level Review System

**Version**: 1.0.0
**Last Updated**: 2026-01-30
**Status**: Active
**Purpose**: Document the dual-layer code review system and correct error handling behavior

---

## Overview

The HTEC Implementation framework implements a **two-level code review architecture**:

1. **Task-Level Review** - Built into each task's execution (Phase 6 of `/htec-sdd-implement`)
2. **Batch-Level Review** - Separate checkpoint command (`/htec-sdd-review`)

Understanding this distinction is critical for proper workflow execution and debugging.

---

## Level 1: Task-Level Review (Phase 6)

### When It Runs

Task-level review executes automatically as **Phase 6** within the `/htec-sdd-implement` command, after the TDD implementation phase (Phase 4) completes successfully.

### What It Does

Spawns **6 parallel quality agents**:

| Agent | Focus Area |
|-------|------------|
| `quality-bug-hunter` | Logic errors, null safety, edge cases |
| `quality-security-auditor` | OWASP Top 10, injection, auth issues |
| `quality-code-quality` | SOLID, DRY, complexity, naming |
| `quality-test-coverage` | Missing tests, AC coverage, edge cases |
| `quality-contracts-reviewer` | API contract compliance, type safety |
| `quality-accessibility-auditor` | WCAG 2.1 AA, ARIA, keyboard navigation |

### Scope

- **Per-task**: Reviews only the files created/modified by that specific task
- **Worktree-scoped**: When running in a worktree, reviews are isolated to that PR's changes

### Blocking Behavior

If **CRITICAL** issues are found:
- Phase 6 fails
- Task is marked as blocked
- Subsequent phases (7-8) do not execute for that task

### Prerequisite

**Phase 6 only runs if Phase 4 (TDD Implementation) succeeds.** If builds fail, Phase 6 is skipped entirely.

---

## Level 2: Batch-Level Review (`/htec-sdd-review`)

### When It Runs

This is a **separate command** executed manually after completing a batch of tasks or a PR-group. It represents **Checkpoint 6** in the implementation workflow.

### What It Does

- Reviews all changed files across the completed batch/PR-group
- Consolidates findings from multiple tasks
- Generates comprehensive review reports
- Acts as a **BLOCKING gate** before `/htec-sdd-integrate`

### Command Options

```bash
/htec-sdd-review InventorySystem                    # Review all changed files
/htec-sdd-review InventorySystem --scope changed    # Review only changed files (default)
/htec-sdd-review InventorySystem --scope all        # Review entire codebase
/htec-sdd-review InventorySystem --agent security   # Run specific agent only
/htec-sdd-review InventorySystem --pr-group PR-001  # Review specific PR group
```

### Blocking Criteria

The command **blocks progression** if:
- Any CRITICAL findings exist
- Any HIGH findings with confidence > 80%
- Test coverage < 80%

### Outputs

- `Implementation_X/reports/CODE_REVIEW.md` - Human-readable findings
- `Implementation_X/reports/review-findings.json` - Machine-readable format
- `traceability/review_registry.json` - Updated registry

---

## Comparison Table

| Aspect | Task-Level (Phase 6) | Batch-Level (`/htec-sdd-review`) |
|--------|---------------------|----------------------------------|
| **Trigger** | Automatic (within `/htec-sdd-implement`) | Manual command |
| **Scope** | Single task's files | All changed files in batch/PR |
| **Checkpoint** | N/A (internal phase) | Checkpoint 6 (BLOCKING) |
| **Prerequisite** | Phase 4 (TDD) must pass | Tasks must be implemented |
| **Purpose** | Immediate feedback per task | Gate before integration |
| **When to Use** | Automatic | After batch completion |

---

## Error Handling: Failed Builds

### The Problem

If builds fail during `/htec-sdd-implement`:

1. Phase 4 (TDD Implementation) fails or produces incomplete code
2. Phase 6 (Task-Level Review) is **skipped** (no code to review)
3. The orchestrator may still suggest running `/htec-sdd-review`

**This suggestion is incorrect** because:
- No working code exists to review
- The batch-level review would find nothing meaningful
- The workflow sequence is broken

### Current Behavior (Gap)

The orchestrator follows the checkpoint sequence (CP3-5 → CP6) even when tasks didn't complete successfully. This is a workflow gap that should be addressed.

### Correct User Action When Builds Fail

**Do NOT run `/htec-sdd-review`.** Instead:

1. **Investigate Failures**
   ```bash
   # Check task-specific logs
   ls Implementation_ERTriage/01-tasks/T-XXX/results/
   cat Implementation_ERTriage/01-tasks/T-XXX/results/build.log
   cat Implementation_ERTriage/01-tasks/T-XXX/results/test.log
   ```

2. **Identify Root Cause**
   - Dependency issues (missing packages)
   - Type errors (TypeScript compilation)
   - Environment problems (missing config)
   - Test failures (logic errors)

3. **Fix and Retry Failed Tasks**
   ```bash
   # Retry specific failed task
   /htec-sdd-implement ERTriage --task T-XXX

   # Or retry entire PR group
   /htec-sdd-implement ERTriage --pr-group PR-XXX
   ```

4. **Run Review Only After Success**
   ```bash
   # Only after tasks build successfully
   /htec-sdd-review ERTriage
   ```

---

## Decision Flow: When to Run `/htec-sdd-review`

```
Did /htec-sdd-implement complete tasks successfully?
│
├── YES (builds pass, tests pass)
│   └── ✅ Run /htec-sdd-review
│
└── NO (builds fail or tests fail)
    │
    ├── Some tasks passed, some failed
    │   └── Fix failed tasks first, then /htec-sdd-review
    │
    └── All tasks failed
        └── ❌ Do NOT run /htec-sdd-review
            └── Investigate and fix build issues first
```

---

## Recommended Orchestrator Enhancement

### Current Gap

The orchestrator suggests `/htec-sdd-review` based on checkpoint progression, ignoring task success state.

### Proposed Fix

The orchestrator should:

1. **Check task completion status** before suggesting next command
2. **Conditional suggestion logic**:
   ```
   IF all_tasks_in_batch == "completed":
       suggest "/htec-sdd-review"
   ELIF some_tasks == "completed" AND some_tasks == "failed":
       suggest "Fix failed tasks: T-XXX, T-YYY, then run /htec-sdd-review"
   ELSE (all_tasks == "failed"):
       suggest "Investigate build failures in 01-tasks/T-XXX/results/"
       DO NOT suggest "/htec-sdd-review"
   ```

3. **Display failure summary**:
   ```
   ⚠️ Build Failures Detected

   Failed Tasks: T-018, T-019, T-020
   Passed Tasks: None

   Next Steps:
   1. Check logs: Implementation_ERTriage/01-tasks/T-018/results/build.log
   2. Fix root cause
   3. Retry: /htec-sdd-implement ERTriage --task T-018

   Do NOT run /htec-sdd-review until builds pass.
   ```

### Implementation Location

This enhancement should be added to:
- `.claude/commands/htec-sdd-implement.md` - Final output section
- `.claude/agents/implementation-task-orchestrator.md` - Result consolidation logic

---

## Related Documentation

| Document | Purpose |
|----------|---------|
| `Task_Execution_Flow_Detailed.md` | Full 8-phase workflow breakdown |
| `HTEC_SDD_COMMAND_REFERENCE.md` | All implementation commands |
| `Parallel_Agent_Coordination.md` | Multi-agent execution patterns |
| `Implementation_Architecture.md` | Overall implementation design |

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-30 | Claude | Initial documentation of two-level review architecture |

---

**Key Takeaway**: Task-level review (Phase 6) provides immediate per-task feedback when builds succeed. Batch-level review (`/htec-sdd-review`) is a separate gate for PR/batch completion. Never run batch-level review when builds are failing - fix the builds first.
