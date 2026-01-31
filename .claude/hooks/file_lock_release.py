#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""File Lock Release Hook

Releases file-level locks acquired by the current agent session.
Called via PostToolUse(Write|Edit) hook in implementation agents.
"""

import json
import sys
import os
from pathlib import Path

# Read stdin for tool input
input_data = json.load(sys.stdin)
session_id = input_data.get('session_id', 'unknown')

# Load lock registry
lock_file = Path('_state/agent_lock.json')
locks = []
if lock_file.exists():
    with open(lock_file, 'r') as f:
        locks = json.load(f).get('locks', [])

# Remove locks for this session
locks = [lock for lock in locks if lock['session_id'] != session_id]

# Write back
with open(lock_file, 'w') as f:
    json.dump({'locks': locks}, f, indent=2)

print(f"LOCKS_RELEASED: session {session_id}")
sys.exit(0)
