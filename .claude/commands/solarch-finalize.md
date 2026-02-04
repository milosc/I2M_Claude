---
name: solarch-finalize
description: Finalize Solution Architecture with validation and documentation
argument-hint: None
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-finalize started '{"stage": "solarch"}'
  Stop:
    - hooks:
        # VALIDATION: Check finalization was completed
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_solarch_output.py"
            --system-name "$(cat _state/session.json 2>/dev/null | grep -o '"project"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"project"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//')"
            --phase finalize
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-finalize ended '{"stage": "solarch", "validated": true}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-finalize instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

This command generates the final validation report and summary, completing the Solution Architecture generation pipeline. This is Checkpoint 12 of the pipeline.

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` (auto-detected from config if not provided)

## Usage

```bash
/solarch-finalize InventorySystem
```

## Prerequisites

- Checkpoint 11 passed (`/solarch-trace` completed)
- All traceability validations passed

## Skills Used

None required - this generates final documentation.

## Execution Steps

### Step 1: Execute

```
LOAD _state/solarch_config.json
LOAD _state/solarch_progress.json
SYSTEM_NAME = config.system_name

GENERATE reports/VALIDATION_REPORT.md (v3.0):
  Overview:
    - System name
    - Generation date
    - Checkpoints passed

  Validation Summary:
    | Checkpoint | Status | Timestamp |
    | 0 - Init | ✅ Passed | timestamp |
    | 1 - Validate | ✅ Passed | timestamp |
    ...
    | 12 - Final | ✅ Passed | timestamp |

  Artifacts Generated:
    - Count by category
    - File listing

  Traceability Summary:
    - Coverage percentages
    - Chain completeness

  Quality Gate Results:
    - All checkpoint validations

GENERATE reports/GENERATION_SUMMARY.md (v3.0):
  Executive Summary:
    - What was generated
    - Key statistics
    - Coverage achieved

  Architecture Overview:
    - Style chosen (from ADR-001)
    - Technology stack (from ADR-002)
    - Module count

  ADR Summary:
    - Total ADRs: N
    - Categories covered

  Outputs:
    - Folder structure
    - Key documents

  Next Steps:
    - Development handoff
    - Implementation priorities

UPDATE traceability/solarch_traceability_register.json:
  CREATE/UPDATE at ROOT level:
    {
      "$schema": "solarch-traceability-register-v1",
      "$metadata": {
        "created_at": "ISO8601",
        "updated_at": "ISO8601",
        "system_name": "{SYSTEM_NAME}",
        "generation_complete": true
      },
      "summary": {
        "adrs_count": N,
        "components_count": N,
        "pain_points_covered": N,
        "requirements_covered": N,
        "modules_architected": N
      },
      "chains": [...]
    }

UPDATE _state/solarch_progress.json:
  phases.final.status = "completed"
  phases.final.completed_at = NOW()
  current_checkpoint = 12
  generation_complete = true

RUN quality gate:
  python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 12 --dir {OUTPUT_PATH}/

DISPLAY completion summary
```

### Step 2: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-finalize" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Output Files

### _registry/

| File | Content |
|------|---------|
| `VALIDATION_REPORT.md` | Complete validation report |
| `GENERATION_SUMMARY.md` | Executive summary |

### traceability/ (ROOT)

| File | Content |
|------|---------|
| `solarch_traceability_register.json` | Final traceability register |

## Template: VALIDATION_REPORT.md

```markdown
---
document_id: SA-VALIDATION-REPORT
version: 1.0.0
generated_at: 2025-12-22T10:00:00Z
---

# Solution Architecture Validation Report

## Overview

| Attribute | Value |
|-----------|-------|
| System Name | InventorySystem |
| Generation Date | 2025-12-22 |
| Total Checkpoints | 13 |
| Passed | 13 |
| Failed | 0 |

## Checkpoint Summary

| CP | Phase | Status | Timestamp |
|----|-------|--------|-----------|
| 0 | Initialize | ✅ Passed | 2025-12-22T10:00:00Z |
| 1 | Validate Inputs | ✅ Passed | 2025-12-22T10:01:00Z |
| 2 | Context & Goals | ✅ Passed | 2025-12-22T10:05:00Z |
| 3 | Solution Strategy | ✅ Passed | 2025-12-22T10:10:00Z |
| 4 | Building Blocks | ✅ Passed | 2025-12-22T10:20:00Z |
| 5 | Runtime & Integration | ✅ Passed | 2025-12-22T10:30:00Z |
| 6 | Quality & Cross-cutting | ✅ Passed | 2025-12-22T10:40:00Z |
| 7 | Deployment | ✅ Passed | 2025-12-22T10:50:00Z |
| 8 | Decisions Complete | ✅ Passed | 2025-12-22T11:00:00Z |
| 9 | Risk Assessment | ✅ Passed | 2025-12-22T11:05:00Z |
| 10 | Documentation | ✅ Passed | 2025-12-22T11:10:00Z |
| 11 | Traceability | ✅ Passed | 2025-12-22T11:15:00Z |
| 12 | Final Validation | ✅ Passed | 2025-12-22T11:20:00Z |

## Artifacts Generated

| Category | Count |
|----------|-------|
| arc42 Sections | 11 folders |
| ADRs | 10 documents |
| C4 Diagrams | 8 diagrams |
| Module Docs | 5 per module |
| Runbooks | 5 documents |
| Total Files | 45+ |

## Traceability Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Pain Point Coverage | 100% | 100% | ✅ |
| P0 Requirement Coverage | 100% | 100% | ✅ |
| Module Coverage | 100% | 100% | ✅ |
| ADR Completeness | 100% | 100% | ✅ |

## Quality Gate Results

All checkpoints passed validation.

### Blocking Checkpoints Verified

- Checkpoint 1 (Input Validation): ProductSpecs and Prototype complete
- Checkpoint 11 (Traceability): 100% coverage achieved

## Recommendations

1. Review ADRs with development team before implementation
2. Update runbooks during initial deployment phase
3. Schedule quarterly architecture review
```

## Template: GENERATION_SUMMARY.md

```markdown
---
document_id: SA-GENERATION-SUMMARY
version: 1.0.0
generated_at: 2025-12-22T10:00:00Z
---

# Solution Architecture Generation Summary

## Executive Summary

Solution Architecture documentation has been successfully generated for the **Inventory Management System**. This documentation provides comprehensive guidance for development teams implementing the system.

### Key Statistics

| Metric | Value |
|--------|-------|
| ADRs Created | 10 |
| Components Documented | 5 modules |
| C4 Diagrams | 8 |
| Quality Scenarios | 12 |
| Runbooks | 5 |

## Architecture Overview

### Style

**Modular Monolith** (ADR-001)
- Single deployment unit
- Clear module boundaries
- Shared database with schema separation

### Technology Stack (ADR-002)

| Layer | Technology |
|-------|------------|
| Frontend | React + TypeScript |
| Backend | .NET 8 |
| Database | PostgreSQL |
| Cache | Redis |
| Events | RabbitMQ |

### Modules

| Module | Priority | Screens | APIs |
|--------|----------|---------|------|
| Stock Adjustment | P0 | 5 | 6 |
| Exception Dashboard | P0 | 3 | 4 |
| Transaction History | P1 | 2 | 3 |
| Approval Workflow | P1 | 3 | 4 |
| Bin Management | P2 | 4 | 5 |

## ADR Summary

| Category | ADRs |
|----------|------|
| Foundation | ADR-001, ADR-002, ADR-003 |
| Data | ADR-004 |
| Integration | ADR-005, ADR-006 |
| Security | ADR-007 |
| Operations | ADR-008, ADR-009, ADR-010 |

## Output Structure

```
SolArch_InventorySystem/
├── 01-introduction-goals/
├── 02-constraints/
├── 03-context-scope/
├── 04-solution-strategy/
├── 05-building-blocks/
├── 06-runtime/
├── 07-quality/
├── 08-deployment/
├── 09-decisions/
├── 10-risks/
├── 11-glossary/
├── _registry/
└── diagrams/
```

## Next Steps

### Development Handoff

1. **Review Session**: Schedule ADR review with development team
2. **Tech Stack Setup**: Prepare development environment per ADR-002
3. **Module Prioritization**: Start with P0 modules

### Implementation Priorities

1. Authentication infrastructure (ADR-007)
2. Event bus setup (ADR-006)
3. API scaffolding (ADR-005)
4. P0 module development

### Ongoing Maintenance

- Review architecture quarterly
- Update ADRs when decisions change
- Keep runbooks current with deployments
```

## Output Format

```
═══════════════════════════════════════════════════════════════
 CHECKPOINT 12: FINAL VALIDATION - COMPLETED
═══════════════════════════════════════════════════════════════

 SOLUTION ARCHITECTURE GENERATION COMPLETE

System: InventorySystem
Duration: 20 minutes

Generated:
├─ arc42 Sections: 11 folders
├─ ADRs: 10 documents
├─ C4 Diagrams: 8 files
├─ Runbooks: 5 documents
└─ Total Files: 45+

Coverage:
├─ Pain Points: 100% ✅
├─ P0 Requirements: 100% ✅
└─ Modules: 100% ✅

All 13 Checkpoints: ✅ PASSED

Output: SolArch_InventorySystem/

Documentation:
├─ _registry/VALIDATION_REPORT.md
├─ _registry/GENERATION_SUMMARY.md
└─ traceability/solarch_traceability_register.json

═══════════════════════════════════════════════════════════════
```

## Checkpoint Validation

```bash
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 12 --dir SolArch_InventorySystem/
```

**Required for Checkpoint 12:**
- `_registry/VALIDATION_REPORT.md` exists
- `_registry/GENERATION_SUMMARY.md` exists

## Error Handling

| Error | Action |
|-------|--------|
| Progress file missing | Reconstruct from folder state |
| Report generation fails | Create minimal report |

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch-trace` | Previous phase (Checkpoint 11) |
| `/solarch-status` | Check final status |
| `/solarch-feedback` | Process change requests |
