---
name: analyzing-discovery-feedback
description: Use when you need to analyze feedback impact across discovery artifacts, identifying affected files and generating impact matrices.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-discovery-feedback started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-discovery-feedback ended '{"stage": "discovery"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-discovery-feedback instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

---

# Analyze Discovery Feedback

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_FeedbackAnalyzer
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Milos Cigoj
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description
Analyzes incoming feedback (text or file) and performs comprehensive impact analysis across all discovery artifacts. Identifies which files, sections, and traceability chains would be affected by implementing the feedback.

**Role**: You are a Feedback Impact Analyst. Your expertise is understanding feedback context, mapping it to existing discovery artifacts, and producing actionable impact assessments.

## Execution Logging (MANDATORY)

This skill logs all execution to the global pipeline progress registry. Logging is automatic and requires no manual configuration.

### How Logging Works

Every execution of this skill is logged to `_state/lifecycle.json`:

- **start_event**: Logged when skill execution begins
- **end_event**: Logged when skill execution completes

Events include:
- skill_name, intent, stage, system_name
- start/end timestamps
- status (completed/failed)
- output files created (feedback analysis)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "analyzing-discovery-feedback"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "analyzing-discovery-feedback" --stage discovery
```

Logging is handled automatically by the skill framework. No user action required.

---

## Trigger Conditions

- User provides feedback (text or file path)
- Request mentions "analyze feedback", "feedback impact", "change request"
- Context involves modifying existing discovery outputs

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Feedback Content | Yes | Raw feedback text or path to .md/.txt file |
| System Name | Yes | Target ClientAnalysis_<SystemName> folder |
| Discovery Path | Yes | Path to discovery outputs |

## Impact Analysis Framework

### 1. Feedback Classification

Categorize the feedback by primary impact area:

| Category | ID Prefix | Description |
|----------|-----------|-------------|
| Persona | CAT-PER | Affects user personas, roles, behaviors |
| Pain Point | CAT-PP | New/modified pain points |
| JTBD | CAT-JTBD | Changes to jobs-to-be-done |
| Vision | CAT-VIS | Strategic vision updates |
| Strategy | CAT-STR | Product strategy changes |
| Roadmap | CAT-RDM | Timeline or prioritization changes |
| KPIs | CAT-KPI | Metrics and goals modifications |
| Screen Design | CAT-SCR | UI/screen definition changes |
| Navigation | CAT-NAV | Navigation structure changes |
| Data Model | CAT-DAT | Data fields/entities changes |
| General | CAT-GEN | Cross-cutting or unclear scope |

### 2. Artifact Scanning

For each category, scan the relevant discovery outputs:

```
ClientAnalysis_<SystemName>/
├── 01-analysis/
│   ├── ANALYSIS_SUMMARY.md
│   └── PAIN_POINTS.md
├── 02-research/
│   ├── personas/PERSONA_*.md
│   └── JOBS_TO_BE_DONE.md
├── 03-strategy/
│   ├── PRODUCT_VISION.md
│   ├── PRODUCT_STRATEGY.md
│   ├── PRODUCT_ROADMAP.md
│   └── KPIS_AND_GOALS.md
├── 04-design-specs/
│   ├── screen-definitions.md
│   ├── navigation-structure.md
│   ├── data-fields.md
│   └── interaction-patterns.md
└── 05-documentation/
    ├── INDEX.md
    └── README.md
```

### 3. Impact Matrix Generation

For each affected file, determine:

| Field | Description |
|-------|-------------|
| File Path | Relative path to file |
| Section | Specific section within file |
| Impact Level | High/Medium/Low |
| Change Type | Add/Modify/Delete/Review |
| Traceability IDs | Affected PP-*, JTBD-*, US-*, S-* |
| Downstream Effects | Files that depend on this |
| Effort Estimate | S/M/L/XL |

### 4. Priority Scoring

Calculate priority score based on:

```
Priority Score = (Impact Level * 3) + (Traceability Depth * 2) + (User Count * 1)

Where:
- Impact Level: High=3, Medium=2, Low=1
- Traceability Depth: Number of downstream dependencies
- User Count: Number of affected personas
```

## Output Format

### Primary Output: `IMPACT_ANALYSIS.md` (in feedback session folder)

```markdown
---
document_id: FB-IMPACT-<ID>
version: 1.0.0
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
generated_by: Discovery_FeedbackAnalyzer
source_files:
  - <feedback_source>
change_history:
  - version: "1.0.0"
    date: "<YYYY-MM-DD>"
    author: "Discovery_FeedbackAnalyzer"
    changes: "Initial impact analysis"
---

# Feedback Impact Analysis

## Feedback Summary
**ID**: FB-<NNN>
**Received**: <YYYY-MM-DD HH:MM>
**Source**: <who provided feedback>
**Inputter**: <who entered it>

### Original Feedback
> [Feedback content here]

---

## Classification

| Category | Confidence | Primary IDs |
|----------|------------|-------------|
| <CAT-XXX> | High/Medium/Low | <IDs> |

---

## Impact Matrix

### High Impact Files

| File | Section | Change Type | Traceability | Downstream | Effort |
|------|---------|-------------|--------------|------------|--------|
| <path> | <section> | <type> | <IDs> | <count> | <S/M/L> |

### Medium Impact Files

| File | Section | Change Type | Traceability | Downstream | Effort |
|------|---------|-------------|--------------|------------|--------|
| <path> | <section> | <type> | <IDs> | <count> | <S/M/L> |

### Low Impact Files (Review Recommended)

| File | Section | Reason |
|------|---------|--------|
| <path> | <section> | <reason> |

---

## Traceability Chain

```
[Affected IDs] → [Downstream IDs] → [Further Downstream]
```

### Upstream Impact
- **Client Facts**: [CF-IDs affected]
- **Pain Points**: [PP-IDs affected]

### Downstream Impact
- **JTBDs**: [JTBD-IDs affected]
- **Requirements**: [US-IDs, FR-IDs affected]
- **Screens**: [S-IDs affected]

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| <risk> | High/Med/Low | High/Med/Low | <action> |

---

## Priority Score: <N>/30

**Recommendation**: [Proceed/Review/Defer]

---

## Next Steps

1. [ ] Review impact matrix with stakeholder
2. [ ] Decide: Approve / Reject / Modify
3. [ ] If approved, proceed to implementation planning
```

## Integration Points

### Receives From
- User input (text or file)
- `/discovery-feedback` command

### Feeds Into
- `Discovery_FeedbackRegister` - Impact data for registry
- `Discovery_FeedbackPlanner` - Impact matrix for planning

## Error Handling

| Issue | Action |
|-------|--------|
| File not found in discovery | Note as "Not Found", continue analysis |
| Ambiguous category | Assign multiple categories, flag for review |
| No matching traceability IDs | Flag as "New" - may require new IDs |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: Discovery Skills Framework v2.0
