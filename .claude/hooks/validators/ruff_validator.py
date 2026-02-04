#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Ruff Validator - Python Code Quality Hook

PostToolUse hook that validates Python files using Ruff linter.
Runs after Write/Edit tool operations on Python files.

Exit Codes:
- 0: File passes Ruff checks (or not a Python file)
- 1: Ruff found linting errors (blocks completion)
- 2: Critical error (Ruff not available, invalid input)

Usage:
    # Via stdin (hook mode - receives tool_input JSON)
    echo '{"tool_input": {"file_path": "/path/to/file.py"}}' | uv run ruff_validator.py

    # Via argument (standalone mode)
    uv run ruff_validator.py --file /path/to/file.py

    # Skip check for non-Python files
    uv run ruff_validator.py --file /path/to/file.tsx  # exits 0 immediately
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


# Python file extensions to validate
PYTHON_EXTENSIONS = {".py", ".pyi"}

# Ruff configuration - use sensible defaults
RUFF_ARGS = [
    "--select=E,F,W,I",  # Enable errors, pyflakes, warnings, isort
    "--ignore=E501",      # Ignore line too long (handled by formatter)
    "--output-format=json",
]


def is_python_file(file_path: Path) -> bool:
    """Check if file is a Python file."""
    return file_path.suffix.lower() in PYTHON_EXTENSIONS


def run_ruff(file_path: Path) -> dict:
    """
    Run Ruff on a file and return results.

    Returns:
        dict with result, errors list, and summary
    """
    if not file_path.exists():
        return {
            "result": "skip",
            "reason": f"File not found: {file_path}",
            "errors": []
        }

    if not is_python_file(file_path):
        return {
            "result": "skip",
            "reason": f"Not a Python file: {file_path.suffix}",
            "errors": []
        }

    try:
        # Try uvx ruff first (preferred)
        result = subprocess.run(
            ["uvx", "ruff", "check", str(file_path)] + RUFF_ARGS,
            capture_output=True,
            text=True,
            timeout=30
        )
    except FileNotFoundError:
        try:
            # Fallback to system ruff
            result = subprocess.run(
                ["ruff", "check", str(file_path)] + RUFF_ARGS,
                capture_output=True,
                text=True,
                timeout=30
            )
        except FileNotFoundError:
            return {
                "result": "error",
                "reason": "Ruff not available (install via: uv tool install ruff)",
                "errors": []
            }
    except subprocess.TimeoutExpired:
        return {
            "result": "error",
            "reason": "Ruff check timed out (30s)",
            "errors": []
        }

    # Parse Ruff JSON output
    errors = []
    if result.stdout.strip():
        try:
            ruff_output = json.loads(result.stdout)
            for issue in ruff_output:
                errors.append({
                    "code": issue.get("code", "UNKNOWN"),
                    "message": issue.get("message", ""),
                    "line": issue.get("location", {}).get("row", 0),
                    "column": issue.get("location", {}).get("column", 0),
                    "severity": "error" if issue.get("code", "").startswith(("E", "F")) else "warning"
                })
        except json.JSONDecodeError:
            # If JSON parsing fails, treat as plain text errors
            errors.append({
                "code": "PARSE_ERROR",
                "message": result.stdout.strip(),
                "line": 0,
                "column": 0,
                "severity": "error"
            })

    # Check for fatal errors in stderr
    if result.returncode != 0 and not errors:
        if result.stderr.strip():
            errors.append({
                "code": "RUFF_ERROR",
                "message": result.stderr.strip(),
                "line": 0,
                "column": 0,
                "severity": "error"
            })

    if errors:
        error_count = len([e for e in errors if e["severity"] == "error"])
        warning_count = len([e for e in errors if e["severity"] == "warning"])
        return {
            "result": "fail",
            "reason": f"Ruff found {error_count} error(s) and {warning_count} warning(s)",
            "errors": errors,
            "file_path": str(file_path)
        }

    return {
        "result": "pass",
        "reason": f"Ruff check passed for {file_path.name}",
        "errors": [],
        "file_path": str(file_path)
    }


def get_file_path_from_stdin() -> Path | None:
    """Extract file_path from hook stdin (tool_input JSON)."""
    try:
        if not sys.stdin.isatty():
            stdin_data = sys.stdin.read()
            if stdin_data.strip():
                data = json.loads(stdin_data)
                # Handle both direct file_path and nested tool_input
                if "tool_input" in data:
                    file_path = data["tool_input"].get("file_path")
                elif "file_path" in data:
                    file_path = data.get("file_path")
                else:
                    return None

                if file_path:
                    return Path(file_path)
    except (json.JSONDecodeError, KeyError):
        pass
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Validate Python files using Ruff linter"
    )
    parser.add_argument(
        "--file", "-f",
        help="Path to file to validate (alternative to stdin)"
    )
    parser.add_argument(
        "--json-output", "-j",
        action="store_true",
        help="Output JSON only (default for hook mode)"
    )

    args = parser.parse_args()

    # Get file path from argument or stdin
    if args.file:
        file_path = Path(args.file)
    else:
        file_path = get_file_path_from_stdin()

    if not file_path:
        result = {
            "result": "error",
            "reason": "No file path provided (use --file or stdin)",
            "errors": []
        }
        print(json.dumps(result, indent=2))
        sys.exit(2)

    # Run Ruff validation
    result = run_ruff(file_path)

    # Output JSON
    print(json.dumps(result, indent=2))

    # Set exit code
    if result["result"] == "pass":
        sys.exit(0)
    elif result["result"] == "skip":
        sys.exit(0)  # Skip is not an error
    elif result["result"] == "error":
        sys.exit(2)
    else:  # fail
        sys.exit(1)


if __name__ == "__main__":
    main()
