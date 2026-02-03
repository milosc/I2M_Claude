# Design Tokens - ClaudeManual

**Version**: 1.0.0
**System**: ClaudeManual
**Generated**: 2026-01-31
**Checkpoint**: CP-6
**Themes**: 2 (light, dark)

---

## Overview

This folder contains the complete design token system for ClaudeManual, a terminal-inspired framework documentation UI. The token system supports stage-based color coding, light/dark themes, responsive typography, and WCAG AA accessibility standards.

---

## Files

| File | Description |
|------|-------------|
| **tokens.json** | Master design tokens file (Tailwind-compatible) |
| **color-system.md** | Color palette, stage colors, WCAG compliance report |
| **typography.md** | Type scale, font families, responsive sizing |
| **spacing-layout.md** | 4px grid, spacing scale, layout tokens, shadows |

---

## Token Categories

### 1. Color System
- **Stage colors**: Discovery (blue), Prototype (green), ProductSpecs (orange), SolArch (red), Implementation (purple)
- **Semantic colors**: Success, warning, error, info
- **Theme support**: Light and dark mode variants
- **WCAG compliance**: All text combinations meet AA standards (4.5:1 contrast ratio)

**See**: `color-system.md`

### 2. Typography
- **Primary font**: JetBrains Mono (monospace, terminal-inspired)
- **Type scale**: 1.25x ratio (8 sizes: xs/sm/base/lg/xl/2xl/3xl/4xl)
- **Font weights**: Normal (400), Medium (500), Semibold (600), Bold (700)
- **Line heights**: Tight (1.25), Normal (1.5), Relaxed (1.75)
- **Responsive sizing**: Mobile reductions for headings

**See**: `typography.md`

### 3. Spacing & Layout
- **Base unit**: 4px grid
- **Spacing scale**: 0/4/8/12/16/20/24/32/40/48/64/80/96
- **Layout tokens**: Tree width (300px), header height (64px), max-width (1920px)
- **Border radius**: sm (2px), md (6px), lg (8px), xl (12px), full (9999px)
- **Shadows**: sm/md/lg/xl elevation levels
- **Animation**: Duration (100/200/300/500ms), easing functions

**See**: `spacing-layout.md`

---

## Quick Reference

### Stage Colors (Light Theme)

| Stage | Color | Hex |
|-------|-------|-----|
| Discovery | Blue | `#3b82f6` |
| Prototype | Green | `#22c55e` |
| ProductSpecs | Orange | `#f97316` |
| SolArch | Red | `#ef4444` |
| Implementation | Purple | `#a855f7` |

### Typography Scale

| Token | Size | Use Case |
|-------|------|----------|
| `xs` | 12px | Badges, micro-copy |
| `sm` | 14px | Labels, small text |
| `base` | 16px | Body text (default) |
| `lg` | 18px | Large body |
| `xl` | 20px | H3 |
| `2xl` | 24px | H2 |
| `3xl` | 30px | H1 |
| `4xl` | 36px | Display headings |

### Spacing Scale

| Token | Size | Use Case |
|-------|------|----------|
| `1` | 4px | Icon padding |
| `2` | 8px | Input padding |
| `3` | 12px | Button padding (vertical) |
| `4` | 16px | Default gap |
| `6` | 24px | Section gaps |
| `8` | 32px | Card padding |
| `12` | 48px | Section padding |
| `16` | 64px | Large gaps |

---

## Usage

### Import Design Tokens

```javascript
import tokens from './tokens.json';

// Access color tokens
const discoveryColor = tokens.color.stage.discovery.light.value; // #3b82f6

// Access spacing tokens
const cardPadding = tokens.spacing['8'].value; // 2rem (32px)

// Access typography tokens
const headingSize = tokens.typography.fontSize['3xl'].value; // 1.875rem (30px)
```

### CSS Variables (Example)

```css
:root {
  /* Stage Colors */
  --color-stage-discovery: #3b82f6;
  --color-stage-prototype: #22c55e;
  --color-stage-productspecs: #f97316;
  --color-stage-solarch: #ef4444;
  --color-stage-implementation: #a855f7;

  /* Typography */
  --font-mono: 'JetBrains Mono', monospace;
  --text-base: 1rem;
  --text-xl: 1.25rem;

  /* Spacing */
  --spacing-4: 1rem; /* 16px */
  --spacing-8: 2rem; /* 32px */

  /* Shadows */
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
}

/* Component Example */
.badge-discovery {
  background: var(--color-stage-discovery);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  padding: var(--spacing-1) var(--spacing-2);
  color: white;
}
```

---

## Tailwind Configuration

To use these tokens with Tailwind CSS, extend your `tailwind.config.js`:

```javascript
const tokens = require('./design-tokens/tokens.json');

module.exports = {
  theme: {
    extend: {
      colors: {
        discovery: tokens.color.stage.discovery.light.value,
        prototype: tokens.color.stage.prototype.light.value,
        productspecs: tokens.color.stage.productspecs.light.value,
        solarch: tokens.color.stage.solarch.light.value,
        implementation: tokens.color.stage.implementation.light.value,
      },
      fontFamily: {
        mono: tokens.typography.fontFamily.mono.value.split(', '),
      },
      spacing: {
        1: tokens.spacing['1'].value,
        2: tokens.spacing['2'].value,
        3: tokens.spacing['3'].value,
        4: tokens.spacing['4'].value,
        6: tokens.spacing['6'].value,
        8: tokens.spacing['8'].value,
        12: tokens.spacing['12'].value,
        16: tokens.spacing['16'].value,
      },
      borderRadius: {
        sm: tokens.borderRadius.sm.value,
        md: tokens.borderRadius.md.value,
        lg: tokens.borderRadius.lg.value,
      },
      boxShadow: {
        sm: tokens.shadow.sm.value,
        md: tokens.shadow.md.value,
        lg: tokens.shadow.lg.value,
        focus: tokens.shadow.focus.value,
      },
    },
  },
};
```

---

## Accessibility

All design tokens meet **WCAG 2.1 AA** standards:

- **Text contrast**: Minimum 4.5:1 for normal text, 3:1 for large text (18px+)
- **Interactive elements**: Minimum 3:1 contrast ratio
- **Focus indicators**: 2px outline with `shadow.focus` token
- **Font scaling**: Supports browser zoom up to 200%
- **Color + icon**: Never use color alone for meaning (add icons/labels)

---

## Design Principles

### 1. Terminal-Inspired Aesthetic (CF-014)
- Monospace primary font (JetBrains Mono)
- Clean, minimalistic UI
- Subtle shadows (avoid heavy drop shadows)

### 2. Stage-Based Color Coding
- Each framework stage has a dedicated color
- Improves visual navigation (JTBD-1.7)
- Reduces cognitive load (JTBD-1.4)

### 3. 4px Base Grid
- All spacing is a multiple of 4px
- Consistent rhythm and alignment
- Predictable visual hierarchy

### 4. WCAG AA Compliance
- All text combinations tested for contrast
- Accessible focus indicators
- Support for reduced motion preferences

---

## Traceability

- **Source**: ClientAnalysis_ClaudeManual/04-design-specs/
- **JTBD**: JTBD-1.1, JTBD-1.2, JTBD-1.4, JTBD-1.7
- **Client Facts**: CF-011 (Stage organization), CF-014 (Terminal look), CF-016 (Light/dark themes)
- **Requirements**: REQ-015, REQ-018, REQ-019, REQ-020
- **Checkpoint**: CP-6 (Design Tokens)

---

## Next Steps

1. **Component Library**: Use tokens to build React components
2. **Theme Switcher**: Implement light/dark mode toggle using tokens
3. **Responsive Testing**: Validate spacing scale on mobile/tablet/desktop
4. **Accessibility Audit**: Test with screen readers and keyboard navigation
5. **Documentation**: Generate Storybook stories for component token usage

---

**Design token system complete. Ready for component implementation (CP-7).**
