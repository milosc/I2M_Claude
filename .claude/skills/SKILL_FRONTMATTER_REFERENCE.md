# Skill Frontmatter Reference

This document provides comprehensive documentation for all YAML frontmatter fields supported in skill SKILL.md files.

---

## Overview

Every skill must have a SKILL.md file with YAML frontmatter at the top. The frontmatter defines metadata that Claude uses to discover, load, and execute skills.

```yaml
---
name: skill-name
description: Use when [trigger conditions] - [what it does]
context: fork  # Optional
agent: Explore  # Optional
---

# Skill content starts here...
```

---

## Required Fields

### `name`

**Type:** String
**Required:** Yes
**Max Length:** Part of 1024 character total limit

The unique identifier for the skill.

**Rules:**
- Use only letters, numbers, and hyphens
- No spaces, underscores, or special characters
- No parentheses or brackets
- Case-sensitive
- Must be unique within the skills directory

**Examples:**
```yaml
# Good
name: systematic-debugging
name: root-cause-tracing
name: test-driven-development

# Bad
name: systematic_debugging  # underscores not allowed
name: Systematic Debugging  # spaces not allowed
name: tdd(v2)               # parentheses not allowed
```

---

### `description`

**Type:** String
**Required:** Yes
**Recommended Length:** Under 500 characters
**Max Length:** Part of 1024 character total limit

Describes when to use the skill and what it does. This is the primary field Claude uses to decide whether to load a skill for a given task.

**Rules:**
- Start with "Use when..." to focus on triggering conditions
- Write in third person
- Include specific symptoms, situations, and contexts
- Include error messages or keywords that would trigger usage
- Describe both WHAT it does AND WHEN to use it

**Examples:**
```yaml
# Good
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently - replaces arbitrary timeouts with condition polling for reliable async tests

description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes - four-phase framework ensuring understanding before attempting solutions

# Bad
description: For async testing  # Too vague, no triggers
description: I can help you with testing  # First person
description: A testing utility  # No when-to-use information
```

---

## Optional Fields

### `context`

**Type:** String
**Required:** No
**Default:** (inline execution)
**Valid Values:** `fork`

Controls the execution context for the skill.

**Values:**

| Value | Description |
|-------|-------------|
| _(omitted)_ | Default inline execution in current conversation |
| `fork` | Runs in a forked sub-agent with isolated state |

**When to use `context: fork`:**
- Skill requires isolated state that shouldn't affect main conversation
- Long-running operations that shouldn't block the main flow
- Operations that might fail and need clean rollback
- Parallel execution of multiple skill instances
- Exploratory operations where memory efficiency matters

**Fork behavior:**
- Creates a new sub-agent with forked conversation state
- Changes in forked context don't affect parent context
- Results are returned to parent when skill completes
- More memory-efficient for exploratory operations

**Example:**
```yaml
---
name: isolated-code-review
description: Use when performing comprehensive code review requiring isolated analysis
context: fork
---
```

---

### `agent`

**Type:** String
**Required:** No
**Default:** (default agent handling)

Specifies which agent type should execute the skill.

**Available agent types:**

| Agent Type | Best For | Tools Available |
|------------|----------|-----------------|
| `general-purpose` | Complex multi-step tasks, research, code changes | All tools |
| `Explore` | Fast codebase exploration, file search, pattern finding | Glob, Grep, Read, WebFetch, WebSearch |
| `Plan` | Implementation planning, architecture design | All tools |
| `Bash` | Command execution, git operations, terminal tasks | Bash |

**When to specify agent type:**
- Skill has specific tool requirements
- Performance optimization (e.g., `Explore` for search-heavy skills)
- Skill workflow matches a specialized agent's strengths

**Example:**
```yaml
---
name: codebase-explorer
description: Use when exploring codebase structure, finding files, or searching code patterns
context: fork
agent: Explore
---
```

---

## Combined Usage Examples

### Minimal (Required fields only)

```yaml
---
name: simple-formatter
description: Use when formatting code files - applies consistent style rules
---
```

### With fork context

```yaml
---
name: parallel-analyzer
description: Use when analyzing multiple modules independently - performs isolated analysis per module
context: fork
---
```

### With agent specification

```yaml
---
name: git-operations
description: Use when performing git operations like commits, branches, or rebases
agent: Bash
---
```

### Full specification

```yaml
---
name: comprehensive-code-review
description: Use when performing multi-file code review requiring isolated analysis - systematically reviews code quality, security, and patterns
context: fork
agent: general-purpose
---
```

---

## Frontmatter Limits

| Constraint | Limit |
|------------|-------|
| Total frontmatter size | 1024 characters |
| Description recommended | Under 500 characters |
| Name characters | Letters, numbers, hyphens only |

---

## Hot-Reload Behavior

Skills support automatic hot-reload:

- **Personal skills** (`~/.claude/skills`): Immediately available after creation/modification
- **Project skills** (`.claude/skills`): Immediately available after creation/modification
- **No restart required**: Changes take effect instantly
- **Enables rapid iteration**: Test skill changes without restarting session

---

## Validation

Claude validates frontmatter when loading skills. Invalid frontmatter may cause:
- Skill not being discovered
- Skill failing to load
- Unexpected execution behavior

**Common validation issues:**
- Missing required fields (`name`, `description`)
- Invalid characters in `name`
- Total frontmatter exceeding 1024 characters
- Invalid `context` value (only `fork` is supported)
- Typos in field names

---

## Related Documentation

- **Skill Creation Guide**: `.claude/commands/create-skill.md`
- **Skill Invocation Framework**: `.claude/skills/SKILL_INVOCATION.md`
- **CLAUDE.md Skills Section**: `CLAUDE.md` (Skills Framework section)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-08 | Initial release with `name`, `description`, `context`, `agent` fields |
