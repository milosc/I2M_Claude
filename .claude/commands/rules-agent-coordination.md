---
name: rules-agent-coordination
description: Load agent coordination rules (locks, sessions, spawning protocol)
---

# Agent Coordination Rules (On-Demand)

**Loaded when needed**: Multi-agent spawning, lock conflicts, parallel execution

---

## Core Protocols

### 1. Pre-Spawn Validation (MANDATORY)

```
BEFORE spawning agent:
  1. INVOKE: pre_agent_spawn.py --agent-id <id> --task-id <id> --agent-type <type> --files <files>
  2. IF validation passes: Receive session_id → Include in agent context → PROCEED
  3. IF validation fails: DO NOT spawn → REPORT reason → SUGGEST resolution
```

### 2. File Lock Protocol

```
BEFORE any write operation:
  1. ACQUIRE: agent_coordinator.py --acquire-lock <agent_id> <task_id> <file_path>
  2. IF granted: Proceed → Complete work → Release
  3. IF denied: Work on different task OR wait

LOCK TIMEOUT: 15 min (single +15 min extension allowed)
```

### 3. Session Lifecycle

```
START:  session_id = register_session(agent_id, task_id, agent_type)
DURING: Send heartbeat every 30s (long-running)
END:    post_task_completion.py --session-id <id> --status completed|failed
```

---

## Execution Rules

### Parallel Agents

| Type | Count | Notes |
|------|-------|-------|
| Quality agents | 6 parallel | bug-hunter, security-auditor, code-quality, test-coverage, contracts-reviewer, accessibility-auditor |
| Developer agents | Up to 3 | Different tasks, different files, file locks required |
| Process Integrity | Continuous | Read-only monitoring (traceability-guardian, state-watchdog) |

### Sequential Agents (No Parallelism)

1. `tech-lead` → Must complete before developers
2. `checkpoint-auditor` → Runs alone at phase boundaries
3. `playbook-enforcer` → Runs after task completion
4. Reflexion loop: `actor` → `evaluator` → `self-refiner`

---

## Process Integrity Veto

**When Process Integrity agent issues VETO**:
1. Stop non-critical agent spawning
2. Check veto reason: `_state/integrity_status.json`
3. DO NOT proceed past blocked checkpoint
4. Fix violation → Re-validate → Clear veto

**Veto-capable agents**: traceability-guardian, playbook-enforcer, checkpoint-auditor

---

## Agent Invocation Format

```javascript
Task({
  subagent_type: "general-purpose",  // or "Explore", "Plan", "Bash"
  model: "sonnet",                   // or "haiku" for structured tasks
  description: "Brief description",
  prompt: `Agent: <agent-name>
    Read: .claude/agents/<agent-name>.md
    SESSION: {session_id} | TASK: {task_id}
    FILES: {locked_files}
    [instructions]
    ON COMPLETION: Report status for post_task_completion hook`
})
```

---

## Error Handling

### Lock Acquisition Failure
**Check**: `agent_coordinator.py --check-lock <file>`
**Options**: Wait for release | Work on different task | Manual intervention

### Session Registration Failure
**Common Causes**: Max agents (12), integrity veto, instance limit
**Resolution**: Wait | Check `agent_coordinator.py --status` | Cleanup stale

### Integrity Veto Active
**Check**: `_state/integrity_status.json`
**Fix**: Resolve violations → Run `post_task_completion.py --trigger-integrity` → Re-audit

---

## Monitoring Commands

```bash
# Overall status
python3 .claude/hooks/agent_coordinator.py --status

# Check specific lock
python3 .claude/hooks/agent_coordinator.py --check-lock <file>

# Clean stale resources
python3 .claude/hooks/agent_coordinator.py --cleanup-stale
```

**State Files**: `_state/agent_lock.json`, `_state/agent_sessions.json`, `_state/integrity_status.json`

---

## Hook Integration

### Pre-Spawn
```bash
python3 .claude/hooks/pre_agent_spawn.py \
  --agent-id <id> --task-id <id> --agent-type <type> --files <files>
```

### Post-Completion
```bash
python3 .claude/hooks/post_task_completion.py \
  --session-id <id> --status completed|failed --task-id <id>
```

---

## Related

- **Full Architecture**: `architecture/Parallel_Agent_Coordination.md`
- **Agent Coordinator**: `.claude/hooks/agent_coordinator.py`
- **Agent Definitions**: `.claude/agents/`
