# DiagramViewer

**ID**: COMP-AGG-007
**Category**: Visualizations
**Priority**: P1

## Overview

Interactive diagram viewer with zoom/pan controls for Mermaid and PlantUML diagrams. Combines Adobe Spectrum's View and Toolbar with Mermaid rendering library.

## Props Interface

```typescript
interface DiagramViewerProps {
  /** Diagram code */
  code: string;
  /** Diagram format */
  format: 'mermaid' | 'plantuml';
  /** Initial zoom level */
  initialZoom?: number;
  /** Export handler */
  onExport?: (format: 'png' | 'svg' | 'pdf') => void;
}
```

## Library Components Used

- **View** (Spectrum): Canvas container
- **Button** (Spectrum): Zoom controls, export
- **Toolbar** (Spectrum): Control buttons
- **Slider** (Spectrum): Zoom slider

## Business Logic

### Mermaid Rendering
```typescript
import mermaid from 'mermaid';

async function renderMermaid(code: string): Promise<string> {
  const { svg } = await mermaid.render('diagram-' + Date.now(), code);
  return svg;
}
```

## Usage Examples

```tsx
<DiagramViewer
  code={mermaidCode}
  format="mermaid"
  initialZoom={1.0}
  onExport={(format) => exportDiagram(format)}
/>
```

## Screen Usage

| Screen | Context |
|--------|---------|
| SCR-009 Workflow Viewer | Workflow diagrams |
| SCR-010 Architecture Browser | C4 diagrams |
| SCR-011 Document Preview Modal | Full-screen diagrams |

---

**Traceability**: JTBD-1.9 (Visualize diagrams), CF-008 (Multi-section documentation)
