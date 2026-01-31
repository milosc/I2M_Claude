# {ServiceName}

> {One-line description of the service's purpose}

## Overview

{2-3 sentences explaining what this service does, what problem it solves, and when to use it}

## Quick Start

```typescript
import { {serviceName} } from './{serviceName}'

// Basic usage
const result = await {serviceName}.{method}({params})
```

## API Reference

### {methodName}

```typescript
{methodName}({params}): Promise<{ReturnType}>
```

{Description of what this method does}

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `{param}` | `{type}` | {Yes/No} | {description} |

**Returns:** `Promise<{ReturnType}>` - {description of return value}

**Example:**

```typescript
const result = await {serviceName}.{methodName}({
  {param}: {value}
})

// result: {exampleResult}
```

---

### {anotherMethod}

```typescript
{anotherMethod}({params}): {ReturnType}
```

{Description}

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|

**Returns:** `{ReturnType}` - {description}

**Example:**

```typescript
const result = {serviceName}.{anotherMethod}({params})
```

---

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `{option}` | `{type}` | `{default}` | {description} |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `{VAR_NAME}` | {Yes/No} | {description} |

## Error Handling

### Error Types

```typescript
class {ServiceName}Error extends Error {
  code: string
  details?: unknown
}
```

| Error Code | Meaning | Resolution |
|------------|---------|------------|
| `{CODE}` | {meaning} | {how to resolve} |

### Error Handling Example

```typescript
try {
  const result = await {serviceName}.{method}({params})
} catch (error) {
  if (error instanceof {ServiceName}Error) {
    switch (error.code) {
      case '{CODE}':
        // Handle specific error
        break
      default:
        // Handle unknown error
    }
  }
}
```

## Retry Logic

| Scenario | Behavior |
|----------|----------|
| Network failure | {retry behavior} |
| Timeout | {timeout behavior} |
| Rate limit | {rate limit behavior} |

## Caching

| Data | Cache Duration | Invalidation |
|------|----------------|--------------|
| `{data}` | {duration} | {when invalidated} |

## Usage Patterns

### Pattern 1: {PatternName}

```typescript
// {description of when to use this pattern}
{code example}
```

### Pattern 2: {PatternName}

```typescript
// {description}
{code example}
```

## Dependencies

| Dependency | Purpose |
|------------|---------|
| `{dependency}` | {why needed} |

## Testing

### Mocking the Service

```typescript
vi.mock('./{serviceName}', () => ({
  {serviceName}: {
    {method}: vi.fn().mockResolvedValue({mockResult}),
  }
}))
```

### Integration Testing

```typescript
describe('{ServiceName}', () => {
  it('{test description}', async () => {
    const result = await {serviceName}.{method}({params})
    expect(result).toEqual({expected})
  })
})
```

## Performance Considerations

- **Batch operations**: {guidance}
- **Connection pooling**: {guidance}
- **Memory usage**: {guidance}

## Related

- [{RelatedService}](./{RelatedService}.ts) - {why related}
- [{Consumer}](../hooks/{useConsumer}.ts) - Uses this service

---
*Traceability: {MOD-ID} / {T-ID}*
*Last updated: {YYYY-MM-DD}*
