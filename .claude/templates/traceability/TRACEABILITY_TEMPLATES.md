# Traceability Templates Documentation

> Single Source of Truth for Traceability Structure

## Overview

This folder contains the canonical templates for all traceability registry files. These templates are used by the `Traceability_Initializer` skill to create new project backbones and repair damaged structures.

## Folder Structure

```
.claude/templates/traceability/
├── TRACEABILITY_TEMPLATES.md    # This file
├── schemas/
│   └── _schema_index.json       # Master index of all registries
└── init/
    ├── client_facts_registry.init.json
    ├── pain_point_registry.init.json
    ├── jtbd_registry.init.json
    ├── user_type_registry.init.json
    ├── requirements_registry.init.json
    ├── screen_registry.init.json
    ├── module_registry.init.json
    ├── nfr_registry.init.json
    ├── component_registry.init.json
    ├── adr_registry.init.json
    ├── epic_registry.init.json
    ├── user_story_registry.init.json
    ├── test_scenario_registry.init.json
    ├── test_case_registry.init.json
    ├── trace_links.init.json
    ├── traceability_matrix_master.init.json
    ├── prototype_traceability_register.init.json
    ├── productspecs_traceability_register.init.json
    ├── solarch_traceability_register.init.json
    ├── discover_feedback_register.init.json
    └── README.init.md
```

## Template Placeholders

Each `.init.json` and `.init.md` file contains placeholders that are replaced during initialization:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{SYSTEM_NAME}}` | Project/system name | `InventorySystem` |
| `{{CREATED_AT}}` | ISO 8601 timestamp | `2025-12-23T07:35:00.000000` |
| `{{UPDATED_AT}}` | ISO 8601 timestamp | `2025-12-23T07:35:00.000000` |

## Schema Index

The `_schema_index.json` file is the master catalog. It defines:

- **registries**: Grouped by stage (discovery, prototype, productspecs, solarch, aggregation, feedback)
- **markdown_files**: Non-JSON documentation files
- **folders**: Required directory structure
- **validation**: Rules for validating file structure

### Registry Entry Format

```json
{
  "file": "pain_point_registry.json",
  "schema": "pain_point_registry.schema.json",
  "init": "pain_point_registry.init.json",
  "required": true,
  "stage": "Discovery",
  "description": "Validated pain points extracted from client facts"
}
```

## $documentation Block Standard

Every init template MUST include a `$documentation` block as the first property:

```json
{
  "$documentation": {
    "purpose": "Human-readable description of what this file does",
    "stage": "Discovery|Prototype|ProductSpecs|SolutionArchitecture|Cross-cutting",
    "phase_position": "Where in the chain this file sits",
    "upstream": ["files that feed into this one"],
    "downstream": ["files that consume this one"],
    "commands": ["/command-that-updates-this"],
    "skills": ["Skills_That_Modify_This"],
    "id_pattern": {
      "format": "XX-{NNN}",
      "example": "PP-1.1"
    },
    "key_attributes": {
      "field.path": "Description of field"
    },
    "validation_rules": [
      "Rules that must be followed"
    ]
  },
  // ... rest of template
}
```

## Adding New Registry Types

To add a new registry type:

1. **Create schema in `schemas/`** (optional, for strict validation)
2. **Create init template in `init/`**
   - Include full `$documentation` block
   - Use placeholders for dynamic values
   - Include empty `items` array
   - Include `summary` section
3. **Update `_schema_index.json`**
   - Add entry to appropriate stage group
   - Set `required` appropriately
4. **Update `README.init.md`** to list new file
5. **Update `Traceability_Guard.md`** if file is required

## Versioning

- Schema version in `_schema_index.json`: `1.0.0`
- Each template has its own `schema_version` field
- When updating templates, increment version and document changes

## Usage

### Initialize New Project
```
/traceability-init MyProject
```

### Repair Existing Project
```
/traceability-init --repair
```

### Validate Structure
```
/traceability-status
```

## Related

- **Skill**: `.claude/skills/traceability/Traceability_Initializer.md`
- **Skill**: `.claude/skills/traceability/Traceability_Guard.md`
- **Rule**: `.claude/rules/traceability-guard.md`
- **Command**: `/traceability-init`
- **Command**: `/traceability-status`
