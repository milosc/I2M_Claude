#!/usr/bin/env python3
"""Extract user context with fallback chain."""

import getpass
import subprocess
import os
import sys

def get_operator_name():
    """Extract meaningful operator name with fallback chain.

    Priority order:
    1. Git user.name (most meaningful for code contributions)
    2. Git user.email (fallback)
    3. getpass.getuser() (system username)
    4. Environment variables (USER, LOGNAME)
    5. "unknown" (last resort)
    """

    # 1. Try git user.name
    try:
        git_name = subprocess.check_output(
            ['git', 'config', 'user.name'],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        if git_name and git_name not in ['', 'unknown', 'system']:
            return git_name
    except:
        pass

    # 2. Try git user.email
    try:
        git_email = subprocess.check_output(
            ['git', 'config', 'user.email'],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        if git_email and git_email not in ['', 'unknown', 'system']:
            return git_email
    except:
        pass

    # 3. Try getpass.getuser()
    try:
        username = getpass.getuser()
        if username and username not in ['', 'unknown', 'system']:
            return username
    except:
        pass

    # 4. Try environment variables
    username = os.environ.get('USER') or os.environ.get('LOGNAME')
    if username and username not in ['', 'unknown', 'system']:
        return username

    # 5. Last resort
    return 'unknown'

if __name__ == '__main__':
    print(get_operator_name())
