---
name: Implementation Task Decomposer
description: Use when you need to decompose module specifications into executable implementation tasks with TDD specifications and parallel execution markers.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_TaskDecomposer started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_TaskDecomposer ended '{"stage": "implementation"}'
---

# Implementation Task Decomposer

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill Implementation_TaskDecomposer instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

> **Version**: 2.0.0 | **Updated**: 2025-12-26
> **Change**: Added Applicability Check for non-UI projects - skips Component/Screen tasks for BACKEND_ONLY, DATABASE_ONLY, INTEGRATION project types

Transforms module specifications from ProductSpecs into granular, TDD-ready implementation tasks with dependency graphs and parallel execution markers.

---

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:Implementation_TaskDecomposer:started` - When skill begins
- `skill:Implementation_TaskDecomposer:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Prerequisites

1. **Traceability Guard Check**: This skill invokes `Traceability_Guard` before execution.
   - If guard fails, execution stops with guidance to run `/traceability-init`.
   - Required files: `requirements_registry.json`, `module_registry.json`

2. **ProductSpecs Completed**: Module specifications exist in `ProductSpecs_<SystemName>/01-modules/`
3. **SolArch Completed**: Architecture decisions available for pattern reference
4. **Implementation Initialized**: `_state/implementation_config.json` exists

## Applicability Check (Smart Obsolescence Handling)

Before decomposing tasks, check the project classification:

```
READ _state/implementation_config.json
EXTRACT project_classification (FULL_STACK | BACKEND_ONLY | DATABASE_ONLY | INTEGRATION | INFRASTRUCTURE)

IF project_classification NOT IN [FULL_STACK]:
  # Non-UI project - skip UI-specific task categories
  SKIP Phase 4b (Component Tasks)
  SKIP Phase 4c (Screen Tasks)
  FOCUS on Infrastructure, Service Layer, and Integration tasks
```

### Task Category Applicability Matrix

| Task Category | FULL_STACK | BACKEND_ONLY | DATABASE_ONLY | INTEGRATION | INFRASTRUCTURE |
|---------------|------------|--------------|---------------|-------------|----------------|
| Phase 3: Infrastructure | ✅ | ✅ | ✅ | ✅ | ✅ |
| Phase 4a: Service Layer | ✅ | ✅ | ❌ N/A | ✅ | ❌ N/A |
| **Phase 4b: Components** | **✅** | **❌ N/A** | **❌ N/A** | **❌ N/A** | **❌ N/A** |
| **Phase 4c: Screens** | **✅** | **❌ N/A** | **❌ N/A** | **❌ N/A** | **❌ N/A** |
| Phase 5: Integration | ✅ | ✅ | ✅ | ✅ | ✅ |

### Decomposition Pattern for Non-UI Projects

For BACKEND_ONLY or INTEGRATION projects:

```
MODULE DECOMPOSITION PATTERN (API-Only)
═══════════════════════════════════════

1. INFRASTRUCTURE TASKS (Phase 3)
   └── T-NNN: Setup feature folder structure
   └── T-NNN: Create TypeScript interfaces/types
   └── T-NNN: Configure feature-specific dependencies

2. SERVICE LAYER TASKS (Phase 4a)
   └── T-NNN: API client/handler functions
   └── T-NNN: Business logic services
   └── T-NNN: State management / data access layer

3. [SKIPPED - N/A] COMPONENT TASKS (Phase 4b)
   └── No UI components for this project type

4. [SKIPPED - N/A] SCREEN TASKS (Phase 4c)
   └── No UI screens for this project type

5. INTEGRATION TASKS (Phase 5)
   └── T-NNN: API endpoint integration tests
   └── T-NNN: Cross-module service integration
   └── T-NNN: E2E API test scenarios
```

### Task Registry Entry for Skipped Categories

When a task category is N/A, add a single summary entry:

```json
{
  "id": "T-SKIP-COMPONENTS",
  "title": "[N/A] Component Tasks - Not Applicable",
  "status": "NOT_APPLICABLE",
  "phase": 4,
  "priority": "N/A",
  "applicability": {
    "applicable": false,
    "project_classification": "{PROJECT_CLASSIFICATION}",
    "reason": "No UI layer - component tasks not applicable"
  },
  "traceability": {
    "module_refs": [],
    "requirement_refs": [],
    "jira_ref": null
  }
}
```

### Minimum Task Count Adjustment

For checkpoint validation:
- **FULL_STACK**: All task categories required
- **BACKEND_ONLY**: Phase 4b/4c tasks marked N/A (counts as valid)
- **DATABASE_ONLY**: Phase 4a/4b/4c tasks marked N/A
- **INTEGRATION**: Phase 4b/4c tasks marked N/A
- **INFRASTRUCTURE**: Only Phase 3/5 tasks required

## Input Requirements

| Input | Location | Purpose |
|-------|----------|---------|
| Module specs | `ProductSpecs_<System>/01-modules/MOD-*.md` | Task source |
| Requirements registry | `traceability/requirements_registry.json` | Traceability |
| JIRA export | `ProductSpecs_<System>/04-jira/jira-import.json` | JIRA linking |
| ADRs | `SolArch_<System>/09-decisions/ADR-*.md` | Pattern reference |

## Output

| Output | Location | Format |
|--------|----------|--------|
| Task registry | `traceability/task_registry.json` | JSON |
| Task index | `Implementation_<System>/tasks/TASK_INDEX.md` | Markdown |
| Individual tasks | `Implementation_<System>/tasks/T-NNN.md` | Markdown |

## Procedure

### Step 1: Load Module Specifications

```
FOR EACH module_file IN ProductSpecs_<System>/01-modules/MOD-*.md:
    PARSE module specification:
        module_id: MOD-APP-FEAT-NN
        title: string
        user_stories: [{id, description, acceptance_criteria}]
        screen_refs: [SCR-NNN]
        api_dependencies: [endpoint paths]
        priority: P0 | P1 | P2
        complexity: low | medium | high
```

### Step 2: Decomposition Strategy

For each module, generate tasks following this hierarchy:

```
MODULE DECOMPOSITION PATTERN
═══════════════════════════════════════

1. INFRASTRUCTURE TASKS (Phase 3)
   └── T-NNN: Setup feature folder structure
   └── T-NNN: Create TypeScript interfaces/types
   └── T-NNN: Configure feature-specific dependencies

2. SERVICE LAYER TASKS (Phase 4a)
   └── T-NNN: API client functions
   └── T-NNN: Business logic services
   └── T-NNN: State management (hooks/stores)

3. COMPONENT TASKS (Phase 4b)
   └── T-NNN: Primitive components (inputs, buttons)
   └── T-NNN: Composite components (forms, cards)
   └── T-NNN: Container components

4. SCREEN TASKS (Phase 4c)
   └── T-NNN: Page components
   └── T-NNN: Layout integration
   └── T-NNN: Navigation wiring

5. INTEGRATION TASKS (Phase 5)
   └── T-NNN: Cross-module integration
   └── T-NNN: E2E test scenarios
```

### Step 3: Generate Task Specifications

For each task:

```json
{
  "id": "T-NNN",
  "title": "Descriptive task title",
  "description": "Detailed description of what needs to be implemented",
  "phase": 3 | 4 | 5,
  "priority": "P0" | "P1" | "P2",
  "status": "pending",
  "estimated_complexity": "low" | "medium" | "high",

  "traceability": {
    "module_ref": "MOD-APP-FEAT-NN",
    "user_story": "US-NNN",
    "jira_ref": "INV-NNN",
    "screen_refs": ["SCR-NNN"],
    "requirement_refs": ["REQ-NNN"],
    "pain_point_refs": ["PP-X.X"]
  },

  "dependencies": ["T-001", "T-002"],
  "parallel": true | false,

  "acceptance_criteria": [
    {
      "id": "AC-1",
      "description": "Specific verifiable criterion",
      "status": "pending",
      "test_location": null
    }
  ],

  "tdd_spec": {
    "test_file": "tests/unit/<feature>/<component>.test.ts",
    "test_cases": [
      {
        "name": "should <expected behavior>",
        "type": "unit" | "integration",
        "acceptance_criteria": "AC-1",
        "setup": ["mock dependencies", "test data"]
      }
    ],
    "coverage_target": 80
  },

  "implementation_notes": [
    "Follow pattern from ADR-007 for error handling",
    "Reference existing component in src/components/Button"
  ]
}
```

### Step 4: Determine Parallel Execution

```
BUILD dependency_graph from task dependencies

FOR EACH task:
    IF task.dependencies.length == 0:
        task.parallel = true
        MARK with [P]
    ELIF ALL dependencies IN completed_tasks:
        task.parallel = true
        MARK with [P]
    ELSE:
        task.parallel = false
        task.blocked_by = pending_dependencies
```

### Step 5: Calculate Execution Order

```
execution_order = topological_sort(tasks, dependency_graph)

GROUP tasks by phase:
    phase_3_tasks = filter(tasks, phase == 3)
    phase_4_tasks = filter(tasks, phase == 4)
    phase_5_tasks = filter(tasks, phase == 5)

WITHIN each phase:
    SORT by priority (P0 first)
    SORT by dependencies (independent first)
```

### Step 6: Generate TDD Specifications

For each acceptance criterion:

```
ANALYZE criterion description
DETERMINE test type:
    - Unit test: isolated component/function behavior
    - Integration test: cross-component interaction
    - E2E test: user flow validation

GENERATE test case specification:
    - Test name following "should <behavior>" pattern
    - Required mocks and test data
    - Expected assertions
    - Edge cases to cover
```

### Step 7: Link to JIRA

```
IF jira-import.json exists:
    READ JIRA items
    FOR EACH task:
        FIND matching JIRA item by:
            - Module reference
            - User story match
            - Description similarity
        SET task.jira_ref = matched_jira_id
```

### Step 8: Generate Output Files

#### Task Registry (JSON)

```json
{
  "schema_version": "1.0.0",
  "system_name": "<SystemName>",
  "generated_at": "<ISO timestamp>",
  "tasks": {
    "T-001": { /* task object */ },
    "T-002": { /* task object */ }
  },
  "dependency_graph": {
    "T-001": [],
    "T-002": ["T-001"],
    "T-003": ["T-001", "T-002"]
  },
  "execution_order": ["T-001", "T-002", "T-003"],
  "statistics": {
    "total": 47,
    "by_status": {"pending": 47, "completed": 0},
    "by_priority": {"P0": 23, "P1": 16, "P2": 8},
    "by_phase": {"3": 8, "4": 31, "5": 8},
    "parallel_tasks": 26
  }
}
```

#### Task Index (Markdown)

```markdown
# Implementation Tasks

## System: <SystemName>
## Generated: <Date>
## Total Tasks: 47

## Summary

| Phase | Tasks | Parallel | Dependencies |
|-------|-------|----------|--------------|
| 3 (Infrastructure) | 8 | 6 [P] | 2 |
| 4 (Features) | 31 | 18 [P] | 13 |
| 5 (Integration) | 8 | 2 [P] | 6 |

## Execution Order

### Phase 3: Infrastructure

| ID | Title | [P] | Depends | Priority |
|----|-------|-----|---------|----------|
| T-001 | Setup project structure | [P] | - | P0 |
...

### Phase 4: Features
...

### Phase 5: Integration
...
```

#### Individual Task Files

See `/htec-sdd-tasks` command for task file template.

## Quality Checks

Before completing:

1. **Coverage**: Every module has at least one task
2. **Traceability**: Every task links to module, user story, and requirements
3. **TDD Ready**: Every task has test specifications
4. **Dependencies Valid**: No circular dependencies
5. **Priority Balance**: P0 tasks form executable critical path

## Error Handling

| Error | Action |
|-------|--------|
| Module file unparseable | Log to FAILURES_LOG.md, skip module |
| Missing requirements registry | Warn, continue without traceability |
| Circular dependency detected | Error, require manual resolution |
| JIRA link not found | Warn, leave jira_ref null |

## Related Skills

- `Implementation_Developer` - Executes decomposed tasks
- `Implementation_CodeReview` - Reviews implemented tasks
