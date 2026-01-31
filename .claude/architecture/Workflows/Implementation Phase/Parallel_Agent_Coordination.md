# Parallel Agent Coordination

## Overview

This document defines the coordination mechanisms for multi-agent execution in the HTEC Implementation stage. When multiple specialized agents work in parallel, they must coordinate access to shared resources (files, state, traceability) while maintaining playbook compliance under Process Integrity monitoring.

---

## 1. Agent Categories and Coordination Roles

### Execution Agents (Coordinate via Locks)

| Category | Agents | Coordination Pattern |
|----------|--------|---------------------|
| **Planning** | product-researcher, hfe-ux-researcher, tech-lead | Sequential within category, parallel across |
| **Implementation** | developer, test-automation-engineer | Parallel with file-level locking |
| **Quality** | code-reviewer (6 sub-agents), bug-hunter, security-auditor | Parallel read-only, sequential write |

### Monitoring Agents (No Locks Required)

| Category | Agents | Coordination Pattern |
|----------|--------|---------------------|
| **Process Integrity** | traceability-guardian, state-watchdog, checkpoint-auditor, playbook-enforcer | Continuous read-only monitoring |
| **Reflexion** | actor, evaluator, self-refiner | Sequential per-task |

---

## 2. Agent Lock Protocol

### Lock File Schema

Location: `_state/agent_lock.json`

```json
{
  "version": "1.0.0",
  "locks": [
    {
      "file_path": "src/features/inventory/InventoryList.tsx",
      "agent_id": "developer-001",
      "agent_type": "developer",
      "task_id": "T-015",
      "acquired_at": "2024-12-27T10:30:00Z",
      "expires_at": "2024-12-27T10:45:00Z",
      "lock_type": "exclusive"
    }
  ],
  "global_locks": [
    {
      "resource": "traceability/task_registry.json",
      "agent_id": "tech-lead-001",
      "reason": "task_decomposition",
      "acquired_at": "2024-12-27T10:25:00Z"
    }
  ]
}
```

### Lock Types

| Type | Description | Use Case |
|------|-------------|----------|
| `exclusive` | Single agent access | Code files during implementation |
| `shared_read` | Multiple read, no write | Code review phase |
| `global` | Entire resource locked | Registry updates |

### Lock Acquisition Protocol

```
┌────────────────────────────────────────────────────────────────────────┐
│                        LOCK ACQUISITION FLOW                           │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  1. READ agent_lock.json                                               │
│         │                                                              │
│         ▼                                                              │
│  2. CHECK existing locks for target file(s)                            │
│         │                                                              │
│         ├─── No conflict ───▶ 3. ACQUIRE lock (atomic write)           │
│         │                           │                                  │
│         │                           ▼                                  │
│         │                    4. PROCEED with task                      │
│         │                           │                                  │
│         │                           ▼                                  │
│         │                    5. RELEASE lock on completion             │
│         │                                                              │
│         └─── Conflict ─────▶ 3a. CHECK lock expiration                 │
│                                   │                                    │
│                                   ├─── Expired ───▶ CLAIM lock         │
│                                   │                                    │
│                                   └─── Valid ─────▶ WAIT or SKIP       │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Lock Timeout Configuration

| Agent Type | Default Timeout | Max Extension |
|------------|-----------------|---------------|
| developer | 15 minutes | 30 minutes |
| code-reviewer | 10 minutes | 20 minutes |
| test-automation-engineer | 20 minutes | 45 minutes |
| tech-lead | 5 minutes | 10 minutes |

---

## 3. Agent Session Management

### Session Registry

Location: `_state/agent_sessions.json`

```json
{
  "active_sessions": [
    {
      "session_id": "sess-20241227-001",
      "agent_type": "developer",
      "agent_id": "developer-001",
      "started_at": "2024-12-27T10:00:00Z",
      "current_task": "T-015",
      "current_phase": "GREEN",
      "files_touched": [
        "src/features/inventory/InventoryList.tsx",
        "tests/unit/InventoryList.test.tsx"
      ],
      "status": "active"
    }
  ],
  "completed_sessions": [],
  "failed_sessions": []
}
```

### Session Lifecycle

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SESSION LIFECYCLE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  SPAWN ──▶ REGISTER ──▶ ACQUIRE_LOCKS ──▶ EXECUTE ──▶ RELEASE ──▶ END  │
│    │           │              │              │            │        │    │
│    │           │              │              │            │        │    │
│    │           ▼              ▼              ▼            ▼        ▼    │
│    │      sessions.json  lock.json     task work    lock.json  summary │
│    │                                                                    │
│    └─────────────────── Process Integrity Monitoring ──────────────────┘│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. State Synchronization

### Shared State Files

| File | Purpose | Write Access |
|------|---------|--------------|
| `_state/implementation_progress.json` | Checkpoint tracking | Orchestrator only |
| `_state/implementation_config.json` | Configuration | Read-only after init |
| `traceability/task_registry.json` | Task status | tech-lead, developer |
| `traceability/review_registry.json` | Review findings | code-reviewer agents |

### Synchronization Rules

1. **Read Before Write**: Always read current state before modifications
2. **Atomic Updates**: Use JSON merge patches for partial updates
3. **Conflict Detection**: Check `last_modified` timestamp before write
4. **Retry on Conflict**: If conflict detected, re-read and retry (max 3 attempts)

### State Update Protocol

```json
{
  "operation": "update_task_status",
  "target": "traceability/task_registry.json",
  "agent_id": "developer-001",
  "changes": {
    "path": "$.tasks[?(@.id=='T-015')].status",
    "old_value": "in_progress",
    "new_value": "completed",
    "timestamp": "2024-12-27T10:45:00Z"
  },
  "checksum_before": "abc123",
  "checksum_after": "def456"
}
```

---

## 5. Conflict Resolution

### Priority Matrix

When two agents request the same resource:

| Agent A | Agent B | Winner | Reason |
|---------|---------|--------|--------|
| developer | developer | First arrival | FIFO |
| developer | code-reviewer | developer | Active implementation |
| code-reviewer | code-reviewer | Parallel OK | Read-only |
| tech-lead | developer | tech-lead | Planning priority |
| process-integrity | any | process-integrity | Monitoring priority |

### Deadlock Prevention

```
┌────────────────────────────────────────────────────────────────────────┐
│                      DEADLOCK PREVENTION RULES                         │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  1. ORDERED ACQUISITION                                                │
│     Agents must acquire locks in alphabetical order by file path       │
│                                                                        │
│  2. TIMEOUT ENFORCEMENT                                                │
│     All locks have mandatory expiration (no indefinite locks)          │
│                                                                        │
│  3. SINGLE GLOBAL LOCK                                                 │
│     Only one global lock per agent at a time                           │
│                                                                        │
│  4. PREEMPTION FOR INTEGRITY                                           │
│     Process Integrity agents can preempt on playbook violations        │
│                                                                        │
│  5. WATCHDOG MONITORING                                                │
│     state-watchdog detects stale locks and triggers cleanup            │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Stale Lock Recovery

```bash
# Detected by state-watchdog every 60 seconds
IF lock.expires_at < NOW AND session.status == "active":
    # Attempt graceful termination
    SIGNAL session.agent_id TERM
    WAIT 30 seconds

    IF lock still held:
        # Force release
        REMOVE lock from agent_lock.json
        MARK session as "terminated"
        LOG to FAILURES_LOG.md
```

---

## 6. Process Integrity Monitoring Layer

### Continuous Monitoring Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PROCESS INTEGRITY MONITORING                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    EXECUTION LAYER                              │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │    │
│  │  │developer │  │developer │  │code-rev  │  │test-automation   │ │    │
│  │  │   001    │  │   002    │  │ agents   │  │   engineer       │ │    │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └─────────┬────────┘ │    │
│  └───────┼─────────────┼─────────────┼──────────────────┼──────────┘    │
│          │             │             │                  │               │
│          ▼             ▼             ▼                  ▼               │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                 MONITORING LAYER (Read-Only)                    │    │
│  │  ┌───────────────┐  ┌─────────────┐  ┌────────────────────────┐ │    │
│  │  │ traceability- │  │   state-    │  │     checkpoint-        │ │    │
│  │  │   guardian    │  │  watchdog   │  │       auditor          │ │    │
│  │  └───────┬───────┘  └──────┬──────┘  └───────────┬────────────┘ │    │
│  │          │                 │                     │              │    │
│  │          └─────────────────┼─────────────────────┘              │    │
│  │                            │                                    │    │
│  │                            ▼                                    │    │
│  │               ┌────────────────────────┐                        │    │
│  │               │   playbook-enforcer    │ ◀── VETO POWER         │    │
│  │               └────────────────────────┘                        │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Monitoring Events

| Agent | Monitors | Frequency | Action on Violation |
|-------|----------|-----------|---------------------|
| traceability-guardian | task_registry.json, review_registry.json | Real-time on change | Block write, alert |
| state-watchdog | agent_lock.json, agent_sessions.json | Every 60 seconds | Clean stale, alert |
| checkpoint-auditor | implementation_progress.json | On checkpoint transition | Block if incomplete |
| playbook-enforcer | All TDD compliance, patterns | Per-task completion | Veto phase advance |

### Violation Severity and Response

| Severity | Response Time | Action |
|----------|---------------|--------|
| CRITICAL | Immediate | HALT all agents, alert orchestrator |
| HIGH | < 30 seconds | Block violating agent, continue others |
| MEDIUM | < 2 minutes | Log warning, request correction |
| LOW | End of phase | Include in review report |

---

## 7. Hook Integration

### Pre-Execution Hooks

```python
# hook: pre_agent_spawn
def pre_agent_spawn(agent_type: str, task_id: str) -> bool:
    """
    Called before spawning any execution agent.
    Returns True to allow, False to block.
    """
    # 1. Check agent_sessions for capacity
    if count_active_sessions(agent_type) >= MAX_CONCURRENT[agent_type]:
        return False

    # 2. Verify task not already claimed
    if is_task_locked(task_id):
        return False

    # 3. Check Process Integrity status
    if get_integrity_status() == "BLOCKED":
        return False

    return True
```

### Post-Execution Hooks

```python
# hook: post_task_completion
def post_task_completion(agent_id: str, task_id: str, result: dict) -> None:
    """
    Called after any agent completes a task.
    """
    # 1. Release all locks held by agent
    release_agent_locks(agent_id)

    # 2. Update session status
    close_session(agent_id)

    # 3. Update task registry
    update_task_status(task_id, result['status'], result['artifacts'])

    # 4. Trigger Process Integrity validation
    validate_task_completion(task_id)

    # 5. Check if phase complete
    if is_phase_complete(get_current_phase()):
        trigger_checkpoint_validation()
```

### Integrity Check Hooks

```python
# hook: phase_transition
def phase_transition(from_phase: str, to_phase: str) -> bool:
    """
    Called at blocking checkpoints (CP1, CP6).
    Returns True to allow transition, False to block.
    """
    # Get integrity report
    report = playbook_enforcer.generate_report()

    # Check for blocking violations
    if report.has_violations(severity=['CRITICAL', 'HIGH']):
        log_transition_blocked(from_phase, to_phase, report)
        return False

    # Verify checkpoint requirements
    if not checkpoint_auditor.verify(to_phase):
        return False

    return True
```

---

## 8. Recovery Procedures

### Agent Failure Recovery

```
┌────────────────────────────────────────────────────────────────────────┐
│                      AGENT FAILURE RECOVERY                            │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  FAILURE DETECTED                                                      │
│         │                                                              │
│         ▼                                                              │
│  1. MARK session as "failed" in agent_sessions.json                    │
│         │                                                              │
│         ▼                                                              │
│  2. RELEASE all locks held by failed agent                             │
│         │                                                              │
│         ▼                                                              │
│  3. ASSESS task state:                                                 │
│         │                                                              │
│         ├── No changes ────▶ RESET task to "pending"                   │
│         │                                                              │
│         ├── Partial ───────▶ ROLLBACK changes, RESET task              │
│         │                                                              │
│         └── Complete* ─────▶ VERIFY artifacts, MARK "needs_review"     │
│                                                                        │
│  4. LOG failure details to FAILURES_LOG.md                             │
│         │                                                              │
│         ▼                                                              │
│  5. SPAWN replacement agent if needed                                  │
│                                                                        │
│  * "Complete" means all TDD phases done but not validated              │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Orphaned Lock Cleanup

```json
{
  "cleanup_policy": {
    "scan_interval_seconds": 60,
    "grace_period_seconds": 30,
    "max_lock_age_minutes": 60,
    "cleanup_actions": [
      "release_lock",
      "mark_session_terminated",
      "reset_task_if_incomplete",
      "log_to_failures"
    ]
  }
}
```

### State Corruption Recovery

1. **Detection**: Checksum mismatch or JSON parse failure
2. **Isolation**: Stop all agents writing to corrupted file
3. **Recovery**: Restore from `_state/backups/` (auto-created every 5 minutes)
4. **Verification**: Validate restored state with Process Integrity
5. **Resume**: Restart affected agents from last known good state

---

## 9. Configuration

### Default Configuration

Location: `_state/coordination_config.json`

```json
{
  "version": "1.0.0",
  "concurrency": {
    "max_parallel_developers": 3,
    "max_parallel_reviewers": 6,
    "max_total_agents": 12
  },
  "timeouts": {
    "lock_default_minutes": 15,
    "lock_max_minutes": 45,
    "session_max_hours": 4,
    "cleanup_interval_seconds": 60
  },
  "integrity": {
    "monitoring_enabled": true,
    "blocking_severities": ["CRITICAL", "HIGH"],
    "checkpoint_validation": true
  },
  "recovery": {
    "auto_cleanup_enabled": true,
    "backup_interval_minutes": 5,
    "max_retry_attempts": 3
  }
}
```

---

## 10. Example: Parallel Implementation Phase

```
┌─────────────────────────────────────────────────────────────────────────┐
│                PARALLEL IMPLEMENTATION EXAMPLE                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  tech-lead spawns 3 developers for Phase 4 tasks:                       │
│                                                                         │
│  T-015 [P] ──▶ developer-001 ──▶ LOCKS: InventoryList.tsx               │
│  T-016 [P] ──▶ developer-002 ──▶ LOCKS: InventoryDetail.tsx             │
│  T-017 [P] ──▶ developer-003 ──▶ LOCKS: InventoryForm.tsx               │
│                                                                         │
│  Process Integrity Layer (continuous):                                  │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ traceability-guardian: watching task_registry.json              │    │
│  │ state-watchdog: watching agent_lock.json, agent_sessions.json   │    │
│  │ playbook-enforcer: verifying TDD compliance per task            │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  Timeline:                                                              │
│  ─────────────────────────────────────────────────────────────────────  │
│  T=0     │ All 3 developers spawn, acquire locks                        │
│  T=5min  │ developer-001 completes RED phase                            │
│  T=8min  │ developer-002 completes RED phase                            │
│  T=10min │ developer-001 completes GREEN phase                          │
│  T=12min │ developer-003 completes RED phase (delayed start)            │
│  T=14min │ developer-001 completes REFACTOR, releases lock              │
│          │ playbook-enforcer validates T-015                            │
│  T=15min │ developer-002 completes GREEN phase                          │
│  T=18min │ developer-002 completes REFACTOR, releases lock              │
│  T=20min │ developer-003 completes GREEN phase                          │
│  T=22min │ developer-003 completes REFACTOR, releases lock              │
│  T=23min │ All Phase 4 [P] tasks complete                               │
│          │ checkpoint-auditor triggers CP4 validation                   │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024-12-27 | Claude | Initial parallel agent coordination specification |
