---
name: generating-user-personas
description: Use when you need to synthesize user research and role data into comprehensive, actionable persona documents with rich narratives and day-in-life scenarios.
model: sonnet
allowed-tools: AskUserQuestion, Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-user-personas started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-user-personas ended '{"stage": "discovery"}'
---

# Generate User Personas

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-user-personas instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_GeneratePersona
- **Version**: 3.0.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-21
- **Change History**:
  - v3.0.0 (2025-12-21): Major update: Separate persona files, rich narrative format, archetypal naming, day-in-life structure
  - v2.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for synthesizing extracted user data into comprehensive persona documents. Creates detailed, actionable personas with rich narratives, day-in-life scenarios, and design implications.

**Role**: You are a Persona Development Specialist. Your expertise is transforming raw user research into vivid, actionable persona documents that product teams can use to guide design decisions and feature prioritization.

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
- output files created (persona documents)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "generating-user-personas"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "generating-user-personas" --stage discovery
```

Logging is handled automatically by the skill framework. No user action required.

---

## CRITICAL OUTPUT REQUIREMENTS

### File Structure (MANDATORY)

```
[output_path]/02-research/
└── personas/                          ← CREATE THIS SUBFOLDER
    ├── PERSONA_WAREHOUSE_OPERATOR.md  ← One file per persona
    ├── PERSONA_WAREHOUSE_SUPERVISOR.md
    ├── PERSONA_WAREHOUSE_MANAGER.md
    └── PERSONA_SYSTEM_ADMINISTRATOR.md
```

### File Naming Convention (MANDATORY)

- Pattern: `PERSONA_[ROLE_NAME].md`
- UPPERCASE with underscores
- Role name from user type (e.g., WAREHOUSE_OPERATOR, SYSTEM_ADMINISTRATOR)
- Examples:
  - `PERSONA_WAREHOUSE_OPERATOR.md`
  - `PERSONA_OPERATIONS_MANAGER.md`
  - `PERSONA_IT_ADMINISTRATOR.md`

## Trigger Conditions

- After extractors have processed analysis data
- Request mentions "create personas", "generate personas", "user personas"
- Context involves synthesizing user research into profiles
- User type registry is available

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| User Type Registry | Yes | From Discovery_ExtractUserTypes |
| Pain Point Registry | Yes | From Discovery_ExtractPainPoints |
| Quote Library | Yes | From Discovery_ExtractQuotes |
| Workflow Registry | No | From Discovery_ExtractWorkflows |
| Output Path | Yes | Where to save persona files |

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
- output file locations (persona files created)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "generating-user-personas"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "generating-user-personas" --stage discovery
```

Logging is handled automatically by the skill framework. No user action required.

---

## Persona Selection Criteria

### Primary Persona Candidates
- Highest interaction frequency with system
- Most pain points attributed
- Critical to business success
- Distinct needs from other users

### Persona Count Guidelines
- **Constraint**: None. All distinct user types with sufficient data should have a corresponding persona.
- **Prioritization**: if user_types > 5, ask user for primary focus (optional), but generate for all.

### Persona Prioritization
IF user_type_count >= 5:
  USE AskUserQuestion:
    question: "I found {N} user types. Which should be considered PRIMARY personas? (Select all that apply)"
    header: "Primary Personas"
    multiSelect: true
    options:
      - label: "{UserType1.name}"
        description: "{frequency} interactions, {pain_count} pain points"
      - label: "{UserType2.name}"
        description: "{frequency} interactions, {pain_count} pain points"
      # ... list all identified types


## Persona Components (REQUIRED)

### Rich Narrative Elements
1. **Archetypal Name** - Memorable name with nickname (e.g., Marcus "The Mover" Thompson)
2. **Background Story** - 2-3 paragraphs of personal and professional context
3. **A Day in [Name]'s Life** - Detailed hour-by-hour narrative with timestamps
4. **Goals** (Primary and Secondary) - With success criteria
5. **Pain Points** - Linked to registry with impact descriptions
6. **Frustrations** - Direct quotes in blockquote format
7. **Motivations** - What drives this person
8. **Technology Profile** - Current vs. desired tools with attitudes
9. **Scenarios** - 3+ scenarios with Current vs. Desired experience
10. **Design Implications** - Must-haves for adoption
11. **Traceability** - Links to user types, pain points, gaps

## Output Format

### Primary Output: `[output_path]/02-research/personas/PERSONA_[ROLE].md`

**One file per persona with this exact structure:**

```markdown
---
persona_id: P-[X].[Y]
version: 1.0.0
created_at: [YYYY-MM-DD]
updated_at: [YYYY-MM-DD]
generated_by: Discovery_GeneratePersona
source_user_type: UT-[X].[Y]
---

# Persona: [First Name] "[Nickname]" [Last Name]

**Archetype**: [Role/Job Title]
**Persona ID**: P-[X].[Y]
**Based on User Type**: UT-[X].[Y] ([Role Description])

---

## Profile Summary

| Attribute | Value |
|-----------|-------|
| Name | [Full Name] |
| Nickname | "[Memorable Nickname]" |
| Age | [Age] |
| Experience | [X years in relevant field] |
| Shift | [Work schedule if relevant] |
| Primary Tool | [Main device/tool they use] |
| Tech Comfort | [Low/Medium/High - with description] |

---

## Background

[2-3 paragraphs describing their professional journey, current situation, personality traits, and relationship with technology. Make them feel like a real person with hopes and frustrations.]

---

## A Day in [First Name]'s Life

**[Time 1]** - [Activity description]

**[Time 2]** - [Activity description including system interaction]

**[Time 3]** - [Activity with pain point encountered]

**[Time 4]** - [Activity showing workaround or frustration]

**[Time 5]** - [End of relevant period, summary of outcomes]

[Continue for full day or shift as relevant]

---

## Goals

### Primary Goals
1. **[Goal 1]** - [Specific measurable description]
2. **[Goal 2]** - [Specific measurable description]
3. **[Goal 3]** - [Specific measurable description]

### Secondary Goals
- [Secondary goal 1]
- [Secondary goal 2]
- [Secondary goal 3]

---

## Pain Points (Linked to Registry)

| Pain Point ID | Description | Impact on [First Name] |
|---------------|-------------|------------------------|
| PP-[X].[Y] | [Brief description] | [Specific impact statement] |
| PP-[X].[Y] | [Brief description] | [Specific impact statement] |
| PP-[X].[Y] | [Brief description] | [Specific impact statement] |

---

## Frustrations

> "[Direct quote showing frustration 1]"

> "[Direct quote showing frustration 2]"

> "[Direct quote showing frustration 3]"

---

## Motivations

- **[Motivation 1]**: [Description of what drives them]
- **[Motivation 2]**: [Description of what drives them]
- **[Motivation 3]**: [Description of what drives them]

---

## Technology Profile

| Aspect | Current | Desired |
|--------|---------|---------|
| Device | [Current device] | [Preferred device] |
| Interface | [Current UI style] | [Preferred UI style] |
| Training | [Current training approach] | [Preferred training] |
| Customization | [Current level] | [Desired level] |

### Technology Attitudes
- **Positive**: "[Quote about what they like in technology]"
- **Skeptical**: "[Quote about what concerns them]"
- **Pragmatic**: "[Quote about their practical approach]"

---

## Scenarios

### Scenario 1: [Scenario Title]
[Narrative description of the scenario]

**Current Experience**: [How they do it today - steps, time, pain]
**Desired Experience**: [How they want it to work - streamlined]

### Scenario 2: [Scenario Title]
[Narrative description of the scenario]

**Current Experience**: [How they do it today]
**Desired Experience**: [How they want it to work]

### Scenario 3: [Scenario Title]
[Narrative description of the scenario]

**Current Experience**: [How they do it today]
**Desired Experience**: [How they want it to work]

---

## Design Implications

### Mobile UI Requirements
- [Requirement 1 with rationale]
- [Requirement 2 with rationale]
- [Requirement 3 with rationale]

### Workflow Requirements
- [Requirement 1 with rationale]
- [Requirement 2 with rationale]
- [Requirement 3 with rationale]

### Training Requirements
- [Requirement 1 with rationale]
- [Requirement 2 with rationale]
- [Requirement 3 with rationale]

---

## Quotes from Interviews

*From [Interview Source]:*

> "[Relevant quote 1]"

> "[Relevant quote 2]"

> "[Relevant quote 3]"

---

## Traceability

| Link Type | IDs |
|-----------|-----|
| User Type | UT-[X].[Y] |
| Pain Points | PP-[list], PP-[list], PP-[list] |
| Client Facts | CF-[list] |
| Gaps | GAP-[list] |

---

**Document Status**: Complete
**Next**: Generate JTBD for this persona
```

## Quality Checklist

Before completing each persona:
- [ ] Has memorable nickname in title
- [ ] Has detailed day-in-life narrative with timestamps
- [ ] Has at least 3 supporting quotes in Frustrations
- [ ] Has at least 3 scenarios with current/desired comparison
- [ ] Pain points link to registry IDs
- [ ] Technology profile shows current vs. desired
- [ ] Design implications are specific and actionable
- [ ] Traceability section links to all related artifacts

## Error Handling

| Issue | Action |
|-------|--------|
| Insufficient data for persona | Flag gaps, create partial persona |
| Overlapping personas | Consider merging or clearly distinguish |
| No quotes for role | Create persona, mark quotes as needed |
| Conflicting information | Note conflict, use most recent/reliable |

## Integration Points

### Receives From
- `Discovery_ExtractUserTypes` - Role definitions
- `Discovery_ExtractPainPoints` - Pain point details
- `Discovery_ExtractQuotes` - Supporting quotes
- `Discovery_ExtractWorkflows` - Daily workflows

### Feeds Into
- `Discovery_GenerateJTBD` - JTBD mapped to personas
- `Discovery_GenerateVision` - Target user summary
- `Discovery_SpecScreens` - Role-based access

---

**Skill Version**: 3.0.0
**Framework Compatibility**: Discovery Skills Framework v5.0
