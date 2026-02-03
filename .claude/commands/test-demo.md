---
name: test-demo
description: Framework lifecycle logging demonstration using deterministic hooks
argument-hint: [--mode command|skill|agent|all]
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Bash, Task, Skill
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

# /test-demo - Deterministic Lifecycle Logging Demonstration

This command demonstrates the **deterministic lifecycle logging architecture** for the HTEC framework.

## Logging Architecture (v2.0)

**DETERMINISTIC IMPLEMENTATION:**
- **Session Management**: `session-init.sh` creates `_state/session.json` on startup
- **Session Context**: `session-update.sh` sets project/stage context
- **Command START**: Logged via `PreToolUse` hook with `once: true` (fires on first tool use)
- **Command END**: Logged via `Stop` frontmatter hook (reliable)
- **Skill invocation**: Logged via global `settings.json` hooks with `--from-input` name extraction
- **Agent spawning**: Logged via global `settings.json` hooks with `--from-input` name extraction
- **Subagent completion**: Logged via global `SubagentStop` hook

All events are written to `_state/lifecycle.json` using the centralized `log-lifecycle.sh` helper.

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /test-demo instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## Execution

### Step 1: Initialize Test Environment

```bash
echo ""
echo "============================================================"
echo " /test-demo - Deterministic Lifecycle Logging Test (v2.0)"
echo "============================================================"
echo ""

# Create output directory
mkdir -p _state/test-demo-outputs

# Clear previous test outputs
rm -f _state/test-demo-outputs/*.md 2>/dev/null || true

# Ensure lifecycle log exists
touch _state/lifecycle.json

# Store line count before test to analyze only new entries
LIFECYCLE_START_LINE=$(wc -l < _state/lifecycle.json)
echo "LIFECYCLE_START_LINE=$LIFECYCLE_START_LINE" > _state/test-demo-outputs/test-markers.txt

echo "Test environment initialized"
echo "Output directory: _state/test-demo-outputs/"
echo "Lifecycle log: _state/lifecycle.json"
echo "Starting from line: $LIFECYCLE_START_LINE"
echo ""
```

### Step 2: Test Command -> Hook (Direct Call)

This demonstrates a **Command** directly calling a hook.

```bash
echo ""
echo "============================================================"
echo " TEST 1: COMMAND -> HOOK (Direct)"
echo "============================================================"
echo ""

# Command directly invokes the hook
python3 .claude/hooks/test_demo_hook.py \
  --output "_state/test-demo-outputs/command-output.md" \
  --paragraphs 3 \
  --title "Command Generated Content" \
  --source "/test-demo (command)"

if [ -f "_state/test-demo-outputs/command-output.md" ]; then
  echo "TEST 1 PASSED: Command -> Hook"
  echo "Output: _state/test-demo-outputs/command-output.md"
else
  echo "TEST 1 FAILED: Output file not created"
fi
```

### Step 3: Test Skill Invocation (Via Skill Tool)

This demonstrates invoking a **Skill** using the Skill tool.

**Expected Logging (with --from-input):**
- Global `PreToolUse` hook fires with `matcher: "Skill"` -> logs `skill:test-demo-gen:pre_invoke`
- Skill's own `PreToolUse` hook fires with `once: true` -> logs `skill:test-demo-gen:started`
- Skill executes
- Skill's `Stop` hook fires -> logs `skill:test-demo-gen:ended`
- Global `PostToolUse` hook fires with `matcher: "Skill"` -> logs `skill:test-demo-gen:post_invoke`

Use the Skill tool to invoke the test-demo-gen skill:

```javascript
Skill({
  skill: "test-demo-gen",
  args: "--output _state/test-demo-outputs/skill-output.md --paragraphs 4"
})
```

After calling Skill(), verify the output:

```bash
if [ -f "_state/test-demo-outputs/skill-output.md" ]; then
  echo "TEST 2 PASSED: Skill Invocation"
  echo "Output: _state/test-demo-outputs/skill-output.md"
else
  echo "TEST 2 FAILED: Output file not created"
fi
```

### Step 4: Test Agent Spawning (Via Task Tool)

This demonstrates spawning an **Agent** using the Task tool.

**Expected Logging (with --from-input):**
- Global `PreToolUse` hook fires with `matcher: "Task"` -> logs `agent:test-demo-agent:pre_spawn`
- Subagent's instruction-based logging -> logs `subagent:test-demo-agent:started`
- Subagent executes
- Subagent's completion logging -> logs `subagent:test-demo-agent:completed`
- Global `SubagentStop` hook fires -> logs `subagent:test-demo-agent:stopped` (with --from-input)
- Global `PostToolUse` hook fires -> logs `agent:test-demo-agent:post_spawn`

Use the Task tool to spawn the test-demo-agent:

```javascript
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Generate test file via agent",
  prompt: `Agent: test-demo-agent
    Read: .claude/agents/test-demo-agent.md

    TASK: Generate Lorem Ipsum test file
    OUTPUT: _state/test-demo-outputs/agent-output.md
    PARAGRAPHS: 3
    TITLE: "Agent Generated Content"

    Execute the agent logic as defined in the agent file.

    RETURN: JSON { status, output_file }`
})
```

After calling Task(), verify the output:

```bash
if [ -f "_state/test-demo-outputs/agent-output.md" ]; then
  echo "TEST 3 PASSED: Agent Spawning"
  echo "Output: _state/test-demo-outputs/agent-output.md"
else
  echo "TEST 3 FAILED: Output file not created"
fi
```

### Step 5: Summary Report

```bash
echo ""
echo "============================================================"
echo " TEST SUMMARY"
echo "============================================================"
echo ""

# Count successful outputs
TOTAL=0
PASSED=0

for file in command skill agent; do
  TOTAL=$((TOTAL + 1))
  if [ -f "_state/test-demo-outputs/${file}-output.md" ]; then
    PASSED=$((PASSED + 1))
    SIZE=$(wc -c < "_state/test-demo-outputs/${file}-output.md")
    echo "PASS: ${file}-output.md ($SIZE bytes)"
  else
    echo "FAIL: ${file}-output.md (missing)"
  fi
done

echo ""
echo "Results: $PASSED/$TOTAL tests passed"
echo ""

# Show all outputs
echo "Generated files:"
ls -la _state/test-demo-outputs/ 2>/dev/null || echo "No outputs directory"
```

### Step 6: Lifecycle Log Analysis

```bash
echo ""
echo "============================================================"
echo " LIFECYCLE LOG ANALYSIS"
echo "============================================================"
echo ""

if [ -f "_state/lifecycle.json" ]; then
  echo "Recent lifecycle events:"
  echo ""
  tail -20 _state/lifecycle.json | while read line; do
    echo "  $line"
  done
  echo ""

  # Count events by type
  echo "Event counts:"
  echo "  command events: $(grep -c '"component":"command"' _state/lifecycle.json 2>/dev/null || echo 0)"
  echo "  skill events: $(grep -c '"component":"skill"' _state/lifecycle.json 2>/dev/null || echo 0)"
  echo "  agent events: $(grep -c '"component":"agent"' _state/lifecycle.json 2>/dev/null || echo 0)"
  echo "  subagent events: $(grep -c '"component":"subagent"' _state/lifecycle.json 2>/dev/null || echo 0)"
  echo "  session events: $(grep -c '"component":"session"' _state/lifecycle.json 2>/dev/null || echo 0)"
else
  echo "FAIL: _state/lifecycle.json not found"
fi
```

### Step 7: Telemetry Improvement Validation (v2.0 NEW)

This step validates the telemetry improvements are working correctly.

```bash
echo ""
echo "============================================================"
echo " TELEMETRY IMPROVEMENT VALIDATION (v2.0)"
echo "============================================================"
echo ""

# Read start line
if [ -f "_state/test-demo-outputs/test-markers.txt" ]; then
  source _state/test-demo-outputs/test-markers.txt
else
  LIFECYCLE_START_LINE=0
fi

# Get only new entries from this test run
NEW_ENTRIES=$(tail -n +$((LIFECYCLE_START_LINE + 1)) _state/lifecycle.json 2>/dev/null || cat _state/lifecycle.json)

# Count issues
UNKNOWN_NAME=$(echo "$NEW_ENTRIES" | grep -c '"name":"unknown"' || echo 0)
UNKNOWN_SESSION=$(echo "$NEW_ENTRIES" | grep -c '"session":"unknown"' || echo 0)
UNKNOWN_PROJECT=$(echo "$NEW_ENTRIES" | grep -c '"project":"unknown"' || echo 0)
TASK_SPAWN=$(echo "$NEW_ENTRIES" | grep -c '"name":"task-spawn"' || echo 0)
SKILL_INVOKE=$(echo "$NEW_ENTRIES" | grep -c '"name":"skill-invoke"' || echo 0)

# Validation results
echo "Checking for 'unknown' entries in new lifecycle events:"
echo ""
echo "  name='unknown' entries: $UNKNOWN_NAME"
echo "  session='unknown' entries: $UNKNOWN_SESSION"
echo "  project='unknown' entries: $UNKNOWN_PROJECT"
echo "  name='task-spawn' entries: $TASK_SPAWN"
echo "  name='skill-invoke' entries: $SKILL_INVOKE"
echo ""

# Check session.json
echo "Checking session.json:"
if [ -f "_state/session.json" ]; then
  echo "  session.json EXISTS"
  SESSION_PROJECT=$(jq -r '.project // "MISSING"' _state/session.json)
  SESSION_STAGE=$(jq -r '.stage // "MISSING"' _state/session.json)
  SESSION_ID=$(jq -r '.session_id // "MISSING"' _state/session.json)
  echo "  project: $SESSION_PROJECT"
  echo "  stage: $SESSION_STAGE"
  echo "  session_id: $SESSION_ID"
else
  echo "  session.json MISSING"
fi
echo ""

# Summary
ISSUES=$((UNKNOWN_NAME + TASK_SPAWN + SKILL_INVOKE))
if [ $ISSUES -eq 0 ]; then
  echo "TELEMETRY VALIDATION: PASS"
  echo "  All entries have proper names (no 'unknown', 'task-spawn', 'skill-invoke')"
else
  echo "TELEMETRY VALIDATION: ISSUES FOUND"
  echo "  $ISSUES entries still need naming improvements"
  echo ""
  echo "  Note: Some 'unknown' entries may be expected if CLAUDE_TOOL_INPUT"
  echo "  is not available in certain hook contexts (e.g., SubagentStop)."
fi
```

### Step 8: Validation Checklist

```bash
echo ""
echo "============================================================"
echo " VALIDATION CHECKLIST"
echo "============================================================"
echo ""

echo "1. Session Management (NEW in v2.0):"
echo "   - [ ] session.json exists with session_id"
echo "   - [ ] session.json has project='TestDemo'"
echo "   - [ ] session.json has stage='utility'"
echo ""
echo "2. Command lifecycle:"
echo "   - [ ] PreToolUse (once:true) logged 'command:/test-demo:started'"
echo "   - [ ] Stop hook will log 'command:/test-demo:ended'"
echo ""
echo "3. Skill lifecycle (via global settings.json hooks with --from-input):"
echo "   - [ ] PreToolUse (matcher:Skill) logged 'skill:test-demo-gen:pre_invoke'"
echo "   - [ ] Skill's own PreToolUse logged 'skill:test-demo-gen:started'"
echo "   - [ ] Skill's Stop logged 'skill:test-demo-gen:ended'"
echo "   - [ ] PostToolUse (matcher:Skill) logged 'skill:test-demo-gen:post_invoke'"
echo ""
echo "4. Agent lifecycle (via global settings.json hooks with --from-input):"
echo "   - [ ] PreToolUse (matcher:Task) logged 'agent:test-demo-agent:pre_spawn'"
echo "   - [ ] Subagent instruction logged 'subagent:test-demo-agent:started'"
echo "   - [ ] Subagent completion logged 'subagent:test-demo-agent:completed'"
echo "   - [ ] SubagentStop logged 'subagent:test-demo-agent:stopped'"
echo "   - [ ] PostToolUse (matcher:Task) logged 'agent:test-demo-agent:post_spawn'"
echo ""
echo "Check _state/lifecycle.json to verify each event was logged."
```

---

## Logging Hook Summary (v2.0)

| Component | Start Hook | End Hook | Name Source | Deterministic |
|-----------|-----------|----------|-------------|---------------|
| Session | SessionStart | - | CLAUDE_SESSION_ID | Yes |
| Command | PreToolUse (once:true) | Stop | Hardcoded | Partial/Yes |
| Skill | Global PreToolUse | Global PostToolUse | --from-input (.skill) | Yes |
| Agent | Global PreToolUse | Global PostToolUse | --from-input (prompt) | Yes |
| Subagent | Instruction-based | SubagentStop | Instruction-based / --from-input | Partial |

## Related

- **Session hooks**: `.claude/hooks/session-init.sh`, `.claude/hooks/session-update.sh`
- **Helper script**: `.claude/hooks/log-lifecycle.sh`
- **Global hooks**: `.claude/settings.json`
- **Skill**: `.claude/skills/test-demo-gen/SKILL.md`
- **Agent**: `.claude/agents/test-demo-agent.md`
- **Documentation**: `architecture/Framework_Test_Demo.md`
- **Improvement Plan**: `architecture/TelemetryImprovementPlan.md`
