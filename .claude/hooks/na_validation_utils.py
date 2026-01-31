#!/usr/bin/env python3
"""
N/A (Not Applicable) Validation Utilities

Shared utilities for handling NOT_APPLICABLE artifacts across all quality gates.
This module provides:
1. Project classification loading
2. Artifact applicability checking
3. N/A file validation
4. N/A file detection

Usage in quality gates:
    from na_validation_utils import (
        get_project_classification,
        check_artifact_applicability,
        validate_na_file,
        is_na_file
    )
"""

import json
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple, List

# Project root for accessing shared resources
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Project types supported by the framework
PROJECT_TYPES = [
    "FULL_STACK",      # Full frontend + backend application
    "BACKEND_ONLY",    # API/service layer only, no UI
    "DATABASE_ONLY",   # Schema design, migrations, data modeling
    "INTEGRATION",     # Middleware, connectors, adapters
    "INFRASTRUCTURE"   # DevOps, IaC, platform engineering
]

# Default artifact applicability matrix
# True = artifact applies to this project type
# False = artifact should be marked N/A
ARTIFACT_APPLICABILITY = {
    "FULL_STACK": {
        "screen-definitions": True,
        "navigation-structure": True,
        "data-fields": True,
        "interaction-patterns": True,
        "ui-components": True,
        "PERSONAS": True,
        "JOBS_TO_BE_DONE": True,
        "PRODUCT_VISION": True,
        "PRODUCT_STRATEGY": True,
        "PRODUCT_ROADMAP": True,
        "KPIS_AND_GOALS": True,
        "PAIN_POINTS": True,
        "PDF_ANALYSIS": True,
        "prototype-code": True,
        "design-tokens": True,
        "component-specs": True
    },
    "BACKEND_ONLY": {
        "screen-definitions": False,
        "navigation-structure": False,
        "data-fields": True,
        "interaction-patterns": False,
        "ui-components": False,
        "PERSONAS": True,
        "JOBS_TO_BE_DONE": True,
        "PRODUCT_VISION": True,
        "PRODUCT_STRATEGY": True,
        "PRODUCT_ROADMAP": True,
        "KPIS_AND_GOALS": True,
        "PAIN_POINTS": True,
        "PDF_ANALYSIS": True,
        "prototype-code": False,
        "design-tokens": False,
        "component-specs": False
    },
    "DATABASE_ONLY": {
        "screen-definitions": False,
        "navigation-structure": False,
        "data-fields": True,
        "interaction-patterns": False,
        "ui-components": False,
        "PERSONAS": True,
        "JOBS_TO_BE_DONE": True,
        "PRODUCT_VISION": True,
        "PRODUCT_STRATEGY": True,
        "PRODUCT_ROADMAP": True,
        "KPIS_AND_GOALS": True,
        "PAIN_POINTS": True,
        "PDF_ANALYSIS": True,
        "prototype-code": False,
        "design-tokens": False,
        "component-specs": False
    },
    "INTEGRATION": {
        "screen-definitions": False,
        "navigation-structure": False,
        "data-fields": True,
        "interaction-patterns": False,
        "ui-components": False,
        "PERSONAS": True,
        "JOBS_TO_BE_DONE": True,
        "PRODUCT_VISION": True,
        "PRODUCT_STRATEGY": True,
        "PRODUCT_ROADMAP": True,
        "KPIS_AND_GOALS": True,
        "PAIN_POINTS": True,
        "PDF_ANALYSIS": True,
        "prototype-code": False,
        "design-tokens": False,
        "component-specs": False
    },
    "INFRASTRUCTURE": {
        "screen-definitions": False,
        "navigation-structure": False,
        "data-fields": False,
        "interaction-patterns": False,
        "ui-components": False,
        "PERSONAS": True,
        "JOBS_TO_BE_DONE": True,
        "PRODUCT_VISION": True,
        "PRODUCT_STRATEGY": True,
        "PRODUCT_ROADMAP": True,
        "KPIS_AND_GOALS": True,
        "PAIN_POINTS": True,
        "PDF_ANALYSIS": True,
        "prototype-code": False,
        "design-tokens": False,
        "component-specs": False
    }
}


def get_project_classification(state_dir: Optional[Path] = None) -> Optional[Dict]:
    """
    Load project classification from discovery_config.json.

    Args:
        state_dir: Path to _state directory. If None, uses PROJECT_ROOT/_state

    Returns:
        Project classification dict or None if not found/configured
    """
    if state_dir is None:
        state_dir = PROJECT_ROOT / "_state"

    config_path = state_dir / "discovery_config.json"
    if not config_path.exists():
        return None

    try:
        with open(config_path) as f:
            config = json.load(f)
        return config.get("project_classification", None)
    except Exception:
        return None


def check_artifact_applicability(
    artifact_name: str,
    project_type: Optional[str] = None,
    classification: Optional[Dict] = None
) -> bool:
    """
    Check if an artifact is applicable for the current project type.

    Args:
        artifact_name: Name of the artifact (e.g., "screen-definitions", "PERSONAS")
        project_type: Optional explicit project type. If None, loads from config
        classification: Optional pre-loaded classification dict

    Returns:
        True if artifact is applicable, False if it should be N/A
    """
    # Load classification if not provided
    if classification is None:
        classification = get_project_classification()

    # Default to FULL_STACK if no classification
    if classification is None:
        return True

    # Get project type
    if project_type is None:
        project_type = classification.get("type", "FULL_STACK")

    # Check custom applicability in classification first
    applicability = classification.get("artifact_applicability", {})

    # Normalize artifact name for lookup
    normalized = artifact_name.lower().replace("_", "-").replace(" ", "-")
    upper_name = artifact_name.upper().replace("-", "_")

    # Try custom applicability first
    if normalized in applicability:
        return applicability[normalized]
    if upper_name in applicability:
        return applicability[upper_name]
    if artifact_name in applicability:
        return applicability[artifact_name]

    # Fall back to default matrix
    default_applicability = ARTIFACT_APPLICABILITY.get(project_type, {})
    if normalized in default_applicability:
        return default_applicability[normalized]
    if upper_name in default_applicability:
        return default_applicability[upper_name]
    if artifact_name in default_applicability:
        return default_applicability[artifact_name]

    # Default to applicable
    return True


def validate_na_file(file_path: Path) -> Tuple[bool, str]:
    """
    Validate that a NOT_APPLICABLE file has correct format.

    N/A files must have:
    - Markdown: status: NOT_APPLICABLE in frontmatter, Reason section, Project Classification section
    - JSON: "status": "NOT_APPLICABLE", "reason", "project_type" keys

    Args:
        file_path: Path to the N/A file

    Returns:
        Tuple of (is_valid, message)
    """
    path = Path(file_path)
    if not path.exists():
        return False, f"N/A file {file_path} does not exist"

    try:
        content = path.read_text()
    except Exception as e:
        return False, f"Cannot read N/A file {file_path}: {e}"

    # Check for required markers
    if "status: NOT_APPLICABLE" not in content and '"status": "NOT_APPLICABLE"' not in content:
        return False, f"File {file_path} missing NOT_APPLICABLE status marker"

    # For markdown files, check for required sections
    if path.suffix == ".md":
        if "### Reason" not in content and "## Reason" not in content:
            return False, f"N/A markdown file {file_path} missing Reason section"
        if "### Project Classification" not in content and "## Project Classification" not in content:
            return False, f"N/A markdown file {file_path} missing Project Classification section"

    # For JSON files, check for required keys
    if path.suffix == ".json":
        try:
            data = json.loads(content)
            if "reason" not in data:
                return False, f"N/A JSON file {file_path} missing 'reason' key"
            if "project_type" not in data:
                return False, f"N/A JSON file {file_path} missing 'project_type' key"
        except json.JSONDecodeError as e:
            return False, f"N/A JSON file {file_path} is not valid JSON: {e}"

    return True, f"N/A file {file_path} is valid"


def is_na_file(file_path: Path) -> bool:
    """
    Check if a file is marked as NOT_APPLICABLE.

    Args:
        file_path: Path to the file to check

    Returns:
        True if file contains NOT_APPLICABLE status marker
    """
    path = Path(file_path)
    if not path.exists():
        return False

    try:
        content = path.read_text()
        return "status: NOT_APPLICABLE" in content or '"status": "NOT_APPLICABLE"' in content
    except Exception:
        return False


def get_na_artifacts(base_dir: Path, stage: str = "discovery") -> List[Dict]:
    """
    Scan a directory for N/A artifacts.

    Args:
        base_dir: Base directory to scan
        stage: Stage name ("discovery", "prototype", "productspecs", "solarch", "implementation")

    Returns:
        List of dicts with artifact info
    """
    na_artifacts = []

    # Scan for markdown files
    for md_file in base_dir.rglob("*.md"):
        if is_na_file(md_file):
            na_artifacts.append({
                "path": str(md_file.relative_to(base_dir)),
                "type": "markdown",
                "stage": stage
            })

    # Scan traceability folder at project root
    trace_dir = PROJECT_ROOT / "traceability"
    if trace_dir.exists():
        for json_file in trace_dir.glob("*.json"):
            if is_na_file(json_file):
                na_artifacts.append({
                    "path": f"traceability/{json_file.name}",
                    "type": "json",
                    "stage": "shared"
                })

    return na_artifacts


def show_project_classification(state_dir: Optional[Path] = None) -> None:
    """
    Display current project classification to stdout.

    Args:
        state_dir: Optional path to _state directory
    """
    classification = get_project_classification(state_dir)

    print("\n" + "=" * 60)
    print("  PROJECT CLASSIFICATION")
    print("=" * 60)

    if not classification:
        print("\nNo project classification found.")
        print("Run /discovery-init or Discovery_ClassifyProject to classify.")
        print("=" * 60 + "\n")
        return

    print(f"\nProject Type: {classification.get('type', 'UNKNOWN')}")
    print(f"Confidence: {classification.get('confidence', 'N/A')}")
    print(f"Detected At: {classification.get('detected_at', 'Not detected')}")

    if classification.get('override_reason'):
        print(f"Override Reason: {classification.get('override_reason')}")

    signals = classification.get('signals', [])
    if signals:
        print(f"\nDetected Signals ({len(signals)}):")
        for s in signals[:10]:
            print(f"  - {s}")
        if len(signals) > 10:
            print(f"  ... and {len(signals) - 10} more")

    applicability = classification.get('artifact_applicability', {})
    if applicability:
        applicable = [k for k, v in applicability.items() if v]
        not_applicable = [k for k, v in applicability.items() if not v]

        print(f"\nApplicable Artifacts ({len(applicable)}):")
        for a in applicable:
            print(f"  + {a}")

        if not_applicable:
            print(f"\nNot Applicable Artifacts ({len(not_applicable)}):")
            for a in not_applicable:
                print(f"  - {a}")

    print("\n" + "=" * 60 + "\n")


def list_na_artifacts_report(base_dir: Path, stage: str = "discovery") -> None:
    """
    Print a report of N/A artifacts to stdout.

    Args:
        base_dir: Base directory to scan
        stage: Stage name for context
    """
    print(f"\n" + "=" * 60)
    print(f"  NOT_APPLICABLE ARTIFACTS - {stage.upper()}")
    print("=" * 60)

    na_artifacts = get_na_artifacts(base_dir, stage)

    if na_artifacts:
        for artifact in na_artifacts:
            print(f"  - {artifact['path']} ({artifact['type']})")
        print(f"\nTotal: {len(na_artifacts)} N/A artifacts")
    else:
        print("\n  No N/A artifacts found.")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    # CLI for testing
    import argparse

    parser = argparse.ArgumentParser(description="N/A Validation Utilities")
    parser.add_argument("--show-classification", action="store_true", help="Show project classification")
    parser.add_argument("--list-na", type=str, metavar="DIR", help="List N/A artifacts in directory")
    parser.add_argument("--validate-na", type=str, metavar="FILE", help="Validate an N/A file")
    parser.add_argument("--check-applicability", type=str, metavar="ARTIFACT", help="Check if artifact is applicable")

    args = parser.parse_args()

    if args.show_classification:
        show_project_classification()
    elif args.list_na:
        list_na_artifacts_report(Path(args.list_na))
    elif args.validate_na:
        valid, msg = validate_na_file(Path(args.validate_na))
        print(f"{'✅' if valid else '❌'} {msg}")
        sys.exit(0 if valid else 1)
    elif args.check_applicability:
        applicable = check_artifact_applicability(args.check_applicability)
        print(f"Artifact '{args.check_applicability}': {'APPLICABLE' if applicable else 'NOT APPLICABLE'}")
    else:
        parser.print_help()
