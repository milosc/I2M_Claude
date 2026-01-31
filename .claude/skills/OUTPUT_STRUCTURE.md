# Output Structure Specification

This document defines the folder structure, naming conventions, and organizational principles for prototype generation. All skills MUST follow this specification to ensure deterministic, consistent outputs **regardless of the specific solution being built**.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: Throughout this document, references to specific apps (e.g., `recruiter-app/`, `candidate-portal/`), entities (e.g., `Candidate.schema.json`), or file names (e.g., `candidate-pipeline.md`) are **examples only**. The actual structure should be derived from your project's discovery documents. Replace example names with your project's actual apps, entities, and screens.

---

## Core Principles

### 1. Lifecycle-Based Organization
Directories are numbered by prototype lifecycle phase:
- **00-** Foundation (must exist before building UI)
- **01-** Components (reusable building blocks)
- **02-** Screens (composed views)
- **03-** Interactions (behavior layer)
- **04-** Implementation (build guidance)
- **05-** Validation (verification)

### 2. Dual Representation
Every significant artifact has:
- **Machine-readable** (`.json`) → For tooling, automation, cross-referencing
- **Human-readable** (`.md`) → For review, documentation, communication

### 3. Summary + Detail Pattern
Each directory contains:
- **Summary file** at root → Overview, navigation, statistics
- **Subdirectories** → Detailed content organized by category
- **Index files** → Lookup tables, cross-references

### 4. Traceability
Every output connects to:
- Source requirements it addresses
- Upstream dependencies it consumes
- Downstream artifacts that consume it

---

## Root Structure

```
{project_root}/
│
├── _state/                      # Machine state and progress tracking
│   Purpose: Central hub for cross-skill communication and progress
│
├── _archive/                    # Superseded versions
│   Purpose: Version history, rollback capability
│
├── 00-foundation/               # Design system and data foundations
│   Purpose: Establish all foundations before UI work begins
│
├── 01-components/               # Component specifications
│   Purpose: Define reusable UI building blocks
│
├── 02-screens/                  # Screen specifications by app/role
│   Purpose: Define complete views composed from components
│
├── 03-interactions/             # Motion and accessibility
│   Purpose: Define behavior layer for components and screens
│
├── 04-implementation/           # Build sequence and prompts
│   Purpose: Guide code generation in optimal order
│
├── 05-validation/               # QA and verification
│   Purpose: Verify prototype meets requirements
│
├── docs/                        # Exported documentation
│   Purpose: Publishable documentation artifacts
│
├── prototype/                   # Runnable prototype (with build tools)
│   Purpose: Working application demonstrating specs
│
├── reports/                     # Audit and analysis reports
│   Purpose: Verification beyond automated testing
│
├── screenshots/                 # Visual captures
│   Purpose: Review artifacts, visual documentation
│
└── src/                         # Source code (alternative to prototype/)
    Purpose: Simpler setup without build tooling
```

---

## _state/ Directory

**Goal:** Enable any skill to understand current project state, find related artifacts, and update progress without re-reading all files.

```
_state/
│
├── discovery_summary.json       # Extracted data from discovery phase
│   Goal: Structured access to personas, pain points, entities, screens
│
├── requirements_registry.json   # All requirements with full metadata
│   Goal: Single source of truth for what must be built
│
├── requirements_index.json      # Quick lookup by ID, type, priority, screen
│   Goal: Fast requirement retrieval without parsing full registry
│
├── data_model.json              # Entity definitions and relationships
│   Goal: Machine-readable entity graph for validation
│
├── api_contracts.json           # API endpoint registry
│   Goal: Track all API endpoints for consistency checking
│
├── implementation_sequence.json # Build phase ordering with dependencies
│   Goal: Define optimal implementation order
│
├── progress.json                # Phase completion tracking
│   Goal: Know what's done, what's pending, what failed
│
├── test_data_manifest.json      # Test data inventory
│   Goal: Track all generated test data files
│
├── prompt_log.json              # Executed prompt history
│   Goal: Audit trail of AI interactions
│
├── feedback_sessions.json       # Change management sessions
│   Goal: Track feedback and resulting changes
│
├── backups.json                 # Backup registry
│   Goal: Track backup locations for recovery
│
├── GAP_REMEDIATION_PLAN.md      # Identified gaps and remediation steps
│   Goal: Document what's missing and how to fix it
│
├── PROGRESS.md                  # Human-readable progress summary
│   Goal: Quick status check without parsing JSON
│
├── REQUIREMENTS_REGISTRY.md     # Human-readable requirements
│   Goal: Review and discuss requirements
│
└── PROMPT_LOG.md                # Human-readable prompt history
    Goal: Review AI interactions
```

**Pattern:** `{noun}.json` for machine data, `{NOUN}.md` for human documentation.

---

## 00-foundation/ Directory

**Goal:** Establish all foundational elements that components and screens will reference. Nothing in 01+ should be created without these foundations existing.

```
00-foundation/
│
├── DESIGN_BRIEF.md              # Visual direction and strategy
│   Goal: Document design decisions and rationale
│
├── DESIGN_PRINCIPLES.md         # UX/UI guiding principles
│   Goal: Decision framework for design choices
│
├── DESIGN_TOKENS.md             # Token system overview
│   Goal: Explain token architecture and usage
│
├── colors.md                    # Color palette and semantic mappings
│   Goal: Document all color tokens with use cases
│
├── typography.md                # Type scale and text styles
│   Goal: Document all typography tokens
│
├── spacing-layout.md            # Spacing scale and layout tokens
│   Goal: Document spacing, sizing, and layout tokens
│
├── data-model/                  # Domain entity definitions
│   │
│   ├── DATA_MODEL.md            # Overview, statistics, relationships
│   │   Goal: Human-readable entity documentation
│   │
│   ├── ENTITY_INDEX.md          # Quick entity lookup with relationships
│   │   Goal: Navigate to any entity quickly
│   │
│   ├── entities/                # One schema file per entity
│   │   └── {EntityName}.schema.json
│   │   Goal: JSON Schema defining each entity's structure
│   │
│   ├── dictionaries/
│   │   ├── data-dictionary.md   # Field definitions across all entities
│   │   │   Goal: Consistent field naming and typing
│   │   └── enum-values.md       # All enumeration definitions
│   │       Goal: Document valid values for enum fields
│   │
│   ├── constraints/
│   │   ├── referential-integrity.md  # Foreign key relationships
│   │   │   Goal: Document required relationships
│   │   └── validation-rules.md       # Field validation rules
│   │       Goal: Document business rules for data
│   │
│   ├── relationships/
│   │   └── ERD.puml             # Entity relationship diagram
│   │       Goal: Visual representation of data model
│   │
│   └── generate_detailed_files.py
│       Goal: Automation script for schema generation
│
├── api-contracts/               # API specification
│   │
│   ├── API_CONTRACTS.md         # Overview, conventions, authentication
│   │   Goal: Document API design decisions
│   │
│   ├── openapi.yaml             # Machine-readable API spec
│   │   Goal: Standard format for tooling integration
│   │
│   ├── endpoints/               # Per-resource endpoint documentation
│   │   └── {resource}.api.md    # Full REST operations for resource
│   │   Goal: Complete endpoint documentation
│   │
│   ├── types/                   # TypeScript type definitions
│   │   ├── entities.d.ts        # Entity interfaces
│   │   ├── requests.d.ts        # Request payload types
│   │   ├── responses.d.ts       # Response payload types
│   │   ├── errors.d.ts          # Error types
│   │   └── index.d.ts           # Re-exports
│   │   Goal: Type safety for API consumers
│   │
│   ├── examples/
│   │   ├── curl-examples.md     # Command-line examples
│   │   └── fetch-examples.js    # JavaScript examples
│   │   Goal: Copy-paste ready API usage
│   │
│   ├── mocks/
│   │   ├── README.md            # Mock usage instructions
│   │   ├── data/
│   │   │   └── mock-data.json   # Static mock responses
│   │   └── handlers/
│   │       └── {resource}.mock.js  # MSW/mock handlers
│   │   Goal: Enable frontend development without backend
│   │
│   └── generate_detailed_api_files.py
│       Goal: Automation script
│
└── test-data/                   # Realistic test data
    │
    ├── TEST_DATA_README.md      # Data generation approach, usage
    │   Goal: Explain test data structure and relationships
    │
    ├── datasets/
    │   ├── catalog/             # Reference/lookup data (low volume, static)
    │   │   └── {category}.json
    │   │   Goal: Seed data for dropdowns, lookups
    │   │
    │   ├── core/                # Primary business entities
    │   │   └── {entity}.json
    │   │   Goal: Main entity instances
    │   │
    │   ├── transactional/       # Events, activities, relationships
    │   │   └── {activity}.json
    │   │   Goal: Data showing entity interactions
    │   │
    │   ├── personas/            # Filtered views per user role
    │   │   └── {persona-name}/
    │   │       └── {view}.json
    │   │   Goal: "What this user sees" datasets
    │   │
    │   ├── scenarios/           # End-to-end user journeys
    │   │   └── {scenario-name}.json
    │   │   Goal: Data demonstrating complete workflows
    │   │
    │   └── combined/
    │       └── full-dataset.json
    │       Goal: All data in single file for seeding
    │
    ├── personas/                # Persona definitions (who, not what they see)
    │   └── {persona-name}/
    │
    ├── scenarios/               # Scenario definitions
    │
    └── generate_*.py            # Data generation scripts
        Goal: Reproducible data generation
```

---

## 01-components/ Directory

**Goal:** Define every reusable UI component with enough detail that implementation is deterministic.

```
01-components/
│
├── COMPONENT_LIBRARY_SUMMARY.md  # Full inventory with categories
│   Goal: Overview of entire component system
│
├── FINAL_DELIVERY_SUMMARY.md     # Delivery status and sign-off
│   Goal: Track component completion
│
├── primitives/                   # Foundation form elements
│   │   Goal: Basic interactive elements (button, input, select, etc.)
│   ├── README.md                 # Category overview
│   └── {component}.md            # Individual component spec
│
├── data-display/                 # Content presentation components
│   │   Goal: Show data to users (card, table, list, badge, etc.)
│   └── {component}.md
│
├── feedback/                     # User communication components
│   │   Goal: Inform users of state (alert, toast, tooltip, etc.)
│   └── {component}.md
│
├── navigation/                   # Wayfinding components
│   │   Goal: Help users navigate (tabs, sidebar, breadcrumb, etc.)
│   └── {component}.md
│
├── overlays/                     # Floating UI components
│   │   Goal: Content above main layer (dialog, drawer, dropdown, etc.)
│   └── {component}.md
│
└── patterns/                     # Domain-specific composite components
    │   Goal: Reusable combinations specific to this solution
    └── {pattern}.md              # Composed from above categories
```

**Component Spec Structure:**
Each `{component}.md` should include:
- Overview and purpose
- Anatomy diagram
- Variants with use cases
- Props/API definition
- States (default, hover, focus, disabled, loading)
- Accessibility requirements
- Token mappings
- Usage examples
- Requirements addressed

---

## 02-screens/ Directory

**Goal:** Define every application screen with layout, components, data, and interactions.

```
02-screens/
│
├── SCREEN_SPECIFICATIONS_SUMMARY.md  # All screens inventory
│   Goal: Overview of all applications and screens
│
├── DELIVERY_SUMMARY.md               # Delivery status
│   Goal: Track screen completion
│
├── README.md                         # Navigation guide
│
└── {app-or-role-name}/               # One directory per application/portal
    │   Goal: Group screens by user role or application
    │
    ├── README.md                     # App overview, user role, navigation flow
    │
    └── {screen-name}.md              # Individual screen specification
        Goal: Complete screen definition
```

**Screen Spec Structure:**
Each `{screen-name}.md` should include:
- Metadata (ID, URL, access roles, priority)
- Requirements addressed (with traceability)
- Purpose (user goal, business goal, success metric)
- Layout (ASCII diagram or wireframe)
- Grid structure
- Components used (referencing 01-components/)
- Data requirements (entities, queries)
- User interactions
- States (loading, empty, error, success)
- Accessibility considerations
- Responsive behavior

**Naming Conventions:**
- App directories: `{role}-app/` or `{role}-portal/` or `{feature}-module/`
- Screen files: `{noun}-{view-type}.md` (e.g., `user-list.md`, `order-detail.md`)

---

## 03-interactions/ Directory

**Goal:** Define motion design, micro-interactions, and accessibility specifications that apply across all components and screens.

```
03-interactions/
│
├── README.md                     # Directory overview
│
├── motion-system.md              # Animation principles and tokens
│   Goal: Define duration, easing, and animation principles
│   Contents: Timing tokens, easing functions, transition patterns
│
├── micro-interactions.md         # Per-component animations
│   Goal: How each component type animates
│   Contents: Hover, focus, active, loading states per component
│
├── accessibility-specs.md        # WCAG compliance specifications
│   Goal: Ensure accessible interactions
│   Contents: Keyboard nav, focus management, screen reader support
│
└── PHASE_06_VALIDATION_REPORT.md # Validation results
    Goal: Document interaction layer verification
```

---

## 04-implementation/ Directory

**Goal:** Provide clear, ordered path from specifications to working code.

```
04-implementation/
│
├── IMPLEMENTATION_PLAN.md        # Master plan overview
│   Goal: High-level implementation strategy
│
├── IMPLEMENTATION_INDEX.md       # Navigation to all implementation docs
│   Goal: Quick access to any implementation document
│
├── MASTER_IMPL_PROMPT.md         # Master prompt for code generation
│   Goal: Entry point for AI code generation
│
├── {APP}_IMPLEMENTATION_PLAN.md  # Per-application implementation
│   Goal: App-specific implementation guidance
│
├── PHASE_NN_VALIDATION_REPORT.md # Phase validation results
│   Goal: Document phase completion verification
│
├── generate_implementation_sequence.py
│   Goal: Automation script
│
├── sequence/                     # Ordered implementation phases
│   │   Goal: Define what to build in what order
│   │
│   ├── phase-00-setup.md         # Project scaffolding
│   ├── phase-01-{name}.md        # Foundation phase
│   ├── phase-02-{name}.md        # Next phase
│   └── phase-NN-{name}.md        # Final phase
│
├── checkpoints/                  # Validation gates between phases
│   │   Goal: Define "done" criteria before proceeding
│   │
│   ├── checkpoint-01-{name}.md
│   ├── checkpoint-02-{name}.md
│   └── checkpoint-NN-{name}.md
│
└── prompts/                      # Structured prompts for AI coding
    │   Goal: Optimized prompts for each implementation task
    │
    ├── foundation-setup.md       # Project setup prompt
    ├── component-development.md  # Component implementation prompt
    ├── screen-implementation.md  # Screen implementation prompt
    └── {task-specific}.md        # Additional task prompts
```

---

## 05-validation/ Directory

**Goal:** Verify prototype meets all requirements before delivery.

```
05-validation/
│
├── VALIDATION_REPORT.md          # Current validation status
│   Goal: Overall validation summary
│
├── VALIDATION_REPORT_FINAL.md    # Final sign-off document
│   Goal: Delivery approval
│
├── VALIDATION_REPORT_V{N}.md     # Version history
│   Goal: Track validation iterations
│
├── TRACEABILITY_MATRIX.md        # Requirement → Implementation mapping
│   Goal: Prove every requirement is addressed
│
├── REQUIREMENTS_COVERAGE.md      # Coverage analysis by priority
│   Goal: P0/P1/P2 coverage percentages
│
├── QA_CHECKLIST.md               # Manual testing checklist
│   Goal: Guide manual verification
│
└── accessibility/
    ├── a11y-audit-results.md     # Accessibility audit findings
    │   Goal: Document accessibility issues
    └── wcag-compliance.md        # WCAG conformance status
        Goal: Track WCAG level compliance
```

---

## prototype/ Directory

**Goal:** Self-contained, buildable application demonstrating all specifications.

```
prototype/
│
├── package.json                  # Dependencies and scripts
├── vite.config.ts                # Build configuration (or equivalent)
├── tsconfig.json                 # TypeScript configuration
├── index.html                    # Entry HTML
├── README.md                     # Setup and run instructions
├── .gitignore
│
├── public/                       # Static assets
│   └── assets/
│
└── src/
    ├── main.tsx                  # Application entry point
    ├── App.tsx                   # Root component
    ├── index.css                 # Global styles
    │
    ├── components/               # Mirrors 01-components/ categories
    │   ├── primitives/
    │   ├── data-display/
    │   ├── feedback/
    │   ├── navigation/
    │   ├── overlays/
    │   └── patterns/
    │
    ├── screens/                  # Mirrors 02-screens/ apps
    │   └── {app-name}/
    │
    ├── db/                       # Local data layer
    │   ├── database.ts           # Database setup
    │   ├── schema.ts             # Type definitions
    │   └── seed.ts               # Seed data loading
    │
    ├── services/                 # API and business logic
    ├── hooks/                    # Custom hooks
    ├── contexts/                 # State contexts
    ├── utils/                    # Utility functions
    ├── types/                    # TypeScript types
    │
    └── styles/
        ├── tokens.css            # Design tokens as CSS variables
        └── global.css            # Global styles
```

---

## src/ Directory (Alternative)

**Goal:** Simpler prototype without build tooling (vanilla JS, no bundler).

```
src/
├── index.html
├── app.js
├── styles.css
│
├── components/                   # Same organization as prototype/src/
├── screens/
├── db/
├── services/
├── forms/
├── pages/
├── utils/
└── workflows/
```

---

## reports/ Directory

**Goal:** Document verification activities beyond automated testing.

```
reports/
│
├── ui-audit/
│   ├── AUDIT_SUMMARY.md          # Overall visual audit status
│   │   Goal: Executive summary of visual verification
│   │
│   ├── {FEAT-NNN}-AUDIT-REPORT.md  # Per-feature audit
│   │   Goal: Detailed audit of feature area
│   │
│   ├── {feat-nnn}-scans/         # Screenshots organized by breakpoint
│   │   ├── desktop/
│   │   ├── tablet/
│   │   └── mobile/
│   │
│   └── ui-audit-report.json      # Machine-readable results
│
└── change-reports/               # Change management reports
    └── CR-{YYYY-MM-DD}-{NNN}_REPORT.md
        Goal: Document feedback and resulting changes
```

---

## File Naming Conventions

### Directories
| Rule | Example |
|------|---------|
| Always kebab-case | `data-model/`, `api-contracts/` |
| Numbered prefixes for lifecycle | `00-foundation/`, `01-components/` |

### Markdown Files
| Pattern | When to Use | Example |
|---------|-------------|---------|
| `UPPER_SNAKE.md` | Summary/overview docs | `DESIGN_BRIEF.md` |
| `kebab-case.md` | Content/spec files | `button.md`, `user-list.md` |

### JSON Files
| Pattern | When to Use | Example |
|---------|-------------|---------|
| `snake_case.json` | State/config files | `progress.json` |
| `kebab-case.json` | Data files | `mock-data.json` |
| `PascalCase.schema.json` | Schema definitions | `User.schema.json` |

### Code Files
| Pattern | When to Use | Example |
|---------|-------------|---------|
| `PascalCase.tsx/jsx` | React components | `Button.tsx` |
| `camelCase.ts/js` | Utilities, hooks | `useDatabase.ts` |
| `snake_case.py` | Python scripts | `generate_test_data.py` |

### Standard File Names
| File | Purpose |
|------|---------|
| `README.md` | Directory explanation |
| `*_SUMMARY.md` | High-level overview |
| `*_INDEX.md` | Navigable listing |
| `PHASE_{NN}_*.md` | Phase-specific documents |

---

## Skill → Output Mapping

| Skill | Primary Directory | Goal |
|-------|-------------------|------|
| ValidateDiscovery | `_state/` | Extract structured data from discovery |
| Requirements | `_state/` | Create requirements registry |
| DataModel | `00-foundation/data-model/` | Define domain entities |
| ApiContracts | `00-foundation/api-contracts/` | Define API specification |
| TestData | `00-foundation/test-data/` | Generate realistic test data |
| DesignBrief | `00-foundation/` | Document design direction |
| DesignTokens | `00-foundation/` | Define token system |
| Components | `01-components/` | Specify UI components |
| Screens | `02-screens/` | Specify application screens |
| Interactions | `03-interactions/` | Define motion and accessibility |
| Sequencer | `04-implementation/` | Create build sequence |
| Prompts | `04-implementation/prompts/` | Create code gen prompts |
| CodeGen | `prototype/` or `src/` | Generate working code |
| QA | `05-validation/` | Verify requirements coverage |
| UIAudit | `reports/ui-audit/` | Visual verification |

---

## Validation Checklist

Before marking any skill complete:

- [ ] Output directory exists at expected path
- [ ] Summary/overview file created at directory root
- [ ] Subdirectories follow expected category structure
- [ ] File names follow naming conventions
- [ ] JSON files are valid and parseable
- [ ] Markdown files have consistent structure
- [ ] `_state/progress.json` updated with completion
- [ ] Requirements traceability documented
- [ ] Human-readable companion exists for machine files
