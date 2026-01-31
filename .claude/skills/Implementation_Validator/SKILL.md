---
name: Implementation Validator
description: Use when performing final validation at Checkpoint 9, verifying traceability, coverage, and quality metrics.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_Validator started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_Validator ended '{"stage": "implementation"}'
---

# Implementation Validator

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill Implementation_Validator instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

Performs final validation of the implementation, verifying end-to-end traceability from pain points to code, generating coverage reports, and creating the implementation traceability register.

---

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:Implementation_Validator:started` - When skill begins
- `skill:Implementation_Validator:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Prerequisites

1. **Traceability Guard Check**: This skill invokes `Traceability_Guard` before execution.
   - If guard fails, execution stops with guidance to run `/traceability-init`.
   - Required files: `task_registry.json`, `requirements_registry.json`, `discovery_traceability_register.json`, `productspecs_traceability_register.json`

2. **Checkpoint 8 Passed**: Documentation complete
3. **All Tasks Completed**: No tasks with status != "completed"
4. **Integration Tests Passed**: CP7 integration checkpoint passed

## State Management

### Read State

```
READ _state/implementation_config.json:
    - system_name
    - source_paths
    - quality_targets (coverage, etc.)

READ _state/implementation_progress.json:
    - current_checkpoint (must be >= 8)
    - metrics (all accumulated metrics)

READ traceability/:
    - task_registry.json
    - discovery_traceability_register.json
    - prototype_traceability_register.json
    - productspecs_traceability_register.json
    - solarch_traceability_register.json
```

### Update State

```
ON COMPLETION:
    UPDATE _state/implementation_progress.json:
        current_checkpoint: 9
        cp9_validation_completed: true
        cp9_completed_at: "<ISO timestamp>"
        status: "completed"
        metrics.final_coverage: <percentage>
        metrics.traceability_coverage: <percentage>

    CREATE traceability/implementation_traceability_register.json
```

## Procedure

### Step 0: Guard Check

```
INVOKE Traceability_Guard WITH required_files:
    - "task_registry.json"
    - "requirements_registry.json"
    - "discovery_traceability_register.json"
    - "productspecs_traceability_register.json"

IF NOT guard.valid:
    STOP and show guard.user_action_required
```

### Step 1: Traceability Chain Verification

```
BUILD full_traceability_chain:

# 1. Load all registries
pain_points = READ traceability/pain_point_registry.json
jtbds = READ traceability/jtbd_registry.json
requirements = READ traceability/requirements_registry.json
modules = READ traceability/module_registry.json
tasks = READ traceability/task_registry.json

# 2. Verify Pain Point -> JTBD coverage
FOR EACH pain_point IN pain_points WHERE priority == "P0":
    FIND linked_jtbds WHERE jtbd.pain_point_refs CONTAINS pain_point.id
    IF linked_jtbds.length == 0:
        LOG warning: "P0 pain point {pain_point.id} has no linked JTBDs"
        coverage_issues.append(pain_point.id)

# 3. Verify JTBD -> Requirement coverage
FOR EACH jtbd IN jtbds:
    FIND linked_reqs WHERE req.jtbd_refs CONTAINS jtbd.id
    IF linked_reqs.length == 0:
        LOG warning: "JTBD {jtbd.id} has no linked requirements"

# 4. Verify Requirement -> Task coverage
FOR EACH requirement IN requirements WHERE priority == "P0":
    FIND linked_tasks WHERE task.requirement_refs CONTAINS requirement.id
    IF linked_tasks.length == 0:
        LOG error: "P0 requirement {requirement.id} has no implementation tasks"
        missing_implementations.append(requirement.id)

# 5. Verify Task -> Code coverage
FOR EACH task IN tasks:
    IF task.status != "completed":
        LOG error: "Task {task.id} not completed"
        incomplete_tasks.append(task.id)
    ELSE:
        VERIFY task.implementation.files_created exist
        VERIFY task.implementation.tests_created exist

OUTPUT:
    traceability_coverage: {
        pain_points: { total: N, traced: M, coverage: M/N },
        jtbds: { total: N, traced: M, coverage: M/N },
        requirements: { total: N, traced: M, coverage: M/N },
        tasks: { total: N, completed: M, coverage: M/N }
    }
```

### Step 2: Test Coverage Analysis

```
RUN: vitest run --coverage --coverage.reporter=json

READ coverage/coverage-final.json

CALCULATE coverage_metrics:
    - lines: { total, covered, percentage }
    - branches: { total, covered, percentage }
    - functions: { total, covered, percentage }
    - statements: { total, covered, percentage }

IDENTIFY uncovered_areas:
    FOR EACH file IN coverage_report:
        IF file.line_coverage < quality_targets.coverage:
            uncovered_areas.append({
                file: file.path,
                coverage: file.line_coverage,
                uncovered_lines: file.uncovered_lines
            })

CREATE Implementation_<System>/reports/COVERAGE_REPORT.md:
```

```markdown
# Test Coverage Report

## System: <SystemName>
## Date: <ISO Date>

## Summary

| Metric | Covered | Total | Percentage | Target | Status |
|--------|---------|-------|------------|--------|--------|
| Lines | <n> | <n> | <n>% | 80% | <PASS/FAIL> |
| Branches | <n> | <n> | <n>% | 75% | <PASS/FAIL> |
| Functions | <n> | <n> | <n>% | 80% | <PASS/FAIL> |
| Statements | <n> | <n> | <n>% | 80% | <PASS/FAIL> |

## Coverage by Module

| Module | Lines | Branches | Functions |
|--------|-------|----------|-----------|
<FOR EACH module>
| <module_name> | <n>% | <n>% | <n>% |
</FOR EACH>

## Uncovered Areas

<IF uncovered_areas.length > 0>
### Files Below Target

| File | Coverage | Uncovered Lines |
|------|----------|-----------------|
<FOR EACH uncovered_area>
| <file> | <coverage>% | <lines> |
</FOR EACH>
</IF>

## Test Distribution

| Test Type | Count |
|-----------|-------|
| Unit | <n> |
| Integration | <n> |
| E2E | <n> |
| Total | <n> |
```

### Step 3: Quality Metrics Analysis

```
ANALYZE codebase:

# Code metrics
total_lines = COUNT lines IN src/**/*.{ts,tsx}
test_lines = COUNT lines IN tests/**/*.{ts,tsx}
test_to_code_ratio = test_lines / total_lines

# Complexity metrics (if tool available)
cyclomatic_complexity = ANALYZE with eslint/complexity
maintainability_index = CALCULATE from complexity metrics

# Duplication analysis
duplication_percentage = ANALYZE with jscpd or similar

CREATE Implementation_<System>/reports/QUALITY_METRICS.md:
```

```markdown
# Quality Metrics Report

## System: <SystemName>
## Date: <ISO Date>

## Code Size

| Metric | Value |
|--------|-------|
| Source Files | <n> |
| Test Files | <n> |
| Total Lines (Source) | <n> |
| Total Lines (Tests) | <n> |
| Test-to-Code Ratio | <n>:1 |

## Complexity

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Avg Cyclomatic Complexity | <n> | < 10 | <PASS/FAIL> |
| Max Cyclomatic Complexity | <n> | < 20 | <PASS/FAIL> |
| Duplication | <n>% | < 5% | <PASS/FAIL> |

## Files by Complexity

<top 10 most complex files>

## Type Safety

| Metric | Value |
|--------|-------|
| TypeScript Strict Mode | Yes/No |
| Any Types Used | <n> |
| Type Coverage | <n>% |

## Dependencies

| Category | Count |
|----------|-------|
| Production | <n> |
| Development | <n> |
| Outdated | <n> |
| Vulnerable | <n> |
```

### Step 4: ADR Compliance Check

```
READ SolArch_<System>/09-decisions/ADR-*.md

FOR EACH adr IN adrs:
    VERIFY implementation follows decision:

    ADR-002 (Tech Stack):
        CHECK: React version matches
        CHECK: TypeScript config matches
        CHECK: Testing framework matches

    ADR-003 (State Management):
        CHECK: Zustand used for global state
        CHECK: No Redux or other state libs

    ADR-007 (Error Handling):
        CHECK: Result pattern used
        CHECK: No unhandled throws in business logic

    LOG: adr.id -> compliance_status

OUTPUT:
    adr_compliance: [
        { adr: "ADR-002", status: "compliant", notes: "" },
        { adr: "ADR-007", status: "partial", notes: "2 files with throws" }
    ]
```

### Step 5: Create Implementation Traceability Register

```
CREATE traceability/implementation_traceability_register.json:
```

```json
{
  "metadata": {
    "version": "1.0.0",
    "system_name": "<SystemName>",
    "created_at": "<ISO timestamp>",
    "created_by": "Implementation_Validator",
    "source_stages": [
      "Discovery",
      "Prototype",
      "ProductSpecs",
      "SolArch"
    ]
  },
  "summary": {
    "total_tasks": 47,
    "completed_tasks": 47,
    "total_tests": 312,
    "test_coverage": "87%",
    "traceability_coverage": "100%",
    "validation_status": "PASSED"
  },
  "traceability_chains": [
    {
      "pain_point": "PP-1.1",
      "jtbd": "JTBD-1.1",
      "requirements": ["REQ-001", "REQ-002"],
      "modules": ["MOD-MOB-INV-01"],
      "tasks": ["T-001", "T-002", "T-003"],
      "tests": ["tests/unit/inventory/*.test.ts"],
      "code": ["src/features/inventory/**"]
    }
  ],
  "tasks": [
    {
      "id": "T-001",
      "status": "completed",
      "requirement_refs": ["REQ-001"],
      "module_ref": "MOD-MOB-INV-01",
      "implementation": {
        "files_created": ["src/features/inventory/hooks/use-inventory.ts"],
        "tests_created": ["tests/unit/inventory/use-inventory.test.ts"],
        "coverage": "92%"
      }
    }
  ],
  "coverage": {
    "lines": { "covered": 4521, "total": 5197, "percentage": "87%" },
    "branches": { "covered": 1205, "total": 1507, "percentage": "80%" },
    "functions": { "covered": 892, "total": 1023, "percentage": "87%" }
  },
  "quality_metrics": {
    "test_to_code_ratio": "1.4:1",
    "avg_complexity": 6.2,
    "duplication": "2.1%",
    "adr_compliance": "100%"
  },
  "validation_results": {
    "cp9_passed": true,
    "blocking_issues": [],
    "warnings": [],
    "recommendations": []
  }
}
```

### Step 6: Generate Validation Report

```
CREATE Implementation_<System>/reports/VALIDATION_REPORT.md:
```

```markdown
# Implementation Validation Report

## System: <SystemName>
## Checkpoint: 9 (Final Validation)
## Date: <ISO Date>
## Status: <PASSED/FAILED>

## Executive Summary

Implementation stage completed <successfully/with issues>. <summary statement>

## Checkpoint Summary

| CP | Phase | Status | Date |
|----|-------|--------|------|
| 0 | Initialize | <status> | <date> |
| 1 | Validate | <status> | <date> |
| 2 | Tasks | <status> | <date> |
| 3 | Infrastructure | <status> | <date> |
| 4 | Features 50% | <status> | <date> |
| 5 | P0 Complete | <status> | <date> |
| 6 | Code Review | <status> | <date> |
| 7 | Integration | <status> | <date> |
| 8 | Documentation | <status> | <date> |
| 9 | Validation | <status> | <date> |

## Traceability Verification

| Source | Target | Coverage | Status |
|--------|--------|----------|--------|
| Pain Points -> JTBDs | <n>% | <PASS/FAIL> |
| JTBDs -> Requirements | <n>% | <PASS/FAIL> |
| Requirements -> Tasks | <n>% | <PASS/FAIL> |
| Tasks -> Code | <n>% | <PASS/FAIL> |
| Code -> Tests | <n>% | <PASS/FAIL> |

## Test Coverage

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Line Coverage | <n>% | 80% | <PASS/FAIL> |
| Branch Coverage | <n>% | 75% | <PASS/FAIL> |
| Function Coverage | <n>% | 80% | <PASS/FAIL> |

## Quality Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Test-to-Code Ratio | <n>:1 | > 1:1 | <PASS/FAIL> |
| Avg Complexity | <n> | < 10 | <PASS/FAIL> |
| Duplication | <n>% | < 5% | <PASS/FAIL> |
| ADR Compliance | <n>% | 100% | <PASS/FAIL> |

## ADR Compliance

| ADR | Decision | Status |
|-----|----------|--------|
<FOR EACH adr>
| <adr.id> | <adr.title> | <compliant/partial/non-compliant> |
</FOR EACH>

## Blocking Issues

<IF blocking_issues.length > 0>
<FOR EACH issue>
- **<issue.id>**: <issue.description>
</FOR EACH>
</IF>
<ELSE>
No blocking issues found.
</ELSE>

## Warnings

<warnings list>

## Recommendations

<recommendations list>

## Files Generated

- traceability/implementation_traceability_register.json
- reports/COVERAGE_REPORT.md
- reports/QUALITY_METRICS.md
- reports/VALIDATION_REPORT.md
```

### Step 7: Update Final State

```
UPDATE _state/implementation_progress.json:
    current_checkpoint: 9
    cp9_validation_completed: true
    cp9_completed_at: "<ISO timestamp>"
    status: "completed"
    metrics.final_coverage: <percentage>
    metrics.traceability_coverage: <percentage>
    metrics.quality_score: <calculated score>
    metrics.total_duration_hours: <elapsed>
```

## Blocking Criteria

Final validation **BLOCKS** if:

1. **P0 Traceability Gap**: Any P0 pain point without traced implementation
2. **Coverage Below Threshold**: Line coverage < 80% (configurable)
3. **Critical Quality Issue**: Complexity > 20 or duplication > 10%
4. **Incomplete Tasks**: Any P0 task not completed
5. **ADR Violation**: Critical ADR not followed

## Output Files

```
Implementation_<System>/
└── reports/
    ├── COVERAGE_REPORT.md
    ├── QUALITY_METRICS.md
    └── VALIDATION_REPORT.md

traceability/
└── implementation_traceability_register.json
```

## Traceability Chain (Complete)

```
Client Materials (CM-XXX)
    ↓
Pain Points (PP-X.X) ← Verified
    ↓
Jobs-to-be-Done (JTBD-X.X) ← Verified
    ↓
Requirements (REQ-XXX) ← Verified
    ↓
Module Specs (MOD-XXX) ← Verified
    ↓
ADRs (ADR-XXX) ← Compliance Checked
    ↓
Tasks (T-NNN) ← All Completed
    ↓
Code (src/**) ← Coverage Checked
    ↓
Tests (tests/**) ← All Passing
    ↓
Implementation Register ← CREATED BY THIS SKILL
```

## Error Handling

| Situation | Action |
|-----------|--------|
| Missing registry file | Use guard to fail early |
| Coverage tool fails | Log warning, use available metrics |
| Traceability gap | Log as blocking issue |
| ADR compliance partial | Log as warning unless critical |

## Related Skills

- `Implementation_Integrator` - Runs before this (CP7)
- `Implementation_Documenter` - Runs before this (CP8)
- `Traceability_Guard` - Prerequisite check
- `SolutionArchitecture_E2ETraceabilityAnalyzer` - Upstream traceability
