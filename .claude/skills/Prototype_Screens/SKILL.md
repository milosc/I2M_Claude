---
name: generating-screen-specs
description: Use when you need to generate detailed screen specifications, including layouts, components, data requirements, and user flows, organized by app or portal.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-screen-specs started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-screen-specs ended '{"stage": "prototype"}'
---
---
name: generating-screen-specs
description: Use when you need to generate detailed screen specifications, including layouts, components, data requirements, and user flows, organized by app or portal.
model: sonnet
allowed-tools: Read, Write, Edit

# Spec App Screens

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-screen-specs instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning
> **Supports**: Smart Obsolescence Handling for non-UI projects

## Metadata
- **Skill ID**: Prototype_Screens
- **Version**: 2.0.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-26
- **Author**: Milos Cigoj
- **Change History**:
  - v2.0.0 (2025-12-26): Added NOT_APPLICABLE handling for non-UI projects
  - v1.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v1.0.0 (2025-01-15): Initial skill version

## Description
Generate screen specifications organized by app/portal. Creates detailed screen specs with layouts, components, data requirements, and user flows.

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

Generate detailed screen specifications organized by application. Follows OUTPUT_STRUCTURE.md for deterministic folder structure.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: The app names, screen names, and structure shown below (e.g., "recruiter-app", "candidate-portal") are examples from an ATS domain. Your actual apps and screens should be derived from the discovery documents for your specific project.

---

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:generating-screen-specs:started` - When skill begins
- `skill:generating-screen-specs:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Output Structure (REQUIRED)

> **⚠️ SHARED STATE FOLDER**: The `_state/` folder is at the **PROJECT ROOT level**, NOT inside `Prototype_<SystemName>/`. This folder is SHARED between Discovery and Prototype phases.
>
> ```
> project_root/
> ├── _state/                           ← SHARED state folder (ROOT LEVEL)
> │   ├── screen_registry.json          # Master screen tracking
> │   ├── discovery_summary.json
> │   └── requirements_registry.json
> ├── ClientAnalysis_<SystemName>/      ← Discovery outputs
> └── Prototype_<SystemName>/           ← Prototype outputs (02-screens/ lives here)
> ```

This skill MUST generate the following structure pattern (inside `Prototype_<SystemName>/`):

```
02-screens/
├── {app-1}/                           # One directory per app/portal
│   ├── {screen-1}.md
│   ├── {screen-2}.md
│   └── {screen-n}.md
├── {app-2}/
│   └── ...
├── {app-n}/
│   └── ...
├── DELIVERY_SUMMARY.md
└── SCREEN_SPECIFICATIONS_SUMMARY.md
```

### Example (ATS Domain)

For an Applicant Tracking System, this might look like:

```
02-screens/
├── recruiter-app/
│   ├── candidate-pipeline.md
│   ├── candidate-profile.md
│   └── recruiter-dashboard.md
├── candidate-portal/
│   ├── application-form.md
│   └── candidate-dashboard.md
├── hiring-manager-app/
│   └── ...
└── SCREEN_SPECIFICATIONS_SUMMARY.md
```

For a different domain (e.g., E-commerce), it might look like:

```
02-screens/
├── customer-app/
│   ├── product-catalog.md
│   ├── shopping-cart.md
│   └── checkout.md
├── merchant-portal/
│   ├── inventory-management.md
│   └── order-fulfillment.md
└── SCREEN_SPECIFICATIONS_SUMMARY.md
```

---

## Applicability Check (Smart Obsolescence Handling)

**BEFORE generating screen specifications**, check project classification:

```
1. Read _state/prototype_config.json (or _state/discovery_config.json)
2. Check project_classification.type
3. IF type IN [BACKEND_ONLY, DATABASE_ONLY, INTEGRATION, INFRASTRUCTURE]:
   → Generate NOT_APPLICABLE placeholder (see below)
   → SKIP full screen generation
4. IF type == FULL_STACK:
   → Proceed with normal screen generation
```

### N/A Placeholder Template

If project type is NOT `FULL_STACK`, generate this placeholder:

```markdown
# Screen Specifications

---
status: NOT_APPLICABLE
artifact: screen-specifications
project_type: {type}
classification_date: {date}
generated_date: {now}
---

## Reason

This artifact is not applicable for **{type}** projects.

Screen specifications are only generated for projects with user interface
components (FULL_STACK).

## Project Classification

- **Type**: {type}
- **Confidence**: {confidence}
- **Classified**: {date}

## What This Means

- No screen specifications will be generated for this project
- Downstream code generation will skip UI screen creation
- Focus remains on {focus_area_for_type}

## Alternative Artifacts

For this project type, refer to:
- `data-model.md` - Data entity definitions
- `api-contracts.json` - API specifications
- `test-data/` - Mock data for testing

---
*Generated by Prototype_Screens v2.0.0*
*Smart Obsolescence Handling enabled*
```

**Output**: Save to `02-screens/SCREEN_SPECIFICATIONS_SUMMARY.md` with N/A status.

---

## Apps/Portals Pattern

Derive apps from discovery documents. Common patterns:

| Pattern | Description | Example |
|---------|-------------|---------|
| **{role}-app** | App for specific user role | `recruiter-app/`, `merchant-portal/` |
| **{role}-portal** | Portal variant | `candidate-portal/`, `vendor-portal/` |
| **{feature}-dashboard** | Feature-focused | `analytics-dashboard/`, `admin-panel/` |
| **analytics-dashboard** | TA Leads, Execs | Reports, metrics |
| **admin-panel** | Admins | Users, roles, settings |

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ _state/discovery_summary.json → screen list by app
READ _state/requirements_registry.json → requirements to address
READ traceability/screen_registry.json → MASTER SCREEN LIST (CRITICAL)
READ 01-components/COMPONENT_LIBRARY_SUMMARY.md → available components
READ discovery/04-design-specs/screen-definitions.md → screen purposes

// ═══════════════════════════════════════════════════════════
// SCREEN REGISTRY VALIDATION (MANDATORY - NEW)
// ═══════════════════════════════════════════════════════════

IF screen_registry.json missing:
  ═══════════════════════════════════════════
  ❌ SCREEN REGISTRY NOT FOUND
  ═══════════════════════════════════════════

  Cannot proceed without traceability/screen_registry.json

  This file is generated by Prototype_ValidateDiscovery.
  Run that skill first.

  BLOCK: "Run Prototype_ValidateDiscovery first"
  ═══════════════════════════════════════════

// Load all Discovery screens from registry
discovery_screens = screen_registry.discovery_screens
total_screens_required = discovery_screens.length

═══════════════════════════════════════════════════════════════
📋 SCREEN REGISTRY LOADED
═══════════════════════════════════════════════════════════════

Total screens to generate: {total_screens_required}

By Priority:
├── P0 (Critical): {count}
├── P1 (Important): {count}
└── P2 (Nice-to-have): {count}

⚠️ ALL {total_screens_required} screens MUST have spec files
   Checkpoint 9 will FAIL if any screens are missing
═══════════════════════════════════════════════════════════════

IDENTIFY requirements this skill MUST address:
  - ALL P0 requirements (must be distributed across screens)
  - US-XXX user stories (each maps to a screen)
  - PP-XXX pain points (solved by specific screens)

IF components not generated:
  BLOCK: "Run Components first"

IF requirements_registry missing:
  BLOCK: "Run Requirements first"

EXTRACT P0 requirements:
  p0_requirements = requirements.filter(r => r.priority == "P0")

LOG: "Found {count} P0 requirements to address across screens"
LOG: "Found {total_screens_required} screens to generate from registry"
```

### Step 2: Map Requirements to Screens
```
FOR each P0 requirement:
  IDENTIFY which screen(s) will address it:
    - PP-001 (manual tracking) → recruiter-app/candidate-pipeline
    - US-003 (view candidates) → recruiter-app/candidate-pipeline
    - JTBD-005 (assess fit) → recruiter-app/candidate-profile
  
  IF requirement cannot be mapped:
    PROMPT for assignment
  
CREATE screen_requirements_map:
  {
    "recruiter-app/candidate-pipeline": ["PP-001", "PP-002", "US-003"],
    "recruiter-app/recruiter-dashboard": ["PP-003", "US-001", "JTBD-001"]
  }
```

### Step 3: Organize by App
```
GROUP screens by app:
  recruiter-app:
    - recruiter-dashboard
    - candidate-pipeline
    - candidate-profile
    - position-management
    - interview-scheduling
    - messaging-hub
    
  hiring-manager-app:
    - triage-queue
    - team-pipeline
    - offer-decision-summary
    
  interviewer-portal:
    - interviewer-dashboard
    - interviewer-availability
    
  candidate-portal:
    - candidate-dashboard
    - candidate-application
    - interview-scheduling
    
  analytics-dashboard:
    - executive-summary
    - ta-lead-analytics
    - pipeline-analytics
    
  admin-panel:
    - user-management
    - admin-roles-permissions
    - system-settings
```

### Step 4: Generate Screen Specs by App

#### 4a: Recruiter App Screens
```
FOR each screen in recruiter-app:
  
  LOG_PROMPT:
    skill: "Prototype_Screens"
    step: "Step 4a: Generate Recruiter App Screens"
    desired_outcome: "Generate {screen} spec with layout, components, flows"
    category: "generation"

  CREATE 02-screens/recruiter-app/{screen}.md:
    # {Screen Name}
    
    ## Metadata
    | Field | Value |
    |-------|-------|
    | App | Recruiter App |
    | URL | /recruiter/{path} |
    | Type | Dashboard / List / Detail / Form |
    | Primary Entity | {entity} |
    | Priority | P0 / P1 / P2 |
    
    ## Requirements Addressed (MANDATORY)
    | Req ID | Priority | Description | Implementation |
    |--------|----------|-------------|----------------|
    | PP-001 | P0 | Manual tracking | Kanban replaces spreadsheets |
    | US-003 | P0 | View pipeline | All stages visible in columns |
    | JTBD-001 | P1 | Quick assessment | Score visible on cards |
    
    ## Overview
    [Description of screen purpose and primary use case]
    
    ## Layout
    ```
    ┌─────────────────────────────────────────────┐
    │ Header                                       │
    ├─────────┬───────────────────────────────────┤
    │         │                                   │
    │ Sidebar │         Main Content              │
    │         │                                   │
    │         │  ┌───────┬───────┬───────┬─────┐ │
    │         │  │ New   │Screen │ Inter │Offer│ │
    │         │  │       │       │       │     │ │
    │         │  └───────┴───────┴───────┴─────┘ │
    │         │                                   │
    └─────────┴───────────────────────────────────┘
    ```
    
    ## Grid Structure
    | Area | Grid | Components |
    |------|------|------------|
    | Header | 1fr | Header, UserMenu |
    | Sidebar | 240px | Sidebar, NavItems |
    | Main | 1fr | KanbanBoard, Cards |
    
    ## Components Used
    | Component | Location | Props | Reqs Supported |
    |-----------|----------|-------|----------------|
    | Header | Top | variant="app" | - |
    | Sidebar | Left | collapsed={false} | - |
    | KanbanBoard | Main | stages={pipeline} | PP-001, US-003 |
    | CandidateCard | Board | candidate={data} | JTBD-001 |
    
    ## Data Requirements
    | Data | Source | Query | Caching |
    |------|--------|-------|---------|
    | candidates | API | GET /candidates?stage={stage} | 5min |
    | stages | Static | Pipeline template | Session |
    
    ## User Interactions
    | Action | Trigger | Handler | Result |
    |--------|---------|---------|--------|
    | Drag card | Mouse/Touch | onDragEnd | Update stage via API |
    | Click card | Click | onClick | Navigate to profile |
    | Filter | Select change | onFilter | Filter candidates |
    
    ## States
    | State | Display | Related Req |
    |-------|---------|-------------|
    | Loading | Skeleton cards | - |
    | Empty | EmptyState with CTA | UX best practice |
    | Error | Alert with retry | NFR-002 |
    | Success | Toast notification | UX best practice |
    
    ## Accessibility
    - Keyboard navigation through columns (Arrow keys)
    - Card reordering via keyboard (Space to grab, Arrows to move)
    - Screen reader announces card moves
    - Focus management on drag-drop
    
    ## Responsive Behavior
    | Breakpoint | Layout Change |
    |------------|---------------|
    | < 768px | Sidebar collapses to icon |
    | < 640px | Single column kanban scroll |
```

#### 4b-4f: Other App Screens
```
[Similar pattern for each app]
CREATE 02-screens/{app}/{screen}.md
```

### Step 5: Generate App READMEs
```
FOR each app directory:
  CREATE 02-screens/{app}/README.md:
    # {App Name}
    
    ## Purpose
    [App purpose and target users]
    
    ## Screens
    | Screen | URL | Priority |
    |--------|-----|----------|
    
    ## Navigation Flow
    [Mermaid diagram or description]
```

### Step 6: Generate Screen Summary
```
CREATE 02-screens/SCREEN_SPECIFICATIONS_SUMMARY.md:
  ---
  document_id: DOC-SCREEN-SUMMARY-001
  version: 1.0.0
  created_at: {YYYY-MM-DD}
  updated_at: {YYYY-MM-DD}
  generated_by: Prototype_Screens
  source_files:
    - _state/discovery_summary.json
    - _state/requirements_registry.json
  change_history:
    - version: "1.0.0"
      date: "{YYYY-MM-DD}"
      author: "Prototype_Screens"
      changes: "Initial screen specifications summary generation"
  ---

  # Screen Specifications Summary

  ## Overview
  Total screens: {count}
  Total apps: 6
  
  ## By App
  | App | Screens | P0 Screens |
  |-----|---------|------------|
  | Recruiter App | 6 | 3 |
  | Hiring Manager App | 3 | 2 |
  
  ## P0 Requirements Coverage
  | Requirement | Screen | Status |
  |-------------|--------|--------|
  | PP-001 | candidate-pipeline | ✅ |
  | PP-002 | candidate-pipeline | ✅ |
  
  **P0 Coverage: {count}/{total} (100%)** ✅
  
  ## Screen Index
  [Links to all screen specs organized by app]
```

### Step 7: Validate P0 Coverage (CRITICAL - BLOCKING)
```
AFTER all screens generated:
  FOR each P0 requirement in registry:
    SCAN all screen specs
    CHECK if requirement appears in "Requirements Addressed"

    IF P0 requirement not addressed:
      ADD to unaddressed_p0_list

IF unaddressed_p0_list.length > 0:
  ═══════════════════════════════════════════
  ❌ P0 COVERAGE VALIDATION FAILED
  ═══════════════════════════════════════════

  The following P0 requirements are NOT addressed:
  • {list requirements}

  This BLOCKS screen generation.

  How would you like to proceed?
  1. "assign: [REQ-ID] to [app/screen]" - Assign and regenerate
  2. "add screen: [app/name] for [REQ-IDs]" - Create new screen
  3. "abort" - Stop and review
  ═══════════════════════════════════════════

  WAIT for user response
  LOOP until all P0 addressed
```

### Step 7.5: Validate ALL Discovery Screens Have Specs (CRITICAL - BLOCKING)

> **SCREEN TRACEABILITY**: This step ensures EVERY screen from Discovery has a spec file.

```
// ═══════════════════════════════════════════════════════════
// SCREEN REGISTRY VALIDATION (MANDATORY - BLOCKING)
// ═══════════════════════════════════════════════════════════

READ traceability/screen_registry.json AS registry
discovery_screens = registry.discovery_screens

// Scan 02-screens/ for all generated spec files
generated_specs = []
FOR each folder in 02-screens/:
  FOR each .md file in folder:
    READ file content
    EXTRACT screen_id from content (look for M-XX or D-XX pattern)
    generated_specs.append(screen_id)

// Match against Discovery screens
missing_screens = []
found_screens = []

FOR each screen in discovery_screens:
  screen_id = screen.id
  screen_name = screen.name

  IF screen_id IN generated_specs:
    found_screens.append(screen_id)

    // Update registry traceability
    FOR trace in registry.traceability:
      IF trace.screen_id == screen_id:
        trace.spec_status = "complete"
        trace.spec_folder = "02-screens/{detected_folder}/"
        trace.updated_at = NOW_ISO()
  ELSE:
    missing_screens.append({
      "id": screen_id,
      "name": screen_name,
      "priority": screen.priority
    })

// Calculate coverage
specs_generated = found_screens.length
specs_missing = missing_screens.length
spec_coverage = (specs_generated / discovery_screens.length) * 100

// Update registry
registry.screen_coverage.specs_generated = specs_generated
registry.screen_coverage.specs_missing = specs_missing
registry.screen_coverage.spec_coverage_percent = round(spec_coverage, 1)
registry.screen_coverage.spec_validated_at = NOW_ISO()

WRITE registry TO traceability/screen_registry.json

// ═══════════════════════════════════════════════════════════
// BLOCKING VALIDATION
// ═══════════════════════════════════════════════════════════

IF missing_screens.length > 0:
  ═══════════════════════════════════════════════════════════════
  ❌ SCREEN COVERAGE VALIDATION FAILED
  ═══════════════════════════════════════════════════════════════

  Generated: {specs_generated}/{discovery_screens.length} screens ({spec_coverage}%)

  ⛔ MISSING SCREEN SPECS ({specs_missing}):

  | ID | Name | Priority |
  |----|------|----------|
  {FOR screen in missing_screens:
    | {screen.id} | {screen.name} | {screen.priority} |
  }

  This BLOCKS screen generation.
  ALL Discovery screens MUST have spec files.

  How would you like to proceed?
  1. "generate missing" - Generate specs for missing screens
  2. "show: [screen_id]" - Show Discovery details for screen
  3. "abort" - Stop and review

  ═══════════════════════════════════════════════════════════════

  WAIT for user response

  IF user selects "generate missing":
    FOR each screen in missing_screens:
      GENERATE spec file using screen details from Discovery
      ADD to 02-screens/{platform}/{screen-name}.md

    // Re-validate
    GOTO Step 7.5  // Repeat validation

ELSE:
  ═══════════════════════════════════════════════════════════════
  ✅ SCREEN COVERAGE VALIDATION PASSED
  ═══════════════════════════════════════════════════════════════

  All {discovery_screens.length} Discovery screens have spec files.

  Coverage: {specs_generated}/{discovery_screens.length} (100%)

  Screen Registry updated: traceability/screen_registry.json
  ═══════════════════════════════════════════════════════════════

LOG: "✅ Screen coverage validation passed: {specs_generated}/{discovery_screens.length}"
```

### Step 7.6: Validate Assembly-First Compliance (MANDATORY)

> **CRITICAL**: Validate that all generated React components follow Assembly-First principles.

```javascript
// ═══════════════════════════════════════════════════════════
// ASSEMBLY-FIRST VALIDATION
// ═══════════════════════════════════════════════════════════

LOG: "🔍 Validating Assembly-First compliance for generated screens..."

RUN assembly_first_validator:
  cd {project_root}
  python3 .claude/hooks/assembly_first_validator.py \
    --validate-prototype Prototype_{SystemName} \
    --verbose

CAPTURE exit_code and validation_report

IF exit_code == 2:
  // Critical violations found - BLOCKING
  ═══════════════════════════════════════════════════════════
  ❌ ASSEMBLY-FIRST VALIDATION FAILED (BLOCKING)
  ═══════════════════════════════════════════════════════════

  Critical violations found in generated screens:

  {validation_report}

  COMMON VIOLATIONS:
  • Raw HTML elements (<button>, <input>, <select>)
    → Replace with components from @/component-library

  • Missing component library imports
    → Add: import { Button, TextField, ... } from '@/component-library'

  • Manual ARIA attributes (except icon-only buttons)
    → React Aria components handle ARIA automatically

  HOW TO FIX:
  1. Review the validation report above
  2. Fix violations in prototype/src/screens/*.tsx files
  3. Re-run this skill

  This is a BLOCKING quality gate. Cannot proceed to Step 8.
  ═══════════════════════════════════════════════════════════

  STOP execution
  RETURN error

ELSE IF exit_code == 1:
  // Warnings only - Non-blocking
  ═══════════════════════════════════════════════════════════
  ⚠️  ASSEMBLY-FIRST WARNINGS (NON-BLOCKING)
  ═══════════════════════════════════════════════════════════

  {validation_report}

  Warnings found but no critical violations.

  RECOMMENDATIONS:
  • Use Tailwind theme tokens instead of arbitrary values
  • Remove manual ARIA attributes where possible
  • Consider refactoring for consistency

  Proceeding to Step 8 (warnings are non-blocking).
  ═══════════════════════════════════════════════════════════

  LOG: "⚠️  Assembly-First validation passed with warnings"

ELSE:
  // All checks passed
  ═══════════════════════════════════════════════════════════
  ✅ ASSEMBLY-FIRST VALIDATION PASSED
  ═══════════════════════════════════════════════════════════

  All generated screens comply with Assembly-First principles:
  • ✅ No raw HTML interactive elements
  • ✅ Component library imports present
  • ✅ No manual ARIA attributes
  • ✅ Using Tailwind theme tokens

  Proceeding to Step 8.
  ═══════════════════════════════════════════════════════════

  LOG: "✅ Assembly-First validation passed: all screens compliant"
```

**Why This Matters:**
- Assembly-First ensures accessibility by default (WCAG 2.1 AA)
- Reduces prototype build failures by 40%+
- Maintains consistency across all screens
- Leverages pre-built, tested component patterns

**Related Documentation:**
- `.claude/commands/_assembly_first_rules.md` - Assembly-First architecture rule
- `.claude/templates/component-library/SKILL.md` - Component library usage guide
- `.claude/agents/prototype-screen-specifier.md` - Screen generation with validation

### Step 8: Generate Delivery Summary
```
CREATE 02-screens/DELIVERY_SUMMARY.md:
  # Screen Delivery Summary
  
  ## Delivery Status
  [Status and sign-off information]
  
  ## Coverage Metrics
  [Detailed metrics]
  
  ## Outstanding Items
  [Any deferred items]
```

### Step 9: Auto-Invoke Decomposition
```
LOG: "Auto-triggering Decomposition (screens changed)"

INVOKE Prototype_Decomposition:
  MODE: merge
  TRIGGER: "screens_completed"
```

### Step 10: Update Progress (Atomic Updates)

> **Phase 4 Enhancement**: Uses ProgressLock for atomic, corruption-proof updates

```python
# IMPORT progress lock utility
from progress_lock import ProgressLock

# UPDATE progress with atomic file locking
with ProgressLock('prototype') as progress:
    # All updates happen atomically
    # Automatically saved on exit, rolled back on exception
    progress['phases']['screens']['status'] = 'complete'
    progress['phases']['screens']['completed_at'] = datetime.now().isoformat()
    progress['phases']['screens']['outputs'] = [
        "02-screens/SCREEN_SPECIFICATIONS_SUMMARY.md",
        "02-screens/DELIVERY_SUMMARY.md",
        "02-screens/recruiter-app/*.md",
        "02-screens/hiring-manager-app/*.md",
        "02-screens/interviewer-portal/*.md",
        "02-screens/candidate-portal/*.md",
        "02-screens/analytics-dashboard/*.md",
        "02-screens/admin-panel/*.md"
    ]
    progress['phases']['screens']['validation'] = {
        'status': 'passed',
        'p0_coverage': '100%'
    }
    progress['phases']['screens']['metrics'] = {
        'total_screens': total_screen_count,
        'by_app': screens_by_app_dict,
        'p0_requirements_addressed': p0_count,
        'p0_coverage': '100%'
    }
    # Lock released and changes saved automatically here
```

**Benefits**:
- ✅ Prevents progress.json corruption on skill failure
- ✅ Automatic rollback if exception occurs
- ✅ File locking prevents concurrent write conflicts
- ✅ Backup created before each update

---

## Output Files (REQUIRED)

| Directory | Min Files | Purpose |
|-----------|-----------|---------|
| `recruiter-app/` | 5+ | Main recruiter screens |
| `hiring-manager-app/` | 2+ | HM screens |
| `interviewer-portal/` | 2+ | Interviewer screens |
| `candidate-portal/` | 2+ | Candidate screens |
| `analytics-dashboard/` | 2+ | Analytics screens |
| `admin-panel/` | 2+ | Admin screens |
| `SCREEN_SPECIFICATIONS_SUMMARY.md` | 1 | Overview |
| `DELIVERY_SUMMARY.md` | 1 | Delivery status |

---

## Screen Spec Template (MANDATORY FORMAT)

```markdown
---
document_id: SCR-{APP}-{SCREEN}-001
version: 1.0.0
created_at: {YYYY-MM-DD}
updated_at: {YYYY-MM-DD}
generated_by: Prototype_Screens
source_files:
  - _state/discovery_summary.json
  - _state/requirements_registry.json
  - 01-components/COMPONENT_LIBRARY_SUMMARY.md
change_history:
  - version: "1.0.0"
    date: "{YYYY-MM-DD}"
    author: "Prototype_Screens"
    changes: "Initial screen specification generation"
---

# {Screen Name}

## Metadata
| Field | Value |
|-------|-------|
| App | {App Name} |
| URL | /{app}/{path} |
| Type | Dashboard / List / Detail / Form |
| Primary Entity | {entity} |
| Priority | P0 / P1 / P2 |

## Requirements Addressed (MANDATORY)
| Req ID | Priority | Description | Implementation |
|--------|----------|-------------|----------------|

## Overview
[Description]

## Layout
[ASCII diagram]

## Grid Structure
| Area | Grid | Components |
|------|------|------------|

## Components Used
| Component | Location | Props | Reqs Supported |
|-----------|----------|-------|----------------|

## Data Requirements
| Data | Source | Query | Caching |
|------|--------|-------|---------|

## User Interactions
| Action | Trigger | Handler | Result |
|--------|---------|---------|--------|

## States
| State | Display | Related Req |
|-------|---------|-------------|

## Accessibility
[Keyboard nav, screen reader, focus management]

## Responsive Behavior
| Breakpoint | Layout Change |
|------------|---------------|
```

---

## Progress.json Update

```json
{
  "phases": {
    "screens": {
      "status": "complete",
      "completed_at": "2024-12-13T12:00:00Z",
      "outputs": [
        "02-screens/SCREEN_SPECIFICATIONS_SUMMARY.md",
        "02-screens/DELIVERY_SUMMARY.md",
        "02-screens/recruiter-app/*.md",
        "02-screens/hiring-manager-app/*.md",
        "02-screens/interviewer-portal/*.md",
        "02-screens/candidate-portal/*.md",
        "02-screens/analytics-dashboard/*.md",
        "02-screens/admin-panel/*.md"
      ],
      "validation": {
        "status": "passed",
        "p0_coverage": "100%"
      },
      "metrics": {
        "total_screens": 18,
        "by_app": {
          "recruiter-app": 6,
          "hiring-manager-app": 3,
          "interviewer-portal": 2,
          "candidate-portal": 3,
          "analytics-dashboard": 2,
          "admin-panel": 2
        },
        "p0_requirements_addressed": 15,
        "p0_coverage": "100%"
      }
    }
  }
}
```
