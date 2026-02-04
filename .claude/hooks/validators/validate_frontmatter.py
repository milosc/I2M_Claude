#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["pyyaml"]
# ///

"""
Validate Frontmatter - HTEC Hook Validator

Checks that markdown files have valid YAML frontmatter with required fields.
Supports field patterns for validation (e.g., document_id must match "DISC-*").

Exit Codes:
- 0: Frontmatter valid with all required fields
- 1: Frontmatter invalid or missing required fields (blocks Stop)
- 2: Critical error (file not found, parse error)

Usage:
    # Check for required fields
    uv run validate_frontmatter.py \\
        --file ClientAnalysis_TestSystem/02-research/persona-01.md \\
        --requires document_id \\
        --requires version \\
        --requires created_at

    # Check with field patterns
    uv run validate_frontmatter.py \\
        --file ClientAnalysis_TestSystem/02-research/persona-01.md \\
        --requires "document_id:PER-*" \\
        --requires version \\
        --requires created_at

    # Check newest file in directory
    uv run validate_frontmatter.py \\
        --directory ClientAnalysis_TestSystem/02-research \\
        --pattern "persona-*.md" \\
        --requires document_id \\
        --requires version
"""

import argparse
import fnmatch
import glob
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

import yaml


class SafeJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles YAML types like date, datetime."""

    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, Path):
            return str(obj)
        return super().default(obj)


def extract_frontmatter(content: str) -> tuple[dict | None, str | None]:
    """
    Extract YAML frontmatter from markdown content.

    Returns:
        tuple of (frontmatter_dict, error_message)
    """
    # Match YAML frontmatter between --- markers
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None, "No YAML frontmatter found (must start with ---)"

    yaml_content = match.group(1)

    try:
        frontmatter = yaml.safe_load(yaml_content)
        if not isinstance(frontmatter, dict):
            return None, "Frontmatter must be a YAML dictionary"
        return frontmatter, None
    except yaml.YAMLError as e:
        return None, f"Invalid YAML in frontmatter: {e}"


def validate_field(frontmatter: dict, field_spec: str) -> tuple[bool, str]:
    """
    Validate a single field specification.

    field_spec can be:
    - "field_name" - just check existence
    - "field_name:pattern" - check existence and pattern match

    Returns:
        tuple of (is_valid, error_message)
    """
    if ":" in field_spec:
        field_name, pattern = field_spec.split(":", 1)
    else:
        field_name = field_spec
        pattern = None

    # Check field exists
    if field_name not in frontmatter:
        return False, f"Missing required field: {field_name}"

    value = frontmatter[field_name]

    # Check pattern if specified
    if pattern:
        str_value = str(value)
        if not fnmatch.fnmatch(str_value, pattern):
            return False, f"Field '{field_name}' value '{str_value}' does not match pattern '{pattern}'"

    return True, ""


def find_newest_file(directory: str, pattern: str) -> Path | None:
    """Find the most recently modified file matching pattern."""
    dir_path = Path(directory)
    full_pattern = str(dir_path / pattern)
    matches = glob.glob(full_pattern, recursive=True)

    if not matches:
        return None

    matches.sort(key=lambda x: Path(x).stat().st_mtime, reverse=True)
    return Path(matches[0])


def validate_frontmatter(
    file_path: str | None,
    directory: str | None,
    pattern: str | None,
    required_fields: list[str]
) -> dict:
    """
    Main validation function.

    Returns:
        dict with 'result', 'reason', 'details'
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

    # Read file content
    try:
        content = target.read_text(encoding='utf-8')
    except Exception as e:
        return {
            "result": "error",
            "reason": f"Failed to read file: {e}",
            "details": {"file": str(target)}
        }

    # Extract frontmatter
    frontmatter, error = extract_frontmatter(content)
    if error:
        return {
            "result": "fail",
            "reason": error,
            "details": {"file": str(target)}
        }

    # Validate required fields
    validation_errors = []
    validated_fields = []

    for field_spec in required_fields:
        is_valid, error_msg = validate_field(frontmatter, field_spec)
        if is_valid:
            field_name = field_spec.split(":")[0]
            validated_fields.append({
                "field": field_name,
                "value": frontmatter.get(field_name)
            })
        else:
            validation_errors.append(error_msg)

    if validation_errors:
        return {
            "result": "fail",
            "reason": f"Frontmatter validation failed: {'; '.join(validation_errors)}",
            "details": {
                "file": str(target),
                "errors": validation_errors,
                "validated_fields": validated_fields,
                "frontmatter": frontmatter
            }
        }

    return {
        "result": "pass",
        "reason": f"Frontmatter valid with all {len(required_fields)} required fields",
        "details": {
            "file": str(target),
            "validated_fields": validated_fields,
            "frontmatter": frontmatter
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate YAML frontmatter in markdown files"
    )

    # File selection
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

    # Required fields
    parser.add_argument(
        "--requires", "-r",
        action="append",
        required=True,
        help="Required field (format: 'field_name' or 'field_name:pattern')"
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

    result = validate_frontmatter(
        args.file,
        args.directory,
        args.pattern,
        args.requires
    )

    # Output JSON for hook parsing
    print(json.dumps(result, indent=2, cls=SafeJSONEncoder))

    # Set exit code based on result
    if result["result"] == "pass":
        sys.exit(0)
    elif result["result"] == "error":
        sys.exit(2)
    else:  # fail
        sys.exit(1)


if __name__ == "__main__":
    main()
