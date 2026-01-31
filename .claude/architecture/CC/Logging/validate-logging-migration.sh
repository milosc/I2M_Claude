#!/bin/bash
# validate-logging-migration.sh

echo "=== LOGGING MIGRATION VALIDATION ==="
echo ""

# Count totals
TOTAL_COMMANDS=$(ls .claude/commands/*.md 2>/dev/null | wc -l)
TOTAL_SKILLS=$(ls -d .claude/skills/*/ 2>/dev/null | wc -l)
TOTAL_AGENTS=$(ls .claude/agents/*.md 2>/dev/null | wc -l)

# Count migrated (have PreToolUse or FIRST ACTION)
MIGRATED_COMMANDS=$(grep -l "PreToolUse:" .claude/commands/*.md 2>/dev/null | wc -l)
MIGRATED_SKILLS=$(grep -l "PreToolUse:" .claude/skills/*/SKILL.md 2>/dev/null | wc -l)
MIGRATED_AGENTS=$(grep -l "FIRST ACTION" .claude/agents/*.md 2>/dev/null | wc -l)

echo "Commands:  $MIGRATED_COMMANDS / $TOTAL_COMMANDS migrated"
echo "Skills:    $MIGRATED_SKILLS / $TOTAL_SKILLS migrated"
echo "Agents:    $MIGRATED_AGENTS / $TOTAL_AGENTS migrated"
echo ""

# List un-migrated components (sample)
echo "=== UN-MIGRATED COMMANDS (Sample) ==="
grep -L "PreToolUse:" .claude/commands/*.md 2>/dev/null | head -5
echo ""

echo "=== UN-MIGRATED SKILLS (Sample) ==="
for skill_dir in .claude/skills/*/; do
  skill_file="$skill_dir/SKILL.md"
  if [ -f "$skill_file" ]; then
    if ! grep -q "PreToolUse:" "$skill_file"; then
      echo "$skill_file"
    fi
  fi
done | head -5
echo ""

echo "=== UN-MIGRATED AGENTS (Sample) ==="
grep -L "FIRST ACTION" .claude/agents/*.md 2>/dev/null | head -5
