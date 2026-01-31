#!/usr/bin/env python3
"""
Post-Task Completion Hook - Cleanup and state updates after task completion.

This hook is called after an agent completes its task to:
1. Release file locks
2. End the session
3. Update task registry
4. Trigger integrity checks
5. Update progress tracking

Usage:
    python3 post_task_completion.py --session-id <id> --status <completed|failed> [--task-id <id>]
    python3 post_task_completion.py --cleanup-all --agent-id <id>
    python3 post_task_completion.py --update-task <task_id> --status <status>

Exit codes:
    0 - Cleanup successful
    1 - Cleanup failed (check output for details)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List


# Import coordinator functions
sys.path.insert(0, str(Path(__file__).parent))
from agent_coordinator import (
    end_session, release_lock, load_sessions, load_locks, save_sessions, cleanup_stale
)

# Import pipeline logger
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "_state"))
try:
    from pipeline_logger import get_logger
    PIPELINE_LOGGING_ENABLED = True
except ImportError:
    PIPELINE_LOGGING_ENABLED = False
    print("Warning: Pipeline logging not available")


# State file paths
STATE_DIR = Path("_state")
TASK_REGISTRY = Path("traceability/task_registry.json")
PROGRESS_FILE = STATE_DIR / "implementation_progress.json"
INTEGRITY_FILE = STATE_DIR / "integrity_status.json"


def load_task_registry() -> Dict[str, Any]:
    """Load task registry if it exists."""
    if TASK_REGISTRY.exists():
        with open(TASK_REGISTRY, 'r') as f:
            return json.load(f)
    return {"tasks": [], "updated_at": None}


def save_task_registry(data: Dict[str, Any]) -> None:
    """Save task registry."""
    data["updated_at"] = datetime.now().isoformat()
    TASK_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with open(TASK_REGISTRY, 'w') as f:
        json.dump(data, f, indent=2)


def load_progress() -> Dict[str, Any]:
    """Load implementation progress if it exists."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {
        "current_checkpoint": 0,
        "tasks_completed": 0,
        "tasks_total": 0,
        "updated_at": None
    }


def save_progress(data: Dict[str, Any]) -> None:
    """Save implementation progress."""
    data["updated_at"] = datetime.now().isoformat()
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def update_task_status(task_id: str, status: str, details: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Update task status in the registry.

    Args:
        task_id: The task ID (e.g., T-015)
        status: New status (pending, in_progress, completed, failed, blocked)
        details: Optional additional details

    Returns:
        {
            "success": bool,
            "message": str,
            "task": dict or None
        }
    """
    registry = load_task_registry()
    tasks = registry.get("tasks", [])

    for task in tasks:
        if task.get("id") == task_id:
            old_status = task.get("status")
            task["status"] = status
            task["status_updated_at"] = datetime.now().isoformat()

            if details:
                task.update(details)

            if status == "completed":
                task["completed_at"] = datetime.now().isoformat()
            elif status == "failed":
                task["failed_at"] = datetime.now().isoformat()

            save_task_registry(registry)

            # Update progress counts
            update_progress_counts(registry)

            return {
                "success": True,
                "message": f"Task {task_id} status updated: {old_status} -> {status}",
                "task": task
            }

    return {
        "success": False,
        "message": f"Task {task_id} not found in registry",
        "task": None
    }


def update_progress_counts(registry: Dict[str, Any]) -> None:
    """Update progress file with task counts."""
    tasks = registry.get("tasks", [])

    completed = sum(1 for t in tasks if t.get("status") == "completed")
    total = len(tasks)

    progress = load_progress()
    progress["tasks_completed"] = completed
    progress["tasks_total"] = total

    if total > 0:
        progress["completion_percentage"] = round((completed / total) * 100, 1)

    save_progress(progress)


def release_all_locks_for_agent(agent_id: str) -> Dict[str, Any]:
    """
    Release all locks held by an agent.

    Returns:
        {
            "success": bool,
            "locks_released": list,
            "message": str
        }
    """
    locks_data = load_locks()
    locks = locks_data.get("locks", [])

    released = []
    remaining = []

    for lock in locks:
        if lock["agent_id"] == agent_id:
            released.append(lock["file_path"])
        else:
            remaining.append(lock)

    locks_data["locks"] = remaining

    from agent_coordinator import save_locks
    save_locks(locks_data)

    return {
        "success": True,
        "locks_released": released,
        "message": f"Released {len(released)} locks for agent {agent_id}"
    }


def trigger_integrity_check() -> Dict[str, Any]:
    """
    Trigger an integrity check after task completion.

    Returns:
        {
            "triggered": bool,
            "message": str
        }
    """
    # This would normally trigger the traceability-guardian or state-watchdog
    # For now, we just update a timestamp to indicate a check is needed

    integrity = {}
    if INTEGRITY_FILE.exists():
        with open(INTEGRITY_FILE, 'r') as f:
            integrity = json.load(f)

    integrity["last_task_completion"] = datetime.now().isoformat()
    integrity["integrity_check_pending"] = True

    INTEGRITY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INTEGRITY_FILE, 'w') as f:
        json.dump(integrity, f, indent=2)

    return {
        "triggered": True,
        "message": "Integrity check flagged as pending"
    }


def complete_session(
    session_id: str,
    status: str,
    task_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Complete a session with full cleanup.

    Args:
        session_id: The session to complete
        status: "completed" or "failed"
        task_id: Optional task ID to update

    Returns:
        {
            "success": bool,
            "session_ended": bool,
            "task_updated": bool,
            "locks_released": list,
            "integrity_triggered": bool,
            "message": str
        }
    """
    result = {
        "success": True,
        "session_ended": False,
        "task_updated": False,
        "locks_released": [],
        "integrity_triggered": False,
        "message": ""
    }

    # Log agent spawn end to pipeline (before ending session)
    if PIPELINE_LOGGING_ENABLED:
        try:
            logger = get_logger()
            sessions_data = load_sessions()
            active_sessions = sessions_data.get("active_sessions", [])

            # Find the session to get start event ID and agent info
            session_info = None
            for session in active_sessions:
                if session["session_id"] == session_id:
                    session_info = session
                    break

            if session_info:
                # Build activity data for end event
                activity = {
                    "type": "agent_spawn",
                    "agent_id": session_info["agent_id"],
                    "agent_type": session_info["agent_type"],
                    "task_id": session_info.get("task_id", task_id),
                    "status": status
                }

                # Calculate duration if we have start time
                if "spawned_at" in session_info:
                    from datetime import datetime
                    start_time = datetime.fromisoformat(session_info["spawned_at"])
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    activity["duration_seconds"] = round(duration, 3)

                # Log the end event
                event_id = logger.log_event(
                    event_type="agent_spawn_end",
                    level="agent",
                    activity=activity,
                    related_start_event_id=session_info.get("pipeline_event_id")
                )

        except Exception as e:
            print(f"Warning: Failed to log agent spawn end: {e}")

    # 1. End the session (this also releases locks via agent_coordinator)
    session_result = end_session(session_id, status)
    result["session_ended"] = session_result["success"]
    result["locks_released"] = session_result.get("locks_released", [])

    if not session_result["success"]:
        result["success"] = False
        result["message"] = session_result["message"]
        return result

    # 2. Update task status if task_id provided
    if task_id:
        task_status = "completed" if status == "completed" else "failed"
        task_result = update_task_status(task_id, task_status)
        result["task_updated"] = task_result["success"]

    # 3. Trigger integrity check
    integrity_result = trigger_integrity_check()
    result["integrity_triggered"] = integrity_result["triggered"]

    # 4. Run stale cleanup (opportunistic)
    cleanup_stale()

    result["message"] = f"Session {session_id} completed with status: {status}"
    return result


def cleanup_all_for_agent(agent_id: str) -> Dict[str, Any]:
    """
    Clean up all resources for an agent (emergency cleanup).

    Args:
        agent_id: The agent ID to clean up

    Returns:
        {
            "success": bool,
            "sessions_ended": int,
            "locks_released": int,
            "message": str
        }
    """
    sessions_ended = 0
    locks_released = 0

    # 1. End all active sessions for this agent
    sessions_data = load_sessions()
    active = sessions_data.get("active_sessions", [])

    for session in list(active):
        if session["agent_id"] == agent_id:
            end_session(session["session_id"], "terminated")
            sessions_ended += 1

    # 2. Release all locks (in case any were missed)
    lock_result = release_all_locks_for_agent(agent_id)
    locks_released = len(lock_result["locks_released"])

    return {
        "success": True,
        "sessions_ended": sessions_ended,
        "locks_released": locks_released,
        "message": f"Cleaned up agent {agent_id}: {sessions_ended} sessions, {locks_released} locks"
    }


def record_task_output(
    task_id: str,
    output_files: List[str],
    test_results: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Record task output for traceability.

    Args:
        task_id: The task ID
        output_files: List of files created/modified
        test_results: Optional test execution results

    Returns:
        {
            "success": bool,
            "message": str
        }
    """
    registry = load_task_registry()
    tasks = registry.get("tasks", [])

    for task in tasks:
        if task.get("id") == task_id:
            task["output_files"] = output_files
            task["output_recorded_at"] = datetime.now().isoformat()

            if test_results:
                task["test_results"] = test_results

            save_task_registry(registry)

            return {
                "success": True,
                "message": f"Recorded {len(output_files)} output files for {task_id}"
            }

    return {
        "success": False,
        "message": f"Task {task_id} not found"
    }


def main():
    parser = argparse.ArgumentParser(description="Post-Task Completion Hook")
    parser.add_argument("--session-id", help="Session ID to complete")
    parser.add_argument("--status", choices=["completed", "failed"],
                        help="Completion status")
    parser.add_argument("--task-id", help="Task ID to update")
    parser.add_argument("--cleanup-all", action="store_true",
                        help="Clean up all resources for an agent")
    parser.add_argument("--agent-id", help="Agent ID for cleanup-all")
    parser.add_argument("--update-task", help="Update task status only")
    parser.add_argument("--output-files", nargs="*", help="Record output files for task")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    result = None

    if args.cleanup_all:
        if not args.agent_id:
            print("Error: --agent-id required with --cleanup-all")
            sys.exit(1)
        result = cleanup_all_for_agent(args.agent_id)

    elif args.update_task:
        if not args.status:
            print("Error: --status required with --update-task")
            sys.exit(1)
        result = update_task_status(args.update_task, args.status)

    elif args.session_id:
        if not args.status:
            print("Error: --status required with --session-id")
            sys.exit(1)
        result = complete_session(args.session_id, args.status, args.task_id)

    elif args.task_id and args.output_files:
        result = record_task_output(args.task_id, args.output_files)

    else:
        parser.print_help()
        sys.exit(1)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result.get("success"):
            print(f"SUCCESS: {result.get('message', 'Completed')}")
        else:
            print(f"FAILED: {result.get('message', 'Unknown error')}")

    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
