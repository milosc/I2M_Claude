---
name: analyzing-e2e-traceability
description: Use when you need to validate and document end-to-end traceability chains from client analysis through to solution architecture.
model: sonnet
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-e2e-traceability started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-e2e-traceability ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill analyzing-e2e-traceability instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Analyze E2E Traceability

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: SolutionArchitecture_E2ETraceabiliyAnalyzer
- **Version**: 1.1.0
- **Created**: 2024-12-16
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v1.1.0 (2025-12-19): Updated metadata for consistency
  - v1.0.0 (2024-12-16): Initial release

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
- output files created (traceability analysis)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '\"skill_name\": \"analyzing-e2e-traceability\"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill \"analyzing-e2e-traceability\" --stage solarch
```

Logging is handled automatically by the skill framework. No user action required.

---

# Traceability Analyzer Skill

> **Version**: 1.0.0
> **Purpose**: Validate and document traceability chains from Client Analysis through to Solution Architecture

---

## Overview

Traceability is the **golden thread** connecting:
1. **Client Pain Points** → Why we're building this
2. **JTBD** → What job users need to accomplish
3. **Requirements** → What the system must do
4. **Screens/Components** → How users interact
5. **Architecture Decisions** → How we build it
6. **Quality Attributes** → How well it performs

This skill validates that every architectural decision traces back to business justification and that no requirements are "orphaned" without architectural coverage.

---

## Traceability Chain Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TRACEABILITY CHAIN                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   03_ClientAnalysis          04_Prototype           05_Specifications       │
│   ────────────────          ────────────           ─────────────────        │
│                                                                             │
│   Pain Point (PP-*)    →    Screen Spec    →    Module (MOD-*)             │
│        ↓                        ↓                     ↓                     │
│   JTBD (JTBD-*)        →    Component      →    API Contract               │
│        ↓                        ↓                     ↓                     │
│   Workflow (WF-*)      →    Data Model     →    Test Case (TC-*)           │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   06_Solution_Architecture                                                  │
│   ────────────────────────                                                  │
│                                                                             │
│   ADR-*        →    Component Diagram    →    Contract                     │
│      ↓                    ↓                       ↓                         │
│   Quality Attr    →    Runtime Scenario    →    Risk                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Chain Types

### Chain A: Pain Point → ADR

Every architectural decision must trace back to a business pain point.

```yaml
chain_a:
  source: PP-001
  source_text: "Picking doesn't reflect adjustments immediately"
  source_file: "03_ClientAnalysis/01-analysis/ANALYSIS_SUMMARY.md"
  
  via_jtbd: JTBD-1.1
  via_jtbd_text: "Complete stock adjustment in under 60 seconds"
  
  via_requirement: US-003
  via_requirement_text: "Know picking was updated after adjustment"
  via_requirement_priority: P0
  via_module: MOD-INV-ADJUST-01
  
  target: ADR-006
  target_text: "Event-Driven Communication"
  target_file: "06_Solution_Architecture/09-decisions/ADR-006-event-communication.md"
```

### Chain B: Requirement → Quality Scenario

Every functional requirement maps to quality attributes and measurable scenarios.

```yaml
chain_b:
  source: FR-002
  source_text: "Real-time Stock Propagation"
  source_priority: P0
  
  quality_attribute: Performance
  quality_metric: "Propagation latency"
  quality_target: "< 10 seconds"
  
  scenario: QS-PERF-001
  scenario_text: "When adjustment saved, picking reflects within 10 seconds"
  
  test_case: TC-E2E-002
```

### Chain C: Module → C4 Component

Every module in specifications maps to a C4 component diagram.

```yaml
chain_c:
  source: MOD-INV-ADJUST-01
  source_name: "Stock Adjustment"
  source_file: "05_Specifications/modules/MOD-INV-ADJUST-01.md"
  
  container: "Inventory API"
  
  components:
    - AdjustmentController
    - AdjustmentService
    - AdjustmentRepository
    - EventPublisher
  
  diagram: "06_Solution_Architecture/05-building-blocks/modules/adjustment/c4-component.mermaid"
```

---

## Validation Rules

### Rule 1: 100% Pain Point Coverage

Every pain point must be addressed by at least one ADR.

```javascript
function validatePainPointCoverage(painPoints, adrs) {
  const errors = [];
  
  for (const pp of painPoints) {
    const addressed = adrs.some(adr => 
      adr.traceability.painPoints.includes(pp.id)
    );
    
    if (!addressed) {
      errors.push({
        rule: "PAIN_POINT_COVERAGE",
        severity: "ERROR",
        message: `Pain point ${pp.id} not addressed by any ADR`,
        painPoint: pp.id,
        text: pp.text
      });
    }
  }
  
  return errors;
}
```

### Rule 2: P0 Requirement Architecture Coverage

Every P0 requirement must have architectural coverage.

```javascript
function validateP0Coverage(requirements, adrs) {
  const errors = [];
  const p0Reqs = requirements.filter(r => r.priority === "P0");
  
  for (const req of p0Reqs) {
    const addressed = adrs.some(adr =>
      adr.traceability.requirements.includes(req.id)
    );
    
    if (!addressed) {
      errors.push({
        rule: "P0_COVERAGE",
        severity: "ERROR",
        message: `P0 requirement ${req.id} has no ADR coverage`,
        requirement: req.id,
        text: req.text
      });
    }
  }
  
  return errors;
}
```

### Rule 3: Module Architecture Coverage

Every module must have a C4 component diagram.

```javascript
function validateModuleCoverage(modules, diagrams) {
  const errors = [];
  
  for (const mod of modules) {
    const hasDiagram = diagrams.some(d => 
      d.module === mod.id && d.level === "component"
    );
    
    if (!hasDiagram) {
      errors.push({
        rule: "MODULE_DIAGRAM",
        severity: "WARNING",
        message: `Module ${mod.id} has no C4 component diagram`,
        module: mod.id
      });
    }
  }
  
  return errors;
}
```

### Rule 4: ADR Completeness

Every ADR must have complete traceability section.

```javascript
function validateAdrCompleteness(adr) {
  const errors = [];
  
  if (!adr.traceability.painPoints?.length) {
    errors.push({
      rule: "ADR_PAIN_POINTS",
      severity: "ERROR",
      adr: adr.id,
      message: "ADR must reference at least one pain point"
    });
  }
  
  if (!adr.traceability.requirements?.length) {
    errors.push({
      rule: "ADR_REQUIREMENTS",
      severity: "WARNING",
      adr: adr.id,
      message: "ADR should reference requirements"
    });
  }
  
  if (!adr.rationale?.alternatives?.length) {
    errors.push({
      rule: "ADR_ALTERNATIVES",
      severity: "WARNING",
      adr: adr.id,
      message: "ADR should document alternatives considered"
    });
  }
  
  return errors;
}
```

### Rule 5: Cross-Reference Integrity

All references must point to existing entities.

```javascript
function validateReferences(architecture, specifications) {
  const errors = [];
  
  // Check ADR references to pain points
  for (const adr of architecture.adrs) {
    for (const ppRef of adr.traceability.painPoints) {
      if (!specifications.painPoints.has(ppRef)) {
        errors.push({
          rule: "INVALID_REFERENCE",
          severity: "ERROR",
          adr: adr.id,
          reference: ppRef,
          message: `Pain point ${ppRef} referenced but not found`
        });
      }
    }
    
    // Check requirement references
    for (const reqRef of adr.traceability.requirements) {
      if (!specifications.requirements.has(reqRef)) {
        errors.push({
          rule: "INVALID_REFERENCE",
          severity: "ERROR",
          adr: adr.id,
          reference: reqRef,
          message: `Requirement ${reqRef} referenced but not found`
        });
      }
    }
  }
  
  return errors;
}
```

---

## Traceability Matrix Output

### Format

```markdown
# Architecture Traceability Matrix

## Pain Point → ADR Coverage

| Pain Point | Description | ADRs | Status |
|------------|-------------|------|--------|
| PP-001 | Picking doesn't reflect adjustments | ADR-006 | ✅ Covered |
| PP-002 | System state reverts | ADR-006, ADR-004 | ✅ Covered |

## Requirement → Architecture Mapping

| Req ID | Priority | Description | ADRs | Components | Quality |
|--------|----------|-------------|------|------------|---------|
| US-001 | P0 | Search items | ADR-005, ADR-009 | ItemSearch | PERF-001 |
| US-003 | P0 | Know propagation status | ADR-006 | PropagationIndicator | PERF-004 |

## Module → Component Diagram Coverage

| Module | Name | C4 Diagram | Status |
|--------|------|------------|--------|
| MOD-INV-ADJUST-01 | Stock Adjustment | c4-component-adjustment.mermaid | ✅ |
| MOD-INV-HISTORY-01 | Transaction History | c4-component-history.mermaid | ✅ |

## Coverage Summary

| Metric | Count | Covered | Percentage |
|--------|-------|---------|------------|
| Pain Points | 10 | 10 | 100% |
| P0 Requirements | 12 | 12 | 100% |
| P1 Requirements | 8 | 8 | 100% |
| Modules | 5 | 5 | 100% |
| ADRs with Pain Points | 10 | 10 | 100% |
```

---

## JSON Registry Schema

### architecture-traceability.json

```json
{
  "$schema": "architecture-traceability/v1.0",
  "generated": "2025-12-16T00:00:00Z",
  "sourceFolder": "05_Product_Specifications_InventorySystem",
  "targetFolder": "06_Solution_Architecture_InventorySystem",
  
  "coverage": {
    "painPoints": {
      "total": 10,
      "covered": 10,
      "percentage": 100
    },
    "requirements": {
      "p0": {"total": 12, "covered": 12, "percentage": 100},
      "p1": {"total": 8, "covered": 8, "percentage": 100},
      "p2": {"total": 6, "covered": 6, "percentage": 100}
    },
    "modules": {
      "total": 5,
      "diagrammed": 5,
      "percentage": 100
    },
    "adrs": {
      "total": 10,
      "withPainPoints": 10,
      "withRequirements": 10
    }
  },
  
  "chains": [
    {
      "id": "CHAIN-001",
      "type": "pain-to-adr",
      "source": {
        "type": "painPoint",
        "id": "PP-001",
        "text": "Picking doesn't reflect adjustments immediately",
        "file": "03_ClientAnalysis/01-analysis/ANALYSIS_SUMMARY.md"
      },
      "intermediates": [
        {
          "type": "jtbd",
          "id": "JTBD-1.1",
          "text": "Complete stock adjustment in under 60 seconds"
        },
        {
          "type": "requirement",
          "id": "US-003",
          "priority": "P0",
          "text": "Know picking was updated after adjustment"
        },
        {
          "type": "module",
          "id": "MOD-INV-ADJUST-01",
          "name": "Stock Adjustment"
        }
      ],
      "targets": [
        {
          "type": "adr",
          "id": "ADR-006",
          "title": "Event-Driven Communication",
          "file": "09-decisions/ADR-006-event-communication.md"
        }
      ]
    }
  ],
  
  "validationResults": {
    "timestamp": "2025-12-16T00:00:00Z",
    "errors": 0,
    "warnings": 0,
    "passed": true,
    "rules": [
      {"rule": "PAIN_POINT_COVERAGE", "status": "PASS", "details": "10/10 covered"},
      {"rule": "P0_COVERAGE", "status": "PASS", "details": "12/12 covered"},
      {"rule": "MODULE_DIAGRAM", "status": "PASS", "details": "5/5 diagrammed"},
      {"rule": "ADR_COMPLETENESS", "status": "PASS", "details": "10/10 complete"}
    ]
  }
}
```

---

## Validation Report Output

### TRACEABILITY_VALIDATION_REPORT.md

```markdown
# Traceability Validation Report

**Generated**: 2025-12-16
**Source**: 05_Product_Specifications_InventorySystem
**Target**: 06_Solution_Architecture_InventorySystem

---

## Executive Summary

**Status**: ✅ ALL VALIDATIONS PASSED

| Category | Result |
|----------|--------|
| Pain Point Coverage | 10/10 (100%) ✅ |
| P0 Requirement Coverage | 12/12 (100%) ✅ |
| Module Diagram Coverage | 5/5 (100%) ✅ |
| ADR Completeness | 10/10 (100%) ✅ |
| Reference Integrity | 0 errors ✅ |

---

## Detailed Results

### Pain Point to ADR Mapping

| PP ID | Pain Point | ADRs | Validation |
|-------|------------|------|------------|
| PP-001 | Picking doesn't reflect adjustments | ADR-006 | ✅ |
| PP-002 | System state reverts | ADR-004, ADR-006 | ✅ |
| PP-003 | No clear explanation of changes | ADR-004 | ✅ |
| PP-004 | No confirmation before save | ADR-008 | ✅ |
| PP-005 | Reason codes bypassed | ADR-007 | ✅ |
| PP-006 | Source bin selection confusing | ADR-005, ADR-008 | ✅ |
| PP-007 | Too many generic warnings | ADR-008 | ✅ |
| PP-008 | Performance slow | ADR-009 | ✅ |
| PP-009 | Inconsistent bin naming | ADR-004 | ✅ |
| PP-010 | Audit trail hard to access | ADR-004 | ✅ |

### P0 Requirements Coverage

| Req ID | Requirement | Module | ADRs | Validation |
|--------|-------------|--------|------|------------|
| US-001 | Search items quickly | MOD-INV-ADJUST-01 | ADR-005, ADR-009 | ✅ |
| US-002 | Confirm before saving | MOD-INV-ADJUST-01 | ADR-008 | ✅ |
| US-003 | Know propagation status | MOD-INV-ADJUST-01 | ADR-006 | ✅ |
| US-004 | View transaction history | MOD-INV-HISTORY-01 | ADR-004 | ✅ |
| US-005 | View exception metrics | MOD-INV-EXCEPT-01 | ADR-003 | ✅ |
| ... | ... | ... | ... | ✅ |

### Warnings

None.

### Errors

None.

---

## Recommendations

1. ✅ All critical traceability chains complete
2. ✅ No orphaned requirements
3. ✅ No orphaned ADRs
4. ✅ All modules have architectural documentation

---

**Validation Status**: COMPLETE
**Next Action**: Ready for implementation
```

---

## Execution Process

### Step 1: Load Source Data

```yaml
load:
  - 05_Specifications/_registry/traceability.json
  - 05_Specifications/_registry/modules.json
  - 05_Specifications/MASTER_DEVELOPMENT_PLAN.md
  - 03_ClientAnalysis/01-analysis/ANALYSIS_SUMMARY.md
```

### Step 2: Load Target Data (v3.0)

```yaml
load:
  # ROOT-level registries (v3.0)
  - traceability/adr_registry.json
  - traceability/component_registry.json
  - traceability/traceability_matrix_master.json
```

> **NOTE**: Local `_registry/` folders are DEPRECATED. Use ROOT-level `traceability/` registries.

### Step 3: Build Chain Map

Connect source entities to target entities via intermediate hops.

### Step 4: Validate Rules

Run all validation rules and collect errors/warnings.

### Step 5: Generate Reports (v3.0)

- `traceability/traceability_matrix_master.json` (ROOT level)
- `traceability/solarch_traceability_register.json` (ROOT level)
- `reports/TRACEABILITY_VALIDATION_REPORT.md`
- Update `reports/GENERATION_SUMMARY.md`

> **NOTE**: Reports now in `reports/` folder. Registries at ROOT `traceability/`.

---

## State Management Integration

### Command System Integration

This skill is the primary skill for checkpoint 11 (BLOCKING):

```
Commands that use this skill:
└─ /solarch-trace (checkpoint 11, BLOCKING)
```

### Blocking Validation

Checkpoint 11 is **BLOCKING** - must pass before proceeding to finalization:

- Pain Point Coverage: 100% required
- P0 Requirement Coverage: 100% required
- Module Architecture Coverage: 100% required

### Registry Updates (v3.0)

After validation, update ROOT-level traceability files:

**Primary: `traceability/traceability_matrix_master.json`**
```json
{
  "version": "1.0.0",
  "stage": "SolutionArchitecture",
  "checkpoint": 11,
  "validated_at": "ISO8601",
  "validation_passed": true,
  "coverage": {
    "pain_points": {
      "total": 21,
      "addressed": 21,
      "coverage_percent": 100
    },
    "requirements": {
      "total": 15,
      "covered": 15,
      "coverage_percent": 100
    },
    "modules": {
      "total": 16,
      "covered": 16,
      "coverage_percent": 100
    }
  }
}
```

**Stage-specific: `traceability/solarch_traceability_register.json`**

> **NOTE (v3.0)**: Local `_registry/architecture-traceability.json` is DEPRECATED. Use ROOT `traceability/traceability_matrix_master.json`.

### Quality Gate Validation

```bash
# Validate traceability (checkpoint 11)
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 11 --dir SolArch_X/

# Or validate traceability specifically
python3 .claude/hooks/solarch_quality_gates.py --validate-traceability --dir SolArch_X/
```

### Failure Actions

If traceability validation fails:
1. Identify gaps in pain point/requirement coverage
2. Return to relevant commands to add missing references
3. Re-run `/solarch-trace` after fixes

---

**Skill Status**: Ready for Use
