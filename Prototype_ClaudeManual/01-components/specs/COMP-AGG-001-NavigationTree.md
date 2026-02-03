# NavigationTree

**ID**: COMP-AGG-001
**Category**: Navigation
**Priority**: P0

## Overview

Hierarchical tree component for framework exploration with stage filtering, count badges, and favorites integration. Combines Adobe Spectrum's Tree component with ClaudeManual-specific business logic for navigating skills, commands, agents, rules, and hooks.

## Props Interface

```typescript
interface NavigationTreeProps {
  /** Tree data structure */
  items: TreeNode[];
  /** Currently selected item ID */
  selectedId?: string;
  /** Active stage filter (Discovery, Prototype, etc.) */
  stageFilter?: Stage[];
  /** Search query for filtering items */
  searchQuery?: string;
  /** Show/hide count badges */
  showCountBadges?: boolean;
  /** Favorites list IDs */
  favorites?: string[];
  /** Selection handler */
  onSelect: (itemId: string) => void;
  /** Favorite toggle handler */
  onToggleFavorite?: (itemId: string) => void;
  /** Collapse/expand handler */
  onExpandChange?: (itemId: string, expanded: boolean) => void;
  /** Loading state */
  loading?: boolean;
  /** Error state */
  error?: string;
}

interface TreeNode {
  id: string;
  label: string;
  type: 'category' | 'skill' | 'command' | 'agent' | 'rule' | 'hook';
  stage?: Stage;
  path?: string;
  description?: string;
  children?: TreeNode[];
  count?: number;
  isFavorite?: boolean;
}

type Stage = 'discovery' | 'prototype' | 'productspecs' | 'solarch' | 'implementation' | 'utility' | 'security' | 'grc';
```

## Variants

| Variant | Use Case | Visual Differences |
|---------|----------|-------------------|
| Default | Standard navigation tree | Full width, collapsible categories |
| Filtered | Stage filter active | Muted non-matching items, count badges updated |
| Search | Search query active | Expanded matching branches, highlighted text |
| Empty | No items match filter | Empty state message with clear filter CTA |

## Library Components Used

### Primary Component
- **Tree** (Spectrum): Hierarchical data visualization with expand/collapse
  - Props: `items`, `selectedKeys`, `expandedKeys`, `onSelectionChange`, `onExpandedChange`
  - Provides keyboard navigation (Arrow keys, Enter, Space)

### Supporting Components
- **Badge** (Spectrum): Count indicators (e.g., "Skills (85)")
  - Props: `variant="info"`, `size="S"`
- **Tooltip** (Spectrum): Category descriptions on [i] icon hover
  - Props: `placement="right"`, `delay={300}`
- **TextField** (Spectrum): Search input (Cmd+K focus)
  - Props: `type="search"`, `placeholder`, `value`, `onChange`

## States

| State | Condition | Visual Behavior | Token Mapping |
|-------|-----------|----------------|---------------|
| Default | First load | Categories collapsed except first | `color.background.light.primary` |
| Hover | Mouse over item | Background highlight | `color.background.light.hover` (blue.50) |
| Selected | Item clicked | Blue background, bold text | `color.background.light.selected` (blue.100) |
| Favorite | Item in favorites | Gold star icon (⭐) | `color.primitive.amber.500` |
| Filtered | Stage filter active | Non-matching items muted | `opacity: 0.4` |
| Expanded | Category expanded | Arrow icon rotated 90° | `motion.duration.fast` (100ms) |
| Collapsed | Category collapsed | Arrow icon pointing right | - |
| Loading | Fetching tree data | Skeleton loader | `color.primitive.gray.200` |
| Error | Fetch failure | Error message with retry button | `color.semantic.light.error` |

## Design Token Mapping

| Property | Token Path | Value (Light) |
|----------|------------|---------------|
| Background | `color.background.light.primary` | `#ffffff` |
| Background (Hover) | `color.background.light.hover` | `color.primitive.blue.50` |
| Background (Selected) | `color.background.light.selected` | `color.primitive.blue.100` |
| Text | `color.text.light.primary` | `color.primitive.gray.900` |
| Text (Muted) | `color.text.light.secondary` | `color.primitive.gray.600` |
| Border | `color.border.light.default` | `color.primitive.gray.200` |
| Badge (Discovery) | `color.stage.discovery.light` | `color.primitive.blue.500` |
| Badge (Prototype) | `color.stage.prototype.light` | `color.primitive.green.500` |
| Font Family | `typography.fontFamily.mono` | JetBrains Mono |
| Font Size | `typography.fontSize.sm` | 0.875rem (14px) |
| Padding | `spacing.3` | 0.75rem (12px) |
| Border Radius | `borderRadius.md` | 0.375rem (6px) |
| Transition | `motion.duration.fast` | 100ms |

## Business Logic

### Stage Filtering
```typescript
function filterByStage(nodes: TreeNode[], stages: Stage[]): TreeNode[] {
  if (!stages.length) return nodes;

  return nodes.map(node => {
    const matchesStage = !node.stage || stages.includes(node.stage);
    const filteredChildren = node.children
      ? filterByStage(node.children, stages)
      : [];

    return {
      ...node,
      children: filteredChildren,
      // Update count badge to reflect filtered children
      count: filteredChildren.length,
      // Mute if doesn't match filter
      isFiltered: !matchesStage && filteredChildren.length === 0
    };
  });
}
```

### Search Filtering
```typescript
function searchTree(nodes: TreeNode[], query: string): TreeNode[] {
  if (!query) return nodes;

  const lowerQuery = query.toLowerCase();

  return nodes.reduce((acc, node) => {
    const matchesLabel = node.label.toLowerCase().includes(lowerQuery);
    const matchesDescription = node.description?.toLowerCase().includes(lowerQuery);
    const matchesPath = node.path?.toLowerCase().includes(lowerQuery);

    const filteredChildren = node.children
      ? searchTree(node.children, query)
      : [];

    if (matchesLabel || matchesDescription || matchesPath || filteredChildren.length > 0) {
      acc.push({
        ...node,
        children: filteredChildren,
        // Auto-expand matching branches
        expanded: true,
        // Highlight matching text (handled by renderer)
        highlight: matchesLabel || matchesDescription
      });
    }

    return acc;
  }, [] as TreeNode[]);
}
```

### Favorites Integration
```typescript
function toggleFavorite(itemId: string, favorites: string[]): string[] {
  const isFavorite = favorites.includes(itemId);

  if (isFavorite) {
    // Remove from favorites
    return favorites.filter(id => id !== itemId);
  } else {
    // Add to favorites
    return [...favorites, itemId];
  }
}

function syncFavoritesToLocalStorage(favorites: string[]): void {
  localStorage.setItem('claudemanual:favorites', JSON.stringify(favorites));
}
```

## Usage Examples

### Basic Tree
```tsx
import { NavigationTree } from '@/components/NavigationTree';

<NavigationTree
  items={treeData}
  selectedId="Discovery_JTBD"
  onSelect={(itemId) => console.log('Selected:', itemId)}
/>
```

### With Stage Filter
```tsx
<NavigationTree
  items={treeData}
  stageFilter={['discovery', 'prototype']}
  showCountBadges={true}
  onSelect={handleSelect}
/>
```

### With Search
```tsx
<NavigationTree
  items={treeData}
  searchQuery="persona"
  favorites={userFavorites}
  onToggleFavorite={(itemId) => {
    const newFavorites = toggleFavorite(itemId, userFavorites);
    setUserFavorites(newFavorites);
    syncFavoritesToLocalStorage(newFavorites);
  }}
  onSelect={handleSelect}
/>
```

### With Favorites
```tsx
<NavigationTree
  items={treeData}
  favorites={['Discovery_JTBD', '/htec-sdd-implement']}
  onToggleFavorite={handleToggleFavorite}
  onSelect={handleSelect}
/>
```

## Screen Usage

| Screen | Context | Configuration |
|--------|---------|---------------|
| SCR-001 Main Explorer | Master pane navigation | Default variant, all categories |
| SCR-003 Stage-Filtered View | Filtered by stage | stageFilter prop active |
| SCR-010 Architecture Browser | Architecture-only tree | Filtered to architecture items |

## Accessibility

- **Role**: `tree` (provided by Spectrum Tree)
- **ARIA**: `aria-expanded`, `aria-selected`, `aria-label="Framework navigation"`
- **Keyboard**:
  - Arrow keys: Navigate tree
  - Enter/Space: Select item
  - Right Arrow: Expand category
  - Left Arrow: Collapse category
  - Home/End: First/last item
  - Type-ahead: Jump to item by typing
- **Focus**: Visible 2px blue ring (`shadow.focus`)
- **Screen Reader**: Category counts announced, favorite status announced
- **Contrast**: 4.5:1 minimum for text

## Performance Considerations

- **Virtualization**: Use Spectrum's virtualized tree for 100+ items
- **Lazy Loading**: Load children on expand for large categories
- **Debounced Search**: 300ms debounce on search input
- **Memoization**: Memoize filtered/searched results
- **Local Storage**: Persist favorites, expanded state

## Testing Checklist

- [ ] Renders tree with nested categories
- [ ] Expands/collapses categories on click
- [ ] Highlights selected item
- [ ] Shows count badges (e.g., "Skills (85)")
- [ ] Filters items by stage
- [ ] Filters items by search query
- [ ] Auto-expands matching search branches
- [ ] Toggles favorite status with ⭐ icon
- [ ] Persists favorites to localStorage
- [ ] Updates count badges when filter active
- [ ] Shows empty state when no matches
- [ ] Keyboard navigation works (Arrow, Enter, Space)
- [ ] Focus indicator visible
- [ ] Screen reader announces counts and favorites
- [ ] Respects `prefers-reduced-motion` for transitions

---

**Traceability**:
- **Addresses Pain Points**: PP-1.4 (Organizational Chaos), PP-1.1 (Knowledge Transfer)
- **Enables JTBD**: JTBD-1.7 (Navigate hierarchies visually), JTBD-1.4 (Stage-appropriate tools)
- **Client Facts**: CF-006 (Dual-pane layout), CF-014 (Terminal-inspired UI)
- **Design Tokens**: Uses stage colors, spacing scale, mono font
- **Library**: Adobe Spectrum React Tree, Badge, Tooltip, TextField
