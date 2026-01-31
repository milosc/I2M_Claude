---
name: analyzing-solarch-feedback
description: Use when you need to analyze feedback impact across Solution Architecture artifacts, identifying affected ADRs, components, diagrams, and traceability chains.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-solarch-feedback started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-solarch-feedback ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-solarch-feedback instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

---

# SolArch_FeedbackAnalyzer

Impact analysis for Solution Architecture feedback.

## Purpose

Analyzes feedback impact across Solution Architecture outputs, identifying affected ADRs, components, diagrams, and traceability chains to inform implementation planning.

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
- output files created (feedback analysis reports)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "analyzing-solarch-feedback"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "analyzing-solarch-feedback" --stage solarch
```

Logging is handled automatically by the skill framework. No user action required.

---

## When to Use

- After feedback is registered
- To determine scope of changes needed
- To identify cascade effects across architecture
- To assess traceability chain impacts

## Input Requirements

```json
{
  "feedback_id": "SF-001",
  "system_name": "InventorySystem",
  "feedback_text": "ADR-001 needs stronger justification...",
  "category": "ADR"
}
```

## Output Files

### Impact Analysis Report

Location: `SolArch_<SystemName>/feedback-sessions/<session>/impact_analysis.md`

```markdown
---
feedback_id: SF-001
analysis_timestamp: 2025-12-22T10:15:00Z
category: ADR
type: Enhancement
---

# Impact Analysis Report

## Summary

| Metric | Count |
|--------|-------|
| Direct Impacts | 1 |
| Cascade Impacts | 2 |
| Traceability Chains | 3 |
| Risk Level | Medium |

## Feedback Analysis

### Original Feedback
"ADR-001 needs stronger justification for choosing monolith over microservices"

### Classification
- **Category**: ADR (Architecture Decision Record)
- **Type**: Enhancement
- **Scope**: Single ADR with cascading documentation

## Direct Impacts

### ADR-001-architecture-style.md

**Path**: `09-decisions/ADR-001-architecture-style.md`

**Sections Affected**:
| Section | Change Type | Description |
|---------|-------------|-------------|
| Context | Enhance | Add scaling analysis |
| Decision | Enhance | Add future evolution path |
| Consequences | Enhance | Expand negative consequences |

**Current Content** (relevant excerpt):
```
## Decision
We will use a modular monolith architecture...
```

**Suggested Enhancement**:
- Add detailed comparison with microservices
- Include scaling thresholds for evolution
- Document trade-off analysis

## Cascade Impacts

### 1. solution-strategy.md

**Path**: `04-solution-strategy/solution-strategy.md`

**Reason**: References ADR-001 as foundation for architecture approach

**Sections to Review**:
- Architecture Approach section
- Quality Attribute section

**Impact Level**: Low (alignment check only)

### 2. traceability/adr_registry.json

**Path**: `traceability/adr_registry.json` (ROOT level - single source of truth)

**Reason**: Contains ADR-001 metadata

**Changes Required**:
- Update version field
- Update modified_at timestamp

## Traceability Chain Impacts

### Chain 1: PP-1.1 → ADR-001 → COMP-CORE

```
PP-1.1 (System Reliability)
    ↓ addresses
ADR-001 (Architecture Style)
    ↓ enables
COMP-CORE (Core Module)
```

**Status**: Affected (ADR modification)
**Action**: Verify chain integrity after changes

### Chain 2: PP-2.1 → ADR-001 → COMP-CORE

```
PP-2.1 (Performance Issues)
    ↓ addresses
ADR-001 (Architecture Style)
    ↓ enables
COMP-CORE (Core Module)
```

**Status**: Affected (ADR modification)
**Action**: Verify chain integrity after changes

### Chain 3: REQ-001 → ADR-001

```
REQ-001 (Scalability Requirement)
    ↓ satisfied_by
ADR-001 (Architecture Style)
```

**Status**: Affected (ADR modification)
**Action**: Ensure enhancement addresses REQ-001

## Risk Assessment

### Risk Level: Medium

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Inconsistency with strategy | Low | Medium | Review solution-strategy.md |
| Traceability break | Low | High | Validate chains after changes |
| Version conflict | Low | Low | Increment version properly |

### Blockers

None identified.

### Warnings

- Ensure ADR versioning is updated
- May need alignment in solution-strategy.md

## Recommendations

1. **Primary**: Enhance ADR-001 Decision and Consequences sections
2. **Secondary**: Review solution-strategy.md for alignment
3. **Validation**: Run traceability validation after implementation

## Implementation Complexity

- **Effort**: Small (1-2 hours)
- **Files**: 2-3
- **Risk**: Low-Medium
```

## Procedures

### 1. Analyze Feedback

```
PROCEDURE analyze_feedback(feedback_id, system_name, feedback_text, category):

  LOAD architecture context:
    READ _state/solarch_config.json
    READ _state/solarch_progress.json
    READ traceability/adr_registry.json  # ROOT level - single source of truth
    READ traceability/component_registry.json  # ROOT level - single source of truth
    READ traceability/solarch_traceability_register.json  # ROOT level - single source of truth

  CLASSIFY feedback:
    DETECT category (ADR, Component, Diagram, Quality, Traceability, Documentation)
    DETECT type (Enhancement, Correction, Clarification, Challenge)
    DETECT scope (Single file, Multiple files, Cross-cutting)

  FIND direct impacts:
    SEARCH for files matching feedback keywords
    IDENTIFY specific sections affected
    DOCUMENT current content

  FIND cascade impacts:
    FOR each direct impact:
      FIND files that reference this file
      CHECK for consistency dependencies
      NOTE sections that may need alignment

  ANALYZE traceability chains:
    LOAD traceability register
    FIND chains involving affected files
    ASSESS chain integrity risk

  ASSESS risk:
    EVALUATE probability of issues
    EVALUATE impact severity
    IDENTIFY blockers and warnings

  GENERATE recommendations:
    PRIMARY: Main changes required
    SECONDARY: Alignment changes
    VALIDATION: Steps to verify

  CALCULATE complexity:
    effort = estimate based on files and changes
    risk_level = based on traceability impact

  WRITE impact_analysis.md

  UPDATE registry:
    impacts = {
      direct_files: count,
      cascade_files: count,
      traceability_chains: count
    }

  RETURN impact_analysis
```

### 2. Scan Architecture Files

```
PROCEDURE scan_architecture(system_name, keywords):

  files_to_scan = [
    "09-decisions/ADR-*.md",
    "04-solution-strategy/*.md",
    "05-building-blocks/*.md",
    "06-runtime/*.md",
    "07-quality/*.md",
    "08-deployment/*.md",
    "traceability/*_registry.json",  # ROOT level registries
    "diagrams/*.mmd"
  ]

  matches = []

  FOR each file_pattern IN files_to_scan:
    FOR each file IN GLOB(SolArch_{system_name}/{file_pattern}):
      content = READ file
      IF any keyword IN content:
        matches.append({
          file: file,
          matches: extract_matches(content, keywords)
        })

  RETURN matches
```

### 3. Analyze Traceability Impact

```
PROCEDURE analyze_traceability(system_name, affected_files):

  LOAD traceability register:
    READ traceability/solarch_traceability_register.json  # ROOT level - single source of truth

  affected_chains = []

  FOR each file IN affected_files:
    EXTRACT entity_id from file (e.g., ADR-001 from ADR-001-*.md)

    FOR each chain IN traceability.chains:
      IF entity_id IN chain.nodes:
        affected_chains.append({
          chain: chain,
          affected_node: entity_id,
          impact: assess_chain_impact(chain, entity_id)
        })

  RETURN affected_chains
```

### 4. Generate Impact Matrix

```
PROCEDURE generate_impact_matrix(direct, cascade, traceability):

  matrix = {
    "direct_impacts": [],
    "cascade_impacts": [],
    "traceability_impacts": []
  }

  FOR each impact IN direct:
    matrix.direct_impacts.append({
      "file": impact.file,
      "sections": impact.sections,
      "change_type": impact.change_type,
      "current_content": excerpt,
      "suggested_change": recommendation
    })

  FOR each impact IN cascade:
    matrix.cascade_impacts.append({
      "file": impact.file,
      "reason": impact.reason,
      "dependency": impact.source_file,
      "change_type": "review" | "update" | "none"
    })

  FOR each chain IN traceability:
    matrix.traceability_impacts.append({
      "chain_id": chain.id,
      "nodes": chain.nodes,
      "affected_node": chain.affected_node,
      "integrity_risk": chain.risk
    })

  RETURN matrix
```

## Impact Categories

| Category | Files to Scan | Typical Impact |
|----------|---------------|----------------|
| ADR | 09-decisions/ADR-*.md | Decision docs, registry |
| Component | 05-building-blocks/*.md | Component docs, diagrams |
| Diagram | diagrams/*.mmd | Mermaid files, referencing docs |
| Quality | 07-quality/*.md | Quality scenarios, NFRs |
| Traceability | *-traceability.json | Chain integrity |
| Documentation | 11-glossary/*.md | Terms, references |

## Risk Levels

| Level | Criteria | Typical Response |
|-------|----------|------------------|
| Low | Single file, no cascades | Proceed normally |
| Medium | Multiple files, some cascades | Review dependencies |
| High | Traceability impacts, many cascades | Careful planning |
| Critical | Cross-cutting, blocking | Detailed review required |

## Error Handling

| Error | Action |
|-------|--------|
| File not found | Skip, note in analysis |
| Parse error | Log warning, continue |
| Traceability register missing | Note limitation, continue |

## Integration Points

### Upstream
- Receives feedback_id from `SolArch_FeedbackRegister`
- Gets architecture context from Solution Architecture outputs

### Downstream
- Provides impact analysis to `/solarch-feedback` command
- Updates registry via `SolArch_FeedbackRegister`
- Informs `SolArch_FeedbackImplementer` planning

## Quality Gates

```bash
# Validate impact analysis completeness
python3 .claude/hooks/solarch_quality_gates.py --validate-feedback SF-001 --dir SolArch_X/
```
