#!/usr/bin/env python3
import sys
import json
import os
import re
from pathlib import Path

# Configuration
LOG_FILE = Path("\"$CLAUDE_PROJECT_DIR/.claude/hooks/hook_log.jsonl\"")
PROJECT_ROOT = Path("\"$CLAUDE_PROJECT_DIR\"")

# Import project classifier if available
try:
    sys.path.insert(0, str(PROJECT_ROOT / ".claude/skills/tools"))
    from project_classifier import (
        load_project_classification,
        is_artifact_applicable,
        PROJECT_TYPES
    )
    HAS_CLASSIFIER = True
except ImportError:
    HAS_CLASSIFIER = False
    PROJECT_TYPES = ["FULL_STACK", "BACKEND_ONLY", "DATABASE_ONLY", "INTEGRATION", "INFRASTRUCTURE"]


def get_project_classification():
    """Load project classification from discovery_config.json."""
    config_path = PROJECT_ROOT / "_state" / "discovery_config.json"
    if not config_path.exists():
        return None

    try:
        with open(config_path) as f:
            config = json.load(f)
        return config.get("project_classification", None)
    except:
        return None


def check_artifact_applicability(artifact_name):
    """Check if an artifact is applicable for the current project type."""
    classification = get_project_classification()
    if not classification:
        return True  # Default to applicable if no classification

    applicability = classification.get("artifact_applicability", {})

    # Normalize artifact name for lookup
    normalized = artifact_name.lower().replace("_", "-").replace(" ", "-")

    # Direct lookup
    if normalized in applicability:
        return applicability[normalized]

    # Try uppercase version
    upper_name = artifact_name.upper().replace("-", "_")
    if upper_name in applicability:
        return applicability[upper_name]

    # Default to applicable
    return True


def validate_na_file(file_path):
    """Validate that a NOT_APPLICABLE file has correct format."""
    path = Path(file_path)
    if not path.exists():
        return False, f"N/A file {file_path} does not exist"

    content = path.read_text()

    # Check for required markers
    if "status: NOT_APPLICABLE" not in content and '"status": "NOT_APPLICABLE"' not in content:
        return False, f"File {file_path} missing NOT_APPLICABLE status marker"

    # For markdown files, check for reason
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


def is_na_file(file_path):
    """Check if a file is marked as NOT_APPLICABLE."""
    path = Path(file_path)
    if not path.exists():
        return False

    try:
        content = path.read_text()
        return "status: NOT_APPLICABLE" in content or '"status": "NOT_APPLICABLE"' in content
    except:
        return False

def log_event(hook_type, data, decision):
    """Log hook event for debugging."""
    try:
        with open(LOG_FILE, "a") as f:
            log_entry = {
                "hook_type": hook_type,
                "tool_name": data.get("tool_name"),
                "decision": decision,
                "timestamp": os.getpid() # Simple proxy for order/session
            }
            f.write(json.dumps(log_entry) + "\n")
    except:
        pass

def allow():
    """Output allow decision and exit."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow"
        }
    }
    print(json.dumps(output))
    sys.exit(0)

def deny(reason):
    """Output deny decision and exit."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "reason": reason
        }
    }
    # Some versions of Claude Code might use a different format for deny
    # But often just exiting non-zero or providing a message is enough.
    # We will try to provide a helpful reason.
    print(json.dumps(output))
    # We exit 0 because the hook itself finished successfully, but the decision is 'deny'
    # Actually, often a non-zero exit or a specific JSON is required.
    sys.exit(0)

def check_traceability_ids(content, file_path):
    """Check if content has required traceability IDs (PP-*, JTBD-*, etc)."""
    # Just a simple check for now
    patterns = [r"PP-\d+\.\d+", r"JTBD-\d+\.\d+", r"US-\d+\.\d+", r"S-\d+\.\d+"]
    if any(re.search(p, content) for p in patterns):
        return True
    
    # Check if the file name suggests it should have IDs
    if any(x in file_path.lower() for x in ["persona", "jtbd", "analysis", "spec"]):
        return False
    return True

import argparse

def validate_file(file_path):
    """Scan a file for mandatory metadata and traceability IDs."""
    path = Path(file_path)
    if not path.exists():
        return False, f"File {file_path} not found."
    
    content = path.read_text()
    
    # 1. Check for YAML Metadata Block
    if not (content.startswith("---") and "---" in content[4:]):
         return False, f"Missing YAML metadata block in {file_path}"

    # 2. Check for Traceability IDs (PP-*, JTBD-*, US-*, etc)
    patterns = {
        "PP": r"PP-\d+\.\d+",
        "JTBD": r"JTBD-\d+\.\d+",
        "REQ": r"(US|FR|NFR)-\d+\.\d+",
        "SCR": r"S-\d+\.\d+"
    }
    
    found_ids = {k: len(re.findall(v, content)) for k, v in patterns.items()}
    
    # Heuristic: persona files must have PP or JTBD, specs must have REQ or SCR
    if "persona" in file_path.lower() and found_ids["JTBD"] == 0:
        return False, f"No JTBD references found in persona file {file_path}"
    
    if "jtbd" in file_path.lower() and found_ids["PP"] == 0:
         return False, f"No Pain Point (PP) references found in JTBD file {file_path}"

    return True, f"Validation passed for {file_path} (IDs: {found_ids})"

def validate_state_files():
    """Validate that _state/ files exist and have proper structure."""
    state_dir = Path("_state")
    if not state_dir.exists():
        return False, "_state/ directory does not exist"

    required_state_files = [
        "discovery_config.json",
        "discovery_progress.json"
    ]

    for sf in required_state_files:
        sf_path = state_dir / sf
        if not sf_path.exists():
            return False, f"Missing required state file: _state/{sf}"
        if sf_path.stat().st_size < 50:
            return False, f"State file _state/{sf} is too small (likely empty or invalid)"

    # Validate discovery_progress.json has proper structure
    try:
        import json
        with open(state_dir / "discovery_progress.json") as f:
            progress = json.load(f)

        if "phases" not in progress:
            return False, "_state/discovery_progress.json missing 'phases' key"
        if "overall_progress" not in progress:
            return False, "_state/discovery_progress.json missing 'overall_progress' key"
    except json.JSONDecodeError as e:
        return False, f"_state/discovery_progress.json is not valid JSON: {e}"

    return True, "State files validated"

def validate_checkpoint(checkpoint_num, target_dir=None):
    """Check if mandatory files for a checkpoint exist.

    File naming conventions (v6.0):
    - Analysis, Research, Strategy: UPPERCASE with underscores
    - Design Specs: lowercase with dashes
    - Personas: Separate files in personas/ subfolder

    N/A Handling (v7.0):
    - If artifact is not applicable per project classification, check for N/A file
    - N/A files must have correct format with status, reason, and project_type
    """
    # First validate state files exist
    state_ok, state_msg = validate_state_files()
    if not state_ok:
        return False, f"State validation failed: {state_msg}"

    # Map patterns to artifact names for applicability check
    artifact_mapping = {
        "04-design-specs/screen-definitions.md": "screen-definitions",
        "04-design-specs/navigation-flows.md": "navigation-structure",
        "04-design-specs/data-fields.md": "data-fields",
        "04-design-specs/interaction-patterns.md": "interaction-patterns",
        "02-research/personas/PERSONA_*.md": "PERSONAS",
        "02-research/JOBS_TO_BE_DONE.md": "JOBS_TO_BE_DONE",
        "03-strategy/PRODUCT_VISION.md": "PRODUCT_VISION",
        "03-strategy/PRODUCT_STRATEGY.md": "PRODUCT_STRATEGY",
        "03-strategy/PRODUCT_ROADMAP.md": "PRODUCT_ROADMAP",
        "03-strategy/KPIS_AND_GOALS.md": "KPIS_AND_GOALS",
        "01-analysis/PAIN_POINTS.md": "PAIN_POINTS",
        "01-analysis/PDF_ANALYSIS_INDEX.md": "PDF_ANALYSIS",
        "01-analysis/PDF_FINDINGS_SUMMARY.md": "PDF_ANALYSIS",
    }

    required = {
        "0": ["00-management/PROGRESS_TRACKER.md", "00-management/FAILURES_LOG.md"],
        "1": ["01-analysis/ANALYSIS_SUMMARY.md"],
        "1.5": ["01-analysis/PDF_ANALYSIS_INDEX.md", "01-analysis/PDF_FINDINGS_SUMMARY.md"],
        "2": ["01-analysis/PAIN_POINTS.md", "01-analysis/USER_TYPES.md"],
        "3": ["02-research/personas/PERSONA_*.md"],
        "4": ["02-research/JOBS_TO_BE_DONE.md"],
        "5": ["03-strategy/PRODUCT_VISION.md"],
        "6": ["03-strategy/PRODUCT_STRATEGY.md"],
        "6.5": [
            "03-strategy/COMPETITIVE_LANDSCAPE.md",
            "03-strategy/THREAT_OPPORTUNITY_MATRIX.md",
            "03-strategy/DIFFERENTIATION_BLUEPRINT.md",
            "03-strategy/COMPETITIVE_INTELLIGENCE_SUMMARY.md"
        ],
        "7": ["03-strategy/PRODUCT_ROADMAP.md"],
        "8": ["03-strategy/KPIS_AND_GOALS.md"],
        "9": [
            "04-design-specs/screen-definitions.md",
            "04-design-specs/navigation-flows.md",
            "04-design-specs/data-fields.md",
            "04-design-specs/interaction-patterns.md"
        ],
        "10": [
            "05-documentation/INDEX.md",
            "05-documentation/README.md",
            "05-documentation/DOCUMENTATION_SUMMARY.md",
            "05-documentation/GETTING_STARTED.md",
            "05-documentation/FILES_CREATED.md"
        ],
        "11": ["05-documentation/VALIDATION_REPORT.md", "05-documentation/AUDIT_REPORT.md"]
    }

    # Check directory
    base_dir = Path(".")

    if target_dir:
        ca_path = Path(target_dir)
        if not ca_path.exists():
            return False, f"Output directory {target_dir} not found."
    else:
        # Find active ClientAnalysis folder
        ca_dirs = list(base_dir.glob("ClientAnalysis_*"))
        if not ca_dirs:
            return False, "No ClientAnalysis output directory found."
        ca_path = ca_dirs[0]

    # Special logic for Checkpoint 11: Fact Audit Verification
    if str(checkpoint_num) == "11":
        # Run the audit gate hook
        import subprocess
        audit_script = PROJECT_ROOT / ".claude/hooks/discovery_audit_gate.py"
        if audit_script.exists():
            try:
                result = subprocess.run(
                    [sys.executable, str(audit_script), str(ca_path)],
                    capture_output=True, text=True
                )
                if result.returncode != 0:
                    return False, f"Fact Audit Gate Failed: {result.stdout.strip()}"
            except Exception as e:
                return False, f"Error running audit gate: {str(e)}"

    na_artifacts = []  # Track N/A artifacts for summary

    if str(checkpoint_num) in required:
        for pattern in required[str(checkpoint_num)]:
            # Check artifact applicability
            artifact_name = artifact_mapping.get(pattern, None)
            is_applicable = True
            if artifact_name:
                is_applicable = check_artifact_applicability(artifact_name)

            files = list(ca_path.glob(pattern))

            if not is_applicable:
                # For non-applicable artifacts, check for N/A file
                if files:
                    # File exists - check if it's a valid N/A file
                    for f in files:
                        if is_na_file(f):
                            valid, msg = validate_na_file(f)
                            if not valid:
                                return False, msg
                            na_artifacts.append(f.name)
                        else:
                            # File exists but is not N/A - that's fine, user might have overridden
                            pass
                else:
                    # No file exists - create path for expected N/A file
                    expected_file = ca_path / pattern.replace("*", "NOT_APPLICABLE")
                    return False, f"Missing N/A file for non-applicable artifact: {expected_file}"
            else:
                # Normal validation for applicable artifacts
                if not files:
                    return False, f"Missing mandatory deliverable for Checkpoint {checkpoint_num} in {ca_path.name}: {pattern}"

                # Additional check: files must not be essentially empty (unless N/A)
                for f in files:
                    if is_na_file(f):
                        # Validate N/A format
                        valid, msg = validate_na_file(f)
                        if not valid:
                            return False, msg
                        na_artifacts.append(f.name)
                    elif f.stat().st_size < 100:
                        return False, f"Deliverable {f.name} for Checkpoint {checkpoint_num} is too small (<100 bytes)."

    # Checkpoint 1: Also validate client_facts_registry.json at ROOT traceability/
    if str(checkpoint_num) == "1":
        trace_path = base_dir / "traceability" / "client_facts_registry.json"
        if not trace_path.exists():
            return False, f"Missing traceability/client_facts_registry.json - Client facts MUST be extracted in Phase 1"
        try:
            with open(trace_path) as f:
                cf_data = json.load(f)

            # Check if it's an N/A registry
            if cf_data.get("status") == "NOT_APPLICABLE":
                na_artifacts.append("client_facts_registry.json")
            else:
                facts = cf_data.get("facts", cf_data.get("items", []))
                if not facts or len(facts) < 1:
                    return False, f"traceability/client_facts_registry.json is empty - MUST have at least one client fact!"
        except Exception as e:
            return False, f"Error reading client_facts_registry.json: {str(e)}"

    # Build success message
    success_msg = f"Checkpoint {checkpoint_num} deliverables verified in {ca_path.name}"
    if na_artifacts:
        success_msg += f" (N/A artifacts: {', '.join(na_artifacts)})"

    return True, success_msg

def list_checkpoints():
    """Print all checkpoint requirements."""
    checkpoints = {
        "0": ("Initialize", ["00-management/PROGRESS_TRACKER.md", "00-management/FAILURES_LOG.md"]),
        "1": ("Analyze Materials", ["01-analysis/ANALYSIS_SUMMARY.md", "traceability/client_facts_registry.json (ROOT)"]),
        "1.5": ("Deep PDF Analysis", ["01-analysis/PDF_ANALYSIS_INDEX.md", "01-analysis/PDF_FINDINGS_SUMMARY.md"]),
        "2": ("Extract Pain Points", ["01-analysis/PAIN_POINTS.md", "01-analysis/USER_TYPES.md"]),
        "3": ("Generate Personas", ["02-research/personas/PERSONA_*.md"]),
        "4": ("Generate JTBD", ["02-research/JOBS_TO_BE_DONE.md"]),
        "5": ("Product Vision", ["03-strategy/PRODUCT_VISION.md"]),
        "6": ("Product Strategy", ["03-strategy/PRODUCT_STRATEGY.md"]),
        "6.5": ("Competitive Intelligence", [
            "03-strategy/COMPETITIVE_LANDSCAPE.md",
            "03-strategy/THREAT_OPPORTUNITY_MATRIX.md",
            "03-strategy/DIFFERENTIATION_BLUEPRINT.md",
            "03-strategy/COMPETITIVE_INTELLIGENCE_SUMMARY.md"
        ]),
        "7": ("Product Roadmap", ["03-strategy/PRODUCT_ROADMAP.md"]),
        "8": ("KPIs & Goals", ["03-strategy/KPIS_AND_GOALS.md"]),
        "9": ("Design Specs", [
            "04-design-specs/screen-definitions.md",
            "04-design-specs/navigation-flows.md",
            "04-design-specs/data-fields.md",
            "04-design-specs/interaction-patterns.md"
        ]),
        "10": ("Documentation", [
            "05-documentation/INDEX.md",
            "05-documentation/README.md",
            "05-documentation/DOCUMENTATION_SUMMARY.md",
            "05-documentation/GETTING_STARTED.md",
            "05-documentation/FILES_CREATED.md"
        ]),
        "11": ("Validation Report", ["05-documentation/VALIDATION_REPORT.md"]),
    }

    print("\n📋 Discovery Checkpoint Requirements (v6.0)\n")
    print("=" * 60)
    for num, (name, files) in checkpoints.items():
        print(f"\nCheckpoint {num}: {name}")
        for f in files:
            print(f"  └── {f}")
    print("\n" + "=" * 60)
    print("\nUsage:")
    print("  python3 predictability_gate.py --validate-checkpoint 1 --dir ClientAnalysis_X/")
    print("  python3 predictability_gate.py --validate-file ClientAnalysis_X/02-research/JOBS_TO_BE_DONE.md")
    print()

def validate_progress_status(checkpoint_num):
    """Validate that progress file reflects completed phases up to checkpoint."""
    state_dir = Path("_state")
    progress_file = state_dir / "discovery_progress.json"

    if not progress_file.exists():
        return False, "discovery_progress.json not found"

    try:
        with open(progress_file) as f:
            progress = json.load(f)

        phases = progress.get("phases", {})
        overall = progress.get("overall_progress", 0)

        # Map checkpoint to expected completed phases
        expected_complete = {
            "0": ["0_init"],
            "1": ["0_init", "1_analyze"],
            "1.5": ["0_init", "1_analyze", "1.5_pdf_analysis"],
            "2": ["0_init", "1_analyze", "1.5_pdf_analysis", "2_extract"],
            "3": ["0_init", "1_analyze", "1.5_pdf_analysis", "2_extract", "3_personas"],
            "4": ["0_init", "1_analyze", "1.5_pdf_analysis", "2_extract", "3_personas", "4_jtbd"],
            "5": ["0_init", "1_analyze", "1.5_pdf_analysis", "2_extract", "3_personas", "4_jtbd", "5_vision"],
            "6": ["0_init", "1_analyze", "1.5_pdf_analysis", "2_extract", "3_personas", "4_jtbd", "5_vision", "6_strategy"],
            "6.5": ["0_init", "1_analyze", "1.5_pdf_analysis", "2_extract", "3_personas", "4_jtbd", "5_vision", "6_strategy", "6.5_competitive_intelligence"],
            "7": ["0_init", "1_analyze", "1.5_pdf_analysis", "2_extract", "3_personas", "4_jtbd", "5_vision", "6_strategy", "6.5_competitive_intelligence", "7_roadmap"],
            "8": ["0_init", "1_analyze", "1.5_pdf_analysis", "2_extract", "3_personas", "4_jtbd", "5_vision", "6_strategy", "6.5_competitive_intelligence", "7_roadmap", "8_kpis"],
            "9": ["0_init", "1_analyze", "1.5_pdf_analysis", "2_extract", "3_personas", "4_jtbd", "5_vision", "6_strategy", "6.5_competitive_intelligence", "7_roadmap", "8_kpis", "9_specs"],
            "10": ["0_init", "1_analyze", "1.5_pdf_analysis", "2_extract", "3_personas", "4_jtbd", "5_vision", "6_strategy", "6.5_competitive_intelligence", "7_roadmap", "8_kpis", "9_specs", "10_docs"],
            "11": ["0_init", "1_analyze", "1.5_pdf_analysis", "2_extract", "3_personas", "4_jtbd", "5_vision", "6_strategy", "6.5_competitive_intelligence", "7_roadmap", "8_kpis", "9_specs", "10_docs", "11_validate"],
        }

        if str(checkpoint_num) not in expected_complete:
            return True, "Unknown checkpoint, skipping progress validation"

        for phase in expected_complete.get(str(checkpoint_num), []):
            phase_status = phases.get(phase, {}).get("status", "pending")
            if phase_status != "complete":
                return False, f"Phase {phase} should be 'complete' but is '{phase_status}' - UPDATE _state/discovery_progress.json!"

        return True, f"Progress status validated for checkpoint {checkpoint_num}"

    except json.JSONDecodeError as e:
        return False, f"Invalid JSON in discovery_progress.json: {e}"


def validate_traceability_completeness():
    """Verify that traceability registries exist and have content."""
    trace_dir = Path("traceability")
    if not trace_dir.exists():
        return False, "traceability/ directory does not exist"

    registries = [
        "pain_point_registry.json",
        "jtbd_registry.json",
        "requirements_registry.json",
        "screen_registry.json",
        "module_registry.json",
        "adr_registry.json",
        "client_facts_registry.json",
        "trace_links.json",
        "trace_matrix.json",
        "user_type_registry.json"
    ]

    for reg in registries:
        reg_path = trace_dir / reg
        if not reg_path.exists():
            return False, f"Missing traceability registry: traceability/{reg}"
        
        # Check if registries that should be populated early have content
        if reg in ["client_facts_registry.json", "pain_point_registry.json", "jtbd_registry.json", "user_type_registry.json"]:
            try:
                with open(reg_path) as f:
                    full_data = json.load(f)

                # Handle exact keys from strict templates
                category = reg.replace("_registry.json", "")
                data_key = "items" # Default
                if category == "pain_point": data_key = "pain_points"
                elif category == "jtbd": data_key = "jtbd"
                elif category == "trace_matrix": data_key = "chains"
                elif category == "client_facts": data_key = "facts"
                
                if isinstance(full_data, list):
                    data = full_data
                elif isinstance(full_data, dict):
                    # Try specific key, then 'items', then empty
                    data = full_data.get(data_key, full_data.get("items", []))
                else:
                    data = []

                if not isinstance(data, list) or len(data) < 1:
                    return False, f"Traceability registry traceability/{reg} is empty - MUST have at least one entry!"
            except Exception as e:
                return False, f"Error reading traceability registry: traceability/{reg} - {str(e)}"

    # Check visualization files
    visuals = ["PROTOTYPE.md", "SPECIFICATION.md", "SOLUTION_ARCHITECTURE.md"]
    for vis in visuals:
        vis_path = trace_dir / vis
        if not vis_path.exists():
            return False, f"Missing traceability visualization file: traceability/{vis}"
        if vis_path.stat().st_size < 100:
            return False, f"Traceability visualization file traceability/{vis} is too small (likely unpopulated)"

    for helper in helpers:
        helper_path = helper_dir / helper
        if not helper_path.exists():
            return False, f"Missing helper file: helperFiles/{helper}"
        if helper_path.stat().st_size < 100:
            return False, f"Helper file helperFiles/{helper} is too small (likely unpopulated)"

    # Check for at least one complete chain in trace_matrix.json
    matrix_path = trace_dir / "trace_matrix.json"
    if matrix_path.exists():
        try:
            with open(matrix_path, "r") as f:
                matrix_data = json.load(f)
            chains = matrix_data.get("chains", [])
            if not chains:
                return False, "trace_matrix.json is empty - MUST have at least one traceability chain!"
            
            # Verify if at least one chain has the basic discovery elements
            has_complete_chain = False
            for chain in chains:
                if chain.get("pain_points") and chain.get("jtbd") and (chain.get("requirements") or chain.get("features")):
                     has_complete_chain = True
                     break
            
            if not has_complete_chain:
                return False, "No complete traceability chains found (PP -> JTBD -> REQ). Please link your discovery items!"
        except Exception as e:
            return False, f"Error validating trace_matrix.json: {str(e)}"

    return True, "Traceability completeness validated including helper files and chains"


def show_project_classification():
    """Display current project classification."""
    classification = get_project_classification()

    print("\n📊 Project Classification (Discovery Phase)\n")
    print("=" * 60)

    if not classification:
        print("No project classification found.")
        print("Run /discovery-init or Discovery_ClassifyProject to classify.")
        return

    print(f"Project Type: {classification.get('type', 'UNKNOWN')}")
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
            print(f"  ✅ {a}")

        if not_applicable:
            print(f"\nNot Applicable Artifacts ({len(not_applicable)}):")
            for a in not_applicable:
                print(f"  ⊘ {a}")

    print("\n" + "=" * 60)


def list_na_artifacts(target_dir=None):
    """List all N/A artifacts in the project."""
    base_dir = Path(".")

    if target_dir:
        ca_path = Path(target_dir)
    else:
        ca_dirs = list(base_dir.glob("ClientAnalysis_*"))
        if not ca_dirs:
            print("No ClientAnalysis directory found.")
            return
        ca_path = ca_dirs[0]

    print(f"\n📋 NOT_APPLICABLE Artifacts in {ca_path.name}\n")
    print("=" * 60)

    na_files = []

    # Scan for N/A markdown files
    for md_file in ca_path.rglob("*.md"):
        if is_na_file(md_file):
            na_files.append(md_file)

    # Scan traceability for N/A JSON files
    trace_dir = base_dir / "traceability"
    if trace_dir.exists():
        for json_file in trace_dir.glob("*.json"):
            if is_na_file(json_file):
                na_files.append(json_file)

    if na_files:
        for f in na_files:
            rel_path = f.relative_to(base_dir) if f.is_relative_to(base_dir) else f
            print(f"  ⊘ {rel_path}")
        print(f"\nTotal: {len(na_files)} N/A artifacts")
    else:
        print("  No N/A artifacts found.")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Discovery Predictability Gate - Validates deliverables and checkpoints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --validate-file ClientAnalysis_X/02-research/JOBS_TO_BE_DONE.md
  %(prog)s --validate-checkpoint 1 --dir ClientAnalysis_X/
  %(prog)s --validate-checkpoint 1.5 --dir ClientAnalysis_X/
  %(prog)s --validate-state
  %(prog)s --validate-progress 9
  %(prog)s --validate-na-file ClientAnalysis_X/04-design-specs/screen-definitions.md
  %(prog)s --show-classification
  %(prog)s --list-na-artifacts
  %(prog)s --list-checkpoints
        """
    )
    parser.add_argument("--validate-file", help="Path to markdown deliverable to validate")
    parser.add_argument("--validate-checkpoint", type=str, help="Checkpoint number to verify (0, 1, 1.5, 2-11)")
    parser.add_argument("--validate-state", action="store_true", help="Validate _state/ files exist and are valid")
    parser.add_argument("--validate-progress", type=str, help="Validate progress status for checkpoint (e.g., 9)")
    parser.add_argument("--validate-traceability", action="store_true", help="Validate traceability completeness")
    parser.add_argument("--validate-na-file", help="Validate a NOT_APPLICABLE file has correct format")
    parser.add_argument("--show-classification", action="store_true", help="Show current project classification")
    parser.add_argument("--list-na-artifacts", action="store_true", help="List all N/A artifacts in the project")
    parser.add_argument("--dir", help="Target Discovery output directory (e.g., ClientAnalysis_X/)")
    parser.add_argument("--list-checkpoints", action="store_true", help="List all checkpoint requirements")
    parser.add_argument("--check", choices=["notify", "write"], help="Backwards compat for hook attempts")

    args = parser.parse_args()

    if args.list_checkpoints:
        list_checkpoints()
        sys.exit(0)
    elif args.show_classification:
        show_project_classification()
        sys.exit(0)
    elif args.list_na_artifacts:
        list_na_artifacts(args.dir)
        sys.exit(0)
    elif args.validate_state:
        success, message = validate_state_files()
    elif args.validate_progress:
        success, message = validate_progress_status(args.validate_progress)
    elif args.validate_file:
        success, message = validate_file(args.validate_file)
    elif args.validate_na_file:
        success, message = validate_na_file(args.validate_na_file)
    elif args.validate_checkpoint:
        success, message = validate_checkpoint(args.validate_checkpoint, args.dir)
    elif args.validate_traceability:
        success, message = validate_traceability_completeness()
    elif args.check:
        # Hook compatibility fallback
        try:
            hook_data = json.load(sys.stdin)
            log_event("gate", hook_data, "hook_call")
        except:
            pass
        allow()
        return
    else:
        parser.print_help()
        sys.exit(1)

    if success:
        print(f"✅ {message}")
        sys.exit(0)
    else:
        print(f"❌ QUALITY GATE FAILED: {message}")
        print("\n💡 Fix the issue and re-run validation before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()
