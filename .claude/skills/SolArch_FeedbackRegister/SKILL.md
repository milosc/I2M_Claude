---
name: registering-solarch-feedback
description: Use when you need to register, track, and manage Solution Architecture feedback entries with unique IDs, status tracking, and session folder management.
model: haiku
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill registering-solarch-feedback started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill registering-solarch-feedback ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill registering-solarch-feedback instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

---

# SolArch_FeedbackRegister

Registry management for Solution Architecture feedback processing.

## Purpose

Manages the central feedback registry for Solution Architecture, including ID assignment, session folder creation, status tracking, and metadata management.

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
- output files created (feedback registry updates)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "registering-solarch-feedback"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "registering-solarch-feedback" --stage solarch
```

Logging is handled automatically by the skill framework. No user action required.

---

## When to Use

- Processing new feedback on Solution Architecture outputs
- Creating feedback session folders
- Assigning unique feedback IDs
- Updating feedback status through workflow phases
- Listing or querying feedback items

## Input Requirements

### For New Feedback

```json
{
  "system_name": "InventorySystem",
  "feedback_text": "ADR-001 needs stronger justification...",
  "submitter": "Stakeholder",
  "priority": "Medium",
  "category": "ADR",
  "type": "Enhancement"
}
```

### For Status Update

```json
{
  "feedback_id": "SF-001",
  "new_status": "implementing",
  "metadata": { ... }
}
```

## Output Files

### Registry File

Location: `SolArch_<SystemName>/feedback-sessions/solarch_feedback_registry.json`

```json
{
  "$schema": "solarch-feedback-registry-v1",
  "version": "1.0.0",
  "created_at": "2025-12-22T10:00:00Z",
  "updated_at": "2025-12-22T11:30:00Z",
  "items": [
    {
      "id": "SF-001",
      "status": "completed",
      "created_at": "2025-12-22T10:00:00Z",
      "updated_at": "2025-12-22T11:30:00Z",
      "completed_at": "2025-12-22T11:30:00Z",
      "feedback_text": "ADR-001 needs stronger justification...",
      "submitter": "Stakeholder",
      "priority": "Medium",
      "category": "ADR",
      "type": "Enhancement",
      "session_folder": "2025-12-22_SolArchFeedback-001",
      "impacts": {
        "direct_files": 1,
        "cascade_files": 2,
        "traceability_chains": 3
      },
      "implementation": {
        "plan_selected": "Option A",
        "steps_total": 5,
        "steps_completed": 5,
        "files_changed": 3
      },
      "validation": {
        "passed": true,
        "timestamp": "2025-12-22T11:29:00Z"
      }
    }
  ],
  "statistics": {
    "total": 1,
    "by_status": {
      "pending": 0,
      "analyzing": 0,
      "awaiting_approval": 0,
      "implementing": 0,
      "validating": 0,
      "completed": 1,
      "rejected": 0,
      "failed": 0
    },
    "by_category": {
      "ADR": 1
    },
    "by_priority": {
      "Medium": 1
    }
  }
}
```

### Session Folder

Location: `SolArch_<SystemName>/feedback-sessions/<YYYY-MM-DD>_SolArchFeedback-<ID>/`

Created files:
- `FEEDBACK_ORIGINAL.md` - Original feedback content

## Procedures

### 1. Register New Feedback

```
PROCEDURE register_feedback(system_name, feedback_text, metadata):

  LOAD or CREATE registry:
    path = SolArch_{system_name}/feedback-sessions/solarch_feedback_registry.json
    IF NOT exists:
      CREATE with empty items array

  ASSIGN ID:
    next_id = max(items.*.id) + 1 OR 1
    feedback_id = "SF-{next_id:03d}"

  CREATE session folder:
    date = TODAY in YYYY-MM-DD format
    folder_name = "{date}_SolArchFeedback-{feedback_id}"
    folder_path = SolArch_{system_name}/feedback-sessions/{folder_name}/

  CREATE FEEDBACK_ORIGINAL.md:
    ---
    feedback_id: {feedback_id}
    received_at: {NOW}
    submitter: {metadata.submitter}
    priority: {metadata.priority}
    ---

    # Original Feedback

    {feedback_text}

    ## Metadata

    - **Category**: {metadata.category}
    - **Type**: {metadata.type}
    - **Priority**: {metadata.priority}

  ADD to registry:
    {
      "id": feedback_id,
      "status": "analyzing",
      "created_at": NOW(),
      "feedback_text": feedback_text,
      "submitter": metadata.submitter,
      "priority": metadata.priority,
      "category": metadata.category,
      "type": metadata.type,
      "session_folder": folder_name
    }

  UPDATE statistics

  RETURN feedback_id, folder_path
```

### 2. Update Feedback Status

```
PROCEDURE update_status(feedback_id, new_status, additional_data):

  LOAD registry

  FIND item with id == feedback_id
  IF NOT found:
    ERROR "Feedback {feedback_id} not found"

  UPDATE item:
    status = new_status
    updated_at = NOW()

    IF new_status == "completed":
      completed_at = NOW()

    MERGE additional_data into item

  UPDATE statistics

  SAVE registry
```

### 3. Get Feedback Item

```
PROCEDURE get_feedback(feedback_id):

  LOAD registry

  FIND item with id == feedback_id
  IF NOT found:
    RETURN null

  RETURN item
```

### 4. List Feedback Items

```
PROCEDURE list_feedback(filters):

  LOAD registry

  APPLY filters:
    IF filters.status:
      items = items WHERE status == filters.status
    IF filters.category:
      items = items WHERE category == filters.category
    IF filters.priority:
      items = items WHERE priority == filters.priority

  RETURN items
```

### 5. Get Session Folder Path

```
PROCEDURE get_session_path(feedback_id, system_name):

  LOAD registry

  FIND item with id == feedback_id

  RETURN SolArch_{system_name}/feedback-sessions/{item.session_folder}/
```

## Status Workflow

```
pending → analyzing → awaiting_approval → implementing → validating → completed
                  ↓                   ↓                         ↓
               rejected            modified                  failed
```

| Status | Description |
|--------|-------------|
| pending | Feedback received, not yet processed |
| analyzing | Impact analysis in progress |
| awaiting_approval | Analysis complete, waiting for decision |
| implementing | Approved, changes being made |
| validating | Implementation complete, validation in progress |
| completed | All phases complete, validation passed |
| rejected | Feedback rejected at approval gate |
| failed | Implementation or validation failed |

## Feedback Categories

| Category | Code | Description |
|----------|------|-------------|
| ADR | CAT-ADR | Architecture Decision Records |
| Component | CAT-COMP | Building block components |
| Diagram | CAT-DIAG | C4 or other diagrams |
| Quality | CAT-QUAL | Quality scenarios/requirements |
| Traceability | CAT-TRACE | Traceability chains |
| Documentation | CAT-DOC | Glossary, other docs |

## Feedback Types

| Type | Description |
|------|-------------|
| Enhancement | Add detail, expand coverage |
| Correction | Fix error or inaccuracy |
| Clarification | Make clearer, reduce ambiguity |
| Challenge | Question decision or approach |

## Priority Levels

| Priority | Description | SLA |
|----------|-------------|-----|
| Critical | Blocking issue | Immediate |
| High | Significant impact | Same session |
| Medium | Moderate impact | Normal flow |
| Low | Minor improvement | When convenient |

## Error Handling

| Error | Action |
|-------|--------|
| Registry file corrupt | Backup, recreate from session folders |
| Session folder exists | Append timestamp suffix |
| ID collision | Skip to next available ID |

## Integration Points

### Upstream
- Receives feedback from `/solarch-feedback` command
- Gets system_name from `_state/solarch_config.json`

### Downstream
- Provides feedback_id to `SolArch_FeedbackAnalyzer`
- Updates status based on `SolArch_FeedbackValidator` results

## Quality Gates

```bash
# Validate registry structure
python3 .claude/hooks/solarch_quality_gates.py --validate-feedback-registry --dir SolArch_X/

# List all feedback items
python3 .claude/hooks/solarch_quality_gates.py --list-feedback --dir SolArch_X/
```

## Template: FEEDBACK_ORIGINAL.md

```markdown
---
feedback_id: SF-001
received_at: 2025-12-22T10:00:00Z
submitter: Stakeholder
priority: Medium
---

# Original Feedback

[Feedback text here]

## Metadata

- **Category**: ADR
- **Type**: Enhancement
- **Priority**: Medium
- **Submitted By**: Stakeholder
- **Received At**: 2025-12-22T10:00:00Z

## Processing Status

- [ ] Impact Analysis
- [ ] Approval
- [ ] Implementation
- [ ] Validation
```
