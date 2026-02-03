# Component Detail Modal

**ID**: SCR-006
**Discovery ID**: S-X.X
**Application**: Web
**Priority**: P0
**Primary Persona**: All personas

---

## Overview

Full-screen modal for deep-dive into component documentation with tabbed interface, sticky header, and scrollable content. Provides progressive disclosure of component details with Purpose (default), Examples, Options, Workflow, and Traceability tabs.

**JTBD**: JTBD-1.2 (Understand component context), JTBD-2.1 (Build confidence through examples and workflow diagrams)

**Pain Points Addressed**: PP-1.2 (Lack of Contextual Documentation)

---

## Layout

### Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────────────────────┐  │
│ │ [×]                              Discovery_JTBD                     [⭐]│  │
│ ├─────────────────────────────────────────────────────────────────────────┤  │
│ │ [Purpose] [Examples] [Options] [Workflow] [Traceability]               │  │
│ ├─────────────────────────────────────────────────────────────────────────┤  │
│ │                                                                         │  │
│ │ # Discovery_JTBD                                                        │  │
│ │                                                                         │  │
│ │ **Path**: `.claude/skills/Discovery_JTBD/SKILL.md`                     │  │
│ │ [Copy Path to Clipboard]                                               │  │
│ │                                                                         │  │
│ │ ## Purpose                                                              │  │
│ │ Extracts Jobs To Be Done from validated pain points and client facts.  │  │
│ │ Generates structured JTBD document with functional, emotional, and     │  │
│ │ social jobs following When/Want/So-that format.                        │  │
│ │                                                                         │  │
│ │ ## When to Use                                                          │  │
│ │ **Workflow Stage**: Discovery (Checkpoint 4)                            │  │
│ │ **Prerequisites**: Pain points extracted (CP-2), client facts validated│  │
│ │ **Outputs**: JOBS_TO_BE_DONE.md, jtbd_registry.json                    │  │
│ │                                                                         │  │
│ │ ## Example Usage                                                        │  │
│ │ ```bash                                                                 │  │
│ │ # Invoke via Discovery orchestrator                                    │  │
│ │ /discovery ClaudeManual Client_Materials/                              │  │
│ │ ```                                                                     │  │
│ │                                                                         │  │
│ │ [Workflow Diagram Placeholder - Mermaid]                                │  │
│ │                                                                         │  │
│ │ ... (scrollable content)                                                │  │
│ │                                                                         │  │
│ └─────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Grid Structure

| Region | Layout | Components |
|--------|--------|------------|
| Modal Overlay | Full viewport | Dialog (Adobe Spectrum) |
| Header | Sticky top, flex row justify-between | Heading, Close button, Favorite button |
| Tab Bar | Sticky below header | Tabs (Adobe Spectrum) |
| Content Area | Scrollable | MarkdownRenderer (COMP-AGG-008) |
| Footer | Sticky bottom (optional) | Action buttons if needed |

---

## Components Used

| Component | Instance | Props | Source |
|-----------|----------|-------|--------|
| Dialog | Modal container | `isDismissable={true}`, `size="L"` | Adobe Spectrum |
| Heading | Title | `level={2}` | Adobe Spectrum |
| Button | Close button | `variant="secondary"`, `onPress={onClose}` | Adobe Spectrum |
| Button | Favorite button | `variant="primary"`, `onPress={toggleFavorite}` | Adobe Spectrum |
| Tabs | Tab navigation | `selectedKey={selectedTab}`, `onSelectionChange={setSelectedTab}` | Adobe Spectrum |
| TabList | Tab bar | - | Adobe Spectrum |
| TabPanels | Tab content | - | Adobe Spectrum |
| Item | Tab items | - | Adobe Spectrum |
| View | Content container | `padding="size-400"` | Adobe Spectrum |
| Link | Copy Path button | `variant="primary"` | Adobe Spectrum |
| MarkdownRenderer | Content display | `content={markdownContent}` | COMP-AGG-008 |

---

## Data Requirements

### Page Load Data

| Field | Source | Type | Required |
|-------|--------|------|----------|
| componentId | URL param or props | string | Yes |
| componentType | URL param or props | 'Skill' \| 'Command' \| 'Agent' \| 'Rule' \| 'Hook' \| 'Workflow' \| 'WaysOfWorking' \| 'ArchitectureDoc' | Yes |
| componentData | GET /api/{type}/{id} | Skill \| Command \| Agent \| ... | Yes |
| isFavorited | localStorage or GET /api/preferences | boolean | No |

### User Input Data

| Field | Component | Validation |
|-------|-----------|------------|
| selectedTab | Tabs | enum: 'purpose' \| 'examples' \| 'options' \| 'workflow' \| 'traceability' |
| favoriteToggle | Button | boolean |

---

## State Management

### Local State

```typescript
interface ComponentDetailModalState {
  isOpen: boolean;
  componentId: string | null;
  componentType: 'Skill' | 'Command' | 'Agent' | 'Rule' | 'Hook' | 'Workflow' | 'WaysOfWorking' | 'ArchitectureDoc' | null;
  componentData: any | null;
  selectedTab: 'purpose' | 'examples' | 'options' | 'workflow' | 'traceability';
  loading: boolean;
  error: string | null;
  isFavorited: boolean;
}
```

### Global State Dependencies

| Store | Slice | Usage |
|-------|-------|-------|
| preferences | favorites | Check if component is favorited |
| preferences | theme | Apply theme to markdown rendering |

---

## Navigation

### Entry Points

| From | Trigger | Params |
|------|---------|--------|
| Search Results (SCR-002) | Click "View Details" button | `{ id, type }` |
| Comparison View (SCR-005) | Click component card | `{ id, type }` |
| Favorites Page (SCR-004) | Click favorite item | `{ id, type }` |
| Main Explorer (SCR-001) | Click tree item | `{ id, type }` |

### Exit Points

| To | Trigger | Data Passed |
|----|---------|-------------|
| Previous screen | Close button (×) | - |
| Previous screen | Esc key | - |
| Previous screen | Click outside modal | - |

---

## Interactions

### User Actions

| Action | Component | Handler | Result |
|--------|-----------|---------|--------|
| View Details | Modal open | `onOpen(id, type)` | Load component data, show modal |
| Switch Tab | Tabs | `onSelectionChange` | Update selectedTab, render new content |
| Copy Path | Link button | `onClick` | Copy file path to clipboard, show toast |
| Toggle Favorite | Button (⭐) | `onPress` | Add/remove from favorites, update icon state |
| Close Modal | Button (×) | `onPress` | Close modal, clear state |
| Close Modal | Backdrop | `onDismiss` | Close modal, clear state |

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Esc` | Close modal |
| `Tab` | Navigate between tabs |
| `Cmd+C` (when focused on path) | Copy path |

---

## Responsive Behavior

| Breakpoint | Changes |
|------------|---------|
| Desktop (>1024px) | Full modal with max-width 80vw, centered |
| Tablet (768-1024px) | Full modal with max-width 90vw |
| Mobile (<768px) | Full-screen modal (100vw, 100vh), tabs scroll horizontally |

---

## Accessibility

- **ARIA Role**: `role="dialog"`, `aria-modal="true"`, `aria-labelledby="modal-title"`
- **Focus Management**: Focus Close button on open, trap focus within modal
- **Keyboard Navigation**: Tab through interactive elements, Esc to close
- **Screen Reader Support**: Tab labels announced, content changes announced on tab switch
- **Color Contrast**: 4.5:1 minimum for text

---

## Error States

| State | Display | Recovery |
|-------|---------|----------|
| Load Error | ErrorBanner in modal content | Retry button |
| Invalid Component ID | "Component not found" message | Close button |
| Network Error | Toast notification, modal remains open | Retry button |
| Markdown Parse Error | Display raw markdown with warning | No retry (show raw content) |

---

## UX Psychology

### Progressive Disclosure
- **Default Tab**: Purpose (most common need)
- **Advanced Tabs**: Options, Workflow, Traceability (power users)
- **Benefit**: Newcomers see only what they need, experts can dive deeper

### Visual Learning
- **Workflow Diagrams**: Mermaid/PlantUML diagrams clarify complex processes
- **Code Examples**: Syntax-highlighted examples with copy buttons
- **Benefit**: Builds confidence through visual context (JTBD-2.1)

### Low-Friction Actions
- **Copy Path Button**: One-click copy eliminates manual file navigation
- **Favorites Toggle**: Single-click bookmark for future access
- **Benefit**: Reduces developer friction (PP-1.6)

---

## Traceability

### Discovery Traceability
- **Pain Points**: PP-1.2 (Lack of Contextual Documentation)
- **JTBD**: JTBD-1.2 (Component context), JTBD-2.1 (Confidence)
- **Client Facts**: CF-008 (Multi-section documentation)
- **Roadmap Features**: F-004 (Multi-section detail pane), F-018 (Workflow diagrams), F-019 (Usage examples)

### Requirements Traceability
- **REQ-021**: Skill documentation display ✅
- **REQ-022**: Command documentation display ✅
- **REQ-023**: Agent documentation display ✅

---

## Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Modal Open Time | < 200ms | Time to first paint |
| Tab Switch Time | < 100ms | Time to render new content |
| Markdown Render Time | < 500ms | Full content visible |
| Mermaid Diagram Render | < 1s | SVG fully rendered |

---

## Testing Criteria

### Functional Tests
- [ ] Modal opens with correct component data
- [ ] Tabs switch between Purpose, Examples, Options, Workflow, Traceability
- [ ] Copy Path button copies to clipboard
- [ ] Favorite button toggles favorite state
- [ ] Close button closes modal
- [ ] Esc key closes modal
- [ ] Click outside modal closes modal

### Visual Tests
- [ ] Sticky header remains visible on scroll
- [ ] Tab bar remains visible on scroll
- [ ] Markdown renders with syntax highlighting
- [ ] Mermaid diagrams render correctly
- [ ] Mobile layout uses full-screen modal

### Accessibility Tests
- [ ] Focus trapped within modal
- [ ] Tab navigation works correctly
- [ ] Screen reader announces tab changes
- [ ] Color contrast meets WCAG 2.1 AA
- [ ] Keyboard shortcuts work

---

*Generated: 2026-01-31 | Agent: prototype-screen-specifier | Session: session-screen-scr006*
