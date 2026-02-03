---
name: solarch-strategy
description: Generate architecture strategy document
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-strategy started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-strategy ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-strategy instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

This command generates the solution strategy documentation and creates the foundation Architecture Decision Records (ADR-001, ADR-002). This is Checkpoint 3 of the pipeline.

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` (auto-detected from config if not provided)

## Usage

```bash
/solarch-strategy InventorySystem
```

## Prerequisites

- Checkpoint 2 passed (`/solarch-context` completed)
- Pain points and requirements available

## Skills Used

Read BEFORE execution:
- `.claude/skills/SolutionArchitecture_Arc42Generator/SKILL.md`
- `.claude/skills/SolutionArchitecture_AdrGenerator/SKILL.md`

## Execution Steps

### Step 1: Execute

```
LOAD _state/solarch_config.json
LOAD _state/solarch_input_validation.json
SYSTEM_NAME = config.system_name

READ ProductSpecs materials:
  - ProductSpecs_X/00-overview/MASTER_DEVELOPMENT_PLAN.md
  - ProductSpecs_X/_registry/modules.json
  - ProductSpecs_X/_registry/nfrs.json

READ Discovery materials:
  - ClientAnalysis_X/01-analysis/PAIN_POINTS.md

### Architecture Style Decision

ANALYZE pain points and requirements to determine candidate architecture styles

USE AskUserQuestion:
  question: "Which architecture style best fits this system?"
  header: "Architecture"
  options:
    - label: "Modular Monolith (Recommended)"
      description: "Single deployment, clear module boundaries. Best for: MVP, small team"
    - label: "Microservices"
      description: "Independent deployment per service. Best for: Scale, multiple teams"
    - label: "Event-Driven"
      description: "Async communication, loose coupling. Best for: Real-time, integrations"
    - label: "Layered (Traditional)"
      description: "Horizontal layers (UI/Business/Data). Best for: Simple CRUD apps"

STORE architecture_style_selection in:
  - State file: _state/solarch_config.json
  - Key: architecture_style
  - Value: { choice: "[selected]", timestamp: "[ISO]", source: "user" }

### Technology Stack Decision

IF architecture_style selected:
  USE AskUserQuestion:
    question: "Which technology stack should we use?"
    header: "Tech Stack"
    options:
      - label: "React + .NET + PostgreSQL (Recommended)"
        description: "Enterprise-grade, strong typing, mature ecosystem"
      - label: "React + Node.js + PostgreSQL"
        description: "JavaScript/TypeScript full-stack, faster iteration"
      - label: "Vue + Python/FastAPI + PostgreSQL"
        description: "Simpler frontend, Python backend for data-heavy apps"
      - label: "Next.js + Supabase"
        description: "Serverless, rapid prototyping, built-in auth"

STORE tech_stack_selection in:
  - State file: _state/solarch_config.json
  - Key: technology_stack
  - Value: { choice: "[selected]", timestamp: "[ISO]", source: "user" }

GENERATE 04-solution-strategy/solution-strategy.md:
  USE Arc42Generator Section 04 template:

    4.1 Technology Decisions:
      | Decision | Choice | Rationale | ADR |
      | Architecture Style | {choice} | {why} | ADR-001 |
      | Frontend | {choice} | {why} | ADR-002 |
      | Backend | {choice} | {why} | ADR-002 |
      | Database | {choice} | {why} | ADR-002 |

    4.2 Top-Level Decomposition:
      {Module structure from modules.json}

    4.3 Approaches to Quality Goals:
      {From NFRs}

    4.4 Organizational Decisions:
      {Deployment, Testing, Documentation approaches}

GENERATE ADR-001-architecture-style.md:
  USE AdrGenerator template:
    - Title: Architecture Style Selection
    - Status: Accepted
    - Context: Business requirements, team capabilities
    - Decision: {Modular Monolith / Microservices / etc.}
    - Consequences: Positive and negative
    - Traceability: PP-* that drove this decision

GENERATE ADR-002-technology-stack.md:
  USE AdrGenerator template:
    - Title: Technology Stack Selection
    - Status: Accepted
    - Context: Team skills, integration requirements
    - Decision: Frontend, Backend, Database choices
    - Consequences: Positive and negative
    - Traceability: PP-* that drove this decision

UPDATE _registry/decisions.json:
  ADD ADR-001:
    {
      "id": "ADR-001",
      "title": "Architecture Style Selection",
      "status": "accepted",
      "date": "ISO8601",
      "document": "./09-decisions/ADR-001-architecture-style.md",
      "painPoints": ["PP-*"],
      "modules": ["all"],
      "summary": "{brief summary}"
    }

  ADD ADR-002:
    {
      "id": "ADR-002",
      "title": "Technology Stack Selection",
      "status": "accepted",
      "date": "ISO8601",
      "document": "./09-decisions/ADR-002-technology-stack.md",
      "painPoints": ["PP-*"],
      "modules": ["all"],
      "summary": "{brief summary}"
    }

UPDATE _state/solarch_progress.json:
  phases.strategy.status = "completed"
  phases.strategy.completed_at = NOW()
  current_checkpoint = 3

RUN quality gate:
  python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 3 --dir {OUTPUT_PATH}/

DISPLAY checkpoint 3 summary
```

### Step 2: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-strategy" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Output Files

### 04-solution-strategy/

| File | Content |
|------|---------|
| `solution-strategy.md` | Technology decisions, decomposition, quality approaches |

### 09-decisions/

| File | Content |
|------|---------|
| `ADR-001-architecture-style.md` | Architecture style decision |
| `ADR-002-technology-stack.md` | Technology stack decision |

## ADR Template

```markdown
---
document_id: ADR-001
version: 1.0.0
created_at: 2025-12-22T10:00:00Z
status: accepted
---

# ADR-001: Architecture Style Selection

## Status

**Accepted** - 2025-12-22

## Context

{Business context and requirements that drove this decision}

### Pain Points Addressed

| Pain Point | Description | Impact |
|------------|-------------|--------|
| PP-1.1 | {description} | High |

### Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| REQ-001 | {requirement} | P0 |

## Decision

We will adopt a **{Architecture Style}** approach because:

1. {Reason 1}
2. {Reason 2}
3. {Reason 3}

### Architecture Diagram

```mermaid
{architecture diagram}
```

## Consequences

### Positive

- {Positive consequence 1}
- {Positive consequence 2}

### Negative

- {Negative consequence 1}
- {Risk mitigation approach}

### Neutral

- {Neutral observation}

## Traceability

| Pain Point | JTBD | Requirement | Module |
|------------|------|-------------|--------|
| PP-1.1 | JTBD-1.1 | REQ-001 | All |

## References

- [MASTER_DEVELOPMENT_PLAN.md](../../ProductSpecs_X/00-overview/MASTER_DEVELOPMENT_PLAN.md)
```

## Foundation ADRs

### ADR-001: Architecture Style

Common choices:
- **Modular Monolith**: Single deployment, clear module boundaries
- **Microservices**: Independent deployment, distributed
- **Layered Architecture**: Traditional separation of concerns
- **Event-Driven**: Async communication, loose coupling

### ADR-002: Technology Stack

Typical structure:
- Frontend: React/Vue/Angular + TypeScript
- Backend: .NET/Node.js/Java
- Database: PostgreSQL/SQL Server
- Cache: Redis
- Message Queue: RabbitMQ/Kafka

## Output Format

```
═══════════════════════════════════════════════════════════════
 CHECKPOINT 3: SOLUTION STRATEGY - COMPLETED
═══════════════════════════════════════════════════════════════

Generated Files:
├─ 04-solution-strategy/
│   └─ solution-strategy.md ✅
└─ 09-decisions/
    ├─ ADR-001-architecture-style.md ✅
    └─ ADR-002-technology-stack.md ✅

Architecture Decision:
├─ Style: Modular Monolith
└─ Stack: React + .NET + PostgreSQL

ADRs Registered: 2

Traceability:
├─ Pain Points Addressed: 10
└─ Requirements Covered: 26

Quality Gate: ✅ PASSED

Next: /solarch-blocks InventorySystem
═══════════════════════════════════════════════════════════════
```

## Checkpoint Validation

```bash
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 3 --dir SolArch_InventorySystem/
```

**Required for Checkpoint 3:**
- `04-solution-strategy/solution-strategy.md` exists with content
- `09-decisions/ADR-001-architecture-style.md` exists with required sections
- `09-decisions/ADR-002-technology-stack.md` exists with required sections

## Error Handling

| Error | Action |
|-------|--------|
| NFRs missing | Generate with available data, note gaps |
| Pain points incomplete | Log to FAILURES_LOG, continue |
| Modules.json missing | ERROR, checkpoint 1 should have caught this |

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch-context` | Previous phase (Checkpoint 2) |
| `/solarch-blocks` | Next phase (Checkpoint 4) |
