#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["python-dotenv"]
# ///

"""
Universal event capture script for HTEC framework.
Captures all Claude Code hook events with full context.
"""

import json
import sys
import os
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
        with open(session_file, 'r') as f:
            return json.load(f)
    return {}

def save_call_stack(session_id, call_stack):
    """Save call stack for session."""
    state_dir = ensure_state_dir()
    stack_file = state_dir / f'call_stack_{session_id}.json'
    with open(stack_file, 'w') as f:
        json.dump({'session_id': session_id, 'stack': call_stack}, f, indent=2)

def load_call_stack(session_id):
    """Load call stack for session."""
    state_dir = ensure_state_dir()
    stack_file = state_dir / f'call_stack_{session_id}.json'
    if stack_file.exists():
        with open(stack_file, 'r') as f:
            data = json.load(f)
            return data.get('stack', [])
    return []

def extract_agent_name(tool_input):
    """
    Extract agent name from Task tool input.
    Looks for patterns:
    1. "Agent: agent-name" in prompt
    2. "Read: .claude/agents/agent-name.md" in prompt
    3. Falls back to subagent_type
    """
    if 'prompt' in tool_input:
        prompt = tool_input['prompt']

        # Pattern 1: "Agent: name"
        import re
        match = re.search(r'Agent:\s*([a-zA-Z0-9_-]+)', prompt, re.IGNORECASE)
        if match:
            return match.group(1)

        # Pattern 2: "Read: .claude/agents/name.md"
        match = re.search(r'Read:\s*\.claude/agents/([a-zA-Z0-9_-]+)\.md', prompt, re.IGNORECASE)
        if match:
            return match.group(1)

    # Pattern 3: subagent_type
    return tool_input.get('subagent_type', 'unknown')

def capture_event(event_type, input_data):
    """
    Capture event with full context.

    event_type: PreToolUse, PostToolUse, UserPromptSubmit, SubagentStop, etc.
    input_data: JSON from stdin
    """
    state_dir = ensure_state_dir()
    lifecycle_file = state_dir / 'lifecycle.json'

    # Get session context
    session_context = load_session_context()
    session_id = input_data.get('session_id', os.getenv('CLAUDE_SESSION_ID', 'unknown'))
    project_name = session_context.get('project', 'unknown')
    stage = session_context.get('stage', 'unknown')

    # Load call stack for this session
    call_stack = load_call_stack(session_id)

    # Build event entry
    event = {
        'event_type': event_type,
        'timestamp': datetime.now().isoformat(),
        'session_id': session_id,
        'project': project_name,
        'stage': stage,
        'call_stack': call_stack,
        'payload': input_data
    }

    # Event-specific processing
    if event_type == 'PreToolUse':
        tool_name = input_data.get('tool_name', 'unknown')
        event['tool_name'] = tool_name

        if tool_name == 'Task':
            # Agent spawn
            tool_input = input_data.get('tool_input', {})
            agent_name = extract_agent_name(tool_input)
            event['component'] = 'agent'
            event['name'] = agent_name
            event['event'] = 'pre_spawn'
            event['model'] = tool_input.get('model', 'unknown')
            event['subagent_type'] = tool_input.get('subagent_type', 'unknown')

            # Store in pending spawns for linking
            pending_file = state_dir / 'pending_spawns.json'
            pending = []
            if pending_file.exists():
                with open(pending_file, 'r') as f:
                    pending = json.load(f)
            pending.append({
                'agent_name': agent_name,
                'parent_session': session_id,
                'timestamp': event['timestamp'],
                'call_stack': call_stack + [agent_name]
            })
            with open(pending_file, 'w') as f:
                json.dump(pending, f, indent=2)

        elif tool_name == 'Skill':
            # Skill invocation
            tool_input = input_data.get('tool_input', {})
            skill_name = tool_input.get('skill', 'unknown')
            event['component'] = 'skill'
            event['name'] = skill_name
            event['event'] = 'pre_invoke'

    elif event_type == 'PostToolUse':
        tool_name = input_data.get('tool_name', 'unknown')
        event['tool_name'] = tool_name

        if tool_name == 'Task':
            # Agent completion
            tool_input = input_data.get('tool_input', {})
            agent_name = extract_agent_name(tool_input)
            event['component'] = 'agent'
            event['name'] = agent_name
            event['event'] = 'post_spawn'

        elif tool_name == 'Skill':
            # Skill completion
            tool_input = input_data.get('tool_input', {})
            skill_name = tool_input.get('skill', 'unknown')
            event['component'] = 'skill'
            event['name'] = skill_name
            event['event'] = 'post_invoke'

    elif event_type == 'SessionStart':
        # Check if this is a subagent session
        pending_file = state_dir / 'pending_spawns.json'
        if pending_file.exists():
            with open(pending_file, 'r') as f:
                pending = json.load(f)

            # Find matching spawn (most recent)
            if pending:
                spawn = pending[-1]  # Most recent spawn
                parent_session = spawn['parent_session']
                call_stack = spawn['call_stack']

                # Update this session's call stack
                save_call_stack(session_id, call_stack)
                event['parent_session'] = parent_session
                event['call_stack'] = call_stack
                event['component'] = 'session'
                event['name'] = 'subagent'
                event['event'] = 'started'

                # Remove from pending
                pending.pop()
                with open(pending_file, 'w') as f:
                    json.dump(pending, f, indent=2)
        else:
            # Main session
            event['component'] = 'session'
            event['name'] = 'main'
            event['event'] = 'started'

    elif event_type == 'SubagentStop':
        event['component'] = 'subagent'
        event['name'] = 'unknown'  # TODO: extract from context
        event['event'] = 'stopped'

    elif event_type == 'UserPromptSubmit':
        prompt = input_data.get('prompt', '')
        event['component'] = 'user_prompt'
        event['name'] = 'prompt'
        event['event'] = 'submitted'
        event['prompt_text'] = prompt[:200]  # Truncate for readability

    # Append to lifecycle.json
    with open(lifecycle_file, 'a') as f:
        f.write(json.dumps(event) + '\n')

    # Optionally send to observability server (if running)
    try:
        import urllib.request
        server_url = 'http://localhost:4000/events'
        req = urllib.request.Request(
            server_url,
            data=json.dumps(event).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req, timeout=1)
    except:
        pass  # Fail silently if server not running

    return event

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--event-type', required=True, help='Hook event type')
    args = parser.parse_args()

    # Read input from stdin
    input_data = json.load(sys.stdin)

    # Capture event
    event = capture_event(args.event_type, input_data)

    # Output confirmation
    print(f"CAPTURED: {event.get('component', 'event')}:{event.get('name', 'unknown')}:{event.get('event', args.event_type)}")

    sys.exit(0)

if __name__ == '__main__':
    main()
