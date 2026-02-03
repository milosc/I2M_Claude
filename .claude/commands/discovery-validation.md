---
name: discovery-validation
description: Generate validation rules from discovery specifications
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-validation started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-validation ended '{"stage": "discovery"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-validation instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- All previous phases complete
- All documentation folders populated

## Skills Used

- `.claude/skills/Discovery_Validate/Discovery_Validate.md` - CRITICAL: Read entire skill

## Execution Steps

This command is an alias for `/discovery-validate`. It runs validation and generates the report.

1. **Load State**
   - Read `_state/discovery_config.json`
   - Read all traceability registries
   - Inventory all generated files

2. **Read Discovery_Validate Skill**
   - Review all validation categories
   - Understand pass/fail criteria

3. **Run Validation Checks**

   ### File Completeness
   - All required files exist
   - Files have content (not empty)

   ### Content Completeness
   - Required sections present in each document
   - Version metadata included

   ### Consistency
   - IDs match across documents
   - Names consistent across references

   ### Traceability
   - P0 pain points traced to screens
   - All chains complete

   ### Cross-References
   - Internal links valid
   - File references exist

   ### Prototype Readiness
   - Phase 1 screens defined
   - Data model complete
   - Sample data valid JSON

4. **Generate Validation Report**
   - Create `05-documentation/VALIDATION_REPORT.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-VALIDATION-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_Validate
     ---
     ```

5. **Content Structure**
   Follow the full template from Discovery_Validate skill:
   - Validation Summary table
   - File Completeness section
   - Content Completeness section
   - Consistency Checks section
   - Traceability Matrix section
   - Cross-Reference Validation section
   - Prototype Readiness section
   - Issues Found section
   - Statistics Summary
   - Validation Conclusion

6. **Determine Overall Status**
   - 🟢 Pass: 0 critical issues, ≤5 warnings
   - 🟡 Pass with Warnings: 0 critical issues, >5 warnings
   - 🔴 Fail: ≥1 critical issue

7. **Update State**
   - Update `discovery_config.json` status
   - Update `discovery_progress.json` to 100% if passing
   - Finalize `trace_matrix.json` with coverage stats

## Pass/Fail Criteria

### Critical Issues (Cause Failure)
- Missing required file
- P0 pain point not traced to screen
- Invalid sample-data.json
- Broken critical cross-reference

### Warnings (Don't Cause Failure)
- Missing optional section
- P1/P2 pain point not traced
- Inconsistent naming (non-critical)
- Minor cross-reference issues

### Notes (Informational)
- Suggestions for improvement
- Minor formatting issues
- Optional enhancements

## Output Summary

```markdown
## Overall Status: 🟢 Pass

| Category | Status | Score |
|----------|--------|-------|
| File Completeness | 🟢 | 20/20 |
| Content Completeness | 🟢 | 45/47 |
| Consistency | 🟢 | 15/15 |
| Traceability | 🟢 | 100% P0 |
| Cross-References | 🟢 | 0 invalid |
| Prototype Ready | 🟢 | Ready |

**Recommendation**: Ready for Implementation
```

## Outputs

- `ClientAnalysis_<SystemName>/05-documentation/VALIDATION_REPORT.md`
- Updated `_state/discovery_config.json` (status: complete)
- Updated `_state/discovery_progress.json` (100%)
- Updated `traceability/trace_matrix.json` (final coverage)

### Step 8: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
- If 🔴 Fail: Fix critical issues and re-run validation
- Proceed to `/prototype` command when ready
