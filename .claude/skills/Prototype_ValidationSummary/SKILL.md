---
name: summarizing-prototype-validation
description: Use when you need to generate a comprehensive validation summary report after prototype build completion, aggregating results from all phases.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill summarizing-prototype-validation started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill summarizing-prototype-validation ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill summarizing-prototype-validation instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

# Prototype Validation Summary

> **Phase 4 Enhancement**: Auto-generated validation summary after prototype build completion

## Metadata
- **Skill ID**: Prototype_ValidationSummary
- **Version**: 1.0.0
- **Created**: 2026-01-03
- **Author**: Phase 4 Quality of Life Improvements
- **Depends On**: Prototype_QA (CP13), Prototype_UIAudit (CP14)

## Description

Auto-invoked after CP14 (UI Audit) to generate a comprehensive validation summary showing the complete health of the prototype build. Aggregates validation results from all phases, Assembly-First compliance checks, test coverage metrics, and build artifacts.

**Key Features:**
- ✅ Phase-by-phase validation status with duration tracking
- ✅ Assembly-First compliance summary
- ✅ Test coverage metrics
- ✅ Build artifact metrics (screens, components, LOC, bundle size)
- ✅ Actionable recommendations
- ✅ Machine-readable JSON output

## Execution Logging (MANDATORY)

This skill logs all execution to the global pipeline progress registry. Logging is automatic and requires no manual configuration.

### How Logging Works

Every execution of this skill is logged to `_state/lifecycle.json`:

- **start_event**: Logged when skill execution begins
- **end_event**: Logged when skill execution completes

Events include:
- skill_name, intent, stage, system_name
- start/end timestamps
- status (completed/failed)
- output files created (validation summary reports)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "summarizing-prototype-validation"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "summarizing-prototype-validation" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## Trigger Conditions

This skill is **automatically invoked** when:
1. Prototype_UIAudit completes successfully (CP14 status = "complete")
2. `_state/progress.json` shows `phases.ui_audit.status = "complete"`
3. No manual invocation required (orchestrator auto-triggers)

---

## Output Structure

```
Prototype_<SystemName>/
├── 05-validation/
│   └── VALIDATION_SUMMARY.md       # Human-readable summary
└── _state/
    └── validation_summary.json     # Machine-readable data
```

---

## Procedure

### Step 1: Load Validation Data from All Phases

```
READ _state/progress.json → all phase data
READ 05-validation/VALIDATION_REPORT.md → QA results
READ 05-validation/TRACEABILITY_MATRIX.md → traceability data
READ 05-validation/REQUIREMENTS_COVERAGE.md → coverage data
READ 05-validation/accessibility/a11y-audit-results.md → A11Y results
READ reports/ui-audit/AUDIT_SUMMARY.md → UI audit results (if exists)

EXTRACT phase data:
  FOR each phase in [components, screens, interactions, build, codegen, qa, ui_audit]:
    RECORD:
      - status
      - completed_at
      - validation status
      - metrics
      - outputs

CALCULATE phase durations:
  FOR each phase:
    IF phase has completed_at AND previous phase has completed_at:
      duration = completed_at - previous_phase_completed_at
```

### Step 2: Run Assembly-First Compliance Check

```
INVOKE assembly_first_validator:
  python3 .claude/hooks/assembly_first_validator.py \
    --validate-prototype Prototype_{SystemName} \
    --json-output _state/assembly_validation.json

READ _state/assembly_validation.json → validation results

EXTRACT compliance metrics:
  - total_files_checked
  - files_with_violations
  - critical_violations_count
  - high_violations_count
  - medium_violations_count
  - low_violations_count
  - most_common_violations (top 3)

CATEGORIZE compliance status:
  IF critical_violations_count == 0:
    compliance_status = "PASS"
  ELSE:
    compliance_status = "FAIL"

GENERATE compliance summary:
  - ✅ No raw HTML elements (if critical_violations_count == 0)
  - ✅ Component imports valid (check import violations)
  - ⚠️ {count} warnings (if warnings > 0)
```

### Step 3: Aggregate Test Coverage Metrics

```
IF prototype/package.json exists:
  RUN test coverage:
    cd prototype
    npm run test -- --coverage --silent > /tmp/coverage_output.txt 2>&1

  PARSE coverage output:
    EXTRACT coverage percentages:
      - statements
      - branches
      - functions
      - lines

  COMPARE to targets:
    target_coverage = 80%
    IF coverage >= target_coverage:
      coverage_status = "PASS"
    ELSE:
      coverage_status = "BELOW_TARGET"

ELSE:
  coverage_status = "N/A"
  WARN: "No test framework detected"

COUNT test files:
  unit_tests = count files in prototype/tests/unit/
  integration_tests = count files in prototype/tests/integration/
  e2e_tests = count files in prototype/tests/e2e/
  total_test_files = unit_tests + integration_tests + e2e_tests
```

### Step 4: Calculate Build Artifact Metrics

```
COUNT screens:
  screen_specs = count files in 02-screens/*/*.md
  screen_code = count files in prototype/src/screens/*.tsx

COUNT components:
  component_specs = count files in 01-components/**/*.md
  component_code = count files in prototype/src/components/*.tsx

CALCULATE lines of code:
  cd prototype/src
  total_lines = wc -l **/*.tsx **/*.ts | tail -1

ESTIMATE bundle size:
  IF prototype/dist/ exists:
    bundle_size = du -sh prototype/dist/
  ELSE IF prototype/.next/ exists:
    bundle_size = du -sh prototype/.next/
  ELSE:
    bundle_size = "Not built yet"

RECORD artifacts:
  - screen_count: screen_code
  - component_count: component_code
  - total_loc: total_lines
  - bundle_size: bundle_size
```

### Step 5: Generate Phase-by-Phase Validation Table

```
CREATE phase_validation_table:

| Phase | Status | Duration | Issues |
|-------|--------|----------|--------|
| CP8: Components | {status} | {duration} | {issues_count} |
| CP9: Screens | {status} | {duration} | {issues_count} |
| CP10: Interactions | {status} | {duration} | {issues_count} |
| CP11-12: Build | {status} | {duration} | {issues_count} |
| CP13: QA | {status} | {duration} | {issues_count} |
| CP14: UI Audit | {status} | {duration} | {issues_count} |

FOR each phase:
  status_icon = ✅ if status == "complete" and validation passed
              = ⚠️ if status == "complete" but warnings exist
              = ❌ if status == "failed"

  duration_format = "{minutes}m {seconds}s"

  issues_count = count of CRITICAL + HIGH + MEDIUM issues in phase
```

### Step 6: Generate Recommendations

```
ANALYZE validation results and generate recommendations:

IF assembly_validation has warnings > 0:
  ADD recommendation:
    "Address {count} Assembly-First warnings in {files_with_warnings}"

IF test_coverage < 80%:
  ADD recommendation:
    "Increase test coverage from {current}% to 80% (add {needed} tests)"

IF critical_violations_count > 0:
  ADD recommendation:
    "CRITICAL: Fix {count} Assembly-First violations before delivery"

IF bundle_size > 500KB:
  ADD recommendation:
    "Consider code splitting - bundle size is {size}KB (target: <500KB)"

IF any phase has status != "complete":
  ADD recommendation:
    "Complete pending phase: {phase_name}"

PRIORITIZE recommendations:
  1. CRITICAL issues (blocking delivery)
  2. HIGH issues (affects quality)
  3. MEDIUM issues (nice to have)
```

### Step 7: Generate Human-Readable Summary

```
CREATE 05-validation/VALIDATION_SUMMARY.md:
  # Prototype Validation Summary

  **Generated**: {timestamp}
  **Build Duration**: {total_duration}
  **Status**: {overall_status}

  ---

  ## Executive Summary

  | Metric | Value | Status |
  |--------|-------|--------|
  | Overall Status | {PASS/FAIL} | {icon} |
  | Build Success | {yes/no} | {icon} |
  | Test Coverage | {coverage}% | {icon} |
  | Assembly-First Compliance | {PASS/FAIL} | {icon} |
  | P0 Coverage | {100%} | {icon} |

  ---

  ## Phase-by-Phase Validation

  {phase_validation_table from Step 5}

  **Total Build Time**: {total_duration}

  ---

  ## Assembly-First Compliance

  | Check | Status | Details |
  |-------|--------|---------|
  | No raw HTML elements | {✅/❌} | {details} |
  | Component imports valid | {✅/❌} | {details} |
  | Theme tokens used | {✅/⚠️} | {warnings_count} warnings |
  | No manual ARIA | {✅/⚠️} | {warnings_count} warnings |

  **Files Checked**: {total_files}
  **Files with Violations**: {files_with_violations}
  **Critical Violations**: {critical_count}
  **Warnings**: {warnings_count}

  {IF warnings > 0:}
  ### Non-Blocking Warnings

  Most common warnings:
  1. {warning_type_1}: {count} occurrences
  2. {warning_type_2}: {count} occurrences
  3. {warning_type_3}: {count} occurrences
  {END IF}

  ---

  ## Test Coverage

  | Type | Coverage | Target | Status |
  |------|----------|--------|--------|
  | Unit Tests | {coverage}% | 80% | {icon} |
  | Integration Tests | {scenarios} scenarios | - | {icon} |
  | Accessibility | WCAG 2.1 AA | AA | {icon} |

  **Total Test Files**: {total_test_files}
  - Unit: {unit_tests}
  - Integration: {integration_tests}
  - E2E: {e2e_tests}

  ---

  ## Build Artifacts

  | Artifact | Count | Details |
  |----------|-------|---------|
  | Screens | {screen_count} | {list of apps/portals} |
  | Components | {component_count} | {primitives, patterns, etc.} |
  | Lines of Code | {total_loc} | TypeScript + React |
  | Bundle Size | {bundle_size} | {gzipped size if available} |

  ### Screens by App

  {FOR each app in screens:}
  - **{app_name}**: {screen_count} screens
    - {screen_1}, {screen_2}, ...
  {END FOR}

  ### Components by Category

  - **Primitives**: {count}
  - **Data Display**: {count}
  - **Feedback**: {count}
  - **Navigation**: {count}
  - **Overlays**: {count}
  - **Patterns**: {count}

  ---

  ## Recommendations

  {IF no recommendations:}
  ✅ No recommendations - prototype is ready for delivery!
  {ELSE:}

  ### Critical (Must Fix Before Delivery)
  {FOR each critical recommendation:}
  - {recommendation}
  {END FOR}

  ### High Priority (Affects Quality)
  {FOR each high recommendation:}
  - {recommendation}
  {END FOR}

  ### Medium Priority (Nice to Have)
  {FOR each medium recommendation:}
  - {recommendation}
  {END FOR}
  {END IF}

  ---

  ## Next Steps

  {IF overall_status == "PASS":}
  ✅ **Prototype is approved for delivery**

  1. Review validation summary with stakeholders
  2. Address any non-blocking warnings (optional)
  3. Proceed to ProductSpecs generation or delivery
  {ELSE:}
  ⚠️ **Action Required Before Delivery**

  1. Fix critical issues listed in Recommendations
  2. Re-run validation: `python3 .claude/hooks/assembly_first_validator.py --validate-prototype Prototype_{SystemName}`
  3. Re-run QA: `/prototype-qa {SystemName}`
  {END IF}

  ---

  **Report Generated**: {timestamp}
  **Phase 4 Enhancement**: Automated validation summary
```

### Step 8: Generate Machine-Readable JSON

```
CREATE _state/validation_summary.json:
  {
    "generated_at": "{timestamp}",
    "prototype_version": "1.0.0",
    "system_name": "{SystemName}",
    "overall_status": "{PASS|FAIL}",
    "build_duration": {
      "total_seconds": total_seconds,
      "total_formatted": "{hours}h {minutes}m {seconds}s"
    },
    "executive_summary": {
      "overall_status": "{PASS|FAIL}",
      "build_success": true|false,
      "test_coverage_percent": coverage_percent,
      "assembly_first_compliance": "{PASS|FAIL}",
      "p0_coverage": "100%"
    },
    "phases": [
      {
        "checkpoint": "CP8",
        "name": "Components",
        "status": "complete",
        "duration_seconds": duration,
        "issues_count": count,
        "validation_passed": true|false
      },
      // ... more phases
    ],
    "assembly_first": {
      "compliance_status": "{PASS|FAIL}",
      "files_checked": count,
      "files_with_violations": count,
      "critical_violations": count,
      "high_violations": count,
      "medium_violations": count,
      "low_violations": count,
      "checks": {
        "no_raw_html": true|false,
        "valid_imports": true|false,
        "theme_tokens": true|false,
        "no_manual_aria": true|false
      },
      "top_warnings": [
        {"type": "...", "count": N},
        {"type": "...", "count": N},
        {"type": "...", "count": N}
      ]
    },
    "test_coverage": {
      "status": "{PASS|BELOW_TARGET|N/A}",
      "unit_coverage_percent": percent,
      "target_coverage_percent": 80,
      "test_files": {
        "unit": count,
        "integration": count,
        "e2e": count,
        "total": count
      }
    },
    "build_artifacts": {
      "screens": {
        "count": count,
        "by_app": {
          "app_name": screen_count
        }
      },
      "components": {
        "count": count,
        "by_category": {
          "primitives": count,
          "data_display": count,
          "feedback": count,
          "navigation": count,
          "overlays": count,
          "patterns": count
        }
      },
      "code": {
        "total_lines": count,
        "typescript_files": count,
        "react_files": count
      },
      "bundle": {
        "size": "{size}",
        "gzipped_size": "{size}",
        "status": "{OK|LARGE}"
      }
    },
    "recommendations": [
      {
        "priority": "CRITICAL|HIGH|MEDIUM",
        "message": "...",
        "action": "..."
      }
    ],
    "next_steps": {
      "approved_for_delivery": true|false,
      "actions": [
        "..."
      ]
    }
  }
```

### Step 9: Update Progress and Log

```
UPDATE _state/progress.json:
  phases.validation_summary.status = "complete"
  phases.validation_summary.completed_at = timestamp
  phases.validation_summary.outputs = [
    "05-validation/VALIDATION_SUMMARY.md",
    "_state/validation_summary.json"
  ]

LOG completion:
  ✅ Validation Summary Generated
  📄 Report: 05-validation/VALIDATION_SUMMARY.md
  📊 Data: _state/validation_summary.json
  🎯 Status: {overall_status}
```

---

## Integration with Prototype_QA

The Prototype_QA skill (CP13) should auto-invoke this skill after completing validation.

**Update to Prototype_QA/SKILL.md Step 9.5 (Verification Gate)**:

```markdown
### Step 9.5: Verification Gate (MANDATORY)

EXECUTE verification_gate:
  // ... existing validation checks ...

  // ONLY THEN proceed
  LOG: "✅ VERIFICATION PASSED: P0=100%, all outputs exist"

  // AUTO-INVOKE Validation Summary (Phase 4 Enhancement)
  IF phases.ui_audit.status == "complete":
    LOG: "Auto-invoking Validation Summary generation..."
    INVOKE Prototype_ValidationSummary skill
    WAIT for completion
    LOG: "✅ Validation Summary generated"

  PROCEED to "Update Progress"
```

---

## Usage

### Automatic Invocation (Default)

No manual invocation needed. The skill runs automatically after CP14 (UI Audit) completes.

### Manual Invocation (If Needed)

```bash
# If you need to regenerate the summary
/validation-summary <SystemName>
```

---

## Output Files

| Path | Purpose |
|------|---------|
| `05-validation/VALIDATION_SUMMARY.md` | Human-readable summary report |
| `_state/validation_summary.json` | Machine-readable data for tooling |

---

## Success Criteria

- ✅ Summary auto-generated after CP14
- ✅ Includes all phase validations
- ✅ Shows Assembly-First compliance
- ✅ Reports test coverage
- ✅ Lists build artifacts
- ✅ Provides actionable recommendations
- ✅ JSON output available for programmatic access

---

## Example Output

```markdown
# Prototype Validation Summary

**Generated**: 2026-01-03T15:30:00Z
**Build Duration**: 18m 32s
**Status**: ✅ PASS

---

## Executive Summary

| Metric | Value | Status |
|--------|-------|--------|
| Overall Status | PASS | ✅ |
| Build Success | Yes | ✅ |
| Test Coverage | 85% | ✅ |
| Assembly-First Compliance | PASS | ✅ |
| P0 Coverage | 100% | ✅ |

---

## Phase-by-Phase Validation

| Phase | Status | Duration | Issues |
|-------|--------|----------|--------|
| CP8: Components | ✅ | 2m 15s | 0 |
| CP9: Screens | ✅ | 5m 42s | 0 |
| CP10: Interactions | ✅ | 1m 10s | 0 |
| CP11-12: Build | ✅ | 3m 30s | 0 |
| CP13: QA | ✅ | 3m 10s | 0 |
| CP14: UI Audit | ⚠️ | 4m 25s | 5 warnings |

**Total Build Time**: 18m 32s

---

## Assembly-First Compliance

| Check | Status | Details |
|-------|--------|---------|
| No raw HTML elements | ✅ | All screens use component library |
| Component imports valid | ✅ | All imports resolve correctly |
| Theme tokens used | ⚠️ | 5 arbitrary color values |
| No manual ARIA | ✅ | All ARIA handled by components |

**Files Checked**: 42
**Files with Violations**: 1
**Critical Violations**: 0
**Warnings**: 5

### Non-Blocking Warnings

Most common warnings:
1. Arbitrary color value: 5 occurrences (DoctorKanbanDashboard.tsx)

---

## Test Coverage

| Type | Coverage | Target | Status |
|------|----------|--------|--------|
| Unit Tests | 85% | 80% | ✅ |
| Integration Tests | 12 scenarios | - | ✅ |
| Accessibility | WCAG 2.1 AA | AA | ✅ |

**Total Test Files**: 28
- Unit: 20
- Integration: 6
- E2E: 2

---

## Build Artifacts

| Artifact | Count | Details |
|----------|-------|---------|
| Screens | 7 | Emergency Triage System |
| Components | 23 | Component library usage |
| Lines of Code | 2,450 | TypeScript + React |
| Bundle Size | 245 KB | (gzipped: 78 KB) |

### Screens by App

- **Triage App**: 5 screens
  - login, intake-form, triage-form, triage-queue, emergency-bypass
- **Doctor Dashboard**: 1 screen
  - kanban-dashboard
- **Public Display**: 1 screen
  - display-board

### Components by Category

- **Primitives**: 8
- **Data Display**: 5
- **Feedback**: 3
- **Navigation**: 2
- **Overlays**: 3
- **Patterns**: 2

---

## Recommendations

### Medium Priority (Nice to Have)

- Address 5 arbitrary color warnings in DoctorKanbanDashboard.tsx
- Consider adding E2E tests for critical user flows

---

## Next Steps

✅ **Prototype is approved for delivery**

1. Review validation summary with stakeholders
2. Address any non-blocking warnings (optional)
3. Proceed to ProductSpecs generation or delivery

---

**Report Generated**: 2026-01-03T15:30:00Z
**Phase 4 Enhancement**: Automated validation summary
```

---

## Related Files

- **Progress Tracking**: `_state/progress.json`
- **QA Report**: `05-validation/VALIDATION_REPORT.md`
- **Traceability**: `05-validation/TRACEABILITY_MATRIX.md`
- **Assembly Validator**: `.claude/hooks/assembly_first_validator.py`
- **Phase 4 Plan**: `PHASE_4_IMPLEMENTATION_PLAN.md`
