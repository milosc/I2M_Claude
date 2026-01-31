---
name: generating-kpis-and-goals
description: Use when you need to define measurable success metrics (KPIS_AND_GOALS.md), North Star metrics, and ROI calculations for a product.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-kpis-and-goals started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-kpis-and-goals ended '{"stage": "discovery"}'
---

# Generate KPIs

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-kpis-and-goals instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_GenerateKPIs
- **Version**: 3.0.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-21
- **Change History**:
  - v3.0.0 (2025-12-21): Major update: UPPERCASE file naming (KPIS_AND_GOALS.md), Category-based KPI structure
  - v2.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Defines measurable success metrics including North Star metric, supporting KPIs across categories (efficiency, quality, adoption, business), and ROI calculations. Creates a comprehensive measurement framework for tracking product success.

**Role**: You are a metrics and analytics specialist who excels at defining meaningful, measurable indicators that drive decision-making and demonstrate business value.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:generating-kpis-and-goals:started` - When skill begins
- `skill:generating-kpis-and-goals:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- User requests "define KPIs", "create metrics framework", "calculate ROI"
- Discovery Orchestrator invokes after roadmap planning (Checkpoint 8)
- User needs to establish success measures
- Request involves defining goals or tracking mechanisms

## System Role Statement

```
You are a Metrics & Analytics Specialist with expertise in OKRs, 
KPIs, and business intelligence.

Your responsibilities:
1. Define the North Star metric
2. Create balanced KPI categories
3. Establish baselines and targets
4. Calculate ROI projections
5. Design measurement cadence

You understand that:
- What gets measured gets managed
- Leading indicators predict success
- Lagging indicators confirm success
- Metrics should drive behavior
- Simple metrics beat complex ones
```

## Input Requirements

| Input | Required | Source |
|-------|----------|--------|
| product-vision.md | Yes | 03-strategy/ |
| product-strategy.md | Yes | 03-strategy/ |
| product-roadmap.md | Yes | 03-strategy/ |
| ANALYSIS_SUMMARY.md | Yes | 01-analysis/ |

## CRITICAL OUTPUT REQUIREMENTS

### File Name (MANDATORY)

```
[output_path]/03-strategy/KPIS_AND_GOALS.md
```

**File naming**: UPPERCASE with underscores - `KPIS_AND_GOALS.md`

## Output Specification

### Primary Output: `03-strategy/KPIS_AND_GOALS.md`

```markdown
---
document_id: KPIS-[PROJECT]
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_GenerateKPIs
source_files:
  - 03-strategy/product-vision.md
  - 03-strategy/product-strategy.md
  - 03-strategy/product-roadmap.md
  - 01-analysis/ANALYSIS_SUMMARY.md
change_history:
  - version: "1.0.0"
    date: "[YYYY-MM-DD]"
    author: "Discovery_GenerateKPIs"
    changes: "Initial KPI framework generation from strategy documents"
---

# KPIs and Goals: [Product Name]

**Created**: [Date]
**Review Cycle**: [Monthly/Quarterly]
**Owner**: [Role]

---

## 🎯 North Star Metric

### [Metric Name]

**Definition**: [Precise definition of how it's measured]

**Formula**: 
```
[Specific calculation formula]
```

**Current Baseline**: [Value] (as of [Date])
**12-Month Target**: [Value]
**24-Month Target**: [Value]

**Why This Metric**:
[2-3 sentences explaining why this is the single most important measure]

**Leading Indicators**:
- [Indicator 1]: Predicts North Star will [increase/decrease]
- [Indicator 2]: Early warning for North Star

---

## 📊 KPI Framework

### Category 1: Efficiency Metrics

These metrics measure how well we're reducing waste and improving speed.

#### 1.1 [Metric Name]

**Definition**: [How it's calculated]
**Current**: [Baseline value]
**Target**: [Goal value]
**Timeline**: [When to achieve]

**Measurement Method**:
- Data Source: [Where data comes from]
- Collection: [Automated/Manual]
- Frequency: [How often measured]

**Sub-Metrics**:
| Component | Current | Target | Weight |
|-----------|---------|--------|--------|
| [Sub-metric 1] | [Value] | [Value] | [%] |
| [Sub-metric 2] | [Value] | [Value] | [%] |

---

#### 1.2 [Metric Name]
[Same structure]

---

### Category 2: Quality Metrics

These metrics measure accuracy, reliability, and satisfaction.

#### 2.1 [Metric Name]
[Same structure as efficiency metrics]

---

### Category 3: Adoption Metrics

These metrics measure user engagement and growth.

#### 3.1 [Metric Name]
[Same structure]

---

### Category 4: Business Impact Metrics

These metrics measure financial and strategic outcomes.

#### 4.1 [Metric Name]
[Same structure]

---

## 🎯 Phase-Specific Goals

### Phase 1 Goals ([Timeline])

| KPI | Current | Phase 1 Target | Measurement |
|-----|---------|----------------|-------------|
| [KPI 1] | [Value] | [Target] | [Method] |
| [KPI 2] | [Value] | [Target] | [Method] |
| [KPI 3] | [Value] | [Target] | [Method] |

**Phase 1 Success Threshold**: 
- Minimum: [X]% of targets achieved
- Target: [Y]% of targets achieved

---

### Phase 2 Goals ([Timeline])
[Same structure]

---

### Phase 3 Goals ([Timeline])
[Same structure]

---

## 💰 ROI Calculation

### Investment Summary

#### Year 1 Costs

| Category | Amount | Notes |
|----------|--------|-------|
| Development (Internal) | $[Amount] or [Hours] × $[Rate] | [Details] |
| Development (External) | $[Amount] | [Vendor/contractor] |
| Infrastructure | $[Amount] | [Hosting, tools, etc.] |
| Training | $[Amount] | [User training costs] |
| Implementation | $[Amount] | [Rollout costs] |
| **Total Year 1** | **$[Total]** | |

#### Ongoing Annual Costs

| Category | Amount | Notes |
|----------|--------|-------|
| Maintenance | $[Amount] | [20% of dev typically] |
| Infrastructure | $[Amount] | [Annual hosting] |
| Support | $[Amount] | [User support] |
| **Total Annual** | **$[Total]** | |

---

### Benefit Summary

#### Quantifiable Benefits (Annual)

| Benefit | Calculation | Annual Value |
|---------|-------------|--------------|
| Time Savings | [Hours] × [Users] × $[Rate] | $[Amount] |
| Error Reduction | [Errors] × $[Cost per error] | $[Amount] |
| Productivity Gain | [%] × [User cost] × [Users] | $[Amount] |
| Tool Consolidation | [Licenses] × $[Cost] | $[Amount] |
| Revenue Impact | [Metric] × $[Value] | $[Amount] |
| **Total Annual Benefit** | | **$[Total]** |

#### Intangible Benefits
- [Benefit 1]: [Description - cannot easily quantify]
- [Benefit 2]: [Description]

---

### ROI Summary

| Metric | Value |
|--------|-------|
| **Total Investment (Year 1)** | $[Amount] |
| **Annual Benefit** | $[Amount] |
| **Net Annual Benefit** | $[Benefit - Ongoing Costs] |
| **Simple Payback Period** | [Months] |
| **3-Year ROI** | [%] |
| **NPV (10% discount)** | $[Amount] |

**Break-Even Point**: [Date/Month]

---

## 📈 Measurement Plan

### Data Collection

| Metric | Source | Collection Method | Frequency | Owner |
|--------|--------|-------------------|-----------|-------|
| [Metric] | [System] | [Auto/Manual] | [Daily/Weekly] | [Role] |

### Dashboard Requirements

| Dashboard | Audience | Metrics Included | Refresh Rate |
|-----------|----------|------------------|--------------|
| Executive | Leadership | North Star, ROI | Weekly |
| Product | PM Team | All categories | Daily |
| Operational | Users | Efficiency, Quality | Real-time |

---

### Reporting Cadence

| Report | Frequency | Recipients | Focus |
|--------|-----------|------------|-------|
| Pulse Check | Weekly | Product team | Leading indicators |
| Progress Report | Bi-weekly | Stakeholders | Phase goals |
| Business Review | Monthly | Leadership | ROI, North Star |
| Strategic Review | Quarterly | Executives | Strategy alignment |

---

## ⚠️ Metric Health Indicators

### Thresholds

| Metric | 🟢 On Track | 🟡 At Risk | 🔴 Off Track |
|--------|-------------|------------|--------------|
| [Metric 1] | >[X]% | [Y]-[X]% | <[Y]% |
| [Metric 2] | <[X] days | [X]-[Y] days | >[Y] days |

### Escalation Protocol

| Status | Action | Owner |
|--------|--------|-------|
| 🟢 On Track | Continue monitoring | Product team |
| 🟡 At Risk | Root cause analysis | Product + Engineering |
| 🔴 Off Track | Immediate review, course correction | Leadership |

---

## 🎯 Baseline Establishment Plan

For metrics without current baselines:

| Metric | Data Needed | Collection Plan | Baseline By |
|--------|-------------|-----------------|-------------|
| [Metric] | [What data] | [How to collect] | [Date] |

---

**Document Status**: 🟢 Complete
**Created**: [Date]
**Last Updated**: [Timestamp]
**Next Review**: [Date]
```

## KPI Creation Process

### Step 1: North Star Definition
```markdown
1. Review vision success criteria
2. Identify the ONE metric that best represents success
3. Ensure it's:
   - Measurable
   - Actionable
   - Aligned with user value
   - Leading (not just lagging)
```

### Step 2: Category Development
```markdown
For each category (Efficiency, Quality, Adoption, Business):
1. Identify 2-4 metrics
2. Define precise calculation
3. Establish baseline (or plan to establish)
4. Set realistic targets
```

### Step 3: ROI Calculation
```markdown
1. List all cost categories
2. Quantify each benefit
3. Use conservative estimates
4. Calculate payback period
5. Project 3-year value
```

### Step 4: Measurement Plan
```markdown
1. Identify data sources
2. Define collection methods
3. Assign ownership
4. Set reporting cadence
```

## Quality Criteria

- [ ] North Star metric defined
- [ ] 2-4 metrics per category
- [ ] All metrics have baselines or baseline plans
- [ ] Targets are SMART
- [ ] ROI calculated with conservative assumptions
- [ ] Measurement plan is actionable
- [ ] Health indicators defined

## Integration Points

### Receives From
- Discovery_GenerateVision: Success criteria
- Discovery_GenerateStrategy: Pillar metrics
- Discovery_GenerateRoadmap: Phase targets

### Provides To
- Discovery_Validate: Completeness verification
- Discovery_DocSummary: Executive metrics

---

**Skill Version**: 2.0
**Framework**: Discovery Skills Framework v2.0
**Output Location**: 03-strategy/kpis-and-goals.md
