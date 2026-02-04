---
name: discovery-index
description: Generate Discovery master index and navigation
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-index started '{"stage": "discovery"}'
  Stop:
    - hooks:
        # VALIDATION: Check INDEX.md was created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/05-documentation"
            --requires "INDEX.md"
        # VALIDATION: Check INDEX has required sections
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_file_contains.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/05-documentation"
            --pattern "INDEX.md"
            --contains "## Quick Navigation"
            --contains "## Document Map"
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-index ended '{"stage": "discovery", "validated": true}'
---


# /discovery-index - Generate Documentation Index

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-index instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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
- All documentation folders have content

## Skills Used

- `.claude/skills/Discovery_DocIndex/Discovery_DocIndex.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path, system_name
   - Inventory all files in `ClientAnalysis_<SystemName>/`

2. **Read Discovery_DocIndex Skill**
   - Understand index structure
   - Review navigation format

3. **Generate Index Document**
   - Create `05-documentation/INDEX.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-INDEX-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_DocIndex
     source_files:
       - ClientAnalysis_<SystemName>/**/*
     ---
     ```

4. **Content Structure**
   ```markdown
   # Documentation Index - <SystemName>

   ## Quick Navigation

   | Document | Purpose | Audience |
   |----------|---------|----------|
   | [README](README.md) | Project overview | All |
   | [GETTING_STARTED](GETTING_STARTED.md) | Where to begin | New readers |
   | [DOCUMENTATION_SUMMARY](DOCUMENTATION_SUMMARY.md) | Executive summary | Stakeholders |

   ## Document Map

   ### 00-management/
   Project management and tracking documents.

   | Document | Description |
   |----------|-------------|
   | [PROGRESS_TRACKER](../00-management/PROGRESS_TRACKER.md) | Discovery progress status |

   ### 01-analysis/
   Analysis outputs from client materials.

   | Document | Description |
   |----------|-------------|
   | [ANALYSIS_SUMMARY](../01-analysis/ANALYSIS_SUMMARY.md) | Consolidated analysis findings |

   ### 02-research/
   User research and persona documentation.

   | Document | Description |
   |----------|-------------|
   | [Personas](../02-research/) | User persona profiles |
   | - [persona-<role-1>](../02-research/persona-<role-1>.md) | [Role 1 description] |
   | - [persona-<role-2>](../02-research/persona-<role-2>.md) | [Role 2 description] |
   | [JTBD](../02-research/jtbd-jobs-to-be-done.md) | Jobs to be done analysis |

   ### 03-strategy/
   Product strategy and roadmap.

   | Document | Description |
   |----------|-------------|
   | [Product Vision](../03-strategy/product-vision.md) | Vision statement and goals |
   | [Product Strategy](../03-strategy/product-strategy.md) | Strategic pillars |
   | [Product Roadmap](../03-strategy/product-roadmap.md) | Phased delivery plan |
   | [KPIs and Goals](../03-strategy/kpis-and-goals.md) | Success metrics |

   ### 04-design-specs/
   Technical specifications for implementation.

   | Document | Description |
   |----------|-------------|
   | [Screen Definitions](../04-design-specs/screen-definitions.md) | UI screen specifications |
   | [Navigation Structure](../04-design-specs/navigation-structure.md) | Site map and flows |
   | [Data Fields](../04-design-specs/data-fields.md) | Data model specification |
   | [Sample Data](../04-design-specs/sample-data.json) | Test data for prototyping |
   | [UI Components](../04-design-specs/ui-components.md) | Component library |
   | [Interaction Patterns](../04-design-specs/interaction-patterns.md) | UX patterns |

   ### 05-documentation/
   Project documentation and guides.

   | Document | Description |
   |----------|-------------|
   | [INDEX](INDEX.md) | This document |
   | [README](README.md) | Project overview |
   | [DOCUMENTATION_SUMMARY](DOCUMENTATION_SUMMARY.md) | Executive summary |
   | [GETTING_STARTED](GETTING_STARTED.md) | Onboarding guide |
   | [FILES_CREATED](FILES_CREATED.md) | Complete file list |
   | [VALIDATION_REPORT](VALIDATION_REPORT.md) | Quality validation |

   ## Traceability Documents

   Located at project root in `traceability/`:

   | Document | Description |
   |----------|-------------|
   | [TRACEABILITY_MATRIX_MASTER](../../traceability/TRACEABILITY_MATRIX_MASTER.md) | End-to-end traceability |
   | trace_matrix.json | Machine-readable trace data |
   | *_registry.json | Entity registries |

   ## Reading Order

   ### For Stakeholders
   1. DOCUMENTATION_SUMMARY
   2. Product Vision
   3. Product Roadmap
   4. KPIs and Goals

   ### For Designers
   1. Personas
   2. Screen Definitions
   3. UI Components
   4. Interaction Patterns

   ### For Developers
   1. GETTING_STARTED
   2. Data Fields
   3. Screen Definitions
   4. Sample Data
   ```

## Quality Checklist

- [ ] All files in project listed
- [ ] Links are valid relative paths
- [ ] Audience-specific reading orders
- [ ] Traceability documents referenced

## Outputs

- `ClientAnalysis_<SystemName>/05-documentation/INDEX.md`

## Next Command

- Run `/discovery-readme` for README
- Or run `/discovery-docs-all` for all documentation
