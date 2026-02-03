# SearchResultCard

**ID**: COMP-AGG-003
**Category**: Search
**Priority**: P0

## Overview

Search result preview card displaying framework component matches with metadata, one-sentence summary, and quick actions. Combines Adobe Spectrum's Card component with ClaudeManual-specific search result formatting.

## Props Interface

```typescript
interface SearchResultCardProps {
  /** Search result data */
  result: SearchResult;
  /** Search query for highlighting */
  query: string;
  /** Click handler */
  onClick: (resultId: string) => void;
  /** Copy path handler */
  onCopyPath?: (path: string) => void;
  /** Favorite toggle handler */
  onToggleFavorite?: (resultId: string) => void;
  /** Highlighted variant */
  highlighted?: boolean;
}

interface SearchResult {
  id: string;
  name: string;
  type: 'skill' | 'command' | 'agent' | 'rule' | 'hook';
  stage: Stage;
  path: string;
  summary: string;
  relevanceScore: number;
  tags?: string[];  // PF-002: User-defined tags for filtering and display
  isFavorite: boolean;
}

type Stage = 'discovery' | 'prototype' | 'productspecs' | 'solarch' | 'implementation' | 'utility' | 'security' | 'grc';
```

## Variants

| Variant | Use Case | Visual Differences |
|---------|----------|-------------------|
| Default | Standard search result | White background, hover effect |
| Highlighted | Keyboard navigation | Blue border, subtle shadow |
| Favorite | Bookmarked result | Gold star icon prominent |

## Library Components Used

### Primary Component
- **Card** (Spectrum): Container for search result content
  - Props: `variant="outlined"`, `onPress`, `isQuiet`

### Supporting Components
- **Badge** (Spectrum): Type and stage indicators
  - Props: `variant="info"` (type), stage-specific colors
- **Link** (Spectrum): "View Details" link
  - Props: `variant="primary"`, `onPress`
- **Button** (Spectrum): Copy Path, Add to Favorites
  - Props: `variant="secondary"`, `size="S"`, `onPress`
- **Text** (Spectrum): Summary and path text
  - Props: `size="S"`, `color="secondary"`

## States

| State | Condition | Visual Behavior | Token Mapping |
|-------|-----------|----------------|---------------|
| Default | Standard render | White background, gray border | `color.background.light.primary` |
| Hover | Mouse over card | Blue tint, slight shadow | `color.background.light.hover` |
| Highlighted | Keyboard selection | Blue border (2px) | `color.border.light.focus` |
| Favorite | isFavorite=true | Gold star icon visible | `color.primitive.amber.500` |
| Pressed | Click/tap | Slight scale down (0.98) | `motion.duration.fast` |

## Design Token Mapping

| Property | Token Path | Value (Light) |
|----------|------------|---------------|
| Background | `color.background.light.primary` | `#ffffff` |
| Background (Hover) | `color.background.light.hover` | `color.primitive.blue.50` |
| Border | `color.border.light.default` | `color.primitive.gray.200` |
| Border (Highlighted) | `color.border.light.focus` | `color.primitive.blue.500` |
| Text (Title) | `color.text.light.primary` | `color.primitive.gray.900` |
| Text (Summary) | `color.text.light.secondary` | `color.primitive.gray.600` |
| Text (Path) | `color.text.light.tertiary` | `color.primitive.gray.500` |
| Badge (Discovery) | `color.stage.discovery.light` | `color.primitive.blue.500` |
| Shadow | `shadow.sm` | 0 1px 2px rgba(0,0,0,0.05) |
| Shadow (Hover) | `shadow.md` | 0 4px 6px rgba(0,0,0,0.1) |
| Border Radius | `borderRadius.lg` | 0.5rem (8px) |
| Padding | `spacing.4` | 1rem (16px) |
| Gap | `spacing.3` | 0.75rem (12px) |

## Business Logic

### Query Highlighting
```typescript
function highlightQuery(text: string, query: string): React.ReactNode {
  if (!query) return text;

  const regex = new RegExp(`(${query})`, 'gi');
  const parts = text.split(regex);

  return parts.map((part, index) => {
    if (part.toLowerCase() === query.toLowerCase()) {
      return (
        <mark key={index} style={{ backgroundColor: 'color.primitive.amber.200', fontWeight: 600 }}>
          {part}
        </mark>
      );
    }
    return part;
  });
}
```

### Relevance Score Display
```typescript
function getRelevanceBadgeVariant(score: number): BadgeVariant {
  if (score >= 0.8) return 'positive'; // High relevance
  if (score >= 0.5) return 'info'; // Medium relevance
  return 'neutral'; // Low relevance
}
```

## Usage Examples

### Basic Search Result
```tsx
import { SearchResultCard } from '@/components/SearchResultCard';

<SearchResultCard
  result={{
    id: 'Discovery_JTBD',
    name: 'Discovery_JTBD',
    type: 'skill',
    stage: 'discovery',
    path: '.claude/skills/Discovery_JTBD/SKILL.md',
    summary: 'Extracts Jobs To Be Done from pain points and client facts.',
    relevanceScore: 0.92,
    isFavorite: false
  }}
  query="jtbd"
  onClick={(id) => navigateTo(id)}
/>
```

### With Favorite Toggle
```tsx
<SearchResultCard
  result={searchResult}
  query={searchQuery}
  onClick={handleResultClick}
  onToggleFavorite={(id) => {
    const newFavorites = toggleFavorite(id, favorites);
    setFavorites(newFavorites);
  }}
  onCopyPath={(path) => copyToClipboard(path)}
/>
```

### Highlighted (Keyboard Navigation)
```tsx
<SearchResultCard
  result={searchResult}
  query={searchQuery}
  highlighted={selectedResultIndex === 2}
  onClick={handleResultClick}
/>
```

## Screen Usage

| Screen | Context | Configuration |
|--------|---------|---------------|
| SCR-002 Search Results Page | Search results list | Default variant, grid layout |

## Accessibility

- **Role**: `article` (semantic card)
- **ARIA**: `aria-label="Search result: [component name]"`, `aria-describedby="summary-[id]"`
- **Keyboard**:
  - Tab: Focus card
  - Enter/Space: Activate card (navigate to detail)
  - Arrow Down/Up: Navigate results list (handled by parent)
- **Focus**: Visible 2px blue ring
- **Screen Reader**: Announces title, type, stage, summary
- **Contrast**: 4.5:1 minimum for text

## Performance Considerations

- **Virtualization**: Use react-window for 100+ results
- **Lazy Rendering**: Render cards on-demand during scroll
- **Highlight Memoization**: Memoize highlighted text to avoid re-renders
- **Image Lazy Loading**: If cards include thumbnails in future

## Testing Checklist

- [ ] Renders title, type badge, stage badge
- [ ] Renders one-sentence summary
- [ ] Renders file path with muted text
- [ ] Highlights query text in title and summary
- [ ] Shows favorite star if isFavorite=true
- [ ] Hover effect applies (background tint, shadow)
- [ ] Click navigates to component detail
- [ ] Copy Path button copies to clipboard
- [ ] Add to Favorites toggles favorite status
- [ ] Keyboard focus visible (blue ring)
- [ ] Screen reader announces all metadata
- [ ] Respects `prefers-reduced-motion` for hover transitions

---

**Traceability**:
- **Addresses Pain Points**: PP-1.3 (Discoverability Challenge)
- **Enables JTBD**: JTBD-1.3 (Find relevant tools - tagging), JTBD-2.2 (Autonomous exploration)
- **Client Facts**: CF-009 (Search page requirement), CF-010 (Tagging system)
- **Feedback**: PF-002 (Tagging feature - tags field added to SearchResult interface)
- **Design Tokens**: Uses semantic colors, shadow levels, spacing
- **Library**: Adobe Spectrum React Card, Badge, Link, Button, Text
