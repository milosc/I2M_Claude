#!/usr/bin/env python3
"""
Project Classification Utility for HTEC ClaudeCode Accelerators Framework.

Provides functions to:
- Load project classification from config
- Check artifact applicability
- Generate N/A placeholders
- Detect project type signals from content

Usage:
    python3 project_classifier.py check <artifact_name>
    python3 project_classifier.py classify
    python3 project_classifier.py detect <analysis_summary_path>
    python3 project_classifier.py generate-na --type md|json --artifact <name> --project-type <type>
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Project types supported by the framework
PROJECT_TYPES = [
    "FULL_STACK",
    "BACKEND_ONLY",
    "DATABASE_ONLY",
    "INTEGRATION",
    "INFRASTRUCTURE"
]

# Artifact applicability matrix - which artifacts apply to which project types
ARTIFACT_APPLICABILITY = {
    "FULL_STACK": {
        "screen-definitions": True,
        "navigation-structure": True,
        "ui-components": True,
        "design-tokens": True,
        "interaction-patterns": True,
        "data-fields": True,
        "api-contracts": True,
        "data-model": True,
        "prototype-code": True,
    },
    "BACKEND_ONLY": {
        "screen-definitions": False,
        "navigation-structure": False,
        "ui-components": False,
        "design-tokens": False,
        "interaction-patterns": False,
        "data-fields": True,
        "api-contracts": True,
        "data-model": True,
        "prototype-code": True,  # API server code
    },
    "DATABASE_ONLY": {
        "screen-definitions": False,
        "navigation-structure": False,
        "ui-components": False,
        "design-tokens": False,
        "interaction-patterns": False,
        "data-fields": True,
        "api-contracts": False,
        "data-model": True,
        "prototype-code": True,  # Schema/migration code
    },
    "INTEGRATION": {
        "screen-definitions": False,
        "navigation-structure": False,
        "ui-components": False,
        "design-tokens": False,
        "interaction-patterns": False,
        "data-fields": True,
        "api-contracts": True,
        "data-model": True,
        "prototype-code": True,  # Integration code
    },
    "INFRASTRUCTURE": {
        "screen-definitions": False,
        "navigation-structure": False,
        "ui-components": False,
        "design-tokens": False,
        "interaction-patterns": False,
        "data-fields": False,
        "api-contracts": False,
        "data-model": False,
        "prototype-code": True,  # IaC code
    },
}

# Signal patterns for project type detection
SIGNAL_PATTERNS = {
    "UI": [
        r"screenshot",
        r"wireframe",
        r"mockup",
        r"user\s+interface",
        r"UI\s+design",
        r"user\s+clicks",
        r"user\s+sees",
        r"screen\s+shows",
        r"button",
        r"form\s+field",
        r"modal",
        r"dialog",
        r"navigation\s+menu",
        r"dashboard",
        r"mobile\s+app",
        r"web\s+app",
        r"frontend",
        r"react",
        r"vue",
        r"angular",
    ],
    "BACKEND": [
        r"API\s+endpoint",
        r"REST\s+API",
        r"GraphQL",
        r"microservice",
        r"backend\s+service",
        r"server-side",
        r"request\s*/\s*response",
        r"authentication\s+API",
        r"webhook",
        r"no\s+UI",
        r"headless",
        r"API-only",
    ],
    "DATABASE": [
        r"database\s+schema",
        r"table\s+definition",
        r"column",
        r"migration",
        r"ETL",
        r"data\s+warehouse",
        r"SQL",
        r"stored\s+procedure",
        r"data\s+model",
        r"entity\s+relationship",
        r"foreign\s+key",
        r"index",
    ],
    "INTEGRATION": [
        r"integrate\s+with",
        r"connect\s+to",
        r"middleware",
        r"message\s+queue",
        r"event-driven",
        r"pub\s*/\s*sub",
        r"kafka",
        r"rabbitmq",
        r"external\s+system",
        r"third-party",
        r"API\s+gateway",
        r"orchestration",
    ],
    "INFRASTRUCTURE": [
        r"infrastructure",
        r"terraform",
        r"cloudformation",
        r"kubernetes",
        r"docker",
        r"CI\s*/\s*CD",
        r"deployment",
        r"scaling",
        r"monitoring",
        r"AWS",
        r"Azure",
        r"GCP",
        r"DevOps",
        r"IaC",
    ],
}

# Reasons for N/A by project type
NA_REASONS = {
    "BACKEND_ONLY": {
        "screen-definitions": "Project classified as BACKEND_ONLY - no user-facing screens. API endpoints serve as the interface.",
        "navigation-structure": "Project classified as BACKEND_ONLY - no UI navigation. API routing handles request flow.",
        "ui-components": "Project classified as BACKEND_ONLY - no UI components. Backend services don't render visual elements.",
        "design-tokens": "Project classified as BACKEND_ONLY - no visual design system. API responses define data contracts instead.",
        "interaction-patterns": "Project classified as BACKEND_ONLY - no user interactions. Request/response patterns define behavior.",
    },
    "DATABASE_ONLY": {
        "screen-definitions": "Project classified as DATABASE_ONLY - data layer focus. No application screens.",
        "navigation-structure": "Project classified as DATABASE_ONLY - no application layer. Data access is direct.",
        "ui-components": "Project classified as DATABASE_ONLY - no presentation layer.",
        "design-tokens": "Project classified as DATABASE_ONLY - no visual output.",
        "interaction-patterns": "Project classified as DATABASE_ONLY - data operations don't have UI interactions.",
        "api-contracts": "Project classified as DATABASE_ONLY - direct data access, no API layer.",
    },
    "INTEGRATION": {
        "screen-definitions": "Project classified as INTEGRATION - middleware focus. No user-facing screens.",
        "navigation-structure": "Project classified as INTEGRATION - event/message routing, not UI navigation.",
        "ui-components": "Project classified as INTEGRATION - connector components, not UI components.",
        "design-tokens": "Project classified as INTEGRATION - no visual interface.",
        "interaction-patterns": "Project classified as INTEGRATION - system-to-system interactions, not user interactions.",
    },
    "INFRASTRUCTURE": {
        "screen-definitions": "Project classified as INFRASTRUCTURE - DevOps/Cloud focus. No application screens.",
        "navigation-structure": "Project classified as INFRASTRUCTURE - no application layer.",
        "ui-components": "Project classified as INFRASTRUCTURE - infrastructure as code, not UI code.",
        "design-tokens": "Project classified as INFRASTRUCTURE - no visual design.",
        "interaction-patterns": "Project classified as INFRASTRUCTURE - operational patterns, not user patterns.",
        "data-fields": "Project classified as INFRASTRUCTURE - no application data model.",
        "api-contracts": "Project classified as INFRASTRUCTURE - infrastructure APIs, not application APIs.",
        "data-model": "Project classified as INFRASTRUCTURE - no application data layer.",
    },
}


def load_project_classification(config_path: str = "_state/discovery_config.json") -> Dict:
    """Load project classification from config file."""
    if not os.path.exists(config_path):
        return {
            "type": "FULL_STACK",
            "detected_at": None,
            "confidence": None,
            "signals": [],
            "artifact_applicability": ARTIFACT_APPLICABILITY["FULL_STACK"]
        }

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "type": "FULL_STACK",
            "detected_at": None,
            "confidence": None,
            "signals": [],
            "artifact_applicability": ARTIFACT_APPLICABILITY["FULL_STACK"]
        }

    return config.get("project_classification", {
        "type": "FULL_STACK",
        "detected_at": None,
        "confidence": None,
        "signals": [],
        "artifact_applicability": ARTIFACT_APPLICABILITY["FULL_STACK"]
    })


def is_artifact_applicable(artifact_name: str, project_type: str = None, config_path: str = "_state/discovery_config.json") -> bool:
    """Check if an artifact is applicable for the current project type."""
    if project_type is None:
        classification = load_project_classification(config_path)
        project_type = classification.get("type", "FULL_STACK")

    applicability = ARTIFACT_APPLICABILITY.get(project_type, ARTIFACT_APPLICABILITY["FULL_STACK"])
    return applicability.get(artifact_name, True)


def get_na_reason(artifact_name: str, project_type: str) -> str:
    """Get the reason why an artifact is not applicable."""
    type_reasons = NA_REASONS.get(project_type, {})
    if artifact_name in type_reasons:
        return type_reasons[artifact_name]
    return f"Artifact '{artifact_name}' is not applicable for {project_type} project type."


def detect_signals(content: str) -> Dict[str, List[str]]:
    """Detect project type signals from content."""
    signals = {category: [] for category in SIGNAL_PATTERNS.keys()}

    content_lower = content.lower()

    for category, patterns in SIGNAL_PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(pattern, content_lower, re.IGNORECASE)
            if matches:
                # Get the original case match from content
                original_matches = re.findall(pattern, content, re.IGNORECASE)
                for match in original_matches[:3]:  # Limit to 3 examples per pattern
                    signal = f"Found '{match}' pattern"
                    if signal not in signals[category]:
                        signals[category].append(signal)

    return signals


def classify_project(signals: Dict[str, List[str]]) -> Tuple[str, float, List[str]]:
    """
    Classify project type based on detected signals.

    Returns:
        Tuple of (project_type, confidence, collected_signals)
    """
    # Count signals per category
    scores = {category: len(sigs) for category, sigs in signals.items()}
    total_signals = sum(scores.values())

    if total_signals == 0:
        return "FULL_STACK", 0.5, ["No specific signals detected - defaulting to FULL_STACK"]

    # Collect all signals for output
    all_signals = []
    for category, sigs in signals.items():
        for sig in sigs:
            all_signals.append(f"[{category}] {sig}")

    # Determine dominant category
    max_score = max(scores.values())
    dominant_categories = [cat for cat, score in scores.items() if score == max_score]

    # UI signals present → FULL_STACK
    if scores["UI"] > 0 and scores["UI"] >= max_score * 0.5:
        confidence = scores["UI"] / total_signals
        return "FULL_STACK", min(confidence + 0.3, 1.0), all_signals

    # Map signal categories to project types
    category_to_type = {
        "BACKEND": "BACKEND_ONLY",
        "DATABASE": "DATABASE_ONLY",
        "INTEGRATION": "INTEGRATION",
        "INFRASTRUCTURE": "INFRASTRUCTURE",
    }

    # Find the dominant non-UI category
    non_ui_scores = {k: v for k, v in scores.items() if k != "UI"}
    if non_ui_scores:
        dominant = max(non_ui_scores, key=non_ui_scores.get)
        if non_ui_scores[dominant] > 0:
            project_type = category_to_type.get(dominant, "FULL_STACK")
            confidence = non_ui_scores[dominant] / total_signals
            return project_type, min(confidence + 0.2, 1.0), all_signals

    return "FULL_STACK", 0.5, all_signals


def generate_na_markdown(
    artifact_name: str,
    artifact_title: str,
    skill_name: str,
    checkpoint: int,
    project_type: str,
    signals: List[str],
    regenerate_command: str,
    analysis_summary_ref: str = "01-analysis/ANALYSIS_SUMMARY.md#project-type-signals"
) -> str:
    """Generate NOT_APPLICABLE markdown content."""
    timestamp = datetime.now().isoformat()

    # Format signals as markdown list
    if signals:
        signals_md = "\n".join(f"  - {s}" for s in signals[:10])  # Limit to 10
    else:
        signals_md = "  - (No specific signals recorded)"

    # Get reason
    reason = get_na_reason(artifact_name, project_type)

    # Generate document ID
    doc_id = artifact_name.upper().replace('-', '_').replace('.', '_') + "-NA-001"

    return f"""---
document_id: {doc_id}
version: 1.0.0
created_at: {timestamp}
updated_at: {timestamp}
generated_by: {skill_name}
status: NOT_APPLICABLE
---

# {artifact_title}

## Status: NOT APPLICABLE

This artifact has been marked as **NOT APPLICABLE** for the current project.

### Reason

{reason}

### Project Classification

- **Project Type**: {project_type}
- **Detected Signals**:
{signals_md}

### Decision Metadata

| Field | Value |
|-------|-------|
| Decision Date | {timestamp} |
| Deciding Skill | {skill_name} |
| Checkpoint | {checkpoint} |
| Confidence | HIGH |

### Traceability

This decision traces to:
- **Analysis Summary**: `{analysis_summary_ref}`
- **Project Type Detection**: `_state/discovery_config.json#project_classification`

### Override Instructions

If this artifact becomes applicable in the future:

1. Update `_state/discovery_config.json` → `project_classification.type` to `FULL_STACK`
2. Re-run: `{regenerate_command}`
3. Or manually create the artifact following the standard template

---

*This placeholder maintains framework integrity while acknowledging that not all artifacts apply to every project type.*
"""


def generate_na_json(
    purpose: str,
    stage: str,
    artifact_name: str,
    skill_name: str,
    checkpoint: int,
    project_type: str,
    signals: List[str],
    analysis_summary_ref: str = "01-analysis/ANALYSIS_SUMMARY.md#project-type-signals"
) -> Dict[str, Any]:
    """Generate NOT_APPLICABLE JSON content."""
    timestamp = datetime.now().isoformat()
    reason = get_na_reason(artifact_name, project_type)

    return {
        "$documentation": {
            "purpose": purpose,
            "stage": stage,
            "status": "NOT_APPLICABLE",
            "reason": reason
        },
        "schema_version": "1.0.0",
        "status": "NOT_APPLICABLE",
        "reason": reason,
        "project_type": project_type,
        "detected_signals": signals[:10] if signals else [],
        "decision_metadata": {
            "decision_date": timestamp,
            "deciding_skill": skill_name,
            "checkpoint": checkpoint,
            "confidence": "HIGH"
        },
        "traceability": {
            "analysis_summary_ref": analysis_summary_ref,
            "config_ref": "_state/discovery_config.json#project_classification"
        },
        "items": []
    }


def update_config_with_classification(
    config_path: str,
    project_type: str,
    confidence: float,
    signals: List[str]
) -> bool:
    """Update discovery_config.json with project classification."""
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        config["project_classification"] = {
            "type": project_type,
            "detected_at": datetime.now().isoformat(),
            "confidence": round(confidence, 2),
            "signals": signals[:20],  # Limit to 20 signals
            "artifact_applicability": ARTIFACT_APPLICABILITY.get(project_type, ARTIFACT_APPLICABILITY["FULL_STACK"])
        }

        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        return True
    except Exception as e:
        print(f"Error updating config: {e}", file=sys.stderr)
        return False


def print_applicability_matrix(project_type: str = None):
    """Print the artifact applicability matrix."""
    if project_type:
        types_to_show = [project_type]
    else:
        types_to_show = PROJECT_TYPES

    artifacts = list(ARTIFACT_APPLICABILITY["FULL_STACK"].keys())

    # Header
    header = "| Artifact |"
    separator = "|----------|"
    for pt in types_to_show:
        header += f" {pt[:12]:^12} |"
        separator += "--------------|"

    print(header)
    print(separator)

    # Rows
    for artifact in artifacts:
        row = f"| {artifact:17} |"
        for pt in types_to_show:
            applicable = ARTIFACT_APPLICABILITY[pt].get(artifact, True)
            status = "   YES   " if applicable else "   N/A   "
            row += f" {status:^12} |"
        print(row)


# CLI interface
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "check":
        # Check if artifact is applicable
        if len(sys.argv) < 3:
            print("Usage: project_classifier.py check <artifact_name> [config_path]")
            sys.exit(1)

        artifact = sys.argv[2]
        config_path = sys.argv[3] if len(sys.argv) > 3 else "_state/discovery_config.json"

        classification = load_project_classification(config_path)
        project_type = classification.get("type", "FULL_STACK")
        applicable = is_artifact_applicable(artifact, project_type)

        print(json.dumps({
            "artifact": artifact,
            "project_type": project_type,
            "applicable": applicable,
            "reason": None if applicable else get_na_reason(artifact, project_type)
        }, indent=2))

    elif command == "classify":
        # Show current classification
        config_path = sys.argv[2] if len(sys.argv) > 2 else "_state/discovery_config.json"
        classification = load_project_classification(config_path)
        print(json.dumps(classification, indent=2))

    elif command == "detect":
        # Detect signals from content
        if len(sys.argv) < 3:
            print("Usage: project_classifier.py detect <file_path>")
            sys.exit(1)

        file_path = sys.argv[2]

        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)

        with open(file_path, 'r') as f:
            content = f.read()

        signals = detect_signals(content)
        project_type, confidence, all_signals = classify_project(signals)

        print(json.dumps({
            "project_type": project_type,
            "confidence": round(confidence, 2),
            "signals_by_category": {k: v for k, v in signals.items() if v},
            "recommendation": f"Classify as {project_type}" if confidence >= 0.6 else "Low confidence - recommend user confirmation"
        }, indent=2))

    elif command == "generate-na":
        # Generate N/A content
        import argparse
        parser = argparse.ArgumentParser(prog="project_classifier.py generate-na")
        parser.add_argument("--type", choices=["md", "json"], required=True)
        parser.add_argument("--artifact", required=True)
        parser.add_argument("--project-type", required=True)
        parser.add_argument("--skill", default="Discovery_Skill")
        parser.add_argument("--checkpoint", type=int, default=9)
        parser.add_argument("--title", default=None)
        parser.add_argument("--purpose", default="Registry placeholder")
        parser.add_argument("--stage", default="Discovery")
        parser.add_argument("--command", default="/discovery-specs-all")

        # Parse remaining args after 'generate-na'
        args = parser.parse_args(sys.argv[2:])

        signals = ["Project type detection during Discovery Phase 1"]

        if args.type == "md":
            title = args.title or args.artifact.replace("-", " ").title()
            content = generate_na_markdown(
                artifact_name=args.artifact,
                artifact_title=title,
                skill_name=args.skill,
                checkpoint=args.checkpoint,
                project_type=args.project_type,
                signals=signals,
                regenerate_command=args.command
            )
            print(content)
        else:
            content = generate_na_json(
                purpose=args.purpose,
                stage=args.stage,
                artifact_name=args.artifact,
                skill_name=args.skill,
                checkpoint=args.checkpoint,
                project_type=args.project_type,
                signals=signals
            )
            print(json.dumps(content, indent=2))

    elif command == "matrix":
        # Print applicability matrix
        project_type = sys.argv[2] if len(sys.argv) > 2 else None
        print_applicability_matrix(project_type)

    elif command == "types":
        # List project types
        for pt in PROJECT_TYPES:
            print(f"- {pt}")

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
