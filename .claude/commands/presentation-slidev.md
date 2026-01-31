---
name: presentation-slidev
description: Generate web-based technical presentations using Slidev with interactive configuration for source files, audience, key messages, and presentation settings.
---

# /presentation-slidev - Interactive Slidev Presentation Generator

**Version**: 1.0.0
**Created**: 2026-01-27
**Author**: Framework Integration

---

## Overview

Interactive command to generate professional web-based presentations using Slidev. Asks user for source materials, audience, key messages, detail level, speaker notes preference, diagram format, and project name, then generates an optimized Slidev presentation.

---

## Usage

```bash
/presentation-slidev
```

The command will interactively ask for all configuration parameters.

---

## Procedure

### Step 1: Ask for Source Files/Folders

```
DISPLAY:
  ═══════════════════════════════════════════
  📂 SOURCE SELECTION
  ═══════════════════════════════════════════

  What files or folders should be the source for this presentation?

  Examples:
  - ClientAnalysis_InventorySystem/
  - Prototype_InventorySystem/
  - ProductSpecs_InventorySystem/
  - SolArch_InventorySystem/
  - Multiple: ClientAnalysis_X/,Prototype_X/

  Enter source path(s):
  ═══════════════════════════════════════════

WAIT for user input
STORE source_paths[]
VALIDATE: All paths exist

LOG: "Source files selected: {source_paths}"
```

### Step 2: Ask for Audience

```
DISPLAY:
  ═══════════════════════════════════════════
  👥 AUDIENCE DEFINITION
  ═══════════════════════════════════════════

  Who is the target audience for this presentation?

  Examples:
  - "C-level executives and stakeholders"
  - "Development team and technical architects"
  - "Product managers and business analysts"
  - "Mixed audience (technical + business)"
  - "Conference attendees (developers)"

  Enter target audience:
  ═══════════════════════════════════════════

WAIT for user input
STORE audience

LOG: "Target audience: {audience}"
```

### Step 3: Ask for 3 Key Messages

```
DISPLAY:
  ═══════════════════════════════════════════
  🎯 KEY MESSAGES (3 Required)
  ═══════════════════════════════════════════

  What are the 3 key messages you must deliver?

  Message 1:
  Message 2:
  Message 3:

  Enter each message (press Enter between):
  ═══════════════════════════════════════════

WAIT for user input (3 messages)
STORE key_messages[3]

LOG: "Key messages defined: {key_messages}"
```

### Step 4: Ask for Detail Level

```
DISPLAY:
  ═══════════════════════════════════════════
  📊 DETAIL LEVEL
  ═══════════════════════════════════════════

  How detailed should the presentation be?

  [1] Executive Summary (10-15 slides, high-level)
  [2] Standard Overview (20-30 slides, balanced)
  [3] Detailed Deep-Dive (40+ slides, comprehensive)
  [4] Workshop Format (50+ slides, interactive)

  Select detail level (1-4):
  ═══════════════════════════════════════════

WAIT for user selection
STORE detail_level

SLIDE_COUNT_MAP = {
  1: "10-15",
  2: "20-30",
  3: "40-50",
  4: "50+"
}

LOG: "Detail level: {detail_level} ({SLIDE_COUNT_MAP[detail_level]} slides)"
```

### Step 5: Ask for Speaker Notes

```
DISPLAY:
  ═══════════════════════════════════════════
  📝 SPEAKER NOTES
  ═══════════════════════════════════════════

  Do you need speaker notes for each slide?

  [y] Yes - Include detailed speaker notes
  [n] No - Slides only
  [c] Critical slides only - Add notes to key slides

  Include speaker notes? (y/n/c):
  ═══════════════════════════════════════════

WAIT for user input
STORE speaker_notes_mode

LOG: "Speaker notes: {speaker_notes_mode}"
```

### Step 6: Ask for Diagram Format

```
DISPLAY:
  ═══════════════════════════════════════════
  🎨 DIAGRAM FORMAT
  ═══════════════════════════════════════════

  Which diagram format should be used?

  [1] Mermaid - Flowcharts, sequence, class diagrams
  [2] PlantUML - UML diagrams, architecture
  [3] Both - Use Mermaid for flows, PlantUML for architecture
  [4] None - Text/images only

  Select diagram format (1-4):
  ═══════════════════════════════════════════

WAIT for user selection
STORE diagram_format

DIAGRAM_MAP = {
  1: "mermaid",
  2: "plantuml",
  3: "both",
  4: "none"
}

LOG: "Diagram format: {DIAGRAM_MAP[diagram_format]}"
```

### Step 7: Ask for Project Name

```
DISPLAY:
  ═══════════════════════════════════════════
  📛 PROJECT NAME
  ═══════════════════════════════════════════

  What is the name of this presentation project?

  Example: "InventorySystem_Overview_2026"

  Enter project name:
  ═══════════════════════════════════════════

WAIT for user input
STORE project_name

SANITIZE project_name (remove special chars, spaces -> underscores)

LOG: "Project name: {project_name}"
```

### Step 8: Generate Slidev Configuration

```
CREATE slidev_config.json:
  {
    "source_paths": source_paths,
    "audience": audience,
    "key_messages": key_messages,
    "detail_level": detail_level,
    "slide_count": SLIDE_COUNT_MAP[detail_level],
    "speaker_notes": speaker_notes_mode,
    "diagram_format": DIAGRAM_MAP[diagram_format],
    "project_name": project_name,
    "output_path": "presentations/{project_name}/",
    "theme": "default",
    "timestamp": ISO_8601_now()
  }

SAVE to _state/slidev_config.json

LOG: "✅ Configuration saved to _state/slidev_config.json"
```

### Step 9: Generate Content Outline

```
ANALYZE source_paths:
  - Read all markdown files
  - Extract headings, key points, data
  - Identify diagrams, images, code snippets
  - Map to key_messages

CREATE content_outline:
  sections[] = [
    {
      title: "Introduction",
      slides: ["Title", "Agenda", "Context"],
      key_message: key_messages[0]
    },
    {
      title: "Main Content",
      slides: [extracted from source_paths],
      key_message: key_messages[1]
    },
    {
      title: "Conclusion",
      slides: ["Summary", "Key Takeaways", "Next Steps"],
      key_message: key_messages[2]
    }
  ]

ADJUST section.slides count based on detail_level

SAVE content_outline to presentations/{project_name}/outline.json

LOG: "✅ Content outline generated"
```

### Step 10: Generate Slidev Markdown

```
CREATE presentations/{project_name}/slides.md:

  ---
  theme: default
  title: {project_name}
  class: text-center
  highlighter: shiki
  drawings:
    persist: false
  transition: slide-left
  mdc: true
  ---

  # {project_name}

  {audience} Presentation

  <div class="pt-12">
    <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
      Press Space for next page <carbon:arrow-right class="inline"/>
    </span>
  </div>

  <!--
  Speaker notes: {IF speaker_notes_mode}
  Welcome to the {project_name} presentation.
  -->

  ---
  layout: default
  ---

  # Agenda

  <v-clicks>

  - {key_messages[0]}
  - {key_messages[1]}
  - {key_messages[2]}

  </v-clicks>

  ---

  FOR each section in content_outline:
    FOR each slide in section.slides:

      ---
      layout: {choose_layout(slide.type)}
      ---

      # {slide.title}

      {slide.content}

      {IF diagram_format AND slide.has_diagram:
        ```{diagram_format}
        {slide.diagram_code}
        ```
      }

      {IF speaker_notes_mode AND (speaker_notes_mode == "y" OR slide.is_critical):
        <!--
        {slide.speaker_notes}
        -->
      }

  ---
  layout: center
  class: text-center
  ---

  # Key Takeaways

  <v-clicks>

  - {key_messages[0]}
  - {key_messages[1]}
  - {key_messages[2]}

  </v-clicks>

  ---
  layout: end
  ---

  # Thank You

  Questions?

SAVE to presentations/{project_name}/slides.md

LOG: "✅ Slidev markdown generated"
```

### Step 11: Create package.json and Setup

```
CREATE presentations/{project_name}/package.json:

  {
    "name": "{project_name}",
    "version": "1.0.0",
    "scripts": {
      "dev": "slidev",
      "build": "slidev build",
      "export": "slidev export"
    },
    "dependencies": {
      "@slidev/cli": "latest",
      "@slidev/theme-default": "latest"
    }
  }

IF diagram_format == "plantuml":
  ADD to package.json:
    "dependencies": {
      "@slidev/plantuml": "latest"
    }

SAVE package.json

LOG: "✅ Package.json created"
```

### Step 12: Install Dependencies and Start Dev Server

```
DISPLAY:
  ═══════════════════════════════════════════
  🚀 SLIDEV READY
  ═══════════════════════════════════════════

  Presentation generated at:
  presentations/{project_name}/slides.md

  To start the dev server:

  cd presentations/{project_name}
  npm install
  npm run dev

  To export to PDF:
  npm run export

  To build for deployment:
  npm run build

  ═══════════════════════════════════════════

ASK USER:
  "Would you like to start the dev server now? (y/n)"

IF yes:
  EXECUTE:
    cd presentations/{project_name}
    npm install
    npm run dev

  LOG: "✅ Slidev dev server started at http://localhost:3030"

ELSE:
  LOG: "✅ Presentation ready. Run 'npm run dev' in presentations/{project_name}/ to start."
```

### Step 13: Generate README

```
CREATE presentations/{project_name}/README.md:

  # {project_name} - Slidev Presentation

  **Generated**: {timestamp}
  **Audience**: {audience}

  ## Key Messages

  1. {key_messages[0]}
  2. {key_messages[1]}
  3. {key_messages[2]}

  ## Configuration

  - **Detail Level**: {detail_level} ({slide_count} slides)
  - **Speaker Notes**: {speaker_notes_mode}
  - **Diagram Format**: {diagram_format}

  ## Commands

  ```bash
  # Start dev server
  npm run dev

  # Export to PDF
  npm run export

  # Build for deployment
  npm run build
  ```

  ## Source Files

  {LIST source_paths}

  ## Customization

  Edit `slides.md` to modify slides.
  See https://sli.dev for full documentation.

SAVE README.md

LOG: "✅ README.md created"
```

---

## Output Structure

```
presentations/{project_name}/
├── slides.md                 # Main presentation file
├── package.json              # Dependencies and scripts
├── README.md                 # Documentation
├── outline.json              # Content structure
└── dist/                     # Built presentation (after npm run build)
    ├── index.html
    └── assets/
```

---

## Configuration File

All user selections are saved to `_state/slidev_config.json` for reference and future regeneration.

---

## Examples

### Example 1: Discovery Presentation for Executives

```
Source: ClientAnalysis_InventorySystem/
Audience: C-level executives and stakeholders
Key Messages:
  1. Users face 5 critical pain points in current inventory system
  2. Proposed solution addresses all P0 requirements
  3. ROI expected within 6 months
Detail Level: Executive Summary (10-15 slides)
Speaker Notes: Critical slides only
Diagrams: Mermaid
Project Name: InventorySystem_ExecutiveBrief_2026
```

### Example 2: Technical Deep-Dive for Developers

```
Source: SolArch_InventorySystem/,ProductSpecs_InventorySystem/
Audience: Development team and technical architects
Key Messages:
  1. Microservices architecture with event-driven patterns
  2. React + TypeScript frontend with shadcn/ui
  3. 12 ADRs covering all major technical decisions
Detail Level: Detailed Deep-Dive (40+ slides)
Speaker Notes: Yes
Diagrams: Both (Mermaid + PlantUML)
Project Name: InventorySystem_TechDeepDive_2026
```

### Example 3: Prototype Demo for Product Team

```
Source: Prototype_InventorySystem/
Audience: Product managers and business analysts
Key Messages:
  1. Prototype covers 100% of P0 requirements
  2. 15 screens, 42 components, full design system
  3. Interactive demo available for user testing
Detail Level: Standard Overview (20-30 slides)
Speaker Notes: Yes
Diagrams: Mermaid
Project Name: InventorySystem_PrototypeDemo_2026
```

---

## Integration with Framework

This command integrates with:
- **Discovery outputs**: ClientAnalysis_* folders
- **Prototype outputs**: Prototype_* folders
- **ProductSpecs outputs**: ProductSpecs_* folders
- **SolArch outputs**: SolArch_* folders

It can also be invoked by:
- **Prototype_Deliverables** skill (as "slidev" format option)
- **Any agent** generating presentations

---

## Dependencies

Requires:
- Node.js and npm
- `@slidev/cli` (installed automatically via npm install)
- Optional: Playwright (for PDF export)

---

## Related Skills

- **slidev** - Core Slidev knowledge base
- **pptx** - Alternative PowerPoint format
- **prototype-deliverables** - Can invoke this command

---

## Notes

- Slidev presentations are web-based and work in all modern browsers
- Can be deployed as static HTML (npm run build)
- Supports live code examples, interactive demos, and animations
- PDF export requires Playwright (`npm install -D @playwright/test`)
- Speaker view available (press 'S' during presentation)
- Drawing mode available (press 'C' during presentation)
