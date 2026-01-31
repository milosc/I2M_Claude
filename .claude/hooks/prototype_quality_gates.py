#!/usr/bin/env python3
"""
Prototype Quality Gates - Checkpoint Validation

Validates prototype outputs against checkpoint requirements.
Mirrors the discovery_quality_gates.py pattern for consistency.

Usage:
    python3 prototype_quality_gates.py --validate-checkpoint <N> --dir <path>
    python3 prototype_quality_gates.py --validate-file <path>
    python3 prototype_quality_gates.py --list-checkpoints
    python3 prototype_quality_gates.py --validate-traceability --dir <path>
    python3 prototype_quality_gates.py --validate-screens --dir <path>
    python3 prototype_quality_gates.py --validate-screen-code --dir <path>

Feedback Validation Commands:
    python3 prototype_quality_gates.py --validate-feedback PF-<NNN> --dir <path>
    python3 prototype_quality_gates.py --validate-feedback-registry --dir <path>
    python3 prototype_quality_gates.py --list-feedback --dir <path>
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════
# ERROR GUIDANCE HELPERS (Phase 4.2 Enhancement)
# ═══════════════════════════════════════════════════════════════════

class ErrorGuidance:
    """Provides detailed, actionable error messages with fix instructions."""

    # Checkpoint-to-skill mapping for fix commands
    CHECKPOINT_TO_SKILL = {
        1: "Prototype_ValidateDiscovery",
        2: "Prototype_Requirements",
        3: "Prototype_DataModel",
        4: "Prototype_ApiContracts",
        5: "Prototype_TestData",
        6: "Prototype_DesignBrief",
        7: "Prototype_DesignTokens",
        8: "Prototype_Components",
        9: "Prototype_Screens",
        10: "Prototype_Interactions",
        11: "Prototype_BuildSequence",
        12: "Prototype_CodeGen",
        13: "Prototype_QA",
        14: "Prototype_UIAudit"
    }

    @staticmethod
    def file_not_found(file_path: str, checkpoint: int, base_path: Path) -> str:
        """Generate detailed guidance for missing files with auto-fix suggestions."""
        skill_name = ErrorGuidance.CHECKPOINT_TO_SKILL.get(checkpoint, "Unknown")

        # Detect file type and generate auto-fix
        auto_fix = None
        system_name = base_path.name.replace("Prototype_", "") if "Prototype_" in base_path.name else "System"

        if file_path == "_state/prototype_config.json":
            auto_fix = AutoFixGenerator.suggest_fix("config_missing", system_name=system_name, file_path=file_path)
        elif file_path == "_state/prototype_progress.json":
            auto_fix = AutoFixGenerator.suggest_fix("progress_missing", file_path=file_path)
        elif "requirements_registry.json" in file_path:
            auto_fix = AutoFixGenerator.suggest_fix("requirements_missing", file_path=file_path)
        elif "screen_registry.json" in file_path:
            auto_fix = AutoFixGenerator.suggest_fix("screen_registry_missing", file_path=file_path)
        elif file_path.endswith("DATA_MODEL.md"):
            auto_fix = AutoFixGenerator.suggest_fix("markdown_missing", file_path=file_path, doc_type="DATA_MODEL", system_name=system_name)
        elif "API_CONTRACTS" in file_path:
            auto_fix = AutoFixGenerator.suggest_fix("markdown_missing", file_path=file_path, doc_type="API_CONTRACTS", system_name=system_name)
        elif "COMPONENT_INDEX" in file_path or "component-index" in file_path:
            auto_fix = AutoFixGenerator.suggest_fix("markdown_missing", file_path=file_path, doc_type="COMPONENT_INDEX", system_name=system_name)
        elif "SCREEN_INDEX" in file_path or "screen-index" in file_path:
            auto_fix = AutoFixGenerator.suggest_fix("markdown_missing", file_path=file_path, doc_type="SCREEN_INDEX", system_name=system_name)

        base_message = f"""❌ {file_path} - File not found

   CAUSE: Required output file is missing

   IMPACT: Checkpoint {checkpoint} validation will fail

   FIX:
   1. Re-run the skill that generates this file:
      Skill({{"subagent_type": "{skill_name}"}})

   2. Or manually create the file:
      touch {base_path / file_path}

   3. Verify the file exists:
      ls -la {base_path / file_path}

   Expected location: {base_path / file_path}"""

        if auto_fix:
            base_message += f"""

   ──────────────────────────────────────────────────────────────
   ✨ AUTO-GENERATED FIX (Task 4.4)
   ──────────────────────────────────────────────────────────────

   QUICK FIX - Copy and paste this command:

   {auto_fix['command']}

   ──────────────────────────────────────────────────────────────
   OR - Create file with this content:
   ──────────────────────────────────────────────────────────────

{auto_fix['code']}

   ──────────────────────────────────────────────────────────────
   OR - Save and run this script:
   ──────────────────────────────────────────────────────────────

{auto_fix['script']}

   Save as: fix_{file_path.replace('/', '_').replace('.', '_')}.sh
   Run: bash fix_{file_path.replace('/', '_').replace('.', '_')}.sh
   ──────────────────────────────────────────────────────────────"""

        return base_message

    @staticmethod
    def folder_not_found(folder_path: str, checkpoint: int, base_path: Path) -> str:
        """Generate detailed guidance for missing folders with auto-fix suggestions."""
        skill_name = ErrorGuidance.CHECKPOINT_TO_SKILL.get(checkpoint, "Unknown")

        # Generate auto-fix for folder creation
        auto_fix = AutoFixGenerator.suggest_fix("folder_missing", file_path=str(base_path / folder_path))

        base_message = f"""❌ {folder_path}/ - Folder not found

   CAUSE: Required folder structure is missing

   IMPACT: Checkpoint {checkpoint} validation will fail

   FIX:
   1. Create the folder:
      mkdir -p {base_path / folder_path}

   2. Re-run the skill that populates this folder:
      Skill({{"subagent_type": "{skill_name}"}})

   3. Verify the folder exists:
      ls -la {base_path / folder_path}/

   Expected location: {base_path / folder_path}/"""

        if auto_fix:
            base_message += f"""

   ──────────────────────────────────────────────────────────────
   ✨ AUTO-GENERATED FIX (Task 4.4)
   ──────────────────────────────────────────────────────────────

   QUICK FIX - Copy and paste this command:

   {auto_fix['command']}

   ──────────────────────────────────────────────────────────────
   OR - Save and run this script:
   ──────────────────────────────────────────────────────────────

{auto_fix['script']}

   Save as: fix_create_folder_{folder_path.replace('/', '_')}.sh
   Run: bash fix_create_folder_{folder_path.replace('/', '_')}.sh
   ──────────────────────────────────────────────────────────────"""

        return base_message

    @staticmethod
    def missing_json_field(file_path: str, field: str, checkpoint: int) -> str:
        """Generate detailed guidance for missing JSON fields."""

        return f"""❌ {file_path} missing '{field}' field

   CAUSE: JSON file is missing required field

   IMPACT: Downstream processes expecting this field will fail

   FIX:
   1. Open the file:
      {file_path}

   2. Add the missing field to the JSON structure:
      {{
        ...existing fields...,
        "{field}": {{}}  // or [] if it's an array
      }}

   3. Validate JSON syntax:
      python3 -m json.tool {file_path} > /dev/null

   EXPECTED STRUCTURE:
   The file should contain at minimum:
   - "{field}": <value>

   Run validation again after fixing."""

    @staticmethod
    def missing_file_content(file_path: str, missing_content: str, checkpoint: int) -> str:
        """Generate detailed guidance for missing content."""

        return f"""❌ {file_path} missing required content: "{missing_content}"

   CAUSE: File exists but doesn't contain expected section/heading

   IMPACT: File may be incomplete or incorrectly structured

   FIX:
   1. Open the file:
      {file_path}

   2. Add the missing section:
      {missing_content}

   3. Verify the file follows the template structure

   EXPECTED CONTENT:
   The file should contain: "{missing_content}"

   Check the template in .claude/templates/ for the correct format."""

    @staticmethod
    def insufficient_folder_files(folder_path: str, actual: int, required: int, checkpoint: int) -> str:
        """Generate detailed guidance for folders with insufficient files."""

        return f"""❌ {folder_path}/ has {actual} files (minimum: {required})

   CAUSE: Folder contains fewer files than required

   IMPACT: May indicate incomplete generation or missing artifacts

   FIX:
   1. Check what's currently in the folder:
      ls -la {folder_path}/

   2. Re-run the skill that generates these files:
      Checkpoint {checkpoint} skill

   3. Verify required files are present

   EXPECTED: At least {required} files in {folder_path}/
   ACTUAL: {actual} files found

   Missing: {required - actual} file(s)"""

    @staticmethod
    def traceability_propagation_failure(source: str, target: str) -> str:
        """Generate detailed guidance for traceability propagation failures."""

        return f"""
═══════════════════════════════════════════════════════════════════
⚠️  TRACEABILITY PROPAGATION FAILURE (BLOCKING)
═══════════════════════════════════════════════════════════════════

   SOURCE: {source}
   TARGET: {target} (ROOT-level traceability)

   CAUSE: File not propagated to shared traceability/ folder

   IMPACT:
   - Downstream stages will fail (ProductSpecs, SolArch, Implementation)
   - Cross-stage traceability broken
   - Quality gates will BLOCK

   FIX:
   1. Verify source file exists:
      ls -la {source}

   2. Run traceability propagation:
      /traceability-init --repair

   3. Manually copy if needed:
      cp {source} {target}

   4. Verify propagation:
      ls -la {target}
      diff {source} {target}

   WHY THIS IS CRITICAL:
   The traceability/ folder is SHARED across all stages at the ROOT level.
   All registries must be propagated here for end-to-end traceability.

   See: CLAUDE.md section on "SHARED FOLDERS ARCHITECTURE"
═══════════════════════════════════════════════════════════════════"""


class AutoFixGenerator:
    """
    Generates automatic fix suggestions with actual code snippets.

    Phase 4 Task 4.4: Provides corrected code that can be directly used
    to fix common validation errors.
    """

    @staticmethod
    def generate_config_json_template(system_name: str) -> str:
        """Generate prototype_config.json template."""
        return f'''{{
  "system_name": "{system_name}",
  "stage": "prototype",
  "version": "1.0.0",
  "created_at": "{datetime.now().isoformat()}",
  "discovery_path": "../ClientAnalysis_{system_name}/",
  "output_path": "./",
  "settings": {{
    "skip_existing": false,
    "verbose": true
  }}
}}'''

    @staticmethod
    def generate_progress_json_template() -> str:
        """Generate prototype_progress.json template."""
        return '''{
  "checkpoint": 0,
  "current_phase": null,
  "started_at": "''' + datetime.now().isoformat() + '''",
  "updated_at": "''' + datetime.now().isoformat() + '''",
  "phases": {},
  "validation": {
    "status": "pending",
    "issues": []
  }
}'''

    @staticmethod
    def generate_requirements_registry_template() -> str:
        """Generate requirements_registry.json template."""
        return '''{
  "metadata": {
    "created_at": "''' + datetime.now().isoformat() + '''",
    "version": "1.0.0",
    "stage": "prototype",
    "source": "Discovery Phase"
  },
  "requirements": {},
  "hierarchy": {
    "pain_points": [],
    "jtbd": [],
    "user_stories": [],
    "functional_requirements": []
  },
  "traceability": {
    "pain_point_to_jtbd": {},
    "jtbd_to_requirements": {},
    "requirements_to_screens": {}
  }
}'''

    @staticmethod
    def generate_screen_registry_template() -> str:
        """Generate screen_registry.json template."""
        return '''{
  "metadata": {
    "created_at": "''' + datetime.now().isoformat() + '''",
    "version": "1.0.0",
    "stage": "prototype"
  },
  "discovery_screens": [],
  "screen_coverage": {
    "discovery_total": 0,
    "specs_generated": 0,
    "code_generated": 0,
    "spec_coverage_percent": 0,
    "code_coverage_percent": 0
  },
  "traceability": {}
}'''

    @staticmethod
    def generate_markdown_template(file_type: str, system_name: str = "") -> str:
        """Generate markdown file templates based on file type."""
        templates = {
            "DATA_MODEL": f'''# Data Model

**System**: {system_name}
**Version**: 1.0.0
**Generated**: {datetime.now().strftime("%Y-%m-%d")}

---

## Overview

This document defines the core data entities and their relationships for the {system_name} system.

## Entities

### Entity: [Name]

**Description**: [Purpose and role]

**Attributes**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | Yes | Unique identifier |

---

## Relationships

### [Entity A] → [Entity B]

- **Type**: One-to-Many
- **Description**: [Relationship description]

---

## Validation Rules

### [Entity Name]

- [Validation rule 1]
- [Validation rule 2]

---

*Generated by Prototype_DataModel skill*
''',
            "API_CONTRACTS": f'''# API Contracts

**System**: {system_name}
**Version**: 1.0.0
**Generated**: {datetime.now().strftime("%Y-%m-%d")}

---

## Overview

This document defines the API endpoints and contracts for the {system_name} system.

## Endpoints

### GET /api/[resource]

**Description**: [Endpoint purpose]

**Request**:
```json
{{
  "param": "value"
}}
```

**Response**:
```json
{{
  "data": []
}}
```

---

*Generated by Prototype_ApiContracts skill*
''',
            "COMPONENT_INDEX": f'''# Component Library Index

**System**: {system_name}
**Version**: 1.0.0
**Generated**: {datetime.now().strftime("%Y-%m-%d")}

---

## Overview

This document catalogs all UI components used in the {system_name} prototype.

## Component Categories

### Primitives

| Component | Description | File |
|-----------|-------------|------|
| Button | Primary action button | primitives/Button.tsx |

### Data Display

| Component | Description | File |
|-----------|-------------|------|
| Table | Data table with sorting | data-display/Table.tsx |

---

*Generated by Prototype_Components skill*
''',
            "SCREEN_INDEX": f'''# Screen Index

**System**: {system_name}
**Version**: 1.0.0
**Generated**: {datetime.now().strftime("%Y-%m-%d")}

---

## Overview

This document indexes all screens in the {system_name} prototype.

## Screens

### [App/Portal Name]

| Screen ID | Name | Route | Priority |
|-----------|------|-------|----------|
| S-1.1 | [Screen Name] | /path | P0 |

---

*Generated by Prototype_Screens skill*
'''
        }

        return templates.get(file_type, f'''# {file_type}

**Generated**: {datetime.now().strftime("%Y-%m-%d")}

---

## Overview

[Document purpose]

---

*Template generated automatically*
''')

    @staticmethod
    def generate_fix_script(error_type: str, file_path: str, **kwargs) -> str:
        """Generate a shell script to fix the error."""
        scripts = {
            "missing_file": f'''#!/bin/bash
# Auto-generated fix script for missing file

FILE_PATH="{file_path}"
echo "Creating missing file: $FILE_PATH"
mkdir -p "$(dirname "$FILE_PATH")"
cat > "$FILE_PATH" << 'EOF'
{kwargs.get('content', '# File created by auto-fix')}
EOF
echo "✅ File created: $FILE_PATH"
ls -la "$FILE_PATH"
''',
            "missing_folder": f'''#!/bin/bash
# Auto-generated fix script for missing folder

FOLDER_PATH="{file_path}"
echo "Creating missing folder: $FOLDER_PATH"
mkdir -p "$FOLDER_PATH"
echo "✅ Folder created: $FOLDER_PATH"
ls -la "$FOLDER_PATH/"
''',
            "invalid_json": f'''#!/bin/bash
# Auto-generated fix script for invalid JSON

FILE_PATH="{file_path}"
echo "Fixing invalid JSON in: $FILE_PATH"
# Backup original
cp "$FILE_PATH" "$FILE_PATH.backup"
# Validate and format
python3 -m json.tool "$FILE_PATH" > "$FILE_PATH.tmp" && mv "$FILE_PATH.tmp" "$FILE_PATH"
echo "✅ JSON formatted: $FILE_PATH"
python3 -m json.tool "$FILE_PATH" > /dev/null && echo "✅ JSON is valid"
'''
        }

        return scripts.get(error_type, f'''#!/bin/bash
# Fix script for {error_type}
echo "Manual intervention required for: {file_path}"
''')

    @staticmethod
    def suggest_fix(error_type: str, **kwargs) -> Dict[str, str]:
        """
        Generate comprehensive fix suggestion with multiple formats.

        Returns:
            Dictionary with 'instruction', 'code', 'script', and 'command' keys
        """
        system_name = kwargs.get('system_name', 'UnknownSystem')
        file_path = kwargs.get('file_path', '')
        checkpoint = kwargs.get('checkpoint', 0)

        fixes = {
            "config_missing": {
                "instruction": f"Create prototype_config.json with system configuration",
                "code": AutoFixGenerator.generate_config_json_template(system_name),
                "command": f"cat > _state/prototype_config.json << 'EOF'\n{AutoFixGenerator.generate_config_json_template(system_name)}\nEOF",
                "script": AutoFixGenerator.generate_fix_script(
                    "missing_file",
                    "_state/prototype_config.json",
                    content=AutoFixGenerator.generate_config_json_template(system_name)
                )
            },
            "progress_missing": {
                "instruction": f"Create prototype_progress.json to track checkpoint progress",
                "code": AutoFixGenerator.generate_progress_json_template(),
                "command": f"cat > _state/prototype_progress.json << 'EOF'\n{AutoFixGenerator.generate_progress_json_template()}\nEOF",
                "script": AutoFixGenerator.generate_fix_script(
                    "missing_file",
                    "_state/prototype_progress.json",
                    content=AutoFixGenerator.generate_progress_json_template()
                )
            },
            "requirements_missing": {
                "instruction": f"Create requirements_registry.json with hierarchical requirements",
                "code": AutoFixGenerator.generate_requirements_registry_template(),
                "command": f"cat > traceability/requirements_registry.json << 'EOF'\n{AutoFixGenerator.generate_requirements_registry_template()}\nEOF",
                "script": AutoFixGenerator.generate_fix_script(
                    "missing_file",
                    "traceability/requirements_registry.json",
                    content=AutoFixGenerator.generate_requirements_registry_template()
                )
            },
            "screen_registry_missing": {
                "instruction": f"Create screen_registry.json to track Discovery screen implementation",
                "code": AutoFixGenerator.generate_screen_registry_template(),
                "command": f"cat > traceability/screen_registry.json << 'EOF'\n{AutoFixGenerator.generate_screen_registry_template()}\nEOF",
                "script": AutoFixGenerator.generate_fix_script(
                    "missing_file",
                    "traceability/screen_registry.json",
                    content=AutoFixGenerator.generate_screen_registry_template()
                )
            },
            "markdown_missing": {
                "instruction": f"Create {file_path} with template structure",
                "code": AutoFixGenerator.generate_markdown_template(
                    kwargs.get('doc_type', 'GENERIC'),
                    system_name
                ),
                "command": f"cat > {file_path} << 'EOF'\n{AutoFixGenerator.generate_markdown_template(kwargs.get('doc_type', 'GENERIC'), system_name)}\nEOF",
                "script": AutoFixGenerator.generate_fix_script(
                    "missing_file",
                    file_path,
                    content=AutoFixGenerator.generate_markdown_template(
                        kwargs.get('doc_type', 'GENERIC'),
                        system_name
                    )
                )
            },
            "folder_missing": {
                "instruction": f"Create missing folder: {file_path}",
                "code": f"# Create folder structure\nmkdir -p {file_path}",
                "command": f"mkdir -p {file_path}",
                "script": AutoFixGenerator.generate_fix_script("missing_folder", file_path)
            }
        }

        return fixes.get(error_type, {
            "instruction": f"Manual fix required for {error_type}",
            "code": f"# No automatic fix available for {error_type}",
            "command": f"# Manual intervention needed",
            "script": f"# Manual fix required"
        })


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
    # Checkpoint 3 - Data Model (UI-dependent)
    "data-model": ["00-foundation/data-model/DATA_MODEL_SUMMARY.md", "00-foundation/data-model/relationships.md"],
    # Checkpoint 4 - API Contracts (UI-dependent for prototypes)
    "api-contracts": ["00-foundation/api-contracts/API_CONTRACTS_SUMMARY.md", "00-foundation/api-contracts/openapi.json"],
    # Checkpoint 5 - Test Data
    "test-data": ["00-foundation/test-data/TESTDATA_GENERATION_SUMMARY.md", "00-foundation/test-data/DATASET_CATALOG.md"],
    # Checkpoint 6 - Design Brief (UI-dependent)
    "design-brief": ["00-foundation/design-brief.md"],
    # Checkpoint 7 - Design Tokens (UI-dependent)
    "design-tokens": ["00-foundation/design-tokens.json", "00-foundation/color-system.md", "00-foundation/typography.md"],
    # Checkpoint 8 - Components (UI-dependent)
    "ui-components": ["01-components/component-index.md"],
    "component-specs": ["01-components/component-index.md"],
    # Checkpoint 9 - Screens (UI-dependent)
    "screen-definitions": ["02-screens/screen-index.md"],
    "screens": ["02-screens/screen-index.md"],
    # Checkpoint 10 - Interactions (UI-dependent)
    "interaction-patterns": ["03-interactions/motion-system.md", "03-interactions/accessibility-spec.md"],
    # Checkpoint 11-12 - Build (UI-dependent)
    "prototype-code": ["04-implementation/build-sequence.md", "prototype/src/App.tsx"],
}


def get_root_path(prototype_path: Path) -> Path:
    """
    Get the project root path where shared _state/ folder lives.

    The _state/ folder is SHARED between Discovery and Prototype phases
    and lives at the project root level, NOT inside Prototype_<SystemName>/.

    Structure:
        /project_root/
        ├── _state/                          <- SHARED state folder
        ├── traceability/                    <- SHARED traceability
        ├── ClientAnalysis_<SystemName>/     <- Discovery outputs
        └── Prototype_<SystemName>/          <- Prototype outputs
    """
    # If the path is Prototype_<SystemName>/, go up one level
    # The shared _state/ is at the parent (project root) level
    if prototype_path.name.startswith("Prototype_"):
        return prototype_path.parent
    # If already at root (e.g., running from project root), return as-is
    return prototype_path


def get_state_path(prototype_path: Path) -> Path:
    """Get the shared _state/ folder path (at project root level)."""
    return get_root_path(prototype_path) / "_state"


def get_traceability_path(prototype_path: Path) -> Path:
    """Get the shared traceability/ folder path (at project root level)."""
    return get_root_path(prototype_path) / "traceability"


def get_discovery_path(prototype_path: Path) -> Optional[Path]:
    """
    Get the corresponding ClientAnalysis folder for this prototype.

    Assumes naming convention: Prototype_<SystemName> -> ClientAnalysis_<SystemName>
    """
    if prototype_path.name.startswith("Prototype_"):
        system_name = prototype_path.name.replace("Prototype_", "")
        discovery_path = prototype_path.parent / f"ClientAnalysis_{system_name}"
        if discovery_path.exists():
            return discovery_path
    return None


# Checkpoint requirements mapping
# NOTE: Paths starting with "_state/" are ROOT-RELATIVE (shared folder)
#       All other paths are PROTOTYPE-RELATIVE
CHECKPOINT_REQUIREMENTS = {
    0: {
        "name": "Initialize",
        "description": "Folder structure and state files created (nested structure)",
        "required_files": [
            "_state/prototype_config.json",
            "_state/prototype_progress.json",
            "_state/FAILURES_LOG.md"
        ],
        "required_folders": [
            "_state",
            # Foundation with nested structure
            "00-foundation",
            "00-foundation/data-model",
            "00-foundation/data-model/entities",
            "00-foundation/data-model/dictionaries",
            "00-foundation/data-model/constraints",
            "00-foundation/api-contracts",
            "00-foundation/api-contracts/endpoints",
            "00-foundation/api-contracts/examples",
            "00-foundation/api-contracts/mocks",
            "00-foundation/test-data",
            "00-foundation/test-data/datasets",
            "00-foundation/test-data/datasets/catalog",
            "00-foundation/test-data/datasets/core",
            "00-foundation/test-data/datasets/junction",
            "00-foundation/test-data/datasets/transactional",
            "00-foundation/test-data/datasets/personas",
            "00-foundation/test-data/datasets/scenarios",
            "00-foundation/test-data/datasets/combined",
            "00-foundation/test-data/personas",
            # Components
            "01-components",
            "01-components/primitives",
            "01-components/data-display",
            "01-components/feedback",
            "01-components/navigation",
            "01-components/overlays",
            "01-components/patterns",
            # Screens
            "02-screens",
            # Interactions
            "03-interactions",
            # Implementation with phases/checkpoints/prompts
            "04-implementation",
            "04-implementation/sequence",
            "04-implementation/checkpoints",
            "04-implementation/prompts",
            # Validation
            "05-validation",
            "05-validation/screenshots",
            "05-validation/accessibility",
            # Change requests
            "06-change-requests",
            # Prototype code
            "prototype",
            "prototype/src",
            "prototype/public",
            # Reports
            "reports"
        ]
    },
    1: {
        "name": "Validate Discovery",
        "description": "Discovery outputs validated and summarized",
        "required_files": [
            "_state/discovery_summary.json"
        ],
        "json_validation": {
            "file": "_state/discovery_summary.json",
            "required_fields": ["personas", "pain_points", "screens"]
        }
    },
    2: {
        "name": "Extract Requirements",
        "description": "Requirements extracted with traceability and propagated to ROOT",
        "required_files": [
            "_state/requirements_registry.json",
            "traceability/requirements_registry.json"  # CRITICAL: Must propagate to ROOT
        ],
        "json_validation": {
            "file": "_state/requirements_registry.json",
            "required_fields": ["requirements", "statistics"],
            "array_min_items": {"requirements": 1}
        },
        # NEW: Validate ROOT-level propagation
        "traceability_propagation": {
            "source": "_state/requirements_registry.json",
            "target": "traceability/requirements_registry.json",
            "required_fields": ["items", "traceability_chain"],
            "must_sync": True
        }
    },
    3: {
        "name": "Data Model",
        "description": "Entity schemas and relationships defined (nested structure)",
        "required_files": [
            "00-foundation/data-model/DATA_MODEL_SUMMARY.md",
            "00-foundation/data-model/relationships.md"
        ],
        "required_folders": [
            "00-foundation/data-model/entities",
            "00-foundation/data-model/dictionaries",
            "00-foundation/data-model/constraints"
        ],
        "file_content_check": {
            "file": "00-foundation/data-model/DATA_MODEL_SUMMARY.md",
            "must_contain": ["# Data Model Summary", "## Overview", "## Entity Inventory"]
        },
        "folder_min_files": {
            "00-foundation/data-model/entities": 2
        }
    },
    4: {
        "name": "API Contracts",
        "description": "API endpoint specifications created (nested structure)",
        "required_files": [
            "00-foundation/api-contracts/API_CONTRACTS_SUMMARY.md",
            "00-foundation/api-contracts/openapi.json"
        ],
        "required_folders": [
            "00-foundation/api-contracts/endpoints",
            "00-foundation/api-contracts/examples"
        ],
        "json_validation": {
            "file": "00-foundation/api-contracts/openapi.json",
            "required_fields": ["paths"]
        },
        "file_content_check": {
            "file": "00-foundation/api-contracts/API_CONTRACTS_SUMMARY.md",
            "must_contain": ["# API Contracts Summary", "## Endpoint Inventory"]
        }
    },
    5: {
        "name": "Test Data",
        "description": "Test data files generated (organized datasets)",
        "required_files": [
            "00-foundation/test-data/TEST_DATA_SUMMARY.md"
        ],
        "required_folders": [
            "00-foundation/test-data/datasets/catalog",
            "00-foundation/test-data/datasets/core",
            "00-foundation/test-data/datasets/transactional",
            "00-foundation/test-data/datasets/scenarios"
        ],
        "file_content_check": {
            "file": "00-foundation/test-data/TEST_DATA_SUMMARY.md",
            "must_contain": ["# Test Data Summary", "## Dataset Inventory", "## Persona Scenarios"]
        },
        "folder_min_files": {
            "00-foundation/test-data/datasets/core": 1,
            "00-foundation/test-data/datasets/catalog": 1
        }
    },
    6: {
        "name": "Design Brief",
        "description": "Visual direction and principles defined",
        "required_files": [
            "00-foundation/design-brief.md",
            "00-foundation/design-principles.md"
        ]
    },
    7: {
        "name": "Design Tokens",
        "description": "Design token system created",
        "required_files": [
            "00-foundation/design-tokens.json",
            "00-foundation/color-system.md",
            "00-foundation/typography.md",
            "00-foundation/spacing-layout.md"
        ],
        "json_validation": {
            "file": "00-foundation/design-tokens.json",
            "required_fields": ["color", "typography", "spacing"]
        }
    },
    8: {
        "name": "Components",
        "description": "Component library specifications created with summaries",
        "required_files": [
            "01-components/component-index.md",
            "01-components/COMPONENT_LIBRARY_SUMMARY.md"
        ],
        "required_folders": [
            "01-components/primitives",
            "01-components/data-display",
            "01-components/feedback",
            "01-components/navigation",
            "01-components/overlays",
            "01-components/patterns"
        ],
        "folder_min_files": {
            "01-components/primitives": 3,
            "01-components/data-display": 2,
            "01-components/feedback": 2,
            "01-components/navigation": 2
        },
        "file_content_check": {
            "file": "01-components/COMPONENT_LIBRARY_SUMMARY.md",
            "must_contain": ["# Component Library Summary", "## Overview", "## Requirements Coverage"]
        }
    },
    9: {
        "name": "Screens",
        "description": "Screen specifications created for ALL Discovery screens with summaries",
        "required_files": [
            "02-screens/screen-index.md",
            "02-screens/SCREEN_SPECIFICATIONS_SUMMARY.md"
        ],
        "folder_min_folders": {
            "02-screens": 1  # At least one screen folder
        },
        "file_content_check": {
            "file": "02-screens/SCREEN_SPECIFICATIONS_SUMMARY.md",
            "must_contain": ["# Screen Specifications Summary", "## Overview", "## Screen Inventory"]
        },
        # NEW: Screen count validation - ensures ALL Discovery screens have specs
        "screen_validation": {
            "source": "traceability/screen_registry.json",
            "check_type": "all_screens_have_specs"
        }
    },
    10: {
        "name": "Interactions",
        "description": "Motion, accessibility, and responsive specs created",
        "required_files": [
            "03-interactions/motion-system.md",
            "03-interactions/accessibility-spec.md",
            "03-interactions/responsive-behavior.md"
        ],
        "file_content_check": {
            "file": "03-interactions/accessibility-spec.md",
            "must_contain": ["WCAG"]
        }
    },
    11: {
        "name": "Build Sequence",
        "description": "Implementation order with phases, checkpoints, and prompts",
        "required_files": [
            "04-implementation/build-sequence.md"
        ],
        "required_folders": [
            "04-implementation/sequence",
            "04-implementation/checkpoints",
            "04-implementation/prompts"
        ],
        "file_content_check": {
            "file": "04-implementation/build-sequence.md",
            "must_contain": ["# Build Sequence", "## Build Order", "## Phase Sequences", "## Checkpoints"]
        },
        "folder_min_files": {
            "04-implementation/sequence": 3,
            "04-implementation/checkpoints": 2,
            "04-implementation/prompts": 3
        }
    },
    12: {
        "name": "Code Generation",
        "description": "Working prototype code generated for ALL screen specs",
        "required_files": [
            "prototype/package.json"
        ],
        "required_folders": [
            "prototype/src"
        ],
        "json_validation": {
            "file": "prototype/package.json",
            "required_fields": ["name", "dependencies"]
        },
        # NEW: Screen code validation - ensures ALL screen specs have React components
        "screen_code_validation": {
            "source": "traceability/screen_registry.json",
            "check_type": "all_specs_have_code"
        }
    },
    13: {
        "name": "QA Testing",
        "description": "QA testing completed",
        "required_files": [
            "05-validation/qa-report.md"
        ],
        "file_content_check": {
            "file": "05-validation/qa-report.md",
            "must_contain": ["# QA Report", "## Test Results"]
        }
    },
    14: {
        "name": "UI Audit",
        "description": "Visual audit, final reports, and traceability matrix generated",
        "required_files": [
            "05-validation/ui-audit-report.md",
            "reports/ARCHITECTURE.md",
            "reports/README.md",
            "reports/TRACEABILITY_MATRIX.md"
        ],
        "required_folders": [
            "05-validation/screenshots",
            "05-validation/accessibility"
        ],
        "file_content_check": {
            "file": "reports/TRACEABILITY_MATRIX.md",
            "must_contain": ["# Traceability Matrix", "## Pain Point", "## Screen-to-Requirement Mapping", "## Coverage Summary"]
        }
    }
}


def resolve_path(base_path: Path, relative_path: str) -> Path:
    """
    Resolve a relative path to its full path.

    - Paths starting with "_state/" resolve to the ROOT _state/ folder
    - Paths starting with "traceability/" resolve to the ROOT traceability/ folder
    - All other paths resolve relative to the Prototype folder
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
        # All other paths are relative to the Prototype folder
        return base_path / relative_path


def validate_file_exists(base_path: Path, file_path: str, artifact_name: Optional[str] = None, checkpoint: int = 0) -> Tuple[bool, str]:
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

    # ENHANCED: Use detailed error guidance (Phase 4.2)
    return False, ErrorGuidance.file_not_found(file_path, checkpoint, base_path)


def validate_folder_exists(base_path: Path, folder_path: str, checkpoint: int = 0) -> Tuple[bool, str]:
    """Check if a folder exists."""
    full_path = resolve_path(base_path, folder_path)
    if full_path.exists() and full_path.is_dir():
        return True, f"✅ {folder_path}/"

    # ENHANCED: Use detailed error guidance (Phase 4.2)
    return False, ErrorGuidance.folder_not_found(folder_path, checkpoint, base_path)


def validate_json_file(base_path: Path, config: Dict, checkpoint: int = 0) -> Tuple[bool, List[str]]:
    """Validate JSON file structure."""
    results = []
    file_path = resolve_path(base_path, config["file"])

    if not file_path.exists():
        # ENHANCED: Use detailed error guidance (Phase 4.2)
        return False, [ErrorGuidance.file_not_found(config["file"], checkpoint, base_path)]

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Check required fields
        if "required_fields" in config:
            for field in config["required_fields"]:
                if field in data:
                    results.append(f"✅ {config['file']} has '{field}' field")
                else:
                    # ENHANCED: Use detailed error guidance (Phase 4.2)
                    error_msg = ErrorGuidance.missing_json_field(config['file'], field, checkpoint)
                    results.append(error_msg)
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


def validate_file_content(base_path: Path, config: Dict, checkpoint: int = 0) -> Tuple[bool, List[str]]:
    """Validate file contains required content."""
    results = []
    file_path = resolve_path(base_path, config["file"])

    if not file_path.exists():
        # ENHANCED: Use detailed error guidance (Phase 4.2)
        return False, [ErrorGuidance.file_not_found(config["file"], checkpoint, base_path)]

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        for text in config.get("must_contain", []):
            if text in content:
                results.append(f"✅ {config['file']} contains '{text}'")
            else:
                # ENHANCED: Use detailed error guidance (Phase 4.2)
                error_msg = ErrorGuidance.missing_file_content(config['file'], text, checkpoint)
                results.append(error_msg)
                return False, results

        return True, results

    except Exception as e:
        return False, [f"❌ {config['file']} - Error reading: {e}"]


def validate_folder_min_files(base_path: Path, config: Dict, checkpoint: int = 0) -> Tuple[bool, List[str]]:
    """Validate folder contains minimum number of files."""
    results = []

    for folder, min_count in config.items():
        folder_path = resolve_path(base_path, folder)
        if not folder_path.exists():
            # ENHANCED: Use detailed error guidance (Phase 4.2)
            error_msg = ErrorGuidance.folder_not_found(folder, checkpoint, base_path)
            results.append(error_msg)
            return False, results

        files = [f for f in folder_path.iterdir() if f.is_file()]
        if len(files) >= min_count:
            results.append(f"✅ {folder}/ has {len(files)} files (min: {min_count})")
        else:
            # ENHANCED: Use detailed error guidance (Phase 4.2)
            error_msg = ErrorGuidance.insufficient_folder_files(folder, len(files), min_count, checkpoint)
            results.append(error_msg)
            return False, results

    return True, results


def validate_folder_min_folders(base_path: Path, config: Dict, checkpoint: int = 0) -> Tuple[bool, List[str]]:
    """Validate folder contains minimum number of subfolders."""
    results = []

    for folder, min_count in config.items():
        folder_path = resolve_path(base_path, folder)
        if not folder_path.exists():
            # ENHANCED: Use detailed error guidance (Phase 4.2)
            error_msg = ErrorGuidance.folder_not_found(folder, checkpoint, base_path)
            results.append(error_msg)
            return False, results

        # Exclude index files from folder count
        subfolders = [f for f in folder_path.iterdir() if f.is_dir()]
        if len(subfolders) >= min_count:
            results.append(f"✅ {folder}/ has {len(subfolders)} subfolders (min: {min_count})")
        else:
            # Use insufficient_folder_files helper (applies to subfolders too)
            error_msg = ErrorGuidance.insufficient_folder_files(folder, len(subfolders), min_count, checkpoint)
            # Customize message to say "subfolders" instead of "files"
            error_msg = error_msg.replace("files", "subfolders")
            results.append(error_msg)
            return False, results

    return True, results


def validate_traceability_propagation(base_path: Path, config: Dict) -> Tuple[bool, List[str]]:
    """
    Validate that a registry file has been properly propagated from _state/ to traceability/.

    This is CRITICAL for ensuring the traceability chain is complete.
    If propagation fails, downstream stages will have broken references.
    """
    results = []
    source_path = resolve_path(base_path, config["source"])
    target_path = resolve_path(base_path, config["target"])

    # Check source exists
    if not source_path.exists():
        results.append(f"❌ SOURCE MISSING: {config['source']}")
        results.append(f"   The skill that creates this file did not run successfully")
        return False, results

    # Check target exists (ROOT-level traceability)
    if not target_path.exists():
        # ENHANCED: Use detailed error guidance (Phase 4.2)
        error_msg = ErrorGuidance.traceability_propagation_failure(config['source'], config['target'])
        results.append(error_msg)
        return False, results

    results.append(f"✅ {config['source']} → {config['target']} propagation exists")

    # Validate target has required fields
    if "required_fields" in config:
        try:
            with open(target_path, 'r') as f:
                data = json.load(f)

            missing_fields = []
            for field in config["required_fields"]:
                if field not in data:
                    missing_fields.append(field)

            if missing_fields:
                results.append(f"❌ {config['target']} missing required fields: {missing_fields}")
                return False, results
            else:
                results.append(f"✅ {config['target']} has all required fields")

        except json.JSONDecodeError as e:
            results.append(f"❌ {config['target']} is not valid JSON: {e}")
            return False, results
        except Exception as e:
            results.append(f"❌ Error reading {config['target']}: {e}")
            return False, results

    # Optional: Check sync between source and target
    if config.get("must_sync", False):
        try:
            with open(source_path, 'r') as f:
                source_data = json.load(f)
            with open(target_path, 'r') as f:
                target_data = json.load(f)

            # Compare key metrics
            source_count = len(source_data.get("requirements", source_data.get("items", [])))
            target_count = len(target_data.get("items", []))

            if source_count > 0 and target_count == 0:
                results.append(f"⚠️  SOURCE has {source_count} items but TARGET has 0 - possible sync issue")
            else:
                results.append(f"✅ Sync check: source={source_count}, target={target_count} items")

        except Exception as e:
            results.append(f"⚠️  Could not verify sync: {e}")

    return True, results


def validate_checkpoint(checkpoint: int, dir_path: str) -> Dict:
    """Validate a specific checkpoint."""
    if checkpoint not in CHECKPOINT_REQUIREMENTS:
        return {
            "success": False,
            "checkpoint": checkpoint,
            "error": f"Invalid checkpoint: {checkpoint}. Valid range: 0-14"
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
            # ENHANCED: Pass checkpoint for detailed error guidance (Phase 4.2)
            passed, message = validate_file_exists(base_path, file_path, checkpoint=checkpoint)
            results["validations"].append(message)
            if not passed:
                results["success"] = False

    # Validate required folders
    if "required_folders" in req:
        for folder_path in req["required_folders"]:
            # ENHANCED: Pass checkpoint for detailed error guidance (Phase 4.2)
            passed, message = validate_folder_exists(base_path, folder_path, checkpoint=checkpoint)
            results["validations"].append(message)
            if not passed:
                results["success"] = False

    # Validate JSON structure
    if "json_validation" in req:
        # ENHANCED: Pass checkpoint for detailed error guidance (Phase 4.2)
        passed, messages = validate_json_file(base_path, req["json_validation"], checkpoint=checkpoint)
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False

    # Validate file content
    if "file_content_check" in req:
        # ENHANCED: Pass checkpoint for detailed error guidance (Phase 4.2)
        passed, messages = validate_file_content(base_path, req["file_content_check"], checkpoint=checkpoint)
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False

    # Validate folder minimum files
    if "folder_min_files" in req:
        # ENHANCED: Pass checkpoint for detailed error guidance (Phase 4.2)
        passed, messages = validate_folder_min_files(base_path, req["folder_min_files"], checkpoint=checkpoint)
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False

    # Validate folder minimum subfolders
    if "folder_min_folders" in req:
        # ENHANCED: Pass checkpoint for detailed error guidance (Phase 4.2)
        passed, messages = validate_folder_min_folders(base_path, req["folder_min_folders"], checkpoint=checkpoint)
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False

    # CRITICAL: Validate traceability propagation (Checkpoint 2)
    # This ensures _state/ files are propagated to ROOT traceability/
    if "traceability_propagation" in req:
        passed, messages = validate_traceability_propagation(base_path, req["traceability_propagation"])
        results["validations"].extend(messages)
        if not passed:
            results["success"] = False
            # Add prominent error message for propagation failures
            results["validations"].append("")
            results["validations"].append("═" * 60)
            results["validations"].append("⚠️  TRACEABILITY PROPAGATION FAILURE")
            results["validations"].append("   This is a BLOCKING error. Downstream stages will fail.")
            results["validations"].append("   Run: /traceability-init --repair")
            results["validations"].append("═" * 60)

    # NEW: Validate screen specs coverage (Checkpoint 9)
    if "screen_validation" in req:
        config = req["screen_validation"]
        if config.get("check_type") == "all_screens_have_specs":
            passed, messages = validate_all_screens_have_specs(base_path)
            results["validations"].extend(messages)
            if not passed:
                results["success"] = False

    # NEW: Validate screen code coverage (Checkpoint 12)
    if "screen_code_validation" in req:
        config = req["screen_code_validation"]
        if config.get("check_type") == "all_specs_have_code":
            passed, messages = validate_all_specs_have_code(base_path)
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
            if "requirements_registry" in path.name:
                if "requirements" not in data:
                    results["success"] = False
                    results["validations"].append("❌ Missing 'requirements' field")
            elif "discovery_summary" in path.name:
                for field in ["personas", "pain_points", "screens"]:
                    if field not in data:
                        results["success"] = False
                        results["validations"].append(f"❌ Missing '{field}' field")
            elif "design-tokens" in path.name:
                for field in ["color", "typography", "spacing"]:
                    if field not in data:
                        results["success"] = False
                        results["validations"].append(f"❌ Missing '{field}' field")

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

        except Exception as e:
            results["success"] = False
            results["validations"].append(f"❌ Error reading file: {e}")

    return results


def extract_discovery_screens(discovery_path: Path) -> List[Dict]:
    """Extract screen definitions from Discovery screen-definitions.md."""
    screens = []
    screen_def_path = discovery_path / "04-design-specs" / "screen-definitions.md"

    if not screen_def_path.exists():
        return screens

    try:
        with open(screen_def_path, 'r') as f:
            content = f.read()

        # Parse screen table rows - look for | ID | Name | Priority | pattern
        # Pattern matches: | M-01 | Task Execution | P0 |... or | D-01 | Dashboard | P0 |...
        screen_pattern = r'\|\s*(M-\d+|D-\d+)\s*\|\s*([^|]+)\s*\|\s*(P[012])\s*\|'
        matches = re.findall(screen_pattern, content)

        for match in matches:
            screen_id, name, priority = match
            screens.append({
                "id": screen_id.strip(),
                "name": name.strip(),
                "priority": priority.strip(),
                "source": "discovery"
            })

        return screens
    except Exception as e:
        print(f"⚠️ Error extracting Discovery screens: {e}")
        return screens


def validate_screen_registry(base_path: Path) -> Dict:
    """Validate screen_registry.json exists and has required structure."""
    # screen_registry.json is in the SHARED traceability/ folder at project root
    registry_path = get_traceability_path(base_path) / "screen_registry.json"

    if not registry_path.exists():
        return {
            "success": False,
            "error": "screen_registry.json not found. Run Prototype_ValidateDiscovery first."
        }

    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)

        required_fields = ["discovery_screens", "screen_coverage", "traceability"]
        missing_fields = [f for f in required_fields if f not in registry]

        if missing_fields:
            return {
                "success": False,
                "error": f"screen_registry.json missing fields: {missing_fields}"
            }

        return {
            "success": True,
            "registry": registry
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Invalid JSON in screen_registry.json: {e}"
        }


def validate_all_screens_have_specs(base_path: Path) -> Tuple[bool, List[str]]:
    """Validate that ALL Discovery screens have spec folders in 02-screens/."""
    results = []

    # Load screen registry
    registry_result = validate_screen_registry(base_path)
    if not registry_result["success"]:
        return False, [f"❌ {registry_result['error']}"]

    registry = registry_result["registry"]
    discovery_screens = registry.get("discovery_screens", [])

    if not discovery_screens:
        return False, ["❌ No Discovery screens found in registry"]

    # Check each screen has a spec folder
    screens_path = base_path / "02-screens"
    missing_specs = []
    found_specs = []

    for screen in discovery_screens:
        screen_id = screen["id"]
        screen_name = screen.get("name", screen_id)

        # Look for spec folder - could be in mobile/ or desktop/ subfolder
        spec_found = False
        for subdir in ["", "mobile", "desktop"]:
            check_path = screens_path / subdir if subdir else screens_path
            if check_path.exists():
                for folder in check_path.iterdir():
                    if folder.is_dir():
                        # Check if folder contains spec file mentioning this screen ID
                        for md_file in folder.glob("*.md"):
                            try:
                                content = md_file.read_text()
                                if screen_id in content:
                                    spec_found = True
                                    found_specs.append(screen_id)
                                    break
                            except:
                                pass
                    if spec_found:
                        break
            if spec_found:
                break

        if not spec_found:
            missing_specs.append(f"{screen_id}: {screen_name}")

    # Update registry with spec status
    registry["screen_coverage"]["specs_generated"] = len(found_specs)
    registry["screen_coverage"]["specs_missing"] = len(missing_specs)

    # Calculate coverage
    total = len(discovery_screens)
    coverage = (len(found_specs) / total * 100) if total > 0 else 0
    registry["screen_coverage"]["spec_coverage_percent"] = round(coverage, 1)

    # Write updated registry to SHARED traceability/ at project root
    registry_path = get_traceability_path(base_path) / "screen_registry.json"
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)

    # Generate results
    results.append(f"✅ Screen registry loaded: {total} Discovery screens")
    results.append(f"📊 Spec coverage: {len(found_specs)}/{total} ({coverage:.1f}%)")

    if missing_specs:
        results.append(f"❌ Missing screen specs ({len(missing_specs)}):")
        for spec in missing_specs:
            results.append(f"   • {spec}")
        return False, results

    results.append("✅ All Discovery screens have specifications")
    return True, results


def validate_all_specs_have_code(base_path: Path) -> Tuple[bool, List[str]]:
    """Validate that ALL screen specs have React component code."""
    results = []

    # Load screen registry
    registry_result = validate_screen_registry(base_path)
    if not registry_result["success"]:
        return False, [f"❌ {registry_result['error']}"]

    registry = registry_result["registry"]
    discovery_screens = registry.get("discovery_screens", [])

    if not discovery_screens:
        return False, ["❌ No Discovery screens found in registry"]

    # Check for React component files
    prototype_src = base_path / "prototype" / "src"
    screens_dirs = [
        prototype_src / "screens",
        prototype_src / "pages",
        prototype_src / "views"
    ]

    # Find all .tsx/.jsx files that could be screen components
    code_files = []
    for screens_dir in screens_dirs:
        if screens_dir.exists():
            code_files.extend(screens_dir.glob("**/*.tsx"))
            code_files.extend(screens_dir.glob("**/*.jsx"))

    # Map screens to code files
    missing_code = []
    found_code = []
    screen_to_code = {}

    for screen in discovery_screens:
        screen_id = screen["id"]
        screen_name = screen.get("name", screen_id)
        code_found = False

        # Look for code file that references this screen
        for code_file in code_files:
            try:
                content = code_file.read_text()
                # Check if file contains the screen ID or a normalized version of the name
                name_normalized = screen_name.replace(" ", "").replace("-", "").lower()
                file_name_normalized = code_file.stem.replace(" ", "").replace("-", "").lower()

                if (screen_id in content or
                    name_normalized in file_name_normalized or
                    screen_id.replace("-", "").lower() in file_name_normalized):
                    code_found = True
                    screen_to_code[screen_id] = str(code_file.relative_to(base_path))
                    found_code.append(screen_id)
                    break
            except:
                pass

        if not code_found:
            missing_code.append(f"{screen_id}: {screen_name}")

    # Update registry with code status
    registry["screen_coverage"]["code_generated"] = len(found_code)
    registry["screen_coverage"]["code_missing"] = len(missing_code)

    # Calculate coverage
    total = len(discovery_screens)
    coverage = (len(found_code) / total * 100) if total > 0 else 0
    registry["screen_coverage"]["code_coverage_percent"] = round(coverage, 1)

    # Update traceability
    for screen_id, code_path in screen_to_code.items():
        for trace in registry.get("traceability", []):
            if trace.get("screen_id") == screen_id:
                trace["code_file"] = code_path
                trace["code_status"] = "complete"

    # Mark missing as incomplete
    for screen in registry.get("traceability", []):
        if screen.get("screen_id") in [m.split(":")[0] for m in missing_code]:
            screen["code_status"] = "missing"

    # Write updated registry to SHARED traceability/ at project root
    registry_path = get_traceability_path(base_path) / "screen_registry.json"
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)

    # Generate results
    results.append(f"✅ Screen registry loaded: {total} Discovery screens")
    results.append(f"📊 Code coverage: {len(found_code)}/{total} ({coverage:.1f}%)")

    if missing_code:
        results.append(f"❌ Missing React code ({len(missing_code)}):")
        for code in missing_code:
            results.append(f"   • {code}")
        return False, results

    results.append("✅ All Discovery screens have React components")
    return True, results


def validate_screens(dir_path: str) -> Dict:
    """Full screen validation - Discovery to Specs to Code."""
    base_path = Path(dir_path)

    results = {
        "success": True,
        "validations": [],
        "coverage": {},
        "timestamp": datetime.now().isoformat()
    }

    # Step 1: Check screen registry exists (in SHARED traceability/ at project root)
    registry_path = get_traceability_path(base_path) / "screen_registry.json"
    if not registry_path.exists():
        results["success"] = False
        results["validations"].append("❌ screen_registry.json not found")
        results["validations"].append("   Run Prototype_ValidateDiscovery to generate it")
        return results

    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)

        discovery_count = len(registry.get("discovery_screens", []))
        coverage = registry.get("screen_coverage", {})

        results["validations"].append(f"✅ Screen registry found: {discovery_count} screens from Discovery")

        # Step 2: Validate specs
        specs_generated = coverage.get("specs_generated", 0)
        specs_missing = coverage.get("specs_missing", discovery_count)
        spec_coverage = coverage.get("spec_coverage_percent", 0)

        results["validations"].append(f"📋 Specs: {specs_generated}/{discovery_count} ({spec_coverage}%)")

        if specs_missing > 0:
            results["validations"].append(f"   ⚠️ {specs_missing} screens missing specs")

        # Step 3: Validate code
        code_generated = coverage.get("code_generated", 0)
        code_missing = coverage.get("code_missing", discovery_count)
        code_coverage = coverage.get("code_coverage_percent", 0)

        results["validations"].append(f"💻 Code: {code_generated}/{discovery_count} ({code_coverage}%)")

        if code_missing > 0:
            results["validations"].append(f"   ⚠️ {code_missing} screens missing code")

        # Step 4: Check traceability
        full_trace = 0
        partial_trace = 0
        for trace in registry.get("traceability", []):
            if trace.get("code_status") == "complete" and trace.get("spec_status") == "complete":
                full_trace += 1
            elif trace.get("spec_status") == "complete":
                partial_trace += 1

        results["validations"].append(f"🔗 Full traceability (Discovery→Spec→Code): {full_trace}/{discovery_count}")

        # Set coverage summary
        results["coverage"] = {
            "discovery_screens": discovery_count,
            "specs_generated": specs_generated,
            "code_generated": code_generated,
            "spec_coverage_percent": spec_coverage,
            "code_coverage_percent": code_coverage,
            "full_traceability": full_trace
        }

        # Determine overall success
        if code_coverage < 100:
            results["success"] = False
            results["validations"].append("")
            results["validations"].append("❌ SCREEN VALIDATION FAILED")
            results["validations"].append(f"   {code_missing} screens from Discovery are not implemented")
            results["validations"].append("   All Discovery screens MUST have React code")
        else:
            results["validations"].append("")
            results["validations"].append("✅ SCREEN VALIDATION PASSED")
            results["validations"].append("   All Discovery screens have been implemented")

    except json.JSONDecodeError as e:
        results["success"] = False
        results["validations"].append(f"❌ Invalid JSON in screen_registry.json: {e}")
    except Exception as e:
        results["success"] = False
        results["validations"].append(f"❌ Error: {e}")

    return results


def validate_traceability(dir_path: str) -> Dict:
    """Validate traceability linkages between Discovery and Prototype."""
    base_path = Path(dir_path)

    results = {
        "success": True,
        "validations": [],
        "coverage": {}
    }

    # Check for discovery summary (in SHARED _state/ at project root)
    state_path = get_state_path(base_path)
    discovery_summary_path = state_path / "discovery_summary.json"
    if not discovery_summary_path.exists():
        results["success"] = False
        results["validations"].append("❌ Missing _state/discovery_summary.json")
        return results

    # Check for requirements registry (in SHARED _state/ at project root)
    requirements_path = state_path / "requirements_registry.json"
    if not requirements_path.exists():
        results["success"] = False
        results["validations"].append("❌ Missing _state/requirements_registry.json")
        return results

    try:
        with open(discovery_summary_path, 'r') as f:
            discovery = json.load(f)

        with open(requirements_path, 'r') as f:
            requirements = json.load(f)

        # Count pain points
        pain_points = discovery.get("pain_points", [])
        pain_point_ids = set(pp.get("id") for pp in pain_points)

        # Check requirements link to pain points
        linked_pain_points = set()
        for req in requirements.get("requirements", []):
            refs = req.get("pain_point_refs", [])
            linked_pain_points.update(refs)

        # Calculate coverage
        if pain_point_ids:
            coverage = len(linked_pain_points & pain_point_ids) / len(pain_point_ids) * 100
        else:
            coverage = 0

        results["coverage"] = {
            "pain_points_total": len(pain_point_ids),
            "pain_points_linked": len(linked_pain_points & pain_point_ids),
            "coverage_percent": round(coverage, 1)
        }

        if coverage >= 80:
            results["validations"].append(f"✅ Pain point coverage: {coverage:.1f}%")
        elif coverage >= 50:
            results["validations"].append(f"⚠️ Pain point coverage: {coverage:.1f}% (recommend 80%+)")
        else:
            results["validations"].append(f"❌ Pain point coverage: {coverage:.1f}% (below 50%)")
            results["success"] = False

        # Check for orphan requirements (no pain point refs)
        orphan_count = sum(1 for req in requirements.get("requirements", [])
                         if not req.get("pain_point_refs"))
        if orphan_count > 0:
            results["validations"].append(f"⚠️ {orphan_count} requirements without pain_point_refs")
        else:
            results["validations"].append("✅ All requirements linked to pain points")

    except json.JSONDecodeError as e:
        results["success"] = False
        results["validations"].append(f"❌ JSON parse error: {e}")
    except Exception as e:
        results["success"] = False
        results["validations"].append(f"❌ Error: {e}")

    return results


# ============================================================================
# FEEDBACK VALIDATION FUNCTIONS
# ============================================================================

def get_feedback_sessions_path(prototype_path: Path) -> Path:
    """Get the feedback-sessions folder path within the Prototype folder."""
    return prototype_path / "feedback-sessions"


def get_feedback_registry_path(prototype_path: Path) -> Path:
    """Get the prototype_feedback_registry.json path."""
    return get_feedback_sessions_path(prototype_path) / "prototype_feedback_registry.json"


def validate_feedback_registry(prototype_path: Path) -> Dict:
    """Validate the feedback registry structure and integrity."""
    registry_path = get_feedback_registry_path(prototype_path)

    results = {
        "success": True,
        "validations": [],
        "statistics": {},
        "timestamp": datetime.now().isoformat()
    }

    if not registry_path.exists():
        results["success"] = False
        results["validations"].append("❌ prototype_feedback_registry.json not found")
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

        # Validate each feedback item has required fields
        feedback_items = registry.get("feedback_items", [])
        invalid_items = []

        required_item_fields = ["id", "status", "type", "title", "session_folder"]
        for item in feedback_items:
            missing = [f for f in required_item_fields if f not in item]
            if missing:
                invalid_items.append(f"{item.get('id', 'UNKNOWN')}: missing {missing}")

        if invalid_items:
            results["validations"].append(f"⚠️ {len(invalid_items)} items with missing fields:")
            for item in invalid_items[:5]:
                results["validations"].append(f"   • {item}")
            if len(invalid_items) > 5:
                results["validations"].append(f"   ... and {len(invalid_items) - 5} more")
        else:
            results["validations"].append(f"✅ All {len(feedback_items)} items have required fields")

        return results

    except json.JSONDecodeError as e:
        results["success"] = False
        results["validations"].append(f"❌ Invalid JSON in registry: {e}")
        return results
    except Exception as e:
        results["success"] = False
        results["validations"].append(f"❌ Error reading registry: {e}")
        return results


def validate_feedback_session(prototype_path: Path, feedback_id: str) -> Dict:
    """Validate a specific feedback session has all required files."""
    results = {
        "success": True,
        "feedback_id": feedback_id,
        "validations": [],
        "files_found": [],
        "files_missing": [],
        "timestamp": datetime.now().isoformat()
    }

    # Load registry to find session folder
    registry_path = get_feedback_registry_path(prototype_path)
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

        session_path = prototype_path / session_folder
        if not session_path.exists():
            results["success"] = False
            results["validations"].append(f"❌ Session folder not found: {session_folder}")
            return results

        results["validations"].append(f"✅ Session folder exists: {session_folder}")

        # Define required files based on status
        status = feedback_item.get("status", "")

        # Base files always required after registration
        required_files = ["FEEDBACK_ORIGINAL.md"]

        # Files required based on how far the feedback has progressed
        if status in ["approved", "in_progress", "implemented", "validated", "closed"]:
            required_files.append("impact_analysis.md")

        if status in ["in_progress", "implemented", "validated", "closed"]:
            required_files.extend([
                "implementation_options.md",
                "implementation_plan.md"
            ])

        if status in ["implemented", "validated", "closed"]:
            required_files.append("implementation_log.md")

        if status in ["validated", "closed"]:
            required_files.extend([
                "files_changed.md",
                "VALIDATION_REPORT.md",
                "FEEDBACK_SUMMARY.md"
            ])

        # Check each required file
        for req_file in required_files:
            file_path = session_path / req_file
            if file_path.exists():
                results["files_found"].append(req_file)
                results["validations"].append(f"✅ {req_file}")
            else:
                results["files_missing"].append(req_file)
                results["validations"].append(f"❌ {req_file} - Not found")
                results["success"] = False

        # Summary
        found_count = len(results["files_found"])
        total_count = len(required_files)
        coverage = (found_count / total_count * 100) if total_count > 0 else 0

        results["validations"].append("")
        results["validations"].append(f"📊 Session completeness: {found_count}/{total_count} ({coverage:.0f}%)")

        return results

    except Exception as e:
        results["success"] = False
        results["validations"].append(f"❌ Error: {e}")
        return results


def validate_feedback_versions(prototype_path: Path, feedback_id: str) -> Dict:
    """Validate that files modified by feedback have correct version increments."""
    results = {
        "success": True,
        "feedback_id": feedback_id,
        "validations": [],
        "version_checks": [],
        "timestamp": datetime.now().isoformat()
    }

    # Load registry
    registry_path = get_feedback_registry_path(prototype_path)
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
            results["validations"].append(f"❌ Feedback {feedback_id} not found")
            return results

        # Get session folder to read implementation log
        session_folder = feedback_item.get("session_folder")
        if not session_folder:
            results["validations"].append("⚠️ No session folder - cannot verify versions")
            return results

        impl_log_path = prototype_path / session_folder / "implementation_log.md"
        files_changed_path = prototype_path / session_folder / "files_changed.md"

        # Try to read files_changed.md for list of modified files
        modified_files = []
        if files_changed_path.exists():
            try:
                content = files_changed_path.read_text()
                # Parse table rows for file paths
                # Looking for pattern: | path/to/file.md | Action | Version |
                file_pattern = r'\|\s*([^\|]+\.(?:md|json))\s*\|'
                matches = re.findall(file_pattern, content)
                modified_files = [m.strip() for m in matches if not m.strip().startswith('File')]
            except:
                pass

        if not modified_files:
            results["validations"].append("⚠️ No modified files found to verify")
            return results

        results["validations"].append(f"📋 Checking {len(modified_files)} modified files")

        # Check each file for feedback reference in change_history
        root_path = get_root_path(prototype_path)
        files_with_ref = 0
        files_without_ref = 0

        for file_rel_path in modified_files[:10]:  # Check up to 10 files
            # Resolve path
            if file_rel_path.startswith("_state/"):
                file_path = get_state_path(prototype_path) / file_rel_path[7:]
            elif file_rel_path.startswith("traceability/"):
                file_path = get_traceability_path(prototype_path) / file_rel_path[13:]
            else:
                file_path = prototype_path / file_rel_path

            if not file_path.exists():
                results["validations"].append(f"⚠️ {file_rel_path} - File not found")
                continue

            try:
                content = file_path.read_text()

                # Check for feedback ID reference
                if feedback_id in content:
                    files_with_ref += 1
                    results["version_checks"].append({
                        "file": file_rel_path,
                        "has_feedback_ref": True,
                        "status": "pass"
                    })
                    results["validations"].append(f"✅ {file_rel_path} - Has {feedback_id} reference")
                else:
                    files_without_ref += 1
                    results["version_checks"].append({
                        "file": file_rel_path,
                        "has_feedback_ref": False,
                        "status": "fail"
                    })
                    results["validations"].append(f"❌ {file_rel_path} - Missing {feedback_id} reference")
                    results["success"] = False

            except Exception as e:
                results["validations"].append(f"⚠️ {file_rel_path} - Error reading: {e}")

        # Summary
        results["validations"].append("")
        results["validations"].append(f"📊 Version integrity: {files_with_ref}/{files_with_ref + files_without_ref} files have feedback reference")

        return results

    except Exception as e:
        results["success"] = False
        results["validations"].append(f"❌ Error: {e}")
        return results


def validate_feedback(prototype_path: Path, feedback_id: str) -> Dict:
    """Complete feedback validation - session, versions, and traceability."""
    results = {
        "success": True,
        "feedback_id": feedback_id,
        "validations": [],
        "checks": {
            "session": None,
            "versions": None
        },
        "timestamp": datetime.now().isoformat()
    }

    # Validate session
    session_result = validate_feedback_session(prototype_path, feedback_id)
    results["checks"]["session"] = session_result

    if not session_result["success"]:
        results["success"] = False
        results["validations"].append("❌ Session validation failed")
    else:
        results["validations"].append("✅ Session validation passed")

    # Only check versions if session passed and feedback is implemented
    registry_path = get_feedback_registry_path(prototype_path)
    if registry_path.exists():
        try:
            with open(registry_path, 'r') as f:
                registry = json.load(f)

            feedback_item = None
            for item in registry.get("feedback_items", []):
                if item.get("id") == feedback_id:
                    feedback_item = item
                    break

            if feedback_item and feedback_item.get("status") in ["implemented", "validated", "closed"]:
                version_result = validate_feedback_versions(prototype_path, feedback_id)
                results["checks"]["versions"] = version_result

                if not version_result["success"]:
                    results["success"] = False
                    results["validations"].append("❌ Version validation failed")
                else:
                    results["validations"].append("✅ Version validation passed")
        except:
            pass

    # Final status
    results["validations"].append("")
    if results["success"]:
        results["validations"].append("════════════════════════════════════════")
        results["validations"].append(f" FEEDBACK VALIDATION PASSED: {feedback_id}")
        results["validations"].append("════════════════════════════════════════")
    else:
        results["validations"].append("════════════════════════════════════════")
        results["validations"].append(f" FEEDBACK VALIDATION FAILED: {feedback_id}")
        results["validations"].append("════════════════════════════════════════")

    return results


def list_feedback(prototype_path: Path) -> Dict:
    """List all feedback items with their status."""
    results = {
        "success": True,
        "feedback_items": [],
        "validations": [],
        "timestamp": datetime.now().isoformat()
    }

    registry_path = get_feedback_registry_path(prototype_path)
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

        # Display in order of workflow progression
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

        # Any unknown statuses
        for status, items in by_status.items():
            if status not in status_order:
                results["validations"].append(f"\n  {status.upper()} ({len(items)}):")
                for item in items:
                    results["validations"].append(f"    • {item.get('id')}: {item.get('title', '')[:40]}")

        return results

    except Exception as e:
        results["success"] = False
        results["validations"].append(f"❌ Error reading registry: {e}")
        return results


def generate_validation_summary(dir_path: str, output_file: Optional[str] = None) -> Dict:
    """
    Generate comprehensive validation summary for entire prototype.

    Aggregates validation results across all checkpoints, traceability,
    and screen coverage to provide a complete quality report.

    Args:
        dir_path: Path to prototype directory
        output_file: Optional path to save summary report

    Returns:
        Dictionary with summary results
    """
    base_path = Path(dir_path)

    summary = {
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "prototype_path": str(base_path),
        "checkpoints": {},
        "overall_stats": {
            "total_checkpoints": len(CHECKPOINT_REQUIREMENTS),
            "passed": 0,
            "failed": 0,
            "not_reached": 0
        },
        "critical_issues": [],
        "warnings": [],
        "recommendations": [],
        "validations": []
    }

    # Validate all checkpoints
    summary["validations"].append("═" * 70)
    summary["validations"].append(" PROTOTYPE VALIDATION SUMMARY")
    summary["validations"].append("═" * 70)
    summary["validations"].append("")
    summary["validations"].append(f"Prototype Path: {base_path}")
    summary["validations"].append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary["validations"].append("")
    summary["validations"].append("─" * 70)
    summary["validations"].append(" CHECKPOINT VALIDATION")
    summary["validations"].append("─" * 70)
    summary["validations"].append("")

    for checkpoint in sorted(CHECKPOINT_REQUIREMENTS.keys()):
        req = CHECKPOINT_REQUIREMENTS[checkpoint]
        result = validate_checkpoint(checkpoint, dir_path)

        summary["checkpoints"][checkpoint] = {
            "name": req["name"],
            "success": result["success"],
            "validation_count": len(result.get("validations", [])),
            "issues": [v for v in result.get("validations", []) if v.startswith("❌")]
        }

        # Update stats
        if result["success"]:
            summary["overall_stats"]["passed"] += 1
            status_icon = "✅"
        else:
            summary["overall_stats"]["failed"] += 1
            status_icon = "❌"
            summary["success"] = False

            # Collect critical issues
            for validation in result.get("validations", []):
                if "❌" in validation:
                    summary["critical_issues"].append({
                        "checkpoint": checkpoint,
                        "name": req["name"],
                        "issue": validation
                    })

        summary["validations"].append(
            f"  {status_icon} Checkpoint {checkpoint}: {req['name']}"
        )

    summary["validations"].append("")
    summary["validations"].append("─" * 70)
    summary["validations"].append(" TRACEABILITY VALIDATION")
    summary["validations"].append("─" * 70)
    summary["validations"].append("")

    # Validate traceability
    trace_result = validate_traceability(dir_path)
    if trace_result["success"]:
        summary["validations"].append("  ✅ Traceability linkages valid")
        if "coverage" in trace_result:
            coverage = trace_result["coverage"]
            summary["validations"].append(
                f"     Pain point coverage: {coverage.get('coverage_percent', 0)}%"
            )
    else:
        summary["validations"].append("  ❌ Traceability validation failed")
        summary["success"] = False
        for validation in trace_result.get("validations", []):
            if "❌" in validation:
                summary["critical_issues"].append({
                    "checkpoint": "traceability",
                    "name": "Traceability",
                    "issue": validation
                })

    summary["validations"].append("")
    summary["validations"].append("─" * 70)
    summary["validations"].append(" SCREEN COVERAGE VALIDATION")
    summary["validations"].append("─" * 70)
    summary["validations"].append("")

    # Validate screen coverage
    screen_result = validate_screens(dir_path)
    if screen_result["success"]:
        summary["validations"].append("  ✅ All Discovery screens implemented")
        if "coverage" in screen_result:
            cov = screen_result["coverage"]
            summary["validations"].append(
                f"     Discovery screens: {cov.get('discovery_screens', 0)}"
            )
            summary["validations"].append(
                f"     Specs generated: {cov.get('specs_generated', 0)} "
                f"({cov.get('spec_coverage_percent', 0)}%)"
            )
            summary["validations"].append(
                f"     Code generated: {cov.get('code_generated', 0)} "
                f"({cov.get('code_coverage_percent', 0)}%)"
            )
    else:
        summary["validations"].append("  ❌ Screen coverage incomplete")
        summary["success"] = False
        for validation in screen_result.get("validations", []):
            if "❌" in validation:
                summary["critical_issues"].append({
                    "checkpoint": "screens",
                    "name": "Screen Coverage",
                    "issue": validation
                })

    summary["validations"].append("")
    summary["validations"].append("─" * 70)
    summary["validations"].append(" OVERALL STATISTICS")
    summary["validations"].append("─" * 70)
    summary["validations"].append("")

    stats = summary["overall_stats"]
    summary["validations"].append(f"  Total Checkpoints: {stats['total_checkpoints']}")
    summary["validations"].append(f"  ✅ Passed: {stats['passed']}")
    summary["validations"].append(f"  ❌ Failed: {stats['failed']}")

    success_rate = (stats['passed'] / stats['total_checkpoints'] * 100) if stats['total_checkpoints'] > 0 else 0
    summary["validations"].append(f"  Success Rate: {success_rate:.1f}%")

    # Critical issues section
    if summary["critical_issues"]:
        summary["validations"].append("")
        summary["validations"].append("─" * 70)
        summary["validations"].append(" CRITICAL ISSUES")
        summary["validations"].append("─" * 70)
        summary["validations"].append("")

        for issue in summary["critical_issues"][:10]:  # Show first 10
            summary["validations"].append(f"  {issue['issue']}")
            summary["validations"].append(f"     Location: {issue['name']} (CP{issue['checkpoint']})")
            summary["validations"].append("")

        if len(summary["critical_issues"]) > 10:
            summary["validations"].append(
                f"  ... and {len(summary['critical_issues']) - 10} more issues"
            )

    # Recommendations
    summary["validations"].append("")
    summary["validations"].append("─" * 70)
    summary["validations"].append(" RECOMMENDATIONS")
    summary["validations"].append("─" * 70)
    summary["validations"].append("")

    if summary["success"]:
        summary["validations"].append("  🎉 All validations passed!")
        summary["validations"].append("     Prototype is ready for delivery.")
        summary["recommendations"].append("Prototype ready for delivery")
    else:
        summary["validations"].append("  ⚠️  Validation incomplete - address the following:")
        summary["validations"].append("")

        # Add specific recommendations based on failures
        failed_checkpoints = [
            cp for cp, data in summary["checkpoints"].items()
            if not data["success"]
        ]

        if failed_checkpoints:
            summary["validations"].append("  1. Fix failing checkpoints:")
            for cp in failed_checkpoints[:5]:
                name = summary["checkpoints"][cp]["name"]
                skill = ErrorGuidance.CHECKPOINT_TO_SKILL.get(cp, "unknown")
                summary["validations"].append(f"     • Checkpoint {cp} ({name})")
                summary["validations"].append(f"       Fix: /prototype-{skill}")

            summary["recommendations"].append(
                f"Fix {len(failed_checkpoints)} failing checkpoints"
            )

        if not trace_result["success"]:
            summary["validations"].append("  2. Fix traceability linkages:")
            summary["validations"].append("     Run: python3 .claude/hooks/prototype_quality_gates.py --validate-traceability")
            summary["recommendations"].append("Fix traceability linkages")

        if not screen_result["success"]:
            summary["validations"].append("  3. Complete screen implementation:")
            summary["validations"].append("     Run: /prototype-screens")
            summary["recommendations"].append("Complete screen implementation")

    summary["validations"].append("")
    summary["validations"].append("═" * 70)

    if summary["success"]:
        summary["validations"].append(" ✅ VALIDATION COMPLETE - ALL CHECKS PASSED")
    else:
        summary["validations"].append(" ❌ VALIDATION INCOMPLETE - ISSUES FOUND")

    summary["validations"].append("═" * 70)

    # Optionally save to file
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            f.write("\n".join(summary["validations"]))
            f.write("\n")

        summary["validations"].append("")
        summary["validations"].append(f"📄 Summary saved to: {output_file}")

    return summary


def list_checkpoints() -> None:
    """List all checkpoint requirements."""
    print("\n" + "=" * 60)
    print("  PROTOTYPE CHECKPOINTS")
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
            for f in req["required_folders"][:5]:  # Show first 5
                print(f"    • {f}/")
            if len(req["required_folders"]) > 5:
                print(f"    ... and {len(req['required_folders']) - 5} more")

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
    else:
        print(f"  Traceability Validation - {status}")
    print("=" * 60 + "\n")

    for validation in results.get("validations", []):
        print(f"  {validation}")

    if "coverage" in results:
        print("\n  Coverage Metrics:")
        for key, value in results["coverage"].items():
            print(f"    • {key}: {value}")

    print("")


def main():
    parser = argparse.ArgumentParser(
        description="Prototype Quality Gates - Checkpoint Validation"
    )

    parser.add_argument(
        "--validate-checkpoint",
        type=int,
        metavar="N",
        help="Validate specific checkpoint (0-14)"
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
        "--validate-screens",
        action="store_true",
        help="Validate ALL Discovery screens have specs and code"
    )

    parser.add_argument(
        "--validate-screen-specs",
        action="store_true",
        help="Validate ALL Discovery screens have spec files"
    )

    parser.add_argument(
        "--validate-screen-code",
        action="store_true",
        help="Validate ALL screen specs have React code"
    )

    parser.add_argument(
        "--validate-feedback",
        type=str,
        metavar="PF-NNN",
        help="Validate a specific feedback item (e.g., PF-001)"
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

    parser.add_argument(
        "--generate-summary",
        action="store_true",
        help="Generate comprehensive validation summary for entire prototype"
    )

    parser.add_argument(
        "--output",
        type=str,
        metavar="FILE",
        help="Output file path for summary report (use with --generate-summary)"
    )

    # Auto-fix generation options (Task 4.4)
    parser.add_argument(
        "--generate-fix",
        type=str,
        metavar="TYPE",
        choices=["config_missing", "progress_missing", "requirements_missing",
                 "screen_registry_missing", "markdown_missing", "folder_missing"],
        help="Generate auto-fix script for specific error type"
    )

    parser.add_argument(
        "--system-name",
        type=str,
        metavar="NAME",
        help="System name for template generation (use with --generate-fix)"
    )

    parser.add_argument(
        "--fix-output",
        type=str,
        metavar="FILE",
        help="Output file for generated fix script (use with --generate-fix)"
    )

    parser.add_argument(
        "--doc-type",
        type=str,
        metavar="TYPE",
        choices=["DATA_MODEL", "API_CONTRACTS", "COMPONENT_INDEX", "SCREEN_INDEX"],
        help="Document type for markdown template (use with --generate-fix markdown_missing)"
    )

    parser.add_argument(
        "--file-path",
        type=str,
        metavar="PATH",
        help="File path for fix generation (use with --generate-fix)"
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
        help="List all N/A artifacts in the prototype"
    )

    parser.add_argument(
        "--dir",
        type=str,
        default=".",
        help="Prototype directory path"
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
        list_na_artifacts_report(base_path, "prototype")
        sys.exit(0)

    # Auto-fix generation handler (Task 4.4)
    if args.generate_fix:
        # Gather kwargs for fix generation
        kwargs = {
            "system_name": args.system_name or "System",
            "file_path": args.file_path or ""
        }

        if args.doc_type:
            kwargs["doc_type"] = args.doc_type

        # Generate fix
        fix = AutoFixGenerator.suggest_fix(args.generate_fix, **kwargs)

        # Output or save
        if args.fix_output:
            with open(args.fix_output, 'w') as f:
                f.write(fix['script'])
            print(f"✅ Fix script saved to: {args.fix_output}")
            if not args.json:
                print(f"\nTo apply the fix, run:")
                print(f"  bash {args.fix_output}")
        else:
            if args.json:
                print(json.dumps(fix, indent=2))
            else:
                print("=" * 70)
                print("AUTO-GENERATED FIX (Task 4.4)")
                print("=" * 70)
                print("\n📋 QUICK FIX COMMAND:\n")
                print(fix['command'])
                print("\n" + "─" * 70)
                print("📝 OR - CREATE FILE WITH THIS CONTENT:")
                print("─" * 70 + "\n")
                print(fix['code'])
                print("\n" + "─" * 70)
                print("🔧 OR - SAVE AND RUN THIS SCRIPT:")
                print("─" * 70 + "\n")
                print(fix['script'])
                print("\n" + "=" * 70)

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

    if args.validate_screens:
        results = validate_screens(args.dir)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)
        sys.exit(0 if results["success"] else 1)

    if args.validate_screen_specs:
        base_path = Path(args.dir)
        passed, messages = validate_all_screens_have_specs(base_path)
        results = {
            "success": passed,
            "validations": messages
        }
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)
        sys.exit(0 if passed else 1)

    if args.validate_screen_code:
        base_path = Path(args.dir)
        passed, messages = validate_all_specs_have_code(base_path)
        results = {
            "success": passed,
            "validations": messages
        }
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print_results(results)
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

    if args.generate_summary:
        results = generate_validation_summary(args.dir, output_file=args.output)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            # Print the formatted validation output
            for line in results["validations"]:
                print(line)
        sys.exit(0 if results["success"] else 1)

    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
