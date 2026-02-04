---
name: prototype-design
description: Generate design tokens and design brief
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-design started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: |
            SYSTEM_NAME=$(cat _state/session.json 2>/dev/null | grep -o '"project"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"project"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//' || echo "")
            if [ -n "$SYSTEM_NAME" ] && [ "$SYSTEM_NAME" != "pending" ]; then
              uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_prototype_output.py" --system-name "$SYSTEM_NAME" --phase design_tokens
            else
              echo '{"result": "skip", "reason": "System name not found in session"}'
              exit 0
            fi
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-design ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-design instruction_start '{"stage": "prototype", "method": "instruction-based"}'
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

- Phase 5 completed: Test data exists
- Checkpoint 5 passed

## Skills Used

Read BEFORE execution:
- `.claude/skills/Prototype_DesignBrief/SKILL.md` (Phase 6)
- `.claude/skills/Prototype_DesignTokens/SKILL.md` (Phase 7)

## Execution Flow

---

---

### Phase 6: Design Brief (Checkpoint 6)

#### Step 6.1: Load Inputs

Read:
- `_state/discovery_summary.json` (personas, brand context)
- `_state/requirements_registry.json` (feature scope)
- `ClientAnalysis_<SystemName>/03-strategy/PRODUCT_VISION.md` (if exists)

#### Step 6.2: Update Progress

```json
{
  "current_phase": 6,
  "phases": {
    "design_brief": {
      "status": "in_progress",
      "started_at": "<timestamp>"
    }
  }
}
```

#### Step 6.3: Execute Prototype_DesignBrief Skill

1. **Define Visual Direction**:
   - Industry context
   - Competitive positioning
   - Brand personality

2. **Define Design Principles**:
   - 3-5 core principles
   - Each with rationale and examples

3. **Define Accessibility Requirements**:
   - WCAG level (AA default)
   - Color contrast requirements
   - Keyboard navigation requirements

#### Step 6.4: Generate Design Brief

Create `00-foundation/design-brief.md`:

```markdown
# Design Brief

## Project Overview

**System:** <SystemName>
**Industry:** <industry>
**Target Users:** <persona list>

## Visual Direction

### Personality
- Professional and trustworthy
- Clear and efficient
- Modern but not trendy

### Mood
- Calm and focused
- Confident and capable
- Organized and systematic

### Inspiration
- Industrial efficiency tools
- Modern dashboard interfaces
- Clean data visualization

## Scope

### In Scope (MVP)
- P0 requirements from requirements registry
- Core user flows for primary personas

### Out of Scope
- P2 features
- Advanced customization
- Mobile-specific optimizations

## Constraints

- Accessibility: WCAG 2.1 AA compliance
- Performance: <3s initial load
- Browser Support: Chrome, Firefox, Safari, Edge (latest 2 versions)
```

Create `00-foundation/design-principles.md`:

```markdown
# Design Principles

## 1. Clarity Over Cleverness

**Rationale:** Users need to complete tasks efficiently without cognitive overhead.

**Application:**
- Use clear, descriptive labels
- Avoid hidden functionality
- Show system status prominently

**Example:**
- ✅ "Save Changes" button
- ❌ Floppy disk icon only

## 2. Progressive Disclosure

**Rationale:** Show only what's needed, when it's needed.

**Application:**
- Start with essential information
- Reveal details on demand
- Keep primary actions visible

## 3. Consistent Patterns

**Rationale:** Reduce learning curve through predictable interactions.

**Application:**
- Same action = same interaction everywhere
- Consistent component placement
- Unified feedback patterns

## 4. Accessible by Default

**Rationale:** Accessibility benefits all users and is a requirement.

**Application:**
- Sufficient color contrast (4.5:1 minimum)
- Keyboard navigation support
- Screen reader compatibility
- Clear focus indicators

## 5. Performance is UX

**Rationale:** Slow interfaces feel broken and frustrate users.

**Application:**
- Optimistic updates where safe
- Loading states for all async operations
- Lazy load non-critical content
```

#### Step 6.5: Validate Checkpoint 6

```bash
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 6 --dir Prototype_<SystemName>/
```

#### Step 6.6: Update Progress

Mark phase 6 completed, move to phase 7.

---

### Phase 7: Design Tokens (Checkpoint 7)

#### Step 7.1: Update Progress

```json
{
  "current_phase": 7,
  "phases": {
    "design_tokens": {
      "status": "in_progress",
      "started_at": "<timestamp>"
    }
  }
}
```

#### Step 7.2: Execute Prototype_DesignTokens Skill

1. **Define Color System**:
   - Primary, secondary, accent
   - Semantic colors (success, warning, error, info)
   - Neutral scale
   - Background and surface colors

2. **Define Typography**:
   - Font families (primary, mono)
   - Size scale
   - Weight scale
   - Line heights

3. **Define Spacing**:
   - Base unit
   - Spacing scale
   - Layout grid

4. **Generate Token JSON**:
   - CSS custom properties format
   - Tailwind config format

#### Step 7.3: Generate Design Tokens

Create `00-foundation/design-tokens.json`:

```json
{
  "color": {
    "primary": {
      "50": "#eff6ff",
      "100": "#dbeafe",
      "500": "#3b82f6",
      "600": "#2563eb",
      "700": "#1d4ed8",
      "900": "#1e3a8a"
    },
    "secondary": {
      "50": "#f8fafc",
      "500": "#64748b",
      "900": "#0f172a"
    },
    "semantic": {
      "success": "#22c55e",
      "warning": "#f59e0b",
      "error": "#ef4444",
      "info": "#3b82f6"
    },
    "neutral": {
      "0": "#ffffff",
      "50": "#f8fafc",
      "100": "#f1f5f9",
      "200": "#e2e8f0",
      "300": "#cbd5e1",
      "400": "#94a3b8",
      "500": "#64748b",
      "600": "#475569",
      "700": "#334155",
      "800": "#1e293b",
      "900": "#0f172a",
      "1000": "#000000"
    }
  },
  "typography": {
    "fontFamily": {
      "sans": "Inter, system-ui, sans-serif",
      "mono": "JetBrains Mono, monospace"
    },
    "fontSize": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem"
    },
    "fontWeight": {
      "normal": "400",
      "medium": "500",
      "semibold": "600",
      "bold": "700"
    },
    "lineHeight": {
      "tight": "1.25",
      "normal": "1.5",
      "relaxed": "1.75"
    }
  },
  "spacing": {
    "base": "4px",
    "scale": {
      "0": "0",
      "1": "0.25rem",
      "2": "0.5rem",
      "3": "0.75rem",
      "4": "1rem",
      "5": "1.25rem",
      "6": "1.5rem",
      "8": "2rem",
      "10": "2.5rem",
      "12": "3rem",
      "16": "4rem",
      "20": "5rem"
    }
  },
  "borderRadius": {
    "none": "0",
    "sm": "0.125rem",
    "default": "0.25rem",
    "md": "0.375rem",
    "lg": "0.5rem",
    "xl": "0.75rem",
    "full": "9999px"
  },
  "shadow": {
    "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
    "default": "0 1px 3px 0 rgb(0 0 0 / 0.1)",
    "md": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
    "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1)",
    "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1)"
  }
}
```

Create `00-foundation/color-system.md`:

```markdown
# Color System

## Primary Palette

Used for primary actions, links, and focus states.

| Token | Value | Usage |
|-------|-------|-------|
| primary-500 | #3b82f6 | Default primary |
| primary-600 | #2563eb | Hover state |
| primary-700 | #1d4ed8 | Active state |

## Semantic Colors

| Token | Value | Usage |
|-------|-------|-------|
| success | #22c55e | Positive actions, confirmations |
| warning | #f59e0b | Cautions, alerts |
| error | #ef4444 | Errors, destructive actions |
| info | #3b82f6 | Informational messages |

## Accessibility

All color combinations meet WCAG 2.1 AA requirements:
- Text on backgrounds: 4.5:1 minimum
- Large text: 3:1 minimum
- UI components: 3:1 minimum
```

Create `00-foundation/typography.md`:

```markdown
# Typography

## Font Families

- **Primary:** Inter (sans-serif)
- **Monospace:** JetBrains Mono

## Type Scale

| Name | Size | Line Height | Usage |
|------|------|-------------|-------|
| xs | 12px | 1.5 | Captions, labels |
| sm | 14px | 1.5 | Secondary text |
| base | 16px | 1.5 | Body text |
| lg | 18px | 1.5 | Emphasized text |
| xl | 20px | 1.25 | Subheadings |
| 2xl | 24px | 1.25 | Section headings |
| 3xl | 30px | 1.25 | Page headings |
| 4xl | 36px | 1.25 | Hero headings |

## Font Weights

| Weight | Value | Usage |
|--------|-------|-------|
| Normal | 400 | Body text |
| Medium | 500 | Emphasis |
| Semibold | 600 | Subheadings |
| Bold | 700 | Headings, strong emphasis |
```

Create `00-foundation/spacing-layout.md`:

```markdown
# Spacing & Layout

## Spacing Scale

Base unit: 4px

| Token | Value | Usage |
|-------|-------|-------|
| 1 | 4px | Tight spacing |
| 2 | 8px | Component internal |
| 3 | 12px | Related elements |
| 4 | 16px | Standard gap |
| 6 | 24px | Section separation |
| 8 | 32px | Major sections |
| 12 | 48px | Page sections |

## Layout Grid

- Container max-width: 1280px
- Gutter: 24px
- Columns: 12

## Breakpoints

| Name | Value | Description |
|------|-------|-------------|
| sm | 640px | Small tablets |
| md | 768px | Tablets |
| lg | 1024px | Laptops |
| xl | 1280px | Desktops |
| 2xl | 1536px | Large screens |
```

#### Step 7.4: Validate Checkpoint 7

```bash
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 7 --dir Prototype_<SystemName>/
```

#### Step 7.5: Update Progress

Mark phase 7 completed.

---

## Final Summary

```
═══════════════════════════════════════════════════════
  DESIGN PHASES COMPLETE (6-7)
═══════════════════════════════════════════════════════

  Phase 6 - Design Brief:
  ├── Visual Direction:    Defined
  ├── Principles:          <N>
  ├── Accessibility:       WCAG AA
  └── Outputs:
      • 00-foundation/design-brief.md
      • 00-foundation/design-principles.md

  Phase 7 - Design Tokens:
  ├── Colors:              <N> tokens
  ├── Typography:          <N> tokens
  ├── Spacing:             <N> tokens
  └── Outputs:
      • 00-foundation/design-tokens.json
      • 00-foundation/color-system.md
      • 00-foundation/typography.md
      • 00-foundation/spacing-layout.md

  Checkpoints:             6 ✅  7 ✅

═══════════════════════════════════════════════════════

  Next: /prototype-components or /prototype <SystemName>

═══════════════════════════════════════════════════════
```

## Outputs

| File | Phase | Purpose |
|------|-------|---------|
| `00-foundation/design-brief.md` | 6 | Visual direction |
| `00-foundation/design-principles.md` | 6 | Design principles |
| `00-foundation/design-tokens.json` | 7 | Token definitions |
| `00-foundation/color-system.md` | 7 | Color documentation |
| `00-foundation/typography.md` | 7 | Typography documentation |
| `00-foundation/spacing-layout.md` | 7 | Spacing documentation |

## Error Handling

| Error | Action |
|-------|--------|
| Vision document missing | Generate from requirements |
| Token generation fails | Use default token set |

### Step 8: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/prototype-design" \
  --stage "prototype" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype-data` | Run Phases 3-5 |
| `/prototype-components` | Run Phase 8 |
| `/prototype` | Run full prototype |
