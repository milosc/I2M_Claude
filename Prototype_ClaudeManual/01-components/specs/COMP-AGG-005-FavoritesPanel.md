# FavoritesPanel

**ID**: COMP-AGG-005
**Category**: Collections
**Priority**: P1

## Overview

User-curated favorites list with drag-drop reordering and quick actions. Combines Adobe Spectrum's GridList with ClaudeManual-specific favorites management.

## Props Interface

```typescript
interface FavoritesPanelProps {
  /** Favorites list */
  favorites: ComponentMeta[];
  /** Reorder handler */
  onReorder: (newOrder: string[]) => void;
  /** Remove handler */
  onRemove: (componentId: string) => void;
  /** Clear all handler */
  onClearAll: () => void;
  /** Item click handler */
  onClick: (componentId: string) => void;
}
```

## Library Components Used

- **GridList** (Spectrum): Drag-drop list
- **Card** (Spectrum): Favorite items
- **Button** (Spectrum): Remove, Clear All actions
- **IllustratedMessage** (Spectrum): Empty state

## Usage Examples

```tsx
<FavoritesPanel
  favorites={userFavorites}
  onReorder={(newOrder) => setFavoritesOrder(newOrder)}
  onRemove={(id) => removeFromFavorites(id)}
  onClearAll={() => clearAllFavorites()}
  onClick={(id) => navigateTo(id)}
/>
```

## Screen Usage

| Screen | Context |
|--------|---------|
| SCR-004 Favorites Page | Main favorites list with drag-drop |

---

**Traceability**: PP-1.5 (Personalization), JTBD-1.6 (Bookmark tools), CF-012 (Favorites)
