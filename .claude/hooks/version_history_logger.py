import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def get_operator_name():
    """Get operator name from get_user_context.py."""
    try:
        script_dir = Path(__file__).parent
        result = subprocess.check_output(
            [sys.executable, str(script_dir / 'get_user_context.py')],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        return result if result else 'Claude'
    except:
        return 'Claude'

def log_change(traceability_dir, system_name, stage, author, version, reason, references, file_path, action):
    """Log a version change to traceability history.

    Args:
        author: Author name (pass explicit name or empty string to auto-detect)
    """
    # If author is hardcoded "Claude" or empty, replace with real user
    if not author or author.lower() in ['claude', 'system', 'unknown', '']:
        author = get_operator_name()

    history_file = os.path.join(traceability_dir, f"{system_name}_version_history.json")

    entry = {
        "timestamp": datetime.now().isoformat(),
        "stage": stage,
        "author": author,
        "version": version,
        "action": action, # creation, modification, deletion
        "file": file_path,
        "reason": reason,
        "references": references,
    }

    history = {"system_name": system_name, "history": []}
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                pass

    history["history"].append(entry)
    
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    print(f"✅ Logged {action} to {history_file}")

if __name__ == "__main__":
    # Args: traceability_dir, system_name, stage, author, version, reason, references, file_path, action
    if len(sys.argv) < 10:
        print("Usage: python3 version_history_logger.py <dir> <sys> <stage> <auth> <ver> <reason> <refs> <path> <action>")
        sys.exit(1)
        
    log_change(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7].split(','), sys.argv[8], sys.argv[9])
