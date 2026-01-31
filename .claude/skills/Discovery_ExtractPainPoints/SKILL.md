---
name: extracting-pain-points
description: Use when you need to extract and categorize user pain points from discovery materials to drive product strategy.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-pain-points started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-pain-points ended '{"stage": "discovery"}'
---

# Extract Pain Points

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill extracting-pain-points instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_ExtractPainPoints
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Extract, categorize, and prioritize pain points from analyzed materials (transcripts, documents, research). Focus on identifying P0 "blockers" that define the core product value proposition.

**Role**: You are a Pain Point Analysis Specialist. Your expertise is identifying, categorizing, and prioritizing user problems from diverse research inputs. You synthesize scattered complaints into actionable, trackable pain points with clear severity and business impact.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:extracting-pain-points:started` - When skill begins
- `skill:extracting-pain-points:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- After input analyzers have processed materials
- Request mentions "extract pain points", "identify problems", "find frustrations"
- Context involves consolidating issues from multiple sources
- Need to prioritize problems for roadmap planning

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Analysis Files | Yes | Output from input analyzer skills |
| Priority Framework | No | Custom P0/P1/P2 definitions |
| Focus User Types | No | Specific roles to prioritize |
| Output Path | Yes | Where to save pain point registry |

## Pain Point Severity Framework

### P0 - Critical (Blocker)
**Definition**: Prevents users from completing essential tasks
**Indicators**:
- "Can't", "Unable to", "Blocks", "Stops"
- Workaround requires significant time/effort
- Mentioned by multiple users/sources
- Has quantified business impact
- Forces manual intervention

### P1 - High Priority (Major Impact)
**Definition**: Significantly degrades user experience or efficiency
**Indicators**:
- "Frustrating", "Takes too long", "Difficult"
- Workaround exists but is inconvenient
- Mentioned repeatedly by same user
- Affects daily workflows
- Causes errors or rework

### P2 - Medium Priority (Minor Impact)
**Definition**: Causes inconvenience but doesn't block work
**Indicators**:
- "Would be nice if", "Annoying", "Wish"
- Easy workaround available
- Mentioned once or in passing
- Affects occasional tasks
- Cosmetic or preference-based

## Extraction Framework

### 1. Source Scanning
For each analysis file:
- Scan pain point sections
- Extract quotes with negative sentiment
- Identify workflow bottlenecks
- Note data quality issues mentioned
- Find time/cost impacts

### 2. Pain Point Normalization
- Standardize language (action-oriented)
- Remove duplicates (merge similar)
- Attribute to source materials
- Connect to user types
- Add supporting quotes

### 3. Impact Quantification
- Time lost per occurrence
- Frequency of occurrence
- Number of users affected
- Business cost if available
- Opportunity cost if not fixed

### 4. Categorization
- Assign to feature areas
- Map to user workflows
- Tag with themes
- Link to related pain points
- Identify root causes

## Output Format

### Primary Output: `[output_path]/01-analysis/pain-point-registry.md`

```markdown
# Pain Point Registry

**Extraction Date**: [Date]
**Sources Analyzed**: [Count] files
**Total Pain Points**: [Count]
**By Severity**: P0: [N] | P1: [N] | P2: [N]

---

## 📊 Executive Summary

### Critical Issues (P0)
[Count] pain points block essential user workflows:
1. [Top P0 issue - one line]
2. [Second P0 issue - one line]
3. [Third P0 issue - one line]

### Highest Impact Areas
| Area | Pain Point Count | Severity Distribution |
|------|-----------------|----------------------|
| [Area 1] | [N] | P0: [N], P1: [N], P2: [N] |
| [Area 2] | [N] | P0: [N], P1: [N], P2: [N] |

### Most Affected Users
| User Type | Pain Point Count | Critical Issues |
|-----------|-----------------|-----------------|
| [User 1] | [N] | [N] |
| [User 2] | [N] | [N] |

---

## 🔴 CRITICAL Pain Points (P0)

### PP-001: [Pain Point Title]
**Severity**: P0 - Critical
**Category**: [Feature Area]
**Affected Users**: [User types]

**Problem Statement**:
[Clear, action-oriented description of the problem]

**Impact**:
- **Frequency**: [How often it occurs]
- **Time Lost**: [Per occurrence]
- **Users Affected**: [Count/percentage]
- **Business Cost**: [If quantified]

**Current Workaround**:
[How users currently deal with this]

**Supporting Evidence**:
> "[Quote 1]" - [Source, Role]
> "[Quote 2]" - [Source, Role]

**Source Files**:
- [File 1]: [Specific reference]
- [File 2]: [Specific reference]

**Related Pain Points**: PP-XXX, PP-YYY

---

### PP-002: [Pain Point Title]
[Same structure...]

---

## 🟡 HIGH Priority Pain Points (P1)

### PP-010: [Pain Point Title]
[Same structure but with P1 indicators...]

---

## 🟢 MEDIUM Priority Pain Points (P2)

### PP-030: [Pain Point Title]
[Same structure but with P2 indicators...]

---

## 📈 Pain Point Analysis

### By Feature Area

| Feature Area | P0 | P1 | P2 | Total | Priority Score |
|--------------|----|----|----|----|----------------|
| [Area 1] | [N] | [N] | [N] | [N] | [Weighted] |

### By User Type

| User Type | P0 | P1 | P2 | Total | Key Concern |
|-----------|----|----|----|----|-------------|
| [User 1] | [N] | [N] | [N] | [N] | [Main issue] |

### Root Cause Clusters

| Root Cause | Pain Points | Feature Areas |
|------------|-------------|---------------|
| [Cause 1] | PP-001, PP-015 | [Areas] |
| [Cause 2] | PP-003, PP-022 | [Areas] |

---

## 🔗 Traceability Matrix

| Pain Point ID | Sources | Users | Feature Area | JTBD Link |
|---------------|---------|-------|--------------|-----------|
| PP-001 | [Sources] | [Users] | [Area] | [JTBD-X.X] |

---

## 📋 Next Steps

### Immediate Actions (P0)
1. [ ] Address PP-001: [Action]
2. [ ] Address PP-002: [Action]

### Short-term (P1)
1. [ ] Address PP-010: [Action]

### Medium-term (P2)
1. [ ] Address PP-030: [Action]

---

**Registry Status**: 🟢 Complete
**Last Updated**: [Date]
```

## Deduplication Rules

When merging similar pain points:
1. Keep the most specific description
2. Combine all supporting quotes
3. Use highest severity across duplicates
4. Merge affected user types
5. Link all source references
6. Note the merge in registry

## Quality Checks

Before finalizing:
- [ ] Every P0 has quantified impact
- [ ] Every pain point has at least one quote
- [ ] Every pain point links to source file
- [ ] Duplicates identified and merged
- [ ] User types assigned to all pain points
- [ ] Feature areas assigned to all pain points

## Error Handling

| Issue | Action |
|-------|--------|
| No pain points found in source | Note limitation, check source quality |
| Conflicting severity indicators | Use highest severity, note conflict |
| Missing user attribution | Mark as "All Users" or "Unknown" |
| Vague pain point descriptions | Request clarification or rephrase |

## Integration Points

### Receives From
- All `Discovery_Analyze*` skills - Raw pain point mentions
- `Discovery_ExtractQuotes` - Supporting quotes

### Feeds Into
- `Discovery_GeneratePersona` - Pain points per persona
- `Discovery_GenerateJTBD` - Pain points drive jobs
- `Discovery_GenerateVision` - Top pain points in vision
- `Discovery_GenerateRoadmap` - Priority informs sequencing

---

**Skill Version**: 2.0
**Framework Compatibility**: Discovery Skills Framework v2.0
