---
name: htec-sdd-status
description: Display Implementation stage status and progress
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-status started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-status ended '{"stage": "implementation"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "implementation"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /htec-sdd-status instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Implementation stage rules:

```bash
# Load TDD and quality gate rules
/rules-process-integrity

# Load multi-agent coordination rules (if spawning agents)
/rules-agent-coordination

# Load Traceability rules for task IDs
/rules-traceability
```

## Usage

```
/htec-sdd-status
/htec-sdd-status <SystemName>
/htec-sdd-status --verbose
```

## Arguments

- `SystemName`: Optional. If not provided, reads from active config.

## Options

| Option | Description |
|--------|-------------|
| `--verbose` | Show detailed task breakdown |
| `--tasks` | Show task list only |
| `--metrics` | Show metrics only |

## Procedure

### 1. Load Status Data

```
READ _state/implementation_config.json
READ _state/implementation_progress.json
READ traceability/task_registry.json

CALCULATE:
    - Tasks by status
    - Tasks by priority
    - Test coverage
    - Review status
    - Blocking issues
```

## Output

### Standard Output

```
Implementation Status: InventorySystem
═══════════════════════════════════════
Current Checkpoint: 5 (P0 Tasks Complete)
Started: 2024-01-15
Last Activity: 2024-01-17 14:32

Progress: 67% ████████████████░░░░░░░░ (32/47 tasks)

Tasks by Status:
  ✓ Completed:   32
  ◐ In Progress:  2
  ○ Pending:     13
  ✗ Blocked:      0

Tasks by Phase:
  Phase 3 (Infrastructure): 8/8   ✓ Complete
  Phase 4 (Features):      22/31  ◐ In Progress
  Phase 5 (Integration):    2/8   ○ Pending

Tasks by Priority:
  P0: 23/23 ✓ Complete
  P1: 9/16  ◐ In Progress
  P2: 0/8   ○ Pending

Metrics:
  Test Coverage: 84%
  Tests: 198 passing, 0 failing
  Files: 67 created, 12 modified

Review Status: Pending (not started)

Next Steps:
  1. Continue with /htec-sdd-implement
  2. After tasks complete, run /htec-sdd-review
```

### Verbose Output (--verbose)

```
Implementation Status: InventorySystem (Verbose)
═══════════════════════════════════════

... [standard output above] ...

Recent Tasks:
  ✓ T-032 Inventory list pagination    [12m ago]
  ✓ T-031 Inventory search component   [25m ago]
  ◐ T-033 Inventory filters            [in progress]
  ◐ T-034 Export functionality         [in progress]

Blocked Tasks: None

Upcoming Tasks (next 5):
  ○ T-035 Inventory detail view        [depends: T-033]
  ○ T-036 Edit inventory item          [depends: T-035]
  ○ T-037 Delete confirmation modal    [depends: T-035]
  ○ T-038 Bulk operations              [depends: T-033, T-034]
  ○ T-039 Inventory history view       [depends: T-035]

Traceability:
  Pain Points covered: 12/12 (100%)
  Requirements traced: 47/47 (100%)
  Screens implemented: 8/12 (67%)
```

### Tasks Only (--tasks)

```
Implementation Tasks: InventorySystem
═══════════════════════════════════════

Phase 3 (Infrastructure) - Complete
  ✓ T-001 Setup project structure
  ✓ T-002 Configure TypeScript
  ✓ T-003 Setup Vitest
  ✓ T-004 Configure Tailwind
  ✓ T-005 Setup API client
  ✓ T-006 Configure state management
  ✓ T-007 Setup routing
  ✓ T-008 Error boundary setup

Phase 4 (Features) - In Progress
  ✓ T-010 Barcode scanner types
  ✓ T-011 Barcode scanner service
  ...
  ◐ T-033 Inventory filters
  ◐ T-034 Export functionality
  ○ T-035 Inventory detail view
  ...

Phase 5 (Integration) - Pending
  ○ T-040 E2E: Login flow
  ○ T-041 E2E: Inventory CRUD
  ...
```


---

## Related Commands

- `/htec-sdd-implement` - Continue implementation
- `/htec-sdd-reset` - Reset progress
- `/htec-sdd-resume` - Resume from checkpoint
