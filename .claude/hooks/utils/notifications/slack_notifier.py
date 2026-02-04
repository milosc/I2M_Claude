#!/usr/bin/env python3
"""
Slack Notification Utility for Claude Code Hooks

Provides functions to send Slack notifications from Claude Code hooks.
All functions are designed to FAIL SILENTLY to avoid disrupting
the main framework workflow.

Environment Variables:
    SLACK_BOT_TOKEN: Required. Bot token starting with xoxb-
    SLACK_CHANNEL: Optional. Default channel (default: #claude-notifications)
    ENGINEER_NAME: Optional. Name for personalized messages

Usage:
    # Simple notification
    from utils.notifications import notify_slack
    notify_slack("Task completed!")

    # Rich notification with status
    from utils.notifications import notify_slack_rich
    notify_slack_rich("Build Complete", "All tests passed!", "success")

    # CLI usage
    python slack_notifier.py "Your message here"
    python slack_notifier.py --rich "Title" "Message" success
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional
from datetime import datetime


def notify_slack(
    message: str,
    channel: Optional[str] = None,
    emoji: str = ":robot_face:",
    username: str = "Claude Code"
) -> bool:
    """
    Send a notification to Slack.

    This function is designed to FAIL SILENTLY. Any errors are caught
    and logged, but the function always returns gracefully.

    Args:
        message: The notification text
        channel: Channel to post to (default: SLACK_CHANNEL env or #claude-notifications)
        emoji: Bot emoji icon
        username: Display name for the bot

    Returns:
        True if successful, False otherwise (never raises exceptions)
    """
    try:
        token = os.getenv('SLACK_BOT_TOKEN')
        if not token:
            # No token configured - silent return, not an error
            return False

        channel = channel or os.getenv('SLACK_CHANNEL', '#claude-notifications')

        payload = {
            "channel": channel,
            "text": message,
            "icon_emoji": emoji,
            "username": username
        }

        req = urllib.request.Request(
            "https://slack.com/api/chat.postMessage",
            data=json.dumps(payload).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8"
            }
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('ok', False)

    except Exception:
        # SILENT FAILURE - never disrupt the framework
        return False


def notify_slack_rich(
    title: str,
    message: str,
    status: str = "info",
    channel: Optional[str] = None
) -> bool:
    """
    Send a rich formatted Slack message with color coding.

    This function is designed to FAIL SILENTLY. Any errors are caught
    and logged, but the function always returns gracefully.

    Args:
        title: Header text
        message: Body text (supports Slack mrkdwn)
        status: One of "info", "success", "warning", "error"
        channel: Target channel

    Returns:
        True if successful, False otherwise (never raises exceptions)
    """
    try:
        token = os.getenv('SLACK_BOT_TOKEN')
        if not token:
            return False

        channel = channel or os.getenv('SLACK_CHANNEL', '#claude-notifications')
        engineer = os.getenv('ENGINEER_NAME', 'Developer')

        colors = {
            "info": "#36a64f",
            "success": "#00ff00",
            "warning": "#ffcc00",
            "error": "#ff0000"
        }

        emojis = {
            "info": ":information_source:",
            "success": ":white_check_mark:",
            "warning": ":warning:",
            "error": ":x:"
        }

        payload = {
            "channel": channel,
            "attachments": [{
                "color": colors.get(status, colors["info"]),
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{emojis.get(status, '')} {title}",
                            "emoji": True
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": message
                        }
                    },
                    {
                        "type": "context",
                        "elements": [{
                            "type": "mrkdwn",
                            "text": f":robot_face: Claude Code | {engineer}"
                        }]
                    }
                ]
            }]
        }

        req = urllib.request.Request(
            "https://slack.com/api/chat.postMessage",
            data=json.dumps(payload).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8"
            }
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('ok', False)

    except Exception:
        # SILENT FAILURE - never disrupt the framework
        return False


def notify_command_complete(
    command_name: str,
    status: str = "completed",
    details: Optional[str] = None,
    channel: Optional[str] = None
) -> bool:
    """
    Send a command completion notification.

    Args:
        command_name: Name of the command (e.g., "/discovery")
        status: "completed", "failed", or "cancelled"
        details: Optional additional details
        channel: Target channel

    Returns:
        True if successful, False otherwise
    """
    status_map = {
        "completed": ("success", "completed successfully"),
        "failed": ("error", "failed"),
        "cancelled": ("warning", "was cancelled")
    }

    emoji_status, status_text = status_map.get(status, ("info", status))

    title = f"Command {command_name} {status_text}"
    message = details or f"The command `{command_name}` has {status_text}."

    return notify_slack_rich(title, message, emoji_status, channel)


def notify_agent_complete(
    agent_type: str,
    task_summary: Optional[str] = None,
    status: str = "completed",
    channel: Optional[str] = None
) -> bool:
    """
    Send an agent/subagent completion notification.

    Args:
        agent_type: Type of agent (e.g., "discovery-domain-researcher")
        task_summary: Brief summary of what was done
        status: "completed" or "failed"
        channel: Target channel

    Returns:
        True if successful, False otherwise
    """
    emoji_status = "success" if status == "completed" else "error"

    title = f"Agent Complete: {agent_type}"
    message = task_summary or f"Agent `{agent_type}` has finished."

    return notify_slack_rich(title, message, emoji_status, channel)


def notify_input_required(
    context: Optional[str] = None,
    channel: Optional[str] = None
) -> bool:
    """
    Send a notification that user input is required.

    Args:
        context: Optional context about what input is needed
        channel: Target channel

    Returns:
        True if successful, False otherwise
    """
    engineer = os.getenv('ENGINEER_NAME', '')

    if engineer:
        message = f"{engineer}, your agent needs your input"
    else:
        message = "Your agent needs your input"

    if context:
        message = f"{message}: {context}"

    return notify_slack(f":bell: {message}", channel)


# CLI usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python slack_notifier.py <message> [channel]")
        print("       python slack_notifier.py --rich <title> <message> [status]")
        print("       python slack_notifier.py --command <name> <status> [details]")
        print("       python slack_notifier.py --agent <type> [summary] [status]")
        print("       python slack_notifier.py --input [context]")
        sys.exit(1)

    if sys.argv[1] == "--rich":
        title = sys.argv[2] if len(sys.argv) > 2 else "Notification"
        message = sys.argv[3] if len(sys.argv) > 3 else "No message"
        status = sys.argv[4] if len(sys.argv) > 4 else "info"
        success = notify_slack_rich(title, message, status)
    elif sys.argv[1] == "--command":
        name = sys.argv[2] if len(sys.argv) > 2 else "/unknown"
        status = sys.argv[3] if len(sys.argv) > 3 else "completed"
        details = sys.argv[4] if len(sys.argv) > 4 else None
        success = notify_command_complete(name, status, details)
    elif sys.argv[1] == "--agent":
        agent_type = sys.argv[2] if len(sys.argv) > 2 else "unknown-agent"
        summary = sys.argv[3] if len(sys.argv) > 3 else None
        status = sys.argv[4] if len(sys.argv) > 4 else "completed"
        success = notify_agent_complete(agent_type, summary, status)
    elif sys.argv[1] == "--input":
        context = sys.argv[2] if len(sys.argv) > 2 else None
        success = notify_input_required(context)
    else:
        message = sys.argv[1]
        channel = sys.argv[2] if len(sys.argv) > 2 else None
        success = notify_slack(message, channel)

    print("OK" if success else "SKIP")
    sys.exit(0)  # Always exit 0 to not disrupt framework
