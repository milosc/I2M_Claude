---
name: summarizing-discovery-docs
description: Use when you need to generate an executive summary (DOCUMENTATION_SUMMARY.md) of the entire product discovery package.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill summarizing-discovery-docs started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill summarizing-discovery-docs ended '{"stage": "discovery"}'
---

# Summarize Discovery Docs

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill summarizing-discovery-docs instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_DocSummary
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for creating executive summaries and documentation overviews. Generates DOCUMENTATION_SUMMARY.md that provides stakeholders with a concise overview of the entire documentation package in 5-10 minutes reading time.

**Role**: You are an Executive Communications Specialist. Your expertise is distilling complex documentation into clear, actionable summaries for time-constrained stakeholders. You understand that executives need key insights quickly without losing important nuance.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:summarizing-discovery-docs:started` - When skill begins
- `skill:summarizing-discovery-docs:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- All discovery phases (1-9) are complete
- Request mentions "create summary", "executive summary", "documentation overview"
- User wants a quick overview of the documentation package
- Checkpoint 10 in orchestrator flow (alongside DocIndex)

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Output Path | Yes | Root folder with all generated content |
| Product Name | Yes | From earlier phases |
| All Strategy Files | Yes | Vision, strategy, roadmap, KPIs |
| Persona Files | Yes | For user summary |
| JTBD File | Yes | For needs summary |
| Design Spec Files | Yes | For readiness summary |

## Output Files

This skill creates 1 file in `[output_path]/05-documentation/`:

- `DOCUMENTATION_SUMMARY.md` - Executive summary of entire package

## Summary Sections

### 1. Executive Overview
- One-paragraph product description
- Key stakeholder value proposition
- Timeline overview

### 2. Problem Statement
- Top 3 pain points synthesized
- Impact quantification
- Current state summary

### 3. Solution Approach
- Vision one-liner
- Key capabilities (3-5)
- Differentiation points

### 4. User Summary
- Persona count and names
- Key user insights
- Primary needs

### 5. Roadmap Preview
- Phase count and timeline
- Epic highlights
- Key milestones

### 6. Success Metrics
- North Star metric
- Primary KPIs (3-5)
- ROI summary

### 7. Prototype Readiness
- Screen count
- Data model summary
- Implementation readiness

### 8. Next Steps
- Recommended actions
- Key decisions needed
- Resource requirements

## Output Format

### DOCUMENTATION_SUMMARY.md Template

```markdown
# [Product Name] - Documentation Summary

**Package Date**: [Date]
**Analysis Duration**: ~[N] hours
**Total Documents**: [N] files
**Status**: 🟢 Ready for Implementation

---

## 📋 Executive Overview

[Product Name] is a [one-sentence description of what it is and who it's for].

This documentation package provides everything needed to understand the product direction and begin implementation, including:
- [N] validated user personas
- [N] jobs-to-be-done
- Complete strategic direction (vision, strategy, roadmap)
- Production-ready design specifications
- [N] screens defined with data models

**Timeline**: [Phase 1 duration] for MVP, [Total duration] for full vision

---

## 🔴 The Problem

### Top Pain Points

1. **[Pain Point 1 - Title]**
   - [One sentence description]
   - Impact: [Quantified impact]
   - Affects: [User types]

2. **[Pain Point 2 - Title]**
   - [One sentence description]
   - Impact: [Quantified impact]
   - Affects: [User types]

3. **[Pain Point 3 - Title]**
   - [One sentence description]
   - Impact: [Quantified impact]
   - Affects: [User types]

### Current State Impact
- [Key metric 1]: [Current state]
- [Key metric 2]: [Current state]
- [Key metric 3]: [Current state]

**Total Opportunity**: [Quantified if available]

---

## 💡 The Solution

### Vision Statement
> [One compelling sentence from product-vision.md]

### Key Capabilities

| Capability | Addresses | Impact |
|------------|-----------|--------|
| [Capability 1] | [Pain Point] | [Expected improvement] |
| [Capability 2] | [Pain Point] | [Expected improvement] |
| [Capability 3] | [Pain Point] | [Expected improvement] |
| [Capability 4] | [Pain Point] | [Expected improvement] |
| [Capability 5] | [Pain Point] | [Expected improvement] |

### Differentiation
- [Key differentiator 1]
- [Key differentiator 2]
- [Key differentiator 3]

---

## 👥 User Summary

### Primary Users ([N] Personas Created)

| Persona | Role | Count | Key Need |
|---------|------|-------|----------|
| [Persona 1 Name] | [Role] | [N] | [One-line need] |
| [Persona 2 Name] | [Role] | [N] | [One-line need] |
| [Persona 3 Name] | [Role] | [N] | [One-line need] |

### Key User Insights
1. **[Insight 1]**: [Supporting detail]
2. **[Insight 2]**: [Supporting detail]
3. **[Insight 3]**: [Supporting detail]

### Jobs-to-Be-Done Summary
- **Total JTBDs**: [N]
- **Critical (P0)**: [N]
- **High Priority (P1)**: [N]
- **Feature Areas**: [N]

---

## 🗺️ Roadmap Preview

### Timeline Overview

| Phase | Duration | Focus | Epics |
|-------|----------|-------|-------|
| Phase 1 | [Duration] | [Focus area] | [N] |
| Phase 2 | [Duration] | [Focus area] | [N] |
| Phase 3 | [Duration] | [Focus area] | [N] |

### Phase 1 Highlights (MVP)
- **Epic 1**: [Name] - [One sentence]
- **Epic 2**: [Name] - [One sentence]
- **Epic 3**: [Name] - [One sentence]

### Key Milestones
1. [Milestone 1]: [Target date/timeframe]
2. [Milestone 2]: [Target date/timeframe]
3. [Milestone 3]: [Target date/timeframe]

---

## 📊 Success Metrics

### North Star Metric
**[Metric Name]**: [Current] → [Target]
- Measurement: [How measured]
- Timeline: [When to achieve]

### Primary KPIs

| KPI | Current | Target | Improvement |
|-----|---------|--------|-------------|
| [KPI 1] | [Value] | [Value] | [%] |
| [KPI 2] | [Value] | [Value] | [%] |
| [KPI 3] | [Value] | [Value] | [%] |

### ROI Summary
- **Investment**: [Amount/effort]
- **Annual Benefit**: [Amount]
- **Payback Period**: [Duration]
- **3-Year ROI**: [Percentage]

---

## 🎨 Prototype Readiness

### What's Ready

| Component | Status | Details |
|-----------|--------|---------|
| Screen Inventory | 🟢 | [N] screens defined |
| Navigation Structure | 🟢 | [N] primary flows |
| Data Model | 🟢 | [N] entities, [N] fields |
| Sample Data | 🟢 | [N] records ready |
| UI Components | 🟢 | Design system defined |
| Interactions | 🟢 | Patterns documented |

### Implementation Estimate
- **Phase 1 Screens**: [N]
- **Complexity**: [Low/Medium/High]
- **Estimated Effort**: [Duration/FTE]

---

## 🚀 Next Steps

### Immediate Actions
1. [ ] [Action 1] - [Owner if known]
2. [ ] [Action 2] - [Owner if known]
3. [ ] [Action 3] - [Owner if known]

### Key Decisions Needed
1. **[Decision 1]**: [Options/context]
2. **[Decision 2]**: [Options/context]

### Resource Requirements
- **Design**: [Estimate]
- **Development**: [Estimate]
- **QA**: [Estimate]

---

## 📁 Full Documentation

For complete details, see:
- [INDEX.md](./INDEX.md) - Master navigation
- [README.md](./README.md) - Documentation guide
- [GETTING_STARTED.md](./GETTING_STARTED.md) - Role-based quick start

---

## 📊 Package Statistics

| Category | Count |
|----------|-------|
| **Total Files** | [N] |
| **Pain Points** | [N] |
| **Personas** | [N] |
| **JTBDs** | [N] |
| **Screens** | [N] |
| **Data Entities** | [N] |

---

**Summary Generated**: [Date]
**Framework**: Discovery Skills v2.0
**Package Status**: 🟢 Complete
```

## Content Selection Guidelines

### For Problem Section
- Select top 3 pain points by:
  1. Severity (P0 first)
  2. User impact breadth
  3. Quantified impact available
- Synthesize, don't copy verbatim
- Lead with business impact

### For Solution Section
- Vision: Use exact statement from vision doc
- Capabilities: Map directly to pain points
- Keep to 5 key capabilities max

### For User Section
- List all primary personas
- Highlight surprising insights
- Focus on actionable information

### For Roadmap Section
- Phase overview only (details in roadmap doc)
- Highlight MVP scope
- Clear milestones with dates/timeframes

### For Metrics Section
- North Star must be measurable
- Include only metrics with baselines
- ROI only if data supports calculation

## Quality Checklist

Before finalizing:
- [ ] Can be read in 5-10 minutes
- [ ] All numbers match source documents
- [ ] No jargon without definition
- [ ] Links work
- [ ] Actionable next steps
- [ ] Executive-appropriate tone

## Writing Guidelines

### Tone
- Confident but not overselling
- Data-driven where possible
- Action-oriented
- Professionally optimistic

### Length
- Target 2-3 pages when printed
- 1,000-1,500 words maximum
- Dense with information, not filler

### Formatting
- Heavy use of tables for scannability
- Bold key numbers
- Clear section headers
- Minimal prose, maximum information

## Error Handling

| Issue | Action |
|-------|--------|
| Missing source data | Mark with [TBD] or [Data needed] |
| Conflicting information | Use most recent source |
| No quantified impact | Use qualitative descriptions |
| Missing ROI data | Omit ROI section, note in next steps |

## Integration Points

### Receives From
- `Discovery_GenerateVision` - Vision statement
- `Discovery_GenerateRoadmap` - Phase overview
- `Discovery_GenerateKPIs` - Metrics summary
- `Discovery_ExtractPainPoints` - Top pain points
- `Discovery_GeneratePersona` - Persona list

### Feeds Into
- Stakeholder presentations
- Decision-maker briefings
- Project kickoff materials

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
