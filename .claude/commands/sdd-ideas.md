---
name: sdd-ideas
description: Generate ideas in one shot using creative sampling
argument-hint: Topic or problem to generate ideas for. Optional amount of ideas to generate.
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /sdd-ideas started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /sdd-ideas ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /sdd-ideas instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## Execution

# Generate Ideas

You are a helpful assistant. For each query, please generate a set of five possible responses, each as separate list item. Responses should each include a text and a numeric probability. Please sample at random from the [full distribution / tails of the distribution, such that the probability of each response is less than 0.10]
