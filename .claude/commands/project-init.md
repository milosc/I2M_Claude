---
description: Initialize project metadata (name, user, stage)
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

# /project-init - Initialize Project Metadata

## Purpose

Captures project name, user context, and stage at the start of a new HTEC framework workflow.

**When to run**: Before ANY orchestrator command (/discovery, /prototype, etc.) or when session warnings appear.

## Execution Steps

### Step 1: Check Current State

Read current session to show what needs fixing:

```bash
cat _state/session.json 2>/dev/null || echo "⚠️  No session file found"
```

### Step 2: Extract User Context

Get real username (not "system"):

```bash
USER_NAME=$(python3 .claude/hooks/get_user_context.py)
echo "✅ Detected user: $USER_NAME"
```

### Step 3: Prompt for Project Name

Use AskUserQuestion to get project name:

1. First ask if they want to use directory name or custom name
2. If custom, ask for the specific project name
3. Validate the name is not empty or invalid

**Example valid project names:**
- InventorySystem
- ERTriage
- CustomerPortal
- WarehouseManagement

### Step 4: Update Session File

Update session.json with meaningful values:

```bash
# Update project and stage
bash .claude/hooks/session-update.sh \
  --project "{ProjectName}" \
  --stage "initialization" \
  --description "Project initialized via /project-init"

# Update user field
python3 .claude/hooks/update_session_user.py "$USER_NAME"
```

### Step 5: Validate

Verify session is now valid:

```bash
python3 .claude/hooks/validate_session.py
```

Show final state:

```bash
echo ""
echo "✅ Project initialized successfully:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat _state/session.json | jq '{project, user, stage, updated_at}'
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

### Step 6: Suggest Next Command

Based on project state, suggest the appropriate next command:

```
✅ Project initialized successfully

📋 Next Steps:

  1. Start Discovery analysis:
     /discovery {ProjectName} Client_Materials/

  2. Or if Discovery is complete, generate Prototype:
     /prototype {ProjectName}

  3. Or if Prototype is complete, generate ProductSpecs:
     /productspecs {ProjectName}

  4. Check status anytime:
     /discovery-status
     /prototype-status
     /productspecs-status
```

## Success Criteria

- ✅ session.json exists
- ✅ project != "pending", "unknown", "system", etc.
- ✅ user != "system", "unknown", "Claude", etc.
- ✅ validate_session.py passes
- ✅ User knows what command to run next

## Error Handling

If session file doesn't exist, it will be created by session-update.sh automatically.

If user provides invalid project name (empty, "pending", "unknown"), ask again with clear error message.

## Notes

- This command is **optional but recommended** for new projects
- Orchestrator commands will show warnings if session is invalid
- Running this command fixes those warnings
- Can be run multiple times to update project metadata
