---
name: extracting-discovery-metrics
description: Use when you need to extract quantitative data, KPIs, and measurable outcomes from discovery materials to build a data-driven business case.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-discovery-metrics started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-discovery-metrics ended '{"stage": "discovery"}'
---

# Extract Metrics

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill extracting-discovery-metrics instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_ExtractMetrics
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for extracting quantitative data, KPIs, benchmarks, and measurable outcomes from analyzed materials. Creates a metrics catalog with baselines, targets, and business context for ROI calculations and success measurement.

**Role**: You are a Metrics Analysis Specialist. Your expertise is identifying quantitative data points from research materials, understanding their business context, and organizing them into a metrics framework that supports ROI calculations and success measurement.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:extracting-discovery-metrics:started` - When skill begins
- `skill:extracting-discovery-metrics:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- After input analyzers have processed materials
- Request mentions "metrics", "KPIs", "numbers", "quantify", "ROI"
- Context involves measuring impact or setting targets
- Need to build business case with data

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Analysis Files | Yes | Output from input analyzer skills |
| Metric Categories | No | Specific categories to focus on |
| Baseline Context | No | Current state measurements |
| Output Path | Yes | Where to save metrics catalog |

## Metric Categories

### Time Metrics
- Duration (hours, days, weeks)
- Frequency (per day, per week)
- Response time
- Wait time
- Cycle time

### Volume Metrics
- Counts (records, users, transactions)
- Throughput
- Capacity
- Growth rates

### Quality Metrics
- Error rates
- Accuracy percentages
- Rework rates
- Defect counts

### Financial Metrics
- Costs (labor, tools, overhead)
- Revenue impact
- Savings potential
- Investment amounts

### Satisfaction Metrics
- Scores (NPS, CSAT)
- Ratings
- Survey results
- Complaint counts

## Extraction Framework

### 1. Number Identification
Scan for quantitative content:
- Explicit numbers (25, 3.5, 100%)
- Time expressions (3 hours, twice a week)
- Comparisons (doubled, halved, 3x faster)
- Ranges (10-15, approximately 100)

### 2. Context Capture
For each metric:
- What does it measure?
- Current vs target
- Source/confidence
- Timeframe
- Scope (per person, team, company)

### 3. Standardization
- Normalize units (hours→minutes, weekly→monthly)
- Calculate comparable rates
- Note assumptions made
- Flag estimates vs actuals

### 4. Business Impact
- Connect to pain points
- Map to potential savings
- Link to efficiency gains
- Calculate ROI potential

## Output Format

### Primary Output: `[output_path]/01-analysis/metrics-catalog.md`

```markdown
# Metrics Catalog

**Extraction Date**: [Date]
**Sources Analyzed**: [Count] files
**Total Metrics**: [Count]
**Quantified Baselines**: [N] | Targets Mentioned: [N]

---

## 📊 Metrics Dashboard

### Key Performance Indicators

| Metric | Category | Current | Target | Gap | Impact |
|--------|----------|---------|--------|-----|--------|
| [Metric 1] | Time | [Value] | [Value] | [%] | [Business impact] |
| [Metric 2] | Quality | [Value] | [Value] | [%] | [Business impact] |

### Quick ROI Summary
- **Total Annual Time Saved**: [Hours] → $[Value at rate]
- **Error Reduction Value**: [%] → $[Value]
- **Potential Annual Benefit**: $[Total]

---

## ⏱️ Time Metrics

### TM-001: [Metric Name]
**Category**: Time - Duration
**Current Value**: [Value with unit]
**Target Value**: [If mentioned]
**Scope**: [Per task/day/week/month]
**Affected Users**: [Role/count]

**Business Context**:
[What this metric measures and why it matters]

**Source Evidence**:
> "[Quote with metric]" - [Source]

**Impact Calculation**:
- Current: [Value] × [Frequency] × [Cost rate] = $[Annual cost]
- Target: [Value] × [Frequency] × [Cost rate] = $[Annual cost]
- **Potential Savings**: $[Difference]

---

### TM-002: [Metric Name]
[Same structure...]

---

## 📦 Volume Metrics

### VM-001: [Metric Name]
**Category**: Volume - Count
**Current Value**: [Value]
**Growth Rate**: [If known]
**Scope**: [Per period]

**Business Context**:
[What this metric measures]

**Source Evidence**:
> "[Quote]" - [Source]

**Capacity Implications**:
[What volume means for system/process design]

---

## ✅ Quality Metrics

### QM-001: [Metric Name]
**Category**: Quality - Error Rate
**Current Value**: [Value]%
**Target Value**: [If mentioned]
**Scope**: [Per X transactions]

**Business Context**:
[Impact of errors]

**Source Evidence**:
> "[Quote]" - [Source]

**Cost of Quality**:
- Error correction cost: [Per error]
- Current annual cost: $[Value]
- Potential savings at target: $[Value]

---

## 💰 Financial Metrics

### FM-001: [Metric Name]
**Category**: Financial - Cost
**Current Value**: $[Value]
**Period**: [Annual/Monthly/Per occurrence]
**Scope**: [Team/Company/Per user]

**Source Evidence**:
> "[Quote]" - [Source]

**Components**:
| Component | Value | Notes |
|-----------|-------|-------|
| [Labor] | $[Value] | [Basis] |
| [Tools] | $[Value] | [Basis] |
| [Overhead] | $[Value] | [Basis] |

---

## 😊 Satisfaction Metrics

### SM-001: [Metric Name]
**Category**: Satisfaction - Score
**Current Value**: [Score/Rating]
**Benchmark**: [Industry/Historical]
**Sample Size**: [If known]

**Source Evidence**:
> "[Quote]" - [Source]

**Interpretation**:
[What this score indicates]

---

## 📈 Derived Metrics

### DM-001: [Calculated Metric Name]
**Formula**: [How calculated]
**Inputs**: [Which raw metrics]
**Current Value**: [Calculated result]

**Example Calculation**:
```
[Metric A] × [Metric B] / [Metric C] = [Result]
[Value] × [Value] / [Value] = [Value]
```

---

## 🎯 Baseline vs Target Summary

| Metric ID | Metric | Baseline | Target | Gap | Priority |
|-----------|--------|----------|--------|-----|----------|
| TM-001 | [Name] | [Current] | [Target] | [%] | P0/P1/P2 |
| TM-002 | [Name] | [Current] | [Target] | [%] | P0/P1/P2 |

---

## 💵 ROI Calculation Framework

### Annual Cost Analysis (Current State)

| Category | Metric | Value | Frequency | Annual Cost |
|----------|--------|-------|-----------|-------------|
| Time | [Metric] | [Hours] | [× Rate × Count] | $[Value] |
| Errors | [Metric] | [Rate] | [× Cost per error] | $[Value] |
| Tools | [Metric] | [Cost] | [× Users] | $[Value] |
| **Total Current State Cost** | | | | **$[Total]** |

### Projected Future State

| Category | Improvement | Savings |
|----------|-------------|---------|
| Time | [%] reduction | $[Value] |
| Errors | [%] reduction | $[Value] |
| Tools | Consolidation | $[Value] |
| **Total Annual Benefit** | | **$[Total]** |

### Investment & Payback

| Investment | Amount | Notes |
|------------|--------|-------|
| Development | $[Est] | [Assumptions] |
| Training | $[Est] | [Assumptions] |
| Migration | $[Est] | [Assumptions] |
| **Total Investment** | **$[Total]** | |

**Simple Payback Period**: [Total Investment] / [Annual Benefit] = [Months]
**3-Year ROI**: ([3 × Annual Benefit] - [Investment]) / [Investment] = [%]

---

## ⚠️ Data Quality Notes

| Metric | Confidence | Notes |
|--------|------------|-------|
| TM-001 | High | Direct quote with number |
| TM-002 | Medium | Estimated from context |
| TM-003 | Low | Assumption based on industry |

---

## 📋 Metrics Not Yet Captured

| Metric Needed | Purpose | How to Obtain |
|---------------|---------|---------------|
| [Metric] | [Why needed] | [Research method] |

---

**Catalog Status**: 🟢 Complete
**Last Updated**: [Date]
```

## Error Handling

| Issue | Action |
|-------|--------|
| Vague numbers ("many", "few") | Note as qualitative, estimate if reasonable |
| Missing units | Infer from context, flag uncertainty |
| Conflicting data | Note both, indicate more reliable source |
| Incomplete calculations | Show formula, mark inputs as TBD |

## Integration Points

### Receives From
- All `Discovery_Analyze*` skills - Raw numbers and data
- `Discovery_ExtractQuotes` - Quotes with quantification

### Feeds Into
- `Discovery_GenerateKPIs` - Baseline metrics for KPI setting
- `Discovery_GenerateVision` - Impact quantification
- `Discovery_GenerateRoadmap` - Prioritization support

---

**Skill Version**: 2.0
**Framework Compatibility**: Discovery Skills Framework v2.0
