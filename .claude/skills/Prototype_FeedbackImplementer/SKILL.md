---
name: implementing-prototype-feedback
description: Use when you need to execute approved implementation plans for prototype feedback with full traceability, version control, and resumption capability.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill implementing-prototype-feedback started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill implementing-prototype-feedback ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill implementing-prototype-feedback instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

# Implement Prototype Feedback

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_FeedbackImplementer
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Claude Code
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description

Executes approved implementation plans, modifying Discovery materials, Prototype specifications, and prototype code with full traceability. Maintains detailed logs, updates version metadata, and handles partial failures with resume capability.

**Role**: You are an Implementation Executor. Your expertise is executing precise, traceable changes across documentation, specifications, and code while maintaining data integrity and full audit trails.

> **INTEGRATES**: executing-plans skill for controlled batch execution
> **INTEGRATES**: verification-before-completion skill for verification

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
- output files created (implementation results)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "implementing-prototype-feedback"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "implementing-prototype-feedback" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## Trigger Conditions

- Implementation plan has been confirmed
- Feedback status is "approved" with selected plan
- Resume request for failed/partial implementation

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Feedback ID | Yes | PF-NNN identifier |
| Implementation Plan | Yes | Confirmed implementation_plan.md |
| Prototype Path | Yes | `Prototype_<SystemName>` path |
| Discovery Path | Conditional | `ClientAnalysis_<SystemName>` if upstream changes |
| Resume From | No | Step number to resume from |

## Implementation Protocol

### Phase 1: Pre-Implementation Checks

```
VALIDATE:
  1. Plan file exists and is confirmed
  2. Feedback status == "approved"
  3. All target files are accessible
  4. No conflicting implementations in progress
  5. Traceability registries accessible

IF feedback.type == "Bug":
  VERIFY debugging_evidence exists
  VERIFY root_cause is documented

IF any check fails:
  BLOCK with specific error message

LOG: "Pre-implementation validation passed"
```

### Phase 2: Create Backup

```
backup_id = "BK-PF-{feedback_id}-{timestamp}"
backup_path = "Prototype_<SystemName>/_backups/{backup_id}/"

CREATE backup:
  COPY:
    - _state/ → backup_path/_state/
    - Prototype_<SystemName>/01-components/ → backup_path/01-components/
    - Prototype_<SystemName>/02-screens/ → backup_path/02-screens/
    - Prototype_<SystemName>/prototype/src/ → backup_path/prototype-src/
    - ClientAnalysis_<SystemName>/ → backup_path/discovery/ (if upstream changes)

RECORD backup in session folder:
  {
    backup_id: backup_id,
    feedback_id: feedback_id,
    created_at: timestamp,
    files_backed_up: count
  }

LOG: "Backup created: {backup_id}"
DISPLAY: "Rollback available via: rollback to {backup_id}"
```

### Phase 3: Update Status

```
UPDATE feedback registry:
  status: "in_progress"
  lifecycle.implementation_started_at: NOW()

UPDATE _state/prototype_feedback_state.json:
  active_feedback.status: "in_progress"
  active_feedback.current_phase: 6

LOG: "Implementation started for PF-{id}"
```

### Phase 4: Execute Changes (Dependency Order)

> **CRITICAL**: Execution MUST follow the COMPREHENSIVE ORDER below. Skipping layers = incomplete implementation.

## MANDATORY COMPREHENSIVE EXECUTION ORDER

```
════════════════════════════════════════════════════════════════
 LAYER 1: DISCOVERY (ClientAnalysis_*) - UPSTREAM FIRST
════════════════════════════════════════════════════════════════

Step 1.1: screen-definitions.md
  IF new/modified screen:
    - Add screen entry with ID, name, priority, platform
    - Define zones (A, B, C, etc.) with components
    - List data requirements
    - Document states and transitions

Step 1.2: navigation-structure.md
  IF navigation affected:
    - Add screen to navigation hierarchy
    - Update flow diagrams
    - Define entry/exit points

Step 1.3: data-fields.md
  IF new data fields:
    - Add field definitions with types
    - Define validation rules
    - Document relationships

Step 1.4: interaction-patterns.md
  IF new interaction patterns:
    - Document interaction sequences
    - Define feedback states
    - Specify timing requirements

Step 1.5: JOBS_TO_BE_DONE.md
  IF new feature:
    - Link to relevant JTBD
    - Update acceptance criteria if needed

════════════════════════════════════════════════════════════════
 LAYER 2: PROTOTYPE SPECIFICATIONS (Prototype_*)
════════════════════════════════════════════════════════════════

Step 2.1: 04-implementation/data-model.md
  IF data model affected:
    - Add entity schema
    - Define relationships
    - Document constraints

Step 2.2: 04-implementation/api-contracts.json
  IF API affected:
    - Add endpoint specification
    - Define request/response schemas
    - Document error responses

Step 2.3: 04-implementation/test-data/
  IF test data needed:
    - Create {entity}.json with realistic test data
    - Ensure data covers all scenarios
    - Follow existing patterns

Step 2.4: 01-components/component-index.md
  IF new component:
    - Add component to index
    - Categorize appropriately

Step 2.5: 01-components/{category}/{component}/spec.md
  IF new component:
    - Create full specification
    - Define props, states, variants
    - Document accessibility

Step 2.6: 02-screens/screen-index.md
  IF new/modified screen:
    - Add screen to index
    - Set priority and platform

Step 2.7: 02-screens/{platform}/{screen}/spec.md
  IF new/modified screen:
    - Create full screen specification
    - Define zones and components
    - Document interactions

Step 2.8: 03-interactions/motion-system.md
  IF motion affected:
    - Add motion specifications
    - Define timing and easing

Step 2.9: 03-interactions/accessibility-spec.md
  IF accessibility affected:
    - Add a11y requirements
    - Define keyboard navigation
    - Document ARIA labels

Step 2.10: 03-interactions/responsive-behavior.md
  IF responsive affected:
    - Define breakpoints
    - Document layout changes

════════════════════════════════════════════════════════════════
 LAYER 3: CODE (prototype/src/)
════════════════════════════════════════════════════════════════

Step 3.1: src/components/{Component}.tsx
  IF new component:
    - Implement component
    - Follow existing patterns
    - Include TypeScript types

Step 3.2: src/screens/{platform}/{Screen}.tsx
  IF new screen:
    - Implement screen component
    - Import required components
    - Connect to data/context

Step 3.3: src/App.tsx
  IF routing affected:
    - Add route definition
    - Update navigation logic

Step 3.4: src/data/{entity}.json
  IF mock data needed:
    - Add mock data file
    - Use realistic test data
    - NOTE: This is DIFFERENT from test-data/ in specs

Step 3.5: src/contexts/{Context}.tsx
  IF context needed:
    - Create/update context
    - Implement state management

════════════════════════════════════════════════════════════════
 LAYER 4: REGISTRIES (ROOT LEVEL) - ALWAYS REQUIRED
════════════════════════════════════════════════════════════════

Step 4.1: traceability/screen_registry.json (ALWAYS FOR SCREEN CHANGES)
  - Add entry to discovery_screens[] with:
    - id: "S-XX" or "M-XX" or "D-XX"
    - name, priority, phase, platform, category
    - requirements[], jtbd_refs[]
    - feedback_source: "PF-XXX"
    - added_via: "Prototype Feedback"
    - added_at: "{date}"
  - Add entry to traceability[] with:
    - screen_id, screen_name, discovery_ref
    - spec_status, spec_path
    - code_status, code_path
    - test_status, test_path
    - feedback_source: "PF-XXX"
  - Update screen_coverage statistics

Step 4.2: traceability/prototype_traceability_register.json (ALWAYS)
  - Add to screen_traceability.screens[] with:
    - id, name, priority, platform
    - spec_status, spec_path
    - code_status, code_path
    - test_status, test_path
    - feedback_source: "PF-XXX"
    - added_via: "Prototype Feedback"
  - Update coverage counts

Step 4.3: traceability/discovery_traceability_register.json
  IF discovery changed:
    - Update relevant entries
    - Add feedback references

Step 4.4: _state/requirements_registry.json
  IF requirements affected:
    - Add/update requirement entries

════════════════════════════════════════════════════════════════
 LAYER 5: TRACEABILITY MATRICES (helperFiles/)
════════════════════════════════════════════════════════════════

Step 5.1: helperFiles/TRACEABILITY_MATRIX_MASTER.md
  IF new trace chains:
    - Add trace chain from Client Fact → Pain Point → JTBD → Requirement → Screen → Test
    - Update coverage table

Step 5.2: helperFiles/TRACEABILITY_ASSESSMENT_REPORT.md
  IF coverage metrics changed:
    - Update coverage percentages
    - Add new items to inventory
    - Update assessment summary

════════════════════════════════════════════════════════════════
```

## LEGACY EXECUTION ORDER (for reference)

```
EXECUTION_ORDER:
  1. Discovery files (if affected)
  2. Data model / API contracts
  3. Design tokens / styles
  4. Component specifications
  5. Screen specifications
  6. Component code
  7. Page code
  8. Test data
  9. Traceability registries

FOR each step in implementation_plan.steps:

  LOG: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  LOG: "Step {N}/{total}: {action}"
  LOG: "Target: {file_path}"
  LOG: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  # Update resume point BEFORE attempting
  SET_RESUME_POINT(feedback_id, step.number, step.target, step.action)

  TRY:
    EXECUTE_STEP(step)
    LOG_STEP_SUCCESS(step)
    UPDATE step.status = "completed"
    UPDATE step.completed_at = NOW()

  CATCH error:
    LOG_STEP_FAILURE(step, error)
    UPDATE step.status = "failed"
    UPDATE step.error = error.message

    # Continue with independent steps if possible
    IF step.blocking:
      BREAK  # Stop execution
    ELSE:
      CONTINUE  # Try next step

  DISPLAY: "✓ Step {N}/{total} complete: {action}"
```

### Phase 5: Single File Change Protocol

```
FUNCTION EXECUTE_STEP(step):

  SWITCH step.type:

    CASE "discovery":
      file_path = "ClientAnalysis_<SystemName>/{step.target}"
      APPLY_CHANGE_WITH_VERSION(file_path, step.changes)

    CASE "spec":
      file_path = "Prototype_<SystemName>/{step.target}"
      APPLY_CHANGE_WITH_VERSION(file_path, step.changes)

    CASE "code":
      file_path = "Prototype_<SystemName>/prototype/{step.target}"
      APPLY_CODE_CHANGE(file_path, step.changes)

    CASE "data":
      file_path = "Prototype_<SystemName>/04-implementation/{step.target}"
      APPLY_CHANGE_WITH_VERSION(file_path, step.changes)

    CASE "registry":
      APPLY_REGISTRY_UPDATE(step.target, step.changes)
```

### Phase 6: Version Update Protocol

```
FUNCTION APPLY_CHANGE_WITH_VERSION(file_path, changes):

  # Step 1: Read current file
  content = READ(file_path)

  # Step 2: Parse version metadata
  IF file_path.endsWith(".md"):
    metadata = PARSE_YAML_FRONTMATTER(content)
  ELSE IF file_path.endsWith(".json"):
    metadata = content.$metadata

  # Step 3: Calculate new version
  current_version = metadata.version OR "1.0.0"
  [major, minor, patch] = current_version.split(".")

  IF changes.type == "structure":
    new_version = "{major+1}.0.0"
  ELSE IF changes.type == "content_added":
    new_version = "{major}.{minor+1}.0"
  ELSE:  # content_modified
    new_version = "{major}.{minor}.{patch+1}"

  # Step 4: Apply changes
  new_content = APPLY_CHANGES(content, changes.modifications)

  # Step 5: Update metadata
  metadata.version = new_version
  metadata.updated_at = TODAY()
  metadata.change_history.push({
    version: new_version,
    date: TODAY(),
    author: "Prototype_FeedbackImplementer",
    changes: "PF-{feedback_id}: {changes.description}"
  })

  # Step 6: Write file
  IF file_path.endsWith(".md"):
    new_content = REBUILD_WITH_FRONTMATTER(new_content, metadata)
  ELSE IF file_path.endsWith(".json"):
    new_content.$metadata = metadata

  WRITE(file_path, new_content)

  # Step 7: Log to implementation log
  LOG_CHANGE(file_path, current_version, new_version, changes)

  RETURN { success: true, old_version: current_version, new_version: new_version }
```

### Phase 7: Code Change Protocol

```
FUNCTION APPLY_CODE_CHANGE(file_path, changes):

  # Code files don't have YAML frontmatter
  # Track changes in implementation log only

  content = READ(file_path)

  # Apply code modifications
  new_content = APPLY_CODE_MODIFICATIONS(content, changes.modifications)

  WRITE(file_path, new_content)

  # Log the diff
  LOG_CODE_DIFF(file_path, content, new_content)

  RETURN { success: true }
```

### Phase 8: Traceability Update Protocol

```
FUNCTION APPLY_REGISTRY_UPDATE(registry_name, changes):

  registry_path = "traceability/{registry_name}"
  registry = READ_JSON(registry_path)

  FOR each update in changes:
    IF update.action == "add_reference":
      item = FIND(registry, update.item_id)
      item.feedback_refs.push("PF-{feedback_id}")

    IF update.action == "update_status":
      item = FIND(registry, update.item_id)
      item.status = update.new_status

    IF update.action == "add_link":
      registry.trace_links.push({
        source: update.source,
        target: update.target,
        type: "feedback_change",
        feedback_id: "PF-{feedback_id}"
      })

  registry.$metadata.updated_at = NOW()
  WRITE_JSON(registry_path, registry)

  LOG: "Updated traceability: {registry_name}"
```

### Phase 9: Failure Handling

```
IF any step failed:

  # Determine failure severity
  failed_steps = steps.filter(s => s.status == "failed")
  completed_steps = steps.filter(s => s.status == "completed")

  IF failed_steps includes blocking step:
    implementation_status = "failed"
  ELSE:
    implementation_status = "partial"

  # Update registry
  UPDATE feedback registry:
    status: "failed"
    resume_point: {
      step_number: first_failed_step.number,
      file_path: first_failed_step.target,
      action: first_failed_step.action,
      timestamp: NOW()
    }

  # Display failure report
  ════════════════════════════════════════════
   IMPLEMENTATION {FAILED|PARTIAL}
  ════════════════════════════════════════════

  Completed: {completed_steps.length}/{total} steps
  Failed: {failed_steps.length} steps

  Failed Steps:
  {FOR each failed_step:}
  • Step {N}: {action}
    Error: {error_message}
    File: {target}

  Resume Command:
  /prototype-feedback resume PF-{id}

  Or Rollback:
  rollback to {backup_id}
  ════════════════════════════════════════════
```

### Phase 10: Generate Implementation Log

```
CREATE implementation_log.md in session folder:

---
document_id: PF-IMPL-{ID}
version: 1.0.0
created_at: {date}
updated_at: {date}
generated_by: Prototype_FeedbackImplementer
source_files:
  - implementation_plan.md
change_history:
  - version: "1.0.0"
    date: "{date}"
    author: "Prototype_FeedbackImplementer"
    changes: "Implementation execution"
---

# Implementation Log

## Feedback Reference
- **ID**: PF-{id}
- **Plan**: Option {X}
- **Started**: {timestamp}
- **Completed**: {timestamp} OR "In Progress" OR "Failed at Step N"

---

## Execution Summary

| Status | Count |
|--------|-------|
| Steps Completed | N |
| Steps Failed | N |
| Steps Skipped | N |
| Files Modified | N |
| Registries Updated | N |

---

## Step-by-Step Log

### Step 1: {action}
**Status**: COMPLETED
**Target**: {file_path}
**Action**: {create|modify|delete}
**Timestamp**: {time}

**Changes Applied**:
```diff
- {removed content}
+ {added content}
```

**Version Update**: 1.0.0 → 1.1.0

**Traceability**:
- Updated: {IDs}
- Linked to: PF-{id}

---

### Step 2: {action}
...

---

## Version Changes Summary

| File | Before | After | Change Type | Reason |
|------|--------|-------|-------------|--------|
| {path} | 1.0.0 | 1.1.0 | Minor | PF-{id}: {reason} |

---

## Traceability Updates

### Registry Updates
| Registry | Items Updated | IDs |
|----------|---------------|-----|
| prototype_traceability_register.json | N | SCR-001, COMP-Button |

### New Links Created
| Source | Target | Type |
|--------|--------|------|
| PF-{id} | SCR-001 | feedback_change |

---

## Failure Log (if any)

### Step {N} Failure
**Error**: {error_message}
**File**: {file_path}
**Resume Command**: `/prototype-feedback resume PF-{id}`

---

## Final Status

**Implementation**: COMPLETE | PARTIAL | FAILED

**Next Steps**:
- [If complete]: Proceed to validation
- [If partial]: Resume from step N
- [If failed]: Review error and retry
```

## Resume Protocol

```
WHEN resuming from failure:

  # Read state
  READ _state/prototype_feedback_state.json
  feedback = GET_FEEDBACK(active_feedback.id)
  resume_point = feedback.resume_point

  # Verify file states
  FOR each completed_step:
    VERIFY file exists and has expected version

  IF verification fails:
    WARN: "State mismatch detected"
    PROMPT: "Continue anyway or rollback?"

  # Add resume marker to log
  APPEND to implementation_log.md:
    ---

    ## [RESUMED]
    **Resumed At**: {timestamp}
    **From Step**: {resume_point.step_number}
    **Reason**: Previous session interrupted

    ---

  # Continue from resume point
  FOR step in plan.steps WHERE step.number >= resume_point.step_number:
    EXECUTE_STEP(step)
```

## Output Files

### Files Created/Modified

| File | Location | Purpose |
|------|----------|---------|
| implementation_log.md | Session folder | Detailed execution log |
| files_changed.md | Session folder | Summary of all changes |
| Various specs | Prototype folders | Updated specifications |
| Various code | prototype/src/ | Updated code files |

## Integration Points

### Receives From
- `Prototype_FeedbackPlanner` - Confirmed implementation plan
- `Prototype_FeedbackRegister` - Feedback details, resume point

### Feeds Into
- `Prototype_FeedbackValidator` - Implementation log for validation
- `Prototype_FeedbackRegister` - Status updates, resume points
- Traceability registries - Change references

### Uses Skills
- `executing-plans` - Controlled batch execution
- `verification-before-completion` - Step verification

## Error Handling

| Issue | Action |
|-------|--------|
| File not found | Log as FAILED, continue if non-blocking |
| Permission denied | Log as FAILED, report to user |
| Invalid version format | Create new metadata, log warning |
| Registry corruption | Backup, attempt repair, or skip |
| Conflict detected | Stop, ask user for resolution |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: Prototype Skills Framework v2.3
