---
description: Generate product roadmap from discovery strategy
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-roadmap started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-roadmap ended '{"stage": "discovery"}'
---


# /discovery-roadmap - Generate Product Roadmap Document

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-roadmap instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- Strategy document exists
- `03-strategy/product-strategy.md` exists
- `traceability/jtbd_registry.json` populated

## Skills Used

- `.claude/skills/Discovery_ClassifyProject/SKILL.md` - **MANDATORY**: Classifies project type
- `.claude/skills/Discovery_GenerateRoadmap/Discovery_GenerateRoadmap.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read `03-strategy/product-strategy.md` for strategic pillars
   - Read `traceability/jtbd_registry.json` for jobs to map

2. **Verify Project Classification** (MANDATORY)
   - Read `_state/discovery_config.json`
   - Check if `project_classification` field exists and is populated
   - **IF MISSING**:
     - Read `.claude/skills/Discovery_ClassifyProject/SKILL.md`
     - Run `Discovery_ClassifyProject` to analyze materials and determine project type
     - This will update `_state/discovery_config.json` with type (FULL_STACK, BACKEND_ONLY, etc.)
     - **CONTINUE** only after classification is set

3. **Read Discovery_GenerateRoadmap Skill**
   - Understand phase/epic structure
   - Review feature mapping approach

3. **Generate Roadmap Document**
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

4. **Content Structure**
   ```markdown
   # Product Roadmap - <SystemName>

   ## Roadmap Overview
   [Summary of phased approach]

   ## Phase 1: Foundation
   **Focus**: Core functionality addressing P0 pain points
   **Target**: [Target milestone/release]

   ### Epic 1.1: [Epic Name]
   **Priority**: P0
   **JTBDs Addressed**: JTBD-1.1, JTBD-1.2

   #### Features
   | ID | Feature | Priority | JTBD | Status |
   |----|---------|----------|------|--------|
   | US-1.1 | ... | P0 | JTBD-1.1 | Planned |
   | US-1.2 | ... | P0 | JTBD-1.1 | Planned |

   ### Epic 1.2: [Epic Name]
   ...

   ## Phase 2: Core Experience
   **Focus**: Enhanced functionality and efficiency
   **Target**: [Target milestone]

   ### Epic 2.1: [Epic Name]
   ...

   ## Phase 3: Advanced Features
   **Focus**: Differentiation and optimization
   **Target**: [Target milestone]

   ### Epic 3.1: [Epic Name]
   ...

   ## Feature-JTBD Mapping

   | Feature ID | Feature Name | JTBD | Pain Points |
   |------------|--------------|------|-------------|
   | US-1.1 | ... | JTBD-1.1 | PP-1.1, PP-1.2 |

   ## Dependencies

   ```mermaid
   graph LR
   A[Epic 1.1] --> B[Epic 1.2]
   B --> C[Epic 2.1]
   ```

   ## Release Notes
   [Summary of what each phase delivers]
   ```

5. **Populate Requirements Registry**
   - Update `traceability/requirements_registry.json`
   - Assign hierarchical IDs: US-1.1, US-1.2, FR-1.1...
   - Link features to JTBDs (JTBD-X.Y)

6. **Update Trace Matrix**
   - Add JTBD → Feature links to `traceability/trace_matrix.json`

7. **Update Progress**
   - Set phase `7_roadmap` to "complete"

## ID Assignment Rules

- US-X.Y for user stories (X = epic, Y = sequence)
- FR-X.Y for functional requirements
- NFR-X.Y for non-functional requirements

## Quality Checklist

- [ ] All P0 JTBDs addressed in Phase 1
- [ ] Features linked to JTBDs
- [ ] Dependencies clearly defined
- [ ] Phases have clear scope boundaries

## Outputs

- `ClientAnalysis_<SystemName>/03-strategy/product-roadmap.md`
- Updated `traceability/requirements_registry.json`
- Updated `traceability/trace_matrix.json`

## ID Assignment Rules

## Next Command

- Run `/discovery-kpis` to generate KPIs document
- Or run `/discovery-strategy-all` for all strategy docs
