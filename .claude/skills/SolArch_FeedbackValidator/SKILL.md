---
name: validating-solarch-feedback
description: Use when you need to validate that Solution Architecture feedback implementation matches the approved plan with full verification of file integrity and traceability.
model: haiku
allowed-tools: Bash, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-solarch-feedback started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-solarch-feedback ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-solarch-feedback instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

---

# SolArch_FeedbackValidator

Validation of Solution Architecture feedback implementation.

## Purpose

Validates that feedback implementation was executed correctly, verifying plan compliance, file integrity, version updates, traceability chain integrity, and ADR consistency.

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
- output files created (validation reports)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "validating-solarch-feedback"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "validating-solarch-feedback" --stage solarch
```

Logging is handled automatically by the skill framework. No user action required.

---

## When to Use

- After implementation phase completes
- To verify changes were applied correctly
- To check traceability chain integrity
- Before marking feedback as completed

## Input Requirements

```json
{
  "feedback_id": "SF-001",
  "system_name": "InventorySystem"
}
```

## Output Files

### Validation Report

Location: `SolArch_<SystemName>/feedback-sessions/<session>/VALIDATION_REPORT.md`

```markdown
---
feedback_id: SF-001
validation_timestamp: 2025-12-22T11:15:00Z
result: PASSED
---

# Validation Report

## Summary

| Check | Status | Details |
|-------|--------|---------|
| Plan Compliance | ✅ Passed | 5/5 steps completed |
| File Integrity | ✅ Passed | All files valid |
| Version Updates | ✅ Passed | Versions incremented |
| Traceability | ✅ Passed | All chains intact |
| ADR Consistency | ✅ Passed | Cross-references valid |
| **Overall** | ✅ PASSED | |

## Detailed Results

### 1. Plan Compliance

**Status**: ✅ Passed

| Step | Planned | Executed | Result |
|------|---------|----------|--------|
| 1 | Modify ADR-001 | ✅ Completed | Changes applied |
| 2 | Update decisions.json | ✅ Completed | Registry updated |
| 3 | Review solution-strategy.md | ✅ Completed | No changes needed |

**Unexpected Changes**: None

### 2. File Integrity

**Status**: ✅ Passed

| File | Readable | Parseable | Valid Structure |
|------|----------|-----------|-----------------|
| ADR-001-architecture-style.md | ✅ | ✅ | ✅ |
| decisions.json | ✅ | ✅ | ✅ |

**Issues Found**: None

### 3. Version Updates

**Status**: ✅ Passed

| File | Previous | Current | Valid |
|------|----------|---------|-------|
| ADR-001 | 1.0.0 | 1.1.0 | ✅ |

**Version Conflicts**: None

### 4. Traceability Chain Integrity

**Status**: ✅ Passed

| Chain | Nodes | Status |
|-------|-------|--------|
| PP-1.1 → ADR-001 → COMP-CORE | 3 | ✅ Intact |
| PP-2.1 → ADR-001 → COMP-CORE | 3 | ✅ Intact |
| REQ-001 → ADR-001 | 2 | ✅ Intact |

**Broken Chains**: None

### 5. ADR Consistency

**Status**: ✅ Passed

| Check | Result |
|-------|--------|
| Required sections present | ✅ |
| Status field valid | ✅ |
| Traceability section present | ✅ |
| Cross-references valid | ✅ |

**Issues**: None

## Recommendations

No issues found. Implementation validated successfully.

## Quality Gate

```bash
python3 .claude/hooks/solarch_quality_gates.py --validate-feedback SF-001 --dir SolArch_InventorySystem/
```

**Result**: ✅ PASSED
```

## Procedures

### 1. Validate Implementation

```
PROCEDURE validate_implementation(feedback_id, system_name):

  session_path = get_session_path(feedback_id, system_name)

  results = {
    plan_compliance: null,
    file_integrity: null,
    version_updates: null,
    traceability: null,
    adr_consistency: null,
    overall: null
  }

  # Run all validations
  results.plan_compliance = validate_plan_compliance(session_path)
  results.file_integrity = validate_file_integrity(session_path, system_name)
  results.version_updates = validate_version_updates(session_path, system_name)
  results.traceability = validate_traceability(session_path, system_name)
  results.adr_consistency = validate_adr_consistency(system_name)

  # Determine overall result
  results.overall = all_passed(results)

  # Generate report
  GENERATE VALIDATION_REPORT.md

  # Update registry
  UPDATE registry:
    IF results.overall == "PASSED":
      status = "completed"
      validation.passed = true
    ELSE:
      status = "failed"
      validation.passed = false

  RETURN results
```

### 2. Validate Plan Compliance

```
PROCEDURE validate_plan_compliance(session_path):

  # Read plan
  plan = READ implementation_plan.md

  # Read execution log
  log = READ implementation_log.md

  # Compare planned vs executed
  planned_steps = plan.steps
  executed_steps = parse_executed_steps(log)

  compliance = {
    passed: true,
    steps_planned: planned_steps.length,
    steps_executed: executed_steps.length,
    steps_successful: 0,
    unexpected_changes: []
  }

  FOR each planned_step IN planned_steps:
    executed = find_executed_step(executed_steps, planned_step.step_number)

    IF executed AND executed.status == "completed":
      compliance.steps_successful += 1
    ELSE:
      compliance.passed = false

  # Check for unexpected changes
  FOR each executed_step IN executed_steps:
    IF NOT in_plan(planned_steps, executed_step):
      compliance.unexpected_changes.append(executed_step)
      compliance.passed = false

  RETURN compliance
```

### 3. Validate File Integrity

```
PROCEDURE validate_file_integrity(session_path, system_name):

  # Read files changed summary
  changed = READ files_changed.md

  integrity = {
    passed: true,
    files_checked: [],
    issues: []
  }

  FOR each file IN changed.files:
    file_path = SolArch_{system_name}/{file.path}

    check = {
      file: file.path,
      readable: false,
      parseable: false,
      valid_structure: false
    }

    TRY:
      content = READ file_path
      check.readable = true

      IF file.path ENDS WITH ".json":
        parsed = JSON.parse(content)
        check.parseable = true
        check.valid_structure = validate_json_schema(parsed, file.schema)

      ELIF file.path ENDS WITH ".md":
        frontmatter, body = parse_markdown(content)
        check.parseable = true
        check.valid_structure = frontmatter IS NOT EMPTY

    CATCH error:
      integrity.issues.append({
        file: file.path,
        error: error.message
      })
      integrity.passed = false

    integrity.files_checked.append(check)

  RETURN integrity
```

### 4. Validate Version Updates

```
PROCEDURE validate_version_updates(session_path, system_name):

  # Read files changed summary
  changed = READ files_changed.md

  versions = {
    passed: true,
    updates: [],
    conflicts: []
  }

  FOR each file IN changed.files WHERE file.version_change:
    file_path = SolArch_{system_name}/{file.path}
    content = READ file_path

    # Extract current version
    IF file.path ENDS WITH ".md":
      frontmatter, _ = parse_markdown(content)
      current_version = frontmatter.version
    ELIF file.path ENDS WITH ".json":
      data = JSON.parse(content)
      current_version = data.version OR extract_item_version(data, file.entity)

    # Verify version was incremented
    expected_version = file.version_change.to
    IF current_version != expected_version:
      versions.conflicts.append({
        file: file.path,
        expected: expected_version,
        actual: current_version
      })
      versions.passed = false

    versions.updates.append({
      file: file.path,
      previous: file.version_change.from,
      current: current_version,
      valid: current_version == expected_version
    })

  RETURN versions
```

### 5. Validate Traceability

```
PROCEDURE validate_traceability(session_path, system_name):

  # Read impact analysis for affected chains
  impact = READ impact_analysis.md
  affected_chains = impact.traceability_impacts

  # Load current traceability
  trace = READ SolArch_{system_name}/_registry/architecture-traceability.json

  traceability = {
    passed: true,
    chains_checked: [],
    broken_chains: []
  }

  FOR each affected IN affected_chains:
    chain_id = affected.chain_id

    # Find chain in current state
    current_chain = find_chain(trace, chain_id)

    IF NOT current_chain:
      traceability.broken_chains.append({
        chain_id: chain_id,
        reason: "Chain not found in register"
      })
      traceability.passed = false
      CONTINUE

    # Verify all nodes exist
    FOR each node IN current_chain.nodes:
      IF NOT entity_exists(system_name, node):
        traceability.broken_chains.append({
          chain_id: chain_id,
          reason: "Node {node} does not exist"
        })
        traceability.passed = false

    traceability.chains_checked.append({
      chain_id: chain_id,
      nodes: current_chain.nodes,
      status: "intact" IF valid ELSE "broken"
    })

  RETURN traceability
```

### 6. Validate ADR Consistency

```
PROCEDURE validate_adr_consistency(system_name):

  adr_path = SolArch_{system_name}/09-decisions/
  adrs = GLOB ADR-*.md

  consistency = {
    passed: true,
    adrs_checked: [],
    issues: []
  }

  FOR each adr_file IN adrs:
    content = READ adr_file
    frontmatter, body = parse_markdown(content)

    checks = {
      file: adr_file,
      required_sections: false,
      status_valid: false,
      traceability_present: false,
      cross_references_valid: false
    }

    # Check required sections
    required = ["Status", "Context", "Decision", "Consequences"]
    checks.required_sections = all(section IN body FOR section IN required)

    # Check status validity
    valid_statuses = ["Proposed", "Accepted", "Deprecated", "Superseded"]
    checks.status_valid = frontmatter.status IN valid_statuses

    # Check traceability section
    checks.traceability_present = "Traceability" IN body OR "traceability" IN frontmatter

    # Check cross-references
    references = extract_references(body)  # ADR-XXX, PP-X.X, REQ-XXX
    checks.cross_references_valid = all_references_exist(references, system_name)

    IF NOT all(checks):
      consistency.issues.append({
        file: adr_file,
        failed_checks: get_failed_checks(checks)
      })
      consistency.passed = false

    consistency.adrs_checked.append(checks)

  RETURN consistency
```

## Validation Checks

| Check | What It Validates | Failure Impact |
|-------|-------------------|----------------|
| Plan Compliance | All planned steps executed | High |
| File Integrity | Files readable and valid | High |
| Version Updates | Versions incremented correctly | Medium |
| Traceability | Chains not broken | High |
| ADR Consistency | ADR structure valid | Medium |

## Result Statuses

| Status | Description |
|--------|-------------|
| PASSED | All checks passed |
| FAILED | One or more checks failed |
| WARNING | Passed with warnings |

## Error Handling

| Error | Action |
|-------|--------|
| Plan file missing | Fail validation |
| Log file missing | Fail validation |
| File unreadable | Log error, mark check failed |
| Chain missing | Log warning, mark check failed |

## Integration Points

### Upstream
- Runs after `SolArch_FeedbackImplementer` completes
- Uses session files from implementation phase

### Downstream
- Updates registry status via `SolArch_FeedbackRegister`
- Triggers completion summary generation

## Quality Gates Integration

```bash
# Run validation via quality gates hook
python3 .claude/hooks/solarch_quality_gates.py --validate-feedback SF-001 --dir SolArch_X/

# Expected output:
# FEEDBACK SF-001 VALIDATION: PASSED
# - Plan Compliance: ✅
# - File Integrity: ✅
# - Version Updates: ✅
# - Traceability: ✅
# - ADR Consistency: ✅
```
