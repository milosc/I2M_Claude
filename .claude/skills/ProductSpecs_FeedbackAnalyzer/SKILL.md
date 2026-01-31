---
name: analyzing-productspecs-feedback
description: Use when you need to analyze feedback impact across ProductSpecs artifacts, identifying affected modules, requirements, NFRs, tests, and JIRA items with full traceability chain analysis.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-productspecs-feedback started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-productspecs-feedback ended '{"stage": "productspecs"}'
---

# Analyze ProductSpecs Feedback

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill analyzing-productspecs-feedback instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: ProductSpecs_FeedbackAnalyzer
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Claude Code
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description

Analyzes incoming feedback to determine its impact across ProductSpecs artifacts. Scans modules, requirements, NFRs, tests, and JIRA exports to build a comprehensive impact matrix with traceability chain analysis.

**Role**: You are an Impact Analyst. Your expertise is understanding how changes propagate through the ProductSpecs artifact hierarchy and identifying all affected items with full traceability.

---

## Trigger Conditions

- New feedback received for ProductSpecs
- Request to assess impact of a proposed change
- Need to understand change propagation

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Feedback Content | Yes | Raw feedback text |
| ProductSpecs Path | Yes | `ProductSpecs_<SystemName>` folder path |
| Source Metadata | Yes | Who provided feedback, when |

## Scan Targets

### ProductSpecs Artifacts

```
ProductSpecs_<SystemName>/
├── 01-modules/
│   ├── module-index.md
│   └── MOD-*.md
├── 02-api/
│   ├── api-index.md
│   ├── NFR_SPECIFICATIONS.md
│   └── data-contracts.md
├── 03-tests/
│   ├── test-case-registry.md
│   ├── e2e-scenarios.md
│   └── accessibility-checklist.md
└── 04-jira/
    ├── full-hierarchy.csv
    └── jira-import.json

### Registry Files (ROOT level - single source of truth)
traceability/
├── module_registry.json
├── requirements_registry.json
├── nfr_registry.json
├── test_case_registry.json
└── productspecs_traceability_register.json
```

### Upstream Sources

```
ClientAnalysis_<SystemName>/   # Discovery (if changes propagate upstream)
Prototype_<SystemName>/        # Prototype (if changes propagate upstream)
_state/                        # Shared state files
traceability/                  # Traceability registers
```

## Procedure

### Phase 1: Parse Feedback

```
EXTRACT from feedback_content:
  - keywords: technical terms, IDs, names
  - identifiers: REQ-XXX, MOD-XXX, NFR-XXX, TC-XXX
  - intent: bug, enhancement, requirement change, priority change

CLASSIFY feedback_type:
  - "Bug" if mentions error, broken, not working
  - "Enhancement" if mentions improve, add, better
  - "RequirementChange" if mentions requirement, REQ-XXX, user story
  - "PriorityChange" if mentions priority, P0, P1, P2
  - "TraceabilityGap" if mentions missing link, orphan, coverage

LOG: "Feedback type: {feedback_type}"
LOG: "Keywords: {keywords}"
LOG: "Identifiers: {identifiers}"
```

### Phase 2: Scan Module Specifications

```
FOR each file in ProductSpecs_<SystemName>/01-modules/:
  SEARCH for:
    - Keywords from feedback
    - Related identifiers
    - Module IDs mentioned

  IF match found:
    ADD to affected_items.modules
    EXTRACT:
      - module_id
      - title
      - match_context
      - linked_requirements
      - linked_screens

LOG: "Modules affected: {count}"
```

### Phase 3: Scan Requirements Registry

```
READ traceability/requirements_registry.json  # ROOT level - single source of truth

FOR each requirement:
  CHECK if:
    - ID mentioned in feedback
    - Title contains keywords
    - Description contains keywords
    - Linked to affected modules

  IF match found:
    ADD to affected_items.requirements
    EXTRACT:
      - requirement_id
      - title
      - priority
      - linked_pain_points
      - linked_jtbds

LOG: "Requirements affected: {count}"
```

### Phase 4: Scan NFRs

```
READ traceability/nfr_registry.json  # ROOT level - single source of truth

FOR each nfr:
  CHECK if:
    - ID mentioned in feedback
    - Category affected
    - Linked to affected modules

  IF match found:
    ADD to affected_items.nfrs
    EXTRACT:
      - nfr_id
      - category
      - metric

LOG: "NFRs affected: {count}"
```

### Phase 5: Scan Test Specifications

```
READ traceability/test_case_registry.json  # ROOT level - single source of truth

FOR each test_case:
  CHECK if:
    - ID mentioned in feedback
    - Tests affected requirement
    - Tests affected module

  IF match found:
    ADD to affected_items.tests
    EXTRACT:
      - test_id
      - type
      - requirement_ref

LOG: "Test cases affected: {count}"
```

### Phase 6: Scan JIRA Export

```
READ ProductSpecs_<SystemName>/04-jira/jira-import.json

FOR each jira_item:
  CHECK if:
    - Maps to affected requirement
    - Maps to affected module
    - Contains affected content

  IF match found:
    ADD to affected_items.jira
    EXTRACT:
      - jira_key
      - type (Epic/Story/Subtask)
      - requirement_ref

LOG: "JIRA items affected: {count}"
```

### Phase 7: Trace Impact Chains

```
READ traceability/productspecs_traceability_register.json  # ROOT level - single source of truth

FOR each affected_requirement:
  TRACE full chain:
    CM → PP → JTBD → REQ → Screen → Module → Test → JIRA

  IDENTIFY:
    - Upstream impacts (Discovery, Prototype)
    - Downstream impacts (JIRA regeneration needed)
    - Cross-chain impacts

ADD chain analysis to impact_analysis
```

### Phase 8: Calculate Priority Score

```
CALCULATE priority_score (0-30):

Base score:
  + 10 if affects P0 requirements
  + 5 if affects P1 requirements
  + 2 if affects P2 requirements

Impact score:
  + 5 if affects >5 modules
  + 3 if affects 2-5 modules
  + 1 if affects 1 module

Propagation score:
  + 5 if requires JIRA regeneration
  + 3 if requires test updates
  + 5 if breaks traceability chain

Type score:
  + 5 if Bug (requires fix)
  + 3 if RequirementChange
  + 2 if Enhancement

priority_score = base + impact + propagation + type
```

### Phase 9: Generate Impact Matrix

```
CREATE impact_matrix = {
  feedback_type: {type},
  severity: calculate_severity(priority_score),
  priority_score: {score},
  categories: [affected_categories],

  counts: {
    modules: len(affected_modules),
    requirements: len(affected_requirements),
    nfrs: len(affected_nfrs),
    tests: len(affected_tests),
    jira: len(affected_jira),
    total: sum_all
  },

  affected_items: {
    modules: [list],
    requirements: [list],
    nfrs: [list],
    tests: [list],
    jira: [list]
  },

  traceability_impact: {
    chains_affected: [chain_ids],
    upstream_propagation: {bool},
    jira_regeneration_needed: {bool}
  },

  recommendations: [action_recommendations]
}
```

### Phase 10: Write Impact Analysis

```
WRITE to session folder: impact_analysis.md

---
document_id: PSF-IMPACT-{feedback_id}
version: 1.0.0
created_at: {date}
updated_at: {date}
generated_by: ProductSpecs_FeedbackAnalyzer
---

# Impact Analysis

## Summary
- **Type**: {feedback_type}
- **Severity**: {severity}
- **Priority Score**: {score}/30
- **Total Items Affected**: {total}

## Impact Matrix

| Category | Count | Items |
|----------|-------|-------|
| Modules | {n} | MOD-XXX, MOD-YYY |
| Requirements | {n} | REQ-XXX, REQ-YYY |
| NFRs | {n} | NFR-XXX |
| Tests | {n} | TC-XXX |
| JIRA | {n} | INV-XXX |

## Traceability Impact

### Affected Chains
{chain_visualization}

### Propagation
- Upstream (Discovery): {Yes/No}
- Upstream (Prototype): {Yes/No}
- JIRA Regeneration: {Yes/No}

## Recommendations
1. {recommendation_1}
2. {recommendation_2}
```

## Output Format

### Impact Summary

```
═══════════════════════════════════════════════════════════════
 PRODUCTSPECS IMPACT ANALYSIS
═══════════════════════════════════════════════════════════════

Type: RequirementChange
Severity: High
Priority Score: 23/30

Impact Matrix:
────────────────────────────────────────────────────────────────
│ Category      │ Count │ Items                              │
│───────────────│───────│────────────────────────────────────│
│ Modules       │ 3     │ MOD-INV-SEARCH-01, ...            │
│ Requirements  │ 5     │ REQ-001, REQ-002, ...             │
│ NFRs          │ 2     │ NFR-PERF-001, NFR-SEC-001         │
│ Tests         │ 8     │ TC-E2E-001, TC-UNIT-003, ...      │
│ JIRA          │ 15    │ INV-1, INV-2, INV-10, ...         │
│ Total         │ 33    │                                    │

Traceability:
├─ Chains Affected: 3
├─ Upstream Propagation: No
└─ JIRA Regeneration: Yes

Recommendations:
1. Update module specifications first
2. Regenerate affected test cases
3. Re-export JIRA files after changes

═══════════════════════════════════════════════════════════════
```

## Integration Points

### Receives From
- `/productspecs-feedback` command - Raw feedback
- User input - Additional context

### Feeds Into
- `ProductSpecs_FeedbackRegister` - Impact data for registration
- `ProductSpecs_FeedbackImplementer` - Affected items list

## Error Handling

| Issue | Action |
|-------|--------|
| Registry file missing | Use markdown files as fallback |
| Module file unreadable | Skip, log to FAILURES_LOG.md |
| Traceability incomplete | Note gaps, continue analysis |
| Empty impact | Flag as low-impact, minimal changes |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: ProductSpecs Skills Framework v1.0
