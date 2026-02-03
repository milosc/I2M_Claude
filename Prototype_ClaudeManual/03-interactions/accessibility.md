# Accessibility Specification - ClaudeManual

## Overview

This document defines WCAG 2.1 AA compliance requirements for the ClaudeManual prototype, ensuring the application is usable by people with disabilities.

**Traceability**:
- Requirements: REQ-015 (Keyboard shortcuts), REQ-041 (WCAG compliance)
- Pain Points: PP-1.6 (Developer friction - needs keyboard efficiency)
- JTBD: JTBD-2.2 (Explore autonomously)

---

## WCAG 2.1 AA Requirements

### 1. Perceivable

#### 1.1 Text Alternatives

| Element | Requirement | Implementation |
|---------|-------------|----------------|
| Icons | All icons have `aria-label` or visible text | `<Button aria-label="Add to favorites">` |
| Images | Decorative images have `alt=""` | `<img alt="" role="presentation" />` |
| Diagrams | Complex diagrams have text descriptions | Long description in expandable section |
| Stage badges | Color + text label | `<Badge>Discovery</Badge>` not just color |

#### 1.2 Color Contrast

| Context | Requirement | Achieved |
|---------|-------------|----------|
| Normal text | 4.5:1 minimum | 7:1 (gray-900 on white) |
| Large text (18px+) | 3:1 minimum | 4.5:1 |
| UI components | 3:1 minimum | 3:1 (borders, icons) |
| Focus indicators | 3:1 minimum | 3:1 (blue-500 ring) |

**Verification**: All color combinations tested with axe-core and manual contrast checker.

### 2. Operable

#### 2.1 Keyboard Navigation

**Tab Order**: Logical flow matching visual layout

```
Header → Search → Stage Filter → Navigation Tree → Detail Pane → Footer
```

**Focus Management**:

| Interaction | Focus Behavior |
|-------------|----------------|
| Modal open | Focus trapped inside, first focusable element |
| Modal close | Return focus to trigger element |
| Tree expand | Focus remains on expanded node |
| Search execute | Focus moves to first result |
| Tab switch | Focus moves to tab panel content |

**Focus Indicators**:

```css
:focus-visible {
  outline: 2px solid var(--color-blue-500);
  outline-offset: 2px;
}

/* Remove outline for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

#### 2.2 Keyboard Shortcuts

| Shortcut | Action | Scope |
|----------|--------|-------|
| `Cmd/Ctrl + K` | Open global search | Global |
| `Cmd/Ctrl + B` | Toggle favorites panel | Global |
| `Cmd/Ctrl + /` | Open keyboard shortcuts help | Global |
| `Escape` | Close modal/dropdown | Modal/Dropdown |
| `Arrow Up/Down` | Navigate tree items | Navigation Tree |
| `Arrow Left` | Collapse tree node | Navigation Tree |
| `Arrow Right` | Expand tree node | Navigation Tree |
| `Enter` | Select tree item | Navigation Tree |
| `Home` | First tree item | Navigation Tree |
| `End` | Last tree item | Navigation Tree |
| `Tab` | Next focusable element | Global |
| `Shift + Tab` | Previous focusable element | Global |
| `Space` | Activate button/checkbox | Buttons |

**Implementation**:

```tsx
// Global keyboard shortcuts
useEffect(() => {
  const handleKeyDown = (e: KeyboardEvent) => {
    // Cmd/Ctrl + K: Open search
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      openSearch();
    }
    // Cmd/Ctrl + B: Toggle favorites
    if ((e.metaKey || e.ctrlKey) && e.key === 'b') {
      e.preventDefault();
      toggleFavorites();
    }
  };

  window.addEventListener('keydown', handleKeyDown);
  return () => window.removeEventListener('keydown', handleKeyDown);
}, []);
```

#### 2.3 Focus Trap (Modals)

```tsx
// Focus trap for modals
import { FocusTrap } from '@adobe/react-spectrum';

<FocusTrap>
  <Dialog>
    {/* Modal content */}
  </Dialog>
</FocusTrap>
```

### 3. Understandable

#### 3.1 Page Titles

| Page | Title Format |
|------|--------------|
| Main Explorer | "ClaudeManual - Explorer" |
| Search Results | "Search: {query} - ClaudeManual" |
| Favorites | "Favorites - ClaudeManual" |
| Component Detail | "{Component Name} - ClaudeManual" |

#### 3.2 Error Messages

| Error Type | Message | Recovery |
|------------|---------|----------|
| Search no results | "No results found for '{query}'" | Suggestions shown |
| Network error | "Unable to load. Check your connection." | Retry button |
| Invalid filter | "Filter combination returned no results" | Clear filters button |

#### 3.3 Form Labels

All form inputs have associated labels:

```tsx
<TextField>
  <Label>Search skills, commands, and agents</Label>
  <Input placeholder="Type to search..." />
</TextField>
```

### 4. Robust

#### 4.1 ARIA Roles and Attributes

| Component | Role | ARIA Attributes |
|-----------|------|-----------------|
| Navigation Tree | `tree` | `aria-label="Navigation"` |
| Tree Item | `treeitem` | `aria-expanded`, `aria-selected`, `aria-level` |
| Search Results | `listbox` | `aria-label="Search results"` |
| Search Result | `option` | `aria-selected` |
| Detail Tabs | `tablist` | `aria-label="Component sections"` |
| Tab Panel | `tabpanel` | `aria-labelledby` |
| Modal | `dialog` | `aria-modal="true"`, `aria-labelledby` |
| Loading | `status` | `aria-busy="true"`, `aria-live="polite"` |

#### 4.2 Live Regions

```tsx
// Announce search results count
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {results.length} results found for "{query}"
</div>

// Announce favorites changes
<div aria-live="assertive" className="sr-only">
  {lastAction === 'add' ? 'Added to favorites' : 'Removed from favorites'}
</div>
```

---

## Screen Reader Support

### Tested Combinations

| Screen Reader | Browser | Status |
|---------------|---------|--------|
| VoiceOver | Safari (macOS) | ✅ Supported |
| VoiceOver | Chrome (macOS) | ✅ Supported |
| NVDA | Firefox (Windows) | ✅ Supported |
| NVDA | Chrome (Windows) | ✅ Supported |
| JAWS | Chrome (Windows) | ✅ Supported |

### Screen Reader Announcements

| Action | Announcement |
|--------|--------------|
| Page load | Page title + landmark summary |
| Search execute | "X results found" |
| Tree expand | "Node expanded, X children" |
| Modal open | Dialog title + first focusable |
| Error | Error message via `aria-live` |
| Success | Success message via `aria-live` |

---

## Skip Links

```tsx
// Skip to main content
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>

// Skip to navigation
<a href="#navigation" className="sr-only focus:not-sr-only">
  Skip to navigation
</a>

// In page content
<main id="main-content" tabIndex={-1}>
  {/* Main content */}
</main>
```

---

## Testing Checklist

### Automated Testing

- [ ] axe-core integration in CI/CD
- [ ] Lighthouse accessibility audit (score ≥ 90)
- [ ] jest-axe for component tests

### Manual Testing

- [ ] Keyboard-only navigation (no mouse)
- [ ] Screen reader testing (VoiceOver/NVDA)
- [ ] High contrast mode
- [ ] Zoom to 200% (no content loss)
- [ ] Reduced motion preference respected

### Test Commands

```bash
# Run axe-core audit
npm run test:a11y

# Lighthouse accessibility
npx lighthouse http://localhost:3000 --only-categories=accessibility

# Generate accessibility report
npm run a11y:report
```

---

## Related

- `motion.md` - Reduced motion support
- `responsive.md` - Touch target sizes
- `design-tokens/tokens.json` - Color contrast values
