# HTEC Framework Hooks - Quick Reference

**Version**: 3.0.0 (Python-based Traceability)
**Date**: 2026-01-26
**Last Updated**: 2026-01-26T20:15:00

---

## 🚀 New: Python-Based Traceability System

**Status**: ✅ Implemented (Phases 1 & 3)

The framework now uses a Python-based event capture system that provides:
- **Complete call hierarchy** - Command → Agent → Skill → Nested Agent
- **Agent name extraction** - Zero "unknown" agents with proper prompt patterns
- **Full context capture** - Tool inputs, outputs, timestamps, models
- **Call stack tracking** - Parent-child relationships with `pending_spawns.json`
- **Visualization tools** - `view_call_stack.py` for hierarchical display

**Documentation**: See `.claude/architecture/Agent_Traceability_Usage_Guide.md`

---

## Hook Locations

### Global Hooks (Python-Based)
**File**: `.claude/settings.json`
**Script**: `.claude/hooks/capture_event.py` (Python)
**Events**: All hook events (SessionStart, SessionEnd, UserPromptSubmit, PreToolUse, PostToolUse, Stop, SubagentStop, PreCompact, Notification)
**Purpose**: System-wide event capture for call stack building
**Output**: `_state/lifecycle.json`, `_state/pending_spawns.json`, `_state/call_stack_{session_id}.json`

### Component Hooks
**Files**: Agent frontmatter (`.claude/agents/*.md`), Skill frontmatter (`.claude/commands/*.md`)
**Events**: PreToolUse, PostToolUse, Stop
**Purpose**: Component-specific behavior (validation, logging, enforcement)

---

## Quick Syntax

### Agent Hooks
```yaml
---
name: agent-name
description: Agent purpose
model: sonnet|haiku
hooks:
  PreToolUse:
    - matcher: "Tool1|Tool2"  # Optional: specific tools
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/agent_hook.py"
  PostToolUse:
    - matcher: "Tool3|Tool4"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/agent_hook.py"
  Stop:  # MANDATORY - logs completion
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_complete.py --agent agent-name --stage stage"
---
```

### Skill Hooks
```yaml
---
name: /skill-name
description: Skill purpose
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/skill_hook.py"
      once: true  # Run only once per session (ONLY for skills)
  Stop:  # MANDATORY - logs completion
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_skill_complete.py --skill skill-name --stage stage"
---
```

---

## Hook Patterns by Use Case

### 1. Track Agent Spawns (Orchestrators)
```yaml
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_spawn.py --stage $STAGE"
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_result.py --stage $STAGE"
```

### 2. Validate Outputs (Validators)
```yaml
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_output.py"
```

### 3. Enforce TDD (Implementation)
```yaml
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/file_lock_acquire.py"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/tdd_compliance_check.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/file_lock_release.py"
```

### 4. Log Security Scans (Quality)
```yaml
hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/tag_security_scan.py"
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_security_findings.py"
```

### 5. Session Initialization (Skills with once: true)
```yaml
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_workflow_start.py"
      once: true  # Only run on first agent spawn
```

---

## Agent Categories and Hook Patterns

| Agent Type | PreToolUse | PostToolUse | Stop | Use Cases |
|------------|------------|-------------|------|-----------|
| **Orchestrators** | Task spawn logging | Task result logging | ✅ Required | Multi-agent coordination |
| **Analysts** | - | Output validation | ✅ Required | Input processing |
| **Validators** | Validation prep | Output checks | ✅ Required | Quality gates |
| **Generators** | - | Structure validation | ✅ Required | Artifact generation |
| **Implementation** | File locks, TDD phase | TDD checks, lock release | ✅ Required | Code writing |
| **Quality** | Scan tagging | Findings logging | ✅ Required | Code review |
| **Process Integrity** | - | Traceability checks | ✅ Required | Monitoring |
| **Planning** | - | Task spec validation | ✅ Required | Decomposition |

---

## Skill Categories and Hook Patterns

| Skill Type | PreToolUse | PostToolUse | Stop | once |
|------------|------------|-------------|------|------|
| **Orchestration** (/discovery, /prototype) | Start logging | - | ✅ Required | ✅ Yes (start log) |
| **Multi-agent** (/discovery-multiagent) | Parallel spawn log | - | ✅ Required | No |
| **Audit** (/discovery-audit) | Audit start log | - | ✅ Required | ✅ Yes (audit start) |
| **Implementation** (/htec-sdd-implement) | Task start log | - | ✅ Required | No |
| **Review** (/htec-sdd-review) | Review start log | - | ✅ Required | ✅ Yes (review start) |

---

## Stop Hook - MANDATORY

**Every agent and skill MUST have a Stop hook.**

**Why**: Logs the END of execution, completing the call stack trace.

**Agent Stop Hook**:
```yaml
Stop:
  - hooks:
      - type: command
        command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_complete.py --agent $AGENT_NAME --stage $STAGE"
```

**Skill Stop Hook**:
```yaml
Stop:
  - hooks:
      - type: command
        command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_skill_complete.py --skill $SKILL_NAME --stage $STAGE"
```

---

## once: true - Skills Only

**Use `once: true` to run a hook only once per session.**

**Supported**: ✅ Skills
**Not Supported**: ❌ Agents

**Example**:
```yaml
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_workflow_start.py"
      once: true  # Only logs first spawn, not subsequent
```

**Use cases**:
- Session initialization
- Workflow start logging
- One-time prerequisite checks

---

## Commands vs Skills

**Commands are invoked via the Skill tool**, so:
- Commands inherit skill hooks automatically
- No separate command frontmatter for hooks
- Ensure skills have proper hooks defined

**Example**:
```
User: /discovery InventorySystem Client_Materials/
  ↓
Skill tool invoked: skill="discovery"
  ↓
discovery skill's hooks fire (PreToolUse, PostToolUse, Stop)
  ↓
Skill spawns agents via Task tool
  ↓
Agent hooks fire when agents execute
```

---

## Hook Script Templates

### Minimal Agent Stop Hook
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json, sys, os
from datetime import datetime
from pathlib import Path

input_data = json.load(sys.stdin)
session_id = input_data.get('session_id', 'unknown')

event = {
    'event_type': 'Stop',
    'component': 'agent',
    'name': os.getenv('AGENT_NAME', 'unknown'),
    'stage': os.getenv('STAGE', 'unknown'),
    'session_id': session_id,
    'timestamp': datetime.now().isoformat()
}

lifecycle_file = Path(os.getenv('CLAUDE_PROJECT_DIR', '.')) / '_state' / 'lifecycle.json'
with open(lifecycle_file, 'a') as f:
    f.write(json.dumps(event) + '\n')

print(f"AGENT_COMPLETE: {event['name']}")
sys.exit(0)
```

### Minimal Skill Stop Hook
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json, sys, os
from datetime import datetime
from pathlib import Path

input_data = json.load(sys.stdin)
session_id = input_data.get('session_id', 'unknown')

event = {
    'event_type': 'Stop',
    'component': 'skill',
    'name': os.getenv('SKILL_NAME', 'unknown'),
    'stage': os.getenv('STAGE', 'unknown'),
    'session_id': session_id,
    'timestamp': datetime.now().isoformat()
}

lifecycle_file = Path(os.getenv('CLAUDE_PROJECT_DIR', '.')) / '_state' / 'lifecycle.json'
with open(lifecycle_file, 'a') as f:
    f.write(json.dumps(event) + '\n')

print(f"SKILL_COMPLETE: {event['name']}")
sys.exit(0)
```

---

## Testing Checklist

### Agent Hooks
- [ ] Stop hook fires when agent completes
- [ ] PreToolUse hooks fire before tool execution
- [ ] PostToolUse hooks fire after tool success
- [ ] Matchers filter correctly (e.g., "Write|Edit")
- [ ] Multiple hooks execute in parallel
- [ ] Hook failures don't block agent (exit 0)

### Skill Hooks
- [ ] Stop hook fires when skill completes
- [ ] `once: true` runs only once per session
- [ ] PreToolUse logs first agent spawn
- [ ] Hooks don't interfere with agent spawning
- [ ] Multiple skills can have hooks without conflict

---

## Common Pitfalls

### ❌ Wrong: Agent with `once: true`
```yaml
# NOT SUPPORTED - once is ONLY for skills
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "..."
      once: true  # ERROR: Not supported for agents
```

### ✅ Correct: Skill with `once: true`
```yaml
# SUPPORTED - skills can use once
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "..."
      once: true  # OK: Supported for skills
```

### ❌ Wrong: Missing Stop hook
```yaml
# INCOMPLETE - missing Stop hook
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "..."
  # Missing Stop hook!
```

### ✅ Correct: Complete hooks
```yaml
# COMPLETE - includes Stop hook
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "..."
  Stop:  # Required!
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_complete.py"
```

---

## Quick Start: Add Hooks to One Agent

1. **Choose an agent**: Start with a simple one (e.g., `discovery-interview-analyst.md`)

2. **Add Stop hook** (mandatory):
```yaml
---
name: discovery-interview-analyst
description: Extract insights from interviews
model: sonnet
hooks:
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/log_agent_complete.py --agent discovery-interview-analyst --stage discovery"
---
```

3. **Create the hook script**:
```bash
# Create hook directory
mkdir -p .claude/hooks

# Copy the template script from the guide
cp <template> .claude/hooks/log_agent_complete.py

# Make executable
chmod +x .claude/hooks/log_agent_complete.py
```

4. **Test**:
```bash
# Run Discovery and check lifecycle.json
/discovery InventorySystem Client_Materials/

# Verify Stop event logged
tail -f _state/lifecycle.json | grep "discovery-interview-analyst"
```

5. **Repeat** for other agents and skills.

---

## Related Documentation

- **Complete Hooks Guide**: `.claude/architecture/Agent_Traceability_Hooks_Complete.md`
- **Implementation Plan**: `.claude/architecture/Agent_Traceability_Implementation_Plan.md`
- **Claude Code Hooks Docs**: https://code.claude.com/docs/en/hooks
- **HTEC Architecture**: `.claude/architecture/`

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-26 | Initial quick reference |
| 2.0.0 | 2026-01-26 | Complete reference with examples and templates |
