---
description: Perform multi-agent code review with specialized quality reviewers
argument-hint: <SystemName> [--scope all|changed] [--agent <name>] [--threshold 70]
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TaskOutput
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-review started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-review ended '{"stage": "implementation"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "implementation"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /htec-sdd-review instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

---

## Usage

```
/htec-sdd-review <SystemName>
/htec-sdd-review <SystemName> --scope changed
/htec-sdd-review <SystemName> --agent security
/htec-sdd-review <SystemName> --threshold 80
```

## Arguments

- `SystemName`: Name of the system (e.g., ERTriage, InventorySystem)

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--scope <all\|changed\|module>` | Files to review | all |
| `--agent <name>` | Run specific agent only | All agents |
| `--threshold <0-100>` | Min confidence for findings | 70 |
| `--fix` | Auto-fix low-risk issues | false |
| `--module <MOD-ID>` | Review specific module | All |

---

## This is a BLOCKING Checkpoint

Implementation cannot proceed to integration until:
- No CRITICAL findings
- No HIGH findings with confidence > 90%
- Test coverage >= 80% (warning only)

---

## Review Agents

Four specialized agents run in parallel:

| Agent | Focus Area | Severity Weight |
|-------|------------|-----------------|
| `quality-security-auditor` | OWASP Top 10, injection, auth, data exposure | CRITICAL |
| `quality-code-quality` | SOLID, DRY, complexity, naming, patterns | MEDIUM |
| `quality-test-coverage` | Missing tests, edge cases, mocking issues | HIGH |
| `quality-accessibility-auditor` | WCAG compliance, a11y patterns | MEDIUM |

---

## Execution Procedure

### Phase 1: Setup

1. **Validate System Exists**
```bash
# Check implementation folder exists
ls Implementation_<SystemName>/
```

2. **Determine Review Scope**
```
IF --scope == "all":
    FILES = glob("Implementation_<System>/packages/**/src/**/*")
ELIF --scope == "changed":
    FILES = git diff --name-only (since last review)
ELIF --scope == "module":
    FILES = get_files_for_module(--module)
```

3. **Create Reports Directory**
```bash
mkdir -p Implementation_<SystemName>/reports
```

4. **Get Test Status**
```bash
cd Implementation_<SystemName> && pnpm test --reporter=json 2>/dev/null || pnpm test
```

### Phase 2: Execute Review Agents (Parallel)

Launch 4 agents in parallel using Task tool with `run_in_background=true`:

```javascript
// Launch all 4 agents in a SINGLE message with parallel tool calls
Task({
  subagent_type: "quality-security-auditor",
  description: "Security audit <SystemName>",
  prompt: `[See Agent Prompt Template below]`,
  run_in_background: true
})

Task({
  subagent_type: "quality-code-quality",
  description: "Code quality review <SystemName>",
  prompt: `[See Agent Prompt Template below]`,
  run_in_background: true
})

Task({
  subagent_type: "quality-test-coverage",
  description: "Test coverage analysis <SystemName>",
  prompt: `[See Agent Prompt Template below]`,
  run_in_background: true
})

Task({
  subagent_type: "quality-accessibility-auditor",
  description: "Accessibility audit <SystemName>",
  prompt: `[See Agent Prompt Template below]`,
  run_in_background: true
})
```

### Phase 3: Collect Agent Results

Wait for all agents to complete and collect their outputs:

```javascript
// For each agent task
const result = TaskOutput(agent_task_id, { block: true, timeout: 300000 });
```

### Phase 4: Consolidate Findings (CRITICAL)

**You MUST consolidate all agent findings into a single JSON structure.**

Create a temporary findings file with this structure:

```json
{
  "findings": [
    {
      "id": "SEC-001",
      "agent": "security",
      "severity": "high",
      "confidence": 90,
      "category": "A05:2021 - Security Misconfiguration",
      "owasp": "A05:2021",
      "wcag": null,
      "file": "packages/api/src/main.ts",
      "line": 29,
      "issue": "CORS wildcard configuration",
      "remediation": "Configure explicit origin whitelist",
      "priority": "P0",
      "status": "open",
      "blocking": false
    }
  ],
  "metrics": {
    "files_reviewed": 95,
    "test_coverage": 78,
    "tests_passing": 382,
    "tests_failing": 0,
    "tests_skipped": 1,
    "code_quality_score": 78,
    "accessibility_score": 78,
    "security_risk_level": "medium"
  },
  "agents": {
    "security": { "status": "completed", "findings_count": 7 },
    "code_quality": { "status": "completed", "findings_count": 11 },
    "test_coverage": { "status": "completed", "findings_count": 12 },
    "accessibility": { "status": "completed", "findings_count": 10 }
  },
  "positive_findings": {
    "security": ["SQL Injection: TypeORM with parameterized queries", "..."],
    "code_quality": ["Excellent documentation with traceability IDs", "..."],
    "test_coverage": ["AAA pattern used consistently", "..."],
    "accessibility": ["48px touch targets on buttons", "..."]
  },
  "recommendations": {
    "P0": ["SEC-001: Configure CORS", "TC-001: Add patientApi tests"],
    "P1": ["SEC-003: Migrate JWT to cookies", "..."],
    "P2": ["CQ-003: Refactor TriageForm", "..."],
    "P3": ["CQ-010: Extract shared API client", "..."]
  }
}
```

**Write this to a temporary file:**
```bash
# Write consolidated findings to temp file
cat > /tmp/review_findings_<SystemName>.json << 'EOF'
{ ... consolidated JSON ... }
EOF
```

### Phase 5: Generate Reports (MANDATORY)

**This step is MANDATORY - reports MUST be generated.**

```bash
# Generate CODE_REVIEW.md and review-findings.json
python3 .claude/hooks/generate_review_report.py \
  "<SystemName>" \
  "/tmp/review_findings_<SystemName>.json" \
  --scope "<scope>" \
  --update-progress \
  --update-registry
```

**Output files created:**
- `Implementation_<SystemName>/reports/CODE_REVIEW.md` - Human-readable report
- `Implementation_<SystemName>/reports/review-findings.json` - Machine-readable JSON

### Phase 6: Log Version History

```bash
# Log markdown report
python3 .claude/hooks/version_history_logger.py \
  "traceability/" "<SystemName>" "implementation" "Claude" "3.0.0" \
  "Generated code review report from /htec-sdd-review" \
  "REV-XXX" \
  "Implementation_<SystemName>/reports/CODE_REVIEW.md" \
  "creation"

# Log JSON report
python3 .claude/hooks/version_history_logger.py \
  "traceability/" "<SystemName>" "implementation" "Claude" "3.0.0" \
  "Generated machine-readable review findings" \
  "REV-XXX" \
  "Implementation_<SystemName>/reports/review-findings.json" \
  "creation"
```

### Phase 7: Display Summary

Print the review summary to the user:

```
Code Review: PASSED/FAILED
═══════════════════════════════════════

Agents: 4/4 completed
Files reviewed: N
Time: Xm Ys

Summary:
  CRITICAL: 0 ✓/✗
  HIGH: N (all below 90% confidence) ✓/✗
  MEDIUM: N
  LOW: N

Test Coverage: N% (target: 80%) ✓/⚠️

Reports generated:
  - Implementation_<SystemName>/reports/CODE_REVIEW.md
  - Implementation_<SystemName>/reports/review-findings.json

Next: Run /htec-sdd-status <SystemName> --finalize
```

---

## Agent Prompt Template

### Security Auditor

```
Perform security audit for {SystemName} implementation.

READ: .claude/agents/quality-security-auditor.md for full instructions

TARGET FILES:
- Implementation_{SystemName}/packages/api/src/**/*
- Implementation_{SystemName}/packages/web/src/**/*

FOCUS (OWASP Top 10):
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection (SQL, XSS)
- A05: Security Misconfiguration (CORS, headers)
- A07: Authentication Failures

OUTPUT FORMAT (JSON):
Return your findings as a JSON object with this structure:
{
  "agent": "security",
  "files_reviewed": N,
  "risk_level": "low|medium|high|critical",
  "findings": [
    {
      "id": "SEC-001",
      "severity": "critical|high|medium|low",
      "confidence": 0-100,
      "category": "OWASP category",
      "owasp": "A01:2021",
      "cwe": "CWE-XXX",
      "file": "path/to/file.ts",
      "line": N,
      "issue": "Description",
      "remediation": "How to fix",
      "references": ["URLs"]
    }
  ],
  "positive_findings": ["Good practices found"]
}

IMPORTANT: Return ONLY the JSON object, no markdown wrapping.
```

### Code Quality

```
Perform code quality review for {SystemName} implementation.

READ: .claude/agents/quality-code-quality.md for full instructions

TARGET FILES:
- Implementation_{SystemName}/packages/**/src/**/*

FOCUS:
- SOLID principles
- DRY violations
- Cyclomatic complexity (threshold: 10)
- Function length (threshold: 50 lines)
- Nesting depth (threshold: 4)
- Naming conventions

OUTPUT FORMAT (JSON):
Return your findings as a JSON object with this structure:
{
  "agent": "code_quality",
  "files_reviewed": N,
  "quality_score": 0-100,
  "findings": [
    {
      "id": "CQ-001",
      "severity": "high|medium|low",
      "confidence": 0-100,
      "category": "SOLID:SRP|DRY|COMPLEXITY|NAMING",
      "file": "path/to/file.ts",
      "line": N,
      "issue": "Description",
      "metrics": { "complexity": N, "lines": N },
      "remediation": "How to fix"
    }
  ],
  "metrics": {
    "avg_complexity": N,
    "max_function_length": N,
    "duplicate_blocks": N
  },
  "positive_findings": ["Good practices found"]
}

IMPORTANT: Return ONLY the JSON object, no markdown wrapping.
```

### Test Coverage

```
Analyze test coverage for {SystemName} implementation.

READ: .claude/agents/quality-test-coverage.md for full instructions

SOURCE FILES: Implementation_{SystemName}/packages/**/src/**/*
TEST FILES: Implementation_{SystemName}/packages/**/tests/**/*

FOCUS:
- Files without tests
- Untested public functions
- Missing error scenario tests
- Testing anti-patterns
- Coverage gaps

OUTPUT FORMAT (JSON):
Return your findings as a JSON object with this structure:
{
  "agent": "test_coverage",
  "source_files": N,
  "test_files": N,
  "coverage_estimate": 0-100,
  "findings": [
    {
      "id": "TC-001",
      "severity": "high|medium|low",
      "confidence": 0-100,
      "category": "missing_test|anti_pattern|edge_case",
      "file": "path/to/source.ts",
      "test_file": "path/to/test.ts or MISSING",
      "issue": "Description",
      "suggested_tests": ["Test scenario 1", "Test scenario 2"]
    }
  ],
  "positive_findings": ["Good testing practices found"]
}

IMPORTANT: Return ONLY the JSON object, no markdown wrapping.
```

### Accessibility Auditor

```
Perform accessibility audit for {SystemName} implementation.

READ: .claude/agents/quality-accessibility-auditor.md for full instructions

TARGET FILES:
- Implementation_{SystemName}/packages/web/src/**/*.tsx
- Implementation_{SystemName}/packages/web/src/**/*.css

WCAG LEVEL: AA

FOCUS:
- ARIA labels and roles
- Keyboard navigation
- Color contrast
- Focus management
- Screen reader compatibility
- Touch targets (48px minimum)

OUTPUT FORMAT (JSON):
Return your findings as a JSON object with this structure:
{
  "agent": "accessibility",
  "files_reviewed": N,
  "wcag_level": "AA",
  "compliance_score": 0-100,
  "findings": [
    {
      "id": "A11Y-001",
      "severity": "high|medium|low",
      "confidence": 0-100,
      "wcag": "1.4.3|2.1.1|4.1.2|etc",
      "criterion": "Contrast|Keyboard|etc",
      "file": "path/to/component.tsx",
      "line": N,
      "issue": "Description",
      "remediation": "How to fix"
    }
  ],
  "positive_findings": ["Good a11y practices found"]
}

IMPORTANT: Return ONLY the JSON object, no markdown wrapping.
```

---

## Example Complete Workflow

```
# User runs:
/htec-sdd-review ERTriage

# Claude executes:

# Phase 1: Setup
mkdir -p Implementation_ERTriage/reports
cd Implementation_ERTriage && pnpm test

# Phase 2: Launch 4 agents in parallel
[Task calls with run_in_background=true]

# Phase 3: Wait for completion
[TaskOutput for each agent]

# Phase 4: Consolidate findings
cat > /tmp/review_findings_ERTriage.json << 'EOF'
{ "findings": [...], "metrics": {...}, ... }
EOF

# Phase 5: Generate reports (MANDATORY)
python3 .claude/hooks/generate_review_report.py \
  "ERTriage" \
  "/tmp/review_findings_ERTriage.json" \
  --scope "all" \
  --update-progress \
  --update-registry

# Phase 6: Log version history
python3 .claude/hooks/version_history_logger.py ...

# Phase 7: Display summary
Code Review: PASSED
═══════════════════════════════════════
...
Reports generated:
  - Implementation_ERTriage/reports/CODE_REVIEW.md
  - Implementation_ERTriage/reports/review-findings.json
```

---

## Output Files (ALWAYS Generated)

| File | Format | Description |
|------|--------|-------------|
| `Implementation_<System>/reports/CODE_REVIEW.md` | Markdown | Human-readable report with all findings, severity, remediation |
| `Implementation_<System>/reports/review-findings.json` | JSON | Machine-readable findings for CI/CD integration |

---

## Registry Updates

The command automatically updates:

1. **`_state/implementation_progress.json`**
   - Sets checkpoint 4 (Code Review) to completed
   - Records review metrics and blocking status

2. **`traceability/review_registry.json`**
   - Adds new review entry with REV-XXX ID
   - Categorizes findings by type
   - Tracks P0 blockers

3. **`traceability/<SystemName>_version_history.json`**
   - Logs creation of both report files

---

## Auto-Fix Mode (Optional)

```bash
/htec-sdd-review <SystemName> --fix
```

When `--fix` is enabled:
- LOW severity issues are auto-fixed
- MEDIUM issues are fixed if confidence > 90%
- HIGH/CRITICAL always require manual review

---

## Related Commands

- `/htec-sdd-implement` - Fix issues and re-implement
- `/htec-sdd-integrate` - Next step after passing review
- `/htec-sdd-status` - Check review status
- `/fix-tests` - Fix failing tests before review
