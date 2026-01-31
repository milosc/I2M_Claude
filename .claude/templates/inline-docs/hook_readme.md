# {useHookName}

> {One-line description of the hook's purpose}

## Overview

{2-3 sentences explaining what this hook does, what problem it solves, and its primary responsibility}

## Returns

```typescript
interface {UseHookNameReturn} {
  // Data
  {data}: {DataType} | null

  // State
  isLoading: boolean
  error: string | null

  // Actions
  {actionName}: ({params}) => Promise<{ReturnType}>
}
```

| Property | Type | Description |
|----------|------|-------------|
| `{data}` | `{DataType} \| null` | {Description of the data} |
| `isLoading` | `boolean` | True while fetching data |
| `error` | `string \| null` | Error message if request failed |
| `{actionName}` | `({params}) => Promise<{ReturnType}>` | {Action description} |

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `{paramName}` | `{type}` | {Yes/No} | `{default}` | {Description} |

## Usage

```typescript
import { {useHookName} } from './{useHookName}'

function MyComponent() {
  const { {data}, isLoading, error, {action} } = {useHookName}()

  if (isLoading) return <Loading />
  if (error) return <Error message={error} />

  return <Display data={{data}} />
}
```

## Examples

### Basic Usage

```typescript
function BasicExample() {
  const { {data} } = {useHookName}()
  return <div>{{data}?.{property}}</div>
}
```

### With Error Handling

```typescript
function WithErrorHandling() {
  const { {data}, error, retry } = {useHookName}()

  if (error) {
    return (
      <div>
        <p>Error: {error}</p>
        <button onClick={retry}>Retry</button>
      </div>
    )
  }

  return <Display data={{data}} />
}
```

### With Actions

```typescript
function WithActions() {
  const { {data}, {action} } = {useHookName}()

  const handleAction = async () => {
    const result = await {action}({params})
    console.log('Result:', result)
  }

  return (
    <div>
      <Display data={{data}} />
      <button onClick={handleAction}>Perform Action</button>
    </div>
  )
}
```

## State Management

### Internal State

| State | Initial | Updated By |
|-------|---------|------------|
| `{data}` | `null` | API response |
| `isLoading` | `false` | Fetch start/end |
| `error` | `null` | API error |

### State Flow

```
Initial Load:
  isLoading: false → true → false
  data: null → {data}
  error: null

On Error:
  isLoading: true → false
  data: unchanged
  error: null → "error message"

On Retry:
  error: "message" → null
  isLoading: false → true → false
```

## Side Effects

- **Auto-fetch on mount**: {Yes/No} - {description}
- **Polling interval**: {interval or "None"}
- **Cleanup on unmount**: {what gets cleaned up}

## Dependencies

| Dependency | Purpose |
|------------|---------|
| `apiClient` | HTTP requests to backend |
| `{otherHook}` | {purpose} |

## API Calls

| Endpoint | Method | When Called |
|----------|--------|-------------|
| `{endpoint}` | `{method}` | {trigger} |

## Error Handling

| Error Type | Handling |
|------------|----------|
| Network error | Sets `error` state, allows retry |
| 401 Unauthorized | {behavior} |
| 404 Not Found | {behavior} |
| 500 Server Error | {behavior} |

## Testing

```typescript
// Mock the hook for component tests
vi.mock('./{useHookName}', () => ({
  {useHookName}: () => ({
    {data}: mockData,
    isLoading: false,
    error: null,
    {action}: vi.fn(),
  })
}))
```

## Related

- [{useRelatedHook}](./{useRelatedHook}.ts) - {why related}
- [{RelatedComponent}](../components/{RelatedComponent}.tsx) - Uses this hook
- [{apiClient}](../api/client.ts) - API layer

---
*Traceability: {MOD-ID} / {T-ID}*
*Last updated: {YYYY-MM-DD}*
