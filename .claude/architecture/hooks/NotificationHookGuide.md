# Notification Hook Guide

**Version**: 1.0.0
**Last Updated**: 2026-02-03

---

## Overview

The Notification Hook system provides multi-channel notifications for Claude Code events. Currently supports **Slack** with an extensible architecture for future channels (email, SMS, Discord, etc.).

**Key Design Principle**: All notification hooks are designed to **FAIL SILENTLY** - they never disrupt the main framework workflow, even if the notification service is unavailable.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Claude Code Events                              │
│    ┌──────────────┐    ┌──────────────┐    ┌────────────────┐          │
│    │ Notification │    │     Stop     │    │  SubagentStop  │          │
│    │ (Input Req)  │    │ (Session End)│    │ (Agent Done)   │          │
│    └──────┬───────┘    └──────┬───────┘    └───────┬────────┘          │
│           │                   │                    │                    │
│           └───────────────────┼────────────────────┘                    │
│                               ▼                                         │
│                   ┌───────────────────────┐                             │
│                   │ slack_notification_   │                             │
│                   │      hook.py          │                             │
│                   │                       │                             │
│                   │  - Event routing      │                             │
│                   │  - Silent failure     │                             │
│                   │  - Logging            │                             │
│                   └───────────┬───────────┘                             │
│                               │                                         │
│                               ▼                                         │
│                   ┌───────────────────────┐                             │
│                   │  utils/notifications/ │                             │
│                   │    slack_notifier.py  │                             │
│                   │                       │                             │
│                   │  - notify_slack()     │                             │
│                   │  - notify_slack_rich()│                             │
│                   │  - API integration    │                             │
│                   └───────────┬───────────┘                             │
│                               │                                         │
│                               ▼                                         │
│                        ┌─────────────┐                                  │
│                        │  Slack API  │                                  │
│                        └─────────────┘                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
.claude/hooks/
├── slack_notification_hook.py      # Main hook entry point
├── utils/
│   └── notifications/
│       ├── __init__.py             # Package exports
│       └── slack_notifier.py       # Slack API integration
└── settings.json                   # Hook configuration

.claude/architecture/hooks/
└── NotificationHookGuide.md        # This documentation

_state/logs/
└── slack_notifications.jsonl       # Notification audit log
```

---

## Setup

### Prerequisites

1. **Slack App Created** with proper scopes (see `docs/SLACK_NOTIFICATION_SETUP.md`)
2. **Bot Token** obtained after installing app to workspace

### Environment Variables

Add to `~/.zshrc` or `~/.bashrc`:

```bash
# Required
export SLACK_BOT_TOKEN="xoxb-your-token-here"

# Optional
export SLACK_CHANNEL="#claude-notifications"     # Default channel
export ENGINEER_NAME="YourName"                  # For personalized messages
export SLACK_NOTIFICATIONS_ENABLED="true"        # Kill switch (default: true)
```

Reload shell:
```bash
source ~/.zshrc
```

### Verify Setup

```bash
# Test the notifier directly
uv run .claude/hooks/utils/notifications/slack_notifier.py "Test notification"

# Test via hook
uv run .claude/hooks/slack_notification_hook.py --event Custom --message "Test" --title "Setup Test" --status success
```

---

## Hook Events

### Notification Event

**Triggered**: When Claude Code needs user input (permission requests, questions, etc.)

**Configuration** (settings.json):
```json
"Notification": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type Notification"
      },
      {
        "type": "command",
        "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/slack_notification_hook.py\" --event Notification --quiet"
      }
    ]
  }
]
```

**Slack Message**: `:bell: {ENGINEER_NAME}, your agent needs your input`

### Stop Event

**Triggered**: When main Claude Code session ends

**Configuration** (settings.json):
```json
"Stop": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type Stop"
      },
      {
        "type": "command",
        "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/slack_notification_hook.py\" --event Stop --status completed --quiet"
      }
    ]
  }
]
```

**Slack Message**: Rich formatted message with title "Claude Code Session Complete"

### SubagentStop Event

**Triggered**: When a spawned subagent completes its task

**Configuration** (settings.json):
```json
"SubagentStop": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py\" --event-type SubagentStop"
      },
      {
        "type": "command",
        "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/slack_notification_hook.py\" --event SubagentStop --quiet"
      }
    ]
  }
]
```

**Slack Message**: Rich formatted message with agent type and completion status

---

## API Reference

### slack_notifier.py

#### `notify_slack(message, channel=None, emoji=":robot_face:", username="Claude Code")`

Send a simple text notification.

```python
from utils.notifications import notify_slack

notify_slack("Build complete!")
notify_slack("Test passed!", channel="#ci-cd")
```

#### `notify_slack_rich(title, message, status="info", channel=None)`

Send a rich formatted notification with color coding.

```python
from utils.notifications import notify_slack_rich

notify_slack_rich(
    title="Build Complete",
    message="All 47 tests passed in 12.3 seconds",
    status="success"  # info, success, warning, error
)
```

**Status Colors**:
| Status | Color | Emoji |
|--------|-------|-------|
| `info` | Green (#36a64f) | :information_source: |
| `success` | Bright Green (#00ff00) | :white_check_mark: |
| `warning` | Yellow (#ffcc00) | :warning: |
| `error` | Red (#ff0000) | :x: |

#### `notify_command_complete(command_name, status="completed", details=None)`

Notify about command completion.

```python
from utils.notifications.slack_notifier import notify_command_complete

notify_command_complete("/discovery", "completed", "Generated 15 personas")
```

#### `notify_agent_complete(agent_type, task_summary=None, status="completed")`

Notify about agent/subagent completion.

```python
from utils.notifications.slack_notifier import notify_agent_complete

notify_agent_complete(
    "discovery-domain-researcher",
    "Analyzed 12 interview transcripts",
    "completed"
)
```

#### `notify_input_required(context=None)`

Notify that user input is required.

```python
from utils.notifications.slack_notifier import notify_input_required

notify_input_required("Permission needed to write to config file")
```

---

## CLI Usage

### Direct Notifier

```bash
# Simple message
uv run .claude/hooks/utils/notifications/slack_notifier.py "Your message"

# Rich notification
uv run .claude/hooks/utils/notifications/slack_notifier.py --rich "Title" "Message" success

# Command notification
uv run .claude/hooks/utils/notifications/slack_notifier.py --command "/discovery" completed

# Agent notification
uv run .claude/hooks/utils/notifications/slack_notifier.py --agent "discovery-researcher" "Found 5 pain points"

# Input required
uv run .claude/hooks/utils/notifications/slack_notifier.py --input "Need file permission"
```

### Hook Entry Point

```bash
# Notification event
uv run .claude/hooks/slack_notification_hook.py --event Notification

# Stop event
uv run .claude/hooks/slack_notification_hook.py --event Stop --status completed

# SubagentStop event
uv run .claude/hooks/slack_notification_hook.py --event SubagentStop --agent-type "discovery-researcher"

# Command end event
uv run .claude/hooks/slack_notification_hook.py --event CommandEnd --command "/discovery" --status completed

# Custom notification
uv run .claude/hooks/slack_notification_hook.py --event Custom --message "Build done" --title "CI" --status success
```

---

## Silent Failure Design

**Critical**: All notification code is wrapped in try/except blocks that catch ALL exceptions and return gracefully. This ensures:

1. **Framework never breaks** - Even if Slack is down, token is invalid, or network fails
2. **Always exit 0** - The hook always exits with code 0
3. **Failures are logged** - Issues are logged to `_state/logs/slack_notifications.jsonl`

### Example Pattern

```python
def notify_slack(message: str) -> bool:
    try:
        token = os.getenv('SLACK_BOT_TOKEN')
        if not token:
            return False  # No token = silent skip

        # ... API call ...
        return result.get('ok', False)

    except Exception:
        # SILENT FAILURE - never disrupt the framework
        return False
```

### Kill Switch

To completely disable Slack notifications without removing configuration:

```bash
export SLACK_NOTIFICATIONS_ENABLED="false"
```

---

## Logging & Debugging

### Notification Log

All notification attempts are logged to `_state/logs/slack_notifications.jsonl`:

```json
{"timestamp": "2026-02-03T10:30:45.123456", "event_type": "Notification", "success": true, "details": null}
{"timestamp": "2026-02-03T10:31:12.654321", "event_type": "Stop", "success": true, "details": "status=completed"}
{"timestamp": "2026-02-03T10:32:00.000000", "event_type": "SubagentStop", "success": false, "details": "Error: timeout"}
```

### Debug Mode

Remove `--quiet` from settings.json to see output:

```json
"command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/slack_notification_hook.py\" --event Notification"
```

Output will show:
- `SLACK_NOTIFY: Notification sent` - Success
- `SLACK_NOTIFY: Disabled or not configured` - No token or disabled
- `SLACK_NOTIFY: Notification skipped` - API failure
- `SLACK_NOTIFY: Error (ignored): ...` - Exception occurred

---

## Extending to Other Channels

The architecture supports adding new notification channels:

### 1. Create New Notifier

```python
# .claude/hooks/utils/notifications/email_notifier.py

import os
import smtplib
from email.mime.text import MIMEText

def notify_email(subject: str, message: str, recipient: str = None) -> bool:
    try:
        recipient = recipient or os.getenv('NOTIFY_EMAIL')
        if not recipient:
            return False

        # ... email sending logic ...
        return True

    except Exception:
        return False
```

### 2. Update Package Init

```python
# .claude/hooks/utils/notifications/__init__.py

from .slack_notifier import notify_slack, notify_slack_rich
from .email_notifier import notify_email

__all__ = ['notify_slack', 'notify_slack_rich', 'notify_email']
```

### 3. Integrate in Hook

```python
# In slack_notification_hook.py (or create unified notification_hook.py)

def handle_notification_event(context=None):
    # Slack
    notify_slack(...)

    # Email (if configured)
    if os.getenv('NOTIFY_EMAIL'):
        notify_email(...)

    # SMS (if configured)
    if os.getenv('TWILIO_ACCOUNT_SID'):
        notify_sms(...)
```

### Potential Channels

| Channel | Env Var | Package |
|---------|---------|---------|
| Email | `NOTIFY_EMAIL`, `SMTP_*` | `smtplib` (stdlib) |
| SMS (Twilio) | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` | `twilio` |
| Discord | `DISCORD_WEBHOOK_URL` | `urllib` (stdlib) |
| Teams | `TEAMS_WEBHOOK_URL` | `urllib` (stdlib) |
| Push (FCM) | `FCM_SERVER_KEY` | `firebase-admin` |

---

## Troubleshooting

### No Notifications Received

1. **Check token is set**:
   ```bash
   echo $SLACK_BOT_TOKEN
   ```

2. **Test manually**:
   ```bash
   curl -X POST https://slack.com/api/chat.postMessage \
     -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
     -H "Content-Type: application/json; charset=utf-8" \
     -d '{"channel":"#claude-notifications","text":"Test"}'
   ```

3. **Check log file**:
   ```bash
   tail -20 _state/logs/slack_notifications.jsonl
   ```

4. **Remove `--quiet` flag** in settings.json to see output

### Wrong Channel

- Verify channel exists and is spelled correctly
- Try using Channel ID instead of name (e.g., `C0XXXXXXXX`)
- For private channels, invite the bot: `/invite @ClaudeBuilder`

### Token Issues

- Ensure using Bot Token (`xoxb-`), not User Token (`xoxp-`)
- After adding scopes, **reinstall app** to get new token
- Token must match the workspace where channel exists

---

## Related Files

| File | Purpose |
|------|---------|
| `docs/SLACK_NOTIFICATION_SETUP.md` | Slack app setup guide |
| `.claude/settings.json` | Hook configuration |
| `.claude/hooks/slack_notification_hook.py` | Main hook entry point |
| `.claude/hooks/utils/notifications/slack_notifier.py` | Slack API integration |
| `_state/logs/slack_notifications.jsonl` | Notification audit log |

---

## Changelog

### v1.0.0 (2026-02-03)
- Initial implementation
- Slack integration for Notification, Stop, SubagentStop events
- Silent failure design
- Rich message formatting
- CLI interface
- Comprehensive logging
