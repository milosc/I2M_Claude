# Component Index - ClaudeManual

---
system_name: ClaudeManual
checkpoint: CP-8
component_count: 11
aggregate_components: 11
library_components_used: 16
date_created: 2026-01-31
last_modified: 2026-02-01
session: session-components-claudemanual
created_by: prototype-component-specifier
modified_by: prototype-feedback PF-002
assembly_first: true
---

## Assembly-First Approach

This component specification follows **Assembly-First Architecture**: we use Adobe Spectrum React components as the foundation and define ONLY aggregate components that combine library components with ClaudeManual-specific business logic.

**Library Used**: Adobe Spectrum React (62 components available)

**Assembly Strategy**:
- ✅ **DO**: Create aggregate components for business logic (NavigationTree, DetailPane, SearchResultCard)
- ❌ **DON'T**: Recreate primitive components (Button, TextField, Select, Table, Tree, Tabs)

---

## Aggregate Components Inventory

| Component ID | Component Name | Category | Priority | Library Components Used |
|---|---|---|---|---|
| COMP-AGG-001 | NavigationTree | Navigation | P0 | Tree, Badge, Tooltip, TextField |
| COMP-AGG-002 | DetailPane | Content Display | P0 | Tabs, View, Heading, Link, Button |
| COMP-AGG-003 | SearchResultCard | Search | P0 | Card, Badge, Link, Button, Text |
| COMP-AGG-004 | ComponentCard | Content Display | P1 | Card, Badge, Button, Switch, StatusLight |
| COMP-AGG-005 | FavoritesPanel | Collections | P1 | GridList, Card, Button, IllustratedMessage |
| COMP-AGG-006 | StageFilterDropdown | Filters | P1 | Select, Badge, Text |
| COMP-AGG-007 | DiagramViewer | Visualizations | P1 | View, Button, Toolbar, Slider |
| COMP-AGG-008 | MarkdownRenderer | Content Display | P0 | View, Heading, Text, Link |
| COMP-AGG-009 | TagDisplay | Tags | P1 | - (custom badges) |
| COMP-AGG-010 | TagInput | Tags | P1 | ComboBox, Item |
| COMP-AGG-011 | TagFilter | Tags | P1 | - (custom buttons) |

---

## Library Component Usage Summary

### Adobe Spectrum React Components Used (15 total)

| Library Component | Used In Aggregate Components | Count |
|---|---|---|
| Tree | NavigationTree | 1 |
| Badge | NavigationTree, SearchResultCard, ComponentCard, StageFilterDropdown | 4 |
| Tooltip | NavigationTree | 1 |
| TextField | NavigationTree | 1 |
| Tabs | DetailPane | 1 |
| View | DetailPane, DiagramViewer, MarkdownRenderer | 3 |
| Heading | DetailPane, MarkdownRenderer | 2 |
| Link | DetailPane, SearchResultCard, MarkdownRenderer | 3 |
| Button | DetailPane, SearchResultCard, ComponentCard, FavoritesPanel, DiagramViewer | 5 |
| Card | SearchResultCard, ComponentCard, FavoritesPanel | 3 |
| Text | SearchResultCard, StageFilterDropdown, MarkdownRenderer | 3 |
| Switch | ComponentCard | 1 |
| StatusLight | ComponentCard | 1 |
| GridList | FavoritesPanel | 1 |
| IllustratedMessage | FavoritesPanel | 1 |
| Select | StageFilterDropdown | 1 |
| Toolbar | DiagramViewer | 1 |
| Slider | DiagramViewer | 1 |

---

## Component Categories

### Navigation (1 component)
- **COMP-AGG-001**: NavigationTree - Hierarchical framework explorer with stage filtering and favorites

### Content Display (3 components)
- **COMP-AGG-002**: DetailPane - Tabbed documentation viewer with markdown rendering
- **COMP-AGG-004**: ComponentCard - Framework component card with metadata and favorite toggle
- **COMP-AGG-008**: MarkdownRenderer - Markdown content renderer with Mermaid diagram support

### Search (1 component)
- **COMP-AGG-003**: SearchResultCard - Search result preview with metadata and quick actions

### Collections (1 component)
- **COMP-AGG-005**: FavoritesPanel - User-curated favorites list with drag-drop reordering

### Filters (1 component)
- **COMP-AGG-006**: StageFilterDropdown - Multi-select stage filter with visual badges

### Visualizations (1 component)
- **COMP-AGG-007**: DiagramViewer - Mermaid/PlantUML diagram renderer with zoom/pan controls

### Tags (3 components) - PF-002
- **COMP-AGG-009**: TagDisplay - Displays tags as badges with optional remove capability
- **COMP-AGG-010**: TagInput - Autocomplete input for adding tags to components
- **COMP-AGG-011**: TagFilter - Multi-select filter for filtering search results by tags

---

## Screen-to-Component Mapping

| Screen ID | Screen Name | Aggregate Components Used |
|---|---|---|
| SCR-001 | Main Explorer View | NavigationTree, DetailPane, StageFilterDropdown |
| SCR-002 | Search Results Page | SearchResultCard, StageFilterDropdown |
| SCR-003 | Stage-Filtered View | NavigationTree, DetailPane, StageFilterDropdown |
| SCR-004 | Favorites Page | FavoritesPanel, ComponentCard |
| SCR-005 | Comparison View | ComponentCard |
| SCR-006 | Component Detail Modal | DetailPane, MarkdownRenderer |
| SCR-009 | Workflow Viewer | DiagramViewer, MarkdownRenderer |
| SCR-010 | Architecture Browser | NavigationTree, DiagramViewer, MarkdownRenderer |
| SCR-011 | Document Preview Modal | DiagramViewer, MarkdownRenderer |

---

## Priority Breakdown

- **P0 (MVP)**: 4 components (NavigationTree, DetailPane, SearchResultCard, MarkdownRenderer)
- **P1 (Phase 2)**: 7 components (ComponentCard, FavoritesPanel, StageFilterDropdown, DiagramViewer, TagDisplay, TagInput, TagFilter)
- **P2 (Future)**: 0 components

---

## Design Token Integration

All aggregate components use tokens from `/00-foundation/design-tokens/tokens.json`:

- **Colors**: Stage-specific colors (Discovery=blue, Prototype=green, etc.)
- **Typography**: JetBrains Mono for terminal-inspired UI (CF-014)
- **Spacing**: 4px base unit system
- **Shadows**: Elevation levels for cards and modals
- **Motion**: 200ms default transitions

---

## Accessibility Requirements

All components follow WCAG 2.1 AA standards:

- **Keyboard Navigation**: Full keyboard support (Tab, Enter, Space, Arrow keys)
- **Screen Reader Support**: ARIA labels, roles, live regions
- **Focus Management**: Visible focus indicators (2px blue ring)
- **Color Contrast**: 4.5:1 minimum for text, 3:1 for UI components
- **Motion**: Respects `prefers-reduced-motion` preference

---

## Next Steps

1. Generate detailed specs for each aggregate component (COMP-AGG-001 to COMP-AGG-008)
2. Define TypeScript interfaces for props
3. Map component variants to design tokens
4. Document Spectrum React integration patterns
5. Create usage examples with library component composition

---

*8 aggregate components defined using 15 Adobe Spectrum React library components. Assembly-first approach ensures rapid development with maintained consistency and accessibility.*
