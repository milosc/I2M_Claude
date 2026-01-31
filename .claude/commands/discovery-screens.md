---
description: Generate screen definitions from discovery materials
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-screens started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-screens ended '{"stage": "discovery"}'
---


# /discovery-screens - Generate Screen Definitions Document

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-screens instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- Roadmap exists
- `03-strategy/product-roadmap.md` exists
- `traceability/requirements_registry.json` populated

## Skills Used

- `.claude/skills/Discovery_SpecScreens/Discovery_SpecScreens.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read `03-strategy/product-roadmap.md` for Phase 1 features
   - Read `02-research/persona-*.md` for user context
   - Read `traceability/requirements_registry.json` for features

2. **Read Discovery_SpecScreens Skill**
   - Understand screen inventory structure
   - Review layout specification format

3. **Generate Screen Definitions**
   - Create `04-design-specs/screen-definitions.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-SCREENS-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_SpecScreens
     source_files:
       - 03-strategy/product-roadmap.md
       - traceability/requirements_registry.json
     ---
     ```

4. **Content Structure**
   ```markdown
   # Screen Definitions - <SystemName>

   ## Screen Inventory

   | ID | Screen Name | Type | Features | Personas | Priority |
   |----|-------------|------|----------|----------|----------|
   | S-1.1 | Dashboard | Overview | US-1.1, US-1.2 | All | P0 |
   | S-1.2 | [Name] | Form/List/Detail | ... | ... | ... |

   ## Screen Specifications

   ### S-1.1: Dashboard
   **Type**: Overview
   **Primary Persona**: [Persona]
   **Features Supported**: US-1.1, US-1.2

   #### Purpose
   [What this screen accomplishes]

   #### Layout Specification
   ```
   +--------------------------------------------------+
   |  Header                                          |
   +--------------------------------------------------+
   |  Nav  |  Main Content Area                       |
   |       |                                          |
   |       |  +----------------+ +----------------+   |
   |       |  |  Widget 1      | |  Widget 2      |   |
   |       |  +----------------+ +----------------+   |
   |       |                                          |
   +--------------------------------------------------+
   ```

   #### Components Used
   - Component 1
   - Component 2

   #### Data Displayed
   | Data Field | Source Entity | Format |
   |------------|---------------|--------|
   | ... | ... | ... |

   #### Actions Available
   | Action | Trigger | Result |
   |--------|---------|--------|
   | ... | Button click | ... |

   #### User Flow
   - Entry: [How users arrive]
   - Exit: [Where users go next]

   ### S-1.2: [Screen Name]
   ...

   ## Screen Flow Diagram

   ```mermaid
   graph TD
   A[Login] --> B[Dashboard]
   B --> C[List View]
   C --> D[Detail View]
   D --> E[Edit Form]
   ```

   ## Screen-Feature Matrix

   | Screen | US-1.1 | US-1.2 | US-1.3 | FR-1.1 |
   |--------|--------|--------|--------|--------|
   | S-1.1 | ✅ | ✅ | - | - |
   | S-1.2 | - | ✅ | ✅ | ✅ |
   ```

5. **Populate Screen Registry**
   - Update `traceability/screen_registry.json`
   - Assign hierarchical IDs: S-1.1, S-1.2, S-2.1...
   - Link to features (US-X.Y, FR-X.Y)

6. **Update Trace Matrix**
   - Add Feature → Screen links

## ID Assignment Rules

- S-X.Y where X = module/area, Y = sequence
- Example: S-1.1 (Dashboard), S-1.2 (User List), S-2.1 (Settings)

## Quality Checklist

- [ ] All Phase 1 features have associated screens
- [ ] Each screen has clear purpose and layout
- [ ] Components mapped to screens
- [ ] User flows documented

## Outputs

- `ClientAnalysis_<SystemName>/04-design-specs/screen-definitions.md`
- Updated `traceability/screen_registry.json`
- Updated `traceability/trace_matrix.json`

## Next Command

- Run `/discovery-navigation` for navigation structure
- Or run `/discovery-specs-all` for all spec documents
