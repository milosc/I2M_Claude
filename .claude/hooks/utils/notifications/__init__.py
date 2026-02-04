"""
Notification utilities for Claude Code hooks.

This package provides multi-channel notification capabilities:
- Slack notifications
- (Future: Email, SMS, Discord, etc.)

All notification functions are designed to fail silently to avoid
disrupting the main framework workflow.
"""

from .slack_notifier import notify_slack, notify_slack_rich

__all__ = ['notify_slack', 'notify_slack_rich']
