---
name: discovery-competitive-analysis
description: "/discovery-competitive-analysis - Perform competitive intelligence analysis with threat/opportunity scoring and sales battlecards"
args:
  - name: system_name
    description: "System name (e.g., InventorySystem)"
    required: true
  - name: competitors
    description: "Comma-separated list of known competitors (e.g., 'Competitor1,Competitor2,Competitor3')"
    required: false
  - name: segment
    description: "Specific market segment/niche definition (e.g., 'Enterprise SaaS for cold-chain logistics')"
    required: false
  - name: depth
    description: "Analysis depth: quick_scan, standard (default), or deep_dive"
    required: false
hooks:
  Start:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-competitive-analysis started '{"stage": "discovery", "system_name": "$1"}'
        # VALIDATION: Ensure Discovery outputs exist before running competitive analysis
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$1/03-strategy"
            --requires "PRODUCT_VISION.md"
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$1/03-strategy"
            --requires "PRODUCT_STRATEGY.md"
  Stop:
    - hooks:
        # VALIDATION: Check competitive intelligence outputs exist (CP-6.5)
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$1/03-strategy"
            --requires "COMPETITIVE_LANDSCAPE.md"
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$1/03-strategy"
            --requires "THREAT_OPPORTUNITY_MATRIX.md"
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$1/03-strategy"
            --requires "DIFFERENTIATION_BLUEPRINT.md"
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$1/03-strategy"
            --requires "COMPETITIVE_INTELLIGENCE_SUMMARY.md"
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-competitive-analysis ended '{"stage": "discovery", "system_name": "$1"}'
---

# /discovery-competitive-analysis Command

Performs strategic competitive intelligence analysis for a specific market niche, generating threat/opportunity scores, differentiation strategies, and sales battlecards.

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh command /discovery-competitive-analysis started '{"stage": "discovery", "system_name": "$ARGS_SYSTEM_NAME"}'
```

## Usage

```bash
# Basic usage (analyzes competitors based on Discovery outputs)
/discovery-competitive-analysis InventorySystem

# With known competitors to focus on
/discovery-competitive-analysis InventorySystem --competitors "NetSuite,SAP,Zoho Inventory"

# With specific market segment definition
/discovery-competitive-analysis InventorySystem --segment "SMB inventory management for e-commerce"

# Deep dive analysis with all parameters
/discovery-competitive-analysis InventorySystem --competitors "NetSuite,SAP" --segment "Enterprise inventory SaaS" --depth deep_dive
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `system_name` | Yes | - | Name of the system (matches Discovery folder) |
| `--competitors` | No | Auto-discover | Comma-separated list of known competitors |
| `--segment` | No | From strategy | Specific market niche definition |
| `--depth` | No | `standard` | Analysis depth: `quick_scan`, `standard`, `deep_dive` |

### Analysis Depth Levels

| Level | Time | Competitors | Reviews/Competitor | Includes |
|-------|------|-------------|-------------------|----------|
| `quick_scan` | ~15 min | 3-5 direct only | 10 | Landscape, Matrix |
| `standard` | ~45 min | 5-8 (direct + indirect) | 20 | + Battlecards, Blueprint |
| `deep_dive` | ~90 min | 10+ (all categories) | 50+ | + Predictive analysis, Patent review |

## Prerequisites

**Required Discovery Outputs** (in `ClientAnalysis_<SystemName>/`):

| File | Location | Purpose |
|------|----------|---------|
| `PRODUCT_VISION.md` | `03-strategy/` | Defines value proposition |
| `PRODUCT_STRATEGY.md` | `03-strategy/` | Defines market positioning |
| `personas/` | `02-research/` | Target customer profiles |
| `JOBS_TO_BE_DONE.md` | `02-research/` | Customer needs |
| `PAIN_POINTS.md` | `01-analysis/` | Unmet needs to exploit |

**If Discovery not complete**, run first:
```bash
/discovery <SystemName> <InputPath>
```

## Output Artifacts

All outputs written to `ClientAnalysis_<SystemName>/03-strategy/`:

| Artifact | Description |
|----------|-------------|
| `COMPETITIVE_LANDSCAPE.md` | Market map with direct, indirect, aspirational competitors |
| `THREAT_OPPORTUNITY_MATRIX.md` | Scored analysis of each competitor (Threat/Opportunity) |
| `DIFFERENTIATION_BLUEPRINT.md` | USP analysis and positioning strategy |
| `battlecards/` | Per-competitor quick-reference cards for sales |
| `COMPETITIVE_INTELLIGENCE_SUMMARY.md` | Executive summary with key insights |

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│           /discovery-competitive-analysis FLOW                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. VALIDATE prerequisites exist                                    │
│         │                                                           │
│         ▼                                                           │
│  2. SPAWN discovery-competitor-analyst agent                        │
│         │                                                           │
│         ├── Load organizational context (Vision, Strategy, etc.)    │
│         ├── Define market boundaries                                │
│         ├── Discover competitors via WebSearch                      │
│         ├── Analyze each competitor (features, GTM, reviews)        │
│         ├── Score threats and opportunities                         │
│         ├── Create differentiation blueprint                        │
│         ├── Generate sales battlecards                              │
│         └── Predict competitor next moves                           │
│         │                                                           │
│         ▼                                                           │
│  3. VALIDATE outputs (CP-6.5)                                       │
│         │                                                           │
│         ▼                                                           │
│  4. LOG completion                                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Execution Instructions

### Step 1: Parse Arguments

```bash
SYSTEM_NAME="$1"
COMPETITORS="${2:-}"        # Optional: --competitors "A,B,C"
SEGMENT="${3:-}"            # Optional: --segment "Market niche"
DEPTH="${4:-standard}"      # Optional: --depth quick_scan|standard|deep_dive

# Derive paths
DISCOVERY_PATH="ClientAnalysis_${SYSTEM_NAME}"
OUTPUT_PATH="${DISCOVERY_PATH}/03-strategy"
```

### Step 2: Validate Prerequisites

Check that required Discovery outputs exist:

```bash
# Check critical files
for file in "03-strategy/PRODUCT_VISION.md" "03-strategy/PRODUCT_STRATEGY.md" "02-research/JOBS_TO_BE_DONE.md" "01-analysis/PAIN_POINTS.md"; do
    if [ ! -f "${DISCOVERY_PATH}/${file}" ]; then
        echo "❌ ERROR: Missing prerequisite: ${file}"
        echo "Run '/discovery ${SYSTEM_NAME} <InputPath>' first"
        exit 1
    fi
done
```

### Step 3: Spawn Competitor Analyst Agent

Use the Task tool to spawn the agent:

```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Competitive analysis for " + SYSTEM_NAME,
  prompt: `
    Agent: discovery-competitor-analyst
    Read instructions from: .claude/agents/discovery-competitor-analyst.md

    SYSTEM NAME: ${SYSTEM_NAME}
    OUTPUT PATH: ${OUTPUT_PATH}/

    INPUTS:
    - PRODUCT_VISION: ${OUTPUT_PATH}/PRODUCT_VISION.md
    - PRODUCT_STRATEGY: ${OUTPUT_PATH}/PRODUCT_STRATEGY.md
    - PERSONAS: ${DISCOVERY_PATH}/02-research/personas/
    - JTBD: ${DISCOVERY_PATH}/02-research/JOBS_TO_BE_DONE.md
    - PAIN_POINTS: ${DISCOVERY_PATH}/01-analysis/PAIN_POINTS.md

    ${COMPETITORS ? `KNOWN COMPETITORS (validate and expand): ${COMPETITORS}` : 'DISCOVER competitors via web search'}
    ${SEGMENT ? `MARKET SEGMENT: ${SEGMENT}` : 'DERIVE segment from strategy'}
    ANALYSIS DEPTH: ${DEPTH}

    OUTPUT ARTIFACTS:
    - COMPETITIVE_LANDSCAPE.md
    - THREAT_OPPORTUNITY_MATRIX.md
    - DIFFERENTIATION_BLUEPRINT.md
    - battlecards/*.md (one per major direct competitor)
    - COMPETITIVE_INTELLIGENCE_SUMMARY.md

    REQUIREMENTS:
    - Score all competitors using Threat/Opportunity methodology
    - Cite all sources with URLs
    - Include battlecards for top direct competitors
    ${DEPTH === 'deep_dive' ? '- Include 6-month predictive analysis' : ''}
    ${DEPTH === 'deep_dive' ? '- Review patent/trademark filings' : ''}

    Write all artifacts directly using the Write tool.
    Do NOT return code to orchestrator.
  `
})
```

### Step 4: Log Completion

```bash
bash .claude/hooks/log-lifecycle.sh command /discovery-competitive-analysis ended '{"stage": "discovery", "system_name": "'$SYSTEM_NAME'", "status": "completed"}'
```

## Example Session

```bash
# User runs competitive analysis after Discovery
/discovery-competitive-analysis ERTriage --competitors "Triage.ai,TriageBot,MedSort" --segment "Emergency room triage software for community hospitals"

# Output:
⏳ Validating prerequisites...
✅ PRODUCT_VISION.md found
✅ PRODUCT_STRATEGY.md found
✅ JOBS_TO_BE_DONE.md found
✅ PAIN_POINTS.md found

⏳ Spawning discovery-competitor-analyst agent...
   └── Analyzing direct competitors: Triage.ai, TriageBot, MedSort
   └── Searching for indirect competitors...
   └── Gathering customer reviews from G2, Capterra...
   └── Scoring threats and opportunities...

✅ Competitive analysis complete!

Output files:
- ClientAnalysis_ERTriage/03-strategy/COMPETITIVE_LANDSCAPE.md
- ClientAnalysis_ERTriage/03-strategy/THREAT_OPPORTUNITY_MATRIX.md
- ClientAnalysis_ERTriage/03-strategy/DIFFERENTIATION_BLUEPRINT.md
- ClientAnalysis_ERTriage/03-strategy/battlecards/TRIAGE_AI_BATTLECARD.md
- ClientAnalysis_ERTriage/03-strategy/battlecards/TRIAGEBOT_BATTLECARD.md
- ClientAnalysis_ERTriage/03-strategy/battlecards/MEDSORT_BATTLECARD.md
- ClientAnalysis_ERTriage/03-strategy/COMPETITIVE_INTELLIGENCE_SUMMARY.md

💡 Suggested next: /discovery-roadmap ERTriage (incorporate competitive insights)
```

## Integration with Discovery Workflow

This command can be run:

1. **After full Discovery** - As a follow-up to enrich strategy outputs
2. **During Discovery** - Integrated at CP-6.5 by `/discovery` and `/discovery-multiagent`
3. **Standalone** - When existing Discovery outputs need competitive refresh

```
Discovery Flow:
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  /discovery → CP-1 to CP-6 → CP-6.5 (Competitive) → CP-7 to CP-12  │
│                                  ↑                                  │
│                                  │                                  │
│                    /discovery-competitive-analysis                  │
│                    (can run standalone at this point)               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Quality Criteria

| Criterion | Threshold |
|-----------|-----------|
| Competitor coverage | At least 3 direct, 2 indirect |
| Evidence depth | Minimum 3 sources per major claim |
| Scoring justification | Clear methodology with evidence |
| Battlecard completeness | All sections filled, no placeholders |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Missing prerequisite" | Run `/discovery <SystemName> <InputPath>` first |
| No competitors found | Provide `--competitors` parameter with known players |
| WebSearch failures | Agent will proceed with partial data, check COMPETITIVE_INTELLIGENCE_SUMMARY.md for limitations |
| Stale data | Re-run command to refresh analysis |

## Related Commands

| Command | Description |
|---------|-------------|
| `/discovery` | Full Discovery workflow (includes CP-6.5) |
| `/discovery-strategy-doc` | Generate/update PRODUCT_STRATEGY.md |
| `/discovery-vision` | Generate/update PRODUCT_VISION.md |
| `/discovery-roadmap` | Generate roadmap (uses competitive insights) |

## Traceability

This command contributes to checkpoint **CP-6.5** in the Discovery workflow.

Outputs trace to:
- `PRODUCT_VISION.md` (informs differentiation)
- `PRODUCT_STRATEGY.md` (validates positioning)
- `PAIN_POINTS.md` (identifies unmet needs competitors miss)
- `JOBS_TO_BE_DONE.md` (validates jobs competitors don't solve)
