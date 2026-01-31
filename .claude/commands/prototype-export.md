---
description: Export Prototype outputs for ProductSpecs stage
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-export started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-export ended '{"stage": "prototype"}'
---


# /prototype-export - Export Prototype Package

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-export instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Assembly-First and traceability rules:

```bash
# Assembly-First rules (loaded automatically in Prototype stage)
/_assembly_first_rules

# Traceability rules for ID management
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` and export options
  - `<SystemName>` - Target prototype
  - `--format <type>` - Export format: `full` (default), `specs`, `code`, `reports`
  - `--output <path>` - Custom output path

## Prerequisites

- Prototype completed: All 14 phases (or at least Phase 12)
- Validation reports generated

## Export Formats

### Full Export (Default)

Complete package with all artifacts.

```
/prototype-export InventorySystem
/prototype-export InventorySystem --format full
```

### Specs Only

Design and specification documents only (no code).

```
/prototype-export InventorySystem --format specs
```

### Code Only

Working prototype code only.

```
/prototype-export InventorySystem --format code
```

### Reports Only

Validation and summary reports only.

```
/prototype-export InventorySystem --format reports
```

---

## Execution Steps

### Step 1: Locate Prototype

Identify and validate prototype:
- Check `Prototype_<SystemName>/` exists
- Read `_state/prototype_progress.json`
- Verify minimum completion (Phase 12)

### Step 2: Validate Completeness

```
═══════════════════════════════════════════════════════
  EXPORT VALIDATION
═══════════════════════════════════════════════════════

  System:              <SystemName>
  Completed Phases:    14/14

  Validation Status:
  ├── Build Status:    ✅ Success
  ├── QA Report:       ✅ Present
  ├── UI Audit:        ✅ Present
  └── Traceability:    ✅ Complete

  Export Ready:        ✅ YES

═══════════════════════════════════════════════════════
```

If incomplete:

```
  ⚠️  WARNING: Prototype incomplete

  Missing:
  ├── Phase 13: QA Testing
  └── Phase 14: UI Audit

  Options:
  [E] Export Anyway - Proceed with partial export
  [C] Complete First - Run remaining phases
  [A] Abort
```

### Step 3: Generate Export Package

#### Full Export Structure

```
exports/Prototype_<SystemName>_<YYYYMMDD>/
├── README.md                        # Package overview
├── MANIFEST.md                      # Contents listing
├── discovery-link/
│   └── README.md                    # Link to ClientAnalysis
├── specifications/
│   ├── 00-foundation/               # Design system
│   │   ├── design-brief.md
│   │   ├── design-tokens.json
│   │   ├── color-system.md
│   │   ├── typography.md
│   │   └── spacing-layout.md
│   ├── 01-components/               # Component specs
│   │   ├── component-index.md
│   │   └── [category]/[component].md
│   ├── 02-screens/                  # Screen specs
│   │   ├── screen-index.md
│   │   └── [screen]/
│   ├── 03-interactions/             # Interaction specs
│   │   ├── motion-system.md
│   │   ├── accessibility-spec.md
│   │   └── responsive-behavior.md
│   └── 04-implementation/           # Implementation specs
│       ├── data-model.md
│       ├── api-contracts.json
│       ├── build-sequence.md
│       └── test-data/
├── prototype/                        # Working code
│   ├── package.json
│   ├── src/
│   ├── public/
│   └── README.md
├── validation/                       # QA artifacts
│   ├── qa-report.md
│   ├── ui-audit-report.md
│   └── screenshots/
├── reports/                          # Summary docs
│   ├── ARCHITECTURE.md
│   ├── README.md
│   └── TRACEABILITY_MATRIX.md
└── traceability/
    ├── prototype_traceability_register.json
    └── requirements_registry.json
```

#### Specs Only Structure

```
exports/Prototype_<SystemName>_Specs_<YYYYMMDD>/
├── README.md
├── 00-foundation/
├── 01-components/
├── 02-screens/
├── 03-interactions/
└── 04-implementation/
    ├── data-model.md
    ├── api-contracts.json
    └── build-sequence.md
```

#### Code Only Structure

```
exports/Prototype_<SystemName>_Code_<YYYYMMDD>/
├── README.md
├── package.json
├── src/
├── public/
├── vite.config.ts
└── tailwind.config.js
```

#### Reports Only Structure

```
exports/Prototype_<SystemName>_Reports_<YYYYMMDD>/
├── README.md
├── qa-report.md
├── ui-audit-report.md
├── ARCHITECTURE.md
├── TRACEABILITY_MATRIX.md
└── screenshots/
```

### Step 4: Generate Package README

```markdown
# Prototype Export: <SystemName>

## Package Information

| Field | Value |
|-------|-------|
| System Name | <SystemName> |
| Export Date | <YYYY-MM-DD> |
| Export Format | Full |
| Discovery Source | ClientAnalysis_<SystemName>/ |
| Prototype Version | 1.0.0 |

## Contents

### Specifications (`specifications/`)

Design system, component specs, screen specs, and implementation details.

### Prototype (`prototype/`)

Working React application.

**Quick Start:**
```bash
cd prototype
npm install
npm run dev
```

### Validation (`validation/`)

QA testing results and UI audit with screenshots.

### Reports (`reports/`)

Architecture overview and traceability documentation.

## Traceability

This prototype traces back to:
- **Discovery:** ClientAnalysis_<SystemName>/
- **Pain Points:** <N> addressed
- **Requirements:** <N> implemented
- **Coverage:** <X>%

## Next Steps

1. Review specifications with stakeholders
2. Run prototype locally for demonstration
3. Proceed to ProductSpecs stage for production specs

## Generated By

This package was generated by the Prototype Builder framework.
- Framework Version: 1.0.0
- Export Date: <YYYY-MM-DD HH:MM:SS>
```

### Step 5: Generate MANIFEST.md

```markdown
# Export Manifest

## Package: Prototype_<SystemName>_<YYYYMMDD>

### File Inventory

| Path | Type | Size | Description |
|------|------|------|-------------|
| README.md | Markdown | 2KB | Package overview |
| specifications/00-foundation/design-tokens.json | JSON | 5KB | Design tokens |
| specifications/01-components/component-index.md | Markdown | 3KB | Component index |
| ... | ... | ... | ... |

### Statistics

| Category | Count | Size |
|----------|-------|------|
| Specifications | 45 files | 120KB |
| Prototype Code | 35 files | 85KB |
| Validation | 8 files | 2MB |
| Reports | 4 files | 15KB |
| **Total** | **92 files** | **2.2MB** |

### Checksums

```
SHA256:
specifications/design-tokens.json: abc123...
prototype/package.json: def456...
```
```

### Step 6: Create Archive (Optional)

If requested, create zip archive:

```bash
cd exports
zip -r Prototype_<SystemName>_<YYYYMMDD>.zip Prototype_<SystemName>_<YYYYMMDD>/
```

### Step 7: Display Summary

```
═══════════════════════════════════════════════════════
  EXPORT COMPLETE
═══════════════════════════════════════════════════════

  System:              <SystemName>
  Format:              Full Export
  Output:              exports/Prototype_<SystemName>_<YYYYMMDD>/

  Package Contents:
  ├── Specifications:  45 files
  ├── Prototype Code:  35 files
  ├── Validation:      8 files
  └── Reports:         4 files

  Total Size:          2.2 MB

═══════════════════════════════════════════════════════

  Package Location:
  exports/Prototype_<SystemName>_<YYYYMMDD>/

  To run prototype:
  cd exports/Prototype_<SystemName>_<YYYYMMDD>/prototype
  npm install && npm run dev

  Next Steps:
  • Share package with stakeholders
  • Proceed to /productspecs for production specs

═══════════════════════════════════════════════════════
```

---

## ProductSpecs Integration

The export package is structured for seamless handoff to the ProductSpecs stage:

```
/productspecs Prototype_<SystemName>_<YYYYMMDD>/
```

The ProductSpecs generator will:
1. Read all specifications
2. Read traceability data
3. Generate production-ready specs
4. Create development stories

---

## Error Handling

| Error | Action |
|-------|--------|
| Prototype not found | Display error, list available |
| Incomplete prototype | Warn, offer partial export |
| Output path not writable | Display error, suggest alternative |
| Large file copy fails | Log, continue with others |

---

## Examples

### Example 1: Full Export

```
/prototype-export InventorySystem

> Validating prototype...
> ✅ All 14 phases complete
> Creating export package...
> ✅ Export complete: exports/Prototype_InventorySystem_20240115/
```

### Example 2: Specs Only

```
/prototype-export InventorySystem --format specs

> Creating specs-only package...
> ✅ Export complete: exports/Prototype_InventorySystem_Specs_20240115/
```

### Example 3: Custom Output Path

```
/prototype-export InventorySystem --output ~/Deliverables/

> Creating export package...
> ✅ Export complete: ~/Deliverables/Prototype_InventorySystem_20240115/
```

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype-status` | Check prototype status |
| `/prototype-qa` | Run QA before export |
| `/productspecs` | Generate production specs |
