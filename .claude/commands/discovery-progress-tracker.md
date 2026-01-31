---
description: Display Discovery checkpoint progress and completion status
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-progress-tracker started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-progress-tracker ended '{"stage": "discovery"}'
---


# /discovery-progress-tracker - Generate Progress Tracker

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-progress-tracker instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- `/discovery-init` completed
- `_state/discovery_config.json` exists
- `_state/discovery_progress.json` exists

## Skills Used

- `.claude/skills/Discovery_Orchestrator/Discovery_Orchestrator.md` - PROGRESS_TRACKER template

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path, system_name
   - Read `_state/discovery_progress.json` for phase statuses

2. **Generate Progress Tracker**
   - Create `ClientAnalysis_<SystemName>/00-management/PROGRESS_TRACKER.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-PROGRESS-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_Orchestrator
     ---
     ```
   - Show phase completion status
   - Display overall progress percentage
   - List completed outputs
   - Note any skipped files from error log

3. **Content Structure**
   ```markdown
   # Discovery Progress Tracker

   **System**: <SystemName>
   **Status**: <In Progress | Complete>
   **Progress**: <N>%

   ## Phase Status

   | Phase | Status | Started | Completed |
   |-------|--------|---------|-----------|
   | 0. Init | ✅ | ... | ... |
   | 1. Analyze | ⏳/✅ | ... | ... |
   ...

   ## Files Generated
   - [List of generated files with status]

   ## Skipped Items
   - [From error log, if any]
   ```

## Outputs

- `ClientAnalysis_<SystemName>/00-management/PROGRESS_TRACKER.md`

## Next Command

- Continue with next discovery phase command
