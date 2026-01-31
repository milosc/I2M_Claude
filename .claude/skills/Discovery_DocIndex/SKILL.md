---
name: indexing-discovery-docs
description: Use when you need to generate master navigation and documentation index files (INDEX.md, README.md, etc.) for a discovery package.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill indexing-discovery-docs started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill indexing-discovery-docs ended '{"stage": "discovery"}'
---

# Index Discovery Docs

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill indexing-discovery-docs instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_DocIndex
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for creating master navigation and documentation index files. Generates INDEX.md, README.md, GETTING_STARTED.md, and FILES_CREATED.md to help stakeholders navigate the complete documentation package.

**Role**: You are a Documentation Architecture Specialist. Your expertise is creating clear, navigable documentation structures that help different audiences find exactly what they need quickly. You understand that stakeholders have varying time constraints and interests.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:indexing-discovery-docs:started` - When skill begins
- `skill:indexing-discovery-docs:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- All discovery phases (1-9) are complete
- Request mentions "create index", "generate documentation", "navigation docs"
- User wants to finalize documentation package
- Checkpoint 10 in orchestrator flow

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Output Path | Yes | Root folder with all generated content |
| Product Name | Yes | From earlier phases |
| File Inventory | Yes | List of all created files |
| Persona List | No | For reading path recommendations |

## Output Files

This skill creates 4 files in `[output_path]/05-documentation/`:

1. `INDEX.md` - Master overview and entry point
2. `README.md` - Documentation hub with links
3. `GETTING_STARTED.md` - Quick start guide by audience
4. `FILES_CREATED.md` - Complete file inventory

## Output Formats

### INDEX.md Template

```markdown
# [Product Name] Product Documentation - Complete Package

**Analysis Date**: [Date]
**Status**: 🟢 Complete
**Version**: 1.0
**Total Files**: [N]

---

## 📦 What You're Getting

This documentation package contains the complete product discovery analysis including:

- **User Research**: [N] personas, [N] jobs-to-be-done
- **Strategic Direction**: Vision, strategy, roadmap, KPIs
- **Design Specifications**: Screens, navigation, data model, components
- **Supporting Documentation**: Navigation guides, validation report

---

## 🚀 Start Here

| Your Role | Start With | Time Needed |
|-----------|------------|-------------|
| Executive | [DOCUMENTATION_SUMMARY.md](./DOCUMENTATION_SUMMARY.md) | 10 min |
| Product Manager | [product-vision.md](../03-strategy/product-vision.md) | 30 min |
| Designer | [screen-definitions.md](../04-design-specs/screen-definitions.md) | 45 min |
| Developer | [data-fields.md](../04-design-specs/data-fields.md) | 30 min |
| QA | [VALIDATION_REPORT.md](./VALIDATION_REPORT.md) | 15 min |

---

## 📁 Folder Structure

```
[OUTPUT_PATH]/
├── 00-management/
│   └── PROGRESS_TRACKER.md
├── 01-analysis/
│   ├── ANALYSIS_SUMMARY.md
│   └── pain-point-registry.md
├── 02-research/
│   ├── jtbd-jobs-to-be-done.md
│   └── persona-*.md (x[N])
├── 03-strategy/
│   ├── product-vision.md
│   ├── product-strategy.md
│   ├── product-roadmap.md
│   └── kpis-and-goals.md
├── 04-design-specs/
│   ├── screen-definitions.md
│   ├── navigation-structure.md
│   ├── data-fields.md
│   ├── sample-data.json
│   ├── ui-components.md
│   └── interaction-patterns.md
└── 05-documentation/
    ├── INDEX.md (you are here)
    ├── README.md
    ├── DOCUMENTATION_SUMMARY.md
    ├── GETTING_STARTED.md
    ├── FILES_CREATED.md
    └── VALIDATION_REPORT.md
```

---

## 📊 Documentation by Category

### Strategy & Vision ([N] documents)
| Document | Purpose | Key Takeaway |
|----------|---------|--------------|
| [product-vision.md](../03-strategy/product-vision.md) | Why we're building this | [One sentence] |
| [product-strategy.md](../03-strategy/product-strategy.md) | How we'll approach it | [One sentence] |
| [product-roadmap.md](../03-strategy/product-roadmap.md) | What we'll build when | [One sentence] |
| [kpis-and-goals.md](../03-strategy/kpis-and-goals.md) | How we'll measure success | [One sentence] |

### User Research ([N] documents)
| Document | Purpose | Key Takeaway |
|----------|---------|--------------|
| [jtbd-jobs-to-be-done.md](../02-research/jtbd-jobs-to-be-done.md) | What users need to accomplish | [N] jobs identified |
| [persona-*.md](../02-research/) | Who our users are | [N] key personas |

### Design Specifications ([N] documents)
| Document | Purpose | Key Takeaway |
|----------|---------|--------------|
| [screen-definitions.md](../04-design-specs/screen-definitions.md) | What screens to build | [N] screens defined |
| [navigation-structure.md](../04-design-specs/navigation-structure.md) | How users navigate | [N] primary flows |
| [data-fields.md](../04-design-specs/data-fields.md) | What data to store | [N] entities |
| [sample-data.json](../04-design-specs/sample-data.json) | Test data for prototype | [N] records |
| [ui-components.md](../04-design-specs/ui-components.md) | Component specifications | Design system |
| [interaction-patterns.md](../04-design-specs/interaction-patterns.md) | How things behave | UX patterns |

---

## 👥 Stakeholder Quick Links

### For Executives
1. [DOCUMENTATION_SUMMARY.md](./DOCUMENTATION_SUMMARY.md) - 5 min overview
2. [kpis-and-goals.md](../03-strategy/kpis-and-goals.md) - Success metrics
3. [product-roadmap.md](../03-strategy/product-roadmap.md) - Timeline

### For Product Managers
1. [product-vision.md](../03-strategy/product-vision.md) - Vision and goals
2. [jtbd-jobs-to-be-done.md](../02-research/jtbd-jobs-to-be-done.md) - User needs
3. [product-strategy.md](../03-strategy/product-strategy.md) - Strategic approach

### For Designers
1. All [persona-*.md](../02-research/) files - User understanding
2. [screen-definitions.md](../04-design-specs/screen-definitions.md) - Screen layouts
3. [ui-components.md](../04-design-specs/ui-components.md) - Component specs

### For Developers
1. [data-fields.md](../04-design-specs/data-fields.md) - Data model
2. [sample-data.json](../04-design-specs/sample-data.json) - Test data
3. [interaction-patterns.md](../04-design-specs/interaction-patterns.md) - Behaviors

---

## 📈 Key Numbers

| Metric | Value |
|--------|-------|
| **Pain Points Identified** | [N] |
| **User Personas** | [N] |
| **Jobs-to-be-Done** | [N] |
| **Screens Defined** | [N] |
| **Data Entities** | [N] |
| **Total Documentation Pages** | ~[N] |

---

## 🎯 North Star Metric

**[North Star Metric Name]**: [Current] → [Target]

---

**Index Created**: [Date]
**Package Version**: 1.0
**Framework**: Discovery Skills v2.0
```

### README.md Template

```markdown
# [Product Name] Product Documentation

**Version**: 1.0
**Last Updated**: [Date]
**Status**: 🟢 Complete

---

## 📋 What's Inside

This package contains comprehensive product documentation generated from user research and stakeholder interviews. It includes everything needed to understand the product direction and begin implementation.

---

## 🚀 Quick Navigation

### 📑 Strategy & Vision
- [product-vision.md](../03-strategy/product-vision.md) - Product vision and goals
- [product-strategy.md](../03-strategy/product-strategy.md) - Strategic approach and pillars
- [product-roadmap.md](../03-strategy/product-roadmap.md) - Development timeline and phases
- [kpis-and-goals.md](../03-strategy/kpis-and-goals.md) - Success metrics and ROI

### 👥 User Research
- [jtbd-jobs-to-be-done.md](../02-research/jtbd-jobs-to-be-done.md) - Jobs-to-be-done catalog
- [persona-*.md](../02-research/) - User persona profiles

### 🎨 Design Specifications
- [screen-definitions.md](../04-design-specs/screen-definitions.md) - Screen inventory and layouts
- [navigation-structure.md](../04-design-specs/navigation-structure.md) - Navigation and user flows
- [data-fields.md](../04-design-specs/data-fields.md) - Data model specifications
- [sample-data.json](../04-design-specs/sample-data.json) - Test data for prototyping
- [ui-components.md](../04-design-specs/ui-components.md) - UI component library
- [interaction-patterns.md](../04-design-specs/interaction-patterns.md) - Interaction behaviors

### 📚 Documentation
- [INDEX.md](./INDEX.md) - Master overview
- [DOCUMENTATION_SUMMARY.md](./DOCUMENTATION_SUMMARY.md) - Executive summary
- [GETTING_STARTED.md](./GETTING_STARTED.md) - Quick start guide
- [FILES_CREATED.md](./FILES_CREATED.md) - File inventory
- [VALIDATION_REPORT.md](./VALIDATION_REPORT.md) - Quality validation

---

## 🔄 Document Status Legend

| Symbol | Meaning |
|--------|---------|
| 🟢 | Complete - Ready for use |
| 🟡 | In Progress - Under development |
| 🔴 | Planned - Not yet started |
| ⚠️ | Issue - Requires attention |

---

## 📝 How to Use This Documentation

### Step 1: Understand the Users
Start with the persona files to understand who you're building for.

### Step 2: Understand the Vision
Read the vision and strategy to understand the direction.

### Step 3: Review the Requirements
Use JTBD to understand what users need to accomplish.

### Step 4: Plan the Build
Use design specifications to plan implementation.

### Step 5: Validate Progress
Use the roadmap and KPIs to track progress.

---

## 📞 Questions?

For questions about this documentation:
- Check [GETTING_STARTED.md](./GETTING_STARTED.md) for orientation
- Review [VALIDATION_REPORT.md](./VALIDATION_REPORT.md) for known gaps
- Consult [INDEX.md](./INDEX.md) for navigation

---

**Maintained By**: Product Team
**Generated By**: Discovery Skills Framework v2.0
**Next Review**: [Date + 1 month]
```

### GETTING_STARTED.md Template

```markdown
# Getting Started with [Product Name] Documentation

Welcome! This guide helps you navigate the product documentation efficiently.

---

## 📖 What This Is

This documentation package contains:
- **Analysis**: Raw insights from user research
- **Research**: Personas and jobs-to-be-done
- **Strategy**: Vision, strategy, roadmap, and metrics
- **Design**: Screen layouts, data model, and UI specifications
- **Documentation**: Navigation aids and validation

---

## 🚀 Quick Start by Role

### 👔 Executives (15 minutes)
**Goal**: Understand strategic direction and expected outcomes

1. **Start here**: [DOCUMENTATION_SUMMARY.md](./DOCUMENTATION_SUMMARY.md)
   - Executive overview of entire package
   
2. **Key metrics**: [kpis-and-goals.md](../03-strategy/kpis-and-goals.md)
   - North star metric and ROI calculation
   
3. **Timeline**: [product-roadmap.md](../03-strategy/product-roadmap.md)
   - Phases and milestones

### 📊 Product Managers (1 hour)
**Goal**: Deep understanding of users and product direction

1. **Vision**: [product-vision.md](../03-strategy/product-vision.md)
   - Problem space and solution approach
   
2. **Users**: All persona files in [02-research/](../02-research/)
   - Who we're building for
   
3. **Needs**: [jtbd-jobs-to-be-done.md](../02-research/jtbd-jobs-to-be-done.md)
   - What users need to accomplish
   
4. **Strategy**: [product-strategy.md](../03-strategy/product-strategy.md)
   - How we'll approach the solution

### 🎨 Designers (1 hour)
**Goal**: Understand users and design requirements

1. **Users first**: All [persona-*.md](../02-research/) files
   - Deep user understanding
   
2. **Layouts**: [screen-definitions.md](../04-design-specs/screen-definitions.md)
   - Screen inventory and specifications
   
3. **Flows**: [navigation-structure.md](../04-design-specs/navigation-structure.md)
   - Navigation and user journeys
   
4. **Components**: [ui-components.md](../04-design-specs/ui-components.md)
   - Design system basics

### ⚙️ Developers (45 minutes)
**Goal**: Understand data and technical requirements

1. **Context**: [product-vision.md](../03-strategy/product-vision.md)
   - Why we're building this
   
2. **Data model**: [data-fields.md](../04-design-specs/data-fields.md)
   - Entity and field definitions
   
3. **Test data**: [sample-data.json](../04-design-specs/sample-data.json)
   - Ready-to-use mock data
   
4. **Behaviors**: [interaction-patterns.md](../04-design-specs/interaction-patterns.md)
   - How things should work

### 🧪 QA Engineers (30 minutes)
**Goal**: Understand test scope and acceptance criteria

1. **Features**: [product-roadmap.md](../03-strategy/product-roadmap.md)
   - What's being built
   
2. **Flows**: [navigation-structure.md](../04-design-specs/navigation-structure.md)
   - Critical paths to test
   
3. **Validation**: [VALIDATION_REPORT.md](./VALIDATION_REPORT.md)
   - Known gaps and coverage

---

## 📚 Document Overview

| Document | Purpose | Read Time |
|----------|---------|-----------|
| DOCUMENTATION_SUMMARY.md | Executive overview | 5 min |
| product-vision.md | The "why" | 10 min |
| product-strategy.md | The "how" | 15 min |
| product-roadmap.md | The "when" | 15 min |
| kpis-and-goals.md | Success metrics | 10 min |
| persona-*.md | User profiles | 10 min each |
| jtbd-jobs-to-be-done.md | User needs | 20 min |
| screen-definitions.md | UI layouts | 20 min |
| data-fields.md | Data model | 15 min |

---

## 🎯 Key Takeaways

### The Problem
[1-2 sentence summary of the core problem being solved]

### The Solution
[1-2 sentence summary of the approach]

### The Impact
[Key metrics: Current → Target]

---

## ❓ FAQ

**Q: Where do I find the prototype data?**
A: Check [sample-data.json](../04-design-specs/sample-data.json)

**Q: What are the navigation rules?**
A: See [navigation-structure.md](../04-design-specs/navigation-structure.md)

**Q: Who are the target users?**
A: See persona files in [02-research/](../02-research/)

**Q: What's the timeline?**
A: See [product-roadmap.md](../03-strategy/product-roadmap.md)

**Q: What's the validation status?**
A: See [VALIDATION_REPORT.md](./VALIDATION_REPORT.md)

---

**Last Updated**: [Date]
**Framework**: Discovery Skills v2.0
```

### FILES_CREATED.md Template

```markdown
# Files Created - [Product Name] Documentation

## ✅ Complete File Inventory ([N] total files)

### 00-management/ (1 file)

| # | File | Purpose | Status |
|---|------|---------|--------|
| 1 | PROGRESS_TRACKER.md | Analysis progress tracking | 🟢 Complete |

### 01-analysis/ (2 files)

| # | File | Purpose | Status |
|---|------|---------|--------|
| 2 | ANALYSIS_SUMMARY.md | Consolidated material analysis | 🟢 Complete |
| 3 | pain-point-registry.md | Categorized pain points | 🟢 Complete |

### 02-research/ ([N] files)

| # | File | Purpose | Status |
|---|------|---------|--------|
| 4 | jtbd-jobs-to-be-done.md | Jobs-to-be-done catalog | 🟢 Complete |
| 5 | persona-[role-1].md | User persona | 🟢 Complete |
| 6 | persona-[role-2].md | User persona | 🟢 Complete |
| 7 | persona-[role-3].md | User persona | 🟢 Complete |
[Add more as needed]

### 03-strategy/ (4 files)

| # | File | Purpose | Status |
|---|------|---------|--------|
| [N] | product-vision.md | Vision and goals | 🟢 Complete |
| [N] | product-strategy.md | Strategic approach | 🟢 Complete |
| [N] | product-roadmap.md | Development timeline | 🟢 Complete |
| [N] | kpis-and-goals.md | Success metrics | 🟢 Complete |

### 04-design-specs/ (6 files)

| # | File | Purpose | Status |
|---|------|---------|--------|
| [N] | screen-definitions.md | Screen inventory and layouts | 🟢 Complete |
| [N] | navigation-structure.md | Navigation and flows | 🟢 Complete |
| [N] | data-fields.md | Data model specification | 🟢 Complete |
| [N] | sample-data.json | Test data for prototype | 🟢 Complete |
| [N] | ui-components.md | Component library | 🟢 Complete |
| [N] | interaction-patterns.md | Behavior patterns | 🟢 Complete |

### 05-documentation/ (6 files)

| # | File | Purpose | Status |
|---|------|---------|--------|
| [N] | INDEX.md | Master navigation | 🟢 Complete |
| [N] | README.md | Documentation hub | 🟢 Complete |
| [N] | DOCUMENTATION_SUMMARY.md | Executive summary | 🟢 Complete |
| [N] | GETTING_STARTED.md | Quick start guide | 🟢 Complete |
| [N] | FILES_CREATED.md | This file | 🟢 Complete |
| [N] | VALIDATION_REPORT.md | Quality validation | 🟢 Complete |

---

## 📊 Statistics

| Category | Files | ~Pages | ~Words |
|----------|-------|--------|--------|
| Management | 1 | 3 | 500 |
| Analysis | 2 | 15 | 3,000 |
| Research | [N] | [N×10] | [N×2000] |
| Strategy | 4 | 30 | 6,000 |
| Design Specs | 6 | 40 | 8,000 |
| Documentation | 6 | 20 | 4,000 |
| **Total** | **[N]** | **~[N]** | **~[N]** |

---

## 📦 Deliverable Summary

### Created
- ✅ [N] user personas
- ✅ [N] jobs-to-be-done
- ✅ [N] pain points categorized
- ✅ [N] strategic pillars
- ✅ [N] roadmap phases
- ✅ [N] epics
- ✅ [N] screens defined
- ✅ [N] data entities
- ✅ [N] sample records
- ✅ Complete navigation documentation

### Coverage
| Area | Status | Files |
|------|--------|-------|
| Strategy & Vision | 🟢 Complete | 4/4 |
| User Research | 🟢 Complete | [N]/[N] |
| Design Specs | 🟢 Complete | 6/6 |
| Documentation | 🟢 Complete | 6/6 |
| **Overall** | 🟢 **Complete** | **[N]/[N]** |

---

## 📝 Generation Notes

**Source Materials**: [N] files analyzed
**Analysis Duration**: ~[N] hours
**Generated By**: Discovery Skills Framework v2.0
**Generation Date**: [Date]

---

**Inventory Status**: 🟢 Complete
**Last Updated**: [Date]
```

## Quality Checklist

Before finalizing:
- [ ] All links are relative and correct
- [ ] File counts match actual files
- [ ] Persona names match actual files
- [ ] Folder structure matches actual
- [ ] Reading times are realistic
- [ ] Key numbers are accurate

## Error Handling

| Issue | Action |
|-------|--------|
| Missing files in inventory | Note gap, create placeholder entry |
| Broken links | Fix path, verify file exists |
| Inconsistent naming | Use actual file names |
| Count mismatch | Recount, update statistics |

## Integration Points

### Receives From
- All previous phases - Files to index
- `Discovery_Orchestrator` - Product name, counts

### Feeds Into
- `Discovery_Validate` - File list for validation

## State Management Reminder

⚠️ **This skill produces output files only.** The calling orchestrator/command is responsible for updating state after all Phase 10 skills complete.

**After running ALL Phase 10 skills (DocIndex + DocSummary), update state:**
```bash
python3 .claude/skills/tools/update_discovery_state.py --phase 10_docs --status complete
```

**Or manually update `_state/discovery_progress.json`:**
```json
"10_docs": { "status": "complete", "started": "<ISO>", "completed": "<ISO>" },
"overall_progress": 90,
"resumable_from": "11_validate"
```

---

**Skill Version**: 3.0
**Framework Compatibility**: Discovery Skills Framework v2.0
