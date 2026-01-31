# Claude Code Component Lifecycle Logging Reference



## Quick Reference Table

| Component | Start Detection | End Detection | Deterministic? | Notes |
|-----------|-----------------|---------------|----------------|-------|
| **Slash Commands** | `PreToolUse` hook (first tool, `once: true`) | `Stop` hook in frontmatter | Partial/Yes | Start requires tool usage to trigger |
| **Skills** | `PreToolUse` hook (first tool, `once: true`) | `Stop` hook in frontmatter | Partial/Yes | Start requires tool usage to trigger |
| **Subagents** | `PreToolUse` hook (first tool, `once: true`) | `SubagentStop` hook | Partial/Yes | Use `SubagentStop` not `Stop` |
| **Agents (Task tool)** | Parent's `PreToolUse` matcher on `Task` | `SubagentStop` hook | Yes/Yes | Task tool invocation is detectable |
| **Settings-based Hooks** | N/A (they ARE the events) | N/A | Yes | Define in `.claude/settings.json` |

---

## Detailed Implementation by Component

### 1. Slash Commands (`/.claude/commands/*.md`)

```yaml
---
name: my-command
description: Does something useful
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: |
            echo '{"component": "command", "name": "my-command", "event": "started", "timestamp": "'$(date -Iseconds)'"}' >> "$CLAUDE_PROJECT_DIR/.claude/lifecycle.json"
  Stop:
    - hooks:
        - type: command
          command: |
            echo '{"component": "command", "name": "my-command", "event": "ended", "timestamp": "'$(date -Iseconds)'"}' >> "$CLAUDE_PROJECT_DIR/.claude/lifecycle.json"
---

Your command instructions here...
```

**Limitations:**
- `PreToolUse` only fires when Claude uses a tool — if your command doesn't trigger tools, start won't log
- No native `CommandStart` event exists

**Alternative Start Detection (Instruction-based):**
```markdown
---
name: my-command
description: Does something useful
hooks:
  Stop:
    - hooks:
        - type: command
          command: ./scripts/log-end.sh my-command
---

## FIRST ACTION (MANDATORY)
Before doing anything else, run this exact command:
```bash
echo '{"component": "command", "name": "my-command", "event": "started", "timestamp": "'$(date -Iseconds)'"}' >> .claude/lifecycle.json
```

Then proceed with the actual task...
```

---

### 2. Skills (`/.claude/skills/*.md` or `CLAUDE.md` skills)

```yaml
---
name: database-migration
description: Handles database migrations safely
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: |
            echo '{"component": "skill", "name": "database-migration", "event": "started", "timestamp": "'$(date -Iseconds)'", "session": "'$CLAUDE_SESSION_ID'"}' >> "$CLAUDE_PROJECT_DIR/.claude/lifecycle.json"
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: |
            # Optional: log each tool execution within the skill
            echo '{"component": "skill", "name": "database-migration", "event": "tool_used", "tool": "Bash", "timestamp": "'$(date -Iseconds)'"}' >> "$CLAUDE_PROJECT_DIR/.claude/lifecycle.json"
  Stop:
    - hooks:
        - type: command
          command: |
            echo '{"component": "skill", "name": "database-migration", "event": "ended", "timestamp": "'$(date -Iseconds)'"}' >> "$CLAUDE_PROJECT_DIR/.claude/lifecycle.json"
---

Skill instructions here...
```

**Available Hook Options for Skills:**
| Option | Type | Description |
|--------|------|-------------|
| `matcher` | string | Tool pattern: `"Bash"`, `"Edit\|Write"`, `"*"` |
| `once` | boolean | Run only once per session (Skills/Commands only) |
| `type` | string | `"command"` or `"prompt"` |
| `command` | string | Bash command to execute |
| `timeout` | number | Seconds before hook is cancelled |

---

### 3. Subagents (Task Tool Spawned Agents)

Subagents are spawned via the `Task` tool. They have their own lifecycle.

**In the subagent definition:**
```yaml
---
name: code-reviewer
description: Reviews code changes
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: |
            echo '{"component": "subagent", "name": "code-reviewer", "event": "started", "timestamp": "'$(date -Iseconds)'"}' >> "$CLAUDE_PROJECT_DIR/.claude/lifecycle.json"
  SubagentStop:
    - hooks:
        - type: command
          command: |
            echo '{"component": "subagent", "name": "code-reviewer", "event": "ended", "timestamp": "'$(date -Iseconds)'"}' >> "$CLAUDE_PROJECT_DIR/.claude/lifecycle.json"
---

Review instructions...
```

**IMPORTANT:** Use `SubagentStop`, not `Stop` for subagents!

---

### 4. Detecting Agent/Subagent Spawning from Parent

To log when the parent agent spawns a subagent (Task tool), use settings-based hooks:

**`.claude/settings.json`:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Task",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"event\": \"subagent_spawned\", \"timestamp\": \"'$(date -Iseconds)'\", \"input\": '\"$CLAUDE_TOOL_INPUT\"'}' >> \"$CLAUDE_PROJECT_DIR/.claude/lifecycle.json\""
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"event\": \"subagent_completed\", \"timestamp\": \"'$(date -Iseconds)'\"}' >> \"$CLAUDE_PROJECT_DIR/.claude/lifecycle.json\""
          }
        ]
      }
    ]
  }
}
```

---

### 5. Global Session Logging (Settings-Based)

For logging all activity regardless of which component is active:

**`.claude/settings.json`:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"event\": \"session_started\", \"source\": \"'$CLAUDE_SESSION_SOURCE'\", \"timestamp\": \"'$(date -Iseconds)'\"}' >> \"$CLAUDE_PROJECT_DIR/.claude/lifecycle.json\""
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"event\": \"prompt_submitted\", \"timestamp\": \"'$(date -Iseconds)'\"}' >> \"$CLAUDE_PROJECT_DIR/.claude/lifecycle.json\""
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"event\": \"tool_pre\", \"tool\": \"'$CLAUDE_TOOL_NAME'\", \"timestamp\": \"'$(date -Iseconds)'\"}' >> \"$CLAUDE_PROJECT_DIR/.claude/lifecycle.json\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"event\": \"tool_post\", \"tool\": \"'$CLAUDE_TOOL_NAME'\", \"timestamp\": \"'$(date -Iseconds)'\"}' >> \"$CLAUDE_PROJECT_DIR/.claude/lifecycle.json\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"event\": \"agent_stopped\", \"timestamp\": \"'$(date -Iseconds)'\"}' >> \"$CLAUDE_PROJECT_DIR/.claude/lifecycle.json\""
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"event\": \"subagent_stopped\", \"timestamp\": \"'$(date -Iseconds)'\"}' >> \"$CLAUDE_PROJECT_DIR/.claude/lifecycle.json\""
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"event\": \"pre_compact\", \"timestamp\": \"'$(date -Iseconds)'\"}' >> \"$CLAUDE_PROJECT_DIR/.claude/lifecycle.json\""
          }
        ]
      }
    ]
  }
}
```

---

## Available Environment Variables

| Variable | Description | Available In |
|----------|-------------|--------------|
| `CLAUDE_PROJECT_DIR` | Project root directory | All hooks |
| `CLAUDE_SESSION_ID` | Current session identifier | All hooks |
| `CLAUDE_TOOL_NAME` | Name of tool being used | PreToolUse, PostToolUse |
| `CLAUDE_TOOL_INPUT` | JSON input to tool | PreToolUse, PostToolUse |
| `CLAUDE_TOOL_OUTPUT` | JSON output from tool | PostToolUse only |
| `CLAUDE_SESSION_SOURCE` | `"startup"`, `"resume"`, `"clear"` | SessionStart |
| `CLAUDE_CODE_REMOTE` | `"true"` if web environment | All hooks |

---

## Available Hook Events

| Event | Fires When | Supports Matcher | Frontmatter Support |
|-------|------------|------------------|---------------------|
| `SessionStart` | Session starts/resumes | No | No |
| `UserPromptSubmit` | User submits prompt | No | No |
| `PreToolUse` | Before tool execution | Yes | Yes |
| `PostToolUse` | After tool completion | Yes | Yes |
| `PermissionRequest` | Tool requests permission | Yes | No |
| `Stop` | Agent finishes responding | No | Yes |
| `SubagentStop` | Subagent finishes | No | Yes |
| `PreCompact` | Before context compaction | No | No |

---

## Logging Script Helper

Create a reusable logging script at `.claude/hooks/log-lifecycle.sh`:

```bash
#!/bin/bash
# Usage: log-lifecycle.sh <component_type> <component_name> <event>
# Example: log-lifecycle.sh skill database-migration started

COMPONENT_TYPE="$1"
COMPONENT_NAME="$2"
EVENT="$3"
LOG_FILE="${CLAUDE_PROJECT_DIR:-.}/.claude/lifecycle.json"

# Ensure directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Create JSON entry
cat >> "$LOG_FILE" << EOF
{"component": "$COMPONENT_TYPE", "name": "$COMPONENT_NAME", "event": "$EVENT", "timestamp": "$(date -Iseconds)", "session": "${CLAUDE_SESSION_ID:-unknown}"}
EOF
```

Make it executable:
```bash
chmod +x .claude/hooks/log-lifecycle.sh
```

Then use in frontmatter:
```yaml
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh skill my-skill started"
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh skill my-skill ended"
```

---

## Known Limitations & Workarounds

| Limitation | Impact | Workaround |
|------------|--------|------------|
| No `SkillStart`/`CommandStart` event | Can't deterministically log activation | Use `PreToolUse` with `once: true` or instruction-based |
| `PreToolUse`/`PostToolUse` may not fire | Reported bug (GitHub #6305) | Use `Stop`/`SubagentStop` which work reliably |
| Frontmatter hooks only run when component active | Won't log if component not invoked | Use settings-based hooks for global logging |
| No access to component name in env vars | Can't dynamically identify which skill | Hardcode name in each component's hooks |

---

## Recommended Architecture

For comprehensive observability:

1. **Global hooks** in `.claude/settings.json` for session-level events
2. **Component-specific hooks** in frontmatter for skill/command-specific logging
3. **Centralized log file** at `.claude/lifecycle.json`
4. **Helper script** for consistent JSON formatting

