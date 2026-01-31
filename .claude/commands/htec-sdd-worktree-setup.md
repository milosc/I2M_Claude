---
description: Execute worktree setup script for parallel PR development
argument-hint: <SystemName> [--base <branch>]
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-worktree-setup started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-worktree-setup ended '{"stage": "implementation"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "implementation"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /htec-sdd-worktree-setup instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

## Usage

```
/htec-sdd-worktree-setup <SystemName>
/htec-sdd-worktree-setup <SystemName> --base develop
/htec-sdd-worktree-setup <SystemName> --base main --clean
```

## Arguments

- `SystemName`: Name of the system (e.g., InventorySystem)

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--base <branch>` | Base branch for worktrees | main |
| `--clean` | Remove existing worktrees first | false |
| `--dry-run` | Show what would be created | false |

## Prerequisites

- `/htec-sdd-tasks` completed (with PR groups generated)
- Clean git working directory (no uncommitted changes)
- Generated setup script exists

## Procedure

### 1. Validate Prerequisites

```bash
# Check that task decomposition is complete
IF NOT EXISTS traceability/task_registry.json:
    ERROR "Task registry not found. Run /htec-sdd-tasks first."
    EXIT

# Verify PR groups exist in registry
READ traceability/task_registry.json
IF pr_groups is empty:
    ERROR "No PR groups found. Run /htec-sdd-tasks to generate."
    EXIT

# Check for generated setup script
SCRIPT_PATH="Implementation_${SystemName}/scripts/setup-worktrees.sh"
IF NOT EXISTS $SCRIPT_PATH:
    ERROR "Setup script not found at $SCRIPT_PATH"
    ERROR "Run /htec-sdd-tasks to generate PR groups and scripts."
    EXIT

LOG "✓ Prerequisites validated"
```

### 2. Check Git Status

```bash
# Ensure clean working directory
GIT_STATUS=$(git status --porcelain)

IF GIT_STATUS is not empty:
    ERROR "Working directory has uncommitted changes:"
    SHOW git status
    ERROR "Commit or stash changes before creating worktrees."
    EXIT

# Verify we're in a git repository
IF NOT git rev-parse --git-dir:
    ERROR "Not in a git repository."
    EXIT

# Check that base branch exists
BASE_BRANCH="${--base:-main}"
IF NOT git rev-parse --verify "$BASE_BRANCH":
    ERROR "Base branch '$BASE_BRANCH' does not exist."
    EXIT

LOG "✓ Git status clean"
LOG "✓ Base branch: $BASE_BRANCH"
```

### 3. Clean Existing Worktrees (--clean)

```bash
IF --clean:
    LOG "Cleaning existing worktrees..."

    # List existing worktrees
    WORKTREES=$(git worktree list --porcelain | grep "worktree " | cut -d' ' -f2)

    FOR EACH worktree IN WORKTREES:
        IF worktree matches "../worktrees/pr-*":
            LOG "Removing worktree: $worktree"
            git worktree remove "$worktree" --force

    # Remove worktrees directory if empty
    IF EXISTS "../worktrees" AND is_empty:
        rmdir "../worktrees"

    LOG "✓ Cleanup complete"
```

### 4. Dry Run (--dry-run)

```bash
IF --dry-run:
    LOG "Dry run: Would execute the following:"
    LOG ""
    cat "$SCRIPT_PATH"
    LOG ""
    LOG "To execute: /htec-sdd-worktree-setup $SystemName"
    EXIT
```

### 5. Execute Setup Script

```bash
# Make script executable if not already
chmod +x "$SCRIPT_PATH"

# Execute with base branch parameter
LOG "Executing worktree setup..."
LOG "Script: $SCRIPT_PATH"
LOG "Base branch: $BASE_BRANCH"
LOG ""

bash "$SCRIPT_PATH" "$BASE_BRANCH"

# Check exit code
IF exit_code != 0:
    ERROR "Worktree setup failed with exit code $exit_code"
    ERROR "Check the script and try again."
    EXIT

LOG ""
LOG "✓ Worktree setup complete"
```

### 6. Verify Worktrees Created

```bash
# List all worktrees
WORKTREE_LIST=$(git worktree list)
WORKTREE_COUNT=$(echo "$WORKTREE_LIST" | grep -c "../worktrees/pr-")

LOG ""
LOG "Worktrees created: $WORKTREE_COUNT"
LOG ""
git worktree list
LOG ""
```

### 7. Generate Usage Instructions

```bash
# Read PR groups from registry
READ traceability/task_registry.json
PR_GROUPS = registry.pr_groups

LOG "PR Groups Available:"
LOG ""

FOR EACH pr_group IN PR_GROUPS:
    LOG "  ${pr_group.id}: ${pr_group.title}"
    LOG "    Worktree: ${pr_group.worktree_path}"
    LOG "    Branch: ${pr_group.branch}"
    LOG "    Tasks: ${pr_group.tasks.length}"
    LOG ""

LOG "Next Steps:"
LOG ""
LOG "  1. Navigate to a worktree:"
LOG "     cd ${PR_GROUPS[0].worktree_path}"
LOG ""
LOG "  2. Start implementation (auto-detects PR group):"
LOG "     /htec-sdd-implement $SystemName"
LOG ""
LOG "  3. Or specify PR group explicitly:"
LOG "     /htec-sdd-implement $SystemName --pr-group ${PR_GROUPS[0].id}"
LOG ""
```

## Output

### Successful Execution

```
Worktree Setup: InventorySystem
═══════════════════════════════════════

✓ Prerequisites validated
✓ Git status clean
✓ Base branch: main

Executing worktree setup...
Script: Implementation_InventorySystem/scripts/setup-worktrees.sh
Base branch: main

Creating worktree: pr-001-auth
Creating worktree: pr-002-inventory
Creating worktree: pr-003-reports
Creating worktree: pr-004-settings

✓ Worktree setup complete

Worktrees created: 4

worktree /Users/user/project                     abc1234 [main]
worktree /Users/user/worktrees/pr-001-auth      def5678 [feature/pr-001-auth]
worktree /Users/user/worktrees/pr-002-inventory ghi9012 [feature/pr-002-inventory]
worktree /Users/user/worktrees/pr-003-reports   jkl3456 [feature/pr-003-reports]
worktree /Users/user/worktrees/pr-004-settings  mno7890 [feature/pr-004-settings]

PR Groups Available:

  PR-001: User Authentication System
    Worktree: ../worktrees/pr-001-auth
    Branch: feature/pr-001-auth
    Tasks: 3

  PR-002: Inventory Management
    Worktree: ../worktrees/pr-002-inventory
    Branch: feature/pr-002-inventory
    Tasks: 8

  PR-003: Reports Dashboard
    Worktree: ../worktrees/pr-003-reports
    Branch: feature/pr-003-reports
    Tasks: 5

  PR-004: Settings & Configuration
    Worktree: ../worktrees/pr-004-settings
    Branch: feature/pr-004-settings
    Tasks: 4

Next Steps:

  1. Navigate to a worktree:
     cd ../worktrees/pr-001-auth

  2. Start implementation (auto-detects PR group):
     /htec-sdd-implement InventorySystem

  3. Or specify PR group explicitly:
     /htec-sdd-implement InventorySystem --pr-group PR-001
```

### Error: No Script Found

```
❌ Setup script not found at Implementation_InventorySystem/scripts/setup-worktrees.sh

Run /htec-sdd-tasks to generate PR groups and scripts.
```

### Error: Uncommitted Changes

```
❌ Working directory has uncommitted changes:

 M .claude/commands/htec-sdd-tasks.md
 M .claude/commands/htec-sdd-implement.md

Commit or stash changes before creating worktrees.
```

### Error: PR Groups Not Generated

```
❌ No PR groups found in task registry.

Run /htec-sdd-tasks to generate PR groups and worktree scripts.
```

## Files Modified

- None (creates worktrees only, no file modifications)

## State Changes

- Git worktrees created in `../worktrees/` directory
- New branches created for each PR group
- Working directories initialized for each worktree

## Cleanup

To remove worktrees after PR completion:

```bash
# Remove specific worktree
git worktree remove ../worktrees/pr-001-auth

# Or use --clean flag to remove all
/htec-sdd-worktree-setup InventorySystem --clean

# Clean up branches after merge
git branch -d feature/pr-001-auth
```

---

## Related Commands

- `/htec-sdd-tasks` - Generate PR groups and setup script (prerequisite)
- `/htec-sdd-implement` - Start implementation in worktree
- `/htec-sdd-status` - View implementation progress across worktrees
