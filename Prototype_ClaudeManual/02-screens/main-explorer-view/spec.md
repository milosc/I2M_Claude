# Main Explorer View

**ID**: SCR-001
**Discovery ID**: S-1.1
**Application**: Web
**Priority**: P0
**Primary Persona**: PER-001 (Framework Creator), PER-002 (Product People), PER-003 (Developers)

## Overview

Primary interface for framework exploration with dual-pane master-detail layout enabling self-service learning. The screen provides a hierarchical navigation tree on the left and a tabbed detail pane on the right, allowing users to browse 115+ skills, commands, agents, rules, and hooks without overwhelming cognitive load.

**Key User Goals**:
- Navigate framework components visually without folder diving (JTBD-1.7)
- Understand component purpose and usage from context (JTBD-1.2, JTBD-1.1)
- Quickly copy file paths for VSCode editing (JTBD-1.5)
- Filter by workflow stage to reduce visible choices (JTBD-1.4)
- Bookmark frequently-used tools (JTBD-1.6)

## Layout

### Wireframe

```
┌────────────────────────────────────────────────────────────────────────────┐
│  Header                                                                    │
│  ┌─────────┐ ┌──────────────────────┐ ┌──────┐ ┌────────┐ ┌─────────┐    │
│  │ Logo    │ │ Search (Cmd+K)       │ │Theme │ │ Stage  │ │Favorites│    │
│  │ Claude  │ │ "skills, cmds..."    │ │Toggle│ │ Filter │ │  (icon) │    │
│  │ Manual  │ │                      │ │      │ │        │ │         │    │
│  └─────────┘ └──────────────────────┘ └──────┘ └────────┘ └─────────┘    │
├──────────────────────────────┬─────────────────────────────────────────────┤
│                              │                                             │
│ Navigation Tree (Master)     │ Detail Pane                                 │
│ ────────────────────────────│ ─────────────────────────────────────────── │
│                              │                                             │
│ ▼ Skills (85)           [i]  │ [Purpose | Examples | Options | Workflow | │
│   ▼ Discovery (29)       ↓   │  Traceability]                             │
│     ├ Discovery_JTBD    ⭐   │                                             │
│     ├ Discovery_Persona      │ # Discovery_JTBD                            │
│     ├ Discovery_Vision       │                                             │
│     └ ...                    │ **Path**: `.claude/skills/Discovery_JTBD/   │
│   ▼ Prototype (14)           │ SKILL.md`                                  │
│     ├ Prototype_DesignSystem │ [Copy Path] [Add to Favorites]             │
│     ├ Prototype_CodeGen      │                                             │
│     └ ...                    │ ## Purpose                                  │
│   ▼ ProductSpecs (10)        │ Extracts Jobs To Be Done from pain points, │
│   ▼ Implementation (5)       │ client facts, and user research. Generates │
│   ▼ Security (10)            │ structured JTBD document...                │
│   ▼ GRC (22)                 │                                             │
│                              │ ## Example                                  │
│ ▼ Commands (30)         [i]  │ ```bash                                     │
│   ├ /discovery               │ # Invoke skill directly                     │
│   ├ /discovery-multiagent⭐  │ /discovery ClaudeManual Client_Materials/  │
│   ├ /prototype               │ ```                                         │
│   └ ...                      │                                             │
│                              │ ## Options                                  │
│ ▼ Agents (25)           [i]  │ | Parameter | Type | Required | Default |  │
│   ▼ Discovery (6)            │ |-----------|------|----------|----------|  │
│   ▼ Quality (4)              │ | input_dir | Path | Yes      | -        | │
│   └ ...                      │                                             │
│                              │ [Workflow Diagram - Mermaid]                │
│ ▼ Rules (5)             [i]  │                                             │
│                              │                                             │
│ ▼ Hooks (8)             [i]  │                                             │
│                              │                                             │
│ [Collapse All] [Expand All]  │                                             │
│                              │                                             │
├──────────────────────────────┴─────────────────────────────────────────────┤
│ Footer: Version 3.0.0 | Last Updated: 2026-01-31 | © HTEC Framework       │
└────────────────────────────────────────────────────────────────────────────┘
```

### Grid Structure

| Region | Grid Columns | Breakpoint | Width | Components |
|--------|--------------|------------|-------|------------|
| Header | 1-12 | All | Full width | Logo, SearchBar, ThemeToggle, StageFilterDropdown, FavoritesButton |
| Sidebar (Master) | 1-4 | Desktop (>1024px) | 300px fixed | NavigationTree |
| Sidebar (Master) | Off-canvas drawer | Tablet/Mobile (<1024px) | 280px overlay | NavigationTree |
| Main (Detail) | 5-12 | Desktop | Flexible | DetailPane |
| Main (Detail) | 1-12 | Tablet/Mobile | Full width | DetailPane |
| Footer | 1-12 | All | Full width | Text (version info) |

## Components Used

| Component ID | Component Name | Instance Name | Props | Library Components Used |
|--------------|----------------|---------------|-------|------------------------|
| COMP-AGG-001 | NavigationTree | mainNav | `onSelect={handleItemSelect}`, `expandedNodes={expandedNodes}`, `favorites={userFavorites}` | Tree, Badge, Tooltip, TextField |
| COMP-AGG-002 | DetailPane | detailView | `selectedItem={selectedItem}`, `tabs={['Purpose', 'Examples', 'Options', 'Workflow', 'Traceability']}` | Tabs, View, Heading, Link, Button |
| COMP-AGG-006 | StageFilterDropdown | stageFilter | `value={selectedStages}`, `onChange={handleStageFilter}`, `options={STAGE_OPTIONS}` | Select, Badge, Text |
| N/A (Library) | Button | favoritesBtn | `variant="ghost"`, `icon={<Star />}`, `onClick={navToFavorites}` | Button |
| N/A (Library) | TextField | searchInput | `placeholder="Search (Cmd+K)"`, `onFocus={navToSearch}` | TextField |
| N/A (Library) | Switch | themeToggle | `isSelected={isDark}`, `onChange={handleThemeToggle}` | Switch |

## Data Requirements

### Page Load Data

| Field | Source | Entity | Type | Required | Description |
|-------|--------|--------|------|----------|-------------|
| skills | GET /api/skills | Skill | Skill[] | Yes | List of all skills with frontmatter |
| commands | GET /api/commands | Command | Command[] | Yes | List of all commands |
| agents | GET /api/agents | Agent | Agent[] | Yes | List of all agents |
| rules | GET /api/rules | Rule | Rule[] | Yes | List of all rules |
| hooks | GET /api/hooks | Hook | Hook[] | Yes | List of all hooks |
| userPreferences | localStorage | UserPreferences | UserPreferences | Yes | Theme, favorites, collapsed nodes, stage filter |

### User Input Data

| Field | Component | Validation | Storage |
|-------|-----------|------------|---------|
| selectedItem | NavigationTree | Must exist in items array | sessionStorage (last_viewed) |
| expandedNodes | NavigationTree | Array of valid node IDs | localStorage (collapsed_nodes) |
| selectedStages | StageFilterDropdown | Subset of ['Discovery', 'Prototype', 'ProductSpecs', 'SolArch', 'Implementation', 'Utility', 'GRC', 'Security'] | localStorage (stage_filter) |
| isDarkMode | Switch | Boolean | localStorage (theme) |
| favorites | Button clicks | Array of item IDs | localStorage (favorites) |

## State Management

### Local State (React useState)

```typescript
interface ScreenState {
  items: Array<Skill | Command | Agent | Rule | Hook>; // Loaded from API
  selectedItem: Skill | Command | Agent | Rule | Hook | null; // Currently selected item
  expandedNodes: string[]; // Node IDs that are expanded
  selectedStages: string[]; // Active stage filters
  isLoading: boolean; // Loading state for API calls
  error: string | null; // Error message if API fails
  searchFocused: boolean; // Whether search bar is focused
}
```

### Global State Dependencies (LocalStorage)

| Store | Slice | Usage | Default Value |
|-------|-------|-------|---------------|
| userPreferences | theme | Apply light/dark mode | 'system' |
| userPreferences | favorites | Highlight favorited items with ⭐ | [] |
| userPreferences | collapsed_nodes | Persist tree expansion state | [] |
| userPreferences | last_viewed | Auto-select last viewed item on page load | null |
| userPreferences | stage_filter | Pre-apply stage filter if set | [] |

## Navigation

### Entry Points

| From | Trigger | Params | State Initialization |
|------|---------|--------|---------------------|
| Direct URL | App launch | / | Load all items, apply saved filters, select last_viewed |
| Home Page | Click "Explore Framework" | / | Same as direct URL |
| Deep Link | URL with item ID | /?item=Discovery_JTBD | Load all items, select specified item, expand parent nodes |
| Search Results | Click result | /?item={item_id} | Same as deep link |
| Favorites Page | Click favorite | /?item={item_id} | Same as deep link |

### Exit Points

| To | Trigger | Data Passed | State Persistence |
|----|---------|-------------|-------------------|
| Search Results (SCR-002) | Focus search bar, type query | Query string | Save current selectedItem to last_viewed |
| Stage-Filtered View (SCR-003) | Select stage filter | Selected stages | Same screen, update URL params |
| Favorites Page (SCR-004) | Click Favorites button | - | Save current selectedItem |
| Component Detail Modal (SCR-006) | Click "View Details" in DetailPane | selectedItem | Modal overlay, no navigation |

## Interactions

### User Actions

| Action | Component | Handler | Result | UX Psychology |
|--------|-----------|---------|--------|---------------|
| Click tree item | NavigationTree | onSelect | Update selectedItem, scroll DetailPane to top, save to last_viewed | **Instant Feedback**: Detail pane updates within 200ms |
| Expand/collapse node | NavigationTree | onToggle | Toggle node in expandedNodes array, persist to localStorage | **Persistence**: State survives page refresh |
| Click "Copy Path" | Button in DetailPane | onClick | Copy item.path to clipboard, show toast | **Friction Reduction**: Single-click file access (JTBD-1.5) |
| Click "Add to Favorites" | Button in DetailPane | onClick | Add/remove item.id from favorites, persist to localStorage | **Personalization**: Bookmark frequently-used tools (JTBD-1.6) |
| Select stage filter | StageFilterDropdown | onChange | Filter items array by stage, update count badges | **Hicks Law**: Reduce visible items from 115+ to ~20-40 (JTBD-1.4) |
| Toggle theme | Switch | onChange | Update theme in localStorage, apply CSS class to body | **Visual Comfort**: Light/dark mode (CF-016) |
| Focus search bar | TextField | onFocus | Navigate to SCR-002 (Search Results Page) | **Progressive Disclosure**: Dedicated search UI |
| Keyboard Cmd+K | Window listener | onKeyDown | Focus search bar | **Power User**: Keyboard shortcut (JTBD-2.2) |

### Keyboard Shortcuts

| Key | Action | Focus Requirement |
|-----|--------|------------------|
| `/` | Focus search bar | Any |
| `Cmd+K` / `Ctrl+K` | Focus search bar | Any |
| `Esc` | Clear selection, collapse all filters | Any |
| `Tab` | Navigate tree items | Tree focused |
| `Enter` | Select focused tree item | Tree focused |
| `←` / `→` | Collapse/expand focused tree node | Tree focused |

## Responsive Behavior

| Breakpoint | Screen Width | Layout Changes | Component Behavior |
|------------|--------------|----------------|-------------------|
| Desktop | >1024px | Dual-pane side-by-side, fixed 300px sidebar | Full wireframe as specified |
| Tablet | 768-1024px | Sidebar becomes collapsible drawer, hamburger menu | NavigationTree hidden by default, slides in from left |
| Mobile | <768px | Full-width detail pane, bottom sheet navigation | Sidebar as bottom sheet, swipe up to reveal tree |

### Mobile-Specific Changes

- Header: Logo shrinks, search bar collapses to icon, stage filter moves to drawer
- Navigation: Hamburger menu (☰) opens drawer overlay
- Detail Pane: Full viewport width, tabs stack vertically if needed
- Touch Targets: Minimum 44×44px for tree items and buttons

## Accessibility

### WCAG 2.1 AA Compliance

| Criterion | Implementation | Validation Method |
|-----------|----------------|-------------------|
| **Page Title** | "ClaudeManual - Main Explorer View" | Unique `<title>` tag |
| **Landmarks** | header, nav (tree), main (detail), footer | ARIA roles + semantic HTML |
| **Skip Link** | "Skip to main content" focuses DetailPane | Hidden until focused |
| **Focus Management** | Focus first tree item on page load | tabindex management |
| **Keyboard Navigation** | Full keyboard support (Tab, Enter, Arrow keys) | Manual testing + axe-core |
| **Screen Reader** | Tree announced as "Navigation tree with 5 categories, 115 items" | NVDA/VoiceOver testing |
| **ARIA Labels** | `aria-label="Copy file path"` on Copy button | Axe DevTools scan |
| **Live Regions** | `aria-live="polite"` for toast notifications | Screen reader testing |
| **Color Contrast** | Text: 4.5:1 minimum, UI: 3:1 minimum | Contrast checker |
| **Focus Indicators** | 2px blue ring on all focusable elements | Visual inspection |

### Announcements (aria-live)

| Event | Announcement | Politeness Level |
|-------|--------------|------------------|
| Page load | "Loaded 115 framework components" | polite |
| Item selected | "Selected: {item.name}" | polite |
| Stage filter applied | "Filtered to {count} items in {stage} stage" | polite |
| Path copied | "File path copied to clipboard" | assertive |
| Favorite added | "{item.name} added to favorites" | polite |

## Error States

| State | Condition | Display | Recovery Action |
|-------|-----------|---------|-----------------|
| **API Load Error** | GET /api/skills fails | ErrorBanner: "Failed to load framework components. Retry?" | [Retry] button re-fetches |
| **Empty State** | No items loaded | EmptyState illustration: "No components found. Check API connection." | [Refresh Page] button |
| **Partial Load Error** | Some endpoints fail | Warning Toast: "Loaded skills and commands, but agents failed to load." | Continue with partial data |
| **Markdown Parse Error** | DetailPane fails to render content | Error in detail pane: "Content unavailable. View source file instead." | [Copy Path] button as fallback |
| **Favorites Sync Error** | localStorage quota exceeded | Warning: "Favorites not saved. Clear browser cache." | Degrade gracefully, favorites lost on refresh |
| **Invalid Deep Link** | URL param item ID not found | Navigate to default view, show toast: "Item not found." | Auto-recover, show all items |

## Performance Targets

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Initial Load** | <2 seconds (API + render) | Lighthouse Performance score |
| **Tree Expansion** | <100ms | React DevTools Profiler |
| **Detail Pane Update** | <200ms | User perception (feels instant) |
| **Search Focus** | <50ms | Manual testing |
| **Stage Filter Apply** | <300ms | React DevTools Profiler |
| **Favorites Toggle** | <100ms (optimistic update) | Manual testing |

### Optimization Strategies

- **Lazy Load Detail Content**: Only fetch markdown content when item is selected
- **Virtual Scrolling**: For tree with 115+ items (react-window)
- **Memoization**: useMemo for filtered items array
- **Debounce**: Stage filter changes debounced 300ms
- **Code Splitting**: Detail pane tabs loaded on-demand
- **Caching**: API responses cached in sessionStorage for 5 minutes

## Traceability

### Pain Points Addressed

| Pain Point | How Addressed | Validation |
|------------|---------------|------------|
| PP-1.1 (Knowledge Transfer) | Self-service UI eliminates need for developer walkthroughs | User testing: new user completes exploration in <60 min |
| PP-1.2 (Contextual Documentation) | Multi-section detail pane with Purpose/Examples/Options | User testing: users find usage examples without asking |
| PP-1.4 (Organizational Chaos) | Stage filtering reduces 115+ items to ~20-40 per stage | Analytics: 70%+ users apply stage filter within first session |
| PP-1.6 (Developer Friction) | Copy Path button eliminates 10-15 min of manual navigation | Analytics: 90%+ users click Copy Path within first use |

### JTBD Coverage

| JTBD | Implementation | Success Criteria |
|------|----------------|------------------|
| JTBD-1.1 (Self-service learning) | DetailPane with Purpose/Examples tabs | 80%+ users complete onboarding without human help |
| JTBD-1.2 (Component context) | Workflow tab with Mermaid diagrams | 70%+ users view Workflow tab when learning new skill |
| JTBD-1.4 (Stage-appropriate tools) | Stage filter dropdown | 60%+ users apply stage filter within 2 sessions |
| JTBD-1.5 (Edit source files) | Copy Path button | 90%+ users copy path within first 5 uses |
| JTBD-1.6 (Bookmark tools) | Add to Favorites button | 60%+ users have 3+ favorites within 4 weeks |
| JTBD-1.7 (Navigate hierarchies) | Tree navigation with expand/collapse | 80%+ users successfully navigate to target item in <2 min |

### Client Facts Referenced

| Client Fact | Implementation | Validation |
|-------------|----------------|------------|
| CF-006 (Master-detail UI) | Dual-pane layout with NavigationTree + DetailPane | Screenshot comparison |
| CF-008 (Multi-section documentation) | Tabbed interface with 5 tabs | Component props validation |
| CF-013 (File path references) | Copy Path button in every detail view | Functional testing |
| CF-014 (Minimalistic terminal look) | JetBrains Mono font, monochrome color scheme | Design review |
| CF-016 (Light/dark theme) | Theme toggle in header, persisted to localStorage | Functional testing |

### Requirements Linked

| Requirement | Field/Component | Status |
|-------------|-----------------|--------|
| REQ-021 (Browse skills) | NavigationTree with Skill category | ✅ Implemented |
| REQ-022 (Stage filtering) | StageFilterDropdown | ✅ Implemented |
| REQ-023 (File path access) | Copy Path button | ✅ Implemented |
| REQ-024 (Favorites) | Add to Favorites button | ✅ Implemented |
| REQ-025 (Search) | Search bar (navigates to SCR-002) | ✅ Implemented |
| REQ-026 (Workflow visualization) | Workflow tab in DetailPane | ✅ Implemented |

---

*Traceability: S-1.1, JTBD-1.1, JTBD-1.2, JTBD-1.4, JTBD-1.5, JTBD-1.6, JTBD-1.7, PP-1.1, PP-1.2, PP-1.4, PP-1.6, CF-006, CF-008, CF-013, CF-014, CF-016, REQ-021, REQ-022, REQ-023, REQ-024, REQ-025, REQ-026*

*Components: COMP-AGG-001 (NavigationTree), COMP-AGG-002 (DetailPane), COMP-AGG-006 (StageFilterDropdown)*

*Screen specification complete with full layout, data requirements, state management, navigation flows, interactions, responsive behavior, accessibility, error states, and performance targets.*
