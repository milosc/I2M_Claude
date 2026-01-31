---
name: analyzing-pdf-documents
description: Use when you need to perform deep extraction of system knowledge, terminology, and gap analysis from technical PDF manuals or guides.
model: sonnet
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-pdf-documents started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-pdf-documents ended '{"stage": "discovery"}'
---

# Analyze PDF Documents

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill analyzing-pdf-documents instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_AnalyzePDF
- **Version**: 1.0.0
- **Created**: 2025-12-21
- **Updated**: 2025-12-21
- **Author**: Discovery Framework
- **Change History**:
  - v1.0.0 (2025-12-21): Initial skill version - deep PDF analysis with dedicated subfolders

## Description
Deep analysis of PDF documents (especially technical manuals, user guides, and reference documentation) to extract system knowledge, terminology, and gap analysis. Produces dedicated analysis subfolders per PDF and consolidated findings.

## Execution Logging (MANDATORY)

This skill logs all execution to the global pipeline progress registry. Logging is automatic and requires no manual configuration.

### How Logging Works

Every execution of this skill is logged to `_state/lifecycle.json`:

- **start_event**: Logged when skill execution begins
- **end_event**: Logged when skill execution completes

Events include:
- skill_name, intent, stage, system_name
- start/end timestamps
- status (completed/failed)
- output files created (PDF analysis documents)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "analyzing-pdf-documents"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "analyzing-pdf-documents" --stage discovery
```

Logging is handled automatically by the skill framework. No user action required.

---

## Output Structure

```
01-analysis/
├── [PDF_Name]_Analysis/           ← One folder per PDF
│   ├── SYSTEM_KNOWLEDGE.md        ← Architecture, concepts, capabilities
│   ├── TERMINOLOGY.md             ← Domain terms and definitions
│   ├── GAP_ANALYSIS.md            ← System capabilities vs user needs
│   └── SECTION_INDEX.md           ← PDF sections with page ranges
├── PDF_ANALYSIS_INDEX.md          ← Master index of all analyzed PDFs
└── PDF_FINDINGS_SUMMARY.md        ← Consolidated findings across PDFs
```

---

## Trigger Conditions

Execute this skill when:
- PDF files are detected in input materials
- PDF is a technical manual, user guide, or reference document
- PDF has >10 pages (smaller PDFs use Discovery_AnalyzeDocument)
- Deep system knowledge extraction is needed

---

## Prerequisites

### PDF Processing (for PDFs >10 pages)

```bash
# Check page count
.venv/bin/python .claude/skills/tools/pdf_splitter.py count <file.pdf>

# Auto-process + convert to Markdown (MANDATORY for PDFs >10 pages)
# Store in client materials folder for REUSE across discovery runs!
.venv/bin/python .claude/skills/tools/pdf_splitter.py automd <file.pdf> [INPUT_PATH]/_pdf_markdown/[pdf_name]/

# This splits large PDFs into 20-page chunks and converts all to Markdown files
```

### Dependencies

Ensure virtual environment is set up:
```bash
/htec-libraries-init
# Or: python3 .claude/skills/tools/htec_dependencies_installer.py
```

Required packages: PyPDF2, markitdown (installed via htec-libraries-init)

---

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:analyzing-pdf-documents:started` - When skill begins
- `skill:analyzing-pdf-documents:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## 🚨 MANDATORY: PDF READING PROCEDURE

### ⚠️ CRITICAL: NEVER Read() a Large PDF Without Converting to Markdown First

**THE RULE**: You MUST check page count BEFORE attempting to read ANY PDF file. For PDFs >10 pages, convert to Markdown first using `automd` command.

```
WRONG (causes "PDF too large" error or high context usage):
    Read("/path/to/large_manual.pdf")  ← NEVER DO THIS

CORRECT:
    1. .venv/bin/python .claude/skills/tools/pdf_splitter.py count /path/to/large_manual.pdf
    2. If pages ≤ 10: Read("/path/to/large_manual.pdf") directly
    3. If pages > 10: Convert to Markdown, then read .md files
```

### PDF Processing Flow (MANDATORY)

```
FOR EACH .pdf file in input folder:

    STEP 1: CHECK PAGE COUNT (REQUIRED - NO EXCEPTIONS)
    ═══════════════════════════════════════════════════
    Run: .venv/bin/python .claude/skills/tools/pdf_splitter.py count <file.pdf>

    This returns the page count. Store it.

    STEP 2: BRANCH BASED ON PAGE COUNT
    ═══════════════════════════════════
    IF pages ≤ 10:
        → Read(<file.pdf>) directly
        → Process content

    IF pages > 10:
        → DO NOT attempt Read() on original file
        → Proceed to STEP 3

    STEP 3: CONVERT TO MARKDOWN (when pages > 10)
    ═════════════════════════════════════════════
    Create markdown directory: [INPUT_PATH]/_pdf_markdown/[pdf_name]/

    NOTE: Store in client materials folder for REUSE across discovery runs!

    Run: .venv/bin/python .claude/skills/tools/pdf_splitter.py automd <file.pdf> [INPUT_PATH]/_pdf_markdown/[pdf_name]/

    This splits into 20-page chunks AND converts to Markdown files:
    Example: manual_1_20.md, manual_21_40.md, manual_41_60.md

    STEP 4: READ MARKDOWN FILES SEQUENTIALLY
    ════════════════════════════════════════
    FOR EACH .md file in [INPUT_PATH]/_pdf_markdown/[pdf_name]/:
        Read(<chunk.md>)          ← Markdown files, NOT PDFs
        Extract insights from chunk
        Store extracted content
    END FOR

    STEP 5: COMBINE CHUNK INSIGHTS
    ══════════════════════════════
    Merge all extracted content from markdown files into single analysis

    STEP 6: CREATE ANALYSIS FOLDER
    ══════════════════════════════
    Create sanitized folder name: [PDF_Name]_Analysis
       - Remove spaces, special chars
       - Example: "115wmsug.pdf" → "115wmsug_Analysis"
    Create output folder: 01-analysis/[PDF_Name]_Analysis/

END FOR
```

### Example: Correct Processing of a 326-Page PDF

```bash
# STEP 1: Check page count FIRST
.venv/bin/python .claude/skills/tools/pdf_splitter.py count "/path/to/115wmsug.pdf"
# Output: 📄 115wmsug.pdf: 326 pages
#         ⚠️ NEEDS SPLITTING (threshold: 10 pages)

# STEP 2: Pages > 10, so DO NOT read original

# STEP 3: Convert to Markdown (splits + converts in one step)
# Store in client materials folder for reuse!
.venv/bin/python .claude/skills/tools/pdf_splitter.py automd "/path/to/115wmsug.pdf" "[INPUT_PATH]/_pdf_markdown/115wmsug/"
# Creates: 115wmsug_1_20.md, 115wmsug_21_40.md, ... 115wmsug_321_326.md

# STEP 4: Read each Markdown file (NOT PDF chunks)
Read("[INPUT_PATH]/_pdf_markdown/115wmsug/115wmsug_1_20.md")    # ✅ Works - Markdown
Read("[INPUT_PATH]/_pdf_markdown/115wmsug/115wmsug_21_40.md")   # ✅ Works - Markdown
... continue for all .md files ...

# STEP 5: Combine insights from all markdown files

# STEP 6: Create analysis folder and outputs
```

### Phase 2: Deep Content Extraction (Per PDF)

For each PDF (or its chunks), extract:

#### 2.1 System Knowledge

Extract and document:
- **Core Architecture**: System components, modules, layers
- **Key Concepts**: Primary entities, objects, identifiers (e.g., LPNs, transactions)
- **Processing Rules**: Business rules, engines, decision logic
- **Data Flow**: How information moves through the system
- **Transaction Types**: Supported operations and their characteristics
- **Integration Points**: APIs, interfaces, external connections

#### 2.2 Terminology

Extract domain-specific terms:
- Technical terms with definitions
- Acronyms and abbreviations
- System-specific concepts
- Industry terminology

#### 2.3 Section Analysis

Document PDF structure:
- Major sections with page ranges
- Content summary per section
- Key topics covered

---

## Output Templates

### 1. SYSTEM_KNOWLEDGE.md

```markdown
---
document_id: DISC-SYSKNOW-[PDF_NAME]-001
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_AnalyzePDF
source_files:
  - "[PDF filename]"
change_history:
  - version: "1.0.0"
    date: "[YYYY-MM-DD]"
    author: "Discovery_AnalyzePDF"
    changes: "Initial extraction from PDF"
---

# System Knowledge: [PDF Title]

**Source**: [Full PDF name and page count]
**Extracted**: [Date]

---

## Executive Summary

[2-3 paragraph overview of what this document covers and key takeaways]

---

## Core Architecture

### 1. [Primary Component/Concept]

[Description of the component]

**Key Characteristics**:
- [Bullet points of important attributes]

**Implications for [Product Name]**:
- [How this affects the product being designed]

### 2. [Secondary Component/Concept]

[Continue pattern for each major system component]

---

## Processing Rules / Business Logic

### [Rule Category 1]

| Rule Type | Purpose |
|-----------|---------|
| [Rule 1]  | [Description] |
| [Rule 2]  | [Description] |

**Rule Components**:
- [List of rule elements]

### [Rule Category 2]

[Continue for other rule categories]

---

## Data Flow

```
[ASCII diagram or description of data flow]
```

### Known System Behaviors

1. **[Behavior 1]**: [Description]
2. **[Behavior 2]**: [Description]

---

## Transaction Types

| Transaction | Description |
|-------------|-------------|
| [Type 1]    | [What it does] |
| [Type 2]    | [What it does] |

### Transaction Processing

[Description of how transactions are processed]

---

## Integration Points

| Integration | Type | Notes |
|-------------|------|-------|
| [System 1]  | [API/File/etc] | [Details] |

---

## Technical Architecture Notes

- **Platform**: [Platform details]
- **Client Type**: [Client architecture]
- **Database**: [Database info]
- **Known Limitations**: [List of limitations]

---

## Recommendations Based on System Knowledge

### For [Recommendation Area 1]
- **Current**: [Current state]
- **Needed**: [What's needed]

### For [Recommendation Area 2]
- **Current**: [Current state]
- **Needed**: [What's needed]

---

**Document Status**: Complete
**Integration**: Cross-referenced with ANALYSIS_SUMMARY.md
```

### 2. TERMINOLOGY.md

```markdown
---
document_id: DISC-TERMS-[PDF_NAME]-001
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_AnalyzePDF
source_files:
  - "[PDF filename]"
change_history:
  - version: "1.0.0"
    date: "[YYYY-MM-DD]"
    author: "Discovery_AnalyzePDF"
    changes: "Initial terminology extraction"
---

# Terminology Reference: [PDF Title]

**Source**: [PDF name]
**Terms Extracted**: [Count]

---

## Acronyms & Abbreviations

| Acronym | Full Form | Context |
|---------|-----------|---------|
| [ABC]   | [Full name] | [Where/how used] |

---

## Domain Terms

| Term | Definition | Related Concepts |
|------|------------|------------------|
| [Term 1] | [Definition] | [Related terms] |
| [Term 2] | [Definition] | [Related terms] |

---

## System-Specific Concepts

| Concept | Definition | Usage |
|---------|------------|-------|
| [Concept 1] | [What it means in this system] | [How it's used] |

---

## Industry Standards Referenced

| Standard | Description | Relevance |
|----------|-------------|-----------|
| [Standard 1] | [Description] | [Why it matters] |

---

**Cross-Reference**: See SYSTEM_KNOWLEDGE.md for detailed explanations
```

### 3. GAP_ANALYSIS.md

```markdown
---
document_id: DISC-GAPS-[PDF_NAME]-001
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_AnalyzePDF
source_files:
  - "[PDF filename]"
  - "01-analysis/ANALYSIS_SUMMARY.md"
change_history:
  - version: "1.0.0"
    date: "[YYYY-MM-DD]"
    author: "Discovery_AnalyzePDF"
    changes: "Initial gap analysis"
---

# Gap Analysis: [PDF Title] vs User Needs

**Source System**: [System name from PDF]
**Analysis Date**: [Date]

---

## Executive Summary

[Brief overview of the gap analysis findings]

---

## Gap Analysis Matrix

| User Pain Point | System Capability | Gap | Severity |
|-----------------|-------------------|-----|----------|
| [PP-X.X: Description] | [What system offers] | [What's missing] | P0/P1/P2 |
| [PP-X.X: Description] | [What system offers] | [What's missing] | P0/P1/P2 |

---

## Detailed Gap Analysis

### Gap 1: [Gap Title]

**User Need** (from Pain Point [PP-X.X]):
> [Quote or description of user need]

**System Reality**:
> [Quote from PDF or description of system behavior]

**Gap Description**:
[Detailed explanation of the gap]

**Impact**:
- [Business impact]
- [User impact]
- [Operational impact]

**Recommendation**:
[Suggested approach to address]

---

### Gap 2: [Gap Title]

[Continue pattern for each significant gap]

---

## Opportunities

| Opportunity | System Support | Implementation Notes |
|-------------|---------------|---------------------|
| [What could be improved] | [How system could help] | [Implementation considerations] |

---

## Constraints from System

| Constraint | Description | Workaround Needed |
|------------|-------------|-------------------|
| [Constraint 1] | [Why it exists] | [How to handle] |

---

## Priority Matrix

### Must Address (P0)
1. [Gap that blocks core functionality]

### Should Address (P1)
1. [Gap that significantly impacts UX]

### Could Address (P2)
1. [Gap that would be nice to fix]

---

**Cross-Reference**:
- Pain Points: `traceability/pain_point_registry.json`
- System Knowledge: `[PDF_Name]_Analysis/SYSTEM_KNOWLEDGE.md`
```

### 4. SECTION_INDEX.md

```markdown
---
document_id: DISC-INDEX-[PDF_NAME]-001
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_AnalyzePDF
source_files:
  - "[PDF filename]"
change_history:
  - version: "1.0.0"
    date: "[YYYY-MM-DD]"
    author: "Discovery_AnalyzePDF"
    changes: "Initial section index"
---

# PDF Section Index: [PDF Title]

**Source**: [PDF name]
**Total Pages**: [Page count]

---

## Document Structure

| Section | Pages | Content Summary |
|---------|-------|-----------------|
| [Section 1] | 1-25 | [What this section covers] |
| [Section 2] | 26-50 | [What this section covers] |

---

## Key Topics by Section

### [Section 1 Name] (Pages X-Y)

**Topics Covered**:
- [Topic 1]
- [Topic 2]

**Key Takeaways**:
- [Important point 1]
- [Important point 2]

### [Section 2 Name] (Pages X-Y)

[Continue pattern]

---

## Quick Reference

| Topic | Section | Page |
|-------|---------|------|
| [Topic 1] | [Section] | [Page] |
| [Topic 2] | [Section] | [Page] |

---

## Chunks Processed

| Chunk File | Pages | Status |
|------------|-------|--------|
| [filename]_1_30.pdf | 1-30 | Processed |
| [filename]_31_60.pdf | 31-60 | Processed |

---

**Full extracts available in**: This folder
```

### 5. PDF_ANALYSIS_INDEX.md (Master Index)

```markdown
---
document_id: DISC-PDF-INDEX-001
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_AnalyzePDF
source_files:
  - "[List all PDFs analyzed]"
change_history:
  - version: "1.0.0"
    date: "[YYYY-MM-DD]"
    author: "Discovery_AnalyzePDF"
    changes: "Initial PDF analysis index"
---

# PDF Analysis Index

**Analysis Date**: [Date]
**Total PDFs Analyzed**: [Count]
**Total Pages Processed**: [Count]

---

## Analyzed Documents

| PDF | Pages | Analysis Folder | Key Topics |
|-----|-------|-----------------|------------|
| [PDF 1] | [N] | [Folder link] | [Topics] |
| [PDF 2] | [N] | [Folder link] | [Topics] |

---

## Analysis Contents Per PDF

### [PDF 1 Name]

| Document | Purpose | Link |
|----------|---------|------|
| SYSTEM_KNOWLEDGE.md | Architecture & concepts | [Link] |
| TERMINOLOGY.md | Domain terms | [Link] |
| GAP_ANALYSIS.md | System vs needs | [Link] |
| SECTION_INDEX.md | PDF structure | [Link] |

### [PDF 2 Name]

[Continue pattern]

---

## Cross-PDF Insights

### Common Themes
- [Theme found across multiple PDFs]

### Conflicting Information
- [Any contradictions found]

### Integration Points
- [How PDFs relate to each other]

---

## Navigation

- [PDF_FINDINGS_SUMMARY.md](./PDF_FINDINGS_SUMMARY.md) - Consolidated findings
- [ANALYSIS_SUMMARY.md](./ANALYSIS_SUMMARY.md) - Overall analysis
```

### 6. PDF_FINDINGS_SUMMARY.md (Consolidated Findings)

```markdown
---
document_id: DISC-PDF-FINDINGS-001
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_AnalyzePDF
source_files:
  - "[List all PDF analysis folders]"
change_history:
  - version: "1.0.0"
    date: "[YYYY-MM-DD]"
    author: "Discovery_AnalyzePDF"
    changes: "Initial consolidated findings"
---

# PDF Analysis Findings Summary

**Analysis Date**: [Date]
**PDFs Analyzed**: [Count]

---

## Executive Summary

[2-3 paragraphs summarizing key findings across all PDFs]

---

## Key System Knowledge (Consolidated)

### Architecture Overview
[Consolidated view of system architecture from all PDFs]

### Core Concepts
| Concept | Source PDF | Description |
|---------|------------|-------------|
| [Concept 1] | [PDF] | [Description] |

### Critical Constraints
| Constraint | Source | Impact |
|------------|--------|--------|
| [Constraint 1] | [PDF] | [Impact] |

---

## Gap Analysis Summary

### Critical Gaps (P0)
| Gap | Source PDF | User Impact |
|-----|------------|-------------|
| [Gap 1] | [PDF] | [Impact] |

### High Priority Gaps (P1)
| Gap | Source PDF | User Impact |
|-----|------------|-------------|
| [Gap 1] | [PDF] | [Impact] |

---

## Terminology Master List

| Term | Definition | Source |
|------|------------|--------|
| [Term 1] | [Definition] | [PDF] |

[Top 20 most important terms across all PDFs]

---

## Recommendations

### Immediate Actions
1. [Action based on PDF findings]

### Strategic Considerations
1. [Long-term recommendation]

---

## Traceability

| Artifact | Location |
|----------|----------|
| Individual PDF Analyses | `01-analysis/[PDF_Name]_Analysis/` |
| Pain Points Registry | `traceability/pain_point_registry.json` |
| Client Facts Registry | `traceability/client_facts_registry.json` |

---

**Next Steps**: Use these findings in:
- `02-research/` - Personas and JTBD
- `03-strategy/` - Vision and Strategy
- `04-design-specs/` - Screen and component specs
```

---


## 🚨 ERROR HANDLING

> **STRICT RULE**: Follow the global error handling rules in `.claude/rules/error-handling.md`.
>
> 1. **One Attempt ONLY**: If a file fails to read/process, log failure and SKIP.
> 2. **No Fixes**: Do not retry, install tools, or switch libraries.
> 3. **PDF Markdown Conversion**: If >10 pages, MUST convert to Markdown using `automd`. If conversion fails, SKIP.

---

## Integration with Other Skills

### Input Dependencies
- None (runs early in Phase 1)

### Output Consumers
- `Discovery_ExtractPainPoints` - Uses gap analysis
- `Discovery_GeneratePersona` - Uses terminology
- `Discovery_GenerateStrategy` - Uses system constraints
- All design specs - Reference system knowledge

### Updates to ANALYSIS_SUMMARY.md

After completing PDF analysis, add a section:

```markdown
## PDF Deep Analysis

| PDF | Analysis Folder | Key Findings |
|-----|-----------------|--------------|
| [PDF 1] | [Link to folder] | [Summary] |

See [PDF_ANALYSIS_INDEX.md](./PDF_ANALYSIS_INDEX.md) for complete index.
See [PDF_FINDINGS_SUMMARY.md](./PDF_FINDINGS_SUMMARY.md) for consolidated findings.
```

---

## Quality Checklist

Before marking complete:

- [ ] Each PDF has its own `[PDF_Name]_Analysis/` folder
- [ ] Each folder contains all 4 documents (SYSTEM_KNOWLEDGE, TERMINOLOGY, GAP_ANALYSIS, SECTION_INDEX)
- [ ] PDF_ANALYSIS_INDEX.md lists all analyzed PDFs
- [ ] PDF_FINDINGS_SUMMARY.md consolidates findings
- [ ] Gap analysis references pain points from ANALYSIS_SUMMARY.md
- [ ] All cross-references are valid links
- [ ] Version control metadata in all output files

---

## Example Execution

```
Processing PDFs in /path/to/materials...

📄 Found: 115wmsug.pdf (326 pages)
📊 Converting to Markdown (17 chunks of 20 pages)...
  ✅ 115wmsug_1_20.md - converted
  ✅ 115wmsug_21_40.md - converted
  ...
  ✅ 115wmsug_321_326.md - converted
📖 Reading Markdown files...
  ✅ Chunk 1/17: 115wmsug_1_20.md - processed
  ✅ Chunk 2/17: 115wmsug_21_40.md - processed
  ...
  ✅ Chunk 17/17: 115wmsug_321_326.md - processed

📁 Creating: 01-analysis/115wmsug_Analysis/
  ✅ SYSTEM_KNOWLEDGE.md - 15 concepts extracted
  ✅ TERMINOLOGY.md - 42 terms defined
  ✅ GAP_ANALYSIS.md - 8 gaps identified
  ✅ SECTION_INDEX.md - 10 sections mapped

📄 Found: quick_reference.pdf (8 pages)
📖 Reading directly (≤10 pages)...
  ✅ Processed

📁 Creating: 01-analysis/quick_reference_Analysis/
  ✅ All 4 documents generated

📋 Generating consolidated outputs...
  ✅ PDF_ANALYSIS_INDEX.md
  ✅ PDF_FINDINGS_SUMMARY.md

Summary: 2 PDFs analyzed, 0 skipped
```

---

**Skill Version**: 1.0.0
**Key Principle**: Deep extraction with dedicated folders, consolidated index
