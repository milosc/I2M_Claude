---
description: Generate Discovery executive summary document
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-summary started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-summary ended '{"stage": "discovery"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-summary instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- All previous phases complete
- All core documents exist

## Skills Used

- `.claude/skills/Discovery_DocSummary/Discovery_DocSummary.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for system_name
   - Read `traceability/trace_matrix.json` for coverage stats
   - Read all registries for counts

2. **Read Discovery_DocSummary Skill**
   - Understand executive summary format
   - Review statistics presentation

3. **Generate Summary Document**
   - Create `05-documentation/DOCUMENTATION_SUMMARY.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-SUMMARY-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_DocSummary
     ---
     ```

4. **Content Structure**
   ```markdown
   # Documentation Summary - <SystemName>

   ## Executive Summary

   [2-3 paragraph summary of key findings and recommendations]

   ## Discovery Statistics

   | Metric | Count |
   |--------|-------|
   | Materials Analyzed | [N] files |
   | Personas Identified | [N] |
   | Pain Points Found | [N] total |
   | - Critical (P0) | [N] |
   | - High (P1) | [N] |
   | - Medium (P2) | [N] |
   | Jobs To Be Done | [N] |
   | Features Defined | [N] |
   | Screens Specified | [N] |
   | Data Entities | [N] |

   ## Traceability Coverage

   | Chain | Items | Coverage |
   |-------|-------|----------|
   | Pain Point → JTBD | [N]/[N] | [N]% |
   | JTBD → Feature | [N]/[N] | [N]% |
   | Feature → Screen | [N]/[N] | [N]% |
   | **P0 End-to-End** | [N]/[N] | **[N]%** |

   ## Key Findings

   ### Critical Pain Points
   [Summary of P0 pain points and their business impact]

   ### User Needs
   [Summary of primary user needs from personas and JTBDs]

   ### Strategic Recommendations
   [Key recommendations from strategy documents]

   ## Deliverables Summary

   ### Phase 1 Scope
   - [N] screens
   - [N] features
   - Addresses [N] P0 pain points

   ### Full Roadmap
   - Phase 1: Foundation
   - Phase 2: Core Experience
   - Phase 3: Advanced Features

   ## Success Criteria

   | KPI | Target |
   |-----|--------|
   | [North Star Metric] | [Target] |
   | [Key KPI 1] | [Target] |
   | [Key KPI 2] | [Target] |

   ## Risks & Mitigations

   | Risk | Impact | Mitigation |
   |------|--------|------------|
   | [Risk 1] | High | [Mitigation] |
   | [Risk 2] | Medium | [Mitigation] |

   ## Data Gaps

   [List any missing information or areas needing further research]

   ## Next Steps

   1. Review and approve discovery documentation
   2. Proceed to Prototype stage
   3. Begin design implementation

   ## Document Inventory

   | Folder | Files | Status |
   |--------|-------|--------|
   | 00-management | [N] | ✅ Complete |
   | 01-analysis | [N] | ✅ Complete |
   | 02-research | [N] | ✅ Complete |
   | 03-strategy | [N] | ✅ Complete |
   | 04-design-specs | [N] | ✅ Complete |
   | 05-documentation | [N] | ✅ Complete |
   | **Total** | **[N]** | **✅ Complete** |
   ```

## Quality Checklist

- [ ] Statistics accurate from registries
- [ ] Traceability coverage calculated
- [ ] Key findings highlighted
- [ ] Risks identified
- [ ] Next steps clear

## Outputs

- `ClientAnalysis_<SystemName>/05-documentation/DOCUMENTATION_SUMMARY.md`

### Step 5: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST

echo "✅ Logged command completion"
```

## Next Command

- Run `/discovery-getting-started` for onboarding guide
- Or run `/discovery-docs-all` for all documentation
