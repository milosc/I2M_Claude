---
name: analyzing-prototype-feedback
description: Use when you need to analyze feedback impact across Discovery materials, Prototype specifications, and prototype code with full traceability chain analysis.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-prototype-feedback started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-prototype-feedback ended '{"stage": "discovery"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-prototype-feedback instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

---

# Analyze Prototype Feedback

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_FeedbackAnalyzer
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Claude Code
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description

Performs comprehensive impact analysis of feedback across the entire prototype ecosystem: Discovery materials (upstream), Prototype specifications, and actual prototype code. Uses traceability chains and state registries to identify all affected artifacts.

**Role**: You are a Feedback Impact Analyst. Your expertise is tracing dependencies across documentation, specifications, and code to identify the full blast radius of proposed changes.

> **INTEGRATES**: systematic-debugging skill for Bug-type feedback
> **INTEGRATES**: root-cause-tracing skill for tracing data flow issues

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
- output files created (feedback analysis reports)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "analyzing-prototype-feedback"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "analyzing-prototype-feedback" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## Trigger Conditions

- New feedback received for analysis
- Request to assess impact of proposed change
- Need to understand feedback scope before planning

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Feedback Content | Yes | Raw feedback text or file |
| Prototype Path | Yes | `Prototype_<SystemName>` folder |
| Discovery Path | Yes | `ClientAnalysis_<SystemName>` folder |
| Traceability Path | Yes | `traceability/` folder |
| State Path | Yes | `_state/` folder |

## Impact Categories

| Category | Code | Description | Affected Artifacts |
|----------|------|-------------|-------------------|
| Discovery | CAT-DISC | Upstream documentation | Personas, JTBD, Vision, Strategy |
| Screen Specs | CAT-SCR | Screen specifications | `02-screens/` folder |
| Component Specs | CAT-COMP | Component specifications | `01-components/` folder |
| Data Model | CAT-DATA | Data structures/API | `data-model.md`, `api-contracts.json` |
| Design Tokens | CAT-STYLE | Visual styling | `design-tokens.json`, `color-system.md` |
| Prototype Code | CAT-CODE | Actual code | `prototype/src/` folder |
| Test Data | CAT-TEST | Test datasets | `test-data/` folder |
| Interactions | CAT-INT | Motion, accessibility, responsive | `03-interactions/` folder |
| Registries | CAT-REG | State and traceability | `_state/`, `traceability/` |
| Matrices | CAT-MATRIX | Master traceability matrices | `helperFiles/` |

## MANDATORY END-TO-END ARTIFACT CHECKLIST

> **CRITICAL**: EVERY feedback analysis MUST check ALL artifact layers. Missing artifacts = incomplete implementation.

### Discovery Layer (ClientAnalysis_*)

| File | When Affected | Check For |
|------|---------------|-----------|
| `04-design-specs/screen-definitions.md` | New/modified screens | Screen entries, zone definitions |
| `04-design-specs/navigation-structure.md` | New screens, navigation changes | Nav flows, menu items |
| `04-design-specs/data-fields.md` | New data elements | Field definitions |
| `04-design-specs/interaction-patterns.md` | New interactions | Pattern definitions |
| `02-research/JOBS_TO_BE_DONE.md` | New features | Related JTBD statements |
| `02-research/personas/*.md` | Role-specific changes | Persona scenarios |
| `03-strategy/PRODUCT_ROADMAP.md` | Major features | Phase/epic references |

### Prototype Specification Layer (Prototype_*)

| Folder | Files to Check | When Affected |
|--------|----------------|---------------|
| `00-foundation/` | `design-tokens.json`, `color-system.md`, `typography.md`, `spacing-layout.md` | Visual changes |
| `01-components/` | `component-index.md`, specific component specs | New/modified components |
| `02-screens/` | `screen-index.md`, screen-specific folders | New/modified screens |
| `03-interactions/` | `motion-system.md`, `accessibility-spec.md`, `responsive-behavior.md` | Interaction changes |
| `04-implementation/` | `data-model.md`, `api-contracts.json`, `build-sequence.md`, `test-data/` | Data/API changes |

### Code Layer (Prototype_*/prototype/)

| Folder | Files to Check | When Affected |
|--------|----------------|---------------|
| `src/screens/` | Screen components | Screen changes |
| `src/components/` | Shared components | Component changes |
| `src/data/` | Mock data files | Data model changes |
| `src/contexts/` | State management | Auth, data context changes |
| `src/hooks/` | Custom hooks | Behavior changes |
| `src/styles/` | Global styles | Visual changes |

### State & Registry Layer (ROOT LEVEL)

| File | Purpose | When to Update |
|------|---------|----------------|
| `traceability/screen_registry.json` | Master screen tracking | New/modified screens |
| `_state/requirements_registry.json` | Requirements tracking | New requirements |
| `_state/discovery_summary.json` | Discovery extraction | Discovery changes |
| `_state/progress.json` | Build progress | Milestone changes |
| `traceability/prototype_traceability_register.json` | Prototype traceability | All prototype changes |
| `traceability/discovery_traceability_register.json` | Discovery traceability | Discovery changes |

### Traceability Matrix Layer (helperFiles/)

| File | Purpose | When to Update |
|------|---------|----------------|
| `helperFiles/TRACEABILITY_MATRIX_MASTER.md` | End-to-end trace chains | Any traceability change |
| `helperFiles/TRACEABILITY_ASSESSMENT_REPORT.md` | Coverage metrics | Any artifact added/removed |

## Procedure

### Phase 1: Parse Feedback Content

```
PARSE feedback for:
  - Explicit entity mentions (screen names, component names)
  - Implicit references (descriptions of behavior/appearance)
  - Keywords mapping to categories
  - Severity indicators

EXTRACT entities:
  screens_mentioned: []
  components_mentioned: []
  behaviors_mentioned: []
  visual_elements_mentioned: []
  data_elements_mentioned: []

CLASSIFY feedback_type:
  IF mentions "bug", "broken", "doesn't work", "error" → Bug
  IF mentions "improve", "better", "enhance" → Enhancement
  IF mentions "add", "new", "feature" → NewFeature
  IF mentions "confusing", "hard to use", "UX" → UXIssue
  IF mentions "looks", "color", "style", "visual" → VisualIssue

LOG: "Parsed feedback: {feedback_type}, {entity_count} entities found"
```

### Phase 2: Load Traceability Data

```
READ traceability files:
  discovery_trace = traceability/discovery_traceability_register.json
  prototype_trace = traceability/prototype_traceability_register.json

READ state files:
  screen_registry = traceability/screen_registry.json
  requirements_registry = _state/requirements_registry.json
  discovery_summary = _state/discovery_summary.json

READ prototype structure:
  component_index = Prototype_X/01-components/component-index.md
  screen_index = Prototype_X/02-screens/screen-index.md

IF feedback_type == "Bug":
  LOG: "Bug detected - will require systematic debugging"
  debugging_required = TRUE
```

### Phase 3: MANDATORY Comprehensive Artifact Scan

> **CRITICAL**: This phase MUST scan ALL artifact layers. Skipping = incomplete analysis.

```
LOG: "════════════════════════════════════════════"
LOG: " COMPREHENSIVE ARTIFACT SCAN"
LOG: "════════════════════════════════════════════"

# Initialize comprehensive impact structure
comprehensive_impact = {
  discovery: {
    screen_definitions: { affected: FALSE, changes: [] },
    navigation_structure: { affected: FALSE, changes: [] },
    data_fields: { affected: FALSE, changes: [] },
    interaction_patterns: { affected: FALSE, changes: [] },
    jobs_to_be_done: { affected: FALSE, changes: [] },
    personas: { affected: FALSE, changes: [] },
    roadmap: { affected: FALSE, changes: [] }
  },
  prototype_specs: {
    foundation: { affected: FALSE, changes: [] },
    components: { affected: FALSE, changes: [] },
    screens: { affected: FALSE, changes: [] },
    interactions: { affected: FALSE, changes: [] },
    implementation: { affected: FALSE, changes: [] }
  },
  code: {
    screens: { affected: FALSE, changes: [] },
    components: { affected: FALSE, changes: [] },
    data: { affected: FALSE, changes: [] },
    contexts: { affected: FALSE, changes: [] },
    hooks: { affected: FALSE, changes: [] },
    styles: { affected: FALSE, changes: [] }
  },
  registries: {
    screen_registry: { affected: FALSE, changes: [] },
    requirements_registry: { affected: FALSE, changes: [] },
    prototype_traceability: { affected: FALSE, changes: [] },
    discovery_traceability: { affected: FALSE, changes: [] }
  },
  matrices: {
    traceability_master: { affected: FALSE, changes: [] },
    assessment_report: { affected: FALSE, changes: [] }
  }
}

# SCAN DISCOVERY LAYER
LOG: "Scanning Discovery Layer..."

IF feedback implies new screen OR screen modification:
  CHECK ClientAnalysis/04-design-specs/screen-definitions.md
    IF screen NOT exists OR needs update:
      SET comprehensive_impact.discovery.screen_definitions.affected = TRUE
      ADD change: "Add/update screen definition for {screen_name}"

  CHECK ClientAnalysis/04-design-specs/navigation-structure.md
    IF navigation affected:
      SET comprehensive_impact.discovery.navigation_structure.affected = TRUE
      ADD change: "Update navigation flow for {screen_name}"

IF feedback implies new data fields:
  CHECK ClientAnalysis/04-design-specs/data-fields.md
    SET comprehensive_impact.discovery.data_fields.affected = TRUE
    ADD change: "Add data field definitions"

IF feedback type is NewFeature:
  CHECK ClientAnalysis/02-research/JOBS_TO_BE_DONE.md
    IF feature relates to existing JTBD:
      SET comprehensive_impact.discovery.jobs_to_be_done.affected = TRUE
      ADD change: "Link feature to JTBD-X.X"

# SCAN PROTOTYPE SPECS LAYER
LOG: "Scanning Prototype Specs Layer..."

IF feedback implies new/modified components:
  CHECK Prototype/01-components/component-index.md
    SET comprehensive_impact.prototype_specs.components.affected = TRUE
    ADD change: "Add/update component spec for {component_name}"

IF feedback implies new/modified screens:
  CHECK Prototype/02-screens/screen-index.md
  CHECK Prototype/02-screens/{screen_folder}/
    SET comprehensive_impact.prototype_specs.screens.affected = TRUE
    ADD change: "Add/update screen spec for {screen_name}"

IF feedback implies interactions/accessibility:
  CHECK Prototype/03-interactions/*.md
    SET comprehensive_impact.prototype_specs.interactions.affected = TRUE
    ADD change: "Update interaction patterns"

IF feedback implies data/API changes:
  CHECK Prototype/04-implementation/data-model.md
  CHECK Prototype/04-implementation/api-contracts.json
  CHECK Prototype/04-implementation/test-data/
    SET comprehensive_impact.prototype_specs.implementation.affected = TRUE
    ADD change: "Update data model/API/test data"

# SCAN CODE LAYER
LOG: "Scanning Code Layer..."

FOR each affected screen:
  CHECK prototype/src/screens/
    SET comprehensive_impact.code.screens.affected = TRUE
    ADD change: "Implement/modify {screen_name}.tsx"

FOR each affected component:
  CHECK prototype/src/components/
    SET comprehensive_impact.code.components.affected = TRUE
    ADD change: "Implement/modify {component_name}.tsx"

IF data model affected:
  CHECK prototype/src/data/
    SET comprehensive_impact.code.data.affected = TRUE
    ADD change: "Update mock data files"

# SCAN REGISTRIES LAYER
LOG: "Scanning Registries Layer..."

# ALWAYS check registries for any change
SET comprehensive_impact.registries.screen_registry.affected = TRUE
SET comprehensive_impact.registries.prototype_traceability.affected = TRUE

IF discovery changes:
  SET comprehensive_impact.registries.discovery_traceability.affected = TRUE

# SCAN MATRICES LAYER
LOG: "Scanning Traceability Matrices..."

# ALWAYS update matrices for any structural change
IF any new screen OR component OR requirement:
  SET comprehensive_impact.matrices.traceability_master.affected = TRUE
  SET comprehensive_impact.matrices.assessment_report.affected = TRUE

LOG: "Comprehensive scan complete"
```

### Phase 4: Direct Impact Analysis

```
FOR each entity in feedback:

  IF entity is SCREEN:
    SEARCH screen_registry for matching screen
    ADD to direct_impact.screens[]

    TRACE screen → components (from screen spec)
    ADD to direct_impact.components[]

    TRACE screen → requirements (from requirements_registry)
    ADD to direct_impact.requirements[]

    TRACE screen → code files (from prototype/src/pages/)
    ADD to direct_impact.code_files[]

  IF entity is COMPONENT:
    SEARCH component_index for matching component
    ADD to direct_impact.components[]

    TRACE component → screens using it (reverse lookup)
    ADD to direct_impact.screens[]

    TRACE component → code file (from prototype/src/components/)
    ADD to direct_impact.code_files[]

  IF entity is BEHAVIOR/INTERACTION:
    SEARCH interaction patterns in:
      - 03-interactions/motion-system.md
      - 03-interactions/accessibility-spec.md
    ADD to direct_impact.interaction_specs[]

  IF entity is DATA:
    SEARCH in:
      - 04-implementation/data-model.md
      - 04-implementation/api-contracts.json
    ADD to direct_impact.data_specs[]

    TRACE data → components using it
    TRACE data → screens displaying it

  IF entity is VISUAL:
    SEARCH in:
      - 00-foundation/design-tokens.json
      - 00-foundation/color-system.md
    ADD to direct_impact.design_specs[]
```

### Phase 4: Cascading Impact Analysis

```
FOR each item in direct_impact:

  TRACE UPSTREAM (toward Discovery):
    screen → requirement → JTBD → persona → pain_point

    FOR each upstream item found:
      IF change affects upstream semantics:
        ADD to cascading_impact.discovery[]
        SET upstream_impact = TRUE

  TRACE DOWNSTREAM (toward Code):
    spec → component_code → page_code → styles

    FOR each downstream item found:
      ADD to cascading_impact.code[]

  TRACE LATERAL (siblings):
    component → other_components_using_same_props
    screen → other_screens_in_same_flow

    FOR each lateral item found:
      ADD to cascading_impact.related[]

BUILD dependency_tree:
  {
    "direct": { screens: [], components: [], code: [] },
    "upstream": { discovery: [], requirements: [] },
    "downstream": { code: [], tests: [] },
    "lateral": { related_screens: [], related_components: [] }
  }
```

### Phase 5: Bug-Specific Analysis (For Bug Types)

> **MANDATORY**: Uses systematic-debugging skill

```
IF feedback_type == "Bug":

  LOG: "════════════════════════════════════════════"
  LOG: " SYSTEMATIC DEBUGGING REQUIRED"
  LOG: "════════════════════════════════════════════"

  APPLY systematic-debugging Phase 1 (Root Cause Investigation):

  1. READ ERROR MESSAGES
     - Extract any error text from feedback
     - Note exact symptoms described
     - Check browser console (if available)

  2. REPRODUCE CONSISTENTLY
     CREATE reproduction_steps = {
       starting_state: "...",
       steps: [...],
       expected: "...",
       actual: "...",
       reproducible: TRUE|FALSE|UNKNOWN
     }

  3. CHECK RECENT CHANGES
     - Query git history for affected files
     - Note any recent modifications
     - Check dependency updates

  4. TRACE DATA FLOW (uses root-cause-tracing)
     symptom = feedback.description

     TRACE backwards through:
       Component render → Props received → Parent component →
       State/Context → API response → Data source

     RECORD data_flow_trace = [
       { level: 1, location: "...", value: "...", issue: "..." },
       { level: 2, location: "...", value: "...", issue: "..." },
       ...
     ]

  5. FORM INITIAL HYPOTHESIS
     hypothesis = {
       statement: "I think X is the root cause because Y",
       evidence: [...],
       confidence: HIGH|MEDIUM|LOW
     }

  RECORD debugging_investigation = {
    error_messages: [...],
    reproduction: reproduction_steps,
    recent_changes: [...],
    data_flow_trace: data_flow_trace,
    initial_hypothesis: hypothesis
  }

  ADD debugging_investigation to impact_analysis
```

### Phase 6: Calculate Impact Metrics

```
CALCULATE counts:
  discovery_count = cascading_impact.discovery.length
  spec_count = direct_impact.screens.length +
               direct_impact.components.length +
               direct_impact.interaction_specs.length +
               direct_impact.data_specs.length +
               direct_impact.design_specs.length
  code_count = direct_impact.code_files.length +
               cascading_impact.code.length
  total_count = discovery_count + spec_count + code_count

CALCULATE priority_score (30-point scale):
  severity_points:
    Critical: 10, High: 7, Medium: 4, Low: 2

  scope_points:
    total_count > 10: 10
    total_count > 5: 7
    total_count > 2: 4
    total_count <= 2: 2

  type_points:
    Bug: 10, UXIssue: 7, Enhancement: 5, NewFeature: 3, VisualIssue: 2

  priority_score = severity_points + scope_points + type_points

DETERMINE impact_levels:
  FOR each affected file:
    IF file is in critical path (P0 requirement): HIGH
    ELSE IF file is in main flow: MEDIUM
    ELSE: LOW
```

### Phase 7: Generate Impact Matrix

```
CREATE impact_matrix:
  {
    "high_impact": [
      { file: "...", reason: "...", type: "screen|component|code" }
    ],
    "medium_impact": [...],
    "low_impact": [...]
  }

CREATE traceability_chain:
  FOR each affected item:
    RECORD chain from discovery → spec → code

  Example:
    PP-1.2 (Pain Point) →
    JTBD-1.1 (Job) →
    REQ-001 (Requirement) →
    SCR-001 (Screen Spec) →
    InventoryList.tsx (Code)
```

## Output Format

### Primary Output: `impact_analysis.md`

```markdown
---
document_id: PF-IA-{ID}
version: 1.0.0
created_at: {date}
updated_at: {date}
generated_by: Prototype_FeedbackAnalyzer
source_files:
  - FEEDBACK_ORIGINAL.md
change_history:
  - version: "1.0.0"
    date: "{date}"
    author: "Prototype_FeedbackAnalyzer"
    changes: "Initial impact analysis"
---

# Impact Analysis

## Feedback Summary
- **Type**: {feedback_type}
- **Severity**: {severity}
- **Priority Score**: {score}/30
- **Debugging Required**: {yes/no}

---

## COMPREHENSIVE IMPACT SUMMARY

> **ALL LAYERS SCANNED**: Discovery, Specs, Code, Registries, Matrices

### Discovery Layer Impact (ClientAnalysis_*)

| File | Status | Required Changes |
|------|--------|------------------|
| `04-design-specs/screen-definitions.md` | NEEDS UPDATE / NO CHANGE | {changes} |
| `04-design-specs/navigation-structure.md` | NEEDS UPDATE / NO CHANGE | {changes} |
| `04-design-specs/data-fields.md` | NEEDS UPDATE / NO CHANGE | {changes} |
| `04-design-specs/interaction-patterns.md` | NEEDS UPDATE / NO CHANGE | {changes} |
| `02-research/JOBS_TO_BE_DONE.md` | NEEDS UPDATE / NO CHANGE | {changes} |
| `02-research/personas/*.md` | NEEDS UPDATE / NO CHANGE | {changes} |

### Prototype Specs Layer Impact (Prototype_*)

| Folder | Status | Required Changes |
|--------|--------|------------------|
| `00-foundation/` | NEEDS UPDATE / NO CHANGE | {changes} |
| `01-components/` | NEEDS UPDATE / NO CHANGE | {changes} |
| `02-screens/` | NEEDS UPDATE / NO CHANGE | {changes} |
| `03-interactions/` | NEEDS UPDATE / NO CHANGE | {changes} |
| `04-implementation/` | NEEDS UPDATE / NO CHANGE | {changes} |

### Code Layer Impact (prototype/src/)

| Folder | Status | Required Changes |
|--------|--------|------------------|
| `screens/` | NEEDS UPDATE / NO CHANGE | {changes} |
| `components/` | NEEDS UPDATE / NO CHANGE | {changes} |
| `data/` | NEEDS UPDATE / NO CHANGE | {changes} |
| `contexts/` | NEEDS UPDATE / NO CHANGE | {changes} |

### Registry Layer Impact (ROOT LEVEL)

| File | Status | Required Changes |
|------|--------|------------------|
| `traceability/screen_registry.json` | NEEDS UPDATE / NO CHANGE | {changes} |
| `_state/requirements_registry.json` | NEEDS UPDATE / NO CHANGE | {changes} |
| `traceability/prototype_traceability_register.json` | NEEDS UPDATE / NO CHANGE | {changes} |
| `traceability/discovery_traceability_register.json` | NEEDS UPDATE / NO CHANGE | {changes} |

### Traceability Matrix Impact (helperFiles/)

| File | Status | Required Changes |
|------|--------|------------------|
| `TRACEABILITY_MATRIX_MASTER.md` | NEEDS UPDATE / NO CHANGE | {changes} |
| `TRACEABILITY_ASSESSMENT_REPORT.md` | NEEDS UPDATE / NO CHANGE | {changes} |

---

## Impact Overview

| Level | Count | Categories |
|-------|-------|------------|
| Discovery | {N} | CAT-DISC |
| Specifications | {N} | CAT-SCR, CAT-COMP, CAT-DATA, CAT-INT |
| Code | {N} | CAT-CODE |
| Registries | {N} | CAT-REG |
| Matrices | {N} | CAT-MATRIX |
| **Total** | **{N}** | |

---

## Direct Impact

### Screens Affected
| Screen ID | Name | Impact Level | Reason |
|-----------|------|--------------|--------|
| SCR-001 | Inventory List | HIGH | Primary target of feedback |

### Components Affected
| Component | Impact Level | Used By |
|-----------|--------------|---------|
| DataTable | HIGH | 3 screens |
| FilterPanel | MEDIUM | 2 screens |

### Code Files Affected
| File | Type | Impact Level |
|------|------|--------------|
| src/pages/InventoryList.tsx | Page | HIGH |
| src/components/DataTable.tsx | Component | HIGH |

---

## Cascading Impact

### Upstream (Discovery)
| Item | Type | Impact |
|------|------|--------|
| PP-1.2 | Pain Point | May need update if behavior changes |
| JTBD-1.1 | Job | Related to affected screen |

### Downstream (Code Dependencies)
| File | Depends On | Impact |
|------|------------|--------|
| InventoryList.tsx | DataTable | Will need update |

### Lateral (Related Items)
| Item | Relationship | Impact |
|------|--------------|--------|
| SCR-002 | Same flow | Should test |

---

## Traceability Chain

```
PP-1.2 (Slow inventory lookup)
  └─► JTBD-1.1 (Quickly find items)
      └─► REQ-001 (Search functionality)
          └─► SCR-001 (Inventory List)
              └─► DataTable component
                  └─► src/components/DataTable.tsx
```

---

## Risk Assessment

| Factor | Score | Notes |
|--------|-------|-------|
| P0 Requirements Affected | {N} | {list} |
| Critical Screens Affected | {N} | {list} |
| Data Integrity Risk | LOW/MED/HIGH | {reason} |
| User Flow Disruption | LOW/MED/HIGH | {reason} |
| **Overall Risk** | **{LEVEL}** | |

---

## Debugging Investigation (Bug Type Only)

### Reproduction Steps
1. Navigate to {screen}
2. Perform {action}
3. Expected: {expected}
4. Actual: {actual}

### Data Flow Trace
```
Level 1: DataTable.render() → rows = undefined
Level 2: Props received → data prop missing
Level 3: Parent InventoryList → API response not mapped
Level 4: API call → Returns { items: [...] } not { data: [...] }
```

### Initial Hypothesis
**Statement**: "{hypothesis}"
**Confidence**: {HIGH/MEDIUM/LOW}
**Evidence**: {evidence_list}

---

## Regression Scope

### Must Test
- [ ] {critical_test_1}
- [ ] {critical_test_2}

### Should Test
- [ ] {related_test_1}

### Optional Test
- [ ] {tangential_test_1}

---

## Categories Assigned
{list of CAT-* categories}

---

**Analysis Complete**: {timestamp}
```

## Integration Points

### Receives From
- `/prototype-feedback` command - Raw feedback input
- User - Feedback text or file

### Feeds Into
- `Prototype_FeedbackRegister` - Analysis results for registration
- `Prototype_FeedbackPlanner` - Impact data for planning
- `Prototype_FeedbackImplementer` - Debugging evidence (for bugs)

### Uses Skills
- `systematic-debugging` - For Bug-type root cause investigation
- `root-cause-tracing` - For tracing data flow issues

## Error Handling

| Issue | Action |
|-------|--------|
| Traceability file missing | Warn, continue with available data |
| Screen not found in registry | Add to "untracked" list, flag for attention |
| Code file not found | Note as "missing implementation" |
| Cannot reproduce bug | Mark reproduction as "unable", continue |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: Prototype Skills Framework v2.3
