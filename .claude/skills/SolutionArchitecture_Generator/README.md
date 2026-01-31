# Solution Architecture Generator

> **Version**: 2.1.0
> **Purpose**: Transform Product Specifications into comprehensive Solution Architecture documentation

---

## 🚀 Quick Start

**Copy one of these prompts to execute:**

### Automatic Mode (runs all checkpoints)
```
# Solution Architecture Generator - AUTO MODE

Project: InventorySystem
Mode: AUTO

Sources:
- Specs: /BuilderPrompts/Test/05_Product_Specifications_InventorySystem/
- Prototype: /BuilderPrompts/Test/04_Prototype_InventorySystem/
- Analysis: /BuilderPrompts/Test/03_ClientAnalysis_InventorySystem/

Target: /BuilderPrompts/Test/06_Solution_Architecture_InventorySystem/
Skills: /BuilderPrompts/ATS Series/06-SolutionArchitecture/

Execute all 12 checkpoints automatically. Stop only on validation failures.
```

### Interactive Mode (review each checkpoint)
```
# Solution Architecture Generator - INTERACTIVE MODE

Project: InventorySystem
Mode: INTERACTIVE

Sources:
- Specs: /BuilderPrompts/Test/05_Product_Specifications_InventorySystem/
- Prototype: /BuilderPrompts/Test/04_Prototype_InventorySystem/
- Analysis: /BuilderPrompts/Test/03_ClientAnalysis_InventorySystem/

Target: /BuilderPrompts/Test/06_Solution_Architecture_InventorySystem/
Skills: /BuilderPrompts/ATS Series/06-SolutionArchitecture/

Execute checkpoints one at a time. Pause after each for my review.
I will respond with: continue | retry | skip | abort
```

---

## Execution Modes

| Mode | Behavior | Best For |
|------|----------|----------|
| **AUTO** | Runs all 12 checkpoints, stops only on errors | Fast generation, trusted inputs |
| **INTERACTIVE** | Pauses after each checkpoint for review | First run, learning, verification |

### Interactive Commands

| Command | Action |
|---------|--------|
| `c` / `continue` | Proceed to next checkpoint |
| `r` / `retry` | Re-run current checkpoint |
| `s` / `skip` | Skip to next (mark incomplete) |
| `a` / `abort` | Stop and save progress |
| `status` | Show full progress |

---

## Checkpoints

| # | Name | Outputs | Gate |
|---|------|---------|------|
| 1 | Initialize Structure | Folders, registry files | - |
| 2 | Context Extraction | Introduction, stakeholders, C4 context | - |
| 3 | Constraints | Business, technical, regulatory | - |
| 4 | Solution Strategy | ADR-001, strategy doc | **Gate 1** |
| 5 | Technology Stack | ADR-002 | - |
| 6 | Module Structure | ADR-003, C4 container | - |
| 7 | Module Components | C4 component per module | **Gate 2** |
| 8 | API Design | ADR-005, API contracts | - |
| 9 | Event Communication | ADR-006, event catalog | - |
| 10 | Security | ADR-007, security doc | **Gate 3** |
| 11 | Quality & ADRs | ADR-004,008,009, quality docs | - |
| 12 | Deployment & Validation | ADR-010, final validation | **Gate 4** |

---

## File Structure

```
06-SolutionArchitecture/
├── README.md                 # This file
├── SKILL.md                  # Master orchestration skill
├── skills/
│   ├── arc42-generator.md    # arc42 section templates
│   ├── adr-generator.md      # ADR creation
│   ├── c4-generator.md       # C4 diagrams
│   ├── contract-generator.md # API/Event contracts
│   └── traceability-analyzer.md
└── prompts/
    ├── RUN.md                # ⭐ START HERE - execution prompts
    ├── CHECKPOINT_LOGIC.md   # Internal execution logic
    ├── CHECKPOINT_EXECUTION.md
    └── MASTER_EXECUTION.md
```

---

## Output

```
06_Solution_Architecture_{project}/
├── README.md
├── GENERATION_SUMMARY.md
├── TRACEABILITY_VALIDATION_REPORT.md
├── _registry/           # Machine-readable indexes
├── _state/              # Execution progress
├── 01-introduction-goals/
├── 02-constraints/
├── 03-context-scope/    # + C4 Context diagram
├── 04-solution-strategy/
├── 05-building-blocks/  # + C4 Container/Component
├── 06-runtime-view/
├── 07-deployment-view/  # + C4 Deployment
├── 08-cross-cutting/
├── 09-decisions/        # 10+ ADRs
├── 10-information-design/
├── 11-quality/
├── 12-risks-debt/
└── 13-glossary/
```

**~40-50 files** depending on module count

---

## Traceability Guarantee

Every decision traces back to source:

```
Pain Point (PP-*) → JTBD → Requirement (US/FR-*) → Module (MOD-*) → ADR
```

Validation ensures:
- ✓ 100% pain point coverage
- ✓ 100% P0 requirement coverage  
- ✓ 100% module diagram coverage
- ✓ All ADRs have traceability sections

---

## Quality Gates

| Gate | After | Must Pass |
|------|-------|-----------|
| 1 | CP-4 | Stakeholders, external systems, C4 context |
| 2 | CP-7 | ADR traceability, pain point coverage |
| 3 | CP-10 | All modules diagrammed, patterns defined |
| 4 | CP-12 | Full validation, all metrics at 100% |

---

**Last Updated**: 2025-12-16
