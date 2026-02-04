#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Capture Failure - HTEC PostToolUseFailure Hook

Captures structured error information when tool calls fail.
Appends to _state/lifecycle.json with error details.

Exit Codes:
- 0: Always (logging only, never blocks)

Usage (as PostToolUseFailure hook):
    Input via stdin: {
        "tool_name": "Bash",
        "tool_input": {...},
        "error": "Command failed with exit code 1"
    }

    Output: Structured error logged to lifecycle.json
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


def load_session_context():
    """Load session context from _state/session.json."""
    session_file = Path(get_project_dir()) / '_state' / 'session.json'
    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def classify_error(tool_name, error_message):
    """
    Classify the error for better analysis.

    Returns:
        Tuple of (error_category, severity)
    """
    error_lower = error_message.lower() if error_message else ''

    # Severity levels: critical, high, medium, low
    if 'permission denied' in error_lower or 'access denied' in error_lower:
        return 'permission_error', 'high'

    if 'not found' in error_lower or 'no such file' in error_lower:
        return 'file_not_found', 'medium'

    if 'timeout' in error_lower or 'timed out' in error_lower:
        return 'timeout', 'high'

    if 'syntax error' in error_lower or 'parse error' in error_lower:
        return 'syntax_error', 'medium'

    if 'module not found' in error_lower or 'import error' in error_lower:
        return 'module_error', 'medium'

    if 'connection' in error_lower or 'network' in error_lower:
        return 'network_error', 'high'

    if 'exit code' in error_lower:
        return 'command_failure', 'medium'

    return 'unknown', 'low'


def capture_failure(input_data):
    """
    Capture and log tool failure with context.

    Args:
        input_data: Hook input with tool_name, tool_input, error

    Returns:
        dict with failure entry details
    """
    state_dir = ensure_state_dir()
    lifecycle_file = state_dir / 'lifecycle.json'

    # Get session context
    session_context = load_session_context()
    session_id = input_data.get('session_id', os.getenv('CLAUDE_SESSION_ID', 'unknown'))

    # Extract failure details
    tool_name = input_data.get('tool_name', 'unknown')
    tool_input = input_data.get('tool_input', {})
    error_message = input_data.get('error', 'Unknown error')

    # Classify the error
    error_category, severity = classify_error(tool_name, error_message)

    # Build failure entry
    entry = {
        'event_type': 'ToolFailure',
        'timestamp': datetime.now().isoformat(),
        'session_id': session_id,
        'project': session_context.get('project', 'unknown'),
        'stage': session_context.get('stage', 'unknown'),
        'component': 'tool_failure',
        'name': tool_name,
        'event': 'failed',
        'error': {
            'message': error_message[:500],  # Truncate long errors
            'category': error_category,
            'severity': severity
        },
        'tool_input_summary': _summarize_tool_input(tool_name, tool_input)
    }

    # Append to lifecycle.json
    with open(lifecycle_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

    return entry


def _summarize_tool_input(tool_name, tool_input):
    """Create a safe summary of tool input for logging."""
    if not tool_input:
        return {}

    summary = {}

    if tool_name == 'Bash':
        cmd = tool_input.get('command', '')
        summary['command'] = cmd[:100] if cmd else ''

    elif tool_name == 'Read':
        summary['file_path'] = tool_input.get('file_path', '')[:200]

    elif tool_name == 'Write' or tool_name == 'Edit':
        summary['file_path'] = tool_input.get('file_path', '')[:200]
        content = tool_input.get('content', '')
        summary['content_length'] = len(content) if content else 0

    elif tool_name == 'Task':
        summary['subagent_type'] = tool_input.get('subagent_type', 'unknown')
        summary['description'] = tool_input.get('description', '')[:100]

    else:
        # Generic summary - just get first few keys
        for key in list(tool_input.keys())[:3]:
            val = tool_input[key]
            if isinstance(val, str):
                summary[key] = val[:100]
            elif isinstance(val, (int, float, bool)):
                summary[key] = val

    return summary


def main():
    """
    Main entry point. Reads JSON from stdin, logs failure.
    """
    # Read all stdin
    raw_input = sys.stdin.read().strip()

    if not raw_input:
        print("FAILURE: No failure data provided", file=sys.stderr)
        sys.exit(0)

    try:
        input_data = json.loads(raw_input)
    except json.JSONDecodeError:
        print("FAILURE: Invalid JSON input", file=sys.stderr)
        sys.exit(0)

    entry = capture_failure(input_data)

    # Output confirmation to stderr
    tool = entry['name']
    category = entry['error']['category']
    severity = entry['error']['severity']
    print(f"FAILURE_CAPTURED: {tool} - {category} ({severity})", file=sys.stderr)

    # Output JSON to stdout for hook parsing
    result = {
        "logged": True,
        "tool_name": tool,
        "error_category": category,
        "severity": severity,
        "timestamp": entry['timestamp']
    }
    print(json.dumps(result, indent=2))

    # Always exit 0 (logging only)
    sys.exit(0)


if __name__ == "__main__":
    main()
