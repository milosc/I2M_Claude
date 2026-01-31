#!/usr/bin/env python3
"""
Auto-load stage-specific rules based on current pipeline stage.
Called at session start or stage transitions.
"""

import json
import os
import sys

def get_current_stage():
    """Detect current stage from state files."""
    # Check pipeline config (multi-stage projects)
    if os.path.exists("_state/pipeline_config.json"):
        try:
            with open("_state/pipeline_config.json") as f:
                config = json.load(f)
                return config.get("current_stage", "unknown")
        except Exception:
            pass

    # Check discovery config (Discovery-only projects)
    if os.path.exists("_state/discovery_config.json"):
        return "discovery"

    # Check prototype config
    if os.path.exists("_state/prototype_config.json"):
        return "prototype"

    # Check productspecs config
    if os.path.exists("_state/productspecs_config.json"):
        return "productspecs"

    # Check solarch config
    if os.path.exists("_state/solarch_config.json"):
        return "solarch"

    # Check implementation config
    if os.path.exists("_state/implementation_config.json"):
        return "implementation"

    return "unknown"

def get_rules_for_stage(stage):
    """Return list of rules to load for each stage."""
    rules_map = {
        "discovery": [
            "/rules-discovery",
            "/rules-traceability"
        ],
        "prototype": [
            "/_assembly_first_rules",
            "/rules-traceability"
        ],
        "productspecs": [
            "/rules-traceability"
        ],
        "solarch": [
            "/rules-traceability"
        ],
        "implementation": [
            "/rules-process-integrity",
            "/rules-agent-coordination",
            "/rules-traceability"
        ],
        "unknown": [
            # No stage detected, load minimal rules
        ]
    }

    return rules_map.get(stage, [])

def main():
    """Main entry point."""
    stage = get_current_stage()
    rules = get_rules_for_stage(stage)

    # Output format for hook consumption
    print(f"STAGE: {stage}")
    if rules:
        print(f"AUTO_LOAD: {','.join(rules)}")
    else:
        print("AUTO_LOAD: (none)")

    # Return success
    return 0

if __name__ == "__main__":
    sys.exit(main())
