---
name: analyzing-spreadsheets
description: Use when you need to extract insights from spreadsheet files (XLSX, CSV, TSV, XLS) including metrics, comparisons, and workflows.
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
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-spreadsheets started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-spreadsheets ended '{"stage": "discovery"}'
---

# Analyze Spreadsheets

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill analyzing-spreadsheets instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_AnalyzeSpreadsheet
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for extracting insights from spreadsheet files (xlsx, csv, tsv, xls). Analyzes tabular data for metrics, comparisons, workflows, and structured information relevant to product discovery.

**Role**: You are a Spreadsheet Analysis Specialist. Your expertise is interpreting tabular data, identifying patterns, extracting metrics, and understanding the business context encoded in spreadsheets.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:analyzing-spreadsheets:started` - When skill begins
- `skill:analyzing-spreadsheets:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- User provides spreadsheet files (xlsx, xls, csv, tsv)
- Request mentions "analyze spreadsheet", "extract from Excel", "data analysis"
- Context involves metrics, comparisons, or structured data review

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Spreadsheet Files | Yes | One or more spreadsheet files |
| Sheet Names | No | Specific sheets to analyze |
| Data Context | No | What the data represents |
| Output Path | Yes | Where to save analysis |

## Spreadsheet Type Detection

### Auto-Classification Rules

| Pattern | Classification |
|---------|---------------|
| Columns: Name, Email, Status | User/Contact List |
| Columns: Feature, Priority, Status | Backlog/Tracker |
| Columns: Date, Amount, Category | Financial Data |
| Columns: KPI, Target, Actual | Metrics Dashboard |
| Columns: Step, Owner, Duration | Process/Workflow |
| Comparison columns (A vs B) | Comparison Matrix |
| Triage, Score, Decision | Evaluation Matrix |

## Extraction Framework

### 1. Structure Analysis
- Identify header rows
- Detect data types per column
- Find calculated fields/formulas
- Note conditional formatting (priorities)
- Identify pivot tables or summaries

### 2. Content Extraction

#### Metrics & KPIs
- Numeric columns with targets
- Percentage calculations
- Trend indicators
- Aggregate formulas (SUM, AVG, COUNT)

#### Categorical Data
- Status columns (Open, Closed, In Progress)
- Priority indicators (P0, P1, High, Low)
- Owner/Assignment columns
- Type classifications

#### Workflow Indicators
- Date sequences
- Stage progressions
- Handoff points
- Duration calculations

### 3. Pain Point Detection in Data
- High counts in "blocked" or "delayed" status
- Long durations compared to targets
- Low scores in satisfaction columns
- High error rates or rework counts

## Output Format

### Primary Output: `[output_path]/01-analysis/spreadsheet-[name]-analysis.md`

```markdown
# Spreadsheet Analysis: [Filename]

**Source File**: [Filename]
**Sheets Analyzed**: [List]
**Total Rows**: [Count]
**Data Date Range**: [If applicable]

---

## 📋 Spreadsheet Overview

**Purpose**: [Inferred purpose]
**Data Type**: [List/Tracker/Metrics/Comparison/etc.]
**Key Entities**: [What rows represent]

---

## 📊 Structure Summary

### Sheet: [Sheet Name]

| Column | Data Type | Sample Values | Purpose |
|--------|-----------|---------------|---------|
| [Column A] | [Text/Number/Date] | [Examples] | [Inferred purpose] |

---

## 📈 Metrics Extracted

### Key Performance Indicators

| Metric | Current Value | Target | Status |
|--------|---------------|--------|--------|
| [Metric name] | [Value] | [Target] | [Above/Below/On Target] |

### Aggregate Statistics

| Measure | Value | Context |
|---------|-------|---------|
| Total Records | [N] | - |
| Average [X] | [Value] | [Interpretation] |
| Max/Min [X] | [Range] | [Significance] |

---

## 🔴 Pain Points Detected in Data

### Pattern: [Pain Point Category]
**Evidence**: [What the data shows]
**Impact**: [Quantified if possible]
**Rows Affected**: [Count or percentage]

---

## 📋 Categorical Analysis

### Status Distribution
| Status | Count | Percentage |
|--------|-------|------------|
| [Status A] | [N] | [%] |

### Priority Distribution
| Priority | Count | Percentage |
|----------|-------|------------|
| P0 | [N] | [%] |

---

## 🔄 Workflow Insights

**Identified Stages**: [List stages from data]
**Average Duration**: [If calculable]
**Bottlenecks**: [Stages with long durations]

---

## 👥 Entity/User Insights

**Unique Entities**: [Count]
**Entity Types**: [Categories found]
**Key Attributes**: [Important fields per entity]

---

## 📊 Data Quality Notes

- [Missing data observations]
- [Inconsistent formatting]
- [Potential data issues]

---

## 🏷️ Tags

`#spreadsheet` `#[data-type]` `#[topic]`

---

**Analysis Date**: [Date]
**Confidence Level**: [High/Medium/Low]
```

## Specific Spreadsheet Patterns

### Triage/Evaluation Matrices
- Extract scoring criteria
- Identify decision thresholds
- Map candidate → score → decision flow
- Note rejection/approval patterns

### Comparison Spreadsheets
- Identify compared entities
- Extract evaluation criteria
- Note winner/selection rationale
- Capture feature comparisons

### Tracking Spreadsheets
- Identify workflow stages
- Extract timing metrics
- Note status patterns
- Capture assignment flows

## 🚨 ERROR HANDLING

> **STRICT RULE**: Follow the global error handling rules in `.claude/rules/error-handling.md`.

| Issue | Action |
|-------|--------|
| Any read error | Log skip, continue |
| Password protected | Log skip (cannot process) |
| Very large (>100k rows) | Sample first 10k rows ONLY |


## Integration Points

### Feeds Into
- `Discovery_ExtractMetrics` - Quantitative data
- `Discovery_ExtractWorkflows` - Process patterns
- `Discovery_ExtractUserTypes` - Entity categories

### Receives From
- `Discovery_Orchestrator` - Files and context

---

**Skill Version**: 2.0
**Framework Compatibility**: Discovery Skills Framework v2.0
