#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Validate Files Exist - HTEC Hook Validator

Checks that required files matching glob patterns exist in a directory.
Used by Stop hooks to block command completion until outputs are present.

Exit Codes:
- 0: All required files exist
- 1: One or more required files missing (blocks Stop)
- 2: Critical error (invalid arguments, directory not found)

Usage:
    uv run validate_files_exist.py --directory <path> --requires "pattern1" --requires "pattern2"

Example:
    uv run validate_files_exist.py \\
        --directory ClientAnalysis_TestSystem/02-research \\
        --requires "persona-*.md" \\
        --requires "jtbd-*.md"
"""

import argparse
import glob
import json
import sys
from pathlib import Path


def validate_files_exist(directory: str, patterns: list[str]) -> dict:
    """
    Check that files matching all patterns exist in directory.

    Args:
        directory: Path to directory to check
        patterns: List of glob patterns (relative to directory)

    Returns:
        dict with 'result' (pass/fail), 'reason', 'details'
    """
    dir_path = Path(directory)

    if not dir_path.exists():
        return {
            "result": "error",
            "reason": f"Directory not found: {directory}",
            "details": {"directory": directory, "patterns": patterns}
        }

    if not dir_path.is_dir():
        return {
            "result": "error",
            "reason": f"Path is not a directory: {directory}",
            "details": {"directory": directory, "patterns": patterns}
        }

    missing_patterns = []
    found_files = {}

    for pattern in patterns:
        # Use glob to find matching files
        full_pattern = str(dir_path / pattern)
        matches = glob.glob(full_pattern, recursive=True)

        if not matches:
            missing_patterns.append(pattern)
        else:
            found_files[pattern] = [str(Path(m).relative_to(dir_path)) for m in matches]

    if missing_patterns:
        return {
            "result": "fail",
            "reason": f"Missing files for patterns: {', '.join(missing_patterns)}",
            "details": {
                "directory": directory,
                "missing_patterns": missing_patterns,
                "found_files": found_files
            }
        }

    return {
        "result": "pass",
        "reason": f"All {len(patterns)} required file patterns found",
        "details": {
            "directory": directory,
            "found_files": found_files
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate that required files exist in a directory"
    )
    parser.add_argument(
        "--directory", "-d",
        required=True,
        help="Directory to check for files"
    )
    parser.add_argument(
        "--requires", "-r",
        action="append",
        required=True,
        help="Glob pattern for required files (can be specified multiple times)"
    )
    parser.add_argument(
        "--json-output", "-j",
        action="store_true",
        help="Output JSON only (for hook parsing)"
    )

    args = parser.parse_args()

    result = validate_files_exist(args.directory, args.requires)

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
