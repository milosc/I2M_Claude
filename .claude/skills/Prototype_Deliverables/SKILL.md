---
name: generating-professional-deliverables
description: Use when you need to export prototype artifacts into professional formats like PowerPoint (PPTX), Word (DOCX), or PDF reports for stakeholders.
model: haiku
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-professional-deliverables started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-professional-deliverables ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-professional-deliverables instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

# Professional Deliverables Generator

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_Deliverables
- **Version**: 2.3.1
- **Created**: 2024-12-13
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3

Export prototype artifacts as professional documents for stakeholders. Follows OUTPUT_STRUCTURE.md for deterministic folder structure.

> **Phase 4 Enhancement**: Integrates pptx, docx, and pdf skills for professional document generation.

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
- output files created (professional deliverables)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "generating-professional-deliverables"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "generating-professional-deliverables" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## Output Structure (REQUIRED)

This skill MUST generate the following structure:

```
06-deliverables/
├── presentations/
│   ├── requirements_deck.pptx          # Stakeholder requirements presentation
│   ├── prototype_overview.pptx         # High-level prototype presentation
│   └── thumbnails/                     # Visual previews
│       ├── requirements_deck.jpg
│       └── prototype_overview.jpg
├── documents/
│   ├── prototype_spec.docx             # Complete specification document
│   ├── technical_handoff.docx          # Developer handoff document
│   └── user_guide_draft.docx           # User documentation draft
├── reports/
│   ├── qa_report.pdf                   # Formal QA validation report
│   ├── requirements_summary.pdf        # Requirements summary for stakeholders
│   └── accessibility_report.pdf        # A11Y compliance report
└── DELIVERABLES_MANIFEST.md            # Index of all deliverables
```

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)

```
READ _state/progress.json → check phases
READ _state/requirements_registry.json → requirements
READ _state/discovery_summary.json → personas, pain points
READ 05-validation/VALIDATION_REPORT.md → QA results
READ 05-validation/TRACEABILITY_MATRIX.md → coverage

REQUIRED_PHASES = ["requirements", "design_tokens", "components", "screens", "qa"]

FOR each phase in REQUIRED_PHASES:
  IF progress.phases[phase].status != "complete":
    ═══════════════════════════════════════════
    ⚠️ PREREQUISITE NOT MET
    ═══════════════════════════════════════════

    Phase "{phase}" must be complete before generating deliverables.

    How would you like to proceed?
    1. "run {phase}" - Complete the missing phase
    2. "partial" - Generate available deliverables only
    3. "abort" - Stop and complete prerequisites
    ═══════════════════════════════════════════

    WAIT for user response

LOG: "All prerequisites validated. Starting deliverable generation..."
```

### Step 2: Select Deliverables

```
DISPLAY:
  ═══════════════════════════════════════════
  📦 DELIVERABLE SELECTION
  ═══════════════════════════════════════════

  Which deliverables would you like to generate?

  PRESENTATIONS:
  [1] Requirements Deck (stakeholder presentation)
  [2] Prototype Overview (high-level summary)

  PRESENTATION FORMAT:
  [format] PowerPoint (PPTX) - Traditional slides
  [format] Slidev (Markdown) - Web-based developer presentation

  DOCUMENTS:
  [3] Prototype Specification (complete spec)
  [4] Technical Handoff (developer documentation)
  [5] User Guide Draft (end-user documentation)

  REPORTS:
  [6] QA Report (formal validation report)
  [7] Requirements Summary (stakeholder summary)
  [8] Accessibility Report (A11Y compliance)

  OPTIONS:
  - "all" - Generate all deliverables
  - "1,3,6" - Generate specific items
  - "presentations" - All presentations
  - "documents" - All documents
  - "reports" - All reports

  FORMAT OPTIONS:
  - "pptx" - Use PowerPoint format (default)
  - "slidev" - Use Slidev web-based format
  ═══════════════════════════════════════════

WAIT for user selection

STORE selected_deliverables[]
STORE presentation_format (default: "pptx")
```

### Step 3: Generate Requirements Deck

```
IF "requirements_deck" in selected_deliverables:

  LOG: "Generating Requirements Deck presentation..."

  IF presentation_format == "slidev":
    // Use Slidev format
    INVOKE slidev skill with:
      - Content from discovery_summary.json
      - Diagram format: mermaid
      - Theme: professional/technical
    SKIP to Step 4

  // Otherwise continue with PPTX format

  // Step 3.1: Design approach
  DESIGN_APPROACH:
    - Subject: Project requirements and user research
    - Tone: Professional, data-driven
    - Palette: Ocean Depths (#1C2833, #2E4053, #AAB7B8, #F4F6F6)
    - Typography: Arial for body, bold headers
    - Layout: Clean with visual hierarchy

  // Step 3.2: Create slide content
  SLIDES = [
    {
      type: "title",
      title: "{project_name} Requirements",
      subtitle: "Stakeholder Presentation",
      date: "{date}"
    },
    {
      type: "agenda",
      items: ["User Research", "Pain Points", "Requirements", "Priorities", "Next Steps"]
    },
    {
      type: "section",
      title: "User Research"
    },
    {
      type: "personas",
      FOR each persona in discovery_summary.personas:
        name: persona.name,
        role: persona.role,
        goals: persona.goals,
        frustrations: persona.frustrations
    },
    {
      type: "section",
      title: "Pain Points"
    },
    {
      type: "pain_points",
      FOR each pain_point in discovery_summary.pain_points (top 5 by severity):
        id: pain_point.id,
        description: pain_point.description,
        severity: pain_point.severity,
        personas_affected: pain_point.personas_affected
    },
    {
      type: "section",
      title: "Requirements Overview"
    },
    {
      type: "requirements_summary",
      p0_count: requirements.filter(p => p.priority == "P0").length,
      p1_count: requirements.filter(p => p.priority == "P1").length,
      p2_count: requirements.filter(p => p.priority == "P2").length,
      categories: [group requirements by type]
    },
    {
      type: "requirements_detail",
      FOR each category:
        title: category.name,
        items: category.requirements (top 5)
    },
    {
      type: "priorities",
      title: "P0 Requirements (Must Have)",
      items: requirements.filter(p => p.priority == "P0")
    },
    {
      type: "next_steps",
      items: ["Review requirements", "Approve priorities", "Begin prototype development"]
    }
  ]

  // Step 3.3: Generate presentation using html2pptx workflow
  CREATE HTML files for each slide:
    - Use 720pt × 405pt dimensions (16:9)
    - Apply design approach colors/fonts
    - Include proper positioning

  GENERATE presentation:
    READ skills/pptx/html2pptx.md for detailed syntax
    CREATE workspace/requirements_deck/
    CREATE HTML slides
    RUN html2pptx conversion
    SAVE to 06-deliverables/presentations/requirements_deck.pptx

  // Step 3.4: Create thumbnail
  CREATE thumbnail:
    python scripts/thumbnail.py requirements_deck.pptx workspace/thumbnails
    COPY to 06-deliverables/presentations/thumbnails/requirements_deck.jpg

  LOG: "✅ Requirements Deck generated"
```

### Step 4: Generate Prototype Overview Deck

```
IF "prototype_overview" in selected_deliverables:

  LOG: "Generating Prototype Overview presentation..."

  IF presentation_format == "slidev":
    // Use Slidev format
    INVOKE slidev skill with:
      - Content from prototype artifacts
      - Diagram format: mermaid
      - Theme: professional/technical
    SKIP to Step 5

  // Otherwise continue with PPTX format

  SLIDES = [
    {
      type: "title",
      title: "{project_name} Prototype",
      subtitle: "Overview Presentation"
    },
    {
      type: "agenda",
      items: ["Solution Overview", "Key Screens", "Components", "Data Model", "Implementation Status"]
    },
    {
      type: "solution_overview",
      pain_points_addressed: count,
      screens_built: count,
      components_created: count
    },
    {
      type: "screen_gallery",
      FOR each screen in top_screens (P0 screens):
        name: screen.name,
        purpose: screen.purpose,
        screenshot: "if available from playwright"
    },
    {
      type: "component_library",
      categories: [list component categories],
      total_components: count
    },
    {
      type: "data_model",
      entities: [list main entities],
      relationships: [key relationships]
    },
    {
      type: "implementation_status",
      phases_complete: [list],
      p0_coverage: "100%",
      next_steps: [list]
    }
  ]

  GENERATE using html2pptx workflow
  SAVE to 06-deliverables/presentations/prototype_overview.pptx
  CREATE thumbnail

  LOG: "✅ Prototype Overview generated"
```

### Step 5: Generate Prototype Specification (DOCX)

```
IF "prototype_spec" in selected_deliverables:

  LOG: "Generating Prototype Specification document..."

  // Use docx-js for document creation
  READ skills/docx/docx-js.md for detailed syntax

  DOCUMENT_STRUCTURE = {
    title: "{project_name} Prototype Specification",

    sections: [
      {
        heading: "1. Executive Summary",
        content: [
          "Project overview",
          "Scope and objectives",
          "Key stakeholders"
        ]
      },
      {
        heading: "2. User Research",
        subsections: [
          "2.1 Personas" → FROM discovery_summary.personas,
          "2.2 User Journeys" → FROM discovery_summary.workflows,
          "2.3 Pain Points" → FROM discovery_summary.pain_points
        ]
      },
      {
        heading: "3. Requirements",
        subsections: [
          "3.1 Functional Requirements" → FROM requirements_registry (type == "functional"),
          "3.2 Non-Functional Requirements" → FROM requirements_registry (type == "non_functional"),
          "3.3 Accessibility Requirements" → FROM requirements_registry (type == "accessibility")
        ]
      },
      {
        heading: "4. Design System",
        subsections: [
          "4.1 Design Tokens" → FROM 01-design-system/,
          "4.2 Component Library" → FROM 01-components/,
          "4.3 Interaction Patterns" → FROM 03-interactions/
        ]
      },
      {
        heading: "5. Screen Specifications",
        subsections: [
          FOR each screen in 02-screens/:
            "5.N {screen.name}" → FROM screen spec
        ]
      },
      {
        heading: "6. Data Model",
        subsections: [
          "6.1 Entity Definitions" → FROM 00-foundation/data-model/,
          "6.2 API Contracts" → FROM 00-foundation/api-contracts/
        ]
      },
      {
        heading: "7. Implementation",
        subsections: [
          "7.1 Technical Stack",
          "7.2 Implementation Sequence" → FROM 04-implementation/
        ]
      },
      {
        heading: "8. Validation",
        subsections: [
          "8.1 Requirements Coverage" → FROM 05-validation/,
          "8.2 Accessibility Compliance" → FROM 05-validation/accessibility/
        ]
      },
      {
        heading: "Appendix A: Requirements Traceability Matrix",
        content: FROM 05-validation/TRACEABILITY_MATRIX.md
      }
    ]
  }

  CREATE document:
    const doc = new Document({
      sections: [...]
    });

    // Add title page
    // Add table of contents
    // Add each section with proper formatting
    // Add tables for requirements, components, etc.

    Packer.toBuffer(doc).then(buffer => {
      fs.writeFileSync('06-deliverables/documents/prototype_spec.docx', buffer);
    });

  LOG: "✅ Prototype Specification generated"
```

### Step 6: Generate Technical Handoff Document (DOCX)

```
IF "technical_handoff" in selected_deliverables:

  LOG: "Generating Technical Handoff document..."

  DOCUMENT_STRUCTURE = {
    title: "Technical Handoff Document",

    sections: [
      {
        heading: "1. Project Setup",
        content: [
          "Repository structure",
          "Installation instructions",
          "Development environment"
        ]
      },
      {
        heading: "2. Architecture Overview",
        subsections: [
          "2.1 Technology Stack",
          "2.2 Folder Structure",
          "2.3 Key Dependencies"
        ]
      },
      {
        heading: "3. Data Model",
        content: "Entity schemas with TypeScript types"
      },
      {
        heading: "4. API Reference",
        content: "All API endpoints with request/response formats"
      },
      {
        heading: "5. Component Reference",
        content: "All components with props and usage examples"
      },
      {
        heading: "6. Implementation Notes",
        content: [
          "Known limitations",
          "Future enhancements",
          "Technical debt"
        ]
      }
    ]
  }

  GENERATE using docx-js
  SAVE to 06-deliverables/documents/technical_handoff.docx

  LOG: "✅ Technical Handoff generated"
```

### Step 7: Generate QA Report (PDF)

```
IF "qa_report" in selected_deliverables:

  LOG: "Generating QA Report PDF..."

  // Use reportlab for PDF creation
  READ skills/pdf/SKILL.md for detailed syntax

  REPORT_CONTENT = {
    title: "Quality Assurance Report",

    sections: [
      {
        heading: "Executive Summary",
        content: [
          "Validation status: {APPROVED/BLOCKED}",
          "P0 Coverage: {coverage}%",
          "Critical issues: {count}",
          "Sign-off status: {status}"
        ]
      },
      {
        heading: "Requirements Coverage",
        table: FROM 05-validation/REQUIREMENTS_COVERAGE.md
      },
      {
        heading: "Traceability Matrix",
        table: FROM 05-validation/TRACEABILITY_MATRIX.md
      },
      {
        heading: "Functional Testing Results",
        content: FROM 05-validation/QA_CHECKLIST.md
      },
      {
        heading: "Automated Test Results",
        content: FROM 05-validation/AUTOMATED_TEST_RESULTS.md (if exists)
      },
      {
        heading: "Accessibility Audit",
        content: FROM 05-validation/accessibility/
      },
      {
        heading: "Recommendations",
        content: "Outstanding items and next steps"
      }
    ]
  }

  CREATE PDF:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    doc = SimpleDocTemplate("06-deliverables/reports/qa_report.pdf")
    story = []

    # Add title
    # Add executive summary
    # Add coverage tables
    # Add test results

    doc.build(story)

  LOG: "✅ QA Report generated"
```

### Step 8: Generate Accessibility Report (PDF)

```
IF "accessibility_report" in selected_deliverables:

  LOG: "Generating Accessibility Report PDF..."

  REPORT_CONTENT = {
    title: "Accessibility Compliance Report",

    sections: [
      {
        heading: "WCAG 2.1 AA Compliance",
        content: FROM 05-validation/accessibility/wcag-compliance.md
      },
      {
        heading: "Audit Results",
        content: FROM 05-validation/accessibility/a11y-audit-results.md
      },
      {
        heading: "Component Audit",
        table: "Component-by-component accessibility status"
      },
      {
        heading: "Remediation Plan",
        content: "Issues found and recommended fixes"
      }
    ]
  }

  GENERATE PDF using reportlab
  SAVE to 06-deliverables/reports/accessibility_report.pdf

  LOG: "✅ Accessibility Report generated"
```

### Step 9: Generate Requirements Summary (PDF)

```
IF "requirements_summary" in selected_deliverables:

  LOG: "Generating Requirements Summary PDF..."

  REPORT_CONTENT = {
    title: "Requirements Summary",

    sections: [
      {
        heading: "Overview",
        content: "High-level requirements summary for stakeholders"
      },
      {
        heading: "P0 Requirements (Must Have)",
        table: requirements.filter(p => p.priority == "P0")
      },
      {
        heading: "P1 Requirements (Should Have)",
        table: requirements.filter(p => p.priority == "P1")
      },
      {
        heading: "P2 Requirements (Nice to Have)",
        table: requirements.filter(p => p.priority == "P2")
      },
      {
        heading: "Coverage Status",
        content: "Current implementation status"
      }
    ]
  }

  GENERATE PDF
  SAVE to 06-deliverables/reports/requirements_summary.pdf

  LOG: "✅ Requirements Summary generated"
```

### Step 10: Generate Deliverables Manifest

```
CREATE 06-deliverables/DELIVERABLES_MANIFEST.md:

  # Deliverables Manifest

  **Generated:** {timestamp}
  **Project:** {project_name}

  ---

  ## Summary

  | Category | Count | Status |
  |----------|-------|--------|
  | Presentations | {count} | ✅ |
  | Documents | {count} | ✅ |
  | Reports | {count} | ✅ |

  ---

  ## Presentations

  | File | Purpose | Size | Generated |
  |------|---------|------|-----------|
  | [requirements_deck.pptx](presentations/requirements_deck.pptx) | Stakeholder presentation | {size} | {date} |
  | [prototype_overview.pptx](presentations/prototype_overview.pptx) | High-level overview | {size} | {date} |

  ### Thumbnails

  | Preview | Deck |
  |---------|------|
  | ![Requirements](presentations/thumbnails/requirements_deck.jpg) | Requirements Deck |
  | ![Overview](presentations/thumbnails/prototype_overview.jpg) | Prototype Overview |

  ---

  ## Documents

  | File | Purpose | Size | Generated |
  |------|---------|------|-----------|
  | [prototype_spec.docx](documents/prototype_spec.docx) | Complete specification | {size} | {date} |
  | [technical_handoff.docx](documents/technical_handoff.docx) | Developer documentation | {size} | {date} |
  | [user_guide_draft.docx](documents/user_guide_draft.docx) | User documentation | {size} | {date} |

  ---

  ## Reports

  | File | Purpose | Size | Generated |
  |------|---------|------|-----------|
  | [qa_report.pdf](reports/qa_report.pdf) | Formal QA report | {size} | {date} |
  | [requirements_summary.pdf](reports/requirements_summary.pdf) | Requirements overview | {size} | {date} |
  | [accessibility_report.pdf](reports/accessibility_report.pdf) | A11Y compliance | {size} | {date} |

  ---

  ## Usage Notes

  ### For Stakeholders
  - Start with `requirements_deck.pptx` for requirements review
  - Reference `requirements_summary.pdf` for priority decisions

  ### For Developers
  - Use `technical_handoff.docx` for implementation guidance
  - Reference `prototype_spec.docx` for complete specifications

  ### For QA Team
  - Review `qa_report.pdf` for validation status
  - Reference `accessibility_report.pdf` for A11Y compliance

  ---

  ## Regeneration

  To regenerate deliverables:
  ```
  "run deliverables"
  "run deliverables only presentations"
  "run deliverables only qa_report"
  ```
```

### Step 11: Verification Gate (MANDATORY)

```
EXECUTE verification_gate:

  // 1. IDENTIFY verification commands
  verification_commands = [
    FOR each generated deliverable:
      "test -s 06-deliverables/{path}"
  ]

  // 2. RUN all verifications
  FOR each command:
    EXECUTE and CAPTURE result

  // 3. CHECK all deliverables exist
  IF any deliverable missing:
    ═══════════════════════════════════════════
    ⚠️ DELIVERABLE GENERATION INCOMPLETE
    ═══════════════════════════════════════════

    Missing deliverables:
    {list missing files}

    How would you like to proceed?
    1. "retry" - Attempt to regenerate missing files
    2. "continue" - Proceed without missing files
    3. "investigate" - Show generation errors
    ═══════════════════════════════════════════

    WAIT for user response

  // 4. ONLY THEN mark complete
  LOG: "✅ VERIFICATION PASSED: All deliverables generated"
```

### Step 12: Update Progress

```
UPDATE _state/progress.json:
  phases.deliverables.status = "complete"
  phases.deliverables.completed_at = timestamp
  phases.deliverables.outputs = [
    "06-deliverables/DELIVERABLES_MANIFEST.md",
    "06-deliverables/presentations/requirements_deck.pptx",
    "06-deliverables/presentations/prototype_overview.pptx",
    "06-deliverables/documents/prototype_spec.docx",
    "06-deliverables/documents/technical_handoff.docx",
    "06-deliverables/reports/qa_report.pdf",
    "06-deliverables/reports/requirements_summary.pdf",
    "06-deliverables/reports/accessibility_report.pdf"
  ]
  phases.deliverables.validation = {
    status: "passed",
    deliverables_generated: count,
    deliverables_requested: count
  }
  phases.deliverables.metrics = {
    presentations: count,
    documents: count,
    reports: count,
    total_size_mb: size
  }
```

---

## Output Files (REQUIRED)

| Path | Purpose | Blocking? |
|------|---------|-----------|
| `DELIVERABLES_MANIFEST.md` | Index of all deliverables | ✅ Yes |
| `presentations/requirements_deck.pptx` | Stakeholder presentation | ⚠️ If selected |
| `presentations/prototype_overview.pptx` | Overview presentation | ⚠️ If selected |
| `documents/prototype_spec.docx` | Complete specification | ⚠️ If selected |
| `documents/technical_handoff.docx` | Developer handoff | ⚠️ If selected |
| `reports/qa_report.pdf` | QA validation report | ⚠️ If selected |
| `reports/accessibility_report.pdf` | A11Y compliance | ⚠️ If selected |

---

## Commands

| Command | Action |
|---------|--------|
| `deliverables` | Interactive deliverable selection |
| `deliverables all` | Generate all deliverables |
| `deliverables presentations` | Generate presentations only |
| `deliverables documents` | Generate documents only |
| `deliverables reports` | Generate reports only |
| `deliverables only [name]` | Generate specific deliverable |

---

## Dependencies

Required tools (should be pre-installed):
- **pptxgenjs**: `npm install -g pptxgenjs` (presentations)
- **docx**: `npm install -g docx` (documents)
- **reportlab**: `pip install reportlab` (PDFs)
- **pypdf**: `pip install pypdf` (PDF utilities)

---

## Progress.json Update

```json
{
  "phases": {
    "deliverables": {
      "status": "complete",
      "completed_at": "2024-12-13T16:00:00Z",
      "outputs": [
        "06-deliverables/DELIVERABLES_MANIFEST.md",
        "06-deliverables/presentations/*.pptx",
        "06-deliverables/documents/*.docx",
        "06-deliverables/reports/*.pdf"
      ],
      "validation": {
        "status": "passed",
        "deliverables_generated": 7,
        "deliverables_requested": 7
      },
      "metrics": {
        "presentations": 2,
        "documents": 3,
        "reports": 3,
        "total_size_mb": 4.2
      }
    }
  }
}
```
