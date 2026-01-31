---
name: Shared_FeedbackPlanGenerator_Reflexion
allowed-tools: Read
description: Reflexion-enhanced implementation plan generation with option evaluation and before/after content specification
context: fork
agent: general-purpose
hooks:
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---

# Shared_FeedbackPlanGenerator_Reflexion

## Purpose

Generate multiple implementation options for feedback/change requests with reflexion-powered evaluation to score each option's completeness, consistency, and quality.

## Inputs

- `impact_analysis_path`: Path to impact_analysis.md file
- `feedback_id`: Feedback identifier (FB-NNN, PF-NNN, etc.)
- `stage`: Stage name (discovery, prototype, productspecs, solarch, implementation)
- `system_name`: System name
- `stage_folder`: Path to stage output folder

## Outputs

- `implementation_options.md`: Comprehensive options document with:
  - Minimum 2 options (3 recommended)
  - Detailed steps with before/after content for each
  - Reflexion evaluation score (X/10) for each
  - Recommendation (APPROVE/APPROVE WITH CAUTION/REJECT)

## Procedure

### Step 1: Load Impact Analysis

```
READ impact_analysis_path

EXTRACT:
- affected_artifacts[] (all artifacts with change details)
- traceability_chains[]
- confidence_level
- complexity_assessment
- risk_factors[]

STORE as impact_data
```

### Step 2: Generate Option A - Minimal/Quick

```
STRATEGY: Address only highest-priority artifacts with minimal scope

SELECT artifacts:
   FOR each chain IN traceability_chains:
      INCLUDE only root artifacts (sources like PP, JTBD)
      EXCLUDE intermediate nodes
      EXCLUDE leaf nodes (implementation artifacts)

RATIONALE: Fast turnaround, limited scope, addresses immediate feedback

GENERATE steps:
   FOR each selected_artifact:
      CREATE step:
         step_number: N
         artifact_id: {ID}
         artifact_title: {title}
         file_path: {exact/path/to/file.md}
         section: {section_name}
         line_range: {start}-{end}

         action: {CREATE|MODIFY|DELETE}

         before_content: |
            [Exact current content with line numbers]

         after_content: |
            [Exact proposed content with changes highlighted]

         traceability_updates:
            - registry: {registry_path}
              field: {field_name}
              change: {description}

         version_update:
            current: {X.Y.Z}
            new: {X.Y.Z+1}
            reason: {MAJOR|MINOR|PATCH change}

         estimated_time: {minutes}

CALCULATE effort:
   total_steps: COUNT(steps)
   total_time: SUM(step.estimated_time)

ASSESS risk:
   - Breaks traceability chains? YES (many chains incomplete)
   - Regression potential? LOW
   - Technical debt? HIGH (incomplete implementation)
```

### Step 3: Generate Option B - Comprehensive/Standard (RECOMMENDED)

```
STRATEGY: Address ALL affected artifacts maintaining complete traceability

SELECT artifacts:
   INCLUDE all artifacts from impact_analysis

RATIONALE: Complete implementation, maintains integrity, addresses root causes

GENERATE steps:
   ORDER by dependency:
      1. Source artifacts first (PP, JTBD, Personas)
      2. Requirements/Specifications next
      3. Design/Screens next
      4. Implementation artifacts last (Modules, Code, Tests)

   FOR each artifact IN dependency_order:
      CREATE detailed_step:
         [Same structure as Option A, but for ALL artifacts]

         ADDITIONAL for MODIFY steps:
            affected_fields: [{field, old_value, new_value}]
            side_effects: [List any cascading changes]

CALCULATE effort:
   total_steps: COUNT(steps)
   total_time: SUM(step.estimated_time)

ASSESS risk:
   - Breaks traceability chains? NO
   - Regression potential? LOW
   - Technical debt? NONE
```

### Step 4: Generate Option C - Extended/Preventive

```
STRATEGY: Address artifacts + add preventive measures + improvements

SELECT artifacts:
   INCLUDE all from Option B
   ADD preventive artifacts:
      - Regression tests for affected functionality
      - Documentation updates
      - Related edge cases
      - Future-proofing measures

RATIONALE: Prevents future issues, comprehensive, high quality

GENERATE steps:
   [Same as Option B]
   PLUS additional steps for:
      - Regression test creation
      - Documentation updates
      - Related improvements identified during analysis

CALCULATE effort:
   total_steps: COUNT(steps)
   total_time: SUM(step.estimated_time)

ASSESS risk:
   - Breaks traceability chains? NO
   - Regression potential? VERY LOW (tests added)
   - Technical debt? NONE
```

### Step 5: Reflexion Evaluation - Per Option

```
FOR each option IN [Option_A, Option_B, Option_C]:

   === COMPLETENESS EVALUATION ===

   Question: "Does this option address ALL affected artifacts from impact analysis?"

   CHECK:
      affected_from_impact = impact_data.affected_artifacts[]
      addressed_in_option = option.steps[].artifact_id[]

      missing_artifacts = affected_from_impact - addressed_in_option

      IF missing_artifacts is empty:
         completeness_score = 10
         completeness_status = "✓ COMPLETE"
         completeness_reasoning = "All {N} artifacts from impact analysis addressed"
      ELIF len(missing_artifacts) < 20% of affected_from_impact:
         completeness_score = 7
         completeness_status = "⚠ MOSTLY COMPLETE"
         completeness_reasoning = "Missing {N} artifacts: {list}"
      ELSE:
         completeness_score = 3
         completeness_status = "❌ INCOMPLETE"
         completeness_reasoning = "Missing {N} artifacts: {list}"

   === CONSISTENCY EVALUATION ===

   Question: "Does this option maintain traceability integrity?"

   CHECK:
      FOR each chain IN traceability_chains:
         FOR each node IN chain:
            IF node in addressed_in_option:
               nodes_addressed += 1

         chain_coverage = nodes_addressed / total_nodes

         IF chain_coverage == 1.0:
            chains_intact += 1
         ELIF chain_coverage >= 0.5:
            chains_partial += 1
         ELSE:
            chains_broken += 1

      IF all chains intact:
         consistency_score = 10
         consistency_status = "✓ INTACT"
         consistency_reasoning = "All {N} traceability chains remain complete"
      ELIF chains_broken == 0:
         consistency_score = 6
         consistency_status = "⚠ PARTIAL"
         consistency_reasoning = "{N} chains partially addressed, {M} fully addressed"
      ELSE:
         consistency_score = 2
         consistency_status = "❌ BROKEN"
         consistency_reasoning = "{N} chains broken, {M} partial, {P} intact"

   === QUALITY EVALUATION ===

   Question: "Does this option follow framework standards and best practices?"

   CHECK quality_criteria:

      1. Version Metadata:
         ✓ All steps include version updates?
         ✓ Change history references feedback_id?
         Score: 0-2 points

      2. Before/After Content:
         ✓ All MODIFY steps show before/after?
         ✓ Content changes are clear and specific?
         Score: 0-2 points

      3. Traceability Updates:
         ✓ All steps update relevant registries?
         ✓ Registry field changes specified?
         Score: 0-2 points

      4. Format Consistency:
         ✓ Follows stage-specific templates?
         ✓ YAML/JSON/Markdown format correct?
         Score: 0-2 points

      5. Documentation:
         ✓ Each step includes reasoning?
         ✓ Side effects documented?
         Score: 0-2 points

      quality_score = SUM(criteria_scores) # Max 10

      IF quality_score >= 8:
         quality_status = "✓ HIGH QUALITY"
      ELIF quality_score >= 5:
         quality_status = "⚠ ACCEPTABLE"
      ELSE:
         quality_status = "❌ POOR QUALITY"

   === RISK ASSESSMENT ===

   risks = []

   IF consistency_status == "❌ BROKEN":
      risks.append({
         severity: "HIGH",
         description: "Breaks traceability chains",
         mitigation: "Manual chain repair required"
      })

   IF completeness_status == "❌ INCOMPLETE":
      risks.append({
         severity: "MEDIUM",
         description: "Leaves artifacts unaddressed",
         mitigation: "Follow-up work needed"
      })

   IF option.total_time > 4 hours:
      risks.append({
         severity: "LOW",
         description: "High effort estimate",
         mitigation: "Consider phased implementation"
      })

   FOR each risk:
      DEDUCT 1 point from total_score (max -3 points)

   === EFFORT ASSESSMENT ===

   effort_level =
      IF option.total_time < 1 hour: "LOW"
      ELIF option.total_time < 3 hours: "MEDIUM"
      ELSE: "HIGH"

   === CALCULATE FINAL SCORE ===

   base_score = (completeness_score * 0.4) +
                (consistency_score * 0.35) +
                (quality_score * 0.25)

   total_score = base_score - risk_penalty

   total_score = CLAMP(total_score, 0, 10)
   total_score = ROUND(total_score, 1)

   === GENERATE RECOMMENDATION ===

   IF total_score >= 8.0:
      recommendation = "APPROVE"
      recommendation_label = "✅ RECOMMENDED"
   ELIF total_score >= 6.0:
      recommendation = "APPROVE WITH CAUTION"
      recommendation_label = "⚠ USE WITH CARE"
   ELSE:
      recommendation = "REJECT"
      recommendation_label = "❌ NOT RECOMMENDED"

   reasoning = |
      Completeness: {completeness_status} ({completeness_score}/10)
      {completeness_reasoning}

      Consistency: {consistency_status} ({consistency_score}/10)
      {consistency_reasoning}

      Quality: {quality_status} ({quality_score}/10)
      {quality_reasoning}

      Risks: {len(risks)} identified
      {FOR each risk: - {risk.description}}

      Effort: {effort_level} ({option.total_time})

      Final Score: {total_score}/10
      Recommendation: {recommendation}

   STORE evaluation = {
      completeness: {score, status, reasoning},
      consistency: {score, status, reasoning},
      quality: {score, status, reasoning},
      risks: risks,
      effort: {level, time},
      total_score: total_score,
      recommendation: recommendation,
      reasoning: reasoning
   }
```

### Step 6: Rank Options

```
SORT options by total_score DESC

highest_score = options[0].evaluation.total_score

FOR each option:
   IF option.evaluation.total_score == highest_score:
      option.recommended = true
```

### Step 7: Generate Output File

```
CREATE implementation_options.md:

---
document_id: PLAN-{feedback_id}
version: 1.0.0
created_at: {YYYY-MM-DD}
updated_at: {YYYY-MM-DD}
generated_by: Shared_FeedbackPlanGenerator_Reflexion
feedback_id: {feedback_id}
stage: {stage}
system_name: {system_name}
---

# Implementation Options - {feedback_id}

## Context

Based on impact analysis showing:
- {N} traceability chains affected
- {M} artifacts requiring changes
- Confidence level: {level}

## Option Comparison

| Option | Steps | Artifacts | Effort | Score | Recommendation |
|--------|-------|-----------|--------|-------|----------------|
| A: {name} | {N} | {M} | {time} | {X}/10 | {emoji} {label} |
| B: {name} | {N} | {M} | {time} | {X}/10 | {emoji} {label} |
| C: {name} | {N} | {M} | {time} | {X}/10 | {emoji} {label} |

---

## Option A: {Name}

### Strategy
{strategy_description}

### Steps

#### Step 1: {Action} {Artifact-ID} - {Description}

**File**: `{exact/path/to/file.md}`
**Section**: {section_name}
**Line**: {start}-{end}
**Action**: {CREATE|MODIFY|DELETE}

**BEFORE:**
```yaml
{exact current content with line numbers}
```

**AFTER:**
```yaml
{exact proposed content with changes}
```

**Affected Fields:**
- `{field1}`: `{old_value}` → `{new_value}`
- `{field2}`: `{old_value}` → `{new_value}`

**Side Effects:**
- {side_effect_1}
- {side_effect_2}

**Traceability Updates:**
- **Registry**: `{registry_path}`
  - **Field**: `{field_name}`
  - **Change**: {description}

**Version Update:**
- Current: {X.Y.Z}
- New: {X.Y.Z+1}
- Reason: {change_type} - {justification}

**Estimated Time**: {minutes} minutes

---

#### Step 2: ...
[Continue for all steps]

---

### Reflexion Evaluation

#### Completeness: {status} ({score}/10)
{reasoning}

Missing Artifacts (if any):
- {artifact_1}
- {artifact_2}

#### Consistency: {status} ({score}/10)
{reasoning}

Traceability Chains:
- ✓ Intact: {N}
- ⚠ Partial: {M}
- ❌ Broken: {P}

#### Quality: {status} ({score}/10)
{reasoning}

Quality Criteria:
- Version Metadata: {✓/❌}
- Before/After Content: {✓/❌}
- Traceability Updates: {✓/❌}
- Format Consistency: {✓/❌}
- Documentation: {✓/❌}

#### Risk Assessment

Identified Risks:
1. **{Risk 1}** ({severity})
   - Description: {description}
   - Mitigation: {mitigation}

2. **{Risk 2}** ({severity})
   - Description: {description}
   - Mitigation: {mitigation}

#### Effort Assessment

- **Level**: {LOW|MEDIUM|HIGH}
- **Total Time**: {hours}h {minutes}m
- **Complexity**: {complexity_distribution}

#### Final Score: {X.X}/10

**Recommendation**: {recommendation_label}

**Reasoning**:
{detailed_reasoning}

---

## Option B: {Name}

[Same structure as Option A]

---

## Option C: {Name}

[Same structure as Option A, OR:]

### Custom Plan Instructions

If you choose to provide a custom plan:

1. Describe your implementation approach
2. List specific files and changes
3. Include before/after content for critical changes
4. Specify traceability update strategy

Your custom plan will be evaluated using the same reflexion criteria:
- Completeness (does it address all affected artifacts?)
- Consistency (does it maintain traceability?)
- Quality (does it follow standards?)
- Risk assessment
- Effort estimation

---

## Recommendation Summary

**Highest Scoring Option**: Option {X} - {name} ({score}/10)

**Rationale**: {why_this_option_is_best}

**Alternative**: If time is constrained, consider Option {Y} ({score}/10), but note: {warnings}

---

**Generated at**: {timestamp}
**Generator**: Shared_FeedbackPlanGenerator_Reflexion

SAVE to feedback_sessions/{date}_{id}/implementation_options.md
```

### Step 8: Return Summary

```
RETURN {
   "status": "success",
   "output_file": "path/to/implementation_options.md",
   "options": [
      {
         "id": "A",
         "name": "{name}",
         "steps": N,
         "artifacts": M,
         "effort": "{time}",
         "score": X.X,
         "recommendation": "{APPROVE|APPROVE WITH CAUTION|REJECT}",
         "recommended": true|false
      },
      ...
   ],
   "recommended_option": "{id}"
}
```

## Stage-Specific Adaptations

### Discovery
- Focus on documentation artifacts (personas, JTBDs, strategy docs)
- Version updates typically MINOR (content enhancements)
- Low regression risk

### Prototype
- Multi-layer planning (Discovery → Specs → Code)
- Must consider all 5 layers in comprehensive options
- Code changes require build verification steps

### ProductSpecs
- Module spec changes may trigger JIRA regeneration
- Test case updates critical for traceability
- NFR impacts need explicit handling

### SolArch
- ADR changes require consistency checks across related ADRs
- Component changes may affect multiple diagrams
- Quality scenario updates need validation

### Implementation
- TDD cycle integration required (RED-GREEN-REFACTOR)
- Test coverage maintenance critical
- Code review steps included

## Example Output

```markdown
# Implementation Options - FB-003

## Context

Based on impact analysis showing:
- 2 traceability chains affected
- 6 artifacts requiring changes
- Confidence level: HIGH (90%)

## Option Comparison

| Option | Steps | Artifacts | Effort | Score | Recommendation |
|--------|-------|-----------|--------|-------|----------------|
| A: Minimal Update | 2 | 2 | 30m | 3.5/10 | ❌ NOT RECOMMENDED |
| B: Comprehensive | 15 | 6 | 2.5h | 9.2/10 | ✅ RECOMMENDED |
| C: Extended Prevention | 22 | 8 | 4h | 8.5/10 | ⚠ USE WITH CARE |

---

## Option A: Minimal Update

### Strategy
Address only immediate feedback by updating persona and pain point descriptions. Skip downstream artifacts to minimize effort.

### Steps

#### Step 1: MODIFY PP-1.3 - Add night shift pain point

**File**: `ClientAnalysis_InventorySystem/01-pain-points/warehouse-operators.md`
**Section**: pain_points array
**Line**: 45-62
**Action**: MODIFY

**BEFORE:**
```yaml
pain_points:
  - id: PP-1.1
    category: performance
    severity: high
    description: "Barcode scanner slow on network lag"
  - id: PP-1.2
    category: usability
    severity: medium
    description: "Interface confusing for new users"
```

**AFTER:**
```yaml
pain_points:
  - id: PP-1.1
    category: performance
    severity: high
    description: "Barcode scanner slow on network lag"
  - id: PP-1.2
    category: usability
    severity: medium
    description: "Interface confusing for new users"
  - id: PP-1.3
    category: visibility
    severity: high
    description: "Poor visibility in low-light conditions during night shift"
    evidence: "Stakeholder feedback from warehouse operators"
    affected_roles: ["Warehouse Operator - Night Shift"]
```

**Affected Fields:**
- `pain_points`: Added new entry PP-1.3

**Side Effects:**
- Traceability registry will show PP-1.3 without downstream connections (orphaned)

**Traceability Updates:**
- **Registry**: `traceability/discovery_traceability_register.json`
  - **Field**: `pain_points`
  - **Change**: Add entry for PP-1.3 with source: "Stakeholder Feedback"

**Version Update:**
- Current: 1.2.0
- New: 1.3.0
- Reason: MINOR - Added new pain point

**Estimated Time**: 15 minutes

---

#### Step 2: MODIFY PERSONA-02 - Update persona description

**File**: `ClientAnalysis_InventorySystem/02-research/personas/warehouse-operator.md`
**Section**: Context
**Line**: 12-18
**Action**: MODIFY

**BEFORE:**
```yaml
context:
  work_environment: "Large warehouse with high ceilings and fluorescent lighting"
  shift: "Day shift (8am-5pm)"
  typical_day: "Receiving shipments, scanning items, updating inventory"
```

**AFTER:**
```yaml
context:
  work_environment: "Large warehouse with high ceilings and variable lighting"
  shift: "Day shift (8am-5pm) or Night shift (8pm-5am)"
  typical_day: "Receiving shipments, scanning items, updating inventory in varying lighting conditions"
  lighting_note: "Night shift workers experience reduced visibility and rely on task lighting"
```

**Affected Fields:**
- `context.work_environment`: Added "variable lighting"
- `context.shift`: Added night shift option
- `context.typical_day`: Added lighting context
- `context.lighting_note`: New field

**Side Effects:**
- None (persona is source artifact)

**Traceability Updates:**
- **Registry**: `traceability/discovery_traceability_register.json`
  - **Field**: `personas.PERSONA-02`
  - **Change**: Mark as updated with feedback_ref: "FB-003"

**Version Update:**
- Current: 1.1.0
- New: 1.2.0
- Reason: MINOR - Enhanced persona context

**Estimated Time**: 15 minutes

---

### Reflexion Evaluation

#### Completeness: ❌ INCOMPLETE (3/10)

**Reasoning**: Only 2 out of 6 affected artifacts addressed. Missing:
- JTBD-1.1 (not updated to reflect night shift context)
- REQ-008 (no acceptance criteria for low-light mode)
- SCR-002 (screen spec doesn't include low-light toggle)
- MOD-INV-UI-01 (module spec unchanged)

This creates orphaned artifacts and incomplete traceability chains.

**Missing Artifacts:**
- JTBD-1.1: "Efficiently scan items in any lighting condition"
- REQ-008: "Scanner visibility requirements"
- SCR-002: "Inventory Scanning Screen"
- MOD-INV-UI-01: "Scanning Interface Module"

#### Consistency: ❌ BROKEN (2/10)

**Reasoning**: Traceability chains severely broken.

**Traceability Chains:**
- ✓ Intact: 0
- ⚠ Partial: 0
- ❌ Broken: 2 (PP-1.3 → [orphaned], PERSONA-02 → [incomplete])

Chain 1 (PP-1.3 → JTBD → REQ → SCR → MOD): Only root node addressed, all downstream missing.
Chain 2 (PERSONA-02 → JTBD → ...): Root updated but not propagated.

This violates framework traceability requirements and will cause validation failures.

#### Quality: ⚠ ACCEPTABLE (6/10)

**Reasoning**: Steps are well-formed but incomplete scope undermines quality.

**Quality Criteria:**
- Version Metadata: ✓ (proper version increments)
- Before/After Content: ✓ (clear content specified)
- Traceability Updates: ⚠ (registries updated but chains broken)
- Format Consistency: ✓ (follows YAML format)
- Documentation: ✓ (steps well-documented)

While individual steps are high quality, the incomplete implementation creates technical debt.

#### Risk Assessment

**Identified Risks:**

1. **Traceability Chain Breaks** (HIGH)
   - Description: Both chains broken, orphaned pain point, incomplete persona propagation
   - Mitigation: Follow Option B to complete chains

2. **Validation Failure** (HIGH)
   - Description: Discovery quality gates will fail on traceability check
   - Mitigation: Manual chain repair or full reimplementation

3. **Downstream Confusion** (MEDIUM)
   - Description: Prototype/ProductSpecs stages won't have proper Discovery inputs
   - Mitigation: Document gaps and plan follow-up work

#### Effort Assessment

- **Level**: LOW
- **Total Time**: 30 minutes
- **Complexity**: 2 simple modifications

#### Final Score: 3.5/10

**Recommendation**: ❌ NOT RECOMMENDED

**Reasoning**:
While this option provides quick turnaround (30 minutes), it:
- Leaves 67% of affected artifacts unaddressed (❌ Completeness)
- Breaks all traceability chains (❌ Consistency)
- Creates technical debt requiring future fixes
- Will FAIL discovery quality gates
- Requires follow-up work to complete properly

**This option should only be used if**:
- Immediate stakeholder demo needed with incomplete work acknowledged
- Full implementation planned as immediate follow-up
- Quality gates temporarily bypassed (NOT RECOMMENDED)

**Better alternative**: Choose Option B for complete implementation in 2.5 hours.

---

## Option B: Comprehensive Update ✅ RECOMMENDED

### Strategy
Address ALL 6 affected artifacts maintaining complete traceability chains from source (persona, pain points) through implementation (modules). Standard best practice approach.

### Steps

[... 15 detailed steps with before/after for all 6 artifacts ...]

### Reflexion Evaluation

#### Completeness: ✓ COMPLETE (10/10)

**Reasoning**: All 6 artifacts from impact analysis addressed in proper dependency order. No missing artifacts.

**Artifact Coverage**: 6/6 (100%)

#### Consistency: ✓ INTACT (10/10)

**Reasoning**: All traceability chains maintained completely.

**Traceability Chains:**
- ✓ Intact: 2 (100%)
- ⚠ Partial: 0
- ❌ Broken: 0

All chains complete: PP-1.3 → JTBD-1.1 → REQ-008 → SCR-002 → MOD-INV-UI-01 ✓

#### Quality: ✓ HIGH QUALITY (9/10)

**Reasoning**: All quality criteria met with proper documentation and standards adherence.

**Quality Criteria:**
- Version Metadata: ✓
- Before/After Content: ✓
- Traceability Updates: ✓
- Format Consistency: ✓
- Documentation: ✓

#### Risk Assessment

**Identified Risks:**

1. **Design Token Verification Needed** (LOW)
   - Description: Low-light color scheme may need new design tokens
   - Mitigation: Consult design team during implementation

2. **Effort Estimation** (LOW)
   - Description: 2.5 hour estimate may extend with design consultation
   - Mitigation: Plan buffer time for design decisions

#### Effort Assessment

- **Level**: MEDIUM
- **Total Time**: 2 hours 30 minutes
- **Complexity**: Mix of simple (6 steps) and moderate (9 steps) changes

#### Final Score: 9.2/10

**Recommendation**: ✅ RECOMMENDED

**Reasoning**:
- Addresses all artifacts (✓ Completeness)
- Maintains all traceability chains (✓ Consistency)
- Follows all framework standards (✓ Quality)
- Reasonable effort for scope (2.5 hours)
- Low risk with clear mitigations
- Will PASS all quality gates

This is the recommended option for production-quality implementation.

---

## Recommendation Summary

**Highest Scoring Option**: Option B - Comprehensive Update (9.2/10)

**Rationale**: Option B provides complete implementation maintaining framework integrity with reasonable effort. While Option C scores slightly lower (8.5/10), its 4-hour effort and extended scope (regression tests, documentation) may be overkill for this medium-severity enhancement. Option A should be avoided as it breaks traceability and creates technical debt.

**Alternative**: If time is severely constrained, consider implementing Option B in two phases:
- Phase 1: Steps 1-10 (source through specs) - 1.5 hours
- Phase 2: Steps 11-15 (implementation artifacts) - 1 hour

But note: Phasing breaks atomicity and requires coordination between phases.

---

**Generated at**: 2026-01-25 14:45:00
**Generator**: Shared_FeedbackPlanGenerator_Reflexion
```
