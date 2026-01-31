#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""File Lock Acquisition Hook

Acquires file-level locks to prevent concurrent modifications by multiple agents.
Called via PreToolUse(Write|Edit) hook in implementation agents.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Read stdin for tool input
input_data = json.load(sys.stdin)
tool_input = input_data.get('tool_input', {})
file_path = tool_input.get('file_path', 'unknown')
session_id = input_data.get('session_id', 'unknown')

# Load lock registry
lock_file = Path('_state/agent_lock.json')
locks = []
if lock_file.exists():
    with open(lock_file, 'r') as f:
        locks = json.load(f).get('locks', [])

# Check for existing lock
for lock in locks:
    if lock['file_path'] == file_path:
        expires_at = datetime.fromisoformat(lock['expires_at'])
        if datetime.now() < expires_at:
            print(f"FILE_LOCKED: {file_path} by {lock['agent_id']}")
            sys.exit(1)  # Block (locked)

# Acquire lock
lock_entry = {
    'lock_id': f"lock-{session_id}-{file_path.replace('/', '-')}",
    'file_path': file_path,
    'agent_id': os.getenv('AGENT_ID', session_id),
    'session_id': session_id,
    'acquired_at': datetime.now().isoformat(),
    'expires_at': (datetime.now() + timedelta(minutes=15)).isoformat()
}
locks.append(lock_entry)

# Ensure _state directory exists
lock_file.parent.mkdir(parents=True, exist_ok=True)

# Write back
with open(lock_file, 'w') as f:
    json.dump({'locks': locks}, f, indent=2)

print(f"LOCK_ACQUIRED: {file_path}")
sys.exit(0)
