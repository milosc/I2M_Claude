---
name: validating-discovery-feedback-implementation
description: Use when you need to validate that feedback implementation matches the approved plan and all changes are properly traced.
model: haiku
allowed-tools: Bash, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-discovery-feedback-implementation started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-discovery-feedback-implementation ended '{"stage": "discovery"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-discovery-feedback-implementation instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

---

# Validate Discovery Feedback Implementation

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_FeedbackValidator
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Milos Cigoj
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description
Validates that feedback implementation matches the approved plan, verifies all changes are properly traced, and triggers post-implementation workflows (Discovery_Validate, Discovery_Traceability rebuild).

**Role**: You are a Feedback Validation Specialist. Your expertise is ensuring implementation fidelity, traceability completeness, and triggering appropriate post-implementation quality gates.

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
- output files created (validation report)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "validating-discovery-feedback-implementation"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "validating-discovery-feedback-implementation" --stage discovery
```

Logging is handled automatically by the skill framework. No user action required.

---

## Trigger Conditions

- Implementation has been completed (full or partial)
- Request mentions "validate feedback", "verify implementation"
- Feedback status is `implemented`

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Feedback ID | Yes | FB-<NNN> identifier |
| Implementation Plan | Yes | IMPLEMENTATION_PLAN.md |
| Implementation Log | Yes | IMPLEMENTATION_LOG.md |
| Discovery Path | Yes | ClientAnalysis_<SystemName> path |

## Validation Framework

### 1. Plan Compliance Check

Verify each planned step was executed:

```
For each step in plan:
  CHECK: Step appears in log
  CHECK: Step status is COMPLETED
  CHECK: Target file was modified
  CHECK: Changes match plan description
  RESULT: PASS / FAIL / PARTIAL
```

### 2. Version Integrity Check

Verify version metadata consistency:

```
For each modified file:
  CHECK: Version was incremented
  CHECK: updated_at reflects today
  CHECK: change_history includes FB-<NNN> reference
  CHECK: generated_by is appropriate skill
  RESULT: PASS / FAIL / PARTIAL
```

### 3. Traceability Completeness Check

Verify all traceability requirements:

```
For each affected traceability ID:
  CHECK: ID exists in appropriate registry
  CHECK: Registry item has feedback reference
  CHECK: trace_links.json updated (if applicable)
  CHECK: Downstream items flagged for review
  RESULT: PASS / FAIL / PARTIAL
```

### 4. Content Validation

Verify content quality:

```
For each modified section:
  CHECK: Content is non-empty
  CHECK: No placeholder text remains
  CHECK: Formatting is consistent
  CHECK: Cross-references are valid
  RESULT: PASS / FAIL / WARNING
```

### 5. Downstream Impact Validation

Verify downstream consistency:

```
For each downstream dependency:
  CHECK: File exists
  CHECK: References to modified items are valid
  CHECK: No orphaned references
  RESULT: PASS / FAIL / WARNING
```

## Post-Validation Actions

### If All Checks Pass:

```
1. Update feedback status to "validated"
2. Execute: /discovery-validate (re-run full validation)
3. Execute: /discovery-rebuild-traceability
4. Generate VALIDATION_REPORT.md
5. Generate FEEDBACK_SUMMARY.md
```

### If Checks Fail:

```
1. Update feedback status to "failed"
2. Generate failure report with specific issues
3. Provide remediation steps
4. Offer to retry failed validations
```

## Output Format

### Primary Output: `VALIDATION_REPORT.md` (in feedback session folder)

```markdown
---
document_id: FB-VAL-<ID>
version: 1.0.0
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
generated_by: Discovery_FeedbackValidator
source_files:
  - IMPLEMENTATION_PLAN.md
  - IMPLEMENTATION_LOG.md
change_history:
  - version: "1.0.0"
    date: "<YYYY-MM-DD>"
    author: "Discovery_FeedbackValidator"
    changes: "Validation execution"
---

# Validation Report

## Feedback Reference
- **ID**: FB-<NNN>
- **Implementation**: [Complete/Partial]
- **Validated At**: <YYYY-MM-DD HH:MM>

---

## Validation Summary

| Check Category | Passed | Failed | Warnings | Total |
|----------------|--------|--------|----------|-------|
| Plan Compliance | N | N | N | N |
| Version Integrity | N | N | N | N |
| Traceability | N | N | N | N |
| Content Quality | N | N | N | N |
| Downstream Impact | N | N | N | N |
| **TOTAL** | N | N | N | N |

### Overall Status: PASSED / FAILED / PASSED WITH WARNINGS

---

## Detailed Results

### 1. Plan Compliance

| Step | Expected | Actual | Status |
|------|----------|--------|--------|
| Step 1 | [description] | [result] | PASS/FAIL |
| Step 2 | [description] | [result] | PASS/FAIL |

**Issues Found**:
- [Issue 1]
- [Issue 2]

---

### 2. Version Integrity

| File | Expected Version | Actual Version | FB Reference | Status |
|------|------------------|----------------|--------------|--------|
| [path] | [version] | [version] | [yes/no] | PASS/FAIL |

**Issues Found**:
- [Issue 1]

---

### 3. Traceability Completeness

| ID | Registry | Updated | Linked | Status |
|----|----------|---------|--------|--------|
| [ID] | [registry] | [yes/no] | [yes/no] | PASS/FAIL |

**Issues Found**:
- [Issue 1]

---

### 4. Content Quality

| File | Section | Issue Type | Details |
|------|---------|------------|---------|
| [path] | [section] | [type] | [details] |

---

### 5. Downstream Impact

| File | Dependency | Status | Notes |
|------|------------|--------|-------|
| [path] | [dependency] | PASS/WARN | [notes] |

---

## Post-Validation Actions

### Executed

- [ ] Discovery_Validate: [PASSED/FAILED]
  - [Details or link to validation report]
- [ ] Discovery_Traceability Rebuild: [PASSED/FAILED]
  - [Details or link to traceability output]

### Feedback Status Update

- **Previous Status**: implemented
- **New Status**: validated / failed
- **Updated At**: <timestamp>

---

## Remediation Steps (if failed)

### Critical Issues (Must Fix)

1. **[Issue]**
   - File: [path]
   - Problem: [description]
   - Fix: [action to take]

### Warnings (Recommended)

1. **[Issue]**
   - File: [path]
   - Recommendation: [action]

---

## Final Certification

**Validation Status**: CERTIFIED / NOT CERTIFIED

**Validator**: Discovery_FeedbackValidator v1.0.0
**Timestamp**: <YYYY-MM-DD HH:MM:SS>
```

### Secondary Output: `FEEDBACK_SUMMARY.md` (in feedback session folder)

```markdown
---
document_id: FB-SUM-<ID>
version: 1.0.0
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
generated_by: Discovery_FeedbackValidator
source_files:
  - FEEDBACK_ORIGINAL.md
  - IMPACT_ANALYSIS.md
  - IMPLEMENTATION_PLAN.md
  - IMPLEMENTATION_LOG.md
  - VALIDATION_REPORT.md
change_history:
  - version: "1.0.0"
    date: "<YYYY-MM-DD>"
    author: "Discovery_FeedbackValidator"
    changes: "Summary generation"
---

# Feedback Summary

## Overview

| Field | Value |
|-------|-------|
| Feedback ID | FB-<NNN> |
| Status | [validated/failed/rejected] |
| Source | [who provided] |
| Inputter | [who entered] |
| Received | [date] |
| Completed | [date] |

---

## Feedback Content

> [Original feedback text]

---

## Implementation Summary

- **Plan Used**: [A/B/Custom]
- **Files Modified**: N
- **Steps Completed**: N/M
- **Traceability IDs Updated**: N

---

## Key Changes

| Area | Change | Impact |
|------|--------|--------|
| [area] | [change] | [impact] |

---

## Artifacts

| Document | Location |
|----------|----------|
| Original Feedback | [path] |
| Impact Analysis | [path] |
| Implementation Plan | [path] |
| Implementation Log | [path] |
| Validation Report | [path] |

---

## Timeline

| Event | Timestamp | Actor |
|-------|-----------|-------|
| Received | [time] | [source] |
| Logged | [time] | [inputter] |
| Approved | [time] | [approver] |
| Implemented | [time] | Discovery_FeedbackImplementer |
| Validated | [time] | Discovery_FeedbackValidator |

---

**Session Folder**: `traceability/feedback_sessions/discovery/<YYYY-MM-DD>_Feedback_<NNN>/`
```

## Integration Points

### Receives From
- `Discovery_FeedbackImplementer` - Implementation log
- `Discovery_FeedbackPlanner` - Implementation plan
- `Discovery_FeedbackRegister` - Feedback details

### Feeds Into
- `Discovery_FeedbackRegister` - Final status update
- `Discovery_Validate` - Full re-validation trigger
- `Traceability_Manager` - Rebuild trigger

## Error Handling

| Issue | Action |
|-------|--------|
| Missing implementation log | Cannot validate, report error |
| Missing plan file | Cannot validate, report error |
| Partial implementation | Validate completed steps only |
| Discovery_Validate fails | Log in report, flag for attention |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: Discovery Skills Framework v2.0
