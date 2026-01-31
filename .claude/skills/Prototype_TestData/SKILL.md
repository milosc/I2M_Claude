---
name: generating-prototype-test-data
description: Use when you need to generate realistic, interconnected test datasets (catalog, core, transactional) and persona-specific scenarios for a prototype.
model: sonnet
allowed-tools: AskUserQuestion, Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-prototype-test-data started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-prototype-test-data ended '{"stage": "prototype"}'
---

# Spec Test Data

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-prototype-test-data instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_TestData
- **Version**: 1.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v1.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v1.0.0 (2025-01-15): Initial skill version

## Description
Generate realistic, interconnected test data organized by category. Creates catalog, core, transactional data plus persona-specific views and scenarios.

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

Generate realistic test data with proper referential integrity. Follows OUTPUT_STRUCTURE.md for deterministic folder structure.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: Entity names, persona names, and scenario names shown below are examples from an ATS domain. Your actual entities, personas, and scenarios should be derived from your project's data model and discovery documents.

## Output Structure (REQUIRED)

This skill MUST generate the following structure pattern:

```
00-foundation/test-data/
├── datasets/
│   ├── catalog/                      # Reference/lookup data (low volume, static)
│   │   └── {lookup-entity}.json      # e.g., departments.json, categories.json
│   ├── combined/
│   │   └── full-dataset.json         # All data combined for seeding
│   ├── core/                         # Primary business entities
│   │   └── {core-entity}.json        # e.g., users.json, products.json
│   ├── transactional/                # Events and activities
│   │   └── {activity-entity}.json    # e.g., orders.json, messages.json
│   ├── personas/                     # Filtered views per user role
│   │   └── {persona-name}/
│   │       └── {view}.json
│   └── scenarios/                    # End-to-end user journeys
│       └── {scenario-name}.json
├── personas/                         # Persona definitions
│   └── {persona-name}/
│       └── profile.json
├── scenarios/                        # Scenario definitions
│   └── {scenario-name}.md
├── generate_test_data.py
├── generate_persona_views.py
└── TEST_DATA_README.md
```

State file:
```
_state/test_data_manifest.json        # Data inventory and requirements mapping
```

---

## Data Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **catalog** | Reference/lookup data, rarely changes | Departments, roles, categories, statuses |
| **core** | Primary business entities | Users, products, customers, orders |
| **transactional** | Events and activities | Messages, logs, history records |
| **personas** | Per-user filtered views | What each persona sees |
| **scenarios** | Complete user journey data | End-to-end workflow examples |

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ _state/data_model.json → entities, relationships, enums
READ _state/api_contracts.json → expected data shapes
READ _state/requirements_registry.json → scenarios to support
READ _state/discovery_summary.json → personas

IDENTIFY requirements this skill MUST address:
  - P0 requirements that need data scenarios
  - US-XXX that require specific data states

IF data_model.json missing:
  BLOCK: "Run DataModel first"

EXTRACT from discovery:
  - Entity list from data model
  - Personas from user research
  - Key scenarios from requirements
```

### Step 1.5: Select Data Strategy (REQUIRED)

Determine the data approach for the prototype.

```
USE AskUserQuestion:
  question: "What data approach should the prototype use?"
  header: "Data"
  options:
    - label: "Mock Data (Recommended)"
      description: "JSON files, no backend needed, fast iteration"
    - label: "MSW (Mock Service Worker)"
      description: "Simulated API, realistic network behavior"
    - label: "Real API (if available)"
      description: "Connect to existing backend, requires credentials"

STORE selected strategy in _state/prototype_config.json:
  {
    "data_strategy": "{selected_option}",
    "data_strategy_rationale": "{option_description}"
  }
```

### Step 2: Generate Catalog Data
```
CREATE 00-foundation/test-data/datasets/catalog/:

FOR each catalog/reference entity in data model:
  CREATE {entity-name}.json:
    [
      { "id": "{entity}-001", "name": "...", ... },
      { "id": "{entity}-002", "name": "...", ... },
      // 5-20 records depending on entity type
    ]

EXAMPLES (ATS domain):
  - departments.json
  - roles.json
  - skills.json
  - pipeline-templates.json

EXAMPLES (E-commerce domain):
  - categories.json
  - shipping-methods.json
  - payment-types.json
```

### Step 3: Generate Core Entity Data
```
CREATE 00-foundation/test-data/datasets/core/:

FOR each core entity in data model:
  CREATE {entity-name}.json:
    [
      {
        "id": "{entity}-001",
        // All fields from entity schema
        "createdAt": "...",
        "updatedAt": "..."
      },
      // 10-50 records with varied states
    ]

ENSURE:
  - Referential integrity (FKs point to valid records)
  - Varied statuses (active, inactive, draft, etc.)
  - Realistic data distribution
  - Temporal consistency
```

### Step 4: Generate Transactional Data
```
CREATE 00-foundation/test-data/datasets/transactional/:

FOR each transactional entity in data model:
  CREATE {entity-name}.json:
    [
      {
        "id": "{entity}-001",
        // All fields from entity schema
        // Proper FK references
        "timestamp": "..."
      },
      // Volume based on entity type
    ]

ENSURE:
  - Temporal sequences make sense
  - Related records link properly
  - History records show progression
```

### Step 5: Generate Scenario Data
```
CREATE 00-foundation/test-data/datasets/scenarios/:

FOR each key user journey from requirements:
  CREATE {scenario-name}.json:
    {
      "$metadata": {
        "document_id": "DATA-SCENARIO-{NNN}",
        "version": "1.0.0",
        "created_at": "YYYY-MM-DDTHH:MM:SSZ",
        "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
        "generated_by": "Prototype_TestData",
        "source_files": [
          "_state/requirements_registry.json"
        ],
        "change_history": [
          {
            "version": "1.0.0",
            "date": "YYYY-MM-DD",
            "author": "Prototype_TestData",
            "changes": "Initial scenario data generation"
          }
        ]
      },
      "scenarioId": "{scenario-name}",
      "description": "...",
      "requirements_demonstrated": ["REQ-001", "REQ-002"],
      // Complete data for this journey
      "entities": {
        "{entity}": { ... },
        "{related-entity}": { ... }
      },
      "timeline": [
        { "date": "...", "event": "..." },
        // Chronological journey
      ]
    }

EXAMPLES:
  - successful-hire.json (ATS)
  - complete-purchase.json (E-commerce)
  - project-delivery.json (Project management)
```

### Step 6: Generate Persona Views
```
CREATE 00-foundation/test-data/datasets/personas/:

FOR each persona from discovery:
  CREATE {persona-name}/:
  
    CREATE dashboard.json:
      {
        "personaId": "{persona-name}",
        "metrics": { ... },
        "recentActivity": [ ... ],
        "upcoming": [ ... ]
      }
    
    CREATE {role-specific-view}.json:
      // Data filtered to what this persona sees
```

### Step 7: Generate Combined Dataset
```
CREATE 00-foundation/test-data/datasets/combined/full-dataset.json:
  {
    "$metadata": {
      "document_id": "DATA-FULL-001",
      "version": "1.0.0",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ",
      "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
      "generated_by": "Prototype_TestData",
      "source_files": [
        "_state/data_model.json",
        "_state/discovery_summary.json"
      ],
      "change_history": [
        {
          "version": "1.0.0",
          "date": "YYYY-MM-DD",
          "author": "Prototype_TestData",
          "changes": "Initial test data generation"
        }
      ]
    },
    "generated_at": "{timestamp}",
    "catalog": {
      // All catalog entities
    },
    "core": {
      // All core entities
    },
    "transactional": {
      // All transactional entities
    }
  }
```

### Step 8: Generate Persona Profiles
```
CREATE 00-foundation/test-data/personas/{persona-name}/profile.json:
  {
    "personaId": "{persona-name}",
    "name": "...",
    "role": "...",
    "responsibilities": [...],
    "pain_points": ["PP-001", ...],
    "daily_tasks": [...]
  }
```

### Step 9: Generate Helper Scripts
```
CREATE 00-foundation/test-data/generate_test_data.py
CREATE 00-foundation/test-data/generate_persona_views.py
```

### Step 10: Generate README
```
CREATE 00-foundation/test-data/TEST_DATA_README.md:
  # Test Data
  
  ## Overview
  ## Data Volume
  ## Scenarios
  ## Personas
  ## Usage
  ## Regenerating Data
```

### Step 11: Validate Outputs (REQUIRED)
```
VALIDATE test data:
  DIRECTORY CHECKS:
    - datasets/catalog/ has files for each catalog entity
    - datasets/core/ has files for each core entity
    - datasets/transactional/ has files for each transactional entity
    - datasets/personas/ has directory per persona
    - datasets/scenarios/ has ≥1 scenario
    - datasets/combined/full-dataset.json exists
    
  DATA CHECKS:
    - All FKs resolve to valid records
    - Temporal sequences are valid
    - Each persona has meaningful data
    - Each P0 requirement has supporting scenario
    
IF any validation fails:
  PROMPT with mitigation options
```

### Step 12: Update Progress
```
WRITE _state/test_data_manifest.json

UPDATE _state/progress.json:
  phases.test_data.status = "complete"
  phases.test_data.outputs = [...]
  phases.test_data.metrics = {
    total_records: count,
    catalog_records: count,
    core_records: count,
    transactional_records: count,
    scenarios: count,
    personas: count
  }
```

---

## Output Files (REQUIRED)

| Path | Purpose | Blocking? |
|------|---------|-----------|
| `datasets/catalog/*.json` | Reference data | ✅ Yes |
| `datasets/core/*.json` | Primary entities | ✅ Yes |
| `datasets/transactional/*.json` | Activity data | ✅ Yes |
| `datasets/personas/**/*.json` | Persona views | ✅ Yes |
| `datasets/scenarios/*.json` | Journey scenarios | ✅ Yes |
| `datasets/combined/full-dataset.json` | Combined data | ✅ Yes |
| `TEST_DATA_README.md` | Documentation | ⚠️ Warning |
| `generate_*.py` | Helper scripts | ⚠️ Warning |

---

## Progress.json Update

```json
{
  "phases": {
    "test_data": {
      "status": "complete",
      "completed_at": "...",
      "outputs": ["00-foundation/test-data/**/*.json"],
      "metrics": {
        "total_records": "...",
        "scenarios": "...",
        "personas": "..."
      }
    }
  }
}
```
