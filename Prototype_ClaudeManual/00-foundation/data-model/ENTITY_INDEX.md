# Entity Index - ClaudeManual

---
**System**: ClaudeManual
**Generated**: 2026-01-31
**Session**: session-data-model-claudemanual
**Total Entities**: 9
---

## Quick Reference

| Entity ID | Entity Name | Purpose | Total Fields | Key Fields |
|-----------|-------------|---------|--------------|------------|
| ENT-001 | Skill | AI prompt templates | 22 | id, name, stage, path, skills_required |
| ENT-002 | Command | Slash commands | 17 | id, name, stage, path |
| ENT-003 | Agent | AI personas | 17 | id, name, model, stage, checkpoint |
| ENT-004 | Rule | Framework rules | 12 | id, name, auto_load_paths |
| ENT-005 | Hook | Lifecycle hooks | 8 | id, path, type, language |
| ENT-006 | UserPreferences | User settings | 7 | theme, favorites, stage_filter |
| ENT-007 | Workflow | Process diagrams | 12 | id, name, format, category |
| ENT-008 | WaysOfWorking | Team practices | 11 | id, name, category, audience |
| ENT-009 | ArchitectureDoc | Architecture docs | 16 | id, name, category, c4_level, adr_status |

---

## Entity Catalog

### ENT-001: Skill

**Location**: `.claude/skills/{skill-id}/SKILL.md`
**Primary Key**: `id` (string)
**Description**: Reusable AI prompt templates for specific tasks

**Core Fields** (11):
- id, name, description, stage, path, model, context, agent, allowed_tools, skills_required, hooks

**Content Sections** (6):
- Purpose, Usage, Options, Example, Workflow, Related

**Derived Fields** (5):
- stage_prefix, category, file_size, last_modified, content_hash

**Relationships**:
- uses_skill → Skill (1:N)
- invoked_by → Command (N:M)
- used_by_agent → Agent (N:M)

**Validation Rules**: 5
- VR-SKL-001: ID must match folder name
- VR-SKL-002: File must exist at path
- VR-SKL-003: Stage must be valid enum
- VR-SKL-004: Must have Purpose and Usage sections
- VR-SKL-005: Referenced skills must exist

**Traceability**: CF-001, CF-008, JTBD-1.2, JTBD-1.3

---

### ENT-002: Command

**Location**: `.claude/commands/{command-id}.md`
**Primary Key**: `id` (string)
**Description**: Slash commands executable in Claude Code

**Core Fields** (8):
- id, name, description, stage, path, model, allowed_tools, argument_hint

**Content Sections** (6):
- Usage, Arguments, Options, Example, Execution, Related

**Derived Fields** (3):
- invocation_syntax, requires_system_name, has_options

**Relationships**:
- invokes_skill → Skill (N:M)
- orchestrates_agents → Agent (N:M)

**Validation Rules**: 3
- VR-CMD-001: ID must match filename
- VR-CMD-002: Stage must be valid enum
- VR-CMD-003: Must have Usage and Example sections

**Traceability**: CF-001, CF-007, JTBD-1.1, JTBD-1.4

---

### ENT-003: Agent

**Location**: `.claude/agents/{agent-id}.md`
**Primary Key**: `id` (string)
**Description**: Specialized AI personas with specific skills

**Core Fields** (9):
- id, name, description, model, checkpoint, path, tools, color, stage

**Content Sections** (5):
- Your Expertise, Analysis Approach, Skills to Load, Output Format, Related

**Derived Fields** (3):
- stage_prefix, role, subagent_type

**Relationships**:
- loads_skill → Skill (N:M)
- spawned_by → Command (N:M)

**Validation Rules**: 3
- VR-AGT-001: ID must follow {stage}-{role} naming
- VR-AGT-002: Model must be valid enum
- VR-AGT-003: Must have Expertise and Output Format sections

**Traceability**: CF-001, CF-008, JTBD-1.2

---

### ENT-004: Rule

**Location**: `.claude/rules/{rule-id}.md`
**Primary Key**: `id` (string)
**Description**: Framework rules and conventions

**Core Fields** (7):
- id, name, description, path, auto_load_paths, version, category

**Content Sections** (4):
- Overview, Rules, Examples, Related

**Derived Fields** (1):
- applies_to_stages

**Relationships**: None

**Validation Rules**: 2
- VR-RUL-001: File must exist
- VR-RUL-002: Auto-load paths must be valid glob patterns

**Traceability**: CF-001, JTBD-1.2

---

### ENT-005: Hook

**Location**: `.claude/hooks/{hook-id}.(py|sh)`
**Primary Key**: `id` (string)
**Description**: Lifecycle hooks for commands, skills, agents

**Core Fields** (6):
- id, name, description, path, type, language

**Content Sections**: None (script file)

**Derived Fields** (2):
- executable, has_shebang

**Relationships**: None

**Validation Rules**: 2
- VR-HKS-001: File must exist and be executable
- VR-HKS-002: Language must match file extension

**Traceability**: CF-001, JTBD-1.5

---

### ENT-006: UserPreferences

**Location**: Browser localStorage
**Primary Key**: None (singleton per user)
**Description**: Per-user settings and preferences

**Core Fields** (7):
- theme, favorites, collapsed_nodes, last_viewed, search_history, stage_filter, type_filter

**Storage**: Browser localStorage (persistent)

**Relationships**:
- favorites → Skill, Command, Agent (N:M)

**Validation Rules**: 3
- VR-USR-001: Theme must be valid enum
- VR-USR-002: Referenced items must exist
- VR-USR-003: Search history max 20 items

**Traceability**: CF-003, CF-012, CF-016, JTBD-1.6

---

### ENT-007: Workflow

**Location**: `.claude/` or project folders
**Primary Key**: `id` (string)
**Description**: Process and workflow diagrams

**Core Fields** (8):
- id, name, description, format, path, stage, category, tags

**Content Sections** (4):
- Overview, Diagram, Steps, Related

**Relationships**:
- referenced_in → Skill (N:M)

**Validation Rules**: 3
- VR-WFL-001: File must exist
- VR-WFL-002: File extension must match format
- VR-WFL-003: Must have Diagram section for mermaid/plantuml

**Traceability**: CF-001, JTBD-1.9, JTBD-1.2

---

### ENT-008: WaysOfWorking

**Location**: Documentation folders
**Primary Key**: `id` (string)
**Description**: Team practices and guidelines

**Core Fields** (7):
- id, name, description, path, category, audience, tags

**Content Sections** (4):
- Overview, Guidelines, Examples, Checklist

**Relationships**: None

**Validation Rules**: 2
- VR-WOW-001: File must exist
- VR-WOW-002: Must have Overview section

**Traceability**: CF-001, JTBD-1.9, JTBD-1.1

---

### ENT-009: ArchitectureDoc

**Location**: `architecture/` folder
**Primary Key**: `id` (string)
**Description**: Architecture diagrams and documentation (C4, ADRs, patterns)

**Core Fields** (10):
- id, name, description, format, path, category, c4_level, adr_status, tags, related_adrs

**Content Sections** (6):
- Overview, Diagram, Context, Decision, Consequences, Related

**Relationships**:
- related_adrs → ArchitectureDoc (N:M)

**Validation Rules**: 4
- VR-ARC-001: File must exist
- VR-ARC-002: File extension must match format
- VR-ARC-003: C4 diagrams should specify c4_level
- VR-ARC-004: ADRs should specify adr_status

**Traceability**: CF-001, JTBD-1.9, JTBD-1.2, JTBD-2.1

---

## Field Summary

| Entity | Core Fields | Content Sections | Derived Fields | Total |
|--------|-------------|------------------|----------------|-------|
| Skill | 11 | 6 | 5 | 22 |
| Command | 8 | 6 | 3 | 17 |
| Agent | 9 | 5 | 3 | 17 |
| Rule | 7 | 4 | 1 | 12 |
| Hook | 6 | 0 | 2 | 8 |
| UserPreferences | 7 | 0 | 0 | 7 |
| Workflow | 8 | 4 | 0 | 12 |
| WaysOfWorking | 7 | 4 | 0 | 11 |
| ArchitectureDoc | 10 | 6 | 0 | 16 |
| **TOTAL** | **73** | **35** | **14** | **122** |

---

## Relationship Summary

| Relationship | From Entity | To Entity | Type | Description |
|--------------|-------------|-----------|------|-------------|
| uses_skill | Skill | Skill | 1:N | Skill dependencies |
| invokes_skill | Command | Skill | N:M | Command invokes skills |
| orchestrates_agents | Command | Agent | N:M | Command spawns agents |
| loads_skill | Agent | Skill | N:M | Agent loads skills |
| favorites | UserPreferences | Skill/Command/Agent | N:M | User favorited items |
| referenced_in | Workflow | Skill | N:M | Workflow referenced in skill docs |
| related_adrs | ArchitectureDoc | ArchitectureDoc | N:M | Related ADRs |

**Total Relationships**: 8

---

## Validation Summary

| Entity | Rules | Critical Rules |
|--------|-------|----------------|
| Skill | 5 | VR-SKL-001, VR-SKL-002, VR-SKL-004 |
| Command | 3 | VR-CMD-001, VR-CMD-003 |
| Agent | 3 | VR-AGT-001, VR-AGT-003 |
| Rule | 2 | VR-RUL-001 |
| Hook | 2 | VR-HKS-001 |
| UserPreferences | 3 | VR-USR-002 |
| Workflow | 3 | VR-WFL-001, VR-WFL-002 |
| WaysOfWorking | 2 | VR-WOW-001 |
| ArchitectureDoc | 4 | VR-ARC-001, VR-ARC-002 |
| **TOTAL** | **27** | **15** |

---

## Enum Reference

### Stage Enum
`Discovery`, `Prototype`, `ProductSpecs`, `SolArch`, `Implementation`, `Utility`, `GRC`, `Security`

### Model Enum
`sonnet`, `opus`, `haiku`

### Context Enum
`fork` (isolated sub-agent), `null`

### Theme Enum
`light`, `dark`, `system`

### Format Enum
`md`, `mermaid`, `plantuml`

### Category Enum (Workflow)
`process`, `integration`, `decision`, `data-flow`

### Category Enum (WaysOfWorking)
`practices`, `guidelines`, `processes`, `checklists`

### Category Enum (ArchitectureDoc)
`c4`, `adr`, `patterns`, `infrastructure`, `data-model`

### C4 Level Enum
`context`, `container`, `component`, `code`

### ADR Status Enum
`proposed`, `accepted`, `deprecated`, `superseded`

### Hook Type Enum
`PreToolUse`, `PostToolUse`, `Stop`, `lifecycle`

### Language Enum
`python`, `bash`

### Audience Enum
`developers`, `product`, `all`, `leads`

---

**Index Generated**: 2026-01-31
**Session**: session-data-model-claudemanual
**Agent**: prototype-data-model-specifier
