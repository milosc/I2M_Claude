---
name: discovery-navigation-specifier
description: Define navigation structure, menu hierarchy, and routing patterns for the application.
model: sonnet
skills:
  required:
    - Discovery_SpecNavigation
  optional:
    - hicks-law
    - progressive-disclosure
    - graph-thinking
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

# Navigation Specifier Agent

## FIRST ACTION (MANDATORY)

```bash
bash .claude/hooks/log-lifecycle.sh subagent discovery-navigation-specifier started '{"stage": "discovery", "method": "instruction-based"}'
python3 .claude/hooks/agent_coordinator.py --register --agent-id "navigation-specifier" --agent-type "discovery-navigation-specifier" --task-id "{TASK_ID}"
```

**Agent ID**: `discovery:navigation-specifier`
**Model**: sonnet | **Checkpoint**: 9 | **Version**: 2.0.0

---

## Purpose

Define navigation structure, menu hierarchy, breadcrumbs, and routing patterns based on screen definitions.

---

## Inputs/Outputs

```yaml
inputs:
  - screen-definitions.md (Screen IDs and flows)
  - personas/*.md (navigation preferences)

output:
  - 04-design-specs/navigation-structure.md
```

---

## Template Sections

- Primary Navigation (main menu structure)
- Secondary Navigation (contextual menus)
- Breadcrumb Trails
- Deep Linking Patterns
- Navigation States (active, disabled, etc.)
- Mobile Navigation Adaptations

---

## Related

- **Skill**: `.claude/skills/Discovery_SpecNavigation/`
