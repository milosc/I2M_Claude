---
name: generating-jtbd
description: Use when you need to transform pain points and user research into prioritized Jobs-To-Be-Done (JTBD) statements organized by persona.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-jtbd started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-jtbd ended '{"stage": "discovery"}'
---

# Generate JTBD

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-jtbd instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_GenerateJTBD
- **Version**: 3.0.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-21
- **Change History**:
  - v3.0.0 (2025-12-21): Major update: Persona-organized jobs, Job Steps, Success Criteria, Functional/Emotional/Social categories
  - v2.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Transforms extracted pain points, user types, and workflows into structured Jobs-To-Be-Done (JTBD) statements. Creates a comprehensive catalog of user needs **organized by persona** with job steps, success criteria, and traceability to pain points and gaps.

**Role**: You are a Jobs-To-Be-Done specialist who excels at translating user research findings into actionable need statements that drive product development decisions.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:generating-jtbd:started` - When skill begins
- `skill:generating-jtbd:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- User requests "generate JTBD", "create jobs to be done", "extract user needs"
- Discovery Orchestrator invokes after persona synthesis (Checkpoint 4)
- User wants to understand what users are trying to accomplish
- Request involves translating pain points into opportunity statements

## System Role Statement

```
You are a Jobs-To-Be-Done specialist with deep expertise in the JTBD framework.

Your responsibilities:
1. Extract jobs from pain points, workflows, and user research
2. Structure jobs in the canonical JTBD format
3. Organize jobs by feature area (8-12 areas typical)
4. Assign jobs to relevant personas
5. Prioritize based on frequency, impact, and current workaround difficulty
6. Identify opportunities where jobs are underserved

You understand that:
- Jobs are stable over time (unlike solutions)
- Jobs have functional, emotional, and social dimensions
- Current workarounds reveal job importance
- Jobs should be solution-agnostic
```

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
- output file location (JOBS_TO_BE_DONE.md)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "generating-jtbd"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "generating-jtbd" --stage discovery
```

Logging is handled automatically by the skill framework. No user action required.

---

## Input Requirements

| Input | Required | Source |
|-------|----------|--------|
| ANALYSIS_SUMMARY.md | Yes | 01-analysis/ |
| persona-*.md files | Yes | 02-research/ |
| Pain points registry | Yes | From ANALYSIS_SUMMARY |
| Workflow mappings | Yes | From ANALYSIS_SUMMARY |
| User quotes library | Yes | From ANALYSIS_SUMMARY |

## CRITICAL OUTPUT REQUIREMENTS

### File Name (MANDATORY)

```
[output_path]/02-research/JOBS_TO_BE_DONE.md
```

**File naming**: UPPERCASE with underscores - `JOBS_TO_BE_DONE.md`

### Organization (MANDATORY)

Jobs MUST be organized **by Persona**, NOT by feature area:
- `## P-1.1: [Persona Role] ([Name]) Jobs`
- `## P-1.2: [Persona Role] ([Name]) Jobs`
- etc.

## Output Specification

### Primary Output: `02-research/JOBS_TO_BE_DONE.md`

```markdown
---
document_id: DISC-JTBD-001
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_GenerateJTBD
---

# Jobs-To-Be-Done: [Product Name]

**Version**: 1.0.0
**Created**: [YYYY-MM-DD]

---

## Executive Summary

This document captures the Jobs-To-Be-Done (JTBD) for the [Product Name] project, derived from persona analysis and pain point research. Jobs are organized by persona and prioritized based on frequency, importance, and connection to identified pain points.

**Total Jobs Identified**: [N]
- Functional Jobs: [N]
- Emotional Jobs: [N]
- Social Jobs: [N]

---

## JTBD Framework

Each job follows the structure:
```
When [situation], I want to [motivation], so I can [expected outcome].
```

Jobs are rated on:
- **Frequency**: How often the job occurs (Daily, Weekly, Monthly, Quarterly)
- **Importance**: Critical, High, Medium, Low
- **Satisfaction**: Current satisfaction with existing solution (1-5)

---

## P-1.1: [Role Name] ([Persona First Name]) Jobs

### JTBD-1.1: [Short Descriptive Title]

**Statement**: When [situation], I want to [motivation], so I can [expected outcome].

| Attribute | Value |
|-----------|-------|
| Frequency | [Daily (N times/day) / Weekly / Monthly / Quarterly] |
| Importance | [Critical / High / Medium / Low] |
| Current Satisfaction | [N]/5 |
| Related Pain Points | PP-[X].[Y], PP-[X].[Y] |
| Related Gaps | GAP-[XXX], GAP-[XXX] |

**Job Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]
4. [Step 4]

**Success Criteria**:
- [Measurable criterion 1]
- [Measurable criterion 2]
- [Measurable criterion 3]

---

### JTBD-1.2: [Short Descriptive Title]

[Same structure as above]

---

### JTBD-1.X: [Title] (Emotional)

**Statement**: When [context], I want to [emotional motivation], so I [emotional outcome].

[Mark emotional jobs with (Emotional) in title]
[Mark social jobs with (Social) in title]

---

## P-1.2: [Role Name] ([Persona First Name]) Jobs

[Repeat pattern for each persona]

---

## JTBD Summary by Priority

### Critical Jobs (Must Address)

| ID | Job | Persona | Gap |
|----|-----|---------|-----|
| JTBD-1.1 | [Title] | [Role] | GAP-[XXX] |

### High Priority Jobs

| ID | Job | Persona | Gap |
|----|-----|---------|-----|
| JTBD-2.1 | [Title] | [Role] | GAP-[XXX] |

---

## Traceability Matrix

| JTBD | Pain Points | Gaps | Persona |
|------|-------------|------|---------|
| JTBD-1.1 | PP-[list] | GAP-[list] | P-1.1 |
| JTBD-1.2 | PP-[list] | GAP-[list] | P-1.1 |

---

**Document Status**: Complete
**Next Phase**: Generate Product Vision and Strategy

*Generated by Discovery Skills Framework v5.0*
```

## Extraction Process

### Step 1: Gather Sources
```markdown
Read and synthesize:
1. ANALYSIS_SUMMARY.md - Pain points, workflows, quotes
2. All persona-*.md files - Goals, contexts, frustrations
```

### Step 2: Identify Feature Areas
```markdown
Group related activities into 8-12 feature areas:
- Look for common themes in pain points
- Consider workflow stages
- Align with typical product modules
```

### Step 3: Extract Jobs per Area
For each feature area and persona combination:
```markdown
1. What triggers this need? (When...)
2. What action do they want to take? (I want to...)
3. What outcome do they expect? (So I can...)
4. How do they do it today?
5. How painful is the current approach?
```

### Step 4: Prioritize
```markdown
P0 Criteria (any one):
- Blocks critical work
- Daily occurrence + high impact
- No viable workaround

P1 Criteria:
- Significant impact
- Weekly occurrence
- Painful workaround exists

P2 Criteria:
- Moderate impact
- Less frequent
- Acceptable workaround exists
```

### Step 5: Calculate Opportunity Scores
```markdown
Opportunity Score = Importance + (Importance - Satisfaction)

Where:
- Importance: How critical is this job? (1-10)
- Satisfaction: How well served currently? (1-10)

Higher scores = bigger opportunities
```

## Quality Criteria

### Completeness
- [ ] 30-50 total JTBDs identified
- [ ] All personas have associated JTBDs
- [ ] All major pain points addressed
- [ ] All workflows covered

### JTBD Quality
- [ ] Jobs are solution-agnostic
- [ ] Jobs use "When/I want to/So I can" format
- [ ] Jobs include all three dimensions where applicable
- [ ] Current workarounds documented

### Traceability
- [ ] Each JTBD links to source evidence
- [ ] Pain point references included
- [ ] Persona assignments clear

### Prioritization
- [ ] P0/P1/P2 assigned to all jobs
- [ ] Priority rationale clear
- [ ] Phase mapping provided

## JTBD Writing Guidelines

### Good JTBD Examples
```markdown
✅ When I receive a new application, I want to quickly assess candidate fit, 
   so I can prioritize my review queue and respond within 24 hours.

✅ When I'm preparing for an interview, I want to see the candidate's 
   complete history in one view, so I can ask informed questions 
   without shuffling between screens.
```

### Poor JTBD Examples
```markdown
❌ I want a better dashboard. (No context, solution-specific)

❌ When using the system, I want it to be faster. (Vague, no outcome)

❌ I need to click fewer buttons. (Implementation detail)
```

### Transformation Patterns

| Pain Point | JTBD Transformation |
|------------|---------------------|
| "I waste time switching between systems" | When [context], I want to access all information in one place, so I can [outcome] |
| "I don't know what stage candidates are in" | When managing my pipeline, I want to see candidate status at a glance, so I can prioritize actions |
| "I forget to follow up" | When a candidate reaches a decision point, I want to be reminded to take action, so I can maintain momentum |

## Error Handling

| Issue | Response |
|-------|----------|
| Insufficient pain points | Request additional research or note gap |
| No clear user types | Use generic personas, flag for follow-up |
| Overlapping jobs | Consolidate or distinguish by context |
| Solution-specific language | Reframe to focus on outcome |

## Integration Points

### Receives From
- Discovery_ExtractPainPoints: Pain point registry
- Discovery_ExtractUserTypes: User profiles
- Discovery_ExtractWorkflows: Process maps
- Discovery_ExtractQuotes: Evidence library
- Discovery_GeneratePersona: Persona files

### Provides To
- Discovery_GenerateVision: User needs summary
- Discovery_GenerateStrategy: Prioritized needs
- Discovery_GenerateRoadmap: Feature requirements
- Discovery_SpecScreens: Functionality requirements

---

**Skill Version**: 3.0.0
**Framework Compatibility**: Discovery Skills Framework v5.0
**Output Location**: 02-research/JOBS_TO_BE_DONE.md
