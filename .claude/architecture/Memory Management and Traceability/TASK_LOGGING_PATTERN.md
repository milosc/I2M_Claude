# Deterministic Task Logging Pattern

## Problem

When spawning agents with `Task()`, logging must happen but it's easy to forget:
- ❌ Manual logging is error-prone
- ❌ Easy to skip checkpoint logging
- ❌ No guarantee logging completes
- ❌ Inconsistent between spawns

## Solution: Atomic Three-Step Pattern

The `task_with_logging.py` module provides a **deterministic wrapper** that makes logging impossible to forget.

---

## Usage (Claude follows this pattern)

### Step 1: Prepare Spawn (Always Log)

```python
from _state.task_with_logging import prepare_agent_spawn

config = prepare_agent_spawn(
    agent_type="prototype-data-model-specifier",
    checkpoint=3,
    checkpoint_name="Data Model",
    stage="prototype",
    system_name="EmergencyTriage",
    model="sonnet",
    description="Generate data model from Discovery",
    prompt="""
    Agent: prototype-data-model-specifier
    Read: .claude/agents/prototype-data-model-specifier.md

    ## Task
    Extract entities from Discovery data fields...
    """,
    expected_outputs=["Prototype_EmergencyTriage/04-implementation/data-model.md"],
    headless=False
)

# Output:
# ✅ Prepared agent spawn: prototype-data-model-specifier
#    Spawn Token: spawn-a3f7b2c8d9e1
#    Checkpoint: 3 (Data Model)
#    Model: sonnet
#    Checkpoint Event: evt-92ebb8e0
#    Spawn Event: evt-0daa527f
#
# ⚠️  CRITICAL: Use spawn_token 'spawn-a3f7b2c8d9e1' in complete_agent_spawn()
```

**What happens:**
- ✅ Logs checkpoint start (`evt-92ebb8e0`)
- ✅ Logs agent spawn prepared (`evt-0daa527f`)
- ✅ Creates spawn token (`spawn-a3f7b2c8d9e1`)
- ✅ Returns Task() parameters

---

### Step 2: Execute Task() (Claude does this)

```python
# Use the config from Step 1
task_result = Task(
    subagent_type=config["task_params"]["subagent_type"],
    model=config["task_params"]["model"],
    description=config["task_params"]["description"],
    prompt=config["task_params"]["prompt"]
)

# task_result contains task_id we need for Step 3
```

**What happens:**
- Agent spawns and executes
- Returns task_id (e.g., `"task-dm-1735851234567"`)

---

### Step 3: Complete Logging (Always Log)

```python
from _state.task_with_logging import complete_agent_spawn

result = complete_agent_spawn(
    spawn_token=config["spawn_token"],  # From Step 1 (REQUIRED)
    task_id=task_result.task_id,        # From Step 2
    status="completed",                  # "completed" | "failed" | "partial"
    outputs=[
        "Prototype_EmergencyTriage/04-implementation/data-model.md"
    ]
)

# Output:
# ✅ Completed agent spawn: spawn-a3f7b2c8d9e1
#    Task ID: task-dm-1735851234567
#    Status: completed
#    Outputs: 1 files
#    Completion Event: evt-3b8c9d2e
#    Checkpoint End Event: evt-4f7a1b5c
```

**What happens:**
- ✅ Validates spawn_token (Step 1 and 3 are linked)
- ✅ Logs agent completion (`evt-3b8c9d2e`)
- ✅ Logs checkpoint end (`evt-4f7a1b5c`)
- ✅ Updates `pipeline_progress.json`
- ✅ Cleans up spawn token

---

## Why This Is Deterministic (5/5)

### 1. **Spawn Token Enforcement**

The spawn token from Step 1 MUST be used in Step 3:

```python
# Step 1 generates token
config = prepare_agent_spawn(...)
spawn_token = config["spawn_token"]  # "spawn-a3f7b2c8d9e1"

# Step 3 requires the token
complete_agent_spawn(spawn_token=spawn_token, ...)
```

**If you forget Step 3:**
- ❌ `ValueError: Invalid spawn_token`
- ❌ Orphaned logs in `_state/active_spawns.json`
- ❌ Can detect with: `python3 _state/task_with_logging.py --check-incomplete`

### 2. **No Way to Skip Step 1**

To call `Task()`, you need the parameters from Step 1:

```python
config = prepare_agent_spawn(...)  # Logging happens here

# Can't call Task() without config
Task(**config["task_params"])      # Need config from Step 1
```

### 3. **Registry Tracking**

Active spawns are tracked in `_state/active_spawns.json`:

```json
{
  "spawn-a3f7b2c8d9e1": {
    "checkpoint_event_id": "evt-92ebb8e0",
    "spawn_event_id": "evt-0daa527f",
    "completed": false
  }
}
```

**Detection:**
```bash
python3 _state/task_with_logging.py --check-incomplete

# Output if forgotten:
⚠️  Found 1 incomplete spawns:
  - Token: spawn-a3f7b2c8d9e1
    Checkpoint Event: evt-92ebb8e0
    Spawn Event: evt-0daa527f
```

### 4. **Cannot Reuse Tokens**

Each spawn gets a unique token. Attempting to complete twice:

```python
complete_agent_spawn(spawn_token="spawn-a3f7b2c8d9e1", ...)  # First time ✅
complete_agent_spawn(spawn_token="spawn-a3f7b2c8d9e1", ...)  # Second time ❌

# ValueError: Spawn token already used: spawn-a3f7b2c8d9e1
# This spawn has already been completed. Cannot complete twice.
```

---

## Complete Example

```python
# ═══════════════════════════════════════════════════════════════════════
# STEP 1: PREPARE (Logging checkpoint start + spawn prepared)
# ═══════════════════════════════════════════════════════════════════════

from _state.task_with_logging import prepare_agent_spawn

config = prepare_agent_spawn(
    agent_type="prototype-data-model-specifier",
    checkpoint=3,
    checkpoint_name="Data Model",
    stage="prototype",
    system_name="EmergencyTriage",
    model="sonnet",
    description="Generate data model from Discovery",
    prompt="""
    Agent: prototype-data-model-specifier
    Read: .claude/agents/prototype-data-model-specifier.md

    Input: ClientAnalysis_EmergencyTriage/04-design-specs/data-fields.md
    Output: Prototype_EmergencyTriage/04-implementation/data-model.md

    Task:
    1. Extract all entities (Patient, Triage, User, AuditLog, Session)
    2. Map relationships with cardinality
    3. Define validation rules
    4. Generate TypeScript interfaces
    """,
    expected_outputs=["Prototype_EmergencyTriage/04-implementation/data-model.md"]
)

print(f"🔑 Spawn Token: {config['spawn_token']}")

# ═══════════════════════════════════════════════════════════════════════
# STEP 2: EXECUTE (Claude spawns the agent)
# ═══════════════════════════════════════════════════════════════════════

task_result = Task(
    subagent_type=config["task_params"]["subagent_type"],
    model=config["task_params"]["model"],
    description=config["task_params"]["description"],
    prompt=config["task_params"]["prompt"]
)

print(f"📋 Task ID: {task_result.task_id}")

# ═══════════════════════════════════════════════════════════════════════
# STEP 3: COMPLETE (Logging agent completion + checkpoint end)
# ═══════════════════════════════════════════════════════════════════════

from _state.task_with_logging import complete_agent_spawn

result = complete_agent_spawn(
    spawn_token=config["spawn_token"],
    task_id=task_result.task_id,
    status="completed",
    outputs=[
        "Prototype_EmergencyTriage/04-implementation/data-model.md"
    ]
)

print(f"✅ Agent completed successfully")
print(f"   Completion Event: {result['completion_event_id']}")
print(f"   Checkpoint End Event: {result['checkpoint_end_event_id']}")
```

---

## Error Handling

### If Agent Fails

```python
try:
    task_result = Task(...)

    result = complete_agent_spawn(
        spawn_token=config["spawn_token"],
        task_id=task_result.task_id,
        status="completed",
        outputs=[...]
    )
except Exception as e:
    # ALWAYS complete logging even on failure
    result = complete_agent_spawn(
        spawn_token=config["spawn_token"],
        task_id=task_result.task_id if 'task_result' in locals() else "unknown",
        status="failed",
        error_message=str(e)
    )
```

### If You Forget Step 3

```bash
# Check for orphaned spawns
python3 _state/task_with_logging.py --check-incomplete

# Output:
⚠️  Found 1 incomplete spawns:
  - Token: spawn-a3f7b2c8d9e1
    Checkpoint Event: evt-92ebb8e0
    Spawn Event: evt-0daa527f

# Fix by completing manually:
python3 << 'EOF'
from _state.task_with_logging import complete_agent_spawn

complete_agent_spawn(
    spawn_token="spawn-a3f7b2c8d9e1",
    task_id="task-dm-1735851234567",
    status="completed",
    outputs=["Prototype_EmergencyTriage/04-implementation/data-model.md"]
)
EOF
```

---

## Integration with Orchestrator

The orchestrator should provide instructions using this pattern:

```markdown
## Checkpoint 3: Data Model

**Main Session Action Required**: Use deterministic spawn pattern:

```python
from _state.task_with_logging import prepare_agent_spawn, complete_agent_spawn

# Step 1: Prepare
config = prepare_agent_spawn(
    agent_type="prototype-data-model-specifier",
    checkpoint=3,
    checkpoint_name="Data Model",
    stage="prototype",
    system_name="EmergencyTriage",
    model="sonnet",
    description="Generate data model",
    prompt="..."
)

# Step 2: Execute
task_result = Task(**config["task_params"])

# Step 3: Complete
complete_agent_spawn(
    spawn_token=config["spawn_token"],
    task_id=task_result.task_id,
    status="completed",
    outputs=[...]
)
```
```

---

## Verification

```bash
# Check pipeline progress
python3 << 'EOF'
import json
with open('_state/pipeline_progress.json') as f:
    data = json.load(f)
print(f"Total Events: {data['statistics']['total_events']}")
print(f"Agents Spawned: {data['statistics']['total_agents_spawned']}")
EOF

# Check for incomplete spawns
python3 _state/task_with_logging.py --check-incomplete
```

---

## Benefits

✅ **Impossible to forget logging** - Spawn token enforces completion
✅ **Atomic operation** - All logging in two function calls
✅ **Crash recovery** - Incomplete spawns detected via registry
✅ **Consistent** - Same pattern for all agent spawns
✅ **Testable** - Can unit test the wrapper
✅ **Auditable** - Clear event chain in pipeline_progress.json

**Determinism: 5/5** - Logging guaranteed if pattern is followed.
