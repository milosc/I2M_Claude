#!/usr/bin/env python3
"""
N/A Placeholder Generator
=========================

Generates NOT_APPLICABLE placeholder files for artifacts that don't apply
to the current project type (BACKEND_ONLY, DATABASE_ONLY, INTEGRATION, INFRASTRUCTURE).

Usage:
    python3 na_placeholder_generator.py --artifact <artifact_name> --output <output_path> [options]
    python3 na_placeholder_generator.py --generate-all --output-dir <dir> --config <config_path>

Options:
    --artifact          Single artifact to generate (e.g., screen-definitions)
    --output            Output file path for single artifact
    --generate-all      Generate all N/A artifacts based on project classification
    --output-dir        Directory for generated artifacts
    --config            Path to discovery_config.json
    --project-type      Override project type (BACKEND_ONLY, DATABASE_ONLY, INTEGRATION, INFRASTRUCTURE)
    --confidence        Classification confidence (HIGH, MEDIUM, LOW)
    --reason            Custom reason for N/A status
    --dry-run           Show what would be generated without writing files

Part of: Smart Obsolescence Handling for Non-UI Projects
Version: 1.0.0
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Artifact metadata
ARTIFACT_METADATA = {
    "screen-definitions": {
        "title": "Screen Definitions",
        "filename": "screen-definitions.md",
        "subfolder": "04-design-specs",
        "description": "Screen inventory and layout specifications",
        "skill": "Discovery_SpecScreens",
        "skill_version": "4.0.0",
        "ui_required": True
    },
    "navigation-flows": {
        "title": "Navigation Flows",
        "filename": "navigation-flows.md",
        "subfolder": "04-design-specs",
        "description": "Navigation structure and user flows",
        "skill": "Discovery_SpecNavigation",
        "skill_version": "4.0.0",
        "ui_required": True
    },
    "ui-components": {
        "title": "UI Component Library Specifications",
        "filename": "ui-components.md",
        "subfolder": "04-design-specs",
        "description": "Component library and design tokens",
        "skill": "Discovery_SpecComponents",
        "skill_version": "3.0.0",
        "ui_required": True
    },
    "interaction-patterns": {
        "title": "Interaction Patterns",
        "filename": "interaction-patterns.md",
        "subfolder": "04-design-specs",
        "description": "Interaction behaviors and animations",
        "skill": "Discovery_SpecInteractions",
        "skill_version": "4.0.0",
        "ui_required": True
    }
}

# Project type descriptions
PROJECT_TYPE_FOCUS = {
    "BACKEND_ONLY": "API contracts and service layer specifications",
    "DATABASE_ONLY": "Data models and schema specifications",
    "INTEGRATION": "Integration specs and connector definitions",
    "INFRASTRUCTURE": "Infrastructure configurations and deployment specs"
}

# Artifacts applicable to each project type (True = applicable, False = N/A)
ARTIFACT_APPLICABILITY = {
    "FULL_STACK": {
        "screen-definitions": True,
        "navigation-flows": True,
        "ui-components": True,
        "interaction-patterns": True,
        "data-fields": True
    },
    "BACKEND_ONLY": {
        "screen-definitions": False,
        "navigation-flows": False,
        "ui-components": False,
        "interaction-patterns": False,
        "data-fields": True
    },
    "DATABASE_ONLY": {
        "screen-definitions": False,
        "navigation-flows": False,
        "ui-components": False,
        "interaction-patterns": False,
        "data-fields": True
    },
    "INTEGRATION": {
        "screen-definitions": False,
        "navigation-flows": False,
        "ui-components": False,
        "interaction-patterns": False,
        "data-fields": True
    },
    "INFRASTRUCTURE": {
        "screen-definitions": False,
        "navigation-flows": False,
        "ui-components": False,
        "interaction-patterns": False,
        "data-fields": False
    }
}


def generate_na_placeholder(artifact_name: str, project_type: str, confidence: str = "HIGH",
                            classification_date: str = None, custom_reason: str = None) -> str:
    """Generate NOT_APPLICABLE placeholder content for an artifact."""

    if artifact_name not in ARTIFACT_METADATA:
        raise ValueError(f"Unknown artifact: {artifact_name}")

    meta = ARTIFACT_METADATA[artifact_name]
    now = datetime.now().isoformat()
    classification_date = classification_date or now
    focus = PROJECT_TYPE_FOCUS.get(project_type, "non-UI specifications")

    reason = custom_reason or f"{meta['description']} are only generated for projects with user interface components (FULL_STACK)."

    template = f"""# {meta['title']}

---
status: NOT_APPLICABLE
artifact: {artifact_name}
project_type: {project_type}
classification_date: {classification_date}
generated_date: {now}
---

## Reason

This artifact is not applicable for **{project_type}** projects.

{reason}

## Project Classification

- **Type**: {project_type}
- **Confidence**: {confidence}
- **Classified**: {classification_date}

## What This Means

- No {meta['description'].lower()} will be generated for this project
- Downstream Prototype phase will skip related UI generation
- Focus remains on {focus}

## Alternative Artifacts

For this project type, refer to:
- `data-fields.md` - Data contract definitions (if applicable)
- `PRODUCT_ROADMAP.md` - Feature specifications
- `JOBS_TO_BE_DONE.md` - User/system jobs

---
*Generated by {meta['skill']} v{meta['skill_version']}*
*Smart Obsolescence Handling enabled*
"""
    return template


def get_na_artifacts_for_type(project_type: str) -> list:
    """Get list of artifacts that should be N/A for a project type."""
    if project_type not in ARTIFACT_APPLICABILITY:
        return []

    return [
        artifact for artifact, applicable in ARTIFACT_APPLICABILITY[project_type].items()
        if not applicable and artifact in ARTIFACT_METADATA
    ]


def read_discovery_config(config_path: str) -> dict:
    """Read project classification from discovery_config.json."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get('project_classification', {})
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not read config from {config_path}: {e}")
        return {}


def update_discovery_progress(progress_path: str, artifact_name: str, project_type: str):
    """Update discovery_progress.json with N/A artifact entry."""
    try:
        with open(progress_path, 'r') as f:
            progress = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        progress = {"na_artifacts": [], "na_summary": {}}

    # Add to na_artifacts list
    na_entry = {
        "artifact": artifact_name,
        "project_type": project_type,
        "reason": f"Not applicable for {project_type} projects",
        "timestamp": datetime.now().isoformat()
    }

    if "na_artifacts" not in progress:
        progress["na_artifacts"] = []

    # Avoid duplicates
    existing = [a["artifact"] for a in progress["na_artifacts"]]
    if artifact_name not in existing:
        progress["na_artifacts"].append(na_entry)

    # Update summary
    if "na_summary" not in progress:
        progress["na_summary"] = {}
    progress["na_summary"]["total_na_artifacts"] = len(progress["na_artifacts"])
    progress["na_summary"]["project_type"] = project_type
    progress["na_summary"]["ui_artifacts_applicable"] = project_type == "FULL_STACK"

    # Update checkpoint 9 artifact status if exists
    if "checkpoints" in progress and "9_specs" in progress["checkpoints"]:
        if "artifacts" in progress["checkpoints"]["9_specs"]:
            artifact_key = artifact_name.replace("-", "_") if "-" in artifact_name else artifact_name
            for key in progress["checkpoints"]["9_specs"]["artifacts"]:
                if key.replace("-", "_") == artifact_name.replace("-", "_") or key == artifact_name:
                    progress["checkpoints"]["9_specs"]["artifacts"][key]["status"] = "completed"
                    progress["checkpoints"]["9_specs"]["artifacts"][key]["na_status"] = "NOT_APPLICABLE"

    with open(progress_path, 'w') as f:
        json.dump(progress, f, indent=2)

    return progress


def main():
    parser = argparse.ArgumentParser(
        description="Generate NOT_APPLICABLE placeholder files for non-UI projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate single artifact placeholder
  python3 na_placeholder_generator.py --artifact screen-definitions --output ./04-design-specs/screen-definitions.md --project-type BACKEND_ONLY

  # Generate all N/A artifacts based on config
  python3 na_placeholder_generator.py --generate-all --output-dir ./ClientAnalysis_X/ --config ./_state/discovery_config.json

  # Dry run to see what would be generated
  python3 na_placeholder_generator.py --generate-all --output-dir ./ClientAnalysis_X/ --config ./_state/discovery_config.json --dry-run

  # List N/A artifacts for a project type
  python3 na_placeholder_generator.py --list-na --project-type DATABASE_ONLY
"""
    )

    parser.add_argument("--artifact", help="Single artifact to generate")
    parser.add_argument("--output", help="Output file path for single artifact")
    parser.add_argument("--generate-all", action="store_true", help="Generate all N/A artifacts")
    parser.add_argument("--output-dir", help="Base directory for generated artifacts")
    parser.add_argument("--config", help="Path to discovery_config.json")
    parser.add_argument("--project-type", choices=["BACKEND_ONLY", "DATABASE_ONLY", "INTEGRATION", "INFRASTRUCTURE"],
                        help="Project type (required if no config)")
    parser.add_argument("--confidence", choices=["HIGH", "MEDIUM", "LOW"], default="HIGH",
                        help="Classification confidence")
    parser.add_argument("--reason", help="Custom reason for N/A status")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    parser.add_argument("--list-na", action="store_true", help="List N/A artifacts for project type")
    parser.add_argument("--update-progress", help="Path to discovery_progress.json to update")

    args = parser.parse_args()

    # Get project classification
    project_type = args.project_type
    confidence = args.confidence
    classification_date = None

    if args.config and os.path.exists(args.config):
        classification = read_discovery_config(args.config)
        project_type = project_type or classification.get("type")
        confidence = classification.get("confidence", confidence)
        classification_date = classification.get("detected_at")

    if not project_type:
        if args.list_na or args.generate_all:
            print("Error: --project-type or --config with project_classification required")
            sys.exit(1)

    # List N/A artifacts
    if args.list_na:
        na_artifacts = get_na_artifacts_for_type(project_type)
        print(f"N/A Artifacts for {project_type}:")
        for artifact in na_artifacts:
            meta = ARTIFACT_METADATA.get(artifact, {})
            print(f"  - {artifact}: {meta.get('description', 'No description')}")
        print(f"\nTotal: {len(na_artifacts)} artifacts")
        return

    # Generate single artifact
    if args.artifact:
        if args.artifact not in ARTIFACT_METADATA:
            print(f"Error: Unknown artifact '{args.artifact}'")
            print(f"Available artifacts: {', '.join(ARTIFACT_METADATA.keys())}")
            sys.exit(1)

        content = generate_na_placeholder(
            args.artifact, project_type, confidence, classification_date, args.reason
        )

        if args.dry_run:
            print(f"Would generate: {args.output or 'stdout'}")
            print("-" * 60)
            print(content)
            return

        if args.output:
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
            with open(args.output, 'w') as f:
                f.write(content)
            print(f"Generated: {args.output}")

            # Update progress if specified
            if args.update_progress:
                update_discovery_progress(args.update_progress, args.artifact, project_type)
                print(f"Updated: {args.update_progress}")
        else:
            print(content)
        return

    # Generate all N/A artifacts
    if args.generate_all:
        if not args.output_dir:
            print("Error: --output-dir required with --generate-all")
            sys.exit(1)

        na_artifacts = get_na_artifacts_for_type(project_type)
        if not na_artifacts:
            print(f"No N/A artifacts for project type: {project_type}")
            return

        generated = []
        for artifact in na_artifacts:
            meta = ARTIFACT_METADATA[artifact]
            output_path = os.path.join(args.output_dir, meta["subfolder"], meta["filename"])

            if args.dry_run:
                print(f"Would generate: {output_path}")
                continue

            content = generate_na_placeholder(
                artifact, project_type, confidence, classification_date
            )

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(content)

            generated.append(output_path)
            print(f"Generated: {output_path}")

            # Update progress if specified
            if args.update_progress:
                update_discovery_progress(args.update_progress, artifact, project_type)

        if not args.dry_run:
            print(f"\nGenerated {len(generated)} N/A placeholder files")
            if args.update_progress:
                print(f"Updated progress: {args.update_progress}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
