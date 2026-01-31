---
name: Implementation Integrator
description: Use when validating cross-module integration, API contracts, and E2E flows at Checkpoint 7.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_Integrator started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_Integrator ended '{"stage": "implementation"}'
---

# Implementation Integrator

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill Implementation_Integrator instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

> **Version**: 2.0.0 | **Updated**: 2025-12-26
> **Change**: Added Applicability Check for non-UI projects - skips E2E UI tests and UI performance metrics for BACKEND_ONLY, DATABASE_ONLY, INTEGRATION project types

Orchestrates integration testing across modules, validates API contracts against specifications, and runs E2E smoke tests to verify system cohesion.

---

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:Implementation_Integrator:started` - When skill begins
- `skill:Implementation_Integrator:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Prerequisites

1. **Traceability Guard Check**: This skill invokes `Traceability_Guard` before execution.
   - If guard fails, execution stops with guidance to run `/traceability-init`.
   - Required files: `task_registry.json`, `requirements_registry.json`

2. **Checkpoint 6 Passed**: Code review complete with no critical findings
3. **All P0 Tasks Completed**: No P0 tasks with status != "completed"
4. **Test Environment**: Database, mock APIs, browser automation (if applicable) ready

## Applicability Check (Smart Obsolescence Handling)

Before executing integration tests, check the project classification:

```
READ _state/implementation_config.json
EXTRACT project_classification (FULL_STACK | BACKEND_ONLY | DATABASE_ONLY | INTEGRATION | INFRASTRUCTURE)

IF project_classification NOT IN [FULL_STACK]:
  # Non-UI project - skip UI-related integration tests
  SKIP Step 4 (E2E Smoke Tests - Playwright)
  SKIP Step 5 UI metrics (FCP, LCP, TTI, bundle size)
  FOCUS on cross-module integration and API contract validation
```

### Integration Test Applicability Matrix

| Test Category | FULL_STACK | BACKEND_ONLY | DATABASE_ONLY | INTEGRATION | INFRASTRUCTURE |
|---------------|------------|--------------|---------------|-------------|----------------|
| Step 2: Cross-Module Integration | ✅ | ✅ | ✅ | ✅ | ❌ N/A |
| Step 3: API Contract Validation | ✅ | ✅ | ❌ N/A | ✅ | ❌ N/A |
| **Step 4: E2E Smoke Tests (UI)** | **✅** | **❌ N/A** | **❌ N/A** | **❌ N/A** | **❌ N/A** |
| **Step 5: FCP/LCP/TTI Metrics** | **✅** | **❌ N/A** | **❌ N/A** | **❌ N/A** | **❌ N/A** |
| Step 5: API P50/P95/P99 Metrics | ✅ | ✅ | ❌ N/A | ✅ | ❌ N/A |
| Database Integration Tests | ✅ | ✅ | ✅ | ❌ N/A | ❌ N/A |

### Integration Report for Non-UI Projects

When E2E UI tests are skipped, include in INTEGRATION_REPORT.md:

```markdown
## E2E Smoke Tests

**Status**: NOT_APPLICABLE
**Reason**: Project classified as {PROJECT_CLASSIFICATION} - no UI layer

This test category is not applicable for non-UI projects because:
- No browser-based user interface to test
- No page navigation or UI interaction flows
- No Playwright/Cypress tests required

For API-level E2E testing, see the API Contract Validation section above.

## Performance Metrics (UI)

**Status**: NOT_APPLICABLE

UI performance metrics (FCP, LCP, TTI, bundle size) are not applicable.
API performance metrics (P50, P95, P99) are reported in API Contract Validation.
```

### Blocking Criteria Adjustment

For non-UI projects, the blocking criteria focus on applicable tests:
- Cross-module integration tests must pass
- API contract validation must pass
- API performance within thresholds

E2E UI tests and UI performance metrics are NOT blocking for non-UI projects.

## State Management

### Read State

```
READ _state/implementation_config.json:
    - system_name
    - source_paths (ProductSpecs, SolArch)

READ _state/implementation_progress.json:
    - current_checkpoint (must be >= 6)
    - metrics.tasks_completed

READ traceability/task_registry.json:
    - tasks (for dependency graph)
```

### Update State

```
ON COMPLETION:
    UPDATE _state/implementation_progress.json:
        current_checkpoint: 7
        cp7_integration_completed: true
        cp7_completed_at: "<ISO timestamp>"
        metrics.integration_tests_passed: <count>
        metrics.api_contracts_validated: <count>
        metrics.e2e_tests_passed: <count>
```

## Procedure

### Step 0: Guard Check

```
INVOKE Traceability_Guard WITH required_files:
    - "task_registry.json"
    - "requirements_registry.json"

IF NOT guard.valid:
    STOP and show guard.user_action_required
```

### Step 1: Build Dependency Graph

```
READ traceability/task_registry.json

BUILD module_dependency_graph:
    FOR EACH task IN tasks:
        EXTRACT module_ref from task.module_ref
        EXTRACT dependencies from task.dependencies
        ADD edges: module -> dependency_module

IDENTIFY integration_pairs:
    - Modules with cross-dependencies
    - Data flow paths (input -> processing -> output)

OUTPUT:
    dependency_graph: { module_id: [dependent_modules] }
    integration_pairs: [[moduleA, moduleB], ...]
```

### Step 2: Cross-Module Integration Tests

```
FOR EACH [moduleA, moduleB] IN integration_pairs:
    IDENTIFY:
        - Shared interfaces
        - Data contracts
        - Error propagation paths

    CREATE tests/integration/<moduleA>-<moduleB>.test.ts:
```

```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { setupTestDb, teardownTestDb } from '@/test-utils';
import { ModuleAService } from '@/services/module-a';
import { ModuleBService } from '@/services/module-b';

describe('ModuleA -> ModuleB Integration', () => {
  beforeAll(async () => {
    await setupTestDb();
  });

  afterAll(async () => {
    await teardownTestDb();
  });

  it('should pass data correctly from ModuleA to ModuleB', async () => {
    // Arrange
    const inputData = { /* test data */ };

    // Act
    const resultA = await ModuleAService.process(inputData);
    const resultB = await ModuleBService.consume(resultA.output);

    // Assert
    expect(resultB.success).toBe(true);
    expect(resultB.data).toMatchObject(expectedShape);
  });

  it('should propagate errors from ModuleA to ModuleB correctly', async () => {
    // Arrange
    const invalidData = { /* invalid test data */ };

    // Act
    const resultA = await ModuleAService.process(invalidData);
    const resultB = await ModuleBService.consume(resultA.output);

    // Assert
    expect(resultB.success).toBe(false);
    expect(resultB.error).toContain('INVALID_INPUT');
  });
});
```

```
RUN: vitest run tests/integration/ --reporter=verbose

LOG results to integration_results[]
```

### Step 3: API Contract Validation

```
READ Implementation_<System>/04-implementation/api-contracts.json
READ SolArch_<System>/06-runtime/api-design.md

FOR EACH endpoint IN api_contracts:
    CREATE contract test:
```

```typescript
import { describe, it, expect } from 'vitest';
import { request } from '@/test-utils/api-client';

describe('API Contract: GET /api/inventory', () => {
  it('should return items matching contract schema', async () => {
    const response = await request.get('/api/inventory');

    expect(response.status).toBe(200);
    expect(response.body).toMatchSchema(inventoryListSchema);
  });

  it('should return 401 for unauthenticated request', async () => {
    const response = await request.get('/api/inventory', { auth: false });

    expect(response.status).toBe(401);
    expect(response.body.error).toBe('UNAUTHORIZED');
  });

  it('should support pagination parameters', async () => {
    const response = await request.get('/api/inventory?page=1&limit=10');

    expect(response.body.data.length).toBeLessThanOrEqual(10);
    expect(response.body.pagination).toMatchObject({
      page: 1,
      limit: 10,
      total: expect.any(Number)
    });
  });
});
```

```
RUN: vitest run tests/contracts/

CREATE Implementation_<System>/reports/API_CONTRACT_VALIDATION.md:
    - Endpoint list with status
    - Schema validation results
    - Any mismatches found
```

### Step 4: E2E Smoke Tests

```
IF config.run_e2e (default: true):

    IDENTIFY critical_flows from Prototype_<System>/02-screens/:
        - Login/Auth flow
        - Primary CRUD operations
        - Error handling flows
        - Navigation flows

    FOR EACH flow IN critical_flows:
        CREATE tests/e2e/<flow>.spec.ts:
```

```typescript
import { test, expect } from '@playwright/test';

test.describe('Login Flow', () => {
  test('should login with valid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[data-testid="email"]', 'test@example.com');
    await page.fill('[data-testid="password"]', 'password123');
    await page.click('[data-testid="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[data-testid="email"]', 'test@example.com');
    await page.fill('[data-testid="password"]', 'wrongpassword');
    await page.click('[data-testid="submit"]');

    await expect(page.locator('[data-testid="error-message"]')).toContainText('Invalid credentials');
  });
});
```

```
RUN: npx playwright test --reporter=html

LOG results to e2e_results[]
```

### Step 5: Performance Baseline (Optional)

```
IF config.run_performance:

    MEASURE metrics:
        - First Contentful Paint (FCP)
        - Largest Contentful Paint (LCP)
        - Time to Interactive (TTI)
        - API response P50, P95, P99
        - Bundle size (main, vendor, total)
        - Memory usage patterns

    CREATE Implementation_<System>/reports/PERFORMANCE_BASELINE.md:
        | Metric | Value | Target | Status |
        |--------|-------|--------|--------|
        | FCP | 1.2s | < 2s | PASS |
        | LCP | 2.1s | < 2.5s | PASS |
        | Bundle | 245KB | < 500KB | PASS |
```

### Step 6: Generate Integration Report

```
CREATE Implementation_<System>/reports/INTEGRATION_REPORT.md:
```

```markdown
# Integration Test Report

## System: <SystemName>
## Checkpoint: 7
## Date: <ISO Date>

## Summary

| Category | Passed | Failed | Skipped |
|----------|--------|--------|---------|
| Cross-module | <count> | <count> | <count> |
| API contracts | <count> | <count> | <count> |
| E2E smoke | <count> | <count> | <count> |

## Cross-Module Integration

<FOR EACH integration_pair>
### <ModuleA> -> <ModuleB>
- <test results with checkmarks>
</FOR EACH>

## API Contract Validation

<endpoint list with validation status>

## E2E Smoke Tests

<test results with timing>

## Performance Baseline

<metrics table if run>

## Traceability

| Source | Target | Coverage |
|--------|--------|----------|
| Requirements -> Integration Tests | <percentage> |
| Screens -> E2E Tests | <percentage> |
```

### Step 7: Update State and Registry

```
UPDATE _state/implementation_progress.json:
    current_checkpoint: 7
    cp7_integration_completed: true
    cp7_completed_at: "<ISO timestamp>"
    metrics.integration_tests_passed: <count>
    metrics.api_contracts_validated: <count>
    metrics.e2e_tests_passed: <count>

UPDATE traceability/task_registry.json:
    integration_checkpoint: {
        status: "passed",
        date: "<ISO timestamp>",
        integration_tests: <count>,
        api_validations: <count>,
        e2e_tests: <count>
    }
```

## Blocking Criteria

Integration testing **BLOCKS** if:

1. **Critical Integration Failure**: Cross-module data flow broken
2. **API Contract Mismatch**: Response schema doesn't match contract
3. **E2E Critical Flow Failure**: Login or primary CRUD broken
4. **P0 Regression**: Any P0 functionality regressed

## Error Handling

| Situation | Action |
|-----------|--------|
| Test environment unavailable | Log, skip tests requiring env, continue |
| Single test failure | Log, continue with other tests |
| Contract mismatch | Log detailed diff, flag for review |
| Playwright timeout | Retry once, then skip with warning |
| Performance miss | Log as warning, don't block (unless critical) |

## Output Files

```
Implementation_<System>/
├── tests/
│   ├── integration/
│   │   └── <moduleA>-<moduleB>.test.ts
│   ├── contracts/
│   │   └── <endpoint>.test.ts
│   └── e2e/
│       └── <flow>.spec.ts
└── reports/
    ├── INTEGRATION_REPORT.md
    ├── API_CONTRACT_VALIDATION.md
    └── PERFORMANCE_BASELINE.md (optional)
```

## Traceability Chain

```
Requirements (REQ-XXX)
    ↓
Tasks (T-NNN)
    ↓
Unit Tests (task.tdd_spec.test_file)
    ↓
Integration Tests (tests/integration/*.test.ts)  ← THIS SKILL
    ↓
E2E Tests (tests/e2e/*.spec.ts)  ← THIS SKILL
    ↓
Validation Report (reports/INTEGRATION_REPORT.md)
```

## Related Skills

- `Implementation_Developer` - Creates unit tests (feeds into this)
- `Implementation_CodeReview` - Reviews before integration
- `Implementation_Validator` - Final validation after this
