#!/usr/bin/env python3
"""
ProductSpecs Quality Gates - Checkpoint Validation

Validates ProductSpecs outputs against checkpoint requirements.
Mirrors the prototype_quality_gates.py pattern for consistency.

Usage:
    python3 productspecs_quality_gates.py --validate-checkpoint <N> --dir <path>
    python3 productspecs_quality_gates.py --validate-file <path>
    python3 productspecs_quality_gates.py --list-checkpoints
    python3 productspecs_quality_gates.py --validate-traceability --dir <path>
    python3 productspecs_quality_gates.py --validate-modules --dir <path>
    python3 productspecs_quality_gates.py --validate-jira --dir <path>
    python3 productspecs_quality_gates.py --validate-module-registry --dir <path>

Feedback Validation Commands:
    python3 productspecs_quality_gates.py --validate-feedback PS-<NNN> --dir <path>
    python3 productspecs_quality_gates.py --validate-feedback-registry --dir <path>
    python3 productspecs_quality_gates.py --list-feedback --dir <path>
"""

import argparse
import json
import os
import re
import csv
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

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
    # ProductSpecs artifacts - most are applicable to all project types
    "modules": ["01-modules/module-index.md"],
    "api-contracts": ["02-api/api-index.md", "02-api/data-contracts.md"],
    "nfr-specs": ["02-api/NFR_SPECIFICATIONS.md"],
    "test-cases": ["03-tests/test-case-registry.md"],
    "jira-export": ["04-jira/full-hierarchy.csv", "04-jira/IMPORT_GUIDE.md"],
}


def get_root_path(specs_path: Path) -> Path:
    """
    Get the project root path where shared _state/ folder lives.

    The _state/ folder is SHARED between Discovery, Prototype, and ProductSpecs phases
    and lives at the project root level, NOT inside ProductSpecs_<SystemName>/.

    Structure:
        /project_root/
        ├── _state/                          <- SHARED state folder
        ├── traceability/                    <- SHARED traceability
        ├── ClientAnalysis_<SystemName>/     <- Discovery outputs
        ├── Prototype_<SystemName>/          <- Prototype outputs
        └── ProductSpecs_<SystemName>/       <- ProductSpecs outputs
    """
    # If the path is ProductSpecs_<SystemName>/, go up one level
    if specs_path.name.startswith("ProductSpecs_"):
        return specs_path.parent
    # If already at root (e.g., running from project root), return as-is
    return specs_path


def get_state_path(specs_path: Path) -> Path:
    """Get the shared _state/ folder path (at project root level)."""
    return get_root_path(specs_path) / "_state"


def get_traceability_path(specs_path: Path) -> Path:
    """Get the shared traceability/ folder path (at project root level)."""
    return get_root_path(specs_path) / "traceability"


def get_prototype_path(specs_path: Path) -> Optional[Path]:
    """
    Get the corresponding Prototype folder for this ProductSpecs.

    Assumes naming convention: ProductSpecs_<SystemName> -> Prototype_<SystemName>
    """
    if specs_path.name.startswith("ProductSpecs_"):
        system_name = specs_path.name.replace("ProductSpecs_", "")
        prototype_path = specs_path.parent / f"Prototype_{system_name}"
        if prototype_path.exists():
            return prototype_path
    return None


def get_discovery_path(specs_path: Path) -> Optional[Path]:
    """
    Get the corresponding ClientAnalysis folder for this ProductSpecs.

    Assumes naming convention: ProductSpecs_<SystemName> -> ClientAnalysis_<SystemName>
    """
    if specs_path.name.startswith("ProductSpecs_"):
        system_name = specs_path.name.replace("ProductSpecs_", "")
        discovery_path = specs_path.parent / f"ClientAnalysis_{system_name}"
        if discovery_path.exists():
            return discovery_path
    return None


# Checkpoint requirements mapping
# NOTE: Paths starting with "_state/" are ROOT-RELATIVE (shared folder)
#       All other paths are PRODUCTSPECS-RELATIVE
CHECKPOINT_REQUIREMENTS = {
    0: {
        "name": "Initialize",
        "description": "Folder structure and state files created",
        "required_files": [
            "_state/productspecs_config.json",
            "_state/productspecs_progress.json"
        ],
        "required_folders": [
            "_state",
            "00-overview",
            "01-modules",
            "02-api",
            "03-tests",
            "04-jira",
            # NOTE: _registry/ removed in v3.0 - all registries now in traceability/
            "feedback-sessions"
        ]
    },
    1: {
        "name": "Validate Sources",
        "description": "Discovery and Prototype outputs validated",
        "required_files": [
            "_state/productspecs_config.json"
        ],
        "json_validation": {
            "file": "_state/productspecs_config.json",
            "required_fields": ["system_name", "prototype_path", "discovery_path"]
        },
        "source_validation": {
            "check_discovery_summary": True,
            "check_prototype_complete": True
        }
    },
    2: {
        "name": "Extract Requirements",
        "description": "Requirements hierarchy extracted with traceability",
        "required_files": [
            # v3.0: All registries now in traceability/ at ROOT level
            "traceability/requirements_registry.json"
        ],
        "json_validation": {
            "file": "traceability/requirements_registry.json",
            "required_fields": ["items"],
            "array_min_items": {"items": 1}
        }
    },
    3: {
        "name": "Modules Core",
        "description": "Core module specifications generated",
        "required_files": [
            "01-modules/module-index.md"
        ],
        "required_folders": [
            "01-modules"
        ],
        "folder_min_files": {
            "01-modules": 2  # At least module-index.md and one MOD-*.md
        },
        "file_content_check": {
            "file": "01-modules/module-index.md",
            "must_contain": ["# Module Index", "## Modules"]
        }
    },
    4: {
        "name": "Modules Extended",
        "description": "All screens have module specifications + module registry populated",
        "required_files": [
            "01-modules/module-index.md",
            # v3.0: Single source of truth at ROOT level
            "traceability/module_registry.json"
        ],
        "module_coverage_validation": {
            "check_type": "all_screens_have_modules"
        },
        "module_registry_validation": {
            "check_type": "registry_populated",
            "min_items": 1,
            "required_fields": ["id", "title", "app", "priority", "phase"]
        }
    },
    5: {
        "name": "API Contracts",
        "description": "API contracts and data specifications generated",
        "required_files": [
            "02-api/api-index.md"
        ],
        "required_folders": [
            "02-api"
        ],
        "file_content_check": {
            "file": "02-api/api-index.md",
            "must_contain": ["# API Index", "## Endpoints"]
        }
    },
    6: {
        "name": "Test Specifications",
        "description": "Test specifications and acceptance criteria generated",
        "required_files": [
            "03-tests/test-case-registry.md"
        ],
        "required_folders": [
            "03-tests"
        ],
        "file_content_check": {
            "file": "03-tests/test-case-registry.md",
            "must_contain": ["# Test Case Registry", "## Test Cases"]
        }
    },
    7: {
        "name": "Traceability Validation",
        "description": "All P0 requirements have complete traceability chains",
        "required_files": [
            # v3.0: All traceability now in ROOT traceability/ folder
            "traceability/traceability_matrix_master.json",
            "traceability/productspecs_traceability_register.json"
        ],
        "traceability_validation": {
            "check_type": "all_p0_traced",
            "chain": ["pain_point", "jtbd", "requirement", "screen", "module", "test"]
        }
    },
    8: {
        "name": "Export",
        "description": "JIRA export and documentation generated",
        "required_files": [
            "00-overview/MASTER_DEVELOPMENT_PLAN.md",
            "00-overview/GENERATION_SUMMARY.md",
            "04-jira/IMPORT_GUIDE.md",
            "04-jira/full-hierarchy.csv"
        ],
        "required_folders": [
            "04-jira"
        ],
        "file_content_check": {
            "file": "00-overview/MASTER_DEVELOPMENT_PLAN.md",
            "must_contain": ["# Master Development Plan", "## Traceability Matrix"]
        },
        "jira_validation": {
            "check_csv_format": True,
            "check_hierarchy": True
        }
    }
}


def resolve_path(base_path: Path, relative_path: str) -> Path:
    """
    Resolve a relative path to its full path.

    - Paths starting with "_state/" resolve to the ROOT _state/ folder
    - Paths starting with "traceability/" resolve to the ROOT traceability/ folder
    - All other paths resolve relative to the ProductSpecs folder
    """
    if relative_path.startswith("_state/"):
        # _state/ is at project root level (shared)
        state_subpath = relative_path[len("_state/"):]
        return get_state_path(base_path) / state_subpath
    elif relative_path == "_state":
        return get_state_path(base_path)
    elif relative_path.startswith("traceability/"):
        # traceability/ is at project root level (shared)
        trace_subpath = relative_path[len("traceability/"):]
        return get_traceability_path(base_path) / trace_subpath
    elif relative_path == "traceability":
        return get_traceability_path(base_path)
    else:
        # All other paths are relative to the ProductSpecs folder
        return base_path / relative_path


def validate_file_exists(base_path: Path, file_path: str, artifact_name: Optional[str] = None) -> Tuple[bool, str]:
    """
    Check if a file exists, with N/A artifact support.

    If the file is marked as NOT_APPLICABLE and the artifact is not applicable
    for this project type, validation passes with N/A status.
    """
    full_path = resolve_path(base_path, file_path)

    if full_path.exists() and full_path.is_file():
        # Check if it's an N/A file
        if is_na_file(full_path):
            # Validate N/A file format
            valid, msg = validate_na_file(full_path)
            if valid:
                return True, f"⊘ {file_path} - NOT_APPLICABLE (valid format)"
            else:
                return False, f"❌ {file_path} - N/A file with invalid format: {msg}"
        return True, f"✅ {file_path}"

    # File doesn't exist - check if artifact should be N/A
    if artifact_name and not check_artifact_applicability(artifact_name):
        return False, f"⊘ {file_path} - Missing (expected N/A file for non-applicable artifact '{artifact_name}')"

    return False, f"❌ {file_path} - File not found"


def validate_folder_exists(base_path: Path, folder_path: str) -> Tuple[bool, str]:
    """Check if a folder exists."""
    full_path = resolve_path(base_path, folder_path)
    if full_path.exists() and full_path.is_dir():
        return True, f"✅ {folder_path}/"
    return False, f"❌ {folder_path}/ - Folder not found"


def validate_json_file(base_path: Path, config: Dict) -> Tuple[bool, List[str]]:
    """Validate JSON file structure."""
    results = []
    file_path = resolve_path(base_path, config["file"])

    if not file_path.exists():
        return False, [f"❌ {config['file']} - File not found"]

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Check required fields
        if "required_fields" in config:
            for field in config["required_fields"]:
                if field in data:
                    results.append(f"✅ {config['file']} has '{field}' field")
                else:
                    results.append(f"❌ {config['file']} missing '{field}' field")
                    return False, results

        # Check array minimum items
        if "array_min_items" in config:
            for field, min_count in config["array_min_items"].items():
                if field in data and isinstance(data[field], list):
                    if len(data[field]) >= min_count:
                        results.append(f"✅ {config['file']}.{field} has {len(data[field])} items (min: {min_count})")
                    else:
                        results.append(f"❌ {config['file']}.{field} has {len(data[field])} items (min: {min_count})")
                        return False, results
                else:
                    results.append(f"❌ {config['file']}.{field} not found or not an array")
                    return False, results

        return True, results

    except json.JSONDecodeError as e:
        return False, [f"❌ {config['file']} - Invalid JSON: {e}"]
    except Exception as e:
        return False, [f"❌ {config['file']} - Error: {e}"]


def validate_file_content(base_path: Path, config: Dict) -> Tuple[bool, List[str]]:
    """Validate file contains required content."""
    results = []
    file_path = resolve_path(base_path, config["file"])

    if not file_path.exists():
        return False, [f"❌ {config['file']} - File not found"]

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        for text in config.get("must_contain", []):
            if text in content:
                results.append(f"✅ {config['file']} contains '{text}'")
            else:
                results.append(f"❌ {config['file']} missing '{text}'")
                return False, results

        return True, results

    except Exception as e:
        return False, [f"❌ {config['file']} - Error reading: {e}"]


def validate_folder_min_files(base_path: Path, config: Dict) -> Tuple[bool, List[str]]:
    """Validate folder contains minimum number of files."""
    results = []

    for folder, min_count in config.items():
        folder_path = resolve_path(base_path, folder)
        if not folder_path.exists():
            results.append(f"❌ {folder}/ - Folder not found")
            return False, results

        files = [f for f in folder_path.iterdir() if f.is_file()]
        if len(files) >= min_count:
            results.append(f"✅ {folder}/ has {len(files)} files (min: {min_count})")
        else:
            results.append(f"❌ {folder}/ has {len(files)} files (min: {min_count})")
            return False, results

    return True, results


def validate_source_availability(base_path: Path, config: Dict) -> Tuple[bool, List[str]]:
    """Validate that Discovery and Prototype sources are available."""
    results = []

    # Check discovery summary exists in shared _state/
    if config.get("check_discovery_summary"):
        discovery_summary_path = get_state_path(base_path) / "discovery_summary.json"
        if discovery_summary_path.exists():
            results.append("✅ _state/discovery_summary.json available")
        else:
            results.append("❌ _state/discovery_summary.json not found")
            return False, results

    # Check prototype is complete (has progress file with phase 14 completed)
    if config.get("check_prototype_complete"):
        prototype_progress_path = get_state_path(base_path) / "prototype_progress.json"
        if prototype_progress_path.exists():
            try:
                with open(prototype_progress_path, 'r') as f:
                    progress = json.load(f)

                # Check if prototype phases are complete
                phases = progress.get("phases", {})
                completed_phases = sum(1 for p in phases.values() if p.get("status") == "completed")
                total_phases = len(phases)

                if completed_phases >= 12:  # At least phases 0-12 complete
                    results.append(f"✅ Prototype has {completed_phases}/{total_phases} phases complete")
                else:
                    results.append(f"⚠️ Prototype has only {completed_phases}/{total_phases} phases complete")
            except:
                results.append("⚠️ Could not read prototype progress")
        else:
            results.append("⚠️ _state/prototype_progress.json not found")

    return True, results


def validate_module_coverage(base_path: Path, config: Dict) -> Tuple[bool, List[str]]:
    """Validate that all screens have module specifications."""
    results = []

    # Load screen registry from shared traceability/
    screen_registry_path = get_traceability_path(base_path) / "screen_registry.json"
    if not screen_registry_path.exists():
        return False, ["❌ screen_registry.json not found - run ProductSpecs_Validate first"]

    try:
        with open(screen_registry_path, 'r') as f:
            registry = json.load(f)

        discovery_screens = registry.get("discovery_screens", [])
        if not discovery_screens:
            return False, ["❌ No Discovery screens found in registry"]

        # Find all module files
        modules_path = base_path / "01-modules"
        module_files = list(modules_path.glob("MOD-*.md")) if modules_path.exists() else []

        # Read module index to understand screen-to-module mapping
        module_index_path = modules_path / "module-index.md"
        screens_in_modules = set()

        if module_index_path.exists():
            with open(module_index_path, 'r') as f:
                index_content = f.read()
            # Extract screen IDs mentioned in module index
            screen_pattern = r'(M-\d+|D-\d+|S-\d+|SCR-[A-Z]+-[A-Z]+-\d+)'
            screens_in_modules = set(re.findall(screen_pattern, index_content))

        # Also scan module files for screen references
        for mod_file in module_files:
            try:
                content = mod_file.read_text()
                found_screens = re.findall(r'(M-\d+|D-\d+|S-\d+|SCR-[A-Z]+-[A-Z]+-\d+)', content)
                screens_in_modules.update(found_screens)
            except:
                pass

        # Check coverage
        discovery_screen_ids = set(s.get("id") for s in discovery_screens)
        covered_screens = discovery_screen_ids & screens_in_modules
        missing_screens = discovery_screen_ids - screens_in_modules

        coverage = (len(covered_screens) / len(discovery_screen_ids) * 100) if discovery_screen_ids else 0

        results.append(f"📊 Module coverage: {len(covered_screens)}/{len(discovery_screen_ids)} ({coverage:.1f}%)")

        if missing_screens:
            results.append(f"❌ {len(missing_screens)} screens missing module coverage:")
            for sid in list(missing_screens)[:5]:
                results.append(f"   • {sid}")
            if len(missing_screens) > 5:
                results.append(f"   ... and {len(missing_screens) - 5} more")
            return False, results

        results.append("✅ All Discovery screens covered by module specifications")
        return True, results

    except Exception as e:
        return False, [f"❌ Error checking module coverage: {e}"]


def validate_module_registry(base_path: Path, config: Dict) -> Tuple[bool, List[str]]:
    """
    Validate that module registry is populated at ROOT level (v3.0 - Single Source of Truth).

    This is a GATE validation - Checkpoint 4 CANNOT pass if the module registry
    at traceability/module_registry.json has an empty items array.

    NOTE (v3.0): Local _registry/ folder no longer exists. All registries are in traceability/.
    """
    results = []

    # Check ROOT-level module registry (SINGLE SOURCE OF TRUTH)
    root_registry_path = get_traceability_path(base_path) / "module_registry.json"

    if not root_registry_path.exists():
        results.append("❌ traceability/module_registry.json not found (ROOT level)")
        results.append("   → Run ProductSpecs_Generator CP 3-4 to create module registry")
        return False, results

    try:
        # Read ROOT registry (Single Source of Truth)
        with open(root_registry_path, 'r') as f:
            root_data = json.load(f)

        # Check ROOT registry has items
        root_items = root_data.get("items", [])
        min_items = config.get("min_items", 1)

        if len(root_items) < min_items:
            results.append(f"❌ traceability/module_registry.json has {len(root_items)} items (minimum: {min_items})")
            results.append("   → GATE FAILED: Module registry empty")
            results.append("   → Fix: Run ProductSpecs_Generator CP 3-4 to populate traceability/module_registry.json")
            return False, results

        results.append(f"✅ traceability/module_registry.json has {len(root_items)} items")

        # Validate required fields on each item
        required_fields = config.get("required_fields", ["id", "title", "app", "priority", "phase"])
        items_with_issues = []

        for item in root_items:
            item_id = item.get("id", "UNKNOWN")
            missing_fields = [f for f in required_fields if not item.get(f)]
            if missing_fields:
                items_with_issues.append(f"{item_id}: missing {', '.join(missing_fields)}")

        if items_with_issues:
            results.append(f"⚠️ {len(items_with_issues)} modules with missing required fields:")
            for issue in items_with_issues[:5]:
                results.append(f"   • {issue}")
            if len(items_with_issues) > 5:
                results.append(f"   ... and {len(items_with_issues) - 5} more")
            # Don't fail on missing optional fields, just warn
        else:
            results.append("✅ All modules have required fields")

        # Check P0 modules have critical traceability links
        p0_modules = [m for m in root_items if m.get("priority") == "P0"]
        if p0_modules:
            p0_with_traceability = 0
            for mod in p0_modules:
                if mod.get("epic_id") or mod.get("requirement_refs"):
                    if mod.get("screen_refs") or mod.get("screens"):
                        p0_with_traceability += 1

            if p0_with_traceability == len(p0_modules):
                results.append(f"✅ All {len(p0_modules)} P0 modules have traceability links")
            else:
                results.append(f"⚠️ {p0_with_traceability}/{len(p0_modules)} P0 modules have traceability links")

        # Verify sync between local and ROOT
        if len(local_modules) != len(root_items):
            results.append(f"⚠️ Registry sync issue: local has {len(local_modules)}, ROOT has {len(root_items)}")
        else:
            results.append("✅ Local and ROOT registries are in sync")

        return True, results

    except json.JSONDecodeError as e:
        return False, [f"❌ Invalid JSON in module registry: {e}"]
    except Exception as e:
        return False, [f"❌ Error validating module registry: {e}"]


def validate_traceability_chains(base_path: Path, config: Dict) -> Tuple[bool, List[str]]:
    """
    Validate that all P0 requirements have complete traceability chains.

    NOTE (v3.0): Reads from traceability/traceability_matrix_master.json (Single Source of Truth)
    """
    results = []

    # v3.0: Use ROOT-level traceability matrix
    traceability_path = get_traceability_path(base_path) / "traceability_matrix_master.json"
    if not traceability_path.exists():
        return False, ["❌ traceability/traceability_matrix_master.json not found"]

    try:
        with open(traceability_path, 'r') as f:
            traceability = json.load(f)

        requirements = traceability.get("requirements", [])
        chain_fields = config.get("chain", ["pain_point", "jtbd", "requirement", "screen", "module", "test"])

        # Filter P0 requirements
        p0_reqs = [r for r in requirements if r.get("priority") == "P0"]

        if not p0_reqs:
            results.append("⚠️ No P0 requirements found")
            return True, results

        incomplete_chains = []
        complete_chains = 0

        for req in p0_reqs:
            req_id = req.get("id", "UNKNOWN")
            missing_links = []

            # Check each link in the chain
            if not req.get("pain_point_refs"):
                missing_links.append("pain_point")
            if not req.get("jtbd_refs"):
                missing_links.append("jtbd")
            if not req.get("screen_refs"):
                missing_links.append("screen")
            if not req.get("module_refs"):
                missing_links.append("module")
            if not req.get("test_refs"):
                missing_links.append("test")

            if missing_links:
                incomplete_chains.append(f"{req_id}: missing {', '.join(missing_links)}")
            else:
                complete_chains += 1

        coverage = (complete_chains / len(p0_reqs) * 100) if p0_reqs else 0
        results.append(f"📊 P0 traceability: {complete_chains}/{len(p0_reqs)} ({coverage:.1f}%)")

        if incomplete_chains:
            results.append(f"❌ {len(incomplete_chains)} P0 requirements with incomplete chains:")
            for chain in incomplete_chains[:5]:
                results.append(f"   • {chain}")
            if len(incomplete_chains) > 5:
                results.append(f"   ... and {len(incomplete_chains) - 5} more")
            return False, results

        results.append("✅ All P0 requirements have complete traceability chains")
        return True, results

    except Exception as e:
        return False, [f"❌ Error validating traceability: {e}"]


def validate_jira_export(base_path: Path, config: Dict) -> Tuple[bool, List[str]]:
    """Validate JIRA export files format and structure."""
    results = []

    jira_path = base_path / "04-jira"
    if not jira_path.exists():
        return False, ["❌ 04-jira/ folder not found"]

    # Check CSV format
    if config.get("check_csv_format"):
        csv_file = jira_path / "full-hierarchy.csv"
        if csv_file.exists():
            try:
                with open(csv_file, 'r', newline='') as f:
                    reader = csv.DictReader(f)
                    headers = reader.fieldnames or []

                    # Check for required JIRA columns
                    required_headers = ["Summary", "Issue Type"]
                    missing_headers = [h for h in required_headers if h not in headers]

                    if missing_headers:
                        results.append(f"❌ CSV missing headers: {missing_headers}")
                        return False, results

                    # Count rows
                    rows = list(reader)
                    results.append(f"✅ full-hierarchy.csv has {len(rows)} rows")

                    # Count by issue type
                    type_counts = {}
                    for row in rows:
                        issue_type = row.get("Issue Type", "Unknown")
                        type_counts[issue_type] = type_counts.get(issue_type, 0) + 1

                    for itype, count in type_counts.items():
                        results.append(f"   • {itype}: {count}")

            except Exception as e:
                results.append(f"❌ Error reading CSV: {e}")
                return False, results
        else:
            results.append("❌ full-hierarchy.csv not found")
            return False, results

    # Check hierarchy integrity
    if config.get("check_hierarchy"):
        # Validate that Stories have valid Epic parents
        epics_stories_file = jira_path / "epics-and-stories.csv"
        if epics_stories_file.exists():
            try:
                with open(epics_stories_file, 'r', newline='') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)

                epic_names = set()
                orphan_stories = []

                for row in rows:
                    if row.get("Issue Type") == "Epic":
                        epic_names.add(row.get("Summary", ""))
                    elif row.get("Issue Type") == "Story":
                        parent = row.get("Epic Name", "")
                        if parent and parent not in epic_names:
                            orphan_stories.append(row.get("Summary", "Unknown")[:40])

                if orphan_stories:
                    results.append(f"⚠️ {len(orphan_stories)} stories reference unknown epics")
                else:
                    results.append("✅ All stories have valid epic parents")

            except Exception as e:
                results.append(f"⚠️ Could not validate hierarchy: {e}")

    return True, results


def validate_checkpoint(checkpoint: int, dir_path: str) -> Dict:
    """Validate a specific checkpoint."""
    if checkpoint not in CHECKPOINT_REQUIREMENTS:
        return {
            "success": False,
            "checkpoint": checkpoint,
            "error": f"Invalid checkpoint: {checkpoint}. Valid range: 0-8"
        }

    base_path = Path(dir_path)
    if not base_path.exists():
        return {
            "success": False,
            "checkpoint": checkpoint,
            "error": f"Directory not found: {dir_path}"
        }

    req = CHECKPOINT_REQUIREMENTS[checkpoint]
    results = {
        "success": True,
        "checkpoint": checkpoint,
        "name": req["name"],
        "description": req["description"],
        "validations": [],
        "timestamp": datetime.now().isoformat()
    }

    # Validate required files
    if "required_files" in req:
        for file_path in req["required_files"]:
            passed, message = validate_file_exists(base_path, file_path)
            results["validations"].append(message)
            if not passed:
                results["success"] = False

    # Validate required folders
    if "required_folders" in req:
        for folder_path in req["required_folders"]:
            passed, message = validate_folder_exists(base_path, folder_path)
            results["validations"].append(message)
            if not passed:
                results["success"] = False

    # Validate JSON structure
    if "json_validation" in req:
        passed, messages = validate_json_file(base_path, req["json_validation"])
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False

    # Validate file content
    if "file_content_check" in req:
        passed, messages = validate_file_content(base_path, req["file_content_check"])
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False

    # Validate folder minimum files
    if "folder_min_files" in req:
        passed, messages = validate_folder_min_files(base_path, req["folder_min_files"])
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False

    # Validate source availability (Checkpoint 1)
    if "source_validation" in req:
        passed, messages = validate_source_availability(base_path, req["source_validation"])
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False

    # Validate module coverage (Checkpoint 4)
    if "module_coverage_validation" in req:
        passed, messages = validate_module_coverage(base_path, req["module_coverage_validation"])
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False

    # Validate module registry (Checkpoint 4 GATE)
    if "module_registry_validation" in req:
        passed, messages = validate_module_registry(base_path, req["module_registry_validation"])
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False

    # Validate traceability chains (Checkpoint 7)
    if "traceability_validation" in req:
        passed, messages = validate_traceability_chains(base_path, req["traceability_validation"])
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False

    # Validate JIRA export (Checkpoint 8)
    if "jira_validation" in req:
        passed, messages = validate_jira_export(base_path, req["jira_validation"])
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False

    return results


def validate_file(file_path: str) -> Dict:
    """Validate a specific file against its expected format."""
    path = Path(file_path)

    if not path.exists():
        return {
            "success": False,
            "file": file_path,
            "error": "File not found"
        }

    results = {
        "success": True,
        "file": file_path,
        "validations": []
    }

    # Determine file type and validate accordingly
    if path.suffix == ".json":
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            results["validations"].append("✅ Valid JSON structure")

            # Check for common required fields based on filename
            if "requirements" in path.name:
                if "requirements" not in data:
                    results["success"] = False
                    results["validations"].append("❌ Missing 'requirements' field")
            elif "traceability" in path.name:
                for field in ["requirements", "statistics"]:
                    if field not in data:
                        results["success"] = False
                        results["validations"].append(f"❌ Missing '{field}' field")
            elif "modules" in path.name:
                if "modules" not in data:
                    results["success"] = False
                    results["validations"].append("❌ Missing 'modules' field")

        except json.JSONDecodeError as e:
            results["success"] = False
            results["validations"].append(f"❌ Invalid JSON: {e}")

    elif path.suffix == ".md":
        try:
            with open(path, 'r') as f:
                content = f.read()

            if len(content.strip()) > 0:
                results["validations"].append("✅ File has content")
            else:
                results["success"] = False
                results["validations"].append("❌ File is empty")

            # Check for heading
            if content.startswith("#"):
                results["validations"].append("✅ Has heading")
            else:
                results["validations"].append("⚠️ Missing heading")

            # Module-specific validation
            if path.name.startswith("MOD-"):
                required_sections = [
                    "## Traceability",
                    "## Screen Specifications",
                    "## Access Control",
                    "## Non-Functional Requirements",
                    "## Test Specifications"
                ]
                for section in required_sections:
                    if section in content:
                        results["validations"].append(f"✅ Has '{section}'")
                    else:
                        results["validations"].append(f"⚠️ Missing '{section}'")

        except Exception as e:
            results["success"] = False
            results["validations"].append(f"❌ Error reading file: {e}")

    elif path.suffix == ".csv":
        try:
            with open(path, 'r', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)

            if len(rows) > 1:
                results["validations"].append(f"✅ CSV has {len(rows) - 1} data rows")
            else:
                results["success"] = False
                results["validations"].append("❌ CSV has no data rows")

        except Exception as e:
            results["success"] = False
            results["validations"].append(f"❌ Error reading CSV: {e}")

    return results


def validate_traceability(dir_path: str) -> Dict:
    """
    Validate full traceability from Discovery through ProductSpecs.

    NOTE (v3.0): Uses traceability/traceability_matrix_master.json (Single Source of Truth)
    """
    base_path = Path(dir_path)

    results = {
        "success": True,
        "validations": [],
        "coverage": {},
        "timestamp": datetime.now().isoformat()
    }

    # Check for required files
    state_path = get_state_path(base_path)
    discovery_summary_path = state_path / "discovery_summary.json"
    if not discovery_summary_path.exists():
        results["success"] = False
        results["validations"].append("❌ Missing _state/discovery_summary.json")
        return results

    # v3.0: Use ROOT-level traceability matrix
    traceability_path = get_traceability_path(base_path) / "traceability_matrix_master.json"
    if not traceability_path.exists():
        results["success"] = False
        results["validations"].append("❌ Missing traceability/traceability_matrix_master.json")
        return results

    try:
        with open(discovery_summary_path, 'r') as f:
            discovery = json.load(f)

        with open(traceability_path, 'r') as f:
            traceability = json.load(f)

        # Pain point coverage
        pain_points = discovery.get("pain_points", [])
        pain_point_ids = set(pp.get("id") for pp in pain_points)

        requirements = traceability.get("requirements", [])
        linked_pain_points = set()
        for req in requirements:
            refs = req.get("pain_point_refs", [])
            linked_pain_points.update(refs)

        pp_coverage = len(linked_pain_points & pain_point_ids) / len(pain_point_ids) * 100 if pain_point_ids else 0

        results["coverage"]["pain_points"] = {
            "total": len(pain_point_ids),
            "linked": len(linked_pain_points & pain_point_ids),
            "coverage_percent": round(pp_coverage, 1)
        }

        if pp_coverage >= 80:
            results["validations"].append(f"✅ Pain point coverage: {pp_coverage:.1f}%")
        elif pp_coverage >= 50:
            results["validations"].append(f"⚠️ Pain point coverage: {pp_coverage:.1f}% (recommend 80%+)")
        else:
            results["validations"].append(f"❌ Pain point coverage: {pp_coverage:.1f}% (below 50%)")
            results["success"] = False

        # P0 requirement chain completeness
        p0_reqs = [r for r in requirements if r.get("priority") == "P0"]
        complete_p0 = 0
        for req in p0_reqs:
            if (req.get("pain_point_refs") and
                req.get("jtbd_refs") and
                req.get("screen_refs") and
                req.get("module_refs") and
                req.get("test_refs")):
                complete_p0 += 1

        p0_coverage = (complete_p0 / len(p0_reqs) * 100) if p0_reqs else 100

        results["coverage"]["p0_requirements"] = {
            "total": len(p0_reqs),
            "complete": complete_p0,
            "coverage_percent": round(p0_coverage, 1)
        }

        if p0_coverage >= 100:
            results["validations"].append(f"✅ P0 chain completeness: {p0_coverage:.1f}%")
        elif p0_coverage >= 80:
            results["validations"].append(f"⚠️ P0 chain completeness: {p0_coverage:.1f}%")
        else:
            results["validations"].append(f"❌ P0 chain completeness: {p0_coverage:.1f}%")
            results["success"] = False

    except json.JSONDecodeError as e:
        results["success"] = False
        results["validations"].append(f"❌ JSON parse error: {e}")
    except Exception as e:
        results["success"] = False
        results["validations"].append(f"❌ Error: {e}")

    return results


def validate_modules(dir_path: str) -> Dict:
    """Validate module specifications quality."""
    base_path = Path(dir_path)

    results = {
        "success": True,
        "validations": [],
        "statistics": {},
        "timestamp": datetime.now().isoformat()
    }

    modules_path = base_path / "01-modules"
    if not modules_path.exists():
        results["success"] = False
        results["validations"].append("❌ 01-modules/ folder not found")
        return results

    # Find all module files
    module_files = list(modules_path.glob("MOD-*.md"))
    results["statistics"]["module_count"] = len(module_files)
    results["validations"].append(f"📊 Found {len(module_files)} module files")

    # Check each module
    valid_modules = 0
    module_issues = []

    required_sections = [
        "## Traceability",
        "## Screen Specifications",
        "## Access Control",
        "## Non-Functional Requirements",
        "## Test Specifications"
    ]

    for mod_file in module_files:
        try:
            content = mod_file.read_text()
            missing = [s for s in required_sections if s not in content]

            if not missing:
                valid_modules += 1
            else:
                module_issues.append(f"{mod_file.name}: missing {len(missing)} sections")

        except Exception as e:
            module_issues.append(f"{mod_file.name}: read error")

    results["statistics"]["valid_modules"] = valid_modules
    results["statistics"]["modules_with_issues"] = len(module_issues)

    if module_issues:
        results["validations"].append(f"⚠️ {len(module_issues)} modules with missing sections:")
        for issue in module_issues[:5]:
            results["validations"].append(f"   • {issue}")
        if len(module_issues) > 5:
            results["validations"].append(f"   ... and {len(module_issues) - 5} more")
    else:
        results["validations"].append("✅ All modules have required sections")

    return results


# ============================================================================
# FEEDBACK VALIDATION FUNCTIONS
# ============================================================================

def get_feedback_sessions_path(specs_path: Path) -> Path:
    """Get the feedback-sessions folder path within the ProductSpecs folder."""
    return specs_path / "feedback-sessions"


def get_feedback_registry_path(specs_path: Path) -> Path:
    """Get the productspecs_feedback_registry.json path."""
    return get_feedback_sessions_path(specs_path) / "productspecs_feedback_registry.json"


def validate_feedback_registry(specs_path: Path) -> Dict:
    """Validate the feedback registry structure and integrity."""
    registry_path = get_feedback_registry_path(specs_path)

    results = {
        "success": True,
        "validations": [],
        "statistics": {},
        "timestamp": datetime.now().isoformat()
    }

    if not registry_path.exists():
        results["success"] = False
        results["validations"].append("❌ productspecs_feedback_registry.json not found")
        results["validations"].append("   No feedback has been processed yet")
        return results

    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)

        # Check required fields
        required_fields = ["feedback_items", "statistics", "$metadata"]
        for field in required_fields:
            if field in registry:
                results["validations"].append(f"✅ Registry has '{field}' field")
            else:
                results["validations"].append(f"❌ Registry missing '{field}' field")
                results["success"] = False

        # Validate statistics
        stats = registry.get("statistics", {})
        results["statistics"] = stats

        total = stats.get("total", 0)
        results["validations"].append(f"📊 Total feedback items: {total}")

        # Status breakdown
        by_status = stats.get("by_status", {})
        if by_status:
            results["validations"].append("   Status breakdown:")
            for status, count in by_status.items():
                results["validations"].append(f"     • {status}: {count}")

        return results

    except json.JSONDecodeError as e:
        results["success"] = False
        results["validations"].append(f"❌ Invalid JSON in registry: {e}")
        return results
    except Exception as e:
        results["success"] = False
        results["validations"].append(f"❌ Error reading registry: {e}")
        return results


def validate_feedback(specs_path: Path, feedback_id: str) -> Dict:
    """Validate a specific feedback item."""
    results = {
        "success": True,
        "feedback_id": feedback_id,
        "validations": [],
        "timestamp": datetime.now().isoformat()
    }

    registry_path = get_feedback_registry_path(specs_path)
    if not registry_path.exists():
        results["success"] = False
        results["validations"].append("❌ Feedback registry not found")
        return results

    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)

        # Find the feedback item
        feedback_item = None
        for item in registry.get("feedback_items", []):
            if item.get("id") == feedback_id:
                feedback_item = item
                break

        if not feedback_item:
            results["success"] = False
            results["validations"].append(f"❌ Feedback {feedback_id} not found in registry")
            return results

        results["validations"].append(f"✅ Found {feedback_id} in registry")
        results["validations"].append(f"   Status: {feedback_item.get('status')}")
        results["validations"].append(f"   Type: {feedback_item.get('type')}")

        # Get session folder
        session_folder = feedback_item.get("session_folder")
        if not session_folder:
            results["success"] = False
            results["validations"].append("❌ No session folder recorded")
            return results

        session_path = specs_path / session_folder
        if not session_path.exists():
            results["success"] = False
            results["validations"].append(f"❌ Session folder not found: {session_folder}")
            return results

        results["validations"].append(f"✅ Session folder exists: {session_folder}")

        # Check required files based on status
        status = feedback_item.get("status", "")
        required_files = ["FEEDBACK_ORIGINAL.md"]

        if status in ["approved", "in_progress", "implemented", "validated", "closed"]:
            required_files.append("impact_analysis.md")

        if status in ["in_progress", "implemented", "validated", "closed"]:
            required_files.extend(["implementation_options.md", "implementation_plan.md"])

        if status in ["implemented", "validated", "closed"]:
            required_files.append("implementation_log.md")

        if status in ["validated", "closed"]:
            required_files.extend(["files_changed.md", "VALIDATION_REPORT.md", "FEEDBACK_SUMMARY.md"])

        for req_file in required_files:
            file_path = session_path / req_file
            if file_path.exists():
                results["validations"].append(f"✅ {req_file}")
            else:
                results["validations"].append(f"❌ {req_file} - Not found")
                results["success"] = False

        return results

    except Exception as e:
        results["success"] = False
        results["validations"].append(f"❌ Error: {e}")
        return results


def list_feedback(specs_path: Path) -> Dict:
    """List all feedback items with their status."""
    results = {
        "success": True,
        "feedback_items": [],
        "validations": [],
        "timestamp": datetime.now().isoformat()
    }

    registry_path = get_feedback_registry_path(specs_path)
    if not registry_path.exists():
        results["validations"].append("ℹ️ No feedback registry found")
        results["validations"].append("   No feedback has been processed yet")
        return results

    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)

        feedback_items = registry.get("feedback_items", [])

        if not feedback_items:
            results["validations"].append("ℹ️ No feedback items in registry")
            return results

        results["validations"].append(f"📋 Feedback Items ({len(feedback_items)} total)")
        results["validations"].append("─" * 50)

        # Group by status
        by_status = {}
        for item in feedback_items:
            status = item.get("status", "unknown")
            if status not in by_status:
                by_status[status] = []
            by_status[status].append(item)

        # Display in order
        status_order = ["registered", "approved", "in_progress", "implemented", "validated", "closed", "rejected", "failed"]

        for status in status_order:
            if status in by_status:
                items = by_status[status]
                results["validations"].append(f"\n  {status.upper()} ({len(items)}):")
                for item in items:
                    feedback_id = item.get("id", "?")
                    title = item.get("title", "Untitled")[:40]
                    fb_type = item.get("type", "?")
                    results["validations"].append(f"    • {feedback_id} [{fb_type}]: {title}")
                    results["feedback_items"].append({
                        "id": feedback_id,
                        "status": status,
                        "type": fb_type,
                        "title": item.get("title", "Untitled")
                    })

        return results

    except Exception as e:
        results["success"] = False
        results["validations"].append(f"❌ Error reading registry: {e}")
        return results


def list_checkpoints() -> None:
    """List all checkpoint requirements."""
    print("\n" + "=" * 60)
    print("  PRODUCTSPECS CHECKPOINTS")
    print("=" * 60 + "\n")

    for cp, req in CHECKPOINT_REQUIREMENTS.items():
        print(f"  Checkpoint {cp}: {req['name']}")
        print(f"  {'-' * 50}")
        print(f"  {req['description']}")

        if "required_files" in req:
            print(f"\n  Required Files:")
            for f in req["required_files"]:
                print(f"    • {f}")

        if "required_folders" in req:
            print(f"\n  Required Folders:")
            for f in req["required_folders"]:
                print(f"    • {f}/")

        print("\n")


def print_results(results: Dict) -> None:
    """Print validation results in a formatted way."""
    if "error" in results:
        print(f"\n❌ ERROR: {results['error']}\n")
        return

    status = "✅ PASSED" if results["success"] else "❌ FAILED"

    print("\n" + "=" * 60)
    if "checkpoint" in results:
        print(f"  Checkpoint {results['checkpoint']}: {results['name']} - {status}")
    elif "file" in results:
        print(f"  File Validation: {results['file']} - {status}")
    elif "feedback_id" in results:
        print(f"  Feedback Validation: {results['feedback_id']} - {status}")
    else:
        print(f"  Validation - {status}")
    print("=" * 60 + "\n")

    for validation in results.get("validations", []):
        print(f"  {validation}")

    if "coverage" in results:
        print("\n  Coverage Metrics:")
        for key, value in results["coverage"].items():
            if isinstance(value, dict):
                print(f"    • {key}:")
                for k, v in value.items():
                    print(f"      - {k}: {v}")
            else:
                print(f"    • {key}: {value}")

    if "statistics" in results:
        print("\n  Statistics:")
        for key, value in results["statistics"].items():
            print(f"    • {key}: {value}")

    print("")


def main():
    parser = argparse.ArgumentParser(
        description="ProductSpecs Quality Gates - Checkpoint Validation"
    )

    parser.add_argument(
        "--validate-checkpoint",
        type=int,
        metavar="N",
        help="Validate specific checkpoint (0-8)"
    )

    parser.add_argument(
        "--validate-file",
        type=str,
        metavar="PATH",
        help="Validate specific file"
    )

    parser.add_argument(
        "--validate-traceability",
        action="store_true",
        help="Validate traceability linkages"
    )

    parser.add_argument(
        "--validate-modules",
        action="store_true",
        help="Validate module specifications quality"
    )

    parser.add_argument(
        "--validate-jira",
        action="store_true",
        help="Validate JIRA export files"
    )

    parser.add_argument(
        "--validate-module-registry",
        action="store_true",
        help="Validate module registry at ROOT level (traceability/module_registry.json)"
    )

    parser.add_argument(
        "--validate-feedback",
        type=str,
        metavar="PS-NNN",
        help="Validate a specific feedback item (e.g., PS-001)"
    )

    parser.add_argument(
        "--validate-feedback-registry",
        action="store_true",
        help="Validate the feedback registry structure"
    )

    parser.add_argument(
        "--list-feedback",
        action="store_true",
        help="List all feedback items with status"
    )

    parser.add_argument(
        "--list-checkpoints",
        action="store_true",
        help="List all checkpoint requirements"
    )

    # N/A validation options
    parser.add_argument(
        "--validate-na-file",
        type=str,
        metavar="PATH",
        help="Validate a NOT_APPLICABLE file format"
    )

    parser.add_argument(
        "--show-classification",
        action="store_true",
        help="Show current project classification"
    )

    parser.add_argument(
        "--list-na-artifacts",
        action="store_true",
        help="List all N/A artifacts in ProductSpecs"
    )

    parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help="ProductSpecs directory path"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    if args.list_checkpoints:
        list_checkpoints()
        sys.exit(0)

    # N/A validation handlers
    if args.show_classification:
        show_project_classification()
        sys.exit(0)

    if args.validate_na_file:
        valid, msg = validate_na_file(Path(args.validate_na_file))
        if args.json:
            print(json.dumps({"valid": valid, "message": msg}))
        else:
            print(f"{'✅' if valid else '❌'} {msg}")
        sys.exit(0 if valid else 1)

    if args.list_na_artifacts:
        base_path = Path(args.dir)
        list_na_artifacts_report(base_path, "productspecs")
        sys.exit(0)

    if args.validate_checkpoint is not None:
        results = validate_checkpoint(args.validate_checkpoint, args.dir)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)
        sys.exit(0 if results["success"] else 1)

    if args.validate_file:
        results = validate_file(args.validate_file)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)
        sys.exit(0 if results["success"] else 1)

    if args.validate_traceability:
        results = validate_traceability(args.dir)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)
        sys.exit(0 if results["success"] else 1)

    if args.validate_modules:
        results = validate_modules(args.dir)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)
        sys.exit(0 if results["success"] else 1)

    if args.validate_jira:
        base_path = Path(args.dir)
        passed, messages = validate_jira_export(base_path, {"check_csv_format": True, "check_hierarchy": True})
        results = {
            "success": passed,
            "validations": messages
        }
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)
        sys.exit(0 if passed else 1)

    if args.validate_module_registry:
        base_path = Path(args.dir)
        config = {
            "check_type": "registry_populated",
            "min_items": 1,
            "required_fields": ["id", "title", "app", "priority", "phase"]
        }
        passed, messages = validate_module_registry(base_path, config)
        results = {
            "success": passed,
            "validations": messages,
            "timestamp": datetime.now().isoformat()
        }
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print("\n" + "=" * 60)
            print("  MODULE REGISTRY VALIDATION - " + ("✅ PASSED" if passed else "❌ FAILED"))
            print("=" * 60 + "\n")
            for msg in messages:
                print(f"  {msg}")
            print("")
        sys.exit(0 if passed else 1)

    if args.validate_feedback:
        base_path = Path(args.dir)
        results = validate_feedback(base_path, args.validate_feedback)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)
        sys.exit(0 if results["success"] else 1)

    if args.validate_feedback_registry:
        base_path = Path(args.dir)
        results = validate_feedback_registry(base_path)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)
        sys.exit(0 if results["success"] else 1)

    if args.list_feedback:
        base_path = Path(args.dir)
        results = list_feedback(base_path)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)
        sys.exit(0)

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
