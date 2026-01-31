---
name: logging-prompt-execution
description: Use when you need to maintain a centralized audit trail of all prompts executed during the prototype generation lifecycle.
model: haiku
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill logging-prompt-execution started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill logging-prompt-execution ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill logging-prompt-execution instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

# Prompt Log System

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_PromptLog
- **Version**: 2.3.1
- **Created**: 2024-12-13
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3

## Description
Centralized logging of all prompts executed during prototype generation. Every skill MUST actively write to this log during execution.

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

Centralized logging of all prompts executed during prototype generation. Every skill MUST actively write to this log during execution.

## Execution Logging (MANDATORY)

This skill logs all execution to the global pipeline progress registry. Logging is automatic and requires no manual configuration.

### How Logging Works

Every execution of this skill is logged to `_state/lifecycle.json`:

- **start_event**: Logged when skill execution begins
- **end_event**: Logged when skill execution completes

Events include:
- skill_name, intent, stage, system_name
- start/end timestamps
- status (completed/failed)
- output files created (prompt logs)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "logging-prompt-execution"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "logging-prompt-execution" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## ⚠️ CRITICAL: This Requires ACTUAL File Operations

**Claude must ACTUALLY read and write files, not just document the intention.**

When executing any skill that generates content, Claude must:

1. **BEFORE generating**: Use file tools to READ `_state/prompt_log.json`, modify the JSON, and WRITE it back
2. **AFTER generating**: Use file tools to READ, update the entry result, and WRITE again

This is not pseudocode. This is not documentation. Claude must perform actual file I/O operations.

**Example of CORRECT behavior:**
```
// Claude actually executes:
Filesystem:read_text_file({path: "_state/prompt_log.json"})
// Claude parses JSON, adds entry
Filesystem:write_file({path: "_state/prompt_log.json", content: updatedJSON})
```

**If `_state/prompt_log.json` has no entries after running skills, Claude failed to follow instructions.**

---

## Active Logging Required

The prompt log is NOT automatically populated. Each skill must:
1. **READ** `_state/prompt_log.json` at the start of each generation step
2. **APPEND** a new entry with prompt details
3. **WRITE** the updated log back to `_state/prompt_log.json`
4. **UPDATE** the entry with results after execution

**This is NOT pseudocode** - skills must actually perform these file operations.

---

## Log Location

- **JSON Log**: `_state/prompt_log.json` (machine-readable, complete)
- **Markdown Log**: `_state/PROMPT_LOG.md` (human-readable, summarized)

---

## Entry Schema

```json
{
  "id": "PL-001",
  "session_id": "sess-001",
  "timestamp": "2024-12-14T10:30:00Z",
  "skill": "Prototype_Components",
  "step": "Step 4: Generate Component Spec",
  "category": "generation",
  "desired_outcome": "Generate Button component spec with variants and accessibility",
  "inputs": ["00-foundation/DESIGN_TOKENS.md", "_state/requirements_registry.json"],
  "target": "01-components/primitives/button.md",
  "result": {
    "status": "success",
    "output_summary": "Generated Button with 5 variants, 3 sizes, full a11y"
  }
}
```

---

## Integration Pattern (MANDATORY FOR ALL SKILLS)

### Step 1: Initialize Session (Builder does this once)

```
READ _state/prompt_log.json
IF not exists:
  CREATE with structure:
    {
      "version": "1.0",
      "created_at": "{timestamp}",
      "sessions": [],
      "entries": [],
      "summary": { "total_entries": 0, "by_skill": {}, "by_category": {}, "by_status": {} }
    }

CREATE new session entry:
  {
    "session_id": "sess-{NNN}",
    "started_at": "{timestamp}",
    "skills_executed": [],
    "entry_count": 0,
    "success_count": 0,
    "error_count": 0
  }

APPEND to sessions array
WRITE _state/prompt_log.json
```

### Step 2: Log Before Each Generation (Each Skill Does This)

**BEFORE generating any output**, each skill must:

```
READ _state/prompt_log.json
CALCULATE next_id = "PL-" + (summary.total_entries + 1).toString().padStart(3, '0')

CREATE entry:
  {
    "id": "{next_id}",
    "session_id": "{current_session_id}",
    "timestamp": "{ISO timestamp}",
    "skill": "{Prototype_SkillName}",
    "step": "{Step N: Step Name}",
    "category": "{generation|extraction|validation|transformation|analysis}",
    "desired_outcome": "{What this generation should produce}",
    "inputs": ["{list of files being read}"],
    "target": "{file being generated}",
    "result": {
      "status": "pending"
    }
  }

APPEND entry to entries array
INCREMENT summary.total_entries
INCREMENT summary.by_skill[skill] (or create if not exists)
INCREMENT summary.by_category[category]
UPDATE sessions[current].entry_count

WRITE _state/prompt_log.json
```

### Step 3: Update After Generation

**AFTER generating output**, update the entry:

```
READ _state/prompt_log.json
FIND entry by id

UPDATE entry.result:
  {
    "status": "success" | "error" | "partial",
    "output_summary": "{Brief description of what was generated}"
  }

IF status == "success":
  INCREMENT summary.by_status.success
  INCREMENT sessions[current].success_count
ELSE IF status == "error":
  ADD entry.result.error_message = "{error details}"
  INCREMENT summary.by_status.error
  INCREMENT sessions[current].error_count

WRITE _state/prompt_log.json
```

---

## Concrete Example: Component Generation

Here's exactly what the Components skill should do when generating a button spec:

```
// BEFORE generating button.md

READ _state/prompt_log.json AS log

// Calculate next ID
next_id = "PL-" + String(log.summary.total_entries + 1).padStart(3, '0')

// Create entry
new_entry = {
  "id": next_id,
  "session_id": log.sessions[log.sessions.length - 1].session_id,
  "timestamp": new Date().toISOString(),
  "skill": "Prototype_Components",
  "step": "Step 4: Generate Component Spec",
  "category": "generation",
  "desired_outcome": "Generate Button component specification with all variants, sizes, states, and accessibility requirements",
  "inputs": [
    "00-foundation/DESIGN_TOKENS.md",
    "_state/requirements_registry.json"
  ],
  "target": "01-components/primitives/button.md",
  "result": {
    "status": "pending"
  }
}

// Append and update counts
log.entries.push(new_entry)
log.summary.total_entries++
log.summary.by_skill["Prototype_Components"] = (log.summary.by_skill["Prototype_Components"] || 0) + 1
log.summary.by_category["generation"] = (log.summary.by_category["generation"] || 0) + 1
log.sessions[log.sessions.length - 1].entry_count++

WRITE log TO _state/prompt_log.json

// NOW generate button.md
CREATE 01-components/primitives/button.md WITH content...

// AFTER generation complete
READ _state/prompt_log.json AS log

// Find and update the entry
entry_index = log.entries.findIndex(e => e.id === next_id)
log.entries[entry_index].result = {
  "status": "success",
  "output_summary": "Generated Button with 5 variants (primary, secondary, outline, ghost, destructive), 3 sizes, 6 states, full accessibility"
}
log.summary.by_status["success"] = (log.summary.by_status["success"] || 0) + 1
log.sessions[log.sessions.length - 1].success_count++

WRITE log TO _state/prompt_log.json
```

---

## Categories

| Category | When to Use | Examples |
|----------|-------------|----------|
| `generation` | Creating new files | Component specs, screen specs, code |
| `extraction` | Pulling data from sources | Requirements from discovery |
| `validation` | Checking outputs | P0 coverage, accessibility audit |
| `transformation` | Converting formats | Spec to OPML, JSON to MD |
| `analysis` | Analyzing content | Dependency analysis, gap analysis |

---

## Log File Structure

### prompt_log.json

```json
{
  "version": "1.0",
  "created_at": "2024-12-14T09:00:00Z",
  
  "sessions": [
    {
      "session_id": "sess-001",
      "started_at": "2024-12-14T09:00:00Z",
      "ended_at": null,
      "skills_executed": ["Prototype_ValidateDiscovery", "Prototype_Requirements"],
      "entry_count": 15,
      "success_count": 14,
      "error_count": 1
    }
  ],
  
  "entries": [
    {
      "id": "PL-001",
      "session_id": "sess-001",
      "timestamp": "2024-12-14T09:05:00Z",
      "skill": "Prototype_ValidateDiscovery",
      "step": "Step 3: Extract Personas",
      "category": "extraction",
      "desired_outcome": "Extract all personas from discovery/02-user-research/personas/",
      "inputs": ["discovery/02-user-research/personas/*.md"],
      "target": "_state/discovery_summary.json",
      "result": {
        "status": "success",
        "output_summary": "Extracted 4 personas: Recruiter, Hiring Manager, Interviewer, Candidate"
      }
    }
  ],
  
  "summary": {
    "total_entries": 15,
    "by_skill": {
      "Prototype_ValidateDiscovery": 7,
      "Prototype_Requirements": 8
    },
    "by_category": {
      "extraction": 10,
      "generation": 3,
      "validation": 2
    },
    "by_status": {
      "success": 14,
      "error": 1,
      "pending": 0
    }
  }
}
```

---

## Updating PROMPT_LOG.md

After updating prompt_log.json, also update the human-readable markdown:

```
READ _state/prompt_log.json AS log

GENERATE _state/PROMPT_LOG.md:

# Prompt Execution Log

**Generated:** {current timestamp}
**Total Prompts:** {log.summary.total_entries}
**Success Rate:** {success_count / total * 100}%

## Current Session: {latest session_id}

Started: {session.started_at}
Skills: {session.skills_executed.join(", ")}
Prompts: {entry_count} ({success_count} success, {error_count} error)

### Recent Entries

FOR each entry in last 10 entries (newest first):
  #### {entry.id} | {entry.skill} | {entry.step}
  
  **Desired Outcome:** {entry.desired_outcome}
  **Target:** {entry.target}
  **Status:** {entry.result.status === "success" ? "✅" : "❌"} {entry.result.status}
  **Output:** {entry.result.output_summary}
  
  ---

## Summary by Skill

| Skill | Count | Success | Error |
|-------|-------|---------|-------|
FOR each skill in by_skill:
  | {skill} | {count} | ... | ... |

## Summary by Category

| Category | Count |
|----------|-------|
FOR each category in by_category:
  | {category} | {count} |
```

---

## When to Log

Log entries should be created for:

| Action | Log? | Category |
|--------|------|----------|
| Generating a component spec | ✅ Yes | generation |
| Generating a screen spec | ✅ Yes | generation |
| Extracting requirements | ✅ Yes | extraction |
| Creating entity schemas | ✅ Yes | generation |
| Validating P0 coverage | ✅ Yes | validation |
| Generating OPML | ✅ Yes | transformation |
| Reading a file for context | ❌ No | - |
| Writing progress.json | ❌ No | - |
| Simple file copies | ❌ No | - |

**Rule of thumb:** Log when the AI is generating significant content or performing analysis.

---

## Error Handling

When generation fails:

```json
{
  "id": "PL-015",
  "result": {
    "status": "error",
    "error_message": "Missing required input: requirements_registry.json not found",
    "output_summary": null
  }
}
```

---

## Viewing the Log

### Commands

| Command | Action |
|---------|--------|
| `show prompt log` | Display recent entries |
| `show prompt log for {skill}` | Filter by skill |
| `show prompt log errors` | Show only errors |
| `export prompt log` | Save complete log |

### Quick Status

```
READ _state/prompt_log.json

REPORT:
  Session: {current session_id}
  Total Prompts: {total_entries}
  Success: {by_status.success} ({percentage}%)
  Errors: {by_status.error}
  
  By Skill:
  - Prototype_Components: {count}
  - Prototype_Screens: {count}
  ...
```

---

## Skill Integration Checklist

For each skill that generates content:

- [ ] READ prompt_log.json before generation
- [ ] CREATE entry with unique ID, skill name, step, desired outcome
- [ ] APPEND entry to entries array
- [ ] UPDATE summary counts
- [ ] WRITE prompt_log.json
- [ ] PERFORM the generation
- [ ] READ prompt_log.json again
- [ ] UPDATE entry with result status and output summary
- [ ] UPDATE status counts
- [ ] WRITE prompt_log.json
- [ ] UPDATE PROMPT_LOG.md periodically (at least at skill completion)
