# Slack Notification Setup Guide

**Purpose**: Configure Slack to receive notifications from Claude Code hooks (task completion, input required, subagent updates).

---

## Prerequisites

- Slack workspace admin access (or permission to install apps)
- Shell access to set environment variables

---

## Step 1: Create a Slack App

1. Go to **https://api.slack.com/apps**
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Enter:
   - **App Name**: `Claude Code Notifications` (or your preference)
   - **Workspace**: Select your workspace
5. Click **"Create App"**

---

## Step 2: Configure Bot Permissions (CRITICAL)

> **Common Error**: `missing_scope` / `chat:write:bot` needed
>
> If you see this error, your bot is missing required permissions. Follow these steps carefully.

1. In your app's settings, go to **"OAuth & Permissions"** (left sidebar)
2. Scroll to **"Scopes"** section
3. Find **"Bot Token Scopes"** (NOT User Token Scopes)
4. Click **"Add an OAuth Scope"** and add these scopes:

| Scope | Purpose | Required |
|-------|---------|----------|
| `chat:write` | Send messages to channels | **YES** |
| `chat:write.public` | Post to public channels without joining | **YES** |
| `users:read` | Look up user IDs (for DMs) | Optional |
| `im:write` | Send direct messages | Optional |

**Minimum required**: `chat:write` + `chat:write.public`

### After Adding Scopes - REINSTALL THE APP

> **Important**: After changing scopes, you MUST reinstall the app!

1. Scroll up to **"OAuth Tokens for Your Workspace"**
2. Click **"Reinstall to Workspace"** (or "Install to Workspace" if first time)
3. Review permissions and click **"Allow"**
4. Copy the new **"Bot User OAuth Token"** (starts with `xoxb-`)

---

## Step 3: Create a Notification Channel

**Option A: New dedicated channel (Recommended)**
1. In Slack, create channel: `#claude-notifications` or `#claudebuilder`
2. Bot can post without being invited (due to `chat:write.public`)

**Option B: Use existing channel**
- Invite the bot: Type `/invite @Claude Code Notifications` in the channel

---

## Step 4: Set Environment Variables

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# Required
export SLACK_BOT_TOKEN="xoxb-your-new-token-here"

# Optional - default channel
export SLACK_CHANNEL="#claude-notifications"

# Optional - for personalized messages
export ENGINEER_NAME="Milos"
```

**Reload your shell:**
```bash
source ~/.zshrc
# or
source ~/.bashrc
```

**Verify it's set:**
```bash
echo $SLACK_BOT_TOKEN
# Should print: xoxb-...
```

---

## Step 5: Test the Integration

### Quick Test (curl)

```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "channel": "#claude-notifications",
    "text": "✅ Claude Code notifications connected!"
  }'
```

**Expected success response:**
```json
{"ok":true,"channel":"C0XXXXXXXXX","ts":"1234567890.123456",...}
```

### Python Test

```bash
python3 -c "
import os, json, urllib.request
token = os.getenv('SLACK_BOT_TOKEN')
data = json.dumps({'channel': '#claude-notifications', 'text': 'Python test!'}).encode()
req = urllib.request.Request(
    'https://slack.com/api/chat.postMessage',
    data=data,
    headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json; charset=utf-8'}
)
print(urllib.request.urlopen(req).read().decode())
"
```

---

## Troubleshooting

### Error: `missing_scope`

```json
{"ok":false,"error":"missing_scope","needed":"chat:write:bot","provided":"app_mentions:read,bookmarks:read"}
```

**Fix:**
1. Go to https://api.slack.com/apps → Select your app
2. Go to **OAuth & Permissions** → **Bot Token Scopes**
3. Add `chat:write` and `chat:write.public`
4. **Click "Reinstall to Workspace"** ← Don't forget this!
5. Copy the NEW token and update `SLACK_BOT_TOKEN`

### Error: `not_in_channel`

**Fix:** Either:
- Add `chat:write.public` scope (can post to any public channel), OR
- Invite bot to channel: `/invite @Claude Code Notifications`

### Error: `invalid_auth`

**Fix:**
- Token may be expired or incorrect
- Go to OAuth & Permissions → Copy fresh token
- Make sure you're using Bot Token (`xoxb-`), not User Token (`xoxp-`)

### Error: `channel_not_found`

**Fix:**
- Check channel name spelling (include `#`)
- Try using Channel ID instead of name:
  1. Right-click channel → "View channel details"
  2. Scroll to bottom → Copy ID (starts with `C`)
  3. Use ID: `"channel": "C0XXXXXXXXX"`

### Warning: `missing_charset`

**Fix:** Add charset to Content-Type header:
```bash
-H "Content-Type: application/json; charset=utf-8"
```

---

## Python Integration Code

Create `.claude/hooks/utils/notifications/slack_notifier.py`:

```python
#!/usr/bin/env python3
"""Slack notification utility for Claude Code hooks."""

import os
import json
import urllib.request
import urllib.error
from typing import Optional

def notify_slack(
    message: str,
    channel: Optional[str] = None,
    emoji: str = ":robot_face:",
    username: str = "Claude Code"
) -> bool:
    """
    Send a notification to Slack.

    Args:
        message: The notification text
        channel: Channel to post to (default: SLACK_CHANNEL env or #claude-notifications)
        emoji: Bot emoji icon
        username: Display name for the bot

    Returns:
        True if successful, False otherwise
    """
    token = os.getenv('SLACK_BOT_TOKEN')
    if not token:
        return False

    channel = channel or os.getenv('SLACK_CHANNEL', '#claude-notifications')

    payload = {
        "channel": channel,
        "text": message,
        "icon_emoji": emoji,
        "username": username
    }

    try:
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
            if not result.get('ok'):
                print(f"Slack error: {result.get('error')}")
            return result.get('ok', False)

    except (urllib.error.URLError, json.JSONDecodeError, Exception) as e:
        print(f"Slack notification failed: {e}")
        return False


def notify_slack_rich(
    title: str,
    message: str,
    status: str = "info",
    channel: Optional[str] = None
) -> bool:
    """
    Send a rich formatted Slack message with color coding.

    Args:
        title: Header text
        message: Body text (supports Slack mrkdwn)
        status: One of "info", "success", "warning", "error"
        channel: Target channel

    Returns:
        True if successful, False otherwise
    """
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
                        "text": f":robot_face: Claude Code • {engineer}"
                    }]
                }
            ]
        }]
    }

    try:
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
        return False


# CLI usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python slack_notifier.py <message> [channel]")
        print("       python slack_notifier.py --rich <title> <message> [status]")
        sys.exit(1)

    if sys.argv[1] == "--rich":
        title = sys.argv[2] if len(sys.argv) > 2 else "Notification"
        message = sys.argv[3] if len(sys.argv) > 3 else "No message"
        status = sys.argv[4] if len(sys.argv) > 4 else "info"
        success = notify_slack_rich(title, message, status)
    else:
        message = sys.argv[1]
        channel = sys.argv[2] if len(sys.argv) > 2 else None
        success = notify_slack(message, channel)

    print("✅ Sent" if success else "❌ Failed")
    sys.exit(0 if success else 1)
```

---

## Hook Integration Examples

### Add to notification.py

```python
# At the top
from utils.notifications.slack_notifier import notify_slack

# In announce_notification()
def announce_notification():
    message = "Your agent needs your input"

    # TTS (existing)
    try:
        tts_script = get_tts_script_path()
        subprocess.run(["uv", "run", tts_script, message], timeout=10)
    except:
        pass

    # Slack (new)
    notify_slack(f"🔔 {message}")
```

### Add to stop.py

```python
from utils.notifications.slack_notifier import notify_slack_rich

def announce_stop():
    # ... existing TTS logic ...

    # Slack rich notification
    notify_slack_rich(
        title="Task Complete",
        message="Claude Code has finished the current task.",
        status="success"
    )
```

### Add to subagent_stop.py

```python
from utils.notifications.slack_notifier import notify_slack

def announce_subagent_completion(summary: str):
    # ... existing TTS logic ...

    # Slack notification
    notify_slack(f"🤖 Subagent: {summary}")
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SLACK_BOT_TOKEN` | **Yes** | - | Bot token (`xoxb-...`) |
| `SLACK_CHANNEL` | No | `#claude-notifications` | Default channel |
| `ENGINEER_NAME` | No | `Developer` | Name for personalized messages |

---

## Quick Reference

### Scopes Checklist
- [x] `chat:write` - Send messages
- [x] `chat:write.public` - Post to public channels
- [ ] `users:read` - Optional: lookup users
- [ ] `im:write` - Optional: send DMs

### After Any Scope Change
1. Go to OAuth & Permissions
2. Click **"Reinstall to Workspace"**
3. Copy new token
4. Update `SLACK_BOT_TOKEN` env var

### Test Command
```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{"channel":"#claude-notifications","text":"Test!"}'
```

---

## Related Files

- TTS hooks: `.claude/hooks/notification.py`, `stop.py`, `subagent_stop.py`
- TTS backends: `.claude/hooks/utils/tts/`
- Slack notifier: `.claude/hooks/utils/notifications/slack_notifier.py`
