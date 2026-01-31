---
name: implementing-solarch-feedback
description: Use when you need to execute approved implementation plans for Solution Architecture feedback with full traceability and version control.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill implementing-solarch-feedback started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill implementing-solarch-feedback ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill implementing-solarch-feedback instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

---

# SolArch_FeedbackImplementer

Change execution for Solution Architecture feedback with version tracking.

## Purpose

Executes approved implementation plans for Solution Architecture feedback, making controlled changes to ADRs, components, diagrams, and registries with full version tracking and resume capability.

---

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
- output files created (implementation logs and modified artifacts)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "implementing-solarch-feedback"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "implementing-solarch-feedback" --stage solarch
```

Logging is handled automatically by the skill framework. No user action required.

---

## When to Use

- After implementation plan is approved
- To execute changes across architecture files
- To update registries with new versions
- To resume interrupted implementations

## Input Requirements

```json
{
  "feedback_id": "SF-001",
  "system_name": "InventorySystem",
  "implementation_plan": {
    "option_selected": "A",
    "steps": [
      {
        "step_number": 1,
        "file": "09-decisions/ADR-001-architecture-style.md",
        "action": "modify",
        "sections": ["Context", "Decision", "Consequences"],
        "changes": { ... }
      }
    ]
  }
}
```

## Output Files

### Implementation Log

Location: `SolArch_<SystemName>/feedback-sessions/<session>/implementation_log.md`

```markdown
---
feedback_id: SF-001
started_at: 2025-12-22T11:00:00Z
plan_selected: Option A
total_steps: 5
---

# Implementation Log

## Summary

| Metric | Value |
|--------|-------|
| Steps Total | 5 |
| Steps Completed | 5 |
| Steps Failed | 0 |
| Files Changed | 3 |

## Execution Log

### Step 1: Modify ADR-001

**File**: `09-decisions/ADR-001-architecture-style.md`
**Action**: modify
**Status**: ✅ Completed
**Timestamp**: 2025-12-22T11:01:00Z

**Changes Made**:
- Context section: Added scaling analysis (lines 25-40)
- Decision section: Added future evolution path (lines 55-70)
- Consequences section: Expanded negative impacts (lines 85-95)

**Version**: 1.0.0 → 1.1.0

**Backup**: ADR-001-architecture-style.md.backup

---

### Step 2: Update Registry

**File**: `_registry/decisions.json`
**Action**: update
**Status**: ✅ Completed
**Timestamp**: 2025-12-22T11:02:00Z

**Changes Made**:
- ADR-001 version: "1.0.0" → "1.1.0"
- ADR-001 modified_at: updated to current timestamp

---

### Step 3: Review solution-strategy.md

**File**: `04-solution-strategy/solution-strategy.md`
**Action**: review
**Status**: ✅ Completed (no changes needed)
**Timestamp**: 2025-12-22T11:03:00Z

**Notes**: Content aligned with ADR changes, no modifications required.

---

## Final Status

All steps completed successfully.

Next: Validation phase
```

### Files Changed Summary

Location: `SolArch_<SystemName>/feedback-sessions/<session>/files_changed.md`

```markdown
---
feedback_id: SF-001
implementation_timestamp: 2025-12-22T11:05:00Z
---

# Files Changed

## Summary

| Category | Files Changed |
|----------|---------------|
| ADRs | 1 |
| Registries | 1 |
| Other | 0 |
| **Total** | 2 |

## Changed Files

### 1. ADR-001-architecture-style.md

**Path**: `SolArch_InventorySystem/09-decisions/ADR-001-architecture-style.md`

**Version Change**: 1.0.0 → 1.1.0

**Sections Modified**:
| Section | Change Type | Lines |
|---------|-------------|-------|
| Context | Enhanced | 25-40 |
| Decision | Enhanced | 55-70 |
| Consequences | Enhanced | 85-95 |

**Backup Location**: `ADR-001-architecture-style.md.backup`

### 2. decisions.json

**Path**: `SolArch_InventorySystem/_registry/decisions.json`

**Changes**:
- ADR-001.version: "1.1.0"
- ADR-001.modified_at: "2025-12-22T11:02:00Z"

## Traceability Updates

Updated in `_registry/architecture-traceability.json`:
- Chain PP-1.1 → ADR-001: verified
- Chain PP-2.1 → ADR-001: verified
- Chain REQ-001 → ADR-001: verified
```

## Procedures

### 1. Execute Implementation

```
PROCEDURE execute_implementation(feedback_id, system_name, plan):

  LOAD session context:
    session_path = get_session_path(feedback_id, system_name)
    READ impact_analysis.md

  INITIALIZE log:
    CREATE implementation_log.md header
    steps_completed = 0
    steps_failed = 0
    files_changed = []

  FOR each step IN plan.steps:
    LOG step start:
      "### Step {step.step_number}: {step.action} {step.file}"

    TRY:
      EXECUTE step:
        IF step.action == "modify":
          execute_modify(step)
        ELIF step.action == "update":
          execute_update(step)
        ELIF step.action == "review":
          execute_review(step)
        ELIF step.action == "create":
          execute_create(step)

      LOG step success:
        Status: ✅ Completed
        Timestamp: NOW()
        Changes: step.changes_made

      steps_completed += 1
      files_changed.append(step.file)

    CATCH error:
      LOG step failure:
        Status: ❌ Failed
        Error: error.message

      steps_failed += 1
      CONTINUE (skip and continue pattern)

  GENERATE files_changed.md

  UPDATE registry status:
    IF steps_failed == 0:
      status = "validating"
    ELSE:
      status = "implementing" (partial)

  RETURN {
    steps_completed,
    steps_failed,
    files_changed
  }
```

### 2. Execute Modify Action

```
PROCEDURE execute_modify(step):

  file_path = SolArch_{system_name}/{step.file}

  # Backup original
  COPY file_path → file_path.backup

  # Read current content
  content = READ file_path

  # Parse frontmatter
  frontmatter, body = parse_markdown(content)

  # Update version
  old_version = frontmatter.version OR "1.0.0"
  new_version = increment_version(old_version)
  frontmatter.version = new_version
  frontmatter.modified_at = NOW()

  # Apply section changes
  FOR each section IN step.sections:
    IF step.changes[section]:
      body = apply_section_change(body, section, step.changes[section])

  # Write updated file
  new_content = format_markdown(frontmatter, body)
  WRITE file_path, new_content

  # Record change
  step.changes_made = {
    version_change: "{old_version} → {new_version}",
    sections_modified: step.sections
  }
```

### 3. Execute Update Action (Registry)

```
PROCEDURE execute_update(step):

  file_path = SolArch_{system_name}/{step.file}

  # Read JSON
  data = READ_JSON file_path

  # Apply updates
  FOR each update IN step.updates:
    path = update.path  # e.g., "items[0].version"
    value = update.value
    set_json_path(data, path, value)

  # Update metadata
  data.updated_at = NOW()

  # Write updated file
  WRITE_JSON file_path, data

  step.changes_made = step.updates
```

### 4. Execute Review Action

```
PROCEDURE execute_review(step):

  file_path = SolArch_{system_name}/{step.file}

  content = READ file_path

  # Check for alignment issues
  issues = []
  FOR each check IN step.alignment_checks:
    IF NOT content CONTAINS check.expected:
      issues.append(check.description)

  IF issues.length == 0:
    step.changes_made = "No changes needed - content aligned"
  ELSE:
    # Flag for manual review
    step.changes_made = "Issues found: {issues}"
    step.requires_attention = true
```

### 5. Resume Implementation

```
PROCEDURE resume_implementation(feedback_id, system_name):

  session_path = get_session_path(feedback_id, system_name)

  # Read implementation log
  log = READ implementation_log.md

  # Find last completed step
  last_completed = parse_last_completed_step(log)

  # Load plan
  plan = READ implementation_plan.md

  # Filter remaining steps
  remaining_steps = plan.steps WHERE step_number > last_completed

  IF remaining_steps.length == 0:
    RETURN "Implementation already complete"

  # Continue from next step
  execute_implementation(feedback_id, system_name, {
    steps: remaining_steps
  }, append_to_log=true)
```

### 6. Update Traceability

```
PROCEDURE update_traceability(system_name, changed_files):

  # Load traceability register
  trace_path = SolArch_{system_name}/_registry/architecture-traceability.json
  trace = READ_JSON trace_path

  FOR each file IN changed_files:
    entity_id = extract_entity_id(file)  # e.g., ADR-001

    # Find chains involving this entity
    FOR each chain IN trace.chains:
      IF entity_id IN chain.nodes:
        chain.verified_at = NOW()
        chain.last_change = "Feedback {feedback_id}"

  # Update metadata
  trace.updated_at = NOW()

  WRITE_JSON trace_path, trace
```

## Version Incrementing

| Change Type | Version Increment | Example |
|-------------|-------------------|---------|
| Enhancement | Patch | 1.0.0 → 1.0.1 |
| Correction | Patch | 1.0.0 → 1.0.1 |
| Major change | Minor | 1.0.0 → 1.1.0 |
| Breaking change | Major | 1.0.0 → 2.0.0 |

## Action Types

| Action | Description | Creates Backup |
|--------|-------------|----------------|
| modify | Change file sections | Yes |
| update | Update registry/JSON | No |
| review | Check for alignment | No |
| create | Create new file | No |

## Error Handling

| Error | Action |
|-------|--------|
| File not found | Log error, skip step, continue |
| Parse error | Log error, skip step, continue |
| Write error | Log error, restore backup, continue |
| Version conflict | Log warning, force update |

## Integration Points

### Upstream
- Receives approved plan from `/solarch-feedback` command
- Uses impact analysis from `SolArch_FeedbackAnalyzer`

### Downstream
- Updates registry via JSON writes
- Triggers `SolArch_FeedbackValidator` on completion

## Quality Gates

```bash
# Validate implementation completeness
python3 .claude/hooks/solarch_quality_gates.py --validate-feedback SF-001 --dir SolArch_X/
```

## Templates

### Implementation Plan

```markdown
---
feedback_id: SF-001
plan_created_at: 2025-12-22T10:30:00Z
option_selected: A
---

# Implementation Plan

## Option A: Minimal Change

### Steps

1. **Modify ADR-001**
   - File: `09-decisions/ADR-001-architecture-style.md`
   - Sections: Context, Decision, Consequences
   - Changes: Enhance justification

2. **Update Registry**
   - File: `_registry/decisions.json`
   - Changes: Version, modified_at

3. **Review Strategy**
   - File: `04-solution-strategy/solution-strategy.md`
   - Action: Verify alignment

### Risk Assessment

- **Overall Risk**: Low
- **Rollback Available**: Yes (via backups)
```
