---
name: trace-audit
description: Comprehensive traceability audit orchestrator - spawns specialized agents to analyze traceability/, _state/, and all JSON registries, then consolidates findings into a unified health report and visual matrix
argument-hint: <SystemName>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /trace-audit started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /trace-audit ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /trace-audit instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# /trace-audit - Traceability Audit Orchestrator

**Version**: 1.0.0
**Purpose**: Comprehensive traceability audit with multi-agent parallel analysis

---

## Usage

```bash
/trace-audit <SystemName>                    # Full audit with visual report
/trace-audit <SystemName> --quick            # Quick health check only
/trace-audit <SystemName> --section registry # Only traceability/ folder
/trace-audit <SystemName> --section state    # Only _state/ folder
/trace-audit <SystemName> --section json     # Only JSON discovery
/trace-audit <SystemName> --json             # Output as JSON only
/trace-audit <SystemName> --no-parallel      # Run agents sequentially (debug)
```

---

## Arguments

| Argument | Description |
|----------|-------------|
| `<SystemName>` | **Required**. The system to audit (e.g., "ERTriage") |
| `--quick` | Quick health check - summary only, no visual matrix |
| `--section <name>` | Run only one section: `registry`, `state`, `json` |
| `--json` | Output results as JSON for programmatic use |
| `--no-parallel` | Run agents sequentially instead of parallel (for debugging) |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         /trace-audit ORCHESTRATOR                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PHASE 1: PARALLEL AGENT SPAWN                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                                                                      │   │
│  │  ┌─────────────────────┐  ┌─────────────────────┐  ┌──────────────┐ │   │
│  │  │ trace-audit-        │  │ trace-audit-        │  │ trace-audit- │ │   │
│  │  │ registry-scanner    │  │ state-analyzer      │  │ json-        │ │   │
│  │  │                     │  │                     │  │ discovery    │ │   │
│  │  │ Scope:              │  │ Scope:              │  │              │ │   │
│  │  │ traceability/       │  │ _state/             │  │ Scope:       │ │   │
│  │  │                     │  │                     │  │ All other    │ │   │
│  │  │ Outputs:            │  │ Outputs:            │  │ .json files  │ │   │
│  │  │ - Registry health   │  │ - Checkpoint state  │  │              │ │   │
│  │  │ - Broken links      │  │ - Session integrity │  │ Outputs:     │ │   │
│  │  │ - Orphaned IDs      │  │ - Config validity   │  │ - Shadow     │ │   │
│  │  │ - Coverage metrics  │  │ - Lifecycle events  │  │   registries │ │   │
│  │  │ - ID format issues  │  │ - Lock analysis     │  │ - Untracked  │ │   │
│  │  └─────────────────────┘  └─────────────────────┘  │   refs       │ │   │
│  │           │                        │               │ - Bypass     │ │   │
│  │           │                        │               │   chains     │ │   │
│  │           │                        │               └──────────────┘ │   │
│  │           │                        │                      │         │   │
│  └───────────┼────────────────────────┼──────────────────────┼─────────┘   │
│              │                        │                      │             │
│              ▼                        ▼                      ▼             │
│  PHASE 2: CONSOLIDATION                                                    │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     trace-audit-consolidator                         │   │
│  │                                                                      │   │
│  │  Inputs: JSON findings from all 3 scanner agents                     │   │
│  │                                                                      │   │
│  │  Processing:                                                         │   │
│  │  - Cross-validation of findings                                      │   │
│  │  - Issue deduplication                                               │   │
│  │  - Severity escalation                                               │   │
│  │  - E2E chain analysis                                                │   │
│  │  - Risk assessment                                                   │   │
│  │  - Recommendation generation                                         │   │
│  │                                                                      │   │
│  │  Outputs:                                                            │   │
│  │  - traceability/TRACEABILITY_AUDIT_REPORT.md                         │   │
│  │  - traceability/TRACEABILITY_MATRIX_MASTER.md                        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Procedure

### Step 0: Validate Input

1. **Parse arguments**
   ```bash
   SYSTEM_NAME="$1"
   OPTIONS="${@:2}"
   ```

2. **Validate system exists**
   - Check for at least one of: `ClientAnalysis_{SystemName}/`, `traceability/`
   - If neither exists, error: "No data found for system: {SystemName}"

3. **Determine mode**
   - `--quick`: Skip visual matrix generation
   - `--section`: Run only specified agent
   - `--json`: Suppress markdown output
   - `--no-parallel`: Sequential execution

---

### Step 1: Log Audit Start

```bash
EVENT_ID=$(python3 .claude/hooks/command_start.py \
  --command-name "/trace-audit" \
  --stage "utility" \
  --system-name "$SYSTEM_NAME" \
  --intent "Comprehensive traceability audit")
```

---

### Step 2: Display Audit Header

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        TRACEABILITY AUDIT                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  System: {SYSTEM_NAME}                                                       ║
║  Mode: {Full | Quick | Section: X}                                           ║
║  Timestamp: {ISO timestamp}                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

⏳ Spawning audit agents...
```

---

### Step 3: Spawn Scanner Agents (Parallel)

**IMPORTANT**: Spawn all three agents in PARALLEL using a single message with multiple Task tool calls.

If `--no-parallel` is specified, run sequentially instead.

If `--section` is specified, only spawn the relevant agent.

#### Agent 1: Registry Scanner

```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Audit traceability registries",
  prompt: `
    Agent: trace-audit-registry-scanner
    Read agent definition: .claude/agents/trace-audit-registry-scanner.md

    PROJECT_ROOT: ${PROJECT_ROOT}
    SYSTEM_NAME: ${SYSTEM_NAME}

    TASK:
    1. Inventory all files in traceability/
    2. Validate ID formats in each registry
    3. Check all cross-references between registries
    4. Detect orphaned artifacts
    5. Calculate coverage metrics
    6. Check for consistency issues

    CRITICAL: Only report what you actually find. No hallucination.

    RETURN: JSON structure as defined in agent spec.
  `
})
```

#### Agent 2: State Analyzer

```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Audit state files",
  prompt: `
    Agent: trace-audit-state-analyzer
    Read agent definition: .claude/agents/trace-audit-state-analyzer.md

    PROJECT_ROOT: ${PROJECT_ROOT}
    SYSTEM_NAME: ${SYSTEM_NAME}

    TASK:
    1. Inventory all files in _state/
    2. Validate checkpoint consistency per stage
    3. Check cross-stage dependencies
    4. Analyze session integrity
    5. Review lifecycle events
    6. Check for stale locks

    CRITICAL: Only report what you actually find. No hallucination.

    RETURN: JSON structure as defined in agent spec.
  `
})
```

#### Agent 3: JSON Discovery

```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Discover JSON registries",
  prompt: `
    Agent: trace-audit-json-discovery
    Read agent definition: .claude/agents/trace-audit-json-discovery.md

    PROJECT_ROOT: ${PROJECT_ROOT}
    SYSTEM_NAME: ${SYSTEM_NAME}

    TASK:
    1. Find all .json files outside traceability/ and _state/
    2. Classify potential registries using scoring system
    3. Detect shadow registries
    4. Find untracked references
    5. Identify bypass chains
    6. Analyze stage output folders

    CRITICAL: Only report what you actually find. No hallucination.

    RETURN: JSON structure as defined in agent spec.
  `
})
```

---

### Step 4: Wait for Agent Results

Display progress:

```
⏳ Audit agents running...

  [1/3] Registry Scanner     ████████████████░░░░ 80%
  [2/3] State Analyzer       ████████████████████ 100% ✅
  [3/3] JSON Discovery       ████████░░░░░░░░░░░░ 40%
```

Collect results:
- `REGISTRY_FINDINGS`: JSON from registry-scanner
- `STATE_FINDINGS`: JSON from state-analyzer
- `JSON_FINDINGS`: JSON from json-discovery

---

### Step 5: Quick Mode Check

If `--quick` flag is set:
1. Parse summary sections from each agent's findings
2. Display quick summary:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      TRACEABILITY QUICK CHECK                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Overall Health: ⚠️ WARNING                                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Traceability Registries:  ⚠️  2 critical, 3 high issues                     ║
║  State Management:         ✅  0 critical, 1 high issue                      ║
║  JSON Integrity:           ⚠️  1 critical (shadow registry)                  ║
║                                                                              ║
║  Run /trace-audit {SYSTEM_NAME} for full report.                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

3. Exit (skip consolidation)

---

### Step 6: Spawn Consolidator Agent

```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Consolidate audit findings",
  prompt: `
    Agent: trace-audit-consolidator
    Read agent definition: .claude/agents/trace-audit-consolidator.md

    PROJECT_ROOT: ${PROJECT_ROOT}
    SYSTEM_NAME: ${SYSTEM_NAME}

    REGISTRY_FINDINGS:
    ${JSON.stringify(REGISTRY_FINDINGS)}

    STATE_FINDINGS:
    ${JSON.stringify(STATE_FINDINGS)}

    JSON_FINDINGS:
    ${JSON.stringify(JSON_FINDINGS)}

    TASK:
    1. Cross-validate findings between agents
    2. Deduplicate issues
    3. Escalate severity where issues compound
    4. Build E2E traceability chain analysis
    5. Generate risk assessment
    6. Create prioritized recommendations
    7. Write TRACEABILITY_AUDIT_REPORT.md
    8. Write TRACEABILITY_MATRIX_MASTER.md

    CRITICAL: Only synthesize from provided findings. No hallucination.

    RETURN: JSON with files_written and summary.
  `
})
```

---

### Step 7: Display Results

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      TRACEABILITY AUDIT COMPLETE                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  📊 SUMMARY                                                                  ║
║  ┌────────────────────┬────────┬──────────┬────────┬────────┐               ║
║  │ Area               │ Critical│ High    │ Medium │ Low    │               ║
║  ├────────────────────┼────────┼──────────┼────────┼────────┤               ║
║  │ Registries         │ 1      │ 2        │ 3      │ 5      │               ║
║  │ State              │ 0      │ 1        │ 2      │ 3      │               ║
║  │ JSON Discovery     │ 1      │ 1        │ 2      │ 4      │               ║
║  ├────────────────────┼────────┼──────────┼────────┼────────┤               ║
║  │ TOTAL              │ 2      │ 4        │ 7      │ 12     │               ║
║  └────────────────────┴────────┴──────────┴────────┴────────┘               ║
║                                                                              ║
║  🔗 E2E COVERAGE: 85% (17/20 complete chains)                                ║
║                                                                              ║
║  ⚠️ TOP RISKS:                                                               ║
║  1. Shadow screen registry with 2 unsynced items                             ║
║  2. 3 orphaned pain points (PP-6.3, PP-7.1, PP-8.2)                          ║
║  3. Broken reference to REQ-099 in module spec                               ║
║                                                                              ║
║  📁 FILES GENERATED:                                                         ║
║  ✅ traceability/TRACEABILITY_AUDIT_REPORT.md                                ║
║  ✅ traceability/TRACEABILITY_MATRIX_MASTER.md                               ║
║                                                                              ║
║  💡 NEXT STEPS:                                                              ║
║  1. Run /traceability-init --repair to fix shadow registries                 ║
║  2. Review orphaned pain points in Discovery outputs                         ║
║  3. Fix broken reference REQ-099 in MOD-DSK-AUTH-01                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

### Step 8: Log Audit Completion

```bash
python3 .claude/hooks/command_end.py \
  --command-name "/trace-audit" \
  --stage "utility" \
  --status "completed" \
  --start-event-id "$EVENT_ID" \
  --outputs '{"files_created": 2, "critical_issues": 2, "overall_health": "WARNING"}'
```

---

### Step 9: Version History Logging

```bash
python3 .claude/hooks/version_history_logger.py \
  "traceability/" \
  "$SYSTEM_NAME" \
  "utility" \
  "$(python3 .claude/hooks/get_user_context.py)" \
  "1.0" \
  "Generated traceability audit report and matrix" \
  "" \
  "traceability/TRACEABILITY_AUDIT_REPORT.md" \
  "creation"

python3 .claude/hooks/version_history_logger.py \
  "traceability/" \
  "$SYSTEM_NAME" \
  "utility" \
  "$(python3 .claude/hooks/get_user_context.py)" \
  "1.0" \
  "Generated traceability matrix master" \
  "" \
  "traceability/TRACEABILITY_MATRIX_MASTER.md" \
  "creation"
```

---

## Error Handling

| Error | Action |
|-------|--------|
| System not found | Display error, suggest `/discovery-init` |
| Agent timeout | Log failure, continue with available findings |
| Agent error | Log error, mark section as "AUDIT_FAILED" |
| No registries | Note as finding (empty project state) |
| JSON parse error | Log and skip that agent's findings |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Audit complete, health GOOD or WARNING |
| 1 | Audit complete, health CRITICAL |
| 2 | Audit failed (agent errors) |
| 3 | Invalid arguments |

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/traceability-init` | Initialize or repair traceability backbone |
| `/traceability-status` | Quick status check (no agents) |
| `/integrity-check` | Broader integrity check (includes artifacts) |
| `/discovery-audit` | Zero hallucination audit (Discovery only) |

---

## Related Agents

| Agent | Purpose |
|-------|---------|
| `trace-audit-registry-scanner` | Analyzes traceability/ folder |
| `trace-audit-state-analyzer` | Analyzes _state/ folder |
| `trace-audit-json-discovery` | Discovers all .json registries |
| `trace-audit-consolidator` | Merges findings into reports |

---

## Performance Notes

- **Parallel mode** (default): 3 agents run simultaneously, ~60% faster
- **Sequential mode** (`--no-parallel`): Useful for debugging agent issues
- **Quick mode** (`--quick`): Skips consolidator, ~50% faster
- **Section mode** (`--section`): Runs only 1 agent, fastest for targeted audits

---

## No Hallucination Guarantee

This command and all its agents are designed with strict no-hallucination policies:

1. **Registry Scanner**: Only reports IDs found in actual files
2. **State Analyzer**: Only reports values read from state files
3. **JSON Discovery**: Only reports files found via glob
4. **Consolidator**: Only synthesizes from agent findings

All findings include evidence (file paths, line numbers, actual values).

If any finding cannot be verified, it is marked as "NEEDS_VERIFICATION".
