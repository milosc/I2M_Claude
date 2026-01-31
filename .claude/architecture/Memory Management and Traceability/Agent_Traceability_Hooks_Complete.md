# Complete Hooks Implementation for HTEC Framework

**Version**: 2.0.0
**Date**: 2026-01-26
**Objective**: Add hooks to agents, skills, and commands for complete execution tracing

---

## Hook Types Supported

### Global Hooks (`.claude/settings.json`)
All hook events: SessionStart, SessionEnd, UserPromptSubmit, PreToolUse, PostToolUse, Stop, SubagentStop, PreCompact, Notification, PermissionRequest

### Component Hooks (Frontmatter)
**Agents**: PreToolUse, PostToolUse, Stop
**Skills**: PreToolUse, PostToolUse, Stop (with `once` option)
**Commands**: N/A (commands are invoked via Skill tool, so skill hooks apply)

---

## Stop Hooks (MANDATORY)

**Per documentation**: "Stop hooks run when the main Claude Code agent has finished responding."

**Why mandatory**: Logs the END of execution for every agent and skill, completing the call stack trace.

### Global Stop Hook (Already in settings.json)
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type Stop"
          }
        ]
      }
    ]
  }
}
```

### Component-Scoped Stop Hooks
Every agent and skill MUST have a Stop hook to log completion.

---

## Agent Hooks by Category

### 1. Orchestrator Agents

**Purpose**: Track agent spawning and coordinate multi-agent workflows

**Agents**:
- `discovery-orchestrator.md`
- `prototype-orchestrator.md`
- `productspecs-orchestrator.md`
- `solarch-orchestrator.md`

**Frontmatter**:
```yaml
---
name: discovery-orchestrator
description: Master coordinator, 12 checkpoints
model: sonnet
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_spawn.py --stage discovery --checkpoint $CHECKPOINT"
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_result.py --stage discovery"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_complete.py --agent discovery-orchestrator --stage discovery"
---
```

### 2. Analysis Agents

**Purpose**: Track input processing and output generation

**Agents**:
- `discovery-interview-analyst.md`
- `discovery-pdf-analyst.md`
- `discovery-data-analyst.md`
- `discovery-design-analyst.md`

**Frontmatter**:
```yaml
---
name: discovery-interview-analyst
description: Extract pain points and quotes from interview transcripts
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validate_output_structure.py --agent discovery-interview-analyst"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_complete.py --agent discovery-interview-analyst --stage discovery"
---
```

### 3. Validator Agents

**Purpose**: Validate outputs and enforce quality gates

**Agents**:
- `discovery-pain-point-validator.md`
- `discovery-cross-reference-validator.md`
- `productspecs-traceability-validator.md`
- `productspecs-cross-reference-validator.md`
- All `quality-*-auditor.md` agents

**Frontmatter**:
```yaml
---
name: discovery-pain-point-validator
description: Validate pain points against source materials
model: haiku
hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/tag_validation_scan.py --validator pain-point"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validate_pain_point_output.py"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_complete.py --agent discovery-pain-point-validator --stage discovery"
---
```

### 4. Generator Agents

**Purpose**: Generate artifacts from templates or specifications

**Agents**:
- `discovery-persona-generator.md`
- `prototype-design-token-generator.md`
- `prototype-component-specifier.md`
- `productspecs-nfr-generator.md`

**Frontmatter**:
```yaml
---
name: discovery-persona-generator
description: Synthesize persona from pain points and interviews
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validate_persona_structure.py"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_complete.py --agent discovery-persona-generator --stage discovery"
---
```

### 5. Implementation Agents

**Purpose**: Enforce TDD cycle, file locking, and code quality

**Agents**:
- `implementation-developer.md`
- `implementation-test-automation-engineer.md`

**Frontmatter**:
```yaml
---
name: implementation-developer
description: TDD implementation following RED-GREEN-REFACTOR cycle
model: sonnet
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/file_lock_acquire.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/tdd_phase_check.py"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/tdd_compliance_check.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/file_lock_release.py"
    - matcher: "Bash"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/test_result_capture.py"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_complete.py --agent implementation-developer --stage implementation"
---
```

### 6. Quality Agents

**Purpose**: Perform code review and security audits

**Agents**:
- `quality-bug-hunter.md`
- `quality-security-auditor.md`
- `quality-code-quality.md`
- `quality-test-coverage.md`
- `quality-contracts-reviewer.md`
- `quality-accessibility-auditor.md`

**Frontmatter**:
```yaml
---
name: quality-security-auditor
description: OWASP Top 10 security review
model: sonnet
hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/tag_security_scan.py --file $FILE_PATH"
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_security_findings.py"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_complete.py --agent quality-security-auditor --stage implementation"
---
```

### 7. Process Integrity Agents

**Purpose**: Monitor traceability, state, and playbook compliance

**Agents**:
- `process-integrity-traceability-guardian.md`
- `process-integrity-state-watchdog.md`
- `process-integrity-checkpoint-auditor.md`
- `process-integrity-playbook-enforcer.md`

**Frontmatter**:
```yaml
---
name: process-integrity-traceability-guardian
description: Monitor traceability chain integrity
model: haiku
hooks:
  PostToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validate_traceability_chain.py"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_complete.py --agent process-integrity-traceability-guardian --stage utility"
---
```

### 8. Planning Agents

**Purpose**: Task decomposition and code exploration

**Agents**:
- `planning-tech-lead.md`
- `planning-code-explorer.md`

**Frontmatter**:
```yaml
---
name: planning-tech-lead
description: Task decomposition with TDD specifications
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validate_task_spec.py"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_complete.py --agent planning-tech-lead --stage implementation"
---
```

### 9. Reflexion Agents

**Purpose**: Actor-Evaluator-Refiner cycle for change requests

**Agents**:
- `reflexion-actor.md`
- `reflexion-evaluator.md`
- `reflexion-self-refiner.md`

**Frontmatter**:
```yaml
---
name: reflexion-actor
description: Initial implementation attempt
model: sonnet
hooks:
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_complete.py --agent reflexion-actor --stage implementation"
---
```

---

## Skill Hooks

### Skill Hook Structure

```yaml
---
name: skill-name
description: Skill purpose
hooks:
  PreToolUse:
    - matcher: "Tool1|Tool2"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/skill_pre_hook.py"
      once: true  # Optional: Run only once per session (ONLY for skills, NOT agents)
  PostToolUse:
    - matcher: "Tool3|Tool4"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/skill_post_hook.py"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_skill_complete.py --skill skill-name"
---
```

### Discovery Skills

#### /discovery (Main Orchestration)

**File**: `.claude/commands/discovery.md`

```yaml
---
name: /discovery
description: Complete Discovery orchestration
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_discovery_start.py --mode full"
      once: true
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_skill_complete.py --skill discovery --stage discovery"
---
```

#### /discovery-multiagent

```yaml
---
name: /discovery-multiagent
description: Parallel multi-agent Discovery
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_parallel_spawn_start.py --stage discovery"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_skill_complete.py --skill discovery-multiagent --stage discovery"
---
```

#### /discovery-audit

```yaml
---
name: /discovery-audit
description: Zero Hallucination Audit
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_audit_start.py --audit-type zero-hallucination"
      once: true
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_skill_complete.py --skill discovery-audit --stage discovery"
---
```

### Prototype Skills

#### /prototype

```yaml
---
name: /prototype
description: Complete Prototype generation
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_prototype_start.py --mode full"
      once: true
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_skill_complete.py --skill prototype --stage prototype"
---
```

### ProductSpecs Skills

#### /productspecs

```yaml
---
name: /productspecs
description: Complete ProductSpecs generation
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_productspecs_start.py --mode full"
      once: true
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_skill_complete.py --skill productspecs --stage productspecs"
---
```

### SolArch Skills

#### /solarch

```yaml
---
name: /solarch
description: Complete Solution Architecture generation
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_solarch_start.py --mode full"
      once: true
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_skill_complete.py --skill solarch --stage solarch"
---
```

### Implementation Skills

#### /htec-sdd-implement

```yaml
---
name: /htec-sdd-implement
description: Execute TDD implementation
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_implementation_start.py --task $TASK_ID"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_skill_complete.py --skill htec-sdd-implement --stage implementation"
---
```

#### /htec-sdd-review

```yaml
---
name: /htec-sdd-review
description: Multi-agent code review
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_review_start.py --review-type multi-agent"
      once: true
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_skill_complete.py --skill htec-sdd-review --stage implementation"
---
```

---

## Command Hooks

**IMPORTANT**: Commands are invoked via the Skill tool, so they **inherit** the skill's hooks automatically.

**Example**: When a user runs `/discovery`, Claude Code:
1. Invokes the Skill tool with `skill: "discovery"`
2. The `discovery` skill's hooks fire (PreToolUse, PostToolUse, Stop)
3. The skill spawns agents via Task tool
4. Agent hooks fire when agents execute

**No separate command frontmatter needed** - just ensure skills have proper hooks.

---

## Hook Script Examples

### log_agent_complete.py

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def log_agent_complete():
    """Log agent completion with full context."""
    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Extract metadata
    session_id = input_data.get('session_id', 'unknown')
    agent = os.getenv('AGENT_NAME', 'unknown')  # From --agent flag
    stage = os.getenv('STAGE', 'unknown')  # From --stage flag

    # Build event
    event = {
        'event_type': 'Stop',
        'component': 'agent',
        'name': agent,
        'stage': stage,
        'session_id': session_id,
        'timestamp': datetime.now().isoformat(),
        'payload': input_data
    }

    # Append to lifecycle.json
    lifecycle_file = Path(os.getenv('CLAUDE_PROJECT_DIR', '.')) / '_state' / 'lifecycle.json'
    with open(lifecycle_file, 'a') as f:
        f.write(json.dumps(event) + '\n')

    print(f"AGENT_COMPLETE: {agent} (session: {session_id[:8]})")
    sys.exit(0)

if __name__ == '__main__':
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent', required=True)
    parser.add_argument('--stage', required=True)
    args = parser.parse_args()

    # Set environment for the function
    os.environ['AGENT_NAME'] = args.agent
    os.environ['STAGE'] = args.stage

    log_agent_complete()
```

### log_skill_complete.py

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import sys
import os
from datetime import datetime
from pathlib import Path

def log_skill_complete():
    """Log skill completion."""
    input_data = json.load(sys.stdin)

    session_id = input_data.get('session_id', 'unknown')
    skill = os.getenv('SKILL_NAME', 'unknown')
    stage = os.getenv('STAGE', 'unknown')

    event = {
        'event_type': 'Stop',
        'component': 'skill',
        'name': skill,
        'stage': stage,
        'session_id': session_id,
        'timestamp': datetime.now().isoformat(),
        'payload': input_data
    }

    lifecycle_file = Path(os.getenv('CLAUDE_PROJECT_DIR', '.')) / '_state' / 'lifecycle.json'
    with open(lifecycle_file, 'a') as f:
        f.write(json.dumps(event) + '\n')

    print(f"SKILL_COMPLETE: {skill} (session: {session_id[:8]})")
    sys.exit(0)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--skill', required=True)
    parser.add_argument('--stage', required=True)
    args = parser.parse_args()

    os.environ['SKILL_NAME'] = args.skill
    os.environ['STAGE'] = args.stage

    log_skill_complete()
```

---

## Using the `once` Option

**Only for skills, not agents.**

Use `once: true` to run a hook only once per session. After first execution, the hook is removed.

**Use cases**:
- Session initialization (loading context)
- One-time validation (check prerequisites)
- Start-of-workflow logging

**Example**:
```yaml
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_discovery_start.py"
      once: true  # Only logs the first agent spawn, not subsequent ones
```

---

## Implementation Checklist

### Phase 1: Core Hook Scripts (Week 1)
- [ ] Create `log_agent_complete.py`
- [ ] Create `log_skill_complete.py`
- [ ] Create `log_agent_spawn.py`
- [ ] Create `log_agent_result.py`
- [ ] Create `validate_output_structure.py`
- [ ] Create `validate_traceability_chain.py`
- [ ] Create `file_lock_acquire.py` / `file_lock_release.py`
- [ ] Create `tdd_compliance_check.py`
- [ ] Test all scripts standalone

### Phase 2: Agent Hooks (Week 2)
- [ ] Add hooks to orchestrator agents (4 agents)
- [ ] Add hooks to analysis agents (4 agents)
- [ ] Add hooks to validator agents (10+ agents)
- [ ] Add hooks to generator agents (15+ agents)
- [ ] Add hooks to implementation agents (2 agents)
- [ ] Add hooks to quality agents (6 agents)
- [ ] Add hooks to process integrity agents (4 agents)
- [ ] Add hooks to planning agents (2 agents)
- [ ] Add hooks to reflexion agents (3 agents)
- [ ] Test each category with sample workflows

### Phase 3: Skill Hooks (Week 3)
- [ ] Add hooks to Discovery skills (12 skills)
- [ ] Add hooks to Prototype skills (14 skills)
- [ ] Add hooks to ProductSpecs skills (10 skills)
- [ ] Add hooks to SolArch skills (6 skills)
- [ ] Add hooks to Implementation skills (5 skills)
- [ ] Use `once: true` for initialization hooks
- [ ] Test full workflow: /discovery → /prototype → /productspecs

### Phase 4: Validation (Week 4)
- [ ] Run full Discovery workflow and verify logs
- [ ] Run full Prototype workflow and verify logs
- [ ] Check call stack hierarchy in lifecycle.json
- [ ] Verify Stop hooks fire for all agents/skills
- [ ] Test parallel agent spawns (discovery-multiagent)
- [ ] Validate file locking in implementation
- [ ] Test TDD compliance checks

---

## Benefits Summary

| Feature | Without Component Hooks | With Component Hooks |
|---------|-------------------------|----------------------|
| **Agent name extraction** | ❌ Bash regex parsing | ✅ Automatic tagging |
| **Agent-specific validation** | ❌ | ✅ Per-agent validators |
| **TDD enforcement** | ❌ | ✅ File locks + phase checks |
| **File locking** | ❌ | ✅ PreToolUse acquire, PostToolUse release |
| **Execution completion logs** | ❌ Partial (SubagentStop only) | ✅ Complete (Stop hooks everywhere) |
| **Session initialization** | ❌ | ✅ Skill hooks with `once: true` |
| **Logging noise** | High (all events) | Low (filtered by matcher) |

---

## Best Practices

1. **Always add Stop hooks** - Every agent and skill needs a Stop hook
2. **Use matchers to filter** - `matcher: "Write|Edit"` instead of `matcher: ""`
3. **Use `once: true` for init** - Session initialization hooks should run once
4. **Keep hooks fast** - Hooks have 60s timeout, keep them under 5s
5. **Fail gracefully** - Exit 0 even on non-critical errors
6. **Tag with context** - Include agent/skill/stage in hook output
7. **Use absolute paths** - Always use `$CLAUDE_PROJECT_DIR`

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-26 | Initial plan (global hooks only) |
| 2.0.0 | 2026-01-26 | Complete plan with agent/skill hooks, Stop hooks, once option |
