# Frontmatter Hooks Examples

**Version**: 1.0.0
**Date**: 2026-01-26
**Purpose**: Real-world examples of deployed frontmatter hooks across agent and skill categories

---

## Agent Hook Examples

### 1. Orchestrator Agent (`discovery-orchestrator`)

**Location**: `.claude/agents/discovery-orchestrator.md`

**Hook Pattern**:
```yaml
---
name: discovery-orchestrator
description: Master coordination guide for Discovery analysis (Stage 1)
model: sonnet
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Purpose**:
- **PreToolUse(Task)** - Log each agent spawn with parent context
- **PostToolUse(Task)** - Link agent completion back to spawn
- **Stop** - Mark orchestrator completion

**Logs**:
- Agent spawn events (which agents are being spawned)
- Agent completion events (when spawned agents finish)
- Orchestrator completion (when coordination finishes)

---

### 2. Implementation Agent (`implementation-developer`)

**Location**: `.claude/agents/implementation-developer.md`

**Hook Pattern**:
```yaml
---
name: implementation-developer
description: TDD implementation with RED-GREEN-REFACTOR cycle
model: sonnet
hooks:
  PreToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/file_lock_acquire.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
    - matcher: "Bash"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/tdd_compliance_check.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/file_lock_release.py"
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
    - matcher: "Bash"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Purpose**:
- **PreToolUse(Write|Edit)** - Acquire file lock, prevent concurrent modifications
- **PostToolUse(Write|Edit)** - Validate TDD compliance, release lock, log event
- **PreToolUse(Bash)** / **PostToolUse(Bash)** - Track test execution
- **Stop** - Mark implementation completion

**Special Features**:
- **File Locking** - Prevents multiple agents from modifying the same file
- **TDD Compliance Check** - Warns if writing tests in non-RED phase or implementation in non-GREEN phase

---

### 3. Analyst Agent (`discovery-interview-analyst`)

**Location**: `.claude/agents/discovery-interview-analyst.md`

**Hook Pattern**:
```yaml
---
name: discovery-interview-analyst
description: Extract pain points, workflows, quotes, and user needs from interview transcripts
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Purpose**:
- **PostToolUse(Write|Edit)** - Log output file creation
- **Stop** - Mark analysis completion
- **No PreToolUse** - Input files are parameters, not tool calls

---

### 4. Validator Agent (`discovery-cross-reference-validator`)

**Location**: `.claude/agents/discovery-cross-reference-validator.md`

**Hook Pattern**:
```yaml
---
name: discovery-cross-reference-validator
description: Validate bidirectional links between Discovery artifacts
model: haiku
hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Purpose**:
- **PreToolUse(Read)** - Track which artifacts being validated
- **PostToolUse(Write)** - Log validation report generation
- **Stop** - Mark validation completion
- **Uses Haiku** - Cost-efficient for checklist-based validation

---

### 5. Generator Agent (`discovery-persona-generator`)

**Location**: `.claude/agents/discovery-persona-generator.md`

**Hook Pattern**:
```yaml
---
name: discovery-persona-generator
description: Generate persona document from research data
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Purpose**:
- **PostToolUse(Write|Edit)** - Log artifact creation
- **Stop** - Mark generation completion
- **No PreToolUse** - Specifications provided as parameters

---

### 6. Process Integrity Agent (`process-integrity-traceability-guardian`)

**Location**: `.claude/agents/process-integrity-traceability-guardian.md`

**Hook Pattern**:
```yaml
---
name: process-integrity-traceability-guardian
description: Validate traceability chains and ID integrity
model: haiku
hooks:
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Purpose**:
- **PreToolUse(Read)** - Track registry files being checked
- **PostToolUse(Write)** - Log integrity violations
- **Stop** - Mark integrity check completion
- **Uses Haiku** - Cost-efficient for checklist-based validation

---

## Skill Hook Examples

### 1. Orchestration Skill (`/discovery`)

**Location**: `.claude/commands/discovery.md` (skill file)

**Hook Pattern**:
```yaml
---
name: discovery
description: Complete Discovery orchestration with checkpoint-by-checkpoint execution
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
      once: true  # Only log the FIRST agent spawn (workflow start)
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Purpose**:
- **PreToolUse(Task) + once:true** - Log workflow start (only first spawn)
- **PostToolUse(Task)** - Log agent completions (all spawns)
- **Stop** - Mark command completion

**Special Feature**:
- **once: true** - Only runs the PreToolUse hook ONCE per session (for workflow start logging)

---

### 2. Multi-Agent Parallel Skill (`/discovery-multiagent`)

**Location**: `.claude/commands/discovery-multiagent.md`

**Hook Pattern**:
```yaml
---
name: discovery-multiagent
description: Massively parallel Discovery with 60-70% speedup
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Purpose**:
- **PreToolUse(Task)** - Log ALL parallel spawns (no `once: true`)
- **PostToolUse(Task)** - Log ALL parallel completions
- **Stop** - Mark command completion

**Special Feature**:
- **No once:true** - Logs every agent spawn (important for tracking parallel execution)

---

### 3. Audit/Validation Skill (`/discovery-audit`)

**Location**: `.claude/commands/discovery-audit.md`

**Hook Pattern**:
```yaml
---
name: discovery-audit
description: Zero Hallucination Audit - verify all facts are cited
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
      once: true  # Log audit start
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Purpose**:
- **PreToolUse(Task) + once:true** - Log audit start
- **Stop** - Mark audit completion

---

### 4. Feedback Processing Skill (`/prototype-feedback`)

**Location**: `.claude/commands/prototype-feedback.md`

**Hook Pattern**:
```yaml
---
name: prototype-feedback
description: Process prototype feedback with Reflexion loop
hooks:
  PreToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse"
  PostToolUse:
    - matcher: "Task"
      hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse"
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Purpose**:
- **PreToolUse(Task)** - Log feedback analyzer spawn
- **PostToolUse(Task)** - Log implementation completion
- **Stop** - Mark feedback processing completion

---

### 5. Utility Skill (`/discovery-status`)

**Location**: `.claude/commands/discovery-status.md`

**Hook Pattern**:
```yaml
---
name: discovery-status
description: Show Discovery progress across all checkpoints
hooks:
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---
```

**Purpose**:
- **Stop only** - Read-only operations, no spawns
- Track utility invocations

---

## Hook Scripts Reference

### 1. capture_event.py (Universal Event Capture)

**Location**: `.claude/hooks/capture_event.py`

**Purpose**: Universal event capture for all agents and skills

**Usage**:
```bash
uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PreToolUse
uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type PostToolUse
uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop
```

**Logs to**: `_state/lifecycle.json`

---

### 2. file_lock_acquire.py (File Locking)

**Location**: `.claude/hooks/file_lock_acquire.py`

**Purpose**: Acquire file-level locks to prevent concurrent modifications

**Usage**: Called automatically via PreToolUse(Write|Edit) hook in implementation agents

**Behavior**:
- Checks existing locks in `_state/agent_lock.json`
- Blocks if file is locked by another agent (exit 1)
- Acquires lock with 15-minute expiration
- Stores lock entry with session ID and file path

---

### 3. file_lock_release.py (Lock Release)

**Location**: `.claude/hooks/file_lock_release.py`

**Purpose**: Release file-level locks acquired by current agent session

**Usage**: Called automatically via PostToolUse(Write|Edit) hook in implementation agents

**Behavior**:
- Reads `_state/agent_lock.json`
- Removes locks for current session
- Writes updated lock registry

---

### 4. tdd_compliance_check.py (TDD Phase Validation)

**Location**: `.claude/hooks/tdd_compliance_check.py`

**Purpose**: Validate TDD phase compliance (RED → GREEN → REFACTOR)

**Usage**: Called automatically via PostToolUse(Write|Edit) hook in implementation agents

**Behavior**:
- Reads `_state/tdd_state.json` for current TDD phase
- Checks if test file or implementation file
- Warns if writing tests in non-RED phase
- Warns if writing implementation in non-GREEN phase
- Always exits 0 (never blocks)

---

## Call Stack Flow Example

**Command**: `/discovery InventorySystem Client_Materials/`

**Event Flow**:
```
1. UserPromptSubmit (global hook)
   → CAPTURED: user_prompt:prompt:submitted

2. PreToolUse(Skill) (global hook)
   → CAPTURED: skill:discovery:pre_invoke

3. PreToolUse(Task) (discovery skill hook + once:true)
   → CAPTURED: agent:discovery-orchestrator:pre_spawn

4. SessionStart (subagent hook)
   → CAPTURED: session:subagent:started (discovery-orchestrator)

5. PreToolUse(Task) (orchestrator agent hook)
   → CAPTURED: agent:discovery-interview-analyst:pre_spawn

6. PostToolUse(Write) (analyst agent hook)
   → CAPTURED: file:write (ANALYSIS_SUMMARY.md)

7. Stop (analyst agent hook)
   → CAPTURED: agent:discovery-interview-analyst:stopped

8. PostToolUse(Task) (orchestrator hook)
   → CAPTURED: agent:discovery-interview-analyst:post_spawn

9. Stop (orchestrator hook)
   → CAPTURED: agent:discovery-orchestrator:stopped

10. PostToolUse(Skill) (global hook)
    → CAPTURED: skill:discovery:post_invoke

11. Stop (skill hook)
    → CAPTURED: skill:discovery:stopped
```

**Result**: Complete traceability from command → skill → agents → files

---

## Verification Commands

### Check Hook Coverage
```bash
# Count agents with hooks
grep -l "^hooks:" .claude/agents/*.md | wc -l

# Count skills with hooks
find .claude/skills -name "SKILL.md" -exec grep -l "^hooks:" {} \; | wc -l

# Verify hook scripts exist
ls -l .claude/hooks/*.py | grep -E "(capture_event|file_lock|tdd_compliance)"
```

### View Sample Hooks
```bash
# View orchestrator hooks
head -25 .claude/agents/discovery-orchestrator.md

# View implementation hooks
head -45 .claude/agents/implementation-developer.md

# View skill hooks
head -25 .claude/commands/discovery.md
```

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-26 | Initial hook examples documentation |
