---
name: solarch-decisions
description: Generate Architecture Decision Records with traceability
argument-hint: None
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-decisions started '{"stage": "solarch"}'
  Stop:
    - hooks:
        # VALIDATION: Check ADR files were created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_solarch_output.py"
            --system-name "$(cat _state/session.json 2>/dev/null | grep -o '"project"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"project"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//')"
            --phase decisions
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-decisions ended '{"stage": "solarch", "validated": true}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-decisions instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

This command ensures all Architecture Decision Records (ADRs) are complete and generates the decision index. This is Checkpoint 8 of the pipeline, requiring minimum 9 ADRs.

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` (auto-detected from config if not provided)

## Usage

```bash
/solarch-decisions InventorySystem
```

## Prerequisites

- Checkpoint 7 passed (`/solarch-deploy` completed)
- Foundation ADRs created in previous phases

## Skills Used

Read BEFORE execution:
- `.claude/skills/SolutionArchitecture_AdrGenerator/SKILL.md`

## Required ADRs

### Foundation ADRs (Always Required)

| ADR | Title | Phase Created |
|-----|-------|---------------|
| ADR-001 | Architecture Style Selection | Strategy |
| ADR-002 | Technology Stack Selection | Strategy |
| ADR-003 | Module Structure | Blocks |
| ADR-004 | Data Storage Strategy | Blocks |
| ADR-005 | API Design Principles | Runtime |
| ADR-006 | Event-Driven Communication | Runtime |
| ADR-007 | Security Architecture | Runtime |
| ADR-008 | Caching Strategy | Quality |
| ADR-009 | Observability Strategy | Quality |
| ADR-010 | Deployment Strategy | Deploy |

### Conditional ADRs (Based on System)

| ADR | Title | Condition |
|-----|-------|-----------|
| ADR-011 | Real-time Updates | If WebSocket/SignalR used |
| ADR-012 | External Integration | If external systems integrated |
| ADR-013 | Audit Trail | If compliance requirements |
| ADR-014 | Multi-tenancy | If multi-tenant system |
| ADR-015 | Offline Support | If offline capability needed |

## Execution Steps

### Step 1: Execute

```
LOAD _state/solarch_config.json
SYSTEM_NAME = config.system_name

READ existing ADRs:
  GLOB 09-decisions/ADR-*.md
  COUNT existing ADRs

CHECK missing foundation ADRs:
  FOR adr_num IN [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    IF ADR-{adr_num}-*.md NOT exists:
      GENERATE missing ADR

GENERATE missing ADRs:
  FOR each missing ADR:
    USE AdrGenerator template
    INCLUDE:
      - Status: Accepted
      - Context: From discovery and requirements
      - Decision: Based on constraints and NFRs
      - Consequences: Positive and negative
      - Traceability: PP-*, REQ-*, MOD-*

EVALUATE conditional ADRs:
  IF real_time_features:
    GENERATE ADR-011-real-time-updates.md

  IF external_integrations:
    GENERATE ADR-012-external-integration.md

  IF audit_requirements:
    GENERATE ADR-013-audit-trail.md

GENERATE 09-decisions/INDEX.md:
  Decision Log:
    | ADR | Title | Status | Date |
    | ADR-001 | Architecture Style | Accepted | date |
    ...

  Decision Categories:
    - Foundation Decisions
    - Data Decisions
    - Integration Decisions
    - Security Decisions
    - Operations Decisions

  Traceability Summary:
    | ADR | Pain Points | Requirements |
    | ADR-001 | PP-1.1, PP-2.1 | REQ-001 |

VALIDATE all ADRs:
  FOR each ADR file:
    VERIFY required sections:
      - Status
      - Context
      - Decision
      - Consequences
      - Traceability

UPDATE traceability/adr_registry.json (ROOT level, v3.0):
  ENSURE all ADRs registered
  UPDATE statistics:
    total: N
    by_status: { accepted: N, proposed: N }
  # NOTE: Local _registry/decisions.json is DEPRECATED

UPDATE _state/solarch_progress.json:
  phases.decisions.status = "completed"
  phases.decisions.completed_at = NOW()
  current_checkpoint = 8

RUN quality gate:
  python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 8 --dir {OUTPUT_PATH}/

DISPLAY checkpoint 8 summary
```

### Step 2: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-decisions" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Output Files

### 09-decisions/

| File | Content |
|------|---------|
| `INDEX.md` | Decision index and categories |
| `ADR-001-architecture-style.md` | Architecture style decision |
| `ADR-002-technology-stack.md` | Technology stack decision |
| `ADR-003-module-structure.md` | Module structure decision |
| `ADR-004-data-storage.md` | Data storage decision |
| `ADR-005-api-design.md` | API design decision |
| `ADR-006-event-communication.md` | Event communication decision |
| `ADR-007-security-architecture.md` | Security architecture decision |
| `ADR-008-caching-strategy.md` | Caching strategy decision |
| `ADR-009-observability.md` | Observability decision |
| `ADR-010-deployment-strategy.md` | Deployment strategy decision |

## Decision Index Template

```markdown
---
document_id: SA-09-INDEX
version: 1.0.0
arc42_section: 9
---

# Architecture Decisions

## Decision Log

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-001](./ADR-001-architecture-style.md) | Architecture Style Selection | Accepted | 2025-12-22 |
| [ADR-002](./ADR-002-technology-stack.md) | Technology Stack Selection | Accepted | 2025-12-22 |
| [ADR-003](./ADR-003-module-structure.md) | Module Structure | Accepted | 2025-12-22 |
| [ADR-004](./ADR-004-data-storage.md) | Data Storage Strategy | Accepted | 2025-12-22 |
| [ADR-005](./ADR-005-api-design.md) | API Design Principles | Accepted | 2025-12-22 |
| [ADR-006](./ADR-006-event-communication.md) | Event-Driven Communication | Accepted | 2025-12-22 |
| [ADR-007](./ADR-007-security-architecture.md) | Security Architecture | Accepted | 2025-12-22 |
| [ADR-008](./ADR-008-caching-strategy.md) | Caching Strategy | Accepted | 2025-12-22 |
| [ADR-009](./ADR-009-observability.md) | Observability Strategy | Accepted | 2025-12-22 |
| [ADR-010](./ADR-010-deployment-strategy.md) | Deployment Strategy | Accepted | 2025-12-22 |

## Decision Categories

### Foundation Decisions

Define the fundamental architecture approach:
- **ADR-001**: Architecture Style Selection
- **ADR-002**: Technology Stack Selection
- **ADR-003**: Module Structure

### Data Decisions

Define data management approach:
- **ADR-004**: Data Storage Strategy

### Integration Decisions

Define communication patterns:
- **ADR-005**: API Design Principles
- **ADR-006**: Event-Driven Communication

### Security Decisions

Define security approach:
- **ADR-007**: Security Architecture

### Operations Decisions

Define operational approach:
- **ADR-008**: Caching Strategy
- **ADR-009**: Observability Strategy
- **ADR-010**: Deployment Strategy

## Traceability Summary

| ADR | Pain Points Addressed | Requirements Covered |
|-----|----------------------|---------------------|
| ADR-001 | PP-1.1, PP-2.1 | REQ-001, REQ-002 |
| ADR-002 | PP-2.2, PP-3.1 | REQ-003 |
| ADR-003 | PP-1.2, PP-4.1 | REQ-004, REQ-005 |
| ADR-004 | PP-3.2 | REQ-006 |
| ADR-005 | PP-4.2, PP-5.1 | REQ-007, REQ-008 |
| ADR-006 | PP-1.1, PP-5.2 | REQ-009 |
| ADR-007 | PP-6.1 | REQ-010 |
| ADR-008 | PP-2.1, PP-7.1 | REQ-011 |
| ADR-009 | PP-8.1 | REQ-012 |
| ADR-010 | PP-9.1 | REQ-013 |

## ADR Template Reference

All ADRs follow the standard template:
- **Status**: Proposed → Accepted → Deprecated → Superseded
- **Context**: Business and technical background
- **Decision**: The choice made and rationale
- **Consequences**: Positive, negative, and neutral impacts
- **Traceability**: Links to pain points, requirements, and modules
```

## Output Format

```
═══════════════════════════════════════════════════════════════
 CHECKPOINT 8: DECISIONS COMPLETE - COMPLETED
═══════════════════════════════════════════════════════════════

Generated/Verified Files:
├─ 09-decisions/
│   ├─ INDEX.md ✅
│   ├─ ADR-001-architecture-style.md ✅
│   ├─ ADR-002-technology-stack.md ✅
│   ├─ ADR-003-module-structure.md ✅
│   ├─ ADR-004-data-storage.md ✅
│   ├─ ADR-005-api-design.md ✅
│   ├─ ADR-006-event-communication.md ✅
│   ├─ ADR-007-security-architecture.md ✅
│   ├─ ADR-008-caching-strategy.md ✅
│   ├─ ADR-009-observability.md ✅
│   └─ ADR-010-deployment-strategy.md ✅

ADR Summary:
├─ Total ADRs: 10
├─ Accepted: 10
├─ Proposed: 0
└─ All required sections: ✅

Traceability:
├─ Pain Points Covered: 10/10 (100%)
└─ Requirements Addressed: 26

Quality Gate: ✅ PASSED

Next: /solarch-risks InventorySystem
═══════════════════════════════════════════════════════════════
```

## Checkpoint Validation

```bash
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 8 --dir SolArch_InventorySystem/
```

**Required for Checkpoint 8:**
- `_registry/decisions.json` exists with minimum 9 ADRs
- Each ADR document exists
- Each ADR has required sections (Status, Context, Decision, Consequences, Traceability)

## Error Handling

| Error | Action |
|-------|--------|
| Missing ADR | Generate from available context |
| Incomplete ADR | Complete missing sections |
| Traceability gaps | Add links where possible, note gaps |

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch-deploy` | Previous phase (Checkpoint 7) |
| `/solarch-risks` | Next phase (Checkpoint 9) |
