---
name: discovery-getting-started
description: Generate Discovery getting started guide
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-getting-started started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-getting-started ended '{"stage": "discovery"}'
---


# /discovery-getting-started - Generate Getting Started Guide

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-getting-started instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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
- INDEX.md exists

## Skills Used

- `.claude/skills/Discovery_DocSummary/Discovery_DocSummary.md`

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for system_name
   - Read `05-documentation/INDEX.md` for document list

2. **Read Discovery_DocSummary Skill**
   - Understand onboarding guide format

3. **Generate Getting Started Document**
   - Create `05-documentation/GETTING_STARTED.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-GETSTARTED-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_DocSummary
     ---
     ```

4. **Content Structure**
   ```markdown
   # Getting Started - <SystemName> Discovery Documentation

   ## Welcome

   This guide helps you navigate the discovery documentation for <SystemName>. Choose your path based on your role and what you need to accomplish.

   ## Quick Start (5 minutes)

   1. Read the [README](README.md) for project overview
   2. Review the [Documentation Summary](DOCUMENTATION_SUMMARY.md) for key findings
   3. Explore based on your role below

   ## Reading Paths by Role

   ### For Product Managers / Stakeholders

   **Goal**: Understand strategic direction and validate findings

   | Order | Document | Time | Purpose |
   |-------|----------|------|---------|
   | 1 | DOCUMENTATION_SUMMARY | 5 min | Executive overview |
   | 2 | Product Vision | 10 min | Strategic direction |
   | 3 | Personas (skim) | 15 min | User understanding |
   | 4 | Product Roadmap | 10 min | Delivery plan |
   | 5 | KPIs and Goals | 10 min | Success metrics |

   **Total time**: ~50 minutes

   ### For UX Designers

   **Goal**: Understand users and design requirements

   | Order | Document | Time | Purpose |
   |-------|----------|------|---------|
   | 1 | Personas (all) | 30 min | Deep user understanding |
   | 2 | JTBD | 20 min | User jobs and needs |
   | 3 | Screen Definitions | 30 min | UI requirements |
   | 4 | Navigation Structure | 15 min | Information architecture |
   | 5 | UI Components | 20 min | Component library |
   | 6 | Interaction Patterns | 15 min | UX patterns |

   **Total time**: ~2 hours

   ### For Developers / Engineers

   **Goal**: Understand technical requirements for implementation

   | Order | Document | Time | Purpose |
   |-------|----------|------|---------|
   | 1 | README | 5 min | Project overview |
   | 2 | Data Fields | 30 min | Data model |
   | 3 | Screen Definitions | 20 min | UI structure |
   | 4 | Sample Data | 10 min | Test data review |
   | 5 | Navigation Structure | 15 min | Routing requirements |
   | 6 | Interaction Patterns | 15 min | UX implementation |

   **Total time**: ~1.5 hours

   ### For QA / Testers

   **Goal**: Understand testing requirements

   | Order | Document | Time | Purpose |
   |-------|----------|------|---------|
   | 1 | ANALYSIS_SUMMARY | 15 min | Pain points context |
   | 2 | JTBD | 20 min | User scenarios |
   | 3 | Screen Definitions | 20 min | UI coverage |
   | 4 | Sample Data | 15 min | Test data |
   | 5 | Interaction Patterns | 15 min | Edge cases |
   | 6 | VALIDATION_REPORT | 10 min | Quality status |

   **Total time**: ~1.5 hours

   ## Document Overview

   ### Core Documents (Start Here)

   | Document | What You'll Learn |
   |----------|-------------------|
   | README | Project overview and structure |
   | DOCUMENTATION_SUMMARY | Key findings and statistics |
   | Product Vision | What we're building and why |

   ### User Research

   | Document | What You'll Learn |
   |----------|-------------------|
   | Personas | Who our users are |
   | JTBD | What users need to accomplish |
   | ANALYSIS_SUMMARY | Pain points and opportunities |

   ### Strategy

   | Document | What You'll Learn |
   |----------|-------------------|
   | Product Vision | Strategic direction |
   | Product Strategy | How we'll achieve the vision |
   | Product Roadmap | What we'll build and when |
   | KPIs and Goals | How we'll measure success |

   ### Technical Specifications

   | Document | What You'll Learn |
   |----------|-------------------|
   | Screen Definitions | UI layouts and features |
   | Navigation Structure | Site map and user flows |
   | Data Fields | Data model and relationships |
   | Sample Data | Example data for testing |
   | UI Components | Component specifications |
   | Interaction Patterns | UX behaviors |

   ## Finding Specific Information

   | If you need... | Go to... |
   |----------------|----------|
   | User pain points | ANALYSIS_SUMMARY, Personas |
   | Feature list | Product Roadmap |
   | Screen layouts | Screen Definitions |
   | Data structure | Data Fields |
   | Test data | Sample Data (JSON) |
   | Metrics | KPIs and Goals |
   | Traceability | TRACEABILITY_MATRIX_MASTER |

   ## Traceability

   All artifacts are connected through the traceability chain:

   ```
   Pain Point → JTBD → Feature → Screen
   ```

   Find the complete traceability matrix at:
   - `traceability/TRACEABILITY_MATRIX_MASTER.md`

   ## Questions?

   If you have questions about the documentation:
   1. Check the [INDEX](INDEX.md) for all documents
   2. Review the [VALIDATION_REPORT](VALIDATION_REPORT.md) for known issues
   3. Contact the discovery team

   ## Next Steps After Discovery

   1. **Review & Approve**: Stakeholder sign-off on findings
   2. **Prototype**: Use `/prototype` command to begin Stage 2
   3. **Iterate**: Incorporate feedback as needed
   ```

## Quality Checklist

- [ ] Role-based paths defined
- [ ] Time estimates reasonable
- [ ] All key documents referenced
- [ ] Traceability explained
- [ ] Next steps clear

## Outputs

- `ClientAnalysis_<SystemName>/05-documentation/GETTING_STARTED.md`

## Next Command

- Run `/discovery-files-created` for file list
- Or run `/discovery-docs-all` for all documentation
