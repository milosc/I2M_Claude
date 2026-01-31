# Assembly-First Integration for Prototype_Components

> **CRITICAL**: This document OVERRIDES the standard component generation workflow in SKILL.md when Assembly-First mode is enabled.

## Version

- **Version**: 3.0.0
- **Updated**: 2026-01-02
- **Change**: Assembly-First component library integration

---

## New Workflow: Assembly-First Component Specifications

### Mode Detection

**BEFORE any component generation:**

```
1. Check if .claude/templates/component-library/ exists
2. Check if component-library/manifests/components.json exists
3. IF both exist:
   → ASSEMBLY_FIRST_MODE = true
   → Follow this document's workflow
4. ELSE:
   → ASSEMBLY_FIRST_MODE = false
   → Follow original SKILL.md workflow
```

---

## Assembly-First Procedure

When `ASSEMBLY_FIRST_MODE = true`, follow this procedure instead of the original SKILL.md:

### Step 0: Read Component Library (MANDATORY BLOCKING)

**This is the FIRST STEP. Do not proceed without completing it.**

```
// ========== BLOCKING READ OPERATIONS ==========
READ .claude/templates/component-library/manifests/components.json AS lib_components
READ .claude/templates/component-library/SKILL.md AS lib_protocol
READ .claude/templates/component-library/INTERACTIONS.md AS lib_interactions

VERIFY:
  - lib_components exists and is valid JSON
  - lib_components.components has at least 50 entries
  - lib_protocol contains "Strict Usage Protocol" section

IF any verification fails:
  LOG ERROR: "Component library invalid or incomplete"
  FALLBACK to standard SKILL.md workflow

ELSE:
  LOG: "✅ Component library loaded: {lib_components.components.length} components available"

STORE:
  - lib_components (registry of available components)
  - lib_protocol (LLM usage rules)
  - lib_interactions (state patterns)
// =============================================
```

### Step 1: Validate Inputs (Same as Original)

```
READ 00-foundation/DESIGN_BRIEF.md
READ 00-foundation/DESIGN_TOKENS.md
READ 00-foundation/colors.md
READ 00-foundation/typography.md
READ 00-foundation/spacing-layout.md
READ _state/requirements_registry.json
READ discovery/04-design-specs/screen-definitions.md

IDENTIFY requirements this skill MUST address:
  - A11Y-001: Keyboard navigation (library handles this)
  - A11Y-003: Focus indicators (library handles this)
  - A11Y-004: Form labels (library handles this)
  - FR-XXX: Functional requirements related to UI controls
```

### Step 2: Map Discovery Requirements to Library Components

```
// ========== REQUIREMENT → COMPONENT MAPPING ==========
SCAN screen-definitions.md for UI elements mentioned

FOR each UI element requirement:

  SEARCH lib_components for matching component:

    "text input" → TextField (Forms)
    "password field" → TextField with type="password" (Forms)
    "dropdown" → Select or ComboBox (Pickers)
    "searchable dropdown" → Autocomplete or ComboBox (Pickers)
    "checkbox" → Checkbox (Forms)
    "radio buttons" → RadioGroup (Forms)
    "toggle" → Switch (Forms)
    "number input" → NumberField (Forms)
    "date picker" → DatePicker (Date & Time)
    "data table" → Table (Collections)
    "list" → ListBox or GridList (Collections)
    "menu" → Menu (Collections)
    "button" → Button (Buttons)
    "file upload" → FileTrigger (Buttons)
    "tabs" → Tabs (Navigation)
    "breadcrumb" → Breadcrumbs (Navigation)
    "modal/dialog" → Dialog or Modal (Overlays)
    "tooltip" → Tooltip (Overlays)
    "popover" → Popover (Overlays)
    "loading bar" → ProgressBar (Status)
    "status badge" → Badge (Status)

  RECORD:
    requirement_id → library_component mapping

CREATE component_mapping.json:
  {
    "mapped_to_library": [
      {"requirement": "FR-005", "component": "TextField", "category": "Forms"},
      {"requirement": "FR-007", "component": "Table", "category": "Collections"},
      ...
    ],
    "needs_aggregate": [
      {"requirement": "FR-015", "reason": "Combines Avatar + Badge + Text"},
      ...
    ]
  }
// ===================================================
```

### Step 3: Identify Aggregate Components Only

**KEY CHANGE**: Instead of generating ALL components, only generate aggregates.

```
// ========== AGGREGATE IDENTIFICATION ==========
AGGREGATE_NEEDED = false

FOR each unique UI pattern in screen-definitions.md:

  IF pattern combines 2+ library components with custom logic:
    → Mark as aggregate_needed

  EXAMPLES of valid aggregates:
    ✅ "UserProfileCard": Combines Avatar + Heading + Text + Badge + Button
    ✅ "TaskListItem": Combines Checkbox + Text + Menu + Button
    ✅ "KPICard": Combines Meter + Heading + Text + custom calculation logic
    ✅ "SearchBar": Combines SearchField + Popover + ListBox with API integration

  EXAMPLES of INVALID aggregates (use library instead):
    ❌ "CustomButton" → Use library Button
    ❌ "DataGrid" → Use library Table
    ❌ "FormInput" → Use library TextField
    ❌ "DropdownMenu" → Use library Menu

GENERATE aggregate_components_list[]

IF aggregate_components_list.length == 0:
  LOG: "No aggregate components needed - all requirements met by library"

ELSE:
  LOG: "Identified {count} aggregate components to specify"
  FOR each aggregate in aggregate_components_list:
    LOG: "  - {aggregate.name}: {aggregate.reason}"
// ==============================================
```

### Step 4: Generate Library Component Reference

**Instead of re-specifying library components, create a reference document:**

```
// ========== LIBRARY COMPONENTS REFERENCE ==========
CREATE 01-components/library-components/LIBRARY_REFERENCE.md:
  ---
  document_id: COMP-LIB-REF
  version: 1.0.0
  created_at: {DATE}
  updated_at: {DATE}
  generated_by: Prototype_Components (Assembly-First Mode)
  source_files:
    - .claude/templates/component-library/manifests/components.json
    - .claude/templates/component-library/SKILL.md
  ---

  # Component Library Reference

  This prototype uses the **Assembly-First Component Library** located at:
  `.claude/templates/component-library/`

  ## Available Components ({lib_components.components.length} total)

  ### Forms (10 components)
  | Component | Category | Path | Requirements |
  |-----------|----------|------|--------------|
  | TextField | Forms | src/TextField/ | FR-005, A11Y-001, A11Y-004 |
  | Checkbox | Forms | src/Checkbox/ | FR-008, A11Y-001 |
  ...

  ### Collections (8 components)
  | Component | Category | Path | Requirements |
  |-----------|----------|------|--------------|
  | Table | Collections | src/Table/ | FR-007, A11Y-001 |
  | ListBox | Collections | src/ListBox/ | FR-012, A11Y-001 |
  ...

  ### [Continue for all categories]

  ## Usage Protocol

  **MANDATORY**: All prototype code MUST follow the usage protocol in:
  `.claude/templates/component-library/SKILL.md`

  ### Import Pattern
  ```tsx
  import { Button, TextField, Form } from '@/component-library';
  ```

  ### Accessibility
  All library components handle accessibility automatically:
  - ✅ A11Y-001 (Keyboard navigation) - Built-in
  - ✅ A11Y-003 (Focus indicators) - Built-in
  - ✅ A11Y-004 (Form labels) - Built-in via Label component

  **Do NOT add manual ARIA attributes.**

  ### State Management
  Use render props for state-driven styling:
  ```tsx
  <Button
    className={({ isPressed, isHovered }) =>
      `px-4 py-2 ${isPressed ? 'bg-accent-active' : 'bg-accent-default'}`
    }
  >
    Click Me
  </Button>
  ```

  ### Design Tokens
  Use Tailwind theme tokens from `tailwind.config.js`:
  - Colors: `bg-surface-1`, `text-primary`, `accent-default`, `border-subtle`
  - Shadows: `shadow-subtle`, `shadow-medium`, `shadow-overlay`
  - Radius: `rounded-sm`, `rounded-md`, `rounded-lg`

  ## Component Mapping

  | Discovery Requirement | Library Component | Category |
  |-----------------------|-------------------|----------|
  FOR each mapping in component_mapping.json:
    | {requirement_id}: {description} | {component} | {category} |

  ## Documentation

  - **API Specs**: `.claude/templates/component-library/src/{Component}/{Component}.tsx`
  - **Examples**: `.claude/templates/component-library/stories/{Component}.stories.tsx`
  - **Storybook**: Run `npm run storybook` in component-library directory

  ---
  *This prototype uses Assembly-First approach - library components are NOT re-specified here.*
  *See `.claude/templates/component-library/` for full component documentation.*

SAVE to 01-components/library-components/LIBRARY_REFERENCE.md
// ===================================================
```

### Step 5: Generate Aggregate Component Specs Only

**ONLY generate specs for identified aggregates:**

```
// ========== AGGREGATE COMPONENT GENERATION ==========
FOR each aggregate in aggregate_components_list:

  // ========== PROMPT LOG: BEFORE ==========
  READ _state/prompt_log.json AS log
  next_id = "PL-" + String(log.summary.total_entries + 1).padStart(3, '0')

  LOG entry with:
    id: next_id
    skill: "Prototype_Components"
    step: "Step 5: Generate Aggregate Component"
    category: "generation"
    desired_outcome: "Generate {aggregate.name} specification"
    inputs: [
      "01-components/library-components/LIBRARY_REFERENCE.md",
      "discovery/04-design-specs/screen-definitions.md"
    ]
    target: "01-components/aggregates/{aggregate.name}.md"

  WRITE log
  // ========================================

  // ========== GENERATE AGGREGATE SPEC ==========
  CREATE 01-components/aggregates/{aggregate.name}.md:
    ---
    document_id: COMP-AGG-{AGGREGATE_NAME}
    version: 1.0.0
    created_at: {DATE}
    updated_at: {DATE}
    generated_by: Prototype_Components (Assembly-First Mode)
    type: aggregate_component
    source_files:
      - 01-components/library-components/LIBRARY_REFERENCE.md
      - discovery/04-design-specs/screen-definitions.md
    change_history:
      - version: "1.0.0"
        date: "{DATE}"
        author: "Prototype_Components"
        changes: "Initial generation"
    ---

    # {Aggregate Component Name}

    ## Type: Aggregate Component

    This is a **custom aggregate component** that combines multiple library components
    with domain-specific business logic.

    ## Requirements Addressed
    | Req ID | Description | Implementation |
    |--------|-------------|----------------|
    | {req_id} | {description} | {how_this_aggregate_addresses_it} |

    ## Composition

    This component combines the following library components:
    | Library Component | Category | Purpose in Aggregate |
    |-------------------|----------|----------------------|
    | {Component1} | {category} | {purpose} |
    | {Component2} | {category} | {purpose} |
    ...

    ## Business Logic

    {Describe the custom logic that justifies this aggregate}

    ## Data Shape

    ```typescript
    interface {AggregateName}Props {
      // Props definition
    }
    ```

    ## Visual Treatment

    > **Aesthetic**: {aesthetic_direction from 00-foundation/AESTHETIC_DIRECTION.md}

    ### Layout
    - Composition: {how_library_components_are_arranged}
    - Spacing: {spacing_values}

    ### States
    | State | Visual Changes | Library Components Affected |
    |-------|----------------|------------------------------|
    | Default | ... | ... |
    | Hover | ... | Button (isHovered) |
    | Loading | ... | ProgressBar (isIndeterminate) |

    ## Usage Example

    ```tsx
    import { {AggregateName} } from '@/components/aggregates';
    import { {LibComponent1}, {LibComponent2} } from '@/component-library';

    // Aggregate wraps library components with custom logic
    <{AggregateName}
      {props}
    />
    ```

    ## Implementation Notes

    - Uses library components for UI primitives
    - Adds custom business logic for {specific_behavior}
    - Follows Assembly-First rule: no raw HTML elements

    ---
    *This aggregate component follows Assembly-First principles.*
    *See LIBRARY_REFERENCE.md for underlying component documentation.*

  SAVE to 01-components/aggregates/{aggregate.name}.md
  // =============================================

  // ========== PROMPT LOG: AFTER ==========
  UPDATE log entry result: {
    "status": "success",
    "output_summary": "Generated {aggregate.name} with {N} library components"
  }
  WRITE log
  // ========================================
// ====================================================
```

### Step 6: Generate Component Library Summary (Assembly-First Version)

```
// ========== ASSEMBLY-FIRST SUMMARY ==========
CREATE 01-components/COMPONENT_LIBRARY_SUMMARY.md:
  ---
  document_id: COMP-SUMMARY
  version: 1.0.0
  created_at: {DATE}
  mode: assembly_first
  ---

  # Component Library Summary (Assembly-First)

  ## Overview

  This prototype uses the **Assembly-First** approach:
  - **Library Components**: {lib_components.components.length} pre-built accessible components
  - **Aggregate Components**: {aggregate_components_list.length} custom composites
  - **Total Available**: {lib_components.components.length + aggregate_components_list.length}

  ## Library Components (Pre-Built)

  | Category | Count | Components |
  |----------|-------|------------|
  | Forms | 10 | TextField, Checkbox, RadioGroup, Switch, ... |
  | Collections | 8 | Table, ListBox, GridList, Menu, ... |
  | Buttons | 4 | Button, ActionGroup, FileTrigger, ToggleButton |
  | Pickers | 3 | Autocomplete, ComboBox, Select |
  | Date & Time | 3 | Calendar, DateField, DatePicker |
  | Navigation | 3 | Breadcrumbs, Link, Tabs |
  | Overlays | 4 | Dialog, Modal, Popover, Tooltip |
  | Status | 4 | Badge, Meter, ProgressBar, StatusLight |
  | Layout | 8 | Disclosure, Flex, Grid, Group, ... |
  | Content | 4 | Header, Heading, Text, IllustratedMessage |
  | Color | 6 | ColorArea, ColorField, ColorPicker, ... |
  | Drag & Drop | 1 | DropZone |

  **Total Library Components**: {count}

  See: `01-components/library-components/LIBRARY_REFERENCE.md`

  ## Aggregate Components (Custom)

  | Component | Combines | Requirements | File |
  |-----------|----------|--------------|------|
  FOR each aggregate:
    | {name} | {library_components} | {requirement_ids} | {file_path} |

  **Total Aggregate Components**: {aggregate_components_list.length}

  ## Requirements Coverage

  | Req ID | Type | Addressed By |
  |--------|------|--------------|
  | A11Y-001 | Accessibility | Library (100% coverage) |
  | A11Y-003 | Accessibility | Library (100% coverage) |
  | A11Y-004 | Accessibility | Library (100% coverage) |
  FOR each functional requirement:
    | {req_id} | Functional | {library_component OR aggregate_component} |

  ## Token Savings

  **Assembly-First Efficiency:**
  - Library components: ~50 tokens per usage (vs ~800 traditional)
  - Token savings: ~15x per component
  - Total estimated savings: ~{calculate_savings} tokens

  ## Usage Protocol

  **MANDATORY** for all prototype code generation:
  1. ✅ Import from component library: `import { Button } from '@/component-library'`
  2. ✅ Use library components for ALL UI elements
  3. ✅ Only create aggregates when combining multiple components
  4. ❌ FORBIDDEN: Raw HTML elements (`<button>`, `<input>`, etc.)
  5. ❌ FORBIDDEN: Manual ARIA attributes
  6. ❌ FORBIDDEN: Custom CSS for component internals

  See: `.claude/commands/_assembly_first_rules.md` for complete rules

  ## Component Index

  ### Library Components
  - [Full Reference](./library-components/LIBRARY_REFERENCE.md)
  - [API Specs](./.claude/templates/component-library/src/)
  - [Examples](./.claude/templates/component-library/stories/)

  ### Aggregate Components
  FOR each aggregate:
    - [{aggregate.name}](./aggregates/{aggregate.name}.md)

  ---
  *Generated in Assembly-First mode*
  *Library components are NOT duplicated - see LIBRARY_REFERENCE.md*

SAVE to 01-components/COMPONENT_LIBRARY_SUMMARY.md
// ============================================
```

### Step 7: Update Traceability (ROOT-level)

```
// ========== ROOT-LEVEL TRACEABILITY ==========
BUILD component_registry:
  {
    "schema_version": "1.0.0",
    "stage": "Prototype",
    "checkpoint": 8,
    "mode": "assembly_first",
    "source_folder": "01-components/",
    "library_path": ".claude/templates/component-library/",
    "created_at": "{timestamp}",
    "updated_at": "{timestamp}",
    "traceability_chain": {
      "upstream": ["requirements_registry.json", "screen_registry.json"],
      "downstream": ["module_registry.json", "test_case_registry.json"]
    },
    "library_components": [
      FOR each component in lib_components.components:
        {
          "id": "COMP-LIB-{CATEGORY}-{NAME}",
          "name": "{name}",
          "category": "{category}",
          "source": "component-library",
          "path": ".claude/templates/component-library/src/{name}/",
          "requirement_refs": ["{req_ids from mapping}"],
          "a11y_built_in": true
        }
    ],
    "aggregate_components": [
      FOR each aggregate in aggregate_components_list:
        {
          "id": "COMP-AGG-{NAME}",
          "name": "{name}",
          "type": "aggregate",
          "file_path": "01-components/aggregates/{name}.md",
          "combines": ["{library_component_ids}"],
          "requirement_refs": ["{req_ids}"],
          "business_logic": "{description}"
        }
    ],
    "summary": {
      "library_components": {lib_components.components.length},
      "aggregate_components": {aggregate_components_list.length},
      "total_available": {sum},
      "a11y_coverage": "100% (library built-in)",
      "token_savings": "~15x per component"
    }
  }

WRITE traceability/component_registry.json

// Update requirements registry with component links
READ traceability/requirements_registry.json AS req_reg

FOR each library_component in component_registry.library_components:
  FOR each req_id in library_component.requirement_refs:
    FIND requirement WHERE id == req_id
    APPEND library_component.id TO requirement.component_refs

FOR each aggregate in component_registry.aggregate_components:
  FOR each req_id in aggregate.requirement_refs:
    FIND requirement WHERE id == req_id
    APPEND aggregate.id TO requirement.component_refs

WRITE traceability/requirements_registry.json
// =============================================
```

### Step 8: Validation

```
// ========== ASSEMBLY-FIRST VALIDATION ==========
VALIDATE:
  CHECKS:
    - ✅ Library reference document exists
    - ✅ Component library manifest was read
    - ✅ All Discovery UI requirements mapped to library or aggregates
    - ✅ Aggregate components justify why they're not library components
    - ✅ No library components re-specified (no duplication)
    - ✅ traceability/component_registry.json exists
    - ✅ Requirements registry updated with component links

  IF any check fails:
    LOG ERROR with details
    ADD to FAILURES_LOG.md

  ELSE:
    LOG: "✅ Assembly-First component specifications complete"
// ================================================
```

### Step 9: Update Progress

```
UPDATE _state/progress.json:
  phases.components.status = "complete"
  phases.components.mode = "assembly_first"
  phases.components.completed_at = timestamp
  phases.components.outputs = [
    "01-components/library-components/LIBRARY_REFERENCE.md",
    "01-components/aggregates/*.md",
    "01-components/COMPONENT_LIBRARY_SUMMARY.md"
  ]
  phases.components.metrics = {
    library_components: {lib_components.components.length},
    aggregate_components: {aggregate_components_list.length},
    total_available: {sum},
    requirements_addressed: {count},
    token_savings: "~15x",
    prompts_logged: {count}
  }
```

---

## Output Structure (Assembly-First Mode)

```
01-components/
├── COMPONENT_LIBRARY_SUMMARY.md      # Assembly-First summary
├── library-components/
│   └── LIBRARY_REFERENCE.md          # Reference to component library
└── aggregates/
    ├── UserProfileCard.md            # Custom aggregate
    ├── TaskListItem.md               # Custom aggregate
    └── KPICard.md                    # Custom aggregate
```

**Key Difference**: No duplication of library components. Only aggregates are specified.

---

## Comparison: Traditional vs Assembly-First

| Aspect | Traditional Mode | Assembly-First Mode |
|--------|------------------|---------------------|
| **Components Generated** | All ~50 components | Only aggregates (~5-10) |
| **Library Components** | Re-specified | Referenced only |
| **Accessibility** | Must specify manually | Built-in to library |
| **Token Usage** | ~800 per component | ~50 per component (15x savings) |
| **Specification Files** | ~50 files | ~10 files |
| **Maintenance** | Duplicate specs | Single source of truth |
| **Consistency** | Varies per generation | Guaranteed (library) |

---

## Backward Compatibility

If `.claude/templates/component-library/` does NOT exist:
- Fall back to traditional SKILL.md workflow
- Generate all component specifications
- No assembly-first benefits

---

## Related Documentation

- **Architecture**: `architecture/Assembly-First Design System/ASSEMBLY_FIRST_ARCHITECTURE.md`
- **Rule**: `.claude/commands/_assembly_first_rules.md`
- **Component Library**: `.claude/templates/component-library/`
- **Original Skill**: `SKILL.md` (fallback workflow)
