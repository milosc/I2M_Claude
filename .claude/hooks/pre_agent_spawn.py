#!/usr/bin/env python3
"""
Pre-Agent Spawn Hook - Validation before spawning agents.

This hook is called before spawning any agent to:
1. Validate capacity (not exceeding MAX_CONCURRENT_AGENTS)
2. Validate file locks for exclusive access agents
3. Check process integrity status
4. Register the session

Usage:
    python3 pre_agent_spawn.py --agent-id <id> --task-id <id> --agent-type <type> [--files <files>]
    python3 pre_agent_spawn.py --validate-only --agent-type <type> [--files <files>]

Exit codes:
    0 - Spawn allowed
    1 - Spawn blocked (check output for reason)
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional


# Import coordinator functions
sys.path.insert(0, str(Path(__file__).parent))
from agent_coordinator import (
    load_sessions, load_locks, acquire_lock, register_session,
    get_status, MAX_CONCURRENT_AGENTS
)

# Import pipeline logger
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "_state"))
try:
    from pipeline_logger import get_logger
    PIPELINE_LOGGING_ENABLED = True
except ImportError:
    PIPELINE_LOGGING_ENABLED = False
    print("Warning: Pipeline logging not available")


# Agent type configurations - UNIFIED NAMING CONVENTION
# All agents use hyphenated stage-prefix format: {stage}-{agent-name}
# This matches the file structure in .claude/agents/
AGENT_CONFIGS = {
    # ==========================================================================
    # STAGE 1: DISCOVERY AGENTS
    # ==========================================================================
    "discovery-orchestrator": {
        "category": "discovery",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": ["_state/discovery_config.json"],
        "can_spawn_parallel": False
    },
    "discovery-interview-analyst": {
        "category": "discovery",
        "model": "sonnet",
        "max_instances": 3,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "discovery-pdf-analyst": {
        "category": "discovery",
        "model": "sonnet",
        "max_instances": 2,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "discovery-data-analyst": {
        "category": "discovery",
        "model": "haiku",  # Structured data extraction
        "max_instances": 3,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "discovery-design-analyst": {
        "category": "discovery",
        "model": "haiku",  # Visual pattern analysis
        "max_instances": 3,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "discovery-pain-point-validator": {
        "category": "discovery",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "discovery-persona-generator": {
        "category": "discovery",
        "model": "sonnet",
        "max_instances": 3,  # One per persona
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "discovery-jtbd-extractor": {
        "category": "discovery",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "discovery-cross-reference-validator": {
        "category": "discovery",
        "model": "haiku",  # ID validation is rule-based
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },

    # ==========================================================================
    # STAGE 2: PROTOTYPE AGENTS
    # ==========================================================================
    "prototype-orchestrator": {
        "category": "prototype",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": ["_state/pipeline_config.json"],
        "can_spawn_parallel": False
    },
    "prototype-data-model-specifier": {
        "category": "prototype",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "prototype-api-contract-specifier": {
        "category": "prototype",
        "model": "haiku",  # OpenAPI schema is structured/templated
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "prototype-design-token-generator": {
        "category": "prototype",
        "model": "haiku",  # JSON token generation is templated
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "prototype-component-specifier": {
        "category": "prototype",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "prototype-screen-specifier": {
        "category": "prototype",
        "model": "sonnet",
        "max_instances": 5,  # Parallel per screen group
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "prototype-ux-validator": {
        "category": "prototype",
        "model": "haiku",  # Pattern-based validation
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "prototype-component-validator": {
        "category": "prototype",
        "model": "haiku",  # Schema compliance check
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "prototype-screen-validator": {
        "category": "prototype",
        "model": "haiku",  # Coverage validation
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "prototype-accessibility-auditor": {
        "category": "prototype",
        "model": "haiku",  # WCAG checklist-based
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "prototype-visual-qa-tester": {
        "category": "prototype",
        "model": "sonnet",  # Visual comparison needs reasoning
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },

    # ==========================================================================
    # STAGE 3: PRODUCTSPECS AGENTS
    # ==========================================================================
    "productspecs-orchestrator": {
        "category": "productspecs",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "productspecs-ui-module-specifier": {
        "category": "productspecs",
        "model": "sonnet",
        "max_instances": 3,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "productspecs-api-module-specifier": {
        "category": "productspecs",
        "model": "sonnet",
        "max_instances": 3,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "productspecs-nfr-generator": {
        "category": "productspecs",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "productspecs-unit-test-specifier": {
        "category": "productspecs",
        "model": "sonnet",
        "max_instances": 2,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "productspecs-integration-test-specifier": {
        "category": "productspecs",
        "model": "sonnet",
        "max_instances": 2,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "productspecs-e2e-test-specifier": {
        "category": "productspecs",
        "model": "sonnet",
        "max_instances": 2,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "productspecs-pict-combinatorial": {
        "category": "productspecs",
        "model": "haiku",  # Algorithmic pairwise generation
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "productspecs-traceability-validator": {
        "category": "productspecs",
        "model": "haiku",  # ID chain validation
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "productspecs-cross-reference-validator": {
        "category": "productspecs",
        "model": "haiku",  # Reference integrity check
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "productspecs-spec-reviewer": {
        "category": "productspecs",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },

    # ==========================================================================
    # STAGE 4: SOLARCH AGENTS
    # ==========================================================================
    "solarch-orchestrator": {
        "category": "solarch",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "solarch-tech-researcher": {
        "category": "solarch",
        "model": "sonnet",
        "max_instances": 2,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "solarch-integration-analyst": {
        "category": "solarch",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "solarch-cost-estimator": {
        "category": "solarch",
        "model": "haiku",  # Formula-based calculation
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "solarch-c4-context-generator": {
        "category": "solarch",
        "model": "haiku",  # Structured diagram generation
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "solarch-c4-container-generator": {
        "category": "solarch",
        "model": "haiku",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "solarch-c4-component-generator": {
        "category": "solarch",
        "model": "haiku",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "solarch-c4-deployment-generator": {
        "category": "solarch",
        "model": "haiku",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "solarch-performance-scenarios": {
        "category": "solarch",
        "model": "haiku",  # Template-based scenarios
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "solarch-security-scenarios": {
        "category": "solarch",
        "model": "haiku",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "solarch-reliability-scenarios": {
        "category": "solarch",
        "model": "haiku",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "solarch-usability-scenarios": {
        "category": "solarch",
        "model": "haiku",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "solarch-adr-foundation-writer": {
        "category": "solarch",
        "model": "sonnet",  # ADRs need reasoning
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "solarch-adr-communication-writer": {
        "category": "solarch",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "solarch-adr-operational-writer": {
        "category": "solarch",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "solarch-adr-validator": {
        "category": "solarch",
        "model": "haiku",  # Consistency checking
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "solarch-arch-evaluator": {
        "category": "solarch",
        "model": "sonnet",  # ATAM analysis needs reasoning
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "solarch-risk-scorer": {
        "category": "solarch",
        "model": "haiku",  # Formula-based scoring
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },

    # ==========================================================================
    # STAGE 5: IMPLEMENTATION AGENTS
    # ==========================================================================
    # Planning layer
    "planning-tech-lead": {
        "category": "planning",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": ["traceability/task_registry.json"],
        "can_spawn_parallel": False
    },
    "planning-product-researcher": {
        "category": "planning",
        "model": "haiku",
        "max_instances": 2,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "planning-hfe-ux-researcher": {
        "category": "planning",
        "model": "haiku",
        "max_instances": 2,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "planning-code-explorer": {
        "category": "planning",
        "model": "sonnet",
        "max_instances": 3,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },

    # Implementation layer
    "implementation-developer": {
        "category": "implementation",
        "model": "sonnet",
        "max_instances": 3,
        "requires_exclusive_files": [],  # Files specified per-task
        "can_spawn_parallel": True
    },
    "implementation-test-automation-engineer": {
        "category": "implementation",
        "model": "sonnet",
        "max_instances": 2,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },

    # Quality layer (all parallel during code review)
    "quality-bug-hunter": {
        "category": "quality",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "quality-security-auditor": {
        "category": "quality",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "quality-code-quality": {
        "category": "quality",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "quality-test-coverage": {
        "category": "quality",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "quality-contracts-reviewer": {
        "category": "quality",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "quality-accessibility-auditor": {
        "category": "quality",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },

    # Process Integrity layer (monitoring)
    "process-integrity-traceability-guardian": {
        "category": "process-integrity",
        "model": "haiku",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "process-integrity-state-watchdog": {
        "category": "process-integrity",
        "model": "haiku",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "process-integrity-checkpoint-auditor": {
        "category": "process-integrity",
        "model": "haiku",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "process-integrity-playbook-enforcer": {
        "category": "process-integrity",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },

    # Reflexion layer
    "reflexion-actor": {
        "category": "reflexion",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    },
    "reflexion-evaluator": {
        "category": "reflexion",
        "model": "sonnet",
        "max_instances": 3,  # Multi-judge mode
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    },
    "reflexion-self-refiner": {
        "category": "reflexion",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": False
    }
}


def get_agent_config(agent_type: str) -> Dict[str, Any]:
    """Get configuration for an agent type."""
    return AGENT_CONFIGS.get(agent_type, {
        "category": "unknown",
        "model": "sonnet",
        "max_instances": 1,
        "requires_exclusive_files": [],
        "can_spawn_parallel": True
    })


def check_capacity() -> Dict[str, Any]:
    """Check if there's capacity for a new agent."""
    status = get_status()
    remaining = status["sessions"]["capacity_remaining"]

    if remaining <= 0:
        return {
            "allowed": False,
            "reason": f"Maximum concurrent agents ({MAX_CONCURRENT_AGENTS}) reached",
            "capacity_remaining": 0
        }

    return {
        "allowed": True,
        "reason": None,
        "capacity_remaining": remaining
    }


def check_instance_limit(agent_type: str) -> Dict[str, Any]:
    """Check if agent type has reached its instance limit."""
    config = get_agent_config(agent_type)
    max_instances = config.get("max_instances", 1)

    sessions_data = load_sessions()
    active = sessions_data.get("active_sessions", [])

    # Count active instances of this agent type
    instance_count = sum(1 for s in active if s.get("agent_type") == agent_type)

    if instance_count >= max_instances:
        return {
            "allowed": False,
            "reason": f"Agent type {agent_type} has reached max instances ({max_instances})",
            "current_instances": instance_count,
            "max_instances": max_instances
        }

    return {
        "allowed": True,
        "reason": None,
        "current_instances": instance_count,
        "max_instances": max_instances
    }


def check_file_availability(files: List[str], agent_id: str, task_id: str) -> Dict[str, Any]:
    """Check if required files are available (not locked by others)."""
    locks_data = load_locks()
    locks = locks_data.get("locks", [])

    blocked_files = []
    for file_path in files:
        for lock in locks:
            if lock["file_path"] == file_path and lock["agent_id"] != agent_id:
                blocked_files.append({
                    "file": file_path,
                    "locked_by": lock["agent_id"],
                    "task": lock["task_id"]
                })

    if blocked_files:
        return {
            "allowed": False,
            "reason": "Required files are locked",
            "blocked_files": blocked_files
        }

    return {
        "allowed": True,
        "reason": None,
        "blocked_files": []
    }


def check_integrity_status() -> Dict[str, Any]:
    """Check if process integrity allows spawning."""
    integrity_path = Path("_state/integrity_status.json")

    if not integrity_path.exists():
        return {
            "allowed": True,
            "reason": None,
            "integrity_status": "unknown"
        }

    with open(integrity_path, 'r') as f:
        integrity = json.load(f)

    # Check for active vetos
    if integrity.get("veto", {}).get("active"):
        veto = integrity["veto"]
        return {
            "allowed": False,
            "reason": f"Active veto from {veto.get('agent')}: {veto.get('reason')}",
            "integrity_status": "veto_active"
        }

    # Check for critical violations
    violations = integrity.get("violations", [])
    critical = [v for v in violations if v.get("severity") == "CRITICAL"]

    if critical:
        return {
            "allowed": False,
            "reason": f"{len(critical)} CRITICAL violation(s) must be resolved",
            "integrity_status": "critical_violations",
            "violations": critical
        }

    return {
        "allowed": True,
        "reason": None,
        "integrity_status": integrity.get("status", "healthy")
    }


def validate_spawn(
    agent_type: str,
    agent_id: Optional[str] = None,
    task_id: Optional[str] = None,
    files: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Validate if an agent can be spawned.

    Returns:
        {
            "allowed": bool,
            "reason": str or None,
            "checks": {
                "capacity": {...},
                "instance_limit": {...},
                "file_availability": {...},
                "integrity": {...}
            }
        }
    """
    checks = {}
    files = files or []

    # Get agent config for required files
    config = get_agent_config(agent_type)
    required_files = config.get("requires_exclusive_files", []) + files

    # 1. Check capacity
    checks["capacity"] = check_capacity()
    if not checks["capacity"]["allowed"]:
        return {
            "allowed": False,
            "reason": checks["capacity"]["reason"],
            "checks": checks
        }

    # 2. Check instance limit
    checks["instance_limit"] = check_instance_limit(agent_type)
    if not checks["instance_limit"]["allowed"]:
        return {
            "allowed": False,
            "reason": checks["instance_limit"]["reason"],
            "checks": checks
        }

    # 3. Check file availability
    if required_files and agent_id and task_id:
        checks["file_availability"] = check_file_availability(
            required_files, agent_id, task_id
        )
        if not checks["file_availability"]["allowed"]:
            return {
                "allowed": False,
                "reason": checks["file_availability"]["reason"],
                "checks": checks
            }

    # 4. Check integrity status
    checks["integrity"] = check_integrity_status()
    if not checks["integrity"]["allowed"]:
        return {
            "allowed": False,
            "reason": checks["integrity"]["reason"],
            "checks": checks
        }

    return {
        "allowed": True,
        "reason": None,
        "checks": checks
    }


def prepare_spawn(
    agent_id: str,
    task_id: str,
    agent_type: str,
    files: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Prepare for agent spawn: validate, register session, acquire locks.

    Returns:
        {
            "success": bool,
            "session_id": str or None,
            "locks_acquired": list,
            "message": str
        }
    """
    files = files or []

    # Validate first
    validation = validate_spawn(agent_type, agent_id, task_id, files)
    if not validation["allowed"]:
        return {
            "success": False,
            "session_id": None,
            "locks_acquired": [],
            "message": validation["reason"]
        }

    # Register session
    session_result = register_session(agent_id, task_id, agent_type)
    if not session_result["success"]:
        return {
            "success": False,
            "session_id": None,
            "locks_acquired": [],
            "message": session_result["message"]
        }

    session_id = session_result["session_id"]

    # Log agent spawn start to pipeline
    if PIPELINE_LOGGING_ENABLED:
        try:
            logger = get_logger()
            config = get_agent_config(agent_type)

            # Build activity data
            activity = {
                "type": "agent_spawn",
                "agent_id": agent_id,
                "agent_type": agent_type,
                "task_id": task_id,
                "model": config.get("model", "unknown"),
                "category": config.get("category", "unknown"),
                "intent": f"Spawn {agent_type} agent for task {task_id}"
            }

            # Get context from current pipeline state
            pipeline_state = logger._load_progress()
            context = pipeline_state.get("current_context", {})

            # Log the event
            event_id = logger.log_event(
                event_type="agent_spawn_start",
                level="agent",
                activity=activity,
                context=context
            )

            # Store event_id in session for matching with end event
            sessions = load_sessions()
            for session in sessions:
                if session["session_id"] == session_id:
                    session["pipeline_event_id"] = event_id
                    from agent_coordinator import save_sessions
                    save_sessions(sessions)
                    break

        except Exception as e:
            print(f"Warning: Failed to log agent spawn: {e}")

    # Acquire locks for required files
    config = get_agent_config(agent_type)
    required_files = config.get("requires_exclusive_files", []) + files
    locks_acquired = []

    for file_path in required_files:
        lock_result = acquire_lock(agent_id, task_id, file_path)
        if lock_result["success"]:
            locks_acquired.append({
                "file": file_path,
                "lock_id": lock_result["lock_id"]
            })
        else:
            # Rollback: release acquired locks
            from agent_coordinator import release_lock, end_session
            for lock in locks_acquired:
                release_lock(agent_id, lock["file"])
            end_session(session_id, "failed")

            return {
                "success": False,
                "session_id": None,
                "locks_acquired": [],
                "message": f"Failed to acquire lock: {lock_result['message']}"
            }

    return {
        "success": True,
        "session_id": session_id,
        "locks_acquired": locks_acquired,
        "message": "Spawn prepared successfully"
    }


def main():
    parser = argparse.ArgumentParser(description="Pre-Agent Spawn Hook")
    parser.add_argument("--agent-id", help="Agent ID")
    parser.add_argument("--task-id", help="Task ID")
    parser.add_argument("--agent-type", required=True, help="Agent type (e.g., implementation-developer)")
    parser.add_argument("--files", nargs="*", default=[], help="Files requiring exclusive access")
    parser.add_argument("--validate-only", action="store_true",
                        help="Only validate, don't register or acquire locks")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.validate_only:
        result = validate_spawn(
            agent_type=args.agent_type,
            agent_id=args.agent_id,
            task_id=args.task_id,
            files=args.files
        )
    else:
        if not args.agent_id or not args.task_id:
            print("Error: --agent-id and --task-id required for full spawn preparation")
            sys.exit(1)

        result = prepare_spawn(
            agent_id=args.agent_id,
            task_id=args.task_id,
            agent_type=args.agent_type,
            files=args.files
        )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result.get("allowed", result.get("success")):
            print(f"ALLOWED: {result.get('message', 'Spawn permitted')}")
            if result.get("session_id"):
                print(f"Session ID: {result['session_id']}")
            if result.get("locks_acquired"):
                print(f"Locks acquired: {len(result['locks_acquired'])}")
        else:
            print(f"BLOCKED: {result.get('reason', result.get('message'))}")

    # Exit code based on result
    if not result.get("allowed", result.get("success")):
        sys.exit(1)


if __name__ == "__main__":
    main()
