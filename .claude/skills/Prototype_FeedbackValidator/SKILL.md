---
name: validating-prototype-feedback
description: Use when you need to validate that feedback implementation matches the approved plan, all changes are properly traced, and the prototype still builds correctly.
model: haiku
allowed-tools: Bash, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-prototype-feedback started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-prototype-feedback ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-prototype-feedback instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

# Validate Prototype Feedback

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_FeedbackValidator
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Claude Code
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description

Validates that feedback implementation matches the approved plan, all versions are correctly incremented, traceability is maintained, and the prototype builds/runs correctly. Generates validation report and updates feedback status.

**Role**: You are a Quality Assurance Validator. Your expertise is verifying implementation completeness, traceability integrity, and overall system health after changes.

> **INTEGRATES**: verification-before-completion skill for thorough verification
> **INTEGRATES**: test-driven-development skill for test validation (Bug types)

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
- output files created (validation reports)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "validating-prototype-feedback"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "validating-prototype-feedback" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## Trigger Conditions

- Implementation phase completed (status = "implemented")
- Request to validate feedback implementation
- Pre-closure verification required

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Feedback ID | Yes | PF-NNN identifier |
| Implementation Log | Yes | implementation_log.md from session |
| Implementation Plan | Yes | implementation_plan.md from session |
| Prototype Path | Yes | `Prototype_<SystemName>` path |

## Validation Checklist

### Core Validations

| Check | Description | Severity |
|-------|-------------|----------|
| Plan Compliance | All plan steps executed | BLOCKING |
| Version Integrity | All versions incremented | BLOCKING |
| Traceability | Registries updated | BLOCKING |
| Build Success | Prototype builds | BLOCKING |
| No Regressions | Existing functionality works | WARNING |
| Bug Test (Bug type) | Regression test passes | BLOCKING |

## MANDATORY COMPREHENSIVE VALIDATION

> **CRITICAL**: Validation MUST verify ALL artifact layers were properly updated.

### Layer-by-Layer Validation Checklist

#### LAYER 1: Discovery Validation (ClientAnalysis_*)

| Check | File | Validation | Severity |
|-------|------|------------|----------|
| Screen Definition | `04-design-specs/screen-definitions.md` | Screen entry exists with zones, components | BLOCKING |
| Navigation | `04-design-specs/navigation-structure.md` | Screen in navigation hierarchy | BLOCKING |
| Data Fields | `04-design-specs/data-fields.md` | All new fields documented | WARNING |
| Interactions | `04-design-specs/interaction-patterns.md` | New patterns documented | WARNING |
| JTBD Link | `02-research/JOBS_TO_BE_DONE.md` | Feature linked to JTBD (if new feature) | WARNING |

#### LAYER 2: Prototype Specification Validation (Prototype_*)

| Check | Folder/File | Validation | Severity |
|-------|-------------|------------|----------|
| Component Index | `01-components/component-index.md` | New components listed | BLOCKING |
| Component Specs | `01-components/{category}/{component}/` | Spec file exists | BLOCKING |
| Screen Index | `02-screens/screen-index.md` | New screens listed | BLOCKING |
| Screen Specs | `02-screens/{platform}/{screen}/spec.md` | Spec file exists | BLOCKING |
| Interactions | `03-interactions/*.md` | Relevant specs updated | WARNING |
| Data Model | `04-implementation/data-model.md` | Entity schemas exist | BLOCKING |
| API Contracts | `04-implementation/api-contracts.json` | Endpoints defined | BLOCKING |
| Test Data | `04-implementation/test-data/` | Test data files exist | WARNING |

#### LAYER 3: Code Validation (prototype/src/)

| Check | Folder/File | Validation | Severity |
|-------|-------------|------------|----------|
| Screen Components | `src/screens/{platform}/` | Screen files exist | BLOCKING |
| Shared Components | `src/components/` | Component files exist | BLOCKING |
| Routing | `src/App.tsx` | Routes configured | BLOCKING |
| Mock Data | `src/data/` | Data files in correct location | WARNING |
| Build | `npm run build` | Build succeeds | BLOCKING |

#### LAYER 4: Registry Validation (ROOT LEVEL) - ALWAYS REQUIRED

| Check | File | Validation | Severity |
|-------|------|------------|----------|
| Screen Registry | `traceability/screen_registry.json` | - Entry in `discovery_screens[]` with feedback_source | BLOCKING |
| | | - Entry in `traceability[]` with all statuses | BLOCKING |
| | | - `screen_coverage` statistics updated | BLOCKING |
| Prototype Trace | `traceability/prototype_traceability_register.json` | - Entry in `screen_traceability.screens[]` | BLOCKING |
| | | - `coverage` counts updated | BLOCKING |
| | | - `feedback_source` field set | BLOCKING |
| Discovery Trace | `traceability/discovery_traceability_register.json` | Updated if discovery changed | WARNING |
| Requirements | `_state/requirements_registry.json` | Updated if requirements added | WARNING |

#### LAYER 5: Traceability Matrix Validation (helperFiles/)

| Check | File | Validation | Severity |
|-------|------|------------|----------|
| Master Matrix | `helperFiles/TRACEABILITY_MATRIX_MASTER.md` | Trace chain exists for new items | WARNING |
| Assessment | `helperFiles/TRACEABILITY_ASSESSMENT_REPORT.md` | Coverage metrics updated | WARNING |

## Procedure

### Phase 1: Load Implementation Data

```
READ from session folder:
  implementation_plan = implementation_plan.md
  implementation_log = implementation_log.md
  impact_analysis = impact_analysis.md

READ feedback entry:
  feedback = GET_FEEDBACK(feedback_id)

VERIFY feedback.status == "implemented"

IF status != "implemented":
  ERROR: "Cannot validate - implementation not complete"
  DISPLAY current status and suggest next action
  BLOCK
```

### Phase 2: Plan Compliance Check

```
EXTRACT planned_steps from implementation_plan
EXTRACT executed_steps from implementation_log

FOR each planned_step:
  FIND matching executed_step

  IF NOT found:
    ADD to compliance_failures:
      { step: N, issue: "Step not executed" }

  ELSE IF executed_step.status != "completed":
    ADD to compliance_failures:
      { step: N, issue: "Step failed: {error}" }

  ELSE:
    ADD to compliance_passed:
      { step: N, action: planned_step.action }

compliance_result = {
  passed: compliance_passed.length,
  failed: compliance_failures.length,
  total: planned_steps.length,
  status: compliance_failures.length == 0 ? "PASS" : "FAIL"
}

LOG: "Plan compliance: {passed}/{total} steps passed"
```

### Phase 3: Version Integrity Check

```
EXTRACT files_changed from implementation_log

FOR each changed_file:

  IF file.type == "md" OR file.type == "json":
    # Read current file
    content = READ(changed_file.path)
    metadata = EXTRACT_METADATA(content)

    # Verify version incremented
    IF metadata.version <= changed_file.version_before:
      ADD to version_failures:
        { file: path, issue: "Version not incremented" }

    # Verify change_history includes feedback reference
    last_change = metadata.change_history[-1]
    IF NOT last_change.changes.includes("PF-{feedback_id}"):
      ADD to version_failures:
        { file: path, issue: "Missing feedback reference in change_history" }

    # Verify updated_at is today
    IF metadata.updated_at != TODAY():
      ADD to version_warnings:
        { file: path, issue: "updated_at not current" }

version_result = {
  passed: files_checked - version_failures.length,
  failed: version_failures.length,
  warnings: version_warnings.length,
  status: version_failures.length == 0 ? "PASS" : "FAIL"
}

LOG: "Version integrity: {passed}/{total} files valid"
```

### Phase 4: Traceability Check

```
READ traceability registries:
  prototype_trace = traceability/prototype_traceability_register.json
  discovery_trace = traceability/discovery_traceability_register.json (if upstream)

# Check feedback is referenced
feedback_refs_found = 0

FOR each affected_item in impact_analysis.affected_items:
  FIND item in appropriate registry

  IF item.feedback_refs NOT includes "PF-{feedback_id}":
    ADD to traceability_failures:
      { item: item.id, issue: "Missing feedback reference" }
  ELSE:
    feedback_refs_found++

# Check trace links created
IF implementation_plan includes new_links:
  FOR each expected_link:
    IF NOT exists in registry.trace_links:
      ADD to traceability_failures:
        { link: expected_link, issue: "Link not created" }

traceability_result = {
  refs_found: feedback_refs_found,
  refs_expected: affected_items.length,
  failures: traceability_failures.length,
  status: traceability_failures.length == 0 ? "PASS" : "FAIL"
}

LOG: "Traceability: {refs_found}/{refs_expected} references found"
```

### Phase 5: Build Verification

```
IF implementation affected code files:

  LOG: "Running prototype build verification..."

  # Navigate to prototype directory
  cd Prototype_<SystemName>/prototype/

  # Check if dependencies are installed
  IF NOT exists node_modules/:
    RUN: npm install

  # Run build
  build_result = RUN: npm run build

  IF build_result.exit_code != 0:
    ADD to build_failures:
      { issue: "Build failed", output: build_result.stderr }
    build_status = "FAIL"
  ELSE:
    build_status = "PASS"

  # Run type check (if TypeScript)
  IF exists tsconfig.json:
    typecheck_result = RUN: npm run typecheck OR npx tsc --noEmit

    IF typecheck_result.exit_code != 0:
      ADD to build_warnings:
        { issue: "Type errors", output: typecheck_result.stderr }

  # Run lint (if configured)
  IF exists .eslintrc*:
    lint_result = RUN: npm run lint

    IF lint_result.exit_code != 0:
      ADD to build_warnings:
        { issue: "Lint warnings", output: lint_result.stderr }

build_result = {
  build: build_status,
  typecheck: typecheck_status,
  lint: lint_status,
  failures: build_failures,
  warnings: build_warnings
}

ELSE:
  LOG: "No code changes - skipping build verification"
  build_result = { status: "SKIPPED" }
```

### Phase 6: Bug Regression Test (Bug Type Only)

```
IF feedback.type == "Bug":

  LOG: "Verifying bug fix with regression test..."

  # Check if regression test was created (Option C)
  IF implementation_plan.option == "C":
    test_file = "prototype/src/__tests__/bugfix-PF-{id}.test.ts"

    IF NOT exists test_file:
      ADD to test_failures:
        { issue: "Regression test not created" }

    ELSE:
      # Run the specific test
      test_result = RUN: npm test -- --testPathPattern="bugfix-PF-{id}"

      IF test_result.exit_code != 0:
        ADD to test_failures:
          { issue: "Regression test failed", output: test_result.output }

  # Verify original bug scenario
  reproduction = feedback.debugging_evidence.reproduction

  PROMPT user:
    ════════════════════════════════════════════
     BUG VERIFICATION REQUIRED
    ════════════════════════════════════════════

    Please verify the original bug is fixed:

    Reproduction Steps:
    1. {reproduction.steps[0]}
    2. {reproduction.steps[1]}
    ...

    Expected Result: {reproduction.expected}

    Is the bug fixed?
    - "yes" - Bug is fixed
    - "no" - Bug still occurs
    - "partial" - Bug is partially fixed

    ════════════════════════════════════════════

  IF user_response == "no":
    ADD to test_failures:
      { issue: "Bug not fixed per user verification" }

  IF user_response == "partial":
    ADD to test_warnings:
      { issue: "Bug partially fixed - may need follow-up" }

test_result = {
  regression_test: test_file_result,
  user_verification: user_response,
  status: test_failures.length == 0 ? "PASS" : "FAIL"
}
```

### Phase 7: Quality Gates Validation

```
LOG: "Running prototype quality gates..."

# Run quality gate validation for affected checkpoints
affected_checkpoints = DETERMINE_AFFECTED_CHECKPOINTS(impact_analysis)

FOR each checkpoint in affected_checkpoints:
  gate_result = RUN: python3 .claude/hooks/prototype_quality_gates.py \
    --validate-checkpoint {checkpoint} \
    --dir Prototype_<SystemName>/

  IF gate_result.exit_code != 0:
    ADD to gate_failures:
      { checkpoint: checkpoint, output: gate_result.stderr }

gate_result = {
  checkpoints_checked: affected_checkpoints.length,
  failures: gate_failures.length,
  status: gate_failures.length == 0 ? "PASS" : "FAIL"
}
```

### Phase 8: Generate Validation Report

```
CREATE VALIDATION_REPORT.md in session folder:

---
document_id: PF-VAL-{ID}
version: 1.0.0
created_at: {date}
updated_at: {date}
generated_by: Prototype_FeedbackValidator
source_files:
  - implementation_log.md
  - implementation_plan.md
change_history:
  - version: "1.0.0"
    date: "{date}"
    author: "Prototype_FeedbackValidator"
    changes: "Validation execution"
---

# Validation Report

## Feedback Reference
- **ID**: PF-{id}
- **Type**: {type}
- **Validated At**: {timestamp}

---

## Overall Status: {PASS|FAIL}

---

## Validation Summary

| Check | Status | Details |
|-------|--------|---------|
| Plan Compliance | {PASS/FAIL} | {passed}/{total} steps |
| Version Integrity | {PASS/FAIL} | {passed}/{total} files |
| Traceability | {PASS/FAIL} | {refs_found}/{expected} refs |
| Build | {PASS/FAIL/SKIPPED} | {details} |
| Bug Test | {PASS/FAIL/N/A} | {details} |
| Quality Gates | {PASS/FAIL} | {checkpoints} |

---

## Detailed Results

### Plan Compliance
{compliance_details}

### Version Integrity
{version_details}

### Traceability
{traceability_details}

### Build Verification
{build_details}

### Bug Regression Test (if applicable)
{test_details}

### Quality Gates
{gate_details}

---

## Failures (if any)

{FOR each failure:}
### {failure.category}
- **Issue**: {failure.issue}
- **Details**: {failure.details}
- **Suggested Fix**: {failure.suggestion}

---

## Warnings (if any)

{FOR each warning:}
- {warning.issue}: {warning.details}

---

## Recommendation

{IF all_passed:}
**APPROVED FOR CLOSURE**
All validation checks passed. Feedback implementation is complete and verified.

{ELSE:}
**REQUIRES ATTENTION**
{count} validation failures found. Address the issues above before closing.

---

**Validated By**: Prototype_FeedbackValidator
**Timestamp**: {timestamp}
```

### Phase 9: Update Status and Generate Summary

```
# Determine final status
IF all validations passed:
  final_status = "validated"
ELSE:
  final_status = "failed"

# Update feedback registry
UPDATE feedback entry:
  status: final_status
  lifecycle.validated_at: NOW() (if passed)

# Generate files_changed.md summary
CREATE files_changed.md in session folder:

---
document_id: PF-CHANGES-{ID}
version: 1.0.0
created_at: {date}
...
---

# Files Changed Summary

## Statistics
- **Total Files Modified**: {N}
- **Discovery Files**: {N}
- **Specification Files**: {N}
- **Code Files**: {N}

## Changes by Category

### Discovery Materials
| File | Change Type | Version | Description |
|------|-------------|---------|-------------|
| {path} | Modified | 1.0.0 → 1.1.0 | PF-{id}: {description} |

### Specifications
| File | Change Type | Version | Description |
|------|-------------|---------|-------------|
| ... | ... | ... | ... |

### Code Files
| File | Change Type | Description |
|------|-------------|-------------|
| ... | ... | ... |

### Traceability
| Registry | Items Updated | IDs |
|----------|---------------|-----|
| ... | ... | ... |

---

## Version Change Log

| File | Before | After | Change Type |
|------|--------|-------|-------------|
| {path} | 1.0.0 | 1.1.0 | Minor |

---

**Generated**: {timestamp}


# Generate FEEDBACK_SUMMARY.md
CREATE FEEDBACK_SUMMARY.md in session folder:

---
document_id: PF-SUMMARY-{ID}
version: 1.0.0
...
---

# Feedback Summary

## Overview
| Field | Value |
|-------|-------|
| **ID** | PF-{id} |
| **Type** | {type} |
| **Status** | {final_status} |
| **Title** | {title} |

---

## Timeline

| Phase | Timestamp | Duration |
|-------|-----------|----------|
| Created | {created_at} | - |
| Approved | {approved_at} | {duration} |
| Implementation Started | {started_at} | {duration} |
| Implementation Completed | {implemented_at} | {duration} |
| Validated | {validated_at} | {duration} |
| **Total** | - | **{total_duration}** |

---

## Impact Summary
- **Discovery Files**: {N}
- **Specification Files**: {N}
- **Code Files**: {N}
- **Total**: {N}

---

## Implementation Option
**Selected**: Option {X} - {name}

---

## Validation Status
{PASS/FAIL with summary}

---

## Artifacts Generated
| Artifact | Path |
|----------|------|
| Original Feedback | FEEDBACK_ORIGINAL.md |
| Impact Analysis | impact_analysis.md |
| Implementation Options | implementation_options.md |
| Implementation Plan | implementation_plan.md |
| Implementation Log | implementation_log.md |
| Files Changed | files_changed.md |
| Validation Report | VALIDATION_REPORT.md |
| This Summary | FEEDBACK_SUMMARY.md |

---

**Feedback Processing Complete**
```

## Integration Points

### Receives From
- `Prototype_FeedbackImplementer` - Implementation log
- `Prototype_FeedbackPlanner` - Implementation plan
- `Prototype_FeedbackAnalyzer` - Impact analysis

### Feeds Into
- `Prototype_FeedbackRegister` - Status update to "validated" or "failed"
- User - Validation report for review

### Uses Skills
- `verification-before-completion` - Thorough verification patterns
- `test-driven-development` - Test validation for bugs

## Post-Validation Actions

```
IF validation passed:
  DISPLAY:
    ════════════════════════════════════════════
     VALIDATION PASSED
    ════════════════════════════════════════════

    PF-{id}: {title}
    Status: VALIDATED

    All checks passed:
    ✓ Plan compliance
    ✓ Version integrity
    ✓ Traceability
    ✓ Build verification
    ✓ Bug test (if applicable)
    ✓ Quality gates

    Ready for closure.

    Next: "close" to finalize
    ════════════════════════════════════════════

IF validation failed:
  DISPLAY:
    ════════════════════════════════════════════
     VALIDATION FAILED
    ════════════════════════════════════════════

    PF-{id}: {title}
    Status: FAILED

    Issues found:
    {FOR each failure:}
    ✗ {failure.category}: {failure.issue}

    Options:
    - "fix" - Address issues and re-validate
    - "rollback" - Restore from backup
    - "override" - Close with known issues (not recommended)
    ════════════════════════════════════════════
```

## Error Handling

| Issue | Action |
|-------|--------|
| Implementation log missing | Error, cannot validate |
| Build fails | Mark as FAIL, suggest fix |
| Test not found | Warn, continue validation |
| Registry read error | Warn, mark traceability as incomplete |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: Prototype Skills Framework v2.3
