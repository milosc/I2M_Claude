#!/usr/bin/env python3
"""
Phase 10 Validation Script - Comprehensive validation of all migrations
Checks:
1. Frontmatter YAML syntax validity
2. FIRST ACTION sections present
3. No legacy logging code remains
4. Hooks correctly formatted
"""

import re
from pathlib import Path
import json

COMMANDS_DIR = Path(".claude/commands")
SKILLS_DIR = Path(".claude/skills")
AGENTS_DIR = Path(".claude/agents")

ISSUES = []
WARNINGS = []

def check_yaml_syntax(content):
    """Check if frontmatter is valid YAML"""
    try:
        if not content.startswith("---"):
            return False, "No frontmatter"

        end_marker = content.find("---", 3)
        if end_marker == -1:
            return False, "No closing ---"

        frontmatter = content[3:end_marker].strip()
        # Basic YAML validation
        for line in frontmatter.split("\n"):
            if line and not line.startswith(" ") and ":" not in line:
                return False, f"Invalid YAML line: {line[:50]}"

        return True, "Valid"
    except Exception as e:
        return False, str(e)

def check_first_action(content):
    """Check if FIRST ACTION section is present"""
    return "## FIRST ACTION (MANDATORY)" in content

def check_legacy_code(content):
    """Check for legacy logging code"""
    legacy_patterns = [
        r"PreExecution:",
        r"PostExecution:",
        r"command_start\.py",
        r"command_end\.py",
        r"skill_invoke\.py",
        r"pipeline_progress\.json",
        r"### Step 0: Log Command Start",
        r"### Step Final: Log Command End",
    ]

    for pattern in legacy_patterns:
        if re.search(pattern, content):
            return False, f"Found legacy code: {pattern}"

    return True, "No legacy code"

def check_hooks(filepath):
    """Check if hooks are properly formatted"""
    with open(filepath, 'r') as f:
        content = f.read()

    if filepath.name.endswith("SKILL.md") or filepath.suffix == ".md" and ".claude/skills" in str(filepath):
        # Skills should have hooks
        if "PreToolUse:" not in content:
            return False, "Missing PreToolUse hook in skill"
        if "Stop:" not in content:
            return False, "Missing Stop hook in skill"
        if "log-lifecycle.sh" not in content:
            return False, "Not using log-lifecycle.sh"
    elif ".claude/commands" in str(filepath):
        # Commands should have hooks
        if "PreToolUse:" not in content:
            return False, "Missing PreToolUse hook in command"
        if "Stop:" not in content:
            return False, "Missing Stop hook in command"
        if "log-lifecycle.sh" not in content:
            return False, "Not using log-lifecycle.sh"
    elif ".claude/agents" in str(filepath) and "README" not in filepath.name:
        # Agents should have FIRST ACTION (not hooks)
        if "## FIRST ACTION" not in content:
            return False, "Missing FIRST ACTION in agent"

    return True, "Hooks OK"

def validate_commands():
    """Validate all command files"""
    print("\n" + "="*60)
    print("VALIDATING COMMANDS")
    print("="*60)

    passed = 0
    failed = 0

    for cmd_file in sorted(COMMANDS_DIR.glob("*.md")):
        with open(cmd_file, 'r') as f:
            content = f.read()

        errors = []

        # Check 1: YAML syntax
        is_valid, msg = check_yaml_syntax(content)
        if not is_valid:
            errors.append(f"Invalid YAML: {msg}")

        # Check 2: FIRST ACTION
        if not check_first_action(content):
            errors.append("Missing FIRST ACTION section")

        # Check 3: No legacy code
        is_clean, msg = check_legacy_code(content)
        if not is_clean:
            errors.append(msg)

        # Check 4: Hooks
        is_valid, msg = check_hooks(cmd_file)
        if not is_valid:
            errors.append(msg)

        if errors:
            print(f"❌ {cmd_file.name}")
            for error in errors:
                print(f"   - {error}")
            failed += 1
            ISSUES.append((cmd_file.name, errors))
        else:
            passed += 1

    print(f"\n✅ Passed: {passed} | ❌ Failed: {failed}")
    return passed, failed

def validate_skills():
    """Validate all skill files"""
    print("\n" + "="*60)
    print("VALIDATING SKILLS")
    print("="*60)

    passed = 0
    failed = 0

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        with open(skill_file, 'r') as f:
            content = f.read()

        errors = []

        # Check 1: YAML syntax
        is_valid, msg = check_yaml_syntax(content)
        if not is_valid:
            errors.append(f"Invalid YAML: {msg}")

        # Check 2: FIRST ACTION
        if not check_first_action(content):
            errors.append("Missing FIRST ACTION section")

        # Check 3: No legacy code
        is_clean, msg = check_legacy_code(content)
        if not is_clean:
            errors.append(msg)

        # Check 4: Hooks
        is_valid, msg = check_hooks(skill_file)
        if not is_valid:
            errors.append(msg)

        if errors:
            print(f"❌ {skill_dir.name}")
            for error in errors:
                print(f"   - {error}")
            failed += 1
            ISSUES.append((skill_dir.name, errors))
        else:
            passed += 1

    print(f"\n✅ Passed: {passed} | ❌ Failed: {failed}")
    return passed, failed

def validate_agents():
    """Validate all agent files"""
    print("\n" + "="*60)
    print("VALIDATING AGENTS")
    print("="*60)

    passed = 0
    failed = 0

    for agent_file in sorted(AGENTS_DIR.glob("*.md")):
        with open(agent_file, 'r') as f:
            content = f.read()

        errors = []

        # Skip README.md
        if agent_file.name == "README.md":
            passed += 1
            continue

        # Check 1: YAML syntax (if has frontmatter)
        if content.startswith("---"):
            is_valid, msg = check_yaml_syntax(content)
            if not is_valid:
                errors.append(f"Invalid YAML: {msg}")

        # Check 2: FIRST ACTION
        if not check_first_action(content):
            errors.append("Missing FIRST ACTION section")

        # Check 3: No legacy code
        is_clean, msg = check_legacy_code(content)
        if not is_clean:
            errors.append(msg)

        # Check 4: Hooks
        is_valid, msg = check_hooks(agent_file)
        if not is_valid:
            errors.append(msg)

        if errors:
            print(f"❌ {agent_file.name}")
            for error in errors:
                print(f"   - {error}")
            failed += 1
            ISSUES.append((agent_file.name, errors))
        else:
            passed += 1

    print(f"\n✅ Passed: {passed} | ❌ Failed: {failed}")
    return passed, failed

def main():
    print("\n" + "="*80)
    print("PHASE 10: COMPREHENSIVE VALIDATION")
    print("="*80)

    cmd_pass, cmd_fail = validate_commands()
    skill_pass, skill_fail = validate_skills()
    agent_pass, agent_fail = validate_agents()

    total_pass = cmd_pass + skill_pass + agent_pass
    total_fail = cmd_fail + skill_fail + agent_fail

    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    print(f"✅ Total Passed: {total_pass}")
    print(f"❌ Total Failed: {total_fail}")
    print(f"📊 Pass Rate: {total_pass / (total_pass + total_fail) * 100:.1f}%")

    if ISSUES:
        print(f"\n⚠️  {len(ISSUES)} files with issues:")
        for filename, errors in ISSUES[:10]:  # Show first 10
            print(f"  - {filename}: {len(errors)} issue(s)")

    return total_fail == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
