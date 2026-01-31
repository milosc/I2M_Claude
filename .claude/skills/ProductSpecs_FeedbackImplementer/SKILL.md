---
name: implementing-productspecs-feedback
description: Use when you need to execute approved implementation plans for ProductSpecs feedback with full traceability, version control, and resumption capability.
model: sonnet
allowed-tools: Read, Write, Edit, Bash
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill implementing-productspecs-feedback started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill implementing-productspecs-feedback ended '{"stage": "productspecs"}'
---

# Implement ProductSpecs Feedback

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill implementing-productspecs-feedback instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: ProductSpecs_FeedbackImplementer
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Claude Code
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description

Executes approved implementation plans for ProductSpecs feedback, modifying module specifications, requirements, NFRs, tests, and regenerating JIRA exports while maintaining full traceability and version control.

**Role**: You are an Implementation Specialist. Your expertise is executing changes systematically with proper versioning, maintaining traceability, and handling JIRA regeneration.

---

## Trigger Conditions

- Implementation plan approved by user
- Resume request for failed/partial implementation
- Single-step execution request

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Feedback ID | Yes | PSF-XXX identifier |
| Implementation Plan | Yes | Approved plan from user |
| ProductSpecs Path | Yes | `ProductSpecs_<SystemName>` folder path |
| Resume Point | No | Step to resume from (if resuming) |

## Implementation Order

Changes are applied in this order to maintain consistency:

```
1. Requirements Registry    # Source of truth
2. Module Specifications    # Depend on requirements
3. NFR Specifications       # May depend on modules
4. Test Specifications      # Depend on requirements
5. Traceability Registry    # References all above
6. JIRA Export             # Generated from all above
```

## Procedure

### Phase 1: Load Implementation Context

```
READ feedback entry from registry
READ implementation_plan from session folder
READ affected_items from impact_analysis

DETERMINE:
  - start_step = resume_point.step_number OR 0
  - total_steps = len(plan.steps)

LOG: "Starting implementation from step {start_step + 1}/{total_steps}"
```

### Phase 2: Update Registry Status

```
UPDATE feedback status: "approved" → "in_progress"

WRITE to session folder: implementation_log.md

---
document_id: PSF-IMPL-{feedback_id}
version: 1.0.0
started_at: {timestamp}
---

# Implementation Log

## Session Info
- **Feedback ID**: {feedback_id}
- **Plan Selected**: {plan_id}
- **Started**: {timestamp}
- **Status**: In Progress

## Execution Log
```

### Phase 3: Execute Steps

```
FOR step_number, step IN plan.steps[start_step:]:
  LOG_STEP_START(step_number, step)

  TRY:
    CASE step.action:

      "update_requirement":
        LOAD requirements.json
        FIND requirement by ID
        UPDATE fields as specified
        INCREMENT version
        SAVE requirements.json
        LOG: "Updated {req_id} v{version}"

      "update_module":
        LOAD MOD-XXX.md
        UPDATE sections as specified
        INCREMENT frontmatter version
        SAVE MOD-XXX.md
        LOG: "Updated {module_id} v{version}"

      "update_nfr":
        LOAD nfrs.json
        FIND NFR by ID
        UPDATE fields as specified
        SAVE nfrs.json
        LOG: "Updated {nfr_id}"

      "update_test":
        LOAD test-cases.json
        FIND test by ID
        UPDATE fields as specified
        SAVE test-cases.json
        LOG: "Updated {test_id}"

      "add_requirement":
        LOAD requirements.json
        GENERATE new requirement ID
        ADD to requirements array
        UPDATE statistics
        SAVE requirements.json
        LOG: "Added {new_req_id}"

      "add_test":
        LOAD test-cases.json
        GENERATE new test ID
        ADD to test_cases array
        UPDATE statistics
        SAVE test-cases.json
        LOG: "Added {new_test_id}"

      "remove_item":
        LOAD appropriate registry
        REMOVE item by ID
        UPDATE statistics
        SAVE registry
        LOG: "Removed {item_id}"

      "update_traceability":
        LOAD traceability.json
        UPDATE chains as specified
        RECALCULATE coverage
        SAVE traceability.json
        LOG: "Updated traceability chains"

    SET_RESUME_POINT(step_number + 1, step.file, "pending")
    LOG_STEP_COMPLETE(step_number, step)

  CATCH error:
    SET_RESUME_POINT(step_number, step.file, step.action)
    LOG_STEP_FAILED(step_number, step, error)
    UPDATE status: "in_progress" → "failed"
    THROW error

LOG: "All {total_steps} steps completed"
```

### Phase 4: Regenerate JIRA Export

```
IF impact_analysis.traceability_impact.jira_regeneration_needed:
  LOG: "Regenerating JIRA export files..."

  LOAD all registries:
    - modules.json
    - requirements.json
    - nfrs.json
    - test-cases.json
    - traceability.json

  LOAD jira_config.json

  REGENERATE:
    - full-hierarchy.csv
    - epics-and-stories.csv
    - subtasks-only.csv
    - jira-import.json

  UPDATE jira-import.json metadata:
    - updated_at: NOW()
    - regenerated_by: "ProductSpecs_FeedbackImplementer"
    - reason: feedback_id

  LOG: "JIRA export regenerated"
ELSE:
  LOG: "JIRA regeneration not required"
```

### Phase 5: Update Traceability

```
LOAD traceability.json

FOR each affected_chain:
  VERIFY chain integrity:
    - All IDs exist in respective registries
    - Links are bidirectional
    - Coverage still meets thresholds

  IF chain broken:
    FLAG for review
    ADD to validation_issues

UPDATE traceability.json:
  - chains: updated_chains
  - coverage: recalculated_coverage
  - updated_at: NOW()

SAVE traceability.json

LOG: "Traceability updated, coverage: {p0_coverage}%"
```

### Phase 6: Record Changes

```
CREATE files_changed.md in session folder:

---
document_id: PSF-CHANGES-{feedback_id}
version: 1.0.0
created_at: {timestamp}
---

# Files Changed

## Summary
- **Total Files Modified**: {count}
- **Registries Updated**: {list}
- **JIRA Regenerated**: {Yes/No}

## Change Details

### Requirements Registry
| Action | ID | Field | Old Value | New Value |
|--------|----|----|-----------|-----------|
| Update | REQ-001 | title | "Old title" | "New title" |
| Update | REQ-001 | priority | P1 | P0 |

### Module Specifications
| Action | File | Version | Changes |
|--------|------|---------|---------|
| Update | MOD-INV-SEARCH-01.md | 1.0.0 → 1.1.0 | Updated description |

### Test Specifications
| Action | ID | Changes |
|--------|----|----|
| Add | TC-E2E-015 | New E2E test for updated flow |

### JIRA Export
- Regenerated: {timestamp}
- Items affected: {count}
```

### Phase 7: Update Status

```
UPDATE feedback entry:
  status: "in_progress" → "implemented"
  lifecycle.implemented_at: NOW()
  resume_point: null

UPDATE implementation_log.md:
  - Status: Completed
  - Completed at: {timestamp}
  - Steps executed: {total_steps}

LOG: "Implementation complete for {feedback_id}"
```

## Resume Capability

### Resume Point Structure

```json
{
  "step_number": 3,
  "file_path": "01-modules/MOD-INV-SEARCH-01.md",
  "action": "update_module",
  "timestamp": "2025-12-22T10:30:00Z"
}
```

### Resume Procedure

```
READ resume_point from registry entry

IF resume_point exists:
  DISPLAY: "Resuming from step {step_number}: {action} on {file_path}"

  VERIFY file state:
    - File exists
    - Previous steps completed

  CONTINUE from step_number
```

## Version Control

### Version Increment Rules

```
For JSON registries:
  - $metadata.updated_at = NOW()
  - Individual item versions as appropriate

For Markdown files:
  - frontmatter.version: increment minor (1.0.0 → 1.1.0)
  - frontmatter.updated_at: NOW()
  - Add to change_history array

For CSV files:
  - Regenerate completely (no versioning)

For JIRA JSON:
  - $metadata.updated_at = NOW()
  - $metadata.regenerated_by = skill_id
```

## Output Format

### Implementation Progress

```
═══════════════════════════════════════════════════════════════
 IMPLEMENTING PRODUCTSPECS FEEDBACK
═══════════════════════════════════════════════════════════════

Feedback ID: PSF-001
Plan: Option A - Update Requirements and Cascade

Progress: ████████░░░░░░░░░░░░ 40%

Step 3/8: Updating MOD-INV-SEARCH-01.md
├─ Reading module specification...
├─ Updating description section...
├─ Incrementing version: 1.0.0 → 1.1.0
└─ ✓ Saved

═══════════════════════════════════════════════════════════════
```

### Implementation Complete

```
═══════════════════════════════════════════════════════════════
 IMPLEMENTATION COMPLETE
═══════════════════════════════════════════════════════════════

Feedback ID: PSF-001
Status: Implemented
Duration: 2 minutes

Changes Made:
├─ Requirements: 3 updated
├─ Modules: 2 updated
├─ Tests: 4 added
├─ Traceability: Updated
└─ JIRA: Regenerated

Files Changed:
├─ _registry/requirements.json
├─ _registry/test-cases.json
├─ _registry/traceability.json
├─ 01-modules/MOD-INV-SEARCH-01.md
├─ 01-modules/MOD-INV-ADJUST-01.md
├─ 04-jira/full-hierarchy.csv
├─ 04-jira/jira-import.json
└─ (7 files total)

Next: Run /productspecs-feedback validate PSF-001
═══════════════════════════════════════════════════════════════
```

## Integration Points

### Receives From
- `ProductSpecs_FeedbackRegister` - Approved feedback, resume points
- User input - Plan selection, approval

### Feeds Into
- `ProductSpecs_FeedbackValidator` - Completed implementation
- JIRA export files - Regenerated content
- Traceability registry - Updated chains

## Error Handling

| Issue | Action |
|-------|--------|
| File read fails | Log to FAILURES_LOG, set resume point |
| Registry corrupt | Attempt recovery from backup, fail if impossible |
| JIRA regeneration fails | Mark as partial, flag for manual review |
| Traceability broken | Log gaps, continue, flag for validation |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: ProductSpecs Skills Framework v1.0
