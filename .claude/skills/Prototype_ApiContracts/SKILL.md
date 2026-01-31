---
name: specifying-api-contracts
description: Use when you need to generate comprehensive API specifications (endpoints, types, mocks, OpenAPI) for prototype foundation.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill specifying-api-contracts started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill specifying-api-contracts ended '{"stage": "prototype"}'
---

# Spec API Contracts

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill specifying-api-contracts instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_ApiContracts
- **Version**: 1.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v1.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v1.0.0 (2025-01-15): Initial skill version

## Description
Generate comprehensive API specifications with endpoint docs, TypeScript types, examples, mock handlers, and OpenAPI specification.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: Resource names and endpoints shown below (e.g., `/candidates`, `/positions`, `/applications`) are examples from an ATS domain. Your actual API resources should be derived from your project's data model.

## Output Structure (REQUIRED)

This skill MUST generate the following structure pattern:

```
00-foundation/api-contracts/
├── API_CONTRACTS.md                  # Overview and conventions
├── endpoints/
│   ├── applications.api.md           # Per-entity endpoint specs
│   ├── availability.api.md
│   ├── candidates.api.md
│   ├── documents.api.md
│   ├── feedback.api.md
│   ├── interviews.api.md
│   ├── messages.api.md
│   ├── positions.api.md
│   ├── reports.api.md
│   └── users.api.md
├── examples/
│   ├── curl-examples.md              # cURL command examples
│   └── fetch-examples.js             # JavaScript fetch examples
├── mocks/
│   ├── data/
│   │   └── mock-data.json            # Mock response data
│   ├── handlers/
│   │   ├── candidates.mock.js        # MSW handlers per entity
│   │   ├── applications.mock.js
│   │   └── {entity}.mock.js
│   └── README.md
├── openapi.yaml                      # OpenAPI 3.0 specification
└── types/
    ├── entities.d.ts                 # Entity type definitions
    ├── errors.d.ts                   # Error type definitions
    ├── index.d.ts                    # Type exports
    ├── requests.d.ts                 # Request payload types
    └── responses.d.ts                # Response payload types
```

State file:
```
_state/api_contracts.json             # Machine-readable endpoint registry
```

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ _state/data_model.json → entities and relationships
READ _state/requirements_registry.json → API requirements
READ 00-foundation/data-model/entities/*.schema.json → entity schemas

IDENTIFY requirements this skill MUST address:
  - FR-XXX related to data operations
  - US-XXX that involve API calls
  - NFR-XXX for performance/security
  
IF data_model.json missing:
  BLOCK: "Run DataModel first"
  
IF requirements_registry missing:
  BLOCK: "Run Requirements first"
```

### Step 2: Identify API Resources
```
FOR each entity in data_model:
  DETERMINE if entity needs API endpoints:
    core entities → full CRUD
    transactional → full CRUD + bulk operations
    catalog → read-only (GET, LIST)
    audit → read-only (LIST with filters)
    
CREATE resource_list:
  - candidates (core) → full CRUD
  - applications (transactional) → full CRUD + bulk
  - departments (catalog) → read-only
```

### Step 3: Generate Endpoint Specs

#### 3a: Per-Entity API Files
```
FOR each resource:

  CREATE 00-foundation/api-contracts/endpoints/{resource}.api.md:
    # {Resource} API
    
    ## Overview
    Base URL: `/api/v1/{resource}`
    Entity: {Entity}
    Operations: [list of operations]
    
    ## Requirements Addressed
    | Req ID | Description | Endpoint |
    |--------|-------------|----------|
    | FR-003 | Create candidates | POST /candidates |
    | US-001 | List candidates | GET /candidates |
    
    ---
    
    ## Endpoints
    
    ### List {Resources}
    `GET /api/v1/{resources}`
    
    **Description:** Retrieve paginated list of {resources}
    
    **Query Parameters:**
    | Parameter | Type | Required | Default | Description |
    |-----------|------|----------|---------|-------------|
    | page | integer | No | 1 | Page number |
    | limit | integer | No | 20 | Items per page (max 100) |
    | sort | string | No | createdAt | Sort field |
    | order | string | No | desc | Sort order (asc/desc) |
    | search | string | No | - | Search query |
    | status | string | No | - | Filter by status |
    
    **Response:** `200 OK`
    ```json
    {
      "data": [...],
      "pagination": {
        "page": 1,
        "limit": 20,
        "total": 150,
        "totalPages": 8
      }
    }
    ```
    
    **Errors:**
    | Code | Description |
    |------|-------------|
    | 400 | Invalid query parameters |
    | 401 | Not authenticated |
    | 403 | Not authorized |
    
    ---
    
    ### Get {Resource}
    `GET /api/v1/{resources}/:id`
    
    **Description:** Retrieve single {resource} by ID
    
    **Path Parameters:**
    | Parameter | Type | Description |
    |-----------|------|-------------|
    | id | uuid | {Resource} ID |
    
    **Response:** `200 OK`
    ```json
    {
      "id": "...",
      "createdAt": "...",
      ...
    }
    ```
    
    **Errors:**
    | Code | Description |
    |------|-------------|
    | 404 | {Resource} not found |
    
    ---
    
    ### Create {Resource}
    `POST /api/v1/{resources}`
    
    **Request Body:**
    ```json
    {
      "field1": "value",
      "field2": "value"
    }
    ```
    
    **Response:** `201 Created`
    
    **Errors:**
    | Code | Description |
    |------|-------------|
    | 400 | Validation error |
    | 409 | Duplicate entry |
    
    ---
    
    ### Update {Resource}
    `PATCH /api/v1/{resources}/:id`
    
    **Request Body:** Partial update
    
    **Response:** `200 OK`
    
    ---
    
    ### Delete {Resource}
    `DELETE /api/v1/{resources}/:id`
    
    **Response:** `204 No Content`
    
    **Errors:**
    | Code | Description |
    |------|-------------|
    | 404 | Not found |
    | 409 | Cannot delete (has dependencies) |
```

### Step 4: Generate TypeScript Types
```
CREATE 00-foundation/api-contracts/types/entities.d.ts:
  // Generated from data model schemas
  
  export interface Candidate {
    id: string;
    firstName: string;
    lastName: string;
    email: string;
    phone?: string;
    status: CandidateStatus;
    createdAt: string;
    updatedAt: string;
  }
  
  export type CandidateStatus = 
    | 'new' 
    | 'screening' 
    | 'interview' 
    | 'offer' 
    | 'hired' 
    | 'rejected';
  
  // ... all entities

CREATE 00-foundation/api-contracts/types/requests.d.ts:
  export interface CreateCandidateRequest {
    firstName: string;
    lastName: string;
    email: string;
    phone?: string;
  }
  
  export interface UpdateCandidateRequest {
    firstName?: string;
    lastName?: string;
    email?: string;
    phone?: string;
    status?: CandidateStatus;
  }
  
  // ... all request types

CREATE 00-foundation/api-contracts/types/responses.d.ts:
  export interface PaginatedResponse<T> {
    data: T[];
    pagination: {
      page: number;
      limit: number;
      total: number;
      totalPages: number;
    };
  }
  
  export interface ErrorResponse {
    error: {
      code: string;
      message: string;
      details?: Record<string, string[]>;
    };
  }

CREATE 00-foundation/api-contracts/types/errors.d.ts:
  export interface ApiError {
    code: string;
    message: string;
    status: number;
  }
  
  export const ErrorCodes = {
    VALIDATION_ERROR: 'VALIDATION_ERROR',
    NOT_FOUND: 'NOT_FOUND',
    UNAUTHORIZED: 'UNAUTHORIZED',
    FORBIDDEN: 'FORBIDDEN',
    CONFLICT: 'CONFLICT',
  } as const;

CREATE 00-foundation/api-contracts/types/index.d.ts:
  export * from './entities';
  export * from './requests';
  export * from './responses';
  export * from './errors';
```

### Step 5: Generate Examples
```
CREATE 00-foundation/api-contracts/examples/curl-examples.md:
  # API Examples (cURL)
  
  ## Authentication
  All requests require Bearer token:
  ```bash
  -H "Authorization: Bearer <token>"
  ```
  
  ## Candidates
  
  ### List Candidates
  ```bash
  curl -X GET "https://api.example.com/v1/candidates?page=1&limit=20" \
    -H "Authorization: Bearer <token>"
  ```
  
  ### Create Candidate
  ```bash
  curl -X POST "https://api.example.com/v1/candidates" \
    -H "Authorization: Bearer <token>" \
    -H "Content-Type: application/json" \
    -d '{
      "firstName": "John",
      "lastName": "Doe",
      "email": "john.doe@example.com"
    }'
  ```
  
  [... all endpoints ...]

CREATE 00-foundation/api-contracts/examples/fetch-examples.js:
  // API Examples (JavaScript Fetch)
  
  const API_BASE = 'https://api.example.com/v1';
  
  // List candidates
  async function listCandidates(params = {}) {
    const query = new URLSearchParams(params);
    const response = await fetch(`${API_BASE}/candidates?${query}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return response.json();
  }
  
  // Create candidate
  async function createCandidate(data) {
    const response = await fetch(`${API_BASE}/candidates`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return response.json();
  }
  
  // ... all endpoints
```

### Step 6: Generate Mock Handlers
```
CREATE 00-foundation/api-contracts/mocks/handlers/{entity}.mock.js:
  // MSW Mock Handlers for {Entity}
  import { rest } from 'msw';
  import { mockData } from '../data/mock-data.json';
  
  export const {entity}Handlers = [
    // List
    rest.get('/api/v1/{entities}', (req, res, ctx) => {
      const page = Number(req.url.searchParams.get('page')) || 1;
      const limit = Number(req.url.searchParams.get('limit')) || 20;
      
      const start = (page - 1) * limit;
      const data = mockData.{entities}.slice(start, start + limit);
      
      return res(
        ctx.status(200),
        ctx.json({
          data,
          pagination: {
            page,
            limit,
            total: mockData.{entities}.length,
            totalPages: Math.ceil(mockData.{entities}.length / limit),
          },
        })
      );
    }),
    
    // Get by ID
    rest.get('/api/v1/{entities}/:id', (req, res, ctx) => {
      const { id } = req.params;
      const item = mockData.{entities}.find(i => i.id === id);
      
      if (!item) {
        return res(ctx.status(404), ctx.json({ error: 'Not found' }));
      }
      
      return res(ctx.status(200), ctx.json(item));
    }),
    
    // Create
    rest.post('/api/v1/{entities}', async (req, res, ctx) => {
      const body = await req.json();
      const newItem = {
        id: crypto.randomUUID(),
        ...body,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      
      return res(ctx.status(201), ctx.json(newItem));
    }),
    
    // Update
    rest.patch('/api/v1/{entities}/:id', async (req, res, ctx) => {
      const { id } = req.params;
      const body = await req.json();
      // Update logic...
      return res(ctx.status(200), ctx.json({ ...body, id }));
    }),
    
    // Delete
    rest.delete('/api/v1/{entities}/:id', (req, res, ctx) => {
      return res(ctx.status(204));
    }),
  ];

CREATE 00-foundation/api-contracts/mocks/README.md:
  # Mock API Handlers
  
  ## Setup
  ```javascript
  import { setupWorker } from 'msw';
  import { candidatesHandlers } from './handlers/candidates.mock';
  import { applicationsHandlers } from './handlers/applications.mock';
  
  const worker = setupWorker(
    ...candidatesHandlers,
    ...applicationsHandlers,
    // ... other handlers
  );
  
  worker.start();
  ```
  
  ## Usage
  Mock handlers intercept API requests during development.
```

### Step 7: Generate OpenAPI Spec
```
CREATE 00-foundation/api-contracts/openapi.yaml:
  openapi: 3.0.3
  info:
    title: {Product Name} API
    version: 1.0.0
    description: API specification for {Product Name}
  
  servers:
    - url: https://api.example.com/v1
      description: Production
    - url: http://localhost:3000/api/v1
      description: Development
  
  security:
    - bearerAuth: []
  
  paths:
    /candidates:
      get:
        summary: List candidates
        tags: [Candidates]
        parameters:
          - name: page
            in: query
            schema:
              type: integer
              default: 1
          - name: limit
            in: query
            schema:
              type: integer
              default: 20
        responses:
          '200':
            description: Success
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/CandidateListResponse'
      post:
        summary: Create candidate
        tags: [Candidates]
        requestBody:
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CreateCandidateRequest'
        responses:
          '201':
            description: Created
  
  components:
    securitySchemes:
      bearerAuth:
        type: http
        scheme: bearer
    schemas:
      Candidate:
        type: object
        properties:
          id:
            type: string
            format: uuid
          firstName:
            type: string
          lastName:
            type: string
          email:
            type: string
            format: email
      # ... all schemas
```

### Step 8: Generate API Overview
```
CREATE 00-foundation/api-contracts/API_CONTRACTS.md:
  # API Contracts Overview
  
  ## Base URL
  - Production: `https://api.example.com/v1`
  - Development: `http://localhost:3000/api/v1`
  
  ## Authentication
  All endpoints require Bearer token authentication.
  
  ## Rate Limiting
  - 100 requests per minute per user
  - 429 Too Many Requests when exceeded
  
  ## Pagination
  All list endpoints support pagination:
  - `page`: Page number (default: 1)
  - `limit`: Items per page (default: 20, max: 100)
  
  ## Error Handling
  All errors follow standard format:
  ```json
  {
    "error": {
      "code": "VALIDATION_ERROR",
      "message": "Validation failed",
      "details": {...}
    }
  }
  ```
  
  ## Endpoint Index
  | Resource | Endpoints | File |
  |----------|-----------|------|
  | Candidates | 5 | [candidates.api.md](endpoints/candidates.api.md) |
  | Applications | 6 | [applications.api.md](endpoints/applications.api.md) |
  ...
  
  ## Requirements Coverage
  | Req ID | Endpoint | Status |
  |--------|----------|--------|
  | FR-003 | POST /candidates | ✅ |
```

### Step 9: Validate Outputs (REQUIRED)
```
VALIDATE API contracts:
  DIRECTORY CHECKS:
    - endpoints/ contains file for each resource entity
    - types/ contains all 4 type files
    - examples/ contains curl and fetch examples
    - mocks/handlers/ contains handler per entity
    - openapi.yaml exists and valid YAML
    - API_CONTRACTS.md exists
    
  CONTENT CHECKS:
    - Each endpoint file has Requirements Addressed
    - OpenAPI covers all endpoints
    - Types match data model schemas
    
IF any validation fails:
  PROMPT with mitigation options
```

### Step 10: Update Progress
```
WRITE _state/api_contracts.json

UPDATE _state/progress.json:
  phases.api_contracts.status = "complete"
  phases.api_contracts.completed_at = timestamp
  phases.api_contracts.outputs = [
    "00-foundation/api-contracts/API_CONTRACTS.md",
    "00-foundation/api-contracts/endpoints/*.api.md",
    "00-foundation/api-contracts/types/*.d.ts",
    "00-foundation/api-contracts/examples/*.md",
    "00-foundation/api-contracts/examples/*.js",
    "00-foundation/api-contracts/mocks/**/*",
    "00-foundation/api-contracts/openapi.yaml"
  ]
  phases.api_contracts.metrics = {
    endpoint_count: count,
    resource_count: count,
    type_definitions: count
  }
```

---

## Output Files (REQUIRED)

| Path | Purpose | Blocking? |
|------|---------|-----------|
| `API_CONTRACTS.md` | Overview | ✅ Yes |
| `endpoints/{entity}.api.md` | Per-entity specs | ✅ Yes |
| `types/entities.d.ts` | Entity types | ✅ Yes |
| `types/requests.d.ts` | Request types | ✅ Yes |
| `types/responses.d.ts` | Response types | ✅ Yes |
| `types/errors.d.ts` | Error types | ✅ Yes |
| `types/index.d.ts` | Type exports | ✅ Yes |
| `examples/curl-examples.md` | cURL examples | ⚠️ Warning |
| `examples/fetch-examples.js` | JS examples | ⚠️ Warning |
| `mocks/handlers/*.mock.js` | MSW handlers | ⚠️ Warning |
| `mocks/README.md` | Mock setup guide | ⚠️ Warning |
| `openapi.yaml` | OpenAPI spec | ✅ Yes |

---

## Progress.json Update

```json
{
  "phases": {
    "api_contracts": {
      "status": "complete",
      "completed_at": "2024-12-13T10:45:00Z",
      "outputs": [
        "00-foundation/api-contracts/API_CONTRACTS.md",
        "00-foundation/api-contracts/endpoints/*.api.md",
        "00-foundation/api-contracts/types/*.d.ts",
        "00-foundation/api-contracts/openapi.yaml"
      ],
      "metrics": {
        "endpoint_count": 45,
        "resource_count": 10,
        "type_definitions": 35
      }
    }
  }
}
```
