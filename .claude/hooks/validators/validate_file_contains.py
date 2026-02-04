#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Validate File Contains - HTEC Hook Validator

Checks that files contain required sections/strings.
Can find newest file in a directory or check a specific file.

Exit Codes:
- 0: All required sections found
- 1: One or more required sections missing (blocks Stop)
- 2: Critical error (file not found, invalid arguments)

Usage:
    # Check newest file in directory matching pattern
    uv run validate_file_contains.py \\
        --directory ClientAnalysis_TestSystem/02-research \\
        --pattern "persona-*.md" \\
        --contains "## Demographics" \\
        --contains "## Goals"

    # Check specific file
    uv run validate_file_contains.py \\
        --file ClientAnalysis_TestSystem/discovery_summary.json \\
        --contains "personas" \\
        --contains "pain_points"
"""

import argparse
import glob
import json
import sys
from pathlib import Path


def find_newest_file(directory: str, pattern: str) -> Path | None:
    """Find the most recently modified file matching pattern."""
    dir_path = Path(directory)
    full_pattern = str(dir_path / pattern)
    matches = glob.glob(full_pattern, recursive=True)

    if not matches:
        return None

    # Sort by modification time, newest first
    matches.sort(key=lambda x: Path(x).stat().st_mtime, reverse=True)
    return Path(matches[0])


def check_file_contains(file_path: Path, required_strings: list[str]) -> dict:
    """
    Check that a file contains all required strings.

    Args:
        file_path: Path to file to check
        required_strings: List of strings that must be present

    Returns:
        dict with 'result', 'reason', 'details'
    """
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return {
            "result": "error",
            "reason": f"Failed to read file: {e}",
            "details": {"file": str(file_path)}
        }

    missing_sections = []
    found_sections = []

    for required in required_strings:
        if required in content:
            found_sections.append(required)
        else:
            missing_sections.append(required)

    if missing_sections:
        return {
            "result": "fail",
            "reason": f"Missing required sections: {', '.join(missing_sections)}",
            "details": {
                "file": str(file_path),
                "missing_sections": missing_sections,
                "found_sections": found_sections,
                "file_size_bytes": file_path.stat().st_size
            }
        }

    return {
        "result": "pass",
        "reason": f"All {len(required_strings)} required sections found",
        "details": {
            "file": str(file_path),
            "found_sections": found_sections,
            "file_size_bytes": file_path.stat().st_size
        }
    }


def validate_file_contains(
    directory: str | None,
    pattern: str | None,
    file_path: str | None,
    required_strings: list[str]
) -> dict:
    """
    Main validation function.

    Either (directory + pattern) or file_path must be provided.
    """
    # Determine target file
    if file_path:
        target = Path(file_path)
        if not target.exists():
            return {
                "result": "error",
                "reason": f"File not found: {file_path}",
                "details": {"file": file_path}
            }
    elif directory and pattern:
        dir_path = Path(directory)
        if not dir_path.exists():
            return {
                "result": "error",
                "reason": f"Directory not found: {directory}",
                "details": {"directory": directory, "pattern": pattern}
            }

        target = find_newest_file(directory, pattern)
        if not target:
            return {
                "result": "fail",
                "reason": f"No files matching pattern '{pattern}' in {directory}",
                "details": {"directory": directory, "pattern": pattern}
            }
    else:
        return {
            "result": "error",
            "reason": "Must provide either --file or (--directory + --pattern)",
            "details": {}
        }

    return check_file_contains(target, required_strings)


def main():
    parser = argparse.ArgumentParser(
        description="Validate that files contain required sections"
    )

    # File selection (mutually exclusive groups)
    file_group = parser.add_argument_group('File selection')
    file_group.add_argument(
        "--file", "-f",
        help="Specific file to check"
    )
    file_group.add_argument(
        "--directory", "-d",
        help="Directory to search for files"
    )
    file_group.add_argument(
        "--pattern", "-p",
        help="Glob pattern for file selection (used with --directory)"
    )

    # Required content
    parser.add_argument(
        "--contains", "-c",
        action="append",
        required=True,
        help="String that must be present in file (can be specified multiple times)"
    )
    parser.add_argument(
        "--json-output", "-j",
        action="store_true",
        help="Output JSON only (for hook parsing)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.file and not (args.directory and args.pattern):
        parser.error("Must provide either --file or (--directory + --pattern)")

    result = validate_file_contains(
        args.directory,
        args.pattern,
        args.file,
        args.contains
    )

    # Output JSON for hook parsing
    print(json.dumps(result, indent=2))

    # Set exit code based on result
    if result["result"] == "pass":
        sys.exit(0)
    elif result["result"] == "error":
        sys.exit(2)
    else:  # fail
        sys.exit(1)


if __name__ == "__main__":
    main()
