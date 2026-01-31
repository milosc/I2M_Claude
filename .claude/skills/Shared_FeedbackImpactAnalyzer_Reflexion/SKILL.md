---
name: Shared_FeedbackImpactAnalyzer_Reflexion
allowed-tools: Read
description: Reflexion-enhanced impact analysis for feedback across all stages with critical self-assessment
context: fork
agent: general-purpose
hooks:
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---

# Shared_FeedbackImpactAnalyzer_Reflexion

## Purpose

Perform comprehensive impact analysis for feedback/change requests with reflexion-powered critical thinking to ensure completeness and accuracy.

## Inputs

- `feedback_content`: Original feedback text
- `stage`: Stage name (discovery, prototype, productspecs, solarch, implementation)
- `system_name`: System name (e.g., InventorySystem)
- `stage_folder`: Path to stage output folder (e.g., ClientAnalysis_InventorySystem/)

## Outputs

- `impact_analysis.md`: Comprehensive impact report with:
  - Hierarchical traceability chains
  - Before/after content previews
  - Flat summary table
  - Reflexion self-critique
  - Confidence scoring

## Procedure

### Step 1: Parse Feedback

```
READ feedback_content

EXTRACT key entities:
- Artifact IDs explicitly mentioned (PP-X.X, JTBD-X.X, REQ-XXX, etc.)
- Artifact descriptions/titles
- Keywords indicating artifact types
- Change intent keywords (add, remove, modify, fix, update)

STORE as parsed_entities
```

### Step 2: Scan Artifacts

```
SCAN stage_folder recursively:
- Read all .md, .json, .yaml files
- Parse artifact IDs from content
- Extract titles/descriptions
- Build artifact inventory

CREATE artifact_map:
{
  "PP-1.1": {
    "type": "pain_point",
    "file": "ClientAnalysis_X/01-pain-points/warehouse-operators.md",
    "line": 45,
    "title": "Slow barcode scanning",
    "content_snippet": "...",
    "traces_to": ["JTBD-2.1", "REQ-015"]
  },
  ...
}
```

### Step 3: Match Feedback to Artifacts

```
FOR each parsed_entity:
   SEARCH artifact_map by:
   - Exact ID match
   - Title similarity (fuzzy matching)
   - Description keyword match
   - Content keyword match

   IF match found:
      ADD to affected_artifacts[]
      MARK as direct_impact

FOR each affected_artifact:
   READ traceability registries
   TRACE backwards (to sources: PP, JTBD)
   TRACE forwards (to implementations: Code, Tests)

   FOR each connected_artifact:
      IF not in affected_artifacts:
         ADD to affected_artifacts[]
         MARK as indirect_impact
```

### Step 4: Build Hierarchical Chains

```
IDENTIFY root artifacts (no incoming traces)
IDENTIFY leaf artifacts (no outgoing traces)

FOR each root_artifact:
   BUILD chain recursively:
      chain = [root]
      current = root

      WHILE current has outgoing traces:
         next = get_next_in_chain(current)
         IF next in affected_artifacts:
            chain.append(next)
            current = next
         ELSE:
            BREAK

   STORE chain with metadata

OUTPUT chains as tree structure:
   Chain N: ROOT → NODE1 → NODE2 → ... → LEAF
   ├─ [ID]: "[Title]"
   │  └─ Change: [CREATE|MODIFY|DELETE] - [Description]
   │     Before: [Content snippet]
   │     After:  [Expected content snippet]
   │     Reasoning: [Why this change is needed]
   │
   ├─ [Next artifact...]
   ...
```

### Step 5: Determine Change Types and Content

```
FOR each affected_artifact:

   CLASSIFY change_type:

   IF artifact doesn't exist yet:
      change_type = "CREATE"
      before_content = null
      after_content = [Generate expected structure based on stage templates]

   ELIF feedback mentions "remove" or "delete":
      change_type = "DELETE"
      before_content = [Current content snippet]
      after_content = null

   ELSE:
      change_type = "MODIFY"
      before_content = [Current content snippet - relevant section]
      after_content = [Proposed changes based on feedback]

   DETERMINE affected_sections:
      - Parse artifact structure (YAML frontmatter, markdown sections)
      - Identify which sections need changes
      - Note specific fields/keys to modify

   ESTIMATE change_complexity:
      - SIMPLE: Single field change
      - MODERATE: Multiple fields or section restructure
      - COMPLEX: Major refactoring or cascading changes

   STORE change_details = {
      type: change_type,
      before: before_content,
      after: after_content,
      sections: affected_sections,
      complexity: change_complexity,
      reasoning: [Why this change addresses feedback]
   }
```

### Step 6: Generate Flat Summary

```
GROUP affected_artifacts by type

CREATE summary_table:
| Artifact Type | Count | Create | Modify | Delete |
|---------------|-------|--------|--------|--------|
| Pain Points   | X     | 0      | X      | 0      |
| JTBDs         | X     | 0      | X      | 0      |
| Requirements  | X     | X      | X      | 0      |
| Screens       | X     | X      | 0      | 0      |
| Modules       | X     | 0      | X      | 0      |
| Tasks         | X     | 0      | X      | 0      |
| **TOTAL**     | **N** | **X**  | **Y**  | **0**  |
```

### Step 7: Reflexion Self-Critique

```
CRITICAL SELF-ASSESSMENT:

Question 1: Completeness - "Are these ALL affected artifacts?"

   STEP 1: Re-scan with alternative search terms
      - Use synonyms for key terms
      - Use related terminology
      - Check for indirect references

   STEP 2: Check for orphaned references
      - Search for artifact IDs in all files
      - Identify any artifacts referencing affected ones
      - Check bidirectional links

   STEP 3: Verify no missing chains
      - For each chain, verify all intermediate nodes present
      - Check for broken or dangling links
      - Validate against traceability registries

   RESULT: ✓ Complete | ⚠ Possibly incomplete | ❌ Gaps found
   REASONING: [Explain findings]
   MISSING: [List any potentially missed artifacts]

Question 2: Accuracy - "Are change types correct?"

   FOR each affected_artifact:
      ✓ If MODIFY: Verify artifact exists at specified path
      ✓ If DELETE: Verify artifact exists and deletion is appropriate
      ✓ If CREATE: Verify artifact doesn't already exist

   CHECK before/after content:
      ✓ Before content matches current file state?
      ✓ After content addresses feedback intent?
      ✓ Changes maintain format/schema consistency?

   RESULT: ✓ Accurate | ⚠ Minor issues | ❌ Major issues
   REASONING: [Explain findings]
   ISSUES: [List any inaccuracies]

Question 3: Downstream Impact - "Any cascading effects missed?"

   CHECK Implementation stage (if exists):
      - Search for task IDs related to affected artifacts
      - Check if code exists referencing affected items
      - Verify test coverage for affected functionality

   CHECK cross-stage dependencies:
      - Discovery affects Prototype?
      - Prototype affects ProductSpecs?
      - ProductSpecs affects Implementation?

   IDENTIFY additional impacts:
      - Tests that need updating
      - Documentation that needs syncing
      - JIRA items that need regeneration

   RESULT: ✓ All impacts identified | ⚠ Possible additional | ❌ Missed major impacts
   REASONING: [Explain findings]
   ADDITIONAL: [List any additional impacts]

Question 4: Risk Assessment

   IDENTIFY risks:
      - Traceability chain breaks: [Y/N] - [Details]
      - Regression risk: [LOW|MEDIUM|HIGH] - [Why]
      - Timeline impact: [None|Sprint|Release] - [Reasoning]
      - Data migration needed: [Y/N] - [Details]
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

OUTPUT Reflexion Critique:

Completeness Check: [✓/⚠/❌] [Reasoning]
Accuracy Check: [✓/⚠/❌] [Reasoning]
Downstream Impact: [✓/⚠/❌] [Reasoning]

Risk Assessment:
- Traceability: [risk]
- Regression: [risk]
- Timeline: [impact]
- Breaking Changes: [Y/N]

Confidence Level: {level} ({percentage}%)
Reasoning: [Detailed explanation of confidence level]

Warnings:
- [Warning 1 if any]
- [Warning 2 if any]

Recommendations:
- [Recommendation 1]
- [Recommendation 2]
```

### Step 8: Generate Output File

```
CREATE impact_analysis.md:

---
document_id: IMPACT-{feedback_id}
version: 1.0.0
created_at: {YYYY-MM-DD}
updated_at: {YYYY-MM-DD}
generated_by: Shared_FeedbackImpactAnalyzer_Reflexion
feedback_id: {feedback_id}
stage: {stage}
system_name: {system_name}
---

# Impact Analysis - {feedback_id}

## Original Feedback

{feedback_content}

## Classification

- **Type**: {Bug|Enhancement|NewFeature|Clarification|etc.}
- **Severity**: {Critical|High|Medium|Low}
- **Categories**: {CAT-XXX, CAT-YYY}

## Hierarchical Traceability Chains Affected

{For each chain, show tree structure with before/after}

## Flat Summary

{Summary table}

## Reflexion Self-Critique

{Reflexion output from Step 7}

## Recommended Next Steps

1. {Step 1}
2. {Step 2}
...

---

**Analysis completed at**: {timestamp}
**Confidence Level**: {level} ({percentage}%)

SAVE to feedback_sessions/{date}_{id}/impact_analysis.md
```

## Stage-Specific Adaptations

### Discovery

**Artifact Types**: PP, JTBD, Persona, Vision, Strategy, Screen, Component, DataField
**Registries**: `traceability/discovery_traceability_register.json`
**Templates**: Discovery document templates

### Prototype

**Layers**: Discovery, Specs (components/screens/interactions/data), Code (src/)
**Registries**: `traceability/screen_registry.json`, `traceability/prototype_traceability_register.json`
**Special**: Check for code file dependencies

### ProductSpecs

**Artifact Types**: MOD-XXX-XXX-NN, REQ-XXX, NFR-XXX, Test cases
**Registries**: `ProductSpecs_*/registry/*.json`
**Special**: JIRA regeneration impact assessment

### SolArch

**Artifact Types**: ADR-XXX, Components, Diagrams (C4), Quality Scenarios
**Registries**: `SolArch_*/registry/*.json`
**Special**: ADR consistency checking

### Implementation

**Artifact Types**: T-NNN (Tasks), Code files, Tests
**Registries**: `Implementation_*/task_registry.json`
**Special**: TDD impact, test coverage

## Error Handling

- **File not found**: Log warning, skip file, note in critique
- **Parse error**: Log warning, skip section, note in critique
- **Invalid ID format**: Flag in critique, suggest correction
- **Broken traceability**: Flag as HIGH risk in critique

## Output

Returns path to `impact_analysis.md` with full reflexion-enhanced analysis.

## Example Output

```markdown
# Impact Analysis - FB-003

## Original Feedback

"The warehouse operator persona should include night shift workers who have different pain points around visibility in low-light conditions."

## Classification

- **Type**: Enhancement
- **Severity**: Medium
- **Categories**: CAT-PERSONA, CAT-PAIN

## Hierarchical Traceability Chains Affected

### Chain 1: PP-1.3 → JTBD-1.1 → REQ-008 → SCR-002 → MOD-INV-UI-01

├─ **PP-1.3**: "Visibility issues during night shift"
│  └─ Change: CREATE - Add new pain point for night shift
│     Before: [Does not exist]
│     After:
│     ```yaml
│     pain_points:
│       - id: PP-1.3
│         category: visibility
│         severity: high
│         description: "Poor visibility in low-light conditions during night shift"
│         evidence: "Stakeholder feedback from warehouse operators"
│     ```
│     Reasoning: Feedback explicitly mentions night shift visibility issues
│
├─ **JTBD-1.1**: "Efficiently scan items in any lighting condition"
│  └─ Change: MODIFY - Update success criteria to include low-light
│     Before: "Scan items quickly during business hours"
│     After: "Scan items quickly in any lighting condition (day/night shifts)"
│     Sections: success_criteria, context
│     Reasoning: JTBD must reflect night shift context
│
├─ **REQ-008**: "Scanner visibility requirements"
│  └─ Change: MODIFY - Add acceptance criterion for low-light mode
│     Before: 3 acceptance criteria (general scanning)
│     After: 4 acceptance criteria + low-light mode requirement
│     Complexity: MODERATE
│
├─ **SCR-002**: "Inventory Scanning Screen"
│  └─ Change: MODIFY - Add low-light mode toggle component
│     Sections: components[], states[], data_requirements[]
│
└─ **MOD-INV-UI-01**: "Scanning Interface Module"
   └─ Change: MODIFY - Implement low-light color scheme
      Before: Single color scheme
      After: Dual color scheme (normal + low-light)

### Chain 2: PERSONA-02 → JTBD-1.1 (already in Chain 1)

├─ **PERSONA-02**: "Warehouse Operator - Day Shift"
│  └─ Change: MODIFY - Expand to include night shift variant
│     Before: "Works 8am-5pm, high ambient lighting"
│     After: Split into two variants (day shift + night shift)
│     Sections: context, pain_points, goals
│     Reasoning: Feedback requires night shift persona representation

## Flat Summary

| Artifact Type | Count | Create | Modify | Delete |
|---------------|-------|--------|--------|--------|
| Pain Points   | 1     | 1      | 0      | 0      |
| JTBDs         | 1     | 0      | 1      | 0      |
| Personas      | 1     | 0      | 1      | 0      |
| Requirements  | 1     | 0      | 1      | 0      |
| Screens       | 1     | 0      | 1      | 0      |
| Modules       | 1     | 0      | 1      | 0      |
| **TOTAL**     | **6** | **1**  | **5**  | **0**  |

## Reflexion Self-Critique

### Completeness Check: ✓ COMPLETE

Re-scanned with terms: ["night shift", "lighting", "visibility", "low-light"]
- Found all primary references
- Checked Implementation_* folder: No existing tasks for this feature
- Verified all traceability chains complete

Reasoning: Comprehensive scan found 6 affected artifacts across 2 chains. No orphaned references detected.

### Accuracy Check: ✓ ACCURATE

- All MODIFY artifacts verified to exist at specified paths
- CREATE artifact (PP-1.3) confirmed not to exist currently
- Before/after content matches current file states
- No schema inconsistencies detected

Reasoning: All artifact paths validated. Content snippets match current files. Proposed changes maintain YAML/Markdown format consistency.

### Downstream Impact: ⚠ POSSIBLE ADDITIONAL

Checked Implementation stage: No current tasks found
**Potential additional impacts**:
- Design system may need low-light color tokens
- Accessibility testing requirements may expand
- User testing plan should include night shift scenarios

Reasoning: While primary artifacts identified, some supporting materials (design tokens, test plans) may need updates. Flagged for consideration during planning phase.

### Risk Assessment

- **Traceability chain breaks**: NO - All chains remain intact
- **Regression risk**: LOW - Additive change, doesn't modify existing functionality
- **Timeline impact**: Sprint-level - Moderate effort, can fit in current sprint
- **Data migration needed**: NO - No schema changes to existing data
- **Breaking changes**: NO - Backward compatible

**SEVERITY**: MEDIUM
**MITIGATION**:
- Verify design token availability for low-light mode
- Include accessibility review in validation
- Plan for A/B testing with night shift workers

## Confidence Level: HIGH (90%)

**Reasoning**:
- Completeness: Thorough multi-pass scan found all direct and indirect impacts (✓)
- Accuracy: All artifact paths validated, content verified (✓)
- Downstream: Primary impacts identified, secondary impacts flagged (⚠)
- Confidence reduced by 10% due to potential design token and testing impacts

**Warnings**:
- Design system impact needs verification during planning
- Accessibility requirements may expand scope

**Recommendations**:
1. During planning, consult with design team on low-light color palette
2. Include accessibility specialist in validation phase
3. Plan user testing session with actual night shift workers

---

**Analysis completed at**: 2026-01-25 14:32:00
**Confidence Level**: HIGH (90%)
```

## Return

```json
{
  "status": "success",
  "output_file": "path/to/impact_analysis.md",
  "summary": {
    "chains_affected": 2,
    "artifacts_affected": 6,
    "create_count": 1,
    "modify_count": 5,
    "delete_count": 0,
    "confidence_level": "HIGH",
    "confidence_percentage": 90
  }
}
```
