# Verification Gate Pattern

> **MANDATORY FOR ALL SKILLS**: Include this verification gate before marking any phase as "complete".

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this execution, you cannot claim it passes.

---

## The Gate Function

Every skill MUST execute this gate before updating `progress.json` with `status: "complete"`:

```
VERIFICATION_GATE:

  1. IDENTIFY: What command(s) prove this phase succeeded?
     - Output file existence checks
     - Content validation checks
     - Build/lint/test commands
     - Schema validation

  2. RUN: Execute FULL verification (fresh, complete)
     - DO NOT skip any checks
     - DO NOT rely on previous runs
     - Capture all output

  3. READ: Parse verification output
     - Check exit codes
     - Count errors/warnings
     - Verify expected content exists

  4. VERIFY: Does output confirm success?
     - If NO → State actual status with evidence, DO NOT mark complete
     - If YES → State claim WITH evidence path

  5. ONLY THEN: Mark phase complete in progress.json

SKIP ANY STEP = VIOLATION
```

---

## Forbidden Phrases

**NEVER use these before verification:**

| Forbidden | Why |
|-----------|-----|
| "Should pass now" | No evidence |
| "Looks correct" | Subjective, no verification |
| "Probably complete" | Uncertainty = not verified |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "All done!" | Celebration before proof |

---

## Verification Commands by Skill

### ValidateDiscovery
```bash
# Verify outputs exist and are non-empty
test -s _state/discovery_summary.json && echo "PASS: discovery_summary exists"
jq '.entities | length' _state/discovery_summary.json  # Should return > 0
jq '.personas | length' _state/discovery_summary.json  # Should return > 0
```

### Requirements
```bash
# Verify requirements registry
test -s _state/requirements_registry.json && echo "PASS: registry exists"
jq '.summary.epics.total' _state/requirements_registry.json  # Should return > 0
jq '.summary.stories.total' _state/requirements_registry.json  # Should return > 0
# Verify P0 requirements exist
jq '[.epics[] | select(.priority == "P0")] | length' _state/requirements_registry.json
```

### DataModel
```bash
# Verify schema files exist
ls 00-foundation/data-model/entities/*.schema.json | wc -l  # Should match entity count
# Validate JSON schemas
for f in 00-foundation/data-model/entities/*.schema.json; do
  jq empty "$f" && echo "PASS: $f is valid JSON"
done
```

### DesignTokens
```bash
# Verify token file exists
test -s 00-foundation/DESIGN_TOKENS.md && echo "PASS: DESIGN_TOKENS.md exists"
grep -c "color" 00-foundation/DESIGN_TOKENS.md  # Should return > 0
grep -c "spacing" 00-foundation/DESIGN_TOKENS.md  # Should return > 0
```

### Components
```bash
# Count components per category
ls 01-components/primitives/*.md | wc -l  # Should be >= 7
ls 01-components/data-display/*.md | wc -l  # Should be >= 10
ls 01-components/feedback/*.md | wc -l  # Should be >= 3
ls 01-components/navigation/*.md | wc -l  # Should be >= 5
ls 01-components/overlays/*.md | wc -l  # Should be >= 5
# Verify all components have Requirements Addressed section
for f in 01-components/**/*.md; do
  grep -q "Requirements Addressed" "$f" || echo "FAIL: $f missing Requirements Addressed"
done
```

### Screens
```bash
# Verify screens exist per app
ls 02-screens/*/  # List all apps
# Verify P0 coverage
grep -r "P0" 02-screens/ | wc -l  # Should match P0 requirement count
```

### CodeGen
```bash
# Build verification
cd prototype && npm install && npm run build
echo "Exit code: $?"  # Must be 0

# TypeScript check
npx tsc --noEmit
echo "TypeScript errors: $?"  # Must be 0

# Lint check
npm run lint
echo "Lint errors: $?"  # Must be 0

# File count verification
find src/components -name "*.tsx" | wc -l  # Should match component count
find src/screens -name "*.tsx" | wc -l  # Should match screen count
```

### QA
```bash
# Verify P0 coverage is 100%
jq '.phases.qa.validation.p0_coverage' _state/progress.json  # Must be "100%"
# Verify traceability matrix
test -s 05-validation/TRACEABILITY_MATRIX.md && echo "PASS"
# Count unaddressed P0
jq '[.epics[] | select(.priority == "P0" and .status != "addressed")] | length' _state/requirements_registry.json
# Must be 0
```

---

## Integration Template

Add this section to the END of every skill's procedure (before "Update Progress"):

```
### Step N-1: Verification Gate (MANDATORY)

EXECUTE verification_gate:

  // 1. IDENTIFY verification commands
  verification_commands = [
    "test -s {output_file_1}",
    "jq '.key' {json_file}",
    "{build_or_lint_command}"
  ]

  // 2. RUN all verifications
  FOR each command in verification_commands:
    result = EXECUTE(command)
    CAPTURE output and exit_code

    IF exit_code != 0:
      LOG: "VERIFICATION FAILED: {command}"
      LOG: "Output: {output}"
      APPEND to failures[]

  // 3. READ results
  total_checks = verification_commands.length
  passed_checks = total_checks - failures.length

  // 4. VERIFY success
  IF failures.length > 0:
    ═══════════════════════════════════════════
    ❌ VERIFICATION GATE FAILED
    ═══════════════════════════════════════════

    {passed_checks}/{total_checks} checks passed

    Failures:
    • {list failures with outputs}

    CANNOT mark phase complete.

    How would you like to proceed?
    1. "fix: [issue]" - Address specific failure
    2. "retry" - Re-run verification
    3. "investigate" - Show detailed diagnostics
    ═══════════════════════════════════════════

    WAIT for user response
    DO NOT proceed to "Update Progress"

  ELSE:
    LOG: "✅ VERIFICATION PASSED: {total_checks}/{total_checks} checks"
    verification_evidence = {
      checks_run: total_checks,
      checks_passed: total_checks,
      outputs_verified: [...],
      timestamp: NOW()
    }

    // 5. ONLY NOW proceed to Update Progress
    PROCEED to "Update Progress" step
```

---

## Progress.json Verification Evidence

When verification passes, update progress.json with evidence:

```json
{
  "phases": {
    "{skill_name}": {
      "status": "complete",
      "completed_at": "2024-12-15T10:30:00Z",
      "verification": {
        "status": "passed",
        "checks_run": 8,
        "checks_passed": 8,
        "evidence": {
          "output_files_exist": true,
          "json_valid": true,
          "build_success": true,
          "lint_clean": true
        },
        "verified_at": "2024-12-15T10:29:55Z"
      }
    }
  }
}
```

---

## Real-World Impact

From prior failures:
- "I don't believe you" - trust broken when claims weren't verified
- Undefined functions shipped - would crash in production
- Missing requirements shipped - incomplete features
- Time wasted on false completion → redirect → rework

**Verification is non-negotiable.**

---

## Quick Reference

| Before saying... | First run... |
|------------------|--------------|
| "Phase complete" | All verification commands |
| "Build passes" | `npm run build` (capture exit code) |
| "Tests pass" | `npm test` (capture output) |
| "Files generated" | `ls` or `test -s` on each file |
| "JSON valid" | `jq empty file.json` |
| "P0 covered" | Query requirements registry |

---

*This pattern is based on the verification-before-completion skill from 3rdParty.*
