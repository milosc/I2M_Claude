---
name: extracting-user-quotes
description: Use when you need to extract and categorize impactful verbatim statements from user research to support personas, vision, and strategic claims.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-user-quotes started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill extracting-user-quotes ended '{"stage": "discovery"}'
---

# Extract Quotes

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill extracting-user-quotes instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_ExtractQuotes
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for extracting, categorizing, and organizing verbatim quotes from analyzed materials. Creates a searchable quote library with attribution, context, and thematic categorization for use in personas, documentation, and stakeholder presentations.

**Role**: You are a Quote Curation Specialist. Your expertise is identifying impactful verbatim statements from user research, preserving their authenticity while organizing them for effective use in product documentation and presentations.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:extracting-user-quotes:started` - When skill begins
- `skill:extracting-user-quotes:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- After input analyzers have processed materials
- Request mentions "extract quotes", "user quotes", "verbatim evidence"
- Context involves building evidence for recommendations
- Need supporting quotes for personas or documentation

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Analysis Files | Yes | Output from input analyzer skills |
| Quote Themes | No | Specific themes to categorize by |
| Min Quote Length | No | Minimum words for inclusion |
| Output Path | Yes | Where to save quote library |

## Quote Quality Criteria

### High-Value Quotes
- Express clear opinion or experience
- Include specific details or quantification
- Represent a common sentiment
- Are memorable and impactful
- Can stand alone with context

### Quote Types

| Type | Characteristics | Use Case |
|------|-----------------|----------|
| Pain Quote | Expresses frustration/problem | Pain point evidence |
| Desire Quote | Expresses want/need | JTBD support |
| Workflow Quote | Describes process | Process documentation |
| Impact Quote | Quantifies effect | ROI/Business case |
| Emotion Quote | Expresses feeling | Persona development |
| Comparison Quote | Compares options | Competitive analysis |

## Extraction Framework

### 1. Quote Identification
Scan for quotable content:
- Text in quotation marks
- Statements with "I" or "We" perspective
- Strongly worded opinions
- Specific examples or stories
- Quantified statements

### 2. Quote Cleaning
- Remove filler words (um, uh) unless meaningful
- Preserve meaning and tone
- Add [context] brackets where needed
- Mark [emphasis] if tone indicates
- Note [redacted] for sensitive content

### 3. Attribution
- Speaker role/title
- Source document
- Timestamp (if audio/video)
- Interview context
- Confidence level

### 4. Categorization
- Primary theme
- Related themes
- Quote type
- Sentiment (positive/negative/neutral)
- Impact level

## Output Format

### Primary Output: `[output_path]/01-analysis/quote-library.md`

```markdown
# Quote Library

**Extraction Date**: [Date]
**Sources Analyzed**: [Count] files
**Total Quotes**: [Count]
**By Sentiment**: Positive: [N] | Neutral: [N] | Negative: [N]

---

## 📊 Quote Summary

### By Theme
| Theme | Count | Key Quote |
|-------|-------|-----------|
| [Theme 1] | [N] | "[Preview...]" |
| [Theme 2] | [N] | "[Preview...]" |

### By Speaker Role
| Role | Count | Primary Themes |
|------|-------|----------------|
| [Role 1] | [N] | [Themes] |
| [Role 2] | [N] | [Themes] |

---

## 🔴 Pain Point Quotes

### Theme: [Theme Name]

#### Q-001
> "[Full verbatim quote]"

**Speaker**: [Role/Title]
**Source**: [File], [Timestamp/Page]
**Context**: [Brief context of when/why this was said]
**Sentiment**: Negative
**Impact Level**: High
**Related Pain Points**: PP-XXX, PP-YYY
**Tags**: `#[tag1]` `#[tag2]`

---

#### Q-002
[Same structure...]

---

## 💡 Desire/Need Quotes

### Theme: [Theme Name]

#### Q-020
> "[Full verbatim quote]"

**Speaker**: [Role/Title]
**Source**: [File], [Timestamp/Page]
**Context**: [Brief context]
**Sentiment**: Positive/Hopeful
**Related JTBDs**: JTBD-X.X
**Tags**: `#[tag1]` `#[tag2]`

---

## 🔄 Workflow/Process Quotes

### Theme: [Theme Name]

#### Q-040
> "[Full verbatim quote describing process]"

**Speaker**: [Role/Title]
**Source**: [File]
**Context**: [Description of workflow context]
**Related Workflows**: WF-XXX
**Tags**: `#[tag1]`

---

## 📈 Impact/Quantified Quotes

#### Q-060
> "[Quote with specific numbers or measurements]"

**Speaker**: [Role/Title]
**Source**: [File]
**Metric Mentioned**: [What was quantified]
**Value**: [The number/measurement]
**Tags**: `#metrics` `#[area]`

---

## 😊 Positive Experience Quotes

#### Q-080
> "[Quote expressing satisfaction or success]"

**Speaker**: [Role/Title]
**Source**: [File]
**What Works**: [Feature/aspect praised]
**Tags**: `#success` `#[feature]`

---

## 🏷️ Quote Index by Tag

### #onboarding
- Q-001: "[Preview...]" - [Role]
- Q-023: "[Preview...]" - [Role]

### #reporting
- Q-005: "[Preview...]" - [Role]
- Q-041: "[Preview...]" - [Role]

[Continue for all tags...]

---

## 👥 Quotes by Persona

### [Persona Name]
Best quotes representing this persona's perspective:

1. **On Pain Points**:
   > "[Quote]" (Q-XXX)

2. **On Desires**:
   > "[Quote]" (Q-YYY)

3. **On Daily Work**:
   > "[Quote]" (Q-ZZZ)

---

## ⭐ Featured Quotes

Highest-impact quotes for presentations and executive summaries:

### The Problem
> "[Most impactful problem quote]"
> — [Role], [Source]

### The Opportunity
> "[Most compelling opportunity quote]"
> — [Role], [Source]

### The Vision
> "[Quote that captures desired future]"
> — [Role], [Source]

---

## 📋 Quote Usage Guidelines

### For Personas
Use quotes that:
- Represent the persona's perspective
- Express goals, frustrations, workflows
- Are 1-2 sentences max

### For Presentations
Use quotes that:
- Are impactful and memorable
- Can stand alone without context
- Have clear attribution

### For Documentation
Use quotes that:
- Provide evidence for claims
- Include specific details
- Support requirements traceability

---

**Library Status**: 🟢 Complete
**Last Updated**: [Date]
```

## Quote Deduplication

When similar quotes found:
1. Keep most complete version
2. Note variations exist
3. Preserve all attributions
4. Link related quotes

## Privacy Considerations

- Remove personally identifiable information
- Use role/title instead of names (unless consent)
- Redact sensitive business information
- Note when quotes are anonymized

## Error Handling

| Issue | Action |
|-------|--------|
| Unclear attribution | Mark as "Unknown Role" |
| Partial quote | Include with [...] for missing parts |
| Sensitive content | Redact or exclude, note omission |
| Non-English quotes | Include with translation if possible |

## Integration Points

### Receives From
- All `Discovery_Analyze*` skills - Raw quotes
- `Discovery_ExtractPainPoints` - Pain context
- `Discovery_ExtractUserTypes` - Speaker roles

### Feeds Into
- `Discovery_GeneratePersona` - Representative quotes
- `Discovery_GenerateVision` - Supporting evidence
- `Discovery_DocSummary` - Featured quotes

---

**Skill Version**: 2.0
**Framework Compatibility**: Discovery Skills Framework v2.0
