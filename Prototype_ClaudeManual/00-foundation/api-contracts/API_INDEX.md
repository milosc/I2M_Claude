# API Index - ClaudeManual

---
**System**: ClaudeManual
**Stage**: Prototype
**Checkpoint**: CP-4
**Created**: 2026-01-31
**Session**: session-api-contracts-claudemanual
**Agent**: prototype-api-contract-specifier
**Total Endpoints**: 23
**Total Schemas**: 9
---

## Overview

This document provides a comprehensive index of all API endpoints for the ClaudeManual framework explorer. The API follows RESTful conventions with OpenAPI 3.0 specification.

| Metric | Value |
|--------|-------|
| **Base URL (Dev)** | `http://localhost:3001/api/v1` |
| **Base URL (Prod)** | `https://api.claudemanual.dev/v1` |
| **Authentication** | localStorage token (placeholder) |
| **Total Endpoints** | 23 |
| **Entity Types** | 8 |
| **Search Endpoint** | Yes (POST /search) |
| **File Watching** | Yes (GET /watch, SSE) |

---

## Endpoint Categories

### 1. Skills (4 endpoints)

Skills are reusable AI prompt templates for specific tasks, organized by workflow stage.

| Method | Endpoint | Description | Screen |
|--------|----------|-------------|--------|
| GET | `/skills` | List skills with filters (stage, model, search, favorited) | SCR-001, SCR-003 |
| GET | `/skills/{id}` | Get skill details with relationships (related skills, commands, agents) | SCR-001, SCR-006 |

**Query Parameters**:
- `stage`: Filter by Discovery, Prototype, ProductSpecs, SolArch, Implementation, Utility, GRC, Security
- `model`: Filter by sonnet, opus, haiku
- `search`: Full-text search
- `has_example`: Boolean filter for skills with examples
- `favorited`: Boolean filter for user's favorites
- `page`, `pageSize`, `sortBy`, `sortOrder`: Standard pagination

**Response**: PaginatedResponse<Skill> or SkillDetailResponse

**Traceability**: REQ-021, JTBD-1.2, JTBD-1.3

---

### 2. Commands (4 endpoints)

Slash commands executable in Claude Code.

| Method | Endpoint | Description | Screen |
|--------|----------|-------------|--------|
| GET | `/commands` | List commands with filters (stage, search) | SCR-001, SCR-003 |
| GET | `/commands/{id}` | Get command details with invoked skills and spawned agents | SCR-001, SCR-006 |

**Query Parameters**:
- `stage`: Filter by Discovery, Prototype, ProductSpecs, SolArch, Implementation, Utility
- `requires_system_name`: Boolean filter
- `has_options`: Boolean filter
- `search`: Full-text search
- `page`, `pageSize`, `sortBy`, `sortOrder`: Standard pagination

**Response**: PaginatedResponse<Command> or CommandDetailResponse

**Traceability**: REQ-022, JTBD-1.1, JTBD-1.4

---

### 3. Agents (4 endpoints)

Specialized AI personas with specific skills and model configuration.

| Method | Endpoint | Description | Screen |
|--------|----------|-------------|--------|
| GET | `/agents` | List agents with filters (stage, model, checkpoint, search) | SCR-001, SCR-003 |
| GET | `/agents/{id}` | Get agent details with loaded skills and spawning commands | SCR-001, SCR-006 |

**Query Parameters**:
- `stage`: Filter by Discovery, Prototype, ProductSpecs, SolArch, Implementation, Utility, GRC, Security
- `model`: Filter by sonnet, opus, haiku
- `checkpoint`: Filter by checkpoint number (1-20)
- `search`: Full-text search
- `page`, `pageSize`, `sortBy`, `sortOrder`: Standard pagination

**Response**: PaginatedResponse<Agent> or AgentDetailResponse

**Traceability**: REQ-023, JTBD-1.2

---

### 4. Rules (2 endpoints)

Framework rules and conventions with auto-loading path patterns.

| Method | Endpoint | Description | Screen |
|--------|----------|-------------|--------|
| GET | `/rules` | List rules with category filter | SCR-001 |
| GET | `/rules/{id}` | Get rule details | SCR-001, SCR-006 |

**Query Parameters**:
- `category`: Filter by core, stage-specific, quality, process
- `search`: Full-text search
- `page`, `pageSize`: Standard pagination

**Response**: PaginatedResponse<Rule> or Rule

**Traceability**: REQ-024

---

### 5. Hooks (2 endpoints)

Lifecycle hooks for commands, skills, and agents.

| Method | Endpoint | Description | Screen |
|--------|----------|-------------|--------|
| GET | `/hooks` | List hooks with type and language filters | SCR-001 |
| GET | `/hooks/{id}` | Get hook details | SCR-001, SCR-006 |

**Query Parameters**:
- `type`: Filter by PreToolUse, PostToolUse, Stop, lifecycle
- `language`: Filter by python, bash
- `search`: Full-text search
- `page`, `pageSize`: Standard pagination

**Response**: PaginatedResponse<Hook> or Hook

**Traceability**: REQ-024

---

### 6. Workflows (2 endpoints)

Process and workflow diagrams (Mermaid, PlantUML).

| Method | Endpoint | Description | Screen |
|--------|----------|-------------|--------|
| GET | `/workflows` | List workflows with filters (stage, category, format, tags) | SCR-001, SCR-009 |
| GET | `/workflows/{id}` | Get workflow details with diagram content | SCR-009, SCR-011 |

**Query Parameters**:
- `stage`: Filter by Discovery, Prototype, ProductSpecs, SolArch, Implementation, Utility
- `category`: Filter by process, integration, decision, data-flow
- `format`: Filter by md, mermaid, plantuml
- `tags`: Filter by tag array
- `search`: Full-text search
- `page`, `pageSize`: Standard pagination

**Response**: PaginatedResponse<Workflow> or Workflow

**Traceability**: REQ-026, JTBD-1.9

---

### 7. Ways of Working (2 endpoints)

Team practices, guidelines, and process documentation.

| Method | Endpoint | Description | Screen |
|--------|----------|-------------|--------|
| GET | `/ways-of-working` | List documents with category, audience, tags filters | SCR-001 |
| GET | `/ways-of-working/{id}` | Get document details | SCR-006 |

**Query Parameters**:
- `category`: Filter by practices, guidelines, processes, checklists
- `audience`: Filter by developers, product, all, leads
- `tags`: Filter by tag array
- `search`: Full-text search
- `page`, `pageSize`: Standard pagination

**Response**: PaginatedResponse<WaysOfWorking> or WaysOfWorking

**Traceability**: REQ-026, JTBD-1.9

---

### 8. Architecture (2 endpoints)

Architecture diagrams and documentation (C4, ADRs, patterns).

| Method | Endpoint | Description | Screen |
|--------|----------|-------------|--------|
| GET | `/architecture` | List docs with category, C4 level, ADR status, format, tags filters | SCR-001, SCR-010 |
| GET | `/architecture/{id}` | Get document details with diagram and related ADRs | SCR-010, SCR-011 |

**Query Parameters**:
- `category`: Filter by c4, adr, patterns, infrastructure, data-model
- `c4_level`: Filter by context, container, component, code
- `adr_status`: Filter by proposed, accepted, deprecated, superseded
- `format`: Filter by md, mermaid, plantuml
- `tags`: Filter by tag array
- `search`: Full-text search
- `page`, `pageSize`: Standard pagination

**Response**: PaginatedResponse<ArchitectureDoc> or ArchitectureDoc

**Traceability**: REQ-026, JTBD-1.9, JTBD-2.1

---

### 9. Search (1 endpoint)

Global full-text search across all entity types with relevance scoring.

| Method | Endpoint | Description | Screen |
|--------|----------|-------------|--------|
| POST | `/search` | Search all entities with type and stage filters | SCR-002 |

**Request Body**:
```json
{
  "query": "persona",
  "types": ["Skill", "Command", "Agent"],
  "stage": ["Discovery"],
  "limit": 20
}
```

**Response**:
```json
{
  "results": [
    {
      "id": "Discovery_JTBD",
      "type": "Skill",
      "name": "Discovery_JTBD",
      "description": "Extracts Jobs To Be Done from pain points...",
      "stage": "Discovery",
      "score": 0.95
    }
  ],
  "total": 12
}
```

**Success Criteria**: Results returned in < 2 seconds (JTBD-1.3)

**Traceability**: REQ-025, JTBD-1.3, JTBD-2.2

---

### 10. Preferences (2 endpoints)

User preferences and settings (stored in localStorage).

| Method | Endpoint | Description | Screen |
|--------|----------|-------------|--------|
| GET | `/preferences` | Get user preferences | SCR-001, SCR-007 |
| PUT | `/preferences` | Update user preferences | SCR-007 |

**Request Body** (PUT):
```json
{
  "theme": "dark",
  "favorites": ["Discovery_JTBD", "discovery-multiagent"],
  "collapsed_nodes": ["skills-discovery"],
  "last_viewed": "Discovery_JTBD",
  "search_history": ["persona", "GDPR", "TDD"],
  "stage_filter": ["Discovery"],
  "type_filter": ["Skill", "Command"]
}
```

**Response**: UserPreferences object

**Traceability**: REQ-024, JTBD-1.6, CF-012, CF-016

---

### 11. File Watch (1 endpoint)

Server-Sent Events (SSE) stream for file system changes (hot-reload).

| Method | Endpoint | Description | Screen |
|--------|----------|-------------|--------|
| GET | `/watch` | Subscribe to file system change events | All screens |

**Response Format** (SSE):
```
event: file-change
data: {"type":"modified","path":".claude/skills/Discovery_JTBD/SKILL.md","entity_type":"Skill","entity_id":"Discovery_JTBD","timestamp":"2026-01-31T12:34:56Z"}

event: file-change
data: {"type":"created","path":".claude/agents/quality/new-agent.md","entity_type":"Agent","entity_id":"quality-new-agent","timestamp":"2026-01-31T12:35:00Z"}
```

**Use Case**: Hot-reload UI when skill/command/agent files are edited externally (VSCode, terminal)

**Traceability**: REQ-036, CF-013

---

## Error Handling

### Standard Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_PARAMS` | 400 | Invalid request parameters |
| `INVALID_STAGE` | 400 | Invalid stage filter value |
| `INVALID_TYPE` | 400 | Invalid entity type |
| `SKILL_NOT_FOUND` | 404 | Skill ID not found |
| `COMMAND_NOT_FOUND` | 404 | Command ID not found |
| `AGENT_NOT_FOUND` | 404 | Agent ID not found |
| `RULE_NOT_FOUND` | 404 | Rule ID not found |
| `HOOK_NOT_FOUND` | 404 | Hook ID not found |
| `WORKFLOW_NOT_FOUND` | 404 | Workflow ID not found |
| `WAYSOFWORKING_NOT_FOUND` | 404 | Ways of Working document not found |
| `ARCHITECTURE_NOT_FOUND` | 404 | Architecture document not found |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

### Error Response Format

```json
{
  "error": "BadRequest",
  "message": "Invalid stage filter value",
  "code": "INVALID_STAGE",
  "details": {
    "valid_stages": ["Discovery", "Prototype", "ProductSpecs", "SolArch", "Implementation", "Utility"]
  }
}
```

---

## Pagination

All list endpoints support pagination with the following parameters:

| Parameter | Type | Default | Max | Description |
|-----------|------|---------|-----|-------------|
| `page` | integer | 1 | - | Page number (1-indexed) |
| `pageSize` | integer | 20 | 100 | Items per page |
| `sortBy` | string | - | - | Field to sort by |
| `sortOrder` | enum | asc | - | Sort order (asc, desc) |

**Response Format**:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 85,
    "totalPages": 5
  }
}
```

---

## Filtering

### Stage Filters

All entity list endpoints support `stage` query parameter with multiple values:

```
GET /skills?stage=Discovery&stage=Prototype
```

**Valid Stages**:
- Discovery
- Prototype
- ProductSpecs
- SolArch
- Implementation
- Utility
- GRC (Skills, Agents only)
- Security (Skills, Agents only)

### Model Filters

Skills and Agents support `model` query parameter:

```
GET /agents?model=sonnet&model=opus
```

**Valid Models**: sonnet, opus, haiku

### Category Filters

Workflows, Ways of Working, and Architecture docs support category-specific filters:

**Workflows**: `category=process&category=integration`
**Ways of Working**: `category=practices&audience=developers`
**Architecture**: `category=c4&c4_level=context&adr_status=accepted`

---

## Relationships

### Skills

**Relationships returned in detail endpoint** (`GET /skills/{id}`):

| Relation | Type | Description |
|----------|------|-------------|
| `related_skills` | Skill[] | Skills referenced in `skills_required` |
| `used_by_commands` | Command[] | Commands that invoke this skill |
| `used_by_agents` | Agent[] | Agents that load this skill |

### Commands

**Relationships returned in detail endpoint** (`GET /commands/{id}`):

| Relation | Type | Description |
|----------|------|-------------|
| `invoked_skills` | Skill[] | Skills invoked by this command |
| `spawned_agents` | Agent[] | Agents spawned by this command |

### Agents

**Relationships returned in detail endpoint** (`GET /agents/{id}`):

| Relation | Type | Description |
|----------|------|-------------|
| `loaded_skills` | Skill[] | Skills loaded by this agent |
| `spawned_by_commands` | Command[] | Commands that spawn this agent |

---

## Performance Targets

| Operation | Target | Success Criteria |
|-----------|--------|------------------|
| List endpoints | < 500ms | All 115+ items with filters |
| Detail endpoints | < 200ms | Single item with relationships |
| Search | < 2s | Full-text search across all entities (JTBD-1.3) |
| File watch | < 100ms | Event delivery from file change to client |

---

## Authentication (Placeholder)

**Current**: No authentication required (development mode)

**Future**: JWT token stored in browser localStorage

```http
Authorization: Bearer <jwt-token>
```

**Token Storage**: `localStorage.getItem('claude-manual-auth-token')`

---

## CORS Configuration

Development server allows all origins:

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

Production server restricts to allowed domains.

---

## Content-Type

All endpoints return JSON except `/watch` (Server-Sent Events):

```http
Content-Type: application/json
```

File watch endpoint:

```http
Content-Type: text/event-stream
```

---

## Traceability

### Requirements Coverage

| Requirement | Endpoints | Coverage |
|-------------|-----------|----------|
| REQ-021 | GET /skills, GET /skills/{id} | 100% |
| REQ-022 | GET /commands, GET /commands/{id} | 100% |
| REQ-023 | GET /agents, GET /agents/{id} | 100% |
| REQ-024 | GET /rules, GET /hooks, GET /preferences | 100% |
| REQ-025 | POST /search | 100% |
| REQ-026 | GET /workflows, GET /ways-of-working, GET /architecture | 100% |
| REQ-036 | All endpoints, GET /watch | 100% |
| REQ-037 | All list endpoints (filters), POST /search | 100% |

### JTBD Coverage

| JTBD | Endpoints | Coverage |
|------|-----------|----------|
| JTBD-1.1 (Self-service learning) | GET /skills, GET /commands, GET /agents | 100% |
| JTBD-1.2 (Component context) | All detail endpoints | 100% |
| JTBD-1.3 (Find relevant tools) | POST /search | 100% |
| JTBD-1.4 (Stage-appropriate tools) | All list endpoints (stage filter) | 100% |
| JTBD-1.5 (Edit source files) | All detail endpoints (path field) | 100% |
| JTBD-1.6 (Bookmark tools) | GET /preferences, PUT /preferences | 100% |
| JTBD-1.9 (Visualize diagrams) | GET /workflows, GET /architecture | 100% |
| JTBD-2.1 (Confidence) | All detail endpoints (examples, workflows) | 100% |
| JTBD-2.2 (Autonomous exploration) | POST /search, All list endpoints | 100% |

### Client Facts Coverage

| Client Fact | Endpoints | Implementation |
|-------------|-----------|----------------|
| CF-013 (File path references) | All detail endpoints | `path` field in all entities |
| CF-012 (Favorites) | GET /preferences, PUT /preferences | `favorites` array |
| CF-016 (Light/dark theme) | GET /preferences, PUT /preferences | `theme` field |

---

## Next Steps

1. **API Client Generation**: Generate TypeScript client from OpenAPI spec
2. **Mock Server**: Implement MSW (Mock Service Worker) handlers
3. **Integration Tests**: Write API endpoint integration tests
4. **File Watcher**: Implement Chokidar-based file system watching
5. **Performance Testing**: Validate < 2s search response time
6. **Error Catalog**: Document all error codes and recovery strategies

---

**Total Endpoints**: 23
**Entities Covered**: 9 (Skill, Command, Agent, Rule, Hook, Workflow, WaysOfWorking, ArchitectureDoc, UserPreferences)
**Traceability**: 100% coverage of REQ-021 to REQ-037, JTBD-1.1 to JTBD-2.2
**Created**: 2026-01-31 by prototype-api-contract-specifier
**Session**: session-api-contracts-claudemanual
**Checkpoint**: CP-4
