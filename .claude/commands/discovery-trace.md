---
name: discovery-trace
description: Display Discovery traceability chain coverage
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-trace started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-trace ended '{"stage": "discovery"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-trace instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Discovery-specific rules. Load them now:

```bash
# Load Discovery rules (includes PDF handling, input processing, output structure)
/rules-discovery

# Load Traceability rules (includes ID formats, source linking)
/rules-traceability
```

## Arguments

None required - reads from `traceability/` files

## Prerequisites

- Discovery session in progress or complete
- `traceability/trace_matrix.json` exists

## Skills Used

None - utility command reading traceability files

## Execution Steps

1. **Load Traceability Files**
   - Read `traceability/trace_matrix.json`
   - Read `traceability/pain_point_registry.json`
   - Read `traceability/jtbd_registry.json`
   - Read `traceability/requirements_registry.json`
   - Read `traceability/screen_registry.json`

2. **Calculate Coverage Statistics**
   - Count items at each level
   - Calculate trace percentages
   - Identify orphans (untraced items)
   - Identify gaps (incomplete chains)

3. **Display Traceability Report**
   ```
   ╔════════════════════════════════════════════════════════════╗
   ║            TRACEABILITY COVERAGE REPORT                     ║
   ╠════════════════════════════════════════════════════════════╣
   ║ Pipeline Stage:  Discovery                                  ║
   ║ Last Updated:    2025-01-15                                 ║
   ╚════════════════════════════════════════════════════════════╝

   OVERALL COVERAGE
   ────────────────────────────────────────────────────────────

   P0 Pain Points → Screens:  ████████████████████ 100% (5/5)
   P1 Pain Points → Screens:  ████████████░░░░░░░░  60% (3/5)
   P2 Pain Points → Screens:  ░░░░░░░░░░░░░░░░░░░░   0% (0/2)

   CHAIN STATISTICS
   ────────────────────────────────────────────────────────────

   | Artifact Type    | Total | Traced | Orphaned | Coverage |
   |------------------|-------|--------|----------|----------|
   | Pain Points (P0) |     5 |      5 |        0 |     100% |
   | Pain Points (P1) |     5 |      3 |        2 |      60% |
   | Pain Points (P2) |     2 |      0 |        2 |       0% |
   | JTBDs            |    12 |     10 |        2 |      83% |
   | Features         |    15 |     12 |        3 |      80% |
   | Screens          |     8 |      8 |        0 |     100% |

   TRACEABILITY CHAINS
   ────────────────────────────────────────────────────────────

   CHAIN-1.1: ✅ Fully Traced
   PP-1.1 → JTBD-1.1 → US-1.1 → S-1.1, S-1.2

   CHAIN-1.2: ✅ Fully Traced
   PP-1.2 → JTBD-1.2 → US-1.2 → S-1.3

   CHAIN-2.1: ⚠️ Incomplete (Missing Screen)
   PP-2.1 → JTBD-2.1 → US-2.1 → ???

   CHAIN-3.1: ❌ Orphaned
   PP-3.1 → ??? (No JTBD linked)

   ORPHANED ITEMS
   ────────────────────────────────────────────────────────────

   Pain Points without JTBD:
   • PP-3.1: [Description] (P2)

   JTBDs without Features:
   • JTBD-4.1: [Description]
   • JTBD-4.2: [Description]

   Features without Screens:
   • US-2.1: [Description]
   • US-3.2: [Description]
   • US-3.3: [Description]

   COVERAGE BY PRIORITY
   ────────────────────────────────────────────────────────────

   P0 (Critical):
   ┌────────────────────────────────────────────────────┐
   │ ████████████████████████████████████████████ 100%  │
   │ 5/5 fully traced to screens                        │
   └────────────────────────────────────────────────────┘

   P1 (High):
   ┌────────────────────────────────────────────────────┐
   │ ████████████████████████░░░░░░░░░░░░░░░░░░░░  60%  │
   │ 3/5 traced, 2 missing screen coverage              │
   └────────────────────────────────────────────────────┘

   P2 (Medium):
   ┌────────────────────────────────────────────────────┐
   │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0%  │
   │ 0/2 traced (future phases)                         │
   └────────────────────────────────────────────────────┘

   RECOMMENDATIONS
   ────────────────────────────────────────────────────────────

   ✅ P0 coverage meets requirement (100%)
   ⚠️  Consider adding screens for: US-2.1
   ℹ️  P2 items planned for Phase 3

   VALIDATION STATUS
   ────────────────────────────────────────────────────────────

   Ready for Prototype: ✅ Yes (P0 = 100%)
   ```

## Coverage Calculations

| Metric | Formula |
|--------|---------|
| P0 Coverage | P0 Pain Points with Screen / Total P0 |
| Chain Coverage | Complete Chains / Total Chains |
| Orphan Rate | Items with No Links / Total Items |

## Status Indicators

| Icon | Meaning |
|------|---------|
| ✅ | Fully traced |
| ⚠️ | Partially traced |
| ❌ | Orphaned/Not traced |
| ℹ️ | Informational |

## Output Sections

| Section | Description |
|---------|-------------|
| Overall Coverage | P0/P1/P2 end-to-end coverage |
| Chain Statistics | Counts by artifact type |
| Traceability Chains | Individual chain status |
| Orphaned Items | Items missing links |
| Recommendations | Actions to improve coverage |

## Outputs

- Traceability report displayed to console
- No files modified

### Step 4: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
- Ready for next stage: `/discovery-export`
