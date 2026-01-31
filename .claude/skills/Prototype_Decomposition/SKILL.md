---
name: decomposing-prototype-structure
description: Use when you need to generate updated traceability views (OPML mindmaps) showing the complete prototype structure from Pages to Tests.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill decomposing-prototype-structure started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill decomposing-prototype-structure ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill decomposing-prototype-structure instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

# Decompose Prototype Structure

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_Decomposition
- **Version**: 2.3.1
- **Created**: 2024-12-13
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3

## Description
Generate OPML v2.0 mindmap files showing the complete prototype structure from a frontend perspective. Creates one file per app with full traceability from pages through components to requirements and tests.

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
- output files created (OPML mindmaps)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "decomposing-prototype-structure"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "decomposing-prototype-structure" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## When to Invoke

### Manual Invocation
- On user request for updated traceability view
- As part of final delivery documentation
- Via Builder command: `decompose` or `decompose [AppName]`

### Auto-Invocation (by other skills)
The following skills automatically invoke Decomposition after completion:

| Skill | Trigger | What Changes |
|-------|---------|--------------|
| Prototype_Components | `components_completed` | Component library updated |
| Prototype_Screens | `screens_completed` | Pages structure updated |
| Prototype_CodeGen | `codegen_completed` | Structure finalized |
| Prototype_QA | `qa_completed` | Test statuses updated |

Auto-invocation is **non-blocking** — if Decomposition fails, the calling skill still succeeds.

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
CHECK invocation mode:
  IF TRIGGER parameter provided:
    MODE = "auto" (invoked by another skill)
    LOG: "Auto-invoked by: {TRIGGER}"
  ELSE:
    MODE = "manual" (user command)
    LOG: "Manual invocation"

READ _state/discovery_summary.json → product name, app list
READ _state/requirements_registry.json → all requirements
READ outputs/03-screens/SCREEN_INDEX.md → page list by app
READ outputs/03-screens/*.md → page specs with components and requirements
READ outputs/02-components/COMPONENT_INDEX.md → component list
READ outputs/02-components/*.md → component specs with requirements

IF discovery_summary missing:
  BLOCK: "Run ValidateDiscovery first"
  
IF requirements_registry missing:
  BLOCK: "Run Requirements first"

IF screen specs missing:
  ═══════════════════════════════════════════
  ⚠️ INPUT VALIDATION FAILED
  ═══════════════════════════════════════════
  
  Screen specifications not found.
  Cannot build page decomposition.
  
  How would you like to proceed?
  1. "run Screens" - Generate screen specs first
  2. "partial" - Build from available data only
  3. "abort" - Stop and complete upstream skills
  ═══════════════════════════════════════════
  
  WAIT for user response

EXTRACT apps from discovery:
  apps = discovery_summary.apps[] or infer from screen-definitions.md
  
LOG: "Building decomposition for {app_count} apps"
```

### Step 2: Check for Existing OPML Files
```
FOR each app:
  CHECK if outputs/09-decomposition/{AppName}.opml exists
  
  IF exists:
    LOAD existing file
    EXTRACT user_edited_nodes:
      - Nodes with _userEdited="true" attribute
      - Custom notes added by user
      - Manual test annotations
    
    EXTRACT existing_version from head/version
    INCREMENT version: existing_version + 0.1
    
    SET merge_mode = true
    LOG: "Will merge into existing {AppName}.opml (v{version})"
  ELSE:
    SET merge_mode = false
    SET version = "1.0"
    LOG: "Creating new {AppName}.opml"
```

### Step 3: Build Page Structure per App
```
FOR each app:
  CREATE app_structure = {
    name: app_name,
    pages: []
  }
  
  FOR each page in app (from SCREEN_INDEX):
    LOAD page spec from outputs/03-screens/{PageName}.md
    
    EXTRACT:
      - priority (P0/P1/P2)
      - status (from progress.json or spec)
      - route (from spec or infer from name)
      - components_used[]
      - requirements_addressed[]
    
    CREATE page_node = {
      name: page_name,
      priority: priority,
      status: status,
      route: route,
      components: [],
      created: timestamp (if new),
      modified: timestamp
    }
    
    ADD to app_structure.pages[]
```

### Step 4: Build Component Hierarchy per Page
```
FOR each page in app_structure:
  FOR each component in page.components_used:
    LOAD component spec from outputs/02-components/{Component}.md
    
    EXTRACT:
      - variants[]
      - states[]
      - props[]
      - requirements_addressed[] from spec
      
    CREATE component_node = {
      name: component_name,
      variants: variants.join(", "),
      states: states.join(", "),
      props: props.join(", "),
      requirements: [],
      created: timestamp (if new),
      modified: timestamp
    }
    
    FOR each requirement_id in component.requirements_addressed:
      LOAD requirement from registry
      
      CREATE requirement_node = {
        id: requirement_id,
        description: requirement.description,
        priority: requirement.priority,
        type: requirement.type,
        tests: []
      }
      
      EXTRACT validation criteria from spec:
        FOR each criterion in component spec "Validation Criteria":
          IF criterion relates to this requirement:
            ADD test_node = {
              criterion: criterion_text,
              status: "pending" | from qa_results
            }
      
      ADD requirement_node to component_node.requirements[]
    
    ADD component_node to page_node.components[]
```

### Step 5: Build Component Library Branch
```
CREATE component_library = {
  name: "Component Library",
  components: []
}

FOR each unique component across all pages:
  LOAD component spec
  
  CREATE library_component = {
    name: component_name,
    used_on: [list of pages using this component],
    variants: variants,
    states: states,
    props: props,
    requirements: [all requirements this component addresses],
    tests: [all validation criteria]
  }
  
  ADD to component_library.components[]
```

### Step 6: Build Changelog Branch
```
IF merge_mode:
  LOAD existing changelog from OPML
  
  COMPARE current structure to existing:
    FOR each page:
      IF new: ADD to changelog.added[]
      IF modified (different components/reqs): ADD to changelog.modified[]
    FOR each component:
      IF new: ADD to changelog.added[]
      IF modified: ADD to changelog.modified[]
    FOR existing items not in current:
      ADD to changelog.removed[]
  
  CREATE changelog_entry = {
    version: new_version,
    date: timestamp,
    trigger: TRIGGER or "manual",
    added: [...],
    modified: [...],
    removed: [...]
  }
  
  PREPEND to changelog (newest first)
ELSE:
  CREATE changelog = [{
    version: "1.0",
    date: timestamp,
    added: ["Initial decomposition"],
    modified: [],
    removed: []
  }]
```

### Step 7: Merge with Existing (if applicable)
```
IF merge_mode:
  FOR each node in new structure:
    CHECK if corresponding node exists in old structure
    
    IF exists AND old_node._userEdited == "true":
      PRESERVE user edits:
        - Keep user-added child nodes
        - Keep user-modified attributes
        - Keep user notes
      MERGE new data alongside preserved edits
      SET node._merged = "true"
      
    IF exists AND NOT user edited:
      REPLACE with new data
      SET node.modified = timestamp
      
    IF NOT exists:
      ADD as new node
      SET node.created = timestamp
      
  FOR each node in old structure NOT in new:
    IF node._userEdited == "true":
      PRESERVE in "_Archived (User Edited)" branch
      LOG WARNING: "Preserved user-edited node: {node_name}"
    ELSE:
      REMOVE (will appear in changelog.removed)
```

### Step 8: Generate OPML v2.0 Structure
```
CREATE opml_document:

<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <head>
    <title>{ProductName} - {AppName} Decomposition</title>
    <dateCreated>{original_created}</dateCreated>
    <dateModified>{now}</dateModified>
    <ownerName>Prototype Skills Framework</ownerName>
    <docs>https://github.com/your-repo/prototype-skills</docs>
    <!-- Custom metadata -->
    <decompositionVersion>{version}</decompositionVersion>
    <schemaVersion>1.0</schemaVersion>
    <generatedBy>Prototype_Decomposition</generatedBy>
  </head>
  <body>
    <!-- App Root -->
    <outline text="{AppName}" _type="app" _created="{ts}" _modified="{ts}">
      
      <!-- Pages Branch -->
      <outline text="Pages" _type="pages-container">
        <outline text="{PageName}" _type="page" 
                 _priority="P0" _status="complete" _route="/dashboard"
                 _created="{ts}" _modified="{ts}">
          
          <!-- Components on this page -->
          <outline text="Components" _type="components-container">
            <outline text="{ComponentName}" _type="component"
                     _variants="primary, secondary" _states="default, hover, focus"
                     _props="onClick, disabled, children"
                     _created="{ts}" _modified="{ts}">
              
              <!-- Requirements this component addresses -->
              <outline text="Requirements" _type="requirements-container">
                <outline text="{REQ-ID}: {description}" _type="requirement"
                         _reqId="PP-001" _reqPriority="P0" _reqType="pain_point">
                  
                  <!-- Tests for this requirement -->
                  <outline text="Tests" _type="tests-container">
                    <outline text="{validation_criterion}" _type="test"
                             _status="pending"/>
                  </outline>
                </outline>
              </outline>
            </outline>
          </outline>
          
          <!-- Page-level requirements summary -->
          <outline text="Page Requirements Summary" _type="page-requirements">
            <outline text="{REQ-ID}: {description}" _type="requirement-ref"
                     _reqId="PP-001" _addressedBy="ComponentA, ComponentB"/>
          </outline>
        </outline>
      </outline>
      
      <!-- Component Library Branch -->
      <outline text="Component Library" _type="component-library">
        <outline text="{ComponentName}" _type="library-component"
                 _usedOn="Dashboard, Pipeline, CandidateDetail"
                 _variants="..." _states="..." _props="...">
          <outline text="Requirements" _type="requirements-container">
            ...
          </outline>
          <outline text="Tests" _type="tests-container">
            ...
          </outline>
        </outline>
      </outline>
      
      <!-- Changelog Branch -->
      <outline text="Changelog" _type="changelog">
        <outline text="v{version} ({date})" _type="changelog-entry" _version="{v}">
          <outline text="Added" _type="changelog-added">
            <outline text="{item}"/>
          </outline>
          <outline text="Modified" _type="changelog-modified">
            <outline text="{item}"/>
          </outline>
          <outline text="Removed" _type="changelog-removed">
            <outline text="{item}"/>
          </outline>
        </outline>
      </outline>
      
      <!-- Archived user edits (if any) -->
      <outline text="_Archived (User Edited)" _type="archived" _collapsed="true">
        ...
      </outline>
      
    </outline>
  </body>
</opml>
```

### Step 9: Validate Outputs (REQUIRED)
```
VALIDATE OPML structure:
  CHECKS:
    - Valid XML syntax
    - OPML 2.0 schema compliance
    - All pages from SCREEN_INDEX present
    - All components have at least 1 requirement
    - All requirements have at least 1 test
    - Changelog present and current
    - Version incremented (if merge)
    - User edits preserved (if merge)
    
IF any validation fails:
  ═══════════════════════════════════════════
  ⚠️ OUTPUT VALIDATION FAILED
  ═══════════════════════════════════════════
  
  OPML validation errors:
  • [list specific failures]
  
  Missing from decomposition:
  • [pages/components/requirements not included]
  
  How would you like to proceed?
  1. "fix: [issue]" - Address specific issue
  2. "add: [item]" - Add missing item
  3. "regenerate" - Re-run from Step 3
  4. "continue anyway" - Save with warnings
  ═══════════════════════════════════════════
  
  WAIT for user response
  HANDLE accordingly
```

### Step 10: Write Outputs & Update Progress
```
FOR each app:
  WRITE outputs/09-decomposition/{AppName}.opml

WRITE outputs/09-decomposition/DECOMPOSITION_INDEX.md:
  # Prototype Decomposition Index
  
  | App | Version | Pages | Components | Requirements | Last Updated |
  |-----|---------|-------|------------|--------------|--------------|
  | TalentApp | 1.2 | 12 | 45 | 67 | 2024-12-14 |

UPDATE _state/progress.json:
  phases.decomposition.status = "complete"
  phases.decomposition.completed_at = timestamp
  phases.decomposition.outputs = [file list]
  phases.decomposition.validation = {
    status: "passed",
    checks_run: count,
    checks_passed: count
  }
  phases.decomposition.metrics = {
    apps_documented: count,
    total_pages: count,
    total_components: count,
    total_requirements: count,
    total_tests: count,
    user_edits_preserved: count,
    version: version
  }
```

---

## Input Requirements

| Input | Required | Used For |
|-------|----------|----------|
| discovery_summary.json | ✅ Yes | Product name, app list |
| requirements_registry.json | ✅ Yes | Requirement details |
| SCREEN_INDEX.md | ✅ Yes | Page list by app |
| Screen specs (*.md) | ✅ Yes | Page details, components |
| COMPONENT_INDEX.md | ✅ Yes | Component list |
| Component specs (*.md) | ✅ Yes | Component details, tests |
| Existing OPML (if any) | ⚠️ Optional | Merge base |

---

## Output Validation Criteria

| Check | Requirement | Blocking? |
|-------|-------------|-----------|
| Valid XML | Well-formed | ✅ Yes |
| OPML 2.0 compliant | Schema valid | ✅ Yes |
| All pages included | 100% coverage | ✅ Yes |
| Components have reqs | ≥ 1 per component | ⚠️ Warning |
| Requirements have tests | ≥ 1 per requirement | ⚠️ Warning |
| User edits preserved | If merge mode | ✅ Yes |
| Version incremented | If merge mode | ✅ Yes |

---

## User Mitigation Options

| Response | Action |
|----------|--------|
| `run Screens` | Execute Screens skill first |
| `partial` | Build from available data |
| `fix: [issue]` | Address specific validation issue |
| `add: [item]` | Add missing page/component |
| `regenerate` | Re-run generation |
| `continue anyway` | Save with logged warnings |
| `abort` | Stop execution |

---

## OPML Node Types Reference

| _type Value | Description | Key Attributes |
|-------------|-------------|----------------|
| `app` | Application root | _created, _modified |
| `pages-container` | Pages branch | - |
| `page` | Individual page | _priority, _status, _route |
| `components-container` | Components on page | - |
| `component` | Component instance | _variants, _states, _props |
| `requirements-container` | Requirements branch | - |
| `requirement` | Individual requirement | _reqId, _reqPriority, _reqType |
| `tests-container` | Tests branch | - |
| `test` | Individual test | _status |
| `component-library` | Shared components | - |
| `library-component` | Library entry | _usedOn |
| `changelog` | Change history | - |
| `changelog-entry` | Version entry | _version |
| `archived` | Preserved user edits | _collapsed |

---

## Preserving User Edits

When users manually edit the OPML file (e.g., in a mindmap tool), their edits are preserved on regeneration:

### Marking User Edits
Users should add `_userEdited="true"` to nodes they customize:
```xml
<outline text="My Custom Note" _userEdited="true" _type="user-note">
  ...
</outline>
```

### What Gets Preserved
- Nodes with `_userEdited="true"`
- Child nodes under user-edited parents
- Custom attributes on user-edited nodes
- User-added notes and annotations

### What Gets Updated
- Auto-generated nodes without user edits
- Timestamps (_modified)
- Derived data (requirements, tests)
- Changelog entries

---

## Example Output Structure

```
TalentApp.opml
├── TalentApp (v1.2)
│   ├── Pages
│   │   ├── Dashboard (P0, complete, /dashboard)
│   │   │   ├── Components
│   │   │   │   ├── MetricsCard
│   │   │   │   │   └── Requirements
│   │   │   │   │       ├── PP-001: Manual tracking (P0)
│   │   │   │   │       │   └── Tests
│   │   │   │   │       │       └── Displays count in < 1s
│   │   │   │   │       └── A11Y-002: Color contrast
│   │   │   │   │           └── Tests
│   │   │   │   │               └── Ratio ≥ 4.5:1
│   │   │   │   └── NavigationSidebar
│   │   │   │       └── ...
│   │   │   └── Page Requirements Summary
│   │   │       ├── PP-001 → MetricsCard
│   │   │       └── US-003 → MetricsCard, QuickActions
│   │   ├── Pipeline (P0, complete, /pipeline)
│   │   │   └── ...
│   │   └── Settings (P2, pending, /settings)
│   │       └── ...
│   ├── Component Library
│   │   ├── Button
│   │   │   ├── Used On: Dashboard, Pipeline, CandidateDetail
│   │   │   ├── Variants: primary, secondary, danger, ghost
│   │   │   ├── Requirements
│   │   │   │   ├── A11Y-001: Keyboard navigation
│   │   │   │   └── A11Y-003: Focus indicators
│   │   │   └── Tests
│   │   │       ├── Tab focuses button
│   │   │       └── Enter/Space activates
│   │   └── Card
│   │       └── ...
│   └── Changelog
│       ├── v1.2 (2024-12-14)
│       │   ├── Added: Settings page
│       │   └── Modified: Dashboard (added MetricsCard)
│       └── v1.1 (2024-12-13)
│           └── Added: Pipeline page
```

---

## Progress.json Update

```json
{
  "phases": {
    "decomposition": {
      "status": "complete",
      "completed_at": "2024-12-14T10:00:00Z",
      "outputs": [
        "outputs/09-decomposition/TalentApp.opml",
        "outputs/09-decomposition/ClientApp.opml",
        "outputs/09-decomposition/DECOMPOSITION_INDEX.md"
      ],
      "validation": {
        "status": "passed",
        "checks_run": 8,
        "checks_passed": 8
      },
      "metrics": {
        "apps_documented": 2,
        "total_pages": 15,
        "total_components": 45,
        "total_requirements": 67,
        "total_tests": 120,
        "user_edits_preserved": 3,
        "versions": {
          "TalentApp": "1.2",
          "ClientApp": "1.0"
        }
      }
    }
  }
}
```

---

## Integration with Builder

The Decomposition skill is NOT in the standard build pipeline but can be invoked:

```
Builder Commands:
  "decompose" - Generate/update decomposition for all apps
  "decompose [AppName]" - Generate/update for specific app
  "decompose status" - Show current decomposition versions
```

Add to Prototype_Builder SKILL.md under optional skills if desired.
