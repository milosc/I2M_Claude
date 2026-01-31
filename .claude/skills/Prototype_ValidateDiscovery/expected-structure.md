# Expected Discovery Structure

This document details the expected structure of Stage 1 Discovery outputs
that Prototype_ValidateDiscovery validates.

---

## Directory Tree

```
DISCOVERY_PATH/
│
├── 01-analysis/
│   └── ANALYSIS_SUMMARY.md        [REQUIRED]
│
├── 02-research/
│   ├── persona-recruiter.md       [REQUIRED - at least 1]
│   ├── persona-hiring-manager.md  [OPTIONAL]
│   ├── persona-admin.md           [OPTIONAL]
│   └── jtbd-jobs-to-be-done.md    [REQUIRED]
│
├── 03-strategy/
│   ├── product-vision.md          [REQUIRED]
│   ├── product-strategy.md        [OPTIONAL]
│   └── product-roadmap.md         [REQUIRED]
│
└── 04-design-specs/
    ├── screen-definitions.md      [REQUIRED]
    ├── navigation-structure.md    [OPTIONAL]
    ├── data-fields.md             [REQUIRED]
    └── sample-data.json           [OPTIONAL]
```

---

## File Specifications

### ANALYSIS_SUMMARY.md

**Purpose**: High-level analysis of user research and problem space.

**Expected Sections**:

```markdown
# Analysis Summary: [Product Name]

## Executive Summary
Brief overview of findings.

## User Types Identified
| User Type | Count | Context |
|-----------|-------|---------|
| Recruiter | ~25   | Internal TA team |

## Critical Pain Points (P0)
1. **[Pain Point Title]**
   - Impact: [Description]
   - Affected Users: [List]

## High Priority Pain Points (P1)
1. **[Pain Point Title]**
   ...

## Technical Context
- Current systems: [List]
- Integrations: [List]
- Constraints: [List]
```

**Extraction Points**:
- Product name from title
- Pain points with priorities
- User type counts
- Technical constraints

---

### persona-*.md

**Purpose**: Detailed user persona for each primary user type.

**Naming**: `persona-[role].md` (e.g., `persona-recruiter.md`)

**Expected Sections**:

```markdown
# Persona: [Role Name]

## Overview
| Attribute | Value |
|-----------|-------|
| Role | [Role] |
| User Count | ~[N] |
| Tech Savviness | High/Medium/Low |
| Usage Pattern | Daily/Weekly/Monthly |

## Goals
1. [Primary goal]
2. [Secondary goal]

## Pain Points
### P0 (Critical)
1. [Pain point]

### P1 (High)
1. [Pain point]

## Jobs to be Done
- [JTBD 1]
- [JTBD 2]

## Workflows
1. [Workflow name]
   - Step 1
   - Step 2
```

**Extraction Points**:
- Role name
- User count
- Tech level
- Primary goal
- Top pain point

---

### jtbd-jobs-to-be-done.md

**Purpose**: Comprehensive list of jobs users need to accomplish.

**Expected Sections**:

```markdown
# Jobs to be Done

## Summary
- Total JTBD: [N]
- P0 (Critical): [N]
- P1 (High): [N]
- P2 (Medium): [N]

## By Feature Area

### [Feature Area 1]
| ID | Job | Priority | User |
|----|-----|----------|------|
| JTBD-001 | [Job description] | P0 | Recruiter |

### [Feature Area 2]
...
```

**Extraction Points**:
- Total count
- Priority breakdown
- Feature area list

---

### product-vision.md

**Purpose**: Product vision and value proposition.

**Expected Sections**:

```markdown
# Product Vision: [Product Name]

## Vision Statement
[One paragraph vision]

## Target Users
- [User 1]
- [User 2]

## Key Value Propositions
1. [Value prop 1]
2. [Value prop 2]

## Success Metrics
| Metric | Target |
|--------|--------|
| [Metric] | [Value] |
```

---

### product-roadmap.md

**Purpose**: Phased delivery plan with priorities.

**Expected Sections**:

```markdown
# Product Roadmap

## Phase 1: MVP (P0)
- [Feature 1]
- [Feature 2]

## Phase 2: Enhancement (P1)
- [Feature 3]
- [Feature 4]

## Phase 3: Scale (P2)
- [Feature 5]
```

---

### screen-definitions.md

**Purpose**: Inventory of all application screens.

**Expected Sections**:

```markdown
# Screen Definitions

## [Application Name 1]

### Dashboard
- Purpose: [Description]
- Primary User: [Role]
- Key Features: [List]

### [Screen 2]
...

## [Application Name 2]
...
```

**Extraction Points**:
- Application names
- Screen count
- Screen purposes

---

### data-fields.md

**Purpose**: Entity and field definitions.

**Expected Sections**:

```markdown
# Data Fields

## Entities

### User
| Field | Type | Required | Notes |
|-------|------|----------|-------|
| id | UUID | Yes | Primary key |
| email | String | Yes | Unique |
| role | Enum | Yes | recruiter, admin, etc. |

**Volume**: Medium (~100 records)
**Relationships**: 
- Has many: Applications
- Belongs to: Department

### [Entity 2]
...
```

**Extraction Points**:
- Entity names
- Field counts
- Volume classifications
- Relationships

---

## Validation Rules

### Required File Rules

| Rule | Action if Violated |
|------|-------------------|
| ANALYSIS_SUMMARY.md missing | STOP |
| No persona files | STOP |
| jtbd file missing | STOP |
| product-vision missing | STOP |
| product-roadmap missing | STOP |
| screen-definitions missing | STOP |
| data-fields missing | STOP |

### Content Rules

| Rule | Action if Violated |
|------|-------------------|
| No product name found | WARN, use folder name |
| No pain points | WARN, continue |
| No personas extractable | STOP |
| No JTBD count | WARN, default to 0 |
| No screens found | STOP |
| No entities found | STOP |

---

## Common Issues

### Issue: Persona file not recognized

**Cause**: File doesn't match `persona-*.md` pattern.

**Fix**: Rename to `persona-[role].md` format.

### Issue: Pain points not extracted

**Cause**: Section headers don't match expected format.

**Fix**: Use "Critical Pain Points (P0)" and "High Priority Pain Points (P1)" headers.

### Issue: Entity volumes missing

**Cause**: No "Volume" line in entity definition.

**Fix**: Add `**Volume**: Low/Medium/High (~N records)` to each entity.
