# Assembly-First Automatic Mode Detection

> **Version**: 1.0.0
> **Last Updated**: 2026-01-02
> **Status**: Active

---

## Overview

Assembly-First mode is **automatically detected** by the LLM during prototype generation. No manual configuration is required. The system checks for the presence of the component library and sets the mode accordingly.

**Key Principle**: If the component library exists, use it. Otherwise, fall back to traditional mode.

---

## Detection Flow

### Phase 0: Initialization

When the user runs `/prototype <SystemName>`, the LLM automatically performs detection during Phase 0:

```
USER: /prototype InventorySystem

LLM EXECUTION (Phase 0):

1. Parse arguments → SystemName = "InventorySystem"
2. Validate Discovery exists → ClientAnalysis_InventorySystem/
3. Create output folder → Prototype_InventorySystem/
4. **RUN ASSEMBLY-FIRST MODE DETECTION** ← HAPPENS HERE
5. Initialize state files (with detection result)
6. Initialize traceability
7. Validate Checkpoint 0
```

---

## Detection Logic

The LLM executes the following checks in sequence:

### Check 1: Component Library Folder Exists

```typescript
const libraryPath = '.claude/templates/component-library/';
const libraryExists = await fs.exists(libraryPath);

if (!libraryExists) {
  return { enabled: false, reason: 'component_library_folder_missing' };
}
```

### Check 2: Component Manifest Exists

```typescript
const manifestPath = '.claude/templates/component-library/manifests/components.json';
const manifestExists = await fs.exists(manifestPath);

if (!manifestExists) {
  return { enabled: false, reason: 'component_manifest_missing' };
}
```

### Check 3: Library SKILL File Exists

```typescript
const skillPath = '.claude/templates/component-library/SKILL.md';
const skillExists = await fs.exists(skillPath);

if (!skillExists) {
  return { enabled: false, reason: 'library_skill_file_missing' };
}
```

### Check 4: Project Type is FULL_STACK

```typescript
// Inferred from Discovery or user input
const projectType = getProjectType(discoveryPath);

if (projectType !== 'FULL_STACK') {
  return { enabled: false, reason: 'project_type_not_full_stack' };
}
```

### Final Decision

```typescript
if (libraryExists && manifestExists && skillExists && projectType === 'FULL_STACK') {
  return {
    enabled: true,
    component_library_path: '.claude/templates/component-library/',
    detected_at: new Date().toISOString(),
    reason: 'enabled'
  };
} else {
  return {
    enabled: false,
    component_library_path: null,
    detected_at: new Date().toISOString(),
    reason: reason_from_failed_check
  };
}
```

---

## Where the Variable is Stored

### Primary Storage: `_state/prototype_config.json`

The detection result is stored in the prototype config file:

```json
{
  "schema_version": "1.0.0",
  "system_name": "InventorySystem",
  "created_at": "2026-01-02",
  "discovery_source": "ClientAnalysis_InventorySystem/",
  "output_path": "Prototype_InventorySystem/",
  "framework": "react",
  "styling": "tailwind",
  "assembly_first": {
    "enabled": true,
    "component_library_path": ".claude/templates/component-library/",
    "detected_at": "2026-01-02T10:30:00Z",
    "reason": "enabled"
  },
  "settings": {
    "skip_failures": true,
    "generate_tests": true,
    "accessibility_level": "AA"
  }
}
```

**Location**: `_state/prototype_config.json` (at project root, shared folder)

**Created**: Phase 0 (Initialize)

**Read by**: All subsequent phases (8, 9, 11-12)

---

## How Phases Use the Variable

Each phase that needs to know the mode reads the config file:

### Phase 8: Components

```typescript
// Read config
const config = JSON.parse(fs.readFileSync('_state/prototype_config.json'));
const assemblyFirstEnabled = config.assembly_first.enabled;

if (assemblyFirstEnabled) {
  // Read ASSEMBLY_FIRST_INTEGRATION.md
  const integrationDoc = fs.readFileSync('.claude/skills/Prototype_Components/ASSEMBLY_FIRST_INTEGRATION.md');
  // Generate library reference + aggregates only
  generateLibraryReference();
  generateAggregatesOnly();
} else {
  // Read SKILL.md
  const skillDoc = fs.readFileSync('.claude/skills/Prototype_Components/SKILL.md');
  // Generate all components traditionally
  generateAllComponents();
}
```

### Phase 9: Screens

```typescript
const config = JSON.parse(fs.readFileSync('_state/prototype_config.json'));
const assemblyFirstEnabled = config.assembly_first.enabled;

if (assemblyFirstEnabled) {
  // Read ASSEMBLY_FIRST_INTEGRATION.md
  // Generate component-usage.md per screen
  generateScreensWithComponentUsage();
} else {
  // Read SKILL.md
  // Generate standard screen specs
  generateStandardScreenSpecs();
}
```

### Phase 11-12: Build

```typescript
const config = JSON.parse(fs.readFileSync('_state/prototype_config.json'));
const assemblyFirstEnabled = config.assembly_first.enabled;

if (assemblyFirstEnabled) {
  // Read Prototype_Builder/ASSEMBLY_FIRST_INTEGRATION.md
  // Read assembly-first.md rules
  const rules = loadAssemblyFirstRules();

  // Generate code with enforcement
  generateCodeWithLibraryImports();
  validateNoRawHTML();
  validateNoManualARIA();
} else {
  // Read Prototype_Sequencer/SKILL.md + Prototype_CodeGen/SKILL.md
  // Generate all components from scratch
  generateComponentsFromScratch();
}
```

---

## Console Output

The LLM logs the detection result to provide visibility:

### When Enabled

```
═══════════════════════════════════════════════════════
  PHASE 0: INITIALIZE
═══════════════════════════════════════════════════════

  System Name:     InventorySystem
  Discovery:       ClientAnalysis_InventorySystem/
  Output:          Prototype_InventorySystem/

  ✅ Assembly-First mode ENABLED
     Component library: .claude/templates/component-library/
     62 accessible components available
     Token savings: ~7x overall

═══════════════════════════════════════════════════════
```

### When Disabled

```
═══════════════════════════════════════════════════════
  PHASE 0: INITIALIZE
═══════════════════════════════════════════════════════

  System Name:     InventorySystem
  Discovery:       ClientAnalysis_InventorySystem/
  Output:          Prototype_InventorySystem/

  ⚠️  Assembly-First mode DISABLED
     Reason: component_library_folder_missing
     Will use traditional component generation

═══════════════════════════════════════════════════════
```

---

## Manual Override (Optional)

While automatic detection handles most cases, users can manually override if needed.

### How to Disable Assembly-First

Edit `_state/prototype_config.json` **before** running phases 8+:

```json
{
  "assembly_first": {
    "enabled": false,
    "reason": "user_override_disabled"
  }
}
```

### How to Force Enable Assembly-First

Edit `_state/prototype_config.json` **before** running phases 8+:

```json
{
  "assembly_first": {
    "enabled": true,
    "component_library_path": ".claude/templates/component-library/",
    "reason": "user_override_enabled"
  }
}
```

**⚠️ Warning**: Forcing enabled without the component library will cause errors in phases 8, 9, 11-12.

---

## State Transitions

The mode cannot change mid-execution:

```
Phase 0: Detect → Set mode → Store in config
         ↓
Phase 8: Read config → Branch to workflow
         ↓
Phase 9: Read config → Branch to workflow
         ↓
Phase 11-12: Read config → Branch to workflow
```

**Once set in Phase 0, the mode remains constant for the entire prototype generation.**

To change mode:
1. Delete `_state/prototype_config.json`
2. Re-run `/prototype-init` or `/prototype` (will re-detect)

---

## Validation

The mode is validated at each checkpoint:

### Checkpoint 8: Components

```python
# prototype_quality_gates.py
def validate_checkpoint_8(prototype_dir):
    config = load_config(f"{prototype_dir}/_state/prototype_config.json")

    if config['assembly_first']['enabled']:
        # Validate library reference exists
        assert exists(f"{prototype_dir}/01-components/library-components/LIBRARY_REFERENCE.md")
        # Validate no library components duplicated
        assert not exists(f"{prototype_dir}/01-components/primitives/Button.md")  # Should use library
    else:
        # Validate all components generated
        assert exists(f"{prototype_dir}/01-components/primitives/button.md")
```

### Checkpoint 12: Build

```python
def validate_checkpoint_12(prototype_dir):
    config = load_config(f"{prototype_dir}/_state/prototype_config.json")

    if config['assembly_first']['enabled']:
        # Scan for raw HTML violations
        violations = scan_for_raw_html(f"{prototype_dir}/prototype/src/")
        assert len(violations) == 0, f"Assembly-First violations: {violations}"
    else:
        # Standard build validation
        assert build_succeeds(f"{prototype_dir}/prototype/")
```

---

## Troubleshooting

### Issue: Mode is OFF but library exists

**Symptoms**:
- Component library folder exists at `.claude/templates/component-library/`
- But `assembly_first.enabled == false`

**Diagnosis**:
```bash
# Check if manifest exists
ls .claude/templates/component-library/manifests/components.json

# Check config reason
cat _state/prototype_config.json | grep -A 5 "assembly_first"
```

**Possible Causes**:
1. Manifest file missing → Add `manifests/components.json`
2. SKILL.md missing → Add `SKILL.md` to library
3. Project type not FULL_STACK → Set project type correctly

### Issue: Mode is ON but library missing

**Symptoms**:
- `assembly_first.enabled == true`
- But library folder doesn't exist
- Phases 8, 9, 11-12 fail

**Diagnosis**:
```bash
# Verify library exists
ls .claude/templates/component-library/

# Check if manually forced
cat _state/prototype_config.json | grep "user_override"
```

**Solution**:
1. Restore component library to `.claude/templates/component-library/`
2. OR set `enabled: false` in config
3. Re-run from checkpoint before phase 8

---

## Testing Mode Detection

To test the detection logic:

### Test 1: Library Present → Enabled

```bash
# Ensure library exists
ls .claude/templates/component-library/manifests/components.json

# Run prototype
/prototype TestSystem

# Verify mode
cat _state/prototype_config.json | grep "enabled"
# Expected: "enabled": true
```

### Test 2: Library Missing → Disabled

```bash
# Temporarily move library
mv .claude/templates/component-library /tmp/

# Run prototype
/prototype TestSystem

# Verify mode
cat _state/prototype_config.json | grep "enabled"
# Expected: "enabled": false

# Restore library
mv /tmp/component-library .claude/templates/
```

### Test 3: Partial Library → Disabled

```bash
# Remove manifest
rm .claude/templates/component-library/manifests/components.json

# Run prototype
/prototype TestSystem

# Verify mode and reason
cat _state/prototype_config.json | grep -A 3 "assembly_first"
# Expected: "enabled": false, "reason": "component_manifest_missing"

# Restore manifest
# (from backup)
```

---

## Summary

| Aspect | Details |
|--------|---------|
| **Detection Time** | Phase 0 (Initialize) |
| **Detection Method** | Automatic file system checks |
| **Who Sets It** | LLM (Claude Code) |
| **Storage Location** | `_state/prototype_config.json` |
| **Scope** | Entire prototype generation (Phases 0-14) |
| **Can Change Mid-Run** | No (set once in Phase 0) |
| **Manual Override** | Optional (edit config file) |
| **Validation** | Checkpoints 8, 9, 12 |
| **Logging** | Console output at Phase 0 and completion |

---

## Related Documentation

- **Architecture**: `ASSEMBLY_FIRST_ARCHITECTURE.md`
- **Rule**: `../../.claude/commands/_assembly_first_rules.md`
- **Command Guide**: `ASSEMBLY_FIRST_COMMAND_GUIDE.md`
- **Integration Docs**:
  - `.claude/skills/Prototype_Components/ASSEMBLY_FIRST_INTEGRATION.md`
  - `.claude/skills/Prototype_Screens/ASSEMBLY_FIRST_INTEGRATION.md`
  - `.claude/skills/Prototype_Builder/ASSEMBLY_FIRST_INTEGRATION.md`
- **Commands**:
  - `.claude/commands/prototype.md`
  - `.claude/commands/prototype-components.md`
  - `.claude/commands/prototype-screens.md`
  - `.claude/commands/prototype-build.md`

---

## Conclusion

Assembly-First mode detection is **fully automatic** and requires **zero configuration**. The LLM:

1. ✅ Detects component library presence at Phase 0
2. ✅ Sets the mode boolean in config
3. ✅ Logs the decision for visibility
4. ✅ Phases 8, 9, 11-12 read config and branch accordingly
5. ✅ Validates mode compliance at checkpoints

**Result**: Users get optimized prototypes automatically when the component library is present, with seamless fallback to traditional mode when it's not.
