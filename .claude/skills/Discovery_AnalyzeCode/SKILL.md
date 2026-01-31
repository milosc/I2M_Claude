---
name: analyzing-source-code
description: Use when you need to extract architecture, data models, and business logic from source code files to understand an existing system.
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
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-source-code started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-source-code ended '{"stage": "discovery"}'
---

# Analyze Code

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill analyzing-source-code instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_AnalyzeCode
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for extracting product insights from source code files (Java, Python, JavaScript, TypeScript, C#, Go, etc.). Analyzes existing codebases to understand current architecture, data models, business logic, integrations, and technical debt relevant to product discovery and replacement/enhancement planning.

**Role**: You are a Code Analysis Specialist for Product Discovery. Your expertise is reverse-engineering product requirements from existing code, understanding data models, identifying technical constraints, and extracting business rules embedded in source code.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:analyzing-source-code:started` - When skill begins
- `skill:analyzing-source-code:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- User provides source code files for analysis
- Request mentions "analyze codebase", "understand current system", "code review for requirements"
- Context involves replacing or enhancing existing software
- Files with extensions: .java, .py, .js, .ts, .cs, .go, .rb, .php, .swift, .kt
- Need to understand what existing system does before replacement

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Code Files | Yes | Source code files or repository |
| Code Context | No | Purpose: current system, prototype, etc. |
| Focus Areas | No | Specific aspects to analyze |
| Output Path | Yes | Where to save analysis |

## Code Type Detection

### Auto-Classification Rules

| Pattern | Classification |
|---------|---------------|
| @Entity, models/, schema | Data Model Code |
| @Controller, routes/, endpoints | API/Controller Code |
| @Service, services/, business | Business Logic Code |
| @Repository, dao/, data access | Data Access Code |
| components/, views/, templates | UI Component Code |
| config/, settings, .env | Configuration Code |
| test/, spec/, __tests__ | Test Code |
| migrations/, schema changes | Database Migration |

## Extraction Framework

### 1. Architecture Analysis
- Identify architectural pattern (MVC, layered, microservices)
- Map module/package structure
- Detect frameworks and libraries used
- Identify entry points and controllers
- Note authentication/authorization patterns

### 2. Data Model Extraction

#### Entity Identification
- Class/model definitions
- Field names and types
- Relationships (1:1, 1:N, N:N)
- Validation rules in code
- Computed/derived fields

#### Database Schema Indicators
- ORM mappings (@Entity, models)
- Foreign key references
- Indexes mentioned
- Constraints (unique, not null)

### 3. Business Logic Extraction

#### Rules and Workflows
- Conditional logic (if/else chains)
- State transitions
- Calculation formulas
- Validation rules
- Business exceptions

#### Integration Points
- API calls to external services
- Event publishing/subscribing
- File imports/exports
- Email/notification triggers

### 4. Feature Extraction
- Routes/endpoints = Features
- UI components = User-facing features
- Batch jobs = Background features
- Reports/exports = Reporting features

### 5. Technical Debt Identification
- TODO/FIXME comments
- Deprecated code
- Duplicated logic
- Complex methods (high cyclomatic complexity)
- Missing error handling

## Output Format

### Primary Output: `[output_path]/01-analysis/code-[name]-analysis.md`

```markdown
# Code Analysis: [Project/File Name]

**Source**: [Path/Repository]
**Language(s)**: [Languages found]
**Framework(s)**: [Frameworks detected]
**Total Files Analyzed**: [Count]
**Lines of Code**: [Approximate]

---

## 📋 Architecture Overview

**Pattern**: [MVC/Layered/Microservices/Monolith]
**Structure**:
```
[Project Root]
├── [folder] - [Purpose]
├── [folder] - [Purpose]
└── [folder] - [Purpose]
```

**Entry Points**:
- [Main class/file]
- [API entry point]
- [UI entry point]

---

## 📊 Data Model Extracted

### Entity: [Entity Name]
**Purpose**: [What this entity represents]
**Source File**: [Path]

| Field | Type | Required | Constraints | Notes |
|-------|------|----------|-------------|-------|
| id | [Type] | Yes | Primary Key | |
| [field] | [Type] | [Y/N] | [Constraints] | [Notes] |

**Relationships**:
- Has Many: [Related entities]
- Belongs To: [Parent entities]
- Many-to-Many: [Associated entities]

[Repeat for each significant entity...]

---

## 🔄 Business Rules Extracted

### Rule Category: [Category Name]

#### Rule 1: [Rule Name]
**Source**: [File:Line]
**Condition**: [When this applies]
**Logic**: [What happens]
**Code Pattern**:
```[language]
[Simplified code snippet]
```
**Product Implication**: [What this means for requirements]

---

## 🔌 Integration Points

### External Services

| Service | Purpose | Method | Frequency |
|---------|---------|--------|-----------|
| [Service name] | [Purpose] | [REST/SOAP/etc] | [On-demand/Scheduled] |

### Events/Messages

| Event | Publisher | Subscribers | Payload |
|-------|-----------|-------------|---------|
| [Event name] | [Component] | [Listeners] | [Data sent] |

---

## 🛤️ API/Routes Inventory

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| [/path] | [GET/POST] | [Purpose] | [Yes/No] |

---

## 🖥️ UI Features Detected

| Component | Purpose | Data Required | Actions |
|-----------|---------|---------------|---------|
| [Component] | [Purpose] | [Data it displays] | [User actions] |

---

## ⚙️ Configuration & Environment

| Config Key | Purpose | Default | Notes |
|------------|---------|---------|-------|
| [Key] | [Purpose] | [Value] | [Environment-specific] |

---

## 🐛 Technical Debt Identified

### High Priority

| Issue | Location | Impact | Recommendation |
|-------|----------|--------|----------------|
| [Issue] | [File:Line] | [Impact] | [Fix suggestion] |

### TODO/FIXME Comments

| Comment | Location | Age (if known) |
|---------|----------|----------------|
| [Comment text] | [File:Line] | [If datable] |

---

## 📋 Feature Inventory (Inferred from Code)

| Feature | Implementation Location | Completeness | Notes |
|---------|------------------------|--------------|-------|
| [Feature name] | [Files/Classes] | [%] | [Observations] |

---

## 🔐 Security Observations

| Observation | Location | Severity | Notes |
|-------------|----------|----------|-------|
| [Observation] | [Where] | [High/Med/Low] | [Details] |

---

## 📊 Test Coverage Indicators

| Area | Test Files | Coverage Notes |
|------|------------|----------------|
| [Area] | [Test files] | [What's tested] |

---

## 🏷️ Tags

`#code-analysis` `#[language]` `#[framework]` `#[domain]`

---

**Analysis Date**: [Date]
**Confidence Level**: [High/Medium/Low]
**Completeness**: [% of codebase analyzed]
```

## Language-Specific Patterns

### Java
- Look for @Entity, @Service, @Controller annotations
- Extract from Spring/Jakarta EE patterns
- Map Hibernate relationships
- Identify REST endpoints from @RequestMapping

### Python
- Look for Django models, Flask routes
- Extract SQLAlchemy mappings
- Identify Celery tasks
- Map FastAPI endpoints

### JavaScript/TypeScript
- Look for React components, Express routes
- Extract Mongoose/Prisma schemas
- Identify Redux actions/reducers
- Map GraphQL resolvers

### C#/.NET
- Look for Entity Framework models
- Extract ASP.NET controllers
- Identify service interfaces
- Map dependency injection

## 🚨 ERROR HANDLING

> **STRICT RULE**: Follow the global error handling rules in `.claude/rules/error-handling.md`.

| Issue | Action |
|-------|--------|
| Syntax errors | Note error, analyze parseable parts |
| Binary/compiled | Skip (cannot analyze) |
| Large codebase | Sample key files only |


## Integration Points

### Feeds Into
- `Discovery_SpecDataModel` - Entity definitions become data specs
- `Discovery_ExtractWorkflows` - Business logic reveals workflows
- `Discovery_GenerateRoadmap` - Technical debt informs priorities

### Receives From
- `Discovery_Orchestrator` - Files and analysis priorities

---

**Skill Version**: 2.0
**Framework Compatibility**: Discovery Skills Framework v2.0
