---
name: Implementation Change Analyzer
description: Use when analyzing change requests (bugs, improvements, feedback) using Kaizen root cause analysis methods (5 Whys, Fishbone, A3, Gemba Walk).
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_ChangeAnalyzer started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_ChangeAnalyzer ended '{"stage": "implementation"}'
---

# Implementation Change Analyzer

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill Implementation_ChangeAnalyzer instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

Applies Kaizen problem-solving techniques to analyze change requests before any fixes are attempted. Based on Toyota Production System principles with 70+ years of real-world validation.

---

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:Implementation_ChangeAnalyzer:started` - When skill begins
- `skill:Implementation_ChangeAnalyzer:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Prerequisites

1. **Traceability Guard Check**: This skill invokes `Traceability_Guard` before execution.
   - If guard fails, execution stops with guidance to run `/traceability-init`.
   - Required files: `task_registry.json`, `change_request_registry.json`

2. **Implementation Exists**: Code in `Implementation_<System>/`
3. **Change Request Received**: Description of issue or improvement
4. **Session Folder Created**: `change-requests/<YYYY-MM-DD>_CR-<NNN>/`

## Core Principle

> **"Fix the system, not just the symptom"**
>
> Most bugs and quality issues are symptoms of deeper systemic problems.
> Fixing only the symptom leads to recurring issues.
> Finding and addressing the root cause prevents entire classes of problems.

## Analysis Method Selection

```
TRIAGE change request:

INPUT:
    - severity: critical | high | medium | low
    - complexity: simple | moderate | complex
    - type: bug | improvement | feedback

OUTPUT analysis_method:

    IF severity == "critical" OR complexity == "complex":
        RETURN "A3_FULL"
    ELIF severity == "high" OR complexity == "moderate":
        RETURN "FIVE_WHYS"
    ELIF type == "bug" AND unfamiliar_code:
        RETURN "GEMBA_THEN_FIVE_WHYS"
    ELSE:
        RETURN "QUICK_CHECK"
```

## Method 1: Quick Check

**When**: Simple, low-risk changes with obvious cause.

```
PROCEDURE quick_check:

1. VERIFY reproduction
   - Confirm the issue exists
   - Document reproduction steps
   - Note environment details

2. IDENTIFY immediate cause
   - Locate the problematic code
   - Understand what's wrong

3. CONFIRM fix location
   - Identify file(s) to change
   - Verify scope is limited

4. DOCUMENT briefly
   - Root cause (1-2 sentences)
   - Proposed fix (1-2 sentences)

DURATION: 10-15 minutes

OUTPUT FORMAT:
```

```markdown
## Quick Analysis: CR-<ID>

**Issue**: [Brief description]
**Immediate Cause**: [What's wrong]
**Fix Location**: [File:line]
**Proposed Fix**: [What to change]
**Risk**: Low
```

## Method 2: Five Whys

**When**: Moderate complexity, need to find root cause.

```
PROCEDURE five_whys:

1. STATE the problem clearly
   - Observable symptom
   - Specific, not vague
   - Facts, not opinions

2. ASK "Why?" iteratively
   For each answer, ask why again

3. BRANCH when needed
   - If multiple causes emerge, explore each
   - Track all branches

4. STOP at root cause
   - Usually process/systemic issues
   - Not always exactly 5 whys
   - "Human error" is not a root cause (ask why error was possible)

5. VALIDATE chain
   - Work backwards: does root cause → symptom?
   - Is this actionable?

DEPTH GUIDELINES:
    - Stop when: You reach process, policy, or systemic issues
    - Keep going if: Answer is "human error" or "forgot to"
    - Branch when: Multiple contributing factors exist
    - Usually 3-7 levels deep

DURATION: 30-60 minutes

OUTPUT FORMAT:
```

```markdown
## Five Whys Analysis: CR-<ID>

### Problem Statement
[Clear, specific description of the observable symptom]

### Analysis Chain

**Why 1**: [Immediate cause - what code triggered it?]
> Evidence: [How you know this]

**Why 2**: [Why did that code behave that way?]
> Evidence: [How you know this]

**Why 3**: [Why was it written/configured that way?]
> Evidence: [How you know this]

**Why 4**: [Why wasn't this caught earlier?]
> Evidence: [How you know this]

**Why 5**: [What systemic issue allowed this?]
> Evidence: [How you know this]

### Root Cause
[Fundamental issue identified]

### Contributing Factors
- [Factor 1]
- [Factor 2]

### Countermeasures
| Priority | Action | Addresses |
|----------|--------|-----------|
| 1 | [Immediate fix] | Symptom |
| 2 | [Prevention] | Root cause |
| 3 | [Systemic improvement] | Future prevention |
```

## Method 3: Fishbone (Cause-and-Effect)

**When**: Complex issues with multiple contributing factors.

```
PROCEDURE fishbone_analysis:

1. STATE the problem (the "effect")
   - Specific, measurable outcome
   - Not the cause, the symptom

2. EXPLORE each category
   For each of 6 categories, brainstorm potential causes:

   PEOPLE
   ├─ Skills/training gaps?
   ├─ Communication issues?
   ├─ Team dynamics?
   └─ Knowledge silos?

   PROCESS
   ├─ Workflow gaps?
   ├─ Review failures?
   ├─ Missing standards?
   └─ Documentation issues?

   TECHNOLOGY
   ├─ Tool limitations?
   ├─ Infrastructure issues?
   ├─ Dependency problems?
   └─ Configuration drift?

   ENVIRONMENT
   ├─ Dev/prod differences?
   ├─ External factors?
   ├─ Resource constraints?
   └─ Timing issues?

   METHODS
   ├─ Architectural issues?
   ├─ Pattern violations?
   ├─ Design decisions?
   └─ Technical debt?

   MATERIALS
   ├─ Data quality issues?
   ├─ Third-party problems?
   ├─ Input validation?
   └─ External dependencies?

3. DIG DEEPER on promising causes
   - Use 5 Whys on each significant cause
   - Follow connections between categories

4. IDENTIFY root causes
   - Distinguish contributing factors from fundamental causes
   - Usually 2-3 root causes

5. PRIORITIZE by impact × feasibility

DURATION: 60-90 minutes

OUTPUT FORMAT:
```

```markdown
## Fishbone Analysis: CR-<ID>

### Problem (Effect)
[Specific, measurable problem statement]

### Cause Analysis

#### PEOPLE
- [Cause 1]
  - Why: [Deeper analysis]
- [Cause 2]

#### PROCESS
- [Cause 1]
- [Cause 2]

#### TECHNOLOGY
- [Cause 1]
- [Cause 2]

#### ENVIRONMENT
- [Cause 1]

#### METHODS
- [Cause 1]

#### MATERIALS
- [Cause 1]

### Root Causes Identified
1. **[Root Cause 1]** (Category: [X])
   - Evidence: [How you know]
   - Impact: [Severity]

2. **[Root Cause 2]** (Category: [X])
   - Evidence: [How you know]
   - Impact: [Severity]

### Cross-Category Connections
- [Category A] → [Category B]: [Relationship]

### Countermeasures (Priority Order)
| # | Action | Addresses | Effort | Impact |
|---|--------|-----------|--------|--------|
| 1 | [Fix] | [Root cause] | [Est] | High |
| 2 | [Prevention] | [Factor] | [Est] | Med |
```

## Method 4: A3 Full Analysis

**When**: Critical issues requiring comprehensive documentation.

```
PROCEDURE a3_analysis:

CREATE A3 document with all 7 sections:

═══════════════════════════════════════════════════════════════
                    A3 PROBLEM ANALYSIS
═══════════════════════════════════════════════════════════════

TITLE: [Descriptive title]
OWNER: [Responsible party]
DATE: [Date]
STATUS: [Draft | In Review | Approved]

1. BACKGROUND
   • Why this problem matters
   • Business/user impact (quantified if possible)
   • Urgency factors
   • Stakeholders affected

2. CURRENT CONDITION
   • What's happening now (facts, data, metrics)
   • Reproduction evidence
   • Timeline of when it started
   • Frequency and patterns

3. GOAL/TARGET
   • Specific success criteria
   • Measurable outcomes
   • Timeline for resolution
   • Definition of "done"

4. ROOT CAUSE ANALYSIS
   [Embed Five Whys or Fishbone analysis here]

5. COUNTERMEASURES
   IMMEDIATE (hours/days):
   • [Stop the bleeding]

   SHORT-TERM (days/weeks):
   • [Proper fix]

   LONG-TERM (weeks/months):
   • [Systemic prevention]

6. IMPLEMENTATION PLAN
   | Task | Owner | Deadline | Dependencies | Status |
   |------|-------|----------|--------------|--------|
   | [Task 1] | [Who] | [When] | [Deps] | Pending |

7. FOLLOW-UP
   • Success metrics to monitor
   • Verification method
   • Review schedule
   • Escalation criteria

═══════════════════════════════════════════════════════════════

DURATION: 2-4 hours

OUTPUT: Full A3 document in ANALYSIS.md
```

## Method 5: Gemba Walk

**When**: Unfamiliar code area, need to understand before analyzing.

```
PROCEDURE gemba_walk:

"Go and see" - Observe reality before making assumptions.

1. DEFINE SCOPE
   - Code area to explore
   - Entry points
   - Expected boundaries

2. STATE ASSUMPTIONS
   Before reading code, document what you think it does:
   - Expected flow
   - Expected behavior
   - Expected dependencies

3. OBSERVE REALITY
   Read actual code and document:
   - True entry points
   - Actual data flow
   - Real dependencies
   - Undocumented behavior

4. IDENTIFY SURPRISES
   - What differs from assumptions?
   - Hidden complexity?
   - Unexpected patterns?
   - Missing error handling?

5. DOCUMENT GAPS
   - Documentation vs. implementation
   - Expected vs. actual behavior
   - Design intent vs. reality

6. RECOMMEND
   - Update documentation?
   - Refactor needed?
   - Accept as-is?

DURATION: 30-60 minutes

OUTPUT FORMAT:
```

```markdown
## Gemba Walk: CR-<ID>

### Scope
[Code area explored]

### Assumptions (Before)
- [What I expected]
- [Expected flow]
- [Expected behavior]

### Observations (Actual Code)

**Entry Points**:
- `[file:line]`: [Description]

**Actual Flow**:
```
[Diagram or description of real flow]
```

**Dependencies**:
- [Internal deps]
- [External deps]

### Surprises
- [What differed from assumptions]
- [Hidden complexity found]
- [Undocumented behavior]

### Gaps
| Documentation Says | Code Does | Impact |
|--------------------|-----------|--------|
| [Expected] | [Actual] | [Severity] |

### Recommendations
1. [Action item]
2. [Action item]
```

## Combining Methods

For complex issues, combine methods:

```
TYPICAL COMBINATIONS:

1. Gemba Walk → Five Whys
   - First understand the code
   - Then drill into root cause

2. Five Whys → Fishbone
   - Start with single thread
   - Expand when multiple factors emerge

3. Any Method → A3
   - Use A3 as comprehensive wrapper
   - Embed other analyses in Section 4
```

## Quality Checklist

Before completing analysis:

```
□ Problem clearly stated (facts, not opinions)
□ Root cause identified (not just symptoms)
□ Evidence provided for conclusions
□ Countermeasures address root cause (not just symptom)
□ Analysis method appropriate for complexity
□ Documentation complete in ANALYSIS.md
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Wrong | Do This Instead |
|--------------|----------------|-----------------|
| "It's a typo" | Stops at symptom | Ask why typo wasn't caught |
| "Human error" | Blames person | Ask why system allowed error |
| "Just fix it" | Skips analysis | Quick check at minimum |
| "We'll never know" | Gives up | Use Gemba Walk to investigate |
| "It's always been this way" | Accepts broken | Ask why it's acceptable |

## Related Skills

- `Implementation_ChangeImplementer` - Execute fixes with Reflexion
- `systematic-debugging` - Technical debugging techniques
- `root-cause-tracing` - Call stack analysis
