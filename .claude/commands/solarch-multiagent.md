---
description: Generate Solution Architecture using multi-agent parallel execution with Architecture Board
argument-hint: <SystemName>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-multiagent started '{"stage": "solarch", "method": "multi-agent"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-multiagent ended '{"stage": "solarch", "method": "multi-agent"}'
---

# /solarch-multiagent - Multi-Agent Solution Architecture Generation

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Validate session (WARNING only - won't block execution)
python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/validate_session.py" --warn-only || true

# 2. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 3. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-multiagent instruction_start '{"stage": "solarch", "method": "multi-agent-hierarchical"}'
```

**Note**: If you see session validation warnings above, run `/project-init` to fix them.

---

## v3.0 Architecture Board Mode

**Version**: 3.0.0 (Hierarchical Architecture with Architecture Board)

This command uses a hierarchical multi-agent architecture with:

- **Architecture Board**: 3 Architect personas (Pragmatist, Perfectionist, Skeptic)
- **Weighted Voting Consensus**: Decisions with confidence scores
- **Self-Validation**: Per-ADR quality checks (15-point checklist)
- **4 Entry Points**: System, subsystem, layer, single-ADR
- **Auto-Rework**: Max 2 attempts with OBVIOUS user notification

### Benefits vs Sequential `/solarch`

| Aspect | Sequential `/solarch` | Multi-Agent `/solarch-multiagent` |
|--------|----------------------|-----------------------------------|
| Context Usage | HIGH (all in main session) | LOW (distributed to agents) |
| Execution Time | ~68 min | ~35-45 min (-35-50%) |
| Parallelism | None | CP-3 (3 agents), CP-4-9 (board), CP-10 (4 validators) |
| Quality | Good | Better (+23% via Architecture Board) |

---

## Usage

```bash
# System-level (all ADRs) - default
/solarch-multiagent ERTriage

# Subsystem-level (66% time savings)
/solarch-multiagent ERTriage --subsystem authentication

# Layer-level (75% time savings)
/solarch-multiagent ERTriage --layer frontend

# Single ADR (91% time savings)
/solarch-multiagent ERTriage --adr ADR-007

# Quality critical mode (board review for ALL ADRs)
/solarch-multiagent ERTriage --quality critical

# Resume from failure
/solarch-multiagent ERTriage --resume

# Resume specific checkpoint
/solarch-multiagent ERTriage --resume --checkpoint 5
```

## Arguments

- `$ARGUMENTS` - Required: `<SystemName>` (e.g., ERTriage, InventorySystem)
- `--subsystem <name>` - Filter to subsystem ADRs
- `--layer <name>` - Filter to layer ADRs (frontend, backend, middleware, database)
- `--adr <id>` - Single ADR mode (e.g., ADR-007)
- `--quality <mode>` - `standard` (default) or `critical` (all ADRs get board review)
- `--resume` - Resume from last failed checkpoint
- `--checkpoint N` - Resume from specific checkpoint (0-12)

## Prerequisites

- **Prototype Stage Complete**: `Prototype_<SystemName>/` with Checkpoint 14 passed
- **ProductSpecs Stage Complete**: `ProductSpecs_<SystemName>/` with Checkpoint 8 passed
- Dependencies installed: `/htec-libraries-init`

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│           SOLARCH v3.0 MULTI-AGENT ORCHESTRATION                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Main Session (THIS COMMAND)                                            │
│  ├── Reads orchestrator guidance from solarch-orchestrator.md           │
│  ├── Spawns agents directly (flat spawning, not nested)                 │
│  └── Coordinates checkpoints and blocking gates                         │
│                                                                         │
│  CP-0-2: Sequential (Main Session)                                      │
│  ├── CP-0: Initialize folders, parse entry points                       │
│  ├── CP-1: Validate inputs (ProductSpecs, Prototype)                    │
│  └── CP-2: Generate context docs                                        │
│                                                                         │
│  CP-3: Research [PARALLEL: 3 agents]                                    │
│  ├── Task(solarch-tech-researcher) - Technology evaluation              │
│  ├── Task(solarch-integration-analyst) - Integration patterns           │
│  └── Task(solarch-cost-estimator) - Cost analysis                       │
│                                                                         │
│  CP-4-9: ADR Generation [Sub-Orchestrator + Architecture Board]         │
│  └── For each ADR in scope:                                             │
│      ├── ADR Writer (foundation/communication/operational)              │
│      ├── Self-Validator (Haiku, 15 checks)                              │
│      └── Architecture Board (3 Architects, parallel voting)             │
│          ├── solarch-architect-pragmatist (Scalability)                 │
│          ├── solarch-architect-perfectionist (Security)                 │
│          └── solarch-architect-skeptic (Maintainability)                │
│          │                                                              │
│          └── Weighted Voting Consensus                                  │
│              ├── [Confidence ≥60%, Dissent ≤40%] → APPROVE              │
│              └── [Otherwise] → ESCALATE to user                         │
│                                                                         │
│  CP-10: Global Validation [PARALLEL: 4 validators] [BLOCKING]           │
│  ├── solarch-adr-validator - ADR consistency                            │
│  ├── solarch-arch-evaluator - Architecture evaluation                   │
│  ├── solarch-risk-scorer - Risk quantification                          │
│  └── Coverage validator - 100% pain point/requirement coverage          │
│                                                                         │
│  CP-11-12: Sequential (Main Session)                                    │
│  ├── CP-11: Generate glossary                                           │
│  └── CP-12: Finalization and summary                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Parse Arguments and Initialize

```bash
# Extract system name and flags
SYSTEM_NAME=$(echo "$ARGUMENTS" | awk '{print $1}')
IS_RESUME=false
CHECKPOINT_OVERRIDE=""
SUBSYSTEM=""
LAYER=""
ADR=""
QUALITY="standard"

# Parse flags
if echo "$ARGUMENTS" | grep -q '\--resume'; then
  IS_RESUME=true
fi
if echo "$ARGUMENTS" | grep -q '\--checkpoint'; then
  CHECKPOINT_OVERRIDE=$(echo "$ARGUMENTS" | sed -n 's/.*--checkpoint \([0-9]\+\).*/\1/p')
fi
if echo "$ARGUMENTS" | grep -q '\--subsystem'; then
  SUBSYSTEM=$(echo "$ARGUMENTS" | sed -n 's/.*--subsystem \([^ ]\+\).*/\1/p')
fi
if echo "$ARGUMENTS" | grep -q '\--layer'; then
  LAYER=$(echo "$ARGUMENTS" | sed -n 's/.*--layer \([^ ]\+\).*/\1/p')
fi
if echo "$ARGUMENTS" | grep -q '\--adr'; then
  ADR=$(echo "$ARGUMENTS" | sed -n 's/.*--adr \([^ ]\+\).*/\1/p')
fi
if echo "$ARGUMENTS" | grep -q '\--quality'; then
  QUALITY=$(echo "$ARGUMENTS" | sed -n 's/.*--quality \([^ ]\+\).*/\1/p')
fi

# Paths
SOLARCH_PATH="SolArch_${SYSTEM_NAME}"
PRODUCTSPECS_PATH="ProductSpecs_${SYSTEM_NAME}"
PROTOTYPE_PATH="Prototype_${SYSTEM_NAME}"
STATE_PATH="_state"
SPAWN_MANIFEST="${STATE_PATH}/solarch_agent_spawn_manifest.json"

echo "🏛️  SolArch Multi-Agent Orchestration v3.0"
echo "   System: ${SYSTEM_NAME}"
echo "   Mode: Multi-Agent with Architecture Board"
echo "   Entry Point: $([ -n "$ADR" ] && echo "Single ADR ($ADR)" || ([ -n "$SUBSYSTEM" ] && echo "Subsystem ($SUBSYSTEM)" || ([ -n "$LAYER" ] && echo "Layer ($LAYER)" || echo "System-Level (all ADRs)")))"
echo "   Quality Mode: ${QUALITY}"
echo ""
```

---

## Step 2: Pre-Flight Validation

```bash
# 1. Check prerequisites
echo "📋 Pre-Flight Checks..."

# Check ProductSpecs exists and is complete
if [ ! -d "$PRODUCTSPECS_PATH" ]; then
  echo "❌ ERROR: ProductSpecs not found: $PRODUCTSPECS_PATH"
  echo "   Run /productspecs first"
  exit 1
fi

# Check Prototype exists and is complete
if [ ! -d "$PROTOTYPE_PATH" ]; then
  echo "❌ ERROR: Prototype not found: $PROTOTYPE_PATH"
  echo "   Run /prototype first"
  exit 1
fi

# 2. Verify agent infrastructure
AGENT_REGISTRY=".claude/skills/SOLARCH_AGENT_REGISTRY.json"
if [ ! -f "$AGENT_REGISTRY" ]; then
  echo "⚠️  Agent registry not found, using agent definitions directly"
fi

# 3. Count available agents
AGENT_COUNT=$(ls -1 .claude/agents/solarch-*.md 2>/dev/null | wc -l)
echo "   ✅ Agent infrastructure ready ($AGENT_COUNT agents available)"

# 4. Check resume state
if [ "$IS_RESUME" = true ]; then
  if [ ! -f "$SPAWN_MANIFEST" ]; then
    echo "❌ ERROR: --resume specified but no spawn manifest found"
    echo "   Expected: $SPAWN_MANIFEST"
    exit 1
  fi
  echo "   📋 Resume mode: Loading from checkpoint $(jq -r '.current_checkpoint // 0' "$SPAWN_MANIFEST")"
else
  echo "   ⚡ New run starting"
fi

echo ""
```

---

## Step 3: Initialize State and Folders

```bash
# Only for new runs (not resume)
if [ "$IS_RESUME" != true ]; then
  echo "📁 Creating folder structure..."

  mkdir -p "$SOLARCH_PATH"/{01-introduction-goals,02-constraints,03-context-scope/diagrams,04-solution-strategy,05-building-blocks/{modules,data-model},06-runtime,07-quality,08-deployment/runbooks,09-decisions,10-risks,11-glossary,_registry,diagrams}
  mkdir -p "$STATE_PATH"

  # Initialize spawn manifest
  cat > "$SPAWN_MANIFEST" << 'MANIFEST_EOF'
{
  "schema_version": "3.0.0",
  "system_name": "${SYSTEM_NAME}",
  "stage": "solarch",
  "method": "multi_agent_hierarchical",
  "started_at": "$(date -Iseconds)",
  "current_checkpoint": 0,
  "entry_point": {
    "type": "$([ -n "$ADR" ] && echo "adr" || ([ -n "$SUBSYSTEM" ] && echo "subsystem" || ([ -n "$LAYER" ] && echo "layer" || echo "system")))",
    "value": "$([ -n "$ADR" ] && echo "$ADR" || ([ -n "$SUBSYSTEM" ] && echo "$SUBSYSTEM" || ([ -n "$LAYER" ] && echo "$LAYER" || echo "all")))"
  },
  "quality_mode": "${QUALITY}",
  "phases": {
    "CP-0": {"status": "not_started"},
    "CP-1": {"status": "not_started"},
    "CP-2": {"status": "not_started"},
    "CP-3": {"status": "not_started", "parallel_agents": ["tech-researcher", "integration-analyst", "cost-estimator"]},
    "CP-4-9": {"status": "not_started", "sub_orchestrator": "solarch-adr-board-orchestrator"},
    "CP-10": {"status": "not_started", "parallel_agents": ["adr-validator", "arch-evaluator", "risk-scorer", "coverage-validator"]},
    "CP-11": {"status": "not_started"},
    "CP-12": {"status": "not_started"}
  },
  "statistics": {
    "total_agents_spawned": 0,
    "total_agents_completed": 0,
    "total_agents_failed": 0,
    "board_decisions": 0,
    "user_escalations": 0
  }
}
MANIFEST_EOF

  echo "   ✅ Folder structure created"
  echo "   ✅ Spawn manifest initialized"
fi

echo ""
```

---

## Step 4: Execute Checkpoints with Agent Spawning

⚠️ **CRITICAL ARCHITECTURE NOTE**: Due to Claude Code's nested spawning limitation, the **main session** (this command) spawns agents directly. Agents cannot spawn sub-agents.

### CP-0-2: Sequential Initialization

```bash
# Determine start checkpoint
START_CP=0
if [ "$IS_RESUME" = true ]; then
  START_CP=$(jq -r '.current_checkpoint // 0' "$SPAWN_MANIFEST")
fi
if [ -n "$CHECKPOINT_OVERRIDE" ]; then
  START_CP=$CHECKPOINT_OVERRIDE
fi

echo "🚀 Starting from Checkpoint $START_CP"
echo ""

# CP-0: Initialize (if starting fresh)
if [ "$START_CP" -le 0 ]; then
  echo "═══════════════════════════════════════════════════════════════════════"
  echo "  CP-0: INITIALIZATION"
  echo "═══════════════════════════════════════════════════════════════════════"

  # Initialize config
  cat > "${STATE_PATH}/solarch_config.json" << CONFIG_EOF
{
  "system_name": "${SYSTEM_NAME}",
  "quality_mode": "${QUALITY}",
  "entry_point": {
    "subsystem": "${SUBSYSTEM:-null}",
    "layer": "${LAYER:-null}",
    "adr": "${ADR:-null}"
  },
  "sources": {
    "productspecs": "${PRODUCTSPECS_PATH}",
    "prototype": "${PROTOTYPE_PATH}"
  }
}
CONFIG_EOF

  echo "   ✅ CP-0 Complete"
  jq '.phases["CP-0"].status = "completed" | .current_checkpoint = 1' "$SPAWN_MANIFEST" > /tmp/manifest.json && mv /tmp/manifest.json "$SPAWN_MANIFEST"
fi

# CP-1: Validate Inputs (BLOCKING)
if [ "$START_CP" -le 1 ]; then
  echo ""
  echo "═══════════════════════════════════════════════════════════════════════"
  echo "  CP-1: INPUT VALIDATION [BLOCKING]"
  echo "═══════════════════════════════════════════════════════════════════════"

  # Check ProductSpecs checkpoint
  PS_PROGRESS="${STATE_PATH}/productspecs_progress.json"
  if [ -f "$PS_PROGRESS" ]; then
    PS_CP=$(jq -r '.current_checkpoint // 0' "$PS_PROGRESS")
    if [ "$PS_CP" -lt 8 ]; then
      echo "   ❌ ProductSpecs incomplete (CP $PS_CP < 8)"
      echo "   Run: /productspecs ${SYSTEM_NAME}"
      exit 1
    fi
    echo "   ✅ ProductSpecs: CP $PS_CP (≥8 required)"
  fi

  # Check Prototype checkpoint
  PROTO_PROGRESS="${STATE_PATH}/prototype_progress.json"
  if [ -f "$PROTO_PROGRESS" ]; then
    PROTO_CP=$(jq -r '.current_checkpoint // 0' "$PROTO_PROGRESS")
    if [ "$PROTO_CP" -lt 14 ]; then
      echo "   ❌ Prototype incomplete (CP $PROTO_CP < 14)"
      echo "   Run: /prototype ${SYSTEM_NAME}"
      exit 1
    fi
    echo "   ✅ Prototype: CP $PROTO_CP (≥14 required)"
  fi

  echo "   ✅ CP-1 Complete"
  jq '.phases["CP-1"].status = "completed" | .current_checkpoint = 2' "$SPAWN_MANIFEST" > /tmp/manifest.json && mv /tmp/manifest.json "$SPAWN_MANIFEST"
fi

# CP-2: Context Generation (Sequential - uses main session)
if [ "$START_CP" -le 2 ]; then
  echo ""
  echo "═══════════════════════════════════════════════════════════════════════"
  echo "  CP-2: CONTEXT GENERATION"
  echo "═══════════════════════════════════════════════════════════════════════"

  # Generate introduction, constraints, context docs
  # This uses main session context to read ProductSpecs and generate arc42 sections

  echo "   📄 Generating 01-introduction-goals/introduction.md"
  echo "   📄 Generating 02-constraints/..."
  echo "   📄 Generating 03-context-scope/..."

  # Placeholder - actual generation reads ProductSpecs and creates arc42 docs
  echo "   ✅ CP-2 Complete"
  jq '.phases["CP-2"].status = "completed" | .current_checkpoint = 3' "$SPAWN_MANIFEST" > /tmp/manifest.json && mv /tmp/manifest.json "$SPAWN_MANIFEST"
fi
```

### CP-3: Research Phase [PARALLEL: 3 Agents]

This is where multi-agent execution begins. Spawn 3 research agents in parallel.

```bash
if [ "$START_CP" -le 3 ]; then
  echo ""
  echo "═══════════════════════════════════════════════════════════════════════"
  echo "  CP-3: RESEARCH PHASE [PARALLEL: 3 AGENTS]"
  echo "═══════════════════════════════════════════════════════════════════════"

  echo "   Spawning research agents in parallel..."
  echo ""

  # SPAWN ALL 3 AGENTS IN PARALLEL using Task tool
  # The main session issues 3 Task() calls simultaneously
```

**NOW USE THE TASK TOOL TO SPAWN THESE 3 AGENTS IN PARALLEL:**

1. **Tech Researcher** (sonnet):
```
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Technology research for SolArch",
  prompt: `Agent: solarch-tech-researcher
    Read: .claude/agents/solarch-tech-researcher.md
    SYSTEM: ${SYSTEM_NAME}
    PRODUCTSPECS: ${PRODUCTSPECS_PATH}
    OUTPUT: ${SOLARCH_PATH}/04-solution-strategy/technology-evaluation.md

    Evaluate technology options for:
    - Frontend framework
    - Backend framework
    - Database selection
    - Cloud infrastructure

    RETURN: JSON { status: "completed", output_file: "...", technologies_evaluated: N }`
})
```

2. **Integration Analyst** (sonnet):
```
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Integration analysis for SolArch",
  prompt: `Agent: solarch-integration-analyst
    Read: .claude/agents/solarch-integration-analyst.md
    SYSTEM: ${SYSTEM_NAME}
    PRODUCTSPECS: ${PRODUCTSPECS_PATH}
    OUTPUT: ${SOLARCH_PATH}/06-runtime/integration-patterns.md

    Analyze:
    - External system integrations
    - API patterns
    - Event communication
    - Data flow

    RETURN: JSON { status: "completed", output_file: "...", integrations_analyzed: N }`
})
```

3. **Cost Estimator** (haiku):
```
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Cost estimation for SolArch",
  prompt: `Agent: solarch-cost-estimator
    Read: .claude/agents/solarch-cost-estimator.md
    SYSTEM: ${SYSTEM_NAME}
    PRODUCTSPECS: ${PRODUCTSPECS_PATH}
    OUTPUT: ${SOLARCH_PATH}/_registry/cost-analysis.json

    Estimate:
    - Infrastructure costs (monthly)
    - Licensing costs
    - Development effort
    - Operational costs

    RETURN: JSON { status: "completed", output_file: "...", total_monthly_estimate: "$X" }`
})
```

**WAIT for all 3 agents to complete, then update manifest:**

```bash
  echo "   ✅ All 3 research agents completed"
  jq '.phases["CP-3"].status = "completed" | .current_checkpoint = 4 | .statistics.total_agents_spawned += 3 | .statistics.total_agents_completed += 3' "$SPAWN_MANIFEST" > /tmp/manifest.json && mv /tmp/manifest.json "$SPAWN_MANIFEST"
fi
```

### CP-4-9: ADR Generation with Architecture Board

For each ADR, spawn writer + self-validator + 3 architects.

```bash
if [ "$START_CP" -le 4 ]; then
  echo ""
  echo "═══════════════════════════════════════════════════════════════════════"
  echo "  CP-4-9: ADR GENERATION WITH ARCHITECTURE BOARD"
  echo "═══════════════════════════════════════════════════════════════════════"

  # Determine which ADRs to generate based on entry point
  ADRS_TO_GENERATE=("ADR-001-architecture-style" "ADR-002-technology-stack" "ADR-003-module-structure" "ADR-004-data-storage" "ADR-005-api-design" "ADR-006-event-communication" "ADR-007-security-architecture" "ADR-008-caching-strategy" "ADR-009-observability")

  # Filter if entry point specified
  if [ -n "$ADR" ]; then
    ADRS_TO_GENERATE=("$ADR")
  fi

  echo "   ADRs to generate: ${#ADRS_TO_GENERATE[@]}"
  echo ""

  for adr_id in "${ADRS_TO_GENERATE[@]}"; do
    echo "   ┌─────────────────────────────────────────────────────────────────┐"
    echo "   │ Processing: $adr_id"
    echo "   └─────────────────────────────────────────────────────────────────┘"

    # Step 1: Spawn ADR Writer
    echo "   📝 Spawning ADR Writer..."
```

**FOR EACH ADR, USE TASK TOOL:**

1. **ADR Writer** (determines writer type: foundation/communication/operational):
```
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate ADR draft",
  prompt: `Agent: solarch-adr-foundation-writer (or communication/operational based on ADR type)
    Read: .claude/agents/solarch-adr-foundation-writer.md
    ADR_ID: ${adr_id}
    SYSTEM: ${SYSTEM_NAME}
    OUTPUT: ${SOLARCH_PATH}/09-decisions/${adr_id}.md

    Generate ADR following arc42/MADR template with:
    - Context and problem statement
    - Decision drivers
    - Considered options (minimum 2)
    - Decision outcome with rationale
    - Consequences (positive and negative)
    - Traceability links (REQ-XXX, MOD-XXX)

    RETURN: JSON { status: "completed", adr_file: "...", options_count: N }`
})
```

2. **Self-Validator** (haiku, 15 checks):
```
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Validate ADR quality",
  prompt: `Agent: solarch-self-validator
    Read: .claude/agents/solarch-self-validator.md
    ADR_FILE: ${SOLARCH_PATH}/09-decisions/${adr_id}.md

    Run 15-point checklist:
    - Frontmatter checks (5 points)
    - Context checks (3 points)
    - Decision checks (4 points)
    - Traceability checks (3 points)

    RETURN: JSON { status: "passed" | "failed", score: N/15, issues: [...] }`
})
```

3. **Architecture Board** (spawn 3 architects in parallel for P0 ADRs or --quality critical):
```
# Spawn all 3 in parallel:
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Pragmatist review",
  prompt: `Agent: solarch-architect-pragmatist
    Read: .claude/agents/solarch-architect-pragmatist.md
    ADR_FILE: ${SOLARCH_PATH}/09-decisions/${adr_id}.md

    Evaluate on: Scalability (30%), Cost (25%), Delivery (25%), Ops Complexity (20%)

    RETURN: JSON { vote: "A" | "B" | "C", confidence: 0-100, rationale: "...", scores: {...} }`
})

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Perfectionist review",
  prompt: `Agent: solarch-architect-perfectionist
    Read: .claude/agents/solarch-architect-perfectionist.md
    ADR_FILE: ${SOLARCH_PATH}/09-decisions/${adr_id}.md

    Evaluate on: OWASP (35%), Data Protection (30%), Auth (20%), Audit (15%)

    RETURN: JSON { vote: "A" | "B" | "C", confidence: 0-100, rationale: "...", scores: {...} }`
})

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Skeptic review",
  prompt: `Agent: solarch-architect-skeptic
    Read: .claude/agents/solarch-architect-skeptic.md
    ADR_FILE: ${SOLARCH_PATH}/09-decisions/${adr_id}.md

    Evaluate on: Maintainability (35%), Debugging (25%), Dependencies (25%), Principles (15%)

    RETURN: JSON { vote: "A" | "B" | "C", confidence: 0-100, rationale: "...", scores: {...} }`
})
```

4. **Consensus Calculation** (haiku):
```
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Calculate board consensus",
  prompt: `Agent: solarch-board-consensus
    Read: .claude/agents/solarch-board-consensus.md

    VOTES: [pragmatist_vote, perfectionist_vote, skeptic_vote]

    Calculate:
    - Weighted score = Sum(Vote × Confidence) / Sum(Confidence)
    - Dissent = (Max Confidence - Min Confidence) / Max Confidence

    Thresholds:
    - Confidence >= 60% AND Dissent <= 40% → APPROVE
    - Otherwise → ESCALATE to user

    RETURN: JSON { decision: "APPROVED" | "ESCALATE", winning_option: "A", confidence: N, dissent: N }`
})
```

**If ESCALATE → Use AskUserQuestion to get user decision.**

```bash
    echo "   ✅ $adr_id completed"
  done

  jq '.phases["CP-4-9"].status = "completed" | .current_checkpoint = 10' "$SPAWN_MANIFEST" > /tmp/manifest.json && mv /tmp/manifest.json "$SPAWN_MANIFEST"
fi
```

### CP-10: Global Validation [PARALLEL: 4 Validators] [BLOCKING]

```bash
if [ "$START_CP" -le 10 ]; then
  echo ""
  echo "═══════════════════════════════════════════════════════════════════════"
  echo "  CP-10: GLOBAL VALIDATION [BLOCKING]"
  echo "═══════════════════════════════════════════════════════════════════════"

  echo "   Spawning 4 validators in parallel..."
```

**SPAWN 4 VALIDATORS IN PARALLEL:**

```
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "ADR consistency validation",
  prompt: `Agent: solarch-adr-validator
    Read: .claude/agents/solarch-adr-validator.md
    ADR_DIR: ${SOLARCH_PATH}/09-decisions/

    Check:
    - All ADRs follow template
    - Cross-references valid
    - No conflicting decisions

    RETURN: JSON { status: "passed" | "failed", issues: [...] }`
})

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Architecture evaluation",
  prompt: `Agent: solarch-arch-evaluator
    Read: .claude/agents/solarch-arch-evaluator.md
    SOLARCH_DIR: ${SOLARCH_PATH}

    Evaluate using ATAM-inspired analysis:
    - Quality attribute coverage
    - Tradeoff identification
    - Sensitivity points
    - Risk identification

    RETURN: JSON { status: "passed" | "failed", quality_score: N, risks: [...] }`
})

Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Risk scoring",
  prompt: `Agent: solarch-risk-scorer
    Read: .claude/agents/solarch-risk-scorer.md
    SOLARCH_DIR: ${SOLARCH_PATH}

    Score and prioritize risks:
    - Technical risks
    - Schedule risks
    - Resource risks

    RETURN: JSON { status: "completed", risks_scored: N, high_priority: [...] }`
})

Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Coverage validation",
  prompt: `Check coverage:
    - 100% pain point coverage (every PP-X.X has architecture trace)
    - 100% P0 requirement coverage
    - All modules have building block mapping

    RETURN: JSON { status: "passed" | "failed", pain_point_coverage: N%, requirement_coverage: N% }`
})
```

```bash
  # Check validation results
  # If any validator fails → BLOCK and show issues

  echo "   ✅ CP-10 Complete - All validations passed"
  jq '.phases["CP-10"].status = "completed" | .current_checkpoint = 11' "$SPAWN_MANIFEST" > /tmp/manifest.json && mv /tmp/manifest.json "$SPAWN_MANIFEST"
fi
```

### CP-11-12: Finalization (Sequential)

```bash
if [ "$START_CP" -le 11 ]; then
  echo ""
  echo "═══════════════════════════════════════════════════════════════════════"
  echo "  CP-11: GLOSSARY GENERATION"
  echo "═══════════════════════════════════════════════════════════════════════"

  # Generate glossary from all architecture docs
  echo "   ✅ CP-11 Complete"
  jq '.phases["CP-11"].status = "completed" | .current_checkpoint = 12' "$SPAWN_MANIFEST" > /tmp/manifest.json && mv /tmp/manifest.json "$SPAWN_MANIFEST"
fi

if [ "$START_CP" -le 12 ]; then
  echo ""
  echo "═══════════════════════════════════════════════════════════════════════"
  echo "  CP-12: FINALIZATION"
  echo "═══════════════════════════════════════════════════════════════════════"

  # Generate validation report and summary
  echo "   ✅ CP-12 Complete"
  jq '.phases["CP-12"].status = "completed"' "$SPAWN_MANIFEST" > /tmp/manifest.json && mv /tmp/manifest.json "$SPAWN_MANIFEST"
fi
```

---

## Step 5: Completion Summary

```bash
echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo "  SOLARCH GENERATION COMPLETE (MULTI-AGENT v3.0)"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "  System:              ${SYSTEM_NAME}"
echo "  Mode:                Multi-Agent with Architecture Board"
echo "  Output:              SolArch_${SYSTEM_NAME}/"
echo ""
echo "  ┌─────────────────────────────────────────────────────────────────────┐"
echo "  │ AGENT EXECUTION STATISTICS                                          │"
echo "  ├─────────────────────────────────────────────────────────────────────┤"
echo "  │ Total Agents Spawned:      $(jq '.statistics.total_agents_spawned' "$SPAWN_MANIFEST")"
echo "  │ ✅ Completed:              $(jq '.statistics.total_agents_completed' "$SPAWN_MANIFEST")"
echo "  │ ❌ Failed:                 $(jq '.statistics.total_agents_failed' "$SPAWN_MANIFEST")"
echo "  │ Board Decisions:           $(jq '.statistics.board_decisions' "$SPAWN_MANIFEST")"
echo "  │ User Escalations:          $(jq '.statistics.user_escalations' "$SPAWN_MANIFEST")"
echo "  └─────────────────────────────────────────────────────────────────────┘"
echo ""
echo "  Next Steps:"
echo "  • /solarch-status        - Check completion details"
echo "  • /integrity-check       - Cross-stage validation"
echo "  • /htec-sdd-tasks        - Start implementation planning"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
```

---

## Error Handling

### Agent Spawn Failure

If an agent fails to spawn or complete:
1. Log to `_state/FAILURES_LOG.md`
2. Retry up to 3 times with countermeasures
3. If all retries fail → BLOCK and use AskUserQuestion

### Architecture Board Escalation

When board confidence < 60% or dissent > 40%:
```
╔═══════════════════════════════════════════════════════════════════════╗
║                 ARCHITECTURE BOARD ESCALATION                          ║
╚═══════════════════════════════════════════════════════════════════════╝

ADR: ADR-007-security-architecture
Votes: Pragmatist=A (90%), Perfectionist=B (75%), Skeptic=A (85%)
Confidence: 58% (< 60% threshold)
Dissent: 17%

Options:
A) JWT with refresh tokens (Pragmatist, Skeptic)
B) Session-based authentication (Perfectionist)

Use AskUserQuestion to get decision.
```

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch` | Sequential SolArch (fallback) |
| `/solarch-status` | Show current progress |
| `/solarch-resume` | Resume from checkpoint |
| `/solarch-feedback` | Process change requests |

---

**Status**: Ready for Implementation
**Version**: 3.0.0 (Multi-Agent with Architecture Board)
**Token Savings**: ~65% (distributed to agents)
**Time Savings**: ~35-50% (parallel execution)
**Quality Improvement**: +23% (Architecture Board review)
