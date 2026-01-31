---
name: extracting-client-facts
description: Use when you need to extract and trace raw client facts (quotes, metrics, requirements, constraints) from discovery materials to build upstream traceability.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-client-facts started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-client-facts ended '{"stage": "discovery"}'
---

# Extract Client Facts

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill extracting-client-facts instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_ExtractClientFacts
- **Version**: 1.0.0
- **Created**: 2025-12-23
- **Updated**: 2025-12-23
- **Author**: Milos Cigoj
- **Change History**:
  - v1.0.0 (2025-12-23): Initial skill version - extracts client facts with full traceability

## Description

Extracts raw facts from client materials (interviews, documents, PDFs, screenshots) and populates the `traceability/client_facts_registry.json` registry. This is the **upstream anchor** for all traceability chains - every pain point, JTBD, and requirement should trace back to specific client facts.

**Role**: You are a Client Facts Curator. Your expertise is identifying verifiable facts from client materials, preserving source attribution, and building the foundation for full upstream traceability.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:extracting-client-facts:started` - When skill begins
- `skill:extracting-client-facts:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Why Client Facts Matter

```
CLIENT FACTS (CF) → Pain Points (PP) → JTBD → Requirements → Screens → Code
     ↑
     └── This is the UPSTREAM ANCHOR that validates everything downstream
```

Without client facts:
- Pain points have no evidence
- JTBDs have no grounding
- Requirements are unsubstantiated claims

## Trigger Conditions

- **Phase 1** of Discovery Analysis (during material processing)
- After reading each client material file
- Request mentions "extract facts", "client evidence", "source traceability"

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Client Materials | Yes | Processed content from interviews, PDFs, documents |
| System Name | Yes | For registry metadata |
| Output Path | Yes | PROJECT ROOT for `traceability/client_facts_registry.json` |

## Fact Types to Extract

| Type | What to Extract | Example | ID Prefix |
|------|-----------------|---------|-----------|
| `quote` | Direct stakeholder statements | "We lose 2 hours daily searching for items" | CF-Q-XXX |
| `metric` | Quantitative data | "87% accuracy", "2 hours daily", "$50K loss" | CF-M-XXX |
| `requirement` | Explicit client requirements | "Must support offline mode" | CF-R-XXX |
| `constraint` | Limitations or mandates | "Cannot replace existing ERP" | CF-C-XXX |
| `observation` | Observed behaviors/patterns | "Users switch between 3 systems" | CF-O-XXX |

## Fact Categories

| Category | Description | Links To |
|----------|-------------|----------|
| `pain_point` | Evidence of problems | PP-X.X |
| `baseline` | Current state metrics | KPI-XXX |
| `goal` | Desired outcomes | PRODUCT_VISION |
| `constraint` | Technical/business limits | CONST-XXX |
| `workflow` | Process descriptions | WF-XXX |

## Extraction Framework

### 1. Source File Processing

For each client material file:

```
FILE: interviews/warehouse_manager.md
SOURCE_ID: SRC-001

Extract:
├── Quotes (direct statements in quotes or first-person)
├── Metrics (numbers, percentages, time, money)
├── Requirements (must, shall, should, need)
├── Constraints (cannot, must not, blocked by)
└── Observations (screen behavior, process steps)
```

### 2. Fact Identification Signals

**Quote Signals:**
- Text in quotation marks
- "I...", "We...", "Our team..."
- Strong opinion words (frustrating, critical, essential)

**Metric Signals:**
- Numbers with units (hours, dollars, percentage)
- Comparisons (X times more, Y% less)
- Frequencies (daily, weekly, always, never)

**Requirement Signals:**
- "Must have...", "Need to...", "Should be able to..."
- "Required for...", "Essential that..."
- User story format: "As a X, I want Y, so that Z"

**Constraint Signals:**
- "Cannot change...", "Must keep..."
- "Budget limited to...", "Timeline is..."
- "Legacy system requires...", "Regulation mandates..."

### 3. Attribution

Every fact MUST have:
- **Source File**: Which file it came from
- **Source ID**: Unique identifier for the source (SRC-XXX)
- **Stakeholder**: Who said/wrote it (role, not name)
- **Location**: Page number, timestamp, or section reference
- **Confidence**: How certain we are this is accurate

## Output: `traceability/client_facts_registry.json`

```json
{
  "schema_version": "1.0.0",
  "stage": "Discovery",
  "checkpoint": 1,
  "system_name": "{SystemName}",
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "source_files": [
    {
      "id": "SRC-001",
      "path": "interviews/warehouse_manager.md",
      "type": "interview",
      "processed_at": "YYYY-MM-DDTHH:MM:SSZ",
      "facts_extracted": 12
    },
    {
      "id": "SRC-002",
      "path": "manuals/115wmsug_Analysis/",
      "type": "pdf_analysis",
      "processed_at": "YYYY-MM-DDTHH:MM:SSZ",
      "facts_extracted": 25
    }
  ],
  "facts": [
    {
      "id": "CF-Q-001",
      "type": "quote",
      "source_id": "SRC-001",
      "source_file": "interviews/warehouse_manager.md",
      "source_location": "Line 45",
      "stakeholder": "Warehouse Manager",
      "content": "We lose 2 hours daily searching for items in the wrong locations",
      "category": "pain_point",
      "confidence": "high",
      "tags": ["time_waste", "inventory_location", "search"],
      "referenced_by": ["PP-1.1", "PP-1.2"],
      "extracted_at": "YYYY-MM-DDTHH:MM:SSZ"
    },
    {
      "id": "CF-M-001",
      "type": "metric",
      "source_id": "SRC-001",
      "source_file": "interviews/warehouse_manager.md",
      "source_location": "Line 67",
      "stakeholder": "Warehouse Manager",
      "content": "Current inventory accuracy is 87%",
      "category": "baseline",
      "confidence": "high",
      "tags": ["accuracy", "baseline", "kpi"],
      "referenced_by": ["KPI-001"],
      "extracted_at": "YYYY-MM-DDTHH:MM:SSZ"
    },
    {
      "id": "CF-R-001",
      "type": "requirement",
      "source_id": "SRC-002",
      "source_file": "requirements.docx",
      "source_location": "Section 3.2",
      "stakeholder": "Client",
      "content": "System must integrate with SAP ERP for real-time inventory sync",
      "category": "constraint",
      "confidence": "high",
      "tags": ["integration", "sap", "real_time"],
      "referenced_by": ["CONST-001", "REQ-INT-001"],
      "extracted_at": "YYYY-MM-DDTHH:MM:SSZ"
    },
    {
      "id": "CF-C-001",
      "type": "constraint",
      "source_id": "SRC-001",
      "source_file": "interviews/operations_director.md",
      "source_location": "Line 120",
      "stakeholder": "Operations Director",
      "content": "We cannot replace the existing barcode scanners - $200K investment last year",
      "category": "constraint",
      "confidence": "high",
      "tags": ["hardware", "budget", "barcode"],
      "referenced_by": ["CONST-002"],
      "extracted_at": "YYYY-MM-DDTHH:MM:SSZ"
    },
    {
      "id": "CF-O-001",
      "type": "observation",
      "source_id": "SRC-003",
      "source_file": "screenshots/current_system.png",
      "source_location": "Screenshot analysis",
      "stakeholder": "System",
      "content": "Current UI requires 5 clicks to complete a simple inventory transfer",
      "category": "pain_point",
      "confidence": "medium",
      "tags": ["ux", "efficiency", "clicks"],
      "referenced_by": ["PP-2.1"],
      "extracted_at": "YYYY-MM-DDTHH:MM:SSZ"
    }
  ],
  "summary": {
    "total_facts": 45,
    "total_sources": 5,
    "by_type": {
      "quote": 25,
      "metric": 10,
      "requirement": 5,
      "constraint": 3,
      "observation": 2
    },
    "by_category": {
      "pain_point": 20,
      "baseline": 8,
      "goal": 10,
      "constraint": 5,
      "workflow": 2
    },
    "by_confidence": {
      "high": 35,
      "medium": 8,
      "low": 2
    }
  }
}
```

## Execution Steps

### Step 1: Initialize Registry

```python
# At start of Phase 1
registry = {
    "schema_version": "1.0.0",
    "stage": "Discovery",
    "checkpoint": 1,
    "system_name": SYSTEM_NAME,
    "created_at": TODAY,
    "updated_at": TODAY,
    "source_files": [],
    "facts": [],
    "summary": {}
}
```

### Step 2: Process Each Material

For each client material file being analyzed:

```python
# After successfully reading file content
source_entry = {
    "id": f"SRC-{source_counter:03d}",
    "path": relative_path,
    "type": detect_type(file),  # interview, pdf_analysis, screenshot, etc.
    "processed_at": NOW,
    "facts_extracted": 0
}

facts = extract_facts(content, source_entry)
source_entry["facts_extracted"] = len(facts)

registry["source_files"].append(source_entry)
registry["facts"].extend(facts)
```

### Step 3: Finalize and Write

```python
# After all materials processed
registry["updated_at"] = NOW
registry["summary"] = compute_summary(registry["facts"])

# Write to ROOT-level traceability folder
write("traceability/client_facts_registry.json", registry)
```

## ID Assignment

| Type | Format | Example |
|------|--------|---------|
| Source | SRC-NNN | SRC-001, SRC-002 |
| Quote | CF-Q-NNN | CF-Q-001, CF-Q-025 |
| Metric | CF-M-NNN | CF-M-001, CF-M-010 |
| Requirement | CF-R-NNN | CF-R-001, CF-R-005 |
| Constraint | CF-C-NNN | CF-C-001, CF-C-003 |
| Observation | CF-O-NNN | CF-O-001, CF-O-002 |

## Linking to Downstream Artifacts

When Pain Points are extracted (Phase 2), update the `referenced_by` field:

```json
{
  "id": "CF-Q-001",
  "content": "We lose 2 hours daily searching for items",
  "referenced_by": ["PP-1.1", "PP-1.2"]  // ← Updated when PP extracted
}
```

Pain Point should reference back:

```json
{
  "id": "PP-1.1",
  "title": "Time wasted searching for inventory",
  "client_facts": ["CF-Q-001", "CF-M-001"]  // ← Upstream evidence
}
```

## Error Handling

| Issue | Action |
|-------|--------|
| File fails to read | Skip file, log in FAILURES_LOG.md |
| No facts found in file | Log warning, continue (some files may be metadata-only) |
| Duplicate fact detected | Keep first occurrence, note duplicate source |
| Unclear attribution | Set confidence to "low", mark stakeholder as "Unknown" |

## Integration Points

### Called During
- `discovery-analyze` command (Phase 1)
- After each file is successfully read
- Before Phase 2 (Pain Points extraction)

### Receives From
- `Discovery_AnalyzeDocument` - Document content
- `Discovery_AnalyzePDF` - PDF analysis folders
- `Discovery_AnalyzePresentation` - Presentation content
- All `Discovery_Analyze*` skills

### Feeds Into
- `Discovery_ExtractPainPoints` - Evidence for pain points
- `Discovery_GeneratePersona` - Stakeholder quotes
- `Discovery_GenerateKPIs` - Baseline metrics
- `Discovery_Validate` - Traceability verification

## Quality Gates

After Phase 1, verify:

```bash
python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 1 --dir ClientAnalysis_X/

# Should check:
# - traceability/client_facts_registry.json exists
# - Registry has at least 1 fact
# - All facts have valid source_id references
# - Summary totals match facts array length
```

## Minimum Requirements

| Metric | Minimum | Target |
|--------|---------|--------|
| Total facts | ≥5 | ≥20 |
| Sources processed | ≥1 | All available |
| Types covered | ≥2 | All 5 types |
| High confidence | ≥50% | ≥80% |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: Discovery Skills Framework v6.1
