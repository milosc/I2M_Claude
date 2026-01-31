---
name: Verifying Traceability Structure
description: Use when called as a prerequisite by other skills that modify traceability files. Validates that the traceability backbone exists and files have valid schemas. Returns validation results and required user actions if structure is invalid.
stage: Guard
version: 1.0.0
created_at: 2025-12-23
skill_type: Guard
triggers:
  - Before any skill modifies files in traceability/
  - Called explicitly by /traceability-status
outputs:
  - validation_result: { valid: boolean, missing_files: string[], schema_errors: string[], user_action_required: string }
implements: VERSION_CONTROL_STANDARD.md
---

# Verifying Traceability Structure

## Purpose

This guard skill is invoked **before** any skill attempts to modify files in the `traceability/` folder. It ensures the backbone structure exists and is valid, preventing runtime failures and data corruption.

## When Called

This skill MUST be invoked (as stated in `.claude/rules/traceability-guard.md`) when:
- Any skill needs to read from or write to `traceability/*.json`
- Running `/discovery`, `/prototype`, `/productspecs`, `/solarch` commands
- Running `/traceability-status` command

## Procedure

### 1. Check Folder Existence

```
IF traceability/ folder does not exist:
  RETURN {
    valid: false,
    missing_files: ["traceability/"],
    schema_errors: [],
    user_action_required: "Traceability backbone not initialized. Run `/traceability-init {SystemName}` first."
  }
```

### 2. Check Required Files

Load the schema index from `.claude/templates/traceability/schemas/_schema_index.json` and verify each required file exists:

```
FOR EACH registry in schema_index.registries.*:
  IF registry.required == true:
    target_file = registry.file.replace('{{SYSTEM_NAME}}', system_name)
    IF file traceability/{target_file} does not exist:
      ADD to missing_files
```

Required files at minimum:
- `client_facts_registry.json`
- `pain_point_registry.json`
- `jtbd_registry.json`
- `user_type_registry.json`
- `requirements_registry.json`
- `screen_registry.json`
- `trace_links.json`
- `traceability_matrix_master.json`

### 3. Validate Schema Structure

For each existing file, verify:

```
FOR EACH file in traceability/*.json:
  PARSE as JSON
  IF parse fails:
    ADD to schema_errors: "{file}: Invalid JSON"
  ELSE IF file.$documentation is missing:
    ADD to schema_errors: "{file}: Missing $documentation block"
  ELSE IF file.$documentation.purpose is missing:
    ADD to schema_errors: "{file}: $documentation missing 'purpose' field"
```

### 4. Check Schema Version Compatibility

```
IF file.schema_version exists:
  IF file.schema_version < minimum_supported_version:
    ADD to schema_errors: "{file}: Outdated schema version {version}. Run `/traceability-init --repair`"
```

### 5. Return Result

```
IF missing_files.length > 0:
  RETURN {
    valid: false,
    missing_files: missing_files,
    schema_errors: schema_errors,
    user_action_required: "Missing required files. Run `/traceability-init --repair` to restore them."
  }

ELSE IF schema_errors.length > 0 AND any error is critical:
  RETURN {
    valid: false,
    missing_files: [],
    schema_errors: schema_errors,
    user_action_required: "Schema validation failed. Run `/traceability-init --repair` to fix structure."
  }

ELSE:
  RETURN {
    valid: true,
    missing_files: [],
    schema_errors: schema_errors,  // May contain warnings
    user_action_required: null
  }
```

## Output Format

```json
{
  "valid": true,
  "missing_files": [],
  "schema_errors": [],
  "user_action_required": null,
  "checked_at": "2025-12-23T07:35:00Z",
  "files_checked": 18,
  "schema_version": "1.0.0"
}
```

## Error Responses

When `valid: false`, the calling skill MUST:

1. **Log the validation result** for debugging
2. **Stop execution** - do not proceed with file modifications
3. **Return to user** with the `user_action_required` message

Example user-facing message:
```
⚠️ Traceability Guard Failed

The traceability backbone is not properly initialized.

Missing files:
- pain_point_registry.json
- jtbd_registry.json

Please run: /traceability-init --repair

Then retry your command.
```

## Integration with Other Skills

Skills that modify traceability files should include in their Prerequisites section:

```markdown
## Prerequisites

1. **Traceability Guard**: This skill invokes `Traceability_Guard` before execution.
   If the guard fails, execution stops with guidance to run `/traceability-init`.
```

## Related

- **Rule**: `.claude/rules/traceability-guard.md` - Global rule enforcing guard invocation
- **Skill**: `Traceability_Initializer.md` - Creates/repairs the backbone
- **Command**: `/traceability-status` - User-facing status check
- **Templates**: `.claude/templates/traceability/` - Source templates
