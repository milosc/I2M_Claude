---
name: specifying-interaction-design
description: Use when you need to generate motion systems, micro-interactions, and accessibility specifications for the interaction layer.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill specifying-interaction-design started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill specifying-interaction-design ended '{"stage": "prototype"}'
---

# Spec Interaction Design

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill specifying-interaction-design instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_Interactions
- **Version**: 2.3.1
- **Created**: 2024-12-13
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3

## Description
Generate motion design system, micro-interactions, and accessibility specifications. Follows OUTPUT_STRUCTURE.md for deterministic folder structure.

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

Generate motion design system, micro-interactions, and accessibility specifications. Follows OUTPUT_STRUCTURE.md for deterministic folder structure.

## Output Structure (REQUIRED)

This skill MUST generate the following structure:

```
03-interactions/
├── accessibility-specs.md            # WCAG compliance details
├── micro-interactions.md             # Component-level animations
├── motion-system.md                  # Timing, easing, principles
├── PHASE_06_VALIDATION_REPORT.md     # Validation results
└── README.md                         # Directory overview
```

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ 01-components/COMPONENT_LIBRARY_SUMMARY.md → components needing motion
READ 02-screens/SCREEN_SPECIFICATIONS_SUMMARY.md → screen transitions
READ _state/requirements_registry.json → A11Y requirements

IDENTIFY requirements this skill MUST address:
  - A11Y-006: Reduced motion support (if exists)
  - A11Y-007: Animation timing (if exists)
  - UX requirements for feedback
  
IF components not generated:
  BLOCK: "Run Components first"
```

### Step 2: Generate Motion System
```
CREATE 03-interactions/motion-system.md:
  # Motion System
  
  ## Design Principles
  1. **Purposeful**: Every animation has meaning
  2. **Quick**: Never delay user intent
  3. **Natural**: Follow physics-based easing
  4. **Consistent**: Same actions = same animations
  5. **Accessible**: Respect prefers-reduced-motion
  
  ## Timing Tokens
  | Token | Duration | Use Case |
  |-------|----------|----------|
  | --duration-instant | 0ms | Immediate feedback |
  | --duration-fast | 100ms | Button hover/active |
  | --duration-normal | 200ms | Standard transitions |
  | --duration-slow | 300ms | Complex reveals |
  | --duration-slower | 500ms | Page transitions |
  
  ## Easing Functions
  | Token | Curve | Use Case |
  |-------|-------|----------|
  | --ease-default | cubic-bezier(0.4, 0, 0.2, 1) | General purpose |
  | --ease-in | cubic-bezier(0.4, 0, 1, 1) | Exit animations |
  | --ease-out | cubic-bezier(0, 0, 0.2, 1) | Enter animations |
  | --ease-in-out | cubic-bezier(0.4, 0, 0.2, 1) | Symmetric |
  | --ease-bounce | cubic-bezier(0.68, -0.55, 0.265, 1.55) | Playful feedback |
  
  ## CSS Custom Properties
  ```css
  :root {
    /* Durations */
    --duration-instant: 0ms;
    --duration-fast: 100ms;
    --duration-normal: 200ms;
    --duration-slow: 300ms;
    --duration-slower: 500ms;
    
    /* Easings */
    --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
    --ease-in: cubic-bezier(0.4, 0, 1, 1);
    --ease-out: cubic-bezier(0, 0, 0.2, 1);
    --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
    --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  }
  
  /* Reduced motion override */
  @media (prefers-reduced-motion: reduce) {
    :root {
      --duration-instant: 0ms;
      --duration-fast: 0ms;
      --duration-normal: 0ms;
      --duration-slow: 0ms;
      --duration-slower: 0ms;
    }
  }
  ```
  
  ## Transition Patterns
  
  ### Fade
  ```css
  .fade-enter { opacity: 0; }
  .fade-enter-active { 
    opacity: 1; 
    transition: opacity var(--duration-normal) var(--ease-out);
  }
  .fade-exit { opacity: 1; }
  .fade-exit-active { 
    opacity: 0; 
    transition: opacity var(--duration-fast) var(--ease-in);
  }
  ```
  
  ### Slide
  ```css
  .slide-up-enter { 
    opacity: 0; 
    transform: translateY(16px); 
  }
  .slide-up-enter-active { 
    opacity: 1; 
    transform: translateY(0); 
    transition: all var(--duration-normal) var(--ease-out);
  }
  ```
  
  ### Scale
  ```css
  .scale-enter { 
    opacity: 0; 
    transform: scale(0.95); 
  }
  .scale-enter-active { 
    opacity: 1; 
    transform: scale(1); 
    transition: all var(--duration-normal) var(--ease-out);
  }
  ```
```

### Step 3: Generate Micro-Interactions
```
CREATE 03-interactions/micro-interactions.md:
  # Micro-Interactions
  
  ## Component Animations
  
  ### Button
  | State | Property | Value | Duration | Easing |
  |-------|----------|-------|----------|--------|
  | hover | background | darken 5% | fast | default |
  | active | transform | scale(0.98) | instant | - |
  | focus | box-shadow | focus ring | fast | out |
  | loading | - | spinner rotate | 1000ms | linear |
  
  ```css
  .button {
    transition: 
      background-color var(--duration-fast) var(--ease-default),
      transform var(--duration-instant),
      box-shadow var(--duration-fast) var(--ease-out);
  }
  
  .button:hover {
    filter: brightness(0.95);
  }
  
  .button:active {
    transform: scale(0.98);
  }
  
  .button:focus-visible {
    box-shadow: 0 0 0 2px var(--focus-ring-color);
  }
  ```
  
  ### Card
  | Interaction | Animation |
  |-------------|-----------|
  | Hover (if interactive) | Subtle lift (translateY -2px, shadow increase) |
  | Click | Scale down slightly |
  | Drag start | Lift higher, add shadow |
  | Drag end | Settle back |
  
  ### Modal/Dialog
  | Stage | Animation |
  |-------|-----------|
  | Backdrop enter | Fade in (slow) |
  | Content enter | Scale + fade in (normal) |
  | Content exit | Fade out (fast) |
  | Backdrop exit | Fade out (fast) |
  
  ### Toast/Alert
  | Stage | Animation |
  |-------|-----------|
  | Enter | Slide in from edge + fade |
  | Exit | Slide out + fade |
  | Auto-dismiss | Progress bar countdown |
  
  ### Dropdown/Menu
  | Stage | Animation |
  |-------|-----------|
  | Open | Scale from origin + fade (fast) |
  | Close | Fade out (fast) |
  | Item hover | Background highlight (instant) |
  
  ### Sidebar
  | State | Animation |
  |-------|-----------|
  | Collapse | Width transition (slow) |
  | Expand | Width transition (normal) |
  | Icons only | Opacity transition for labels |
  
  ## Drag and Drop
  
  ### Kanban Cards
  ```
  Drag Start:
    - Lift card (transform: scale(1.02) translateY(-4px))
    - Add shadow (box-shadow increase)
    - Reduce opacity of original position (opacity: 0.5)
  
  Dragging:
    - Ghost follows cursor smoothly
    - Valid drop zones highlight
    - Invalid zones show not-allowed cursor
  
  Drop:
    - Card settles into position (ease-bounce)
    - Flash highlight to confirm (background pulse)
    - Update column counts (fade transition)
  
  Cancel:
    - Card returns to origin (ease-out)
    - Shadow reduces
  ```
  
  ## Loading States
  
  ### Skeleton
  - Shimmer animation (gradient slide)
  - Duration: 1500ms
  - Infinite loop
  
  ### Spinner
  - Rotation: 1000ms linear infinite
  - Opacity pulse for trail effect
  
  ### Progress Bar
  - Width transition: 200ms ease-out
  - Indeterminate: sliding gradient
```

### Step 4: Generate Accessibility Specs
```
CREATE 03-interactions/accessibility-specs.md:
  # Accessibility Specifications
  
  ## Requirements Addressed
  | Req ID | Description | Implementation |
  |--------|-------------|----------------|
  | A11Y-001 | Keyboard navigation | Tab order, arrow keys |
  | A11Y-003 | Visible focus | 2px focus ring |
  | A11Y-006 | Reduced motion | prefers-reduced-motion |
  
  ## WCAG Compliance
  
  ### 2.1.1 Keyboard (Level A)
  All functionality available from keyboard.
  
  **Implementation:**
  - All interactive elements focusable
  - Tab order follows visual order
  - Skip links for main content
  - Arrow key navigation in menus
  
  ### 2.1.2 No Keyboard Trap (Level A)
  Focus can move away from any component.
  
  **Implementation:**
  - Modal focus trap with Escape to close
  - Dropdown closes on Tab out
  - No infinite focus loops
  
  ### 2.3.1 Three Flashes (Level A)
  No content flashes more than 3x per second.
  
  **Implementation:**
  - All animations < 3 flashes/second
  - Loading spinners use smooth rotation
  
  ### 2.3.3 Animation from Interactions (Level AAA)
  Users can disable motion animations.
  
  **Implementation:**
  ```css
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }
  }
  ```
  
  ## Focus Management
  
  ### Focus Indicators
  ```css
  :focus-visible {
    outline: none;
    box-shadow: 
      0 0 0 2px var(--color-background),
      0 0 0 4px var(--focus-ring-color);
  }
  ```
  
  ### Focus Trap (Modals)
  ```javascript
  // Focus trapping for modals
  const focusableElements = modal.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];
  
  // Trap focus within modal
  modal.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    }
    
    if (e.key === 'Escape') {
      closeModal();
    }
  });
  ```
  
  ## Screen Reader Announcements
  
  ### Live Regions
  ```html
  <!-- Status updates -->
  <div role="status" aria-live="polite" aria-atomic="true">
    {status message}
  </div>
  
  <!-- Alerts -->
  <div role="alert" aria-live="assertive">
    {error message}
  </div>
  ```
  
  ### Drag and Drop Announcements
  - Drag start: "Grabbed {item}. Use arrow keys to move."
  - Moving: "Over {zone}. Press Space to drop."
  - Drop: "{item} dropped in {zone}."
  - Cancel: "Movement cancelled. {item} returned to original position."
  
  ## Color Contrast
  
  | Element | Foreground | Background | Ratio | Level |
  |---------|------------|------------|-------|-------|
  | Body text | #1a1a1a | #ffffff | 15.3:1 | AAA |
  | Link | #0066cc | #ffffff | 5.9:1 | AA |
  | Error text | #cc0000 | #fff5f5 | 5.7:1 | AA |
  | Disabled | #6b7280 | #ffffff | 4.6:1 | AA |
  
  ## Touch Targets
  
  | Element | Minimum Size | Recommended |
  |---------|--------------|-------------|
  | Button | 44x44px | 48x48px |
  | Link | 44x44px | - |
  | Checkbox | 24x24px + 44px hit area | - |
  | Close button | 44x44px | - |
```

### Step 5: Generate README
```
CREATE 03-interactions/README.md:
  # Interactions
  
  This directory contains the motion and interaction design system.
  
  ## Files
  
  | File | Purpose |
  |------|---------|
  | motion-system.md | Timing tokens, easing functions, patterns |
  | micro-interactions.md | Component-specific animations |
  | accessibility-specs.md | WCAG compliance, keyboard, screen readers |
  
  ## Quick Reference
  
  ### Duration Tokens
  - Instant: 0ms (immediate feedback)
  - Fast: 100ms (hover, focus)
  - Normal: 200ms (standard transitions)
  - Slow: 300ms (reveals)
  - Slower: 500ms (page transitions)
  
  ### Key Principles
  1. Always respect `prefers-reduced-motion`
  2. Keep animations under 300ms for interactions
  3. Use ease-out for entering, ease-in for exiting
  4. Ensure focus indicators are always visible
```

### Step 6: Generate Validation Report
```
CREATE 03-interactions/PHASE_06_VALIDATION_REPORT.md:
  # Phase 06: Interactions Validation Report
  
  ## Summary
  | Metric | Value |
  |--------|-------|
  | Files Generated | 4 |
  | A11Y Requirements Addressed | {count} |
  | Motion Tokens Defined | 10 |
  | Component Interactions | {count} |
  
  ## Validation Results
  
  ### Motion System
  - [x] Timing tokens defined
  - [x] Easing functions defined
  - [x] Reduced motion support
  - [x] CSS custom properties
  
  ### Micro-Interactions
  - [x] All interactive components covered
  - [x] Drag-drop animations
  - [x] Loading states
  - [x] Transitions documented
  
  ### Accessibility
  - [x] Focus indicators specified
  - [x] Keyboard navigation patterns
  - [x] Screen reader announcements
  - [x] Color contrast documented
  
  ## Status: PASSED ✅
```

### Step 7: Update Progress
```
UPDATE _state/progress.json:
  phases.interactions.status = "complete"
  phases.interactions.completed_at = timestamp
  phases.interactions.outputs = [
    "03-interactions/motion-system.md",
    "03-interactions/micro-interactions.md",
    "03-interactions/accessibility-specs.md",
    "03-interactions/README.md",
    "03-interactions/PHASE_06_VALIDATION_REPORT.md"
  ]
  phases.interactions.validation = {
    status: "passed"
  }
  phases.interactions.metrics = {
    motion_tokens: 10,
    component_interactions: count,
    a11y_requirements_addressed: count
  }
```

---

## Output Files (REQUIRED)

| Path | Purpose | Blocking? |
|------|---------|-----------|
| `motion-system.md` | Timing and easing | ✅ Yes |
| `micro-interactions.md` | Component animations | ✅ Yes |
| `accessibility-specs.md` | WCAG, keyboard, focus | ✅ Yes |
| `README.md` | Overview | ⚠️ Warning |
| `PHASE_06_VALIDATION_REPORT.md` | Validation | ⚠️ Warning |

---

## Progress.json Update

```json
{
  "phases": {
    "interactions": {
      "status": "complete",
      "completed_at": "2024-12-13T12:30:00Z",
      "outputs": [
        "03-interactions/motion-system.md",
        "03-interactions/micro-interactions.md",
        "03-interactions/accessibility-specs.md",
        "03-interactions/README.md"
      ],
      "metrics": {
        "motion_tokens": 10,
        "component_interactions": 15,
        "a11y_requirements_addressed": 4
      }
    }
  }
}
```
