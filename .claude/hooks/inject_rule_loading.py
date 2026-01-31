#!/usr/bin/env python3
"""
Inject "Rules Loading (On-Demand)" sections into command files.
"""

import os
import re
import sys
from pathlib import Path

# Rule loading templates by command prefix
RULE_TEMPLATES = {
    'discovery': '''
## Rules Loading (On-Demand)

This command requires Discovery-specific rules. Load them now:

```bash
# Load Discovery rules (includes PDF handling, input processing, output structure)
/rules-discovery

# Load Traceability rules (includes ID formats, source linking)
/rules-traceability
```
''',
    'prototype': '''
## Rules Loading (On-Demand)

This command requires Assembly-First and traceability rules:

```bash
# Assembly-First rules (loaded automatically in Prototype stage)
/_assembly_first_rules

# Traceability rules for ID management
/rules-traceability
```
''',
    'productspecs': '''
## Rules Loading (On-Demand)

This command requires traceability rules for module/test ID management:

```bash
# Load Traceability rules (includes module ID format MOD-XXX-XXX-NN)
/rules-traceability
```
''',
    'solarch': '''
## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```
''',
    'htec-sdd': '''
## Rules Loading (On-Demand)

This command requires Implementation stage rules:

```bash
# Load TDD and quality gate rules
/rules-process-integrity

# Load multi-agent coordination rules (if spawning agents)
/rules-agent-coordination

# Load Traceability rules for task IDs
/rules-traceability
```
'''
}

def get_command_prefix(filename):
    """Extract command prefix (discovery, prototype, etc.)"""
    for prefix in RULE_TEMPLATES.keys():
        if filename.startswith(prefix):
            return prefix
    return None

def has_rule_loading_section(content):
    """Check if file already has Rules Loading section"""
    return '## Rules Loading (On-Demand)' in content

def inject_rule_loading(filepath):
    """Inject rule loading section into command file"""
    with open(filepath, 'r') as f:
        content = f.read()

    # Skip if already has rule loading section
    if has_rule_loading_section(content):
        return False

    # Get command prefix
    filename = os.path.basename(filepath)
    prefix = get_command_prefix(filename)

    if not prefix:
        return False

    # Find insertion point (after FIRST ACTION section)
    # Pattern: Look for the end of the bash code block after "## FIRST ACTION"
    pattern = r'(## FIRST ACTION \(MANDATORY\).*?```\n)(## Arguments|## Usage|## Description)'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        # Alternative pattern: Look for just "## Arguments" or "## Usage" or "## Description" without FIRST ACTION
        pattern = r'(---\n\n)(## Arguments|## Usage|## Description)'
        match = re.search(pattern, content, re.DOTALL)

    if match:
        # Insert rule loading section
        template = RULE_TEMPLATES[prefix]
        new_content = content[:match.end(1)] + template + '\n' + match.group(2) + content[match.end():]

        # Write back
        with open(filepath, 'w') as f:
            f.write(new_content)

        return True

    return False

def main():
    """Main entry point"""
    commands_dir = Path('.claude/commands')

    if not commands_dir.exists():
        print("ERROR: .claude/commands directory not found")
        sys.exit(1)

    updated = 0
    skipped = 0
    errors = 0

    for filepath in sorted(commands_dir.glob('*.md')):
        filename = filepath.name

        # Skip non-command files
        if filename.startswith('_') or filename.startswith('rules-'):
            continue

        try:
            if inject_rule_loading(filepath):
                print(f"✅ Updated: {filename}")
                updated += 1
            else:
                print(f"⏭️  Skipped: {filename} (already has rules or no match)")
                skipped += 1
        except Exception as e:
            print(f"❌ Error: {filename} - {e}")
            errors += 1

    print(f"\n📊 Summary:")
    print(f"   Updated: {updated}")
    print(f"   Skipped: {skipped}")
    print(f"   Errors: {errors}")

    return 0 if errors == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
