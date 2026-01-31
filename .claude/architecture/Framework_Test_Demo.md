# Framework Test Demo - Architecture Documentation

**Version**: 3.0.0 - DETERMINISTIC LIFECYCLE LOGGING
**Purpose**: Demonstrate and validate HTEC framework lifecycle logging using Claude Code native hooks
**Last Updated**: 2026-01-12

---

## Overview

This document describes the **deterministic lifecycle logging architecture** for the HTEC framework. It replaces the previous manual logging approach with Claude Code's native frontmatter hooks and settings-based hooks.

### Key Changes from v2.0

| Aspect | v2.0 (Manual) | v3.0 (Deterministic) |
|--------|---------------|---------------------|
| Command logging | Manual `command_start.py` / `command_end.py` | Frontmatter `PreToolUse` + `Stop` hooks |
| Skill logging | Expected "automatic" (didn't exist) | Frontmatter `PreToolUse` + `Stop` hooks |
| Agent logging | Expected "automatic" (didn't exist) | Instruction-based + `SubagentStop` hook |
| Global detection | None | Settings-based `PreToolUse`/`PostToolUse` matchers |
| Log format | `_state/pipeline_progress.json` | `_state/lifecycle.json` (NDJSON) |
| Determinism | Partial (depended on Claude following instructions) | Full (uses Claude Code native events) |

---

## Architecture

### Component Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HTEC LIFECYCLE LOGGING ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  GLOBAL HOOKS (.claude/settings.json)                                       │
│  ─────────────────────────────────────                                      │
│  │ SessionStart      │ → session started                                    │
│  │ PreToolUse:Task   │ → agent pre_spawn                                    │
│  │ PreToolUse:Skill  │ → skill pre_invoke                                   │
│  │ PostToolUse:Task  │ → agent post_spawn                                   │
│  │ PostToolUse:Skill │ → skill post_invoke                                  │
│  │ Stop              │ → main agent stopped                                 │
│  │ SubagentStop      │ → subagent stopped                                   │
│                                                                             │
│  COMPONENT HOOKS (frontmatter)                                              │
│  ────────────────────────────────                                           │
│  │                                                                          │
│  │  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                    │
│  │  │   COMMAND   │   │    SKILL    │   │  SUBAGENT   │                    │
│  │  │  PreToolUse │   │  PreToolUse │   │ Instruction │                    │
│  │  │  (once:true)│   │  (once:true)│   │   -based    │                    │
│  │  │     Stop    │   │     Stop    │   │ SubagentStop│                    │
│  │  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘                    │
│  │         │                 │                 │                            │
│  │         └─────────────────┴─────────────────┘                            │
│  │                           │                                              │
│  │                           ▼                                              │
│  │         ┌─────────────────────────────────────┐                         │
│  │         │        log-lifecycle.sh             │                         │
│  │         │   (centralized logging helper)      │                         │
│  │         └─────────────────────────────────────┘                         │
│  │                           │                                              │
│  │                           ▼                                              │
│  │         ┌─────────────────────────────────────┐                         │
│  │         │      _state/lifecycle.json          │                         │
│  │         │         (NDJSON format)             │                         │
│  │         └─────────────────────────────────────┘                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Deterministic Logging Reference

### Hook Events Summary

| Event | Fires When | Supports Matcher | Frontmatter Support |
|-------|------------|------------------|---------------------|
| `SessionStart` | Session starts/resumes | No | No |
| `PreToolUse` | Before tool execution | Yes | Yes |
| `PostToolUse` | After tool completion | Yes | Yes |
| `Stop` | Agent finishes responding | No | Yes |
| `SubagentStop` | Subagent finishes | No | Yes |

### Component Logging Matrix

| Component | Start Detection | End Detection | Start Deterministic | End Deterministic |
|-----------|-----------------|---------------|---------------------|-------------------|
| **Command** | `PreToolUse` (once:true) | `Stop` | Partial | **Yes** |
| **Skill** | `PreToolUse` (once:true) | `Stop` | Partial | **Yes** |
| **Subagent** | Instruction-based | `SubagentStop` | **Yes** | **Yes** |
| **Task invocation** | Global `PreToolUse:Task` | Global `PostToolUse:Task` | **Yes** | **Yes** |
| **Skill invocation** | Global `PreToolUse:Skill` | Global `PostToolUse:Skill` | **Yes** | **Yes** |

### Why "Partial" for Start Detection?

- `PreToolUse` with `once: true` only fires when Claude uses a tool
- If a command/skill doesn't trigger any tools, the start event won't fire
- **Workaround**: Instruction-based start (FIRST ACTION MANDATORY section)

---

## Files Created

### 1. Log Helper Script

**File**: `.claude/hooks/log-lifecycle.sh`

```bash
#!/bin/bash
# Usage: log-lifecycle.sh <component> <name> <event> [extra_json]
# Logs to: _state/lifecycle.json
```

### 2. Global Settings Hooks

**File**: `.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [...],
    "PreToolUse": [
      { "matcher": "Task", ... },
      { "matcher": "Skill", ... }
    ],
    "PostToolUse": [
      { "matcher": "Task", ... },
      { "matcher": "Skill", ... }
    ],
    "Stop": [...],
    "SubagentStop": [...]
  }
}
```

### 3. Command with Frontmatter Hooks

**File**: `.claude/commands/test-demo.md`

```yaml
---
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /test-demo started
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /test-demo ended
---
```

### 4. Skill with Frontmatter Hooks

**File**: `.claude/skills/test-demo-gen/SKILL.md`

```yaml
---
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill test-demo-gen started
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill test-demo-gen ended
---
```

### 5. Agent with SubagentStop

**File**: `.claude/agents/test-demo-agent.md`

Agents use instruction-based start (FIRST ACTION) and rely on global `SubagentStop` hook for end detection.

---

## Log Format

### Output File

**Location**: `_state/lifecycle.json`
**Format**: NDJSON (Newline Delimited JSON)

### Event Schema

```json
{
  "component": "command|skill|agent|subagent|session",
  "name": "component-name",
  "event": "started|ended|stopped|pre_spawn|post_spawn|pre_invoke|post_invoke",
  "timestamp": "ISO8601",
  "session": "CLAUDE_SESSION_ID",
  "extra": {}
}
```

### Example Events

```json
{"component": "session", "name": "abc123", "event": "started", "timestamp": "2026-01-12T10:00:00+00:00", "session": "abc123", "extra": {"source": "startup"}}
{"component": "command", "name": "/test-demo", "event": "started", "timestamp": "2026-01-12T10:00:01+00:00", "session": "abc123"}
{"component": "skill", "name": "skill-invoke", "event": "pre_invoke", "timestamp": "2026-01-12T10:00:02+00:00", "session": "abc123"}
{"component": "skill", "name": "test-demo-gen", "event": "started", "timestamp": "2026-01-12T10:00:02+00:00", "session": "abc123"}
{"component": "skill", "name": "test-demo-gen", "event": "ended", "timestamp": "2026-01-12T10:00:03+00:00", "session": "abc123"}
{"component": "skill", "name": "skill-invoke", "event": "post_invoke", "timestamp": "2026-01-12T10:00:03+00:00", "session": "abc123"}
{"component": "agent", "name": "task-spawn", "event": "pre_spawn", "timestamp": "2026-01-12T10:00:04+00:00", "session": "abc123"}
{"component": "subagent", "name": "test-demo-agent", "event": "started", "timestamp": "2026-01-12T10:00:04+00:00", "session": "abc123"}
{"component": "subagent", "name": "test-demo-agent", "event": "ended", "timestamp": "2026-01-12T10:00:05+00:00", "session": "abc123"}
{"component": "subagent", "name": "unknown", "event": "stopped", "timestamp": "2026-01-12T10:00:05+00:00", "session": "abc123"}
{"component": "agent", "name": "task-spawn", "event": "post_spawn", "timestamp": "2026-01-12T10:00:05+00:00", "session": "abc123"}
{"component": "command", "name": "/test-demo", "event": "ended", "timestamp": "2026-01-12T10:00:06+00:00", "session": "abc123"}
{"component": "agent", "name": "main", "event": "stopped", "timestamp": "2026-01-12T10:00:06+00:00", "session": "abc123"}
```

---

## Execution Flow

### Complete Flow: Command → Skill → Agent

```
User invokes: /test-demo
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│ GLOBAL HOOK: SessionStart (if new session)                    │
│ → Logs: session:$SESSION_ID:started                           │
└───────────────────────────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│ COMMAND: /test-demo                                           │
│ FRONTMATTER: PreToolUse (once:true, matcher:*)                │
│ → Logs: command:/test-demo:started                            │
├───────────────────────────────────────────────────────────────┤
│ 1. Initialize (create output dir)                             │
│ 2. Test 1: Direct hook call                                   │
│ 3. Test 2: Invoke skill via Skill() tool                      │
│ 4. Test 3: Spawn agent via Task() tool                        │
│ 5. Verify outputs and analyze lifecycle log                   │
├───────────────────────────────────────────────────────────────┤
│ FRONTMATTER: Stop                                             │
│ → Logs: command:/test-demo:ended                              │
└───────────────────────────────────────────────────────────────┘
```

### Skill Invocation Flow

```
Command calls: Skill({ skill: "test-demo-gen", args: "..." })
        │
        ├─── GLOBAL: PreToolUse (matcher:Skill)
        │    → Logs: skill:skill-invoke:pre_invoke
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│ SKILL: test-demo-gen                                          │
│ FRONTMATTER: PreToolUse (once:true, matcher:*)                │
│ → Logs: skill:test-demo-gen:started                           │
├───────────────────────────────────────────────────────────────┤
│ 1. Parse arguments                                             │
│ 2. Execute skill logic (test_demo_hook.py)                    │
│ 3. Verify output                                               │
├───────────────────────────────────────────────────────────────┤
│ FRONTMATTER: Stop                                             │
│ → Logs: skill:test-demo-gen:ended                             │
└───────────────────────────────────────────────────────────────┘
        │
        ├─── GLOBAL: PostToolUse (matcher:Skill)
        │    → Logs: skill:skill-invoke:post_invoke
        ▼
```

### Agent Spawning Flow

```
Command calls: Task({ subagent_type: "general-purpose", prompt: "..." })
        │
        ├─── GLOBAL: PreToolUse (matcher:Task)
        │    → Logs: agent:task-spawn:pre_spawn
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│ SUBAGENT: test-demo-agent                                     │
│ INSTRUCTION: FIRST ACTION (deterministic workaround)          │
│ → Logs: subagent:test-demo-agent:started                      │
├───────────────────────────────────────────────────────────────┤
│ 1. Parse instructions                                          │
│ 2. Execute agent logic (test_demo_hook.py)                    │
│ 3. Verify output                                               │
│ 4. Return JSON result                                          │
├───────────────────────────────────────────────────────────────┤
│ GLOBAL: SubagentStop                                          │
│ → Logs: subagent:unknown:stopped                              │
└───────────────────────────────────────────────────────────────┘
        │
        ├─── GLOBAL: PostToolUse (matcher:Task)
        │    → Logs: agent:task-spawn:post_spawn
        ▼
```

---

## Implementation Pattern

### For Commands

```yaml
---
description: Your command description
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /your-command started
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /your-command ended
---

## FIRST ACTION (MANDATORY)
Before doing anything else, run:
```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /your-command instruction_start
```
```

### For Skills

```yaml
---
name: your-skill
description: Your skill description
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill your-skill started
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill your-skill ended
---

## FIRST ACTION (MANDATORY)
Before doing anything else, run:
```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill your-skill instruction_start
```
```

### For Agents

```markdown
# Your Agent

## FIRST ACTION (MANDATORY)
Before doing ANYTHING else, run:
```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" subagent your-agent started
```

[Agent instructions follow...]

The end is automatically logged by the global SubagentStop hook in settings.json.
```

---

## Known Limitations & Workarounds

| Limitation | Impact | Workaround |
|------------|--------|------------|
| No `CommandStart` event | Can't deterministically log command activation | `PreToolUse` with `once:true` + instruction-based backup |
| No `SkillStart` event | Can't deterministically log skill activation | `PreToolUse` with `once:true` + instruction-based backup |
| No `SubagentStart` event | Can't deterministically log subagent activation | Instruction-based (FIRST ACTION) |
| `PreToolUse` may not fire | Reported bug (GitHub #6305) | Instruction-based backup |
| `SubagentStop` doesn't know agent name | Can't identify which subagent stopped | Instruction-based logging before stop |
| Frontmatter hooks only in components | Won't log if component not invoked | Global settings.json hooks |

---

## Environment Variables

| Variable | Description | Available In |
|----------|-------------|--------------|
| `CLAUDE_PROJECT_DIR` | Project root directory | All hooks |
| `CLAUDE_SESSION_ID` | Current session identifier | All hooks |
| `CLAUDE_TOOL_NAME` | Name of tool being used | PreToolUse, PostToolUse |
| `CLAUDE_TOOL_INPUT` | JSON input to tool | PreToolUse, PostToolUse |
| `CLAUDE_TOOL_OUTPUT` | JSON output from tool | PostToolUse only |
| `CLAUDE_SESSION_SOURCE` | `"startup"`, `"resume"`, `"clear"` | SessionStart |

---

## Running the Test

### Execute Test Demo

```bash
/test-demo
```

### Verify Results

```bash
# Check output files
ls -la _state/test-demo-outputs/

# Check lifecycle log
cat _state/lifecycle.json

# Count events by type
grep -c '"component": "command"' _state/lifecycle.json
grep -c '"component": "skill"' _state/lifecycle.json
grep -c '"component": "subagent"' _state/lifecycle.json
```

### Expected Output Files

```
_state/test-demo-outputs/
├── command-output.md   (3 paragraphs) ← TEST 1: Direct hook
├── skill-output.md     (4 paragraphs) ← TEST 2: Skill() tool
└── agent-output.md     (3 paragraphs) ← TEST 3: Task() tool
```

### Expected Lifecycle Events

```
_state/lifecycle.json should contain:

1. command:/test-demo:started (via PreToolUse or instruction)
2. skill:skill-invoke:pre_invoke (via global PreToolUse:Skill)
3. skill:test-demo-gen:started (via skill's PreToolUse)
4. skill:test-demo-gen:ended (via skill's Stop)
5. skill:skill-invoke:post_invoke (via global PostToolUse:Skill)
6. agent:task-spawn:pre_spawn (via global PreToolUse:Task)
7. subagent:test-demo-agent:started (via instruction)
8. subagent:unknown:stopped (via global SubagentStop)
9. agent:task-spawn:post_spawn (via global PostToolUse:Task)
10. command:/test-demo:ended (via command's Stop)
11. agent:main:stopped (via global Stop)
```

---

## Migration Guide

### From v2.0 Manual Logging

1. **Remove manual logging calls** from command/skill/agent definitions:
   - Delete `python3 .claude/hooks/command_start.py ...`
   - Delete `python3 .claude/hooks/command_end.py ...`
   - Delete `python3 .claude/hooks/skill_invoke.py ...`
   - Delete `python3 .claude/hooks/agent_spawn.py ...`

2. **Add frontmatter hooks** to each component:
   - Commands: `PreToolUse` (once:true) + `Stop`
   - Skills: `PreToolUse` (once:true) + `Stop`
   - Agents: Instruction-based start (relies on global `SubagentStop`)

3. **Add instruction-based workaround** (FIRST ACTION section) for deterministic start

4. **Update global settings.json** with lifecycle hooks

5. **Update log file reference** from `_state/pipeline_progress.json` to `_state/lifecycle.json`

### Coexistence with Old Logging

The new lifecycle logging system can coexist with the old `pipeline_progress.json` system:
- Old system: `_state/pipeline_progress.json` (JSON with events array)
- New system: `_state/lifecycle.json` (NDJSON, one event per line)

---

## Test Files Reference

| File | Purpose |
|------|---------|
| `.claude/hooks/log-lifecycle.sh` | Centralized logging helper |
| `.claude/settings.json` | Global lifecycle hooks |
| `.claude/commands/test-demo.md` | Test command with frontmatter hooks |
| `.claude/skills/test-demo-gen/SKILL.md` | Test skill with frontmatter hooks |
| `.claude/agents/test-demo-agent.md` | Test agent with instruction-based logging |
| `.claude/hooks/test_demo_hook.py` | Content generation hook |
| `_state/lifecycle.json` | Lifecycle event log |
| `_state/test-demo-outputs/` | Test output files |

---

## Related Documentation

- **Lifecycle Reference**: `architecture/Logging/claude-code-lifecycle-logging-reference.md`
- **Skills Reference**: `architecture/Skills_Reference.md`
- **Agent Architecture**: `architecture/Agent_Spawning_Architecture.md`
- **CLAUDE.md**: Main project documentation

---

## Summary

The v3.0 deterministic lifecycle logging architecture provides:

1. **Reliable end detection** via `Stop` and `SubagentStop` hooks
2. **Best-effort start detection** via `PreToolUse` (once:true) with instruction-based backup
3. **Global invocation detection** via settings-based `PreToolUse`/`PostToolUse` matchers
4. **Centralized logging** via `log-lifecycle.sh` helper
5. **NDJSON format** for easy parsing and streaming
6. **Separation of concerns** between component hooks and global hooks

This architecture should be used as the template for implementing lifecycle logging across all HTEC framework components.
