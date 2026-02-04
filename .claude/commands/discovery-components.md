---
name: discovery-components
description: Generate component specifications from discovery materials
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
skills:
  required:
    - Discovery_SpecComponents
  optional:
    - ui-design-system
    - tailwind-patterns
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-components started '{"stage": "discovery"}'
  Stop:
    - hooks:
        # VALIDATION: Check ui-components document was created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/04-design-specs"
            --requires "ui-components.md"
        # VALIDATION: Check components has required sections
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_file_contains.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/04-design-specs"
            --pattern "ui-components.md"
            --contains "## Components"
            --contains "### Props"
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-components ended '{"stage": "discovery", "validated": true}'
---


# /discovery-components - Generate UI Components Document

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-components instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- `.claude/skills/Discovery_SpecComponents/Discovery_SpecComponents.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read `04-design-specs/screen-definitions.md` for component needs
   - Read `traceability/screen_registry.json`

2. **Read Discovery_SpecComponents Skill**
   - Understand component specification format
   - Review variant documentation

3. **Generate Components Document**
   - Create `04-design-specs/ui-components.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-COMPONENTS-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_SpecComponents
     source_files:
       - 04-design-specs/screen-definitions.md
       - traceability/screen_registry.json
     ---
     ```

4. **Content Structure**
   ```markdown
   # UI Components - <SystemName>

   ## Component Inventory

   | Category | Component | Screens Used | Priority |
   |----------|-----------|--------------|----------|
   | Layout | AppShell | All | P0 |
   | Navigation | Sidebar | All | P0 |
   | Data Display | DataTable | S-1.2, S-2.1 | P0 |
   | Forms | TextInput | S-1.4, S-2.2 | P0 |

   ## Layout Components

   ### AppShell
   **Purpose**: Main application layout wrapper
   **Used In**: All screens

   #### Structure
   ```
   +-------------------------------------------+
   |  Header (fixed)                           |
   +-------------------------------------------+
   |  Sidebar  |  Main Content                 |
   |  (fixed)  |  (scrollable)                 |
   |           |                               |
   +-------------------------------------------+
   ```

   #### Props
   | Prop | Type | Required | Default | Description |
   |------|------|----------|---------|-------------|
   | header | ReactNode | Yes | - | Header content |
   | sidebar | ReactNode | No | - | Sidebar content |
   | children | ReactNode | Yes | - | Main content |

   #### Variants
   | Variant | Description | Use Case |
   |---------|-------------|----------|
   | with-sidebar | Shows sidebar | Main app |
   | full-width | No sidebar | Auth pages |

   ## Navigation Components

   ### Sidebar
   **Purpose**: Primary navigation menu
   **Used In**: All authenticated screens

   #### Props
   | Prop | Type | Required | Description |
   |------|------|----------|-------------|
   | items | NavItem[] | Yes | Menu items |
   | activeItem | string | No | Current page |
   | collapsed | boolean | No | Collapsed state |

   #### States
   | State | Visual | Behavior |
   |-------|--------|----------|
   | default | Full width | Shows labels |
   | collapsed | Icon only | Tooltip on hover |
   | mobile | Hidden | Hamburger trigger |

   ## Data Display Components

   ### DataTable
   **Purpose**: Display tabular data with sorting/filtering
   **Used In**: S-1.2, S-2.1, S-3.1

   #### Props
   | Prop | Type | Required | Description |
   |------|------|----------|-------------|
   | columns | Column[] | Yes | Column definitions |
   | data | T[] | Yes | Data array |
   | sortable | boolean | No | Enable sorting |
   | filterable | boolean | No | Enable filtering |
   | pagination | boolean | No | Enable pagination |
   | selectable | boolean | No | Row selection |

   #### Features
   - [ ] Column sorting
   - [ ] Search/filter
   - [ ] Pagination
   - [ ] Row selection
   - [ ] Row actions
   - [ ] Export

   ### Card
   **Purpose**: Container for related content
   **Used In**: S-1.1, S-1.3

   #### Variants
   | Variant | Description |
   |---------|-------------|
   | default | Standard card |
   | clickable | Interactive card |
   | highlighted | Accent border |

   ## Form Components

   ### TextInput
   **Purpose**: Single-line text input
   **Used In**: All forms

   #### Props
   | Prop | Type | Required | Description |
   |------|------|----------|-------------|
   | label | string | Yes | Field label |
   | value | string | Yes | Current value |
   | onChange | function | Yes | Change handler |
   | placeholder | string | No | Placeholder text |
   | error | string | No | Error message |
   | disabled | boolean | No | Disabled state |
   | required | boolean | No | Required indicator |

   #### States
   | State | Visual |
   |-------|--------|
   | default | Standard border |
   | focused | Accent border |
   | error | Red border + message |
   | disabled | Grayed out |

   ### Select
   ...

   ### Button
   ...

   ## Feedback Components

   ### Toast
   **Purpose**: Transient notifications
   **Used In**: After actions

   #### Variants
   | Variant | Icon | Color | Use Case |
   |---------|------|-------|----------|
   | success | ✓ | Green | Action completed |
   | error | ✗ | Red | Action failed |
   | warning | ⚠ | Yellow | Needs attention |
   | info | ℹ | Blue | Information |

   ### Modal
   ...

   ## Component-Screen Matrix

   | Component | S-1.1 | S-1.2 | S-1.3 | S-1.4 |
   |-----------|-------|-------|-------|-------|
   | AppShell | ✅ | ✅ | ✅ | ✅ |
   | DataTable | - | ✅ | - | - |
   | Card | ✅ | - | ✅ | - |
   | TextInput | - | - | - | ✅ |
   ```

## Quality Checklist

- [ ] All screens have required components
- [ ] Props documented for each component
- [ ] Variants and states defined
- [ ] Accessibility considerations noted
- [ ] Component-screen mapping complete

## Outputs

- `ClientAnalysis_<SystemName>/04-design-specs/ui-components.md`

## Next Command

- Run `/discovery-interactions` for interaction patterns
- Or run `/discovery-specs-all` for all spec documents
