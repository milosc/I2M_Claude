#!/usr/bin/env python3
"""
Command End Hook

Logs command end event to pipeline_progress.json.
Called at the end of command execution.

Usage:
    python3 .claude/hooks/command_end.py \\
        --command-name "/prototype" \\
        --stage "prototype" \\
        --status "completed" \\
        --start-event-id "evt-abc12345" \\
        --outputs '{"files_created": 45, "checkpoint": 14}'

Returns:
    event_id - The generated event ID for the end event
"""

import sys
import json
from pathlib import Path

# Add _state to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "_state"))

from pipeline_logger import get_logger


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Log command end event")
    parser.add_argument("--command-name", required=True, help="Command name (e.g., /prototype)")
    parser.add_argument("--stage", required=True, help="Stage name (e.g., prototype)")
    parser.add_argument("--status", required=True, choices=["completed", "failed", "cancelled"], help="Command status")
    parser.add_argument("--start-event-id", required=False, help="Related start event ID")
    parser.add_argument("--outputs", required=False, help="Command outputs (JSON string)")
    parser.add_argument("--error-message", required=False, help="Error message if failed")

    args = parser.parse_args()

    # Get logger
    logger = get_logger()

    # Parse outputs if provided
    outputs = None
    if args.outputs:
        try:
            outputs = json.loads(args.outputs)
        except json.JSONDecodeError:
            outputs = {"raw": args.outputs}

    # Build activity
    activity = {
        "type": "command",
        "name": args.command_name,
        "status": args.status,
        "stage": args.stage
    }

    if args.error_message:
        activity["error_message"] = args.error_message

    # Build results
    results = {}
    if outputs:
        results["outputs"] = outputs

    # Log command end
    event_id = logger.log_event(
        event_type="command_end",
        level="command",
        activity=activity,
        results=results if results else None,
        related_start_event_id=args.start_event_id
    )

    # Output event_id
    print(event_id)

    return 0


if __name__ == "__main__":
    sys.exit(main())
