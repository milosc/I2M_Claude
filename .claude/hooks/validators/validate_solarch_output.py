#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Validate SolArch Output - HTEC Stage Validator

Comprehensive validation of Solution Architecture stage outputs.
Checks that all required deliverables exist and contain expected sections.

Exit Codes:
- 0: All SolArch outputs valid
- 1: One or more outputs missing or incomplete (blocks Stop)
- 2: Critical error (directory not found, invalid arguments)

Usage:
    # Full SolArch validation
    uv run validate_solarch_output.py --system-name MySystem

    # Validate specific phase
    uv run validate_solarch_output.py --system-name MySystem --phase blocks

    # Quick validation (essential files only)
    uv run validate_solarch_output.py --system-name MySystem --quick
"""

import argparse
import glob
import json
import sys
from pathlib import Path


# SolArch output structure and requirements
SOLARCH_REQUIREMENTS = {
    "init": {
        "folder": "",
        "files": [],  # Just folder structure
        "subfolders": [
            "01-introduction-goals",
            "02-constraints",
            "03-context-scope",
            "04-solution-strategy",
            "05-building-blocks",
            "06-runtime",
            "07-quality",
            "08-deployment",
            "09-decisions",
            "10-risks",
            "11-glossary",
            "diagrams"
        ],
        "state_files": [
            "_state/solarch_config.json",
            "_state/solarch_progress.json",
        ]
    },
    "validate": {
        "folder": "_state",
        "files": [
            {"pattern": "solarch_progress.json", "contains": []}
        ],
        "check_progress_phase": 1
    },
    "context": {
        "folder": "",
        "files": [
            {"pattern": "01-introduction-goals/introduction.md", "contains": ["## Purpose", "## Stakeholders"]},
            {"pattern": "02-constraints/business-constraints.md", "contains": ["## Constraints"]},
            {"pattern": "03-context-scope/business-context.md", "contains": ["## Context"]}
        ]
    },
    "strategy": {
        "folder": "04-solution-strategy",
        "files": [
            {"pattern": "solution-strategy.md", "contains": ["## Architecture", "## Technology"]}
        ],
        "decisions_folder": "09-decisions",
        "adr_files": [
            {"pattern": "ADR-001-*.md", "contains": ["## Status", "## Decision"]},
            {"pattern": "ADR-002-*.md", "contains": ["## Status", "## Decision"]}
        ]
    },
    "blocks": {
        "folder": "05-building-blocks",
        "files": [
            {"pattern": "overview.md", "contains": ["## Level 1", "## Level 2"]}
        ],
        "subfolders": ["modules", "data-model"],
        "diagrams_files": [
            {"pattern": "c4-context.mermaid", "contains": []},
            {"pattern": "c4-container.mermaid", "contains": []}
        ]
    },
    "runtime": {
        "folder": "06-runtime",
        "files": [
            {"pattern": "api-design.md", "contains": ["## API", "## Endpoints"]},
            {"pattern": "event-communication.md", "contains": ["## Events"]}
        ]
    },
    "quality": {
        "folder": "07-quality",
        "files": [
            {"pattern": "quality-requirements.md", "contains": ["## Performance", "## Security"]},
            {"pattern": "testing-strategy.md", "contains": ["## Testing"]}
        ]
    },
    "deploy": {
        "folder": "08-deployment",
        "files": [
            {"pattern": "deployment-view.md", "contains": ["## Deployment"]},
            {"pattern": "operations-guide.md", "contains": ["## Operations"]}
        ]
    },
    "decisions": {
        "folder": "09-decisions",
        "files": [
            {"pattern": "INDEX.md", "contains": ["## Decision Log", "## Categories"]},
            {"pattern": "ADR-*.md", "min_count": 9, "contains": ["## Status", "## Context", "## Decision"]}
        ],
        "registry_files": [
            {"pattern": "_registry/decisions.json", "contains": []}
        ]
    },
    "risks": {
        "folder": "10-risks",
        "files": [
            {"pattern": "risks-technical-debt.md", "contains": ["## Risks", "## Technical Debt"]}
        ]
    },
    "docs": {
        "folder": "11-glossary",
        "files": [
            {"pattern": "glossary.md", "contains": ["## Terms", "## Definitions"]}
        ]
    },
    "trace": {
        "folder": "_registry",
        "files": [
            {"pattern": "architecture-traceability.json", "contains": []}
        ],
        "traceability_files": [
            {"pattern": "traceability/solarch_traceability_register.json", "contains": []}
        ]
    },
    "finalize": {
        "folder": "reports",
        "files": [
            {"pattern": "VALIDATION_REPORT.md", "contains": ["## Overview", "## Checkpoint Summary"]},
            {"pattern": "GENERATION_SUMMARY.md", "contains": ["## Executive Summary", "## Architecture Overview"]}
        ],
        "alt_folder": "_registry",  # Fallback for older structure
        "alt_files": [
            {"pattern": "VALIDATION_REPORT.md", "contains": ["## Overview"]},
            {"pattern": "GENERATION_SUMMARY.md", "contains": ["## Executive Summary"]}
        ]
    }
}

# Essential phases for quick validation
ESSENTIAL_PHASES = ["init", "blocks", "decisions", "trace", "finalize"]


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
    """Check if solarch progress has reached expected phase."""
    try:
        with open(progress_file) as f:
            progress = json.load(f)
        current = progress.get("current_checkpoint", 0)
        if current >= expected_phase:
            return True, f"Checkpoint {current} >= {expected_phase}"
        return False, f"Current checkpoint {current} < expected {expected_phase}"
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
        # Check for alt_folder fallback
        alt_folder = requirements.get("alt_folder")
        if alt_folder:
            alt_dir = base_dir / alt_folder
            if alt_dir.exists():
                phase_dir = alt_dir
                # Use alt_files if available
                if "alt_files" in requirements:
                    requirements = {**requirements, "files": requirements["alt_files"]}
            else:
                return {
                    "phase": phase,
                    "status": "fail",
                    "issues": [f"Folder not found: {folder} (or {alt_folder})"],
                    "passed": []
                }
        else:
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

    # Check state files (relative to project root, not SolArch folder)
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

    # Check registry files (in SolArch folder)
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

    # Check subfolders
    for subfolder in requirements.get("subfolders", []):
        subfolder_path = base_dir / subfolder
        if not subfolder_path.exists():
            issues.append(f"Missing subfolder: {subfolder}")
        else:
            passed.append(f"{subfolder}/ ✓")

    # Check diagrams files
    for diag_file in requirements.get("diagrams_files", []):
        pattern = diag_file["pattern"]
        diag_path = base_dir / "diagrams" / pattern
        if not diag_path.exists():
            issues.append(f"Missing diagram: diagrams/{pattern}")
        else:
            passed.append(f"diagrams/{pattern} ✓")

    # Check ADR files (in decisions folder)
    decisions_folder = requirements.get("decisions_folder")
    if decisions_folder:
        for adr_file in requirements.get("adr_files", []):
            pattern = adr_file["pattern"]
            adr_path = base_dir / decisions_folder / pattern
            matches = find_files(base_dir / decisions_folder, pattern)
            if not matches:
                issues.append(f"Missing ADR: {decisions_folder}/{pattern}")
            else:
                for match in matches:
                    required_sections = adr_file.get("contains", [])
                    if required_sections:
                        has_all, missing = check_file_contains(match, required_sections)
                        if not has_all:
                            issues.append(f"ADR {match.name} missing sections: {', '.join(missing)}")
                        else:
                            passed.append(f"{match.name} ✓")
                    else:
                        passed.append(f"{match.name} ✓")

    # Check progress phase if required
    if "check_progress_phase" in requirements:
        progress_file = base_dir.parent / "_state" / "solarch_progress.json"
        ok, msg = check_progress_phase(progress_file, requirements["check_progress_phase"])
        if not ok:
            issues.append(f"Progress check failed: {msg}")
        else:
            passed.append(f"Progress checkpoint check ✓")

    return {
        "phase": phase,
        "status": "fail" if issues else "pass",
        "issues": issues,
        "passed": passed
    }


def validate_solarch_output(system_name: str, phase: str | None = None, quick: bool = False) -> dict:
    """
    Validate SolArch stage outputs.

    Args:
        system_name: Name of the system (e.g., "MySystem")
        phase: Specific phase to validate (None for all)
        quick: If True, only validate essential phases

    Returns:
        dict with overall result and per-phase details
    """
    base_dir = Path(f"SolArch_{system_name}")

    if not base_dir.exists():
        return {
            "result": "error",
            "reason": f"SolArch folder not found: SolArch_{system_name}",
            "details": {"system_name": system_name}
        }

    # Determine which phases to validate
    if phase:
        if phase not in SOLARCH_REQUIREMENTS:
            return {
                "result": "error",
                "reason": f"Unknown phase: {phase}. Valid phases: {', '.join(SOLARCH_REQUIREMENTS.keys())}",
                "details": {"requested_phase": phase}
            }
        phases_to_check = {phase: SOLARCH_REQUIREMENTS[phase]}
    elif quick:
        phases_to_check = {p: SOLARCH_REQUIREMENTS[p] for p in ESSENTIAL_PHASES}
    else:
        phases_to_check = SOLARCH_REQUIREMENTS

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
            "reason": f"All {len(phases_to_check)} SolArch phases validated successfully",
            "details": {
                "system_name": system_name,
                "phases_checked": list(phases_to_check.keys()),
                "phase_results": results
            }
        }
    else:
        return {
            "result": "fail",
            "reason": f"SolArch validation failed with {len(total_issues)} issues",
            "details": {
                "system_name": system_name,
                "phases_checked": list(phases_to_check.keys()),
                "issues": total_issues,
                "phase_results": results
            }
        }


def main():
    parser = argparse.ArgumentParser(
        description="Validate SolArch stage outputs for completeness"
    )
    parser.add_argument(
        "--system-name", "-s",
        required=True,
        help="Name of the system (used to find SolArch_<name>/ folder)"
    )
    parser.add_argument(
        "--phase", "-p",
        choices=list(SOLARCH_REQUIREMENTS.keys()),
        help="Validate only a specific phase"
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Quick validation (essential phases only: init, blocks, decisions, trace, finalize)"
    )
    parser.add_argument(
        "--json-output", "-j",
        action="store_true",
        help="Output JSON only (for hook parsing)"
    )

    args = parser.parse_args()

    result = validate_solarch_output(
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
