# {ComponentName}

> {One-line description of the component's purpose}

## Overview

{2-3 sentences explaining what this component does, when to use it, and its primary responsibility}

## Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `{propName}` | `{type}` | {Yes/No} | `{default}` | {Description} |

## Usage

```tsx
import { {ComponentName} } from './{ComponentName}'

function Example() {
  return (
    <{ComponentName}
      {propName}={value}
    />
  )
}
```

## Examples

### Basic Usage

```tsx
<{ComponentName} {requiredProp}="value" />
```

### With All Options

```tsx
<{ComponentName}
  {requiredProp}="value"
  {optionalProp}={optionalValue}
  on{Event}={() => console.log('event')}
/>
```

## Accessibility

- **Role**: `{role}` - {why this role}
- **Keyboard**: {keyboard interactions supported}
- **ARIA**: {aria attributes used and their purpose}

## States

| State | Appearance | Triggered By |
|-------|------------|--------------|
| Default | {description} | Initial render |
| Loading | {description} | `isLoading={true}` |
| Error | {description} | `error` prop provided |
| Disabled | {description} | `disabled={true}` |

## Styling

This component uses inline CSS-in-JS styles. Key classes:
- `.{component-name}` - Main container
- `.{component-name}-header` - Header section
- `.{component-name}-content` - Content area

## Related

- [{RelatedComponent}](./{RelatedComponent}.tsx) - {why related}
- [{useRelatedHook}](../hooks/{useRelatedHook}.ts) - {why related}

---
*Traceability: {MOD-ID} / {T-ID}*
*Last updated: {YYYY-MM-DD}*
