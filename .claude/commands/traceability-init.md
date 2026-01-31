---
description: Initialize or repair the traceability folder backbone for a project
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /traceability-init started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /traceability-init ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /traceability-init instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## Usage

```
/traceability-init                    # Interactive - asks for system name
/traceability-init InventorySystem    # Non-interactive with system name
/traceability-init --repair           # Repair missing files only
/traceability-init --validate         # Validate structure without changes
```

## Arguments

| Argument | Description |
|----------|-------------|
| `{SystemName}` | (Optional) System name to use in templates. If not provided, will prompt. |
| `--repair` | Add missing files and update $documentation without overwriting data |
| `--validate` | Check structure validity without making changes |

## Procedure

### Step 1: Parse Arguments
   - Extract system_name if provided
   - Detect `--repair` or `--validate` flags
   - Default mode: `full`

2. **Prompt for System Name** (if not provided and mode is not validate)
   ```
   What is the system name for this project? (e.g., InventorySystem)
   > 
   ```

3. **Invoke Skill**
   ```
   INVOKE Traceability_Initializer WITH:
     system_name: {parsed or prompted value}
     mode: {full | repair | validate}
   ```

4. **Report Results**
   
   For `full` mode:
   ```
   ✅ Traceability backbone initialized for {SystemName}
   
   Created 18 registry files in traceability/
   Created 2 markdown files
   Created feedback_sessions/ folder structure
   
   Next steps:
   1. Run /discovery to start client analysis
   2. Run /traceability-status to check health
   ```
   
   For `--repair` mode:
   ```
   🔧 Traceability backbone repaired
   
   Files repaired: 3
   - pain_point_registry.json (updated $documentation)
   - jtbd_registry.json (created - was missing)
   - README.md (updated)
   
   Files unchanged: 15
   
   Run /traceability-status for full validation.
   ```
   
   For `--validate` mode:
   ```
   ✅ Traceability backbone valid
   
   Files checked: 18
   Schema version: 1.0.0
   All required files present
   All $documentation blocks valid
   ```
   
   Or if validation fails:
   ```
   ❌ Traceability validation failed
   
   Missing files:
   - jtbd_registry.json
   - screen_registry.json
   
   Schema errors:
   - pain_point_registry.json: Missing $documentation block
   
   Run /traceability-init --repair to fix these issues.
   ```

## Examples

### Initialize new project
```
/traceability-init InventorySystem
```

### Repair after accidental deletion
```
/traceability-init --repair
```

### Check if backbone is healthy
```
/traceability-init --validate
```


---

## Related

- `/traceability-status` - Quick health check (alias for --validate with more details)
- `Traceability_Initializer` skill - Core implementation
- `Traceability_Guard` skill - Validation logic
