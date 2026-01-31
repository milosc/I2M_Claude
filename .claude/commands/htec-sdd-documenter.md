---
description: Generate comprehensive documentation for implemented features using the implementation-documenter agent
argument-hint: <SystemName> [--task <T-ID>] [--module <MOD-ID>] [--scope all|task|module]
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TaskOutput
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-documenter started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-documenter ended '{"stage": "implementation"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "implementation"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /htec-sdd-documenter instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

---

## 🎯 Guiding Architectural Principle

**Optimize for maintainability, not simplicity.**

When making documentation decisions:

1. **Prioritize long-term clarity** - Documentation should help future developers understand code intent
2. **Maintain traceability** - Link all documentation to pain points, requirements, and tasks
3. **Follow conventions** - Use `_readme.md` pattern for inline module documentation
4. **Generate diagrams** - Visual documentation aids comprehension

---

## Usage

```bash
/htec-sdd-documenter <SystemName>
/htec-sdd-documenter <SystemName> --task T-015
/htec-sdd-documenter <SystemName> --module MOD-AUTH-01
/htec-sdd-documenter <SystemName> --scope all
```

## Arguments

- `SystemName`: Name of the system (e.g., ERTriage, InventorySystem)

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--task <T-ID>` | Document specific task only | All tasks |
| `--module <MOD-ID>` | Document specific module only | All modules |
| `--scope <all\|task\|module\|changed>` | Documentation scope | all |
| `--api-only` | Generate only API documentation | false |
| `--diagrams-only` | Generate only Mermaid diagrams | false |

---

## Overview

This command invokes the `implementation-documenter` agent to generate comprehensive documentation for implemented features:

1. **Inline Documentation** - JSDoc/TSDoc comments in source files
2. **Module READMEs** - `_readme.md` files following inline documentation convention
3. **API Documentation** - Endpoint documentation with examples
4. **Mermaid Diagrams** - Architecture and sequence diagrams
5. **Usage Examples** - Practical code examples

---

## Execution Procedure

### Phase 1: Validate Prerequisites

```bash
# Check implementation folder exists
ls Implementation_<SystemName>/

# Check that implementation has completed tasks
python3 .claude/hooks/implementation_quality_gates.py \
  --validate-checkpoint 5 \
  --dir Implementation_<SystemName>/
```

**Prerequisites:**
- Implementation checkpoint 5+ (P0 tasks complete)
- Source files exist in `Implementation_<SystemName>/src/`
- Test files exist in `Implementation_<SystemName>/tests/`

### Phase 2: Determine Scope

```
IF --task == specified:
    FILES = get_files_for_task(--task)
ELIF --module == specified:
    FILES = get_files_for_module(--module)
ELIF --scope == "changed":
    FILES = git diff --name-only (since last documentation run)
ELSE:
    FILES = glob("Implementation_<System>/src/**/*")
```

### Phase 3: Create Documentation Directory

```bash
mkdir -p Implementation_<SystemName>/05-documentation
mkdir -p Implementation_<SystemName>/05-documentation/api
mkdir -p Implementation_<SystemName>/05-documentation/diagrams
```

### Phase 4: Invoke Documentation Agent

Launch the `implementation-documenter` agent:

```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate documentation for <SystemName>",
  prompt: `
Agent: implementation-documenter
Read: .claude/agents/implementation-documenter.md

SESSION: ${session_id}
SYSTEM: ${SystemName}
SCOPE: ${scope}
${task_id ? `TASK: ${task_id}` : ''}
${module_id ? `MODULE: ${module_id}` : ''}

TARGET FILES:
- Implementation_${SystemName}/src/**/*
- Implementation_${SystemName}/tests/**/*

OUTPUTS (05-documentation/):
- api/<module>.md - API documentation
- diagrams/<module>-architecture.mmd - Mermaid diagrams
- _readme.md - Documentation index

INLINE OUTPUTS (src/):
- src/features/<feature>/_readme.md - Module READMEs
- src/**/*.ts - JSDoc/TSDoc comments (via Edit)

RETURN JSON:
{
  "status": "completed|failed",
  "documentation_files": ["path/to/file.md"],
  "inline_docs_updated": ["path/to/source.ts"],
  "diagrams_generated": N,
  "examples_count": N,
  "issues": []
}
`
})
```

### Phase 5: Validate Output

After agent completes, verify outputs:

```bash
# Check documentation folder has content
ls -la Implementation_<SystemName>/05-documentation/

# Validate documentation index exists
test -f Implementation_<SystemName>/05-documentation/_readme.md

# Check API docs were generated
ls Implementation_<SystemName>/05-documentation/api/
```

### Phase 6: Log Version History

```bash
# Log documentation index
python3 .claude/hooks/version_history_logger.py \
  "traceability/" "<SystemName>" "implementation" "Claude" "3.0.0" \
  "Generated documentation index from /htec-sdd-documenter" \
  "DOC-XXX" \
  "Implementation_<SystemName>/05-documentation/_readme.md" \
  "creation"

# Log each API doc
FOR EACH api_doc IN Implementation_<SystemName>/05-documentation/api/*.md:
    python3 .claude/hooks/version_history_logger.py \
      "traceability/" "<SystemName>" "implementation" "Claude" "3.0.0" \
      "Generated API documentation" \
      "DOC-XXX,MOD-XXX" \
      "${api_doc}" \
      "creation"
```

### Phase 7: Display Summary

```
Documentation Generation: COMPLETED
═══════════════════════════════════════

System: <SystemName>
Scope: <all|task|module>
Time: Xm Ys

Generated:
  📄 API Docs: N files
  📊 Diagrams: N files
  📝 Module READMEs: N files
  💬 Inline Docs: N files updated

Output Location:
  Implementation_<SystemName>/05-documentation/
  ├── _readme.md (index)
  ├── api/
  │   └── *.md
  └── diagrams/
      └── *.mmd

Next: Run /htec-sdd-review to verify documentation quality
```

---

## Output Structure

```
Implementation_<SystemName>/05-documentation/
├── _readme.md                    # Documentation index
├── api/
│   ├── auth.md                   # Auth module API docs
│   ├── inventory.md              # Inventory module API docs
│   └── reports.md                # Reports module API docs
├── diagrams/
│   ├── auth-architecture.mmd     # Auth module architecture
│   ├── auth-sequence.mmd         # Auth flow sequence
│   └── system-overview.mmd       # System-level diagram
└── guides/
    └── GETTING_STARTED.md        # Quick start guide
```

### Inline Documentation (in src/)

```
Implementation_<SystemName>/src/
├── features/
│   ├── auth/
│   │   ├── _readme.md            # Module README
│   │   └── services/
│   │       └── auth-service.ts   # JSDoc comments added
│   └── inventory/
│       ├── _readme.md            # Module README
│       └── ...
```

---

## Documentation Standards

### Module README Pattern (`_readme.md`)

Each feature module gets a `_readme.md` file with:

- **Overview** - What the module does
- **Architecture** - Mermaid diagram
- **Public API** - Methods, parameters, return types
- **Usage Examples** - Code snippets
- **Configuration** - Environment variables
- **Testing** - Test coverage and commands
- **Dependencies** - Internal and external
- **Traceability** - Links to pain points, requirements, tasks
- **Maintenance Notes** - Known limitations, future enhancements

### JSDoc/TSDoc Pattern

```typescript
/**
 * Brief description
 *
 * @module MOD-AUTH-01
 * @task T-015
 * @requirements REQ-001, REQ-002
 * @pain-points PP-1.1, PP-1.2
 * @adr ADR-007
 *
 * @example
 * ```typescript
 * const result = service.method(param);
 * ```
 */
```

---

## Quality Checklist

The agent validates:

- ✅ All public APIs have JSDoc/TSDoc
- ✅ All modules have `_readme.md`
- ✅ Traceability IDs are present
- ✅ Usage examples are runnable
- ✅ Architecture diagrams are valid Mermaid
- ✅ Configuration is documented
- ✅ Error handling is documented

---

## Registry Updates

The command automatically updates:

1. **`_state/implementation_progress.json`**
   - Records documentation generation timestamp
   - Updates Phase 7 (Documentation) status

2. **`traceability/<SystemName>_version_history.json`**
   - Logs creation of all documentation files

---

## Example Complete Workflow

```bash
# User runs:
/htec-sdd-documenter ERTriage

# Claude executes:

# Phase 1: Validate
ls Implementation_ERTriage/
python3 .claude/hooks/implementation_quality_gates.py --validate-checkpoint 5 --dir Implementation_ERTriage/

# Phase 2: Determine scope
SCOPE="all"

# Phase 3: Create directories
mkdir -p Implementation_ERTriage/05-documentation/api
mkdir -p Implementation_ERTriage/05-documentation/diagrams

# Phase 4: Invoke agent
Task({ subagent_type: "general-purpose", ... })

# Phase 5: Validate output
ls Implementation_ERTriage/05-documentation/

# Phase 6: Log version history
python3 .claude/hooks/version_history_logger.py ...

# Phase 7: Display summary
Documentation Generation: COMPLETED
═══════════════════════════════════════
...
```

---

## Related Commands

- `/htec-sdd-implement` - Implement tasks before documentation
- `/htec-sdd-review` - Review code and documentation quality
- `/htec-sdd-finalize` - Complete implementation with all documentation
- `/htec-sdd-status` - Check documentation progress

---

## Troubleshooting

### No Source Files Found

```
Error: No source files in Implementation_<SystemName>/src/
```

**Solution**: Run `/htec-sdd-implement` first to generate source code.

### Missing Prerequisites

```
Error: Checkpoint 5 not reached
```

**Solution**: Complete P0 implementation tasks before generating documentation.

### Documentation Agent Timeout

If the agent takes too long:

```bash
# Run for specific module instead of full system
/htec-sdd-documenter ERTriage --module MOD-AUTH-01
```
