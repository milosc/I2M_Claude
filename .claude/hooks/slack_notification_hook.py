#!/usr/bin/env python3
"""
Slack Notification Hook

Integrates Slack notifications with Claude Code hooks.
Called by settings.json hooks for Notification, Stop, and SubagentStop events.

This hook is designed to NEVER FAIL - all errors are caught and logged
silently to avoid disrupting the main framework workflow.

Usage:
    # For Notification events (user input required)
    python slack_notification_hook.py --event Notification

    # For Stop events (main agent complete)
    python slack_notification_hook.py --event Stop --status completed

    # For SubagentStop events
    python slack_notification_hook.py --event SubagentStop --agent-type "discovery-researcher"

    # For command completion
    python slack_notification_hook.py --event CommandEnd --command "/discovery" --status completed

Environment Variables:
    SLACK_BOT_TOKEN: Required for Slack notifications
    SLACK_CHANNEL: Optional, default channel
    ENGINEER_NAME: Optional, for personalized messages
    SLACK_NOTIFICATIONS_ENABLED: Set to "false" to disable (default: true)

Exit Codes:
    Always 0 - This hook NEVER fails to avoid disrupting the framework
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


# Add utils to path
sys.path.insert(0, str(Path(__file__).parent / "utils" / "notifications"))

try:
    from slack_notifier import (
        notify_slack,
        notify_slack_rich,
        notify_command_complete,
        notify_agent_complete,
        notify_input_required
    )
    SLACK_AVAILABLE = True
except ImportError:
    SLACK_AVAILABLE = False


def is_notifications_enabled() -> bool:
    """Check if Slack notifications are enabled."""
    # Check kill switch
    enabled = os.getenv('SLACK_NOTIFICATIONS_ENABLED', 'true').lower()
    if enabled in ('false', '0', 'no', 'off'):
        return False

    # Check if token is configured
    if not os.getenv('SLACK_BOT_TOKEN'):
        return False

    return SLACK_AVAILABLE


def log_notification_attempt(event_type: str, success: bool, details: Optional[str] = None) -> None:
    """
    Log notification attempt to file for debugging.
    Silent - never raises exceptions.
    """
    try:
        log_dir = Path("_state/logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "slack_notifications.jsonl"

        entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "success": success,
            "details": details
        }

        with open(log_file, 'a') as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # Silent failure


def handle_notification_event(context: Optional[str] = None) -> bool:
    """
    Handle Notification event (user input required).

    Args:
        context: Optional context about what input is needed

    Returns:
        True if notification sent successfully
    """
    if not is_notifications_enabled():
        return False

    success = notify_input_required(context)
    log_notification_attempt("Notification", success, context)
    return success


def handle_stop_event(status: str = "completed", details: Optional[str] = None) -> bool:
    """
    Handle Stop event (main agent complete).

    Args:
        status: "completed", "failed", or "cancelled"
        details: Optional details about completion

    Returns:
        True if notification sent successfully
    """
    if not is_notifications_enabled():
        return False

    engineer = os.getenv('ENGINEER_NAME', '')

    if status == "completed":
        title = "Claude Code Session Complete"
        message = details or "Your Claude Code session has finished successfully."
        emoji_status = "success"
    elif status == "failed":
        title = "Claude Code Session Failed"
        message = details or "Your Claude Code session encountered an error."
        emoji_status = "error"
    else:
        title = "Claude Code Session Ended"
        message = details or f"Session ended with status: {status}"
        emoji_status = "info"

    if engineer:
        message = f"{engineer}, {message.lower()}"

    success = notify_slack_rich(title, message, emoji_status)
    log_notification_attempt("Stop", success, f"status={status}")
    return success


def handle_subagent_stop_event(
    agent_type: str,
    status: str = "completed",
    summary: Optional[str] = None
) -> bool:
    """
    Handle SubagentStop event.

    Args:
        agent_type: Type of subagent that completed
        status: "completed" or "failed"
        summary: Optional summary of what the agent accomplished

    Returns:
        True if notification sent successfully
    """
    if not is_notifications_enabled():
        return False

    success = notify_agent_complete(agent_type, summary, status)
    log_notification_attempt("SubagentStop", success, f"agent={agent_type}, status={status}")
    return success


def handle_command_end_event(
    command_name: str,
    status: str = "completed",
    details: Optional[str] = None
) -> bool:
    """
    Handle CommandEnd event.

    Args:
        command_name: Name of the command
        status: "completed", "failed", or "cancelled"
        details: Optional details

    Returns:
        True if notification sent successfully
    """
    if not is_notifications_enabled():
        return False

    success = notify_command_complete(command_name, status, details)
    log_notification_attempt("CommandEnd", success, f"command={command_name}, status={status}")
    return success


def handle_custom_event(message: str, title: Optional[str] = None, status: str = "info") -> bool:
    """
    Handle custom notification event.

    Args:
        message: The notification message
        title: Optional title for rich notification
        status: Status for color coding

    Returns:
        True if notification sent successfully
    """
    if not is_notifications_enabled():
        return False

    if title:
        success = notify_slack_rich(title, message, status)
    else:
        success = notify_slack(message)

    log_notification_attempt("Custom", success, message[:50])
    return success


def main():
    """Main entry point for the hook."""
    parser = argparse.ArgumentParser(
        description="Slack Notification Hook",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Events:
  Notification   - User input required
  Stop           - Main agent session complete
  SubagentStop   - Subagent completed
  CommandEnd     - Command completed
  Custom         - Custom notification

Examples:
  %(prog)s --event Notification
  %(prog)s --event Stop --status completed
  %(prog)s --event SubagentStop --agent-type "discovery-researcher"
  %(prog)s --event CommandEnd --command "/discovery" --status completed
  %(prog)s --event Custom --message "Build finished" --title "CI/CD" --status success
        """
    )

    parser.add_argument(
        "--event",
        required=True,
        choices=["Notification", "Stop", "SubagentStop", "CommandEnd", "Custom"],
        help="Event type to handle"
    )
    parser.add_argument("--status", default="completed", help="Event status")
    parser.add_argument("--command", help="Command name (for CommandEnd)")
    parser.add_argument("--agent-type", help="Agent type (for SubagentStop)")
    parser.add_argument("--summary", help="Task summary (for SubagentStop)")
    parser.add_argument("--message", help="Custom message")
    parser.add_argument("--title", help="Title for rich notifications")
    parser.add_argument("--context", help="Context for Notification events")
    parser.add_argument("--details", help="Additional details")
    parser.add_argument("--quiet", action="store_true", help="Suppress output")

    args = parser.parse_args()

    try:
        success = False

        if args.event == "Notification":
            success = handle_notification_event(args.context)

        elif args.event == "Stop":
            success = handle_stop_event(args.status, args.details)

        elif args.event == "SubagentStop":
            agent_type = args.agent_type or "unknown-agent"
            success = handle_subagent_stop_event(agent_type, args.status, args.summary)

        elif args.event == "CommandEnd":
            command = args.command or "/unknown"
            success = handle_command_end_event(command, args.status, args.details)

        elif args.event == "Custom":
            message = args.message or "Notification from Claude Code"
            success = handle_custom_event(message, args.title, args.status)

        if not args.quiet:
            if success:
                print(f"SLACK_NOTIFY: {args.event} sent")
            elif not is_notifications_enabled():
                print(f"SLACK_NOTIFY: Disabled or not configured")
            else:
                print(f"SLACK_NOTIFY: {args.event} skipped")

    except Exception as e:
        # NEVER fail - just log the error
        if not args.quiet:
            print(f"SLACK_NOTIFY: Error (ignored): {str(e)[:50]}")
        log_notification_attempt(args.event, False, f"Error: {str(e)[:100]}")

    # ALWAYS exit 0 to not disrupt the framework
    sys.exit(0)


if __name__ == "__main__":
    main()
