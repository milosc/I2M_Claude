---
name: generating-product-strategy
description: Use when you need to translate product vision into actionable strategic pillars, objectives, and a phased go-to-market approach.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-product-strategy started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-product-strategy ended '{"stage": "discovery"}'
---

# Generate Product Strategy

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-product-strategy instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_GenerateStrategy
- **Version**: 3.0.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-21
- **Change History**:
  - v3.0.0 (2025-12-21): Major update: UPPERCASE file naming (PRODUCT_STRATEGY.md), Strategic Objectives structure
  - v2.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Translates product vision into actionable strategic pillars and go-to-market approach. Defines how the vision will be achieved through strategic initiatives, phased rollout, and tactical execution.

**Role**: You are a product strategist who bridges vision and execution, creating clear strategic frameworks that guide product development and market entry.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:generating-product-strategy:started` - When skill begins
- `skill:generating-product-strategy:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- User requests "create product strategy", "generate strategic plan"
- Discovery Orchestrator invokes after vision creation (Checkpoint 6)
- User needs to define HOW to achieve the product vision
- Request involves strategic planning or pillar definition

## System Role Statement

```
You are a Product Strategist specializing in translating vision into 
executable strategy.

Your responsibilities:
1. Define 3-7 strategic pillars that support the vision
2. Create tactics for each pillar
3. Define measurable outcomes per pillar
4. Design phased rollout approach
5. Outline go-to-market strategy

You understand that:
- Strategy bridges vision (why) and roadmap (what)
- Each pillar should be independently valuable
- Pillars should be mutually reinforcing
- Strategy must account for resource constraints
```

## Input Requirements

| Input | Required | Source |
|-------|----------|--------|
| product-vision.md | Yes | 03-strategy/ |
| jtbd-jobs-to-be-done.md | Yes | 02-research/ |
| persona-*.md files | Yes | 02-research/ |
| ANALYSIS_SUMMARY.md | Yes | 01-analysis/ |

## CRITICAL OUTPUT REQUIREMENTS

### File Name (MANDATORY)

```
[output_path]/03-strategy/PRODUCT_STRATEGY.md
```

**File naming**: UPPERCASE with underscores - `PRODUCT_STRATEGY.md`

## Output Specification

### Primary Output: `03-strategy/PRODUCT_STRATEGY.md`

```markdown
---
document_id: STRATEGY-[PROJECT]
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_GenerateStrategy
source_files:
  - 03-strategy/product-vision.md
  - 02-research/jtbd-jobs-to-be-done.md
  - 02-research/persona-*.md
  - 01-analysis/ANALYSIS_SUMMARY.md
change_history:
  - version: "1.0.0"
    date: "[YYYY-MM-DD]"
    author: "Discovery_GenerateStrategy"
    changes: "Initial strategy document generation from vision and research"
---

# Product Strategy: [Product Name]

**Strategy Date**: [Date]
**Planning Horizon**: [12-18 months]
**Status**: 🟢 Approved | 🟡 Draft

---

## 🎯 Strategic Objective

[One sentence describing what success looks like in 12-18 months]

**North Star Metric**: [Primary success measure]
**Target**: [Specific goal]

---

## 🏗️ Build vs. Buy Decision

**Decision**: BUILD | BUY | HYBRID

**Rationale**:
1. [Reason 1 with supporting evidence]
2. [Reason 2 with supporting evidence]
3. [Reason 3 with supporting evidence]

**Risk Mitigation**: [How risks of this approach will be managed]

---

## 🎯 Strategic Pillars

### Pillar 1: [Pillar Name]

**Goal**: [Specific, measurable goal for this pillar]

**Why This Pillar**:
[2-3 sentences explaining strategic importance]

**Key Tactics**:
| # | Tactic | Owner | Timeline | Dependencies |
|---|--------|-------|----------|--------------|
| 1.1 | [Specific action] | [Role] | [Quarter] | [None/Other tactics] |
| 1.2 | [Specific action] | [Role] | [Quarter] | [Dependencies] |
| 1.3 | [Specific action] | [Role] | [Quarter] | [Dependencies] |

**Success Metrics**:
- [Metric]: [Current] → [Target]
- [Metric]: [Current] → [Target]

**Risks & Mitigations**:
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| [Risk] | High/Med/Low | High/Med/Low | [Strategy] |

---

### Pillar 2: [Pillar Name]
[Same structure as Pillar 1]

---

### Pillar 3: [Pillar Name]
[Same structure as Pillar 1]

---

[Continue for 3-7 pillars total]

---

## 📊 Pillar Interdependencies

```
[Pillar 1] ──enables──▶ [Pillar 3]
     │                      │
     │                      │
     ▼                      ▼
[Pillar 2] ◀──requires── [Pillar 4]
```

### Dependency Matrix

| Pillar | Depends On | Enables |
|--------|------------|---------|
| Pillar 1 | None | Pillar 2, 3 |
| Pillar 2 | Pillar 1 | Pillar 4 |

---

## 🎭 Go-To-Market Strategy

### Phase 1: [Phase Name] ([Timeline])

**Objective**: [Phase goal]

**Target Segment**:
- **Users**: [Specific user group]
- **Size**: [Number/percentage]
- **Characteristics**: [Key traits]

**Value Proposition**: 
[What we're offering this segment]

**Channels**:
| Channel | Purpose | Metrics |
|---------|---------|---------|
| [Channel] | [Why this channel] | [Success measure] |

**Success Criteria**:
- [ ] [Measurable milestone]
- [ ] [Measurable milestone]

---

### Phase 2: [Phase Name] ([Timeline])
[Same structure as Phase 1]

---

### Phase 3: [Phase Name] ([Timeline])
[Same structure as Phase 1]

---

## 💰 Resource Strategy

### Team Requirements

| Role | Phase 1 | Phase 2 | Phase 3 |
|------|---------|---------|---------|
| [Role] | [FTE] | [FTE] | [FTE] |

### Investment Areas

| Area | Phase 1 | Phase 2 | Phase 3 | Total |
|------|---------|---------|---------|-------|
| Development | [%] | [%] | [%] | [%] |
| Design | [%] | [%] | [%] | [%] |
| Marketing | [%] | [%] | [%] | [%] |
| Operations | [%] | [%] | [%] | [%] |

---

## 🎯 Competitive Strategy

### Positioning

**Primary Differentiator**: [What sets us apart]
**Secondary Differentiators**: 
- [Differentiator 1]
- [Differentiator 2]

### Competitive Response Matrix

| Competitor Move | Our Response |
|-----------------|--------------|
| [Likely action] | [Counter-strategy] |

---

## ⚠️ Strategic Risks

### Risk Register

| # | Risk | Impact | Likelihood | Mitigation | Owner |
|---|------|--------|------------|------------|-------|
| R1 | [Risk description] | High | Medium | [Strategy] | [Role] |
| R2 | [Risk description] | Medium | High | [Strategy] | [Role] |

### Assumptions to Validate

| Assumption | Validation Method | Timeline | Decision if Wrong |
|------------|-------------------|----------|-------------------|
| [Assumption] | [How to test] | [When] | [Pivot strategy] |

---

## 📈 Strategy Review Cadence

| Review Type | Frequency | Participants | Focus |
|-------------|-----------|--------------|-------|
| Tactical | Weekly | Product team | Sprint progress |
| Strategic | Monthly | Leadership | Pillar progress |
| Vision | Quarterly | All stakeholders | Direction alignment |

---

**Document Status**: 🟢 Complete
**Created**: [Date]
**Next Review**: [Date]
**Owner**: [Product Team]
```

## Strategy Creation Process

### Step 1: Pillar Identification
```markdown
1. Review vision capabilities
2. Review JTBD priority clusters
3. Identify 3-7 strategic themes
4. Ensure each pillar is:
   - Independently valuable
   - Measurable
   - Achievable in planning horizon
```

### Step 2: Tactics Definition
```markdown
For each pillar:
1. Break into 3-5 specific tactics
2. Assign ownership
3. Estimate timeline
4. Identify dependencies
```

### Step 3: Go-To-Market Design
```markdown
1. Define target segments
2. Sequence based on:
   - Technical dependencies
   - Market readiness
   - Resource availability
3. Define success criteria per phase
```

### Step 4: Risk Assessment
```markdown
1. Identify top 5-10 risks
2. Assess impact and likelihood
3. Define mitigation strategies
4. Assign owners
```

## Quality Criteria

- [ ] 3-7 strategic pillars defined
- [ ] Each pillar has measurable goals
- [ ] Tactics are specific and actionable
- [ ] Dependencies clearly mapped
- [ ] Go-to-market phases defined
- [ ] Risks identified and mitigated
- [ ] Resource implications considered

## Integration Points

### Receives From
- Discovery_GenerateVision: Success criteria, capabilities
- Discovery_GenerateJTBD: Priority needs

### Provides To
- Discovery_GenerateRoadmap: Phase structure, priorities
- Discovery_GenerateKPIs: Pillar metrics

---

**Skill Version**: 2.0
**Framework**: Discovery Skills Framework v2.0
**Output Location**: 03-strategy/product-strategy.md
