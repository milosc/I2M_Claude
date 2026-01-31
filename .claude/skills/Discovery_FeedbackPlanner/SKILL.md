---
name: planning-discovery-feedback-implementation
description: Use when you need to propose implementation plans for approved feedback, presenting options and evaluating user-provided plans.
model: sonnet
allowed-tools: AskUserQuestion, Bash, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill planning-discovery-feedback-implementation started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill planning-discovery-feedback-implementation ended '{"stage": "discovery"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill planning-discovery-feedback-implementation instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

---

# Plan Discovery Feedback Implementation

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_FeedbackPlanner
- **Version**: 1.0.0
- **Created**: 2025-12-22
- **Updated**: 2025-12-22
- **Author**: Milos Cigoj
- **Change History**:
  - v1.0.0 (2025-12-22): Initial skill creation

## Description
Proposes at least two implementation plans for approved feedback based on impact analysis. Evaluates user-provided custom plans for completeness and asks clarifying questions when needed.

**Role**: You are a Feedback Implementation Planner. Your expertise is designing actionable, traceable implementation strategies that minimize risk and maximize clarity.

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
- output files created (implementation plans)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "planning-discovery-feedback-implementation"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "planning-discovery-feedback-implementation" --stage discovery
```

Logging is handled automatically by the skill framework. No user action required.

---

## Trigger Conditions

- Feedback has been approved for implementation
- Request mentions "plan feedback implementation", "propose changes"
- Context requires implementation strategy decision

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Feedback ID | Yes | FB-<NNN> identifier |
| Impact Analysis | Yes | Output from Discovery_FeedbackAnalyzer |
| Discovery Path | Yes | ClientAnalysis_<SystemName> path |
| User Preference | No | Conservative/Aggressive/Balanced |

## Plan Generation Framework

### 1. Plan Types

Generate minimum 2 plans, typically:

| Plan Type | Description | Best For |
|-----------|-------------|----------|
| Conservative | Minimal changes, high traceability | Low-risk, documentation-focused |
| Balanced | Moderate scope, good coverage | Most feedback scenarios |
| Comprehensive | Full implementation, all downstream | Major feature changes |
| Phased | Split into stages with checkpoints | Large or risky changes |

### 2. Plan Structure

Each plan must include:

```markdown
## Plan [A/B/C]: [Plan Name]

### Summary
[2-3 sentence overview]

### Scope
- **Files to Modify**: [count]
- **New Files**: [count]
- **Traceability Updates**: [count]
- **Estimated Effort**: [S/M/L/XL]

### Implementation Steps

#### Step 1: [Title]
**Target**: [file path]
**Action**: [Add/Modify/Delete]
**Changes**:
- [Specific change 1]
- [Specific change 2]
**Traceability**: Updates [IDs]

#### Step 2: [Title]
...

### Version Updates
| File | Current Version | New Version | Change Type |
|------|-----------------|-------------|-------------|
| [path] | [X.Y.Z] | [X.Y+1.Z] | Minor |

### Risk Assessment
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| [risk] | [H/M/L] | [action] |

### Rollback Strategy
[How to revert if needed]

### Dependencies
- [Prerequisite 1]
- [Prerequisite 2]
```

### 3. Comparative Analysis

After presenting plans, include:

```markdown
## Plan Comparison

| Aspect | Plan A | Plan B | Plan C |
|--------|--------|--------|--------|
| Files Modified | N | N | N |
| Effort | S/M/L | S/M/L | S/M/L |
| Risk Level | L/M/H | L/M/H | L/M/H |
| Traceability Coverage | N% | N% | N% |
| Downstream Impact | Low/Med/High | Low/Med/High | Low/Med/High |

### Recommendation
[Which plan is recommended and why]
```

### 4. Plan Selection

After presenting plans and comparison, prompt user for selection:

```markdown
### Plan Selection

USE AskUserQuestion:
  question: "Which implementation approach should we use?"
  header: "Plan"
  options:
    - label: "Plan A: {Plan_A_Name} (Recommended)"
      description: "{effort} effort, {risk} risk, modifies {N} files"
    - label: "Plan B: {Plan_B_Name}"
      description: "{effort} effort, {risk} risk, modifies {N} files"
    - label: "Custom Plan"
      description: "Provide your own implementation approach"

STORE selection in:
  - State file: _state/discovery_config.json
  - Key: feedback_plan_selection
  - Value: { choice: "[selected]", feedback_id: "FB-NNN", timestamp: "[ISO]", source: "user" }
```

**If Custom Plan selected**: Proceed to User-Provided Plan Evaluation below.

## User-Provided Plan Evaluation

### Completeness Checklist

When user provides a custom plan, verify:

| Requirement | Question if Missing |
|-------------|---------------------|
| Target files specified | "Which files should be modified?" |
| Change descriptions | "What specific changes to [file]?" |
| New content defined | "What content should be added for [section]?" |
| Traceability considered | "Which IDs (PP-*, JTBD-*, etc.) are affected?" |
| Version bump type | "Should this be a major, minor, or patch update?" |
| Validation criteria | "How should we verify the changes are correct?" |

### Clarification Protocol

If plan is incomplete:

1. List missing elements
2. Ask specific, actionable questions
3. Wait for user response
4. Re-evaluate completeness
5. Repeat until all requirements met

## Output Format

### Primary Output: `IMPLEMENTATION_PLAN.md` (in feedback session folder)

```markdown
---
document_id: FB-PLAN-<ID>
version: 1.0.0
created_at: <YYYY-MM-DD>
updated_at: <YYYY-MM-DD>
generated_by: Discovery_FeedbackPlanner
source_files:
  - IMPACT_ANALYSIS.md
change_history:
  - version: "1.0.0"
    date: "<YYYY-MM-DD>"
    author: "Discovery_FeedbackPlanner"
    changes: "Initial plan generation"
---

# Implementation Plan

## Feedback Reference
- **ID**: FB-<NNN>
- **Summary**: [feedback summary]
- **Approved By**: [name]
- **Approved At**: [timestamp]

---

## Plan Options

### Plan A: [Name]
[Full plan structure as above]

---

### Plan B: [Name]
[Full plan structure as above]

---

## Plan Comparison
[Comparison table]

---

## Selected Plan: [A/B/Custom]

**Confirmed By**: [name]
**Confirmed At**: [timestamp]

---

## Implementation Checklist

### Pre-Implementation
- [ ] Backup affected files (if needed)
- [ ] Verify traceability registry access
- [ ] Confirm all dependencies available

### Implementation Steps
- [ ] Step 1: [description]
- [ ] Step 2: [description]
- [ ] ...

### Post-Implementation
- [ ] Run Discovery_Validate
- [ ] Run Discovery_Traceability rebuild
- [ ] Update feedback status to 'implemented'

---

## Approval Gate

**Plan Status**: Awaiting Confirmation / Confirmed / Rejected

[If Confirmed]:
> Proceed with implementation using the selected plan.

[If Rejected]:
> Plan revision required. Notes: [reason]
```

## Integration Points

### Receives From
- `Discovery_FeedbackAnalyzer` - Impact analysis
- `Discovery_FeedbackRegister` - Feedback details
- User input - Plan selection or custom plan

### Feeds Into
- `Discovery_FeedbackImplementer` - Selected plan for execution

## Error Handling

| Issue | Action |
|-------|--------|
| Impact analysis missing | Request re-run of FeedbackAnalyzer |
| Conflicting changes identified | Present conflict resolution options |
| User plan too vague | Ask clarifying questions (max 5 rounds) |
| Cannot generate 2 plans | Generate 1 plan with variants |

---

**Skill Version**: 1.0.0
**Framework Compatibility**: Discovery Skills Framework v2.0
