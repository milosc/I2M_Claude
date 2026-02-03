---
name: discovery-rebuild-traceability
description: Rebuild traceability registry from discovery artifacts
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-rebuild-traceability started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-rebuild-traceability ended '{"stage": "discovery"}'
---


# Rebuild Traceability Registries

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-rebuild-traceability instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Discovery-specific rules. Load them now:

```bash
# Load Discovery rules (includes PDF handling, input processing, output structure)
/rules-discovery

# Load Traceability rules (includes ID formats, source linking)
/rules-traceability
```

## Description

This command parses Discovery markdown files (PAIN_POINTS.md, JOBS_TO_BE_DONE.md, USER_TYPES.md, screen-definitions.md) and:
1. Populates the `traceability/` JSON registries with extracted data and cross-references
2. Generates `TRACEABILITY_MATRIX_MASTER.md` - condensed view of all traceability chains
3. Generates `TRACEABILITY_ASSESSMENT_REPORT.md` - formal assessment report with coverage statistics

**Use this when:**
- Traceability registries are empty or incomplete after a Discovery run
- You want to refresh traceability data from updated markdown files
- Registry JSON files got corrupted or deleted
- You need traceability documentation for stakeholder review

## Arguments

- `$ARGUMENTS`: Path to Discovery output directory (e.g., `ClientAnalysis_InventorySystem/`)

## Execution Steps

### Step 1: Execute Rebuild Script

```bash
python3 .claude/skills/tools/rebuild_traceability.py --dir $ARGUMENTS
```

## What It Does

### Phase 1: Parse Markdown Files

1. **Parses Pain Points** from `01-analysis/PAIN_POINTS.md`
   - Extracts: PP-X.Y IDs, titles, priorities, descriptions, impact, affected users
   - Populates: `traceability/pain_point_registry.json`

2. **Parses JTBDs** from `02-research/JOBS_TO_BE_DONE.md`
   - Extracts: JTBD-X.Y IDs, statements, priorities, related pain points
   - Populates: `traceability/jtbd_registry.json`

3. **Parses User Types** from `01-analysis/USER_TYPES.md`
   - Extracts: UT-X IDs, names, roles, categories
   - Populates: `traceability/user_type_registry.json`

4. **Parses Screens** from `04-design-specs/screen-definitions.md`
   - Extracts: M-XX/D-XX IDs, names, purposes, related JTBDs
   - Populates: `traceability/screen_registry.json`

5. **Creates Trace Links**
   - PP -> JTBD links (type: "addresses")
   - Screen -> JTBD links (type: "implements")
   - Populates: `traceability/trace_links.json`

### Phase 2: Generate Traceability Documents

6. **Generates TRACEABILITY_MATRIX_MASTER.md**
   - Complete chain table (Pain Point -> JTBD -> Screen -> Requirements -> Tests -> ADR)
   - Pain Points to JTBD mapping
   - JTBD to Requirements mapping
   - Screens to Tests mapping
   - Coverage summary
   - Sections without data left blank as placeholders for later phases

7. **Generates TRACEABILITY_ASSESSMENT_REPORT.md**
   - Executive summary with key metrics
   - Traceability chain model diagram
   - Complete end-to-end matrix
   - All registry contents in table format
   - Coverage statistics
   - Gap analysis
   - Recommendations
   - Appendices with ID reference guide

## Example

```bash
# Rebuild traceability for InventorySystem
/discovery-rebuild-traceability ClientAnalysis_InventorySystem/
```

## Output

The command produces:
1. **Console summary** showing counts of extracted items
2. **JSON registry files** in `traceability/`
3. **Markdown documents** in `traceability/`

## Files Updated/Created

### Registry Files (JSON)

| File | Content |
|------|---------|
| `traceability/pain_point_registry.json` | All PP-X.Y pain points |
| `traceability/jtbd_registry.json` | All JTBD-X.Y jobs |
| `traceability/user_type_registry.json` | All UT-X user types |
| `traceability/screen_registry.json` | All M-XX/D-XX screens |
| `traceability/trace_links.json` | Cross-reference links |

### Traceability Documents (Markdown)

| File | Content |
|------|---------|
| `traceability/TRACEABILITY_MATRIX_MASTER.md` | Condensed view of all chains |
| `traceability/TRACEABILITY_ASSESSMENT_REPORT.md` | Formal assessment report |

## Placeholder Sections

The following sections are left blank in generated documents, to be populated by later phases:

| Section | Populated By |
|---------|--------------|
| Client Facts | Interview analysis |
| Requirements (Epics, Stories) | Prototype phase |
| Test Cases | Product Specs phase |
| Modules | Product Specs phase |
| ADRs | Solution Architecture phase |

## Notes

- The `traceability/` directory is created if it doesn't exist
- Existing items with matching IDs are updated (not duplicated)
- Files that don't exist are skipped with a warning
- Run this after completing Discovery to ensure registries are populated
- Documents use data from JSON registries, so run rebuild after any registry updates

## Files Updated/Created
