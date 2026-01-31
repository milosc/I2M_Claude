---
description: Generate data field specifications from discovery materials
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-data-fields started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-data-fields ended '{"stage": "discovery"}'
---


# /discovery-data-fields - Generate Data Fields Document

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-data-fields instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- Screen definitions exist
- `04-design-specs/screen-definitions.md` exists
- `01-analysis/ANALYSIS_SUMMARY.md` exists for domain context

## Skills Used

- `.claude/skills/Discovery_SpecDataModel/Discovery_SpecDataModel.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read `04-design-specs/screen-definitions.md` for data requirements
   - Read `01-analysis/ANALYSIS_SUMMARY.md` for domain entities

2. **Read Discovery_SpecDataModel Skill**
   - Understand entity definition format
   - Review field type specifications
   - Understand relationship documentation

3. **Generate Data Fields Document**
   - Create `04-design-specs/data-fields.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-DATAMODEL-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_SpecDataModel
     source_files:
       - 04-design-specs/screen-definitions.md
       - 01-analysis/ANALYSIS_SUMMARY.md
     ---
     ```

4. **Content Structure**
   ```markdown
   # Data Fields - <SystemName>

   ## Entity Overview

   | Entity | Description | Key Fields | Screens |
   |--------|-------------|------------|---------|
   | User | System users | id, email, role | S-1.1, S-2.1 |
   | [Entity] | ... | ... | ... |

   ## Entity Relationship Diagram

   ```mermaid
   erDiagram
   User ||--o{ Order : places
   Order ||--|{ OrderItem : contains
   Product ||--o{ OrderItem : "included in"
   ```

   ## Entity Definitions

   ### User
   **Description**: System users and their roles
   **Primary Key**: id
   **Screens**: S-1.1, S-2.1, S-2.2

   | Field | Type | Required | Constraints | Description |
   |-------|------|----------|-------------|-------------|
   | id | UUID | Yes | PK, Auto-gen | Unique identifier |
   | email | String | Yes | Unique, Email format | User email |
   | name | String | Yes | Max 100 chars | Display name |
   | role | Enum | Yes | admin, manager, user | User role |
   | created_at | DateTime | Yes | Auto-gen | Creation timestamp |
   | updated_at | DateTime | Yes | Auto-update | Last update |

   **Relationships**:
   - Has many: Order
   - Belongs to: Organization

   **Indexes**:
   - email (unique)
   - role

   **Business Rules**:
   - Email must be unique across all users
   - Role determines feature access

   ### [Entity Name]
   ...

   ## Enumerations

   ### UserRole
   | Value | Label | Description |
   |-------|-------|-------------|
   | admin | Administrator | Full system access |
   | manager | Manager | Department access |
   | user | User | Standard access |

   ### [EnumName]
   ...

   ## Field Type Reference

   | Type | Format | Validation | Example |
   |------|--------|------------|---------|
   | UUID | string | UUID v4 | "550e8400-e29b-..." |
   | String | string | Max length | "Example" |
   | Integer | number | Min/Max | 42 |
   | Decimal | number | Precision | 99.99 |
   | Boolean | boolean | true/false | true |
   | DateTime | ISO 8601 | Valid date | "2025-01-15T10:30:00Z" |
   | Enum | string | Allowed values | "active" |
   | JSON | object | Valid JSON | {"key": "value"} |

   ## Validation Rules

   | Entity | Field | Rule | Error Message |
   |--------|-------|------|---------------|
   | User | email | Valid email format | "Invalid email format" |
   | User | email | Unique | "Email already exists" |

   ## Computed Fields

   | Entity | Field | Calculation | Description |
   |--------|-------|-------------|-------------|
   | Order | total | sum(items.price * items.qty) | Order total |

   ## Audit Fields

   All entities include:
   | Field | Type | Description |
   |-------|------|-------------|
   | created_at | DateTime | Record creation |
   | created_by | UUID | Creator reference |
   | updated_at | DateTime | Last modification |
   | updated_by | UUID | Modifier reference |
   ```

## Quality Checklist

- [ ] All entities from screens defined
- [ ] Field types and constraints specified
- [ ] Relationships documented
- [ ] Validation rules complete
- [ ] Audit fields included

## Outputs

- `ClientAnalysis_<SystemName>/04-design-specs/data-fields.md`

## Next Command

- Run `/discovery-sample-data` to generate sample data
- Or run `/discovery-specs-all` for all spec documents
