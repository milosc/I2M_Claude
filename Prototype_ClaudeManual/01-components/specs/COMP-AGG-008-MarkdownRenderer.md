# MarkdownRenderer

**ID**: COMP-AGG-008
**Category**: Content Display
**Priority**: P0

## Overview

Markdown content renderer with syntax highlighting, Mermaid diagrams, and code copy buttons. Combines Adobe Spectrum's View, Heading, Text, and Link with marked and Mermaid libraries.

## Props Interface

```typescript
interface MarkdownRendererProps {
  /** Markdown content */
  content: string;
  /** Theme variant */
  theme?: 'light' | 'dark';
  /** Enable Mermaid rendering */
  enableDiagrams?: boolean;
  /** Code copy handler */
  onCopyCode?: (code: string, language: string) => void;
}
```

## Library Components Used

- **View** (Spectrum): Container
- **Heading** (Spectrum): H1-H6 rendering
- **Text** (Spectrum): Body text
- **Link** (Spectrum): Hyperlinks

## Business Logic

### Markdown Parsing
```typescript
import { marked } from 'marked';
import Prism from 'prismjs';

function renderMarkdown(markdown: string): string {
  marked.setOptions({
    highlight: (code, lang) => {
      if (Prism.languages[lang]) {
        return Prism.highlight(code, Prism.languages[lang], lang);
      }
      return code;
    }
  });

  return marked(markdown);
}
```

## Usage Examples

```tsx
<MarkdownRenderer
  content={markdownContent}
  theme="light"
  enableDiagrams={true}
  onCopyCode={(code, lang) => copyToClipboard(code)}
/>
```

## Screen Usage

| Screen | Context |
|--------|---------|
| SCR-006 Component Detail Modal | Full documentation |
| SCR-009 Workflow Viewer | Workflow descriptions |
| SCR-010 Architecture Browser | ADR content |

---

**Traceability**: JTBD-1.2 (Component context), CF-008 (Multi-section documentation)
