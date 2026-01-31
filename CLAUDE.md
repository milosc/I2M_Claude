# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **enterprise pilot project** for making Claude Code slash commands and hooks work as an end-to-end process. It contains AI-assisted product discovery and prototyping meta-prompts that form a structured framework for transforming raw client materials (interviews, screenshots, documents) into comprehensive product documentation and working prototypes.

**There is no traditional codebase here** - this is a collection of prompts, skills, and reference materials for running discovery and prototype workflows via Claude Code.

## Key Workflows

### 1. Discovery Analysis (promptsActual/Discovery_MetaPrompt_V5.md)
Transforms raw client materials into structured documentation:
- Input: Client interviews, screenshots, documents, spreadsheets
- Output: 20+ deliverables across 6 folders (personas, JTBD, vision, strategy, roadmap, KPIs, design specs)
- Uses 29 Discovery_* skills from `.claude/skills/`

### 2. Prototype Builder (prompts/Prototype_MetaPrompt_V1.md)
Transforms discovery outputs into working prototypes:
- Input: Completed Discovery analysis folder
- Output: Design tokens, component library, screen specs, working React prototype
- Uses 14+ Prototype_* skills from `.claude/skills/`

### 3. ProductSpecs Generator (prompts/ProductSpecs_Meta_Prompt_v1.md)
Generates production specifications from prototypes with full traceability.

## Directory Structure

```
prompts/               # Meta-prompts that orchestrate skills
helperFils/           # Helper instructions (error handling rules)
InventorySystem/      # Example client materials for inventory management project
.claude/skills/       # 115+ skills for Discovery and Prototype workflows
architecture/         # Detailed architecture documentation
```

## Initial Setup (REQUIRED)

Before running any workflows, install dependencies:

```bash
/htec-libraries-init
# Or directly:
python3 .claude/skills/tools/htec_dependencies_installer.py
```

This creates a `.venv` virtual environment with PDF processing, Office documents, Playwright, and LSP support.

## Quality Guardrails (MANDATORY)

### Traceability Guard
The framework enforces a **Global Traceability Version History**. Every change is logged to `traceability/{system_name}_version_history.json`.

- **Rule**: `.claude/rules/traceability.md` (ID formats, source linking, version logging)
- **Hook**: `.claude/hooks/version_history_logger.py`
- **Details**: `architecture/Version_and_Traceability_Management.md`

### Zero Hallucination Audit
The `/discovery-audit` command ensures every persona trait, JTBD, and requirement is backed by a specific citation or Client Fact ID.

### Validation Tool

```bash
python3 .claude/hooks/discovery_quality_gates.py --list-checkpoints
python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint N --dir ClientAnalysis_X/
```

**Full checkpoint requirements**: `architecture/Quality_Gates_Reference.md`

### Maintainability-First Principle

The framework enforces a **Maintainability-First Architectural Principle** across all agents and commands that shape or implement code solutions.

**Core Principle**: **Optimize for maintainability, not simplicity.**

- Prioritize long-term maintainability over short-term convenience
- Avoid "simplicity traps" (adding libraries without considering debugging burden)
- Think 6 months ahead: will this decision make debugging easier or harder?
- Use libraries strategically with justification, not by default

**Details**: `.claude/architecture/Maintainability_First_Principle.md`

**Application**:
- ADR writers evaluate maintenance burden as primary decision driver
- Tech researchers score dependencies on maintainability metrics
- Implementation developers justify every library addition
- Code quality agents detect maintainability anti-patterns
- Tech Lead presents dependency strategy questions to users

---

## Execution Logging (MANDATORY)

### Rule: Log Every Command and Skill Execution

Before executing ANY command or skill, you MUST run the logging hooks. This is BLOCKING - do not proceed without logging.

### Command Execution Pattern

```bash
# 1. BEFORE command starts - capture event_id
EVENT_ID=$(python3 .claude/hooks/command_start.py \
  --command-name "/<command>" \
  --stage "<stage>" \
  --system-name "<SystemName>" \
  --intent "<description>")

# 2. Execute command logic...

# 3. AFTER command completes
python3 .claude/hooks/command_end.py \
  --command-name "/<command>" \
  --stage "<stage>" \
  --status "completed" \
  --start-event-id "$EVENT_ID" \
  --outputs '{"files_created": N}'
```

### Skill Execution Pattern

```bash
# 1. BEFORE skill starts
SKILL_EVENT=$(python3 .claude/hooks/skill_invoke.py \
  --skill-name "<SkillName>" \
  --action start \
  --stage "<stage>" \
  --system-name "<SystemName>" \
  --intent "<description>")

# 2. Execute skill logic...

# 3. AFTER skill completes
python3 .claude/hooks/skill_invoke.py \
  --skill-name "<SkillName>" \
  --action end \
  --start-event-id "$SKILL_EVENT" \
  --status "completed" \
  --outputs '{"output_files": ["file1.md", "file2.md"]}'
```

### Stage Values

| Stage | Value |
|-------|-------|
| Discovery | `discovery` |
| Prototype | `prototype` |
| ProductSpecs | `productspecs` |
| Solution Architecture | `solarch` |
| Implementation | `implementation` |
| Utility | `utility` |

### Logging Hooks Reference

| Hook | Purpose | Required Arguments |
|------|---------|-------------------|
| `command_start.py` | Log command start | `--command-name`, `--stage`, `--system-name`, `--intent` |
| `command_end.py` | Log command end | `--command-name`, `--stage`, `--status`, `--start-event-id`, `--outputs` |
| `skill_invoke.py` | Log skill start/end | `--skill-name`, `--action`, `--stage`, `--system-name`, `--intent` |

### NEVER Skip Logging

- Logging is BLOCKING - do not proceed without it
- If hook fails, log to `_state/FAILURES_LOG.md` and continue
- Check `_state/pipeline_progress.json` to verify logging
- All events are stored in `_state/pipeline_progress.json`

---

## Error Handling (Critical)

When processing client materials:
1. **Skip and Continue**: Log `⛔ SKIPPED: [filename]` and continue
2. **Never retry** failed operations
3. **Never pip install** on errors
4. **Never ask** what to do - just skip and continue

### PDF Handling (10-Page Threshold)

```bash
# Check page count FIRST
.venv/bin/python .claude/skills/tools/pdf_splitter.py count <file.pdf>

# If >10 pages, convert to Markdown
.venv/bin/python .claude/skills/tools/pdf_splitter.py automd <file.pdf> [OUTPUT_DIR]/
```

---

## Slash Commands Quick Reference

### Discovery (Stage 1)
Full reference: `.claude/commands/DISCOVERY_COMMAND_REFERENCE.md`

| Command | Description |
|---------|-------------|
| `/discovery <SystemName> <InputPath>` | Complete end-to-end discovery (sequential) |
| `/discovery-multiagent <SystemName> <InputPath>` | **Multi-agent discovery (massively parallel, 60-70% faster)** |
| `/discovery-resume` | Resume from last checkpoint |
| `/discovery-audit` | Zero Hallucination Audit |
| `/discovery-feedback` | Process feedback with impact analysis |

### Prototype (Stage 2)
Full reference: `.claude/commands/PROTOTYPE_COMMAND_REFERENCE.md`

| Command | Description |
|---------|-------------|
| `/prototype <SystemName>` | Complete end-to-end prototype |
| `/prototype-resume` | Resume from last checkpoint |
| `/prototype-feedback` | Process change requests with debugging |
| `/presentation-slidev` | Generate web-based Slidev presentation (interactive) |

### ProductSpecs (Stage 3)
Full reference: `.claude/commands/PRODUCTSPECS_COMMAND_REFERENCE.md`

| Command | Description |
|---------|-------------|
| `/productspecs <SystemName> [OPTIONS]` | Complete end-to-end ProductSpecs with v2.0 hierarchical orchestration |
| `/productspecs-jira` | JIRA export only |
| `/productspecs-feedback` | Process change requests |

#### ProductSpecs v2.0 Architecture

**Version**: 2.0.0 (Hierarchical Orchestration + Self-Validation + VP Review)

**Key Features**:
- **Hierarchical Orchestration**: Master orchestrator + 3 sub-orchestrators (module, test, validation)
- **Self-Validation**: Per-agent validation using Haiku (15 checks, <15s per artifact)
- **VP Review Integration**: Auto-trigger for P0 modules and score < 70, batch review for P1/P2
- **7 Entry Points**: System/module/feature/screen/persona/subsystem/layer-level generation
- **Quality Critical Flag**: Force VP review for all modules

**Command Options**:
```bash
# System-level (default) - all modules
/productspecs InventorySystem

# Module-level - single module (80% time savings)
/productspecs InventorySystem --module MOD-INV-SEARCH-01

# Feature-level - all search modules (60-70% savings)
/productspecs InventorySystem --feature SEARCH

# Screen-level - all modules for screen
/productspecs InventorySystem --screen SCR-003

# Quality critical - VP review for ALL modules
/productspecs InventorySystem --quality critical
```

**Performance (v2.0)**:
| Mode | Time (20 modules) | Cost | VP Reviews | Quality Score |
|------|-------------------|------|------------|---------------|
| Standard | 18 min (+12%) | $60 (+13%) | 0 | 85 (+13%) |
| Auto-Reflexion | 24 min (+50%) | $85 (+60%) | 5 P0 + batch | 92 (+23%) |
| --quality critical | 35 min (+119%) | $120 (+126%) | 20 per-module | 96 (+28%) |

**Benefits**:
- +13% quality improvement (standard mode)
- +23% with auto-reflexion (P0 modules)
- +28% with --quality critical (all modules)
- 80% time savings for module-level updates
- -33% context usage reduction
- 30% reduction in merge gate failures

**Documentation**:
- **Architecture**: `.claude/architecture/Workflows/Solution Specification Phase/ProductSpecs_MultiAgent_Architecture.md`
- **Performance**: `.claude/architecture/Workflows/Solution Specification Phase/ProductSpecs_Performance_Benchmarks.md`
- **Entry Points**: `.claude/architecture/Workflows/Solution Specification Phase/Entry_Points_Usage_Guide.md`
- **Agent Registry**: `.claude/skills/PRODUCTSPECS_AGENT_REGISTRY.json`

### Solution Architecture (Stage 4)
Full reference: `.claude/commands/SOLARCH_COMMAND_REFERENCE.md`

| Command | Description |
|---------|-------------|
| `/solarch <SystemName>` | Complete end-to-end SolArch |
| `/solarch-feedback` | Process architecture feedback |

### Implementation (Stage 5)
Full reference: `.claude/commands/HTEC_SDD_COMMAND_REFERENCE.md`

**Implementation Philosophy**: Always task-based or PR-based execution (narrow scope).

| Command | Description |
|---------|-------------|
| `/htec-sdd-tasks <SystemName>` | Interactive task decomposition with PR grouping |
| `/htec-sdd-worktree-setup <SystemName>` | Create git worktrees for parallel PR development |
| `/htec-sdd-implement <SystemName> [--task T-001]` | Execute TDD implementation (worktree-aware, granular) |
| `/htec-sdd-review` | Multi-agent code review (run after batch) |
| `/htec-sdd-changerequest` | Kaizen-based change management |

**Detailed Execution Flow**: See `.claude/architecture/workflows/Implementation Phase/Task_Execution_Flow_Detailed.md`

#### Task Isolation Mode (v2.0)

**Purpose**: Prevents context memory rot when processing multiple tasks by spawning a separate orchestrator agent per task.

**Default behavior** (enabled by default):
```bash
# Each task gets its own isolated agent context
/htec-sdd-implement ERTriage --pr-group PR-003

# With batch concurrency limit (default: 2)
/htec-sdd-implement ERTriage --pr-group PR-003 --batch=3
```

**Options**:
| Option | Description | Default |
|--------|-------------|---------|
| `--isolate-tasks` | Spawn agent per task | `true` |
| `--batch <N>` | Max concurrent task agents | `2` |

**Results storage**: Each task's build/test results saved to:
```
Implementation_<System>/01-tasks/<T-ID>/results/
├── execution.json          # Main execution record
├── implementation_plan.md  # Phase 2 output
├── test_spec.md            # Phase 3 test design
├── build.log               # Build output
├── test.log                # Test output
├── quality_report.json     # Quality findings
└── pr_description.md       # PR prep
```

**Legacy mode** (shared context, not recommended for multi-task):
```bash
/htec-sdd-implement ERTriage --pr-group PR-003 --isolate-tasks=false
```

**Agent registry**: `.claude/skills/IMPLEMENTATION_AGENT_REGISTRY.json`
**Plan document**: `.claude/architecture/plans/PLAN_task_level_agent_isolation.md`

### Utility Commands

| Command | Description |
|---------|-------------|
| `/htec-libraries-init` | Install all dependencies |
| `/integrity-check` | Cross-stage validation |
| `/trace-audit <SystemName>` | **Multi-agent traceability audit** - comprehensive health report |
| `/traceability-status` | Quick traceability status check |
| `/version-bump major\|minor` | Version management |

#### Traceability Audit (`/trace-audit`)

**Version**: 1.0.0 (Multi-Agent Parallel Analysis)

The `/trace-audit` command provides comprehensive traceability validation with strict no-hallucination policies. It spawns specialized agents in parallel:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    /trace-audit ORCHESTRATOR                        │
├─────────────────────────────────────────────────────────────────────┤
│  PHASE 1: PARALLEL SCANNERS                                         │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐           │
│  │ registry-     │  │ state-        │  │ json-         │           │
│  │ scanner       │  │ analyzer      │  │ discovery     │           │
│  │               │  │               │  │               │           │
│  │ traceability/ │  │ _state/       │  │ all other     │           │
│  │               │  │               │  │ .json files   │           │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘           │
│          └──────────────────┼──────────────────┘                   │
│                             ▼                                       │
│  PHASE 2: CONSOLIDATOR                                              │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Cross-validation → Deduplication → Risk Assessment          │   │
│  │                                                             │   │
│  │ Outputs: TRACEABILITY_AUDIT_REPORT.md                       │   │
│  │          TRACEABILITY_MATRIX_MASTER.md                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

**Command Options**:
```bash
# Full audit with visual matrix
/trace-audit ERTriage

# Quick health check (no matrix)
/trace-audit ERTriage --quick

# Single section only
/trace-audit ERTriage --section registry
/trace-audit ERTriage --section state
/trace-audit ERTriage --section json

# JSON output for CI/CD
/trace-audit ERTriage --json
```

**Key Features**:
- **No Hallucination**: All agents only report verified findings with evidence
- **Parallel Execution**: 3 scanner agents run simultaneously (~60% faster)
- **Cross-Validation**: Consolidator detects conflicting findings between agents
- **Visual Matrix**: Generates `TRACEABILITY_MATRIX_MASTER.md` with E2E chain diagrams
- **Risk Assessment**: Prioritized recommendations with severity levels

**Agent Registry**: `.claude/skills/TRACEABILITY_AGENT_REGISTRY.json`

### Worktree Workflow (Parallel PR Development)

The framework supports git worktrees for true parallel development across multiple PRs:

**Setup Process**:
1. Run `/htec-sdd-tasks <SystemName>` - Generates PR groups with interactive strategy selection
2. Run `/htec-sdd-worktree-setup <SystemName>` - Creates worktrees for each PR group
3. Navigate to worktree: `cd ../worktrees/pr-001-auth`
4. Run `/htec-sdd-implement <SystemName>` - Auto-detects PR group, executes tasks

**Example**:
```bash
# Generate tasks with PR grouping
/htec-sdd-tasks InventorySystem
# User selects: "Per-story" grouping, "Per-PR worktrees"

# Setup worktrees
/htec-sdd-worktree-setup InventorySystem
# Creates: ../worktrees/pr-001-auth, pr-002-inventory, etc.

# Work in parallel (different terminals/sessions)
cd ../worktrees/pr-001-auth
/htec-sdd-implement InventorySystem  # Works on PR-001 tasks

cd ../worktrees/pr-002-inventory
/htec-sdd-implement InventorySystem  # Works on PR-002 tasks (parallel)
```

**Benefits**:
- **True Parallelism**: Multiple developers/agents can modify "same" files independently
- **Clean PRs**: Each PR has its own branch and isolated changes
- **Fast Reviews**: PR-scoped quality checks review only changed files
- **Registry Safety**: Shared files (_state/, traceability/) remain sequentially coordinated

**Full Documentation**: `.claude/architecture/workflows/Implementation Phase/Worktree_State_Schemas.md`

---

## Output Structure

**Full output trees**: `architecture/Stage_Output_Structures.md`

### Shared Folders (PROJECT ROOT)

```
project_root/
├── _state/                           <- SHARED state management
├── traceability/                     <- SHARED traceability registers
├── ClientAnalysis_<SystemName>/      <- Discovery outputs
├── Prototype_<SystemName>/           <- Prototype outputs
├── ProductSpecs_<SystemName>/        <- ProductSpecs outputs
├── SolArch_<SystemName>/             <- SolArch outputs
└── Implementation_<SystemName>/      <- Implementation outputs
```

**Path Resolution**: Paths starting with `_state/` or `traceability/` -> ROOT level. All other paths -> relative to phase folder.

---

## Traceability System

**Full documentation**: `architecture/Traceability_System.md`

### ID Formats

| ID Prefix | Artifact Type |
|-----------|---------------|
| `PP-X.X` | Pain Point |
| `JTBD-X.X` | Job To Be Done |
| `REQ-XXX` | Requirement |
| `SCR-XXX` | Screen |
| `MOD-XXX-XXX-NN` | Module Spec |
| `ADR-XXX` | Architecture Decision |
| `T-NNN` | Implementation Task |

### End-to-End Chain

```
CM-XXX -> PP-X.X -> JTBD-X.X -> REQ-XXX -> SCR-XXX -> MOD-XXX -> ADR-XXX -> T-NNN -> Code -> Tests
```

---

## Skills Framework

**Full skills list**: `architecture/Skills_Reference.md`

Skills are in `.claude/skills/` with naming conventions:
- `Discovery_*` - Analysis and documentation (29 skills)
- `Prototype_*` - Design and code generation (14+ skills)
- `ProductSpecs_*` - Module specs and JIRA export (10 skills)
- `SolutionArchitecture_*` - Architecture docs and C4/ADR (6 skills)
- `Implementation_*` - TDD, code review, integration (5 skills)
- `SECURITY_*` - Vulnerability scanning and security testing (10 skills)
- `GRC_*` - Governance, Risk, Compliance for regulated industries (22 skills)

### New Skill Categories (Added 2026-01-30)

#### Security Enhancement Skills

The `quality-security-auditor` agent now includes integrated security skills:
- `SECURITY_vulnerability-scanner` - OWASP 2025 vulnerability scanning
- `SECURITY_api-security-best-practices` - API security patterns
- `SECURITY_broken-authentication` - Authentication bypass detection
- `SECURITY_sql-injection-testing` - SQL injection pattern detection
- `SECURITY_xss-html-injection` - XSS vulnerability scanning
- `SECURITY_idor-testing` - Insecure Direct Object Reference testing
- `SECURITY_file-uploads` - File upload security validation

#### GRC Compliance Skills (Regulated Industries)

New `/compliance-check` command provides compliance validation:

```bash
# Medical device compliance
/compliance-check MedicalDevice --standard iso13485,mdr,fda

# Healthcare application
/compliance-check HealthApp --standard gdpr,hipaa

# Security-focused application
/compliance-check SecureApp --standard iso27001
```

| Standard | GRC Skill Used | Domain |
|----------|---------------|--------|
| `iso13485` | GRC_quality-manager-qms-iso13485 | Medical Device QMS |
| `gdpr` | GRC_gdpr-dsgvo-expert | EU Data Protection |
| `hipaa` | GRC_data-privacy-compliance | Healthcare Data |
| `fda` | GRC_fda-consultant-specialist | FDA 21 CFR Part 11 |
| `mdr` | GRC_mdr-745-specialist | EU Medical Device Regulation |
| `iso27001` | GRC_information-security-manager-iso27001 | Information Security |
| `risk` | GRC_risk-management-specialist | ISO 14971 Risk Management |

#### GRC Standalone Assessment Commands

These commands provide comprehensive compliance assessments using specialized agents:

| Command | Description | Agent Used |
|---------|-------------|------------|
| `/grc-assess-ai <description>` | AI governance and responsible AI assessment (EU AI Act, NIST AI RMF) | N/A (loads skills) |
| `/grc-assess-gdpr <description>` | GDPR compliance assessment with DPIA and data subject rights | `privacy-officer` |
| `/grc-assess-hipaa <description>` | HIPAA compliance assessment for healthcare systems | `compliance-analyst` |
| `/grc-assess-pci <description>` | PCI-DSS scope and compliance assessment | `security-auditor` |
| `/grc-map-frameworks <frameworks>` | Cross-framework control mapping (ISO 27001, SOC 2, NIST, CIS) | `security-auditor` |
| `/grc-scan-licenses [path]` | Open source license compliance scan | N/A (reads project) |

**Example Usage:**

```bash
# AI governance assessment
/grc-assess-ai "AI-powered resume screening and candidate ranking"

# GDPR compliance assessment
/grc-assess-gdpr "CRM system processing EU customer data"

# HIPAA compliance assessment
/grc-assess-hipaa "patient portal with PHI access and messaging"

# PCI-DSS assessment
/grc-assess-pci "e-commerce checkout using Stripe Elements"

# Cross-framework mapping
/grc-map-frameworks "ISO 27001, SOC 2, NIST CSF, CIS Controls"

# License compliance scan
/grc-scan-licenses "./src/MyApp"
```

**GRC Assessment Skills Reference:**

| Skill | Purpose |
|-------|---------|
| `GRC_ai-governance` | EU AI Act classification, NIST AI RMF, responsible AI |
| `GRC_ethics-review` | Ethical impact assessment, stakeholder analysis |
| `GRC_gdpr-compliance` | GDPR requirements, DPIA, data subject rights |
| `GRC_hipaa-compliance` | HIPAA safeguards, PHI handling, BAA management |
| `GRC_pci-dss-compliance` | PCI DSS requirements, scope reduction, SAQ selection |
| `GRC_security-frameworks` | ISO 27001, SOC 2, NIST CSF, CIS Controls mapping |
| `GRC_data-classification` | Sensitivity levels, handling requirements, labeling |
| `GRC_license-compliance` | Open source license compatibility, obligations |
| `GRC_sbom-management` | SBOM generation, vulnerability tracking, supply chain |

#### Design Enhancement Skills

Enhanced UI specification agents include:
- `ui-design-system` - Design system patterns and components
- `mobile-design` - Mobile-first UI patterns
- `tailwind-patterns` - Tailwind CSS v4 best practices
- `ui-ux-pro-max` - Advanced UX design intelligence

### Skill Hot-Reload

Skills are **automatically hot-reloaded** - changes take effect instantly without restart.

### Skill Frontmatter

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier |
| `description` | Yes | When to use and what it does |
| `context` | No | `fork` for isolated sub-agent |
| `agent` | No | `general-purpose`, `Explore`, `Plan`, `Bash` |

See `.claude/commands/create-skill.md` for skill authoring guidance.

### Skill Registries

Skills and agents are indexed in JSON registry files:

| Registry | Purpose |
|----------|---------|
| `SKILL_REGISTRY.json` | Central index mapping skill IDs to folders, inputs/outputs, dependencies |
| `PROTOTYPE_AGENT_REGISTRY.json` | Multi-agent coordination for Prototype stage (11 agents) |
| `SOLARCH_AGENT_REGISTRY.json` | Multi-agent coordination for SolArch stage |
| `PRODUCTSPECS_AGENT_REGISTRY.json` | Multi-agent coordination for ProductSpecs stage |

**Maintenance**: When adding skills or modifying commands, update registries. See `.claude/architecture/Skills_and_Registry_System.md` for detailed maintenance workflows.

---

## Multi-Agent Architecture

**Full documentation**: `architecture/Agent_Spawning_Architecture.md`

The framework uses a multi-agent system with specialized agents for different tasks. Agents are spawned via Claude Code's native Task tool.

### Agent Naming Convention

Agents follow the `{stage}-{role}` naming pattern:

| Stage | Agent Examples |
|-------|----------------|
| Discovery | `discovery-domain-researcher`, `discovery-persona-synthesizer` |
| Prototype | `prototype-screen-specifier`, `prototype-code-generator` |
| Implementation | `implementation-developer`, `implementation-test-automation-engineer` |
| Planning | `planning-tech-lead`, `planning-code-explorer` |
| Quality | `quality-bug-hunter`, `quality-security-auditor` |
| GRC | `compliance-analyst`, `privacy-officer`, `security-auditor` |
| Process Integrity | `process-integrity-traceability-guardian`, `process-integrity-checkpoint-auditor` |
| Reflexion | `reflexion-actor`, `reflexion-evaluator`, `reflexion-self-refiner` |

### GRC Agents (Standalone)

The following agents can be spawned directly for compliance assessments:

| Agent | Purpose | Skills Loaded |
|-------|---------|---------------|
| `compliance-analyst` | Regulatory framework assessment (GDPR, HIPAA, PCI-DSS), gap analysis, remediation roadmaps | `gdpr-compliance`, `hipaa-compliance`, `pci-dss-compliance`, `data-classification`, `security-frameworks` |
| `privacy-officer` | Data privacy assessment, DPIAs, data subject rights, international transfers | `gdpr-compliance`, `data-classification`, `ethics-review` |
| `security-auditor` | Security framework alignment, control assessment, audit readiness (ISO 27001, SOC 2, NIST, CIS) | `security-frameworks`, `data-classification`, `ai-governance` |

**Agent Capabilities:**

- **compliance-analyst**: Identifies applicable regulations, assesses current state, performs gap analysis, prioritizes remediation
- **privacy-officer**: Maps personal data flows, determines lawful basis, assesses DPIA triggers, evaluates privacy-by-design
- **security-auditor**: Defines audit scope, assesses controls, identifies gaps, reviews evidence, creates remediation roadmap

### Agent Invocation Pattern

All agents use Claude Code's native `subagent_type` values:

```javascript
Task({
  subagent_type: "general-purpose",  // Native Claude Code type
  model: "sonnet",                   // or "haiku" for structured tasks
  description: "Brief description",
  prompt: `Agent: {agent-name}
    Read: .claude/agents/{agent-name}.md
    SESSION: {session_id} | TASK: {task_id}
    [compact instructions]
    RETURN: JSON { status, files_written, issues }`
})
```

**Native subagent_type values**: `general-purpose`, `Explore`, `Plan`, `Bash`

### Model Selection Strategy

| Model | Use Cases | Examples |
|-------|-----------|----------|
| `sonnet` | Complex reasoning, code generation, analysis | Developer, Tech Lead, Security Auditor |
| `haiku` | Structured outputs, checklists, templated tasks | Traceability Guardian, Checkpoint Auditor |

### Agent Coordination

- **File Locking**: Agents acquire locks before modifying files
- **Session Tracking**: Each agent registers a session for monitoring
- **Process Integrity**: Guardian agents monitor TDD compliance and traceability

**Commands**:
```bash
/agent-spawn <agent-type> <task-id>   # Spawn specific agent
/agent-status                          # View active agents
/agent-cleanup                         # Clean stale sessions
```

**Details**: `.claude/rules/agent-coordination.md`

---

## Presentation Generation

The framework supports two presentation formats for delivering project artifacts to stakeholders and team members:

### Format Options

| Format | Best For | Features | Output |
|--------|----------|----------|--------|
| **PowerPoint (PPTX)** | Executives, business stakeholders, formal presentations | Traditional slides, offline viewing, familiar format | `.pptx` files |
| **Slidev (Markdown)** | Developers, technical teams, conference talks | Web-based, live code, animations, interactive | Web app + `.md` source |

### PowerPoint (PPTX)

**Use when:**
- Presenting to non-technical stakeholders
- Formal board presentations or client deliverables
- Offline viewing required
- Traditional slide deck format expected

**Generated via:**
- Prototype_Deliverables skill (automatic)
- Part of `/prototype` workflow (Phase 6)

**Output location:** `06-deliverables/presentations/*.pptx`

### Slidev (Web-based Markdown)

**Use when:**
- Technical presentations for developers
- Conference talks or workshops
- Live code demonstrations needed
- Interactive features required (Monaco editor, animations)
- Speaker notes and recording needed

**Generated via:**
- `/presentation-slidev` command (interactive)
- Prototype_Deliverables skill (format option)

**Features:**
- Markdown-based slides
- Syntax-highlighted code with line-by-line animations
- Mermaid and PlantUML diagrams
- LaTeX math equations
- Interactive Monaco code editor
- Speaker view and notes
- Recording mode with camera
- Export to PDF, PPTX, PNG
- Host as web app (SPA)

**Interactive Configuration:**

The `/presentation-slidev` command asks for:
1. **Source files/folders** - Which framework outputs to include
2. **Audience** - Target audience (e.g., "technical architects", "executives")
3. **3 Key Messages** - Core takeaways to deliver
4. **Detail Level** - Executive (10-15 slides) → Workshop (50+ slides)
5. **Speaker Notes** - Yes/No/Critical slides only
6. **Diagram Format** - Mermaid, PlantUML, Both, or None
7. **Project Name** - Sanitized name for output folder

**Output structure:**
```
presentations/{ProjectName}/
├── slides.md              # Main presentation (edit this)
├── package.json           # Dependencies
├── README.md              # Documentation
└── dist/                  # Built web app (after npm run build)
```

**Commands:**
```bash
# Interactive generation
/presentation-slidev

# Start dev server (auto-reload on edit)
cd presentations/{ProjectName}
npm install
npm run dev                # Opens http://localhost:3030

# Export to PDF
npm run export

# Build for deployment
npm run build
```

**Keyboard Shortcuts:**
- `Space` / `Arrow Keys` - Navigate slides
- `S` - Speaker view (notes + timer)
- `C` - Drawing mode
- `G` - Camera/recording mode
- `O` - Overview mode

**Integration with Framework Stages:**

| Stage | Typical Presentation Content | Format Recommendation |
|-------|------------------------------|----------------------|
| **Discovery** | Personas, pain points, JTBD, vision | PPTX for stakeholders, Slidev for product team |
| **Prototype** | Design system, screens, components, validation | Slidev (interactive demos) |
| **ProductSpecs** | Module specs, test cases, requirements | PPTX for executives, Slidev for dev team |
| **SolArch** | C4 diagrams, ADRs, tech stack | Slidev (architecture deep-dive) |
| **Implementation** | TDD examples, code reviews, progress | Slidev (live code examples) |

**Example Use Cases:**

1. **Executive Discovery Brief**
   - Format: PPTX
   - Detail: Executive Summary (10-15 slides)
   - Content: Personas, top 5 pain points, P0 requirements

2. **Technical Architecture Deep-Dive**
   - Format: Slidev
   - Detail: Detailed (40+ slides)
   - Content: C4 diagrams (Mermaid), ADRs, code examples

3. **Prototype Demo Workshop**
   - Format: Slidev
   - Detail: Workshop (50+ slides)
   - Content: Interactive component demos, live code editing

**Related Files:**
- Slidev skill: `.claude/skills/slidev/SKILL.md`
- Presentation command: `.claude/commands/presentation-slidev.md`
- PPTX skill: `.claude/skills/pptx/SKILL.md`
- Deliverables skill: `.claude/skills/Prototype_Deliverables/SKILL.md`

---

## Quality Gates Summary

**Full checkpoint requirements**: `architecture/Quality_Gates_Reference.md`

### Blocking Gates

| Stage | Checkpoint | Requirement |
|-------|------------|-------------|
| Discovery | 10.5 | Zero hallucination audit pass |
| ProductSpecs | 7 | 100% P0 coverage |
| SolArch | 1 | ProductSpecs CP8+, Prototype CP14+ |
| SolArch | 11 | 100% pain point & requirement coverage |
| Implementation | 1 | ProductSpecs CP8+, SolArch CP12+ |
| Implementation | 6 | No CRITICAL findings, coverage > 80% |

---

## Change Request System

**Full documentation**: `architecture/ChangeRequest_Process.md`

The `/htec-sdd-changerequest` command provides Kaizen-based change management:

| Method | When to Use |
|--------|-------------|
| Quick Check | Simple, obvious cause |
| 5 Whys | Moderate complexity |
| Fishbone | Multiple contributing factors |
| A3 Full | Critical issues |

Integration: PDCA + TDD + Reflexion

---

## Integrity Check

```bash
/integrity-check              # Full report
/integrity-check --quick      # Summary only
/integrity-check --section traceability
/integrity-check --json       # CI/CD output
```

---

## Architecture Documentation

| Document | Content |
|----------|---------|
| `architecture/Stage_Output_Structures.md` | All output folder trees |
| `architecture/Quality_Gates_Reference.md` | Checkpoint requirements |
| `architecture/Traceability_System.md` | IDs, chains, registries |
| `architecture/Skills_Reference.md` | All skills by stage |
| `architecture/Agent_Spawning_Architecture.md` | Multi-agent system design |
| `architecture/ChangeRequest_Process.md` | Kaizen/PDCA workflow |
| `architecture/Version_and_Traceability_Management.md` | Versioning |

---

## Implementation Learnings

This section captures learnings from change requests. Each entry includes evidence reference.

### Error Patterns to Avoid

_Populated by the Reflexion MEMORIZE phase during change request processing._

### Debugging Strategies

_Populated by the Reflexion MEMORIZE phase during change request processing._

### Code Quality Rules

_Populated by the Reflexion MEMORIZE phase during change request processing._
