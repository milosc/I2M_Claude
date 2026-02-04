---
name: productspecs-feedback
description: Process feedback on ProductSpecs with reflexion-enhanced impact analysis and JIRA regeneration tracking
argument-hint: [feedback-text] | --feedback-id <ID> | resume <ID> | status | list
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Skill
skills:
  required:
    - Shared_FeedbackImpactAnalyzer_Reflexion
    - Shared_FeedbackPlanGenerator_Reflexion
    - Shared_FeedbackReviewer_Reflexion
  optional:
    - five-whys
    - thinking-critically
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-feedback started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-feedback ended '{"stage": "productspecs"}'
---

# /productspecs-feedback - Process ProductSpecs Change Requests

**Version**: 2.0.0 (Reflexion-Enhanced)
**Stage**: ProductSpecs (Stage 3)
**Last Updated**: 2026-01-25

---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs-feedback instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

---

## Overview

This command provides a **reflexion-enhanced workflow** for processing feedback and change requests on ProductSpecs artifacts (modules, requirements, NFRs, tests, JIRA exports). It integrates critical self-assessment, hierarchical traceability visualization, and JIRA regeneration impact tracking.

### What's New in v2.0.0

1. **Reflexion Integration**: Critical self-assessment at Impact Analysis, Planning, and Validation phases
2. **AskUserQuestion Integration**: Structured decision prompts at all gates
3. **Hierarchical Chain Visualization**: Tree-structured traceability with before/after content
4. **JIRA Regeneration Tracking**: Detailed impact assessment for JIRA ticket regeneration
5. **Confidence Scoring**: Weighted scoring (40% completeness + 35% accuracy + 25% downstream) producing LOW/MEDIUM/HIGH
6. **Before/After Content Specification**: Exact content snippets for every change
7. **Module Chain Traceability**: Full MOD-XXX-XXX-NN → Requirements → Tests → JIRA mapping

---

## Arguments

- `$ARGUMENTS` - Optional: `[feedback_text | file.md | resume PSF-NNN | status | list]`

## Usage

| Command | Description |
|---------|-------------|
| `/productspecs-feedback` | Interactive mode - prompts for feedback |
| `/productspecs-feedback "<text>"` | Process inline feedback text |
| `/productspecs-feedback <file.md>` | Process feedback from file |
| `/productspecs-feedback resume PSF-NNN` | Resume failed/partial implementation |
| `/productspecs-feedback validate PSF-NNN` | Run validation on implemented feedback |
| `/productspecs-feedback status` | Show current feedback processing status |
| `/productspecs-feedback list` | List all registered feedback items |

---

## Prerequisites

1. **ProductSpecs Completion**: ProductSpecs generation completed (Checkpoint 8 passed)
2. **Folder Structure**: `ProductSpecs_<SystemName>/` folder exists with:
   - `01-modules/*.md` (Module specifications)
   - `02-api/*.md` (API/backend modules)
   - `03-tests/*.json` (Test specifications)
   - `04-jira/` (JIRA export files)
   - `_registry/*.json` (Registries)
   - `traceability/*.json` (Traceability chains)

---

## Skills Used

These skills are invoked automatically during workflow execution:

1. **Shared_FeedbackImpactAnalyzer_Reflexion**: Phase 2 - Impact analysis with critical self-assessment
2. **Shared_FeedbackPlanGenerator_Reflexion**: Phase 5 - Plan generation with X/10 scoring
3. **Shared_FeedbackReviewer_Reflexion**: Phase 7 - Multi-perspective validation

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│           PRODUCTSPECS FEEDBACK WORKFLOW (v2.0.0)               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: Input Collection                                      │
│  ├── Receive feedback (text/file)                              │
│  ├── Identify target ProductSpecs                              │
│  └── Collect metadata (source, date, priority)                 │
│                                                                 │
│  Phase 2: Impact Analysis (REFLEXION)                           │
│  ├── Scan modules, requirements, NFRs, tests, JIRA            │
│  ├── Trace hierarchical chains (MOD → REQ → TEST → JIRA)      │
│  ├── Assess JIRA regeneration impact                           │
│  ├── Generate before/after content previews                    │
│  └── Self-Critique: Completeness, Accuracy, Downstream         │
│      → Confidence Level: HIGH (85%+) | MEDIUM (60-84%) | LOW (<60%) │
│                                                                 │
│  Phase 3: Registration                                          │
│  ├── Assign unique ID (PSF-NNN)                                │
│  ├── Create session folder                                     │
│  ├── Save FEEDBACK_ORIGINAL.md, impact_analysis.md            │
│  └── Log to productspecs_feedback_registry.json               │
│                                                                 │
│  Phase 4: Approval Gate (ASKUSERQUESTION)                       │
│  ├── Present impact summary with reflexion context            │
│  ├── Show JIRA regeneration impact                             │
│  └── Options: Approve | Reject | Modify Scope | Request Deeper Analysis │
│                                                                 │
│  Phase 5: Implementation Planning (REFLEXION)                   │
│  ├── Generate 2-3 plan options with scoring                   │
│  ├── Each option: Steps, Effort, Risk, JIRA Impact, X/10 score │
│  └── User selects via AskUserQuestion                          │
│                                                                 │
│  Phase 6: Implementation                                        │
│  ├── Execute plan steps sequentially                           │
│  ├── Update registries (requirements, nfrs, modules, tests)   │
│  ├── Regenerate JIRA export if needed                          │
│  ├── Handle partial failures (resumable checkpoints)          │
│  └── Log all changes to implementation_log.md                 │
│                                                                 │
│  Phase 7: Validation (REFLEXION)                                │
│  ├── Verify plan compliance (100% steps executed)             │
│  ├── Check registry integrity (valid JSON, no duplicates)     │
│  ├── Validate traceability chains (P0 = 100%)                 │
│  ├── Confirm JIRA sync (export matches registries)            │
│  └── Multi-Perspective Review: Requirements, Architecture, Quality │
│      → Consensus Score: 0-10 (PASS ≥ 7.0)                      │
│                                                                 │
│  Phase 8: Completion                                            │
│  ├── Generate FEEDBACK_SUMMARY.md                             │
│  ├── Update registry status → "closed"                         │
│  └── Display completion summary with confidence metrics        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase-by-Phase Procedures

### Phase 1: Input Collection

```bash
# Parse arguments
IF $ARGUMENTS contains "resume":
   GOTO Resume Mode (see Resume Capability section)

IF $ARGUMENTS contains "status":
   GOTO Status Mode (see Status Mode section)

IF $ARGUMENTS contains "list":
   GOTO List Mode (see List Mode section)

# Input source detection
IF feedback provided as inline text:
   feedback_content = $ARGUMENTS
   source = "inline"

ELIF feedback provided as file path:
   READ file at $ARGUMENTS
   feedback_content = file_contents
   source = file_path

ELSE:
   # Interactive mode
   PROMPT: "Please describe your feedback or change request:"
   feedback_content = user_input
   source = "interactive"

# Metadata collection via AskUserQuestion
USE AskUserQuestion:
   question: "What is the source of this feedback?"
   header: "Source"
   multiSelect: false
   options:
     - label: "Product Manager"
       description: "Feedback from product management team"
     - label: "Engineering Team"
       description: "Feedback from developers or architects"
     - label: "QA Team"
       description: "Feedback from quality assurance"
     - label: "Stakeholder"
       description: "Feedback from business stakeholders"
     - label: "User Testing"
       description: "Feedback from user testing sessions"

STORE feedback_source

USE AskUserQuestion:
   question: "What is the priority level for this feedback?"
   header: "Priority"
   multiSelect: false
   options:
     - label: "Critical (Recommended for Blockers)"
       description: "Blocking issue - must fix immediately"
     - label: "High"
       description: "Important change - should address soon"
     - label: "Medium (Recommended for Enhancements)"
       description: "Moderate importance - address in current sprint"
     - label: "Low"
       description: "Nice-to-have - can defer if needed"

STORE feedback_priority

# Identify target ProductSpecs
SEARCH for ProductSpecs_* folders in project root

IF no ProductSpecs folders found:
   ❌ ERROR: "No ProductSpecs found. Run /productspecs first."
   EXIT

IF multiple ProductSpecs folders found:
   USE AskUserQuestion:
      question: "Multiple ProductSpecs found. Which system does this feedback apply to?"
      header: "System"
      multiSelect: false
      options: [List each ProductSpecs_* as option]

   STORE selected_system
ELSE:
   selected_system = single ProductSpecs folder

SET PRODUCTSPECS_DIR = "ProductSpecs_{selected_system}/"
EXTRACT system_name from folder name
```

---

### Phase 2: Impact Analysis (REFLEXION)

**Purpose**: Identify all affected artifacts across ProductSpecs layers with critical self-assessment.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 2: IMPACT ANALYSIS (REFLEXION-ENHANCED)
═══════════════════════════════════════════════════════════════

STEP 1: INVOKE SHARED IMPACT ANALYZER

Skill({
  skill: "Shared_FeedbackImpactAnalyzer_Reflexion",
  args: JSON.stringify({
    feedback_content: feedback_content,
    stage: "productspecs",
    system_name: system_name,
    stage_folder: PRODUCTSPECS_DIR
  })
})

# The skill performs:
# 1. Parse feedback for artifact mentions (MOD-XXX-XXX-NN, REQ-XXX, NFR-XXX, TST-XXX)
# 2. Scan all ProductSpecs artifacts:
#    - 01-modules/*.md (Module specs)
#    - 02-api/*.md (API/backend specs)
#    - 03-tests/*.json (Test cases)
#    - 04-jira/* (JIRA exports)
#    - _registry/*.json (Registries)
#    - traceability/*.json (Chains)
# 3. Match feedback to artifacts (exact ID, title similarity, keyword match)
# 4. Trace traceability chains:
#    - Backwards: MOD → REQ → JTBD → PP
#    - Forwards: MOD → TEST → JIRA
# 5. Build hierarchical chains with before/after content
# 6. Assess JIRA regeneration impact
# 7. Reflexion self-critique (Completeness, Accuracy, Downstream)
# 8. Calculate confidence score (0-100%)

READ impact_analysis.md output from skill

EXTRACT from impact_analysis.md:
- chains_affected (number)
- artifacts_affected (number)
- change_types (CREATE, MODIFY, DELETE counts)
- confidence_level (HIGH, MEDIUM, LOW)
- confidence_percentage (0-100)
- jira_regeneration_required (boolean)
- jira_items_affected (number)
- reflexion_warnings (list)
- reflexion_recommendations (list)

STEP 2: GENERATE 4-LAYER IMPACT SUMMARY

## 4-Layer Impact Summary

| Layer | Artifacts Affected | Details |
|-------|-------------------|---------|
| 1. Requirements | {X} | {requirements.json entries, nfrs.json entries} |
| 2. Modules | {Y} | {UI modules (01-modules/*.md), API modules (02-api/*.md)} |
| 3. Tests | {Z} | {Unit tests, Integration tests, E2E tests (03-tests/*.json)} |
| 4. JIRA Export | {J} | {JIRA tickets in 04-jira/*, regeneration required: YES/NO} |
| **TOTAL** | **{N}** | - |

STEP 3: DISPLAY HIERARCHICAL CHAINS

For each chain in impact_analysis.md:

### Chain N: ROOT → NODE1 → NODE2 → ... → LEAF

├─ **{ARTIFACT_ID}**: "{Title}"
│  └─ Change: {CREATE|MODIFY|DELETE} - {Description}
│     File: {file_path}:{line_range}
│     Before:
│     ```
│     {content_snippet_before}
│     ```
│     After:
│     ```
│     {expected_content_after}
│     ```
│     Reasoning: {Why this change addresses feedback}
│     Complexity: {SIMPLE|MODERATE|COMPLEX}
│
├─ **{NEXT_ARTIFACT_ID}**: "{Title}"
│  └─ Change: ...
│
└─ **{LEAF_ARTIFACT_ID}**: "{Title}"
   └─ Change: ...

STEP 4: JIRA REGENERATION IMPACT ASSESSMENT

IF jira_regeneration_required == true:

   ═══════════════════════════════════════════════════════════════
   📋 JIRA REGENERATION IMPACT
   ═══════════════════════════════════════════════════════════════

   Affected JIRA Items: {jira_items_affected}

   JIRA Files to Regenerate:
   - 04-jira/EPIC_*.md ({N} epics)
   - 04-jira/STORY_*.md ({M} stories)
   - 04-jira/TASK_*.md ({K} tasks)

   Regeneration Scope:
   - Full: All JIRA items regenerated from scratch
   - Partial: Only affected epics/stories/tasks regenerated

   Timeline Impact: {estimate based on jira_items_affected}
   - < 10 items: Low (< 5 minutes)
   - 10-50 items: Medium (5-15 minutes)
   - > 50 items: High (15+ minutes)

   Risk Assessment:
   - Traceability chain breaks: {YES/NO}
   - Manual JIRA sync required: {YES/NO}
   - Existing JIRA tickets impacted: {YES/NO}

   ═══════════════════════════════════════════════════════════════

STEP 5: DISPLAY REFLEXION CRITIQUE

READ reflexion section from impact_analysis.md

DISPLAY:

═══════════════════════════════════════════════════════════════
🤔 REFLEXION SELF-CRITIQUE
═══════════════════════════════════════════════════════════════

Completeness Check: {✓ Complete | ⚠ Possibly incomplete | ❌ Gaps found}
Reasoning: {detailed reasoning from reflexion}
Missing: {list any potentially missed artifacts}

Accuracy Check: {✓ Accurate | ⚠ Minor issues | ❌ Major issues}
Reasoning: {detailed reasoning from reflexion}
Issues: {list any inaccuracies}

Downstream Impact: {✓ All impacts identified | ⚠ Possible additional | ❌ Missed major impacts}
Reasoning: {detailed reasoning from reflexion}
Additional: {list any additional impacts}

Risk Assessment:
- Traceability chain breaks: {Y/N} - {Details}
- Regression risk: {LOW|MEDIUM|HIGH} - {Why}
- Timeline impact: {None|Sprint|Release} - {Reasoning}
- Breaking changes: {Y/N} - {What breaks}

SEVERITY: {CRITICAL|HIGH|MEDIUM|LOW}
MITIGATION: {Recommended mitigations}

Confidence Level: {HIGH|MEDIUM|LOW} ({percentage}%)
Reasoning: {Detailed explanation of confidence level}

Warnings:
{List each warning from reflexion}

Recommendations:
{List each recommendation from reflexion}

═══════════════════════════════════════════════════════════════

PROCEED to Phase 3: Registration
```

**Example Output (Phase 2)**:

```markdown
═══════════════════════════════════════════════════════════════
⏳ PHASE 2: IMPACT ANALYSIS (REFLEXION-ENHANCED)
═══════════════════════════════════════════════════════════════

## 4-Layer Impact Summary

| Layer | Artifacts Affected | Details |
|-------|-------------------|---------|
| 1. Requirements | 3 | requirements.json (REQ-008, REQ-015, REQ-022) |
| 2. Modules | 2 | MOD-INV-UI-02 (Scanning Interface), MOD-INV-API-03 (Barcode Service) |
| 3. Tests | 5 | Unit: 2, Integration: 2, E2E: 1 |
| 4. JIRA Export | 8 | 2 Epics, 4 Stories, 2 Tasks (regeneration required: YES) |
| **TOTAL** | **18** | - |

## Hierarchical Traceability Chains Affected

### Chain 1: REQ-008 → MOD-INV-UI-02 → TST-UI-008-1 → JIRA STORY-012

├─ **REQ-008**: "Scanner shall support barcode and QR code formats"
│  └─ Change: MODIFY - Add NFC tag support to acceptance criteria
│     File: _registry/requirements.json:45-52
│     Before:
│     ```json
│     "acceptance_criteria": [
│       "Supports Code 128 barcodes",
│       "Supports QR codes",
│       "Scan success rate > 95%"
│     ]
│     ```
│     After:
│     ```json
│     "acceptance_criteria": [
│       "Supports Code 128 barcodes",
│       "Supports QR codes",
│       "Supports NFC tag reading",
│       "Scan success rate > 95%"
│     ]
│     ```
│     Reasoning: Feedback explicitly requests NFC support
│     Complexity: MODERATE
│
├─ **MOD-INV-UI-02**: "Scanning Interface Module"
│  └─ Change: MODIFY - Add NFC scan mode and related UI components
│     File: 01-modules/MOD-INV-UI-02-Scanning-Interface.md:120-145
│     Before: Single scan mode (barcode/QR)
│     After: Multi-mode scan (barcode/QR/NFC) with mode selector
│     Sections: components[], states[], data_requirements[], acceptance_criteria[]
│     Reasoning: Module must implement the new requirement
│     Complexity: COMPLEX
│
├─ **TST-UI-008-1**: "Barcode scanning test suite"
│  └─ Change: MODIFY - Add NFC scanning test cases
│     File: 03-tests/ui-tests.json:230-245
│     Before: 3 test cases (barcode, QR, error handling)
│     After: 5 test cases (add NFC success, NFC error)
│     Reasoning: New functionality requires test coverage
│
└─ **JIRA STORY-012**: "Implement barcode scanning"
   └─ Change: MODIFY - Update story acceptance criteria and sub-tasks
      File: 04-jira/STORY_012_Implement_Barcode_Scanning.md
      Before: Story covers barcode + QR only
      After: Story covers barcode + QR + NFC
      Reasoning: JIRA ticket must reflect updated requirements

### Chain 2: REQ-015 → MOD-INV-API-03 → TST-API-015-1 → JIRA TASK-043

(Similar structure for Chain 2...)

═══════════════════════════════════════════════════════════════
📋 JIRA REGENERATION IMPACT
═══════════════════════════════════════════════════════════════

Affected JIRA Items: 8

JIRA Files to Regenerate:
- 04-jira/EPIC_002_Inventory_Scanning.md
- 04-jira/EPIC_005_Barcode_Management.md
- 04-jira/STORY_012_Implement_Barcode_Scanning.md
- 04-jira/STORY_015_Barcode_API.md
- 04-jira/STORY_018_NFC_Support.md (NEW)
- 04-jira/TASK_043_Scanner_Component.md
- 04-jira/TASK_044_Barcode_Service.md
- 04-jira/TASK_051_NFC_Driver.md (NEW)

Regeneration Scope: Partial (8 items only)

Timeline Impact: Medium (5-10 minutes)

Risk Assessment:
- Traceability chain breaks: NO - All chains remain intact
- Manual JIRA sync required: YES - If existing tickets exist in JIRA system
- Existing JIRA tickets impacted: YES - STORY-012, STORY-015 descriptions will change

═══════════════════════════════════════════════════════════════
🤔 REFLEXION SELF-CRITIQUE
═══════════════════════════════════════════════════════════════

Completeness Check: ✓ COMPLETE

Re-scanned with terms: ["NFC", "tag", "RFID", "contactless", "reader"]
- Found all primary references (REQ-008, REQ-015, MOD-INV-UI-02, MOD-INV-API-03)
- Checked for orphaned references: None found
- Verified all traceability chains complete (2 chains, 8 artifacts total)

Reasoning: Comprehensive scan found all artifacts directly and indirectly affected by NFC addition. No orphaned references detected in registries or JIRA exports.

Accuracy Check: ✓ ACCURATE

- All MODIFY artifacts verified to exist at specified paths
- Before/after content matches current file states
- JSON schema consistency validated (requirements.json, tests.json)
- Module spec format compliance verified

Reasoning: All artifact paths validated. Content snippets match current files. Proposed changes maintain schema consistency.

Downstream Impact: ⚠ POSSIBLE ADDITIONAL

Checked downstream:
- Test coverage: Existing (needs expansion for NFC)
- JIRA export: Existing (regeneration required)

**Potential additional impacts**:
- Hardware compatibility documentation may need updates
- User training materials may need NFC instructions
- Privacy/security review may be needed for NFC data handling

Reasoning: While primary technical artifacts identified, supporting documentation (hardware specs, training, security) may need updates. Flagged for consideration during planning.

Risk Assessment:
- **Traceability chain breaks**: NO - All chains remain intact after changes
- **Regression risk**: MEDIUM - New NFC mode may interfere with existing barcode/QR modes if not properly isolated
- **Timeline impact**: Sprint-level - Moderate effort, can fit in current sprint with proper planning
- **Breaking changes**: NO - Backward compatible (additive change)

**SEVERITY**: MEDIUM
**MITIGATION**:
- Implement feature flag for NFC mode to allow gradual rollout
- Add integration tests covering all scan modes (barcode, QR, NFC)
- Conduct regression testing on existing barcode/QR functionality
- Plan hardware compatibility testing with NFC-enabled devices

Confidence Level: HIGH (88%)

Reasoning:
- Completeness: Thorough multi-pass scan found all direct and indirect impacts (✓) → +40 points
- Accuracy: All artifact paths validated, content verified, schema checked (✓) → +35 points
- Downstream: Primary impacts identified, secondary impacts flagged (⚠) → +15 points
- Total: 90 points, reduced to 88% due to potential documentation and security review needs

Warnings:
- Hardware compatibility implications not fully explored
- Security/privacy review may uncover additional requirements
- User training materials need assessment

Recommendations:
1. During planning, consult with hardware team on NFC device compatibility
2. Include security specialist to review NFC data handling (PII, encryption)
3. Plan documentation updates (user guide, training materials)
4. Consider feature flag strategy for controlled rollout

═══════════════════════════════════════════════════════════════
```

---

### Phase 3: Registration

**Purpose**: Assign unique ID and create session folder structure.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 3: REGISTRATION
═══════════════════════════════════════════════════════════════

STEP 1: GENERATE FEEDBACK ID

READ {PRODUCTSPECS_DIR}/feedback-sessions/productspecs_feedback_registry.json

IF file does not exist:
   CREATE empty registry:
   {
     "schema_version": "2.0.0",
     "system_name": "{system_name}",
     "stage": "productspecs",
     "feedback_items": {}
   }

EXTRACT existing IDs (PSF-001, PSF-002, ...)
GENERATE next_id = PSF-{max_id + 1} (zero-padded to 3 digits)

STEP 2: CREATE SESSION FOLDER

SET session_date = YYYY-MM-DD
SET session_folder = "{PRODUCTSPECS_DIR}/feedback-sessions/{session_date}_ProductSpecsFeedback-{next_id}/"

CREATE session_folder

STEP 3: SAVE ARTIFACTS

WRITE {session_folder}/FEEDBACK_ORIGINAL.md:
---
feedback_id: {next_id}
created_at: {ISO8601 timestamp}
source: {feedback_source}
priority: {feedback_priority}
---

# Original Feedback - {next_id}

{feedback_content}

COPY impact_analysis.md from Shared_FeedbackImpactAnalyzer_Reflexion output
  TO {session_folder}/impact_analysis.md

STEP 4: UPDATE REGISTRY

ADD to productspecs_feedback_registry.json:

{
  "feedback_items": {
    "{next_id}": {
      "title": "{brief_summary_from_feedback}",
      "type": "{Bug|Enhancement|RequirementChange|PriorityChange|TraceabilityGap}",
      "severity": "{Critical|High|Medium|Low}",
      "status": "analyzing",
      "source": {
        "origin": "{feedback_source}",
        "priority": "{feedback_priority}",
        "submitted_by": "{source person if available}",
        "submitted_at": "{ISO8601 timestamp}"
      },
      "categories": ["{CAT-MOD}", "{CAT-REQ}", ...],
      "impact": {
        "chains_affected": {chains_affected},
        "artifacts_affected": {artifacts_affected},
        "layer_1_requirements": {X},
        "layer_2_modules": {Y},
        "layer_3_tests": {Z},
        "layer_4_jira": {J},
        "jira_regeneration_required": {true|false},
        "jira_items_affected": {number},
        "confidence_level": "{HIGH|MEDIUM|LOW}",
        "confidence_percentage": {0-100},
        "reflexion_score": {confidence_percentage}
      },
      "lifecycle": {
        "created_at": "{ISO8601}",
        "updated_at": "{ISO8601}",
        "phase": "registration",
        "session_folder": "{session_folder}"
      }
    }
  }
}

✅ Registration complete: {next_id}
   Session folder: {session_folder}

PROCEED to Phase 4: Approval Gate
```

---

### Phase 4: Approval Gate (ASKUSERQUESTION)

**Purpose**: Present impact analysis with reflexion context and get user approval.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 4: APPROVAL GATE
═══════════════════════════════════════════════════════════════

STEP 1: PREPARE APPROVAL CONTEXT

READ impact_analysis.md from session folder
EXTRACT:
- impact_summary (artifact counts, layer breakdown)
- reflexion_context (confidence level, warnings, recommendations)
- risk_context (severity, traceability breaks, regression risk)
- jira_impact (regeneration required, items affected, timeline)

STEP 2: PRESENT TO USER VIA ASKUSERQUESTION

USE AskUserQuestion:
   question: "
   ═══════════════════════════════════════════════════════════════
   FEEDBACK IMPACT ANALYSIS: {next_id}
   ═══════════════════════════════════════════════════════════════

   {impact_summary}

   {jira_impact}

   {reflexion_context}

   {risk_context}

   ═══════════════════════════════════════════════════════════════

   Review the detailed impact analysis above. How should we proceed?"

   header: "Approval"
   multiSelect: false
   options:
     - label: "Approve (Recommended)"
       description: "Proceed to implementation planning. JIRA regeneration timeline: {estimate}. Effort will be calculated during option generation with reflexion scoring."
     - label: "Reject"
       description: "Mark feedback as rejected. No changes will be made. Requires rejection reason."
     - label: "Modify Scope"
       description: "Adjust which artifacts/layers to change before proceeding to planning. Allows selective implementation (e.g., skip JIRA regeneration, focus on critical modules only)."
     - label: "Request Deeper Analysis"
       description: "Reflexion confidence is {confidence_level} ({confidence_percentage}%) - request more investigation before deciding. Recommended if confidence < 85% or critical warnings exist."

STORE user_decision

STEP 3: PROCESS DECISION

IF user_decision == "Approve":
   UPDATE registry:
      status = "approved"
      lifecycle.phase = "approval_gate"
      lifecycle.updated_at = NOW()

   ✅ Feedback approved for implementation
   PROCEED to Phase 5: Implementation Planning

ELIF user_decision == "Reject":
   PROMPT: "Please provide a rejection reason:"
   rejection_reason = user_input

   UPDATE registry:
      status = "rejected"
      lifecycle.phase = "approval_gate"
      lifecycle.rejection_reason = rejection_reason
      lifecycle.updated_at = NOW()
      lifecycle.closed_at = NOW()

   WRITE {session_folder}/REJECTION_REASON.md:
   ---
   feedback_id: {next_id}
   rejected_at: {ISO8601}
   rejected_by: User
   ---

   # Rejection Reason

   {rejection_reason}

   ❌ Feedback rejected: {next_id}
   EXIT

ELIF user_decision == "Modify Scope":
   USE AskUserQuestion:
      question: "Which layers should be modified?"
      header: "Scope"
      multiSelect: true
      options:
        - label: "Requirements (Layer 1)"
          description: "Modify requirements.json and nfrs.json"
        - label: "Modules (Layer 2)"
          description: "Modify module specifications (01-modules/, 02-api/)"
        - label: "Tests (Layer 3)"
          description: "Modify test specifications (03-tests/)"
        - label: "JIRA Export (Layer 4)"
          description: "Regenerate JIRA tickets (04-jira/)"

   STORE selected_layers

   # Filter artifacts by selected layers
   FILTER impact_analysis artifacts by selected_layers
   UPDATE registry with filtered scope

   ✅ Scope modified - proceeding with selected layers only
   PROCEED to Phase 5: Implementation Planning

ELIF user_decision == "Request Deeper Analysis":
   PROMPT: "What specific areas should be investigated further?"
   investigation_areas = user_input

   UPDATE registry:
      status = "investigating"
      lifecycle.investigation_request = investigation_areas
      lifecycle.updated_at = NOW()

   # Re-run impact analyzer with focused investigation
   Skill({
     skill: "Shared_FeedbackImpactAnalyzer_Reflexion",
     args: JSON.stringify({
       feedback_content: feedback_content,
       stage: "productspecs",
       system_name: system_name,
       stage_folder: PRODUCTSPECS_DIR,
       investigation_focus: investigation_areas
     })
   })

   ⚠️ Deeper analysis requested - re-running impact analyzer
   GOTO Phase 2 (with investigation focus)
```

---

### Phase 5: Implementation Planning (REFLEXION)

**Purpose**: Generate multiple implementation options with X/10 scoring and get user selection.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 5: IMPLEMENTATION PLANNING (REFLEXION-ENHANCED)
═══════════════════════════════════════════════════════════════

STEP 1: INVOKE SHARED PLAN GENERATOR

Skill({
  skill: "Shared_FeedbackPlanGenerator_Reflexion",
  args: JSON.stringify({
    feedback_id: next_id,
    stage: "productspecs",
    system_name: system_name,
    impact_analysis_path: "{session_folder}/impact_analysis.md",
    session_folder: session_folder
  })
})

# The skill performs:
# 1. Read impact_analysis.md and affected artifacts
# 2. Generate 2-3 implementation options:
#    - Option A: Comprehensive (all layers, full traceability, JIRA regeneration)
#    - Option B: Focused (core changes only, minimal JIRA impact)
#    - Option C: Custom (user-defined)
# 3. For each option:
#    - Define steps with specific file operations
#    - Estimate effort (LOW, MEDIUM, HIGH)
#    - Assess risk (LOW, MEDIUM, HIGH)
#    - Calculate JIRA impact (none, partial, full regeneration)
#    - Specify before/after content for key changes
#    - Score with reflexion (X/10 based on completeness, correctness, risk)
# 4. Recommend best option based on scoring
# 5. Save to implementation_options.md

READ implementation_options.md output from skill

STEP 2: PRESENT OPTIONS VIA ASKUSERQUESTION

DISPLAY implementation_options.md content to user

USE AskUserQuestion:
   question: "
   ═══════════════════════════════════════════════════════════════
   IMPLEMENTATION OPTIONS FOR {next_id}
   ═══════════════════════════════════════════════════════════════

   {Display full implementation_options.md content here}

   ═══════════════════════════════════════════════════════════════

   Which implementation plan should we use for this specification change?"

   header: "Plan"
   multiSelect: false
   options:
     - label: "Plan A: Comprehensive Update (Recommended)" (if score >= 8/10)
       description: "{scope} scope, {N} artifacts affected, {effort} effort, Score: {score}/10"
     - label: "Plan B: Focused Update"
       description: "{scope} scope, {N} artifacts affected, {effort} effort, Score: {score}/10"
     - label: "Plan C: Custom Plan"
       description: "Provide your own implementation plan with specific steps and file changes"

STORE selected_plan

STEP 3: HANDLE CUSTOM PLAN

IF selected_plan == "Plan C":
   PROMPT: "Please provide your custom implementation plan. Include:
   1. List of files to modify
   2. Specific changes for each file
   3. Traceability updates needed
   4. Whether JIRA regeneration is required"

   custom_plan = user_input

   # Parse custom plan and validate
   PARSE custom_plan for:
   - File paths
   - Change descriptions
   - Traceability implications
   - JIRA impact

   VALIDATE:
   - All mentioned files exist
   - Changes align with feedback intent
   - Traceability chains remain intact

   IF validation fails:
      ❌ Custom plan validation failed: {issues}
      PROMPT to revise or select Plan A/B
   ELSE:
      ✅ Custom plan validated
      SAVE custom_plan to implementation_plan.md

ELIF selected_plan == "Plan A" OR selected_plan == "Plan B":
   COPY selected option from implementation_options.md
     TO {session_folder}/implementation_plan.md

UPDATE registry:
   status = "planning_complete"
   lifecycle.phase = "planning"
   lifecycle.selected_plan = "{selected_plan}"
   lifecycle.updated_at = NOW()

✅ Implementation plan finalized: {selected_plan}

PROCEED to Phase 6: Implementation
```

**Example implementation_options.md (generated by Shared_FeedbackPlanGenerator_Reflexion)**:

```markdown
# Implementation Options - PSF-003

## Option A: Comprehensive Update (RECOMMENDED)

**Scope**: Full implementation across all layers
**Reflexion Score**: 9/10

### Steps

1. **Update Requirements** (Layer 1)
   - File: `_registry/requirements.json`
   - Changes:
     - REQ-008: Add NFC support to acceptance criteria (line 45-52)
     - REQ-015: Update barcode service requirements (line 78-85)
     - REQ-022: Add hardware compatibility requirement (NEW)
   - Before/After: See impact_analysis.md Chain 1

2. **Update Module Specifications** (Layer 2)
   - File: `01-modules/MOD-INV-UI-02-Scanning-Interface.md`
   - Changes:
     - Add NFC scan mode to components[] (line 120)
     - Add nfcEnabled to states[] (line 135)
     - Add nfcTagId to data_requirements[] (line 145)
     - Update acceptance criteria (line 200)
   - Before/After: See impact_analysis.md Chain 1

   - File: `02-api/MOD-INV-API-03-Barcode-Service.md`
   - Changes:
     - Add POST /api/scan/nfc endpoint
     - Update data model for NFC tags

3. **Update Test Specifications** (Layer 3)
   - File: `03-tests/ui-tests.json`
   - Changes:
     - Add TST-UI-008-4: NFC scan success test
     - Add TST-UI-008-5: NFC scan error handling test

   - File: `03-tests/integration-tests.json`
   - Changes:
     - Add TST-INT-015-3: NFC-to-barcode service integration test

4. **Update Traceability Registries**
   - File: `traceability/productspecs_traceability_register.json`
   - Changes:
     - Add MOD-INV-UI-02 → TST-UI-008-4 link
     - Add MOD-INV-UI-02 → TST-UI-008-5 link
     - Add MOD-INV-API-03 → TST-INT-015-3 link

5. **Regenerate JIRA Export** (Layer 4)
   - Command: `/productspecs-jira --system {system_name} --scope partial`
   - Scope: 8 items (2 epics, 4 stories, 2 tasks)
   - Files affected:
     - 04-jira/EPIC_002_Inventory_Scanning.md
     - 04-jira/EPIC_005_Barcode_Management.md
     - 04-jira/STORY_012_Implement_Barcode_Scanning.md
     - 04-jira/STORY_015_Barcode_API.md
     - 04-jira/STORY_018_NFC_Support.md (NEW)
     - 04-jira/TASK_043_Scanner_Component.md
     - 04-jira/TASK_044_Barcode_Service.md
     - 04-jira/TASK_051_NFC_Driver.md (NEW)

### Effort Estimate
- **Overall**: MEDIUM
- **Breakdown**:
  - Requirements: LOW (3 JSON edits)
  - Modules: MEDIUM (2 markdown files, substantial changes)
  - Tests: LOW (JSON edits)
  - JIRA: MEDIUM (8 files, partial regeneration)
- **Estimated Time**: 15-20 minutes

### Risk Assessment
- **Overall Risk**: LOW
- **Risks**:
  - Traceability chain breaks: NO (all chains preserved)
  - Regression: MEDIUM (new NFC mode may interfere with existing modes)
  - JIRA sync: LOW (regeneration handles all updates)
- **Mitigation**:
  - Feature flag for NFC mode
  - Integration tests covering all modes
  - Regression testing plan

### JIRA Impact
- **Regeneration**: Partial (8 items)
- **Timeline**: 5-10 minutes
- **Manual sync**: Required if tickets exist in live JIRA instance

### Reflexion Scoring Breakdown
- **Completeness** (40%): 10/10 - All affected artifacts addressed
- **Correctness** (35%): 9/10 - Changes align with feedback, minor risk of mode interference
- **Risk Management** (25%): 8/10 - Mitigation strategies provided, JIRA sync manual step
- **Overall**: 9.1/10 → **9/10**

---

## Option B: Focused Update

**Scope**: Core changes only (skip JIRA regeneration)
**Reflexion Score**: 6/10

### Steps

1. **Update Requirements** (Layer 1) - Same as Option A
2. **Update Module Specifications** (Layer 2) - Same as Option A
3. **Update Test Specifications** (Layer 3) - Same as Option A
4. **Update Traceability Registries** - Same as Option A
5. **Skip JIRA Regeneration** - Manual JIRA updates required later

### Effort Estimate
- **Overall**: LOW
- **Estimated Time**: 10-12 minutes (saves JIRA regeneration time)

### Risk Assessment
- **Overall Risk**: MEDIUM
- **Risks**:
  - JIRA out of sync: HIGH (tickets will not reflect new requirements)
  - Traceability incomplete: MEDIUM (JIRA links missing)
- **Mitigation**:
  - Document JIRA updates needed
  - Schedule manual JIRA sync

### JIRA Impact
- **Regeneration**: None (deferred)
- **Manual Updates Required**: 8 tickets

### Reflexion Scoring Breakdown
- **Completeness** (40%): 5/10 - Missing JIRA layer
- **Correctness** (35%): 9/10 - Core changes correct
- **Risk Management** (25%): 5/10 - High JIRA sync risk
- **Overall**: 6.3/10 → **6/10**

**Recommendation**: Only use if JIRA updates can be deferred. Option A is strongly recommended.

---

## Option C: Custom Plan

Provide your own implementation plan. Must include:
- List of files to modify
- Specific changes for each file
- Traceability updates
- JIRA regeneration decision
```

---

### Phase 6: Implementation

**Purpose**: Execute the selected implementation plan with resumable checkpoints.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 6: IMPLEMENTATION
═══════════════════════════════════════════════════════════════

STEP 1: INITIALIZE IMPLEMENTATION LOG

WRITE {session_folder}/implementation_log.md:
# Implementation Log - {next_id}

Plan: {selected_plan}
Started: {ISO8601 timestamp}

## Steps

UPDATE registry:
   status = "implementing"
   lifecycle.phase = "implementation"
   lifecycle.implementation_started_at = NOW()
   lifecycle.updated_at = NOW()

STEP 2: EXECUTE PLAN STEPS

READ implementation_plan.md
PARSE steps from plan

FOR each step IN steps:
   step_number = index + 1

   APPEND to implementation_log.md:
   ### Step {step_number}: {step.title}
   Started: {timestamp}

   TRY:
      # Execute step based on type

      IF step.type == "update_requirements":
         READ {PRODUCTSPECS_DIR}/_registry/requirements.json
         APPLY changes from step.changes
         WRITE updated requirements.json

      ELIF step.type == "update_nfrs":
         READ {PRODUCTSPECS_DIR}/_registry/nfrs.json
         APPLY changes from step.changes
         WRITE updated nfrs.json

      ELIF step.type == "update_module_spec":
         READ {step.file_path}
         APPLY changes from step.changes
         WRITE updated module spec

      ELIF step.type == "update_test_spec":
         READ {PRODUCTSPECS_DIR}/03-tests/{step.file}
         APPLY changes from step.changes
         WRITE updated test spec

      ELIF step.type == "update_traceability":
         READ {PRODUCTSPECS_DIR}/traceability/productspecs_traceability_register.json
         ADD links from step.links
         WRITE updated traceability

      ELIF step.type == "regenerate_jira":
         IF step.scope == "partial":
            # Partial regeneration (specific items)
            Skill({
              skill: "ProductSpecs_JiraExporter",
              args: JSON.stringify({
                system_name: system_name,
                scope: "partial",
                items: step.jira_items
              })
            })
         ELIF step.scope == "full":
            # Full regeneration
            bash .claude/commands/productspecs-jira.md --system {system_name}

      # Log version history
      python3 .claude/hooks/version_history_logger.py \
        "traceability/" \
        "{system_name}" \
        "productspecs" \
        "Claude" \
        "{version}" \
        "Feedback {next_id}: {step.title}" \
        "{artifact_ids_comma_separated}" \
        "{file_path}" \
        "modification"

      APPEND to implementation_log.md:
      Status: ✅ SUCCESS
      Completed: {timestamp}
      Files modified: {list files}

      UPDATE registry:
         lifecycle.last_completed_step = step_number
         lifecycle.updated_at = NOW()

   CATCH error:
      APPEND to implementation_log.md:
      Status: ❌ FAILED
      Error: {error.message}
      Failed at: {timestamp}

      UPDATE registry:
         status = "failed"
         lifecycle.phase = "implementation"
         lifecycle.failed_step = step_number
         lifecycle.error = error.message
         lifecycle.resume_point = step_number
         lifecycle.updated_at = NOW()

      ❌ Implementation failed at step {step_number}
      ERROR: {error.message}

      USE AskUserQuestion:
         question: "Implementation failed at step {step_number}: {step.title}. How should we proceed?"
         header: "Failure"
         multiSelect: false
         options:
           - label: "Retry Step"
             description: "Retry the failed step immediately"
           - label: "Skip Step"
             description: "Skip this step and continue (may break traceability)"
           - label: "Abort"
             description: "Stop implementation, save resume point for later"
           - label: "Debug"
             description: "Investigate the error before deciding"

      STORE failure_action

      IF failure_action == "Retry Step":
         RETRY current step (max 2 retries)
      ELIF failure_action == "Skip Step":
         LOG skip to FAILURES_LOG.md
         CONTINUE to next step
      ELIF failure_action == "Abort":
         ⚠️ Implementation aborted - resume point saved
         EXIT
      ELIF failure_action == "Debug":
         DISPLAY error details, file paths, stack trace
         GOTO failure_action prompt (allow retry/skip/abort after debug)

STEP 3: GENERATE FILES CHANGED REPORT

WRITE {session_folder}/files_changed.md:
# Files Changed - {next_id}

## Summary
- Total files modified: {N}
- Requirements updated: {X}
- Modules updated: {Y}
- Tests updated: {Z}
- JIRA files regenerated: {J}

## Detailed Changes

{For each file modified, list:}
### {file_path}
- Change type: {MODIFY|CREATE|DELETE}
- Lines affected: {line_range}
- Artifact IDs: {list IDs}
- Summary: {brief description}

UPDATE registry:
   status = "implemented"
   lifecycle.phase = "implementation"
   lifecycle.implementation_completed_at = NOW()
   lifecycle.updated_at = NOW()

✅ Implementation complete - all steps executed

PROCEED to Phase 7: Validation
```

---

### Phase 7: Validation (REFLEXION)

**Purpose**: Verify implementation correctness with multi-perspective review.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 7: VALIDATION (REFLEXION-ENHANCED)
═══════════════════════════════════════════════════════════════

STEP 1: INVOKE SHARED REVIEWER

Skill({
  skill: "Shared_FeedbackReviewer_Reflexion",
  args: JSON.stringify({
    feedback_id: next_id,
    stage: "productspecs",
    system_name: system_name,
    session_folder: session_folder,
    implementation_plan_path: "{session_folder}/implementation_plan.md",
    files_changed_path: "{session_folder}/files_changed.md"
  })
})

# The skill performs:
# 1. Read implementation_plan.md and files_changed.md
# 2. Verify plan compliance (all steps executed)
# 3. Check registry integrity:
#    - Valid JSON syntax
#    - No duplicate IDs
#    - Schema compliance
#    - Version increments
# 4. Validate traceability chains:
#    - All chains intact (no broken links)
#    - P0 coverage = 100%
#    - New artifacts properly linked
# 5. Validate JIRA sync:
#    - JIRA files match registry data
#    - All affected tickets updated
#    - Traceability to JIRA intact
# 6. Multi-perspective review:
#    - Requirements Validator: Check requirements alignment
#    - Architecture Validator: Check module consistency
#    - Quality Validator: Check test coverage
# 7. Calculate consensus score (0-10)
# 8. Generate VALIDATION_REPORT.md

READ VALIDATION_REPORT.md output from skill

STEP 2: DISPLAY VALIDATION RESULTS

DISPLAY VALIDATION_REPORT.md content

EXTRACT from VALIDATION_REPORT.md:
- validation_passed (boolean)
- plan_compliance (percentage)
- registry_integrity (PASS/FAIL)
- traceability_valid (boolean)
- jira_sync_valid (boolean)
- consensus_score (0-10)
- critical_issues (list)
- warnings (list)

IF validation_passed == true AND consensus_score >= 7.0:
   ✅ VALIDATION PASSED
   Consensus Score: {consensus_score}/10

   UPDATE registry:
      status = "validated"
      lifecycle.phase = "validation"
      lifecycle.validation_passed = true
      lifecycle.validation_score = consensus_score
      lifecycle.updated_at = NOW()

   PROCEED to Phase 8: Completion

ELSE:
   ❌ VALIDATION FAILED
   Consensus Score: {consensus_score}/10

   DISPLAY critical_issues and warnings

   USE AskUserQuestion:
      question: "Validation failed with score {consensus_score}/10. How should we proceed?"
      header: "Validation"
      multiSelect: false
      options:
        - label: "Fix Issues"
          description: "Review validation report and fix critical issues before re-validating"
        - label: "Accept Anyway"
          description: "Accept implementation despite validation failures (not recommended)"
        - label: "Re-Implement"
          description: "Revert changes and re-run implementation with corrected plan"

   STORE validation_action

   IF validation_action == "Fix Issues":
      DISPLAY fix instructions from VALIDATION_REPORT.md
      PROMPT user to make manual fixes
      WAIT for user confirmation
      RETRY validation (GOTO STEP 1)

   ELIF validation_action == "Accept Anyway":
      ⚠️ Validation bypassed - proceeding with warnings
      UPDATE registry:
         status = "validated_with_warnings"
         lifecycle.validation_bypassed = true
         lifecycle.validation_warnings = warnings
      PROCEED to Phase 8: Completion

   ELIF validation_action == "Re-Implement":
      UPDATE registry:
         status = "re_implementing"
         lifecycle.phase = "implementation"
      GOTO Phase 6: Implementation
```

**Example VALIDATION_REPORT.md (generated by Shared_FeedbackReviewer_Reflexion)**:

```markdown
# Validation Report - PSF-003

**Generated**: 2026-01-25 15:45:00
**Feedback ID**: PSF-003
**Plan**: Option A (Comprehensive Update)

---

## Executive Summary

✅ **VALIDATION PASSED**
**Consensus Score**: 8.5/10 (PASS - threshold: 7.0)

- Plan Compliance: 100% (5/5 steps completed)
- Registry Integrity: PASS
- Traceability Valid: YES (all chains intact)
- JIRA Sync Valid: YES (8/8 items updated)

---

## Plan Compliance Check

### Steps Executed: 5/5 (100%)

| Step | Title | Status | Files Modified |
|------|-------|--------|----------------|
| 1 | Update Requirements | ✅ | requirements.json |
| 2 | Update Module Specifications | ✅ | MOD-INV-UI-02.md, MOD-INV-API-03.md |
| 3 | Update Test Specifications | ✅ | ui-tests.json, integration-tests.json |
| 4 | Update Traceability Registries | ✅ | productspecs_traceability_register.json |
| 5 | Regenerate JIRA Export | ✅ | 8 JIRA files (2 epics, 4 stories, 2 tasks) |

**Result**: ✅ PASS - All planned steps executed successfully

---

## Registry Integrity Check

### requirements.json
- **Syntax**: ✅ Valid JSON
- **Schema**: ✅ Compliant
- **Duplicates**: ✅ None found
- **Version**: ✅ Incremented (1.2.0 → 1.3.0)
- **New/Modified**: REQ-008 (modified), REQ-015 (modified), REQ-022 (created)

### nfrs.json
- **Syntax**: ✅ Valid JSON
- **Schema**: ✅ Compliant
- **Duplicates**: ✅ None found
- **Version**: ✅ Incremented (1.1.0 → 1.2.0)

### productspecs_traceability_register.json
- **Syntax**: ✅ Valid JSON
- **Schema**: ✅ Compliant
- **Links Added**: 3 (MOD-INV-UI-02 → TST-UI-008-4, MOD-INV-UI-02 → TST-UI-008-5, MOD-INV-API-03 → TST-INT-015-3)
- **Orphaned Links**: ✅ None

**Result**: ✅ PASS - All registries valid

---

## Traceability Chain Validation

### Chain 1: REQ-008 → MOD-INV-UI-02 → TST-UI-008-1,4,5 → JIRA STORY-012
- **Status**: ✅ INTACT
- **Links**: 6/6 valid
- **Coverage**: P0 = 100%

### Chain 2: REQ-015 → MOD-INV-API-03 → TST-API-015-1,3 → JIRA TASK-043,044
- **Status**: ✅ INTACT
- **Links**: 5/5 valid
- **Coverage**: P0 = 100%

### Chain 3: REQ-022 (NEW) → MOD-INV-UI-02 → TST-UI-008-4 → JIRA STORY-018 (NEW)
- **Status**: ✅ INTACT
- **Links**: 4/4 valid
- **Coverage**: P0 = 100%

**Result**: ✅ PASS - All traceability chains intact, P0 coverage = 100%

---

## JIRA Sync Validation

### JIRA Files Updated: 8/8

| File | Status | Traceability |
|------|--------|--------------|
| EPIC_002_Inventory_Scanning.md | ✅ Updated | Links to STORY-012, STORY-018 |
| EPIC_005_Barcode_Management.md | ✅ Updated | Links to TASK-043, TASK-044 |
| STORY_012_Implement_Barcode_Scanning.md | ✅ Updated | REQ-008 referenced |
| STORY_015_Barcode_API.md | ✅ Updated | REQ-015 referenced |
| STORY_018_NFC_Support.md | ✅ Created | REQ-022 referenced |
| TASK_043_Scanner_Component.md | ✅ Updated | MOD-INV-UI-02 referenced |
| TASK_044_Barcode_Service.md | ✅ Updated | MOD-INV-API-03 referenced |
| TASK_051_NFC_Driver.md | ✅ Created | MOD-INV-API-03 referenced |

**Result**: ✅ PASS - All JIRA files match registry data

---

## Multi-Perspective Review

### Requirements Validator (Perspective 1)

**Focus**: Requirements alignment and acceptance criteria completeness

✅ **PASS** (Score: 9/10)

**Findings**:
- REQ-008 acceptance criteria properly updated to include NFC
- REQ-015 correctly modified for barcode service API changes
- REQ-022 appropriately added for hardware compatibility
- All requirements have proper traceability to modules and tests

**Minor Issue**:
- REQ-022 could benefit from more specific hardware models (e.g., "NFC reader: XYZ-1000") (-1)

**Recommendation**: Add hardware compatibility matrix in future revision

---

### Architecture Validator (Perspective 2)

**Focus**: Module specification consistency and design coherence

✅ **PASS** (Score: 8/10)

**Findings**:
- MOD-INV-UI-02 properly extended with NFC scan mode
- MOD-INV-API-03 correctly updated with NFC endpoint
- Component hierarchy maintained (no breaking changes)
- Data models consistent across UI and API

**Minor Issues**:
- NFC mode integration with existing barcode/QR modes not explicitly documented (-1)
- Error handling for NFC failures could be more detailed (-1)

**Recommendation**: Add sequence diagram showing NFC scan flow

---

### Quality Validator (Perspective 3)

**Focus**: Test coverage and quality assurance

✅ **PASS** (Score: 8.5/10)

**Findings**:
- New test cases added for NFC functionality (TST-UI-008-4, TST-UI-008-5, TST-INT-015-3)
- Integration test covers NFC-to-barcode service flow
- Error handling test cases included
- Test traceability properly linked to modules

**Minor Issue**:
- No regression test explicitly checking barcode/QR modes still work after NFC addition (-0.5)
- Performance test for NFC scan latency missing (-1)

**Recommendation**: Add regression test suite and performance benchmarks

---

## Consensus Scoring

| Validator | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Requirements | 9/10 | 40% | 3.6 |
| Architecture | 8/10 | 35% | 2.8 |
| Quality | 8.5/10 | 25% | 2.125 |
| **TOTAL** | **8.5/10** | - | - |

**Threshold**: 7.0/10
**Result**: ✅ PASS (8.5 ≥ 7.0)

---

## Issues and Warnings

### Critical Issues
None

### Warnings
1. ⚠️ REQ-022 lacks specific hardware model compatibility details
2. ⚠️ NFC mode integration with existing modes not documented
3. ⚠️ No explicit regression test for barcode/QR modes post-NFC
4. ⚠️ Performance benchmarks for NFC scan latency missing

### Recommendations
1. Add hardware compatibility matrix document
2. Create sequence diagram for multi-mode scan flow
3. Add regression test suite (TST-UI-008-REGRESSION)
4. Add performance test case (TST-PERF-008-NFC)

---

## Final Verdict

✅ **VALIDATION PASSED**

**Consensus Score**: 8.5/10 (PASS)
**Critical Issues**: 0
**Warnings**: 4 (non-blocking)

All core requirements met. Warnings are recommendations for future improvement and do not block closure.

---

**Validated by**: Shared_FeedbackReviewer_Reflexion
**Timestamp**: 2026-01-25 15:45:00
```

---

### Phase 8: Completion

**Purpose**: Finalize feedback processing and close the session.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 8: COMPLETION
═══════════════════════════════════════════════════════════════

STEP 1: GENERATE FEEDBACK SUMMARY

WRITE {session_folder}/FEEDBACK_SUMMARY.md:
---
feedback_id: {next_id}
status: validated
closed_at: {ISO8601 timestamp}
---

# Feedback Summary - {next_id}

## Original Feedback

{feedback_content}

## Impact Analysis Summary

- Chains Affected: {chains_affected}
- Artifacts Affected: {artifacts_affected}
- Requirements: {X} modified
- Modules: {Y} modified
- Tests: {Z} modified
- JIRA: {J} regenerated
- Confidence Level: {confidence_level} ({confidence_percentage}%)

## Implementation Summary

- Plan Selected: {selected_plan}
- Steps Executed: {total_steps} / {total_steps}
- Files Modified: {total_files}
- Implementation Time: {duration}

## Validation Summary

- Validation Status: PASSED
- Consensus Score: {consensus_score}/10
- Critical Issues: {critical_count}
- Warnings: {warning_count}

## Files Modified

{List all files from files_changed.md}

## Traceability Impact

{List affected traceability chains}

## JIRA Impact

- Regeneration: {yes/no}
- Items Affected: {jira_items_affected}
- Files Regenerated: {list JIRA files}

## Reflexion Insights

**Confidence Metrics**:
- Impact Analysis: {confidence_percentage}%
- Validation Score: {consensus_score}/10

**Key Recommendations**:
{List reflexion recommendations from impact and validation}

---

**Session Folder**: {session_folder}
**Completed**: {ISO8601 timestamp}

STEP 2: UPDATE REGISTRY

UPDATE productspecs_feedback_registry.json:
   {
      "{next_id}": {
         "status": "closed",
         "lifecycle": {
            ...existing lifecycle fields,
            "closed_at": "{ISO8601}",
            "total_duration_seconds": {duration},
            "validation_score": {consensus_score},
            "files_modified": {total_files}
         }
      }
   }

STEP 3: DISPLAY COMPLETION SUMMARY

═══════════════════════════════════════════════════════════════
✅ FEEDBACK PROCESSING COMPLETE: {next_id}
═══════════════════════════════════════════════════════════════

Status: CLOSED
Validation: PASSED ({consensus_score}/10)

Impact:
├─ Requirements: {X} modified
├─ Modules: {Y} modified
├─ Tests: {Z} modified
└─ JIRA: {J} items regenerated

Files Modified: {total_files}
Duration: {duration}

Session Folder: {session_folder}
Summary: {session_folder}/FEEDBACK_SUMMARY.md

═══════════════════════════════════════════════════════════════

DONE
```

---

## Resume Capability

If implementation fails or is interrupted, resume from the last checkpoint:

```bash
/productspecs-feedback resume PSF-003
```

**Resume Procedure**:

```bash
STEP 1: LOAD FEEDBACK SESSION

READ ProductSpecs_{system_name}/feedback-sessions/productspecs_feedback_registry.json
EXTRACT entry for PSF-{id}

IF status == "closed" OR status == "validated":
   ⚠️ Feedback {id} already completed
   EXIT

IF status == "failed" OR status == "implementing":
   EXTRACT resume_point (step number)
   EXTRACT failed_step (if applicable)

   READ {session_folder}/implementation_plan.md
   READ {session_folder}/implementation_log.md

   ✅ Resume point found: Step {resume_point}

STEP 2: VERIFY PREVIOUS STEPS

FOR each step FROM 1 TO resume_point - 1:
   VERIFY step completion in implementation_log.md
   CHECK file modifications applied

   IF any step incomplete:
      ❌ Resume aborted - previous steps incomplete
      PROMPT to restart from Phase 6

STEP 3: RESUME IMPLEMENTATION

✅ Previous steps verified - resuming from step {resume_point}

GOTO Phase 6: Implementation (at step {resume_point})
```

---

## Status Mode

Check current feedback processing status:

```bash
/productspecs-feedback status
```

**Status Output**:

```bash
READ ProductSpecs_{system_name}/feedback-sessions/productspecs_feedback_registry.json

FIND most recent feedback with status != "closed"

IF found:
   EXTRACT:
   - feedback_id
   - status
   - lifecycle.phase
   - lifecycle.last_completed_step
   - lifecycle.updated_at

   DISPLAY:
   ═══════════════════════════════════════════════════════════════
   PRODUCTSPECS FEEDBACK STATUS
   ═══════════════════════════════════════════════════════════════

   Active Feedback: {feedback_id}
   Status: {status}
   Phase: {phase_number} ({phase_name})
   Last Activity: {ISO8601}

   {If phase == "implementation":}
   Progress: Step {last_completed_step} / {total_steps}

   {If status == "failed":}
   ⚠️ Failed at step {failed_step}: {error}
   Resume with: /productspecs-feedback resume {feedback_id}

   ═══════════════════════════════════════════════════════════════
ELSE:
   ✅ No active feedback processing
```

---

## List Mode

List all registered feedback items:

```bash
/productspecs-feedback list
```

**List Output**:

```bash
READ ProductSpecs_{system_name}/feedback-sessions/productspecs_feedback_registry.json

EXTRACT all feedback_items

DISPLAY:
═══════════════════════════════════════════════════════════════
PRODUCTSPECS FEEDBACK REGISTRY
═══════════════════════════════════════════════════════════════

System: {system_name}
Total Feedback Items: {count}

ID       Status      Type              Severity  Created      Updated
-------  ----------  ----------------  --------  -----------  -----------
PSF-001  closed      RequirementChange  High     2025-12-20   2025-12-20
PSF-002  validated   Enhancement        Medium   2025-12-21   2025-12-21
PSF-003  in_progress Bug                Critical 2025-12-22   2025-12-22
PSF-004  failed      TraceabilityGap    Medium   2025-12-23   2025-12-23

Legend:
- closed: Fully implemented and validated
- validated: Implementation validated, pending closure
- in_progress: Currently implementing
- failed: Implementation failed, needs resume
- rejected: User rejected during approval gate
- analyzing: Impact analysis in progress

═══════════════════════════════════════════════════════════════

USE AskUserQuestion:
   question: "Would you like to view details for a specific feedback item?"
   header: "Details"
   multiSelect: false
   options:
     - label: "No"
       description: "Exit list mode"
     - label: "Yes - Specify ID"
       description: "View detailed information for a feedback item"

IF selected == "Yes - Specify ID":
   PROMPT: "Enter feedback ID (e.g., PSF-003):"
   feedback_id = user_input

   READ {session_folder for feedback_id}/FEEDBACK_SUMMARY.md
   DISPLAY summary
```

---

## Feedback Types

| Type | Code | Description | Typical Artifacts Affected |
|------|------|-------------|----------------------------|
| **Bug** | BUG | Error in specification or inconsistency | Requirements, Modules, Tests |
| **Enhancement** | ENH | Improvement to existing specification | Modules, Tests, JIRA |
| **RequirementChange** | REQ | Change to functional/non-functional requirement | Requirements, Modules, Tests, JIRA |
| **PriorityChange** | PRI | Change requirement or module priority level | Requirements, JIRA |
| **TraceabilityGap** | TRC | Missing traceability link or broken chain | Traceability registries, JIRA |
| **NewFeature** | NEW | Entirely new feature not in original scope | Requirements, Modules, Tests, JIRA |

---

## Impact Categories

| Category | Code | Artifacts | Files |
|----------|------|-----------|-------|
| **Requirements** | CAT-REQ | Requirements, NFRs | _registry/requirements.json, _registry/nfrs.json |
| **Modules** | CAT-MOD | UI/API module specs | 01-modules/*.md, 02-api/*.md |
| **Tests** | CAT-TEST | Unit, Integration, E2E tests | 03-tests/*.json |
| **JIRA** | CAT-JIRA | Epics, Stories, Tasks | 04-jira/*.md |
| **Traceability** | CAT-TRACE | Traceability links | traceability/*.json |
| **Registry** | CAT-REG | Registry files | _registry/*.json |

---

## Session Folder Structure

```
ProductSpecs_<SystemName>/feedback-sessions/
├── productspecs_feedback_registry.json
└── <YYYY-MM-DD>_ProductSpecsFeedback-<ID>/
    ├── FEEDBACK_ORIGINAL.md              # Original feedback text
    ├── impact_analysis.md                # Reflexion-enhanced impact analysis
    ├── implementation_options.md         # Generated plan options with X/10 scoring
    ├── implementation_plan.md            # Selected implementation plan
    ├── implementation_log.md             # Step-by-step execution log
    ├── files_changed.md                  # Detailed file change report
    ├── VALIDATION_REPORT.md              # Multi-perspective validation results
    └── FEEDBACK_SUMMARY.md               # Final completion summary
```

---

## Registry Schema

```json
{
  "schema_version": "2.0.0",
  "system_name": "{PRODUCTSPECS_NAME}",
  "stage": "productspecs",
  "feedback_items": {
    "PSF-001": {
      "title": "{brief_summary}",
      "type": "{Bug|Enhancement|RequirementChange|PriorityChange|TraceabilityGap|NewFeature}",
      "severity": "{Critical|High|Medium|Low}",
      "status": "{analyzing|approved|planning_complete|implementing|implemented|validated|validated_with_warnings|closed|rejected|failed}",
      "source": {
        "origin": "{Product Manager|Engineering Team|QA Team|Stakeholder|User Testing}",
        "priority": "{Critical|High|Medium|Low}",
        "submitted_by": "{name}",
        "submitted_at": "{ISO8601}"
      },
      "categories": ["{CAT-REQ}", "{CAT-MOD}", "{CAT-TEST}", "{CAT-JIRA}", "{CAT-TRACE}"],
      "impact": {
        "chains_affected": N,
        "artifacts_affected": M,
        "layer_1_requirements": X,
        "layer_2_modules": Y,
        "layer_3_tests": Z,
        "layer_4_jira": J,
        "jira_regeneration_required": true|false,
        "jira_items_affected": K,
        "confidence_level": "{HIGH|MEDIUM|LOW}",
        "confidence_percentage": 0-100,
        "reflexion_score": {confidence_percentage}
      },
      "lifecycle": {
        "created_at": "{ISO8601}",
        "updated_at": "{ISO8601}",
        "approved_at": "{ISO8601}",
        "implementation_started_at": "{ISO8601}",
        "implementation_completed_at": "{ISO8601}",
        "validation_passed": true|false,
        "validation_score": 0-10,
        "validation_bypassed": true|false,
        "closed_at": "{ISO8601}",
        "phase": "{input_collection|impact_analysis|registration|approval_gate|planning|implementation|validation|completion}",
        "selected_plan": "{Plan A|Plan B|Plan C}",
        "last_completed_step": N,
        "failed_step": N,
        "resume_point": N,
        "error": "{error_message}",
        "session_folder": "{path}",
        "files_modified": N,
        "total_duration_seconds": N
      }
    }
  }
}
```

---

## Error Handling

| Error | Action |
|-------|--------|
| No ProductSpecs found | ❌ Show error, suggest running `/productspecs` |
| Registry corrupt | Attempt recovery, create new if needed |
| Multiple ProductSpecs found | Use AskUserQuestion to select target system |
| Implementation step fails | Save resume point, offer Retry/Skip/Abort via AskUserQuestion |
| Validation fails | Display issues, offer Fix/Accept/Re-Implement via AskUserQuestion |
| JIRA regeneration fails | Log to FAILURES_LOG.md, mark JIRA validation as failed, continue |
| File not found during implementation | Log skip to implementation_log.md, mark step as failed |
| JSON parse error in registry | ❌ BLOCK - registry must be manually fixed before proceeding |

---

## Integration with Other Stages

Changes to ProductSpecs may propagate to downstream stages:

```
ProductSpecs Change
       ↓
   [Impact Analysis]
       ↓
┌──────┴──────┐
│             │
↓             ↓
Upstream?     Downstream?
(Discovery,   (JIRA,
 Prototype)   Implementation)
       ↓             ↓
 [Flag for      [Automatic
  manual        regeneration
  review]       if possible]
```

### Upstream Impact (Discovery/Prototype)
If feedback affects upstream artifacts (Pain Points, JTBD, Screens, Components), the system **flags this for manual review** but does **not automatically modify** those stages. Use `/discovery-feedback` or `/prototype-feedback` instead.

### Downstream Impact (Implementation)
If Implementation stage exists and references affected modules:
- **Implementation tasks may become outdated**
- **Test implementations may need updates**
- The system **logs warnings** in VALIDATION_REPORT.md
- Use `/htec-sdd-changerequest` to propagate changes to implementation

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/productspecs` | Generate ProductSpecs from Prototype outputs |
| `/productspecs-status` | Show ProductSpecs generation progress |
| `/productspecs-jira` | Regenerate JIRA export only |
| `/discovery-feedback` | Process feedback on Discovery artifacts |
| `/prototype-feedback` | Process feedback on Prototype artifacts |
| `/htec-sdd-changerequest` | Process change requests on Implementation |

---

## Examples

### Example 1: Process Inline Feedback

```bash
/productspecs-feedback "The search requirement REQ-001 should include fuzzy matching with configurable threshold"
```

**Output**:
```
⏳ PHASE 1: INPUT COLLECTION
✅ Feedback received (inline text)
   Source: Product Manager
   Priority: Medium

⏳ PHASE 2: IMPACT ANALYSIS (REFLEXION-ENHANCED)
✅ Impact analysis complete
   Artifacts affected: 7 (1 requirement, 2 modules, 3 tests, 1 JIRA)
   Confidence: HIGH (91%)

⏳ PHASE 3: REGISTRATION
✅ Feedback registered: PSF-005

⏳ PHASE 4: APPROVAL GATE
[Displays impact summary with reflexion context]
User approves

⏳ PHASE 5: IMPLEMENTATION PLANNING (REFLEXION-ENHANCED)
[Generates 3 plan options]
User selects Plan A (Comprehensive Update, Score: 9/10)

⏳ PHASE 6: IMPLEMENTATION
✅ Step 1: Update Requirements (REQ-001) - SUCCESS
✅ Step 2: Update Module Spec (MOD-SRC-UI-01) - SUCCESS
✅ Step 3: Update Module Spec (MOD-SRC-API-02) - SUCCESS
✅ Step 4: Update Test Specs - SUCCESS
✅ Step 5: Update Traceability - SUCCESS
✅ Step 6: Regenerate JIRA (3 items) - SUCCESS

⏳ PHASE 7: VALIDATION (REFLEXION-ENHANCED)
✅ Validation passed
   Consensus Score: 8.7/10
   Warnings: 2 (non-blocking)

⏳ PHASE 8: COMPLETION
✅ FEEDBACK PROCESSING COMPLETE: PSF-005
   Files Modified: 9
   Duration: 18 minutes
```

---

### Example 2: Process Feedback from File

```bash
/productspecs-feedback feedback/nfc_support_request.md
```

**(nfc_support_request.md content)**:
```markdown
# NFC Support Request

## Summary
Add NFC tag reading support to the barcode scanning module.

## Requirements
- REQ-008 should include NFC support
- Scanner UI should have NFC mode selector
- Barcode service API should handle NFC tags

## Priority: High
## Source: Product Manager
```

**Output**: (Similar to Example 1 with file source)

---

### Example 3: Resume Failed Implementation

```bash
/productspecs-feedback list

# Output shows PSF-003 status: failed

/productspecs-feedback resume PSF-003
```

**Output**:
```
⏳ RESUMING FEEDBACK: PSF-003
✅ Previous steps verified: Steps 1-3 completed
⏳ Resuming from Step 4: Update Traceability Registries

⏳ PHASE 6: IMPLEMENTATION (RESUMED)
✅ Step 4: Update Traceability Registries - SUCCESS
✅ Step 5: Regenerate JIRA Export - SUCCESS

⏳ PHASE 7: VALIDATION (REFLEXION-ENHANCED)
✅ Validation passed (Score: 8.3/10)

⏳ PHASE 8: COMPLETION
✅ FEEDBACK PROCESSING COMPLETE: PSF-003
```

---

### Example 4: Check Status

```bash
/productspecs-feedback status
```

**Output**:
```
═══════════════════════════════════════════════════════════════
PRODUCTSPECS FEEDBACK STATUS
═══════════════════════════════════════════════════════════════

Active Feedback: PSF-006
Status: implementing
Phase: 6 (Implementation)
Progress: Step 3 / 5
Last Activity: 2025-12-22 14:32:15

Current Step: Update Module Specifications
Estimated Completion: 5 minutes

═══════════════════════════════════════════════════════════════
```

---

### Example 5: List All Feedback

```bash
/productspecs-feedback list
```

**Output**:
```
═══════════════════════════════════════════════════════════════
PRODUCTSPECS FEEDBACK REGISTRY
═══════════════════════════════════════════════════════════════

System: InventorySystem
Total Feedback Items: 6

ID       Status      Type              Severity  Created      Updated
-------  ----------  ----------------  --------  -----------  -----------
PSF-001  closed      RequirementChange  High     2025-12-20   2025-12-20
PSF-002  closed      Enhancement        Medium   2025-12-21   2025-12-21
PSF-003  closed      Bug                Critical 2025-12-22   2025-12-22
PSF-004  failed      TraceabilityGap    Medium   2025-12-23   2025-12-23
PSF-005  validated   NewFeature         High     2025-12-24   2025-12-24
PSF-006  implementing RequirementChange Medium   2025-12-24   2025-12-24

Legend:
- closed: Fully implemented and validated
- validated: Implementation validated, pending closure
- implementing: Currently in progress
- failed: Needs resume (use: /productspecs-feedback resume PSF-004)

═══════════════════════════════════════════════════════════════
```

---

## Reflexion Integration Summary

This command integrates reflexion at **3 critical phases**:

### Phase 2: Impact Analysis
- **Skill**: Shared_FeedbackImpactAnalyzer_Reflexion
- **Self-Assessment**: Completeness, Accuracy, Downstream Impact
- **Output**: Confidence Level (HIGH/MEDIUM/LOW), Confidence Percentage (0-100%)
- **Purpose**: Ensure all affected artifacts identified before approval

### Phase 5: Implementation Planning
- **Skill**: Shared_FeedbackPlanGenerator_Reflexion
- **Self-Assessment**: Completeness, Correctness, Risk Management
- **Output**: X/10 Score per option (recommend ≥ 8/10)
- **Purpose**: Generate high-quality implementation plans with justified scoring

### Phase 7: Validation
- **Skill**: Shared_FeedbackReviewer_Reflexion
- **Multi-Perspective Review**: Requirements, Architecture, Quality validators
- **Output**: Consensus Score 0-10 (PASS ≥ 7.0)
- **Purpose**: Verify implementation correctness from multiple angles

---

## Success Criteria

Feedback processing is considered successful when:

1. ✅ **Impact Analysis**: Confidence ≥ 85% (HIGH) OR user accepts MEDIUM/LOW with justification
2. ✅ **Approval Gate**: User explicitly approves (not rejected or deferred)
3. ✅ **Implementation**: All plan steps executed successfully (100% completion)
4. ✅ **Validation**: Consensus Score ≥ 7.0/10 (PASS)
5. ✅ **Traceability**: All chains intact, P0 coverage = 100%
6. ✅ **JIRA Sync**: If regeneration required, all affected items updated

---

**END OF COMMAND**
