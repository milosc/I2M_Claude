#!/usr/bin/env python3
"""Update user field in session.json."""

import json
import sys
from pathlib import Path
from datetime import datetime

def update_user(project_dir, user_name):
    """Update user field in session.json."""
    session_file = Path(project_dir) / '_state' / 'session.json'

    if not session_file.exists():
        print(f"ERROR: Session file not found: {session_file}", file=sys.stderr)
        sys.exit(1)

    # Load current session
    with open(session_file) as f:
        session = json.load(f)

    # Update user field
    session['user'] = user_name
    session['updated_at'] = datetime.now().isoformat()

    # Write back
    with open(session_file, 'w') as f:
        json.dump(session, f, indent=2)

    print(f"✅ Updated user to: {user_name}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: update_session_user.py <username>", file=sys.stderr)
        sys.exit(1)

    import os
    project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
    update_user(project_dir, sys.argv[1])
