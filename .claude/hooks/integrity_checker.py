#!/usr/bin/env python3
"""
Framework Integrity Checker

Unified validation tool for the AI-driven product development framework.
Checks _state/, traceability/, and build artifacts against templates and schemas.

Usage:
    python3 integrity_checker.py                    # Full integrity report
    python3 integrity_checker.py --quick            # Quick pass/fail
    python3 integrity_checker.py --section state    # Check _state/ only
    python3 integrity_checker.py --section trace    # Check traceability/ only
    python3 integrity_checker.py --section builds   # Check build artifacts only
    python3 integrity_checker.py --fix              # Show remediation commands
    python3 integrity_checker.py --json             # Output as JSON
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

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


# =============================================================================
# CONFIGURATION
# =============================================================================

TEMPLATES_PATH = Path(".claude/templates")
STATE_PATH = Path("_state")
TRACEABILITY_PATH = Path("traceability")

# Stage folder patterns
STAGE_FOLDERS = {
    "Discovery": "ClientAnalysis_*",
    "Prototype": "Prototype_*",
    "ProductSpecs": "ProductSpecs_*",
    "SolArch": "SolArch_*",
    "Implementation": "Implementation_*"
}

# Required state files per stage
STATE_FILES = {
    "Discovery": ["discovery_config.json", "discovery_progress.json"],
    "Prototype": ["prototype_config.json", "prototype_progress.json", "discovery_summary.json"],
    "ProductSpecs": ["productspecs_config.json", "productspecs_progress.json"],
    "SolArch": ["solarch_config.json", "solarch_progress.json"],
    "Implementation": ["implementation_config.json", "implementation_progress.json"]
}

# Required traceability files per stage
TRACEABILITY_FILES = {
    "Discovery": [
        "client_facts_registry.json",
        "pain_point_registry.json",
        "jtbd_registry.json",
        "user_type_registry.json"
    ],
    "Prototype": [
        "requirements_registry.json",  # CRITICAL: Must be propagated from _state/
        "screen_registry.json",
        "prototype_traceability_register.json"
    ],
    "ProductSpecs": [
        "module_registry.json",
        "nfr_registry.json",
        "epic_registry.json",
        "user_story_registry.json",
        "test_scenario_registry.json",
        "test_case_registry.json"
    ],
    "SolArch": [
        "component_registry.json",
        "adr_registry.json",
        "solarch_traceability_register.json"
    ],
    "Implementation": [
        "task_registry.json",
        "review_registry.json",
        "implementation_traceability_register.json"
    ],
    "Aggregation": [
        "trace_links.json",
        "traceability_matrix_master.json"
    ]
}

# CRITICAL propagation files - these MUST exist if stage checkpoint >= threshold
# Format: { "file": "path", "stage": "Stage", "checkpoint_threshold": N, "source": "source_path" }
CRITICAL_PROPAGATION_FILES = [
    {
        "file": "requirements_registry.json",
        "stage": "Prototype",
        "checkpoint_threshold": 2,
        "source": "_state/requirements_registry.json",
        "description": "Requirements registry must be propagated from _state/ to traceability/",
        "downstream_impact": ["ProductSpecs", "SolArch", "Implementation"]
    },
    {
        "file": "screen_registry.json",
        "stage": "Prototype",
        "checkpoint_threshold": 1,
        "source": "Prototype_ValidateDiscovery skill",
        "description": "Screen registry tracks all Discovery screens through prototype",
        "downstream_impact": ["ProductSpecs", "SolArch"]
    }
]

# Checkpoint requirements per stage
CHECKPOINT_REQUIREMENTS = {
    "Discovery": {
        0: ["00-management/PROGRESS_TRACKER.md"],
        1: ["01-analysis/ANALYSIS_SUMMARY.md"],
        2: ["01-analysis/PAIN_POINTS.md"],
        3: ["02-research/personas/PERSONA_*.md"],
        4: ["02-research/JOBS_TO_BE_DONE.md"],
        5: ["03-strategy/PRODUCT_VISION.md"],
        9: ["04-design-specs/screen-definitions.md"],
        11: ["05-documentation/VALIDATION_REPORT.md"]
    },
    "Prototype": {
        0: [],  # Config only
        1: [],  # Validation only
        8: ["01-components/component-index.md"],
        9: ["02-screens/screen-index.md"],
        12: ["prototype/src/"],
        14: ["05-validation/qa-report.md"]
    },
    "ProductSpecs": {
        0: [],
        3: ["01-modules/module-index.md"],
        6: ["03-tests/test-case-registry.md"],
        8: ["04-jira/full-hierarchy.csv"]
    },
    "SolArch": {
        0: [],
        4: ["05-building-blocks/overview.md"],
        8: ["09-decisions/ADR-001-*.md"],
        12: ["reports/VALIDATION_REPORT.md"]
    },
    "Implementation": {
        0: [],
        2: ["tasks/TASK_INDEX.md"],
        5: [],  # P0 complete - check task_registry
        6: ["reports/CODE_REVIEW.md"],
        9: ["reports/VALIDATION_REPORT.md"]
    }
}

# =============================================================================
# RESULT CLASSES
# =============================================================================

class Issue:
    """Represents a single integrity issue."""

    def __init__(self, severity: str, category: str, message: str,
                 file_path: str = None, fix_command: str = None):
        self.severity = severity  # CRITICAL, HIGH, MEDIUM, LOW
        self.category = category  # state, traceability, build, drift, links
        self.message = message
        self.file_path = file_path
        self.fix_command = fix_command

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "file_path": self.file_path,
            "fix_command": self.fix_command
        }


class IntegrityReport:
    """Aggregates all integrity check results."""

    def __init__(self, system_name: str = None):
        self.system_name = system_name or "Unknown"
        self.timestamp = datetime.now().isoformat()
        self.issues: List[Issue] = []
        self.state_status: Dict[str, Any] = {}
        self.traceability_status: Dict[str, Any] = {}
        self.propagation_status: Dict[str, Any] = {}  # CRITICAL propagation validation
        self.build_status: Dict[str, Any] = {}
        self.cross_links_status: Dict[str, Any] = {}
        self.template_drift: List[Dict] = []
        self.current_stage: str = None
        self.current_checkpoint: int = 0

    def add_issue(self, issue: Issue):
        self.issues.append(issue)

    @property
    def is_healthy(self) -> bool:
        return not any(i.severity in ["CRITICAL", "HIGH"] for i in self.issues)

    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "CRITICAL")

    @property
    def high_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "HIGH")

    @property
    def medium_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "MEDIUM")

    @property
    def low_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "LOW")

    def to_dict(self) -> dict:
        return {
            "system_name": self.system_name,
            "timestamp": self.timestamp,
            "is_healthy": self.is_healthy,
            "current_stage": self.current_stage,
            "current_checkpoint": self.current_checkpoint,
            "summary": {
                "critical": self.critical_count,
                "high": self.high_count,
                "medium": self.medium_count,
                "low": self.low_count,
                "total": len(self.issues)
            },
            "state_status": self.state_status,
            "traceability_status": self.traceability_status,
            "propagation_status": self.propagation_status,
            "build_status": self.build_status,
            "cross_links_status": self.cross_links_status,
            "template_drift": self.template_drift,
            "issues": [i.to_dict() for i in self.issues]
        }


# =============================================================================
# DETECTION FUNCTIONS
# =============================================================================

def detect_system_name() -> Optional[str]:
    """Detect system name from existing folders."""
    for pattern in STAGE_FOLDERS.values():
        matches = list(Path(".").glob(pattern))
        if matches:
            # Extract system name from folder name
            folder_name = matches[0].name
            parts = folder_name.split("_", 1)
            if len(parts) > 1:
                return parts[1]
    return None


def detect_current_stage() -> Tuple[str, int]:
    """Detect which stage is currently active and at what checkpoint."""
    # Check in reverse order (Implementation is latest)
    stage_order = ["Implementation", "SolArch", "ProductSpecs", "Prototype", "Discovery"]

    for stage in stage_order:
        pattern = STAGE_FOLDERS[stage]
        matches = list(Path(".").glob(pattern))
        if matches:
            # Found a stage folder, now check progress file
            progress_file = STATE_PATH / f"{stage.lower()}_progress.json"
            if progress_file.exists():
                try:
                    with open(progress_file) as f:
                        progress = json.load(f)
                    checkpoint = progress.get("current_checkpoint", 0)
                    return stage, checkpoint
                except:
                    return stage, 0
            return stage, 0

    return "None", 0


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_state_files(report: IntegrityReport) -> Dict[str, Any]:
    """Validate _state/ folder files."""
    status = {
        "folder_exists": STATE_PATH.exists(),
        "files": {},
        "total": 0,
        "present": 0,
        "valid": 0
    }

    if not STATE_PATH.exists():
        report.add_issue(Issue(
            "CRITICAL", "state",
            "_state/ folder does not exist",
            fix_command="mkdir -p _state"
        ))
        return status

    # Check all expected state files
    all_state_files = set()
    for files in STATE_FILES.values():
        all_state_files.update(files)

    # Add FAILURES_LOG.md
    all_state_files.add("FAILURES_LOG.md")

    status["total"] = len(all_state_files)

    for filename in sorted(all_state_files):
        file_path = STATE_PATH / filename
        file_status = {
            "exists": file_path.exists(),
            "valid_json": False,
            "has_documentation": False,
            "size": 0
        }

        if file_path.exists():
            status["present"] += 1
            file_status["size"] = file_path.stat().st_size

            if filename.endswith(".json"):
                try:
                    with open(file_path) as f:
                        data = json.load(f)
                    file_status["valid_json"] = True
                    file_status["has_documentation"] = "$documentation" in data

                    if not file_status["has_documentation"]:
                        report.add_issue(Issue(
                            "LOW", "state",
                            f"Missing $documentation block in {filename}",
                            file_path=str(file_path),
                            fix_command=f"# Add $documentation to {filename}"
                        ))
                    else:
                        status["valid"] += 1

                except json.JSONDecodeError as e:
                    report.add_issue(Issue(
                        "HIGH", "state",
                        f"Invalid JSON in {filename}: {e}",
                        file_path=str(file_path)
                    ))
            else:
                status["valid"] += 1  # Non-JSON files just need to exist
        else:
            # Determine severity based on current stage
            stage_for_file = None
            for stage, files in STATE_FILES.items():
                if filename in files:
                    stage_for_file = stage
                    break

            # Only report as issue if we're at or past that stage
            if stage_for_file and report.current_stage:
                stage_order = list(STATE_FILES.keys())
                current_idx = stage_order.index(report.current_stage) if report.current_stage in stage_order else -1
                file_idx = stage_order.index(stage_for_file) if stage_for_file in stage_order else -1

                if current_idx >= file_idx:
                    report.add_issue(Issue(
                        "MEDIUM", "state",
                        f"Missing state file: {filename}",
                        file_path=str(file_path),
                        fix_command=f"/{stage_for_file.lower()}-init"
                    ))

        status["files"][filename] = file_status

    return status


def validate_traceability_files(report: IntegrityReport) -> Dict[str, Any]:
    """Validate traceability/ folder files against schema index."""
    status = {
        "folder_exists": TRACEABILITY_PATH.exists(),
        "files": {},
        "total": 0,
        "present": 0,
        "valid": 0,
        "schema_version": None
    }

    if not TRACEABILITY_PATH.exists():
        report.add_issue(Issue(
            "CRITICAL", "traceability",
            "traceability/ folder does not exist",
            fix_command="/traceability-init"
        ))
        return status

    # Load schema index if available
    schema_index_path = TEMPLATES_PATH / "traceability/schemas/_schema_index.json"
    expected_files = set()

    if schema_index_path.exists():
        try:
            with open(schema_index_path) as f:
                schema_index = json.load(f)
            status["schema_version"] = schema_index.get("schema_version", "unknown")

            # Collect all expected files from schema index
            for stage_files in schema_index.get("registries", {}).values():
                for reg in stage_files:
                    expected_files.add(reg["file"])
        except:
            pass

    # Fallback to hardcoded list if schema index not available
    if not expected_files:
        for files in TRACEABILITY_FILES.values():
            expected_files.update(files)

    status["total"] = len(expected_files)

    for filename in sorted(expected_files):
        file_path = TRACEABILITY_PATH / filename
        file_status = {
            "exists": file_path.exists(),
            "valid_json": False,
            "has_documentation": False,
            "items_count": 0,
            "schema_version": None
        }

        if file_path.exists():
            status["present"] += 1

            try:
                with open(file_path) as f:
                    data = json.load(f)
                file_status["valid_json"] = True
                file_status["has_documentation"] = "$documentation" in data
                file_status["schema_version"] = data.get("schema_version")

                # Count items
                for key in ["items", "facts", "pain_points", "jtbd", "tasks", "reviews", "links"]:
                    if key in data:
                        file_status["items_count"] = len(data[key])
                        break

                if not file_status["has_documentation"]:
                    report.add_issue(Issue(
                        "MEDIUM", "traceability",
                        f"Missing $documentation in {filename}",
                        file_path=str(file_path),
                        fix_command="/traceability-init --repair"
                    ))
                else:
                    status["valid"] += 1

            except json.JSONDecodeError as e:
                report.add_issue(Issue(
                    "HIGH", "traceability",
                    f"Invalid JSON in {filename}: {e}",
                    file_path=str(file_path)
                ))
        else:
            # Determine which stage this file belongs to
            stage_for_file = None
            for stage, files in TRACEABILITY_FILES.items():
                if filename in files:
                    stage_for_file = stage
                    break

            severity = "LOW"
            if stage_for_file == "Aggregation":
                severity = "LOW"
            elif report.current_stage:
                stage_order = list(TRACEABILITY_FILES.keys())
                if stage_for_file in stage_order:
                    current_idx = stage_order.index(report.current_stage) if report.current_stage in stage_order else -1
                    file_idx = stage_order.index(stage_for_file)
                    if current_idx >= file_idx:
                        severity = "MEDIUM"

            report.add_issue(Issue(
                severity, "traceability",
                f"Missing traceability file: {filename}",
                file_path=str(file_path),
                fix_command="/traceability-init --repair"
            ))

        status["files"][filename] = file_status

    return status


def validate_critical_propagation(report: IntegrityReport) -> Dict[str, Any]:
    """
    Validate critical propagation files that MUST exist after specific checkpoints.

    These files are critical for the end-to-end traceability chain. If they are missing,
    downstream stages will have broken references and incomplete traceability.
    """
    status = {
        "checks_run": 0,
        "checks_passed": 0,
        "critical_failures": []
    }

    for prop_file in CRITICAL_PROPAGATION_FILES:
        file_path = TRACEABILITY_PATH / prop_file["file"]
        stage = prop_file["stage"]
        threshold = prop_file["checkpoint_threshold"]

        # Check if we've passed the checkpoint threshold for this file
        progress_file = STATE_PATH / f"{stage.lower()}_progress.json"
        current_checkpoint = -1

        if progress_file.exists():
            try:
                with open(progress_file) as f:
                    progress = json.load(f)
                current_checkpoint = progress.get("current_checkpoint", -1)
            except:
                pass

        # Only validate if we've passed the threshold
        if current_checkpoint >= threshold:
            status["checks_run"] += 1

            if not file_path.exists():
                status["critical_failures"].append({
                    "file": prop_file["file"],
                    "stage": stage,
                    "checkpoint": current_checkpoint,
                    "threshold": threshold,
                    "source": prop_file["source"],
                    "impact": prop_file["downstream_impact"]
                })

                # This is a CRITICAL issue
                report.add_issue(Issue(
                    "CRITICAL", "traceability",
                    f"PROPAGATION FAILURE: {prop_file['file']} is missing after {stage} CP{threshold}",
                    file_path=str(file_path),
                    fix_command=f"/traceability-init --repair  # Or re-run {stage} phase"
                ))

                # Add detailed context
                report.add_issue(Issue(
                    "HIGH", "traceability",
                    f"  → Source: {prop_file['source']}",
                    file_path=str(file_path)
                ))
                report.add_issue(Issue(
                    "HIGH", "traceability",
                    f"  → Impact: Breaks traceability for {', '.join(prop_file['downstream_impact'])}",
                    file_path=str(file_path)
                ))
            else:
                status["checks_passed"] += 1

                # Verify the file has content
                try:
                    with open(file_path) as f:
                        data = json.load(f)

                    items = data.get("items", data.get("requirements", []))
                    if not items or len(items) == 0:
                        report.add_issue(Issue(
                            "HIGH", "traceability",
                            f"EMPTY FILE: {prop_file['file']} exists but has no items",
                            file_path=str(file_path),
                            fix_command=f"Re-run {stage} phase to populate the file"
                        ))
                except:
                    pass

    return status


def validate_build_artifacts(report: IntegrityReport) -> Dict[str, Any]:
    """Validate build artifacts for each stage."""
    status = {}

    for stage, pattern in STAGE_FOLDERS.items():
        matches = list(Path(".").glob(pattern))
        stage_status = {
            "folder_exists": len(matches) > 0,
            "folder_path": str(matches[0]) if matches else None,
            "checkpoints": {},
            "total_files": 0,
            "checkpoint_reached": 0
        }

        if matches:
            stage_path = matches[0]

            # Count total files
            stage_status["total_files"] = sum(1 for _ in stage_path.rglob("*") if _.is_file())

            # Check checkpoint requirements
            if stage in CHECKPOINT_REQUIREMENTS:
                for cp, requirements in CHECKPOINT_REQUIREMENTS[stage].items():
                    cp_status = {"required": requirements, "found": [], "missing": []}

                    for req in requirements:
                        req_matches = list(stage_path.glob(req))
                        if req_matches:
                            cp_status["found"].append(req)
                        else:
                            cp_status["missing"].append(req)

                    cp_status["passed"] = len(cp_status["missing"]) == 0
                    if cp_status["passed"]:
                        stage_status["checkpoint_reached"] = max(stage_status["checkpoint_reached"], cp)

                    stage_status["checkpoints"][cp] = cp_status

                    # Report missing artifacts for current stage
                    if stage == report.current_stage and cp <= report.current_checkpoint:
                        for missing in cp_status["missing"]:
                            report.add_issue(Issue(
                                "MEDIUM", "build",
                                f"{stage} CP{cp}: Missing {missing}",
                                file_path=str(stage_path / missing),
                                fix_command=f"/{stage.lower()}-resume"
                            ))

        status[stage] = stage_status

    return status


def validate_cross_stage_links(report: IntegrityReport) -> Dict[str, Any]:
    """Validate that IDs referenced across registries actually exist."""
    status = {
        "orphan_references": [],
        "broken_chains": [],
        "coverage": {}
    }

    # Load all registries
    registries = {}
    registry_files = [
        ("client_facts", "client_facts_registry.json", ["facts"], "id"),
        ("pain_points", "pain_point_registry.json", ["pain_points", "items"], "id"),
        ("jtbd", "jtbd_registry.json", ["jtbd", "items"], "id"),
        ("requirements", "requirements_registry.json", ["items"], "id"),
        ("screens", "screen_registry.json", ["discovery_screens", "screens"], "id"),
        ("modules", "module_registry.json", ["items"], "id"),
        ("tasks", "task_registry.json", ["tasks"], "id"),
        ("adrs", "adr_registry.json", ["items"], "id")
    ]

    for name, filename, item_keys, id_field in registry_files:
        file_path = TRACEABILITY_PATH / filename
        if file_path.exists():
            try:
                with open(file_path) as f:
                    data = json.load(f)

                items = []
                for key in item_keys:
                    if key in data:
                        items = data[key]
                        break

                registries[name] = {item.get(id_field): item for item in items if item.get(id_field)}
            except:
                pass

    # Check references
    reference_checks = [
        ("pain_points", "client_fact_refs", "client_facts"),
        ("jtbd", "related_pain_points", "pain_points"),
        ("requirements", "jtbd_refs", "jtbd"),
        ("requirements", "pain_point_refs", "pain_points"),
        ("modules", "screen_refs", "screens"),
        ("tasks", "module_ref", "modules")
    ]

    for source_reg, ref_field, target_reg in reference_checks:
        if source_reg not in registries or target_reg not in registries:
            continue

        source_items = registries[source_reg]
        target_items = registries[target_reg]

        for item_id, item in source_items.items():
            refs = item.get(ref_field, [])
            if isinstance(refs, str):
                refs = [refs]

            for ref in refs:
                if ref and ref not in target_items:
                    status["orphan_references"].append({
                        "source": f"{source_reg}/{item_id}",
                        "reference": ref,
                        "expected_in": target_reg
                    })
                    report.add_issue(Issue(
                        "MEDIUM", "links",
                        f"Orphan reference: {item_id} references {ref} but it doesn't exist in {target_reg}",
                        fix_command=f"# Check {ref} in traceability/{target_reg.replace('_', '_')}_registry.json"
                    ))

    # Calculate coverage
    for name, items in registries.items():
        status["coverage"][name] = len(items)

    return status


def detect_template_drift(report: IntegrityReport) -> List[Dict]:
    """Detect files that have drifted from their templates."""
    drift = []

    # Check traceability files against init templates
    init_path = TEMPLATES_PATH / "traceability/init"
    if init_path.exists():
        for template_file in init_path.glob("*.init.json"):
            # Get the actual file name (remove .init from name)
            actual_name = template_file.name.replace(".init.json", ".json")
            actual_path = TRACEABILITY_PATH / actual_name

            if actual_path.exists():
                try:
                    with open(template_file) as f:
                        template_data = json.load(f)
                    with open(actual_path) as f:
                        actual_data = json.load(f)

                    # Compare $documentation blocks
                    template_doc = template_data.get("$documentation", {})
                    actual_doc = actual_data.get("$documentation", {})

                    # Check for missing keys in actual
                    missing_keys = set(template_doc.keys()) - set(actual_doc.keys())
                    if missing_keys:
                        drift.append({
                            "file": actual_name,
                            "type": "missing_documentation_keys",
                            "missing": list(missing_keys)
                        })
                        report.add_issue(Issue(
                            "LOW", "drift",
                            f"Template drift in {actual_name}: missing $documentation keys: {missing_keys}",
                            file_path=str(actual_path),
                            fix_command="/traceability-init --repair"
                        ))

                    # Check schema version
                    template_version = template_data.get("schema_version")
                    actual_version = actual_data.get("schema_version")
                    if template_version and actual_version and template_version != actual_version:
                        drift.append({
                            "file": actual_name,
                            "type": "schema_version_mismatch",
                            "template_version": template_version,
                            "actual_version": actual_version
                        })

                except:
                    pass

    return drift


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_text_report(report: IntegrityReport, show_fix: bool = False) -> str:
    """Generate human-readable text report."""
    lines = []

    # Header
    lines.append("")
    lines.append("╔" + "═" * 70 + "╗")
    lines.append("║" + "FRAMEWORK INTEGRITY REPORT".center(70) + "║")
    lines.append("║" + f"System: {report.system_name} | Generated: {report.timestamp[:19]}".center(70) + "║")
    lines.append("╚" + "═" * 70 + "╝")
    lines.append("")

    # Overall status
    status_icon = "✅" if report.is_healthy else "❌"
    status_text = "HEALTHY" if report.is_healthy else "ISSUES FOUND"
    lines.append(f"Overall Status: {status_icon} {status_text}")
    lines.append(f"Current Stage: {report.current_stage} (Checkpoint {report.current_checkpoint})")
    lines.append(f"Issues: {report.critical_count} CRITICAL | {report.high_count} HIGH | {report.medium_count} MEDIUM | {report.low_count} LOW")
    lines.append("")

    # State Files Section
    lines.append("─" * 72)
    lines.append("📁 STATE FILES (_state/)")
    lines.append("─" * 72)

    state = report.state_status
    if state.get("folder_exists"):
        lines.append(f"   Present: {state.get('present', 0)}/{state.get('total', 0)} files")
        lines.append(f"   Valid: {state.get('valid', 0)}/{state.get('present', 0)} files")
        lines.append("")

        # File table
        lines.append("   ┌─────────────────────────────────────┬────────┬───────────────┐")
        lines.append("   │ File                                │ Status │ Notes         │")
        lines.append("   ├─────────────────────────────────────┼────────┼───────────────┤")

        for filename, fstatus in state.get("files", {}).items():
            icon = "✅" if fstatus.get("exists") and (not filename.endswith(".json") or fstatus.get("valid_json")) else "❌"
            notes = ""
            if not fstatus.get("exists"):
                notes = "Missing"
            elif filename.endswith(".json") and not fstatus.get("valid_json"):
                notes = "Invalid JSON"
            elif filename.endswith(".json") and not fstatus.get("has_documentation"):
                notes = "No $doc"

            lines.append(f"   │ {filename:<35} │ {icon:^6} │ {notes:<13} │")

        lines.append("   └─────────────────────────────────────┴────────┴───────────────┘")
    else:
        lines.append("   ❌ Folder does not exist")
    lines.append("")

    # Traceability Section
    lines.append("─" * 72)
    lines.append("📊 TRACEABILITY (traceability/)")
    lines.append("─" * 72)

    trace = report.traceability_status
    if trace.get("folder_exists"):
        lines.append(f"   Schema Version: {trace.get('schema_version', 'unknown')}")
        lines.append(f"   Present: {trace.get('present', 0)}/{trace.get('total', 0)} files")
        lines.append(f"   Valid: {trace.get('valid', 0)}/{trace.get('present', 0)} files")
        lines.append("")

        # Summarize by status
        missing = [f for f, s in trace.get("files", {}).items() if not s.get("exists")]
        invalid = [f for f, s in trace.get("files", {}).items() if s.get("exists") and not s.get("valid_json")]
        no_doc = [f for f, s in trace.get("files", {}).items() if s.get("exists") and s.get("valid_json") and not s.get("has_documentation")]

        if missing:
            lines.append(f"   Missing files: {', '.join(missing[:3])}{'...' if len(missing) > 3 else ''}")
        if invalid:
            lines.append(f"   Invalid JSON: {', '.join(invalid)}")
        if no_doc:
            lines.append(f"   Missing $documentation: {', '.join(no_doc[:3])}{'...' if len(no_doc) > 3 else ''}")
    else:
        lines.append("   ❌ Folder does not exist")
    lines.append("")

    # Critical Propagation Section
    prop = report.propagation_status
    if prop and prop.get("checks_run", 0) > 0:
        lines.append("─" * 72)
        lines.append("🚨 CRITICAL PROPAGATION CHECKS")
        lines.append("─" * 72)
        lines.append(f"   Checks run: {prop.get('checks_run', 0)} | Passed: {prop.get('checks_passed', 0)}")

        if prop.get("critical_failures"):
            lines.append("")
            lines.append("   ⛔ CRITICAL FAILURES (Blocks downstream stages):")
            for failure in prop["critical_failures"]:
                lines.append(f"   │")
                lines.append(f"   ├── File: {failure['file']}")
                lines.append(f"   ├── Stage: {failure['stage']} (CP{failure['checkpoint']} >= threshold CP{failure['threshold']})")
                lines.append(f"   ├── Source: {failure['source']}")
                lines.append(f"   └── Impact: {', '.join(failure['impact'])}")
            lines.append("")
            lines.append("   ⚠️  These files MUST exist for end-to-end traceability!")
            lines.append("   Fix: Re-run the stage phase or use /traceability-init --repair")
        else:
            lines.append("   ✅ All critical propagation files present")
        lines.append("")

    # Build Artifacts Section
    lines.append("─" * 72)
    lines.append("🏗️  BUILD ARTIFACTS BY STAGE")
    lines.append("─" * 72)
    lines.append("")
    lines.append("   ┌─────────────────┬────────┬────────┬────────┬──────────────────────────┐")
    lines.append("   │ Stage           │ CP     │ Status │ Files  │ Notes                    │")
    lines.append("   ├─────────────────┼────────┼────────┼────────┼──────────────────────────┤")

    for stage in ["Discovery", "Prototype", "ProductSpecs", "SolArch", "Implementation"]:
        build = report.build_status.get(stage, {})
        if build.get("folder_exists"):
            cp_reached = build.get("checkpoint_reached", 0)
            max_cp = max(CHECKPOINT_REQUIREMENTS.get(stage, {0: []}).keys()) if stage in CHECKPOINT_REQUIREMENTS else 0
            icon = "✅" if cp_reached >= max_cp else "⚠️"
            files = build.get("total_files", 0)
            notes = "Complete" if cp_reached >= max_cp else f"At CP{cp_reached}"
            lines.append(f"   │ {stage:<15} │ {cp_reached:>2}/{max_cp:<2}  │ {icon:^6} │ {files:>6} │ {notes:<24} │")
        else:
            lines.append(f"   │ {stage:<15} │ {'--':^6} │ {'⬜':^6} │ {'--':>6} │ {'Not started':<24} │")

    lines.append("   └─────────────────┴────────┴────────┴────────┴──────────────────────────┘")
    lines.append("")

    # Cross-stage Links Section
    links = report.cross_links_status
    if links.get("orphan_references"):
        lines.append("─" * 72)
        lines.append("🔗 CROSS-STAGE LINK ISSUES")
        lines.append("─" * 72)
        lines.append(f"   Orphan references: {len(links['orphan_references'])}")
        for orphan in links["orphan_references"][:5]:
            lines.append(f"   - {orphan['source']} → {orphan['reference']} (not in {orphan['expected_in']})")
        if len(links["orphan_references"]) > 5:
            lines.append(f"   ... and {len(links['orphan_references']) - 5} more")
        lines.append("")

    # Template Drift Section
    if report.template_drift:
        lines.append("─" * 72)
        lines.append("📐 TEMPLATE DRIFT")
        lines.append("─" * 72)
        for drift in report.template_drift[:5]:
            lines.append(f"   - {drift['file']}: {drift['type']}")
        lines.append("")

    # Remediation Section
    if show_fix and report.issues:
        lines.append("─" * 72)
        lines.append("📋 REMEDIATION ACTIONS")
        lines.append("─" * 72)

        # Group by severity
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            severity_issues = [i for i in report.issues if i.severity == severity and i.fix_command]
            if severity_issues:
                lines.append(f"   [{severity}]")
                for issue in severity_issues[:5]:
                    lines.append(f"   → {issue.fix_command}")
                    lines.append(f"     ({issue.message})")
                if len(severity_issues) > 5:
                    lines.append(f"   ... and {len(severity_issues) - 5} more {severity} issues")
                lines.append("")

    lines.append("─" * 72)
    lines.append("")

    return "\n".join(lines)


def generate_quick_report(report: IntegrityReport) -> str:
    """Generate quick pass/fail summary."""
    status_icon = "✅" if report.is_healthy else "❌"
    status_text = "HEALTHY" if report.is_healthy else "UNHEALTHY"

    state_count = f"{report.state_status.get('present', 0)}/{report.state_status.get('total', 0)}"
    trace_count = f"{report.traceability_status.get('present', 0)}/{report.traceability_status.get('total', 0)}"

    return f"""
{status_icon} Framework Integrity: {status_text}
   System: {report.system_name}
   Stage: {report.current_stage} (CP{report.current_checkpoint})
   State files: {state_count} | Traceability: {trace_count}
   Issues: {report.critical_count}C {report.high_count}H {report.medium_count}M {report.low_count}L
   {"Run: /integrity-check --fix for details" if not report.is_healthy else ""}
"""


# =============================================================================
# MAIN
# =============================================================================

def run_integrity_check(quick: bool = False, section: str = None,
                        show_fix: bool = False, output_json: bool = False) -> IntegrityReport:
    """Run the full integrity check."""
    system_name = detect_system_name() or "Unknown"
    current_stage, current_checkpoint = detect_current_stage()

    report = IntegrityReport(system_name)
    report.current_stage = current_stage
    report.current_checkpoint = current_checkpoint

    # Run validations based on section filter
    if section is None or section == "state":
        report.state_status = validate_state_files(report)

    if section is None or section == "trace":
        report.traceability_status = validate_traceability_files(report)
        # CRITICAL: Also validate propagation files that MUST exist after checkpoints
        report.propagation_status = validate_critical_propagation(report)

    if section is None or section == "builds":
        report.build_status = validate_build_artifacts(report)

    if section is None or section == "links":
        report.cross_links_status = validate_cross_stage_links(report)

    if section is None or section == "drift":
        report.template_drift = detect_template_drift(report)

    return report


def main():
    parser = argparse.ArgumentParser(description="Framework Integrity Checker")
    parser.add_argument("--quick", action="store_true", help="Quick pass/fail check")
    parser.add_argument("--section", choices=["state", "trace", "builds", "links", "drift", "na"],
                        help="Check specific section only ('na' for N/A artifacts)")
    parser.add_argument("--fix", action="store_true", help="Show remediation commands")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    # N/A validation options
    parser.add_argument("--validate-na-file", type=str, metavar="PATH",
                        help="Validate a NOT_APPLICABLE file format")
    parser.add_argument("--show-classification", action="store_true",
                        help="Show current project classification")
    parser.add_argument("--list-na-artifacts", action="store_true",
                        help="List all N/A artifacts across all stages")

    args = parser.parse_args()

    # N/A validation handlers
    if args.show_classification:
        show_project_classification()
        sys.exit(0)

    if args.validate_na_file:
        valid, msg = validate_na_file(Path(args.validate_na_file))
        print(f"{'✅' if valid else '❌'} {msg}")
        sys.exit(0 if valid else 1)

    if args.list_na_artifacts:
        print("\n" + "=" * 60)
        print("  NOT_APPLICABLE ARTIFACTS - ALL STAGES")
        print("=" * 60)
        for stage in ["discovery", "prototype", "productspecs", "solarch", "implementation"]:
            stage_folders = {
                "discovery": "ClientAnalysis_*",
                "prototype": "Prototype_*",
                "productspecs": "ProductSpecs_*",
                "solarch": "SolArch_*",
                "implementation": "Implementation_*"
            }
            import glob
            folders = glob.glob(stage_folders.get(stage, "*"))
            if folders:
                for folder in folders:
                    print(f"\n{stage.upper()} ({folder}):")
                    na_artifacts = get_na_artifacts(Path(folder), stage)
                    if na_artifacts:
                        for artifact in na_artifacts:
                            print(f"  - {artifact['path']}")
                    else:
                        print("  (no N/A artifacts)")
        print("\n" + "=" * 60 + "\n")
        sys.exit(0)

    # Handle section=na specially
    if args.section == "na":
        args.show_classification = True
        show_project_classification()
        args.list_na_artifacts = True
        sys.exit(0)

    report = run_integrity_check(
        quick=args.quick,
        section=args.section,
        show_fix=args.fix,
        output_json=args.json
    )

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    elif args.quick:
        print(generate_quick_report(report))
    else:
        print(generate_text_report(report, show_fix=args.fix))

    # Exit with appropriate code
    sys.exit(0 if report.is_healthy else 1)


if __name__ == "__main__":
    main()
