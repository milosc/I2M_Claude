---
name: prototype
description: Generate complete working prototype from Discovery with full traceability
argument-hint: <SystemName>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Task, Glob, Grep
skills:
  required:
    - Prototype_ValidateDiscovery
    - Prototype_Requirements
    - Prototype_DataModel
    - Prototype_DesignTokens
    - Prototype_Components
    - Prototype_Screens
    - Prototype_Sequencer
    - Prototype_CodeGen
  optional:
    - Prototype_ApiContracts
    - Prototype_TestData
    - Prototype_DesignBrief
    - Prototype_Interactions
    - Prototype_QA
    - Prototype_UIAudit
    - flowchart-creator
    - dashboard-creator
    - architecture-diagram-creator
    - technical-doc-creator
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: |
            SYSTEM_NAME=$(cat _state/session.json 2>/dev/null | grep -o '"project"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"project"[[:space:]]*:[[:space:]]*"//' | sed 's/"$//' || echo "")
            if [ -n "$SYSTEM_NAME" ] && [ "$SYSTEM_NAME" != "pending" ]; then
              uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_prototype_output.py" --system-name "$SYSTEM_NAME" --quick
            else
              echo '{"result": "skip", "reason": "System name not found in session"}'
              exit 0
            fi
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype ended '{"stage": "prototype"}'
---


# /prototype - Full Prototype Generation

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Validate session (WARNING only - won't block execution)
python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/validate_session.py" --warn-only || true

# 2. CP-0: Validate Traceability Backbone (BLOCKING if invalid)
python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/validate_traceability_backbone.py" --stage prototype || {
  echo "❌ BACKBONE INVALID - Run: /traceability-init --repair"
  exit 1
}

# 3. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 4. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

**Note**: If you see session validation warnings above, run `/project-init` to fix them.
**Note**: If backbone validation fails, run `/traceability-init --repair` to fix missing registries.

## Rules Loading (On-Demand)

This command requires Assembly-First and traceability rules:

```bash
# Assembly-First rules (loaded automatically in Prototype stage)
/_assembly_first_rules

# Traceability rules for ID management
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Required: `<SystemName>` or path to `ClientAnalysis_<SystemName>/`

## Prerequisites

- Completed Discovery: `ClientAnalysis_<SystemName>/` exists with all required outputs
- Dependencies installed: Run `/htec-libraries-init` first
- Traceability folder: `traceability/` exists at project root

---

## Execution Mode: Multi-Agent (Default)

**CRITICAL**: This command uses **multi-agent parallel execution** by default for 60% faster prototype generation.

### Multi-Agent Architecture Check

**AT THE START OF EXECUTION**, check if multi-agent infrastructure is available:

```javascript
// Check for agent infrastructure
const agentRegistryExists = fileExists('.claude/agents/PROTOTYPE_AGENT_REGISTRY.json');
const coordinatorExists = fileExists('.claude/hooks/agent_coordinator.py');
const orchestratorDefined = fileExists('.claude/agents/prototype-orchestrator.md');

if (agentRegistryExists && coordinatorExists && orchestratorDefined) {
  // ✅ MULTI-AGENT MODE ENABLED
  console.log("✅ Multi-Agent Mode ENABLED");
  console.log("   11 specialized agents available");
  console.log("   Expected speedup: up to 60%");
  console.log("   Agent tracking: _state/agent_sessions.json");

  // Spawn the orchestrator agent
  Task({
    subagent_type: "prototype-orchestrator",
    model: "sonnet",
    description: "Orchestrate Prototype generation with parallel agents",
    prompt: `
      Generate complete Prototype for ${SYSTEM_NAME}.

      DISCOVERY_PATH: ClientAnalysis_${SYSTEM_NAME}/
      OUTPUT_PATH: Prototype_${SYSTEM_NAME}/

      Execute all 14 checkpoints (CP0-CP14) using the multi-agent architecture:

      SEQUENTIAL PHASES (Main orchestrator):
      - CP0: Initialize state and folders
      - CP1: Validate Discovery [BLOCKING]
      - CP2: Extract requirements
      - CP5: Generate test data
      - CP10: Generate interaction specs
      - CP11: Generate build sequence
      - CP12: Generate React code

      AGENT-DRIVEN PHASES (Spawn specialized agents):
      - CP3: Spawn data-model-specifier agent
        * Input: ClientAnalysis/04-design-specs/data-fields.md
        * Output: 04-implementation/data-model.md

      - CP4: Spawn api-contract-specifier agent (depends on CP3)
        * Input: data-model.md, screen requirements
        * Output: 04-implementation/api-contracts.json

      - CP6-7: Spawn design-token-generator agent
        * Input: Discovery design specs, pain points
        * Output: design-tokens.json, color-system.md, typography.md

      - CP8: Spawn component-specifier agent (depends on CP6-7)
        * Input: design-tokens.json, Discovery screens
        * Output: 01-components/component-index.md, component specs

      - CP9: Spawn screen-specifier agents (PARALLEL - one per screen)
        * Input: component-index.md, Discovery screen-definitions.md
        * Output: 02-screens/[screen-name]/ folders
        * Strategy: Launch one agent per Discovery screen

      - CP13: Spawn 4 validation agents (PARALLEL)
        * component-validator (haiku)
        * screen-validator (haiku)
        * ux-validator (haiku)
        * accessibility-auditor (sonnet)
        * Output: 05-validation/ validation reports

      - CP14: Spawn visual-qa-tester agent [BLOCKING]
        * Input: Built prototype
        * Output: ui-audit-report.md, screenshots

      AGENT COORDINATION:
      1. Register all agent sessions via agent_coordinator.py
      2. Acquire file locks before modifications
      3. Track activity in _state/agent_sessions.json
      4. Enable Process Integrity monitoring
      5. Use parallel execution for CP9 (screens) and CP13 (validation)

      ASSEMBLY-FIRST MODE:
      - Detect component library at start (Phase 0)
      - Pass assembly_first config to all agents
      - Enforce Assembly-First rules during code generation

      ERROR HANDLING:
      - Skip failures, continue with available data
      - Log to _state/FAILURES_LOG.md
      - Block only on BLOCKING checkpoints (CP1, CP14)

      CRITICAL: Actually spawn agents using Task() calls. Do not execute tasks directly in main session.
    `
  });

  // Exit - orchestrator handles everything
  return;

} else {
  // ⚠️ SEQUENTIAL MODE FALLBACK
  console.log("⚠️ Multi-Agent Mode UNAVAILABLE");
  console.log("   Reason: Agent infrastructure not found");
  console.log("   Fallback: Sequential execution (slower)");
  console.log("   Missing:");
  if (!agentRegistryExists) console.log("   - .claude/agents/PROTOTYPE_AGENT_REGISTRY.json");
  if (!coordinatorExists) console.log("   - .claude/hooks/agent_coordinator.py");
  if (!orchestratorDefined) console.log("   - .claude/agents/prototype-orchestrator.md");

  // Continue with sequential execution (existing workflow below)
}
```

**Verification:**

After execution, check if agents were used:
```bash
./verify_multi_agent.sh
# OR
cat _state/agent_sessions.json
```

If `agent_sessions.json` exists with completed agents → Multi-agent mode was used
If `agent_sessions.json` missing → Sequential fallback was used

---

## Assembly-First Mode Detection

**AT THE START OF EXECUTION** (Phase 0), check if Assembly-First mode should be enabled:

```
ASSEMBLY-FIRST MODE DETECTION:

1. Check if .claude/templates/component-library/ exists
2. Check if .claude/templates/component-library/manifests/components.json exists
3. Check if .claude/templates/component-library/SKILL.md exists
4. Check if project will be a FULL_STACK prototype

IF all checks pass:
  assembly_first_enabled = true
  LOG: "✅ Assembly-First mode ENABLED"
  LOG: "   Component library: .claude/templates/component-library/"
  LOG: "   62 accessible components available"
  LOG: "   Token savings: ~7x overall"

ELSE:
  assembly_first_enabled = false
  LOG: "⚠️ Assembly-First mode DISABLED"
  LOG: "   Reason: {reason_for_failure}"
  LOG: "   Will use traditional component generation"

STORE in _state/prototype_config.json:
  {
    ...
    "assembly_first": {
      "enabled": assembly_first_enabled,
      "component_library_path": ".claude/templates/component-library/",
      "detected_at": timestamp,
      "reason": {reason or "enabled"}
    }
  }
```

**Impact on Workflow:**
- **Phase 8 (Components)**: If ON → Generate LIBRARY_REFERENCE.md + aggregates only (~16x token savings)
- **Phase 9 (Screens)**: If ON → Generate component-usage.md per screen (~6x token savings)
- **Phase 11-12 (Build)**: If ON → Import library components, enforce Assembly-First rules (~5x token savings)

## Skills Used

Read these skills BEFORE executing each phase:

| Phase | Skill File | Notes |
|-------|------------|-------|
| 1 | `.claude/skills/Prototype_ValidateDiscovery/SKILL.md` | - |
| 2 | `.claude/skills/Prototype_Requirements/SKILL.md` | - |
| 3 | `.claude/skills/Prototype_DataModel/SKILL.md` | - |
| 4 | `.claude/skills/Prototype_ApiContracts/SKILL.md` | - |
| 5 | `.claude/skills/Prototype_TestData/SKILL.md` | - |
| 6 | `.claude/skills/Prototype_DesignBrief/SKILL.md` | - |
| 7 | `.claude/skills/Prototype_DesignTokens/SKILL.md` | - |
| 8 | **Mode-dependent** (see below) | If Assembly-First ON: `ASSEMBLY_FIRST_INTEGRATION.md`, else: `SKILL.md` |
| 9 | **Mode-dependent** (see below) | If Assembly-First ON: `ASSEMBLY_FIRST_INTEGRATION.md`, else: `SKILL.md` |
| 10 | `.claude/skills/Prototype_Interactions/SKILL.md` | - |
| 11-12 | **Mode-dependent** (see below) | If Assembly-First ON: `Prototype_Builder/ASSEMBLY_FIRST_INTEGRATION.md`, else: `Sequencer/SKILL.md` + `CodeGen/SKILL.md` |
| 13 | `.claude/skills/Prototype_QA/SKILL.md` | - |
| 14 | `.claude/skills/Prototype_UIAudit/SKILL.md` | - |

**Assembly-First Mode Skills:**
- **Phase 8**: If enabled, read `.claude/skills/Prototype_Components/ASSEMBLY_FIRST_INTEGRATION.md` (generates library reference + aggregates only)
- **Phase 9**: If enabled, read `.claude/skills/Prototype_Screens/ASSEMBLY_FIRST_INTEGRATION.md` (generates component-usage.md per screen)
- **Phase 11-12**: If enabled, read `.claude/skills/Prototype_Builder/ASSEMBLY_FIRST_INTEGRATION.md` (enforces Assembly-First rules during code generation)

## Execution Flow

### Phase 0: Initialize (Checkpoint 0)

1. **Parse Arguments**:
   - If path provided: Extract SystemName from `ClientAnalysis_<SystemName>/`
   - If name provided: Use as SystemName

2. **Validate Discovery Exists**:
   ```bash
   ls ClientAnalysis_<SystemName>/
   ```
   Required files:
   - `01-analysis/ANALYSIS_SUMMARY.md`
   - `01-analysis/PAIN_POINTS.md`
   - `02-research/personas/PERSONA_*.md` (at least one)
   - `02-research/JOBS_TO_BE_DONE.md`
   - `04-design-specs/screen-definitions.md`
   - `04-design-specs/data-fields.md`

3. **Create Output Folder Structure**:
   ```
   Prototype_<SystemName>/
   ├── _state/
   ├── 00-foundation/
   ├── 01-components/
   │   ├── primitives/
   │   ├── data-display/
   │   ├── feedback/
   │   ├── navigation/
   │   ├── overlays/
   │   └── patterns/
   ├── 02-screens/
   ├── 03-interactions/
   ├── 04-implementation/
   │   └── test-data/
   ├── 05-validation/
   │   └── screenshots/
   ├── 06-change-requests/
   ├── prototype/
   │   ├── src/
   │   └── public/
   └── reports/
   ```

4. **Initialize State Files**:

   **IMPORTANT**: Before creating config file, run Assembly-First Mode Detection (see section above)

   `_state/prototype_config.json`:
   ```json
   {
     "schema_version": "1.0.0",
     "system_name": "<SystemName>",
     "created_at": "<YYYY-MM-DD>",
     "discovery_source": "ClientAnalysis_<SystemName>/",
     "output_path": "Prototype_<SystemName>/",
     "framework": "react",
     "styling": "tailwind",
     "assembly_first": {
       "enabled": true,
       "component_library_path": ".claude/templates/component-library/",
       "detected_at": "<YYYY-MM-DD HH:MM:SS>",
       "reason": "enabled"
     },
     "settings": {
       "skip_failures": true,
       "generate_tests": true,
       "accessibility_level": "AA"
     }
   }
   ```

   **Note**: The `assembly_first` object will be `enabled: false` if detection failed (see Assembly-First Mode Detection section)

   `_state/prototype_progress.json`:
   ```json
   {
     "schema_version": "2.3",
     "current_phase": 0,
     "current_checkpoint": 0,
     "started_at": "<YYYY-MM-DD HH:MM:SS>",
     "updated_at": "<YYYY-MM-DD HH:MM:SS>",
     "phases": {
       "initialize": {"phase_number": 0, "status": "in_progress", "started_at": "<timestamp>", "completed_at": null, "outputs": []},
       "validate_discovery": {"phase_number": 1, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "requirements": {"phase_number": 2, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "data_model": {"phase_number": 3, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "api_contracts": {"phase_number": 4, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "test_data": {"phase_number": 5, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "design_brief": {"phase_number": 6, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "design_tokens": {"phase_number": 7, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "components": {"phase_number": 8, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "screens": {"phase_number": 9, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "interactions": {"phase_number": 10, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "sequencer": {"phase_number": 11, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "codegen": {"phase_number": 12, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "qa": {"phase_number": 13, "status": "pending", "started_at": null, "completed_at": null, "outputs": []},
       "ui_audit": {"phase_number": 14, "status": "pending", "started_at": null, "completed_at": null, "outputs": []}
     },
     "validation_history": []
   }
   ```

   `_state/FAILURES_LOG.md`:
   ```markdown
   # Failures Log

   | Timestamp | Phase | Item | Reason |
   |-----------|-------|------|--------|
   ```

5. **Initialize Traceability**:

   Update `traceability/prototype_traceability_register.json`:
   ```json
   {
     "schema_version": "1.0.0",
     "system_name": "<SystemName>",
     "created_at": "<YYYY-MM-DD>",
     "updated_at": "<YYYY-MM-DD>",
     "discovery_link": {
       "folder": "ClientAnalysis_<SystemName>/",
       "register": "traceability/discovery_traceability_register.json"
     },
     "trace_chains": [],
     "coverage": {
       "pain_points_addressed": 0,
       "pain_points_total": 0,
       "coverage_percent": 0
     }
   }
   ```

6. **Validate Checkpoint 0**:
   ```bash
   python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 0 --dir Prototype_<SystemName>/
   ```

7. **Update Progress**: Mark phase 0 completed

---

### Phase 1: Validate Discovery (Checkpoint 1)

1. **Read Skill**: `Prototype_ValidateDiscovery/SKILL.md`
2. **Update Progress**: Mark phase 1 `in_progress`
3. **Execute Skill**:
   - Validate all Discovery outputs exist
   - Extract personas, pain_points, JTBD, screens, entities
   - Fill gaps via brainstorming if needed
4. **Output**: `_state/discovery_summary.json`
5. **Validate Checkpoint 1**:
   ```bash
   python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 1 --dir Prototype_<SystemName>/
   ```
6. **Update Progress**: Mark phase 1 completed

---

### Phase 2: Extract Requirements (Checkpoint 2)

1. **Read Skill**: `Prototype_Requirements/SKILL.md`
2. **Update Progress**: Mark phase 2 `in_progress`
3. **Execute Skill**:
   - Transform Discovery outputs into hierarchical requirements
   - Link each requirement to pain_point_refs, jtbd_refs, persona_refs
   - Assign priority (P0/P1/P2)
4. **Output**: `_state/requirements_registry.json`
5. **Validate Checkpoint 2**:
   ```bash
   python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 2 --dir Prototype_<SystemName>/
   ```
6. **Update Progress**: Mark phase 2 completed

---

### Phase 3: Data Model (Checkpoint 3)

1. **Read Skill**: `Prototype_DataModel/SKILL.md`
2. **Update Progress**: Mark phase 3 `in_progress`
3. **Execute Skill**:
   - Define entity schemas from Discovery data-fields
   - Map relationships and constraints
   - Create data dictionary
4. **Output**: `04-implementation/data-model.md`
5. **Validate Checkpoint 3**
6. **Update Progress**: Mark phase 3 completed

---

### Phase 4: API Contracts (Checkpoint 4)

1. **Read Skill**: `Prototype_ApiContracts/SKILL.md`
2. **Update Progress**: Mark phase 4 `in_progress`
3. **Execute Skill**:
   - Define REST/GraphQL endpoints
   - Map to data model entities
   - Specify request/response schemas
4. **Output**: `04-implementation/api-contracts.json`
5. **Validate Checkpoint 4**
6. **Update Progress**: Mark phase 4 completed

---

### Phase 5: Test Data (Checkpoint 5)

1. **Read Skill**: `Prototype_TestData/SKILL.md`
2. **Update Progress**: Mark phase 5 `in_progress`
3. **Execute Skill**:
   - Generate catalog data (static reference data)
   - Generate core data (primary entities)
   - Generate transactional data (operations)
   - Create persona-specific scenarios
4. **Output**: `04-implementation/test-data/` folder with JSON files
5. **Validate Checkpoint 5**
6. **Update Progress**: Mark phase 5 completed

---

### Phase 6: Design Brief (Checkpoint 6)

1. **Read Skill**: `Prototype_DesignBrief/SKILL.md`
2. **Update Progress**: Mark phase 6 `in_progress`
3. **Execute Skill**:
   - Define visual direction
   - Establish design principles
   - Document accessibility requirements
4. **Outputs**:
   - `00-foundation/design-brief.md`
   - `00-foundation/design-principles.md`
5. **Validate Checkpoint 6**
6. **Update Progress**: Mark phase 6 completed

---

### Phase 7: Design Tokens (Checkpoint 7)

1. **Read Skill**: `Prototype_DesignTokens/SKILL.md`
2. **Update Progress**: Mark phase 7 `in_progress`
3. **Execute Skill**:
   - Define color system
   - Define typography scale
   - Define spacing and layout system
   - Generate tokens JSON
4. **Outputs**:
   - `00-foundation/design-tokens.json`
   - `00-foundation/color-system.md`
   - `00-foundation/typography.md`
   - `00-foundation/spacing-layout.md`
5. **Validate Checkpoint 7**
6. **Update Progress**: Mark phase 7 completed

---

### Phase 8: Components (Checkpoint 8)

1. **Read Skill**: `Prototype_Components/SKILL.md`
2. **Update Progress**: Mark phase 8 `in_progress`
3. **Execute Skill**:
   - Spec primitives (buttons, inputs, etc.)
   - Spec data-display components
   - Spec feedback components
   - Spec navigation components
   - Spec overlays
   - Spec patterns (forms, tables, etc.)
4. **Outputs**:
   - `01-components/component-index.md`
   - `01-components/primitives/*.md`
   - `01-components/data-display/*.md`
   - `01-components/feedback/*.md`
   - `01-components/navigation/*.md`
   - `01-components/overlays/*.md`
   - `01-components/patterns/*.md`
5. **Validate Checkpoint 8**
6. **Update Progress**: Mark phase 8 completed

---

### Phase 9: Screens (Checkpoint 9)

1. **Read Skill**: `Prototype_Screens/SKILL.md`
2. **Update Progress**: Mark phase 9 `in_progress`
3. **Execute Skill**:
   - Define screen layouts from Discovery screen-definitions
   - Map components to screens
   - Define data requirements per screen
   - Document user flows
4. **Outputs**:
   - `02-screens/screen-index.md`
   - `02-screens/[screen-name]/layout.md`
   - `02-screens/[screen-name]/components.md`
   - `02-screens/[screen-name]/data-requirements.md`
5. **Validate Checkpoint 9**
6. **Update Progress**: Mark phase 9 completed

---

### Phase 10: Interactions (Checkpoint 10)

1. **Read Skill**: `Prototype_Interactions/SKILL.md`
2. **Update Progress**: Mark phase 10 `in_progress`
3. **Execute Skill**:
   - Define motion system (transitions, animations)
   - Define accessibility specifications (WCAG AA)
   - Define responsive behavior
4. **Outputs**:
   - `03-interactions/motion-system.md`
   - `03-interactions/accessibility-spec.md`
   - `03-interactions/responsive-behavior.md`
5. **Validate Checkpoint 10**
6. **Update Progress**: Mark phase 10 completed

---

### Phase 11: Build Sequence (Checkpoint 11)

1. **Read Skill**: `Prototype_Sequencer/SKILL.md`
2. **Update Progress**: Mark phase 11 `in_progress`
3. **Execute Skill**:
   - Analyze component dependencies
   - Create build order (DAG)
   - Generate implementation prompts
4. **Output**: `04-implementation/build-sequence.md`
5. **Validate Checkpoint 11**
6. **Update Progress**: Mark phase 11 completed

---

### Phase 12: Code Generation (Checkpoint 12)

1. **Read Skill**: `Prototype_CodeGen/SKILL.md`
2. **Update Progress**: Mark phase 12 `in_progress`
3. **Execute Skill**:
   - Initialize React project with Vite
   - Generate component code
   - Generate screen code
   - Wire up routing
   - Apply design tokens
4. **Outputs**:
   - `prototype/package.json`
   - `prototype/src/App.tsx`
   - `prototype/src/components/`
   - `prototype/src/pages/`
   - `prototype/src/styles/`
5. **Validate Checkpoint 12**:
   ```bash
   cd Prototype_<SystemName>/prototype && npm install && npm run build
   ```
6. **Update Progress**: Mark phase 12 completed

---

### Phase 13: QA Testing (Checkpoint 13)

1. **Read Skill**: `Prototype_QA/SKILL.md`
2. **Update Progress**: Mark phase 13 `in_progress`
3. **Execute Skill**:
   - Run functional tests
   - Validate requirements coverage
   - Test user flows
   - Document issues
4. **Output**: `05-validation/qa-report.md`
5. **Validate Checkpoint 13**
6. **Update Progress**: Mark phase 13 completed

---

### Phase 14: UI Audit (Checkpoint 14)

1. **Read Skill**: `Prototype_UIAudit/SKILL.md`
2. **Update Progress**: Mark phase 14 `in_progress`
3. **Execute Skill**:
   - Capture screenshots via Playwright
   - Compare against design specs
   - Document visual issues
   - Generate architecture documentation
4. **Outputs**:
   - `05-validation/ui-audit-report.md`
   - `05-validation/screenshots/`
   - `reports/ARCHITECTURE.md`
   - `reports/README.md`
   - `reports/TRACEABILITY_MATRIX.md`
5. **Validate Checkpoint 14**
6. **Update Progress**: Mark phase 14 completed

---

## State Management

After EACH phase completion:

1. **Update Progress File**:
   ```json
   {
     "phases": {
       "<phase_name>": {
         "status": "completed",
         "completed_at": "<timestamp>",
         "outputs": ["<file1>", "<file2>"]
       }
     },
     "current_phase": <next_phase_number>,
     "updated_at": "<timestamp>"
   }
   ```

2. **Run Checkpoint Validation**:
   ```bash
   python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint <N> --dir Prototype_<SystemName>/
   ```

3. **Record Validation**:
   Add to `validation_history` array in progress file

4. **Update Traceability**:
   - Add new artifacts to `prototype_traceability_register.json`
   - Update coverage metrics

5. **Log Failures**:
   Any skipped items to `_state/FAILURES_LOG.md`:
   ```markdown
   | <timestamp> | <phase> | <item> | <reason> |
   ```

---

## Error Handling

> **STRICT RULE**: ERROR → SKIP → CONTINUE → NEVER RETRY

| Error | Action |
|-------|--------|
| Discovery file missing | Log `⛔ SKIPPED`, continue with available data |
| Skill execution fails | Log failure, skip to next phase |
| Checkpoint validation fails | **BLOCK** - Must fix before proceeding |
| Code generation fails | Log failure, provide manual instructions |
| npm install/build fails | Log failure, continue to QA with notes |

### BANNED Actions

- ❌ pip install anything
- ❌ Retry failed operations
- ❌ Ask user what to do on error
- ❌ Wait for input after error

---

## Completion

On successful completion, display:

**If Assembly-First Mode ON:**
```
═══════════════════════════════════════════════════════
  PROTOTYPE GENERATION COMPLETE
  Assembly-First Mode: ENABLED
═══════════════════════════════════════════════════════

  System:              <SystemName>
  Discovery Source:    ClientAnalysis_<SystemName>/
  Output:              Prototype_<SystemName>/

  Phases Completed:    14/14
  Checkpoints Passed:  15/15

  Assembly-First Benefits:
  ├── Library Components:  62 (imported)
  ├── Aggregate Components: <N> (generated)
  ├── Token Savings:       ~7x overall
  ├── Accessibility:       100% WCAG AA (built-in)
  └── Build Time:          ~30% faster

  Artifacts Generated:
  ├── Component Specs:     <N> aggregates (~80% fewer files)
  ├── Screen Specs:        <N> screens (with component-usage.md)
  ├── Test Cases:          <N> scenarios
  └── Code Files:          <N> files

  Traceability:
  ├── Pain Points:     <N>/<M> addressed (<P>%)
  ├── Requirements:    <N> linked
  └── Test Coverage:   <P>%

  Assembly-First Validation:
  ├── Raw HTML Check:      ✅ PASSED (0 violations)
  ├── Import Check:        ✅ PASSED (all from library)
  ├── ARIA Check:          ✅ PASSED (no manual attributes)
  └── Build Check:         ✅ PASSED

═══════════════════════════════════════════════════════

  Next Steps:
  • /prototype-serve     - Start development server
  • /prototype-export    - Package for ProductSpecs
  • /prototype-feedback  - Process change requests

═══════════════════════════════════════════════════════
```

**If Assembly-First Mode OFF (Traditional):**
```
═══════════════════════════════════════════════════════
  PROTOTYPE GENERATION COMPLETE
═══════════════════════════════════════════════════════

  System:              <SystemName>
  Discovery Source:    ClientAnalysis_<SystemName>/
  Output:              Prototype_<SystemName>/

  Phases Completed:    14/14
  Checkpoints Passed:  15/15

  Artifacts Generated:
  ├── Components:      <N> specs
  ├── Screens:         <N> specs
  ├── Test Cases:      <N> scenarios
  └── Code Files:      <N> files

  Traceability:
  ├── Pain Points:     <N>/<M> addressed (<P>%)
  ├── Requirements:    <N> linked
  └── Test Coverage:   <P>%

═══════════════════════════════════════════════════════

  Next Steps:
  • /prototype-serve     - Start development server
  • /prototype-export    - Package for ProductSpecs
  • /prototype-feedback  - Process change requests

═══════════════════════════════════════════════════════
```

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype-init` | Initialize only (Phase 0) |
| `/prototype-status` | Show current progress |
| `/prototype-resume` | Resume from last checkpoint |
| `/prototype-reset` | Reset state or delete all |
| `/prototype-feedback` | Process change requests |
| `/prototype-export` | Package for ProductSpecs |
