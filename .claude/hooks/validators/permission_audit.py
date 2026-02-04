#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Permission Audit - HTEC PermissionRequest Hook

Logs all permission requests to _state/permission_audit.json.
Auto-allows read-only operations, logs write operations for audit.

Exit Codes:
- 0: Always (logging only, never blocks)

Usage (as PermissionRequest hook):
    Input via stdin: {"prompts": [{"tool": "Bash", "prompt": "run tests"}], ...}

    Output: Confirmation message to stderr
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def get_project_dir():
    """Get project directory from environment or current directory."""
    return os.getenv('CLAUDE_PROJECT_DIR', os.getcwd())


def ensure_state_dir():
    """Ensure _state directory exists."""
    state_dir = Path(get_project_dir()) / '_state'
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


def classify_operation(prompts):
    """
    Classify the permission request as read-only or write.

    Returns:
        Tuple of (is_read_only, operation_summary)
    """
    read_only_keywords = [
        'read', 'view', 'list', 'show', 'display', 'get', 'fetch',
        'search', 'find', 'check', 'status', 'info', 'help'
    ]

    write_keywords = [
        'write', 'edit', 'delete', 'remove', 'create', 'modify',
        'update', 'install', 'run', 'execute', 'npm', 'pip', 'deploy'
    ]

    operations = []
    is_write = False

    for p in prompts:
        tool = p.get('tool', 'unknown')
        prompt = p.get('prompt', '').lower()
        operations.append(f"{tool}: {prompt[:50]}")

        # Check if any write keyword is present
        for kw in write_keywords:
            if kw in prompt:
                is_write = True
                break

    return (not is_write), operations


def log_permission_request(input_data):
    """
    Log permission request to audit file.

    Args:
        input_data: Hook input with prompts, session_id, etc.

    Returns:
        dict with audit entry details
    """
    state_dir = ensure_state_dir()
    audit_file = state_dir / 'permission_audit.json'

    # Extract request details
    session_id = input_data.get('session_id', os.getenv('CLAUDE_SESSION_ID', 'unknown'))
    prompts = input_data.get('prompts', [])

    is_read_only, operations = classify_operation(prompts)

    # Build audit entry
    entry = {
        'timestamp': datetime.now().isoformat(),
        'session_id': session_id,
        'is_read_only': is_read_only,
        'operations': operations,
        'raw_prompts': prompts[:5],  # Limit for safety
        'auto_action': 'allowed' if is_read_only else 'logged_for_review'
    }

    # Append to audit log (JSON lines format)
    with open(audit_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

    return entry


def main():
    """
    Main entry point. Reads JSON from stdin, logs audit entry.
    """
    # Read all stdin
    raw_input = sys.stdin.read().strip()

    if not raw_input:
        print("AUDIT: No permission request data", file=sys.stderr)
        sys.exit(0)

    try:
        input_data = json.loads(raw_input)
    except json.JSONDecodeError:
        print("AUDIT: Invalid JSON input", file=sys.stderr)
        sys.exit(0)

    entry = log_permission_request(input_data)

    # Output confirmation (to stderr so it doesn't interfere with hook response)
    ops = ', '.join(entry['operations'][:3])
    status = "auto-allowed" if entry['is_read_only'] else "logged"
    print(f"AUDIT: {status} - {ops}", file=sys.stderr)

    # Always exit 0 (audit-only, never blocks)
    sys.exit(0)


if __name__ == "__main__":
    main()
