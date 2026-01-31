# Design Constraints Reference

Non-negotiable design rules enforced across all generated specifications.

---

## Hard Constraints

### Color System

| Constraint | Limit | Rationale |
|------------|-------|-----------|
| Total colors | **≤ 5** | Visual coherence, brand focus |
| Primary colors | **1** | Clear brand identity |
| Neutral scale | **2-3** | Sufficient for hierarchy |
| Accent/Semantic | **1-2** | Status indication |

**Rules**:
- ❌ NEVER use more than 5 colors total
- ❌ NEVER use gradients unless explicitly requested
- ❌ NEVER use purple/violet prominently without explicit request
- ❌ NEVER use color as the only indicator (accessibility)
- ✅ Primary color for main CTAs only
- ✅ Neutrals for 90% of interface
- ✅ Semantic colors only for intended purpose

### Typography

| Constraint | Limit | Rationale |
|------------|-------|-----------|
| Font families | **≤ 2** | Performance, consistency |
| Minimum font size | **14px** | Readability, accessibility |
| Body line height | **1.4-1.6** | Reading comfort |
| Max line width | **65-75ch** | Reading comfort |

**Rules**:
- ❌ NEVER use more than 2 font families
- ❌ NEVER go below 14px for interactive elements
- ❌ NEVER go below 12px for any text
- ❌ NEVER use decorative fonts for body text
- ❌ NEVER justify text (use left-align)
- ✅ Use relative units (rem) not fixed pixels
- ✅ Limit to 3-4 weights per font

### Spacing

| Constraint | Limit | Rationale |
|------------|-------|-----------|
| Base unit | **4px** | Consistent scale |
| Spacing scale | **Tailwind default** | Framework compatibility |

**Rules**:
- ❌ NEVER use arbitrary values (e.g., `p-[17px]`)
- ❌ NEVER mix margin and gap on same element
- ❌ NEVER use space-x/space-y (use gap instead)
- ✅ Use spacing tokens consistently
- ✅ Use gap for child spacing
- ✅ Use padding for internal spacing

### Touch & Click Targets

| Constraint | Limit | Rationale |
|------------|-------|-----------|
| Minimum touch target | **44×44px** | WCAG 2.5.5, mobile usability |
| Minimum click target | **24×24px** | Desktop usability |
| Target spacing | **≥8px** | Prevent mis-taps |

### Contrast (WCAG AA)

| Text Type | Minimum Ratio |
|-----------|---------------|
| Normal text (<18px) | **4.5:1** |
| Large text (≥18px or ≥14px bold) | **3:1** |
| UI components | **3:1** |
| Non-text graphics | **3:1** |

---

## Required Design Tokens

### Color Tokens

```
--color-background
--color-foreground
--color-card
--color-card-foreground
--color-primary
--color-primary-foreground
--color-secondary
--color-secondary-foreground
--color-muted
--color-muted-foreground
--color-border
--color-input
--color-ring
--color-destructive
--color-destructive-foreground
```

### Typography Tokens

```
--font-sans
--font-mono (optional)
```

### Spacing Tokens

```
--radius-sm (4px)
--radius (6px)
--radius-md (8px)
--radius-lg (12px)
--radius-xl (16px)
```

---

## Component Requirements

### Every Component Must Have

1. **Variants**: At least default + 1 alternative
2. **Sizes**: At least sm, default, lg
3. **States**: default, hover, focus, active, disabled
4. **Accessibility**: Keyboard support, ARIA attributes
5. **Responsive**: Mobile-first approach

### Every Form Input Must Have

1. **Label**: Associated via htmlFor/id
2. **Error state**: Visual + text + aria-invalid
3. **Helper text**: Optional but supported
4. **Required indicator**: Visual + aria-required
5. **Focus ring**: Visible, meets contrast

### Every Interactive Element Must Have

1. **data-testid**: For test automation
2. **Keyboard access**: Tab, Enter/Space
3. **Focus indicator**: Visible, 3:1 contrast
4. **Feedback**: Visual response to interaction

---

## Responsive Requirements

### Breakpoints (Tailwind Default)

| Name | Width | Target |
|------|-------|--------|
| (base) | 0 | Mobile phones |
| sm | 640px | Large phones |
| md | 768px | Tablets |
| lg | 1024px | Laptops |
| xl | 1280px | Desktops |
| 2xl | 1536px | Large monitors |

### Required Behaviors

- **Mobile (base)**: Single column, stacked layout
- **Tablet (md)**: 2 columns where appropriate
- **Desktop (lg)**: Full layout with sidebars
- **Must work at**: 320px width (WCAG reflow)
- **Must work at**: 200% zoom (WCAG resize)

---

## Validation Checklist

### Color
- [ ] Total colors ≤ 5
- [ ] All text meets 4.5:1 contrast
- [ ] All UI components meet 3:1 contrast
- [ ] Color is not the only indicator

### Typography
- [ ] Font families ≤ 2
- [ ] No text below 14px for interactive
- [ ] No text below 12px anywhere
- [ ] Line height 1.4-1.6 for body

### Spacing
- [ ] All spacing uses token scale
- [ ] No arbitrary values
- [ ] Touch targets ≥ 44px

### Accessibility
- [ ] All inputs have labels
- [ ] All interactive elements keyboard accessible
- [ ] Focus indicators visible
- [ ] ARIA attributes specified

---

**Reference Version**: 2.0
