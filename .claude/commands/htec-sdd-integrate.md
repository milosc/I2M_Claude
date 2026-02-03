---
name: htec-sdd-integrate
description: Validate cross-module integration and E2E flows
argument-hint: None
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-integrate started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-integrate ended '{"stage": "implementation"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "implementation"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /htec-sdd-integrate instruction_start '{"stage": "implementation", "method": "instruction-based"}'
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
/htec-sdd-integrate <SystemName>
/htec-sdd-integrate <SystemName> --e2e
/htec-sdd-integrate <SystemName> --api-only
```

## Arguments

- `SystemName`: Name of the system (e.g., InventorySystem)

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--e2e` | Run E2E tests with Playwright | true |
| `--api-only` | API contract tests only | false |
| `--smoke` | Quick smoke test suite | false |
| `--performance` | Include performance baseline | false |

## Prerequisites

- Checkpoint 6 (Code Review) passed
- All P0 tasks completed

## Procedure

### 1. Setup Test Environment

```
VERIFY test environment:
    - Test database available
    - Mock API server configured
    - Browser automation ready (if --e2e)

READ Implementation_<System>/04-implementation/api-contracts.json
READ SolArch_<System>/06-runtime/api-design.md
```

### 2. Cross-Module Integration Tests

```
FOR EACH module_pair IN dependency_graph:
    GENERATE integration test:
        - Module A calls Module B
        - Verify data flow
        - Check error propagation

    CREATE tests/integration/<moduleA>-<moduleB>.test.ts

RUN: vitest run tests/integration/
```

### 3. API Contract Validation

```
FOR EACH endpoint IN api-contracts.json:
    VERIFY:
        - Request shape matches contract
        - Response shape matches contract
        - Error responses follow standard
        - Status codes are correct

CREATE Implementation_<System>/reports/API_CONTRACT_VALIDATION.md
```

### 4. E2E Smoke Tests

```
IF --e2e:
    FOR EACH critical_flow:
        - Login flow
        - Main CRUD operations
        - Error handling flows

    CREATE tests/e2e/<flow>.spec.ts

    RUN: npx playwright test
```

### 5. Performance Baseline (if --performance)

```
MEASURE:
    - Page load times
    - API response times
    - Bundle size
    - Memory usage

CREATE Implementation_<System>/reports/PERFORMANCE_BASELINE.md
```

### 6. Generate Report

```markdown
<!-- Implementation_<System>/reports/INTEGRATION_REPORT.md -->

# Integration Test Report

## System: InventorySystem
## Date: <Date>

## Summary

| Category | Passed | Failed | Skipped |
|----------|--------|--------|---------|
| Cross-module | 24 | 0 | 2 |
| API contracts | 47 | 0 | 0 |
| E2E smoke | 8 | 0 | 0 |

## Cross-Module Integration

### Auth → Inventory
- ✓ Authenticated user can list inventory
- ✓ Unauthenticated user is redirected
- ✓ Token refresh works during session

### Inventory → Reporting
- ✓ Export generates correct format
- ✓ Large dataset pagination works
...

## API Contract Validation

All 47 endpoints validated:
- ✓ GET /api/inventory
- ✓ POST /api/inventory
- ✓ PUT /api/inventory/:id
...

## E2E Smoke Tests

- ✓ Login with valid credentials (2.3s)
- ✓ Create inventory item (1.8s)
- ✓ Search inventory (0.9s)
...

## Performance Baseline

| Metric | Value | Target |
|--------|-------|--------|
| First Load | 1.2s | < 2s |
| API P95 | 180ms | < 300ms |
| Bundle Size | 245KB | < 500KB |
```

## Output

```
Integration Testing Complete
═══════════════════════════════════════

Cross-Module Tests: 24/24 passed
API Contract Tests: 47/47 passed
E2E Smoke Tests: 8/8 passed

Performance:
  First Load: 1.2s ✓
  API P95: 180ms ✓
  Bundle: 245KB ✓

Checkpoint 7: PASSED

Reports:
  • reports/INTEGRATION_REPORT.md
  • reports/API_CONTRACT_VALIDATION.md
  • reports/PERFORMANCE_BASELINE.md

Next: Run /htec-sdd-finalize
```

## Skills Used

- `Implementation_Integrator`
- `Implementation_E2ETester`


---

## Related Commands

- `/htec-sdd-review` - Previous checkpoint
- `/htec-sdd-finalize` - Next step
