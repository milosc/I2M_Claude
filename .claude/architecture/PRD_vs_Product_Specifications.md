# PRD vs Product Specifications in HTEC Framework

**Version**: 1.0.0
**Created**: 2026-01-27
**Status**: Reference Document

---

## Overview

This document clarifies the distinction between **Product Requirements Documents (PRDs)** and **Product Specifications (ProductSpecs)** within the HTEC framework, and explains the architectural parallel with **ADRs vs Solution Architecture Spec**.

---

## Key Distinction

### PRD (Product Requirements Document)
- **Perspective**: Business and product management
- **Audience**: Stakeholders, product managers, business analysts
- **Purpose**: Define WHAT to build and WHY
- **Focus**: User needs, business value, market fit
- **Language**: Business-oriented, user-centric
- **Outcome**: Product definition and prioritization

### Product Specifications (ProductSpecs)
- **Perspective**: Engineering and implementation
- **Audience**: Developers, technical architects, QA engineers
- **Purpose**: Define HOW to build it
- **Focus**: Technical implementation, acceptance criteria, test cases
- **Language**: Technical, implementation-ready
- **Outcome**: JIRA-ready stories, technical specs, test plans

---

## Architectural Parallel

The relationship between PRD and ProductSpecs mirrors the relationship between ADRs and Solution Architecture Spec:

| Concept | Individual Unit | Comprehensive Document |
|---------|----------------|------------------------|
| **Requirements** | User Story / Requirement (REQ-XXX) | **PRD** (Product Requirements Document) |
| **Specifications** | Module Spec (MOD-XXX-XXX-NN) | **ProductSpecs** (Product Specifications) |
| **Architecture** | ADR (Architecture Decision Record) | **SolArch** (Solution Architecture Spec) |

### Pattern Recognition

```
Individual Decision → Comprehensive Document
─────────────────────────────────────────────
User Story (REQ-XXX) → PRD
Module Spec (MOD-XXX) → ProductSpecs
ADR (ADR-XXX) → SolArch (arc42 document)
```

**Analogy**:
- **ADRs** are individual decisions → **SolArch** is the complete architecture
- **Requirements** are individual needs → **PRD** is the complete product definition
- **Module Specs** are individual implementations → **ProductSpecs** is the complete technical specification

---

## Where These Artifacts Live in HTEC Framework

### PRD Components (Stages 1-2)

#### Stage 1: Discovery - Strategic PRD Content
**Location**: `ClientAnalysis_<SystemName>/`

| File | PRD Section Equivalent | Audience |
|------|------------------------|----------|
| `PRODUCT_VISION.md` | Vision Statement | Executives, stakeholders |
| `PRODUCT_STRATEGY.md` | Market Analysis, Go-to-Market | Product leadership |
| `PRODUCT_ROADMAP.md` | Roadmap, Milestones | Stakeholders, investors |
| `KPIS_AND_GOALS.md` | Success Metrics | Business analysts |
| `personas/*.md` | User Personas | UX, product team |
| `JOBS_TO_BE_DONE.md` | User Needs | Product managers |
| `PAIN_POINTS.md` | Problem Statement | Stakeholders |
| `screen-definitions.md` | User Flows (high-level) | UX designers |

**Think of Discovery as**: The Business PRD (Why and What)

---

#### Stage 2: Prototype - Functional PRD Content
**Location**: `Prototype_<SystemName>/00-foundation/`

| File | PRD Section Equivalent | Audience |
|------|------------------------|----------|
| `REQUIREMENTS.md` | Functional Requirements | Product team |
| `traceability/requirements_registry.json` | Requirements Database | PM, QA |
| `design-tokens.json` | Design System | Designers |
| `component-index.md` | UI Component Inventory | UX/UI team |
| `screen-index.md` | User Flows (detailed) | Product designers |

**Think of Prototype as**: The Functional PRD (What exactly)

---

### Product Specifications (Stage 3)

#### Stage 3: ProductSpecs - Technical Implementation Specs
**Location**: `ProductSpecs_<SystemName>/`

| File | Purpose | Audience |
|------|---------|----------|
| **`MASTER_DEVELOPMENT_PLAN.md`** | Complete development roadmap | Tech leads |
| `01-modules/MOD-*.md` | Module-level specifications | Developers |
| `02-api/data-contracts.md` | API contracts | Backend devs |
| `02-api/NFR_SPECIFICATIONS.md` | Non-functional requirements | Architects |
| `03-tests/test-case-registry.md` | Test specifications | QA engineers |
| `04-jira/*.csv` | JIRA import files | Project managers |
| `TRACEABILITY_MATRIX.md` | Requirement → Implementation mapping | QA, PM |

**Think of ProductSpecs as**: The Technical Implementation Specification (How to build)

---

### Solution Architecture (Stage 4)

#### Stage 4: SolArch - Complete Architecture Document
**Location**: `SolArch_<SystemName>/`

| File | Purpose | Equivalent |
|------|---------|------------|
| `09-decisions/ADR-*.md` | Individual architecture decisions | Individual ADR |
| **arc42 complete document** | Comprehensive architecture | SolArch Spec |
| `05-building-blocks/` | System components | Architecture overview |
| `06-runtime/` | Runtime behavior | Runtime view |
| `07-quality/` | Quality scenarios | Quality requirements |

**Think of SolArch as**: The Complete Architecture (integrates all ADRs)

---

## Complete Requirements Flow

```
Stage 1: Discovery (Business PRD)
├── PRODUCT_VISION.md          ─┐
├── PRODUCT_STRATEGY.md         │
├── PRODUCT_ROADMAP.md          │─→ Strategic "Why" and "What"
├── KPIS_AND_GOALS.md           │
├── personas/*.md               │
├── JOBS_TO_BE_DONE.md          │
└── PAIN_POINTS.md             ─┘
        ↓
Stage 2: Prototype (Functional PRD)
├── REQUIREMENTS.md            ─┐
├── requirements_registry.json  │─→ Functional "What exactly"
├── screen-index.md             │
└── component-index.md         ─┘
        ↓
Stage 3: ProductSpecs (Technical Specs)
├── MASTER_DEVELOPMENT_PLAN.md ─┐
├── 01-modules/MOD-*.md         │
├── 02-api/data-contracts.md    │─→ Technical "How to build"
├── 03-tests/*.md               │
└── TRACEABILITY_MATRIX.md     ─┘
        ↓
Stage 4: SolArch (Architecture)
├── 09-decisions/ADR-*.md      ─┐
├── 05-building-blocks/         │─→ Architectural "How it works"
├── 06-runtime/                 │
└── 07-quality/                ─┘
        ↓
Stage 5: Implementation (Code)
└── Actual implementation       ─→ Working software
```

---

## Comparison Tables

### PRD vs ProductSpecs

| Aspect | PRD | ProductSpecs |
|--------|-----|--------------|
| **Stage** | Discovery (1) + Prototype (2) | ProductSpecs (3) |
| **Perspective** | Business, product, user | Technical, implementation |
| **Audience** | Stakeholders, executives, PM | Developers, architects, QA |
| **Language** | Business terms, user stories | Technical specs, acceptance criteria |
| **Focus** | Why and What | How and When |
| **Traceability** | Pain Points → JTBD → Requirements | Requirements → Modules → Tests |
| **Deliverable** | Product definition | JIRA-ready stories |
| **Approval** | Product leadership | Tech leadership |
| **Change frequency** | Low (strategic) | Medium (tactical) |
| **Granularity** | High-level (features) | Detailed (modules, APIs) |

---

### ADRs vs SolArch Spec

| Aspect | ADRs | SolArch Spec |
|--------|------|--------------|
| **Stage** | SolArch (4) | SolArch (4) |
| **Scope** | Individual decision | Complete architecture |
| **Format** | Markdown (ADR-NNN.md) | arc42 multi-section document |
| **Perspective** | Single decision rationale | Comprehensive system view |
| **Audience** | Technical team (decision context) | All stakeholders (full picture) |
| **Focus** | Why we chose X over Y | How the entire system works |
| **Traceability** | NFRs → ADRs | Requirements → Architecture → Code |
| **Deliverable** | Decision record | Architecture document |
| **Approval** | Tech lead, architect | All stakeholders |
| **Change frequency** | Low (decisions locked) | Low (architecture stable) |
| **Granularity** | Fine (one decision) | Coarse (entire system) |

---

## Traditional PRD Mapping to HTEC Framework

If you're used to traditional PRDs with these sections, here's where each section lives:

| Traditional PRD Section | HTEC Framework Location | Stage | File |
|-------------------------|-------------------------|-------|------|
| **1. Executive Summary** | Discovery | 1 | `PRODUCT_VISION.md` |
| **2. Product Overview** | Discovery | 1 | `PRODUCT_VISION.md` |
| **3. Market Analysis** | Discovery | 1 | `PRODUCT_STRATEGY.md` |
| **4. User Personas** | Discovery | 1 | `02-research/personas/*.md` |
| **5. User Needs / Jobs** | Discovery | 1 | `JOBS_TO_BE_DONE.md` |
| **6. Pain Points** | Discovery | 1 | `PAIN_POINTS.md` |
| **7. Product Goals** | Discovery | 1 | `KPIS_AND_GOALS.md` |
| **8. Success Metrics** | Discovery | 1 | `KPIS_AND_GOALS.md` |
| **9. Roadmap** | Discovery | 1 | `PRODUCT_ROADMAP.md` |
| **10. Feature List** | Prototype | 2 | `REQUIREMENTS.md` |
| **11. User Stories** | Prototype | 2 | `requirements_registry.json` |
| **12. Functional Requirements** | Prototype | 2 | `REQUIREMENTS.md` |
| **13. Non-Functional Requirements** | ProductSpecs | 3 | `02-api/NFR_SPECIFICATIONS.md` |
| **14. User Flows** | Prototype | 2 | `screen-index.md` |
| **15. Wireframes** | Prototype | 2 | `02-screens/*/wireframe.md` |
| **16. Design System** | Prototype | 2 | `00-foundation/design-tokens.json` |
| **17. Acceptance Criteria** | ProductSpecs | 3 | `01-modules/MOD-*.md` |
| **18. Test Cases** | ProductSpecs | 3 | `03-tests/test-case-registry.md` |
| **19. API Specifications** | ProductSpecs | 3 | `02-api/data-contracts.md` |
| **20. Dependencies** | SolArch | 4 | `09-decisions/ADR-*.md` |

---

## When to Use What

### Use PRD Outputs (Discovery + Prototype) When:
- Presenting to executives or stakeholders
- Getting product approval
- Defining market strategy
- Prioritizing features
- Validating user needs
- Securing funding or resources

### Use ProductSpecs Outputs When:
- Starting development sprints
- Creating JIRA tickets
- Writing test cases
- Defining acceptance criteria
- Planning sprint capacity
- Conducting technical reviews

### Use SolArch Outputs When:
- Making technical decisions
- Designing system architecture
- Evaluating technology options
- Planning infrastructure
- Assessing technical risks
- Conducting architecture reviews

---

## Document Generation Commands

### Generate PRD Content

```bash
# Stage 1: Discovery (Business PRD)
/discovery <SystemName> <ClientMaterialsPath>

# Outputs: PRODUCT_VISION.md, PRODUCT_STRATEGY.md, PRODUCT_ROADMAP.md, etc.
# Location: ClientAnalysis_<SystemName>/
```

```bash
# Stage 2: Prototype (Functional PRD)
/prototype <SystemName>

# Outputs: REQUIREMENTS.md, requirements_registry.json, screen-index.md
# Location: Prototype_<SystemName>/00-foundation/
```

### Generate Product Specifications

```bash
# Stage 3: ProductSpecs (Technical Specs)
/productspecs <SystemName>

# Outputs: MASTER_DEVELOPMENT_PLAN.md, MOD-*.md, test cases, JIRA files
# Location: ProductSpecs_<SystemName>/
```

### Generate Solution Architecture

```bash
# Stage 4: SolArch (Architecture)
/solarch <SystemName>

# Outputs: ADR-*.md, arc42 sections, C4 diagrams
# Location: SolArch_<SystemName>/
```

---

## Presentation Format Recommendations

### For PRD Content
- **Format**: PowerPoint (PPTX) or Slidev
- **Audience**: Executives, stakeholders, product team
- **Focus**: Vision, strategy, roadmap, user needs

```bash
/presentation-slidev
# Source: ClientAnalysis_<SystemName>/ + Prototype_<SystemName>/
# Audience: C-level executives and stakeholders
# Detail Level: Executive Summary (10-15 slides)
```

### For ProductSpecs Content
- **Format**: Slidev (technical) or DOCX (documentation)
- **Audience**: Developers, QA engineers, tech leads
- **Focus**: Module specs, test cases, acceptance criteria

```bash
/presentation-slidev
# Source: ProductSpecs_<SystemName>/
# Audience: Development team and technical architects
# Detail Level: Detailed Deep-Dive (40-50 slides)
```

### For SolArch Content
- **Format**: Slidev (architecture deep-dive)
- **Audience**: Technical architects, senior developers
- **Focus**: ADRs, C4 diagrams, quality scenarios

```bash
/presentation-slidev
# Source: SolArch_<SystemName>/
# Audience: Technical architects and senior developers
# Detail Level: Detailed Deep-Dive (40-50 slides)
# Diagrams: Both (Mermaid + PlantUML)
```

---

## Traceability Chains

### PRD → ProductSpecs → Implementation

```
Pain Point (PP-X.X)                    [Discovery - PRD]
    ↓
Job To Be Done (JTBD-X.X)              [Discovery - PRD]
    ↓
Requirement (REQ-XXX)                  [Prototype - PRD]
    ↓
Screen (SCR-XXX)                       [Prototype - PRD]
    ↓
Module Spec (MOD-XXX-XXX-NN)           [ProductSpecs - Technical Spec]
    ↓
Test Case (TC-XXX)                     [ProductSpecs - Technical Spec]
    ↓
Implementation Task (T-NNN)            [Implementation]
    ↓
Code + Tests                           [Implementation]
```

### NFR → ADR → Architecture

```
Non-Functional Requirement (NFR-XXX)   [ProductSpecs]
    ↓
Architecture Decision Record (ADR-XXX) [SolArch]
    ↓
Architecture Component                 [SolArch - arc42]
    ↓
Implementation                         [Implementation]
```

---

## Key Insights

### 1. Progressive Refinement
The HTEC framework doesn't create a single monolithic PRD. Instead, it follows **progressive refinement**:
- **Discovery**: Strategic PRD (Why/What)
- **Prototype**: Functional PRD (What exactly)
- **ProductSpecs**: Technical Specs (How)

### 2. Separation of Concerns
Just as ADRs focus on individual decisions while SolArch provides the complete picture:
- **Requirements** focus on individual needs while **PRD** provides the complete product definition
- **Module Specs** focus on individual implementations while **ProductSpecs** provides the complete technical specification

### 3. Audience-Driven Documentation
Different stakeholders need different views:
- **Executives** → PRD (Discovery outputs)
- **Product Team** → PRD + Requirements (Discovery + Prototype)
- **Engineering** → ProductSpecs (ProductSpecs stage)
- **Architects** → SolArch (SolArch stage)

### 4. Traceability First
Every artifact traces back to business value:
- Pain Points → JTBD → Requirements → Modules → Code
- NFRs → ADRs → Architecture → Implementation

---

## Summary

| Concept | Scope | Location | Stage | Audience |
|---------|-------|----------|-------|----------|
| **PRD** | Complete product definition (Why/What) | Discovery + Prototype | 1-2 | Business/Product |
| **ProductSpecs** | Complete technical specification (How) | ProductSpecs | 3 | Engineering |
| **ADRs** | Individual architecture decisions | SolArch/09-decisions/ | 4 | Technical |
| **SolArch** | Complete architecture document | SolArch | 4 | All stakeholders |

**Parallel Pattern**:
```
Requirements → PRD           (as)   ADRs → SolArch
Individual → Complete        (as)   Individual → Complete
What → Why                   (as)   Decision → Architecture
```

---

## Related Documentation

- **Stage Output Structures**: `.claude/architecture/Stage_Output_Structures.md`
- **Quality Gates**: `.claude/architecture/Quality_Gates_Reference.md`
- **Traceability System**: `.claude/architecture/Traceability_System.md`
- **Discovery Command Reference**: `.claude/commands/DISCOVERY_COMMAND_REFERENCE.md`
- **Prototype Command Reference**: `.claude/commands/PROTOTYPE_COMMAND_REFERENCE.md`
- **ProductSpecs Command Reference**: `.claude/commands/PRODUCTSPECS_COMMAND_REFERENCE.md`
- **SolArch Command Reference**: `.claude/commands/SOLARCH_COMMAND_REFERENCE.md`

---

**Document Purpose**: This document clarifies the distinction between PRD (product requirements) and ProductSpecs (technical specifications), and explains the architectural parallel with ADRs vs SolArch within the HTEC framework.
