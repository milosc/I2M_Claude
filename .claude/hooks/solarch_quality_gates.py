#!/usr/bin/env python3
"""
Solution Architecture Quality Gates
====================================

Validates checkpoints for Solution Architecture generation pipeline (Stage 4).

Usage:
    python3 .claude/hooks/solarch_quality_gates.py --list-checkpoints
    python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint N --dir SolArch_X/
    python3 .claude/hooks/solarch_quality_gates.py --validate-file SolArch_X/09-decisions/ADR-001.md
    python3 .claude/hooks/solarch_quality_gates.py --validate-traceability --dir SolArch_X/

Checkpoints:
    0: Initialize - Config, progress, folders
    1: Validate Inputs - ProductSpecs & Prototype completeness
    2: Context Extraction - Introduction, constraints, context
    3: Solution Strategy - Strategy doc, initial ADRs
    4: Building Blocks - Module architecture, C4 diagrams
    5: Runtime Integration - Runtime scenarios, API design
    6: Quality & Cross-cutting - NFRs, security, cross-cutting
    7: Deployment - Deployment view, operations
    8: Decisions Complete - All ADRs, decision index
    9: Risk Assessment - Risks, technical debt
    10: Documentation - Glossary, final docs
    11: Traceability - Full chain validation (BLOCKING)
    12: Final Validation - Complete validation report
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# Import shared N/A validation utilities
try:
    from na_validation_utils import (
        get_project_classification,
        check_artifact_applicability,
        validate_na_file,
        is_na_file,
        get_na_artifacts,
        show_project_classification,
        list_na_artifacts_report,
        ARTIFACT_APPLICABILITY
    )
    HAS_NA_UTILS = True
except ImportError:
    HAS_NA_UTILS = False
    # Fallback implementations if utils not available
    def get_project_classification(): return None
    def check_artifact_applicability(name): return True
    def validate_na_file(path): return True, "N/A utils not available"
    def is_na_file(path): return False
    def get_na_artifacts(base, stage): return []
    def show_project_classification(): print("N/A utils not available")
    def list_na_artifacts_report(base, stage): print("N/A utils not available")


# Artifact name to checkpoint mapping for N/A validation
# Maps artifact names to the checkpoint requirements that check them
ARTIFACT_TO_CHECKPOINT = {
    # SolArch artifacts - most are applicable to all project types
    "adrs": ["09-decisions/ADR-001-architecture-style.md", "09-decisions/ADR-002-technology-stack.md"],
    "c4-diagrams": ["diagrams/c4-context.mermaid", "diagrams/c4-container.mermaid"],
    "deployment-view": ["08-deployment/deployment-view.md", "08-deployment/operations-guide.md"],
    "quality-requirements": ["07-quality/quality-requirements.md"],
}


# ============================================================================
# Checkpoint Definitions
# ============================================================================

CHECKPOINTS = {
    0: {
        "name": "Initialize",
        "phase": "Initialization",
        "description": "Create folder structure, config, and progress files",
        "required_files": [
            "_state/solarch_config.json",
            "_state/solarch_progress.json"
        ],
        "required_folders": [
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
            "11-glossary"
            # NOTE (v3.0): _registry/ removed - all registries now in traceability/ at ROOT level
        ],
        "validation": "folder_structure",
        "blocking": False
    },
    1: {
        "name": "Validate Inputs",
        "phase": "Input Validation",
        "description": "Verify ProductSpecs and Prototype completeness",
        "required_files": [
            "_state/solarch_input_validation.json"
        ],
        "validations": [
            "productspecs_checkpoint_7_passed",
            "prototype_checkpoint_14_passed"
        ],
        "validation": "input_validation",
        "blocking": True
    },
    2: {
        "name": "Context Extraction",
        "phase": "Context & Goals",
        "description": "Generate introduction, constraints, context scope",
        "required_files": [
            "01-introduction-goals/introduction.md",
            "01-introduction-goals/stakeholders.md",
            "02-constraints/business-constraints.md",
            "02-constraints/technical-constraints.md",
            "03-context-scope/business-context.md",
            "03-context-scope/technical-context.md"
        ],
        "validation": "content_check",
        "blocking": False
    },
    3: {
        "name": "Solution Strategy",
        "phase": "Strategy",
        "description": "Generate solution strategy and foundation ADRs",
        "required_files": [
            "04-solution-strategy/solution-strategy.md",
            "09-decisions/ADR-001-architecture-style.md",
            "09-decisions/ADR-002-technology-stack.md"
        ],
        "validation": "content_check",
        "blocking": False
    },
    4: {
        "name": "Building Blocks",
        "phase": "Building Blocks",
        "description": "Generate building block views, module architecture, C4 diagrams",
        "required_files": [
            "05-building-blocks/overview.md",
            "traceability/component_registry.json"  # v3.0: ROOT-level registry
        ],
        "required_patterns": [
            "05-building-blocks/modules/*/README.md"
        ],
        "validation": "building_blocks",
        "blocking": False
    },
    5: {
        "name": "Runtime Integration",
        "phase": "Runtime",
        "description": "Generate runtime scenarios, API design, event communication",
        "required_files": [
            "06-runtime/api-design.md",
            "06-runtime/event-communication.md"
        ],
        "validation": "content_check",
        "blocking": False
    },
    6: {
        "name": "Quality & Cross-cutting",
        "phase": "Quality",
        "description": "Generate quality requirements, security, cross-cutting concerns",
        "required_files": [
            "07-quality/quality-requirements.md",
            "06-runtime/security-architecture.md",
            "05-building-blocks/cross-cutting.md"
        ],
        "validation": "content_check",
        "blocking": False
    },
    7: {
        "name": "Deployment",
        "phase": "Deployment",
        "description": "Generate deployment view and operations guide",
        "required_files": [
            "08-deployment/deployment-view.md",
            "08-deployment/operations-guide.md"
        ],
        "validation": "content_check",
        "blocking": False
    },
    8: {
        "name": "Decisions Complete",
        "phase": "Decisions",
        "description": "Complete all ADRs and generate decision index",
        "required_files": [
            "traceability/adr_registry.json"  # v3.0: ROOT-level registry
        ],
        "min_adrs": 9,
        "validation": "decisions_complete",
        "blocking": False
    },
    9: {
        "name": "Risk Assessment",
        "phase": "Risks",
        "description": "Generate risks and technical debt documentation",
        "required_files": [
            "10-risks/risks-technical-debt.md"
        ],
        "validation": "content_check",
        "blocking": False
    },
    10: {
        "name": "Documentation",
        "phase": "Documentation",
        "description": "Generate glossary and finalize documentation",
        "required_files": [
            "11-glossary/glossary.md"
        ],
        "validation": "content_check",
        "blocking": False
    },
    11: {
        "name": "Traceability Validation",
        "phase": "Traceability",
        "description": "Validate end-to-end traceability chains",
        "required_files": [
            # v3.0: All registries now at ROOT level in traceability/
            "traceability/traceability_matrix_master.json",
            "traceability/solarch_traceability_register.json"
        ],
        "validation": "traceability_validation",
        "coverage_requirements": {
            "pain_points": 100,
            "p0_requirements": 100,
            "modules": 100
        },
        "blocking": True
    },
    12: {
        "name": "Final Validation",
        "phase": "Finalization",
        "description": "Complete validation report and summary",
        "required_files": [
            # v3.0: Reports stay in local folder (not registries)
            "reports/VALIDATION_REPORT.md",
            "reports/GENERATION_SUMMARY.md"
        ],
        "validation": "final_validation",
        "blocking": False
    }
}


# ============================================================================
# Validation Functions
# ============================================================================

def validate_json_file(filepath: str, artifact_name: Optional[str] = None) -> tuple[bool, str]:
    """
    Validate a JSON file exists and is valid JSON, with N/A artifact support.

    If the file is marked as NOT_APPLICABLE and the artifact is not applicable
    for this project type, validation passes with N/A status.
    """
    if not os.path.exists(filepath):
        if artifact_name and not check_artifact_applicability(artifact_name):
            return False, f"⊘ {filepath} - Missing (expected N/A file for non-applicable artifact)"
        return False, f"File not found: {filepath}"

    # Check if it's an N/A file
    if is_na_file(Path(filepath)):
        valid, msg = validate_na_file(Path(filepath))
        if valid:
            return True, f"⊘ NOT_APPLICABLE (valid format)"
        else:
            return False, f"N/A file with invalid format: {msg}"

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return True, "Valid JSON"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def validate_markdown_file(filepath: str, min_lines: int = 10, artifact_name: Optional[str] = None) -> tuple[bool, str]:
    """
    Validate a markdown file exists and has content, with N/A artifact support.

    If the file is marked as NOT_APPLICABLE and the artifact is not applicable
    for this project type, validation passes with N/A status.
    """
    if not os.path.exists(filepath):
        if artifact_name and not check_artifact_applicability(artifact_name):
            return False, f"⊘ {filepath} - Missing (expected N/A file for non-applicable artifact)"
        return False, f"File not found: {filepath}"

    # Check if it's an N/A file
    if is_na_file(Path(filepath)):
        valid, msg = validate_na_file(Path(filepath))
        if valid:
            return True, f"⊘ NOT_APPLICABLE (valid format)"
        else:
            return False, f"N/A file with invalid format: {msg}"

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = [l for l in content.split('\n') if l.strip()]
        if len(lines) < min_lines:
            return False, f"Insufficient content: {len(lines)} lines (min: {min_lines})"

        # Check for placeholder text
        placeholders = ['{TODO}', '{PLACEHOLDER}', '{{', '}}', '[TBD]']
        for p in placeholders:
            if p in content:
                return False, f"Contains placeholder: {p}"

        return True, f"Valid markdown ({len(lines)} lines)"
    except Exception as e:
        return False, f"Error reading file: {e}"


def validate_folder_structure(base_dir: str, checkpoint: dict) -> tuple[bool, list]:
    """Validate required folders and files exist."""
    issues = []

    # Check required folders
    for folder in checkpoint.get("required_folders", []):
        folder_path = os.path.join(base_dir, folder)
        if not os.path.isdir(folder_path):
            issues.append(f"Missing folder: {folder}")

    # Check required files
    for file in checkpoint.get("required_files", []):
        # Handle root _state files
        if file.startswith("_state/"):
            # Check at project root
            root_dir = find_project_root(base_dir)
            file_path = os.path.join(root_dir, file)
        else:
            file_path = os.path.join(base_dir, file)

        if not os.path.exists(file_path):
            issues.append(f"Missing file: {file}")

    return len(issues) == 0, issues


def find_project_root(start_dir: str) -> str:
    """Find the project root (directory containing _state folder or .git)."""
    current = os.path.abspath(start_dir)
    while current != '/':
        if os.path.isdir(os.path.join(current, '_state')) or os.path.isdir(os.path.join(current, '.git')):
            return current
        current = os.path.dirname(current)
    return os.path.abspath(start_dir)


def validate_input_validation(base_dir: str, checkpoint: dict) -> tuple[bool, list]:
    """Validate that ProductSpecs and Prototype are complete."""
    issues = []
    root_dir = find_project_root(base_dir)

    validation_file = os.path.join(root_dir, "_state/solarch_input_validation.json")
    if not os.path.exists(validation_file):
        issues.append("Missing input validation file: _state/solarch_input_validation.json")
        return False, issues

    try:
        with open(validation_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not data.get("productspecs_valid", False):
            issues.append("ProductSpecs validation failed")
        if not data.get("prototype_valid", False):
            issues.append("Prototype validation failed")

    except Exception as e:
        issues.append(f"Error reading validation file: {e}")

    return len(issues) == 0, issues


def validate_content_check(base_dir: str, checkpoint: dict) -> tuple[bool, list]:
    """Validate required files exist and have sufficient content."""
    issues = []
    root_dir = find_project_root(base_dir)

    for file in checkpoint.get("required_files", []):
        # v3.0: All registries now at ROOT level in traceability/
        if file.startswith("_state/") or file.startswith("traceability/"):
            file_path = os.path.join(root_dir, file)
        else:
            file_path = os.path.join(base_dir, file)

        if file_path.endswith('.json'):
            valid, msg = validate_json_file(file_path)
        else:
            valid, msg = validate_markdown_file(file_path)

        if not valid:
            issues.append(f"{file}: {msg}")

    return len(issues) == 0, issues


def validate_building_blocks(base_dir: str, checkpoint: dict) -> tuple[bool, list]:
    """Validate building blocks and module architecture."""
    issues = []

    # Check required files
    for file in checkpoint.get("required_files", []):
        file_path = os.path.join(base_dir, file)
        if not os.path.exists(file_path):
            issues.append(f"Missing file: {file}")

    # Check module folders exist
    modules_dir = os.path.join(base_dir, "05-building-blocks/modules")
    if not os.path.isdir(modules_dir):
        issues.append("Missing modules directory: 05-building-blocks/modules/")
        return False, issues

    # Count module READMEs
    module_count = 0
    for entry in os.listdir(modules_dir):
        module_path = os.path.join(modules_dir, entry, "README.md")
        if os.path.isfile(module_path):
            module_count += 1

    if module_count == 0:
        issues.append("No module README.md files found in 05-building-blocks/modules/")

    return len(issues) == 0, issues


def validate_decisions_complete(base_dir: str, checkpoint: dict) -> tuple[bool, list]:
    """Validate ADRs are complete."""
    issues = []

    # v3.0: ADR registry now at ROOT level in traceability/
    root_dir = find_project_root(base_dir)
    decisions_file = os.path.join(root_dir, "traceability/adr_registry.json")
    if not os.path.exists(decisions_file):
        issues.append("Missing ADR registry: traceability/adr_registry.json")
        return False, issues

    try:
        with open(decisions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # v3.0: Schema uses "items" array instead of "decisions"
        decisions = data.get("items", data.get("decisions", []))
        min_adrs = checkpoint.get("min_adrs", 9)

        if len(decisions) < min_adrs:
            issues.append(f"Insufficient ADRs: {len(decisions)} (minimum: {min_adrs})")

        # Verify each ADR has a document
        for decision in decisions:
            doc_path = decision.get("document", "")
            if doc_path:
                full_path = os.path.join(base_dir, doc_path.lstrip('./'))
                if not os.path.exists(full_path):
                    issues.append(f"ADR document missing: {doc_path}")

    except Exception as e:
        issues.append(f"Error reading decisions registry: {e}")

    return len(issues) == 0, issues


def validate_traceability(base_dir: str, checkpoint: dict) -> tuple[bool, list]:
    """Validate end-to-end traceability chains."""
    issues = []

    # v3.0: Traceability matrix now at ROOT level in traceability/
    root_dir = find_project_root(base_dir)
    trace_file = os.path.join(root_dir, "traceability/traceability_matrix_master.json")
    if not os.path.exists(trace_file):
        issues.append("Missing traceability file: traceability/traceability_matrix_master.json")
        return False, issues

    try:
        with open(trace_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # v3.0: New schema uses "coverage" with different structure
        coverage = data.get("coverage", {})
        requirements = checkpoint.get("coverage_requirements", {})

        # Check pain points coverage (v3.0 schema)
        pp_data = coverage.get("pain_points", {})
        pp_covered = pp_data.get("addressed", pp_data.get("painPointsCovered", 0))
        pp_total = pp_data.get("total", pp_data.get("painPointsTotal", 1))
        pp_pct = pp_data.get("coverage_percent", (pp_covered / pp_total * 100) if pp_total > 0 else 0)

        if pp_pct < requirements.get("pain_points", 100):
            issues.append(f"Pain point coverage: {pp_pct:.1f}% (required: {requirements.get('pain_points', 100)}%)")

        # Check modules coverage (v3.0 schema)
        mod_data = coverage.get("modules", {})
        mod_covered = mod_data.get("covered", mod_data.get("modulesArchitected", 0))
        mod_total = mod_data.get("total", mod_data.get("modulesTotal", 1))
        mod_pct = mod_data.get("coverage_percent", (mod_covered / mod_total * 100) if mod_total > 0 else 0)

        if mod_pct < requirements.get("modules", 100):
            issues.append(f"Module architecture coverage: {mod_pct:.1f}% (required: {requirements.get('modules', 100)}%)")

        # Check requirements coverage (v3.0 schema)
        req_data = coverage.get("requirements", {})
        req_covered = req_data.get("covered", req_data.get("requirementsCovered", 0))
        req_total = req_data.get("total", req_data.get("requirementsTotal", 1))
        req_pct = req_data.get("coverage_percent", (req_covered / req_total * 100) if req_total > 0 else 0)

        # P0 requirements should be 100%
        if req_pct < requirements.get("p0_requirements", 100):
            issues.append(f"Requirements coverage: {req_pct:.1f}% (required: {requirements.get('p0_requirements', 100)}%)")

    except Exception as e:
        issues.append(f"Error validating traceability: {e}")

    return len(issues) == 0, issues


def validate_final(base_dir: str, checkpoint: dict) -> tuple[bool, list]:
    """Validate final documentation."""
    issues = []

    for file in checkpoint.get("required_files", []):
        file_path = os.path.join(base_dir, file)
        if not os.path.exists(file_path):
            issues.append(f"Missing file: {file}")

    return len(issues) == 0, issues


def validate_adr_file(filepath: str) -> tuple[bool, list]:
    """Validate an ADR file has required sections."""
    issues = []

    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"]

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        required_sections = [
            "## Status",
            "## Context",
            "## Decision",
            "## Consequences",
            "## Traceability"
        ]

        for section in required_sections:
            if section not in content:
                issues.append(f"Missing section: {section}")

        # Check for traceability table
        if "| Pain Point |" not in content and "| PP-" not in content:
            issues.append("Missing traceability table with pain point references")

    except Exception as e:
        issues.append(f"Error reading file: {e}")

    return len(issues) == 0, issues


# ============================================================================
# Main Validation Router
# ============================================================================

def validate_checkpoint(checkpoint_num: int, base_dir: str) -> tuple[bool, list]:
    """Route to appropriate validation function."""
    if checkpoint_num not in CHECKPOINTS:
        return False, [f"Invalid checkpoint: {checkpoint_num}"]

    checkpoint = CHECKPOINTS[checkpoint_num]
    validation_type = checkpoint.get("validation", "content_check")

    validators = {
        "folder_structure": validate_folder_structure,
        "input_validation": validate_input_validation,
        "content_check": validate_content_check,
        "building_blocks": validate_building_blocks,
        "decisions_complete": validate_decisions_complete,
        "traceability_validation": validate_traceability,
        "final_validation": validate_final
    }

    validator = validators.get(validation_type, validate_content_check)
    return validator(base_dir, checkpoint)


def validate_file(filepath: str) -> tuple[bool, list]:
    """Validate a single file based on its type."""
    if not os.path.exists(filepath):
        return False, [f"File not found: {filepath}"]

    filename = os.path.basename(filepath)

    if filename.startswith("ADR-"):
        return validate_adr_file(filepath)
    elif filepath.endswith('.json'):
        valid, msg = validate_json_file(filepath)
        return valid, [msg] if not valid else []
    elif filepath.endswith('.md'):
        valid, msg = validate_markdown_file(filepath)
        return valid, [msg] if not valid else []
    else:
        return True, []


# ============================================================================
# CLI Interface
# ============================================================================

def list_checkpoints():
    """Print all checkpoint definitions."""
    print("\n" + "=" * 70)
    print(" SOLUTION ARCHITECTURE QUALITY GATES - CHECKPOINT REFERENCE")
    print("=" * 70 + "\n")

    for cp_num, cp in sorted(CHECKPOINTS.items()):
        blocking = " [BLOCKING]" if cp.get("blocking") else ""
        print(f"Checkpoint {cp_num}: {cp['name']}{blocking}")
        print(f"  Phase: {cp['phase']}")
        print(f"  Description: {cp['description']}")

        if cp.get("required_files"):
            print(f"  Required Files:")
            for f in cp["required_files"][:5]:  # Show first 5
                print(f"    - {f}")
            if len(cp.get("required_files", [])) > 5:
                print(f"    ... and {len(cp['required_files']) - 5} more")

        print()

    print("=" * 70)
    print("\nUsage:")
    print("  python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint N --dir SolArch_X/")
    print("  python3 .claude/hooks/solarch_quality_gates.py --validate-file SolArch_X/09-decisions/ADR-001.md")
    print("  python3 .claude/hooks/solarch_quality_gates.py --validate-traceability --dir SolArch_X/")
    print()


def main():
    parser = argparse.ArgumentParser(description="Solution Architecture Quality Gates")
    parser.add_argument("--list-checkpoints", action="store_true", help="List all checkpoints")
    parser.add_argument("--validate-checkpoint", type=int, metavar="N", help="Validate checkpoint N")
    parser.add_argument("--validate-file", type=str, metavar="PATH", help="Validate a specific file")
    parser.add_argument("--validate-traceability", action="store_true", help="Validate traceability chains")

    # N/A validation options
    parser.add_argument("--validate-na-file", type=str, metavar="PATH", help="Validate a NOT_APPLICABLE file format")
    parser.add_argument("--show-classification", action="store_true", help="Show current project classification")
    parser.add_argument("--list-na-artifacts", action="store_true", help="List all N/A artifacts in SolArch")

    parser.add_argument("--dir", type=str, default=".", help="Base directory for validation")

    args = parser.parse_args()

    # N/A validation handlers
    if args.show_classification:
        show_project_classification()
        return 0

    if args.validate_na_file:
        valid, msg = validate_na_file(Path(args.validate_na_file))
        print(f"{'✅' if valid else '❌'} {msg}")
        return 0 if valid else 1

    if args.list_na_artifacts:
        base_dir = os.path.abspath(args.dir)
        list_na_artifacts_report(Path(base_dir), "solarch")
        return 0

    if args.list_checkpoints:
        list_checkpoints()
        return 0

    if args.validate_checkpoint is not None:
        base_dir = os.path.abspath(args.dir)
        cp_num = args.validate_checkpoint

        if cp_num not in CHECKPOINTS:
            print(f"ERROR: Invalid checkpoint {cp_num}")
            return 1

        cp = CHECKPOINTS[cp_num]
        print(f"\n{'=' * 60}")
        print(f" Validating Checkpoint {cp_num}: {cp['name']}")
        print(f"{'=' * 60}")
        print(f"Directory: {base_dir}")
        print(f"Blocking: {'Yes' if cp.get('blocking') else 'No'}")
        print()

        valid, issues = validate_checkpoint(cp_num, base_dir)

        if valid:
            print(f"RESULT: PASSED")
            return 0
        else:
            print(f"RESULT: FAILED")
            print("\nIssues:")
            for issue in issues:
                print(f"  - {issue}")

            if cp.get("blocking"):
                print(f"\n[BLOCKING] This checkpoint must pass before proceeding.")

            return 1

    if args.validate_file:
        filepath = os.path.abspath(args.validate_file)
        print(f"\nValidating file: {filepath}")

        valid, issues = validate_file(filepath)

        if valid:
            print("RESULT: PASSED")
            return 0
        else:
            print("RESULT: FAILED")
            print("\nIssues:")
            for issue in issues:
                print(f"  - {issue}")
            return 1

    if args.validate_traceability:
        base_dir = os.path.abspath(args.dir)
        print(f"\nValidating traceability for: {base_dir}")

        valid, issues = validate_traceability(base_dir, CHECKPOINTS[11])

        if valid:
            print("RESULT: PASSED")
            return 0
        else:
            print("RESULT: FAILED")
            print("\nIssues:")
            for issue in issues:
                print(f"  - {issue}")
            return 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
