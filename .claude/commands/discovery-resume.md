---
name: discovery-resume
description: Resume Discovery analysis from last completed checkpoint
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-resume started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-resume ended '{"stage": "discovery"}'
---


# /discovery-resume - Resume Discovery from Checkpoint

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-resume instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

None required - reads state from `_state/discovery_progress.json`

## Prerequisites

- Previous discovery session started
- `_state/discovery_config.json` exists
- `_state/discovery_progress.json` exists with checkpoint

## Skills Used

- `.claude/skills/Discovery_Orchestrator/Discovery_Orchestrator.md` - For phase execution

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for configuration
   - Read `_state/discovery_progress.json` for last checkpoint
   - Read `_state/discovery_context.json` for resumption context

2. **Display Current State**
   ```
   Discovery Session: <SystemName>
   Status: <Paused/In Progress>
   Last Checkpoint: <checkpoint name>
   Progress: <N>%
   Resumable From: <phase>

   Last Session Context:
   <resumption_context from discovery_context.json>
   ```

3. **Determine Resume Point**
   - Find `resumable_from` in progress.json
   - Map to appropriate command:
     | resumable_from | Command to Run |
     |----------------|----------------|
     | 1_analyze | /discovery-analyze |
     | 2_extract | /discovery-analyze |
     | 3_personas | /discovery-research |
     | 4_jtbd | /discovery-research |
     | 5_vision | /discovery-strategy-all |
     | 6_strategy | /discovery-strategy-all |
     | 7_roadmap | /discovery-strategy-all |
     | 8_kpis | /discovery-strategy-all |
     | 9_specs | /discovery-specs-all |
     | 10_docs | /discovery-docs-all |
     | 11_validate | /discovery-validate |

4. **Update Session Context**
   - Add new session entry to `discovery_context.json`
   - Update `discovery_config.json` status to "in_progress"

5. **Resume Execution**
   - Run the appropriate phase command
   - Continue through remaining phases to completion

## Example Output

```
Resuming Discovery Session
==========================

System: InventorySystem
Last Checkpoint: discovery-research
Progress: 33%
Phases Complete: 0_init, 1_analyze, 2_extract, 3_personas

Resumption Context:
"Last session completed persona generation. Ready to generate JTBD document."

Resuming from phase 4_jtbd...
Running /discovery-research (continuing from JTBD)...
```

## State Updates

### Updated in `_state/`:
- `discovery_config.json` - status: "in_progress", updated_at
- `discovery_context.json` - new session entry added
- `discovery_progress.json` - updated as phases complete

## Error Handling

- No state files found: Suggest `/discovery-init`
- Already complete: Suggest `/discovery-reset` to start fresh
- Invalid checkpoint: Reset to last valid phase

## Recovery Options

If state is corrupted:
1. Use `/discovery-status` to view current state
2. Use `/discovery-reset` to start fresh
3. Manually edit `_state/discovery_progress.json` to set checkpoint

## Outputs

- Resumes discovery from checkpoint
- Continues through completion
- Updates all state files

## Next Command

After resume completes:
- Check `/discovery-status` to verify completion
- Run `/discovery-validate` if not auto-run
- Use `/discovery-export` to package for Prototype
