---
name: analyzing-presentations
description: Use when you need to extract strategic messaging and visual concepts from presentation files (PPTX, PPT, KEY, PDF).
model: sonnet
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-presentations started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-presentations ended '{"stage": "discovery"}'
---

# Analyze Presentation

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill analyzing-presentations instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_AnalyzePresentation
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for extracting insights from presentation files (pptx, ppt, key, pdf presentations). Analyzes slide decks for strategic messaging, visual concepts, stakeholder communications, and business narratives relevant to product discovery.

**Role**: You are a Presentation Analysis Specialist. Your expertise is interpreting slide narratives, extracting visual concepts, understanding stakeholder communications, and identifying the strategic story being told through presentations.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:analyzing-presentations:started` - When skill begins
- `skill:analyzing-presentations:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- User provides presentation files (pptx, ppt, key)
- Request mentions "analyze deck", "review slides", "presentation analysis"
- Context involves stakeholder decks, pitch materials, or visual documentation
- PDF files that appear to be exported presentations

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Presentation Files | Yes | One or more presentation files |
| Presentation Context | No | Type: pitch, internal, workshop, etc. |
| Focus Areas | No | Specific topics to prioritize |
| Output Path | Yes | Where to save analysis |

## Presentation Type Detection

### Auto-Classification Rules

| Pattern | Classification |
|---------|---------------|
| "Executive Summary", "Recommendation" | Executive Deck |
| "Workshop", "Exercise", "Activity" | Workshop Materials |
| "Architecture", "System Design" | Technical Presentation |
| "User Research", "Interview Findings" | Research Readout |
| "Roadmap", "Timeline", "Milestones" | Planning Presentation |
| "Pitch", "Investment", "Series" | Pitch Deck |
| "Pain Points", "Solution", "Demo" | Product Demo |

## Extraction Framework

### 1. Structure Analysis
- Count total slides
- Identify sections/dividers
- Extract speaker notes if present
- Note visual-heavy vs text-heavy slides
- Identify key diagrams/charts

### 2. Content Extraction

#### Strategic Messaging
- Title slide messaging (positioning)
- Section headers (narrative arc)
- Call-to-action slides
- Key takeaway slides

#### Visual Concepts
- Architecture diagrams
- Process flows
- User journey maps
- Comparison charts
- Wireframes/mockups

#### Data & Metrics
- Charts and graphs
- Statistics cited
- Before/after comparisons
- ROI projections

#### Pain Points & Solutions
- Problem statement slides
- Current state descriptions
- Solution positioning
- Benefit statements

### 3. Narrative Extraction
- Story arc (problem → solution → outcome)
- Stakeholder concerns addressed
- Objection handling points
- Value propositions

## Output Format

### Primary Output: `[output_path]/01-analysis/presentation-[name]-analysis.md`

```markdown
# Presentation Analysis: [Filename]

**Source File**: [Filename]
**Format**: [PPTX/KEY/PDF]
**Total Slides**: [Count]
**Estimated Duration**: [Based on slide count]

---

## 📋 Presentation Overview

**Type**: [Executive/Workshop/Technical/Research/Pitch/Demo]
**Audience**: [Intended viewers]
**Purpose**: [Inferred goal of presentation]
**Date**: [If visible]
**Author**: [If identifiable]

---

## 🎯 Narrative Arc

### Act 1: Setup (Slides 1-N)
**Theme**: [Problem/Context establishment]
**Key Messages**:
- [Message 1]
- [Message 2]

### Act 2: Conflict/Opportunity (Slides N-M)
**Theme**: [Pain points/Market opportunity]
**Key Messages**:
- [Message 1]
- [Message 2]

### Act 3: Resolution (Slides M-End)
**Theme**: [Solution/Recommendation]
**Key Messages**:
- [Message 1]
- [Message 2]

---

## 📊 Slide-by-Slide Summary

### Slide 1: [Title]
**Type**: [Title/Content/Visual/Data]
**Key Content**: [Summary]
**Visuals**: [Description of diagrams/images]
**Speaker Notes**: [If present]

[Repeat for significant slides...]

---

## 🔴 Pain Points Presented

| Slide # | Pain Point | Evidence/Data | Audience Impact |
|---------|------------|---------------|-----------------|
| [N] | [Pain point] | [Supporting data] | [Who it affects] |

---

## 💡 Solutions/Recommendations

| Slide # | Solution | Benefit | Supporting Data |
|---------|----------|---------|-----------------|
| [N] | [Solution] | [Benefit statement] | [Data if any] |

---

## 📈 Data & Metrics Cited

| Slide # | Metric | Value | Context |
|---------|--------|-------|---------|
| [N] | [Metric name] | [Value] | [What it supports] |

---

## 🖼️ Visual Assets Inventory

| Slide # | Visual Type | Description | Reusability |
|---------|-------------|-------------|-------------|
| [N] | [Diagram/Chart/Mockup] | [Description] | [High/Med/Low] |

---

## 👥 Stakeholders Referenced

| Role/Group | Mentioned In | Context |
|------------|--------------|---------|
| [Role] | Slides [N, M] | [How they're discussed] |

---

## 🔑 Key Quotes/Statements

| Slide # | Quote/Statement | Significance |
|---------|-----------------|--------------|
| [N] | "[Verbatim text]" | [Why it matters] |

---

## 📝 Speaker Notes Summary

[If speaker notes present, summarize key points not visible in slides]

---

## 🏷️ Tags

`#presentation` `#[type]` `#[topic1]` `#[topic2]`

---

**Analysis Date**: [Date]
**Confidence Level**: [High/Medium/Low]
```

## Specific Presentation Patterns

### Workshop Decks
- Extract exercise instructions
- Identify collaboration activities
- Note facilitation guidance
- Capture expected outputs

### Executive Decks
- Focus on decision points
- Extract approval criteria
- Identify risk mitigation
- Note budget/resource asks

### Research Readouts
- Extract methodology
- Identify sample details
- Note confidence levels
- Capture key findings

### Technical Presentations
- Extract architecture diagrams
- Identify integration points
- Note technical constraints
- Capture API/data flows

## 🚨 ERROR HANDLING

> **STRICT RULE**: Follow the global error handling rules in `.claude/rules/error-handling.md`.

| Issue | Action |
|-------|--------|
| Any read error | Log skip, continue |
| Password protected | Log skip (cannot process) |
| Embedded media | Note limitation, extract available text |


## Integration Points

### Feeds Into
- `Discovery_ExtractPainPoints` - Problem statements from slides
- `Discovery_ExtractMetrics` - Cited statistics
- `Discovery_ExtractWorkflows` - Process diagrams

### Receives From
- `Discovery_Orchestrator` - Files and context

---

**Skill Version**: 2.0
**Framework Compatibility**: Discovery Skills Framework v2.0
