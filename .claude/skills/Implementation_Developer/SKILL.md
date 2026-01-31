---
name: Implementation Developer
description: Use when executing implementation tasks using Test-Driven Development (TDD) protocol with the RED-GREEN-REFACTOR cycle.
model: sonnet
allowed-tools: Read, Write, Edit, Bash
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_Developer started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_Developer ended '{"stage": "implementation"}'
---

# Implementation Developer

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill Implementation_Developer instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

Executes implementation tasks following strict TDD protocol. Each task goes through RED (failing test) → GREEN (minimal implementation) → REFACTOR (clean up) → VERIFY (full suite) → MARK (update registry).

---

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:Implementation_Developer:started` - When skill begins
- `skill:Implementation_Developer:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Prerequisites

1. **Traceability Guard Check**: This skill invokes `Traceability_Guard` before execution.
   - If guard fails, execution stops with guidance to run `/traceability-init`.
   - Required files: `task_registry.json`

2. **Tasks Decomposed**: `traceability/task_registry.json` populated
3. **Tech Stack Known**: ADR-002 technology decisions available
4. **Patterns Defined**: Error handling, API patterns from ADRs

## TDD Protocol

```
┌─────────────────────────────────────────────────────────────┐
│                     TDD CYCLE                                │
├─────────────────────────────────────────────────────────────┤
│  1. RED      │ Write failing tests for acceptance criteria  │
│  2. GREEN    │ Write minimal code to pass tests             │
│  3. REFACTOR │ Clean up code while keeping tests green      │
│  4. VERIFY   │ Run full test suite, check coverage          │
│  5. MARK     │ Update task registry, log completion         │
└─────────────────────────────────────────────────────────────┘
```

## Procedure

### Step 0: Load Task Context

```
READ task from traceability/task_registry.json
READ related module: ProductSpecs_<System>/01-modules/<module_ref>.md
READ tech stack: SolArch_<System>/09-decisions/ADR-002-technology-stack.md
READ patterns: SolArch_<System>/09-decisions/ADR-007-error-handling.md

EXTRACT:
    - Acceptance criteria
    - TDD specifications
    - Implementation notes
    - Dependencies
```

### Step 1: RED - Write Failing Tests

```
CREATE test file at task.tdd_spec.test_file

IMPORT required testing utilities:
    - describe, it, expect from vitest
    - render, screen from @testing-library/react (if component)
    - Mock utilities as needed

FOR EACH acceptance_criterion IN task.acceptance_criteria:
    WRITE test case:
        - Name: "should <criterion description>"
        - Arrange: Setup test data and mocks
        - Act: Call the function/render component
        - Assert: Verify expected behavior

EXAMPLE TEST STRUCTURE:
```

```typescript
import { describe, it, expect, vi } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useBarcodeScanner } from './use-barcode-scanner';

describe('useBarcodeScanner', () => {
  // AC-1: Scan and decode EAN-13 barcodes
  it('should decode valid EAN-13 barcode', async () => {
    const { result } = renderHook(() => useBarcodeScanner());

    const scanResult = await result.current.scan('4006381333931');

    expect(scanResult.success).toBe(true);
    expect(scanResult.format).toBe('EAN-13');
    expect(scanResult.data).toBe('4006381333931');
  });

  // AC-2: Handle invalid barcodes gracefully
  it('should return error for invalid barcode', async () => {
    const { result } = renderHook(() => useBarcodeScanner());

    const scanResult = await result.current.scan('invalid');

    expect(scanResult.success).toBe(false);
    expect(scanResult.error).toBe('INVALID_FORMAT');
  });
});
```

```
RUN: vitest run <test_file> --reporter=verbose

VERIFY all tests FAIL:
    ✗ should decode valid EAN-13 barcode
    ✗ should return error for invalid barcode

IF tests pass unexpectedly:
    REVIEW: Functionality may already exist
    ADJUST: Tests or task scope
```

### Step 2: GREEN - Minimal Implementation

```
ANALYZE test requirements:
    - What functions/components need to exist?
    - What interfaces/types are needed?
    - What external dependencies are required?

CREATE/MODIFY source files:
    - Follow project structure conventions
    - Implement ONLY what's needed to pass tests
    - No premature optimization
    - No extra features

EXAMPLE IMPLEMENTATION:
```

```typescript
// src/features/inventory/hooks/use-barcode-scanner.ts

import { useState, useCallback } from 'react';

interface ScanResult {
  success: boolean;
  format?: string;
  data?: string;
  error?: string;
}

export function useBarcodeScanner() {
  const [isScanning, setIsScanning] = useState(false);

  const scan = useCallback(async (input: string): Promise<ScanResult> => {
    // Validate EAN-13 format (13 digits)
    if (!/^\d{13}$/.test(input)) {
      return { success: false, error: 'INVALID_FORMAT' };
    }

    return {
      success: true,
      format: 'EAN-13',
      data: input,
    };
  }, []);

  return { scan, isScanning };
}
```

```
RUN: vitest run <test_file>

VERIFY all tests PASS:
    ✓ should decode valid EAN-13 barcode
    ✓ should return error for invalid barcode

IF tests fail:
    DEBUG: Identify failing assertion
    FIX: Adjust implementation
    REPEAT until green
```

### Step 3: REFACTOR - Clean Up

```
REVIEW implementation for:
    □ Code duplication (DRY)
    □ Clear naming conventions
    □ Proper TypeScript types
    □ Error handling patterns (per ADR-007)
    □ Performance concerns
    □ Accessibility (if UI component)

REFACTOR while keeping tests green:
    - Extract reusable utilities
    - Improve naming
    - Add proper error boundaries
    - Optimize if obvious improvements

AFTER each refactoring step:
    RUN: vitest run <test_file>
    VERIFY: Still green
```

### Step 4: VERIFY - Full Suite

```
RUN full test suite:
    vitest run --coverage

CHECK results:
    □ No regressions in other tests
    □ Coverage meets target (default: 80%)
    □ No TypeScript errors
    □ No linting errors

RUN type check:
    tsc --noEmit

RUN linting:
    eslint src/<feature>/

IF any failures:
    FIX issues
    RETURN to Step 3 if needed
```

### Step 5: MARK - Update Registry

```
UPDATE traceability/task_registry.json:

task.status = "completed"
task.completed_at = "<ISO timestamp>"

task.implementation = {
  files_created: [
    "src/features/inventory/hooks/use-barcode-scanner.ts"
  ],
  files_modified: [],
  tests_created: [
    "tests/unit/inventory/use-barcode-scanner.test.ts"
  ],
  lines_of_code: 45,
  test_count: 2
}

FOR EACH acceptance_criterion:
    criterion.status = "passed"
    criterion.test_location = "<file>:<line>"

UPDATE _state/implementation_progress.json:
    metrics.tasks_completed += 1
    metrics.test_coverage = <new coverage>
```

## Parallel Execution Mode

When running with `--parallel`:

```
RECEIVE task assignment from orchestrator
ACQUIRE file lock for task.id

EXECUTE TDD cycle (Steps 1-5)

ON completion:
    RELEASE file lock
    SIGNAL completion to orchestrator
    RETURN {
        task_id: task.id,
        status: "completed" | "failed",
        files_created: [...],
        tests_created: [...],
        duration_ms: elapsed
    }

ON failure:
    RELEASE file lock
    LOG error to _state/FAILURES_LOG.md
    SIGNAL failure to orchestrator
```

## Code Patterns

### Following ADRs

```
BEFORE implementing, check relevant ADRs:

ADR-002 (Tech Stack):
    - React for UI
    - TypeScript for type safety
    - Vitest for testing
    - Tailwind for styling

ADR-007 (Error Handling):
    - Use Result<T, E> pattern
    - No throwing in business logic
    - Log errors with context

ADR-003 (State Management):
    - Use Zustand for global state
    - React Query for server state
    - Local state for UI-only
```

### Component Pattern

```typescript
// Standard component structure
import { FC } from 'react';
import { cn } from '@/lib/utils';

interface ComponentProps {
  // Props interface
}

export const Component: FC<ComponentProps> = ({ ...props }) => {
  // Implementation
  return (
    <div className={cn('base-styles', props.className)}>
      {/* Content */}
    </div>
  );
};
```

### Service Pattern

```typescript
// Standard service structure
import { Result, ok, err } from '@/lib/result';

export interface ServiceInput {
  // Input types
}

export interface ServiceOutput {
  // Output types
}

export async function serviceFunction(
  input: ServiceInput
): Promise<Result<ServiceOutput, ServiceError>> {
  try {
    // Implementation
    return ok(result);
  } catch (error) {
    return err(new ServiceError('MESSAGE', { cause: error }));
  }
}
```

## Quality Checks

Before marking complete:

1. **Tests Pass**: All test cases green
2. **Coverage Met**: ≥80% line coverage for new code
3. **Types Clean**: No TypeScript errors
4. **Lint Clean**: No ESLint errors
5. **AC Verified**: Every acceptance criterion has passing test
6. **Patterns Followed**: Code matches ADR guidelines

## Error Handling

| Situation | Action |
|-----------|--------|
| Test won't pass after 3 attempts | Mark blocked, log reason |
| External dependency issue | Mock dependency, continue |
| Type error in existing code | Fix or report, don't propagate |
| Coverage below target | Add edge case tests |

## Reflexion Integration

If reflexion is enabled in config:

```
AFTER completing task:
    REFLECT on implementation:
        - What patterns worked well?
        - What could be improved?
        - Any learnings for future tasks?

    IF significant learning:
        APPEND to CLAUDE.md under "## Implementation Learnings"
```

## Related Skills

- `Implementation_TaskDecomposer` - Creates tasks this skill executes
- `Implementation_CodeReview` - Reviews completed implementations
- `systematic-debugging` - Use when tests fail unexpectedly
