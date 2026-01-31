# Prototype Skills Framework

> **📁 OUTPUT STRUCTURE**: All skills must follow the folder structure defined in [OUTPUT_STRUCTURE.md](OUTPUT_STRUCTURE.md). This is the authoritative reference for file naming, directory organization, and output conventions.

> **⚠️ CRITICAL - ACTIVE FILE OPERATIONS**: Instructions in skills like `READ _state/prompt_log.json` and `WRITE _state/progress.json` are **NOT pseudocode**. Claude MUST actually use file tools to read, modify, and write these files. If state files are empty after running skills, Claude failed to execute the instructions correctly.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: References to specific apps (e.g., "Recruiter App", "Candidate Portal", "Hiring Manager Dashboard"), entities (e.g., "Candidate", "Position", "Interview"), or domains (e.g., "ATS", "HR Tech") throughout these skills are **examples only**. The actual apps, entities, and structure should be derived from the discovery documents for each specific project.

> **🔗 DYNAMIC SKILL INVOCATION**: Skills can invoke other skills (including 3rdParty skills) using the `INVOKE_SKILL` pattern. See [SKILL_INVOCATION.md](SKILL_INVOCATION.md) for the full invocation framework and [SKILL_REGISTRY.json](SKILL_REGISTRY.json) for the skill registry.

## Overview

This framework provides 20 skills for generating and managing prototypes from discovery documentation. Every skill is designed with three critical capabilities:

1. **Progress Tracking**: Every skill updates `_state/progress.json` on completion
2. **Requirements Traceability**: Skills link their outputs to the requirements registry
3. **Prompt Logging**: All executed prompts are logged for audit and debugging

## Core Principles

### Progress.json Updates
Every skill MUST update progress.json with:
- Phase status (`complete`, `in_progress`, `blocked`)
- Completion timestamp
- Output files generated
- Metrics relevant to that phase

### Requirements Traceability
The requirements registry (`_state/requirements_registry.json`) is the single source of truth. Skills that generate specs MUST:
- Include "Requirements Addressed" sections in their outputs
- Update the registry's `addressed_by` arrays
- Track P0 coverage metrics

### Input/Output Validation
Every skill MUST:
- **Validate Inputs**: Check required files exist and contain expected data
- **Validate Outputs**: Verify generated outputs meet requirements
- **Prompt for Mitigation**: When validation fails, ask user how to proceed

### Verification Gate (Phase 1 Enhancement)
> **See: [VERIFICATION_GATE.md](VERIFICATION_GATE.md) for full pattern**

Every skill MUST execute a verification gate before marking any phase as "complete":
- Run ALL verification commands fresh (no relying on previous runs)
- Capture output as evidence
- ONLY mark complete if ALL checks pass
- Block with user options if verification fails

**Forbidden phrases before verification:** "Should pass now", "Looks correct", "Probably complete"

### Test-Driven Development (Phase 1 Enhancement)
> **See: Prototype_CodeGen/SKILL.md for TDD integration**

The CodeGen skill enforces TDD for all code generation:
- **RED**: Write failing test first
- **GREEN**: Write minimal code to pass
- **REFACTOR**: Clean up while staying green
- **No exceptions**: Implementation without test = DELETE and restart

### Systematic Debugging (Phase 1 Enhancement)
> **See: Prototype_ChangeManager/SKILL.md for debugging integration**

For Bug-type changes, the ChangeManager requires root cause investigation:
- **No fix without root cause**: Random fixes are prohibited
- **Four-phase process**: Read errors → Reproduce → Check changes → Trace data
- **Hypothesis confirmation**: User must confirm root cause before fix variants
- **Fix thrashing prevention**: After 3 failed fixes, escalate to architectural review

### Frontend Design (Phase 2 Enhancement)
> **See: Prototype_Components/SKILL.md and Prototype_CodeGen/SKILL.md**

Avoid generic AI aesthetics and create distinctive, memorable interfaces:
- **Aesthetic Direction**: Choose bold visual direction before component generation
- **Visual Treatment**: Every component spec includes typography, color, shape, animation details
- **Forbidden Patterns**: Inter/Roboto/Arial fonts, purple gradients, generic 8px radius
- **Motion Library**: Framer-motion integration for sophisticated animations

### Theme Factory (Phase 2 Enhancement)
> **See: Prototype_DesignTokens/SKILL.md**

10 professional pre-set themes for quick, cohesive styling:
- Ocean Depths, Sunset Boulevard, Forest Canopy, Modern Minimalist
- Golden Hour, Arctic Frost, Desert Rose, Tech Innovation
- Botanical Garden, Midnight Galaxy
- Custom theme generation from description

### Visual Documentation (Phase 2 Enhancement)
> **See: Prototype_DataModel, Prototype_Sequencer skills**

Interactive HTML visualizations for documentation:
- **ERD Visualization**: Interactive entity relationship diagram (DataModel)
- **Implementation Roadmap**: Visual timeline with phases and checkpoints (Sequencer)
- SVG-based diagrams with hover effects and statistics

### Professional Deliverables (Phase 4 Enhancement)
> **See: Prototype_Deliverables skill**

Export prototype artifacts as professional documents:
- **Presentations**: Requirements deck, prototype overview (PPTX)
- **Documents**: Prototype specification, technical handoff (DOCX)
- **Reports**: QA report, accessibility report, requirements summary (PDF)
- Interactive deliverable selection and manifest generation

### Interactive Gap Filling (Phase 4 Enhancement)
> **See: Prototype_ValidateDiscovery/SKILL.md**

When discovery documents have gaps, use collaborative questioning to fill them:
- **One question at a time**: Focused, manageable interactions
- **Multiple choice preferred**: Easy selection for common patterns
- **Incremental validation**: Confirm each gap is filled before moving on
- **YAGNI principle**: Only gather essential information

### Root Cause Tracing (Phase 4 Enhancement)
> **See: Prototype_QA/SKILL.md**

When validation fails, systematically trace to root cause:
- **Observe symptom**: Identify what failed and how
- **Find immediate cause**: Which output is missing or incorrect?
- **Trace backwards**: Build chain from symptom to source skill
- **Fix at source**: Apply fix at origin, not at symptom point
- **Defense in depth**: Recommend preventive measures at each layer

### Modern Stack Options (Phase 5 Enhancement)
> **See: Prototype_CodeGen/SKILL.md**

Advanced technology stack selection:
- **Standard Stack**: React 18 + TypeScript + Vite + Tailwind CSS
- **shadcn/ui Stack**: 40+ pre-built accessible components, Radix UI primitives
- **Artifact Mode**: Bundle prototype to single HTML file for sharing
- Parcel-based bundling with all dependencies inlined

### Custom Visual Assets (Phase 5 Enhancement)
> **See: Prototype_DesignTokens/SKILL.md**

Generate custom visual assets with design philosophy approach:
- **Design Philosophy**: Create visual movement manifesto before assets
- **Icons**: Custom icon sets matching design tokens
- **Illustrations**: Empty states, onboarding, success/error graphics
- **Patterns**: Background textures, gradients, geometric decorations
- **Hero Graphics**: Landing page and feature visuals

### Document Conversion (Phase 5 Enhancement)
> **See: Prototype_ValidateDiscovery/SKILL.md**

Convert various file formats to markdown for processing:
- **Supported**: PDF, DOCX, PPTX, XLSX, CSV, HTML, JSON, XML, images
- **OCR**: Extract text from wireframe images, whiteboard photos
- **AI Descriptions**: Optional vision model for rich image context
- **MarkItDown**: Microsoft's conversion tool with plugin support

### Dynamic Skill Invocation (Phase 5 Enhancement)
> **See: SKILL_INVOCATION.md, SKILL_REGISTRY.json**

Skills can dynamically invoke other skills at runtime:
- **Skill Registry**: Central JSON registry of all available skills
- **INVOKE_SKILL Pattern**: Standard syntax for inter-skill calls
- **3rdParty Integration**: Call theme-factory, canvas-design, etc. from prototype skills
- **Fallback Support**: Graceful degradation when invoked skill unavailable

Example invocation:
```
INVOKE_SKILL:
  skill: "theme-factory"
  inputs:
    theme_name: "ocean_depths"
  on_success: STORE selected_theme
  on_failure: WARN "Using default theme"
```

### Prompt Logging (ACTIVE FILE OPERATIONS REQUIRED)
Every skill MUST **actually write** to `_state/prompt_log.json` using file tools:

**BEFORE generating content:**
```
1. Filesystem:read_text_file({path: "_state/prompt_log.json"})
2. Parse JSON, add new entry with status="pending"
3. Filesystem:write_file({path: "_state/prompt_log.json", content: updatedJSON})
```

**AFTER generating content:**
```
1. Filesystem:read_text_file({path: "_state/prompt_log.json"})
2. Find entry, update result.status="success", add output_summary
3. Filesystem:write_file({path: "_state/prompt_log.json", content: updatedJSON})
```

Each entry includes:
- Skill name and step
- Desired outcome
- Inputs and target files
- Execution result

## Skill Index

### Generation Skills (Build Phase)

| Skill | Purpose | Updates Registry | Priority |
|-------|---------|------------------|----------|
| **ValidateDiscovery** | Validate discovery docs | No | First |
| **Requirements** | Create requirements registry | Creates it | Foundation |
| **DataModel** | Generate entity schemas | Yes | Foundation |
| **ApiContracts** | Define API endpoints | Yes | Foundation |
| **TestData** | Generate test data | Yes (story links) | Foundation |
| **DesignBrief** | Design direction | Yes (pain points) | Design |
| **DesignTokens** | CSS custom properties | Yes (A11Y tokens) | Design |
| **Components** | Component specifications | **Yes (MANDATORY)** | Design |
| **Screens** | Screen specifications | **Yes (MANDATORY)** | Design |
| **Interactions** | Motion/animation tokens | Yes (A11Y-006) | Design |
| **Sequencer** | Implementation order | No | Implementation |
| **Prompts** | External code prompts | References reqs | Implementation |
| **CodeGen** | Direct code generation | Tracks at checkpoints | Implementation |

### Validation Skills (Quality Phase)

| Skill | Purpose | Updates Registry | Priority |
|-------|---------|------------------|----------|
| **QA** | Requirements validation | **Validates 100% P0** | Validation |
| **UIAudit** | Visual QA | Verifies A11Y | Validation |

### Documentation Skills

| Skill | Purpose | Updates Registry | Priority |
|-------|---------|------------------|----------|
| **Decomposition** | OPML mindmap of structure | Reads registry | Documentation |
| **PromptLog** | Log all executed prompts | N/A | Audit/Debug |
| **Deliverables** | Export to PPTX/DOCX/PDF | No | Delivery |

### Management Skills

| Skill | Purpose | Updates Registry | Priority |
|-------|---------|------------------|----------|
| **ChangeManager** | Post-feedback change management | Creates/Links | Post-Build |
| **Migrate** | Version migration | Preserves registry | Utility |
| **Builder** | Pipeline coordination | Enforces tracking | Meta |

## Lifecycle Phases

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROTOTYPE LIFECYCLE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │  BUILD   │───►│ VALIDATE │───►│ FEEDBACK │───►│  CHANGE  │ │
│  │  PHASE   │    │  PHASE   │    │ SESSION  │    │  CYCLE   │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       │               │               │               │        │
│   Builder         QA, UIAudit    (External)    ChangeManager   │
│   + Skills                                                      │
│                                                                 │
│                          ◄────────────────────────────┘        │
│                              (iterate)                          │
└─────────────────────────────────────────────────────────────────┘
```

## Auto-Invocation Pattern

Some skills automatically invoke other skills when structural changes occur:

| Triggering Skill | Auto-Invokes | Trigger Event |
|------------------|--------------|---------------|
| Components | Decomposition | Component library changed |
| Screens | Decomposition | Pages structure changed |
| CodeGen | Decomposition | Structure finalized |
| QA | Decomposition | Test statuses updated |
| ChangeManager | QA, Decomposition | After implementation |

Auto-invocation is **non-blocking** — if the invoked skill fails, the triggering skill still succeeds.

## Change Management (Post-Build)

After user feedback sessions, use the **ChangeManager** skill to:

1. **Capture Feedback** - Structured input from testing sessions
2. **Group Related Items** - Batch changes for efficiency
3. **Analyze Impact** - Full regression scope analysis
4. **Propose Variants** - 3 implementation options for Medium/Large changes
5. **Implement Surgically** - Minimal changes preserving customizations
6. **Validate Changes** - Targeted regression testing
7. **Track Everything** - Full audit trail and traceability

### Expert Roles
The ChangeManager acts as:
- **Project Manager**: Session tracking, planning
- **Product Expert**: Requirements alignment
- **Risk Manager**: Impact assessment
- **QA Specialist**: Regression scope
- **UX Designer**: Interaction solutions
- **UI Expert**: Component/screen changes
- **Technology Lead**: Technical feasibility

### Change Size Classification

| Size | Criteria | Variants? |
|------|----------|-----------|
| **Small** | ≤1 screen, ≤2 components, <2h | Direct implementation |
| **Medium** | 2-4 screens, 3-5 components, 2-8h | 3 variants proposed |
| **Large** | 5+ screens, 6+ components, >8h | 3 variants proposed |

## Prompt Logging

All skills log their prompts to enable:
- **Audit trail**: See exactly what was generated and how
- **Debugging**: Identify which prompts failed and why
- **Reproducibility**: Re-run specific prompts
- **Metrics**: Track token usage, duration, success rates

### Log Structure
```json
{
  "id": "PL-047",
  "skill": "Prototype_Components",
  "step": "Step 3: Generate Spec",
  "desired_outcome": "Generate Button component with variants",
  "prompt_text": "Generate a component specification for Button...",
  "result": {
    "status": "success",
    "duration_ms": 2340,
    "output_summary": "Generated Button with 4 variants"
  }
}
```

## Mandatory Requirements Sections

The following skills MUST include "Requirements Addressed" sections in their outputs:

### Components (MANDATORY)
Every component spec must include:
```markdown
## Requirements Addressed
| Req ID | Type | Description | Implementation |
|--------|------|-------------|----------------|
| A11Y-001 | Accessibility | Keyboard navigation | Tab to focus |
```

### Screens (MANDATORY)
Every screen spec must include:
```markdown
## Requirements Addressed
| Req ID | Type | Description | Implementation |
|--------|------|-------------|----------------|
| US-001 | User Story | View candidates | DataTable displays all |
```

## Validation and Mitigation

Every skill prompts the user when validation fails:

```
═══════════════════════════════════════════
⚠️ VALIDATION FAILED
═══════════════════════════════════════════

[Description of failure]

How would you like to proceed?
1. "fix: [item]" - Address specific issue
2. "skip" - Continue without (may affect downstream)
3. "abort" - Stop and fix manually
═══════════════════════════════════════════
```

## P0 Coverage Enforcement

The QA skill enforces 100% P0 coverage:
- If P0 coverage < 100%, delivery is **BLOCKED**
- Unaddressed P0 requirements are listed
- Resolution is required before proceeding

## Skill Dependency Order

```
ValidateDiscovery
       │
       ▼
  Requirements
       │
       ├──────────────┐
       ▼              ▼
   DataModel     DesignBrief
       │              │
       ▼              ▼
 ApiContracts   DesignTokens
       │              │
       ▼              ▼
   TestData      Components ──────┐
                      │           │
                      ▼           │ (auto-invokes)
                   Screens ───────┤
                      │           │
                      ▼           │
                Interactions      ▼
                      │      Decomposition
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
   Sequencer      Prompts        CodeGen ──────┐
                                    │          │
       └────────────┬───────────────┘          │ (auto-invokes)
                    ▼                          │
                   QA  ←─── BLOCKS if P0 < 100%┤
                    │                          │
                    ▼                          ▼
                UIAudit               Decomposition
                    │
                    ▼
            ┌───────────────┐
            │   FEEDBACK    │  (external user testing)
            │   SESSION     │
            └───────────────┘
                    │
                    ▼
            ┌───────────────┐
            │ ChangeManager │──► Decomposition
            │  (iterate)    │──► QA (targeted)
            └───────────────┘
```

## Builder Commands

### Build Phase
| Command | Action |
|---------|--------|
| `build` | Execute all skills in order |
| `build from {skill}` | Resume from specific skill |
| `build only {skill}` | Execute single skill |
| `status` | Show current progress |
| `requirements` | Show P0 coverage progress |
| `validate` | Run QA validation only |
| `reset` | Clear progress, start fresh |

### Documentation
| Command | Action |
|---------|--------|
| `decompose` | Generate/update OPML decomposition |
| `decompose {AppName}` | Generate/update for specific app |
| `show prompt log` | Display recent prompt entries |
| `export prompt log` | Export complete prompt log |

### Change Management
| Command | Action |
|---------|--------|
| `new session` | Start feedback session |
| `resume session [id]` | Continue existing session |
| `list sessions` | Show all feedback sessions |
| `next change` | Process next pending change |
| `rollback to [backup]` | Restore from backup |

## Usage

### Start New Prototype
```
"Generate prototype from [discovery_path] to [output_path]"
```

### Check Progress
```
"Prototype status"
```

### Resume Work
```
"Resume prototype"
```

### Run Single Skill
```
"Generate components"
"Run QA validation"
```

### Generate Traceability View
```
"Decompose" or "Generate decomposition"
```

### View Prompt History
```
"Show prompt log"
"Show prompt log for Components"
```

### Manage Changes (Post-Build)
```
"New session" - Start feedback session
"Next change" - Process pending change
"Rollback to BK-xxx" - Restore from backup
```

## State Files Summary

| File | Purpose |
|------|---------|
| `_state/progress.json` | Build progress tracking |
| `_state/requirements_registry.json` | All requirements |
| `_state/prompt_log.json` | Prompt audit trail |
| `_state/feedback_sessions.json` | Feedback session tracking |
| `_state/backups.json` | Backup registry |
| `_state/PROMPT_LOG.md` | Human-readable prompt log |

## Output Directories

| Directory | Contents |
|-----------|----------|
| `outputs/01-design-system/` | Design tokens, brief |
| `outputs/02-components/` | Component specs |
| `outputs/03-screens/` | Screen specs |
| `outputs/04-interactions/` | Animation specs |
| `outputs/05-sequence/` | Implementation order |
| `outputs/06-prompts/` | Code generation prompts |
| `outputs/07-qa/` | QA reports, traceability |
| `outputs/08-audit/` | UI audit results |
| `outputs/09-decomposition/` | OPML mindmaps |
| `outputs/06-deliverables/` | Professional documents (PPTX, DOCX, PDF) |
| `outputs/change-reports/` | Change request reports |
| `src/` | Generated code |
| `_backups/` | Pre-change backups |
