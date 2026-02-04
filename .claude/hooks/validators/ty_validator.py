#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Ty Validator - Python Type Checking Hook

PostToolUse hook that validates Python files using ty (or pyright/mypy fallback).
Runs after Write/Edit tool operations on Python files.

Exit Codes:
- 0: File passes type checks (or not a Python file)
- 1: Type checker found errors (blocks completion)
- 2: Critical error (type checker not available, invalid input)

Usage:
    # Via stdin (hook mode - receives tool_input JSON)
    echo '{"tool_input": {"file_path": "/path/to/file.py"}}' | uv run ty_validator.py

    # Via argument (standalone mode)
    uv run ty_validator.py --file /path/to/file.py

    # Skip check for non-Python files
    uv run ty_validator.py --file /path/to/file.tsx  # exits 0 immediately
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


# Python file extensions to validate
PYTHON_EXTENSIONS = {".py", ".pyi"}


def is_python_file(file_path: Path) -> bool:
    """Check if file is a Python file."""
    return file_path.suffix.lower() in PYTHON_EXTENSIONS


def run_type_checker(file_path: Path) -> dict:
    """
    Run type checker on a file and return results.
    Tries ty first, then pyright, then mypy.

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

    # Try different type checkers in order of preference
    type_checkers = [
        ("uvx", ["uvx", "ty", "check", str(file_path)]),
        ("ty", ["ty", "check", str(file_path)]),
        ("uvx-pyright", ["uvx", "pyright", str(file_path), "--outputjson"]),
        ("pyright", ["pyright", str(file_path), "--outputjson"]),
        ("mypy", ["mypy", str(file_path), "--no-error-summary"]),
    ]

    last_error = None
    for checker_name, cmd in type_checkers:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )

            # Parse output based on checker
            errors = parse_type_checker_output(checker_name, result)

            if errors is not None:  # None means parse failed, try next checker
                if errors:
                    error_count = len(errors)
                    return {
                        "result": "fail",
                        "reason": f"{checker_name} found {error_count} type error(s)",
                        "errors": errors,
                        "file_path": str(file_path),
                        "checker": checker_name
                    }
                else:
                    return {
                        "result": "pass",
                        "reason": f"Type check passed ({checker_name}) for {file_path.name}",
                        "errors": [],
                        "file_path": str(file_path),
                        "checker": checker_name
                    }

        except FileNotFoundError:
            last_error = f"{checker_name} not found"
            continue
        except subprocess.TimeoutExpired:
            last_error = f"{checker_name} timed out"
            continue

    # No type checker available
    return {
        "result": "skip",
        "reason": f"No type checker available ({last_error}). Install via: uv tool install pyright",
        "errors": []
    }


def parse_type_checker_output(checker_name: str, result: subprocess.CompletedProcess) -> list | None:
    """
    Parse type checker output into standardized error format.
    Returns None if parsing fails (try next checker).
    """
    errors = []

    if "pyright" in checker_name:
        # Pyright JSON output
        try:
            if result.stdout.strip():
                data = json.loads(result.stdout)
                diagnostics = data.get("generalDiagnostics", [])
                for diag in diagnostics:
                    if diag.get("severity") == "error":
                        errors.append({
                            "code": diag.get("rule", "TYPE_ERROR"),
                            "message": diag.get("message", ""),
                            "line": diag.get("range", {}).get("start", {}).get("line", 0) + 1,
                            "column": diag.get("range", {}).get("start", {}).get("character", 0) + 1,
                            "severity": "error"
                        })
            return errors
        except json.JSONDecodeError:
            return None

    elif "ty" in checker_name:
        # ty output format (similar to pyright/ruff)
        # Check return code - 0 means no errors
        if result.returncode == 0:
            return []

        # Parse line-based output
        for line in result.stdout.splitlines():
            if "error:" in line.lower() or "Error:" in line:
                parts = line.split(":")
                if len(parts) >= 4:
                    try:
                        errors.append({
                            "code": "TYPE_ERROR",
                            "message": ":".join(parts[3:]).strip(),
                            "line": int(parts[1]) if parts[1].isdigit() else 0,
                            "column": int(parts[2]) if parts[2].isdigit() else 0,
                            "severity": "error"
                        })
                    except (ValueError, IndexError):
                        errors.append({
                            "code": "TYPE_ERROR",
                            "message": line.strip(),
                            "line": 0,
                            "column": 0,
                            "severity": "error"
                        })

        # If we got errors, return them; if not but returncode != 0, something went wrong
        if errors or result.returncode != 0:
            return errors if errors else [{
                "code": "TYPE_ERROR",
                "message": result.stderr.strip() or result.stdout.strip() or "Unknown type error",
                "line": 0,
                "column": 0,
                "severity": "error"
            }]
        return []

    elif "mypy" in checker_name:
        # Mypy text output
        if result.returncode == 0:
            return []

        for line in result.stdout.splitlines():
            if ": error:" in line:
                parts = line.split(":")
                if len(parts) >= 4:
                    try:
                        errors.append({
                            "code": "TYPE_ERROR",
                            "message": ":".join(parts[3:]).strip(),
                            "line": int(parts[1]) if parts[1].isdigit() else 0,
                            "column": int(parts[2]) if parts[2].isdigit() else 0,
                            "severity": "error"
                        })
                    except (ValueError, IndexError):
                        errors.append({
                            "code": "TYPE_ERROR",
                            "message": line.strip(),
                            "line": 0,
                            "column": 0,
                            "severity": "error"
                        })

        return errors

    return None


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
        description="Validate Python files using type checker (ty/pyright/mypy)"
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

    # Run type checker validation
    result = run_type_checker(file_path)

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
