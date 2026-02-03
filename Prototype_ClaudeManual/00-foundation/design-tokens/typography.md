# Typography System - ClaudeManual

---
system_name: ClaudeManual
version: 1.0.0
date_created: 2026-01-31
checkpoint: CP-6
font_family: JetBrains Mono (monospace)
type_scale: 1.25x ratio
responsive: Yes
---

## Overview

The ClaudeManual typography system uses **monospace fonts** to create a terminal-inspired aesthetic (CF-014) that appeals to developer audiences. The type scale follows a **1.25x ratio** for consistent visual hierarchy and responsive sizing.

**Key Features**:
- Monospace primary font (JetBrains Mono)
- 1.25x modular scale (8 sizes)
- Responsive line heights
- Clear visual hierarchy
- Developer-friendly readability

---

## Font Families

### Primary: Monospace

```
Font Stack: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco', monospace
```

**Use Cases**:
- All body text
- Headings
- Code blocks
- Navigation labels
- Button text
- Badges

**Rationale**: Monospace fonts evoke a terminal aesthetic (CF-014), align with developer workflows, and provide excellent readability for code examples.

### Fallback: Sans-Serif

```
Font Stack: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif
```

**Use Cases**:
- Long-form documentation (optional)
- Marketing pages (if needed)

**Rationale**: Provides fallback for environments where monospace may reduce readability in paragraphs.

---

## Type Scale

The type scale uses a **1.25x ratio** (Major Third) for harmonious sizing relationships.

| Size | Token | rem | px | Use Case |
|------|-------|-----|----|----|
| **4xl** | `fontSize.4xl` | 2.25rem | 36px | Display headings, hero text |
| **3xl** | `fontSize.3xl` | 1.875rem | 30px | Page titles (H1) |
| **2xl** | `fontSize.2xl` | 1.5rem | 24px | Section headings (H2) |
| **xl** | `fontSize.xl` | 1.25rem | 20px | Subsection headings (H3) |
| **lg** | `fontSize.lg` | 1.125rem | 18px | Large body text, lead paragraphs |
| **base** | `fontSize.base` | 1rem | 16px | Body text (default) |
| **sm** | `fontSize.sm` | 0.875rem | 14px | Small labels, captions |
| **xs** | `fontSize.xs` | 0.75rem | 12px | Badges, micro-copy |

**Formula**: Next size = Previous size × 1.25

---

## Font Weights

| Weight | Token | Value | Use Case |
|--------|-------|-------|----------|
| **Normal** | `fontWeight.normal` | 400 | Body text, paragraphs |
| **Medium** | `fontWeight.medium` | 500 | Navigation labels, emphasis |
| **Semibold** | `fontWeight.semibold` | 600 | Subheadings (H3-H5) |
| **Bold** | `fontWeight.bold` | 700 | Headings (H1-H2), CTAs |

**Note**: JetBrains Mono supports weights 100-800. We limit to 400-700 for consistency.

---

## Line Heights

| Token | Value | Use Case |
|-------|-------|----------|
| **Tight** | 1.25 | Headings, short text |
| **Normal** | 1.5 | Body text (default) |
| **Relaxed** | 1.75 | Long-form content, documentation |

**Rationale**:
- Tight line height (1.25) for headings prevents excessive vertical space
- Normal (1.5) for body text ensures readability
- Relaxed (1.75) for long paragraphs improves scannability

---

## Letter Spacing

| Token | Value | Use Case |
|-------|-------|----------|
| **Tight** | -0.025em | Large headings (H1-H2) |
| **Normal** | 0em | Body text (default) |
| **Wide** | 0.05em | Uppercase text, badges, labels |

**Rationale**: Tight spacing for large headings creates visual density; wide spacing for all-caps text improves readability.

---

## Typography Styles

### Heading Styles

#### H1 (Page Title)
```css
font-family: 'JetBrains Mono', monospace;
font-size: 1.875rem; /* 30px */
font-weight: 700; /* Bold */
line-height: 1.25; /* Tight */
letter-spacing: -0.025em; /* Tight */
color: var(--color-text-primary);
```

**Example**:
```
# ClaudeManual
```

#### H2 (Section Heading)
```css
font-family: 'JetBrains Mono', monospace;
font-size: 1.5rem; /* 24px */
font-weight: 700; /* Bold */
line-height: 1.25; /* Tight */
letter-spacing: -0.025em; /* Tight */
color: var(--color-text-primary);
```

**Example**:
```
## Navigation Patterns
```

#### H3 (Subsection Heading)
```css
font-family: 'JetBrains Mono', monospace;
font-size: 1.25rem; /* 20px */
font-weight: 600; /* Semibold */
line-height: 1.25; /* Tight */
letter-spacing: 0em; /* Normal */
color: var(--color-text-primary);
```

**Example**:
```
### Keyboard Shortcuts
```

#### H4 (Minor Heading)
```css
font-family: 'JetBrains Mono', monospace;
font-size: 1rem; /* 16px */
font-weight: 600; /* Semibold */
line-height: 1.5; /* Normal */
letter-spacing: 0em; /* Normal */
color: var(--color-text-primary);
```

---

### Body Text Styles

#### Body Large (Lead Paragraph)
```css
font-family: 'JetBrains Mono', monospace;
font-size: 1.125rem; /* 18px */
font-weight: 400; /* Normal */
line-height: 1.75; /* Relaxed */
letter-spacing: 0em; /* Normal */
color: var(--color-text-primary);
```

**Use Case**: Introductory paragraphs, summaries

#### Body Default
```css
font-family: 'JetBrains Mono', monospace;
font-size: 1rem; /* 16px */
font-weight: 400; /* Normal */
line-height: 1.5; /* Normal */
letter-spacing: 0em; /* Normal */
color: var(--color-text-primary);
```

**Use Case**: Paragraphs, lists, general content

#### Body Small
```css
font-family: 'JetBrains Mono', monospace;
font-size: 0.875rem; /* 14px */
font-weight: 400; /* Normal */
line-height: 1.5; /* Normal */
letter-spacing: 0em; /* Normal */
color: var(--color-text-secondary);
```

**Use Case**: Captions, helper text, labels

---

### UI Component Styles

#### Navigation Label
```css
font-family: 'JetBrains Mono', monospace;
font-size: 0.875rem; /* 14px */
font-weight: 500; /* Medium */
line-height: 1.5; /* Normal */
letter-spacing: 0em; /* Normal */
color: var(--color-text-primary);
```

#### Button Text
```css
font-family: 'JetBrains Mono', monospace;
font-size: 0.875rem; /* 14px */
font-weight: 600; /* Semibold */
line-height: 1.5; /* Normal */
letter-spacing: 0.05em; /* Wide */
color: var(--color-text-on-primary);
text-transform: uppercase;
```

**Rationale**: Uppercase + wide spacing improves legibility for short button labels.

#### Badge Text
```css
font-family: 'JetBrains Mono', monospace;
font-size: 0.75rem; /* 12px */
font-weight: 600; /* Semibold */
line-height: 1; /* Tight */
letter-spacing: 0.05em; /* Wide */
color: white;
text-transform: uppercase;
```

**Example**: `DISCOVERY` `PROTOTYPE` `P0`

#### Code Inline
```css
font-family: 'JetBrains Mono', monospace;
font-size: 0.875rem; /* 14px */
font-weight: 400; /* Normal */
line-height: 1.5; /* Normal */
letter-spacing: 0em; /* Normal */
color: var(--color-text-primary);
background: var(--color-bg-tertiary);
padding: 0.125rem 0.25rem;
border-radius: 0.25rem;
```

**Example**: `npm install` `.claude/skills/Discovery_JTBD/SKILL.md`

#### Code Block
```css
font-family: 'JetBrains Mono', monospace;
font-size: 0.875rem; /* 14px */
font-weight: 400; /* Normal */
line-height: 1.75; /* Relaxed */
letter-spacing: 0em; /* Normal */
color: var(--color-text-primary);
background: var(--color-bg-secondary);
padding: 1rem;
border-radius: 0.5rem;
overflow-x: auto;
```

---

## Responsive Typography

### Mobile (< 768px)

| Size | Desktop | Mobile | Ratio |
|------|---------|--------|-------|
| **4xl** | 36px | 28px | 0.78x |
| **3xl** | 30px | 24px | 0.8x |
| **2xl** | 24px | 20px | 0.83x |
| **xl** | 20px | 18px | 0.9x |
| **lg** | 18px | 16px | 0.89x |
| **base** | 16px | 16px | 1x |
| **sm** | 14px | 14px | 1x |
| **xs** | 12px | 12px | 1x |

**Implementation**:
```css
/* Desktop (default) */
h1 { font-size: 1.875rem; }

/* Mobile */
@media (max-width: 768px) {
  h1 { font-size: 1.5rem; }
}
```

---

## Accessibility

### Font Scaling

Support browser zoom up to **200%** without horizontal scrolling:
```css
html {
  font-size: 16px; /* Base size */
}

/* Ensure layouts accommodate scaling */
body {
  max-width: 100%;
  overflow-x: hidden;
}
```

### Readability

- **Minimum font size**: 14px (0.875rem) for body text
- **Line length**: 50-75 characters per line (optimal readability)
- **Contrast**: WCAG AA (4.5:1 for normal text, 3:1 for large text)

### Dyslexia-Friendly

JetBrains Mono features:
- Clear distinction between similar characters (0/O, 1/l/I)
- Generous spacing between letters
- Monospace rhythm aids tracking for dyslexic readers

---

## Visual Samples

### Heading Hierarchy

```
█████████████████████████████████████
H1: ClaudeManual Design System
  30px / Bold / -0.025em
█████████████████████████████████████

█████████████████████████████████
H2: Navigation Patterns
  24px / Bold / -0.025em
█████████████████████████████████

█████████████████████████████
H3: Keyboard Shortcuts
  20px / Semibold / 0em
█████████████████████████████

███████████████████████
H4: Usage Guidelines
  16px / Semibold / 0em
███████████████████████

Body text (16px / Normal / 1.5 line-height)
This is a paragraph demonstrating body text style.
Monospace fonts provide excellent readability for
technical documentation and developer tools.
```

### Component Text

```
┌─────────────────────────────────────┐
│ [COPY PATH]  (14px / Semibold / Wide) │
└─────────────────────────────────────┘

┌──────┐ ┌──────────┐ ┌──────────────┐
│ DISCOVERY │ │ PROTOTYPE │ │ IMPLEMENTATION │
└──────┘ └──────────┘ └──────────────┘
   (12px / Semibold / Wide)

Navigation Label (14px / Medium)
├ Discovery_JTBD
├ Prototype_DesignSystem
└ Implementation_Developer
```

---

## Usage Guidelines

### Do's ✓
- Use monospace fonts for terminal aesthetic
- Maintain 1.25x type scale ratio
- Use rem units for scalability
- Test with browser zoom at 200%
- Provide relaxed line height (1.75) for long-form content

### Don'ts ✗
- Do not use monospace for long paragraphs (>150 words) - switch to sans-serif
- Do not reduce font sizes below 14px for body text
- Do not use tight line height (1.25) for body text
- Do not mix font families arbitrarily
- Do not use pure black (#000) - use token values

---

## Implementation Example (CSS)

```css
/* Typography Tokens */
:root {
  /* Font Families */
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --font-sans: 'Inter', system-ui, sans-serif;

  /* Font Sizes */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;

  /* Font Weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;

  /* Letter Spacing */
  --tracking-tight: -0.025em;
  --tracking-normal: 0em;
  --tracking-wide: 0.05em;
}

/* Base Styles */
body {
  font-family: var(--font-mono);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  letter-spacing: var(--tracking-normal);
  color: var(--color-text-primary);
}

/* Heading Styles */
h1 {
  font-size: var(--text-3xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
}

h2 {
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
}

h3 {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
}

/* Component Styles */
.btn {
  font-size: var(--text-sm);
  font-weight: var(--font-semibold);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
}

.badge {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
}

code {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  background: var(--color-bg-tertiary);
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
}
```

---

## Traceability

- **Source**: ClientAnalysis_ClaudeManual/04-design-specs/interaction-patterns.md
- **JTBD**: JTBD-1.1 (Self-service learning), JTBD-1.2 (Component context)
- **Client Facts**: CF-014 (Clean, modern, minimalistic terminal look)
- **Requirements**: REQ-018 (Typography system), REQ-020 (Accessibility)
- **Checkpoint**: CP-6 (Design Tokens)

---

*Typography system v1.0.0 with monospace primary font, 1.25x type scale, responsive sizing, and WCAG AA compliance.*
