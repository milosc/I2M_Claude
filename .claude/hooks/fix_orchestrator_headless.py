#!/usr/bin/env python3
"""
Fix headless parameter in all orchestrator files.

This script adds:
1. Configuration loading instructions (read config.json)
2. HEADLESS constant definition
3. headless: HEADLESS to all Task() calls
"""

import re
import sys
from pathlib import Path

ORCHESTRATOR_FILES = [
    'agents/discovery/discovery-orchestrator.md',
    'agents/productspecs/productspecs-orchestrator.md',
    'agents/solarch/solarch-orchestrator.md',
]

CONFIG_LOADING_SECTION = '''### Phase 0: Load Configuration

**BEFORE spawning ANY agents**, you MUST:

1. Read `_state/{stage}_config.json` to get the `headless_mode` setting
2. **ALWAYS pass `headless: config.headless_mode`** to EVERY Task() call

```javascript
// Read config first
const config = JSON.parse(await Read('_state/{stage}_config.json'));
const HEADLESS = config.headless_mode; // false = visible terminals (default), true = hidden

// Then use in ALL Task() calls:
Task({{
  subagent_type: "{stage}:agent-name",
  model: "sonnet",
  description: "Agent description",
  headless: HEADLESS,  // ← REQUIRED: Pass terminal visibility setting
  prompt: `...`
}})
```

**WHY THIS MATTERS**:
- `headless: false` (default) = Visible terminal windows for debugging
- `headless: true` (--headless flag) = Background execution for CI/CD
- If you don't specify `headless`, it defaults to true (unwanted background mode)

'''

def get_stage_name(file_path: str) -> str:
    """Extract stage name from file path."""
    if 'discovery' in file_path:
        return 'discovery'
    elif 'productspecs' in file_path:
        return 'productspecs'
    elif 'solarch' in file_path:
        return 'solarch'
    return 'unknown'

def fix_orchestrator(file_path: Path) -> bool:
    """
    Fix a single orchestrator file.

    Returns True if changes were made, False otherwise.
    """
    print(f"\nProcessing: {file_path.name}")

    if not file_path.exists():
        print(f"  ⊘ File not found, skipping")
        return False

    content = file_path.read_text()
    original_content = content

    stage = get_stage_name(str(file_path))

    # Check if already has Phase 0 section
    if 'Phase 0: Load Configuration' in content:
        print(f"  ✓ Already has configuration loading section")
        has_config = True
    else:
        has_config = False

    # Check if already has headless in Task calls
    if 'headless: HEADLESS' in content or 'headless: config.headless_mode' in content:
        print(f"  ✓ Already has headless parameter in Task calls")
        has_headless = True
    else:
        has_headless = False

    if has_config and has_headless:
        print(f"  ⊘ Already fully fixed, skipping")
        return False

    # Fix 1: Add configuration loading section
    if not has_config:
        # Find "## Your Approach" section and add Phase 0 after it
        pattern = r'(## Your Approach.*?\n\n)(### Phase 1:)'
        config_section = CONFIG_LOADING_SECTION.replace('{stage}', stage)
        replacement = r'\1' + config_section + r'\2'
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        print(f"  ✓ Added configuration loading section")

    # Fix 2: Add headless parameter to all Task() calls that don't have it
    if not has_headless:
        # Find Task({ calls and add headless parameter
        # Pattern: Task({...subagent_type...model...description...prompt
        # Insert headless after description

        def add_headless(match):
            """Add headless parameter to Task call if not present."""
            task_call = match.group(0)

            # Skip if already has headless
            if 'headless:' in task_call:
                return task_call

            # Find description line and add headless after it
            pattern = r'(description: .*?,)\n(\s+prompt:)'
            if re.search(pattern, task_call):
                modified = re.sub(
                    pattern,
                    r'\1\n\2headless: HEADLESS,  // Pass terminal visibility from config\n\2',
                    task_call
                )
                return modified

            return task_call

        # Match Task({ ... }) blocks
        pattern = r'Task\(\{[^}]+subagent_type[^}]+\}\)'
        content = re.sub(pattern, add_headless, content, flags=re.DOTALL)
        print(f"  ✓ Added headless parameter to Task calls")

    # Check if any changes were made
    if content == original_content:
        print(f"  ⚠ No changes made")
        return False

    # Write back to file
    file_path.write_text(content)
    print(f"  ✓ Fixed successfully")
    return True


def main():
    """Main entry point."""
    base_path = Path(__file__).parent.parent

    print("Fixing orchestrator headless parameters...")
    print("=" * 60)

    fixed_count = 0
    for rel_path in ORCHESTRATOR_FILES:
        file_path = base_path / rel_path
        if fix_orchestrator(file_path):
            fixed_count += 1

    print("\n" + "=" * 60)
    print(f"Summary: Fixed {fixed_count} of {len(ORCHESTRATOR_FILES)} files")
    print("=" * 60)


if __name__ == '__main__':
    main()
