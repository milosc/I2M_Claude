#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Validate Discovery Output - HTEC Stage Validator

Comprehensive validation of Discovery stage outputs.
Checks that all required deliverables exist and contain expected sections.

Exit Codes:
- 0: All Discovery outputs valid
- 1: One or more outputs missing or incomplete (blocks Stop)
- 2: Critical error (directory not found, invalid arguments)

Usage:
    # Full Discovery validation
    uv run validate_discovery_output.py --system-name MySystem

    # Validate specific phase
    uv run validate_discovery_output.py --system-name MySystem --phase personas

    # Quick validation (essential files only)
    uv run validate_discovery_output.py --system-name MySystem --quick
"""

import argparse
import glob
import json
import sys
from pathlib import Path


# Discovery output structure and requirements
DISCOVERY_REQUIREMENTS = {
    "init": {
        "folder": "",
        "files": [],  # Just folder structure
        "state_files": [
            "_state/discovery_config.json",
            "_state/discovery_progress.json",
        ]
    },
    "analysis": {
        "folder": "01-analysis",
        "files": [
            {"pattern": "ANALYSIS_SUMMARY.md", "contains": ["## Executive Summary", "## Key Findings"]}
        ],
        "registries": [
            "traceability/client_facts_registry.json",
            "traceability/pain_point_registry.json",
        ]
    },
    "personas": {
        "folder": "02-research",
        "files": [
            {"pattern": "persona-*.md", "min_count": 1, "contains": ["## Demographics", "## Goals", "## Frustrations"]}
        ],
        "registries": [
            "traceability/user_type_registry.json",
        ]
    },
    "jtbd": {
        "folder": "02-research",
        "files": [
            {"pattern": "jtbd-jobs-to-be-done.md", "contains": ["## Job Statements", "When I", "I want to", "So that"]}
        ],
        "registries": [
            "traceability/jtbd_registry.json",
        ]
    },
    "vision": {
        "folder": "03-strategy",
        "files": [
            {"pattern": "product-vision.md", "contains": ["## Vision Statement", "## Target Users"]}
        ]
    },
    "strategy": {
        "folder": "03-strategy",
        "files": [
            {"pattern": "product-strategy.md", "contains": ["## Strategic Goals", "## Key Initiatives"]}
        ]
    },
    "competitive_intelligence": {
        "folder": "03-strategy",
        "files": [
            {"pattern": "COMPETITIVE_LANDSCAPE.md", "contains": ["## Market Map", "## Competitor Categories"]},
            {"pattern": "THREAT_OPPORTUNITY_MATRIX.md", "contains": ["## Threat Scores", "## Opportunity Scores"]},
            {"pattern": "DIFFERENTIATION_BLUEPRINT.md", "contains": ["## Unique Selling Proposition", "## Positioning"]},
            {"pattern": "COMPETITIVE_INTELLIGENCE_SUMMARY.md", "contains": ["## Executive Summary", "## Key Insights"]}
        ]
    },
    "roadmap": {
        "folder": "03-strategy",
        "files": [
            {"pattern": "product-roadmap.md", "contains": ["## Phase", "## Milestones"]}
        ],
        "registries": [
            "traceability/requirements_registry.json",
        ]
    },
    "kpis": {
        "folder": "03-strategy",
        "files": [
            {"pattern": "kpis-and-goals.md", "contains": ["## KPIs", "## Success Metrics"]}
        ]
    },
    "screens": {
        "folder": "04-design-specs",
        "files": [
            {"pattern": "screen-definitions.md", "contains": ["## Screen", "### Components", "### Data Requirements"]}
        ],
        "registries": [
            "traceability/screen_registry.json",
        ]
    },
    "navigation": {
        "folder": "04-design-specs",
        "files": [
            {"pattern": "navigation-structure.md", "contains": ["## Navigation", "## Routes"]}
        ]
    },
    "data_fields": {
        "folder": "04-design-specs",
        "files": [
            {"pattern": "data-fields.md", "contains": ["## Data Model", "### Fields"]}
        ]
    },
    "components": {
        "folder": "04-design-specs",
        "files": [
            {"pattern": "ui-components.md", "contains": ["## Components", "### Props"]}
        ]
    },
    "interactions": {
        "folder": "04-design-specs",
        "files": [
            {"pattern": "interaction-patterns.md", "contains": ["## Interactions", "## Feedback"]}
        ]
    },
    "documentation": {
        "folder": "05-documentation",
        "files": [
            {"pattern": "INDEX.md", "contains": ["## Table of Contents"]},
            {"pattern": "README.md", "contains": ["## Overview"]},
            {"pattern": "VALIDATION_REPORT.md", "contains": ["## Validation Results"]}
        ]
    }
}

# Essential files for quick validation
ESSENTIAL_PHASES = ["analysis", "personas", "jtbd", "screens", "documentation"]


def find_files(directory: Path, pattern: str) -> list[Path]:
    """Find files matching pattern in directory."""
    full_pattern = str(directory / pattern)
    return [Path(p) for p in glob.glob(full_pattern)]


def check_file_contains(file_path: Path, required_strings: list[str]) -> tuple[bool, list[str]]:
    """Check if file contains all required strings. Returns (success, missing_strings)."""
    try:
        content = file_path.read_text(encoding='utf-8')
        missing = [s for s in required_strings if s not in content]
        return len(missing) == 0, missing
    except Exception:
        return False, required_strings


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
        state_path = base_dir.parent / state_file
        if not state_path.exists():
            issues.append(f"Missing state file: {state_file}")
        else:
            passed.append(f"{state_file} ✓")

    # Check registry files (relative to project root)
    for registry in requirements.get("registries", []):
        registry_path = base_dir.parent / registry
        if not registry_path.exists():
            issues.append(f"Missing registry: {registry}")
        else:
            passed.append(f"{registry} ✓")

    return {
        "phase": phase,
        "status": "fail" if issues else "pass",
        "issues": issues,
        "passed": passed
    }


def validate_discovery_output(system_name: str, phase: str | None = None, quick: bool = False) -> dict:
    """
    Validate Discovery stage outputs.

    Args:
        system_name: Name of the system (e.g., "MySystem")
        phase: Specific phase to validate (None for all)
        quick: If True, only validate essential phases

    Returns:
        dict with overall result and per-phase details
    """
    base_dir = Path(f"ClientAnalysis_{system_name}")

    if not base_dir.exists():
        return {
            "result": "error",
            "reason": f"Discovery folder not found: ClientAnalysis_{system_name}",
            "details": {"system_name": system_name}
        }

    # Determine which phases to validate
    if phase:
        if phase not in DISCOVERY_REQUIREMENTS:
            return {
                "result": "error",
                "reason": f"Unknown phase: {phase}. Valid phases: {', '.join(DISCOVERY_REQUIREMENTS.keys())}",
                "details": {"requested_phase": phase}
            }
        phases_to_check = {phase: DISCOVERY_REQUIREMENTS[phase]}
    elif quick:
        phases_to_check = {p: DISCOVERY_REQUIREMENTS[p] for p in ESSENTIAL_PHASES}
    else:
        phases_to_check = DISCOVERY_REQUIREMENTS

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
            "reason": f"All {len(phases_to_check)} Discovery phases validated successfully",
            "details": {
                "system_name": system_name,
                "phases_checked": list(phases_to_check.keys()),
                "phase_results": results
            }
        }
    else:
        return {
            "result": "fail",
            "reason": f"Discovery validation failed with {len(total_issues)} issues",
            "details": {
                "system_name": system_name,
                "phases_checked": list(phases_to_check.keys()),
                "issues": total_issues,
                "phase_results": results
            }
        }


def main():
    parser = argparse.ArgumentParser(
        description="Validate Discovery stage outputs for completeness"
    )
    parser.add_argument(
        "--system-name", "-s",
        required=True,
        help="Name of the system (used to find ClientAnalysis_<name>/ folder)"
    )
    parser.add_argument(
        "--phase", "-p",
        choices=list(DISCOVERY_REQUIREMENTS.keys()),
        help="Validate only a specific phase"
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="Quick validation (essential phases only: analysis, personas, jtbd, screens, docs)"
    )
    parser.add_argument(
        "--json-output", "-j",
        action="store_true",
        help="Output JSON only (for hook parsing)"
    )

    args = parser.parse_args()

    result = validate_discovery_output(
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
