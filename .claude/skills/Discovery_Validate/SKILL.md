---
name: validating-discovery-package
description: Use when you need to perform final quality assurance, cross-reference validation, and traceability checks on a complete discovery package.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-discovery-package started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-discovery-package ended '{"stage": "discovery"}'
---

# Validate Discovery Package

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill validating-discovery-package instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_Validate
- **Version**: 2.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.1.0 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Specialized skill for cross-reference validation and quality assurance of the complete documentation package. Ensures completeness, consistency, and traceability across all generated documents.

**Role**: You are a Quality Assurance Specialist for product documentation. Your expertise is finding gaps, inconsistencies, and broken connections in complex documentation sets. You ensure every claim is traceable and every cross-reference resolves.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:validating-discovery-package:started` - When skill begins
- `skill:validating-discovery-package:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- All discovery phases (1-10) are complete
- Request mentions "validate", "check quality", "verify completeness"
- User wants final quality review before handoff
- Checkpoint 11 (final) in orchestrator flow

## Input Requirements

| Input | Required | Description |
|-------|----------|-------------|
| Output Path | Yes | Root folder with all generated content |
| All Generated Files | Yes | Complete documentation package |
| Original Analysis | Yes | ANALYSIS_SUMMARY.md for traceability |

## Validation Categories

### 1. Completeness Checks
- All expected files exist
- All files have required sections
- All personas have complete profiles
- All JTBDs have required components

### 2. Consistency Checks
- Persona names match across documents
- Pain point IDs match registry
- Feature names match roadmap
- Metrics align with KPIs

### 3. Traceability Checks
- Pain points → JTBD → Features → Screens
- All pain points addressed
- All JTBDs mapped to features
- All screens map to roadmap epics

### 4. Cross-Reference Checks
- All internal links resolve
- All file references exist
- All ID references valid
- All names match

### 5. Prototype Readiness Checks
- Screen inventory complete
- Data model matches sample data
- Navigation covers all flows
- Components defined for screens

## Validation Rules

### File Existence Rules

| File | Required | Location |
|------|----------|----------|
| PROGRESS_TRACKER.md | Yes | 00-management/ |
| ANALYSIS_SUMMARY.md | Yes | 01-analysis/ |
| pain-point-registry.md | Yes | 01-analysis/ |
| jtbd-jobs-to-be-done.md | Yes | 02-research/ |
| persona-*.md (3+ files) | Yes | 02-research/ |
| product-vision.md | Yes | 03-strategy/ |
| product-strategy.md | Yes | 03-strategy/ |
| product-roadmap.md | Yes | 03-strategy/ |
| kpis-and-goals.md | Yes | 03-strategy/ |
| screen-definitions.md | Yes | 04-design-specs/ |
| navigation-structure.md | Yes | 04-design-specs/ |
| data-fields.md | Yes | 04-design-specs/ |
| sample-data.json | Yes | 04-design-specs/ |
| ui-components.md | Yes | 04-design-specs/ |
| interaction-patterns.md | Yes | 04-design-specs/ |
| INDEX.md | Yes | 05-documentation/ |
| README.md | Yes | 05-documentation/ |
| DOCUMENTATION_SUMMARY.md | Yes | 05-documentation/ |
| GETTING_STARTED.md | Yes | 05-documentation/ |
| FILES_CREATED.md | Yes | 05-documentation/ |
| VALIDATION_REPORT.md | Yes | 05-documentation/ |

### Content Completeness Rules

| Document | Required Sections |
|----------|-------------------|
| Persona files | Overview, Goals, Pain Points, Workflow, Design Implications |
| JTBD file | Feature areas, JTBD format (When/Want/So), Priority, Persona mapping |
| Vision | Vision statement, Pain points, Solution capabilities |
| Strategy | Strategic pillars, Go-to-market |
| Roadmap | Phases, Epics, Timeline |
| KPIs | North Star, Category KPIs, ROI (if data available) |
| Screen definitions | Screen inventory, Layout specs |
| Data fields | Entity definitions, Field types |
| Sample data | Valid JSON, Matches data fields |

### Traceability Rules

| Source | Must Map To |
|--------|-------------|
| Pain Points (P0) | At least one JTBD |
| Pain Points (P0) | Vision capabilities |
| JTBDs (P0) | Roadmap features |
| Personas | JTBD assignments |
| Roadmap epics (Phase 1) | Screen definitions |
| Data entities | Sample data records |

## Output Format

### VALIDATION_REPORT.md Template

```markdown
# Validation Report - [Product Name] Documentation

**Validation Date**: [Date]
**Validator**: Discovery Validate Skill v2.0
**Overall Status**: 🟢 Pass | 🟡 Pass with Warnings | 🔴 Fail

---

## 📊 Validation Summary

| Category | Status | Score | Issues |
|----------|--------|-------|--------|
| File Completeness | [Status] | [N]/[N] | [N] |
| Content Completeness | [Status] | [N]/[N] | [N] |
| Consistency | [Status] | [N]/[N] | [N] |
| Traceability | [Status] | [N]/[N] | [N] |
| Cross-References | [Status] | [N]/[N] | [N] |
| Prototype Readiness | [Status] | [N]/[N] | [N] |
| **Overall** | **[Status]** | **[N]%** | **[N]** |

---

## ✅ File Completeness ([N]/[N])

### Required Files

| File | Status | Notes |
|------|--------|-------|
| PROGRESS_TRACKER.md | ✅/❌ | [Notes if any] |
| ANALYSIS_SUMMARY.md | ✅/❌ | [Notes] |
| pain-point-registry.md | ✅/❌ | [Notes] |
| jtbd-jobs-to-be-done.md | ✅/❌ | [Notes] |
| persona-[name-1].md | ✅/❌ | [Notes] |
| persona-[name-2].md | ✅/❌ | [Notes] |
| persona-[name-3].md | ✅/❌ | [Notes] |
| product-vision.md | ✅/❌ | [Notes] |
| product-strategy.md | ✅/❌ | [Notes] |
| product-roadmap.md | ✅/❌ | [Notes] |
| kpis-and-goals.md | ✅/❌ | [Notes] |
| screen-definitions.md | ✅/❌ | [Notes] |
| navigation-structure.md | ✅/❌ | [Notes] |
| data-fields.md | ✅/❌ | [Notes] |
| sample-data.json | ✅/❌ | [Notes] |
| ui-components.md | ✅/❌ | [Notes] |
| interaction-patterns.md | ✅/❌ | [Notes] |
| INDEX.md | ✅/❌ | [Notes] |
| README.md | ✅/❌ | [Notes] |
| DOCUMENTATION_SUMMARY.md | ✅/❌ | [Notes] |
| GETTING_STARTED.md | ✅/❌ | [Notes] |
| FILES_CREATED.md | ✅/❌ | [Notes] |

---

## ✅ Content Completeness ([N]/[N])

### Persona Files

| Persona | Overview | Goals | Pain Points | Workflow | Design Implications |
|---------|----------|-------|-------------|----------|---------------------|
| [Name 1] | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| [Name 2] | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| [Name 3] | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

### Strategy Documents

| Document | Required Sections | Status |
|----------|-------------------|--------|
| Vision | Statement, Pain points, Capabilities | ✅/❌ |
| Strategy | Pillars, Go-to-market | ✅/❌ |
| Roadmap | Phases, Epics, Timeline | ✅/❌ |
| KPIs | North Star, KPIs | ✅/❌ |

### Design Specifications

| Document | Required Sections | Status |
|----------|-------------------|--------|
| Screens | Inventory, Layouts | ✅/❌ |
| Navigation | Site map, Flows | ✅/❌ |
| Data fields | Entities, Fields | ✅/❌ |
| Sample data | Valid JSON | ✅/❌ |
| Components | Component specs | ✅/❌ |
| Interactions | Patterns | ✅/❌ |

---

## ✅ Consistency Checks ([N]/[N])

### Persona Name Consistency

| Document | Personas Referenced | Match Status |
|----------|---------------------|--------------|
| JTBD | [Names] | ✅/❌ |
| Vision | [Names] | ✅/❌ |
| Roadmap | [Names] | ✅/❌ |
| Screen definitions | [Names] | ✅/❌ |

### Pain Point ID Consistency

| Pain Point | Registry | JTBD | Vision | Status |
|------------|----------|------|--------|--------|
| PP-001 | ✅ | ✅/❌ | ✅/❌ | [Status] |
| PP-002 | ✅ | ✅/❌ | ✅/❌ | [Status] |

### Feature Name Consistency

| Feature | Roadmap | Screens | Status |
|---------|---------|---------|--------|
| [Feature 1] | ✅ | ✅/❌ | [Status] |
| [Feature 2] | ✅ | ✅/❌ | [Status] |

---

## ✅ Traceability Matrix ([N]/[N])

### Pain Points → Coverage

| Pain Point ID | Severity | JTBD | Vision | Feature | Screen | Status |
|---------------|----------|------|--------|---------|--------|--------|
| PP-001 | P0 | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | [Status] |
| PP-002 | P0 | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | [Status] |
| PP-003 | P1 | ✅/❌ | - | ✅/❌ | ✅/❌ | [Status] |

### JTBD → Feature Mapping

| JTBD ID | Priority | Feature | Epic | Phase | Status |
|---------|----------|---------|------|-------|--------|
| JTBD-1.1 | P0 | ✅/❌ | ✅/❌ | ✅/❌ | [Status] |
| JTBD-1.2 | P0 | ✅/❌ | ✅/❌ | ✅/❌ | [Status] |

### Roadmap → Screen Coverage

| Phase | Epic | Screens Defined | Status |
|-------|------|-----------------|--------|
| Phase 1 | Epic 1 | [Screen list] | ✅/❌ |
| Phase 1 | Epic 2 | [Screen list] | ✅/❌ |

---

## ✅ Cross-Reference Validation ([N]/[N])

### Internal Links

| Document | Links Found | Valid | Invalid |
|----------|-------------|-------|---------|
| INDEX.md | [N] | [N] | [N] |
| README.md | [N] | [N] | [N] |
| GETTING_STARTED.md | [N] | [N] | [N] |

### Invalid Links Found
[List any broken links with file and target]

1. [File]: Link to [target] - [Issue]

---

## ✅ Prototype Readiness ([N]/[N])

### Screen Inventory Completeness

| Check | Status | Details |
|-------|--------|---------|
| All Phase 1 screens defined | ✅/❌ | [N]/[N] screens |
| Layout specs present | ✅/❌ | [N]/[N] screens |
| Component mapping complete | ✅/❌ | [Details] |

### Data Model Validation

| Check | Status | Details |
|-------|--------|---------|
| All entities defined | ✅/❌ | [N] entities |
| Field types specified | ✅/❌ | [N]/[N] fields |
| Sample data matches schema | ✅/❌ | [Details] |
| Foreign keys valid | ✅/❌ | [Details] |

### Navigation Coverage

| Check | Status | Details |
|-------|--------|---------|
| All screens reachable | ✅/❌ | [N]/[N] screens |
| Critical flows defined | ✅/❌ | [N] flows |
| Entry points clear | ✅/❌ | [Details] |

---

## ⚠️ Issues Found

### Critical Issues (Must Fix)
[List any issues that prevent implementation]

1. **[Issue Title]**
   - Location: [File/Section]
   - Description: [What's wrong]
   - Impact: [Why it matters]
   - Resolution: [How to fix]

### Warnings (Should Fix)
[List issues that may cause confusion]

1. **[Issue Title]**
   - Location: [File/Section]
   - Description: [What's wrong]
   - Impact: [Why it matters]
   - Resolution: [How to fix]

### Notes (Minor)
[List minor inconsistencies or suggestions]

1. [Note]

---

## 📊 Statistics Summary

| Metric | Count |
|--------|-------|
| **Total Files** | [N] |
| **Personas** | [N] |
| **Pain Points** | [N] (P0: [N], P1: [N], P2: [N]) |
| **JTBDs** | [N] |
| **Features** | [N] |
| **Screens** | [N] |
| **Data Entities** | [N] |
| **Cross-references** | [N] valid, [N] invalid |

---

## 🎯 Validation Conclusion

### Overall Assessment
[1-2 paragraph summary of documentation quality]

### Strengths
- [Strength 1]
- [Strength 2]
- [Strength 3]

### Areas for Improvement
- [Area 1]
- [Area 2]

### Recommendation
**[Ready for Implementation / Needs Revision / Major Rework Required]**

[Brief rationale for recommendation]

---

## 📋 Sign-Off Checklist

- [ ] All critical issues resolved
- [ ] All P0 pain points traced to screens
- [ ] Sample data matches data model
- [ ] Navigation covers all critical flows
- [ ] Documentation reviewed by stakeholder

---

**Validation Complete**: [Date]
**Report Version**: 1.0
**Framework**: Discovery Skills v2.0
```

## Validation Logic

### Severity Classification

| Issue Type | Severity | Action |
|------------|----------|--------|
| Missing required file | Critical | Must fix before handoff |
| Broken cross-reference | Critical | Must fix |
| P0 pain point not traced | Critical | Must fix |
| Missing section in file | Warning | Should fix |
| Inconsistent naming | Warning | Should fix |
| Minor formatting issue | Note | Nice to fix |

### Pass/Fail Criteria

| Status | Criteria |
|--------|----------|
| 🟢 Pass | 0 critical issues, ≤5 warnings |
| 🟡 Pass with Warnings | 0 critical issues, >5 warnings |
| 🔴 Fail | ≥1 critical issue |

## Quality Checklist

Before completing validation:
- [ ] Every file checked for existence
- [ ] Every required section verified
- [ ] All cross-references tested
- [ ] Traceability matrix complete
- [ ] Sample data JSON parsed successfully
- [ ] All personas have quotes
- [ ] All P0 items traced

## Error Handling

| Issue | Action |
|-------|--------|
| File not found | Mark as critical issue |
| Section missing | Mark as warning |
| Link broken | List in invalid links section |
| JSON parse error | Mark as critical for sample data |
| Name mismatch | Note all instances |

## Integration Points

### Receives From
- All previous phases - Documents to validate
- `Discovery_DocIndex` - File list
- `Discovery_Orchestrator` - Expected outputs

### Feeds Into
- Final handoff documentation
- Quality gates for implementation
- Stakeholder sign-off

## State Management Reminder

⚠️ **This skill produces output files only.** The calling orchestrator/command is responsible for updating state after Phase 11 completes.

**After running Discovery_Validate, update state:**
```bash
python3 .claude/skills/tools/update_discovery_state.py --phase 11_validate --status complete
```

**Or use the all-complete shortcut:**
```bash
python3 .claude/skills/tools/update_discovery_state.py --set-complete
```

**Or manually update `_state/discovery_progress.json`:**
```json
"11_validate": { "status": "complete", "started": "<ISO>", "completed": "<ISO>" },
"overall_progress": 100,
"resumable_from": null
```

**Also update `_state/discovery_config.json`:**
```json
"status": "complete"
```

---

**Skill Version**: 3.0
**Framework Compatibility**: Discovery Skills Framework v2.0
