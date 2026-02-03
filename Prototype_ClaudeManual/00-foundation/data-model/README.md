# Data Model Documentation

## Overview

This folder contains the complete data model specification for the ClaudeManual interactive documentation system. The data model defines 9 core entities, 122 fields, 8 relationships, and 27 validation rules.

## Files

| File | Purpose | Lines |
|------|---------|-------|
| `DATA_MODEL.md` | Complete data model specification with ER diagram, entity definitions, API types | ~800 |
| `ENTITY_INDEX.md` | Quick reference guide for all entities with field summaries | ~300 |
| `types.ts` | TypeScript interfaces, enums, and type definitions | ~550 |
| `validation.ts` | Zod validation schemas and validation utilities | ~550 |
| `mock-data.ts` | Faker.js mock data generators for testing | ~450 |

## Entities

### Core Entities (5)

| ID | Entity | Location | Purpose |
|----|--------|----------|---------|
| ENT-001 | **Skill** | `.claude/skills/{id}/SKILL.md` | Reusable AI prompt templates |
| ENT-002 | **Command** | `.claude/commands/{id}.md` | Slash commands for Claude Code |
| ENT-003 | **Agent** | `.claude/agents/{id}.md` | Specialized AI personas |
| ENT-004 | **Rule** | `.claude/rules/{id}.md` | Framework rules and conventions |
| ENT-005 | **Hook** | `.claude/hooks/{id}.(py|sh)` | Lifecycle hooks |

### Reference Entities (1)

| ID | Entity | Location | Purpose |
|----|--------|----------|---------|
| ENT-006 | **UserPreferences** | Browser localStorage | Per-user settings (theme, favorites) |

### Documentation Entities (3)

| ID | Entity | Location | Purpose |
|----|--------|----------|---------|
| ENT-007 | **Workflow** | `.claude/` or project folders | Process and workflow diagrams |
| ENT-008 | **WaysOfWorking** | Documentation folders | Team practices and guidelines |
| ENT-009 | **ArchitectureDoc** | `architecture/` folder | C4 diagrams, ADRs, patterns |

## Relationships

```
Skill ──(uses_skill)──> Skill
Command ──(invokes_skill)──> Skill
Command ──(orchestrates_agents)──> Agent
Agent ──(loads_skill)──> Skill
UserPreferences ──(favorites)──> Skill | Command | Agent
Workflow ──(referenced_in)──> Skill
ArchitectureDoc ──(related_adrs)──> ArchitectureDoc
```

## Field Summary

| Entity | Core | Content Sections | Derived | Total |
|--------|------|------------------|---------|-------|
| Skill | 11 | 6 | 5 | 22 |
| Command | 8 | 6 | 3 | 17 |
| Agent | 9 | 5 | 3 | 17 |
| Rule | 7 | 4 | 1 | 12 |
| Hook | 6 | 0 | 2 | 8 |
| UserPreferences | 7 | 0 | 0 | 7 |
| Workflow | 8 | 4 | 0 | 12 |
| WaysOfWorking | 7 | 4 | 0 | 11 |
| ArchitectureDoc | 10 | 6 | 0 | 16 |
| **TOTAL** | **73** | **35** | **14** | **122** |

## Validation Rules

**Total**: 27 rules across 9 entities

**Critical Rules** (15):
- VR-SKL-001: Skill ID must match folder name
- VR-SKL-002: Skill file must exist at path
- VR-SKL-004: Skill must have Purpose and Usage sections
- VR-CMD-001: Command ID must match filename
- VR-CMD-003: Command must have Usage and Example sections
- VR-AGT-001: Agent ID must follow {stage}-{role} naming
- VR-AGT-003: Agent must have Expertise and Output Format sections
- VR-RUL-001: Rule file must exist
- VR-HKS-001: Hook must be executable
- VR-USR-002: Favorites must reference existing items
- VR-WFL-001: Workflow file must exist
- VR-WFL-002: Workflow file extension must match format
- VR-WOW-001: WaysOfWorking file must exist
- VR-ARC-001: ArchitectureDoc file must exist
- VR-ARC-002: ArchitectureDoc file extension must match format

## Usage Examples

### TypeScript Types

```typescript
import { Skill, Command, Agent } from './types';

const skill: Skill = {
  id: 'Discovery_JTBD',
  name: 'Discovery JTBD',
  description: 'Generate Jobs To Be Done analysis',
  stage: 'Discovery',
  path: '.claude/skills/Discovery_JTBD/SKILL.md',
  model: 'sonnet',
  // ... other fields
};
```

### Validation

```typescript
import { skillSchema, validateEntity } from './validation';

const result = validateEntity(skillSchema, skillData);

if (!result.valid) {
  console.error('Validation errors:', result.errors);
}
```

### Mock Data

```typescript
import { mockSkill, generateMockDataset } from './mock-data';

// Generate single entity
const skill = mockSkill();

// Generate complete dataset
const dataset = generateMockDataset({
  skillCount: 20,
  commandCount: 10,
  agentCount: 15,
});
```

## API Types

### List Endpoints

```typescript
import { SkillListResponse, SkillQueryParams } from './types';

// GET /api/skills?stage=Discovery&page=1&pageSize=20
const params: SkillQueryParams = {
  stage: ['Discovery', 'Prototype'],
  page: 1,
  pageSize: 20,
  favorited: true,
};

const response: SkillListResponse = {
  data: [...skills],
  pagination: {
    page: 1,
    pageSize: 20,
    totalItems: 45,
    totalPages: 3,
  },
};
```

### Search Endpoint

```typescript
import { SearchRequest, SearchResponse } from './types';

// POST /api/search
const request: SearchRequest = {
  query: 'JTBD analysis',
  types: ['Skill', 'Command'],
  stage: ['Discovery'],
  limit: 10,
};

const response: SearchResponse = {
  results: [
    {
      id: 'Discovery_JTBD',
      type: 'Skill',
      name: 'Discovery JTBD',
      description: 'Generate Jobs To Be Done analysis',
      stage: 'Discovery',
      score: 0.95,
    },
  ],
  total: 1,
};
```

## Traceability

| Data Field | Traces To |
|------------|-----------|
| DF-SKL-004 (stage) | JTBD-1.4, PP-1.4, CF-011 |
| DF-SKL-C04 (Example) | JTBD-2.1, PP-1.2, CF-008 |
| DF-USR-002 (favorites) | JTBD-1.6, PP-1.5, CF-012 |
| DF-USR-001 (theme) | PP-1.5, CF-016 |
| DF-SKL-005 (path) | JTBD-1.5, PP-1.6, CF-013 |
| IDX-001 (search) | JTBD-1.3, PP-1.3, CF-009 |

## Implementation Notes

### Data Source Strategy

1. **File System Scanning**: All entities read from `.claude/` folders at app startup
2. **Frontmatter Parsing**: YAML frontmatter provides structured metadata
3. **Markdown Parsing**: Extract content sections using heading-based delimiters
4. **Cache Invalidation**: Use file `last_modified` timestamp and `content_hash`

### Performance Targets

| Operation | Target Time | Strategy |
|-----------|-------------|----------|
| Initial Load | < 2s | Parallel file reads, lazy content parsing |
| Search | < 200ms | Pre-built inverted index, debounced input |
| Filter | < 100ms | In-memory filtering on indexed fields |
| Detail View | < 50ms | Cached parsed content |

### Error Handling

| Error Type | Strategy | User Message |
|------------|----------|--------------|
| Missing file | Skip entity, log warning | "Some items could not be loaded" |
| Invalid frontmatter | Use defaults, log error | "Warning: {file} has invalid metadata" |
| Validation failure | Mark entity as invalid | "Invalid {entity}: {reason}" |

## Related Files

- **Source**: `ClientAnalysis_ClaudeManual/04-design-specs/data-fields.md`
- **Requirements**: `traceability/requirements_registry.json`
- **Client Facts**: `traceability/client_facts_registry.json`
- **Pain Points**: `ClientAnalysis_ClaudeManual/01-analysis/PAIN_POINTS.md`
- **JTBD**: `ClientAnalysis_ClaudeManual/02-research/JOBS_TO_BE_DONE.md`

---

**Generated**: 2026-01-31
**Session**: session-data-model-claudemanual
**Agent**: prototype-data-model-specifier
**Checkpoint**: CP-3
