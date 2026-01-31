#!/usr/bin/env python3
"""
Batch fix agent write permissions across all stages.

This script automatically updates agent definition files to:
1. Add Tools line with Write tool access
2. Add CRITICAL warning about Write tool access
3. Change "GENERATE" to "WRITE using Write tool"
4. Change "RETURN to orchestrator" to "REPORT completion"
5. Update version from 1.0.0 to 2.0.0
"""

import re
import sys
from pathlib import Path

def fix_agent_file(file_path: Path) -> bool:
    """
    Fix a single agent definition file.

    Returns True if changes were made, False otherwise.
    """
    print(f"Processing: {file_path.name}")

    content = file_path.read_text()
    original_content = content

    # Check if already v2.0.0 (already fixed)
    if '**Version**: 2.0.0' in content:
        print(f"  ✓ Already v2.0.0, skipping")
        return False

    # Check if this is an agent file (has version)
    if '**Version**: 1.0.0' not in content:
        print(f"  ⊘ Not a v1.0.0 agent file, skipping")
        return False

    # Fix 1: Add Tools line after Model line
    pattern1 = r'(\*\*Model\*\*: sonnet)\n(\*\*Coordination\*\*:)'
    replacement1 = r'\1\n**Tools**: Read, Write, Edit, Grep, Glob, Bash\n\2'
    content = re.sub(pattern1, replacement1, content)

    # Fix 2: Update version and add CRITICAL warning
    pattern2 = r'\*\*Version\*\*: 1\.0\.0\n\n---'
    replacement2 = '''**Version**: 2.0.0

**CRITICAL**: You have **Write tool access** - write files directly, do NOT return code to orchestrator!

---'''
    content = re.sub(pattern2, replacement2, content)

    # Fix 3: Change "GENERATE outputs:" to "WRITE outputs using Write tool:"
    # This matches various numbered steps (5, 6, 7, 8, etc.)
    content = re.sub(
        r'│  (\d+)\. GENERATE outputs:',
        r'│  \1. WRITE outputs using Write tool:',
        content
    )

    # Fix 4: Change "GENERATE" lines to "Write" in execution flow
    content = re.sub(
        r'│\s+├── ([A-Z][A-Za-z_\-\.]+\.(?:md|json|ts))',
        r'│         ├── Write \1',
        content
    )
    content = re.sub(
        r'│\s+└── ([A-Z][A-Za-z_\-\.]+\.(?:md|json|ts))',
        r'│         └── Write \1',
        content
    )

    # Fix 5: Change "UPDATE" to "WRITE/update"
    content = re.sub(
        r'│  (\d+)\. UPDATE (.+_registry\.json)',
        r'│  \1. WRITE/update \2',
        content
    )

    # Fix 6: Change "RETURN summary to orchestrator" to "REPORT completion"
    content = re.sub(
        r'│  (\d+)\. RETURN summary to orchestrator\s+│',
        r'│  \1. REPORT completion (output summary only, NOT code)                      │',
        content
    )

    # Check if any changes were made
    if content == original_content:
        print(f"  ⚠ No pattern matches found, skipping")
        return False

    # Write back to file
    file_path.write_text(content)
    print(f"  ✓ Fixed successfully")
    return True


def main():
    """
    Main entry point - process all agent files.
    """
    base_path = Path(__file__).parent.parent / 'agents'

    if not base_path.exists():
        print(f"Error: Agent directory not found: {base_path}")
        sys.exit(1)

    # Find all agent .md files (excluding README and registries)
    agent_files = []
    for stage_dir in base_path.iterdir():
        if stage_dir.is_dir():
            for file in stage_dir.glob('*.md'):
                if file.stem not in ['README', 'AGENT_REGISTRY'] and not file.stem.endswith('-orchestrator'):
                    agent_files.append(file)

    print(f"Found {len(agent_files)} agent files to check\n")

    fixed_count = 0
    skipped_count = 0

    for file_path in sorted(agent_files):
        if fix_agent_file(file_path):
            fixed_count += 1
        else:
            skipped_count += 1
        print()

    print(f"{'='*60}")
    print(f"Summary:")
    print(f"  Fixed: {fixed_count} files")
    print(f"  Skipped: {skipped_count} files")
    print(f"  Total: {len(agent_files)} files")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
