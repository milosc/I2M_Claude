---
description: Comprehensive integrity check for all stages - state, traceability, build artifacts, and template drift
argument-hint: None
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /integrity-check started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /integrity-check ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /integrity-check instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## Usage

```
/integrity-check                           # Full integrity report
/integrity-check --quick                   # Quick summary only
/integrity-check --section state           # Check only state files
/integrity-check --section traceability    # Check only traceability
/integrity-check --section artifacts       # Check only build artifacts
/integrity-check --section links           # Check only cross-stage links
/integrity-check --section drift           # Check only template drift
/integrity-check --json                    # Output as JSON
/integrity-check --fix                     # Show fix instructions
```

## Arguments

| Argument | Description |
|----------|-------------|
| `--quick` | Show summary only (counts and overall status) |
| `--section <name>` | Check only a specific section: `state`, `traceability`, `artifacts`, `links`, `drift` |
| `--json` | Output results as JSON for programmatic use |
| `--fix` | Include detailed fix instructions for each issue |

## What Gets Checked

### 1. State Files (`_state/`)

- Presence of expected state files per initialized stage
- JSON schema validation
- Required fields presence
- Checkpoint consistency (current_checkpoint matches status)

### 2. Traceability Files (`traceability/`)

- All expected registries exist per initialized stage
- Schema validation against `_schema_index.json`
- Required fields and documentation blocks
- Item counts and coverage percentages

### 3. Build Artifacts (per stage)

| Stage | Checked Artifacts |
|-------|-------------------|
| Discovery | `PROGRESS_TRACKER.md`, `ANALYSIS_SUMMARY.md`, personas, JTBD, strategy docs |
| Prototype | `00-foundation/`, `01-components/`, `02-screens/`, `prototype/` code |
| ProductSpecs | `01-modules/`, `02-api/`, `03-tests/`, `04-jira/` |
| SolArch | `01-introduction-goals/` through `11-glossary/`, ADRs |
| Implementation | `src/`, `tests/`, `tasks/`, `reports/` |

### 4. Cross-Stage Links

- Pain Point IDs referenced in JTBDs exist
- JTBD IDs referenced in Requirements exist
- Screen IDs referenced in Modules exist
- Module IDs referenced in Tasks exist
- All upstream references are valid

### 5. Template Drift

- Compare current files against `.claude/templates/` init templates
- Detect missing documentation blocks
- Detect missing required fields
- Flag schema version mismatches

## Procedure

### Step 1: Run Integrity Checker
   ```bash
   python3 .claude/hooks/integrity_checker.py
   ```

2. **Parse Results**
   - Categorize issues by severity (ERROR, WARNING, INFO)
   - Group by section (state, traceability, artifacts, links, drift)

3. **Generate Report** (format based on flags)

## Report Formats

### Full Report (default)

```
╔══════════════════════════════════════════════════════════════════════════╗
║                         INTEGRITY CHECK REPORT                           ║
╠══════════════════════════════════════════════════════════════════════════╣
║  Project Root: /path/to/project                                          ║
║  Timestamp: 2025-12-25T10:30:00Z                                         ║
║  Overall Status: ⚠️ ISSUES FOUND                                         ║
╚══════════════════════════════════════════════════════════════════════════╝

📊 SUMMARY
┌────────────────────┬────────┬──────────┬────────┐
│ Section            │ Errors │ Warnings │ Info   │
├────────────────────┼────────┼──────────┼────────┤
│ State Files        │ 0      │ 1        │ 0      │
│ Traceability       │ 0      │ 0        │ 2      │
│ Build Artifacts    │ 2      │ 3        │ 0      │
│ Cross-Stage Links  │ 1      │ 0        │ 0      │
│ Template Drift     │ 0      │ 2        │ 0      │
├────────────────────┼────────┼──────────┼────────┤
│ TOTAL              │ 3      │ 6        │ 2      │
└────────────────────┴────────┴──────────┴────────┘

═══════════════════════════════════════════════════════════════════════════
📁 STATE FILES
═══════════════════════════════════════════════════════════════════════════

✅ _state/discovery_config.json - Valid
✅ _state/discovery_progress.json - Valid
✅ _state/prototype_config.json - Valid
✅ _state/prototype_progress.json - Valid
⚠️ _state/implementation_progress.json
   └─ WARNING: current_checkpoint (5) inconsistent with checkpoints status

═══════════════════════════════════════════════════════════════════════════
📋 TRACEABILITY FILES
═══════════════════════════════════════════════════════════════════════════

✅ traceability/client_facts_registry.json - 45 items
✅ traceability/pain_point_registry.json - 20 items
✅ traceability/jtbd_registry.json - 35 items
✅ traceability/requirements_registry.json - 12 items
✅ traceability/screen_registry.json - 18 items
ℹ️ traceability/task_registry.json - 0 items (pending initialization)
ℹ️ traceability/review_registry.json - 0 items (pending review)

═══════════════════════════════════════════════════════════════════════════
🏗️ BUILD ARTIFACTS
═══════════════════════════════════════════════════════════════════════════

Discovery (ClientAnalysis_InventorySystem/)
├── ✅ 00-management/PROGRESS_TRACKER.md
├── ✅ 01-analysis/ANALYSIS_SUMMARY.md
├── ✅ 02-research/personas/ (4 files)
├── ✅ 02-research/JOBS_TO_BE_DONE.md
├── ✅ 03-strategy/ (4 files)
└── ✅ 05-documentation/INDEX.md

Prototype (Prototype_InventorySystem/)
├── ✅ 00-foundation/design-tokens.json
├── ✅ 01-components/ (15 specs)
├── ❌ 02-screens/ - Missing: S-3.2, S-4.1
└── ⚠️ prototype/src/ - Missing component implementations

ProductSpecs (ProductSpecs_InventorySystem/)
├── ✅ 01-modules/ (15 modules)
├── ✅ 02-api/api-index.md
├── ⚠️ 03-tests/ - 3 test specs incomplete
└── ✅ 04-jira/full-hierarchy.csv

Implementation (Implementation_InventorySystem/)
├── ✅ src/components/ (12 components)
├── ❌ tests/unit/ - Missing tests for 5 components
├── ⚠️ tasks/TASK_INDEX.md - 3 tasks without status
└── ✅ reports/CODE_REVIEW.md

═══════════════════════════════════════════════════════════════════════════
🔗 CROSS-STAGE LINKS
═══════════════════════════════════════════════════════════════════════════

✅ Pain Points → JTBDs: All 20 PPs linked
✅ JTBDs → Requirements: 32/35 linked (91%)
✅ Requirements → Screens: 12/12 linked (100%)
❌ Screens → Modules: SCR-MOB-INV-03 references non-existent MOD-XXX

═══════════════════════════════════════════════════════════════════════════
📝 TEMPLATE DRIFT
═══════════════════════════════════════════════════════════════════════════

⚠️ _state/implementation_progress.json
   └─ Missing field: code_review.status (required by template)

⚠️ traceability/task_registry.json
   └─ $documentation.purpose differs from template

═══════════════════════════════════════════════════════════════════════════
🔧 RECOMMENDED ACTIONS
═══════════════════════════════════════════════════════════════════════════

1. Fix missing screen specifications:
   /prototype-screens S-3.2 S-4.1

2. Regenerate tests for untested components:
   /htec-sdd-implement --task T-015 T-018 T-021 T-024 T-027

3. Repair template drift:
   /traceability-init --repair

4. Fix invalid cross-stage link (SCR-MOB-INV-03):
   Check module_ref in screen_registry.json
```

### Quick Report (--quick)

```
INTEGRITY CHECK: ⚠️ ISSUES FOUND

State Files:       ✅ 5/5 valid (1 warning)
Traceability:      ✅ 14/14 present (2 info)
Build Artifacts:   ⚠️ 2 errors, 3 warnings
Cross-Stage Links: ❌ 1 broken link
Template Drift:    ⚠️ 2 drifted files

Run /integrity-check for full report.
Run /integrity-check --fix for remediation instructions.
```

### JSON Output (--json)

```json
{
  "timestamp": "2025-12-25T10:30:00Z",
  "project_root": "/path/to/project",
  "overall_status": "ISSUES_FOUND",
  "summary": {
    "errors": 3,
    "warnings": 6,
    "info": 2
  },
  "sections": {
    "state": {
      "status": "WARNING",
      "issues": [...]
    },
    "traceability": {
      "status": "OK",
      "issues": [...]
    },
    "artifacts": {
      "status": "ERROR",
      "issues": [...]
    },
    "links": {
      "status": "ERROR",
      "issues": [...]
    },
    "drift": {
      "status": "WARNING",
      "issues": [...]
    }
  },
  "recommended_actions": [...]
}
```

## Integration Points

The integrity checker integrates with:

| Tool | Integration |
|------|-------------|
| `/traceability-init --repair` | Fixes traceability structure issues |
| `/discovery-validate` | Re-validates Discovery outputs |
| `/prototype-qa` | Re-runs Prototype quality checks |
| `/productspecs-finalize` | Re-validates ProductSpecs traceability |
| `/solarch-trace` | Re-validates SolArch traceability |
| `/htec-sdd-review` | Re-runs Implementation code review |

## When to Run

| Scenario | Recommendation |
|----------|----------------|
| After completing a stage | Run full check |
| Before starting next stage | Run full check |
| After feedback implementation | Run `--section links` |
| After template updates | Run `--section drift` |
| CI/CD pipeline | Run `--quick --json` |
| Debugging issues | Run `--fix` |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed (only INFO issues) |
| 1 | Warnings found (no errors) |
| 2 | Errors found |
| 3 | Critical errors (cannot proceed) |


---

## Related

- `/traceability-status` - Traceability-specific status
- `/traceability-init` - Initialize or repair traceability backbone
- `Integrity_Checker` skill - Underlying validation logic
- Quality gates per stage (discovery, prototype, productspecs, solarch, implementation)
