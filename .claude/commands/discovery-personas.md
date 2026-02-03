---
name: discovery-personas
description: Generate all persona files from user types
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-personas started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-personas ended '{"stage": "discovery"}'
---


# /discovery-personas - Generate All Persona Files

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-personas instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

None required - reads configuration from `_state/discovery_config.json`

## Prerequisites

- Analysis phase complete
- `traceability/user_type_registry.json` populated
- `traceability/pain_point_registry.json` populated
- `01-analysis/ANALYSIS_SUMMARY.md` exists

## Skills Used

- `.claude/skills/Discovery_GeneratePersona/Discovery_GeneratePersona.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read `traceability/user_type_registry.json` for user types
   - Read `traceability/pain_point_registry.json` for pain points
   - Read `01-analysis/ANALYSIS_SUMMARY.md` for context

2. **Read Discovery_GeneratePersona Skill**
   - Review persona selection criteria
   - Understand persona count guidelines
   - Review template structure

3. **Determine Personas to Create**
   | User Types Found | Action |
   |-----------------|--------|
   | 1-3 | All as personas |
   | 4-6 | 3-4 primary + composite |
   | 7+ | 4-5 primary, group others |

4. **Generate Each Persona File**
   For each selected user type:
   - Create `02-research/persona-<role-slug>.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: PERSONA-<SystemName>-<ROLE-SLUG>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_GeneratePersona
     source_files:
       - 01-analysis/ANALYSIS_SUMMARY.md
       - traceability/user_type_registry.json
     ---
     ```
   - Follow full template from skill:
     - Overview table
     - Profile with representative name
     - Goals with success metrics
     - Pain points (P0, P1, P2) with quotes
     - Daily workflow table
     - Technical context
     - Jobs To Be Done preview
     - Representative quotes
     - Design implications
     - Feature priorities
     - Success indicators
     - Relationships

5. **Update User Type Registry**
   - Add `persona_file` reference to each entry

6. **Update Progress**
   - Set phase `3_personas` to "complete" if all personas generated

## File Naming Convention

- Use lowercase with hyphens
- Pattern: `persona-<role-slug>.md`
- Examples:
  - `persona-warehouse-manager.md`
  - `persona-inventory-clerk.md`
  - `persona-shipping-coordinator.md`

## Quality Checklist

Before completing:
- [ ] Each persona has at least 3 supporting quotes
- [ ] Pain points link to registry IDs (PP-X.Y)
- [ ] Workflow is specific to role
- [ ] Feature priorities are justified
- [ ] Success metrics are measurable

## Outputs

- `ClientAnalysis_<SystemName>/02-research/persona-*.md` (3-5 files)
- Updated `traceability/user_type_registry.json`

## Next Command

- Run `/discovery-jtbd` to generate JTBD document
- Or run `/discovery-research` for full research phase
