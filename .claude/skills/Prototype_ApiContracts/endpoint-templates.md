# Endpoint Templates

Templates for API endpoint definitions used by Prototype_ApiContracts.

---

## CRUD Endpoint Set Template

For each core entity, generate these 5 endpoints:

### List (GET /)

```json
{
  "id": "list[Entity]s",
  "method": "GET",
  "path": "/[entities]",
  "summary": "List all [entities] with filtering and pagination",
  "parameters": {
    "query": [
      { "name": "page", "type": "integer", "default": 1, "description": "Page number" },
      { "name": "limit", "type": "integer", "default": 20, "max": 100, "description": "Items per page" },
      { "name": "sort", "type": "string", "default": "createdAt:desc", "description": "Sort field:direction" },
      { "name": "search", "type": "string", "description": "Search in name/email fields" },
      { "name": "status", "type": "string", "enum": "[StatusEnum]", "description": "Filter by status" }
    ]
  },
  "responses": {
    "200": {
      "description": "List of [entities]",
      "schema": { "$ref": "#/schemas/[Entity]ListResponse" }
    },
    "400": { "$ref": "#/responses/ValidationError" },
    "401": { "$ref": "#/responses/Unauthorized" }
  }
}
```

### Get One (GET /:id)

```json
{
  "id": "get[Entity]",
  "method": "GET",
  "path": "/[entities]/{id}",
  "summary": "Get [entity] by ID",
  "parameters": {
    "path": [
      { "name": "id", "type": "string", "format": "uuid", "required": true }
    ],
    "query": [
      { "name": "include", "type": "array", "items": "string", "description": "Related data to include" }
    ]
  },
  "responses": {
    "200": {
      "description": "[Entity] details",
      "schema": { "$ref": "#/schemas/[Entity]Response" }
    },
    "404": { "$ref": "#/responses/NotFound" }
  }
}
```

### Create (POST /)

```json
{
  "id": "create[Entity]",
  "method": "POST",
  "path": "/[entities]",
  "summary": "Create new [entity]",
  "requestBody": {
    "required": true,
    "schema": { "$ref": "#/schemas/Create[Entity]Request" }
  },
  "responses": {
    "201": {
      "description": "[Entity] created",
      "schema": { "$ref": "#/schemas/[Entity]Response" }
    },
    "400": { "$ref": "#/responses/ValidationError" },
    "409": { "$ref": "#/responses/Conflict" }
  }
}
```

### Update (PATCH /:id)

```json
{
  "id": "update[Entity]",
  "method": "PATCH",
  "path": "/[entities]/{id}",
  "summary": "Update [entity]",
  "parameters": {
    "path": [
      { "name": "id", "type": "string", "format": "uuid", "required": true }
    ]
  },
  "requestBody": {
    "schema": { "$ref": "#/schemas/Update[Entity]Request" }
  },
  "responses": {
    "200": {
      "description": "[Entity] updated",
      "schema": { "$ref": "#/schemas/[Entity]Response" }
    },
    "400": { "$ref": "#/responses/ValidationError" },
    "404": { "$ref": "#/responses/NotFound" },
    "409": { "$ref": "#/responses/Conflict" }
  }
}
```

### Delete (DELETE /:id)

```json
{
  "id": "delete[Entity]",
  "method": "DELETE",
  "path": "/[entities]/{id}",
  "summary": "Delete [entity]",
  "parameters": {
    "path": [
      { "name": "id", "type": "string", "format": "uuid", "required": true }
    ]
  },
  "responses": {
    "204": { "description": "Successfully deleted" },
    "404": { "$ref": "#/responses/NotFound" },
    "409": { "$ref": "#/responses/Conflict", "description": "Cannot delete: has related records" }
  }
}
```

---

## Nested Endpoint Template

For parent-child relationships:

```json
{
  "id": "get[Parent][Children]",
  "method": "GET",
  "path": "/[parents]/{parentId}/[children]",
  "summary": "Get all [children] for a [parent]",
  "parameters": {
    "path": [
      { "name": "parentId", "type": "string", "format": "uuid", "required": true }
    ],
    "query": [
      { "name": "page", "type": "integer", "default": 1 },
      { "name": "limit", "type": "integer", "default": 20 }
    ]
  },
  "responses": {
    "200": {
      "schema": { "$ref": "#/schemas/[Child]ListResponse" }
    },
    "404": { "$ref": "#/responses/NotFound", "description": "[Parent] not found" }
  }
}
```

---

## Bulk Operations Template

### Bulk Update

```json
{
  "id": "bulkUpdate[Entity]s",
  "method": "PATCH",
  "path": "/[entities]/bulk",
  "summary": "Update multiple [entities]",
  "requestBody": {
    "schema": {
      "type": "object",
      "properties": {
        "ids": { "type": "array", "items": { "type": "string" } },
        "updates": { "$ref": "#/schemas/Update[Entity]Request" }
      },
      "required": ["ids", "updates"]
    }
  },
  "responses": {
    "200": {
      "schema": {
        "type": "object",
        "properties": {
          "updated": { "type": "integer" },
          "failed": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  }
}
```

### Bulk Delete

```json
{
  "id": "bulkDelete[Entity]s",
  "method": "DELETE",
  "path": "/[entities]/bulk",
  "summary": "Delete multiple [entities]",
  "requestBody": {
    "schema": {
      "type": "object",
      "properties": {
        "ids": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["ids"]
    }
  },
  "responses": {
    "200": {
      "schema": {
        "type": "object",
        "properties": {
          "deleted": { "type": "integer" },
          "failed": { "type": "array", "items": { "type": "string" } }
        }
      }
    }
  }
}
```

---

## Aggregation Endpoint Template

```json
{
  "id": "get[Report]Metrics",
  "method": "GET",
  "path": "/reports/[report-name]",
  "summary": "Get [report] metrics",
  "parameters": {
    "query": [
      { "name": "dateFrom", "type": "string", "format": "date" },
      { "name": "dateTo", "type": "string", "format": "date" },
      { "name": "groupBy", "type": "string", "enum": ["day", "week", "month"] }
    ]
  },
  "responses": {
    "200": {
      "schema": { "$ref": "#/schemas/[Report]Response" }
    }
  }
}
```

---

## Response Schema Templates

### Single Entity Response

```json
{
  "[Entity]Response": {
    "type": "object",
    "properties": {
      "data": { "$ref": "#/schemas/[Entity]" },
      "included": {
        "type": "object",
        "description": "Related entities if requested via include param"
      }
    }
  }
}
```

### List Response

```json
{
  "[Entity]ListResponse": {
    "type": "object",
    "properties": {
      "data": {
        "type": "array",
        "items": { "$ref": "#/schemas/[Entity]" }
      },
      "pagination": {
        "type": "object",
        "properties": {
          "total": { "type": "integer" },
          "page": { "type": "integer" },
          "limit": { "type": "integer" },
          "hasMore": { "type": "boolean" }
        }
      }
    }
  }
}
```

### Error Response

```json
{
  "ApiError": {
    "type": "object",
    "properties": {
      "type": { "type": "string", "format": "uri" },
      "title": { "type": "string" },
      "status": { "type": "integer" },
      "detail": { "type": "string" },
      "instance": { "type": "string" },
      "errors": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "field": { "type": "string" },
            "message": { "type": "string" },
            "code": { "type": "string" }
          }
        }
      }
    },
    "required": ["type", "title", "status"]
  }
}
```

---

## Common Error Responses

```json
{
  "responses": {
    "NotFound": {
      "description": "Resource not found",
      "schema": { "$ref": "#/schemas/ApiError" },
      "example": {
        "type": "https://api.example.com/errors/not-found",
        "title": "Not Found",
        "status": 404,
        "detail": "Resource with ID 'abc123' not found"
      }
    },
    "ValidationError": {
      "description": "Validation failed",
      "schema": { "$ref": "#/schemas/ApiError" },
      "example": {
        "type": "https://api.example.com/errors/validation",
        "title": "Validation Error",
        "status": 400,
        "detail": "Request validation failed",
        "errors": [
          { "field": "email", "message": "Invalid email format", "code": "INVALID_FORMAT" }
        ]
      }
    },
    "Conflict": {
      "description": "Resource conflict",
      "schema": { "$ref": "#/schemas/ApiError" },
      "example": {
        "type": "https://api.example.com/errors/conflict",
        "title": "Conflict",
        "status": 409,
        "detail": "A resource with this identifier already exists"
      }
    },
    "Unauthorized": {
      "description": "Authentication required",
      "schema": { "$ref": "#/schemas/ApiError" },
      "example": {
        "type": "https://api.example.com/errors/unauthorized",
        "title": "Unauthorized",
        "status": 401,
        "detail": "Valid authentication credentials required"
      }
    }
  }
}
```
