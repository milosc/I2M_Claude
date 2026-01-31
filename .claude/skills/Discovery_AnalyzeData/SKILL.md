---
name: analyzing-structured-data
description: Use when you need to infer schemas, relationships, and business entities from structured data files (JSON, XML, YAML, TOML).
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
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-structured-data started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-structured-data ended '{"stage": "discovery"}'
---

# Analyze Data

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill analyzing-structured-data instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_AnalyzeData
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for extracting insights from structured data files (JSON, XML, YAML, TOML). Analyzes data schemas, API responses, configuration files, and data exports to understand system data structures, relationships, and business entities relevant to product discovery.

**Role**: You are a Data Structure Analysis Specialist. Your expertise is interpreting structured data formats, inferring schemas, understanding data relationships, and extracting business entity definitions from real-world data samples.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:analyzing-structured-data:started` - When skill begins
- `skill:analyzing-structured-data:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- User provides data files (json, xml, yaml, toml)
- Request mentions "analyze data", "understand schema", "data structure"
- Context involves API responses, data exports, or configuration analysis
- Need to understand data models from actual data samples

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Data Files | Yes | Structured data files |
| Data Context | No | Type: API response, export, config, etc. |
| Schema Hints | No | Known entity names or structure |
| Output Path | Yes | Where to save analysis |

## Data Type Detection

### Auto-Classification Rules

| Pattern | Classification |
|---------|---------------|
| Single object with many fields | Entity Definition |
| Array of similar objects | Entity Collection |
| Nested objects with consistent structure | Relational Data |
| Key-value pairs with simple values | Configuration |
| OpenAPI/Swagger markers | API Specification |
| Database export markers | Data Export |
| Contains timestamps, IDs, status | Transactional Data |

## Extraction Framework

### 1. Schema Inference
- Identify all unique keys/fields
- Determine data types per field
- Detect nullable/optional fields
- Identify ID fields and references
- Find enum-like fields (limited values)

### 2. Relationship Detection

#### Foreign Key Patterns
- Fields ending in `_id`, `Id`, `ID`
- Fields matching entity names + `Id`
- Nested objects (embedded relationships)
- Arrays of IDs (many-to-many hints)

#### Hierarchical Relationships
- Parent-child nesting
- Self-referential structures
- Tree/graph patterns

### 3. Business Entity Extraction
- Infer entity names from keys
- Determine entity purpose from data
- Identify primary identifiers
- Extract validation hints from data patterns

### 4. Data Quality Analysis
- Missing required fields
- Inconsistent formats
- Outlier values
- Data completeness per entity

## Output Format

### Primary Output: `[output_path]/01-analysis/data-[name]-analysis.md`

```markdown
# Data Analysis: [Filename]

**Source File**: [Filename]
**Format**: [JSON/XML/YAML/TOML]
**Data Type**: [Entity/Collection/Config/API Spec]
**Record Count**: [If collection]
**Nesting Depth**: [Max depth]

---

## 📋 Data Overview

**Purpose**: [Inferred purpose of data]
**Domain**: [Business domain]
**Source System**: [If identifiable]
**Data Currency**: [If timestamps present]

---

## 📊 Schema Inference

### Entity: [Inferred Entity Name]
**Source Key**: [Root key or array name]
**Record Count**: [N records if collection]

| Field | Type | Required | Sample Values | Notes |
|-------|------|----------|---------------|-------|
| id | [string/number] | Yes | [Sample] | Primary Key |
| [field] | [Type] | [Y/N] | [Sample values] | [Notes] |

**Inferred Purpose**: [What this entity represents]

[Repeat for each distinct entity in data...]

---

## 🔗 Relationships Detected

### Relationship 1: [Entity A] → [Entity B]
**Type**: [1:1 / 1:N / N:N]
**Join Field**: [field_name]
**Evidence**: [How this was determined]

```
[Entity A]
    └──< [Entity B] (via [field])
```

---

## 📝 Enum Fields Detected

| Field | Entity | Possible Values | Notes |
|-------|--------|-----------------|-------|
| status | [Entity] | [value1, value2, ...] | [Meaning] |
| type | [Entity] | [value1, value2, ...] | [Meaning] |

---

## 🗃️ Data Dictionary

### [Entity Name]

| Field | Business Meaning | Example | Validation |
|-------|------------------|---------|------------|
| [field] | [What it means] | [Real example] | [Inferred rules] |

---

## 📈 Data Statistics

### Volume Analysis
| Entity | Count | Unique Values (Key Fields) |
|--------|-------|---------------------------|
| [Entity] | [N] | [Unique IDs] |

### Field Completeness
| Entity | Field | % Populated | % Null/Empty |
|--------|-------|-------------|--------------|
| [Entity] | [Field] | [%] | [%] |

---

## ⚠️ Data Quality Observations

| Issue | Location | Severity | Examples |
|-------|----------|----------|----------|
| [Issue type] | [Entity.field] | [High/Med/Low] | [Specific cases] |

### Common Issues Detected
- [ ] Inconsistent date formats
- [ ] Mixed case in enum values
- [ ] Orphan foreign keys
- [ ] Duplicate records
- [ ] Missing required fields

---

## 🔧 Configuration Analysis

*(If config file detected)*

| Setting | Value | Purpose | Environment-Specific |
|---------|-------|---------|---------------------|
| [Key] | [Value] | [Purpose] | [Yes/No] |

---

## 📡 API Specification Analysis

*(If OpenAPI/Swagger detected)*

| Endpoint | Method | Request Body | Response |
|----------|--------|--------------|----------|
| [/path] | [GET/POST] | [Schema ref] | [Schema ref] |

---

## 💼 Business Insights from Data

### Entity Volumes
- [Entity A]: [N] records - [Volume assessment]
- [Entity B]: [N] records - [Volume assessment]

### FK Control Implications
Based on volumes, recommended UI controls:
| Entity | Volume | Recommended Control |
|--------|--------|---------------------|
| [Entity] | ≤5 | Radio Buttons |
| [Entity] | 6-20 | Dropdown |
| [Entity] | >20 | Searchable Select |

### Data Relationships for Prototype
[How entities should be connected in sample data]

---

## 🏷️ Tags

`#data-analysis` `#[format]` `#[domain]` `#[entity-types]`

---

**Analysis Date**: [Date]
**Confidence Level**: [High/Medium/Low]
```

## Format-Specific Handling

### JSON
- Parse and validate JSON
- Handle nested structures
- Support JSON arrays
- Process JSONL (line-delimited)

### XML
- Extract from XML elements and attributes
- Handle namespaces
- Process nested elements
- Map XML to entity structure

### YAML
- Parse YAML syntax
- Handle anchors and aliases
- Process multi-document YAML
- Support complex types

### TOML
- Parse TOML tables
- Handle arrays of tables
- Process inline tables
- Map to configuration structure

## 🚨 ERROR HANDLING

> **STRICT RULE**: Follow the global error handling rules in `.claude/rules/error-handling.md`.

| Issue | Action |
|-------|--------|
| Invalid format | Log error, attempt partial parse |
| Large file (>10MB) | Sample first 1000 records/lines |
| Binary content | Skip binary fields |
| Circular refs | Break cycles |


## Integration Points

### Feeds Into
- `Discovery_SpecDataModel` - Entity definitions become data specs
- `Discovery_SpecSampleData` - Real data informs sample data generation
- `Discovery_ExtractMetrics` - Numeric data provides metrics

### Receives From
- `Discovery_Orchestrator` - Files and schema hints

---

**Skill Version**: 2.0
**Framework Compatibility**: Discovery Skills Framework v2.0
