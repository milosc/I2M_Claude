---
name: prototype-multiagent
description: Generate prototype using multi-agent parallel execution
argument-hint: <SystemName>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-multiagent started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-multiagent ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-multiagent instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Assembly-First and traceability rules:

```bash
# Assembly-First rules (loaded automatically in Prototype stage)
/_assembly_first_rules

# Traceability rules for ID management
/rules-traceability
```

## Usage

```bash
# Start new prototype generation (visible terminal windows)
/prototype-multiagent EmergencyTriage

# Start with headless mode (no visible terminals)
/prototype-multiagent EmergencyTriage --headless

# Resume after agent failure
/prototype-multiagent EmergencyTriage --resume

# Resume specific checkpoint
/prototype-multiagent EmergencyTriage --resume --checkpoint 9

# Force retry failed agents
/prototype-multiagent EmergencyTriage --resume --retry-failed

# Resume with headless mode
/prototype-multiagent EmergencyTriage --resume --headless
```

## Arguments

- `$ARGUMENTS` - Required: `<SystemName>` or path to `ClientAnalysis_<SystemName>/`
- `--resume` - Resume from last failed or incomplete agent spawn
- `--checkpoint N` - Resume from specific checkpoint (0-14)
- `--retry-failed` - Retry previously failed agents instead of skipping
- `--headless` - Enable headless mode (no visible terminal windows). **Default: OFF** (terminals are visible)

## Prerequisites

- Completed Discovery: `ClientAnalysis_<SystemName>/` exists
- Dependencies installed: `/htec-libraries-init`
- Agent infrastructure:
  - `.claude/agents/PROTOTYPE_AGENT_REGISTRY.json`
  - `.claude/agents/prototype-orchestrator.md`
  - `.claude/hooks/agent_coordinator.py`

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ROBUST MULTI-AGENT ORCHESTRATION                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. Pre-Flight Checks:                                                  │
│     ├── Verify agent infrastructure exists                             │
│     ├── Check for resume state (_state/agent_spawn_manifest.json)      │
│     └── Load completed/failed agent history                            │
│                                                                         │
│  2. Phase Execution:                                                    │
│     ├── Determine start checkpoint (new vs resume)                     │
│     ├── For each checkpoint with agents:                               │
│     │   ├── Skip if all agents completed                               │
│     │   ├── Spawn agents (new or failed only)                          │
│     │   ├── VERIFY spawn succeeded (30s timeout)                       │
│     │   ├── RETRY with countermeasures (up to 3 attempts)              │
│     │   └── BLOCK & ASK USER if all retries fail                       │
│     └── Update spawn manifest after each agent                         │
│                                                                         │
│  3. Spawn Verification Protocol:                                        │
│     ├── Method 1: Check _state/agent_sessions.json for new entry       │
│     ├── Method 2: Poll agent_coordinator.py --status                   │
│     ├── Method 3: File system watcher (output file created)            │
│     └── Timeout: 30 seconds (configurable per agent)                   │
│                                                                         │
│  4. Retry Countermeasures (in order):                                   │
│     ├── Attempt 1: Retry with same prompt                              │
│     ├── Attempt 2: Retry with simplified prompt + explicit session ID  │
│     ├── Attempt 3: Fallback to general-purpose agent                   │
│     └── Attempt 4: BLOCK and request user intervention                 │
│                                                                         │
│  5. Resume Logic:                                                       │
│     ├── Load spawn manifest (_state/agent_spawn_manifest.json)         │
│     ├── Filter agents by status:                                       │
│     │   ├── completed → Skip                                           │
│     │   ├── failed → Skip (unless --retry-failed)                      │
│     │   ├── in_progress → Check heartbeat, resume or retry             │
│     │   └── not_started → Spawn                                        │
│     └── Continue from first incomplete checkpoint                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Execution Logic

### Step 1: Parse Arguments and Initialize

```javascript
// Extract system name
const SYSTEM_NAME = extractSystemName($ARGUMENTS);
const IS_RESUME = $ARGUMENTS.includes('--resume');
const RETRY_FAILED = $ARGUMENTS.includes('--retry-failed');
const HEADLESS_MODE = $ARGUMENTS.includes('--headless'); // Default: false (visible terminals)
const CHECKPOINT_OVERRIDE = extractCheckpoint($ARGUMENTS); // --checkpoint N

// Paths
const DISCOVERY_PATH = `ClientAnalysis_${SYSTEM_NAME}/`;
const OUTPUT_PATH = `Prototype_${SYSTEM_NAME}/`;
const STATE_PATH = `_state/`;
const SPAWN_MANIFEST_PATH = `${STATE_PATH}agent_spawn_manifest.json`;

// Log terminal mode
log(`Terminal Mode: ${HEADLESS_MODE ? '❌ HEADLESS (no visible terminals)' : '✅ VISIBLE (terminal windows will open)'}`);
```

### Step 2: Pre-Flight Validation

```javascript
// 1. Verify Discovery exists
if (!exists(DISCOVERY_PATH)) {
  error(`Discovery not found: ${DISCOVERY_PATH}`);
  exit(1);
}

// 2. Verify agent infrastructure
const infraChecks = {
  registry: exists('.claude/agents/PROTOTYPE_AGENT_REGISTRY.json'),
  orchestrator: exists('.claude/agents/prototype-orchestrator.md'),
  coordinator: exists('.claude/hooks/agent_coordinator.py'),
  pre_spawn: exists('.claude/hooks/pre_agent_spawn.py'),
  post_completion: exists('.claude/hooks/post_task_completion.py')
};

if (!Object.values(infraChecks).every(v => v)) {
  error('❌ Multi-Agent Infrastructure Incomplete');
  Object.entries(infraChecks).forEach(([name, exists]) => {
    log(`   ${exists ? '✅' : '❌'} ${name}`);
  });
  log('\n💡 Run standard /prototype command for sequential fallback');
  exit(1);
}

log('✅ Multi-Agent Infrastructure: READY');
log('   11 specialized agents available');
log('   Spawn verification: ENABLED');
log('   Retry logic: ENABLED (3 attempts per agent)');
log('   Resume capability: ENABLED\n');
```

### Step 3: Load or Initialize Spawn Manifest

```javascript
// Agent Spawn Manifest Schema
const manifestSchema = {
  schema_version: "1.0.0",
  system_name: SYSTEM_NAME,
  started_at: timestamp,
  updated_at: timestamp,
  mode: "multi_agent",
  headless_mode: HEADLESS_MODE, // false = visible terminals (default), true = no terminals
  orchestrator_session_id: null, // Set when orchestrator spawns

  // Agent execution tracking
  agents: [
    {
      agent_id: "prototype-data-model-specifier",
      checkpoint: 3,
      phase: "data_model",
      status: "not_started", // not_started | spawning | in_progress | completed | failed | blocked
      spawn_attempts: 0,
      max_attempts: 3,

      // Spawn verification
      task_call_id: null,           // Task() call identifier
      session_id: null,             // From agent_sessions.json
      spawn_method: null,           // "orchestrator" | "general-purpose" | "fallback"
      spawn_requested_at: null,
      spawn_verified_at: null,
      spawn_timeout_seconds: 30,

      // Execution tracking
      started_at: null,
      completed_at: null,
      heartbeat_at: null,

      // Outputs
      expected_outputs: [
        "00-foundation/data-model/DATA_MODEL.md",
        "00-foundation/data-model/ENTITY_INDEX.md"
      ],
      actual_outputs: [],

      // Error handling
      error_message: null,
      retry_history: [],
      countermeasure_applied: null,

      // Dependencies
      depends_on: [],               // Agent IDs that must complete first
      blocks: []                    // Agent IDs that wait for this one
    }
    // ... more agents
  ],

  // Phase tracking
  phases: {
    "CP-0": { status: "completed", agents: [] },
    "CP-1": { status: "completed", agents: [] },
    "CP-2": { status: "completed", agents: [] },
    "CP-3": { status: "in_progress", agents: ["prototype-data-model-specifier"] },
    // ... more phases
  },

  // Global state
  current_checkpoint: 0,
  total_agents_planned: 11,
  total_agents_completed: 0,
  total_agents_failed: 0,
  total_spawn_attempts: 0,
  blocked_on_agent: null,        // Agent ID blocking progress
  blocked_reason: null,
  user_intervention_required: false
};

let manifest;

if (IS_RESUME && exists(SPAWN_MANIFEST_PATH)) {
  // Resume mode
  manifest = JSON.parse(read(SPAWN_MANIFEST_PATH));
  log(`📋 Resume Mode: Loaded spawn manifest`);
  log(`   Started: ${manifest.started_at}`);
  log(`   Checkpoint: ${manifest.current_checkpoint}`);
  log(`   Completed: ${manifest.total_agents_completed}/${manifest.total_agents_planned}`);
  log(`   Failed: ${manifest.total_agents_failed}`);

  if (manifest.user_intervention_required) {
    log(`\n⚠️  USER INTERVENTION REQUIRED`);
    log(`   Blocked on: ${manifest.blocked_on_agent}`);
    log(`   Reason: ${manifest.blocked_reason}`);
    log(`\n   To retry: /prototype-multiagent ${SYSTEM_NAME} --resume --retry-failed`);
    log(`   To skip: Mark agent as 'failed' in manifest, then --resume`);
    exit(1);
  }

  // Apply checkpoint override
  if (CHECKPOINT_OVERRIDE !== null) {
    manifest.current_checkpoint = CHECKPOINT_OVERRIDE;
    log(`   Override: Starting from checkpoint ${CHECKPOINT_OVERRIDE}\n`);
  }

} else {
  // New run mode
  manifest = initializeManifest(SYSTEM_NAME);
  log(`📋 New Run: Initialized spawn manifest\n`);
}

// Save initial manifest
write(SPAWN_MANIFEST_PATH, JSON.stringify(manifest, null, 2));
```

### Step 4: Spawn Orchestrator with Verification

```javascript
log(`🚀 Spawning Orchestrator Agent...\n`);

const orchestratorTaskId = `task-orchestrator-${Date.now()}`;

// Spawn orchestrator
const orchestratorSpawn = spawnAgentWithVerification({
  agent_id: "prototype-orchestrator",
  task_call_id: orchestratorTaskId,
  subagent_type: "prototype-orchestrator",
  model: "sonnet",
  description: "Orchestrate Prototype generation",
  prompt: generateOrchestratorPrompt(SYSTEM_NAME, manifest),
  headless_mode: HEADLESS_MODE, // Pass terminal visibility setting
  verification_method: "session_registry",
  timeout_seconds: 30,
  retry_config: {
    max_attempts: 3,
    countermeasures: [
      "retry_same",           // Attempt 1: Same prompt
      "retry_with_session",   // Attempt 2: Add explicit session ID
      "fallback_sequential"   // Attempt 3: Run phases in main session
    ]
  }
});

// Verification function (defined below)
async function spawnAgentWithVerification(config) {
  const startTime = Date.now();
  let attempt = 0;

  while (attempt < config.retry_config.max_attempts) {
    attempt++;

    log(`   Attempt ${attempt}/${config.retry_config.max_attempts}: Spawning ${config.agent_id}...`);

    // Apply countermeasure for retry attempts
    if (attempt > 1) {
      const countermeasure = config.retry_config.countermeasures[attempt - 1];
      log(`   Applying countermeasure: ${countermeasure}`);
      config = applyCountermeasure(config, countermeasure, attempt);
    }

    // Call Task() to spawn agent
    // NOTE: Terminal visibility controlled by headless_mode (default: false = visible terminals)
    const taskCall = Task({
      subagent_type: config.subagent_type,
      model: config.model,
      description: config.description,
      prompt: config.prompt,
      run_in_background: false,  // Wait for completion
      // headless parameter controls terminal visibility:
      // - false (default): Opens visible terminal window for agent
      // - true: Runs agent without visible terminal
      headless: config.headless_mode
    });

    // VERIFICATION PHASE (30 second timeout)
    log(`   Verifying spawn...`);

    const verification = await verifyAgentSpawn({
      agent_id: config.agent_id,
      task_call_id: config.task_call_id,
      timeout_seconds: config.timeout_seconds,
      verification_method: config.verification_method
    });

    if (verification.success) {
      log(`   ✅ Agent spawned successfully`);
      log(`      Session ID: ${verification.session_id}`);
      log(`      Verified in: ${verification.verification_time_ms}ms\n`);

      // Update manifest
      updateManifestAgentStatus(manifest, config.agent_id, {
        status: "in_progress",
        spawn_attempts: attempt,
        session_id: verification.session_id,
        spawn_method: config.subagent_type,
        spawn_verified_at: new Date().toISOString(),
        spawn_requested_at: new Date(startTime).toISOString()
      });

      saveManifest(manifest);

      return {
        success: true,
        session_id: verification.session_id,
        attempt: attempt
      };
    } else {
      log(`   ❌ Spawn verification failed: ${verification.error}`);

      // Update retry history
      updateManifestRetryHistory(manifest, config.agent_id, {
        attempt: attempt,
        countermeasure: attempt > 1 ? config.retry_config.countermeasures[attempt - 1] : null,
        error: verification.error,
        timestamp: new Date().toISOString()
      });

      saveManifest(manifest);

      if (attempt < config.retry_config.max_attempts) {
        log(`   Retrying in 5 seconds...\n`);
        await sleep(5000);
      }
    }
  }

  // All retries exhausted
  log(`\n❌ SPAWN FAILURE: All ${config.retry_config.max_attempts} attempts exhausted`);
  log(`   Agent: ${config.agent_id}`);
  log(`   Reason: Spawn verification timeout (${config.timeout_seconds}s)\n`);

  // Update manifest - block execution
  updateManifestAgentStatus(manifest, config.agent_id, {
    status: "blocked",
    spawn_attempts: attempt,
    error_message: "Spawn verification failed after all retries"
  });

  manifest.user_intervention_required = true;
  manifest.blocked_on_agent = config.agent_id;
  manifest.blocked_reason = "Spawn verification timeout after 3 attempts";
  saveManifest(manifest);

  // Request user intervention
  blockAndRequestIntervention({
    agent_id: config.agent_id,
    attempts: attempt,
    manifest_path: SPAWN_MANIFEST_PATH,
    system_name: SYSTEM_NAME
  });

  throw new Error(`Agent spawn failed: ${config.agent_id}`);
}
```

### Step 5: Verification Methods

```javascript
async function verifyAgentSpawn({ agent_id, task_call_id, timeout_seconds, verification_method }) {
  const startTime = Date.now();
  const deadline = startTime + (timeout_seconds * 1000);

  // Method 1: Session Registry Check (Primary)
  if (verification_method === "session_registry") {
    while (Date.now() < deadline) {
      // Check if agent_sessions.json has new entry
      if (exists('_state/agent_sessions.json')) {
        const sessions = JSON.parse(read('_state/agent_sessions.json'));

        // Look for active session matching agent_id
        const activeSession = sessions.active_sessions?.find(s =>
          s.agent_id === agent_id || s.agent_type === agent_id
        );

        if (activeSession) {
          return {
            success: true,
            session_id: activeSession.session_id,
            verification_time_ms: Date.now() - startTime,
            method: "session_registry"
          };
        }

        // Check completed sessions (fast agents)
        const completedSession = sessions.completed_sessions?.find(s =>
          s.agent_id === agent_id || s.agent_type === agent_id
        );

        if (completedSession) {
          return {
            success: true,
            session_id: completedSession.session_id,
            verification_time_ms: Date.now() - startTime,
            method: "session_registry",
            already_completed: true
          };
        }
      }

      // Poll every 500ms
      await sleep(500);
    }
  }

  // Method 2: Agent Coordinator Status (Fallback)
  if (verification_method === "coordinator_status" || Date.now() >= deadline) {
    const coordinatorOutput = exec('python3 .claude/hooks/agent_coordinator.py --status --json');
    const status = JSON.parse(coordinatorOutput);

    const activeAgent = status.active_agents?.find(a => a.agent_id === agent_id);
    if (activeAgent) {
      return {
        success: true,
        session_id: activeAgent.session_id,
        verification_time_ms: Date.now() - startTime,
        method: "coordinator_status"
      };
    }
  }

  // Timeout - verification failed
  return {
    success: false,
    error: `No agent session found within ${timeout_seconds}s`,
    verification_time_ms: Date.now() - startTime
  };
}
```

### Step 6: Countermeasures

```javascript
function applyCountermeasure(config, countermeasure, attempt) {
  const newConfig = { ...config };

  switch (countermeasure) {
    case "retry_same":
      // No changes - retry with same prompt
      log(`      → Retry with identical configuration`);
      break;

    case "retry_with_session":
      // Add explicit session ID to prompt
      const explicitSessionId = `sess-${Date.now()}-${attempt}`;
      newConfig.prompt = `
        SESSION_ID: ${explicitSessionId}

        ${config.prompt}

        CRITICAL: Register your session immediately:
        python3 .claude/hooks/agent_coordinator.py --register \\
          --session-id "${explicitSessionId}" \\
          --agent-id "${config.agent_id}" \\
          --agent-type "${config.subagent_type}"
      `;
      log(`      → Added explicit session ID: ${explicitSessionId}`);
      break;

    case "fallback_general_purpose":
      // Use general-purpose agent as fallback
      newConfig.subagent_type = "general-purpose";
      newConfig.prompt = `
        You are acting as: ${config.agent_id}

        ${config.prompt}

        IMPORTANT: This is a fallback spawn using general-purpose agent.
        Execute the task exactly as the specialized agent would.
      `;
      log(`      → Fallback to general-purpose agent`);
      break;

    case "fallback_sequential":
      // Last resort - execute in main session
      log(`      → Fallback to sequential execution (main session)`);
      // This will be handled by throwing and catching in orchestrator
      break;

    default:
      log(`      → Unknown countermeasure: ${countermeasure}`);
  }

  return newConfig;
}
```

### Step 7: Block and Request User Intervention

```javascript
function blockAndRequestIntervention({ agent_id, attempts, manifest_path, system_name }) {
  const troubleshooting = generateTroubleshootingGuide(agent_id);

  log(`
╔═══════════════════════════════════════════════════════════════════════════╗
║                     USER INTERVENTION REQUIRED                            ║
╚═══════════════════════════════════════════════════════════════════════════╝

  Agent: ${agent_id}
  Status: SPAWN FAILURE after ${attempts} attempts
  System: ${system_name}

  📋 Spawn Manifest: ${manifest_path}

  ❌ PROBLEM:
     The agent did not register a session within the 30-second timeout.
     This indicates the agent either:
       1. Did not spawn at all (Task() call failed)
       2. Spawned but failed to register with agent_coordinator.py
       3. Spawned but crashed before session registration

  🔍 TROUBLESHOOTING:

     1. Check if agent is defined in registry:
        grep "${agent_id}" .claude/agents/PROTOTYPE_AGENT_REGISTRY.json

     2. Verify agent definition file exists:
        ls -la .claude/agents/${agent_id}.md

     3. Check for recent agent errors:
        tail -50 _state/FAILURES_LOG.md

     4. Test minimal agent spawn:
        Task({
          subagent_type: "general-purpose",
          description: "Test spawn",
          prompt: "Echo: Agent spawn test successful"
        })

     5. Check agent coordinator status:
        python3 .claude/hooks/agent_coordinator.py --status

  🛠️  RESOLUTION OPTIONS:

     Option A: Fix the issue and retry
       1. Fix the root cause (missing file, registry, etc.)
       2. Run: /prototype-multiagent ${system_name} --resume --retry-failed

     Option B: Skip the failed agent and continue
       1. Edit ${manifest_path}
       2. Change agent status from "blocked" to "failed"
       3. Run: /prototype-multiagent ${system_name} --resume
          (Will skip failed agent, may cause downstream issues)

     Option C: Fallback to sequential execution
       1. Run: /prototype ${system_name}
          (Traditional sequential mode, no agents)

  📖 Detailed Troubleshooting:

${troubleshooting}

╚═══════════════════════════════════════════════════════════════════════════╝

  Execution halted. Please resolve the issue and resume.

`);
}

function generateTroubleshootingGuide(agent_id) {
  // Agent-specific troubleshooting steps
  const guides = {
    "prototype-orchestrator": `
      The orchestrator is the master coordinator. If it fails to spawn:
      - Verify .claude/agents/prototype-orchestrator.md exists
      - Check if "prototype-orchestrator" is in .claude/agents/PROTOTYPE_AGENT_REGISTRY.json
      - Try spawning with general-purpose agent as fallback
    `,
    "prototype-data-model-specifier": `
      The data model specifier generates entity schemas. If it fails:
      - Ensure input file exists: ClientAnalysis_X/04-design-specs/data-fields.md
      - Check skill file: .claude/skills/Prototype_DataModel/SKILL.md
      - Verify output path is writable: Prototype_X/00-foundation/data-model/
    `,
    // ... more agent-specific guides
  };

  return guides[agent_id] || "No specific troubleshooting guide available.";
}
```

### Step 8: Resume Logic in Orchestrator

The orchestrator prompt includes resume logic:

```javascript
function generateOrchestratorPrompt(systemName, manifest) {
  return `
    Generate complete Prototype for ${systemName}.

    DISCOVERY_PATH: ClientAnalysis_${systemName}/
    OUTPUT_PATH: Prototype_${systemName}/
    SPAWN_MANIFEST: _state/agent_spawn_manifest.json

    MODE: ${manifest.mode === "resume" ? "RESUME" : "NEW"}
    START_CHECKPOINT: ${manifest.current_checkpoint}
    TERMINAL_MODE: ${manifest.headless_mode ? "HEADLESS (no visible terminals)" : "VISIBLE (terminal windows will open)"}

    ${manifest.mode === "resume" ? `
    ⚠️  RESUME MODE ENABLED

    You are resuming from checkpoint ${manifest.current_checkpoint}.

    AGENT STATUS SUMMARY:
    - Completed: ${manifest.total_agents_completed}/${manifest.total_agents_planned}
    - Failed: ${manifest.total_agents_failed}
    - Remaining: ${manifest.total_agents_planned - manifest.total_agents_completed - manifest.total_agents_failed}

    RESUME RULES:
    1. Load spawn manifest from _state/agent_spawn_manifest.json
    2. For each checkpoint >= ${manifest.current_checkpoint}:
       a. Check agent status in manifest
       b. If status === "completed" → SKIP (already done)
       c. If status === "failed" → SKIP (unless --retry-failed)
       d. If status === "in_progress" → CHECK heartbeat:
          - If heartbeat < 5 min old → Wait for completion
          - If heartbeat > 5 min old → Consider stale, retry
       e. If status === "not_started" → SPAWN agent
    3. Update manifest after each agent completes
    4. Continue from last incomplete checkpoint

    AGENT MANIFEST EXAMPLE:
    {
      "agents": [
        {
          "agent_id": "prototype-data-model-specifier",
          "checkpoint": 3,
          "status": "completed",          ← SKIP this agent
          "session_id": "sess-001",
          "completed_at": "2026-01-02T20:45:00Z"
        },
        {
          "agent_id": "prototype-api-contract-specifier",
          "checkpoint": 4,
          "status": "failed",             ← SKIP (unless --retry-failed)
          "spawn_attempts": 3,
          "error_message": "Spawn timeout"
        },
        {
          "agent_id": "prototype-design-token-generator",
          "checkpoint": 6,
          "status": "not_started"         ← SPAWN this agent
        }
      ]
    }
    ` : ""}

    EXECUTION PLAN (14 Checkpoints):

    CP-0: Initialize (Main Orchestrator)
      - Create folder structure
      - Initialize _state/ files
      - Create spawn manifest
      → Status: ${getCheckpointStatus(manifest, 0)}

    CP-1: Validate Discovery (Main Orchestrator) [BLOCKING]
      - Validate Discovery outputs exist
      - Extract summary to _state/discovery_summary.json
      → Status: ${getCheckpointStatus(manifest, 1)}

    CP-2: Extract Requirements (Main Orchestrator)
      - Transform Discovery to requirements
      - Create _state/requirements_registry.json
      → Status: ${getCheckpointStatus(manifest, 2)}

    CP-3: Data Model [AGENT]
      Agent: prototype-data-model-specifier
      Status: ${getAgentStatus(manifest, "prototype-data-model-specifier")}
      ${getAgentResumeInstructions(manifest, "prototype-data-model-specifier")}

    CP-4: API Contracts [AGENT]
      Agent: prototype-api-contract-specifier
      Dependencies: CP-3 completed
      Status: ${getAgentStatus(manifest, "prototype-api-contract-specifier")}
      ${getAgentResumeInstructions(manifest, "prototype-api-contract-specifier")}

    CP-5: Test Data (Main Orchestrator)
      - Generate test data files
      → Status: ${getCheckpointStatus(manifest, 5)}

    CP-6-7: Design Tokens [AGENT]
      Agent: prototype-design-token-generator
      Status: ${getAgentStatus(manifest, "prototype-design-token-generator")}
      ${getAgentResumeInstructions(manifest, "prototype-design-token-generator")}

    CP-8: Component Specifications [AGENT]
      Agent: prototype-component-specifier
      Dependencies: CP-6-7 completed
      Status: ${getAgentStatus(manifest, "prototype-component-specifier")}
      ${getAgentResumeInstructions(manifest, "prototype-component-specifier")}

    CP-9: Screen Specifications [PARALLEL AGENTS]
      ${getScreenAgentsStatus(manifest)}

      PARALLEL EXECUTION:
      - Spawn one agent per Discovery screen
      - All agents run concurrently
      - Wait for all to complete before CP-10

      Resume Logic:
      ${getScreenAgentsResumeInstructions(manifest)}

    CP-10: Interactions (Main Orchestrator)
      - Generate motion/accessibility specs
      → Status: ${getCheckpointStatus(manifest, 10)}

    CP-11: Build Sequence (Main Orchestrator)
      - Generate implementation order
      → Status: ${getCheckpointStatus(manifest, 11)}

    CP-12: Code Generation (Main Orchestrator)
      - Generate React code for all screens
      → Status: ${getCheckpointStatus(manifest, 12)}

    CP-13: QA Validation [PARALLEL AGENTS]
      ${getQAAgentsStatus(manifest)}

      Resume Logic:
      ${getQAAgentsResumeInstructions(manifest)}

    CP-14: UI Audit [AGENT] [BLOCKING]
      Agent: prototype-visual-qa-tester
      Status: ${getAgentStatus(manifest, "prototype-visual-qa-tester")}
      ${getAgentResumeInstructions(manifest, "prototype-visual-qa-tester")}

    ═══════════════════════════════════════════════════════════════════════

    AGENT SPAWN PROTOCOL:

    For each agent that needs spawning:

    1. BEFORE spawning, update manifest:
       {
         "agent_id": "<agent-id>",
         "status": "spawning",
         "spawn_requested_at": "<timestamp>",
         "task_call_id": "<unique-id>"
       }

    2. SPAWN agent with Task() call:
       const result = Task({
         subagent_type: "<agent-type>",
         model: "sonnet" | "haiku",
         description: "<short description>",
         headless: ${manifest.headless_mode},  // Terminal visibility: false=visible, true=hidden
         prompt: \`
           <agent instructions>

           CRITICAL: Register session IMMEDIATELY on start:
           python3 .claude/hooks/agent_coordinator.py --register \\
             --agent-id "<agent-id>" \\
             --agent-type "<agent-type>" \\
             --task-id "<task-id>"
         \`
       });

    3. AFTER spawn returns, verify in manifest:
       - Check if agent status changed to "in_progress"
       - Check if session_id was assigned
       - If not verified within 30s → Agent spawn failed

    4. ON SUCCESS:
       - Mark agent as "completed"
       - Record outputs in manifest
       - Continue to next agent

    5. ON FAILURE:
       - This should not happen (already handled by spawn wrapper)
       - If it does, log error and update manifest

    ═══════════════════════════════════════════════════════════════════════

    ERROR HANDLING:

    - Agent spawn timeout → Already handled by wrapper (3 retries)
    - Agent execution failure → Log to manifest, continue if not blocking
    - Missing dependency → Wait for dependency or fail
    - User intervention required → Exit with clear instructions

    ═══════════════════════════════════════════════════════════════════════

    EXECUTION LOOP (CRITICAL):

    You MUST execute ALL 15 checkpoints (0-14) in a continuous loop:

    ```
    FOR checkpoint = 0 TO 14:
      1. Read current_checkpoint from _state/prototype_progress.json
      2. Execute checkpoint (spawn agent OR do work directly)
      3. Wait for completion
      4. Update _state/prototype_progress.json:
         - current_checkpoint += 1
         - phase status = "completed"
      5. **IMMEDIATELY continue to next checkpoint**
      6. DO NOT STOP between checkpoints
      7. DO NOT generate "Next Steps" summaries between checkpoints
    ENDFOR
    ```

    ═══════════════════════════════════════════════════════════════════════

    STOPPING CONDITIONS:

    ✅ ONLY STOP WHEN:
    - current_checkpoint == 14 AND
    - All agents completed AND
    - Final UI audit passed

    ❌ DO NOT STOP IF:
    - You just completed one checkpoint (there are 15 total!)
    - You wrote a "Next Steps" section (that's informational only)
    - current_checkpoint < 14
    - Any agents still in progress

    ═══════════════════════════════════════════════════════════════════════

    COMPLETION (Only after all 15 checkpoints):

    When ALL checkpoints complete (current_checkpoint == 14):
    1. Update manifest: status = "completed"
    2. Generate final report
    3. Display summary with agent statistics
  `;
}
```

---

## Spawn Manifest Schema

Full JSON schema saved to `_state/agent_spawn_manifest.json`:

```json
{
  "schema_version": "1.0.0",
  "system_name": "EmergencyTriage",
  "started_at": "2026-01-02T20:00:00Z",
  "updated_at": "2026-01-02T21:30:00Z",
  "completed_at": null,
  "mode": "multi_agent",
  "headless_mode": false,
  "orchestrator_session_id": "sess-orch-001",

  "resume_config": {
    "resume_from_checkpoint": null,
    "retry_failed": false,
    "skip_failed": true
  },

  "agents": [
    {
      "agent_id": "prototype-data-model-specifier",
      "agent_type": "prototype-data-model-specifier",
      "checkpoint": 3,
      "phase": "data_model",
      "status": "completed",
      "priority": "normal",
      "blocking": false,

      "spawn_info": {
        "spawn_attempts": 1,
        "max_attempts": 3,
        "task_call_id": "task-dm-1735851234567",
        "session_id": "sess-002",
        "spawn_method": "orchestrator",
        "spawn_requested_at": "2026-01-02T20:35:00Z",
        "spawn_verified_at": "2026-01-02T20:35:02Z",
        "spawn_timeout_seconds": 30
      },

      "execution": {
        "started_at": "2026-01-02T20:35:02Z",
        "completed_at": "2026-01-02T20:45:00Z",
        "duration_seconds": 598,
        "heartbeat_at": "2026-01-02T20:44:55Z"
      },

      "outputs": {
        "expected": [
          "00-foundation/data-model/DATA_MODEL.md",
          "00-foundation/data-model/ENTITY_INDEX.md"
        ],
        "actual": [
          "00-foundation/data-model/DATA_MODEL.md",
          "00-foundation/data-model/ENTITY_INDEX.md",
          "00-foundation/data-model/entities/Patient.schema.json",
          "00-foundation/data-model/entities/Triage.schema.json"
        ]
      },

      "error": {
        "error_message": null,
        "retry_history": [],
        "countermeasure_applied": null
      },

      "dependencies": {
        "depends_on": [],
        "blocks": ["prototype-api-contract-specifier"]
      }
    },

    {
      "agent_id": "prototype-screen-specifier-login",
      "agent_type": "prototype-screen-specifier",
      "checkpoint": 9,
      "phase": "screens",
      "status": "failed",
      "priority": "normal",
      "blocking": false,
      "screen_id": "SCR-001",
      "screen_name": "login",

      "spawn_info": {
        "spawn_attempts": 3,
        "max_attempts": 3,
        "task_call_id": "task-screen-login-1735851567890",
        "session_id": null,
        "spawn_method": null,
        "spawn_requested_at": "2026-01-02T21:05:00Z",
        "spawn_verified_at": null,
        "spawn_timeout_seconds": 30
      },

      "execution": {
        "started_at": null,
        "completed_at": null,
        "duration_seconds": null,
        "heartbeat_at": null
      },

      "outputs": {
        "expected": ["02-screens/login/"],
        "actual": []
      },

      "error": {
        "error_message": "Spawn verification timeout after 3 attempts",
        "retry_history": [
          {
            "attempt": 1,
            "countermeasure": null,
            "error": "No session registered within 30s",
            "timestamp": "2026-01-02T21:05:30Z"
          },
          {
            "attempt": 2,
            "countermeasure": "retry_with_session",
            "error": "No session registered within 30s",
            "timestamp": "2026-01-02T21:06:05Z"
          },
          {
            "attempt": 3,
            "countermeasure": "fallback_general_purpose",
            "error": "No session registered within 30s",
            "timestamp": "2026-01-02T21:06:40Z"
          }
        ],
        "countermeasure_applied": "fallback_general_purpose"
      },

      "dependencies": {
        "depends_on": ["prototype-component-specifier"],
        "blocks": []
      }
    }
  ],

  "phases": {
    "CP-0": { "status": "completed", "agents": [], "completed_at": "2026-01-02T20:10:00Z" },
    "CP-1": { "status": "completed", "agents": [], "completed_at": "2026-01-02T20:30:00Z" },
    "CP-2": { "status": "completed", "agents": [], "completed_at": "2026-01-02T20:35:00Z" },
    "CP-3": {
      "status": "completed",
      "agents": ["prototype-data-model-specifier"],
      "completed_at": "2026-01-02T20:45:00Z"
    },
    "CP-9": {
      "status": "partial",
      "agents": [
        "prototype-screen-specifier-login",
        "prototype-screen-specifier-intake",
        "prototype-screen-specifier-triage",
        "prototype-screen-specifier-dashboard",
        "prototype-screen-specifier-emergency",
        "prototype-screen-specifier-queue",
        "prototype-screen-specifier-display"
      ],
      "completed_agents": 6,
      "failed_agents": 1,
      "completed_at": null
    }
  },

  "statistics": {
    "total_agents_planned": 11,
    "total_agents_completed": 9,
    "total_agents_failed": 1,
    "total_agents_in_progress": 0,
    "total_agents_not_started": 1,
    "total_spawn_attempts": 15,
    "total_spawn_failures": 1,
    "average_spawn_verification_time_ms": 1843
  },

  "blocking": {
    "user_intervention_required": false,
    "blocked_on_agent": null,
    "blocked_reason": null,
    "blocked_at": null
  }
}
```

---

## Helper Scripts

Create `_state/agent_spawn_utils.py` for manifest operations:

```python
#!/usr/bin/env python3
"""
Agent Spawn Manifest Utilities

Provides helper functions for managing agent spawn manifest.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

MANIFEST_PATH = Path("_state/agent_spawn_manifest.json")

def load_manifest():
    """Load spawn manifest from disk."""
    if not MANIFEST_PATH.exists():
        return None
    with open(MANIFEST_PATH) as f:
        return json.load(f)

def save_manifest(manifest):
    """Save spawn manifest to disk."""
    manifest["updated_at"] = datetime.utcnow().isoformat() + "Z"
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

def get_agent_status(agent_id):
    """Get status of specific agent."""
    manifest = load_manifest()
    if not manifest:
        return None

    for agent in manifest["agents"]:
        if agent["agent_id"] == agent_id:
            return agent["status"]
    return None

def update_agent_status(agent_id, status, **kwargs):
    """Update agent status and optional fields."""
    manifest = load_manifest()
    if not manifest:
        print("Error: Manifest not found", file=sys.stderr)
        return False

    for agent in manifest["agents"]:
        if agent["agent_id"] == agent_id:
            agent["status"] = status
            for key, value in kwargs.items():
                if "." in key:
                    # Nested update (e.g., "execution.completed_at")
                    parts = key.split(".")
                    obj = agent
                    for part in parts[:-1]:
                        obj = obj.setdefault(part, {})
                    obj[parts[-1]] = value
                else:
                    agent[key] = value
            break

    save_manifest(manifest)
    return True

def list_agents_by_status(status):
    """List all agents with given status."""
    manifest = load_manifest()
    if not manifest:
        return []

    return [
        agent["agent_id"]
        for agent in manifest["agents"]
        if agent["status"] == status
    ]

def get_resume_plan():
    """Generate resume execution plan."""
    manifest = load_manifest()
    if not manifest:
        return None

    plan = {
        "current_checkpoint": manifest["current_checkpoint"],
        "completed": list_agents_by_status("completed"),
        "failed": list_agents_by_status("failed"),
        "in_progress": list_agents_by_status("in_progress"),
        "not_started": list_agents_by_status("not_started"),
        "blocked": list_agents_by_status("blocked")
    }

    return plan

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: agent_spawn_utils.py <command> [args]")
        print("Commands: status, update, list, resume-plan")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "status":
        agent_id = sys.argv[2]
        status = get_agent_status(agent_id)
        print(status or "not_found")

    elif cmd == "update":
        agent_id = sys.argv[2]
        status = sys.argv[3]
        update_agent_status(agent_id, status)
        print(f"Updated {agent_id} -> {status}")

    elif cmd == "list":
        status = sys.argv[2]
        agents = list_agents_by_status(status)
        for agent in agents:
            print(agent)

    elif cmd == "resume-plan":
        plan = get_resume_plan()
        print(json.dumps(plan, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
```

---

## Usage Examples

### Example 1: New Run (Visible Terminals - Default)

```bash
/prototype-multiagent EmergencyTriage
```

Output:
```
Terminal Mode: ✅ VISIBLE (terminal windows will open)

✅ Multi-Agent Infrastructure: READY
   11 specialized agents available
   Spawn verification: ENABLED
   Retry logic: ENABLED (3 attempts per agent)
   Resume capability: ENABLED

📋 New Run: Initialized spawn manifest

🚀 Spawning Orchestrator Agent...
   Attempt 1/3: Spawning prototype-orchestrator...
   Verifying spawn...
   ✅ Agent spawned successfully
      Session ID: sess-orch-001
      Verified in: 1.2s

[Orchestrator takes over, spawns 11 agents across phases]

═══════════════════════════════════════════════════════
  PROTOTYPE GENERATION COMPLETE (MULTI-AGENT)
═══════════════════════════════════════════════════════

  System:              EmergencyTriage
  Mode:                Multi-Agent
  Orchestrator:        sess-orch-001

  Agents Spawned:      11
  Agents Completed:    11
  Agents Failed:       0
  Total Spawn Attempts: 11
  Average Verification: 1.8s

  Duration:            47 minutes
  Speedup:             ~58% vs sequential
```

### Example 2: New Run (Headless Mode)

```bash
/prototype-multiagent EmergencyTriage --headless
```

Output:
```
Terminal Mode: ❌ HEADLESS (no visible terminals)

✅ Multi-Agent Infrastructure: READY
   11 specialized agents available
   Spawn verification: ENABLED
   Retry logic: ENABLED (3 attempts per agent)
   Resume capability: ENABLED

📋 New Run: Initialized spawn manifest

🚀 Spawning Orchestrator Agent...
   Attempt 1/3: Spawning prototype-orchestrator...
   Verifying spawn...
   ✅ Agent spawned successfully
      Session ID: sess-orch-001
      Verified in: 1.2s

[All agents run in background without visible terminal windows]
```

### Example 3: Resume After Failure

```bash
/prototype-multiagent EmergencyTriage --resume
```

Output:
```
📋 Resume Mode: Loaded spawn manifest
   Started: 2026-01-02T20:00:00Z
   Checkpoint: 9
   Completed: 10/11
   Failed: 1

🚀 Resuming from Checkpoint 9 (Screen Specifications)...

   Analyzing agent states:
   ✅ prototype-screen-specifier-intake (completed)
   ✅ prototype-screen-specifier-triage (completed)
   ✅ prototype-screen-specifier-dashboard (completed)
   ✅ prototype-screen-specifier-emergency (completed)
   ✅ prototype-screen-specifier-queue (completed)
   ✅ prototype-screen-specifier-display (completed)
   ❌ prototype-screen-specifier-login (failed) → SKIPPING

   ⚠️  Warning: 1 agent failed, continuing with available data

   Moving to Checkpoint 10...
```

### Example 4: Retry Failed Agents

```bash
/prototype-multiagent EmergencyTriage --resume --retry-failed
```

Output:
```
📋 Resume Mode: Loaded spawn manifest
   Retry Mode: ENABLED (will retry failed agents)

   Failed agents to retry:
   - prototype-screen-specifier-login (3 previous attempts)

🚀 Retrying Failed Agent: prototype-screen-specifier-login
   Previous failures: 3
   Resetting spawn attempts counter

   Attempt 1/3: Spawning prototype-screen-specifier-login...
   Verifying spawn...
   ✅ Agent spawned successfully
      Session ID: sess-screen-login-002
      Verified in: 2.1s

   ✅ Retry successful! Continuing...
```

### Example 5: Blocked on Agent

```bash
/prototype-multiagent EmergencyTriage --resume
```

Output when blocked:
```
📋 Resume Mode: Loaded spawn manifest

⚠️  USER INTERVENTION REQUIRED
   Blocked on: prototype-design-token-generator
   Reason: Spawn verification timeout after 3 attempts

   To retry: /prototype-multiagent EmergencyTriage --resume --retry-failed
   To skip: Mark agent as 'failed' in manifest, then --resume

[Detailed troubleshooting guide displayed]

Execution halted. Please resolve the issue and resume.
```

---

## Completion Summary

```
═══════════════════════════════════════════════════════════════════════════
  PROTOTYPE GENERATION COMPLETE (MULTI-AGENT)
═══════════════════════════════════════════════════════════════════════════

  System:              EmergencyTriage
  Mode:                Multi-Agent (Robust)
  Terminal Mode:       ${manifest.headless_mode ? "Headless" : "Visible"}
  Discovery:           ClientAnalysis_EmergencyTriage/
  Output:              Prototype_EmergencyTriage/

  ┌─────────────────────────────────────────────────────────────────────┐
  │ AGENT EXECUTION STATISTICS                                          │
  ├─────────────────────────────────────────────────────────────────────┤
  │ Total Agents:            11                                         │
  │ ✅ Completed:            11                                         │
  │ ❌ Failed:               0                                          │
  │ 🔄 Retries:              2                                          │
  │ Total Spawn Attempts:    13                                         │
  │ Avg Verification Time:   1.84s                                      │
  │ Max Verification Time:   4.2s                                       │
  └─────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────┐
  │ PARALLEL EXECUTION METRICS                                          │
  ├─────────────────────────────────────────────────────────────────────┤
  │ CP-9 (Screens):          7 agents in parallel                       │
  │   Sequential estimate:   ~35 minutes                                │
  │   Parallel actual:       ~7 minutes                                 │
  │   Speedup:               5x (80% time saved)                        │
  │                                                                      │
  │ CP-13 (QA):              4 agents in parallel                       │
  │   Sequential estimate:   ~20 minutes                                │
  │   Parallel actual:       ~6 minutes                                 │
  │   Speedup:               3.3x (70% time saved)                      │
  └─────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────┐
  │ TIME BREAKDOWN                                                       │
  ├─────────────────────────────────────────────────────────────────────┤
  │ Total Duration:          47 minutes                                 │
  │ Sequential Estimate:     112 minutes                                │
  │ Time Saved:              65 minutes (58% faster)                    │
  │                                                                      │
  │ Initialization:          3 min                                      │
  │ Agent Execution:         40 min                                     │
  │ Coordination Overhead:   4 min                                      │
  └─────────────────────────────────────────────────────────────────────┘

  📋 Spawn Manifest: _state/agent_spawn_manifest.json
  📊 Agent Sessions:  _state/agent_sessions.json

  Next Steps:
  • /prototype-serve     - Start development server
  • /prototype-export    - Package for ProductSpecs
  • /prototype-feedback  - Process change requests

═══════════════════════════════════════════════════════════════════════════
```

---


---

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype` | Standard prototype (sequential fallback) |
| `/prototype-status` | Show current progress |
| `/verify-agents` | Check agent spawn status |
| `/prototype-serve` | Start dev server |

---

**Status**: Production Ready
**Version**: 1.0.0
**Features**: Spawn verification, retry logic, granular resume, user intervention protocol
