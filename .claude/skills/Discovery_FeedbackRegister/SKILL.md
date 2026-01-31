---
name: registering-discovery-feedback
description: Use when you need to log feedback to the central registry, assign unique IDs, and manage feedback lifecycle status.
model: haiku
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill registering-discovery-feedback started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill registering-discovery-feedback ended '{"stage": "discovery"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill registering-discovery-feedback instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

---

# Register Discovery Feedback

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_FeedbackRegister
- **Version**: 1.1.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Milos Cigoj
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation
  - v1.1.0 (2025-12-22): Added explicit Statistics Calculation section - counts based on lifecycle fields (approved_at, implemented_at) not just current status

## Description
Manages the central feedback registry (`discover_feedback_register.json`). Assigns unique sequential IDs, tracks metadata (source, inputter, timestamps), and maintains lifecycle status for each feedback item.

**Role**: You are a Feedback Registry Manager. Your expertise is maintaining a reliable audit trail of all feedback items with complete metadata and status tracking.

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
- output files created (feedback registry)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "registering-discovery-feedback"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "registering-discovery-feedback" --stage discovery
```

Logging is handled automatically by the skill framework. No user action required.

---

## Trigger Conditions

- New feedback needs to be logged
- Feedback status needs to be updated
- Request mentions "register feedback", "log feedback", "update feedback status"

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Feedback Content | Yes | Raw feedback text or summary |
| Source Person | Yes | Who provided the feedback |
| Inputter Person | Yes | Who is entering the feedback |
| Impact Analysis | Yes | Output from Discovery_FeedbackAnalyzer |
| Category | Yes | Primary impact category |
| Priority | No | P0/P1/P2 (default: P1) |

## Registry Schema

### Feedback Item Structure

```json
{
  "id": "FB-001",
  "external_id": null,
  "status": "pending",
  "metadata": {
    "source_person": "John Doe",
    "inputter_person": "Jane Smith",
    "received_at": "2025-12-22T14:30:00Z",
    "logged_at": "2025-12-22T14:35:00Z",
    "last_updated": "2025-12-22T14:35:00Z"
  },
  "content": {
    "summary": "Brief summary of feedback",
    "full_text": "Complete feedback content...",
    "source_file": null
  },
  "classification": {
    "category": "CAT-PER",
    "priority": "P1",
    "effort_estimate": "M",
    "confidence": "High"
  },
  "impact": {
    "files_affected": 5,
    "high_impact_count": 2,
    "traceability_ids": ["PP-001", "JTBD-2.1"],
    "priority_score": 18
  },
  "lifecycle": {
    "approved_at": null,
    "approved_by": null,
    "rejected_at": null,
    "rejected_by": null,
    "rejection_reason": null,
    "implemented_at": null,
    "validated_at": null
  },
  "session_folder": "2025-12-22_Feedback_001",
  "plan_file": null,
  "implementation_log": null
}
```

### Status Values

| Status | Description |
|--------|-------------|
| `pending` | Feedback logged, awaiting approval decision |
| `approved` | User approved for implementation |
| `rejected` | User rejected, no implementation |
| `in_progress` | Implementation underway |
| `implemented` | Changes applied successfully |
| `validated` | Implementation verified against plan |
| `failed` | Implementation failed (partial) |
| `resumed` | Previously failed, now resumed |

## Operations

### 1. Register New Feedback

```
ACTION: register
INPUT:
  - feedback_content: string
  - source_person: string
  - inputter_person: string
  - impact_analysis: object
  - category: string
  - priority: string (optional)
OUTPUT:
  - feedback_id: FB-<NNN>
  - session_folder: <YYYY-MM-DD>_Feedback_<NNN>
```

**Steps**:
1. Read current registry from `traceability/feedback_sessions/discovery/discover_feedback_register.json`
2. Get `next_id` and format as `FB-<NNN>` (zero-padded to 3 digits)
3. Create session folder: `traceability/feedback_sessions/discovery/<YYYY-MM-DD>_Feedback_<NNN>/`
4. Build feedback item object
5. Append to `feedback_items` array
6. Increment `next_id`
7. Update `statistics` (see Statistics Calculation section - count based on lifecycle fields, not just status)
8. Update `$metadata.updated_at` and `$metadata.change_history`
9. Write registry back

### 2. Update Status

```
ACTION: update_status
INPUT:
  - feedback_id: string
  - new_status: string
  - actor: string (optional)
  - reason: string (optional)
OUTPUT:
  - success: boolean
```

**Steps**:
1. Read registry
2. Find feedback item by ID
3. Update `status` field
4. Update relevant `lifecycle` fields based on status
5. Update `metadata.last_updated`
6. Update statistics (see Statistics Calculation below)
7. Write registry back

## Statistics Calculation

**IMPORTANT**: Statistics track cumulative lifecycle states, not just current status.

### Calculation Rules

```
For each feedback item, check lifecycle fields:

approved = count where lifecycle.approved_at IS NOT NULL
rejected = count where lifecycle.rejected_at IS NOT NULL
pending = count where status == "pending"
implemented = count where lifecycle.implemented_at IS NOT NULL
failed = count where status == "failed"
```

### Key Principle

A feedback that progresses through approval → implementation should be counted in BOTH `approved` AND `implemented` because:
- It WAS approved (lifecycle.approved_at is set)
- It WAS implemented (lifecycle.implemented_at is set)

### Example

| Feedback | Status | approved_at | implemented_at | Counts Toward |
|----------|--------|-------------|----------------|---------------|
| FB-001 | implemented | 2025-12-22 | 2025-12-22 | approved=1, implemented=1 |
| FB-002 | approved | 2025-12-22 | null | approved=1 |
| FB-003 | pending | null | null | pending=1 |
| FB-004 | rejected | null | null | rejected=1 |

**Result**: `approved: 2, rejected: 1, pending: 1, implemented: 1`

### Implementation Code Pattern

```javascript
// Calculate statistics from feedback_items array
const stats = {
  total_feedbacks: items.length,
  approved: items.filter(i => i.lifecycle.approved_at !== null).length,
  rejected: items.filter(i => i.lifecycle.rejected_at !== null).length,
  pending: items.filter(i => i.status === "pending").length,
  implemented: items.filter(i => i.lifecycle.implemented_at !== null).length,
  failed: items.filter(i => i.status === "failed").length
};
```

### 3. Link Plan File

```
ACTION: link_plan
INPUT:
  - feedback_id: string
  - plan_file_path: string
OUTPUT:
  - success: boolean
```

### 4. Link Implementation Log

```
ACTION: link_implementation
INPUT:
  - feedback_id: string
  - log_file_path: string
OUTPUT:
  - success: boolean
```

## Session Folder Structure

Each feedback creates:

```
traceability/feedback_sessions/discovery/<YYYY-MM-DD>_Feedback_<NNN>/
├── FEEDBACK_ORIGINAL.md          # Original feedback content
├── IMPACT_ANALYSIS.md            # From Discovery_FeedbackAnalyzer
├── IMPLEMENTATION_PLAN.md        # From Discovery_FeedbackPlanner
├── IMPLEMENTATION_LOG.md         # From Discovery_FeedbackImplementer
├── VALIDATION_REPORT.md          # From Discovery_FeedbackValidator
└── FEEDBACK_SUMMARY.md           # Final summary
```

## Output Format

### Registry Update Log Entry

When modifying the registry, add to change_history:

```json
{
  "version": "<incremented>",
  "date": "<YYYY-MM-DD>",
  "author": "Discovery_FeedbackRegister",
  "changes": "Registered FB-<NNN>: <summary>"
}
```

## Integration Points

### Receives From
- `Discovery_FeedbackAnalyzer` - Impact analysis data
- `/discovery-feedback` command - Metadata inputs

### Feeds Into
- `Discovery_FeedbackPlanner` - Feedback details for planning
- `Discovery_FeedbackImplementer` - Status updates
- `Discovery_FeedbackValidator` - Status updates

## Error Handling

| Issue | Action |
|-------|--------|
| Registry file missing | Initialize new registry with default structure |
| Duplicate feedback detected | Warn user, offer to link or create new |
| Invalid status transition | Reject update, log warning |
| Session folder exists | Append suffix (e.g., _a, _b) |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: Discovery Skills Framework v2.0
