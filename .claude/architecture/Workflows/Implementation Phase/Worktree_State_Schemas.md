# Worktree State Schemas

**Version**: 3.0.0 (Worktree Support)
**Last Updated**: 2026-01-26
**Status**: Active

---

## Overview

This document defines the updated state schemas for worktree-aware coordination in the Implementation Phase. The schemas support parallel development across multiple git worktrees while maintaining proper coordination for shared resources.

---

## Schema Changes Summary

| Schema File | New Fields | Purpose |
|-------------|-----------|----------|
| `_state/agent_sessions.json` | `pr_group`, `worktree_path`, `branch`, `lock_scope` | Track agent worktree context |
| `_state/agent_lock.json` | `lock_key`, `lock_scope`, `worktree_path`, `pr_group` | Enable worktree-scoped locking |

---

## 1. Agent Sessions Schema

**File**: `_state/agent_sessions.json`

### Purpose
Tracks active agent sessions with worktree context for parallel PR development.

### Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Sessions Registry",
  "type": "object",
  "properties": {
    "sessions": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "session_id": {
            "type": "string",
            "pattern": "^sess-[a-zA-Z0-9]{8}$",
            "description": "Unique session identifier"
          },
          "agent_id": {
            "type": "string",
            "description": "Agent instance identifier"
          },
          "agent_type": {
            "type": "string",
            "enum": ["developer", "bug-hunter", "security-auditor", "code-quality", "test-coverage", "contracts-reviewer", "accessibility-auditor"],
            "description": "Agent type/role"
          },
          "task_id": {
            "type": "string",
            "pattern": "^T-\\d{3}$",
            "description": "Task being executed"
          },
          "pr_group": {
            "type": ["string", "null"],
            "pattern": "^PR-\\d{3}$",
            "description": "PR group ID (null if not in PR workflow)"
          },
          "worktree_path": {
            "type": ["string", "null"],
            "description": "Path to worktree (e.g., ../worktrees/pr-001-auth)"
          },
          "branch": {
            "type": ["string", "null"],
            "description": "Git branch name (e.g., feature/pr-001-auth)"
          },
          "lock_scope": {
            "type": "string",
            "enum": ["worktree", "global"],
            "default": "global",
            "description": "Default lock scope for this agent's operations"
          },
          "started_at": {
            "type": "string",
            "format": "date-time",
            "description": "Session start timestamp"
          },
          "last_heartbeat": {
            "type": "string",
            "format": "date-time",
            "description": "Last activity timestamp"
          },
          "status": {
            "type": "string",
            "enum": ["active", "completed", "failed", "stale"],
            "description": "Session status"
          }
        },
        "required": ["session_id", "agent_id", "agent_type", "started_at", "status"]
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "last_updated": {
          "type": "string",
          "format": "date-time"
        },
        "active_count": {
          "type": "integer",
          "minimum": 0
        }
      }
    }
  }
}
```

### Example Entry

```json
{
  "sessions": {
    "sess-a1b2c3d4": {
      "session_id": "sess-a1b2c3d4",
      "agent_id": "developer-001",
      "agent_type": "developer",
      "task_id": "T-015",
      "pr_group": "PR-001",
      "worktree_path": "../worktrees/pr-001-auth",
      "branch": "feature/pr-001-auth",
      "lock_scope": "worktree",
      "started_at": "2026-01-26T10:30:00Z",
      "last_heartbeat": "2026-01-26T10:32:15Z",
      "status": "active"
    },
    "sess-e5f6g7h8": {
      "session_id": "sess-e5f6g7h8",
      "agent_id": "developer-002",
      "agent_type": "developer",
      "task_id": "T-042",
      "pr_group": "PR-002",
      "worktree_path": "../worktrees/pr-002-inventory",
      "branch": "feature/pr-002-inventory",
      "lock_scope": "worktree",
      "started_at": "2026-01-26T10:31:00Z",
      "last_heartbeat": "2026-01-26T10:32:30Z",
      "status": "active"
    }
  },
  "metadata": {
    "last_updated": "2026-01-26T10:32:30Z",
    "active_count": 2
  }
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | Yes | Unique identifier (sess-XXXXXXXX) |
| `agent_id` | string | Yes | Agent instance identifier |
| `agent_type` | enum | Yes | Agent role/type |
| `task_id` | string | Yes | Task being executed (T-XXX) |
| `pr_group` | string\|null | No | PR group ID (PR-XXX) or null |
| `worktree_path` | string\|null | No | Path to worktree or null |
| `branch` | string\|null | No | Git branch name or null |
| `lock_scope` | enum | No | Default lock scope (worktree/global) |
| `started_at` | datetime | Yes | Session start time |
| `last_heartbeat` | datetime | Yes | Last activity timestamp |
| `status` | enum | Yes | Session status |

### Lock Scope Defaults

| Agent Type | Default Lock Scope | Reasoning |
|------------|-------------------|-----------|
| `developer` | `worktree` | Most operations are file writes in src/ |
| `bug-hunter` | `global` | Read-only reviews across codebase |
| `security-auditor` | `global` | Read-only reviews across codebase |
| `code-quality` | `global` | Read-only reviews across codebase |
| `test-coverage` | `global` | Analyzes coverage across project |
| `contracts-reviewer` | `global` | Validates against specs (read-only) |
| `accessibility-auditor` | `global` | Read-only UI reviews |

---

## 2. Agent Lock Schema

**File**: `_state/agent_lock.json`

### Purpose
Tracks file locks with worktree-aware scoping to enable parallel development while preventing conflicts.

### Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Agent Lock Registry",
  "type": "object",
  "properties": {
    "locks": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "lock_key": {
            "type": "string",
            "description": "Unique lock identifier (worktree-scoped or global)"
          },
          "file_path": {
            "type": "string",
            "description": "Relative path to locked file"
          },
          "lock_scope": {
            "type": "string",
            "enum": ["worktree", "global"],
            "description": "Lock scope type"
          },
          "worktree_path": {
            "type": ["string", "null"],
            "description": "Worktree path for worktree-scoped locks (null for global)"
          },
          "pr_group": {
            "type": ["string", "null"],
            "pattern": "^PR-\\d{3}$",
            "description": "PR group ID (null for global locks)"
          },
          "branch": {
            "type": ["string", "null"],
            "description": "Git branch name (null for global locks)"
          },
          "agent_id": {
            "type": "string",
            "description": "Agent holding the lock"
          },
          "agent_type": {
            "type": "string",
            "description": "Agent type"
          },
          "task_id": {
            "type": "string",
            "pattern": "^T-\\d{3}$",
            "description": "Associated task ID"
          },
          "acquired_at": {
            "type": "string",
            "format": "date-time",
            "description": "Lock acquisition time"
          },
          "expires_at": {
            "type": "string",
            "format": "date-time",
            "description": "Lock expiration time"
          },
          "lock_type": {
            "type": "string",
            "enum": ["exclusive", "shared"],
            "description": "Lock type (always exclusive for writes)"
          }
        },
        "required": ["lock_key", "file_path", "lock_scope", "agent_id", "acquired_at", "expires_at", "lock_type"]
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "last_updated": {
          "type": "string",
          "format": "date-time"
        },
        "active_locks": {
          "type": "integer",
          "minimum": 0
        }
      }
    }
  }
}
```

### Example Entries

#### Worktree-Scoped Lock

```json
{
  "locks": {
    "../worktrees/pr-001-auth:src/features/auth/login.ts": {
      "lock_key": "../worktrees/pr-001-auth:src/features/auth/login.ts",
      "file_path": "src/features/auth/login.ts",
      "lock_scope": "worktree",
      "worktree_path": "../worktrees/pr-001-auth",
      "pr_group": "PR-001",
      "branch": "feature/pr-001-auth",
      "agent_id": "developer-001",
      "agent_type": "developer",
      "task_id": "T-015",
      "acquired_at": "2026-01-26T10:30:00Z",
      "expires_at": "2026-01-26T10:45:00Z",
      "lock_type": "exclusive"
    }
  }
}
```

#### Global-Scoped Lock

```json
{
  "locks": {
    "traceability/task_registry.json": {
      "lock_key": "traceability/task_registry.json",
      "file_path": "traceability/task_registry.json",
      "lock_scope": "global",
      "worktree_path": null,
      "pr_group": null,
      "branch": null,
      "agent_id": "developer-001",
      "agent_type": "developer",
      "task_id": "T-015",
      "acquired_at": "2026-01-26T10:32:00Z",
      "expires_at": "2026-01-26T10:34:00Z",
      "lock_type": "exclusive"
    }
  }
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `lock_key` | string | Yes | Unique lock identifier |
| `file_path` | string | Yes | Relative path to locked file |
| `lock_scope` | enum | Yes | Lock scope (worktree/global) |
| `worktree_path` | string\|null | No | Worktree path (null for global) |
| `pr_group` | string\|null | No | PR group ID (null for global) |
| `branch` | string\|null | No | Git branch (null for global) |
| `agent_id` | string | Yes | Agent holding lock |
| `agent_type` | string | Yes | Agent type |
| `task_id` | string | Yes | Associated task (T-XXX) |
| `acquired_at` | datetime | Yes | Lock acquisition time |
| `expires_at` | datetime | Yes | Lock expiration time |
| `lock_type` | enum | Yes | Lock type (exclusive/shared) |

### Lock Key Format

**Worktree-Scoped Lock Key**:
```
{worktree_path}:{file_path}
Example: ../worktrees/pr-001-auth:src/features/auth/login.ts
```

**Global-Scoped Lock Key**:
```
{file_path}
Example: traceability/task_registry.json
```

### Lock Scope Determination

Files are assigned lock scopes based on their path:

| Path Pattern | Lock Scope | Reasoning |
|-------------|-----------|-----------|
| `src/**/*` | worktree | Source code isolated per worktree |
| `tests/**/*` | worktree | Tests isolated per worktree |
| `public/**/*` | worktree | Static assets isolated per worktree |
| `_state/**/*` | global | Shared state across all agents |
| `traceability/**/*` | global | Shared traceability data |
| `.claude/**/*` | global | Framework configuration |
| Other paths | global | Default to global for safety |

### Lock Timeout Values

| Lock Scope | Default Timeout | Max Extension | Use Case |
|------------|----------------|---------------|----------|
| worktree | 15 minutes | 30 minutes | Source/test file modification |
| global | 2 minutes | 5 minutes | Registry updates (short operations) |

---

## 3. Lock Conflict Resolution

### Conflict Detection

```javascript
function checkLockConflict(requestedLock, existingLocks) {
  for (const existingLock of existingLocks) {
    // Check if lock keys match
    if (requestedLock.lock_key === existingLock.lock_key) {
      // Check if existing lock is expired
      if (new Date(existingLock.expires_at) < new Date()) {
        return { conflict: false, reason: "expired_lock" };
      }

      // Same lock key = conflict
      return { conflict: true, reason: "lock_key_conflict" };
    }
  }

  return { conflict: false, reason: "no_conflict" };
}
```

### Conflict Resolution Rules

| Scenario | Lock Scope 1 | Lock Scope 2 | File | Result |
|----------|--------------|--------------|------|--------|
| Same worktree, same file | worktree | worktree | `src/auth.ts` | **CONFLICT** |
| Different worktrees, same file | worktree | worktree | `src/auth.ts` | **ALLOW** (different lock_keys) |
| Any agent, global file | global | global | `traceability/task_registry.json` | **CONFLICT** |
| Worktree + global file | worktree | global | `traceability/task_registry.json` | **CONFLICT** (always sequential) |

---

## 4. Migration Guide

### Upgrading from v2.0.0 (No Worktree Support)

**Old Schema (v2.0.0)**:
```json
{
  "sessions": {
    "sess-abc123": {
      "session_id": "sess-abc123",
      "agent_id": "developer-001",
      "task_id": "T-015",
      "started_at": "2026-01-26T10:30:00Z"
    }
  }
}
```

**New Schema (v3.0.0)**:
```json
{
  "sessions": {
    "sess-abc123": {
      "session_id": "sess-abc123",
      "agent_id": "developer-001",
      "agent_type": "developer",
      "task_id": "T-015",
      "pr_group": null,
      "worktree_path": null,
      "branch": null,
      "lock_scope": "global",
      "started_at": "2026-01-26T10:30:00Z",
      "last_heartbeat": "2026-01-26T10:32:00Z",
      "status": "active"
    }
  }
}
```

**Migration Steps**:
1. Add `pr_group: null` to all existing sessions
2. Add `worktree_path: null` to all existing sessions
3. Add `branch: null` to all existing sessions
4. Add `lock_scope: "global"` to all existing sessions
5. Add `agent_type` field based on agent_id prefix
6. Add `last_heartbeat` (copy from started_at)
7. Add `status: "active"` or "stale" based on age

### Backward Compatibility

- **v2.0.0 agents**: Can still operate (null worktree fields = single-branch workflow)
- **v3.0.0 agents**: Fully worktree-aware, check for null worktree fields before using
- **Mixed workflows**: Supported (some tasks in worktrees, others in main)

---

## 5. Validation

### Schema Validation Script

```bash
# Validate agent_sessions.json schema
python3 .claude/hooks/validate_schemas.py \
  --schema agent_sessions \
  --file _state/agent_sessions.json

# Validate agent_lock.json schema
python3 .claude/hooks/validate_schemas.py \
  --schema agent_lock \
  --file _state/agent_lock.json
```

### Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Missing `lock_key` | Old lock format | Regenerate lock with new schema |
| Invalid `pr_group` format | Incorrect ID pattern | Use PR-XXX format |
| Mismatched `lock_scope` and `worktree_path` | Inconsistent data | Worktree-scoped locks must have worktree_path |
| Expired lock not cleaned | Stale lock entry | Run cleanup: `python3 .claude/hooks/cleanup_locks.py` |

---

## 6. Related Documentation

- **Worktree Commands**: `.claude/commands/htec-sdd-worktree-setup.md`
- **Agent Coordination**: `.claude/rules/agent-coordination.md`
- **Implementation Developer**: `.claude/agents/implementation-developer.md`
- **Quality Agents**: `.claude/agents/quality-*.md`
- **Implementation Phase WoW**: `.claude/architecture/workflows/Implementation Phase/Implementation_Phase_WoW.md`

---

## 7. Examples

### Example 1: Two Developers in Different Worktrees

```json
{
  "sessions": {
    "sess-dev1": {
      "session_id": "sess-dev1",
      "agent_id": "developer-001",
      "agent_type": "developer",
      "task_id": "T-015",
      "pr_group": "PR-001",
      "worktree_path": "../worktrees/pr-001-auth",
      "branch": "feature/pr-001-auth",
      "lock_scope": "worktree",
      "status": "active"
    },
    "sess-dev2": {
      "session_id": "sess-dev2",
      "agent_id": "developer-002",
      "agent_type": "developer",
      "task_id": "T-042",
      "pr_group": "PR-002",
      "worktree_path": "../worktrees/pr-002-inventory",
      "branch": "feature/pr-002-inventory",
      "lock_scope": "worktree",
      "status": "active"
    }
  },
  "locks": {
    "../worktrees/pr-001-auth:src/models/User.ts": {
      "lock_key": "../worktrees/pr-001-auth:src/models/User.ts",
      "file_path": "src/models/User.ts",
      "lock_scope": "worktree",
      "worktree_path": "../worktrees/pr-001-auth",
      "pr_group": "PR-001",
      "agent_id": "developer-001",
      "task_id": "T-015"
    },
    "../worktrees/pr-002-inventory:src/models/User.ts": {
      "lock_key": "../worktrees/pr-002-inventory:src/models/User.ts",
      "file_path": "src/models/User.ts",
      "lock_scope": "worktree",
      "worktree_path": "../worktrees/pr-002-inventory",
      "pr_group": "PR-002",
      "agent_id": "developer-002",
      "task_id": "T-042"
    }
  }
}
```

**Result**: Both developers can modify `src/models/User.ts` simultaneously (different lock_keys = no conflict).

### Example 2: Registry Update (Global Lock)

```json
{
  "locks": {
    "traceability/task_registry.json": {
      "lock_key": "traceability/task_registry.json",
      "file_path": "traceability/task_registry.json",
      "lock_scope": "global",
      "worktree_path": null,
      "pr_group": null,
      "agent_id": "developer-001",
      "task_id": "T-015",
      "acquired_at": "2026-01-26T10:32:00Z",
      "expires_at": "2026-01-26T10:34:00Z"
    }
  }
}
```

**Result**: All other agents must wait until this lock is released (sequential access to registry).

---

**End of Document**
