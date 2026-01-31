---
description: Spawn specialized agent for specific task with coordination and locking
argument-hint: <agent-type> <task-id>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /agent-spawn started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /agent-spawn ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /agent-spawn instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## Execution

# /agent-spawn Command

Manually spawn a specific agent type for a task.

## Usage

```
/agent-spawn <agent-type> <task-id> [--files <files>]
/agent-spawn developer T-015 --files src/services/OrderService.ts
/agent-spawn code-review          # Spawn all 6 review agents in parallel
```

## Available Agents

### Planning Agents
| Agent | ID | Description |
|-------|----|----|
| tech-lead | `planning-tech-lead` | Task decomposition and sprint planning |
| code-explorer | `planning-code-explorer` | Codebase analysis and mapping |

**Note**: `planning-product-researcher` and `planning-hfe-ux-researcher` are archived (see `.claude/agents/archived/`). These agents are used in Discovery/Prototype phases but not in Implementation Phase.

### Implementation Agents
| Agent | ID | Description |
|-------|----|----|
| developer | `implementation-developer` | TDD implementation (max 3 parallel) |
| test-automation | `implementation-test-automation-engineer` | E2E test setup |

### Quality Agents (Code Review)
| Agent | ID | Description |
|-------|----|----|
| bug-hunter | `quality-bug-hunter` | Logic errors and edge cases |
| security-auditor | `quality-security-auditor` | OWASP Top 10 and security |
| code-quality | `quality-code-quality` | SOLID, DRY, complexity |
| test-coverage | `quality-test-coverage` | Missing tests |
| contracts-reviewer | `quality-contracts-reviewer` | API contract compliance |
| accessibility-auditor | `quality-accessibility-auditor` | WCAG compliance |

### Process Integrity Agents
| Agent | ID | Description |
|-------|----|----|
| traceability-guardian | `process-integrity-traceability-guardian` | Trace link validation |
| state-watchdog | `process-integrity-state-watchdog` | Lock and session health |
| checkpoint-auditor | `process-integrity-checkpoint-auditor` | Gate validation |
| playbook-enforcer | `process-integrity-playbook-enforcer` | TDD compliance |

### Reflexion Agents
| Agent | ID | Description |
|-------|----|----|
| actor | `reflexion-actor` | Solution generation |
| evaluator | `reflexion-evaluator` | Solution critique |
| self-refiner | `reflexion-self-refiner` | Final polish |

## Spawn Process

### 1. Register Intent (MANDATORY)
Before spawning, ensure the agent's task is registered in the appropriate manifest (e.g., `_state/agent_spawn_manifest.json`). This ensures visibility in the i2m Conductor "Plan vs Actual" view.

### 2. Prepare & Validate
```bash
# Full spawn preparation
python3 .claude/hooks/pre_agent_spawn.py \
  --agent-id developer-001 \
  --task-id T-015 \
  --agent-type implementation-developer \
  --files src/services/OrderService.ts
```

Returns:
- `session_id` for tracking
- `locks_acquired` list
- Error if validation fails

## Special Commands

### Code Review (All 6 Agents)

```
/agent-spawn code-review --target src/
```

Spawns all 6 quality agents in parallel:
- bug-hunter
- security-auditor
- code-quality
- test-coverage
- contracts-reviewer
- accessibility-auditor

### Reflexion Loop

```
/agent-spawn reflexion --task T-015
```

Spawns reflexion loop: actor → evaluator → self-refiner

## Output

### Success

```markdown
## Agent Spawn: implementation-developer

**Status**: SPAWNED
**Session ID**: session-abc123
**Task**: T-015

**Locks Acquired**:
- src/services/OrderService.ts (lock-xyz789)

**Agent Context**:
```json
{
  "session_id": "session-abc123",
  "task_id": "T-015",
  "files": ["src/services/OrderService.ts"],
  "locks": ["lock-xyz789"]
}
```

Agent is now active. Monitor with `/agent-status`.
```

### Blocked

```markdown
## Agent Spawn: BLOCKED

**Reason**: File is locked by another agent

**Details**:
- File: src/services/OrderService.ts
- Locked By: developer-002
- Task: T-016
- Expires: 10 minutes

**Options**:
1. Wait for lock to release
2. Work on different task
3. Force unlock with `/agent-cleanup --lock <file>`
```

## Related

- **Agent Status**: `/agent-status`
- **Agent Cleanup**: `/agent-cleanup`
- **Pre-Spawn Hook**: `.claude/hooks/pre_agent_spawn.py`
- **Agent Definitions**: `.claude/agents/`
