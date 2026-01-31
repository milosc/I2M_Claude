# Feedback Workflow Template (Reflexion-Enhanced)

**Version**: 2.0.0 (Reflexion Integration)
**Purpose**: Shared template for all feedback/change request commands
**Stages**: Discovery, Prototype, ProductSpecs, SolArch, Implementation

---

## Design Principles

1. **Reflexion Throughout**: Critical self-assessment at every phase
2. **Explicit Impact**: Show exactly what changes (before/after content)
3. **Hierarchical Chains**: Display traceability chains as trees, not lists
4. **AskUserQuestion**: Structured user decisions with clear options
5. **Resumability**: Every phase has clear checkpoints for recovery

---

## Workflow Phases (Universal)

### Phase 1: Input Collection

```
1. PARSE arguments:
   - If resume <ID>: Load from registry, jump to Phase 6
   - If status: Display current state, exit
   - If list: Display all feedback items, exit
   - If file path: Read file content
   - If text: Use directly
   - If empty: Prompt for input

2. IDENTIFY target:
   - List available stage folders ({Stage}_*)
   - If multiple, prompt user to select
   - Store as SYSTEM_NAME

3. COLLECT metadata:
   - Source person (who provided feedback)
   - Source role (optional)
   - Inputter (who is entering it)
   - Date/time (auto)
```

### Phase 2: Impact Analysis (REFLEXION ENHANCED)

```
READ skill: {Stage}_FeedbackImpactAnalyzer_Reflexion

STEP 1: SCAN ARTIFACTS
   - Read all relevant artifacts in {Stage}_<SYSTEM_NAME>/
   - Parse traceability registries
   - Identify direct mentions (by ID or description)
   - Identify indirect dependencies (traceability chains)

STEP 2: CLASSIFY FEEDBACK
   - Type: Bug | Enhancement | NewFeature | Clarification | PriorityChange | etc.
   - Severity: Critical | High | Medium | Low
   - Categories: {Stage-specific categories}

STEP 3: BUILD HIERARCHICAL CHAINS
   For each affected artifact:
      TRACE backwards to source (PP/JTBD/Requirements)
      TRACE forwards to implementation (Code/Tests)

   OUTPUT FORMAT:
      Chain N: [SOURCE] → [INTERMEDIATE] → ... → [LEAF]
      ├─ [ID]: "[Title/Description]"
      │  └─ Change: [CREATE|MODIFY|DELETE] - [What changes]
      │     Before: [Exact content snippet]
      │     After:  [Exact content snippet]
      │
      ├─ [Next artifact in chain...]
      │  └─ Change: ...
      │
      └─ [Leaf artifact...]
         └─ Change: ...

STEP 4: REFLEXION SELF-CRITIQUE
   Critical Questions (MUST ANSWER):

   ✓ Completeness: "Are these ALL affected artifacts?"
     - Re-scan with different search terms
     - Check for orphaned references
     - Verify no missing chains

   ✓ Accuracy: "Are change types correct (CREATE/MODIFY/DELETE)?"
     - Verify each artifact exists (for MODIFY/DELETE)
     - Check if artifact needs creation (for CREATE)

   ✓ Downstream Impact: "Any cascading effects missed?"
     - Check Implementation stage for affected tasks
     - Check if code needs updates
     - Check if tests need updates

   ✓ Risk Assessment:
     - Traceability chain breaks?
     - Regression risk?
     - Timeline impact?

   Confidence Level: [LOW|MEDIUM|HIGH] (XX%)
   Reasoning: [Explain confidence level]
   Warnings: [List any risks or uncertainties]

STEP 5: CREATE SESSION FOLDER
   {Stage}_<SYSTEM>/feedback-sessions/<YYYY-MM-DD>_Feedback-<ID>/

STEP 6: SAVE OUTPUTS
   - FEEDBACK_ORIGINAL.md
   - impact_analysis.md (with reflexion critique)

OUTPUT TO USER:
═══════════════════════════════════════════════════════════════
 IMPACT ANALYSIS - {ID}
═══════════════════════════════════════════════════════════════

Feedback Type: {type}
Severity: {severity}
Categories: {categories}

## Hierarchical Traceability Chains Affected

[Show detailed chains as per STEP 3 format]

## Flat Summary

| Artifact Type | Count | Create | Modify | Delete |
|--------------|-------|--------|--------|--------|
| Pain Points  | X     | 0      | X      | 0      |
| JTBDs        | X     | 0      | X      | 0      |
| Requirements | X     | X      | X      | 0      |
| Screens      | X     | X      | 0      | 0      |
| Modules      | X     | 0      | X      | 0      |
| Tasks        | X     | 0      | X      | 0      |
| **TOTAL**    | **X** | **X**  | **X**  | **0**  |

## Reflexion Self-Critique

Completeness Check: ✓ [Reasoning]
Accuracy Check: ✓ [Reasoning]
Downstream Impact: ⚠ [Any warnings]

Confidence Level: HIGH (95%)
Reasoning: [Why this confidence level]
Warnings: [Any risks flagged]

═══════════════════════════════════════════════════════════════
```

### Phase 3: Registration

```
READ skill: {Stage}_FeedbackRegister

ASSIGN unique ID:
   - Discovery: FB-NNN
   - Prototype: PF-NNN
   - ProductSpecs: PSF-NNN
   - SolArch: SF-NNN
   - Implementation: CR-{SYSTEM}-NNN

CREATE/UPDATE registry:
   {stage}_feedback_registry.json OR change_request_registry.json

   Entry:
   {
     "id": "{ID}",
     "status": "analyzing",
     "type": "{type}",
     "severity": "{severity}",
     "categories": ["{CAT-XXX}"],
     "created_at": "{ISO8601}",
     "source_person": "{name}",
     "inputter": "{name}",
     "feedback_text": "{original}",
     "impact": {
       "chains_affected": N,
       "artifacts_affected": N,
       "confidence_level": "HIGH"
     },
     "lifecycle": {
       "analyzed_at": "{ISO8601}"
     }
   }

UPDATE _state/{stage}_config.json:
   active_feedback: "{ID}"

DISPLAY to user:
   Feedback Registered:
   - ID: {ID}
   - Type: {type}
   - Severity: {severity}
   - Artifacts Affected: {count}
   - Confidence: {level}
   - Session: {path}
```

### Phase 4: Approval Gate (ASKUSERQUESTION INTEGRATION)

```
PREPARE approval prompt using impact_analysis.md

USE AskUserQuestion:
   question: "Feedback {ID} affects {N} artifacts across {M} traceability chains with {SEVERITY} impact. Reflexion confidence: {LEVEL}. Review the detailed impact analysis above. How should we proceed?"
   header: "Approval"
   options:
     - label: "Approve (Recommended)"
       description: "Proceed to implementation planning. Estimated effort: {effort} based on chain complexity."
     - label: "Reject"
       description: "Mark feedback as rejected. No changes will be made. Requires rejection reason."
     - label: "Modify Scope"
       description: "Adjust which artifacts to change before proceeding to planning."
     - label: "Request Deeper Analysis"
       description: "Reflexion confidence is {LEVEL} - request more investigation before deciding."

HANDLE responses:

IF "Approve":
   UPDATE registry:
      status = "approved"
      lifecycle.approved_at = NOW()
      lifecycle.approved_by = "{user}"
   CONTINUE to Phase 5

IF "Reject":
   ASK for rejection reason (text input)
   UPDATE registry:
      status = "rejected"
      lifecycle.rejected_at = NOW()
      lifecycle.rejected_by = "{user}"
      lifecycle.rejection_reason = "{reason}"
   GENERATE FEEDBACK_SUMMARY.md
   END WORKFLOW

IF "Modify Scope":
   USE AskUserQuestion with multiSelect:
      question: "Select which artifact types to EXCLUDE from implementation:"
      options: [List all artifact types found in impact analysis]

   RE-GENERATE impact_analysis.md with reduced scope
   RETURN to Approval Gate

IF "Request Deeper Analysis":
   PROMPT: "What specific areas need more investigation?"
   RE-RUN Phase 2 with focused analysis
   RETURN to Approval Gate
```

### Phase 5: Implementation Planning (REFLEXION ENHANCED)

```
READ skill: {Stage}_FeedbackPlanGenerator_Reflexion

STEP 1: GENERATE OPTIONS (Minimum 2)

   For each option:
      - List exact steps (with file paths)
      - Show before/after content for each change
      - List traceability updates needed
      - Estimate effort
      - Assess risk

   STEP 2: REFLEXION EVALUATION PER OPTION

      FOR each option:

         Completeness: Does it address ALL affected artifacts?
            ✓ = All chains addressed
            ⚠ = Some artifacts skipped
            ❌ = Major gaps

         Consistency: Does it maintain traceability integrity?
            ✓ = All chains remain valid
            ⚠ = Some manual fixes needed
            ❌ = Breaks chains

         Quality: Does it follow framework standards?
            ✓ = Follows all conventions
            ⚠ = Minor deviations
            ❌ = Violates standards

         Risk Assessment:
            [List specific risks]

         Effort Estimate:
            {time} (based on step count and complexity)

         SCORE: X/10
         RECOMMENDATION: APPROVE | APPROVE WITH CAUTION | REJECT
         REASONING: [Explain score]

STEP 3: SAVE OPTIONS
   implementation_options.md with reflexion scores

OUTPUT FORMAT:
═══════════════════════════════════════════════════════════════
 IMPLEMENTATION OPTIONS - WITH REFLEXION EVALUATION
═══════════════════════════════════════════════════════════════

## Option A: {Name}

### Steps (Detailed with Before/After)

Step 1: Update {Artifact-ID} - {Description}
   File: {exact/path/to/file.md}
   Section: {section_name}
   Line: {line_range}

   BEFORE:
   ```yaml
   [exact content]
   ```

   AFTER:
   ```yaml
   [exact content with changes]
   ```

   Traceability Update:
   - Registry: {registry_path}
   - Field: {field_name}
   - Change: {description}

Step 2: ...
[Continue for all steps]

### Reflexion Evaluation

Completeness: ✓ / ⚠ / ❌  [Reasoning]
Consistency: ✓ / ⚠ / ❌  [Reasoning]
Quality: ✓ / ⚠ / ❌  [Reasoning]

Risk Assessment:
- Risk 1: [description]
- Risk 2: [description]

Effort: {time estimate}
Score: X/10
Recommendation: APPROVE | APPROVE WITH CAUTION | REJECT
Reasoning: [Why this score]

---

## Option B: {Name}
[Same structure]

---

## Option C: Custom Plan
User provides their own plan - will be evaluated by reflexion before execution.

═══════════════════════════════════════════════════════════════

USE AskUserQuestion:
   question: "Three implementation options generated with reflexion scores. Option {X} scored {Y}/10 and {reasoning}. Which approach?"
   header: "Plan"
   options:
     - label: "Option A: {Name} (Recommended)"
       description: "{N} steps, {M} artifacts, {status}. Effort: {time}. Reflexion score: {X}/10"
     - label: "Option B: {Name}"
       description: "{N} steps, {M} artifacts, {status}. Effort: {time}. Reflexion score: {X}/10"
     - label: "Custom Plan"
       description: "Provide your own plan - will be evaluated by reflexion before execution"

HANDLE responses:

IF "Option A" or "Option B":
   STORE selection in _state/{stage}_config.json:
      feedback_plan_selection: "{option}"
      feedback_session_id: "{session_id}"

   CREATE implementation_plan.md:
      - Mark selected option
      - Copy full step details
      - Include reflexion evaluation

   CONTINUE to Phase 6

IF "Custom Plan":
   PROMPT: "Provide your custom implementation plan (step-by-step):"

   RECEIVE custom_plan

   EVALUATE using reflexion (same criteria as Option A/B)

   DISPLAY evaluation results

   ASK: "Custom plan scored {X}/10. Proceed or revise?"

   IF revise: Loop back to custom plan input
   IF proceed: Save and continue
```

### Phase 6: Implementation

```
READ skill: {Stage}_FeedbackImplementer

LOAD implementation_plan.md

CREATE BACKUP:
   - For each file in plan, create {file}.backup

UPDATE registry:
   status = "in_progress"
   lifecycle.implementation_started_at = NOW()

EXECUTE in order:
   FOR each step IN plan:

      1. READ current file
      2. VERIFY current state matches "BEFORE" content
         IF mismatch:
            LOG warning
            ASK user: "File state differs from plan. Continue anyway?"

      3. APPLY changes (Edit/Write tool)
      4. UPDATE version metadata in frontmatter
      5. ADD change_history entry with {feedback_id} reference
      6. LOG to implementation_log.md:
         - Timestamp
         - Step number
         - File modified
         - Change description
         - Success/Failure

      7. UPDATE registries (if step includes traceability updates)

      8. SET resume point

      IF step fails:
         LOG failure with details
         MARK step as "failed" in log
         ASK user:
            question: "Step {N} failed: {error}. How to proceed?"
            options:
              - "Skip and Continue" (skip-and-continue pattern)
              - "Retry Step"
              - "Abort and Save Resume Point"

UPDATE registry:
   status = "implemented"
   lifecycle.implementation_completed_at = NOW()
   resume_point = null

SAVE implementation_log.md
CREATE files_changed.md (summary of all modifications)
```

### Phase 7: Validation (REFLEXION ENHANCED)

```
READ skill: {Stage}_FeedbackReviewer_Reflexion

STEP 1: PLAN COMPLIANCE VALIDATION

   ✓ All steps executed?
   ✓ All files modified as specified?
   ✓ Any unexpected changes?
   ✓ Backup files exist?

STEP 2: CONTENT VALIDATION

   FOR each modified file:
      ✓ Before/After matches implementation_plan.md?
      ✓ Frontmatter version incremented?
      ✓ change_history entry added with {feedback_id}?
      ✓ File format valid (YAML/JSON/Markdown)?

STEP 3: TRACEABILITY VALIDATION

   ✓ All registries updated?
   ✓ All traceability chains intact?
   ✓ No broken references?
   ✓ No orphaned artifacts?

STEP 4: STAGE-SPECIFIC VALIDATION

   {Stage-specific quality gates - see below}

STEP 5: REFLEXION MULTI-PERSPECTIVE REVIEW

   Perspective 1: REQUIREMENTS VALIDATOR
      - Does implementation address original feedback?
      - Are acceptance criteria met?
      - Any scope creep?
      Score: X/10
      Issues: [list]

   Perspective 2: SOLUTION ARCHITECT
      - Is the approach sound?
      - Does it follow architecture patterns?
      - Any technical debt introduced?
      Score: X/10
      Issues: [list]

   Perspective 3: CODE QUALITY REVIEWER
      - Is content clean and maintainable?
      - Are conventions followed?
      - Documentation updated?
      Score: X/10
      Issues: [list]

   CONSENSUS CALCULATION:
      Average Score: X/10

      IF score >= 8:
         Recommendation: ACCEPT
      ELIF score >= 6:
         Recommendation: ACCEPT WITH MINOR FIXES
      ELSE:
         Recommendation: REVISE AND REIMPLEMENT

STEP 6: RUN QUALITY GATES (if available)

   python3 .claude/hooks/{stage}_quality_gates.py \
      --validate-feedback {ID} \
      --dir {Stage}_<SYSTEM>/

SAVE VALIDATION_REPORT.md:
   - Plan compliance results
   - Content validation results
   - Traceability validation results
   - Reflexion multi-perspective review
   - Quality gate results
   - Overall pass/fail
   - Action items (if any)

UPDATE registry:
   IF all validations pass:
      status = "validated"
      lifecycle.validated_at = NOW()
      validation_score = {average}
   ELSE:
      status = "failed"
      lifecycle.failed_at = NOW()
      validation_issues = [{issues}]

DISPLAY to user:
═══════════════════════════════════════════════════════════════
 VALIDATION RESULTS - {ID}
═══════════════════════════════════════════════════════════════

Plan Compliance: ✓ PASS
Content Validation: ✓ PASS
Traceability: ✓ PASS

Reflexion Multi-Perspective Review:
├─ Requirements Validator: {score}/10
├─ Solution Architect: {score}/10
└─ Code Quality Reviewer: {score}/10

Consensus Score: {average}/10
Recommendation: {recommendation}

{If issues exist:}
Action Items:
1. {issue_1}
2. {issue_2}

═══════════════════════════════════════════════════════════════

IF score < 8:
   USE AskUserQuestion:
      question: "Validation identified {N} issues with consensus score {X}/10. How to proceed?"
      header: "Decision"
      options:
         - "Accept As-Is" (override validation)
         - "Fix Issues Now" (iterate Phase 6)
         - "Mark As Incomplete" (close with known issues)
```

### Phase 8: Completion

```
GENERATE FEEDBACK_SUMMARY.md:

   # Feedback Summary - {ID}

   ## Original Feedback
   [From FEEDBACK_ORIGINAL.md]

   ## Impact Analysis Summary
   - Chains Affected: {N}
   - Artifacts Modified: {M}
   - Confidence Level: {level}

   ## Implementation Approach
   - Selected Plan: {option_name}
   - Reflexion Score: {X}/10
   - Effort: {time}

   ## Changes Made
   [From files_changed.md]

   ## Validation Results
   - Plan Compliance: PASS/FAIL
   - Content Validation: PASS/FAIL
   - Traceability: PASS/FAIL
   - Reflexion Consensus: {X}/10

   ## Timeline
   | Phase | Duration |
   |-------|----------|
   | Analysis | {time} |
   | Planning | {time} |
   | Implementation | {time} |
   | Validation | {time} |
   | Total | {time} |

   ## Status
   {Final status and any action items}

UPDATE registry:
   status = "completed"
   lifecycle.completed_at = NOW()

USE AskUserQuestion:
   question: "Feedback {ID} processing complete with status: {status}. Close feedback?"
   header: "Closure"
   options:
      - "Close" (mark as closed)
      - "Keep Open" (leave for review)

IF "Close":
   UPDATE registry:
      status = "closed"
      lifecycle.closed_at = NOW()

DISPLAY completion summary:
═══════════════════════════════════════════════════════════════
 FEEDBACK PROCESSING COMPLETE - {ID}
═══════════════════════════════════════════════════════════════

ID: {ID}
Status: {status}
Type: {type}

Statistics:
- Artifacts Modified: {N}
- Traceability Chains Updated: {M}
- Reflexion Consensus Score: {X}/10

Session Folder: {path}

Artifacts Generated:
├─ FEEDBACK_ORIGINAL.md
├─ impact_analysis.md (with reflexion critique)
├─ implementation_options.md (with reflexion scores)
├─ implementation_plan.md
├─ implementation_log.md
├─ files_changed.md
├─ VALIDATION_REPORT.md (with multi-perspective review)
└─ FEEDBACK_SUMMARY.md

═══════════════════════════════════════════════════════════════
```

---

## Stage-Specific Adaptations

### Discovery (FB-NNN)

**Artifacts**: Personas, JTBDs, Vision, Strategy, Screens, Components, Data Fields
**Registries**: `traceability/discovery_traceability_register.json`
**Quality Gate**: `discovery_quality_gates.py --validate-checkpoint 11`

### Prototype (PF-NNN)

**Layers** (ALL must be checked):
1. Discovery (ClientAnalysis_*)
2. Prototype Specs (Prototype_*/01-04/)
3. Code (prototype/src/)
4. Registries (traceability/*)
5. Matrices (helperFiles/TRACEABILITY_*)

**Special**: Bug feedback requires systematic debugging before planning

### ProductSpecs (PSF-NNN)

**Artifacts**: Modules (MOD-*), Requirements, NFRs, Tests
**Impact**: May require JIRA regeneration
**Registries**: `ProductSpecs_*/registry/*.json`

### SolArch (SF-NNN)

**Artifacts**: ADRs, Components, Diagrams, Quality Scenarios
**Registries**: `SolArch_*/registry/*.json`
**Special**: ADR consistency validation required

### Implementation (CR-{SYSTEM}-NNN)

**Integration**: Kaizen (5 Whys, Fishbone, A3) + Reflexion + PDCA + TDD
**See**: `htec-sdd-changerequest.md` for full workflow

---

## Resume Capability (All Stages)

```
COMMAND: /{stage}-feedback resume {ID}

LOAD from registry:
   - Feedback details
   - Current status
   - Resume point (if any)

VALIDATE state:
   - Session folder exists
   - implementation_log.md exists
   - Files match expected state

DETERMINE resume phase:
   IF status == "analyzing":
      RESUME at Phase 2
   ELIF status == "approved":
      RESUME at Phase 5
   ELIF status == "in_progress":
      RESUME at Phase 6 (from resume_point)
   ELIF status == "implemented":
      RESUME at Phase 7
   ELSE:
      ERROR: Cannot resume from status {status}

ADD resume marker to log
CONTINUE workflow from resume phase
```

---

## Error Handling (Universal)

| Error Type | Action |
|------------|--------|
| No stage folder found | Error: Run /{stage} command first |
| File read failure during analysis | Skip file, note in impact_analysis.md |
| File write failure during implementation | Log failure, save resume point, offer retry |
| Validation failure | Show issues, offer fix/accept/abort options |
| Traceability breaks | Warn, attempt auto-fix, flag for manual review |

**Skip-and-Continue Pattern**: For technical errors (parse failures, missing files), log and skip. For quality violations (missing IDs, broken chains), BLOCK and fix.

---

## Version Metadata (All Files)

```yaml
---
document_id: {appropriate_id}
version: {MAJOR.MINOR.PATCH}
created_at: {YYYY-MM-DD}
updated_at: {YYYY-MM-DD}
generated_by: {skill_or_command}
source_files:
  - {sources}
change_history:
  - version: "{version}"
    date: "{YYYY-MM-DD}"
    author: "{skill_or_command}"
    changes: "{description}"
    feedback_ref: "{feedback_id}"
---
```

---

## Registry Schema (Universal Structure)

```json
{
  "schema_version": "2.0.0",
  "system_name": "{SystemName}",
  "stage": "{stage}",
  "feedback_items": {
    "{ID}": {
      "title": "{brief_title}",
      "type": "{type}",
      "severity": "{severity}",
      "status": "{status}",
      "categories": ["{CAT-XXX}"],
      "impact": {
        "chains_affected": N,
        "artifacts_affected": N,
        "confidence_level": "{HIGH|MEDIUM|LOW}",
        "reflexion_score": X.X
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
        "plan_selected": "{option}",
        "steps_total": N,
        "steps_completed": N,
        "resume_point": "{step_N}",
        "files_changed": ["{paths}"]
      },
      "validation": {
        "plan_compliance": true|false,
        "content_valid": true|false,
        "traceability_intact": true|false,
        "reflexion_consensus_score": X.X,
        "recommendations": ["{items}"],
        "issues": ["{items}"]
      }
    }
  },
  "statistics": {
    "total_feedback": N,
    "by_status": {...},
    "by_type": {...},
    "by_severity": {...},
    "average_reflexion_score": X.X
  }
}
```

---

## Session Folder Structure (Universal)

```
{Stage}_<SystemName>/feedback-sessions/
├── {stage}_feedback_registry.json
└── <YYYY-MM-DD>_{Stage}Feedback-<ID>/
    ├── FEEDBACK_ORIGINAL.md
    ├── impact_analysis.md              # With reflexion critique
    ├── implementation_options.md       # With reflexion scores
    ├── implementation_plan.md          # Selected plan with before/after
    ├── implementation_log.md           # Step-by-step execution log
    ├── files_changed.md                # Summary of modifications
    ├── VALIDATION_REPORT.md            # With multi-perspective review
    └── FEEDBACK_SUMMARY.md             # Final summary
```

---

## Reflexion Integration Summary

| Phase | Reflexion Application |
|-------|----------------------|
| **Impact Analysis** | Self-critique for completeness, accuracy, downstream impact |
| **Plan Generation** | Evaluation of each option against criteria (completeness, consistency, quality) |
| **Post-Implementation** | Multi-perspective review (requirements, architecture, quality) |
| **Throughout** | Confidence scoring, risk flagging, recommendation generation |

---

## AskUserQuestion Integration Points

1. **Approval Gate** (Phase 4): Approve/Reject/Modify/Investigate
2. **Plan Selection** (Phase 5): Choose from scored options
3. **Custom Plan Approval** (Phase 5): Proceed with custom plan after evaluation
4. **Scope Modification** (Phase 4): Select artifacts to exclude
5. **Validation Override** (Phase 7): Accept/Fix/Mark Incomplete
6. **Closure** (Phase 8): Close or Keep Open

---

**END OF TEMPLATE**
