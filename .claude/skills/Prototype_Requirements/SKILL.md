---
name: generating-prototype-requirements
description: Use when you need to extract and structure hierarchical requirements (Epics/Stories) from discovery for prototype implementation.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-prototype-requirements started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-prototype-requirements ended '{"stage": "prototype"}'
---

# Requirements Generator

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-prototype-requirements instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_Requirements
- **Version**: 1.2.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-23
- **Author**: Milos Cigoj
- **Change History**:
  - v1.2.0 (2025-12-23): Added mandatory ROOT-level registry propagation for full traceability chain
  - v1.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md.
  - v1.0.0 (2025-01-15): Initial skill version.

## Description
Create hierarchical requirements registry from discovery documentation. Generates Epics (high-level) and Stories (implementation-level) with full traceability to screens and components.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: Requirement IDs, titles, and examples shown below are from an ATS domain. Your actual requirements should be derived from your project's discovery documents.

## Requirements Hierarchy

```
JTBD (Jobs to Be Done)
  └── linked to → Pain Points (problems to solve)
  └── linked to → Epics (US, FR, NFR)
                    └── Stories (implementation-level)
                          └── linked to → Screens
                          └── linked to → Components
                          └── linked to → Code Files

A11Y (Accessibility) → Cross-cutting, referenced by components/screens
```

### Requirement Levels

| Level | Purpose | Example |
|-------|---------|---------|
| **JTBD** | Outcome user wants to achieve | "Make quick, confident hiring decisions" |
| **Pain Point** | Problem blocking the outcome | "Manual tracking causes lost candidates" |
| **Epic** | High-level requirement (US/FR/NFR) | "View all candidates in visual pipeline" |
| **Story** | Implementation-level requirement | "Display candidate card with avatar, name, stage, days-in-stage" |

---

## Output Structure (REQUIRED)

This skill MUST generate the following files:

```
_state/
├── requirements_registry.json        # Complete hierarchical registry
├── requirements_index.json           # Quick lookup index
├── jtbd_map.json                     # JTBD → Epic/Pain Point linkages
├── screen_requirements_map.json      # Screen → Epic/Story linkages
└── REQUIREMENTS_REGISTRY.md          # Human-readable registry
```

---

## Requirement Types

### Epic-Level Types

| Type | Prefix | Description | Gets Stories? |
|------|--------|-------------|---------------|
| Pain Point | PP-NNN | User pain points to solve | ❌ No (linked to JTBD) |
| User Story | US-NNN | User needs/goals | ✅ Yes |
| Functional | FR-NNN | System capabilities | ✅ Yes |
| Non-Functional | NFR-NNN | Quality attributes | ✅ Yes |
| Accessibility | A11Y-NNN | Accessibility requirements | ❌ No (cross-cutting) |

### Story-Level Format

| Format | Example | Description |
|--------|---------|-------------|
| `{EPIC-ID}-S{NN}` | `US-001-S01` | Story 01 under User Story 001 |
| `{EPIC-ID}-S{NN}` | `FR-005-S03` | Story 03 under Functional Req 005 |
| `{EPIC-ID}-S{NN}` | `NFR-002-S01` | Story 01 under Non-Functional 002 |

---

## Priority Levels

| Priority | Definition | Criteria |
|----------|------------|----------|
| P0 | Must have for MVP | Core functionality, blocking pain points, critical path |
| P1 | Should have | Important but not blocking |
| P2 | Nice to have | Enhancements, polish |

**Stories inherit priority from their parent Epic** unless explicitly overridden.

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ _state/discovery_summary.json

IF discovery_summary.json missing:
  BLOCK: "Run ValidateDiscovery first"

EXTRACT from discovery_summary:
  - pain_points[]
  - personas[]
  - entities[]
  - screens[]
  - workflows[]
  - jtbd[] (if available)
```

### Step 2: Extract Jobs to Be Done (JTBD)
```
FOR each job in discovery (or derive from personas/workflows):
  CREATE jtbd:
    {
      "id": "JTBD-{sequence}",
      "title": "{outcome user wants}",
      "description": "When {situation}, I want to {motivation}, so I can {outcome}",
      "personas": ["persona-id-1", "persona-id-2"],
      "linked_pain_points": [],    // Populated in Step 3
      "linked_epics": [],          // Populated in Steps 4-6
      "source": "discovery document path"
    }

EXAMPLE:
  {
    "id": "JTBD-001",
    "title": "Make quick, confident hiring decisions",
    "description": "When I have multiple candidates to evaluate, I want to see all relevant information at a glance, so I can make quick, confident hiring decisions",
    "personas": ["hiring-manager"],
    "linked_pain_points": ["PP-001", "PP-003"],
    "linked_epics": ["US-001", "US-005", "FR-012"]
  }
```

### Step 3: Extract Pain Point Requirements
```
FOR each pain_point in discovery_summary.pain_points:
  CREATE requirement:
    {
      "id": "PP-{sequence}",
      "type": "pain_point",
      "level": "epic",
      "priority": map_severity_to_priority(pain_point.severity),
      "title": "{concise problem statement}",
      "description": "Problem: {full description}",
      "source": "discovery/02-user-research/pain-points.md",
      "personas_affected": ["persona-1", "persona-2"],
      "linked_jtbd": ["JTBD-001"],           // Link to parent JTBD
      "linked_epics": [],                     // US/FR that solve this
      "acceptance_criteria": [
        "User can {solution} instead of {current_workaround}",
        "{measurable improvement}"
      ],
      "addressed_by": [],
      "status": "pending"
    }

AFTER creating all Pain Points:
  UPDATE each JTBD.linked_pain_points with relevant PP-IDs
```

### Step 4: Extract User Story Epics + Stories
```
FOR each persona in discovery_summary.personas:
  FOR each goal in persona.goals:
    
    // Create Epic
    CREATE epic:
      {
        "id": "US-{sequence}",
        "type": "user_story",
        "level": "epic",
        "priority": determine_priority(goal),
        "title": "As {persona.role}, I want to {goal}",
        "description": "{expanded description of need}",
        "source": "discovery/02-user-research/personas/{persona.id}.md",
        "persona": persona.id,
        "linked_jtbd": ["JTBD-XXX"],
        "linked_pain_points": ["PP-XXX"],    // Pain points this solves
        "linked_screens": [],                 // Populated by screens
        "acceptance_criteria": [
          "{high-level criterion 1}",
          "{high-level criterion 2}"
        ],
        "stories": [],                        // Story IDs
        "addressed_by": [],
        "status": "pending"
      }
    
    // Create Stories (component/interaction level)
    DECOMPOSE goal into implementation stories:
      
      FOR each UI element/interaction needed:
        CREATE story:
          {
            "id": "{EPIC-ID}-S{sequence}",    // e.g., US-001-S01
            "type": "story",
            "level": "story",
            "parent_epic": "US-{N}",
            "priority": inherit_or_override(epic.priority),
            "title": "{specific implementation requirement}",
            "description": "{detailed description}",
            "acceptance_criteria": [
              "{specific, testable criterion}",
              "{interaction behavior}",
              "{edge case handling}"
            ],
            "implements_with": {
              "screens": ["app/screen-name"],
              "components": ["ComponentName"],
              "code_files": []                // Populated during implementation
            },
            "addressed_by": [],
            "status": "pending"
          }
        
        ADD story.id to epic.stories[]

EXAMPLE Epic + Stories:

Epic: US-001 "As a Recruiter, I want to view all candidates in a visual pipeline"
├── US-001-S01: "Display pipeline with column per stage (New, Screening, Interview, Offer, Hired, Rejected)"
├── US-001-S02: "Show candidate card with avatar, name, current stage, days-in-stage badge"
├── US-001-S03: "Highlight urgent candidates (>5 days in stage) with warning indicator"
├── US-001-S04: "Enable drag-drop of candidate card between stage columns"
├── US-001-S05: "Show confirmation modal when moving to Rejected stage"
├── US-001-S06: "Display stage counts in column headers"
├── US-001-S07: "Support keyboard navigation between cards (arrow keys)"
└── US-001-S08: "Filter pipeline by position, source, or date range"
```

### Step 5: Extract Functional Requirement Epics + Stories
```
FOR each entity in discovery_summary.entities:
  
  // Create CRUD Epic
  CREATE epic:
    {
      "id": "FR-{sequence}",
      "type": "functional",
      "level": "epic",
      "priority": "P0",
      "title": "Manage {entity} records",
      "description": "Full CRUD operations for {entity}",
      "entity": entity.name,
      "linked_jtbd": [],
      "linked_screens": [],
      "acceptance_criteria": [
        "User can create new {entity}",
        "User can view {entity} details",
        "User can update {entity} fields",
        "User can delete/archive {entity}",
        "User can list/search {entity}s"
      ],
      "stories": [],
      "addressed_by": [],
      "status": "pending"
    }
  
  // Create Stories for each operation
  CREATE stories:
    - FR-{N}-S01: "Create {entity} form with required fields validation"
    - FR-{N}-S02: "Display {entity} detail view with all fields"
    - FR-{N}-S03: "Edit {entity} with inline or modal form"
    - FR-{N}-S04: "Delete {entity} with confirmation dialog"
    - FR-{N}-S05: "List {entity}s with pagination (20 per page)"
    - FR-{N}-S06: "Search {entity}s by {key_fields}"
    - FR-{N}-S07: "Sort {entity} list by {sortable_fields}"
    - FR-{N}-S08: "Filter {entity}s by {filter_fields}"

FOR each screen in discovery_summary.screens:
  FOR each primary_action in screen.actions:
    
    IF action not covered by CRUD:
      CREATE epic + stories for action

FOR each workflow in discovery_summary.workflows:
  CREATE epic for workflow with stories for each step
```

### Step 6: Extract Non-Functional Requirement Epics + Stories
```
CREATE NFR epics with stories:

// Performance
CREATE epic:
  {
    "id": "NFR-001",
    "type": "non_functional",
    "level": "epic",
    "priority": "P0",
    "title": "Page Load Performance",
    "description": "Application must load quickly",
    "category": "performance",
    "acceptance_criteria": [
      "Initial page load < 3 seconds",
      "Subsequent navigations < 1 second",
      "No UI blocking during data fetch"
    ],
    "stories": ["NFR-001-S01", "NFR-001-S02", "NFR-001-S03"],
    "addressed_by": [],
    "status": "pending"
  }

CREATE stories:
  - NFR-001-S01: "Implement skeleton loaders for all data-dependent sections"
  - NFR-001-S02: "Lazy load below-fold content and images"
  - NFR-001-S03: "Cache API responses in IndexedDB for offline access"

// Responsiveness
CREATE epic:
  {
    "id": "NFR-002",
    "type": "non_functional",
    "level": "epic",
    "priority": "P1",
    "title": "Responsive Design",
    "description": "Application must work across device sizes",
    "category": "responsiveness",
    "acceptance_criteria": [
      "Usable on mobile (320px+)",
      "Optimized for tablet (768px+)",
      "Full experience on desktop (1024px+)"
    ],
    "stories": ["NFR-002-S01", "NFR-002-S02", "NFR-002-S03"]
  }

CREATE stories:
  - NFR-002-S01: "Implement collapsible sidebar for mobile"
  - NFR-002-S02: "Stack cards vertically on narrow screens"
  - NFR-002-S03: "Adapt table to card view on mobile"

// Error Handling
CREATE epic:
  {
    "id": "NFR-003",
    "type": "non_functional",
    "level": "epic", 
    "priority": "P0",
    "title": "Error Handling",
    "description": "Application must handle errors gracefully",
    "category": "reliability"
  }

CREATE stories:
  - NFR-003-S01: "Display user-friendly error messages for API failures"
  - NFR-003-S02: "Implement retry mechanism for transient failures"
  - NFR-003-S03: "Show empty states with actionable guidance"
  - NFR-003-S04: "Preserve form data on submission errors"

// Data Persistence (for prototype)
CREATE epic:
  {
    "id": "NFR-004",
    "type": "non_functional",
    "level": "epic",
    "priority": "P0", 
    "title": "Local Data Persistence",
    "description": "Prototype must persist data locally",
    "category": "data"
  }

CREATE stories:
  - NFR-004-S01: "Initialize IndexedDB with schema on first load"
  - NFR-004-S02: "Seed demo data if database empty"
  - NFR-004-S03: "Implement data export functionality"
  - NFR-004-S04: "Implement data reset functionality"
```

### Step 7: Define Accessibility Requirements (Cross-Cutting)
```
CREATE A11Y requirements (no stories - referenced by components):
  [
    {
      "id": "A11Y-001",
      "type": "accessibility",
      "level": "cross-cutting",
      "priority": "P0",
      "title": "Keyboard Navigation",
      "description": "All interactive elements accessible via keyboard",
      "wcag": "2.1.1",
      "acceptance_criteria": [
        "Tab navigates through all interactive elements",
        "Enter/Space activates buttons and links",
        "Escape closes modals and dropdowns",
        "Arrow keys navigate within components"
      ],
      "applies_to": {
        "components": ["all interactive"],
        "patterns": ["navigation", "forms", "dialogs"]
      },
      "addressed_by": [],
      "status": "pending"
    },
    {
      "id": "A11Y-002",
      "type": "accessibility",
      "level": "cross-cutting",
      "priority": "P0",
      "title": "Color Contrast",
      "wcag": "1.4.3"
    },
    {
      "id": "A11Y-003",
      "type": "accessibility",
      "level": "cross-cutting",
      "priority": "P0",
      "title": "Focus Indicators",
      "wcag": "2.4.7"
    },
    {
      "id": "A11Y-004",
      "type": "accessibility",
      "level": "cross-cutting",
      "priority": "P0",
      "title": "Form Labels",
      "wcag": "1.3.1"
    },
    {
      "id": "A11Y-005",
      "type": "accessibility",
      "level": "cross-cutting",
      "priority": "P1",
      "title": "Screen Reader Support",
      "wcag": "4.1.2"
    },
    {
      "id": "A11Y-006",
      "type": "accessibility",
      "level": "cross-cutting",
      "priority": "P1",
      "title": "Reduced Motion",
      "wcag": "2.3.3"
    }
  ]
```

### Step 8: Link Screens to Requirements
```
FOR each screen in discovery_summary.screens:
  
  IDENTIFY which epics this screen addresses:
    - User Stories that mention this screen's functionality
    - Functional Requirements for entities shown on screen
    - Pain Points solved by this screen
  
  IDENTIFY which stories are implemented on this screen:
    - Stories whose implements_with.screens includes this screen
  
  CREATE screen_requirement_entry:
    {
      "screen_id": "{app}/{screen-name}",
      "screen_path": "02-screens/{app}/{screen-name}.md",
      "linked_epics": ["US-001", "FR-003", "PP-002"],
      "linked_stories": ["US-001-S01", "US-001-S02", "FR-003-S05"],
      "linked_a11y": ["A11Y-001", "A11Y-003", "A11Y-004"],
      "primary_persona": "recruiter"
    }

UPDATE each epic.linked_screens with screen IDs
UPDATE each story.implements_with.screens with screen IDs

WRITE _state/screen_requirements_map.json:
  {
    "screens": {
      "recruiter-app/candidate-pipeline": {
        "linked_epics": ["US-001", "US-002", "FR-001"],
        "linked_stories": ["US-001-S01", "US-001-S02", ...],
        "linked_a11y": ["A11Y-001", "A11Y-003"],
        "p0_count": 8,
        "total_stories": 15
      },
      ...
    },
    "coverage": {
      "screens_with_requirements": 12,
      "total_screens": 12,
      "screens_with_p0": 10
    }
  }
```

### Step 9: Create JTBD Map
```
WRITE _state/jtbd_map.json:
  {
    "jobs": [
      {
        "id": "JTBD-001",
        "title": "Make quick, confident hiring decisions",
        "personas": ["hiring-manager"],
        "pain_points": [
          {
            "id": "PP-001",
            "title": "Manual tracking causes lost candidates",
            "severity": "high"
          },
          {
            "id": "PP-003",
            "title": "No visibility into pipeline status",
            "severity": "high"
          }
        ],
        "epics": [
          {
            "id": "US-001",
            "title": "View candidates in visual pipeline",
            "story_count": 8,
            "p0_stories": 5
          },
          {
            "id": "FR-012",
            "title": "Filter and search candidates",
            "story_count": 6,
            "p0_stories": 4
          }
        ],
        "total_stories": 14,
        "completion": "0%"
      }
    ],
    "unlinked_epics": [],
    "unlinked_pain_points": []
  }
```

### Step 10: Create Requirements Registry
```
WRITE _state/requirements_registry.json:
  {
    "$metadata": {
      "document_id": "REG-REQUIREMENTS-001",
      "version": "1.0.0",
      "created_at": "YYYY-MM-DDTHH:MM:SSZ",
      "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
      "generated_by": "Prototype_Requirements",
      "source_files": [
        "_state/discovery_summary.json"
      ],
      "change_history": [
        {
          "version": "1.0.0",
          "date": "YYYY-MM-DD",
          "author": "Prototype_Requirements",
          "changes": "Initial requirements registry generation"
        }
      ]
    },
    "schema": "epic-story-hierarchy",
    "schema_version": "2.0",
    
    "summary": {
      "total_requirements": N,
      "epics": {
        "total": N,
        "by_type": {
          "pain_point": N,
          "user_story": N,
          "functional": N,
          "non_functional": N
        },
        "by_priority": { "P0": N, "P1": N, "P2": N }
      },
      "stories": {
        "total": N,
        "by_parent_type": {
          "user_story": N,
          "functional": N,
          "non_functional": N
        },
        "by_priority": { "P0": N, "P1": N, "P2": N }
      },
      "accessibility": {
        "total": N,
        "p0": N
      },
      "jtbd": {
        "total": N
      }
    },
    
    "jtbd": [
      // All JTBD entries
    ],
    
    "epics": [
      // All Epic-level requirements (PP, US, FR, NFR)
    ],
    
    "stories": [
      // All Story-level requirements
    ],
    
    "accessibility": [
      // All A11Y requirements
    ]
  }
```

### Step 11: Create Quick Lookup Index
```
WRITE _state/requirements_index.json:
  {
    "by_id": {
      "JTBD-001": { "type": "jtbd", "index": 0 },
      "PP-001": { "type": "epic", "index": 0 },
      "US-001": { "type": "epic", "index": 5 },
      "US-001-S01": { "type": "story", "index": 0, "parent": "US-001" },
      "A11Y-001": { "type": "accessibility", "index": 0 }
    },
    
    "epics_by_type": {
      "pain_point": ["PP-001", "PP-002", ...],
      "user_story": ["US-001", "US-002", ...],
      "functional": ["FR-001", "FR-002", ...],
      "non_functional": ["NFR-001", "NFR-002", ...]
    },
    
    "stories_by_epic": {
      "US-001": ["US-001-S01", "US-001-S02", ...],
      "FR-001": ["FR-001-S01", "FR-001-S02", ...],
      ...
    },
    
    "by_priority": {
      "P0": {
        "epics": ["PP-001", "US-001", ...],
        "stories": ["US-001-S01", "US-001-S02", ...]
      },
      "P1": { ... },
      "P2": { ... }
    },
    
    "by_screen": {
      "recruiter-app/candidate-pipeline": {
        "epics": ["US-001", "FR-001"],
        "stories": ["US-001-S01", "US-001-S02", "FR-001-S05"]
      }
    },
    
    "by_persona": {
      "recruiter": {
        "epics": ["US-001", "US-002"],
        "stories": ["US-001-S01", ...]
      }
    },
    
    "by_component": {
      "CandidateCard": ["US-001-S02", "US-001-S03"],
      "Button": ["A11Y-001", "A11Y-003"]
    }
  }
```

### Step 12: Generate Human-Readable Registry
```
WRITE _state/REQUIREMENTS_REGISTRY.md:

---
document_id: DOC-REQUIREMENTS-001
version: 1.0.0
created_at: {YYYY-MM-DD}
updated_at: {YYYY-MM-DD}
generated_by: Prototype_Requirements
source_files:
  - _state/discovery_summary.json
  - _state/requirements_registry.json
change_history:
  - version: "1.0.0"
    date: "{YYYY-MM-DD}"
    author: "Prototype_Requirements"
    changes: "Initial human-readable requirements registry generation"
---

# Requirements Registry

> Generated: {timestamp}
> Schema: Epic-Story Hierarchy v2.0

## Summary

| Level | Count | P0 | P1 | P2 |
|-------|-------|----|----|----| 
| JTBD | {N} | - | - | - |
| Epics (PP) | {N} | {N} | {N} | {N} |
| Epics (US) | {N} | {N} | {N} | {N} |
| Epics (FR) | {N} | {N} | {N} | {N} |
| Epics (NFR) | {N} | {N} | {N} | {N} |
| Stories | {N} | {N} | {N} | {N} |
| A11Y | {N} | {N} | {N} | - |

---

## Jobs to Be Done (JTBD)

### JTBD-001: Make quick, confident hiring decisions

**Personas:** Hiring Manager, TA Lead

**Linked Pain Points:**
- PP-001: Manual tracking causes lost candidates
- PP-003: No visibility into pipeline status

**Linked Epics:**
- US-001: View candidates in visual pipeline (8 stories)
- FR-012: Filter and search candidates (6 stories)

---

## P0 Requirements (Must Have)

### Pain Points

| ID | Title | Personas | Linked JTBD | Status |
|----|-------|----------|-------------|--------|
| PP-001 | Manual tracking causes lost candidates | Recruiter, HM | JTBD-001 | Pending |

### User Story Epics

#### US-001: As a Recruiter, I want to view all candidates in a visual pipeline

| Field | Value |
|-------|-------|
| Priority | P0 |
| Persona | Recruiter |
| Linked JTBD | JTBD-001 |
| Linked Pain Points | PP-001, PP-003 |
| Linked Screens | recruiter-app/candidate-pipeline |
| Stories | 8 |

**Epic Acceptance Criteria:**
- [ ] User can see all candidates organized by stage
- [ ] User can move candidates between stages
- [ ] Pipeline updates in real-time

**Stories:**

| ID | Title | Priority | Screens | Components | Status |
|----|-------|----------|---------|------------|--------|
| US-001-S01 | Display pipeline with column per stage | P0 | candidate-pipeline | KanbanColumn | Pending |
| US-001-S02 | Show candidate card with avatar, name, days-in-stage | P0 | candidate-pipeline | CandidateCard, Avatar, Badge | Pending |
| US-001-S03 | Highlight urgent candidates (>5 days) | P0 | candidate-pipeline | Badge | Pending |
| US-001-S04 | Enable drag-drop between stages | P0 | candidate-pipeline | KanbanColumn | Pending |
| US-001-S05 | Show confirmation modal for Rejected | P1 | candidate-pipeline | Dialog | Pending |
| US-001-S06 | Display stage counts in headers | P0 | candidate-pipeline | KanbanColumn | Pending |
| US-001-S07 | Keyboard navigation between cards | P1 | candidate-pipeline | CandidateCard | Pending |
| US-001-S08 | Filter by position, source, date | P1 | candidate-pipeline | Select, Input | Pending |

<details>
<summary>Story Details</summary>

##### US-001-S01: Display pipeline with column per stage

**Acceptance Criteria:**
- [ ] Display 6 columns: New, Screening, Interview, Offer, Hired, Rejected
- [ ] Each column has header with stage name
- [ ] Columns are horizontally scrollable on narrow screens
- [ ] Empty columns show "No candidates" placeholder

**Implements With:**
- Screens: recruiter-app/candidate-pipeline
- Components: KanbanColumn, EmptyState

---

##### US-001-S02: Show candidate card with avatar, name, days-in-stage

**Acceptance Criteria:**
- [ ] Card displays candidate avatar (or initials fallback)
- [ ] Card shows full name prominently
- [ ] Badge shows days in current stage
- [ ] Card is clickable to open candidate detail

**Implements With:**
- Screens: recruiter-app/candidate-pipeline
- Components: CandidateCard, Avatar, Badge, Card

</details>

---

### Functional Requirement Epics

#### FR-001: Manage Candidate records

[Similar structure with stories]

---

### Non-Functional Requirement Epics

#### NFR-001: Page Load Performance

| ID | Title | Priority | Status |
|----|-------|----------|--------|
| NFR-001-S01 | Implement skeleton loaders | P0 | Pending |
| NFR-001-S02 | Lazy load below-fold content | P1 | Pending |
| NFR-001-S03 | Cache API responses in IndexedDB | P1 | Pending |

---

## Accessibility Requirements (Cross-Cutting)

| ID | Title | WCAG | Priority | Applies To |
|----|-------|------|----------|------------|
| A11Y-001 | Keyboard Navigation | 2.1.1 | P0 | All interactive |
| A11Y-002 | Color Contrast | 1.4.3 | P0 | All text |
| A11Y-003 | Focus Indicators | 2.4.7 | P0 | All focusable |
| A11Y-004 | Form Labels | 1.3.1 | P0 | All forms |
| A11Y-005 | Screen Reader Support | 4.1.2 | P1 | All content |
| A11Y-006 | Reduced Motion | 2.3.3 | P1 | Animations |

---

## Screen Coverage

| Screen | Epics | Stories | P0 Stories | Status |
|--------|-------|---------|------------|--------|
| recruiter-app/candidate-pipeline | 3 | 15 | 10 | Pending |
| recruiter-app/candidate-profile | 2 | 12 | 8 | Pending |
| hiring-manager-app/triage-queue | 2 | 8 | 6 | Pending |

---

## Traceability Quick Reference

### By Component

| Component | Stories |
|-----------|---------|
| CandidateCard | US-001-S02, US-001-S03, US-005-S01 |
| KanbanColumn | US-001-S01, US-001-S04, US-001-S06 |
| Dialog | US-001-S05, FR-001-S04, FR-003-S02 |

### By Persona

| Persona | Epics | Stories |
|---------|-------|---------|
| Recruiter | 8 | 45 |
| Hiring Manager | 5 | 28 |
| Candidate | 3 | 15 |
```

### Step 13: Validate Requirements (REQUIRED)
```
VALIDATE requirements:
  
  STRUCTURE CHECKS:
    - [ ] At least 1 JTBD defined
    - [ ] At least 1 P0 Pain Point
    - [ ] At least 1 P0 User Story Epic
    - [ ] At least 1 P0 Functional Epic
    - [ ] All A11Y requirements present (6 minimum)
    - [ ] No duplicate IDs
    - [ ] All story IDs follow {EPIC-ID}-S{NN} format
  
  HIERARCHY CHECKS:
    - [ ] All Pain Points linked to at least 1 JTBD
    - [ ] All Epics (US/FR) linked to at least 1 JTBD or Pain Point
    - [ ] All Stories have valid parent_epic reference
    - [ ] All Epics have at least 1 Story (except PP and A11Y)
  
  CONTENT CHECKS:
    - [ ] All Epics have acceptance criteria
    - [ ] All Stories have acceptance criteria
    - [ ] All Stories have implements_with.screens (at least 1)
    - [ ] P0 Epics have P0 Stories
  
  COVERAGE CHECKS:
    - [ ] All screens linked to at least 1 Epic
    - [ ] All personas have at least 1 Epic
    - [ ] Critical user flows covered by Stories
    
IF validation fails:
  ═══════════════════════════════════════════
  ⚠️ REQUIREMENTS VALIDATION FAILED
  ═══════════════════════════════════════════
  
  Issues found:
  • {list issues}
  
  How would you like to proceed?
  1. "fix: [issue]" - Address specific issue
  2. "regenerate" - Re-run extraction
  3. "continue anyway" - Proceed with warnings
  ═══════════════════════════════════════════
  
  WAIT for user response
```

### Step 14: PROPAGATE TO ROOT-LEVEL TRACEABILITY (MANDATORY)

> **CRITICAL**: After creating local `_state/` registries, MUST propagate to ROOT-level `traceability/` folder.

```
# ═══════════════════════════════════════════════════════════════════════
# ROOT-LEVEL REGISTRY PROPAGATION (AUTOMATIC - NO USER PROMPTS)
# ═══════════════════════════════════════════════════════════════════════

# Step 14.1: Propagate Requirements Registry
READ _state/requirements_registry.json AS local_reqs

WRITE traceability/requirements_registry.json:
{
  "schema_version": "1.0.0",
  "stage": "Prototype",
  "checkpoint": 2,
  "source_file": "_state/requirements_registry.json",
  "created_at": "{timestamp}",
  "updated_at": "{timestamp}",
  "traceability_chain": {
    "upstream": ["pain_point_registry.json", "jtbd_registry.json"],
    "downstream": ["screen_registry.json", "module_registry.json"]
  },
  "summary": {
    "total": local_reqs.summary.total_requirements,
    "by_type": local_reqs.summary.epics.by_type,
    "by_priority": local_reqs.summary.epics.by_priority
  },
  "items": local_reqs.epics.concat(local_reqs.stories)
}

# Step 14.2: Update JTBD Registry with Requirement Links
READ traceability/jtbd_registry.json AS jtbd_reg

FOR each requirement in local_reqs.epics:
  FOR each jtbd_id in requirement.linked_jtbd:
    FIND jtbd in jtbd_reg.jtbd WHERE jtbd.id == jtbd_id
    IF jtbd.requirement_ids NOT EXISTS:
      jtbd.requirement_ids = []
    APPEND requirement.id TO jtbd.requirement_ids

jtbd_reg.updated_at = "{timestamp}"
WRITE traceability/jtbd_registry.json

# Step 14.3: Log Propagation
LOG: "✅ ROOT-level traceability propagated:"
LOG: "   - traceability/requirements_registry.json ({N} items)"
LOG: "   - traceability/jtbd_registry.json (updated with REQ links)"

# Step 14.4: MANDATORY Propagation Validation (BLOCKING)
# ═══════════════════════════════════════════════════════════════════════
# THIS STEP CANNOT BE SKIPPED - Propagation failure blocks the checkpoint
# ═══════════════════════════════════════════════════════════════════════

VERIFY FILE EXISTS: traceability/requirements_registry.json
IF NOT EXISTS:
  ERROR: "❌ CRITICAL: Propagation to traceability/requirements_registry.json FAILED"
  ERROR: "   This is a BLOCKING error. Checkpoint 2 cannot pass without this file."
  ERROR: "   The file MUST exist in the ROOT traceability/ folder."
  FAIL_CHECKPOINT: 2
  EXIT with error

VERIFY FILE HAS CONTENT:
READ traceability/requirements_registry.json AS propagated_file
IF propagated_file.items IS EMPTY OR propagated_file.items.length == 0:
  ERROR: "❌ CRITICAL: traceability/requirements_registry.json has no items"
  ERROR: "   Propagation appears to have created an empty file."
  FAIL_CHECKPOINT: 2
  EXIT with error

LOG: "✅ Propagation validation PASSED:"
LOG: "   - traceability/requirements_registry.json exists with {N} items"
LOG: "   - Ready for downstream stages (ProductSpecs, SolArch, Implementation)"
```

---

### Step 15: Update Progress
```
UPDATE _state/progress.json:
  phases.requirements.status = "complete"
  phases.requirements.completed_at = timestamp
  phases.requirements.outputs = [
    "_state/requirements_registry.json",
    "_state/requirements_index.json",
    "_state/jtbd_map.json",
    "_state/screen_requirements_map.json",
    "_state/REQUIREMENTS_REGISTRY.md"
  ]
  phases.requirements.validation = {
    status: "passed",
    checks_run: N,
    checks_passed: N
  }
  phases.requirements.metrics = {
    jtbd_count: N,
    epic_count: N,
    story_count: N,
    p0_epics: N,
    p0_stories: N,
    pain_points: N,
    user_stories: N,
    functional: N,
    non_functional: N,
    accessibility: N,
    screens_covered: N,
    personas_covered: N
  }
```

---

## Output Files (REQUIRED)

### Local State Files (`_state/`)
| Path | Purpose | Blocking? |
|------|---------|-----------|
| `_state/requirements_registry.json` | Complete hierarchical registry (source) | ✅ Yes |
| `_state/requirements_index.json` | Quick lookup by ID, type, screen, etc. | ✅ Yes |
| `_state/jtbd_map.json` | JTBD → Pain Point → Epic linkages | ✅ Yes |
| `_state/screen_requirements_map.json` | Screen → requirement linkages | ✅ Yes |
| `_state/REQUIREMENTS_REGISTRY.md` | Human-readable documentation | ✅ Yes |

### ROOT Traceability Files (`traceability/`) - CRITICAL
| Path | Purpose | Blocking? |
|------|---------|-----------|
| `traceability/requirements_registry.json` | **Propagated registry for cross-stage traceability** | ✅ **CRITICAL** |

> **⚠️ CRITICAL**: The `traceability/requirements_registry.json` file MUST be created during Step 14.
> This file is referenced by downstream stages (ProductSpecs, SolArch, Implementation).
> If this file is missing, the entire traceability chain is broken.

---

## Schema Reference

### Epic Schema
```json
{
  "id": "US-001",
  "type": "user_story|functional|non_functional|pain_point",
  "level": "epic",
  "priority": "P0|P1|P2",
  "title": "Short title",
  "description": "Full description",
  "source": "Path to source document",
  "persona": "persona-id (for US)",
  "entity": "entity-name (for FR)",
  "category": "performance|reliability|... (for NFR)",
  "linked_jtbd": ["JTBD-001"],
  "linked_pain_points": ["PP-001"],
  "linked_screens": ["app/screen-name"],
  "acceptance_criteria": ["Criterion 1", "Criterion 2"],
  "stories": ["US-001-S01", "US-001-S02"],
  "addressed_by": ["component: X", "screen: Y"],
  "status": "pending|addressed|verified"
}
```

### Story Schema
```json
{
  "id": "US-001-S01",
  "type": "story",
  "level": "story",
  "parent_epic": "US-001",
  "priority": "P0|P1|P2",
  "title": "Specific implementation requirement",
  "description": "Detailed description",
  "acceptance_criteria": [
    "Specific testable criterion",
    "Interaction behavior",
    "Edge case handling"
  ],
  "implements_with": {
    "screens": ["recruiter-app/candidate-pipeline"],
    "components": ["CandidateCard", "Avatar"],
    "code_files": ["src/components/patterns/CandidateCard.tsx"]
  },
  "addressed_by": [],
  "status": "pending|addressed|verified"
}
```

### JTBD Schema
```json
{
  "id": "JTBD-001",
  "title": "Outcome user wants",
  "description": "When {situation}, I want {motivation}, so I can {outcome}",
  "personas": ["hiring-manager", "ta-lead"],
  "linked_pain_points": ["PP-001", "PP-003"],
  "linked_epics": ["US-001", "FR-012"]
}
```

### A11Y Schema (Cross-Cutting)
```json
{
  "id": "A11Y-001",
  "type": "accessibility",
  "level": "cross-cutting",
  "priority": "P0",
  "title": "Keyboard Navigation",
  "description": "All interactive elements accessible via keyboard",
  "wcag": "2.1.1",
  "acceptance_criteria": ["Tab navigates...", "Enter activates..."],
  "applies_to": {
    "components": ["all interactive"],
    "patterns": ["navigation", "forms"]
  },
  "addressed_by": [],
  "status": "pending"
}
```

---

## Progress.json Update

```json
{
  "phases": {
    "requirements": {
      "status": "complete",
      "completed_at": "2024-12-13T09:30:00Z",
      "outputs": [
        "_state/requirements_registry.json",
        "_state/requirements_index.json",
        "_state/jtbd_map.json",
        "_state/screen_requirements_map.json",
        "_state/REQUIREMENTS_REGISTRY.md"
      ],
      "validation": {
        "status": "passed",
        "checks_run": 15,
        "checks_passed": 15
      },
      "metrics": {
        "jtbd_count": 5,
        "epic_count": 35,
        "story_count": 180,
        "p0_epics": 15,
        "p0_stories": 85,
        "pain_points": 12,
        "user_stories": 20,
        "functional": 25,
        "non_functional": 8,
        "accessibility": 6,
        "screens_covered": 15,
        "personas_covered": 4
      }
    }
  }
}
```
