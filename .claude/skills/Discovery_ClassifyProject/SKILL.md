---
name: classifying-project-type
description: Use when you need to classify a project type (FULL_STACK, BACKEND_ONLY, DATABASE_ONLY, INTEGRATION, INFRASTRUCTURE) to determine which artifacts apply and enable NOT_APPLICABLE handling.
model: haiku
allowed-tools: AskUserQuestion, Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill classifying-project-type started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill classifying-project-type ended '{"stage": "discovery"}'
---

# Classify Project Type

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill classifying-project-type instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Part of**: Smart Obsolescence Handling for Non-UI Projects

## Metadata
- **Skill ID**: Discovery_ClassifyProject
- **Version**: 1.0.0
- **Created**: 2025-12-26
- **Author**: AI Assistant
- **Change History**:
  - v1.0.0 (2025-12-26): Initial skill version for Smart Obsolescence Handling

## Description

Analyzes client materials and input signals to classify the project type. This classification determines which discovery artifacts are applicable and which should be marked as NOT_APPLICABLE.

**Role**: You are a Project Classification Specialist. Your expertise is analyzing client materials, code artifacts, and documentation to determine the type of project and which framework artifacts apply.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:classifying-project-type:started` - When skill begins
- `skill:classifying-project-type:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Project Types

| Type | Description | UI Required | Examples |
|------|-------------|-------------|----------|
| `FULL_STACK` | Complete frontend + backend application | Yes | Web apps, mobile apps, dashboards |
| `BACKEND_ONLY` | API/service layer only, no UI | No | REST APIs, microservices, batch processors |
| `DATABASE_ONLY` | Schema design, migrations, data modeling | No | Data warehouse, ETL pipelines, schema designs |
| `INTEGRATION` | Middleware, connectors, adapters | No | ESB, API gateways, data connectors |
| `INFRASTRUCTURE` | DevOps, IaC, platform engineering | No | Terraform configs, K8s manifests, CI/CD pipelines |

## Trigger Conditions

- Start of Discovery phase (after `/discovery-init`)
- User explicitly requests project classification
- Analyzing client materials to determine scope
- Before generating artifacts that may not be applicable

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Client Materials | Yes | Files in INPUT_PATH to analyze |
| System Name | Yes | Name of the system being analyzed |
| Override Reason | No | Manual override with justification |

## Signal Detection Patterns

### FULL_STACK Signals
- UI mockups, wireframes, or screenshots
- Design files (Figma, Sketch, XD)
- Frontend framework mentions (React, Angular, Vue)
- Screen flows, navigation diagrams
- CSS/SCSS files, style guides
- Mobile app references (iOS, Android)

### BACKEND_ONLY Signals
- API specifications (OpenAPI, Swagger, RAML)
- No UI mockups or design files
- Service-oriented terminology
- Microservices architecture mentions
- Queue/message broker references (Kafka, RabbitMQ)
- Backend-only frameworks (Spring Boot, Express.js APIs)

### DATABASE_ONLY Signals
- ER diagrams, schema files
- SQL scripts, migrations
- Data modeling terminology
- ETL processes
- Data warehouse mentions
- No application code references

### INTEGRATION Signals
- Connector specifications
- Message transformation rules
- Protocol adapters (SOAP, REST, GraphQL)
- ESB configuration
- Data mapping specifications
- API gateway configurations

### INFRASTRUCTURE Signals
- IaC files (Terraform, CloudFormation, Pulumi)
- Kubernetes manifests
- CI/CD pipeline definitions
- Container specifications (Dockerfile)
- Network/security configurations
- Platform engineering docs

## Classification Algorithm

```
1. Scan all files in INPUT_PATH
2. Extract signal keywords from:
   - File names and extensions
   - Directory structure
   - Document content (first 1000 chars)
3. Count signals per project type
4. Calculate confidence:
   - HIGH: > 5 signals, clear winner with 2x+ margin
   - MEDIUM: 3-5 signals, clear winner with 1.5x+ margin
   - LOW: < 3 signals OR no clear winner
5. Set project type to highest signal count
6. Default to FULL_STACK if LOW confidence
```

## Procedure

### Phase 1: Signal Collection

1. List all files in INPUT_PATH
2. For each file/folder:
   - Extract name, extension
   - Read first 1000 characters (if text file)
   - Log detected signals

### Phase 2: Signal Analysis

1. Count signals per project type
2. Calculate confidence level
3. Determine winning project type

### Phase 3: User Confirmation (when confidence < HIGH)

IF confidence != "HIGH":
  USE AskUserQuestion:
    question: "I detected this as a {detected_type} project with {confidence} confidence. Is this correct?"
    header: "Project Type"
    options:
      - label: "{detected_type} (Recommended)"
        description: "Based on signals: {top_signals}"
      - label: "FULL_STACK"
        description: "Complete frontend + backend application"
      - label: "BACKEND_ONLY"
        description: "API/service layer only, no UI screens"
      - label: "DATABASE_ONLY"
        description: "Schema design, migrations, data modeling"

  SET project_type = user_selection


### Phase 4: Update Configuration

1. Read `_state/discovery_config.json`
2. Update `project_classification` section:
   ```json
   {
     "type": "<PROJECT_TYPE>",
     "detected_at": "<ISO_TIMESTAMP>",
     "confidence": "<HIGH|MEDIUM|LOW>",
     "signals": ["<signal1>", "<signal2>", ...],
     "override_reason": null,
     "artifact_applicability": { ... }
   }
   ```
3. Set artifact_applicability based on ARTIFACT_APPLICABILITY matrix

### Phase 5: Report Generation

Generate classification report:

```markdown
# Project Classification Report

## Classification Result

- **Project Type**: BACKEND_ONLY
- **Confidence**: HIGH
- **Detected At**: 2025-12-26T10:30:00Z

## Detected Signals

| Signal | Type | Source |
|--------|------|--------|
| OpenAPI specification | BACKEND_ONLY | api-spec.yaml |
| No UI mockups found | BACKEND_ONLY | (absence signal) |
| Spring Boot project | BACKEND_ONLY | pom.xml |

## Artifact Applicability

| Artifact | Applicable | Reason |
|----------|------------|--------|
| screen-definitions | No | No UI in scope |
| navigation-structure | No | No UI in scope |
| data-fields | Yes | Data contracts needed |
| PERSONAS | Yes | Always applicable |
| PAIN_POINTS | Yes | Always applicable |
```

## Artifact Applicability Matrix

| Artifact | FULL_STACK | BACKEND_ONLY | DATABASE_ONLY | INTEGRATION | INFRASTRUCTURE |
|----------|------------|--------------|---------------|-------------|----------------|
| screen-definitions | Yes | No | No | No | No |
| navigation-structure | Yes | No | No | No | No |
| data-fields | Yes | Yes | Yes | Yes | No |
| interaction-patterns | Yes | No | No | No | No |
| ui-components | Yes | No | No | No | No |
| PERSONAS | Yes | Yes | Yes | Yes | Yes |
| JOBS_TO_BE_DONE | Yes | Yes | Yes | Yes | Yes |
| PRODUCT_VISION | Yes | Yes | Yes | Yes | Yes |
| PRODUCT_STRATEGY | Yes | Yes | Yes | Yes | Yes |
| PRODUCT_ROADMAP | Yes | Yes | Yes | Yes | Yes |
| KPIS_AND_GOALS | Yes | Yes | Yes | Yes | Yes |
| PAIN_POINTS | Yes | Yes | Yes | Yes | Yes |
| PDF_ANALYSIS | Yes | Yes | Yes | Yes | Yes |
| prototype-code | Yes | No | No | No | No |
| design-tokens | Yes | No | No | No | No |
| component-specs | Yes | No | No | No | No |

## Output Files

| File | Location | Description |
|------|----------|-------------|
| Classification in config | `_state/discovery_config.json#project_classification` | Updated configuration |
| Classification report | `<OUTPUT_PATH>/01-analysis/PROJECT_CLASSIFICATION_REPORT.md` | Detailed report |

## Manual Override

To manually override classification:

1. Update `_state/discovery_config.json`:
   ```json
   {
     "project_classification": {
       "type": "BACKEND_ONLY",
       "override_reason": "User confirmed no UI in scope",
       ...
     }
   }
   ```

2. Re-run validation to confirm applicability is correct

## Integration with Quality Gates

All quality gates now support N/A validation:

```bash
# Show current project classification
python3 .claude/hooks/discovery_quality_gates.py --show-classification

# Validate a NOT_APPLICABLE file
python3 .claude/hooks/discovery_quality_gates.py --validate-na-file <path>

# List all N/A artifacts
python3 .claude/hooks/discovery_quality_gates.py --list-na-artifacts --dir <path>
```

## Error Handling

| Error | Action |
|-------|--------|
| Cannot read file | Skip file, log signal, continue |
| Ambiguous signals | Default to FULL_STACK with LOW confidence |
| Config file missing | Create with default FULL_STACK classification |
| Invalid project type | Log error, use FULL_STACK |

## Dependencies

- `na_validation_utils.py` - Shared N/A validation utilities
- `discovery_config.json` - Discovery configuration file

## Related Skills

- `Discovery_AnalyzeDocument` - Initial material analysis
- `Discovery_Init` - Discovery initialization
