# Three-Layer Architecture: How It Works

**Document Type**: Architecture Reference
**Version**: 1.0.0
**Last Updated**: 2026-01-25
**Scope**: All HTEC Framework Stages (Discovery, Prototype, ProductSpecs, SolArch, Implementation)

---

## Overview

The HTEC Framework uses a **three-layer architecture** where knowledge is shared between different execution modes. This document explains the relationship between **Skills**, **Commands**, and **Agents**, and clarifies that knowledge is **shared, not moved or duplicated**.

---

## Three-Layer Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: SKILLS (Procedural Logic - Source of Truth)  │
│  .claude/skills/Discovery_GenerateKPIs/                 │
│  .claude/skills/Discovery_GenerateJTBD/                 │
│  .claude/skills/Discovery_GeneratePersona/              │
│  .claude/skills/Prototype_ScreenSpecifier/              │
│                                                         │
│  Contains: Templates, instructions, validation rules    │
└─────────────────────────────────────────────────────────┘
                        ↓ (shared by)
                        ↓
        ┌───────────────┴───────────────┐
        ↓                               ↓
┌──────────────────┐          ┌──────────────────┐
│  LAYER 2:        │          │  LAYER 3:        │
│  COMMANDS        │          │  AGENTS          │
│  (User-Facing)   │          │  (Orchestrated)  │
├──────────────────┤          ├──────────────────┤
│ /discovery-kpis  │          │ discovery-kpis-  │
│ /discovery-jtbd  │          │   generator.md   │
│ /discovery-      │          │ discovery-jtbd-  │
│   persona        │          │   extractor.md   │
│                  │          │ discovery-       │
│ Manual,          │          │   persona-       │
│ single-artifact  │          │   generator.md   │
│ execution        │          │                  │
│                  │          │ Automated,       │
│                  │          │ pipeline         │
│                  │          │ execution        │
└──────────────────┘          └──────────────────┘
```

---

## Layer 1: Skills (Source of Truth)

**Location**: `.claude/skills/{Stage}_{Function}/`

**Purpose**: Core procedural logic - the "how to" instructions

**Contains**:
- Templates (e.g., `kpis_template.md`)
- Validation rules (e.g., `kpi_rules.yaml`)
- Instructions (e.g., `SKILL.md`)
- Examples (e.g., `sample_kpis.md`)

**Example Structure**:
```
.claude/skills/Discovery_GenerateKPIs/
├── SKILL.md (main instructions)
├── templates/
│   └── kpis_template.md
├── validation/
│   └── kpi_rules.yaml
└── examples/
    └── sample_kpis.md
```

**Key Principle**: Skills contain the **single source of truth** for procedural logic. Both Commands and Agents reference and use these skills.

---

## Layer 2: Commands (User-Facing, Manual)

**Location**: `.claude/commands/{command-name}.md`

**Purpose**: Individual, targeted artifact generation

**Invocation**: User types command directly

**Execution Mode**: Synchronous, in main session

**Example**: `/discovery-kpis`

**File**: `.claude/commands/discovery-kpis.md`

### What Commands Do

1. Load the corresponding skill (e.g., `Discovery_GenerateKPIs`)
2. Read required inputs from Discovery outputs
3. Execute in MAIN SESSION (not spawned)
4. Write output artifact
5. Return control to user

### When to Use Commands

- ✅ "I need to regenerate just the KPIs document"
- ✅ "I want to manually create a single artifact"
- ✅ Debugging/testing
- ✅ Selective updates after feedback
- ✅ Ad-hoc, one-off generation

### Example Command Execution

```bash
# User types:
/discovery-kpis InventorySystem

# What happens:
# 1. Main session loads Discovery_GenerateKPIs skill
# 2. Reads PAIN_POINTS.md, PRODUCT_VISION.md
# 3. Executes in main session
# 4. Writes ClientAnalysis_InventorySystem/03-strategy/KPIS_AND_GOALS.md
# 5. Returns control to user
```

---

## Layer 3: Agents (Orchestrated, Automated)

**Location**: `.claude/agents/{stage}-{role}.md`

**Purpose**: Automated execution within multi-agent pipeline

**Invocation**: Spawned by orchestration command (e.g., `/discovery-multiagent`)

**Execution Mode**: Asynchronous, spawned sub-agent

**Example**: `discovery-kpis-generator.md`

**File**: `.claude/agents/discovery-kpis-generator.md`

### What Agents Do

1. Get spawned by orchestration command at specific checkpoint
2. Register session with coordinator
3. Read the corresponding skill (e.g., `Discovery_GenerateKPIs`)
4. Read required inputs
5. Execute independently as sub-agent
6. Write output artifact
7. Report completion to spawn manifest
8. Terminate

### When Agents Are Used

- ✅ Part of full `/discovery-multiagent` pipeline
- ✅ Automated checkpoint-based execution
- ✅ Parallel execution with other agents
- ✅ Production workflows

### Example Agent Execution

```bash
# User types:
/discovery-multiagent InventorySystem Client_Materials/

# What happens at Checkpoint 8:
# 1. Main session spawns Task(discovery-kpis-generator)
# 2. Agent registers session
# 3. Agent reads Discovery_GenerateKPIs skill
# 4. Agent reads inputs
# 5. Agent executes independently
# 6. Agent writes KPIS_AND_GOALS.md
# 7. Agent updates spawn manifest
# 8. Agent terminates
# 9. Main session continues to CP-9
```

---

## Comparison Table

| Aspect | Commands | Agents |
|--------|----------|--------|
| **Invocation** | User types `/discovery-kpis` | Spawned by `/discovery-multiagent` |
| **Execution** | Main session, synchronous | Sub-agent, asynchronous |
| **Scope** | Single artifact | Part of full pipeline |
| **Use Case** | Manual, targeted work | Automated, orchestrated |
| **Parallelization** | Not applicable | Can run in parallel with others |
| **Session** | Uses main session | Independent session |
| **State Tracking** | Discovery progress only | Spawn manifest + sessions |
| **Skill Loading** | Loads skill directly | Reads skill from agent definition |
| **Resume Support** | Via stage-specific resume command | Via `--resume` flag |
| **Speed** | Baseline | 60-70% faster (parallel execution) |
| **Context Usage** | Full main session context | Fresh context per agent |

---

## Knowledge Flow

### Skills Are the Source of Truth

**Skills contain all procedural logic**:
- Templates
- Validation rules
- Step-by-step instructions
- Examples
- Quality criteria

### Commands Reference Skills

```markdown
# In .claude/commands/discovery-kpis.md

## Execution

Load and execute Discovery_GenerateKPIs skill:
- Template: .claude/skills/Discovery_GenerateKPIs/templates/kpis_template.md
- Validation: .claude/skills/Discovery_GenerateKPIs/validation/kpi_rules.yaml
- Instructions: Follow SKILL.md step-by-step
```

### Agents Reference Skills

```markdown
# In .claude/agents/discovery-kpis-generator.md

## Related

- **Skill**: `.claude/skills/Discovery_GenerateKPIs/`

## Execution

1. READ skill instructions from Discovery_GenerateKPIs/SKILL.md
2. LOAD template from Discovery_GenerateKPIs/templates/
3. VALIDATE output using Discovery_GenerateKPIs/validation/
4. EXECUTE following skill procedures
```

### Knowledge Is Shared, Not Duplicated

**❌ WRONG APPROACH** (Knowledge duplication):
```
Command: Contains KPI generation logic
Agent: Contains same KPI generation logic (duplicated)
Skill: Contains same KPI generation logic (duplicated)
```

**✅ CORRECT APPROACH** (Knowledge shared):
```
Skill: Contains KPI generation logic (source of truth)
Command: References skill and executes in main session
Agent: References skill and executes in sub-agent
```

**Benefits**:
- ✅ Single source of truth
- ✅ Easy maintenance (update once)
- ✅ Consistency across execution modes
- ✅ Reduced duplication
- ✅ Clear separation of concerns

---

## Usage Scenarios

### Scenario 1: Full Discovery Run (Automated Pipeline)

**User Action**:
```bash
/discovery-multiagent InventorySystem Client_Materials/
```

**What Happens**:
- Main session spawns 15+ agents
- Each agent (including `discovery-kpis-generator`) spawns at its checkpoint
- Agents execute in parallel where possible
- All agents reference their respective skills
- ✅ **Agent definitions used**
- ❌ **Individual commands NOT used**

**Execution Mode**: Multi-agent orchestrated
**Speed**: 60-70% faster than sequential
**Use Case**: Production, full automation

---

### Scenario 2: Regenerate Single Artifact (Manual)

**User Action**:
```bash
/discovery-kpis InventorySystem
```

**What Happens**:
- Main session loads `Discovery_GenerateKPIs` skill directly
- Executes in main session (no spawning)
- Writes KPIS_AND_GOALS.md
- Returns control to user
- ✅ **Command used**
- ❌ **Agent definition NOT used**

**Execution Mode**: Single-session synchronous
**Speed**: Baseline
**Use Case**: Targeted regeneration, debugging, manual updates

---

### Scenario 3: Feedback-Driven Update

**User Action**:
```bash
/discovery-feedback InventorySystem
# User specifies: "Update KPI targets based on new metrics"
```

**What Happens**:
- Feedback workflow identifies affected artifact: KPIS_AND_GOALS.md
- Spawns Reflexion agents for impact analysis
- Final implementation may:
  - **Option A**: Call `/discovery-kpis` command to regenerate (if only KPIs affected)
  - **Option B**: Spawn `discovery-kpis-generator` agent (if part of larger update)
- Decision based on whether other artifacts need updates
- ✅ **Could use either command or agent**

**Execution Mode**: Depends on scope
**Use Case**: Change management, feedback incorporation

---

## Decision Matrix: Command vs Agent

### Use Commands When:

| Scenario | Example |
|----------|---------|
| Need just one artifact | "Regenerate KPIs only" |
| Manual, ad-hoc work | "Let me test this template" |
| Debugging | "I want to see the KPI generation in detail" |
| Selective update | "Only the roadmap changed, regenerate it" |
| Interactive work | "Generate, review, regenerate" |
| Learning/testing | "Let me understand how personas are created" |

### Use Agents (Multi-Agent Pipeline) When:

| Scenario | Example |
|----------|---------|
| Full stage execution | "Generate complete Discovery" |
| Time-sensitive work | "Need this by end of day" |
| Large input sets | "Analyze 10+ interviews" |
| Production workflow | "Standard Discovery process" |
| Parallel execution needed | "Process all materials simultaneously" |
| Resume capability needed | "Pick up where we left off" |

---

## Benefits of Three-Layer Architecture

### 1. Single Source of Truth

**Skills** contain all procedural logic in one place.

**Benefit**: Update skill once, both commands and agents get the update.

**Example**:
```
# Update KPI template
Edit: .claude/skills/Discovery_GenerateKPIs/templates/kpis_template.md

# Both /discovery-kpis command and discovery-kpis-generator agent
# will use the updated template automatically
```

### 2. Flexibility

Users can choose execution mode based on their needs.

**Options**:
- Manual, targeted work → Commands
- Automated, full pipeline → Agents

### 3. Maintainability

Clear separation of concerns:
- **Skills**: What to do and how
- **Commands**: User interface for manual execution
- **Agents**: Orchestration interface for automation

### 4. Consistency

Both execution modes use the same skills, ensuring consistent outputs.

### 5. Scalability

New stages can be added following the same pattern:
1. Create skills (procedural logic)
2. Create commands (manual interface)
3. Create agents (automation interface)

---

## Common Questions

### Q: "Why have both commands and agents if they do the same thing?"

**A**: They serve different workflows:
- **Commands** = Manual, interactive, targeted
- **Agents** = Automated, parallel, orchestrated

Analogy: You can drive to the store (manual) or take an autonomous bus (automated). Same destination, different use cases.

### Q: "Was knowledge moved from commands to agents?"

**A**: No, knowledge was **never in commands or agents**. It's always been in **skills**. Both commands and agents **reference** skills.

### Q: "Can I use just commands and ignore agents?"

**A**: Yes! If you prefer manual, sequential work:
```bash
/discovery-kpis InventorySystem
/discovery-jtbd InventorySystem
/discovery-personas InventorySystem
# etc.
```

But you lose:
- ❌ 60-70% speed improvement
- ❌ Parallel execution
- ❌ Resume capability
- ❌ Automated orchestration

### Q: "Can I mix commands and agents?"

**A**: Yes! Common pattern:
1. Run `/discovery-multiagent` for full automation
2. Review outputs
3. Use `/discovery-kpis` to regenerate specific artifact
4. Continue with `/prototype`

### Q: "What if I update a skill?"

**A**: Both commands and agents use the updated skill immediately (hot-reload).

### Q: "Do agents work without commands?"

**A**: Yes. Agents are spawned by orchestration commands (e.g., `/discovery-multiagent`), not by individual artifact commands.

---

## Architecture Pattern Across Stages

This three-layer pattern applies to **all HTEC stages**:

| Stage | Skills | Commands | Agents | Orchestration |
|-------|--------|----------|--------|---------------|
| Discovery | `Discovery_*` | `/discovery-*` | `discovery-*-generator.md` | `/discovery-multiagent` |
| Prototype | `Prototype_*` | `/prototype-*` | `prototype-*-specifier.md` | `/prototype-multiagent` |
| ProductSpecs | `ProductSpecs_*` | `/productspecs-*` | `productspecs-*-specifier.md` | `/productspecs` |
| SolArch | `SolutionArchitecture_*` | `/solarch-*` | `solarch-*-generator.md` | `/solarch` |
| Implementation | `Implementation_*` | `/htec-sdd-*` | `implementation-developer.md` | `/htec-sdd` |

---

## Visual Summary

```
┌─────────────────────────────────────────────────────────────┐
│ USER WORKFLOW CHOICE                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Manual, Targeted Work           Automated, Full Pipeline  │
│         ↓                                 ↓                 │
│    COMMANDS                           AGENTS               │
│         ↓                                 ↓                 │
│         └─────────────┬───────────────────┘                 │
│                       ↓                                     │
│                    SKILLS                                   │
│              (Source of Truth)                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Summary

### Key Points

1. **Skills** = Source of truth for procedural logic
2. **Commands** = User-facing, manual, synchronous execution
3. **Agents** = Orchestrated, automated, asynchronous execution
4. **Knowledge is SHARED** = Both reference the same skills
5. **Both are valuable** = Serve different workflows

### When to Use What

| Goal | Use |
|------|-----|
| Manual artifact generation | Commands (`/discovery-kpis`) |
| Full automated pipeline | Agents (via `/discovery-multiagent`) |
| Targeted regeneration | Commands |
| Maximum speed | Agents (60-70% faster) |
| Debugging/learning | Commands |
| Production workflow | Agents |

### Architecture Benefits

- ✅ Single source of truth (skills)
- ✅ Flexibility (choose execution mode)
- ✅ Maintainability (clear separation)
- ✅ Consistency (shared logic)
- ✅ Scalability (reusable pattern)

---

**The three-layer architecture provides the best of both worlds: manual control when needed, automation when desired, all while maintaining a single source of truth.**

---

## Related Documents

- **Agent Spawning Architecture**: `.claude/architecture/Agent_Spawning_Architecture.md`
- **Discovery Multi-Agent Architecture**: `.claude/architecture/workflows/discovery-multiagent-architecture.md`
- **Skills Reference**: `.claude/architecture/Skills_Reference.md`
- **Command Reference (Discovery)**: `.claude/commands/DISCOVERY_COMMAND_REFERENCE.md`
- **AGENTS.md**: Root-level agent taxonomy and overview

---

**Version**: 1.0.0
**Last Updated**: 2026-01-25
**Author**: Claude Code (Architecture Documentation)
