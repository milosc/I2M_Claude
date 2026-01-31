---
name: planning-prototype-feedback
description: Use when you need to generate implementation options and plans for approved prototype feedback with risk assessment and effort estimation.
model: sonnet
allowed-tools: Bash, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill planning-prototype-feedback started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill planning-prototype-feedback ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill planning-prototype-feedback instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

# Plan Prototype Feedback Implementation

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_FeedbackPlanner
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Claude Code
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description

Generates implementation options (minimum 2) for approved feedback, including step-by-step plans, risk assessments, and effort estimates. For Bug-type feedback, enforces that root cause must be identified before generating fix options.

**Role**: You are an Implementation Strategist. Your expertise is designing multiple viable approaches to address feedback, weighing trade-offs, and creating actionable step-by-step plans.

> **INTEGRATES**: executing-plans skill for plan execution patterns
> **ENFORCES**: Iron Law of Debugging for Bug types

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
- output files created (implementation plans)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "planning-prototype-feedback"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "planning-prototype-feedback" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## Trigger Conditions

- Feedback has been approved (status = "approved")
- User requests implementation options
- Ready to plan after impact analysis complete

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Feedback ID | Yes | PF-NNN identifier |
| Impact Analysis | Yes | Results from Prototype_FeedbackAnalyzer |
| Debugging Evidence | Conditional | Required for Bug type |
| Session Folder | Yes | Path to feedback session |

## The Iron Law (Bug Types)

```
NO FIX OPTIONS WITHOUT ROOT CAUSE IDENTIFICATION
```

For Bug-type feedback, this skill WILL NOT generate implementation options until:
1. Debugging evidence exists in the feedback registry
2. Root cause hypothesis has been confirmed
3. Confidence level is at least MEDIUM

## Procedure

### Phase 1: Pre-Planning Validation

```
READ feedback entry from registry

VALIDATE:
  1. Status == "approved"
  2. Impact analysis exists

IF feedback.type == "Bug":
  CHECK debugging_evidence exists:
    IF NOT exists:
      ════════════════════════════════════════════
       CANNOT GENERATE OPTIONS
      ════════════════════════════════════════════

      Bug-type feedback requires root cause investigation.

      Debugging evidence not found for PF-{id}.

      Action: Return to Prototype_FeedbackAnalyzer
              and complete systematic debugging.
      ════════════════════════════════════════════

      BLOCK - DO NOT PROCEED

    IF debugging_evidence.confidence == "LOW":
      WARN: "Low confidence root cause - consider more investigation"
      PROMPT for confirmation to proceed

LOG: "Pre-planning validation passed"
```

### Phase 2: Determine Option Strategy

```
BASED on feedback.type:

  Bug:
    option_strategy = "fix_variants"
    options = [
      "Quick Fix" - Address symptom
      "Proper Fix" - Address root cause (RECOMMENDED)
      "Preventive Fix" - Root cause + defense-in-depth
    ]

  Enhancement:
    option_strategy = "enhancement_levels"
    options = [
      "Minimal" - Targeted improvement
      "Standard" - Full enhancement (RECOMMENDED)
      "Comprehensive" - Enhancement + related improvements
    ]

  NewFeature:
    option_strategy = "feature_scope"
    options = [
      "MVP" - Minimum viable
      "Full" - Complete feature (RECOMMENDED)
      "Extended" - Feature + enhancements
    ]

  UXIssue:
    option_strategy = "ux_approaches"
    options = [
      "Quick Win" - Fast UX fix
      "Proper UX" - Proper UX solution (RECOMMENDED)
      "UX Overhaul" - Comprehensive UX improvement
    ]

  VisualIssue:
    option_strategy = "visual_scope"
    options = [
      "Spot Fix" - Fix specific visual
      "Consistent" - Fix + align related (RECOMMENDED)
      "Systematic" - Update design system
    ]
```

## MANDATORY ARTIFACT COVERAGE

> **CRITICAL**: ALL implementation options MUST address ALL affected artifact layers identified in impact analysis.

### Required Artifact Categories

Each option MUST explicitly address:

1. **Discovery Layer** (ClientAnalysis_*):
   - `04-design-specs/screen-definitions.md` - If new/modified screens
   - `04-design-specs/navigation-structure.md` - If navigation affected
   - `04-design-specs/data-fields.md` - If new data fields
   - `02-research/JOBS_TO_BE_DONE.md` - If new features

2. **Prototype Specs Layer** (Prototype_*):
   - `01-components/component-index.md` + specs - If new/modified components
   - `02-screens/screen-index.md` + specs - If new/modified screens
   - `03-interactions/*.md` - If interaction patterns affected
   - `04-implementation/data-model.md` - If data model affected
   - `04-implementation/api-contracts.json` - If API affected
   - `04-implementation/test-data/` - If test data needed

3. **Code Layer** (prototype/src/):
   - `screens/` - Screen components
   - `components/` - Shared components
   - `data/` - Mock data files
   - `App.tsx` - If routing affected

4. **Registry Layer** (ROOT LEVEL):
   - `traceability/screen_registry.json` - ALWAYS for screen changes
   - `_state/requirements_registry.json` - If requirements affected
   - `traceability/prototype_traceability_register.json` - ALWAYS
   - `traceability/discovery_traceability_register.json` - If discovery affected

5. **Matrix Layer** (helperFiles/):
   - `TRACEABILITY_MATRIX_MASTER.md` - If new trace chains
   - `TRACEABILITY_ASSESSMENT_REPORT.md` - If coverage metrics change

### Phase 3: Generate Option A (Minimal/Quick)

```
CREATE option_a = {
  id: "A",
  name: option_names[0],
  approach: "Minimal changes to address immediate issue",

  # COMPREHENSIVE CHANGES STRUCTURE
  changes: {
    discovery: [
      # Even Option A must note discovery impact
      IF screen_definitions affected:
        { file: "ClientAnalysis/04-design-specs/screen-definitions.md", action: "note", changes: ["Deferred to Option B/C"] }
    ],

    specifications: [
      FOR each directly affected spec:
        { file: "...", action: "modify", changes: ["..."] }
    ],

    code: [
      FOR each directly affected code file:
        { file: "...", action: "modify", changes: ["..."] }
    ],

    registries: [
      # ALWAYS include registry updates
      { file: "traceability/screen_registry.json", action: "update", changes: ["Update code_status"] },
      { file: "traceability/prototype_traceability_register.json", action: "update", changes: ["Add feedback ref"] }
    ],

    matrices: [
      # Note deferred for Option A
      { file: "helperFiles/TRACEABILITY_MATRIX_MASTER.md", action: "deferred", changes: ["Full update in Option B/C"] }
    ]
  },

  steps: [
    FOR each change in dependency order:
      {
        step: N,
        action: "description",
        target: "file path",
        type: "discovery|spec|code",
        details: "what to change",
        estimated_time: "Xm"
      }
  ],

  pros: [
    "Fast to implement",
    "Low risk",
    "Minimal testing required"
  ],

  cons: [
    "May not fully address underlying issue",
    "Could need revisiting",
    "Limited improvement"
  ],

  risk_assessment: {
    implementation_risk: "LOW",
    regression_risk: "LOW",
    user_impact: "POSITIVE_SMALL"
  },

  effort: {
    specification_changes: "Xh",
    code_changes: "Xh",
    testing: "Xh",
    total: "Xh"
  }
}
```

### Phase 4: Generate Option B (Standard/Proper) - RECOMMENDED

> **COMPREHENSIVE**: Option B MUST include ALL affected artifacts across ALL layers.

```
CREATE option_b = {
  id: "B",
  name: option_names[1],
  approach: "Proper solution addressing core issue with FULL traceability",
  recommended: TRUE,

  # COMPREHENSIVE CHANGES - ALL LAYERS REQUIRED
  changes: {
    # LAYER 1: DISCOVERY (ClientAnalysis_*)
    discovery: [
      IF new/modified screen:
        { file: "ClientAnalysis/04-design-specs/screen-definitions.md", action: "update", changes: ["Add screen entry with zones, components, data requirements"] },
        { file: "ClientAnalysis/04-design-specs/navigation-structure.md", action: "update", changes: ["Add navigation entry, update flow diagrams"] },
      IF new data fields:
        { file: "ClientAnalysis/04-design-specs/data-fields.md", action: "update", changes: ["Add field definitions"] },
      IF new feature:
        { file: "ClientAnalysis/02-research/JOBS_TO_BE_DONE.md", action: "update", changes: ["Link to JTBD or add acceptance criteria"] },
      IF affects interaction patterns:
        { file: "ClientAnalysis/04-design-specs/interaction-patterns.md", action: "update", changes: ["Document new patterns"] }
    ],

    # LAYER 2: PROTOTYPE SPECIFICATIONS (Prototype_*)
    specifications: [
      # Components
      IF new component required:
        { file: "01-components/component-index.md", action: "update", changes: ["Add component entry"] },
        { file: "01-components/{category}/{component}/spec.md", action: "create", changes: ["Full component spec"] },

      # Screens
      IF new/modified screen:
        { file: "02-screens/screen-index.md", action: "update", changes: ["Add screen entry"] },
        { file: "02-screens/{platform}/{screen}/spec.md", action: "create|update", changes: ["Full screen spec"] },

      # Interactions
      IF interaction patterns affected:
        { file: "03-interactions/motion-system.md", action: "update", changes: ["Add motion specs"] },
        { file: "03-interactions/accessibility-spec.md", action: "update", changes: ["Add a11y requirements"] },
        { file: "03-interactions/responsive-behavior.md", action: "update", changes: ["Add responsive specs"] },

      # Implementation
      IF data model affected:
        { file: "04-implementation/data-model.md", action: "update", changes: ["Add entity/schema"] },
      IF API affected:
        { file: "04-implementation/api-contracts.json", action: "update", changes: ["Add endpoint spec"] },
      IF test data needed:
        { file: "04-implementation/test-data/{entity}.json", action: "create|update", changes: ["Add test data"] }
    ],

    # LAYER 3: CODE (prototype/src/)
    code: [
      IF new screen:
        { file: "prototype/src/screens/{platform}/{Screen}.tsx", action: "create", changes: ["Implement screen component"] },
        { file: "prototype/src/App.tsx", action: "update", changes: ["Add route"] },
      IF new component:
        { file: "prototype/src/components/{Component}.tsx", action: "create", changes: ["Implement component"] },
      IF mock data needed:
        { file: "prototype/src/data/{entity}.json", action: "create|update", changes: ["Add mock data"] },
      IF context needed:
        { file: "prototype/src/contexts/{Context}.tsx", action: "create|update", changes: ["Add/update context"] }
    ],

    # LAYER 4: REGISTRIES (ROOT LEVEL) - ALWAYS REQUIRED
    registries: [
      { file: "traceability/screen_registry.json", action: "update", changes: [
        "Add screen entry to discovery_screens[]",
        "Add traceability entry",
        "Update screen_coverage statistics"
      ]},
      { file: "traceability/prototype_traceability_register.json", action: "update", changes: [
        "Add screen to screen_traceability.screens[]",
        "Update coverage counts",
        "Add feedback_source reference"
      ]},
      IF discovery changed:
        { file: "traceability/discovery_traceability_register.json", action: "update", changes: ["Update discovery references"] },
      IF requirements added:
        { file: "_state/requirements_registry.json", action: "update", changes: ["Add requirement entry"] }
    ],

    # LAYER 5: TRACEABILITY MATRICES (helperFiles/)
    matrices: [
      { file: "helperFiles/TRACEABILITY_MATRIX_MASTER.md", action: "update", changes: [
        "Add new trace chains",
        "Update coverage metrics"
      ]},
      { file: "helperFiles/TRACEABILITY_ASSESSMENT_REPORT.md", action: "update", changes: [
        "Update coverage percentages",
        "Add new items to inventory"
      ]}
    ]
  },

  # COMPREHENSIVE EXECUTION ORDER
  steps: [
    # Phase 1: Discovery (Upstream)
    1. "Update ClientAnalysis/04-design-specs/screen-definitions.md",
    2. "Update ClientAnalysis/04-design-specs/navigation-structure.md",
    3. "Update ClientAnalysis/04-design-specs/data-fields.md (if needed)",
    4. "Update ClientAnalysis/02-research/JOBS_TO_BE_DONE.md (if needed)",

    # Phase 2: Prototype Specs
    5. "Update 04-implementation/data-model.md",
    6. "Update 04-implementation/api-contracts.json",
    7. "Create/update 04-implementation/test-data/",
    8. "Update 01-components/component-index.md",
    9. "Create component specs in 01-components/",
    10. "Update 02-screens/screen-index.md",
    11. "Create screen specs in 02-screens/",
    12. "Update 03-interactions/*.md",

    # Phase 3: Code
    13. "Implement components in prototype/src/components/",
    14. "Implement screens in prototype/src/screens/",
    15. "Update prototype/src/App.tsx (routing)",
    16. "Add mock data to prototype/src/data/",

    # Phase 4: Registries & Traceability
    17. "Update traceability/screen_registry.json",
    18. "Update traceability/prototype_traceability_register.json",
    19. "Update traceability/discovery_traceability_register.json (if needed)",

    # Phase 5: Matrices
    20. "Update helperFiles/TRACEABILITY_MATRIX_MASTER.md",
    21. "Update helperFiles/TRACEABILITY_ASSESSMENT_REPORT.md"
  ],

  IF feedback.type == "Bug":
    # Include root cause fix
    root_cause_fix = {
      description: "Fix {debugging_evidence.root_cause}",
      location: "{from data_flow_trace}",
      code_change: "specific change to fix root cause"
    }
    INSERT root_cause_fix as appropriate step

  pros: [
    "Addresses core issue properly",
    "Maintainable solution",
    "Follows best practices"
  ],

  cons: [
    "More effort than minimal",
    "Requires thorough testing"
  ],

  risk_assessment: {
    implementation_risk: "MEDIUM",
    regression_risk: "MEDIUM",
    user_impact: "POSITIVE_SIGNIFICANT"
  },

  effort: {
    specification_changes: "Xh",
    code_changes: "Xh",
    testing: "Xh",
    total: "Xh"
  }
}
```

### Phase 5: Generate Option C (Comprehensive/Preventive)

```
CREATE option_c = {
  id: "C",
  name: option_names[2],
  approach: "Comprehensive solution with future-proofing",

  changes: {
    discovery: [
      ALL upstream items that could benefit from update
    ],

    specifications: [
      All direct + cascading + lateral items
    ],

    code: [
      All affected code + related improvements
    ]
  },

  steps: [
    # Full implementation sequence
    ...all steps from Option B...
    PLUS:
    - Related improvements
    - Additional validation
    - Enhanced error handling
  ],

  IF feedback.type == "Bug":
    # Add defense-in-depth layers
    defense_layers = [
      { layer: 1, description: "Validation at entry point" },
      { layer: 2, description: "Type checking at boundary" },
      { layer: 3, description: "Fallback handling" },
      { layer: 4, description: "Logging for future debugging" }
    ]
    INSERT defense_layers as additional steps

    # Add regression test
    regression_test = {
      description: "Automated test covering this bug scenario",
      location: "prototype/src/__tests__/",
      covers: [feedback.description]
    }
    INSERT regression_test as final step

  pros: [
    "Most thorough solution",
    "Prevents similar issues",
    "Improves overall quality"
  ],

  cons: [
    "Highest effort",
    "Scope creep risk",
    "Longer testing cycle"
  ],

  risk_assessment: {
    implementation_risk: "MEDIUM-HIGH",
    regression_risk: "HIGH",
    user_impact: "POSITIVE_MAJOR"
  },

  effort: {
    specification_changes: "Xh",
    code_changes: "Xh",
    testing: "Xh",
    total: "Xh"
  }
}
```

### Phase 6: Generate Comparison Matrix

```
CREATE comparison = {
  summary: {
    option_a: { effort: "Xh", risk: "LOW", coverage: "X%" },
    option_b: { effort: "Xh", risk: "MED", coverage: "X%" },
    option_c: { effort: "Xh", risk: "HIGH", coverage: "X%" }
  },

  trade_offs: [
    { factor: "Time to implement", a: "fastest", b: "moderate", c: "longest" },
    { factor: "Risk", a: "lowest", b: "moderate", c: "highest" },
    { factor: "Completeness", a: "partial", b: "complete", c: "comprehensive" },
    { factor: "Future maintenance", a: "may need more", b: "standard", c: "reduced" }
  ],

  recommendation: "B",
  recommendation_reason: "Best balance of effort, risk, and completeness"
}
```

## Output Format

### Primary Output: `implementation_options.md`

```markdown
---
document_id: PF-OPT-{ID}
version: 1.0.0
created_at: {date}
updated_at: {date}
generated_by: Prototype_FeedbackPlanner
source_files:
  - impact_analysis.md
change_history:
  - version: "1.0.0"
    date: "{date}"
    author: "Prototype_FeedbackPlanner"
    changes: "Initial options generation"
---

# Implementation Options

## Feedback Reference
- **ID**: PF-{ID}
- **Type**: {type}
- **Title**: {title}

---

## Option A: "{name}"

### Approach
{approach_description}

### Changes Required

**Specifications** ({count} files):
| File | Action | Changes |
|------|--------|---------|
| 01-components/Button.spec.md | Modify | Update hover state |

**Code** ({count} files):
| File | Action | Changes |
|------|--------|---------|
| src/components/Button.tsx | Modify | Fix hover handler |

### Implementation Steps
| Step | Action | Target | Time |
|------|--------|--------|------|
| 1 | Update Button spec | 01-components/Button.spec.md | 15m |
| 2 | Modify Button code | src/components/Button.tsx | 30m |

### Assessment
| Factor | Rating |
|--------|--------|
| Implementation Risk | LOW |
| Regression Risk | LOW |
| Effort | {X}h |

### Pros & Cons
| Pros | Cons |
|------|------|
| Fast implementation | Partial solution |
| Low risk | May need revisiting |

---

## Option B: "{name}" (RECOMMENDED)

### Approach
{approach_description}

### Root Cause Fix (Bug Type)
**Root Cause**: {debugging_evidence.root_cause}
**Fix Location**: {location}
**Change**: {specific_change}

### Changes Required

**Discovery** ({count} files):
| File | Action | Changes |
|------|--------|---------|
| JOBS_TO_BE_DONE.md | Update | Clarify acceptance criteria |

**Specifications** ({count} files):
| File | Action | Changes |
|------|--------|---------|

**Code** ({count} files):
| File | Action | Changes |
|------|--------|---------|

### Implementation Steps
| Step | Action | Target | Time |
|------|--------|--------|------|
| 1 | ... | ... | ... |

### Assessment
| Factor | Rating |
|--------|--------|
| Implementation Risk | MEDIUM |
| Regression Risk | MEDIUM |
| Effort | {X}h |

### Pros & Cons
| Pros | Cons |
|------|------|
| Complete solution | More effort |
| Addresses root cause | Requires testing |

---

## Option C: "{name}"

[Similar structure to B with additional scope]

### Defense-in-Depth Layers (Bug Type)
| Layer | Description |
|-------|-------------|
| 1 | Input validation at entry |
| 2 | Type checking at boundary |
| 3 | Fallback handling |
| 4 | Debug logging |

### Regression Test
- **File**: `src/__tests__/bugfix-PF-{ID}.test.ts`
- **Covers**: {original_bug_description}

---

## Comparison Matrix

| Factor | Option A | Option B | Option C |
|--------|----------|----------|----------|
| Effort | {X}h | {X}h | {X}h |
| Risk | LOW | MEDIUM | HIGH |
| Coverage | Partial | Complete | Comprehensive |
| Maintenance | Higher | Standard | Lower |

---

## Recommendation

**Selected**: Option B

**Reasoning**: {recommendation_reason}

---

## Selection

Please select an option:
- `A` - {option_a_name}
- `B` - {option_b_name} (Recommended)
- `C` - {option_c_name}
- `custom` - Provide custom plan

---

**Generated**: {timestamp}
```

### Secondary Output: `implementation_plan.md`

After user selects option:

```markdown
---
document_id: PF-PLAN-{ID}
version: 1.0.0
created_at: {date}
updated_at: {date}
generated_by: Prototype_FeedbackPlanner
source_files:
  - implementation_options.md
change_history:
  - version: "1.0.0"
    date: "{date}"
    author: "Prototype_FeedbackPlanner"
    changes: "Plan created from Option {X}"
---

# Implementation Plan

## Feedback Reference
- **ID**: PF-{ID}
- **Selected Option**: {option_name}
- **Total Effort**: {X}h

---

## Pre-Implementation Checklist
- [ ] Backup created
- [ ] All dependencies available
- [ ] No conflicting changes in progress

---

## Execution Steps

### Step 1: {action}
- **Target**: {file_path}
- **Type**: {discovery|spec|code}
- **Action**: {create|modify|delete}
- **Details**: {what_to_change}
- **Estimated Time**: {Xm}
- **Requirements Affected**: {list}

### Step 2: {action}
...

---

## Rollback Plan
- **Backup ID**: {to_be_created}
- **Rollback Command**: `rollback to {backup_id}`

---

## Post-Implementation
- [ ] Run regression tests
- [ ] Update traceability
- [ ] Generate change report

---

**Plan Confirmed**: {timestamp}
**Ready for Implementation**: YES
```

## Custom Plan Handling

```
IF user selects "custom":

  PROMPT:
    ════════════════════════════════════════════
     CUSTOM PLAN INPUT
    ════════════════════════════════════════════

    Please describe your custom implementation approach:

    1. What files will you change?
    2. What is the order of changes?
    3. How does this address the feedback?

    ════════════════════════════════════════════

  RECEIVE custom_plan_description

  VALIDATE custom plan:
    checklist = [
      "Addresses root cause (if Bug)",
      "Covers all affected items",
      "Has clear sequence",
      "Includes testing step"
    ]

    FOR each check:
      IF NOT satisfied:
        ASK clarifying question (max 5 rounds)

  CONVERT to structured plan format
  SAVE as implementation_plan.md
```

## Integration Points

### Receives From
- `Prototype_FeedbackAnalyzer` - Impact analysis, debugging evidence
- `Prototype_FeedbackRegister` - Feedback entry details

### Feeds Into
- `Prototype_FeedbackImplementer` - Implementation plan for execution
- User - Options for selection

### Uses Skills
- `executing-plans` - Plan execution patterns

## Error Handling

| Issue | Action |
|-------|--------|
| Missing debugging evidence (Bug) | Block, redirect to analyzer |
| Incomplete impact analysis | Warn, generate partial options |
| User provides incomplete custom plan | Ask clarifying questions |
| Cannot generate 3 options | Generate 2, note limitation |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: Prototype Skills Framework v2.3
