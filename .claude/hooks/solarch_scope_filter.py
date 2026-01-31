#!/usr/bin/env python3
"""
SolArch Scope Filter Utility

Filters ADRs based on entry point flags (system, subsystem, layer, single-ADR).
Supports the 4 entry points defined in SolArch v2.0 architecture.

Usage:
    python3 solarch_scope_filter.py --system-name InventorySystem
    python3 solarch_scope_filter.py --system-name InventorySystem --subsystem authentication
    python3 solarch_scope_filter.py --system-name InventorySystem --layer frontend
    python3 solarch_scope_filter.py --system-name InventorySystem --adr ADR-007
    python3 solarch_scope_filter.py --system-name InventorySystem --quality critical
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Expected execution time by entry point
TIME_ESTIMATES = {
    "system": {"minutes": 68, "description": "All ADRs (12)"},
    "subsystem": {"minutes": 23, "description": "Subsystem ADRs (3-4)"},
    "layer": {"minutes": 17, "description": "Layer ADRs (2-3)"},
    "adr": {"minutes": 6, "description": "Single ADR (1)"},
}

# Default ADR registry structure (used when registry doesn't exist)
DEFAULT_ADR_REGISTRY = [
    {"id": "ADR-001", "title": "Architecture Style", "priority": "P0", "subsystem": "core", "layer": "all", "category": "foundation"},
    {"id": "ADR-002", "title": "Technology Stack", "priority": "P0", "subsystem": "core", "layer": "all", "category": "foundation"},
    {"id": "ADR-003", "title": "Data Storage", "priority": "P0", "subsystem": "core", "layer": "backend", "category": "foundation"},
    {"id": "ADR-004", "title": "Frontend Architecture", "priority": "P1", "subsystem": "core", "layer": "frontend", "category": "foundation"},
    {"id": "ADR-005", "title": "API Design", "priority": "P1", "subsystem": "api", "layer": "backend", "category": "communication"},
    {"id": "ADR-006", "title": "Event Communication", "priority": "P1", "subsystem": "messaging", "layer": "backend", "category": "communication"},
    {"id": "ADR-007", "title": "Authentication Strategy", "priority": "P0", "subsystem": "authentication", "layer": "backend", "category": "communication"},
    {"id": "ADR-008", "title": "External Integration", "priority": "P1", "subsystem": "integration", "layer": "backend", "category": "communication"},
    {"id": "ADR-009", "title": "Deployment Strategy", "priority": "P1", "subsystem": "devops", "layer": "infrastructure", "category": "operational"},
    {"id": "ADR-010", "title": "Observability", "priority": "P1", "subsystem": "devops", "layer": "infrastructure", "category": "operational"},
    {"id": "ADR-011", "title": "Security Infrastructure", "priority": "P0", "subsystem": "security", "layer": "infrastructure", "category": "operational"},
    {"id": "ADR-012", "title": "CI/CD Pipeline", "priority": "P2", "subsystem": "devops", "layer": "infrastructure", "category": "operational"},
]


def load_adr_registry(system_name: str) -> list:
    """Load ADR registry from traceability or use defaults."""
    registry_path = Path(f"traceability/{system_name}_adr_registry.json")

    if registry_path.exists():
        try:
            with open(registry_path) as f:
                data = json.load(f)
                return data.get("adrs", data) if isinstance(data, dict) else data
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Warning: Could not load ADR registry: {e}", file=sys.stderr)

    # Return default registry
    return DEFAULT_ADR_REGISTRY


def filter_scope(
    system_name: str,
    subsystem: Optional[str] = None,
    layer: Optional[str] = None,
    adr_id: Optional[str] = None,
    quality_mode: str = "standard"
) -> dict:
    """
    Filter ADRs based on entry point flags.

    Args:
        system_name: The system being analyzed
        subsystem: Filter by subsystem (e.g., "authentication")
        layer: Filter by layer (e.g., "frontend", "backend", "infrastructure")
        adr_id: Filter to single ADR (e.g., "ADR-007")
        quality_mode: "standard" (P0 board review) or "critical" (all board review)

    Returns:
        Filtered scope dictionary
    """
    adr_registry = load_adr_registry(system_name)

    # Determine entry point type and filter
    if adr_id:
        # Single ADR entry point
        entry_type = "adr"
        entry_value = adr_id
        filtered_adrs = [a for a in adr_registry if a["id"].upper() == adr_id.upper()]
    elif subsystem:
        # Subsystem entry point
        entry_type = "subsystem"
        entry_value = subsystem
        filtered_adrs = [
            a for a in adr_registry
            if subsystem.lower() in a.get("subsystem", "").lower()
        ]
    elif layer:
        # Layer entry point
        entry_type = "layer"
        entry_value = layer
        filtered_adrs = [
            a for a in adr_registry
            if a.get("layer", "").lower() == layer.lower() or a.get("layer", "").lower() == "all"
        ]
    else:
        # System-level (all ADRs)
        entry_type = "system"
        entry_value = "all"
        filtered_adrs = adr_registry

    # Add board review flag based on quality mode and priority
    for adr in filtered_adrs:
        if quality_mode == "critical":
            adr["needs_board_review"] = True
        else:
            # Standard mode: only P0 gets board review
            adr["needs_board_review"] = adr.get("priority", "P1") == "P0"

    # Calculate statistics
    total_adrs = len(filtered_adrs)
    p0_count = len([a for a in filtered_adrs if a.get("priority") == "P0"])
    board_review_count = len([a for a in filtered_adrs if a.get("needs_board_review")])

    # Estimate time
    time_estimate = TIME_ESTIMATES.get(entry_type, TIME_ESTIMATES["system"])

    return {
        "$schema": "solarch-filtered-scope-v1",
        "system_name": system_name,
        "entry_point": {
            "type": entry_type,
            "value": entry_value
        },
        "quality_mode": quality_mode,
        "adrs": filtered_adrs,
        "total_adrs": total_adrs,
        "p0_count": p0_count,
        "board_review_count": board_review_count,
        "estimated_time_minutes": time_estimate["minutes"] if entry_type == "system" else int(time_estimate["minutes"] * total_adrs / 12),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def save_filtered_scope(scope: dict, output_path: str = "_state/solarch_filtered_scope.json") -> None:
    """Save filtered scope to state file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(scope, f, indent=2)
    print(f"✅ Filtered scope saved to: {output_path}")


def print_scope_summary(scope: dict) -> None:
    """Print human-readable scope summary."""
    print("=" * 60)
    print("SOLARCH v2.0 - Scope Filter")
    print("=" * 60)
    print()
    print(f"System: {scope['system_name']}")
    print(f"Entry Point: {scope['entry_point']['type'].capitalize()} ({scope['entry_point']['value']})")
    print(f"Quality Mode: {scope['quality_mode'].capitalize()}")
    print()
    print("-" * 60)
    print("SCOPE SUMMARY")
    print("-" * 60)
    print(f"  Total ADRs: {scope['total_adrs']}")
    print(f"  P0 ADRs: {scope['p0_count']}")
    print(f"  Board Reviews: {scope['board_review_count']}")
    print(f"  Estimated Time: {scope['estimated_time_minutes']} minutes")
    print()
    print("-" * 60)
    print("ADRs IN SCOPE")
    print("-" * 60)

    for adr in scope["adrs"]:
        board_flag = "🔍" if adr.get("needs_board_review") else "  "
        priority = adr.get("priority", "P1")
        print(f"  {board_flag} {adr['id']}: {adr.get('title', 'Untitled')} ({priority})")

    print()
    print("🔍 = Board review required")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="SolArch Scope Filter - Filter ADRs by entry point",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # System-level (all ADRs)
  python3 solarch_scope_filter.py --system-name InventorySystem

  # Subsystem-level (authentication ADRs)
  python3 solarch_scope_filter.py --system-name InventorySystem --subsystem authentication

  # Layer-level (frontend ADRs)
  python3 solarch_scope_filter.py --system-name InventorySystem --layer frontend

  # Single ADR
  python3 solarch_scope_filter.py --system-name InventorySystem --adr ADR-007

  # Quality critical mode (all ADRs get board review)
  python3 solarch_scope_filter.py --system-name InventorySystem --quality critical
        """
    )

    parser.add_argument(
        "--system-name",
        required=True,
        help="System name (e.g., InventorySystem)"
    )
    parser.add_argument(
        "--subsystem",
        help="Filter by subsystem (e.g., authentication, api, security)"
    )
    parser.add_argument(
        "--layer",
        choices=["frontend", "backend", "infrastructure", "all"],
        help="Filter by architecture layer"
    )
    parser.add_argument(
        "--adr",
        help="Filter to single ADR (e.g., ADR-007)"
    )
    parser.add_argument(
        "--quality",
        choices=["standard", "critical"],
        default="standard",
        help="Quality mode: standard (P0 board review) or critical (all board review)"
    )
    parser.add_argument(
        "--output",
        default="_state/solarch_filtered_scope.json",
        help="Output file path (default: _state/solarch_filtered_scope.json)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON only (no summary)"
    )

    args = parser.parse_args()

    # Validate mutually exclusive entry points
    entry_points = [args.subsystem, args.layer, args.adr]
    if sum(1 for ep in entry_points if ep) > 1:
        parser.error("Only one entry point can be specified: --subsystem, --layer, or --adr")

    # Filter scope
    scope = filter_scope(
        system_name=args.system_name,
        subsystem=args.subsystem,
        layer=args.layer,
        adr_id=args.adr,
        quality_mode=args.quality
    )

    # Output
    if args.json:
        print(json.dumps(scope, indent=2))
    else:
        print_scope_summary(scope)
        save_filtered_scope(scope, args.output)


if __name__ == "__main__":
    main()
