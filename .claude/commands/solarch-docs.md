---
name: solarch-docs
description: Generate Solution Architecture documentation package
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-docs started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-docs ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-docs instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

This command generates the glossary and ensures all documentation is complete. This is Checkpoint 10 of the pipeline.

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` (auto-detected from config if not provided)

## Usage

```bash
/solarch-docs InventorySystem
```

## Prerequisites

- Checkpoint 9 passed (`/solarch-risks` completed)

## Skills Used

Read BEFORE execution:
- `.claude/skills/SolutionArchitecture_Arc42Generator/SKILL.md`

## Execution Steps

### Step 1: Execute

```
LOAD _state/solarch_config.json
SYSTEM_NAME = config.system_name

EXTRACT domain terms from all sources:
  - ProductSpecs_X/01-modules/MOD-*.md
  - ClientAnalysis_X/01-analysis/ANALYSIS_SUMMARY.md
  - All generated architecture docs

GENERATE 11-glossary/glossary.md:
  USE Arc42Generator Section 12 template:

    Domain Terms:
      | Term | Definition | Context |
      | Adjustment | Stock movement between bins | Inventory |
      | Bin | Physical storage location | Warehouse |

    Acronyms:
      | Acronym | Expansion | Usage |
      | ADR | Architecture Decision Record | Documentation |
      | API | Application Programming Interface | Integration |

    Technical Terms:
      | Term | Definition |
      | Facade | Interface for cross-module queries |
      | Domain Event | Internal module state change |

UPDATE _state/solarch_progress.json:
  phases.docs.status = "completed"
  phases.docs.completed_at = NOW()
  current_checkpoint = 10

RUN quality gate:
  python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 10 --dir {OUTPUT_PATH}/

DISPLAY checkpoint 10 summary
```

### Step 2: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-docs" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Output Files

### 11-glossary/

| File | Content |
|------|---------|
| `glossary.md` | Domain terms, acronyms, technical terms |

## Template Structure

```markdown
---
document_id: SA-11-GLOSSARY
version: 1.0.0
arc42_section: 12
---

# Glossary

## Domain Terms

| Term | Definition | Context | Source |
|------|------------|---------|--------|
| Adjustment | A stock movement between storage bins, tracked for audit purposes | Inventory Management | MOD-INV-ADJUST |
| Bin | A physical storage location within the warehouse identified by zone-aisle-rack-level code | Warehouse Layout | Discovery |
| Exception | A discrepancy between expected and actual stock levels | Quality Control | MOD-INV-EXCEPT |
| Propagation | Real-time notification of stock changes to downstream systems | Integration | ADR-006 |
| Reason Code | Predefined classification for stock adjustments | Audit | Requirements |
| Stock Level | Current quantity of an item at a specific location | Inventory | Core Domain |

## Acronyms

| Acronym | Expansion | Usage |
|---------|-----------|-------|
| ADR | Architecture Decision Record | Documentation of key architectural decisions |
| API | Application Programming Interface | External and internal integration |
| CRUD | Create, Read, Update, Delete | Basic data operations |
| DTO | Data Transfer Object | API request/response structures |
| E2E | End-to-End | Testing strategy |
| JWT | JSON Web Token | Authentication mechanism |
| JTBD | Jobs To Be Done | Requirements methodology |
| NFR | Non-Functional Requirement | Quality attributes |
| PP | Pain Point | Discovery methodology |
| RBAC | Role-Based Access Control | Authorization model |
| REST | Representational State Transfer | API architecture |
| SSE | Server-Sent Events | Real-time updates |
| WMS | Warehouse Management System | External system |

## Technical Terms

| Term | Definition |
|------|------------|
| Building Block | A logical component of the system architecture |
| Container | A deployable unit in C4 model terminology |
| Context | The environment in which the system operates |
| Domain Event | An event that represents a significant occurrence within a bounded context |
| Facade | A simplified interface that abstracts complex subsystem interactions |
| Integration Event | An event used for communication between bounded contexts |
| Quality Scenario | A measurable specification of a quality requirement |
| Runtime View | Documentation of system behavior during execution |
| Traceability | The ability to trace requirements through architecture to implementation |

## Patterns

| Pattern | Definition | Usage |
|---------|------------|-------|
| Circuit Breaker | Prevents cascading failures by failing fast when services are unavailable | External integrations |
| Event Sourcing | Stores state changes as events rather than current state | Audit trail |
| CQRS | Command Query Responsibility Segregation | Read/write optimization |
| Repository | Abstracts data access behind a collection-like interface | Data layer |
| Saga | Manages distributed transactions through compensating actions | Cross-module workflows |

## Module-Specific Terms

### Stock Adjustment Module

| Term | Definition |
|------|------------|
| From Bin | Source location of a stock movement |
| To Bin | Destination location of a stock movement |
| Quantity | Number of units being moved |
| Approval Required | Flag indicating supervisor verification needed |

### Exception Dashboard Module

| Term | Definition |
|------|------------|
| Age | Time since exception was detected |
| Resolution | Action taken to address exception |
| Trend | Pattern of exceptions over time |

## Reference

- [arc42 Documentation](https://arc42.org)
- [C4 Model](https://c4model.com)
- [ADR Templates](https://adr.github.io)
```

## Output Format

```
═══════════════════════════════════════════════════════════════
 CHECKPOINT 10: DOCUMENTATION - COMPLETED
═══════════════════════════════════════════════════════════════

Generated Files:
└─ 11-glossary/
    └─ glossary.md ✅

Glossary Contents:
├─ Domain Terms: 6 defined
├─ Acronyms: 13 defined
├─ Technical Terms: 9 defined
└─ Module Terms: 6 defined

Quality Gate: ✅ PASSED

Next: /solarch-trace InventorySystem
═══════════════════════════════════════════════════════════════
```

## Checkpoint Validation

```bash
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 10 --dir SolArch_InventorySystem/
```

**Required for Checkpoint 10:**
- `11-glossary/glossary.md` exists with content

## Error Handling

| Error | Action |
|-------|--------|
| Source files missing | Generate basic glossary |
| Terms extraction fails | Use available terms |

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch-risks` | Previous phase (Checkpoint 9) |
| `/solarch-trace` | Next phase (Checkpoint 11) |
