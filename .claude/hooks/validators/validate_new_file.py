#!/usr/bin/env python3
"""
Validate New File Validator

Validates that a new file was created in a specified directory with a specific extension.
Used by planning commands to ensure plan documents are properly created.

Exit codes:
- 0: Validation passed
- 1: Validation failed (blocking)
- 2: Critical error (fatal)

Usage:
  uv run validate_new_file.py --directory <dir> --extension <ext>

Example:
  uv run validate_new_file.py --directory specs --extension .md
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def find_recent_files(directory: Path, extension: str, max_age_seconds: int = 300) -> list[Path]:
    """
    Find files in directory that were modified recently (within max_age_seconds).

    Args:
        directory: Directory to search
        extension: File extension to filter by (e.g., '.md')
        max_age_seconds: Maximum age in seconds to consider a file "recent"

    Returns:
        List of recently modified file paths
    """
    recent_files = []
    cutoff_time = datetime.now().timestamp() - max_age_seconds

    if not directory.exists():
        return recent_files

    for file_path in directory.rglob(f"*{extension}"):
        if file_path.is_file():
            mtime = file_path.stat().st_mtime
            if mtime >= cutoff_time:
                recent_files.append(file_path)

    return sorted(recent_files, key=lambda f: f.stat().st_mtime, reverse=True)


def validate_new_file(directory: str, extension: str, max_age_seconds: int = 300) -> tuple[bool, str, list[Path]]:
    """
    Validate that at least one new file was created in the directory.

    Args:
        directory: Directory path to check (relative to project root)
        extension: Required file extension (e.g., '.md')
        max_age_seconds: Maximum age in seconds to consider a file "new"

    Returns:
        Tuple of (success, message, list of found files)
    """
    # Get project root from CLAUDE_PROJECT_DIR or use cwd
    project_root = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))
    target_dir = project_root / directory

    if not target_dir.exists():
        return False, f"Directory '{directory}' does not exist", []

    recent_files = find_recent_files(target_dir, extension, max_age_seconds)

    if not recent_files:
        return False, f"No new {extension} files found in '{directory}' (within last {max_age_seconds}s)", []

    return True, f"Found {len(recent_files)} new {extension} file(s) in '{directory}'", recent_files


def main():
    parser = argparse.ArgumentParser(description="Validate that a new file was created")
    parser.add_argument(
        "--directory", "-d",
        required=True,
        help="Directory to check for new files (relative to project root)"
    )
    parser.add_argument(
        "--extension", "-e",
        required=True,
        help="Required file extension (e.g., '.md', '.json')"
    )
    parser.add_argument(
        "--max-age", "-m",
        type=int,
        default=300,
        help="Maximum age in seconds to consider a file 'new' (default: 300)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Ensure extension has leading dot
    extension = args.extension if args.extension.startswith(".") else f".{args.extension}"

    success, message, files = validate_new_file(
        args.directory,
        extension,
        args.max_age
    )

    if args.json:
        result = {
            "success": success,
            "message": message,
            "files": [str(f) for f in files],
            "directory": args.directory,
            "extension": extension,
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(result, indent=2))
    else:
        if success:
            print(f"✅ {message}")
            for f in files:
                print(f"   - {f.relative_to(Path(os.environ.get('CLAUDE_PROJECT_DIR', os.getcwd())))}")
        else:
            print(f"❌ {message}")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
