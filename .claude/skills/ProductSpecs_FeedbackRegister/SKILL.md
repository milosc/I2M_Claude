---
name: registering-productspecs-feedback
description: Use when you need to register, track, and manage ProductSpecs feedback entries with unique IDs, status tracking, and session folder management.
model: haiku
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill registering-productspecs-feedback started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill registering-productspecs-feedback ended '{"stage": "productspecs"}'
---

# Register ProductSpecs Feedback

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill registering-productspecs-feedback instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: ProductSpecs_FeedbackRegister
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Claude Code
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description

Manages the ProductSpecs feedback registry, assigns unique IDs, creates session folders, and tracks feedback lifecycle. This skill is the central hub for feedback state management in the ProductSpecs stage.

**Role**: You are a Feedback Registry Manager. Your expertise is maintaining accurate records, generating sequential IDs, and ensuring all feedback has proper tracking throughout its lifecycle.

---

## Trigger Conditions

- New feedback received for ProductSpecs
- Request to register, track, or query feedback status
- Resume request for existing feedback

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| ProductSpecs Path | Yes | `ProductSpecs_<SystemName>` folder path |
| Feedback Content | Yes | Parsed feedback from analyzer |
| Impact Analysis | Yes | Results from ProductSpecs_FeedbackAnalyzer |
| Metadata | Yes | Source person, inputter, timestamp |

## Registry Structure

### Registry Location

```
ProductSpecs_<SystemName>/feedback-sessions/
├── productspecs_feedback_registry.json    # Central registry
└── <yyyy-mm-dd>_ProductSpecsFeedback-<ID>/ # Session folders
```

### Registry Schema

```json
{
  "$metadata": {
    "schema_version": "1.0.0",
    "created_at": "2025-12-22T10:00:00Z",
    "updated_at": "2025-12-22T10:30:00Z",
    "generated_by": "ProductSpecs_FeedbackRegister"
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
      "CAT-MOD": 3,
      "CAT-REQ": 4,
      "CAT-NFR": 2,
      "CAT-TEST": 1,
      "CAT-JIRA": 2
    },
    "by_type": {
      "Bug": 2,
      "Enhancement": 2,
      "TraceabilityGap": 1
    }
  },
  "feedback_items": []
}
```

### Feedback Entry Schema

```json
{
  "id": "PSF-001",
  "status": "pending",
  "type": "Bug|Enhancement|TraceabilityGap|RequirementChange|PriorityChange",
  "source": {
    "person": "John Smith",
    "role": "Product Manager"
  },
  "inputter": {
    "person": "Jane Doe",
    "timestamp": "2025-12-22T09:00:00Z"
  },
  "category": ["CAT-MOD", "CAT-REQ"],
  "priority_score": 25,
  "severity": "Critical|High|Medium|Low",
  "title": "Short descriptive title",
  "description": "Full feedback description",
  "impact_summary": {
    "module_files": 3,
    "requirement_entries": 5,
    "nfr_entries": 2,
    "test_cases": 8,
    "jira_items": 15,
    "total_affected": 33
  },
  "affected_items": {
    "modules": ["MOD-INV-SEARCH-01", "MOD-INV-ADJUST-01"],
    "requirements": ["REQ-001", "REQ-002"],
    "nfrs": ["NFR-PERF-001"],
    "tests": ["TC-E2E-001"],
    "jira": ["INV-1", "INV-2"]
  },
  "session_folder": "2025-12-22_ProductSpecsFeedback-001",
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
  registry_path = "ProductSpecs_<SystemName>/feedback-sessions/productspecs_feedback_registry.json"

IF NOT exists:
  CREATE directory: "ProductSpecs_<SystemName>/feedback-sessions/"

  CREATE registry = {
    "$metadata": {
      "schema_version": "1.0.0",
      "created_at": NOW(),
      "updated_at": NOW(),
      "generated_by": "ProductSpecs_FeedbackRegister"
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
    last_id = feedback_items[-1].id  # e.g., "PSF-005"
    last_seq = parseInt(last_id.split("-")[1])
    next_seq = last_seq + 1

new_id = "PSF-" + String(next_seq).padStart(3, "0")

LOG: "Generated ID: {new_id}"
```

### Phase 3: Create Session Folder

```
session_date = format(NOW(), "yyyy-MM-dd")
session_folder_name = "{session_date}_ProductSpecsFeedback-{new_id}"
session_path = "ProductSpecs_<SystemName>/feedback-sessions/{session_folder_name}/"

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
    module_files: impact_analysis.counts.modules,
    requirement_entries: impact_analysis.counts.requirements,
    nfr_entries: impact_analysis.counts.nfrs,
    test_cases: impact_analysis.counts.tests,
    jira_items: impact_analysis.counts.jira,
    total_affected: impact_analysis.counts.total
  },
  affected_items: impact_analysis.affected_items,
  session_folder: session_folder_name,
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
   document_id: PSF-ORIG-{new_id}
   version: 1.0.0
   created_at: {date}
   updated_at: {date}
   generated_by: ProductSpecs_FeedbackRegister
   source_files: []
   change_history:
     - version: "1.0.0"
       date: "{date}"
       author: "ProductSpecs_FeedbackRegister"
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
READ _state/productspecs_feedback_state.json (or create if not exists)

UPDATE:
  active_feedback = {
    id: new_id,
    status: "pending",
    current_phase: 2,  # Impact Analysis complete
    current_step: 0,
    session_folder: session_folder_name,
    resume_point: null
  }

WRITE _state/productspecs_feedback_state.json
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

## Impact Categories

| Category | Code | Description |
|----------|------|-------------|
| Modules | CAT-MOD | Module specifications |
| Requirements | CAT-REQ | Requirements registry |
| NFRs | CAT-NFR | Non-functional requirements |
| Tests | CAT-TEST | Test specifications |
| JIRA | CAT-JIRA | JIRA export files |
| Traceability | CAT-TRACE | Traceability chains |

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

  ALSO update _state/productspecs_feedback_state.json
```

## Output Format

### Registration Confirmation

```
═══════════════════════════════════════════════════════════════
 PRODUCTSPECS FEEDBACK REGISTERED
═══════════════════════════════════════════════════════════════

ID: PSF-001
Status: pending
Type: RequirementChange
Severity: High
Priority Score: 25/30

Category: CAT-MOD, CAT-REQ, CAT-JIRA

Impact Summary:
├─ Module Files: 3
├─ Requirement Entries: 5
├─ NFR Entries: 2
├─ Test Cases: 8
├─ JIRA Items: 15
└─ Total: 33 items affected

Session Folder:
ProductSpecs_InventorySystem/feedback-sessions/2025-12-22_ProductSpecsFeedback-001/

Artifacts Created:
├─ FEEDBACK_ORIGINAL.md
└─ impact_analysis.md

Next: Proceed to Approval Gate
═══════════════════════════════════════════════════════════════
```

## Integration Points

### Receives From
- `ProductSpecs_FeedbackAnalyzer` - Impact analysis results
- User input - Approval decisions, plan selections

### Feeds Into
- `ProductSpecs_FeedbackImplementer` - Status and resume tracking
- `ProductSpecs_FeedbackValidator` - Status updates
- `_state/productspecs_feedback_state.json` - Active state

## Error Handling

| Issue | Action |
|-------|--------|
| Registry corrupt | Backup existing, create new, log warning |
| Duplicate ID | Increment sequence, retry |
| Missing session folder | Create folder, log warning |
| State file missing | Create new state file |
| Invalid status transition | Reject update, return error |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: ProductSpecs Skills Framework v1.0
