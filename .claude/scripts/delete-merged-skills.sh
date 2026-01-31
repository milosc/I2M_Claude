#!/bin/bash
# Delete Merged Skills Script (Run AFTER Phase 1 merge)
# Generated: 2026-01-30
# Total skills to delete: 14 (5 PERSONA + 4 redundant merges + 5 ML/Data PERSONA)

set -e

SKILLS_DIR=".claude/skills"

echo "=== Deleting Merged Skills ==="
echo "WARNING: Only run this AFTER Phase 1 merge is complete!"
echo ""

read -p "Have you completed all Phase 1 merges? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Aborted. Complete Phase 1 merges first."
  exit 1
fi

# Phase 5.2: Delete merged skills (14)
MERGED_SKILLS=(
  "PERSONA_senior-architect"
  "PERSONA_senior-backend"
  "PERSONA_senior-frontend"
  "PERSONA_senior-fullstack"
  "PERSONA_senior-devops"
  "PERSONA_senior-computer-vision"
  "PERSONA_senior-data-engineer"
  "PERSONA_senior-data-scientist"
  "PERSONA_senior-ml-engineer"
  "PERSONA_security-compliance"
  "database-design"
  "production-code-audit"
  "mermaid-diagram-specialist"
  "github_gh-fix-ci"
)

deleted_count=0
for skill in "${MERGED_SKILLS[@]}"; do
  if [ -d "$SKILLS_DIR/$skill" ]; then
    rm -rf "$SKILLS_DIR/$skill"
    echo "  Deleted: $skill"
    ((deleted_count++))
  else
    echo "  Not found: $skill"
  fi
done

echo ""
echo "=== Phase 5.2 Complete: Deleted $deleted_count merged skills ==="
