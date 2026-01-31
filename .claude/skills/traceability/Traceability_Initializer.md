---
name: Initializing Traceability Backbone
description: Use when setting up or repairing the traceability folder structure for a project. Creates all required JSON registries and markdown documentation from templates. Supports full initialization, repair mode (add missing without overwriting), and validation-only mode.
stage: Setup
version: 2.0.0
created_at: 2025-12-23
updated_at: 2025-12-25
skill_type: Initializer
inputs:
  - system_name: string (required for full mode)
  - mode: 'full' | 'repair' | 'validate' (default: 'full')
  - stages: string[] (optional, default: all stages)
outputs:
  - files_created: string[]
  - files_repaired: string[]
  - files_skipped: string[]
  - validation_errors: string[]
implements: VERSION_CONTROL_STANDARD.md
changelog:
  - "1.0.0 - Initial version with Discovery through SolArch stages"
  - "2.0.0 - Added Implementation stage (task_registry, review_registry, implementation_traceability_register), added _state/ folder initialization"
---

# Initializing Traceability Backbone

## Purpose

This skill creates the complete traceability folder structure from templates, ensuring a consistent and validated backbone for all projects. It also supports repairing damaged structures and updating `$documentation` in existing files.

## Modes

| Mode | Description |
|------|-------------|
| `full` | Create all files from templates. Fails if files exist (use --repair instead). |
| `repair` | Add missing files and update $documentation in existing files. Never overwrites data. |
| `validate` | Check structure validity without making changes. |

## Procedure

### 1. Load Schema Index

```
READ .claude/templates/traceability/schemas/_schema_index.json
EXTRACT all registry definitions grouped by stage
```

### 2. Determine Mode

```
IF mode == 'full':
  IF traceability/ exists AND has files:
    PROMPT: "Traceability folder already exists. Use --repair to add missing files without overwriting. Continue with full init? (This will overwrite existing files)"
    IF user declines: EXIT

IF mode == 'repair':
  IF traceability/ does not exist:
    SWITCH to 'full' mode (nothing to repair)

IF mode == 'validate':
  INVOKE Traceability_Guard
  RETURN guard results
```

### 3. Create Folder Structure

```
CREATE traceability/ IF NOT EXISTS
CREATE traceability/feedback_sessions/ IF NOT EXISTS
CREATE traceability/feedback_sessions/discovery/ IF NOT EXISTS
CREATE traceability/feedback_sessions/prototype/ IF NOT EXISTS
CREATE traceability/feedback_sessions/productspecs/ IF NOT EXISTS
CREATE traceability/feedback_sessions/solarch/ IF NOT EXISTS
CREATE traceability/feedback_sessions/implementation/ IF NOT EXISTS

CREATE _state/ IF NOT EXISTS
```

### 4. Process Each Registry

```
FOR EACH stage in ['discovery', 'prototype', 'productspecs', 'solarch', 'implementation', 'aggregation', 'feedback']:
  FOR EACH registry in schema_index.registries[stage]:

    target_file = registry.file.replace('{{SYSTEM_NAME}}', system_name)
    target_path = traceability/{target_file}
    template_path = .claude/templates/traceability/init/{registry.init}

    IF mode == 'full' OR target_path does not exist:
      READ template_path
      REPLACE {{SYSTEM_NAME}} with system_name
      REPLACE {{CREATED_AT}} with current ISO timestamp
      REPLACE {{UPDATED_AT}} with current ISO timestamp
      WRITE to target_path
      ADD to files_created

    ELSE IF mode == 'repair' AND target_path exists:
      READ existing file
      READ template

      IF existing file missing $documentation:
        COPY $documentation from template
        UPDATE updated_at timestamp
        WRITE back to target_path
        ADD to files_repaired

      ELSE IF existing.$documentation.purpose != template.$documentation.purpose:
        MERGE template.$documentation into existing.$documentation
        UPDATE updated_at timestamp
        WRITE back to target_path
        ADD to files_repaired

      ELSE:
        ADD to files_skipped
```

### 4a. Process State Files

```
FOR EACH state_file in schema_index.state_files.files:
  target_path = _state/{state_file.file}
  template_path = .claude/templates/_state/init/{state_file.file.replace('.json', '.init.json')}

  IF mode == 'full' OR target_path does not exist:
    IF template exists:
      READ template_path
      REPLACE {{SYSTEM_NAME}} with system_name
      REPLACE {{CREATED_AT}} with current ISO timestamp
      REPLACE {{UPDATED_AT}} with current ISO timestamp
      WRITE to target_path
      ADD to files_created
    ELSE:
      SKIP (state files are stage-specific, created by their stage commands)

  ELSE IF mode == 'repair' AND target_path exists:
    // State files are actively managed by stage commands
    // Only repair if $documentation is missing
    READ existing file
    IF existing file has $documentation AND it's outdated:
      UPDATE $documentation from template (if template exists)
      UPDATE updated_at timestamp
      WRITE back to target_path
      ADD to files_repaired
    ELSE:
      ADD to files_skipped
```

### 5. Process Markdown Files

```
FOR EACH md_file in schema_index.markdown_files:
  target_path = traceability/{md_file.file}
  template_path = .claude/templates/traceability/init/{md_file.init}
  
  IF mode == 'full' OR target_path does not exist:
    READ template_path
    REPLACE {{SYSTEM_NAME}} with system_name
    REPLACE {{CREATED_AT}} with current ISO timestamp
    WRITE to target_path
    ADD to files_created
```

### 6. Validate Result

```
INVOKE Traceability_Guard
IF guard.valid == false:
  REPORT validation_errors = guard.schema_errors
  LOG warning: "Initialization completed but validation failed"
```

### 7. Generate Report

```
OUTPUT:
  ✅ Traceability backbone initialized for {system_name}
  
  Files created: {files_created.length}
  - {file1}
  - {file2}
  ...
  
  Files repaired: {files_repaired.length}
  - {file1} (updated $documentation)
  ...
  
  Files skipped: {files_skipped.length}
  
  Validation: {PASSED/FAILED with N errors}
  
  Next steps:
  - Run /discovery to start client analysis
  - Run /traceability-status to check health
```

## Template Placeholders

| Placeholder | Replaced With |
|-------------|---------------|
| `{{SYSTEM_NAME}}` | User-provided system name |
| `{{CREATED_AT}}` | Current ISO 8601 timestamp |
| `{{UPDATED_AT}}` | Current ISO 8601 timestamp |

## Repair Mode Details

When in `--repair` mode, this skill:

1. **Never deletes data** - Only adds missing files or updates metadata
2. **Preserves items arrays** - Never touches actual content in `items`, `facts`, `pain_points`, etc.
3. **Updates $documentation** - Brings documentation in sync with latest templates
4. **Updates timestamps** - Sets `updated_at` to current time
5. **Adds missing fields** - Fills in any new schema fields with defaults

### $documentation Merge Strategy

```
FOR EACH field in template.$documentation:
  IF field NOT IN existing.$documentation:
    existing.$documentation[field] = template.$documentation[field]
  ELSE IF field == 'validation_rules' OR field == 'key_attributes':
    // Merge arrays/objects, prefer template values for new items
    MERGE template values into existing
```

## Error Handling

| Error | Action |
|-------|--------|
| Template file not found | FAIL with clear message about missing template |
| Permission denied | FAIL with instruction to check directory permissions |
| Invalid JSON in existing file | WARN and skip file, report in validation_errors |
| Schema version mismatch | WARN and suggest manual review |

## Stages and Registries

| Stage | Registries |
|-------|------------|
| Discovery | client_facts_registry, pain_point_registry, jtbd_registry, user_type_registry, discovery_traceability_register |
| Prototype | requirements_registry, screen_registry, prototype_traceability_register |
| ProductSpecs | module_registry, nfr_registry, epic_registry, user_story_registry, test_scenario_registry, test_case_registry, productspecs_traceability_register |
| SolArch | component_registry, adr_registry, solarch_traceability_register |
| Implementation | task_registry, review_registry, implementation_traceability_register |
| Aggregation | trace_links, traceability_matrix_master |
| Feedback | Per-stage feedback registers in feedback_sessions/ |

## Related

- **Skill**: `Traceability_Guard.md` - Validates structure before modifications
- **Command**: `/traceability-init` - User-facing command invoking this skill
- **Command**: `/traceability-status` - Check backbone health
- **Rule**: `traceability-guard.md` - Enforces guard invocation
- **Templates**: `.claude/templates/traceability/` - Traceability registry templates
- **Templates**: `.claude/templates/_state/` - State file templates
