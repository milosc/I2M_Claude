#!/usr/bin/env python3
"""
Agent Spawn Hook

Logs agent spawn events to pipeline_progress.json.
Increments the total_agents_spawned statistic.

Usage:
    # Start agent
    python3 .claude/hooks/agent_spawn.py \
        --agent-id "test-demo-agent" \
        --action "start" \
        --stage "utility" \
        --system-name "Framework" \
        --intent "Test demo agent execution" \
        --task-id "T-001"

    # End agent
    python3 .claude/hooks/agent_spawn.py \
        --agent-id "test-demo-agent" \
        --action "end" \
        --start-event-id "evt-xxxxx" \
        --status "completed" \
        --outputs '{"output_file": "test.md"}'

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
def log_agent_execution(
    agent_id: str,
    intent: str,
    stage: Optional[str] = None,
    system_name: Optional[str] = None,
    task_id: Optional[str] = None,
    agent_type: Optional[str] = None
):
    """
    Context manager for logging agent execution with automatic start/end.

    Args:
        agent_id: ID of the agent being spawned
        intent: Description of what the agent will do
        stage: Optional stage name
        system_name: Optional system name
        task_id: Optional task ID being executed
        agent_type: Optional agent type (e.g., general-purpose, Explore)

    Usage:
        with log_agent_execution("test-demo-agent", "Generate test file") as event_id:
            # Agent execution
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
        "type": "agent",
        "agent_id": agent_id,
        "intent": intent
    }

    if task_id:
        activity["task_id"] = task_id
    if agent_type:
        activity["agent_type"] = agent_type

    # Use the logger's activity_context for automatic start/end logging
    with logger.activity_context(
        event_type_prefix="agent_spawn",
        level="agent",
        activity=activity,
        context=context if context else None
    ) as event_id:
        yield event_id


def log_agent_start(
    agent_id: str,
    intent: str,
    stage: Optional[str] = None,
    system_name: Optional[str] = None,
    task_id: Optional[str] = None,
    agent_type: Optional[str] = None
) -> str:
    """
    Log agent spawn start event.

    Args:
        agent_id: ID of the agent
        intent: Intent description
        stage: Optional stage name
        system_name: Optional system name
        task_id: Optional task ID
        agent_type: Optional agent type

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
        "type": "agent",
        "agent_id": agent_id,
        "intent": intent
    }

    if task_id:
        activity["task_id"] = task_id
    if agent_type:
        activity["agent_type"] = agent_type

    # Log start event - uses "agent_spawn_start" which increments total_agents_spawned
    event_id = logger.log_event(
        event_type="agent_spawn_start",
        level="agent",
        activity=activity,
        context=context if context else None
    )

    return event_id


def log_agent_end(
    agent_id: str,
    start_event_id: str,
    status: str = "completed",
    outputs: Optional[Dict[str, Any]] = None,
    error_message: Optional[str] = None
) -> str:
    """
    Log agent spawn end event.

    Args:
        agent_id: ID of the agent
        start_event_id: Related start event ID
        status: "completed" or "failed"
        outputs: Optional agent outputs
        error_message: Optional error message if failed

    Returns:
        event_id: The generated event ID
    """
    if not PIPELINE_LOGGING_ENABLED:
        return "evt-disabled"

    logger = get_logger()

    # Build activity
    activity = {
        "type": "agent",
        "agent_id": agent_id,
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
        event_type="agent_spawn_end",
        level="agent",
        activity=activity,
        results=results if results else None,
        related_start_event_id=start_event_id
    )

    return event_id


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Log agent spawn event")
    parser.add_argument("--agent-id", required=True, help="Agent ID")
    parser.add_argument("--action", required=True, choices=["start", "end"], help="Action type")
    parser.add_argument("--intent", help="Intent description (for start)")
    parser.add_argument("--stage", help="Stage name")
    parser.add_argument("--system-name", help="System name")
    parser.add_argument("--task-id", help="Task ID being executed")
    parser.add_argument("--agent-type", help="Agent type (e.g., general-purpose)")
    parser.add_argument("--start-event-id", help="Related start event ID (for end)")
    parser.add_argument("--status", choices=["completed", "failed"], default="completed",
                        help="Status (for end)")
    parser.add_argument("--outputs", help="Agent outputs (JSON string, for end)")
    parser.add_argument("--error-message", help="Error message (for end)")

    args_parsed = parser.parse_args()

    if args_parsed.action == "start":
        if not args_parsed.intent:
            print("Error: --intent required for start action")
            sys.exit(1)

        event_id = log_agent_start(
            agent_id=args_parsed.agent_id,
            intent=args_parsed.intent,
            stage=args_parsed.stage,
            system_name=args_parsed.system_name,
            task_id=args_parsed.task_id,
            agent_type=args_parsed.agent_type
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

        event_id = log_agent_end(
            agent_id=args_parsed.agent_id,
            start_event_id=args_parsed.start_event_id,
            status=args_parsed.status,
            outputs=outputs,
            error_message=args_parsed.error_message
        )

        print(event_id)

    return 0


if __name__ == "__main__":
    sys.exit(main())
