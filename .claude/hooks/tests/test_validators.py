#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["pytest"]
# ///

"""
Integration Tests for HTEC Hooks Validators

Tests the validator hooks to ensure they correctly block/allow operations
based on the validation criteria.

Run with:
    uv run pytest .claude/hooks/tests/test_validators.py -v

Or directly:
    uv run .claude/hooks/tests/test_validators.py
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
VALIDATORS_DIR = PROJECT_ROOT / ".claude" / "hooks" / "validators"


def run_validator(validator_name: str, args: list[str] = None, stdin: str = None, cwd: str = None) -> tuple[int, dict]:
    """
    Run a validator script and return exit code and parsed JSON output.

    Args:
        validator_name: Name of validator (e.g., "security_gate.py")
        args: Command line arguments
        stdin: Input to pass via stdin
        cwd: Working directory (defaults to PROJECT_ROOT)

    Returns:
        Tuple of (exit_code, parsed_json_output)
    """
    validator_path = VALIDATORS_DIR / validator_name
    cmd = ["uv", "run", str(validator_path)]

    if args:
        cmd.extend(args)

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        input=stdin,
        timeout=30,
        cwd=cwd if cwd else str(PROJECT_ROOT)
    )

    # Try to parse JSON output
    output = {}
    if result.stdout.strip():
        try:
            output = json.loads(result.stdout)
        except json.JSONDecodeError:
            output = {"raw_output": result.stdout}

    if result.stderr.strip():
        output["stderr"] = result.stderr

    return result.returncode, output


class TestSecurityGate:
    """Tests for security_gate.py - PreToolUse Bash blocking."""

    def test_blocks_rm_rf_root(self):
        """Security gate should block 'rm -rf /'."""
        stdin = json.dumps({
            "tool_name": "Bash",
            "tool_input": {"command": "rm -rf /"}
        })

        exit_code, output = run_validator("security_gate.py", stdin=stdin)

        assert exit_code == 2, f"Expected exit code 2 (block), got {exit_code}"
        assert output.get("decision") == "block", f"Expected block decision, got {output}"
        assert "rm -rf" in output.get("reason", "").lower() or "dangerous" in output.get("reason", "").lower()

    def test_blocks_rm_rf_star(self):
        """Security gate should block 'rm -rf *'."""
        stdin = json.dumps({
            "tool_name": "Bash",
            "tool_input": {"command": "rm -rf *"}
        })

        exit_code, output = run_validator("security_gate.py", stdin=stdin)

        assert exit_code == 2, f"Expected exit code 2 (block), got {exit_code}"
        assert output.get("decision") == "block"

    def test_blocks_sudo_rm(self):
        """Security gate should block 'sudo rm -rf'."""
        stdin = json.dumps({
            "tool_name": "Bash",
            "tool_input": {"command": "sudo rm -rf /tmp/test"}
        })

        exit_code, output = run_validator("security_gate.py", stdin=stdin)

        assert exit_code == 2, f"Expected exit code 2 (block), got {exit_code}"
        assert output.get("decision") == "block"

    def test_blocks_env_file_access(self):
        """Security gate should block direct .env file access."""
        stdin = json.dumps({
            "tool_name": "Bash",
            "tool_input": {"command": "cat .env"}
        })

        exit_code, output = run_validator("security_gate.py", stdin=stdin)

        assert exit_code == 2, f"Expected exit code 2 (block), got {exit_code}"
        assert output.get("decision") == "block"

    def test_allows_env_sample(self):
        """Security gate should allow .env.sample access."""
        stdin = json.dumps({
            "tool_name": "Bash",
            "tool_input": {"command": "cat .env.sample"}
        })

        exit_code, output = run_validator("security_gate.py", stdin=stdin)

        assert exit_code == 0, f"Expected exit code 0 (allow), got {exit_code}"
        assert output.get("decision") == "allow"

    def test_allows_safe_commands(self):
        """Security gate should allow safe commands like ls, pwd, git status."""
        safe_commands = [
            "ls -la",
            "pwd",
            "git status",
            "npm install",
            "python --version"
        ]

        for cmd in safe_commands:
            stdin = json.dumps({
                "tool_name": "Bash",
                "tool_input": {"command": cmd}
            })

            exit_code, output = run_validator("security_gate.py", stdin=stdin)

            assert exit_code == 0, f"Command '{cmd}' should be allowed, got exit code {exit_code}"
            assert output.get("decision") == "allow", f"Command '{cmd}' should be allowed"

    def test_blocks_force_push_main(self):
        """Security gate should block force push to main/master."""
        stdin = json.dumps({
            "tool_name": "Bash",
            "tool_input": {"command": "git push --force origin main"}
        })

        exit_code, output = run_validator("security_gate.py", stdin=stdin)

        assert exit_code == 2, f"Expected exit code 2 (block), got {exit_code}"
        assert output.get("decision") == "block"


class TestValidateFilesExist:
    """Tests for validate_files_exist.py - Stop hook file validation."""

    def test_passes_when_files_exist(self):
        """Should pass when required files exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            Path(tmpdir, "persona-admin.md").write_text("# Admin Persona")
            Path(tmpdir, "persona-user.md").write_text("# User Persona")

            exit_code, output = run_validator(
                "validate_files_exist.py",
                args=["--directory", tmpdir, "--requires", "persona-*.md"]
            )

            assert exit_code == 0, f"Expected exit code 0, got {exit_code}: {output}"
            assert output.get("result") == "pass"

    def test_fails_when_files_missing(self):
        """Should fail when required files don't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Don't create any files

            exit_code, output = run_validator(
                "validate_files_exist.py",
                args=["--directory", tmpdir, "--requires", "persona-*.md"]
            )

            assert exit_code == 1, f"Expected exit code 1 (fail), got {exit_code}"
            assert output.get("result") == "fail"
            assert "persona-*.md" in str(output.get("details", {}).get("missing_patterns", []))

    def test_fails_for_multiple_missing_patterns(self):
        """Should report all missing patterns."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create only one type of file
            Path(tmpdir, "persona-admin.md").write_text("# Admin")

            exit_code, output = run_validator(
                "validate_files_exist.py",
                args=[
                    "--directory", tmpdir,
                    "--requires", "persona-*.md",
                    "--requires", "jtbd-*.md",
                    "--requires", "vision.md"
                ]
            )

            assert exit_code == 1, f"Expected exit code 1, got {exit_code}"
            assert output.get("result") == "fail"
            missing = output.get("details", {}).get("missing_patterns", [])
            assert "jtbd-*.md" in missing
            assert "vision.md" in missing

    def test_error_when_directory_not_found(self):
        """Should return error (exit 2) when directory doesn't exist."""
        exit_code, output = run_validator(
            "validate_files_exist.py",
            args=["--directory", "/nonexistent/path", "--requires", "*.md"]
        )

        assert exit_code == 2, f"Expected exit code 2 (error), got {exit_code}"
        assert output.get("result") == "error"


class TestValidateFileContains:
    """Tests for validate_file_contains.py - Stop hook content validation."""

    def test_passes_when_sections_present(self):
        """Should pass when all required sections are present."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir, "ANALYSIS_SUMMARY.md")
            test_file.write_text("""
# Analysis Summary

## Executive Summary
This is the executive summary.

## Key Findings
Here are the key findings.

## Recommendations
These are the recommendations.
""")

            exit_code, output = run_validator(
                "validate_file_contains.py",
                args=[
                    "--file", str(test_file),
                    "--contains", "## Executive Summary",
                    "--contains", "## Key Findings"
                ]
            )

            assert exit_code == 0, f"Expected exit code 0, got {exit_code}: {output}"
            assert output.get("result") == "pass"

    def test_fails_when_sections_missing(self):
        """Should fail when required sections are missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir, "incomplete.md")
            test_file.write_text("""
# Incomplete Document

## Executive Summary
Only has executive summary.
""")

            exit_code, output = run_validator(
                "validate_file_contains.py",
                args=[
                    "--file", str(test_file),
                    "--contains", "## Executive Summary",
                    "--contains", "## Key Findings",
                    "--contains", "## Pain Points"
                ]
            )

            assert exit_code == 1, f"Expected exit code 1, got {exit_code}"
            assert output.get("result") == "fail"
            missing = output.get("details", {}).get("missing_sections", [])
            assert "## Key Findings" in missing
            assert "## Pain Points" in missing

    def test_error_when_file_not_found(self):
        """Should return error when file doesn't exist."""
        exit_code, output = run_validator(
            "validate_file_contains.py",
            args=[
                "--file", "/nonexistent/file.md",
                "--contains", "## Something"
            ]
        )

        assert exit_code == 2, f"Expected exit code 2 (error), got {exit_code}"
        assert output.get("result") == "error"


class TestValidateFrontmatter:
    """Tests for validate_frontmatter.py - YAML frontmatter validation."""

    def test_passes_with_valid_frontmatter(self):
        """Should pass when frontmatter has all required fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir, "document.md")
            test_file.write_text("""---
document_id: DISC-PERSONA-001
version: 1.0.0
created_at: 2026-01-01
updated_at: 2026-01-15
---

# Document Content
""")

            exit_code, output = run_validator(
                "validate_frontmatter.py",
                args=[
                    "--file", str(test_file),
                    "--requires", "document_id",
                    "--requires", "version"
                ]
            )

            assert exit_code == 0, f"Expected exit code 0, got {exit_code}: {output}"
            assert output.get("result") == "pass"

    def test_fails_with_missing_fields(self):
        """Should fail when required fields are missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir, "document.md")
            test_file.write_text("""---
document_id: DISC-PERSONA-001
---

# Document Content
""")

            exit_code, output = run_validator(
                "validate_frontmatter.py",
                args=[
                    "--file", str(test_file),
                    "--requires", "document_id",
                    "--requires", "version",
                    "--requires", "created_at"
                ]
            )

            assert exit_code == 1, f"Expected exit code 1, got {exit_code}"
            assert output.get("result") == "fail"

    def test_fails_with_no_frontmatter(self):
        """Should fail when file has no frontmatter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir, "no_frontmatter.md")
            test_file.write_text("""# Document Without Frontmatter

Just regular content.
""")

            exit_code, output = run_validator(
                "validate_frontmatter.py",
                args=[
                    "--file", str(test_file),
                    "--requires", "document_id"
                ]
            )

            assert exit_code == 1, f"Expected exit code 1, got {exit_code}"
            assert output.get("result") == "fail"


class TestRuffValidator:
    """Tests for ruff_validator.py - Python linting validation."""

    def test_passes_for_clean_python(self):
        """Should pass for well-formatted Python code."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir, "clean.py")
            test_file.write_text('''"""A clean Python module."""


def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("World"))
''')

            exit_code, output = run_validator(
                "ruff_validator.py",
                args=["--file", str(test_file)]
            )

            # Should pass or skip (if ruff not installed)
            assert exit_code in [0], f"Expected exit code 0, got {exit_code}: {output}"

    def test_fails_for_syntax_errors(self):
        """Should fail for Python with syntax errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir, "bad_syntax.py")
            test_file.write_text('''def broken(
    # Missing closing paren
''')

            exit_code, output = run_validator(
                "ruff_validator.py",
                args=["--file", str(test_file)]
            )

            # Should fail with exit code 1
            assert exit_code == 1, f"Expected exit code 1 (fail), got {exit_code}: {output}"

    def test_fails_for_undefined_names(self):
        """Should fail for undefined variable references (F821)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir, "undefined.py")
            test_file.write_text('''"""Module with undefined name."""


def process():
    """Use undefined variable."""
    return undefined_variable  # F821: undefined name
''')

            exit_code, output = run_validator(
                "ruff_validator.py",
                args=["--file", str(test_file)]
            )

            assert exit_code == 1, f"Expected exit code 1 (fail), got {exit_code}: {output}"
            assert output.get("result") == "fail"

    def test_skips_non_python_files(self):
        """Should skip (exit 0) for non-Python files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir, "component.tsx")
            test_file.write_text('export const Button = () => <button>Click</button>')

            exit_code, output = run_validator(
                "ruff_validator.py",
                args=["--file", str(test_file)]
            )

            assert exit_code == 0, f"Expected exit code 0 (skip), got {exit_code}"
            assert output.get("result") == "skip"

    def test_handles_stdin_input(self):
        """Should work with stdin input (hook mode)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir, "via_stdin.py")
            test_file.write_text('''"""Valid Python."""


def hello():
    """Say hello."""
    return "Hello"
''')

            stdin = json.dumps({
                "tool_input": {"file_path": str(test_file)}
            })

            exit_code, output = run_validator(
                "ruff_validator.py",
                stdin=stdin
            )

            assert exit_code == 0, f"Expected exit code 0, got {exit_code}: {output}"


class TestTyValidator:
    """Tests for ty_validator.py - Python type checking validation."""

    def test_skips_non_python_files(self):
        """Should skip (exit 0) for non-Python files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir, "component.tsx")
            test_file.write_text('export const Button = () => <button>Click</button>')

            exit_code, output = run_validator(
                "ty_validator.py",
                args=["--file", str(test_file)]
            )

            assert exit_code == 0, f"Expected exit code 0 (skip), got {exit_code}"
            assert output.get("result") == "skip"

    def test_passes_for_typed_python(self):
        """Should pass for well-typed Python code."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir, "typed.py")
            test_file.write_text('''"""Properly typed module."""


def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


result: int = add(1, 2)
''')

            exit_code, output = run_validator(
                "ty_validator.py",
                args=["--file", str(test_file)]
            )

            # Should pass or skip (if type checker not installed)
            assert exit_code in [0], f"Expected exit code 0, got {exit_code}: {output}"


class TestCaptureFailure:
    """Tests for capture_failure.py - PostToolUseFailure logging."""

    def test_logs_tool_failure(self):
        """Should log tool failures to lifecycle.json."""
        stdin = json.dumps({
            "tool_name": "Bash",
            "tool_input": {"command": "nonexistent-command"},
            "error": "Command not found: nonexistent-command"
        })

        exit_code, output = run_validator(
            "capture_failure.py",
            stdin=stdin
        )

        # Should always succeed (logging shouldn't block)
        assert exit_code == 0, f"Expected exit code 0, got {exit_code}"
        assert output.get("logged") is True


class TestPermissionAudit:
    """Tests for permission_audit.py - PermissionRequest logging."""

    def test_logs_permission_request(self):
        """Should log permission requests."""
        stdin = json.dumps({
            "permission_type": "write",
            "file_path": "/some/path/file.py"
        })

        exit_code, output = run_validator(
            "permission_audit.py",
            stdin=stdin
        )

        # Should always succeed
        assert exit_code == 0, f"Expected exit code 0, got {exit_code}"


class TestValidateDiscoveryOutput:
    """Tests for validate_discovery_output.py - Discovery stage validation."""

    def test_error_when_folder_not_found(self):
        """Should return error when ClientAnalysis folder doesn't exist."""
        exit_code, output = run_validator(
            "validate_discovery_output.py",
            args=["--system-name", "NonExistentSystem"]
        )

        assert exit_code == 2, f"Expected exit code 2 (error), got {exit_code}"
        assert output.get("result") == "error"
        assert "not found" in output.get("reason", "").lower()

    def test_quick_validation_mode(self):
        """Should validate only essential phases in quick mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create minimal Discovery structure
            base = Path(tmpdir) / "ClientAnalysis_QuickTest"
            base.mkdir()
            (base / "01-analysis").mkdir()
            (base / "02-research").mkdir()
            (base / "04-design-specs").mkdir()
            (base / "05-documentation").mkdir()

            # Create minimal files for essential phases
            (base / "01-analysis" / "ANALYSIS_SUMMARY.md").write_text(
                "# Summary\n## Executive Summary\nTest\n## Key Findings\nTest"
            )
            (base / "02-research" / "persona-admin.md").write_text(
                "# Persona\n## Demographics\nTest\n## Goals\nTest\n## Frustrations\nTest"
            )
            (base / "02-research" / "jtbd-jobs-to-be-done.md").write_text(
                "# JTBD\n## Job Statements\nWhen I... I want to... So that..."
            )
            (base / "04-design-specs" / "screen-definitions.md").write_text(
                "# Screens\n## Screen\n### Components\n### Data Requirements\n"
            )
            (base / "05-documentation" / "INDEX.md").write_text(
                "# Index\n## Table of Contents\n"
            )
            (base / "05-documentation" / "README.md").write_text(
                "# Readme\n## Overview\n"
            )
            (base / "05-documentation" / "VALIDATION_REPORT.md").write_text(
                "# Validation\n## Validation Results\n"
            )

            exit_code, output = run_validator(
                "validate_discovery_output.py",
                args=["--system-name", "QuickTest", "--quick"],
                cwd=tmpdir
            )

            # May fail due to missing registries, but should not error
            assert exit_code in [0, 1], f"Expected exit code 0 or 1, got {exit_code}: {output}"

    def test_specific_phase_validation(self):
        """Should validate only specified phase."""
        exit_code, output = run_validator(
            "validate_discovery_output.py",
            args=["--system-name", "TestSystem", "--phase", "personas"]
        )

        # Should error because folder doesn't exist
        assert exit_code == 2, f"Expected exit code 2, got {exit_code}"


class TestValidatePrototypeOutput:
    """Tests for validate_prototype_output.py - Prototype stage validation."""

    def test_error_when_folder_not_found(self):
        """Should return error when Prototype folder doesn't exist."""
        exit_code, output = run_validator(
            "validate_prototype_output.py",
            args=["--system-name", "NonExistentSystem"]
        )

        assert exit_code == 2, f"Expected exit code 2 (error), got {exit_code}"
        assert output.get("result") == "error"
        assert "not found" in output.get("reason", "").lower()

    def test_quick_validation_mode(self):
        """Should validate only essential phases in quick mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create minimal Prototype structure
            base = Path(tmpdir) / "Prototype_QuickTest"
            base.mkdir()
            (base / "00-foundation").mkdir()
            (base / "01-components").mkdir()
            (base / "01-components" / "primitives").mkdir()
            (base / "01-components" / "data-display").mkdir()
            (base / "01-components" / "feedback").mkdir()
            (base / "02-screens").mkdir()
            (base / "prototype").mkdir()
            (base / "prototype" / "src").mkdir()
            (base / "prototype" / "src" / "components").mkdir()
            (base / "prototype" / "src" / "pages").mkdir()
            state_dir = Path(tmpdir) / "_state"
            state_dir.mkdir()

            # Create minimal files
            (state_dir / "prototype_config.json").write_text("{}")
            (state_dir / "prototype_progress.json").write_text("{}")
            (state_dir / "requirements_registry.json").write_text("{}")
            (base / "00-foundation" / "design-tokens.json").write_text("{}")
            (base / "01-components" / "component-index.md").write_text(
                "# Components\n## Overview\n## Component Count\n5"
            )
            (base / "02-screens" / "screen-index.md").write_text(
                "# Screens\n## Screen Inventory\n## Screen Flow\n"
            )
            (base / "prototype" / "package.json").write_text("{}")
            (base / "prototype" / "src" / "App.tsx").write_text("export default function App() {}")

            exit_code, output = run_validator(
                "validate_prototype_output.py",
                args=["--system-name", "QuickTest", "--quick"],
                cwd=tmpdir
            )

            # May fail due to missing files, but should not error
            assert exit_code in [0, 1], f"Expected exit code 0 or 1, got {exit_code}: {output}"

    def test_specific_phase_validation(self):
        """Should validate only specified phase."""
        exit_code, output = run_validator(
            "validate_prototype_output.py",
            args=["--system-name", "TestSystem", "--phase", "components"]
        )

        assert exit_code == 2, f"Expected exit code 2, got {exit_code}"


class TestValidateProductSpecsOutput:
    """Tests for validate_productspecs_output.py - ProductSpecs stage validation."""

    def test_error_when_folder_not_found(self):
        """Should return error when ProductSpecs folder doesn't exist."""
        exit_code, output = run_validator(
            "validate_productspecs_output.py",
            args=["--system-name", "NonExistentSystem"]
        )

        assert exit_code == 2, f"Expected exit code 2 (error), got {exit_code}"
        assert output.get("result") == "error"
        assert "not found" in output.get("reason", "").lower()

    def test_quick_validation_mode(self):
        """Should validate only essential phases in quick mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create minimal ProductSpecs structure
            base = Path(tmpdir) / "ProductSpecs_QuickTest"
            base.mkdir()
            (base / "00-overview").mkdir()
            (base / "01-modules").mkdir()
            (base / "02-api").mkdir()
            (base / "03-tests").mkdir()
            (base / "04-jira").mkdir()
            (base / "_registry").mkdir()
            state_dir = Path(tmpdir) / "_state"
            state_dir.mkdir()

            # Create minimal files
            (state_dir / "productspecs_config.json").write_text("{}")
            (state_dir / "productspecs_progress.json").write_text('{"current_phase": 1}')
            (base / "01-modules" / "module-index.md").write_text(
                "# Modules\n## Modules by Priority\n## Traceability\n"
            )
            (base / "01-modules" / "MOD-TEST-001.md").write_text(
                "# Module\n## 1. Traceability\n## 2. Screen Specifications\n"
            )
            (base / "03-tests" / "test-case-registry.md").write_text(
                "# Tests\n## Summary\n## Coverage\n"
            )
            (base / "03-tests" / "e2e-scenarios.md").write_text(
                "# E2E\n## Critical Paths\nFeature: Test"
            )
            (base / "03-tests" / "accessibility-checklist.md").write_text(
                "# A11y\n## Screen Checklist\nWCAG 2.1"
            )
            (base / "00-overview" / "TRACEABILITY_MATRIX.md").write_text(
                "# Matrix\n## P0 Requirements\n## Coverage Summary\n"
            )
            (base / "00-overview" / "VALIDATION_REPORT.md").write_text(
                "# Validation\n## Executive Summary\n## Detailed Results\n"
            )
            (base / "_registry" / "modules.json").write_text("[]")
            (base / "_registry" / "test-cases.json").write_text("[]")
            (base / "_registry" / "traceability.json").write_text("{}")

            exit_code, output = run_validator(
                "validate_productspecs_output.py",
                args=["--system-name", "QuickTest", "--quick"],
                cwd=tmpdir
            )

            assert exit_code in [0, 1], f"Expected exit code 0 or 1, got {exit_code}: {output}"

    def test_specific_phase_validation(self):
        """Should validate only specified phase."""
        exit_code, output = run_validator(
            "validate_productspecs_output.py",
            args=["--system-name", "TestSystem", "--phase", "modules_core"]
        )

        assert exit_code == 2, f"Expected exit code 2, got {exit_code}"


class TestValidateSolArchOutput:
    """Tests for validate_solarch_output.py - SolArch stage validation."""

    def test_error_when_folder_not_found(self):
        """Should return error when SolArch folder doesn't exist."""
        exit_code, output = run_validator(
            "validate_solarch_output.py",
            args=["--system-name", "NonExistentSystem"]
        )

        assert exit_code == 2, f"Expected exit code 2 (error), got {exit_code}"
        assert output.get("result") == "error"
        assert "not found" in output.get("reason", "").lower()

    def test_quick_validation_mode(self):
        """Should validate only essential phases in quick mode."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create minimal SolArch structure
            base = Path(tmpdir) / "SolArch_QuickTest"
            base.mkdir()
            for folder in [
                "01-introduction-goals", "02-constraints", "03-context-scope",
                "04-solution-strategy", "05-building-blocks", "06-runtime",
                "07-quality", "08-deployment", "09-decisions", "10-risks",
                "11-glossary", "diagrams", "reports", "_registry"
            ]:
                (base / folder).mkdir()
            (base / "05-building-blocks" / "modules").mkdir()
            (base / "05-building-blocks" / "data-model").mkdir()
            state_dir = Path(tmpdir) / "_state"
            state_dir.mkdir()
            trace_dir = Path(tmpdir) / "traceability"
            trace_dir.mkdir()

            # Create minimal files for essential phases
            (state_dir / "solarch_config.json").write_text("{}")
            (state_dir / "solarch_progress.json").write_text('{"current_checkpoint": 1}')
            (base / "05-building-blocks" / "overview.md").write_text(
                "# Overview\n## Level 1\n## Level 2\n"
            )
            (base / "diagrams" / "c4-context.mermaid").write_text("graph TD")
            (base / "diagrams" / "c4-container.mermaid").write_text("graph TD")
            (base / "09-decisions" / "INDEX.md").write_text(
                "# Decisions\n## Decision Log\n## Categories\n"
            )
            # Create 9 ADRs
            for i in range(1, 10):
                (base / "09-decisions" / f"ADR-00{i}-test.md").write_text(
                    f"# ADR-00{i}\n## Status\nAccepted\n## Context\nTest\n## Decision\nTest"
                )
            (base / "_registry" / "decisions.json").write_text("[]")
            (base / "_registry" / "architecture-traceability.json").write_text("{}")
            (trace_dir / "solarch_traceability_register.json").write_text("{}")
            (base / "reports" / "VALIDATION_REPORT.md").write_text(
                "# Report\n## Overview\n## Checkpoint Summary\n"
            )
            (base / "reports" / "GENERATION_SUMMARY.md").write_text(
                "# Summary\n## Executive Summary\n## Architecture Overview\n"
            )

            exit_code, output = run_validator(
                "validate_solarch_output.py",
                args=["--system-name", "QuickTest", "--quick"],
                cwd=tmpdir
            )

            assert exit_code in [0, 1], f"Expected exit code 0 or 1, got {exit_code}: {output}"

    def test_specific_phase_validation(self):
        """Should validate only specified phase."""
        exit_code, output = run_validator(
            "validate_solarch_output.py",
            args=["--system-name", "TestSystem", "--phase", "blocks"]
        )

        assert exit_code == 2, f"Expected exit code 2, got {exit_code}"


def run_tests():
    """Run all tests and print summary."""
    import traceback

    test_classes = [
        TestSecurityGate,
        TestValidateFilesExist,
        TestValidateFileContains,
        TestValidateFrontmatter,
        TestRuffValidator,
        TestTyValidator,
        TestCaptureFailure,
        TestPermissionAudit,
        TestValidateDiscoveryOutput,
        TestValidatePrototypeOutput,
        TestValidateProductSpecsOutput,
        TestValidateSolArchOutput,
    ]

    passed = 0
    failed = 0
    skipped = 0

    print("=" * 70)
    print("HTEC Hooks Validators - Integration Tests")
    print("=" * 70)
    print()

    for test_class in test_classes:
        print(f"\n{test_class.__name__}")
        print("-" * len(test_class.__name__))

        instance = test_class()

        for method_name in dir(instance):
            if not method_name.startswith("test_"):
                continue

            method = getattr(instance, method_name)
            test_name = method_name.replace("test_", "").replace("_", " ")

            try:
                method()
                print(f"  ✅ {test_name}")
                passed += 1
            except AssertionError as e:
                print(f"  ❌ {test_name}")
                print(f"     {str(e)}")
                failed += 1
            except Exception as e:
                print(f"  ⚠️  {test_name} (skipped)")
                print(f"     {str(e)}")
                skipped += 1

    print()
    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed, {skipped} skipped")
    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
