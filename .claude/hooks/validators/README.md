# HTEC Framework Validators Library

Self-validating hooks that enforce quality gates deterministically.

## Overview

This library provides validators that can be used as hooks to block Claude from completing commands until quality criteria are met. Unlike traditional validation that relies on Claude following instructions, these hooks **enforce** validation - Claude cannot stop a command until all validators pass.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     VALIDATORS ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  LAYER 1: GENERIC VALIDATORS (Reusable across all stages)           │
│  ├── validate_files_exist.py     - Check file patterns exist        │
│  ├── validate_file_contains.py   - Check file has required content  │
│  └── validate_frontmatter.py     - Check YAML metadata              │
│                                                                      │
│  LAYER 2: SECURITY VALIDATORS                                       │
│  ├── security_gate.py            - Block dangerous bash commands    │
│  └── permission_audit.py         - Audit permission requests        │
│                                                                      │
│  LAYER 3: CODE QUALITY VALIDATORS                                   │
│  ├── ruff_validator.py           - Python linting (Ruff)            │
│  └── ty_validator.py             - Python type checking             │
│                                                                      │
│  LAYER 4: STAGE-SPECIFIC VALIDATORS                                 │
│  ├── validate_discovery_output.py    - Discovery completeness       │
│  ├── validate_prototype_output.py    - Prototype completeness       │
│  ├── validate_productspecs_output.py - ProductSpecs completeness    │
│  └── validate_solarch_output.py      - SolArch completeness         │
│                                                                      │
│  LAYER 5: ERROR CAPTURE                                             │
│  └── capture_failure.py          - Log tool failures                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Exit Code Protocol

All validators follow this exit code convention:

| Exit Code | Meaning | Hook Behavior |
|-----------|---------|---------------|
| 0 | Validation passed / Skip (non-applicable) | Allow Claude to continue/stop |
| 1 | Validation failed | Block Claude from stopping |
| 2 | Critical error / Security block | Force Claude to address immediately |

## Available Validators

### Generic Validators

#### `validate_files_exist.py`

Checks that required files matching glob patterns exist in a directory.

```bash
# Check for persona files
uv run validate_files_exist.py \
  --directory ClientAnalysis_TestSystem/02-research \
  --requires "persona-*.md"

# Check for multiple patterns
uv run validate_files_exist.py \
  --directory ClientAnalysis_TestSystem \
  --requires "02-research/persona-*.md" \
  --requires "02-research/jtbd-*.md" \
  --requires "05-documentation/VALIDATION_REPORT.md"
```

#### `validate_file_contains.py`

Checks that files contain required sections/strings.

```bash
# Check specific file for sections
uv run validate_file_contains.py \
  --file ClientAnalysis_TestSystem/01-analysis/ANALYSIS_SUMMARY.md \
  --contains "## Executive Summary" \
  --contains "## Key Findings"

# Check newest file in directory for sections
uv run validate_file_contains.py \
  --directory ClientAnalysis_TestSystem/02-research \
  --pattern "persona-*.md" \
  --contains "## Demographics" \
  --contains "## Goals"
```

#### `validate_frontmatter.py`

Checks that markdown files have valid YAML frontmatter with required fields.

```bash
# Check for required fields
uv run validate_frontmatter.py \
  --file ClientAnalysis_TestSystem/02-research/persona-01.md \
  --requires document_id \
  --requires version

# Check with field patterns (fnmatch syntax)
uv run validate_frontmatter.py \
  --file persona-01.md \
  --requires "document_id:PER-*" \
  --requires "version:1.*"
```

### Security Validators

#### `security_gate.py`

Blocks dangerous bash commands before execution. Used as a PreToolUse hook.

```bash
# Test with JSON input (hook format)
echo '{"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}' | \
  uv run security_gate.py

# Test with raw command
echo "rm -rf /" | uv run security_gate.py
```

**Blocked Patterns:**
- `rm -rf /` or `rm -rf /*` - Root/wildcard deletion
- `sudo rm` - Elevated deletion
- `.env` file access (except `.env.sample`, `.env.example`)
- `chmod 777` - World-writable permissions
- Device writes (`/dev/sda`)
- Filesystem destruction (`mkfs`, `dd if=/dev/zero`)
- Fork bombs
- `git push --force` to main/master
- History manipulation (`history -c`, etc.)

#### `permission_audit.py`

Logs all permission requests to `_state/permission_audit.json`.

```bash
# Test with permission request
echo '{"permission_type": "write", "file_path": "/some/file.py"}' | \
  uv run permission_audit.py
```

### Code Quality Validators

#### `ruff_validator.py`

Validates Python files using the Ruff linter. Used as a PostToolUse hook for Write/Edit operations.

```bash
# Via argument (standalone mode)
uv run ruff_validator.py --file /path/to/file.py

# Via stdin (hook mode)
echo '{"tool_input": {"file_path": "/path/to/file.py"}}' | \
  uv run ruff_validator.py
```

**Checks:**
- Errors (E), pyflakes (F), warnings (W), isort (I)
- Skips non-Python files automatically
- JSON output with error details

#### `ty_validator.py`

Validates Python files using type checker (ty/pyright/mypy fallback).

```bash
# Via argument (standalone mode)
uv run ty_validator.py --file /path/to/file.py

# Via stdin (hook mode)
echo '{"tool_input": {"file_path": "/path/to/file.py"}}' | \
  uv run ty_validator.py
```

**Checks:**
- Type annotations
- Type inference errors
- Skips non-Python files automatically

### Stage-Specific Validators

#### `validate_discovery_output.py`

Validates complete Discovery stage output.

```bash
uv run validate_discovery_output.py --system-name MyProject
```

**Checks:**
- Analysis summary exists with required sections
- At least one persona file exists
- JTBD document exists
- Screen definitions exist
- Validation report exists

#### `validate_prototype_output.py`

Validates complete Prototype stage output.

```bash
uv run validate_prototype_output.py --system-name MyProject
```

#### `validate_productspecs_output.py`

Validates complete ProductSpecs stage output.

```bash
uv run validate_productspecs_output.py --system-name MyProject
```

#### `validate_solarch_output.py`

Validates complete SolArch stage output.

```bash
uv run validate_solarch_output.py --system-name MyProject
```

### Error Capture

#### `capture_failure.py`

Logs tool failures to `_state/lifecycle.json`. Used as a PostToolUseFailure hook.

```bash
echo '{"tool_name": "Bash", "tool_input": {"command": "..."}, "error": "..."}' | \
  uv run capture_failure.py
```

**Features:**
- Error classification (permission, file_not_found, timeout, syntax, etc.)
- Severity assessment (critical, high, medium, low)
- Tool input summarization for debugging

## Hook Usage Examples

### Stop Hook (Command Frontmatter)

```yaml
hooks:
  Stop:
    - hooks:
        # VALIDATION: Check required files exist
        - type: command
          command: >-
            uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py
            --directory ClientAnalysis_$1/02-research
            --requires "persona-*.md"
        # VALIDATION: Check content requirements
        - type: command
          command: >-
            uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_file_contains.py
            --file ClientAnalysis_$1/01-analysis/ANALYSIS_SUMMARY.md
            --contains "## Executive Summary"
        # LOGGING: Record completion
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery ended
```

### PreToolUse Hook (Global settings.json)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/security_gate.py"
          }
        ]
      }
    ]
  }
}
```

### PostToolUse Hook (Agent Frontmatter)

```yaml
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/ruff_validator.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/validators/ty_validator.py"
```

## JSON Output Format

All validators output JSON for hook parsing:

```json
{
  "result": "pass|fail|error|skip",
  "reason": "Human-readable explanation",
  "details": {
    // Validator-specific details
  }
}
```

### Security Gate Output

```json
{
  "decision": "allow|block",
  "reason": "Security gate: <explanation>",
  "details": {
    "blocked_command": "<truncated command>",
    "pattern_matched": "<matched pattern>"
  }
}
```

## Testing

Run the integration tests to verify all validators work correctly:

```bash
# Run all tests
uv run .claude/hooks/tests/test_validators.py

# Run with pytest (more verbose)
uv run pytest .claude/hooks/tests/test_validators.py -v
```

**Test Coverage (38 tests total):**
- SecurityGate: 7 tests (blocks rm -rf, sudo rm, .env, force push; allows safe commands)
- ValidateFilesExist: 4 tests (pass/fail/error scenarios)
- ValidateFileContains: 3 tests (pass/fail/error scenarios)
- ValidateFrontmatter: 3 tests (pass/fail/missing scenarios)
- RuffValidator: 5 tests (clean, syntax errors, undefined names, skip non-Python, stdin)
- TyValidator: 2 tests (typed Python, skip non-Python)
- CaptureFailure: 1 test (logging)
- PermissionAudit: 1 test (logging)
- ValidateDiscoveryOutput: 3 tests (error, quick mode, specific phase)
- ValidatePrototypeOutput: 3 tests (error, quick mode, specific phase)
- ValidateProductSpecsOutput: 3 tests (error, quick mode, specific phase)
- ValidateSolArchOutput: 3 tests (error, quick mode, specific phase)

## Dependencies

- Python 3.8+
- UV (for running scripts)
- Ruff (`uvx ruff` for linting)
- Type checker (ty/pyright/mypy - any available)

## Performance

Validators are designed to complete in <2 seconds. For large file checks:
- Use specific glob patterns instead of `**`
- Limit directory depth
- Cache file reads where possible
- Validators use 30-second timeout for subprocess calls

## Troubleshooting

### Validator hangs
- Check if subprocess is waiting for input
- Verify file paths are correct
- Check for infinite loops in glob patterns

### Exit code 2 on safe command
- Review security_gate.py BLOCKED_PATTERNS
- Check if command matches an unintended pattern
- Add to ALLOWED_EXCEPTIONS if needed

### Ruff/Ty not found
- Install via: `uv tool install ruff` or `uv tool install pyright`
- Validators will skip (exit 0) if type checker unavailable
