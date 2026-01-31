---
description: Sets up code formatting rules and style guidelines in CLAUDE.md
argument-hint: None required - creates standard formatting configuration
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /ddd-setup-formatting started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /ddd-setup-formatting ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /ddd-setup-formatting instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## Execution

# Setup Architecture Memory

Create or update CLAUDE.md in with following content, <critical>write it strictly as it is<critical>, do not summaraise or introduce and new additional information:

```markdown
## Code Style Rules

### Code Formatting

- No semicolons (enforced)
- Single quotes (enforced)
- No unnecessary curly braces (enforced)
- 2-space indentation
- Import order: external → internal → types
```
