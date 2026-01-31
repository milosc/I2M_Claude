#!/bin/bash
# log-lifecycle.sh - Enhanced lifecycle logging for Claude Code components
#
# CHANGES FROM ORIGINAL (v2.0):
# 1. Reads session_id, project, stage from _state/session.json (fallback to CLAUDE_SESSION_ID)
# 2. Adds project and stage fields to all log entries
# 3. Supports --from-input parameter to extract name from CLAUDE_TOOL_INPUT
#
# Usage: log-lifecycle.sh <component_type> <component_name> <event> [extra_json] [description]
#
# Arguments:
#   component_type  - Type of component: command, skill, agent, subagent, session
#   component_name  - Name of the component OR "--from-input" to extract from CLAUDE_TOOL_INPUT
#   event           - Event type: instruction_start, instruction_end, pre_invoke, post_invoke, started, stopped
#   extra_json      - Optional JSON object with additional metadata (stage, method, outputs, etc.)
#   description     - Optional one-line description of what this component does
#
# Special --from-input mode:
#   When component_name is "--from-input", the script will attempt to extract the
#   actual name from the CLAUDE_TOOL_INPUT environment variable:
#   - For agents/subagents: Extracts from "Agent:" in prompt or .subagent_type
#   - For skills: Extracts from .skill field
#
# Examples:
#   log-lifecycle.sh command /solarch instruction_start '{"stage": "solarch"}'
#   log-lifecycle.sh agent --from-input pre_spawn  # Extracts agent name from CLAUDE_TOOL_INPUT
#   log-lifecycle.sh skill --from-input pre_invoke # Extracts skill name from CLAUDE_TOOL_INPUT
#
# Output JSON Schema:
# {
#   "component": "command|skill|agent|subagent|session",
#   "name": "/command-name or skill-name",
#   "event": "instruction_start|instruction_end|pre_invoke|post_invoke|started|stopped",
#   "timestamp": "ISO8601",
#   "session": "session-id or unknown",
#   "project": "project name or unknown",
#   "stage": "discovery|prototype|productspecs|solarch|implementation|utility|unknown",
#   "description": "One-line description of component purpose",
#   "extra": { ...additional metadata... }
# }

set -euo pipefail

COMPONENT_TYPE="${1:-unknown}"
COMPONENT_NAME="${2:-unknown}"
EVENT="${3:-unknown}"
EXTRA_JSON="${4:-}"
DESCRIPTION="${5:-}"

# Determine project directory
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
LOG_FILE="${PROJECT_DIR}/_state/lifecycle.json"
SESSION_FILE="${PROJECT_DIR}/_state/session.json"
STATE_DIR="${PROJECT_DIR}/_state"

# Ensure state directory exists
mkdir -p "$STATE_DIR"

# Generate timestamp
TIMESTAMP=$(date -Iseconds 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S")

# Read session info from session.json (NEW)
SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"
PROJECT_NAME="unknown"
STAGE="unknown"

if [ -f "$SESSION_FILE" ] && command -v jq &>/dev/null; then
    SESSION_DATA=$(cat "$SESSION_FILE" 2>/dev/null || echo "{}")
    # Read session_id from file, but prefer CLAUDE_SESSION_ID if available
    FILE_SESSION_ID=$(echo "$SESSION_DATA" | jq -r '.session_id // "unknown"')
    if [ "$SESSION_ID" = "unknown" ]; then
        SESSION_ID="$FILE_SESSION_ID"
    fi
    PROJECT_NAME=$(echo "$SESSION_DATA" | jq -r '.project // "unknown"')
    STAGE=$(echo "$SESSION_DATA" | jq -r '.stage // "unknown"')
fi

# Handle special case for extracting name from tool input (NEW)
if [ "$COMPONENT_NAME" = "--from-input" ]; then
    # Extract name from CLAUDE_TOOL_INPUT environment variable
    if [ -n "${CLAUDE_TOOL_INPUT:-}" ] && command -v jq &>/dev/null; then
        case "$COMPONENT_TYPE" in
            agent|subagent)
                # Extract from Task tool input: look for "Agent:" in prompt or subagent_type
                # First try to find "Agent: agent-name" pattern in prompt
                EXTRACTED=$(echo "$CLAUDE_TOOL_INPUT" | jq -r '
                    if .prompt then
                        # Try to extract "Agent: name" pattern (case insensitive)
                        ((.prompt | capture("Agent:\\s*(?<name>[a-zA-Z0-9_-]+)"; "i").name) // null) //
                        # Try to extract from Read: .claude/agents/name.md pattern
                        ((.prompt | capture("Read:\\s*\\.claude/agents/(?<name>[a-zA-Z0-9_-]+)\\.md"; "i").name) // null) //
                        # Fall back to subagent_type
                        .subagent_type //
                        "unknown"
                    else
                        .subagent_type // "unknown"
                    end
                ' 2>/dev/null || echo "unknown")
                COMPONENT_NAME="${EXTRACTED:-unknown}"
                ;;
            skill)
                # Extract skill name from Skill tool input
                EXTRACTED=$(echo "$CLAUDE_TOOL_INPUT" | jq -r '.skill // "unknown"' 2>/dev/null || echo "unknown")
                COMPONENT_NAME="${EXTRACTED:-unknown}"
                ;;
            *)
                COMPONENT_NAME="unknown"
                ;;
        esac
    else
        COMPONENT_NAME="unknown"
    fi
fi

# Build JSON entry with session context
if command -v jq &>/dev/null; then
    # Use jq for proper JSON construction and escaping (-c for compact output)
    if [ -n "$EXTRA_JSON" ] && [ -n "$DESCRIPTION" ]; then
        JSON_ENTRY=$(jq -c -n \
            --arg comp "$COMPONENT_TYPE" \
            --arg name "$COMPONENT_NAME" \
            --arg event "$EVENT" \
            --arg ts "$TIMESTAMP" \
            --arg sess "$SESSION_ID" \
            --arg proj "$PROJECT_NAME" \
            --arg stage "$STAGE" \
            --arg desc "$DESCRIPTION" \
            --argjson extra "$EXTRA_JSON" \
            '{component: $comp, name: $name, event: $event, timestamp: $ts, session: $sess, project: $proj, stage: $stage, description: $desc, extra: $extra}')
    elif [ -n "$EXTRA_JSON" ]; then
        JSON_ENTRY=$(jq -c -n \
            --arg comp "$COMPONENT_TYPE" \
            --arg name "$COMPONENT_NAME" \
            --arg event "$EVENT" \
            --arg ts "$TIMESTAMP" \
            --arg sess "$SESSION_ID" \
            --arg proj "$PROJECT_NAME" \
            --arg stage "$STAGE" \
            --argjson extra "$EXTRA_JSON" \
            '{component: $comp, name: $name, event: $event, timestamp: $ts, session: $sess, project: $proj, stage: $stage, extra: $extra}')
    elif [ -n "$DESCRIPTION" ]; then
        JSON_ENTRY=$(jq -c -n \
            --arg comp "$COMPONENT_TYPE" \
            --arg name "$COMPONENT_NAME" \
            --arg event "$EVENT" \
            --arg ts "$TIMESTAMP" \
            --arg sess "$SESSION_ID" \
            --arg proj "$PROJECT_NAME" \
            --arg stage "$STAGE" \
            --arg desc "$DESCRIPTION" \
            '{component: $comp, name: $name, event: $event, timestamp: $ts, session: $sess, project: $proj, stage: $stage, description: $desc}')
    else
        JSON_ENTRY=$(jq -c -n \
            --arg comp "$COMPONENT_TYPE" \
            --arg name "$COMPONENT_NAME" \
            --arg event "$EVENT" \
            --arg ts "$TIMESTAMP" \
            --arg sess "$SESSION_ID" \
            --arg proj "$PROJECT_NAME" \
            --arg stage "$STAGE" \
            '{component: $comp, name: $name, event: $event, timestamp: $ts, session: $sess, project: $proj, stage: $stage}')
    fi
else
    # Fallback: manual JSON construction (no special character escaping)
    if [ -n "$EXTRA_JSON" ] && [ -n "$DESCRIPTION" ]; then
        JSON_ENTRY="{\"component\": \"$COMPONENT_TYPE\", \"name\": \"$COMPONENT_NAME\", \"event\": \"$EVENT\", \"timestamp\": \"$TIMESTAMP\", \"session\": \"$SESSION_ID\", \"project\": \"$PROJECT_NAME\", \"stage\": \"$STAGE\", \"description\": \"$DESCRIPTION\", \"extra\": $EXTRA_JSON}"
    elif [ -n "$EXTRA_JSON" ]; then
        JSON_ENTRY="{\"component\": \"$COMPONENT_TYPE\", \"name\": \"$COMPONENT_NAME\", \"event\": \"$EVENT\", \"timestamp\": \"$TIMESTAMP\", \"session\": \"$SESSION_ID\", \"project\": \"$PROJECT_NAME\", \"stage\": \"$STAGE\", \"extra\": $EXTRA_JSON}"
    elif [ -n "$DESCRIPTION" ]; then
        JSON_ENTRY="{\"component\": \"$COMPONENT_TYPE\", \"name\": \"$COMPONENT_NAME\", \"event\": \"$EVENT\", \"timestamp\": \"$TIMESTAMP\", \"session\": \"$SESSION_ID\", \"project\": \"$PROJECT_NAME\", \"stage\": \"$STAGE\", \"description\": \"$DESCRIPTION\"}"
    else
        JSON_ENTRY="{\"component\": \"$COMPONENT_TYPE\", \"name\": \"$COMPONENT_NAME\", \"event\": \"$EVENT\", \"timestamp\": \"$TIMESTAMP\", \"session\": \"$SESSION_ID\", \"project\": \"$PROJECT_NAME\", \"stage\": \"$STAGE\"}"
    fi
fi

# Append to log file
echo "$JSON_ENTRY" >> "$LOG_FILE"

# Output for confirmation (optional, useful for debugging)
echo "LIFECYCLE_LOG: $COMPONENT_TYPE:$COMPONENT_NAME:$EVENT (project=$PROJECT_NAME, stage=$STAGE)"
