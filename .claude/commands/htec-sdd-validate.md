---
description: Validate Implementation checkpoint requirements and TDD compliance
argument-hint: --checkpoint <N>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-validate started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-validate ended '{"stage": "implementation"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "implementation"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /htec-sdd-validate instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Implementation stage rules:

```bash
# Load TDD and quality gate rules
/rules-process-integrity

# Load multi-agent coordination rules (if spawning agents)
/rules-agent-coordination

# Load Traceability rules for task IDs
/rules-traceability
```

## Usage

```
/htec-sdd-validate <SystemName>
```

## Arguments

- `SystemName`: Name of the system (e.g., InventorySystem)

## This is a BLOCKING Checkpoint

Implementation cannot proceed until all validation criteria pass.

## Validation Criteria

### 1. ProductSpecs Validation

| Check | Requirement | Priority |
|-------|-------------|----------|
| Checkpoint | Must be 8+ (JIRA export complete) | CRITICAL |
| Module specs | At least 1 MOD-*.md file | CRITICAL |
| Requirements registry | `traceability/requirements_registry.json` exists | CRITICAL |
| Module index | `01-modules/module-index.md` exists | HIGH |
| Test specs | `03-tests/test-case-registry.md` exists | MEDIUM |

### 2. SolArch Validation

| Check | Requirement | Priority |
|-------|-------------|----------|
| Checkpoint | Must be 12+ (validation complete) | CRITICAL |
| ADRs | At least 9 ADR-*.md files | CRITICAL |
| C4 diagrams | Context and Container diagrams exist | HIGH |
| API design | `06-runtime/api-design.md` exists | HIGH |
| Tech stack ADR | ADR-002-technology-stack.md exists | CRITICAL |

### 3. Traceability Validation

| Check | Requirement | Priority |
|-------|-------------|----------|
| P0 coverage | 100% of P0 pain points traced to modules | CRITICAL |
| Requirements | All REQ-* linked to MOD-* | HIGH |
| Screen coverage | All screens have module mapping | MEDIUM |

## Procedure

### 1. Read Existing State

```
READ _state/productspecs_progress.json
READ _state/solarch_progress.json

EXTRACT:
    productspecs_checkpoint
    solarch_checkpoint
```

### 2. Validate ProductSpecs

```
CHECK productspecs_checkpoint >= 8
    IF FAIL: CRITICAL "ProductSpecs incomplete. Run /productspecs to complete."

GLOB ProductSpecs_<SystemName>/01-modules/MOD-*.md
    IF count == 0: CRITICAL "No module specifications found."

CHECK traceability/requirements_registry.json exists
    IF FAIL: CRITICAL "Requirements registry missing."

CHECK ProductSpecs_<SystemName>/01-modules/module-index.md exists
    IF FAIL: HIGH "Module index missing."

CHECK ProductSpecs_<SystemName>/03-tests/test-case-registry.md exists
    IF FAIL: MEDIUM "Test case registry missing."
```

### 3. Validate SolArch

```
CHECK solarch_checkpoint >= 12
    IF FAIL: CRITICAL "SolArch incomplete. Run /solarch to complete."

GLOB SolArch_<SystemName>/09-decisions/ADR-*.md
    IF count < 9: CRITICAL "Insufficient ADRs (need 9+, found {count})."

CHECK SolArch_<SystemName>/diagrams/c4-context.mermaid exists
    IF FAIL: HIGH "C4 Context diagram missing."

CHECK SolArch_<SystemName>/06-runtime/api-design.md exists
    IF FAIL: HIGH "API design document missing."

CHECK ADR-002-technology-stack.md exists
    IF FAIL: CRITICAL "Technology stack ADR missing."
```

### 4. Validate Traceability

```
READ traceability/discovery_traceability_register.json
READ traceability/productspecs_traceability_register.json

FOR EACH pain_point WHERE priority == "P0":
    CHECK has_module_mapping == true
    IF FAIL: CRITICAL "P0 pain point {PP-X.X} not traced to module."

FOR EACH requirement:
    CHECK module_refs.length > 0
    IF FAIL: HIGH "Requirement {REQ-XXX} has no module mapping."
```

### 5. Extract Technology Stack

```
READ SolArch_<SystemName>/09-decisions/ADR-002-technology-stack.md

EXTRACT:
    framework: (React, Vue, Angular, etc.)
    language: (TypeScript, JavaScript)
    test_framework: (Vitest, Jest, etc.)
    style_system: (Tailwind, CSS Modules, etc.)
    state_management: (Zustand, Redux, etc.)

UPDATE _state/implementation_config.json WITH extracted values
```

### 6. Generate Validation Report

```json
// _state/implementation_input_validation.json
{
  "validated_at": "<ISO timestamp>",
  "status": "passed" | "failed",
  "productspecs": {
    "checkpoint": 8,
    "modules_count": 12,
    "requirements_count": 47,
    "status": "valid"
  },
  "solarch": {
    "checkpoint": 12,
    "adrs_count": 11,
    "status": "valid"
  },
  "traceability": {
    "p0_coverage": 100,
    "requirement_coverage": 98,
    "status": "valid"
  },
  "tech_stack": {
    "framework": "react",
    "language": "typescript",
    "test_framework": "vitest"
  },
  "findings": []
}
```

## Output

### Success Output

```
Input Validation: PASSED
═══════════════════════════════════════

ProductSpecs:
  ✓ Checkpoint: 8 (required: 8+)
  ✓ Modules: 12 found
  ✓ Requirements registry: valid

SolArch:
  ✓ Checkpoint: 12 (required: 12+)
  ✓ ADRs: 11 found (required: 9+)
  ✓ C4 diagrams: present

Traceability:
  ✓ P0 coverage: 100%
  ✓ Requirement mapping: 98%

Tech Stack Detected:
  Framework: React + TypeScript
  Testing: Vitest
  Styling: Tailwind CSS

Next: Run /htec-sdd-tasks to decompose into tasks
```

### Failure Output

```
Input Validation: FAILED
═══════════════════════════════════════

CRITICAL Issues (must fix):
  ✗ ProductSpecs checkpoint: 6 (required: 8+)
  ✗ P0 pain point PP-1.2 not traced to module

HIGH Issues (recommended):
  ⚠ Module index missing
  ⚠ C4 Container diagram missing

To fix:
  1. Run /productspecs-finalize to complete ProductSpecs
  2. Update traceability for PP-1.2
  3. Run /htec-sdd-validate again
```


---

## Related Commands

- `/htec-sdd-init` - Must run before validate
- `/htec-sdd-tasks` - Run after validation passes
- `/productspecs` - Fix ProductSpecs issues
- `/solarch` - Fix SolArch issues
