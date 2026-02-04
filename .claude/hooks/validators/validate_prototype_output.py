#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Validate Prototype Output - HTEC Stage Validator

Comprehensive validation of Prototype stage outputs.
Checks that all required deliverables exist and contain expected sections.

Exit Codes:
- 0: All Prototype outputs valid
- 1: One or more outputs missing or incomplete (blocks Stop)
- 2: Critical error (directory not found, invalid arguments)

Usage:
    # Full Prototype validation
    uv run validate_prototype_output.py --system-name MySystem

    # Validate specific phase
    uv run validate_prototype_output.py --system-name MySystem --phase components

    # Quick validation (essential files only)
    uv run validate_prototype_output.py --system-name MySystem --quick
"""

import argparse
import glob
import json
import sys
from pathlib import Path


# Prototype output structure and requirements
PROTOTYPE_REQUIREMENTS = {
    "init": {
        "folder": "",
        "files": [],  # Just folder structure
        "state_files": [
            "_state/prototype_config.json",
            "_state/prototype_progress.json",
        ]
    },
    "validate_discovery": {
        "folder": "_state",
        "files": [
            {"pattern": "discovery_summary.json", "contains": []}
        ]
    },
    "requirements": {
        "folder": "_state",
        "files": [
            {"pattern": "requirements_registry.json", "contains": []}
        ]
    },
    "data_model": {
        "folder": "04-implementation",
        "files": [
            {"pattern": "data-model.md", "contains": ["## Entity", "## Relationships"]}
        ]
    },
    "api_contracts": {
        "folder": "04-implementation",
        "files": [
            {"pattern": "api-contracts.json", "contains": []}
        ]
    },
    "test_data": {
        "folder": "04-implementation/test-data",
        "files": [
            {"pattern": "*.json", "min_count": 1}
        ]
    },
    "design_brief": {
        "folder": "00-foundation",
        "files": [
            {"pattern": "design-brief.md", "contains": ["## Project Overview", "## Visual Direction"]},
            {"pattern": "design-principles.md", "contains": ["## ", "Rationale"]}
        ]
    },
    "design_tokens": {
        "folder": "00-foundation",
        "files": [
            {"pattern": "design-tokens.json", "contains": []},
            {"pattern": "color-system.md", "contains": ["## ", "Palette"]},
            {"pattern": "typography.md", "contains": ["## Font", "## Type Scale"]}
        ]
    },
    "components": {
        "folder": "01-components",
        "files": [
            {"pattern": "component-index.md", "contains": ["## Overview", "## Component Count"]}
        ],
        "subfolders": ["primitives", "data-display", "feedback"]
    },
    "screens": {
        "folder": "02-screens",
        "files": [
            {"pattern": "screen-index.md", "contains": ["## Screen Inventory", "## Screen Flow"]}
        ],
        "screen_folders": True  # At least one screen folder expected
    },
    "interactions": {
        "folder": "03-interactions",
        "files": [
            {"pattern": "motion-system.md", "contains": ["## Animation", "## Transition"]},
            {"pattern": "accessibility-spec.md", "contains": ["## Keyboard", "## Screen Reader"]}
        ]
    },
    "sequencer": {
        "folder": "04-implementation",
        "files": [
            {"pattern": "build-sequence.md", "contains": ["## Build Order", "## Dependencies"]}
        ]
    },
    "codegen": {
        "folder": "prototype",
        "files": [
            {"pattern": "package.json", "contains": []},
            {"pattern": "src/App.tsx", "contains": []}
        ],
        "subfolders": ["src/components", "src/pages"]
    },
    "qa": {
        "folder": "05-validation",
        "files": [
            {"pattern": "qa-report.md", "contains": ["## Test Results", "## Coverage"]}
        ]
    },
    "ui_audit": {
        "folder": "05-validation",
        "files": [
            {"pattern": "ui-audit-report.md", "contains": ["## Visual Audit", "## Issues"]}
        ],
        "subfolders": ["screenshots"]
    }
}

# Essential files for quick validation
ESSENTIAL_PHASES = ["init", "requirements", "design_tokens", "components", "screens", "codegen"]


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


def check_screen_folders(screens_dir: Path) -> tuple[bool, list[str]]:
    """Check that at least one screen folder exists with expected files."""
    if not screens_dir.exists():
        return False, ["02-screens folder not found"]

    # Look for screen folders (any subfolder that's not screen-index.md related)
    screen_folders = [d for d in screens_dir.iterdir()
                     if d.is_dir() and not d.name.startswith('.')]

    if not screen_folders:
        return False, ["No screen folders found in 02-screens/"]

    issues = []
    for folder in screen_folders:
        # Check for essential files in each screen folder
        # Assembly-First mode: specification.md, component-usage.md, data-requirements.md
        # Traditional mode: layout.md, components.md, data-requirements.md
        has_spec = (folder / "specification.md").exists() or (folder / "layout.md").exists()
        has_data = (folder / "data-requirements.md").exists()

        if not has_spec:
            issues.append(f"Screen folder {folder.name} missing specification/layout file")
        if not has_data:
            issues.append(f"Screen folder {folder.name} missing data-requirements.md")

    return len(issues) == 0, issues


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

    # Check state files (relative to project root)
    for state_file in requirements.get("state_files", []):
        # State files are relative to Prototype folder for prototype stage
        state_path = base_dir / state_file
        if not state_path.exists():
            # Also check at project root
            root_state_path = base_dir.parent / state_file
            if not root_state_path.exists():
                issues.append(f"Missing state file: {state_file}")
            else:
                passed.append(f"{state_file} ✓")
        else:
            passed.append(f"{state_file} ✓")

    # Check subfolders
    for subfolder in requirements.get("subfolders", []):
        subfolder_path = phase_dir / subfolder
        if not subfolder_path.exists():
            issues.append(f"Missing subfolder: {folder}/{subfolder}")
        else:
            passed.append(f"{subfolder}/ ✓")

    # Check screen folders if required
    if requirements.get("screen_folders"):
        screen_ok, screen_issues = check_screen_folders(phase_dir)
        if not screen_ok:
            issues.extend(screen_issues)
        else:
            passed.append("Screen folders validated ✓")

    return {
        "phase": phase,
        "status": "fail" if issues else "pass",
        "issues": issues,
        "passed": passed
    }


def validate_prototype_output(system_name: str, phase: str | None = None, quick: bool = False) -> dict:
    """
    Validate Prototype stage outputs.

    Args:
        system_name: Name of the system (e.g., "MySystem")
        phase: Specific phase to validate (None for all)
        quick: If True, only validate essential phases

    Returns:
        dict with overall result and per-phase details
    """
    base_dir = Path(f"Prototype_{system_name}")

    if not base_dir.exists():
        return {
            "result": "error",
            "reason": f"Prototype folder not found: Prototype_{system_name}",
            "details": {"system_name": system_name}
        }

    # Determine which phases to validate
    if phase:
        if phase not in PROTOTYPE_REQUIREMENTS:
            return {
                "result": "error",
                "reason": f"Unknown phase: {phase}. Valid phases: {', '.join(PROTOTYPE_REQUIREMENTS.keys())}",
                "details": {"requested_phase": phase}
            }
        phases_to_check = {phase: PROTOTYPE_REQUIREMENTS[phase]}
    elif quick:
        phases_to_check = {p: PROTOTYPE_REQUIREMENTS[p] for p in ESSENTIAL_PHASES}
    else:
        phases_to_check = PROTOTYPE_REQUIREMENTS

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
            "reason": f"All {len(phases_to_check)} Prototype phases validated successfully",
            "details": {
                "system_name": system_name,
                "phases_checked": list(phases_to_check.keys()),
                "phase_results": results
            }
        }
    else:
        return {
            "result": "fail",
            "reason": f"Prototype validation failed with {len(total_issues)} issues",
            "details": {
                "system_name": system_name,
                "phases_checked": list(phases_to_check.keys()),
                "issues": total_issues,
                "phase_results": results
            }
        }


def main():
    parser = argparse.ArgumentParser(
        description="Validate Prototype stage outputs for completeness"
    )
    parser.add_argument(
        "--system-name", "-s",
        required=True,
        help="Name of the system (used to find Prototype_<name>/ folder)"
    )
    parser.add_argument(
        "--phase", "-p",
        choices=list(PROTOTYPE_REQUIREMENTS.keys()),
        help="Validate only a specific phase"
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Quick validation (essential phases only: init, requirements, design_tokens, components, screens, codegen)"
    )
    parser.add_argument(
        "--json-output", "-j",
        action="store_true",
        help="Output JSON only (for hook parsing)"
    )

    args = parser.parse_args()

    result = validate_prototype_output(
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
