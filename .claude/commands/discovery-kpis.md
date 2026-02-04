---
name: discovery-kpis
description: Generate KPI definitions from discovery materials
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
skills:
  required:
    - Discovery_GenerateKPIs
  optional:
    - business-model-canvas
    - dashboard-creator
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-kpis started '{"stage": "discovery"}'
  Stop:
    - hooks:
        # VALIDATION: Check kpis-and-goals document was created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/03-strategy"
            --requires "kpis-and-goals.md"
        # VALIDATION: Check kpis has required sections
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_file_contains.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/03-strategy"
            --pattern "kpis-and-goals.md"
            --contains "## KPIs"
            --contains "## Success Metrics"
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-kpis ended '{"stage": "discovery", "validated": true}'
---


# /discovery-kpis - Generate KPIs and Goals Document

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-kpis instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- Roadmap document exists
- `03-strategy/product-roadmap.md` exists
- `traceability/pain_point_registry.json` populated

## Skills Used

- `.claude/skills/Discovery_GenerateKPIs/Discovery_GenerateKPIs.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read `03-strategy/product-roadmap.md` for features
   - Read `traceability/pain_point_registry.json` for impact metrics

2. **Read Discovery_GenerateKPIs Skill**
   - Understand North Star metric concept
   - Review KPI categories

3. **Generate KPIs Document**
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

4. **Content Structure**
   ```markdown
   # KPIs and Goals - <SystemName>

   ## North Star Metric

   ### [Metric Name]
   **Definition**: [Clear definition]
   **Current Baseline**: [If known]
   **Target**: [Specific target]
   **Rationale**: [Why this is the North Star]

   ## KPI Categories

   ### Adoption Metrics
   | KPI | Definition | Baseline | Target | Timeline |
   |-----|------------|----------|--------|----------|
   | Active Users | ... | ... | ... | Phase 1 |
   | Feature Adoption | ... | ... | ... | Phase 1 |

   ### Engagement Metrics
   | KPI | Definition | Baseline | Target | Timeline |
   |-----|------------|----------|--------|----------|
   | Session Duration | ... | ... | ... | ... |
   | Actions per Session | ... | ... | ... | ... |

   ### Efficiency Metrics
   | KPI | Definition | Baseline | Target | Timeline |
   |-----|------------|----------|--------|----------|
   | Time to Complete [Task] | ... | ... | ... | ... |
   | Error Rate | ... | ... | ... | ... |

   ### Satisfaction Metrics
   | KPI | Definition | Baseline | Target | Timeline |
   |-----|------------|----------|--------|----------|
   | NPS Score | ... | ... | ... | ... |
   | User Satisfaction | ... | ... | ... | ... |

   ## Pain Point Resolution Metrics

   | Pain Point | Metric | Current | Target |
   |------------|--------|---------|--------|
   | PP-1.1 | [Related metric] | ... | ... |
   | PP-1.2 | [Related metric] | ... | ... |

   ## ROI Framework

   ### Cost Savings
   | Area | Current Cost | Projected Savings | Calculation |
   |------|--------------|-------------------|-------------|
   | ... | ... | ... | ... |

   ### Productivity Gains
   | Task | Current Time | Target Time | Hours Saved |
   |------|--------------|-------------|-------------|
   | ... | ... | ... | ... |

   ## Measurement Plan

   ### Data Sources
   | Metric | Source | Collection Method |
   |--------|--------|-------------------|
   | ... | ... | ... |

   ### Review Cadence
   - Daily: [Metrics]
   - Weekly: [Metrics]
   - Monthly: [Metrics]
   - Quarterly: [Metrics]

   ## Goals by Roadmap Phase

   ### Phase 1 Goals
   - [ ] Goal 1 (Target: [value])
   - [ ] Goal 2 (Target: [value])

   ### Phase 2 Goals
   - [ ] Goal 1 (Target: [value])

   ### Phase 3 Goals
   - [ ] Goal 1 (Target: [value])
   ```

5. **Update Progress**
   - Set phase `8_kpis` to "complete"

## Quality Checklist

- [ ] North Star metric clearly defined
- [ ] KPIs cover all four categories
- [ ] Baselines established where possible
- [ ] Targets are specific and measurable
- [ ] Pain points mapped to metrics

## Outputs

- `ClientAnalysis_<SystemName>/03-strategy/kpis-and-goals.md`

## Next Command

- Run `/discovery-screens` to start design specs phase
- Or run `/discovery-specs-all` for all spec documents
