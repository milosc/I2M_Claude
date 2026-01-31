# Assembly-First Integration for Prototype_Builder

> **CRITICAL**: This document adds Assembly-First mode detection and enforcement to the prototype build orchestration.

## Version

- **Version**: 3.0.0
- **Updated**: 2026-01-02
- **Change**: Assembly-First component library integration for full prototype workflow

---

## Assembly-First Mode Detection

**At the start of prototype generation (before Phase 8), detect if Assembly-First mode should be enabled:**

```
// ========== ASSEMBLY-FIRST MODE DETECTION ==========
assembly_first_enabled = false

CHECK:
  1. Does .claude/templates/component-library/ exist?
  2. Does .claude/templates/component-library/manifests/components.json exist?
  3. Does .claude/templates/component-library/SKILL.md exist?
  4. Is project_classification.type == "FULL_STACK"?

IF all checks pass:
  assembly_first_enabled = true
  LOG: "✅ Assembly-First mode ENABLED"
  LOG: "   Component library: .claude/templates/component-library/"
  LOG: "   Will use pre-built accessible components"

ELSE:
  assembly_first_enabled = false
  LOG: "⚠️ Assembly-First mode DISABLED"
  LOG: "   Reason: {reason_for_failure}"
  LOG: "   Will use traditional component generation"

STORE assembly_first_enabled in _state/prototype_config.json:
  {
    ...
    "assembly_first": {
      "enabled": assembly_first_enabled,
      "component_library_path": ".claude/templates/component-library/",
      "detected_at": timestamp,
      "reason": {reason or "enabled"}
    }
  }
// ===================================================
```

---

## Modified Build Sequence

When Assembly-First mode is enabled, the build sequence is modified:

### **Phase 8: Component Specifications**

**Assembly-First Mode ON:**
```
INVOKE Prototype_Components with:
  MODE: assembly_first
  PROCEDURE: Read ASSEMBLY_FIRST_INTEGRATION.md instead of standard SKILL.md

EXPECTED OUTPUTS:
  - 01-components/library-components/LIBRARY_REFERENCE.md
  - 01-components/aggregates/*.md (only custom aggregates)
  - 01-components/COMPONENT_LIBRARY_SUMMARY.md (assembly-first mode)

VALIDATION:
  - ✅ Library reference exists
  - ✅ Component manifest was read
  - ✅ Only aggregates generated (no duplication of library)
  - ✅ traceability/component_registry.json exists with mode: "assembly_first"
```

**Assembly-First Mode OFF:**
```
INVOKE Prototype_Components with:
  MODE: traditional
  PROCEDURE: Follow standard SKILL.md

EXPECTED OUTPUTS:
  - 01-components/primitives/*.md
  - 01-components/data-display/*.md
  - 01-components/feedback/*.md
  - 01-components/navigation/*.md
  - 01-components/overlays/*.md
  - 01-components/patterns/*.md
  - 01-components/COMPONENT_LIBRARY_SUMMARY.md
```

---

### **Phase 9: Screen Specifications**

**Assembly-First Mode ON:**
```
INVOKE Prototype_Screens with:
  MODE: assembly_first
  PROCEDURE: Read ASSEMBLY_FIRST_INTEGRATION.md instead of standard SKILL.md

EXPECTED OUTPUTS:
  - 02-screens/*/specification.md (with component composition from library)
  - 02-screens/*/component-usage.md (detailed library component usage)
  - 02-screens/*/data-requirements.md
  - 02-screens/screen-index.md (with component usage matrix)

VALIDATION:
  - ✅ All screens reference library or aggregate components
  - ✅ No raw HTML elements mentioned in specs
  - ✅ All interaction patterns use library render props
  - ✅ Component usage documented per screen
```

**Assembly-First Mode OFF:**
```
INVOKE Prototype_Screens with:
  MODE: traditional
  PROCEDURE: Follow standard SKILL.md

EXPECTED OUTPUTS:
  - 02-screens/*/specification.md
  - 02-screens/*/data-requirements.md
  - 02-screens/screen-index.md
```

---

### **Phase 11-12: Code Generation (Sequencer + CodeGen)**

**Assembly-First Mode ON:**

#### **Additional Pre-Generation Step:**
```
BEFORE generating any code:

1. READ .claude/commands/_assembly_first_rules.md (enforcement rules)
2. READ .claude/templates/component-library/SKILL.md (usage protocol)
3. READ .claude/templates/component-library/INTERACTIONS.md (state patterns)
4. READ 01-components/library-components/LIBRARY_REFERENCE.md (component mapping)

LOG: "✅ Assembly-First rules loaded for code generation"

STORE for use during code generation:
  - forbidden_practices[] (raw HTML elements, manual ARIA)
  - required_practices[] (imports, render props, tokens)
  - component_mapping{} (requirement → component)
```

#### **Code Generation with Assembly-First Enforcement:**
```
FOR each screen in build_sequence:

  // ========== ASSEMBLY-FIRST CODE GENERATION ==========

  GENERATE screen code with MANDATORY constraints:

    1. **Imports MUST be from component library:**
       ```tsx
       import {
         Button,
         TextField,
         Form,
         Table
       } from '@/component-library';
       ```

    2. **NO raw HTML elements:**
       FORBIDDEN: <button>, <input>, <select>, <textarea>, <div role="button">
       REQUIRED: <Button>, <TextField>, <Select>, <TextArea>

    3. **NO manual ARIA attributes:**
       FORBIDDEN: role="button", aria-label="..." (except icon-only)
       LIBRARY HANDLES: All ARIA attributes automatically

    4. **USE render props for state:**
       ```tsx
       <Button
         className={({ isPressed, isHovered, isPending }) =>
           `px-4 py-2 ${isPressed ? 'bg-accent-active' : 'bg-accent-default'}`
         }
         isPending={isLoading}
       >
         {isLoading ? 'Loading...' : 'Submit'}
       </Button>
       ```

    5. **USE Tailwind theme tokens:**
       REQUIRED: bg-surface-1, text-primary, accent-default
       FORBIDDEN: bg-gray-100, text-black, bg-blue-500

    6. **FOCUS on glue code:**
       - Data fetching (useQuery, useMutation)
       - Business logic
       - State management
       - API integration

  // ===================================================

  VALIDATE generated code:
    CHECKS:
      - ✅ All imports from @/component-library or @/components/aggregates
      - ✅ No raw HTML interactive elements
      - ✅ No manual ARIA attributes (except icon-only buttons)
      - ✅ Render props used for state-driven styling
      - ✅ Tailwind theme tokens used
      - ✅ Code compiles successfully

    IF any check fails:
      LOG ERROR: "Assembly-First rule violation in {file}"
      ADD to FAILURES_LOG.md
      REQUIRE fix before proceeding

  SAVE generated code to prototype/src/screens/{screen}.tsx

// =======================================================
```

**Assembly-First Mode OFF:**
```
INVOKE standard CodeGen workflow:
  - Generate components from scratch
  - Include ARIA attributes manually
  - Traditional component implementation
```

---

## Quality Gate Integration

### **Checkpoint 8: Component Specifications**

**Assembly-First Mode ON:**
```
VALIDATE:
  - [X] Component library manifest read
  - [X] LIBRARY_REFERENCE.md exists
  - [X] Only aggregate components generated
  - [X] No duplication of library components
  - [X] traceability/component_registry.json mode == "assembly_first"

IF validation fails:
  BLOCK: Cannot proceed to Phase 9
  REASON: Assembly-First components not properly initialized
```

**Assembly-First Mode OFF:**
```
VALIDATE:
  - [X] All component categories generated
  - [X] Component specs complete
  - [X] A11Y requirements addressed
```

---

### **Checkpoint 9: Screen Specifications**

**Assembly-First Mode ON:**
```
VALIDATE:
  - [X] All screens reference library or aggregate components
  - [X] No raw HTML mentioned in specifications
  - [X] component-usage.md exists for each screen
  - [X] All components exist in library or aggregates
  - [X] Component usage matrix generated in screen-index.md

IF validation fails:
  BLOCK: Cannot proceed to Phase 10
  REASON: Screen specifications don't follow Assembly-First rules
```

---

### **Checkpoint 12: Build**

**Assembly-First Mode ON:**
```
VALIDATE code:
  SCAN prototype/src/ for violations:

    SEARCH for raw HTML elements:
      - grep -r "<button" prototype/src/
      - grep -r "<input" prototype/src/
      - grep -r "<select" prototype/src/
      - grep -r "<textarea" prototype/src/

    IF any found:
      FAIL: "Assembly-First violation: Raw HTML elements found"
      LIST violating files
      BLOCK build

    SEARCH for imports:
      - All component imports from '@/component-library' or '@/components/aggregates'
      - No imports from 'react' for interactive elements

    IF violations found:
      FAIL: "Assembly-First violation: Invalid imports"
      LIST violating files
      BLOCK build

    RUN build:
      - npm run build

    IF build fails:
      FAIL: "Build error"
      SHOW errors
      BLOCK deployment

  IF all validations pass:
    LOG: "✅ Assembly-First build successful"
    PROCEED to Checkpoint 13
```

**Assembly-First Mode OFF:**
```
VALIDATE:
  - Standard build validation
  - Component implementations complete
  - Build succeeds
```

---

## Progress Tracking

Update `_state/progress.json` to track Assembly-First mode:

```json
{
  "assembly_first": {
    "enabled": true,
    "component_library_path": ".claude/templates/component-library/",
    "phases": {
      "components": {
        "mode": "assembly_first",
        "library_components_referenced": 62,
        "aggregate_components_generated": 8,
        "token_savings": "~15x"
      },
      "screens": {
        "mode": "assembly_first",
        "screens_generated": 15,
        "library_components_used": 28,
        "aggregate_components_used": 5,
        "component_usage_matrix": "generated"
      },
      "code_generation": {
        "mode": "assembly_first",
        "validation": {
          "raw_html_check": "passed",
          "import_check": "passed",
          "aria_check": "passed",
          "build_check": "passed"
        }
      }
    }
  }
}
```

---

## Error Handling

### **If Component Library Missing Mid-Build:**

```
IF assembly_first_enabled == true AND component_library_not_found:
  LOG ERROR: "Component library missing during build"
  PROMPT user:
    ═══════════════════════════════════════════════════════
    ⚠️  COMPONENT LIBRARY MISSING
    ═══════════════════════════════════════════════════════

    Assembly-First mode was enabled, but component library is now missing:
    Expected: .claude/templates/component-library/

    Options:
    1. "restore" - Restore component library from backup
    2. "fallback" - Switch to traditional mode (will regenerate components)
    3. "abort" - Stop build process
    ═══════════════════════════════════════════════════════

  WAIT for user response
  HANDLE accordingly
```

---

### **If Assembly-First Rules Violated:**

```
IF assembly_first_validation_fails:
  LOG ERROR: "Assembly-First rule violation detected"
  GENERATE violation report:

    # Assembly-First Violation Report

    Generated: {timestamp}

    ## Violations Found: {count}

    FOR each violation:
      ### {violation.type}
      - **File**: {violation.file}
      - **Line**: {violation.line}
      - **Issue**: {violation.description}
      - **Rule**: {violation.rule_reference}
      - **Fix**: {violation.suggested_fix}

    ## Required Actions:

    1. Review violations above
    2. Fix according to .claude/commands/_assembly_first_rules.md
    3. Re-run validation

  SAVE to _state/ASSEMBLY_FIRST_VIOLATIONS.md

  PROMPT user:
    ═══════════════════════════════════════════════════════
    ⚠️  ASSEMBLY-FIRST VIOLATIONS
    ═══════════════════════════════════════════════════════

    {count} violations detected. See:
    _state/ASSEMBLY_FIRST_VIOLATIONS.md

    Options:
    1. "fix" - Auto-fix violations where possible
    2. "review" - Review violations manually
    3. "continue" - Continue build (not recommended)
    ═══════════════════════════════════════════════════════

  WAIT for user response
```

---

## Backward Compatibility

The Prototype_Builder skill remains **fully backward compatible**:

| Scenario | Behavior |
|----------|----------|
| Component library present + FULL_STACK | Assembly-First mode ON |
| Component library present + BACKEND_ONLY | Assembly-First mode OFF (N/A) |
| Component library missing | Assembly-First mode OFF (traditional) |
| User disables in config | Assembly-First mode OFF (traditional) |

**No breaking changes** to existing workflows.

---

## Benefits Summary

When Assembly-First mode is enabled:

| Metric | Traditional | Assembly-First | Improvement |
|--------|-------------|----------------|-------------|
| **Token Usage** | ~800 per component | ~50 per component | **~15x reduction** |
| **Component Specs** | ~50 files | ~10 files (aggregates only) | **80% fewer files** |
| **Accessibility** | Manual ARIA | Built-in | **100% coverage** |
| **Consistency** | Varies | Guaranteed | **0 drift** |
| **Build Time** | Baseline | Faster (less generation) | **~30% faster** |
| **Code Quality** | Variable | Enforced by rules | **Higher** |

---

## Configuration

Users can control Assembly-First mode via `_state/prototype_config.json`:

```json
{
  "assembly_first": {
    "enabled": true,  // Set to false to disable
    "component_library_path": ".claude/templates/component-library/",
    "strict_validation": true,  // Block build on violations
    "auto_fix_violations": false  // Experimental auto-fix
  }
}
```

---

## Related Documentation

- **Architecture**: `architecture/Assembly-First Design System/ASSEMBLY_FIRST_ARCHITECTURE.md`
- **Rule**: `.claude/commands/_assembly_first_rules.md`
- **Component Integration**: `.claude/skills/Prototype_Components/ASSEMBLY_FIRST_INTEGRATION.md`
- **Screen Integration**: `.claude/skills/Prototype_Screens/ASSEMBLY_FIRST_INTEGRATION.md`
- **Component Library**: `.claude/templates/component-library/`

---

## Summary

The Prototype_Builder now:
1. ✅ Detects component library presence
2. ✅ Enables Assembly-First mode automatically
3. ✅ Orchestrates modified build sequence
4. ✅ Enforces Assembly-First rules during code generation
5. ✅ Validates compliance at checkpoints
6. ✅ Tracks Assembly-First metrics
7. ✅ Maintains backward compatibility

**Result**: Faster, more consistent, more accessible prototypes with significantly reduced token usage.
