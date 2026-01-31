# Skill Logging Template

This template shows how to integrate pipeline logging into skills.

## For Python-based Skills

Add this at the top of your skill logic:

```python
#!/usr/bin/env python3
import sys
from pathlib import Path

# Import skill logging
sys.path.insert(0, str(Path(__file__).parent.parent.parent / ".claude/hooks"))
from skill_invoke import log_skill_execution

# Your skill logic
def main():
    # Use context manager for automatic start/end logging
    with log_skill_execution(
        skill_name="YourSkillName",
        intent="Brief description of what this skill does",
        stage="discovery",  # or prototype, productspecs, solarch, implementation
        system_name=None  # Optional: pass if available
    ):
        # Your skill implementation here
        print("🚀 Starting skill execution...")

        # ... do work ...

        print("✅ Skill completed")

if __name__ == "__main__":
    main()
```

## For Markdown-based Skills (Agent Prompts)

Add this section at the beginning of your skill prompt:

```markdown
## Execution Logging

**BEFORE starting work:**

```bash
SKILL_EVENT_ID=$(python3 .claude/hooks/skill_invoke.py \
  --skill-name "YourSkillName" \
  --action "start" \
  --stage "discovery" \
  --intent "Brief description of what this skill does")

echo "Skill started: $SKILL_EVENT_ID"
```

**AFTER completing work:**

```bash
python3 .claude/hooks/skill_invoke.py \
  --skill-name "YourSkillName" \
  --action "end" \
  --start-event-id "$SKILL_EVENT_ID" \
  --status "completed" \
  --outputs '{"files_created": 5, "checkpoint": 3}'
```

## If skill fails:

```bash
python3 .claude/hooks/skill_invoke.py \
  --skill-name "YourSkillName" \
  --action "end" \
  --start-event-id "$SKILL_EVENT_ID" \
  --status "failed" \
  --error-message "Reason for failure"
```
```

## For Skills Invoked via Claude Code Skill Tool

When Claude Code invokes a skill, add logging at the START and END of the skill prompt:

```markdown
---
name: your-skill-name
description: Your skill description
---

# Your Skill Name

**IMPORTANT: Log skill execution for monitoring**

At the start of your work:
1. Read the skill_invoke.py module
2. Call it to log skill start

```javascript
// Log skill start
const skillEventId = await bash(`python3 .claude/hooks/skill_invoke.py \\
  --skill-name "your-skill-name" \\
  --action "start" \\
  --stage "discovery" \\
  --intent "Your skill intent description"`);

console.log(`📊 Skill started: ${skillEventId}`);
```

[Your skill implementation]

At the end of your work:

```javascript
// Log skill end
await bash(`python3 .claude/hooks/skill_invoke.py \\
  --skill-name "your-skill-name" \\
  --action "end" \\
  --start-event-id "${skillEventId}" \\
  --status "completed" \\
  --outputs '{"result": "success", "files_created": 10}'`);

console.log(`✅ Skill completed`);
```
```

## Automatic Logging for Orchestrator Skills

For orchestrator skills that spawn multiple sub-skills, wrap the entire orchestration:

```python
from skill_invoke import log_skill_execution

def orchestrate():
    with log_skill_execution("OrchestratorSkill", "Orchestrate multi-step process"):
        # Spawn sub-skills
        # Each sub-skill will log its own execution
        spawn_sub_skill_1()
        spawn_sub_skill_2()
        spawn_sub_skill_3()
```

## Context Information

The logging automatically captures:
- **skill_name**: Name of the skill
- **intent**: What the skill is doing
- **stage**: Current pipeline stage (discovery, prototype, etc.)
- **system_name**: System being worked on (if available)
- **duration**: Automatically calculated for context manager
- **status**: completed, failed
- **outputs**: Optional results/outputs

## Best Practices

1. **Always use context manager** when possible (automatic start/end)
2. **Log at skill boundaries** - not for internal helper functions
3. **Include meaningful intent** - helps with debugging and monitoring
4. **Pass system_name** when available - enables better attribution
5. **Include outputs** on success - helps track what was produced
6. **Include error_message** on failure - aids debugging

## Examples

### Discovery Persona Generator Skill

```python
from skill_invoke import log_skill_execution

def generate_persona(system_name, persona_data):
    with log_skill_execution(
        skill_name="Discovery_GeneratePersona",
        intent=f"Generate persona from user research data",
        stage="discovery",
        system_name=system_name
    ):
        # Generate persona document
        persona = create_persona_document(persona_data)

        # Write to file
        output_file = f"ClientAnalysis_{system_name}/personas/{persona['id']}.md"
        write_file(output_file, persona)

        return {"persona_id": persona['id'], "file": output_file}
```

### Prototype Component Generator Skill

```python
from skill_invoke import log_skill_execution

def generate_components(system_name, component_specs):
    with log_skill_execution(
        skill_name="Prototype_ComponentGenerator",
        intent=f"Generate {len(component_specs)} components",
        stage="prototype",
        system_name=system_name
    ):
        generated = []

        for spec in component_specs:
            component_file = generate_component(spec)
            generated.append(component_file)

        return {
            "components_generated": len(generated),
            "files": generated
        }
```

## Integration Checklist

- [ ] Import `log_skill_execution` or call `skill_invoke.py`
- [ ] Wrap skill logic with logging context
- [ ] Include meaningful skill name and intent
- [ ] Pass stage and system_name when available
- [ ] Handle errors with proper logging
- [ ] Return outputs for success tracking
