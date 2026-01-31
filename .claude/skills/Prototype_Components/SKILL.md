---
name: generating-component-specs
description: Use when you need to generate high-quality, distinctive component specifications including variants, states, and accessibility mappings.
model: sonnet
allowed-tools: AskUserQuestion, Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-component-specs started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-component-specs ended '{"stage": "prototype"}'
---
---
name: generating-component-specs
description: Use when you need to generate high-quality, distinctive component specifications including variants, states, and accessibility mappings.
model: sonnet
allowed-tools: Read, Write, Edit

# Spec React Components

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-component-specs instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning
> **Supports**: Smart Obsolescence Handling for non-UI projects

## Metadata
- **Skill ID**: Prototype_Components
- **Version**: 2.0.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-26
- **Author**: Milos Cigoj
- **Change History**:
  - v2.0.0 (2025-12-26): Added NOT_APPLICABLE handling for non-UI projects
  - v1.2.0 (2025-12-23): Added mandatory ROOT-level component registry propagation for end-to-end traceability
  - v1.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v1.0.0 (2025-01-15): Initial skill version

## Description
Generate DISTINCTIVE component specifications with high design quality. Creates complete component library with specs for primitives, data-display, feedback, navigation, overlays, and patterns. Integrates frontend-design principles to avoid generic AI aesthetics.

Generate detailed component specifications from design system foundation with **exceptional visual quality**. Follows OUTPUT_STRUCTURE.md for deterministic folder structure.

> **DESIGN QUALITY ENFORCEMENT**: This skill integrates frontend-design principles. Components MUST be distinctive, memorable, and avoid generic AI aesthetics. Every component needs a clear visual treatment that reflects the project's aesthetic direction.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: Components in `primitives/`, `data-display/`, `feedback/`, `navigation/`, and `overlays/` categories are generally universal. However, `patterns/` components (e.g., "candidate-card", "interview-slot") are domain-specific examples. Your actual pattern components should be derived from your project's entities and workflows.

---

## Output Structure (REQUIRED)

This skill MUST generate the following structure:

```
01-components/
├── COMPONENT_LIBRARY_SUMMARY.md      # Full library overview
├── data-display/
│   ├── avatar.md
│   ├── badge.md
│   ├── card.md
│   ├── empty-state.md
│   ├── kanban-column.md
│   ├── list.md
│   ├── progress.md
│   ├── skeleton.md
│   ├── stat.md
│   ├── table.md
│   ├── tag.md
│   └── timeline.md
├── feedback/
│   ├── alert.md
│   ├── toast.md
│   └── tooltip.md
├── FINAL_DELIVERY_SUMMARY.md
├── navigation/
│   ├── breadcrumb.md
│   ├── command-palette.md
│   ├── header.md
│   ├── pagination.md
│   ├── sidebar.md
│   ├── stepper.md
│   └── tabs.md
├── overlays/
│   ├── context-menu.md
│   ├── dialog.md
│   ├── drawer.md
│   ├── dropdown.md
│   ├── menu.md
│   └── popover.md
├── patterns/
│   └── {domain-specific}.md
└── primitives/
    ├── button.md
    ├── checkbox.md
    ├── input.md
    ├── label.md
    ├── radio.md
    ├── README.md
    ├── select.md
    ├── switch.md
    └── textarea.md
```

---

## Applicability Check (Smart Obsolescence Handling)

**BEFORE generating component specifications**, check project classification:

```
1. Read _state/prototype_config.json (or _state/discovery_config.json)
2. Check project_classification.type
3. IF type IN [BACKEND_ONLY, DATABASE_ONLY, INTEGRATION, INFRASTRUCTURE]:
   → Generate NOT_APPLICABLE placeholder (see below)
   → SKIP full component generation
4. IF type == FULL_STACK:
   → Proceed with normal component generation
```

### N/A Placeholder Template

If project type is NOT `FULL_STACK`, generate this placeholder:

```markdown
# Component Library Specifications

---
status: NOT_APPLICABLE
artifact: component-library
project_type: {type}
classification_date: {date}
generated_date: {now}
---

## Reason

This artifact is not applicable for **{type}** projects.

Component specifications are only generated for projects with user interface
components (FULL_STACK).

## Project Classification

- **Type**: {type}
- **Confidence**: {confidence}
- **Classified**: {date}

## What This Means

- No component specifications will be generated for this project
- Downstream code generation will skip UI component creation
- Focus remains on {focus_area_for_type}

## Alternative Artifacts

For this project type, refer to:
- `data-model.md` - Data entity definitions
- `api-contracts.json` - API specifications
- `test-data/` - Mock data for testing

---
*Generated by Prototype_Components v2.0.0*
*Smart Obsolescence Handling enabled*
```

**Output**: Save to `01-components/COMPONENT_LIBRARY_SUMMARY.md` with N/A status.

---

## Component Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **primitives** | Basic form elements | button, input, select, checkbox |
| **data-display** | Content presentation | card, table, badge, avatar |
| **feedback** | User communication | alert, toast, tooltip |
| **navigation** | Wayfinding elements | tabs, breadcrumb, sidebar |
| **overlays** | Floating UI | dialog, dropdown, drawer |
| **patterns** | Domain-specific composites | Built from above components |

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ 00-foundation/DESIGN_BRIEF.md
READ 00-foundation/DESIGN_TOKENS.md
READ 00-foundation/colors.md
READ 00-foundation/typography.md
READ 00-foundation/spacing-layout.md
READ _state/requirements_registry.json
READ discovery/04-design-specs/screen-definitions.md

IDENTIFY requirements this skill MUST address:
  - A11Y-001: Keyboard navigation (for ALL interactive components)
  - A11Y-003: Focus indicators (for ALL focusable components)
  - A11Y-004: Form labels (for ALL form components)
  - FR-XXX: Functional requirements related to UI controls

IF DESIGN_TOKENS.md missing:
  BLOCK: "Run DesignTokens first"

IF requirements_registry missing:
  BLOCK: "Run Requirements first"
```

### Step 1.4: Select Component Library Strategy (REQUIRED)

Determine the component library approach before generating specifications.

```
USE AskUserQuestion:
  question: "Which component approach should the prototype use?"
  header: "Components"
  options:
    - label: "React Aria (Recommended)"
      description: "Maximum accessibility, unstyled, theme-able"
    - label: "Radix UI"
      description: "Good accessibility, minimal styling"
    - label: "Shadcn/ui"
      description: "Pre-styled, faster development"

STORE selected strategy in _state/prototype_config.json:
  {
    "component_library": "{selected_option}",
    "component_library_rationale": "{option_description}"
  }
```

### Step 1.5: Establish Aesthetic Direction (REQUIRED)

> **Frontend Design Integration**: Before generating any components, establish a BOLD aesthetic direction.

```
READ 00-foundation/AESTHETIC_DIRECTION.md IF exists
READ 00-foundation/DESIGN_BRIEF.md for design philosophy

IF AESTHETIC_DIRECTION.md not exists:

  ANALYZE design_brief for aesthetic cues:
    - Brand personality
    - Target audience
    - Competitive positioning
    - Emotional tone

  PROMPT user:
    ═══════════════════════════════════════════════════════════════
    🎨 AESTHETIC DIRECTION
    ═══════════════════════════════════════════════════════════════

    Before generating components, commit to a BOLD aesthetic direction.
    This ensures components are distinctive, not generic.

    Based on the design brief, I recommend:

    **{recommended_direction}**: {description}

    Alternative directions:
    1. **Brutally Minimal**: Stark whites, heavy typography, no decoration
    2. **Soft & Organic**: Rounded corners, gradients, natural feel
    3. **Editorial/Magazine**: Bold typography, asymmetric layouts, dramatic
    4. **Tech Innovation**: High contrast, neon accents, dark backgrounds
    5. **Refined Luxury**: Muted tones, elegant spacing, subtle details
    6. **Playful/Toy-like**: Bright colors, bouncy animations, friendly
    7. **Retro-Futuristic**: Gradients, glow effects, vintage-modern fusion
    8. **Industrial/Utilitarian**: Functional, grid-based, monospace fonts

    Select direction:
    1. "use: [direction]" - Apply recommended or alternative
    2. "custom: [description]" - Define custom aesthetic
    3. "skip" - Use neutral aesthetic (NOT RECOMMENDED)
    ═══════════════════════════════════════════════════════════════

    WAIT for user response

  CREATE 00-foundation/AESTHETIC_DIRECTION.md:
    # Aesthetic Direction

    ## Chosen Direction: {direction_name}

    {description}

    ## Design Commitments

    ### Typography
    - Display Font: {distinctive_display_font} (NOT Inter, Roboto, Arial)
    - Body Font: {complementary_body_font}
    - Font Pairing Rationale: {why_these_work_together}

    ### Color Strategy
    - Approach: {dominant_with_accents | balanced | monochromatic}
    - Signature Color: {hex} - {where_it_appears}
    - Contrast Philosophy: {high_contrast | subtle_tones | vibrant}

    ### Spatial Composition
    - Layout Approach: {grid_based | asymmetric | overlap_layers | generous_whitespace}
    - Spacing Philosophy: {tight_and_dense | balanced | spacious}
    - Grid-Breaking Elements: {what_breaks_the_grid}

    ### Motion & Animation
    - Animation Style: {snappy | smooth | bouncy | dramatic}
    - Signature Interaction: {one_memorable_animation}
    - Entry Animations: {staggered | simultaneous | scroll_triggered}

    ### Visual Details
    - Background Treatment: {solid | gradient | texture | pattern}
    - Shadow Style: {none | subtle | dramatic}
    - Border Approach: {none | fine | bold | decorative}
    - Decorative Elements: {icons | patterns | illustrations | none}

    ## The Differentiator

    What makes this UNFORGETTABLE?
    {the_one_thing_users_will_remember}

    ## Forbidden Patterns (Generic AI Aesthetics)

    - ❌ Inter/Roboto/Arial fonts
    - ❌ Purple gradients on white
    - ❌ Cookie-cutter shadcn/ui defaults
    - ❌ Evenly distributed color palettes
    - ❌ Predictable grid layouts
    - ❌ Generic card radiuses (8px rounded corners everywhere)

ELSE:
  READ 00-foundation/AESTHETIC_DIRECTION.md → aesthetic
  LOG: "Using aesthetic direction: {aesthetic.direction_name}"

STORE aesthetic_direction for use in component generation
```

### Step 2: Identify Required Components
```
SCAN screen-definitions.md for UI elements mentioned

MAP to component categories:
  primitives: Button, Input, Select, Checkbox, Radio, Switch, Textarea, Label
  data-display: Card, Table, Badge, Avatar, Tag, Stat, Timeline, List, Skeleton, EmptyState, Progress, KanbanColumn
  feedback: Alert, Toast, Tooltip
  navigation: Tabs, Breadcrumb, Sidebar, Header, Pagination, Stepper, CommandPalette
  overlays: Dialog, Dropdown, Drawer, Menu, Popover, ContextMenu
  patterns: (domain-specific composites)

CREATE component_list[] with categories
```

### Step 3: Generate Component Specs by Category

**FOR EACH COMPONENT, perform prompt logging:**

#### 3a: Log and Generate Primitives
```
FOR each primitive component (button, input, select, etc.):

  // ========== PROMPT LOG: BEFORE GENERATION ==========
  READ _state/prompt_log.json AS log
  
  next_id = "PL-" + String(log.summary.total_entries + 1).padStart(3, '0')
  current_session = log.sessions[log.sessions.length - 1]
  
  new_entry = {
    "id": next_id,
    "session_id": current_session.session_id,
    "timestamp": NOW_ISO(),
    "skill": "Prototype_Components",
    "step": "Step 3a: Generate Primitives",
    "category": "generation",
    "desired_outcome": "Generate {component} specification with variants, sizes, states, and accessibility",
    "inputs": [
      "00-foundation/DESIGN_TOKENS.md",
      "00-foundation/colors.md",
      "_state/requirements_registry.json"
    ],
    "target": "01-components/primitives/{component}.md",
    "result": { "status": "pending" }
  }
  
  APPEND new_entry TO log.entries
  log.summary.total_entries++
  log.summary.by_skill["Prototype_Components"] = (log.summary.by_skill["Prototype_Components"] || 0) + 1
  log.summary.by_category["generation"] = (log.summary.by_category["generation"] || 0) + 1
  current_session.entry_count++
  
  IF "Prototype_Components" NOT IN current_session.skills_executed:
    APPEND "Prototype_Components" TO current_session.skills_executed
  
  WRITE log TO _state/prompt_log.json
  // ====================================================

  // ========== GENERATE COMPONENT ==========
  CREATE 01-components/primitives/{component}.md:
    # {Component Name}

    ## Requirements Addressed (MANDATORY)
    | Req ID | Description | Implementation |
    |--------|-------------|----------------|
    | A11Y-001 | Keyboard navigation | Tab focuses, Enter activates |
    | A11Y-003 | Visible focus | 2px ring using focus-ring token |

    ## Overview
    [One sentence description]

    ## Visual Treatment (from Aesthetic Direction)

    > **Aesthetic**: {aesthetic_direction.direction_name}

    ### Typography
    - Font: {component_specific_font_choice}
    - Weight: {weight_for_this_component}
    - Letter Spacing: {tracking_choice}

    ### Color Application
    - Primary Surface: {color_token} — {hex}
    - Accent/Highlight: {accent_token} — {hex}
    - Text on Surface: {text_color_token}

    ### Shape & Space
    - Border Radius: {specific_radius} (NOT generic 8px)
    - Padding: {padding_values}
    - Shadow: {shadow_treatment_if_any}

    ### Distinctive Details
    - {what_makes_this_component_visually_memorable}
    - {unique_treatment_aligned_with_aesthetic}

    ### Animation (from Aesthetic)
    - Hover: {hover_transition}
    - Active: {active_animation}
    - Focus: {focus_animation}

    ## Variants
    | Variant | Use Case | Visual |

    ## Sizes
    | Size | Height | Padding | Font Size |

    ## States
    | State | Visual Changes | CSS | A11Y |

    ## Props
    | Prop | Type | Default | Description |

    ## Accessibility
    - **Keyboard**: [keyboard interactions]
    - **Screen Reader**: [announcements]
    - **Focus**: [focus behavior]

    ## Token Mapping
    | Element | Token |

    ## Usage Examples
    ```jsx
    [code examples]
    ```
  // ==========================================

  // ========== PROMPT LOG: AFTER GENERATION ==========
  READ _state/prompt_log.json AS log
  
  entry_index = log.entries.findIndex(e => e.id === next_id)
  log.entries[entry_index].result = {
    "status": "success",
    "output_summary": "Generated {component} with {N} variants, {M} sizes, full accessibility"
  }
  log.summary.by_status["success"] = (log.summary.by_status["success"] || 0) + 1
  current_session.success_count++
  
  WRITE log TO _state/prompt_log.json
  // ===================================================
```

#### 3b: Log and Generate Data Display Components
```
FOR each data-display component:

  // Log before (same pattern as 3a)
  LOG entry with:
    step: "Step 3b: Generate Data Display"
    target: "01-components/data-display/{component}.md"
    desired_outcome: "Generate {component} with domain-specific variants"

  CREATE 01-components/data-display/{component}.md
  
  INCLUDE domain-specific variants:
    - Card: default, candidate, position, interview
    - Table: sortable headers, row selection, pagination
    - Badge: status colors mapped to pipeline stages

  // Log after with result
```

#### 3c: Log and Generate Feedback Components
```
FOR each feedback component:

  // Log before
  LOG entry with:
    step: "Step 3c: Generate Feedback"
    target: "01-components/feedback/{component}.md"

  CREATE 01-components/feedback/{component}.md
  
  INCLUDE:
    - Auto-dismiss timing
    - Stacking behavior (toasts)
    - ARIA live regions

  // Log after
```

#### 3d: Log and Generate Navigation Components
```
FOR each navigation component:

  // Log before
  LOG entry with:
    step: "Step 3d: Generate Navigation"
    target: "01-components/navigation/{component}.md"

  CREATE 01-components/navigation/{component}.md
  
  INCLUDE:
    - Route integration
    - Active state handling
    - Keyboard navigation within

  // Log after
```

#### 3e: Log and Generate Overlay Components
```
FOR each overlay component:

  // Log before
  LOG entry with:
    step: "Step 3e: Generate Overlays"
    target: "01-components/overlays/{component}.md"

  CREATE 01-components/overlays/{component}.md
  
  INCLUDE:
    - Focus trap
    - Escape to close
    - Click outside behavior
    - Portal rendering

  // Log after
```

#### 3f: Log and Generate Pattern Components
```
FOR each pattern component:

  // Log before
  LOG entry with:
    step: "Step 3f: Generate Patterns"
    target: "01-components/patterns/{component}.md"

  CREATE 01-components/patterns/{component}.md
  
  INCLUDE:
    - Composition of primitives
    - Domain-specific props
    - Data shape requirements

  // Log after
```

### Step 4: Generate README for Primitives
```
CREATE 01-components/primitives/README.md:
  # Primitives
  
  Foundation components for all form interactions.
  
  ## Components
  | Component | A11Y | Interactive | Form |
  |-----------|------|-------------|------|
  | Button | ✅ | ✅ | ❌ |
  | Input | ✅ | ✅ | ✅ |
  ...
```

### Step 5: Log and Generate Component Library Summary
```
// ========== PROMPT LOG: BEFORE ==========
READ _state/prompt_log.json AS log

next_id = "PL-" + String(log.summary.total_entries + 1).padStart(3, '0')

LOG entry with:
  id: next_id
  skill: "Prototype_Components"
  step: "Step 5: Generate Library Summary"
  category: "generation"
  desired_outcome: "Generate component library summary with full inventory and requirements coverage"
  target: "01-components/COMPONENT_LIBRARY_SUMMARY.md"

WRITE log
// ========================================

CREATE 01-components/COMPONENT_LIBRARY_SUMMARY.md:
  # Component Library Summary
  
  ## Overview
  Total components: {count}
  Generated: {timestamp}
  
  ## By Category
  | Category | Count | Components |
  |----------|-------|------------|
  | primitives | 9 | button, input, select... |
  | data-display | 12 | card, table, badge... |
  | feedback | 3 | alert, toast, tooltip |
  | navigation | 7 | tabs, sidebar, breadcrumb... |
  | overlays | 6 | dialog, drawer, dropdown... |
  | patterns | N | [domain-specific] |
  
  ## Requirements Coverage
  | Req ID | Type | Components Addressing |
  |--------|------|----------------------|
  | A11Y-001 | Accessibility | All interactive (100%) |
  | A11Y-003 | Accessibility | All focusable (100%) |
  | A11Y-004 | Accessibility | All form components (100%) |
  
  ## Component Index
  [links to all specs organized by category]

// ========== PROMPT LOG: AFTER ==========
READ log, UPDATE entry result, WRITE log
// =======================================
```

### Step 6: Link to Requirements (TRACEABILITY)
```
FOR each component:
  IF interactive component (button, link, input, select):
    MUST include: A11Y-001 (keyboard navigation)
    MUST include: A11Y-003 (focus indicators)
    
  IF form component (input, select, checkbox, radio):
    MUST include: A11Y-004 (form labels)

UPDATE _state/requirements_registry.json:
  FOR each requirement addressed:
    ADD "component: {name}" to requirement.addressed_by[]
```

### Step 7: Validate Each Component (REQUIRED)
```
FOR each component spec:
  CHECKS:
    - "Requirements Addressed" section EXISTS
    - "Requirements Addressed" section NOT EMPTY
    - Interactive components have A11Y-001
    - Focusable components have A11Y-003
    - Form components have A11Y-004
    - All variants documented
    - All states specified
    - Token references valid
    
  IF any check fails:
    PROMPT for correction
```

### Step 8: Validate Overall Outputs (REQUIRED)
```
VALIDATE component library:
  DIRECTORY CHECKS:
    - 01-components/primitives/ exists with ≥7 files
    - 01-components/data-display/ exists with ≥10 files
    - 01-components/feedback/ exists with ≥3 files
    - 01-components/navigation/ exists with ≥5 files
    - 01-components/overlays/ exists with ≥5 files
    - 01-components/patterns/ exists with ≥1 file
    - COMPONENT_LIBRARY_SUMMARY.md exists
    
  CONTENT CHECKS:
    - 100% of interactive components have A11Y-001
    - 100% of focusable components have A11Y-003
    - 100% of form components have A11Y-004
    - No component has empty Requirements Addressed
    
IF any validation fails:
  PROMPT with mitigation options
```

### Step 9: Update Prompt Log Summary (REQUIRED)
```
// ========== UPDATE PROMPT_LOG.MD ==========
READ _state/prompt_log.json AS log

GENERATE _state/PROMPT_LOG.md:
  # Prompt Execution Log
  
  **Generated:** {NOW}
  **Total Prompts:** {log.summary.total_entries}
  
  ## Current Session: {current_session.session_id}
  
  Started: {current_session.started_at}
  Skills: {current_session.skills_executed.join(", ")}
  Prompts: {current_session.entry_count} ({current_session.success_count} success)
  
  ### Recent Entries (Components)
  
  | ID | Step | Target | Status |
  |----|------|--------|--------|
  FOR last 20 entries WHERE skill === "Prototype_Components":
    | {id} | {step} | {target} | {result.status} |
  
  ---
  
  ## Summary by Skill
  
  | Skill | Count |
  |-------|-------|
  FOR each skill in log.summary.by_skill:
    | {skill} | {count} |

WRITE _state/PROMPT_LOG.md
// ==========================================
```

### Step 10: Auto-Invoke Decomposition
```
LOG: "Auto-triggering Decomposition (components changed)"

INVOKE Prototype_Decomposition:
  MODE: merge
  TRIGGER: "components_completed"
```

### Step 10.5: PROPAGATE TO ROOT-LEVEL TRACEABILITY (MANDATORY)

> **CRITICAL**: After creating local component registries, MUST propagate to ROOT-level `traceability/` folder for end-to-end traceability chain.

```
# Step 10.5.1: Build Component Registry
BUILD component_registry from all generated component specs:

component_registry = {
  "schema_version": "1.0.0",
  "stage": "Prototype",
  "checkpoint": 8,
  "source_folder": "01-components/",
  "created_at": "{timestamp}",
  "updated_at": "{timestamp}",
  "traceability_chain": {
    "upstream": ["requirements_registry.json", "screen_registry.json"],
    "downstream": ["module_registry.json", "test_case_registry.json"]
  },
  "items": [
    FOR each component in all categories:
      {
        "id": "COMP-{CATEGORY}-{NAME}",
        "name": "{component_name}",
        "category": "{primitives|data-display|feedback|navigation|overlays|patterns}",
        "file_path": "01-components/{category}/{component}.md",
        "requirement_refs": ["{A11Y-XXX}", "{FR-XXX}"],
        "screen_refs": ["{SCR-XXX}"],
        "variants": [{variant list}],
        "states": [{state list}],
        "a11y_compliance": {
          "A11Y-001": true,
          "A11Y-003": true,
          "A11Y-004": {true if form component}
        }
      }
  ],
  "summary": {
    "total_components": {count},
    "by_category": {
      "primitives": {count},
      "data-display": {count},
      "feedback": {count},
      "navigation": {count},
      "overlays": {count},
      "patterns": {count}
    },
    "a11y_coverage": "100%"
  }
}

# Step 10.5.2: Write to ROOT-level traceability folder
WRITE traceability/component_registry.json:
  {component_registry}

# Step 10.5.3: Update Requirements Registry with Component Links
READ traceability/requirements_registry.json AS req_reg

FOR each component in component_registry.items:
  FOR each req_id in component.requirement_refs:
    FIND requirement in req_reg.items WHERE id == req_id
    IF requirement.component_refs NOT CONTAINS component.id:
      APPEND component.id TO requirement.component_refs

WRITE traceability/requirements_registry.json:
  {req_reg with updated component_refs}

# Step 10.5.4: Validation
VERIFY:
  - traceability/component_registry.json EXISTS
  - All components have at least one requirement_ref
  - Requirements registry updated with component links

IF validation fails:
  LOG: "⚠️ ROOT-level traceability propagation incomplete"
  ADD to FAILURES_LOG.md
```

### Step 11: Update Progress (Atomic Updates)

> **Phase 4 Enhancement**: Uses ProgressLock for atomic, corruption-proof updates

```python
# IMPORT progress lock utility
from progress_lock import ProgressLock

# UPDATE progress with atomic file locking
with ProgressLock('prototype') as progress:
    # All updates happen atomically
    # Automatically saved on exit, rolled back on exception
    progress['phases']['components']['status'] = 'complete'
    progress['phases']['components']['completed_at'] = datetime.now().isoformat()
    progress['phases']['components']['outputs'] = [
        "01-components/COMPONENT_LIBRARY_SUMMARY.md",
        "01-components/primitives/*.md",
        "01-components/data-display/*.md",
        "01-components/feedback/*.md",
        "01-components/navigation/*.md",
        "01-components/overlays/*.md",
        "01-components/patterns/*.md"
    ]
    progress['phases']['components']['validation'] = {
        'status': 'passed',
        'checks_run': total_checks,
        'checks_passed': passed_checks,
        'a11y_coverage': {
            "A11Y-001": "100%",
            "A11Y-003": "100%",
            "A11Y-004": "100%"
        }
    }
    progress['phases']['components']['metrics'] = {
        'total_components': component_count,
        'primitives': primitives_count,
        'data_display': data_display_count,
        'feedback': feedback_count,
        'navigation': navigation_count,
        'overlays': overlays_count,
        'patterns': patterns_count,
        'requirements_addressed': reqs_addressed,
        'prompts_logged': prompts_logged
    }
    # Lock released and changes saved automatically here
```

**Benefits**:
- ✅ Prevents progress.json corruption on skill failure
- ✅ Automatic rollback if exception occurs
- ✅ File locking prevents concurrent write conflicts
- ✅ Backup created before each update

---

## Output Files (REQUIRED)

| Directory | Min Files | Purpose |
|-----------|-----------|---------|
| `primitives/` | 7+ | Basic form elements |
| `data-display/` | 10+ | Content presentation |
| `feedback/` | 3+ | User communication |
| `navigation/` | 5+ | Wayfinding |
| `overlays/` | 5+ | Floating UI |
| `patterns/` | 1+ | Domain composites |
| `COMPONENT_LIBRARY_SUMMARY.md` | 1 | Overview |

---

## Component Spec Template (MANDATORY FORMAT)

```markdown
---
document_id: COMP-{CATEGORY}-{NAME}
version: 1.0.0
created_at: {DATE}
updated_at: {DATE}
generated_by: Prototype_Components
source_files:
  - 00-foundation/DESIGN_TOKENS.md
  - 00-foundation/AESTHETIC_DIRECTION.md
  - _state/requirements_registry.json
change_history:
  - version: "1.0.0"
    date: "{DATE}"
    author: "Prototype_Components"
    changes: "Initial generation"
---

# {Component Name}

## Requirements Addressed (MANDATORY)
| Req ID | Description | Implementation |
|--------|-------------|----------------|
| A11Y-001 | Keyboard navigation | Tab focuses, Enter activates |
| A11Y-003 | Visible focus | 2px ring using focus-ring token |

## Overview
[One sentence description]

## Visual Treatment

> **Aesthetic**: {aesthetic_direction from 00-foundation/AESTHETIC_DIRECTION.md}

### Typography
- Font: {component_specific_font_choice}
- Weight: {weight_for_this_component}
- Letter Spacing: {tracking_choice}

### Color Application
| Variant | Background | Text | Border |
|---------|------------|------|--------|
| primary | {color_token} | {text_token} | {border_token} |

### Shape & Space
- Border Radius: {specific_radius}
- Padding: {padding_values}
- Shadow: {shadow_treatment}

### Distinctive Details
- {what_makes_this_component_visually_memorable}

### Animation
- Hover: {hover_transition}
- Active: {active_animation}
- Focus: {focus_animation}

## Variants
| Variant | Use Case | Visual |
|---------|----------|--------|

## Sizes
| Size | Height | Padding | Font Size | Usage |
|------|--------|---------|-----------|-------|

## States
| State | Visual Changes | CSS | A11Y |
|-------|----------------|-----|------|
| Default | ... | ... | ... |
| Hover | ... | ... | ... |
| Focus | ... | `focus-visible` | focus ring |
| Active | ... | ... | ... |
| Disabled | opacity: 0.5 | `aria-disabled` | ... |
| Loading | spinner | `aria-busy` | ... |

## Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|

## Accessibility
- **Keyboard**: [keyboard interactions]
- **Screen Reader**: [announcements]
- **Focus**: [focus behavior]
- **WCAG**: [specific criteria met]

## Token Mapping
| Element | Token |
|---------|-------|
| Background | `--color-*` |
| Text | `--text-*` |
| Border | `--border-*` |
| Radius | `--radius-*` |
| Shadow | `--shadow-*` |
| Transition | `--duration-*` |

## Usage Examples
```jsx
// Primary usage
<{Component} variant="primary">...</{Component}>

// With props
<{Component} variant="secondary" size="lg" leftIcon={<Icon />}>
  ...
</{Component}>
```

## Related Components
- [{RelatedComponent1}](./{path})
- [{RelatedComponent2}](./{path})

---

**Document Metadata**
- **ID**: {document_id}
- **Version**: {version}
- **Last Updated**: {updated_at}
- **Generated By**: {generated_by}
```

---

## Prompt Logging Summary

This skill logs the following prompt types:
| Step | Category | Logged Per |
|------|----------|------------|
| 3a-3f | generation | Each component |
| 5 | generation | Library summary |

Expected log entries for full run: ~45-50 entries (one per component + summaries)

---

## Progress.json Update

```json
{
  "phases": {
    "components": {
      "status": "complete",
      "completed_at": "2024-12-13T11:45:00Z",
      "outputs": ["01-components/**/*.md"],
      "validation": { "status": "passed" },
      "metrics": {
        "total_components": 42,
        "prompts_logged": 45
      }
    }
  }
}
```
