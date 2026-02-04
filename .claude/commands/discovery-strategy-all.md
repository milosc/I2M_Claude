---
name: discovery-strategy-all
description: Generate all strategy documents (vision, roadmap, KPIs)
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-strategy-all started '{"stage": "discovery"}'
  Stop:
    - hooks:
        # VALIDATION: Check product-vision.md was created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/03-strategy"
            --requires "product-vision.md"
        # VALIDATION: Check product-strategy.md was created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/03-strategy"
            --requires "product-strategy.md"
        # VALIDATION: Check product-roadmap.md was created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/03-strategy"
            --requires "product-roadmap.md"
        # VALIDATION: Check kpis-and-goals.md was created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/03-strategy"
            --requires "kpis-and-goals.md"
        # VALIDATION: Check vision has required sections
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_file_contains.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/03-strategy"
            --pattern "product-vision.md"
            --contains "## Vision Statement"
            --contains "## Target Users"
        # VALIDATION: Check roadmap has required sections
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_file_contains.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/03-strategy"
            --pattern "product-roadmap.md"
            --contains "## Phase"
        # VALIDATION: Check requirements registry was updated
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "traceability"
            --requires "requirements_registry.json"
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-strategy-all ended '{"stage": "discovery", "validated": true}'
---


# /discovery-strategy-all - Generate All Strategy Documents

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-strategy-all instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- `/discovery-research` completed (phases 3-4 complete)
- `_state/discovery_progress.json` shows phases 3-4 complete
- `02-research/persona-*.md` files exist
- `02-research/jtbd-jobs-to-be-done.md` exists
- `traceability/jtbd_registry.json` populated

## Skills Used

- `.claude/skills/Discovery_ClassifyProject/SKILL.md` - **MANDATORY**: Classifies project type
- `.claude/skills/Discovery_GenerateVision/Discovery_GenerateVision.md`
- `.claude/skills/Discovery_GenerateStrategy/Discovery_GenerateStrategy.md`
- `.claude/skills/Discovery_GenerateRoadmap/Discovery_GenerateRoadmap.md`
- `.claude/skills/Discovery_GenerateKPIs/Discovery_GenerateKPIs.md`

## Execution Steps

### Phase 5: Generate Vision

1. **Load Prerequisites**
   - Read `_state/discovery_config.json` for output_path
   - Read all persona files from `02-research/`
   - Read `02-research/jtbd-jobs-to-be-done.md`
   - Read `traceability/pain_point_registry.json`

2. **Update Progress**
   - Set phase `5_vision` status to "in_progress"

3. **Verify Project Classification** (MANDATORY)
   - Read `_state/discovery_config.json`
   - Check if `project_classification` field exists and is populated
   - **IF MISSING**:
     - Read `.claude/skills/Discovery_ClassifyProject/SKILL.md`
     - Run `Discovery_ClassifyProject` to analyze materials and determine project type
     - This will update `_state/discovery_config.json` with type (FULL_STACK, BACKEND_ONLY, etc.)
     - **CONTINUE** only after classification is set

4. **Read Discovery_GenerateVision Skill**
   - Understand vision statement structure
   - Identify key components: pain points, capabilities, target users

4. **Generate Vision Document**
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
   - Include vision statement addressing top P0 pain points
   - Map capabilities to pain points
   - Reference personas as target users

5. **Update Progress**
   - Set phase `5_vision` to "complete"

### Phase 6: Generate Strategy

6. **Update Progress**
   - Set phase `6_strategy` status to "in_progress"

7. **Read Discovery_GenerateStrategy Skill**
   - Understand strategic pillars structure
   - Identify go-to-market considerations

8. **Generate Strategy Document**
   - Create `03-strategy/product-strategy.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-STRATEGY-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_GenerateStrategy
     source_files:
       - 03-strategy/product-vision.md
       - 02-research/jtbd-jobs-to-be-done.md
     ---
     ```
   - Define strategic pillars
   - Include go-to-market approach
   - Reference vision and JTBDs

9. **Update Progress**
   - Set phase `6_strategy` to "complete"

### Phase 7: Generate Roadmap

10. **Update Progress**
    - Set phase `7_roadmap` status to "in_progress"

11. **Read Discovery_GenerateRoadmap Skill**
    - Understand phase/epic structure
    - Map JTBDs to features

12. **Generate Roadmap Document**
    - Create `03-strategy/product-roadmap.md`
    - Include version metadata:
      ```yaml
      ---
      document_id: DISC-ROADMAP-<SystemName>
      version: 1.0.0
      created_at: <YYYY-MM-DD>
      updated_at: <YYYY-MM-DD>
      generated_by: Discovery_GenerateRoadmap
      source_files:
        - 03-strategy/product-strategy.md
        - traceability/jtbd_registry.json
      ---
      ```
    - Define phases (Foundation, Core, Enhanced)
    - Create epics with features
    - Map JTBDs to features
    - Prioritize based on P0/P1/P2 pain points

13. **Extract Features to Registry**
    - Populate `traceability/requirements_registry.json`
    - Assign hierarchical IDs: US-1.1, US-1.2, FR-1.1...
    - Link features to JTBDs (JTBD-X.Y)

14. **Update Trace Matrix**
    - Add JTBD → Feature links to chains
    - Update coverage statistics

15. **Update Progress**
    - Set phase `7_roadmap` to "complete"

### Phase 8: Generate KPIs

16. **Update Progress**
    - Set phase `8_kpis` status to "in_progress"

17. **Read Discovery_GenerateKPIs Skill**
    - Understand North Star metric concept
    - Identify KPI categories

18. **Generate KPIs Document**
    - Create `03-strategy/kpis-and-goals.md`
    - Include version metadata:
      ```yaml
      ---
      document_id: DISC-KPIS-<SystemName>
      version: 1.0.0
      created_at: <YYYY-MM-DD>
      updated_at: <YYYY-MM-DD>
      generated_by: Discovery_GenerateKPIs
      source_files:
        - 03-strategy/product-roadmap.md
        - traceability/pain_point_registry.json
      ---
      ```
    - Define North Star metric
    - Create category KPIs (adoption, engagement, efficiency, satisfaction)
    - Link KPIs to roadmap phases
    - Include ROI calculations if data available

19. **Update Context Memory**
    - Add key decisions to `discovery_context.json`
    - Record strategic choices made
    - Update resumption_context

20. **Update Progress**
    - Set phase `8_kpis` to "complete"
    - Update overall_progress
    - Set resumable_from to "9_specs"

## State Updates

### Updated in `_state/`:
- `discovery_config.json` - current_phase, current_checkpoint, updated_at, **project_classification**
- `discovery_progress.json` - phases 5-8 complete, overall_progress
- `discovery_context.json` - key_decisions, resumption_context

### Updated in `traceability/`:
- `requirements_registry.json` - populated with US-X.Y, FR-X.Y items
- `trace_matrix.json` - JTBD→Feature links added, coverage updated

## Outputs

- `ClientAnalysis_<SystemName>/03-strategy/product-vision.md`
- `ClientAnalysis_<SystemName>/03-strategy/product-strategy.md`
- `ClientAnalysis_<SystemName>/03-strategy/product-roadmap.md`
- `ClientAnalysis_<SystemName>/03-strategy/kpis-and-goals.md`
- Updated traceability registries

## Error Handling

- If insufficient JTBDs: Create minimal roadmap with identified pain points
- If no quantified metrics available: Note gap, use qualitative goals
- Continue with available data, note gaps in outputs

## State Updates

## Next Command

After `/discovery-strategy-all`:
- Run `/discovery-specs-all` to generate design specifications
- Or run individual commands: `/discovery-screens`, `/discovery-navigation`, etc.
