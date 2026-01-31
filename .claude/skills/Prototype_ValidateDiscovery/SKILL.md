---
name: validating-discovery-completeness
description: Use when you need to validate discovery documentation for completeness, extract structured data, and create a foundational summary for downstream skills.
model: sonnet
allowed-tools: Bash, Glob, Grep, Read
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-discovery-completeness started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-discovery-completeness ended '{"stage": "prototype"}'
---

# Validate Discovery Completeness

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill validating-discovery-completeness instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_ValidateDiscovery
- **Version**: 2.3.1
- **Created**: 2024-12-13
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3

## Description
Validate discovery documentation for completeness and extract key data. Creates summary state file for downstream skills.

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

Validate discovery documentation and extract structured data. Creates foundation for all downstream skills.

> **💡 DISCOVERY IS PROJECT-SPECIFIC**: This skill reads from your discovery documents. Examples shown (personas, entities, screens) are illustrative. The actual data extracted depends entirely on your project's discovery content.

## Output Structure (REQUIRED)

> **⚠️ SHARED STATE FOLDER**: The `_state/` folder is at the **PROJECT ROOT level**, NOT inside `Prototype_<SystemName>/`. This folder is SHARED between Discovery and Prototype phases.

```
project_root/
├── _state/                           ← SHARED state folder (ROOT LEVEL)
│   ├── discovery_summary.json        # Extracted data from discovery
│   ├── screen_registry.json          # Master screen tracking
│   ├── GAP_REMEDIATION_PLAN.md       # Gaps found and remediation steps
│   ├── progress.json                 # Machine state
│   └── PROGRESS.md                   # Human-readable progress
├── ClientAnalysis_<SystemName>/      ← Discovery outputs
└── Prototype_<SystemName>/           ← Prototype outputs
```

**Path Resolution**:
- All paths starting with `_state/` resolve to the **ROOT-LEVEL shared folder**
- All other paths resolve relative to `Prototype_<SystemName>/`

---

## Expected Discovery Structure

The skill expects discovery documentation in this structure:

```
discovery/
├── 01-stakeholder-interviews/
│   ├── stakeholder-1.md
│   ├── stakeholder-2.md
│   └── SUMMARY.md
├── 02-user-research/
│   ├── personas/
│   │   ├── persona-recruiter.md
│   │   ├── persona-hiring-manager.md
│   │   └── ...
│   ├── user-journeys/
│   │   └── ...
│   ├── pain-points.md
│   └── SUMMARY.md
├── 03-competitive-analysis/
│   ├── competitor-1.md
│   └── SUMMARY.md
├── 04-design-specs/
│   ├── data-fields.md
│   ├── screen-definitions.md
│   └── workflows.md
└── DISCOVERY_SUMMARY.md
```

---

## Procedure

### Step 1: Check Discovery Directory Exists
```
CHECK discovery/ directory exists

IF not exists:
  ═══════════════════════════════════════════
  ❌ DISCOVERY NOT FOUND
  ═══════════════════════════════════════════
  
  Cannot find discovery documentation at:
  discovery/
  
  Please provide discovery path:
  1. "path: [path]" - Specify alternate location
  2. "create minimal" - Create minimal discovery template
  3. "abort" - Stop and gather discovery first
  ═══════════════════════════════════════════
  
  WAIT for user response
```

### Step 1.5: Document Conversion (Phase 5 Enhancement)

> **markitdown Integration**: Convert various file formats to markdown for processing.

```
// ═══════════════════════════════════════════════════════════
// PHASE 5: DOCUMENT CONVERSION
// ═══════════════════════════════════════════════════════════

// Supported formats for conversion
SUPPORTED_FORMATS = [
  ".pdf",     // PDF documents - stakeholder presentations, specs
  ".docx",    // Microsoft Word - requirements docs, interviews
  ".pptx",    // PowerPoint - discovery presentations, workshops
  ".xlsx",    // Excel - data field definitions, mappings
  ".csv",     // CSV files - data exports, lists
  ".html",    // Web pages - competitor analysis, research
  ".json",    // JSON - API specs, configurations
  ".xml",     // XML documents - data exports
  ".epub",    // E-books - documentation
  ".png", ".jpg", ".jpeg", ".gif", ".webp"  // Images - wireframes, whiteboard photos (OCR)
]

// Scan discovery directory for non-markdown files
SCAN discovery_path recursively for files matching SUPPORTED_FORMATS

non_markdown_files = []
FOR each file in discovery_path:
  IF file.extension in SUPPORTED_FORMATS:
    non_markdown_files.append(file)

IF non_markdown_files.length > 0:

  ═══════════════════════════════════════════════════════════════
  📄 DOCUMENT CONVERSION AVAILABLE
  ═══════════════════════════════════════════════════════════════

  Found {non_markdown_files.length} documents that can be converted to markdown:

  | # | File | Format | Size | Location |
  |---|------|--------|------|----------|
  {FOR i, file in non_markdown_files:
    | {i+1} | {file.name} | {file.extension} | {file.size} | {file.relative_path} |
  }

  MarkItDown can convert these to markdown for better extraction.

  Benefits:
  • Extracts text from PDFs, Word docs, PowerPoints
  • Preserves tables from Excel/CSV
  • OCR for images (wireframes, whiteboard photos)
  • Clean, structured markdown output

  Options:
  1. "convert all" - Convert all documents to markdown
  2. "convert: 1,3,5" - Convert specific files by number
  3. "preview: [filename]" - Preview what will be extracted
  4. "skip" - Process only existing markdown files
  ═══════════════════════════════════════════════════════════════

  WAIT for user response

IF user selects conversion:

  // Ensure markitdown is installed
  LOG: "Checking markitdown installation..."

  RUN: pip install 'markitdown[all]' --quiet 2>/dev/null || pip install markitdown

  // Create converted documents directory
  CREATE discovery/_converted/ directory

  converted_files = []
  conversion_errors = []

  FOR each file in files_to_convert:

    LOG: "📄 Converting: {file.name}..."

    output_path = "discovery/_converted/{file.stem}.md"

    // Determine conversion method based on file type
    CASE file.extension:

      ".pdf":
        // PDF conversion - handles text, tables, basic layout
        TRY:
          RUN: markitdown "{file.path}" -o "{output_path}"

          // For large/complex PDFs, offer enhanced conversion
          IF file.size > 5MB:
            PROMPT: "Large PDF ({file.size}). Use enhanced extraction? (y/n)"
            IF yes AND docintel_available:
              RUN: markitdown "{file.path}" -o "{output_path}" -d -e "{docintel_endpoint}"

          LOG: "✅ Converted: {file.name}"
          converted_files.append({original: file, output: output_path})

        CATCH error:
          LOG: "⚠️ PDF conversion failed: {error}"
          conversion_errors.append({file: file, error: error})

      ".docx":
        // Word document - preserves headings, tables, formatting
        TRY:
          RUN: markitdown "{file.path}" -o "{output_path}"
          LOG: "✅ Converted: {file.name}"
          converted_files.append({original: file, output: output_path})
        CATCH error:
          conversion_errors.append({file: file, error: error})

      ".pptx":
        // PowerPoint - extracts slides with speaker notes
        TRY:
          // Check if images need AI descriptions
          IF file contains embedded images:
            PROMPT: "PowerPoint contains images/diagrams. Generate AI descriptions? (y/n)"

            IF yes AND openrouter_available:
              // Use Python API with vision model
              EXECUTE python:
                from markitdown import MarkItDown
                from openai import OpenAI
                import os

                client = OpenAI(
                  api_key=os.environ.get("OPENROUTER_API_KEY"),
                  base_url="https://openrouter.ai/api/v1"
                )

                md = MarkItDown(
                  llm_client=client,
                  llm_model="anthropic/claude-sonnet-4.5",
                  llm_prompt="Describe this slide image focusing on: diagrams, workflows, data structures, UI mockups, and key information presented."
                )

                result = md.convert("{file.path}")
                with open("{output_path}", "w") as f:
                  f.write(result.text_content)

            ELSE:
              RUN: markitdown "{file.path}" -o "{output_path}"

          ELSE:
            RUN: markitdown "{file.path}" -o "{output_path}"

          LOG: "✅ Converted: {file.name}"
          converted_files.append({original: file, output: output_path})

        CATCH error:
          conversion_errors.append({file: file, error: error})

      ".xlsx":
        // Excel - converts sheets to markdown tables
        TRY:
          RUN: markitdown "{file.path}" -o "{output_path}"
          LOG: "✅ Converted: {file.name}"
          converted_files.append({original: file, output: output_path})
        CATCH error:
          conversion_errors.append({file: file, error: error})

      ".csv":
        // CSV - direct table conversion
        TRY:
          RUN: markitdown "{file.path}" -o "{output_path}"
          LOG: "✅ Converted: {file.name}"
          converted_files.append({original: file, output: output_path})
        CATCH error:
          conversion_errors.append({file: file, error: error})

      ".html":
        // HTML - clean conversion to markdown
        TRY:
          RUN: markitdown "{file.path}" -o "{output_path}"
          LOG: "✅ Converted: {file.name}"
          converted_files.append({original: file, output: output_path})
        CATCH error:
          conversion_errors.append({file: file, error: error})

      ".png" | ".jpg" | ".jpeg" | ".gif" | ".webp":
        // Images - OCR extraction for wireframes, whiteboard photos
        LOG: "🔍 Extracting text from image via OCR..."

        TRY:
          // Basic OCR extraction
          RUN: markitdown "{file.path}" -o "{output_path}"

          // Offer AI description for richer context (wireframes, diagrams)
          PROMPT: "Image detected. Generate AI description for better context? (y/n)"

          IF yes AND openrouter_available:
            EXECUTE python:
              from markitdown import MarkItDown
              from openai import OpenAI
              import os

              client = OpenAI(
                api_key=os.environ.get("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1"
              )

              md = MarkItDown(
                llm_client=client,
                llm_model="anthropic/claude-sonnet-4.5",
                llm_prompt="Describe this image in detail. If it's a wireframe or UI mockup, list all screens, components, and interactions shown. If it's a diagram, explain the entities and relationships."
              )

              result = md.convert("{file.path}")
              with open("{output_path}", "w") as f:
                f.write(result.text_content)

          LOG: "✅ Extracted: {file.name}"
          converted_files.append({original: file, output: output_path})

        CATCH error:
          LOG: "⚠️ Image extraction failed: {error}"
          conversion_errors.append({file: file, error: error})

      ".json":
        // JSON - structured representation
        TRY:
          RUN: markitdown "{file.path}" -o "{output_path}"
          LOG: "✅ Converted: {file.name}"
          converted_files.append({original: file, output: output_path})
        CATCH error:
          conversion_errors.append({file: file, error: error})

      ".xml":
        // XML - structured format
        TRY:
          RUN: markitdown "{file.path}" -o "{output_path}"
          LOG: "✅ Converted: {file.name}"
          converted_files.append({original: file, output: output_path})
        CATCH error:
          conversion_errors.append({file: file, error: error})

  // Generate conversion summary
  ═══════════════════════════════════════════════════════════════
  📄 DOCUMENT CONVERSION COMPLETE
  ═══════════════════════════════════════════════════════════════

  Successfully converted: {converted_files.length}/{files_to_convert.length}

  | Original | Converted | Status |
  |----------|-----------|--------|
  {FOR file in converted_files:
    | {file.original.name} | {file.output} | ✅ |
  }
  {FOR err in conversion_errors:
    | {err.file.name} | - | ❌ {err.error} |
  }

  Converted files saved to: discovery/_converted/

  These will now be included in discovery extraction.
  ═══════════════════════════════════════════════════════════════

  // Create conversion manifest
  CREATE discovery/_converted/CONVERSION_MANIFEST.md:
    # Document Conversion Manifest

    **Converted at:** {timestamp}
    **Tool:** MarkItDown

    ## Converted Files

    | Original | Format | Converted | Size |
    |----------|--------|-----------|------|
    {list all conversions}

    ## Conversion Notes

    {any special handling notes}

    ## How to Use

    These markdown files are now included in discovery extraction.
    Original files preserved in their original locations.

  // Update discovery paths to include converted files
  FOR each converted in converted_files:
    discovery_documents.append(converted.output)

ELSE:
  LOG: "Skipping document conversion (not selected or no convertible files)"
```

### Step 2: Validate Required Sections
```
REQUIRED_SECTIONS = [
  "01-stakeholder-interviews",
  "02-user-research",
  "04-design-specs"
]

OPTIONAL_SECTIONS = [
  "03-competitive-analysis"
]

FOR each required section:
  CHECK directory exists
  CHECK contains at least 1 .md file
  
  IF missing:
    ADD to missing_sections[]

IF missing_sections.length > 0:
  ═══════════════════════════════════════════
  ⚠️ INCOMPLETE DISCOVERY
  ═══════════════════════════════════════════
  
  Missing required sections:
  • {list missing sections}
  
  How would you like to proceed?
  1. "continue" - Proceed with available data
  2. "provide: [section]" - Add missing section
  3. "abort" - Stop and complete discovery
  ═══════════════════════════════════════════
  
  WAIT for user response
```

### Step 3: Extract Stakeholder Data
```
READ discovery/01-stakeholder-interviews/*.md

EXTRACT:
  stakeholders: [
    {
      name: "...",
      role: "...",
      key_insights: ["..."],
      pain_points: ["..."],
      requirements_mentioned: ["..."]
    }
  ]
  
  brand_guidelines: {
    colors: [],
    typography: [],
    voice_tone: ""
  }
```

### Step 4: Extract User Research Data
```
READ discovery/02-user-research/personas/*.md

EXTRACT:
  personas: [
    {
      id: "persona-recruiter",
      name: "Sarah Johnson",
      role: "Recruiter",
      goals: ["..."],
      frustrations: ["..."],
      daily_tasks: ["..."],
      tech_savviness: "high|medium|low"
    }
  ]

READ discovery/02-user-research/pain-points.md

EXTRACT:
  pain_points: [
    {
      id: "PP-001",
      description: "Manual tracking in spreadsheets",
      severity: "high",
      personas_affected: ["recruiter", "hiring-manager"],
      current_workaround: "..."
    }
  ]
```

### Step 5: Extract Design Specifications
```
READ discovery/04-design-specs/data-fields.md

EXTRACT:
  entities: [
    {
      name: "Candidate",
      fields: ["firstName", "lastName", "email", ...],
      relationships: ["has many Applications"]
    }
  ]

READ discovery/04-design-specs/screen-definitions.md

EXTRACT:
  screens: [
    {
      name: "Candidate Pipeline",
      app: "recruiter",
      purpose: "View and manage candidates by stage",
      primary_actions: ["move candidate", "filter", "search"]
    }
  ]

READ discovery/04-design-specs/workflows.md (if exists)

EXTRACT:
  workflows: [
    {
      name: "Interview Scheduling",
      steps: ["select candidate", "check availability", ...],
      actors: ["recruiter", "interviewer"]
    }
  ]
```

### Step 6: Identify Gaps
```
ANALYZE extracted data for gaps:

CRITICAL_GAPS (blocking):
  - No personas defined
  - No pain points identified
  - No entities specified
  - No screens defined

MAJOR_GAPS (warning):
  - Fewer than 3 personas
  - Fewer than 5 pain points
  - No workflows defined
  - Missing competitive analysis

MINOR_GAPS (informational):
  - Missing brand guidelines
  - No user journeys
  - Incomplete stakeholder interviews

FOR each gap found:
  ADD to gaps[]
```

### Step 6.5: Interactive Gap Filling (Phase 4 Enhancement)

> **brainstorming Integration**: When discovery has gaps, use collaborative questioning to fill them.

```
// ═══════════════════════════════════════════════════════════
// PHASE 4: BRAINSTORMING FOR GAP REMEDIATION
// ═══════════════════════════════════════════════════════════

IF critical_gaps.length > 0 OR major_gaps.length > 0:

  ═══════════════════════════════════════════
  💡 DISCOVERY GAP REMEDIATION
  ═══════════════════════════════════════════

  Discovery documents have gaps that could affect prototype quality.

  Would you like to:
  1. "fill gaps" - Interactively fill missing information
  2. "show gaps" - Review all gaps first
  3. "skip" - Continue with available data (not recommended)
  ═══════════════════════════════════════════

  IF user selects "fill gaps":

    // BRAINSTORMING PROCESS
    // Key principles from brainstorming skill:
    // - Ask ONE question at a time
    // - Prefer multiple choice when possible
    // - Present 2-3 approaches for ambiguous areas
    // - Validate answers incrementally

    FOR each gap in [critical_gaps, major_gaps]:

      // Step 1: Present the gap
      ═══════════════════════════════════════════
      📋 Gap {gap.id}: {gap.description}
      ═══════════════════════════════════════════

      Severity: {gap.severity}
      Impact: {gap.impact}

      // Step 2: Ask ONE focused question
      CASE gap.type:

        "missing_personas":
          ═══════════════════════════════════════════
          ❓ Who are the primary users of this system?

          Select user types (or describe your own):
          A) Operations Staff - Daily system users
          B) Managers - Oversight and approvals
          C) Administrators - System configuration
          D) External Users - Customers/partners
          E) Other: [describe]

          (You can select multiple, e.g., "A, B, D")
          ═══════════════════════════════════════════

          WAIT for user response
          CAPTURE selected_users

          // Follow-up for each selected user type
          FOR each user_type in selected_users:
            ═══════════════════════════════════════════
            📝 Tell me about the {user_type}:

            What are their 2-3 main goals?
            (e.g., "Process orders quickly, Track inventory, Generate reports")
            ═══════════════════════════════════════════

            WAIT for response
            CAPTURE goals

            ═══════════════════════════════════════════
            What frustrates them most today?
            (e.g., "Manual data entry, Slow searches, Lack of visibility")
            ═══════════════════════════════════════════

            WAIT for response
            CAPTURE frustrations

            // Build persona from responses
            ADD to discovery_summary.personas:
              {
                id: "persona-{user_type}",
                name: "[Generated Name]",
                role: user_type,
                goals: parse(goals),
                frustrations: parse(frustrations)
              }

        "missing_pain_points":
          ═══════════════════════════════════════════
          ❓ What are the biggest pain points in the current process?

          Common categories:
          A) Efficiency - Tasks take too long
          B) Accuracy - Errors and data quality issues
          C) Visibility - Hard to find information
          D) Communication - Coordination problems
          E) Compliance - Regulatory/policy challenges

          Select categories that apply (or describe specific issues):
          ═══════════════════════════════════════════

          WAIT for response

          FOR each selected category:
            ═══════════════════════════════════════════
            📝 Describe a specific {category} pain point:

            Example: "Manual tracking in spreadsheets leads to duplicate entries"
            ═══════════════════════════════════════════

            WAIT for response
            CAPTURE pain_point_description

            ═══════════════════════════════════════════
            How severe is this? (1-5)
            1 = Minor inconvenience
            3 = Significant productivity impact
            5 = Critical business blocker
            ═══════════════════════════════════════════

            WAIT for response

            ADD to discovery_summary.pain_points:
              {
                id: "PP-{next_id}",
                description: pain_point_description,
                severity: map_severity(response),
                category: category
              }

        "missing_entities":
          ═══════════════════════════════════════════
          ❓ What are the main "things" this system manages?

          Examples:
          - E-commerce: Products, Orders, Customers, Inventory
          - HR System: Employees, Departments, Jobs, Payroll
          - Project Management: Projects, Tasks, Teams, Resources

          List the main entities (comma-separated):
          ═══════════════════════════════════════════

          WAIT for response
          CAPTURE entities_list

          FOR each entity in parse(entities_list):
            ═══════════════════════════════════════════
            📝 What key information does a {entity} have?

            Examples for "Customer": name, email, phone, address, status
            List fields for {entity} (comma-separated):
            ═══════════════════════════════════════════

            WAIT for response
            CAPTURE fields

            ADD to discovery_summary.entities:
              {
                name: entity,
                fields: parse(fields),
                relationships: []  // Will infer later
              }

        "missing_screens":
          ═══════════════════════════════════════════
          ❓ What are the main screens/views needed?

          Common patterns:
          A) Dashboard - Overview with key metrics
          B) List View - Browse and search items
          C) Detail View - Full item information
          D) Form - Create/edit items
          E) Report - Analytics and exports

          Which patterns apply? (Select all that apply)
          ═══════════════════════════════════════════

          WAIT for response

          FOR each entity in discovery_summary.entities:
            ═══════════════════════════════════════════
            For {entity}, which screens are needed?

            A) List View - Browse {entity} records
            B) Detail View - View single {entity}
            C) Create/Edit Form - Add or modify {entity}
            D) Dashboard - {entity} metrics and status
            E) Other: [describe]

            (e.g., "A, B, C")
            ═══════════════════════════════════════════

            WAIT for response

            FOR each selected screen:
              ADD to discovery_summary.screens:
                {
                  name: "{entity} {screen_type}",
                  purpose: "Manage {entity} records",
                  primary_actions: infer_from_type(screen_type)
                }

        "few_pain_points":
          ═══════════════════════════════════════════
          📝 We have {count} pain points. Can you add 2-3 more?

          Current pain points:
          {list existing}

          What else causes friction in the current process?
          ═══════════════════════════════════════════

          // Continue until 5+ pain points

      // Validate incrementally
      ═══════════════════════════════════════════
      ✅ Gap filled: {gap.id}

      Current status:
      - Personas: {count} defined
      - Pain Points: {count} identified
      - Entities: {count} specified
      - Screens: {count} planned

      Continue to next gap? (y/n)
      ═══════════════════════════════════════════

    // Final validation
    RECALCULATE gaps after filling

    IF remaining_critical_gaps > 0:
      ═══════════════════════════════════════════
      ⚠️ Some critical gaps remain unfilled.

      Remaining gaps:
      {list remaining}

      How would you like to proceed?
      1. "continue filling" - Address remaining gaps
      2. "proceed anyway" - Continue with limitations
      3. "abort" - Stop and gather more discovery
      ═══════════════════════════════════════════

    ELSE:
      LOG: "✅ All critical gaps filled through brainstorming"

// Update discovery_summary.json with filled data
WRITE updated discovery_summary to _state/discovery_summary.json
```

### Step 7: Generate Gap Remediation Plan
```
IF gaps.length > 0:
  CREATE _state/GAP_REMEDIATION_PLAN.md:
    # Gap Remediation Plan
    
    ## Summary
    
    | Severity | Count |
    |----------|-------|
    | Critical | {count} |
    | Major | {count} |
    | Minor | {count} |
    
    ---
    
    ## Critical Gaps (Must Fix)
    
    ### GAP-001: {description}
    **Impact:** Cannot proceed without this
    **Remediation:** {steps to fix}
    **Owner:** {suggested owner}
    **Due:** Before prototype generation
    
    ---
    
    ## Major Gaps (Should Fix)
    
    ### GAP-002: {description}
    **Impact:** Reduced prototype quality
    **Remediation:** {steps}
    **Can Proceed:** Yes, with limitations
    
    ---
    
    ## Minor Gaps (Nice to Have)
    
    [List minor gaps]
    
    ---
    
    ## Next Steps
    
    1. Address all critical gaps
    2. Review major gaps with stakeholders
    3. Proceed with prototype generation

IF critical gaps exist:
  PROMPT user for resolution before continuing
```

### Step 7.5: Generate Screen Registry (CRITICAL - NEW)

> **SCREEN TRACEABILITY**: This step creates the master screen registry that ensures ALL Discovery screens are tracked through to implementation.

```
// ═══════════════════════════════════════════════════════════
// SCREEN REGISTRY GENERATION (MANDATORY)
// ═══════════════════════════════════════════════════════════

// Step 1: Read Discovery screen-definitions.md
READ discovery/04-design-specs/screen-definitions.md AS screen_definitions

// Step 2: Extract ALL screens with IDs
// Pattern matches: | M-01 | Screen Name | P0 | or | D-01 | Screen Name | P0 |
discovery_screens = []

FOR each table row in screen_definitions:
  IF row matches pattern "|<ID>|<Name>|<Priority>|":
    // Extract screen ID (e.g., M-01, D-01, D-12)
    screen_id = extract_id(row)  // M-01, M-02, D-01, etc.
    screen_name = extract_name(row)
    priority = extract_priority(row)  // P0, P1, P2

    discovery_screens.append({
      "id": screen_id,
      "name": screen_name,
      "priority": priority,
      "platform": "mobile" if screen_id.startswith("M") else "desktop",
      "source_file": "04-design-specs/screen-definitions.md",
      "source_line": row_number
    })

// Step 3: Validate extraction
IF discovery_screens.length == 0:
  ═══════════════════════════════════════════
  ❌ NO SCREENS FOUND IN DISCOVERY
  ═══════════════════════════════════════════

  Could not extract screen definitions from:
  discovery/04-design-specs/screen-definitions.md

  Expected format:
  | ID | Name | Priority |
  | M-01 | Task Execution | P0 |
  | D-01 | Dashboard | P0 |

  BLOCK: Cannot proceed without screen definitions
  ═══════════════════════════════════════════

// Step 4: Count by priority and platform
screen_counts = {
  "total": discovery_screens.length,
  "by_priority": {
    "P0": count where priority == "P0",
    "P1": count where priority == "P1",
    "P2": count where priority == "P2"
  },
  "by_platform": {
    "mobile": count where platform == "mobile",
    "desktop": count where platform == "desktop"
  }
}

// Step 5: Initialize traceability array
traceability = []
FOR each screen in discovery_screens:
  traceability.append({
    "screen_id": screen.id,
    "screen_name": screen.name,
    "priority": screen.priority,
    "discovery_source": screen.source_file,
    "spec_folder": null,        // Will be set by Prototype_Screens
    "spec_status": "pending",   // pending → complete
    "code_file": null,          // Will be set by Prototype_CodeGen
    "code_status": "pending",   // pending → complete
    "test_status": "pending",   // Will be set by Prototype_QA
    "created_at": NOW_ISO(),
    "updated_at": NOW_ISO()
  })

// Step 6: Create screen_registry.json
CREATE traceability/screen_registry.json:
{
  "$metadata": {
    "document_id": "STATE-SCREEN-REGISTRY-001",
    "version": "1.0.0",
    "created_at": NOW_ISO(),
    "updated_at": NOW_ISO(),
    "generated_by": "Prototype_ValidateDiscovery",
    "purpose": "Master registry tracking Discovery screens through implementation"
  },
  "discovery_source": {
    "folder": "ClientAnalysis_<SystemName>/",
    "screen_definitions_file": "04-design-specs/screen-definitions.md",
    "extracted_at": NOW_ISO()
  },
  "discovery_screens": discovery_screens,
  "screen_counts": screen_counts,
  "screen_coverage": {
    "discovery_total": discovery_screens.length,
    "specs_generated": 0,
    "specs_missing": discovery_screens.length,
    "spec_coverage_percent": 0,
    "code_generated": 0,
    "code_missing": discovery_screens.length,
    "code_coverage_percent": 0,
    "tests_passed": 0,
    "test_coverage_percent": 0
  },
  "traceability": traceability,
  "validation_rules": {
    "all_screens_must_have_specs": true,
    "all_screens_must_have_code": true,
    "p0_screens_must_have_tests": true
  }
}

// Step 7: Display extraction summary
═══════════════════════════════════════════════════════════════
📋 SCREEN REGISTRY CREATED
═══════════════════════════════════════════════════════════════

Extracted {discovery_screens.length} screens from Discovery:

By Priority:
├── P0 (Critical): {screen_counts.by_priority.P0}
├── P1 (Important): {screen_counts.by_priority.P1}
└── P2 (Nice-to-have): {screen_counts.by_priority.P2}

By Platform:
├── Mobile: {screen_counts.by_platform.mobile}
└── Desktop: {screen_counts.by_platform.desktop}

Screen List:
{FOR each screen in discovery_screens:
  • {screen.id}: {screen.name} [{screen.priority}]
}

Registry saved to: traceability/screen_registry.json

⚠️ ENFORCEMENT: All {discovery_screens.length} screens MUST be:
   1. Specified in 02-screens/ (Checkpoint 9)
   2. Implemented in prototype/src/ (Checkpoint 12)
   3. Tested in QA (Checkpoint 13)
═══════════════════════════════════════════════════════════════

LOG: "✅ Screen registry created with {discovery_screens.length} screens"
```

---

### Step 8: Generate Discovery Summary
```
CREATE _state/discovery_summary.json:
  {
    "version": "1.0",
    "validated_at": "timestamp",
    "validation_status": "complete|partial|failed",
    
    "stakeholders": [...],
    
    "personas": [...],
    
    "pain_points": [...],
    
    "entities": [...],
    
    "screens": [...],
    
    "workflows": [...],
    
    "brand": {...},
    
    "gaps": {
      "critical": [],
      "major": [],
      "minor": []
    },
    
    "metrics": {
      "stakeholder_count": N,
      "persona_count": N,
      "pain_point_count": N,
      "entity_count": N,
      "screen_count": N
    }
  }
```

### Step 9: Validate Outputs (REQUIRED)
```
VALIDATE discovery summary:
  CHECKS:
    - discovery_summary.json exists
    - At least 1 persona extracted
    - At least 1 pain point extracted
    - At least 1 entity extracted
    - At least 1 screen extracted
    - No critical gaps (or user accepted)
    
IF validation fails:
  PROMPT with specific issues and mitigation options
```

### Step 10: Update Progress
```
CREATE or UPDATE _state/progress.json:
  {
    "schema_version": "2.3",
    "pipeline_status": "in_progress",
    "started_at": "timestamp",
    
    "phases": {
      "validate_discovery": {
        "status": "complete",
        "completed_at": "timestamp",
        "outputs": [
          "_state/discovery_summary.json",
          "_state/GAP_REMEDIATION_PLAN.md"
        ],
        "validation": {
          "status": "passed|passed_with_warnings",
          "checks_run": N,
          "checks_passed": N,
          "warnings": []
        },
        "metrics": {
          "stakeholders": N,
          "personas": N,
          "pain_points": N,
          "entities": N,
          "screens": N,
          "gaps_critical": N,
          "gaps_major": N
        }
      }
    }
  }

CREATE or UPDATE _state/PROGRESS.md:
  # Prototype Progress
  
  ## Current Status: Discovery Validated
  
  ### Phases
  | Phase | Status | Date |
  |-------|--------|------|
  | Validate Discovery | ✅ Complete | {date} |
  | Requirements | ⏳ Pending | |
  
  ### Metrics
  - Personas: {N}
  - Pain Points: {N}
  - Entities: {N}
  - Screens: {N}
  
  ### Gaps Identified
  [List if any]
```

---

## Output Files (REQUIRED)

| Path | Purpose | Blocking? |
|------|---------|-----------|
| `_state/discovery_summary.json` | Extracted data | ✅ Yes |
| `traceability/screen_registry.json` | **Master screen tracking** | ✅ Yes |
| `_state/GAP_REMEDIATION_PLAN.md` | Gap documentation | ⚠️ If gaps |
| `_state/progress.json` | Progress tracking | ✅ Yes |
| `_state/PROGRESS.md` | Human-readable status | ✅ Yes |

### screen_registry.json Schema

```json
{
  "$metadata": { ... },
  "discovery_source": {
    "folder": "ClientAnalysis_<SystemName>/",
    "screen_definitions_file": "04-design-specs/screen-definitions.md"
  },
  "discovery_screens": [
    { "id": "M-01", "name": "Task Execution", "priority": "P0", "platform": "mobile" },
    { "id": "D-01", "name": "Dashboard", "priority": "P0", "platform": "desktop" }
  ],
  "screen_counts": { "total": 18, "by_priority": {...}, "by_platform": {...} },
  "screen_coverage": {
    "discovery_total": 18,
    "specs_generated": 0,
    "code_generated": 0
  },
  "traceability": [
    {
      "screen_id": "M-01",
      "screen_name": "Task Execution",
      "priority": "P0",
      "spec_status": "pending",
      "code_status": "pending",
      "test_status": "pending"
    }
  ]
}
```

---

## Validation Criteria

| Check | Requirement | Blocking? |
|-------|-------------|-----------|
| Discovery exists | Directory present | ✅ Yes |
| Has personas | At least 1 | ✅ Yes |
| Has pain points | At least 1 | ✅ Yes |
| Has entities | At least 1 | ✅ Yes |
| Has screens | At least 1 | ✅ Yes |
| No critical gaps | Or user accepted | ✅ Yes |

---

## Progress.json Update

```json
{
  "schema_version": "2.3",
  "pipeline_status": "in_progress",
  "started_at": "2024-12-13T09:00:00Z",
  
  "phases": {
    "validate_discovery": {
      "status": "complete",
      "completed_at": "2024-12-13T09:15:00Z",
      "outputs": [
        "_state/discovery_summary.json",
        "_state/GAP_REMEDIATION_PLAN.md"
      ],
      "validation": {
        "status": "passed",
        "checks_run": 7,
        "checks_passed": 7
      },
      "metrics": {
        "stakeholders": 5,
        "personas": 4,
        "pain_points": 12,
        "entities": 15,
        "screens": 18,
        "gaps_critical": 0,
        "gaps_major": 2
      }
    }
  }
}
```
