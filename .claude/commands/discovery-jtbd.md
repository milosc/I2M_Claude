---
name: discovery-jtbd
description: Generate Jobs-To-Be-Done from pain points and research
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-jtbd started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-jtbd ended '{"stage": "discovery"}'
---


# /discovery-jtbd - Generate Jobs-To-Be-Done Document

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-jtbd instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- Personas generated
- `02-research/persona-*.md` files exist
- `traceability/pain_point_registry.json` populated

## Skills Used

- `.claude/skills/Discovery_GenerateJTBD/Discovery_GenerateJTBD.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read all persona files from `02-research/`
   - Read `traceability/pain_point_registry.json`

2. **Read Discovery_GenerateJTBD Skill**
   - Understand JTBD format
   - Review grouping and prioritization approach

3. **Generate JTBD Document**
   - Create `02-research/jtbd-jobs-to-be-done.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-JTBD-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_GenerateJTBD
     source_files:
       - 02-research/persona-*.md
       - traceability/pain_point_registry.json
     ---
     ```

4. **JTBD Format**
   Use standard format:
   > **When** [situation/trigger], **I want to** [action/capability], **So I can** [outcome/benefit]

5. **Content Structure**
   ```markdown
   # Jobs To Be Done - <SystemName>

   ## Overview
   [Summary of JTBD approach and coverage]

   ## JTBD by Feature Area

   ### 1. [Feature Area Name]

   #### JTBD-1.1: [Job Title]
   **Priority**: P0
   **Personas**: [Persona names]

   > **When** [situation], **I want to** [action], **So I can** [outcome]

   **Pain Points Addressed**: PP-1.1, PP-1.2
   **Success Criteria**: [Measurable outcome]

   #### JTBD-1.2: [Job Title]
   ...

   ### 2. [Feature Area Name]
   ...

   ## JTBD-Persona Matrix

   | JTBD | Persona 1 | Persona 2 | Persona 3 |
   |------|-----------|-----------|-----------|
   | JTBD-1.1 | ✅ Primary | ⚪ Secondary | - |
   ...

   ## Priority Summary

   | Priority | Count | Feature Areas |
   |----------|-------|---------------|
   | P0 | N | Area1, Area2 |
   | P1 | N | Area3 |
   | P2 | N | Area4 |
   ```

6. **Populate JTBD Registry**
   - Update `traceability/jtbd_registry.json`
   - Assign hierarchical IDs: JTBD-1.1, JTBD-1.2, JTBD-2.1...
   - Link to source pain points (PP-X.Y)
   - Link to personas (UT-X.Y)

7. **Update Trace Matrix**
   - Add PP → JTBD links to `traceability/trace_matrix.json`

8. **Update Progress**
   - Set phase `4_jtbd` to "complete"

## ID Assignment Rules

- Group by feature area (X = area number)
- Sequence within area (Y = sequence)
- Examples: JTBD-1.1, JTBD-1.2, JTBD-2.1, JTBD-2.2

## Quality Checklist

- [ ] Every P0 pain point has at least one JTBD
- [ ] Every persona has assigned JTBDs
- [ ] JTBDs are actionable and measurable
- [ ] Priority reflects pain point severity

## Outputs

- `ClientAnalysis_<SystemName>/02-research/jtbd-jobs-to-be-done.md`
- Updated `traceability/jtbd_registry.json`
- Updated `traceability/trace_matrix.json`

## Next Command

- Run `/discovery-vision` to start strategy phase
- Or run `/discovery-strategy-all` for all strategy docs
