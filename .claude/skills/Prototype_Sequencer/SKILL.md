---
name: sequencing-prototype-implementation
description: Use when you need to generate a phased implementation sequence, including checkpoints, implementation plans, and individual task prompts.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill sequencing-prototype-implementation started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill sequencing-prototype-implementation ended '{"stage": "prototype"}'
---

# Sequence Prototype Implementation

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill sequencing-prototype-implementation instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_Sequencer
- **Version**: 2.3.1
- **Created**: 2024-12-13
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3

## Description
Generate implementation sequence with phases, checkpoints, and prompts. Creates the complete implementation plan structure.

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

Generate implementation sequence with phased approach, checkpoints, and code generation prompts. Follows OUTPUT_STRUCTURE.md for deterministic folder structure.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: App names in implementation plans (e.g., "CANDIDATE_APP_IMPLEMENTATION_PLAN.md") are examples from an ATS domain. Your actual implementation plans should be generated for your project's apps.

## Output Structure (REQUIRED)

This skill MUST generate the following structure pattern:

```
04-implementation/
├── CANDIDATE_APP_IMPLEMENTATION_PLAN.md   # Per-app plans (one per app)
├── checkpoints/
│   ├── checkpoint-01-foundation.md
│   ├── checkpoint-02-core-functionality.md
│   ├── checkpoint-03-dashboards.md
│   └── checkpoint-04-production-ready.md
├── generate_implementation_sequence.py
├── IMPLEMENTATION_INDEX.md
├── IMPLEMENTATION_PLAN.md                 # Master implementation plan
├── MASTER_IMPL_PROMPT.md                  # Master prompt for CodeGen
├── PHASE_07_VALIDATION_REPORT.md
├── prompts/
│   ├── component-development.md
│   ├── foundation-setup.md
│   └── screen-implementation.md
└── sequence/
    ├── phase-00-setup.md
    ├── phase-01-auth.md
    ├── phase-02-catalog.md
    ├── phase-03-core-crud.md
    ├── phase-04-transactional.md
    ├── phase-05-lists-nav.md
    ├── phase-06-details.md
    ├── phase-07-dashboards.md
    ├── phase-08-workflows.md
    ├── phase-09-reporting.md
    └── phase-10-polish.md
```

State file:
```
_state/implementation_sequence.json       # Machine-readable sequence
```

---

## Implementation Phases

| Phase | Name | Description | Dependencies |
|-------|------|-------------|--------------|
| 00 | Setup | Project scaffolding, tooling | None |
| 01 | Auth | Authentication, session | Phase 00 |
| 02 | Catalog | Reference data, lookups | Phase 01 |
| 03 | Core CRUD | Primary entities | Phase 02 |
| 04 | Transactional | Events, activities | Phase 03 |
| 05 | Lists & Nav | List views, navigation | Phase 03 |
| 06 | Details | Detail views, profiles | Phase 05 |
| 07 | Dashboards | Aggregate views | Phase 06 |
| 08 | Workflows | Multi-step processes | Phase 06 |
| 09 | Integrations | External systems, notifications | Phase 07, 08 |
| 10 | Polish | Final refinements, accessibility | Phase 09 |

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ _state/requirements_registry.json → requirements to sequence
READ _state/data_model.json → entity dependencies
READ 01-components/COMPONENT_LIBRARY_SUMMARY.md → components available
READ 02-screens/SCREEN_SPECIFICATIONS_SUMMARY.md → screens to implement

IF any missing:
  BLOCK with appropriate message
```

### Step 2: Analyze Dependencies
```
BUILD dependency graph:
  - Entity dependencies (FK relationships)
  - Screen dependencies (shared components)
  - Requirement dependencies (which reqs need others)
  
DETERMINE optimal implementation order
```

### Step 3: Generate Phase Sequences
```
FOR each phase (00-10):
  CREATE 04-implementation/sequence/phase-{NN}-{name}.md:
    # Phase {NN}: {Name}
    
    ## Overview
    [Phase description and goals]
    
    ## Prerequisites
    - Phase {N-1} complete
    - [specific requirements]
    
    ## Deliverables
    | Deliverable | Type | Priority |
    |-------------|------|----------|
    | Component X | Component | P0 |
    | Screen Y | Screen | P0 |
    
    ## Requirements Addressed
    | Req ID | Description | Deliverable |
    |--------|-------------|-------------|
    | FR-001 | ... | Component X |
    
    ## Implementation Steps
    1. Create [component/screen]
    2. Implement [functionality]
    3. Connect [integrations]
    4. Test [scenarios]
    
    ## Validation Criteria
    - [ ] All P0 deliverables complete
    - [ ] Unit tests passing
    - [ ] Integration verified
    
    ## Estimated Effort
    | Task | Hours |
    |------|-------|
    | Development | X |
    | Testing | Y |
    | **Total** | Z |
```

### Step 4: Generate Checkpoints
```
CREATE 04-implementation/checkpoints/:

CREATE checkpoint-01-foundation.md:
  # Checkpoint 1: Foundation Complete
  
  ## Criteria
  - [ ] Project scaffolded with Vite
  - [ ] Design tokens integrated
  - [ ] Base components implemented
  - [ ] Routing configured
  - [ ] Mock API ready
  
  ## Validation
  - Run: npm run build (no errors)
  - Run: npm run test (all pass)
  - Visual: Base layout renders
  
  ## Sign-off
  Date: ___
  Status: ___

CREATE checkpoint-02-core-functionality.md:
  # Checkpoint 2: Core Functionality
  
  ## Criteria
  - [ ] All core entities have CRUD
  - [ ] Primary screens functional
  - [ ] Data flows working
  
  [... validation criteria ...]

CREATE checkpoint-03-dashboards.md:
  # Checkpoint 3: Dashboards
  
  ## Criteria
  - [ ] All persona dashboards render
  - [ ] Metrics display correctly
  - [ ] Navigation complete
  
  [... validation criteria ...]

CREATE checkpoint-04-production-ready.md:
  # Checkpoint 4: Production Ready
  
  ## Criteria
  - [ ] All P0 requirements addressed
  - [ ] QA validation passed
  - [ ] Accessibility verified
  - [ ] Performance acceptable
  
  [... validation criteria ...]
```

### Step 5: Generate Phase-Numbered Implementation Prompts
```
CREATE 04-implementation/prompts/:

CREATE README.md:
  # Implementation Prompts

  These prompts are designed to guide AI assistants or developers through each implementation phase.

  ## Usage

  1. Copy the prompt for your current phase
  2. Provide it to your AI assistant along with relevant reference files
  3. Review generated code against validation checklist
  4. Proceed to next phase when all validations pass

  ## Prompt Index

  | Phase | Prompt | Description |
  |-------|--------|-------------|
  | 00 | [00-setup-prompt.md](./00-setup-prompt.md) | Project initialization |
  | 01 | [01-auth-layout-prompt.md](./01-auth-layout-prompt.md) | Auth context and app shell |
  | 02 | [02-catalog-prompt.md](./02-catalog-prompt.md) | Database and seed data |
  | 03 | [03-core-crud-prompt.md](./03-core-crud-prompt.md) | Core entity CRUD operations |
  | 04 | [04-transactional-prompt.md](./04-transactional-prompt.md) | Events and activities |
  | 05 | [05-lists-nav-prompt.md](./05-lists-nav-prompt.md) | List views and navigation |
  | 06 | [06-details-prompt.md](./06-details-prompt.md) | Detail views |
  | 07 | [07-dashboards-prompt.md](./07-dashboards-prompt.md) | Dashboard views |
  | 08 | [08-workflows-prompt.md](./08-workflows-prompt.md) | Multi-step workflows |
  | 09 | [09-integrations-prompt.md](./09-integrations-prompt.md) | External integrations |
  | 10 | [10-polish-prompt.md](./10-polish-prompt.md) | Final polish and accessibility |

  ## Prompt Structure

  Each prompt follows this structure:

  1. **Context** - What has been built so far
  2. **Task** - What needs to be implemented
  3. **Specifications** - Technical requirements and code snippets
  4. **Validation** - Checklist of items to verify
  5. **Reference Files** - Pointers to specifications

  ## Tips for AI Assistants

  1. Always read reference files before generating code
  2. Follow the existing code style and patterns
  3. Implement accessibility features (keyboard nav, ARIA)
  4. Add TypeScript types for all interfaces
  5. Include error handling
  6. Test each component in isolation before integration

  ## Checkpoint Validation

  After completing a group of phases, run the corresponding checkpoint:

  - **Checkpoint 1** (after Phase 02): `../checkpoints/checkpoint-01-foundation.md`
  - **Checkpoint 2** (after Phase 05): `../checkpoints/checkpoint-02-core-functionality.md`
  - **Checkpoint 3** (after Phase 07): `../checkpoints/checkpoint-03-dashboards.md`
  - **Checkpoint 4** (after Phase 10): `../checkpoints/checkpoint-04-production-ready.md`

FOR phase_num in 00-10:
  CREATE {phase_num}-{phase_name}-prompt.md:
    # Phase {NN}: {Name} - Implementation Prompt

    ---
    document_id: PROMPT-{NN}
    version: 1.0.0
    created_at: {DATE}
    ---

    ## Context

    You are implementing Phase {NN}: {Name} of {Product Name}.

    **Previous Phases Complete:**
    - [List what was built in previous phases]

    **This Phase Goal:**
    [One sentence describing what this phase builds]

    ## Reference Files

    Read these before starting:
    - `00-foundation/DESIGN_TOKENS.md` - Design system
    - `01-components/component-index.md` - Available components
    - `02-screens/screen-index.md` - Screen specs
    - `../sequence/phase-{NN}-{name}.md` - Full phase spec

    ## Task

    ### Components to Build
    | Component | Category | Spec Location |
    |-----------|----------|---------------|
    | {Component1} | {category} | 01-components/{category}/{component1}.md |

    ### Screens to Build
    | Screen | App | Spec Location |
    |--------|-----|---------------|
    | {Screen1} | {app} | 02-screens/{app}/{screen1}/ |

    ### Services/Hooks to Build
    | Name | Type | Purpose |
    |------|------|---------|
    | {service1} | Service | {description} |
    | {hook1} | Hook | {description} |

    ## Specifications

    ### Component Spec: {Component1}
    ```typescript
    // Key interfaces and implementation hints
    interface {Component1}Props {
      // from component spec
    }
    ```

    ### Screen Layout: {Screen1}
    ```
    ┌─────────────────────────────────────┐
    │  [Visual ASCII layout from spec]    │
    └─────────────────────────────────────┘
    ```

    ## Validation Checklist

    - [ ] All components render correctly
    - [ ] TypeScript compiles without errors
    - [ ] Keyboard navigation works
    - [ ] All tests pass
    - [ ] Accessibility verified

    ## Expected Output Files

    ```
    prototype/src/
    ├── components/{category}/{Component1}.tsx
    ├── screens/{app}/{Screen1}.tsx
    ├── services/{service1}.ts
    └── hooks/{hook1}.ts
    ```

    ## Next Phase

    → [Phase {NN+1}: {NextName}](../sequence/phase-{NN+1}-{next-name}.md)
```

### Step 6: Generate Master Implementation Plan
```
CREATE 04-implementation/IMPLEMENTATION_PLAN.md:
  # Implementation Plan
  
  ## Overview
  Total phases: 11 (00-10)
  Total checkpoints: 4
  Estimated total: {hours} hours
  
  ## Phase Summary
  | Phase | Name | Deliverables | Hours | P0 Reqs |
  |-------|------|--------------|-------|---------|
  | 00 | Setup | 5 | 4 | 0 |
  | 01 | Auth | 3 | 6 | 2 |
  ...
  
  ## Checkpoint Summary
  | Checkpoint | After Phase | Validation |
  |------------|-------------|------------|
  | 1 - Foundation | 02 | Build, tests |
  | 2 - Core | 05 | CRUD working |
  | 3 - Dashboards | 07 | All views |
  | 4 - Production | 10 | Full QA |
  
  ## Critical Path
  [Mermaid diagram or description of critical path]
  
  ## Risk Areas
  | Risk | Impact | Mitigation |
  |------|--------|------------|
  | Complex workflows | High | Early prototype |

CREATE 04-implementation/MASTER_IMPL_PROMPT.md:
  # Master Implementation Prompt
  
  ## Project: {Product Name}
  
  ## Quick Start
  1. Read IMPLEMENTATION_PLAN.md for overview
  2. Start with sequence/phase-00-setup.md
  3. Complete each phase in order
  4. Validate at each checkpoint
  
  ## Key Resources
  - Design: 00-foundation/
  - Components: 01-components/
  - Screens: 02-screens/
  - Interactions: 03-interactions/
  
  ## Implementation Order
  [Full sequence with dependencies]
```

### Step 7: Generate Per-App Plans
```
FOR each app in 02-screens/:
  CREATE 04-implementation/{APP}_IMPLEMENTATION_PLAN.md:
    # {App Name} Implementation Plan
    
    ## Screens
    | Screen | Phase | Priority |
    |--------|-------|----------|
    | dashboard | 07 | P0 |
    | list | 05 | P0 |
    
    ## Components Required
    [List of components needed for this app]
    
    ## Implementation Order
    1. [screen 1]
    2. [screen 2]
```

### Step 8: Generate Implementation Index
```
CREATE 04-implementation/IMPLEMENTATION_INDEX.md:
  # Implementation Index

  ## Quick Navigation

  | Phase | File | Status |
  |-------|------|--------|
  | 00 | [phase-00-setup.md](./sequence/phase-00-setup.md) | Ready |
  | 01 | [phase-01-auth.md](./sequence/phase-01-auth.md) | Ready |
  | 02 | [phase-02-catalog.md](./sequence/phase-02-catalog.md) | Ready |
  | 03 | [phase-03-core-crud.md](./sequence/phase-03-core-crud.md) | Ready |
  | 04 | [phase-04-transactional.md](./sequence/phase-04-transactional.md) | Ready |
  | 05 | [phase-05-lists-nav.md](./sequence/phase-05-lists-nav.md) | Ready |
  | 06 | [phase-06-details.md](./sequence/phase-06-details.md) | Ready |
  | 07 | [phase-07-dashboards.md](./sequence/phase-07-dashboards.md) | Ready |
  | 08 | [phase-08-workflows.md](./sequence/phase-08-workflows.md) | Ready |
  | 09 | [phase-09-integrations.md](./sequence/phase-09-integrations.md) | Ready |
  | 10 | [phase-10-polish.md](./sequence/phase-10-polish.md) | Ready |

  ---

  ## Checkpoints

  | Checkpoint | After Phase | File |
  |------------|-------------|------|
  | 1 | Phase 02 | [checkpoint-01-foundation.md](./checkpoints/checkpoint-01-foundation.md) |
  | 2 | Phase 05 | [checkpoint-02-core-functionality.md](./checkpoints/checkpoint-02-core-functionality.md) |
  | 3 | Phase 07 | [checkpoint-03-dashboards.md](./checkpoints/checkpoint-03-dashboards.md) |
  | 4 | Phase 10 | [checkpoint-04-production-ready.md](./checkpoints/checkpoint-04-production-ready.md) |

  ---

  ## Key Documents

  | Document | Purpose |
  |----------|---------|
  | [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) | Master implementation plan |
  | [MASTER_IMPL_PROMPT.md](./MASTER_IMPL_PROMPT.md) | Quick start guide |
  | [{APP}_IMPLEMENTATION_PLAN.md](./{APP}_IMPLEMENTATION_PLAN.md) | Per-app detailed plan |

  ---

  ## Phase Dependencies

  ```
  Phase 00 ─┬─> Phase 01 ─┬─> Phase 02 ─── CHECKPOINT 1
            │             │
            │             └─> Phase 03 ─┬─> Phase 04 ─┬─> Phase 05 ─── CHECKPOINT 2
            │                           │             │
            │                           └─────────────┘
            │
            └─────────────────────────────────────────────────┐
                                                              │
  Phase 06 ─┬─> Phase 07 ─── CHECKPOINT 3                    │
            │                                                 │
            └─────────────────────────────────────────────────┤
                                                              │
  Phase 08 ─┬─> Phase 09 ─┬─> Phase 10 ─── CHECKPOINT 4      │
            │             │               (Final)             │
            └─────────────┘                                   │
                                                              │
  All phases depend on Phase 00 ─────────────────────────────┘
  ```

  ---

  ## Component Build Order

  ### Foundation Components (Phase 01-02)
  [List components built in early phases]

  ### Core Components (Phase 03-05)
  [List P0 components with phase assignments]

  ### Visibility Components (Phase 06-07)
  [List dashboard/detail components]

  ### Workflow Components (Phase 08)
  [List workflow-specific components]

  ### Integration Components (Phase 09)
  [List integration components like CommandPalette, ShortcutsHelp]

  ### Polish Components (Phase 10)
  [List polish components like Skeleton, ErrorBoundary, SkipLink]

  ---

  ## Screen Build Order

  | Order | Screen | ID | Phase |
  |-------|--------|-----|-------|
  [Populate from traceability/screen_registry.json and phase assignments]

  ---

  ## Service Build Order

  | Order | Service | Phase |
  |-------|---------|-------|
  | 1 | Database (Dexie) | 02 |
  | 2 | {CoreService} | 03 |
  | 3 | EventBus | 04 |
  [Continue for all services]

  ---

  ## Hook Build Order

  | Order | Hook | Phase |
  |-------|------|-------|
  | 1 | useAuth | 01 |
  | 2 | use{Entity}s | 02 |
  [Continue for all hooks]

  ---

  ## P0 Requirements Traceability

  | Req ID | Component/Screen | Phase |
  |--------|------------------|-------|
  [Populate from _state/requirements_registry.json - P0 items only]

  ---

  ## Quick Commands

  ```bash
  # Start development
  npm run dev

  # Check types
  npx tsc --noEmit

  # Run tests
  npm test

  # Build for production
  npm run build

  # Run specific phase validation
  # (Replace XX with phase number)
  npm run validate:phase-XX
  ```
```

### Step 8.5: Generate Engineer-Ready Task Plans (Phase 3 Enhancement)

> **writing-plans Integration**: Generate bite-sized task plans for zero-context engineers.

```
// ═══════════════════════════════════════════════════════════
// PHASE 3: BITE-SIZED IMPLEMENTATION PLANS
// ═══════════════════════════════════════════════════════════

LOG: "Generating engineer-ready task plans..."

PLAN_PRINCIPLES:
  - Each step is ONE action (2-5 minutes)
  - Exact file paths always
  - Complete code in plan (not "add validation")
  - TDD: Write test → Run test (fail) → Implement → Run test (pass) → Commit
  - Exact commands with expected output

CREATE 04-implementation/plans/ directory

FOR each phase in sequence/:

  CREATE 04-implementation/plans/{phase-name}-tasks.md:

    # {Phase Name} Implementation Tasks

    > **For Claude:** Use executing-plans skill to implement these tasks in batches.

    **Goal:** {one sentence describing what this phase builds}

    **Architecture:** {2-3 sentences about approach}

    **Tech Stack:** React 18, TypeScript, Tailwind, Dexie

    ---

    ## Task 1: {First Component/Feature}

    **Files:**
    - Create: `prototype/src/components/{category}/{Component}.tsx`
    - Create: `prototype/src/components/{category}/__tests__/{Component}.test.tsx`

    **Step 1: Write the failing test**

    ```typescript
    // prototype/src/components/{category}/__tests__/{Component}.test.tsx
    import { render, screen } from '@testing-library/react';
    import { describe, it, expect } from 'vitest';
    import { {Component} } from '../{Component}';

    describe('{Component}', () => {
      it('renders with required props', () => {
        render(<{Component} label="Test" />);
        expect(screen.getByText('Test')).toBeInTheDocument();
      });

      it('handles click events', () => {
        const handleClick = vi.fn();
        render(<{Component} onClick={handleClick} />);
        fireEvent.click(screen.getByRole('button'));
        expect(handleClick).toHaveBeenCalledTimes(1);
      });
    });
    ```

    **Step 2: Run test to verify it fails**

    ```bash
    cd prototype && npm run test:run -- src/components/{category}/__tests__/{Component}.test.tsx
    ```

    Expected: FAIL with "Cannot find module '../{Component}'"

    **Step 3: Write minimal implementation**

    ```typescript
    // prototype/src/components/{category}/{Component}.tsx
    import React from 'react';

    interface {Component}Props {
      label: string;
      onClick?: () => void;
    }

    export const {Component}: React.FC<{Component}Props> = ({
      label,
      onClick
    }) => {
      return (
        <button onClick={onClick} className="...">
          {label}
        </button>
      );
    };
    ```

    **Step 4: Run test to verify it passes**

    ```bash
    cd prototype && npm run test:run -- src/components/{category}/__tests__/{Component}.test.tsx
    ```

    Expected: PASS (all tests green)

    **Step 5: Commit**

    ```bash
    git add prototype/src/components/{category}/{Component}.tsx prototype/src/components/{category}/__tests__/{Component}.test.tsx
    git commit -m "feat({category}): add {Component} component with tests"
    ```

    ---

    ## Task 2: {Second Component/Feature}

    **Files:**
    - Create: `prototype/src/components/{category}/{Component2}.tsx`
    - Create: `prototype/src/components/{category}/__tests__/{Component2}.test.tsx`

    [... same TDD pattern ...]

    ---

    ## Task N: Integration Test

    **Files:**
    - Create: `prototype/src/__tests__/{phase}-integration.test.tsx`

    **Step 1: Write integration test**

    ```typescript
    // Test that all components from this phase work together
    describe('{Phase} Integration', () => {
      it('all components render without errors', () => {
        // Render parent component that uses all phase components
      });

      it('data flows correctly between components', () => {
        // Test props passing and state management
      });
    });
    ```

    **Step 2: Run and verify**

    ```bash
    cd prototype && npm run test:run
    ```

    Expected: All tests pass

    **Step 3: Commit phase completion**

    ```bash
    git add .
    git commit -m "feat: complete {phase-name} implementation"
    ```

    ---

    ## Checkpoint Verification

    After completing all tasks:

    ```bash
    # Run all tests
    cd prototype && npm run test:run

    # Type check
    cd prototype && npx tsc --noEmit

    # Build
    cd prototype && npm run build

    # Start dev server and verify manually
    cd prototype && npm run dev
    ```

    **Expected Results:**
    - All tests pass
    - No TypeScript errors
    - Build succeeds
    - Dev server starts without errors

// Generate summary of all task plans
CREATE 04-implementation/plans/TASK_INDEX.md:
  # Implementation Task Index

  > **Execution:** Use Prototype_Builder with batch execution mode.

  ## Overview

  | Phase | Tasks | Est. Time | TDD Tests |
  |-------|-------|-----------|-----------|
  | phase-00-setup | 5 | 2 hours | 0 (setup) |
  | phase-01-auth | 4 | 3 hours | 8 |
  | phase-02-catalog | 6 | 2 hours | 12 |
  | phase-03-core-crud | 8 | 4 hours | 24 |
  | ... | ... | ... | ... |

  ## Execution Order

  1. [phase-00-setup-tasks.md](phase-00-setup-tasks.md) — Project scaffolding
  2. [phase-01-auth-tasks.md](phase-01-auth-tasks.md) — Authentication
  3. [phase-02-catalog-tasks.md](phase-02-catalog-tasks.md) — Reference data
  ...

  ## Principles

  - **DRY**: Don't repeat yourself
  - **YAGNI**: You aren't gonna need it
  - **TDD**: Test-driven development (Red → Green → Refactor)
  - **Frequent Commits**: Commit after each task

LOG: "✅ Generated {plan_count} bite-sized task plans"
```

### Step 9: Generate Helper Script
```
CREATE 04-implementation/generate_implementation_sequence.py:
  """
  Generate implementation sequence from specs.
  Analyzes dependencies and creates optimal order.
  """
  import json
  import os
  
  def analyze_dependencies():
      # Load data model for entity deps
      # Load screens for component deps
      pass
  
  def generate_sequence():
      # Create phase assignments
      pass
  
  if __name__ == '__main__':
      generate_sequence()
```

### Step 9.5: Generate Visual Roadmap (Phase 2 Enhancement)

> **Visual Documentation Integration**: Generate interactive HTML timeline for implementation roadmap.

```
CREATE 04-implementation/ROADMAP_VISUAL.html:

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Product Name} - Implementation Roadmap</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: system-ui, -apple-system, sans-serif;
      background: #1a1a2e;
      min-height: 100vh;
      padding: 40px;
      color: white;
    }
    .container { max-width: 1400px; margin: 0 auto; }
    h1 { font-size: 2.5rem; margin-bottom: 10px; }
    .subtitle { color: #888; margin-bottom: 40px; }

    .timeline { position: relative; padding: 20px 0; }

    .phase-group {
      margin-bottom: 40px;
      background: rgba(255,255,255,0.05);
      border-radius: 16px;
      padding: 24px;
    }
    .phase-group-header {
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 20px;
    }
    .checkpoint-badge {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
    }
    .phase-group-title {
      font-size: 1.5rem;
    }

    .phases-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;
    }

    .phase-card {
      background: rgba(255,255,255,0.08);
      border-radius: 12px;
      padding: 20px;
      transition: transform 0.2s, background 0.2s;
      cursor: pointer;
    }
    .phase-card:hover {
      transform: translateY(-4px);
      background: rgba(255,255,255,0.12);
    }
    .phase-number {
      font-size: 12px;
      color: #888;
      margin-bottom: 4px;
    }
    .phase-name {
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 8px;
    }
    .phase-description {
      font-size: 14px;
      color: #aaa;
      margin-bottom: 12px;
    }
    .phase-items {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .phase-item {
      background: rgba(255,255,255,0.1);
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 12px;
    }
    .phase-status {
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid rgba(255,255,255,0.1);
      display: flex;
      justify-content: space-between;
      font-size: 12px;
    }
    .status-planned { color: #888; }
    .status-in-progress { color: #f59e0b; }
    .status-complete { color: #48bb78; }

    .progress-bar {
      margin-top: 40px;
      background: rgba(255,255,255,0.1);
      border-radius: 8px;
      padding: 20px;
    }
    .progress-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 12px;
    }
    .progress-track {
      height: 8px;
      background: rgba(255,255,255,0.2);
      border-radius: 4px;
      overflow: hidden;
    }
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, #48bb78, #4299e1);
      border-radius: 4px;
      transition: width 0.5s ease;
    }
    .progress-phases {
      display: flex;
      justify-content: space-between;
      margin-top: 8px;
      font-size: 11px;
      color: #666;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>{Product Name} Implementation Roadmap</h1>
    <p class="subtitle">{phase_count} Phases • {checkpoint_count} Checkpoints • {requirement_count} Requirements</p>

    <div class="timeline">
      <!-- Checkpoint 1: Foundation -->
      <div class="phase-group">
        <div class="phase-group-header">
          <span class="checkpoint-badge">Checkpoint 1</span>
          <h2 class="phase-group-title">Foundation</h2>
        </div>
        <div class="phases-grid">
          <div class="phase-card">
            <div class="phase-number">Phase 00</div>
            <div class="phase-name">Setup</div>
            <div class="phase-description">Project scaffolding, tooling, base configuration</div>
            <div class="phase-items">
              <span class="phase-item">Vite</span>
              <span class="phase-item">React 18</span>
              <span class="phase-item">TypeScript</span>
              <span class="phase-item">Tailwind</span>
            </div>
            <div class="phase-status">
              <span class="status-planned">● Planned</span>
              <span>~2 hours</span>
            </div>
          </div>
          <div class="phase-card">
            <div class="phase-number">Phase 01</div>
            <div class="phase-name">Auth</div>
            <div class="phase-description">Authentication, session management</div>
            <div class="phase-items">
              <span class="phase-item">Login</span>
              <span class="phase-item">Session</span>
              <span class="phase-item">Routes</span>
            </div>
            <div class="phase-status">
              <span class="status-planned">● Planned</span>
              <span>~3 hours</span>
            </div>
          </div>
          <div class="phase-card">
            <div class="phase-number">Phase 02</div>
            <div class="phase-name">Catalog</div>
            <div class="phase-description">Reference data, lookups, enums</div>
            <div class="phase-items">
              <span class="phase-item">{CatalogEntity1}</span>
              <span class="phase-item">{CatalogEntity2}</span>
            </div>
            <div class="phase-status">
              <span class="status-planned">● Planned</span>
              <span>~2 hours</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Checkpoint 2: Core Functionality -->
      <div class="phase-group">
        <div class="phase-group-header">
          <span class="checkpoint-badge">Checkpoint 2</span>
          <h2 class="phase-group-title">Core Functionality</h2>
        </div>
        <div class="phases-grid">
          <div class="phase-card">
            <div class="phase-number">Phase 03</div>
            <div class="phase-name">Core CRUD</div>
            <div class="phase-description">Primary entity operations</div>
            <div class="phase-items">
              <span class="phase-item">{CoreEntity1}</span>
              <span class="phase-item">{CoreEntity2}</span>
            </div>
            <div class="phase-status">
              <span class="status-planned">● Planned</span>
              <span>~4 hours</span>
            </div>
          </div>
          <div class="phase-card">
            <div class="phase-number">Phase 04</div>
            <div class="phase-name">Transactional</div>
            <div class="phase-description">Events, activities, state changes</div>
            <div class="phase-items">
              <span class="phase-item">{TransactionalEntity1}</span>
            </div>
            <div class="phase-status">
              <span class="status-planned">● Planned</span>
              <span>~3 hours</span>
            </div>
          </div>
          <!-- Add more phases... -->
        </div>
      </div>

      <!-- Add more checkpoint groups... -->
    </div>

    <div class="progress-bar">
      <div class="progress-header">
        <span>Overall Progress</span>
        <span>0%</span>
      </div>
      <div class="progress-track">
        <div class="progress-fill" style="width: 0%"></div>
      </div>
      <div class="progress-phases">
        <span>Setup</span>
        <span>Auth</span>
        <span>Core</span>
        <span>UI</span>
        <span>Dashboard</span>
        <span>Polish</span>
      </div>
    </div>
  </div>
</body>
</html>

POPULATE template with actual phases and requirements
WRITE to 04-implementation/ROADMAP_VISUAL.html

LOG: "✅ Generated visual implementation roadmap"
```

### Step 10: Validate Outputs and Generate Report (REQUIRED)
```
VALIDATE implementation structure:
  DIRECTORY CHECKS:
    - sequence/ has phases 00-10 (11 files)
    - checkpoints/ has 4 checkpoint files
    - prompts/ has 11+ prompt files (one per phase + README)
    - IMPLEMENTATION_PLAN.md exists
    - MASTER_IMPL_PROMPT.md exists
    - IMPLEMENTATION_INDEX.md exists
    - ROADMAP_VISUAL.html exists

  CONTENT CHECKS:
    - All phases have requirements mapped
    - Checkpoints cover all P0 requirements
    - No circular dependencies
    - All screens assigned to phases
    - All P0 components assigned to phases

IF any validation fails:
  PROMPT with mitigation options

CREATE 04-implementation/SEQUENCER_VALIDATION_REPORT.md:
  # Sequencer Validation Report

  ---
  document_id: SEQ-VAL-001
  version: 1.0.0
  generated_at: {TIMESTAMP}
  ---

  ## Summary

  | Metric | Count | Status |
  |--------|-------|--------|
  | Total Phases | 11 | ✅ |
  | Total Checkpoints | 4 | ✅ |
  | Total Prompts | 11 | ✅ |
  | P0 Requirements | {count} | ✅/⚠️ |
  | P0 Coverage | {percent}% | ✅/⚠️ |
  | Screens Assigned | {count}/{total} | ✅/⚠️ |
  | Components Assigned | {count}/{total} | ✅/⚠️ |

  ## Phase Distribution

  | Phase | Components | Screens | Services | Hooks | P0 Reqs |
  |-------|------------|---------|----------|-------|---------|
  | 00 | 0 | 0 | 0 | 0 | 0 |
  | 01 | {n} | 0 | 0 | {n} | {n} |
  [... for all phases ...]

  ## Checkpoint Coverage

  ### Checkpoint 1: Foundation (After Phase 02)
  - [ ] Project scaffolded
  - [ ] Design tokens integrated
  - [ ] Base components implemented
  - P0 Requirements: {list}

  ### Checkpoint 2: Core Functionality (After Phase 05)
  - [ ] All core entities have CRUD
  - [ ] Primary screens functional
  - P0 Requirements: {list}

  ### Checkpoint 3: Dashboards (After Phase 07)
  - [ ] All persona dashboards render
  - [ ] Metrics display correctly
  - P0 Requirements: {list}

  ### Checkpoint 4: Production Ready (After Phase 10)
  - [ ] All P0 requirements addressed
  - [ ] QA validation passed
  - P0 Requirements: {list}

  ## Dependency Graph Validation

  ✅ No circular dependencies detected
  ✅ All dependencies resolvable
  ✅ Critical path identified

  ## Warnings

  [List any warnings or edge cases found during validation]

  ## Validation Passed

  - **Validator**: Prototype_Sequencer
  - **Timestamp**: {TIMESTAMP}
  - **Result**: PASS/FAIL
```

### Step 11: Update Progress
```
WRITE _state/implementation_sequence.json

UPDATE _state/progress.json:
  phases.sequencer.status = "complete"
  phases.sequencer.outputs = [
    "04-implementation/IMPLEMENTATION_PLAN.md",
    "04-implementation/IMPLEMENTATION_INDEX.md",
    "04-implementation/MASTER_IMPL_PROMPT.md",
    "04-implementation/sequence/phase-*.md",
    "04-implementation/checkpoints/checkpoint-*.md",
    "04-implementation/prompts/*.md"
  ]
  phases.sequencer.metrics = {
    total_phases: 11,
    total_checkpoints: 4,
    total_prompts: count,
    estimated_hours: sum
  }
```

---

## Output Files (REQUIRED)

| Path | Purpose | Blocking? |
|------|---------|-----------|
| `IMPLEMENTATION_PLAN.md` | Master plan | ✅ Yes |
| `IMPLEMENTATION_INDEX.md` | Navigation index | ✅ Yes |
| `MASTER_IMPL_PROMPT.md` | Master prompt for CodeGen | ✅ Yes |
| `SEQUENCER_VALIDATION_REPORT.md` | Validation report | ✅ Yes |
| `sequence/phase-00-setup.md` | Phase 00: Setup | ✅ Yes |
| `sequence/phase-01-auth.md` | Phase 01: Auth | ✅ Yes |
| `sequence/phase-02-catalog.md` | Phase 02: Catalog | ✅ Yes |
| `sequence/phase-03-core-crud.md` | Phase 03: Core CRUD | ✅ Yes |
| `sequence/phase-04-transactional.md` | Phase 04: Transactional | ✅ Yes |
| `sequence/phase-05-lists-nav.md` | Phase 05: Lists & Nav | ✅ Yes |
| `sequence/phase-06-details.md` | Phase 06: Details | ✅ Yes |
| `sequence/phase-07-dashboards.md` | Phase 07: Dashboards | ✅ Yes |
| `sequence/phase-08-workflows.md` | Phase 08: Workflows | ✅ Yes |
| `sequence/phase-09-integrations.md` | Phase 09: Integrations | ✅ Yes |
| `sequence/phase-10-polish.md` | Phase 10: Polish | ✅ Yes |
| `checkpoints/checkpoint-01-foundation.md` | After Phase 02 | ✅ Yes |
| `checkpoints/checkpoint-02-core-functionality.md` | After Phase 05 | ✅ Yes |
| `checkpoints/checkpoint-03-dashboards.md` | After Phase 07 | ✅ Yes |
| `checkpoints/checkpoint-04-production-ready.md` | After Phase 10 | ✅ Yes |
| `prompts/README.md` | Prompt index and usage | ✅ Yes |
| `prompts/00-setup-prompt.md` | Phase 00 prompt | ✅ Yes |
| `prompts/01-auth-layout-prompt.md` | Phase 01 prompt | ✅ Yes |
| `prompts/02-catalog-prompt.md` | Phase 02 prompt | ✅ Yes |
| `prompts/03-core-crud-prompt.md` | Phase 03 prompt | ✅ Yes |
| `prompts/04-transactional-prompt.md` | Phase 04 prompt | ✅ Yes |
| `prompts/05-lists-nav-prompt.md` | Phase 05 prompt | ✅ Yes |
| `prompts/06-details-prompt.md` | Phase 06 prompt | ✅ Yes |
| `prompts/07-dashboards-prompt.md` | Phase 07 prompt | ✅ Yes |
| `prompts/08-workflows-prompt.md` | Phase 08 prompt | ✅ Yes |
| `prompts/09-integrations-prompt.md` | Phase 09 prompt | ✅ Yes |
| `prompts/10-polish-prompt.md` | Phase 10 prompt | ✅ Yes |
| `{APP}_IMPLEMENTATION_PLAN.md` | Per-app plans | ⚠️ Warning |
| `plans/TASK_INDEX.md` | Bite-sized task index | ⚠️ Optional |
| `plans/phase-*-tasks.md` | Engineer-ready tasks | ⚠️ Optional |
| `ROADMAP_VISUAL.html` | Interactive timeline | ⚠️ Optional |
| `generate_implementation_sequence.py` | Helper script | ⚠️ Optional |

---

## Progress.json Update

```json
{
  "phases": {
    "sequencer": {
      "status": "complete",
      "completed_at": "2024-12-13T13:00:00Z",
      "outputs": [
        "04-implementation/IMPLEMENTATION_PLAN.md",
        "04-implementation/IMPLEMENTATION_INDEX.md",
        "04-implementation/MASTER_IMPL_PROMPT.md",
        "04-implementation/sequence/*.md",
        "04-implementation/checkpoints/*.md",
        "04-implementation/prompts/*.md"
      ],
      "metrics": {
        "total_phases": 11,
        "total_checkpoints": 4,
        "total_prompts": 5,
        "estimated_hours": 120
      }
    }
  }
}
```
