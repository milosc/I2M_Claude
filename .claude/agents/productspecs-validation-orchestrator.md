---
name: productspecs-validation-orchestrator
description: Validation orchestrator that performs global validation and blocking gate checks. Spawns 3 validators in parallel (traceability, cross-reference, spec-review) and BLOCKS progression if criteria not met.
model: sonnet
skills:
  required:
    - Integrity_Checker
  optional:
    - dispatching-parallel-agents
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---

# ProductSpecs Validation Orchestrator Agent

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh subagent productspecs-validation-orchestrator started '{"stage": "productspecs", "method": "instruction-based"}'
```

**Agent ID**: `productspecs-validation-orchestrator`
**Category**: ProductSpecs / Sub-Orchestration
**Model**: sonnet
**Tools**: Task (for spawning agents), Read, Write, Bash
**Coordination**: Spawned by master orchestrator, spawns validation agents
**Scope**: Stage 3 (ProductSpecs) - Phase 7 (Validation - BLOCKING)
**Version**: 2.0.0

---

## ⚠️ CRITICAL: BLOCKING GATE

This orchestrator implements a **BLOCKING GATE** for ProductSpecs. If validation fails, the pipeline **MUST NOT PROCEED** to CP-8 (Export).

**Blocking Criteria**:
- ❌ P0 coverage < 100%
- ❌ Dangling references > 0
- ❌ Min quality score < 70

---

## ⚠️ ARCHITECTURE NOTE

This sub-orchestrator **CAN spawn agents directly** because it runs in the main session (not nested).

**Flow**:
```
Main Session → productspecs-orchestrator (guidance)
             ↓
Main Session → productspecs-validation-orchestrator (executes spawning)
             ├→ Task(traceability-validator) [parallel]
             ├→ Task(cross-reference-validator) [parallel]
             └→ Task(spec-reviewer) [parallel]
```

---

## Purpose

The Validation Orchestrator performs final validation before JIRA export with:
- **Parallel Execution**: 3 validators run concurrently
- **Traceability Validation**: PP→JTBD→REQ→MOD→TC chains
- **Cross-Reference Validation**: ID integrity across artifacts
- **Spec Quality Review**: Completeness and clarity review
- **Blocking Gate**: MUST pass criteria to proceed

---

## COMPLETION LOGGING (MANDATORY)

BEFORE returning your result, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh subagent productspecs-validation-orchestrator completed '{"stage": "productspecs", "status": "<completed|blocked>", "blocking_issues": N}'
```

---

## Execution Logging

This agent uses **deterministic lifecycle logging**.

**Events logged:**
- `subagent:productspecs-validation-orchestrator:started`
- `subagent:productspecs-validation-orchestrator:completed`
- `subagent:productspecs-validation-orchestrator:stopped`

**Log file:** `_state/lifecycle.json`

---

## Input Requirements

```yaml
required:
  - system_name: "SystemName"
  - output_path: "ProductSpecs_{SystemName}/"
  - module_registry_path: "traceability/module_registry.json"
  - test_registry_path: "traceability/test_case_registry.json"
```

---

## Execution Flow

### Phase 1: Spawn Validation Agents (Parallel)

**Strategy**: Spawn all 3 validators concurrently

```javascript
const tasks = [
  // 1. Traceability Validator
  Task({
    subagent_type: "general-purpose",
    model: "haiku",
    description: "Validate traceability chains",
    prompt: `Agent: productspecs-traceability-validator
      Read: .claude/agents/productspecs-traceability-validator.md

      Validate complete traceability chains:
      - PP→JTBD→REQ→MOD→TC
      - 100% P0 coverage required
      - 90% P1 coverage required
      - 80% P2 coverage required

      Generate:
      - 00-overview/traceability-validation.md
      - 00-overview/TRACEABILITY_MATRIX.md
      - traceability/productspecs_traceability_register.json

      Return JSON: {p0_coverage: N, p1_coverage: N, p2_coverage: N, dangling_refs: N, status: "pass|fail"}`
  }),

  // 2. Cross-Reference Validator
  Task({
    subagent_type: "general-purpose",
    model: "haiku",
    description: "Validate ID reference integrity",
    prompt: `Agent: productspecs-cross-reference-validator
      Read: .claude/agents/productspecs-cross-reference-validator.md

      Validate ID reference integrity across all ProductSpecs artifacts:
      - All referenced IDs exist
      - No circular dependencies
      - No dangling references
      - Proper ID format

      Generate:
      - 00-overview/cross-ref-report.md
      - 00-overview/id-registry.md

      Return JSON: {dangling_refs: [], circular_deps: [], format_errors: [], status: "pass|fail"}`
  }),

  // 3. Spec Reviewer
  Task({
    subagent_type: "general-purpose",
    model: "sonnet",
    description: "Review spec completeness",
    prompt: `Agent: productspecs-spec-reviewer
      Read: .claude/agents/productspecs-spec-reviewer.md

      Review spec completeness and quality:
      - All modules have acceptance criteria
      - All modules have user stories
      - All modules have technical requirements
      - Clarity and implementability
      - Min quality score: 70

      Generate:
      - 00-overview/review-findings.md
      - 00-overview/quality-scorecard.md

      Return JSON: {avg_quality_score: N, modules_below_threshold: [], status: "pass|fail"}`
  })
];

// Wait for all validators to complete
const results = await Promise.all(tasks);
```

---

### Phase 2: Analyze Validation Results

**Purpose**: Check if blocking criteria are met

```javascript
// Extract results
const [trace_result, xref_result, review_result] = results;

// Check blocking criteria
const blocking_issues = [];

// Criterion 1: P0 Coverage
if (trace_result.p0_coverage < 100) {
  blocking_issues.push({
    criterion: "P0 Coverage",
    required: 100,
    actual: trace_result.p0_coverage,
    severity: "CRITICAL",
    message: `P0 coverage is ${trace_result.p0_coverage}% (required: 100%)`
  });
}

// Criterion 2: Dangling References
const total_dangling = trace_result.dangling_refs + xref_result.dangling_refs.length;
if (total_dangling > 0) {
  blocking_issues.push({
    criterion: "Dangling References",
    required: 0,
    actual: total_dangling,
    severity: "CRITICAL",
    message: `Found ${total_dangling} dangling references`
  });
}

// Criterion 3: Min Quality Score
if (review_result.avg_quality_score < 70) {
  blocking_issues.push({
    criterion: "Quality Score",
    required: 70,
    actual: review_result.avg_quality_score,
    severity: "CRITICAL",
    message: `Average quality score is ${review_result.avg_quality_score} (required: 70)`
  });
}

// Criterion 4: Circular Dependencies
if (xref_result.circular_deps.length > 0) {
  blocking_issues.push({
    criterion: "Circular Dependencies",
    required: 0,
    actual: xref_result.circular_deps.length,
    severity: "WARNING",
    message: `Found ${xref_result.circular_deps.length} circular dependencies`
  });
}
```

---

### Phase 3: Generate Blocking Gate Report

**Purpose**: Document validation results and blocking issues

```bash
# Generate blocking gate report
cat > ProductSpecs_${SystemName}/00-overview/blocking-gate-report.md <<EOF
# Blocking Gate Report - CP-7

**System**: ${SystemName}
**Date**: $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Status**: ${GATE_STATUS}

---

## Validation Results

### 1. Traceability Validation

| Priority | Coverage | Required | Status |
|----------|----------|----------|--------|
| P0 | ${p0_coverage}% | 100% | ${p0_status} |
| P1 | ${p1_coverage}% | 90% | ${p1_status} |
| P2 | ${p2_coverage}% | 80% | ${p2_status} |

**Dangling References**: ${dangling_refs}

---

### 2. Cross-Reference Validation

| Check | Count | Status |
|-------|-------|--------|
| Dangling References | ${dangling_refs} | ${xref_status} |
| Circular Dependencies | ${circular_deps} | ${circ_status} |
| Format Errors | ${format_errors} | ${format_status} |

---

### 3. Spec Quality Review

| Metric | Value | Required | Status |
|--------|-------|----------|--------|
| Average Quality Score | ${avg_score} | ≥70 | ${quality_status} |
| Modules Below Threshold | ${modules_below} | 0 | ${threshold_status} |

---

## Blocking Issues

${blocking_issues_list}

---

## Recommendations

${recommendations}

---

## Action Required

${action_items}
EOF

# Log version history for blocking gate report
python3 .claude/hooks/version_history_logger.py \
  "traceability/" \
  "${SystemName}" \
  "productspecs" \
  "Claude" \
  "$(cat .claude/version.json | jq -r '.version')" \
  "Generated CP-7 blocking gate report: ${GATE_STATUS}" \
  "CP-7" \
  "ProductSpecs_${SystemName}/00-overview/blocking-gate-report.md" \
  "creation"
```

---

### Phase 4: Block or Proceed

```bash
# Check blocking criteria and run final quality gate
if [ ${P0_COVERAGE} -lt 100 ] || [ ${DANGLING_REFS} -gt 0 ] || [ ${AVG_QUALITY_SCORE} -lt 70 ]; then
  # BLOCK progression
  GATE_STATUS="BLOCKED"
  echo "❌ BLOCKED: CP-7 validation failed"

  # Log blocking
  python3 .claude/hooks/version_history_logger.py \
    "traceability/" \
    "${SystemName}" \
    "productspecs" \
    "Claude" \
    "$(cat .claude/version.json | jq -r '.version')" \
    "CP-7 BLOCKED: P0=${P0_COVERAGE}%, dangling=${DANGLING_REFS}, quality=${AVG_QUALITY_SCORE}" \
    "CP-7-BLOCKED" \
    "ProductSpecs_${SystemName}/00-overview/blocking-gate-report.md" \
    "modification"

  return {
    "status": "BLOCKED",
    "checkpoint": 7,
    "blocking_issues": blocking_issues,
    "message": "ProductSpecs CP-7 validation FAILED. Cannot proceed to CP-8 (Export).",
    "action_required": "Fix blocking issues and re-run validation."
  }
else
  # PASS - allow progression
  GATE_STATUS="PASS"
  echo "✅ PASS: All validation gates passed"

  # Run final quality gate validation
  python3 .claude/hooks/productspecs_quality_gates.py \
    --validate-checkpoint 7 \
    --dir "ProductSpecs_${SystemName}/"

  if [ $? -ne 0 ]; then
    echo "⚠️ Quality gate warnings detected (non-blocking)"
  fi

  # Log success
  python3 .claude/hooks/version_history_logger.py \
    "traceability/" \
    "${SystemName}" \
    "productspecs" \
    "Claude" \
    "$(cat .claude/version.json | jq -r '.version')" \
    "CP-7 PASSED: P0=100%, dangling=0, quality=${AVG_QUALITY_SCORE}" \
    "CP-7-PASS" \
    "ProductSpecs_${SystemName}/00-overview/blocking-gate-report.md" \
    "modification"

  return {
    "status": "PASS",
    "checkpoint": 7,
    "blocking_issues": [],
    "message": "ProductSpecs CP-7 validation PASSED. Ready to proceed to CP-8 (Export).",
    "validation_results": {
      "p0_coverage": ${P0_COVERAGE},
      "dangling_refs": ${DANGLING_REFS},
      "avg_quality_score": ${AVG_QUALITY_SCORE}
    }
  }
fi
```

---

## Blocking Criteria (Detailed)

### Critical Criteria (MUST PASS)

| Criterion | Required | Severity | Blocking |
|-----------|----------|----------|----------|
| P0 Coverage | 100% | CRITICAL | ✅ YES |
| Dangling References | 0 | CRITICAL | ✅ YES |
| Min Quality Score | ≥70 | CRITICAL | ✅ YES |

### Warning Criteria (NON-BLOCKING)

| Criterion | Required | Severity | Blocking |
|-----------|----------|----------|----------|
| P1 Coverage | ≥90% | WARNING | ❌ NO |
| P2 Coverage | ≥80% | WARNING | ❌ NO |
| Circular Dependencies | 0 | WARNING | ❌ NO |

---

## Error Handling

### If Validator Fails

```json
{
  "status": "ERROR",
  "validator": "traceability-validator",
  "error": "Validator timed out after 180s",
  "action": "Retry validation or investigate validator error"
}
```

**Action**: Retry validation with extended timeout

---

### If Registries Not Found

```json
{
  "status": "ERROR",
  "error": "Module registry not found: traceability/module_registry.json",
  "action": "Ensure CP-3-4 (Module Generation) completed successfully"
}
```

**Action**: BLOCK and require previous checkpoints to complete

---

## Output Artifacts

| Artifact | Location | Description |
|----------|----------|-------------|
| Traceability Validation | `00-overview/traceability-validation.md` | Traceability chain validation report |
| Traceability Matrix | `00-overview/TRACEABILITY_MATRIX.md` | Complete traceability matrix |
| Cross-Ref Report | `00-overview/cross-ref-report.md` | ID reference integrity report |
| ID Registry | `00-overview/id-registry.md` | Complete ID registry |
| Review Findings | `00-overview/review-findings.md` | Spec quality review findings |
| Quality Scorecard | `00-overview/quality-scorecard.md` | Per-module quality scores |
| Blocking Gate Report | `00-overview/blocking-gate-report.md` | CP-7 blocking gate report |
| Traceability Register | `traceability/productspecs_traceability_register.json` | Consolidated traceability data |

---

## Coordination with Master Orchestrator

**Input from Master**:
```json
{
  "command": "spawn_validation_orchestrator",
  "system_name": "InventorySystem",
  "module_registry_path": "traceability/module_registry.json",
  "test_registry_path": "traceability/test_case_registry.json"
}
```

**Output to Master (PASS)**:
```json
{
  "status": "PASS",
  "checkpoint": 7,
  "blocking_issues": [],
  "validation_results": {
    "p0_coverage": 100,
    "dangling_refs": 0,
    "avg_quality_score": 87
  },
  "files_written": [
    "00-overview/traceability-validation.md",
    "00-overview/TRACEABILITY_MATRIX.md",
    "00-overview/blocking-gate-report.md"
  ]
}
```

**Output to Master (BLOCKED)**:
```json
{
  "status": "BLOCKED",
  "checkpoint": 7,
  "blocking_issues": [
    {
      "criterion": "P0 Coverage",
      "required": 100,
      "actual": 95,
      "severity": "CRITICAL",
      "message": "P0 coverage is 95% (required: 100%)"
    }
  ],
  "action_required": "Fix P0 coverage gaps in modules: MOD-INV-SEARCH-01, MOD-INV-API-02"
}
```

---

## Performance Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Parallel Speedup | 2.5x | 3 validators run concurrently |
| Validation Time | <3 min | Total validation time |
| False Positive Rate | <2% | Incorrect blocking |

---

## Exit Criteria

✅ **PASS**:
- All critical criteria met
- Blocking gate report generated
- Ready to proceed to CP-8

❌ **BLOCKED**:
- ≥1 critical criterion failed
- Action items logged
- Pipeline MUST NOT proceed to CP-8

---

## Usage Example

```javascript
// Main session spawns validation orchestrator
const result = await Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Coordinate validation",
  prompt: `Agent: productspecs-validation-orchestrator
    Read: .claude/agents/productspecs-validation-orchestrator.md

    Perform blocking gate validation:
    - System: InventorySystem
    - Module registry: traceability/module_registry.json
    - Test registry: traceability/test_case_registry.json

    Spawn 3 validators in parallel and check blocking criteria.
    Return JSON with status (PASS or BLOCKED).`
});

if (result.status === "BLOCKED") {
  console.error(`❌ Validation BLOCKED: ${result.blocking_issues.length} issues`);
  process.exit(1);
} else {
  console.log(`✅ Validation PASSED: Ready for CP-8 (Export)`);
}
```

---

## Related Agents

- **productspecs-orchestrator**: Master orchestrator that spawns this sub-orchestrator
- **productspecs-traceability-validator**: Spawned by this orchestrator (Haiku)
- **productspecs-cross-reference-validator**: Spawned by this orchestrator (Haiku)
- **productspecs-spec-reviewer**: Spawned by this orchestrator (Sonnet)

---

## Notes

1. **Blocking Gate**: This is the FINAL quality gate before JIRA export
2. **No Retries**: Validation orchestrator does NOT fix issues (requires human intervention or re-running CP-3-4)
3. **Critical vs Warning**: Only CRITICAL issues block progression
4. **Parallel Execution**: All 3 validators run concurrently for speed
