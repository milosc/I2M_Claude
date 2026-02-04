# Discovery Command Reference

**Stage**: 1 (Discovery)
**Output**: `ClientAnalysis_{SystemName}/`
**Status**: Production

---

## Available Commands

| Command | Mode | Description | Performance |
|---------|------|-------------|-------------|
| `/discovery` | Sequential | Traditional single-session execution | Baseline |
| `/discovery-multiagent` | Massively Parallel | Multi-agent with per-file spawning | **60-70% faster** |
| `/discovery-resume` | Sequential | Resume from last checkpoint | - |
| `/discovery-audit` | Validation | Zero hallucination audit | - |
| `/discovery-feedback` | Change Management | Process feedback with impact analysis | - |
| `/discovery-competitive-analysis` | Standalone | Competitive intelligence with threat/opportunity scoring | - |

---

## Primary Commands

### `/discovery <SystemName> <InputPath>`

**Mode**: Sequential
**File**: `.claude/commands/discovery.md`

Traditional Discovery execution in a single session. All skills loaded sequentially.

**Usage**:
```bash
/discovery InventorySystem Client_Materials/
```

**When to use**:
- Simple projects (<10 client materials)
- Debugging/testing
- When multi-agent infrastructure is unavailable

**Performance**: Baseline (100%)

---

### `/discovery-multiagent <SystemName> <InputPath>` ⚡

**Mode**: Massively Parallel (v2.0)
**File**: `.claude/commands/discovery-multiagent.md`
**Registry**: `.claude/agents/DISCOVERY_AGENT_REGISTRY.json`
**Architecture**: Flat spawning (main session spawns all agents directly)

Multi-agent Discovery with per-file spawning for massive parallelization.

**Usage**:
```bash
# Start new discovery (visible terminals - default)
/discovery-multiagent InventorySystem Client_Materials/

# Headless mode (no visible terminal windows)
/discovery-multiagent InventorySystem Client_Materials/ --headless

# Resume from last checkpoint
/discovery-multiagent InventorySystem --resume

# Resume from specific checkpoint
/discovery-multiagent InventorySystem --resume --checkpoint 3

# Retry failed agents
/discovery-multiagent InventorySystem --resume --retry-failed
```

**Arguments**:
- `<SystemName>` - Required: Name of system being analyzed
- `<InputPath>` - Required: Path to folder containing client materials
- `--resume` - Resume from last failed/incomplete agent spawn
- `--checkpoint N` - Resume from specific checkpoint (0-11)
- `--retry-failed` - Retry previously failed agents instead of skipping
- `--headless` - Enable headless mode (no visible terminal windows)

**Architecture**:

```
Main Session (discovery-multiagent command)
├→ CP-1: Material Analysis [MASSIVE PARALLEL]
│  ├→ Task(interview-analyst-1) [1M context, Sonnet]
│  ├→ Task(interview-analyst-2) [1M context, Sonnet]
│  ├→ Task(interview-analyst-N) [1M context, Sonnet]
│  ├→ Task(data-analyst) [Sonnet]
│  └→ Task(design-analyst) [Sonnet]
├→ CP-1.5: PDF Analysis [PARALLEL]
│  ├→ Task(pdf-analyst-1) [Sonnet]
│  └→ Task(pdf-analyst-N) [Sonnet]
├→ CP-2: Task(pain-point-validator) [Sonnet]
├→ CP-3: Persona Generation [PARALLEL]
│  ├→ Task(persona-generator-1) [Sonnet]
│  └→ Task(persona-generator-N) [Sonnet]
├→ CP-4: Task(jtbd-extractor) [Sonnet]
├→ CP-5: Task(vision-generator) [Sonnet]
├→ CP-6: Task(strategy-generator) [Sonnet]
├→ CP-7: Task(roadmap-generator) [Sonnet]
├→ CP-8: Task(kpis-generator) [Sonnet]
├→ CP-9: Design Specs [PARALLEL - 4 AGENTS]
│  ├→ Task(screen-specifier) [Sonnet]
│  ├→ Task(navigation-specifier) [Sonnet]
│  ├→ Task(data-fields-specifier) [Sonnet]
│  └→ Task(interaction-specifier) [Sonnet]
└→ CP-11: Task(cross-reference-validator) [Haiku]
```

**Key Features**:
- **Massive Parallelization**: One interview-analyst per interview file (5 interviews = 7 parallel agents at CP-1)
- **Extended Context**: interview-analyst uses 1M context window for long transcripts
- **Model Strategy**: Sonnet for all agents except cross-reference-validator (Haiku)
- **Resume Capability**: Checkpoint-based recovery with spawn manifest tracking
- **Spawn Verification**: 30-second timeout with 3 retry attempts
- **Terminal Modes**: Visible (default) or headless (--headless flag)

**Performance**: **60-70% faster** than sequential mode
**Token Reduction**: 76% (62,500 → 15,000 peak)
**Agent Count**: 15 base agents + N instances for interviews/PDFs/personas

**When to use**:
- Complex projects (>5 client materials)
- Time-sensitive deliverables
- Large interview sets (10+ interviews)
- Production use cases

**Prerequisites**:
- Agent infrastructure: `.claude/agents/DISCOVERY_AGENT_REGISTRY.json`
- Agent coordinator: `.claude/hooks/agent_coordinator.py`
- Dependencies installed: `/htec-libraries-init`

**State Files**:
- `_state/discovery_agent_spawn_manifest.json` - Tracks all agent executions
- `_state/agent_sessions.json` - Active agent sessions
- `_state/discovery_progress.json` - Checkpoint progress

---

## Utility Commands

### `/discovery-competitive-analysis <SystemName> [OPTIONS]`

**File**: `.claude/commands/discovery-competitive-analysis.md`

Standalone competitive intelligence analysis with threat/opportunity scoring and sales battlecards.

**Usage**:
```bash
# Basic (auto-discover competitors)
/discovery-competitive-analysis InventorySystem

# With known competitors
/discovery-competitive-analysis InventorySystem --competitors "NetSuite,SAP,Zoho"

# With market segment definition
/discovery-competitive-analysis InventorySystem --segment "SMB inventory SaaS"

# Deep dive analysis
/discovery-competitive-analysis InventorySystem --competitors "NetSuite,SAP" --depth deep_dive
```

**Arguments**:
- `<SystemName>` - Required: System name (must have completed Discovery)
- `--competitors` - Optional: Comma-separated list of known competitors
- `--segment` - Optional: Market niche definition
- `--depth` - Optional: `quick_scan`, `standard` (default), `deep_dive`

**Prerequisites**: Requires completed Discovery outputs (PRODUCT_VISION.md, PRODUCT_STRATEGY.md, etc.)

**Outputs** (to `ClientAnalysis_<SystemName>/03-strategy/`):
- `COMPETITIVE_LANDSCAPE.md` - Market map with competitor categorization
- `THREAT_OPPORTUNITY_MATRIX.md` - Scored threat/opportunity analysis
- `DIFFERENTIATION_BLUEPRINT.md` - USP and positioning strategy
- `COMPETITIVE_INTELLIGENCE_SUMMARY.md` - Executive summary
- `battlecards/*.md` - Per-competitor sales enablement cards

**When to use**:
- After Discovery to enrich strategy with competitive insights
- Standalone refresh of competitive analysis
- Before roadmap planning (informs feature prioritization)

---

### `/discovery-resume`

Resume sequential Discovery from last checkpoint.

**Usage**:
```bash
/discovery-resume InventorySystem
```

**Note**: For multi-agent resume, use `/discovery-multiagent --resume` instead.

---

### `/discovery-audit`

**File**: `.claude/commands/discovery-audit.md`

Run zero hallucination audit to verify every claim has source citation.

**Usage**:
```bash
/discovery-audit InventorySystem
```

**Checks**:
- All persona traits have interview citations
- All pain points have source evidence
- All JTBD have user quotes
- No orphaned claims

**Output**: `05-documentation/VALIDATION_REPORT.md`

---

### `/discovery-feedback`

**File**: `.claude/commands/discovery-feedback.md`

Process feedback and change requests using Reflexion-enhanced impact analysis.

**Usage**:
```bash
/discovery-feedback InventorySystem
```

**Workflow**:
1. **Impact Analysis** (Reflexion Actor)
2. **Impact Validation** (Reflexion Evaluator)
3. **Implementation Plan** (Reflexion Actor)
4. **Plan Validation** (Reflexion Evaluator)
5. **Execution** (Reflexion Actor)
6. **Review** (Reflexion Evaluator)

**Features**:
- Multi-perspective critical review
- Kaizen PDCA integration
- Memorization of lessons learned
- Full traceability preservation

---

## 13 Checkpoints

| CP | Phase | Agents | Execution Mode |
|----|-------|--------|----------------|
| 0 | Initialize | Main session | Direct |
| 1 | Material Analysis | interview-analyst (N), data-analyst, design-analyst | **Massive Parallel** |
| 1.5 | PDF Analysis | pdf-analyst (N) | **Parallel** |
| 2 | Pain Point Validation | pain-point-validator | Sequential |
| 3 | Persona Generation | persona-generator (N) | **Parallel** |
| 4 | JTBD Extraction | jtbd-extractor | Sequential |
| 5 | Vision | vision-generator | Sequential |
| 6 | Strategy | strategy-generator | Sequential |
| 6.5 | **Competitive Intelligence** | competitor-analyst | Sequential |
| 7 | Roadmap | roadmap-generator | Sequential |
| 8 | KPIs | kpis-generator | Sequential |
| 9 | Design Specs | screen-specifier, navigation-specifier, data-fields-specifier, interaction-specifier | **Parallel (4 agents)** |
| 10 | Documentation | Main session | Direct |
| 11 | Validation (BLOCKING) | cross-reference-validator | Sequential |

**Note**: N = number of files (interviews, PDFs, personas)

### CP-6.5: Competitive Intelligence (New)

The `competitor-analyst` agent performs strategic intelligence synthesis:
- **Input**: PRODUCT_VISION.md, PRODUCT_STRATEGY.md, personas/, JOBS_TO_BE_DONE.md, PAIN_POINTS.md
- **Output**:
  - `03-strategy/COMPETITIVE_LANDSCAPE.md` - Market map with competitor categorization
  - `03-strategy/THREAT_OPPORTUNITY_MATRIX.md` - Quantitative threat/opportunity analysis
  - `03-strategy/DIFFERENTIATION_BLUEPRINT.md` - USP definition and positioning
  - `03-strategy/COMPETITIVE_INTELLIGENCE_SUMMARY.md` - Executive summary
  - `03-strategy/battlecards/[COMPETITOR]_BATTLECARD.md` - Per-competitor sales enablement
- **Dependencies**: Requires CP-6 (Strategy) completed
- **Blocks**: CP-7 (Roadmap) - competitive insights inform feature prioritization

---

## Output Structure

```
ClientAnalysis_{SystemName}/
├── 00-management/
│   └── project_summary.md
├── 01-analysis/
│   ├── interviews/{Interview_Name}_Analysis.md (per interview)
│   ├── data/DATA_ANALYSIS.md
│   ├── design/DESIGN_ANALYSIS.md
│   └── PAIN_POINTS.md
├── 02-research/
│   ├── personas/PERSONA_{ROLE}.md (per persona)
│   └── JOBS_TO_BE_DONE.md
├── 03-strategy/
│   ├── PRODUCT_VISION.md
│   ├── PRODUCT_STRATEGY.md
│   ├── PRODUCT_ROADMAP.md
│   └── KPIS_AND_GOALS.md
├── 04-design-specs/
│   ├── screen-definitions.md
│   ├── navigation-structure.md
│   ├── data-fields.md
│   └── interaction-patterns.md
└── 05-documentation/
    ├── INDEX.md
    ├── README.md
    └── VALIDATION_REPORT.md
```

---

## Traceability

All Discovery outputs maintain traceability chains:

```
CM-XXX (Client Material)
  └→ PP-X.X (Pain Point)
      └→ JTBD-X.X (Job To Be Done)
          └→ REQ-XXX (Requirement)
              └→ SCR-XXX (Screen)
```

**Registries**:
- `traceability/pain_point_registry.json`
- `traceability/jtbd_registry.json`
- `traceability/requirements_registry.json`
- `traceability/client_facts_registry.json`

---

## Quality Gates

| Checkpoint | Gate | Requirement |
|------------|------|-------------|
| CP-2 | Pain Point Extraction | Min 3 pain points per interview |
| CP-3 | Persona Generation | Min 2 personas |
| CP-11 | Traceability Validation | 100% P0 coverage (BLOCKING) |

**Blocking Gate**: CP-11 must achieve 100% P0 traceability or stage fails.

---

## Error Handling

### One Attempt Rule

When processing client materials:
1. **Log** the failure to `_state/FAILURES_LOG.md`
2. **Skip** the item immediately
3. **Continue** to next item

**Never**:
- ❌ Retry operations
- ❌ Try different libraries
- ❌ Ask user (unless blocking error)

### Skip Triggers (Technical)
- PDF too large (>30 pages without chunking)
- ModuleNotFoundError
- Exit codes 1/127
- Timeout, Permission denied

### Correction Triggers (Quality)
- Missing deliverables
- Traceability gaps
- Empty/placeholder files
- Quality gate failures

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/discovery-status` | Show current progress |
| `/discovery-trace` | Review traceability coverage |
| `/discovery-export` | Package for Prototype stage |
| `/discovery-competitive-analysis` | Standalone competitive intelligence |
| `/htec-libraries-init` | Install dependencies |
| `/integrity-check` | Cross-stage validation |

---

## Next Stage

After Discovery completion, proceed to Prototype:

```bash
/prototype InventorySystem
```

Or for multi-agent prototype:

```bash
/prototype-multiagent InventorySystem
```

---

**Version**: 2.0.0 (Massively Parallel Multi-Agent)
**Last Updated**: 2026-01-25
