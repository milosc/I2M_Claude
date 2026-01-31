---
description: Complete Discovery analysis from client materials to specifications
argument-hint: <SystemName> <InputPath>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Task, Glob, Grep
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery ended '{"stage": "discovery"}'
---


# /discovery - Complete Discovery Orchestration

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Validate session (WARNING only - won't block execution)
python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/validate_session.py" --warn-only || true

# 2. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 3. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

**Note**: If you see session validation warnings above, they won't block execution but may result in "pending" or "system" values in traceability logs. Run `/project-init` to fix them.

## Rules Loading (On-Demand)

This command requires Discovery-specific rules. Load them now:

```bash
# Load Discovery rules (includes PDF handling, input processing, output structure)
/rules-discovery

# Load Traceability rules (includes ID formats, source linking)
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Required: `<SystemName> <InputPath>` where:
  - `<SystemName>` - Name of the system being analyzed (e.g., InventorySystem)
  - `<InputPath>` - Path to folder containing raw client materials

## Prerequisites

- Raw client materials exist at `<InputPath>`
- No active discovery session (or use `/discovery-reset` first)
- **Dependencies installed** (run `/htec-libraries-init` if not done)

## Pre-Flight: Dependency Check

**BEFORE starting discovery, check if dependencies are installed:**

```bash
# Quick check - if this fails, run full installation
.venv/bin/python --version 2>/dev/null || echo "NEEDS_INSTALL"
```

**If dependencies are missing, run the installer:**
```bash
python3 .claude/skills/tools/htec_dependencies_installer.py
```

This installs:
- PyPDF2 (PDF chunking)
- Playwright (UI testing)
- All other required packages

See `/htec-libraries-init` for full details.

## Skills Used (All 28 Discovery Skills)

Read these skills BEFORE executing each phase:

**Phase 0 - Init:**
- `.claude/skills/Discovery_Orchestrator/Discovery_Orchestrator.md`

**Phase 1-2 - Analyze & Extract:**
- `.claude/skills/Discovery_ClassifyProject/SKILL.md` - **MANDATORY**: Classifies project type (Full Stack, Backend Only, etc.)
- `.claude/skills/Discovery_AnalyzeDocument/Discovery_AnalyzeDocument.md`
- `.claude/skills/Discovery_AnalyzeSpreadsheet/Discovery_AnalyzeSpreadsheet.md`
- `.claude/skills/Discovery_AnalyzePresentation/Discovery_AnalyzePresentation.md`
- `.claude/skills/Discovery_AnalyzeScreenshot/Discovery_AnalyzeScreenshot.md`
- `.claude/skills/Discovery_AnalyzeAudioVideo/Discovery_AnalyzeAudioVideo.md`
- `.claude/skills/Discovery_AnalyzeData/Discovery_AnalyzeData.md`
- `.claude/skills/Discovery_AnalyzeInterview/Discovery_AnalyzeInterview.md`
- `.claude/skills/Discovery_ExtractPainPoints/Discovery_ExtractPainPoints.md`
- `.claude/skills/Discovery_ExtractUserTypes/Discovery_ExtractUserTypes.md`
- `.claude/skills/Discovery_ExtractWorkflows/Discovery_ExtractWorkflows.md`
- `.claude/skills/Discovery_ExtractQuotes/Discovery_ExtractQuotes.md`
- `.claude/skills/Discovery_ExtractMetrics/Discovery_ExtractMetrics.md`

**Phase 3-4 - Research:**
- `.claude/skills/Discovery_GeneratePersona/Discovery_GeneratePersona.md`
- `.claude/skills/Discovery_GenerateJTBD/Discovery_GenerateJTBD.md`

**Phase 5-8 - Strategy:**
- `.claude/skills/Discovery_GenerateVision/Discovery_GenerateVision.md`
- `.claude/skills/Discovery_GenerateStrategy/Discovery_GenerateStrategy.md`
- `.claude/skills/Discovery_GenerateRoadmap/Discovery_GenerateRoadmap.md`
- `.claude/skills/Discovery_GenerateKPIs/Discovery_GenerateKPIs.md`

**Phase 9 - Design Specs:**
- `.claude/skills/Discovery_SpecScreens/Discovery_SpecScreens.md`
- `.claude/skills/Discovery_SpecNavigation/Discovery_SpecNavigation.md`
- `.claude/skills/Discovery_SpecDataModel/Discovery_SpecDataModel.md`
- `.claude/skills/Discovery_SpecSampleData/Discovery_SpecSampleData.md`
- `.claude/skills/Discovery_SpecComponents/Discovery_SpecComponents.md`
- `.claude/skills/Discovery_SpecInteractions/Discovery_SpecInteractions.md`

**Phase 10 - Documentation:**
- `.claude/skills/Discovery_DocIndex/Discovery_DocIndex.md`
- `.claude/skills/Discovery_DocSummary/Discovery_DocSummary.md`

**Phase 11 - Validation:**
- `.claude/skills/Discovery_Validate/Discovery_Validate.md`

## Execution Steps

### Phase 0: Initialize

0. **Check Dependencies** (FIRST):
   ```bash
   # Check if .venv exists and has required packages
   .venv/bin/python -c "import PyPDF2; import playwright" 2>/dev/null
   ```
   - If check fails → Run: `python3 .claude/skills/tools/htec_dependencies_installer.py`
   - Wait for installation to complete before proceeding
   - Log: "Dependencies installed" or "Dependencies already available"

1. Parse arguments: `<SystemName>` and `<InputPath>`
2. Create shared state folders at project root:
   ```
   _state/
   traceability/
   traceability/feedback_sessions/
   ```
3. Create discovery output folder: `ClientAnalysis_<SystemName>/`
4. Create subfolder structure:
   ```
   ClientAnalysis_<SystemName>/
   ├── 00-management/
   ├── 01-analysis/
   ├── 02-research/
   ├── 03-strategy/
   ├── 04-design-specs/
   └── 05-documentation/
   ```
5. Initialize state files:
   - `_state/pipeline_config.json`
   - `_state/discovery_config.json`
   - `_state/discovery_progress.json`
   - `_state/discovery_context.json`
   - `_state/discovery_materials_inventory.json`
   - `_state/discovery_error_log.md`
7. **Initialize Traceability Memory**:
   ```bash
   python3 .claude/skills/tools/traceability_manager.py init
   ```
8. Update progress: Phase 0 complete

### Phase 1-2: Analyze & Extract

1. Read Discovery_Orchestrator skill for error handling rules
2. List all files in `<InputPath>`
3. Categorize files by type in `discovery_materials_inventory.json`
4. **Classify Project** (MANDATORY):
   - Read `.claude/skills/Discovery_ClassifyProject/SKILL.md`
   - Run `Discovery_ClassifyProject` to determine project type
   - Update `_state/discovery_config.json` with classification
5. For each supported file:
   - Read appropriate Discovery_Analyze* skill
   - Process file, extract content
   - **Run Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-file <Path>`
   - On ANY error: log to `discovery_error_log.md`, skip, continue
5. Run all Discovery_Extract* skills on processed content
6. Generate `ClientAnalysis_<SystemName>/01-analysis/ANALYSIS_SUMMARY.md`
7. **Run Phase Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 1` && `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 2`
8. **Update Visualization**: `python3 .claude/skills/tools/traceability_manager.py visualize`
9. Update progress: Phases 1-2 complete

### Phase 3-4: Research

1. Read Discovery_GeneratePersona skill
2. Generate persona files in `02-research/persona-*.md`
3. **Run Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-file <PersonaPath>`
4. Link personas to user_type_registry
5. Read Discovery_GenerateJTBD skill
6. Generate `02-research/jtbd-jobs-to-be-done.md`
7. **Run Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-file <JTBDPath>`
8. Populate `traceability/jtbd_registry.json`
9. Update `trace_matrix.json` with PP→JTBD links
10. **Run Phase Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 3` && `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 4`
11. **Update Visualization**: `python3 .claude/skills/tools/traceability_manager.py visualize`
12. Update progress: Phases 3-4 complete

### Phase 5-8: Strategy

1. Read Discovery_GenerateVision skill
2. Generate `03-strategy/product-vision.md`
3. Read Discovery_GenerateStrategy skill
4. Generate `03-strategy/product-strategy.md`
5. Read Discovery_GenerateRoadmap skill
6. Generate `03-strategy/product-roadmap.md`
7. Populate `traceability/requirements_registry.json` (features from roadmap)
8. Read Discovery_GenerateKPIs skill
9. Generate `03-strategy/kpis-and-goals.md`
10. Update `trace_matrix.json` with JTBD→Feature links
11. **Run Phase Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint <PHASE_NUM>` for 5, 6, 7, 8
12. **Update Visualization**: `python3 .claude/skills/tools/traceability_manager.py visualize`
13. Update progress: Phases 5-8 complete

### Phase 9: Design Specs

1. Read all Discovery_Spec* skills
2. Generate in `04-design-specs/`:
   - `screen-definitions.md` → update `traceability/screen_registry.json`
   - `navigation-structure.md`
   - `data-fields.md`
   - `sample-data.json`
   - `ui-components.md`
   - `interaction-patterns.md`
3. **Run Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-file <SpecPath>` for all deliverables
4. Update `trace_matrix.json` with Feature→Screen links
5. **Run Phase Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 9`
6. **Update Visualization**: `python3 .claude/skills/tools/traceability_manager.py visualize`
7. Update progress: Phase 9 complete

### Phase 10: Documentation

1. Read Discovery_DocIndex and Discovery_DocSummary skills
2. Generate in `05-documentation/`:
   - `INDEX.md`
   - `README.md`
   - `DOCUMENTATION_SUMMARY.md`
   - `GETTING_STARTED.md`
   - `FILES_CREATED.md`
3. **Update Traceability & Helpers**:
   ```bash
   python3 .claude/skills/tools/traceability_manager.py visualize
   ```
   *This updates all MD visualizations in `traceability/` and all reports in `helperFiles/`.*
4. **Run Phase Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 10`
5. Update progress: Phase 10 complete

### Phase 11: Validation

1. Read Discovery_Validate skill
2. Run all validation checks per skill template
3. **Run Predictability Validator**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 11`
4. Generate `05-documentation/VALIDATION_REPORT.md`
5. Finalize `trace_matrix.json` with coverage statistics
6. Update `discovery_config.json` status to "complete"
7. **Final Check**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 12`
8. Update progress: 100% complete

## 🚨 MANDATORY STATE UPDATES 🚨

**CRITICAL**: You MUST update state files after EACH phase. Failure to do so breaks resume functionality.

### After Phase 0 - Write These Files:

**`_state/discovery_progress.json`** (MANDATORY):
```json
{
  "phases": {
    "0_init": { "status": "complete", "started": "<ISO_TIMESTAMP>", "completed": "<ISO_TIMESTAMP>" },
    "1_analyze": { "status": "pending" },
    "1.5_pdf_analysis": { "status": "pending" },
    "2_extract": { "status": "pending" },
    "3_personas": { "status": "pending" },
    "4_jtbd": { "status": "pending" },
    "5_vision": { "status": "pending" },
    "6_strategy": { "status": "pending" },
    "7_roadmap": { "status": "pending" },
    "8_kpis": { "status": "pending" },
    "9_specs": { "status": "pending" },
    "10_docs": { "status": "pending" },
    "11_validate": { "status": "pending" }
  },
  "overall_progress": 8,
  "last_checkpoint": "discovery-init",
  "resumable_from": "1_analyze"
}
```

**`_state/discovery_config.json`** (MANDATORY):
```json
{
  "system_name": "<SystemName>",
  "input_path": "<InputPath>",
  "output_path": "ClientAnalysis_<SystemName>/",
  "created_at": "<ISO_TIMESTAMP>",
  "updated_at": "<ISO_TIMESTAMP>",
  "status": "in_progress",
  "current_phase": 0,
  "current_checkpoint": "discovery-init"
}
```

### After Each Phase - UPDATE Progress:

**Template for updating `_state/discovery_progress.json`:**
```json
// After Phase 1-2:
"1_analyze": { "status": "complete", "started": "...", "completed": "..." },
"2_extract": { "status": "complete", "started": "...", "completed": "..." },
"overall_progress": 25,
"resumable_from": "3_personas"

// After Phase 3-4:
"3_personas": { "status": "complete", ... },
"4_jtbd": { "status": "complete", ... },
"overall_progress": 40,
"resumable_from": "5_vision"

// After Phase 5-8:
"5_vision": { "status": "complete", ... },
"6_strategy": { "status": "complete", ... },
"7_roadmap": { "status": "complete", ... },
"8_kpis": { "status": "complete", ... },
"overall_progress": 65,
"resumable_from": "9_specs"

// After Phase 9:
"9_specs": { "status": "complete", ... },
"overall_progress": 80,
"resumable_from": "10_docs"

// After Phase 10:
"10_docs": { "status": "complete", ... },
"overall_progress": 90,
"resumable_from": "11_validate"

// After Phase 11:
"11_validate": { "status": "complete", ... },
"overall_progress": 100,
"resumable_from": null
```

### State Update Checklist (Run After EACH Phase)

```
✅ Phase complete? → Update discovery_progress.json with status: "complete"
✅ Set overall_progress percentage
✅ Set resumable_from to next phase
✅ Update discovery_config.json current_phase and current_checkpoint
✅ Verify state file was written (Read it back to confirm)
```

### `_state/` Files Created/Updated:
- `pipeline_config.json` - Created in Phase 0
- `discovery_config.json` - Created in Phase 0, updated throughout
- `discovery_progress.json` - **MUST BE UPDATED after each phase**
- `discovery_context.json` - Updated with session history
- `discovery_materials_inventory.json` - Created in Phase 1
- `discovery_error_log.md` - Updated on any file failures

### `traceability/` Files Created/Updated:
- `trace_matrix.json` - Progressive updates with chain links
- `client_facts_registry.json` - Populated in Phase 1-2
- `pain_point_registry.json` - Populated in Phase 1-2
- `user_type_registry.json` - Populated in Phase 1-2
- `jtbd_registry.json` - Populated in Phase 3-4
- `requirements_registry.json` - Populated in Phase 5-8
- `screen_registry.json` - Populated in Phase 9
- `TRACEABILITY_MATRIX_MASTER.md` - Generated in Phase 10

## Outputs

Complete `ClientAnalysis_<SystemName>/` folder with:
- `00-management/PROGRESS_TRACKER.md`
- `01-analysis/ANALYSIS_SUMMARY.md`
- `02-research/persona-*.md`, `jtbd-jobs-to-be-done.md`
- `03-strategy/product-vision.md`, `product-strategy.md`, `product-roadmap.md`, `kpis-and-goals.md`
- `04-design-specs/screen-definitions.md`, `navigation-structure.md`, `data-fields.md`, `sample-data.json`, `ui-components.md`, `interaction-patterns.md`
- `05-documentation/INDEX.md`, `README.md`, `DOCUMENTATION_SUMMARY.md`, `GETTING_STARTED.md`, `FILES_CREATED.md`, `VALIDATION_REPORT.md`

## Error Handling

## Error Handling

> **STRICT RULE**: Follow the global error handling rules in `.claude/rules/error-handling.md`.

*   **Policy**: ERROR → SKIP → CONTINUE.
*   **Logging**: All skips must be logged to `_state/discovery_error_log.md`.
*   **Completeness**: Finish analysis with whatever files are readable.


## Version Metadata

All generated files include version metadata per VERSION_CONTROL_STANDARD.md:

```yaml
---
document_id: DISC-<TYPE>-<SystemName>
version: 1.0.0
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
generated_by: Discovery_<SkillName>
source_files:
  - <InputPath>/*
change_history:
  - version: "1.0.0"
    date: "<YYYY-MM-DD>"
    author: "Discovery_<SkillName>"
    changes: "Initial generation"
---
```

## Next Command

After `/discovery` completes:
- Use `/discovery-status` to verify completion
- Use `/discovery-trace` to review traceability coverage
- Use `/discovery-export` to package for Prototype stage
- Or proceed directly to `/prototype` command (Stage 2)
