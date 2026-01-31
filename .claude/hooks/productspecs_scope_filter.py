#!/usr/bin/env python3
"""
ProductSpecs Scope Filter
Implements 7 entry point types for granular module generation with fuzzy matching
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from difflib import get_close_matches


def load_json(filepath: str) -> dict:
    """Load JSON file with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON file {filepath}: {e}", file=sys.stderr)
        return {}


def fuzzy_match_feature(feature_input: str, module_ids: List[str], threshold: float = 0.6) -> List[str]:
    """
    Fuzzy match feature name against module IDs

    Args:
        feature_input: User input feature name (e.g., "SEARCH", "search", "srch")
        module_ids: List of module IDs (e.g., ["MOD-INV-SEARCH-01", "MOD-INV-REPORT-01"])
        threshold: Minimum similarity threshold (0.0 to 1.0)

    Returns:
        List of matched module IDs
    """
    feature_upper = feature_input.upper()

    # Extract feature parts from module IDs (format: MOD-{APP}-{FEATURE}-{NN})
    feature_map = {}
    for module_id in module_ids:
        parts = module_id.split('-')
        if len(parts) >= 3:
            feature_part = parts[2]  # e.g., "SEARCH" from "MOD-INV-SEARCH-01"
            if feature_part not in feature_map:
                feature_map[feature_part] = []
            feature_map[feature_part].append(module_id)

    # Exact match first
    if feature_upper in feature_map:
        return feature_map[feature_upper]

    # Fuzzy match
    feature_names = list(feature_map.keys())
    matches = get_close_matches(feature_upper, feature_names, n=5, cutoff=threshold)

    if not matches:
        return []

    # Return modules for all matched features
    matched_modules = []
    for match in matches:
        matched_modules.extend(feature_map[match])

    return matched_modules


def filter_scope(system_name: str, flags: Dict[str, any]) -> Dict[str, any]:
    """
    Filter module scope based on entry point flags

    Args:
        system_name: System name (e.g., "InventorySystem")
        flags: Dict with keys: module, feature, screen, persona, subsystem, layer, quality_critical

    Returns:
        Dict with keys: type, value, modules, total_modules, quality_critical, errors, warnings
    """
    # Load registries
    requirements_path = Path("traceability/requirements_registry.json")
    module_registry_path = Path(f"traceability/{system_name}_module_registry.json")

    # Fallback to generic module_registry.json if system-specific doesn't exist
    if not module_registry_path.exists():
        module_registry_path = Path("traceability/module_registry.json")

    requirements = load_json(str(requirements_path))
    module_registry = load_json(str(module_registry_path))

    if not isinstance(module_registry, list):
        # Handle case where registry is a dict with "modules" key
        module_registry = module_registry.get("modules", [])

    errors = []
    warnings = []

    # Validate module registry exists
    if not module_registry:
        errors.append("Module registry is empty or missing. Run ProductSpecs first to generate modules.")
        return {
            "type": "error",
            "value": None,
            "modules": [],
            "total_modules": 0,
            "quality_critical": flags.get("quality_critical", False),
            "errors": errors,
            "warnings": warnings
        }

    # Apply filter based on flag priority
    modules = []
    filter_type = "system"
    filter_value = system_name

    if flags.get("module"):
        # Module-level: exact match
        filter_type = "module"
        filter_value = flags["module"]
        modules = [m for m in module_registry if m.get("id") == flags["module"]]

        if not modules:
            errors.append(f"Module '{flags['module']}' not found. Available modules: {', '.join([m.get('id', '') for m in module_registry[:5]])}...")

    elif flags.get("feature"):
        # Feature-level: fuzzy match
        filter_type = "feature"
        filter_value = flags["feature"]

        module_ids = [m.get("id") for m in module_registry if m.get("id")]
        matched_ids = fuzzy_match_feature(flags["feature"], module_ids)

        if matched_ids:
            modules = [m for m in module_registry if m.get("id") in matched_ids]
            if len(matched_ids) < len([m.get("id") for m in modules]):
                # Fuzzy match found multiple features
                matched_features = set()
                for module_id in matched_ids:
                    parts = module_id.split('-')
                    if len(parts) >= 3:
                        matched_features.add(parts[2])
                warnings.append(f"Fuzzy match: '{flags['feature']}' matched features: {', '.join(matched_features)}")
        else:
            errors.append(f"No modules found for feature '{flags['feature']}'. Try: {', '.join(set([m.get('id', '').split('-')[2] for m in module_registry if '-' in m.get('id', '')]))}")

    elif flags.get("screen"):
        # Screen-level: modules linked to screen
        filter_type = "screen"
        filter_value = flags["screen"]
        modules = [m for m in module_registry
                   if flags["screen"] in m.get("sources", {}).get("screens", [])]

        if not modules:
            errors.append(f"No modules found for screen '{flags['screen']}'")

    elif flags.get("persona"):
        # Persona-level: modules used by persona
        filter_type = "persona"
        filter_value = flags["persona"]
        modules = [m for m in module_registry
                   if flags["persona"].lower() in [p.lower() for p in m.get("personas", [])]]

        if not modules:
            errors.append(f"No modules found for persona '{flags['persona']}'")

    elif flags.get("subsystem"):
        # Subsystem-level: modules in subsystem
        filter_type = "subsystem"
        filter_value = flags["subsystem"]
        modules = [m for m in module_registry
                   if m.get("subsystem", "").lower() == flags["subsystem"].lower()]

        if not modules:
            errors.append(f"No modules found for subsystem '{flags['subsystem']}'")

    elif flags.get("layer"):
        # Layer-level: modules in layer
        filter_type = "layer"
        filter_value = flags["layer"]
        valid_layers = ["frontend", "backend", "middleware", "database"]

        if flags["layer"].lower() not in valid_layers:
            errors.append(f"Invalid layer '{flags['layer']}'. Valid layers: {', '.join(valid_layers)}")
        else:
            modules = [m for m in module_registry
                       if m.get("layer", "").lower() == flags["layer"].lower()]

            if not modules:
                errors.append(f"No modules found for layer '{flags['layer']}'")

    else:
        # System-level: all modules (default)
        filter_type = "system"
        filter_value = system_name
        modules = module_registry

    # Add VP review flags
    for module in modules:
        module["needs_vp_review"] = (
            flags.get("quality_critical", False) or  # --quality critical
            module.get("priority") == "P0"  # Always review P0
        )

    # Generate summary
    if modules:
        p0_count = len([m for m in modules if m.get("priority") == "P0"])
        p1_count = len([m for m in modules if m.get("priority") == "P1"])
        p2_count = len([m for m in modules if m.get("priority") == "P2"])

        warnings.append(f"Scope: {len(modules)} modules (P0: {p0_count}, P1: {p1_count}, P2: {p2_count})")

    return {
        "type": filter_type,
        "value": filter_value,
        "modules": modules,
        "total_modules": len(modules),
        "quality_critical": flags.get("quality_critical", False),
        "errors": errors,
        "warnings": warnings
    }


def main():
    parser = argparse.ArgumentParser(
        description="ProductSpecs Scope Filter - Filter modules by entry point",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Module-level entry point
  %(prog)s InventorySystem --module MOD-INV-SEARCH-01

  # Feature-level entry point (with fuzzy matching)
  %(prog)s InventorySystem --feature SEARCH
  %(prog)s InventorySystem --feature srch  # fuzzy match

  # Screen-level entry point
  %(prog)s InventorySystem --screen SCR-003

  # Persona-level entry point
  %(prog)s InventorySystem --persona admin

  # Subsystem-level entry point
  %(prog)s InventorySystem --subsystem middleware

  # Layer-level entry point
  %(prog)s InventorySystem --layer frontend

  # Quality critical flag (all modules get VP review)
  %(prog)s InventorySystem --quality critical

  # System-level (default - all modules)
  %(prog)s InventorySystem
        """
    )

    parser.add_argument("system_name", help="System name (e.g., InventorySystem)")
    parser.add_argument("--module", help="Generate single module (e.g., MOD-INV-SEARCH-01)")
    parser.add_argument("--feature", help="Generate all modules for a feature (e.g., SEARCH)")
    parser.add_argument("--screen", help="Generate modules for a screen (e.g., SCR-003)")
    parser.add_argument("--persona", help="Generate modules for a persona (e.g., admin)")
    parser.add_argument("--subsystem", help="Generate modules in a subsystem (e.g., middleware)")
    parser.add_argument("--layer",
                        choices=["frontend", "backend", "middleware", "database"],
                        help="Generate modules in a layer")
    parser.add_argument("--quality",
                        choices=["critical"],
                        help="Enable VP review for ALL modules (P0, P1, P2)")
    parser.add_argument("--output",
                        default="_state/filtered_scope.json",
                        help="Output file path (default: _state/filtered_scope.json)")

    args = parser.parse_args()

    # Build flags dict
    flags = {
        "module": args.module,
        "feature": args.feature,
        "screen": args.screen,
        "persona": args.persona,
        "subsystem": args.subsystem,
        "layer": args.layer,
        "quality_critical": (args.quality == "critical")
    }

    # Filter scope
    result = filter_scope(args.system_name, flags)

    # Write result to file
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n{'='*70}")
    print(f"  PRODUCTSPECS SCOPE FILTER")
    print(f"{'='*70}\n")

    print(f"  System:       {args.system_name}")
    print(f"  Entry Point:  {result['type']}-level")
    print(f"  Filter Value: {result['value']}")
    print(f"  Quality Mode: {'CRITICAL' if result['quality_critical'] else 'Standard'}")
    print()

    # Print warnings
    for warning in result.get("warnings", []):
        print(f"  ⚠️  {warning}")

    # Print errors
    if result.get("errors"):
        print()
        for error in result["errors"]:
            print(f"  ❌ {error}")
        print()
        print(f"{'='*70}\n")
        sys.exit(1)

    # Success summary
    print()
    print(f"  ✅ Filtered Scope: {result['total_modules']} modules")

    if result['total_modules'] > 0:
        print()
        print(f"  Modules:")
        for i, module in enumerate(result['modules'][:10], 1):
            priority = module.get('priority', 'N/A')
            needs_vp = '🔍' if module.get('needs_vp_review') else '  '
            print(f"    {i}. {needs_vp} {module.get('id', 'N/A')} ({priority})")

        if result['total_modules'] > 10:
            print(f"    ... and {result['total_modules'] - 10} more")

    print()
    print(f"  Output: {args.output}")
    print()
    print(f"{'='*70}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
