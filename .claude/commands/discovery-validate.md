---
name: discovery-validate
description: Validate Discovery checkpoint requirements and quality gates
argument-hint: --checkpoint <N>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-validate started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-validate ended '{"stage": "discovery"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-validate instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

None required - reads configuration from `_state/discovery_config.json`

## Prerequisites

- `/discovery-docs-all` completed (phase 10 complete)
- `_state/discovery_progress.json` shows phase 10 complete
- All documentation folders populated (00-management through 05-documentation)
- `traceability/trace_matrix.json` populated

## Skills Used

- `.claude/skills/Discovery_Validate/Discovery_Validate.md` - CRITICAL: Read entire skill before executing

## Execution Steps

### Phase 11: Validation

1. **Load Prerequisites**
   - Read `_state/discovery_config.json` for output_path and system_name
   - Read `traceability/trace_matrix.json` for chains
   - Read all traceability registries

2. **Update Progress**
   - Set phase `11_validate` status to "in_progress"

3. **Read Discovery_Validate Skill**
   - Understand all validation categories
   - Review pass/fail criteria

### 11.1: File Completeness Checks

4. **Verify Required Files Exist**
   Check for each required file per skill specification:

   | File | Location | Status |
   |------|----------|--------|
   | PROGRESS_TRACKER.md | 00-management/ | ✅/❌ |
   | ANALYSIS_SUMMARY.md | 01-analysis/ | ✅/❌ |
   | persona-*.md (3+ files) | 02-research/ | ✅/❌ |
   | jtbd-jobs-to-be-done.md | 02-research/ | ✅/❌ |
   | product-vision.md | 03-strategy/ | ✅/❌ |
   | product-strategy.md | 03-strategy/ | ✅/❌ |
   | product-roadmap.md | 03-strategy/ | ✅/❌ |
   | kpis-and-goals.md | 03-strategy/ | ✅/❌ |
   | screen-definitions.md | 04-design-specs/ | ✅/❌ |
   | navigation-structure.md | 04-design-specs/ | ✅/❌ |
   | data-fields.md | 04-design-specs/ | ✅/❌ |
   | sample-data.json | 04-design-specs/ | ✅/❌ |
   | ui-components.md | 04-design-specs/ | ✅/❌ |
   | interaction-patterns.md | 04-design-specs/ | ✅/❌ |
   | INDEX.md | 05-documentation/ | ✅/❌ |
   | README.md | 05-documentation/ | ✅/❌ |
   | DOCUMENTATION_SUMMARY.md | 05-documentation/ | ✅/❌ |
   | GETTING_STARTED.md | 05-documentation/ | ✅/❌ |
   | FILES_CREATED.md | 05-documentation/ | ✅/❌ |

### 11.2: Content Completeness Checks

5. **Verify Required Sections in Each Document**
   - Persona files: Overview, Goals, Pain Points, Workflow, Design Implications
   - JTBD file: Feature areas, JTBD format, Priority, Persona mapping
   - Vision: Statement, Pain points, Capabilities
   - Strategy: Pillars, Go-to-market
   - Roadmap: Phases, Epics
   - KPIs: North Star, Category KPIs
   - Screen definitions: Inventory, Layouts
   - Data fields: Entities, Field types
   - Sample data: Valid JSON, Matches schema

### 11.3: Consistency Checks

6. **Verify Naming Consistency**
   - Persona names match across all documents
   - Pain point IDs (PP-X.Y) match registry
   - Feature names match roadmap
   - JTBD IDs (JTBD-X.Y) match registry
   - Screen IDs (S-X.Y) match registry

### 11.4: Traceability Checks

7. **Verify Complete Traceability Chains**
   For each P0 pain point:
   - Traced to at least one JTBD ✅/❌
   - Traced to Vision capabilities ✅/❌
   - Traced to Roadmap features ✅/❌
   - Traced to Screen definitions ✅/❌

   Calculate coverage:
   ```
   P0 Coverage = (P0 pain points traced to screens) / (Total P0 pain points) × 100%
   ```

### 11.5: Cross-Reference Checks

8. **Validate All Internal Links**
   - Scan all markdown files for links
   - Verify each link target exists
   - Report invalid links

### 11.6: Prototype Readiness Checks

9. **Verify Prototype Requirements**
   - All Phase 1 screens defined ✅/❌
   - Data model matches sample data ✅/❌
   - Navigation covers all critical flows ✅/❌
   - Components defined for all screens ✅/❌

### Generate Validation Report

10. **Create VALIDATION_REPORT.md**
    - Create `05-documentation/VALIDATION_REPORT.md`
    - Include version metadata:
      ```yaml
      ---
      document_id: DISC-VALIDATION-<SystemName>
      version: 1.0.0
      created_at: <YYYY-MM-DD>
      updated_at: <YYYY-MM-DD>
      generated_by: Discovery_Validate
      source_files:
        - ClientAnalysis_<SystemName>/**/*
        - traceability/**/*
      ---
      ```
    - Follow Discovery_Validate template structure
    - Include all check results
    - Determine overall status:
      - 🟢 Pass: 0 critical issues, ≤5 warnings
      - 🟡 Pass with Warnings: 0 critical issues, >5 warnings
      - 🔴 Fail: ≥1 critical issue

### Finalize Discovery

11. **Update Trace Matrix**
    - Finalize `traceability/trace_matrix.json`
    - Add final coverage statistics
    - Mark stage_completed as "discovery"

12. **Update Discovery Config**
    - Set `discovery_config.json` status to "complete"
    - Update timestamps

13. **Update Progress**
    - Set phase `11_validate` to "complete"
    - Set overall_progress to 100
    - Clear resumable_from

14. **Update Context Memory**
    - Final session entry in `discovery_context.json`
    - Record validation results
    - Set resumption_context for next stage

## State Updates

### Updated in `_state/`:
- `discovery_config.json` - status: "complete", updated_at
- `discovery_progress.json` - phase 11 complete, overall_progress: 100
- `discovery_context.json` - final session, validation results

### Updated in `traceability/`:
- `trace_matrix.json` - final coverage stats, stage_completed: "discovery"

## Outputs

- `ClientAnalysis_<SystemName>/05-documentation/VALIDATION_REPORT.md`
- Updated state files with completion status

## Pass/Fail Criteria

| Status | Criteria |
|--------|----------|
| 🟢 Pass | 0 critical issues, ≤5 warnings |
| 🟡 Pass with Warnings | 0 critical issues, >5 warnings |
| 🔴 Fail | ≥1 critical issue |

### Critical Issues (Must Fix):
- Missing required file
- Broken cross-reference
- P0 pain point not traced to screen
- Invalid JSON in sample-data.json

### Warnings (Should Fix):
- Missing section in document
- Inconsistent naming
- P1 pain point not traced

### Step 15: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
- If 🔴 Fail: Fix critical issues and re-run `/discovery-validate`
- Proceed to `/prototype` command (Stage 2) when ready
