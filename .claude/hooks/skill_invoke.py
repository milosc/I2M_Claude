#!/usr/bin/env python3
"""
Skill Invocation Hook

Logs skill invocation events to pipeline_progress.json.
Can be used as a context manager for automatic start/end logging.

Usage:
    from .claude.hooks.skill_invoke import log_skill_execution

    # Context manager (automatic start/end)
    with log_skill_execution("Prototype_Builder", "Generate prototype", stage="prototype"):
        # Skill logic here
        pass

    # Or manual logging
    python3 .claude/hooks/skill_invoke.py \\
        --skill-name "Prototype_Builder" \\
        --action "start" \\
        --stage "prototype" \\
        --intent "Generate prototype from discovery"

Returns:
    event_id - The generated event ID
"""

import sys
import json
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, Dict, Any

# Add _state to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "_state"))

try:
    from pipeline_logger import get_logger
    PIPELINE_LOGGING_ENABLED = True
except ImportError:
    PIPELINE_LOGGING_ENABLED = False


@contextmanager
def log_skill_execution(
    skill_name: str,
    intent: str,
    stage: Optional[str] = None,
    system_name: Optional[str] = None,
    args: Optional[Dict[str, Any]] = None
):
    """
    Context manager for logging skill execution with automatic start/end.

    Args:
        skill_name: Name of the skill being executed
        intent: Description of what the skill will do
        stage: Optional stage name
        system_name: Optional system name
        args: Optional skill arguments

    Usage:
        with log_skill_execution("Prototype_Builder", "Generate prototype") as event_id:
            # Skill execution
            pass
        # Automatically logs end event
    """
    if not PIPELINE_LOGGING_ENABLED:
        yield None
        return

    logger = get_logger()

    # Set context if provided
    context = {}
    if stage:
        context["stage"] = stage
    if system_name:
        context["system_name"] = system_name

    if context:
        logger.set_context(**context)

    # Build activity
    activity = {
        "type": "skill",
        "skill_name": skill_name,
        "intent": intent
    }

    if args:
        activity["args"] = args

    # Use the logger's activity_context for automatic start/end logging
    with logger.activity_context(
        event_type_prefix="skill_invoke",
        level="skill",
        activity=activity,
        context=context if context else None
    ) as event_id:
        yield event_id


def log_skill_start(
    skill_name: str,
    intent: str,
    stage: Optional[str] = None,
    system_name: Optional[str] = None,
    args: Optional[Dict[str, Any]] = None
) -> str:
    """
    Log skill start event.

    Args:
        skill_name: Name of the skill
        intent: Intent description
        stage: Optional stage name
        system_name: Optional system name
        args: Optional skill arguments

    Returns:
        event_id: The generated event ID
    """
    if not PIPELINE_LOGGING_ENABLED:
        return "evt-disabled"

    logger = get_logger()

    # Set context if provided
    context = {}
    if stage:
        context["stage"] = stage
    if system_name:
        context["system_name"] = system_name

    if context:
        logger.set_context(**context)

    # Build activity
    activity = {
        "type": "skill",
        "skill_name": skill_name,
        "intent": intent
    }

    if args:
        activity["args"] = args

    # Log start event
    event_id = logger.log_event(
        event_type="skill_invoke_start",
        level="skill",
        activity=activity,
        context=context if context else None
    )

    return event_id


def log_skill_end(
    skill_name: str,
    start_event_id: str,
    status: str = "completed",
    outputs: Optional[Dict[str, Any]] = None,
    error_message: Optional[str] = None
) -> str:
    """
    Log skill end event.

    Args:
        skill_name: Name of the skill
        start_event_id: Related start event ID
        status: "completed" or "failed"
        outputs: Optional skill outputs
        error_message: Optional error message if failed

    Returns:
        event_id: The generated event ID
    """
    if not PIPELINE_LOGGING_ENABLED:
        return "evt-disabled"

    logger = get_logger()

    # Build activity
    activity = {
        "type": "skill",
        "skill_name": skill_name,
        "status": status
    }

    if error_message:
        activity["error_message"] = error_message

    # Build results
    results = {}
    if outputs:
        results["outputs"] = outputs

    # Log end event
    event_id = logger.log_event(
        event_type="skill_invoke_end",
        level="skill",
        activity=activity,
        results=results if results else None,
        related_start_event_id=start_event_id
    )

    return event_id


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Log skill invocation event")
    parser.add_argument("--skill-name", required=True, help="Skill name")
    parser.add_argument("--action", required=True, choices=["start", "end"], help="Action type")
    parser.add_argument("--intent", help="Intent description (for start)")
    parser.add_argument("--stage", help="Stage name")
    parser.add_argument("--system-name", help="System name")
    parser.add_argument("--args", help="Skill arguments (JSON string)")
    parser.add_argument("--start-event-id", help="Related start event ID (for end)")
    parser.add_argument("--status", choices=["completed", "failed"], default="completed",
                        help="Status (for end)")
    parser.add_argument("--outputs", help="Skill outputs (JSON string, for end)")
    parser.add_argument("--error-message", help="Error message (for end)")

    args_parsed = parser.parse_args()

    if args_parsed.action == "start":
        if not args_parsed.intent:
            print("Error: --intent required for start action")
            sys.exit(1)

        # Parse args if provided
        skill_args = None
        if args_parsed.args:
            try:
                skill_args = json.loads(args_parsed.args)
            except json.JSONDecodeError:
                skill_args = {"raw": args_parsed.args}

        event_id = log_skill_start(
            skill_name=args_parsed.skill_name,
            intent=args_parsed.intent,
            stage=args_parsed.stage,
            system_name=args_parsed.system_name,
            args=skill_args
        )

        print(event_id)

    else:  # end
        if not args_parsed.start_event_id:
            print("Error: --start-event-id required for end action")
            sys.exit(1)

        # Parse outputs if provided
        outputs = None
        if args_parsed.outputs:
            try:
                outputs = json.loads(args_parsed.outputs)
            except json.JSONDecodeError:
                outputs = {"raw": args_parsed.outputs}

        event_id = log_skill_end(
            skill_name=args_parsed.skill_name,
            start_event_id=args_parsed.start_event_id,
            status=args_parsed.status,
            outputs=outputs,
            error_message=args_parsed.error_message
        )

        print(event_id)

    return 0


if __name__ == "__main__":
    sys.exit(main())
