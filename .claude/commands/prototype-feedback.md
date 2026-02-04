---
name: prototype-feedback
description: Process feedback on Prototype with systematic debugging and reflexion-enhanced change management
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
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-feedback started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: |
            SYSTEM_NAME=$(cat _state/session.json 2>/dev/null | grep -o '"project"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"project"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//' || echo "")
            if [ -n "$SYSTEM_NAME" ] && [ "$SYSTEM_NAME" != "pending" ]; then
              uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_prototype_output.py" --system-name "$SYSTEM_NAME" --quick
            else
              echo '{"result": "skip", "reason": "System name not found in session"}'
              exit 0
            fi
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-feedback ended '{"stage": "prototype"}'
---

# /prototype-feedback - Process Prototype Feedback with Reflexion

**Version**: 2.0.0 (Reflexion-Enhanced)
**Template**: `.claude/templates/feedback-workflow-template.md`

## Purpose

Process feedback on Prototype artifacts with:
- **5-layer impact analysis** (Discovery → Specs → Code → Registries → Matrices)
- **Systematic debugging** for bugs before planning
- **Reflexion-enhanced planning** with scored options
- **Multi-perspective validation** with consensus scoring
- **Complete traceability** maintained across all layers

---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-feedback instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

## CRITICAL: COMPREHENSIVE 5-LAYER TRACEABILITY

> **IRON LAW**: Every feedback implementation MUST update ALL affected artifact layers.
> Missing layers = incomplete implementation = validation failure.

### Artifact Layers (ALL MUST BE CONSIDERED)

| Layer | Location | Key Files |
|-------|----------|-----------|
| **1. Discovery** | `ClientAnalysis_*/` | `screen-definitions.md`, `navigation-structure.md`, `data-fields.md`, `JOBS_TO_BE_DONE.md` |
| **2. Prototype Specs** | `Prototype_*/` | `01-components/`, `02-screens/`, `03-interactions/`, `04-implementation/` |
| **3. Code** | `prototype/src/` | `screens/`, `components/`, `data/`, `App.tsx` |
| **4. Registries** | ROOT level | `traceability/screen_registry.json`, `traceability/prototype_traceability_register.json` |
| **5. Matrices** | `helperFiles/` | `TRACEABILITY_MATRIX_MASTER.md`, `TRACEABILITY_ASSESSMENT_REPORT.md` |

### Layer Update Requirements by Feedback Type

| Feedback Type | Discovery | Specs | Code | Registries | Matrices |
|---------------|-----------|-------|------|------------|----------|
| **NewFeature** | Required | Required | Required | ALWAYS | Required |
| **Enhancement** | Depends | Required | Required | ALWAYS | Depends |
| **Bug** | Rarely | Depends | Required | ALWAYS | Rarely |
| **UXIssue** | Depends | Likely | Likely | ALWAYS | Rarely |
| **VisualIssue** | No | Likely | Likely | ALWAYS | No |

**Note**: Registries (Layer 4) are ALWAYS required for ALL feedback types.

---

## Arguments

- `$ARGUMENTS` - Optional: Feedback content or special commands
  - If no argument: Interactive mode prompts for feedback input
  - If text: Use as direct feedback content
  - If file path (.md/.txt): Read feedback from file
  - If `resume PF-<NNN>`: Resume failed/partial implementation
  - If `status`: Show current feedback processing status
  - If `list`: Show all registered feedback items

---

## Prerequisites

- Completed prototype exists in `Prototype_<SystemName>/`
- Dependencies installed (`/htec-libraries-init`)
- State files accessible (`_state/`, `traceability/`)

---

## Shared Skills (Reflexion-Enhanced)

These skills are shared across ALL feedback commands:

1. **Shared_FeedbackImpactAnalyzer_Reflexion** (`.claude/skills/Shared_FeedbackImpactAnalyzer_Reflexion/SKILL.md`)
   - Scans artifacts and builds hierarchical traceability chains
   - Self-critique with 4 critical questions
   - Confidence scoring (LOW/MEDIUM/HIGH with percentage)

2. **Shared_FeedbackPlanGenerator_Reflexion** (`.claude/skills/Shared_FeedbackPlanGenerator_Reflexion/SKILL.md`)
   - Generates 2-3 implementation options
   - Reflexion evaluation per option (X/10 scores)
   - Detailed before/after content for every step

3. **Shared_FeedbackReviewer_Reflexion** (`.claude/skills/Shared_FeedbackReviewer_Reflexion/SKILL.md`)
   - Multi-perspective validation (Requirements, Architecture, Quality)
   - Consensus scoring with confidence level
   - Actionable recommendations (PASS/CONDITIONAL PASS/FAIL)

---

## 8-Phase Workflow

### Phase 1: Input Collection

**STEP 1: PARSE ARGUMENTS**

```bash
IF "$ARGUMENTS" == "resume PF-<NNN>":
   JUMP to Resume Mode (see bottom of doc)
   EXIT Phase 1

IF "$ARGUMENTS" == "status":
   CALL show_status_mode()
   EXIT

IF "$ARGUMENTS" == "list":
   CALL show_list_mode()
   EXIT

IF "$ARGUMENTS" is file path (.md or .txt):
   READ file content
   STORE as feedback_content

ELIF "$ARGUMENTS" is non-empty text:
   STORE $ARGUMENTS as feedback_content

ELSE:
   PROMPT: "Enter feedback or describe the change needed:"
   STORE input as feedback_content
```

**STEP 2: IDENTIFY TARGET PROTOTYPE**

```bash
LIST available prototypes:
   ls -d Prototype_*/

IF count == 0:
   ERROR: "No prototype found. Run /prototype first."
   EXIT

IF count == 1:
   STORE as PROTOTYPE_NAME (without Prototype_ prefix)

ELIF count > 1:
   USE AskUserQuestion:
      question: "Which prototype does this feedback apply to?"
      header: "Target"
      options:
         [One option per prototype folder]

   STORE selected as PROTOTYPE_NAME
```

**STEP 3: COLLECT METADATA**

```bash
PROMPT: "Who is the source of this feedback? (Name/Role)"
STORE as source_person

PROMPT: "Who is entering this feedback? (Your name)"
STORE as inputter

RECORD:
   created_at = TODAY (YYYY-MM-DD)
   created_time = NOW (HH:MM:SS)
```

---

### Phase 2: Impact Analysis (REFLEXION ENHANCED)

**STEP 1: READ SKILL**

```bash
READ: .claude/skills/Shared_FeedbackImpactAnalyzer_Reflexion/SKILL.md
```

**STEP 2: CLASSIFY FEEDBACK**

```bash
ANALYZE feedback_content for keywords:

Type Classification:
   IF contains ["bug", "broken", "error", "doesn't work", "not working"]:
      type = "Bug"
   ELIF contains ["new feature", "add", "should have"]:
      type = "NewFeature"
   ELIF contains ["improve", "enhance", "better"]:
      type = "Enhancement"
   ELIF contains ["UX", "usability", "confusing", "hard to"]:
      type = "UXIssue"
   ELIF contains ["color", "spacing", "font", "visual", "looks"]:
      type = "VisualIssue"
   ELSE:
      type = "Clarification"

Severity Classification:
   IF type == "Bug" AND ["broken", "error", "crash"]:
      severity = "Critical"
   ELIF type == "Bug" OR type == "UXIssue":
      severity = "High"
   ELIF type == "NewFeature":
      severity = "Medium"
   ELSE:
      severity = "Low"
```

**STEP 3: BUG-SPECIFIC DEBUGGING (MANDATORY FOR BUGS)**

```bash
IF type == "Bug":

   ═══════════════════════════════════════════════════════════════
   🐛 BUG DETECTED - SYSTEMATIC DEBUGGING REQUIRED
   ═══════════════════════════════════════════════════════════════

   STEP 3A: GATHER REPRODUCTION STEPS

      ASK user:
         "What are the exact steps to reproduce this bug?"

      RECORD as reproduction_steps[]

   STEP 3B: TRACE DATA FLOW

      IDENTIFY symptom:
         - What component/screen shows the bug?
         - What action triggers it?
         - What is the expected vs. actual behavior?

      SEARCH CODE:
         - Find affected screen in prototype/src/screens/
         - Find affected component in prototype/src/components/
         - Trace event handlers
         - Trace state management
         - Trace data flow (API → Component → UI)

      BUILD TRACE CHAIN:
         User Action → Event Handler → State Update → Data Flow → Rendering

   STEP 3C: FORM HYPOTHESIS

      Based on trace chain, propose root cause:
         hypothesis = "The bug occurs because {root_cause}"

      Evidence:
         - Code location: {file}:{line}
         - Mechanism: {how_bug_happens}

   STEP 3D: CONFIRM HYPOTHESIS

      PRESENT to user:
         "Root Cause Hypothesis: {hypothesis}"
         "Evidence: {evidence}"

      ASK: "Does this match your understanding of the bug?"

      IF no:
         RE-INVESTIGATE
         RETURN to STEP 3B

   STEP 3E: SAVE DEBUGGING EVIDENCE

      CREATE: debugging_evidence.md
      - Reproduction steps
      - Trace chain
      - Root cause hypothesis
      - Evidence references

   ═══════════════════════════════════════════════════════════════

ENDIF
```

**STEP 4: INVOKE SHARED IMPACT ANALYZER**

```bash
INVOKE Shared_FeedbackImpactAnalyzer_Reflexion:

   inputs:
      feedback_content: {feedback_content}
      stage: "prototype"
      system_name: {PROTOTYPE_NAME}
      stage_folder: "Prototype_{PROTOTYPE_NAME}/"

   PROTOTYPE-SPECIFIC SCANNING:

      Layer 1: Discovery Artifacts (ClientAnalysis_{PROTOTYPE_NAME}/)
         SCAN:
            - 04-design-specs/screen-definitions.md
            - 04-design-specs/navigation-structure.md
            - 04-design-specs/data-fields.md
            - 04-design-specs/interaction-patterns.md
            - 04-design-specs/ui-components.md
            - 02-research/JOBS_TO_BE_DONE.md

         IDENTIFY affected screens, components, data fields
         EXTRACT discovery_screen_ids[]

      Layer 2: Prototype Specifications (Prototype_{PROTOTYPE_NAME}/)
         SCAN:
            - 01-components/component-index.md
            - 01-components/{category}/{component}/spec.md
            - 02-screens/screen-index.md
            - 02-screens/{platform}/{screen}/spec.md
            - 03-interactions/motion-system.md
            - 03-interactions/accessibility-spec.md
            - 03-interactions/responsive-behavior.md
            - 04-implementation/data-model.md
            - 04-implementation/api-contracts.json
            - 04-implementation/test-data/*.json

         IDENTIFY affected component specs, screen specs, data models

      Layer 3: Code (prototype/src/)
         SCAN:
            - src/screens/{platform}/{screen}.tsx
            - src/components/{category}/{component}.tsx
            - src/data/*.json
            - src/contexts/*.tsx
            - src/App.tsx

         IDENTIFY affected code files
         FOR Bug types:
            CROSS-REFERENCE with debugging_evidence.md

      Layer 4: Registries (ROOT level)
         SCAN:
            - traceability/screen_registry.json
            - traceability/prototype_traceability_register.json
            - traceability/discovery_traceability_register.json (if discovery affected)
            - _state/requirements_registry.json

         IDENTIFY affected registry entries
         CHECK feedback_source fields

      Layer 5: Matrices (helperFiles/)
         SCAN:
            - helperFiles/TRACEABILITY_MATRIX_MASTER.md
            - helperFiles/TRACEABILITY_ASSESSMENT_REPORT.md

         IDENTIFY trace chains to update
         CHECK coverage percentages

   BUILD HIERARCHICAL CHAINS:

      Example Chain Format:
      ═════════════════════════════════════════════════════════════
      Chain 1: JTBD-2.1 → REQ-015 → SCR-003 → COMP-INV-TABLE → CODE-src/components/InventoryTable.tsx

      ├─ **JTBD-2.1**: "View real-time inventory status"
      │  └─ Change: MODIFY - Update success criteria for color coding
      │     File: `ClientAnalysis_{PROTOTYPE_NAME}/02-research/JOBS_TO_BE_DONE.md`
      │     Section: success_criteria
      │     Before:
      │     ```yaml
      │     success_criteria:
      │       - "User can view stock levels in table"
      │     ```
      │     After:
      │     ```yaml
      │     success_criteria:
      │       - "User can view stock levels with color indicators (red=low, green=sufficient)"
      │     ```
      │     Reasoning: Feedback requires color coding feature
      │
      ├─ **REQ-015**: "Inventory table display"
      │  └─ Change: MODIFY - Add acceptance criterion for color coding
      │     File: `_state/requirements_registry.json`
      │     Section: acceptance_criteria
      │     Before: 3 criteria
      │     After: 4 criteria + color coding requirement
      │
      ├─ **SCR-003**: "Inventory Dashboard Screen"
      │  └─ Change: MODIFY - Add color coding to table component
      │     File: `Prototype_{PROTOTYPE_NAME}/02-screens/desktop/inventory-dashboard/spec.md`
      │     Section: components
      │
      ├─ **COMP-INV-TABLE**: "InventoryTable Component"
      │  └─ Change: MODIFY - Add stockLevelColor variant
      │     File: `Prototype_{PROTOTYPE_NAME}/01-components/data-display/inventory-table/spec.md`
      │     Section: variants
      │     Before:
      │     ```yaml
      │     variants:
      │       size: [compact, standard, expanded]
      │     ```
      │     After:
      │     ```yaml
      │     variants:
      │       size: [compact, standard, expanded]
      │       stockIndicator: [none, color, badge]
      │     ```
      │
      └─ **CODE**: `src/components/InventoryTable.tsx`
         └─ Change: MODIFY - Implement color coding logic
            File: `prototype/src/components/InventoryTable.tsx`
            Lines: 45-60
            Before:
            ```tsx
            <td>{item.stockLevel}</td>
            ```
            After:
            ```tsx
            <td style={{
              color: item.stockLevel < threshold ? 'red' : 'green'
            }}>
              {item.stockLevel}
            </td>
            ```

      ═════════════════════════════════════════════════════════════

   REFLEXION SELF-CRITIQUE:

      Question 1: Completeness - "Are these ALL affected artifacts?"

         Re-scan with alternative terms: ["stock", "inventory level", "table color"]
         Check orphaned references
         Verify chain completeness

         RESULT: ✓ Complete | ⚠ Possibly incomplete | ❌ Gaps found
         REASONING: [Explain findings]
         MISSING: [List any potentially missed artifacts]

      Question 2: Accuracy - "Are change types correct?"

         For each artifact:
            ✓ If MODIFY: Verify artifact exists at specified path
            ✓ If DELETE: Verify artifact exists and deletion is appropriate
            ✓ If CREATE: Verify artifact doesn't already exist

         Check before/after content:
            ✓ Before content matches current file state?
            ✓ After content addresses feedback intent?
            ✓ Changes maintain format/schema consistency?

         RESULT: ✓ Accurate | ⚠ Minor issues | ❌ Major issues
         REASONING: [Explain findings]
         ISSUES: [List any inaccuracies]

      Question 3: Downstream Impact - "Any cascading effects missed?"

         CHECK CODE DEPENDENCIES:
            - Search for imports of affected components
            - Check parent screens using affected components
            - Verify test files for affected code

         CHECK DATA DEPENDENCIES:
            - data-model.md affects api-contracts.json
            - api-contracts.json affects test-data/*.json
            - test-data/*.json affects code

         CHECK TRACEABILITY:
            - Implementation_* folder for related tasks
            - ProductSpecs_* folder for module specs
            - SolArch_* folder for ADRs

         RESULT: ✓ All impacts identified | ⚠ Possible additional | ❌ Missed major impacts
         REASONING: [Explain findings]
         ADDITIONAL: [List any additional impacts]

      Question 4: Risk Assessment

         IDENTIFY risks:
            - Traceability chain breaks: [Y/N] - [Details]
            - Build failures: [Y/N] - [Why]
            - Visual regression: [Y/N] - [What might break]
            - Regression risk: [LOW|MEDIUM|HIGH] - [Reasoning]
            - Breaking changes: [Y/N] - [What breaks]

         SEVERITY: [CRITICAL|HIGH|MEDIUM|LOW]
         MITIGATION: [Recommended mitigations]

   CALCULATE Confidence Level:

      confidence_score = 0

      IF completeness == "✓": confidence_score += 40
      ELIF completeness == "⚠": confidence_score += 25
      ELSE: confidence_score += 10

      IF accuracy == "✓": confidence_score += 35
      ELIF accuracy == "⚠": confidence_score += 20
      ELSE: confidence_score += 5

      IF downstream == "✓": confidence_score += 25
      ELIF downstream == "⚠": confidence_score += 15
      ELSE: confidence_score += 5

      confidence_level =
         IF confidence_score >= 85: "HIGH"
         ELIF confidence_score >= 60: "MEDIUM"
         ELSE: "LOW"

      confidence_percentage = confidence_score

   returns:
      impact_analysis_path: "feedback-sessions/{date}_PrototypeFeedback-{ID}/impact_analysis.md"
      summary: {
         chains_affected: N,
         artifacts_affected: M,
         layer_1_discovery: X,
         layer_2_specs: Y,
         layer_3_code: Z,
         layer_4_registries: R,
         layer_5_matrices: T,
         confidence_level: "HIGH|MEDIUM|LOW",
         confidence_percentage: XX
      }
```

**STEP 5: CATEGORIZE IMPACT**

```bash
ASSIGN categories based on affected layers:

   - CAT-DISC - Discovery materials affected (Layer 1)
   - CAT-COMP - Component specifications affected (Layer 2)
   - CAT-SCR - Screen specifications affected (Layer 2)
   - CAT-DATA - Data model/API contracts affected (Layer 2)
   - CAT-CODE - Prototype code affected (Layer 3)
   - CAT-STYLE - Design tokens/styles affected (Layer 2)
   - CAT-TEST - Test data affected (Layer 2)
   - CAT-REG - Registries affected (Layer 4 - ALWAYS present)
   - CAT-MATRIX - Matrices affected (Layer 5)
```

**STEP 6: CREATE SESSION FOLDER**

```bash
CREATE: Prototype_{PROTOTYPE_NAME}/feedback-sessions/<YYYY-MM-DD>_PrototypeFeedback-<TEMP>/
```

**STEP 7: SAVE PHASE 2 OUTPUTS**

```bash
WRITE to session folder:

   1. FEEDBACK_ORIGINAL.md:
      ---
      document_id: PF-TEMP
      version: 1.0.0
      created_at: {YYYY-MM-DD}
      feedback_type: {type}
      severity: {severity}
      source_person: {name}
      inputter: {inputter}
      ---

      # Original Feedback

      {feedback_content}

   2. impact_analysis.md:
      [Full output from Shared_FeedbackImpactAnalyzer_Reflexion]

   3. debugging_evidence.md (IF type == "Bug"):
      [From STEP 3 bug debugging]
```

**STEP 8: DISPLAY IMPACT ANALYSIS TO USER**

```bash
OUTPUT:
═══════════════════════════════════════════════════════════════
 IMPACT ANALYSIS - PF-TEMP (Pending Registration)
═══════════════════════════════════════════════════════════════

Feedback Type: {type}
Severity: {severity}
Categories: {categories}

## 5-Layer Impact Summary

| Layer | Artifacts Affected | Details |
|-------|-------------------|---------|
| 1. Discovery | {X} | {screen-definitions.md, data-fields.md, ...} |
| 2. Prototype Specs | {Y} | {component specs, screen specs, data-model.md, ...} |
| 3. Code | {Z} | {src/components/*, src/screens/*, ...} |
| 4. Registries | {R} | {screen_registry.json, prototype_traceability_register.json} |
| 5. Matrices | {T} | {TRACEABILITY_MATRIX_MASTER.md, ...} |
| **TOTAL** | **{N}** | - |

## Hierarchical Traceability Chains Affected

[Display chains as per example in STEP 4]

## Flat Summary

| Artifact Type | Count | Create | Modify | Delete |
|---------------|-------|--------|--------|--------|
| Discovery Screens | X | 0 | X | 0 |
| JTBDs | X | 0 | X | 0 |
| Requirements | X | X | X | 0 |
| Component Specs | X | X | X | 0 |
| Screen Specs | X | X | 0 | 0 |
| Data Models | X | 0 | X | 0 |
| API Contracts | X | 0 | X | 0 |
| Code Files | X | X | X | 0 |
| Registry Entries | R | X | X | 0 |
| Matrix Entries | T | 0 | T | 0 |
| **TOTAL** | **{N}** | **{C}** | **{M}** | **{D}** |

## Reflexion Self-Critique

Completeness Check: {✓/⚠/❌}
{Reasoning from reflexion}

Accuracy Check: {✓/⚠/❌}
{Reasoning from reflexion}

Downstream Impact: {✓/⚠/❌}
{Reasoning from reflexion}

Risk Assessment:
- Traceability Breaks: {Y/N} - {details}
- Build Failures: {Y/N} - {details}
- Visual Regression: {Y/N} - {details}
- Regression Risk: {LOW|MEDIUM|HIGH}
- Breaking Changes: {Y/N} - {what}

Severity: {CRITICAL|HIGH|MEDIUM|LOW}

Confidence Level: {HIGH|MEDIUM|LOW} ({XX}%)
Reasoning: {Why this confidence level}

Warnings:
{List any risks or uncertainties}

═══════════════════════════════════════════════════════════════
```

---

### Phase 3: Registration

**STEP 1: ASSIGN UNIQUE ID**

```bash
READ/CREATE: Prototype_{PROTOTYPE_NAME}/feedback-sessions/prototype_feedback_registry.json

EXTRACT existing IDs: [PF-001, PF-002, ...]
CALCULATE next_id = max(IDs) + 1
FORMAT as PF-{NNN} (zero-padded to 3 digits)

STORE as feedback_id
```

**STEP 2: RENAME SESSION FOLDER**

```bash
RENAME:
   FROM: feedback-sessions/<YYYY-MM-DD>_PrototypeFeedback-TEMP/
   TO:   feedback-sessions/<YYYY-MM-DD>_PrototypeFeedback-{feedback_id}/
```

**STEP 3: UPDATE FRONTMATTER IN SESSION FILES**

```bash
FOR each .md file in session folder:
   UPDATE document_id: PF-TEMP → {feedback_id}
```

**STEP 4: CREATE REGISTRY ENTRY**

```bash
ADD to prototype_feedback_registry.json:

{
  "id": "{feedback_id}",
  "title": "{first_line_or_summary}",
  "type": "{type}",
  "severity": "{severity}",
  "status": "analyzing",
  "categories": ["{CAT-XXX}", ...],
  "impact": {
    "chains_affected": N,
    "artifacts_affected": M,
    "layer_1_discovery": X,
    "layer_2_specs": Y,
    "layer_3_code": Z,
    "layer_4_registries": R,
    "layer_5_matrices": T,
    "confidence_level": "{level}",
    "reflexion_score": XX
  },
  "source": {
    "person": "{source_person}",
    "role": "{role}",
    "inputter": "{inputter}"
  },
  "lifecycle": {
    "created_at": "{ISO8601}",
    "analyzed_at": "{ISO8601}"
  },
  "session_folder": "feedback-sessions/{date}_PrototypeFeedback-{feedback_id}/"
}

UPDATE statistics:
   total_feedback += 1
   by_status.analyzing += 1
   by_type.{type} += 1
   by_severity.{severity} += 1
```

**STEP 5: UPDATE STATE FILE**

```bash
UPDATE _state/prototype_config.json:
   active_feedback: "{feedback_id}"
   last_feedback_at: "{ISO8601}"
```

**STEP 6: DISPLAY REGISTRATION CONFIRMATION**

```bash
OUTPUT:
✅ Feedback Registered

   ID: {feedback_id}
   Type: {type}
   Severity: {severity}
   Categories: {categories}

   5-Layer Impact:
   - Discovery: {X} artifacts
   - Specs: {Y} artifacts
   - Code: {Z} files
   - Registries: {R} entries (ALWAYS updated)
   - Matrices: {T} chains

   Reflexion Confidence: {level} ({XX}%)
   Session: {session_folder}
```

---

### Phase 4: Approval Gate (ASKUSERQUESTION INTEGRATION)

**STEP 1: PREPARE APPROVAL PROMPT**

```bash
READ: feedback-sessions/{date}_PrototypeFeedback-{feedback_id}/impact_analysis.md

EXTRACT summary statistics:
   - chains_affected
   - artifacts_affected
   - layer counts
   - confidence level
   - severity

CONSTRUCT approval context:
   impact_summary = "Feedback {feedback_id} affects {M} artifacts across {N} traceability chains spanning all 5 layers (Discovery: {X}, Specs: {Y}, Code: {Z}, Registries: {R}, Matrices: {T})."

   reflexion_context = "Reflexion confidence: {level} ({XX}%)."

   risk_context = IF severity == "Critical" OR confidence < 60:
      "⚠️ {severity} severity with {risk_details}"
   ELSE:
      "Impact is well-understood with no critical risks identified."
```

**STEP 2: ASK FOR APPROVAL DECISION**

```bash
USE AskUserQuestion:
   question: "{impact_summary} {reflexion_context} {risk_context} Review the detailed impact analysis above. How should we proceed?"
   header: "Approval"
   multiSelect: false
   options:
     - label: "Approve (Recommended)"
       description: "Proceed to implementation planning. Effort will be calculated during option generation with reflexion scoring."

     - label: "Reject"
       description: "Mark feedback as rejected. No changes will be made. Requires rejection reason."

     - label: "Modify Scope"
       description: "Adjust which artifacts/layers to change before proceeding to planning."

     - label: "Request Deeper Analysis"
       description: "Reflexion confidence is {level} - request more investigation before deciding."
```

**STEP 3: HANDLE APPROVAL RESPONSES**

```bash
CASE approval_decision:

   WHEN "Approve":
      UPDATE prototype_feedback_registry.json:
         feedback_items.{feedback_id}.status = "approved"
         feedback_items.{feedback_id}.lifecycle.approved_at = NOW()
         feedback_items.{feedback_id}.lifecycle.approved_by = "{user}"

      UPDATE statistics:
         by_status.analyzing -= 1
         by_status.approved += 1

      CONTINUE to Phase 5

   WHEN "Reject":
      PROMPT: "Please provide a reason for rejection:"
      STORE as rejection_reason

      UPDATE prototype_feedback_registry.json:
         feedback_items.{feedback_id}.status = "rejected"
         feedback_items.{feedback_id}.lifecycle.rejected_at = NOW()
         feedback_items.{feedback_id}.lifecycle.rejected_by = "{user}"
         feedback_items.{feedback_id}.lifecycle.rejection_reason = "{rejection_reason}"

      UPDATE statistics:
         by_status.analyzing -= 1
         by_status.rejected += 1

      GENERATE FEEDBACK_SUMMARY.md:
         # Feedback Summary - {feedback_id}

         ## Original Feedback
         [Content]

         ## Status
         REJECTED

         ## Reason
         {rejection_reason}

         ## Rejected By
         {user} on {date}

      OUTPUT:
      ❌ Feedback {feedback_id} marked as REJECTED

      END WORKFLOW

   WHEN "Modify Scope":

      EXTRACT all artifact types from impact_analysis.md

      USE AskUserQuestion:
         question: "Select which artifact types/layers to EXCLUDE from implementation:"
         header: "Exclusions"
         multiSelect: true
         options:
            [One option per artifact type/layer found in analysis]
            Example:
            - "Discovery Layer (screen-definitions, data-fields)"
            - "Component Specs"
            - "Screen Specs"
            - "Data Model Changes"
            - "Code Changes"

      RECEIVE exclusions[]

      RE-RUN Shared_FeedbackImpactAnalyzer_Reflexion:
         WITH exclusion filters
         UPDATE impact_analysis.md (append version 1.1.0)

      RETURN to STEP 2 (Ask for approval decision)

   WHEN "Request Deeper Analysis":

      PROMPT: "What specific areas need more investigation? (screens/components/data/code/traceability)"
      STORE as investigation_focus

      RE-RUN Shared_FeedbackImpactAnalyzer_Reflexion:
         WITH focus_areas = [investigation_focus]
         INCREASE verbosity for those areas
         UPDATE impact_analysis.md (append version 1.1.0)

      RETURN to STEP 2 (Ask for approval decision)
```

---

### Phase 5: Implementation Planning (REFLEXION ENHANCED)

**STEP 1: READ SKILL**

```bash
READ: .claude/skills/Shared_FeedbackPlanGenerator_Reflexion/SKILL.md
```

**STEP 2: BUG TYPES - ENFORCE ROOT CAUSE REQUIREMENT**

```bash
IF type == "Bug":

   VERIFY debugging_evidence.md EXISTS
   READ debugging_evidence.md

   EXTRACT:
      - root_cause_hypothesis
      - hypothesis_confidence

   IF hypothesis_confidence < "MEDIUM":
      ❌ BLOCK: Cannot generate fix options without confirmed root cause

      OUTPUT:
      ═════════════════════════════════════════════════════════════
      ⛔ BLOCKED: Root Cause Not Confirmed
      ═════════════════════════════════════════════════════════════

      The bug debugging phase did not reach MEDIUM+ confidence on the root cause.
      Implementation planning requires a confirmed hypothesis.

      Current hypothesis: {hypothesis}
      Confidence: {confidence}

      Please return to Phase 2, STEP 3 for more investigation.
      ═════════════════════════════════════════════════════════════

      END WORKFLOW

   ENDIF
```

**STEP 3: INVOKE SHARED PLAN GENERATOR**

```bash
INVOKE Shared_FeedbackPlanGenerator_Reflexion:

   inputs:
      impact_analysis_path: {path_to_impact_analysis.md}
      feedback_type: {type}
      stage: "prototype"
      system_name: {PROTOTYPE_NAME}

   GENERATE OPTIONS (minimum 2):

      FOR Bug types:
         Option A: Quick Fix (symptom-level fix, may recur)
         Option B: Proper Fix (root cause fix) - RECOMMENDED
         Option C: Preventive Fix (root cause + defensive code + regression test)

      FOR Enhancement/NewFeature types:
         Option A: Minimal/MVP (core change only)
         Option B: Standard/Full (complete implementation) - RECOMMENDED
         Option C: Comprehensive/Extended (extra polish + docs)

      FOR VisualIssue types:
         Option A: Code-only (direct style change)
         Option B: Token-based (update design tokens) - RECOMMENDED
         Option C: Spec-first (update specs → tokens → code)

   FOR EACH option:

      GENERATE DETAILED STEPS:

         Step N: Update {Artifact-ID} - {Description}

         File: `{exact/path/to/file.md}`
         Section: {section_name}
         Line: {start_line}-{end_line}

         BEFORE:
         ```{language}
         {exact current content with line numbers}
         ```

         AFTER:
         ```{language}
         {exact proposed content with changes highlighted}
         ```

         Traceability Updates:
         - Registry: `{registry_path}`
         - Field: `{field_name}`
         - Change: {description of registry update}

         Version Update:
         - Current: {X.Y.Z}
         - New: {X.Y.Z+1}
         - Reason: {MAJOR|MINOR|PATCH} - {change_type}

         Estimated Time: {minutes} minutes

      REFLEXION EVALUATION:

         Completeness: Does it address ALL affected artifacts?
            ✓ = All chains in impact_analysis.md addressed
            ⚠ = Some artifacts skipped (list which)
            ❌ = Major gaps (list missing)

         Consistency: Does it maintain traceability integrity?
            ✓ = All chains remain valid, all registries updated
            ⚠ = Some manual registry fixes needed
            ❌ = Breaks traceability chains

         Quality: Does it follow Prototype framework standards?
            ✓ = Follows component/screen spec templates
            ⚠ = Minor deviations (list)
            ❌ = Violates standards (list violations)

         Risk Assessment:
            - Build risk: {description}
            - Visual regression risk: {description}
            - Traceability risk: {description}

         Effort Estimate:
            {time} (based on {N} steps, complexity)

         CALCULATE SCORE:

            base_score = (completeness_score * 0.4) +
                        (consistency_score * 0.35) +
                        (quality_score * 0.25)

            risk_penalty = SUM(risk_levels)
            total_score = base_score - risk_penalty

         SCORE: {total_score}/10

         RECOMMENDATION:
            IF total_score >= 8.0:
               recommendation = "APPROVE"
            ELIF total_score >= 6.0:
               recommendation = "APPROVE WITH CAUTION"
            ELSE:
               recommendation = "REJECT"

         REASONING: [Explain score and recommendation]

   returns:
      implementation_options_path: "feedback-sessions/{date}_PrototypeFeedback-{feedback_id}/implementation_options.md"
      options_count: N
      recommended_option: "{option_letter}"
      highest_score: X.X
```

**STEP 4: DISPLAY OPTIONS TO USER**

```bash
READ: implementation_options.md

OUTPUT:
═══════════════════════════════════════════════════════════════
 IMPLEMENTATION OPTIONS - {feedback_id}
═══════════════════════════════════════════════════════════════

[Full content of implementation_options.md with all options and reflexion scores]

═══════════════════════════════════════════════════════════════
```

**STEP 5: ASK FOR PLAN SELECTION**

```bash
EXTRACT from implementation_options.md:
   - option_a_name, option_a_score, option_a_steps, option_a_effort
   - option_b_name, option_b_score, option_b_steps, option_b_effort
   - option_c_name (if exists), option_c_score, option_c_steps, option_c_effort

IDENTIFY recommended (highest score)

USE AskUserQuestion:
   question: "Three implementation options generated with reflexion evaluation. {recommended_option} scored {highest_score}/10 (Recommended). Which approach?"
   header: "Plan"
   multiSelect: false
   options:
     - label: "Option A: {option_a_name}{' (Recommended)' if A is recommended else ''}"
       description: "{option_a_steps} steps, {option_a_artifacts} artifacts. Effort: {option_a_effort}. Reflexion score: {option_a_score}/10. {option_a_recommendation}"

     - label: "Option B: {option_b_name}{' (Recommended)' if B is recommended else ''}"
       description: "{option_b_steps} steps, {option_b_artifacts} artifacts. Effort: {option_b_effort}. Reflexion score: {option_b_score}/10. {option_b_recommendation}"

     - label: "Option C: {option_c_name}{' (Recommended)' if C is recommended else ''}"
       description: "{option_c_steps} steps, {option_c_artifacts} artifacts. Effort: {option_c_effort}. Reflexion score: {option_c_score}/10. {option_c_recommendation}"

     - label: "Custom Plan"
       description: "Provide your own implementation plan - will be evaluated by reflexion before execution."
```

**STEP 6: HANDLE PLAN SELECTION**

```bash
CASE plan_selection:

   WHEN "Option A" OR "Option B" OR "Option C":

      UPDATE _state/prototype_config.json:
         feedback_plan_selection: "{selected_option}"
         feedback_session_id: "{feedback_id}"

      CREATE implementation_plan.md:

         ---
         document_id: PF-PLAN-{feedback_id}
         version: 1.0.0
         created_at: {YYYY-MM-DD}
         selected_option: "{option_letter}"
         reflexion_score: {score}/10
         ---

         # Implementation Plan - {feedback_id}

         ## Selected Option: {option_name}

         Reflexion Score: {score}/10
         Recommendation: {recommendation}
         Effort: {effort}

         ## Steps (with Before/After Content)

         [Copy full steps from selected option in implementation_options.md]

         ## Reflexion Evaluation

         [Copy reflexion evaluation from selected option]

      CONTINUE to Phase 6

   WHEN "Custom Plan":

      PROMPT: "Provide your custom implementation plan (step-by-step format):"

      RECEIVE custom_plan_text

      VALIDATE using Shared_FeedbackPlanGenerator_Reflexion:
         PARSE custom_plan_text into structured steps
         EVALUATE against same reflexion criteria
         GENERATE reflexion_score

      DISPLAY evaluation:
         Custom Plan Reflexion Evaluation:
         - Completeness: {✓/⚠/❌}
         - Consistency: {✓/⚠/❌}
         - Quality: {✓/⚠/❌}
         - Score: {X}/10
         - Recommendation: {recommendation}

      USE AskUserQuestion:
         question: "Custom plan scored {score}/10 with recommendation: {recommendation}. Proceed or revise?"
         header: "Decision"
         options:
            - "Proceed" (use custom plan)
            - "Revise" (re-enter plan)

      IF "Revise":
         LOOP back to custom plan input

      IF "Proceed":
         CREATE implementation_plan.md with custom plan
         CONTINUE to Phase 6
```

---

### Phase 6: Implementation

**STEP 1: LOAD PLAN**

```bash
READ: feedback-sessions/{date}_PrototypeFeedback-{feedback_id}/implementation_plan.md

PARSE steps:
   FOR each step:
      EXTRACT:
         - step_number
         - artifact_id
         - file_path
         - section
         - line_range
         - before_content
         - after_content
         - traceability_updates
         - version_update

STORE as implementation_steps[]
```

**STEP 2: CREATE BACKUPS**

```bash
FOR each unique file in implementation_steps[]:
   COPY {file} to {file}.backup

LOG: "Created {count} backup files"
```

**STEP 3: UPDATE REGISTRY STATUS**

```bash
UPDATE prototype_feedback_registry.json:
   feedback_items.{feedback_id}.status = "in_progress"
   feedback_items.{feedback_id}.lifecycle.implementation_started_at = NOW()
   feedback_items.{feedback_id}.implementation.steps_total = {count}

UPDATE statistics:
   by_status.approved -= 1
   by_status.in_progress += 1
```

**STEP 4: EXECUTE IMPLEMENTATION**

```bash
INITIALIZE implementation_log.md:

   ---
   document_id: PF-LOG-{feedback_id}
   version: 1.0.0
   created_at: {YYYY-MM-DD}
   ---

   # Implementation Log - {feedback_id}

   Plan: {selected_option}
   Total Steps: {count}
   Started: {ISO8601}

   ---

FOR each step IN implementation_steps:

   APPEND to implementation_log.md:

      ## Step {N}/{total}: {artifact_id} - {description}

      Started: {HH:MM:SS}
      File: {file_path}

   TRY:

      1. READ current file
         current_content = Read(file_path)

      2. VERIFY before content matches
         expected_before = step.before_content
         actual_before = EXTRACT_SECTION(current_content, step.section, step.line_range)

         IF actual_before != expected_before:
            ⚠️ WARNING: File state differs from plan

            APPEND to log:
               Status: ⚠️ STATE MISMATCH
               Expected Before:
               ```
               {expected_before}
               ```
               Actual Before:
               ```
               {actual_before}
               ```

            USE AskUserQuestion:
               question: "Step {N}: File state differs from plan. The file may have been modified since planning. Continue anyway?"
               header: "Mismatch"
               options:
                  - "Continue Anyway" (apply changes to current state)
                  - "Skip This Step" (skip and continue)
                  - "Abort Implementation" (stop and save resume point)

            CASE response:
               WHEN "Continue Anyway":
                  # Proceed to step 3
               WHEN "Skip This Step":
                  MARK step as "skipped"
                  APPEND to log: Status: ⏭️ SKIPPED
                  CONTINUE to next step
               WHEN "Abort Implementation":
                  SAVE resume_point = step_number
                  UPDATE registry status = "failed"
                  EXIT Phase 6

      3. APPLY CHANGES

         IF step.change_type == "CREATE":
            WRITE {file_path}: {after_content}

         ELIF step.change_type == "MODIFY":
            IF file is YAML/JSON:
               PARSE current_content
               APPLY changes per step.after_content
               SERIALIZE back to file

            ELSE:
               EDIT {file_path}:
                  old_string = {before_content}
                  new_string = {after_content}

         ELIF step.change_type == "DELETE":
            DELETE {file_path}

      4. UPDATE VERSION METADATA (if file has frontmatter)

         PARSE frontmatter
         INCREMENT version per step.version_update.reason
         UPDATE updated_at = TODAY
         ADD to change_history:
            version: {new_version}
            date: {YYYY-MM-DD}
            author: "Prototype_Feedback"
            changes: {step.description}
            feedback_ref: "{feedback_id}"
         WRITE frontmatter back

      5. UPDATE TRACEABILITY REGISTRIES (if step includes registry updates)

         FOR each registry_update IN step.traceability_updates:
            READ {registry_update.registry}
            APPLY {registry_update.change}
            ADD feedback_source: "{feedback_id}"
            WRITE registry

      6. LOG SUCCESS

         APPEND to implementation_log.md:
            Status: ✅ SUCCESS
            Version: {old} → {new}
            Completed: {HH:MM:SS}

      7. UPDATE PROGRESS

         UPDATE prototype_feedback_registry.json:
            feedback_items.{feedback_id}.implementation.steps_completed = {N}

         SET resume_point = {N+1}

   CATCH error:

      LOG FAILURE:
         APPEND to implementation_log.md:
            Status: ❌ FAILED
            Error: {error_message}
            Failed At: {HH:MM:SS}

      SAVE resume_point = {step_number}

      USE AskUserQuestion:
         question: "Step {N} failed: {error}. How to proceed?"
         header: "Failure"
         options:
            - "Skip and Continue" (log skip, continue to next step)
            - "Retry Step" (attempt step again)
            - "Abort and Save Resume Point" (stop, allow resume later)

      CASE response:
         WHEN "Skip and Continue":
            MARK step as "skipped"
            APPEND to log: Status: ⏭️ SKIPPED (user requested)
            CONTINUE to next step

         WHEN "Retry Step":
            RETRY current step (max 3 retries)

         WHEN "Abort and Save Resume Point":
            UPDATE registry:
               status = "failed"
               implementation.resume_point = "{step_number}"
            SAVE implementation_log.md
            EXIT Phase 6

ENDFOR
```

**STEP 5: FINALIZE IMPLEMENTATION**

```bash
APPEND to implementation_log.md:

   ---

   ## Summary

   Total Steps: {total}
   Succeeded: {success_count}
   Failed: {fail_count}
   Skipped: {skip_count}

   Completed: {ISO8601}

UPDATE prototype_feedback_registry.json:
   feedback_items.{feedback_id}.status = "implemented"
   feedback_items.{feedback_id}.lifecycle.implementation_completed_at = NOW()
   feedback_items.{feedback_id}.implementation.resume_point = null

UPDATE statistics:
   by_status.in_progress -= 1
   by_status.implemented += 1

CREATE files_changed.md:

   ---
   document_id: PF-CHANGES-{feedback_id}
   version: 1.0.0
   created_at: {YYYY-MM-DD}
   ---

   # Files Changed - {feedback_id}

   ## Summary

   Total Files Modified: {count}

   | Layer | Files |
   |-------|-------|
   | Discovery | {X} |
   | Prototype Specs | {Y} |
   | Code | {Z} |
   | Registries | {R} |
   | Matrices | {T} |

   ## Detailed Changes

   ### Layer 1: Discovery

   {For each discovery file modified:}
   - `{file_path}` - {change_type} - {description}

   ### Layer 2: Prototype Specs

   {For each spec file modified:}
   - `{file_path}` - {change_type} - {description}

   ### Layer 3: Code

   {For each code file modified:}
   - `{file_path}` - {change_type} - {description}

   ### Layer 4: Registries

   {For each registry modified:}
   - `{registry_path}` - {entries_added/modified}

   ### Layer 5: Matrices

   {For each matrix modified:}
   - `{matrix_path}` - {chains_updated}

OUTPUT:
✅ Implementation Complete

   Steps: {success_count}/{total}
   Failed: {fail_count}
   Skipped: {skip_count}

   Files Changed: {count}
   - Discovery: {X}
   - Specs: {Y}
   - Code: {Z}
   - Registries: {R}
   - Matrices: {T}
```

---

### Phase 7: Validation (REFLEXION ENHANCED)

**STEP 1: READ SKILL**

```bash
READ: .claude/skills/Shared_FeedbackReviewer_Reflexion/SKILL.md
```

**STEP 2: PLAN COMPLIANCE VALIDATION**

```bash
READ: implementation_plan.md
READ: implementation_log.md

CHECK:
   ✓ All planned steps executed?
      expected_steps = PARSE implementation_plan.md
      executed_steps = PARSE implementation_log.md
      missing_steps = expected_steps - executed_steps

   ✓ All files modified as specified?
      FOR each file in files_changed.md:
         VERIFY file exists
         VERIFY version incremented

   ✓ Any unexpected changes?
      git status (if in git repo)
      COMPARE with files_changed.md

   ✓ Backup files exist?
      FOR each changed file:
         VERIFY {file}.backup exists

RESULT:
   plan_compliance = IF all checks pass: PASS ELSE: FAIL
   plan_compliance_issues = [list of failures]
```

**STEP 3: CONTENT VALIDATION**

```bash
FOR each file in files_changed.md:

   READ file

   ✓ Before/After matches implementation_plan.md?
      expected_after = LOOKUP in implementation_plan.md
      actual_after = EXTRACT_SECTION(file)
      COMPARE

   ✓ Frontmatter version incremented?
      PARSE frontmatter
      CHECK version field exists and matches expected

   ✓ change_history entry added with {feedback_id}?
      SEARCH for feedback_ref: "{feedback_id}" in change_history

   ✓ File format valid (YAML/JSON/Markdown)?
      PARSE file
      CATCH syntax errors

RESULT:
   content_validation = IF all checks pass: PASS ELSE: FAIL
   content_issues = [list of failures]
```

**STEP 4: 5-LAYER TRACEABILITY VALIDATION (PROTOTYPE-SPECIFIC)**

```bash
LAYER 1: Discovery Validation
   ✓ screen-definitions.md - Screen entry exists with zones, components
   ✓ navigation-structure.md - Screen in navigation hierarchy
   ✓ data-fields.md - All new fields documented
   ✓ JOBS_TO_BE_DONE.md - Feature linked to JTBD (if new feature)

LAYER 2: Prototype Specs Validation
   ✓ 01-components/component-index.md - New components listed
   ✓ 01-components/{category}/{component}/spec.md - Spec files exist
   ✓ 02-screens/screen-index.md - New screens listed
   ✓ 02-screens/{platform}/{screen}/spec.md - Spec files exist
   ✓ 03-interactions/*.md - Relevant specs updated
   ✓ 04-implementation/data-model.md - Entity schemas exist
   ✓ 04-implementation/api-contracts.json - Endpoints defined
   ✓ 04-implementation/test-data/*.json - Test data files exist

LAYER 3: Code Validation
   ✓ src/screens/{platform}/ - Screen files exist
   ✓ src/components/ - Component files exist
   ✓ src/App.tsx - Routes configured (if new screen)
   ✓ src/data/ - Data files in correct location
   ✓ npm run build - Build succeeds

   RUN BUILD VERIFICATION (if Layer 3 changed):
      cd Prototype_{PROTOTYPE_NAME}/prototype/
      npm run build

      IF build fails:
         LOG failure details
         traceability_validation = FAIL
         traceability_issues.add("Build failure - see log")

LAYER 4: Registry Validation (ALWAYS REQUIRED)
   ✓ traceability/screen_registry.json:
       - Entry in discovery_screens[] with feedback_source: "{feedback_id}"
       - Entry in traceability[] with all statuses
       - screen_coverage statistics updated

   ✓ traceability/prototype_traceability_register.json:
       - Entry in screen_traceability.screens[]
       - coverage counts updated
       - feedback_source field set to "{feedback_id}"

   ✓ traceability/discovery_traceability_register.json (if Layer 1 changed)
   ✓ _state/requirements_registry.json (if requirements added)

LAYER 5: Matrix Validation
   ✓ helperFiles/TRACEABILITY_MATRIX_MASTER.md:
       - Trace chain exists for new items
       - Coverage table updated

   ✓ helperFiles/TRACEABILITY_ASSESSMENT_REPORT.md:
       - Coverage percentages updated
       - New items in inventory

RESULT:
   traceability_validation = IF all layers pass: PASS ELSE: FAIL
   traceability_issues = [list of failures]
```

**STEP 5: INVOKE SHARED REVIEWER (REFLEXION MULTI-PERSPECTIVE)**

```bash
INVOKE Shared_FeedbackReviewer_Reflexion:

   inputs:
      feedback_id: {feedback_id}
      stage: "prototype"
      session_folder: "Prototype_{PROTOTYPE_NAME}/feedback-sessions/{date}_PrototypeFeedback-{feedback_id}/"
      impact_analysis_path: "impact_analysis.md"
      implementation_plan_path: "implementation_plan.md"
      implementation_log_path: "implementation_log.md"
      files_changed_path: "files_changed.md"

   PERSPECTIVE 1: REQUIREMENTS VALIDATOR

      Questions:
         ✓ Does implementation address the original feedback?
         ✓ Are all affected artifacts from impact analysis updated?
         ✓ Is any scope creep introduced?
         ✓ For Bug types: Is root cause fixed?

      SCORE: X/10
      ISSUES: [list]
      RECOMMENDATION: {text}

   PERSPECTIVE 2: SOLUTION ARCHITECT

      Questions:
         ✓ Is the approach architecturally sound?
         ✓ Does it follow Prototype framework patterns?
         ✓ Are 5 layers properly updated?
         ✓ Is traceability intact?
         ✓ Any technical debt introduced?

      SCORE: X/10
      ISSUES: [list]
      RECOMMENDATION: {text}

   PERSPECTIVE 3: CODE QUALITY REVIEWER

      Questions:
         ✓ Is content clean and maintainable?
         ✓ Are Prototype conventions followed?
         ✓ Is documentation updated?
         ✓ Are version histories correct?
         ✓ Build successful?

      SCORE: X/10
      ISSUES: [list]
      RECOMMENDATION: {text}

   CONSENSUS CALCULATION:

      average_score = (perspective_1_score + perspective_2_score + perspective_3_score) / 3

      IF average_score >= 8.0:
         consensus_recommendation = "✅ PASS - Accept implementation"
      ELIF average_score >= 6.0:
         consensus_recommendation = "⚠️ CONDITIONAL PASS - Accept with minor fixes"
      ELSE:
         consensus_recommendation = "❌ FAIL - Revise and reimplement"

   returns:
      validation_report_path: "VALIDATION_REPORT.md"
      consensus_score: X.X
      consensus_recommendation: "{recommendation}"
      issues: [{issue_list}]
      recommendations: [{recommendation_list}]
```

**STEP 6: RUN PROTOTYPE QUALITY GATES (if available)**

```bash
IF exists: .claude/hooks/prototype_quality_gates.py

   RUN:
      python3 .claude/hooks/prototype_quality_gates.py \
         --validate-feedback {feedback_id} \
         --dir Prototype_{PROTOTYPE_NAME}/

   CAPTURE output

   IF exit_code != 0:
      quality_gate_result = FAIL
      quality_gate_issues = [parse output]
   ELSE:
      quality_gate_result = PASS

ELSE:
   quality_gate_result = SKIPPED (no quality gate script)
```

**STEP 7: UPDATE REGISTRY WITH VALIDATION RESULTS**

```bash
UPDATE prototype_feedback_registry.json:

   IF plan_compliance == PASS AND content_validation == PASS AND traceability_validation == PASS AND consensus_score >= 6.0:

      feedback_items.{feedback_id}.status = "validated"
      feedback_items.{feedback_id}.lifecycle.validated_at = NOW()
      feedback_items.{feedback_id}.validation = {
         "plan_compliance": true,
         "content_valid": true,
         "traceability_intact": true,
         "build_successful": {true if build passed},
         "reflexion_consensus_score": {average_score},
         "recommendations": [{recommendations}],
         "issues": []
      }

      UPDATE statistics:
         by_status.in_progress -= 1
         by_status.validated += 1

   ELSE:

      feedback_items.{feedback_id}.status = "failed"
      feedback_items.{feedback_id}.lifecycle.failed_at = NOW()
      feedback_items.{feedback_id}.validation = {
         "plan_compliance": {true|false},
         "content_valid": {true|false},
         "traceability_intact": {true|false},
         "build_successful": {true|false},
         "reflexion_consensus_score": {average_score},
         "recommendations": [{recommendations}],
         "issues": [{combined_issues}]
      }

      UPDATE statistics:
         by_status.in_progress -= 1
         by_status.failed += 1
```

**STEP 8: DISPLAY VALIDATION RESULTS**

```bash
OUTPUT:
═══════════════════════════════════════════════════════════════
 VALIDATION RESULTS - {feedback_id}
═══════════════════════════════════════════════════════════════

Plan Compliance: {PASS/FAIL}
{If failed: list issues}

Content Validation: {PASS/FAIL}
{If failed: list issues}

5-Layer Traceability: {PASS/FAIL}
├─ Layer 1 (Discovery): {✓/❌}
├─ Layer 2 (Specs): {✓/❌}
├─ Layer 3 (Code): {✓/❌}
├─ Layer 4 (Registries): {✓/❌}
└─ Layer 5 (Matrices): {✓/❌}
{If failed: list issues per layer}

Build Verification: {PASS/FAIL/SKIPPED}
{If failed: show build error}

Quality Gates: {PASS/FAIL/SKIPPED}
{If failed: show gate errors}

---

Reflexion Multi-Perspective Review:

├─ Requirements Validator: {score}/10
│  {If issues: list them}
│  Recommendation: {text}
│
├─ Solution Architect: {score}/10
│  {If issues: list them}
│  Recommendation: {text}
│
└─ Code Quality Reviewer: {score}/10
   {If issues: list them}
   Recommendation: {text}

Consensus Score: {average_score}/10
Consensus Recommendation: {consensus_recommendation}

{If issues exist:}
Action Items:
1. {issue_1}
2. {issue_2}
...

═══════════════════════════════════════════════════════════════
```

**STEP 9: HANDLE VALIDATION FAILURES**

```bash
IF consensus_score < 8.0 OR any validation == FAIL:

   USE AskUserQuestion:
      question: "Validation identified {N} issues with consensus score {average_score}/10. Recommendation: {consensus_recommendation}. How to proceed?"
      header: "Decision"
      options:
         - "Accept As-Is" (override validation, mark as validated)
         - "Fix Issues Now" (iterate Phase 6 for failed steps)
         - "Mark As Incomplete" (close with known issues documented)

   CASE response:

      WHEN "Accept As-Is":
         UPDATE registry:
            status = "validated"
            validation.override_reason = "User accepted despite issues"
            lifecycle.validated_at = NOW()

      WHEN "Fix Issues Now":
         EXTRACT failed_steps from implementation_log.md
         RE-RUN Phase 6 for failed_steps only
         RETURN to Phase 7

      WHEN "Mark As Incomplete":
         UPDATE registry:
            status = "completed_with_issues"
            validation.known_issues = [{issues}]
            lifecycle.completed_at = NOW()

         CONTINUE to Phase 8
```

---

### Phase 8: Completion

**STEP 1: GENERATE SUMMARY**

```bash
CREATE FEEDBACK_SUMMARY.md:

---
document_id: PF-SUMMARY-{feedback_id}
version: 1.0.0
created_at: {YYYY-MM-DD}
---

# Feedback Summary - {feedback_id}

## Original Feedback

{feedback_content}

## Classification

- **Type**: {type}
- **Severity**: {severity}
- **Categories**: {categories}

## Impact Analysis Summary

- Traceability Chains Affected: {N}
- Total Artifacts Modified: {M}
- Reflexion Confidence: {level} ({XX}%)

5-Layer Breakdown:
- Discovery: {X} artifacts
- Prototype Specs: {Y} artifacts
- Code: {Z} files
- Registries: {R} entries
- Matrices: {T} chains

## Implementation Approach

- Selected Plan: {option_name}
- Reflexion Score: {score}/10
- Recommendation: {recommendation}
- Total Steps: {total}
- Succeeded: {success_count}
- Failed: {fail_count}
- Skipped: {skip_count}

## Changes Made

{Content from files_changed.md}

## Validation Results

- Plan Compliance: {PASS/FAIL}
- Content Validation: {PASS/FAIL}
- 5-Layer Traceability: {PASS/FAIL}
- Build Verification: {PASS/FAIL/SKIPPED}
- Reflexion Consensus: {average_score}/10
- Consensus Recommendation: {consensus_recommendation}

{If issues:}
Known Issues:
1. {issue_1}
2. {issue_2}

{If recommendations:}
Recommendations:
1. {rec_1}
2. {rec_2}

## Timeline

| Phase | Duration |
|-------|----------|
| Analysis | {analyzed_at - created_at} |
| Planning | {planning time} |
| Implementation | {implementation_completed_at - implementation_started_at} |
| Validation | {validated_at - implementation_completed_at} |
| **Total** | {total time} |

## Status

{Final status and any action items}

---

**Generated**: {ISO8601}
**Status**: {status}
```

**STEP 2: UPDATE FINAL STATUS**

```bash
UPDATE prototype_feedback_registry.json:
   feedback_items.{feedback_id}.status = "completed"
   feedback_items.{feedback_id}.lifecycle.completed_at = NOW()

UPDATE statistics:
   by_status.validated -= 1
   by_status.completed += 1
```

**STEP 3: ASK FOR CLOSURE**

```bash
USE AskUserQuestion:
   question: "Feedback {feedback_id} processing complete with final status: {status}. Close this feedback?"
   header: "Closure"
   options:
      - "Close (Recommended)" (mark as closed, removes from active list)
      - "Keep Open" (leave for review or further work)
```

**STEP 4: HANDLE CLOSURE**

```bash
IF "Close":
   UPDATE prototype_feedback_registry.json:
      feedback_items.{feedback_id}.status = "closed"
      feedback_items.{feedback_id}.lifecycle.closed_at = NOW()

   UPDATE statistics:
      by_status.completed -= 1
      by_status.closed += 1

   UPDATE _state/prototype_config.json:
      active_feedback: null
```

**STEP 5: DISPLAY COMPLETION SUMMARY**

```bash
OUTPUT:
═══════════════════════════════════════════════════════════════
 FEEDBACK PROCESSING COMPLETE - {feedback_id}
═══════════════════════════════════════════════════════════════

ID: {feedback_id}
Status: {status}
Type: {type}
Severity: {severity}

Statistics:
- Traceability Chains Updated: {N}
- Artifacts Modified: {M}
- Files Changed: {count}
- Reflexion Consensus Score: {average_score}/10

5-Layer Impact:
├─ Discovery: {X} artifacts
├─ Specs: {Y} artifacts
├─ Code: {Z} files
├─ Registries: {R} entries (ALWAYS updated)
└─ Matrices: {T} chains

Session Folder: Prototype_{PROTOTYPE_NAME}/feedback-sessions/{date}_PrototypeFeedback-{feedback_id}/

Artifacts Generated:
├─ FEEDBACK_ORIGINAL.md
├─ impact_analysis.md (with reflexion critique)
├─ implementation_options.md (with reflexion scores)
├─ implementation_plan.md (selected plan with before/after)
├─ implementation_log.md (step-by-step execution log)
├─ files_changed.md (summary of modifications)
├─ VALIDATION_REPORT.md (with multi-perspective review)
└─ FEEDBACK_SUMMARY.md (final summary)

{If debugging_evidence.md exists:}
├─ debugging_evidence.md (bug root cause analysis)

═══════════════════════════════════════════════════════════════

LOG command completion:
   bash .claude/hooks/log-lifecycle.sh command /prototype-feedback instruction_end '{"stage": "prototype", "status": "completed", "feedback_id": "{feedback_id}"}'
```

---

## Resume Mode

To resume a failed or partial implementation:

```bash
/prototype-feedback resume PF-<NNN>
```

**STEP 1: LOAD FROM REGISTRY**

```bash
READ: Prototype_{PROTOTYPE_NAME}/feedback-sessions/prototype_feedback_registry.json

FIND entry with id == "PF-<NNN>"

IF not found:
   ERROR: "Feedback PF-<NNN> not found in registry"
   EXIT

EXTRACT:
   - current_status
   - resume_point
   - session_folder
```

**STEP 2: VALIDATE STATE**

```bash
CHECK session_folder exists
CHECK implementation_log.md exists
CHECK files match expected state (from log)
```

**STEP 3: DETERMINE RESUME PHASE**

```bash
CASE current_status:

   WHEN "analyzing":
      OUTPUT: "⏭️ Resuming from Phase 2: Impact Analysis"
      RESUME at Phase 2, STEP 4

   WHEN "approved":
      OUTPUT: "⏭️ Resuming from Phase 5: Implementation Planning"
      RESUME at Phase 5, STEP 1

   WHEN "in_progress":
      OUTPUT: "⏭️ Resuming from Phase 6: Implementation, Step {resume_point}"
      LOAD implementation_steps from implementation_plan.md
      START from step {resume_point}
      RESUME at Phase 6, STEP 4

   WHEN "implemented":
      OUTPUT: "⏭️ Resuming from Phase 7: Validation"
      RESUME at Phase 7, STEP 1

   OTHERWISE:
      ERROR: "Cannot resume from status: {current_status}"
      EXIT
```

**STEP 4: ADD RESUME MARKER**

```bash
APPEND to implementation_log.md:

   ---

   ## RESUMED

   Resume Point: {phase} - {step}
   Resumed At: {ISO8601}
   Resumed By: {user}

   ---
```

**STEP 5: CONTINUE WORKFLOW**

```bash
CONTINUE workflow from determined phase
```

---

## Status Mode

To check current feedback status:

```bash
/prototype-feedback status
```

**DISPLAY**:

```bash
READ: _state/prototype_config.json
EXTRACT: active_feedback

IF active_feedback == null:
   OUTPUT: "No active feedback processing"
   EXIT

READ: prototype_feedback_registry.json
FIND: entry with id == active_feedback

OUTPUT:
═══════════════════════════════════════════════════════════════
 PROTOTYPE FEEDBACK STATUS
═══════════════════════════════════════════════════════════════

Active Feedback: {feedback_id}
Status: {status}
Type: {type}
Severity: {severity}

Current Phase: {infer from status}
{If in_progress:}
   Resume Point: Step {N}/{total}

Timeline:
- Created: {created_at}
- Analyzed: {analyzed_at}
{If approved:}
- Approved: {approved_at}
{If in_progress:}
- Implementation Started: {implementation_started_at}
{If validated:}
- Validated: {validated_at}

Session: {session_folder}

═══════════════════════════════════════════════════════════════
```

---

## List Mode

To list all feedback items:

```bash
/prototype-feedback list
```

**DISPLAY**:

```bash
READ: Prototype_{PROTOTYPE_NAME}/feedback-sessions/prototype_feedback_registry.json

GROUP feedback_items by status

OUTPUT:
═══════════════════════════════════════════════════════════════
 PROTOTYPE FEEDBACK REGISTRY
═══════════════════════════════════════════════════════════════

System: {PROTOTYPE_NAME}
Total Feedback: {statistics.total_feedback}

By Status:
- Analyzing: {by_status.analyzing}
- Approved: {by_status.approved}
- In Progress: {by_status.in_progress}
- Validated: {by_status.validated}
- Completed: {by_status.completed}
- Closed: {by_status.closed}
- Rejected: {by_status.rejected}
- Failed: {by_status.failed}

By Type:
- Bug: {by_type.Bug}
- Enhancement: {by_type.Enhancement}
- NewFeature: {by_type.NewFeature}
- UXIssue: {by_type.UXIssue}
- VisualIssue: {by_type.VisualIssue}

Average Reflexion Score: {statistics.average_reflexion_score}/10

---

## All Feedback Items

{FOR each feedback_item in registry:}

{id} | {status} | {type} | {severity} | {created_at}
   Title: {title}
   Artifacts: {impact.artifacts_affected}
   Reflexion: {impact.confidence_level} ({impact.reflexion_score}%)
   Session: {session_folder}

═══════════════════════════════════════════════════════════════
```

---

## Error Handling

Following global error handling rules (`.claude/rules/CORE_RULES.md`):

| Error Type | Action |
|------------|--------|
| **No Prototype folder found** | Error: "Run /prototype first" - EXIT |
| **File read failure during analysis** | Skip file, note in impact_analysis.md, reduce confidence |
| **File write failure during implementation** | Log failure, save resume point, offer retry/skip/abort |
| **Build failure** | Log in validation, mark build_successful=false, flag in issues |
| **Validation failure** | Show issues, offer accept/fix/mark-incomplete options |
| **Traceability breaks** | Warn, flag as HIGH risk, attempt auto-fix if possible |
| **Registry corruption** | Error: "Registry corrupted - manual fix required" - EXIT |

**Skip-and-Continue Pattern**: Technical errors (parse failures, missing optional files) → skip. Quality violations (missing IDs, broken chains) → BLOCK and fix.

---

## Outputs

### Session Folder Structure

```
Prototype_{PROTOTYPE_NAME}/feedback-sessions/
├── prototype_feedback_registry.json                    # Central registry
└── <YYYY-MM-DD>_PrototypeFeedback-{ID}/               # Per-feedback folder
    ├── FEEDBACK_ORIGINAL.md                           # Original feedback text
    ├── impact_analysis.md                             # Impact analysis with reflexion critique
    ├── debugging_evidence.md                          # (Bug types only) Root cause analysis
    ├── implementation_options.md                      # Generated options with reflexion scores
    ├── implementation_plan.md                         # Selected plan with before/after content
    ├── implementation_log.md                          # Step-by-step execution log
    ├── files_changed.md                               # Summary of all modifications
    ├── VALIDATION_REPORT.md                           # Multi-perspective validation results
    └── FEEDBACK_SUMMARY.md                            # Final summary with timeline
```

### State Updates

- `_state/prototype_config.json` - Active feedback tracking
- `traceability/prototype_traceability_register.json` - Updated with feedback refs
- `traceability/screen_registry.json` - Updated with feedback_source fields

### File Changes (5 Layers)

All modified files will have:
- Version incremented per VERSION_CONTROL_STANDARD.md
- `updated_at` set to today
- `change_history` entry with PF-<NNN> reference and feedback_ref field

---

## Examples

### Example 1: Direct Text Feedback (Enhancement)

```bash
/prototype-feedback "The inventory table should show stock levels in color - red for low, green for sufficient"
```

**Expected Flow**:
1. Classify as Enhancement, Medium severity
2. 5-layer impact analysis → affects all layers
3. Register as PF-001
4. User approves
5. Generate 3 options (Minimal, Standard, Comprehensive)
6. User selects Option B (Standard) - score 8.5/10
7. Implement across 5 layers
8. Validate (build succeeds, consensus 9/10)
9. Mark as validated and closed

---

### Example 2: Bug Report with Debugging

```bash
/prototype-feedback "Bug: The save button on the inventory form doesn't work. Clicking it does nothing and no error is shown."
```

**Expected Flow**:
1. Classify as Bug, Critical severity
2. **Systematic debugging**:
   - Ask for reproduction steps
   - Trace from click event → handler → state → API
   - Form hypothesis: "onClick handler not wired to form submit"
   - User confirms hypothesis
3. 5-layer impact analysis (focuses on Layer 3: Code)
4. Register as PF-002
5. User approves
6. Generate 3 bug fix options (Quick/Proper/Preventive)
7. User selects Option C (Preventive Fix) - score 9/10
8. Implement: Fix handler + add validation + add regression test
9. Validate (build succeeds, bug no longer reproduces, consensus 9.5/10)
10. Mark as validated and closed

---

### Example 3: File-Based Feedback

```bash
/prototype-feedback ./stakeholder_feedback_jan_25.md
```

**Expected Flow**:
- Read file content
- Follow standard workflow

---

### Example 4: Interactive Mode

```bash
/prototype-feedback
```

**Expected Flow**:
- Prompt: "Enter feedback or describe the change needed:"
- User types feedback
- Follow standard workflow

---

### Example 5: Resume Failed Implementation

```bash
/prototype-feedback resume PF-003
```

**Expected Flow**:
- Load PF-003 from registry
- Check status: "in_progress", resume_point: Step 7
- Resume implementation from Step 7
- Continue to validation and completion

---

### Example 6: Check Status

```bash
/prototype-feedback status
```

**Expected Output**:
```
═══════════════════════════════════════════════════════════════
 PROTOTYPE FEEDBACK STATUS
═══════════════════════════════════════════════════════════════

Active Feedback: PF-002
Status: in_progress
Type: Bug
Severity: Critical

Current Phase: Implementation
Resume Point: Step 7/15

Timeline:
- Created: 2026-01-25 10:30:00
- Analyzed: 2026-01-25 10:45:00
- Approved: 2026-01-25 11:00:00
- Implementation Started: 2026-01-25 11:15:00

Session: feedback-sessions/2026-01-25_PrototypeFeedback-PF-002/

═══════════════════════════════════════════════════════════════
```

---

### Example 7: List All Feedback

```bash
/prototype-feedback list
```

**Expected Output**:
```
═══════════════════════════════════════════════════════════════
 PROTOTYPE FEEDBACK REGISTRY
═══════════════════════════════════════════════════════════════

System: InventorySystem
Total Feedback: 5

By Status:
- Analyzing: 0
- Approved: 1
- In Progress: 1
- Validated: 0
- Completed: 2
- Closed: 1
- Rejected: 0
- Failed: 0

By Type:
- Bug: 2
- Enhancement: 2
- NewFeature: 1

Average Reflexion Score: 8.7/10

---

## All Feedback Items

PF-001 | closed | Enhancement | Medium | 2026-01-24
   Title: "Color-coded stock levels"
   Artifacts: 8
   Reflexion: HIGH (92%)
   Session: feedback-sessions/2026-01-24_PrototypeFeedback-PF-001/

PF-002 | in_progress | Bug | Critical | 2026-01-25
   Title: "Save button not working"
   Artifacts: 4
   Reflexion: HIGH (88%)
   Session: feedback-sessions/2026-01-25_PrototypeFeedback-PF-002/

PF-003 | completed | Enhancement | Low | 2026-01-25
   Title: "Add tooltips to table headers"
   Artifacts: 3
   Reflexion: MEDIUM (75%)
   Session: feedback-sessions/2026-01-25_PrototypeFeedback-PF-003/

[...]

═══════════════════════════════════════════════════════════════
```

---

## Related Commands

- `/prototype-status` - Check prototype build progress
- `/prototype-qa` - Run QA validation on prototype
- `/prototype-reset` - Reset prototype state
- `/prototype-validate` - Validate prototype against Discovery
- `/prototype-resume` - Resume prototype build from checkpoint

---

## Debugging Commands (During Bug Feedback)

During Phase 2, STEP 3 (Bug Debugging), these sub-commands are available:

| Command | Action |
|---------|--------|
| `reproduce` | Define/update reproduction steps |
| `trace` | Trace data flow from symptom to root cause |
| `hypothesis: <theory>` | Propose root cause hypothesis |
| `confirm` | Accept current hypothesis and proceed |
| `investigate more` | Gather more evidence before hypothesis |

**Example debugging session**:

```
> reproduce
Steps to reproduce:
1. Open inventory form
2. Fill in item details
3. Click Save button
4. Nothing happens

> trace
Tracing from: Save button click
Found: src/screens/InventoryForm.tsx:45
Handler: handleSaveClick()
State: No state update detected
API: No API call triggered

Issue: onClick handler is defined but not connected to button

> hypothesis: The onClick handler exists but is not wired to the Save button
Root Cause Hypothesis: The onClick handler exists but is not wired to the Save button
Evidence: Line 45 defines handleSaveClick, but line 89 <Button> has no onClick prop

> confirm
✅ Hypothesis confirmed - proceeding to impact analysis
```

---

## Comparison with Discovery Feedback

| Aspect | Discovery Feedback | Prototype Feedback |
|--------|-------------------|--------------------|
| **Scope** | Documentation only (1 layer) | Documentation + Specs + Code (5 layers) |
| **ID Format** | FB-NNN | PF-NNN |
| **Debugging** | Not required | REQUIRED for Bug types |
| **Build Check** | N/A | Required for Layer 3 (Code) changes |
| **Session Location** | `traceability/feedback_sessions/discovery/` | `Prototype_X/feedback-sessions/` |
| **Registries** | discovery_traceability_register.json | screen_registry.json + prototype_traceability_register.json |
| **Quality Gates** | discovery_quality_gates.py --validate-checkpoint 11 | prototype_quality_gates.py --validate-feedback |
| **Complexity** | Lower (single layer) | Higher (5 layers + build verification) |

---

## Registry Schema

```json
{
  "schema_version": "2.0.0",
  "system_name": "{PROTOTYPE_NAME}",
  "stage": "prototype",
  "feedback_items": {
    "PF-001": {
      "title": "{brief_summary}",
      "type": "{Bug|Enhancement|NewFeature|UXIssue|VisualIssue|Clarification}",
      "severity": "{Critical|High|Medium|Low}",
      "status": "{analyzing|approved|in_progress|implemented|validated|completed|closed|rejected|failed}",
      "categories": ["CAT-DISC", "CAT-CODE", ...],
      "impact": {
        "chains_affected": N,
        "artifacts_affected": M,
        "layer_1_discovery": X,
        "layer_2_specs": Y,
        "layer_3_code": Z,
        "layer_4_registries": R,
        "layer_5_matrices": T,
        "confidence_level": "{HIGH|MEDIUM|LOW}",
        "reflexion_score": XX
      },
      "source": {
        "person": "{name}",
        "role": "{role}",
        "inputter": "{name}"
      },
      "lifecycle": {
        "created_at": "{ISO8601}",
        "analyzed_at": "{ISO8601}",
        "approved_at": "{ISO8601}",
        "approved_by": "{user}",
        "implementation_started_at": "{ISO8601}",
        "implementation_completed_at": "{ISO8601}",
        "validated_at": "{ISO8601}",
        "completed_at": "{ISO8601}",
        "closed_at": "{ISO8601}",
        "rejected_at": "{ISO8601}",
        "rejected_by": "{user}",
        "rejection_reason": "{reason}"
      },
      "implementation": {
        "plan_selected": "{Option A|Option B|Option C|Custom}",
        "steps_total": N,
        "steps_completed": N,
        "resume_point": "{step_N}",
        "files_changed": ["{paths}"]
      },
      "validation": {
        "plan_compliance": true|false,
        "content_valid": true|false,
        "traceability_intact": true|false,
        "build_successful": true|false,
        "reflexion_consensus_score": X.X,
        "recommendations": ["{items}"],
        "issues": ["{items}"]
      },
      "session_folder": "feedback-sessions/{date}_PrototypeFeedback-{ID}/"
    }
  },
  "statistics": {
    "total_feedback": N,
    "by_status": {
      "analyzing": N,
      "approved": N,
      "in_progress": N,
      "implemented": N,
      "validated": N,
      "completed": N,
      "closed": N,
      "rejected": N,
      "failed": N
    },
    "by_type": {
      "Bug": N,
      "Enhancement": N,
      "NewFeature": N,
      "UXIssue": N,
      "VisualIssue": N,
      "Clarification": N
    },
    "by_severity": {
      "Critical": N,
      "High": N,
      "Medium": N,
      "Low": N
    },
    "average_reflexion_score": X.X
  }
}
```

---

## Version Metadata (All Files)

All generated files include version metadata per VERSION_CONTROL_STANDARD.md:

```yaml
---
document_id: PF-{TYPE}-{NNN}
version: 1.0.0
created_at: {YYYY-MM-DD}
updated_at: {YYYY-MM-DD}
generated_by: Prototype_Feedback{Phase}
source_files:
  - {sources}
feedback_ref: "PF-{NNN}"
change_history:
  - version: "1.0.0"
    date: "{YYYY-MM-DD}"
    author: "Prototype_Feedback{Phase}"
    changes: "{description}"
    feedback_ref: "PF-{NNN}"
---
```

---

## Prototype-Specific Validations

### Component Spec Validation

```bash
IF component spec modified:

   CHECK:
      ✓ component_id present
      ✓ props schema valid
      ✓ variants defined
      ✓ states documented
      ✓ accessibility requirements present
      ✓ Referenced in component-index.md

   IF code file exists:
      ✓ Props interface matches spec
      ✓ Variants implemented
```

### Screen Spec Validation

```bash
IF screen spec modified:

   CHECK:
      ✓ screen_id present
      ✓ layout defined
      ✓ components[] list present
      ✓ data_requirements defined
      ✓ Referenced in screen-index.md

   IF code file exists:
      ✓ Component imports match spec
      ✓ Data props match data_requirements
      ✓ Route exists in App.tsx
```

### Data Model Validation

```bash
IF data-model.md modified:

   CHECK:
      ✓ Entity schemas valid
      ✓ Relationships documented
      ✓ Validation rules present

   VERIFY DOWNSTREAM:
      ✓ api-contracts.json reflects entity schemas
      ✓ test-data/*.json includes new entities
      ✓ Code uses correct entity types
```

### Build Verification (REQUIRED for Code Changes)

```bash
IF layer_3_code > 0:

   cd Prototype_{PROTOTYPE_NAME}/prototype/
   npm run build

   IF exit_code != 0:
      ❌ Build failed
      APPEND build output to VALIDATION_REPORT.md
      MARK validation.build_successful = false
      ADD to validation issues

   ELSE:
      ✅ Build successful
      MARK validation.build_successful = true
```

---

## Reflexion Integration Summary

| Phase | Reflexion Application |
|-------|----------------------|
| **Phase 2: Impact Analysis** | Self-critique for completeness (40%), accuracy (35%), downstream impact (25%) with confidence scoring |
| **Phase 5: Plan Generation** | Evaluation of each option with X/10 scoring against completeness, consistency, quality criteria |
| **Phase 7: Post-Implementation** | Multi-perspective review (Requirements, Architecture, Quality) with consensus scoring |
| **Throughout** | Continuous confidence scoring, risk flagging, actionable recommendations |

---

## Key Differences from Other Stages

### vs. Discovery Feedback
- **5 layers** vs. 1 layer
- **Build verification** required
- **Code impact** analysis
- **Systematic debugging** for bugs

### vs. ProductSpecs Feedback
- **Prototype-specific artifacts** (components, screens vs. modules)
- **Visual/UX focus** vs. functional specs
- **Build verification** vs. spec consistency

### vs. SolArch Feedback
- **Implementation artifacts** vs. architectural decisions
- **Concrete code** vs. ADRs/diagrams
- **Immediate build impact** vs. long-term architecture

---

**END OF COMMAND**
