#!/bin/bash
# Delete Unused Skills Script
# Generated: 2026-01-30
# Total skills to delete: 28 (6 redundant + 22 pentest)

set -e

SKILLS_DIR=".claude/skills"

echo "=== Deleting Unused Skills ==="
echo ""

# Phase 5.1.1: Delete redundant skills (6)
echo "Deleting 6 redundant skills..."
REDUNDANT_SKILLS=(
  "github_git-commit-helper"
  "github_gh-address-comments"
  "skill-creator"
  "skill-developer"
  "software-architecture"
  "PERSONA_senior-qa"
)

deleted_count=0
for skill in "${REDUNDANT_SKILLS[@]}"; do
  if [ -d "$SKILLS_DIR/$skill" ]; then
    rm -rf "$SKILLS_DIR/$skill"
    echo "  Deleted: $skill"
    ((deleted_count++))
  else
    echo "  Not found: $skill"
  fi
done

# Phase 5.1.2: Delete pentest skills (22)
echo ""
echo "Deleting 22 penetration testing skills..."
PENTEST_SKILLS=(
  "SECURITY_active-directory-attacks"
  "SECURITY_aws-penetration-testing"
  "SECURITY_burp-suite-testing"
  "SECURITY_cloud-penetration-testing"
  "SECURITY_ethical-hacking-methodology"
  "SECURITY_file-path-traversal"
  "SECURITY_html-injection-testing"
  "SECURITY_linux-privilege-escalation"
  "SECURITY_metasploit-framework"
  "SECURITY_pentest-checklist"
  "SECURITY_pentest-commands"
  "SECURITY_privilege-escalation-methods"
  "SECURITY_red-team-tactics"
  "SECURITY_red-team-tools"
  "SECURITY_scanning-tools"
  "SECURITY_senior-secops"
  "SECURITY_senior-security"
  "SECURITY_shodan-reconnaissance"
  "SECURITY_smtp-penetration-testing"
  "SECURITY_sqlmap-database-pentesting"
  "SECURITY_ssh-penetration-testing"
  "SECURITY_wireshark-analysis"
  "SECURITY_windows-privilege-escalation"
  "SECURITY_wordpress-penetration-testing"
)

for skill in "${PENTEST_SKILLS[@]}"; do
  if [ -d "$SKILLS_DIR/$skill" ]; then
    rm -rf "$SKILLS_DIR/$skill"
    echo "  Deleted: $skill"
    ((deleted_count++))
  else
    echo "  Not found: $skill"
  fi
done

echo ""
echo "=== Phase 5.1 Complete: Deleted $deleted_count skills ==="
echo ""
echo "NOTE: Run delete-merged-skills.sh AFTER completing Phase 1 merges"
