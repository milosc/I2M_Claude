---
name: generating-solution-traceability-reports
description: Use when you need to generate comprehensive traceability reports assessing the quality of links between client materials, requirements, prototypes, specifications, and architecture.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-solution-traceability-reports started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-solution-traceability-reports ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-solution-traceability-reports instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Solution Traceability Report

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Solution_Traceability_Report
- **Version**: 1.1.0
- **Created**: 2024-12-16
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v1.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v1.0.0 (2024-12-16): Initial release

## Description
Generate comprehensive traceability reports assessing the quality of links between client materials, requirements, prototypes, specifications, and architecture.

## Purpose

This skill produces formal traceability assessment reports that validate end-to-end linkages from client discovery through solution architecture. It ensures every architectural decision can be traced back to a client need and every client pain point is addressed in the final solution.

---

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
- output files created (traceability reports)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "generating-solution-traceability-reports"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "generating-solution-traceability-reports" --stage solarch
```

Logging is handled automatically by the skill framework. No user action required.

---

## Trigger Conditions

Use this skill when the user requests:
- Traceability assessment or audit
- End-to-end requirement tracking
- Validation of client-to-architecture linkages
- Gap analysis across project artifacts
- "Show me how requirements connect to architecture"
- "Assess the traceability quality"

---

## Prerequisites

The project must have these artifact types available:

| Layer | Artifact Type | ID Pattern | Example |
|-------|---------------|------------|---------|
| 1 | Client Facts | CF-XXX | CF-001 |
| 2 | Pain Points | PP-XXX | PP-001 |
| 3 | Jobs to Be Done | JTBD-X.X | JTBD-1.1 |
| 4 | Epics | EPIC-XXX | EPIC-001 |
| 5 | User Stories | US-XXX | US-001 |
| 6 | Screens | S-XXX-XXX | S-ADJ-001 |
| 7 | Test Cases | TC-XXX-XXX | TC-ADJ-001 |
| 8 | Modules | MOD-XXX-XXX-XX | MOD-INV-ADJUST-01 |
| 9 | Architecture Decisions | ADR-XXX | ADR-001 |

---

## Procedure

### Phase 1: Discovery Scan

**Step 1.1**: Identify project structure
```
Glob for these patterns:
- **/Interviews/*.md - Client interview transcripts
- **/analysis/*.md - Analysis summaries
- **/jtbd*.md - Jobs to Be Done documents
- **/requirements*.md - Requirements registries
- **/TRACEABILITY*.md - Existing traceability matrices
- **/modules/*.md - Module specifications
- **/decisions/*.md OR **/ADR-*.md - Architecture decisions
```

**Step 1.2**: Build artifact inventory
Create a count of each artifact type found:
```markdown
| Artifact Type | Count | Location |
|---------------|-------|----------|
| Client Facts | N | path/to/interviews |
| Pain Points | N | path/to/analysis |
| JTBDs | N | path/to/jtbd |
| ... | ... | ... |
```

### Phase 2: Extract Client Facts

**Step 2.1**: Read all interview transcripts
For each interview file, extract:
- Direct quotes (verbatim statements)
- Implicit facts (derived insights)
- Emotional indicators (frustration, satisfaction)

**Step 2.2**: Create Client Facts table
```markdown
| ID | Quote/Fact | Source | Interview Date | Interviewee |
|----|------------|--------|----------------|-------------|
| CF-001 | "quote here" | File.md:L42 | YYYY-MM-DD | Name |
```

### Phase 3: Map Pain Points

**Step 3.1**: Extract pain points from analysis
Look for patterns:
- Explicit PP-XXX identifiers
- Sections titled "Pain Points" or "Problems"
- Negative sentiment in interviews

**Step 3.2**: Create Pain Point mapping
```markdown
| PP-ID | Description | Source Facts | Severity |
|-------|-------------|--------------|----------|
| PP-001 | Description | CF-001, CF-002 | High/Medium/Low |
```

### Phase 4: Validate JTBD Coverage

**Step 4.1**: Read JTBD document
Extract all jobs with format:
- Category (Functional/Emotional/Social)
- When-I-Want-To-So-That structure
- Importance score (1-10)
- Satisfaction score (1-10)

**Step 4.2**: Calculate Opportunity Scores
```
Opportunity = Importance + max(Importance - Satisfaction, 0)
```

**Step 4.3**: Map JTBDs to Pain Points
```markdown
| JTBD-ID | Job Statement | Linked Pain Points | Opportunity Score |
|---------|---------------|-------------------|-------------------|
| JTBD-1.1 | When... | PP-001, PP-002 | 12 |
```

### Phase 5: Requirements Traceability

**Step 5.1**: Extract requirements from registry
Look for:
- Epic definitions (EPIC-XXX)
- User stories (US-XXX)
- Functional requirements (FR-XXX)
- Non-functional requirements (NFR-XXX)

**Step 5.2**: Verify JTBD→Requirement links
```markdown
| Requirement | Type | Linked JTBDs | Coverage |
|-------------|------|--------------|----------|
| US-001 | Story | JTBD-1.1, JTBD-2.1 | Full |
| US-002 | Story | JTBD-3.1 | Partial |
```

### Phase 6: Screen & Test Coverage

**Step 6.1**: Map requirements to screens
```markdown
| Screen ID | Screen Name | Requirements Addressed | Completeness |
|-----------|-------------|----------------------|--------------|
| S-ADJ-001 | Search | US-001, US-002 | 100% |
```

**Step 6.2**: Map screens to test cases
```markdown
| Screen | Test Cases | Pass Rate | Gaps |
|--------|------------|-----------|------|
| S-ADJ-001 | TC-ADJ-001, TC-ADJ-002 | 100% | None |
```

### Phase 7: Module & Architecture Validation

**Step 7.1**: Extract module definitions
For each module file, capture:
- Module ID (MOD-XXX-XXX-XX)
- Purpose and scope
- Linked requirements
- API contracts

**Step 7.2**: Map modules to ADRs
```markdown
| Module | Related ADRs | Architectural Patterns |
|--------|--------------|----------------------|
| MOD-INV-ADJUST-01 | ADR-001, ADR-002 | Modular Monolith, CQRS |
```

**Step 7.3**: Verify ADR traceability
Each ADR should reference:
- Pain points it addresses
- JTBDs it enables
- Modules it governs

### Phase 8: Generate End-to-End Chains

**Step 8.1**: Build complete traceability chains
For each significant client fact, trace through all 9 layers:
```markdown
## Chain: [Chain Name]

CF-001 → PP-001 → JTBD-1.1 → EPIC-001 → US-001 → S-ADJ-001 → TC-ADJ-001 → MOD-INV-ADJUST-01 → ADR-001

| Layer | ID | Description |
|-------|-----|-------------|
| Client Fact | CF-001 | "Quote from interview" |
| Pain Point | PP-001 | Description of problem |
| JTBD | JTBD-1.1 | When I want to... |
| Epic | EPIC-001 | Epic description |
| Story | US-001 | As a user I want... |
| Screen | S-ADJ-001 | Screen name |
| Test | TC-ADJ-001 | Test case name |
| Module | MOD-INV-ADJUST-01 | Module name |
| Decision | ADR-001 | Decision title |
```

### Phase 9: Score and Assess

**Step 9.1**: Calculate coverage metrics
```markdown
| Metric | Score | Max | Percentage |
|--------|-------|-----|------------|
| Pain Points → JTBD | X | Y | Z% |
| JTBD → Requirements | X | Y | Z% |
| Requirements → Screens | X | Y | Z% |
| Screens → Tests | X | Y | Z% |
| Modules → ADRs | X | Y | Z% |
| **Overall Coverage** | | | **Z%** |
```

**Step 9.2**: Apply scoring rubric
```markdown
| Score Range | Rating | Description |
|-------------|--------|-------------|
| 95-100 | Excellent | Complete bidirectional traceability |
| 85-94 | Good | Minor gaps, mostly traceable |
| 70-84 | Adequate | Some gaps requiring attention |
| 50-69 | Needs Work | Significant gaps in traceability |
| <50 | Poor | Major traceability issues |
```

**Step 9.3**: Identify gaps
List any:
- Orphan artifacts (no upstream or downstream links)
- Broken chains (missing intermediate links)
- Unaddressed pain points
- Untested requirements

---

## Output Structure

### Report 1: TRACEABILITY_ASSESSMENT_REPORT.md

```markdown
# Traceability Assessment Report

## Executive Summary
- Overall Score: XX/100 (Rating)
- Complete Chains: N of M
- Coverage: X%

## Methodology
- Layers assessed
- Scoring criteria

## Layer-by-Layer Analysis
### Layer 1: Client Facts
### Layer 2: Pain Points
... (all 9 layers)

## Coverage Metrics
(Tables from Phase 9)

## Gap Analysis
### Critical Gaps
### Minor Gaps
### Recommendations

## Conclusion
```

### Report 2: TRACEABILITY_MATRIX_MASTER.md

```markdown
# Master Traceability Matrix

## Quick Reference
| Chain | Start | End | Complete |
|-------|-------|-----|----------|
| 1 | CF-001 | ADR-001 | Yes |
| 2 | CF-002 | ADR-002 | Yes |

## End-to-End Chains
(Detailed chain documentation)

## Cross-Reference Tables
(Compact mapping tables)
```

---

## Validation Gates

Before finalizing reports, verify:

| Gate | Validation | Required |
|------|------------|----------|
| G1 | All pain points have JTBD links | Yes |
| G2 | All JTBDs have requirement links | Yes |
| G3 | All requirements have screen/test links | Yes |
| G4 | All modules reference ADRs | Yes |
| G5 | At least 80% coverage overall | Recommended |

---

## Example Invocation

**User**: "Assess the traceability quality of this inventory system project"

**Claude**:
1. Scan project structure for artifacts
2. Build inventory counts
3. Extract and map all layers
4. Generate end-to-end chains
5. Calculate scores
6. Produce both reports

---

## Notes

- Always read source files before making traceability claims
- Use exact IDs from the source documents
- Flag any ID format inconsistencies
- Report both forward and backward traceability
- Include line number references where possible
- Generate both summary and detailed reports
