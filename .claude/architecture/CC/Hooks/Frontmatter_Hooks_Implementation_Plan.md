# Frontmatter Hooks Implementation Plan

**Version**: 1.0.0
**Date**: 2026-01-26
**Objective**: Add execution traceability hooks to all agents and skills using frontmatter-style hook configuration

---

## Executive Summary

This plan implements frontmatter-style hooks across all 87+ agents and 115+ skills in the HTEC framework to achieve **complete call stack traceability** from command invocation through nested agent execution.

### Goals

1. **Complete Call Hierarchy** - Trace: Command → Skill → Agent → Nested Agent → Tool Use
2. **Zero Hallucination** - Extract agent/skill names from actual tool inputs, not inferred
3. **Minimal Performance Impact** - Hooks run in parallel, non-blocking
4. **Standardized Patterns** - Role-based hook templates for consistency
5. **Integration with capture_event.py** - Leverage existing Python hook infrastructure

### Key Principles

| Principle | Implementation |
|-----------|----------------|
| **Stop Hook MANDATORY** | Every agent and skill MUST have a Stop hook |
| **Role-Based Patterns** | Different agent roles have different hook needs |
| **Skill once: true** | Skills can use `once: true` for session initialization |
| **Agent No once** | Agents CANNOT use `once: true` (not supported) |
| **Non-Blocking** | All hooks exit 0 (never block execution) |

---

## Agent Categories and Hook Patterns

### 1. Orchestrator Agents

**Role**: Spawn multiple sub-agents and coordinate their execution

**Agents**:
- `discovery-orchestrator`
- `prototype-orchestrator`
- `productspecs-orchestrator`
- `solarch-orchestrator`
- `project-orchestrator`

**Hook Pattern**:

```yaml
---
name: discovery-orchestrator
description: Orchestrate Discovery analysis with parallel agent spawning
model: sonnet
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PreToolUse(Task)** - Log each agent spawn with parent context
- **PostToolUse(Task)** - Link agent completion back to spawn
- **Stop** - Mark orchestrator completion (MANDATORY)

---

### 2. Analyst Agents

**Role**: Process input materials and extract structured insights

**Agents**:
- `discovery-interview-analyst`
- `discovery-pdf-analyst`
- `discovery-data-analyst`
- `discovery-design-analyst`

**Hook Pattern**:

```yaml
---
name: discovery-interview-analyst
description: Extract insights from interview transcripts
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PostToolUse(Write|Edit)** - Log output file creation
- **Stop** - Mark analysis completion
- No PreToolUse needed (input files are parameters, not tool calls)

---

### 3. Validator Agents

**Role**: Verify artifact quality and compliance

**Agents**:
- `discovery-fact-auditor-reviewer`
- `discovery-pain-point-validator`
- `discovery-cross-reference-validator`
- `productspecs-cross-reference-validator`
- `productspecs-traceability-validator`
- `prototype-component-validator`
- `prototype-screen-validator`
- `solarch-adr-validator`

**Hook Pattern**:

```yaml
---
name: discovery-fact-auditor-reviewer
description: Validate all facts are backed by source citations
model: sonnet
hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PreToolUse(Read)** - Track which artifacts being validated
- **PostToolUse(Write)** - Log validation report generation
- **Stop** - Mark validation completion

---

### 4. Generator Agents

**Role**: Create new artifacts from specifications

**Agents**:
- `discovery-persona-generator`
- `discovery-vision-generator`
- `discovery-strategy-generator`
- `discovery-kpis-generator`
- `discovery-roadmap-generator`
- `prototype-design-token-generator`
- `prototype-component-specifier`
- `prototype-screen-specifier`
- `prototype-data-model-specifier`
- `prototype-api-contract-specifier`
- `productspecs-ui-module-specifier`
- `productspecs-api-module-specifier`
- `productspecs-nfr-generator`
- All `solarch-*-generator` agents

**Hook Pattern**:

```yaml
---
name: discovery-persona-generator
description: Generate persona document from research data
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PostToolUse(Write|Edit)** - Log artifact creation
- **Stop** - Mark generation completion
- No PreToolUse needed (specifications provided as parameters)

---

### 5. Implementation Agents

**Role**: Write production code following TDD

**Agents**:
- `implementation-developer`
- `implementation-test-automation-engineer`
- `implementation-test-designer`
- `implementation-documenter`
- `implementation-pr-preparer`

**Hook Pattern**:

```yaml
---
name: implementation-developer
description: TDD implementation with RED-GREEN-REFACTOR cycle
model: sonnet
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
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/tdd_compliance_check.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/file_lock_release.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
    - matcher: "Bash"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PreToolUse(Write|Edit)** - Acquire file lock, prevent conflicts
- **PostToolUse(Write|Edit)** - Validate TDD compliance, release lock
- **PreToolUse(Bash)** / **PostToolUse(Bash)** - Track test execution
- **Stop** - Mark implementation completion

---

### 6. Quality Agents (Code Review)

**Role**: Multi-agent code review with specialized focus areas

**Agents**:
- `quality-bug-hunter`
- `quality-security-auditor`
- `quality-code-quality`
- `quality-test-coverage`
- `quality-contracts-reviewer`
- `quality-accessibility-auditor`

**Hook Pattern**:

```yaml
---
name: quality-security-auditor
description: OWASP Top 10 security analysis
model: sonnet
hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PreToolUse(Read)** - Track files being reviewed
- **PostToolUse(Write)** - Log review findings file
- **Stop** - Mark review completion

---

### 7. Process Integrity Agents

**Role**: Monitor framework compliance and traceability

**Agents**:
- `process-integrity-traceability-guardian`
- `process-integrity-state-watchdog`
- `process-integrity-checkpoint-auditor`
- `process-integrity-playbook-enforcer`

**Hook Pattern**:

```yaml
---
name: process-integrity-traceability-guardian
description: Validate traceability chains and ID integrity
model: haiku
hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PreToolUse(Read)** - Track registry files being checked
- **PostToolUse(Write)** - Log integrity violations
- **Stop** - Mark integrity check completion
- Uses **haiku** for cost efficiency (checklist-based validation)

---

### 8. Planning Agents

**Role**: Research, task decomposition, codebase exploration

**Agents**:
- `planning-tech-lead`
- `planning-code-explorer`

**Hook Pattern**:

```yaml
---
name: planning-tech-lead
description: Decompose module specs into implementation tasks
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PostToolUse(Write|Edit)** - Log task spec creation
- **Stop** - Mark planning completion

---

### 9. Reflexion Agents

**Role**: Self-improvement loop (Actor → Evaluator → Self-Refiner)

**Agents**:
- `reflexion-actor`
- `reflexion-evaluator`
- `reflexion-self-refiner`

**Hook Pattern**:

```yaml
---
name: reflexion-actor
description: Generate initial solution for evaluation
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PostToolUse(Write|Edit)** - Log solution files
- **Stop** - Mark reflexion phase completion

---

## Skill Categories and Hook Patterns

### 1. Orchestration Skills

**Role**: Top-level commands that spawn multiple agents

**Skills**:
- `/discovery`
- `/discovery-multiagent`
- `/prototype`
- `/productspecs`
- `/solarch`
- `/htec-sdd-tasks`
- `/htec-sdd-implement`
- `/htec-sdd-review`

**Hook Pattern**:

```yaml
---
name: /discovery
description: Complete Discovery orchestration with checkpoint-by-checkpoint execution
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
      once: true  # Only log the FIRST agent spawn (workflow start)
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PreToolUse(Task) + once: true** - Log workflow start (only first spawn)
- **PostToolUse(Task)** - Log agent completions (all spawns)
- **Stop** - Mark command completion (MANDATORY)

**Critical**: Skills can use `once: true` to run hooks only once per session

---

### 2. Multi-Agent Parallel Skills

**Role**: Spawn multiple agents in parallel for performance

**Skills**:
- `/discovery-multiagent`

**Hook Pattern**:

```yaml
---
name: /discovery-multiagent
description: Massively parallel Discovery with 60-70% speedup
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PreToolUse(Task)** - Log ALL parallel spawns (no `once: true`)
- **PostToolUse(Task)** - Log ALL parallel completions
- **Stop** - Mark command completion

---

### 3. Audit/Validation Skills

**Role**: Validate artifacts for quality and compliance

**Skills**:
- `/discovery-audit`
- `/discovery-validate`
- `/prototype-validate`
- `/productspecs-validate`
- `/solarch-validate`
- `/integrity-check`

**Hook Pattern**:

```yaml
---
name: /discovery-audit
description: Zero Hallucination Audit - verify all facts are cited
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
      once: true  # Log audit start
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PreToolUse(Task) + once: true** - Log audit start
- **Stop** - Mark audit completion

---

### 4. Feedback Processing Skills

**Role**: Process change requests with impact analysis

**Skills**:
- `/discovery-feedback`
- `/prototype-feedback`
- `/productspecs-feedback`
- `/solarch-feedback`
- `/htec-sdd-changerequest`

**Hook Pattern**:

```yaml
---
name: /prototype-feedback
description: Process prototype feedback with Reflexion loop
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PreToolUse(Task)** - Log feedback analyzer spawn
- **PostToolUse(Task)** - Log implementation completion
- **Stop** - Mark feedback processing completion

---

### 5. Documentation Generation Skills

**Role**: Generate documentation from stage outputs

**Skills**:
- `/discovery-docs-all`
- `/discovery-vision`
- `/discovery-strategy`
- `/discovery-roadmap`
- `/discovery-kpis`
- `/prototype-export`
- `/productspecs-jira`
- `/solarch-docs`

**Hook Pattern**:

```yaml
---
name: /discovery-docs-all
description: Generate all documentation artifacts
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
      once: true  # Log doc generation start
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **PreToolUse(Task) + once: true** - Log doc generation start
- **Stop** - Mark completion

---

### 6. State Management Skills

**Role**: Manage session state and progress

**Skills**:
- `/discovery-init`
- `/discovery-resume`
- `/discovery-reset`
- `/prototype-init`
- `/prototype-resume`
- `/prototype-reset`
- `/productspecs-init`
- `/productspecs-resume`
- `/productspecs-reset`
- `/solarch-init`
- `/solarch-resume`
- `/solarch-reset`

**Hook Pattern**:

```yaml
---
name: /discovery-init
description: Initialize Discovery session configuration
hooks:
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **Stop only** - No agent spawns, just state file updates
- Track session lifecycle events

---

### 7. Utility Skills

**Role**: Single-purpose utilities (no agent spawning)

**Skills**:
- `/discovery-status`
- `/prototype-status`
- `/productspecs-status`
- `/solarch-status`
- `/discovery-files-created`
- `/agent-status`
- `/agent-cleanup`
- `/traceability-status`

**Hook Pattern**:

```yaml
---
name: /discovery-status
description: Show Discovery progress across all checkpoints
hooks:
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Why**:
- **Stop only** - Read-only operations, no spawns
- Track utility invocations

---

## Integration with capture_event.py

### How Frontmatter Hooks Connect to Python Infrastructure

```
Agent/Skill Frontmatter
    ↓
Claude Code Hook Trigger (PreToolUse, PostToolUse, Stop)
    ↓
Command: uv run capture_event.py --event-type X
    ↓
Python Script Execution
    ↓
Extract Context (session_id, tool_input, agent name)
    ↓
Build Event Entry (with call_stack)
    ↓
Append to lifecycle.json + events.db (if server running)
    ↓
Update Call Stack Registry (_state/call_stack_<session>.json)
```

### Event Flow Example

**User Command**: `/discovery InventorySystem Client_Materials/`

```
1. UserPromptSubmit (global hook)
   → capture_event.py logs: {type: "user_prompt", prompt: "/discovery..."}

2. PreToolUse(Skill) (global hook)
   → capture_event.py logs: {type: "skill_start", name: "discovery", parent: "main-123"}

3. PreToolUse(Task) (discovery skill hook + once: true)
   → capture_event.py logs: {type: "agent_spawn", name: "discovery-orchestrator", parent: "discovery"}
   → Stores in pending_spawns.json

4. SessionStart (subagent hook)
   → capture_event.py links: {session: "sub-456", parent: "main-123", call_stack: [...]}

5. PreToolUse(Task) (orchestrator agent hook)
   → capture_event.py logs: {type: "agent_spawn", name: "discovery-interview-analyst", parent: "sub-456"}

6. Stop (analyst agent hook)
   → capture_event.py logs: {type: "agent_complete", session: "sub-789"}

7. PostToolUse(Task) (orchestrator hook)
   → capture_event.py logs: {type: "agent_result", name: "discovery-interview-analyst"}

8. Stop (orchestrator hook)
   → capture_event.py logs: {type: "agent_complete", session: "sub-456"}

9. PostToolUse(Skill) (global hook)
   → capture_event.py logs: {type: "skill_end", name: "discovery"}

10. Stop (skill hook)
    → capture_event.py logs: {type: "skill_complete", name: "discovery"}
```

---

## Migration Strategy

### Phase 1: Agent Hooks (Week 1)

#### 1.1 Process Integrity Agents (Highest Priority)

**Why First**: These agents monitor framework compliance and must be traceable

**Agents**: 4 total
- `process-integrity-traceability-guardian`
- `process-integrity-state-watchdog`
- `process-integrity-checkpoint-auditor`
- `process-integrity-playbook-enforcer`

**Action**:
```bash
# For each agent:
1. Open .claude/agents/{agent-name}.md
2. Add frontmatter hooks (see pattern above)
3. Test with a simple spawn
4. Verify lifecycle.json entry
```

**Verification**:
```bash
# Spawn agent and check logs
python3 .claude/tools/view_call_stack.py | grep "process-integrity"
```

---

#### 1.2 Implementation Agents (Second Priority)

**Why Second**: TDD compliance and file locking require traceability

**Agents**: 5 total
- `implementation-developer`
- `implementation-test-automation-engineer`
- `implementation-test-designer`
- `implementation-documenter`
- `implementation-pr-preparer`

**Action**: Add hooks with file locking support (see pattern above)

---

#### 1.3 Orchestrator Agents (Third Priority)

**Why Third**: Critical for tracking multi-agent workflows

**Agents**: 5 total
- `discovery-orchestrator`
- `prototype-orchestrator`
- `productspecs-orchestrator`
- `solarch-orchestrator`
- `project-orchestrator`

**Action**: Add hooks with Task tracking (see pattern above)

---

#### 1.4 Remaining Agents (Batch Processing)

**Approach**: Group by category, apply category-specific pattern

| Category | Count | Pattern |
|----------|-------|---------|
| Analysts | 4 | PostToolUse(Write) + Stop |
| Validators | 8 | PreToolUse(Read) + PostToolUse(Write) + Stop |
| Generators | 30+ | PostToolUse(Write) + Stop |
| Quality Agents | 6 | PreToolUse(Read) + PostToolUse(Write) + Stop |
| Planning Agents | 2 | PostToolUse(Write) + Stop |
| Reflexion Agents | 3 | PostToolUse(Write) + Stop |

**Script Approach** (Optional):
```python
# .claude/tools/add_agent_hooks.py
import os
import re
from pathlib import Path

def add_hooks_to_agent(agent_file, category):
    """Add category-specific hooks to agent frontmatter"""
    with open(agent_file, 'r') as f:
        content = f.read()

    # Parse existing frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        print(f"⚠️  No frontmatter found: {agent_file}")
        return

    frontmatter = match.group(1)
    body = match.group(2)

    # Check if hooks already exist
    if 'hooks:' in frontmatter:
        print(f"✅ Hooks already exist: {agent_file}")
        return

    # Add hooks based on category
    hooks_yaml = get_hooks_for_category(category)
    new_frontmatter = frontmatter + '\n' + hooks_yaml

    # Write back
    with open(agent_file, 'w') as f:
        f.write(f"---\n{new_frontmatter}\n---\n{body}")

    print(f"✅ Added hooks: {agent_file}")

def get_hooks_for_category(category):
    # Returns YAML hooks for category
    patterns = {
        'orchestrator': ORCHESTRATOR_HOOKS,
        'analyst': ANALYST_HOOKS,
        'validator': VALIDATOR_HOOKS,
        # ... etc
    }
    return patterns.get(category, DEFAULT_HOOKS)

# Run
agents_dir = Path('.claude/agents')
for agent_file in agents_dir.glob('*.md'):
    category = detect_category(agent_file.stem)
    add_hooks_to_agent(agent_file, category)
```

---

### Phase 2: Skill Hooks (Week 2)

#### 2.1 Orchestration Skills (Highest Priority)

**Skills**: 7 total
- `/discovery`
- `/discovery-multiagent`
- `/prototype`
- `/productspecs`
- `/solarch`
- `/htec-sdd-tasks`
- `/htec-sdd-implement`

**Action**: Add hooks with `once: true` for workflow start logging

---

#### 2.2 Feedback Skills (Second Priority)

**Skills**: 5 total
- `/discovery-feedback`
- `/prototype-feedback`
- `/productspecs-feedback`
- `/solarch-feedback`
- `/htec-sdd-changerequest`

**Action**: Add hooks without `once: true` (track all spawns)

---

#### 2.3 Remaining Skills (Batch)

**Approach**: Group by category, apply pattern

| Category | Count | Pattern |
|----------|-------|---------|
| Audit/Validation | 6 | PreToolUse(Task) + once: true + Stop |
| Documentation | 10+ | PreToolUse(Task) + once: true + Stop |
| State Management | 12 | Stop only |
| Utility | 15+ | Stop only |

---

### Phase 3: Verification (Week 3)

#### 3.1 Test Each Agent Category

```bash
# Test orchestrator
python3 test_agent_hooks.py --agent discovery-orchestrator

# Test analyst
python3 test_agent_hooks.py --agent discovery-interview-analyst

# Test validator
python3 test_agent_hooks.py --agent discovery-fact-auditor-reviewer

# ... etc
```

**Test Script**:
```python
# test_agent_hooks.py
import subprocess
import json
from pathlib import Path

def test_agent_hooks(agent_name):
    print(f"Testing: {agent_name}")

    # Clear lifecycle.json
    lifecycle_file = Path('_state/lifecycle.json')
    if lifecycle_file.exists():
        lifecycle_file.unlink()

    # Spawn agent (mock task)
    subprocess.run([
        'uv', 'run',
        '.claude/tools/spawn_agent_test.py',
        '--agent', agent_name
    ])

    # Check lifecycle.json for events
    events = []
    with open(lifecycle_file, 'r') as f:
        for line in f:
            events.append(json.loads(line))

    # Verify expected events
    expected_events = ['PreToolUse', 'PostToolUse', 'Stop']  # Vary by category
    actual_events = [e['event_type'] for e in events if agent_name in str(e)]

    missing = set(expected_events) - set(actual_events)
    if missing:
        print(f"❌ Missing events: {missing}")
    else:
        print(f"✅ All events logged")

    # Verify call stack
    last_event = events[-1]
    if 'call_stack' not in last_event:
        print(f"❌ Missing call_stack")
    else:
        print(f"✅ Call stack: {last_event['call_stack']}")

# Run tests
for agent in ['discovery-orchestrator', 'discovery-interview-analyst', ...]:
    test_agent_hooks(agent)
```

---

#### 3.2 Test End-to-End Workflows

```bash
# Full Discovery workflow
/discovery TestSystem sample_materials/

# Check call stack
python3 .claude/tools/view_call_stack.py

# Expected output:
# ├─ [timestamp] session:main (started)
# │  ├─ [timestamp] user_prompt:prompt (submitted)
# │  ├─ [timestamp] skill:discovery (pre_invoke)
# │  │  ├─ [timestamp] agent:discovery-orchestrator (pre_spawn)
# │  │  │  ├─ [timestamp] agent:discovery-interview-analyst (pre_spawn)
# │  │  │  │  └─ [timestamp] agent:discovery-interview-analyst (stopped)
# │  │  │  └─ [timestamp] agent:discovery-orchestrator (stopped)
# │  │  └─ [timestamp] skill:discovery (stopped)
```

---

### Phase 4: Documentation and Monitoring (Week 4)

#### 4.1 Update Documentation

**Files to Update**:
- `CLAUDE.md` - Add hooks section to Multi-Agent Architecture
- `.claude/agents/README.md` - Add frontmatter hooks examples
- `.claude/skills/README.md` - Add skill hooks examples
- `architecture/Agent_Spawning_Architecture.md` - Add hooks section

---

#### 4.2 Create Monitoring Dashboard (Optional)

**Option 1: Simple CLI Tool**

```bash
# Real-time event stream
python3 .claude/tools/watch_events.py

# Output:
# [10:00:05] skill:discovery → STARTED
# [10:00:06]   agent:discovery-orchestrator → SPAWNED
# [10:00:07]     agent:discovery-interview-analyst → SPAWNED
# [10:00:10]     agent:discovery-interview-analyst → COMPLETED
# [10:00:15]   agent:discovery-orchestrator → COMPLETED
# [10:00:16] skill:discovery → COMPLETED
```

**Option 2: Port Observability Server**

- Copy server from `sample/claude-code-hooks-multi-agent-observability-main/`
- Update `capture_event.py` to send events to server (already included)
- Start server: `cd .claude/observability && ./start-system.sh`
- Open UI: `http://localhost:5173`

---

## Hook Scripts Reference

### Required Hook Scripts

All hook scripts are in `.claude/hooks/`:

| Script | Purpose | Used By |
|--------|---------|---------|
| `capture_event.py` | Universal event capture | All agents/skills |
| `file_lock_acquire.py` | Acquire file lock | Implementation agents |
| `file_lock_release.py` | Release file lock | Implementation agents |
| `tdd_compliance_check.py` | Validate TDD cycle | Implementation agents |

**Create Missing Scripts**:

```bash
# File lock acquire
cat > .claude/hooks/file_lock_acquire.py << 'EOF'
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json, sys, os
from pathlib import Path
from datetime import datetime, timedelta

input_data = json.load(sys.stdin)
tool_input = input_data.get('tool_input', {})
file_path = tool_input.get('file_path', 'unknown')
session_id = input_data.get('session_id', 'unknown')

# Load lock registry
lock_file = Path('_state/agent_lock.json')
locks = []
if lock_file.exists():
    with open(lock_file, 'r') as f:
        locks = json.load(f).get('locks', [])

# Check for existing lock
for lock in locks:
    if lock['file_path'] == file_path:
        expires_at = datetime.fromisoformat(lock['expires_at'])
        if datetime.now() < expires_at:
            print(f"FILE_LOCKED: {file_path} by {lock['agent_id']}")
            sys.exit(1)  # Block (locked)

# Acquire lock
lock_entry = {
    'lock_id': f"lock-{session_id}-{file_path.replace('/', '-')}",
    'file_path': file_path,
    'agent_id': os.getenv('AGENT_ID', 'unknown'),
    'session_id': session_id,
    'acquired_at': datetime.now().isoformat(),
    'expires_at': (datetime.now() + timedelta(minutes=15)).isoformat()
}
locks.append(lock_entry)

# Write back
with open(lock_file, 'w') as f:
    json.dump({'locks': locks}, f, indent=2)

print(f"LOCK_ACQUIRED: {file_path}")
sys.exit(0)
EOF

chmod +x .claude/hooks/file_lock_acquire.py
```

```bash
# File lock release
cat > .claude/hooks/file_lock_release.py << 'EOF'
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json, sys, os
from pathlib import Path

input_data = json.load(sys.stdin)
session_id = input_data.get('session_id', 'unknown')

# Load lock registry
lock_file = Path('_state/agent_lock.json')
locks = []
if lock_file.exists():
    with open(lock_file, 'r') as f:
        locks = json.load(f).get('locks', [])

# Remove locks for this session
locks = [lock for lock in locks if lock['session_id'] != session_id]

# Write back
with open(lock_file, 'w') as f:
    json.dump({'locks': locks}, f, indent=2)

print(f"LOCKS_RELEASED: session {session_id}")
sys.exit(0)
EOF

chmod +x .claude/hooks/file_lock_release.py
```

```bash
# TDD compliance check
cat > .claude/hooks/tdd_compliance_check.py << 'EOF'
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json, sys, os
from pathlib import Path

input_data = json.load(sys.stdin)
tool_input = input_data.get('tool_input', {})
file_path = tool_input.get('file_path', 'unknown')

# Check if test file or implementation file
is_test = 'test' in file_path or 'spec' in file_path

# Load TDD state (_state/tdd_state.json)
tdd_state_file = Path('_state/tdd_state.json')
tdd_state = {}
if tdd_state_file.exists():
    with open(tdd_state_file, 'r') as f:
        tdd_state = json.load(f)

current_phase = tdd_state.get('phase', 'UNKNOWN')

# TDD Phase Validation
if is_test and current_phase != 'RED':
    print(f"⚠️  TDD_WARNING: Writing test in {current_phase} phase (expected RED)")
    # Don't block, just warn
elif not is_test and current_phase != 'GREEN':
    print(f"⚠️  TDD_WARNING: Writing implementation in {current_phase} phase (expected GREEN)")

print(f"TDD_CHECK: {file_path} in {current_phase} phase")
sys.exit(0)
EOF

chmod +x .claude/hooks/tdd_compliance_check.py
```

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Zero "unknown" agents** | 100% | All agent names extracted from prompts |
| **Complete call stacks** | 100% | Every subagent linked to parent session |
| **Hook coverage** | 100% | All agents and skills have Stop hook |
| **Event integrity** | 100% | All PreToolUse have matching PostToolUse |
| **Performance impact** | <5% overhead | Hook execution time vs total execution |

---

## Testing Checklist

### Agent Hooks

- [ ] Stop hook fires when agent completes
- [ ] PreToolUse hooks fire before tool execution
- [ ] PostToolUse hooks fire after tool success
- [ ] Matchers filter correctly (e.g., "Write|Edit")
- [ ] Multiple hooks execute in parallel
- [ ] Hook failures don't block agent (exit 0)
- [ ] Agent name extracted from prompt
- [ ] Call stack inherited from parent

### Skill Hooks

- [ ] Stop hook fires when skill completes
- [ ] `once: true` runs only once per session
- [ ] PreToolUse logs first agent spawn
- [ ] Hooks don't interfere with agent spawning
- [ ] Multiple skills can have hooks without conflict
- [ ] Skill name extracted from Skill tool's `.skill` field

### End-to-End Workflows

- [ ] `/discovery` - Full call stack logged
- [ ] `/discovery-multiagent` - Parallel spawns tracked
- [ ] `/prototype` - Nested agent hierarchy captured
- [ ] `/htec-sdd-implement` - TDD phases tracked
- [ ] `/htec-sdd-review` - Multi-agent review logged

---

## Rollback Plan

If implementation causes issues:

```bash
# Remove hooks from all agents
python3 .claude/tools/remove_agent_hooks.py

# Remove hooks from all skills
python3 .claude/tools/remove_skill_hooks.py

# Restore global hooks only
cp .claude/settings.json.backup .claude/settings.json

# Verify basic logging still works
tail -f _state/lifecycle.json
```

---

## Common Pitfalls and Solutions

### ❌ Pitfall 1: Agent with `once: true`

```yaml
# WRONG - once is NOT supported for agents
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "..."
      once: true  # ❌ ERROR
```

**Solution**: Remove `once: true` from agent hooks (only for skills)

---

### ❌ Pitfall 2: Missing Stop Hook

```yaml
# WRONG - incomplete hooks
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "..."
  # Missing Stop hook!
```

**Solution**: Always add Stop hook (MANDATORY)

---

### ❌ Pitfall 3: Blocking Hook (exit 1)

```python
# WRONG - hook blocks execution
if validation_failed:
    sys.exit(1)  # ❌ Blocks agent
```

**Solution**: Always exit 0 (log warnings, don't block)

---

### ❌ Pitfall 4: Hook Depends on Previous Hook

```yaml
# WRONG - hooks run in parallel, not sequential
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "acquire_lock.py"  # Runs in parallel
        - type: command
          command: "validate_file.py"  # May run before lock acquired!
```

**Solution**: Use single hook script that does both operations sequentially

---

## Related Documentation

- **Hooks Quick Reference**: `.claude/architecture/Hooks_Quick_Reference.md`
- **Agent Traceability Implementation Plan**: `.claude/architecture/Agent_Traceability_Implementation_Plan.md`
- **Agent Spawning Architecture**: `.claude/architecture/Agent_Spawning_Architecture.md`
- **Traceability System**: `.claude/architecture/Traceability_System.md`
- **Claude Code Hooks Docs**: https://code.claude.com/docs/en/hooks

---

## Summary

This plan provides:

1. **87+ agent definitions** with role-specific hook patterns
2. **115+ skill definitions** with category-specific hooks
3. **Complete call stack traceability** from command → skill → agent → nested agents
4. **4-week migration strategy** with prioritization and batch processing
5. **Verification tools** for testing hook correctness
6. **Integration with capture_event.py** for unified event capture
7. **Zero hallucination** agent name extraction from prompts

**Next Steps**:
1. Start with Phase 1.1 (Process Integrity Agents)
2. Test with one agent from each category
3. Use batch scripting for remaining agents
4. Verify end-to-end workflows
5. Enable optional observability server for real-time monitoring

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-26 | Initial frontmatter hooks implementation plan |
