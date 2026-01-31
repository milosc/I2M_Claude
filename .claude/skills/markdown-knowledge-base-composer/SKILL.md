---
name: markdown-knowledge-base-composer
description: Aggregate Markdown folders into a cohesive knowledge base with TOC, cross-links, and export.
model: sonnet
allowed-tools: Read, Write, Edit, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill markdown-knowledge-base-composer started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill markdown-knowledge-base-composer ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill markdown-knowledge-base-composer instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Markdown Knowledge Base Composer Skill

## What This Skill Enables

Claude can organize, process, and transform Markdown documentation into cohesive knowledge bases. Generate table of contents, fix broken links, convert formats, create static sites, and export to PDF or HTML.

## Prerequisites

**Required:**
- Claude Pro subscription
- Code Interpreter feature enabled
- Markdown files uploaded (can be multiple files/folders)

**What Claude handles:**
- Installing Markdown processing tools (remark, unified, pandoc)
- Parsing and transforming Markdown
- Link validation and fixing
- TOC generation
- Format conversion (MD → HTML, PDF, DOCX)
- Static site generation

## How to Use This Skill

### Generate Table of Contents

**Prompt:** "Generate a table of contents from all these Markdown files. Include links to each section."

Claude will:
1. Parse all Markdown files
2. Extract headings
3. Create hierarchical TOC
4. Add anchor links
5. Save as README.md or TOC.md

### Fix Broken Links

**Prompt:** "Check all internal links in these Markdown files and fix any broken ones. Report what was fixed."

Claude will:
1. Parse all Markdown files
2. Extract all links
3. Validate targets exist
4. Fix broken links
5. Report changes made

### Convert Format

**Prompt:** "Convert all these Markdown docs to a single PDF with:
- Table of contents
- Page numbers
- Consistent heading styles
- Code syntax highlighting"

Claude will:
1. Merge Markdown files
2. Generate TOC
3. Apply styling
4. Convert to PDF
5. Export final document

### Create Static Site

**Prompt:** "Generate a static HTML site from these docs:
- Homepage with navigation
- Responsive design
- Search functionality
- Dark mode toggle"

Claude will:
1. Process Markdown to HTML
2. Generate navigation
3. Apply responsive CSS
4. Add JavaScript features
5. Create static site files

## Common Workflows

### Documentation Site Generation
```
"Create documentation site:
1. Parse all .md files in docs/
2. Generate sidebar navigation
3. Create search index
4. Add syntax highlighting for code blocks
5. Export as static HTML site
Use clean, professional styling."
```

### Knowledge Base Consolidation
```
"Consolidate scattered notes:
1. Combine all Markdown files into sections
2. Generate master TOC
3. Normalize heading levels (start all at H1)
4. Fix relative links between files
5. Create single comprehensive document
Export as both Markdown and PDF."
```

### README Generation
```
"Generate professional README.md:
1. Extract project info from package.json
2. Add badges (build status, version, license)
3. Create sections: About, Installation, Usage, Contributing
4. Add table of contents with anchor links
5. Include code examples from docs/"
```

### Multi-Format Export
```
"Export documentation in multiple formats:
1. HTML (with navigation and search)
2. PDF (with TOC and page numbers)
3. EPUB (for e-readers)
4. DOCX (for Word)
Maintain consistent styling across all formats."
```

## Features & Capabilities

### Markdown Processing
- Parse frontmatter (YAML, TOML)
- Extract and process links
- Handle images and media
- Process code blocks
- Parse tables
- Support GFM (GitHub Flavored Markdown)

### Link Management
- Validate internal links
- Fix broken references
- Convert relative to absolute
- Update moved files
- Generate anchor links

### Content Organization
- Auto-generate TOC at any level
- Sort files by frontmatter or name
- Create hierarchical structure
- Merge multiple files
- Split large files

### Format Conversion
- Markdown → HTML
- Markdown → PDF
- Markdown → DOCX
- Markdown → EPUB
- HTML → Markdown

## Tips for Best Results

1. **File Organization**: Upload files with clear directory structure
2. **Frontmatter**: Use YAML frontmatter for metadata (title, date, tags)
3. **Link Style**: Be consistent with link styles (relative vs absolute)
4. **Heading Hierarchy**: Start with H1, don't skip levels
5. **File Naming**: Use kebab-case or snake_case consistently
6. **Image Paths**: Keep images in dedicated folder (./images/ or ./assets/)
7. **Code Blocks**: Always specify language for syntax highlighting

## Advanced Operations

### Custom Transformations
- Replace text patterns across all files
- Add custom frontmatter
- Insert headers/footers
- Inject custom CSS/JS
- Apply templates

### Multi-Language Support
- Organize by language (en/, es/, etc.)
- Generate language switcher
- Maintain translation links

### Version Control
- Track changes between versions
- Generate changelogs
- Compare documentation versions

## Troubleshooting

**Issue:** Broken links after reorganizing files
**Solution:** "Scan all links and update paths based on new file structure"

**Issue:** TOC not rendering correctly
**Solution:** Ensure consistent heading hierarchy (H1 → H2 → H3, no skipping)

**Issue:** Images not showing in PDF export
**Solution:** "Use absolute paths for images" or "Embed images inline as base64"

**Issue:** Code blocks losing formatting
**Solution:** "Preserve code block syntax highlighting in export" and specify language

**Issue:** Special characters breaking exports
**Solution:** "Escape special characters" or "Use UTF-8 encoding throughout"

**Issue:** Large files causing memory issues
**Solution:** "Process files in batches" or "Split into smaller sections first"

## Learn More

- [Markdown Guide](https://www.markdownguide.org/) - Comprehensive Markdown reference
- [Remark](https://github.com/remarkjs/remark) - Markdown processor
- [Pandoc](https://pandoc.org/) - Universal document converter
- [MkDocs](https://www.mkdocs.org/) - Documentation site generator
- [VitePress](https://vitepress.dev/) - Modern documentation framework


## Key Features

- Heading normalization and slug consistency
- TOC generation across directories
- Cross-link rewriting and validation
- Export to static HTML/PDF

## Use Cases

- Assemble a product handbook
- Publish internal notes
- Create a client-facing knowledge pack

## Examples

### Example 1: Build TOC and rewrite links (Node)

```javascript
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkStringify from 'remark-stringify';

const dir = './notes';
const files = readdirSync(dir).filter(f => f.endsWith('.md'));

for (const file of files) {
  const input = readFileSync(join(dir, file), 'utf8');
  const tree = unified().use(remarkParse).parse(input);
  // ... transform headings and links ...
  const out = unified().use(remarkStringify).stringify(tree);
  // writeFileSync(join('dist', file), out)
}
```

## Troubleshooting

### Broken links after re-organization

Regenerate slugs and run a link validator; ensure relative paths are correct.

### Remark/unified plugins throwing 'Cannot read property' errors

Ensure plugin order is correct: parse → transform plugins → stringify. Check unified() pipeline sequence and plugin compatibility.

### Frontmatter YAML parsing fails with special characters in values

Quote YAML values containing colons, brackets, or special chars. Use remark-frontmatter with yaml-safe mode enabled.

### PDF export cuts off code blocks or loses syntax highlighting

Use Playwright with explicit page breaks. Install prism.js or highlight.js for code styling, set print CSS media queries.

### TOC anchor links not working after Markdown-to-HTML conversion

Use remark-slug to generate consistent heading IDs, then remark-toc with 'tight' option. Ensure heading hierarchy is valid.

## Learn More

For additional documentation and resources, visit:

https://github.com/remarkjs/remark
