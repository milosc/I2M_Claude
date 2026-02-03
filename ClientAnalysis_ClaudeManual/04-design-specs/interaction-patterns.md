# Interaction Patterns - ClaudeManual

---
system_name: ClaudeManual
checkpoint: CP-9
total_patterns: 18
pattern_categories: 6
date_created: 2026-01-31
session: disc-claude-manual-009d
created_by: discovery-interaction-specifier
traceability:
  - JTBD-1.1 (Self-Service Framework Learning)
  - JTBD-1.2 (Component Context Understanding)
  - JTBD-1.3 (Quick Tool Discovery)
  - JTBD-1.4 (Stage-Based Filtering)
  - JTBD-1.5 (Edit Source Files)
  - JTBD-1.6 (Bookmark Favorites)
  - JTBD-1.7 (Visual Hierarchy Navigation)
  - JTBD-1.8 (Component Comparison)
  - CF-003 (Highly Visual)
  - CF-006 (Master-Detail Panes)
  - CF-007 (Click to Open Detail)
  - CF-009 (Search Page)
  - CF-012 (Favorites Concept)
  - CF-013 (File Path Reference)
  - CF-016 (Light/Dark Theme)
---

## Executive Summary

This document defines **18 interaction patterns** across 6 categories for the ClaudeManual interface. Patterns prioritize **self-service learning** (JTBD-1.1), **visual hierarchy navigation** (JTBD-1.7), **quick tool discovery** (JTBD-1.3), and **diagram visualization** (JTBD-1.9). All interactions support both keyboard and mouse input to meet developer efficiency needs.

**Pattern Distribution**:
- **Navigation Interactions**: 4 patterns (tree, tabs, breadcrumbs, keyboard)
- **Search & Discovery**: 3 patterns (instant search, stage filtering, comparison)
- **Data Management**: 3 patterns (favorites, copy path, theme toggle)
- **Diagram Rendering**: 4 patterns (mermaid, plantuml, zoom/pan, export)
- **Feedback Patterns**: 2 patterns (toast notifications, loading states)
- **Responsive Behavior**: 2 patterns (desktop/tablet/mobile, accessibility)

**Performance Targets**:
- Search results: < 200ms
- Tree expand/collapse: 200ms animation
- Navigation transitions: 300ms
- Toast notifications: 200ms appear, 2s auto-dismiss

---

## Pattern Categories

### 1. Navigation Interactions

#### PAT-001: Hierarchical Tree Navigation

**ID**: PAT-001
**Type**: Navigation
**Priority**: P0
**Traces To**: JTBD-1.1, JTBD-1.7, CF-006, CF-007
**Used In**: All screens (SCR-001 through SCR-005)

**Trigger**: User clicks tree node or uses keyboard arrows

**Behavior**:
1. **Expandable nodes** (categories):
   - Click on node → toggle expand/collapse
   - Rotate chevron icon 90° clockwise (collapsed → expanded)
   - Reveal/hide child nodes with slide-down animation (200ms)
   - Store expansion state in localStorage (persist across sessions)

2. **Leaf nodes** (skills/commands/agents):
   - Click on node → select item
   - Highlight selected node with background color
   - Load detail view in right pane
   - Update URL to reflect selection (e.g., `/skills/discovery-jtbd`)
   - Store last selection in localStorage

3. **Visual Hierarchy**:
   - Indentation: 16px per nesting level
   - Icons: Folder icon for categories, document icon for items
   - Badges: Show stage (Discovery/Prototype/Implementation/Utility)
   - Count indicators: Show number of children for categories

**Animation**:
- Expand/collapse: 200ms ease-out
- Selection highlight: 150ms background color transition
- Chevron rotation: 200ms ease-out

**Feedback**:
- **Selected state**: Background color (light: #e0f2fe, dark: #1e3a5f)
- **Hover state**: Subtle background change (light: #f0f9ff, dark: #0f2942)
- **Keyboard focus**: 2px blue outline
- **Expanded state**: Rotated chevron, revealed children

**Keyboard Shortcuts**:
- `↑/↓`: Navigate tree items
- `←`: Collapse current node
- `→`: Expand current node
- `Enter`: Select item

**Performance**: Tree with 115 items renders in < 100ms

**Client Facts**: CF-006 (Master-Detail Panes), CF-007 (Click to Open)

---

#### PAT-002: Stage-Based Tab Navigation

**ID**: PAT-002
**Type**: Navigation
**Priority**: P1
**Traces To**: JTBD-1.4, CF-011
**Used In**: SCR-001 (Browse by Category)

**Trigger**: User clicks stage tab (Discovery/Prototype/ProductSpecs/SolArch/Implementation/Utility)

**Behavior**:
1. Filter tree to show only items matching selected stage
2. Update active tab indicator (underline + color)
3. Update URL query parameter (e.g., `?stage=discovery`)
4. Store stage preference in localStorage
5. Maintain item selection if still visible after filter
6. Clear selection if filtered out

**Visual States**:
- **Active tab**: Blue underline, bold text, primary color
- **Inactive tab**: Gray text, no underline
- **Hover tab**: Subtle background highlight
- **Badge count**: Show number of items per stage

**Animation**: Tab transition 150ms ease-in-out

**Feedback**:
- Active tab visually distinct
- Filtered tree updates instantly
- Badge counts update to reflect current view

**Keyboard Shortcuts**:
- `Tab`: Cycle through stage tabs
- `Shift+Tab`: Reverse cycle

**Client Facts**: CF-011 (Stages: Discovery, Prototyping, Implementation, Utilities)

---

#### PAT-003: Breadcrumb Navigation

**ID**: PAT-003
**Type**: Navigation
**Priority**: P2
**Traces To**: JTBD-1.7
**Used In**: SCR-001 (Browse by Category), Detail views

**Trigger**: User navigates to nested item

**Behavior**:
1. Display breadcrumb trail: Home > Category > Subcategory > Item
2. Each segment is clickable
3. Clicking segment navigates to that level
4. Hover shows underline
5. Truncate long paths with ellipsis (show last 3 segments)

**Visual**:
- Separator: `/` or `>`
- Current item: Bold, not clickable
- Previous items: Links with hover underline
- Truncation: `... > Category > Item`

**Animation**: Breadcrumb transition 100ms fade

**Feedback**:
- Hover: Underline previous segments
- Click: Navigate to parent level

---

#### PAT-004: Keyboard-First Navigation

**ID**: PAT-004
**Type**: Navigation
**Priority**: P0
**Traces To**: JTBD-1.3, JTBD-1.5, CF-013
**Used In**: All screens

**Global Shortcuts**:
| Key | Context | Action |
|-----|---------|--------|
| `/` | Global | Focus search bar |
| `Esc` | Search | Clear and blur search |
| `↑/↓` | Tree | Navigate items |
| `←/→` | Tree | Collapse/Expand |
| `Enter` | Tree | Select item |
| `f` | Detail view | Toggle favorite |
| `c` | Detail view | Copy file path |
| `t` | Global | Toggle theme |
| `?` | Global | Show keyboard shortcuts help |

**Behavior**:
1. All shortcuts work globally unless context-specific
2. Shortcuts display in tooltip on hover
3. `?` opens modal with full shortcut list
4. Focus indicators always visible (2px blue outline)

**Accessibility**:
- All interactive elements keyboard accessible
- Tab order follows visual layout
- Skip-to-content link for screen readers
- Shortcut help modal accessible via keyboard

**Client Facts**: CF-013 (Copy file path for editing)

---

### 2. Search & Discovery

#### PAT-005: Instant Search with Filtering

**ID**: PAT-005
**Type**: Search
**Priority**: P0
**Traces To**: JTBD-1.3, CF-009
**Used In**: SCR-002 (Search)

**Trigger**: User types in search bar

**Behavior**:
1. **Debounce**: 150ms after last keystroke
2. **Search scope**: Name, description, tags, file path
3. **Results display**: Dropdown below search bar (max 10 results)
4. **Highlighting**: Matching text highlighted in results
5. **Keyboard navigation**: `↑/↓` to navigate, `Enter` to select
6. **Empty state**: "No matches found" with search tips
7. **Loading state**: Show spinner during search

**Search Ranking**:
1. Exact name match (highest priority)
2. Name starts with query
3. Description contains query
4. Tag match
5. File path contains query

**Visual States**:
- **Empty**: Placeholder "Search skills, commands, agents..." (gray text)
- **Loading**: Spinner icon (200ms delay before showing)
- **Results**: Dropdown with item cards (icon, name, stage badge, excerpt)
- **No results**: "No matches found. Try 'discovery', 'prototype', or 'implementation'."
- **Focused**: Blue outline, expanded dropdown

**Animation**:
- Dropdown appear: 200ms slide-down + fade
- Result hover: 100ms background highlight

**Feedback**:
- Type indicator: Character count badge
- Result count: "5 results" above dropdown
- Hover: Highlight result row

**Performance**: Results in < 200ms (measured from last keystroke)

**Keyboard Shortcuts**:
- `/`: Focus search
- `Esc`: Clear and blur
- `↑/↓`: Navigate results
- `Enter`: Select result

**Client Facts**: CF-009 (Search page)

---

#### PAT-006: Multi-Faceted Filtering

**ID**: PAT-006
**Type**: Search
**Priority**: P1
**Traces To**: JTBD-1.3, JTBD-1.4
**Used In**: SCR-002 (Search)

**Trigger**: User applies filters (stage, type, tags)

**Behavior**:
1. **Filter types**:
   - Stage: Discovery, Prototype, ProductSpecs, SolArch, Implementation, Utility
   - Type: Skill, Command, Agent
   - Tags: User-defined tags (from frontmatter)
2. **Combination**: Filters combine with AND logic
3. **Visual feedback**: Active filters shown as pills/chips
4. **Clear filters**: X button on each pill, "Clear all" button
5. **Filter persistence**: Store in URL query params

**Visual**:
- Filter pills: Color-coded by type (blue: stage, green: type, purple: tags)
- Active count: Badge showing number of active filters
- Clear button: X icon on hover

**Animation**: Filter apply 150ms transition

**Feedback**:
- Result count updates: "42 results → 8 results"
- Empty state: "No items match filters. Try removing some filters."

**Performance**: Filter operation < 50ms

---

#### PAT-007: Side-by-Side Component Comparison

**ID**: PAT-007
**Type**: Discovery
**Priority**: P1
**Traces To**: JTBD-1.8
**Used In**: SCR-005 (Component Detail)

**Trigger**: User clicks "Compare with..." button in detail view

**Behavior**:
1. Show comparison mode toggle button
2. User selects second component from dropdown
3. Split screen: Left pane = Component A, Right pane = Component B
4. Synchronized scrolling (optional toggle)
5. Highlight differences (features, options, performance)
6. Decision guidance section: "Use A when..., Use B when..."

**Visual**:
- Split-screen layout: 50/50 width
- Difference highlights: Yellow background for unique features
- Synchronized scroll indicator: Lock icon
- Exit comparison: Close button or `Esc` key

**Animation**: Split-screen transition 300ms ease-in-out

**Feedback**:
- Tooltip: "Compare with /discovery-multiagent"
- Differences highlighted
- Guidance section: "Choose /discovery for single-threaded execution, /discovery-multiagent for 60% faster parallel execution"

**Keyboard Shortcuts**:
- `Esc`: Exit comparison mode
- `↑/↓`: Synchronized scroll (when enabled)

---

### 3. Data Management

#### PAT-008: Favorites Management

**ID**: PAT-008
**Type**: Data Management
**Priority**: P2
**Traces To**: JTBD-1.6, CF-012
**Used In**: SCR-003 (Favorites), Detail views

**Trigger**: User clicks star icon

**Behavior**:
1. **Toggle favorite**: Click star → add/remove from favorites
2. **Visual feedback**: Star fills (added) or empties (removed)
3. **Persistence**: Store in localStorage (array of item IDs)
4. **Favorites view**: Dedicated section showing all favorited items
5. **Reordering**: Drag-and-drop to reorder (optional)
6. **Sync**: Export/import favorites JSON (optional)

**Visual States**:
- **Not favorited**: Outline star icon (gray)
- **Favorited**: Filled star icon (yellow)
- **Hover**: Scale 1.1x, pulse animation

**Animation**:
- Star fill: 200ms pulse + color transition
- Remove: 150ms fade out

**Feedback**:
- Toast notification: "Added to Favorites" or "Removed from Favorites"
- Favorites count badge: Show total count in sidebar

**Keyboard Shortcuts**:
- `f`: Toggle favorite (when detail view focused)

**Client Facts**: CF-012 (Favorites concept)

---

#### PAT-009: Copy File Path to Clipboard

**ID**: PAT-009
**Type**: Data Management
**Priority**: P1
**Traces To**: JTBD-1.5, CF-013
**Used In**: SCR-005 (Component Detail)

**Trigger**: User clicks "Copy Path" button

**Behavior**:
1. Copy full file path to clipboard (e.g., `.claude/skills/Discovery_JTBD/SKILL.md`)
2. Show toast notification: "📋 Copied to clipboard"
3. Button icon changes: Copy icon → Checkmark icon
4. Revert icon after 2 seconds
5. Error handling: Show error toast if clipboard access denied

**Visual States**:
- **Default**: Copy icon (📋)
- **Success**: Checkmark icon (✅)
- **Hover**: Tooltip "Copy file path"

**Animation**:
- Icon transition: 150ms fade
- Toast: 200ms slide-in from bottom

**Feedback**:
- Toast notification: "📋 Copied to clipboard"
- Button state change (copy → check)

**Performance**: Copy operation < 10ms

**Client Facts**: CF-013 (File path reference for editing)

---

#### PAT-010: Theme Toggle

**ID**: PAT-010
**Type**: Data Management
**Priority**: P1
**Traces To**: CF-016
**Used In**: All screens

**Trigger**: User clicks theme toggle button

**Behavior**:
1. **Modes**: Light, Dark, System (follows OS preference)
2. **Toggle order**: Light → Dark → System → Light
3. **Persistence**: Store preference in localStorage
4. **CSS variables**: Instant update of color scheme
5. **System mode**: Listen to `prefers-color-scheme` media query

**Visual States**:
- **Light mode**: Sun icon
- **Dark mode**: Moon icon
- **System mode**: Auto icon

**Animation**: 100ms transition for background, text, border colors

**Feedback**:
- Icon changes to reflect current mode
- Tooltip shows next mode: "Switch to Dark Mode"

**Keyboard Shortcuts**:
- `t`: Toggle theme

**Performance**: Theme switch < 50ms

**Client Facts**: CF-016 (Light and dark themes)

---

### 4. Diagram Rendering

#### PAT-015: Mermaid Diagram Rendering

**ID**: PAT-015
**Type**: Diagram Rendering
**Priority**: P1
**Traces To**: JTBD-1.9, JTBD-1.2, CF-003
**Used In**: SCR-009 (Workflow Viewer), SCR-010 (Architecture Browser), Detail views

**Trigger**: User navigates to workflow, architecture, or any document containing Mermaid diagrams

**Behavior**:
1. **Detection**: Parse markdown for ```mermaid code blocks or .mermaid files
2. **Rendering**: Use mermaid.js library to render SVG in-place
3. **Theme integration**: Apply light/dark theme to diagram colors
4. **Error handling**: Show fallback text if rendering fails
5. **Caching**: Cache rendered SVG for performance

**Supported Diagram Types**:
- Flowcharts (`graph TD`, `graph LR`)
- Sequence diagrams (`sequenceDiagram`)
- Class diagrams (`classDiagram`)
- State diagrams (`stateDiagram-v2`)
- Entity-relationship diagrams (`erDiagram`)
- Journey diagrams (`journey`)
- Gantt charts (`gantt`)
- Pie charts (`pie`)
- C4 diagrams (using mermaid-c4 extension)

**Visual States**:
- **Loading**: Skeleton placeholder with shimmer
- **Success**: Rendered SVG diagram
- **Error**: Code block with error message and syntax highlighting
- **Hover**: Subtle highlight border

**Animation**: Fade-in 200ms on render complete

**Performance**:
- Initial render: < 500ms for diagrams with < 50 nodes
- Re-render on theme change: < 100ms
- Cache hit: < 10ms

**Accessibility**:
- ARIA label describing diagram type
- Alt text for screen readers (generated from diagram title)
- High contrast mode support

---

#### PAT-016: PlantUML Diagram Rendering

**ID**: PAT-016
**Type**: Diagram Rendering
**Priority**: P1
**Traces To**: JTBD-1.9, JTBD-1.2
**Used In**: SCR-009 (Workflow Viewer), SCR-010 (Architecture Browser)

**Trigger**: User navigates to document containing PlantUML diagrams (.plantuml files or ```plantuml blocks)

**Behavior**:
1. **Detection**: Parse for @startuml/@enduml blocks or .plantuml files
2. **Rendering**: Send to PlantUML server (Kroki.io or self-hosted) for PNG/SVG generation
3. **Caching**: Cache rendered images with content hash key
4. **Fallback**: Show code block if server unavailable
5. **Theme**: Request light/dark variant based on current theme

**Supported Diagram Types**:
- Sequence diagrams
- Use case diagrams
- Class diagrams
- Activity diagrams
- Component diagrams
- State diagrams
- Object diagrams
- Deployment diagrams
- Timing diagrams
- C4 diagrams (PlantUML C4 stdlib)

**Visual States**:
- **Loading**: Spinner with "Rendering diagram..." text
- **Success**: Rendered PNG/SVG image
- **Error**: Code block with "Server unavailable" message
- **Offline**: Show cached version if available, otherwise code block

**Animation**: Fade-in 300ms on load complete

**Performance**:
- Server render: < 2s (network dependent)
- Cache hit: < 50ms
- Fallback threshold: 5s timeout

**Configuration**:
- Server URL: Configurable (default: kroki.io)
- Output format: SVG preferred, PNG fallback
- Max diagram size: 4096x4096 pixels

---

#### PAT-017: Diagram Zoom and Pan

**ID**: PAT-017
**Type**: Diagram Rendering
**Priority**: P1
**Traces To**: JTBD-1.9, JTBD-1.2
**Used In**: SCR-009 (Workflow Viewer), SCR-010 (Architecture Browser), SCR-011 (Document Preview Modal)

**Trigger**: User interacts with rendered diagram

**Behavior**:
1. **Zoom controls**: + / - buttons and mouse wheel/pinch gesture
2. **Pan**: Click and drag to pan viewport
3. **Reset**: Double-click or "Reset View" button returns to fit-to-container
4. **Zoom levels**: 25%, 50%, 75%, 100%, 150%, 200%, 300%
5. **Minimap**: Optional thumbnail showing current viewport position (large diagrams)

**Controls**:
| Control | Desktop | Mobile |
|---------|---------|--------|
| Zoom in | `+` button, Ctrl+scroll up | Pinch out |
| Zoom out | `-` button, Ctrl+scroll down | Pinch in |
| Pan | Click + drag | Touch drag |
| Reset | Double-click, `0` key | Double-tap |
| Fit width | `W` key | - |
| Fit height | `H` key | - |

**Visual**:
- Zoom controls: Floating toolbar (bottom-right of diagram)
- Current zoom level: Badge showing percentage
- Pan cursor: Grab cursor on hover, grabbing on drag
- Minimap: Semi-transparent overlay (top-right, opt-in)

**Animation**:
- Zoom: 150ms ease-out transition
- Pan: Immediate (no animation)
- Reset: 300ms ease-in-out

**Keyboard Shortcuts**:
- `+` / `=`: Zoom in
- `-`: Zoom out
- `0`: Reset to fit
- Arrow keys: Pan (when diagram focused)

**Performance**:
- Zoom transition: 60fps target
- Pan: Immediate response
- Large diagrams: Use canvas-based rendering for 500+ nodes

---

#### PAT-018: Diagram Export

**ID**: PAT-018
**Type**: Diagram Rendering
**Priority**: P2
**Traces To**: JTBD-1.9, JTBD-3.1
**Used In**: SCR-009, SCR-010, SCR-011

**Trigger**: User clicks "Export" button in diagram toolbar

**Behavior**:
1. **Format selection**: Dropdown with PNG, SVG, PDF options
2. **PNG export**: Render at 2x resolution for print quality
3. **SVG export**: Copy raw SVG with embedded fonts
4. **PDF export**: Generate single-page PDF with diagram centered
5. **Copy to clipboard**: Copy as image (PNG) for pasting

**Export Options**:
| Format | Use Case | Quality |
|--------|----------|---------|
| PNG | Quick sharing, presentations | 2x resolution |
| SVG | Web embedding, editing | Vector, scalable |
| PDF | Documentation, printing | 300 DPI |
| Clipboard | Paste into other apps | 2x PNG |

**Visual**:
- Export button: Download icon in toolbar
- Format dropdown: PNG (default), SVG, PDF
- Progress: Show "Exporting..." spinner for large diagrams
- Success: Toast notification with "Diagram exported"

**File Naming**: `{diagram_name}_{timestamp}.{extension}`

**Keyboard Shortcut**: `Ctrl+E` / `Cmd+E` opens export dropdown

**Performance**:
- PNG export: < 1s for typical diagrams
- PDF export: < 2s
- SVG export: < 100ms (no conversion needed)

---

### 5. Feedback Patterns

#### PAT-011: Toast Notifications

**ID**: PAT-011
**Type**: Feedback
**Priority**: P1
**Traces To**: All user actions (copy, favorite, theme change)
**Used In**: All screens

**Trigger**: User completes action (copy, favorite toggle, theme change)

**Behavior**:
1. **Position**: Bottom-right corner (desktop), bottom-center (mobile)
2. **Duration**: 2 seconds (auto-dismiss), dismiss on click
3. **Stacking**: Max 3 toasts, oldest removed first
4. **Types**: Success (green), Error (red), Info (blue), Warning (yellow)
5. **Icon**: Type-specific icon (✅, ❌, ℹ️, ⚠️)

**Visual**:
- **Success**: Green background, white text, checkmark icon
- **Error**: Red background, white text, X icon
- **Info**: Blue background, white text, info icon
- **Warning**: Yellow background, dark text, warning icon

**Animation**:
- Appear: 200ms slide-in from bottom + fade-in
- Dismiss: 150ms fade-out + slide-out
- Hover: Pause auto-dismiss timer

**Examples**:
- "📋 Copied to clipboard" (Success)
- "⭐ Added to Favorites" (Success)
- "❌ Failed to copy" (Error)
- "🌙 Switched to Dark Mode" (Info)

**Accessibility**:
- ARIA live region for screen readers
- Keyboard dismissable (`Esc`)

---

#### PAT-012: Loading States

**ID**: PAT-012
**Type**: Feedback
**Priority**: P1
**Traces To**: JTBD-1.3 (Search), JTBD-1.7 (Tree navigation)
**Used In**: All screens

**Trigger**: Data loading, search in progress

**Behavior**:
1. **Spinner**: Show after 200ms delay (avoid flash for fast operations)
2. **Skeleton screens**: Use for initial page load (tree, detail pane)
3. **Progress indicators**: Linear progress bar for file operations
4. **Inline loading**: Small spinner for in-place updates

**Visual States**:
- **Spinner**: Rotating circle, primary color
- **Skeleton**: Gray placeholder boxes with shimmer animation
- **Progress bar**: Linear bar at top of screen, blue color

**Animation**:
- Spinner: Continuous rotation
- Skeleton: 1.5s shimmer wave (left-to-right gradient)
- Progress bar: Indeterminate slide animation

**Performance**:
- Spinner threshold: 200ms (avoid showing for fast operations)
- Skeleton: Show immediately for initial load

**Accessibility**:
- ARIA `aria-busy="true"` during loading
- Screen reader announcement: "Loading content..."

---

### 5. Responsive Behavior

#### PAT-013: Adaptive Layout

**ID**: PAT-013
**Type**: Responsive
**Priority**: P1
**Traces To**: JTBD-1.1 (Self-service learning across devices)
**Used In**: All screens

**Breakpoints**:
| Device | Width | Layout |
|--------|-------|--------|
| Desktop | > 1024px | Side-by-side panes (300px tree + flexible detail) |
| Tablet | 768-1024px | Collapsible tree panel (hamburger menu) |
| Mobile | < 768px | Stack layout (tree as drawer, swipe to navigate) |

**Desktop (> 1024px)**:
- Tree panel: Fixed 300px width, left side
- Detail pane: Flexible width, right side
- Resizable divider: Drag to adjust widths

**Tablet (768-1024px)**:
- Tree panel: Collapsible drawer (slide from left)
- Hamburger menu icon: Top-left corner
- Detail pane: Full width when tree collapsed
- Overlay: Dark overlay when tree open (tap to close)

**Mobile (< 768px)**:
- Tree drawer: Full-width overlay from left
- Detail view: Full-screen
- Swipe gestures: Swipe right to open tree, swipe left to close
- Bottom navigation: Stage tabs at bottom
- Floating action button: Search (bottom-right)

**Animation**:
- Drawer slide: 300ms ease-in-out
- Panel resize: Instant (no animation)
- Overlay fade: 200ms

**Touch Gestures (Mobile)**:
- Swipe right (from left edge): Open tree drawer
- Swipe left: Close tree drawer
- Pull-to-refresh: Reload content (optional)

---

#### PAT-014: Accessibility Patterns

**ID**: PAT-014
**Type**: Accessibility
**Priority**: P0
**Traces To**: All JTBD (inclusive access)
**Used In**: All screens

**Keyboard Accessibility**:
- All interactive elements keyboard accessible (Tab navigation)
- Visible focus indicators (2px blue outline, AA contrast compliant)
- Logical tab order (follows visual layout)
- Skip-to-content link (first focusable element)

**Screen Reader Support**:
- ARIA labels for icon-only buttons (e.g., "Toggle theme", "Add to favorites")
- ARIA live regions for dynamic content (toast notifications, search results)
- Landmark regions: `<nav>`, `<main>`, `<aside>`
- Heading hierarchy: Proper `<h1>` to `<h6>` nesting

**Color Contrast**:
- Text contrast ratio: Minimum 4.5:1 (AA standard)
- Interactive element contrast: Minimum 3:1 (AA standard)
- Color not sole indicator: Use icons + color for state changes

**Motion Preferences**:
- Respect `prefers-reduced-motion` media query
- Disable animations if user prefers reduced motion
- Fallback to instant transitions

**Font Scaling**:
- Support browser zoom up to 200%
- Responsive font sizes (rem units)
- No horizontal scrolling at 200% zoom

**ARIA Attributes**:
| Element | ARIA Attribute |
|---------|----------------|
| Tree node | `role="treeitem"`, `aria-expanded` |
| Search input | `aria-label="Search framework components"` |
| Loading spinner | `aria-busy="true"`, `aria-live="polite"` |
| Toast notification | `role="status"`, `aria-live="polite"` |
| Theme toggle | `aria-label="Toggle theme"` |

**Client Facts**: CF-003 (Highly visual), CF-014 (Clean, modern, minimalistic)

---

## Interaction Flow Examples

### Flow 1: First-Time User Explores Framework

**Goal**: Understand framework structure (JTBD-1.1, JTBD-1.7)

1. User opens ClaudeManual
2. **PAT-001**: Tree shows top-level categories (Skills, Commands, Agents)
3. User clicks "Skills" category → expands to show stage subcategories
4. **PAT-002**: User clicks "Discovery" tab → filters to Discovery skills only
5. **PAT-001**: User clicks "Discovery_JTBD" skill → detail pane loads
6. **PAT-012**: Skeleton screen during load → content appears
7. User reads purpose, examples, workflow diagram
8. **PAT-009**: User clicks "Copy Path" → toast notification "📋 Copied to clipboard"
9. User opens IDE and edits `.claude/skills/Discovery_JTBD/SKILL.md`

**Success Metrics**:
- Time to first skill exploration: < 1 minute
- User understands hierarchy: Yes (measured by post-session survey)
- Copy path success rate: > 95%

---

### Flow 2: Developer Searches for Specific Tool

**Goal**: Find tool for JTBD extraction (JTBD-1.3)

1. User presses `/` → search bar focused
2. **PAT-005**: User types "jtbd" → search debounces 150ms
3. **PAT-012**: Spinner shows during search
4. **PAT-005**: Results dropdown shows 3 matches: Discovery_JTBD, ProductSpecs_JTBDMapping, Discovery_JTBD_Audit
5. User presses `↓` twice → highlights "Discovery_JTBD"
6. User presses `Enter` → detail view loads
7. **PAT-008**: User presses `f` → adds to favorites, star icon fills
8. **PAT-011**: Toast notification "⭐ Added to Favorites"

**Success Metrics**:
- Search to selection time: < 10 seconds
- Search success rate: > 90%
- Favorite toggle success: > 95%

---

### Flow 3: User Compares Two Commands

**Goal**: Decide between `/discovery` and `/discovery-multiagent` (JTBD-1.8)

1. User navigates to `/discovery` command detail
2. **PAT-007**: User clicks "Compare with..." button
3. Dropdown shows related commands: `/discovery-multiagent`, `/discovery-resume`
4. User selects `/discovery-multiagent`
5. **PAT-007**: Screen splits 50/50 → synchronized scrolling enabled
6. User reads "Use /discovery for single-threaded, /discovery-multiagent for 60% faster parallel"
7. User decides on `/discovery-multiagent` based on performance
8. User presses `Esc` → exits comparison mode

**Success Metrics**:
- Comparison decision time: < 2 minutes
- Decision confidence: > 80% (measured by survey)

---

## Performance Benchmarks

| Interaction | Target Performance | Measurement |
|-------------|-------------------|-------------|
| Tree expand/collapse | 200ms animation | Visual smoothness |
| Search results | < 200ms | Time from last keystroke to results |
| Tree rendering (115 items) | < 100ms | Initial load time |
| Detail pane load | < 500ms | Markdown parsing + rendering |
| Copy to clipboard | < 10ms | Clipboard API execution |
| Theme toggle | < 50ms | CSS variable update |
| Toast notification | 200ms appear | Animation duration |
| Filter apply | < 50ms | Result filtering operation |
| Navigation transition | 300ms | Panel slide animation |

---

## Micro-Interactions Reference

| Interaction | Duration | Easing | Effect |
|-------------|----------|--------|--------|
| Button hover | 150ms | ease | Background color change |
| Tree expand | 200ms | ease-out | Rotate chevron, slide-down children |
| Selection highlight | 150ms | ease | Background color transition |
| Toast appear | 200ms | ease-out | Slide-in + fade-in |
| Toast dismiss | 150ms | ease-in | Fade-out + slide-out |
| Panel transition | 300ms | ease-in-out | Drawer slide |
| Star pulse (favorite) | 200ms | ease-out | Scale 1.1x + fill color |
| Icon swap (copy → check) | 150ms | ease | Fade transition |
| Breadcrumb transition | 100ms | ease | Fade |
| Skeleton shimmer | 1.5s | linear | Left-to-right gradient wave |

---

## Accessibility Compliance

**WCAG 2.1 AA Compliance**:
- ✅ **1.4.3 Contrast (Minimum)**: Text contrast ratio ≥ 4.5:1
- ✅ **2.1.1 Keyboard**: All functionality keyboard accessible
- ✅ **2.4.7 Focus Visible**: Focus indicators always visible
- ✅ **3.2.4 Consistent Identification**: Icons and labels consistent
- ✅ **4.1.2 Name, Role, Value**: ARIA attributes on dynamic elements

**Screen Reader Testing**:
- Test with NVDA (Windows), VoiceOver (macOS), TalkBack (Android)
- All interactive elements announced correctly
- Live regions announce state changes (toast notifications, search results)

**Keyboard Navigation Testing**:
- All shortcuts documented in help modal (`?` key)
- No keyboard traps (can exit all modals and dropdowns)
- Logical tab order (matches visual hierarchy)

---

## Design System Integration

**Color Tokens** (reference to Design System):
- Primary: `--color-primary` (blue)
- Success: `--color-success` (green)
- Error: `--color-error` (red)
- Warning: `--color-warning` (yellow)
- Background: `--color-bg-primary`, `--color-bg-secondary`
- Text: `--color-text-primary`, `--color-text-secondary`
- Border: `--color-border-default`, `--color-border-focus`

**Spacing** (reference to Design System):
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px

**Typography** (reference to Design System):
- Font family: Monospace (terminal-inspired, CF-014)
- Font sizes: 12px (caption), 14px (body), 16px (heading-3), 20px (heading-2), 24px (heading-1)

**Animation Tokens** (reference to Design System):
- Duration fast: 100ms
- Duration normal: 150-200ms
- Duration slow: 300ms
- Easing: ease, ease-in, ease-out, ease-in-out

---

## Validation Checklist

✅ **All patterns trace to JTBD or Client Facts**
✅ **Keyboard accessibility for all interactions**
✅ **Performance targets defined**
✅ **Animation durations specified**
✅ **Visual states documented**
✅ **ARIA attributes specified**
✅ **Responsive behavior defined**
✅ **Client Facts integrated**: CF-003, CF-006, CF-007, CF-009, CF-012, CF-013, CF-016

---

## Traceability

**Source Material**:
- JTBD: ClientAnalysis_ClaudeManual/02-research/JOBS_TO_BE_DONE.md
- Client Facts: traceability/client_facts_registry.json (CM-001)

**Pattern Coverage**:
- **JTBD-1.1** (Self-Service Learning): PAT-001, PAT-004, PAT-013
- **JTBD-1.2** (Component Context): PAT-007
- **JTBD-1.3** (Quick Tool Discovery): PAT-005, PAT-006
- **JTBD-1.4** (Stage Filtering): PAT-002, PAT-006
- **JTBD-1.5** (Edit Source Files): PAT-009
- **JTBD-1.6** (Bookmark Favorites): PAT-008
- **JTBD-1.7** (Visual Hierarchy): PAT-001, PAT-003, PAT-004
- **JTBD-1.8** (Component Comparison): PAT-007

**Client Facts Coverage**:
- **CF-003** (Highly Visual): All patterns support visual clarity
- **CF-006** (Master-Detail Panes): PAT-001 (Tree navigation)
- **CF-007** (Click to Open): PAT-001 (Tree selection)
- **CF-009** (Search Page): PAT-005 (Instant Search)
- **CF-012** (Favorites): PAT-008 (Favorites Management)
- **CF-013** (File Path Reference): PAT-009 (Copy Path)
- **CF-016** (Light/Dark Theme): PAT-010 (Theme Toggle)

**Checkpoint**: CP-9
**Session**: disc-claude-manual-009d
**Created By**: discovery-interaction-specifier
**Date**: 2026-01-31

---

*14 interaction patterns across 5 categories. 100% JTBD coverage. WCAG 2.1 AA compliant.*
