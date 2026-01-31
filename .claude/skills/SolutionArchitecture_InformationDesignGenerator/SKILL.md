---
name: generating-information-design
description: Use when you need to generate API contracts, data models, and event catalogs from product specifications.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-information-design started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-information-design ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-information-design instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Contract Generator Skill

> **Version**: 1.0.0
> **Purpose**: Generate API Contracts, Data Models, and Event Catalogs from Product Specifications

---

## Execution Logging (MANDATORY)

This skill logs all execution to the global pipeline progress registry. Logging is automatic and requires no manual configuration.

### How Logging Works

Every execution of this skill is logged to `_state/lifecycle.json`:

- **start_event**: Logged when skill execution begins
- **end_event**: Logged when skill execution completes

Events include:
- skill_name, intent, stage, system_name
- start/end timestamps
- status (completed/failed)
- output files created (information design)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '\"skill_name\": \"generating-information-design\"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill \"generating-information-design\" --stage solarch
```

Logging is handled automatically by the skill framework. No user action required.

---

## Overview

This skill transforms module specifications into formal contracts that bridge frontend, backend, and persistence layers. It ensures consistency between the architecture and the implementation specifications.

---

## Contract Types

| Contract Type | Purpose | Source | Output |
|--------------|---------|--------|--------|
| API Contracts | REST endpoint definitions | MOD-*.md Section 7 | api-contracts.md |
| Data Model | Entity schemas and relationships | Data Requirements | data-model.md |
| Event Catalog | Integration events | MOD-*.md state diagrams | event-catalog.md |
| DTO Catalog | Data transfer objects | API responses | dto-catalog.md |

---

## API Contracts

### Source Extraction

From each MOD-*.md:
```yaml
extract:
  endpoints: "7. API Contracts" → "7.1 Endpoint Summary"
  requests: "7.2 Create {Entity}" → Request body
  responses: "7.2 Create {Entity}" → Response body
  errors: "7.3 Error Responses"
```

### Contract Template

```markdown
## {Resource} API

### Endpoint Summary

| Method | Path | Description | Auth | Module |
|--------|------|-------------|------|--------|
| {METHOD} | {/path} | {Description} | {Bearer/None} | {MOD-*} |

### {Method} {Path}

**Purpose**: {What this endpoint does}

**Authorization**:
- Required Role(s): {roles}
- Permission: {permission.action}

**Request**

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| {name} | {path/query/body} | {type} | {Yes/No} | {description} |

```json
{
  "field": "example value"
}
```

**Response**

| Status | Description |
|--------|-------------|
| 200 | Success |
| 400 | Validation error |
| 401 | Unauthorized |
| 404 | Not found |

**Success Response (200)**:
```json
{
  "field": "example value"
}
```

**Error Response (400)**:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Field validation failed",
    "details": [
      {"field": "quantity", "message": "Must be greater than 0"}
    ]
  }
}
```

**Traceability**:
- Requirement: {US/FR-*}
- Screen: {S-*}
- testID: {testID}
```

### Example: Adjustment API Contract

```markdown
## Adjustments API

### Endpoint Summary

| Method | Path | Description | Auth | Module |
|--------|------|-------------|------|--------|
| GET | /items | Search items | Bearer | MOD-INV-ADJUST-01 |
| GET | /items/{id}/bins | Get item bin locations | Bearer | MOD-INV-ADJUST-01 |
| POST | /adjustments | Create stock adjustment | Bearer | MOD-INV-ADJUST-01 |
| GET | /adjustments/{id} | Get adjustment details | Bearer | MOD-INV-ADJUST-01 |
| GET | /reason-codes | List reason codes | Bearer | MOD-INV-ADJUST-01 |

---

### POST /adjustments

**Purpose**: Create a new stock adjustment to move inventory between bins

**Authorization**:
- Required Role(s): Coordinator, Manager, Admin
- Permission: adjustment.create

**Request**

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| itemId | body | string | Yes | ID of item to adjust |
| fromBinId | body | string | Yes | Source bin ID |
| toBinId | body | string | Yes | Destination bin ID |
| quantity | body | integer | Yes | Quantity to move (> 0) |
| reasonCode | body | string | Yes | Adjustment reason code |
| reference | body | string | No | External reference (ticket #) |
| notes | body | string | No | Additional notes (max 500 chars) |

```json
{
  "itemId": "item_WG7892",
  "fromBinId": "bin_A01021",
  "toBinId": "bin_A01011",
  "quantity": 50,
  "reasonCode": "MISPLACED_ITEM",
  "reference": "TICKET-12345",
  "notes": "Found during inventory count"
}
```

**Response**

| Status | Description |
|--------|-------------|
| 201 | Adjustment created successfully |
| 400 | Validation error |
| 401 | Unauthorized |
| 403 | Forbidden (insufficient permissions) |
| 409 | Conflict (insufficient stock or concurrent modification) |
| 422 | Unprocessable (approval required) |

**Success Response (201)**:
```json
{
  "id": "adj_2024_0012",
  "itemId": "item_WG7892",
  "itemCode": "WG-7892",
  "itemName": "Widget Gear 14mm",
  "fromBinId": "bin_A01021",
  "fromBinCode": "A-01-02-1",
  "fromQtyBefore": 75,
  "fromQtyAfter": 25,
  "toBinId": "bin_A01011",
  "toBinCode": "A-01-01-1",
  "toQtyBefore": 12,
  "toQtyAfter": 62,
  "quantity": 50,
  "reasonCode": "MISPLACED_ITEM",
  "reference": "TICKET-12345",
  "status": "completed",
  "requiresApproval": false,
  "propagatedAt": "2025-01-15T16:30:05Z",
  "createdAt": "2025-01-15T16:30:00Z",
  "createdBy": "user_monica"
}
```

**Error Response (409 - Insufficient Stock)**:
```json
{
  "success": false,
  "error": {
    "code": "INSUFFICIENT_STOCK",
    "message": "Source bin has only 25 units available",
    "details": {
      "requested": 50,
      "available": 25,
      "binId": "bin_A01021"
    }
  }
}
```

**Traceability**:
- Requirement: US-002 (Confirm adjustment details before saving)
- Screen: S-03 (Confirmation)
- testID: btn_confirm
```

---

## Data Model

### Source Extraction

From MOD-*.md "Data Requirements" sections and 04_Prototype data-model/:
```yaml
extract:
  entities: Each "Data | Endpoint" row
  fields: Response schemas
  relationships: Cross-module references
```

### Entity Template

```markdown
## {Entity Name}

**Module**: {MOD-*}
**Database Schema**: {schema_name}
**Table**: {table_name}

### Fields

| Field | Type | Nullable | Default | Description |
|-------|------|----------|---------|-------------|
| id | UUID | No | gen_random_uuid() | Primary key |
| {field} | {type} | {Yes/No} | {default} | {description} |
| created_at | TIMESTAMPTZ | No | NOW() | Record creation |
| updated_at | TIMESTAMPTZ | No | NOW() | Last modification |
| created_by | UUID | No | - | FK to users |

### Indexes

| Name | Columns | Type | Purpose |
|------|---------|------|---------|
| {name} | {columns} | {btree/hash/gin} | {query optimization} |

### Relationships

| Relation | Target | Type | FK Column | On Delete |
|----------|--------|------|-----------|-----------|
| {name} | {entity} | {1:N/N:1/N:M} | {column} | {CASCADE/RESTRICT} |

### Constraints

| Name | Type | Expression |
|------|------|------------|
| {name} | {CHECK/UNIQUE} | {expression} |

### Sample Data

```sql
INSERT INTO {table} ({columns}) VALUES
({values});
```
```

### Example: Adjustment Entity

```markdown
## Adjustment

**Module**: MOD-INV-ADJUST-01
**Database Schema**: inventory
**Table**: adjustments

### Fields

| Field | Type | Nullable | Default | Description |
|-------|------|----------|---------|-------------|
| id | UUID | No | gen_random_uuid() | Primary key |
| adjustment_number | VARCHAR(20) | No | - | Human-readable ID (ADJ-YYYY-NNNN) |
| item_id | UUID | No | - | FK to items |
| from_bin_id | UUID | No | - | Source bin FK |
| to_bin_id | UUID | No | - | Destination bin FK |
| quantity | INTEGER | No | - | Units moved |
| reason_code | VARCHAR(50) | No | - | Reason code enum |
| reference | VARCHAR(100) | Yes | NULL | External ticket reference |
| notes | TEXT | Yes | NULL | Additional notes |
| status | VARCHAR(20) | No | 'pending' | pending/completed/failed/cancelled |
| requires_approval | BOOLEAN | No | false | Whether approval needed |
| approval_id | UUID | Yes | NULL | FK to approvals if required |
| propagated_at | TIMESTAMPTZ | Yes | NULL | When picking was notified |
| created_at | TIMESTAMPTZ | No | NOW() | Creation timestamp |
| created_by | UUID | No | - | FK to users |

### Indexes

| Name | Columns | Type | Purpose |
|------|---------|------|---------|
| idx_adj_item | item_id | btree | Item lookup |
| idx_adj_created | created_at DESC | btree | Recent adjustments |
| idx_adj_status | status | btree | Status filtering |
| idx_adj_user | created_by, created_at DESC | btree | User's adjustments |

### Relationships

| Relation | Target | Type | FK Column | On Delete |
|----------|--------|------|-----------|-----------|
| item | items | N:1 | item_id | RESTRICT |
| fromBin | bins | N:1 | from_bin_id | RESTRICT |
| toBin | bins | N:1 | to_bin_id | RESTRICT |
| createdBy | users | N:1 | created_by | RESTRICT |
| approval | approvals | 1:1 | approval_id | SET NULL |

### Constraints

| Name | Type | Expression |
|------|------|------------|
| chk_qty_positive | CHECK | quantity > 0 |
| chk_different_bins | CHECK | from_bin_id != to_bin_id |
| chk_status_valid | CHECK | status IN ('pending', 'completed', 'failed', 'cancelled') |

### Sample Data

```sql
INSERT INTO inventory.adjustments 
(id, adjustment_number, item_id, from_bin_id, to_bin_id, quantity, reason_code, status, created_by)
VALUES
('adj_001', 'ADJ-2025-0001', 'item_WG7892', 'bin_A01021', 'bin_A01011', 50, 'MISPLACED_ITEM', 'completed', 'user_monica');
```
```

---

## Event Catalog

### Source Extraction

From MOD-*.md state diagrams and ADR-006:
```yaml
extract:
  state_transitions: "UI State Logic" mermaid diagrams
  integration_events: "Propagation Flow" sequences
  cross_module: Module dependencies
```

### Event Template

```markdown
## {EventName}

**Type**: Domain Event | Integration Event
**Publisher**: {MOD-*}
**Subscribers**: {MOD-*, MOD-*}

### Purpose
{What this event signifies}

### Payload Schema

```typescript
interface {EventName} {
  eventId: string;       // UUID
  occurredAt: string;    // ISO 8601 timestamp
  // Domain fields
  {field}: {type};
}
```

### Example Payload

```json
{
  "eventId": "evt_123",
  "occurredAt": "2025-01-15T16:30:00Z",
  "field": "value"
}
```

### Triggers
- {What causes this event}

### Subscribers

| Module | Handler | Action |
|--------|---------|--------|
| {MOD-*} | {HandlerName} | {What happens} |

### Idempotency
{How to handle duplicate events}

### Traceability
- Pain Point: {PP-*}
- Requirement: {US/FR-*}
- ADR: ADR-006
```

### Example: StockChangedEvent

```markdown
## StockChangedEvent

**Type**: Integration Event
**Publisher**: MOD-INV-ADJUST-01
**Subscribers**: MOD-INV-HISTORY-01, MOD-INV-EXCEPT-01, Picking System

### Purpose
Notifies all interested parties that stock levels have changed due to an adjustment. Enables real-time propagation to downstream systems.

### Payload Schema

```typescript
interface StockChangedEvent {
  eventId: string;           // UUID
  occurredAt: string;        // ISO 8601
  adjustmentId: string;      // Adjustment that caused change
  itemId: string;            // Item affected
  itemCode: string;          // Human-readable item code
  fromBinId: string;         // Source bin
  fromBinCode: string;       // Human-readable bin code
  toBinId: string;           // Destination bin
  toBinCode: string;         // Human-readable bin code
  quantity: number;          // Units moved
  userId: string;            // Who made the change
  correlationId: string;     // Request correlation
}
```

### Example Payload

```json
{
  "eventId": "evt_abc123",
  "occurredAt": "2025-01-15T16:30:00.123Z",
  "adjustmentId": "adj_2024_0012",
  "itemId": "item_WG7892",
  "itemCode": "WG-7892",
  "fromBinId": "bin_A01021",
  "fromBinCode": "A-01-02-1",
  "toBinId": "bin_A01011",
  "toBinCode": "A-01-01-1",
  "quantity": 50,
  "userId": "user_monica",
  "correlationId": "req_xyz789"
}
```

### Triggers
- Successful POST /adjustments completion
- After database transaction commits

### Subscribers

| Module | Handler | Action |
|--------|---------|--------|
| MOD-INV-HISTORY-01 | TransactionLogHandler | Records in transaction log |
| MOD-INV-EXCEPT-01 | ExceptionMetricsHandler | Updates exception counters |
| WebSocket Hub | PropagationHandler | Pushes status to UI |
| Picking System | ExternalWebhookHandler | HTTP POST to picking API |

### Idempotency
- Use eventId as idempotency key
- Subscribers should check if eventId already processed
- Safe to replay - handlers are idempotent

### Traceability
- Pain Point: PP-001 (Picking doesn't reflect adjustments immediately)
- Requirement: US-003 (Know picking was updated), FR-002 (Real-time propagation)
- ADR: ADR-006 (Event-Driven Communication)
```

---

## Output Files

| File | Location | Content |
|------|----------|---------|
| api-contracts.md | 10-information-design/ | All API endpoints |
| data-model.md | 10-information-design/ | All entities |
| event-catalog.md | 10-information-design/ | All events |
| dto-catalog.md | 10-information-design/ | All DTOs |

---

## State Management Integration

### Command System Integration

This skill generates information design artifacts as part of the building blocks phase:

```
Commands that use this skill:
├─ /solarch-blocks (checkpoint 4) - Data model, entity schemas
└─ /solarch-runtime (checkpoint 5) - API contracts, events
```

### Output Locations

| Artifact | Location |
|----------|----------|
| api-contracts.md | `SolArch_{name}/06-runtime/api-contracts.md` |
| data-model.md | `SolArch_{name}/05-building-blocks/data-model.md` |
| event-catalog.md | `SolArch_{name}/06-runtime/event-catalog.md` |
| dto-catalog.md | `SolArch_{name}/06-runtime/dto-catalog.md` |

### Registry Updates

After generating contracts, update `_registry/components.json`:

```json
{
  "contracts": {
    "api_endpoints": 15,
    "entities": 8,
    "events": 5,
    "dtos": 12
  }
}
```

### Quality Gate Validation

```bash
# Checkpoint 5 validates contracts exist
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 5 --dir SolArch_X/
```

---

**Skill Status**: Ready for Use
