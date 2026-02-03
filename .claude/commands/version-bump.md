---
name: version-bump
description: Increment framework version (major, minor, or patch)
argument-hint: major|minor|patch
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /version-bump started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /version-bump ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /version-bump instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## Arguments

- `$type` - Required: `major` or `minor`
- `$value` - Optional: Explicit value to set. If omitted, increments the current value by 1.

## Prerequisites

- `.claude/version.json` must exist.

## Skills Used

- `.claude/skills/VERSION_CONTROL_STANDARD.md`

## Execution Steps

### Step 1: Read Current State
   - Load `.claude/version.json`.

2. **Determine New Values**
   - If `$type` is `major`:
     - New `major` = `$value` OR `current_major + 1`.
     - New `minor` = 0.
   - If `$type` is `minor`:
     - New `minor` = `$value` OR `current_minor + 1`.

3. **Update Registry**
   - Write new `major` and `minor` values back to `.claude/version.json`.

4. **User Confirmation**
   - Display the updated state: `Major: X, Minor: Y`.
   - Explain that the next file modification will start at `X.Y.0`.


## Outputs

- Updated `.claude/version.json`
