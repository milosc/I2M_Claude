---
name: solarch-init
description: Initialize Solution Architecture folder structure and state files
argument-hint: <SystemName>
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-init started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-init ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-init instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

Creates the output folder structure, configuration file, and progress tracking for a new Solution Architecture generation. This is Checkpoint 0 of the pipeline.

## Arguments

- `$ARGUMENTS` - Required: `<SystemName>` (e.g., InventorySystem)

## Usage

```bash
/solarch-init InventorySystem
```

## Prerequisites

- `Prototype_<SystemName>/` exists
- `ProductSpecs_<SystemName>/` exists

## Skills Used

None required - this is a structural initialization.

## Execution Steps

### Step 1: Initialize

```
SYSTEM_NAME = $ARGUMENTS[0]

IF NOT SYSTEM_NAME:
  PROMPT: "Enter system name:"
  SYSTEM_NAME = user_input

SET paths:
  PROTOTYPE_PATH = "Prototype_{SYSTEM_NAME}"
  PRODUCTSPECS_PATH = "ProductSpecs_{SYSTEM_NAME}"
  OUTPUT_PATH = "SolArch_{SYSTEM_NAME}"

VERIFY inputs exist:
  IF NOT exists(PROTOTYPE_PATH):
    ERROR: "Missing Prototype folder: {PROTOTYPE_PATH}"
  IF NOT exists(PRODUCTSPECS_PATH):
    ERROR: "Missing ProductSpecs folder: {PRODUCTSPECS_PATH}"

CREATE folder structure:
  SolArch_{SYSTEM_NAME}/
  ├── 01-introduction-goals/
  ├── 02-constraints/
  ├── 03-context-scope/
  ├── 04-solution-strategy/
  ├── 05-building-blocks/
  │   ├── modules/
  │   └── data-model/
  ├── 06-runtime/
  ├── 07-quality/
  ├── 08-deployment/
  │   └── runbooks/
  ├── 09-decisions/
  ├── 10-risks/
  ├── 11-glossary/
  ├── reports/                            # v3.0: Reports folder
  └── diagrams/
  # NOTE (v3.0): _registry/ DEPRECATED - use ROOT traceability/

CREATE _state/solarch_config.json:
  {
    "$schema": "solarch-config-v1",
    "$metadata": {
      "created_at": "ISO8601",
      "updated_at": "ISO8601",
      "version": "1.0.0"
    },
    "system_name": "{SYSTEM_NAME}",
    "prototype_path": "{PROTOTYPE_PATH}",
    "productspecs_path": "{PRODUCTSPECS_PATH}",
    "output_path": "{OUTPUT_PATH}",
    "stage": 4
  }

CREATE _state/solarch_progress.json:
  {
    "$schema": "solarch-progress-v1",
    "$metadata": {
      "created_at": "ISO8601",
      "updated_at": "ISO8601"
    },
    "current_checkpoint": 0,
    "current_phase": "init",
    "started_at": "ISO8601",
    "phases": {
      "init": { "status": "in_progress", "checkpoint": 0 },
      "validate": { "status": "pending", "checkpoint": 1 },
      "context": { "status": "pending", "checkpoint": 2 },
      "strategy": { "status": "pending", "checkpoint": 3 },
      "blocks": { "status": "pending", "checkpoint": 4 },
      "runtime": { "status": "pending", "checkpoint": 5 },
      "quality": { "status": "pending", "checkpoint": 6 },
      "deploy": { "status": "pending", "checkpoint": 7 },
      "decisions": { "status": "pending", "checkpoint": 8 },
      "risks": { "status": "pending", "checkpoint": 9 },
      "docs": { "status": "pending", "checkpoint": 10 },
      "trace": { "status": "pending", "checkpoint": 11 },
      "final": { "status": "pending", "checkpoint": 12 }
    },
    "validation_history": []
  }

INITIALIZE _registry/components.json:
  {
    "$schema": "solarch-components-v1",
    "$metadata": {
      "created_at": "ISO8601",
      "updated_at": "ISO8601"
    },
    "components": [],
    "statistics": {
      "total": 0,
      "by_type": {}
    }
  }

INITIALIZE _registry/decisions.json:
  {
    "$schema": "solarch-decisions-v1",
    "$metadata": {
      "created_at": "ISO8601",
      "updated_at": "ISO8601"
    },
    "decisions": [],
    "statistics": {
      "total": 0,
      "by_status": {}
    }
  }

INITIALIZE _registry/architecture-traceability.json:
  {
    "$schema": "architecture-traceability",
    "$metadata": {
      "created_at": "ISO8601",
      "updated_at": "ISO8601"
    },
    "chains": [],
    "coverage": {
      "painPointsCovered": 0,
      "painPointsTotal": 0,
      "requirementsCovered": 0,
      "requirementsTotal": 0,
      "modulesArchitected": 0,
      "modulesTotal": 0
    }
  }

UPDATE _state/solarch_progress.json:
  phases.init.status = "completed"
  phases.init.completed_at = NOW()

RUN quality gate:
  python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 0 --dir {OUTPUT_PATH}/

DISPLAY checkpoint 0 summary
```

### Step 2: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-init" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Output

### Folder Structure Created

```
SolArch_{SystemName}/
├── 01-introduction-goals/
├── 02-constraints/
├── 03-context-scope/
├── 04-solution-strategy/
├── 05-building-blocks/
│   ├── modules/
│   └── data-model/
├── 06-runtime/
├── 07-quality/
├── 08-deployment/
│   └── runbooks/
├── 09-decisions/
├── 10-risks/
├── 11-glossary/
├── _registry/
│   ├── components.json
│   ├── decisions.json
│   └── architecture-traceability.json
└── diagrams/
```

### State Files Created

At project ROOT level:
```
_state/
├── solarch_config.json
└── solarch_progress.json
```

## Checkpoint Validation

```bash
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 0 --dir SolArch_InventorySystem/
```

**Required for Checkpoint 0:**
- `_state/solarch_config.json` exists and valid JSON
- `_state/solarch_progress.json` exists and valid JSON
- All 11 numbered folders exist
- `_registry/` folder exists

## Output Format

```
═══════════════════════════════════════════════════════════════
 CHECKPOINT 0: INITIALIZE - COMPLETED
═══════════════════════════════════════════════════════════════

System: InventorySystem
Output Path: SolArch_InventorySystem/

Created:
├─ 11 arc42 section folders
├─ _registry/ with 3 JSON files
├─ diagrams/ folder
├─ _state/solarch_config.json
└─ _state/solarch_progress.json

Quality Gate: ✅ PASSED

Next: /solarch-validate InventorySystem
═══════════════════════════════════════════════════════════════
```

## Error Handling

| Error | Action |
|-------|--------|
| Prototype folder missing | ERROR, stop |
| ProductSpecs folder missing | ERROR, stop |
| Output folder already exists | Ask to reset or continue |
| Config file creation fails | ERROR, stop |

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch` | Full pipeline |
| `/solarch-validate` | Next phase (Checkpoint 1) |
| `/solarch-status` | Check progress |
| `/solarch-reset` | Reset and start over |
