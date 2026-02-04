---
name: create-agent
description: Create a new specialized Claude Code agent with proper HTEC conventions including hooks, lifecycle logging, and traceability. Spawns the agent-expert in a separate context to design and create production-ready agents for the multi-agent framework.
argument-hint: "<agent-description> - Describe the agent you want to create (e.g., 'React performance optimization specialist' or 'API security auditor')"
model: claude-sonnet-4-5-20250929
allowed-tools: Task, Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /create-agent started '{"stage": "utility"}'
  Stop:
    - hooks:
        # VALIDATION: Verify agents directory has at least one file (sanity check)
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory ".claude/agents"
            --requires "*.md"
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /create-agent ended '{"stage": "utility"}'
---

# /create-agent Command

Create specialized Claude Code agents with proper HTEC conventions.

## Usage

```bash
/create-agent <agent-description>
```

**Examples:**
```bash
/create-agent React performance optimization specialist
/create-agent API security auditor for OWASP compliance
/create-agent Database query optimizer for PostgreSQL
/create-agent Accessibility expert for WCAG 2.1 AA compliance
```

## What This Command Does

1. Spawns the `agent-expert` agent in a **separate Task context**
2. The agent-expert will:
   - Research best practices for the domain (using WebSearch if needed)
   - Design the agent with proper hooks configuration
   - Create the agent file with FIRST ACTION and COMPLETION LOGGING sections
   - Follow HTEC naming conventions and patterns
3. Returns the path to the created agent file

## Execution

**IMPORTANT**: This command spawns a subagent. Do NOT execute the agent logic inline - use the Task tool.

```javascript
// Spawn agent-expert in separate context
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Create agent: $ARGUMENTS",
  prompt: `
## Agent: agent-expert

Read your full instructions from: .claude/agents/agent-expert.md

## Your Task

Create a new specialized agent based on this description:

**User Request**: $ARGUMENTS

## Requirements

1. **Research Phase** (if needed):
   - Use WebSearch to find best practices for this domain
   - Identify key expertise areas and anti-patterns
   - Find relevant code examples and patterns

2. **Design Phase**:
   - Determine appropriate stage (discovery/prototype/productspecs/solarch/implementation/quality/utility)
   - Choose model (sonnet for complex reasoning, haiku for structured tasks)
   - Define coordination mode (sequential/parallel)
   - Design hooks configuration

3. **Implementation Phase**:
   - Create the agent file in .claude/agents/
   - Follow HTEC naming convention: {stage}-{domain}.md
   - Include all required sections:
     - YAML frontmatter with hooks
     - How to Use This Agent section
     - FIRST ACTION (MANDATORY) section
     - Core expertise areas
     - When to Use This Agent
     - Domain-specific content
     - COMPLETION LOGGING (MANDATORY) section
     - Execution Logging section

4. **Registry Phase** (if applicable):
   - Identify which registry to update (if any)
   - Provide registry entry format

## Output

Return:
1. Path to created agent file
2. Summary of agent capabilities
3. Example invocation command
4. Registry update instructions (if applicable)
  `
})
```

## Agent Naming Convention

| Stage | Prefix | Example |
|-------|--------|---------|
| Discovery | `discovery-` | `discovery-interview-analyst.md` |
| Prototype | `prototype-` | `prototype-screen-specifier.md` |
| ProductSpecs | `productspecs-` | `productspecs-module-specifier.md` |
| SolArch | `solarch-` | `solarch-tech-researcher.md` |
| Implementation | `implementation-` | `implementation-developer.md` |
| Quality | `quality-` | `quality-security-auditor.md` |
| Planning | `planning-` | `planning-tech-lead.md` |
| Utility | No prefix or descriptive | `agent-expert.md` |

## Model Selection Guide

| Use Case | Model | Rationale |
|----------|-------|-----------|
| Complex reasoning, code generation | `sonnet` | Better at nuanced decisions |
| Structured output, validation | `haiku` | Faster, good for templates |
| Security/Quality auditing | `sonnet` | Needs deep analysis |
| Schema generation | `haiku` | Templated structure |

## Hooks Configuration Templates

### Minimal (Read-only agents)
```yaml
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
```

### Extended (File-modifying agents)
```yaml
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/file_lock_acquire.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
    - matcher: "Bash"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/ruff_validator.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/file_lock_release.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
```

## Related

- **Agent Expert**: `.claude/agents/agent-expert.md`
- **Agents README**: `.claude/agents/README.md`
- **Agent Registries**: `.claude/skills/*_AGENT_REGISTRY.json`
- **Create Skill**: `/create-skill` (for creating skills instead of agents)
- **Create Command**: `/create-command` (for creating commands)
