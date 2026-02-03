---
name: productspecs-contracts
description: Generate API contracts from prototype specifications
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-contracts started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-contracts ended '{"stage": "implementation"}'
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-contracts started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-contracts ended '{"stage": "productspecs"}'

---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs-contracts instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```
## Summary

| Category | Count | Auth Required |
|----------|-------|---------------|
| Items | 5 | Yes |
| Adjustments | 4 | Yes |
| Reports | 3 | Yes |
| Auth | 2 | No |

---

## Endpoints by Module

### MOD-INV-SEARCH-01

| Method | Endpoint | Purpose | Priority |
|--------|----------|---------|----------|
| GET | /api/v1/items | List items | P0 |
| GET | /api/v1/items/{id} | Get item detail | P0 |
| GET | /api/v1/items/search | Search items | P0 |

### MOD-INV-ADJUST-01

| Method | Endpoint | Purpose | Priority |
|--------|----------|---------|----------|
| POST | /api/v1/adjustments | Create adjustment | P0 |
| GET | /api/v1/adjustments | List adjustments | P1 |
| PUT | /api/v1/adjustments/{id}/approve | Approve adjustment | P0 |

---

## Authentication

All endpoints (except /auth/*) require:
- Bearer token in Authorization header
- Token format: JWT with user claims

---

## Error Response Format

All errors follow standard format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable message",
    "details": [...]
  }
}
```
```

### Step 4: Consolidate API Specifications

Copy and enhance API contracts from Prototype:

```python
for contract in api_contracts:
    # Add traceability
    contract["requirement_refs"] = find_requirements_for_endpoint(contract)
    contract["module_refs"] = find_modules_for_endpoint(contract)

    # Write enhanced contract
    write_api_spec(f"{output_path}/02-api/{contract['name']}.api.md", contract)
```

### Step 5: Generate SMART NFRs

Execute `ProductSpecs_NFRGenerator` skill:

1. Generate Performance NFRs
2. Generate Availability NFRs
3. Generate Security NFRs
4. Generate Accessibility NFRs
5. Generate Scalability NFRs

### Step 6: Write NFR Registry

Write `ProductSpecs_<SystemName>/_registry/nfrs.json` with all NFRs.

### Step 7: Write NFR Documentation

Write `ProductSpecs_<SystemName>/02-api/NFR_SPECIFICATIONS.md`:

```markdown
# Non-Functional Requirements Specification

**System**: <SystemName>
**Generated**: <TIMESTAMP>
**Total NFRs**: <N>

---

## Summary

| Category | Count | P0 | P1 | P2 |
|----------|-------|----|----|-----|
| Performance | 8 | 4 | 3 | 1 |
| Availability | 3 | 2 | 1 | 0 |
| Security | 5 | 5 | 0 | 0 |
| Accessibility | 6 | 6 | 0 | 0 |
| Scalability | 3 | 0 | 2 | 1 |
| **Total** | **25** | **17** | **6** | **2** |

---

## Performance Requirements

### NFR-PERF-001: Screen Load Time

| Attribute | Value |
|-----------|-------|
| **ID** | NFR-PERF-001 |
| **Priority** | P0 |
| **Metric** | Page load time < 2s at 95th percentile |
| **Measurement** | Lighthouse performance audit |
| **Modules** | All |

**SMART Validation**:
- ✅ **S**pecific: Load time < 2 seconds
- ✅ **M**easurable: 95th percentile via Lighthouse
- ✅ **A**chievable: Prototype meets this target
- ✅ **R**elevant: User experience critical
- ✅ **T**ime-bound: Per page load

---

## Security Requirements

### NFR-SEC-001: Authentication Required

| Attribute | Value |
|-----------|-------|
| **ID** | NFR-SEC-001 |
| **Priority** | P0 |
| **Metric** | 100% of non-public endpoints require valid JWT |
| **Test Method** | API security scan + code review |

...
```

### Step 8: Generate Data Contract Specifications

Write `ProductSpecs_<SystemName>/02-api/data-contracts.md`:

```markdown
# Data Contract Specifications

**System**: <SystemName>
**Generated**: <TIMESTAMP>

---

## Entity Schemas

### Item

```typescript
interface Item {
  id: string;           // UUID v4
  code: string;         // Unique item code
  name: string;         // Display name
  category: string;     // Category reference
  quantity: number;     // Current stock quantity
  location: string;     // Warehouse location
  status: ItemStatus;   // active | inactive | discontinued
  createdAt: string;    // ISO 8601 timestamp
  updatedAt: string;    // ISO 8601 timestamp
}

type ItemStatus = 'active' | 'inactive' | 'discontinued';
```

### Adjustment

```typescript
interface Adjustment {
  id: string;
  itemId: string;
  type: AdjustmentType;
  quantity: number;
  reason: string;
  status: AdjustmentStatus;
  createdBy: string;
  approvedBy?: string;
  createdAt: string;
  updatedAt: string;
}
```

---

## Validation Rules

| Entity | Field | Rule |
|--------|-------|------|
| Item | code | Required, unique, 3-20 chars |
| Item | quantity | Required, >= 0 |
| Adjustment | quantity | Required, != 0 |
| Adjustment | reason | Required, 10-500 chars |
```

### Step 9: Update Progress

Update `_state/productspecs_progress.json`:

```python
progress["phases"]["contracts"]["status"] = "completed"
progress["phases"]["contracts"]["completed_at"] = timestamp
progress["phases"]["contracts"]["outputs"] = [
    "02-api/api-index.md",
    "02-api/NFR_SPECIFICATIONS.md",
    "02-api/data-contracts.md",
    "_registry/nfrs.json"
]
progress["current_phase"] = 6
```

### Step 10: Validate Checkpoint 5

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 5 --dir ProductSpecs_<SystemName>/
```

### Step 11: Display Summary

```
═══════════════════════════════════════════════════════
  API CONTRACTS & NFRs GENERATED
═══════════════════════════════════════════════════════

  System:          <SystemName>

  API Contracts:
  ────────────────────────────────────────────────────
  • Total Endpoints:    14
  • With Traceability:  14/14 (100%)

  Non-Functional Requirements:
  ────────────────────────────────────────────────────
  │ Category      │ Count │ P0  │ SMART │
  │───────────────│───────│─────│───────│
  │ Performance   │ 8     │ 4   │ ✅    │
  │ Availability  │ 3     │ 2   │ ✅    │
  │ Security      │ 5     │ 5   │ ✅    │
  │ Accessibility │ 6     │ 6   │ ✅    │
  │ Scalability   │ 3     │ 0   │ ✅    │

  Total NFRs:      25 (100% SMART compliant)

  Checkpoint 5:    ✅ PASSED

═══════════════════════════════════════════════════════

  Next Steps:
  • /productspecs-tests      - Generate test specifications
  • /productspecs            - Continue full generation

═══════════════════════════════════════════════════════
```

## Outputs

| File | Location |
|------|----------|
| `api-index.md` | `ProductSpecs_<SystemName>/02-api/` |
| `NFR_SPECIFICATIONS.md` | `ProductSpecs_<SystemName>/02-api/` |
| `data-contracts.md` | `ProductSpecs_<SystemName>/02-api/` |
| `nfrs.json` | `ProductSpecs_<SystemName>/_registry/` |

## Error Handling

| Error | Action |
|-------|--------|
| Checkpoint 4 not passed | **BLOCK** - Run /productspecs-modules |
| Missing API contracts | **WARN** - Generate from prototype screens |
| NFR not SMART compliant | **WARN** - Flag for review |
| Missing endpoint traceability | **WARN** - Log, continue |

## Quality Checklist

## Related Commands

| Command | Description |
|---------|-------------|
| `/productspecs-modules` | Previous phase |
| `/productspecs-tests` | Next phase |
| `/productspecs` | Full generation |
