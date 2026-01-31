# Skill Invocation Framework

This document defines how skills can dynamically invoke other skills within the Prototype Builder framework.

---

## Overview

Skills can call other skills using the `INVOKE_SKILL` pattern. This enables:
- **Modular composition**: Build complex workflows from simple skills
- **Reusability**: 3rdParty skills can be called by any prototype skill
- **Loose coupling**: Skills only need to know the skill ID and input contract

---

## Skill Registry

All available skills are registered in `SKILL_REGISTRY.json`. The registry contains:
- Skill ID and location
- Input/output contracts
- Dependencies (`can_invoke`, `invoked_by`)
- Phase and category metadata

---

## Invocation Syntax

### Basic Invocation

```
INVOKE_SKILL:
  skill: "{skill-id}"
  inputs:
    {input_name}: {value}
    {input_name}: {value}
  outputs:
    - {expected_output_path}
  on_success: CONTINUE | STORE {variable}
  on_failure: BLOCK | WARN | SKIP
```

### Example: Invoke theme-factory

```
INVOKE_SKILL:
  skill: "theme-factory"
  inputs:
    theme_name: "ocean_depths"
  outputs:
    - theme_colors
    - theme_fonts
  on_success: STORE selected_theme
  on_failure: WARN "Theme not found, using defaults"
```

### Example: Invoke markitdown for document conversion

```
INVOKE_SKILL:
  skill: "markitdown"
  inputs:
    file_path: "discovery/requirements.pdf"
    ai_descriptions: true
  outputs:
    - "discovery/_converted/requirements.md"
  on_success: CONTINUE
  on_failure: BLOCK "Cannot convert document"
```

### Example: Invoke canvas-design for visual assets

```
INVOKE_SKILL:
  skill: "canvas-design"
  inputs:
    design_philosophy: READ("00-foundation/VISUAL_PHILOSOPHY.md")
    asset_type: "icons"
  outputs:
    - "00-foundation/assets/icons/*.svg"
  on_success: CONTINUE
  on_failure: SKIP "Visual assets are optional"
```

---

## Invocation Modes

### 1. Synchronous (Default)
Wait for the invoked skill to complete before continuing.

```
INVOKE_SKILL:
  skill: "prototype-qa"
  mode: sync
  ...
```

### 2. Background
Launch skill in background, continue with current skill.

```
INVOKE_SKILL:
  skill: "prototype-decomposition"
  mode: background
  ...

// Continue with other work...

// Later, wait for result if needed
AWAIT_SKILL: "prototype-decomposition"
```

### 3. Conditional
Only invoke if condition is met.

```
INVOKE_SKILL:
  skill: "webapp-testing"
  condition: prototype_running == true
  ...
```

---

## Input Passing

### Direct Values
```
INVOKE_SKILL:
  skill: "theme-factory"
  inputs:
    theme_name: "tech_innovation"
```

### From Variables
```
INVOKE_SKILL:
  skill: "canvas-design"
  inputs:
    design_philosophy: ${visual_philosophy}
    asset_type: ${selected_asset_type}
```

### From Files
```
INVOKE_SKILL:
  skill: "pptx"
  inputs:
    slides_content: READ("_state/requirements_registry.json")
    design_approach: READ("00-foundation/AESTHETIC_DIRECTION.md")
```

### From Previous Skill Output
```
// First skill
INVOKE_SKILL:
  skill: "prototype-validate-discovery"
  outputs:
    - discovery_summary
  on_success: STORE discovery_data

// Second skill uses output from first
INVOKE_SKILL:
  skill: "prototype-requirements"
  inputs:
    discovery_summary: ${discovery_data}
```

---

## Output Handling

### Store in Variable
```
INVOKE_SKILL:
  skill: "theme-factory"
  on_success: STORE theme_config

// Use later
colors = theme_config.colors
fonts = theme_config.fonts
```

### Expect File Outputs
```
INVOKE_SKILL:
  skill: "prototype-codegen"
  outputs:
    - "prototype/package.json"
    - "prototype/src/App.tsx"
  on_success: VERIFY_FILES
```

### Chain to Next Skill
```
INVOKE_SKILL:
  skill: "prototype-components"
  on_success: INVOKE_SKILL "prototype-screens"
```

---

## Error Handling

### BLOCK Mode
Stop execution if skill fails.

```
INVOKE_SKILL:
  skill: "prototype-validate-discovery"
  on_failure: BLOCK "Cannot proceed without discovery validation"
```

### WARN Mode
Log warning but continue.

```
INVOKE_SKILL:
  skill: "visual-documentation-plugin"
  on_failure: WARN "ERD visualization skipped"
```

### SKIP Mode
Silently skip if skill fails.

```
INVOKE_SKILL:
  skill: "canvas-design"
  on_failure: SKIP
```

### Custom Handler
```
INVOKE_SKILL:
  skill: "webapp-testing"
  on_failure:
    IF error.type == "no_server":
      LOG: "Start server first: npm run dev"
      PROMPT: "Server not running. Start it? (y/n)"
    ELSE:
      BLOCK: ${error.message}
```

---

## Claude Code Skill Tool Integration

When a skill needs to invoke a 3rdParty skill, it should use Claude Code's native Skill tool:

### Pattern for Invoking via Skill Tool

```
// In SKILL.md procedure:

IF need_theme_selection:

  // Use Claude Code's Skill tool to invoke
  USE_TOOL Skill:
    skill: "theme-factory"

  // The Skill tool will:
  // 1. Look up "theme-factory" in SKILL_REGISTRY.json
  // 2. Read .claude/skills/theme-factory/SKILL.md
  // 3. Execute the skill's procedure
  // 4. Return outputs

  // Capture the result
  theme_result = SKILL_OUTPUT
```

### Mapping to Skill Tool Parameters

| INVOKE_SKILL | Skill Tool |
|--------------|------------|
| `skill: "X"` | `skill: "X"` |
| `inputs: {...}` | Passed in conversation context |
| `outputs: [...]` | Verified after skill completes |

---

## Full Example: Prototype_DesignTokens with Dynamic Invocation

```
### Step 0: Theme Selection

PROMPT user for theme choice

IF user selects "apply: {theme_name}":

  // Invoke theme-factory skill
  INVOKE_SKILL:
    skill: "theme-factory"
    inputs:
      action: "apply"
      theme_name: ${user_selected_theme}
    on_success: STORE selected_theme
    on_failure: WARN "Theme not found, using custom generation"

  IF selected_theme:
    colors_source = selected_theme.colors
    fonts_source = selected_theme.fonts
    LOG: "✅ Applied theme: ${selected_theme.name}"

### Step 5.5: Generate Visual Assets

IF user_wants_visual_assets:

  // First, create design philosophy
  CREATE 00-foundation/VISUAL_PHILOSOPHY.md

  // Then invoke canvas-design for each asset type
  FOR each asset_type in [icons, illustrations, patterns, hero]:

    IF asset_type in user_selection:

      INVOKE_SKILL:
        skill: "canvas-design"
        inputs:
          design_philosophy: READ("00-foundation/VISUAL_PHILOSOPHY.md")
          asset_type: ${asset_type}
          color_palette: ${colors_source}
        outputs:
          - "00-foundation/assets/${asset_type}/"
        on_success:
          LOG: "✅ Generated ${asset_type}"
          asset_counts[asset_type] = COUNT(outputs)
        on_failure:
          WARN: "Could not generate ${asset_type}"
```

---

## Dependency Resolution

The framework automatically resolves skill dependencies:

### Check Before Invoke
```
INVOKE_SKILL:
  skill: "prototype-codegen"
  require_complete: ["prototype-components", "prototype-screens"]
  // Will check if required skills have completed before invoking
```

### Auto-Chain
```
INVOKE_SKILL:
  skill: "prototype-screens"
  auto_invoke_dependencies: true
  // Will automatically invoke prototype-components first if not complete
```

---

## Skill Discovery

### List Available Skills
```
QUERY_REGISTRY:
  category: "3rdparty"
  phase: "design"

// Returns: [theme-factory, canvas-design, frontend-design]
```

### Check Skill Capabilities
```
QUERY_REGISTRY:
  skill: "markitdown"

// Returns:
// {
//   inputs: { required: [file_path], optional: [ai_descriptions] },
//   outputs: ["*.md"],
//   can_invoke: [],
//   invoked_by: ["prototype-validate-discovery"]
// }
```

---

## Best Practices

### 1. Always Check Registry First
Before invoking a skill, verify it exists and check its input requirements.

```
IF REGISTRY_HAS("canvas-design"):
  INVOKE_SKILL: ...
ELSE:
  LOG: "canvas-design skill not available"
  FALLBACK: Use embedded asset generation
```

### 2. Provide All Required Inputs
Check the skill's `inputs.required` array and ensure all are provided.

### 3. Handle Failures Gracefully
Always specify `on_failure` behavior, especially for optional skills.

### 4. Use Background Mode for Non-Blocking Skills
Skills like `prototype-decomposition` that don't block workflow should run in background.

### 5. Log Skill Invocations
All skill invocations should be logged to `_state/prompt_log.json` for debugging.

```
LOG_SKILL_INVOCATION:
  invoking_skill: "prototype-design-tokens"
  invoked_skill: "theme-factory"
  inputs: { theme_name: "ocean_depths" }
  timestamp: NOW()
  result: "success" | "failure"
```

---

## Registry Update Protocol

When adding new skills to the framework:

1. Create skill folder in `.claude/skills/{skill-name}/`
2. Add `SKILL.md` with standard structure
3. Register in `SKILL_REGISTRY.json`:
   - Add entry with all metadata
   - Update `can_invoke` for skills that will call it
   - Update `invoked_by` to list callers

---

## Debugging Skill Invocations

### Trace Mode
```
INVOKE_SKILL:
  skill: "prototype-qa"
  trace: true
  // Outputs detailed execution log
```

### Dry Run
```
INVOKE_SKILL:
  skill: "prototype-codegen"
  dry_run: true
  // Shows what would happen without executing
```

---

## Migration from Embedded to Invoked

To migrate from embedded logic to skill invocation:

### Before (Embedded)
```
// TDD logic embedded in Prototype_CodeGen
FOR each component:
  CREATE test file
  VERIFY test fails
  CREATE implementation
  VERIFY test passes
```

### After (Invoked)
```
// TDD logic invoked as skill
FOR each component:
  INVOKE_SKILL:
    skill: "test-driven-development"
    inputs:
      component_spec: ${component}
      test_framework: "vitest"
    outputs:
      - "src/components/__tests__/${component}.test.tsx"
      - "src/components/${component}.tsx"
```

Both approaches work. Use invocation when:
- The capability is reusable across multiple skills
- You want to update the capability independently
- The skill has complex logic worth isolating
