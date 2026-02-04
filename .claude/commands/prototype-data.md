---
name: prototype-data
description: Generate data models from discovery specifications
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-data started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: |
            SYSTEM_NAME=$(cat _state/session.json 2>/dev/null | grep -o '"project"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"project"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//' || echo "")
            if [ -n "$SYSTEM_NAME" ] && [ "$SYSTEM_NAME" != "pending" ]; then
              uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_prototype_output.py" --system-name "$SYSTEM_NAME" --phase test_data
            else
              echo '{"result": "skip", "reason": "System name not found in session"}'
              exit 0
            fi
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-data ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-data instruction_start '{"stage": "prototype", "method": "instruction-based"}'
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

- Phase 2 completed: `_state/requirements_registry.json` exists
- Checkpoint 2 passed

## Skills Used

Read BEFORE execution:
- `.claude/skills/Prototype_DataModel/SKILL.md` (Phase 3)
- `.claude/skills/Prototype_ApiContracts/SKILL.md` (Phase 4)
- `.claude/skills/Prototype_TestData/SKILL.md` (Phase 5)

## Execution Flow

---

---

### Phase 3: Data Model (Checkpoint 3)

#### Step 3.1: Load Inputs

Read:
- `_state/requirements_registry.json`
- `_state/discovery_summary.json` (for data_entities)
- `ClientAnalysis_<SystemName>/04-design-specs/data-fields.md`

#### Step 3.2: Update Progress

```json
{
  "current_phase": 3,
  "phases": {
    "data_model": {
      "status": "in_progress",
      "started_at": "<timestamp>"
    }
  }
}
```

#### Step 3.3: Execute Prototype_DataModel Skill

1. **Define Entities**:
   - Extract from data-fields.md
   - Map to requirements

2. **Define Relationships**:
   - One-to-many, many-to-many
   - Foreign key constraints

3. **Define Constraints**:
   - Required fields
   - Validation rules
   - Business logic constraints

#### Step 3.4: Generate Data Model

Create nested structure in `00-foundation/data-model/`:

```
00-foundation/data-model/
├── DATA_MODEL_SUMMARY.md          # Executive summary
├── entities/                       # One file per entity
│   ├── inventory-item.md
│   ├── location.md
│   ├── transaction-log.md
│   └── user.md
├── dictionaries/                   # Data dictionaries
│   ├── field-dictionary.md
│   └── enum-dictionary.md
├── constraints/                    # Business rules
│   ├── validation-rules.md
│   └── referential-integrity.md
└── relationships.md                # ERD and relationships
```

**DATA_MODEL_SUMMARY.md:**

```markdown
# Data Model Summary

## Overview

| Metric | Value |
|--------|-------|
| Total Entities | 8 |
| Relationships | 12 |
| Business Rules | 15 |
| Fields | 64 |

## Entity Inventory

| Entity | Fields | Relationships | Source |
|--------|--------|---------------|--------|
| InventoryItem | 12 | 3 | data-fields.md |
| Location | 8 | 2 | data-fields.md |
| TransactionLog | 10 | 2 | inferred |
| User | 9 | 1 | PERSONA_* |
```

**entities/inventory-item.md:**

```markdown
# Entity: InventoryItem

## Requirements Addressed

| Requirement | Description |
|-------------|-------------|
| US-003 | View inventory items |
| US-004 | Search inventory |
| FR-008 | Track stock levels |

## Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | Yes | Unique identifier |
| sku | String | Yes | Stock keeping unit |
| name | String | Yes | Item name |
| quantity | Integer | Yes | Current stock level |
| location_id | UUID | Yes | FK to Location |
| updated_at | DateTime | Yes | Last update timestamp |

## Relationships

- belongs_to: Location (via location_id)
- has_many: TransactionLog (via item_id)

## Constraints

- quantity >= 0
- sku must be unique within location
- name max length: 255 characters
```

**relationships.md:**

```markdown
# Entity Relationships

## ERD

\`\`\`mermaid
erDiagram
    InventoryItem ||--o{ TransactionLog : has
    Location ||--o{ InventoryItem : contains
    User ||--o{ TransactionLog : creates
\`\`\`

## Relationship Details

| Parent | Child | Type | FK Field |
|--------|-------|------|----------|
| Location | InventoryItem | 1:N | location_id |
| InventoryItem | TransactionLog | 1:N | item_id |
| User | TransactionLog | 1:N | user_id |
```

#### Step 3.5: Validate Checkpoint 3

```bash
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 3 --dir Prototype_<SystemName>/
```

#### Step 3.6: Update Progress

Mark phase 3 completed, move to phase 4.

---

### Phase 4: API Contracts (Checkpoint 4)

#### Step 4.1: Update Progress

```json
{
  "current_phase": 4,
  "phases": {
    "api_contracts": {
      "status": "in_progress",
      "started_at": "<timestamp>"
    }
  }
}
```

#### Step 4.2: Execute Prototype_ApiContracts Skill

1. **Define Endpoints**:
   - CRUD operations per entity
   - Business operation endpoints
   - Map to requirements

2. **Define Request/Response Schemas**:
   - Based on data model
   - Include validation rules

3. **Define Error Responses**:
   - Standard error format
   - Error codes

#### Step 4.3: Generate API Contracts

Create nested structure in `00-foundation/api-contracts/`:

```
00-foundation/api-contracts/
├── API_CONTRACTS_SUMMARY.md       # Executive summary
├── openapi.json                    # Full OpenAPI spec
├── endpoints/                      # One file per resource
│   ├── inventory.md
│   ├── locations.md
│   ├── transactions.md
│   └── users.md
├── examples/                       # Request/response examples
│   ├── inventory-examples.json
│   └── transaction-examples.json
└── mocks/                          # Mock server config
    └── handlers.json
```

**API_CONTRACTS_SUMMARY.md:**

```markdown
# API Contracts Summary

## Overview

| Metric | Value |
|--------|-------|
| Total Endpoints | 24 |
| Resources | 4 |
| Requirements Covered | 18 |
| Authentication | Bearer Token |

## Endpoint Inventory

| Resource | GET | POST | PUT | DELETE | Total |
|----------|-----|------|-----|--------|-------|
| /api/inventory | ✅ | ✅ | ✅ | ✅ | 4 |
| /api/locations | ✅ | ✅ | ✅ | ❌ | 3 |
| /api/transactions | ✅ | ✅ | ❌ | ❌ | 2 |
| /api/users | ✅ | ❌ | ✅ | ❌ | 2 |

## Requirements to Endpoint Mapping

| Requirement | Endpoint | Method |
|-------------|----------|--------|
| US-003 | /api/inventory | GET |
| US-004 | /api/inventory/:id | GET |
| US-007 | /api/transactions | POST |
```

**endpoints/inventory.md:**

```markdown
# Inventory API Endpoints

## Requirements Addressed

| Requirement | Description |
|-------------|-------------|
| US-003 | View inventory items |
| US-004 | Search inventory |
| US-006 | Update inventory |

## GET /api/inventory

**Purpose:** List all inventory items with filtering

**Parameters:**

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| location_id | query | string | No | Filter by location |
| search | query | string | No | Search term |
| page | query | integer | No | Page number |
| limit | query | integer | No | Items per page |

**Response 200:**

\`\`\`json
{
  "data": [
    {
      "id": "uuid",
      "sku": "WH-001-A",
      "name": "Widget Type A",
      "quantity": 150,
      "location_id": "loc-001"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
\`\`\`
```

#### Step 4.4: Validate Checkpoint 4

```bash
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 4 --dir Prototype_<SystemName>/
```

#### Step 4.5: Update Progress

Mark phase 4 completed, move to phase 5.

---

### Phase 5: Test Data (Checkpoint 5)

#### Step 5.1: Update Progress

```json
{
  "current_phase": 5,
  "phases": {
    "test_data": {
      "status": "in_progress",
      "started_at": "<timestamp>"
    }
  }
}
```

#### Step 5.2: Execute Prototype_TestData Skill

1. **Generate Catalog Data** (static reference):
   - Locations
   - Categories
   - Statuses

2. **Generate Core Data** (primary entities):
   - Inventory items
   - Users
   - Roles

3. **Generate Transactional Data** (operations):
   - Stock movements
   - Audit logs

4. **Generate Persona Scenarios**:
   - Realistic data for each persona's workflows
   - Edge cases

#### Step 5.3: Generate Test Data Files

Create nested structure in `00-foundation/test-data/`:

```
00-foundation/test-data/
├── TEST_DATA_SUMMARY.md            # Executive summary
├── datasets/
│   ├── catalog/                     # Static reference data
│   │   ├── locations.json
│   │   ├── categories.json
│   │   └── statuses.json
│   ├── core/                        # Primary entities
│   │   ├── inventory-items.json
│   │   ├── users.json
│   │   └── roles.json
│   ├── junction/                    # Relationship data
│   │   └── user-locations.json
│   ├── transactional/               # Operations
│   │   ├── stock-movements.json
│   │   └── audit-logs.json
│   ├── personas/                    # Persona-specific data
│   │   ├── warehouse-operator-data.json
│   │   └── supervisor-data.json
│   ├── scenarios/                   # User flow scenarios
│   │   ├── warehouse-operator-day.json
│   │   └── supervisor-audit.json
│   └── combined/                    # Merged datasets
│       └── full-demo-data.json
└── personas/                        # Persona narratives
    ├── PERSONA_WAREHOUSE_OPERATOR.md
    └── PERSONA_SUPERVISOR.md
```

**TEST_DATA_SUMMARY.md:**

```markdown
# Test Data Summary

## Overview

| Metric | Value |
|--------|-------|
| Total Datasets | 12 |
| Total Records | 850 |
| Personas Covered | 3 |
| Scenarios | 5 |

## Dataset Inventory

| Category | Dataset | Records | Purpose |
|----------|---------|---------|---------|
| Catalog | locations | 10 | Warehouse locations |
| Catalog | categories | 15 | Product categories |
| Core | inventory-items | 200 | Primary inventory |
| Core | users | 25 | System users |
| Transactional | stock-movements | 500 | Movement history |
| Scenarios | warehouse-operator-day | 50 | Day-in-life scenario |

## Persona Scenarios

| Persona | Scenario | Records | Coverage |
|---------|----------|---------|----------|
| Warehouse Operator | Daily tasks | 50 | JTBD-1.1, JTBD-1.2 |
| Supervisor | Audit workflow | 30 | JTBD-2.1 |
| Manager | Reporting | 25 | JTBD-3.1 |
```

Example `datasets/core/inventory-items.json`:
```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "sku": "WH-001-A",
      "name": "Widget Type A",
      "quantity": 150,
      "location_id": "loc-001",
      "category": "widgets",
      "reorder_point": 50,
      "last_counted": "2024-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "generated_at": "<timestamp>",
    "record_count": 200,
    "entity": "InventoryItem",
    "category": "core"
  }
}
```

#### Step 5.4: Validate Checkpoint 5

```bash
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 5 --dir Prototype_<SystemName>/
```

#### Step 5.5: Update Progress

Mark phase 5 completed.

---

## Final Summary

```
═══════════════════════════════════════════════════════
  DATA PHASES COMPLETE (3-5)
═══════════════════════════════════════════════════════

  Phase 3 - Data Model:
  ├── Entities:        <N>
  ├── Relationships:   <N>
  └── Output:          04-implementation/data-model.md

  Phase 4 - API Contracts:
  ├── Endpoints:       <N>
  ├── Schemas:         <N>
  └── Output:          04-implementation/api-contracts.json

  Phase 5 - Test Data:
  ├── Catalog Files:   <N>
  ├── Core Files:      <N>
  ├── Scenarios:       <N>
  └── Output:          04-implementation/test-data/

  Checkpoints:         3 ✅  4 ✅  5 ✅

═══════════════════════════════════════════════════════

  Next: /prototype-design or /prototype <SystemName>

═══════════════════════════════════════════════════════
```

## Outputs

| File | Phase | Purpose |
|------|-------|---------|
| `00-foundation/data-model/` | 3 | **Nested entity definitions** |
| `00-foundation/data-model/DATA_MODEL_SUMMARY.md` | 3 | Executive summary |
| `00-foundation/data-model/entities/*.md` | 3 | Per-entity schemas |
| `00-foundation/data-model/relationships.md` | 3 | ERD and relationships |
| `00-foundation/api-contracts/` | 4 | **Nested API contracts** |
| `00-foundation/api-contracts/API_CONTRACTS_SUMMARY.md` | 4 | Executive summary |
| `00-foundation/api-contracts/openapi.json` | 4 | Full OpenAPI spec |
| `00-foundation/api-contracts/endpoints/*.md` | 4 | Per-resource endpoints |
| `00-foundation/test-data/` | 5 | **Nested test data** |
| `00-foundation/test-data/TEST_DATA_SUMMARY.md` | 5 | Executive summary |
| `00-foundation/test-data/datasets/` | 5 | Organized datasets |

### State Files Updated

| State File | Phase | Purpose |
|------------|-------|---------|
| `_state/data_model.json` | 3 | Entity registry for cross-skill lookup |
| `_state/api_contracts.json` | 4 | Endpoint registry |
| `_state/test_data_manifest.json` | 5 | Dataset inventory |

## Error Handling

| Error | Action |
|-------|--------|
| requirements_registry.json missing | **BLOCK** - Run /prototype-requirements |
| Entity extraction fails | Log, generate minimal schema |
| Test data generation fails | Log, create placeholder files |

### Step 6: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/prototype-data" \
  --stage "prototype" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype-requirements` | Run Phase 2 |
| `/prototype-design` | Run Phases 6-7 |
| `/prototype` | Run full prototype |
