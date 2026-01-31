---
paths:
  - "**/*_readme.md"
  - ".claude/agents/**/*"
  - ".claude/skills/**/*"
  - ".claude/commands/**/*"
  - "Implementation_*/**/src/**/*.{ts,tsx,js,jsx}"
---

# Inline Documentation Standards

**Auto-loaded when working with**: _readme.md files, agent/skill definitions, implementation code

---

## File Naming Convention

```
PATTERN: {unit_name}_readme.md

Where:
  {unit_name} = source filename without extension, preserving case

Examples:
  KPICard.tsx      → KPICard_readme.md
  useDashboard.ts  → useDashboard_readme.md
  apiClient.ts     → apiClient_readme.md
  formatters.ts    → formatters_readme.md
```

---

## File Placement

Documentation MUST be placed in the same directory as the source file:

```
CORRECT:
src/components/
├── KPICard.tsx
└── KPICard_readme.md       ✓ Same folder

INCORRECT:
src/components/
├── KPICard.tsx
docs/
└── KPICard_readme.md       ✗ Different folder
```

---

## Required Sections by Type

### Components (*.tsx)

```markdown
# {ComponentName}
> {One-line description}

## Overview
## Props
## Usage
## Examples
## Accessibility (if interactive)
## Related

---
*Traceability: {MOD-ID} / {T-ID}*
```

### Hooks (use*.ts)

```markdown
# {useHookName}
> {One-line description}

## Overview
## Returns
## Usage
## Parameters (if any)
## Examples
## State Management

---
*Traceability: {MOD-ID} / {T-ID}*
```

### Services/Utilities

```markdown
# {ServiceName}
> {One-line description}

## Overview
## API (function signatures)
## Error Handling

---
*Traceability: {MOD-ID} / {T-ID}*
```

---

## Traceability Requirement

All inline documentation MUST include traceability reference at the bottom:

```markdown
---
*Traceability: MOD-DSK-DASH-01 / T-010*
```

This is extracted from the source file's header comments:
```typescript
// MOD-DSK-DASH-01: Operations Dashboard
// T-010: KPICard component
```

---

## When to Create Documentation

| Scenario | Action |
|----------|--------|
| New component/hook created | Create `_readme.md` |
| Significant refactor | Update existing `_readme.md` |
| API/props change | Update props/parameters table |
| New use case discovered | Add example to existing doc |
| Bug fix | No documentation change needed |
| Minor style change | No documentation change needed |

---

## When NOT to Create Documentation

Do NOT create `_readme.md` for:

- **Index files** (`index.ts`) - Just re-exports
- **Type-only files** (`types.ts`, `*.d.ts`) - Types are self-documenting
- **Test files** (`*.test.ts`, `*.spec.ts`) - Tests document themselves
- **Config files** - Usually have their own conventions
- **Files under 10 lines** - Too simple to warrant docs

---

## Quality Gate

Before PR merge, check:

1. All new components have `_readme.md`
2. All new hooks have `_readme.md`
3. Modified public APIs have updated documentation
4. Traceability IDs are present

---

## Migration Guide

For existing codebases without inline documentation:

1. Run `/document src/ --depth brief` for initial coverage
2. Prioritize public/reusable components
3. Skip internal/private utilities
4. Update depth as components mature

---

## Good Examples

```
src/desktop/components/
├── KPICard.tsx
├── KPICard_readme.md          ✓ Matches component
├── AlertFeed.tsx
├── AlertFeed_readme.md        ✓ Matches component
└── index.ts                   (no readme needed)

src/mobile/hooks/
├── useAuth.ts
├── useAuth_readme.md          ✓ Matches hook
├── useTasks.ts
└── useTasks_readme.md         ✓ Matches hook
```

---

## Bad Examples

```
# WRONG: Documentation in separate folder
docs/components/
└── KPICard.md                 ✗ Not with code

# WRONG: Generic README instead of specific
src/components/
├── README.md                  ✗ Should be per-component
├── KPICard.tsx
└── AlertFeed.tsx

# WRONG: Wrong naming pattern
src/hooks/
├── useAuth.ts
└── useAuth.readme.md          ✗ Should be useAuth_readme.md
```

---

## Related

- **Skill**: `.claude/skills/Unit_Documentation/SKILL.md`
- **Command**: `.claude/commands/document.md`
- **Tech Writer**: `.claude/skills/sdd-tech-writer/SKILL.md`
