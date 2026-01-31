---
name: exporting-to-jira
description: Use when you need to generate CSV and JSON files for importing Epics, Stories, and Sub-tasks into Jira from product specifications.
model: sonnet
allowed-tools: Read, Write, Edit, Bash
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill exporting-to-jira started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill exporting-to-jira ended '{"stage": "productspecs"}'
---

# Export to Jira

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill exporting-to-jira instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning
> **Supports**: Smart Obsolescence Handling for non-UI projects

## Metadata
- **Skill ID**: ProductSpecs_JiraExporter
- **Version**: 3.0.0
- **Created**: 2024-12-16
- **Updated**: 2025-12-26
- **Author**: Milos Cigoj
- **Change History**:
  - v3.0.0 (2025-12-26): Added NOT_APPLICABLE handling for non-UI projects with API-focused JIRA export
  - v2.1.0 (2025-12-23): Added automatic traceability propagation (Epic→JTBD, User Stories, Test Scenarios)
  - v2.0.0 (2025-12-22): Added state management hooks, checkpoint integration, shared _state/ folder support
  - v1.1.0 (2025-12-19): Updated metadata for consistency
  - v1.0.0 (2024-12-16): Initial release

---

# ProductSpecs_JiraExport - Jira Import Generator Skill

> **Version**: 2.0.0
> **Purpose**: Generate CSV and JSON files for importing Epics, Stories, and Sub-tasks into Jira
> **Input**: `ProductSpecs_<SystemName>/` with validated specifications
> **Output**: `ProductSpecs_<SystemName>/04-jira/` with CSV, JSON, and import guide
> **Phase**: 8 of ProductSpecs pipeline (Export)

---

## STATE MANAGEMENT INTEGRATION

### Shared State Files (at PROJECT ROOT)

This skill reads from shared state files:

| File | Location | Purpose |
|------|----------|---------|
| `productspecs_config.json` | `_state/` | System configuration |
| `productspecs_progress.json` | `_state/` | Phase tracking |

### ProductSpecs Registry Files

| File | Location | Purpose |
|------|----------|---------|
| `module_registry.json` | `traceability/` (ROOT) | Module index |
| `requirements_registry.json` | `traceability/` (ROOT) | Requirements |
| `productspecs_traceability_register.json` | `traceability/` (ROOT) | Traceability chains |
| `test_case_registry.json` | `traceability/` (ROOT) | Test specifications |

### JIRA Configuration

JIRA settings are collected at export time and stored in:

`ProductSpecs_<SystemName>/04-jira/jira_config.json`:

```json
{
  "project_key": "INV",
  "project_name": "Inventory Management System",
  "subtask_strategy": "by-discipline",
  "generate_subtasks": true,
  "configured_at": "ISO8601"
}
```

### Checkpoint Integration

This skill handles Checkpoint 8:

```bash
# Verify Checkpoint 7 passed
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 7 --dir ProductSpecs_<SystemName>/

# After export
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 8 --dir ProductSpecs_<SystemName>/
```

### Progress Updates

Update `_state/productspecs_progress.json`:

```python
progress["phases"]["export"]["status"] = "completed"
progress["phases"]["export"]["completed_at"] = timestamp
progress["phases"]["export"]["outputs"] = [
    "04-jira/full-hierarchy.csv",
    "04-jira/epics-and-stories.csv",
    "04-jira/subtasks-only.csv",
    "04-jira/jira-import.json",
    "04-jira/IMPORT_GUIDE.md"
]
progress["current_phase"] = 9  # Complete
```

---

## APPLICABILITY CHECK (Smart Obsolescence Handling)

**BEFORE generating JIRA export**, check project classification:

```
1. Read _state/productspecs_config.json
2. Check project_type from upstream (inherited from Discovery/Prototype)
3. IF project_type IN [BACKEND_ONLY, DATABASE_ONLY, INTEGRATION, INFRASTRUCTURE]:
   → Generate API-focused JIRA items only
   → Skip UI-specific sub-tasks ([FE], [A11Y] visual tasks)
   → Adjust sub-task strategy for API work
4. IF project_type == FULL_STACK:
   → Proceed with normal JIRA export (all sub-task types)
```

### Sub-task Strategy Adjustments by Project Type

| Sub-task Type | FULL_STACK | BACKEND_ONLY | DATABASE_ONLY | INTEGRATION |
|---------------|------------|--------------|---------------|-------------|
| `[FE]` Frontend | ✅ | ❌ Skip | ❌ Skip | ❌ Skip |
| `[BE]` Backend | ✅ | ✅ | ❌ Skip | ✅ |
| `[DATA]` Database | ✅ | ✅ | ✅ | ✅ |
| `[TEST]` Testing | ✅ | ✅ | ✅ | ✅ |
| `[A11Y]` Accessibility | ✅ | ❌ Skip | ❌ Skip | ❌ Skip |
| `[INT]` Integration | ✅ | ✅ | ✅ | ✅ |
| `[DOCS]` Documentation | ✅ | ✅ | ✅ | ✅ |
| `[REVIEW]` Review | ✅ | ✅ | ✅ | ✅ |

### API-Focused Story Format

When `ui_artifacts_applicable == false`, adjust story format:

```markdown
**Standard (FULL_STACK):**
"As a [persona], I want to [action on UI] so that [benefit]"

**API-Focused (BACKEND_ONLY/INTEGRATION):**
"As an API consumer, I want to [API action] so that [integration benefit]"

**Database-Focused (DATABASE_ONLY):**
"As a data engineer, I want to [data operation] so that [data integrity benefit]"
```

### Modified Sub-task Generation for Non-UI Projects

```
FUNCTION generateDisciplineSubtasks(story, project_type):
  subtasks = []
  meta = story._meta

  // ===== BACKEND/API Sub-tasks (always applicable for BACKEND_ONLY/INTEGRATION) =====
  IF project_type IN [FULL_STACK, BACKEND_ONLY, INTEGRATION]:
    IF meta.api_endpoints.length > 0:
      subtasks.push({
        "summary": "[BE] Implement API endpoints for {story.req_id}",
        "issueType": "Sub-task",
        "description": buildBackendSubtaskDescription(meta),
        "labels": ["backend", "api"],
        "originalEstimate": estimateBackendWork(meta)
      })

  // ===== DATABASE Sub-tasks (always applicable for DATABASE_ONLY) =====
  IF project_type IN [FULL_STACK, BACKEND_ONLY, DATABASE_ONLY, INTEGRATION]:
    IF meta.data_operations.length > 0:
      subtasks.push({
        "summary": "[DATA] Implement data layer for {story.req_id}",
        "issueType": "Sub-task",
        "description": buildDataLayerDescription(meta),
        "labels": ["database", "data"],
        "originalEstimate": estimateDataWork(meta)
      })

  // ===== FRONTEND Sub-tasks (SKIP for non-UI projects) =====
  IF project_type == FULL_STACK:
    IF meta.ui_components.length > 0:
      subtasks.push({
        "summary": "[FE] Implement {story.screen_id} components",
        "issueType": "Sub-task",
        "description": buildFrontendSubtaskDescription(meta),
        "labels": ["frontend"],
        "originalEstimate": estimateFrontendWork(meta)
      })

  // ===== INTEGRATION Sub-tasks (applicable for INTEGRATION projects) =====
  IF project_type IN [INTEGRATION, BACKEND_ONLY]:
    IF meta.external_systems.length > 0:
      subtasks.push({
        "summary": "[INT] Implement integration with {external_system}",
        "issueType": "Sub-task",
        "description": buildIntegrationDescription(meta),
        "labels": ["integration", "external"],
        "originalEstimate": estimateIntegrationWork(meta)
      })

  // ===== TESTING Sub-tasks (always applicable, adjusted scope) =====
  subtasks.push({
    "summary": "[TEST] Write unit tests for {story.req_id}",
    "issueType": "Sub-task",
    "description": buildUnitTestDescription(story, project_type),
    "labels": ["testing", "unit-test"],
    "originalEstimate": "2h"
  })

  // Integration tests (for API/DB projects)
  IF project_type IN [BACKEND_ONLY, DATABASE_ONLY, INTEGRATION]:
    subtasks.push({
      "summary": "[TEST] Write integration tests for {story.req_id}",
      "issueType": "Sub-task",
      "description": buildIntegrationTestDescription(story),
      "labels": ["testing", "integration-test"],
      "originalEstimate": "3h"
    })

  // E2E tests for P0 (adjusted for project type)
  IF story.priority == "Highest":
    IF project_type == FULL_STACK:
      subtasks.push({
        "summary": "[TEST] Write E2E test for {story.req_id}",
        ...
      })
    ELSE:
      subtasks.push({
        "summary": "[TEST] Write API E2E test for {story.req_id}",
        "issueType": "Sub-task",
        "description": buildAPIE2ETestDescription(story),
        "labels": ["testing", "api-test", "e2e"],
        "originalEstimate": "3h"
      })

  // ===== ACCESSIBILITY Sub-tasks (SKIP for non-UI projects) =====
  IF project_type == FULL_STACK:
    IF meta.has_accessibility:
      subtasks.push({
        "summary": "[A11Y] Verify accessibility for {story.screen_id}",
        ...
      })

  // ===== DOCUMENTATION Sub-tasks (always applicable) =====
  subtasks.push({
    "summary": "[DOCS] Update documentation for {story.req_id}",
    "issueType": "Sub-task",
    "description": buildDocsDescription(story, project_type),
    "labels": ["documentation"],
    "originalEstimate": "1h"
  })

  // ===== REVIEW Sub-tasks (always applicable) =====
  subtasks.push({
    "summary": "[REVIEW] Code review and sign-off",
    "issueType": "Sub-task",
    "description": buildReviewDescription(story, project_type),
    "labels": ["review"],
    "originalEstimate": "1h"
  })

  RETURN subtasks
```

### Export Summary for Non-UI Projects

When generating JIRA export for non-UI projects, include project type note:

```markdown
## Export Summary

| Metric | Value |
|--------|-------|
| **Project Type** | BACKEND_ONLY |
| **UI Artifacts** | Not Applicable |
| **Total Epics** | {count} |
| **Total Stories** | {count} |
| **Total Sub-tasks** | {count} |

### Sub-task Distribution (API-Focused)

| Type | Count | Notes |
|------|-------|-------|
| [BE] Backend | {count} | API endpoint implementation |
| [DATA] Database | {count} | Data layer operations |
| [INT] Integration | {count} | External system integration |
| [TEST] Testing | {count} | Unit + Integration + API E2E |
| [DOCS] Documentation | {count} | API documentation |
| [REVIEW] Review | {count} | Code review |
| **[FE] Frontend** | **0** | *Skipped - not applicable* |
| **[A11Y] Accessibility** | **0** | *Skipped - not applicable* |
```

### IMPORT_GUIDE.md Adjustments

When generating import guide for non-UI projects:

```markdown
## Project Type: {PROJECT_TYPE}

> **Note**: This export was generated for a **{PROJECT_TYPE}** project.
> UI-related items (frontend components, accessibility tasks) have been excluded
> as they are not applicable to this project type.

### Included Work Items

- API endpoint implementation tasks
- Database/data layer tasks
- Integration tasks
- Testing tasks (unit, integration, API E2E)
- Documentation tasks
- Review tasks

### Excluded Work Items (Not Applicable)

- Frontend component tasks
- UI accessibility tasks
- UI-focused E2E tests
```

---

## SKILL OVERVIEW

This skill transforms production specifications into Jira-importable formats:

- **Epics** = Modules (MOD-xxx)
- **Stories** = User Stories and Functional Requirements (US-xxx, FR-xxx)
- **Sub-tasks** = Breakdown of implementation work (frontend, backend, testing, docs)

Each Story description is enriched with:
- Acceptance criteria (Gherkin format)
- Related screens and components
- testIDs for QA automation
- NFR references
- Traceability links

Sub-tasks provide actionable work items for:
- Frontend component implementation
- Backend API integration
- Unit/Integration/E2E testing
- Documentation updates

---

## INPUTS REQUIRED

```
SPECS_PATH: {path to generated product specs folder}
  Required files:
  ├── MASTER_DEVELOPMENT_PLAN.md    # Module registry, traceability matrix
  ├── modules/
  │   ├── MOD-xxx-01.md             # Module specs with Gherkin scenarios
  │   └── ...

REGISTRY_PATH: traceability/ (ROOT level - single source of truth)
  Required files:
  ├── module_registry.json          # Module index
  ├── requirements_registry.json    # Requirements registry
  └── productspecs_traceability_register.json  # Full trace matrix

PROJECT_KEY: {Jira project key, e.g., "INV", "ATS"}
PROJECT_NAME: {Jira project name, e.g., "Inventory Management"}

OPTIONS:
  GENERATE_SUBTASKS: true|false (default: true)
  SUBTASK_STRATEGY: "by-discipline"|"by-component"|"by-acceptance-criteria"|"comprehensive"

OUTPUT_PATH: {path for export files}
  Will create:
  └── jira-export/
      ├── epics-and-stories.csv       # Epics + Stories (no sub-tasks)
      ├── full-hierarchy.csv          # Epics + Stories + Sub-tasks
      ├── subtasks-only.csv           # Sub-tasks for separate import
      ├── jira-import.json            # JSON format for admins
      └── IMPORT_GUIDE.md             # Step-by-step import instructions
```

---

## SUB-TASK STRATEGIES

### Strategy 1: By Discipline (Default)

Creates sub-tasks based on development disciplines:

| Sub-task Type | Template | Assigned To |
|---------------|----------|-------------|
| `[FE]` Frontend | Implement UI components | Frontend Dev |
| `[BE]` Backend | Implement API endpoints | Backend Dev |
| `[TEST]` Testing | Write automated tests | QA Engineer |
| `[DOCS]` Documentation | Update documentation | Tech Writer |
| `[REVIEW]` Review | Code review & QA sign-off | Team Lead |

**Example for US-001:**
```
US-001: Search and select items quickly
  ├── [FE] Implement ItemSearchScreen components
  ├── [BE] Implement GET /api/items search endpoint
  ├── [TEST] Write unit tests for ItemSearchScreen
  ├── [TEST] Write E2E test for search flow
  └── [DOCS] Update API documentation for /api/items
```

### Strategy 2: By Component

Creates sub-tasks for each UI component in the Story:

**Example for US-001:**
```
US-001: Search and select items quickly
  ├── [FE] Implement input_item_search component
  ├── [FE] Implement btn_scan_barcode component
  ├── [FE] Implement card_item_{id} component
  ├── [FE] Implement skeleton_results loading state
  └── [FE] Implement empty_no_results state
```

### Strategy 3: By Acceptance Criteria

Creates sub-tasks for each Gherkin scenario:

**Example for US-001:**
```
US-001: Search and select items quickly
  ├── [AC] Search by item code returns matching items
  ├── [AC] Search by item name (partial match)
  ├── [AC] Search by barcode scan
  └── [AC] Loading state feedback
```

### Strategy 4: Comprehensive

Combines all strategies for maximum granularity:

**Example for US-001:**
```
US-001: Search and select items quickly
  ├── [FE] Implement ItemSearchScreen layout
  ├── [FE] Implement input_item_search with debounce
  ├── [FE] Implement barcode scanner integration
  ├── [FE] Implement ItemCard component
  ├── [FE] Implement loading/empty/error states
  ├── [BE] Implement GET /api/items search endpoint
  ├── [BE] Add search indexing for item code/name
  ├── [TEST] Unit: ItemSearchScreen renders correctly
  ├── [TEST] Unit: Search debounce works (300ms)
  ├── [TEST] Integration: API returns filtered results
  ├── [TEST] E2E: Search by item code returns matching items
  ├── [TEST] E2E: Search by barcode scan
  ├── [A11Y] Verify keyboard navigation
  ├── [A11Y] Verify screen reader compatibility
  └── [DOCS] Update search API documentation
```

---

## OUTPUT FORMATS

### CSV Format

**Columns for Full Hierarchy:**
| Column | Required | Description |
|--------|----------|-------------|
| Summary | Yes | Issue title |
| Issue Type | Yes | "Epic", "Story", or "Sub-task" |
| Description | Yes | Rich markdown description |
| Epic Name | Epic only | Unique epic identifier |
| Epic Link | Story only | References Epic Name |
| Parent | Sub-task only | References parent Story Summary |
| Priority | No | P0→Highest, P1→High, P2→Medium |
| Labels | No | Tags for filtering |
| Story Points | Story only | Complexity estimate |
| Original Estimate | Sub-task only | Time estimate (e.g., "2h", "4h") |
| Component/s | No | Jira component assignment |
| Assignee | No | Team member (if known) |

### JSON Format

```json
{
  "projects": [{
    "name": "Project Name",
    "key": "PROJ",
    "issues": [
      { "issueType": "Epic", ... },
      { 
        "issueType": "Story",
        "subtasks": [
          { "issueType": "Sub-task", ... }
        ]
      }
    ]
  }]
}
```

---

## EXECUTION PHASES

### Phase 1: EXTRACT - Parse Specifications
### Phase 2: TRANSFORM - Build Jira Structures
### Phase 3: GENERATE_SUBTASKS - Create Sub-task Breakdown
### Phase 4: OUTPUT - Create CSV and JSON Files
### Phase 5: VALIDATE - Verify Import Readiness
### Phase 6: PROPAGATE_TRACEABILITY - Update ROOT Registries (AUTOMATIC)

---

## PHASE 1: EXTRACT

### Step 1.1: Load Module Registry

```
READ: traceability/module_registry.json  # ROOT level - single source of truth

EXTRACT:
  - product_name
  - modules[] with:
    - id (MOD-xxx)
    - name
    - priority
    - screens[]
    - requirements[]
```

### Step 1.2: Load Module Specifications

```
FOR EACH module in program.modules:
  
  READ: {SPECS_PATH}/modules/{module.id}.md
  
  PARSE with regex/structured extraction:
    - Module metadata (ID, name, owner)
    - Trace map (CM, PP, JTBD references)
    - Screens[] with:
      - Screen ID
      - User stories with Gherkin
      - UI Component Dictionary (testIDs)
      - Data Requirements (API endpoints)
    - NFRs[]
    - Security policies[]
  
  STORE → extracted.modules[module.id]
```

### Step 1.3: Build Requirement Index

```
FOR EACH module in extracted.modules:
  FOR EACH screen in module.screens:
    FOR EACH user_story in screen.user_stories:
      
      EXTRACT:
        - req_id (US-xxx, FR-xxx)
        - title
        - priority
        - persona
        - gherkin_scenarios[]
        - ui_components[] with testIDs
        - api_endpoints[]
        - related_nfrs[]
      
      STORE → extracted.requirements[req_id]
```

---

## PHASE 2: TRANSFORM

### Step 2.1: Create Epic Records

```
FOR EACH module in extracted.modules:
  
  CREATE epic:
    {
      "summary": "{module.name}",
      "issueType": "Epic",
      "epicName": "{module.id}",
      "externalId": "{module.id}",
      "priority": mapPriority(module.priority),
      "labels": [module.app_id, module.priority],
      "description": buildEpicDescription(module)
    }
  
  STORE → jira.epics[]
```

### Step 2.2: Create Story Records

```
FOR EACH requirement in extracted.requirements:
  
  CREATE story:
    {
      "summary": "{req_id}: {title}",
      "issueType": "Story",
      "epicLink": "{parent_module.id}",
      "externalId": "{req_id}",
      "priority": mapPriority(requirement.priority),
      "labels": [requirement.screen_id, requirement.priority],
      "storyPoints": estimatePoints(requirement),
      "description": buildStoryDescription(requirement),
      "acceptanceCriteria": formatGherkin(requirement.gherkin_scenarios),
      
      // Data for sub-task generation
      "_meta": {
        "ui_components": requirement.ui_components,
        "api_endpoints": requirement.api_endpoints,
        "gherkin_scenarios": requirement.gherkin_scenarios,
        "screen_id": requirement.screen_id,
        "has_accessibility": requirement.related_nfrs.includes("A11Y"),
        "has_security": requirement.has_security_requirements
      }
    }
  
  STORE → jira.stories[]
```

---

## PHASE 3: GENERATE_SUBTASKS

### Step 3.1: Apply Sub-task Strategy

```
FOR EACH story in jira.stories:
  
  SWITCH SUBTASK_STRATEGY:
    
    "by-discipline":
      subtasks = generateDisciplineSubtasks(story)
    
    "by-component":
      subtasks = generateComponentSubtasks(story)
    
    "by-acceptance-criteria":
      subtasks = generateACSubtasks(story)
    
    "comprehensive":
      subtasks = generateComprehensiveSubtasks(story)
  
  story.subtasks = subtasks
```

### Step 3.2: Generate Discipline-Based Sub-tasks

```
FUNCTION generateDisciplineSubtasks(story):
  subtasks = []
  meta = story._meta
  
  // Frontend Sub-task
  IF meta.ui_components.length > 0:
    subtasks.push({
      "summary": "[FE] Implement {story.screen_id} components",
      "issueType": "Sub-task",
      "description": buildFrontendSubtaskDescription(meta),
      "labels": ["frontend"],
      "originalEstimate": estimateFrontendWork(meta),
      "component": "Frontend"
    })
  
  // Backend Sub-task
  IF meta.api_endpoints.length > 0:
    subtasks.push({
      "summary": "[BE] Implement API endpoints for {story.req_id}",
      "issueType": "Sub-task", 
      "description": buildBackendSubtaskDescription(meta),
      "labels": ["backend"],
      "originalEstimate": estimateBackendWork(meta),
      "component": "Backend"
    })
  
  // Unit Test Sub-task
  subtasks.push({
    "summary": "[TEST] Write unit tests for {story.req_id}",
    "issueType": "Sub-task",
    "description": buildUnitTestDescription(story),
    "labels": ["testing", "unit-test"],
    "originalEstimate": "2h",
    "component": "QA"
  })
  
  // E2E Test Sub-task (for P0 stories)
  IF story.priority == "Highest":
    subtasks.push({
      "summary": "[TEST] Write E2E test for {story.req_id}",
      "issueType": "Sub-task",
      "description": buildE2ETestDescription(story),
      "labels": ["testing", "e2e-test"],
      "originalEstimate": "3h",
      "component": "QA"
    })
  
  // Accessibility Sub-task (if applicable)
  IF meta.has_accessibility:
    subtasks.push({
      "summary": "[A11Y] Verify accessibility for {story.screen_id}",
      "issueType": "Sub-task",
      "description": buildA11yDescription(story),
      "labels": ["accessibility"],
      "originalEstimate": "1h",
      "component": "QA"
    })
  
  // Documentation Sub-task (for API-heavy stories)
  IF meta.api_endpoints.length > 0:
    subtasks.push({
      "summary": "[DOCS] Update API documentation",
      "issueType": "Sub-task",
      "description": "Update API docs for endpoints: " + meta.api_endpoints.join(", "),
      "labels": ["documentation"],
      "originalEstimate": "1h",
      "component": "Documentation"
    })
  
  // Code Review Sub-task
  subtasks.push({
    "summary": "[REVIEW] Code review and QA sign-off",
    "issueType": "Sub-task",
    "description": buildReviewDescription(story),
    "labels": ["review"],
    "originalEstimate": "1h",
    "component": "QA"
  })
  
  RETURN subtasks
```

### Step 3.3: Generate Component-Based Sub-tasks

```
FUNCTION generateComponentSubtasks(story):
  subtasks = []
  meta = story._meta
  
  FOR EACH component in meta.ui_components:
    subtasks.push({
      "summary": "[FE] Implement {component.testID} ({component.type})",
      "issueType": "Sub-task",
      "description": buildComponentDescription(component),
      "labels": ["frontend", "component"],
      "originalEstimate": estimateComponentWork(component),
      "component": "Frontend"
    })
  
  RETURN subtasks
```

### Step 3.4: Generate AC-Based Sub-tasks

```
FUNCTION generateACSubtasks(story):
  subtasks = []
  
  FOR EACH scenario in story._meta.gherkin_scenarios:
    subtasks.push({
      "summary": "[AC] {scenario.name}",
      "issueType": "Sub-task",
      "description": buildACDescription(scenario),
      "labels": ["acceptance-criteria", scenario.priority],
      "originalEstimate": "2h",
      "component": "Development"
    })
  
  RETURN subtasks
```

### Step 3.5: Generate Comprehensive Sub-tasks

```
FUNCTION generateComprehensiveSubtasks(story):
  subtasks = []
  meta = story._meta
  
  // --- FRONTEND TASKS ---
  
  // Screen layout
  subtasks.push({
    "summary": "[FE] Implement {story.screen_id} layout and routing",
    "issueType": "Sub-task",
    "description": "Set up screen component, routing, and basic layout structure.",
    "labels": ["frontend", "layout"],
    "originalEstimate": "2h"
  })
  
  // Individual components
  FOR EACH component in meta.ui_components:
    IF component.type IN ["Input", "Select", "Button", "Card"]:
      subtasks.push({
        "summary": "[FE] Implement {component.testID}",
        "issueType": "Sub-task",
        "description": buildComponentDescription(component),
        "labels": ["frontend", "component"],
        "originalEstimate": estimateComponentWork(component)
      })
  
  // State management
  subtasks.push({
    "summary": "[FE] Implement state management for {story.screen_id}",
    "issueType": "Sub-task",
    "description": "Set up React state/context, loading states, error handling.",
    "labels": ["frontend", "state"],
    "originalEstimate": "2h"
  })
  
  // --- BACKEND TASKS ---
  
  FOR EACH endpoint in meta.api_endpoints:
    subtasks.push({
      "summary": "[BE] Implement {endpoint.method} {endpoint.path}",
      "issueType": "Sub-task",
      "description": buildEndpointDescription(endpoint),
      "labels": ["backend", "api"],
      "originalEstimate": estimateEndpointWork(endpoint)
    })
  
  // --- TESTING TASKS ---
  
  // Unit tests per component
  subtasks.push({
    "summary": "[TEST] Unit tests for {story.screen_id} components",
    "issueType": "Sub-task",
    "description": buildUnitTestDescription(story),
    "labels": ["testing", "unit-test"],
    "originalEstimate": "3h"
  })
  
  // Integration tests
  IF meta.api_endpoints.length > 0:
    subtasks.push({
      "summary": "[TEST] Integration tests for API calls",
      "issueType": "Sub-task",
      "description": "Test API integration with mock server.",
      "labels": ["testing", "integration-test"],
      "originalEstimate": "2h"
    })
  
  // E2E tests per scenario
  FOR EACH scenario in meta.gherkin_scenarios:
    IF scenario.priority == "P0":
      subtasks.push({
        "summary": "[TEST] E2E: {scenario.name}",
        "issueType": "Sub-task",
        "description": formatGherkinScenario(scenario),
        "labels": ["testing", "e2e-test"],
        "originalEstimate": "2h"
      })
  
  // --- ACCESSIBILITY TASKS ---
  
  IF meta.has_accessibility:
    subtasks.push({
      "summary": "[A11Y] Keyboard navigation verification",
      "issueType": "Sub-task",
      "description": "Verify all elements reachable via Tab, actions via Enter/Space.",
      "labels": ["accessibility"],
      "originalEstimate": "1h"
    })
    
    subtasks.push({
      "summary": "[A11Y] Screen reader compatibility",
      "issueType": "Sub-task",
      "description": "Test with VoiceOver/NVDA, verify ARIA labels.",
      "labels": ["accessibility"],
      "originalEstimate": "1h"
    })
    
    subtasks.push({
      "summary": "[A11Y] axe-core automated scan",
      "issueType": "Sub-task",
      "description": "Run axe-core, fix any violations to achieve 0 errors.",
      "labels": ["accessibility"],
      "originalEstimate": "1h"
    })
  
  // --- DOCUMENTATION ---
  
  subtasks.push({
    "summary": "[DOCS] Update component documentation",
    "issueType": "Sub-task",
    "description": "Document props, usage examples, testIDs for new components.",
    "labels": ["documentation"],
    "originalEstimate": "1h"
  })
  
  // --- REVIEW ---
  
  subtasks.push({
    "summary": "[REVIEW] Code review",
    "issueType": "Sub-task",
    "description": buildReviewDescription(story),
    "labels": ["review"],
    "originalEstimate": "1h"
  })
  
  subtasks.push({
    "summary": "[REVIEW] QA sign-off",
    "issueType": "Sub-task",
    "description": "QA verification of all acceptance criteria before closing.",
    "labels": ["review", "qa"],
    "originalEstimate": "1h"
  })
  
  RETURN subtasks
```

---

## PHASE 4: OUTPUT

### Step 4.1: Generate Full Hierarchy CSV

```
WRITE: {OUTPUT_PATH}/jira-export/full-hierarchy.csv

HEADER:
Summary,Issue Type,Description,Epic Name,Epic Link,Parent,Priority,Labels,Story Points,Original Estimate,Component/s

ROWS:
# First, all Epics
FOR EACH epic in jira.epics:
  "{epic.summary}","Epic","{epic.description}","{epic.epicName}","","","{epic.priority}","{epic.labels}","","",""

# Then, Stories with their Sub-tasks
FOR EACH story in jira.stories:
  # Story row
  "{story.summary}","Story","{story.description}","","{story.epicLink}","","{story.priority}","{story.labels}","{story.storyPoints}","",""
  
  # Sub-task rows
  FOR EACH subtask in story.subtasks:
    "{subtask.summary}","Sub-task","{subtask.description}","","","{story.summary}","","{subtask.labels}","","{subtask.originalEstimate}","{subtask.component}"
```

### Step 4.2: Generate Separate CSVs

```
WRITE: {OUTPUT_PATH}/jira-export/epics-and-stories.csv
  # Only Epics and Stories (for first import)

WRITE: {OUTPUT_PATH}/jira-export/subtasks-only.csv
  # Only Sub-tasks with Parent references (for second import after Stories exist)
```

### Step 4.3: Generate JSON

```
WRITE: {OUTPUT_PATH}/jira-export/jira-import.json

{
  "projects": [
    {
      "name": "{PROJECT_NAME}",
      "key": "{PROJECT_KEY}",
      "issues": [
        // Epics
        {
          "summary": "{epic.summary}",
          "issueType": "Epic",
          "externalId": "{epic.externalId}",
          ...
        },
        // Stories with nested subtasks
        {
          "summary": "{story.summary}",
          "issueType": "Story",
          "externalId": "{story.externalId}",
          ...
          "subtasks": [
            {
              "summary": "{subtask.summary}",
              "issueType": "Sub-task",
              "externalId": "{story.externalId}-ST-{N}",
              ...
            }
          ]
        }
      ]
    }
  ]
}
```

---

## SUB-TASK DESCRIPTION TEMPLATES

### Frontend Sub-task Description

```markdown
h2. Implementation Scope

Implement the following UI components for {screen_id}:

|| Component || testID || Type || Notes ||
{FOR EACH component}
| {name} | {testID} | {type} | {notes} |

h2. Technical Requirements

* Use design tokens from DESIGN_TOKENS.md
* Follow component patterns from 01-components/
* Implement all states: default, loading, error, empty

h2. testID Checklist

* [ ] {testID_1} implemented
* [ ] {testID_2} implemented
...

h2. Definition of Done

* [ ] All testIDs match specification
* [ ] Storybook stories created
* [ ] Responsive on mobile/tablet/desktop
* [ ] No TypeScript errors
```

### Backend Sub-task Description

```markdown
h2. API Endpoints to Implement

|| Method || Path || Description ||
{FOR EACH endpoint}
| {method} | {path} | {description} |

h2. Request/Response

See module spec for detailed schemas.

h2. Implementation Notes

* Follow OpenAPI spec in api-contracts/openapi.yaml
* Implement validation per schema
* Return appropriate error codes

h2. Definition of Done

* [ ] Endpoint responds correctly
* [ ] Validation works per spec
* [ ] Error responses match spec
* [ ] Unit tests pass
```

### Unit Test Sub-task Description

```markdown
h2. Test Coverage Target

80% coverage for {screen_id} components.

h2. Test Scenarios

{FOR EACH component}
* {component_name}:
  * [ ] Renders correctly with default props
  * [ ] Handles loading state
  * [ ] Handles error state
  * [ ] User interactions work correctly

h2. testID Usage

Use the following testIDs for element selection:
{code}
screen.getByTestId('input_item_search')
screen.getByTestId('btn_submit')
{code}

h2. Definition of Done

* [ ] All test scenarios pass
* [ ] Coverage >= 80%
* [ ] No flaky tests
```

### E2E Test Sub-task Description

```markdown
h2. Gherkin Scenario

{code:title=Gherkin}
{full_gherkin_scenario}
{code}

h2. Playwright Implementation

{code:language=typescript}
test('{scenario_name}', async ({ page }) => {
  // Given
  await page.goto('/path');
  
  // When
  await page.getByTestId('{testID}').click();
  
  // Then
  await expect(page.getByTestId('{result_testID}')).toBeVisible();
});
{code}

h2. Definition of Done

* [ ] Test passes locally
* [ ] Test passes in CI
* [ ] No flaky behavior
```

### Accessibility Sub-task Description

```markdown
h2. WCAG Criteria to Verify

* 2.1.1 Keyboard - All functions via keyboard
* 2.4.7 Focus Visible - Focus indicator visible
* 1.3.1 Info & Relationships - Proper labeling
* 4.1.2 Name, Role, Value - ARIA attributes correct

h2. Verification Checklist

* [ ] Tab through all elements in logical order
* [ ] Enter/Space activates buttons
* [ ] Focus ring visible (3px, high contrast)
* [ ] All inputs have labels
* [ ] Error messages announced to screen reader
* [ ] axe-core scan: 0 violations

h2. Tools

* axe-core browser extension
* VoiceOver (Mac) or NVDA (Windows)
* Keyboard only navigation

h2. Definition of Done

* [ ] All WCAG criteria verified
* [ ] axe-core: 0 violations
* [ ] Manual keyboard test pass
```

### Review Sub-task Description

```markdown
h2. Code Review Checklist

* [ ] Code follows team conventions
* [ ] No TypeScript errors or warnings
* [ ] Components properly typed
* [ ] Error handling in place
* [ ] Loading states implemented
* [ ] testIDs match specification

h2. QA Verification

* [ ] All acceptance criteria demonstrated
* [ ] Edge cases handled
* [ ] Responsive design verified
* [ ] Cross-browser tested (Chrome, Firefox, Safari)

h2. Sign-off Required From

* [ ] Tech Lead (code quality)
* [ ] QA Engineer (functionality)
* [ ] UX Designer (visual alignment with prototype)
```

---

## TIME ESTIMATION RULES

### Frontend Estimates

```
FUNCTION estimateFrontendWork(meta):
  hours = 0
  
  FOR EACH component in meta.ui_components:
    SWITCH component.type:
      "Input", "Button", "Select" → hours += 0.5
      "Card", "Table" → hours += 1
      "Modal", "Form" → hours += 2
      "Chart", "Map" → hours += 3
      DEFAULT → hours += 1
  
  // Add time for state management
  hours += 2
  
  // Add time for responsive design
  hours += 1
  
  RETURN formatEstimate(hours)  // "4h" or "1d"
```

### Backend Estimates

```
FUNCTION estimateBackendWork(meta):
  hours = 0
  
  FOR EACH endpoint in meta.api_endpoints:
    SWITCH endpoint.method:
      "GET" (simple) → hours += 1
      "GET" (with search/filter) → hours += 2
      "POST", "PUT" → hours += 2
      "DELETE" → hours += 1
  
  // Add time for validation
  hours += 1
  
  // Add time for error handling
  hours += 1
  
  RETURN formatEstimate(hours)
```

### Component Estimates

```
FUNCTION estimateComponentWork(component):
  SWITCH component.type:
    "Button" → "30m"
    "Input" → "1h"
    "Select" → "1h"
    "Card" → "2h"
    "Table" → "3h"
    "Modal" → "2h"
    "Form" → "3h"
    "Chart" → "4h"
    DEFAULT → "1h"
```

---

## PHASE 6: PROPAGATE_TRACEABILITY (AUTOMATIC - NO USER PROMPTS)

> **CRITICAL**: This phase runs AUTOMATICALLY after validation. DO NOT ask the user for confirmation.

### Step 6.1: Build JTBD → Epic Mapping

```
FOR EACH epic in jira.epics:

  // Find JTBDs linked to this epic's module
  module = getModule(epic.externalId)
  jtbds = []

  FOR EACH requirement in module.requirements:
    IF requirement.jtbd_refs:
      jtbds.append(requirement.jtbd_refs)

  // Create mapping
  jtbd_epic_map[epic.externalId] = {
    "epic_id": epic.externalId,
    "epic_name": epic.summary,
    "jira_key": "{PROJECT_KEY}-EPIC-{N}",  // Placeholder until Jira assigns
    "jtbd_ids": unique(jtbds)
  }
```

### Step 6.2: Build User Story Registry

```
user_story_registry = {
  "schema_version": "1.0.0",
  "stage": "ProductSpecs",
  "checkpoint": 8,
  "source_file": "ProductSpecs_{SystemName}/04-jira/jira-import.json",
  "created_at": today,
  "updated_at": today,
  "total": count(jira.stories),
  "items": []
}

FOR EACH story in jira.stories:
  user_story_registry.items.append({
    "id": story.externalId,
    "title": story.summary,
    "priority": story.priority,
    "epic_id": story.epicLink,
    "screen_ids": story._meta.screen_id,
    "jtbd_refs": extractJtbdFromRequirement(story.externalId),
    "pain_point_refs": extractPainPointsFromRequirement(story.externalId),
    "acceptance_criteria_count": count(story._meta.gherkin_scenarios),
    "subtask_count": count(story.subtasks)
  })

WRITE: traceability/user_story_registry.json  # Already correct (ROOT level)
```

### Step 6.3: Build Test Scenario Registry

```
test_scenario_registry = {
  "schema_version": "1.0.0",
  "stage": "ProductSpecs",
  "checkpoint": 8,
  "source_file": "ProductSpecs_{SystemName}/04-jira/jira-import.json",
  "created_at": today,
  "updated_at": today,
  "total": 0,
  "items": []
}

FOR EACH story in jira.stories:
  FOR EACH scenario in story._meta.gherkin_scenarios:
    test_scenario_registry.items.append({
      "id": "TS-{story.externalId}-{N}",
      "name": scenario.name,
      "type": scenario.type || "functional",
      "priority": story.priority,
      "user_story_id": story.externalId,
      "epic_id": story.epicLink,
      "gherkin": scenario.gherkin,
      "e2e_subtask": findE2ESubtask(story, scenario)
    })
    test_scenario_registry.total += 1

WRITE: traceability/test_scenario_registry.json
```

### Step 6.4: Build Epic Registry

```
epic_registry = {
  "schema_version": "1.0.0",
  "stage": "ProductSpecs",
  "checkpoint": 8,
  "source_file": "ProductSpecs_{SystemName}/04-jira/jira-import.json",
  "created_at": today,
  "updated_at": today,
  "total": count(jira.epics),
  "items": []
}

FOR EACH epic in jira.epics:
  epic_registry.items.append({
    "id": epic.externalId,
    "name": epic.summary,
    "priority": epic.priority,
    "module_id": epic.externalId,
    "jtbd_ids": jtbd_epic_map[epic.externalId].jtbd_ids,
    "story_count": countStoriesForEpic(epic.externalId),
    "subtask_count": countSubtasksForEpic(epic.externalId)
  })

WRITE: traceability/epic_registry.json
```

### Step 6.5: Update JTBD Registry with Epic IDs

```
// Read existing JTBD registry
jtbd_registry = READ: traceability/jtbd_registry.json

// Update each JTBD with linked Epic IDs
FOR EACH jtbd in jtbd_registry.items:
  jtbd.epic_ids = []

  FOR EACH epic_id, mapping in jtbd_epic_map:
    IF jtbd.id IN mapping.jtbd_ids:
      jtbd.epic_ids.append(epic_id)

jtbd_registry.updated_at = today
jtbd_registry.epic_linkage = {
  "linked_at": today,
  "linked_by": "ProductSpecs_JiraExporter",
  "total_jtbds_linked": countLinkedJtbds()
}

WRITE: traceability/jtbd_registry.json
```

### Step 6.6: Update Master Traceability Register

```
// Read existing productspecs traceability register
register = READ: traceability/productspecs_traceability_register.json

// Add Epic, User Story, Test Scenario coverage
register.coverage.epics = {
  "total": count(jira.epics),
  "with_jtbd_links": countEpicsWithJtbdLinks(),
  "coverage_percent": calculateCoverage()
}

register.coverage.user_stories = {
  "total": count(jira.stories),
  "by_priority": {
    "P0": countStoriesByPriority("P0"),
    "P1": countStoriesByPriority("P1"),
    "P2": countStoriesByPriority("P2")
  }
}

register.coverage.test_scenarios = {
  "total": count(test_scenarios),
  "with_e2e": countScenariosWithE2E()
}

// Add new traceability chain
register.traceability_chain = {
  "description": "CM → PP → JTBD → EPIC → US → SCR → MOD → TS → TC → INV",
  "levels": [
    "Client Material (CM)",
    "Pain Point (PP)",
    "Job To Be Done (JTBD)",
    "Epic (EPIC)",
    "User Story (US)",
    "Screen (SCR)",
    "Module Spec (MOD)",
    "Test Scenario (TS)",
    "Test Case (TC)",
    "JIRA Item (INV)"
  ]
}

WRITE: traceability/productspecs_traceability_register.json
```

### Step 6.7: Update Trace Matrix

```
// Update trace_matrix.json with full chains
trace_matrix = READ: traceability/trace_matrix.json

// Add Epic→JTBD links
FOR EACH epic_id, mapping in jtbd_epic_map:
  FOR EACH jtbd_id in mapping.jtbd_ids:
    trace_matrix.links.append({
      "source": jtbd_id,
      "target": epic_id,
      "type": "JTBD_TO_EPIC"
    })

// Add Epic→User Story links
FOR EACH story in jira.stories:
  trace_matrix.links.append({
    "source": story.epicLink,
    "target": story.externalId,
    "type": "EPIC_TO_USER_STORY"
  })

// Add User Story→Test Scenario links
FOR EACH story in jira.stories:
  FOR EACH scenario in story._meta.gherkin_scenarios:
    trace_matrix.links.append({
      "source": story.externalId,
      "target": "TS-{story.externalId}-{N}",
      "type": "USER_STORY_TO_TEST_SCENARIO"
    })

trace_matrix.updated_at = today
WRITE: traceability/trace_matrix.json
```

### Phase 6 Output Files (All ROOT Level)

| File | Purpose |
|------|---------|
| `traceability/epic_registry.json` | All Epics with JTBD links |
| `traceability/user_story_registry.json` | All User Stories |
| `traceability/test_scenario_registry.json` | All Test Scenarios (Gherkin) |
| `traceability/jtbd_registry.json` | Updated with Epic IDs |
| `traceability/trace_matrix.json` | Updated with new link types |
| `traceability/productspecs_traceability_register.json` | Updated coverage |

---

## IMPORT WORKFLOW

### Two-Phase Import (Recommended)

**Phase 1: Import Epics and Stories**
```
1. Import epics-and-stories.csv
2. Wait for Jira to assign issue keys
3. Note the Story keys (e.g., INV-15, INV-16)
```

**Phase 2: Import Sub-tasks**
```
1. Update subtasks-only.csv with actual Story keys in Parent column
   (Or use Summary matching if Jira supports it)
2. Import subtasks-only.csv
3. Verify sub-tasks linked to correct Stories
```

### Single Import (Admin/JSON)

```
1. Use jira-import.json with External System Import
2. All hierarchy created in one operation
3. External IDs maintain relationships
```

---

## VALIDATION

### Step 5.1: Validate Structure

```
VERIFY:
  - [ ] All Epic Names unique
  - [ ] All Story summaries unique (for Parent matching)
  - [ ] All Sub-task Parents reference valid Story summaries
  - [ ] Time estimates in valid format (e.g., "2h", "1d")
  - [ ] Labels contain no special characters

REPORT: validation_results.json
```

### Step 5.2: Generate Summary

```
GENERATE summary:
  - Total Epics: {count}
  - Total Stories: {count}
  - Total Sub-tasks: {count}
  - Stories by Priority:
    - Highest (P0): {count}
    - High (P1): {count}
  - Sub-tasks by Type:
    - [FE] Frontend: {count}
    - [BE] Backend: {count}
    - [TEST] Testing: {count}
    - [A11Y] Accessibility: {count}
    - [DOCS] Documentation: {count}
    - [REVIEW] Review: {count}
  - Total Estimated Hours: {sum}
```

---

## USAGE EXAMPLES

### Basic Usage (Default Strategy)

```
Generate Jira import files with sub-tasks.

SPECS_PATH: /path/to/03_Product_Specs_InventorySystem
PROJECT_KEY: INV
PROJECT_NAME: Inventory Management System

Execute ProductSpecs_JiraExport skill.
```

### Comprehensive Sub-tasks

```
Generate Jira import with comprehensive sub-task breakdown.

SPECS_PATH: /path/to/03_Product_Specs_InventorySystem
PROJECT_KEY: INV
PROJECT_NAME: Inventory Management System
SUBTASK_STRATEGY: comprehensive

Execute ProductSpecs_JiraExport skill.
```

### Stories Only (No Sub-tasks)

```
Generate Jira import without sub-tasks.

SPECS_PATH: /path/to/03_Product_Specs_InventorySystem
PROJECT_KEY: INV
PROJECT_NAME: Inventory Management System
GENERATE_SUBTASKS: false

Execute ProductSpecs_JiraExport skill.
```

---

## SKILL DEPENDENCIES

This skill requires:
- Completed ProductSpecs_Generator output
- At minimum: modules/*.md files

This skill can invoke:
- `view` - Read spec files
- `create_file` - Write CSV/JSON/MD files
- `bash_tool` - Validate CSV structure

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-12-16 | Initial release |
| 1.1.0 | 2024-12-16 | Added sub-task generation with 4 strategies |
