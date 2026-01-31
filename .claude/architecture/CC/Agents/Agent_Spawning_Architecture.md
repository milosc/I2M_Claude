# Agent Spawning Architecture

**Version**: 1.0.0
**Date**: 2026-01-08
**Status**: Production Ready

This document describes the multi-agent spawning architecture for the i2m framework, including the unified naming convention, invocation patterns, model optimization, and coordination mechanisms.

---

## Table of Contents

1. [Overview](#overview)
2. [Unified Agent Naming Convention](#unified-agent-naming-convention)
3. [Native Task API Integration](#native-task-api-integration)
4. [Model Allocation Strategy](#model-allocation-strategy)
5. [Token Optimization](#token-optimization)
6. [Agent Categories](#agent-categories)
7. [Coordination Infrastructure](#coordination-infrastructure)
8. [Migration from Legacy Patterns](#migration-from-legacy-patterns)
9. [Best Practices](#best-practices)

---

## Overview

The i2m framework uses Claude Code's native Task tool to spawn specialized agents for parallel and sequential task execution. The architecture was optimized for:

| Goal | Approach |
|------|----------|
| **API Compatibility** | Use native `subagent_type` values only |
| **Token Efficiency** | Compact prompts with agent file references |
| **Cost Optimization** | Model-appropriate allocation (haiku for structured tasks) |
| **Consistency** | Unified naming convention across all stages |
| **Coordination** | File locking, session tracking, process integrity |

### Key Design Decisions

1. **Native subagent_type**: All agents use `general-purpose`, `Explore`, `Plan`, or `Bash` (Claude Code native types)
2. **Agent identity via prompt**: Agent role communicated through prompt, not subagent_type
3. **Compact prompts**: Reference `.claude/agents/{agent}.md` instead of inline instructions
4. **Model optimization**: `sonnet` for complex reasoning, `haiku` for structured validation

---

## Unified Agent Naming Convention

### Pattern

```
{stage}-{role}
```

Where:
- **stage**: discovery, prototype, implementation, planning, quality, process-integrity, reflexion
- **role**: Descriptive hyphenated name (e.g., `domain-researcher`, `code-generator`)

### Examples

| Old Naming | New Naming |
|------------|------------|
| `sdd:developer` | `implementation-developer` |
| `sdd:tech-lead` | `planning-tech-lead` |
| `prototype:screen-specifier` | `prototype-screen-specifier` |
| `sdd:traceability-guardian` | `process-integrity-traceability-guardian` |
| `sdd:bug-hunter` | `quality-bug-hunter` |

### Agent Categories

| Category | Prefix | Description |
|----------|--------|-------------|
| Discovery | `discovery-` | Material analysis, persona synthesis, JTBD extraction |
| Prototype | `prototype-` | Specifications, validation, code generation |
| Implementation | `implementation-` | TDD development, test automation |
| Planning | `planning-` | Task decomposition, research, code exploration |
| Quality | `quality-` | Code review (6 specialized reviewers) |
| Process Integrity | `process-integrity-` | Traceability, TDD compliance, checkpoint auditing |
| Reflexion | `reflexion-` | Self-improvement loop (actor, evaluator, self-refiner) |

---

## Native Task API Integration

### Claude Code Task Tool API

The Task tool accepts these native `subagent_type` values:

| subagent_type | Purpose | Use Case |
|---------------|---------|----------|
| `general-purpose` | General tasks, multi-step operations | Most agent work |
| `Explore` | Fast codebase exploration | Finding files, searching code |
| `Plan` | Implementation planning | Designing approaches |
| `Bash` | Command execution | Git, npm, build commands |

### Correct Invocation Pattern

```javascript
Task({
  subagent_type: "general-purpose",  // ALWAYS native type
  model: "sonnet",                   // or "haiku"
  description: "Brief description (3-5 words)",
  prompt: `Agent: {agent-name}
    Read: .claude/agents/{agent-name}.md
    SESSION: {session_id} | TASK: {task_id}
    [compact context parameters]
    RETURN: JSON { status, files_written, issues }`
})
```

### Anti-Patterns (Do NOT Use)

```javascript
// WRONG: Custom subagent_type (not recognized by Task tool)
Task({
  subagent_type: "implementation-developer",  // NOT VALID
  ...
})

// WRONG: sdd: prefix (legacy pattern)
Task({
  subagent_type: "sdd:developer",  // DEPRECATED
  ...
})

// WRONG: prototype: prefix (legacy pattern)
Task({
  subagent_type: "prototype:screen-specifier",  // DEPRECATED
  ...
})
```

---

## Model Allocation Strategy

### Model Selection Criteria

| Model | Token Cost | Speed | Use For |
|-------|------------|-------|---------|
| `sonnet` | Medium | Medium | Complex reasoning, code generation, security analysis |
| `haiku` | Low | Fast | Structured outputs, checklists, templated validation |

### Agent-Model Mapping

#### Sonnet (Complex Tasks)

- `implementation-developer` - TDD implementation
- `planning-tech-lead` - Task decomposition
- `quality-security-auditor` - Security analysis (OWASP)
- `prototype-screen-specifier` - Screen specification generation
- `prototype-code-generator` - React code generation
- `reflexion-actor` - Solution generation
- `reflexion-evaluator` - Solution critique

#### Haiku (Structured Tasks)

- `process-integrity-traceability-guardian` - Link validation (checklist-based)
- `process-integrity-checkpoint-auditor` - Gate validation (rule-based)
- `quality-code-quality` - SOLID/DRY checks (pattern-based)
- `quality-test-coverage` - Coverage analysis (metrics-based)
- `prototype-component-validator` - Spec validation (schema-based)

### Cost Impact

Using haiku for validation agents reduces costs by ~70% for those operations while maintaining quality.

---

## Token Optimization

### Compact Prompt Format

**Before (verbose):**
```javascript
Task({
  subagent_type: "sdd:developer",
  prompt: `
    You are a Developer agent responsible for implementing features using Test-Driven Development.

    Your responsibilities:
    1. Write failing tests first (RED phase)
    2. Write minimal implementation to pass tests (GREEN phase)
    3. Refactor while keeping tests green (REFACTOR phase)

    Follow these guidelines:
    - Use TypeScript with strict mode
    - No any types
    - Explicit return types
    ...
    (200+ lines of instructions)
  `
})
```

**After (compact):**
```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Implement T-015",
  prompt: `Agent: implementation-developer
    Read: .claude/agents/implementation-developer.md
    SESSION: sess-001 | TASK: T-015
    FILES: src/services/OrderService.ts, tests/unit/OrderService.test.ts
    RETURN: JSON { tdd_phase, test_result, files_modified }`
})
```

### Token Savings

| Component | Before | After | Savings |
|-----------|--------|-------|---------|
| Agent instructions | 200+ lines | 1 line (file ref) | ~95% |
| Context parameters | Verbose | Pipe-separated | ~60% |
| Return format | Natural language | JSON schema | ~40% |
| **Total prompt** | ~2000 tokens | ~200 tokens | **~90%** |

### Best Practices

1. **Reference agent files**: `Read: .claude/agents/{agent}.md`
2. **Use pipe separators**: `SESSION: x | TASK: y | FILES: z`
3. **Structured returns**: `RETURN: JSON { field1, field2 }`
4. **Brief descriptions**: 3-5 words maximum

---

## Agent Categories

### Discovery Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `discovery-domain-researcher` | sonnet | External research, market analysis |
| `discovery-persona-synthesizer` | sonnet | Persona generation from research |
| `discovery-jtbd-extractor` | sonnet | Jobs-To-Be-Done extraction |
| `discovery-fact-auditor` | haiku | Zero hallucination validation |

### Prototype Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `prototype-data-model-specifier` | sonnet | Entity schema generation |
| `prototype-screen-specifier` | sonnet | Screen specification (parallel per screen) |
| `prototype-code-generator` | sonnet | React code generation |
| `prototype-component-validator` | haiku | Component spec validation |
| `prototype-accessibility-auditor` | sonnet | WCAG 2.1 AA compliance |

### Implementation Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `implementation-developer` | sonnet | TDD implementation (up to 3 parallel) |
| `implementation-test-automation-engineer` | sonnet | E2E test setup |

### Planning Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `planning-tech-lead` | sonnet | Task decomposition, sprint planning |
| `planning-code-explorer` | sonnet | Codebase analysis and mapping |

**Note**: `planning-product-researcher` and `planning-hfe-ux-researcher` have been **archived** (moved to `.claude/agents/archived/`). These agents were used for research during specification phases but are not needed in Implementation Phase, where all requirements come from ProductSpecs and SolArch outputs. The planning-tech-lead now includes interactive strategy selection to replace the planning research workflow. See `.claude/agents/archived/README.md` for migration details.

### Quality Agents (Code Review)

| Agent | Model | Purpose |
|-------|-------|---------|
| `quality-bug-hunter` | sonnet | Logic errors, null safety, edge cases |
| `quality-security-auditor` | sonnet | OWASP Top 10, security vulnerabilities |
| `quality-code-quality` | haiku | SOLID, DRY, complexity metrics |
| `quality-test-coverage` | haiku | Missing tests, coverage gaps |
| `quality-contracts-reviewer` | haiku | API contract compliance |
| `quality-accessibility-auditor` | sonnet | WCAG compliance |

### Process Integrity Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `process-integrity-traceability-guardian` | haiku | Trace link validation |
| `process-integrity-state-watchdog` | haiku | Lock and session health |
| `process-integrity-checkpoint-auditor` | haiku | Gate validation |
| `process-integrity-playbook-enforcer` | haiku | TDD compliance |

### Reflexion Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `reflexion-actor` | sonnet | Solution generation |
| `reflexion-evaluator` | sonnet | Solution critique |
| `reflexion-self-refiner` | sonnet | Final polish based on feedback |

---

## Coordination Infrastructure

### File Locking

**Location**: `_state/agent_lock.json`

```json
{
  "locks": [
    {
      "lock_id": "lock-abc123",
      "file_path": "src/services/OrderService.ts",
      "agent_id": "implementation-developer",
      "task_id": "T-015",
      "acquired_at": "2026-01-08T14:10:00Z",
      "expires_at": "2026-01-08T14:25:00Z"
    }
  ]
}
```

**Protocol**:
1. Request lock before writing
2. 15-minute timeout (one extension allowed)
3. Auto-release on session end
4. Lock multiple files in alphabetical order (deadlock prevention)

### Session Tracking

**Location**: `_state/agent_sessions.json`

```json
{
  "active_sessions": [
    {
      "session_id": "sess-001",
      "agent_id": "implementation-developer",
      "task_id": "T-015",
      "status": "running"
    }
  ]
}
```

### Process Integrity Monitoring

**Location**: `_state/integrity_status.json`

Monitors:
- Traceability links
- TDD compliance
- Checkpoint gates
- Session health

**Veto Power**: Process integrity agents can block phase transitions on critical violations.

### Worktree Coordination

**Version**: 3.0.0 (Worktree Support)
**Location**: `_state/agent_lock.json`, `_state/agent_sessions.json`

When working with git worktrees for parallel PR development, the framework uses worktree-aware file locking to enable true parallelism while preventing conflicts.

#### Lock Scopes

**Worktree-Scoped Locks**:
- Files in `src/`, `tests/`, `public/`
- Different worktrees can modify the "same" file independently
- Lock key format: `{worktree_path}:{file_path}`
- Example: `../worktrees/pr-001-auth:src/models/User.ts`

**Global-Scoped Locks**:
- Files in `_state/`, `traceability/`, `.claude/`
- All agents must coordinate sequentially
- Lock key format: `{file_path}`
- Example: `traceability/task_registry.json`

#### Lock Scope Determination

```javascript
function determineLockScope(filePath, worktreePath) {
  // Global-scoped files (always sequential)
  if (filePath.startsWith("_state/") ||
      filePath.startsWith("traceability/") ||
      filePath.startsWith(".claude/")) {
    return { scope: "global", lockKey: filePath };
  }

  // Worktree-scoped files (isolated per worktree)
  if (worktreePath &&
      (filePath.startsWith("src/") ||
       filePath.startsWith("tests/") ||
       filePath.startsWith("public/"))) {
    return {
      scope: "worktree",
      lockKey: `${worktreePath}:${filePath}`
    };
  }

  // Default to global for safety
  return { scope: "global", lockKey: filePath };
}
```

#### Conflict Resolution Rules

| Scenario | Result | Reason |
|----------|--------|--------|
| Same worktree, same file | **CONFLICT** | Lock keys match |
| Different worktrees, same file | **ALLOW** | Lock keys differ (isolated) |
| Any agent, global file | **SEQUENTIAL** | Single lock key (coordination point) |

#### Enhanced Lock Entry

```json
{
  "lock_key": "../worktrees/pr-001-auth:src/models/User.ts",
  "file_path": "src/models/User.ts",
  "lock_scope": "worktree",
  "worktree_path": "../worktrees/pr-001-auth",
  "pr_group": "PR-001",
  "branch": "feature/pr-001-auth",
  "agent_id": "developer-001",
  "task_id": "T-015",
  "acquired_at": "2026-01-26T10:30:00Z",
  "expires_at": "2026-01-26T10:45:00Z"
}
```

#### Session Context

```json
{
  "session_id": "sess-001",
  "agent_id": "implementation-developer",
  "task_id": "T-015",
  "pr_group": "PR-001",
  "worktree_path": "../worktrees/pr-001-auth",
  "branch": "feature/pr-001-auth",
  "lock_scope": "worktree",
  "status": "active"
}
```

#### Benefits

- **Max Parallelism**: Multiple agents can work on "same" files in different worktrees
- **Registry Safety**: Global files (registries) remain sequentially coordinated
- **Clear Isolation**: Each PR group has its own branch and worktree
- **Conflict Prevention**: Lock keys prevent false conflicts

**Full Documentation**: `.claude/architecture/workflows/Implementation Phase/Worktree_State_Schemas.md`

---

## Migration from Legacy Patterns

### What Changed

| Aspect | Before | After |
|--------|--------|-------|
| Agent naming | `sdd:developer`, `prototype:*` | `implementation-developer`, `prototype-*` |
| subagent_type | Custom values | Native: `general-purpose`, `Explore`, etc. |
| Prompt style | Verbose inline instructions | Compact with file references |
| Model selection | Default sonnet | Explicit sonnet/haiku allocation |

### Migration Checklist

1. Update all `subagent_type` values to native types
2. Replace colon (`:`) with hyphen (`-`) in agent names
3. Add `model` parameter to all Task() calls
4. Convert verbose prompts to compact format with file references
5. Update agent definition files with new naming

### Files Updated

- `.claude/agents/*.md` - All agent definitions
- `.claude/skills/**/SKILL.md` - Skills that spawn agents
- `.claude/rules/*.md` - Rules referencing agents
- `.claude/commands/*.md` - Commands referencing agents
- `architecture/Multi_Agent_Prototype_Architecture.md` - Architecture docs

---

## Best Practices

### DO

- Use native `subagent_type` values (`general-purpose`, `Explore`, `Plan`, `Bash`)
- Reference agent `.md` files instead of inline instructions
- Use compact pipe-separated parameters
- Specify `model` explicitly for cost optimization
- Use haiku for structured/validation tasks
- Include `RETURN: JSON {}` for structured outputs

### DON'T

- Use custom subagent_type values (they will fail)
- Include verbose inline instructions (wastes tokens)
- Omit model specification (defaults may not be optimal)
- Use sonnet for simple checklist tasks (wastes money)
- Forget to acquire locks before file modifications

### Parallel Execution Rules

1. **Independent tasks**: Run in parallel (multiple Task() calls in one message)
2. **Dependent tasks**: Run sequentially (chain with await)
3. **Max concurrency**: 12 agents total, 3 developers max
4. **File isolation**: Each parallel agent works on different files

---

## Related Documentation

- **CLAUDE.md**: Project overview and multi-agent section
- **Multi-Agent Prototype Architecture**: `architecture/Multi_Agent_Prototype_Architecture.md`
- **Skills Reference**: `architecture/Skills_Reference.md`
- **Agent Coordination Rules**: `.claude/rules/agent-coordination.md`
- **Process Integrity Rules**: `.claude/rules/process-integrity.md`
- **Agent Definitions**: `.claude/agents/`

---

## Summary

The agent spawning architecture enables:

- **60% faster** execution through parallel agents
- **70% cost savings** on validation tasks using haiku
- **90% token savings** through compact prompts
- **100% API compatibility** with native Claude Code Task tool
- **Full traceability** through session and lock tracking

All agents now follow the unified `{stage}-{role}` naming convention and use native `subagent_type` values, ensuring consistent behavior across the framework.
