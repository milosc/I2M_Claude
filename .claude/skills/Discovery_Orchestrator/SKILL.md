---
name: discovery-orchestrator
description: Use when you need to coordinate the complete transformation of raw client materials into a structured product discovery package.
model: sonnet
allowed-tools: Read, Write, Edit, Bash, Task
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill discovery-orchestrator started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill discovery-orchestrator ended '{"stage": "discovery"}'
---

# Discovery Orchestrator

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill discovery-orchestrator instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_Orchestrator
- **Version**: 7.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-27
- **Change History**:
  - v7.1.0 (2025-12-27): **BUGFIX** - Fixed sub-agent file persistence issue:
    - Removed `run_in_background: true` from validators (files weren't persisting)
    - Added explicit "FILE WRITING REQUIREMENT" to all agent prompts requiring Write tool usage
    - Added file verification step after `await Promise.all()` to catch write failures
    - Agents now return structured JSON with `files_written` and `files_failed` arrays
  - v7.0.0 (2025-12-27): **MAJOR** - Added parallel agent execution support with 8 specialized Discovery agents.
  - v6.1.0 (2025-12-23): Added mandatory ROOT-level registry propagation for client_facts, pain_points, user_types, jtbd, and screens.
  - v6.0.0 (2025-12-21): Major update: Enforced file naming conventions, separate persona files, UPPERCASE strategy docs.
  - v5.0.0 (2025-12-21): Added Discovery_AnalyzePDF skill for deep PDF analysis.
  - v4.0.0 (2025-12-21): Added automatic PDF chunking for large PDFs (>30 pages).
  - v3.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md.

## Description
Master coordinator for the Discovery Skills Framework. Orchestrates the complete transformation of raw client materials into structured product documentation.

**Role**: You are the Discovery Orchestrator - a senior product discovery specialist who coordinates multiple specialized analysts (skills) to transform raw client research into actionable product documentation.

**PDF HANDLING**: PDFs with >10 pages are automatically split into 20-page chunks and converted to Markdown using the pdf_splitter.py tool.

---

## 🚨🚨🚨 CRITICAL: ERROR HANDLING 🚨🚨🚨

> **ABSOLUTE RULE**: You MUST follow the global error handling rules in `.claude/rules/error-handling.md`.
>
> 1. **SKIP AND CONTINUE**: If a file fails, log it and move to the next.
> 2. **NEVER LOOP**: One attempt per file. Never retry. Never ask user.
> 3. **NEVER INSTALL**: Do not change the environment.

---

## Trigger Conditions

- User requests "complete discovery analysis" or "full analysis"
- User provides a folder of client materials for analysis
- User mentions "run discovery", "analyze client materials", "product discovery"

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| PATH_TO_CLIENT_MATERIALS | Yes | Folder containing discovery materials |
| PATH_TO_OUTPUT | Yes | Root folder for all outputs |
| CHECKPOINT | No | Resume from checkpoint (0-11, default: 0) |

---

## 🚨🚨🚨 CRITICAL: PDF MARKDOWN CONVERSION (MANDATORY) 🚨🚨🚨

### ⚠️ THE #1 CAUSE OF "PDF TOO LARGE" ERRORS AND HIGH CONTEXT USAGE

**NEVER attempt to Read() a PDF file without first checking its page count.**

```
WRONG (causes "PDF too large" error or high context usage):
    Read("/path/to/manual.pdf")  ← NEVER DO THIS DIRECTLY

CORRECT:
    1. .venv/bin/python .claude/skills/tools/pdf_splitter.py count manual.pdf
    2. If ≤10 pages: Read(manual.pdf)
    3. If >10 pages: Convert to Markdown first using automd, then read .md files
```

### The 10-Page Rule

| PDF Pages | Action |
|-----------|--------|
| ≤10 pages | Read directly with `Read()` tool |
| >10 pages | **MUST convert to Markdown using `automd`, then read .md files** |

### PDF Processing Flow (MANDATORY - NO SHORTCUTS)

```
FOR EACH .pdf file:

    ╔══════════════════════════════════════════════════════════════════╗
    ║ STEP 1: CHECK PAGE COUNT FIRST (REQUIRED - NO EXCEPTIONS)        ║
    ╚══════════════════════════════════════════════════════════════════╝
    Run: .venv/bin/python .claude/skills/tools/pdf_splitter.py count <file.pdf>

    This will output: "📄 filename.pdf: X pages"
    Store the page count. DO NOT SKIP THIS STEP.

    ╔══════════════════════════════════════════════════════════════════╗
    ║ STEP 2: BRANCH BASED ON PAGE COUNT                               ║
    ╚══════════════════════════════════════════════════════════════════╝
    IF pages ≤ 10:
        → Read(<file.pdf>) directly
        → Process content
        → Done with this file

    IF pages > 10:
        → DO NOT attempt Read() on original file (it WILL fail or use too much context!)
        → Proceed to STEP 3

    ╔══════════════════════════════════════════════════════════════════╗
    ║ STEP 3: CONVERT TO MARKDOWN (when pages > 10)                    ║
    ╚══════════════════════════════════════════════════════════════════╝
    Create markdown directory: [INPUT_PATH]/_pdf_markdown/[pdf_basename]/

    NOTE: Store in client materials folder for REUSE across discovery runs!

    Run: .venv/bin/python .claude/skills/tools/pdf_splitter.py automd <file.pdf> [INPUT_PATH]/_pdf_markdown/[pdf_basename]/

    This splits into 20-page chunks AND converts to Markdown:
    Example: manual_1_20.md, manual_21_40.md, manual_41_60.md, manual_61_72.md

    ╔══════════════════════════════════════════════════════════════════╗
    ║ STEP 4: READ EACH MARKDOWN FILE SEQUENTIALLY                     ║
    ╚══════════════════════════════════════════════════════════════════╝
    FOR EACH .md file in [INPUT_PATH]/_pdf_markdown/[pdf_basename]/:
        Read(<chunk.md>)          ← Read Markdown files, NOT PDFs
        extract_insights(chunk)
    END FOR

    ╔══════════════════════════════════════════════════════════════════╗
    ║ STEP 5: COMBINE INSIGHTS FROM ALL CHUNKS                         ║
    ╚══════════════════════════════════════════════════════════════════╝
    Merge extracted content from all markdown files into single analysis

    ON ANY ERROR: log skip, continue to next file

END FOR
```

### Dependency Setup

If PyPDF2 is not installed, create a virtual environment first:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install PyPDF2
```

### Markdown Output Naming

```
Original: UserManual.pdf (72 pages)
Markdown files:
  UserManual_1_20.md    (pages 1-20)
  UserManual_21_40.md   (pages 21-40)
  UserManual_41_60.md   (pages 41-60)
  UserManual_61_72.md   (pages 61-72)
```

### Example Output

```
📄 Processing: 115wmsug.pdf
📊 Page count: 458 pages
⚠️ Pages > 10 threshold → converting to Markdown

📝 Converting to Markdown (23 chunks of 20 pages)...
  ✅ Created: 115wmsug_1_20.md
  ✅ Created: 115wmsug_21_40.md
  ...
  ✅ Created: 115wmsug_441_458.md

📖 Reading Markdown files sequentially...
  ✅ Chunk 1/23: 115wmsug_1_20.md - processed
  ✅ Chunk 2/23: 115wmsug_21_40.md - processed
  ...
```

---

## File Processing Pattern

```python
# This is the ONLY valid pattern for processing files

files = list_all_files(PATH_TO_CLIENT_MATERIALS)
successful = []
failed = []

for file in files:

    # Pre-check: Skip known unsupported types
    if is_video_url(file):
        log_skip(file, "Unsupported media type")
        failed.append(file)
        continue  # ← NEXT FILE

    # Audio/Video Handling
    if is_audio_file(file) or is_video_file(file):
         # Transcribe first
         transcript = transcribe(file)
         if transcript:
             successful.append((file, transcript))
         else:
             log_skip(file, "Transcription failed")
             failed.append(file)
         continue


    # Special handling for PDFs
    if file.endswith('.pdf'):
        # Check page count first
        page_count = get_pdf_page_count(file)  # Use pdf_splitter.py count

        if page_count > 10:
            # Convert to Markdown first
            md_files = convert_to_markdown(file, output_dir)  # Use pdf_splitter.py automd
            for md_file in md_files:
                try:
                    content = read(md_file)  # Read .md files, NOT PDFs
                    if content:
                        successful.append((md_file, content))
                except:
                    log_skip(md_file, "Markdown read failed")
                    failed.append(md_file)
            continue  # ← NEXT FILE (after processing all markdown files)

    # Single attempt to read (for non-PDF or small PDF)
    try:
        content = read(file)
        if content:
            successful.append((file, content))
        else:
            log_skip(file, "Empty content")
            failed.append(file)
    except:
        log_skip(file, "Read failed")
        failed.append(file)

    # ALWAYS continue to next file
    continue

# After all files processed
print(f"Processed {len(successful)} files, skipped {len(failed)} files")
proceed_with_analysis(successful)
```

---

## 🚨🚨🚨 MANDATORY: QUALITY GUARDRAILS & VALIDATION 🚨🚨🚨

The Discovery process is governed by the **Embedded Guardrails** policy. No phase is complete without proof of validation.

### The Predictability Gate
Every Deliverable and Checkpoint MUST be validated using the standalone validator script:
- **Command**: `python3 .claude/hooks/discovery_quality_gates.py`
- **Options**:
  - `--validate-file <Path>`: Use immediately after writing any markdown deliverable.
  - `--validate-checkpoint <N>`: Use after completing all actions in a phase.

### Validation Requirements
1.  **Metadata**: All files must start with the standard YAML metadata block.
2.  **Traceability**: All requirement references must use correct ID patterns (e.g., PP-1.1, JTBD-2.3).
3.  **No Orphans**: P0 requirements must trace to upstream pain points.
4.  **Proof of success**: You must capture and report the validation output as evidence in the `PROGRESS_TRACKER.md`.

---

## 🚨 MANDATORY: ROOT-LEVEL REGISTRY PROPAGATION 🚨

**CRITICAL**: After generating Discovery outputs, you MUST propagate key registries to ROOT-level `traceability/` folder.

### ROOT-Level Files to Create

| Checkpoint | Discovery Output | ROOT File to Create |
|------------|------------------|---------------------|
| CP 1-2 (Analysis) | Client material analysis | `traceability/client_facts_registry.json` |
| CP 2 (Pain Points) | Pain points extracted | `traceability/pain_point_registry.json` |
| CP 3 (Personas) | Personas generated | `traceability/user_type_registry.json` |
| CP 4 (JTBD) | Jobs to be done | `traceability/jtbd_registry.json` |
| CP 9 (Screens) | Screen definitions | `traceability/screen_registry.json` |
| CP 11 (Final) | All trace links | `traceability/trace_links.json` |

### Client Facts Registry (NEW - MANDATORY)

During Phase 1 (Analyze Materials), extract client facts and create:

```json
// traceability/client_facts_registry.json
{
  "schema_version": "1.0.0",
  "stage": "Discovery",
  "checkpoint": 1,
  "system_name": "{SystemName}",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD",
  "source_files": [
    "path/to/interview1.md",
    "path/to/interview2.md"
  ],
  "facts": [
    {
      "id": "CF-001",
      "type": "quote",
      "source": "interview1.md",
      "stakeholder": "Warehouse Manager",
      "content": "We lose 2 hours daily searching for items",
      "category": "pain_point",
      "referenced_by": ["PP-1.1"]
    },
    {
      "id": "CF-002",
      "type": "metric",
      "source": "interview2.md",
      "stakeholder": "Operations Director",
      "content": "Current accuracy is 87%",
      "category": "baseline",
      "referenced_by": ["KPI-001"]
    },
    {
      "id": "CF-003",
      "type": "requirement",
      "source": "requirements.docx",
      "stakeholder": "Client",
      "content": "Must integrate with SAP ERP",
      "category": "constraint",
      "referenced_by": ["CONST-001"]
    }
  ],
  "summary": {
    "total_facts": 45,
    "by_type": {
      "quote": 25,
      "metric": 10,
      "requirement": 8,
      "constraint": 2
    },
    "by_category": {
      "pain_point": 20,
      "baseline": 8,
      "goal": 10,
      "constraint": 7
    }
  }
}
```

### Fact Extraction During Phase 1

When reading each client material file, extract and categorize:

| Fact Type | What to Extract | Example |
|-----------|-----------------|---------|
| `quote` | Direct stakeholder statements | "We spend 30% of time on manual entry" |
| `metric` | Quantitative data | "87% accuracy", "2 hours daily" |
| `requirement` | Explicit client requirements | "Must support offline mode" |
| `constraint` | Limitations or mandates | "Cannot replace existing ERP" |

### Propagation Template

```python
# After Phase 1 (Analyze Materials)
facts = extract_client_facts(processed_files)
write("traceability/client_facts_registry.json", {
  "schema_version": "1.0.0",
  "stage": "Discovery",
  "checkpoint": 1,
  "system_name": system_name,
  "created_at": today,
  "updated_at": today,
  "source_files": processed_files,
  "facts": facts,
  "summary": compute_summary(facts)
})

# After Phase 2 (Pain Points)
pain_points = extract_pain_points()
write("traceability/pain_point_registry.json", pain_points)

# After Phase 3 (Personas)
user_types = extract_user_types()
write("traceability/user_type_registry.json", user_types)

# After Phase 4 (JTBD)
jtbd = extract_jtbd()
write("traceability/jtbd_registry.json", jtbd)

# After Phase 9 (Screens)
screens = extract_screens()
write("traceability/screen_registry.json", screens)
```

### Validation

After completing discovery, verify ROOT files exist:

```bash
ls -la traceability/
# Should show: client_facts_registry.json, pain_point_registry.json,
#              user_type_registry.json, jtbd_registry.json, screen_registry.json
```

---

## Output Structure

Create these folders at PATH_TO_OUTPUT:

```
00-management/
├── PROGRESS_TRACKER.md
└── FAILURES_LOG.md      ← Log all skipped files here
01-analysis/
├── [PDF_Name]_Analysis/     ← Deep PDF analysis (one per PDF)
│   ├── SYSTEM_KNOWLEDGE.md  ← Architecture, concepts, capabilities
│   ├── TERMINOLOGY.md       ← Domain terms and definitions
│   ├── GAP_ANALYSIS.md      ← System capabilities vs user needs
│   └── SECTION_INDEX.md     ← PDF sections with page ranges
├── PDF_ANALYSIS_INDEX.md    ← Master index of all analyzed PDFs
├── PDF_FINDINGS_SUMMARY.md  ← Consolidated findings across PDFs
└── ANALYSIS_SUMMARY.md      ← Overall analysis summary
02-research/
├── personas/                    ← Subfolder for persona files
│   └── PERSONA_[ROLE].md        ← One file per persona (e.g., PERSONA_WAREHOUSE_OPERATOR.md)
└── JOBS_TO_BE_DONE.md           ← Jobs organized by persona
03-strategy/
├── PRODUCT_VISION.md            ← Vision statement and pillars
├── PRODUCT_STRATEGY.md          ← Strategic objectives and initiatives
├── PRODUCT_ROADMAP.md           ← Phased release plan with epics
└── KPIS_AND_GOALS.md            ← Success metrics and targets
04-design-specs/
├── screen-definitions.md        ← Screen inventory and layouts
├── navigation-structure.md      ← Site map and user flows
├── data-fields.md               ← Entity and field specifications
└── interaction-patterns.md      ← Behaviors and state management
05-documentation/
├── INDEX.md                     ← Master document index
├── README.md                    ← Getting started guide
└── VALIDATION_REPORT.md         ← Final validation report
```

---

## 🚨 MANDATORY FILE NAMING CONVENTIONS 🚨

### UPPERCASE with Underscores (Analysis, Research, Strategy)
- `ANALYSIS_SUMMARY.md`, `PAIN_POINTS.md`
- `PERSONA_[ROLE_NAME].md` (e.g., `PERSONA_WAREHOUSE_OPERATOR.md`)
- `JOBS_TO_BE_DONE.md`
- `PRODUCT_VISION.md`, `PRODUCT_STRATEGY.md`, `PRODUCT_ROADMAP.md`
- `KPIS_AND_GOALS.md`

### lowercase with dashes (Design Specs)
- `screen-definitions.md`
- `navigation-structure.md`
- `data-fields.md`
- `interaction-patterns.md`

### Personas MUST be Separate Files
Create `02-research/personas/` subfolder with one file per persona:
```
02-research/personas/
├── PERSONA_WAREHOUSE_OPERATOR.md
├── PERSONA_WAREHOUSE_SUPERVISOR.md
├── PERSONA_WAREHOUSE_MANAGER.md
└── PERSONA_SYSTEM_ADMINISTRATOR.md
```

---

## FAILURES_LOG.md Template

```markdown
---
document_id: DISC-FAILURES-001
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_Orchestrator
source_files:
  - "[PATH_TO_CLIENT_MATERIALS]"
change_history:
  - version: "1.0.0"
    date: "[YYYY-MM-DD]"
    author: "Discovery_Orchestrator"
    changes: "Initial generation from discovery analysis"
---

# ⛔ Skipped Files Log

**Analysis Date**: [Date]
**Total Files**: [N]
**Processed**: [N]
**Skipped**: [N]

## Skipped Items

| File | Reason |
|------|--------|
| manual.pdf | PDF has too many pages |
| intro.mp4 | Video files not supported |
| https://youtube.com/... | Video URLs not supported |

## Impact

These files were not included in the analysis. If they contain critical information:
- For PDFs: Copy text manually or use Adobe Acrobat to export as text
- For videos: Provide a transcript file instead
- For audio: Provide a transcript file instead

## Analysis Continues

The analysis proceeded with [N] successfully processed files.
```

## PROGRESS_TRACKER.md Template

```markdown
---
document_id: DISC-PROGRESS-001
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_Orchestrator
change_history:
  - version: "1.0.0"
    date: "[YYYY-MM-DD]"
    author: "Discovery_Orchestrator"
    changes: "Initial progress tracking creation"
---

# Discovery Progress Tracker

[Progress content here]
```

---

## Execution Phases

### Phase 0: Initialize
1. Create folder structure
2. Create PROGRESS_TRACKER.md (Update with validation section)
3. Create FAILURES_LOG.md
4. List all files in input folder
5. **Run Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 0`

### Phase 1: Analyze Materials
**For each file:**
- Try to read it ONCE
- If success: extract content
- **Extract client facts** (quotes, metrics, requirements, constraints)
- **Run Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-file <DeliverablePath>`
- If fail: log to FAILURES_LOG.md, continue
- **NEVER retry, NEVER try alternatives**

**After processing all files:**
- Create `traceability/client_facts_registry.json` with extracted facts (see ROOT-LEVEL REGISTRY PROPAGATION section)
- **Run Phase Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 1`

### Phase 1.5: Deep PDF Analysis (NEW)
**Uses**: `Discovery_AnalyzePDF` skill

**For each PDF file successfully read:**
1. Create dedicated folder: `01-analysis/[PDF_Name]_Analysis/`
2. Generate 4 analysis documents:
   - `SYSTEM_KNOWLEDGE.md` - Architecture, concepts, capabilities
   - `TERMINOLOGY.md` - Domain terms and definitions
   - `GAP_ANALYSIS.md` - System capabilities vs user pain points
   - `SECTION_INDEX.md` - PDF sections with page ranges
3. After all PDFs processed, generate:
   - `01-analysis/PDF_ANALYSIS_INDEX.md` - Master index
   - `01-analysis/PDF_FINDINGS_SUMMARY.md` - Consolidated findings

**When to use Discovery_AnalyzePDF:**
- PDF is a technical manual, user guide, or reference document
- PDF has >10 pages
- Deep system knowledge extraction is valuable

**Skip this phase if:**
- No PDFs in input materials
- PDFs are simple forms or single-page documents

### Phase 1.8: External Domain Research (NEW)
**Agent**: `discovery-domain-researcher`
**Goal**: Augment internal materials with external market context.

**Actions**:
1. Analyze project domain from Phase 1 outputs.
2. Conduct web research for:
   - Similar domain problems and solutions
   - Competitive landscape and feature sets
   - Go-to-Market (GTM) strategies
   - Technology trends and standards
3. Generate:
   - `02-research/MARKET_ANALYSIS.md`
   - `02-research/COMPETITIVE_LANDSCAPE.md`
   - `02-research/EXTERNAL_TRENDS.md`

**Validation**: Verify files exist and contain cited sources.

### Phase 2: Extract Domain Insights
- Use content from Phase 1 AND Phase 1.5
- Reference PDF gap analysis for pain point validation
- Include terminology in domain vocabulary
- Create `01-analysis/PAIN_POINTS.md`
- **Propagate to ROOT**: Create `traceability/pain_point_registry.json` with extracted pain points
- **Run Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 2`

### Phase 3: Generate Personas
**Skill**: `Discovery_GenPersonas`
**Output**: `02-research/personas/PERSONA_[ROLE].md` (one file per persona)
**Propagate to ROOT**: Create/update `traceability/user_type_registry.json` with user types from personas
**Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 3 --dir [OUTPUT_PATH]`

### Phase 4: Generate JTBD
**Skill**: `Discovery_GenJTBD`
**Output**: `02-research/JOBS_TO_BE_DONE.md`
**Propagate to ROOT**: Create/update `traceability/jtbd_registry.json` with extracted JTBD items
**Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 4 --dir [OUTPUT_PATH]`

### Phase 5: Product Vision
**Skill**: `Discovery_StratVision`
**Output**: `03-strategy/PRODUCT_VISION.md`
**Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 5 --dir [OUTPUT_PATH]`

### Phase 6: Product Strategy
**Skill**: `Discovery_StratStrategy`
**Output**: `03-strategy/PRODUCT_STRATEGY.md`
**Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 6 --dir [OUTPUT_PATH]`

### Phase 7: Product Roadmap
**Skill**: `Discovery_StratRoadmap`
**Output**: `03-strategy/PRODUCT_ROADMAP.md`
**Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 7 --dir [OUTPUT_PATH]`

### Phase 8: KPIs and Goals
**Skill**: `Discovery_StratKPIs`
**Output**: `03-strategy/KPIS_AND_GOALS.md`
**Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 8 --dir [OUTPUT_PATH]`

### Phase 9: Design Specifications (CRITICAL - 4 SKILLS REQUIRED)
**MANDATORY**: Execute ALL 4 skills below. Do NOT skip any.

| Step | Skill | Output File | Required |
|------|-------|-------------|----------|
| 9.1 | `Discovery_SpecScreens` | `04-design-specs/screen-definitions.md` | YES |
| 9.2 | `Discovery_SpecNavigation` | `04-design-specs/navigation-flows.md` | YES |
| 9.3 | `Discovery_SpecDataModel` | `04-design-specs/data-fields.md` | YES |
| 9.4 | `Discovery_SpecInteractions` | `04-design-specs/interaction-patterns.md` | YES |

**OPTIONAL** (if resources allow):
| Step | Skill | Output File |
|------|-------|-------------|
| 9.5 | `Discovery_SpecSampleData` | `04-design-specs/sample-data.json` |
| 9.6 | `Discovery_SpecComponents` | `04-design-specs/ui-components.md` |

**Propagate to ROOT**: After generating screens, create/update `traceability/screen_registry.json`

**Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 9 --dir [OUTPUT_PATH]`

⚠️ **PHASE 9 VALIDATION MUST PASS BEFORE PROCEEDING TO PHASE 10**

### Phase 10: Documentation (5 FILES REQUIRED)
**Skills**: `Discovery_DocIndex` + `Discovery_DocSummary`

| File | Skill | Required |
|------|-------|----------|
| `05-documentation/INDEX.md` | Discovery_DocIndex | YES |
| `05-documentation/README.md` | Discovery_DocIndex | YES |
| `05-documentation/GETTING_STARTED.md` | Discovery_DocIndex | YES |
| `05-documentation/FILES_CREATED.md` | Discovery_DocIndex | YES |
| `05-documentation/DOCUMENTATION_SUMMARY.md` | Discovery_DocSummary | YES |

**Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 10 --dir [OUTPUT_PATH]`

### Phase 11: Validation Report
**Skill**: `Discovery_Validate`
**Output**: `05-documentation/VALIDATION_REPORT.md`
**Validation**: `python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 11 --dir [OUTPUT_PATH]`

---

## 🚀 PARALLEL AGENT EXECUTION MODE (v7.0)

Discovery orchestration supports parallel agent execution for up to **45% faster** completion times. This mode spawns specialized agents that work concurrently on independent tasks.

### Agent Architecture Overview

```
┌────────────────────────────────────────────────────────────────────────────┐
│                     DISCOVERY PARALLEL EXECUTION FLOW                      │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  PHASE 1: MATERIAL ANALYSIS (PARALLEL)                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐  │   │
│  │  │ PDF Analyst  │ │ Interview    │ │ Design       │ │ Data       │  │   │
│  │  │ (sonnet)     │ │ Analyst      │ │ Analyst      │ │ Analyst    │  │   │
│  │  │              │ │ (sonnet)     │ │ (sonnet)     │ │ (haiku)    │  │   │
│  │  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └─────┬──────┘  │   │
│  │         │                │                │               │         │   │
│  │         └────────────────┼────────────────┼───────────────┘         │   │
│  │                          ▼                ▼                         │   │
│  │                  ┌───────────────────────────────┐                  │   │
│  │                  │     REGISTRY MERGE GATE       │                  │   │
│  │                  │ (Consolidate parallel outputs)│                  │   │
│  │                  └───────────────┬───────────────┘                  │   │
│  └──────────────────────────────────┼──────────────────────────────────┘   │
│                                     ▼                                      │
│  CHECKPOINT 1-2: VALIDATION                                                │
│                                     │                                      │
│                                     ▼                                      │
│  PHASE 3-4: RESEARCH (PARALLEL)                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ┌──────────────────────┐        ┌──────────────────────┐           │   │
│  │  │  Persona Generator   │        │  JTBD Extractor      │           │   │
│  │  │  (sonnet)            │        │  (sonnet)            │           │   │
│  │  └──────────┬───────────┘        └──────────┬───────────┘           │   │
│  │             │                               │                       │   │
│  │             └───────────────┬───────────────┘                       │   │
│  │                             ▼                                       │   │
│  │                  ┌───────────────────────────────┐                  │   │
│  │                  │     REGISTRY MERGE GATE       │                  │   │
│  │                  └───────────────┬───────────────┘                  │   │
│  └──────────────────────────────────┼──────────────────────────────────┘   │
│                                     ▼                                      │
│  CHECKPOINT 3-4: VALIDATION                                                │
│                                     │                                      │
│                                     ▼                                      │
│  PHASE 4-11: VALIDATION (PARALLEL)                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ┌────────────────────────┐    ┌────────────────────────────┐       │   │
│  │  │ Pain Point Validator   │    │ Cross-Reference Validator  │       │   │
│  │  │ (haiku)                │    │ (haiku)                    │       │   │
│  │  └────────────────────────┘    └────────────────────────────┘       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Available Discovery Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `discovery-pdf-analyst` | sonnet | Deep PDF extraction with chunking |
| `discovery-interview-analyst` | sonnet | Interview processing for pain points |
| `discovery-design-analyst` | sonnet | Visual material analysis |
| `discovery-data-analyst` | haiku | Spreadsheet/data extraction (structured) |
| `discovery-domain-researcher` | sonnet | Web research for market/competitor context |
| `discovery-persona-generator` | sonnet | Persona synthesis from client facts |
| `discovery-jtbd-extractor` | sonnet | Jobs-to-be-done derivation |
| `discovery-pain-validator` | haiku | Pain point evidence validation (checklist) |
| `discovery-cross-validator` | haiku | Bidirectional link validation (checklist) |

**Note**: All agents use `subagent_type: "general-purpose"` with agent instructions in `.claude/agents/`.

### Parallel Execution Protocol

#### Phase 1: Material Analysis & Domain Research (5 Agents in Parallel)

When input folder contains mixed materials, spawn agents by file type plus the domain researcher:

```javascript
// Spawn material analysis agents in parallel
const agents = [];

// ALWAYS spawn Domain Researcher
agents.push(Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Conduct external domain research",
  prompt: `Agent: discovery-domain-researcher
    Read: .claude/agents/discovery-domain-researcher.md
    INPUT: ${INPUT_PATH} | OUTPUT: ${OUTPUT_PATH}/02-research/
    CREATE: MARKET_ANALYSIS.md, COMPETITIVE_LANDSCAPE.md, EXTERNAL_TRENDS.md
    UPDATE: traceability/client_facts_registry.json (CF-5XX IDs)
    RETURN: JSON { files_written, files_failed, competitors_found, trends_identified }`
}));

if (hasPdfFiles) {
  agents.push(Task({
    subagent_type: "general-purpose",
    model: "sonnet",
    description: "Analyze PDF materials",
    prompt: `Agent: discovery-pdf-analyst
      Read: .claude/agents/discovery-pdf-analyst.md
      INPUT: ${INPUT_PATH} | OUTPUT: ${OUTPUT_PATH}/01-analysis/[PDF_Name]_Analysis/
      CREATE: SYSTEM_KNOWLEDGE.md, TERMINOLOGY.md, GAP_ANALYSIS.md, SECTION_INDEX.md (per PDF)
      UPDATE: traceability/client_facts_registry.json (CF-1XX IDs)
      RETURN: JSON { files_written, files_failed, pdfs_processed, facts_extracted }`
  }));
}

if (hasInterviews) {
  agents.push(Task({
    subagent_type: "general-purpose",
    model: "sonnet",
    description: "Analyze interviews",
    prompt: `Agent: discovery-interview-analyst
      Read: .claude/agents/discovery-interview-analyst.md
      INPUT: ${INPUT_PATH} | OUTPUT: ${OUTPUT_PATH}/01-analysis/
      CREATE: INTERVIEW_INSIGHTS.md
      UPDATE: traceability/pain_point_registry.json (PP-X.X), traceability/quotes_registry.json
      RETURN: JSON { files_written, files_failed, pain_points_extracted, quotes_extracted }`
  }));
}

if (hasDesignFiles) {
  agents.push(Task({
    subagent_type: "general-purpose",
    model: "sonnet",
    description: "Analyze design materials",
    prompt: `Agent: discovery-design-analyst
      Read: .claude/agents/discovery-design-analyst.md
      INPUT: ${INPUT_PATH} | OUTPUT: ${OUTPUT_PATH}/01-analysis/
      CREATE: COMPONENT_INVENTORY.md, NAVIGATION_PATTERNS.md, DESIGN_TOKENS_BASELINE.md
      UPDATE: traceability/client_facts_registry.json (CF-3XX IDs)
      RETURN: JSON { files_written, files_failed, screenshots_processed, components_found }`
  }));
}

if (hasDataFiles) {
  agents.push(Task({
    subagent_type: "general-purpose",
    model: "haiku",  // Structured data extraction
    description: "Analyze data files",
    prompt: `Agent: discovery-data-analyst
      Read: .claude/agents/discovery-data-analyst.md
      INPUT: ${INPUT_PATH} | OUTPUT: ${OUTPUT_PATH}/01-analysis/
      CREATE: DATA_DICTIONARY.md, BUSINESS_RULES.md, ENTITY_RELATIONSHIPS.md
      UPDATE: traceability/client_facts_registry.json (CF-4XX IDs)
      RETURN: JSON { files_written, files_failed, data_files_processed, entities_found }`
  }));
}

// Wait for all to complete
const agentResults = await Promise.all(agents);

// 🚨 CRITICAL: Verify files were actually written by sub-agents
console.log("Verifying sub-agent file outputs...");

for (const result of agentResults) {
  if (result.files_failed && result.files_failed.length > 0) {
    console.error(`⚠️ Sub-agent failed to write files: ${result.files_failed.join(', ')}`);
    // Fallback: Write files from agent response content if available
    for (const failedFile of result.files_failed) {
      if (result.content && result.content[failedFile]) {
        Write(failedFile, result.content[failedFile]);
        console.log(`✅ Recovered file from agent output: ${failedFile}`);
      }
    }
  }
}

// Final verification: Check critical files exist
const criticalFiles = [
  'traceability/client_facts_registry.json',
  'traceability/pain_point_registry.json'
];

for (const file of criticalFiles) {
  if (!fileExists(file)) {
    console.error(`❌ CRITICAL: ${file} was not created by sub-agents`);
    // This will be caught by checkpoint validation
  }
}
```

#### Registry Merge Gate (After Parallel Phase)

After parallel agents complete, merge their outputs:

```python
# Registry Merging Protocol
def merge_parallel_outputs(agent_results):
    """
    Merge outputs from parallel agents into unified registries.

    MERGE RULES:
    1. IDs assigned by agent remain authoritative (no conflicts)
    2. Cross-references validated after merge
    3. Duplicates detected by content similarity (>80%)
    """

    # 1. Collect all client facts from agents
    all_facts = []
    for result in agent_results:
        if 'client_facts' in result:
            all_facts.extend(result['client_facts'])

    # 2. Deduplicate by content similarity
    unique_facts = deduplicate_by_similarity(all_facts, threshold=0.8)

    # 3. Re-sequence IDs if needed (maintain agent prefixes)
    # PDF Analyst: CF-1XX
    # Interview Analyst: CF-2XX
    # Design Analyst: CF-3XX
    # Data Analyst: CF-4XX

    # 4. Write unified registry
    write("traceability/client_facts_registry.json", {
        "schema_version": "1.0.0",
        "facts": unique_facts,
        "merged_from": [r['agent_id'] for r in agent_results],
        "merge_timestamp": datetime.now().isoformat()
    })

    # 5. Similar process for pain_point_registry
    merge_pain_points(agent_results)
```

#### Phase 3-4: Research (2 Agents in Parallel)

```javascript
// Spawn research agents in parallel
const researchAgents = [
  Task({
    subagent_type: "general-purpose",
    model: "sonnet",
    description: "Generate personas",
    prompt: `Agent: discovery-persona-generator
      Read: .claude/agents/discovery-persona-generator.md
      INPUT: traceability/client_facts_registry.json, traceability/pain_point_registry.json
      OUTPUT: ${OUTPUT_PATH}/02-research/personas/
      CREATE: PERSONA_[ROLE].md (one per persona), traceability/user_type_registry.json
      RETURN: JSON { files_written, files_failed, personas_generated }`
  }),

  Task({
    subagent_type: "general-purpose",
    model: "sonnet",
    description: "Extract JTBD",
    prompt: `Agent: discovery-jtbd-extractor
      Read: .claude/agents/discovery-jtbd-extractor.md
      INPUT: traceability/pain_point_registry.json, ${OUTPUT_PATH}/02-research/personas/
      OUTPUT: ${OUTPUT_PATH}/02-research/
      CREATE: JOBS_TO_BE_DONE.md, traceability/jtbd_registry.json
      RETURN: JSON { files_written, files_failed, jtbd_extracted }`
  })
];

const researchResults = await Promise.all(researchAgents);

// 🚨 CRITICAL: Verify research files were written
for (const result of researchResults) {
  if (result.files_failed && result.files_failed.length > 0) {
    console.error(`⚠️ Research agent failed to write: ${result.files_failed.join(', ')}`);
  }
}

// Merge: Cross-link personas and JTBD
await merge_research_outputs();
```

#### Validation Agents (Run After Phase 4)

Validation agents run after Phase 4 completes. **CRITICAL**: Files must be verified before proceeding.

```javascript
// Spawn validators after Phase 4 completes
const validators = [
  Task({
    subagent_type: "general-purpose",
    model: "haiku",  // Checklist-based validation
    description: "Validate pain points",
    prompt: `Agent: discovery-pain-validator
      Read: .claude/agents/discovery-pain-validator.md
      INPUT: traceability/pain_point_registry.json | SOURCE: ${INPUT_PATH}
      OUTPUT: ${OUTPUT_PATH}/reports/PAIN_POINT_VALIDATION.md
      RETURN: { file_written, pain_points_validated, evidence_gaps }`
  }),

  Task({
    subagent_type: "general-purpose",
    model: "haiku",  // Checklist-based validation
    description: "Validate cross-references",
    prompt: `Agent: discovery-cross-validator
      Read: .claude/agents/discovery-cross-validator.md
      INPUT: traceability/
      OUTPUT: ${OUTPUT_PATH}/reports/CROSS_REFERENCE_VALIDATION.md
      RETURN: { file_written, links_validated, orphans_found }`
  })
];

// 🚨 CRITICAL: Wait for ALL validators to complete before proceeding
await Promise.all(validators);

// Verify files were actually written
const validatorOutputs = [
  `${OUTPUT_PATH}/reports/PAIN_POINT_VALIDATION.md`,
  `${OUTPUT_PATH}/reports/CROSS_REFERENCE_VALIDATION.md`
];

for (const file of validatorOutputs) {
  if (!fileExists(file)) {
    console.error(`⚠️ Validator output not persisted: ${file}`);
    // Write from agent response if available
  }
}
```

### ID Namespace Allocation

To prevent ID conflicts during parallel execution:

| Agent | ID Prefix | Range |
|-------|-----------|-------|
| PDF Analyst | CF-1XX | CF-100 to CF-199 |
| Interview Analyst | CF-2XX, PP-1.X-2.X | CF-200 to CF-299 |
| Design Analyst | CF-3XX | CF-300 to CF-399 |
| Data Analyst | CF-4XX | CF-400 to CF-499 |
| Persona Generator | UT-XXX | UT-001 to UT-099 |
| JTBD Extractor | JTBD-X.X | JTBD-1.1 to JTBD-99.99 |

### Coordination Rules

1. **File Locking**: Agents MUST acquire locks before writing to shared registries
2. **Read-Only During Parallel**: Agents read from input, write to temporary outputs
3. **Merge Gate**: All parallel agents must complete before registry merge
4. **Checkpoint Validation**: Run after merge, not after individual agents

### Enabling Parallel Mode

```bash
# Standard (sequential) execution
/discovery InventorySystem ./input/

# Parallel execution (add --parallel flag)
/discovery InventorySystem ./input/ --parallel

# Resume parallel execution
/discovery-resume --parallel
```

### Parallel Execution State

Track parallel execution in `_state/discovery_progress.json`:

```json
{
  "execution_mode": "parallel",
  "current_phase": "1-material-analysis",
  "parallel_agents": [
    {
      "agent_id": "discovery-pdf-analyst",
      "status": "completed",
      "started_at": "2025-12-27T10:00:00Z",
      "completed_at": "2025-12-27T10:15:00Z",
      "output_facts": 45
    },
    {
      "agent_id": "discovery-interview-analyst",
      "status": "completed",
      "started_at": "2025-12-27T10:00:00Z",
      "completed_at": "2025-12-27T10:12:00Z",
      "output_facts": 32
    }
  ],
  "merge_status": "pending",
  "next_gate": "registry-merge"
}
```

---

## 🚨 MANDATORY VALIDATION ENFORCEMENT 🚨

**RULE**: You MUST run checkpoint validation after EACH phase.
**RULE**: You MUST NOT proceed to the next phase until validation passes.
**RULE**: If validation fails, fix the issue before continuing.

```bash
# Example: After completing Phase 9
python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 9 --dir ClientAnalysis_[SystemName]/

# Expected output for PASS:
# ✅ Checkpoint 9 deliverables verified in ClientAnalysis_[SystemName]

# If FAILED:
# ❌ QUALITY GATE FAILED: Missing mandatory deliverable for Checkpoint 9: ...
# → FIX THE ISSUE, then re-run validation
```

---

## Supported File Types

### ✅ Will Attempt to Read
- .txt, .md, .rtf (text files)
- .docx (Word documents)
- .pdf (**auto-chunked if >30 pages** - see PDF CHUNKING section)
- .xlsx, .csv (spreadsheets)
- .pptx (presentations)
- .json, .xml, .yaml (data files)
- .mp3, .wav, .m4a (audio files - **transcribed first**)
- .mp4, .mov, .avi (video files - **transcribed first**)

### 📄 PDF Special Handling
- ≤10 pages: Read directly
- >10 pages: **Auto-convert to Markdown using `automd`, process .md files sequentially**
- Tool: `.claude/skills/tools/pdf_splitter.py automd`
- Output naming: `{filename}_{start}_{end}.md`

### ⛔ Skip Immediately (Don't Even Try)
- Video URLs (youtube.com, vimeo.com, etc.)
- Archive files (.zip, .tar, .gz)
- Executable files (.exe, .app)

---

## Quick Reference: Error Responses

| Error | Response |
|-------|----------|
| PDF too large (>10 pages) | Convert to Markdown using `automd`. If conversion fails → SKIP |
| ANY other error | Log SKIP and CONTINUE |

See `.claude/rules/error-handling.md` for full details.


---

## What Success Looks Like

```
Reading files from /path/to/materials...

✅ interview1.txt - 175 lines processed
✅ interview2.txt - 203 lines processed
✅ requirements.docx - processed
⛔ SKIPPED: manual.pdf - PDF has too many pages
⛔ SKIPPED: demo.mp4 - Video files not supported
✅ data.xlsx - processed
⛔ SKIPPED: https://youtube.com/... - Video URLs not supported
✅ notes.md - processed

Summary: 5 files processed, 3 files skipped

Proceeding with analysis using 5 processed files...
```

---

**Skill Version**: 6.0.0
**Framework Compatibility**: Discovery Skills Framework v6.0

**Key Changes in v6.0**:
- Enforced mandatory file naming conventions
- Personas output to separate files: `02-research/personas/PERSONA_[ROLE].md`
- Strategy documents UPPERCASE: `PRODUCT_VISION.md`, `PRODUCT_STRATEGY.md`, `PRODUCT_ROADMAP.md`, `KPIS_AND_GOALS.md`
- Design specs lowercase with dashes: `screen-definitions.md`, `navigation-structure.md`, `data-fields.md`, `interaction-patterns.md`
- JTBD output renamed to `JOBS_TO_BE_DONE.md`
