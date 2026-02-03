# Architecture Browser

**ID**: SCR-010
**Discovery ID**: S-10 (derived from screen-definitions.md)
**Application**: Web
**Priority**: P1
**Primary Persona**: All personas (framework users, developers, architects)

## Overview

The Architecture Browser enables users to navigate and view architecture documentation including C4 diagrams and ADRs (Architecture Decision Records). It provides a dual-pane interface with category navigation on the left and diagram/document viewer on the right, supporting Mermaid and PlantUML rendering with zoom/pan controls.

**Purpose**: Help developers understand system architecture before implementation by providing visual context through diagrams and decision rationale through ADRs.

**Traceability**: JTBD-1.9 (Visualize Architecture), JTBD-1.2 (Component Context), JTBD-2.1 (Confidence)

---

## Layout

### Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  [Logo]              Search [___________] [🔔] [👤]        │ <- Header
├──────────────────────────────────────┬───────────────────────────────────────┤
│                                      │                                       │
│ Architecture                         │ Context Diagram - ClaudeManual        │
│ ────────────────────────────────────│ ──────────────────────────────────── │
│                                      │                                       │
│ ▼ C4 Diagrams (4)           [i]      │ [C4] [Context] [Mermaid]              │
│   ├ Context Diagram         ←        │                                       │
│   ├ Container Diagram                │ ┌──────────────────────────────────┐ │
│   ├ Component Diagram                │ │                                  │ │
│   └ Code Diagram                     │ │      [Person]                    │ │
│                                      │ │     Framework                    │ │
│ ▼ ADRs (12)                 [i]      │ │      User                        │ │
│   ├ ADR-001: Architecture Style      │ │        │                         │ │
│   ├ ADR-002: Data Storage            │ │        ▼                         │ │
│   ├ ADR-003: API Design              │ │ ┌─────────────┐                  │ │
│   └ ...                              │ │ │ClaudeManual │                  │ │
│                                      │ │ │   System    │                  │ │
│ ▼ Patterns (8)              [i]      │ │ └─────────────┘                  │ │
│   ├ Repository Pattern               │ │                                  │ │
│   ├ Event Sourcing                   │ │                                  │ │
│   └ ...                              │ └──────────────────────────────────┘ │
│                                      │                                       │
│ ▼ Infrastructure (3)        [i]      │ ## Context                            │
│   ├ Deployment Diagram               │ Shows ClaudeManual system in context │
│   ├ Network Topology                 │ with external actors and systems.    │
│   └ ...                              │                                       │
│                                      │ ## Related                            │
│                                      │ [Container Diagram] [ADR-001]        │
│                                      │                                       │
│ [Collapse All] [Expand All]          │ [Copy Path] [Export]                 │
│                                      │                                       │
└──────────────────────────────────────┴───────────────────────────────────────┘
```

### Grid Structure

| Region | Grid Columns | Components |
|--------|--------------|------------|
| Header | 1-12 | AppHeader (not defined in aggregate components) |
| Sidebar | 1-3 | NavigationTree (COMP-AGG-001) |
| Main | 4-12 | DiagramViewer (COMP-AGG-007), MarkdownRenderer (COMP-AGG-008) |

---

## Components Used

| Component | Instance | Props | Library Components Used |
|-----------|----------|-------|-------------------------|
| COMP-AGG-001 | NavigationTree | `data={architectureCategories}`, `onSelect={handleSelect}` | Tree, Badge, Tooltip, TextField |
| COMP-AGG-007 | DiagramViewer | `format={format}`, `content={diagramContent}`, `zoom={true}` | View, Button, Toolbar, Slider |
| COMP-AGG-008 | MarkdownRenderer | `content={markdownContent}`, `enableMermaid={true}` | View, Heading, Text, Link |

### Library Components (Adobe Spectrum React)

- **Tree**: Hierarchical category navigation
- **Badge**: C4 level badges (Context/Container/Component/Code), ADR status badges (Proposed/Accepted/Deprecated/Superseded)
- **Tooltip**: Category descriptions on hover
- **View**: Container for diagram and markdown content
- **Button**: Copy Path, Export actions
- **Toolbar**: Diagram controls (zoom, pan, export)
- **Slider**: Zoom slider control
- **Heading**: Section headings in markdown
- **Text**: Markdown body text
- **Link**: Related document links

---

## Data Requirements

### Page Load Data

| Field | Source | Type | Required | Description |
|-------|--------|------|----------|-------------|
| architectureDocs | GET /api/architecture-docs | ArchitectureDoc[] | Yes | All architecture documents (C4, ADRs, patterns) |
| user | Session | User | Yes | Current user for permissions |

### Architecture Document Entity (from DATA_MODEL.md)

```typescript
interface ArchitectureDoc {
  id: string;
  name: string;
  description: string;
  format: 'md' | 'mermaid' | 'plantuml';
  path: string;
  category?: 'c4' | 'adr' | 'patterns' | 'infrastructure' | 'data-model';
  c4_level?: 'context' | 'container' | 'component' | 'code';
  adr_status?: 'proposed' | 'accepted' | 'deprecated' | 'superseded';
  tags?: string[];
  related_adrs?: string[];
  content?: {
    overview: string;
    diagram?: string;
    context?: string;
    decision?: string;
    consequences?: string;
    related?: string;
  };
}
```

### API Endpoints

| Endpoint | Method | Description | Request | Response |
|----------|--------|-------------|---------|----------|
| /api/architecture-docs | GET | List all architecture documents | `ListArchitectureDocsRequest` | `ArchitectureDocListResponse` |
| /api/architecture-docs/:id | GET | Get document details | - | `ArchitectureDoc` |

### Request/Response Types (from DATA_MODEL.md)

```typescript
interface ListArchitectureDocsRequest {
  category?: string[];
  c4_level?: string[];
  adr_status?: string[];
  format?: string[];
  search?: string;
  page?: number;
  pageSize?: number;
}

interface ArchitectureDocListResponse {
  data: ArchitectureDoc[];
  pagination: {
    page: number;
    pageSize: number;
    totalItems: number;
    totalPages: number;
  };
}
```

---

## State Management

### Local State

```typescript
interface ArchitectureBrowserState {
  categories: {
    c4: ArchitectureDoc[];
    adrs: ArchitectureDoc[];
    patterns: ArchitectureDoc[];
    infrastructure: ArchitectureDoc[];
  };
  selectedDoc: ArchitectureDoc | null;
  loading: boolean;
  error: string | null;
  zoomLevel: number;
  expandedCategories: string[];
}

const initialState: ArchitectureBrowserState = {
  categories: { c4: [], adrs: [], patterns: [], infrastructure: [] },
  selectedDoc: null,
  loading: true,
  error: null,
  zoomLevel: 100,
  expandedCategories: ['c4', 'adrs'],
};
```

### Global State Dependencies

| Store | Slice | Usage |
|-------|-------|-------|
| auth | user | Display user info |
| ui | sidebarCollapsed | Sidebar state |

---

## Navigation

### Entry Points

| From | Trigger | Params |
|------|---------|--------|
| Main Explorer (SCR-001) | Click "Architecture" in navigation tree | - |
| Search Results (SCR-002) | Click architecture document result | `docId` |
| Deep Link | URL | `?category=c4&doc=context-diagram` |

### Exit Points

| To | Trigger | Data Passed |
|----|---------|-------------|
| Main Explorer (SCR-001) | "Back to Explorer" button | - |
| Workflow Viewer (SCR-009) | Click related workflow link | `workflowId` |
| Document Preview Modal (SCR-011) | "Expand" button on diagram | `docId` |

---

## Interactions

### User Actions

| Action | Component | Handler | Result |
|--------|-----------|---------|--------|
| Select Category | NavigationTree | onCategorySelect | Expand/collapse category |
| Select Document | NavigationTree | onDocumentSelect | Load document in viewer |
| Zoom In | DiagramViewer toolbar | onZoomIn | Increase zoom by 25% |
| Zoom Out | DiagramViewer toolbar | onZoomOut | Decrease zoom by 25% |
| Reset Zoom | DiagramViewer toolbar | onResetZoom | Reset to 100% |
| Export | DiagramViewer toolbar | onExport | Download PNG/SVG/PDF |
| Copy Path | Button | onCopyPath | Copy file path to clipboard |
| Click Related ADR | Link | onRelatedClick | Navigate to related ADR |

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Arrow Up/Down` | Navigate tree items |
| `Enter` | Select document |
| `+` | Zoom in |
| `-` | Zoom out |
| `0` | Reset zoom |
| `Esc` | Close modal (if in preview mode) |

---

## Responsive Behavior

| Breakpoint | Changes |
|------------|---------|
| Desktop (>1024px) | Full dual-pane layout |
| Tablet (768-1024px) | Collapsible sidebar, full-width viewer |
| Mobile (<768px) | Bottom sheet navigation, stacked layout |

---

## Accessibility

- **Page Title**: "Architecture Browser - ClaudeManual"
- **Landmarks**: `<nav>` for category tree, `<main>` for viewer
- **Skip Link**: Skip to diagram viewer
- **Focus Management**: Focus first category on load
- **Announcements**: "Document loaded: {name}", "Zoom level: {level}%"
- **ARIA Labels**:
  - Tree: `aria-label="Architecture categories"`
  - Diagram: `aria-label="Architecture diagram"`
  - Toolbar: `aria-label="Diagram controls"`

---

## Error States

| State | Display | Recovery |
|-------|---------|----------|
| Load Error | ErrorBanner + Retry | Retry button |
| Empty Category | EmptyState with illustration | "No documents in this category" |
| Render Error (Mermaid/PlantUML) | Show code block with error message | "Copy Code" button for debugging |
| Missing Document | 404 message | "Back to Architecture" button |

---

## UX Psychology Applied

| Principle | Application | User Benefit |
|-----------|-------------|--------------|
| **Cognitive Load Reduction** | Category tree organizes by type (C4, ADRs, Patterns) | Users find documents faster (JTBD-1.7) |
| **Visual Learning** | Diagrams communicate architecture at a glance | Faster comprehension than text-only docs (JTBD-1.9) |
| **Progressive Disclosure** | Collapsed categories by default, expand on demand | Users explore at their own pace (JTBD-2.2) |
| **Decision Context** | ADR status badges show current state immediately | Developers know which decisions are active (JTBD-2.1) |

---

## Traceability

- **Addresses Pain Points**: PP-1.2 (Lack of Contextual Documentation)
- **Enables JTBD**: JTBD-1.9 (Visualize Architecture), JTBD-1.2 (Component Context), JTBD-2.1 (Confidence)
- **Client Facts**: CF-001 (File system integration), CF-008 (Multi-section documentation)
- **Roadmap Features**: F-NEW-02 (Architecture Documentation), F-018 (Workflow diagrams)
- **Data Model**: ENT-009 (ArchitectureDoc)

---

**Created**: 2026-01-31
**Session**: session-screen-scr010
**Agent**: prototype-screen-specifier
**Assembly-First**: true
