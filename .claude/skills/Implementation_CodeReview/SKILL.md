---
name: Implementation Code Review
description: Use when performing multi-agent code review with 6 specialized reviewers analyzing different aspects of code quality, security, and compliance.
model: sonnet
allowed-tools: Read, Write, Edit, Bash, Task
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_CodeReview started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_CodeReview ended '{"stage": "implementation"}'
---

# Implementation Code Review

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill Implementation_CodeReview instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

> **Version**: 2.0.0 | **Updated**: 2025-12-26
> **Change**: Added Applicability Check for non-UI projects - skips accessibility-auditor for BACKEND_ONLY, DATABASE_ONLY, INTEGRATION project types

Orchestrates specialized review agents to comprehensively analyze implementation code. Each agent focuses on a specific domain, running in parallel for efficiency.

---

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:Implementation_CodeReview:started` - When skill begins
- `skill:Implementation_CodeReview:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Prerequisites

1. **Traceability Guard Check**: This skill invokes `Traceability_Guard` before execution.
   - If guard fails, execution stops with guidance to run `/traceability-init`.
   - Required files: `task_registry.json`

2. **Implementation Complete**: Tasks in `traceability/task_registry.json` marked completed
3. **Source Code Available**: Code in `Implementation_<System>/src/`
4. **Tests Available**: Tests in `Implementation_<System>/tests/`

## Applicability Check (Smart Obsolescence Handling)

Before executing review agents, check the project classification:

```
READ _state/implementation_config.json
EXTRACT project_classification (FULL_STACK | BACKEND_ONLY | DATABASE_ONLY | INTEGRATION | INFRASTRUCTURE)

IF project_classification NOT IN [FULL_STACK]:
  # Non-UI project - skip accessibility agent
  SKIP accessibility-auditor agent
  RUN only 5 applicable review agents
```

### Review Agent Applicability Matrix

| Review Agent | FULL_STACK | BACKEND_ONLY | DATABASE_ONLY | INTEGRATION | INFRASTRUCTURE |
|--------------|------------|--------------|---------------|-------------|----------------|
| `bug-hunter` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `security-auditor` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `code-quality` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `test-coverage` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `contracts-reviewer` | ✅ | ✅ | ❌ N/A | ✅ | ❌ N/A |
| **`accessibility-auditor`** | **✅** | **❌ N/A** | **❌ N/A** | **❌ N/A** | **❌ N/A** |

### Review Report for Skipped Agents

When an agent is skipped due to project type, include in CODE_REVIEW.md:

```markdown
### Accessibility Auditor

**Status**: NOT_APPLICABLE
**Reason**: Project classified as {PROJECT_CLASSIFICATION} - no UI layer

This review agent is not applicable for non-UI projects because:
- No frontend components to audit
- No user-facing screens requiring WCAG compliance
- No interactive elements requiring a11y patterns

For API accessibility (OpenAPI documentation, developer experience), see the contracts-reviewer findings.
```

### Blocking Criteria Adjustment

For non-UI projects, the blocking criteria remain the same for applicable agents:
- Any CRITICAL findings exist (security, bugs)
- Any HIGH findings with confidence > 80%
- Test coverage < 80%

Accessibility findings are NOT blocking for non-UI projects since the agent is skipped.

## Review Agents

| Agent | Focus | Severity Weight |
|-------|-------|-----------------|
| `bug-hunter` | Logic errors, edge cases, null safety | HIGH |
| `security-auditor` | OWASP Top 10, injection, auth | CRITICAL |
| `code-quality` | SOLID, DRY, complexity, patterns | MEDIUM |
| `test-coverage` | Missing tests, edge cases, mocking | HIGH |
| `contracts-reviewer` | API compliance, type safety | HIGH |
| `accessibility-auditor` | WCAG, a11y patterns | MEDIUM |

## Blocking Criteria

Review BLOCKS progress if:
- Any CRITICAL findings exist
- Any HIGH findings with confidence > 80%
- Test coverage < 80%

## Procedure

### Step 1: Determine Review Scope

```
IF scope == "all":
    FILES = glob("Implementation_<System>/src/**/*.{ts,tsx}")
ELIF scope == "changed":
    FILES = get_changed_since_checkpoint(checkpoint - 1)
ELIF scope == "module":
    FILES = get_files_for_module(module_id)

EXCLUDE:
    - node_modules/
    - dist/
    - *.test.ts (reviewed separately)
    - *.d.ts
```

### Step 2: Load Review Context

```
READ _state/implementation_config.json
READ SolArch_<System>/09-decisions/ADR-*.md FOR patterns
READ ProductSpecs_<System>/02-api/api-contracts.json FOR contracts
READ existing tests FOR coverage baseline
```

### Step 3: Execute Review Agents (Parallel)

Launch all 6 agents simultaneously:

```
AGENTS = []

FOR EACH agent_type IN review_agents:
    agent = Task(
        subagent_type="Implementation_CodeReview",
        prompt=generate_agent_prompt(agent_type, FILES),
        run_in_background=true,
        model="sonnet"  # Fast, capable model for review
    )
    AGENTS.append(agent)

# Wait for all agents to complete
RESULTS = []
FOR EACH agent IN AGENTS:
    result = TaskOutput(agent.id, block=true)
    RESULTS.append(result)
```

### Step 4: Agent-Specific Analysis

#### Bug Hunter Agent

```
FOR EACH file IN FILES:
    ANALYZE for:

    1. NULL SAFETY
       - Accessing properties without null checks
       - Optional chaining missing
       - Array access without bounds check

    2. ASYNC ISSUES
       - Missing await
       - Unhandled promise rejections
       - Race conditions in state updates

    3. LOGIC ERRORS
       - Off-by-one errors
       - Incorrect conditionals
       - Type coercion issues

    4. EDGE CASES
       - Empty array/string handling
       - Zero/negative number handling
       - Boundary conditions

    OUTPUT:
    {
        "id": "BH-NNN",
        "severity": "critical|high|medium|low",
        "confidence": 0-100,
        "file": "path/to/file.ts",
        "line": 45,
        "code": "const items = result.data.items;",
        "issue": "Potential null access on result.data",
        "suggestion": "Add optional chaining: result.data?.items ?? []",
        "category": "null-safety"
    }
```

#### Security Auditor Agent

```
FOR EACH file IN FILES:
    ANALYZE for OWASP Top 10:

    1. INJECTION (A03:2021)
       - SQL/NoSQL injection
       - Command injection
       - XSS vulnerabilities

    2. BROKEN AUTH (A07:2021)
       - Hardcoded credentials
       - Insecure session handling
       - Missing auth checks

    3. SENSITIVE DATA (A02:2021)
       - PII in logs
       - Secrets in code
       - Insecure storage

    4. SECURITY MISCONFIG (A05:2021)
       - Debug mode enabled
       - Verbose errors exposed
       - Missing security headers

    OUTPUT:
    {
        "id": "SEC-NNN",
        "severity": "critical|high|medium|low",
        "confidence": 0-100,
        "file": "path/to/file.ts",
        "line": 23,
        "owasp_category": "A03:2021-Injection",
        "issue": "User input directly in query without sanitization",
        "risk": "SQL injection could expose database",
        "remediation": "Use parameterized queries or ORM"
    }
```

#### Code Quality Agent

```
FOR EACH file IN FILES:
    ANALYZE for:

    1. COMPLEXITY
       - Functions > 50 lines
       - Cyclomatic complexity > 10
       - Nesting depth > 3

    2. SOLID VIOLATIONS
       - Single Responsibility
       - Open/Closed
       - Liskov Substitution
       - Interface Segregation
       - Dependency Inversion

    3. DRY VIOLATIONS
       - Duplicate code blocks
       - Copy-paste patterns
       - Repeated logic

    4. NAMING/CLARITY
       - Poor variable names
       - Magic numbers
       - Missing comments for complex logic

    OUTPUT:
    {
        "id": "CQ-NNN",
        "severity": "medium|low",
        "confidence": 0-100,
        "file": "path/to/file.ts",
        "line": "78-120",
        "issue": "Function exceeds 50 lines (42 lines)",
        "metric": "function_length",
        "value": 42,
        "threshold": 50,
        "suggestion": "Extract validation logic to separate function"
    }
```

#### Test Coverage Agent

```
RUN: vitest run --coverage --reporter=json

ANALYZE coverage report:
    - Uncovered functions
    - Uncovered branches
    - Low coverage files

FOR EACH source_file IN FILES:
    CHECK corresponding test file exists
    CHECK test coverage >= 80%
    CHECK edge cases covered

ANALYZE test quality:
    - Tests testing mocks instead of behavior
    - Missing assertion quality
    - Incomplete arrange-act-assert

OUTPUT:
{
    "id": "TC-NNN",
    "severity": "high|medium",
    "confidence": 0-100,
    "file": "path/to/file.ts",
    "function": "processInventoryItem",
    "issue": "Function has no test coverage",
    "current_coverage": 0,
    "suggested_tests": [
        "should process valid inventory item",
        "should handle missing fields",
        "should reject invalid quantity"
    ]
}
```

#### Contracts Reviewer Agent

```
READ api-contracts.json

FOR EACH api_call IN FILES:
    VERIFY:
        - Request shape matches contract
        - Response handling matches contract
        - Error responses handled correctly
        - Status codes handled appropriately

FOR EACH type_definition:
    VERIFY:
        - Matches API contract types
        - No missing required fields
        - No extra unhandled fields

OUTPUT:
{
    "id": "CR-NNN",
    "severity": "high|medium",
    "confidence": 0-100,
    "file": "path/to/file.ts",
    "line": 34,
    "contract": "POST /api/inventory",
    "issue": "Response type missing 'updatedAt' field from contract",
    "expected": "{ id, name, quantity, updatedAt }",
    "actual": "{ id, name, quantity }"
}
```

#### Accessibility Auditor Agent

```
FOR EACH component_file IN FILES (*.tsx):
    ANALYZE for WCAG 2.1 compliance:

    1. PERCEIVABLE
       - Missing alt text
       - Poor color contrast
       - Missing labels

    2. OPERABLE
       - Keyboard navigation
       - Focus management
       - Touch targets

    3. UNDERSTANDABLE
       - Clear error messages
       - Consistent navigation
       - Input validation feedback

    4. ROBUST
       - Semantic HTML
       - ARIA usage
       - Screen reader compatibility

OUTPUT:
{
    "id": "A11Y-NNN",
    "severity": "medium|low",
    "confidence": 0-100,
    "file": "path/to/Component.tsx",
    "line": 15,
    "wcag_criterion": "1.1.1 Non-text Content",
    "issue": "Image missing alt attribute",
    "suggestion": "Add descriptive alt text or aria-hidden if decorative"
}
```

### Step 5: Consolidate Findings

```
ALL_FINDINGS = []

FOR EACH agent_result IN RESULTS:
    FOR EACH finding IN agent_result.findings:
        IF finding.confidence >= threshold:
            ALL_FINDINGS.append(finding)

# Deduplicate overlapping findings
DEDUPLICATE by file + line + similar issue

# Categorize by severity
CRITICAL_FINDINGS = filter(ALL_FINDINGS, severity == "critical")
HIGH_FINDINGS = filter(ALL_FINDINGS, severity == "high")
MEDIUM_FINDINGS = filter(ALL_FINDINGS, severity == "medium")
LOW_FINDINGS = filter(ALL_FINDINGS, severity == "low")

# Calculate blocking status
blocking = (
    len(CRITICAL_FINDINGS) > 0 OR
    any(f.confidence > 80 for f in HIGH_FINDINGS) OR
    test_coverage < 80
)
```

### Step 6: Generate Reports

#### Markdown Report

```markdown
# Code Review Report

## System: <SystemName>
## Date: <Date>
## Files Reviewed: 45
## Threshold: 70% confidence

## Summary

| Severity | Count | Blocking |
|----------|-------|----------|
| Critical | 0 | Yes |
| High | 3 | If conf > 80% |
| Medium | 8 | No |
| Low | 12 | No |

## Blocking Status: PASSED / BLOCKED

## Findings by Agent

### Security Auditor (0 findings)
No security issues found.

### Bug Hunter (2 findings)
...

[Full findings with code snippets and suggestions]

## Metrics

| Metric | Value | Target |
|--------|-------|--------|
| Test Coverage | 87% | 80% |
| Files Reviewed | 45 | - |
| Review Duration | 2m 14s | - |
```

#### JSON Report

```json
{
    "review_id": "REV-001",
    "timestamp": "<ISO>",
    "system": "<SystemName>",
    "scope": "changed",
    "files_reviewed": 45,
    "blocking_status": "passed|blocked",
    "summary": {
        "critical": 0,
        "high": 3,
        "medium": 8,
        "low": 12
    },
    "findings": [...],
    "metrics": {
        "test_coverage": 87,
        "duration_ms": 134000
    },
    "agents": {
        "bug-hunter": { "findings": 2, "duration_ms": 45000 },
        "security-auditor": { "findings": 0, "duration_ms": 38000 },
        ...
    }
}
```

### Step 7: Update Registries

```
CREATE/UPDATE traceability/review_registry.json:
{
    "reviews": {
        "REV-001": {
            "timestamp": "<ISO>",
            "scope": "changed",
            "status": "passed|blocked",
            "findings_count": 23,
            "blocking_issues": 0
        }
    },
    "findings": {
        "BH-001": {
            "status": "open|resolved|wontfix",
            "task_ref": "T-015",
            "resolved_at": null
        }
    }
}

UPDATE _state/implementation_progress.json:
    IF blocking_status == "passed":
        checkpoint = 6
        status = "completed"
    ELSE:
        checkpoint = 6
        status = "blocked"
```

## Auto-Fix Mode

When `--fix` is enabled:

```
FOR EACH finding WHERE severity IN ["low", "medium"]:
    IF finding.confidence >= 90:
        IF auto_fixable(finding):
            APPLY suggested fix
            MARK finding as "auto-fixed"
            RUN tests to verify

AUTO-FIXABLE patterns:
    - Missing optional chaining
    - Missing null checks (simple cases)
    - Unused imports
    - Formatting issues
    - Missing ARIA labels (templates)
```

## Related Skills

- `Implementation_Developer` - Fixes identified issues
- `systematic-debugging` - For complex bug investigation
- `Implementation_Validator` - Final validation after fixes
