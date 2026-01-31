---
name: prototype-orchestrator
description: Coordination guide for Stage 2 Prototype generation. Provides checkpoint-by-checkpoint execution plans for the main session to spawn specialized agents directly. Coordinates 15 checkpoints from Discovery validation to working prototype with full traceability.
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

# Prototype Orchestrator - Coordination Guide

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh subagent prototype-orchestrator started '{"stage": "prototype", "method": "instruction-based"}'
```

This ensures the subagent start is logged. The end is automatically logged by the global `SubagentStop` hook.

## ⚠️ CRITICAL ARCHITECTURE NOTE

**Due to Claude Code's nested spawning limitation**, this orchestrator **DOES NOT SPAWN SUB-AGENTS DIRECTLY**.

The Task tool cannot be called from within an agent that was itself spawned via Task(). Instead, this orchestrator provides detailed coordination logic that the **main Claude session** uses to spawn agents directly.

**Architecture:**
❌ OLD (nested spawning - doesn't work):
Main Session → Task(orchestrator) → Task(sub-agent) [BLOCKED]

✅ NEW (flat spawning - works):
Main Session ├→ Task(data-model-specifier)
             ├→ Task(api-contract-specifier)
             ├→ Task(component-specifier)
             ├→ Task(screen-specifier)
             └→ Task(ux-validator)

**Your Role**: Provide checkpoint execution specs that the main session uses to spawn agents with proper prompts, inputs, and coordination.

---

## Your Mission

**Provide coordination specifications** for the complete prototype generation pipeline:

1. **Initialize** - Folder structure and state files (CP-0)
2. **Validate** - Discovery completeness check (CP-1) [BLOCKING]
3. **Extract** - Build requirements registry (CP-2)
4. **Specify** - Coordinate 6 specification agents for data, APIs, design, components, screens (CP-3 to CP-9)
5. **Generate** - Coordinate interactions, build sequence, code generation (CP-10 to CP-12)
6. **Validate** - Coordinate 4 validation agents in parallel (CP-13)
7. **Audit** - Final UI audit with Playwright (CP-14) [BLOCKING]

**The main session will execute these checkpoints by reading this guide and spawning agents directly.**

## How Main Session Uses This Guide

### 1. Read Configuration Files

The main session should load:
```bash
# Read state files
_state/prototype_config.json     # System name, paths, headless mode
_state/prototype_progress.json   # Current checkpoint, status
_state/prototype_agent_spawn_manifest.json  # Agent tracking
```

### 2. Execute Checkpoints Sequentially

For each checkpoint from `current_checkpoint` to 14:
1. Read the checkpoint specification below
2. Determine if agent spawn is required (see "Agent Required" field)
3. If yes: Spawn agent(s) using provided Task() specs
4. If no: Execute actions directly in main session
5. Update progress and manifest files
6. Advance to next checkpoint

### 3. Spawn Agents Using Task() Tool (Parallel When Possible)

**CRITICAL**: When multiple agents are needed for a checkpoint, spawn them in **parallel** using a single message with multiple Task() calls.

```javascript
// Example: Single agent spawn (CP-3 Data Model)
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate data model specification",
  prompt: `Agent: prototype-data-model-specifier
Read: .claude/agents/prototype-data-model-specifier.md

System: ${SYSTEM_NAME}
Checkpoint: 3
SESSION: session-data-model-${timestamp}
TASK: ${task_id}

Input: ${DISCOVERY_FOLDER}/04-design-specs/data-fields.md
Output: ${OUTPUT_FOLDER}/00-foundation/data-model/

Generate complete data model specification from Discovery data fields.

RETURN: JSON { status, files_written, issues }`
})

// Example: Parallel agent spawning (CP-13 Validation - 4 agents)
// MUST use single message with multiple Task() calls:
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Validate component compliance",
  prompt: `Agent: prototype-component-validator...`
})
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Validate screen compliance",
  prompt: `Agent: prototype-screen-validator...`
})
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Validate accessibility (WCAG 2.1 AA)",
  prompt: `Agent: prototype-accessibility-auditor...`
})
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Perform visual QA testing",
  prompt: `Agent: prototype-visual-qa-tester...`
})

// All 4 agents execute simultaneously
```

### 4. Log All Activities (MANDATORY)

Before and after each checkpoint, call hooks:

```bash
# Before checkpoint
# Logging handled via FIRST ACTION hook
# After checkpoint success
  --command-name "prototype-checkpoint-${N}" \
  --stage "prototype" \
  --status "completed" \
  --start-event-id "${CHECKPOINT_EVENT_ID}" \
```

### 5. Update Progress After Each Checkpoint

```javascript
// Update _state/prototype_progress.json
const progress = {
  current_checkpoint: checkpointNumber + 1,
  phases: {
    [`${checkpointNumber}_${phaseName}`]: {
      status: "completed",
      completed_at: new Date().toISOString(),
      outputs: [...outputFiles]
    }
  },
  overall_progress: ((checkpointNumber + 1) / 15) * 100,
  last_updated: new Date().toISOString()
};

writeFile("_state/prototype_progress.json", JSON.stringify(progress, null, 2));
```

## Checkpoint Execution Plans

### CP-0: Initialize

**Executor**: You (direct execution, no agent spawn)

**Actions**:
1. Create folder structure using Bash:
   ```bash
   mkdir -p ${OUTPUT_FOLDER}/{00-foundation,01-components,02-screens,03-interactions,04-implementation,05-validation}
   mkdir -p ${OUTPUT_FOLDER}/00-foundation/{design-tokens,data-model,api-contracts}
   mkdir -p ${OUTPUT_FOLDER}/01-components/specs
   mkdir -p ${OUTPUT_FOLDER}/05-validation/reports
   ```

2. Initialize `_state/prototype_config.json` (if not exists)

3. Initialize `_state/prototype_progress.json`:
   ```json
   {
     "current_checkpoint": 1,
     "phases": {
       "0_initialize": {
         "status": "completed",
         "completed_at": "2026-01-10T...",
         "outputs": ["${OUTPUT_FOLDER}/"]
       }
     },
     "overall_progress": 6.67,
     "last_updated": "2026-01-10T..."
   }
   ```

4. Call hooks to log initialization

**Outputs**: Folder structure created

---

### CP-1: Validate Discovery [BLOCKING]

**Executor**: You (direct execution)

**Actions**:
1. Read `${DISCOVERY_FOLDER}/_state/discovery_progress.json`
2. Verify `current_checkpoint >= 11`
3. **BLOCK if validation fails** - return error and exit
4. Extract summary:
   - Read all Discovery artifacts
   - Extract screens list, personas, JTBD
   - Write to `_state/discovery_summary.json`

**Validation**:
```javascript
if (discoveryCheckpoint < 11) {
  throw new Error(`Discovery incomplete. Expected CP >= 11, got ${discoveryCheckpoint}`);
}
```

**Outputs**:
- `_state/discovery_summary.json`

---

### CP-2: Extract Requirements

**Executor**: You (direct execution)

**Actions**:
1. Read Discovery files:
   - `${DISCOVERY_FOLDER}/02-research/PAIN_POINTS_VALIDATED.md`
   - `${DISCOVERY_FOLDER}/02-research/JOBS_TO_BE_DONE.md`
   - `${DISCOVERY_FOLDER}/04-design-specs/SCREEN_DEFINITIONS.md`

2. Transform to requirements format:
   ```json
   {
     "requirements": [
       {
         "id": "REQ-001",
         "priority": "P0",
         "category": "Authentication",
         "description": "...",
         "source_pain_point": "PP-X.X",
         "source_jtbd": "JTBD-X.X",
         "screens": ["SCR-001"],
         "acceptance_criteria": [...]
       }
     ]
   }
   ```

3. Write to `_state/requirements_registry.json`

**Outputs**:
- `_state/requirements_registry.json` (35+ requirements expected)

---

### CP-3: Data Model

**Executor**: AGENT (prototype-data-model-specifier)

**Spawn Command**:
```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate data model specification",
  prompt: `Agent: prototype-data-model-specifier
Read: .claude/agents/prototype-data-model-specifier.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 3
INPUT: ${DISCOVERY_FOLDER}/04-design-specs/data-fields.md
OUTPUT: ${OUTPUT_FOLDER}/00-foundation/data-model/

Generate complete data model specification including:
- Entity definitions (ENT-XXX)
- Relationships and foreign keys
- Validation rules
- Enum definitions
- TypeScript interfaces
- API types

REQUIREMENTS:
- Minimum 3 core entities
- All relationships documented
- Validation rules for each field
- Traceability to Discovery

RETURN: JSON status report with created files`
});
```

**Expected Outputs**:
- `00-foundation/data-model/DATA_MODEL.md`
- `00-foundation/data-model/ENTITY_INDEX.md`

---

### CP-4: API Contracts

**Executor**: AGENT (prototype-api-contract-specifier)

**Prerequisites**: CP-3 completed

**Spawn Command**:
```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate API contract specifications",
  prompt: `Agent: prototype-api-contract-specifier
Read: .claude/agents/prototype-api-contract-specifier.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 4
INPUT: ${OUTPUT_FOLDER}/00-foundation/data-model/DATA_MODEL.md
INPUT: ${DISCOVERY_FOLDER}/04-design-specs/SCREEN_DEFINITIONS.md
OUTPUT: ${OUTPUT_FOLDER}/00-foundation/api-contracts/

Generate OpenAPI 3.0 specification including:
- REST endpoints for all entities (CRUD)
- WebSocket events for real-time updates
- Request/response schemas
- Error codes and handling
- Authentication placeholders

RETURN: JSON status report with created files`
});
```

**Expected Outputs**:
- `00-foundation/api-contracts/openapi.json`
- `00-foundation/api-contracts/websockets.md`

---

### CP-5: Test Data

**Executor**: You (direct execution)

**Actions**:
1. Read data model entities
2. Generate realistic test data files (JSON)
3. Create folder: `${OUTPUT_FOLDER}/test-data/`
4. Write files:
   - `patients.json` (15-20 records)
   - `users.json` (5-10 staff members)
   - `triage-records.json` (20-30 records)
   - Entity-specific data files

**Outputs**:
- `test-data/*.json` (multiple files)

---

### CP-6-7: Design Foundations (Combined)

**Executor**: AGENT (prototype-design-token-generator)

**Spawn Command**:
```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate design token system",
  prompt: `Agent: prototype-design-token-generator
Read: .claude/agents/prototype-design-token-generator.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINTS: 6-7 (combined)
INPUT: ${DISCOVERY_FOLDER}/04-design-specs/
OUTPUT: ${OUTPUT_FOLDER}/00-foundation/design-tokens/

Generate comprehensive design token system:
- Color palette (primary, semantic, medical colors)
- Typography scale (responsive)
- Spacing system (8px grid)
- Shadow definitions
- Border radius values
- Animation tokens

REQUIREMENTS:
- WCAG AA contrast ratios
- Emergency medical color coding (red=critical, yellow=urgent)
- Tailwind-compatible JSON format

RETURN: JSON status report with created files`
});
```

**Expected Outputs**:
- `00-foundation/design-tokens/tokens.json`
- `00-foundation/design-tokens/colors.md`
- `00-foundation/design-tokens/typography.md`

---

### CP-8: Components

**Executor**: AGENT (prototype-component-specifier)

**Prerequisites**: CP-6-7 completed

**Spawn Command**:
```javascript
const assemblyFirst = config.assembly_first?.enabled || false;

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate component specifications",
  prompt: `Agent: prototype-component-specifier
Read: .claude/agents/prototype-component-specifier.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 8
ASSEMBLY_FIRST: ${assemblyFirst}
INPUT: ${DISCOVERY_FOLDER}/04-design-specs/SCREEN_DEFINITIONS.md
INPUT: ${OUTPUT_FOLDER}/00-foundation/design-tokens/tokens.json
${assemblyFirst ? 'INPUT: .claude/templates/component-library/manifests/components.json' : ''}
OUTPUT: ${OUTPUT_FOLDER}/01-components/

${assemblyFirst ? `
ASSEMBLY-FIRST MODE:
1. Read component library manifest
2. Map Discovery screens to library components
3. Identify ONLY aggregate components (combining library components with business logic)
4. Generate specs for aggregate components only

DO NOT create specs for Button, TextField, Select, Table, etc. (use library)
CREATE specs for: KPICard, PatientCard, TriageForm, etc. (custom business logic)
` : `
TRADITIONAL MODE:
1. Extract all UI components from screens
2. Categorize and define props, variants, states
3. Specify accessibility requirements
4. Create complete component library
`}

RETURN: JSON status report with created files`
});
```

**Expected Outputs**:
- `01-components/component-index.md`
- `01-components/specs/*.md` (component specifications)

---

### CP-9: Screens (PARALLEL)

**Executor**: AGENTS (prototype-screen-specifier, one per screen) **IN PARALLEL**

**Prerequisites**: CP-8 completed

**Parallel Spawn Logic**:
```javascript
// Read discovery summary to get screen list
const discoverySummary = JSON.parse(readFile("_state/discovery_summary.json"));
const screens = discoverySummary.screens; // e.g., 7 screens

// Spawn one agent per screen IN PARALLEL
const screenTasks = screens.map(screen => {
  return Task({
    subagent_type: "general-purpose",
    model: "sonnet",
    description: `Generate ${screen.name} screen spec`,
    prompt: `Agent: prototype-screen-specifier
Read: .claude/agents/prototype-screen-specifier.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 9
SCREEN: ${screen.id} - ${screen.name}
INPUT: ${DISCOVERY_FOLDER}/04-design-specs/SCREEN_DEFINITIONS.md (section ${screen.id})
INPUT: ${OUTPUT_FOLDER}/01-components/component-index.md
INPUT: ${OUTPUT_FOLDER}/00-foundation/data-model/DATA_MODEL.md
OUTPUT: ${OUTPUT_FOLDER}/02-screens/${screen.slug}/

Generate detailed screen specification:
- Map screen sections to components
- Define layout structure (grid/flex, responsive)
- Specify state management
- Define data fetching/mutations
- Document user flows
- List accessibility requirements

RETURN: JSON status report with created files`
  });
});

// IMPORTANT: Do NOT wait here - let them run in parallel
// Claude Code will handle parallel execution automatically
```

**Expected Outputs**:
- `02-screens/{screen-slug}/spec.md` (7 folders, one per screen)
- `02-screens/{screen-slug}/layout.md`
- `02-screens/{screen-slug}/data-requirements.md`

---

### CP-9.5: REVIEW GATE [USER APPROVAL REQUIRED]

**Executor**: You (direct execution with AskUserQuestion)

**Trigger**: After CP-9 completes (all prep work done)

**Purpose**: Guide user to review all generated artifacts before proceeding to build phase

**Actions**:
```javascript
// Present review options to user
const reviewResponse = await AskUserQuestion({
  questions: [{
    question: "Prototype preparation complete! Please review the following artifacts before I proceed to build the prototype. Which artifacts would you like to review now?",
    header: "Review",
    multiSelect: true,
    options: [
      {
        label: "Data Model (8 entities)",
        description: `Review the data model at: ${OUTPUT_FOLDER}/00-foundation/data-model/DATA_MODEL.md`
      },
      {
        label: "API Contracts (25 endpoints)",
        description: `Review API specifications at: ${OUTPUT_FOLDER}/00-foundation/api-contracts/openapi.json`
      },
      {
        label: "Design Tokens (colors, typography, spacing)",
        description: `Review design system at: ${OUTPUT_FOLDER}/00-foundation/design-tokens/tokens.json`
      },
      {
        label: "Component Specifications (15 components)",
        description: `Review component specs at: ${OUTPUT_FOLDER}/01-components/`
      },
      {
        label: "Screen Specifications (7 screens)",
        description: `Review screen specs at: ${OUTPUT_FOLDER}/02-screens/`
      },
      {
        label: "Requirements Registry (traceability)",
        description: `Review requirements mapping at: _state/requirements_registry.json`
      }
    ]
  }]
});

// Log selected reviews
const selectedReviews = reviewResponse.answers["0"] || [];
console.log(`✅ User reviewed: ${selectedReviews.join(", ")}`);

// Ask for approval to proceed
const approvalResponse = await AskUserQuestion({
  questions: [{
    question: "After reviewing the artifacts, would you like me to proceed with building the prototype? This will create implementation tasks and generate React code using TDD approach with 2 parallel development teams.",
    header: "Approval",
    multiSelect: false,
    options: [
      {
        label: "Yes, proceed to build (Recommended)",
        description: "Start the build phase with task planning, TDD implementation, and parallel teams"
      },
      {
        label: "No, let me make changes first",
        description: "Stop here so you can modify artifacts before building"
      },
      {
        label: "Skip to validation only",
        description: "Skip build phase and run validation on existing code (if prototype already built)"
      }
    ]
  }]
});

const approval = approvalResponse.answers["0"];

if (approval === "No, let me make changes first") {
  console.log("⏸️ Build paused. Run /prototype-resume when ready to continue.");
  updateProgress("current_checkpoint", "9.5");
  updateProgress("phases.review_gate.status", "paused");
  updateProgress("phases.review_gate.user_action_required", true);
  return; // STOP execution
}

if (approval === "Skip to validation only") {
  console.log("⏭️ Skipping build phase. Jumping to CP-13 (Validation).");
  updateProgress("current_checkpoint", 13);
  updateProgress("phases.review_gate.status", "completed");
  updateProgress("phases.review_gate.user_choice", "skip_to_validation");
  // Continue to CP-13
  return;
}

// User approved - continue to CP-10
console.log("✅ User approved. Proceeding to build phase.");
updateProgress("phases.review_gate.status", "completed");
updateProgress("phases.review_gate.user_choice", "proceed_to_build");
updateProgress("current_checkpoint", 10);
```

**Expected User Flow**:
1. User reviews selected artifacts in file system
2. User makes any necessary changes if needed
3. User confirms approval to proceed
4. Orchestrator continues to CP-10 (Planning phase)

**BLOCKING**: This checkpoint BLOCKS until user provides approval. Do not proceed without explicit "Yes" response.

---

### CP-10: Planning Phase

**Executor**: AGENT (prototype-planner)

**Prerequisites**: CP-9.5 approved (user gave go-ahead)

**Spawn Command**:
```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Decompose prototype into evolutionary tasks",
  prompt: `Agent: prototype-planner
Read: .claude/agents/prototype-planner.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 10
INPUT: ${OUTPUT_FOLDER}/02-screens/
INPUT: ${OUTPUT_FOLDER}/01-components/
INPUT: ${OUTPUT_FOLDER}/00-foundation/
OUTPUT: ${OUTPUT_FOLDER}/04-implementation/BUILD_PLAN.md
OUTPUT: ${OUTPUT_FOLDER}/04-implementation/task_registry.json
OUTPUT: ${OUTPUT_FOLDER}/04-implementation/GANTT.mermaid

Decompose all screen specifications into small, evolutionary implementation tasks.

REQUIREMENTS:
- Create tasks for each screen (layout → sections → integration)
- Mark tasks as sequential [S] or parallel [P]
- Balance task load across 2 teams
- Generate TDD specifications for each task (RED-GREEN-REFACTOR)
- Include Assembly-First mode detection
- Classify components (library vs aggregate)

RETURN: JSON status report with task count and file paths`
});
```

**Expected Outputs**:
- `04-implementation/BUILD_PLAN.md` (human-readable plan)
- `04-implementation/task_registry.json` (machine-readable tasks)
- `04-implementation/GANTT.mermaid` (visual timeline)

---

### CP-11: Team-Based TDD Implementation (LOOP)

**Executor**: You (orchestrator with 2 developer + 2 tester agents in parallel)

**Prerequisites**: CP-10 completed (task registry exists)

**Architecture**:
- **2 Teams**: Team A (developer-1 + tester-1), Team B (developer-2 + tester-2)
- **TDD Cycle**: RED → GREEN → REFACTOR for each task
- **Parallel Execution**: Both teams work simultaneously on independent tasks
- **File Locking**: Prevents concurrent writes to same files

**Implementation Loop**:
```javascript
// Load task registry
const taskRegistry = JSON.parse(readFile(`${OUTPUT_FOLDER}/04-implementation/task_registry.json`));
let incompleteTasks = taskRegistry.tasks.filter(t => t.status !== "completed");

while (incompleteTasks.length > 0) {
  // 1. SELECT TASKS: Get next available tasks for each team
  const availableTasksTeamA = incompleteTasks.filter(t =>
    t.parallel_marker === "[P]" &&
    t.depends_on.every(depId => taskRegistry.tasks.find(dep => dep.id === depId)?.status === "completed") &&
    t.team_assignment === "team-a" &&
    !t.file_lock
  );

  const availableTasksTeamB = incompleteTasks.filter(t =>
    t.parallel_marker === "[P]" &&
    t.depends_on.every(depId => taskRegistry.tasks.find(dep => dep.id === depId)?.status === "completed") &&
    t.team_assignment === "team-b" &&
    !t.file_lock
  );

  const nextTaskA = availableTasksTeamA[0] || incompleteTasks.find(t => t.parallel_marker === "[S]" && t.depends_on.length === 0);
  const nextTaskB = availableTasksTeamB[0];

  if (!nextTaskA && !nextTaskB) {
    console.log("⚠️ No tasks available (waiting on dependencies)");
    break;
  }

  // 2. SPAWN DEVELOPERS: Launch both teams in parallel
  const developerTasks = [];

  if (nextTaskA) {
    console.log(`🏗️ Team A starting: ${nextTaskA.id} - ${nextTaskA.title}`);
    developerTasks.push(
      Task({
        subagent_type: "general-purpose",
        model: "sonnet",
        description: `Team A: Implement ${nextTaskA.title}`,
        prompt: `Agent: prototype-developer-1
Read: .claude/agents/prototype-developer.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 11
TEAM: team-a
TASK: ${nextTaskA.id}
INPUT: ${OUTPUT_FOLDER}/04-implementation/task_registry.json
INPUT: ${OUTPUT_FOLDER}/02-screens/${nextTaskA.screen}/
OUTPUT: ${OUTPUT_FOLDER}/04-implementation/src/
OUTPUT: ${OUTPUT_FOLDER}/04-implementation/__tests__/

Execute TDD cycle (RED-GREEN-REFACTOR) for task ${nextTaskA.id}.

TDD SPEC:
${JSON.stringify(nextTaskA.tdd_spec, null, 2)}

RETURN: JSON { status: "completed", files_written: [], test_file: "", implementation_file: "" }`
      })
    );
  }

  if (nextTaskB) {
    console.log(`🏗️ Team B starting: ${nextTaskB.id} - ${nextTaskB.title}`);
    developerTasks.push(
      Task({
        subagent_type: "general-purpose",
        model: "sonnet",
        description: `Team B: Implement ${nextTaskB.title}`,
        prompt: `Agent: prototype-developer-2
Read: .claude/agents/prototype-developer.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 11
TEAM: team-b
TASK: ${nextTaskB.id}
INPUT: ${OUTPUT_FOLDER}/04-implementation/task_registry.json
INPUT: ${OUTPUT_FOLDER}/02-screens/${nextTaskB.screen}/
OUTPUT: ${OUTPUT_FOLDER}/04-implementation/src/
OUTPUT: ${OUTPUT_FOLDER}/04-implementation/__tests__/

Execute TDD cycle (RED-GREEN-REFACTOR) for task ${nextTaskB.id}.

TDD SPEC:
${JSON.stringify(nextTaskB.tdd_spec, null, 2)}

RETURN: JSON { status: "completed", files_written: [], test_file: "", implementation_file: "" }`
      })
    );
  }

  // Wait for developers to complete (Claude Code handles parallel execution)
  const developerResults = await Promise.all(developerTasks);

  // 3. SPAWN TESTERS: Validate completed implementations
  const testerTasks = [];

  if (nextTaskA && developerResults[0]?.status === "completed") {
    console.log(`✅ Team A developer done. Starting tester...`);
    testerTasks.push(
      Task({
        subagent_type: "general-purpose",
        model: "haiku",  // Fast validation
        description: `Team A: Validate ${nextTaskA.title}`,
        prompt: `Agent: prototype-tester-1
Read: .claude/agents/prototype-tester.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 11
TEAM: team-a
TASK: ${nextTaskA.id}
INPUT: ${OUTPUT_FOLDER}/04-implementation/src/${developerResults[0].implementation_file}
INPUT: ${OUTPUT_FOLDER}/04-implementation/__tests__/${developerResults[0].test_file}
OUTPUT: ${OUTPUT_FOLDER}/04-implementation/validation/${nextTaskA.id}_validation.md

Perform 4-check validation:
1. Specification Compliance
2. Test Coverage (>80%)
3. Accessibility (WCAG AA)
4. Integration (Smoke Test)

RETURN: JSON { status: "passed" | "failed", issues: [] }`
      })
    );
  }

  const nextTaskBIndex = nextTaskB ? (nextTaskA ? 1 : 0) : -1;
  if (nextTaskB && developerResults[nextTaskBIndex]?.status === "completed") {
    console.log(`✅ Team B developer done. Starting tester...`);
    testerTasks.push(
      Task({
        subagent_type: "general-purpose",
        model: "haiku",
        description: `Team B: Validate ${nextTaskB.title}`,
        prompt: `Agent: prototype-tester-2
Read: .claude/agents/prototype-tester.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 11
TEAM: team-b
TASK: ${nextTaskB.id}
INPUT: ${OUTPUT_FOLDER}/04-implementation/src/${developerResults[nextTaskBIndex].implementation_file}
INPUT: ${OUTPUT_FOLDER}/04-implementation/__tests__/${developerResults[nextTaskBIndex].test_file}
OUTPUT: ${OUTPUT_FOLDER}/04-implementation/validation/${nextTaskB.id}_validation.md

Perform 4-check validation:
1. Specification Compliance
2. Test Coverage (>80%)
3. Accessibility (WCAG AA)
4. Integration (Smoke Test)

RETURN: JSON { status: "passed" | "failed", issues: [] }`
      })
    );
  }

  // Wait for testers to complete
  const testerResults = await Promise.all(testerTasks);

  // 4. UPDATE REGISTRY: Mark tasks complete or blocked
  if (nextTaskA) {
    const testerResult = testerResults[0];
    if (testerResult.status === "passed") {
      updateTaskStatus(nextTaskA.id, "completed");
      console.log(`✅ Task ${nextTaskA.id} completed by Team A`);
    } else {
      updateTaskStatus(nextTaskA.id, "blocked", testerResult.issues);
      console.log(`❌ Task ${nextTaskA.id} blocked: ${testerResult.issues.join(", ")}`);
    }
  }

  if (nextTaskB) {
    const testerResultIndex = nextTaskA ? 1 : 0;
    const testerResult = testerResults[testerResultIndex];
    if (testerResult.status === "passed") {
      updateTaskStatus(nextTaskB.id, "completed");
      console.log(`✅ Task ${nextTaskB.id} completed by Team B`);
    } else {
      updateTaskStatus(nextTaskB.id, "blocked", testerResult.issues);
      console.log(`❌ Task ${nextTaskB.id} blocked: ${testerResult.issues.join(", ")}`);
    }
  }

  // 5. RELOAD: Get updated task list for next iteration
  const updatedRegistry = JSON.parse(readFile(`${OUTPUT_FOLDER}/04-implementation/task_registry.json`));
  incompleteTasks = updatedRegistry.tasks.filter(t => t.status !== "completed");

  console.log(`📊 Progress: ${updatedRegistry.tasks.filter(t => t.status === "completed").length}/${updatedRegistry.tasks.length} tasks completed`);
}

// All tasks completed
console.log("✅ All implementation tasks completed!");
updateProgress("current_checkpoint", 12);
```

**Expected Outputs**:
- `04-implementation/src/components/**/*.tsx` (React components)
- `04-implementation/src/pages/**/*.tsx` (Next.js pages)
- `04-implementation/__tests__/**/*.test.tsx` (Test files)
- `04-implementation/validation/*.md` (Validation reports)
- Updated `task_registry.json` with completed tasks

---

### CP-12: Integration & App Shell

**Executor**: You (direct execution)

**Prerequisites**: CP-11 completed (all tasks done)

**Purpose**: Wire up all implemented components/screens into a working application

**Actions**:
1. **Setup Router**:
   ```typescript
   // Generate src/App.tsx
   import { BrowserRouter, Routes, Route } from 'react-router-dom';
   import { Dashboard } from './pages/Dashboard';
   import { InventoryList } from './pages/InventoryList';
   // ... other imports

   export function App() {
     return (
       <BrowserRouter>
         <Routes>
           <Route path="/" element={<Dashboard />} />
           <Route path="/inventory" element={<InventoryList />} />
           <Route path="/inventory/:id" element={<InventoryDetail />} />
           {/* ... other routes */}
         </Routes>
       </BrowserRouter>
     );
   }
   ```

2. **Create App Layout** (if not already done by tasks):
   ```typescript
   // Generate src/components/AppLayout.tsx
   import { Outlet } from 'react-router-dom';
   import { Header, NavigationMenu } from '@/component-library';

   export function AppLayout() {
     return (
       <div className="min-h-screen bg-canvas">
         <Header logo={<Logo />} user={{ name: 'User' }} />
         <div className="flex">
           <NavigationMenu items={navItems} />
           <main className="flex-1 p-8">
             <Outlet />
           </main>
         </div>
       </div>
     );
   }
   ```

3. **Add Data Providers** (React Query setup):
   ```typescript
   // Generate src/main.tsx
   import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
   const queryClient = new QueryClient();

   ReactDOM.createRoot(document.getElementById('root')!).render(
     <React.StrictMode>
       <QueryClientProvider client={queryClient}>
         <App />
       </QueryClientProvider>
     </React.StrictMode>
   );
   ```

4. **Add Mock Data** (copy from test data):
   ```bash
   cp -r ${OUTPUT_FOLDER}/00-foundation/test-data/* ${OUTPUT_FOLDER}/04-implementation/src/data/mock/
   ```

5. **Generate Configuration Files** (if not exists):
   - `package.json` (dependencies: react, vite, tailwindcss, react-router-dom, @tanstack/react-query)
   - `tsconfig.json` (strict TypeScript config)
   - `vite.config.ts` (path aliases, component library alias)
   - `tailwind.config.js` (design tokens imported)

6. **Run Build Test**:
   ```bash
   cd ${OUTPUT_FOLDER}/04-implementation
   npm install
   npm run build
   ```

7. **Generate Start Instructions**:
   ```markdown
   # ${SYSTEM_NAME} Prototype - Setup Instructions

   ## Installation

   \`\`\`bash
   cd Prototype_${SYSTEM_NAME}/04-implementation
   npm install
   \`\`\`

   ## Development Server

   \`\`\`bash
   npm run dev
   \`\`\`

   Application will be available at: http://localhost:5173

   ## Available Screens

   - Dashboard: http://localhost:5173/
   - Inventory List: http://localhost:5173/inventory
   - Inventory Detail: http://localhost:5173/inventory/:id
   ... (all screens)

   ## Build for Production

   \`\`\`bash
   npm run build
   npm run preview
   \`\`\`

   ## Testing

   \`\`\`bash
   npm run test
   npm run test:coverage
   \`\`\`

   ## Architecture

   - **Framework**: React + Vite
   - **Routing**: React Router v6
   - **State**: React Query
   - **Styling**: Tailwind CSS + Design Tokens
   - **Components**: React Aria Components (Assembly-First)
   - **Testing**: Vitest + React Testing Library
   ```

**Expected Outputs**:
- `04-implementation/src/App.tsx` (router setup)
- `04-implementation/src/main.tsx` (entry point with providers)
- `04-implementation/src/components/AppLayout.tsx` (app shell)
- `04-implementation/package.json` (dependencies)
- `04-implementation/vite.config.ts` (build config)
- `04-implementation/tailwind.config.js` (theme config)
- `04-implementation/README.md` (setup instructions)

**Validation**:
```bash
# Verify build succeeds
cd ${OUTPUT_FOLDER}/04-implementation
npm run build

# If build fails, log errors but continue to CP-13
if [ $? -ne 0 ]; then
  echo "⚠️ Build failed. Logging errors..."
  npm run build 2>&1 | tee ${OUTPUT_FOLDER}/04-implementation/build-errors.log
fi
```

---

### CP-13: Validation (PARALLEL)

**Executor**: AGENTS (4 validators in parallel)

**Prerequisites**: CP-12 completed

**Parallel Spawn Logic**:
```javascript
// Spawn all 4 validators IN PARALLEL
const validationTasks = [
  Task({
    subagent_type: "general-purpose",
    model: "haiku",  // Simple validation, use cheaper model
    description: "Validate component specifications",
    prompt: `Agent: prototype-component-validator
Read: .claude/agents/prototype-component-validator.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 13.1
INPUT: ${OUTPUT_FOLDER}/01-components/
OUTPUT: ${OUTPUT_FOLDER}/05-validation/component-validation.md

Validate all component specs for completeness, consistency, and coverage.

RETURN: JSON status report`
  }),

  Task({
    subagent_type: "general-purpose",
    model: "haiku",
    description: "Validate screen specifications",
    prompt: `Agent: prototype-screen-validator
Read: .claude/agents/prototype-screen-validator.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 13.2
INPUT: ${OUTPUT_FOLDER}/02-screens/
OUTPUT: ${OUTPUT_FOLDER}/05-validation/screen-validation.md

Validate all screen specs match Discovery requirements.

RETURN: JSON status report`
  }),

  Task({
    subagent_type: "general-purpose",
    model: "haiku",
    description: "Validate UX consistency",
    prompt: `Agent: prototype-ux-validator
Read: .claude/agents/prototype-ux-validator.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 13.3
INPUT: ${OUTPUT_FOLDER}/02-screens/
INPUT: ${OUTPUT_FOLDER}/03-interactions/
OUTPUT: ${OUTPUT_FOLDER}/05-validation/ux-validation.md

Validate UX patterns and interaction consistency.

RETURN: JSON status report`
  }),

  Task({
    subagent_type: "general-purpose",
    model: "sonnet",  // More complex analysis
    description: "Audit WCAG compliance",
    prompt: `Agent: prototype-accessibility-auditor
Read: .claude/agents/prototype-accessibility-auditor.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 13.4
INPUT: ${OUTPUT_FOLDER}/
OUTPUT: ${OUTPUT_FOLDER}/05-validation/accessibility-report.md

Audit WCAG 2.1 AA compliance across all screens and components.

RETURN: JSON status report with pass/fail status`
  })
];

// Let them run in parallel - Claude Code handles coordination
```

**Expected Outputs**:
- `05-validation/component-validation.md`
- `05-validation/screen-validation.md`
- `05-validation/ux-validation.md`
- `05-validation/accessibility-report.md`

---

### CP-14: UI Audit [BLOCKING]

**Executor**: AGENT (prototype-visual-qa-tester)

**Prerequisites**: CP-13 completed (all validators passed)

**Spawn Command**:
```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Perform visual QA testing",
  prompt: `Agent: prototype-visual-qa-tester
Read: .claude/agents/prototype-visual-qa-tester.md

SYSTEM: ${SYSTEM_NAME}
CHECKPOINT: 14 (FINAL)
INPUT: ${OUTPUT_FOLDER}/05-validation/
INPUT: ${OUTPUT_FOLDER}/04-implementation/
OUTPUT: ${OUTPUT_FOLDER}/05-validation/ui-audit-report.md
OUTPUT: ${OUTPUT_FOLDER}/05-validation/screenshots/

Perform comprehensive visual QA audit:
1. Launch prototype with Playwright
2. Capture screenshots of all screens (mobile, tablet, desktop)
3. Compare against design specifications
4. Verify WCAG compliance
5. Generate final audit report

REQUIREMENTS:
- All screens captured and tested
- Responsive tests at 3 breakpoints
- Accessibility tests (contrast, keyboard, screen reader)
- BLOCKING: Must pass WCAG AA

RETURN: JSON status report with APPROVED or NEEDS_WORK`
});
```

**BLOCKING Gate**:
```javascript
const auditReport = JSON.parse(readFile(`${OUTPUT_FOLDER}/05-validation/ui-audit-report.json`));

if (auditReport.status !== "APPROVED") {
  throw new Error(`UI audit failed. Fix issues before proceeding:\n${JSON.stringify(auditReport.issues, null, 2)}`);
}
```

**Expected Outputs**:
- `05-validation/ui-audit-report.md`
- `05-validation/ui-audit-report.json`
- `05-validation/screenshots/*.png` (all screens, all breakpoints)

---

## Completion Criteria

The prototype generation is **COMPLETE** when:

✅ All 15 checkpoints executed (CP-0 through CP-14)
✅ All agents completed successfully
✅ All expected files created
✅ All validation checks passed
✅ WCAG AA compliance achieved
✅ Final UI audit status = APPROVED

## Error Handling

### Checkpoint Failure

If a checkpoint fails:
1. Log error to `_state/FAILURES_LOG.md`
2. Update checkpoint status to "failed" in progress.json
3. **STOP execution** - do not proceed to next checkpoint
4. Return clear error message with:
   - Failed checkpoint number and name
   - Error details
   - Resolution steps
   - Files to check

### Agent Failure

If an agent fails:
1. Log agent error with full context
2. Check retry count (max 3 attempts)
3. If retries exhausted:
   - Mark checkpoint as failed
   - Stop pipeline
   - Provide diagnostics

### Blocking Gate Failure

If a blocking gate fails (CP-1, CP-14):
1. Log blocking failure
2. **STOP immediately** - do not continue
3. Return actionable error message
4. Suggest remediation steps

## State Management

### Progress Tracking

Update `_state/prototype_progress.json` after EVERY checkpoint:

```json
{
  "current_checkpoint": 5,
  "phases": {
    "0_initialize": {
      "status": "completed",
      "completed_at": "2026-01-10T17:56:00Z",
      "outputs": ["Prototype_EmergencyTriage/"]
    },
    "1_validate_discovery": {
      "status": "completed",
      "completed_at": "2026-01-10T17:57:00Z",
      "outputs": ["_state/discovery_summary.json"]
    },
    "2_requirements": {
      "status": "completed",
      "completed_at": "2026-01-10T17:59:00Z",
      "outputs": ["_state/requirements_registry.json"]
    },
    "3_data_model": {
      "status": "completed",
      "completed_at": "2026-01-10T18:05:00Z",
      "outputs": ["00-foundation/data-model/DATA_MODEL.md"]
    },
    "4_api_contracts": {
      "status": "completed",
      "completed_at": "2026-01-10T18:10:00Z",
      "outputs": ["00-foundation/api-contracts/openapi.json"]
    }
  },
  "overall_progress": 33.33,
  "last_updated": "2026-01-10T18:10:00Z"
}
```

### Activity Logging

All activities are logged automatically via deterministic lifecycle logging to `_state/lifecycle.json`:

```bash
# Log checkpoint start
# Logging handled via FIRST ACTION hook
# Log agent spawn
python3 _state/spawn_agent_with_logging.py \
  --action spawn \
  --stage "prototype" \
  --system-name "EmergencyTriage" \
  --agent-type "prototype-data-model-specifier" \
  --task-id "task-abc123" \
  --checkpoint 3

# Log agent completion
python3 _state/spawn_agent_with_logging.py \
  --action complete \
  --stage "prototype" \
  --system-name "EmergencyTriage" \
  --agent-type "prototype-data-model-specifier" \
  --task-id "task-abc123" \
  --checkpoint 3 \
  --status "completed" \

# Log checkpoint end
  --command-name "prototype-checkpoint-3" \
  --stage "prototype" \
  --status "completed" \
  --start-event-id "${CHECKPOINT_EVENT_ID}" \
```

## Final Report

At completion (CP-14), generate a final summary:

```markdown
# Prototype Generation Complete

**System**: ${SYSTEM_NAME}
**Duration**: ${totalDuration}
**Checkpoints**: 15/15 completed
**Status**: ✅ APPROVED

## Outputs Generated

### Foundation (CP-0 to CP-7)
- [x] Data model: 8 entities
- [x] API contracts: 25 endpoints
- [x] Design tokens: Complete system
- [x] Test data: 50+ records

### Specifications (CP-8 to CP-9)
- [x] Components: 15 specified (5 aggregate, 10 library)
- [x] Screens: 7 fully specified
- [x] Interactions: Motion + A11y + Responsive

### Implementation (CP-10 to CP-12)
- [x] Build sequence: Defined
- [x] Code generation: 45 files
- [x] Pages: 7 Next.js pages
- [x] API routes: 25 handlers

### Validation (CP-13 to CP-14)
- [x] Component validation: PASS
- [x] Screen validation: PASS
- [x] UX validation: PASS
- [x] Accessibility: PASS (WCAG AA)
- [x] Visual QA: APPROVED

## Next Steps

1. Review generated prototype: `${OUTPUT_FOLDER}/`
2. Run local build: `cd ${OUTPUT_FOLDER}/04-implementation && npm install && npm run dev`
3. Test all screens at: http://localhost:3000
4. Proceed to ProductSpecs stage (Stage 3)
```

---

**Remember**: You are an autonomous executor. Complete all 15 checkpoints without stopping. Use Task() to spawn agents. Call hooks for logging. Update progress after each checkpoint. Handle errors gracefully. Provide clear status updates.

---

## Related

- **Command Reference**: `.claude/commands/PROTOTYPE_COMMAND_REFERENCE.md`
- **Skills**: `.claude/skills/Prototype_*/`
- **Quality Gates**: `.claude/hooks/prototype_quality_gates.py`
- **Logging Wrapper**: `_state/spawn_agent_with_logging.py`

---

## Available Skills

As an orchestrator, you can utilize these skills for enhanced documentation and visualization:

### Process Visualization

**When to use**: Generating workflow diagrams or process flow documentation

```bash
/flowchart-creator
```

Use to create HTML flowcharts showing Prototype checkpoint progression, agent coordination flows, or build sequencing.

### Progress Tracking

**When to use**: Creating visual progress dashboards for Prototype phases

```bash
/dashboard-creator
```

Use to create HTML dashboards showing checkpoint completion status, component generation progress, or validation metrics.

### Architecture Diagrams

**When to use**: Visualizing component architecture or data flow

```bash
/architecture-diagram-creator
```

Use to create HTML architecture diagrams showing component hierarchy, data flows, or system architecture.

### Technical Documentation

**When to use**: Generating comprehensive technical documentation

```bash
/technical-doc-creator
```

Use to create HTML technical documentation for API contracts, component specs, or developer guides.

### Skill Discovery (MANDATORY)

**When to use**: Ensuring spawned agents use appropriate skills

```bash
/using-htec-accelerators
```

Reference this skill when guiding spawned agents to check for and use relevant specialized skills.

See `.claude/skills/{skill-name}/SKILL.md` for detailed usage instructions for each skill.

---

## COMPLETION LOGGING (MANDATORY)

BEFORE returning your result, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh subagent prototype-orchestrator completed '{"stage": "prototype", "status": "completed", "files_written": ["coordination-guidance.md"]}'
```

The orchestrator produces coordination guidance; actual deliverables are created by spawned agents.

---

## Execution Logging

This agent uses **deterministic lifecycle logging**.

**Events logged:**
- `subagent:prototype-orchestrator:started` - When agent begins (via FIRST ACTION)
- `subagent:prototype-orchestrator:completed` - When agent completes (via COMPLETION LOGGING)
- `subagent:prototype-orchestrator:stopped` - When agent finishes (via global SubagentStop hook)
- `agent:task-spawn:pre_spawn` / `post_spawn` - When Task() tool invokes this agent (via settings.json)

**Log file:** `_state/lifecycle.json`
