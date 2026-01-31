---
description: Resume Solution Architecture generation from last completed checkpoint
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-resume started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-resume ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-resume instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

This command resumes Solution Architecture generation from where it left off, automatically detecting the current checkpoint and continuing from there.

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` (auto-detected from config if not provided)

## Usage

```bash
/solarch-resume
/solarch-resume InventorySystem
```

## Prerequisites

- `_state/solarch_config.json` must exist
- `_state/solarch_progress.json` must exist
- At least checkpoint 0 (init) must be completed

## Execution Steps

### Step 1: Execute

```
DETECT system:
  IF $ARGUMENTS provided:
    SYSTEM_NAME = $ARGUMENTS
  ELSE IF _state/solarch_config.json exists:
    LOAD config
    SYSTEM_NAME = config.system_name
  ELSE:
    ERROR "No active Solution Architecture session found"
    SUGGEST: "/solarch <SystemName> to start new session"
    RETURN

LOAD _state/solarch_progress.json

VALIDATE state:
  IF progress.current_checkpoint == 0 AND phases.init.status != "completed":
    ERROR "Session not initialized"
    SUGGEST: "/solarch-init {SYSTEM_NAME}"
    RETURN

DETERMINE resume point:
  current_cp = progress.current_checkpoint

  IF phases[current_phase].status == "failed":
    resume_from = current_cp (retry failed phase)
  ELSE IF phases[current_phase].status == "completed":
    resume_from = current_cp + 1 (next phase)
  ELSE:
    resume_from = current_cp (continue current phase)

DISPLAY resume plan:
  "Resuming Solution Architecture generation"
  "System: {SYSTEM_NAME}"
  "Starting from: Checkpoint {resume_from}"
  "Remaining phases: {12 - resume_from + 1}"

EXECUTE remaining phases:
  FOR checkpoint IN [resume_from..12]:
    RUN corresponding command:
      0 → /solarch-init (already done)
      1 → /solarch-validate
      2 → /solarch-context
      3 → /solarch-strategy
      4 → /solarch-blocks
      5 → /solarch-runtime
      6 → /solarch-quality
      7 → /solarch-deploy
      8 → /solarch-decisions
      9 → /solarch-risks
      10 → /solarch-docs
      11 → /solarch-trace
      12 → /solarch-finalize

    IF checkpoint fails AND is_blocking(checkpoint):
      STOP execution
      DISPLAY blocking error
      RETURN

    IF checkpoint fails AND NOT is_blocking(checkpoint):
      LOG to FAILURES_LOG.md
      CONTINUE to next checkpoint

DISPLAY completion summary
```

### Step 2: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-resume" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Blocking Checkpoints

Resume will stop if these checkpoints fail:

| Checkpoint | Phase | Reason |
|------------|-------|--------|
| 1 | Validate Inputs | Cannot proceed without valid inputs |
| 11 | Traceability | 100% coverage required before finalization |

## Output Format

### Successful Resume

```
═══════════════════════════════════════════════════════════════
 SOLUTION ARCHITECTURE - RESUMING
═══════════════════════════════════════════════════════════════

System: InventorySystem
Previous Checkpoint: 7 (Deployment)
Resuming from: Checkpoint 8

Remaining Phases:
├─ 8: Decisions Complete
├─ 9: Risks & Technical Debt
├─ 10: Documentation
├─ 11: Traceability Validation [BLOCKING]
└─ 12: Final Validation

Executing...

───────────────────────────────────────────────────────────────
 CHECKPOINT 8: DECISIONS COMPLETE
───────────────────────────────────────────────────────────────
[Phase output...]
Quality Gate: ✅ PASSED

───────────────────────────────────────────────────────────────
 CHECKPOINT 9: RISKS & TECHNICAL DEBT
───────────────────────────────────────────────────────────────
[Phase output...]
Quality Gate: ✅ PASSED

[Continue through remaining phases...]

═══════════════════════════════════════════════════════════════
 SOLUTION ARCHITECTURE GENERATION COMPLETE
═══════════════════════════════════════════════════════════════

System: InventorySystem
Total Checkpoints: 13 (all passed)
Output: SolArch_InventorySystem/

═══════════════════════════════════════════════════════════════
```

### Resume After Failed Phase

```
═══════════════════════════════════════════════════════════════
 SOLUTION ARCHITECTURE - RESUMING
═══════════════════════════════════════════════════════════════

System: InventorySystem
Previous Status: Checkpoint 8 FAILED
Resuming from: Checkpoint 8 (retry)

Last Error:
├─ Phase: decisions
├─ Error: ADR-007 missing traceability section
└─ Time: 2025-12-22T11:15:00Z

Retrying Checkpoint 8...

───────────────────────────────────────────────────────────────
 CHECKPOINT 8: DECISIONS COMPLETE (RETRY)
───────────────────────────────────────────────────────────────
[Phase output...]
Quality Gate: ✅ PASSED

Continuing to next checkpoint...

═══════════════════════════════════════════════════════════════
```

### Resume Blocked

```
═══════════════════════════════════════════════════════════════
 SOLUTION ARCHITECTURE - RESUME BLOCKED
═══════════════════════════════════════════════════════════════

System: InventorySystem
Blocked at: Checkpoint 11 (Traceability) [BLOCKING]

Issue:
├─ Pain Point Coverage: 80% (required: 100%)
├─ Missing: PP-3.2, PP-4.1
└─ P0 Requirement Coverage: 93% (required: 100%)

To Fix:
1. Update ADRs to reference missing pain points
2. Add traceability to ADR-005 or ADR-007
3. Re-run: /solarch-trace InventorySystem

Or reset and regenerate decisions:
  /solarch-reset --phase 8 InventorySystem

═══════════════════════════════════════════════════════════════
```

### No Session Found

```
═══════════════════════════════════════════════════════════════
 SOLUTION ARCHITECTURE - NO SESSION
═══════════════════════════════════════════════════════════════

No active Solution Architecture session found.

To start a new session:
  /solarch <SystemName>

Or initialize manually:
  /solarch-init <SystemName>

═══════════════════════════════════════════════════════════════
```

## State Recovery

If state files are corrupted or missing:

```
ATTEMPT state recovery:
  IF _state/solarch_progress.json missing BUT SolArch_{name}/ exists:
    SCAN folder structure
    DETERMINE highest completed checkpoint from files
    RECREATE progress.json

  IF _state/solarch_config.json missing:
    DETECT system name from folder: SolArch_*/
    RECREATE config.json with defaults

  DISPLAY:
    "State recovered from folder structure"
    "Detected checkpoint: {N}"
    "Verify with /solarch-status before continuing"
```

## Error Handling

| Error | Action |
|-------|--------|
| No session found | Suggest `/solarch <SystemName>` |
| Corrupted state | Attempt recovery from folder structure |
| Blocking checkpoint failed | Stop, display fix instructions |
| Non-blocking failure | Log, continue to next checkpoint |

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch-status` | Check current state before resume |
| `/solarch-reset` | Reset to specific checkpoint |
| `/solarch` | Start fresh generation |
