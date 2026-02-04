#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///

"""
Security Gate - HTEC PreToolUse Hook

Blocks dangerous bash commands before execution.
Used as a PreToolUse hook to prevent destructive operations.

Exit Codes:
- 0: Command allowed (outputs JSON with "decision": "allow")
- 2: Command blocked (outputs JSON with "decision": "block")

Blocked Patterns:
- rm -rf / or rm -rf /*
- sudo rm (any)
- .env file access (except .env.sample, .env.example)
- chmod 777
- > /dev/sda (device writes)
- mkfs (format commands)
- dd if=/dev/zero
- :(){ :|:& };: (fork bomb)

Usage (as PreToolUse hook):
    Input via stdin: {"tool_name": "Bash", "tool_input": {"command": "rm -rf /"}}

    Output (blocked):
    {
        "decision": "block",
        "reason": "Dangerous command: rm -rf with root path"
    }

    Output (allowed):
    {
        "decision": "allow"
    }
"""

import json
import re
import sys
from typing import Tuple


# Dangerous command patterns with explanations
BLOCKED_PATTERNS = [
    # rm -rf with dangerous paths
    (r'rm\s+(-[a-zA-Z]*r[a-zA-Z]*f|--recursive\s+--force|-[a-zA-Z]*f[a-zA-Z]*r)\s+(/|\*|~|/\*)',
     "rm -rf with root/home/wildcard path"),
    (r'rm\s+-rf\s+\$',
     "rm -rf with variable expansion (could be dangerous)"),

    # sudo rm
    (r'sudo\s+rm\s',
     "sudo rm (elevated deletion)"),

    # .env file access (block reading secrets)
    (r'cat\s+[^\s]*\.env($|\s)',
     "Reading .env file (contains secrets)"),
    (r'less\s+[^\s]*\.env($|\s)',
     "Reading .env file (contains secrets)"),
    (r'more\s+[^\s]*\.env($|\s)',
     "Reading .env file (contains secrets)"),
    (r'head\s+[^\s]*\.env($|\s)',
     "Reading .env file (contains secrets)"),
    (r'tail\s+[^\s]*\.env($|\s)',
     "Reading .env file (contains secrets)"),
    (r'nano\s+[^\s]*\.env($|\s)',
     "Editing .env file (contains secrets)"),
    (r'vim?\s+[^\s]*\.env($|\s)',
     "Editing .env file (contains secrets)"),
    (r'echo\s+.*>\s*[^\s]*\.env($|\s)',
     "Writing to .env file"),

    # chmod 777 (world writable)
    (r'chmod\s+777\s',
     "chmod 777 (world writable permissions)"),
    (r'chmod\s+-R\s+777\s',
     "chmod -R 777 (recursive world writable)"),

    # Device writes
    (r'>\s*/dev/sd[a-z]',
     "Direct write to block device"),
    (r'dd\s+.*of=/dev/sd[a-z]',
     "dd write to block device"),

    # Filesystem destruction
    (r'mkfs\s',
     "Format filesystem command"),
    (r'dd\s+.*if=/dev/(zero|random|urandom)',
     "dd with destructive source"),

    # Fork bomb
    (r':\(\)\s*\{\s*:\|:&\s*\}\s*;:',
     "Fork bomb pattern"),

    # Network exfiltration
    (r'curl\s+.*-d\s+.*@.*\.env',
     "Uploading .env file"),
    (r'wget\s+.*--post-file.*\.env',
     "Uploading .env file"),

    # History manipulation (covering tracks)
    (r'history\s+-c',
     "Clearing command history"),
    (r'>\s*~/.bash_history',
     "Wiping bash history"),
    (r'shred\s+.*\.bash_history',
     "Shredding bash history"),

    # Git force push to main/master (dangerous in shared repos)
    (r'git\s+push\s+.*--force.*\s+(origin\s+)?(main|master)',
     "Force push to main/master branch"),
    (r'git\s+push\s+.*-f\s+.*(main|master)',
     "Force push to main/master branch"),
    (r'git\s+push\s+-f\s+origin\s+(main|master)',
     "Force push to main/master branch"),
]

# Allowed exceptions (checked before blocked patterns)
ALLOWED_EXCEPTIONS = [
    r'\.env\.sample',
    r'\.env\.example',
    r'\.env\.template',
    r'\.env\.local\.example',
    r'cp\s+\.env\.example\s+\.env',  # Copying example to real .env is OK
    r'test\s+-f\s+.*\.env',  # Checking if .env exists is OK
    r'\[\s+-f\s+.*\.env',  # Bracket test for .env existence is OK
]


def is_allowed_exception(command: str) -> bool:
    """Check if command matches an allowed exception pattern."""
    for pattern in ALLOWED_EXCEPTIONS:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False


def check_command(command: str) -> Tuple[bool, str]:
    """
    Check if a command is safe to execute.

    Returns:
        Tuple of (is_allowed, reason)
    """
    # First check allowed exceptions
    if is_allowed_exception(command):
        return True, "Matches allowed exception"

    # Then check blocked patterns
    for pattern, reason in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return False, reason

    return True, ""


def process_hook_input(input_data: dict) -> dict:
    """
    Process PreToolUse hook input and return decision.

    Args:
        input_data: Hook input with tool_name and tool_input

    Returns:
        dict with 'decision' (allow/block) and optional 'reason'
    """
    tool_name = input_data.get('tool_name', '')

    # Only check Bash commands
    if tool_name != 'Bash':
        return {"decision": "allow"}

    tool_input = input_data.get('tool_input', {})
    command = tool_input.get('command', '')

    if not command:
        return {"decision": "allow"}

    is_allowed, reason = check_command(command)

    if is_allowed:
        return {"decision": "allow"}
    else:
        return {
            "decision": "block",
            "reason": f"Security gate: {reason}",
            "details": {
                "blocked_command": command[:200],  # Truncate for safety
                "pattern_matched": reason
            }
        }


def main():
    """
    Main entry point. Reads JSON from stdin, outputs decision.
    """
    # Read all stdin first
    raw_input = sys.stdin.read().strip()

    if not raw_input:
        result = {"decision": "allow", "note": "No input provided"}
        print(json.dumps(result, indent=2))
        sys.exit(0)

    try:
        input_data = json.loads(raw_input)
    except json.JSONDecodeError:
        # Treat as raw command for testing
        is_allowed, reason = check_command(raw_input)
        if is_allowed:
            result = {"decision": "allow"}
            print(json.dumps(result, indent=2))
            sys.exit(0)
        else:
            result = {
                "decision": "block",
                "reason": f"Security gate: {reason}",
                "details": {"blocked_command": raw_input[:200]}
            }
            print(json.dumps(result, indent=2))
            sys.exit(2)

    result = process_hook_input(input_data)

    # Output JSON
    print(json.dumps(result, indent=2))

    # Exit code based on decision
    if result["decision"] == "allow":
        sys.exit(0)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
