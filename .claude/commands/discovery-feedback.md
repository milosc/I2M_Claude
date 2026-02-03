---
name: discovery-feedback
description: Process feedback on Discovery artifacts with reflexion-enhanced impact analysis and traceability
argument-hint: [feedback_text | file.md | resume FB-NNN | status | list]
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-feedback started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-feedback ended '{"stage": "discovery"}'
---

# /discovery-feedback - Process Discovery Feedback

**Version**: 2.0.0 (Reflexion Integration)
**Template**: `.claude/templates/feedback-workflow-template.md`

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-feedback instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

## Overview

This command processes feedback on Discovery artifacts using reflexion-enhanced analysis to ensure complete impact assessment and high-quality implementation.

**Key Features**:
- ✓ Reflexion-powered impact analysis with confidence scoring
- ✓ Hierarchical traceability chain visualization with before/after content
- ✓ Multiple implementation options with reflexion evaluation (X/10 scores)
- ✓ Multi-perspective validation (Requirements, Architecture, Quality)
- ✓ Structured user decisions via AskUserQuestion

## Arguments

| Argument | Description |
|----------|-------------|
| (empty) | Interactive mode - prompts for feedback |
| `"<text>"` | Inline feedback text |
| `<file.md>` | Path to feedback file |
| `resume FB-NNN` | Resume failed/partial implementation |
| `status` | Show current feedback processing status |
| `list` | List all registered feedback items |

## Prerequisites

- Completed Discovery analysis exists in `ClientAnalysis_<SystemName>/`
- Dependencies installed (`/htec-libraries-init`)
- Traceability folder exists (`traceability/`)

## Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│              DISCOVERY FEEDBACK WORKFLOW                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. INPUT          Collect feedback, metadata               │
│  2. ANALYZE        ← REFLEXION: Impact analysis + critique  │
│  3. REGISTER       Assign FB-NNN, create session            │
│  4. APPROVE        ← AskUserQuestion: Approve/Reject/Modify │
│  5. PLAN           ← REFLEXION: Evaluate options (X/10)     │
│  6. IMPLEMENT      Execute selected plan                    │
│  7. VALIDATE       ← REFLEXION: Multi-perspective review    │
│  8. COMPLETE       Generate summary, close                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Input Collection

### Step 1.1: Parse Arguments

```bash
IF $ARGUMENTS == "resume FB-NNN":
   JUMP to Phase 6 (Resume Mode)

ELIF $ARGUMENTS == "status":
   READ traceability/feedback_sessions/discovery/discover_feedback_register.json
   DISPLAY active feedback status
   EXIT

ELIF $ARGUMENTS == "list":
   READ traceability/feedback_sessions/discovery/discover_feedback_register.json
   DISPLAY all feedback items with statistics
   EXIT

ELIF $ARGUMENTS is file path (.md or .txt):
   READ file content
   feedback_content = file_contents

ELIF $ARGUMENTS is text:
   feedback_content = $ARGUMENTS

ELSE (no arguments):
   PROMPT: "Please provide your Discovery feedback:"
   feedback_content = user_input
```

### Step 1.2: Identify Target System

```bash
LIST available ClientAnalysis_* folders

IF multiple folders:
   PROMPT: "Which system does this feedback apply to?"
   OPTIONS: [List all ClientAnalysis_* folders]
   system_name = user_selection
ELSE:
   system_name = single_folder_name

STORE as SYSTEM_NAME
```

### Step 1.3: Collect Metadata

```bash
PROMPT: "Who is the source of this feedback? (Name/Role)"
source_person = user_input

PROMPT: "Who is entering this feedback? (Your name)"
inputter = user_input

date_time = NOW()
```

---

## Phase 2: Impact Analysis (REFLEXION ENHANCED)

### Step 2.1: Execute Reflexion-Enhanced Impact Analysis

```bash
READ skill: .claude/skills/Shared_FeedbackImpactAnalyzer_Reflexion/SKILL.md

INVOKE Shared_FeedbackImpactAnalyzer_Reflexion:
   inputs:
      feedback_content: {feedback_content}
      stage: "discovery"
      system_name: {SYSTEM_NAME}
      stage_folder: "ClientAnalysis_{SYSTEM_NAME}/"

   returns:
      impact_analysis_path: path to impact_analysis.md
      summary: {
         chains_affected: N,
         artifacts_affected: M,
         confidence_level: "HIGH|MEDIUM|LOW",
         confidence_percentage: XX
      }
```

**Impact Analysis Output includes**:
- Hierarchical traceability chains (PP → JTBD → Requirements → Screens → Components)
- Before/after content for each change
- Flat summary table
- Reflexion self-critique:
  - ✓ Completeness check
  - ✓ Accuracy check
  - ✓ Downstream impact assessment
  - ✓ Risk assessment
- Confidence level with percentage

### Step 2.2: Display Impact Analysis

```bash
READ impact_analysis_path

DISPLAY to user:
   - Feedback classification (type, severity, categories)
   - Hierarchical chains with before/after
   - Flat summary table
   - Reflexion critique with confidence level
```

---

## Phase 3: Registration

### Step 3.1: Assign Feedback ID

```bash
READ or CREATE: traceability/feedback_sessions/discovery/discover_feedback_register.json

CALCULATE next_id:
   existing_ids = [item.id for item in register.feedback_items]
   max_num = MAX([int(id.split('-')[1]) for id in existing_ids]) OR 0
   next_id = "FB-" + ZERO_PAD(max_num + 1, 3)

STORE as feedback_id
```

### Step 3.2: Create Session Folder

```bash
session_date = FORMAT(NOW(), "YYYY-MM-DD")
session_folder = "traceability/feedback_sessions/discovery/{session_date}_Feedback_{feedback_id}/"

mkdir -p {session_folder}

COPY feedback_content → {session_folder}/FEEDBACK_ORIGINAL.md
COPY impact_analysis → {session_folder}/impact_analysis.md
```

### Step 3.3: Register Feedback

```bash
CREATE registry entry:
{
   "id": "{feedback_id}",
   "status": "analyzing",
   "type": "{type_from_analysis}",
   "severity": "{severity_from_analysis}",
   "categories": ["{categories}"],
   "created_at": "{ISO8601}",
   "source": {
      "person": "{source_person}",
      "inputter": "{inputter}"
   },
   "impact": {
      "chains_affected": {N},
      "artifacts_affected": {M},
      "confidence_level": "{level}",
      "confidence_percentage": {XX}
   },
   "lifecycle": {
      "analyzed_at": "{ISO8601}"
   }
}

UPDATE registry file

DISPLAY:
═══════════════════════════════════════════════════════════════
 FEEDBACK REGISTERED - {feedback_id}
═══════════════════════════════════════════════════════════════

ID: {feedback_id}
Type: {type}
Severity: {severity}
Artifacts Affected: {M}
Confidence: {level} ({XX}%)
Session: {session_folder}

═══════════════════════════════════════════════════════════════
```

---

## Phase 4: Approval Gate (ASKUSERQUESTION)

### Step 4.1: Present Impact Summary

```bash
SUMMARIZE from impact_analysis.md:
   - Total chains affected
   - Total artifacts affected
   - Change distribution (Create/Modify/Delete)
   - Risk level
   - Confidence level
```

### Step 4.2: Request Approval Decision

```bash
USE AskUserQuestion:
   question: "Feedback {feedback_id} affects {M} artifacts across {N} traceability chains with {severity} impact. Reflexion confidence: {level} ({XX}%). Review the detailed impact analysis above. How should we proceed?"
   header: "Approval"
   options:
      - label: "Approve (Recommended)"
        description: "Proceed to implementation planning. Estimated effort will be calculated during planning."
      - label: "Reject"
        description: "Mark feedback as rejected. No changes will be made. Requires rejection reason."
      - label: "Modify Scope"
        description: "Adjust which artifacts to change before proceeding to planning."
      - label: "Request Deeper Analysis"
        description: "Reflexion confidence is {level} - request more investigation before deciding."

STORE user_decision
```

### Step 4.3: Handle Decision

```bash
IF user_decision == "Approve":
   UPDATE registry:
      status = "approved"
      lifecycle.approved_at = NOW()
      lifecycle.approved_by = "{user}"

   CONTINUE to Phase 5

ELIF user_decision == "Reject":
   PROMPT: "Please provide rejection reason:"
   rejection_reason = user_input

   UPDATE registry:
      status = "rejected"
      lifecycle.rejected_at = NOW()
      lifecycle.rejected_by = "{user}"
      lifecycle.rejection_reason = "{rejection_reason}"

   GENERATE FEEDBACK_SUMMARY.md with rejection note
   EXIT WORKFLOW

ELIF user_decision == "Modify Scope":
   # Extract artifact types from impact analysis
   artifact_types = EXTRACT_UNIQUE_TYPES(impact_analysis)

   USE AskUserQuestion:
      question: "Select artifact types to EXCLUDE from implementation:"
      header: "Scope"
      multiSelect: true
      options: [Generate option for each artifact_type]

   excluded_types = user_selections

   # Regenerate impact_analysis with filtered scope
   RE-RUN Phase 2 with exclusion filter
   RETURN to Step 4.2 (Approval Gate)

ELIF user_decision == "Request Deeper Analysis":
   PROMPT: "What specific areas need more investigation?"
   focus_areas = user_input

   # Re-run impact analysis with focused investigation
   RE-RUN Phase 2 with focus_areas parameter
   RETURN to Step 4.2 (Approval Gate)
```

---

## Phase 5: Implementation Planning (REFLEXION ENHANCED)

### Step 5.1: Generate Implementation Options

```bash
READ skill: .claude/skills/Shared_FeedbackPlanGenerator_Reflexion/SKILL.md

INVOKE Shared_FeedbackPlanGenerator_Reflexion:
   inputs:
      impact_analysis_path: {session_folder}/impact_analysis.md
      feedback_id: {feedback_id}
      stage: "discovery"
      system_name: {SYSTEM_NAME}
      stage_folder: "ClientAnalysis_{SYSTEM_NAME}/"

   returns:
      options_path: path to implementation_options.md
      options: [
         {
            id: "A",
            name: "{name}",
            steps: N,
            artifacts: M,
            effort: "{time}",
            score: X.X,
            recommendation: "APPROVE|APPROVE WITH CAUTION|REJECT",
            recommended: true|false
         },
         ...
      ]
      recommended_option: "{id}"
```

**Options Generated** (minimum 2):
- **Option A**: Minimal/Quick (addresses only critical artifacts)
- **Option B**: Comprehensive/Standard (all artifacts, maintains traceability) **← Usually RECOMMENDED**
- **Option C**: Extended/Preventive (includes improvements and safeguards)

**Each Option Includes**:
- Detailed steps with before/after content
- Traceability update specifications
- Version increment strategy
- Reflexion evaluation:
  - Completeness score (X/10)
  - Consistency score (X/10)
  - Quality score (X/10)
  - Risk assessment
  - Final score (X/10) and recommendation

### Step 5.2: Display Options Comparison

```bash
READ implementation_options.md

DISPLAY comparison table:
| Option | Steps | Artifacts | Effort | Score | Recommendation |
|--------|-------|-----------|--------|-------|----------------|
| A: ... | {N}   | {M}       | {time} | {X}/10| {emoji} {label}|
| B: ... | {N}   | {M}       | {time} | {X}/10| {emoji} {label}|
| C: ... | {N}   | {M}       | {time} | {X}/10| {emoji} {label}|

DISPLAY detailed breakdown for each option including reflexion evaluation
```

### Step 5.3: Request Plan Selection

```bash
highest_score_option = options.sort_by_score_desc()[0]

USE AskUserQuestion:
   question: "Three implementation options generated with reflexion scores. Option {highest_score_option.id} scored {highest_score_option.score}/10 as the most complete approach. Which option should we use?"
   header: "Plan"
   options:
      - label: "Option A: {name}"
        description: "{steps} steps, {artifacts} artifacts, {effort}. Reflexion score: {score}/10 - {recommendation}"
      - label: "Option B: {name} (Recommended)"
        description: "{steps} steps, {artifacts} artifacts, {effort}. Reflexion score: {score}/10 - {recommendation}"
      - label: "Option C: {name}"
        description: "{steps} steps, {artifacts} artifacts, {effort}. Reflexion score: {score}/10 - {recommendation}"

STORE selected_option
```

### Step 5.4: Handle Custom Plan (if Option C is "Custom")

```bash
IF selected_option == "Custom Plan":
   PROMPT: "Provide your custom implementation plan (step-by-step with file paths and changes):"
   custom_plan_text = user_input

   # Evaluate custom plan using reflexion
   INVOKE Shared_FeedbackPlanGenerator_Reflexion with custom_plan_text

   DISPLAY evaluation results

   USE AskUserQuestion:
      question: "Custom plan scored {score}/10. Proceed or revise?"
      header: "Decision"
      options:
         - label: "Proceed"
         - label: "Revise Plan"

   IF "Revise": LOOP back to custom plan input
```

### Step 5.5: Finalize Plan

```bash
CREATE implementation_plan.md:
   - Copy selected option details
   - Mark as selected
   - Include full reflexion evaluation
   - Include all steps with before/after content

SAVE to {session_folder}/implementation_plan.md

UPDATE registry:
   implementation.plan_selected = "{selected_option.id}"
   implementation.steps_total = {selected_option.steps}
   lifecycle.planned_at = NOW()

UPDATE _state/discovery_config.json:
   feedback_plan_selection = "{selected_option.id}"
   feedback_session_id = "{feedback_id}"
```

---

## Phase 6: Implementation

### Step 6.1: Create Backups

```bash
FOR each file IN implementation_plan.steps[].file_path:
   IF file exists:
      cp {file} {file}.backup
```

### Step 6.2: Update Registry Status

```bash
UPDATE registry:
   status = "in_progress"
   lifecycle.implementation_started_at = NOW()
```

### Step 6.3: Execute Implementation

```bash
READ implementation_plan.md

steps = implementation_plan.steps[]

FOR each step IN steps:

   LOG to implementation_log.md:
      "Step {step.step_number}: {step.action} {step.artifact_id}"
      "Starting at: {timestamp}"

   # Read current file
   current_content = READ(step.file_path)

   # Verify before state (if MODIFY)
   IF step.action == "MODIFY":
      IF NOT VERIFY_CONTENT_MATCH(current_content, step.before_content):
         LOG warning: "File state differs from plan"

         USE AskUserQuestion:
            question: "Step {N}: File state at {step.file_path} differs from planned 'before' content. This may indicate another change occurred. Continue anyway?"
            header: "Warning"
            options:
               - label: "Continue Anyway"
               - label: "Skip This Step"
               - label: "Abort Implementation"

         IF "Skip This Step":
            LOG: "Step {N} skipped by user"
            CONTINUE to next step

         IF "Abort Implementation":
            UPDATE registry: status = "failed", resume_point = "Step {N}"
            EXIT

   # Apply changes
   IF step.action == "CREATE":
      WRITE(step.file_path, step.after_content)

   ELIF step.action == "MODIFY":
      # Update version in frontmatter
      new_content = UPDATE_VERSION(current_content, step.version_update.new)

      # Add change_history entry
      new_content = ADD_CHANGE_HISTORY(new_content, {
         version: step.version_update.new,
         date: TODAY(),
         author: "Discovery_FeedbackImplementer",
         changes: step.description,
         feedback_ref: feedback_id
      })

      # Apply content changes
      new_content = APPLY_CHANGES(new_content, step.after_content, step.section)

      WRITE(step.file_path, new_content)

   ELIF step.action == "DELETE":
      mv {step.file_path} {step.file_path}.deleted

   # Update traceability registries
   IF step.traceability_updates:
      FOR each update IN step.traceability_updates:
         registry = READ(update.registry)
         registry = UPDATE_FIELD(registry, update.field, update.change)
         WRITE(update.registry, registry)

   # Log success
   LOG to implementation_log.md:
      "Step {step.step_number}: SUCCESS"
      "Completed at: {timestamp}"
      "File: {step.file_path}"
      "Version: {step.version_update.new}"

   # Update resume point
   UPDATE registry:
      implementation.steps_completed = {step.step_number}
      implementation.resume_point = null

   # Handle errors
   IF step fails:
      LOG to implementation_log.md:
         "Step {step.step_number}: FAILED"
         "Error: {error_message}"

      USE AskUserQuestion:
         question: "Step {N} failed: {error}. How to proceed?"
         header: "Error"
         options:
            - label: "Skip and Continue"
              description: "Log failure and continue with remaining steps"
            - label: "Retry Step"
              description: "Attempt this step again"
            - label: "Abort and Save Resume Point"
              description: "Stop implementation, save progress for later resume"

      IF "Skip and Continue":
         LOG: "Step {N} skipped due to error"
         CONTINUE

      IF "Retry Step":
         RETRY current step (once)

      IF "Abort and Save Resume Point":
         UPDATE registry:
            status = "failed"
            implementation.resume_point = "Step {N}"
         EXIT
```

### Step 6.4: Generate Files Changed Summary

```bash
CREATE files_changed.md:

# Files Changed - {feedback_id}

## Summary
- Total files modified: {count}
- Create: {create_count}
- Modify: {modify_count}
- Delete: {delete_count}

## Details

### Created Files
- {file_1}
  - Purpose: {purpose}
  - Step: {step_number}

### Modified Files
- {file_1}
  - Sections: {sections}
  - Version: {old} → {new}
  - Step: {step_number}

### Deleted Files
- {file_1}
  - Reason: {reason}
  - Step: {step_number}

SAVE to {session_folder}/files_changed.md
```

### Step 6.5: Update Completion Status

```bash
UPDATE registry:
   status = "implemented"
   lifecycle.implementation_completed_at = NOW()
   implementation.files_changed = [list of modified files]
```

---

## Phase 7: Validation (REFLEXION ENHANCED)

### Step 7.1: Execute Reflexion-Enhanced Validation

```bash
READ skill: .claude/skills/Shared_FeedbackReviewer_Reflexion/SKILL.md

INVOKE Shared_FeedbackReviewer_Reflexion:
   inputs:
      feedback_id: {feedback_id}
      stage: "discovery"
      system_name: {SYSTEM_NAME}
      stage_folder: "ClientAnalysis_{SYSTEM_NAME}/"
      implementation_plan_path: {session_folder}/implementation_plan.md
      implementation_log_path: {session_folder}/implementation_log.md
      files_changed_path: {session_folder}/files_changed.md

   returns:
      validation_report_path: path to VALIDATION_REPORT.md
      validation_result: "PASS|CONDITIONAL PASS|FAIL"
      consensus_score: X.X
      action_items_count: N
      critical_issues_count: M
```

**Validation Includes**:
1. **Plan Compliance**: All steps executed? Any deviations?
2. **Content Validation**: Version updates, change history, content match, format validity
3. **Traceability Validation**: Registry integrity, bidirectional links, chain completeness
4. **Stage-Specific**: Discovery quality gates (checkpoint 11)
5. **Reflexion Multi-Perspective Review**:
   - Requirements Validator perspective (score/10)
   - Solution Architect perspective (score/10)
   - Code Quality Reviewer perspective (score/10)
   - Consensus score and recommendation

### Step 7.2: Run Discovery Quality Gates

```bash
RUN quality gate validation:
   python3 .claude/hooks/discovery_quality_gates.py \
      --validate-checkpoint 11 \
      --dir ClientAnalysis_{SYSTEM_NAME}/

CAPTURE output and append to validation results
```

### Step 7.3: Display Validation Results

```bash
READ VALIDATION_REPORT.md

DISPLAY:
═══════════════════════════════════════════════════════════════
 VALIDATION RESULTS - {feedback_id}
═══════════════════════════════════════════════════════════════

Overall Status: {PASS|CONDITIONAL PASS|FAIL}
Consensus Score: {X.X}/10
Consensus Confidence: {HIGH|MEDIUM|LOW}

Plan Compliance: {score}/10
Content Validation: {score}/10
Traceability: {score}/10
Discovery Quality Gates: {PASS|FAIL}

Reflexion Multi-Perspective Review:
├─ Requirements Validator: {score}/10
├─ Solution Architect: {score}/10
└─ Code Quality Reviewer: {score}/10

{IF action items:}
Action Items: {N} identified ({M} critical)

Recommendation: {recommendation}

═══════════════════════════════════════════════════════════════
```

### Step 7.4: Handle Validation Results

```bash
IF validation_result == "PASS":
   UPDATE registry:
      status = "validated"
      lifecycle.validated_at = NOW()
      validation.consensus_score = {consensus_score}

   CONTINUE to Phase 8

ELIF validation_result == "CONDITIONAL PASS":
   DISPLAY action items

   USE AskUserQuestion:
      question: "Validation identified {N} minor issues (consensus score {score}/10). How to proceed?"
      header: "Decision"
      options:
         - label: "Accept As-Is"
           description: "Close feedback with known minor issues documented"
         - label: "Fix Issues Now"
           description: "Return to implementation to address issues"

   IF "Accept As-Is":
      UPDATE registry: status = "validated"
      CONTINUE to Phase 8

   IF "Fix Issues Now":
      # Return to Phase 6 with fix instructions
      RETURN to Phase 6 with action_items as guidance

ELIF validation_result == "FAIL":
   DISPLAY critical issues and action items

   USE AskUserQuestion:
      question: "Validation failed with {M} critical issues (consensus score {score}/10). How to proceed?"
      header: "Decision"
      options:
         - label: "Fix and Retry"
           description: "Return to implementation to fix critical issues"
         - label: "Rollback Changes"
           description: "Restore from backups and abort this feedback"
         - label: "Mark As Incomplete"
           description: "Close feedback with failures documented"

   IF "Fix and Retry":
      RETURN to Phase 6 with critical_issues as guidance

   IF "Rollback Changes":
      # Restore backups
      FOR each file IN implementation_log.modified_files:
         IF {file}.backup exists:
            mv {file}.backup {file}

      UPDATE registry: status = "rolled_back"
      EXIT

   IF "Mark As Incomplete":
      UPDATE registry: status = "failed"
      CONTINUE to Phase 8
```

---

## Phase 8: Completion

### Step 8.1: Generate Feedback Summary

```bash
CREATE FEEDBACK_SUMMARY.md:

---
document_id: SUM-{feedback_id}
version: 1.0.0
created_at: {YYYY-MM-DD}
feedback_id: {feedback_id}
stage: discovery
system_name: {SYSTEM_NAME}
---

# Feedback Summary - {feedback_id}

## Original Feedback

{From FEEDBACK_ORIGINAL.md}

## Impact Analysis Summary

- Traceability Chains Affected: {N}
- Artifacts Modified: {M}
- Confidence Level: {level} ({XX}%)

### Affected Artifacts by Type

| Type | Count | Create | Modify | Delete |
|------|-------|--------|--------|--------|
{From impact_analysis.md}

## Implementation Approach

- **Selected Plan**: {option_name}
- **Reflexion Score**: {X.X}/10
- **Total Steps**: {N}
- **Estimated Effort**: {time}
- **Actual Duration**: {calculated from timestamps}

## Changes Made

{From files_changed.md}

## Validation Results

- **Plan Compliance**: {score}/10
- **Content Validation**: {score}/10
- **Traceability**: {score}/10
- **Quality Gates**: {PASS|FAIL}

### Reflexion Consensus

- Requirements Validator: {score}/10
- Solution Architect: {score}/10
- Code Quality Reviewer: {score}/10
- **Consensus Score**: **{X.X}/10**
- **Recommendation**: {recommendation}

{IF action items:}
### Action Items

{List action items from validation}

## Timeline

| Phase | Duration | Timestamp |
|-------|----------|-----------|
| Analysis | {duration} | {timestamp} |
| Planning | {duration} | {timestamp} |
| Implementation | {duration} | {timestamp} |
| Validation | {duration} | {timestamp} |
| **Total** | **{total}** | - |

## Final Status

**Status**: {status}
**Closed**: {closed_at OR "Open"}

{IF status == "validated":}
✅ Feedback successfully processed and validated.

{IF status == "failed":}
❌ Feedback processing failed. See validation report for details.

{IF status == "rolled_back":}
🔄 Changes rolled back. Feedback marked as not implemented.

SAVE to {session_folder}/FEEDBACK_SUMMARY.md
```

### Step 8.2: Update Registry

```bash
UPDATE registry:
   lifecycle.completed_at = NOW()
```

### Step 8.3: Request Closure

```bash
USE AskUserQuestion:
   question: "Feedback {feedback_id} processing complete with status: {status}. Close feedback?"
   header: "Closure"
   options:
      - label: "Close"
        description: "Mark as closed, feedback workflow complete"
      - label: "Keep Open"
        description: "Leave open for additional review or follow-up"

IF "Close":
   UPDATE registry:
      status = "closed"
      lifecycle.closed_at = NOW()
```

### Step 8.4: Display Completion Summary

```bash
DISPLAY:
═══════════════════════════════════════════════════════════════
 FEEDBACK PROCESSING COMPLETE - {feedback_id}
═══════════════════════════════════════════════════════════════

ID: {feedback_id}
Status: {status}
Type: {type}

Statistics:
- Artifacts Modified: {M}
- Traceability Chains Updated: {N}
- Implementation Steps: {steps_completed}/{steps_total}
- Reflexion Consensus Score: {X.X}/10

Timeline:
- Total Duration: {total_duration}

Session Folder: {session_folder}

Artifacts Generated:
├─ FEEDBACK_ORIGINAL.md
├─ impact_analysis.md              ← Reflexion critique included
├─ implementation_options.md       ← Reflexion scores included
├─ implementation_plan.md          ← Selected option with full details
├─ implementation_log.md           ← Step-by-step execution log
├─ files_changed.md                ← Change summary
├─ VALIDATION_REPORT.md            ← Multi-perspective review
└─ FEEDBACK_SUMMARY.md             ← Complete timeline and results

═══════════════════════════════════════════════════════════════
```

---

## Resume Mode

To resume a failed or partial implementation:

```bash
/discovery-feedback resume FB-NNN
```

**Resume Process**:
1. Load feedback from registry
2. Load implementation_log.md
3. Identify last successful step (resume_point)
4. Verify file states match expected
5. Add resume marker to log
6. Continue from resume_point + 1

---

## Status Mode

```bash
/discovery-feedback status
```

**Displays**:
- Active feedback ID (if any)
- Current status
- Current phase
- Resume point (if failed)
- Last activity timestamp

---

## List Mode

```bash
/discovery-feedback list
```

**Displays**:
- All registered feedback items
- Status distribution
- Type distribution
- Average reflexion scores

---

## Output Structure

```
traceability/feedback_sessions/discovery/
├── discover_feedback_register.json       # Central registry
└── <YYYY-MM-DD>_Feedback_<ID>/           # Per-feedback session
    ├── FEEDBACK_ORIGINAL.md
    ├── impact_analysis.md                ← WITH reflexion critique
    ├── implementation_options.md         ← WITH reflexion scores
    ├── implementation_plan.md            ← WITH before/after content
    ├── implementation_log.md
    ├── files_changed.md
    ├── VALIDATION_REPORT.md              ← WITH multi-perspective review
    └── FEEDBACK_SUMMARY.md
```

---

## Discovery-Specific Notes

### Artifact Types
- Pain Points (PP-X.X)
- JTBDs (JTBD-X.X)
- Personas (PERSONA-XX)
- Vision documents
- Strategy documents
- Screen definitions
- Component inventory
- Data fields

### Traceability Chains
Typical chain: `CM-XXX → PP-X.X → JTBD-X.X → REQ-XXX → SCR-XXX`

### Quality Gates
Discovery checkpoint 11 validation includes:
- All deliverables complete
- Traceability integrity
- Source citations present
- Version metadata correct

---

## Error Handling

| Error | Action |
|-------|--------|
| No ClientAnalysis folder | Error: Run /discovery first |
| File read failure during analysis | Skip file, note in impact_analysis.md |
| File write failure during implementation | Log failure, save resume point, offer retry |
| Validation failure | Show issues, offer fix/accept/abort |
| Traceability breaks | Warn, attempt auto-fix, flag in validation |

---

## Examples

### Example 1: Direct Text Feedback

```bash
/discovery-feedback "The warehouse operator persona should include night shift workers who have different pain points around visibility in low-light conditions"
```

### Example 2: File-Based Feedback

```bash
/discovery-feedback ./stakeholder_feedback.md
```

### Example 3: Interactive Mode

```bash
/discovery-feedback
> (prompts for feedback input)
```

### Example 4: Resume Failed Implementation

```bash
/discovery-feedback resume FB-003
```

### Example 5: Check Status

```bash
/discovery-feedback status
```

### Example 6: List All Feedback

```bash
/discovery-feedback list
```

---

## Related Commands

- `/discovery-status` - Check overall discovery status
- `/discovery-validate` - Run validation without feedback
- `/discovery-rebuild-traceability` - Rebuild traceability registries

---

## Version History

- **2.0.0** (2026-01-25): Reflexion integration, hierarchical chains, AskUserQuestion, before/after content
- **1.0.0**: Initial release

---

**Template Reference**: `.claude/templates/feedback-workflow-template.md`
