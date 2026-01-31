---
description: Analyze raw client materials and generate discovery documentation
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-analyze started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-analyze ended '{"stage": "discovery"}'
---


# /discovery-analyze - Analyze Materials & Extract Insights

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-analyze instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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

- `/discovery-init` completed (state files exist)
- `_state/discovery_config.json` exists with valid `input_path`
- `_state/discovery_materials_inventory.json` exists

## Skills Used

**Analysis Skills** (Phase 1):
- `.claude/skills/Discovery_ClassifyProject/SKILL.md` - **MANDATORY**: Classifies project type (Full Stack, Backend Only, etc.)
- `.claude/skills/Discovery_AnalyzeDocument/Discovery_AnalyzeDocument.md` - **includes PDF chunking logic**
- `.claude/skills/Discovery_AnalyzeSpreadsheet/Discovery_AnalyzeSpreadsheet.md`
- `.claude/skills/Discovery_AnalyzePresentation/Discovery_AnalyzePresentation.md`
- `.claude/skills/Discovery_AnalyzeScreenshot/Discovery_AnalyzeScreenshot.md`
- `.claude/skills/Discovery_AnalyzeAudioVideo/Discovery_AnalyzeAudioVideo.md`
- `.claude/skills/Discovery_AnalyzeData/Discovery_AnalyzeData.md`
- `.claude/skills/Discovery_AnalyzeInterview/Discovery_AnalyzeInterview.md`

**Deep PDF Analysis** (Phase 1.5 - NEW):
- `.claude/skills/Discovery_AnalyzePDF/Discovery_AnalyzePDF.md` - Deep extraction of system knowledge, terminology, gap analysis

**PDF Tools**:
- `.claude/skills/tools/pdf_splitter.py` - Splits large PDFs and converts to Markdown (use `automd` command)

**Audio Tools**:
- `.claude/skills/tools/audio_transcriber.py` - Transcribes audio/video files to Markdown with timestamps

**Client Facts Extraction** (Phase 1 - during analysis):
- `.claude/skills/Discovery_ExtractClientFacts/SKILL.md` - **MANDATORY**: Extracts quotes, metrics, requirements, constraints with source traceability

**Extraction Skills** (Phase 2):
- `.claude/skills/Discovery_ExtractPainPoints/Discovery_ExtractPainPoints.md`
- `.claude/skills/Discovery_ExtractUserTypes/Discovery_ExtractUserTypes.md`
- `.claude/skills/Discovery_ExtractWorkflows/Discovery_ExtractWorkflows.md`
- `.claude/skills/Discovery_ExtractQuotes/Discovery_ExtractQuotes.md`
- `.claude/skills/Discovery_ExtractMetrics/Discovery_ExtractMetrics.md`

**Error Handling**:
- `.claude/skills/Discovery_Orchestrator/Discovery_Orchestrator.md` - CRITICAL: Read error handling and PDF chunking sections

## Execution Steps

### Phase 1: Analyze Materials

1. **Read Discovery_Orchestrator** for error handling rules:
   ```
   FILE FAILS → SKIP IT → NEXT FILE → CONTINUE
   ```

2. **Load Configuration**
   - Read `_state/discovery_config.json` for input_path
   - Read `_state/discovery_materials_inventory.json` for file list

3. **Update Progress**
   - Set phase `1_analyze` status to "in_progress"
   - Update `discovery_config.json` current_checkpoint to "discovery-analyze"

3.5. **Determine Material Priority** (When conflicts detected)

   When multiple source types contain conflicting information:

   ```
   USE AskUserQuestion:
     question: "Which materials should take precedence for conflicting information?"
     header: "Priority"
     options:
       - label: "Interviews (Recommended)"
         description: "Direct user quotes take precedence"
       - label: "Documents"
         description: "Written specs/requirements take precedence"
       - label: "Screenshots"
         description: "Visual designs take precedence"

   STORE selected priority in _state/discovery_config.json:
     {
       "material_priority": "{selected_option}",
       "material_priority_rationale": "{option_description}"
     }
   ```

4. **Verify Project Classification** (MANDATORY)
   - Read `_state/discovery_config.json`
   - Check if `project_classification` field exists and is populated
   - **IF MISSING**:
     - Read `.claude/skills/Discovery_ClassifyProject/SKILL.md`
     - Run `Discovery_ClassifyProject` to analyze materials and determine project type
     - This will update `_state/discovery_config.json` with type (FULL_STACK, BACKEND_ONLY, etc.)
     - **CONTINUE** only after classification is set

5. **Process Each File**
   For each file in inventory:

   a. **Pre-check**: Skip immediately if unsupported type:
      - Video URLs (youtube.com, vimeo.com)
      - Log: `⛔ SKIPPED: [filename] - Unsupported media type`

   b. **Audio/Video Special Handling** (MANDATORY for .mp3, .wav, .m4a, .mp4, .mov, .avi, .webm, .mkv):

      ⚠️ **CRITICAL**: Transcribe audio/video content before analysis!

      ```
      STEP 1: TRANSCRIBE AUDIO
      ════════════════════════
      .venv/bin/python .claude/skills/tools/audio_transcriber.py <file> [INPUT_PATH]/_transcripts/

      → Creates Markdown file: [filename]_transcript.md
      
      STEP 2: READ TRANSCRIPT
      ═══════════════════════
      Read(<transcript.md>)     ← Read the generated transcript
      ```

   c. **PDF Special Handling** (MANDATORY for ALL .pdf files - NO EXCEPTIONS):

      ⚠️ **CRITICAL**: NEVER call Read() on a large PDF without converting to Markdown first!
      This is the #1 cause of "PDF too large" errors.

      ```
      STEP 1: CHECK PAGE COUNT (REQUIRED)
      ════════════════════════════════════
      .venv/bin/python .claude/skills/tools/pdf_splitter.py count <file.pdf>
      → This outputs: "📄 filename.pdf: X pages"
      → Store the page count before proceeding

      STEP 2: BRANCH BASED ON PAGE COUNT
      ═══════════════════════════════════
      IF pages ≤ 30:
          → Read(<file.pdf>) directly with Read() tool
          → Process content

      IF pages > 30:
          → DO NOT attempt Read() on original file (it WILL fail!)
          → Proceed to STEP 3

      STEP 3: CONVERT TO MARKDOWN (when pages > 30)
      ══════════════════════════════════════════════
      NOTE: Store in client materials folder for REUSE across discovery runs!

      .venv/bin/python .claude/skills/tools/pdf_splitter.py automd <file.pdf> [INPUT_PATH]/_pdf_markdown/[pdf_name]/

      → Creates Markdown files: {basename}_{start}_{end}.md
      → Example: manual_1_30.md, manual_31_60.md, manual_61_72.md

      STEP 4: READ MARKDOWN FILES SEQUENTIALLY
      ════════════════════════════════════════
      FOR EACH .md file in [INPUT_PATH]/_pdf_markdown/[pdf_name]/:
          Read(<chunk.md>)     ← Read Markdown files, NOT PDFs
          Extract insights
      END FOR

      STEP 5: COMBINE INSIGHTS FROM ALL MARKDOWN FILES
      ═════════════════════════════════════════════════
      Merge all extracted content into single analysis

      Note: Requires PyPDF2 and MarkItDown in .venv. Setup via /htec-libraries-init
      ```

   d. **Select Appropriate Skill**:
      - `.txt`, `.md`, `.rtf` → Discovery_AnalyzeDocument
      - `.docx` → Discovery_AnalyzeDocument
      - `.pdf` → Discovery_AnalyzeDocument (with Markdown conversion per step c)
      - `.xlsx`, `.csv` → Discovery_AnalyzeSpreadsheet
      - `.pptx` → Discovery_AnalyzePresentation
      - `.png`, `.jpg`, `.jpeg` → Discovery_AnalyzeScreenshot
      - `.mp3`, `.wav`, `.m4a` → Discovery_AnalyzeAudioVideo (Transcribe first)
      - `.mp4`, `.mov`, `.avi` → Discovery_AnalyzeAudioVideo (Transcribe first)
      - `.json`, `.xml`, `.yaml` → Discovery_AnalyzeData
      - `.mp3`, `.wav`, `.mp4`, etc. → Discovery_AnalyzeInterview (via transcript)
      - Interview transcripts → Discovery_AnalyzeInterview

   e. **Read File Once** (or each .md file once for large PDFs/Audio):
      - Success → Extract content, add to analysis
      - Failure → Log to `_state/discovery_error_log.md`, continue to next file

   e. **Update Inventory**:
      - Set processing_status to "processed", "markdown:<N>", or "skipped:<reason>"

5. **Extract Client Facts** (MANDATORY - Read `.claude/skills/Discovery_ExtractClientFacts/SKILL.md`)

   During/after processing each file, extract client facts:

   a. **Read the skill**: `.claude/skills/Discovery_ExtractClientFacts/SKILL.md`

   b. **Initialize registry** (if not exists):
      ```json
      {
        "schema_version": "1.0.0",
        "stage": "Discovery",
        "checkpoint": 1,
        "system_name": "{SystemName}",
        "created_at": "YYYY-MM-DD",
        "source_files": [],
        "facts": [],
        "summary": {}
      }
      ```

   c. **For each file processed**, extract:
      | Type | What to Extract | ID Format |
      |------|-----------------|-----------|
      | `quote` | Direct stakeholder statements | CF-Q-NNN |
      | `metric` | Quantitative data (numbers, %, time, $) | CF-M-NNN |
      | `requirement` | Explicit needs (must, shall, should) | CF-R-NNN |
      | `constraint` | Limitations (cannot, must not, blocked) | CF-C-NNN |
      | `observation` | Observed behaviors/patterns | CF-O-NNN |

   d. **Each fact MUST have**:
      - `source_id`: Reference to source file (SRC-NNN)
      - `source_file`: Path to original file
      - `stakeholder`: Role of person who stated it
      - `content`: The actual fact text
      - `category`: pain_point, baseline, goal, constraint, or workflow
      - `confidence`: high, medium, or low

   e. **Write to ROOT traceability folder**:
      - Path: `traceability/client_facts_registry.json`
      - Minimum: ≥5 facts from available materials

   f. **Quality Gate**:
      ```bash
      python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 1 --dir ClientAnalysis_X/
      # Validates client_facts_registry.json has content
      ```

### Phase 1.5: Deep PDF Analysis (NEW)

6. **For Each PDF Processed in Phase 1**
   - Read `.claude/skills/Discovery_AnalyzePDF/Discovery_AnalyzePDF.md`
   - Determine if PDF qualifies for deep analysis:
     - Technical manual, user guide, or reference document: YES
     - PDF has >10 pages: YES
     - Simple form or single-page document: SKIP

7. **Create PDF Analysis Folder**
   - Create `ClientAnalysis_<SystemName>/01-analysis/[PDF_Name]_Analysis/`
   - Sanitize folder name (remove spaces, special chars)
   - Example: `115wmsug.pdf` → `115wmsug_Analysis/`

8. **Generate 4 Analysis Documents Per PDF**
   - `SYSTEM_KNOWLEDGE.md` - Architecture, concepts, capabilities
     - Core system components
     - Key concepts and entities
     - Processing rules and business logic
     - Data flow and transaction types
     - Integration points
   - `TERMINOLOGY.md` - Domain terms and definitions
     - Acronyms and abbreviations
     - Domain-specific terms
     - System-specific concepts
   - `GAP_ANALYSIS.md` - System capabilities vs user needs
     - Map pain points (PP-X.Y) to system capabilities
     - Identify gaps and constraints
     - Priority matrix (P0, P1, P2)
   - `SECTION_INDEX.md` - PDF sections with page ranges
     - Document structure
     - Key topics by section
     - Quick reference table

9. **Generate Consolidated PDF Outputs**
   - Create `ClientAnalysis_<SystemName>/01-analysis/PDF_ANALYSIS_INDEX.md`
     - List all analyzed PDFs with links to folders
     - Summary of key topics per PDF
   - Create `ClientAnalysis_<SystemName>/01-analysis/PDF_FINDINGS_SUMMARY.md`
     - Consolidated system knowledge
     - Master terminology list (top 20 terms)
     - Gap analysis summary across all PDFs
     - Recommendations

### Phase 2: Extract Insights

10. **Extract Pain Points**
    - Read Discovery_ExtractPainPoints skill
    - Categorize by severity (P0, P1, P2)
    - Assign hierarchical IDs: PP-1.1, PP-1.2, PP-2.1...
    - Populate `traceability/pain_point_registry.json`
    - Link to source client facts (CF-X.Y)
    - **Cross-reference with PDF GAP_ANALYSIS.md** for validation

11. **Extract User Types**
    - Read Discovery_ExtractUserTypes skill
    - Assign hierarchical IDs: UT-1.1, UT-1.2...
    - Populate `traceability/user_type_registry.json`
    - Link to relevant pain points

12. **Extract Workflows**
    - Read Discovery_ExtractWorkflows skill
    - Document current-state workflows
    - Identify bottlenecks and pain points
    - **Reference PDF SYSTEM_KNOWLEDGE.md** for system workflow details

13. **Extract Quotes**
    - Read Discovery_ExtractQuotes skill
    - Tag with source and user type
    - Link to pain points and client facts

14. **Extract Metrics**
    - Read Discovery_ExtractMetrics skill
    - Quantify pain point impacts
    - Document business metrics mentioned

15. **Generate Analysis Summary**
    - Create `ClientAnalysis_<SystemName>/01-analysis/ANALYSIS_SUMMARY.md`
    - Include version metadata
    - Summarize all extracted insights
    - Reference traceability registries
    - **Include links to PDF analysis folders and consolidated findings**

16. **Update Trace Matrix**
    - Update `traceability/trace_matrix.json` with initial chains
    - Link CF → PP → UT relationships

17. **Update Progress**
    - Set phases `1_analyze`, `1.5_pdf_analysis`, and `2_extract` to "complete"
    - Update overall_progress
    - Set resumable_from to "3_personas"

## State Updates

### Updated in `_state/`:
- `discovery_config.json` - current_phase, current_checkpoint, updated_at, **project_classification**
- `discovery_progress.json` - phases 1-2 complete, overall_progress
- `discovery_materials_inventory.json` - processing_status for each file
- `discovery_error_log.md` - any skipped files
- `discovery_context.json` - session history, key decisions

### Updated in `traceability/`:
- `client_facts_registry.json` - populated with CF-X.Y items
- `pain_point_registry.json` - populated with PP-X.Y items
- `user_type_registry.json` - populated with UT-X.Y items
- `trace_matrix.json` - initial chains with CF→PP→UT links

## Outputs

**Phase 1 Output:**
- Client facts extracted and registered

**Phase 1.5 Outputs (NEW):**
- `ClientAnalysis_<SystemName>/01-analysis/[PDF_Name]_Analysis/` - One folder per PDF
  - `SYSTEM_KNOWLEDGE.md` - Architecture, concepts, capabilities
  - `TERMINOLOGY.md` - Domain terms and definitions
  - `GAP_ANALYSIS.md` - System capabilities vs user needs
  - `SECTION_INDEX.md` - PDF sections with page ranges
- `ClientAnalysis_<SystemName>/01-analysis/PDF_ANALYSIS_INDEX.md` - Master index
- `ClientAnalysis_<SystemName>/01-analysis/PDF_FINDINGS_SUMMARY.md` - Consolidated findings

**Phase 2 Outputs:**
- `ClientAnalysis_<SystemName>/01-analysis/ANALYSIS_SUMMARY.md`
- Populated traceability registries

## Error Handling

> **STRICT RULE**: Follow the global error handling rules in `.claude/rules/error-handling.md`.

*   **PDF Conversion**: Only automated retry via `automd` (splits + converts to Markdown).
*   **General Errors**: Log to `_state/discovery_error_log.md` and SKIP.


## Next Command

After `/discovery-analyze`:
- Run `/discovery-research` to generate personas and JTBD
- Or use `/discovery-status` to check progress
