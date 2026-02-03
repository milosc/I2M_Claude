# ComponentCard

**ID**: COMP-AGG-004
**Category**: Content Display
**Priority**: P1

## Overview

Framework component card displaying metadata, favorite toggle, and stage badge. Used in favorites page and comparison views. Combines Adobe Spectrum's Card with ClaudeManual-specific component metadata.

## Props Interface

```typescript
interface ComponentCardProps {
  /** Component data */
  component: ComponentMeta;
  /** Click handler */
  onClick: (componentId: string) => void;
  /** Favorite toggle handler */
  onToggleFavorite: (componentId: string) => void;
  /** Remove from view handler (Favorites page) */
  onRemove?: (componentId: string) => void;
  /** Layout variant */
  variant?: 'grid' | 'list';
  /** Show remove button */
  showRemove?: boolean;
}

interface ComponentMeta {
  id: string;
  name: string;
  type: 'skill' | 'command' | 'agent' | 'rule' | 'hook';
  stage: Stage;
  path: string;
  summary: string;
  isFavorite: boolean;
  lastUpdated?: string;
}
```

## Variants

| Variant | Use Case | Layout |
|---------|----------|--------|
| Grid | Favorites grid view | 3 columns desktop, 2 tablet, 1 mobile |
| List | Comparison view | Full width with horizontal layout |

## Library Components Used

### Primary Component
- **Card** (Spectrum): Container for component metadata
  - Props: `variant="outlined"`, `onPress`

### Supporting Components
- **Badge** (Spectrum): Type and stage indicators
  - Props: Stage-specific colors
- **Button** (Spectrum): View, Copy Path, Remove actions
  - Props: `variant="secondary"`, `size="S"`
- **Switch** (Spectrum): Favorite toggle (alternative to button)
  - Props: `isSelected`, `onChange`
- **StatusLight** (Spectrum): Last updated indicator
  - Props: `variant="positive"` (recent), `variant="neutral"` (old)

## States

| State | Condition | Visual Behavior | Token Mapping |
|-------|-----------|----------------|---------------|
| Default | Standard render | White background | `color.background.light.primary` |
| Hover | Mouse over card | Blue tint, shadow | `color.background.light.hover` |
| Favorite | isFavorite=true | Gold star, amber accent | `color.primitive.amber.500` |
| Pressed | Click/tap | Scale down (0.98) | `motion.duration.fast` |

## Design Token Mapping

| Property | Token Path | Value (Light) |
|----------|------------|---------------|
| Background | `color.background.light.primary` | `#ffffff` |
| Background (Hover) | `color.background.light.hover` | `color.primitive.blue.50` |
| Border | `color.border.light.default` | `color.primitive.gray.200` |
| Shadow | `shadow.sm` | 0 1px 2px rgba(0,0,0,0.05) |
| Shadow (Hover) | `shadow.md` | 0 4px 6px rgba(0,0,0,0.1) |
| Border Radius | `borderRadius.lg` | 0.5rem (8px) |
| Padding | `spacing.4` | 1rem (16px) |

## Usage Examples

### Grid Variant (Favorites)
```tsx
import { ComponentCard } from '@/components/ComponentCard';

<ComponentCard
  component={favoriteItem}
  variant="grid"
  showRemove={true}
  onClick={(id) => navigateTo(id)}
  onToggleFavorite={handleToggleFavorite}
  onRemove={(id) => removeFromFavorites(id)}
/>
```

### List Variant (Comparison)
```tsx
<ComponentCard
  component={componentA}
  variant="list"
  onClick={handleClick}
  onToggleFavorite={handleToggleFavorite}
/>
```

## Screen Usage

| Screen | Context | Configuration |
|--------|---------|---------------|
| SCR-004 Favorites Page | Favorites grid | Grid variant, show remove |
| SCR-005 Comparison View | Side-by-side comparison | List variant |

## Accessibility

- **Role**: `article`
- **ARIA**: `aria-label="Component card: [name]"`
- **Keyboard**: Tab, Enter, Space
- **Focus**: Visible 2px blue ring
- **Screen Reader**: Announces metadata
- **Contrast**: 4.5:1 minimum

## Testing Checklist

- [ ] Renders component name, type, stage
- [ ] Shows favorite star if isFavorite=true
- [ ] Hover effect applies
- [ ] Click navigates to component detail
- [ ] Favorite toggle updates state
- [ ] Remove button removes from favorites (if showRemove=true)
- [ ] Grid variant shows 3 columns on desktop
- [ ] List variant shows horizontal layout
- [ ] Keyboard navigation works
- [ ] Screen reader announces metadata

---

**Traceability**: PP-1.5 (Personalization), JTBD-1.6 (Bookmark tools), CF-012 (Favorites)
