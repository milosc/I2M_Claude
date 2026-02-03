# Motion System - ClaudeManual

## Overview

This document defines the animation and transition specifications for the ClaudeManual prototype, ensuring consistent, purposeful motion that enhances usability without causing distraction.

**Traceability**: CF-014 (Minimalistic design), JTBD-2.1 (Confidence through smooth interactions)

---

## Design Principles

1. **Purposeful Motion**: Every animation serves a functional purpose (feedback, orientation, hierarchy)
2. **Performance First**: Animations use GPU-accelerated properties (transform, opacity)
3. **Reduced Motion Support**: All animations respect `prefers-reduced-motion` media query
4. **Consistency**: Same interaction patterns use same timing across the application

---

## Timing Tokens

| Token | Duration | Use Case |
|-------|----------|----------|
| `duration-instant` | 100ms | Hover states, button press feedback |
| `duration-fast` | 150ms | Tree expand/collapse, tooltip appear |
| `duration-normal` | 200ms | Page transitions, modal open |
| `duration-slow` | 300ms | Search results load, complex transitions |
| `duration-deliberate` | 500ms | First-time animations, onboarding |

### CSS Variables

```css
:root {
  --duration-instant: 100ms;
  --duration-fast: 150ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --duration-deliberate: 500ms;
}
```

---

## Easing Functions

| Token | Curve | Use Case |
|-------|-------|----------|
| `ease-out` | cubic-bezier(0.0, 0.0, 0.2, 1) | Elements entering (modals, dropdowns) |
| `ease-in` | cubic-bezier(0.4, 0.0, 1, 1) | Elements exiting |
| `ease-in-out` | cubic-bezier(0.4, 0.0, 0.2, 1) | State changes, toggle switches |
| `ease-spring` | cubic-bezier(0.175, 0.885, 0.32, 1.275) | Playful feedback (favorites toggle) |

### CSS Variables

```css
:root {
  --ease-out: cubic-bezier(0.0, 0.0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0.0, 1, 1);
  --ease-in-out: cubic-bezier(0.4, 0.0, 0.2, 1);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

---

## Component Animations

### Navigation Tree

| Interaction | Property | Duration | Easing |
|-------------|----------|----------|--------|
| Node expand | height, opacity | 150ms | ease-out |
| Node collapse | height, opacity | 150ms | ease-in |
| Hover highlight | background-color | 100ms | ease-in-out |
| Selection change | background-color | 100ms | ease-in-out |

```css
.tree-node-content {
  transition: height var(--duration-fast) var(--ease-out),
              opacity var(--duration-fast) var(--ease-out);
}

.tree-node:hover {
  transition: background-color var(--duration-instant) var(--ease-in-out);
}
```

### Search Results

| Interaction | Property | Duration | Easing |
|-------------|----------|----------|--------|
| Results appear | opacity, transform | 300ms | ease-out |
| Result hover | transform (scale), box-shadow | 100ms | ease-out |
| Filter change | opacity | 200ms | ease-in-out |

```css
.search-result-card {
  transition: transform var(--duration-instant) var(--ease-out),
              box-shadow var(--duration-instant) var(--ease-out);
}

.search-result-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
```

### Modal / Detail Pane

| Interaction | Property | Duration | Easing |
|-------------|----------|----------|--------|
| Modal open | opacity, transform (scale) | 200ms | ease-out |
| Modal close | opacity, transform (scale) | 150ms | ease-in |
| Tab switch | opacity | 150ms | ease-in-out |
| Backdrop appear | opacity | 200ms | ease-out |

```css
.modal-overlay {
  transition: opacity var(--duration-normal) var(--ease-out);
}

.modal-content {
  transition: opacity var(--duration-normal) var(--ease-out),
              transform var(--duration-normal) var(--ease-out);
}

.modal-content[data-state="open"] {
  animation: modal-enter var(--duration-normal) var(--ease-out);
}

@keyframes modal-enter {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

### Favorites Panel

| Interaction | Property | Duration | Easing |
|-------------|----------|----------|--------|
| Drag start | transform (scale), box-shadow | 100ms | ease-out |
| Drag over | transform (translateY) | 150ms | ease-out |
| Drop | transform | 200ms | ease-spring |
| Remove | opacity, transform (translateX) | 200ms | ease-in |

```css
.favorite-card[data-dragging="true"] {
  transform: scale(1.02);
  box-shadow: var(--shadow-xl);
  transition: transform var(--duration-instant) var(--ease-out),
              box-shadow var(--duration-instant) var(--ease-out);
}

.favorite-card[data-removing="true"] {
  animation: slide-out-right var(--duration-normal) var(--ease-in);
}

@keyframes slide-out-right {
  to {
    opacity: 0;
    transform: translateX(100%);
  }
}
```

### Diagram Viewer

| Interaction | Property | Duration | Easing |
|-------------|----------|----------|--------|
| Zoom in/out | transform (scale) | 200ms | ease-out |
| Pan | transform (translate) | 0ms | - (immediate) |
| Fit to view | transform | 300ms | ease-in-out |

---

## Loading States

### Skeleton Loader

```css
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-gray-100) 25%,
    var(--color-gray-200) 50%,
    var(--color-gray-100) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}

@keyframes skeleton-pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Spinner

```css
.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

---

## Reduced Motion

All animations respect user preferences:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Implementation Notes

1. **GPU Acceleration**: Use `transform` and `opacity` for smooth 60fps animations
2. **will-change**: Apply sparingly to elements that will animate
3. **Framer Motion**: Use for complex orchestrated animations
4. **CSS Transitions**: Prefer for simple state changes

```tsx
// Example: Framer Motion for search results
import { motion, AnimatePresence } from 'framer-motion';

<AnimatePresence>
  {results.map((result, index) => (
    <motion.div
      key={result.id}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ delay: index * 0.05, duration: 0.3 }}
    >
      <SearchResultCard {...result} />
    </motion.div>
  ))}
</AnimatePresence>
```

---

## Related

- `design-tokens/tokens.json` - Animation token values
- `accessibility.md` - Reduced motion requirements
- `responsive.md` - Mobile animation adjustments
