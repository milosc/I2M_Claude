---
name: discovery-init
description: Initialize Discovery session folder structure and state files
argument-hint: <SystemName> <InputPath>
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-init started '{"stage": "discovery"}'
  Stop:
    - hooks:
        # VALIDATION: Check discovery config was created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "_state"
            --requires "discovery_config.json"
        # VALIDATION: Check discovery progress was created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "_state"
            --requires "discovery_progress.json"
        # VALIDATION: Check output folder structure was created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$1"
            --requires "00-management"
        # VALIDATION: Check traceability folder was initialized
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "traceability"
            --requires "trace_matrix.json"
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-init ended '{"stage": "discovery", "validated": true}'
---


# /discovery-init - Initialize Discovery Session

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-init instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- `$ARGUMENTS` - Required: `<SystemName> <InputPath>` where:
  - `<SystemName>` - Name of the system being analyzed (e.g., InventorySystem)
  - `<InputPath>` - Path to folder containing raw client materials

## Prerequisites

- Raw client materials exist at `<InputPath>`
- No active discovery session at same output path

## Skills Used

- `.claude/skills/Discovery_Orchestrator/Discovery_Orchestrator.md` - Read for folder structure and state file templates

## Execution Steps

1. **Parse Arguments**
   - Extract `<SystemName>` from first argument
   - Extract `<InputPath>` from second argument
   - Validate `<InputPath>` exists and contains files

2. **Create Shared State Folder** (at project root)
   ```
   _state/
   ```

3. **Create Shared Traceability Folder** (at project root)
   ```
   traceability/
   traceability/feedback_sessions/
   ```

4. **Create Discovery Output Folder**
   ```
   ClientAnalysis_<SystemName>/
   ├── 00-management/
   ├── 01-analysis/
   ├── 02-research/
   ├── 03-strategy/
   │   └── battlecards/           # CP-6.5: Per-competitor sales enablement
   ├── 04-design-specs/
   └── 05-documentation/
   ```

5. **Initialize Pipeline Config** (`_state/pipeline_config.json`)
   ```json
   {
     "project_name": "<SystemName>",
     "project_root": "<current_directory>",
     "created_at": "<ISO_timestamp>",
     "updated_at": "<ISO_timestamp>",
     "stages": {
       "stage_0_materials": "<InputPath>",
       "stage_1_discovery": "ClientAnalysis_<SystemName>/",
       "stage_2_prototype": "Prototype_<SystemName>/",
       "stage_3_specs": "Specifications_<SystemName>/",
       "stage_4_architecture": "Architecture_<SystemName>/"
     },
     "current_stage": "discovery",
     "skills_path": ".claude/skills"
   }
   ```

6. **Initialize Discovery Config** (`_state/discovery_config.json`)
   ```json
   {
     "system_name": "<SystemName>",
     "input_path": "<InputPath>",
     "output_path": "ClientAnalysis_<SystemName>/",
     "created_at": "<ISO_timestamp>",
     "updated_at": "<ISO_timestamp>",
     "status": "in_progress",
     "current_phase": 0,
     "current_checkpoint": "discovery-init"
   }
   ```

7. **Initialize Progress Tracker** (`_state/discovery_progress.json`)
   ```json
   {
     "phases": {
       "0_init": { "status": "complete", "started": "<timestamp>", "completed": "<timestamp>" },
       "1_analyze": { "status": "pending" },
       "1.5_pdf_analysis": { "status": "pending" },
       "2_extract": { "status": "pending" },
       "3_personas": { "status": "pending" },
       "4_jtbd": { "status": "pending" },
       "5_vision": { "status": "pending" },
       "6_strategy": { "status": "pending" },
       "6.5_competitive_intelligence": { "status": "pending" },
       "7_roadmap": { "status": "pending" },
       "8_kpis": { "status": "pending" },
       "9_specs": { "status": "pending" },
       "10_docs": { "status": "pending" },
       "11_validate": { "status": "pending" }
     },
     "overall_progress": 7,
     "last_checkpoint": "discovery-init",
     "resumable_from": "1_analyze"
   }
   ```

8. **Initialize Context Memory** (`_state/discovery_context.json`)
   ```json
   {
     "session_history": [
       { "session_id": "sess_001", "started": "<timestamp>", "checkpoint": "discovery-init" }
     ],
     "key_decisions": [],
     "unresolved_items": [],
     "resumption_context": "Discovery initialized. Ready to analyze materials."
   }
   ```

9. **Initialize Materials Inventory** (`_state/discovery_materials_inventory.json`)
   - List all files in `<InputPath>`
   - Categorize by type (interviews, audio/video, documents, spreadsheets, screenshots, unsupported)
   - Set all processing_status to "pending"

10. **Initialize Error Log** (`_state/discovery_error_log.md`)
    ```markdown
    # Discovery Error Log

    | Timestamp | Phase | File/Item | Error | Action Taken |
    |-----------|-------|-----------|-------|--------------|
    ```

11. **Initialize Empty Traceability Registries**
    - `traceability/<SystemName>_version_history.json` - Use `version_history.init.json` template
    - `traceability/trace_matrix.json` - Empty chains array
    - `traceability/client_facts_registry.json` - Empty items array
    - `traceability/pain_point_registry.json` - Empty items array
    - `traceability/user_type_registry.json` - Empty items array
    - `traceability/jtbd_registry.json` - Empty items array
    - `traceability/requirements_registry.json` - Empty items array
    - `traceability/screen_registry.json` - Empty items array

12. **Create Initial Progress Tracker** (`ClientAnalysis_<SystemName>/00-management/PROGRESS_TRACKER.md`)
    - Use Discovery_Orchestrator template
    - Include version metadata

## State Updates

### Created in `_state/`:
- `pipeline_config.json`
- `discovery_config.json`
- `discovery_progress.json`
- `discovery_context.json`
- `discovery_materials_inventory.json`
- `discovery_error_log.md`

### Created in `traceability/`:
- `trace_matrix.json`
- `client_facts_registry.json`
- `pain_point_registry.json`
- `user_type_registry.json`
- `jtbd_registry.json`
- `requirements_registry.json`
- `screen_registry.json`
- `feedback_sessions/` (empty folder)

## Outputs

- `ClientAnalysis_<SystemName>/` folder structure
- `ClientAnalysis_<SystemName>/00-management/PROGRESS_TRACKER.md`
- All state and traceability files initialized

## Error Handling

- If `<InputPath>` doesn't exist: Error, stop execution
- If output folder already exists: Warn user, suggest `/discovery-reset`
- If state files already exist: Warn user, suggest `/discovery-resume` or `/discovery-reset`

## Next Command

After `/discovery-init`:
- Run `/discovery-analyze` to process materials and extract insights
- Or run `/discovery` to continue full orchestration
