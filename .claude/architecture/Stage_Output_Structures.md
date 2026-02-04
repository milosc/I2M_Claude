# Stage Output Structures

**Version**: 1.0.0
**Created**: 2025-01-08
**Status**: Reference Document

This document defines the folder structures and output artifacts for all five HTEC framework stages.

---

## Shared Folders Architecture

The `_state/` and `traceability/` folders are **SHARED** between all stages and live at the **PROJECT ROOT** level:

```
project_root/
├── _state/                           <- SHARED (ROOT LEVEL)
│   ├── discovery_config.json         <- Discovery stage
│   ├── discovery_progress.json       <- Discovery stage
│   ├── discovery_summary.json        <- Prototype stage
│   ├── prototype_config.json         <- Prototype stage
│   ├── prototype_progress.json       <- Prototype stage
│   ├── productspecs_config.json      <- ProductSpecs stage
│   ├── productspecs_progress.json    <- ProductSpecs stage
│   ├── solarch_config.json           <- SolArch stage
│   ├── solarch_progress.json         <- SolArch stage
│   ├── implementation_config.json    <- Implementation stage
│   ├── implementation_progress.json  <- Implementation stage
│   └── FAILURES_LOG.md               <- Error log
├── traceability/                     <- SHARED (ROOT LEVEL) - MANDATORY
│   ├── discovery_traceability_register.json   <- Created by Discovery
│   ├── prototype_traceability_register.json   <- Created by Prototype
│   ├── productspecs_traceability_register.json <- Created by ProductSpecs (CP7)
│   ├── solarch_traceability_register.json     <- Created by SolArch (CP11)
│   ├── implementation_traceability_register.json <- Created by Implementation
│   ├── screen_registry.json                   <- Master screen tracking
│   ├── requirements_registry.json             <- Requirements
│   ├── task_registry.json                     <- Implementation tasks
│   └── review_registry.json                   <- Code review findings
├── ClientAnalysis_<SystemName>/      <- Discovery outputs
├── Prototype_<SystemName>/           <- Prototype outputs
├── ProductSpecs_<SystemName>/        <- ProductSpecs outputs
├── SolArch_<SystemName>/             <- SolArch outputs
└── Implementation_<SystemName>/      <- Implementation outputs
```

### Path Resolution Rules

- Paths starting with `_state/` -> ROOT-level shared folder
- Paths starting with `traceability/` -> ROOT-level shared folder
- All other paths -> relative to the specific phase folder

### ROOT-LEVEL TRACEABILITY ENFORCEMENT

Each stage MUST create its ROOT-level traceability file. Quality gates enforce this:
- **ProductSpecs CP7** validates `traceability/productspecs_traceability_register.json`
- **SolArch CP11** validates `traceability/solarch_traceability_register.json`

Failure to create these files will cause checkpoint validation to FAIL.

---

## Stage 1: Discovery Output Structure

```
ClientAnalysis_<SystemName>/
├── 00-management/
│   ├── PROGRESS_TRACKER.md
│   └── FAILURES_LOG.md
├── 01-analysis/
│   ├── [PDF_Name]_Analysis/           # One folder per PDF
│   │   ├── SYSTEM_KNOWLEDGE.md
│   │   ├── TERMINOLOGY.md
│   │   ├── GAP_ANALYSIS.md
│   │   └── SECTION_INDEX.md
│   ├── PDF_ANALYSIS_INDEX.md
│   ├── PDF_FINDINGS_SUMMARY.md
│   ├── ANALYSIS_SUMMARY.md
│   └── PAIN_POINTS.md
├── 02-research/
│   ├── personas/                      # SEPARATE persona files
│   │   ├── PERSONA_WAREHOUSE_OPERATOR.md
│   │   ├── PERSONA_WAREHOUSE_SUPERVISOR.md
│   │   └── PERSONA_[ROLE].md
│   └── JOBS_TO_BE_DONE.md
├── 03-strategy/
│   ├── PRODUCT_VISION.md
│   ├── PRODUCT_STRATEGY.md
│   ├── COMPETITIVE_LANDSCAPE.md          # CP-6.5: Market map with competitor categorization
│   ├── THREAT_OPPORTUNITY_MATRIX.md      # CP-6.5: Quantitative threat/opportunity analysis
│   ├── DIFFERENTIATION_BLUEPRINT.md      # CP-6.5: USP definition and positioning
│   ├── COMPETITIVE_INTELLIGENCE_SUMMARY.md # CP-6.5: Executive summary
│   ├── battlecards/                      # CP-6.5: Per-competitor sales enablement
│   │   └── [COMPETITOR]_BATTLECARD.md
│   ├── PRODUCT_ROADMAP.md
│   └── KPIS_AND_GOALS.md
├── 04-design-specs/
│   ├── screen-definitions.md          # lowercase with dashes
│   ├── navigation-structure.md
│   ├── data-fields.md
│   └── interaction-patterns.md
└── 05-documentation/
    ├── INDEX.md
    ├── README.md
    └── VALIDATION_REPORT.md
```

### Discovery File Naming Conventions

| Category | Convention | Examples |
|----------|------------|----------|
| Analysis, Research, Strategy | UPPERCASE with underscores | `ANALYSIS_SUMMARY.md`, `PERSONA_WAREHOUSE_OPERATOR.md`, `PRODUCT_VISION.md` |
| Design Specs | lowercase with dashes | `screen-definitions.md`, `navigation-structure.md` |
| Personas | Separate files in `personas/` subfolder | `PERSONA_[ROLE_NAME].md` |

### Discovery Feedback Sessions

```
traceability/feedback_sessions/discovery/<YYYY-MM-DD>_Feedback_<NNN>/
├── FEEDBACK_ORIGINAL.md
├── IMPACT_ANALYSIS.md
├── IMPLEMENTATION_PLAN.md
├── IMPLEMENTATION_LOG.md
├── VALIDATION_REPORT.md
└── FEEDBACK_SUMMARY.md
```

---

## Stage 2: Prototype Output Structure

```
Prototype_<SystemName>/
├── 00-foundation/                    # Design foundations
│   ├── design-brief.md
│   ├── design-tokens.json
│   ├── color-system.md
│   ├── typography.md
│   └── spacing-layout.md
├── 01-components/                    # Component specifications
│   ├── component-index.md
│   ├── primitives/
│   ├── data-display/
│   ├── feedback/
│   ├── navigation/
│   ├── overlays/
│   └── patterns/
├── 02-screens/                       # Screen specifications
│   ├── screen-index.md
│   └── [screen-name]/
├── 03-interactions/                  # Motion & accessibility
│   ├── motion-system.md
│   ├── accessibility-spec.md
│   └── responsive-behavior.md
├── 04-implementation/                # Build artifacts
│   ├── data-model.md
│   ├── api-contracts.json
│   ├── build-sequence.md
│   └── test-data/
├── 05-validation/                    # QA artifacts
│   ├── qa-report.md
│   ├── ui-audit-report.md
│   └── screenshots/
├── 06-change-requests/               # Feedback sessions
│   └── [YYYY-MM-DD]_CR_<NNN>/
├── prototype/                        # Working code
│   ├── src/
│   ├── public/
│   └── package.json
└── reports/                          # Summary reports
    ├── ARCHITECTURE.md
    ├── README.md
    └── TRACEABILITY_MATRIX.md
```

### Prototype Feedback Sessions

```
Prototype_<SystemName>/feedback-sessions/
├── prototype_feedback_registry.json      # Central registry
└── <YYYY-MM-DD>_PrototypeFeedback-<ID>/  # Per-feedback folder
    ├── FEEDBACK_ORIGINAL.md              # Original feedback content
    ├── impact_analysis.md                # Impact analysis results
    ├── implementation_options.md         # Generated options (A/B/C)
    ├── implementation_plan.md            # Selected/approved plan
    ├── implementation_log.md             # Step-by-step execution log
    ├── files_changed.md                  # Summary of all changes
    ├── VALIDATION_REPORT.md              # Validation results
    └── FEEDBACK_SUMMARY.md               # Final summary with timeline
```

---

## Stage 3: ProductSpecs Output Structure

```
ProductSpecs_<SystemName>/
├── 00-overview/
│   ├── MASTER_DEVELOPMENT_PLAN.md
│   ├── GENERATION_SUMMARY.md
│   ├── TRACEABILITY_MATRIX.md
│   └── VALIDATION_REPORT.md
├── 01-modules/
│   ├── module-index.md
│   └── MOD-<APP>-<FEAT>-<NN>.md
├── 02-api/
│   ├── api-index.md
│   ├── NFR_SPECIFICATIONS.md
│   └── data-contracts.md
├── 03-tests/
│   ├── test-case-registry.md
│   ├── e2e-scenarios.md
│   └── accessibility-checklist.md
├── 04-jira/
│   ├── jira_config.json
│   ├── IMPORT_GUIDE.md
│   ├── full-hierarchy.csv
│   ├── epics-and-stories.csv
│   ├── subtasks-only.csv
│   └── jira-import.json
└── feedback-sessions/
    └── productspecs_feedback_registry.json
```

**Note (v3.0)**: `_registry/` folder is DEPRECATED - registries now at ROOT `traceability/`:
- `modules.json` -> `traceability/module_registry.json`
- `requirements.json` -> `traceability/requirements_registry.json`
- `nfrs.json` -> `traceability/nfr_registry.json`
- `test-cases.json` -> `traceability/test_case_registry.json`

---

## Stage 4: SolArch Output Structure

```
SolArch_<SystemName>/
├── 01-introduction-goals/
│   ├── introduction.md
│   └── stakeholders.md
├── 02-constraints/
│   ├── business-constraints.md
│   ├── technical-constraints.md
│   └── regulatory-constraints.md
├── 03-context-scope/
│   ├── business-context.md
│   └── technical-context.md
├── 04-solution-strategy/
│   └── solution-strategy.md
├── 05-building-blocks/
│   ├── overview.md
│   ├── cross-cutting.md
│   ├── data-model/
│   └── modules/<module-slug>/
├── 06-runtime/
│   ├── api-design.md
│   ├── event-communication.md
│   └── security-architecture.md
├── 07-quality/
│   ├── quality-requirements.md
│   └── testing-strategy.md
├── 08-deployment/
│   ├── deployment-view.md
│   ├── operations-guide.md
│   └── runbooks/
├── 09-decisions/
│   ├── ADR-001-architecture-style.md
│   ├── ADR-002-technology-stack.md
│   └── ... (min 9 ADRs)
├── 10-risks/
│   └── risks-technical-debt.md
├── 11-glossary/
│   └── glossary.md
├── reports/
│   ├── VALIDATION_REPORT.md
│   └── GENERATION_SUMMARY.md
├── diagrams/
│   ├── c4-context.mermaid
│   ├── c4-container.mermaid
│   └── c4-deployment.mermaid
└── feedback-sessions/
    └── solarch_feedback_registry.json
```

**Note (v3.0)**: `_registry/` folder is DEPRECATED - registries now at ROOT `traceability/`:
- `components.json` -> `traceability/component_registry.json`
- `decisions.json` -> `traceability/adr_registry.json`
- `architecture-traceability.json` -> `traceability/traceability_matrix_master.json`

### arc42 Section Mapping

| arc42 Section | Folder | Checkpoint |
|---------------|--------|------------|
| 1. Introduction & Goals | `01-introduction-goals/` | 2 |
| 2. Constraints | `02-constraints/` | 2 |
| 3. Context & Scope | `03-context-scope/` | 2 |
| 4. Solution Strategy | `04-solution-strategy/` | 3 |
| 5. Building Block View | `05-building-blocks/` | 4 |
| 6. Runtime View | `06-runtime/` | 5 |
| 7. Deployment View | `08-deployment/` | 7 |
| 8. Cross-cutting Concepts | `05-building-blocks/cross-cutting.md` | 6 |
| 9. Architecture Decisions | `09-decisions/` | 8 |
| 10. Quality Requirements | `07-quality/` | 6 |
| 11. Risks & Technical Debt | `10-risks/` | 9 |
| 12. Glossary | `11-glossary/` | 10 |

### C4 Diagram Outputs

| Diagram | Location | Generated By |
|---------|----------|--------------|
| Context | `diagrams/c4-context.mermaid` | `/solarch-blocks` |
| Container | `diagrams/c4-container.mermaid` | `/solarch-blocks` |
| Component | `modules/<mod>/c4-component.mermaid` | `/solarch-blocks` |
| Deployment | `diagrams/c4-deployment.mermaid` | `/solarch-deploy` |

---

## Stage 5: Implementation Output Structure

```
Implementation_<SystemName>/
├── src/                             # Source code
│   ├── components/
│   ├── features/
│   ├── services/
│   ├── hooks/
│   ├── utils/
│   └── types/
├── tests/                           # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── tasks/                           # Task specifications
│   ├── TASK_INDEX.md
│   └── T-NNN.md
├── docs/                            # Documentation
│   ├── API_DOCUMENTATION.md
│   ├── COMPONENT_LIBRARY.md
│   └── DEPLOYMENT_GUIDE.md
├── reports/                         # Reports
│   ├── CODE_REVIEW.md
│   ├── INTEGRATION_REPORT.md
│   ├── VALIDATION_REPORT.md
│   └── IMPLEMENTATION_SUMMARY.md
├── change-requests/                 # Change request sessions
│   ├── change_request_registry.json
│   └── <YYYY-MM-DD>_CR-<NNN>/
│       ├── CHANGE_REQUEST.md
│       ├── ANALYSIS.md
│       ├── IMPLEMENTATION_PLAN.md
│       ├── IMPLEMENTATION_LOG.md
│       ├── REFLECTION.md
│       └── SUMMARY.md
└── README.md
```

---

## Related Documentation

- **Quality Gates**: `architecture/Quality_Gates_Reference.md`
- **Traceability System**: `architecture/Traceability_System.md`
- **Change Request Process**: `architecture/ChangeRequest_Process.md`
- **Version Management**: `architecture/Version_and_Traceability_Management.md`
