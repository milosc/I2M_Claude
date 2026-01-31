---
description: Generate interaction patterns from discovery materials
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-interactions started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-interactions ended '{"stage": "discovery"}'
---


# /discovery-interactions - Generate Interaction Patterns Document

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-interactions instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- Screen definitions and components exist
- `04-design-specs/screen-definitions.md` exists
- `04-design-specs/ui-components.md` exists

## Skills Used

- `.claude/skills/Discovery_SpecInteractions/Discovery_SpecInteractions.md` - CRITICAL: Read entire skill

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read `04-design-specs/screen-definitions.md` for screen actions
   - Read `04-design-specs/ui-components.md` for component interactions

2. **Read Discovery_SpecInteractions Skill**
   - Understand interaction pattern format
   - Review micro-interaction documentation

3. **Generate Interactions Document**
   - Create `04-design-specs/interaction-patterns.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-INTERACTIONS-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_SpecInteractions
     source_files:
       - 04-design-specs/screen-definitions.md
       - 04-design-specs/ui-components.md
     ---
     ```

4. **Content Structure**
   ```markdown
   # Interaction Patterns - <SystemName>

   ## Interaction Principles
   - Immediate feedback for all actions
   - Optimistic updates where safe
   - Clear loading states
   - Graceful error handling
   - Undo support for destructive actions

   ## Core Interactions

   ### Click/Tap Actions

   | Action | Trigger | Response | Feedback |
   |--------|---------|----------|----------|
   | Navigate | Menu click | Route change | Highlight active |
   | Submit | Button click | API call | Loading state |
   | Select | Row click | Selection | Visual highlight |
   | Open modal | Button click | Modal appears | Overlay |

   ### Hover Interactions

   | Element | Hover Effect | Purpose |
   |---------|--------------|---------|
   | Button | Slight lift/color | Affordance |
   | Row | Background change | Selection hint |
   | Link | Underline | Clickable hint |
   | Icon | Tooltip | Information |

   ### Drag & Drop

   | Context | Draggable | Drop Target | Visual Feedback |
   |---------|-----------|-------------|-----------------|
   | List reorder | Row | Between rows | Ghost + line |
   | File upload | File | Upload zone | Border highlight |

   ## Form Interactions

   ### Field Validation

   | Timing | Behavior |
   |--------|----------|
   | On blur | Validate single field |
   | On change | Clear error if corrected |
   | On submit | Validate all fields |

   ### Validation Feedback

   | State | Visual | Timing |
   |-------|--------|--------|
   | Error | Red border + message | Immediate |
   | Success | Green checkmark | After valid |
   | Loading | Spinner | During async validation |

   ### Form Submission

   ```
   User clicks Submit
       ↓
   Disable button + show spinner
       ↓
   Validate all fields
       ↓
   [Valid?] → No → Show errors, re-enable
       ↓ Yes
   Make API call
       ↓
   [Success?] → No → Show error toast, re-enable
       ↓ Yes
   Show success toast
       ↓
   Navigate or update UI
   ```

   ## Loading States

   ### Full Page Loading
   - Skeleton screens for initial load
   - Maintain layout structure
   - Animate to indicate progress

   ### Component Loading
   | Component | Loading State |
   |-----------|---------------|
   | DataTable | Skeleton rows |
   | Card | Pulse animation |
   | Button | Spinner icon |
   | Image | Placeholder + fade |

   ### Async Actions
   | Action | Optimistic | Rollback |
   |--------|------------|----------|
   | Create | Add to list | Remove on error |
   | Update | Update UI | Revert on error |
   | Delete | Remove from list | Restore on error |

   ## Error Handling

   ### Error Categories

   | Type | Display | Recovery |
   |------|---------|----------|
   | Validation | Inline | Fix and retry |
   | Network | Toast | Retry button |
   | Server | Modal | Contact support |
   | Permission | Modal | Request access |

   ### Error States

   ```markdown
   #### Empty State
   - Illustration
   - Helpful message
   - Call to action

   #### Error State
   - Error icon
   - Clear message
   - Recovery action

   #### Offline State
   - Offline indicator
   - Cached data access
   - Sync when online
   ```

   ## Transitions & Animations

   ### Page Transitions
   | Transition | Duration | Easing |
   |------------|----------|--------|
   | Page enter | 200ms | ease-out |
   | Page exit | 150ms | ease-in |
   | Modal open | 250ms | ease-out |
   | Modal close | 200ms | ease-in |

   ### Micro-interactions
   | Element | Animation | Duration |
   |---------|-----------|----------|
   | Button press | Scale down | 100ms |
   | Toast appear | Slide up | 200ms |
   | Checkbox | Check mark draw | 150ms |
   | Accordion | Height expand | 200ms |

   ## Keyboard Navigation

   ### Global Shortcuts
   | Shortcut | Action |
   |----------|--------|
   | / | Focus search |
   | Esc | Close modal/menu |
   | ? | Show help |

   ### Focus Management
   | Context | Behavior |
   |---------|----------|
   | Modal open | Focus first input |
   | Modal close | Return to trigger |
   | Form error | Focus first error |

   ## Responsive Behavior

   ### Touch Adaptations
   | Desktop | Mobile |
   |---------|--------|
   | Hover states | Tap feedback |
   | Right-click menu | Long press |
   | Tooltips | Info icons |

   ### Breakpoint Transitions
   | Breakpoint | Layout Change |
   |------------|---------------|
   | < 768px | Stack layout |
   | 768-1024px | Condensed nav |
   | > 1024px | Full layout |
   ```

## Quality Checklist

- [ ] All user actions have defined feedback
- [ ] Loading states for async operations
- [ ] Error handling for all scenarios
- [ ] Keyboard navigation supported
- [ ] Mobile interactions considered
- [ ] Animation timings appropriate

## Outputs

- `ClientAnalysis_<SystemName>/04-design-specs/interaction-patterns.md`

## Next Command

- Run `/discovery-index` for documentation index
- Or run `/discovery-docs-all` for all documentation
