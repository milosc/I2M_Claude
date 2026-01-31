---
name: managing-framework-migration
description: Use when you need to handle framework version upgrades, migrate state files, or manage breaking changes with full validation and backup.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill managing-framework-migration started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill managing-framework-migration ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill managing-framework-migration instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

# Migration Manager

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_Migrate
- **Version**: 2.3.1
- **Created**: 2024-12-13
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3

## Description
Handle version migrations for the Prototype Skills Framework. Ensures smooth transitions when framework structure changes.

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

Handle version migrations for the Prototype Skills Framework. Ensures smooth transitions when framework structure changes.

## Execution Logging (MANDATORY)

This skill logs all execution to the global pipeline progress registry. Logging is automatic and requires no manual configuration.

### How Logging Works

Every execution of this skill is logged to `_state/lifecycle.json`:

- **start_event**: Logged when skill execution begins
- **end_event**: Logged when skill execution completes

Events include:
- skill_name, intent, stage, system_name
- start/end timestamps
- status (completed/failed)
- output files created (migration reports)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "managing-framework-migration"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "managing-framework-migration" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ _state/progress.json if exists
EXTRACT schema_version (default: "1.0" if missing)

CURRENT_VERSION = "2.3"  // This version with full validation

IF schema_version == CURRENT_VERSION:
  LOG: "Already at current version {CURRENT_VERSION}"
  
  ═══════════════════════════════════════════
  ℹ️ NO MIGRATION NEEDED
  ═══════════════════════════════════════════
  
  Current version: {schema_version}
  Target version: {CURRENT_VERSION}
  
  How would you like to proceed?
  1. "continue" - Exit migration
  2. "force" - Re-run migrations anyway
  3. "validate" - Check state file integrity
  ═══════════════════════════════════════════
  
  WAIT for user response

LOG: "Migration needed: {schema_version} → {CURRENT_VERSION}"
```

### Step 2: Create Backup (REQUIRED)
```
CREATE backup directory: _state/backups/pre-migration-{timestamp}/

COPY all state files to backup:
  - progress.json
  - requirements_registry.json
  - discovery_summary.json
  - sequence.json
  - codegen_state.json
  - qa_results.json

IF backup fails:
  ═══════════════════════════════════════════
  ⚠️ BACKUP FAILED
  ═══════════════════════════════════════════
  
  Cannot create backup before migration.
  Error: {error_message}
  
  How would you like to proceed?
  1. "retry backup" - Try again
  2. "skip backup" - Continue without (RISKY)
  3. "abort" - Stop migration
  ═══════════════════════════════════════════
  
  WAIT for user response

LOG: "Backup created at {backup_path}"
```

### Step 3: Determine Migration Path
```
BUILD migration_path based on schema_version:
  1.0 → 2.0: Add requirements_registry
  2.0 → 2.1: Add progress tracking to all skills
  2.1 → 2.2: Add requirements traceability
  2.2 → 2.3: Add validation steps to all skills

LOG: "Migration path: {migration_steps}"
```

### Step 4: Execute Migrations with Validation
```
FOR each migration in path:
  LOG: "Executing migration: {from} → {to}"
  
  EXECUTE migration transforms
  
  VALIDATE migration result:
    IF validation fails:
      ═══════════════════════════════════════════
      ⚠️ MIGRATION STEP FAILED
      ═══════════════════════════════════════════
      
      Migration {from} → {to} failed validation.
      
      Errors:
      • [list specific errors]
      
      How would you like to proceed?
      1. "retry" - Re-run this migration
      2. "rollback" - Restore from backup
      3. "fix: [issue]" - Manual fix, then continue
      4. "skip" - Skip this migration (may break things)
      ═══════════════════════════════════════════
      
      WAIT for user response
  
  UPDATE schema_version after each successful step
```

### Step 5: Migration 1.0 → 2.0 (Requirements Registry)
```
IF migrating from 1.0:
  CREATE _state/requirements_registry.json if missing
  
  IF discovery_summary.json exists:
    EXTRACT pain_points → generate PP-XXX
    GENERATE baseline A11Y-001 through A11Y-006
    
  VALIDATE:
    - File is valid JSON
    - Has requirements array
    - Has summary object
```

### Step 6: Migration 2.0 → 2.1 (Progress Tracking)
```
IF migrating from 2.0:
  UPDATE progress.json structure:
    FOR each phase that exists:
      IF missing metrics: ADD empty metrics object
      IF missing outputs: ADD empty outputs array
      IF missing validation: ADD validation object
      
  VALIDATE:
    - All phases have required fields
```

### Step 7: Migration 2.1 → 2.2 (Requirements Traceability)
```
IF migrating from 2.1:
  FOR each component spec in outputs/02-components/:
    IF missing "Requirements Addressed" section:
      ADD empty section with TODO marker
      LOG WARNING: "{file} needs requirements"
      
  FOR each screen spec in outputs/03-screens/:
    IF missing "Requirements Addressed" section:
      ADD empty section with TODO marker
      LOG WARNING: "{file} needs requirements"
      
  UPDATE requirements_registry.json:
    FOR each requirement:
      IF missing addressed_by: ADD empty array
      
  VALIDATE:
    - All specs have section (even if empty)
    - Registry has addressed_by arrays
```

### Step 8: Migration 2.2 → 2.3 (Validation Steps)
```
IF migrating from 2.2:
  UPDATE progress.json:
    FOR each phase:
      IF missing validation object:
        ADD: { status: "unknown", checks_run: 0, checks_passed: 0 }
        
  LOG: "Added validation tracking to all phases"
  
  VALIDATE:
    - All phases have validation object
```

### Step 9: Final Validation (REQUIRED)
```
VALIDATE all state files:
  CHECKS:
    - progress.json: schema_version == CURRENT_VERSION
    - progress.json: all phases have required fields
    - requirements_registry.json: valid structure
    - All specs have Requirements Addressed section
    
IF any validation fails:
  ═══════════════════════════════════════════
  ⚠️ POST-MIGRATION VALIDATION FAILED
  ═══════════════════════════════════════════
  
  Migration completed but validation failed:
  • [list specific failures]
  
  How would you like to proceed?
  1. "fix: [issue]" - Address specific issue
  2. "rollback" - Restore from backup
  3. "accept" - Accept with warnings
  ═══════════════════════════════════════════
  
  WAIT for user response
```

### Step 10: Generate Migration Log & Update Progress
```
WRITE _state/migration_log.md

UPDATE _state/progress.json:
  schema_version = CURRENT_VERSION
  phases.migrate.status = "complete"
  phases.migrate.completed_at = timestamp
  phases.migrate.outputs = ["migration_log.md"]
  phases.migrate.validation = {
    status: "passed",
    from_version: original,
    to_version: CURRENT_VERSION,
    steps_completed: count
  }
  phases.migrate.metrics = {
    migrations_applied: count,
    files_updated: count,
    warnings: count
  }
```

---

## Input Requirements

| Input | Required | Used For |
|-------|----------|----------|
| progress.json | ⚠️ Optional | Version detection |
| State files | ⚠️ Optional | Migration targets |

---

## Validation at Each Stage

| Stage | Validation | Blocking? |
|-------|------------|-----------|
| Backup | Successfully created | ✅ Yes |
| Each migration | Step completed correctly | ✅ Yes |
| Post-migration | All files valid | ⚠️ Can accept with warnings |

---

## User Mitigation Options

| Response | Action |
|----------|--------|
| `continue` | Exit if no migration needed |
| `force` | Re-run migrations |
| `validate` | Check integrity only |
| `retry backup` | Retry backup creation |
| `skip backup` | Continue without backup |
| `retry` | Re-run failed migration |
| `rollback` | Restore from backup |
| `fix: [issue]` | Manual fix |
| `skip` | Skip migration step |
| `accept` | Accept with warnings |
| `abort` | Stop migration |

---

## Migration Log Template

```markdown
# Migration Log

## Summary
- **From Version**: 2.0
- **To Version**: 2.3
- **Executed At**: 2024-12-13T10:00:00Z
- **Status**: Success

## Migrations Applied

### 2.0 → 2.1: Progress Tracking
- Added metrics to 12 phase entries
- Validation: ✅ Passed

### 2.1 → 2.2: Requirements Traceability
- Updated 18 component specs
- Updated 12 screen specs
- Validation: ✅ Passed

### 2.2 → 2.3: Validation Steps
- Added validation objects to all phases
- Validation: ✅ Passed

## Warnings
- Button.md: Requirements section empty (needs manual review)

## Backup Location
_state/backups/pre-migration-2024-12-13T10-00-00/
```

---

## Progress.json Update

```json
{
  "schema_version": "2.3",
  "phases": {
    "migrate": {
      "status": "complete",
      "completed_at": "2024-12-13T10:00:00Z",
      "outputs": ["_state/migration_log.md"],
      "validation": {
        "status": "passed",
        "from_version": "2.0",
        "to_version": "2.3",
        "steps_completed": 3
      },
      "metrics": {
        "migrations_applied": 3,
        "files_updated": 32,
        "warnings": 1
      }
    }
  }
}
```
