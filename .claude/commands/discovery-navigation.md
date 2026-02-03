---
name: discovery-navigation
description: Generate navigation structure from discovery materials
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-navigation started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-navigation ended '{"stage": "discovery"}'
---


# /discovery-navigation - Generate Navigation Structure Document

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-navigation instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- Screen definitions exist
- `04-design-specs/screen-definitions.md` exists
- `traceability/screen_registry.json` populated

## Skills Used

- `.claude/skills/Discovery_SpecNavigation/Discovery_SpecNavigation.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read `04-design-specs/screen-definitions.md` for screens
   - Read `02-research/persona-*.md` for user journeys
   - Read `traceability/screen_registry.json`

2. **Read Discovery_SpecNavigation Skill**
   - Understand navigation hierarchy format
   - Review user flow documentation

3. **Generate Navigation Document**
   - Create `04-design-specs/navigation-structure.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-NAV-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_SpecNavigation
     source_files:
       - 04-design-specs/screen-definitions.md
       - traceability/screen_registry.json
     ---
     ```

4. **Content Structure**
   ```markdown
   # Navigation Structure - <SystemName>

   ## Site Map

   ```
   Root
   ├── Dashboard (S-1.1)
   │   └── Quick Actions
   ├── [Module 1]
   │   ├── List View (S-1.2)
   │   ├── Detail View (S-1.3)
   │   └── Form (S-1.4)
   ├── [Module 2]
   │   ├── ...
   └── Settings
       ├── Profile
       └── Preferences
   ```

   ## Primary Navigation

   | Position | Label | Target Screen | Icon | Permissions |
   |----------|-------|---------------|------|-------------|
   | 1 | Dashboard | S-1.1 | home | All |
   | 2 | [Module] | S-1.2 | list | Role-based |

   ## Secondary Navigation

   | Context | Items | Behavior |
   |---------|-------|----------|
   | [Module] List | Detail, Edit, Delete | Contextual |

   ## User Flows

   ### Flow 1: [Primary Task Name]
   **Persona**: [Primary persona]
   **Goal**: [What user wants to accomplish]
   **Entry Point**: [Starting screen]

   ```mermaid
   graph LR
   A[S-1.1 Dashboard] --> B[S-1.2 List]
   B --> C[S-1.3 Detail]
   C --> D[S-1.4 Edit]
   D --> E{Save?}
   E -->|Yes| C
   E -->|No| C
   ```

   | Step | Screen | Action | Next |
   |------|--------|--------|------|
   | 1 | S-1.1 | Click [Action] | S-1.2 |
   | 2 | S-1.2 | Select item | S-1.3 |
   | 3 | S-1.3 | Click Edit | S-1.4 |
   | 4 | S-1.4 | Submit form | S-1.3 |

   ### Flow 2: [Secondary Task Name]
   ...

   ## Breadcrumb Structure

   | Screen | Breadcrumb Trail |
   |--------|------------------|
   | S-1.1 | Home |
   | S-1.2 | Home > [Module] |
   | S-1.3 | Home > [Module] > [Item] |
   | S-1.4 | Home > [Module] > [Item] > Edit |

   ## Navigation States

   | State | Behavior | Visual Indicator |
   |-------|----------|------------------|
   | Active | Highlighted | Bold + accent color |
   | Disabled | Not clickable | Grayed out |
   | Has Notification | Badge | Red dot |

   ## Deep Linking

   | Pattern | Screen | Example |
   |---------|--------|---------|
   | /dashboard | S-1.1 | /dashboard |
   | /[module] | S-1.2 | /inventory |
   | /[module]/:id | S-1.3 | /inventory/123 |
   | /[module]/:id/edit | S-1.4 | /inventory/123/edit |

   ## Mobile Navigation

   ### Bottom Navigation
   | Position | Icon | Screen |
   |----------|------|--------|
   | 1 | home | Dashboard |
   | 2 | ... | ... |

   ### Hamburger Menu
   [Items that appear in mobile menu]
   ```

## Quality Checklist

- [ ] All screens reachable via navigation
- [ ] Critical user flows documented
- [ ] Breadcrumb structure complete
- [ ] Mobile navigation considered
- [ ] Deep linking patterns defined

## Outputs

- `ClientAnalysis_<SystemName>/04-design-specs/navigation-structure.md`

## Next Command

- Run `/discovery-data-fields` for data model
- Or run `/discovery-specs-all` for all spec documents
