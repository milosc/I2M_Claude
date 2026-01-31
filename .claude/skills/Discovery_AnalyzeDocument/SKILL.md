---
name: analyzing-documents
description: Use when you need to process external document files (DOCX, TXT, MD) for discovery analysis.
model: sonnet
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
context: fork
agent: general-purpose
skill_id: Discovery_AnalyzeDocument
version: 4.0.0
created_at: 2025-01-15
updated_at: 2025-12-21
change_history:
  - version: "4.0.0"
    date: "2025-12-21"
    author: "Milos Cigoj"
    changes: "Added MarkItDown conversion - large PDFs now converted to Markdown before reading"
  - version: "3.0.0"
    date: "2025-12-21"
    author: "Milos Cigoj"
    changes: "Added automatic PDF chunking for large PDFs (>30 pages)"
  - version: "2.1.0"
    date: "2025-12-19"
    author: "Milos Cigoj"
    changes: "Added version control metadata per VERSION_CONTROL_STANDARD.md"
  - version: "2.0.0"
    date: "2025-01-15"
    author: "Milos Cigoj"
    changes: "Initial skill version for Discovery Skills Framework v2.0"
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-documents started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-documents ended '{"stage": "discovery"}'
---

# Discovery Analyze Document

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill analyzing-documents instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Description

Analyzes text-based documents (txt, docx, pdf, rtf, md) to extract product discovery insights.

**PDF HANDLING**: PDFs with >10 pages are automatically split into 20-page chunks and converted to Markdown files for efficient processing.

---

## ⚙️ DEPENDENCIES: PyPDF2 + MarkItDown

The PDF processing feature requires PyPDF2 and MarkItDown. To install:

```bash
# Use the project's virtual environment
/htec-libraries-init
# Or: python3 .claude/skills/tools/htec_dependencies_installer.py

# Commands available:
.venv/bin/python .claude/skills/tools/pdf_splitter.py count <file.pdf>
.venv/bin/python .claude/skills/tools/pdf_splitter.py automd <file.pdf> <output_dir>
```

If dependencies are not available, large PDFs will be skipped (per error handling rules).

---

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:analyzing-documents:started` - When skill begins
- `skill:analyzing-documents:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## 🚨 MANDATORY: PDF READING PROCEDURE

### ⚠️ CRITICAL: NEVER Read() a Large PDF Without Converting to Markdown First

**THE RULE**: You MUST check page count BEFORE attempting to read ANY PDF file. For PDFs >10 pages, convert to Markdown first using `automd` command.

```
WRONG (causes "PDF too large" error or high context usage):
    Read("/path/to/manual.pdf")  ← NEVER DO THIS DIRECTLY

CORRECT:
    1. Check pages first: .venv/bin/python .claude/skills/tools/pdf_splitter.py count manual.pdf
    2. If pages ≤ 10: Read(manual.pdf) directly
    3. If pages > 10: Convert to Markdown, then read .md files
```

### The Rule: 10-Page Threshold

| PDF Pages | Action |
|-----------|--------|
| ≤10 pages | Read directly with `Read()` tool |
| >10 pages | **MUST convert to Markdown first, then read .md files** |

### PDF Processing Flow (MANDATORY STEPS)

```
FOR EACH .pdf file:

    STEP 1: CHECK PAGE COUNT FIRST (REQUIRED - NO EXCEPTIONS)
    ══════════════════════════════════════════════════════════
    Run: .venv/bin/python .claude/skills/tools/pdf_splitter.py count <file.pdf>

    Store the page count. DO NOT skip this step.

    STEP 2: BRANCH BASED ON PAGE COUNT
    ═══════════════════════════════════
    IF pages ≤ 10:
        → Read(<file.pdf>) directly
        → Process content
        → Done with this file

    IF pages > 10:
        → DO NOT attempt Read() on original file (will fail!)
        → Proceed to STEP 3

    STEP 3: CONVERT TO MARKDOWN (when pages > 10)
    ═════════════════════════════════════════════
    Create markdown directory: [INPUT_PATH]/_pdf_markdown/[pdf_basename]/

    NOTE: Store in client materials folder for REUSE across discovery runs!

    Run: .venv/bin/python .claude/skills/tools/pdf_splitter.py automd <file.pdf> [INPUT_PATH]/_pdf_markdown/[pdf_basename]/

    This splits into 20-page chunks AND converts to Markdown:
    Example: UserManual_1_20.md, UserManual_21_40.md, UserManual_41_60.md, UserManual_61_72.md

    STEP 4: READ MARKDOWN FILES SEQUENTIALLY
    ════════════════════════════════════════
    FOR EACH .md file in [INPUT_PATH]/_pdf_markdown/[pdf_basename]/:
        Read(<chunk.md>)          ← Markdown files, NOT PDFs
        extract_insights(chunk_content)
        log_success(chunk)
    END FOR

    STEP 5: COMBINE INSIGHTS
    ════════════════════════
    Merge all extracted content from markdown files into single analysis

    ON ANY ERROR: log skip, continue to next file

END FOR
```

### Output Naming Convention

```
Original: UserManual.pdf (72 pages)
Output (Markdown):
  UserManual_1_20.md     (pages 1-20)
  UserManual_21_40.md    (pages 21-40)
  UserManual_41_60.md    (pages 41-60)
  UserManual_61_72.md    (pages 61-72)
```

### Example: Processing a 150-page PDF

```
📄 Processing: technical_manual.pdf
📊 Page count: 150 pages
⚠️ Pages > 10 threshold → converting to Markdown

📝 Converting to Markdown (8 chunks of 20 pages)...
  ✅ Created: technical_manual_1_20.md
  ✅ Created: technical_manual_21_40.md
  ✅ Created: technical_manual_41_60.md
  ✅ Created: technical_manual_61_80.md
  ✅ Created: technical_manual_81_100.md
  ✅ Created: technical_manual_101_120.md
  ✅ Created: technical_manual_121_140.md
  ✅ Created: technical_manual_141_150.md

📖 Reading Markdown files...
  ✅ Chunk 1/8: technical_manual_1_20.md - 8 pain points extracted
  ✅ Chunk 2/8: technical_manual_21_40.md - 6 pain points extracted
  ✅ Chunk 3/8: technical_manual_41_60.md - 10 pain points extracted
  ✅ Chunk 4/8: technical_manual_61_80.md - 7 pain points extracted
  ✅ Chunk 5/8: technical_manual_81_100.md - 5 pain points extracted
  ✅ Chunk 6/8: technical_manual_101_120.md - 6 pain points extracted
  ✅ Chunk 7/8: technical_manual_121_140.md - 5 pain points extracted
  ✅ Chunk 8/8: technical_manual_141_150.md - 3 pain points extracted

✅ Complete: 50 total pain points from 8 Markdown files
```

---

## 🚨 ERROR HANDLING

> **STRICT RULE**: Follow the global error handling rules in `.claude/rules/error-handling.md`.
>
> 1. **One Attempt ONLY**: If a file fails to read/process, log failure and SKIP.
> 2. **No Fixes**: Do not retry, install tools, or switch libraries.
> 3. **PDF Markdown Conversion**: If >10 pages, MUST convert to Markdown using `automd`. If conversion fails, SKIP.


---

## Supported Files

| Extension | Notes |
|-----------|-------|
| .txt | Usually works |
| .md | Usually works |
| .rtf | Usually works |
| .docx | Usually works |
| .pdf | **Converted to Markdown if >10 pages** |

---

## Extraction Framework

When a file IS successfully read, extract:

### Pain Points
- "Problem:", "Issue:", "Challenge:"
- "Frustrating", "difficult", "takes too long"

### Requirements  
- "Must", "Shall", "Should"
- User story format

### Quotes
- Text in quotation marks
- "[Name] said..."

### Metrics
- Percentages, dollar amounts
- Time durations

---

## Output Format

Save to: `01-analysis/document-[name]-analysis.md`

```markdown
# Document Analysis: [Title]

**Source**: [filename]
**Status**: ✅ Processed / ⛔ Skipped

## Extracted Content

### Pain Points
- [List]

### Requirements
- [List]

### Quotes
- [List]

### Metrics
- [List]
```

---

## Example: Correct Behavior

```
Processing documents...

document1.txt → Reading... ✅ Extracted 15 pain points
document2.docx → Reading... ✅ Extracted 8 requirements
manual.pdf → Reading... Error: PDF too large
           → ⛔ SKIPPED: manual.pdf - too many pages
           → Moving to next file...
document3.md → Reading... ✅ Extracted 5 quotes

Done. 3 processed, 1 skipped.
```

---

**Version**: 4.0
**Key Principle**: One attempt per file, convert large PDFs to Markdown
