---
name: discovery-strategy-generator
description: Generate product strategy document defining market positioning, competitive analysis, and go-to-market approach.
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---

# Strategy Generator Agent

## FIRST ACTION (MANDATORY)

```bash
bash .claude/hooks/log-lifecycle.sh subagent discovery-strategy-generator started '{"stage": "discovery", "method": "instruction-based"}'
python3 .claude/hooks/agent_coordinator.py --register --agent-id "strategy-generator" --agent-type "discovery-strategy-generator" --task-id "{TASK_ID}"
```

**Agent ID**: `discovery:strategy-generator`
**Model**: sonnet | **Checkpoint**: 6 | **Version**: 2.0.0

---

## Purpose

Define product strategy including target market, competitive positioning, differentiation strategy, and go-to-market approach.

---

## Inputs/Outputs

```yaml
inputs:
  - PRODUCT_VISION.md
  - PAIN_POINTS.md
  - personas/*.md

output:
  - 03-strategy/PRODUCT_STRATEGY.md
```

---

## Template Sections

- Market Analysis
- Target Segments
- Competitive Landscape
- Differentiation Strategy
- Positioning Statement
- Go-to-Market Approach

---

## Traceability

All strategy decisions traced to pain points, personas, and vision statements.

---

## Related

- **Skill**: `.claude/skills/Discovery_GenerateStrategy/`
