---
name: prototype-components
description: Generate component specifications from discovery design specs
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-components started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: |
            SYSTEM_NAME=$(cat _state/session.json 2>/dev/null | grep -o '"project"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"project"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//' || echo "")
            if [ -n "$SYSTEM_NAME" ] && [ "$SYSTEM_NAME" != "pending" ]; then
              uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_prototype_output.py" --system-name "$SYSTEM_NAME" --phase components
            else
              echo '{"result": "skip", "reason": "System name not found in session"}'
              exit 0
            fi
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-components ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-components instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Assembly-First and traceability rules:

```bash
# Assembly-First rules (loaded automatically in Prototype stage)
/_assembly_first_rules

# Traceability rules for ID management
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Required: `<SystemName>` or path to `Prototype_<SystemName>/`

## Prerequisites

- Phase 7 completed: Design tokens exist
- Checkpoint 7 passed

## Assembly-First Mode Detection

**BEFORE execution**, check if Assembly-First mode is enabled:

```
1. Check if .claude/templates/component-library/ exists
2. Check if .claude/templates/component-library/manifests/components.json exists
3. Check if _state/prototype_config.json has assembly_first.enabled == true

IF all true:
  → ASSEMBLY_FIRST_MODE = ON
  → Read .claude/skills/Prototype_Components/ASSEMBLY_FIRST_INTEGRATION.md
  → Follow Assembly-First workflow (library reference + aggregates only)

ELSE:
  → ASSEMBLY_FIRST_MODE = OFF
  → Read .claude/skills/Prototype_Components/SKILL.md
  → Follow traditional workflow (generate all component specs)
```

## Skills Used

**Read BEFORE execution** (mode-dependent):

**IF Assembly-First Mode ON:**
- `.claude/skills/Prototype_Components/ASSEMBLY_FIRST_INTEGRATION.md` (primary)
- `.claude/templates/component-library/manifests/components.json` (component registry)
- `.claude/templates/component-library/SKILL.md` (usage protocol)
- `.claude/commands/_assembly_first_rules.md` (enforcement checklist)

**IF Assembly-First Mode OFF:**
- `.claude/skills/Prototype_Components/SKILL.md` (traditional workflow)

---

## Execution Steps (Assembly-First Mode ON)

When Assembly-First mode is enabled, follow the workflow in `ASSEMBLY_FIRST_INTEGRATION.md`:

### Step 0.5: Read Component Library (MANDATORY BLOCKING)

```
READ .claude/templates/component-library/manifests/components.json AS lib_components
READ .claude/templates/component-library/SKILL.md AS lib_protocol
READ .claude/templates/component-library/INTERACTIONS.md AS lib_interactions

VERIFY lib_components has 62+ components

LOG: "✅ Assembly-First mode enabled: 62 library components available"
```

### Step 1: Map Discovery Requirements to Library Components

Instead of generating all components, map Discovery requirements to existing library components:

```
Discovery Requirement → Library Component:
- "text input" → TextField (Forms)
- "dropdown" → ComboBox (Pickers)
- "data table" → Table (Collections)
- "button" → Button (Buttons)
- etc. (see ASSEMBLY_FIRST_INTEGRATION.md for full mapping)
```

### Step 2: Identify Aggregate Components Only

Generate specs ONLY for aggregates (components that combine multiple library components):

Examples:
- ✅ KPICard (combines Meter + Heading + Text + Badge)
- ✅ TaskListItem (combines Checkbox + Text + Menu + Button)
- ❌ CustomButton (use library Button instead)

### Step 3: Generate Outputs

**Assembly-First outputs:**
```
01-components/
├── library-components/
│   └── LIBRARY_REFERENCE.md          # Reference to 62 library components
├── aggregates/
│   ├── KPICard.md                    # Custom aggregate
│   └── TaskListItem.md               # Custom aggregate
└── COMPONENT_LIBRARY_SUMMARY.md      # Assembly-First summary
```

**Token savings:** ~16x reduction vs traditional

---

## Execution Steps (Assembly-First Mode OFF - Traditional)

When Assembly-First mode is disabled or library not available, follow traditional workflow:

### Step 1: Load Inputs

Read:
- `00-foundation/design-tokens.json`
- `00-foundation/design-principles.md`
- `_state/requirements_registry.json` (for feature context)
- `_state/discovery_summary.json` (for screen requirements)

### Step 2: Update Progress

```json
{
  "current_phase": 8,
  "phases": {
    "components": {
      "status": "in_progress",
      "started_at": "<timestamp>"
    }
  }
}
```

### Step 3: Execute Prototype_Components Skill

Generate components in six categories:

#### 3.1 Primitives (`01-components/primitives/`)

Basic building blocks:

| Component | File |
|-----------|------|
| Button | `button.md` |
| Input | `input.md` |
| Select | `select.md` |
| Checkbox | `checkbox.md` |
| Radio | `radio.md` |
| Toggle | `toggle.md` |
| Badge | `badge.md` |
| Avatar | `avatar.md` |
| Icon | `icon.md` |

#### 3.2 Data Display (`01-components/data-display/`)

Components for showing data:

| Component | File |
|-----------|------|
| Table | `table.md` |
| Card | `card.md` |
| List | `list.md` |
| Stat | `stat.md` |
| Chart | `chart.md` |
| Empty State | `empty-state.md` |

#### 3.3 Feedback (`01-components/feedback/`)

User feedback components:

| Component | File |
|-----------|------|
| Alert | `alert.md` |
| Toast | `toast.md` |
| Progress | `progress.md` |
| Skeleton | `skeleton.md` |
| Spinner | `spinner.md` |

#### 3.4 Navigation (`01-components/navigation/`)

Navigation components:

| Component | File |
|-----------|------|
| Sidebar | `sidebar.md` |
| Header | `header.md` |
| Breadcrumb | `breadcrumb.md` |
| Tabs | `tabs.md` |
| Pagination | `pagination.md` |

#### 3.5 Overlays (`01-components/overlays/`)

Overlay components:

| Component | File |
|-----------|------|
| Modal | `modal.md` |
| Drawer | `drawer.md` |
| Dropdown | `dropdown.md` |
| Tooltip | `tooltip.md` |
| Popover | `popover.md` |

#### 3.6 Patterns (`01-components/patterns/`)

Composite patterns:

| Component | File |
|-----------|------|
| Form | `form.md` |
| Search | `search.md` |
| Filter | `filter.md` |
| Data Table | `data-table.md` |
| Dashboard Card | `dashboard-card.md` |

### Step 4: Generate Component Specifications

Each component file follows this template with **Requirements Addressed as FIRST section**:

```markdown
# [Component Name]

## ⚡ Requirements Addressed

> **MANDATORY FIRST SECTION** - Must appear before any other content

| Requirement | Description | Priority |
|-------------|-------------|----------|
| US-001 | Save inventory item | P0 |
| US-005 | Submit form data | P0 |
| FR-012 | Confirm destructive actions | P1 |

## Overview

Brief description of the component and its purpose.

## Visual Treatment

| Property | Value | Token Reference |
|----------|-------|-----------------|
| Background | Primary blue | `color.primary.500` |
| Border Radius | 8px | `borderRadius.md` |
| Shadow | Subtle lift | `shadow.sm` |
| Hover Effect | Darken 10% | `color.primary.600` |

**Aesthetic Direction**: Modern, professional with subtle depth

## Variants

| Variant | Description | Use Case |
|---------|-------------|----------|
| primary | Main action style | Primary CTAs |
| secondary | Supporting action | Secondary actions |
| ghost | Minimal style | Tertiary actions |
| destructive | Danger action | Delete, remove |

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | 'primary' \| 'secondary' \| 'ghost' \| 'destructive' | 'primary' | Visual style |
| size | 'sm' \| 'md' \| 'lg' | 'md' | Component size |
| disabled | boolean | false | Disable interaction |
| loading | boolean | false | Show loading state |

## Token Mapping

| Design Token | CSS Property | Value |
|--------------|--------------|-------|
| `color.primary.500` | background-color | #2563EB |
| `color.primary.600` | hover:background-color | #1D4ED8 |
| `spacing.2` | padding-left, padding-right | 8px |
| `spacing.1` | padding-top, padding-bottom | 4px |
| `borderRadius.md` | border-radius | 6px |
| `typography.fontSize.sm` | font-size | 14px |
| `typography.fontWeight.medium` | font-weight | 500 |

## States

| State | Description | Visual Treatment |
|-------|-------------|------------------|
| Default | Initial state | Base styling |
| Hover | Mouse over | Darker background |
| Active | Mouse down | Even darker |
| Focus | Keyboard focus | Focus ring |
| Disabled | Non-interactive | Reduced opacity |
| Loading | Processing | Spinner + disabled |

## Accessibility

- **Role:** button
- **Keyboard:** Space/Enter to activate, Tab to navigate
- **Focus:** Visible focus ring (2px primary-500, 2px offset)
- **Screen Reader:** Announces label, state, and loading status
- **ARIA:** `aria-disabled`, `aria-busy` when loading

## Examples

### Primary Button

```jsx
<Button variant="primary" size="md">
  Save Changes
</Button>
```

### With Loading State

```jsx
<Button variant="primary" loading>
  Saving...
</Button>
```

### Destructive Action

```jsx
<Button variant="destructive" onClick={handleDelete}>
  Delete Item
</Button>
```
```

### Step 5: Generate Component Index

Create `01-components/component-index.md`:

```markdown
# Component Library Index

## Overview

This component library provides the building blocks for the <SystemName> prototype.

## Component Count

| Category | Count |
|----------|-------|
| Primitives | 9 |
| Data Display | 6 |
| Feedback | 5 |
| Navigation | 5 |
| Overlays | 5 |
| Patterns | 5 |
| **Total** | **35** |

## Quick Reference

### Primitives

| Component | File | Description |
|-----------|------|-------------|
| Button | [button.md](primitives/button.md) | Interactive button element |
| Input | [input.md](primitives/input.md) | Text input field |
| Select | [select.md](primitives/select.md) | Dropdown selection |
...

### Data Display

| Component | File | Description |
|-----------|------|-------------|
| Table | [table.md](data-display/table.md) | Tabular data display |
| Card | [card.md](data-display/card.md) | Content container |
...

### Feedback

| Component | File | Description |
|-----------|------|-------------|
| Alert | [alert.md](feedback/alert.md) | Inline messages |
| Toast | [toast.md](feedback/toast.md) | Temporary notifications |
...

### Navigation

| Component | File | Description |
|-----------|------|-------------|
| Sidebar | [sidebar.md](navigation/sidebar.md) | Main navigation |
| Header | [header.md](navigation/header.md) | Top bar |
...

### Overlays

| Component | File | Description |
|-----------|------|-------------|
| Modal | [modal.md](overlays/modal.md) | Dialog window |
| Drawer | [drawer.md](overlays/drawer.md) | Side panel |
...

### Patterns

| Component | File | Description |
|-----------|------|-------------|
| Form | [form.md](patterns/form.md) | Form layout pattern |
| Data Table | [data-table.md](patterns/data-table.md) | Sortable, filterable table |
...

## Design Token Integration

All components reference tokens from `00-foundation/design-tokens.json`.

## Accessibility Standards

All components meet WCAG 2.1 AA requirements per `00-foundation/design-principles.md`.
```

### Step 6: Update Traceability

Update `_state/requirements_registry.json`:
- Add `component_refs` to requirements that map to components

Update `traceability/prototype_traceability_register.json`:
- Add components to `artifacts.components`

### Step 7: Validate Checkpoint 8

```bash
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 8 --dir Prototype_<SystemName>/
```

**Validation Criteria**:
- `01-components/component-index.md` exists
- At least 5 component specs exist
- Each spec has: Overview, Props, States, Accessibility
- `primitives/` folder has at least 3 components
- `data-display/` folder has at least 2 components

### Step 8: Update Progress

```json
{
  "current_phase": 9,
  "phases": {
    "components": {
      "status": "completed",
      "completed_at": "<timestamp>",
      "outputs": [
        "01-components/component-index.md",
        "01-components/primitives/button.md",
        ...
      ]
    }
  }
}
```

### Step 9: Display Summary

```
═══════════════════════════════════════════════════════
  COMPONENT SPECIFICATIONS COMPLETE (Phase 8)
═══════════════════════════════════════════════════════

  Components Specified:

  ├── Primitives:      9 components
  │   └── button, input, select, checkbox, radio,
  │       toggle, badge, avatar, icon
  │
  ├── Data Display:    6 components
  │   └── table, card, list, stat, chart, empty-state
  │
  ├── Feedback:        5 components
  │   └── alert, toast, progress, skeleton, spinner
  │
  ├── Navigation:      5 components
  │   └── sidebar, header, breadcrumb, tabs, pagination
  │
  ├── Overlays:        5 components
  │   └── modal, drawer, dropdown, tooltip, popover
  │
  └── Patterns:        5 components
      └── form, search, filter, data-table, dashboard-card

  Total:               35 component specifications

  Checkpoint 8:        ✅ PASSED

═══════════════════════════════════════════════════════

  Output: 01-components/

  Next: /prototype-screens or /prototype <SystemName>

═══════════════════════════════════════════════════════
```

## Outputs

| Folder | Purpose |
|--------|---------|
| `01-components/component-index.md` | Component library index |
| `01-components/COMPONENT_LIBRARY_SUMMARY.md` | **Executive summary with metrics** |
| `01-components/primitives/` | Basic building blocks |
| `01-components/data-display/` | Data visualization components |
| `01-components/feedback/` | User feedback components |
| `01-components/navigation/` | Navigation components |
| `01-components/overlays/` | Overlay components |
| `01-components/patterns/` | Composite patterns |

### COMPONENT_LIBRARY_SUMMARY.md

This summary file provides:

```markdown
# Component Library Summary

## Overview

| Metric | Value |
|--------|-------|
| Total Components | 41 |
| Categories | 6 |
| Requirements Covered | 28/32 (87.5%) |
| Accessibility Compliance | WCAG AA |

## Category Breakdown

| Category | Count | Key Components |
|----------|-------|----------------|
| Primitives | 9 | Button, Input, Select, Checkbox |
| Data Display | 7 | Table, Card, List, Stat, Chart |
| Feedback | 5 | Alert, Toast, Progress, Spinner |
| Navigation | 6 | Sidebar, Header, Breadcrumb, Tabs |
| Overlays | 5 | Modal, Drawer, Dropdown, Tooltip |
| Patterns | 9 | Form, DataTable, Dashboard Card |

## Requirements Coverage

| Priority | Covered | Total | % |
|----------|---------|-------|---|
| P0 | 15 | 15 | 100% |
| P1 | 10 | 12 | 83% |
| P2 | 3 | 5 | 60% |

## Components by Screen Usage

| Screen | Components Used |
|--------|-----------------|
| Dashboard | 12 |
| Inventory List | 8 |
| Inventory Detail | 10 |
| Stock Movement | 7 |

## Design Token Integration

All components reference tokens from `00-foundation/design-tokens.json`
```

## Error Handling

| Error | Action |
|-------|--------|
| Design tokens missing | **BLOCK** - Run /prototype-design first |
| Component generation fails | Log, skip to next component |

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype-design` | Run Phases 6-7 |
| `/prototype-screens` | Run Phase 9 |
| `/prototype` | Run full prototype |

### Step 10: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/prototype-components" \
  --stage "prototype" \
  --status "completed" \

echo "✅ Logged command completion"
```
