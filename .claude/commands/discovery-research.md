---
description: Extract research findings from discovery materials
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-research started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-research ended '{"stage": "discovery"}'
---


# /discovery-research - Generate Personas & JTBD

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-research instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- `/discovery-analyze` completed (phases 1-2 complete)
- `_state/discovery_progress.json` shows phases 1-2 complete
- `traceability/pain_point_registry.json` populated
- `traceability/user_type_registry.json` populated

## Skills Used

- `.claude/skills/Discovery_ClassifyProject/SKILL.md` - **MANDATORY**: Classifies project type
- `.claude/skills/Discovery_GeneratePersona/Discovery_GeneratePersona.md`
- `.claude/skills/Discovery_GenerateJTBD/Discovery_GenerateJTBD.md`

## Execution Steps

### Phase 3: Generate Personas

1. **Load Prerequisites**
   - Read `_state/discovery_config.json` for output_path
   - Read `traceability/user_type_registry.json` for user types
   - Read `traceability/pain_point_registry.json` for pain points
   - Read `01-analysis/ANALYSIS_SUMMARY.md` for context

2. **Update Progress**
   - Set phase `3_personas` status to "in_progress"
   - Update `discovery_config.json` current_checkpoint

3. **Verify Project Classification** (MANDATORY)
   - Read `_state/discovery_config.json`
   - Check if `project_classification` field exists and is populated
   - **IF MISSING**:
     - Read `.claude/skills/Discovery_ClassifyProject/SKILL.md`
     - Run `Discovery_ClassifyProject` to analyze materials and determine project type
     - This will update `_state/discovery_config.json` with type (FULL_STACK, BACKEND_ONLY, etc.)
     - **CONTINUE** only after classification is set

4. **Read Discovery_GeneratePersona Skill**
   - Follow persona selection criteria
   - Use persona count guidelines based on user types found

4. **Determine Personas to Create**
   | User Types Found | Recommended Personas |
   |-----------------|---------------------|
   | 1-3 | All as personas |
   | 4-6 | 3-4 primary + composite secondary |
   | 7+ | 4-5 primary, group others |

5. **Generate Each Persona File**
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
   - Follow Discovery_GeneratePersona template structure
   - Link pain points using PP-X.Y IDs
   - Include supporting quotes

6. **Update User Type Registry**
   - Add `persona_file` reference to each UT-X.Y entry
   - Update trace links

7. **Update Progress**
   - Set phase `3_personas` to "complete"

### Phase 4: Generate JTBD

8. **Read Discovery_GenerateJTBD Skill**
   - Understand JTBD format: "When [situation], I want to [action], So I can [outcome]"

9. **Update Progress**
   - Set phase `4_jtbd` status to "in_progress"

10. **Generate JTBD Document**
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
    - Group JTBDs by feature area
    - Assign hierarchical IDs: JTBD-1.1, JTBD-1.2, JTBD-2.1...
    - Map to personas and pain points
    - Assign priorities (P0, P1, P2)

11. **Populate JTBD Registry**
    - Update `traceability/jtbd_registry.json` with all JTBDs
    - Include links to source pain points (PP-X.Y)
    - Include links to target personas (UT-X.Y)

12. **Update Trace Matrix**
    - Update `traceability/trace_matrix.json`
    - Add PP → JTBD links to chains
    - Update coverage statistics

13. **Update Context Memory**
    - Add key decisions to `discovery_context.json`
    - Record number of personas and JTBDs created
    - Update resumption_context

14. **Update Progress**
    - Set phase `4_jtbd` to "complete"
    - Update overall_progress
    - Set resumable_from to "5_vision"

## State Updates

### Updated in `_state/`:
- `discovery_config.json` - current_phase, current_checkpoint, updated_at, **project_classification**
- `discovery_progress.json` - phases 3-4 complete, overall_progress
- `discovery_context.json` - key_decisions, resumption_context

### Updated in `traceability/`:
- `user_type_registry.json` - persona_file references added
- `jtbd_registry.json` - populated with JTBD-X.Y items
- `trace_matrix.json` - PP→JTBD links added, coverage updated

## Outputs

- `ClientAnalysis_<SystemName>/02-research/persona-*.md` (3-5 files)
- `ClientAnalysis_<SystemName>/02-research/jtbd-jobs-to-be-done.md`
- Updated traceability registries

## Error Handling

- If insufficient user types found: Create composite "Primary User" persona
- If no pain points available: Flag gaps, create minimal persona
- If conflicting information: Note conflict, use most recent/reliable source
- Continue with available data, note gaps in outputs

## State Updates

After `/discovery-research`:
- Run `/discovery-strategy-all` to generate vision, strategy, roadmap, and KPIs
- Or run individual commands: `/discovery-vision`, `/discovery-strategy`, etc.
