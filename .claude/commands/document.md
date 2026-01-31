---
description: Create inline documentation for code units (components, hooks, services) as <unit_name>_readme.md files placed alongside the code
argument-hint: <file-or-folder-path> [--depth brief|standard|comprehensive] [--type component|hook|service|utility|module] [--force]
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /document started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /document ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /document instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## User Arguments

```text
$ARGUMENTS
```

Parse arguments:
- `TARGET`: First argument - file path or folder path to document
- `--depth`: Documentation depth (brief, standard, comprehensive) - default: standard
- `--type`: Force type detection (component, hook, service, utility, module)
- `--force`: Overwrite existing _readme.md files

## Execution

## Why Inline Documentation?

Documentation placed next to code is:
- **Discoverable**: Found when browsing code
- **Maintainable**: Updated when code changes
- **Accurate**: Easy to verify against source
- **Contextual**: Understood in its environment

## Workflow

### 1. Parse Target

```
IF no TARGET provided:
  ERROR: "Usage: /document <path> [--depth brief|standard|comprehensive]"
  EXIT

IF TARGET is a file:
  MODE = "single"
  FILES = [TARGET]
ELSE IF TARGET is a folder:
  MODE = "folder"
  FILES = find all .ts, .tsx, .js, .jsx files in TARGET
ELSE:
  ERROR: "Target not found: {TARGET}"
  EXIT
```

### 2. Filter Files

For folder mode, exclude:
- Files already having `_readme.md` (unless --force)
- Test files (`*.test.ts`, `*.spec.ts`)
- Index files (`index.ts`)
- Type definition only files (`*.d.ts`)
- Files under 10 lines (likely re-exports)

### 3. Analyze Each File

For each file in FILES:

1. **Read source code**
2. **Extract metadata**:
   - Traceability headers (MOD-*, T-*)
   - JSDoc comments
   - Exported members
   - Props/parameters/return types
   - Dependencies

3. **Detect type** (if not forced):
   | Pattern | Type |
   |---------|------|
   | `use*.ts` | hook |
   | `*.tsx` with JSX return | component |
   | `*Service.ts`, `*Client.ts` | service |
   | `*Utils.ts`, `formatters.ts` | utility |
   | Folder with index.ts | module |

4. **Determine depth**:
   - `brief`: Overview + basic usage
   - `standard`: Full template (default)
   - `comprehensive`: All sections + extras

### 4. Generate Documentation

Use the **Unit_Documentation** skill templates:

#### For Components

```markdown
# {ComponentName}

> {description from JSDoc or inferred}

## Overview

{What it does, when to use it}

## Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|

## Usage

\`\`\`tsx
import { {ComponentName} } from './{ComponentName}'

<{ComponentName} prop={value} />
\`\`\`

## Examples

{2-3 examples based on depth}

## Accessibility

{ARIA, keyboard, screen reader notes}

## Related

{Links to related components/hooks}

---
*Traceability: {MOD-ID} / {T-ID}*
```

#### For Hooks

```markdown
# {useHookName}

> {description}

## Overview

{Purpose and when to use}

## Returns

| Property | Type | Description |
|----------|------|-------------|

## Usage

\`\`\`typescript
const { data, isLoading } = {useHookName}()
\`\`\`

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|

## Examples

{Examples based on depth}

## State Management

{Internal state description}

---
*Traceability: {MOD-ID} / {T-ID}*
```

#### For Services/Utilities

```markdown
# {ServiceName}

> {description}

## Overview

{Purpose}

## API

### {functionName}

\`\`\`typescript
{signature}
\`\`\`

{Description, parameters, returns, example}

## Error Handling

{How errors work}

---
*Traceability: {MOD-ID} / {T-ID}*
```

### 5. Write Files

For each generated doc:

1. **Build path**: `{file_directory}/{file_name_without_ext}_readme.md`
2. **Check exists**:
   - If exists and not --force: Skip, log "Skipped: already exists"
   - If exists and --force: Backup to `{name}_readme.md.bak`, overwrite
3. **Write file**
4. **Log**: "Created: {path}"

### 6. Summary

Output summary:

```
Documentation Complete
======================
Target: {TARGET}
Mode: {single|folder}
Depth: {depth}

Created ({count}):
  - src/components/KPICard_readme.md
  - src/components/AlertFeed_readme.md

Skipped ({count}):
  - src/components/Button_readme.md (already exists)

Errors ({count}):
  - None
```

## Examples

### Document Single Component

```
/document src/desktop/components/KPICard.tsx
```

Output: `src/desktop/components/KPICard_readme.md`

### Document All Hooks

```
/document src/mobile/hooks/
```

Output:
- `src/mobile/hooks/useAuth_readme.md`
- `src/mobile/hooks/useTasks_readme.md`
- `src/mobile/hooks/usePerformance_readme.md`

### Brief Documentation

```
/document src/shared/utils/formatters.ts --depth brief
```

Output: Minimal `formatters_readme.md` with overview and basic usage only.

### Comprehensive Documentation

```
/document src/shared/api/client.ts --depth comprehensive
```

Output: Full `client_readme.md` with all sections, extended examples, troubleshooting.

### Force Regenerate

```
/document src/desktop/components/ --force
```

Regenerates all component docs, backing up existing ones.

## Quality Checklist

After documentation is created, verify:

- [ ] Markdown renders correctly
- [ ] Code examples have correct syntax
- [ ] Props/parameters table is complete
- [ ] Usage example actually works
- [ ] Traceability IDs are present
- [ ] Related links point to existing files



## Integration

This command uses the **Unit_Documentation** skill from:
`.claude/skills/Unit_Documentation/SKILL.md`

And follows the **inline-docs** rule from:
`.claude/rules/inline-docs.md`
