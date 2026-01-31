---
description: Display current Discovery stage status and progress
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-status started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-status ended '{"stage": "discovery"}'
---


# /discovery-status - Show Discovery Progress Status

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-status instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

None required - reads state from `_state/` files

## Prerequisites

- Discovery session initialized
- `_state/discovery_config.json` exists

## Skills Used

None - utility command reading state files

## Execution Steps

1. **Check for State Files**
   - Look for `_state/discovery_config.json`
   - If not found: Report no active discovery session

2. **Load State Files**
   - Read `_state/discovery_config.json`
   - Read `_state/discovery_progress.json`
   - Read `_state/discovery_context.json`
   - Read `_state/discovery_materials_inventory.json`
   - Read `_state/discovery_error_log.md`

3. **Display Status Report**
   ```
   ╔════════════════════════════════════════════════════════════╗
   ║              DISCOVERY STATUS: <SystemName>                 ║
   ╠════════════════════════════════════════════════════════════╣
   ║ Status:        <In Progress | Complete | Paused>           ║
   ║ Progress:      ████████████░░░░░░░░ 60%                    ║
   ║ Current Phase: <phase name>                                 ║
   ║ Checkpoint:    <last checkpoint>                            ║
   ╚════════════════════════════════════════════════════════════╝

   PHASE STATUS
   ────────────────────────────────────────────────────────────
   ✅ 0. Initialize          Completed: 2025-01-15 10:00
   ✅ 1. Analyze Materials    Completed: 2025-01-15 10:30
   ✅ 2. Extract Insights     Completed: 2025-01-15 10:45
   ✅ 3. Generate Personas    Completed: 2025-01-15 11:00
   ⏳ 4. Generate JTBD        In Progress...
   ⏸️  5. Generate Vision      Pending
   ⏸️  6. Generate Strategy    Pending
   ⏸️  7. Generate Roadmap     Pending
   ⏸️  8. Generate KPIs        Pending
   ⏸️  9. Design Specs         Pending
   ⏸️  10. Documentation       Pending
   ⏸️  11. Validation          Pending

   MATERIALS PROCESSED
   ────────────────────────────────────────────────────────────
   Total Files:     15
   Processed:       12 (80%)
   Skipped:         3

   By Type:
   • Interviews:    5 files
   • Documents:     4 files
   • Spreadsheets:  2 files
   • Screenshots:   1 file
   • Skipped:       3 files (video/audio)

   TRACEABILITY STATUS
   ────────────────────────────────────────────────────────────
   Pain Points:     12 (P0: 4, P1: 5, P2: 3)
   User Types:      5
   JTBDs:           8
   Features:        0 (pending roadmap)
   Screens:         0 (pending specs)

   ERRORS/SKIPPED
   ────────────────────────────────────────────────────────────
   • manual.pdf - PDF too large
   • demo.mp4 - Unsupported media type
   • intro.mov - Unsupported media type

   CONTEXT
   ────────────────────────────────────────────────────────────
   Last Session:    2025-01-15 11:15
   Sessions:        2

   Resumption Note:
   "Completed persona generation. Ready to generate JTBD document."
   ```

4. **Show Recommended Action**
   ```
   RECOMMENDED ACTION
   ────────────────────────────────────────────────────────────
   Continue with: /discovery-resume
   Or run specific phase: /discovery-jtbd
   ```

## Output Sections

| Section | Source |
|---------|--------|
| Status Header | discovery_config.json |
| Phase Status | discovery_progress.json |
| Materials | discovery_materials_inventory.json |
| Traceability | traceability/*.json |
| Errors | discovery_error_log.md |
| Context | discovery_context.json |

## Status Indicators

| Icon | Meaning |
|------|---------|
| ✅ | Phase complete |
| ⏳ | Phase in progress |
| ⏸️ | Phase pending |
| ❌ | Phase failed |

## Error Handling

- No discovery session: Suggest `/discovery-init`
- Corrupted state: Show available data, suggest reset
- Missing files: Note what's missing

## Outputs

- Status report displayed to console
- No files modified

## Next Command

Based on status:
- If paused: `/discovery-resume`
- If complete: `/discovery-export` or `/prototype`
- If failed: Fix issues and `/discovery-resume`
