---
name: discovery-export
description: Export Discovery outputs to package for Prototype stage
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-export started '{"stage": "discovery"}'
  Stop:
    - hooks:
        # VALIDATION: Check validation report exists (prerequisite for export)
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/05-documentation"
            --requires "VALIDATION_REPORT.md"
        # VALIDATION: Check screen definitions exist (required for prototype)
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/04-design-specs"
            --requires "screen-definitions.md"
        # VALIDATION: Check data model exists (required for prototype)
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ClientAnalysis_$(cat _state/discovery_config.json 2>/dev/null | grep -o '"system_name"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)/04-design-specs"
            --requires "data-fields.md"
        # VALIDATION: Check export manifest was created
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "_state"
            --requires "discovery_export.json"
        # LOGGING: Record command completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-export ended '{"stage": "discovery", "validated": true}'
---


# /discovery-export - Export Discovery for Prototype Stage

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-export instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

None required - reads from completed discovery session

## Prerequisites

- Discovery complete (status: "complete")
- Validation passed (no critical issues)
- All required files generated

## Skills Used

None - utility command packaging outputs

## Execution Steps

1. **Verify Discovery Complete**
   - Read `_state/discovery_config.json`
   - Check status = "complete"
   - If not complete: Error with suggestion to run `/discovery-validate`

2. **Verify Validation Status**
   - Read `05-documentation/VALIDATION_REPORT.md`
   - Check for 🟢 Pass or 🟡 Pass with Warnings
   - If 🔴 Fail: Error with suggestion to fix issues

3. **Generate Export Summary**
   - Create `_state/discovery_export.json`
   ```json
   {
     "export_id": "export_<timestamp>",
     "source_stage": "discovery",
     "target_stage": "prototype",
     "exported_at": "<ISO_timestamp>",
     "system_name": "<SystemName>",
     "discovery_folder": "ClientAnalysis_<SystemName>/",
     "validation_status": "pass",
     "statistics": {
       "personas": 3,
       "pain_points": { "p0": 5, "p1": 5, "p2": 2 },
       "jtbds": 12,
       "features": 15,
       "screens": 8
     },
     "key_files": {
       "personas": ["02-research/persona-*.md"],
       "jtbd": "02-research/jtbd-jobs-to-be-done.md",
       "roadmap": "03-strategy/product-roadmap.md",
       "screens": "04-design-specs/screen-definitions.md",
       "data_model": "04-design-specs/data-fields.md",
       "sample_data": "04-design-specs/sample-data.json"
     },
     "traceability": {
       "p0_coverage": 100,
       "ready_for_prototype": true
     }
   }
   ```

4. **Update Pipeline Config**
   - Update `_state/pipeline_config.json`
   - Set current_stage to "prototype"
   - Record discovery completion

5. **Generate Export Report**
   ```
   ╔════════════════════════════════════════════════════════════╗
   ║              DISCOVERY EXPORT COMPLETE                      ║
   ╠════════════════════════════════════════════════════════════╣
   ║ System:        <SystemName>                                 ║
   ║ Export Time:   2025-01-15 14:30                             ║
   ║ Target Stage:  Prototype                                    ║
   ╚════════════════════════════════════════════════════════════╝

   EXPORT SUMMARY
   ────────────────────────────────────────────────────────────

   Discovery Outputs:
   ✅ ClientAnalysis_<SystemName>/      (complete)
   ✅ traceability/                     (populated)
   ✅ _state/discovery_*.json           (finalized)

   Key Artifacts for Prototype:
   ────────────────────────────────────────────────────────────

   | Artifact | Path | Status |
   |----------|------|--------|
   | Personas | 02-research/persona-*.md | ✅ Ready |
   | JTBD | 02-research/jtbd-*.md | ✅ Ready |
   | Roadmap | 03-strategy/product-roadmap.md | ✅ Ready |
   | Screens | 04-design-specs/screen-definitions.md | ✅ Ready |
   | Data Model | 04-design-specs/data-fields.md | ✅ Ready |
   | Sample Data | 04-design-specs/sample-data.json | ✅ Ready |

   Traceability Status:
   ────────────────────────────────────────────────────────────

   • Pain Points: 12 (P0: 5, P1: 5, P2: 2)
   • P0 → Screen Coverage: 100%
   • Ready for Prototype: ✅ Yes

   PROTOTYPE STAGE PREREQUISITES MET
   ────────────────────────────────────────────────────────────

   ✅ Screen definitions available
   ✅ Data model specified
   ✅ Sample data provided
   ✅ Navigation structure defined
   ✅ Component specs available
   ✅ Interaction patterns documented

   NEXT STEPS
   ────────────────────────────────────────────────────────────

   To start Prototype stage, run:

   /prototype <SystemName>

   Or use individual prototype commands:
   • /prototype-init
   • /prototype-requirements
   • /prototype-screens
   etc.
   ```

6. **Create Prototype Input Summary**
   - Create `_state/prototype_input_summary.md`
   - Summary of discovery outputs for prototype consumption
   - Key files and their purposes
   - Data model summary
   - Screen inventory

## Export Contents

| Category | Files | Purpose for Prototype |
|----------|-------|----------------------|
| Personas | persona-*.md | User context |
| JTBD | jtbd-*.md | Requirements source |
| Roadmap | product-roadmap.md | Feature scope |
| Screens | screen-definitions.md | UI implementation |
| Navigation | navigation-structure.md | Routing |
| Data Model | data-fields.md | Schema design |
| Sample Data | sample-data.json | Test data |
| Components | ui-components.md | Component library |
| Interactions | interaction-patterns.md | UX implementation |

## Validation Gates

Export requires:
- [ ] Discovery status = "complete"
- [ ] Validation status = 🟢 or 🟡
- [ ] P0 traceability = 100%
- [ ] All Phase 1 screens defined
- [ ] Data model complete
- [ ] Sample data valid

## State Updates

### Created/Updated in `_state/`:
- `discovery_export.json` - Export manifest
- `prototype_input_summary.md` - Prototype input guide
- `pipeline_config.json` - Stage updated to "prototype"

## Outputs

- Export summary displayed
- Export manifest created
- Pipeline config updated
- Ready for `/prototype` command

## Next Command

After export:
- Run `/prototype <SystemName>` for full prototype generation
- Or run `/prototype-init` to initialize prototype stage
- Use `/prototype-validate-discovery` to verify inputs
