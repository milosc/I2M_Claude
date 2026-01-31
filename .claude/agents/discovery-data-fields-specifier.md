---
name: discovery-data-fields-specifier
description: Define all data fields, validation rules, and data types extracted from client materials and workflows.
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

# Data Fields Specifier Agent

## FIRST ACTION (MANDATORY)

```bash
bash .claude/hooks/log-lifecycle.sh subagent discovery-data-fields-specifier started '{"stage": "discovery", "method": "instruction-based"}'
python3 .claude/hooks/agent_coordinator.py --register --agent-id "data-fields-specifier" --agent-type "discovery-data-fields-specifier" --task-id "{TASK_ID}"
```

**Agent ID**: `discovery:data-fields-specifier`
**Model**: sonnet | **Checkpoint**: 9 | **Version**: 2.0.0

---

## Purpose

Define all data fields with types, validation rules, constraints, and relationships based on workflows and screen definitions.

---

## Inputs/Outputs

```yaml
inputs:
  - data analysis (spreadsheets, forms)
  - screen-definitions.md
  - workflow observations

output:
  - 04-design-specs/data-fields.md
```

---

## Template Format

```markdown
## Field: {Field Name}

**ID**: DF-XXX
**Type**: {String | Number | Date | Boolean | Enum}
**Required**: {Yes | No}
**Validation**: {Rules}
**Default**: {Default value}
**Appears In**: {Screen IDs}
**Traces To**: {Pain Point or JTBD}
```

---

## Related

- **Skill**: `.claude/skills/Discovery_SpecDataModel/`
