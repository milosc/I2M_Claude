---
name: implementing-discovery-feedback
description: Use when you need to apply approved implementation plans to discovery artifacts with full traceability and version control.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill implementing-discovery-feedback started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill implementing-discovery-feedback ended '{"stage": "discovery"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill implementing-discovery-feedback instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

---

# Implement Discovery Feedback

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_FeedbackImplementer
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Milos Cigoj
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description
Executes approved implementation plans, modifying discovery artifacts with full traceability. Maintains detailed logs of all changes, updates version metadata, and handles partial failures with resume capability.

**Role**: You are a Feedback Implementation Specialist. Your expertise is executing precise, traceable changes to discovery artifacts while maintaining data integrity and full audit trails.

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
- output files created (implementation artifacts)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "implementing-discovery-feedback"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "implementing-discovery-feedback" --stage discovery
```

Logging is handled automatically by the skill framework. No user action required.

---

## Trigger Conditions

- Implementation plan has been approved
- Request mentions "implement feedback", "apply changes", "execute plan"
- Feedback status is `approved` with confirmed plan

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Feedback ID | Yes | FB-<NNN> identifier |
| Implementation Plan | Yes | Confirmed IMPLEMENTATION_PLAN.md |
| Discovery Path | Yes | ClientAnalysis_<SystemName> path |
| Resume From | No | Step number to resume from (for partial failures) |

## Implementation Protocol

### 1. Pre-Implementation Checks

Before any changes:

```
CHECK 1: Plan file exists and is confirmed
CHECK 2: All target files are readable
CHECK 3: Traceability registry is accessible
CHECK 4: No conflicting implementations in progress
```

### 2. Change Execution Order

Execute changes in dependency order:

```
1. Upstream files first (Analysis, Pain Points)
2. Research files (Personas, JTBD)
3. Strategy files (Vision, Strategy, Roadmap, KPIs)
4. Design spec files (Screens, Navigation, Data)
5. Documentation files (Index, README)
6. Traceability registries (JSON files)
```

### 3. Single File Change Protocol

For each file modification:

```
STEP 1: Read current file
STEP 2: Parse YAML frontmatter (if exists)
STEP 3: Extract current version
STEP 4: Calculate new version:
        - MAJOR: Structure changed
        - MINOR: Content added
        - PATCH: Content modified/fixed
STEP 5: Apply changes to content
STEP 6: Update frontmatter:
        - version: <new_version>
        - updated_at: <now>
        - Add change_history entry with:
          - version: <new_version>
          - date: <today>
          - author: "Discovery_FeedbackImplementer"
          - changes: "FB-<NNN>: <description>"
STEP 7: Write file
STEP 8: Log success to implementation log
```

### 4. Traceability Updates

For each affected traceability ID:

```
1. Update relevant registry (JSON)
2. Add feedback reference to item
3. Update trace_links.json if relationships changed
4. Record in implementation log
```

### 5. Partial Failure Handling

On any error:

```
1. Log failure with step number and error
2. Mark feedback status as "failed"
3. Save resume point to implementation log
4. Continue with remaining independent steps (if any)
5. Report partial completion status
```

## Output Format

### Primary Output: `IMPLEMENTATION_LOG.md` (in feedback session folder)

```markdown
---
document_id: FB-IMPL-<ID>
version: 1.0.0
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
generated_by: Discovery_FeedbackImplementer
source_files:
  - IMPLEMENTATION_PLAN.md
change_history:
  - version: "1.0.0"
    date: "<YYYY-MM-DD>"
    author: "Discovery_FeedbackImplementer"
    changes: "Implementation execution"
---

# Implementation Log

## Feedback Reference
- **ID**: FB-<NNN>
- **Plan**: [Plan A/B/Custom]
- **Started**: <YYYY-MM-DD HH:MM>
- **Completed**: <YYYY-MM-DD HH:MM> or "In Progress" or "Failed at Step N"

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

### Step 1: [Step Title]
**Status**: COMPLETED / FAILED / SKIPPED
**Target**: [file path]
**Action**: [Add/Modify/Delete]
**Timestamp**: <YYYY-MM-DD HH:MM:SS>

**Changes Applied**:
```diff
- [removed content]
+ [added content]
```

**Version Update**: [X.Y.Z] -> [X.Y+1.Z]

**Traceability**:
- Updated: [IDs]
- Linked to: FB-<NNN>

---

### Step 2: [Step Title]
...

---

## Version Changes Summary

| File | Before | After | Change Type | Reason |
|------|--------|-------|-------------|--------|
| [path] | [version] | [version] | Minor | FB-<NNN>: [reason] |

---

## Traceability Updates

### Registry Updates

| Registry | Items Updated | IDs |
|----------|---------------|-----|
| pain_point_registry.json | N | PP-001, PP-002 |
| jtbd_registry.json | N | JTBD-1.1 |

### New Links Created

| Source | Target | Type |
|--------|--------|------|
| [ID] | [ID] | [type] |

---

## Failure Log (if any)

### Step [N] Failure

**Error**: [error message]
**File**: [file path]
**Resume Command**: `/discovery-feedback resume FB-<NNN> --from-step N`

---

## Post-Implementation Actions

- [ ] Discovery_Validate: [Pending/Passed/Failed]
- [ ] Discovery_Traceability Rebuild: [Pending/Passed/Failed]
- [ ] Feedback Status Updated: [Yes/No]

---

## Final Status

**Implementation**: COMPLETE / PARTIAL (N/M steps) / FAILED

**Next Steps**:
- [If complete]: Proceed to validation
- [If partial]: Resume from step N
- [If failed]: Review error and retry
```

## Resume Protocol

When resuming from failure:

```
1. Read implementation log
2. Find last successful step
3. Verify file states match expected
4. Continue from resume point
5. Update log with resume marker
```

## Integration Points

### Receives From
- `Discovery_FeedbackPlanner` - Confirmed implementation plan
- `Discovery_FeedbackRegister` - Feedback details and status

### Feeds Into
- `Discovery_FeedbackValidator` - Implementation log for validation
- `Discovery_FeedbackRegister` - Status updates
- `Discovery_Validate` - Re-run after implementation
- `Traceability_Manager` - Registry updates

## Error Handling

| Issue | Action |
|-------|--------|
| File not found | Log as FAILED, continue with next step |
| Permission denied | Log as FAILED, report to user |
| Invalid version format | Create new frontmatter, log warning |
| Registry corruption | Backup, attempt repair, or skip |
| Conflict detected | Stop, ask user for resolution |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: Discovery Skills Framework v2.0
