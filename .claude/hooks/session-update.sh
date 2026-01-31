#!/bin/bash
# session-update.sh - Update session context when stage commands run
#
# Purpose: Updates _state/session.json with project and stage context
# Usage: .claude/hooks/session-update.sh --project "EmergencyTriage" --stage "discovery"
#
# This allows lifecycle entries to include meaningful project/stage information

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
SESSION_FILE="${PROJECT_DIR}/_state/session.json"
STATE_DIR="${PROJECT_DIR}/_state"

mkdir -p "$STATE_DIR"

# Parse arguments
PROJECT_NAME=""
STAGE=""
INPUT_PATH=""
OUTPUT_PATH=""
DESCRIPTION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --project) PROJECT_NAME="$2"; shift 2 ;;
        --stage) STAGE="$2"; shift 2 ;;
        --input) INPUT_PATH="$2"; shift 2 ;;
        --output) OUTPUT_PATH="$2"; shift 2 ;;
        --description) DESCRIPTION="$2"; shift 2 ;;
        *) shift ;;
    esac
done

TIMESTAMP=$(date -Iseconds 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S")

# If session file doesn't exist, create it first
if [ ! -f "$SESSION_FILE" ]; then
    SESSION_ID="${CLAUDE_SESSION_ID:-$(date +%s)-$$}"
    if command -v jq &>/dev/null; then
        jq -n \
            --arg sid "$SESSION_ID" \
            --arg ts "$TIMESTAMP" \
            --arg proj "${PROJECT_NAME:-pending}" \
            --arg stage "${STAGE:-unknown}" \
            '{
                session_id: $sid,
                program: "HTEC Framework",
                project: $proj,
                stage: $stage,
                started_at: $ts,
                updated_at: $ts,
                user: "system",
                metadata: {}
            }' > "$SESSION_FILE"
    else
        echo '{"session_id":"'$SESSION_ID'","program":"HTEC Framework","project":"'${PROJECT_NAME:-pending}'","stage":"'${STAGE:-unknown}'"}' > "$SESSION_FILE"
    fi
    echo "SESSION_CREATED: project=${PROJECT_NAME:-pending} stage=${STAGE:-unknown}"
    exit 0
fi

# Update existing session file
if command -v jq &>/dev/null; then
    UPDATED=$(cat "$SESSION_FILE" | jq \
        --arg ts "$TIMESTAMP" \
        --arg proj "${PROJECT_NAME:-}" \
        --arg stage "${STAGE:-}" \
        --arg input "${INPUT_PATH:-}" \
        --arg output "${OUTPUT_PATH:-}" \
        --arg desc "${DESCRIPTION:-}" \
        '
        .updated_at = $ts |
        if ($proj != "" and $proj != "pending" and $proj != "unknown") then
          .project = $proj
        elif .project == "pending" then
          .project = "pending"
        else . end |
        if ($stage != "" and $stage != "unknown") then
          .stage = $stage
        elif .stage == "unknown" then
          .stage = "unknown"
        else . end |
        if $input != "" then .metadata.input_path = $input else . end |
        if $output != "" then .metadata.output_path = $output else . end |
        if $desc != "" then .metadata.description = $desc else . end
        ')
    echo "$UPDATED" > "$SESSION_FILE"

    # Validate the update worked
    NEW_PROJECT=$(cat "$SESSION_FILE" | jq -r '.project')
    NEW_STAGE=$(cat "$SESSION_FILE" | jq -r '.stage')

    if [ "$NEW_PROJECT" = "pending" ] || [ "$NEW_PROJECT" = "unknown" ]; then
        echo "⚠️  WARNING: Project name is still '$NEW_PROJECT' - run /project-init" >&2
    fi
else
    # Without jq, just output a warning
    echo "WARNING: jq not available, session not updated"
fi

echo "SESSION_UPDATED: project=${PROJECT_NAME:-unchanged} stage=${STAGE:-unchanged}"
