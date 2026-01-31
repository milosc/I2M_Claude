---
name: registering-prototype-feedback
description: Use when you need to register, track, and manage prototype feedback entries with unique IDs, status tracking, and session folder management.
model: haiku
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill registering-prototype-feedback started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill registering-prototype-feedback ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill registering-prototype-feedback instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

# Register Prototype Feedback

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_FeedbackRegister
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Claude Code
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description

Manages the prototype feedback registry, assigns unique IDs, creates session folders, and tracks feedback lifecycle. This skill is the central hub for feedback state management.

**Role**: You are a Feedback Registry Manager. Your expertise is maintaining accurate records, generating sequential IDs, and ensuring all feedback has proper tracking throughout its lifecycle.

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
- output files created (feedback registry updates)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "registering-prototype-feedback"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "registering-prototype-feedback" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## Trigger Conditions

- New feedback received for prototype
- Request to register, track, or query feedback status
- Resume request for existing feedback

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Prototype Path | Yes | `Prototype_<SystemName>` folder path |
| Feedback Content | Yes | Parsed feedback from analyzer |
| Impact Analysis | Yes | Results from Prototype_FeedbackAnalyzer |
| Metadata | Yes | Source person, inputter, timestamp |

## Registry Structure

### Registry Location

```
Prototype_<SystemName>/feedback-sessions/
├── prototype_feedback_registry.json    # Central registry
└── <yyyy-mm-dd>_PrototypeFeedback-<ID>/ # Session folders
```

### Registry Schema

```json
{
  "$metadata": {
    "schema_version": "1.0.0",
    "created_at": "2025-12-22T10:00:00Z",
    "updated_at": "2025-12-22T10:30:00Z",
    "generated_by": "Prototype_FeedbackRegister"
  },
  "statistics": {
    "total": 5,
    "by_status": {
      "pending": 1,
      "approved": 1,
      "in_progress": 0,
      "implemented": 2,
      "validated": 1,
      "rejected": 0,
      "failed": 0
    },
    "by_category": {
      "CAT-CODE": 3,
      "CAT-SCR": 4,
      "CAT-COMP": 2,
      "CAT-DISC": 1
    },
    "by_type": {
      "Bug": 2,
      "Enhancement": 2,
      "NewFeature": 1
    }
  },
  "feedback_items": []
}
```

### Feedback Entry Schema

```json
{
  "id": "PF-001",
  "status": "pending",
  "type": "Bug|Enhancement|NewFeature|UXIssue|VisualIssue",
  "source": {
    "person": "John Smith",
    "role": "Product Manager"
  },
  "inputter": {
    "person": "Jane Doe",
    "timestamp": "2025-12-22T09:00:00Z"
  },
  "category": ["CAT-CODE", "CAT-SCR"],
  "priority_score": 25,
  "severity": "Critical|High|Medium|Low",
  "title": "Short descriptive title",
  "description": "Full feedback description",
  "impact_summary": {
    "discovery_files": 0,
    "spec_files": 3,
    "code_files": 5,
    "total_files": 8
  },
  "affected_items": {
    "screens": ["SCR-001", "SCR-002"],
    "components": ["Button", "Modal"],
    "requirements": ["REQ-001"],
    "code_files": ["src/components/Button.tsx"]
  },
  "session_folder": "2025-12-22_PrototypeFeedback-001",
  "debugging_evidence": null,
  "selected_plan": null,
  "lifecycle": {
    "created_at": "2025-12-22T09:00:00Z",
    "approved_at": null,
    "approved_by": null,
    "plan_selected_at": null,
    "implementation_started_at": null,
    "implemented_at": null,
    "validated_at": null,
    "closed_at": null,
    "rejected_at": null,
    "rejected_by": null,
    "rejection_reason": null
  },
  "resume_point": null
}
```

## Procedure

### Phase 1: Initialize Registry

```
CHECK if registry exists:
  registry_path = "Prototype_<SystemName>/feedback-sessions/prototype_feedback_registry.json"

IF NOT exists:
  CREATE directory: "Prototype_<SystemName>/feedback-sessions/"

  CREATE registry = {
    "$metadata": {
      "schema_version": "1.0.0",
      "created_at": NOW(),
      "updated_at": NOW(),
      "generated_by": "Prototype_FeedbackRegister"
    },
    "statistics": {
      "total": 0,
      "by_status": {},
      "by_category": {},
      "by_type": {}
    },
    "feedback_items": []
  }

  WRITE to registry_path
  LOG: "Created new feedback registry"
```

### Phase 2: Generate Unique ID

```
READ registry.feedback_items

CALCULATE next_id:
  IF feedback_items is empty:
    next_seq = 1
  ELSE:
    last_id = feedback_items[-1].id  # e.g., "PF-005"
    last_seq = parseInt(last_id.split("-")[1])
    next_seq = last_seq + 1

new_id = "PF-" + String(next_seq).padStart(3, "0")

LOG: "Generated ID: {new_id}"
```

### Phase 3: Create Session Folder

```
session_date = format(NOW(), "yyyy-MM-dd")
session_folder_name = "{session_date}_PrototypeFeedback-{new_id}"
session_path = "Prototype_<SystemName>/feedback-sessions/{session_folder_name}/"

CREATE directory: session_path

LOG: "Created session folder: {session_folder_name}"
```

### Phase 4: Register Feedback Entry

```
CREATE feedback_entry = {
  id: new_id,
  status: "pending",
  type: impact_analysis.feedback_type,
  source: {
    person: metadata.source_person,
    role: metadata.source_role
  },
  inputter: {
    person: metadata.inputter_person,
    timestamp: NOW()
  },
  category: impact_analysis.categories,
  priority_score: impact_analysis.priority_score,
  severity: impact_analysis.severity,
  title: impact_analysis.title,
  description: feedback_content,
  impact_summary: {
    discovery_files: impact_analysis.counts.discovery,
    spec_files: impact_analysis.counts.specs,
    code_files: impact_analysis.counts.code,
    total_files: impact_analysis.counts.total
  },
  affected_items: impact_analysis.affected_items,
  session_folder: session_folder_name,
  debugging_evidence: null,
  selected_plan: null,
  lifecycle: {
    created_at: NOW(),
    ...rest_null
  },
  resume_point: null
}

APPEND to registry.feedback_items
UPDATE registry.statistics
UPDATE registry.$metadata.updated_at

WRITE registry
```

### Phase 5: Save Initial Artifacts

```
SAVE to session folder:

1. FEEDBACK_ORIGINAL.md
   ---
   document_id: PF-ORIG-{new_id}
   version: 1.0.0
   created_at: {date}
   updated_at: {date}
   generated_by: Prototype_FeedbackRegister
   source_files: []
   change_history:
     - version: "1.0.0"
       date: "{date}"
       author: "Prototype_FeedbackRegister"
       changes: "Initial feedback capture"
   ---

   # Original Feedback

   ## Metadata
   - **Feedback ID**: {new_id}
   - **Source**: {source_person} ({source_role})
   - **Recorded By**: {inputter_person}
   - **Date**: {date}

   ## Content
   {original_feedback_text}

2. impact_analysis.md (from Analyzer)
```

### Phase 6: Update State File

```
READ _state/prototype_feedback_state.json (or create if not exists)

UPDATE:
  active_feedback = {
    id: new_id,
    status: "pending",
    current_phase: 2,  # Impact Analysis complete
    current_step: 0,
    session_folder: session_folder_name,
    resume_point: null
  }

WRITE _state/prototype_feedback_state.json
```

## Status Transitions

```
pending → approved → in_progress → implemented → validated → closed
    ↓         ↓           ↓            ↓
 rejected   rejected    failed       failed

Valid transitions:
- pending → approved (user approves)
- pending → rejected (user rejects)
- approved → in_progress (implementation starts)
- approved → rejected (user changes mind)
- in_progress → implemented (implementation complete)
- in_progress → failed (implementation error)
- implemented → validated (validation passes)
- implemented → failed (validation fails)
- validated → closed (final closure)
- failed → in_progress (resume after fix)
```

## Update Functions

### Update Status

```
FUNCTION update_status(feedback_id, new_status, metadata):
  READ registry
  FIND entry WHERE id == feedback_id

  VALIDATE transition is allowed

  UPDATE entry.status = new_status
  UPDATE entry.lifecycle.{status}_at = NOW()

  IF new_status == "approved":
    entry.lifecycle.approved_by = metadata.approved_by

  IF new_status == "rejected":
    entry.lifecycle.rejected_by = metadata.rejected_by
    entry.lifecycle.rejection_reason = metadata.reason

  UPDATE registry.statistics
  WRITE registry

  LOG: "{feedback_id} status changed: {old} → {new}"
```

### Update Resume Point

```
FUNCTION set_resume_point(feedback_id, step_number, file_path, action):
  READ registry
  FIND entry WHERE id == feedback_id

  UPDATE entry.resume_point = {
    step_number: step_number,
    file_path: file_path,
    action: action,
    timestamp: NOW()
  }

  WRITE registry

  ALSO update _state/prototype_feedback_state.json
```

### Update Debugging Evidence

```
FUNCTION set_debugging_evidence(feedback_id, evidence):
  READ registry
  FIND entry WHERE id == feedback_id

  UPDATE entry.debugging_evidence = {
    root_cause: evidence.root_cause,
    hypothesis: evidence.hypothesis,
    confidence: evidence.confidence,
    recorded_at: NOW()
  }

  WRITE registry
```

## Query Functions

### Get Active Feedback

```
FUNCTION get_active_feedback():
  READ _state/prototype_feedback_state.json
  RETURN active_feedback
```

### Get Feedback by ID

```
FUNCTION get_feedback(feedback_id):
  READ registry
  FIND entry WHERE id == feedback_id
  RETURN entry
```

### Get Pending Feedback

```
FUNCTION get_pending():
  READ registry
  FILTER WHERE status == "pending"
  RETURN filtered_items
```

### Get Resume Point

```
FUNCTION get_resume_point(feedback_id):
  READ registry
  FIND entry WHERE id == feedback_id
  RETURN entry.resume_point
```

## Output Format

### Registration Confirmation

```
═══════════════════════════════════════════════════════════════
 FEEDBACK REGISTERED
═══════════════════════════════════════════════════════════════

ID: PF-001
Status: pending
Type: Bug
Severity: High
Priority Score: 25/30

Category: CAT-CODE, CAT-SCR

Impact Summary:
├─ Discovery Files: 0
├─ Specification Files: 3
├─ Code Files: 5
└─ Total: 8 files affected

Session Folder:
Prototype_InventorySystem/feedback-sessions/2025-12-22_PrototypeFeedback-001/

Artifacts Created:
├─ FEEDBACK_ORIGINAL.md
└─ impact_analysis.md

Next: Proceed to Approval Gate
═══════════════════════════════════════════════════════════════
```

## Integration Points

### Receives From
- `Prototype_FeedbackAnalyzer` - Impact analysis results
- User input - Approval decisions, plan selections

### Feeds Into
- `Prototype_FeedbackPlanner` - Registered feedback for planning
- `Prototype_FeedbackImplementer` - Status and resume tracking
- `Prototype_FeedbackValidator` - Status updates
- `_state/prototype_feedback_state.json` - Active state

## Error Handling

| Issue | Action |
|-------|--------|
| Registry corrupt | Backup existing, create new, log warning |
| Duplicate ID | Increment sequence, retry |
| Missing session folder | Create folder, log warning |
| State file missing | Create new state file |
| Invalid status transition | Reject update, return error |

## Integration with Skills

### Required Skills
- **systematic-debugging** - Used via Prototype_FeedbackAnalyzer for Bug types
- **root-cause-tracing** - Used via Prototype_FeedbackAnalyzer for Bug types

### Invoked By
- `/prototype-feedback` command

---

**Skill Version**: 1.0.0
**Framework Compatibility**: Prototype Skills Framework v2.3
