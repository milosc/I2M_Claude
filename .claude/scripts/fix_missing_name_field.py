#!/usr/bin/env python3
"""
Fix Missing `name:` Field in HTEC Commands

This script adds the required `name:` field to all command files that are missing it.
The `name:` field is REQUIRED by Claude Code for proper skill/command discovery.

Usage:
    python3 .claude/scripts/fix_missing_name_field.py [--dry-run]

Options:
    --dry-run    Show what would be changed without making changes
"""

import os
import sys
import re
from pathlib import Path

def get_name_from_filename(filepath: str) -> str:
    """Extract command name from filename (without .md extension)."""
    return Path(filepath).stem

def has_frontmatter(content: str) -> bool:
    """Check if file has YAML frontmatter."""
    return content.startswith('---')

def has_name_field(content: str) -> bool:
    """Check if frontmatter contains name: field."""
    # Find frontmatter section
    if not content.startswith('---'):
        return False

    # Find closing ---
    second_delimiter = content.find('---', 3)
    if second_delimiter == -1:
        return False

    frontmatter = content[3:second_delimiter]

    # Check for name: at start of line
    return bool(re.search(r'^name:', frontmatter, re.MULTILINE))

def add_name_field(content: str, name: str) -> str:
    """Add name: field as second line of frontmatter (after opening ---)."""
    if not content.startswith('---'):
        return content

    # Insert name: right after the opening ---
    lines = content.split('\n')
    if lines[0] == '---':
        lines.insert(1, f'name: {name}')

    return '\n'.join(lines)

def fix_commands(commands_dir: str, dry_run: bool = False) -> dict:
    """Fix all commands missing the name: field."""
    results = {
        'fixed': [],
        'skipped_has_name': [],
        'skipped_no_frontmatter': [],
        'errors': []
    }

    commands_path = Path(commands_dir)
    if not commands_path.exists():
        print(f"❌ Directory not found: {commands_dir}")
        return results

    md_files = sorted(commands_path.glob('*.md'))

    for filepath in md_files:
        try:
            content = filepath.read_text(encoding='utf-8')
            name = get_name_from_filename(str(filepath))

            if not has_frontmatter(content):
                results['skipped_no_frontmatter'].append(name)
                continue

            if has_name_field(content):
                results['skipped_has_name'].append(name)
                continue

            # Fix the file
            new_content = add_name_field(content, name)

            if dry_run:
                print(f"🔧 Would fix: {name}")
            else:
                filepath.write_text(new_content, encoding='utf-8')
                print(f"✅ Fixed: {name}")

            results['fixed'].append(name)

        except Exception as e:
            results['errors'].append((str(filepath), str(e)))
            print(f"❌ Error processing {filepath}: {e}")

    return results

def main():
    dry_run = '--dry-run' in sys.argv

    # Determine commands directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    commands_dir = project_root / '.claude' / 'commands'

    print("=" * 60)
    print("HTEC Command Frontmatter Fixer")
    print("=" * 60)
    print(f"Commands directory: {commands_dir}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("=" * 60)
    print()

    results = fix_commands(str(commands_dir), dry_run)

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Fixed (added name:):     {len(results['fixed'])}")
    print(f"⏭️  Skipped (already has):   {len(results['skipped_has_name'])}")
    print(f"⚠️  Skipped (no frontmatter): {len(results['skipped_no_frontmatter'])}")
    print(f"❌ Errors:                  {len(results['errors'])}")
    print()

    if results['skipped_no_frontmatter']:
        print("Files without frontmatter (may need manual review):")
        for name in results['skipped_no_frontmatter']:
            print(f"  - {name}")
        print()

    if results['errors']:
        print("Errors encountered:")
        for filepath, error in results['errors']:
            print(f"  - {filepath}: {error}")
        print()

    if dry_run and results['fixed']:
        print("Run without --dry-run to apply changes.")

    return 0 if not results['errors'] else 1

if __name__ == '__main__':
    sys.exit(main())
