---
name: README
description: HTEC Multi-Agent Architecture
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
# HTEC Multi-Agent Architecture

**Version**: 2.0.0
**Updated**: 2025-12-27

This folder contains agent definitions for the HTEC multi-agent implementation system. Agents are specialized Claude instances that work in parallel to accelerate execution while maintaining quality and traceability across all pipeline stages.

---

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              HTEC I2M PIPELINE STAGES                                   │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  STAGE 1          STAGE 2          STAGE 3          STAGE 4          STAGE 5           │
│  ┌────────┐      ┌────────┐       ┌──────────┐     ┌────────┐       ┌──────────────┐   │
│  │DISCOVERY│ ──▶ │PROTOTYPE│ ──▶  │PRODUCTSPECS│ ──▶│SOLARCH │ ──▶   │IMPLEMENTATION│   │
│  │ 9 agents│      │11 agents│       │11 agents │     │17 agents│       │  20+ agents  │   │
│  └────────┘      └────────┘       └──────────┘     └────────┘       └──────────────┘   │
│                                                                                         │
│  Raw Materials   Design Specs     Module Specs     Architecture    Production Code     │
│  ──────────▶     ──────────▶      ──────────▶      ──────────▶     ──────────▶        │
│  Pain Points     Components       Test Specs       C4/ADRs         Tested Software     │
│  Personas        React Code       JIRA Export      Quality Reqs    Documentation       │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Stage Registries

| Stage | Folder | Registry File | Agents | Orchestrator |
|-------|--------|---------------|--------|--------------|
| **1. Discovery** | `discovery/` | `DISCOVERY_AGENT_REGISTRY.json` | 9 | `discovery:orchestrator` |
| **2. Prototype** | `prototype/` | `PROTOTYPE_AGENT_REGISTRY.json` | 11 | `prototype:orchestrator` |
| **3. ProductSpecs** | `productspecs/` | `PRODUCTSPECS_AGENT_REGISTRY.json` | 11 | `productspecs:orchestrator` |
| **4. SolArch** | `solarch/` | `SOLARCH_AGENT_REGISTRY.json` | 17 | `solarch:orchestrator` |
| **5. Implementation** | (multiple) | N/A | 20+ | Tech Lead |

---

## Stage 1: Discovery (9 Agents)

Transforms raw client materials into structured insights.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DISCOVERY AGENT FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ORCHESTRATOR ─────────────────────────────────────────────────────────────▶│
│       │                                                                     │
│       │  CP-1: PARALLEL ANALYSIS                                            │
│       ├────────────────────────────────────────────────────────────────┐    │
│       │  ┌───────────────┐ ┌─────────────┐ ┌───────────────┐          │    │
│       │  │ interview-    │ │ data-       │ │ design-       │          │    │
│       │  │ analyst       │ │ analyst     │ │ analyst       │          │    │
│       │  │ [sonnet]      │ │ [haiku]     │ │ [haiku]       │          │    │
│       │  └───────────────┘ └─────────────┘ └───────────────┘          │    │
│       └────────────────────────────────────────────────────────────────┘    │
│       │                                                                     │
│       │  CP-1.5: PDF DEEP ANALYSIS                                          │
│       ├──────────────────────┐                                              │
│       │  ┌───────────────┐   │                                              │
│       │  │ pdf-analyst   │   │  Creates [PDF_Name]_Analysis/ folders        │
│       │  │ [sonnet]      │   │                                              │
│       │  └───────────────┘   │                                              │
│       └──────────────────────┘                                              │
│       │                                                                     │
│       │  CP-2: EXTRACTION                                                   │
│       ├──────────────────────┐                                              │
│       │  ┌────────────────┐  │                                              │
│       │  │ pain-point-    │  │                                              │
│       │  │ validator      │  │                                              │
│       │  │ [sonnet]       │  │                                              │
│       │  └────────────────┘  │                                              │
│       └──────────────────────┘                                              │
│       │                                                                     │
│       │  CP-3: PARALLEL PERSONAS                                            │
│       ├────────────────────────────────────────────────────────────────┐    │
│       │  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐     │    │
│       │  │ persona-gen    │ │ persona-gen    │ │ persona-gen    │     │    │
│       │  │ (user type 1)  │ │ (user type 2)  │ │ (user type N)  │     │    │
│       │  └────────────────┘ └────────────────┘ └────────────────┘     │    │
│       └────────────────────────────────────────────────────────────────┘    │
│       │                                                                     │
│       │  CP-4: JTBD                                                         │
│       ├──────────────────────┐                                              │
│       │  ┌────────────────┐  │                                              │
│       │  │ jtbd-extractor │  │                                              │
│       │  │ [sonnet]       │  │                                              │
│       │  └────────────────┘  │                                              │
│       └──────────────────────┘                                              │
│       │                                                                     │
│       │  CP-11: VALIDATION [BLOCKING]                                       │
│       ├──────────────────────┐                                              │
│       │  ┌──────────────────┐│                                              │
│       │  │ cross-reference- ││                                              │
│       │  │ validator       ││                                              │
│       │  │ [haiku]         ││                                              │
│       │  └──────────────────┘│                                              │
│       └──────────────────────┘                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Discovery Agents

| Agent ID | Name | Model | Purpose |
|----------|------|-------|---------|
| `discovery-orchestrator` | Discovery Orchestrator | sonnet | Master coordinator, 12 checkpoints |
| `discovery-interview-analyst` | Interview Analyst | sonnet | Transcript analysis, quote extraction |
| `discovery-pdf-analyst` | PDF Analyst | sonnet | Deep PDF analysis with chunking |
| `discovery-data-analyst` | Data Analyst | haiku | Spreadsheet analysis, metrics |
| `discovery-design-analyst` | Design Analyst | haiku | Screenshot/wireframe analysis |
| `discovery-pain-point-validator` | Pain Point Validator | sonnet | Pain point extraction & severity |
| `discovery-persona-generator` | Persona Generator | sonnet | Persona synthesis, day-in-life |
| `discovery-jtbd-extractor` | JTBD Extractor | sonnet | Jobs-to-be-done mapping |
| `discovery-cross-reference-validator` | Cross-Reference Validator | haiku | ID validation, completeness |

### Discovery Traceability IDs

| Type | Format | Example |
|------|--------|---------|
| Client Material | CM-NNN | CM-001 |
| Pain Point | PP-X.Y | PP-1.2 |
| Persona | PERSONA_{ROLE} | PERSONA_WAREHOUSE_OPERATOR |
| JTBD | JTBD-X.Y | JTBD-1.1 |
| Screen | S-X.Y | S-1.1 |

---

## Stage 2: Prototype (11 Agents)

Transforms Discovery outputs into working prototypes.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PROTOTYPE AGENT FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ORCHESTRATOR ─────────────────────────────────────────────────────────────▶│
│       │                                                                     │
│       │  CP-1: VALIDATE DISCOVERY [BLOCKING]                                │
│       │  CP-2: EXTRACT REQUIREMENTS                                         │
│       │                                                                     │
│       │  CP-3-5: DATA & API (Sequential)                                    │
│       ├──────────────────────────────────────────────────────────────┐      │
│       │  ┌───────────────┐ ┌───────────────┐ ┌──────────────┐       │      │
│       │  │ data-model-   │▶│ api-contract- │▶│ test-data    │       │      │
│       │  │ specifier     │ │ specifier     │ │ generation   │       │      │
│       │  │ [sonnet]      │ │ [sonnet]      │ │              │       │      │
│       │  └───────────────┘ └───────────────┘ └──────────────┘       │      │
│       └──────────────────────────────────────────────────────────────┘      │
│       │                                                                     │
│       │  CP-6-8: DESIGN (Sequential)                                        │
│       ├──────────────────────────────────────────────────────────────┐      │
│       │  ┌───────────────┐ ┌───────────────┐                        │      │
│       │  │ design-token- │▶│ component-    │                        │      │
│       │  │ generator     │ │ specifier     │                        │      │
│       │  │ [sonnet]      │ │ [sonnet]      │                        │      │
│       │  └───────────────┘ └───────────────┘                        │      │
│       └──────────────────────────────────────────────────────────────┘      │
│       │                                                                     │
│       │  CP-9: PARALLEL SCREENS                                             │
│       ├────────────────────────────────────────────────────────────────┐    │
│       │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────┐ │    │
│       │  │screen-spec  │ │screen-spec  │ │screen-spec  │ │screen-   │ │    │
│       │  │(dashboard)  │ │(inventory)  │ │(transfer)   │ │spec (N)  │ │    │
│       │  │[sonnet]     │ │[sonnet]     │ │[sonnet]     │ │[sonnet]  │ │    │
│       │  └─────────────┘ └─────────────┘ └─────────────┘ └──────────┘ │    │
│       └────────────────────────────────────────────────────────────────┘    │
│       │                                                                     │
│       │  CP-13: PARALLEL VALIDATION                                         │
│       ├────────────────────────────────────────────────────────────────┐    │
│       │  ┌──────────────┐ ┌──────────────┐ ┌──────────┐ ┌───────────┐ │    │
│       │  │ component-   │ │ screen-      │ │ ux-      │ │ a11y-     │ │    │
│       │  │ validator    │ │ validator    │ │ validator│ │ auditor   │ │    │
│       │  │ [haiku]      │ │ [haiku]      │ │ [haiku]  │ │ [sonnet]  │ │    │
│       │  └──────────────┘ └──────────────┘ └──────────┘ └───────────┘ │    │
│       └────────────────────────────────────────────────────────────────┘    │
│       │                                                                     │
│       │  CP-14: UI AUDIT [BLOCKING]                                         │
│       ├──────────────────────┐                                              │
│       │  ┌──────────────────┐│                                              │
│       │  │ visual-qa-tester ││  100% screen coverage required               │
│       │  │ [sonnet]         ││                                              │
│       │  └──────────────────┘│                                              │
│       └──────────────────────┘                                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Prototype Agents

| Agent ID | Name | Model | Purpose |
|----------|------|-------|---------|
| `prototype-orchestrator` | Prototype Orchestrator | sonnet | Master coordinator, 15 checkpoints |
| `prototype-data-model-specifier` | Data Model Specifier | sonnet | Entity extraction, type definitions |
| `prototype-api-contract-specifier` | API Contract Specifier | haiku | OpenAPI generation (templated) |
| `prototype-design-token-generator` | Design Token Generator | haiku | Colors, typography, spacing (JSON) |
| `prototype-component-specifier` | Component Specifier | sonnet | Component library specs |
| `prototype-screen-specifier` | Screen Specifier | sonnet | Screen layouts, state management |
| `prototype-component-validator` | Component Validator | haiku | Spec completeness check |
| `prototype-screen-validator` | Screen Validator | haiku | Coverage, data flow |
| `prototype-ux-validator` | UX Validator | haiku | Pattern consistency |
| `prototype-accessibility-auditor` | Accessibility Auditor | haiku | WCAG checklist-based |
| `prototype-visual-qa-tester` | Visual QA Tester | sonnet | Screenshot regression |

### Prototype Traceability IDs

| Type | Format | Example |
|------|--------|---------|
| Requirement | REQ-NNN | REQ-001 |
| User Story | US-NNN | US-001 |
| Screen | SCR-NNN | SCR-001 |
| Component | COMP-NNN | COMP-001 |

---

## Stage 3: ProductSpecs (11 Agents)

Generates production specifications with full traceability.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       PRODUCTSPECS AGENT FLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ORCHESTRATOR ─────────────────────────────────────────────────────────────▶│
│       │                                                                     │
│       │  CP-1: VALIDATE INPUTS [BLOCKING]                                   │
│       │  CP-2: EXTRACT REQUIREMENTS                                         │
│       │                                                                     │
│       │  CP-3-4: PARALLEL MODULE GENERATION                                 │
│       ├────────────────────────────────────────────────────────────────┐    │
│       │  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐        │    │
│       │  │ ui-module-    │ │ api-module-   │ │ nfr-          │        │    │
│       │  │ specifier     │ │ specifier     │ │ generator     │        │    │
│       │  │ [sonnet]      │ │ [sonnet]      │ │ [sonnet]      │        │    │
│       │  └───────────────┘ └───────────────┘ └───────────────┘        │    │
│       └────────────────────────────────────────────────────────────────┘    │
│       │                                                                     │
│       │  CP-6: PARALLEL TEST GENERATION                                     │
│       ├────────────────────────────────────────────────────────────────┐    │
│       │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌─────────────┐ │    │
│       │  │ unit-test- │ │integration-│ │ e2e-test-  │ │ pict-       │ │    │
│       │  │ specifier  │ │test-spec   │ │ specifier  │ │ combinatorial││    │
│       │  │ [sonnet]   │ │ [sonnet]   │ │ [sonnet]   │ │ [haiku]     │ │    │
│       │  └────────────┘ └────────────┘ └────────────┘ └─────────────┘ │    │
│       └────────────────────────────────────────────────────────────────┘    │
│       │                                                                     │
│       │  CP-7: PARALLEL VALIDATION [BLOCKING]                               │
│       ├────────────────────────────────────────────────────────────────┐    │
│       │  ┌────────────────┐ ┌──────────────────┐ ┌──────────────┐     │    │
│       │  │ traceability-  │ │ cross-reference- │ │ spec-        │     │    │
│       │  │ validator      │ │ validator        │ │ reviewer     │     │    │
│       │  │ [haiku]        │ │ [haiku]          │ │ [sonnet]     │     │    │
│       │  └────────────────┘ └──────────────────┘ └──────────────┘     │    │
│       └────────────────────────────────────────────────────────────────┘    │
│       │                                                                     │
│       │  CP-8: JIRA EXPORT                                                  │
│       └─────────────────────────────────────────────────────────────────▶   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### ProductSpecs Agents

| Agent ID | Name | Model | Purpose |
|----------|------|-------|---------|
| `productspecs-orchestrator` | ProductSpecs Orchestrator | sonnet | Pipeline coordination |
| `productspecs-ui-module-specifier` | UI Module Specifier | sonnet | UI/Screen module specs |
| `productspecs-api-module-specifier` | API Module Specifier | sonnet | API/Backend module specs |
| `productspecs-nfr-generator` | NFR Generator | sonnet | Non-functional requirements |
| `productspecs-unit-test-specifier` | Unit Test Specifier | sonnet | Unit test specifications |
| `productspecs-integration-test-specifier` | Integration Test Specifier | sonnet | Integration test specs |
| `productspecs-e2e-test-specifier` | E2E Test Specifier | sonnet | E2E test specifications |
| `productspecs-pict-combinatorial` | PICT Combinatorial | haiku | Pairwise test generation |
| `productspecs-traceability-validator` | Traceability Validator | haiku | PP→JTBD→REQ→MOD→TC chains |
| `productspecs-cross-reference-validator` | Cross-Reference Validator | haiku | ID reference integrity |
| `productspecs-spec-reviewer` | Spec Reviewer | sonnet | Completeness and quality |

### ProductSpecs Traceability IDs

| Type | Format | Example |
|------|--------|---------|
| Module | MOD-{APP}-{FEAT}-NN | MOD-DSK-INV-01 |
| NFR | NFR-{CAT}-NN | NFR-PERF-01 |
| Test Case | TC-{TYPE}-NNN | TC-UNIT-001 |
| JIRA Item | INV-NNN | INV-001 |

---

## Stage 4: SolArch (17 Agents)

Generates arc42-compliant architecture documentation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SOLARCH AGENT FLOW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ORCHESTRATOR ─────────────────────────────────────────────────────────────▶│
│       │                                                                     │
│       │  CP-1: VALIDATE INPUTS [BLOCKING]                                   │
│       │  CP-2: CONTEXT & CONSTRAINTS                                        │
│       │                                                                     │
│       │  CP-3: PARALLEL RESEARCH                                            │
│       ├────────────────────────────────────────────────────────────────┐    │
│       │  ┌────────────────┐ ┌─────────────────┐ ┌──────────────┐      │    │
│       │  │ tech-          │ │ integration-    │ │ cost-        │      │    │
│       │  │ researcher     │ │ analyst         │ │ estimator    │      │    │
│       │  │ [sonnet]       │ │ [sonnet]        │ │ [haiku]      │      │    │
│       │  └────────────────┘ └─────────────────┘ └──────────────┘      │    │
│       └────────────────────────────────────────────────────────────────┘    │
│       │                                                                     │
│       │  CP-4: SEQUENTIAL C4 DIAGRAMS                                       │
│       ├──────────────────────────────────────────────────────────────┐      │
│       │  ┌──────────┐ ┌──────────┐ ┌──────────┐                     │      │
│       │  │c4-context│▶│c4-contain│▶│c4-compont│                     │      │
│       │  │[haiku]   │ │[haiku]   │ │[haiku]   │                     │      │
│       │  └──────────┘ └──────────┘ └──────────┘                     │      │
│       └──────────────────────────────────────────────────────────────┘      │
│       │                                                                     │
│       │  CP-6: PARALLEL QUALITY SCENARIOS                                   │
│       ├────────────────────────────────────────────────────────────────┐    │
│       │  ┌────────────┐ ┌────────────┐ ┌─────────────┐ ┌────────────┐ │    │
│       │  │ perf-      │ │ security-  │ │ reliability-│ │ usability- │ │    │
│       │  │ scenarios  │ │ scenarios  │ │ scenarios   │ │ scenarios  │ │    │
│       │  │ [haiku]    │ │ [haiku]    │ │ [haiku]     │ │ [haiku]    │ │    │
│       │  └────────────┘ └────────────┘ └─────────────┘ └────────────┘ │    │
│       └────────────────────────────────────────────────────────────────┘    │
│       │                                                                     │
│       │  CP-8: ADR WRITING                                                  │
│       ├──────────────────────────────────────────────────────────────┐      │
│       │  ┌────────────────┐                                          │      │
│       │  │ adr-foundation │  ADR-001 to ADR-004                      │      │
│       │  │ [sonnet]       │                                          │      │
│       │  └────────────────┘                                          │      │
│       │          │                                                   │      │
│       │          ▼ PARALLEL                                          │      │
│       │  ┌─────────────────┐ ┌──────────────────┐                   │      │
│       │  │ adr-communication│ │ adr-operational  │                   │      │
│       │  │ ADR-005 to 008  │ │ ADR-009 to 012   │                   │      │
│       │  │ [sonnet]        │ │ [sonnet]         │                   │      │
│       │  └─────────────────┘ └──────────────────┘                   │      │
│       │          │                                                   │      │
│       │          ▼                                                   │      │
│       │  ┌────────────────┐                                          │      │
│       │  │ adr-validator  │  Consistency check                       │      │
│       │  │ [haiku]        │                                          │      │
│       │  └────────────────┘                                          │      │
│       └──────────────────────────────────────────────────────────────┘      │
│       │                                                                     │
│       │  CP-9: EVALUATION                                                   │
│       ├──────────────────────────────────────────────────────────────┐      │
│       │  ┌────────────────┐ ┌────────────────┐                      │      │
│       │  │ arch-evaluator │▶│ risk-scorer    │                      │      │
│       │  │ [sonnet] ATAM  │ │ [haiku]        │                      │      │
│       │  └────────────────┘ └────────────────┘                      │      │
│       └──────────────────────────────────────────────────────────────┘      │
│       │                                                                     │
│       │  CP-11: TRACEABILITY VALIDATION [BLOCKING]                          │
│       │        100% pain point & requirement coverage                       │
│       │                                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### SolArch Agents

| Agent ID | Name | Model | Purpose |
|----------|------|-------|---------|
| `solarch-orchestrator` | SolArch Orchestrator | sonnet | Master coordinator, 13 checkpoints |
| `solarch-tech-researcher` | Technology Researcher | sonnet | Tech evaluation, vendor comparison |
| `solarch-integration-analyst` | Integration Analyst | sonnet | Integration patterns, data flows |
| `solarch-cost-estimator` | Cost Estimator | haiku | TCO analysis, infrastructure cost |
| `solarch-c4-context-generator` | C4 Context Generator | haiku | System boundary, external actors |
| `solarch-c4-container-generator` | C4 Container Generator | haiku | Container identification, tech mapping |
| `solarch-c4-component-generator` | C4 Component Generator | haiku | Component decomposition |
| `solarch-c4-deployment-generator` | C4 Deployment Generator | haiku | Infrastructure mapping, scaling |
| `solarch-performance-scenarios` | Performance Scenarios | haiku | Response time, throughput |
| `solarch-security-scenarios` | Security Scenarios | haiku | STRIDE threat modeling |
| `solarch-reliability-scenarios` | Reliability Scenarios | haiku | Availability, fault tolerance |
| `solarch-usability-scenarios` | Usability Scenarios | haiku | WCAG, UX scenarios |
| `solarch-adr-foundation-writer` | ADR Foundation Writer | sonnet | ADR-001 to ADR-004 |
| `solarch-adr-communication-writer` | ADR Communication Writer | sonnet | ADR-005 to ADR-008 |
| `solarch-adr-operational-writer` | ADR Operational Writer | sonnet | ADR-009 to ADR-012 |
| `solarch-adr-validator` | ADR Validator | haiku | Consistency, coverage |
| `solarch-arch-evaluator` | Architecture Evaluator | sonnet | ATAM analysis, tradeoffs |
| `solarch-risk-scorer` | Risk Scorer | haiku | Risk quantification, mitigation |

### SolArch Traceability IDs

| Type | Format | Example |
|------|--------|---------|
| ADR | ADR-NNN | ADR-001 |
| Component | COMP-{CAT}-NN | COMP-API-01 |
| Quality Scenario | QS-{CAT}-NN | QS-PERF-01 |
| Risk | RISK-{CAT}-NN | RISK-TECH-01 |

---

## Stage 5: Implementation (20+ Agents)

Executes TDD implementation with multi-agent code review.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        IMPLEMENTATION AGENT LAYERS                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      PLANNING LAYER                                 │    │
│  │  ┌────────────┐ ┌────────┐                                          │    │
│  │  │ tech-lead  │ │explorer│  [research agents archived]              │    │
│  │  │ [sonnet]   │ │[sonnet]│                                          │    │
│  │  └────────────┘ └────────┘                                          │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                   IMPLEMENTATION LAYER                              │    │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────────────┐  │    │
│  │  │developer-1 │ │developer-2 │ │developer-3 │ │test-automation   │  │    │
│  │  │ [sonnet]   │ │ [sonnet]   │ │ [sonnet]   │ │ [sonnet]         │  │    │
│  │  └────────────┘ └────────────┘ └────────────┘ └──────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                        │
│                                    ▼                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      QUALITY LAYER (Parallel)                       │    │
│  │  ┌──────────┐ ┌────────────┐ ┌────────────┐ ┌─────────┐ ┌────────┐  │    │
│  │  │bug-hunter│ │security-   │ │code-quality│ │test-cov │ │a11y    │  │    │
│  │  │ [sonnet] │ │auditor     │ │ [sonnet]   │ │[sonnet] │ │auditor │  │    │
│  │  └──────────┘ └────────────┘ └────────────┘ └─────────┘ └────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                        │
│  ══════════════════════════════════╪════════════════════════════════════    │
│                                    │  MONITORING (Continuous)               │
│  ┌─────────────────────────────────▼───────────────────────────────────┐    │
│  │                  PROCESS INTEGRITY LAYER                            │    │
│  │  ┌────────────────┐ ┌─────────────┐ ┌────────────┐ ┌─────────────┐  │    │
│  │  │ traceability-  │ │   state-    │ │checkpoint- │ │ playbook-   │  │    │
│  │  │   guardian     │ │  watchdog   │ │  auditor   │ │  enforcer   │  │    │
│  │  │ [haiku]        │ │ [haiku]     │ │ [haiku]    │ │ [sonnet]    │  │    │
│  │  └────────────────┘ └─────────────┘ └────────────┘ └─────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                        │
│  ┌─────────────────────────────────▼───────────────────────────────────┐    │
│  │                     REFLEXION LAYER                                 │    │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐                       │    │
│  │  │   actor    │ │ evaluator  │ │self-refiner│                       │    │
│  │  │ [sonnet]   │ │ [sonnet]   │ │ [sonnet]   │                       │    │
│  │  └────────────┘ └────────────┘ └────────────┘                       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Implementation Agent Summary

| Category | Agent ID | Purpose | Model | Coordination |
|----------|----------|---------|-------|--------------|
| **Planning** | `planning-tech-lead` | Task decomposition, sprint planning | sonnet | Sequential |
| | `planning-code-explorer` | Codebase analysis, pattern discovery | sonnet | Parallel |
| **Implementation** | `implementation-developer` | TDD implementation (RED-GREEN-REFACTOR) | sonnet | Parallel (×3) |
| | `implementation-test-automation-engineer` | E2E tests, Playwright setup | sonnet | Parallel |
| **Quality** | `quality-bug-hunter` | Logic errors, null safety, edge cases | sonnet | Parallel |
| | `quality-security-auditor` | OWASP Top 10, injection, auth | sonnet | Parallel |
| | `quality-code-quality` | SOLID, DRY, complexity | sonnet | Parallel |
| | `quality-test-coverage` | Missing tests, mock issues | sonnet | Parallel |
| | `quality-contracts-reviewer` | API contract compliance | sonnet | Parallel |
| | `quality-accessibility-auditor` | WCAG compliance | sonnet | Parallel |
| **Process Integrity** | `process-integrity-traceability-guardian` | Registry integrity, trace links | haiku | Continuous |
| | `process-integrity-state-watchdog` | Lock monitoring, session cleanup | haiku | Continuous |
| | `process-integrity-checkpoint-auditor` | Gate validation, artifact checks | haiku | On-transition |
| | `process-integrity-playbook-enforcer` | TDD compliance, pattern validation | sonnet | Per-task |
| **Traceability Audit** | `trace-audit-registry-scanner` | Scans traceability/ folder for broken links, orphans | sonnet | Parallel |
| | `trace-audit-state-analyzer` | Validates _state/ checkpoints, sessions, configs | sonnet | Parallel |
| | `trace-audit-json-discovery` | Discovers shadow registries in all .json files | sonnet | Parallel |
| | `trace-audit-consolidator` | Merges findings, generates visual matrix report | sonnet | Sequential |
| **Reflexion** | `reflexion-actor` | Initial implementation attempt | sonnet | Sequential |
| | `reflexion-evaluator` | Multi-perspective critique | sonnet | Sequential |
| | `reflexion-self-refiner` | Improvement iteration | sonnet | Sequential |

### Implementation Traceability IDs

| Type | Format | Example |
|------|--------|---------|
| Task | T-NNN | T-015 |
| Review Finding | RF-NNN | RF-001 |
| Change Request | CR-NNN | CR-001 |

---

## Archived Agents

Some agents have been archived as they are not used in all pipeline stages. See `.claude/agents/archived/README.md` for details.

**Archived**:
- `planning-product-researcher` - Used in Discovery/Prototype, not Implementation
- `planning-hfe-ux-researcher` - Used in Discovery/Prototype, not Implementation

---

## File Structure

All agent files are at the root level with stage prefixes:

```
.claude/agents/
├── README.md                                    # This file
├── archived/                                    # Archived agents (not used in all stages)
│   ├── README.md                                # Archive explanation
│   ├── planning-product-researcher.md           # Archived: Discovery/Prototype only
│   └── planning-hfe-ux-researcher.md            # Archived: Discovery/Prototype only
├── DISCOVERY_AGENT_REGISTRY.json               # Discovery agent registry
├── PROTOTYPE_AGENT_REGISTRY.json               # Prototype agent registry
├── PRODUCTSPECS_AGENT_REGISTRY.json            # ProductSpecs agent registry
├── SOLARCH_AGENT_REGISTRY.json                 # SolArch agent registry
│
├── discovery-orchestrator.md                   # Discovery orchestrator
├── discovery-interview-analyst.md              # Interview analysis
├── discovery-pdf-analyst.md                    # PDF deep analysis
├── discovery-data-analyst.md                   # Spreadsheet analysis
├── discovery-design-analyst.md                 # Design file analysis
├── discovery-pain-point-validator.md           # Pain point extraction
├── discovery-persona-generator.md              # Persona synthesis
├── discovery-jtbd-extractor.md                 # JTBD mapping
├── discovery-cross-reference-validator.md      # ID validation
├── discovery-fact-auditor-reviewer.md          # Fact audit
│
├── prototype-orchestrator.md                   # Prototype orchestrator
├── prototype-data-model-specifier.md           # Data model generation
├── prototype-api-contract-specifier.md         # API contract generation
├── prototype-design-token-generator.md         # Design tokens
├── prototype-component-specifier.md            # Component specs
├── prototype-screen-specifier.md               # Screen layouts
├── prototype-component-validator.md            # Component validation
├── prototype-screen-validator.md               # Screen validation
├── prototype-ux-validator.md                   # UX patterns
├── prototype-accessibility-auditor.md          # WCAG compliance
├── prototype-visual-qa-tester.md               # Screenshot regression
│
├── productspecs-orchestrator.md                # ProductSpecs orchestrator
├── productspecs-ui-module-specifier.md         # UI module specs
├── productspecs-api-module-specifier.md        # API module specs
├── productspecs-nfr-generator.md               # NFR generation
├── productspecs-unit-test-specifier.md         # Unit test specs
├── productspecs-integration-test-specifier.md  # Integration test specs
├── productspecs-e2e-test-specifier.md          # E2E test specs
├── productspecs-pict-combinatorial.md          # Pairwise testing
├── productspecs-traceability-validator.md      # Traceability validation
├── productspecs-cross-reference-validator.md   # Cross-reference validation
├── productspecs-spec-reviewer.md               # Spec review
│
├── solarch-orchestrator.md                     # SolArch orchestrator
├── solarch-tech-researcher.md                  # Tech evaluation
├── solarch-integration-analyst.md              # Integration patterns
├── solarch-cost-estimator.md                   # TCO analysis
├── solarch-c4-context-generator.md             # C4 Context diagram
├── solarch-c4-container-generator.md           # C4 Container diagram
├── solarch-c4-component-generator.md           # C4 Component diagram
├── solarch-c4-deployment-generator.md          # C4 Deployment diagram
├── solarch-performance-scenarios.md            # Performance scenarios
├── solarch-security-scenarios.md               # Security scenarios
├── solarch-reliability-scenarios.md            # Reliability scenarios
├── solarch-usability-scenarios.md              # Usability scenarios
├── solarch-adr-foundation-writer.md            # ADR 001-004
├── solarch-adr-communication-writer.md         # ADR 005-008
├── solarch-adr-operational-writer.md           # ADR 009-012
├── solarch-adr-validator.md                    # ADR consistency
├── solarch-arch-evaluator.md                   # ATAM analysis
├── solarch-risk-scorer.md                      # Risk quantification
│
├── planning-tech-lead.md                       # Tech lead
├── planning-code-explorer.md                   # Codebase analysis
│
├── implementation-developer.md                 # TDD developer
├── implementation-test-automation-engineer.md  # E2E test automation
│
├── quality-bug-hunter.md                       # Bug detection
├── quality-security-auditor.md                 # Security audit
├── quality-code-quality.md                     # Code quality
├── quality-test-coverage.md                    # Test coverage
├── quality-contracts-reviewer.md               # API contracts
├── quality-accessibility-auditor.md            # Accessibility
├── quality-cross-validator.md                  # Cross-validation
├── quality-spec-reviewer.md                    # Spec review
│
├── process-integrity-traceability-guardian.md  # Traceability monitoring
├── process-integrity-state-watchdog.md         # State monitoring
├── process-integrity-checkpoint-auditor.md     # Gate validation
├── process-integrity-playbook-enforcer.md      # TDD compliance
│
├── trace-audit-registry-scanner.md             # Traceability/ folder audit
├── trace-audit-state-analyzer.md               # _state/ folder audit
├── trace-audit-json-discovery.md               # Shadow registry discovery
├── trace-audit-consolidator.md                 # Audit findings consolidation
│
├── reflexion-actor.md                          # Initial implementation
├── reflexion-evaluator.md                      # Multi-perspective critique
└── reflexion-self-refiner.md                   # Improvement iteration
```

### Agent ID Convention

Agent IDs use hyphenated names matching the filename (without `.md`):

| Filename | Agent ID |
|----------|----------|
| `discovery-pdf-analyst.md` | `discovery-pdf-analyst` |
| `prototype-screen-specifier.md` | `prototype-screen-specifier` |
| `solarch-c4-context-generator.md` | `solarch-c4-context-generator` |

---

## Model Allocation Summary

### By Stage (Optimized)

| Stage | sonnet | haiku | Total | Notes |
|-------|--------|-------|-------|-------|
| Discovery | 6 | 3 | 9 | - |
| Prototype | 5 | 6 | 11 | Optimized: api-contract, design-token, validators use haiku |
| ProductSpecs | 8 | 3 | 11 | - |
| SolArch | 7 | 10 | 17 | - |
| Implementation | 15+ | 4 | 19+ | - |
| **Traceability Audit** | 4 | 0 | 4 | All sonnet for thorough analysis |

### Allocation Rationale

| Model | Use Case | Examples |
|-------|----------|----------|
| **sonnet** | Complex reasoning, code generation, orchestration | orchestrators, developers, ADR writers |
| **haiku** | Structured output, validation, templates | schema generation, validators, C4 diagrams |

### Token Optimization Applied

| Agent | Previous | Current | Rationale |
|-------|----------|---------|-----------|
| `prototype-api-contract-specifier` | sonnet | haiku | OpenAPI schema is templated |
| `prototype-design-token-generator` | sonnet | haiku | JSON token structure is templated |
| `prototype-accessibility-auditor` | sonnet | haiku | WCAG checklist-based |

---

## Coordination Mechanisms

### 1. File Locking

Execution agents acquire exclusive locks on files they modify:

```json
// _state/agent_lock.json
{
  "locks": [{
    "file_path": "src/components/Button.tsx",
    "agent_id": "developer-001",
    "task_id": "T-015",
    "acquired_at": "2025-01-15T10:30:00Z",
    "expires_at": "2025-01-15T10:45:00Z"
  }]
}
```

### 2. Session Management

All active agents are tracked in session registry:

```json
// _state/agent_sessions.json
{
  "active_sessions": [{
    "session_id": "sess-001",
    "agent_type": "developer",
    "agent_id": "developer-001",
    "current_task": "T-015",
    "status": "active"
  }]
}
```

### 3. Blocking Gates

Each stage has blocking checkpoints that must pass before proceeding:

| Stage | Blocking Checkpoints |
|-------|---------------------|
| Discovery | CP-11 (Validation) |
| Prototype | CP-1 (Discovery validation), CP-14 (UI audit) |
| ProductSpecs | CP-1 (Input validation), CP-7 (100% P0 coverage) |
| SolArch | CP-1 (Input validation), CP-11 (Traceability) |
| Implementation | CP-1 (Input validation), CP-6 (Code review), CP-9 (Final validation) |

---

## Agent Invocation

Agents are invoked via the Claude Code Task tool. Use `general-purpose` subagent_type and reference the agent `.md` file:

```javascript
// Example: Spawn stage orchestrator
Task({
  subagent_type: "general-purpose",  // Use native Claude Code agent type
  model: "sonnet",
  description: "Orchestrate Discovery analysis",
  prompt: `
    ## Agent: discovery-orchestrator
    Read instructions from: .claude/agents/discovery-orchestrator.md

    Execute complete Discovery analysis for Inventory System.

    INPUT PATH: InventorySystem/
    OUTPUT PATH: ClientAnalysis_InventorySystem/
    PRODUCT NAME: Inventory Management System

    EXECUTION MODE: full (checkpoints 0-11)
    PARALLEL EXECUTION: enabled
  `
})
```

### Parallel Invocation

For parallel execution, spawn multiple agents in a single message:

```javascript
// Spawn 3 developers in parallel using general-purpose with agent instructions
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "T-015: Create User model",
  prompt: `Agent: implementation-developer. Read .claude/agents/implementation-developer.md. Task: T-015 Create User model`
})
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "T-016: Create JWT utility",
  prompt: `Agent: implementation-developer. Read .claude/agents/implementation-developer.md. Task: T-016 Create JWT utility`
})
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "T-017: Create password hash",
  prompt: `Agent: implementation-developer. Read .claude/agents/implementation-developer.md. Task: T-017 Create password hash`
})
```

### Using Explore Agent for Analysis

For read-only analysis tasks, use the faster `Explore` agent:

```javascript
Task({
  subagent_type: "Explore",  // Fast exploration agent
  model: "haiku",            // Cheaper for analysis
  description: "Analyze interview transcripts",
  prompt: `
    Search InventorySystem/ for interview transcripts.
    Extract: User types, pain points, quotes with citations.
    Output: Structured JSON summary.
  `
})
```

---

## End-to-End Traceability Chain

```
CM-XXX (Client Material)
    ↓  Discovery
PP-X.X (Pain Point)
    ↓  Discovery
JTBD-X.X (Job To Be Done)
    ↓  Prototype
REQ-XXX (Requirement)
    ↓  Prototype
SCR-XXX (Screen)
    ↓  ProductSpecs
MOD-XXX (Module Spec)
    ↓  ProductSpecs
TC-XXX (Test Case)
    ↓  SolArch
ADR-XXX (Architecture Decision)
    ↓  SolArch
COMP-XXX (Component)
    ↓  Implementation
T-NNN (Task)
    ↓  Implementation
src/features/*.ts (Code)
```

---

## Related Files

- **Architecture**: `architecture/Subagent_Architecture.md`
- **Parallel Coordination**: `architecture/Parallel_Agent_Coordination.md`
- **Hooks**: `.claude/hooks/agent_coordinator.py`
- **Rules**: `.claude/rules/agent-coordination.md`
- **Commands**: See stage-specific command references in `.claude/commands/`

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-27 | Initial multi-agent architecture (Implementation only) |
| 2.0.0 | 2025-12-27 | Complete 5-stage documentation with all agent registries |
| 2.1.0 | 2026-01-08 | Unified naming convention (colon→hyphen), optimized model allocation, native Task tool patterns |
