# Workflow Viewer

**ID**: SCR-009
**Discovery ID**: S-9.0
**Application**: Web
**Priority**: P1
**Primary Persona**: All personas

## Overview

The Workflow Viewer screen provides an interactive interface for viewing and exploring workflow diagrams (Mermaid, PlantUML) with zoom, pan, and export controls. Users can visualize process flows, navigate between related workflows, and export diagrams for presentations and documentation.

## Layout

### Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  [Logo]              Search [___________] [🔔] [👤]                          │ <- Header
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [← Back to Explorer]   Workflow: Discovery Process Flow                     │
│                         [Mermaid] [Discovery] ⭐                             │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                        │ │
│  │                      ┌─────────────┐                                   │ │
│  │                      │   Start     │                                   │ │
│  │                      └──────┬──────┘                                   │ │
│  │                             │                                          │ │
│  │                      ┌──────▼──────┐                                   │ │
│  │                      │ Input Files │                                   │ │
│  │                      └──────┬──────┘                                   │ │
│  │                             │                                          │ │
│  │              ┌──────────────┼──────────────┐                           │ │
│  │              │              │              │                           │ │
│  │       ┌──────▼──────┐ ┌─────▼─────┐ ┌─────▼─────┐                     │ │
│  │       │ Pain Points │ │  JTBDs    │ │ Personas  │                     │ │
│  │       └─────────────┘ └───────────┘ └───────────┘                     │ │
│  │                                                                        │ │
│  │                                                                        │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │ [−] [100%] [+]  [Reset]  [Export ▾]       [Minimap ☐]           │ │ │
│  │  └──────────────────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ## Description                                                              │
│  This workflow shows the Discovery phase process flow from client            │
│  materials input through to deliverable generation.                          │
│                                                                              │
│  ## Related Workflows                                                        │
│  [Prototype Process] [ProductSpecs Flow] [Implementation Cycle]              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Grid Structure

| Region | Grid Columns | Components |
|--------|--------------|------------|
| Header | 1-12 | AppHeader |
| Toolbar | 1-12 | BackButton, WorkflowHeader, FavoriteToggle |
| Diagram Canvas | 1-12 | DiagramViewer (COMP-AGG-007) |
| Controls | 1-12 | ZoomControls, ExportDropdown, MinimapToggle |
| Description | 1-12 | MarkdownRenderer (COMP-AGG-008) |
| Related | 1-12 | RelatedLinks |

## Components Used

| Component | Instance | Props |
|-----------|----------|-------|
| COMP-AGG-007 | DiagramViewer | `format="mermaid"`, `initialZoom={100}`, `enablePan={true}` |
| COMP-AGG-008 | MarkdownRenderer | `content={description}` |
| Button (Spectrum) | BackButton | `variant="secondary"`, icon="ArrowLeft" |
| Button (Spectrum) | FavoriteToggle | `variant="action"`, icon="Star" |
| Badge (Spectrum) | FormatBadge | `variant="neutral"` |
| Badge (Spectrum) | StageBadge | `variant="info"` |
| Toolbar (Spectrum) | ZoomControls | `orientation="horizontal"` |
| Button (Spectrum) | ZoomOutButton | `variant="secondary"`, icon="Minus" |
| Button (Spectrum) | ZoomInButton | `variant="secondary"`, icon="Plus" |
| Button (Spectrum) | ResetButton | `variant="secondary"` |
| Slider (Spectrum) | ZoomSlider | `minValue={25}`, `maxValue={200}`, `step={25}` |
| MenuTrigger (Spectrum) | ExportDropdown | - |
| Menu (Spectrum) | ExportMenu | items: PNG, SVG, PDF |
| Switch (Spectrum) | MinimapToggle | label="Minimap" |
| Link (Spectrum) | RelatedLink | `variant="secondary"` |

## Data Requirements

### Page Load Data

| Field | Source | Type | Required |
|-------|--------|------|----------|
| workflow | GET /api/workflows/:id | Workflow | Yes |
| diagram | workflow.content.diagram | string | Yes |
| format | workflow.format | enum | Yes |
| stage | workflow.stage | enum | No |
| relatedWorkflows | GET /api/workflows?related=:id | Workflow[] | No |

### User Input Data

| Field | Component | Validation |
|-------|-----------|------------|
| zoom | ZoomSlider | number: 25-200 |
| pan | DiagramViewer | { x: number, y: number } |
| minimapEnabled | MinimapToggle | boolean |
| exportFormat | ExportDropdown | enum: PNG, SVG, PDF |

## State Management

### Local State

```typescript
interface WorkflowViewerState {
  workflow: Workflow | null;
  loading: boolean;
  error: string | null;

  // Diagram state
  zoom: number; // 25-200
  pan: { x: number; y: number };
  minimapEnabled: boolean;
  diagramSvg: string | null;

  // Related workflows
  relatedWorkflows: Workflow[];
  relatedLoading: boolean;

  // Export
  exportInProgress: boolean;
  exportFormat: 'png' | 'svg' | 'pdf';
}
```

### Global State Dependencies

| Store | Slice | Usage |
|-------|-------|-------|
| user | preferences | Favorite workflows, theme |
| ui | sidebarCollapsed | Layout adjustment |

## Navigation

### Entry Points

| From | Trigger | Params |
|------|---------|--------|
| Main Explorer (SCR-001) | Click workflow in tree | `workflowId` |
| Search Results (SCR-002) | Click workflow result | `workflowId` |
| Architecture Browser (SCR-010) | Click workflow diagram | `workflowId` |
| Related Links | Click related workflow | `workflowId` |
| Deep Link | URL | `/workflows/:workflowId` |

### Exit Points

| To | Trigger | Data Passed |
|----|---------|-------------|
| Main Explorer (SCR-001) | Back button | - |
| Another Workflow Viewer | Click related workflow | `workflowId` |
| Document Preview Modal (SCR-011) | Expand diagram | `workflowId` |

## Interactions

### User Actions

| Action | Component | Handler | Result |
|--------|-----------|---------|--------|
| Zoom In | ZoomInButton | onZoomIn | Increase zoom by 25% |
| Zoom Out | ZoomOutButton | onZoomOut | Decrease zoom by 25% |
| Zoom Slider | ZoomSlider | onChange | Set zoom to value |
| Reset Zoom | ResetButton | onReset | Reset to 100% zoom, center diagram |
| Pan Diagram | DiagramViewer | onPan | Update pan coordinates |
| Toggle Minimap | MinimapToggle | onChange | Show/hide minimap |
| Export | ExportMenu | onAction | Download diagram as selected format |
| Add to Favorites | FavoriteToggle | onClick | Toggle favorite status |
| View Related | RelatedLink | onClick | Navigate to related workflow |

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `+` | Zoom in |
| `-` | Zoom out |
| `0` | Reset zoom |
| `Space` + drag | Pan diagram |
| `F` | Toggle fullscreen (Document Preview Modal) |
| `Esc` | Back to Explorer |

### Gesture Support (Mobile)

| Gesture | Action |
|---------|--------|
| Pinch | Zoom in/out |
| Two-finger drag | Pan diagram |
| Double-tap | Reset zoom |

## Responsive Behavior

| Breakpoint | Changes |
|------------|---------|
| Desktop (>1024px) | Full layout with side description |
| Tablet (768-1024px) | Stack description below diagram |
| Mobile (<768px) | Simplified controls, bottom toolbar, touch gestures |

## Accessibility

- **Page Title**: "Workflow: {workflow.name} - ClaudeManual"
- **Landmarks**: `header`, `main`, `navigation` (related links)
- **Skip Link**: Skip to diagram
- **Focus Management**: Focus diagram canvas on load
- **Announcements**:
  - "Diagram loaded: {workflow.name}"
  - "Zoom level: {zoom}%"
  - "Exporting as {format}..."
- **SVG Accessibility**:
  - `<title>` and `<desc>` elements for diagram
  - ARIA labels for interactive nodes
- **Keyboard Navigation**: Full keyboard control for all zoom/pan operations

## Error States

| State | Display | Recovery |
|-------|---------|----------|
| Workflow Not Found | ErrorMessage + BackButton | Navigate to Explorer |
| Diagram Rendering Error | Code block with diagram source + error message | Show raw diagram code |
| Export Failure | Toast notification with error | Retry button |
| Related Workflows Load Error | Empty related section | Silent fail, no blocking |

## Performance Considerations

| Metric | Target | Strategy |
|--------|--------|----------|
| Diagram Render | < 2s | Lazy load Mermaid/PlantUML libraries |
| Zoom Transition | 60fps | CSS transforms with GPU acceleration |
| Pan Performance | 60fps | RequestAnimationFrame for smooth panning |
| Export Generation | < 5s | Web Worker for export processing |

## Mermaid Integration

### Supported Diagram Types

- Flowchart (`graph TD`, `graph LR`)
- Sequence Diagram (`sequenceDiagram`)
- Class Diagram (`classDiagram`)
- State Diagram (`stateDiagram`)
- Entity Relationship (`erDiagram`)
- Gantt Chart (`gantt`)
- Journey (`journey`)

### Configuration

```typescript
const mermaidConfig = {
  theme: theme === 'dark' ? 'dark' : 'default',
  themeVariables: {
    primaryColor: '#3b82f6',
    primaryTextColor: '#fff',
    primaryBorderColor: '#2563eb',
    lineColor: '#6b7280',
    secondaryColor: '#22c55e',
    tertiaryColor: '#a855f7',
  },
  flowchart: {
    htmlLabels: true,
    curve: 'basis',
  },
  securityLevel: 'strict',
};
```

## PlantUML Integration

### Rendering Strategy

- Use Kroki service (`https://kroki.io`) for PlantUML rendering
- Fallback to embedded PlantUML encoder if Kroki unavailable
- Cache rendered SVGs in localStorage

### Supported Diagram Types

- Sequence Diagram
- Use Case Diagram
- Class Diagram
- Activity Diagram
- Component Diagram
- Deployment Diagram
- State Diagram
- C4 Context/Container/Component diagrams

## Export Formats

### PNG Export

```typescript
async function exportPNG(svgElement: SVGElement): Promise<Blob> {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  const svgData = new XMLSerializer().serializeToString(svgElement);
  const img = new Image();

  img.onload = () => {
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
    canvas.toBlob((blob) => {
      // Download blob
    }, 'image/png');
  };

  img.src = 'data:image/svg+xml;base64,' + btoa(svgData);
}
```

### SVG Export

- Direct download of rendered SVG element
- Preserve theme colors and styles
- Embed fonts for offline viewing

### PDF Export

- Use `jsPDF` library with SVG plugin
- A4 landscape orientation
- Auto-scale diagram to fit page
- Include workflow name as header

## Testing Scenarios

### Visual Regression Tests

1. Mermaid flowchart renders correctly
2. PlantUML sequence diagram renders correctly
3. Zoom controls update diagram size
4. Pan gesture moves diagram
5. Minimap shows correct viewport position
6. Export generates valid file

### Accessibility Tests

1. Screen reader announces diagram title
2. Keyboard navigation works for all controls
3. Focus indicators visible
4. Color contrast meets WCAG AA

### Performance Tests

1. Large diagram (100+ nodes) renders in < 5s
2. Zoom transition maintains 60fps
3. Export completes in < 5s
4. Memory usage stays under 100MB

---

## Traceability

**Addresses Pain Points**: PP-1.2 (Lack of Contextual Documentation)

**Enables JTBD**: JTBD-1.9 (Visualize Process and Architecture Diagrams), JTBD-1.2 (Component Context)

**Client Facts**: CF-001 (Markdown-based structure), CF-008 (Multi-section documentation)

**Roadmap Features**: F-NEW-01 (Workflow Visualization)

**Discovery ID**: S-9.0

**Requirements**: REQ-026 (Workflow visualization support)

---

**Generated**: 2026-01-31
**Agent**: prototype-screen-specifier
**Session**: session-screen-scr009
**Status**: COMPLETE
