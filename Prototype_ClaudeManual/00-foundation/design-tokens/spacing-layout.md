# Spacing & Layout System - ClaudeManual

---
system_name: ClaudeManual
version: 1.0.0
date_created: 2026-01-31
checkpoint: CP-6
base_unit: 4px
grid_system: 4px base grid
scale: Linear (4/8/12/16/24/32/48/64/80/96)
---

## Overview

The ClaudeManual spacing system uses a **4px base unit** for consistent rhythm and alignment. All spacing values are multiples of 4px to maintain visual harmony across components and layouts.

**Key Features**:
- 4px base grid
- Linear scale for predictability
- Consistent component spacing
- Responsive layout breakpoints
- Terminal-inspired minimalism (CF-014)

---

## Spacing Scale

All spacing values are multiples of **4px** (0.25rem).

| Token | rem | px | Use Case |
|-------|-----|----|----|
| `spacing.0` | 0 | 0 | Reset, no spacing |
| `spacing.1` | 0.25rem | 4px | Icon padding, tight spacing |
| `spacing.2` | 0.5rem | 8px | Input padding, small gaps |
| `spacing.3` | 0.75rem | 12px | Button padding (vertical) |
| `spacing.4` | 1rem | 16px | Default gap, button padding (horizontal) |
| `spacing.5` | 1.25rem | 20px | Card padding (small) |
| `spacing.6` | 1.5rem | 24px | Section gaps |
| `spacing.8` | 2rem | 32px | Card padding (default) |
| `spacing.10` | 2.5rem | 40px | Component margins |
| `spacing.12` | 3rem | 48px | Section padding |
| `spacing.16` | 4rem | 64px | Large section gaps |
| `spacing.20` | 5rem | 80px | Hero section padding |
| `spacing.24` | 6rem | 96px | Page section padding |

**Formula**: spacing[N] = N × 4px

---

## Component Spacing

### Buttons

```css
/* Default Button */
padding: spacing.3 spacing.4; /* 12px 16px */
gap: spacing.2; /* 8px between icon and text */

/* Large Button */
padding: spacing.4 spacing.6; /* 16px 24px */

/* Small Button */
padding: spacing.2 spacing.3; /* 8px 12px */
```

**Visual**:
```
┌─────────────────────┐
│  [Icon] Copy Path   │  padding: 12px 16px
└─────────────────────┘
     8px gap
```

### Cards

```css
/* Card Padding */
padding: spacing.8; /* 32px */

/* Card Gap (between cards) */
gap: spacing.6; /* 24px */

/* Compact Card */
padding: spacing.5; /* 20px */
```

**Visual**:
```
┌─────────────────────────────────┐
│                                 │
│  Card Content (32px padding)    │
│                                 │
└─────────────────────────────────┘
       24px gap
┌─────────────────────────────────┐
│  Card Content                   │
└─────────────────────────────────┘
```

### Navigation Tree

```css
/* Tree Item Padding */
padding: spacing.2 spacing.3; /* 8px 12px */

/* Indentation per level */
padding-left: calc(spacing.4 * level); /* 16px per level */

/* Gap between tree items */
gap: spacing.1; /* 4px */
```

**Visual**:
```
▼ Skills
  ├ Discovery_JTBD        (padding: 8px 12px)
  │                       (4px gap)
  ├ Discovery_Persona     (indented 16px)
  └ ...
```

### Detail Pane

```css
/* Content Padding */
padding: spacing.8; /* 32px */

/* Section Gap */
margin-bottom: spacing.6; /* 24px */

/* Heading Margins */
margin-top: spacing.8; /* 32px */
margin-bottom: spacing.4; /* 16px */
```

### Search Results

```css
/* Result Card */
padding: spacing.4; /* 16px */
gap: spacing.3; /* 12px between elements */

/* Result List Gap */
gap: spacing.3; /* 12px between cards */
```

### Toast Notifications

```css
/* Toast Padding */
padding: spacing.4 spacing.6; /* 16px 24px */

/* Toast Gap (between icon and text) */
gap: spacing.3; /* 12px */
```

**Visual**:
```
┌──────────────────────────────────┐
│ ✅  Copied to clipboard          │  padding: 16px 24px
└──────────────────────────────────┘
       12px gap between icon & text
```

### Badges

```css
/* Badge Padding */
padding: spacing.1 spacing.2; /* 4px 8px */

/* Badge Gap (in list) */
gap: spacing.2; /* 8px */
```

**Visual**:
```
[DISCOVERY] [P0] [SKILL]
  8px gap    8px gap
padding: 4px 8px
```

---

## Layout Tokens

### Panel Widths

| Token | Value | Use Case |
|-------|-------|----------|
| `layout.tree-width` | 300px | Navigation tree panel (desktop) |
| `layout.header-height` | 64px | Header bar height |
| `layout.footer-height` | 48px | Footer bar height |
| `layout.max-width` | 1920px | Maximum content width |

### Breakpoints

| Token | Value | Range | Device |
|-------|-------|-------|--------|
| `breakpoints.mobile` | 768px | < 768px | Mobile phones |
| `breakpoints.tablet` | 1024px | 768-1024px | Tablets, small laptops |
| `breakpoints.desktop` | 1280px | > 1024px | Desktops, large laptops |

**Responsive Behavior**:
```css
/* Mobile (< 768px) */
@media (max-width: 768px) {
  .tree-panel {
    width: 100%; /* Full-width drawer */
  }
  .detail-pane {
    padding: spacing.4; /* Reduced padding */
  }
}

/* Tablet (768-1024px) */
@media (min-width: 768px) and (max-width: 1024px) {
  .tree-panel {
    width: 250px; /* Narrower tree */
  }
}

/* Desktop (> 1024px) */
@media (min-width: 1024px) {
  .tree-panel {
    width: 300px; /* Full tree width */
  }
}
```

---

## Grid System

The layout uses a **4px base grid** for alignment.

### Grid Columns

```css
/* Master-Detail Layout (Desktop) */
display: grid;
grid-template-columns: 300px 1fr; /* Tree + Detail */
gap: spacing.6; /* 24px gutter */

/* Responsive Grid (Tablet) */
@media (max-width: 1024px) {
  grid-template-columns: 1fr; /* Stack layout */
}
```

### Grid Alignment

All components align to the 4px grid:
```css
/* Component positioning */
margin-top: spacing.4; /* 16px = 4 × 4px */
padding: spacing.8; /* 32px = 8 × 4px */
gap: spacing.6; /* 24px = 6 × 4px */
```

---

## Visual Rhythm

### Vertical Rhythm

Consistent vertical spacing creates visual flow:

```
┌─────────────────────────────────┐
│ Header (64px height)            │
├─────────────────────────────────┤
│                                 │ 32px padding
│ # Heading                       │
│                                 │ 16px margin-bottom
│ Paragraph text with 1.5 line    │
│ height for optimal readability. │
│                                 │ 24px section gap
│ ## Subheading                   │
│                                 │ 16px margin-bottom
│ More content...                 │
│                                 │ 32px padding
└─────────────────────────────────┘
```

**Rule**: Use consistent spacing tokens (4/8/12/16/24/32) for predictable rhythm.

### Horizontal Rhythm

```
┌─────────────────────────────────────────────┐
│ 32px │ Content Area         │ 32px          │
│ padding                      padding        │
│                                             │
│      [Button] 12px gap [Button]            │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Responsive Spacing

### Mobile Adjustments (< 768px)

| Desktop | Mobile | Reduction |
|---------|--------|-----------|
| `spacing.24` (96px) | `spacing.12` (48px) | 50% |
| `spacing.16` (64px) | `spacing.10` (40px) | 37.5% |
| `spacing.12` (48px) | `spacing.8` (32px) | 33% |
| `spacing.8` (32px) | `spacing.4` (16px) | 50% |
| `spacing.6` (24px) | `spacing.4` (16px) | 33% |
| `spacing.4` (16px) | `spacing.4` (16px) | 0% (unchanged) |

**Implementation**:
```css
/* Desktop */
.section {
  padding: spacing.12; /* 48px */
}

/* Mobile */
@media (max-width: 768px) {
  .section {
    padding: spacing.8; /* 32px */
  }
}
```

---

## Z-Index Scale

Layering for overlays and modals:

| Token | Value | Use Case |
|-------|-------|----------|
| `zIndex.base` | 0 | Default layer |
| `zIndex.dropdown` | 1000 | Search results dropdown |
| `zIndex.sticky` | 1100 | Sticky header |
| `zIndex.modal` | 1200 | Modal backdrop |
| `zIndex.popover` | 1300 | Popovers, tooltips |
| `zIndex.toast` | 1400 | Toast notifications |
| `zIndex.tooltip` | 1500 | Tooltips (always on top) |

**Rationale**: 100-unit increments allow inserting layers between existing values.

---

## Border Radius

| Token | Value | Use Case |
|-------|-------|----------|
| `borderRadius.none` | 0 | Sharp corners |
| `borderRadius.sm` | 2px | Badges, chips |
| `borderRadius.md` | 6px | Buttons, cards (default) |
| `borderRadius.lg` | 8px | Modals, large cards |
| `borderRadius.xl` | 12px | Feature cards |
| `borderRadius.2xl` | 16px | Hero sections |
| `borderRadius.full` | 9999px | Pill buttons, avatars |

**Visual Examples**:
```
┌──────────┐    ╭──────────╮    ╭──────────╮
│  none    │    │   md     │    │   lg     │
│   0px    │    │   6px    │    │   8px    │
└──────────┘    ╰──────────╯    ╰──────────╯

 ╭─────────────────╮    ╭─────────────╮
 │      2xl        │    │    full     │
 │      16px       │    │   9999px    │
 ╰─────────────────╯    ╰─────────────╯
```

---

## Shadow System

| Token | Value | Use Case | Elevation |
|-------|-------|----------|-----------|
| `shadow.sm` | `0 1px 2px 0 rgb(0 0 0 / 0.05)` | Subtle hover | 1dp |
| `shadow.md` | `0 4px 6px -1px rgb(0 0 0 / 0.1)` | Cards, dropdowns | 4dp |
| `shadow.lg` | `0 10px 15px -3px rgb(0 0 0 / 0.1)` | Modals | 8dp |
| `shadow.xl` | `0 20px 25px -5px rgb(0 0 0 / 0.1)` | High elevation | 16dp |
| `shadow.inner` | `inset 0 2px 4px 0 rgb(0 0 0 / 0.05)` | Input fields | Inset |
| `shadow.focus` | `0 0 0 3px rgb(59 130 246 / 0.5)` | Focus ring | N/A |

**Elevation Hierarchy**:
```
┌─────────────────────────────────┐
│                                 │  shadow.xl (modal)
│  ┌───────────────────────────┐  │
│  │                           │  │  shadow.lg (dropdown)
│  │  ┌─────────────────────┐  │  │
│  │  │ shadow.md (card)    │  │  │
│  │  │                     │  │  │
│  │  └─────────────────────┘  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

---

## Animation Tokens

### Duration

| Token | Value | Use Case |
|-------|-------|----------|
| `motion.duration.instant` | 0ms | No animation |
| `motion.duration.fast` | 100ms | Micro-interactions (hover) |
| `motion.duration.normal` | 200ms | Default transitions (expand/collapse) |
| `motion.duration.slow` | 300ms | Panel slides, page transitions |
| `motion.duration.slower` | 500ms | Large animations, loaders |

### Easing

| Token | Value | Use Case |
|-------|-------|----------|
| `motion.easing.linear` | `linear` | Progress bars, spinners |
| `motion.easing.ease` | `ease` | Default easing |
| `motion.easing.ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | Fade out, collapse |
| `motion.easing.ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | Fade in, expand |
| `motion.easing.ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Smooth start/end |

**Implementation**:
```css
/* Tree expand animation */
.tree-item-children {
  transition: max-height 200ms ease-out;
}

/* Panel slide */
.drawer {
  transition: transform 300ms ease-in-out;
}

/* Hover state */
.button:hover {
  transition: background-color 100ms ease;
}
```

---

## Usage Guidelines

### Do's ✓
- Use spacing scale tokens consistently (avoid hardcoded values)
- Maintain 4px grid alignment for all components
- Reduce spacing by 33-50% on mobile for compact layouts
- Use consistent elevation hierarchy (shadow.sm → md → lg → xl)
- Apply focus ring (`shadow.focus`) to all interactive elements

### Don'ts ✗
- Do not use arbitrary spacing values (e.g., 13px, 27px)
- Do not exceed `spacing.24` (96px) for component padding
- Do not stack more than 3 shadow levels
- Do not animate margin/padding (use transform for performance)
- Do not reduce spacing below `spacing.1` (4px) for touch targets

---

## Implementation Example (CSS)

```css
/* Spacing Tokens */
:root {
  --spacing-0: 0;
  --spacing-1: 0.25rem; /* 4px */
  --spacing-2: 0.5rem; /* 8px */
  --spacing-3: 0.75rem; /* 12px */
  --spacing-4: 1rem; /* 16px */
  --spacing-5: 1.25rem; /* 20px */
  --spacing-6: 1.5rem; /* 24px */
  --spacing-8: 2rem; /* 32px */
  --spacing-10: 2.5rem; /* 40px */
  --spacing-12: 3rem; /* 48px */
  --spacing-16: 4rem; /* 64px */
  --spacing-20: 5rem; /* 80px */
  --spacing-24: 6rem; /* 96px */

  /* Layout */
  --layout-tree-width: 300px;
  --layout-header-height: 64px;
  --layout-max-width: 1920px;

  /* Border Radius */
  --radius-sm: 0.125rem; /* 2px */
  --radius-md: 0.375rem; /* 6px */
  --radius-lg: 0.5rem; /* 8px */
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-focus: 0 0 0 3px rgb(59 130 246 / 0.5);

  /* Motion */
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --easing-ease-out: cubic-bezier(0, 0, 0.2, 1);
}

/* Component Examples */
.button {
  padding: var(--spacing-3) var(--spacing-4);
  border-radius: var(--radius-md);
  transition: background-color var(--duration-fast) ease;
}

.card {
  padding: var(--spacing-8);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.tree-item {
  padding: var(--spacing-2) var(--spacing-3);
  border-radius: var(--radius-sm);
  transition: background-color var(--duration-normal) var(--easing-ease-out);
}

.badge {
  padding: var(--spacing-1) var(--spacing-2);
  border-radius: var(--radius-sm);
}
```

---

## Traceability

- **Source**: ClientAnalysis_ClaudeManual/04-design-specs/interaction-patterns.md
- **JTBD**: JTBD-1.1 (Self-service learning), JTBD-1.7 (Visual hierarchy)
- **Client Facts**: CF-006 (Master-detail panes), CF-014 (Minimalistic)
- **Requirements**: REQ-019 (Spacing system), REQ-020 (Accessibility)
- **Checkpoint**: CP-6 (Design Tokens)

---

*Spacing & layout system v1.0.0 with 4px base grid, linear scale, responsive breakpoints, and elevation hierarchy.*
