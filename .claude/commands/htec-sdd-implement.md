---
description: Orchestrate complete implementation workflow with specialized agents
argument-hint: <SystemName> [options]
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-implement started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-implement ended '{"stage": "implementation"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Validate session (WARNING only - won't block execution)
python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/validate_session.py" --warn-only || true

# 2. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "implementation"

# 3. Log command start
bash .claude/hooks/log-lifecycle.sh command /htec-sdd-implement instruction_start '{"stage": "implementation", "method": "orchestration-based"}'

**Note**: If you see session validation warnings above, run `/project-init` to fix them.
```


---

## 🎯 Guiding Architectural Principle

**Optimize for maintainability, not simplicity.**

When making architectural and implementation decisions:

1. **Prioritize long-term maintainability** over short-term simplicity
2. **Minimize complexity** by being strategic with dependencies and libraries
3. **Avoid "simplicity traps"** - adding libraries without considering downstream debugging and maintenance burden
4. **Think 6 months ahead** - will this decision make debugging easier or harder?
5. **Use libraries strategically** - not avoided, but chosen carefully with justification

### Decision-Making Protocol

When facing architectural trade-offs between complexity and maintainability:

**If the decision is clear** → Make the decision autonomously and document the rationale

**If the decision is unclear** → Use `AskUserQuestion` tool with:
- Minimum 3 alternative scenarios
- Clear trade-off analysis for each option
- Maintainability impact assessment (short-term vs long-term)
- Complexity implications (cognitive load, debugging difficulty, dependency graph)
- Recommendation with reasoning

---

## Rules Loading (On-Demand)

This command requires Implementation stage rules:

```bash
# Load TDD and quality gate rules
/rules-process-integrity

# Load multi-agent coordination rules
/rules-agent-coordination

# Load Traceability rules
/rules-traceability
```

---

## Overview

**Philosophy**: `/htec-sdd-implement` is a **comprehensive orchestrator** that manages the complete implementation workflow from codebase research through PR preparation, using specialized agents for each phase.

**Scope**: Task-based or PR-based execution (narrow scope, comprehensive process)

---

## Usage

```bash
# Single task (comprehensive orchestration)
/htec-sdd-implement <SystemName> --task T-001

# PR group (all tasks in group)
/htec-sdd-implement <SystemName> --pr-group PR-001

# Auto-detect from worktree
cd ../worktrees/pr-001-auth
/htec-sdd-implement <SystemName>  # Auto-detects PR-001

# Batch processing
/htec-sdd-implement <SystemName> --batch 5 --parallel

# Priority filter
/htec-sdd-implement <SystemName> --priority P0

# Phase-specific
/htec-sdd-implement <SystemName> --phase 3
```

---

## Arguments

- `<SystemName>`: Name of the system (e.g., InventorySystem)

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--task <T-ID>` | Execute specific task only | All pending |
| `--pr-group <PR-ID>` | Execute PR group | Auto-detect or all |
| `--batch <N>` | Max concurrent tasks | 2 |
| `--parallel` | Enable parallel agent execution | true |
| `--isolate-tasks` | **Spawn agent per task (prevents context rot)** | **true** |
| `--priority <P0\|P1\|P2>` | Filter by priority | All |
| `--phase <N>` | Target specific phase | All phases |
| `--skip-research` | Skip codebase research | false |
| `--skip-review` | Skip quality review | false |

---

## Prerequisites

- ✅ `/htec-sdd-tasks` completed (task registry populated)
- ✅ ProductSpecs Stage 3 completed (CP8+)
- ✅ SolArch Stage 4 completed (CP12+)

---

## Orchestration Flow

This command orchestrates 8 phases with specialized agents:

```
┌─────────────────────────────────────────────────────────┐
│         /htec-sdd-implement ORCHESTRATION FLOW          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Phase 0: Context Detection & Registry Loading         │
│  ├─ Detect worktree & PR group                         │
│  └─ Load task registry & config                        │
│                                                         │
│  Phase 1: Codebase Research                            │
│  ├─ Agent: planning-code-explorer                      │
│  └─ Analyze patterns, conventions, architecture        │
│                                                         │
│  Phase 2: Implementation Planning                      │
│  ├─ Agent: planning-tech-lead                          │
│  └─ Generate detailed implementation plan              │
│                                                         │
│  Phase 3: Test Design                                  │
│  ├─ Agent: implementation-test-designer                │
│  └─ Create BDD scenarios & TDD specs                   │
│                                                         │
│  Phase 4: TDD Implementation                           │
│  ├─ Agent: implementation-developer                    │
│  └─ Execute RED-GREEN-REFACTOR cycle                   │
│                                                         │
│  Phase 5: Test Automation                              │
│  ├─ Agent: implementation-test-automation-engineer     │
│  └─ E2E tests, integration tests, Playwright           │
│                                                         │
│  Phase 6: Quality Review (parallel)                    │
│  ├─ Agents: quality-bug-hunter                         │
│  │           quality-security-auditor                  │
│  │           quality-code-quality                      │
│  │           quality-test-coverage                     │
│  │           quality-contracts-reviewer                │
│  │           quality-accessibility-auditor             │
│  └─ Comprehensive quality assessment                   │
│                                                         │
│  Phase 7: Documentation & PR Prep                      │
│  ├─ Agent: implementation-documenter                   │
│  ├─ Agent: implementation-pr-preparer                  │
│  └─ Generate docs & PR description                     │
│                                                         │
│  Phase 8: Finalization                                 │
│  ├─ Update task registry                               │
│  ├─ Log traceability                                   │
│  └─ Report completion                                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Duration**: 10-25 minutes per task (varies by complexity)

---

## Procedure

### Phase 0: Context Detection & Task Dispatching

**Duration**: 2-3 seconds + agent spawn overhead

**IMPORTANT**: This phase determines whether to run in Task Isolation Mode (default) or Legacy Mode.

#### Step 0.1: Detect Context

First, detect worktree and PR group context:

```bash
# Detect worktree context
git worktree list | grep "$(pwd)" || echo "Not in worktree"
```

If in a worktree like `../worktrees/pr-003-websocket`, extract `PR_GROUP = "PR-003"`.

#### Step 0.2: Load Task Registry

Read the task registry to identify tasks:

```bash
cat traceability/task_registry.json | jq '.pr_groups, .tasks | keys'
```

#### Step 0.3: Build Execution Queue

Based on options provided (`--task`, `--pr-group`, `--priority`), build the task list:
- If `--task T-001` specified: Queue = `["T-001"]`
- If `--pr-group PR-003` specified: Queue = tasks from that PR group
- If auto-detected from worktree: Queue = tasks from detected PR group
- Otherwise: Queue = all pending tasks (filter by priority if specified)

#### Step 0.4: TASK ISOLATION MODE (Default: true)

**CRITICAL**: This step determines execution strategy.

**If `--isolate-tasks=false` (Legacy Mode)**:
- Continue to Phase 1-8 below, running all phases in this session
- ⚠️ WARNING: Context will accumulate across tasks, causing quality degradation

**If `--isolate-tasks=true` (Default)**:
- **DO NOT** continue to Phase 1-8 in this session
- **INSTEAD**, spawn isolated `implementation-task-orchestrator` agents
- Each task gets its own agent with fresh context
- This session becomes a lightweight dispatcher

---

### Phase 0.5: Task Isolation Dispatch (DEFAULT MODE)

**MANDATORY when `--isolate-tasks=true` (the default)**

For each task in the queue (respecting `--batch` concurrency limit), you MUST use the Task tool to spawn an isolated orchestrator agent.

**Execution Pattern**:

1. **Create results directory** for each task:
   ```bash
   mkdir -p "Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results"
   ```

2. **Spawn isolated orchestrator agent** using the Task tool:

   For EACH task, invoke the Task tool with these EXACT parameters:

   ```
   Task tool invocation:
   - subagent_type: "general-purpose"
   - model: "sonnet"
   - description: "Orchestrate implementation for <TASK_ID>"
   - run_in_background: true  (for parallel execution)
   - prompt: See template below
   ```

   **Prompt template for Task tool**:
   ```
   Agent: implementation-task-orchestrator
   Read: .claude/agents/implementation-task-orchestrator.md

   ═══════════════════════════════════════════════════════════
   TASK ORCHESTRATION REQUEST
   ═══════════════════════════════════════════════════════════

   TASK_ID: <task_id>
   SYSTEM_NAME: <system_name>
   PR_GROUP: <pr_group or "none">
   WORKTREE_PATH: <worktree_path or current directory>
   SKIP_RESEARCH: false
   SKIP_REVIEW: false

   Execute the complete 8-phase implementation workflow for this SINGLE task.
   Save ALL results to: Implementation_<system_name>/01-tasks/<task_id>/results/

   IMPORTANT:
   - You have ISOLATED context - no other tasks' data is present
   - Execute ALL 8 phases sequentially (Phase 1-8 as documented)
   - Save build/test logs to the results folder
   - Return ONLY the compact JSON summary when complete

   RETURN FORMAT:
   {
     "task_id": "<task_id>",
     "status": "completed|failed|blocked",
     "duration_seconds": <number>,
     "phases_completed": <number>,
     "results_path": "Implementation_<system_name>/01-tasks/<task_id>/results/",
     "files_created": [...],
     "files_modified": [...],
     "tests": { "passing": <n>, "failing": <n>, "coverage": <n> },
     "quality": { "critical": <n>, "high": <n>, "medium": <n> },
     "error": null
   }
   ```

3. **Track spawned agents**: Keep track of agent IDs returned by Task tool

4. **Wait for completion**: Use TaskOutput tool with `block=false` to poll, or `block=true` to wait

5. **Collect results**: Parse JSON summaries from each completed agent

6. **Consolidate and report**: Aggregate metrics and display final summary

**Concurrency Control**:
- Maximum `--batch` concurrent agents (default: 2)
- When an agent completes, spawn next task if queue not empty
- Continue until all tasks processed

**Example with 4 tasks and --batch=2**:
```
Time 0:   Spawn T-018 orchestrator, Spawn T-019 orchestrator
Time T1:  T-018 completes → Spawn T-020 orchestrator
Time T2:  T-019 completes → Spawn T-021 orchestrator
Time T3:  T-020 completes
Time T4:  T-021 completes
          → All done, consolidate results
```

**After dispatching all tasks and collecting results**:
- Display consolidated summary
- Update implementation progress
- Log to version history
- **EXIT** - do not continue to Phase 1-8 (those run inside the spawned agents)

---

### Phase 0.6: Consolidated Summary (After Isolation Dispatch)

After all task orchestrator agents complete, display:

```
═══════════════════════════════════════════════════════════
📊 TASK ISOLATION DISPATCH COMPLETE
═══════════════════════════════════════════════════════════

Task Results:
─────────────────────────────────────────────────────────────
  ✓ T-018   completed   847s   6 files   12 tests   87% cov
  ✓ T-019   completed   923s   4 files    8 tests   82% cov
  ✓ T-020   completed   756s   3 files    6 tests   91% cov
  ✓ T-021   completed   612s   2 files    4 tests   85% cov

═══════════════════════════════════════════════════════════
Summary
─────────────────────────────────────────────────────────────
  Tasks:        4/4 completed
  Total time:   3138s (wall clock lower due to parallelism)
  Files:        15 created
  Tests:        30 passing
  Quality:      0 CRITICAL, 3 HIGH
═══════════════════════════════════════════════════════════
```

Then update progress and exit.

---

**IMPORTANT**: Phases 1-8 below are executed by the `implementation-task-orchestrator` agent, NOT by this dispatcher session when in isolation mode.

---

### Phase 1: Codebase Research

**Duration**: 2-3 minutes
**Agent**: `planning-code-explorer`
**Optional**: Skip with `--skip-research` if plan exists

**Purpose**: Analyze existing codebase to understand:
- Coding patterns and conventions
- Architecture layers
- Existing similar implementations
- Dependencies and integrations

```bash
# Generate session ID
session_id="sess-$(uuidgen | cut -d'-' -f1)"

# Spawn planning-code-explorer
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Analyze codebase patterns",
  prompt: `Agent: planning-code-explorer
Read: .claude/agents/planning-code-explorer.md
SESSION: ${session_id} | TASK: ${task_id}

ANALYZE codebase for:
- Existing patterns in src/features/
- Architecture conventions (layering, naming)
- Similar implementations
- Integration points
- Dependency patterns

TARGET TASK: ${task_id}
WORKING DIR: ${working_dir}

RETURN JSON:
{
  "status": "completed",
  "patterns_found": ["pattern1", "pattern2"],
  "similar_files": ["file1.ts", "file2.ts"],
  "conventions": {...},
  "recommendations": [...]
}
`
})
```

**Output**:
```
[Phase 1: Codebase Research]
✓ Agent spawned: planning-code-explorer (sess-a7b2c4d1)
✓ Analyzed 47 files in src/features/
✓ Found 3 similar implementations:
  - src/features/user/services/user-service.ts
  - src/features/session/services/session-service.ts
✓ Patterns identified: Service layer, Repository pattern, Error handling
✓ Duration: 2m 15s
```

---

### Phase 2: Implementation Planning

**Duration**: 3-5 minutes
**Agent**: `planning-tech-lead`

**Purpose**: Generate detailed implementation plan using:
- Task specification
- Module specification
- Codebase research results
- ADR references

```bash
# Spawn planning-tech-lead
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate implementation plan",
  prompt: `Agent: planning-tech-lead
Read: .claude/agents/planning-tech-lead.md
SESSION: ${session_id} | TASK: ${task_id}

TASK SPEC:
${read_file('Implementation_${system}/01-tasks/${task_id}.md')}

MODULE SPEC:
${read_file('ProductSpecs_${system}/01-modules/${module_id}.md')}

CODEBASE RESEARCH:
${phase1_results}

GENERATE detailed implementation plan:
- Step-by-step actions
- Exact file paths
- Dependencies to install
- Verification commands
- TDD approach

OUTPUT: Implementation_${system}/docs/featureImplementationplans/${date}-${task_id}.md

RETURN JSON:
{
  "status": "completed",
  "plan_file": "...",
  "steps_count": 8,
  "files_to_create": [...],
  "files_to_modify": [...]
}
`
})
```

**Output**:
```
[Phase 2: Implementation Planning]
✓ Agent spawned: planning-tech-lead (sess-b8c3d5e2)
✓ Plan generated: featureImplementationplans/2026-01-26-T-001-auth-service.md
✓ Steps: 8
✓ Files to create: 2
✓ Files to modify: 1
✓ Duration: 3m 42s
```

---

### Phase 3: Test Design

**Duration**: 4-6 minutes
**Agent**: `implementation-test-designer` (NEW)

**Purpose**: Design comprehensive test specifications BEFORE coding:
- BDD scenarios (Given-When-Then)
- TDD test cases
- Test data fixtures
- Edge cases and error paths

```bash
# Spawn implementation-test-designer
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Design test specifications",
  prompt: `Agent: implementation-test-designer
Read: .claude/agents/implementation-test-designer.md
SESSION: ${session_id} | TASK: ${task_id}

TASK SPEC:
${read_file('Implementation_${system}/01-tasks/${task_id}.md')}

MODULE SPEC:
${read_file('ProductSpecs_${system}/01-modules/${module_id}.md')}

ACCEPTANCE CRITERIA:
${acceptance_criteria}

CREATE test specifications:
- BDD scenarios for each AC
- Unit test cases
- Integration test specs
- E2E test specs (Playwright)
- Test data fixtures

OUTPUT: Implementation_${system}/02-implementation/test-specs/${task_id}-test-spec.md

RETURN JSON:
{
  "status": "completed",
  "test_spec_file": "...",
  "bdd_scenarios_count": 5,
  "unit_tests_count": 12,
  "integration_tests_count": 3,
  "e2e_tests_count": 2
}
`
})
```

**Output**:
```
[Phase 3: Test Design]
✓ Agent spawned: implementation-test-designer (sess-c9d4e6f3)
✓ Test spec created: test-specs/T-001-test-spec.md
✓ BDD scenarios: 5
✓ Unit tests: 12
✓ Integration tests: 3
✓ E2E tests: 2
✓ All ACs covered
✓ Duration: 4m 28s
```

---

### Phase 4: TDD Implementation

**Duration**: 8-15 minutes
**Agent**: `implementation-developer`

**Purpose**: Execute test-driven development cycle:
- RED: Write failing tests
- GREEN: Minimal implementation
- REFACTOR: Code cleanup
- VERIFY: Full test suite
- MARK: Update registry

```bash
# Spawn implementation-developer
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Implement via TDD",
  prompt: `Agent: implementation-developer
Read: .claude/agents/implementation-developer.md
SESSION: ${session_id} | TASK: ${task_id}

IMPLEMENTATION PLAN:
${read_file(plan_file)}

TEST SPECIFICATION:
${read_file(test_spec_file)}

CODEBASE PATTERNS:
${phase1_results}

EXECUTE TDD cycle:
1. RED: Write failing tests (from test spec)
2. GREEN: Minimal implementation
3. REFACTOR: Clean up code
4. VERIFY: Full test suite
5. MARK: Update registry

WORKING DIR: ${working_dir}
WORKTREE PATH: ${worktree_path}

RETURN JSON:
{
  "status": "completed",
  "files_created": [...],
  "files_modified": [...],
  "tests_created": [...],
  "test_results": {
    "passing": 12,
    "failing": 0,
    "coverage": 87
  }
}
`
})
```

**Output**:
```
[Phase 4: TDD Implementation]
✓ Agent spawned: implementation-developer (sess-d0e5f7g4)

  RED Phase:
  ✓ Created: tests/unit/auth/auth-service.test.ts
  ✓ Tests fail as expected (12 failing)

  GREEN Phase:
  ✓ Created: src/features/auth/services/auth-service.ts (87 lines)
  ✓ Tests pass (12 passing)

  REFACTOR Phase:
  ✓ Extracted method: isValidTokenStructure()
  ✓ Tests still pass

  VERIFY Phase:
  ✓ Full suite: 156 passing, 0 failing
  ✓ Coverage: 87%

  MARK Phase:
  ✓ Task T-001 marked complete
  ✓ Registry updated

✓ Duration: 12m 34s
```

---

### Phase 5: Test Automation

**Duration**: 5-8 minutes
**Agent**: `implementation-test-automation-engineer`

**Purpose**: Create additional automated tests:
- E2E tests (Playwright)
- Integration tests
- API tests
- Visual regression tests (if UI)

```bash
# Spawn implementation-test-automation-engineer
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Create E2E and integration tests",
  prompt: `Agent: implementation-test-automation-engineer
Read: .claude/agents/implementation-test-automation-engineer.md
SESSION: ${session_id} | TASK: ${task_id}

TEST SPECIFICATION:
${read_file(test_spec_file)}

IMPLEMENTED FILES:
${phase4_results.files_created}

CREATE automated tests:
- E2E tests using Playwright
- Integration tests for API endpoints
- Visual regression tests (if UI)

TEST DATA:
${test_spec_fixtures}

RETURN JSON:
{
  "status": "completed",
  "e2e_tests_created": [...],
  "integration_tests_created": [...],
  "test_results": {...}
}
`
})
```

**Output**:
```
[Phase 5: Test Automation]
✓ Agent spawned: implementation-test-automation-engineer (sess-e1f6g8h5)
✓ E2E tests created: 2
  - tests/e2e/auth/login-flow.spec.ts
  - tests/e2e/auth/token-expiration.spec.ts
✓ Integration tests created: 3
  - tests/integration/auth/auth-api.test.ts
✓ All tests passing
✓ Duration: 6m 18s
```

---

### Phase 6: Quality Review (Parallel)

**Duration**: 3-5 minutes (parallel execution)
**Agents**: 6 specialized quality agents (parallel)

**Purpose**: Comprehensive quality assessment from multiple perspectives

```bash
# Spawn quality agents in parallel
agents=(
  "quality-bug-hunter"
  "quality-security-auditor"
  "quality-code-quality"
  "quality-test-coverage"
  "quality-contracts-reviewer"
  "quality-accessibility-auditor"
)

for agent in "${agents[@]}"; do
  Task({
    subagent_type: "general-purpose",
    model: "sonnet",
    description: "Quality review: $agent",
    run_in_background: true,
    prompt: `Agent: $agent
Read: .claude/agents/$agent.md
SESSION: ${session_id} | TASK: ${task_id}

REVIEW FILES:
${phase4_results.files_created}

PR GROUP: ${pr_group}
WORKTREE SCOPED: ${worktree_path}

RETURN JSON:
{
  "status": "completed",
  "findings": [...],
  "critical_count": 0,
  "high_count": 2,
  "recommendations": [...]
}
`
  })
done

# Wait for all agents to complete
for agent_id in "${agent_ids[@]}"; do
  result=$(TaskOutput "$agent_id" block=true)
  # Collect findings
done

# Consolidate findings
consolidate_quality_findings
```

**Output**:
```
[Phase 6: Quality Review]
✓ Spawned 6 quality agents (parallel)

  quality-bug-hunter:
  ✓ No CRITICAL issues
  ⚠ 2 HIGH issues (null handling)

  quality-security-auditor:
  ✓ No CRITICAL issues
  ✓ OWASP Top 10 compliant

  quality-code-quality:
  ✓ SOLID principles followed
  ✓ No code duplication

  quality-test-coverage:
  ✓ Coverage: 87% (target: 80%)
  ✓ All ACs covered

  quality-contracts-reviewer:
  ✓ API contracts satisfied
  ✓ Type safety verified

  quality-accessibility-auditor:
  ✓ WCAG 2.1 AA compliant
  ✓ ARIA attributes correct
  ⚠ 1 MEDIUM issue (focus management)

✓ Consolidated: 0 CRITICAL, 2 HIGH, 6 MEDIUM
✓ Duration: 4m 12s (parallel)
```

---

### Phase 7: Documentation & PR Prep

**Duration**: 3-5 minutes
**Agents**: `implementation-documenter`, `implementation-pr-preparer`

**Purpose**: Generate comprehensive documentation and PR materials

```bash
# Spawn implementation-documenter
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate documentation",
  prompt: `Agent: implementation-documenter
Read: .claude/agents/implementation-documenter.md
SESSION: ${session_id} | TASK: ${task_id}

IMPLEMENTED FILES:
${phase4_results.files_created}

GENERATE:
- Inline JSDoc/TSDoc
- Module README (_readme.md convention)
- API documentation
- Usage examples
- Architecture diagrams (Mermaid)

RETURN JSON:
{
  "status": "completed",
  "documentation_files": [...],
  "inline_docs_updated": [...]
}
`
})

# Spawn implementation-pr-preparer
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Prepare PR description",
  prompt: `Agent: implementation-pr-preparer
Read: .claude/agents/implementation-pr-preparer.md
SESSION: ${session_id} | TASK: ${task_id}

PR GROUP: ${pr_group}
TASKS COMPLETED: ${completed_tasks}
FILES CHANGED: ${all_files_changed}
TEST RESULTS: ${consolidated_test_results}
QUALITY FINDINGS: ${quality_findings}

GENERATE:
- PR description with full context
- Change summary with file tree
- Testing checklist
- Traceability links
- Review guidance

OUTPUT: Implementation_${system}/pr-metadata/${pr_group}-description.md

RETURN JSON:
{
  "status": "completed",
  "pr_description_file": "...",
  "pr_title": "feat(auth): User authentication system",
  "pr_branch": "feature/pr-001-auth"
}
`
})
```

**Output**:
```
[Phase 7: Documentation & PR Prep]

  implementation-documenter:
  ✓ Agent spawned (sess-f2g7h9i6)
  ✓ Inline docs added to 2 files
  ✓ Module README created: src/features/auth/_readme.md
  ✓ API docs created: 05-documentation/api/auth.md
  ✓ Mermaid diagrams: 2

  implementation-pr-preparer:
  ✓ Agent spawned (sess-g3h8i0j7)
  ✓ PR description: pr-metadata/PR-001-description.md
  ✓ PR title: feat(auth): User authentication system
  ✓ Change summary: 6 files, +388 lines
  ✓ Traceability complete

✓ Duration: 4m 05s
```

---

### Phase 8: Finalization

**Duration**: 5-10 seconds

```bash
# Update task registry (final consolidation)
update_task_registry_final

# Log version history
python3 .claude/hooks/version_history_logger.py \
  "traceability/" \
  "${system_name}" \
  "implementation" \
  "implementation-orchestrator" \
  "1.0.0" \
  "Completed task ${task_id} via full orchestration" \
  "${traceability_refs}" \
  "traceability/task_registry.json" \
  "modification"

# Update progress
update_implementation_progress

# Generate summary report
generate_completion_report
```

**Output**:
```
[Phase 8: Finalization]
✓ Task registry updated
✓ Version history logged
✓ Progress updated: 23/47 tasks (49%)
✓ Checkpoint: 4 (Features 50%+)
```

---

## Final Output

```
═══════════════════════════════════════════════════════════
✅ Implementation Complete: T-001
═══════════════════════════════════════════════════════════

Duration: 23m 47s

Phases Completed:
  ✓ Phase 1: Codebase Research (2m 15s)
  ✓ Phase 2: Implementation Planning (3m 42s)
  ✓ Phase 3: Test Design (4m 28s)
  ✓ Phase 4: TDD Implementation (12m 34s)
  ✓ Phase 5: Test Automation (6m 18s)
  ✓ Phase 6: Quality Review (4m 12s, parallel)
  ✓ Phase 7: Documentation & PR Prep (4m 05s)
  ✓ Phase 8: Finalization (10s)

Files Created:
  - src/features/auth/services/auth-service.ts (87 lines)
  - tests/unit/auth/auth-service.test.ts (64 lines)
  - tests/e2e/auth/login-flow.spec.ts (42 lines)
  - tests/integration/auth/auth-api.test.ts (38 lines)
  - src/features/auth/_readme.md
  - 05-documentation/api/auth.md

Quality Metrics:
  Tests: 17 passing (12 unit, 3 integration, 2 E2E)
  Coverage: 87% (target: 80%)
  Quality Issues: 0 CRITICAL, 2 HIGH, 5 MEDIUM

Documentation:
  ✓ Inline docs complete
  ✓ Module README generated
  ✓ API docs generated
  ✓ PR description ready

Traceability:
  Pain Points: PP-1.1, PP-1.2 ✅
  Requirements: REQ-001, REQ-002, REQ-003 ✅
  User Story: US-001 ✅
  Module: MOD-AUTH-01 ✅
  ADRs: ADR-007 ✅

Next Steps:
  1. Review quality findings (2 HIGH issues)
  2. Continue with T-002 (or run /htec-sdd-implement --task T-002)
  3. Or run code review batch after multiple tasks: /htec-sdd-review

PR Ready:
  Branch: feature/pr-001-auth
  Title: feat(auth): User authentication system
  Description: Implementation_InventorySystem/pr-metadata/PR-001-description.md
═══════════════════════════════════════════════════════════
```

---
When `--parallel` flag is not used the default value is 'true'

## Parallel Execution (--parallel)

When `--parallel` flag is used:

```bash
# Execute multiple tasks in parallel
BATCH=$(get_parallel_tasks "$QUEUE" $MAX_CONCURRENT)

for task in "${BATCH[@]}"; do
  # Each task runs full orchestration in background
  /htec-sdd-implement "$SYSTEM_NAME" --task "$task" &
done

# Wait for all to complete
wait

# Consolidate results
consolidate_batch_results
```

**Note**: Worktree-scoped locking prevents conflicts when modifying "same" files in different worktrees.

---

## Quality Gate

After Phase 6 (Quality Review), check if progression should be blocked:

```bash
if [ $CRITICAL_COUNT -gt 0 ]; then
  echo "❌ QUALITY GATE FAILED: $CRITICAL_COUNT CRITICAL issues"
  echo "   Fix issues before proceeding"
  exit 1
fi

if [ $HIGH_COUNT -gt 5 ]; then
  echo "⚠️  WARNING: $HIGH_COUNT HIGH issues"
  echo "   Recommend fixing before continuing"
  # Prompt user
fi
```

---

## Files Created

- Source code in `Implementation_<System>/src/`
- Tests in `Implementation_<System>/tests/`
- Test specs in `Implementation_<System>/02-implementation/test-specs/`
- Documentation in `Implementation_<System>/05-documentation/`
- Module READMEs in `src/features/<feature>/_readme.md`
- PR descriptions in `Implementation_<System>/pr-metadata/`
- Updated `traceability/task_registry.json`
- Updated `traceability/<system>_version_history.json`

---

## Agents Used

1. **planning-code-explorer** - Codebase research
2. **planning-tech-lead** - Implementation planning
3. **implementation-test-designer** - Test design
4. **implementation-developer** - TDD implementation
5. **implementation-test-automation-engineer** - E2E & integration tests
6. **quality-bug-hunter** - Bug detection
7. **quality-security-auditor** - Security review
8. **quality-code-quality** - Code quality
9. **quality-test-coverage** - Coverage analysis
10. **quality-contracts-reviewer** - Contract compliance
11. **quality-accessibility-auditor** - WCAG 2.1 AA compliance
12. **implementation-documenter** - Documentation
13. **implementation-pr-preparer** - PR preparation

---

## Task Dispatching Functions (Isolation Mode)

When `--isolate-tasks=true` (default), these functions handle spawning and managing task orchestrator agents.

### dispatch_isolated_tasks()

**Purpose**: Spawn isolated `implementation-task-orchestrator` agents for each task, respecting concurrency limits.

```bash
dispatch_isolated_tasks() {
    local queue="$1"           # Space-separated task IDs
    local max_concurrent="$2"  # Max parallel agents
    local system_name="$3"
    local pr_group="$4"
    local worktree_path="$5"

    local tasks=($queue)
    local active_agents=()
    local active_task_ids=()
    local completed_summaries=()
    local total_tasks=${#tasks[@]}
    local completed_count=0

    echo "═══════════════════════════════════════════════════════════"
    echo "🚀 Starting Task Isolation Dispatch"
    echo "   Total tasks: $total_tasks"
    echo "   Max concurrent: $max_concurrent"
    echo "═══════════════════════════════════════════════════════════"
    echo ""

    for task_id in "${tasks[@]}"; do
        # Wait if at max concurrent
        while [ ${#active_agents[@]} -ge $max_concurrent ]; do
            check_completed_agents
            sleep 2
        done

        # Create results directory
        mkdir -p "Implementation_${system_name}/01-tasks/${task_id}/results"

        # Spawn isolated orchestrator for this task
        echo "🚀 Spawning orchestrator for $task_id..."

        agent_id=$(spawn_task_orchestrator "$task_id" "$system_name" "$pr_group" "$worktree_path")

        active_agents+=("$agent_id")
        active_task_ids+=("$task_id")

        echo "   Agent ID: $agent_id"
    done

    # Wait for remaining agents
    echo ""
    echo "⏳ Waiting for ${#active_agents[@]} remaining task(s)..."

    while [ ${#active_agents[@]} -gt 0 ]; do
        check_completed_agents
        sleep 2
    done

    # Consolidate and report
    echo ""
    consolidate_task_summaries "${completed_summaries[@]}"
}

check_completed_agents() {
    for i in "${!active_agents[@]}"; do
        agent_id="${active_agents[$i]}"
        task_id="${active_task_ids[$i]}"

        # Non-blocking check for completion
        result=$(TaskOutput "$agent_id" block=false timeout=100 2>/dev/null || echo "")

        if [ -n "$result" ] && [ "$result" != "null" ]; then
            status=$(echo "$result" | jq -r '.status // "unknown"')
            duration=$(echo "$result" | jq -r '.duration_seconds // 0')
            results_path=$(echo "$result" | jq -r '.results_path // ""')

            completed_summaries+=("$result")
            ((completed_count++))

            if [ "$status" = "completed" ]; then
                echo "✓ $task_id completed (${duration}s) - Results: $results_path"
            elif [ "$status" = "failed" ]; then
                error=$(echo "$result" | jq -r '.error // "unknown"')
                echo "✗ $task_id FAILED: $error"
            elif [ "$status" = "blocked" ]; then
                echo "⚠ $task_id BLOCKED by quality gate"
            fi

            # Remove from active lists
            unset 'active_agents[$i]'
            unset 'active_task_ids[$i]'

            # Reindex arrays
            active_agents=("${active_agents[@]}")
            active_task_ids=("${active_task_ids[@]}")
        fi
    done
}
```

### spawn_task_orchestrator()

**Purpose**: Spawn a single `implementation-task-orchestrator` agent in background.

```javascript
spawn_task_orchestrator(task_id, system_name, pr_group, worktree_path) {
    // Use Claude Code's native Task tool
    const agent_id = Task({
        subagent_type: "general-purpose",
        model: "sonnet",
        description: `Orchestrate implementation for ${task_id}`,
        run_in_background: true,
        prompt: `Agent: implementation-task-orchestrator
Read: .claude/agents/implementation-task-orchestrator.md

═══════════════════════════════════════════════════════════
TASK ORCHESTRATION REQUEST
═══════════════════════════════════════════════════════════

TASK_ID: ${task_id}
SYSTEM_NAME: ${system_name}
PR_GROUP: ${pr_group || 'none'}
WORKTREE_PATH: ${worktree_path || process.cwd()}
SKIP_RESEARCH: false
SKIP_REVIEW: false

Execute the complete 8-phase implementation workflow for this SINGLE task.
Save ALL results to: Implementation_${system_name}/01-tasks/${task_id}/results/

IMPORTANT:
- You have ISOLATED context - no other tasks' data is present
- Execute ALL 8 phases sequentially
- Save build/test logs to the results folder
- Return ONLY the compact JSON summary when complete

RETURN FORMAT:
{
  "task_id": "${task_id}",
  "status": "completed|failed|blocked",
  "duration_seconds": <number>,
  "phases_completed": <number>,
  "results_path": "Implementation_${system_name}/01-tasks/${task_id}/results/",
  "files_created": [...],
  "files_modified": [...],
  "tests": { "passing": <n>, "failing": <n>, "coverage": <n> },
  "quality": { "critical": <n>, "high": <n>, "medium": <n> },
  "error": null
}
`
    });

    return agent_id;
}
```

### consolidate_task_summaries()

**Purpose**: Aggregate results from all completed task orchestrators and generate final report.

```bash
consolidate_task_summaries() {
    local summaries=("$@")

    local total_tasks=${#summaries[@]}
    local completed=0
    local failed=0
    local blocked=0
    local total_files_created=0
    local total_tests_passing=0
    local total_critical=0
    local total_high=0
    local total_duration=0

    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "📊 TASK ISOLATION DISPATCH COMPLETE"
    echo "═══════════════════════════════════════════════════════════"
    echo ""

    echo "Task Results:"
    echo "─────────────────────────────────────────────────────────────"

    for summary in "${summaries[@]}"; do
        task_id=$(echo "$summary" | jq -r '.task_id')
        status=$(echo "$summary" | jq -r '.status')
        duration=$(echo "$summary" | jq -r '.duration_seconds // 0')
        results_path=$(echo "$summary" | jq -r '.results_path // ""')

        total_duration=$((total_duration + duration))

        if [ "$status" = "completed" ]; then
            ((completed++))
            files=$(echo "$summary" | jq -r '.files_created | length // 0')
            tests=$(echo "$summary" | jq -r '.tests.passing // 0')
            cov=$(echo "$summary" | jq -r '.tests.coverage // 0')
            printf "  ✓ %-8s completed  %4ds  %2d files  %3d tests  %3d%% cov\n" "$task_id" "$duration" "$files" "$tests" "$cov"
        elif [ "$status" = "failed" ]; then
            ((failed++))
            error=$(echo "$summary" | jq -r '.error // "unknown"')
            printf "  ✗ %-8s FAILED     %4ds  Error: %s\n" "$task_id" "$duration" "$error"
        elif [ "$status" = "blocked" ]; then
            ((blocked++))
            printf "  ⚠ %-8s BLOCKED    %4ds  Quality gate failure\n" "$task_id" "$duration"
        fi

        # Aggregate metrics
        total_files_created=$((total_files_created + $(echo "$summary" | jq -r '.files_created | length // 0')))
        total_tests_passing=$((total_tests_passing + $(echo "$summary" | jq -r '.tests.passing // 0')))
        total_critical=$((total_critical + $(echo "$summary" | jq -r '.quality.critical // 0')))
        total_high=$((total_high + $(echo "$summary" | jq -r '.quality.high // 0')))
    done

    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "Summary"
    echo "─────────────────────────────────────────────────────────────"
    echo "  Tasks:        $completed/$total_tasks completed"
    if [ $failed -gt 0 ]; then
        echo "                $failed failed"
    fi
    if [ $blocked -gt 0 ]; then
        echo "                $blocked blocked"
    fi
    echo "  Total time:   ${total_duration}s (wall clock lower due to parallelism)"
    echo "  Files:        $total_files_created created"
    echo "  Tests:        $total_tests_passing passing"
    echo "  Quality:      $total_critical CRITICAL, $total_high HIGH"
    echo ""

    # Quality gate check
    if [ $total_critical -gt 0 ]; then
        echo "❌ QUALITY GATE FAILED: $total_critical CRITICAL issues across tasks"
        echo "   Review results in Implementation_*/01-tasks/*/results/quality_report.json"
        exit 1
    fi

    if [ $failed -gt 0 ]; then
        echo "⚠️  $failed task(s) failed - review error logs in results folders"
    fi

    echo "═══════════════════════════════════════════════════════════"
    echo ""

    # Update implementation progress
    update_implementation_progress "$completed" "$total_tasks"
}

update_implementation_progress() {
    local completed="$1"
    local total="$2"

    python3 .claude/hooks/update_progress.py \
        --stage implementation \
        --completed "$completed" \
        --total "$total" \
        --system-name "$SYSTEM_NAME" 2>/dev/null || true
}
```

### Results Structure

Each task's results are saved to `Implementation_<System>/01-tasks/<T-ID>/results/`:

```
Implementation_ERTriage/01-tasks/T-007/results/
├── execution.json          # Main execution record with all phase results
├── implementation_plan.md  # Phase 2: Planning output
├── test_spec.md            # Phase 3: Test design output
├── build.log               # Phase 4: Build output
├── test.log                # Phase 4: Test output
├── e2e_test.log            # Phase 5: E2E test output
├── quality_report.json     # Phase 6: Quality findings
├── pr_description.md       # Phase 7: PR description
└── error.log               # Only if task failed
```

### Disabling Isolation (Legacy Mode)

To run in legacy mode (in-process phases, shared context):

```bash
/htec-sdd-implement ERTriage --pr-group PR-003 --isolate-tasks=false
```

**Warning**: Legacy mode may cause context degradation on multi-task runs. Only use for debugging or single-task execution.

---

## Related Commands

- `/htec-sdd-tasks` - Generate task breakdown
- `/htec-sdd-worktree-setup` - Setup worktrees for parallel PRs
- `/htec-sdd-review` - Additional code review (if needed)
- `/htec-sdd-integrate` - Integration test suite (separate)
- `/htec-sdd-status` - Check progress
- `/htec-sdd-changerequest` - Process change requests
