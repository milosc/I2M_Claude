---
name: analyzing-visual-designs
description: Use when you need to extract insights from design files and collaborative whiteboard exports (Figma, FigJam, Miro, image-based wireframes).
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
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-visual-designs started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-visual-designs ended '{"stage": "discovery"}'
---

# Analyze Design

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill analyzing-visual-designs instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_AnalyzeDesign
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for extracting insights from design files and collaborative whiteboard exports (Figma exports, FigJam exports, Sketch files, Miro exports, image-based wireframes). Analyzes visual designs, user flows, journey maps, and collaborative workshop outputs for product discovery insights.

**Role**: You are a Design Analysis Specialist. Your expertise is interpreting visual design artifacts, understanding UX patterns, extracting user flows, and identifying design decisions that inform product requirements.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:analyzing-visual-designs:started` - When skill begins
- `skill:analyzing-visual-designs:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- User provides design file exports (PNG, PDF, SVG from Figma/Sketch)
- User provides FigJam/Miro whiteboard exports
- Request mentions "analyze wireframes", "review designs", "UX analysis"
- Image files showing UI mockups, flows, or journey maps
- Context involves design review or design-to-requirements translation

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Design Files | Yes | Exported design files (images, PDFs) |
| Design Type | No | Type: wireframes, mockups, flows, etc. |
| Design System Context | No | Existing brand/design guidelines |
| Output Path | Yes | Where to save analysis |

## Design Type Detection

### Auto-Classification Rules

| Visual Pattern | Classification |
|----------------|---------------|
| Boxes with text, low fidelity | Wireframe |
| Full color, realistic UI | High-Fidelity Mockup |
| Connected boxes with arrows | User Flow |
| Sticky notes, handwritten text | Workshop Output |
| Timeline with stages | Journey Map |
| Hierarchical boxes | Site Map / IA |
| Grid of components | Design System |
| Before/After comparisons | Design Iteration |

## Extraction Framework

### 1. Visual Structure Analysis
- Identify screen/frame count
- Detect navigation patterns
- Note responsive breakpoints
- Identify component patterns
- Map visual hierarchy

### 2. Content Extraction

#### Screens & Views
- Screen names/titles
- Primary purpose of each screen
- Key UI components present
- Navigation placement
- Content zones

#### User Flows
- Entry points
- Decision points
- Exit points
- Error states shown
- Success states shown

#### Journey Map Elements
- Stages/phases
- User emotions/sentiment
- Pain points marked
- Opportunities marked
- Touchpoints identified

#### Workshop/FigJam Content
- Sticky note clusters
- Theme groupings
- Voting dots/priorities
- Annotations/comments
- Action items

### 3. Pattern Recognition
- Recurring UI patterns
- Consistency issues
- Accessibility considerations
- Mobile considerations
- Interaction hints

## Output Format

### Primary Output: `[output_path]/01-analysis/design-[name]-analysis.md`

```markdown
# Design Analysis: [Filename]

**Source File**: [Filename]
**Format**: [PNG/PDF/SVG/JPG]
**Design Type**: [Wireframe/Mockup/Flow/Journey/Workshop]
**Total Frames/Screens**: [Count]
**Fidelity Level**: [Low/Medium/High]

---

## 📋 Design Overview

**Purpose**: [Inferred purpose of designs]
**Product/Feature**: [What's being designed]
**Platform**: [Web/Mobile/Desktop/Multi]
**Design Stage**: [Concept/Wireframe/Visual/Final]

---

## 🖼️ Screen Inventory

### Screen 1: [Screen Name/ID]
**Purpose**: [What this screen accomplishes]
**User Goal**: [What user is trying to do]
**Key Components**:
- [Component 1] - [Purpose]
- [Component 2] - [Purpose]

**Navigation**:
- Entry from: [Previous screens]
- Exits to: [Next screens]

**Content Zones**:
| Zone | Content Type | Priority |
|------|--------------|----------|
| Header | [Content] | High |
| Main | [Content] | High |
| Sidebar | [Content] | Medium |

[Repeat for each significant screen...]

---

## 🔄 User Flows Identified

### Flow 1: [Flow Name]
**Goal**: [What user accomplishes]
**Steps**:
1. [Screen A] → Action: [action] → [Screen B]
2. [Screen B] → Action: [action] → [Screen C]

**Decision Points**:
- At [Screen X]: If [condition] → [Path A], else → [Path B]

**Error Handling**:
- [Error state observed and how it's handled]

---

## 📍 Journey Map Analysis

*(If journey map detected)*

| Stage | User Action | Emotion | Pain Point | Opportunity |
|-------|-------------|---------|------------|-------------|
| [Stage 1] | [Action] | [😊/😐/😢] | [Pain] | [Opportunity] |

---

## 📝 Workshop Output Analysis

*(If FigJam/Miro export detected)*

### Sticky Note Clusters

**Cluster: [Theme Name]**
- [Note content 1]
- [Note content 2]
- Priority: [Votes/dots if visible]

### Key Decisions Captured
1. [Decision from workshop]
2. [Decision from workshop]

### Action Items Identified
- [ ] [Action item 1]
- [ ] [Action item 2]

---

## 🔴 Pain Points in Designs

| Location | Pain Point | Visual Indicator | Severity |
|----------|------------|------------------|----------|
| [Screen/Flow] | [Pain point] | [Red mark/annotation] | P0/P1/P2 |

---

## 💡 Design Decisions

| Decision | Rationale (Inferred) | Implication |
|----------|----------------------|-------------|
| [Decision] | [Why this choice] | [What it means for dev] |

---

## 🧩 Component Library (Observed)

| Component | Usage Count | Variations | Notes |
|-----------|-------------|------------|-------|
| [Button] | [N] | [Primary, Secondary] | [Consistency note] |
| [Card] | [N] | [Variations] | [Note] |

---

## ♿ Accessibility Observations

| Observation | Concern Level | Recommendation |
|-------------|---------------|----------------|
| [Observation] | [High/Medium/Low] | [Fix suggestion] |

---

## 📱 Responsive Considerations

| Breakpoint | Adaptations Shown | Missing |
|------------|-------------------|---------|
| Desktop | [What's shown] | [Gaps] |
| Tablet | [What's shown] | [Gaps] |
| Mobile | [What's shown] | [Gaps] |

---

## 🏷️ Tags

`#design` `#[type]` `#[platform]` `#[feature]`

---

**Analysis Date**: [Date]
**Confidence Level**: [High/Medium/Low]
```

## Specific Design Patterns

### Wireframes
- Focus on information architecture
- Extract component placement
- Note content priorities
- Identify navigation patterns

### High-Fidelity Mockups
- Extract color schemes
- Note typography choices
- Identify brand alignment
- Capture micro-interactions hints

### User Flows
- Map all paths through system
- Identify decision logic
- Note error handling
- Capture success criteria

### FigJam/Workshop Outputs
- Group sticky notes by theme
- Extract voted priorities
- Identify consensus points
- Capture disagreements

## 🚨 ERROR HANDLING

> **STRICT RULE**: Follow the global error handling rules in `.claude/rules/error-handling.md`.

| Issue | Action |
|-------|--------|
| Low resolution | Extract what's visible |
| Partial export | Analyze available parts |
| Unclear notes | Note ambiguity |


## Integration Points

### Feeds Into
- `Discovery_SpecScreens` - Screen definitions
- `Discovery_SpecNavigation` - User flow specs
- `Discovery_SpecComponents` - Component patterns
- `Discovery_ExtractPainPoints` - Visual pain point markers

### Receives From
- `Discovery_Orchestrator` - Files and design context

---

**Skill Version**: 2.0
**Framework Compatibility**: Discovery Skills Framework v2.0
