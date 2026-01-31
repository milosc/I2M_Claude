---
description: Generate sample data from discovery specifications
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-sample-data started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-sample-data ended '{"stage": "discovery"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-sample-data instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Discovery-specific rules. Load them now:

```bash
# Load Discovery rules (includes PDF handling, input processing, output structure)
/rules-discovery

# Load Traceability rules (includes ID formats, source linking)
/rules-traceability
```

## Arguments

None required - reads configuration from `_state/discovery_config.json`

## Prerequisites

- Data fields document exists
- `04-design-specs/data-fields.md` exists

## Skills Used

- `.claude/skills/Discovery_SpecSampleData/Discovery_SpecSampleData.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read `04-design-specs/data-fields.md` for entity schemas

2. **Read Discovery_SpecSampleData Skill**
   - Understand sample data requirements
   - Review data consistency rules

3. **Generate Sample Data**
   - Create `04-design-specs/sample-data.json`
   - Structure:
     ```json
     {
       "_metadata": {
         "document_id": "DISC-SAMPLEDATA-<SystemName>",
         "version": "1.0.0",
         "created_at": "<YYYY-MM-DD>",
         "updated_at": "<YYYY-MM-DD>",
         "generated_by": "Discovery_SpecSampleData",
         "description": "Sample data for prototype and testing"
       },
       "entities": {
         "users": [...],
         "orders": [...],
         ...
       }
     }
     ```

4. **Sample Data Requirements**
   For each entity:
   - Minimum 5-10 records
   - Cover all enum values
   - Include edge cases (empty strings, max values)
   - Maintain referential integrity
   - Use realistic but fictional data

5. **Data Generation Guidelines**
   ```json
   {
     "_metadata": { ... },
     "entities": {
       "users": [
         {
           "id": "user-001",
           "email": "john.smith@example.com",
           "name": "John Smith",
           "role": "admin",
           "created_at": "2025-01-01T08:00:00Z",
           "updated_at": "2025-01-15T14:30:00Z"
         },
         {
           "id": "user-002",
           "email": "jane.doe@example.com",
           "name": "Jane Doe",
           "role": "manager",
           "created_at": "2025-01-02T09:00:00Z",
           "updated_at": "2025-01-10T11:00:00Z"
         }
       ],
       "orders": [
         {
           "id": "order-001",
           "user_id": "user-001",
           "status": "completed",
           "total": 299.99,
           "items": [
             { "product_id": "prod-001", "quantity": 2, "price": 149.99 }
           ],
           "created_at": "2025-01-05T10:30:00Z"
         }
       ]
     }
   }
   ```

6. **Validate Sample Data**
   - All required fields present
   - Field types match schema
   - Foreign keys reference existing records
   - Enum values are valid
   - JSON parses without errors

## Data Consistency Rules

| Rule | Example |
|------|---------|
| Foreign keys valid | order.user_id exists in users |
| Computed fields correct | order.total = sum(items) |
| Dates logical | created_at <= updated_at |
| IDs unique | No duplicate IDs per entity |
| Enums valid | Only defined enum values |

## Sample Data Categories

| Category | Purpose | Count |
|----------|---------|-------|
| Happy path | Normal usage | 5+ records |
| Edge cases | Boundaries | 2+ records |
| Empty states | No data scenarios | 1+ record |
| Full data | All fields populated | 2+ records |

## Quality Checklist

- [ ] JSON validates without errors
- [ ] All entities from data-fields.md included
- [ ] Foreign key relationships valid
- [ ] Realistic data values
- [ ] Edge cases covered
- [ ] Sufficient records for testing

## Outputs

- `ClientAnalysis_<SystemName>/04-design-specs/sample-data.json`

### Step 7: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST

echo "✅ Logged command completion"
```

## Next Command

- Run `/discovery-components` for UI components
- Or run `/discovery-specs-all` for all spec documents
