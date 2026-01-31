#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""TDD Compliance Check Hook

Validates TDD phase compliance (RED → GREEN → REFACTOR).
Called via PostToolUse(Write|Edit) hook in implementation agents.

Warns if:
- Writing tests in non-RED phase
- Writing implementation in non-GREEN phase

Does NOT block execution (exit 0 always).
"""

import json
import sys
import os
from pathlib import Path

# Read stdin for tool input
input_data = json.load(sys.stdin)
tool_input = input_data.get('tool_input', {})
file_path = tool_input.get('file_path', 'unknown')

# Check if test file or implementation file
is_test = 'test' in file_path or 'spec' in file_path

# Load TDD state (_state/tdd_state.json)
tdd_state_file = Path('_state/tdd_state.json')
tdd_state = {}
if tdd_state_file.exists():
    with open(tdd_state_file, 'r') as f:
        tdd_state = json.load(f)

current_phase = tdd_state.get('phase', 'UNKNOWN')

# TDD Phase Validation
if is_test and current_phase != 'RED':
    print(f"⚠️  TDD_WARNING: Writing test in {current_phase} phase (expected RED)")
    # Don't block, just warn
elif not is_test and current_phase != 'GREEN':
    print(f"⚠️  TDD_WARNING: Writing implementation in {current_phase} phase (expected GREEN)")

print(f"TDD_CHECK: {file_path} in {current_phase} phase")
sys.exit(0)
