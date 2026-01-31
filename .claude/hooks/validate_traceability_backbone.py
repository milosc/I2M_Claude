#!/usr/bin/env python3
"""
Traceability Backbone Validator

Validates that core traceability registries exist in the ROOT traceability/ folder.
Used as CP-0 validation before orchestrators run to ensure the backbone is ready.

Usage:
    python3 .claude/hooks/validate_traceability_backbone.py [--repair] [--stage STAGE] [--json]

Options:
    --repair     Auto-invoke /traceability-init --repair if backbone missing
    --stage      Filter required registries by stage (discovery, prototype, productspecs, solarch, implementation)
    --json       Output results as JSON

Exit Codes:
    0 - Backbone valid
    1 - Backbone missing registries (or repair failed)

Version: 1.0.0
Created: 2026-01-29
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Core registries required for traceability backbone (from _schema_index.json)
CORE_REGISTRIES = {
    "discovery": [
        "pain_point_registry.json",
        "jtbd_registry.json",
        "user_type_registry.json",
    ],
    "prototype": [
        "requirements_registry.json",
        "screen_registry.json",
    ],
    "productspecs": [
        "module_registry.json",
        "nfr_registry.json",
        "test_case_registry.json",
    ],
    "solarch": [
        "component_registry.json",
        "adr_registry.json",
    ],
    "aggregation": [
        "trace_links.json",
        "traceability_matrix_master.json",
    ]
}

# Registries needed before each stage can run
STAGE_PREREQUISITES = {
    "discovery": [],  # Discovery is the first stage, no prerequisites
    "prototype": ["discovery"],
    "productspecs": ["discovery", "prototype"],
    "solarch": ["discovery", "prototype", "productspecs"],
    "implementation": ["discovery", "prototype", "productspecs", "solarch"],
}


def get_project_root():
    """Get the project root directory."""
    # Try CLAUDE_PROJECT_DIR first
    if "CLAUDE_PROJECT_DIR" in os.environ:
        return Path(os.environ["CLAUDE_PROJECT_DIR"])

    # Fall back to current working directory
    return Path.cwd()


def get_traceability_path(project_root):
    """Get the traceability folder path."""
    return project_root / "traceability"


def check_registry_exists(traceability_path, registry_file):
    """Check if a registry file exists and has content."""
    file_path = traceability_path / registry_file

    if not file_path.exists():
        return {
            "status": "missing",
            "file": registry_file,
            "path": str(file_path)
        }

    # Check if file has content
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            if not content:
                return {
                    "status": "empty",
                    "file": registry_file,
                    "path": str(file_path)
                }

            # For JSON files, check if valid and has items
            if registry_file.endswith('.json'):
                data = json.loads(content)
                # Check for common registry patterns
                has_items = (
                    "items" in data or
                    "requirements" in data or
                    "pain_points" in data or
                    "jtbds" in data or
                    "modules" in data or
                    "nfrs" in data or
                    "test_cases" in data or
                    "components" in data or
                    "adrs" in data or
                    "links" in data or
                    "coverage" in data
                )
                if not has_items and "schema_version" not in data:
                    return {
                        "status": "empty_registry",
                        "file": registry_file,
                        "path": str(file_path),
                        "note": "File exists but appears to be uninitialized"
                    }

    except json.JSONDecodeError as e:
        return {
            "status": "invalid_json",
            "file": registry_file,
            "path": str(file_path),
            "error": str(e)
        }
    except Exception as e:
        return {
            "status": "error",
            "file": registry_file,
            "path": str(file_path),
            "error": str(e)
        }

    return {
        "status": "valid",
        "file": registry_file,
        "path": str(file_path)
    }


def validate_backbone(traceability_path, stage=None):
    """Validate the traceability backbone.

    Args:
        traceability_path: Path to traceability folder
        stage: Optional stage to filter prerequisites

    Returns:
        dict with validation results
    """
    results = {
        "valid": True,
        "traceability_folder_exists": traceability_path.exists(),
        "checked_at": datetime.now().isoformat(),
        "missing": [],
        "empty": [],
        "invalid": [],
        "valid_registries": [],
        "repair_needed": False
    }

    if not results["traceability_folder_exists"]:
        results["valid"] = False
        results["repair_needed"] = True
        results["error"] = "traceability/ folder does not exist"
        return results

    # Determine which stages to check based on prerequisites
    stages_to_check = ["aggregation"]  # Always check aggregation

    if stage:
        # Add prerequisite stages
        prerequisites = STAGE_PREREQUISITES.get(stage, [])
        stages_to_check.extend(prerequisites)
        stages_to_check.append(stage)
    else:
        # Check all stages
        stages_to_check.extend(CORE_REGISTRIES.keys())

    # Remove duplicates while preserving order
    seen = set()
    stages_to_check = [x for x in stages_to_check if not (x in seen or seen.add(x))]

    # Check each required registry
    for check_stage in stages_to_check:
        if check_stage not in CORE_REGISTRIES:
            continue

        for registry in CORE_REGISTRIES[check_stage]:
            result = check_registry_exists(traceability_path, registry)

            if result["status"] == "valid":
                results["valid_registries"].append(result)
            elif result["status"] == "missing":
                results["missing"].append(result)
                results["valid"] = False
            elif result["status"] in ["empty", "empty_registry"]:
                results["empty"].append(result)
                # Empty is a warning, not a failure
            elif result["status"] in ["invalid_json", "error"]:
                results["invalid"].append(result)
                results["valid"] = False

    # Repair needed if any missing registries
    results["repair_needed"] = len(results["missing"]) > 0 or len(results["invalid"]) > 0

    # Summary
    results["summary"] = {
        "valid_count": len(results["valid_registries"]),
        "missing_count": len(results["missing"]),
        "empty_count": len(results["empty"]),
        "invalid_count": len(results["invalid"]),
        "total_checked": (
            len(results["valid_registries"]) +
            len(results["missing"]) +
            len(results["empty"]) +
            len(results["invalid"])
        )
    }

    return results


def print_human_readable(results):
    """Print results in human-readable format."""
    print("═" * 60)
    print(" TRACEABILITY BACKBONE VALIDATION")
    print("═" * 60)
    print()

    if results["valid"]:
        print("✅ Backbone VALID")
    else:
        print("❌ Backbone INVALID")

    print()
    print(f"Checked: {results['summary']['total_checked']} registries")
    print(f"Valid:   {results['summary']['valid_count']}")
    print(f"Missing: {results['summary']['missing_count']}")
    print(f"Empty:   {results['summary']['empty_count']}")
    print(f"Invalid: {results['summary']['invalid_count']}")
    print()

    if results["missing"]:
        print("Missing registries:")
        for item in results["missing"]:
            print(f"  ❌ {item['file']}")
        print()

    if results["empty"]:
        print("Empty/uninitialized registries:")
        for item in results["empty"]:
            print(f"  ⚠️  {item['file']}")
        print()

    if results["invalid"]:
        print("Invalid registries:")
        for item in results["invalid"]:
            print(f"  ❌ {item['file']}: {item.get('error', 'unknown error')}")
        print()

    if results["repair_needed"]:
        print("═" * 60)
        print("REPAIR NEEDED")
        print("Run: /traceability-init --repair")
        print("═" * 60)

    print()


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate traceability backbone registries"
    )
    parser.add_argument(
        "--repair",
        action="store_true",
        help="Auto-invoke repair if backbone missing"
    )
    parser.add_argument(
        "--stage",
        choices=["discovery", "prototype", "productspecs", "solarch", "implementation"],
        help="Filter validation by stage prerequisites"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Get paths
    project_root = get_project_root()
    traceability_path = get_traceability_path(project_root)

    # Run validation
    results = validate_backbone(traceability_path, stage=args.stage)

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_human_readable(results)

    # Handle repair request
    if args.repair and results["repair_needed"]:
        print("Auto-repair requested but not yet implemented.")
        print("Please run: /traceability-init --repair")
        # Future: Could invoke /traceability-init programmatically

    # Exit code
    sys.exit(0 if results["valid"] else 1)


if __name__ == "__main__":
    main()
