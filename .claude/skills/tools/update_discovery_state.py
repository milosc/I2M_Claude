#!/usr/bin/env python3
"""
Discovery State Management Utility

Updates _state/discovery_progress.json and _state/discovery_config.json
after phase completion.

Usage:
    python3 update_discovery_state.py --phase 0_init --status complete
    python3 update_discovery_state.py --phase 9_specs --status complete
    python3 update_discovery_state.py --set-complete  # Mark all phases complete
    python3 update_discovery_state.py --show          # Show current state
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

STATE_DIR = Path("_state")
PROGRESS_FILE = STATE_DIR / "discovery_progress.json"
CONFIG_FILE = STATE_DIR / "discovery_config.json"

# Phase definitions with progress percentages
PHASES = {
    "0_init": {"order": 0, "progress": 8, "next": "1_analyze", "checkpoint": "discovery-init"},
    "1_analyze": {"order": 1, "progress": 15, "next": "1.5_pdf_analysis", "checkpoint": "discovery-analyze"},
    "1.5_pdf_analysis": {"order": 2, "progress": 20, "next": "2_extract", "checkpoint": "discovery-analyze"},
    "2_extract": {"order": 3, "progress": 25, "next": "3_personas", "checkpoint": "discovery-analyze"},
    "3_personas": {"order": 4, "progress": 35, "next": "4_jtbd", "checkpoint": "discovery-research"},
    "4_jtbd": {"order": 5, "progress": 40, "next": "5_vision", "checkpoint": "discovery-research"},
    "5_vision": {"order": 6, "progress": 50, "next": "6_strategy", "checkpoint": "discovery-strategy-all"},
    "6_strategy": {"order": 7, "progress": 55, "next": "7_roadmap", "checkpoint": "discovery-strategy-all"},
    "7_roadmap": {"order": 8, "progress": 60, "next": "8_kpis", "checkpoint": "discovery-strategy-all"},
    "8_kpis": {"order": 9, "progress": 65, "next": "9_specs", "checkpoint": "discovery-strategy-all"},
    "9_specs": {"order": 10, "progress": 80, "next": "10_docs", "checkpoint": "discovery-specs-all"},
    "10_docs": {"order": 11, "progress": 90, "next": "11_validate", "checkpoint": "discovery-docs-all"},
    "11_validate": {"order": 12, "progress": 100, "next": None, "checkpoint": "discovery-validate"},
}


def load_progress():
    """Load current progress file or create default."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)

    # Default structure
    return {
        "phases": {phase: {"status": "pending"} for phase in PHASES},
        "overall_progress": 0,
        "last_checkpoint": None,
        "resumable_from": "0_init"
    }


def save_progress(progress):
    """Save progress file."""
    STATE_DIR.mkdir(exist_ok=True)
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)
    print(f"✅ Updated {PROGRESS_FILE}")


def load_config():
    """Load config file."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def save_config(config):
    """Save config file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✅ Updated {CONFIG_FILE}")


def update_phase(phase_name, status):
    """Update a specific phase status."""
    if phase_name not in PHASES:
        print(f"❌ Unknown phase: {phase_name}")
        print(f"Valid phases: {', '.join(PHASES.keys())}")
        sys.exit(1)

    progress = load_progress()
    now = datetime.now().isoformat()

    phase_data = progress["phases"].get(phase_name, {})

    if status == "complete":
        phase_data["status"] = "complete"
        if "started" not in phase_data:
            phase_data["started"] = now
        phase_data["completed"] = now

        # Update overall progress
        phase_info = PHASES[phase_name]
        progress["overall_progress"] = phase_info["progress"]
        progress["last_checkpoint"] = phase_info["checkpoint"]
        progress["resumable_from"] = phase_info["next"]

    elif status == "in_progress":
        phase_data["status"] = "in_progress"
        phase_data["started"] = now

    elif status == "pending":
        phase_data["status"] = "pending"
        phase_data.pop("started", None)
        phase_data.pop("completed", None)

    progress["phases"][phase_name] = phase_data
    save_progress(progress)

    # Also update config
    config = load_config()
    if config:
        config["updated_at"] = now
        config["current_phase"] = PHASES[phase_name]["order"]
        config["current_checkpoint"] = PHASES[phase_name]["checkpoint"]
        if status == "complete" and phase_name == "11_validate":
            config["status"] = "complete"
        save_config(config)

    print(f"✅ Phase {phase_name} → {status}")
    print(f"   Overall progress: {progress['overall_progress']}%")
    if progress["resumable_from"]:
        print(f"   Next phase: {progress['resumable_from']}")


def set_all_complete():
    """Mark all phases as complete."""
    progress = load_progress()
    now = datetime.now().isoformat()

    for phase_name in PHASES:
        progress["phases"][phase_name] = {
            "status": "complete",
            "started": now,
            "completed": now
        }

    progress["overall_progress"] = 100
    progress["last_checkpoint"] = "discovery-validate"
    progress["resumable_from"] = None

    save_progress(progress)

    # Update config
    config = load_config()
    if config:
        config["updated_at"] = now
        config["status"] = "complete"
        config["current_phase"] = 11
        config["current_checkpoint"] = "discovery-validate"
        save_config(config)

    print("✅ All phases marked complete")
    print("   Overall progress: 100%")


def show_state():
    """Display current state."""
    if not PROGRESS_FILE.exists():
        print("❌ No _state/discovery_progress.json found")
        sys.exit(1)

    progress = load_progress()

    print("\n📊 Discovery Progress Status\n")
    print("=" * 50)

    for phase_name, phase_info in PHASES.items():
        phase_data = progress["phases"].get(phase_name, {})
        status = phase_data.get("status", "pending")

        if status == "complete":
            icon = "✅"
        elif status == "in_progress":
            icon = "🔄"
        else:
            icon = "⬜"

        print(f"{icon} {phase_name}: {status}")

    print("=" * 50)
    print(f"\nOverall Progress: {progress.get('overall_progress', 0)}%")
    print(f"Last Checkpoint: {progress.get('last_checkpoint', 'None')}")
    print(f"Resumable From: {progress.get('resumable_from', 'None')}")

    if CONFIG_FILE.exists():
        config = load_config()
        print(f"\nConfig Status: {config.get('status', 'unknown')}")


def main():
    parser = argparse.ArgumentParser(
        description="Discovery State Management Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --phase 0_init --status complete
  %(prog)s --phase 9_specs --status complete
  %(prog)s --set-complete
  %(prog)s --show
        """
    )
    parser.add_argument("--phase", help="Phase to update (e.g., 0_init, 9_specs)")
    parser.add_argument("--status", choices=["pending", "in_progress", "complete"],
                        help="New status for the phase")
    parser.add_argument("--set-complete", action="store_true",
                        help="Mark ALL phases as complete")
    parser.add_argument("--show", action="store_true",
                        help="Show current state")

    args = parser.parse_args()

    if args.show:
        show_state()
    elif args.set_complete:
        set_all_complete()
    elif args.phase and args.status:
        update_phase(args.phase, args.status)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
