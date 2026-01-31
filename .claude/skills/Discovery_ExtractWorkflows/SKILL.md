---
name: extracting-workflows
description: Use when you need to extract, map, and document business processes, user journeys, and data flows from analyzed materials to identify improvements.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-workflows started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-workflows ended '{"stage": "discovery"}'
---

# Extract Workflows

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill extracting-workflows instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_ExtractWorkflows
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for extracting, mapping, and documenting workflows from analyzed materials. Identifies current-state processes, desired-state improvements, and workflow pain points that inform product requirements.

**Role**: You are a Process Analysis Specialist. Your expertise is identifying business processes from research materials, mapping current and desired workflows, and identifying inefficiencies and improvement opportunities.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:extracting-workflows:started` - When skill begins
- `skill:extracting-workflows:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- After input analyzers have processed materials
- Request mentions "workflows", "processes", "current state", "how they work"
- Context involves understanding operational procedures
- Need to map user journeys or business processes

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Analysis Files | Yes | Output from input analyzer skills |
| Process Scope | No | Specific processes to focus on |
| Workflow Type | No | User journey, business process, data flow |
| Output Path | Yes | Where to save workflow maps |

## Workflow Categories

### Business Processes
- Operational procedures
- Approval chains
- Service delivery
- Exception handling

### User Journeys
- End-to-end experiences
- Task completion flows
- Decision paths
- Error recovery

### Data Flows
- Information movement
- System integrations
- Data transformations
- Storage and retrieval

## Extraction Framework

### 1. Process Identification
Scan for process indicators:
- Sequential language ("first", "then", "after", "finally")
- Role transitions ("handed off to", "sent to", "reviewed by")
- Status changes ("from X to Y", "changes to", "becomes")
- Time references ("daily", "weekly", "when X happens")

### 2. Step Extraction
For each workflow:
- Entry trigger (what starts it)
- Sequential steps
- Decision points
- Parallel activities
- Exit conditions
- Exception paths

### 3. Pain Point Mapping
Identify workflow problems:
- Bottlenecks (long wait times)
- Manual steps (should be automated)
- Rework loops (errors causing repeats)
- Handoff failures (information loss)
- Workarounds (unofficial paths)

### 4. Improvement Opportunities
- Automation candidates
- Step elimination
- Parallel execution
- Self-service options
- Integration points

## Output Format

### Primary Output: `[output_path]/01-analysis/workflow-registry.md`

```markdown
# Workflow Registry

**Extraction Date**: [Date]
**Sources Analyzed**: [Count] files
**Total Workflows**: [Count]
**Business Processes**: [N] | User Journeys: [N] | Data Flows: [N]

---

## 📊 Workflow Summary

| Workflow ID | Name | Type | Steps | Pain Points | Improvement Potential |
|-------------|------|------|-------|-------------|----------------------|
| WF-001 | [Name] | [Type] | [N] | [N] | [High/Med/Low] |

---

## 🔄 Business Processes

### WF-001: [Workflow Name]
**Type**: Business Process
**Frequency**: [Daily/Weekly/On-demand]
**Primary Users**: [User types involved]
**Systems Involved**: [Current tools/systems]

**Trigger**: [What starts this workflow]
**Outcome**: [What completing this achieves]

**Current State Flow**:
```
[Step 1: Actor - Action]
    ↓
[Step 2: Actor - Action]
    ↓ (if condition)
[Step 3a: Actor - Action]  OR  [Step 3b: Actor - Action]
    ↓
[Step 4: Actor - Action]
    ↓
[End State]
```

**Detailed Steps**:

| # | Actor | Action | Input | Output | Time | Tools |
|---|-------|--------|-------|--------|------|-------|
| 1 | [Role] | [Action] | [Input] | [Output] | [Duration] | [Tool] |
| 2 | [Role] | [Action] | [Input] | [Output] | [Duration] | [Tool] |

**Decision Points**:
- At Step [N]: If [condition] → [Path A], else → [Path B]

**Pain Points in This Workflow**:
| Step | Pain Point | Severity | Impact |
|------|------------|----------|--------|
| [N] | [Pain point] | [P0/P1/P2] | [Time/Error/Cost] |

**Improvement Opportunities**:
1. **[Opportunity 1]**: [Description]
   - Current: [Current state]
   - Proposed: [Improved state]
   - Impact: [Expected benefit]

**Source Evidence**: [Files describing this workflow]

---

### WF-002: [Workflow Name]
[Same structure...]

---

## 🚶 User Journeys

### UJ-001: [Journey Name]
**Journey Goal**: [What user is trying to accomplish]
**Primary Persona**: [Persona reference]
**Touchpoints**: [N] steps
**Duration**: [Total time]

**Journey Map**:

| Stage | User Action | System Response | Emotion | Pain Point |
|-------|-------------|-----------------|---------|------------|
| [Stage 1] | [Action] | [Response] | [😊/😐/😢] | [If any] |
| [Stage 2] | [Action] | [Response] | [😊/😐/😢] | [If any] |

**Moments of Truth**:
1. [Critical moment 1] - [Why it matters]
2. [Critical moment 2] - [Why it matters]

---

## 📊 Data Flows

### DF-001: [Data Flow Name]
**Data Type**: [What data moves]
**Source**: [Origin system/process]
**Destination**: [Target system/process]
**Frequency**: [How often]
**Volume**: [Amount of data]

**Flow Diagram**:
```
[Source] → [Transform/Process] → [Destination]
            ↓
         [Side Effect/Log]
```

---

## 📈 Workflow Analysis

### Time Analysis
| Workflow | Total Time | Value-Add Time | Wait Time | Efficiency |
|----------|------------|----------------|-----------|------------|
| WF-001 | [Total] | [Value] | [Wait] | [%] |

### Automation Candidates
| Workflow | Step | Current | Automation Type | Effort |
|----------|------|---------|-----------------|--------|
| WF-001 | [N] | Manual | [Full/Partial/Assist] | [H/M/L] |

### Integration Points
| Workflow | External System | Integration Type | Data Exchanged |
|----------|-----------------|------------------|----------------|
| WF-001 | [System] | [API/File/Manual] | [Data types] |

---

## 🔗 Workflow Relationships

### Dependencies
```
[WF-001] triggers [WF-002]
[WF-002] feeds into [WF-003]
[WF-001] and [WF-004] share [Resource/Data]
```

### Common Subprocesses
| Subprocess | Used In |
|------------|---------|
| [Approval Process] | WF-001, WF-003, WF-005 |
| [Notification Process] | WF-002, WF-004 |

---

## 📋 Improvement Roadmap

### Quick Wins (Low Effort, High Impact)
1. [Improvement 1] in [WF-XXX]
2. [Improvement 2] in [WF-YYY]

### Major Improvements (High Effort, High Impact)
1. [Improvement 1] affecting [WF-XXX, WF-YYY]

---

**Registry Status**: 🟢 Complete
**Last Updated**: [Date]
```

## Error Handling

| Issue | Action |
|-------|--------|
| Incomplete workflow description | Map known steps, flag gaps |
| Conflicting workflow versions | Note both, indicate current vs desired |
| No workflows found | Infer from user activities, flag for research |
| Complex parallel processes | Simplify representation, note complexity |

## Integration Points

### Receives From
- All `Discovery_Analyze*` skills - Process descriptions
- `Discovery_ExtractUserTypes` - Actor identification

### Feeds Into
- `Discovery_GenerateJTBD` - Workflows inform jobs
- `Discovery_SpecNavigation` - User flows
- `Discovery_SpecScreens` - Workflow-driven screens

---

**Skill Version**: 2.0
**Framework Compatibility**: Discovery Skills Framework v2.0
