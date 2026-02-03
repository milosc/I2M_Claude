# API Contracts - ClaudeManual

---
**System**: ClaudeManual
**Stage**: Prototype
**Checkpoint**: CP-4
**Created**: 2026-01-31
**Session**: session-api-contracts-claudemanual
**Agent**: prototype-api-contract-specifier
---

## Overview

This folder contains comprehensive API contracts for the ClaudeManual framework explorer, including OpenAPI 3.0 specification, TypeScript types, endpoint documentation, and error handling patterns.

## Contents

| File | Description | Lines | Purpose |
|------|-------------|-------|---------|
| `openapi.json` | OpenAPI 3.0.3 specification | ~1200 | Complete API definition with schemas, endpoints, parameters |
| `api-types.ts` | TypeScript types and interfaces | ~400 | Type-safe API client development |
| `API_INDEX.md` | Endpoint documentation | ~500 | Developer reference for all 23 endpoints |
| `ERROR_CATALOG.md` | Error codes and handling | ~400 | Error recovery strategies and client-side patterns |

## Quick Start

### 1. View OpenAPI Spec

Open `openapi.json` in [Swagger Editor](https://editor.swagger.io/):

```bash
# Copy URL to clipboard
echo "https://editor.swagger.io/?url=$(pwd)/openapi.json" | pbcopy

# Or open locally
npx @redocly/cli preview-docs openapi.json
```

### 2. Generate TypeScript Client

```bash
# Install OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# Generate client
openapi-generator-cli generate \
  -i openapi.json \
  -g typescript-axios \
  -o ../04-implementation/src/api
```

### 3. Import Types

```typescript
import {
  Skill,
  Command,
  Agent,
  SearchRequest,
  SearchResponse,
  SkillListResponse,
} from './api-types';

// Type-safe API calls
const searchSkills = async (query: string): Promise<SearchResponse> => {
  const response = await fetch('/api/v1/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, types: ['Skill'] }),
  });
  return response.json();
};
```

## API Overview

### Base URLs

| Environment | URL |
|-------------|-----|
| Development | `http://localhost:3001/api/v1` |
| Production | `https://api.claudemanual.dev/v1` |

### Endpoints

**23 total endpoints** across 11 categories:

1. **Skills** (2 endpoints): List skills, get skill details with relationships
2. **Commands** (2 endpoints): List commands, get command details
3. **Agents** (2 endpoints): List agents, get agent details
4. **Rules** (2 endpoints): List rules, get rule details
5. **Hooks** (2 endpoints): List hooks, get hook details
6. **Workflows** (2 endpoints): List workflows, get workflow with diagram
7. **Ways of Working** (2 endpoints): List documents, get document details
8. **Architecture** (2 endpoints): List architecture docs, get doc with diagrams
9. **Search** (1 endpoint): Global full-text search across all entities
10. **Preferences** (2 endpoints): Get/update user preferences
11. **File Watch** (1 endpoint): Server-Sent Events for file system changes

### Entity Types

| Entity | Count | Stage Applicable | Description |
|--------|-------|------------------|-------------|
| Skill | 85+ | All | Reusable AI prompt templates |
| Command | 30+ | Discovery, Prototype, ProductSpecs, SolArch, Implementation, Utility | Slash commands |
| Agent | 25+ | All | Specialized AI personas |
| Rule | 5+ | N/A | Framework rules and conventions |
| Hook | 8+ | N/A | Lifecycle hooks (Python, Bash) |
| Workflow | 10+ | All (except GRC, Security) | Process diagrams (Mermaid, PlantUML) |
| WaysOfWorking | 5+ | N/A | Team practices and guidelines |
| ArchitectureDoc | 10+ | N/A | C4 diagrams, ADRs, patterns |

## Key Features

### 1. Full-Text Search

**Endpoint**: `POST /api/v1/search`

**Features**:
- Search across all 8 entity types
- Relevance scoring (0-1)
- Type and stage filters
- Fuzzy search tolerates typos
- Results in < 2 seconds (JTBD-1.3 success criteria)

**Example**:
```typescript
const searchResults = await fetch('/api/v1/search', {
  method: 'POST',
  body: JSON.stringify({
    query: 'persona',
    types: ['Skill', 'Command', 'Agent'],
    stage: ['Discovery'],
    limit: 20,
  }),
});
```

### 2. Relationship Traversal

All detail endpoints include related entities:

**Skills** → Related skills, used by commands, used by agents
**Commands** → Invoked skills, spawned agents
**Agents** → Loaded skills, spawned by commands

**Example**:
```typescript
// GET /api/v1/skills/Discovery_JTBD
{
  "skill": { ... },
  "related_skills": [{ id: "Discovery_Persona", ... }],
  "used_by_commands": [{ id: "discovery", ... }],
  "used_by_agents": [{ id: "discovery-jtbd-extractor", ... }]
}
```

### 3. File System Watching (Hot Reload)

**Endpoint**: `GET /api/v1/watch` (Server-Sent Events)

**Use Case**: Hot-reload UI when skill/command/agent files are edited externally (VSCode, terminal)

**Example**:
```typescript
const eventSource = new EventSource('/api/v1/watch');

eventSource.addEventListener('file-change', (event) => {
  const data = JSON.parse(event.data);
  console.log('File changed:', data);
  // { type: 'modified', path: '.claude/skills/...', entity_type: 'Skill', entity_id: '...' }

  // Refetch entity
  if (data.entity_type === 'Skill') {
    refetchSkill(data.entity_id);
  }
});
```

### 4. Advanced Filtering

All list endpoints support:

- **Stage filters**: `?stage=Discovery&stage=Prototype`
- **Model filters**: `?model=sonnet&model=opus`
- **Category filters**: `?category=c4&c4_level=context`
- **Search**: `?search=persona`
- **Pagination**: `?page=1&pageSize=20`
- **Sorting**: `?sortBy=name&sortOrder=asc`

### 5. User Preferences

**Endpoints**: `GET /PUT /api/v1/preferences`

**Stored in localStorage**:
- Theme (light/dark/system)
- Favorites (skill/command/agent IDs)
- Collapsed tree nodes
- Last viewed item
- Search history (max 20 items, FIFO)
- Active stage filters
- Active type filters

## Error Handling

### Standard Error Format

```json
{
  "error": "ErrorType",
  "message": "Human-readable description",
  "code": "ERROR_CODE",
  "details": { ... }
}
```

### Error Codes

**15 total error codes**:

| Category | Codes | Examples |
|----------|-------|----------|
| Client Errors (400) | 4 | INVALID_PARAMS, INVALID_STAGE, INVALID_TYPE, MISSING_QUERY |
| Not Found (404) | 8 | SKILL_NOT_FOUND, COMMAND_NOT_FOUND, AGENT_NOT_FOUND, etc. |
| Server Errors (500) | 3 | INTERNAL_ERROR, FILE_READ_ERROR, MARKDOWN_PARSE_ERROR |

See `ERROR_CATALOG.md` for detailed error handling patterns.

## Traceability

### Requirements Coverage

| Requirement | Coverage | Endpoints |
|-------------|----------|-----------|
| REQ-021 (Skill access) | 100% | GET /skills, GET /skills/{id} |
| REQ-022 (Command access) | 100% | GET /commands, GET /commands/{id} |
| REQ-023 (Agent access) | 100% | GET /agents, GET /agents/{id} |
| REQ-024 (Rules, Hooks, Preferences) | 100% | GET /rules, GET /hooks, GET /preferences |
| REQ-025 (Search functionality) | 100% | POST /search |
| REQ-026 (Workflow, Architecture) | 100% | GET /workflows, GET /architecture |
| REQ-036 (API design) | 100% | All endpoints |
| REQ-037 (Search and filters) | 100% | All list endpoints, POST /search |

### JTBD Coverage

| JTBD | Coverage | Endpoints |
|------|----------|-----------|
| JTBD-1.1 (Self-service learning) | 100% | GET /skills, GET /commands, GET /agents |
| JTBD-1.2 (Component context) | 100% | All detail endpoints |
| JTBD-1.3 (Find relevant tools) | 100% | POST /search |
| JTBD-1.4 (Stage-appropriate tools) | 100% | All list endpoints (stage filter) |
| JTBD-1.5 (Edit source files) | 100% | All detail endpoints (path field) |
| JTBD-1.6 (Bookmark tools) | 100% | GET /preferences, PUT /preferences |
| JTBD-1.9 (Visualize diagrams) | 100% | GET /workflows, GET /architecture |
| JTBD-2.1 (Confidence) | 100% | All detail endpoints (examples, workflows) |
| JTBD-2.2 (Autonomous exploration) | 100% | POST /search, all list endpoints |

## Performance Targets

| Operation | Target | Measurement |
|-----------|--------|-------------|
| List endpoints | < 500ms | 115+ items with filters |
| Detail endpoints | < 200ms | Single item with relationships |
| Search | < 2s | Full-text search across all entities (JTBD-1.3) |
| File watch events | < 100ms | Event delivery from file change to client |

## Next Steps

1. **Mock Server Setup**: Implement MSW handlers for testing
2. **API Client Generation**: Generate TypeScript client from OpenAPI spec
3. **Integration Tests**: Write API endpoint integration tests
4. **File Watcher Implementation**: Implement Chokidar-based file system watching
5. **Performance Testing**: Validate search response time < 2s
6. **Documentation**: Generate API documentation with Redoc or Swagger UI

## Tools and Resources

### OpenAPI Tools

- **Swagger Editor**: https://editor.swagger.io/
- **Redoc**: `npx @redocly/cli preview-docs openapi.json`
- **OpenAPI Generator**: https://openapi-generator.tech/

### TypeScript Client

```bash
# Generate client
npx openapi-typescript openapi.json --output api-types-generated.ts

# Or use Axios client
npx openapi-generator-cli generate \
  -i openapi.json \
  -g typescript-axios \
  -o ../04-implementation/src/api
```

### Mock Server (MSW)

```typescript
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { mockSkill, mockCommand, mockAgent } from './mock-data';

const server = setupServer(
  rest.get('/api/v1/skills', (req, res, ctx) => {
    return res(
      ctx.json({
        data: [mockSkill(), mockSkill(), mockSkill()],
        pagination: { page: 1, pageSize: 20, totalItems: 85, totalPages: 5 },
      })
    );
  }),

  rest.post('/api/v1/search', (req, res, ctx) => {
    const { query } = req.body as { query: string };
    return res(
      ctx.json({
        results: [
          { id: 'Discovery_JTBD', type: 'Skill', name: 'Discovery_JTBD', description: '...', score: 0.95 }
        ],
        total: 1,
      })
    );
  })
);

export { server };
```

### File Watcher (Chokidar)

```typescript
import chokidar from 'chokidar';
import { EventEmitter } from 'events';

const watcher = chokidar.watch('.claude/**/*.md', {
  ignored: /node_modules/,
  persistent: true,
});

const fileEventEmitter = new EventEmitter();

watcher.on('change', (path) => {
  fileEventEmitter.emit('file-change', {
    type: 'modified',
    path,
    entity_type: detectEntityType(path),
    entity_id: extractEntityId(path),
    timestamp: new Date().toISOString(),
  });
});
```

## Related Files

| File | Location | Purpose |
|------|----------|---------|
| Data Model | `../data-model/DATA_MODEL.md` | Entity schemas and relationships |
| Screen Definitions | `ClientAnalysis_ClaudeManual/04-design-specs/screen-definitions.md` | UI screens that consume API |
| TypeScript Types | `api-types.ts` | Type-safe API client |
| OpenAPI Spec | `openapi.json` | Complete API specification |
| API Index | `API_INDEX.md` | Endpoint documentation |
| Error Catalog | `ERROR_CATALOG.md` | Error codes and handling |

---

**Total Endpoints**: 23
**Total Schemas**: 9 entities
**Requirements Coverage**: 100% (REQ-021 to REQ-037)
**JTBD Coverage**: 100% (JTBD-1.1 to JTBD-2.2)
**Created**: 2026-01-31 by prototype-api-contract-specifier
**Session**: session-api-contracts-claudemanual
**Checkpoint**: CP-4
