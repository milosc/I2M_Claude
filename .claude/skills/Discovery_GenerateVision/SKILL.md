---
name: generating-product-vision
description: Use when you need to synthesize discovery findings into a compelling product vision (PRODUCT_VISION.md) that articulates the problem space and success criteria.
model: sonnet
allowed-tools: AskUserQuestion, Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-product-vision started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-product-vision ended '{"stage": "discovery"}'
---

# Generate Product Vision

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-product-vision instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_GenerateVision
- **Version**: 3.0.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-21
- **Change History**:
  - v3.0.0 (2025-12-21): Major update: UPPERCASE file naming (PRODUCT_VISION.md), Vision Pillars structure
  - v2.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Synthesizes discovery findings into a compelling product vision document. Creates the foundational "why" statement that guides all subsequent product decisions, articulating the problem space, solution approach, and success criteria.

**Role**: You are a product visionary who excels at distilling complex research findings into clear, inspiring direction that aligns stakeholders and guides development teams.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:generating-product-vision:started` - When skill begins
- `skill:generating-product-vision:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- User requests "create product vision", "generate vision document"
- Discovery Orchestrator invokes after JTBD extraction (Checkpoint 5)
- User wants to articulate the product's purpose and direction
- Request involves synthesizing research into strategic direction

## System Role Statement

```
You are a Product Visionary with expertise in translating user research 
into compelling product direction.

Your responsibilities:
1. Synthesize pain points into a clear problem statement
2. Articulate the solution approach at a high level
3. Define measurable success criteria
4. Create alignment across stakeholders
5. Set the foundation for strategic planning

You understand that:
- Vision should be inspirational yet actionable
- Vision is stable (3-5 year horizon)
- Vision must connect to real user pain
- Vision should be memorable (1-2 sentences core statement)
```

## Input Requirements

| Input | Required | Source |
|-------|----------|--------|
| ANALYSIS_SUMMARY.md | Yes | 01-analysis/ |
| persona-*.md files | Yes | 02-research/ |
| jtbd-jobs-to-be-done.md | Yes | 02-research/ |

## CRITICAL OUTPUT REQUIREMENTS

### File Name (MANDATORY)

```
[output_path]/03-strategy/PRODUCT_VISION.md
```

**File naming**: UPPERCASE with underscores - `PRODUCT_VISION.md`

## Output Specification

### Primary Output: `03-strategy/PRODUCT_VISION.md`

```markdown
---
document_id: VISION-[PROJECT]
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_GenerateVision
source_files:
  - 01-analysis/ANALYSIS_SUMMARY.md
  - 02-research/persona-*.md
  - 02-research/jtbd-jobs-to-be-done.md
change_history:
  - version: "1.0.0"
    date: "[YYYY-MM-DD]"
    author: "Discovery_GenerateVision"
    changes: "Initial vision document generation from discovery research"
---

# Product Vision: [Product Name]

**Vision Date**: [Date]
**Horizon**: [3-5 years]
**Status**: 🟢 Approved | 🟡 Draft | 🔴 Under Review

---

## 🎯 Vision Statement

> [One compelling sentence: For [target users] who [key need], 
> [Product Name] is a [category] that [key benefit]. 
> Unlike [alternatives], our product [key differentiator].]

---

## 🌟 The Problem We're Solving

### Problem Space Summary

[2-3 paragraph narrative describing the current state, why it's painful, 
and the consequences of not solving it]

### Top Pain Points Addressed

| # | Pain Point | Impact | Current Cost |
|---|------------|--------|--------------|
| 1 | [Pain Point Title] | [Description of impact] | [Quantified if possible] |
| 2 | [Pain Point Title] | [Description of impact] | [Quantified if possible] |
| 3 | [Pain Point Title] | [Description of impact] | [Quantified if possible] |
| 4 | [Pain Point Title] | [Description of impact] | [Quantified if possible] |
| 5 | [Pain Point Title] | [Description of impact] | [Quantified if possible] |

### User Voices

> "[Direct quote illustrating the problem]" - [Persona/Source]

> "[Direct quote illustrating the problem]" - [Persona/Source]

> "[Direct quote illustrating the problem]" - [Persona/Source]

### Current State Consequences

1. **[Consequence Area]**: [Impact description with metrics if available]
2. **[Consequence Area]**: [Impact description]
3. **[Consequence Area]**: [Impact description]

---

## 💡 Our Solution

### Solution Overview

[Product Name] will be [high-level description] that transforms how 
[target users] [key activity].

### Key Capabilities

#### 1. [Capability Name]
**What**: [Description of the capability]
**Why**: [Pain points it addresses]
**Impact**: [Expected benefit]

#### 2. [Capability Name]
[Same structure...]

#### 3. [Capability Name]
[Same structure...]

#### 4. [Capability Name]
[Same structure...]

#### 5. [Capability Name]
[Same structure...]

### Capability to Pain Point Mapping

| Capability | Pain Points Addressed |
|------------|----------------------|
| [Capability 1] | P1, P3, P5 |
| [Capability 2] | P2, P4 |
| [Capability 3] | P1, P2, P3 |

---

## 🚀 Success Criteria

We'll know we've succeeded when:

### Quantitative Metrics

| Metric | Current State | Target | Timeline |
|--------|---------------|--------|----------|
| [Metric 1] | [Baseline] | [Goal] | [When] |
| [Metric 2] | [Baseline] | [Goal] | [When] |
| [Metric 3] | [Baseline] | [Goal] | [When] |

### Qualitative Indicators

1. **[Indicator]**: [Description of success state]
2. **[Indicator]**: [Description of success state]
3. **[Indicator]**: [Description of success state]

### User Success Statements

- "[Persona 1] can [achievement] in [timeframe/ease]"
- "[Persona 2] no longer [pain point]"
- "[Persona 3] reports [satisfaction measure]"

---

## 🎭 Target Users

### Primary Users

| Persona | Count | Key Need | Success Metric |
|---------|-------|----------|----------------|
| [Persona 1] | [N] | [Primary need] | [How we measure their success] |
| [Persona 2] | [N] | [Primary need] | [How we measure their success] |

### Secondary Users

| Persona | Count | Key Need | Relationship to Primary |
|---------|-------|----------|------------------------|
| [Persona 3] | [N] | [Need] | [How they interact] |

### User Ecosystem

```
[Primary User 1] ←→ [Product] ←→ [Primary User 2]
        ↑                               ↑
        |                               |
   [Secondary User]              [External Party]
```

---

## 📊 Strategic Alignment

### Organizational Goals

| Business Goal | How Vision Supports |
|---------------|---------------------|
| [Goal 1] | [Connection to vision] |
| [Goal 2] | [Connection to vision] |

### Market Context

**Market Opportunity**: [Description]
**Competitive Landscape**: [Overview]
**Timing Rationale**: [Why now]

---

## 🔮 Future State

### 6-Month View
[What success looks like in 6 months]

### 1-Year View
[What success looks like in 1 year]

### 3-Year View
[What success looks like in 3 years]

---

## ⚠️ What This Is NOT

To maintain focus, this product will NOT:
- [Anti-goal 1]
- [Anti-goal 2]
- [Anti-goal 3]

---

**Document Status**: 🟢 Complete
**Created**: [Date]
**Last Updated**: [Timestamp]
**Owner**: [Product Team]
```

## Vision Creation Process

### Step 0: Target Audience Prioritization

When multiple personas have conflicting priorities, clarify focus:

```markdown
IF multiple_personas_with_conflicting_priorities:
  USE AskUserQuestion:
    question: "Which user segment should the product vision prioritize?"
    header: "Target User"
    options:
      - label: "{Persona1.name} (Most pain points)"
        description: "{pain_count} pain points, {frequency} usage"
      - label: "{Persona2.name} (Highest value)"
        description: "{value_metric}, {frequency} usage"
      - label: "{Persona3.name} (Strategic importance)"
        description: "{strategic_reason}"
      - label: "Balance all segments"
        description: "No single prioritization, address all equally"

STORE target_user_selection in:
  - State file: _state/discovery_config.json
  - Key: vision_target_user
  - Value: { choice: "[selected]", timestamp: "[ISO]", source: "user" }
```

### Step 1: Problem Synthesis
```markdown
1. Review all P0 and P1 pain points from ANALYSIS_SUMMARY
2. Identify the top 5 highest-impact problems
3. Quantify impact where possible
4. Extract compelling quotes
```

### Step 2: Solution Articulation
```markdown
1. Review JTBD for desired outcomes
2. Group related outcomes into capabilities (5-7 typical)
3. Map capabilities back to pain points
4. Ensure complete coverage of critical needs
```

### Step 3: Success Definition
```markdown
1. Extract metrics mentioned in research
2. Define measurable targets
3. Create user success statements per persona
4. Set timeline expectations
```

### Step 4: Vision Statement Crafting
```markdown
Use the format:
"For [target users] who [key need], 
[Product Name] is a [category] that [key benefit]. 
Unlike [alternatives], our product [key differentiator]."

Refine to be:
- Memorable (can repeat from memory)
- Inspiring (motivates the team)
- Specific (not generic platitudes)
- Measurable (implies success criteria)
```

## Quality Criteria

### Vision Statement Quality
- [ ] One or two sentences maximum
- [ ] Specifies target user
- [ ] Articulates key benefit
- [ ] Differentiates from alternatives
- [ ] Memorable and quotable

### Problem Coverage
- [ ] Top 5-7 pain points included
- [ ] Impact quantified where possible
- [ ] User quotes support each pain point
- [ ] All personas represented

### Solution Clarity
- [ ] 5-7 key capabilities defined
- [ ] Each capability maps to pain points
- [ ] No implementation details
- [ ] Outcome-focused language

### Success Criteria
- [ ] Quantitative metrics defined
- [ ] Baselines established (or noted as TBD)
- [ ] Targets are ambitious but achievable
- [ ] Per-persona success statements

## Integration Points

### Receives From
- Discovery_ExtractPainPoints: Problem evidence
- Discovery_GeneratePersona: User context
- Discovery_GenerateJTBD: Desired outcomes

### Provides To
- Discovery_GenerateStrategy: Foundation for strategic pillars
- Discovery_GenerateRoadmap: Success criteria for phase planning
- Discovery_GenerateKPIs: North star and supporting metrics

---

**Skill Version**: 2.0
**Framework**: Discovery Skills Framework v2.0
**Output Location**: 03-strategy/product-vision.md
