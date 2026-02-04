#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Validate ProductSpecs Output - HTEC Stage Validator

Comprehensive validation of ProductSpecs stage outputs.
Checks that all required deliverables exist and contain expected sections.

Exit Codes:
- 0: All ProductSpecs outputs valid
- 1: One or more outputs missing or incomplete (blocks Stop)
- 2: Critical error (directory not found, invalid arguments)

Usage:
    # Full ProductSpecs validation
    uv run validate_productspecs_output.py --system-name MySystem

    # Validate specific phase
    uv run validate_productspecs_output.py --system-name MySystem --phase modules

    # Quick validation (essential files only)
    uv run validate_productspecs_output.py --system-name MySystem --quick
"""

import argparse
import glob
import json
import sys
from pathlib import Path


# ProductSpecs output structure and requirements
PRODUCTSPECS_REQUIREMENTS = {
    "init": {
        "folder": "",
        "files": [],  # Just folder structure
        "subfolders": ["00-overview", "01-modules", "02-api", "03-tests", "04-jira"],
        "state_files": [
            "_state/productspecs_config.json",
            "_state/productspecs_progress.json",
        ]
    },
    "validate": {
        "folder": "_state",
        "files": [
            {"pattern": "productspecs_progress.json", "contains": []}
        ],
        "check_progress_phase": 1
    },
    "extract": {
        "folder": "",
        "files": [],
        "registry_files": [
            {"pattern": "_registry/requirements.json", "contains": []},
        ],
        "traceability_files": [
            {"pattern": "traceability/requirements_registry.json", "contains": []},
        ]
    },
    "modules_core": {
        "folder": "01-modules",
        "files": [
            {"pattern": "module-index.md", "contains": ["## Modules by Priority", "## Traceability"]}
        ]
    },
    "modules_extended": {
        "folder": "01-modules",
        "files": [
            {"pattern": "MOD-*.md", "min_count": 1, "contains": ["## 1. Traceability", "## 2. Screen Specifications"]}
        ],
        "registry_files": [
            {"pattern": "_registry/modules.json", "contains": []}
        ]
    },
    "contracts": {
        "folder": "02-api",
        "files": [
            {"pattern": "api-index.md", "contains": ["## API", "## Endpoints"]},
            {"pattern": "NFR_SPECIFICATIONS.md", "contains": ["## Performance", "## Security"]},
            {"pattern": "data-contracts.md", "contains": ["## Data", "## Contract"]}
        ],
        "registry_files": [
            {"pattern": "_registry/nfrs.json", "contains": []}
        ]
    },
    "tests": {
        "folder": "03-tests",
        "files": [
            {"pattern": "test-case-registry.md", "contains": ["## Summary", "## Coverage"]},
            {"pattern": "e2e-scenarios.md", "contains": ["## Critical Paths", "Feature:"]},
            {"pattern": "accessibility-checklist.md", "contains": ["## Screen Checklist", "WCAG"]}
        ],
        "registry_files": [
            {"pattern": "_registry/test-cases.json", "contains": []}
        ]
    },
    "traceability": {
        "folder": "00-overview",
        "files": [
            {"pattern": "TRACEABILITY_MATRIX.md", "contains": ["## P0 Requirements", "## Coverage Summary"]},
            {"pattern": "VALIDATION_REPORT.md", "contains": ["## Executive Summary", "## Detailed Results"]}
        ],
        "registry_files": [
            {"pattern": "_registry/traceability.json", "contains": []}
        ]
    },
    "export": {
        "folder": "04-jira",
        "files": [
            {"pattern": "IMPORT_GUIDE.md", "contains": ["## Prerequisites", "## Import Steps"]},
            {"pattern": "full-hierarchy.csv", "contains": []},
            {"pattern": "epics-and-stories.csv", "contains": []},
            {"pattern": "jira-import.json", "contains": []}
        ],
        "overview_files": [
            {"pattern": "00-overview/GENERATION_SUMMARY.md", "contains": ["## Summary", "## Statistics"]}
        ]
    }
}

# Essential phases for quick validation
ESSENTIAL_PHASES = ["init", "modules_core", "modules_extended", "tests", "traceability"]


def find_files(directory: Path, pattern: str) -> list[Path]:
    """Find files matching pattern in directory."""
    full_pattern = str(directory / pattern)
    return [Path(p) for p in glob.glob(full_pattern)]


def check_file_contains(file_path: Path, required_strings: list[str]) -> tuple[bool, list[str]]:
    """Check if file contains all required strings. Returns (success, missing_strings)."""
    if not required_strings:
        return True, []
    try:
        content = file_path.read_text(encoding='utf-8')
        missing = [s for s in required_strings if s not in content]
        return len(missing) == 0, missing
    except Exception:
        return False, required_strings


def check_subfolder_exists(base_dir: Path, subfolder: str) -> bool:
    """Check if a subfolder exists."""
    return (base_dir / subfolder).exists()


def check_progress_phase(progress_file: Path, expected_phase: int) -> tuple[bool, str]:
    """Check if productspecs progress has reached expected phase."""
    try:
        with open(progress_file) as f:
            progress = json.load(f)
        current = progress.get("current_phase", 0)
        if current >= expected_phase:
            return True, f"Phase {current} >= {expected_phase}"
        return False, f"Current phase {current} < expected {expected_phase}"
    except Exception as e:
        return False, f"Cannot read progress: {e}"


def validate_phase(base_dir: Path, phase: str, requirements: dict) -> dict:
    """Validate a single phase's outputs."""
    issues = []
    passed = []

    folder = requirements.get("folder", "")
    phase_dir = base_dir / folder if folder else base_dir

    # Check folder exists (if specified)
    if folder and not phase_dir.exists():
        return {
            "phase": phase,
            "status": "fail",
            "issues": [f"Folder not found: {folder}"],
            "passed": []
        }

    # Check required files
    for file_req in requirements.get("files", []):
        pattern = file_req["pattern"]
        min_count = file_req.get("min_count", 1)
        required_sections = file_req.get("contains", [])

        matches = find_files(phase_dir, pattern)

        if len(matches) < min_count:
            issues.append(f"Missing: {pattern} (found {len(matches)}, need {min_count})")
            continue

        # Check each file for required sections
        for match in matches:
            if required_sections:
                has_all, missing = check_file_contains(match, required_sections)
                if not has_all:
                    issues.append(f"File {match.name} missing sections: {', '.join(missing)}")
                else:
                    passed.append(f"{match.name} ✓")
            else:
                passed.append(f"{match.name} ✓")

    # Check state files (relative to project root, not ProductSpecs folder)
    for state_file in requirements.get("state_files", []):
        # State files are relative to project root
        state_path = base_dir.parent / state_file
        if not state_path.exists():
            # Also check relative to base_dir
            alt_path = base_dir / state_file
            if not alt_path.exists():
                issues.append(f"Missing state file: {state_file}")
            else:
                passed.append(f"{state_file} ✓")
        else:
            passed.append(f"{state_file} ✓")

    # Check registry files (in ProductSpecs folder)
    for reg_file in requirements.get("registry_files", []):
        pattern = reg_file["pattern"]
        reg_path = base_dir / pattern
        if not reg_path.exists():
            # Check in traceability at root level
            root_path = base_dir.parent / pattern
            if not root_path.exists():
                issues.append(f"Missing registry: {pattern}")
            else:
                passed.append(f"{pattern} ✓ (root)")
        else:
            passed.append(f"{pattern} ✓")

    # Check traceability files (at project root)
    for trace_file in requirements.get("traceability_files", []):
        pattern = trace_file["pattern"]
        trace_path = base_dir.parent / pattern
        if not trace_path.exists():
            issues.append(f"Missing traceability file: {pattern}")
        else:
            passed.append(f"{pattern} ✓")

    # Check overview files (in ProductSpecs folder but different path)
    for overview_file in requirements.get("overview_files", []):
        pattern = overview_file["pattern"]
        overview_path = base_dir / pattern
        required_sections = overview_file.get("contains", [])
        if not overview_path.exists():
            issues.append(f"Missing overview file: {pattern}")
        else:
            if required_sections:
                has_all, missing = check_file_contains(overview_path, required_sections)
                if not has_all:
                    issues.append(f"File {pattern} missing sections: {', '.join(missing)}")
                else:
                    passed.append(f"{pattern} ✓")
            else:
                passed.append(f"{pattern} ✓")

    # Check subfolders
    for subfolder in requirements.get("subfolders", []):
        subfolder_path = base_dir / subfolder
        if not subfolder_path.exists():
            issues.append(f"Missing subfolder: {subfolder}")
        else:
            passed.append(f"{subfolder}/ ✓")

    # Check progress phase if required
    if "check_progress_phase" in requirements:
        progress_file = base_dir.parent / "_state" / "productspecs_progress.json"
        ok, msg = check_progress_phase(progress_file, requirements["check_progress_phase"])
        if not ok:
            issues.append(f"Progress check failed: {msg}")
        else:
            passed.append(f"Progress phase check ✓")

    return {
        "phase": phase,
        "status": "fail" if issues else "pass",
        "issues": issues,
        "passed": passed
    }


def validate_productspecs_output(system_name: str, phase: str | None = None, quick: bool = False) -> dict:
    """
    Validate ProductSpecs stage outputs.

    Args:
        system_name: Name of the system (e.g., "MySystem")
        phase: Specific phase to validate (None for all)
        quick: If True, only validate essential phases

    Returns:
        dict with overall result and per-phase details
    """
    base_dir = Path(f"ProductSpecs_{system_name}")

    if not base_dir.exists():
        return {
            "result": "error",
            "reason": f"ProductSpecs folder not found: ProductSpecs_{system_name}",
            "details": {"system_name": system_name}
        }

    # Determine which phases to validate
    if phase:
        if phase not in PRODUCTSPECS_REQUIREMENTS:
            return {
                "result": "error",
                "reason": f"Unknown phase: {phase}. Valid phases: {', '.join(PRODUCTSPECS_REQUIREMENTS.keys())}",
                "details": {"requested_phase": phase}
            }
        phases_to_check = {phase: PRODUCTSPECS_REQUIREMENTS[phase]}
    elif quick:
        phases_to_check = {p: PRODUCTSPECS_REQUIREMENTS[p] for p in ESSENTIAL_PHASES}
    else:
        phases_to_check = PRODUCTSPECS_REQUIREMENTS

    # Validate each phase
    results = []
    all_passed = True
    total_issues = []

    for phase_name, requirements in phases_to_check.items():
        result = validate_phase(base_dir, phase_name, requirements)
        results.append(result)
        if result["status"] != "pass":
            all_passed = False
            total_issues.extend([f"[{phase_name}] {issue}" for issue in result["issues"]])

    if all_passed:
        return {
            "result": "pass",
            "reason": f"All {len(phases_to_check)} ProductSpecs phases validated successfully",
            "details": {
                "system_name": system_name,
                "phases_checked": list(phases_to_check.keys()),
                "phase_results": results
            }
        }
    else:
        return {
            "result": "fail",
            "reason": f"ProductSpecs validation failed with {len(total_issues)} issues",
            "details": {
                "system_name": system_name,
                "phases_checked": list(phases_to_check.keys()),
                "issues": total_issues,
                "phase_results": results
            }
        }


def main():
    parser = argparse.ArgumentParser(
        description="Validate ProductSpecs stage outputs for completeness"
    )
    parser.add_argument(
        "--system-name", "-s",
        required=True,
        help="Name of the system (used to find ProductSpecs_<name>/ folder)"
    )
    parser.add_argument(
        "--phase", "-p",
        choices=list(PRODUCTSPECS_REQUIREMENTS.keys()),
        help="Validate only a specific phase"
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Quick validation (essential phases only: init, modules, tests, traceability)"
    )
    parser.add_argument(
        "--json-output", "-j",
        action="store_true",
        help="Output JSON only (for hook parsing)"
    )

    args = parser.parse_args()

    result = validate_productspecs_output(
        args.system_name,
        args.phase,
        args.quick
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
