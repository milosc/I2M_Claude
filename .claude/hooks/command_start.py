#!/usr/bin/env python3
"""
Command Start Hook

Logs command start event to pipeline_progress.json.
Called at the beginning of command execution.

Usage:
    python3 .claude/hooks/command_start.py \\
        --command-name "/prototype" \\
        --stage "prototype" \\
        --system-name "EmergencyTriage" \\
        --intent "Generate prototype from discovery outputs"

Returns:
    event_id - The generated event ID for matching with command_end
"""

import sys
import json
from pathlib import Path

# Add _state to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "_state"))

from pipeline_logger import get_logger


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Log command start event")
    parser.add_argument("--command-name", required=True, help="Command name (e.g., /prototype)")
    parser.add_argument("--stage", required=True, help="Stage name (e.g., prototype)")
    parser.add_argument("--system-name", required=False, help="System name (e.g., EmergencyTriage)")
    parser.add_argument("--intent", required=False, help="Command intent description")
    parser.add_argument("--args", required=False, help="Command arguments (JSON string)")

    args = parser.parse_args()

    # Get logger
    logger = get_logger()

    # Set context
    context = {
        "stage": args.stage
    }
    if args.system_name:
        context["system_name"] = args.system_name

    logger.set_context(**context)

    # Parse args if provided
    command_args = None
    if args.args:
        try:
            command_args = json.loads(args.args)
        except json.JSONDecodeError:
            command_args = {"raw": args.args}

    # Log command start
    activity = {
        "type": "command",
        "name": args.command_name,
        "intent": args.intent or f"Execute {args.command_name} command",
        "stage": args.stage
    }

    if command_args:
        activity["args"] = command_args

    event_id = logger.log_event(
        event_type="command_start",
        level="command",
        activity=activity,
        context=context
    )

    # Output event_id for matching with command_end
    print(event_id)

    return 0


if __name__ == "__main__":
    sys.exit(main())
