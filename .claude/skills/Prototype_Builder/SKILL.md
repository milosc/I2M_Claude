---
name: prototype-builder
description: Use when you need to coordinate the full prototype generation pipeline, managing dependencies between skills and implementation batches.
model: sonnet
allowed-tools: Read, Write, Edit, Bash, Task
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill prototype-builder started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill prototype-builder ended '{"stage": "prototype"}'
---

# Prototype Builder

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill prototype-builder instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_Builder
- **Version**: 3.0.0
- **Created**: 2024-12-13
- **Updated**: 2025-12-27
- **Author**: Milos Cigoj
- **Change History**:
  - v3.0.0 (2025-12-27): **MAJOR** - Added parallel agent execution support with 10 specialized Prototype agents (5 specifiers + 5 validators). Expected 60% speedup.
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md.
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3.

Coordinate execution of all Prototype_* skills in correct order. Enforces validation at each step, tracks requirements progress, blocks on P0 coverage failures, and logs all prompts.

> **PHASE 3 ENHANCEMENT**: Supports batch execution mode for task plans with architect review checkpoints.
> **v3.0 ENHANCEMENT**: Supports parallel agent execution for 60% faster prototype generation.

## Execution Modes

### Standard Mode (Default)
Run full skill pipeline in sequence with validation at each step.

### Batch Execution Mode (Phase 3)
Execute implementation task plans in controlled batches with review checkpoints.

```
INVOKE Prototype_Builder:
  MODE: batch_execution
  PLAN: "04-implementation/plans/{phase-name}-tasks.md"
  BATCH_SIZE: 3  // Default: first 3 tasks per batch
```

### Parallel Agent Mode (v3.0)
Execute specification and validation tasks using parallel agents for up to 60% faster completion.

```
INVOKE Prototype_Builder:
  MODE: parallel
  DISCOVERY_PATH: "ClientAnalysis_{SystemName}/"
  OUTPUT_PATH: "Prototype_{SystemName}/"
```

---

## ⚠️ CRITICAL: Active Prompt Logging Behavior

**This is NOT optional. Claude MUST actively perform these file operations.**

The prompt logging instructions in skills are NOT pseudocode - they are actual file operations that Claude must execute. When Claude sees instructions like:

```
READ _state/prompt_log.json AS log
APPEND entry TO log.entries
WRITE log TO _state/prompt_log.json
```

Claude MUST actually:
1. Use the file read tool to read `_state/prompt_log.json`
2. Parse the JSON content
3. Modify the data structure as instructed
4. Use the file write tool to write the updated JSON back

### When to Log

**BEFORE generating significant content** (component specs, screen specs, schemas, etc.):
1. READ `_state/prompt_log.json`
2. Calculate next ID: `"PL-" + (summary.total_entries + 1).toString().padStart(3, '0')`
3. CREATE entry with: id, session_id, timestamp, skill, step, category, desired_outcome, inputs, target, result.status="pending"
4. APPEND entry to entries array
5. INCREMENT summary.total_entries and category counts
6. WRITE updated log to `_state/prompt_log.json`

**AFTER generation completes**:
1. READ `_state/prompt_log.json`
2. FIND the entry by id
3. UPDATE entry.result with: status="success"|"error", output_summary
4. INCREMENT summary.by_status counts
5. WRITE updated log to `_state/prompt_log.json`

### Minimum Logging Granularity

At minimum, Claude MUST log:
- One entry per component spec generated
- One entry per screen spec generated  
- One entry per schema file generated
- One entry for summary/index files
- One entry for validation steps

### Verification

After each skill completes, Claude should verify:
- `_state/prompt_log.json` has new entries
- Entry count increased
- Current session shows the skill in `skills_executed`

**If the prompt_log.json is empty or unchanged after running skills, Claude is NOT following these instructions correctly.**

---

## Procedure

### Step 1: Initialize Pipeline (REQUIRED)
```
CHECK _state/ directory exists, create if not

// ========== INITIALIZE PROMPT LOG ==========
READ _state/prompt_log.json AS log

IF file not exists OR log is null:
  // Create fresh prompt log structure
  log = {
    "version": "1.0",
    "created_at": NOW_ISO(),
    "sessions": [],
    "entries": [],
    "summary": {
      "total_entries": 0,
      "by_skill": {},
      "by_category": {},
      "by_status": {}
    }
  }

// Calculate next session ID
next_session_num = log.sessions.length + 1
session_id = "sess-" + String(next_session_num).padStart(3, '0')

// Create new session entry
new_session = {
  "session_id": session_id,
  "started_at": NOW_ISO(),
  "ended_at": null,
  "skills_executed": [],
  "entry_count": 0,
  "success_count": 0,
  "error_count": 0
}

// Append session to sessions array
APPEND new_session TO log.sessions

// WRITE the updated log to file
WRITE log TO _state/prompt_log.json

// Store session ID globally for all skills to reference
SET GLOBAL current_session_id = session_id

LOG: "✅ Prompt logging initialized for session {session_id}"
// ============================================

CHECK progress.json exists:
  IF exists:
    LOAD and determine resume point
    VALIDATE schema_version
    
    IF schema_version < CURRENT_VERSION:
      ═══════════════════════════════════════════
      ⚠️ VERSION MISMATCH
      ═══════════════════════════════════════════
      
      State files are from older version: {schema_version}
      Current version: {CURRENT_VERSION}
      
      How would you like to proceed?
      1. "migrate" - Run migration first
      2. "continue" - Proceed anyway (may fail)
      3. "reset" - Start fresh (loses progress)
      ═══════════════════════════════════════════
      
      WAIT for user response
      
  IF not exists:
    CREATE with schema_version: "2.3"
    
INITIALIZE requirements_progress tracking:
  {
    "p0_total": 0,
    "p0_addressed": 0,
    "p0_coverage": "0%"
  }
```

### Step 2: Load Skill Registry and Define Execution Order
```
// ═══════════════════════════════════════════════════════════
// DYNAMIC SKILL INVOCATION (Phase 5 Enhancement)
// ═══════════════════════════════════════════════════════════

// Load skill registry
READ .claude/skills/Prototype_Builder/PROTOTYPE_SKILL_REGISTRY.json AS registry

IF registry not exists:
  LOG: "⚠️ Skill registry not found, using hardcoded order"
  USE_HARDCODED_ORDER = true

// Build execution order from registry (sorted by phase)
IF registry exists:
  STANDARD_ORDER = []

  // Get all prototype-* skills, sorted by phase
  prototype_skills = registry.skills
    .filter(s => s.id.startsWith("prototype-"))
    .filter(s => s.id != "prototype-builder")  // Exclude self
    .sort((a, b) => registry.phases[a.phase] - registry.phases[b.phase])

  FOR each skill in prototype_skills:
    STANDARD_ORDER.push({
      id: skill.id,
      folder: skill.folder,
      file: skill.file,
      phase: skill.phase,
      can_invoke: skill.can_invoke,
      inputs: skill.inputs,
      outputs: skill.outputs
    })

  LOG: "✅ Loaded {STANDARD_ORDER.length} skills from registry"

ELSE:
  // Fallback hardcoded order
  STANDARD_ORDER = [
    { id: "prototype-validate-discovery", folder: "Prototype_ValidateDiscovery" },
    { id: "prototype-requirements", folder: "Prototype_Requirements" },
    { id: "prototype-data-model", folder: "Prototype_DataModel" },
    { id: "prototype-api-contracts", folder: "Prototype_ApiContracts" },
    { id: "prototype-test-data", folder: "Prototype_TestData" },
    { id: "prototype-design-brief", folder: "Prototype_DesignBrief" },
    { id: "prototype-design-tokens", folder: "Prototype_DesignTokens" },
    { id: "prototype-components", folder: "Prototype_Components" },
    { id: "prototype-screens", folder: "Prototype_Screens" },
    { id: "prototype-interactions", folder: "Prototype_Interactions" },
    { id: "prototype-sequencer", folder: "Prototype_Sequencer" },
    { id: "prototype-prompts", folder: "Prototype_Prompts" },
    { id: "prototype-codegen", folder: "Prototype_CodeGen" },
    { id: "prototype-qa", folder: "Prototype_QA" },
    { id: "prototype-ui-audit", folder: "Prototype_UIAudit" }
  ]
```

### Step 2.5: Define Skill Invocation Helper
```
// ═══════════════════════════════════════════════════════════
// SKILL INVOCATION MECHANISM
// See: SKILL_INVOCATION.md for full documentation
// ═══════════════════════════════════════════════════════════

DEFINE INVOKE_SKILL(skill_id, inputs, options):
  """
  Dynamically invoke a skill by its registry ID.

  Parameters:
    skill_id: string - The skill ID from SKILL_REGISTRY.json
    inputs: object - Input parameters for the skill
    options: object - Invocation options (mode, on_failure, etc.)

  Returns:
    result: object - { success: boolean, outputs: [], error?: string }
  """

  // Step 1: Look up skill in registry
  skill_config = registry.skills[skill_id]

  IF skill_config not exists:
    LOG: "❌ Skill not found in registry: {skill_id}"
    RETURN { success: false, error: "Skill not found" }

  // Step 2: Verify required inputs
  FOR each required_input in skill_config.inputs.required:
    IF required_input not in inputs:
      IF options.on_failure == "BLOCK":
        BLOCK: "Missing required input: {required_input}"
      ELSE:
        LOG: "⚠️ Missing required input: {required_input}"
        RETURN { success: false, error: "Missing input: {required_input}" }

  // Step 3: Check if skill can be invoked by current skill
  IF current_skill not in skill_config.invoked_by AND "*" not in skill_config.invoked_by:
    LOG: "⚠️ {current_skill} is not authorized to invoke {skill_id}"
    // Allow but log warning

  // Step 4: Log invocation start
  LOG_SKILL_INVOCATION:
    invoking_skill: current_skill
    invoked_skill: skill_id
    inputs: inputs
    timestamp: NOW()
    status: "started"

  // Step 5: Invoke the skill
  TRY:
    // Use Claude Code's Skill tool to invoke
    IF skill_config.category == "3rdparty":
      // 3rdParty skills use Skill tool directly
      USE_TOOL Skill:
        skill: skill_config.folder

      skill_output = SKILL_OUTPUT

    ELSE:
      // Prototype skills - read and execute SKILL.md
      skill_path = ".claude/skills/{skill_config.folder}/{skill_config.file}"
      READ skill_path AS skill_definition

      // Execute skill procedure with inputs
      EXECUTE skill_definition WITH inputs

      skill_output = EXECUTION_RESULT

    // Step 6: Verify outputs
    FOR each expected_output in skill_config.outputs:
      IF not FILE_EXISTS(expected_output):
        LOG: "⚠️ Expected output not found: {expected_output}"

    // Step 7: Log invocation success
    LOG_SKILL_INVOCATION:
      invoked_skill: skill_id
      status: "success"
      outputs: skill_output.files

    RETURN { success: true, outputs: skill_output }

  CATCH error:
    // Step 8: Handle failure
    LOG_SKILL_INVOCATION:
      invoked_skill: skill_id
      status: "error"
      error: error.message

    IF options.on_failure == "BLOCK":
      BLOCK: error.message
    ELSE IF options.on_failure == "WARN":
      LOG: "⚠️ Skill failed: {skill_id} - {error.message}"

    RETURN { success: false, error: error.message }
```

### Step 3: Check Prerequisites for Each Skill
```
FOR each skill in order:
  CHECK dependencies complete:
    FOR each dependency:
      IF phases[dependency].status != "complete":
        CANNOT run this skill
        
        ═══════════════════════════════════════════
        ⚠️ DEPENDENCY NOT MET
        ═══════════════════════════════════════════
        
        Cannot run: {skill}
        Missing dependency: {dependency}
        
        How would you like to proceed?
        1. "run: {dependency}" - Run dependency first
        2. "skip to: {skill}" - Force skip (may fail)
        3. "abort" - Stop pipeline
        ═══════════════════════════════════════════
        
        WAIT for user response
```

### Step 4: Execute Skills with Dynamic Invocation
```
// ═══════════════════════════════════════════════════════════
// DYNAMIC SKILL EXECUTION
// ═══════════════════════════════════════════════════════════

FOR each skill in execution_order:
  LOG: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  LOG: "Starting: {skill.folder} (ID: {skill.id})"
  LOG: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  // Update session with skill being executed
  READ _state/prompt_log.json AS log
  current_session = log.sessions[log.sessions.length - 1]
  IF skill.id NOT IN current_session.skills_executed:
    APPEND skill.id TO current_session.skills_executed
  WRITE log TO _state/prompt_log.json

  // Prepare inputs based on skill requirements
  skill_inputs = {}

  FOR each required_input in skill.inputs.required:
    // Resolve input from state or previous skill outputs
    IF required_input is file_path:
      IF FILE_EXISTS(required_input):
        skill_inputs[required_input] = READ(required_input)
      ELSE:
        LOG: "⚠️ Required input not found: {required_input}"
    ELSE IF required_input in global_state:
      skill_inputs[required_input] = global_state[required_input]

  // Invoke skill using dynamic invocation
  result = INVOKE_SKILL(
    skill_id: skill.id,
    inputs: skill_inputs,
    options: {
      mode: "sync",
      on_failure: "BLOCK",
      trace: true
    }
  )

  IF result.success:
    LOG: "✅ Skill completed: {skill.id}"

    // Check if skill can invoke 3rdParty skills
    IF skill.can_invoke.length > 0:
      LOG: "📌 Skill {skill.id} may invoke: {skill.can_invoke.join(', ')}"

      // These invocations happen inside the skill's procedure
      // They're logged automatically by the skill

  ELSE:
    LOG: "❌ Skill failed: {skill.id} - {result.error}"
  
  VERIFY skill updated progress.json:
    CHECK phases.{skill}.status exists
    CHECK phases.{skill}.validation exists
    
    IF not updated:
      ═══════════════════════════════════════════
      ⚠️ SKILL DID NOT UPDATE PROGRESS
      ═══════════════════════════════════════════
      
      Skill {skill} completed but did not update progress.json
      
      How would you like to proceed?
      1. "mark complete" - Manually mark as complete
      2. "rerun: {skill}" - Run skill again
      3. "continue" - Proceed anyway
      ═══════════════════════════════════════════
      
      WAIT for user response
  
  VERIFY skill validation passed:
    IF phases.{skill}.validation.status != "passed":
      ═══════════════════════════════════════════
      ⚠️ SKILL VALIDATION FAILED
      ═══════════════════════════════════════════
      
      Skill {skill} validation did not pass.
      
      Validation results:
      • Checks run: {count}
      • Checks passed: {count}
      • Status: {status}
      
      How would you like to proceed?
      1. "rerun: {skill}" - Run skill again
      2. "continue" - Proceed anyway (may cause issues)
      3. "abort" - Stop pipeline
      ═══════════════════════════════════════════
      
      WAIT for user response
  
  DISPLAY P0 progress
  DISPLAY prompt count for skill
```

### Step 5: Track Requirements Progress Throughout
```
AFTER each skill completes:
  IF requirements_registry.json exists:
    LOAD registry
    
    COUNT requirements with addressed_by entries:
      p0_addressed = count where:
        priority == "P0" AND addressed_by.length > 0
      p0_total = count where priority == "P0"
      
    UPDATE progress.json.requirements_progress:
      {
        "p0_total": p0_total,
        "p0_addressed": p0_addressed,
        "p0_coverage": percentage
      }
      
    DISPLAY:
      ══════════════════════════════════════════════
      P0 Requirements Progress: {p0_addressed}/{p0_total} ({percentage}%)
      ══════════════════════════════════════════════
```

### Step 6: Enforce QA Blocking (CRITICAL)
```
AFTER QA skill completes:
  READ phases.qa.validation
  
  IF delivery_status == "BLOCKED":
    ═══════════════════════════════════════════
    ❌ PIPELINE BLOCKED BY QA
    ═══════════════════════════════════════════
    
    QA validation BLOCKED delivery.
    
    P0 Coverage: {percentage}% (MUST BE 100%)
    
    Unaddressed P0 Requirements:
    • [list from QA results]
    
    Resolution required before proceeding to UIAudit.
    
    How would you like to proceed?
    1. "resolve" - Interactive resolution
    2. "rerun from: [skill]" - Fix and re-run
    3. "exception: [reason]" - Document exception
    4. "abort" - Stop pipeline
    ═══════════════════════════════════════════
    
    WAIT for user response
    
    IF response != "exception":
      LOOP until delivery_status == "APPROVED"
    
  ELSE:
    LOG: "QA APPROVED - proceeding to UIAudit"
    PROCEED to UIAudit
```

### Step 7: Generate Pipeline Summary
```
AFTER all skills complete (or blocked):
  
  CALCULATE final metrics:
    - Skills completed
    - Skills with validation passed
    - P0 coverage
    - Total requirements addressed
    - Total prompts logged
  
  DISPLAY:
    ══════════════════════════════════════════════════════
    PROTOTYPE BUILD {COMPLETE/BLOCKED}
    ══════════════════════════════════════════════════════
    
    Skills Executed: {completed}/{total}
    
    Validation Summary:
    ├─ Passed: {count}
    ├─ Failed: {count}
    └─ Skipped: {count}
    
    Requirements Traceability:
    ├─ P0: {addressed}/{total} ({percentage}%) {status_icon}
    ├─ P1: {addressed}/{total} ({percentage}%)
    └─ P2: {addressed}/{total} ({percentage}%)
    
    QA Status: {APPROVED/BLOCKED}
    
    Prompt Log:
    ├─ Session: {session_id}
    ├─ Prompts Executed: {count}
    └─ Success Rate: {percentage}%
    
    Key Outputs:
    ├─ _state/requirements_registry.json
    ├─ _state/prompt_log.json
    ├─ outputs/07-qa/TRACEABILITY_MATRIX.md
    ├─ src/ (generated code)
    └─ outputs/08-audit/UI_AUDIT_REPORT.md
    
    ══════════════════════════════════════════════════════
```

### Step 8: Update Final Progress
```
UPDATE _state/progress.json:
  pipeline_status = "complete" | "blocked"
  pipeline_completed_at = timestamp
  
  requirements_progress.final = {
    p0_total: count,
    p0_addressed: count,
    p0_coverage: percentage,
    p1_coverage: percentage,
    total_addressed: count
  }
  
  validation_summary = {
    skills_run: count,
    skills_passed: count,
    skills_failed: count
  }
```

### Step 9: Finalize Prompt Log Session
```
UPDATE _state/prompt_log.json:
  FIND current session in sessions[]
  UPDATE session:
    ended_at: timestamp
    skills_executed: [list of skills run]
    entry_count: count of entries in this session
    success_count: count where status == "success"
    error_count: count where status == "error"
    total_tokens: sum of tokens_used
    total_duration_ms: sum of duration_ms
    
  UPDATE summary:
    total_entries: count all entries
    recalculate by_skill, by_category, by_status counts

GENERATE _state/PROMPT_LOG.md (human-readable summary)

LOG: "Session {session_id} finalized: {entry_count} prompts logged"
```

---

## Batch Execution Mode (Phase 3 Enhancement)

> **executing-plans Integration**: Execute implementation task plans in controlled batches with architect review checkpoints.

### When to Use Batch Execution

Use batch execution mode when:
- Running generated task plans from Sequencer
- Implementing features with TDD workflow
- Need checkpoint reviews between batches
- Want controlled, reviewable progress

### Batch Execution Procedure

```
IF MODE == "batch_execution":

  // ═══════════════════════════════════════════════════════════
  // STEP B1: LOAD AND REVIEW PLAN
  // ═══════════════════════════════════════════════════════════

  READ plan_file from PLAN parameter

  IF plan_file not exists:
    ═══════════════════════════════════════════
    ❌ PLAN FILE NOT FOUND
    ═══════════════════════════════════════════

    Could not find: {PLAN}

    Available plans:
    {list 04-implementation/plans/*.md}

    Select a plan or provide correct path.
    ═══════════════════════════════════════════

    WAIT for user response

  PARSE plan_file:
    - Extract goal, architecture, tech stack
    - Extract all tasks with steps
    - Count total tasks

  REVIEW plan critically:
    - Check for missing dependencies
    - Check for unclear instructions
    - Check for incomplete code examples

  IF concerns found:
    DISPLAY:
      ═══════════════════════════════════════════
      ⚠️ PLAN REVIEW: CONCERNS IDENTIFIED
      ═══════════════════════════════════════════

      Before starting execution, I have some concerns:

      {list concerns}

      How would you like to proceed?
      1. "proceed" - Continue with execution anyway
      2. "modify" - Let me address concerns first
      3. "abort" - Stop and revise plan
      ═══════════════════════════════════════════

    WAIT for user response

  ELSE:
    LOG: "✅ Plan reviewed, no concerns. Ready to execute."

  CREATE TodoWrite for all tasks:
    FOR each task in plan:
      ADD todo: { content: task.name, status: "pending", activeForm: task.activeForm }

  // ═══════════════════════════════════════════════════════════
  // STEP B2: EXECUTE BATCH
  // ═══════════════════════════════════════════════════════════

  BATCH_SIZE = BATCH_SIZE parameter OR 3  // Default: 3 tasks

  current_batch = tasks.slice(0, BATCH_SIZE)
  remaining_tasks = tasks.slice(BATCH_SIZE)

  DISPLAY:
    ═══════════════════════════════════════════
    🚀 EXECUTING BATCH 1
    ═══════════════════════════════════════════

    Tasks in this batch:
    1. {task_1.name}
    2. {task_2.name}
    3. {task_3.name}

    Total tasks: {total_count}
    Remaining after batch: {remaining_count}
    ═══════════════════════════════════════════

  FOR each task in current_batch:
    // Mark task as in_progress
    UPDATE TodoWrite: task.status = "in_progress"

    LOG: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    LOG: "Task: {task.name}"
    LOG: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    // Follow each step exactly
    FOR each step in task.steps:
      LOG: "Step {step.number}: {step.description}"

      EXECUTE step.action:
        - If "Write the failing test" → CREATE test file with code from plan
        - If "Run test" → EXECUTE command, CAPTURE output
        - If "Write implementation" → CREATE implementation file with code from plan
        - If "Commit" → EXECUTE git commit

      VERIFY step.expected_result:
        IF actual_result != expected_result:
          ═══════════════════════════════════════════
          ⚠️ STEP VERIFICATION FAILED
          ═══════════════════════════════════════════

          Step: {step.description}
          Expected: {step.expected_result}
          Actual: {actual_result}

          How would you like to proceed?
          1. "retry" - Try step again
          2. "fix: [instruction]" - Apply fix and retry
          3. "skip" - Skip to next step
          4. "stop" - Stop batch execution
          ═══════════════════════════════════════════

          WAIT for user response

    // Mark task as completed
    UPDATE TodoWrite: task.status = "completed"

    LOG: "✅ Task complete: {task.name}"

  // ═══════════════════════════════════════════════════════════
  // STEP B3: REPORT BATCH RESULTS
  // ═══════════════════════════════════════════════════════════

  RUN verification commands:
    cd prototype && npm run test:run
    cd prototype && npx tsc --noEmit

  CAPTURE verification_results

  DISPLAY:
    ═══════════════════════════════════════════════════════════════
    📊 BATCH 1 COMPLETE
    ═══════════════════════════════════════════════════════════════

    Tasks Completed:
    ✅ {task_1.name}
    ✅ {task_2.name}
    ✅ {task_3.name}

    Verification Results:
    • Tests: {test_count} passed, {failed_count} failed
    • TypeScript: {error_count} errors
    • Commits: {commit_count}

    Files Created/Modified:
    {list files}

    Remaining Tasks: {remaining_count}

    ═══════════════════════════════════════════════════════════════

    Ready for feedback.

    Options:
    1. "continue" - Execute next batch
    2. "review: [file]" - Show specific file
    3. "fix: [issue]" - Apply fix before continuing
    4. "pause" - Pause execution, save state
    5. "abort" - Stop execution
    ═══════════════════════════════════════════════════════════════

  WAIT for user response

  // ═══════════════════════════════════════════════════════════
  // STEP B4: CONTINUE OR COMPLETE
  // ═══════════════════════════════════════════════════════════

  IF response == "continue":
    IF remaining_tasks.length > 0:
      // Move to next batch
      current_batch = remaining_tasks.slice(0, BATCH_SIZE)
      remaining_tasks = remaining_tasks.slice(BATCH_SIZE)
      batch_number++

      GOTO STEP B2  // Execute next batch

    ELSE:
      // All tasks complete
      DISPLAY:
        ═══════════════════════════════════════════════════════════════
        🎉 PLAN EXECUTION COMPLETE
        ═══════════════════════════════════════════════════════════════

        All {total_tasks} tasks completed successfully.

        Final Verification:
        {run and display final test results}

        Next Steps:
        1. Review generated code
        2. Run QA validation: "invoke Prototype_QA"
        3. Start next phase plan

        ═══════════════════════════════════════════════════════════════

  ELSE IF response == "pause":
    SAVE execution state to _state/batch_execution.json:
      {
        plan_file: PLAN,
        completed_tasks: [...],
        remaining_tasks: [...],
        batch_number: current,
        paused_at: timestamp
      }

    LOG: "Execution paused. Resume with: invoke Builder MODE: batch_execution RESUME: true"

  ELSE IF response starts with "fix:":
    APPLY fix
    RE-RUN verification
    RETURN to feedback prompt
```

### Batch Execution Commands

| Command | Action |
|---------|--------|
| `batch: {plan}` | Start batch execution for plan |
| `batch continue` | Continue paused execution |
| `batch status` | Show current batch progress |
| `batch skip` | Skip current task |
| `batch abort` | Stop execution |

### When to Stop and Ask

**STOP executing immediately when:**
- Test fails unexpectedly
- Missing dependency discovered
- Instruction is unclear
- File conflict occurs

**Don't guess - ask for clarification.**

---

## Builder Commands

| Command | Action |
|---------|--------|
| `build` | Execute all skills in order |
| `build from {skill}` | Resume from specific skill |
| `build only {skill}` | Execute single skill |
| `status` | Show current progress |
| `requirements` | Show P0 coverage progress |
| `validate` | Run QA validation only |
| `reset` | Clear progress, start fresh |

### Documentation Commands

| Command | Action |
|---------|--------|
| `decompose` | Generate/update OPML decomposition for all apps |
| `decompose {AppName}` | Generate/update for specific app only |
| `decompose status` | Show current decomposition versions |

### Prompt Log Commands

| Command | Action |
|---------|--------|
| `show prompt log` | Display recent prompt entries |
| `show prompt log for {skill}` | Filter by skill |
| `show prompt log errors` | Show only errors |
| `export prompt log` | Export complete log |
| `search prompts for {keyword}` | Search prompt text |

### Change Management Commands

| Command | Action |
|---------|--------|
| `new session` | Start new feedback session |
| `resume session [id]` | Continue existing session |
| `list sessions` | Show all feedback sessions |
| `session summary` | Show current session summary |
| `close session` | Complete and archive session |
| `next change` | Process next pending change |
| `list changes` | Show all change requests |
| `show CR-xxx` | Show specific change request |
| `defer CR-xxx` | Move change to backlog |
| `rollback to [backup_id]` | Restore from backup |
| `list backups` | Show available backups |

---

## Validation Enforcement Rules

| Rule | Enforcement |
|------|-------------|
| Skill must update progress.json | Prompt if missing |
| Skill validation must pass | Prompt on failure |
| QA P0 coverage must be 100% | BLOCKS pipeline |
| Dependencies must complete | BLOCKS dependent skill |
| All prompts must be logged | Required for audit |

---

## User Mitigation Options

| Response | Action |
|----------|--------|
| `migrate` | Run migration skill |
| `continue` | Proceed despite issue |
| `reset` | Start fresh |
| `run: [skill]` | Run specific skill |
| `rerun: [skill]` | Re-run skill |
| `skip to: [skill]` | Force skip |
| `mark complete` | Manual completion |
| `resolve` | Interactive resolution |
| `exception: [reason]` | Document exception |
| `abort` | Stop pipeline |

---

## Progress.json Structure (Schema 2.3)

```json
{
  "$metadata": {
    "document_id": "STATE-PROGRESS-001",
    "version": "1.0.0",
    "created_at": "YYYY-MM-DDTHH:MM:SSZ",
    "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
    "generated_by": "Prototype_Builder",
    "change_history": [
      {
        "version": "1.0.0",
        "date": "YYYY-MM-DD",
        "author": "Prototype_Builder",
        "changes": "Initial progress tracking creation"
      }
    ]
  },
  "schema_version": "2.3",
  "pipeline_status": "in_progress",
  "started_at": "2024-12-13T10:00:00Z",
  "current_session_id": "sess-003",
  
  "phases": {
    "validate_discovery": {
      "status": "complete",
      "completed_at": "...",
      "outputs": ["..."],
      "validation": {
        "status": "passed",
        "checks_run": 7,
        "checks_passed": 7
      },
      "metrics": { ... },
      "prompts_logged": 7
    }
  },
  
  "requirements_progress": {
    "p0_total": 15,
    "p0_addressed": 15,
    "p0_coverage": "100%",
    "last_updated": "..."
  },
  
  "validation_summary": {
    "skills_run": 15,
    "skills_passed": 15,
    "skills_failed": 0
  },
  
  "context": {
    "product_name": "TalentoSphere ATS",
    "entity_count": 12,
    "screen_count": 15
  }
}
```

---

## 🚀 PARALLEL AGENT EXECUTION MODE (v3.0)

Prototype orchestration supports parallel agent execution for up to **60% faster** completion times. This mode spawns specialized agents that work concurrently on independent tasks.

### Agent Architecture Overview

```
┌────────────────────────────────────────────────────────────────────────────┐
│                     PROTOTYPE PARALLEL EXECUTION FLOW                      │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  PHASE 6-7: DESIGN SPECIFICATION (PARALLEL)                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────────┐ │   │
│  │  │ Design Token     │  │ Component        │  │ Data Model         │ │   │
│  │  │ Generator        │  │ Specifier        │  │ Specifier          │ │   │
│  │  │ (sonnet)         │  │ (sonnet)         │  │ (sonnet)           │ │   │
│  │  └────────┬─────────┘  └────────┬─────────┘  └─────────┬──────────┘ │   │
│  │           │                     │                      │            │   │
│  │           └─────────────────────┼──────────────────────┘            │   │
│  │                                 ▼                                   │   │
│  │                    ┌───────────────────────────────┐                │   │
│  │                    │    SPECIFICATION MERGE GATE   │                │   │
│  │                    └───────────────┬───────────────┘                │   │
│  └────────────────────────────────────┼────────────────────────────────┘   │
│                                       ▼                                    │
│  CHECKPOINT 6-7: VALIDATION                                                │
│                                       │                                    │
│                                       ▼                                    │
│  PHASE 8-9: SCREEN SPECIFICATION (PARALLEL)                                │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ┌──────────────────┐          ┌──────────────────┐                 │   │
│  │  │ Screen Specifier │          │ API Contract     │                 │   │
│  │  │ (sonnet)         │          │ Specifier        │                 │   │
│  │  │                  │          │ (sonnet)         │                 │   │
│  │  └────────┬─────────┘          └────────┬─────────┘                 │   │
│  │           │                             │                           │   │
│  │           └─────────────┬───────────────┘                           │   │
│  │                         ▼                                           │   │
│  │             ┌───────────────────────────────┐                       │   │
│  │             │     SPECIFICATION MERGE GATE  │                       │   │
│  │             └───────────────┬───────────────┘                       │   │
│  └─────────────────────────────┼───────────────────────────────────────┘   │
│                                ▼                                           │
│  CHECKPOINT 8-9: VALIDATION                                                │
│                                │                                           │
│                                ▼                                           │
│  PHASE 13-14: VALIDATION (PARALLEL)                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐        │   │
│  │  │ UX         │ │ Component  │ │ Screen     │ │ Accessib.  │        │   │
│  │  │ Validator  │ │ Validator  │ │ Validator  │ │ Auditor    │        │   │
│  │  │ (haiku)    │ │ (haiku)    │ │ (haiku)    │ │ (haiku)    │        │   │
│  │  └──────┬─────┘ └─────┬──────┘ └─────┬──────┘ └─────┬──────┘        │   │
│  │         │             │              │              │               │   │
│  │         └─────────────┼──────────────┼──────────────┘               │   │
│  │                       ▼              ▼                              │   │
│  │              ┌────────────────────────────────┐                     │   │
│  │              │      VALIDATION MERGE GATE     │                     │   │
│  │              └─────────────┬──────────────────┘                     │   │
│  │                            ▼                                        │   │
│  │              ┌────────────────────────────────┐                     │   │
│  │              │     Visual QA Tester           │ ◀── Final (sonnet)  │   │
│  │              │     (Playwright Screenshots)   │                     │   │
│  │              └────────────────────────────────┘                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Available Prototype Agents

#### Specification Agents (Phase 6-9)

| Agent | Type | Model | Purpose | Output |
|-------|------|-------|---------|--------|
| `prototype-design-token-generator` | Specification | **haiku** | Generate design tokens (templated JSON) | `00-foundation/design-tokens.json` |
| `prototype-component-specifier` | Specification | sonnet | Component library specifications | `01-components/component-index.md` |
| `prototype-screen-specifier` | Specification | sonnet | Screen layout and UX specifications | `02-screens/screen-index.md` |
| `prototype-data-model-specifier` | Specification | sonnet | Data model from discovery entities | `04-implementation/data-model.md` |
| `prototype-api-contract-specifier` | Specification | **haiku** | OpenAPI contracts (templated schema) | `04-implementation/api-contracts.json` |

#### Validation Agents (Phase 13-14)

| Agent | Type | Model | Purpose | Output |
|-------|------|-------|---------|--------|
| `prototype-ux-validator` | Validation | haiku | UX principles and heuristics | `05-validation/ux-validation.md` |
| `prototype-component-validator` | Validation | haiku | Component compliance | `05-validation/component-validation.md` |
| `prototype-screen-validator` | Validation | haiku | Screen spec compliance | `05-validation/screen-validation.md` |
| `prototype-accessibility-auditor` | Validation | haiku | WCAG 2.1 AA compliance | `05-validation/accessibility-audit.md` |
| `prototype-visual-qa-tester` | Validation | sonnet | Visual regression with Playwright | `05-validation/visual-qa-report.md` |

> **Note**: Agents use `general-purpose` subagent_type with agent instructions from `.claude/agents/`

### Parallel Execution Protocol

#### Phase 6-7: Design Specification (3 Agents in Parallel)

Spawn design-focused agents after Discovery validation:

```javascript
// Phase 6-7: Parallel design specification
// Use general-purpose subagent_type with agent instructions from .claude/agents/
const designAgents = [];

// Market Validator - independent
designAgents.push(Task({
  subagent_type: "general-purpose",
  model: "haiku",  // Research task
  description: "Validate design against market",
  prompt: `Agent: planning-product-researcher
    Read: .claude/agents/planning-product-researcher.md
    DISCOVERY: ${DISCOVERY_PATH} | OUTPUT: ${OUTPUT_PATH}/00-foundation/
    Generate: market-validation.md, trend-alignment.md`
}));

// Design Token Generator - independent (haiku: templated JSON)
designAgents.push(Task({
  subagent_type: "general-purpose",
  model: "haiku",  // Templated JSON output
  description: "Generate design tokens",
  prompt: `Agent: prototype-design-token-generator
    Read: .claude/agents/prototype-design-token-generator.md
    DISCOVERY: ${DISCOVERY_PATH} | OUTPUT: ${OUTPUT_PATH}/00-foundation/
    Generate: design-tokens.json, color-system.md, typography.md, spacing-layout.md`
}));

// Component Specifier - independent
designAgents.push(Task({
  subagent_type: "general-purpose",
  model: "sonnet",  // Complex spec generation
  description: "Specify components",
  prompt: `Agent: prototype-component-specifier
    Read: .claude/agents/prototype-component-specifier.md
    DISCOVERY: ${DISCOVERY_PATH} | OUTPUT: ${OUTPUT_PATH}/01-components/
    Generate: component-index.md, category specs with props/variants/a11y`
}));

// Data Model Specifier - independent
designAgents.push(Task({
  subagent_type: "general-purpose",
  model: "sonnet",  // Complex entity modeling
  description: "Specify data model",
  prompt: `Agent: prototype-data-model-specifier
    Read: .claude/agents/prototype-data-model-specifier.md
    DISCOVERY: ${DISCOVERY_PATH} | OUTPUT: ${OUTPUT_PATH}/04-implementation/
    Generate: data-model.md, TypeScript interfaces, validation rules`
}));

await Promise.all(designAgents);
await merge_design_outputs();
```

#### Phase 8-9: Screen & API Specification (2 Agents in Parallel)

After design merge, spawn screen-focused agents:

```javascript
// Phase 8-9: Parallel screen and API specification
const screenAgents = [
  Task({
    subagent_type: "general-purpose",
    model: "sonnet",  // Complex screen design
    description: "Specify screens",
    prompt: `Agent: prototype-screen-specifier
      Read: .claude/agents/prototype-screen-specifier.md
      DISCOVERY: ${DISCOVERY_PATH} | COMPONENTS: ${OUTPUT_PATH}/01-components/
      OUTPUT: ${OUTPUT_PATH}/02-screens/
      Generate: screen-index.md, per-screen folders, update screen_registry.json`
  }),

  Task({
    subagent_type: "general-purpose",
    model: "haiku",  // Templated OpenAPI schema
    description: "Specify API contracts",
    prompt: `Agent: prototype-api-contract-specifier
      Read: .claude/agents/prototype-api-contract-specifier.md
      SCREENS: ${OUTPUT_PATH}/02-screens/ | DATA_MODEL: ${OUTPUT_PATH}/04-implementation/data-model.md
      OUTPUT: ${OUTPUT_PATH}/04-implementation/
      Generate: api-contracts.json (OpenAPI 3.0), mock data, error schemas`
  })
];

await Promise.all(screenAgents);
await merge_screen_api_outputs();
```

#### Phase 13-14: Validation (5 Agents - 4 Parallel + 1 Sequential)

Run 4 validation agents in parallel, then visual QA:

```javascript
// Phase 13: Parallel validation (4 agents - all haiku for checklist-based validation)
const validators = [
  Task({
    subagent_type: "general-purpose",
    model: "haiku",
    description: "Validate UX",
    prompt: `Agent: prototype-ux-validator
      Read: .claude/agents/prototype-ux-validator.md
      SCREENS: ${OUTPUT_PATH}/02-screens/ | COMPONENTS: ${OUTPUT_PATH}/01-components/
      OUTPUT: ${OUTPUT_PATH}/05-validation/ux-validation.md
      Checks: Nielsen's heuristics, consistency, error prevention, user control`
  }),

  Task({
    subagent_type: "general-purpose",
    model: "haiku",
    description: "Validate components",
    prompt: `Agent: prototype-component-validator
      Read: .claude/agents/prototype-component-validator.md
      SPECS: ${OUTPUT_PATH}/01-components/ | CODE: ${OUTPUT_PATH}/prototype/src/components/
      TOKENS: ${OUTPUT_PATH}/00-foundation/design-tokens.json
      OUTPUT: ${OUTPUT_PATH}/05-validation/component-validation.md`
  }),

  Task({
    subagent_type: "general-purpose",
    model: "haiku",
    description: "Validate screens",
    prompt: `Agent: prototype-screen-validator
      Read: .claude/agents/prototype-screen-validator.md
      SPECS: ${OUTPUT_PATH}/02-screens/ | CODE: ${OUTPUT_PATH}/prototype/src/pages/
      URL: http://localhost:3000
      OUTPUT: ${OUTPUT_PATH}/05-validation/screen-validation.md`
  }),

  Task({
    subagent_type: "general-purpose",
    model: "haiku",
    description: "Audit accessibility",
    prompt: `Agent: prototype-accessibility-auditor
      Read: .claude/agents/prototype-accessibility-auditor.md
      URL: http://localhost:3000 | SCREENS: ${OUTPUT_PATH}/02-screens/screen-index.md
      TOOL: .claude/skills/tools/accessibility_tester.py
      OUTPUT: ${OUTPUT_PATH}/05-validation/accessibility-audit.md`
  })
];

await Promise.all(validators);

// Phase 14: Visual QA (sequential - sonnet for visual reasoning)
const visualQA = await Task({
  subagent_type: "general-purpose",
  model: "sonnet",  // Visual comparison needs reasoning
  description: "Run visual QA",
  prompt: `Agent: prototype-visual-qa-tester
    Read: .claude/agents/prototype-visual-qa-tester.md
    URL: http://localhost:3000 | SCREENS: ${OUTPUT_PATH}/02-screens/screen-index.md
    BASELINE: ${OUTPUT_PATH}/05-validation/screenshots/baseline/
    TOOL: .claude/skills/tools/playwright_visual_qa.py
    VIEWPORTS: 1920x1080, 768x1024, 375x812 | THRESHOLD: 1%
    OUTPUT: ${OUTPUT_PATH}/05-validation/visual-qa-report.md`
});

await merge_validation_outputs();
```

### ID Namespace Allocation

To prevent ID conflicts during parallel execution:

| Agent | ID Prefix | Range |
|-------|-----------|-------|
| Design Token Generator | TOK-XXX | TOK-001 to TOK-099 |
| Component Specifier | COMP-XXX | COMP-001 to COMP-999 |
| Screen Specifier | SCR-XXX | SCR-001 to SCR-999 |
| Data Model Specifier | ENT-XXX | ENT-001 to ENT-099 |
| API Contract Specifier | API-XXX | API-001 to API-999 |

### Coordination Rules

1. **File Locking**: Agents MUST acquire locks before writing to shared registries
2. **Read-Only During Parallel**: Agents read from discovery, write to temporary outputs
3. **Merge Gate**: All parallel agents must complete before merge
4. **Checkpoint Validation**: Run after merge, not after individual agents
5. **Visual QA Last**: Visual QA runs after all other validators complete

### Enabling Parallel Mode

```bash
# Standard (sequential) execution
/prototype InventorySystem

# Parallel execution (add --parallel flag)
/prototype InventorySystem --parallel

# Resume parallel execution
/prototype-resume --parallel
```

### Parallel Execution State

Track parallel execution in `_state/prototype_progress.json`:

```json
{
  "execution_mode": "parallel",
  "current_phase": "6-7-design-spec",
  "parallel_agents": [
    {
      "agent_id": "prototype-design-token-generator",
      "status": "completed",
      "started_at": "2025-12-27T10:00:00Z",
      "completed_at": "2025-12-27T10:08:00Z",
      "output_tokens": 156
    },
    {
      "agent_id": "prototype-component-specifier",
      "status": "completed",
      "started_at": "2025-12-27T10:00:00Z",
      "completed_at": "2025-12-27T10:15:00Z",
      "output_components": 24
    },
    {
      "agent_id": "prototype-data-model-specifier",
      "status": "completed",
      "started_at": "2025-12-27T10:00:00Z",
      "completed_at": "2025-12-27T10:10:00Z",
      "output_entities": 8
    }
  ],
  "merge_status": "pending",
  "next_gate": "design-merge"
}
```

### Visual QA Tools Integration

The parallel validation phase integrates with CLI tools for automation:

#### Playwright Visual QA Tool

```bash
# Capture screenshots
.venv/bin/python .claude/skills/tools/playwright_visual_qa.py capture \
  --url http://localhost:3000 \
  --output 05-validation/screenshots/current/ \
  --screens screens.json

# Compare with baseline
.venv/bin/python .claude/skills/tools/playwright_visual_qa.py compare \
  --baseline 05-validation/screenshots/baseline/ \
  --current 05-validation/screenshots/current/ \
  --diff 05-validation/screenshots/diff/ \
  --threshold 0.01

# Generate report
.venv/bin/python .claude/skills/tools/playwright_visual_qa.py report \
  --results results.json \
  --output 05-validation/visual-qa-report.md
```

#### Accessibility Tester Tool

```bash
# Audit single page
.venv/bin/python .claude/skills/tools/accessibility_tester.py page \
  --url http://localhost:3000 \
  --wcag AA

# Audit multiple pages
.venv/bin/python .claude/skills/tools/accessibility_tester.py audit \
  --url http://localhost:3000 \
  --pages pages.json \
  --output 05-validation/

# Generate report
.venv/bin/python .claude/skills/tools/accessibility_tester.py report \
  --results results.json \
  --output 05-validation/accessibility-audit.md
```

---

## Quality Checklist

### Validation Enforcement
- [ ] Every skill updates progress.json
- [ ] Every skill has validation status
- [ ] Failed validations prompt user
- [ ] QA blocking enforced

### Requirements Tracking
- [ ] P0 coverage displayed after each skill
- [ ] Final coverage summary generated
- [ ] TRACEABILITY_MATRIX.md created

### Prompt Logging
- [ ] Session initialized at pipeline start
- [ ] All skills log their prompts
- [ ] Session finalized at pipeline end
- [ ] PROMPT_LOG.md generated

### Pipeline Integrity
- [ ] Dependencies checked before each skill
- [ ] Resume point saved on interruption
- [ ] Final status reflects actual state

### Parallel Execution (v3.0)
- [ ] Agent locks acquired before writes
- [ ] Merge gates complete before next phase
- [ ] All parallel agents complete before merge
- [ ] Visual QA runs after validators
