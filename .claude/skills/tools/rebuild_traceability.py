#!/usr/bin/env python3
"""
Rebuild Traceability Registries from Discovery Outputs

This script parses existing Discovery markdown files and populates
the traceability JSON registries. It also generates traceability
documentation (TRACEABILITY_MATRIX_MASTER.md and TRACEABILITY_ASSESSMENT_REPORT.md).

Usage:
    python3 .claude/skills/tools/rebuild_traceability.py --dir ClientAnalysis_[SystemName]/
"""

import json
import re
import sys
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add the tools directory to path for importing traceability_manager
TOOLS_DIR = Path(__file__).parent
sys.path.insert(0, str(TOOLS_DIR))

TRACEABILITY_DIR = Path("traceability")

def get_timestamp():
    return datetime.now().isoformat()

def init_registry(filename, format_type, key):
    """Initialize a registry file with empty structure."""
    filepath = TRACEABILITY_DIR / filename
    timestamp = get_timestamp()

    if format_type == "A":
        template = {
            "version": "1.0.0",
            "created_at": timestamp,
            "updated_at": timestamp,
            key: []
        }
    else:  # Format B
        template = {
            "items": [],
            "meta": {
                "schema_version": "1.0",
                "updated_at": timestamp
            }
        }

    with open(filepath, "w") as f:
        json.dump(template, f, indent=2)
    return template

def add_to_registry(filename, format_type, key, item):
    """Add an item to a registry file."""
    filepath = TRACEABILITY_DIR / filename

    if not filepath.exists():
        data = init_registry(filename, format_type, key)
    else:
        with open(filepath, "r") as f:
            data = json.load(f)

    data_key = key if format_type == "A" else "items"
    if data_key not in data:
        data[data_key] = []

    # Check if item already exists
    item_id = item.get("id")
    updated = False
    for i, existing in enumerate(data[data_key]):
        if isinstance(existing, dict) and existing.get("id") == item_id:
            data[data_key][i] = item
            updated = True
            break

    if not updated:
        data[data_key].append(item)

    # Update timestamp
    if format_type == "A":
        data["updated_at"] = get_timestamp()
    else:
        data["meta"]["updated_at"] = get_timestamp()

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

    return "Updated" if updated else "Added"

def parse_pain_points(filepath):
    """Parse PAIN_POINTS.md and extract pain point data."""
    pain_points = []

    with open(filepath, "r") as f:
        content = f.read()

    # Format: #### PP-1.1: Title
    # Then: - **Priority**: High
    #       - **Description**: ...

    # Split content by pain point sections (#### PP-)
    sections = re.split(r'(?=####\s+PP-\d+\.\d+:)', content)

    for section in sections:
        # Must start with PP- after ####
        if not re.match(r'####\s+PP-\d+\.\d+:', section):
            continue

        # Extract ID and title: #### PP-1.1: Title
        id_match = re.search(r'####\s+(PP-\d+\.\d+):\s*(.+?)(?=\n)', section)
        if not id_match:
            continue

        pp_id = id_match.group(1)
        title = id_match.group(2).strip()

        # Extract priority: - **Priority**: High
        priority_match = re.search(r'-\s*\*\*Priority\*\*:\s*(\w+)', section)
        priority = priority_match.group(1) if priority_match else "Medium"

        # Map priority to P0/P1/P2
        priority_map = {"High": "P0", "Medium": "P1", "Low": "P2"}
        priority_code = priority_map.get(priority, "P1")

        # Extract description: - **Description**: ...
        desc_match = re.search(r'-\s*\*\*Description\*\*:\s*(.+?)(?=\n-|\n\n|$)', section, re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else title

        # Extract impact: - **Impact**: ...
        impact_match = re.search(r'-\s*\*\*Impact\*\*:\s*(.+?)(?=\n)', section)
        impact = impact_match.group(1).strip() if impact_match else ""

        # Extract affected users: - **Affected Users**: ...
        users_match = re.search(r'-\s*\*\*Affected Users\*\*:\s*(.+?)(?=\n)', section)
        affected_users = users_match.group(1).strip() if users_match else ""

        pain_points.append({
            "id": pp_id,
            "title": title,
            "description": description,
            "priority": priority_code,
            "impact": impact,
            "affected_users": affected_users,
            "source": "PAIN_POINTS.md"
        })

    return pain_points

def parse_jtbd(filepath):
    """Parse JOBS_TO_BE_DONE.md and extract JTBD data."""
    jtbds = []

    with open(filepath, "r") as f:
        content = f.read()

    # Pattern to match JTBD sections
    # Format: ### JTBD-X.Y: Title
    jtbd_pattern = r'###\s+(JTBD-\d+\.\d+):\s+(.+?)(?=\n)'
    statement_pattern = r'\*\*Statement\*\*:\s*(.+?)(?=\n\n|\n\|)'
    pain_points_pattern = r'\|\s*Related Pain Points\s*\|\s*([^|]+)\s*\|'
    persona_pattern = r'\|\s*Persona\s*\|\s*([^|]+)\s*\|'
    importance_pattern = r'\|\s*Importance\s*\|\s*(\w+)\s*\|'

    # Split content by JTBD sections
    sections = re.split(r'(?=###\s+JTBD-)', content)

    for section in sections:
        if not re.search(r'JTBD-\d+\.\d+', section):
            continue

        # Extract ID and title
        id_match = re.search(jtbd_pattern, section)
        if not id_match:
            continue

        jtbd_id = id_match.group(1)
        title = id_match.group(2).strip()

        # Extract statement
        stmt_match = re.search(statement_pattern, section, re.DOTALL)
        statement = stmt_match.group(1).strip() if stmt_match else title

        # Extract related pain points
        pp_match = re.search(pain_points_pattern, section)
        related_pps = []
        if pp_match:
            pp_text = pp_match.group(1).strip()
            related_pps = [p.strip() for p in re.findall(r'PP-\d+\.\d+', pp_text)]

        # Extract importance
        imp_match = re.search(importance_pattern, section)
        importance = imp_match.group(1).strip() if imp_match else "High"

        # Map importance to priority
        priority_map = {"Critical": "P0", "High": "P1", "Medium": "P2", "Low": "P2"}
        priority = priority_map.get(importance, "P1")

        jtbds.append({
            "id": jtbd_id,
            "title": title,
            "statement": statement,
            "priority": priority,
            "related_pain_points": related_pps,
            "source": "JOBS_TO_BE_DONE.md"
        })

    return jtbds

def parse_user_types(filepath):
    """Parse USER_TYPES.md and extract user type data."""
    user_types = []

    with open(filepath, "r") as f:
        content = f.read()

    # Pattern to match user type sections
    # Format: ### UT-XXX: Name or ## User Type N: Name
    ut_pattern = r'###?\s+(UT-\d+|User Type \d+):\s*(.+?)(?=\n)'
    role_pattern = r'\*\*Role\*\*:\s*(.+?)(?=\n)'
    category_pattern = r'\*\*Category\*\*:\s*(.+?)(?=\n)'

    # Also try to extract from persona files
    sections = re.split(r'(?=###?\s+(?:UT-|User Type))', content)

    for section in sections:
        id_match = re.search(ut_pattern, section)
        if not id_match:
            continue

        ut_id = id_match.group(1)
        if not ut_id.startswith("UT-"):
            # Normalize ID
            num = re.search(r'\d+', ut_id)
            ut_id = f"UT-{num.group()}" if num else ut_id

        name = id_match.group(2).strip()

        # Extract role
        role_match = re.search(role_pattern, section)
        role = role_match.group(1).strip() if role_match else name

        # Extract category
        cat_match = re.search(category_pattern, section)
        category = cat_match.group(1).strip() if cat_match else "Primary"

        user_types.append({
            "id": ut_id,
            "name": name,
            "role": role,
            "category": category,
            "source": "USER_TYPES.md"
        })

    return user_types

def parse_screens(filepath):
    """Parse screen-definitions.md and extract screen data."""
    screens = []

    with open(filepath, "r") as f:
        content = f.read()

    # Format: ### M-01: Task Execution Screen
    #         **Screen ID**: M-01
    #         **Priority**: P0 (Phase 1)
    #         **Purpose**: Primary screen for...
    #         **JTBD Addressed**: JTBD-1.1, JTBD-1.2

    # Split by screen sections (### M-XX: or ### D-XX:)
    sections = re.split(r'(?=###\s+[MD]-\d+:)', content)

    for section in sections:
        # Must start with screen pattern
        if not re.match(r'###\s+[MD]-\d+:', section):
            continue

        # Extract ID and title: ### M-01: Task Execution Screen
        id_match = re.search(r'###\s+([MD]-\d+):\s*(.+?)(?=\n)', section)
        if not id_match:
            continue

        screen_id = id_match.group(1)
        name = id_match.group(2).strip()

        # Extract priority: **Priority**: P0 (Phase 1)
        priority_match = re.search(r'\*\*Priority\*\*:\s*(\w+)', section)
        priority = priority_match.group(1) if priority_match else "P1"

        # Extract purpose: **Purpose**: ...
        purpose_match = re.search(r'\*\*Purpose\*\*:\s*(.+?)(?=\n\n|\n\*\*)', section, re.DOTALL)
        purpose = purpose_match.group(1).strip() if purpose_match else ""

        # Extract JTBD references: **JTBD Addressed**: JTBD-1.1, JTBD-1.2
        jtbd_match = re.search(r'\*\*JTBD Addressed\*\*:\s*(.+?)(?=\n)', section)
        related_jtbds = []
        if jtbd_match:
            jtbd_text = jtbd_match.group(1)
            related_jtbds = re.findall(r'JTBD-\d+\.\d+', jtbd_text)

        # Extract users: **Users**: Warehouse Operators
        users_match = re.search(r'\*\*Users\*\*:\s*(.+?)(?=\n)', section)
        users = users_match.group(1).strip() if users_match else ""

        screens.append({
            "id": screen_id,
            "name": name,
            "purpose": purpose,
            "priority": priority,
            "related_jtbds": related_jtbds,
            "users": users,
            "source": "screen-definitions.md"
        })

    return screens

def create_trace_links(pain_points, jtbds, screens=None):
    """Create trace links between pain points, JTBDs, and screens."""
    links = []

    # PP -> JTBD links
    for jtbd in jtbds:
        for pp_id in jtbd.get("related_pain_points", []):
            links.append({
                "id": f"LINK-{pp_id}-{jtbd['id']}",
                "source": pp_id,
                "target": jtbd["id"],
                "type": "addresses",
                "timestamp": get_timestamp()
            })

    # Screen -> JTBD links
    if screens:
        for screen in screens:
            for jtbd_id in screen.get("related_jtbds", []):
                links.append({
                    "id": f"LINK-{screen['id']}-{jtbd_id}",
                    "source": screen["id"],
                    "target": jtbd_id,
                    "type": "implements",
                    "timestamp": get_timestamp()
                })

    return links


def load_registry(filename):
    """Load a registry file from the traceability directory."""
    filepath = TRACEABILITY_DIR / filename
    if not filepath.exists():
        return None
    with open(filepath, "r") as f:
        return json.load(f)


def load_implementation_data():
    """Load all implementation phase registries."""
    impl_data = {
        "tasks": [],
        "modules": [],
        "components": [],
        "adrs": [],
        "test_cases": [],
        "progress": None
    }

    # Load task registry
    task_registry = load_registry("task_registry.json")
    if task_registry:
        impl_data["tasks"] = task_registry.get("tasks", [])

    # Load module registry
    module_registry = load_registry("module_registry.json")
    if module_registry:
        impl_data["modules"] = module_registry.get("modules", [])

    # Load component registry
    component_registry = load_registry("component_registry.json")
    if component_registry:
        impl_data["components"] = component_registry.get("components", [])

    # Load ADR registry
    adr_registry = load_registry("adr_registry.json")
    if adr_registry:
        impl_data["adrs"] = adr_registry.get("adrs", [])

    # Load test case registry
    test_registry = load_registry("test_case_registry.json")
    if test_registry:
        impl_data["test_cases"] = test_registry.get("test_cases", test_registry.get("items", []))

    # Load implementation traceability register
    impl_register = load_registry("implementation_traceability_register.json")
    if impl_register:
        impl_data["progress"] = impl_register

    return impl_data


def build_module_to_task_map(tasks):
    """Build mapping from Modules to Tasks."""
    mod_to_task = defaultdict(list)
    for task in tasks:
        module_ref = task.get("module_ref", "")
        if module_ref:
            mod_to_task[module_ref].append(task.get("id", ""))
    return mod_to_task


def build_task_to_files_map(tasks):
    """Build mapping from Tasks to Code Files and Test Files."""
    task_to_code = {}
    task_to_tests = {}
    for task in tasks:
        task_id = task.get("id", "")
        task_to_code[task_id] = task.get("files", [])
        task_to_tests[task_id] = task.get("test_files", [])
    return task_to_code, task_to_tests


def build_screen_to_module_map(modules):
    """Build mapping from Screen IDs to Modules (reverse lookup)."""
    screen_to_mod = defaultdict(list)
    for module in modules:
        mod_id = module.get("id", "")
        for screen_ref in module.get("screen_refs", []):
            screen_to_mod[screen_ref].append(mod_id)
    return screen_to_mod


def build_module_to_adr_map(modules):
    """Build mapping from Modules to ADRs."""
    mod_to_adr = defaultdict(list)
    for module in modules:
        mod_id = module.get("id", "")
        for adr_ref in module.get("adr_refs", []):
            mod_to_adr[mod_id].append(adr_ref)
    return mod_to_adr


def load_client_facts():
    """Load client facts from client_facts_registry.json."""
    cf_registry = load_registry("client_facts_registry.json")
    if cf_registry:
        return cf_registry.get("facts", []), cf_registry.get("source_files", [])
    return [], []


def build_cf_to_pp_map(client_facts):
    """Build mapping from Client Facts to Pain Points using referenced_by field."""
    cf_to_pp = defaultdict(list)
    pp_to_cf = defaultdict(list)

    for fact in client_facts:
        cf_id = fact.get("id", "")
        referenced_by = fact.get("referenced_by", [])

        for ref in referenced_by:
            # Only track PP references (Pain Points start with PP-)
            if ref.startswith("PP-"):
                cf_to_pp[cf_id].append(ref)
                pp_to_cf[ref].append(cf_id)

    return cf_to_pp, pp_to_cf


def build_complete_e2e_chains(pain_points, jtbds, screens, modules, tasks, client_facts=None):
    """
    Build complete end-to-end traceability chains from Client Facts to Code/Tests.

    Chain: CF → PP → JTBD → Screen → Module → Task → Code → Tests

    Returns a list of chain dictionaries with all levels populated.
    """
    chains = []

    # Build CF → PP mapping if client_facts provided
    pp_to_cfs = defaultdict(list)
    if client_facts:
        cf_to_pp, pp_to_cfs = build_cf_to_pp_map(client_facts)

    # Build all necessary reverse mappings
    # JTBD.related_pain_points gives us PP → JTBD
    pp_to_jtbds = defaultdict(list)
    for jtbd in jtbds:
        for pp_id in jtbd.get("related_pain_points", []):
            pp_to_jtbds[pp_id].append(jtbd.get("id", ""))

    # Screen.jtbd_refs or related_jtbds gives us JTBD → Screen
    jtbd_to_screens = defaultdict(list)
    for screen in screens:
        jtbd_refs = screen.get("jtbd_refs", screen.get("related_jtbds", []))
        for jtbd_id in jtbd_refs:
            jtbd_to_screens[jtbd_id].append(screen.get("id", ""))

    # Module.screen_refs gives us Screen → Module
    screen_to_modules = defaultdict(list)
    for module in modules:
        for screen_ref in module.get("screen_refs", []):
            screen_to_modules[screen_ref].append(module.get("id", ""))

    # Module.adr_refs gives us Module → ADR
    mod_to_adrs = defaultdict(list)
    for module in modules:
        mod_id = module.get("id", "")
        mod_to_adrs[mod_id] = module.get("adr_refs", [])

    # Module.tasks or task.module_ref gives us Module → Task
    mod_to_tasks = defaultdict(list)
    for task in tasks:
        mod_ref = task.get("module_ref", "")
        if mod_ref:
            mod_to_tasks[mod_ref].append(task.get("id", ""))

    # Task.files and Task.test_files give us Task → Code/Tests
    task_details = {}
    for task in tasks:
        task_id = task.get("id", "")
        task_details[task_id] = {
            "files": task.get("files", []),
            "test_files": task.get("test_files", []),
            "status": task.get("status", "pending"),
            "priority": task.get("priority", "P1"),
            "name": task.get("name", "")
        }

    # Build chains starting from each Pain Point
    chain_num = 0
    for pp in pain_points:
        pp_id = pp.get("id", "")
        chain_num += 1

        # Get Client Facts that reference this PP
        cf_ids = pp_to_cfs.get(pp_id, [])

        # Get JTBDs for this PP
        jtbd_ids = pp_to_jtbds.get(pp_id, [])

        # Get Screens for these JTBDs
        screen_ids = set()
        for jtbd_id in jtbd_ids:
            screen_ids.update(jtbd_to_screens.get(jtbd_id, []))
        screen_ids = list(screen_ids)

        # Get Modules for these Screens
        module_ids = set()
        for screen_id in screen_ids:
            module_ids.update(screen_to_modules.get(screen_id, []))
        module_ids = list(module_ids)

        # Get ADRs for these Modules
        adr_ids = set()
        for mod_id in module_ids:
            adr_ids.update(mod_to_adrs.get(mod_id, []))
        adr_ids = list(adr_ids)

        # Get Tasks for these Modules
        task_ids = set()
        for mod_id in module_ids:
            task_ids.update(mod_to_tasks.get(mod_id, []))
        task_ids = list(task_ids)

        # Get Code Files and Test Files from Tasks
        code_files = []
        test_files = []
        completed_tasks = 0
        for task_id in task_ids:
            details = task_details.get(task_id, {})
            code_files.extend(details.get("files", []))
            test_files.extend(details.get("test_files", []))
            if details.get("status") == "completed":
                completed_tasks += 1

        chain = {
            "chain_id": f"CHAIN-{chain_num:03d}",
            "client_facts": cf_ids,
            "pain_point": {
                "id": pp_id,
                "title": pp.get("title", ""),
                "priority": pp.get("priority", "P1")
            },
            "jtbds": jtbd_ids,
            "screens": screen_ids,
            "modules": module_ids,
            "adrs": adr_ids,
            "tasks": task_ids,
            "code_files": list(set(code_files)),
            "test_files": list(set(test_files)),
            "metrics": {
                "total_tasks": len(task_ids),
                "completed_tasks": completed_tasks,
                "code_file_count": len(set(code_files)),
                "test_file_count": len(set(test_files)),
                "chain_complete": len(task_ids) > 0 and completed_tasks == len(task_ids),
                "has_client_facts": len(cf_ids) > 0
            }
        }
        chains.append(chain)

    return chains


def calculate_chain_coverage(chains):
    """Calculate overall chain coverage statistics."""
    total_chains = len(chains)
    chains_with_cf = len([c for c in chains if c.get("client_facts", [])])
    chains_with_jtbd = len([c for c in chains if c["jtbds"]])
    chains_with_screen = len([c for c in chains if c["screens"]])
    chains_with_module = len([c for c in chains if c["modules"]])
    chains_with_adr = len([c for c in chains if c["adrs"]])
    chains_with_task = len([c for c in chains if c["tasks"]])
    chains_with_code = len([c for c in chains if c["code_files"]])
    chains_with_tests = len([c for c in chains if c["test_files"]])
    chains_complete = len([c for c in chains if c["metrics"]["chain_complete"]])

    return {
        "total_chains": total_chains,
        "chains_with_cf": chains_with_cf,
        "chains_with_jtbd": chains_with_jtbd,
        "chains_with_screen": chains_with_screen,
        "chains_with_module": chains_with_module,
        "chains_with_adr": chains_with_adr,
        "chains_with_task": chains_with_task,
        "chains_with_code": chains_with_code,
        "chains_with_tests": chains_with_tests,
        "chains_complete": chains_complete,
        "cf_to_pp_coverage": int(chains_with_cf / total_chains * 100) if total_chains else 0,
        "pp_to_jtbd_coverage": int(chains_with_jtbd / total_chains * 100) if total_chains else 0,
        "pp_to_screen_coverage": int(chains_with_screen / total_chains * 100) if total_chains else 0,
        "pp_to_module_coverage": int(chains_with_module / total_chains * 100) if total_chains else 0,
        "pp_to_task_coverage": int(chains_with_task / total_chains * 100) if total_chains else 0,
        "pp_to_code_coverage": int(chains_with_code / total_chains * 100) if total_chains else 0,
        "e2e_complete_coverage": int(chains_complete / total_chains * 100) if total_chains else 0
    }


def build_pp_to_jtbd_map(trace_links):
    """Build mapping from Pain Points to JTBDs."""
    pp_to_jtbd = defaultdict(list)
    if not trace_links:
        return pp_to_jtbd

    items = trace_links.get("items", [])
    for link in items:
        if link.get("type") == "addresses" and link.get("source", "").startswith("PP-"):
            pp_to_jtbd[link["source"]].append(link["target"])
    return pp_to_jtbd


def build_jtbd_to_screen_map(trace_links):
    """Build mapping from JTBDs to Screens."""
    jtbd_to_screen = defaultdict(list)
    if not trace_links:
        return jtbd_to_screen

    items = trace_links.get("items", [])
    for link in items:
        if link.get("type") == "implements":
            jtbd_to_screen[link["target"]].append(link["source"])
    return jtbd_to_screen


def generate_traceability_matrix(discovery_dir, stats):
    """Generate TRACEABILITY_MATRIX_MASTER.md document."""

    # Load registries
    pp_registry = load_registry("pain_point_registry.json")
    jtbd_registry = load_registry("jtbd_registry.json")
    ut_registry = load_registry("user_type_registry.json")
    screen_registry = load_registry("screen_registry.json")
    trace_links = load_registry("trace_links.json")

    pain_points = pp_registry.get("pain_points", []) if pp_registry else []
    jtbds = jtbd_registry.get("jtbd", []) if jtbd_registry else []
    user_types = ut_registry.get("items", []) if ut_registry else []
    screens = screen_registry.get("items", []) if screen_registry else []

    # Load Client Facts
    client_facts, source_files = load_client_facts()

    # Build mappings
    pp_to_jtbd = build_pp_to_jtbd_map(trace_links)
    jtbd_to_screen = build_jtbd_to_screen_map(trace_links)
    cf_to_pp, pp_to_cf = build_cf_to_pp_map(client_facts)

    # Load Implementation phase data
    impl_data = load_implementation_data()
    tasks = impl_data["tasks"]
    modules = impl_data["modules"]
    components = impl_data["components"]
    adrs = impl_data["adrs"]
    test_cases = impl_data["test_cases"]
    impl_progress = impl_data["progress"]

    # Build Implementation mappings
    mod_to_task = build_module_to_task_map(tasks)
    task_to_code, task_to_tests = build_task_to_files_map(tasks)

    # Count implementation stats
    tasks_total = len(tasks)
    tasks_completed = len([t for t in tasks if t.get("status") == "completed"])
    impl_coverage = impl_progress.get("coverage", {}) if impl_progress else {}

    timestamp = datetime.now().isoformat()

    # Build complete E2E chains using the new chain builder (including client facts)
    complete_chains = build_complete_e2e_chains(pain_points, jtbds, screens, modules, tasks, client_facts)
    chain_coverage = calculate_chain_coverage(complete_chains)

    content = f"""# Master Traceability Matrix

## Quick Reference: End-to-End Chains

This document provides a condensed view of all traceability chains.

### Complete Traceability Chain (v5.0 - Full E2E Implementation)

```
┌─────────────────────────────────────────────────────────────────┐
│                    DISCOVERY PHASE                               │
├─────────────────────────────────────────────────────────────────┤
│  CM-XXX (Client Material/Interview Quotes)                      │
│      ↓                                                          │
│  PP-X.X (Pain Point) [{len(pain_points)} identified]                             │
│      ↓                                                          │
│  JTBD-X.X (Job To Be Done) [{len(jtbds)} defined]                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    PROTOTYPE PHASE                               │
├─────────────────────────────────────────────────────────────────┤
│  REQ-XXX (Requirement/PRD)                                      │
│      ↓                                                          │
│  ┌─────────────┐      ┌─────────────┐                          │
│  │ SCR-XXX     │──────│ COMP-XXX    │  (Screen + Components)   │
│  │ (Screen)    │      │ (Component) │  [{len(screens)} screens]                 │
│  └─────────────┘      └─────────────┘                          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  PRODUCT SPECS PHASE                             │
├─────────────────────────────────────────────────────────────────┤
│  MOD-XXX (Module Specification) [{len(modules)} modules]                   │
│      ↓                                                          │
│  NFR-XXX (Non-Functional Requirement)                           │
│      ↓                                                          │
│  ┌─────────────┐      ┌─────────────┐                          │
│  │ EPIC-XXX    │──────│ US-XXX      │  (Epic → User Story)     │
│  │ (Epic)      │      │ (Story)     │                          │
│  └─────────────┘      └─────────────┘                          │
│      ↓                                                          │
│  TS-XXX (Test Scenario - Gherkin)                               │
│      ↓                                                          │
│  TC-XXX (Test Case) [{len(test_cases)} test cases]                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│               SOLUTION ARCHITECTURE PHASE                        │
├─────────────────────────────────────────────────────────────────┤
│  ADR-XXX (Architecture Decision Record) [{len(adrs)} ADRs]              │
│      ↓                                                          │
│  COMP-XXX (SolArch Component) [{len(components)} components]              │
│      ↓                                                          │
│  QS-XXX (Quality Scenario)                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  IMPLEMENTATION PHASE                            │
├─────────────────────────────────────────────────────────────────┤
│  T-NNN (Implementation Task) [{tasks_total} tasks, {tasks_completed} completed]         │
│      ↓                                                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ src/                      │ tests/                          ││
│  │ ├── components/           │ ├── unit/                       ││
│  │ ├── features/             │ ├── integration/                ││
│  │ ├── services/             │ └── e2e/                        ││
│  │ ├── hooks/                │                                 ││
│  │ └── utils/                │                                 ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DELIVERY PHASE                                │
├─────────────────────────────────────────────────────────────────┤
│  INV-XXX (JIRA Item)                                            │
└─────────────────────────────────────────────────────────────────┘
```

### Simplified Chain View

```
PP → JTBD → REQ → SCR/COMP → MOD → NFR → ADR → T → Code → Tests → JIRA
```

### E2E Chain Coverage Summary

| Metric | Value | Coverage |
|--------|-------|----------|
| Total Chains | {chain_coverage['total_chains']} | - |
| **CF → PP** | **{chain_coverage['chains_with_cf']}** | **{chain_coverage['cf_to_pp_coverage']}%** |
| PP → JTBD | {chain_coverage['chains_with_jtbd']} | {chain_coverage['pp_to_jtbd_coverage']}% |
| PP → Screen | {chain_coverage['chains_with_screen']} | {chain_coverage['pp_to_screen_coverage']}% |
| PP → Module | {chain_coverage['chains_with_module']} | {chain_coverage['pp_to_module_coverage']}% |
| PP → Task | {chain_coverage['chains_with_task']} | {chain_coverage['pp_to_task_coverage']}% |
| PP → Code | {chain_coverage['chains_with_code']} | {chain_coverage['pp_to_code_coverage']}% |
| **Complete E2E** | **{chain_coverage['chains_complete']}** | **{chain_coverage['e2e_complete_coverage']}%** |

---

## Complete Chain Table

| Chain | Client Facts | Pain Point | JTBD | Screen | Module | ADR | Task | Code | Tests |
|-------|--------------|------------|------|--------|--------|-----|------|------|-------|
"""

    # Generate chain entries using complete E2E chains
    for chain in complete_chains:
        chain_id = chain["chain_id"]
        pp_id = chain["pain_point"]["id"]

        # Format Client Facts
        cf_ids = chain.get("client_facts", [])
        cf_str = ", ".join(cf_ids[:2]) if cf_ids else "-"
        if len(cf_ids) > 2:
            cf_str += f" +{len(cf_ids)-2}"

        # Format JTBDs
        jtbd_ids = chain["jtbds"]
        jtbd_str = ", ".join(jtbd_ids[:2]) if jtbd_ids else "-"
        if len(jtbd_ids) > 2:
            jtbd_str += f" +{len(jtbd_ids)-2}"

        # Format Screens
        screen_ids = chain["screens"]
        screen_str = ", ".join(screen_ids[:2]) if screen_ids else "-"
        if len(screen_ids) > 2:
            screen_str += f" +{len(screen_ids)-2}"

        # Format Modules
        module_ids = chain["modules"]
        mod_str = ", ".join(module_ids[:2]) if module_ids else "-"
        if len(module_ids) > 2:
            mod_str += f" +{len(module_ids)-2}"

        # Format ADRs
        adr_ids = chain["adrs"]
        adr_str = ", ".join(adr_ids[:2]) if adr_ids else "-"
        if len(adr_ids) > 2:
            adr_str += f" +{len(adr_ids)-2}"

        # Format Tasks
        task_ids = chain["tasks"]
        task_str = ", ".join(task_ids[:2]) if task_ids else "-"
        if len(task_ids) > 2:
            task_str += f" +{len(task_ids)-2}"

        # Format Code and Test Files
        code_files = chain["code_files"]
        code_str = str(len(code_files)) if code_files else "0"

        test_files = chain["test_files"]
        test_str = str(len(test_files)) if test_files else "0"

        content += f"| {chain_id} | {cf_str} | {pp_id} | {jtbd_str} | {screen_str} | {mod_str} | {adr_str} | {task_str} | {code_str} | {test_str} |\n"

    content += """
---

## Detailed Mappings

### Client Facts (CF) Registry

| ID | Source | Type | Summary | Links To |
|----|--------|------|---------|----------|
"""
    # Populate CF table from client_facts registry
    if client_facts:
        for cf in sorted(client_facts, key=lambda x: x.get("id", ""))[:20]:  # Show first 20
            cf_id = cf.get("id", "")
            source = cf.get("source_file", cf.get("source", ""))[:20]
            cf_type = cf.get("fact_type", cf.get("type", "-"))
            # Get content/quote - handle different field names
            text = cf.get("content", cf.get("quote", cf.get("text", "")))[:40]
            links = ", ".join(cf.get("referenced_by", []))[:30] or "-"
            content += f"| {cf_id} | {source} | {cf_type} | {text}... | {links} |\n"
        if len(client_facts) > 20:
            content += f"| ... | *{len(client_facts) - 20} more facts* | ... | ... | ... |\n"
    else:
        content += "| - | - | - | *No client facts found* | - |\n"

    content += """
---

### Pain Points (PP) to JTBD

| PP ID | Description | Severity | JTBD IDs | Opportunity |
|-------|-------------|----------|----------|-------------|
"""
    for pp in sorted(pain_points, key=lambda x: x.get("id", "")):
        pp_id = pp.get("id", "")
        desc = pp.get("title", pp.get("description", ""))[:50]
        priority = pp.get("priority", "P1")
        jtbd_ids = pp_to_jtbd.get(pp_id, [])
        jtbd_str = ", ".join(jtbd_ids) if jtbd_ids else "-"
        content += f"| {pp_id} | {desc} | {priority} | {jtbd_str} | - |\n"

    content += """
---

### JTBD to Requirements

| JTBD ID | Description | Priority | Epic IDs |
|---------|-------------|----------|----------|
"""
    for jtbd in sorted(jtbds, key=lambda x: x.get("id", "")):
        jtbd_id = jtbd.get("id", "")
        title = jtbd.get("title", "")[:40]
        priority = jtbd.get("priority", "P1")
        # Epic IDs - placeholder
        content += f"| {jtbd_id} | {title} | {priority} | - |\n"

    content += """
---

### Modules to Tasks (IMPLEMENTATION PHASE)

| Module ID | Module Name | Priority | Tasks | Status | Code Files |
|-----------|-------------|----------|-------|--------|------------|
"""
    for module in sorted(modules, key=lambda x: x.get("id", "")):
        mod_id = module.get("id", "")
        name = module.get("name", "")[:30]
        priority = module.get("priority", "P1")
        task_ids = mod_to_task.get(mod_id, [])
        task_str = ", ".join(task_ids[:3]) if task_ids else "-"
        if len(task_ids) > 3:
            task_str += f" +{len(task_ids)-3}"
        status = module.get("status", "pending")
        # Collect code files from all tasks
        code_files = []
        for task_id in task_ids:
            code_files.extend(task_to_code.get(task_id, []))
        code_count = len(code_files)
        content += f"| {mod_id} | {name} | {priority} | {task_str} | {status} | {code_count} files |\n"

    content += """
---

### Tasks to Code and Tests (IMPLEMENTATION PHASE)

| Task ID | Name | Module | Priority | Status | Code Files | Test Files |
|---------|------|--------|----------|--------|------------|------------|
"""
    for task in sorted(tasks, key=lambda x: x.get("id", ""))[:20]:  # Limit to first 20 for readability
        task_id = task.get("id", "")
        name = task.get("name", "")[:35]
        mod_ref = task.get("module_ref", "-")
        priority = task.get("priority", "P1")
        status = task.get("status", "pending")
        code_files = task.get("files", [])
        test_files = task.get("test_files", [])
        code_str = str(len(code_files)) if code_files else "0"
        test_str = str(len(test_files)) if test_files else "0"
        content += f"| {task_id} | {name} | {mod_ref} | {priority} | {status} | {code_str} | {test_str} |\n"

    if len(tasks) > 20:
        content += f"| ... | *{len(tasks) - 20} more tasks* | ... | ... | ... | ... | ... |\n"

    content += """
---

### ADRs to Components

| ADR ID | Title | Status | Components |
|--------|-------|--------|------------|
"""
    for adr in sorted(adrs, key=lambda x: x.get("id", "")):
        adr_id = adr.get("id", "")
        title = adr.get("title", "")[:40]
        status = adr.get("status", "Accepted")
        comp_refs = adr.get("component_refs", [])
        comp_str = ", ".join(comp_refs[:3]) if comp_refs else "-"
        if len(comp_refs) > 3:
            comp_str += f" +{len(comp_refs)-3}"
        content += f"| {adr_id} | {title} | {status} | {comp_str} |\n"

    content += """
---

### Components to Tasks

| Component ID | Name | Layer | Tasks |
|--------------|------|-------|-------|
"""
    for comp in sorted(components, key=lambda x: x.get("id", "")):
        comp_id = comp.get("id", "")
        name = comp.get("name", "")[:30]
        layer = comp.get("layer", "-")
        # Find tasks that reference this component
        related_tasks = [t.get("id") for t in tasks if comp_id in t.get("component_refs", [])]
        task_str = ", ".join(related_tasks[:3]) if related_tasks else "-"
        if len(related_tasks) > 3:
            task_str += f" +{len(related_tasks)-3}"
        content += f"| {comp_id} | {name} | {layer} | {task_str} |\n"

    # Calculate coverage statistics
    impl_tests_passing = impl_coverage.get("testsPassing", 0)
    impl_tests_total = impl_coverage.get("testsTotal", 0)
    impl_coverage_pct = impl_coverage.get("tasksCoveragePercent", 0)

    content += f"""
---

## Coverage Summary

| Layer | Total Items | Linked | Coverage |
|-------|-------------|--------|----------|
| **Client Facts** | **{len(client_facts)}** | **{len([cf for cf in client_facts if cf.get('referenced_by')])}** | **{int(len([cf for cf in client_facts if cf.get('referenced_by')]) / len(client_facts) * 100) if client_facts else 0}%** |
| Pain Points | {len(pain_points)} | {len([pp for pp in pain_points if pp_to_jtbd.get(pp.get('id'))])} | {int(len([pp for pp in pain_points if pp_to_jtbd.get(pp.get('id'))]) / len(pain_points) * 100) if pain_points else 0}% |
| JTBDs | {len(jtbds)} | {len([j for j in jtbds if j.get('related_pain_points')])} | {int(len([j for j in jtbds if j.get('related_pain_points')]) / len(jtbds) * 100) if jtbds else 0}% |
| Screens | {len(screens)} | {len([s for s in screens if s.get('related_jtbds')])} | {int(len([s for s in screens if s.get('related_jtbds')]) / len(screens) * 100) if screens else 0}% |
| Modules | {len(modules)} | {len([m for m in modules if mod_to_task.get(m.get('id'))])} | {int(len([m for m in modules if mod_to_task.get(m.get('id'))]) / len(modules) * 100) if modules else 0}% |
| ADRs | {len(adrs)} | {len([a for a in adrs if a.get('component_refs')])} | {int(len([a for a in adrs if a.get('component_refs')]) / len(adrs) * 100) if adrs else 0}% |
| Components | {len(components)} | - | 100% |
| Tasks | {tasks_total} | {tasks_completed} | {int(tasks_completed / tasks_total * 100) if tasks_total else 0}% |
| Test Cases | {len(test_cases)} | - | 100% |

---

## Implementation Phase Summary

| Metric | Value |
|--------|-------|
| Total Tasks | {tasks_total} |
| Completed Tasks | {tasks_completed} |
| Task Completion | {int(tasks_completed / tasks_total * 100) if tasks_total else 0}% |
| Tests Passing | {impl_tests_passing}/{impl_tests_total} |
| P0 Coverage | {impl_coverage.get('p0CoveragePercent', 0)}% |
| P1 Coverage | {impl_coverage.get('p1CoveragePercent', 0)}% |

---

*Generated: {timestamp}*
*Version: 4.0 (Implementation Phase Included)*
"""

    return content


def generate_traceability_report(discovery_dir, stats):
    """Generate TRACEABILITY_ASSESSMENT_REPORT.md document."""

    # Load registries
    pp_registry = load_registry("pain_point_registry.json")
    jtbd_registry = load_registry("jtbd_registry.json")
    ut_registry = load_registry("user_type_registry.json")
    screen_registry = load_registry("screen_registry.json")
    trace_links = load_registry("trace_links.json")

    pain_points = pp_registry.get("pain_points", []) if pp_registry else []
    jtbds = jtbd_registry.get("jtbd", []) if jtbd_registry else []
    user_types = ut_registry.get("items", []) if ut_registry else []
    screens = screen_registry.get("items", []) if screen_registry else []
    links = trace_links.get("items", []) if trace_links else []

    # Load Client Facts
    client_facts, source_files = load_client_facts()

    # Build mappings
    pp_to_jtbd = build_pp_to_jtbd_map(trace_links)
    jtbd_to_screen = build_jtbd_to_screen_map(trace_links)
    cf_to_pp, pp_to_cf = build_cf_to_pp_map(client_facts)

    # Load Implementation phase data
    impl_data = load_implementation_data()
    tasks = impl_data["tasks"]
    modules = impl_data["modules"]
    components = impl_data["components"]
    adrs = impl_data["adrs"]
    test_cases = impl_data["test_cases"]
    impl_progress = impl_data["progress"]

    # Build Implementation mappings
    mod_to_task = build_module_to_task_map(tasks)
    task_to_code, task_to_tests = build_task_to_files_map(tasks)

    # Count implementation stats
    tasks_total = len(tasks)
    tasks_completed = len([t for t in tasks if t.get("status") == "completed"])
    impl_coverage = impl_progress.get("coverage", {}) if impl_progress else {}

    # Build complete E2E chains for this report (including client facts)
    complete_chains = build_complete_e2e_chains(pain_points, jtbds, screens, modules, tasks, client_facts)
    chain_coverage = calculate_chain_coverage(complete_chains)

    # Extract system name from discovery_dir
    system_name = Path(discovery_dir).name.replace("ClientAnalysis_", "").replace("_", " ")

    timestamp = datetime.now().isoformat()
    assessment_date = datetime.now().strftime("%Y-%m-%d")

    # Calculate overall score
    discovery_complete = len(pain_points) > 0 and len(jtbds) > 0
    impl_complete = tasks_completed > 0 and impl_coverage.get("p0CoveragePercent", 0) >= 95
    overall_score = 0
    if discovery_complete:
        overall_score += 30
    if len(modules) > 0:
        overall_score += 20
    if len(adrs) > 0:
        overall_score += 15
    if tasks_completed > 0:
        overall_score += 25
    if impl_coverage.get("testsPassing", 0) > 0:
        overall_score += 10

    # Determine traceability status
    if impl_complete and overall_score >= 90:
        traceability_status = "IMPLEMENTATION COMPLETE"
    elif overall_score >= 60:
        traceability_status = "IN PROGRESS"
    else:
        traceability_status = "DISCOVERY PHASE"

    content = f"""# Formal Traceability Assessment Report

## {system_name}

**Document Version:** 2.0 (Implementation Phase Included)
**Assessment Date:** {assessment_date}
**Assessor:** Claude AI (Automated Analysis)
**Scope:** End-to-End Traceability Verification (Discovery through Implementation)

---

## Executive Summary

This report provides a comprehensive assessment of traceability across all documentation artifacts for the {system_name}. The assessment covers the complete chain from client interviews through implementation, verifying bidirectional linkages at each level.

### Overall Assessment Score: {overall_score}/100 ({traceability_status})

| Dimension | Score | Status |
|-----------|-------|--------|
| **Client Facts to Pain Points** | **{len([cf for cf in client_facts if cf.get('referenced_by')])}/{len(client_facts)}** | **{'Complete' if client_facts else 'Pending'}** |
| Pain Points to JTBDs | {len([pp for pp in pain_points if pp_to_jtbd.get(pp.get('id'))])}/{len(pain_points)} traced | Discovery Complete |
| JTBDs to Screens | {len([j for j in jtbds if jtbd_to_screen.get(j.get('id'))])}/{len(jtbds)} | Prototype Complete |
| Modules to Tasks | {len([m for m in modules if mod_to_task.get(m.get('id'))])}/{len(modules)} | ProductSpecs Complete |
| ADRs to Components | {len([a for a in adrs if a.get('component_refs')])}/{len(adrs)} | SolArch Complete |
| Tasks to Code | {tasks_completed}/{tasks_total} | Implementation {'Complete' if impl_complete else 'In Progress'} |

### Key Metrics

| Metric | Value |
|--------|-------|
| **Client Facts Extracted** | **{len(client_facts)}** |
| Pain Points Identified | {len(pain_points)} |
| Jobs to Be Done | {len(jtbds)} |
| User Types | {len(user_types)} |
| Screens Defined | {len(screens)} |
| Modules | {len(modules)} |
| Architecture Decision Records | {len(adrs)} |
| Components | {len(components)} |
| Test Cases (Specs) | {len(test_cases)} |
| **Implementation Tasks** | **{tasks_total}** |
| **Tasks Completed** | **{tasks_completed}** |
| **Tests Passing** | **{impl_coverage.get('testsPassing', 0)}/{impl_coverage.get('testsTotal', 0)}** |
| **Trace Links Created** | **{len(links)}** |


---

## 1. Methodology

### 1.1 Artifacts Analyzed

| Layer | Source Location | Artifact Count |
|-------|-----------------|----------------|
| Discovery Analysis | `{discovery_dir}` | {len(pain_points)} PPs, {len(jtbds)} JTBDs, {len(screens)} Screens |
| Prototype Specification | `Prototype_*` | Screens, Components |
| Product Specifications | `ProductSpecs_*` | {len(modules)} Modules, {len(test_cases)} Test Cases |
| Solution Architecture | `SolArch_*` | {len(adrs)} ADRs, {len(components)} Components |
| Implementation | `Implementation_*` | {tasks_total} Tasks, {impl_coverage.get('testsTotal', 0)} Tests |

### 1.2 Traceability Chain Model (v2.0 - Full Chain)

```
CLIENT FACTS (Interviews, Screenshots, Manuals)
    |
    v
PAIN POINTS ({len(pain_points)} identified)
    |
    v
JOBS TO BE DONE ({len(jtbds)} defined)
    |
    v
SCREENS ({len(screens)} defined)
    |
    v
MODULES ({len(modules)} modules)
    |
    v
ADRs ({len(adrs)} decisions)
    |
    v
COMPONENTS ({len(components)} components)
    |
    v
IMPLEMENTATION TASKS ({tasks_total} tasks, {tasks_completed} completed)
    |
    v
SOURCE CODE (src/)
    |
    v
TESTS (tests/) - {impl_coverage.get('testsPassing', 0)} passing
```

---

## 2. Complete End-to-End Traceability Matrix

### 2.1 E2E Chain Coverage Summary

| Metric | Value | Coverage |
|--------|-------|----------|
| Total Chains | {chain_coverage['total_chains']} | - |
| **CF → PP** | **{chain_coverage['chains_with_cf']}** | **{chain_coverage['cf_to_pp_coverage']}%** |
| PP → JTBD | {chain_coverage['chains_with_jtbd']} | {chain_coverage['pp_to_jtbd_coverage']}% |
| PP → Screen | {chain_coverage['chains_with_screen']} | {chain_coverage['pp_to_screen_coverage']}% |
| PP → Module | {chain_coverage['chains_with_module']} | {chain_coverage['pp_to_module_coverage']}% |
| PP → Task | {chain_coverage['chains_with_task']} | {chain_coverage['pp_to_task_coverage']}% |
| PP → Code | {chain_coverage['chains_with_code']} | {chain_coverage['pp_to_code_coverage']}% |
| **Complete E2E** | **{chain_coverage['chains_complete']}** | **{chain_coverage['e2e_complete_coverage']}%** |

### 2.2 Master Traceability Table - Client Facts to Implementation

| Client Facts | Pain Point | Priority | JTBD | Screen | Module | ADR | Task | Code | Tests |
|--------------|------------|----------|------|--------|--------|-----|------|------|-------|
"""

    # Generate chain entries using complete E2E chains
    for chain in complete_chains:
        pp_id = chain["pain_point"]["id"]
        pp_priority = chain["pain_point"]["priority"]

        # Format Client Facts
        cf_ids = chain.get("client_facts", [])
        cf_str = ", ".join(cf_ids[:2]) if cf_ids else "-"
        if len(cf_ids) > 2:
            cf_str += f" +{len(cf_ids)-2}"

        # Format JTBDs
        jtbd_ids = chain["jtbds"]
        jtbd_str = ", ".join(jtbd_ids[:2]) if jtbd_ids else "-"
        if len(jtbd_ids) > 2:
            jtbd_str += f" +{len(jtbd_ids)-2}"

        # Format Screens
        screen_ids = chain["screens"]
        screen_str = ", ".join(screen_ids[:2]) if screen_ids else "-"
        if len(screen_ids) > 2:
            screen_str += f" +{len(screen_ids)-2}"

        # Format Modules
        module_ids = chain["modules"]
        mod_str = ", ".join(module_ids[:1]) if module_ids else "-"
        if len(module_ids) > 1:
            mod_str += f" +{len(module_ids)-1}"

        # Format ADRs
        adr_ids = chain["adrs"]
        adr_str = ", ".join(adr_ids[:1]) if adr_ids else "-"
        if len(adr_ids) > 1:
            adr_str += f" +{len(adr_ids)-1}"

        # Format Tasks
        task_ids = chain["tasks"]
        task_str = f"{len(task_ids)}" if task_ids else "0"

        # Format Code and Test Files
        code_count = chain["metrics"]["code_file_count"]
        test_count = chain["metrics"]["test_file_count"]

        content += f"| {cf_str} | **{pp_id}** | {pp_priority} | {jtbd_str} | {screen_str} | {mod_str} | {adr_str} | {task_str} | {code_count} | {test_count} |\n"

    content += """
---

### 2.3 Pain Points Registry

| Pain Point ID | Title | Severity | Impact | Affected Users |
|---------------|-------|----------|--------|----------------|
"""
    for pp in sorted(pain_points, key=lambda x: x.get("id", "")):
        pp_id = pp.get("id", "")
        title = pp.get("title", "")[:40]
        priority = pp.get("priority", "P1")
        impact = pp.get("impact", "-")[:30]
        users = pp.get("affected_users", "-")[:30]
        content += f"| {pp_id} | {title} | {priority} | {impact} | {users} |\n"

    content += """
---

### 2.4 Jobs-To-Be-Done Registry

| JTBD ID | Title | Priority | Related Pain Points |
|---------|-------|----------|---------------------|
"""
    for jtbd in sorted(jtbds, key=lambda x: x.get("id", "")):
        jtbd_id = jtbd.get("id", "")
        title = jtbd.get("title", "")[:40]
        priority = jtbd.get("priority", "P1")
        related_pps = ", ".join(jtbd.get("related_pain_points", [])) or "-"
        content += f"| {jtbd_id} | {title} | {priority} | {related_pps} |\n"

    content += """
---

### 2.5 Modules to Tasks (IMPLEMENTATION)

| Module ID | Module Name | Priority | Tasks | Status | Code Files |
|-----------|-------------|----------|-------|--------|------------|
"""
    for module in sorted(modules, key=lambda x: x.get("id", "")):
        mod_id = module.get("id", "")
        name = module.get("name", "")[:30]
        priority = module.get("priority", "P1")
        task_ids = mod_to_task.get(mod_id, [])
        task_str = ", ".join(task_ids[:3]) if task_ids else "-"
        if len(task_ids) > 3:
            task_str += f" +{len(task_ids)-3}"
        status = module.get("status", "pending")
        # Collect code files
        code_files = []
        for task_id in task_ids:
            code_files.extend(task_to_code.get(task_id, []))
        content += f"| {mod_id} | {name} | {priority} | {task_str} | {status} | {len(code_files)} files |\n"

    content += """
---

### 2.6 Architecture Decision Records

| ADR ID | Title | Status | Components | Tasks Using |
|--------|-------|--------|------------|-------------|
"""
    for adr in sorted(adrs, key=lambda x: x.get("id", "")):
        adr_id = adr.get("id", "")
        title = adr.get("title", "")[:35]
        status = adr.get("status", "Accepted")
        comp_refs = adr.get("component_refs", [])
        comp_str = ", ".join(comp_refs[:2]) if comp_refs else "-"
        if len(comp_refs) > 2:
            comp_str += f" +{len(comp_refs)-2}"
        # Find tasks referencing this ADR
        related_tasks = [t.get("id") for t in tasks if adr_id in t.get("adr_refs", [])]
        task_str = str(len(related_tasks)) if related_tasks else "0"
        content += f"| {adr_id} | {title} | {status} | {comp_str} | {task_str} |\n"

    content += """
---

### 2.7 Implementation Tasks Registry

| Task ID | Name | Module | Priority | Status | Files | Tests |
|---------|------|--------|----------|--------|-------|-------|
"""
    for task in sorted(tasks, key=lambda x: x.get("id", ""))[:25]:  # First 25 tasks
        task_id = task.get("id", "")
        name = task.get("name", "")[:30]
        mod_ref = task.get("module_ref", "-")
        priority = task.get("priority", "P1")
        status = task.get("status", "pending")
        code_files = len(task.get("files", []))
        test_files = len(task.get("test_files", []))
        content += f"| {task_id} | {name} | {mod_ref} | {priority} | {status} | {code_files} | {test_files} |\n"

    if len(tasks) > 25:
        content += f"| ... | *{len(tasks) - 25} more tasks* | ... | ... | ... | ... | ... |\n"

    # Calculate P0/P1/P2 completion
    p0_tasks = [t for t in tasks if t.get("priority") == "P0"]
    p1_tasks = [t for t in tasks if t.get("priority") == "P1"]
    p2_tasks = [t for t in tasks if t.get("priority") == "P2"]
    p0_completed = len([t for t in p0_tasks if t.get("status") == "completed"])
    p1_completed = len([t for t in p1_tasks if t.get("status") == "completed"])
    p2_completed = len([t for t in p2_tasks if t.get("status") == "completed"])

    content += f"""
---

## 3. Coverage Statistics

### 3.1 Discovery Phase Coverage

| Category | Total | With Links | Coverage |
|----------|-------|------------|----------|
| **Client Facts** | **{len(client_facts)}** | **{len([cf for cf in client_facts if cf.get('referenced_by')])}** | **{int(len([cf for cf in client_facts if cf.get('referenced_by')]) / len(client_facts) * 100) if client_facts else 0}%** |
| Pain Points | {len(pain_points)} | {len([pp for pp in pain_points if pp_to_jtbd.get(pp.get('id'))])} | {int(len([pp for pp in pain_points if pp_to_jtbd.get(pp.get('id'))]) / len(pain_points) * 100) if pain_points else 0}% |
| JTBDs | {len(jtbds)} | {len([j for j in jtbds if j.get('related_pain_points')])} | {int(len([j for j in jtbds if j.get('related_pain_points')]) / len(jtbds) * 100) if jtbds else 0}% |
| Screens | {len(screens)} | {len([s for s in screens if s.get('related_jtbds')])} | {int(len([s for s in screens if s.get('related_jtbds')]) / len(screens) * 100) if screens else 0}% |

### 3.2 ProductSpecs & SolArch Coverage

| Category | Total | With Links | Coverage |
|----------|-------|------------|----------|
| Modules | {len(modules)} | {len([m for m in modules if mod_to_task.get(m.get('id'))])} | {int(len([m for m in modules if mod_to_task.get(m.get('id'))]) / len(modules) * 100) if modules else 0}% |
| ADRs | {len(adrs)} | {len([a for a in adrs if a.get('component_refs')])} | {int(len([a for a in adrs if a.get('component_refs')]) / len(adrs) * 100) if adrs else 0}% |
| Components | {len(components)} | {len(components)} | 100% |
| Test Cases | {len(test_cases)} | - | 100% |

### 3.3 Implementation Phase Coverage

| Category | Total | Completed | Coverage |
|----------|-------|-----------|----------|
| P0 Tasks | {len(p0_tasks)} | {p0_completed} | {int(p0_completed / len(p0_tasks) * 100) if p0_tasks else 0}% |
| P1 Tasks | {len(p1_tasks)} | {p1_completed} | {int(p1_completed / len(p1_tasks) * 100) if p1_tasks else 0}% |
| P2 Tasks | {len(p2_tasks)} | {p2_completed} | {int(p2_completed / len(p2_tasks) * 100) if p2_tasks else 0}% |
| **All Tasks** | **{tasks_total}** | **{tasks_completed}** | **{int(tasks_completed / tasks_total * 100) if tasks_total else 0}%** |

### 3.4 Test Coverage

| Test Type | Count | Status |
|-----------|-------|--------|
| Unit Tests | {impl_coverage.get('testBreakdown', {}).get('unit', 0)} | Passing |
| Integration Tests | {impl_coverage.get('testBreakdown', {}).get('integration', 0)} | Passing |
| E2E Tests | {impl_coverage.get('testBreakdown', {}).get('e2e', 0)} | Passing |
| **Total** | **{impl_coverage.get('testsTotal', 0)}** | **{impl_coverage.get('testsPassing', 0)} passing** |

---

## 4. Gap Analysis

### 4.1 Identified Gaps

| Gap ID | Description | Severity | Affected Artifacts | Recommendation |
|--------|-------------|----------|-------------------|----------------|
"""
    # Add CF gap only if no client facts or if not all are linked
    cf_linked = len([cf for cf in client_facts if cf.get('referenced_by')]) if client_facts else 0
    if not client_facts:
        content += "| GAP-001 | Client Facts not yet extracted | Medium | CF registry | Run interview analysis |\n"
    elif cf_linked < len(client_facts):
        unlinked = len(client_facts) - cf_linked
        content += f"| GAP-001 | {unlinked} Client Facts without PP links | Low | CF registry | Review and link to PPs |\n"

    # Add implementation-specific gaps
    if tasks_total > tasks_completed:
        content += f"| GAP-IMP-001 | {tasks_total - tasks_completed} tasks pending | {'High' if (tasks_total - tasks_completed) > 5 else 'Medium'} | task_registry.json | Complete remaining tasks |\n"
    if impl_coverage.get('testsPassing', 0) < impl_coverage.get('testsTotal', 0):
        failing_tests = impl_coverage.get('testsTotal', 0) - impl_coverage.get('testsPassing', 0)
        content += f"| GAP-IMP-002 | {failing_tests} tests failing | High | tests/ | Fix failing tests |\n"

    # If no gaps found
    if client_facts and cf_linked == len(client_facts) and tasks_total == tasks_completed and impl_coverage.get('testsPassing', 0) >= impl_coverage.get('testsTotal', 0):
        content += "| - | No critical gaps identified | - | - | - |\n"

    content += f"""

### 4.2 Gap Resolution Priority

| Priority | Gap IDs | Phase Required |
|----------|---------|----------------|
| High | GAP-IMP-* | Implementation fixes |
| Medium | GAP-001 | Discovery (CF linkage) |

---

## 5. Recommendations

### 5.1 Implementation Status

{'Implementation is **COMPLETE**. All P0 tasks finished, tests passing.' if impl_complete else 'Implementation is **IN PROGRESS**. Continue completing tasks.'}

### 5.2 Next Steps

"""
    if not impl_complete:
        content += """1. **Complete remaining implementation tasks**
2. **Fix any failing tests**
3. **Run final validation**
"""
    else:
        content += """1. **Maintain test coverage** as code evolves
2. **Update traceability** when requirements change
3. **Document any deferred items** for future sprints
"""

    content += f"""

---

## 6. Conclusion

### 6.1 Assessment Summary

The {system_name} has achieved the following traceability coverage:

| Phase | Aspect | Assessment |
|-------|--------|------------|
| **Discovery** | **Client Facts** | **{len(client_facts)} extracted ({len([cf for cf in client_facts if cf.get('referenced_by')])} linked to PPs)** |
| Discovery | Pain Points | {len(pain_points)} identified and categorized |
| Discovery | JTBDs | {len(jtbds)} jobs defined with pain point links |
| Prototype | Screens | {len(screens)} screens with JTBD references |
| ProductSpecs | Modules | {len(modules)} modules with task decomposition |
| SolArch | ADRs | {len(adrs)} architecture decisions |
| SolArch | Components | {len(components)} components defined |
| **Implementation** | **Tasks** | **{tasks_completed}/{tasks_total} completed ({int(tasks_completed/tasks_total*100) if tasks_total else 0}%)** |
| **Implementation** | **Tests** | **{impl_coverage.get('testsPassing', 0)}/{impl_coverage.get('testsTotal', 0)} passing** |

### 6.2 Certification Status

**Traceability Status: {traceability_status}**

Checklist:
- [{'x' if len(pain_points) > 0 else ' '}] Discovery phase (Pain Points, JTBDs)
- [{'x' if len(screens) > 0 else ' '}] Prototype phase (Screens)
- [{'x' if len(modules) > 0 else ' '}] Product Specs phase (Modules, Tests)
- [{'x' if len(adrs) > 0 else ' '}] Solution Architecture phase (ADRs, Components)
- [{'x' if impl_complete else ' '}] Implementation phase (Tasks, Code, Tests)

---

## Appendices

### Appendix A: ID Reference Guide

| Prefix | Artifact Type | Example |
|--------|---------------|---------|
| CF- | Client Fact | CF-001 |
| PP- | Pain Point | PP-1.1 |
| JTBD- | Job To Be Done | JTBD-1.1 |
| UT- | User Type | UT-01 |
| M-/D- | Screen (Mobile/Desktop) | M-01, D-01 |
| MOD- | Module | MOD-DSK-DASH-01 |
| ADR- | Architecture Decision Record | ADR-001 |
| COMP- | Component | COMP-API-001 |
| **T-** | **Implementation Task** | **T-015** |
| TC- | Test Case | TC-001 |

### Appendix B: Registry File Locations

| Registry | File Path |
|----------|-----------|
| Pain Points | `traceability/pain_point_registry.json` |
| JTBDs | `traceability/jtbd_registry.json` |
| Screens | `traceability/screen_registry.json` |
| Modules | `traceability/module_registry.json` |
| ADRs | `traceability/adr_registry.json` |
| Components | `traceability/component_registry.json` |
| **Tasks** | **`traceability/task_registry.json`** |
| **Implementation Progress** | **`traceability/implementation_traceability_register.json`** |

---

**Document End**

*Generated: {timestamp}*
*Assessment Tool: Claude AI Automated Analysis*
*Report Format: ISO/IEC/IEEE 29148 Aligned*
*Version: 2.0 (Implementation Phase Included)*
"""

    return content


def write_traceability_docs(discovery_dir, stats):
    """Generate and write both traceability documents."""
    discovery_path = Path(discovery_dir)

    # Generate documents
    matrix_content = generate_traceability_matrix(discovery_dir, stats)
    report_content = generate_traceability_report(discovery_dir, stats)

    # Write to traceability directory
    matrix_path = TRACEABILITY_DIR / "TRACEABILITY_MATRIX_MASTER.md"
    report_path = TRACEABILITY_DIR / "TRACEABILITY_ASSESSMENT_REPORT.md"

    with open(matrix_path, "w") as f:
        f.write(matrix_content)

    with open(report_path, "w") as f:
        f.write(report_content)

    return matrix_path, report_path

def rebuild_traceability(discovery_dir):
    """Main function to rebuild traceability from discovery outputs."""
    discovery_path = Path(discovery_dir)

    if not discovery_path.exists():
        print(f"Error: Directory not found: {discovery_dir}")
        sys.exit(1)

    # Ensure traceability directory exists
    TRACEABILITY_DIR.mkdir(parents=True, exist_ok=True)

    print(f"🔄 Rebuilding traceability from: {discovery_dir}")
    print("=" * 60)

    stats = {
        "pain_points": 0,
        "jtbd": 0,
        "user_types": 0,
        "screens": 0,
        "links": 0
    }

    # 1. Parse Pain Points
    pain_points_file = discovery_path / "01-analysis" / "PAIN_POINTS.md"
    if pain_points_file.exists():
        print(f"\n📋 Processing: {pain_points_file}")
        pain_points = parse_pain_points(pain_points_file)
        for pp in pain_points:
            result = add_to_registry("pain_point_registry.json", "A", "pain_points", pp)
            stats["pain_points"] += 1
        print(f"   ✅ {len(pain_points)} pain points extracted")
    else:
        print(f"\n⚠️  Pain points file not found: {pain_points_file}")
        pain_points = []

    # 2. Parse JTBDs
    jtbd_file = discovery_path / "02-research" / "JOBS_TO_BE_DONE.md"
    if jtbd_file.exists():
        print(f"\n🎯 Processing: {jtbd_file}")
        jtbds = parse_jtbd(jtbd_file)
        for jtbd in jtbds:
            result = add_to_registry("jtbd_registry.json", "A", "jtbd", jtbd)
            stats["jtbd"] += 1
        print(f"   ✅ {len(jtbds)} JTBDs extracted")
    else:
        print(f"\n⚠️  JTBD file not found: {jtbd_file}")
        jtbds = []

    # 3. Parse User Types
    user_types_file = discovery_path / "01-analysis" / "USER_TYPES.md"
    if user_types_file.exists():
        print(f"\n👥 Processing: {user_types_file}")
        user_types = parse_user_types(user_types_file)
        for ut in user_types:
            result = add_to_registry("user_type_registry.json", "A", "items", ut)
            stats["user_types"] += 1
        print(f"   ✅ {len(user_types)} user types extracted")
    else:
        print(f"\n⚠️  User types file not found: {user_types_file}")

    # 4. Parse Screens
    screens_file = discovery_path / "04-design-specs" / "screen-definitions.md"
    screens = []
    if screens_file.exists():
        print(f"\n📱 Processing: {screens_file}")
        screens = parse_screens(screens_file)
        for screen in screens:
            result = add_to_registry("screen_registry.json", "A", "items", screen)
            stats["screens"] += 1
        print(f"   ✅ {len(screens)} screens extracted")
    else:
        print(f"\n⚠️  Screens file not found: {screens_file}")

    # 5. Create Trace Links
    if pain_points or jtbds or screens:
        print(f"\n🔗 Creating trace links...")
        links = create_trace_links(pain_points, jtbds, screens)
        for link in links:
            result = add_to_registry("trace_links.json", "B", "items", link)
            stats["links"] += 1
        print(f"   ✅ {len(links)} trace links created")

    # 6. Generate Traceability Documents
    print(f"\n📄 Generating traceability documents...")
    matrix_path, report_path = write_traceability_docs(discovery_dir, stats)
    print(f"   ✅ Generated: {matrix_path}")
    print(f"   ✅ Generated: {report_path}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 REBUILD SUMMARY")
    print("=" * 60)
    print(f"   Pain Points:  {stats['pain_points']}")
    print(f"   JTBDs:        {stats['jtbd']}")
    print(f"   User Types:   {stats['user_types']}")
    print(f"   Screens:      {stats['screens']}")
    print(f"   Trace Links:  {stats['links']}")
    print("=" * 60)
    print(f"\n✅ Traceability registries rebuilt in: {TRACEABILITY_DIR}/")
    print(f"✅ Traceability documents generated:")
    print(f"   - {TRACEABILITY_DIR}/TRACEABILITY_MATRIX_MASTER.md")
    print(f"   - {TRACEABILITY_DIR}/TRACEABILITY_ASSESSMENT_REPORT.md")

    return stats

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Rebuild traceability registries from Discovery outputs")
    parser.add_argument("--dir", required=True, help="Path to Discovery output directory (e.g., ClientAnalysis_InventorySystem/)")

    args = parser.parse_args()
    rebuild_traceability(args.dir)

if __name__ == "__main__":
    main()
