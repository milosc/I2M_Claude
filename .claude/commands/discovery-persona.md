---
name: discovery-persona
description: Generate single persona file for specific role
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-persona started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-persona ended '{"stage": "discovery"}'
---


# /discovery-persona - Generate Single Persona File

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-persona instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Discovery-specific rules. Load them now:

```bash
# Load Discovery rules (includes PDF handling, input processing, output structure)
/rules-discovery

# Load Traceability rules (includes ID formats, source linking)
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Required: `<role-slug>` - The role to generate (e.g., warehouse-manager)

## Prerequisites

- Analysis phase complete
- `traceability/user_type_registry.json` populated
- User type exists for the specified role

## Skills Used

- `.claude/skills/Discovery_GeneratePersona/Discovery_GeneratePersona.md`

## Execution Steps

1. **Parse Arguments**
   - Extract `<role-slug>` from arguments
   - Normalize to lowercase with hyphens

2. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read `traceability/user_type_registry.json`
   - Find matching user type for `<role-slug>`
   - Read `traceability/pain_point_registry.json` for related pain points

3. **Validate Role Exists**
   - If no matching user type: Error with available roles list
   - If match found: Continue

4. **Read Discovery_GeneratePersona Skill**
   - Review template structure

5. **Generate Persona File**
   - Create `02-research/persona-<role-slug>.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: PERSONA-<SystemName>-<ROLE-SLUG>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_GeneratePersona
     ---
     ```
   - Follow full template structure
   - Filter pain points relevant to this role
   - Include role-specific quotes

6. **Update User Type Registry**
   - Add `persona_file` reference to the entry

## Example Usage

```bash
/discovery-persona warehouse-manager
/discovery-persona inventory-clerk
/discovery-persona shipping-coordinator
```

## Error Handling

- Role not found: List available roles from user_type_registry.json
- Insufficient data: Generate partial persona, note gaps

## Outputs

- `ClientAnalysis_<SystemName>/02-research/persona-<role-slug>.md`
- Updated `traceability/user_type_registry.json`

## Next Command

- Run `/discovery-persona <another-role>` for additional personas
- Run `/discovery-jtbd` when all personas complete
