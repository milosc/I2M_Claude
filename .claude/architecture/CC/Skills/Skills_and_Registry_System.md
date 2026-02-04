# Skills and Registry System

**Purpose**: Detailed reference for maintaining skills and registry files in `.claude/skills/`

**When to load**: When adding new skills, modifying commands, or maintaining the framework

---

## Overview

Skills are **executable prompts** that perform specific tasks when invoked via Claude Code's Skill tool. They are NOT just documentation - they are the building blocks that orchestrate the HTEC framework.

---

## Skill Structure

### Directory Layout

```
.claude/skills/
├── SKILL_REGISTRY.json           # Central skill index
├── PROTOTYPE_AGENT_REGISTRY.json # Multi-agent coordination (Prototype stage)
├── SOLARCH_AGENT_REGISTRY.json   # Multi-agent coordination (SolArch stage)
├── PRODUCTSPECS_AGENT_REGISTRY.json
├── Discovery_Orchestrator/
│   └── SKILL.md                  # Executable instructions
├── Prototype_Builder/
│   └── SKILL.md
├── theme-factory/
│   └── SKILL.md
└── [115+ other skills]
```

### Skill File (SKILL.md)

Each skill folder contains a `SKILL.md` with:

1. **YAML Frontmatter** (metadata for Claude Code)
2. **Markdown Body** (detailed instructions)

**Example**:
```yaml
---
name: discovery-orchestrator
description: Use when you need to coordinate complete discovery analysis
model: sonnet
allowed-tools: Read, Write, Edit, Bash, Task
context: fork
agent: general-purpose
---

# Discovery Orchestrator

[Detailed instructions follow...]
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (used in `/skill-name`) |
| `description` | Yes | When to use this skill (shown in skill list) |
| `model` | No | `sonnet`, `haiku`, `opus` (defaults to sonnet) |
| `allowed-tools` | No | Tools this skill can use |
| `context` | No | `fork` = isolated sub-agent, default = main session |
| `agent` | No | Claude Code subagent type: `general-purpose`, `Explore`, `Plan`, `Bash` |

---

## Registry Files

### SKILL_REGISTRY.json (Central Index)

**Purpose**: Maps skill IDs to locations, defines input/output contracts, tracks dependencies

**Structure**:
```json
{
  "$schema": "skill-registry-v1",
  "version": "1.0.0",
  "base_path": ".claude/skills",
  "skills": {
    "prototype-design-tokens": {
      "folder": "Prototype_DesignTokens",
      "file": "SKILL.md",
      "category": "generation",
      "phase": "design",
      "description": "Generate design tokens with optional theme selection",
      "inputs": {
        "required": ["00-foundation/DESIGN_BRIEF.md"],
        "optional": ["theme_name", "visual_assets"]
      },
      "outputs": [
        "00-foundation/DESIGN_TOKENS.md",
        "00-foundation/colors.md"
      ],
      "can_invoke": ["theme-factory", "canvas-design"],
      "invoked_by": ["prototype-builder"]
    }
  }
}
```

**Who uses it**:
- Orchestrator skills (to dynamically locate and invoke other skills)
- Claude Code (to validate skill dependencies)
- Framework maintainers (to understand skill relationships)

### AGENT_REGISTRY.json Files (Stage-Specific)

**Purpose**: Define multi-agent systems for parallel execution in each framework stage

**Example**: `PROTOTYPE_AGENT_REGISTRY.json` defines:
- 11 specialized agents (orchestrator, specifiers, validators)
- Model allocation (sonnet vs haiku for each agent)
- Parallel execution groups (which agents run in parallel)
- Checkpoint dependencies (which checkpoints block others)

**Structure**:
```json
{
  "metadata": {
    "stage": "Prototype",
    "stage_number": 2,
    "total_agents": 11
  },
  "agents": [
    {
      "id": "prototype-component-specifier",
      "name": "Component Specifier",
      "category": "specification",
      "model": "sonnet",
      "file": "prototype-component-specifier.md",
      "checkpoint": 8,
      "skill_refs": ["Prototype_Components", "Prototype_Decomposition"],
      "outputs": ["01-components/"]
    }
  ],
  "parallel_groups": {
    "validation": {
      "checkpoint": 13,
      "agents": ["prototype-component-validator", "prototype-screen-validator"],
      "strategy": "all_parallel"
    }
  }
}
```

**Who uses it**:
- Multi-agent commands (`/discovery-multiagent`, `/prototype-multiagent`)
- Coordination logic for parallel agent spawning
- Framework maintainers (to understand agent execution flow)

---

## Skill Invocation

### Method 1: Direct Invocation (Claude Code)

```bash
# User invokes via slash command
/discovery InventorySystem Client_Materials

# Claude Code loads .claude/skills/Discovery_Orchestrator/SKILL.md
# Executes instructions in that file
```

### Method 2: Skill-to-Skill Invocation

Skills can invoke other skills using the `INVOKE_SKILL` pattern:

```markdown
INVOKE_SKILL:
  skill: "theme-factory"
  inputs:
    theme_name: "ocean_depths"
  outputs:
    - theme_colors
    - theme_fonts
  on_success: STORE selected_theme
  on_failure: WARN "Theme not found, using defaults"
```

### Method 3: Agent-Based Invocation

Multi-agent commands spawn agents from registry files:

```bash
/prototype-multiagent InventorySystem
# Reads PROTOTYPE_AGENT_REGISTRY.json
# Spawns 11 agents in parallel/sequential order
# Each agent executes its referenced skills
```

---

## Maintenance Workflows

### Adding a New Skill

1. **Create skill folder**: `.claude/skills/MyNewSkill/SKILL.md`
2. **Add frontmatter**:
   ```yaml
   ---
   name: my-new-skill
   description: Brief description of when to use
   model: sonnet
   ---
   ```
3. **Write instructions**: Detailed markdown body
4. **Register in SKILL_REGISTRY.json**:
   ```json
   "my-new-skill": {
     "folder": "MyNewSkill",
     "file": "SKILL.md",
     "category": "generation",
     "phase": "discovery",
     "inputs": {"required": [], "optional": []},
     "outputs": []
   }
   ```
5. **Create command** (if user-invocable): `.claude/commands/my-new-skill.md`
6. **Test invocation**: `/my-new-skill`

### Adding a New Agent (Multi-Agent)

**Recommended**: Use the `/create-agent` command to create agents with proper HTEC conventions:

```bash
/create-agent React performance optimization specialist
```

This spawns the `agent-expert` in a separate context to create the agent with:
- Proper hooks configuration (PreToolUse, PostToolUse, Stop)
- FIRST ACTION (MANDATORY) lifecycle logging
- COMPLETION LOGGING (MANDATORY) section
- HTEC naming conventions

**Manual process** (if needed):

1. **Create agent definition**: `.claude/agents/discovery-my-agent.md`
   - Follow template in `.claude/agents/agent-expert.md`
   - Include hooks for lifecycle logging
   - Add FIRST ACTION and COMPLETION LOGGING sections
2. **Register in AGENT_REGISTRY.json**:
   ```json
   {
     "id": "discovery-my-agent",
     "name": "My Agent",
     "model": "sonnet",
     "file": "discovery-my-agent.md",
     "checkpoint": 5,
     "skill_refs": ["Discovery_MySkill"]
   }
   ```
3. **Update parallel groups** (if applicable)
4. **Update checkpoint mapping**
5. **Test with orchestrator**: `/discovery-multiagent`

### Modifying a Command

1. **Update command file**: `.claude/commands/my-command.md`
2. **Update skill if needed**: `.claude/skills/MySkill/SKILL.md`
3. **Update CLAUDE.md** (if adding to command reference tables)
4. **Update COMMAND_REFERENCE.md** (stage-specific reference)
5. **Hot-reload**: Changes take effect immediately

### Deprecating a Skill

1. **Remove from SKILL_REGISTRY.json**
2. **Remove skill folder**: `.claude/skills/OldSkill/`
3. **Remove command**: `.claude/commands/old-skill.md`
4. **Update dependent skills**: Remove from `can_invoke` lists
5. **Update CLAUDE.md**: Remove from skill counts/tables

---

## Skill Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| `generation` | Create artifacts | `Discovery_GeneratePersona`, `Prototype_Components` |
| `validation` | Validate outputs | `Discovery_Validate`, `Prototype_QA` |
| `documentation` | Create docs | `Prototype_PromptLog`, `Prototype_Decomposition` |
| `management` | Orchestration | `Prototype_Builder`, `Prototype_ChangeManager` |
| `3rdparty` | External capabilities | `theme-factory`, `markitdown`, `webapp-testing` |

---

## Skill Phases

| Phase | Order | Examples |
|-------|-------|----------|
| `discovery` | 0 | All Discovery_* skills |
| `foundation` | 1 | Data model, API contracts |
| `design` | 2 | Design tokens, components |
| `implementation` | 3 | Code generation, sequencer |
| `validation` | 4 | QA, UI audit |
| `documentation` | 5 | Decomposition, prompt log |
| `delivery` | 6 | Deliverables export |
| `post-build` | 7 | Change management |
| `meta` | 0 | Orchestrators, utilities |

---

## Best Practices

### Skill Design

✅ **Single Responsibility**: One skill = one task
✅ **Clear Inputs/Outputs**: Document in registry and skill header
✅ **Error Handling**: Follow `.claude/rules/CORE_RULES.md` (skip and continue)
✅ **Idempotency**: Skills should be safe to run multiple times
✅ **Traceability**: Log to `_state/pipeline_progress.json`

### Registry Management

✅ **Keep registries in sync**: SKILL_REGISTRY.json must match folder structure
✅ **Update dependencies**: When skill A invokes skill B, add to `can_invoke`
✅ **Version agent registries**: Bump version when adding/removing agents
✅ **Test parallel groups**: Ensure agents in same group don't have file conflicts

### Command Creation

✅ **User-facing commands**: Add to `.claude/commands/`
✅ **Update CLAUDE.md**: Add to command reference tables
✅ **Stage-specific reference**: Update `DISCOVERY_COMMAND_REFERENCE.md`, etc.
✅ **Hook integration**: Add execution logging hooks

---

## File Naming Conventions

| Pattern | Example | Purpose |
|---------|---------|---------|
| `Discovery_*` | `Discovery_GeneratePersona` | Discovery stage skills |
| `Prototype_*` | `Prototype_Components` | Prototype stage skills |
| `ProductSpecs_*` | `ProductSpecs_JIRAExporter` | ProductSpecs stage skills |
| `SolutionArchitecture_*` | `SolutionArchitecture_C4Generator` | SolArch stage skills |
| `Implementation_*` | `Implementation_Developer` | Implementation stage skills |
| `lowercase-hyphen` | `theme-factory`, `web-artifacts-builder` | 3rd party skills |

---

## Hot-Reload Behavior

Skills are **automatically hot-reloaded**:
- Changes to `SKILL.md` take effect immediately
- No need to restart Claude Code
- Registry changes (JSON) also hot-reload

**Exception**: Agent definitions (`.claude/agents/*.md`) may require session restart for multi-agent commands.

---

## Related Documentation

### Authoring Commands
- `/create-agent <description>`: Create new agents with proper HTEC conventions
- `/create-skill`: Create new skills with TDD approach
- `/create-command`: Create new slash commands
- `/create-hook`: Create new validation hooks

### Reference Files
- **CLAUDE.md**: Project overview, command quick reference
- **SKILL_INVOCATION.md**: Detailed invocation syntax
- **Agent_Spawning_Architecture.md**: Multi-agent system design
- **Stage_Output_Structures.md**: What each stage produces
- **Skills_Reference.md**: Full skill inventory by stage
- **agent-expert.md**: Agent creation template and guidelines

---

## Troubleshooting

### Skill not found

**Error**: `Skill 'my-skill' not found`

**Fix**:
1. Check `.claude/skills/SKILL_REGISTRY.json` contains the skill
2. Verify folder name matches `"folder"` field in registry
3. Verify `SKILL.md` exists in that folder
4. Check `name` in frontmatter matches skill ID

### Agent not spawning

**Error**: Agent appears in registry but doesn't spawn

**Fix**:
1. Check `AGENT_REGISTRY.json` has correct `file` path
2. Verify agent definition file exists in `.claude/agents/`
3. Check `checkpoint` field matches expected execution order
4. Verify `depends_on` fields don't create circular dependencies

### Skill invocation fails

**Error**: Skill runs but produces no output

**Fix**:
1. Check skill has Write tool in `allowed-tools`
2. Verify output paths in registry match actual outputs
3. Check skill instructions include explicit Write tool calls
4. Review `_state/pipeline_progress.json` for errors

---

**Last Updated**: 2026-02-03
**Framework Version**: 3.0.0
