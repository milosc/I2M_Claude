# Responsive Behavior - ClaudeManual

## Overview

This document defines responsive design specifications for the ClaudeManual prototype, ensuring optimal experience across all device sizes.

**Traceability**:
- Requirements: REQ-039 (Responsive design)
- Client Facts: CF-016 (Theme support implies device adaptability)
- JTBD: JTBD-2.2 (Explore autonomously - any device)

---

## Breakpoints

| Name | Width | Target Devices |
|------|-------|----------------|
| `mobile` | < 768px | Phones (portrait/landscape) |
| `tablet` | 768px - 1024px | Tablets, small laptops |
| `desktop` | > 1024px | Laptops, desktops |
| `wide` | > 1440px | Large monitors |

### CSS Variables

```css
:root {
  --breakpoint-mobile: 768px;
  --breakpoint-tablet: 1024px;
  --breakpoint-desktop: 1440px;
}
```

### Tailwind Config

```js
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1440px',
      '2xl': '1920px',
    },
  },
};
```

---

## Layout Patterns

### Main Explorer View (SCR-001)

| Breakpoint | Layout | Navigation | Detail Pane |
|------------|--------|------------|-------------|
| Desktop | Two-column | Fixed sidebar (300px) | Flexible main area |
| Tablet | Two-column | Collapsible sidebar (240px) | Flexible main area |
| Mobile | Single-column | Drawer (full-width) | Full-width |

**Desktop (>1024px)**:
```
┌─────────────────────────────────────────────────────────┐
│ Header                                        Search    │
├──────────────┬──────────────────────────────────────────┤
│              │                                          │
│  Navigation  │           Detail Pane                    │
│  Tree        │                                          │
│  (300px)     │                                          │
│              │                                          │
└──────────────┴──────────────────────────────────────────┘
```

**Mobile (<768px)**:
```
┌─────────────────────────────┐
│ Header           ☰ Menu     │
├─────────────────────────────┤
│                             │
│      Detail Pane            │
│      (Full Width)           │
│                             │
├─────────────────────────────┤
│ [Back to Navigation]        │
└─────────────────────────────┘

Drawer (when menu open):
┌─────────────────────────────┐
│ ← Close                     │
├─────────────────────────────┤
│                             │
│    Navigation Tree          │
│    (Full Width)             │
│                             │
└─────────────────────────────┘
```

### Search Results (SCR-002)

| Breakpoint | Grid Columns | Card Size |
|------------|--------------|-----------|
| Desktop | 3 columns | 400px min |
| Tablet | 2 columns | 350px min |
| Mobile | 1 column | Full width |

```css
.search-results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: var(--spacing-6);
}

@media (max-width: 768px) {
  .search-results-grid {
    grid-template-columns: 1fr;
  }
}
```

### Favorites Page (SCR-004)

| Breakpoint | Grid Columns | Drag-Drop |
|------------|--------------|-----------|
| Desktop | 4 columns | Full drag-drop |
| Tablet | 3 columns | Full drag-drop |
| Mobile | 2 columns | Touch drag-drop |

---

## Touch Targets

### Minimum Sizes (WCAG 2.1 AAA)

| Element | Minimum Size | Spacing |
|---------|--------------|---------|
| Buttons | 44px × 44px | 8px between |
| Links (inline) | 24px height | - |
| Tree nodes | 44px height | 4px between |
| Cards (tappable) | 44px minimum hit area | 16px between |
| Form inputs | 44px height | - |

```css
/* Touch-friendly button */
.button {
  min-height: 44px;
  min-width: 44px;
  padding: var(--spacing-3) var(--spacing-4);
}

/* Touch-friendly tree item */
.tree-item {
  min-height: 44px;
  padding: var(--spacing-2) var(--spacing-3);
}
```

---

## Typography Scaling

### Font Sizes by Breakpoint

| Token | Desktop | Tablet | Mobile |
|-------|---------|--------|--------|
| `text-4xl` | 36px | 32px | 28px |
| `text-3xl` | 30px | 26px | 24px |
| `text-2xl` | 24px | 22px | 20px |
| `text-xl` | 20px | 18px | 18px |
| `text-lg` | 18px | 16px | 16px |
| `text-base` | 16px | 16px | 16px |
| `text-sm` | 14px | 14px | 14px |
| `text-xs` | 12px | 12px | 12px |

```css
/* Fluid typography */
:root {
  --text-4xl: clamp(1.75rem, 2vw + 1rem, 2.25rem);
  --text-3xl: clamp(1.5rem, 1.5vw + 1rem, 1.875rem);
  --text-2xl: clamp(1.25rem, 1vw + 1rem, 1.5rem);
}
```

---

## Component Adaptations

### Navigation Tree

| Behavior | Desktop | Mobile |
|----------|---------|--------|
| Visibility | Always visible | Drawer (hidden by default) |
| Width | 300px fixed | 100% of drawer |
| Toggle | N/A | Hamburger menu |
| Close | N/A | Swipe right or × button |

### Detail Pane

| Behavior | Desktop | Mobile |
|----------|---------|--------|
| Tabs | Horizontal | Horizontal (scrollable) |
| Code blocks | Horizontal scroll | Horizontal scroll |
| Diagrams | Zoom/pan | Pinch-to-zoom |

### Search Bar

| Behavior | Desktop | Mobile |
|----------|---------|--------|
| Width | 400px max | 100% |
| Position | Header (inline) | Header (icon → expand) |
| Filters | Inline dropdowns | Bottom sheet |

### Modals

| Behavior | Desktop | Mobile |
|----------|---------|--------|
| Width | 600px max | 100% - 32px padding |
| Height | Auto (max 80vh) | 100% (full sheet) |
| Close | × button, Esc, click outside | × button, swipe down |

---

## Gesture Support (Mobile)

| Gesture | Action |
|---------|--------|
| Swipe right | Close navigation drawer |
| Swipe down | Close modal (bottom sheet style) |
| Pinch | Zoom diagrams |
| Double-tap | Fit diagram to view |
| Long press | Context menu (copy path, add to favorites) |

```tsx
// Swipe gesture handling
import { useSwipeable } from 'react-swipeable';

const handlers = useSwipeable({
  onSwipedRight: () => closeDrawer(),
  onSwipedDown: () => closeModal(),
  trackMouse: false,
});

<div {...handlers}>
  {/* Content */}
</div>
```

---

## Viewport Meta

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

### Safe Areas (Notch/Home Indicator)

```css
.header {
  padding-top: env(safe-area-inset-top);
}

.bottom-bar {
  padding-bottom: env(safe-area-inset-bottom);
}

.sidebar {
  padding-left: env(safe-area-inset-left);
}
```

---

## Media Queries Reference

```css
/* Mobile first approach */

/* Styles for all devices */
.component { /* Base mobile styles */ }

/* Tablet and up */
@media (min-width: 768px) {
  .component { /* Tablet styles */ }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .component { /* Desktop styles */ }
}

/* Wide screens */
@media (min-width: 1440px) {
  .component { /* Wide screen styles */ }
}

/* Orientation */
@media (orientation: landscape) and (max-width: 768px) {
  /* Mobile landscape specific */
}

/* High DPI displays */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  /* Retina-specific styles */
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  /* Disable animations */
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  /* Dark mode colors */
}
```

---

## Testing Checklist

### Device Testing

- [ ] iPhone SE (375px)
- [ ] iPhone 14 Pro (393px)
- [ ] iPad Mini (768px)
- [ ] iPad Pro (1024px)
- [ ] MacBook Air (1440px)
- [ ] 27" Monitor (2560px)

### Orientation Testing

- [ ] Portrait mode (phones, tablets)
- [ ] Landscape mode (phones, tablets)

### Interaction Testing

- [ ] Touch gestures (swipe, pinch, long press)
- [ ] Mouse interactions
- [ ] Keyboard navigation
- [ ] Hybrid (touch laptop)

---

## Related

- `motion.md` - Animation adjustments for mobile
- `accessibility.md` - Touch target requirements
- `design-tokens/tokens.json` - Breakpoint values
