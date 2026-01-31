---
name: specifying-sample-data
description: Use when you need to generate realistic sample data (sample-data.json) in JSON format based on the data model for prototype testing.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill specifying-sample-data started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill specifying-sample-data ended '{"stage": "discovery"}'
---

# Spec Sample Data

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill specifying-sample-data instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_SpecSampleData
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Generates realistic sample data in JSON format based on the data model. Creates interconnected test data that reflects personas, relationships, and realistic scenarios for prototype development.

**Role**: You are a test data specialist who creates realistic, interconnected datasets that enable meaningful prototype testing and stakeholder validation.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:specifying-sample-data:started` - When skill begins
- `skill:specifying-sample-data:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- User requests "generate sample data", "create test data", "mock data"
- Discovery Orchestrator invokes during design specification phase
- User needs realistic data to populate prototypes

## Input Requirements

| Input | Required | Source |
|-------|----------|--------|
| data-fields.md | Yes | 04-design-specs/ |
| persona-*.md files | Yes | 02-research/ |
| screen-definitions.md | Yes | 04-design-specs/ |

## Output Specification

### Primary Output: `04-design-specs/sample-data.json`

```json
{
  "meta": {
    "generated_for": "[Product Name]",
    "version": "1.0",
    "generated_at": "[ISO Date]",
    "record_counts": {
      "users": 10,
      "candidates": 50,
      "jobs": 8
    }
  },
  
  "users": [
    {
      "id": "usr_001",
      "email": "sarah.miller@company.com",
      "name": "Sarah Miller",
      "role": "recruiter",
      "avatar": "https://i.pravatar.cc/150?u=sarah",
      "created_at": "2024-01-15T09:00:00Z",
      "_persona": "Talent Acquisition Specialist",
      "_notes": "Primary user persona"
    },
    {
      "id": "usr_002",
      "email": "james.chen@company.com",
      "name": "James Chen",
      "role": "hiring_manager",
      "avatar": "https://i.pravatar.cc/150?u=james",
      "created_at": "2024-02-01T09:00:00Z",
      "_persona": "Hiring Manager"
    }
  ],
  
  "candidates": [
    {
      "id": "cnd_001",
      "name": "John Smith",
      "email": "john.smith@email.com",
      "phone": "+1-555-0101",
      "status": "interview",
      "job_id": "job_001",
      "recruiter_id": "usr_001",
      "score": 85,
      "applied_at": "2024-11-01T10:30:00Z",
      "_scenario": "Strong candidate in interview stage"
    }
  ],
  
  "jobs": [
    {
      "id": "job_001",
      "title": "Senior Software Developer",
      "department": "Engineering",
      "location": "Remote",
      "status": "active",
      "candidates_count": 12,
      "created_at": "2024-10-15T09:00:00Z",
      "_scenario": "Active role with pipeline"
    }
  ],
  
  "_scenarios": {
    "empty_state": "Filter by status='archived' for empty results",
    "high_volume": "Use job_002 for 50+ candidates",
    "urgent_action": "Candidates cnd_010-015 have pending interviews today"
  }
}
```

## Data Generation Guidelines

### Volume Per Entity

| Entity | Sample Count | Distribution |
|--------|--------------|--------------|
| Users | 10 | 3 recruiters, 5 hiring managers, 2 admins |
| Candidates | 50 | Distributed across stages |
| Jobs | 8 | 5 active, 2 closed, 1 draft |

### Naming Conventions

- Use realistic first/last names
- Email format: firstname.lastname@domain.com
- Phone format: +1-555-XXXX
- IDs: entity_prefix + underscore + number (usr_001, cnd_001)

### Relationship Integrity

- Every candidate has valid job_id and recruiter_id
- Counts match (job.candidates_count = actual candidates)
- Dates are chronologically consistent

### Persona Alignment

- Include records matching each persona's typical view
- Create scenarios that test persona-specific workflows
- Add _persona field for traceability

### Test Scenarios

Include data that enables testing:
- Empty states (filtered views with no results)
- Loading states (large datasets)
- Error scenarios (invalid data flagged)
- Edge cases (max length names, special characters)

## Quality Criteria

- [ ] All entities from data-fields.md represented
- [ ] Relationships maintain referential integrity
- [ ] Volume appropriate for prototype (10-50 per entity)
- [ ] Scenarios documented for testing
- [ ] Persona-aligned records included
- [ ] Realistic naming and values

## Integration Points

### Receives From
- Discovery_SpecDataModel: Entity schema
- Discovery_GeneratePersona: User contexts

### Provides To
- Prototype development: Initial data load
- QA testing: Test scenarios

---

**Skill Version**: 2.0
**Output Location**: 04-design-specs/sample-data.json
