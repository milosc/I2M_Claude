---
name: specifying-data-models
description: Use when you need to transform specifications into complete data models including entity schemas, relationships, constraints, and dictionaries.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill specifying-data-models started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill specifying-data-models ended '{"stage": "prototype"}'
---
---
name: specifying-data-models
description: Use when you need to transform specifications into complete data models including entity schemas, relationships, constraints, and dictionaries.
model: sonnet
allowed-tools: Read, Write, Edit

# Spec Data Models

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill specifying-data-models instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_DataModel
- **Version**: 1.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v1.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v1.0.0 (2025-01-15): Initial skill version

## Description
Generate entity schemas, relationships, constraints, and data dictionaries. Creates complete data model with JSON schemas, ERD, validation rules, and IndexedDB configuration.

Transform discovery data specifications into a complete data model. Generates structured output following the OUTPUT_STRUCTURE.md specification.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: Entity names shown below (e.g., "Candidate", "Position", "Application") are examples from an ATS domain. Your actual entities, fields, and relationships should be derived from your project's discovery documents.

---

## Output Structure (REQUIRED)

This skill MUST generate the following structure pattern:

```
00-foundation/data-model/
├── constraints/
│   ├── referential-integrity.md      # FK relationships and cascade rules
│   └── validation-rules.md           # Field validation specifications
├── DATA_MODEL.md                     # Overview and conventions
├── dictionaries/
│   ├── data-dictionary.md            # Field definitions and descriptions
│   └── enum-values.md                # All enumeration values with transitions
├── entities/
│   ├── ActivityLog.schema.json
│   ├── Application.schema.json
│   ├── ApplicationStageHistory.schema.json
│   ├── AvailabilitySlot.schema.json
│   ├── Candidate.schema.json
│   ├── Department.schema.json
│   ├── Document.schema.json
│   ├── Interview.schema.json
│   ├── InterviewFeedback.schema.json
│   ├── Message.schema.json
│   ├── PipelineTemplate.schema.json
│   ├── Position.schema.json
│   ├── Role.schema.json
│   ├── Skill.schema.json
│   └── User.schema.json
├── ENTITY_INDEX.md                   # Entity listing with relationships
├── generate_detailed_files.py        # Schema generation script
└── relationships/
    └── ERD.puml                      # PlantUML ERD diagram
```

State file:
```
_state/data_model.json                # Machine-readable entity registry (with version metadata)
```

### Version Control for data_model.json

The `_state/data_model.json` MUST include version metadata:

```json
{
  "$schema": "data-model-registry-v1",
  "$metadata": {
    "document_id": "REG-DATAMODEL-001",
    "version": "1.0.0",
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
    "generated_by": "Prototype_DataModel",
    "source_files": [
      "_state/discovery_summary.json",
      "discovery/04-design-specs/data-fields.md"
    ],
    "change_history": [
      {
        "version": "1.0.0",
        "date": "YYYY-MM-DD",
        "author": "Prototype_DataModel",
        "changes": "Initial data model generation"
      }
    ]
  },
  "entities": [...]
}
```

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ _state/discovery_summary.json → entity list
READ _state/requirements_registry.json → data-related requirements
READ discovery/04-design-specs/data-fields.md → field definitions

IDENTIFY requirements this skill MUST address:
  - FR-XXX related to data storage/retrieval
  - US-XXX that involve entity operations
  
IF discovery_summary missing:
  BLOCK: "Run ValidateDiscovery first"
  
IF requirements_registry missing:
  BLOCK: "Run Requirements first"
  
IF data-fields.md missing or empty:
  ═══════════════════════════════════════════
  ⚠️ INPUT VALIDATION FAILED
  ═══════════════════════════════════════════
  
  Cannot generate data model:
  • data-fields.md is missing or empty
  
  How would you like to proceed?
  1. "provide: [path]" - Point to alternate data spec
  2. "generate minimal" - Create basic entities from screens
  3. "abort" - Stop and create data-fields.md
  ═══════════════════════════════════════════
  
  WAIT for user response
```

### Step 2: Classify Entities
```
FOR each entity in discovery:
  CLASSIFY as:
    catalog   → reference data, rarely changes, ≤100 records
    core      → primary business objects, moderate volume
    transactional → events/actions, high volume, has timestamps
    junction  → M:N relationship tables
    audit     → system tracking, append-only
    
  RECORD classification for ENTITY_INDEX.md
```

### Step 3: Define Fields for Each Entity
```
FOR each entity:
  ADD standard fields:
    - id (uuid, primary key)
    - createdAt (timestamp)
    - updatedAt (timestamp)
  
  FOR each field in data-fields.md:
    DETERMINE type (string, number, boolean, date, enum, fk)
    SET constraints (required, unique, indexed)
    
    IF enum type:
      DEFINE enum values with transitions
      RECORD in enum-values.md
      
    IF foreign key:
      SPECIFY target entity
      RECORD in referential-integrity.md
    
    RECORD field in data-dictionary.md
```

### Step 4: Generate Entity Schemas
```
FOR each entity:
  CREATE {Entity}.schema.json:
    {
      "$schema": "http://json-schema.org/draft-07/schema#",
      "$id": "{Entity}.schema.json",
      "title": "{Entity}",
      "description": "...",
      "type": "object",
      "classification": "catalog|core|transactional",
      
      "requirements_addressed": [
        "FR-XXX: Description",
        "US-XXX: Description"
      ],
      
      "properties": {
        "id": { "type": "string", "format": "uuid" },
        "createdAt": { "type": "string", "format": "date-time" },
        "updatedAt": { "type": "string", "format": "date-time" },
        // ... entity-specific fields
      },
      
      "required": ["id", "createdAt", "updatedAt", ...],
      
      "indexes": [
        { "fields": ["fieldName"], "unique": false }
      ],
      
      "relationships": [
        {
          "field": "positionId",
          "target": "Position",
          "type": "many-to-one",
          "onDelete": "CASCADE|SET_NULL|RESTRICT"
        }
      ]
    }
  
  WRITE to 00-foundation/data-model/entities/{Entity}.schema.json
```

### Step 5: Generate ERD

#### 5a: Generate PlantUML ERD
```
CREATE ERD.puml:
  @startuml
  skinparam linetype ortho

  ' Catalog entities
  entity "Department" as dept {
    *id : uuid
    --
    name : string
    code : string
  }

  ' Core entities
  entity "Candidate" as cand {
    *id : uuid
    --
    firstName : string
    lastName : string
    email : string
  }

  ' Relationships
  cand }o--|| dept : department

  @enduml

WRITE to 00-foundation/data-model/relationships/ERD.puml
```

#### 5b: Generate Interactive HTML ERD (Visual Documentation Enhancement)

> **Phase 2 Enhancement**: Generate interactive HTML diagram for visual documentation.

```
CREATE 00-foundation/data-model/ERD_VISUAL.html:

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Product Name} - Data Model ERD</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: system-ui, -apple-system, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 40px;
    }
    .container { max-width: 1400px; margin: 0 auto; }
    h1 {
      color: white;
      font-size: 2.5rem;
      margin-bottom: 10px;
    }
    .subtitle {
      color: rgba(255,255,255,0.8);
      margin-bottom: 30px;
    }
    .erd-canvas {
      background: white;
      border-radius: 16px;
      padding: 40px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    .legend {
      display: flex;
      gap: 20px;
      margin-bottom: 30px;
      flex-wrap: wrap;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
    }
    .legend-color {
      width: 16px;
      height: 16px;
      border-radius: 4px;
    }
    .catalog { background: #4299e1; }
    .core { background: #48bb78; }
    .transactional { background: #ed8936; }
    .junction { background: #9f7aea; }

    svg { width: 100%; height: auto; }

    .entity {
      cursor: pointer;
      transition: transform 0.2s, filter 0.2s;
    }
    .entity:hover {
      transform: scale(1.02);
      filter: drop-shadow(0 4px 12px rgba(0,0,0,0.2));
    }
    .entity-header {
      font-weight: 600;
      font-size: 14px;
    }
    .entity-field {
      font-size: 12px;
      fill: #4a5568;
    }
    .relationship-line {
      stroke: #a0aec0;
      stroke-width: 2;
      fill: none;
    }
    .relationship-label {
      font-size: 10px;
      fill: #718096;
    }

    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 20px;
      margin-top: 30px;
    }
    .stat-card {
      background: #f7fafc;
      padding: 20px;
      border-radius: 8px;
      text-align: center;
    }
    .stat-value {
      font-size: 2rem;
      font-weight: 700;
      color: #2d3748;
    }
    .stat-label {
      font-size: 14px;
      color: #718096;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>{Product Name} Data Model</h1>
    <p class="subtitle">Entity Relationship Diagram • {entity_count} Entities • {relationship_count} Relationships</p>

    <div class="erd-canvas">
      <div class="legend">
        <div class="legend-item">
          <div class="legend-color catalog"></div>
          <span>Catalog (Reference Data)</span>
        </div>
        <div class="legend-item">
          <div class="legend-color core"></div>
          <span>Core (Primary Entities)</span>
        </div>
        <div class="legend-item">
          <div class="legend-color transactional"></div>
          <span>Transactional (Events)</span>
        </div>
        <div class="legend-item">
          <div class="legend-color junction"></div>
          <span>Junction (Many-to-Many)</span>
        </div>
      </div>

      <svg viewBox="0 0 1200 800">
        <defs>
          <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#a0aec0"/>
          </marker>
        </defs>

        <!-- Catalog Entities (Left Column) -->
        <g class="entity" transform="translate(50, 50)">
          <rect width="200" height="100" rx="8" fill="#4299e1"/>
          <text x="100" y="25" text-anchor="middle" class="entity-header" fill="white">{CatalogEntity1}</text>
          <rect x="10" y="35" width="180" height="55" rx="4" fill="white"/>
          <text x="20" y="55" class="entity-field">id: uuid (PK)</text>
          <text x="20" y="72" class="entity-field">name: string</text>
          <text x="20" y="89" class="entity-field">code: string</text>
        </g>

        <!-- Core Entities (Center Column) -->
        <g class="entity" transform="translate(500, 50)">
          <rect width="200" height="140" rx="8" fill="#48bb78"/>
          <text x="100" y="25" text-anchor="middle" class="entity-header" fill="white">{CoreEntity1}</text>
          <rect x="10" y="35" width="180" height="95" rx="4" fill="white"/>
          <text x="20" y="55" class="entity-field">id: uuid (PK)</text>
          <text x="20" y="72" class="entity-field">firstName: string</text>
          <text x="20" y="89" class="entity-field">lastName: string</text>
          <text x="20" y="106" class="entity-field">email: string</text>
          <text x="20" y="123" class="entity-field">status: enum</text>
        </g>

        <!-- Transactional Entities (Right Column) -->
        <g class="entity" transform="translate(900, 200)">
          <rect width="200" height="120" rx="8" fill="#ed8936"/>
          <text x="100" y="25" text-anchor="middle" class="entity-header" fill="white">{TransactionalEntity1}</text>
          <rect x="10" y="35" width="180" height="75" rx="4" fill="white"/>
          <text x="20" y="55" class="entity-field">id: uuid (PK)</text>
          <text x="20" y="72" class="entity-field">candidateId: uuid (FK)</text>
          <text x="20" y="89" class="entity-field">positionId: uuid (FK)</text>
          <text x="20" y="106" class="entity-field">status: enum</text>
        </g>

        <!-- Relationship Lines -->
        <path class="relationship-line" d="M250,100 L500,100" marker-end="url(#arrow)"/>
        <text x="375" y="90" class="relationship-label">belongs_to</text>

        <path class="relationship-line" d="M700,120 L900,220" marker-end="url(#arrow)"/>
        <text x="800" y="160" class="relationship-label">has_many</text>

        <!-- Add more entities and relationships dynamically -->
      </svg>

      <div class="stats">
        <div class="stat-card">
          <div class="stat-value">{catalog_count}</div>
          <div class="stat-label">Catalog Entities</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{core_count}</div>
          <div class="stat-label">Core Entities</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{transactional_count}</div>
          <div class="stat-label">Transactional</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{relationship_count}</div>
          <div class="stat-label">Relationships</div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>

POPULATE template with actual entities from data model
WRITE to 00-foundation/data-model/ERD_VISUAL.html

LOG: "✅ Generated interactive ERD visualization"
```

### Step 6: Generate Data Dictionary
```
CREATE data-dictionary.md:
  # Data Dictionary
  
  ## Candidate
  | Field | Type | Required | Description | Example |
  |-------|------|----------|-------------|---------|
  | id | uuid | Yes | Unique identifier | "abc-123" |
  | firstName | string | Yes | Legal first name | "John" |
  
  [... all entities ...]

WRITE to 00-foundation/data-model/dictionaries/data-dictionary.md
```

### Step 7: Generate Enum Values
```
CREATE enum-values.md:
  # Enumeration Values
  
  ## ApplicationStatus
  | Value | Display | Description | Transitions To |
  |-------|---------|-------------|----------------|
  | new | New | Just received | screening, rejected |
  | screening | Screening | Under review | interview, rejected |
  
  [... all enums ...]

WRITE to 00-foundation/data-model/dictionaries/enum-values.md
```

### Step 8: Generate Constraints
```
CREATE referential-integrity.md:
  # Referential Integrity Constraints
  
  ## Foreign Key Relationships
  | Source | Field | Target | On Delete |
  |--------|-------|--------|-----------|
  | Application | candidateId | Candidate | CASCADE |
  | Application | positionId | Position | RESTRICT |
  
  ## Cascade Rules
  - Deleting Candidate cascades to Applications, Documents
  - Deleting Position restricts if Applications exist

WRITE to 00-foundation/data-model/constraints/referential-integrity.md

CREATE validation-rules.md:
  # Validation Rules
  
  ## Candidate
  | Field | Validation | Error Message |
  |-------|------------|---------------|
  | email | format: email | "Invalid email format" |
  | phone | pattern: /^\+?[\d\s-]+$/ | "Invalid phone number" |

WRITE to 00-foundation/data-model/constraints/validation-rules.md
```

### Step 9: Generate Summary Files
```
CREATE DATA_MODEL.md:
  # Data Model Overview
  
  ## Entity Classification
  | Classification | Count | Examples |
  |----------------|-------|----------|
  | Catalog | 4 | Department, Role, Skill |
  | Core | 4 | Candidate, Position, User |
  | Transactional | 5 | Application, Interview |
  
  ## Quick Reference
  [links to all sections]

WRITE to 00-foundation/data-model/DATA_MODEL.md

CREATE ENTITY_INDEX.md:
  # Entity Index
  
  | Entity | Classification | Fields | Relationships | Requirements |
  |--------|----------------|--------|---------------|--------------|
  | Candidate | Core | 12 | 3 | FR-003, US-001 |
  
  [... all entities ...]

WRITE to 00-foundation/data-model/ENTITY_INDEX.md
```

### Step 10: Generate Helper Script
```
CREATE generate_detailed_files.py:
  """
  Generate detailed data model files from schema definitions.
  Run: python generate_detailed_files.py
  """
  import json
  import os
  
  # Script to regenerate files from schemas
  ...

WRITE to 00-foundation/data-model/generate_detailed_files.py
```

### Step 11: Link to Requirements (TRACEABILITY)
```
READ _state/requirements_registry.json

FOR each entity:
  FIND requirements that mention this entity
  ADD to entity.requirements_addressed[]
  
  UPDATE requirements_registry.json:
    FOR each linked requirement:
      ADD "data_model: [entity]" to requirement.addressed_by[]
```

### Step 12: Validate Outputs (REQUIRED)
```
VALIDATE output structure:
  CHECKS:
    - 00-foundation/data-model/ directory exists
    - DATA_MODEL.md exists and not empty
    - ENTITY_INDEX.md exists and not empty
    - entities/ contains all entity schemas
    - Each schema has requirements_addressed
    - ERD.puml contains all entities
    - data-dictionary.md covers all fields
    - enum-values.md covers all enums
    - referential-integrity.md covers all FKs
    
IF any validation fails:
  ═══════════════════════════════════════════
  ⚠️ OUTPUT VALIDATION FAILED
  ═══════════════════════════════════════════
  
  Missing or incomplete outputs:
  • [list specific failures]
  
  How would you like to proceed?
  1. "fix: [file]" - Regenerate specific file
  2. "regenerate" - Re-run full generation
  3. "continue anyway" - Proceed with warnings
  ═══════════════════════════════════════════
  
  WAIT for user response
```

### Step 13: Update Progress
```
WRITE _state/data_model.json (machine-readable registry)

UPDATE _state/progress.json:
  phases.data_model.status = "complete"
  phases.data_model.completed_at = timestamp
  phases.data_model.outputs = [
    "00-foundation/data-model/DATA_MODEL.md",
    "00-foundation/data-model/ENTITY_INDEX.md",
    "00-foundation/data-model/entities/*.schema.json",
    "00-foundation/data-model/dictionaries/data-dictionary.md",
    "00-foundation/data-model/dictionaries/enum-values.md",
    "00-foundation/data-model/constraints/referential-integrity.md",
    "00-foundation/data-model/constraints/validation-rules.md",
    "00-foundation/data-model/relationships/ERD.puml",
    "00-foundation/data-model/generate_detailed_files.py"
  ]
  phases.data_model.validation = {
    status: "passed",
    checks_run: 9,
    checks_passed: 9
  }
  phases.data_model.metrics = {
    entity_count: count,
    catalog_count: count,
    core_count: count,
    transactional_count: count,
    field_count: count,
    relationship_count: count,
    enum_count: count,
    requirements_linked: count
  }
```

---

## Input Requirements

| Input | Required | Used For |
|-------|----------|----------|
| discovery_summary.json | ✅ Yes | Entity list |
| requirements_registry.json | ✅ Yes | Traceability |
| data-fields.md | ✅ Yes | Field definitions |

---

## Output Files (REQUIRED)

| File | Purpose | Blocking? |
|------|---------|-----------|
| `DATA_MODEL.md` | Overview document | ✅ Yes |
| `ENTITY_INDEX.md` | Entity listing | ✅ Yes |
| `entities/*.schema.json` | Per-entity schemas | ✅ Yes |
| `dictionaries/data-dictionary.md` | Field definitions | ✅ Yes |
| `dictionaries/enum-values.md` | Enum values | ✅ Yes |
| `constraints/referential-integrity.md` | FK rules | ✅ Yes |
| `constraints/validation-rules.md` | Validation | ⚠️ Warning |
| `relationships/ERD.puml` | ERD diagram | ✅ Yes |
| `generate_detailed_files.py` | Helper script | ⚠️ Warning |

---

## User Mitigation Options

| Response | Action |
|----------|--------|
| `fix: [file]` | Regenerate specific file |
| `add entity: [name]` | Add missing entity |
| `link: [entity] to [REQ-ID]` | Add requirement traceability |
| `regenerate` | Re-run full generation |
| `continue anyway` | Proceed with logged warnings |
| `abort` | Stop execution |

---

## Progress.json Update

```json
{
  "phases": {
    "data_model": {
      "status": "complete",
      "completed_at": "2024-12-13T10:30:00Z",
      "outputs": [
        "00-foundation/data-model/DATA_MODEL.md",
        "00-foundation/data-model/ENTITY_INDEX.md",
        "00-foundation/data-model/entities/*.schema.json",
        "00-foundation/data-model/dictionaries/data-dictionary.md",
        "00-foundation/data-model/dictionaries/enum-values.md",
        "00-foundation/data-model/constraints/referential-integrity.md",
        "00-foundation/data-model/constraints/validation-rules.md",
        "00-foundation/data-model/relationships/ERD.puml"
      ],
      "validation": {
        "status": "passed",
        "checks_run": 9,
        "checks_passed": 9
      },
      "metrics": {
        "entity_count": 15,
        "catalog_count": 4,
        "core_count": 5,
        "transactional_count": 6,
        "field_count": 127,
        "relationship_count": 18,
        "enum_count": 8,
        "requirements_linked": 23
      }
    }
  }
}
```
