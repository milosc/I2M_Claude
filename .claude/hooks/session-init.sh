#!/bin/bash
# session-init.sh - Initialize session state on Claude Code startup
#
# Purpose: Creates _state/session.json to track program/project context
# Trigger: SessionStart hook in settings.json
#
# This file addresses the "session: unknown" issue in lifecycle.json

set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
SESSION_FILE="${PROJECT_DIR}/_state/session.json"
STATE_DIR="${PROJECT_DIR}/_state"

mkdir -p "$STATE_DIR"

# Generate session ID from CLAUDE_SESSION_ID or create unique one
SESSION_ID="${CLAUDE_SESSION_ID:-$(date +%s)-$$}"
TIMESTAMP=$(date -Iseconds 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S")

# Check if session file exists and is recent (within 1 hour)
if [ -f "$SESSION_FILE" ]; then
    # Read existing session
    EXISTING_SESSION=$(cat "$SESSION_FILE" 2>/dev/null || echo "{}")

    # Update timestamp only
    if command -v jq &>/dev/null; then
        echo "$EXISTING_SESSION" | jq --arg ts "$TIMESTAMP" --arg sid "$SESSION_ID" '.updated_at = $ts | .session_id = $sid' > "$SESSION_FILE"
    fi
else
    # Create new session with defaults (will be populated by first command)
    # Extract real username (not "system")
    USER_NAME=$("${PROJECT_DIR}/.claude/hooks/get_user_context.py" 2>/dev/null || echo "system")

    if command -v jq &>/dev/null; then
        jq -n \
            --arg sid "$SESSION_ID" \
            --arg ts "$TIMESTAMP" \
            --arg user "$USER_NAME" \
            '{
                session_id: $sid,
                program: "HTEC Framework",
                project: "pending",
                stage: "unknown",
                started_at: $ts,
                updated_at: $ts,
                user: $user,
                metadata: {}
            }' > "$SESSION_FILE"
    else
        echo '{"session_id":"'$SESSION_ID'","program":"HTEC Framework","project":"pending","stage":"unknown","started_at":"'$TIMESTAMP'","updated_at":"'$TIMESTAMP'"}' > "$SESSION_FILE"
    fi
fi

echo "SESSION_INIT: $SESSION_ID"

# Auto-load stage-specific rules
if [ -x "${PROJECT_DIR}/.claude/hooks/auto_load_stage_rules.py" ]; then
    STAGE_RULES_OUTPUT=$(python3 "${PROJECT_DIR}/.claude/hooks/auto_load_stage_rules.py" 2>/dev/null || echo "")

    if [ -n "$STAGE_RULES_OUTPUT" ]; then
        STAGE=$(echo "$STAGE_RULES_OUTPUT" | grep "^STAGE:" | cut -d: -f2 | xargs)
        AUTO_LOAD=$(echo "$STAGE_RULES_OUTPUT" | grep "^AUTO_LOAD:" | cut -d: -f2- | xargs)

        if [ "$STAGE" != "unknown" ] && [ "$AUTO_LOAD" != "(none)" ]; then
            echo "STAGE_DETECTED: $STAGE"
            echo "AUTO_LOAD_RULES: $AUTO_LOAD"
        fi
    fi
fi
