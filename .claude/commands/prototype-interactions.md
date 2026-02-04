---
name: prototype-interactions
description: Generate interaction specifications and motion system
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-interactions started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: |
            SYSTEM_NAME=$(cat _state/session.json 2>/dev/null | grep -o '"project"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"project"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//' || echo "")
            if [ -n "$SYSTEM_NAME" ] && [ "$SYSTEM_NAME" != "pending" ]; then
              uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_prototype_output.py" --system-name "$SYSTEM_NAME" --phase interactions
            else
              echo '{"result": "skip", "reason": "System name not found in session"}'
              exit 0
            fi
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-interactions ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-interactions instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Assembly-First and traceability rules:

```bash
# Assembly-First rules (loaded automatically in Prototype stage)
/_assembly_first_rules

# Traceability rules for ID management
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Required: `<SystemName>` or path to `Prototype_<SystemName>/`

## Prerequisites

- Phase 9 completed: Screen specifications exist
- Checkpoint 9 passed

## Skills Used

Read BEFORE execution:
- `.claude/skills/Prototype_Interactions/SKILL.md`

## Execution Steps

### Step 1: Load Inputs

Read:
- `00-foundation/design-tokens.json`
- `00-foundation/design-principles.md` (accessibility requirements)
- `01-components/component-index.md`
- `02-screens/screen-index.md`

### Step 2: Update Progress

```json
{
  "current_phase": 10,
  "phases": {
    "interactions": {
      "status": "in_progress",
      "started_at": "<timestamp>"
    }
  }
}
```

### Step 3: Execute Prototype_Interactions Skill

Generate three specification files:

#### 3.1 Motion System

Create `03-interactions/motion-system.md`:

```markdown
# Motion System

## Principles

1. **Purposeful**: Motion serves a purpose (feedback, orientation, delight)
2. **Quick**: Animations should feel instant, not slow
3. **Natural**: Follow physics-based easing
4. **Accessible**: Respect reduced motion preferences

## Duration Scale

| Token | Value | Usage |
|-------|-------|-------|
| instant | 0ms | Immediate feedback |
| fast | 100ms | Micro-interactions |
| normal | 200ms | Standard transitions |
| slow | 300ms | Complex transitions |
| slower | 500ms | Page transitions |

## Easing Functions

| Token | Value | Usage |
|-------|-------|-------|
| ease-out | cubic-bezier(0, 0, 0.2, 1) | Enter animations |
| ease-in | cubic-bezier(0.4, 0, 1, 1) | Exit animations |
| ease-in-out | cubic-bezier(0.4, 0, 0.2, 1) | Move animations |
| spring | cubic-bezier(0.34, 1.56, 0.64, 1) | Playful feedback |

## Animation Patterns

### Fade In

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.fade-in {
  animation: fadeIn 200ms ease-out;
}
```

**Usage:** Modals, toasts, tooltips appearing

### Slide In

```css
@keyframes slideInFromRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.slide-in-right {
  animation: slideInFromRight 300ms ease-out;
}
```

**Usage:** Drawers, panels, page transitions

### Scale In

```css
@keyframes scaleIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.scale-in {
  animation: scaleIn 200ms ease-out;
}
```

**Usage:** Modals, dropdown menus

### Skeleton Pulse

```css
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.skeleton {
  animation: pulse 2s ease-in-out infinite;
}
```

**Usage:** Loading states

## Component Animations

| Component | Enter | Exit | Hover | Active |
|-----------|-------|------|-------|--------|
| Button | none | none | 100ms background | 50ms scale(0.98) |
| Modal | scale-in 200ms | fade-out 150ms | - | - |
| Drawer | slide-in 300ms | slide-out 200ms | - | - |
| Toast | slide-in 200ms | fade-out 150ms | - | - |
| Dropdown | scale-in 100ms | fade-out 100ms | - | - |
| Tooltip | fade-in 150ms | fade-out 100ms | - | - |

## Page Transitions

| Transition | Animation | Duration |
|------------|-----------|----------|
| Navigate forward | Slide left + fade | 300ms |
| Navigate back | Slide right + fade | 300ms |
| Same-level nav | Cross-fade | 200ms |

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

All animations respect the user's reduced motion preference.
```

#### 3.2 Accessibility Specification

Create `03-interactions/accessibility-spec.md`:

```markdown
# Accessibility Specification

## Compliance Target

**WCAG 2.1 Level AA**

## Perceivable

### 1.1 Text Alternatives

| Element | Requirement |
|---------|-------------|
| Images | Alt text describing content |
| Icons | aria-label or aria-hidden if decorative |
| Charts | Text summary + data table fallback |
| Videos | Captions and transcripts |

### 1.3 Adaptable

| Requirement | Implementation |
|-------------|----------------|
| Semantic HTML | Use proper heading hierarchy (h1-h6) |
| Landmarks | header, nav, main, aside, footer |
| Lists | ul/ol for related items |
| Tables | th with scope, caption |

### 1.4 Distinguishable

| Requirement | Value |
|-------------|-------|
| Color contrast (text) | 4.5:1 minimum |
| Color contrast (large text) | 3:1 minimum |
| Color contrast (UI) | 3:1 minimum |
| Focus indicator | 2px solid, contrasting color |
| Text resize | Up to 200% without loss |

## Operable

### 2.1 Keyboard Accessible

| Component | Keyboard Support |
|-----------|------------------|
| Button | Space, Enter to activate |
| Link | Enter to activate |
| Input | Standard text input |
| Select | Arrow keys, Enter, Space |
| Checkbox | Space to toggle |
| Radio | Arrow keys to move, Space to select |
| Modal | Tab trap, Escape to close |
| Dropdown | Arrow keys, Enter, Escape |
| Tabs | Arrow keys to switch, Tab to content |

### 2.4 Navigable

| Requirement | Implementation |
|-------------|----------------|
| Skip link | "Skip to main content" link at top |
| Page titles | Descriptive, unique per page |
| Focus order | Logical tab sequence |
| Link purpose | Clear from link text alone |
| Focus visible | Always visible focus ring |

### 2.5 Input Modalities

| Requirement | Implementation |
|-------------|----------------|
| Touch target | Minimum 44x44px |
| Pointer cancellation | Actions on release, not press |
| Motion actuation | Alternative controls available |

## Understandable

### 3.1 Readable

| Requirement | Implementation |
|-------------|----------------|
| Language | lang attribute on html |
| Unusual words | Definitions available |
| Abbreviations | Expanded on first use |

### 3.2 Predictable

| Requirement | Implementation |
|-------------|----------------|
| On focus | No context change |
| On input | Warning before changes |
| Consistent navigation | Same location across pages |
| Consistent identification | Same name for same function |

### 3.3 Input Assistance

| Requirement | Implementation |
|-------------|----------------|
| Error identification | aria-invalid, clear message |
| Labels | Associated label for all inputs |
| Error suggestion | Helpful fix suggestions |
| Error prevention | Confirmation for destructive actions |

## Robust

### 4.1 Compatible

| Requirement | Implementation |
|-------------|----------------|
| Valid HTML | No parsing errors |
| Name, role, value | Proper ARIA usage |
| Status messages | aria-live for updates |

## ARIA Patterns

### Modal Dialog

```html
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <h2 id="modal-title">Confirm Action</h2>
  <p>Are you sure you want to continue?</p>
  <button>Cancel</button>
  <button>Confirm</button>
</div>
```

### Alert

```html
<div role="alert" aria-live="assertive">
  Error: Please fill in all required fields.
</div>
```

### Tab Panel

```html
<div role="tablist">
  <button role="tab" aria-selected="true" aria-controls="panel-1">Tab 1</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2">Tab 2</button>
</div>
<div id="panel-1" role="tabpanel" aria-labelledby="tab-1">Content 1</div>
<div id="panel-2" role="tabpanel" aria-labelledby="tab-2" hidden>Content 2</div>
```

## Screen Reader Testing

Test with:
- NVDA (Windows)
- VoiceOver (macOS/iOS)
- TalkBack (Android)

## Color Blindness

Design accommodates:
- Deuteranopia (red-green)
- Protanopia (red-green)
- Tritanopia (blue-yellow)

Use icons/patterns in addition to color for status indication.
```

#### 3.3 Responsive Behavior

Create `03-interactions/responsive-behavior.md`:

```markdown
# Responsive Behavior

## Breakpoints

| Name | Value | Target |
|------|-------|--------|
| sm | 640px | Mobile landscape |
| md | 768px | Tablets |
| lg | 1024px | Small laptops |
| xl | 1280px | Desktops |
| 2xl | 1536px | Large screens |

## Layout Patterns

### Sidebar Navigation

| Breakpoint | Behavior |
|------------|----------|
| ≥ lg | Fixed sidebar, 256px |
| md - lg | Collapsible sidebar, icon-only default |
| < md | Hidden sidebar, hamburger menu |

### Content Grid

| Breakpoint | Columns |
|------------|---------|
| ≥ xl | 12 columns, 24px gutter |
| lg - xl | 12 columns, 16px gutter |
| md - lg | 8 columns, 16px gutter |
| sm - md | 4 columns, 16px gutter |
| < sm | 2 columns, 12px gutter |

### Card Layouts

| Breakpoint | Cards per row |
|------------|---------------|
| ≥ xl | 4 |
| lg - xl | 3 |
| md - lg | 2 |
| < md | 1 (full width) |

## Component Adaptations

### Data Table

| Breakpoint | Behavior |
|------------|----------|
| ≥ md | Full table with all columns |
| < md | Card view, stacked layout |

### Navigation Header

| Breakpoint | Behavior |
|------------|----------|
| ≥ md | Full navigation links visible |
| < md | Hamburger menu, drawer navigation |

### Form Layout

| Breakpoint | Behavior |
|------------|----------|
| ≥ md | Side-by-side fields where appropriate |
| < md | Stacked fields |

### Modal

| Breakpoint | Behavior |
|------------|----------|
| ≥ md | Centered modal, max-width 600px |
| < md | Full-screen modal |

## Touch Considerations

| Element | Mobile Adjustment |
|---------|-------------------|
| Buttons | Minimum 44px touch target |
| Links | Increased padding, 44px height |
| Inputs | 48px height for easy tap |
| Checkboxes | Larger tap area |
| Close buttons | 44x44px minimum |

## Container Widths

| Breakpoint | Max Width | Padding |
|------------|-----------|---------|
| < sm | 100% | 16px |
| sm | 640px | 24px |
| md | 768px | 24px |
| lg | 1024px | 32px |
| xl | 1280px | 32px |
| 2xl | 1536px | 32px |

## Image Handling

| Context | Strategy |
|---------|----------|
| Hero images | srcset with multiple sizes |
| Thumbnails | Fixed aspect ratio, object-fit: cover |
| Icons | SVG, scalable |
| Charts | Re-render at breakpoints |

## Typography Scaling

| Element | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| h1 | 36px | 32px | 28px |
| h2 | 30px | 26px | 24px |
| h3 | 24px | 22px | 20px |
| body | 16px | 16px | 16px |
| small | 14px | 14px | 14px |

## Testing Requirements

Test at these widths:
- 320px (small mobile)
- 375px (iPhone)
- 768px (iPad portrait)
- 1024px (iPad landscape / small laptop)
- 1280px (laptop)
- 1920px (desktop)
```

### Step 4: Validate Checkpoint 10

```bash
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 10 --dir Prototype_<SystemName>/
```

**Validation Criteria**:
- `03-interactions/motion-system.md` exists
- `03-interactions/accessibility-spec.md` exists
- `03-interactions/responsive-behavior.md` exists
- Accessibility spec mentions WCAG AA
- Motion system includes reduced motion support

### Step 5: Update Progress

```json
{
  "current_phase": 11,
  "phases": {
    "interactions": {
      "status": "completed",
      "completed_at": "<timestamp>",
      "outputs": [
        "03-interactions/motion-system.md",
        "03-interactions/accessibility-spec.md",
        "03-interactions/responsive-behavior.md"
      ]
    }
  }
}
```

### Step 6: Display Summary

```
═══════════════════════════════════════════════════════
  INTERACTIONS COMPLETE (Phase 10)
═══════════════════════════════════════════════════════

  Motion System:
  ├── Duration tokens:     5
  ├── Easing functions:    4
  ├── Animation patterns:  4
  └── Reduced motion:      ✅ Supported

  Accessibility:
  ├── Target:              WCAG 2.1 AA
  ├── Color contrast:      4.5:1 / 3:1
  ├── Keyboard support:    All components
  └── ARIA patterns:       Documented

  Responsive:
  ├── Breakpoints:         5
  ├── Layout patterns:     Documented
  └── Component adaptations: Documented

  Checkpoint 10:           ✅ PASSED

═══════════════════════════════════════════════════════

  Output: 03-interactions/

  Next: /prototype-build or /prototype <SystemName>

═══════════════════════════════════════════════════════
```

## Outputs

| File | Purpose |
|------|---------|
| `03-interactions/motion-system.md` | Animation specifications |
| `03-interactions/accessibility-spec.md` | WCAG compliance spec |
| `03-interactions/responsive-behavior.md` | Responsive design spec |

## Error Handling

| Error | Action |
|-------|--------|
| Screen specs missing | **BLOCK** - Run /prototype-screens first |
| Design tokens missing | Use default tokens |

### Step 7: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/prototype-interactions" \
  --stage "prototype" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype-screens` | Run Phase 9 |
| `/prototype-build` | Run Phases 11-12 |
| `/prototype` | Run full prototype |
