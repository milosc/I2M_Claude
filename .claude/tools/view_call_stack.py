#!/usr/bin/env python3
"""
View hierarchical call stack from lifecycle.json
"""

import json
from pathlib import Path
from collections import defaultdict

def load_lifecycle():
    lifecycle_file = Path('_state/lifecycle.json')
    events = []
    with open(lifecycle_file, 'r') as f:
        for line in f:
            events.append(json.loads(line))
    return events

def build_hierarchy(events):
    """Build hierarchical tree from events."""
    tree = defaultdict(list)

    for event in events:
        session = event.get('session_id', 'unknown')
        parent = event.get('parent_session')

        if parent:
            tree[parent].append(event)
        else:
            tree['root'].append(event)

    return tree

def print_tree(tree, node='root', indent=0):
    """Recursively print tree."""
    prefix = "  " * indent

    for event in tree.get(node, []):
        event_type = event.get('event', event.get('event_type', 'unknown'))
        component = event.get('component', 'unknown')
        name = event.get('name', 'unknown')
        timestamp = event.get('timestamp', '')

        # Format based on event type
        if event_type in ['started', 'pre_spawn', 'pre_invoke']:
            symbol = "├─"
        elif event_type in ['stopped', 'post_spawn', 'post_invoke']:
            symbol = "└─"
        else:
            symbol = "│ "

        print(f"{prefix}{symbol} [{timestamp}] {component}:{name} ({event_type})")

        # Recurse for child sessions
        session = event.get('session_id')
        if session:
            print_tree(tree, session, indent + 1)

def main():
    events = load_lifecycle()
    tree = build_hierarchy(events)

    print("=" * 80)
    print("HTEC FRAMEWORK CALL STACK")
    print("=" * 80)
    print_tree(tree)

if __name__ == '__main__':
    main()
