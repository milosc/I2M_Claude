---
description: Generate product vision document from discovery materials
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-vision started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-vision ended '{"stage": "discovery"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-vision instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- Research phase complete (phases 3-4)
- `02-research/persona-*.md` files exist
- `02-research/jtbd-jobs-to-be-done.md` exists
- `traceability/pain_point_registry.json` populated

## Skills Used

- `.claude/skills/Discovery_ClassifyProject/SKILL.md` - **MANDATORY**: Classifies project type
- `.claude/skills/Discovery_GenerateVision/Discovery_GenerateVision.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path, system_name
   - Read persona files for target users
   - Read `02-research/jtbd-jobs-to-be-done.md` for jobs
   - Read `traceability/pain_point_registry.json` for P0 issues

2. **Verify Project Classification** (MANDATORY)
   - Read `_state/discovery_config.json`
   - Check if `project_classification` field exists and is populated
   - **IF MISSING**:
     - Read `.claude/skills/Discovery_ClassifyProject/SKILL.md`
     - Run `Discovery_ClassifyProject` to analyze materials and determine project type
     - This will update `_state/discovery_config.json` with type (FULL_STACK, BACKEND_ONLY, etc.)
     - **CONTINUE** only after classification is set

3. **Read Discovery_GenerateVision Skill**
   - Understand vision statement format
   - Review capability mapping approach

3. **Generate Vision Document**
   - Create `03-strategy/product-vision.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-VISION-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_GenerateVision
     source_files:
       - 02-research/persona-*.md
       - 02-research/jtbd-jobs-to-be-done.md
       - traceability/pain_point_registry.json
     ---
     ```

4. **Content Structure**
   ```markdown
   # Product Vision - <SystemName>

   ## Vision Statement

   > For [target users] who [need/problem], the [product name] is a [product category] that [key benefit]. Unlike [current alternatives], our product [key differentiator].

   ## The Problem We're Solving

   ### Critical Pain Points (P0)
   | ID | Pain Point | Impact | Users Affected |
   |----|------------|--------|----------------|
   | PP-1.1 | ... | ... | ... |

   ### Current State
   [Description of how users handle these problems today]

   ## Our Solution

   ### Key Capabilities
   | Capability | Pain Points Addressed | JTBDs Enabled |
   |------------|----------------------|---------------|
   | ... | PP-1.1, PP-1.2 | JTBD-1.1 |

   ### Value Proposition
   [Clear statement of unique value]

   ## Target Users

   ### Primary Personas
   [Summary of personas and their needs]

   ### User Priorities
   | Persona | Primary Need | Success Metric |
   |---------|--------------|----------------|
   | ... | ... | ... |

   ## Success Criteria

   ### Business Outcomes
   - [Outcome 1]
   - [Outcome 2]

   ### User Outcomes
   - [Outcome 1]
   - [Outcome 2]

   ## Constraints & Assumptions
   [Known limitations and assumptions]
   ```

5. **Update Progress**
   - Set phase `5_vision` to "complete"

## Quality Checklist

- [ ] Vision statement addresses top P0 pain points
- [ ] All P0 pain points mapped to capabilities
- [ ] All personas represented as target users
- [ ] Success criteria are measurable

## Outputs

- `ClientAnalysis_<SystemName>/03-strategy/product-vision.md`

### Step 6: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST

echo "✅ Logged command completion"
```

## Next Command

- Run `/discovery-strategy` to generate strategy document
- Or run `/discovery-strategy-all` for all strategy docs
