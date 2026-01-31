#!/usr/bin/env python3
"""
Agent Coordinator - Core coordination logic for multi-agent execution.

This module provides file locking, session management, and state coordination
for parallel agent execution in the HTEC ClaudeCode Accelerators framework.

Usage:
    python3 agent_coordinator.py --acquire-lock <agent_id> <task_id> <file_path>
    python3 agent_coordinator.py --release-lock <agent_id> <file_path>
    python3 agent_coordinator.py --check-lock <file_path>
    python3 agent_coordinator.py --register-session <agent_id> <task_id>
    python3 agent_coordinator.py --heartbeat <session_id>
    python3 agent_coordinator.py --end-session <session_id> <status>
    python3 agent_coordinator.py --cleanup-stale
    python3 agent_coordinator.py --status
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any
import uuid


# Configuration
LOCK_TIMEOUT_MINUTES = 15
HEARTBEAT_TIMEOUT_SECONDS = 60
MAX_CONCURRENT_AGENTS = 12
STATE_DIR = "_state"
LOCK_FILE = "agent_lock.json"
SESSIONS_FILE = "agent_sessions.json"


def get_state_dir() -> Path:
    """Get or create the state directory."""
    state_path = Path(STATE_DIR)
    state_path.mkdir(exist_ok=True)
    return state_path


def load_locks() -> Dict[str, Any]:
    """Load current lock state."""
    lock_path = get_state_dir() / LOCK_FILE
    if lock_path.exists():
        with open(lock_path, 'r') as f:
            return json.load(f)
    return {"locks": [], "updated_at": datetime.now().isoformat()}


def save_locks(data: Dict[str, Any]) -> None:
    """Save lock state."""
    lock_path = get_state_dir() / LOCK_FILE
    data["updated_at"] = datetime.now().isoformat()
    with open(lock_path, 'w') as f:
        json.dump(data, f, indent=2)


def load_sessions() -> Dict[str, Any]:
    """Load current sessions state."""
    sessions_path = get_state_dir() / SESSIONS_FILE
    if sessions_path.exists():
        with open(sessions_path, 'r') as f:
            return json.load(f)
    return {
        "active_sessions": [],
        "completed_sessions": [],
        "failed_sessions": [],
        "updated_at": datetime.now().isoformat()
    }


def save_sessions(data: Dict[str, Any]) -> None:
    """Save sessions state."""
    sessions_path = get_state_dir() / SESSIONS_FILE
    data["updated_at"] = datetime.now().isoformat()
    with open(sessions_path, 'w') as f:
        json.dump(data, f, indent=2)


def acquire_lock(agent_id: str, task_id: str, file_path: str) -> Dict[str, Any]:
    """
    Attempt to acquire a lock on a file.

    Returns:
        {
            "success": bool,
            "lock_id": str or None,
            "message": str,
            "conflicting_lock": dict or None
        }
    """
    locks_data = load_locks()
    locks = locks_data.get("locks", [])

    # Check for existing lock on this file
    for lock in locks:
        if lock["file_path"] == file_path:
            # Check if lock is expired
            expires_at = datetime.fromisoformat(lock["expires_at"])
            if expires_at > datetime.now():
                return {
                    "success": False,
                    "lock_id": None,
                    "message": f"File is locked by {lock['agent_id']} for task {lock['task_id']}",
                    "conflicting_lock": lock
                }
            else:
                # Lock is expired, remove it
                locks.remove(lock)
                break

    # Create new lock
    lock_id = f"lock-{uuid.uuid4().hex[:8]}"
    new_lock = {
        "lock_id": lock_id,
        "agent_id": agent_id,
        "task_id": task_id,
        "file_path": file_path,
        "acquired_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(minutes=LOCK_TIMEOUT_MINUTES)).isoformat(),
        "extensions": 0
    }

    locks.append(new_lock)
    locks_data["locks"] = locks
    save_locks(locks_data)

    return {
        "success": True,
        "lock_id": lock_id,
        "message": f"Lock acquired: {lock_id}",
        "conflicting_lock": None
    }


def release_lock(agent_id: str, file_path: str) -> Dict[str, Any]:
    """
    Release a lock on a file.

    Returns:
        {
            "success": bool,
            "message": str
        }
    """
    locks_data = load_locks()
    locks = locks_data.get("locks", [])

    for lock in locks:
        if lock["file_path"] == file_path and lock["agent_id"] == agent_id:
            locks.remove(lock)
            locks_data["locks"] = locks
            save_locks(locks_data)
            return {
                "success": True,
                "message": f"Lock released for {file_path}"
            }

    return {
        "success": False,
        "message": f"No lock found for {file_path} by {agent_id}"
    }


def check_lock(file_path: str) -> Dict[str, Any]:
    """
    Check if a file is locked.

    Returns:
        {
            "locked": bool,
            "lock_info": dict or None
        }
    """
    locks_data = load_locks()
    locks = locks_data.get("locks", [])

    for lock in locks:
        if lock["file_path"] == file_path:
            expires_at = datetime.fromisoformat(lock["expires_at"])
            if expires_at > datetime.now():
                return {
                    "locked": True,
                    "lock_info": lock
                }

    return {
        "locked": False,
        "lock_info": None
    }


def extend_lock(agent_id: str, file_path: str) -> Dict[str, Any]:
    """
    Extend a lock by another LOCK_TIMEOUT_MINUTES.
    Can only extend once.

    Returns:
        {
            "success": bool,
            "message": str,
            "new_expiry": str or None
        }
    """
    locks_data = load_locks()
    locks = locks_data.get("locks", [])

    for lock in locks:
        if lock["file_path"] == file_path and lock["agent_id"] == agent_id:
            if lock.get("extensions", 0) >= 1:
                return {
                    "success": False,
                    "message": "Lock already extended once. Cannot extend further.",
                    "new_expiry": None
                }

            lock["extensions"] = lock.get("extensions", 0) + 1
            lock["expires_at"] = (datetime.now() + timedelta(minutes=LOCK_TIMEOUT_MINUTES)).isoformat()
            save_locks(locks_data)

            return {
                "success": True,
                "message": f"Lock extended for {LOCK_TIMEOUT_MINUTES} minutes",
                "new_expiry": lock["expires_at"]
            }

    return {
        "success": False,
        "message": f"No lock found for {file_path} by {agent_id}",
        "new_expiry": None
    }


def register_session(agent_id: str, task_id: str, agent_type: str = "unknown") -> Dict[str, Any]:
    """
    Register a new agent session.

    Returns:
        {
            "success": bool,
            "session_id": str or None,
            "message": str
        }
    """
    sessions_data = load_sessions()
    active = sessions_data.get("active_sessions", [])

    # Check capacity
    if len(active) >= MAX_CONCURRENT_AGENTS:
        return {
            "success": False,
            "session_id": None,
            "message": f"Max concurrent agents ({MAX_CONCURRENT_AGENTS}) reached"
        }

    session_id = f"session-{uuid.uuid4().hex[:8]}"
    new_session = {
        "session_id": session_id,
        "agent_id": agent_id,
        "agent_type": agent_type,
        "task_id": task_id,
        "status": "active",
        "started_at": datetime.now().isoformat(),
        "last_heartbeat": datetime.now().isoformat(),
        "locks_held": []
    }

    active.append(new_session)
    sessions_data["active_sessions"] = active
    save_sessions(sessions_data)

    return {
        "success": True,
        "session_id": session_id,
        "message": f"Session registered: {session_id}"
    }


def heartbeat(session_id: str) -> Dict[str, Any]:
    """
    Update heartbeat for a session.

    Returns:
        {
            "success": bool,
            "message": str
        }
    """
    sessions_data = load_sessions()
    active = sessions_data.get("active_sessions", [])

    for session in active:
        if session["session_id"] == session_id:
            session["last_heartbeat"] = datetime.now().isoformat()
            save_sessions(sessions_data)
            return {
                "success": True,
                "message": "Heartbeat updated"
            }

    return {
        "success": False,
        "message": f"Session {session_id} not found"
    }


def end_session(session_id: str, status: str = "completed") -> Dict[str, Any]:
    """
    End a session and move it to completed or failed.

    Args:
        session_id: The session to end
        status: "completed" or "failed"

    Returns:
        {
            "success": bool,
            "message": str,
            "locks_released": list
        }
    """
    sessions_data = load_sessions()
    active = sessions_data.get("active_sessions", [])

    for session in active:
        if session["session_id"] == session_id:
            # Release all locks held by this session
            locks_released = []
            if session.get("locks_held"):
                locks_data = load_locks()
                locks = locks_data.get("locks", [])
                for lock_id in session["locks_held"]:
                    locks = [l for l in locks if l["lock_id"] != lock_id]
                    locks_released.append(lock_id)
                locks_data["locks"] = locks
                save_locks(locks_data)

            # Move session to appropriate list
            active.remove(session)
            session["status"] = status
            session["ended_at"] = datetime.now().isoformat()

            if status == "completed":
                completed = sessions_data.get("completed_sessions", [])
                completed.append(session)
                sessions_data["completed_sessions"] = completed
            else:
                failed = sessions_data.get("failed_sessions", [])
                failed.append(session)
                sessions_data["failed_sessions"] = failed

            sessions_data["active_sessions"] = active
            save_sessions(sessions_data)

            return {
                "success": True,
                "message": f"Session ended: {status}",
                "locks_released": locks_released
            }

    return {
        "success": False,
        "message": f"Session {session_id} not found",
        "locks_released": []
    }


def cleanup_stale() -> Dict[str, Any]:
    """
    Clean up stale locks and unresponsive sessions.

    Returns:
        {
            "locks_cleaned": int,
            "sessions_cleaned": int,
            "details": list
        }
    """
    details = []
    locks_cleaned = 0
    sessions_cleaned = 0

    # Clean stale locks
    locks_data = load_locks()
    locks = locks_data.get("locks", [])
    now = datetime.now()

    active_locks = []
    for lock in locks:
        expires_at = datetime.fromisoformat(lock["expires_at"])
        if expires_at <= now:
            locks_cleaned += 1
            details.append(f"Released stale lock: {lock['lock_id']} on {lock['file_path']}")
        else:
            active_locks.append(lock)

    locks_data["locks"] = active_locks
    save_locks(locks_data)

    # Clean unresponsive sessions
    sessions_data = load_sessions()
    active = sessions_data.get("active_sessions", [])

    responsive_sessions = []
    for session in active:
        last_heartbeat = datetime.fromisoformat(session["last_heartbeat"])
        if (now - last_heartbeat).total_seconds() > HEARTBEAT_TIMEOUT_SECONDS:
            sessions_cleaned += 1
            session["status"] = "terminated"
            session["ended_at"] = now.isoformat()
            session["termination_reason"] = "heartbeat_timeout"

            failed = sessions_data.get("failed_sessions", [])
            failed.append(session)
            sessions_data["failed_sessions"] = failed

            details.append(f"Terminated unresponsive session: {session['session_id']}")
        else:
            responsive_sessions.append(session)

    sessions_data["active_sessions"] = responsive_sessions
    save_sessions(sessions_data)

    return {
        "locks_cleaned": locks_cleaned,
        "sessions_cleaned": sessions_cleaned,
        "details": details
    }


def get_status() -> Dict[str, Any]:
    """
    Get current coordination status.

    Returns:
        {
            "locks": {
                "total": int,
                "active": int,
                "by_agent": dict
            },
            "sessions": {
                "active": int,
                "completed": int,
                "failed": int,
                "capacity_remaining": int
            },
            "health": str
        }
    """
    locks_data = load_locks()
    sessions_data = load_sessions()

    locks = locks_data.get("locks", [])
    active_sessions = sessions_data.get("active_sessions", [])
    completed_sessions = sessions_data.get("completed_sessions", [])
    failed_sessions = sessions_data.get("failed_sessions", [])

    # Count active locks (not expired)
    now = datetime.now()
    active_locks = [l for l in locks if datetime.fromisoformat(l["expires_at"]) > now]

    # Group locks by agent
    locks_by_agent = {}
    for lock in active_locks:
        agent = lock["agent_id"]
        locks_by_agent[agent] = locks_by_agent.get(agent, 0) + 1

    # Determine health
    health = "HEALTHY"
    if len(active_sessions) >= MAX_CONCURRENT_AGENTS * 0.9:
        health = "WARNING"
    if len(active_sessions) >= MAX_CONCURRENT_AGENTS:
        health = "CRITICAL"

    return {
        "locks": {
            "total": len(locks),
            "active": len(active_locks),
            "by_agent": locks_by_agent
        },
        "sessions": {
            "active": len(active_sessions),
            "completed": len(completed_sessions),
            "failed": len(failed_sessions),
            "capacity_remaining": MAX_CONCURRENT_AGENTS - len(active_sessions)
        },
        "health": health
    }


def main():
    parser = argparse.ArgumentParser(description="Agent Coordinator")
    parser.add_argument("--acquire-lock", nargs=3, metavar=("AGENT_ID", "TASK_ID", "FILE_PATH"),
                        help="Acquire lock on a file")
    parser.add_argument("--release-lock", nargs=2, metavar=("AGENT_ID", "FILE_PATH"),
                        help="Release lock on a file")
    parser.add_argument("--check-lock", metavar="FILE_PATH",
                        help="Check if file is locked")
    parser.add_argument("--extend-lock", nargs=2, metavar=("AGENT_ID", "FILE_PATH"),
                        help="Extend lock timeout")
    parser.add_argument("--register-session", nargs=2, metavar=("AGENT_ID", "TASK_ID"),
                        help="Register a new session")
    parser.add_argument("--agent-type", default="unknown",
                        help="Agent type for session registration")
    parser.add_argument("--heartbeat", metavar="SESSION_ID",
                        help="Update session heartbeat")
    parser.add_argument("--end-session", nargs=2, metavar=("SESSION_ID", "STATUS"),
                        help="End a session (completed/failed)")
    parser.add_argument("--cleanup-stale", action="store_true",
                        help="Clean up stale locks and sessions")
    parser.add_argument("--status", action="store_true",
                        help="Get current coordination status")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()
    result = None

    if args.acquire_lock:
        agent_id, task_id, file_path = args.acquire_lock
        result = acquire_lock(agent_id, task_id, file_path)

    elif args.release_lock:
        agent_id, file_path = args.release_lock
        result = release_lock(agent_id, file_path)

    elif args.check_lock:
        result = check_lock(args.check_lock)

    elif args.extend_lock:
        agent_id, file_path = args.extend_lock
        result = extend_lock(agent_id, file_path)

    elif args.register_session:
        agent_id, task_id = args.register_session
        result = register_session(agent_id, task_id, args.agent_type)

    elif args.heartbeat:
        result = heartbeat(args.heartbeat)

    elif args.end_session:
        session_id, status = args.end_session
        result = end_session(session_id, status)

    elif args.cleanup_stale:
        result = cleanup_stale()

    elif args.status:
        result = get_status()

    else:
        parser.print_help()
        sys.exit(1)

    if args.json or result:
        print(json.dumps(result, indent=2))
        if result and not result.get("success", True):
            sys.exit(1)


if __name__ == "__main__":
    main()
