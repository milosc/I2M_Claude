#!/usr/bin/env python3
"""
Implementation Stage Quality Gates

Validates checkpoint completion and quality criteria for Stage 5: Implementation.
Supports checkpoint validation, task verification, traceability checks, and
automatic placeholder file generation for empty folders.

Usage:
    python3 implementation_quality_gates.py --list-checkpoints
    python3 implementation_quality_gates.py --validate-checkpoint 6 --dir Implementation_X/
    python3 implementation_quality_gates.py --validate-task T-015 --dir Implementation_X/
    python3 implementation_quality_gates.py --validate-traceability --dir Implementation_X/
    python3 implementation_quality_gates.py --ensure-placeholders --dir Implementation_X/
    python3 implementation_quality_gates.py --check-empty-folders --dir Implementation_X/
"""

import sys
import json
import os
import re
import argparse
from pathlib import Path
from typing import Tuple, Dict, List, Any, Optional

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
ARTIFACT_TO_CHECKPOINT = {
    # Implementation artifacts - most are applicable to all project types
    "tasks": ["traceability/task_registry.json", "tasks/TASK_INDEX.md"],
    "code-review": ["reports/CODE_REVIEW.md"],
    "integration-tests": ["reports/INTEGRATION_REPORT.md"],
}

# Configuration
LOG_FILE = Path(__file__).parent / "hook_log.jsonl"


def log_event(hook_type: str, data: dict, decision: str) -> None:
    """Log hook event for debugging."""
    try:
        with open(LOG_FILE, "a") as f:
            log_entry = {
                "hook_type": hook_type,
                "tool_name": data.get("tool_name"),
                "decision": decision,
                "timestamp": os.getpid()
            }
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass


def validate_state_files() -> Tuple[bool, str]:
    """Validate that implementation state files exist and have proper structure."""
    state_dir = Path("_state")
    if not state_dir.exists():
        return False, "_state/ directory does not exist"

    required_state_files = [
        "implementation_config.json",
        "implementation_progress.json"
    ]

    for sf in required_state_files:
        sf_path = state_dir / sf
        if not sf_path.exists():
            return False, f"Missing required state file: _state/{sf}"
        if sf_path.stat().st_size < 50:
            return False, f"State file _state/{sf} is too small (likely empty or invalid)"

    # Validate implementation_progress.json structure
    try:
        with open(state_dir / "implementation_progress.json") as f:
            progress = json.load(f)

        if "checkpoints" not in progress:
            return False, "_state/implementation_progress.json missing 'checkpoints' key"
        if "current_checkpoint" not in progress:
            return False, "_state/implementation_progress.json missing 'current_checkpoint' key"
    except json.JSONDecodeError as e:
        return False, f"_state/implementation_progress.json is not valid JSON: {e}"

    return True, "State files validated"


def validate_task_registry() -> Tuple[bool, str]:
    """Validate that task registry exists and has proper structure."""
    registry_path = Path("traceability/task_registry.json")

    if not registry_path.exists():
        return False, "traceability/task_registry.json does not exist"

    try:
        with open(registry_path) as f:
            registry = json.load(f)

        if "tasks" not in registry:
            return False, "task_registry.json missing 'tasks' key"
        if "statistics" not in registry:
            return False, "task_registry.json missing 'statistics' key"

        return True, f"Task registry valid ({len(registry['tasks'])} tasks)"
    except json.JSONDecodeError as e:
        return False, f"task_registry.json is not valid JSON: {e}"


def validate_checkpoint(checkpoint_num: int, target_dir: Optional[str] = None) -> Tuple[bool, str]:
    """Check if mandatory files for a checkpoint exist.

    Checkpoint requirements:
    - CP0: Initialize - config and folder structure
    - CP1: Validate Inputs - input validation (BLOCKING)
    - CP2: Tasks - task registry populated
    - CP3: Infrastructure - phase 3 tasks complete
    - CP4: Features 50% - half of feature tasks
    - CP5: P0 Complete - all P0 tasks done
    - CP6: Code Review - review passed (BLOCKING)
    - CP7: Integration - integration tests pass
    - CP8: Documentation - docs generated
    - CP9: Validation - final validation
    """

    # Define checkpoint requirements
    required: Dict[str, Dict[str, Any]] = {
        "0": {
            "name": "Initialize",
            "state_files": ["implementation_config.json"],
            "output_folders": ["src", "tests", "docs", "tasks", "reports"],
            "blocking": False
        },
        "1": {
            "name": "Validate Inputs",
            "state_files": ["implementation_input_validation.json"],
            "validation": "input_validation_passed",
            "blocking": True
        },
        "2": {
            "name": "Task Decomposition",
            "traceability_files": ["task_registry.json"],
            "output_files": ["tasks/TASK_INDEX.md"],
            "min_tasks": 1,
            "blocking": False
        },
        "3": {
            "name": "Infrastructure",
            "phase_complete": 3,
            "blocking": False
        },
        "4": {
            "name": "Features 50%",
            "min_completion": 50,
            "blocking": False
        },
        "5": {
            "name": "P0 Complete",
            "p0_complete": True,
            "blocking": False
        },
        "6": {
            "name": "Code Review",
            "output_files": ["reports/CODE_REVIEW.md"],
            "review_passed": True,
            "blocking": True
        },
        "7": {
            "name": "Integration",
            "output_files": ["reports/INTEGRATION_REPORT.md"],
            "blocking": False
        },
        "8": {
            "name": "Documentation",
            "output_files": [
                "docs/API_DOCUMENTATION.md",
                "docs/DEPLOYMENT_GUIDE.md",
                "README.md"
            ],
            "blocking": False
        },
        "9": {
            "name": "Validation",
            "output_files": [
                "reports/VALIDATION_REPORT.md",
                "reports/IMPLEMENTATION_SUMMARY.md"
            ],
            "traceability_files": ["implementation_traceability_register.json"],
            "blocking": False
        }
    }

    cp_key = str(checkpoint_num)
    if cp_key not in required:
        return False, f"Unknown checkpoint: {checkpoint_num}"

    cp = required[cp_key]
    base_dir = Path(".")

    # Determine implementation directory
    if target_dir:
        impl_path = Path(target_dir)
        if not impl_path.exists():
            return False, f"Implementation directory {target_dir} not found."
    else:
        impl_dirs = list(base_dir.glob("Implementation_*"))
        if not impl_dirs:
            if checkpoint_num == 0:
                return True, "Checkpoint 0: Ready to initialize"
            return False, "No Implementation_* directory found."
        impl_path = impl_dirs[0]

    # Check state files
    if "state_files" in cp:
        state_dir = base_dir / "_state"
        for sf in cp["state_files"]:
            sf_path = state_dir / sf
            if not sf_path.exists():
                return False, f"CP{checkpoint_num}: Missing state file _state/{sf}"
            if sf_path.stat().st_size < 50:
                return False, f"CP{checkpoint_num}: State file _state/{sf} is too small"

    # Check traceability files
    if "traceability_files" in cp:
        trace_dir = base_dir / "traceability"
        for tf in cp["traceability_files"]:
            tf_path = trace_dir / tf
            if not tf_path.exists():
                return False, f"CP{checkpoint_num}: Missing traceability/{tf}"

    # Check output folders
    if "output_folders" in cp:
        for folder in cp["output_folders"]:
            folder_path = impl_path / folder
            if not folder_path.exists():
                return False, f"CP{checkpoint_num}: Missing folder {impl_path.name}/{folder}"

    # Check output files
    if "output_files" in cp:
        for of in cp["output_files"]:
            of_path = impl_path / of
            if not of_path.exists():
                return False, f"CP{checkpoint_num}: Missing {impl_path.name}/{of}"
            if of_path.stat().st_size < 100:
                return False, f"CP{checkpoint_num}: File {of} is too small (<100 bytes)"

    # Check input validation passed (CP1)
    if cp.get("validation") == "input_validation_passed":
        validation_path = base_dir / "_state" / "implementation_input_validation.json"
        if validation_path.exists():
            try:
                with open(validation_path) as f:
                    validation = json.load(f)
                if validation.get("status") != "passed":
                    return False, f"CP{checkpoint_num} BLOCKED: Input validation failed. Fix issues and re-run /htec-sdd-validate"
            except json.JSONDecodeError:
                return False, f"CP{checkpoint_num}: Invalid JSON in input validation file"

    # Check minimum tasks (CP2)
    if "min_tasks" in cp:
        registry_path = base_dir / "traceability" / "task_registry.json"
        if registry_path.exists():
            try:
                with open(registry_path) as f:
                    registry = json.load(f)
                task_count = len(registry.get("tasks", {}))
                if task_count < cp["min_tasks"]:
                    return False, f"CP{checkpoint_num}: Need at least {cp['min_tasks']} tasks, found {task_count}"
            except json.JSONDecodeError:
                return False, f"CP{checkpoint_num}: Invalid task registry JSON"

    # Check phase completion (CP3)
    if "phase_complete" in cp:
        phase = cp["phase_complete"]
        registry_path = base_dir / "traceability" / "task_registry.json"
        if registry_path.exists():
            try:
                with open(registry_path) as f:
                    registry = json.load(f)
                tasks = registry.get("tasks", {})
                phase_tasks = [t for t in tasks.values() if t.get("phase") == phase]
                completed = [t for t in phase_tasks if t.get("status") == "completed"]
                if len(phase_tasks) > 0 and len(completed) < len(phase_tasks):
                    return False, f"CP{checkpoint_num}: Phase {phase} not complete ({len(completed)}/{len(phase_tasks)} tasks)"
            except json.JSONDecodeError:
                return False, f"CP{checkpoint_num}: Invalid task registry JSON"

    # Check minimum completion percentage (CP4)
    if "min_completion" in cp:
        registry_path = base_dir / "traceability" / "task_registry.json"
        if registry_path.exists():
            try:
                with open(registry_path) as f:
                    registry = json.load(f)
                stats = registry.get("statistics", {})
                total = stats.get("total", 0)
                completed = stats.get("by_status", {}).get("completed", 0)
                if total > 0:
                    pct = (completed / total) * 100
                    if pct < cp["min_completion"]:
                        return False, f"CP{checkpoint_num}: Need {cp['min_completion']}% completion, have {pct:.1f}%"
            except json.JSONDecodeError:
                return False, f"CP{checkpoint_num}: Invalid task registry JSON"

    # Check P0 complete (CP5)
    if cp.get("p0_complete"):
        registry_path = base_dir / "traceability" / "task_registry.json"
        if registry_path.exists():
            try:
                with open(registry_path) as f:
                    registry = json.load(f)
                tasks = registry.get("tasks", {})
                p0_tasks = [t for t in tasks.values() if t.get("priority") == "P0"]
                p0_completed = [t for t in p0_tasks if t.get("status") == "completed"]
                if len(p0_tasks) > 0 and len(p0_completed) < len(p0_tasks):
                    return False, f"CP{checkpoint_num}: P0 tasks not complete ({len(p0_completed)}/{len(p0_tasks)})"
            except json.JSONDecodeError:
                return False, f"CP{checkpoint_num}: Invalid task registry JSON"

    # Check code review passed (CP6)
    if cp.get("review_passed"):
        review_path = impl_path / "reports" / "review-findings.json"
        if review_path.exists():
            try:
                with open(review_path) as f:
                    review = json.load(f)
                if review.get("blocking_status") != "passed":
                    critical = review.get("summary", {}).get("critical", 0)
                    high = review.get("summary", {}).get("high", 0)
                    return False, f"CP{checkpoint_num} BLOCKED: Code review has {critical} critical, {high} high findings"
            except json.JSONDecodeError:
                pass  # If no JSON, check markdown exists which we already did

    # AUTO-CREATE PLACEHOLDERS: Ensure empty folders have _readme.md files
    # This is triggered at any checkpoint validation (Option 2: at checkpoint validation)
    try:
        success, msg, created_files = ensure_placeholders(impl_path, auto_create=True)
        if created_files:
            # Log the auto-created files (non-blocking, just informational)
            log_event("checkpoint_validation", {
                "checkpoint": checkpoint_num,
                "impl_path": str(impl_path),
                "auto_created_placeholders": created_files
            }, "placeholders_created")
    except Exception as e:
        # Placeholder creation is non-blocking - log but don't fail
        log_event("checkpoint_validation", {
            "checkpoint": checkpoint_num,
            "error": str(e)
        }, "placeholder_creation_failed")

    blocking_msg = " [BLOCKING]" if cp.get("blocking") else ""
    return True, f"Checkpoint {checkpoint_num} ({cp['name']}){blocking_msg} validated for {impl_path.name}"


def validate_task(task_id: str, target_dir: Optional[str] = None) -> Tuple[bool, str]:
    """Validate a specific task's completion criteria."""
    base_dir = Path(".")
    registry_path = base_dir / "traceability" / "task_registry.json"

    if not registry_path.exists():
        return False, "Task registry not found"

    try:
        with open(registry_path) as f:
            registry = json.load(f)
    except json.JSONDecodeError:
        return False, "Invalid task registry JSON"

    tasks = registry.get("tasks", {})
    if task_id not in tasks:
        return False, f"Task {task_id} not found in registry"

    task = tasks[task_id]

    # Check if task is completed
    if task.get("status") != "completed":
        return False, f"Task {task_id} status is '{task.get('status')}', not completed"

    # Check acceptance criteria
    ac = task.get("acceptance_criteria", [])
    for criterion in ac:
        if criterion.get("status") != "passed":
            return False, f"Task {task_id}: Acceptance criterion {criterion.get('id')} not passed"

    # Check implementation files exist
    impl = task.get("implementation", {})
    if target_dir:
        impl_path = Path(target_dir)
    else:
        impl_dirs = list(base_dir.glob("Implementation_*"))
        impl_path = impl_dirs[0] if impl_dirs else base_dir

    for created_file in impl.get("files_created", []):
        file_path = impl_path / created_file
        if not file_path.exists():
            return False, f"Task {task_id}: Created file {created_file} not found"

    for test_file in impl.get("tests_created", []):
        test_path = impl_path / test_file
        if not test_path.exists():
            return False, f"Task {task_id}: Test file {test_file} not found"

    return True, f"Task {task_id} validated: {len(ac)} ACs passed, {len(impl.get('files_created', []))} files created"


def validate_traceability(target_dir: Optional[str] = None) -> Tuple[bool, str]:
    """Validate end-to-end traceability coverage."""
    base_dir = Path(".")

    # Load registries
    registries = {}
    registry_files = [
        ("pain_points", "traceability/pain_point_registry.json"),
        ("requirements", "traceability/requirements_registry.json"),
        ("tasks", "traceability/task_registry.json"),
    ]

    for name, path in registry_files:
        full_path = base_dir / path
        if full_path.exists():
            try:
                with open(full_path) as f:
                    registries[name] = json.load(f)
            except json.JSONDecodeError:
                return False, f"Invalid JSON in {path}"

    if "tasks" not in registries:
        return False, "Task registry not found for traceability validation"

    tasks = registries["tasks"].get("tasks", {})

    # Check P0 pain point coverage
    if "pain_points" in registries:
        pp_items = registries["pain_points"].get("pain_points", registries["pain_points"].get("items", []))
        p0_pps = [pp for pp in pp_items if pp.get("priority") == "P0"]

        for pp in p0_pps:
            pp_id = pp.get("id")
            # Check if any task references this pain point
            has_task = any(
                pp_id in t.get("pain_point_refs", [])
                for t in tasks.values()
            )
            if not has_task:
                return False, f"P0 pain point {pp_id} has no implementing task"

    # Check requirement coverage
    if "requirements" in registries:
        req_items = registries["requirements"].get("requirements", registries["requirements"].get("items", []))

        for req in req_items:
            req_id = req.get("id")
            # Check if any task references this requirement
            has_task = any(
                req_id in t.get("requirement_refs", [])
                for t in tasks.values()
            )
            if not has_task and req.get("priority") == "P0":
                return False, f"P0 requirement {req_id} has no implementing task"

    # Summary
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks.values() if t.get("status") == "completed"])

    return True, f"Traceability validated: {completed_tasks}/{total_tasks} tasks complete"


def list_checkpoints() -> None:
    """Print all checkpoint requirements."""
    checkpoints = {
        "0": ("Initialize", [
            "_state/implementation_config.json",
            "Implementation_*/src/",
            "Implementation_*/tests/",
            "Implementation_*/tasks/",
        ], False),
        "1": ("Validate Inputs", [
            "_state/implementation_input_validation.json",
            "ProductSpecs checkpoint 8+",
            "SolArch checkpoint 12+",
        ], True),
        "2": ("Task Decomposition", [
            "traceability/task_registry.json",
            "Implementation_*/tasks/TASK_INDEX.md",
            "Implementation_*/tasks/T-*.md",
        ], False),
        "3": ("Infrastructure", [
            "All Phase 3 tasks completed",
            "Project structure set up",
        ], False),
        "4": ("Features 50%", [
            "50%+ of all tasks completed",
        ], False),
        "5": ("P0 Complete", [
            "All P0 priority tasks completed",
        ], False),
        "6": ("Code Review", [
            "Implementation_*/reports/CODE_REVIEW.md",
            "Implementation_*/reports/review-findings.json",
            "No CRITICAL findings",
            "No HIGH findings (conf > 80%)",
            "Test coverage > 80%",
        ], True),
        "7": ("Integration", [
            "Implementation_*/reports/INTEGRATION_REPORT.md",
            "Cross-module tests pass",
            "API contract validation",
        ], False),
        "8": ("Documentation", [
            "Implementation_*/docs/API_DOCUMENTATION.md",
            "Implementation_*/docs/DEPLOYMENT_GUIDE.md",
            "Implementation_*/README.md",
        ], False),
        "9": ("Validation", [
            "Implementation_*/reports/VALIDATION_REPORT.md",
            "Implementation_*/reports/IMPLEMENTATION_SUMMARY.md",
            "traceability/implementation_traceability_register.json",
        ], False),
    }

    print("\n Implementation Stage Checkpoint Requirements\n")
    print("=" * 65)
    for num, (name, files, blocking) in checkpoints.items():
        blocking_str = " [BLOCKING]" if blocking else ""
        print(f"\nCheckpoint {num}: {name}{blocking_str}")
        for f in files:
            print(f"  - {f}")
    print("\n" + "=" * 65)
    print("\nUsage:")
    print("  python3 implementation_quality_gates.py --validate-checkpoint 6 --dir Implementation_X/")
    print("  python3 implementation_quality_gates.py --validate-task T-015")
    print("  python3 implementation_quality_gates.py --validate-traceability")
    print("  python3 implementation_quality_gates.py --ensure-placeholders --dir Implementation_X/")


# =============================================================================
# PLACEHOLDER FILE GENERATION
# =============================================================================

# Folder metadata: defines what each folder should contain and placeholder text
FOLDER_PLACEHOLDERS: Dict[str, Dict[str, Any]] = {
    "00-setup": {
        "status": "Pending - Generated by /htec-sdd-validate",
        "purpose": "Project scaffolding and setup documentation",
        "expected_content": [
            ("project-scaffold.md", "Project structure decisions", "/htec-sdd-validate"),
            ("dependency-manifest.json", "All dependencies with versions", "/htec-sdd-validate"),
            ("environment-config.md", "Environment setup guide", "/htec-sdd-validate"),
        ],
        "generation_command": "/htec-sdd-validate {SystemName}",
    },
    "01-tasks": {
        "status": "Pending - Generated by /htec-sdd-tasks",
        "purpose": "Task specifications and execution logs",
        "expected_content": [
            ("TASK_INDEX.md", "Master task list", "/htec-sdd-tasks"),
            ("T-*.md", "Individual task specifications", "/htec-sdd-tasks"),
            ("<T-ID>/results/", "Per-task execution results", "/htec-sdd-implement"),
        ],
        "generation_command": "/htec-sdd-tasks {SystemName}",
    },
    "02-implementation": {
        "status": "Pending - Generated by /htec-sdd-implement",
        "purpose": "Production source code and test suites",
        "expected_content": [
            ("src/", "Production source code", "/htec-sdd-implement"),
            ("tests/", "Test suites (unit, integration, e2e)", "/htec-sdd-implement"),
            ("config/", "Configuration files", "/htec-sdd-implement"),
            ("test-specs/", "Test specification documents", "/htec-sdd-implement (Phase 3)"),
        ],
        "generation_command": "/htec-sdd-implement {SystemName} --task T-001",
        "monorepo_note": "If this project uses a monorepo structure, code lives in `packages/` instead.",
    },
    "03-tests": {
        "status": "Pending - Tests Generated by /htec-sdd-implement",
        "purpose": "Test aggregation and review outputs",
        "expected_content": [
            ("Test suites", "Unit, integration, E2E tests", "/htec-sdd-implement (Phase 4-5)"),
        ],
        "generation_command": "/htec-sdd-implement {SystemName}",
        "architecture_note": "The original architecture planned this folder as `03-review/` (code review outputs). Code reviews go to `reports/` folder.",
        "monorepo_note": "For monorepo projects, tests are co-located with source code in `packages/*/tests/`.",
    },
    "04-reports": {
        "status": "Pending - Generated by /htec-sdd-implement",
        "purpose": "Build artifacts and deployment configurations",
        "expected_content": [
            ("build-log.md", "Build execution log", "/htec-sdd-implement"),
            ("artifacts/", "Build outputs", "Package manager (pnpm/npm build)"),
            ("deployment-config/", "Docker, K8s manifests", "/htec-sdd-implement"),
        ],
        "generation_command": "/htec-sdd-implement {SystemName}",
        "architecture_note": "The original architecture planned this folder as `04-build/`. Build artifacts are generated in `packages/*/dist/` (monorepo) or `02-implementation/dist/` (standard).",
    },
    "05-documentation": {
        "status": "Pending - Generated by /htec-sdd-implement (Phase 7)",
        "purpose": "Implementation documentation",
        "expected_content": [
            ("IMPLEMENTATION_GUIDE.md", "Developer setup and workflow", "implementation-documenter agent"),
            ("API_REFERENCE.md", "Generated API documentation", "implementation-documenter agent"),
            ("TEST_PLAN.md", "Test strategy and coverage", "implementation-documenter agent"),
            ("RUNBOOK.md", "Operations and deployment guide", "implementation-documenter agent"),
        ],
        "generation_command": "/htec-sdd-implement {SystemName}",
    },
    "pr-metadata": {
        "status": "Pending - Generated by /htec-sdd-implement (Phase 7)",
        "purpose": "PR descriptions and metadata",
        "expected_content": [
            ("PR-{N}.md", "PR group metadata", "/htec-sdd-tasks"),
            ("PR-{N}-description.md", "Full PR description", "implementation-pr-preparer agent"),
        ],
        "generation_command": "/htec-sdd-implement {SystemName} --pr-group PR-001",
    },
    "reports": {
        "status": "Pending - Generated by /htec-sdd-implement and /htec-sdd-review",
        "purpose": "Quality reports and validation results",
        "expected_content": [
            ("CODE_REVIEW.md", "Multi-agent code review findings", "/htec-sdd-review or Phase 6"),
            ("review-findings.json", "Structured review data", "/htec-sdd-review or Phase 6"),
            ("VALIDATION_REPORT.md", "Final validation report", "/htec-sdd-implement (Phase 8)"),
            ("IMPLEMENTATION_SUMMARY.md", "Implementation summary", "/htec-sdd-implement (Phase 8)"),
        ],
        "generation_command": "/htec-sdd-review {SystemName}",
    },
    "scripts": {
        "status": "Pending - Generated by /htec-sdd-tasks",
        "purpose": "Automation scripts (worktree setup, build, deploy)",
        "expected_content": [
            ("setup-worktrees.sh", "Worktree setup script", "/htec-sdd-tasks"),
        ],
        "generation_command": "/htec-sdd-tasks {SystemName}",
    },
    "feedback-sessions": {
        "status": "Pending - Generated by /htec-sdd-changerequest",
        "purpose": "Change request and feedback tracking",
        "expected_content": [
            ("implementation_feedback_registry.json", "Feedback registry", "/htec-sdd-changerequest"),
        ],
        "generation_command": "/htec-sdd-changerequest",
    },
}


def generate_placeholder_content(folder_name: str, system_name: str, is_monorepo: bool = False) -> str:
    """Generate placeholder _readme.md content for a folder."""

    if folder_name not in FOLDER_PLACEHOLDERS:
        # Generic placeholder for unknown folders
        return f"""# {folder_name}

## Status: Empty

This folder does not have defined content in the Implementation architecture.

---

*This placeholder created automatically per HTEC Framework convention.*
"""

    meta = FOLDER_PLACEHOLDERS[folder_name]

    # Build content table
    content_rows = []
    for item in meta.get("expected_content", []):
        if len(item) == 3:
            name, purpose, generator = item
            content_rows.append(f"| `{name}` | {purpose} | {generator} |")

    content_table = "\\n".join(content_rows) if content_rows else "| (none defined) | | |"

    # Build the markdown
    lines = [
        f"# {folder_name}",
        "",
        f"## Status: {meta['status']}",
        "",
        f"{meta['purpose']}.",
        "",
    ]

    # Add architecture note if present
    if "architecture_note" in meta:
        lines.extend([
            "## Note on Architecture Naming",
            "",
            meta["architecture_note"],
            "",
        ])

    # Add expected content table
    lines.extend([
        "## Expected Content",
        "",
        "| File/Folder | Purpose | Generated By |",
        "|-------------|---------|--------------|",
    ])
    for item in meta.get("expected_content", []):
        if len(item) == 3:
            name, purpose, generator = item
            lines.append(f"| `{name}` | {purpose} | {generator} |")

    lines.append("")

    # Add monorepo note if applicable
    if is_monorepo and "monorepo_note" in meta:
        lines.extend([
            "## Monorepo Structure",
            "",
            meta["monorepo_note"],
            "",
        ])

    # Add generation command
    gen_cmd = meta.get("generation_command", "").replace("{SystemName}", system_name)
    if gen_cmd:
        lines.extend([
            "## Generation Command",
            "",
            "```bash",
            gen_cmd,
            "```",
            "",
        ])

    # Footer
    lines.extend([
        "---",
        "",
        "*This placeholder created automatically per HTEC Framework convention: folders must contain a file explaining why they're empty or where content resides.*",
    ])

    return "\\n".join(lines)


def is_folder_empty(folder_path: Path) -> bool:
    """Check if a folder is empty (contains no files except _readme.md)."""
    if not folder_path.exists() or not folder_path.is_dir():
        return True

    for item in folder_path.iterdir():
        # Ignore _readme.md placeholder files
        if item.name == "_readme.md":
            continue
        # Ignore hidden files
        if item.name.startswith("."):
            continue
        # Found non-placeholder content
        return False

    return True


def check_empty_folders(impl_dir: Path) -> List[Dict[str, Any]]:
    """Check for empty folders that need placeholders."""
    results = []

    for folder_name in FOLDER_PLACEHOLDERS.keys():
        folder_path = impl_dir / folder_name

        if not folder_path.exists():
            results.append({
                "folder": folder_name,
                "path": str(folder_path),
                "status": "missing",
                "has_readme": False,
            })
        elif is_folder_empty(folder_path):
            readme_path = folder_path / "_readme.md"
            results.append({
                "folder": folder_name,
                "path": str(folder_path),
                "status": "empty",
                "has_readme": readme_path.exists(),
            })
        else:
            readme_path = folder_path / "_readme.md"
            results.append({
                "folder": folder_name,
                "path": str(folder_path),
                "status": "has_content",
                "has_readme": readme_path.exists(),
            })

    return results


def ensure_placeholders(impl_dir: Path, system_name: str = None, auto_create: bool = True) -> Tuple[bool, str, List[str]]:
    """
    Check and optionally create placeholder files for empty folders.

    Returns:
        Tuple of (all_ok, message, list_of_created_files)
    """
    if not impl_dir.exists():
        return False, f"Implementation directory {impl_dir} does not exist", []

    # Detect system name from folder if not provided
    if not system_name:
        dir_name = impl_dir.name
        if dir_name.startswith("Implementation_"):
            system_name = dir_name[15:]  # Remove "Implementation_" prefix
        else:
            system_name = "SystemName"

    # Detect if monorepo
    is_monorepo = (impl_dir / "packages").exists()

    folder_status = check_empty_folders(impl_dir)
    created_files = []
    warnings = []

    for status in folder_status:
        folder_name = status["folder"]
        folder_path = Path(status["path"])

        # Skip if folder has content (not empty)
        if status["status"] == "has_content":
            continue

        # Create folder if missing
        if status["status"] == "missing":
            if auto_create:
                folder_path.mkdir(parents=True, exist_ok=True)
            else:
                warnings.append(f"Missing folder: {folder_name}")
                continue

        # Create _readme.md if missing
        if not status["has_readme"]:
            readme_path = folder_path / "_readme.md"
            if auto_create:
                content = generate_placeholder_content(folder_name, system_name, is_monorepo)
                # Fix escaped newlines
                content = content.replace("\\n", "\n")
                readme_path.write_text(content)
                created_files.append(str(readme_path))
            else:
                warnings.append(f"Empty folder without placeholder: {folder_name}")

    if warnings:
        return False, f"Found {len(warnings)} issues: " + ", ".join(warnings), created_files

    if created_files:
        return True, f"Created {len(created_files)} placeholder files", created_files

    return True, "All folders have appropriate content or placeholders", created_files


def main():
    parser = argparse.ArgumentParser(description="Implementation Stage Quality Gates")
    parser.add_argument("--list-checkpoints", action="store_true",
                        help="List all checkpoint requirements")
    parser.add_argument("--validate-checkpoint", type=int, metavar="N",
                        help="Validate specific checkpoint (0-9)")
    parser.add_argument("--validate-task", type=str, metavar="T-ID",
                        help="Validate specific task completion")
    parser.add_argument("--validate-traceability", action="store_true",
                        help="Validate end-to-end traceability")

    # N/A validation options
    parser.add_argument("--validate-na-file", type=str, metavar="PATH",
                        help="Validate a NOT_APPLICABLE file format")
    parser.add_argument("--show-classification", action="store_true",
                        help="Show current project classification")
    parser.add_argument("--list-na-artifacts", action="store_true",
                        help="List all N/A artifacts in Implementation")

    # Placeholder management options
    parser.add_argument("--ensure-placeholders", action="store_true",
                        help="Check and create placeholder _readme.md files for empty folders")
    parser.add_argument("--check-empty-folders", action="store_true",
                        help="Report empty folders without creating placeholders")
    parser.add_argument("--system-name", type=str, metavar="NAME",
                        help="System name for placeholder generation")

    parser.add_argument("--dir", type=str, metavar="PATH",
                        help="Target Implementation_* directory")

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
        base_dir = args.dir or "."
        list_na_artifacts_report(Path(base_dir), "implementation")
        sys.exit(0)

    # Placeholder management handlers
    if args.check_empty_folders:
        if not args.dir:
            # Auto-detect Implementation_* directory
            impl_dirs = list(Path(".").glob("Implementation_*"))
            if not impl_dirs:
                print("❌ No Implementation_* directory found. Use --dir to specify.")
                sys.exit(1)
            impl_dir = impl_dirs[0]
        else:
            impl_dir = Path(args.dir)

        if not impl_dir.exists():
            print(f"❌ Directory not found: {impl_dir}")
            sys.exit(1)

        print(f"\n📁 Checking empty folders in {impl_dir.name}...\n")
        folder_status = check_empty_folders(impl_dir)

        empty_count = 0
        missing_readme_count = 0

        for status in folder_status:
            folder_name = status["folder"]
            if status["status"] == "missing":
                print(f"  ❌ {folder_name}/ - MISSING")
                empty_count += 1
            elif status["status"] == "empty":
                if status["has_readme"]:
                    print(f"  ✓ {folder_name}/ - Empty (has _readme.md)")
                else:
                    print(f"  ⚠ {folder_name}/ - Empty (NO _readme.md)")
                    missing_readme_count += 1
                empty_count += 1
            else:
                print(f"  ✓ {folder_name}/ - Has content")

        print("")
        if missing_readme_count > 0:
            print(f"⚠ {missing_readme_count} empty folder(s) without placeholder files")
            print(f"  Run with --ensure-placeholders to create them")
            sys.exit(1)
        else:
            print(f"✓ All {empty_count} empty folders have placeholder files")
            sys.exit(0)

    if args.ensure_placeholders:
        if not args.dir:
            # Auto-detect Implementation_* directory
            impl_dirs = list(Path(".").glob("Implementation_*"))
            if not impl_dirs:
                print("❌ No Implementation_* directory found. Use --dir to specify.")
                sys.exit(1)
            impl_dir = impl_dirs[0]
        else:
            impl_dir = Path(args.dir)

        if not impl_dir.exists():
            print(f"❌ Directory not found: {impl_dir}")
            sys.exit(1)

        print(f"\n📁 Ensuring placeholders in {impl_dir.name}...\n")

        success, message, created_files = ensure_placeholders(
            impl_dir,
            system_name=args.system_name,
            auto_create=True
        )

        if created_files:
            print("Created placeholder files:")
            for f in created_files:
                print(f"  ✓ {f}")
            print("")

        if success:
            print(f"✓ {message}")
            sys.exit(0)
        else:
            print(f"❌ {message}")
            sys.exit(1)

    if args.list_checkpoints:
        list_checkpoints()
        sys.exit(0)

    if args.validate_checkpoint is not None:
        success, message = validate_checkpoint(args.validate_checkpoint, args.dir)
        if success:
            print(f"✓ {message}")
            sys.exit(0)
        else:
            print(f"✗ {message}")
            sys.exit(1)

    if args.validate_task:
        success, message = validate_task(args.validate_task, args.dir)
        if success:
            print(f"✓ {message}")
            sys.exit(0)
        else:
            print(f"✗ {message}")
            sys.exit(1)

    if args.validate_traceability:
        success, message = validate_traceability(args.dir)
        if success:
            print(f"✓ {message}")
            sys.exit(0)
        else:
            print(f"✗ {message}")
            sys.exit(1)

    # If no specific action, show help
    parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
