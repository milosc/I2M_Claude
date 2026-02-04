---
name: discovery-strategy-doc
description: Generate single strategy document
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-strategy-doc started '{"stage": "discovery"}'
  Stop:
    - hooks:
        # VALIDATION: Check product-strategy.md was created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/03-strategy"
            --requires "product-strategy.md"
        # VALIDATION: Check strategy has required sections
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_file_contains.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/03-strategy"
            --pattern "product-strategy.md"
            --contains "## Strategic Pillars"
            --contains "## Go-To-Market"
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-strategy-doc ended '{"stage": "discovery", "validated": true}'
---


# /discovery-strategy-doc - Generate Product Strategy Document

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-strategy-doc instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- Vision document exists
- `03-strategy/product-vision.md` exists
- `02-research/jtbd-jobs-to-be-done.md` exists

## Skills Used

- `.claude/skills/Discovery_ClassifyProject/SKILL.md` - **MANDATORY**: Classifies project type
- `.claude/skills/Discovery_GenerateStrategy/Discovery_GenerateStrategy.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read `03-strategy/product-vision.md` for vision context
   - Read `02-research/jtbd-jobs-to-be-done.md` for jobs

2. **Verify Project Classification** (MANDATORY)
   - Read `_state/discovery_config.json`
   - Check if `project_classification` field exists and is populated
   - **IF MISSING**:
     - Read `.claude/skills/Discovery_ClassifyProject/SKILL.md`
     - Run `Discovery_ClassifyProject` to analyze materials and determine project type
     - This will update `_state/discovery_config.json` with type (FULL_STACK, BACKEND_ONLY, etc.)
     - **CONTINUE** only after classification is set

3. **Read Discovery_GenerateStrategy Skill**
   - Understand strategic pillars format
   - Review go-to-market section

3. **Generate Strategy Document**
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

4. **Content Structure**
   ```markdown
   # Product Strategy - <SystemName>

   ## Strategic Overview
   [Summary of strategic approach]

   ## Strategic Pillars

   ### Pillar 1: [Name]
   **Objective**: [Clear objective]
   **Rationale**: [Why this pillar matters]
   **Key Initiatives**:
   - Initiative 1
   - Initiative 2
   **Success Metrics**:
   - Metric 1
   - Metric 2
   **Related JTBDs**: JTBD-1.1, JTBD-1.2

   ### Pillar 2: [Name]
   ...

   ### Pillar 3: [Name]
   ...

   ## Go-To-Market Strategy

   ### Target Segments
   [Primary user segments and prioritization]

   ### Adoption Strategy
   [How users will be onboarded and engaged]

   ### Rollout Approach
   - Phase 1: [Scope and users]
   - Phase 2: [Expansion]
   - Phase 3: [Full deployment]

   ## Competitive Positioning

   ### Current Alternatives
   | Alternative | Strengths | Weaknesses |
   |-------------|-----------|------------|
   | ... | ... | ... |

   ### Our Differentiation
   [Clear differentiation statement]

   ## Risk Mitigation

   ### Key Risks
   | Risk | Impact | Mitigation |
   |------|--------|------------|
   | ... | High/Medium/Low | ... |

   ## Success Framework
   [How success will be measured at strategic level]
   ```

5. **Update Progress**
   - Set phase `6_strategy` to "complete"

## Quality Checklist

- [ ] Strategic pillars align with vision
- [ ] JTBDs mapped to initiatives
- [ ] Go-to-market is actionable
- [ ] Risks identified with mitigations

## Outputs

- `ClientAnalysis_<SystemName>/03-strategy/product-strategy.md`

## Quality Checklist

## Next Command

- Run `/discovery-roadmap` to generate roadmap
- Or run `/discovery-strategy-all` for all strategy docs
