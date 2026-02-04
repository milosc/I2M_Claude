---
name: solarch-trace
description: Display Solution Architecture traceability coverage
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-trace started '{"stage": "solarch"}'
  Stop:
    - hooks:
        # VALIDATION: Check traceability validation was completed
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_solarch_output.py"
            --system-name "$(cat _state/session.json 2>/dev/null | grep -o '"project"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"project"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//')"
            --phase trace
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-trace ended '{"stage": "solarch", "validated": true}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-trace instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

This command validates that all traceability chains are complete, ensuring 100% coverage of pain points, P0 requirements, and module architecture. This is Checkpoint 11 of the pipeline and is **BLOCKING**.

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` (auto-detected from config if not provided)

## Usage

```bash
/solarch-trace InventorySystem
```

## Prerequisites

- Checkpoint 10 passed (`/solarch-docs` completed)
- All ADRs and components registered

## Skills Used

Read BEFORE execution:
- `.claude/skills/SolutionArchitecture_E2ETraceabiliyAnalyzer/SKILL.md`

## Execution Steps

### Step 1: Execute

```
LOAD _state/solarch_config.json
SYSTEM_NAME = config.system_name

USE E2ETraceabiliyAnalyzer skill:

  LOAD source registries (v3.0 - ROOT level):
    - ClientAnalysis_X/PAIN_POINTS.md → pain_points[]
    - traceability/requirements_registry.json → requirements[]
    - traceability/module_registry.json → modules[]

  LOAD architecture registries (v3.0 - ROOT level):
    - traceability/adr_registry.json → adrs[]
    - traceability/component_registry.json → components[]
    # NOTE: Local _registry/ folders DEPRECATED

  VALIDATE Rule 1: Pain Point Coverage (100% required)
    FOR each pain_point IN pain_points:
      CHECK at least one ADR references pain_point.id
      IF NOT found:
        ADD to coverage_gaps

    coverage = covered / total * 100
    IF coverage < 100:
      BLOCKING: "Pain point coverage: {coverage}% (required: 100%)"

  VALIDATE Rule 2: P0 Requirement Coverage (100% required)
    p0_requirements = filter(requirements, priority == "P0")
    FOR each req IN p0_requirements:
      CHECK at least one ADR references req.id
      IF NOT found:
        ADD to requirement_gaps

    p0_coverage = covered / total * 100
    IF p0_coverage < 100:
      BLOCKING: "P0 requirement coverage: {p0_coverage}% (required: 100%)"

  VALIDATE Rule 3: Module Architecture Coverage (100% required)
    FOR each module IN modules:
      CHECK component exists for module
      CHECK module mentioned in building blocks
      IF NOT found:
        ADD to module_gaps

    module_coverage = architected / total * 100
    IF module_coverage < 100:
      BLOCKING: "Module architecture coverage: {module_coverage}% (required: 100%)"

  VALIDATE Rule 4: ADR Completeness
    FOR each adr IN adrs:
      CHECK traceability section exists
      CHECK pain_points array not empty
      IF incomplete:
        ADD to adr_issues

  VALIDATE Rule 5: Cross-Reference Integrity
    FOR each reference IN all_references:
      CHECK target exists
      IF NOT exists:
        ADD to broken_references

GENERATE TRACEABILITY_VALIDATION_REPORT.md:
  Summary:
    - Pain Point Coverage: X%
    - P0 Requirement Coverage: X%
    - Module Coverage: X%
    - ADR Completeness: X%
    - Cross-Reference Integrity: X%

  Gaps Found:
    - List of uncovered items

  Recommendations:
    - How to fix gaps

UPDATE traceability/traceability_matrix_master.json (ROOT level, v3.0):
  {
    "$metadata": { updated_at: NOW() },
    "stage": "SolutionArchitecture",
    "checkpoint": 11,
    "mappings": {...},
    "coverage": {
      "pain_points": { "total": N, "addressed": N, "coverage_percent": 100 },
      "requirements": { "total": N, "covered": N, "coverage_percent": 100 },
      "modules": { "total": N, "covered": N, "coverage_percent": 100 }
    },
    "validation": {
      "passed": true/false,
      "timestamp": NOW(),
      "issues": [...]
    }
  }
  # NOTE: Local _registry/architecture-traceability.json is DEPRECATED

UPDATE _state/solarch_progress.json:
  phases.trace.status = "completed" OR "failed"
  phases.trace.completed_at = NOW()
  current_checkpoint = 11

RUN quality gate:
  python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 11 --dir {OUTPUT_PATH}/

IF validation fails:
  DISPLAY blocking error with fix instructions
  STOP execution

DISPLAY checkpoint 11 summary
```

### Step 2: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-trace" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Traceability Chain

```
CM-XXX (Client Material)
    ↓
PP-X.X (Pain Point)        ← Must be covered by ADR
    ↓
JTBD-X.X (Job To Be Done)
    ↓
REQ-XXX (Requirement)      ← P0 must be covered by ADR
    ↓
MOD-XXX (Module Spec)      ← Must have architecture component
    ↓
ADR-XXX (Architecture Decision)
    ↓
COMP-XXX (Component)
    ↓
QS-XXX (Quality Scenario)
```

## Validation Rules

| Rule | Threshold | Blocking |
|------|-----------|----------|
| Pain Point Coverage | 100% | YES |
| P0 Requirement Coverage | 100% | YES |
| Module Architecture Coverage | 100% | YES |
| ADR Completeness | 100% | NO (warning) |
| Cross-Reference Integrity | 100% | NO (warning) |

## Output Format

### Success

```
═══════════════════════════════════════════════════════════════
 CHECKPOINT 11: TRACEABILITY VALIDATION - PASSED [BLOCKING]
═══════════════════════════════════════════════════════════════

Traceability Coverage:
├─ Pain Points: 10/10 (100%) ✅
├─ P0 Requirements: 15/15 (100%) ✅
├─ P1 Requirements: 8/11 (73%) ✓
└─ Modules: 5/5 (100%) ✅

ADR Coverage:
├─ ADRs with Traceability: 10/10 (100%) ✅
└─ Cross-References Valid: 42/42 (100%) ✅

Complete Chains:
├─ PP → ADR → Component: 10 complete
└─ REQ → Module → Component: 15 complete

Quality Gate: ✅ PASSED

Next: /solarch-finalize InventorySystem
═══════════════════════════════════════════════════════════════
```

### Failure (Blocking)

```
═══════════════════════════════════════════════════════════════
 CHECKPOINT 11: TRACEABILITY VALIDATION - FAILED [BLOCKING]
═══════════════════════════════════════════════════════════════

Traceability Coverage:
├─ Pain Points: 8/10 (80%) ❌
├─ P0 Requirements: 14/15 (93%) ❌
└─ Modules: 5/5 (100%) ✅

BLOCKING ISSUES:

Pain Points Not Covered:
1. PP-3.2: No ADR addresses "Report generation delays"
2. PP-4.1: No ADR addresses "Manual approval bottlenecks"

P0 Requirements Not Covered:
1. REQ-012 (P0): "Batch adjustment support" - No ADR reference

To Fix:
1. Add PP-3.2 reference to ADR-005 (API Design) or create new ADR
2. Add PP-4.1 reference to ADR-007 (Security) or create new ADR
3. Add REQ-012 to ADR-003 (Module Structure) traceability

Re-run validation:
  /solarch-trace InventorySystem

═══════════════════════════════════════════════════════════════
```

## Output Files

### _registry/

| File | Content |
|------|---------|
| `architecture-traceability.json` | Updated traceability data |
| `TRACEABILITY_VALIDATION_REPORT.md` | Validation report |

## Checkpoint Validation

```bash
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 11 --dir SolArch_InventorySystem/

# Or validate traceability specifically:
python3 .claude/hooks/solarch_quality_gates.py --validate-traceability --dir SolArch_InventorySystem/
```

**Required for Checkpoint 11:**
- `_registry/architecture-traceability.json` exists
- Pain point coverage = 100%
- P0 requirement coverage = 100%
- Module coverage = 100%

## Error Handling

| Error | Action |
|-------|--------|
| Pain point not covered | BLOCKING - show which ADRs could address it |
| P0 requirement not covered | BLOCKING - show which ADRs could address it |
| Module not architected | BLOCKING - require component creation |
| Broken reference | Warning - note in report |

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch-docs` | Previous phase (Checkpoint 10) |
| `/solarch-finalize` | Next phase (Checkpoint 12) |
