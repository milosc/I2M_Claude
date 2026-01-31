---
name: Comprehensive Integrity Check
description: Use when validating the overall health of the end-to-end framework - state files, traceability registries, build artifacts per stage, cross-stage links, and template drift. Can be run at any point to generate an integrity report.
model: sonnet
allowed-tools: Read, Grep, Glob, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Comprehensive Integrity Check started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Comprehensive Integrity Check ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Comprehensive Integrity Check instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Comprehensive Integrity Check

## Purpose

This skill performs end-to-end validation of the entire framework state, detecting issues across:

1. **State Files** (`_state/`) - Configuration and progress tracking
2. **Traceability Files** (`traceability/`) - Registries and trace links
3. **Build Artifacts** - Stage-specific outputs
4. **Cross-Stage Links** - ID references between stages
5. **Template Drift** - Deviations from expected structure

## When to Use

| Scenario | Recommendation |
|----------|----------------|
| Completed a stage | Full check before proceeding |
| Starting new stage | Full check to verify inputs |
| After feedback implementation | Check `--section links` |
| Debugging issues | Full check with `--fix` |
| CI/CD pipeline | Quick check with `--json` |
| Template updates | Check `--section drift` |

## Prerequisites

1. **Project initialized** - At least one stage has been initialized (`/discovery-init`, `/prototype-init`, etc.)
2. **Python available** - The integrity checker runs as a Python script

## Procedure

### 1. Run the Integrity Checker

```bash
python3 .claude/hooks/integrity_checker.py [options]
```

Options:
- `--quick` - Summary only
- `--section <name>` - Single section (`state`, `traceability`, `artifacts`, `links`, `drift`)
- `--json` - JSON output
- `--fix` - Include remediation instructions

### 2. Parse and Categorize Issues

Issues are categorized by:

**Severity:**
- `ERROR` - Must fix before proceeding
- `WARNING` - Should fix but non-blocking
- `INFO` - Informational only

**Section:**
- `state` - State file issues
- `traceability` - Registry issues
- `artifacts` - Build artifact issues
- `links` - Cross-stage reference issues
- `drift` - Template deviation issues

### 3. Generate Report

The report includes:

1. **Summary Table** - Counts by severity and section
2. **Section Details** - Per-file/per-item status
3. **Recommended Actions** - Prioritized fix instructions

## Validation Logic

### State Files

```
FOR EACH expected state file per stage:
  IF file missing:
    ADD ERROR: "Missing state file"
  ELSE:
    PARSE JSON
    IF invalid JSON:
      ADD ERROR: "Invalid JSON structure"
    IF missing required fields:
      ADD ERROR: "Missing field: {field}"
    IF checkpoint inconsistency:
      ADD WARNING: "Checkpoint mismatch"
```

Expected state files by stage:

| Stage | Files |
|-------|-------|
| Discovery | `discovery_config.json`, `discovery_progress.json` |
| Prototype | `prototype_config.json`, `prototype_progress.json`, `discovery_summary.json` |
| ProductSpecs | `productspecs_config.json`, `productspecs_progress.json` |
| SolArch | `solarch_config.json`, `solarch_progress.json`, `solarch_input_validation.json` |
| Implementation | `implementation_config.json`, `implementation_progress.json`, `implementation_input_validation.json` |

### Traceability Files

```
LOAD _schema_index.json from templates

FOR EACH registry in schema_index:
  IF file missing AND required:
    ADD ERROR: "Missing required registry"
  ELSE IF file exists:
    VALIDATE against schema
    CHECK $documentation block
    COUNT items
```

### Build Artifacts

Per-stage artifact requirements based on checkpoint:

**Discovery:**
- CP0: `00-management/PROGRESS_TRACKER.md`
- CP1: `01-analysis/ANALYSIS_SUMMARY.md`
- CP3: `02-research/personas/*.md`
- CP4: `02-research/JOBS_TO_BE_DONE.md`
- CP5-8: `03-strategy/*.md`
- CP10: `05-documentation/INDEX.md`

**Prototype:**
- CP7: `00-foundation/design-tokens.json`
- CP8: `01-components/component-index.md`
- CP9: `02-screens/screen-index.md`
- CP12: `prototype/src/`

**ProductSpecs:**
- CP4: `01-modules/module-index.md`
- CP5: `02-api/api-index.md`
- CP6: `03-tests/test-case-registry.md`
- CP8: `04-jira/full-hierarchy.csv`

**SolArch:**
- CP3: `04-solution-strategy/solution-strategy.md`
- CP8: `09-decisions/ADR-*.md` (min 9)
- CP11: All traceability validated

**Implementation:**
- CP2: `tasks/TASK_INDEX.md`
- CP5: P0 tasks complete
- CP6: `reports/CODE_REVIEW.md`
- CP9: `reports/VALIDATION_REPORT.md`

### Cross-Stage Links

```
FOR EACH registry with references:
  FOR EACH item.refs:
    LOOKUP target_id in target_registry
    IF not found:
      ADD ERROR: "Broken link: {source_id} → {target_id}"
```

Reference chains validated:
- `PP-X.X` → `JTBD-X.X`
- `JTBD-X.X` → `REQ-XXX`
- `REQ-XXX` → `SCR-XXX`
- `SCR-XXX` → `MOD-XXX`
- `MOD-XXX` → `T-NNN`
- `MOD-XXX` → `ADR-XXX`

### Template Drift

```
FOR EACH file with template in .claude/templates/:
  LOAD template
  COMPARE structure:
    - Missing $documentation fields
    - Missing required fields
    - Schema version mismatch
    - Unexpected fields (INFO only)
```

## Output Formats

### Full Report (default)

ASCII-formatted report with:
- Header box with timestamp and overall status
- Summary table
- Per-section details with icons (✅ ❌ ⚠️ ℹ️)
- Recommended actions with commands

### Quick Report (--quick)

One-line-per-section summary:
```
State Files:       ✅ 5/5 valid
Traceability:      ⚠️ 1 warning
Build Artifacts:   ❌ 2 errors
Cross-Stage Links: ✅ All valid
Template Drift:    ⚠️ 1 drifted
```

### JSON Report (--json)

```json
{
  "timestamp": "2025-12-25T10:30:00Z",
  "overall_status": "ERROR",
  "summary": {
    "errors": 2,
    "warnings": 1,
    "info": 0
  },
  "sections": {
    "state": { "status": "OK", "issues": [] },
    "traceability": { "status": "WARNING", "issues": [...] },
    "artifacts": { "status": "ERROR", "issues": [...] },
    "links": { "status": "OK", "issues": [] },
    "drift": { "status": "OK", "issues": [] }
  },
  "recommended_actions": [...]
}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | Warnings only |
| 2 | Errors found |
| 3 | Critical errors |

## Integration with Commands

This skill is invoked by:
- `/integrity-check` - Direct invocation
- Stage resume commands - Pre-check before resuming

## Remediation Actions

The skill provides specific commands to fix each issue type:

| Issue Type | Fix Command |
|------------|-------------|
| Missing state files | `/traceability-init --repair` |
| Missing registries | `/traceability-init --repair` |
| Missing artifacts | Re-run stage phase command |
| Broken links | Manual correction in registry |
| Template drift | `/traceability-init --repair` or manual update |

## Related

- **Command**: `/integrity-check` - User-facing command
- **Script**: `.claude/hooks/integrity_checker.py` - Implementation
- **Skill**: `Traceability_Guard` - Pre-modification guard
- **Skill**: `Traceability_Initializer` - Backbone creation/repair
- **Templates**: `.claude/templates/` - Source templates
