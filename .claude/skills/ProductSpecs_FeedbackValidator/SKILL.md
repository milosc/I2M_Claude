---
name: validating-productspecs-feedback
description: Use when you need to validate that ProductSpecs feedback implementation matches the approved plan and all changes are properly traced with full registry and traceability verification.
model: haiku
allowed-tools: Bash, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-productspecs-feedback started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-productspecs-feedback ended '{"stage": "productspecs"}'
---

# Validate ProductSpecs Feedback

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill validating-productspecs-feedback instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: ProductSpecs_FeedbackValidator
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Claude Code
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description

Validates that ProductSpecs feedback implementation is complete, all changes match the approved plan, registries are consistent, traceability chains are intact, and JIRA exports are up-to-date.

**Role**: You are a Validation Specialist. Your expertise is verifying implementation completeness, ensuring registry consistency, and confirming traceability integrity across all ProductSpecs artifacts.

---

## Trigger Conditions

- Implementation marked as complete
- User requests validation
- Pre-closure verification

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Feedback ID | Yes | PSF-XXX identifier |
| ProductSpecs Path | Yes | `ProductSpecs_<SystemName>` folder path |

## Validation Checks

### Check Categories

| Category | Weight | Description |
|----------|--------|-------------|
| Plan Compliance | 30% | All planned steps executed |
| Registry Integrity | 25% | All JSON registries valid |
| Version Consistency | 15% | All versions incremented properly |
| Traceability | 20% | All chains intact |
| JIRA Sync | 10% | Export matches registries |

## Procedure

### Phase 1: Load Validation Context

```
READ feedback entry from registry
READ implementation_plan from session folder
READ files_changed.md from session folder
READ implementation_log.md from session folder

VERIFY status == "implemented"

IF status != "implemented":
  ERROR: "Cannot validate - status is {status}, expected 'implemented'"
  EXIT

LOG: "Starting validation for {feedback_id}"
```

### Phase 2: Validate Plan Compliance

```
READ plan.steps from implementation_plan

FOR each step IN plan.steps:
  CHECK step was executed:
    - Entry exists in implementation_log
    - No error recorded for step
    - File modified as expected

  IF step not executed:
    ADD to compliance_failures: {
      step: step_number,
      expected: step.action,
      actual: "not executed"
    }

CALCULATE compliance_score:
  executed_steps / total_steps * 100

LOG: "Plan compliance: {compliance_score}%"
```

### Phase 3: Validate Registry Integrity

```
REGISTRIES = [
  "_registry/modules.json",
  "_registry/requirements.json",
  "_registry/nfrs.json",
  "_registry/test-cases.json",
  "_registry/traceability.json"
]

FOR each registry IN REGISTRIES:
  TRY:
    LOAD and parse JSON

    VALIDATE:
      - $metadata exists
      - Schema version compatible
      - All required fields present
      - No duplicate IDs
      - Statistics match counts

    IF validation fails:
      ADD to registry_failures: {
        file: registry,
        issues: [list_of_issues]
      }

  CATCH parse_error:
    ADD to registry_failures: {
      file: registry,
      issues: ["Invalid JSON: {error}"]
    }

CALCULATE registry_score:
  valid_registries / total_registries * 100

LOG: "Registry integrity: {registry_score}%"
```

### Phase 4: Validate Version Consistency

```
READ files_changed.md
EXTRACT list of changed files with expected versions

FOR each changed_file:
  READ current file
  EXTRACT current version from frontmatter/$metadata

  VERIFY:
    - Version was incremented
    - updated_at is recent
    - change_history includes this update (for markdown)

  IF version not incremented:
    ADD to version_failures: {
      file: changed_file,
      expected: "incremented",
      actual: current_version
    }

CALCULATE version_score:
  correct_versions / total_changes * 100

LOG: "Version consistency: {version_score}%"
```

### Phase 5: Validate Traceability Chains

```
READ traceability.json
READ requirements.json
READ modules.json
READ test-cases.json

FOR each chain IN traceability.chains:
  VERIFY chain integrity:

  # Check all IDs exist
  FOR req_id IN chain.requirements:
    IF req_id NOT IN requirements.requirements:
      ADD to trace_failures: "Orphan requirement: {req_id}"

  FOR mod_id IN chain.modules:
    IF mod_id NOT IN modules.modules:
      ADD to trace_failures: "Orphan module: {mod_id}"

  FOR test_id IN chain.tests:
    IF test_id NOT IN test_cases.test_cases:
      ADD to trace_failures: "Orphan test: {test_id}"

  # Check bidirectional links
  VERIFY requirements reference correct modules
  VERIFY modules reference correct screens
  VERIFY tests reference correct requirements

# Verify P0 coverage
p0_requirements = filter(requirements, priority == "P0")
p0_with_full_chain = filter(chains, has_complete_chain AND priority == "P0")

p0_coverage = len(p0_with_full_chain) / len(p0_requirements) * 100

IF p0_coverage < 100:
  ADD to trace_failures: "P0 coverage: {p0_coverage}% (required: 100%)"

CALCULATE trace_score:
  (chains_valid / total_chains) * 100

LOG: "Traceability: {trace_score}%, P0 coverage: {p0_coverage}%"
```

### Phase 6: Validate JIRA Sync

```
READ jira-import.json
READ requirements.json
READ modules.json

# Verify all requirements have JIRA items
FOR req IN requirements.requirements:
  IF req.id NOT IN jira_import.hierarchy.stories[].requirement_ref:
    ADD to jira_failures: "Missing JIRA item for {req.id}"

# Verify all modules have JIRA epics
FOR mod IN modules.modules:
  IF mod.id NOT IN jira_import.hierarchy.epics[].module_ref:
    ADD to jira_failures: "Missing JIRA epic for {mod.id}"

# Verify JIRA metadata is recent
IF jira_import.$metadata.updated_at < implementation_started_at:
  ADD to jira_failures: "JIRA export not regenerated after implementation"

CALCULATE jira_score:
  items_synced / total_items * 100

LOG: "JIRA sync: {jira_score}%"
```

### Phase 7: Run Quality Gates

```
RUN quality gate validation:

python3 .claude/hooks/productspecs_quality_gates.py \
  --validate-checkpoint 7 \
  --dir ProductSpecs_<SystemName>/

IF validation fails:
  ADD to gate_failures: quality_gate_output
  LOG: "Quality gate validation failed"
ELSE:
  LOG: "Quality gate validation passed"
```

### Phase 8: Calculate Overall Score

```
CALCULATE overall_score:
  compliance_score * 0.30 +
  registry_score * 0.25 +
  version_score * 0.15 +
  trace_score * 0.20 +
  jira_score * 0.10

DETERMINE validation_status:
  IF overall_score >= 95 AND no_critical_failures:
    status = "passed"
  ELIF overall_score >= 80:
    status = "passed_with_warnings"
  ELSE:
    status = "failed"

LOG: "Overall validation: {status} ({overall_score}%)"
```

### Phase 9: Generate Validation Report

```
WRITE VALIDATION_REPORT.md to session folder:

---
document_id: PSF-VALID-{feedback_id}
version: 1.0.0
created_at: {timestamp}
generated_by: ProductSpecs_FeedbackValidator
---

# Validation Report

## Summary
- **Feedback ID**: {feedback_id}
- **Status**: {validation_status}
- **Overall Score**: {overall_score}%
- **Validated At**: {timestamp}

## Score Breakdown

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Plan Compliance | {compliance}% | 30% | {weighted} |
| Registry Integrity | {registry}% | 25% | {weighted} |
| Version Consistency | {version}% | 15% | {weighted} |
| Traceability | {trace}% | 20% | {weighted} |
| JIRA Sync | {jira}% | 10% | {weighted} |
| **Overall** | | | **{overall}%** |

## Validation Details

### Plan Compliance
{compliance_details}

### Registry Integrity
{registry_details}

### Version Consistency
{version_details}

### Traceability
{trace_details}

### JIRA Sync
{jira_details}

## Issues Found

### Critical (Blocking)
{critical_issues OR "None"}

### Warnings (Non-blocking)
{warning_issues OR "None"}

## Recommendation

{recommendation based on status}
```

### Phase 10: Update Status

```
IF validation_status == "passed":
  UPDATE feedback entry:
    status: "implemented" → "validated"
    lifecycle.validated_at: NOW()

  LOG: "Feedback {feedback_id} validated successfully"

ELIF validation_status == "passed_with_warnings":
  UPDATE feedback entry:
    status: "implemented" → "validated"
    lifecycle.validated_at: NOW()
    warnings: [list_of_warnings]

  LOG: "Feedback {feedback_id} validated with warnings"

ELSE:
  UPDATE feedback entry:
    status: "implemented" → "failed"
    validation_failures: [list_of_failures]

  LOG: "Feedback {feedback_id} validation failed"
```

## Output Format

### Validation Progress

```
═══════════════════════════════════════════════════════════════
 VALIDATING PRODUCTSPECS FEEDBACK
═══════════════════════════════════════════════════════════════

Feedback ID: PSF-001

Validation Progress:
├─ [✓] Plan Compliance: 100%
├─ [✓] Registry Integrity: 100%
├─ [✓] Version Consistency: 100%
├─ [▶] Traceability: Checking chains...
├─ [ ] JIRA Sync
└─ [ ] Quality Gates

═══════════════════════════════════════════════════════════════
```

### Validation Complete (Passed)

```
═══════════════════════════════════════════════════════════════
 VALIDATION COMPLETE - PASSED
═══════════════════════════════════════════════════════════════

Feedback ID: PSF-001
Status: ✅ VALIDATED
Overall Score: 98%

Score Breakdown:
├─ Plan Compliance:    100% (30% weight)
├─ Registry Integrity: 100% (25% weight)
├─ Version Consistency: 100% (15% weight)
├─ Traceability:        95% (20% weight)
└─ JIRA Sync:          100% (10% weight)

P0 Traceability: 100%
Quality Gates: ✅ Passed

Warnings:
└─ 1 P1 requirement missing test coverage

Next Steps:
1. Review VALIDATION_REPORT.md for details
2. Run /productspecs-feedback close PSF-001 to finalize

═══════════════════════════════════════════════════════════════
```

### Validation Complete (Failed)

```
═══════════════════════════════════════════════════════════════
 VALIDATION FAILED
═══════════════════════════════════════════════════════════════

Feedback ID: PSF-001
Status: ❌ FAILED
Overall Score: 72%

Critical Issues:
1. P0 traceability coverage: 95% (required: 100%)
2. Registry integrity: modules.json has duplicate ID
3. JIRA export not regenerated

Action Required:
1. Fix duplicate ID in modules.json
2. Complete traceability for REQ-007
3. Regenerate JIRA export

To retry:
1. Fix issues above
2. Run /productspecs-feedback implement PSF-001 --resume
3. Run /productspecs-feedback validate PSF-001

═══════════════════════════════════════════════════════════════
```

## Integration Points

### Receives From
- `ProductSpecs_FeedbackImplementer` - Completed implementation
- Quality gates hook - Validation results

### Feeds Into
- `ProductSpecs_FeedbackRegister` - Status updates
- Feedback closure workflow

## Error Handling

| Issue | Action |
|-------|--------|
| Registry unreadable | Mark check as failed, continue |
| Traceability incomplete | Calculate partial score, flag |
| JIRA mismatch | Flag for regeneration |
| Quality gate fails | Include in report, fail validation |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: ProductSpecs Skills Framework v1.0
