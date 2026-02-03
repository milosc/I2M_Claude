---
name: ASSEMBLY_FIRST_COMMAND_GUIDE
description: Guide for Assembly-First prototype generation mode
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /ASSEMBLY_FIRST_COMMAND_GUIDE started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /ASSEMBLY_FIRST_COMMAND_GUIDE ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /ASSEMBLY_FIRST_COMMAND_GUIDE instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Assembly-First Command Guide

## Overview

When the component library is present (`.claude/templates/component-library/`), all prototype commands automatically enable **Assembly-First mode**. This guide explains how the commands behave differently in Assembly-First mode.

---

## Automatic Mode Detection

All `/prototype-*` commands automatically detect Assembly-First mode:

```
Component Library Present → Assembly-First Mode ON
Component Library Missing → Traditional Mode (fallback)
```

**No special flags required.** The system detects and adapts automatically.

---

## Command Behavior Changes

### `/prototype <SystemName>` - Full Orchestration

**Assembly-First Mode ON:**
```
1. Phase 0: Initialize (same)
2. Phase 1: Validate Discovery (same)
3. Phase 2: Requirements (same)
4. Phase 3-5: Data & Contracts (same)
5. Phase 6-7: Design Tokens (same)
6. Phase 8: Component Specifications
   → Reads component library manifest
   → Generates LIBRARY_REFERENCE.md
   → Generates aggregate components only (not all components)
7. Phase 9: Screen Specifications
   → Composes screens using library components
   → Generates component-usage.md per screen
   → Creates component usage matrix
8. Phase 10: Interactions (same)
9. Phase 11-12: Build Sequence & Code Generation
   → Enforces Assembly-First rules
   → Validates no raw HTML elements
   → Validates imports from @/component-library
   → Builds with library components
10. Phase 13-14: QA & UI Audit
    → Validates accessibility (library provides)
    → Validates no Assembly-First rule violations
```

**Traditional Mode:**
- Standard workflow (all components generated from scratch)

---

### `/prototype-components` - Component Specifications

**Assembly-First Mode ON:**
```bash
/prototype-components InventorySystem
```

**Output:**
```
01-components/
├── library-components/
│   └── LIBRARY_REFERENCE.md      # Reference to 62 library components
├── aggregates/
│   ├── KPICard.md                # Custom aggregate
│   ├── TaskListItem.md           # Custom aggregate
│   └── UserProfileCard.md        # Custom aggregate
└── COMPONENT_LIBRARY_SUMMARY.md  # Assembly-First summary
```

**Key Differences:**
- ✅ Reads `.claude/templates/component-library/manifests/components.json`
- ✅ Only generates aggregate components (combines multiple library components)
- ✅ Creates reference document instead of duplicating library components
- ✅ 80% fewer files generated
- ✅ ~15x token savings

**Traditional Mode:**
- Generates all ~50 component specifications

---

### `/prototype-screens` - Screen Specifications

**Assembly-First Mode ON:**
```bash
/prototype-screens InventorySystem
```

**Output:**
```
02-screens/
├── screen-index.md               # Includes component usage matrix
└── login-screen/
    ├── specification.md          # Component composition (library + aggregates)
    ├── component-usage.md        # Detailed library component usage
    └── data-requirements.md      # API calls and state
```

**Key Features:**
- Each screen specifies which library components to use
- Detailed `component-usage.md` with import statements and prop configurations
- Component usage matrix shows which components are used across screens
- No raw HTML elements mentioned in specs

**Traditional Mode:**
- Standard screen specifications (no component-usage.md)

---

### `/prototype-build` - Code Generation

**Assembly-First Mode ON:**
```bash
/prototype-build InventorySystem
```

**Generated Code Style:**
```tsx
// ✅ CORRECT: Assembly-First
import { Button, TextField, Form, Table } from '@/component-library';
import { KPICard } from '@/components/aggregates';
import { useAuth } from '@/hooks';

export function LoginScreen() {
  const { login, isLoading } = useAuth();

  return (
    <div className="flex items-center justify-center min-h-screen bg-canvas">
      <div className="w-full max-w-md p-8">
        <Form onSubmit={login} className="flex flex-col gap-4">
          <TextField name="email" type="email" label="Email" isRequired />
          <TextField name="password" type="password" label="Password" isRequired />
          <Button type="submit" isPending={isLoading}>
            {isLoading ? 'Signing in...' : 'Sign In'}
          </Button>
        </Form>
      </div>
    </div>
  );
}
```

**Validation Performed:**
- ❌ BLOCKS build if raw HTML elements found (`<button>`, `<input>`)
- ❌ BLOCKS build if manual ARIA attributes added
- ❌ BLOCKS build if imports not from @/component-library
- ✅ PASSES only if Assembly-First rules followed

**Traditional Mode:**
- Generates components from scratch
- No library import enforcement

---

### `/prototype-qa` - Quality Assurance

**Assembly-First Mode ON:**

Additional checks performed:
```
1. Assembly-First Rule Compliance
   - Scans code for raw HTML elements
   - Validates imports from component library
   - Checks for manual ARIA attributes
   - Validates render props usage

2. Accessibility (Automated)
   - Library provides A11Y by default
   - Validates keyboard navigation
   - Validates focus management
   - Validates ARIA attributes (auto-generated)

3. Component Coverage
   - Validates all screens use library/aggregate components
   - Checks component usage matrix matches implementation

4. Token Efficiency Report
   - Calculates actual token savings
   - Compares against traditional approach
```

**Traditional Mode:**
- Standard QA checks (manual A11Y verification required)

---

## Validation Commands

### Check Assembly-First Status

```bash
# Check if Assembly-First mode is enabled
cat _state/prototype_config.json | grep -A 5 "assembly_first"
```

**Expected Output (if enabled):**
```json
"assembly_first": {
  "enabled": true,
  "component_library_path": ".claude/templates/component-library/",
  "detected_at": "2026-01-02T10:30:00Z",
  "reason": "enabled"
}
```

---

### Validate Assembly-First Compliance

```bash
# Run Assembly-First validation
python3 .claude/hooks/prototype_quality_gates.py \
  --validate-assembly \
  --dir Prototype_InventorySystem/
```

**Checks Performed:**
```
✓ Component library reference exists
✓ No library components duplicated
✓ All screens use library/aggregate components
✓ No raw HTML elements in code
✓ All imports from @/component-library
✓ No manual ARIA attributes
✓ Build succeeds
```

---

### Scan for Rule Violations

```bash
# Scan for raw HTML elements
grep -r "<button\|<input\|<select\|<textarea" Prototype_*/prototype/src/

# Scan for manual ARIA
grep -r "role=\|aria-label=\|aria-" Prototype_*/prototype/src/

# Validate imports
grep -r "import.*from.*component-library" Prototype_*/prototype/src/
```

---

## Troubleshooting

### Issue: Assembly-First Mode Not Enabled

**Symptoms:**
- Traditional components generated instead of library reference
- `assembly_first.enabled == false` in config

**Diagnosis:**
```bash
# Check component library presence
ls .claude/templates/component-library/manifests/components.json

# Check project classification
cat _state/prototype_config.json | grep project_classification
```

**Solutions:**
1. **Library Missing**: Restore component library to `.claude/templates/component-library/`
2. **Wrong Project Type**: Verify `project_classification.type == "FULL_STACK"`
3. **Disabled in Config**: Set `assembly_first.enabled = true` in config

---

### Issue: Build Fails with Raw HTML Violation

**Error:**
```
Assembly-First violation: Raw HTML elements found
File: prototype/src/screens/LoginScreen.tsx:15
Element: <button>
```

**Fix:**
```tsx
// ❌ WRONG
<button onClick={handleClick}>Submit</button>

// ✅ CORRECT
import { Button } from '@/component-library';
<Button onPress={handleClick}>Submit</Button>
```

---

### Issue: Manual ARIA Attributes Detected

**Error:**
```
Assembly-First violation: Manual ARIA attributes
File: prototype/src/screens/Dashboard.tsx:42
Attribute: role="button"
```

**Fix:**
```tsx
// ❌ WRONG
<div role="button" aria-label="Close" onClick={handleClose}>
  X
</div>

// ✅ CORRECT
import { Button } from '@/component-library';
<Button onPress={handleClose} aria-label="Close">
  <CloseIcon />
</Button>
```

**Note:** `aria-label` is allowed for icon-only buttons.

---

### Issue: Component Not Found in Library

**Error:**
```
Component 'DateRangePicker' not found in library
Available: DatePicker, DateField, Calendar
```

**Solutions:**

**Option 1: Use Existing Components**
```tsx
// Combine DatePicker components
<div className="flex gap-2">
  <DatePicker label="Start Date" />
  <DatePicker label="End Date" />
</div>
```

**Option 2: Create Aggregate**
```tsx
// Create aggregate component in aggregates/
// DateRangePicker.tsx combines 2x DatePicker + custom logic
<DateRangePicker />
```

---

## Performance Metrics

### Token Usage Comparison

| Phase | Traditional | Assembly-First | Savings |
|-------|-------------|----------------|---------|
| **Components** | ~40,000 tokens | ~2,500 tokens | **16x** |
| **Screens** | ~30,000 tokens | ~5,000 tokens | **6x** |
| **Code Gen** | ~50,000 tokens | ~10,000 tokens | **5x** |
| **Total** | ~120,000 tokens | ~17,500 tokens | **~7x overall** |

### File Generation Comparison

| Category | Traditional | Assembly-First | Reduction |
|----------|-------------|----------------|-----------|
| **Component Specs** | ~50 files | ~10 files | **80%** |
| **Screen Specs** | ~45 files | ~60 files | -33% (more detail) |
| **Code Files** | Same | Same | 0% |
| **Total** | ~95 files | ~70 files | **26%** |

---

## Best Practices

### 1. Let Assembly-First Auto-Detect

```bash
# ✅ CORRECT: Let system detect mode
/prototype InventorySystem

# ❌ WRONG: Don't try to force mode
/prototype InventorySystem --mode=assembly-first  # Flag doesn't exist
```

### 2. Review Library Reference First

```bash
# Before generating screens, review available components
cat Prototype_*/01-components/library-components/LIBRARY_REFERENCE.md
```

### 3. Use Component Usage Matrix

```bash
# Check which components are used across screens
cat Prototype_*/02-screens/screen-index.md
# See "Component Usage Matrix" section
```

### 4. Validate Early and Often

```bash
# After Phase 8 (Components)
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 8 --dir Prototype_*/

# After Phase 9 (Screens)
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 9 --dir Prototype_*/

# After Phase 12 (Build)
python3 .claude/hooks/prototype_quality_gates.py --validate-assembly --dir Prototype_*/
```

### 5. Reference Component Library Docs

When unsure about component usage:
```bash
# View component API
cat .claude/templates/component-library/src/Button/Button.tsx

# View examples
cat .claude/templates/component-library/stories/Button.stories.tsx

# Run Storybook
cd .claude/templates/component-library
npm run storybook
```

---

## Related Documentation

- **Architecture**: `architecture/Assembly-First Design System/ASSEMBLY_FIRST_ARCHITECTURE.md`
- **Rule**: `.claude/commands/_assembly_first_rules.md`
- **Component Integration**: `.claude/skills/Prototype_Components/ASSEMBLY_FIRST_INTEGRATION.md`
- **Screen Integration**: `.claude/skills/Prototype_Screens/ASSEMBLY_FIRST_INTEGRATION.md`
- **Builder Integration**: `.claude/skills/Prototype_Builder/ASSEMBLY_FIRST_INTEGRATION.md`
- **Component Library**: `.claude/templates/component-library/`
- **CLAUDE.md**: Assembly-First section (main documentation)

---

## Summary

**Assembly-First mode is:**
- ✅ Automatic (no flags needed)
- ✅ Backward compatible (falls back to traditional)
- ✅ Enforced at build time (violations block deployment)
- ✅ Significantly more efficient (~7x token savings)
- ✅ More accessible (library provides A11Y)
- ✅ More consistent (no style drift)

**Commands work the same, output is optimized.**
