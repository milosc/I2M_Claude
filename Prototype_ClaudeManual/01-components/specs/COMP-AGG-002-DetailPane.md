# DetailPane

**ID**: COMP-AGG-002
**Category**: Content Display
**Priority**: P0

## Overview

Tabbed documentation viewer that displays framework component details with markdown rendering, code syntax highlighting, and workflow diagrams. Combines Adobe Spectrum's Tabs component with ClaudeManual-specific documentation structure.

## Props Interface

```typescript
interface DetailPaneProps {
  /** Selected item data */
  item: ComponentDetail | null;
  /** Loading state */
  loading?: boolean;
  /** Error state */
  error?: string;
  /** Active tab */
  activeTab?: TabId;
  /** Tab change handler */
  onTabChange?: (tabId: TabId) => void;
  /** Copy path handler */
  onCopyPath?: (path: string) => void;
  /** Favorite toggle handler */
  onToggleFavorite?: (itemId: string) => void;
  /** Show/hide specific tabs */
  visibleTabs?: TabId[];
}

interface ComponentDetail {
  id: string;
  name: string;
  type: 'skill' | 'command' | 'agent' | 'rule' | 'hook';
  stage: Stage;
  path: string;
  description: string;
  purpose?: string;
  examples?: CodeExample[];
  options?: OptionField[];
  workflow?: WorkflowDiagram;
  traceability?: TraceabilityLink[];
  tags?: string[];  // PF-002: User-defined tags for categorization
  isFavorite: boolean;
}

type TabId = 'purpose' | 'examples' | 'options' | 'workflow' | 'traceability';

interface CodeExample {
  title: string;
  language: 'bash' | 'typescript' | 'json' | 'yaml';
  code: string;
}

interface OptionField {
  parameter: string;
  type: string;
  required: boolean;
  defaultValue?: string;
  description: string;
}

interface WorkflowDiagram {
  format: 'mermaid' | 'plantuml';
  code: string;
  description?: string;
}

interface TraceabilityLink {
  type: 'input' | 'output' | 'dependency' | 'related';
  id: string;
  label: string;
}
```

## Variants

| Variant | Use Case | Visible Tabs |
|---------|----------|--------------|
| Skill | Skill documentation | Purpose, Examples, Options, Workflow, Traceability |
| Command | Command documentation | Purpose, Examples, Options, Workflow |
| Agent | Agent documentation | Purpose, Examples, Workflow |
| Rule | Rule documentation | Purpose, Examples |
| Minimal | Quick reference | Purpose only |

## Library Components Used

### Primary Component
- **Tabs** (Spectrum): Tabbed interface for organizing documentation sections
  - Props: `selectedKey`, `onSelectionChange`, `density="compact"`
  - TabList: Tab labels (Purpose, Examples, etc.)
  - TabPanels: Tab content areas

### Supporting Components
- **View** (Spectrum): Layout container for tab content
  - Props: `padding="size-300"`, `overflow="auto"`
- **Heading** (Spectrum): Section headings within tabs
  - Props: `level={2}`, `marginBottom="size-200"`
- **Link** (Spectrum): Hyperlinks for paths and traceability
  - Props: `variant="secondary"`, `onPress`
- **Button** (Spectrum): Copy Path, Add to Favorites actions
  - Props: `variant="primary"`, `size="M"`, `onPress`

## States

| State | Condition | Visual Behavior | Token Mapping |
|-------|-----------|----------------|---------------|
| Empty | No item selected | "Select a component to view details" placeholder | `color.text.light.tertiary` |
| Loading | Fetching content | Skeleton loader for tabs and content | `color.primitive.gray.200` |
| Success | Content loaded | Tabs active, markdown rendered | - |
| Error | Fetch failure | Error message with retry button | `color.semantic.light.error` |
| Tab Active | User clicked tab | Tab underlined, content visible | `color.semantic.light.primary` |
| Tab Inactive | Other tabs | Tab gray, content hidden | `color.text.light.secondary` |

## Design Token Mapping

| Property | Token Path | Value (Light) |
|----------|------------|---------------|
| Background | `color.background.light.primary` | `#ffffff` |
| Tab Underline (Active) | `color.semantic.light.primary` | `color.primitive.blue.500` |
| Tab Text (Active) | `color.text.light.primary` | `color.primitive.gray.900` |
| Tab Text (Inactive) | `color.text.light.secondary` | `color.primitive.gray.600` |
| Heading Color | `color.text.light.primary` | `color.primitive.gray.900` |
| Link Color | `color.text.light.link` | `color.primitive.blue.600` |
| Link Hover | `color.text.light.link-hover` | `color.primitive.blue.700` |
| Code Block Background | `color.background.light.tertiary` | `color.primitive.gray.100` |
| Font Family (Headings) | `typography.fontFamily.mono` | JetBrains Mono |
| Font Family (Body) | `typography.fontFamily.sans` | Inter |
| Font Size (Heading) | `typography.fontSize.xl` | 1.25rem (20px) |
| Font Size (Body) | `typography.fontSize.base` | 1rem (16px) |
| Padding | `spacing.6` | 1.5rem (24px) |
| Border Radius | `borderRadius.md` | 0.375rem (6px) |
| Transition | `motion.duration.normal` | 200ms |

## Business Logic

### Tab Visibility Logic
```typescript
function getVisibleTabs(item: ComponentDetail): TabId[] {
  const baseTabs: TabId[] = ['purpose'];

  if (item.examples?.length > 0) {
    baseTabs.push('examples');
  }

  if (item.options?.length > 0) {
    baseTabs.push('options');
  }

  if (item.workflow) {
    baseTabs.push('workflow');
  }

  if (item.traceability?.length > 0 && item.type === 'skill') {
    baseTabs.push('traceability');
  }

  return baseTabs;
}
```

### Markdown Rendering with Mermaid
```typescript
import { marked } from 'marked';
import mermaid from 'mermaid';

async function renderMarkdownWithDiagrams(markdown: string): Promise<string> {
  // Configure marked for syntax highlighting
  marked.setOptions({
    highlight: (code, lang) => {
      return highlightCode(code, lang);
    }
  });

  let html = marked(markdown);

  // Render Mermaid diagrams
  const mermaidBlocks = html.match(/<code class="language-mermaid">(.*?)<\/code>/gs);

  if (mermaidBlocks) {
    for (const block of mermaidBlocks) {
      const code = block.replace(/<code class="language-mermaid">|<\/code>/g, '');
      const { svg } = await mermaid.render('mermaid-' + Date.now(), code);
      html = html.replace(block, svg);
    }
  }

  return html;
}
```

### Copy Path to Clipboard
```typescript
async function copyPathToClipboard(path: string): Promise<void> {
  try {
    await navigator.clipboard.writeText(path);

    // Show success toast
    showToast({
      variant: 'success',
      message: 'Path copied to clipboard',
      duration: 2000
    });
  } catch (error) {
    showToast({
      variant: 'error',
      message: 'Failed to copy path',
      duration: 3000
    });
  }
}
```

## Usage Examples

### Basic Detail Pane
```tsx
import { DetailPane } from '@/components/DetailPane';

<DetailPane
  item={selectedItem}
  onCopyPath={(path) => copyPathToClipboard(path)}
  onToggleFavorite={(itemId) => handleToggleFavorite(itemId)}
/>
```

### With Active Tab Control
```tsx
<DetailPane
  item={selectedItem}
  activeTab="examples"
  onTabChange={(tabId) => setActiveTab(tabId)}
  visibleTabs={['purpose', 'examples', 'workflow']}
/>
```

### Loading State
```tsx
<DetailPane
  item={null}
  loading={true}
/>
```

### Empty State
```tsx
<DetailPane
  item={null}
  error={null}
/>
// Displays: "Select a component to view details"
```

## Tab Content Specifications

### Purpose Tab
- **Markdown rendering**: Component description, when to use, prerequisites
- **Metadata badges**: Stage, type, priority
- **File path**: Clickable with copy button
- **Quick actions**: Add to Favorites button

### Examples Tab
- **Code blocks**: Syntax-highlighted bash, TypeScript, JSON, YAML
- **Copy buttons**: Per code block
- **Titles**: Example scenario descriptions

### Options Tab
- **Table view**: Parameter, type, required, default, description columns
- **Inline badges**: Required vs optional indicators
- **Type formatting**: Monospace font for types

### Workflow Tab
- **Mermaid diagrams**: Rendered SVG with zoom/pan
- **PlantUML diagrams**: Rendered via Kroki service
- **Description**: Workflow context and related steps

### Traceability Tab
- **Link groups**: Input/Output/Dependencies/Related sections
- **Clickable links**: Navigate to related components
- **Visual indicators**: Icons for link type (input/output/etc.)

## Screen Usage

| Screen | Context | Configuration |
|--------|---------|---------------|
| SCR-001 Main Explorer | Detail pane in dual-pane layout | All tabs, default to Purpose |
| SCR-003 Stage-Filtered View | Detail pane with filtered item | All tabs |
| SCR-006 Component Detail Modal | Full-screen modal | All tabs, larger padding |

## Accessibility

- **Role**: `tabpanel` (provided by Spectrum Tabs)
- **ARIA**: `aria-labelledby`, `aria-selected`, `aria-controls`
- **Keyboard**:
  - Tab: Navigate to tab bar
  - Arrow Left/Right: Switch tabs
  - Enter/Space: Activate tab
  - Cmd+C: Copy path (when focused)
- **Focus**: Visible 2px blue ring on tabs
- **Screen Reader**: Tab labels announced, content changes announced
- **Contrast**: 4.5:1 minimum for text, 3:1 for tab underline

## Performance Considerations

- **Lazy Loading**: Render tab content only when tab is active
- **Memoization**: Memoize markdown rendering
- **Code Highlighting**: Use web worker for syntax highlighting
- **Mermaid Caching**: Cache rendered SVG diagrams
- **Virtual Scrolling**: For long documentation content

## Testing Checklist

- [ ] Renders tabs (Purpose, Examples, Options, Workflow, Traceability)
- [ ] Switches tabs on click
- [ ] Shows Purpose tab by default
- [ ] Hides tabs with no content (e.g., no examples)
- [ ] Renders markdown with headings, lists, code blocks
- [ ] Syntax highlights code blocks (bash, TypeScript, JSON)
- [ ] Renders Mermaid diagrams in Workflow tab
- [ ] Copy Path button copies to clipboard
- [ ] Add to Favorites toggles favorite status
- [ ] Shows empty state when no item selected
- [ ] Shows loading skeleton while fetching
- [ ] Shows error message on fetch failure
- [ ] Keyboard navigation works (Arrow keys, Tab)
- [ ] Focus indicator visible on tabs
- [ ] Screen reader announces tab changes
- [ ] Respects `prefers-reduced-motion` for tab transitions

---

**Traceability**:
- **Addresses Pain Points**: PP-1.2 (Contextual Documentation), PP-1.1 (Knowledge Transfer), PP-1.3 (Discoverability Challenge)
- **Enables JTBD**: JTBD-1.2 (Component context), JTBD-2.1 (Confidence), JTBD-1.3 (Find relevant tools - tagging)
- **Client Facts**: CF-008 (Multi-section documentation), CF-013 (File path references), CF-010 (Tagging system)
- **Feedback**: PF-002 (Tagging feature - tags field added to ComponentDetail interface)
- **Design Tokens**: Uses semantic colors, typography scale, spacing
- **Library**: Adobe Spectrum React Tabs, View, Heading, Link, Button
