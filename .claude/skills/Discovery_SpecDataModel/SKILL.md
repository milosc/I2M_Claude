---
name: specifying-data-model
description: Use when you need to define data entities, field specifications, validation rules, and visibility permissions in data-fields.md.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill specifying-data-model started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill specifying-data-model ended '{"stage": "discovery"}'
---

# Spec Data Model

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill specifying-data-model instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_SpecDataModel
- **Version**: 3.0.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-21
- **Change History**:
  - v3.0.0 (2025-12-21): Enforced lowercase with dashes file naming (data-fields.md)
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Defines all data entities, field specifications, validation rules, and visibility permissions. Creates the data schema that drives form fields, table columns, and data relationships.

**Role**: You are a data architect who specializes in defining clean, normalized data models with appropriate validation and access control.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:specifying-data-model:started` - When skill begins
- `skill:specifying-data-model:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- User requests "define data model", "create field specs", "design data schema"
- Discovery Orchestrator invokes during design specification phase
- User needs to document what data the application manages

## Input Requirements

| Input | Required | Source |
|-------|----------|--------|
| screen-definitions.md | Yes | 04-design-specs/ |
| ANALYSIS_SUMMARY.md | Yes | 01-analysis/ |
| persona-*.md files | Yes | 02-research/ |

## CRITICAL OUTPUT REQUIREMENTS

### File Name (MANDATORY)

```
[output_path]/04-design-specs/data-fields.md
```

**File naming**: lowercase with dashes - `data-fields.md`

## Output Specification

### Primary Output: `04-design-specs/data-fields.md`

```markdown
# Data Field Specifications

**Created**: [Date]
**Application**: [Product Name]
**Total Entities**: [N]

---

## 📊 Entity Overview

| Entity | Description | Volume | Key Relationships |
|--------|-------------|--------|-------------------|
| User | System users | High (~1000) | Has many: Candidates |
| [Entity 2] | [Description] | [Volume] | [Relationships] |

---

## 🗃️ Entity Definitions

### User

**Description**: System users with authentication and role-based access
**Volume**: High (~1000 records)

#### Field Definitions

| Field | Type | Required | Validation | UI Control | Default |
|-------|------|----------|------------|------------|---------|
| id | UUID | Yes | Auto-generated | Hidden | uuid() |
| email | String | Yes | Valid email, unique | Text Input | - |
| name | String | Yes | 2-100 chars | Text Input | - |
| role | Enum | Yes | [admin, user, viewer] | Dropdown | user |
| avatar | URL | No | Valid URL | File Upload | null |
| created_at | DateTime | Yes | ISO 8601 | Read-only | now() |
| updated_at | DateTime | Yes | ISO 8601 | Read-only | now() |

#### Relationships

| Relationship | Type | Target Entity | On Delete |
|--------------|------|---------------|-----------|
| candidates | Has Many | Candidate | Cascade |
| team | Belongs To | Team | Nullify |

#### Visibility Rules

| Role | Create | Read | Update | Delete |
|------|--------|------|--------|--------|
| Admin | ✅ | ✅ All | ✅ All | ✅ |
| User | ❌ | ✅ Own | ✅ Own | ❌ |
| Viewer | ❌ | ✅ Own | ❌ | ❌ |

#### Indexes

| Index | Fields | Type | Purpose |
|-------|--------|------|---------|
| idx_user_email | email | Unique | Login lookup |
| idx_user_role | role | Non-unique | Role filtering |

---

### [Entity 2]

[Same structure]

---

## 📋 Enum Definitions

### UserRole

| Value | Label | Description |
|-------|-------|-------------|
| admin | Administrator | Full system access |
| user | User | Standard access |
| viewer | Viewer | Read-only access |

### [Enum 2]

[Same structure]

---

## 🔗 Entity Relationship Diagram

```
┌──────────┐       ┌──────────┐
│   User   │──────<│ Candidate│
└──────────┘       └──────────┘
     │                  │
     │                  │
     ▼                  ▼
┌──────────┐       ┌──────────┐
│   Team   │       │   Job    │
└──────────┘       └──────────┘
```

---

## 🎛️ UI Control Rules

### Based on Entity Volume

| Volume | Record Count | Recommended Control |
|--------|--------------|---------------------|
| Very Low | ≤5 | Radio Buttons |
| Low | 6-20 | Dropdown |
| Medium | 21-100 | Searchable Select |
| High | >100 | Async Autocomplete |

### Based on Field Type

| Field Type | UI Control | Validation Feedback |
|------------|------------|---------------------|
| Email | Email Input | Inline validation |
| Date | Date Picker | Format hint |
| Enum | Dropdown/Radio | - |
| Long Text | Textarea | Character count |
| File | File Upload | Size/type limits |

---

**Document Status**: 🟢 Complete
```

## Quality Criteria

- [ ] All entities from screens defined
- [ ] All fields have types and validation
- [ ] Relationships documented
- [ ] Visibility rules per role
- [ ] UI control recommendations

## Integration Points

### Receives From
- Discovery_SpecScreens: Data requirements
- ANALYSIS_SUMMARY: Existing data context

### Provides To
- Discovery_SpecSampleData: Schema for generation
- Prototype development: Data structure

## State Management Reminder

⚠️ **This skill produces output files only.** The calling orchestrator/command is responsible for updating state after all Phase 9 skills complete.

**After running ALL Phase 9 skills, update state:**
```bash
python3 .claude/skills/tools/update_discovery_state.py --phase 9_specs --status complete
```

**Or manually update `_state/discovery_progress.json`:**
```json
"9_specs": { "status": "complete", "started": "<ISO>", "completed": "<ISO>" },
"overall_progress": 80,
"resumable_from": "10_docs"
```

---

**Skill Version**: 3.0
**Output Location**: 04-design-specs/data-fields.md
