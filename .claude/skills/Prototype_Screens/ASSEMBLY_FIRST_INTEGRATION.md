# Assembly-First Integration for Prototype_Screens

> **CRITICAL**: This document OVERRIDES the standard screen generation workflow when Assembly-First mode is enabled.

## Version

- **Version**: 3.0.0
- **Updated**: 2026-01-02
- **Change**: Assembly-First component library integration for screen specifications

---

## New Workflow: Assembly-First Screen Specifications

### Mode Detection

**BEFORE any screen generation:**

```
1. Check if 01-components/COMPONENT_LIBRARY_SUMMARY.md exists
2. Check if mode == "assembly_first" in summary
3. Check if 01-components/library-components/LIBRARY_REFERENCE.md exists
4. IF all exist:
   → ASSEMBLY_FIRST_MODE = true
   → Follow this document's workflow
5. ELSE:
   → ASSEMBLY_FIRST_MODE = false
   → Follow original SKILL.md workflow
```

---

## Assembly-First Procedure

When `ASSEMBLY_FIRST_MODE = true`, follow this procedure:

### Step 0: Read Component Library Reference (MANDATORY BLOCKING)

```
// ========== BLOCKING READ OPERATIONS ==========
READ 01-components/library-components/LIBRARY_REFERENCE.md AS lib_ref
READ 01-components/COMPONENT_LIBRARY_SUMMARY.md AS comp_summary
READ .claude/templates/component-library/INTERACTIONS.md AS lib_interactions
READ .claude/commands/_assembly_first_rules.md AS assembly_rules

VERIFY:
  - lib_ref exists and contains component mapping table
  - comp_summary.mode == "assembly_first"
  - lib_interactions contains state patterns
  - assembly_rules contains forbidden practices

IF any verification fails:
  LOG ERROR: "Assembly-First components not properly initialized"
  BLOCK: "Run Prototype_Components first"

ELSE:
  LOG: "✅ Assembly-First mode enabled for screens"

EXTRACT from lib_ref:
  - available_library_components[] (62 components)
  - available_aggregates[] (custom components)
  - component_mapping{} (requirement → component)

STORE for use in screen generation
// =============================================
```

### Step 1: Load Discovery Screens and Requirements

```
// ========== LOAD DISCOVERY OUTPUTS ==========
READ discovery/04-design-specs/screen-definitions.md AS screen_defs
READ discovery/04-design-specs/data-fields.md AS data_fields
READ discovery/04-design-specs/navigation-structure.md AS navigation
READ discovery/04-design-specs/interaction-patterns.md AS interactions
READ _state/requirements_registry.json AS req_reg
READ traceability/screen_registry.json AS screen_reg

PARSE screen_defs to extract:
  FOR each screen (S-X.X):
    - screen_id
    - screen_name
    - description
    - ui_elements[] (buttons, inputs, tables, etc.)
    - user_interactions[] (click, submit, search, etc.)
    - data_requirements[] (entities, fields)

PARSE data_fields to extract:
  - field_definitions{} (field_name → type, validation)

PARSE navigation to extract:
  - route_structure{}
  - navigation_patterns{}

PARSE interactions to extract:
  - interaction_patterns{} (hover, focus, validation, etc.)

CREATE discovery_screens_list[]
// ============================================
```

### Step 2: Map Each Screen to Library Components

```
// ========== SCREEN → COMPONENT MAPPING ==========
FOR each screen in discovery_screens_list:

  screen_components = []

  FOR each ui_element in screen.ui_elements:

    // Search library components first
    library_match = SEARCH available_library_components WHERE:
      ui_element.type matches component.category OR
      ui_element.description matches component.use_case

    IF library_match:
      ADD to screen_components:
        {
          "source": "library",
          "component": library_match.name,
          "category": library_match.category,
          "usage": ui_element.description,
          "props": {infer_props_from_element}
        }

    ELSE:
      // Check if aggregate component exists
      aggregate_match = SEARCH available_aggregates WHERE:
        ui_element.description matches aggregate.purpose

      IF aggregate_match:
        ADD to screen_components:
          {
            "source": "aggregate",
            "component": aggregate_match.name,
            "usage": ui_element.description,
            "props": {infer_props_from_element}
          }

      ELSE:
        LOG WARNING: "No component match for: {ui_element.description}"
        ADD to unmatched_elements[]

  STORE screen_components for this screen

IF unmatched_elements.length > 0:
  PROMPT user:
    ═══════════════════════════════════════════════════════
    ⚠️  UNMATCHED UI ELEMENTS
    ═══════════════════════════════════════════════════════

    The following UI elements have no component match:
    FOR each unmatched:
      - {unmatched.description} (Screen: {screen_id})

    Options:
    1. "library: [Component]" - Use existing library component
    2. "aggregate: [Name]" - Create new aggregate component
    3. "skip" - Proceed without (not recommended)
    ═══════════════════════════════════════════════════════

  WAIT for user response
  UPDATE screen_components accordingly
// ================================================
```

### Step 3: Generate Screen Specifications with Component Composition

```
// ========== GENERATE ASSEMBLY-FIRST SCREEN SPECS ==========
FOR each screen in discovery_screens_list:

  screen_slug = slugify(screen.name)

  // ========== PROMPT LOG: BEFORE ==========
  READ _state/prompt_log.json AS log
  next_id = "PL-" + String(log.summary.total_entries + 1).padStart(3, '0')

  LOG entry with:
    id: next_id
    skill: "Prototype_Screens"
    step: "Step 3: Generate Assembly-First Screen Spec"
    category: "generation"
    desired_outcome: "Generate screen spec using library components"
    inputs: [
      "01-components/library-components/LIBRARY_REFERENCE.md",
      "discovery/04-design-specs/screen-definitions.md"
    ]
    target: "02-screens/{screen_slug}/specification.md"

  WRITE log
  // ========================================

  // ========== CREATE SCREEN FOLDER ==========
  CREATE directory: 02-screens/{screen_slug}/
  // ==========================================

  // ========== GENERATE SPECIFICATION ==========
  CREATE 02-screens/{screen_slug}/specification.md:
    ---
    document_id: SCR-SPEC-{SCREEN_ID}
    screen_id: {screen.id}
    version: 1.0.0
    created_at: {DATE}
    updated_at: {DATE}
    generated_by: Prototype_Screens (Assembly-First Mode)
    mode: assembly_first
    source_files:
      - discovery/04-design-specs/screen-definitions.md
      - 01-components/library-components/LIBRARY_REFERENCE.md
    change_history:
      - version: "1.0.0"
        date: "{DATE}"
        author: "Prototype_Screens"
        changes: "Initial generation (Assembly-First)"
    ---

    # {Screen Name} - Specification

    ## Discovery Reference

    - **Screen ID**: {screen.id}
    - **Discovery**: {screen.discovery_reference}
    - **JTBD**: {screen.jtbd_refs}
    - **Persona**: {screen.persona_refs}

    ## Overview

    {screen.description}

    ## Component Composition (Assembly-First)

    This screen is composed using the **Assembly-First Component Library**.

    ### Library Components Used

    | Component | Category | Source | Purpose | Props |
    |-----------|----------|--------|---------|-------|
    FOR each comp in screen_components WHERE source == "library":
      | {comp.component} | {comp.category} | component-library | {comp.usage} | {comp.props} |

    ### Aggregate Components Used

    | Component | Combines | Source | Purpose | Props |
    |-----------|----------|--------|---------|-------|
    FOR each comp in screen_components WHERE source == "aggregate":
      | {comp.component} | {comp.combines} | 01-components/aggregates/ | {comp.usage} | {comp.props} |

    ## Layout Structure

    ```
    {Screen Container}
    ├── {Section1}
    │   ├── {Component1} (library: {name})
    │   ├── {Component2} (library: {name})
    │   └── {Component3} (aggregate: {name})
    ├── {Section2}
    │   └── {Component4} (library: {name})
    └── {Section3}
        └── ...
    ```

    ## Component Integration Code Outline

    ```tsx
    // Imports from component library
    import {
      FOR each library_component in screen_components:
        {library_component.name},
    } from '@/component-library';

    // Imports of aggregate components
    import {
      FOR each aggregate_component in screen_components:
        {aggregate_component.name},
    } from '@/components/aggregates';

    // Imports for data fetching
    import { useQuery } from '@tanstack/react-query';
    import { api } from '@/api';

    export function {ScreenName}() {
      // Data fetching logic (glue code)
      const { data, isLoading, error } = useQuery({
        queryKey: ['{entity}'],
        queryFn: () => api.{entity}.list()
      });

      // Loading state
      if (isLoading) {
        return <ProgressBar aria-label="Loading..." isIndeterminate />;
      }

      // Error state
      if (error) {
        return <Alert variant="danger">{error.message}</Alert>;
      }

      // Main UI composition
      return (
        <div className="flex flex-col gap-6 p-8">
          {/* Header Section */}
          <div className="flex items-center justify-between">
            <Heading level={1}>{screen.title}</Heading>
            <Button onPress={handleAction}>
              {action_label}
            </Button>
          </div>

          {/* Main Content - Compose library components */}
          FOR each section in screen.layout:
            <div className="{section.layout_classes}">
              FOR each component in section.components:
                IF component.source == "library":
                  <{component.name}
                    {...component.props}
                    data={data_binding}
                  >
                    {component.children}
                  </{component.name}>
                ELSE IF component.source == "aggregate":
                  <{component.name}
                    {...component.props}
                    data={data_binding}
                  />
            </div>
        </div>
      );
    }
    ```

    ## Data Requirements

    ### API Endpoints
    | Endpoint | Method | Purpose | Response Shape |
    |----------|--------|---------|----------------|
    FOR each api_call in screen.data_requirements:
      | {endpoint} | {method} | {purpose} | {response_shape} |

    ### State Management
    | State Variable | Type | Source | Purpose |
    |----------------|------|--------|---------|
    FOR each state in screen.state_requirements:
      | {var_name} | {type} | {source} | {purpose} |

    ## User Interactions

    | Action | Trigger | Component | Handler | Outcome |
    |--------|---------|-----------|---------|---------|
    FOR each interaction in screen.interactions:
      | {action} | {trigger} | {component} | {handler} | {outcome} |

    ## Interaction Patterns (from Component Library)

    ### State-Driven Styling
    Use render props from library components:
    ```tsx
    <Button
      className={({ isPressed, isHovered, isPending }) =>
        `px-4 py-2 ${isPressed ? 'bg-accent-active' : 'bg-accent-default'}
         ${isPending ? 'opacity-50' : ''}`
      }
      isPending={isSubmitting}
    >
      {isSubmitting ? 'Submitting...' : 'Submit'}
    </Button>
    ```

    ### Async Data Handling
    ```tsx
    // Library components handle loading states
    <Table
      aria-label="{table_label}"
      loadingState={isLoading ? 'loading' : 'idle'}
    >
      ...
    </Table>
    ```

    ### Form Validation
    ```tsx
    <Form validationErrors={errors}>
      <TextField
        name="email"
        validationState={errors.email ? 'invalid' : 'valid'}
        className="flex flex-col gap-1"
      >
        <Label>Email</Label>
        <Input />
        {errors.email && <FieldError>{errors.email}</FieldError>}
      </TextField>
    </Form>
    ```

    ## Accessibility (Handled by Library)

    ✅ **Library components provide:**
    - Keyboard navigation (A11Y-001) - Tab, Enter, Escape
    - Focus management (A11Y-003) - Focus rings, focus restoration
    - ARIA attributes - Automatic role, aria-label, aria-describedby
    - Screen reader support - Live regions, announcements

    **No manual ARIA required.**

    ## Responsive Behavior

    Use Tailwind responsive utilities with library components:
    ```tsx
    <div className="flex flex-col md:flex-row gap-4">
      <TextField className="w-full md:w-1/2" />
      <TextField className="w-full md:w-1/2" />
    </div>
    ```

    ## Navigation

    - **Route**: `{screen.route}`
    - **Parent**: `{screen.parent_screen}`
    - **Children**: `{screen.child_screens}`

    ## Related Screens

    FOR each related_screen:
      - [{related_screen.name}](../{related_screen.slug}/specification.md)

    ## Requirements Addressed

    | Req ID | Description | Component | Implementation |
    |--------|-------------|-----------|----------------|
    FOR each req in screen.requirements:
      | {req.id} | {req.description} | {component_addressing} | {how_implemented} |

    ---
    **Assembly-First Mode**: This specification composes pre-built library components.
    **No raw HTML elements** will be used in implementation.
    **See**: `.claude/commands/_assembly_first_rules.md` for implementation rules.

  SAVE to 02-screens/{screen_slug}/specification.md
  // =============================================

  // ========== GENERATE COMPONENT USAGE DOC ==========
  CREATE 02-screens/{screen_slug}/component-usage.md:
    ---
    document_id: SCR-COMP-{SCREEN_ID}
    screen_id: {screen.id}
    version: 1.0.0
    type: component_usage_guide
    ---

    # {Screen Name} - Component Usage Guide

    ## Library Components Reference

    This screen uses {count} library components and {count} aggregates.

    ### Detailed Usage

    FOR each component in screen_components:

      ### {component.name} ({component.category})

      **Source**: {component.source == "library" ? "Component Library" : "Aggregate"}
      **Path**: {component.path}

      #### Purpose in This Screen
      {component.usage}

      #### Props Configuration
      ```tsx
      <{component.name}
        FOR each prop in component.props:
          {prop.name}={prop.value}
      />
      ```

      #### State Patterns
      IF component has state patterns:
        ```tsx
        <{component.name}
          className={({ {render_states} }) =>
            `{base_classes} ${conditional_classes}`
          }
        />
        ```

      #### Data Binding
      ```tsx
      // Data source: {component.data_source}
      const data = {component.data_binding};

      <{component.name} {props} data={data} />
      ```

      #### API Reference
      - **Component Docs**: `.claude/templates/component-library/src/{component.name}/`
      - **Stories**: `.claude/templates/component-library/stories/{component.name}.stories.tsx`

      ---

  SAVE to 02-screens/{screen_slug}/component-usage.md
  // ==================================================

  // ========== GENERATE DATA REQUIREMENTS ==========
  CREATE 02-screens/{screen_slug}/data-requirements.md:
    ---
    document_id: SCR-DATA-{SCREEN_ID}
    screen_id: {screen.id}
    version: 1.0.0
    type: data_requirements
    ---

    # {Screen Name} - Data Requirements

    ## Entities Required

    | Entity | Source | Fields | Operations |
    |--------|--------|--------|------------|
    FOR each entity in screen.data_requirements.entities:
      | {entity.name} | {entity.source} | {entity.fields} | {entity.operations} |

    ## API Calls

    ### Read Operations
    ```typescript
    FOR each read_op in screen.api_calls.read:
      // {read_op.description}
      const { data, isLoading, error } = useQuery({
        queryKey: ['{read_op.entity}'],
        queryFn: () => api.{read_op.entity}.{read_op.method}()
      });
    ```

    ### Write Operations
    ```typescript
    FOR each write_op in screen.api_calls.write:
      // {write_op.description}
      const { mutate, isPending } = useMutation({
        mutationFn: (data) => api.{write_op.entity}.{write_op.method}(data),
        onSuccess: () => {
          // Handle success (e.g., toast, navigation)
        },
        onError: (error) => {
          // Handle error (e.g., show Alert component)
        }
      });
    ```

    ## Data Transformations

    FOR each transformation in screen.data_transformations:
      ### {transformation.name}
      **Input**: {transformation.input}
      **Output**: {transformation.output}
      **Logic**: {transformation.logic}

    ## State Management

    | State | Type | Initial Value | Managed By |
    |-------|------|---------------|------------|
    FOR each state in screen.state:
      | {state.name} | {state.type} | {state.initial} | {state.manager} |

  SAVE to 02-screens/{screen_slug}/data-requirements.md
  // ================================================

  // ========== PROMPT LOG: AFTER ==========
  UPDATE log entry result: {
    "status": "success",
    "output_summary": "Generated Assembly-First screen spec with {N} library components"
  }
  WRITE log
  // ========================================

// ===========================================================
```

### Step 4: Generate Screen Index

```
// ========== SCREEN INDEX ==========
CREATE 02-screens/screen-index.md:
  ---
  document_id: SCR-INDEX
  version: 1.0.0
  mode: assembly_first
  total_screens: {count}
  ---

  # Screen Index (Assembly-First)

  ## Overview

  **Total Screens**: {count}
  **Mode**: Assembly-First (using component library)
  **Library Components**: {unique_library_components_count} different components used
  **Aggregate Components**: {unique_aggregate_components_count} different aggregates used

  ## Screens by App/Portal

  FOR each app in screen_groups:

    ### {app.name}

    | Screen ID | Screen Name | Route | Components | Requirements |
    |-----------|-------------|-------|------------|--------------|
    FOR each screen in app.screens:
      | {screen.id} | [{screen.name}](./{screen.slug}/specification.md) | {screen.route} | {screen.component_count} | {screen.requirement_refs} |

  ## Component Usage Matrix

  | Component | Category | Used in Screens | Count |
  |-----------|----------|-----------------|-------|
  FOR each component in all_components_used (sorted by usage count):
    | {component.name} | {component.category} | {screen_ids} | {usage_count} |

  ## Coverage Analysis

  ### Library Components Coverage
  - **Total Available**: {lib_components.length}
  - **Used in Prototype**: {used_lib_components.length}
  - **Coverage**: {percentage}%

  ### Requirements Coverage
  - **Total Requirements**: {total_reqs}
  - **Addressed by Screens**: {addressed_reqs}
  - **Coverage**: {percentage}%

  ## Token Efficiency

  **Assembly-First Savings:**
  - Screens generated: {count}
  - Avg components per screen: {average}
  - Total component usages: {total}
  - Estimated token savings: ~{calculate_savings}x

  ## Navigation Structure

  ```
  FOR each top_level_screen:
    {screen.name} ({screen.route})
    FOR each child_screen:
      ├── {child.name} ({child.route})
      FOR each grandchild:
        │   └── {grandchild.name} ({grandchild.route})
  ```

  ## Implementation Order

  Recommended build sequence based on dependencies:

  1. **Phase 1: Core Screens** ({count} screens)
     FOR each core_screen:
       - {screen.name} - {screen.reason_for_core}

  2. **Phase 2: Secondary Screens** ({count} screens)
     FOR each secondary_screen:
       - {screen.name} - {screen.dependencies}

  3. **Phase 3: Optional Screens** ({count} screens)
     FOR each optional_screen:
       - {screen.name}

  ---
  **Assembly-First**: All screens use component library. See LIBRARY_REFERENCE.md.

SAVE to 02-screens/screen-index.md
// ==================================
```

### Step 5: Validation

```
// ========== ASSEMBLY-FIRST VALIDATION ==========
VALIDATE all screens:
  CHECKS:
    - ✅ All screens have specification.md
    - ✅ All screens have component-usage.md
    - ✅ All screens have data-requirements.md
    - ✅ All screens use library or aggregate components (no raw HTML references)
    - ✅ All screens map to Discovery screen definitions
    - ✅ All components referenced exist in library or aggregates
    - ✅ No manual ARIA mentioned in specs
    - ✅ All interaction patterns use library render props

  IF any check fails:
    LOG ERROR with details
    ADD to FAILURES_LOG.md

  ELSE:
    LOG: "✅ Assembly-First screen specifications complete"
// ================================================
```

### Step 6: Update Traceability

```
// ========== UPDATE ROOT-LEVEL TRACEABILITY ==========
READ traceability/screen_registry.json AS screen_reg

FOR each screen in generated_screens:
  FIND existing screen WHERE id == screen.discovery_id
  UPDATE screen:
    prototype_spec_path: "02-screens/{screen.slug}/specification.md"
    mode: "assembly_first"
    components_used: [
      FOR each comp in screen.components:
        {
          "component_id": comp.id,
          "source": comp.source,
          "category": comp.category
        }
    ]
    data_requirements_path: "02-screens/{screen.slug}/data-requirements.md"
    implementation_status: "spec_complete"

WRITE traceability/screen_registry.json

// Update component registry with screen usage
READ traceability/component_registry.json AS comp_reg

FOR each component usage:
  FIND component WHERE id == usage.component_id
  IF screen_refs NOT CONTAINS usage.screen_id:
    APPEND usage.screen_id TO component.screen_refs

WRITE traceability/component_registry.json
// ====================================================
```

### Step 7: Update Progress

```
UPDATE _state/progress.json:
  phases.screens.status = "complete"
  phases.screens.mode = "assembly_first"
  phases.screens.completed_at = timestamp
  phases.screens.outputs = [
    "02-screens/screen-index.md",
    "02-screens/*/specification.md",
    "02-screens/*/component-usage.md",
    "02-screens/*/data-requirements.md"
  ]
  phases.screens.metrics = {
    total_screens: {count},
    library_components_used: {count},
    aggregate_components_used: {count},
    unique_components: {count},
    token_savings: "~{estimate}x",
    prompts_logged: {count}
  }
```

---

## Output Structure (Assembly-First Mode)

```
02-screens/
├── screen-index.md                     # Assembly-First index with component usage matrix
└── {screen-slug}/
    ├── specification.md                # Component composition (library + aggregates)
    ├── component-usage.md              # Detailed usage guide for each component
    └── data-requirements.md            # API calls and state management
```

---

## Key Differences: Traditional vs Assembly-First

| Aspect | Traditional | Assembly-First |
|--------|-------------|----------------|
| **Component Specs** | Full implementation details | Reference library + composition |
| **HTML in Specs** | May show raw HTML structure | Only library component composition |
| **Accessibility** | Must specify per screen | Inherited from library |
| **State Management** | Custom per screen | Library render props pattern |
| **Token Usage** | High (full component details) | Low (reference + composition) |
| **Implementation Guidance** | Generate from scratch | Compose pre-built components |

---

## Example Screen Spec Comparison

### Traditional Mode:
```markdown
## Login Form

### HTML Structure:
<form>
  <input type="email" aria-label="Email" />
  <input type="password" aria-label="Password" />
  <button type="submit">Sign In</button>
</form>

### Styling: [custom CSS]
### Accessibility: [manual ARIA attributes]
### State: [custom state management]
```

### Assembly-First Mode:
```markdown
## Login Form - Component Composition

### Library Components Used:
| Component | Category | Purpose |
|-----------|----------|---------|
| Form | Forms | Form container with validation |
| TextField | Forms | Email and password inputs |
| Button | Buttons | Submit action |

### Implementation:
```tsx
import { Form, TextField, Label, Input, Button } from '@/component-library';

<Form onSubmit={handleLogin}>
  <TextField name="email" type="email" isRequired className="flex flex-col gap-1">
    <Label>Email</Label>
    <Input />
  </TextField>
  <TextField name="password" type="password" isRequired className="flex flex-col gap-1">
    <Label>Password</Label>
    <Input />
  </TextField>
  <Button type="submit" isPending={isLoading}>Sign In</Button>
</Form>
```

**✅ Accessibility, styling, and state management handled by library**
```

### ⚠️ CRITICAL: DateField Pattern

**COMMON MISTAKE**: Using regular `<Input />` inside `DateField` (WILL NOT RENDER)

```tsx
// ❌ WRONG - DateField will not render
<DateField name="dob" isRequired>
  <Label>Date of Birth</Label>
  <Input />  {/* This does NOT work! */}
</DateField>
```

**CORRECT PATTERN**: Use `DateInput` with `DateSegment` children

```tsx
import { DateField, DateInput, DateSegment, Label } from '@/component-library';
import { parseDate } from '@internationalized/date';
import type { DateValue } from '@internationalized/date';

// State management
const [dateOfBirth, setDateOfBirth] = useState<DateValue | null>(null);

// Rendering
<DateField
  name="dateOfBirth"
  value={dateOfBirth}
  onChange={setDateOfBirth}
  isRequired
  className="flex flex-col gap-1"
>
  <Label>Date of Birth *</Label>
  <DateInput className="flex gap-1 h-[60px] px-4 border border-border-default rounded-md">
    {(segment) => <DateSegment segment={segment} className="px-1 py-2 text-text-primary" />}
  </DateInput>
</DateField>
```

**Key Points:**
- DateField uses `DateValue` types from `@internationalized/date`, NOT strings or `Date` objects
- Use `parseDate('YYYY-MM-DD')` to create DateValue from strings
- Use `dateValue.toString()` to convert back to ISO string for API/storage
- DateInput requires render function `{(segment) => <DateSegment segment={segment} />}`
- Each segment (month, day, year) is individually editable and keyboard-navigable

**LocalStorage Example:**
```tsx
// Save to localStorage
const dataToStore = {
  dateOfBirth: formData.dateOfBirth ? formData.dateOfBirth.toString() : null
};
localStorage.setItem('draft', JSON.stringify(dataToStore));

// Load from localStorage
const draft = localStorage.getItem('draft');
if (draft) {
  const parsed = JSON.parse(draft);
  if (parsed.dateOfBirth && typeof parsed.dateOfBirth === 'string') {
    parsed.dateOfBirth = parseDate(parsed.dateOfBirth);
  }
  setFormData(parsed);
}
```

---

## Related Documentation

- **Rule**: `.claude/commands/_assembly_first_rules.md`
- **Component Integration**: `.claude/skills/Prototype_Components/ASSEMBLY_FIRST_INTEGRATION.md`
- **Architecture**: `architecture/Assembly-First Design System/ASSEMBLY_FIRST_ARCHITECTURE.md`
- **Component Library**: `.claude/templates/component-library/`
- **Original Skill**: `SKILL.md` (fallback workflow)
