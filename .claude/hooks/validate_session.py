#!/usr/bin/env python3
"""Validate session.json for meaningful project/user/stage values."""

import json
import sys
import os
from pathlib import Path

INVALID_VALUES = ['', 'unknown', 'pending', 'system', 'none', 'null']

def load_session(project_dir):
    """Load session.json."""
    session_file = Path(project_dir) / '_state' / 'session.json'
    if not session_file.exists():
        return None
    try:
        with open(session_file) as f:
            return json.load(f)
    except:
        return None

def validate_session(project_dir, require_stage=False):
    """Validate session.json has meaningful values.

    Args:
        project_dir: Project root directory
        require_stage: If True, also validate stage field

    Returns:
        (is_valid, error_messages)
    """
    session = load_session(project_dir)
    errors = []

    if not session:
        errors.append("Session file missing: _state/session.json")
        return False, errors

    # Check project
    project = session.get('project', '').lower()
    if project in INVALID_VALUES:
        errors.append(f"Project name is invalid: '{session.get('project')}'")
        errors.append("Run /project-init to set a meaningful project name")

    # Check user
    user = session.get('user', '').lower()
    if user in INVALID_VALUES:
        errors.append(f"User name is invalid: '{session.get('user')}'")
        errors.append("Run /project-init to capture user information")

    # Check stage (if required)
    if require_stage:
        stage = session.get('stage', '').lower()
        if stage in INVALID_VALUES:
            errors.append(f"Stage is invalid: '{session.get('stage')}'")

    return len(errors) == 0, errors

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-dir', default=os.environ.get('CLAUDE_PROJECT_DIR', '.'))
    parser.add_argument('--require-stage', action='store_true')
    parser.add_argument('--quiet', action='store_true', help='Exit code only, no output')
    parser.add_argument('--warn-only', action='store_true', help='Show warnings but exit 0 (non-blocking)')
    args = parser.parse_args()

    is_valid, errors = validate_session(args.project_dir, args.require_stage)

    if not is_valid:
        if not args.quiet:
            print("\n" + "="*60, file=sys.stderr)
            print("⚠️  SESSION VALIDATION WARNING", file=sys.stderr)
            print("="*60, file=sys.stderr)
            for error in errors:
                print(f"   {error}", file=sys.stderr)
            print("\n💡 Run /project-init to fix these warnings", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)

        # If warn-only mode, exit 0 (allow continuation)
        # Otherwise exit 1 (block execution)
        sys.exit(0 if args.warn_only else 1)
    else:
        if not args.quiet:
            print("✅ Session validation passed")
        sys.exit(0)
