---
description: Test the execution logging framework by triggering start/end hooks and verifying lifecycle.json
argument-hint: None required - runs self-test automatically
model: claude-haiku-4-5-20250515
allowed-tools: Read, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /test-logging started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /test-logging ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /test-logging instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## Execution

# /test-logging - Framework Logging Test

This command tests the execution logging framework by:
```

### Step 2: Verify Logging Hooks Exist

```bash
# Check required hooks
HOOKS_OK=true

# Legacy hooks no longer used - checking for new log-lifecycle.sh instead
if [ -f ".claude/hooks/log-lifecycle.sh" ]; then
  echo "✅ log-lifecycle.sh exists"
else
  echo "❌ log-lifecycle.sh missing"
fi

if [ "$HOOKS_OK" = true ]; then
  echo ""
  echo "✅ All logging hooks present"
else
  echo ""
  echo "❌ Some hooks missing - framework may not work correctly"
fi
```

### Step 3: Check Pipeline Progress Before

```bash
# Capture current stats
echo ""
echo "📊 Current Pipeline Progress Stats:"
echo "===================================="

if [ -f  ]; then
  # Extract current counts
  COMMANDS_BEFORE=$(python3 -c "import json; f=open(); d=json.load(f); print(d.get('statistics', {}).get('total_commands', 0))")
  SKILLS_BEFORE=$(python3 -c "import json; f=open(); d=json.load(f); print(d.get('statistics', {}).get('total_skills_invoked', 0))")

  echo "Commands logged: $COMMANDS_BEFORE"
  echo "Skills invoked: $SKILLS_BEFORE"

  # Show last 3 events
  echo ""
  echo "📋 Last 3 Events:"
  python3 -c "
import json
with open() as f:
    d = json.load(f)
events = d.get('events', [])[-3:]
for e in events:
    print(f\"  - {e.get('timestamp', 'N/A')[:19]} | {e.get('event_type', 'N/A')} | {e.get('command_name', e.get('skill_name', 'N/A'))}\")"
else
  echo "⚠️ lifecycle.json does not exist yet"
  echo "   This is normal for first run - it will be created"
  COMMANDS_BEFORE=0
  SKILLS_BEFORE=0
fi
```

### Step 4: Test Skill Invoke Hook (Optional)

```bash
```

## Expected Output

```
📝 Logged command start: evt-xxxxxxxx
✅ _state directory exists
| Permission denied | Python not executable | Check `.venv` or system Python |
| JSON decode error | Corrupted state file | Delete `_state/lifecycle.json` |
| Count not increasing | Hook returning error | Check Python error output |

## Related

- **Pipeline Progress**: `_state/lifecycle.json`