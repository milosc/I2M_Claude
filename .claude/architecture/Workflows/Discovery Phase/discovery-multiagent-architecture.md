# Discovery Multi-Agent Architecture Plan

**Version**: 2.0.0
**Date**: 2026-01-25
**Status**: Design Proposal (Updated with Enhanced Parallelization)
**Goal**: Reduce token usage by 60-70% and enable massive parallel execution for Discovery phase

---

## Executive Summary

Transform the Discovery phase from sequential to **massively parallel** multi-agent execution, following the proven prototype-multiagent pattern. This will:

- **Reduce token usage** by 60-70% through agent specialization
- **Enable massive parallel execution** at 4 key points with per-file agent spawning:
  - **Material Analysis**: One agent per interview file + data-analyst + design-analyst (all parallel)
  - **PDF Analysis**: One agent per PDF (all parallel)
  - **Persona Generation**: One agent per user type (all parallel)
  - **Design Specs**: 4 spec agents (all parallel)
- **Improve execution time** by ~60-70% through aggressive parallelization (was 40-50%)
- **Maximize quality** by using Sonnet for all agents except validation (extended 1M context for interviews)
- **Preserve traceability** with proper lifecycle logging

### Key Updates in v2.0

1. **Interview Analysis**: One interview-analyst agent **per interview file** (was 1 agent for all)
2. **Extended Context**: interview-analyst uses **Sonnet 1M context window** for deep analysis
3. **Model Upgrade**: All agents use **Sonnet** except cross-reference-validator (Haiku)
4. **Execution Time**: Reduced from 50% to **60-70%** improvement due to interview parallelization

---

## Current Architecture (Sequential)

### Execution Flow

```
Main Session (Monolithic)
  ├─ Load ALL Discovery skills (~50k tokens context)
  ├─ CP-0: Initialize
  ├─ CP-1: Analyze Materials (sequential: interviews → spreadsheets → screenshots)
  ├─ CP-1.5: PDF Analysis (sequential: PDF1 → PDF2 → PDF3)
  ├─ CP-2: Extract Pain Points
  ├─ CP-3: Generate Personas (sequential: Persona1 → Persona2 → Persona3)
  ├─ CP-4: Extract JTBD
  ├─ CP-5-8: Strategy documents (sequential)
  ├─ CP-9: Design Specs (sequential: screens → navigation → data → interactions)
  ├─ CP-10: Documentation
  └─ CP-11: Validation
```

### Problems

1. **Context Rot**: Main session loads all 38 Discovery skills (~50k tokens)
2. **No Parallelization**: Sequential execution even for independent tasks
3. **Long Execution Time**: 5-7 PDFs analyzed sequentially = 30-45 minutes
4. **Memory Overhead**: All skills in context even when not needed

---

## Proposed Architecture (Multi-Agent)

### Orchestration Pattern

```
Main Session (Orchestrator)
  ├─ CP-0: Initialize (direct)
  │
  ├─ CP-1: Material Analysis (MASSIVE PARALLEL) ───┬─→ interview-analyst-1 (sonnet 1M ctx)
  │                                                 ├─→ interview-analyst-2 (sonnet 1M ctx)
  │                                                 ├─→ interview-analyst-N (sonnet 1M ctx)
  │                                                 ├─→ data-analyst (sonnet)
  │                                                 └─→ design-analyst (sonnet)
  │                                                 [5 interviews = 7 agents in parallel]
  │
  ├─ CP-1.5: PDF Analysis (PARALLEL) ──────────────┬─→ pdf-analyst-1 (sonnet)
  │                                                 ├─→ pdf-analyst-2 (sonnet)
  │                                                 └─→ pdf-analyst-N (sonnet)
  │
  ├─ CP-2: Pain Point Extraction ──────────────────→ pain-point-validator (sonnet)
  │
  ├─ CP-3: Persona Generation (PARALLEL) ──────────┬─→ persona-generator-1 (sonnet)
  │                                                 ├─→ persona-generator-2 (sonnet)
  │                                                 └─→ persona-generator-N (sonnet)
  │
  ├─ CP-4: JTBD Extraction ────────────────────────→ jtbd-extractor (sonnet)
  │
  ├─ CP-5: Vision ─────────────────────────────────→ vision-generator (sonnet)
  │
  ├─ CP-6: Strategy ───────────────────────────────→ strategy-generator (sonnet)
  │
  ├─ CP-7: Roadmap ────────────────────────────────→ roadmap-generator (sonnet)
  │
  ├─ CP-8: KPIs ───────────────────────────────────→ kpis-generator (sonnet)
  │
  ├─ CP-9: Design Specs (PARALLEL) ────────────────┬─→ screen-specifier (sonnet)
  │                                                 ├─→ navigation-specifier (sonnet)
  │                                                 ├─→ data-fields-specifier (sonnet)
  │                                                 └─→ interaction-specifier (sonnet)
  │
  ├─ CP-10: Documentation (direct)
  └─ CP-11: Validation ────────────────────────────→ cross-reference-validator (haiku)
```

### Model Strategy (v2.0)

**Sonnet (all agents except validator):**
- Higher quality analysis and synthesis
- Extended 1M context window for interview-analyst
- Cost increase justified by quality and parallelization speed gains

**Haiku (validation only):**
- cross-reference-validator uses checklist-based validation (structured task)
- Cost savings on final validation step

---

## Agent Specifications

### 1. Material Analysis Agents (CP-1)

#### interview-analyst (one per interview file)
- **Model**: `sonnet` with **1M context window** (claude-sonnet-4-20250514 or equivalent)
- **Context**: Interview analysis skill, pain point framework, quote extraction, role-specific patterns
- **Token Budget**: ~15k per agent (with 1M context capability for long interviews)
- **Input**: **Single interview file** (one `.md` or `.txt` from Client_Materials/Interviews/)
- **Output**:
  - `01-analysis/interviews/[Interview_Name]_Analysis.md`
  - Contributes to `client_facts_registry.json`
- **Execution**: **One agent spawned per interview file**, all running in parallel
- **Spawn Strategy**: Per-instance (similar to pdf-analyst)
- **Extended Context Benefit**: Can process very long interview transcripts (50-100 pages) without chunking

**Example**: 5 interview files = 5 interview-analyst agents running simultaneously

#### data-analyst
- **Model**: `sonnet` (deep pattern extraction and business rule inference)
- **Context**: Spreadsheet analysis skill, business rules extraction, validation patterns
- **Token Budget**: ~12k
- **Input**: All `.xlsx`, `.csv` files from Client_Materials/
- **Output**:
  - `01-analysis/data/DATA_ANALYSIS.md`
  - Contributes to `client_facts_registry.json`
- **Execution**: Parallel with all interview-analysts and design-analyst
- **Model Upgrade Rationale**: Sonnet provides better business rule inference from complex spreadsheets

#### design-analyst
- **Model**: `sonnet` (sophisticated visual pattern recognition and component taxonomy)
- **Context**: Screenshot analysis skill, UI component inventory, design pattern catalog
- **Token Budget**: ~12k
- **Input**: All `.png`, `.jpg` files from Client_Materials/
- **Output**:
  - `01-analysis/design/DESIGN_ANALYSIS.md`
  - Contributes to `client_facts_registry.json`
- **Execution**: Parallel with all interview-analysts and data-analyst
- **Model Upgrade Rationale**: Sonnet provides better design pattern recognition and component classification

**Parallelization Benefit (v2.0)**:
- **Example**: 5 interviews + 1 data + 1 design = **7 agents running simultaneously**
- **Sequential time**: 5×15min + 10min + 10min = 95 minutes
- **Parallel time**: max(15, 15, 15, 15, 15, 10, 10) = **15 minutes**
- **Speedup**: **6.3x** for material analysis (was 2.3x in v1.0)

---

### 2. PDF Analysis Agents (CP-1.5)

#### pdf-analyst (one per PDF)
- **Model**: `sonnet` (deep analysis, gap identification)
- **Context**: PDF analysis skill, chunking strategy, terminology extraction
- **Token Budget**: ~15k per agent
- **Input**: Single PDF file (with markdown chunks if >10 pages)
- **Output**:
  - `[PDF_Name]_Analysis/SYSTEM_KNOWLEDGE.md`
  - `[PDF_Name]_Analysis/TERMINOLOGY.md`
  - `[PDF_Name]_Analysis/GAP_ANALYSIS.md`
  - `[PDF_Name]_Analysis/SECTION_INDEX.md`
- **Execution**: One agent per PDF, all running in parallel
- **Scaling**: 5 PDFs = 5 agents running simultaneously = 5x speedup

**Parallelization Benefit**: N agents for N PDFs = N×speedup (typically 3-5x for projects with multiple PDFs)

---

### 3. Pain Point Validation Agent (CP-2)

#### pain-point-validator
- **Model**: `sonnet` (sophisticated pain point extraction and validation)
- **Context**: Pain point extraction rules, citation validation, severity classification, pattern recognition
- **Token Budget**: ~12k
- **Input**:
  - `01-analysis/interviews/[Interview_Name]_Analysis.md` (all interview analyses)
  - `01-analysis/data/DATA_ANALYSIS.md`
  - `01-analysis/design/DESIGN_ANALYSIS.md`
  - `client_facts_registry.json`
- **Output**: `01-analysis/PAIN_POINTS.md` with PP-X.Y IDs
- **Execution**: Sequential (depends on CP-1 completion)
- **Model Upgrade Rationale**: Sonnet provides better pain point synthesis across multiple sources and nuanced severity classification

---

### 4. Persona Generation Agents (CP-3)

#### persona-generator (one per user type)
- **Model**: `sonnet` (rich narrative generation)
- **Context**: Persona template, day-in-life framework, quote integration
- **Token Budget**: ~12k per agent
- **Input**: ANALYSIS_SUMMARY.md, PAIN_POINTS.md, specific user type context
- **Output**: `personas/PERSONA_[ROLE_SLUG].md`
- **Execution**: One agent per user type, all running in parallel
- **Scaling**: 3 user types = 3 agents = 3x speedup

**Parallelization Benefit**: N agents for N user types = N×speedup (typically 2-4x)

---

### 5. JTBD Extraction Agent (CP-4)

#### jtbd-extractor
- **Model**: `sonnet` (transformation of pain points to jobs)
- **Context**: JTBD framework ("When... I want to... So that..."), prioritization
- **Token Budget**: ~12k
- **Input**: PAIN_POINTS.md, all persona files
- **Output**: JOBS_TO_BE_DONE.md with JTBD-X.Y IDs
- **Execution**: Sequential (depends on CP-3 completion)

---

### 6. Strategy Document Agents (CP-5 to CP-8)

#### vision-generator (CP-5)
- **Model**: `sonnet` (strategic synthesis)
- **Context**: Vision template, value proposition framework
- **Token Budget**: ~12k
- **Input**: JOBS_TO_BE_DONE.md, personas
- **Output**: PRODUCT_VISION.md
- **Execution**: Sequential

#### strategy-generator (CP-6)
- **Model**: `sonnet` (strategic analysis and competitive positioning)
- **Context**: Strategy template, competitive positioning, market analysis
- **Token Budget**: ~12k
- **Input**: PRODUCT_VISION.md, JOBS_TO_BE_DONE.md
- **Output**: PRODUCT_STRATEGY.md
- **Execution**: Sequential
- **Model Upgrade Rationale**: Sonnet provides deeper strategic insights and competitive analysis

#### roadmap-generator (CP-7)
- **Model**: `sonnet` (prioritization and phasing)
- **Context**: Roadmap template, RICE scoring, dependency analysis
- **Token Budget**: ~12k
- **Input**: JOBS_TO_BE_DONE.md, PRODUCT_STRATEGY.md
- **Output**: PRODUCT_ROADMAP.md, requirements_registry.json
- **Execution**: Sequential

#### kpis-generator (CP-8)
- **Model**: `sonnet` (metrics extraction and OKR formulation)
- **Context**: KPI template, SMART criteria, OKR framework
- **Token Budget**: ~12k
- **Input**: PRODUCT_VISION.md, PRODUCT_ROADMAP.md
- **Output**: KPIS_AND_GOALS.md
- **Execution**: Sequential
- **Model Upgrade Rationale**: Sonnet provides better alignment between KPIs and strategic goals

---

### 7. Design Specification Agents (CP-9)

#### screen-specifier
- **Model**: `sonnet` (complex screen definitions with flows)
- **Context**: Screen definition template, user flow mapping, state management
- **Token Budget**: ~12k
- **Input**: JOBS_TO_BE_DONE.md, personas, PAIN_POINTS.md
- **Output**: screen-definitions.md with S-X.Y IDs
- **Execution**: Parallel with other spec agents

#### navigation-specifier
- **Model**: `sonnet` (sophisticated hierarchy and IA)
- **Context**: Navigation template, menu structure, information architecture patterns
- **Token Budget**: ~12k
- **Input**: screen-definitions.md (if screens complete first), JOBS_TO_BE_DONE.md
- **Output**: navigation-structure.md
- **Execution**: Parallel with other spec agents
- **Model Upgrade Rationale**: Sonnet provides better information architecture and navigation flow design

#### data-fields-specifier
- **Model**: `sonnet` (field extraction and complex validation logic)
- **Context**: Data field template, validation rules, business logic patterns
- **Token Budget**: ~12k
- **Input**:
  - `01-analysis/data/DATA_ANALYSIS.md`
  - `01-analysis/interviews/[Interview_Name]_Analysis.md` (all)
  - JOBS_TO_BE_DONE.md
- **Output**: data-fields.md
- **Execution**: Parallel with other spec agents
- **Model Upgrade Rationale**: Sonnet provides better validation rule inference and data relationship mapping

#### interaction-specifier
- **Model**: `sonnet` (interaction pattern synthesis)
- **Context**: Interaction pattern library, accessibility patterns, motion design
- **Token Budget**: ~12k
- **Input**: screen-definitions.md (if available), personas, PAIN_POINTS.md
- **Output**: interaction-patterns.md
- **Execution**: Parallel with other spec agents
- **Model Upgrade Rationale**: Sonnet provides better interaction pattern selection and accessibility considerations

**Parallelization Benefit**: 4 agents running simultaneously = 4x speedup for design specs

---

### 8. Cross-Reference Validation Agent (CP-11)

#### cross-reference-validator
- **Model**: `haiku` (checklist validation, traceability chains)
- **Context**: Validation rules, ID format patterns, traceability chains
- **Token Budget**: ~10k
- **Input**: All Discovery artifacts
- **Output**: VALIDATION_REPORT.md
- **Execution**: Sequential (final blocking gate)
- **Blocking**: Must achieve 100% P0 traceability to pass
- **Model Rationale**: Haiku is sufficient for structured validation checklist; cost savings on final step

---

## Parallel Execution Groups

### Group 1: Material Analysis (CP-1) - MASSIVELY PARALLEL

```
┌─────────────────────────────────────────────────────────────────────────┐
│ MASSIVE PARALLEL SPAWN (Single message, N+2 Task() calls)              │
├─────────────────────────────────────────────────────────────────────────┤
│ FOR EACH interview file (*.md, *.txt in Client_Materials/Interviews/): │
│   Task({                                                                │
│     agent: interview-analyst-${interviewName},                          │
│     model: "sonnet",                                                    │
│     context_window: "1M",  // Extended context for long interviews     │
│     input: ${interviewFilePath}                                         │
│   })                                                                    │
│                                                                         │
│ PLUS:                                                                   │
│ Task({ agent: data-analyst, model: "sonnet" })                         │
│ Task({ agent: design-analyst, model: "sonnet" })                       │
│                                                                         │
│ EXAMPLE: 5 interviews = 7 agents spawned in parallel                   │
│ AWAIT: All N+2 completions before CP-1.5                               │
└─────────────────────────────────────────────────────────────────────────┘

Estimated time (5 interviews):
- Sequential: 15+15+15+15+15 + 10 + 10 = 95 minutes
- Parallel: max(15, 15, 15, 15, 15, 10, 10) = 15 minutes
- Speedup: 6.3x

Estimated time (10 interviews):
- Sequential: 10×15 + 10 + 10 = 170 minutes
- Parallel: max(15, ..., 15, 10, 10) = 15 minutes
- Speedup: 11.3x
```

### Group 2: PDF Analysis (CP-1.5)
```
┌─────────────────────────────────────────────────────────────┐
│ PARALLEL SPAWN (Single message, N Task() calls)            │
├─────────────────────────────────────────────────────────────┤
│ FOR EACH PDF:                                               │
│   Task({                                                    │
│     agent: pdf-analyst-${pdfName},                          │
│     model: sonnet,                                          │
│     input: ${pdfPath},                                      │
│     chunks: ${chunksPath if >10 pages}                      │
│   })                                                        │
│                                                             │
│ AWAIT: All N completions before CP-2                        │
└─────────────────────────────────────────────────────────────┘

Estimated time:
- Sequential (5 PDFs): 8 + 8 + 8 + 8 + 8 = 40 minutes
- Parallel: max(8, 8, 8, 8, 8) = 8 minutes
- Speedup: 5x
```

### Group 3: Persona Generation (CP-3)
```
┌─────────────────────────────────────────────────────────────┐
│ PARALLEL SPAWN (Single message, N Task() calls)            │
├─────────────────────────────────────────────────────────────┤
│ FOR EACH USER_TYPE:                                         │
│   Task({                                                    │
│     agent: persona-generator-${roleSlug},                   │
│     model: sonnet,                                          │
│     userType: ${userType}                                   │
│   })                                                        │
│                                                             │
│ AWAIT: All N completions before CP-4                        │
└─────────────────────────────────────────────────────────────┘

Estimated time:
- Sequential (3 personas): 5 + 5 + 5 = 15 minutes
- Parallel: max(5, 5, 5) = 5 minutes
- Speedup: 3x
```

### Group 4: Design Specifications (CP-9)
```
┌─────────────────────────────────────────────────────────────┐
│ PARALLEL SPAWN (Single message, 4 Task() calls)            │
├─────────────────────────────────────────────────────────────┤
│ Task({ agent: screen-specifier, model: "sonnet" })         │
│ Task({ agent: navigation-specifier, model: "sonnet" })     │
│ Task({ agent: data-fields-specifier, model: "sonnet" })    │
│ Task({ agent: interaction-specifier, model: "sonnet" })    │
│                                                             │
│ AWAIT: All 4 completions before CP-10                      │
└─────────────────────────────────────────────────────────────┘

Estimated time:
- Sequential: 8 + 6 + 6 + 6 = 26 minutes
- Parallel: max(8, 6, 6, 6) = 8 minutes
- Speedup: 3.25x
```

---

## Dependency Graph

```
┌────────────────────────────────────────────────────────────────────┐
│                  DISCOVERY DEPENDENCY GRAPH                        │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  CP-0 (Initialize)                                                 │
│    ↓                                                               │
│  CP-1 (Material Analysis) ──┬── interview-analyst                 │
│    ↓                         ├── data-analyst         } PARALLEL  │
│    ↓                         └── design-analyst                    │
│    ↓                                                               │
│  CP-1.5 (PDF Analysis) ─────┬── pdf-analyst-1                     │
│    ↓                         ├── pdf-analyst-2        } PARALLEL  │
│    ↓                         └── pdf-analyst-N                     │
│    ↓                                                               │
│  CP-2 (Pain Points) ────────── pain-point-validator   SEQUENTIAL  │
│    ↓                                                               │
│  CP-3 (Personas) ───────────┬── persona-gen-1                     │
│    ↓                         ├── persona-gen-2        } PARALLEL  │
│    ↓                         └── persona-gen-N                     │
│    ↓                                                               │
│  CP-4 (JTBD) ───────────────── jtbd-extractor         SEQUENTIAL  │
│    ↓                                                               │
│  CP-5 (Vision) ─────────────── vision-generator       SEQUENTIAL  │
│    ↓                                                               │
│  CP-6 (Strategy) ───────────── strategy-generator     SEQUENTIAL  │
│    ↓                                                               │
│  CP-7 (Roadmap) ────────────── roadmap-generator      SEQUENTIAL  │
│    ↓                                                               │
│  CP-8 (KPIs) ───────────────── kpis-generator         SEQUENTIAL  │
│    ↓                                                               │
│  CP-9 (Design Specs) ───────┬── screen-specifier                  │
│    ↓                         ├── navigation-specifier  } PARALLEL │
│    ↓                         ├── data-fields-specifier             │
│    ↓                         └── interaction-specifier             │
│    ↓                                                               │
│  CP-10 (Documentation)                                MAIN SESSION│
│    ↓                                                               │
│  CP-11 (Validation) ─────────── cross-ref-validator   BLOCKING   │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## State Management

### Agent Spawn Manifest

Similar to prototype-multiagent, maintain `_state/discovery_agent_spawn_manifest.json`:

```json
{
  "schema_version": "1.0.0",
  "system_name": "InventorySystem",
  "stage": "discovery",
  "started_at": "2026-01-25T12:00:00Z",
  "updated_at": "2026-01-25T12:45:00Z",
  "mode": "multi_agent",

  "agents": [
    {
      "agent_id": "interview-analyst",
      "checkpoint": 1,
      "phase": "material_analysis",
      "status": "completed",
      "model": "sonnet",
      "priority": "normal",

      "spawn_info": {
        "spawn_attempts": 1,
        "max_attempts": 3,
        "task_call_id": "task-interview-001",
        "session_id": "sess-interview-001",
        "spawn_method": "general-purpose",
        "spawn_requested_at": "2026-01-25T12:05:00Z",
        "spawn_verified_at": "2026-01-25T12:05:02Z"
      },

      "execution": {
        "started_at": "2026-01-25T12:05:02Z",
        "completed_at": "2026-01-25T12:18:00Z",
        "duration_seconds": 778
      },

      "outputs": {
        "expected": ["01-analysis/ANALYSIS_SUMMARY.md (interviews section)"],
        "actual": ["01-analysis/ANALYSIS_SUMMARY.md"]
      },

      "dependencies": {
        "depends_on": [],
        "blocks": ["pain-point-validator"]
      }
    },
    {
      "agent_id": "pdf-analyst-user-manual",
      "checkpoint": 1.5,
      "phase": "pdf_analysis",
      "status": "completed",
      "model": "sonnet",
      "pdf_name": "User_Manual.pdf",
      "page_count": 45,
      "chunks_used": true,

      "spawn_info": {
        "spawn_attempts": 1,
        "task_call_id": "task-pdf-001",
        "session_id": "sess-pdf-001"
      },

      "outputs": {
        "expected": [
          "01-analysis/User_Manual_Analysis/SYSTEM_KNOWLEDGE.md",
          "01-analysis/User_Manual_Analysis/TERMINOLOGY.md",
          "01-analysis/User_Manual_Analysis/GAP_ANALYSIS.md"
        ],
        "actual": [
          "01-analysis/User_Manual_Analysis/SYSTEM_KNOWLEDGE.md",
          "01-analysis/User_Manual_Analysis/TERMINOLOGY.md",
          "01-analysis/User_Manual_Analysis/GAP_ANALYSIS.md",
          "01-analysis/User_Manual_Analysis/SECTION_INDEX.md"
        ]
      }
    },
    {
      "agent_id": "persona-generator-warehouse-operator",
      "checkpoint": 3,
      "phase": "personas",
      "status": "completed",
      "model": "sonnet",
      "user_type": "Warehouse Operator",

      "outputs": {
        "expected": ["02-research/personas/PERSONA_WAREHOUSE_OPERATOR.md"],
        "actual": ["02-research/personas/PERSONA_WAREHOUSE_OPERATOR.md"]
      }
    }
  ],

  "phases": {
    "CP-0": { "status": "completed", "agents": [] },
    "CP-1": {
      "status": "completed",
      "agents": ["interview-analyst", "data-analyst", "design-analyst"],
      "completed_at": "2026-01-25T12:20:00Z"
    },
    "CP-1.5": {
      "status": "completed",
      "agents": ["pdf-analyst-user-manual", "pdf-analyst-tech-spec"],
      "completed_at": "2026-01-25T12:35:00Z"
    },
    "CP-3": {
      "status": "completed",
      "agents": [
        "persona-generator-warehouse-operator",
        "persona-generator-warehouse-supervisor",
        "persona-generator-inventory-manager"
      ],
      "completed_at": "2026-01-25T12:45:00Z"
    }
  },

  "statistics": {
    "total_agents_planned": 18,
    "total_agents_completed": 12,
    "total_agents_in_progress": 2,
    "total_agents_failed": 0,
    "average_spawn_verification_time_ms": 1250
  }
}
```

### Progress Tracking

Maintain `_state/discovery_progress.json` with checkpoint status:

```json
{
  "current_checkpoint": 4,
  "status": "in_progress",
  "overall_progress": 36,
  "last_updated": "2026-01-25T12:45:00Z",

  "checkpoints": {
    "0": { "status": "completed", "completed_at": "2026-01-25T12:02:00Z" },
    "1": { "status": "completed", "agents_spawned": 3, "completed_at": "2026-01-25T12:20:00Z" },
    "1.5": { "status": "completed", "pdfs_analyzed": 2, "completed_at": "2026-01-25T12:35:00Z" },
    "2": { "status": "completed", "completed_at": "2026-01-25T12:38:00Z" },
    "3": { "status": "completed", "personas_generated": 3, "completed_at": "2026-01-25T12:45:00Z" },
    "4": { "status": "in_progress", "started_at": "2026-01-25T12:45:05Z" }
  }
}
```

---

## Command Implementation

### New Command: `/discovery-multiagent`

**File**: `.claude/commands/discovery-multiagent.md`

**Usage**:
```bash
# New run with visible terminals
/discovery-multiagent InventorySystem Client_Materials/

# New run with headless mode
/discovery-multiagent InventorySystem Client_Materials/ --headless

# Resume from last checkpoint
/discovery-multiagent InventorySystem --resume

# Resume and retry failed agents
/discovery-multiagent InventorySystem --resume --retry-failed

# Resume from specific checkpoint
/discovery-multiagent InventorySystem --resume --checkpoint 3
```

**Architecture**:
```
Main Session
  ├─ Load coordination rules (not all skills)
  ├─ Initialize state files
  ├─ For each checkpoint:
  │    ├─ Determine agents to spawn
  │    ├─ Spawn agents in parallel (single message, multiple Task() calls)
  │    ├─ Verify spawn (30s timeout per agent)
  │    ├─ Retry failed spawns (up to 3 attempts with countermeasures)
  │    ├─ Update manifest and progress
  │    └─ Continue to next checkpoint
  └─ Generate final report
```

---

## Token Usage Analysis

### Current Monolithic Approach

| Context Item | Token Count | When Loaded |
|--------------|-------------|-------------|
| Discovery skills (38) | ~35,000 | Always |
| Core rules | ~5,500 | Always |
| CLAUDE.md | ~8,000 | Always |
| Path-specific rules | ~14,000 | Auto-load |
| **Total** | **~62,500** | **Per session** |

### Multi-Agent Approach

#### Main Session (Orchestrator)
| Context Item | Token Count |
|--------------|-------------|
| Orchestrator agent definition | ~4,000 |
| Core rules | ~5,500 |
| CLAUDE.md (summary) | ~3,000 |
| State management | ~1,500 |
| **Total** | **~14,000** |

#### Specialized Agents (per agent)
| Agent Type | Context Token Count |
|------------|---------------------|
| interview-analyst | ~12,000 (1 skill + templates) |
| data-analyst | ~8,000 (1 skill) |
| design-analyst | ~8,000 (1 skill) |
| pdf-analyst | ~15,000 (1 skill + chunking) |
| persona-generator | ~12,000 (1 skill + templates) |
| jtbd-extractor | ~12,000 (1 skill + framework) |
| vision-generator | ~10,000 (1 skill + templates) |
| strategy-generator | ~8,000 (1 skill) |
| roadmap-generator | ~12,000 (1 skill + prioritization) |
| kpis-generator | ~8,000 (1 skill) |
| screen-specifier | ~12,000 (1 skill) |
| navigation-specifier | ~8,000 (1 skill) |
| data-fields-specifier | ~8,000 (1 skill) |
| interaction-specifier | ~8,000 (1 skill) |
| cross-reference-validator | ~10,000 (validation rules) |

### Token Savings

**Example: InventorySystem with 3 interviews, 2 PDFs, 3 user types**

#### Sequential (Current):
- Main session: 62,500 tokens throughout entire execution
- Total: 62,500 tokens

#### Multi-Agent (Proposed):
- Main session orchestrator: 14,000 tokens
- CP-1 parallel (3 agents): max(12k, 8k, 8k) = 12,000 tokens
- CP-1.5 parallel (2 agents): max(15k, 15k) = 15,000 tokens
- CP-2 (1 agent): 10,000 tokens
- CP-3 parallel (3 agents): max(12k, 12k, 12k) = 12,000 tokens
- CP-4 (1 agent): 12,000 tokens
- CP-5 (1 agent): 10,000 tokens
- CP-6 (1 agent): 8,000 tokens
- CP-7 (1 agent): 12,000 tokens
- CP-8 (1 agent): 8,000 tokens
- CP-9 parallel (4 agents): max(12k, 8k, 8k, 8k) = 12,000 tokens
- CP-11 (1 agent): 10,000 tokens

**Peak context**: 15,000 tokens (vs. 62,500)
**Savings**: 76% reduction in peak token usage

---

## Execution Time Analysis

### Current Sequential Execution

| Checkpoint | Activity | Estimated Time |
|------------|----------|----------------|
| CP-0 | Initialize | 1 min |
| CP-1 | Analyze materials (sequential) | 35 min |
| CP-1.5 | Analyze PDFs (sequential, 5 PDFs) | 40 min |
| CP-2 | Extract pain points | 5 min |
| CP-3 | Generate personas (sequential, 3) | 15 min |
| CP-4 | Extract JTBD | 5 min |
| CP-5 | Generate vision | 5 min |
| CP-6 | Generate strategy | 3 min |
| CP-7 | Generate roadmap | 8 min |
| CP-8 | Generate KPIs | 3 min |
| CP-9 | Generate specs (sequential) | 20 min |
| CP-10 | Documentation | 3 min |
| CP-11 | Validation | 5 min |
| **Total** | **Sequential** | **~148 min (2.5 hours)** |

### Multi-Agent Parallel Execution

| Checkpoint | Activity | Estimated Time | Speedup |
|------------|----------|----------------|---------|
| CP-0 | Initialize | 1 min | - |
| CP-1 | Analyze materials (parallel, 3) | 15 min | 2.3x |
| CP-1.5 | Analyze PDFs (parallel, 5) | 8 min | 5x |
| CP-2 | Extract pain points | 5 min | - |
| CP-3 | Generate personas (parallel, 3) | 5 min | 3x |
| CP-4 | Extract JTBD | 5 min | - |
| CP-5 | Generate vision | 5 min | - |
| CP-6 | Generate strategy | 3 min | - |
| CP-7 | Generate roadmap | 8 min | - |
| CP-8 | Generate KPIs | 3 min | - |
| CP-9 | Generate specs (parallel, 4) | 8 min | 2.5x |
| CP-10 | Documentation | 3 min | - |
| CP-11 | Validation | 5 min | - |
| **Total** | **Parallel** | **~74 min (1.25 hours)** | **2x overall** |

**Time Savings**: 50% reduction (148 min → 74 min)

---

## Error Handling & Resilience

### Spawn Verification Protocol

Similar to prototype-multiagent:

1. **Attempt 1**: Spawn with standard prompt
2. **Verification**: Check `_state/agent_sessions.json` for new entry (30s timeout)
3. **Attempt 2** (if failed): Spawn with explicit session ID in prompt
4. **Attempt 3** (if failed): Fallback to general-purpose agent with role instructions
5. **Block** (if all failed): Log error, mark agent as blocked, request user intervention

### Retry Countermeasures

```javascript
const retryStrategies = {
  attempt1: "retry_same",           // Same prompt, may be transient issue
  attempt2: "retry_with_session",   // Add explicit session ID
  attempt3: "fallback_general"      // Use general-purpose agent
};
```

### Resume Logic

```bash
/discovery-multiagent InventorySystem --resume
```

**Resume behavior:**
1. Load `_state/discovery_agent_spawn_manifest.json`
2. Find last incomplete checkpoint
3. For each agent at that checkpoint:
   - If `status === "completed"` → Skip
   - If `status === "failed"` → Skip (unless `--retry-failed`)
   - If `status === "in_progress"` → Check heartbeat:
     - If heartbeat < 5 min → Wait for completion
     - If heartbeat > 5 min → Treat as stale, retry
   - If `status === "not_started"` → Spawn agent
4. Continue normal flow from resumed checkpoint

---

## Quality Gates

### Blocking Gates

| Checkpoint | Gate | Requirement |
|------------|------|-------------|
| CP-11 | Traceability | 100% P0 coverage, no CRITICAL violations |

### Non-Blocking Validations

All other checkpoints have validations that warn but don't block progression.

---

## Migration Strategy

### Phase 1: Create Infrastructure (Week 1)

1. **Create new command**: `.claude/commands/discovery-multiagent.md`
2. **Agent definitions**: Add to `.claude/agents/` for new agents:
   - `discovery-vision-generator.md`
   - `discovery-strategy-generator.md`
   - `discovery-roadmap-generator.md`
   - `discovery-kpis-generator.md`
   - `discovery-screen-specifier.md`
   - `discovery-navigation-specifier.md`
   - `discovery-data-fields-specifier.md`
   - `discovery-interaction-specifier.md`

3. **Update existing agents**: Optimize context for existing:
   - `discovery-interview-analyst.md` (reduce to only interview skills)
   - `discovery-data-analyst.md` (reduce to only data skills)
   - etc.

4. **State management**: Adapt spawn verification from prototype-multiagent

### Phase 2: Implement Parallel Groups (Week 2)

1. **Group 1**: Material Analysis (CP-1)
   - Test parallel spawn of 3 agents
   - Verify output merging into ANALYSIS_SUMMARY.md
   - Validate spawn verification

2. **Group 2**: PDF Analysis (CP-1.5)
   - Test with 1, 2, 5 PDFs
   - Verify chunking strategy
   - Validate parallel output folders

3. **Group 3**: Persona Generation (CP-3)
   - Test with 1, 3, 5 personas
   - Verify parallel generation
   - Validate output consistency

4. **Group 4**: Design Specs (CP-9)
   - Test parallel spec generation
   - Verify dependency handling
   - Validate completeness

### Phase 3: Integration Testing (Week 3)

1. **Full pipeline test**: Run `/discovery-multiagent` on InventorySystem
2. **Compare outputs**: Ensure parity with `/discovery` output quality
3. **Measure metrics**:
   - Token usage per agent
   - Execution time per checkpoint
   - Spawn verification success rate
   - Overall completion time

### Phase 4: Production Rollout (Week 4)

1. **Documentation update**: Update CLAUDE.md with new command
2. **User testing**: Run on 2-3 real client materials
3. **Fallback strategy**: Keep `/discovery` command as fallback
4. **Deprecation plan**: Phase out `/discovery` after 3 successful projects

---

## Agent Registry

Create `.claude/agents/discovery/DISCOVERY_AGENT_REGISTRY.json`:

```json
{
  "schema_version": "2.0.0",
  "stage": "discovery",
  "total_agents": 15,
  "notes": "v2.0: Massively parallel interview analysis, all agents use sonnet except cross-ref-validator",

  "agents": [
    {
      "agent_id": "interview-analyst",
      "checkpoint": 1,
      "model": "sonnet",
      "context_window": "1M",
      "subagent_type": "general-purpose",
      "parallel_group": "material_analysis",
      "description": "Extract pain points, workflows, quotes from interview transcripts",
      "skills_required": ["Discovery_InterviewAnalyst"],
      "input_file_patterns": ["*.md", "*.txt"],
      "output_files": ["01-analysis/interviews/[Interview_Name]_Analysis.md"],
      "spawn_per_instance": true,
      "instance_key": "interview_file"
    },
    {
      "agent_id": "data-analyst",
      "checkpoint": 1,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": "material_analysis",
      "description": "Extract business rules, field definitions from spreadsheets",
      "skills_required": ["Discovery_DataAnalyst"],
      "input_file_patterns": ["*.xlsx", "*.csv"],
      "output_files": ["01-analysis/data/DATA_ANALYSIS.md"]
    },
    {
      "agent_id": "design-analyst",
      "checkpoint": 1,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": "material_analysis",
      "description": "Extract component inventory, navigation patterns from screenshots",
      "skills_required": ["Discovery_DesignAnalyst"],
      "input_file_patterns": ["*.png", "*.jpg"],
      "output_files": ["01-analysis/design/DESIGN_ANALYSIS.md"]
    },
    {
      "agent_id": "pdf-analyst",
      "checkpoint": 1.5,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": "pdf_analysis",
      "description": "Deep analysis of PDF technical documentation",
      "skills_required": ["Discovery_PdfAnalyst"],
      "input_file_patterns": ["*.pdf"],
      "output_files": [
        "01-analysis/[PDF_Name]_Analysis/SYSTEM_KNOWLEDGE.md",
        "01-analysis/[PDF_Name]_Analysis/TERMINOLOGY.md",
        "01-analysis/[PDF_Name]_Analysis/GAP_ANALYSIS.md"
      ],
      "spawn_per_instance": true,
      "instance_key": "pdf_name"
    },
    {
      "agent_id": "pain-point-validator",
      "checkpoint": 2,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": null,
      "description": "Extract and validate pain points with citations",
      "skills_required": ["Discovery_PainPointValidator"],
      "output_files": ["01-analysis/PAIN_POINTS.md"]
    },
    {
      "agent_id": "persona-generator",
      "checkpoint": 3,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": "personas",
      "description": "Generate rich persona documents",
      "skills_required": ["Discovery_PersonaGenerator"],
      "output_files": ["02-research/personas/PERSONA_[ROLE].md"],
      "spawn_per_instance": true,
      "instance_key": "user_type"
    },
    {
      "agent_id": "jtbd-extractor",
      "checkpoint": 4,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": null,
      "description": "Transform pain points to JTBD statements",
      "skills_required": ["Discovery_JTBDExtractor"],
      "output_files": ["02-research/JOBS_TO_BE_DONE.md"]
    },
    {
      "agent_id": "vision-generator",
      "checkpoint": 5,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": null,
      "description": "Articulate product vision and value proposition",
      "skills_required": ["Discovery_VisionGenerator"],
      "output_files": ["03-strategy/PRODUCT_VISION.md"]
    },
    {
      "agent_id": "strategy-generator",
      "checkpoint": 6,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": null,
      "description": "Define product strategy and competitive positioning",
      "skills_required": ["Discovery_StrategyGenerator"],
      "output_files": ["03-strategy/PRODUCT_STRATEGY.md"]
    },
    {
      "agent_id": "roadmap-generator",
      "checkpoint": 7,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": null,
      "description": "Create phased roadmap with prioritization",
      "skills_required": ["Discovery_RoadmapGenerator"],
      "output_files": ["03-strategy/PRODUCT_ROADMAP.md"]
    },
    {
      "agent_id": "kpis-generator",
      "checkpoint": 8,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": null,
      "description": "Define measurable KPIs and success metrics",
      "skills_required": ["Discovery_KPIsGenerator"],
      "output_files": ["03-strategy/KPIS_AND_GOALS.md"]
    },
    {
      "agent_id": "screen-specifier",
      "checkpoint": 9,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": "design_specs",
      "description": "Generate screen definitions with flows",
      "skills_required": ["Discovery_ScreenSpecifier"],
      "output_files": ["04-design-specs/screen-definitions.md"]
    },
    {
      "agent_id": "navigation-specifier",
      "checkpoint": 9,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": "design_specs",
      "description": "Generate navigation structure and menu hierarchy",
      "skills_required": ["Discovery_NavigationSpecifier"],
      "output_files": ["04-design-specs/navigation-structure.md"]
    },
    {
      "agent_id": "data-fields-specifier",
      "checkpoint": 9,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": "design_specs",
      "description": "Generate data field definitions and validation rules",
      "skills_required": ["Discovery_DataFieldsSpecifier"],
      "output_files": ["04-design-specs/data-fields.md"]
    },
    {
      "agent_id": "interaction-specifier",
      "checkpoint": 9,
      "model": "sonnet",
      "subagent_type": "general-purpose",
      "parallel_group": "design_specs",
      "description": "Generate interaction patterns catalog",
      "skills_required": ["Discovery_InteractionSpecifier"],
      "output_files": ["04-design-specs/interaction-patterns.md"]
    },
    {
      "agent_id": "cross-reference-validator",
      "checkpoint": 11,
      "model": "haiku",
      "subagent_type": "general-purpose",
      "parallel_group": null,
      "description": "Validate traceability chains (BLOCKING)",
      "skills_required": ["Discovery_CrossReferenceValidator"],
      "output_files": ["05-documentation/VALIDATION_REPORT.md"],
      "blocking": true
    }
  ],

  "parallel_groups": {
    "material_analysis": {
      "checkpoint": 1,
      "agents": ["interview-analyst", "data-analyst", "design-analyst"],
      "execution": "parallel",
      "notes": "interview-analyst spawns one instance per interview file",
      "spawn_per_instance_agents": ["interview-analyst"],
      "merge_strategy": "separate_files_then_merge"
    },
    "pdf_analysis": {
      "checkpoint": 1.5,
      "agents": ["pdf-analyst"],
      "execution": "parallel",
      "spawn_per_instance": true,
      "instance_key": "pdf_name",
      "merge_strategy": "separate_folders"
    },
    "personas": {
      "checkpoint": 3,
      "agents": ["persona-generator"],
      "execution": "parallel",
      "spawn_per_instance": true,
      "instance_key": "user_type",
      "merge_strategy": "separate_files"
    },
    "design_specs": {
      "checkpoint": 9,
      "agents": [
        "screen-specifier",
        "navigation-specifier",
        "data-fields-specifier",
        "interaction-specifier"
      ],
      "execution": "parallel",
      "merge_strategy": "separate_files"
    }
  }
}
```

---

## Benefits Summary

### 1. Token Usage Reduction

- **Current**: 62,500 tokens loaded throughout execution
- **Proposed**: 15,000 tokens peak (per agent)
- **Savings**: 76% reduction in peak token usage
- **Cost impact**: ~70% reduction in API costs for Discovery

### 2. Execution Time Reduction

- **Current**: ~148 minutes (2.5 hours) for typical project
- **Proposed**: ~74 minutes (1.25 hours) for same project
- **Savings**: 50% time reduction
- **Speedup factors**:
  - Material analysis: 2.3x
  - PDF analysis: 5x (for 5 PDFs)
  - Persona generation: 3x
  - Design specs: 2.5x

### 3. Context Efficiency

Each agent loads only:
- Its specific skill (1 of 38)
- Required templates
- Essential rules

vs. current approach where main session loads all 38 skills.

### 4. Scalability

- **PDFs**: 10 PDFs analyzed in parallel = 10x speedup
- **Personas**: 5 personas generated in parallel = 5x speedup
- Linear scaling with number of independent artifacts

### 5. Resilience

- Spawn verification with 3 retry attempts
- Automatic fallback to general-purpose agents
- Granular resume capability (checkpoint-level)
- User intervention only when all retries exhausted

### 6. Quality Maintenance

- Each agent is specialized with deep context for its task
- Validation gates unchanged (quality maintained)
- Traceability chains preserved
- Lifecycle logging ensures auditability

---

## Risks & Mitigations

### Risk 1: Spawn Coordination Overhead

**Risk**: Managing 18+ agent spawns adds coordination complexity

**Mitigation**:
- Reuse proven prototype-multiagent spawn verification logic
- Automated retry with countermeasures
- Clear troubleshooting guides per agent type

### Risk 2: Output Merging Complexity

**Risk**: Parallel agents generating same file (e.g., ANALYSIS_SUMMARY.md sections)

**Mitigation**:
- Agents write to temporary sections
- Main session merges after all complete
- Clear merge strategies in registry (separate_files, separate_folders, merge_sections)

### Risk 3: Agent Spawn Failure

**Risk**: Agent fails to spawn after 3 retries

**Mitigation**:
- Block execution (don't continue with missing data)
- Provide detailed troubleshooting (agent definition exists, registry entry valid)
- Fallback: User can run `/discovery` (sequential) as backup

### Risk 4: Dependency Violations

**Risk**: Agent B starts before Agent A completes (dependency violation)

**Mitigation**:
- Strict checkpoint sequencing
- Within checkpoint: only spawn parallel groups
- Progress manifest tracks dependencies explicitly

### Risk 5: Quality Regression

**Risk**: Parallel execution produces lower quality outputs

**Mitigation**:
- Pilot with 3 projects, compare outputs to sequential `/discovery`
- Maintain same validation gates
- Each agent has deep specialized context (not breadth)

---

## Next Steps

### Immediate (Week 1)

1. **Create discovery-multiagent command skeleton**
2. **Define agent registry JSON**
3. **Implement Group 1 parallel spawn** (material analysis: 3 agents)
4. **Test spawn verification** with retries

### Short-term (Week 2-3)

1. **Implement all 4 parallel groups**
2. **Add resume capability**
3. **Full pipeline test** on InventorySystem
4. **Measure metrics** (tokens, time, quality)

### Medium-term (Week 4)

1. **Production rollout** with 2-3 real projects
2. **Documentation update** (CLAUDE.md, commands reference)
3. **User training** on new command

### Long-term (Month 2)

1. **Deprecate `/discovery`** sequential command (keep as fallback)
2. **Apply learnings** to other stages (ProductSpecs, SolArch)
3. **Continuous optimization** based on usage patterns

---

## Success Criteria

### Quantitative

- ✅ Token usage reduced by >60%
- ✅ Execution time reduced by >40%
- ✅ Spawn success rate >95%
- ✅ Quality parity with sequential Discovery (validation gates pass)

### Qualitative

- ✅ User feedback positive (easier to resume, faster completion)
- ✅ No regressions in output quality
- ✅ Troubleshooting is clear when failures occur
- ✅ Traceability maintained end-to-end

---

## Appendix: Model Selection Rationale

### Sonnet Usage (Complex Reasoning)

**Use sonnet when:**
- Synthesis required (personas, vision, roadmap)
- Deep analysis needed (interviews, PDFs, JTBD)
- Narrative generation (personas, gap analysis)
- Prioritization logic (roadmap phasing)

**Cost**: Higher per token, but specialized context reduces volume

### Haiku Usage (Structured Extraction)

**Use haiku when:**
- Template-based output (strategy, KPIs, navigation)
- Pattern recognition (data analysis, design patterns)
- Checklist validation (pain points, cross-references)
- Structured field extraction (data fields, interactions)

**Cost**: Lower per token, sufficient for structured tasks

### Optimization Strategy

Start with conservative model choices (more sonnet), then:
1. Measure output quality per agent
2. Downgrade to haiku where quality maintained
3. Iterate based on validation results

---

**END OF DOCUMENT**
