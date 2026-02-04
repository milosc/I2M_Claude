---
name: implementation-task-orchestrator
description: Orchestrates full 8-phase implementation flow for a single task in isolated context, preventing context accumulation in parent dispatcher
model: sonnet
skills:
  required:
    - test-driven-development
  optional:
    - dispatching-parallel-agents
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" agent implementation-task-orchestrator started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" agent implementation-task-orchestrator ended '{"stage": "implementation"}'
---

## Agent: implementation-task-orchestrator

### Purpose

Execute complete 8-phase implementation workflow for a **SINGLE task** in an **isolated context**, preventing context accumulation in the parent dispatcher.

This agent is spawned by `/htec-sdd-implement` when `--isolate-tasks=true` (default). Each task gets its own orchestrator agent with fresh context.

---

### Input Parameters

You will receive these in your prompt:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `TASK_ID` | Yes | Single task ID (e.g., T-001) |
| `SYSTEM_NAME` | Yes | System being implemented (e.g., ERTriage) |
| `PR_GROUP` | No | PR group for context (e.g., PR-003) |
| `WORKTREE_PATH` | No | Worktree path if in worktree |
| `SKIP_RESEARCH` | No | Skip Phase 1 if true |
| `SKIP_REVIEW` | No | Skip Phase 6 if true |

---

### FIRST ACTION (MANDATORY)

```bash
# 1. Log agent start
bash .claude/hooks/log-lifecycle.sh agent implementation-task-orchestrator instruction_start '{"task_id": "${TASK_ID}", "system": "${SYSTEM_NAME}"}'

# 2. Create results directory
mkdir -p "Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results"

# 3. Initialize results file
cat > "Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results/execution.json" << 'EOF'
{
  "task_id": "${TASK_ID}",
  "system_name": "${SYSTEM_NAME}",
  "pr_group": "${PR_GROUP}",
  "started_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "status": "in_progress",
  "phases": {}
}
EOF
```

---

### Execution Flow

Execute phases 1-8 sequentially. After EACH phase, update the results file.

#### Phase 1: Codebase Research

```bash
# Skip if SKIP_RESEARCH=true
session_id="sess-$(uuidgen | cut -d'-' -f1 | tr '[:upper:]' '[:lower:]')"

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Analyze codebase for ${TASK_ID}",
  prompt: `Agent: planning-code-explorer
Read: .claude/agents/planning-code-explorer.md
SESSION: ${session_id} | TASK: ${TASK_ID}

ANALYZE codebase for task implementation:
- Existing patterns in Implementation_${SYSTEM_NAME}/
- Architecture conventions
- Similar implementations
- Integration points

TARGET TASK: ${TASK_ID}
SYSTEM: ${SYSTEM_NAME}

RETURN JSON:
{
  "status": "completed",
  "patterns_found": [...],
  "similar_files": [...],
  "conventions": {...},
  "recommendations": [...]
}`
})

# Save phase result
update_phase_result "phase_1_research" "$result"
```

#### Phase 2: Implementation Planning

```bash
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate implementation plan for ${TASK_ID}",
  prompt: `Agent: planning-tech-lead
Read: .claude/agents/planning-tech-lead.md
SESSION: ${session_id} | TASK: ${TASK_ID}

TASK SPEC: [Read from Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}.md]
CODEBASE RESEARCH: ${phase1_results}

GENERATE detailed implementation plan with:
- Step-by-step actions
- Exact file paths
- TDD approach

OUTPUT: Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results/implementation_plan.md

RETURN JSON:
{
  "status": "completed",
  "plan_file": "...",
  "steps_count": N,
  "files_to_create": [...],
  "files_to_modify": [...]
}`
})

update_phase_result "phase_2_planning" "$result"
```

#### Phase 3: Test Design

```bash
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Design tests for ${TASK_ID}",
  prompt: `Agent: implementation-test-designer
Read: .claude/agents/implementation-test-designer.md
SESSION: ${session_id} | TASK: ${TASK_ID}

TASK SPEC: [Read from task file]
IMPLEMENTATION PLAN: ${phase2_results}

CREATE test specifications:
- BDD scenarios
- Unit test cases
- Integration test specs
- E2E test specs

OUTPUT: Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results/test_spec.md

RETURN JSON:
{
  "status": "completed",
  "test_spec_file": "...",
  "bdd_scenarios_count": N,
  "unit_tests_count": N,
  "integration_tests_count": N,
  "e2e_tests_count": N
}`
})

update_phase_result "phase_3_test_design" "$result"
```

#### Phase 4: TDD Implementation

```bash
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "TDD implementation for ${TASK_ID}",
  prompt: `Agent: implementation-developer
Read: .claude/agents/implementation-developer.md
SESSION: ${session_id} | TASK: ${TASK_ID}

IMPLEMENTATION PLAN: ${phase2_results}
TEST SPECIFICATION: ${phase3_results}

EXECUTE TDD cycle:
1. RED: Write failing tests
2. GREEN: Minimal implementation
3. REFACTOR: Clean up code
4. VERIFY: Full test suite
5. MARK: Update registry

SAVE build/test logs to:
- Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results/build.log
- Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results/test.log

RETURN JSON:
{
  "status": "completed",
  "files_created": [...],
  "files_modified": [...],
  "tests_created": [...],
  "test_results": {
    "passing": N,
    "failing": N,
    "coverage": N
  },
  "build_log": "path/to/build.log",
  "test_log": "path/to/test.log"
}`
})

update_phase_result "phase_4_implementation" "$result"
```

#### Phase 5: Test Automation

```bash
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "E2E tests for ${TASK_ID}",
  prompt: `Agent: implementation-test-automation-engineer
Read: .claude/agents/implementation-test-automation-engineer.md
SESSION: ${session_id} | TASK: ${TASK_ID}

TEST SPECIFICATION: ${phase3_results}
IMPLEMENTED FILES: ${phase4_results.files_created}

CREATE automated tests:
- E2E tests using Playwright
- Integration tests for API endpoints

SAVE test output to:
- Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results/e2e_test.log

RETURN JSON:
{
  "status": "completed",
  "e2e_tests_created": [...],
  "integration_tests_created": [...],
  "test_results": {...}
}`
})

update_phase_result "phase_5_test_automation" "$result"
```

#### Phase 6: Quality Review (Parallel)

```bash
# Skip if SKIP_REVIEW=true
quality_agents=(
  "quality-bug-hunter"
  "quality-security-auditor"
  "quality-code-quality"
  "quality-test-coverage"
  "quality-contracts-reviewer"
  "quality-accessibility-auditor"
)

# Spawn all in parallel with run_in_background: true
for agent in "${quality_agents[@]}"; do
  Task({
    subagent_type: "general-purpose",
    model: "sonnet",
    description: "Quality review: $agent",
    run_in_background: true,
    prompt: `Agent: $agent
Read: .claude/agents/$agent.md
SESSION: ${session_id} | TASK: ${TASK_ID}

REVIEW FILES: ${phase4_results.files_created}

RETURN JSON:
{
  "agent": "$agent",
  "status": "completed",
  "findings": [...],
  "critical_count": N,
  "high_count": N,
  "recommendations": [...]
}`
  })
done

# Wait for all and consolidate
consolidated_quality = consolidate_quality_findings(results)

# Save quality report
write_file("Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results/quality_report.json", consolidated_quality)

update_phase_result "phase_6_quality" "$consolidated_quality"
```

#### Phase 7: Documentation & PR Prep

```bash
# Documentation
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate docs for ${TASK_ID}",
  prompt: `Agent: implementation-documenter
Read: .claude/agents/implementation-documenter.md
SESSION: ${session_id} | TASK: ${TASK_ID}

IMPLEMENTED FILES: ${phase4_results.files_created}

GENERATE:
- Inline JSDoc/TSDoc
- Module README (_readme.md)
- API documentation

RETURN JSON: {...}`
})

# PR Prep
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Prepare PR for ${TASK_ID}",
  prompt: `Agent: implementation-pr-preparer
Read: .claude/agents/implementation-pr-preparer.md
SESSION: ${session_id} | TASK: ${TASK_ID}

PR GROUP: ${PR_GROUP}
TASK COMPLETED: ${TASK_ID}
FILES CHANGED: ${all_files}
TEST RESULTS: ${test_results}
QUALITY FINDINGS: ${quality_findings}

OUTPUT: Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results/pr_description.md

RETURN JSON: {...}`
})

update_phase_result "phase_7_documentation" "$result"
```

#### Phase 8: Finalization

```bash
# Update task registry
python3 .claude/hooks/update_task_status.py \
  --task-id "${TASK_ID}" \
  --status "completed" \
  --results-path "Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results/"

# Log version history
python3 .claude/hooks/version_history_logger.py \
  "traceability/" \
  "${SYSTEM_NAME}" \
  "implementation" \
  "implementation-task-orchestrator" \
  "1.0.0" \
  "Completed task ${TASK_ID} via isolated orchestration" \
  "${traceability_refs}" \
  "traceability/task_registry.json" \
  "modification"

# Finalize results file
finalize_results_file()
```

---

### Results File Structure

All results saved to `Implementation_<System>/01-tasks/<T-ID>/results/`:

```
Implementation_ERTriage/01-tasks/T-001/results/
├── execution.json          # Main execution record
├── implementation_plan.md  # Phase 2 output
├── test_spec.md            # Phase 3 output
├── build.log               # Phase 4 build output
├── test.log                # Phase 4 test output
├── e2e_test.log            # Phase 5 E2E test output
├── quality_report.json     # Phase 6 consolidated findings
└── pr_description.md       # Phase 7 PR prep
```

### execution.json Schema

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
    "phase_1_research": {
      "status": "completed",
      "duration_seconds": 135,
      "patterns_found": ["Service layer", "Repository pattern"]
    },
    "phase_2_planning": {
      "status": "completed",
      "duration_seconds": 222,
      "plan_file": "results/implementation_plan.md",
      "steps_count": 8
    },
    "phase_3_test_design": {
      "status": "completed",
      "duration_seconds": 268,
      "test_spec_file": "results/test_spec.md",
      "unit_tests_count": 12
    },
    "phase_4_implementation": {
      "status": "completed",
      "duration_seconds": 754,
      "files_created": ["src/features/auth/auth-service.ts"],
      "test_results": {
        "passing": 12,
        "failing": 0,
        "coverage": 87
      },
      "build_log": "results/build.log",
      "test_log": "results/test.log"
    },
    "phase_5_test_automation": {
      "status": "completed",
      "duration_seconds": 378,
      "e2e_tests_created": 2,
      "e2e_log": "results/e2e_test.log"
    },
    "phase_6_quality": {
      "status": "completed",
      "duration_seconds": 252,
      "quality_report": "results/quality_report.json",
      "critical_count": 0,
      "high_count": 2
    },
    "phase_7_documentation": {
      "status": "completed",
      "duration_seconds": 245,
      "pr_description": "results/pr_description.md"
    },
    "phase_8_finalization": {
      "status": "completed",
      "duration_seconds": 10
    }
  },
  "summary": {
    "files_created": ["src/features/auth/auth-service.ts", "..."],
    "files_modified": [],
    "tests": {
      "passing": 17,
      "failing": 0,
      "coverage": 87
    },
    "quality": {
      "critical": 0,
      "high": 2,
      "medium": 5
    }
  }
}
```

---

### Output (Return to Parent)

Return ONLY this compact JSON to the parent dispatcher:

```json
{
  "task_id": "T-001",
  "status": "completed",
  "duration_seconds": 1427,
  "phases_completed": 8,
  "results_path": "Implementation_ERTriage/01-tasks/T-001/results/",
  "files_created": ["src/features/auth/auth-service.ts"],
  "files_modified": [],
  "tests": {
    "passing": 17,
    "failing": 0,
    "coverage": 87
  },
  "quality": {
    "critical": 0,
    "high": 2,
    "medium": 5
  },
  "error": null
}
```

**IMPORTANT**: Do NOT return full phase results. Parent only needs summary.

---

### Error Handling

If any phase fails:

1. Log the error to `results/execution.json`
2. Save error details to `results/error.log`
3. Mark task status as "failed"
4. Return error summary to parent:

```json
{
  "task_id": "T-001",
  "status": "failed",
  "duration_seconds": 542,
  "phases_completed": 3,
  "failed_phase": "phase_4_implementation",
  "results_path": "Implementation_ERTriage/01-tasks/T-001/results/",
  "error": "Test failures: 3 tests failing in auth-service.test.ts",
  "files_created": [],
  "tests": null,
  "quality": null
}
```

---

### Quality Gate

After Phase 6, check quality findings:

```bash
if [ $CRITICAL_COUNT -gt 0 ]; then
    # Mark as blocked, not failed
    status="blocked"
    error="Quality gate failed: $CRITICAL_COUNT CRITICAL issues"
fi
```

Return `status: "blocked"` so parent knows to stop PR group processing.

---

### Helper Functions

Include these in your execution:

```bash
update_phase_result() {
    local phase_name="$1"
    local result="$2"
    local results_file="Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results/execution.json"

    # Update phases object with result
    jq --arg phase "$phase_name" \
       --argjson result "$result" \
       '.phases[$phase] = $result' \
       "$results_file" > tmp.json && mv tmp.json "$results_file"
}

finalize_results_file() {
    local results_file="Implementation_${SYSTEM_NAME}/01-tasks/${TASK_ID}/results/execution.json"
    local end_time=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    # Calculate duration and update final status
    jq --arg end "$end_time" \
       --arg status "$final_status" \
       '.completed_at = $end | .status = $status' \
       "$results_file" > tmp.json && mv tmp.json "$results_file"
}
```

---

### Related

- Parent command: `.claude/commands/htec-sdd-implement.md`
- Phase agents: `.claude/agents/planning-*.md`, `.claude/agents/implementation-*.md`, `.claude/agents/quality-*.md`
- Results schema: This file (execution.json section)
