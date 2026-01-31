---
name: extracting-user-types
description: Use when you need to identify and profile distinct stakeholder groups and user roles from discovery materials to inform persona development.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-user-types started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-user-types ended '{"stage": "discovery"}'
---

# Extract User Types

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill extracting-user-types instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_ExtractUserTypes
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for identifying, profiling, and categorizing user types from analyzed materials. Extracts stakeholder roles, user segments, and their characteristics to inform persona creation.

**Role**: You are a User Research Specialist. Your expertise is identifying distinct user types from research materials, understanding their roles, responsibilities, and distinguishing characteristics that will inform persona development.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:extracting-user-types:started` - When skill begins
- `skill:extracting-user-types:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- After input analyzers have processed materials
- Request mentions "identify users", "user types", "stakeholders", "personas"
- Context involves understanding who uses the system
- Need to segment users before persona creation

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Analysis Files | Yes | Output from input analyzer skills |
| Known Roles | No | Pre-identified user roles |
| Focus Scope | No | Internal/External/Both |
| Output Path | Yes | Where to save user registry |

## User Type Categories

### Primary Users
- Direct, daily system users
- Core workflow participants
- Main beneficiaries of solution

### Secondary Users
- Occasional users
- Supervisors/managers viewing reports
- Approvers/reviewers

### Tertiary Users
- Admin/configuration users
- Support/help desk
- External stakeholders

## Extraction Framework

### 1. Role Identification
Scan for role mentions:
- Job titles ("recruiter", "manager", "analyst")
- Role descriptors ("the person who...", "team responsible for...")
- Organizational references ("HR team", "operations staff")
- Self-identification in interviews ("as a recruiter, I...")

### 2. Characteristic Extraction
For each user type:
- Primary responsibilities
- Daily tasks mentioned
- Tools currently used
- Pain points specific to role
- Success metrics for role
- Technical proficiency indicators

### 3. Relationship Mapping
- Reporting structure
- Collaboration patterns
- Handoff points
- Approval chains
- Information flows

### 4. Segmentation Criteria
- By function (what they do)
- By seniority (level/experience)
- By frequency (usage patterns)
- By location (geographic/departmental)
- By access (permissions needed)

## Output Format

### Primary Output: `[output_path]/01-analysis/user-type-registry.md`

```markdown
# User Type Registry

**Extraction Date**: [Date]
**Sources Analyzed**: [Count] files
**Total User Types**: [Count]
**Primary Users**: [Count] | Secondary: [Count] | Tertiary: [Count]

---

## 📊 User Type Summary

| User Type | Category | Count | Usage Frequency | Key Responsibility |
|-----------|----------|-------|-----------------|-------------------|
| [Type 1] | Primary | [N] | Daily | [Main duty] |
| [Type 2] | Primary | [N] | Daily | [Main duty] |
| [Type 3] | Secondary | [N] | Weekly | [Main duty] |

---

## 👥 Primary User Types

### UT-001: [User Type Name]
**Category**: Primary User
**Common Job Titles**: [List of titles]
**Estimated Count**: [Number or range]

**Role Overview**:
[2-3 sentence description of what this user does]

**Primary Responsibilities**:
1. [Responsibility 1]
2. [Responsibility 2]
3. [Responsibility 3]

**Daily Workflow**:
- Morning: [Tasks]
- Ongoing: [Tasks]
- End of day: [Tasks]

**Current Tools Used**:
| Tool | Purpose | Satisfaction |
|------|---------|--------------|
| [Tool] | [Purpose] | [High/Med/Low] |

**Technical Proficiency**: [Low/Medium/High]
**Decision Authority**: [What can they decide]
**Reports To**: [Role]
**Collaborates With**: [Roles]

**Pain Points Specific to Role**:
- [Pain point 1] - Severity: [P0/P1/P2]
- [Pain point 2] - Severity: [P0/P1/P2]

**Success Metrics**:
- [Metric 1]: [Current] → [Desired]
- [Metric 2]: [Current] → [Desired]

**Quote**:
> "[Representative quote]" - [Source]

**Source Evidence**: [List of files where this user type appears]

---

### UT-002: [User Type Name]
[Same structure...]

---

## 👤 Secondary User Types

### UT-010: [User Type Name]
**Category**: Secondary User
[Simplified structure - key fields only]

---

## 🔧 Tertiary User Types

### UT-020: [User Type Name]
**Category**: Tertiary User
[Simplified structure - key fields only]

---

## 🔗 User Relationships

### Organizational Hierarchy
```
[Executive/Leadership]
    └── [Manager Level]
        └── [Individual Contributor]
            └── [Support/Admin]
```

### Collaboration Matrix

| User Type | Interacts With | Interaction Type | Frequency |
|-----------|---------------|------------------|-----------|
| UT-001 | UT-002 | [Handoff/Review/etc] | [Daily/Weekly] |

### Workflow Handoffs

```
[UT-001] → [Task/Data] → [UT-002] → [Task/Data] → [UT-003]
```

---

## 📊 Access & Permission Implications

| User Type | Read Access | Write Access | Admin Access |
|-----------|-------------|--------------|--------------|
| UT-001 | [Scope] | [Scope] | [Y/N] |
| UT-002 | [Scope] | [Scope] | [Y/N] |

---

## 🎯 Persona Recommendations

Based on user type analysis, recommend creating these personas:

| Persona Priority | User Type(s) | Rationale |
|-----------------|--------------|-----------|
| 1 (Must Have) | UT-001 | [Why this persona is critical] |
| 2 (Must Have) | UT-002 | [Why this persona is critical] |
| 3 (Should Have) | UT-010 | [Why this persona is important] |

---

## 📋 Data Quality Notes

- **Well-Documented Types**: [List]
- **Needs More Research**: [List]
- **Assumed/Inferred**: [List]

---

**Registry Status**: 🟢 Complete
**Last Updated**: [Date]
```

## User Type Merging Rules

When similar roles are found:
1. If same function, different title → Merge, note title variations
2. If same title, different functions → Keep separate, clarify distinction
3. If overlapping responsibilities → Note overlap, consider single persona
4. If different seniority levels → Consider single persona with variants

## Error Handling

| Issue | Action |
|-------|--------|
| No clear user types found | Infer from workflows, flag for research |
| Conflicting role descriptions | Note both interpretations, request clarification |
| Unknown user counts | Mark as "Unknown", estimate if possible |
| Generic role names | Add context qualifiers |

## Integration Points

### Receives From
- All `Discovery_Analyze*` skills - User mentions and descriptions
- `Discovery_ExtractWorkflows` - User involvement in processes

### Feeds Into
- `Discovery_GeneratePersona` - Direct input for persona creation
- `Discovery_ExtractPainPoints` - User attribution for pain points
- `Discovery_SpecDataModel` - Permission/role requirements

---

**Skill Version**: 2.0
**Framework Compatibility**: Discovery Skills Framework v2.0
