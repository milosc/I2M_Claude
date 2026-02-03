# Error Catalog - ClaudeManual API

---
**System**: ClaudeManual
**Stage**: Prototype
**Checkpoint**: CP-4
**Created**: 2026-01-31
**Session**: session-api-contracts-claudemanual
**Agent**: prototype-api-contract-specifier
**Total Error Codes**: 15
---

## Overview

This document catalogs all error codes returned by the ClaudeManual API, including HTTP status codes, error messages, recovery strategies, and client-side handling patterns.

---

## Error Response Format

All API errors follow a consistent JSON format:

```json
{
  "error": "ErrorType",
  "message": "Human-readable error description",
  "code": "ERROR_CODE",
  "details": {
    "additionalContext": "value"
  }
}
```

---

## Client Errors (4xx)

### 400 Bad Request

#### ERR-001: INVALID_PARAMS

**Description**: Request parameters are invalid or malformed.

**Example Response**:
```json
{
  "error": "BadRequest",
  "message": "Invalid request parameters",
  "code": "INVALID_PARAMS",
  "details": {
    "field": "pageSize",
    "value": 150,
    "constraint": "maximum 100"
  }
}
```

**Common Causes**:
- `pageSize` > 100
- `page` < 1
- Invalid enum values for `stage`, `model`, `type`
- Malformed JSON in request body

**Client-Side Handling**:
```typescript
if (error.code === 'INVALID_PARAMS') {
  // Show validation error in UI
  showToast(`Invalid parameter: ${error.details.field}`, 'error');
  // Reset to default values
  resetFilters();
}
```

**Recovery**: Correct parameters and retry request.

---

#### ERR-002: INVALID_STAGE

**Description**: Invalid stage filter value provided.

**Example Response**:
```json
{
  "error": "BadRequest",
  "message": "Invalid stage filter value",
  "code": "INVALID_STAGE",
  "details": {
    "provided": "invalidStage",
    "valid_stages": ["Discovery", "Prototype", "ProductSpecs", "SolArch", "Implementation", "Utility"]
  }
}
```

**Common Causes**:
- Typo in stage name (e.g., "Discovry" instead of "Discovery")
- Using unsupported stage for entity type (e.g., "GRC" for Commands)

**Client-Side Handling**:
```typescript
if (error.code === 'INVALID_STAGE') {
  // Show available stages in dropdown
  updateStageFilter(error.details.valid_stages);
  showToast('Please select a valid stage', 'warning');
}
```

**Recovery**: Select valid stage from dropdown, retry request.

---

#### ERR-003: INVALID_TYPE

**Description**: Invalid entity type in search or filter.

**Example Response**:
```json
{
  "error": "BadRequest",
  "message": "Invalid entity type",
  "code": "INVALID_TYPE",
  "details": {
    "provided": "InvalidType",
    "valid_types": ["Skill", "Command", "Agent", "Rule", "Hook", "Workflow", "WaysOfWorking", "ArchitectureDoc"]
  }
}
```

**Client-Side Handling**:
```typescript
if (error.code === 'INVALID_TYPE') {
  // Reset type filter to default
  setTypeFilter(['Skill', 'Command', 'Agent']);
  showToast('Invalid entity type selected', 'error');
}
```

**Recovery**: Clear type filter, retry request.

---

#### ERR-004: MISSING_QUERY

**Description**: Search query parameter is required but missing.

**Example Response**:
```json
{
  "error": "BadRequest",
  "message": "Search query is required",
  "code": "MISSING_QUERY",
  "details": {
    "field": "query",
    "min_length": 1
  }
}
```

**Client-Side Handling**:
```typescript
if (error.code === 'MISSING_QUERY') {
  // Focus search input
  searchInputRef.current?.focus();
  showToast('Please enter a search query', 'warning');
}
```

**Recovery**: Enter search query, retry request.

---

### 404 Not Found

#### ERR-005: SKILL_NOT_FOUND

**Description**: Skill with specified ID does not exist.

**Example Response**:
```json
{
  "error": "NotFound",
  "message": "Skill not found",
  "code": "SKILL_NOT_FOUND",
  "details": {
    "id": "NonExistentSkill"
  }
}
```

**Client-Side Handling**:
```typescript
if (error.code === 'SKILL_NOT_FOUND') {
  // Show 404 page or fallback UI
  navigate('/404', { state: { entity: 'Skill', id: error.details.id } });
}
```

**Recovery**: Navigate back to list view or search.

---

#### ERR-006: COMMAND_NOT_FOUND

**Description**: Command with specified ID does not exist.

**Example Response**:
```json
{
  "error": "NotFound",
  "message": "Command not found",
  "code": "COMMAND_NOT_FOUND",
  "details": {
    "id": "nonexistent-command"
  }
}
```

**Client-Side Handling**: Same as ERR-005, replace entity type.

---

#### ERR-007: AGENT_NOT_FOUND

**Description**: Agent with specified ID does not exist.

**Example Response**:
```json
{
  "error": "NotFound",
  "message": "Agent not found",
  "code": "AGENT_NOT_FOUND",
  "details": {
    "id": "nonexistent-agent"
  }
}
```

**Client-Side Handling**: Same as ERR-005, replace entity type.

---

#### ERR-008: RULE_NOT_FOUND

**Description**: Rule with specified ID does not exist.

**Example Response**:
```json
{
  "error": "NotFound",
  "message": "Rule not found",
  "code": "RULE_NOT_FOUND",
  "details": {
    "id": "nonexistent-rule"
  }
}
```

**Client-Side Handling**: Same as ERR-005, replace entity type.

---

#### ERR-009: HOOK_NOT_FOUND

**Description**: Hook with specified ID does not exist.

**Example Response**:
```json
{
  "error": "NotFound",
  "message": "Hook not found",
  "code": "HOOK_NOT_FOUND",
  "details": {
    "id": "nonexistent-hook"
  }
}
```

**Client-Side Handling**: Same as ERR-005, replace entity type.

---

#### ERR-010: WORKFLOW_NOT_FOUND

**Description**: Workflow with specified ID does not exist.

**Example Response**:
```json
{
  "error": "NotFound",
  "message": "Workflow not found",
  "code": "WORKFLOW_NOT_FOUND",
  "details": {
    "id": "nonexistent-workflow"
  }
}
```

**Client-Side Handling**: Same as ERR-005, replace entity type.

---

#### ERR-011: WAYSOFWORKING_NOT_FOUND

**Description**: Ways of Working document with specified ID does not exist.

**Example Response**:
```json
{
  "error": "NotFound",
  "message": "Ways of Working document not found",
  "code": "WAYSOFWORKING_NOT_FOUND",
  "details": {
    "id": "nonexistent-wow"
  }
}
```

**Client-Side Handling**: Same as ERR-005, replace entity type.

---

#### ERR-012: ARCHITECTURE_NOT_FOUND

**Description**: Architecture document with specified ID does not exist.

**Example Response**:
```json
{
  "error": "NotFound",
  "message": "Architecture document not found",
  "code": "ARCHITECTURE_NOT_FOUND",
  "details": {
    "id": "nonexistent-arch"
  }
}
```

**Client-Side Handling**: Same as ERR-005, replace entity type.

---

## Server Errors (5xx)

### 500 Internal Server Error

#### ERR-013: INTERNAL_ERROR

**Description**: Unexpected server error occurred.

**Example Response**:
```json
{
  "error": "InternalServerError",
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR",
  "details": {
    "request_id": "abc-123-def-456"
  }
}
```

**Common Causes**:
- Unhandled exception in server code
- Database connection failure
- File system read error
- Markdown parsing failure

**Client-Side Handling**:
```typescript
if (error.code === 'INTERNAL_ERROR') {
  // Show retry button with exponential backoff
  showErrorBoundary({
    title: 'Something went wrong',
    message: 'Please try again in a moment',
    requestId: error.details.request_id,
    retryHandler: () => retryRequest(),
  });
}
```

**Recovery**: Retry request after delay, escalate if persistent.

---

#### ERR-014: FILE_READ_ERROR

**Description**: Failed to read entity file from disk.

**Example Response**:
```json
{
  "error": "InternalServerError",
  "message": "Failed to read file",
  "code": "FILE_READ_ERROR",
  "details": {
    "path": ".claude/skills/Discovery_JTBD/SKILL.md",
    "reason": "ENOENT: no such file or directory"
  }
}
```

**Client-Side Handling**:
```typescript
if (error.code === 'FILE_READ_ERROR') {
  // File may have been deleted, refresh list
  refetchEntityList();
  showToast('File not found, refreshing list...', 'warning');
}
```

**Recovery**: Refresh entity list, file may have been deleted or moved.

---

#### ERR-015: MARKDOWN_PARSE_ERROR

**Description**: Failed to parse markdown content or frontmatter.

**Example Response**:
```json
{
  "error": "InternalServerError",
  "message": "Failed to parse markdown file",
  "code": "MARKDOWN_PARSE_ERROR",
  "details": {
    "path": ".claude/skills/BrokenSkill/SKILL.md",
    "line": 5,
    "reason": "Invalid YAML frontmatter"
  }
}
```

**Client-Side Handling**:
```typescript
if (error.code === 'MARKDOWN_PARSE_ERROR') {
  // Show file path so user can fix manually
  showToast(
    `Markdown error in ${error.details.path} at line ${error.details.line}`,
    'error'
  );
}
```

**Recovery**: Fix markdown file manually, retry.

---

## Client-Side Error Handling Pattern

### Error Interceptor

```typescript
import axios, { AxiosError } from 'axios';
import { ErrorResponse } from './api-types';

const apiClient = axios.create({
  baseURL: 'http://localhost:3001/api/v1',
  timeout: 10000,
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ErrorResponse>) => {
    const errorData = error.response?.data;

    switch (errorData?.code) {
      case 'INVALID_PARAMS':
      case 'INVALID_STAGE':
      case 'INVALID_TYPE':
        // Client validation error - show toast
        showToast(errorData.message, 'error');
        break;

      case 'SKILL_NOT_FOUND':
      case 'COMMAND_NOT_FOUND':
      case 'AGENT_NOT_FOUND':
        // Entity not found - navigate to 404
        navigate('/404', { state: { error: errorData } });
        break;

      case 'INTERNAL_ERROR':
      case 'FILE_READ_ERROR':
      case 'MARKDOWN_PARSE_ERROR':
        // Server error - show error boundary with retry
        showErrorBoundary({
          title: 'Server Error',
          message: errorData.message,
          details: errorData.details,
          retryHandler: () => retryRequest(error.config),
        });
        break;

      default:
        // Unknown error - generic handling
        showToast('An unexpected error occurred', 'error');
    }

    return Promise.reject(error);
  }
);
```

---

### Error Boundary Component

```typescript
import { Component, ReactNode } from 'react';
import { ErrorResponse } from './api-types';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: ErrorResponse;
}

class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h1>Something went wrong</h1>
          <p>{this.state.error?.message || 'Please refresh the page'}</p>
          {this.state.error?.details?.request_id && (
            <p>Request ID: {this.state.error.details.request_id}</p>
          )}
          <button onClick={() => window.location.reload()}>
            Refresh Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

---

## Testing Error Scenarios

### Mock Error Responses (MSW)

```typescript
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  // Simulate SKILL_NOT_FOUND
  rest.get('/api/v1/skills/:id', (req, res, ctx) => {
    if (req.params.id === 'nonexistent') {
      return res(
        ctx.status(404),
        ctx.json({
          error: 'NotFound',
          message: 'Skill not found',
          code: 'SKILL_NOT_FOUND',
          details: { id: 'nonexistent' },
        })
      );
    }
  }),

  // Simulate INTERNAL_ERROR
  rest.get('/api/v1/skills', (req, res, ctx) => {
    if (req.url.searchParams.get('trigger_error') === 'true') {
      return res(
        ctx.status(500),
        ctx.json({
          error: 'InternalServerError',
          message: 'An unexpected error occurred',
          code: 'INTERNAL_ERROR',
          details: { request_id: 'test-123' },
        })
      );
    }
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

---

## Error Monitoring

### Recommended Error Tracking

**Sentry Integration**:
```typescript
import * as Sentry from '@sentry/react';

Sentry.init({
  dsn: 'YOUR_SENTRY_DSN',
  integrations: [new Sentry.BrowserTracing()],
  tracesSampleRate: 1.0,
});

// Capture API errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    Sentry.captureException(error, {
      tags: {
        endpoint: error.config?.url,
        method: error.config?.method,
        status: error.response?.status,
      },
    });
    return Promise.reject(error);
  }
);
```

---

## Error Code Summary

| Code | HTTP Status | Severity | User Action |
|------|-------------|----------|-------------|
| INVALID_PARAMS | 400 | Low | Fix parameters, retry |
| INVALID_STAGE | 400 | Low | Select valid stage |
| INVALID_TYPE | 400 | Low | Clear filters |
| MISSING_QUERY | 400 | Low | Enter search query |
| SKILL_NOT_FOUND | 404 | Medium | Navigate back |
| COMMAND_NOT_FOUND | 404 | Medium | Navigate back |
| AGENT_NOT_FOUND | 404 | Medium | Navigate back |
| RULE_NOT_FOUND | 404 | Medium | Navigate back |
| HOOK_NOT_FOUND | 404 | Medium | Navigate back |
| WORKFLOW_NOT_FOUND | 404 | Medium | Navigate back |
| WAYSOFWORKING_NOT_FOUND | 404 | Medium | Navigate back |
| ARCHITECTURE_NOT_FOUND | 404 | Medium | Navigate back |
| INTERNAL_ERROR | 500 | High | Retry, escalate |
| FILE_READ_ERROR | 500 | High | Refresh list |
| MARKDOWN_PARSE_ERROR | 500 | High | Fix file manually |

---

**Total Error Codes**: 15
**Client Errors (4xx)**: 4
**Server Errors (5xx)**: 3
**Entity Not Found (404)**: 8
**Created**: 2026-01-31 by prototype-api-contract-specifier
**Session**: session-api-contracts-claudemanual
**Checkpoint**: CP-4
