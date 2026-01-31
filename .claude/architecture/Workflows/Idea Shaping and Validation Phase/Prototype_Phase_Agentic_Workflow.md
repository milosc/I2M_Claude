# Prototype Phase Multi-Agent Workflow

**Version**: 3.0.0
**Last Updated**: 2026-01-02
**Stage**: Prototype (Stage 2)

## Overview

The Prototype phase fully supports a **multi-agent approach** as of **v3.0.0** (released December 2025). This architecture enables **up to 60% faster** prototype generation through parallel execution of specialized agents.

### Key Metrics

- **Total Agents**: 11 (1 orchestrator + 5 specifiers + 5 validators)
- **Parallel Execution Groups**: 3 (Design, Screens, Validation)
- **Expected Speedup**: Up to 60% faster completion
- **Model Allocation**: 7 Sonnet agents, 4 Haiku agents (cost-optimized)
- **Checkpoints**: 14 total (2 blocking)

---

## Agent Architecture

### Categories

#### 1. Orchestration (1 agent)

| Agent ID | Name | Model | Purpose | Capabilities |
|----------|------|-------|---------|--------------|
| `prototype:orchestrator` | Prototype Orchestrator | Sonnet | Master coordinator for all Prototype agents | Phase orchestration, agent dispatch, parallel coordination, state management, quality gates, code generation |

**Skills Used**:
- `Prototype_Builder`
- `Prototype_ValidateDiscovery`
- `Prototype_Requirements`

**Commands**:
- `/prototype`
- `/prototype-resume`
- All `/prototype-*` phase commands

---

#### 2. Specification Agents (5 agents)

All use **Sonnet** model for complex design decisions and specifications.

| Agent ID | Name | Checkpoint | Purpose | Output Files |
|----------|------|------------|---------|--------------|
| `prototype:data-model-specifier` | Data Model Specifier | 3 | Generate data model from Discovery data fields | `04-implementation/data-model.md` |
| `prototype:api-contract-specifier` | API Contract Specifier | 4 | Generate OpenAPI contracts from screen requirements | `04-implementation/api-contracts.json` |
| `prototype:design-token-generator` | Design Token Generator | 6-7 | Generate design tokens and theming system | `00-foundation/design-tokens.json`, `color-system.md`, `typography.md`, `spacing-layout.md` |
| `prototype:component-specifier` | Component Specifier | 8 | Generate component library specifications | `01-components/component-index.md`, `01-components/**/*.md` |
| `prototype:screen-specifier` | Screen Specifier | 9 | Generate detailed screen specifications | `02-screens/screen-index.md`, `02-screens/[screen-name]/spec.md` |

**Skills Mapping**:

| Agent | Skills Used |
|-------|-------------|
| `prototype:data-model-specifier` | `Prototype_DataModel` |
| `prototype:api-contract-specifier` | `Prototype_ApiContracts`, `Prototype_TestData` |
| `prototype:design-token-generator` | `Prototype_DesignBrief`, `Prototype_DesignTokens` |
| `prototype:component-specifier` | `Prototype_Components`, `Prototype_Decomposition` |
| `prototype:screen-specifier` | `Prototype_Screens`, `Prototype_Interactions` |

**Commands**:
- `/prototype-data` - Triggers data model and API contracts
- `/prototype-design` - Triggers design tokens
- `/prototype-components` - Triggers component specifications
- `/prototype-screens` - Triggers screen specifications

---

#### 3. Validation Agents (5 agents)

Use **Haiku** for pattern-based validation (cost-optimized), **Sonnet** for complex validation.

| Agent ID | Name | Model | Checkpoint | Purpose | Output Files |
|----------|------|-------|------------|---------|--------------|
| `prototype:component-validator` | Component Validator | Haiku | 13 | Validate component spec completeness | `05-validation/component-validation.md` |
| `prototype:screen-validator` | Screen Validator | Haiku | 13 | Validate screen coverage and traceability | `05-validation/screen-validation.md` |
| `prototype:ux-validator` | UX Validator | Haiku | 13 | Validate UX patterns and consistency | `05-validation/ux-validation.md` |
| `prototype:accessibility-auditor` | Accessibility Auditor | Sonnet | 13 | Validate WCAG 2.1 AA compliance | `05-validation/accessibility-report.md` |
| `prototype:visual-qa-tester` | Visual QA Tester | Sonnet | 14 | Perform visual regression testing with Playwright | `05-validation/ui-audit-report.md`, `05-validation/screenshots/` |

**Skills Mapping**:

| Agent | Skills Used |
|-------|-------------|
| All validators (except visual-qa) | `Prototype_QA` |
| `prototype:visual-qa-tester` | `Prototype_UIAudit` |

**Commands**:
- `/prototype-qa` - Triggers all validation agents
- `/prototype-ui-audit` - Triggers visual QA tester (Playwright)

---

## Sequential vs Parallel Execution

### Sequential Phases (Must Complete in Order)

```
CHECKPOINT 0: Initialize
  ├── No agents
  └── Creates folder structure, state files

CHECKPOINT 1: Validate Discovery [BLOCKING]
  ├── No agents
  └── Validates Discovery CP11+, required files exist

CHECKPOINT 2: Extract Requirements
  ├── No agents
  └── Builds requirements registry from Discovery

CHECKPOINT 3: Data Model [SEQUENTIAL]
  └── prototype:data-model-specifier (Sonnet)
      └── Skills: Prototype_DataModel

CHECKPOINT 4: API Contracts [SEQUENTIAL]
  └── prototype:api-contract-specifier (Sonnet)
      ├── Depends on: CP3 (data model)
      └── Skills: Prototype_ApiContracts, Prototype_TestData

CHECKPOINT 5: Test Data [SEQUENTIAL]
  ├── No agents
  └── Generates mock data files

CHECKPOINT 10: Interactions [SEQUENTIAL]
  ├── No agents
  └── Motion, accessibility, responsive specs

CHECKPOINT 11: Build Sequence [SEQUENTIAL]
  ├── No agents
  └── Generates build order for code generation

CHECKPOINT 12: Code Generation [SEQUENTIAL]
  ├── No agents (orchestrator handles)
  └── Generates React prototype code
```

### Parallel Execution Groups

#### Group 1: Design Foundations (Checkpoints 6-7)

**Parallel Agents**: 3 agents run concurrently

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 6-7: DESIGN SPECIFICATION (PARALLEL)                │
│                                                             │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │ design-token-        │  │ component-           │        │
│  │ generator            │  │ specifier            │        │
│  │ (Sonnet)             │  │ (Sonnet)             │        │
│  │                      │  │                      │        │
│  │ Skills:              │  │ Skills:              │        │
│  │ - DesignBrief        │  │ - Components         │        │
│  │ - DesignTokens       │  │ - Decomposition      │        │
│  │                      │  │                      │        │
│  │ Output:              │  │ Output:              │        │
│  │ - design-tokens.json │  │ - component-index.md │        │
│  │ - color-system.md    │  │ - component specs    │        │
│  │ - typography.md      │  │                      │        │
│  └──────────┬───────────┘  └──────────┬───────────┘        │
│             │                         │                    │
│             │  ┌──────────────────────┐                    │
│             │  │ data-model-          │                    │
│             │  │ specifier            │                    │
│             │  │ (Sonnet)             │                    │
│             │  │                      │                    │
│             │  │ Skills:              │                    │
│             │  │ - DataModel          │                    │
│             │  │                      │                    │
│             │  │ Output:              │                    │
│             │  │ - data-model.md      │                    │
│             └──┴──────────┬───────────┘                    │
│                           ▼                                │
│              ┌────────────────────────┐                    │
│              │  MERGE GATE            │                    │
│              │  Cross-reference:      │                    │
│              │  - Tokens → Components │                    │
│              │  - Components → Data   │                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Invocation Pattern**:
```javascript
// Spawn 3 agents in parallel
const designAgents = [
  Task({
    subagent_type: "prototype:design-token-generator",
    model: "sonnet",
    description: "Generate design tokens",
    prompt: "..."
  }),
  Task({
    subagent_type: "prototype:component-specifier",
    model: "sonnet",
    description: "Specify components",
    prompt: "..."
  }),
  Task({
    subagent_type: "prototype:data-model-specifier",
    model: "sonnet",
    description: "Specify data model",
    prompt: "..."
  })
];

// Wait for all to complete
await Promise.all(designAgents);

// Merge outputs
await merge_design_outputs();
```

**Commands**: `/prototype-design`, `/prototype-components`

---

#### Group 2: Screen & API Specification (Checkpoints 8-9)

**Parallel Agents**: 2 agents run concurrently (screen-specifier can spawn N agents for N screens)

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 8-9: SCREEN & API SPECIFICATION (PARALLEL)          │
│                                                             │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │ screen-specifier     │  │ api-contract-        │        │
│  │ (Sonnet)             │  │ specifier            │        │
│  │                      │  │ (Sonnet)             │        │
│  │ Skills:              │  │                      │        │
│  │ - Screens            │  │ Skills:              │        │
│  │ - Interactions       │  │ - ApiContracts       │        │
│  │                      │  │ - TestData           │        │
│  │ Strategy:            │  │                      │        │
│  │ ONE AGENT PER SCREEN │  │ Output:              │        │
│  │ (scales with         │  │ - api-contracts.json │        │
│  │  Discovery screens)  │  │ - mock data files    │        │
│  │                      │  │                      │        │
│  │ Output:              │  │ Depends on:          │        │
│  │ - screen-index.md    │  │ - data-model (CP3)   │        │
│  │ - screen specs       │  │                      │        │
│  └──────────┬───────────┘  └──────────┬───────────┘        │
│             │                         │                    │
│             └────────────┬────────────┘                    │
│                          ▼                                 │
│              ┌────────────────────────┐                    │
│              │  MERGE GATE            │                    │
│              │  Ensure:               │                    │
│              │  - Screen-API align    │                    │
│              │  - 100% screen coverage│                    │
│              └────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

**Per-Screen Parallelization**:
```javascript
// Get screens from Discovery
const discoveryScreens = await getDiscoveryScreens();

// Spawn one agent per screen
const screenAgents = discoveryScreens.map(screen =>
  Task({
    subagent_type: "prototype:screen-specifier",
    model: "sonnet",
    description: `Specify screen: ${screen.id}`,
    prompt: `
      Generate specification for screen ${screen.id}.
      INPUT: ${DISCOVERY_PATH}/04-design-specs/screen-definitions.md
      OUTPUT: ${OUTPUT_PATH}/02-screens/${screen.slug}/
    `
  })
);

// Run in parallel (up to 5 concurrent)
await Promise.all(screenAgents);
```

**Commands**: `/prototype-screens`

---

#### Group 3: Validation (Checkpoint 13)

**Parallel Agents**: 4 validators run concurrently, then 1 final QA

```
┌─────────────────────────────────────────────────────────────┐
│  PHASE 13-14: VALIDATION (4 PARALLEL + 1 FINAL)            │
│                                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │Component │ │  Screen  │ │   UX     │ │  Access. │      │
│  │Validator │ │Validator │ │Validator │ │  Auditor │      │
│  │ (Haiku)  │ │ (Haiku)  │ │ (Haiku)  │ │ (Sonnet) │      │
│  │          │ │          │ │          │ │          │      │
│  │ Skills:  │ │ Skills:  │ │ Skills:  │ │ Skills:  │      │
│  │ - QA     │ │ - QA     │ │ - QA     │ │ - QA     │      │
│  │          │ │          │ │          │ │          │      │
│  │ Checks:  │ │ Checks:  │ │ Checks:  │ │ Checks:  │      │
│  │ - Spec   │ │ - Screen │ │ - Pattern│ │ - WCAG   │      │
│  │   compl. │ │   cover. │ │   consis.│ │   2.1 AA │      │
│  │ - Props  │ │ - Comp.  │ │ - Nav    │ │ - ARIA   │      │
│  │ - Varian.│ │   usage  │ │   flow   │ │ - Keyb.  │      │
│  │ - Tokens │ │ - Data   │ │ - Error  │ │ - Color  │      │
│  │          │ │   flow   │ │   states │ │   contra.│      │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘      │
│       │            │            │            │            │
│       └────────────┼────────────┼────────────┘            │
│                    ▼            ▼                         │
│          ┌─────────────────────────────┐                  │
│          │  VALIDATION MERGE GATE      │                  │
│          │  Aggregate findings:        │                  │
│          │  - Critical issues: 0       │                  │
│          │  - High issues: documented  │                  │
│          │  - Coverage: 100%           │                  │
│          └─────────────┬───────────────┘                  │
│                        ▼                                  │
│          ┌─────────────────────────────┐                  │
│          │  Visual QA Tester (Sonnet)  │ [BLOCKING CP14] │
│          │                             │                  │
│          │  Skills: UIAudit            │                  │
│          │                             │                  │
│          │  Process:                   │                  │
│          │  1. npm run build           │                  │
│          │  2. npm run dev             │                  │
│          │  3. Playwright screenshots  │                  │
│          │  4. Visual comparison       │                  │
│          │  5. Generate report         │                  │
│          │                             │                  │
│          │  Output:                    │                  │
│          │  - ui-audit-report.md       │                  │
│          │  - screenshots/             │                  │
│          └─────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

**Invocation Pattern**:
```javascript
// Phase 13: Spawn 4 validators in parallel
const validators = [
  Task({
    subagent_type: "prototype:component-validator",
    model: "haiku",
    description: "Validate components",
    prompt: "..."
  }),
  Task({
    subagent_type: "prototype:screen-validator",
    model: "haiku",
    description: "Validate screens",
    prompt: "..."
  }),
  Task({
    subagent_type: "prototype:ux-validator",
    model: "haiku",
    description: "Validate UX patterns",
    prompt: "..."
  }),
  Task({
    subagent_type: "prototype:accessibility-auditor",
    model: "sonnet",
    description: "Audit accessibility",
    prompt: "..."
  })
];

// Wait for all validators
await Promise.all(validators);

// Merge validation results
await merge_validation_reports();

// Check if critical issues exist
if (criticalIssues > 0) {
  BLOCK("Cannot proceed to CP14 with critical issues");
}

// Phase 14: Run visual QA (sequential)
await Task({
  subagent_type: "prototype:visual-qa-tester",
  model: "sonnet",
  description: "Visual QA with Playwright",
  prompt: "..."
});
```

**Commands**: `/prototype-qa`, `/prototype-ui-audit`

---

## Complete Execution Flow

### Standard Mode (Default)

```
/prototype <SystemName>

FLOW:
├── CP0:  Initialize                    [Sequential]
├── CP1:  Validate Discovery            [Sequential, BLOCKING]
├── CP2:  Extract Requirements          [Sequential]
├── CP3:  Data Model                    [Sequential]
│         └── data-model-specifier (Sonnet)
├── CP4:  API Contracts                 [Sequential]
│         └── api-contract-specifier (Sonnet)
├── CP5:  Test Data                     [Sequential]
├── CP6-7: Design Foundations           [PARALLEL - 3 agents]
│         ├── design-token-generator (Sonnet)
│         ├── component-specifier (Sonnet)
│         └── data-model-specifier (Sonnet)
│         └── [MERGE GATE]
├── CP8:  Components                    [Sequential]
├── CP9:  Screens                       [PARALLEL - N agents per screen]
│         └── screen-specifier (Sonnet) x N
│         └── [MERGE GATE]
├── CP10: Interactions                  [Sequential]
├── CP11: Build Sequence                [Sequential]
├── CP12: Code Generation               [Sequential]
├── CP13: Validation                    [PARALLEL - 4 agents]
│         ├── component-validator (Haiku)
│         ├── screen-validator (Haiku)
│         ├── ux-validator (Haiku)
│         └── accessibility-auditor (Sonnet)
│         └── [MERGE GATE]
└── CP14: Visual QA                     [Sequential, BLOCKING]
          └── visual-qa-tester (Sonnet)
```

### Parallel Mode (Enhanced)

```
/prototype <SystemName> --mode parallel

SAME FLOW as Standard Mode with:
  - More aggressive parallelization at CP6-7, CP9, CP13
  - Higher concurrent agent limits (up to 5 simultaneous)
  - Optimized for speed over cost
```

---

## Commands Reference

### Primary Commands

| Command | Phase | Agents Triggered | Mode |
|---------|-------|------------------|------|
| `/prototype <SystemName>` | 0-14 | All agents | Sequential + Parallel groups |
| `/prototype <SystemName> --mode parallel` | 0-14 | All agents | Enhanced parallel |
| `/prototype-resume` | Resume | From last checkpoint | Resumes previous mode |

### Phase-Specific Commands

| Command | Checkpoints | Agents | Execution |
|---------|-------------|--------|-----------|
| `/prototype-init` | 0 | None | Sequential |
| `/prototype-validate` | 1 | None | Sequential |
| `/prototype-requirements` | 2 | None | Sequential |
| `/prototype-data` | 3-5 | `data-model-specifier`, `api-contract-specifier` | Sequential |
| `/prototype-design` | 6-7 | `design-token-generator` | Sequential |
| `/prototype-components` | 8 | `component-specifier` | Sequential (or parallel in v3.0) |
| `/prototype-screens` | 9 | `screen-specifier` (x N) | Parallel (per screen) |
| `/prototype-interactions` | 10 | None | Sequential |
| `/prototype-build` | 11-12 | None (orchestrator) | Sequential |
| `/prototype-qa` | 13 | All 4 validators | Parallel |
| `/prototype-ui-audit` | 14 | `visual-qa-tester` | Sequential |

### Utility Commands

| Command | Purpose |
|---------|---------|
| `/prototype-status` | Show current progress and checkpoint |
| `/prototype-reset` | Reset state (--soft/--hard/--phase N) |
| `/prototype-export` | Package for ProductSpecs stage |
| `/prototype-feedback` | Process change requests with debugging |

---

## Skills Reference

### Skill → Agent Mapping

| Skill | Agents Using It | Purpose |
|-------|-----------------|---------|
| `Prototype_Builder` | `prototype:orchestrator` | Master orchestration |
| `Prototype_ValidateDiscovery` | `prototype:orchestrator` | CP1 validation |
| `Prototype_Requirements` | `prototype:orchestrator` | CP2 extraction |
| `Prototype_DataModel` | `data-model-specifier` | Entity & relationship mapping |
| `Prototype_ApiContracts` | `api-contract-specifier` | OpenAPI generation |
| `Prototype_TestData` | `api-contract-specifier` | Mock data generation |
| `Prototype_DesignBrief` | `design-token-generator` | Design direction |
| `Prototype_DesignTokens` | `design-token-generator` | Token generation |
| `Prototype_Components` | `component-specifier` | Component specs |
| `Prototype_Decomposition` | `component-specifier` | Component breakdown |
| `Prototype_Screens` | `screen-specifier` | Screen specs |
| `Prototype_Interactions` | `screen-specifier` | Motion & responsive specs |
| `Prototype_QA` | All validators (except visual-qa) | Validation logic |
| `Prototype_UIAudit` | `visual-qa-tester` | Playwright screenshots |

### Agent → Skill Invocation Pattern

Each agent invokes its assigned skill(s) using the Skill tool:

```javascript
// Example: design-token-generator agent
Skill({
  skill: "Prototype_DesignTokens",
  args: `
    DISCOVERY_PATH=${DISCOVERY_PATH}
    OUTPUT_PATH=${OUTPUT_PATH}/00-foundation/
  `
});
```

---

## Agent Configuration Files

All agent definitions are located in `.claude/agents/`:

```
.claude/agents/
├── prototype-orchestrator.md          # Master coordinator
├── design-token-generator.md          # Design tokens (CP6-7)
├── component-specifier.md             # Components (CP8)
├── screen-specifier.md                # Screens (CP9)
├── data-model-specifier.md            # Data model (CP3)
├── api-contract-specifier.md          # API contracts (CP4)
├── component-validator.md             # Component QA (CP13)
├── screen-validator.md                # Screen QA (CP13)
├── ux-validator.md                    # UX QA (CP13)
├── accessibility-auditor.md           # A11y QA (CP13)
├── visual-qa-tester.md                # Visual QA (CP14)
└── PROTOTYPE_AGENT_REGISTRY.json      # Agent registry & config
```

### Agent Registry Schema

```json
{
  "agents": [
    {
      "id": "prototype:agent-name",
      "category": "specification|validation|orchestration",
      "model": "sonnet|haiku",
      "checkpoint": "N",
      "parallel_group": "design|screens|validation",
      "depends_on": ["other-agent-id"],
      "skill_refs": ["Skill_Name"],
      "inputs": ["path/to/input"],
      "outputs": ["path/to/output"]
    }
  ],
  "parallel_groups": {
    "group_name": {
      "checkpoint": "N",
      "agents": ["agent-id"],
      "strategy": "all_parallel|per_screen"
    }
  }
}
```

---

## Coordination Mechanisms

### Lock-Free Design

**Key Principle**: Agents never modify the same file concurrently.

```
PARALLEL EXECUTION SAFETY:
  ├── Read-Only Discovery Access:
  │   └── All agents READ from ClientAnalysis_* (immutable)
  │
  ├── Isolated Output Paths:
  │   ├── design-token-generator   → 00-foundation/
  │   ├── component-specifier       → 01-components/
  │   ├── screen-specifier          → 02-screens/[screen-name]/
  │   └── validators                → 05-validation/
  │
  └── State Management:
      ├── _state/progress.json (orchestrator only)
      └── _state/prompt_log.json (append-only with IDs)
```

### Merge Gates

After each parallel group, a merge gate validates consistency:

```python
# Example: Design merge gate (CP6-7)
def merge_design_outputs():
    tokens = read("00-foundation/design-tokens.json")
    components = read("01-components/component-index.md")
    data_model = read("04-implementation/data-model.md")

    # Cross-reference validation
    validate_components_use_tokens(components, tokens)
    validate_components_match_entities(components, data_model)

    # Generate cross-reference index
    generate_design_index(tokens, components, data_model)
```

### Dependency Resolution

Agents with `depends_on` wait for prerequisite agents:

```json
{
  "id": "prototype:api-contract-specifier",
  "depends_on": ["prototype:data-model-specifier"],
  "checkpoint": 4
}
```

Orchestrator ensures:
1. `data-model-specifier` completes at CP3
2. `api-contract-specifier` starts at CP4 (after data model exists)

---

## Quality Gates

### Blocking Checkpoints

| Checkpoint | Name | Validation | Blocks If |
|------------|------|------------|-----------|
| **CP1** | Validate Discovery | `discovery_checkpoint >= 11`, required files exist | Discovery incomplete or missing files |
| **CP14** | UI Audit | `screen_coverage == 100%`, `all_screens_have_react_code`, `wcag_aa_compliance` | Any screen missing code or WCAG fails |

### Non-Blocking Checkpoints

All other checkpoints (CP2-13) are non-blocking but log warnings for issues.

### Coverage Requirements

- **P0 Requirements**: 100% coverage required at CP2
- **Screen Coverage**: 100% Discovery screens must have specs at CP9
- **Component Coverage**: All screens must use specified components at CP13
- **Traceability**: All specs linked back to Discovery at CP14

---

## Performance Optimization

### Model Allocation Strategy

**Cost vs Speed Tradeoff**:

| Task Type | Model | Rationale | Count |
|-----------|-------|-----------|-------|
| Complex design decisions | Sonnet | Better design quality, accurate specifications | 7 |
| Pattern-based validation | Haiku | Faster, cheaper, sufficient for checks | 3 |

**Estimated Cost Reduction**: ~30% vs all-Sonnet approach

### Concurrency Limits

```json
{
  "design_group": {
    "max_concurrent": 3,
    "agents": ["design-token-generator", "component-specifier", "data-model-specifier"]
  },
  "screen_group": {
    "max_concurrent": 5,
    "agents": ["screen-specifier"]
  },
  "validation_group": {
    "max_concurrent": 4,
    "agents": ["component-validator", "screen-validator", "ux-validator", "accessibility-auditor"]
  }
}
```

### Expected Speedup Breakdown

| Phase | Sequential Time | Parallel Time | Speedup |
|-------|-----------------|---------------|---------|
| CP6-7 (Design) | 30 min | 10 min | 3x |
| CP9 (Screens, N=10) | 50 min | 15 min | 3.3x |
| CP13 (Validation) | 20 min | 7 min | 2.9x |
| **Total** | **100 min** | **40 min** | **2.5x (60% faster)** |

---

## Traceability

### ID Chains

Every agent maintains full traceability from Discovery to Prototype:

```
Discovery → Prototype Traceability Chain:

PP-X.X (Pain Point)
  ↓
JTBD-X.X (Job To Be Done)
  ↓
REQ-NNN (Requirement) ← Generated at CP2
  ↓
US-NNN (User Story) ← Generated at CP2
  ↓
S-X.X (Discovery Screen)
  ↓
SCR-NNN (Prototype Screen) ← Generated by screen-specifier
  ↓
COMP-NNN (Component) ← Generated by component-specifier
```

### Registry Files

| Registry | Location | Managed By | Purpose |
|----------|----------|------------|---------|
| Requirements | `_state/requirements_registry.json` | Orchestrator (CP2) | REQ-NNN, US-NNN |
| Screens | `traceability/screen_registry.json` | screen-specifier (CP9) | SCR-NNN |
| Components | `traceability/component_registry.json` | component-specifier (CP8) | COMP-NNN |

---

## Failure Handling

### Agent Failure Protocol

```
IF agent fails:
  1. Log failure to _state/FAILURES_LOG.md
  2. Record in _state/progress.json with error details
  3. IF blocking checkpoint:
       HALT pipeline, report to user
     ELSE:
       CONTINUE with available data, mark checkpoint partial
  4. User can review/retry via /prototype-resume
```

### Partial Completion

Prototype supports resuming from any checkpoint:

```bash
# Resume after fixing issues
/prototype-resume

# Or reset specific phase and resume
/prototype-reset --phase 9
/prototype-resume
```

---

## Comparison with Other Stages

| Stage | Agents | Parallel Groups | Sequential Phases | Speedup |
|-------|--------|-----------------|-------------------|---------|
| Discovery | 11 | 3 | 8 | ~50% |
| **Prototype** | **11** | **3** | **9** | **~60%** |
| ProductSpecs | 8 | 2 | 6 | ~40% |
| SolArch | 15 | 4 | 9 | ~55% |
| Implementation | 12 | 2 | 7 | ~50% |

**Prototype has the most mature parallel execution strategy** with clear separation between specification and validation agents.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0.0 | 2025-12-27 | Added parallel agent execution with 10 specialized agents (5 specifiers + 5 validators). Expected 60% speedup. |
| 2.3.1 | 2025-12-19 | Added version control metadata per VERSION_CONTROL_STANDARD.md. |
| 2.3.0 | 2024-12-13 | Initial Prototype Skills Framework. |

---

## Related Documentation

- **Agent Definitions**: `.claude/agents/*.md`
- **Agent Registry**: `.claude/agents/PROTOTYPE_AGENT_REGISTRY.json`
- **Skill Registry**: `.claude/skills/Prototype_Builder/PROTOTYPE_SKILL_REGISTRY.json`
- **Commands**: `.claude/commands/PROTOTYPE_COMMAND_REFERENCE.md`
- **Skills**: `.claude/skills/Prototype_*/SKILL.md`
- **Quality Gates**: `.claude/hooks/prototype_quality_gates.py`
- **Assembly-First Architecture**: `architecture/Assembly-First Design System/`

---

## Quick Reference

### Enable Parallel Execution

```bash
# Standard mode with parallel groups
/prototype InventorySystem

# Enhanced parallel mode
/prototype InventorySystem --mode parallel
```

### Monitor Progress

```bash
# Check current status
/prototype-status

# View prompt log
cat _state/prompt_log.json | jq '.summary'

# Check failures
cat _state/FAILURES_LOG.md
```

### Debug Agent Issues

```bash
# View agent registry
cat .claude/agents/PROTOTYPE_AGENT_REGISTRY.json | jq '.agents[] | {id, checkpoint, parallel_group}'

# Check quality gates
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 9 --dir Prototype_InventorySystem/

# Verify traceability
python3 .claude/hooks/prototype_quality_gates.py --validate-traceability --dir Prototype_InventorySystem/
```

---

**End of Document**
