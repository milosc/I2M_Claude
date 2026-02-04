---
name: productspecs
description: Generate production-ready specifications from Prototype with JIRA export
argument-hint: <SystemName>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Task, Glob, Grep
skills:
  required:
    - ProductSpecs_Generator
    - ProductSpecs_NFRGenerator
    - ProductSpecs_TestSpecGenerator
    - ProductSpecs_Validate
    - ProductSpecs_ExtractRequirements
  optional:
    - ProductSpecs_JIRAExporter
    - flowchart-creator
    - dashboard-creator
    - technical-doc-creator
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_productspecs_output.py"
            --system-name "$1"
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs ended '{"stage": "productspecs"}'
---


# /productspecs - Full ProductSpecs Generation

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Validate session (WARNING only - won't block execution)
python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/validate_session.py" --warn-only || true

# 2. CP-0: Validate Traceability Backbone (BLOCKING if invalid)
python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/validate_traceability_backbone.py" --stage productspecs || {
  echo "❌ BACKBONE INVALID - Run: /traceability-init --repair"
  exit 1
}

# 3. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 4. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

**Note**: If you see session validation warnings above, run `/project-init` to fix them.
**Note**: If backbone validation fails, run `/traceability-init --repair` to fix missing registries.

---

## 🎯 Guiding Architectural Principle

**Optimize for maintainability, not simplicity.**

When making architectural and implementation decisions:

1. **Prioritize long-term maintainability** over short-term simplicity
2. **Minimize complexity** by being strategic with dependencies and libraries
3. **Avoid "simplicity traps"** - adding libraries without considering downstream debugging and maintenance burden
4. **Think 6 months ahead** - will this decision make debugging easier or harder?
5. **Use libraries strategically** - not avoided, but chosen carefully with justification

### Decision-Making Protocol

When facing architectural trade-offs between complexity and maintainability:

**If the decision is clear** → Make the decision autonomously and document the rationale

**If the decision is unclear** → Use `AskUserQuestion` tool with:
- Minimum 3 alternative scenarios
- Clear trade-off analysis for each option
- Maintainability impact assessment (short-term vs long-term)
- Complexity implications (cognitive load, debugging difficulty, dependency graph)
- Recommendation with reasoning

---

## Rules Loading (On-Demand)

This command requires traceability rules for module/test ID management:

```bash
# Load Traceability rules (includes module ID format MOD-XXX-XXX-NN)
/rules-traceability
```

## Description

This is the main orchestrator command that runs all phases (0-8) of the ProductSpecs generation pipeline. It transforms a completed Prototype into production-ready specifications with full traceability and JIRA export files.

## Arguments

- `$ARGUMENTS` - Required: `<SystemName> [OPTIONS]`

### Options (7 Entry Points)

| Option | Description | Example |
|--------|-------------|---------|
| `--module MOD-XXX` | Regenerate single module | `--module MOD-INV-SEARCH-01` |
| `--feature FEATURE` | All modules for a feature (fuzzy matching) | `--feature SEARCH` |
| `--screen SCR-XXX` | All modules linked to screen | `--screen SCR-003` |
| `--persona NAME` | All modules for persona | `--persona admin` |
| `--subsystem NAME` | All modules in subsystem | `--subsystem middleware` |
| `--layer LAYER` | All modules in layer | `--layer frontend` |
| `--quality critical` | Enable VP review for ALL modules | `--quality critical` |
| `--from-checkpoint N` | Resume from checkpoint N | `--from-checkpoint 5` |

**Note**: Only one entry point can be specified at a time. If no option is provided, system-level (all modules) is used.

## Prerequisites

- Completed Discovery: `ClientAnalysis_<SystemName>/` with Checkpoint 11 passed
- Completed Prototype: `Prototype_<SystemName>/` with Checkpoint 14 passed
- Shared state files in `_state/` at ROOT level

## Quick Start

### System-Level (All Modules - Default)
```bash
/productspecs InventorySystem
```

### Module-Level (Single Module)
```bash
/productspecs InventorySystem --module MOD-INV-SEARCH-01
```

### Feature-Level (Fuzzy Matching)
```bash
/productspecs InventorySystem --feature SEARCH
# Also matches: "search", "srch", "Search"
```

### Screen-Level
```bash
/productspecs InventorySystem --screen SCR-003
```

### Persona-Level
```bash
/productspecs InventorySystem --persona admin
```

### Subsystem-Level
```bash
/productspecs InventorySystem --subsystem middleware
```

### Layer-Level
```bash
/productspecs InventorySystem --layer frontend
# Valid layers: frontend, backend, middleware, database
```

### Quality Critical Mode
```bash
/productspecs InventorySystem --quality critical
# Forces VP review for ALL modules (P0, P1, P2)
```

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCTSPECS PIPELINE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 0: Initialize                                            │
│  ├── Create folder structure                                    │
│  ├── Initialize state files                                     │
│  └── Checkpoint 0 ✓                                             │
│                                                                 │
│  Phase 1: Validate                                              │
│  ├── Validate Discovery completeness                            │
│  ├── Validate Prototype completeness                            │
│  └── Checkpoint 1 ✓                                             │
│                                                                 │
│  Phase 2: Extract                                               │
│  ├── Extract requirements hierarchy                             │
│  ├── Build requirements registry                                │
│  └── Checkpoint 2 ✓                                             │
│                                                                 │
│  Phases 3-4: Modules                                            │
│  ├── Generate module index                                      │
│  ├── Generate module specifications                             │
│  ├── Map screens to modules                                     │
│  └── Checkpoints 3-4 ✓                                          │
│                                                                 │
│  Phase 5: Contracts                                             │
│  ├── Consolidate API contracts                                  │
│  ├── Generate SMART NFRs                                        │
│  ├── Document data contracts                                    │
│  └── Checkpoint 5 ✓                                             │
│                                                                 │
│  Phase 6: Tests                                                 │
│  ├── Generate test specifications                               │
│  ├── E2E scenarios                                              │
│  ├── Accessibility checklist                                    │
│  └── Checkpoint 6 ✓                                             │
│                                                                 │
│  Phase 7: Finalize                                              │
│  ├── Validate traceability chains                               │
│  ├── Generate traceability matrix                               │
│  ├── Validation report                                          │
│  └── Checkpoint 7 ✓                                             │
│                                                                 │
│  Phase 8: Export                                                │
│  ├── Collect JIRA configuration                                 │
│  ├── Generate JIRA export files                                 │
│  ├── Generation summary                                         │
│  └── Checkpoint 8 ✓                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Execution Flow

### Pre-Phase: Scope Filtering (NEW in v4.0.0)

**Before Phase 0**, parse command arguments and filter scope:

```bash
# Parse command arguments
SYSTEM_NAME="$1"
shift  # Remove system name from arguments

# Parse flags using Python utility
python3 .claude/hooks/productspecs_scope_filter.py \
  "$SYSTEM_NAME" \
  "$@" \
  --output "_state/filtered_scope.json"

# Check for errors
if [ $? -ne 0 ]; then
  echo "❌ Scope filtering failed. Fix errors above."
  exit 1
fi

# Load filtered scope
FILTERED_SCOPE=$(cat _state/filtered_scope.json)
TOTAL_MODULES=$(echo "$FILTERED_SCOPE" | jq -r '.total_modules')
FILTER_TYPE=$(echo "$FILTERED_SCOPE" | jq -r '.type')
QUALITY_CRITICAL=$(echo "$FILTERED_SCOPE" | jq -r '.quality_critical')

echo "✅ Scope filtered: $TOTAL_MODULES modules ($FILTER_TYPE-level)"
```

**Benefits**:
- **80% time savings** for module-level updates
- **Targeted regeneration** for feature/screen/persona
- **Quality critical mode** for high-stakes releases

---

## 🚀 EXECUTION: Multi-Agent Orchestration (v2.0)

This command uses **hierarchical multi-agent orchestration**. The main session spawns specialized agents directly (flat spawning pattern) following the orchestrator's coordination logic.

### Architecture Pattern

```
Main Session
├─→ CP-0-2: Sequential (main session - init, validate, extract)
├─→ CP-3-4: Parallel Agent Spawning (module generation)
│   ├─ Task(ui-module-specifier) ──┐
│   ├─ Task(api-module-specifier) ─┼─→ Merge Gate → self-validation → VP review
│   └─ Task(nfr-generator) ────────┘
├─→ CP-5: Sequential (main session - contracts consolidation)
├─→ CP-6: Parallel Agent Spawning (test generation)
│   ├─ Task(unit-test-specifier) ────┐
│   ├─ Task(integration-test-specifier) ┼─→ Merge Gate → coverage analysis
│   ├─ Task(e2e-test-specifier) ─────┘
│   └─ Task(pict-combinatorial) ─────┘
├─→ CP-7: Parallel Agent Spawning (validation - BLOCKING)
│   ├─ Task(traceability-validator) ───┐
│   ├─ Task(cross-reference-validator) ┼─→ BLOCK if criteria not met
│   └─ Task(spec-reviewer) ────────────┘
└─→ CP-8: Sequential (main session - JIRA export)
```

### Step 1: Initialize & Parse Scope (CP-0)

```bash
# Parse command arguments
SYSTEM_NAME="{SystemName}"
# Options are parsed from $ARGUMENTS

# Initialize state and filter scope
python3 .claude/hooks/productspecs_scope_filter.py "$SYSTEM_NAME" $ARGUMENTS --output "_state/filtered_scope.json"

# Create folders and config
# ... (handled by /productspecs-init logic)
```

### Step 2: Validate Prerequisites (CP-1)

Run validation checks:
- Discovery checkpoint ≥ 11
- Prototype checkpoint ≥ 14
- Required state files exist

### Step 3: Extract Requirements (CP-2)

Sequential extraction in main session:
- Build requirements hierarchy
- Create `_registry/requirements.json`

### Step 4: Module Generation (CP-3-4) - PARALLEL AGENTS

**Spawn 3 agents in parallel for module specification:**

```
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate UI module specs",
  prompt: `Agent: productspecs-ui-module-specifier
    Read: .claude/agents/productspecs-ui-module-specifier.md
    SYSTEM: {SystemName}
    SCOPE: {filtered_scope from _state/filtered_scope.json}
    CONFIG: {from _state/productspecs_config.json}

    Generate UI module specifications for filtered modules.
    After each module: spawn self-validator, check score, trigger VP review if needed.

    RETURN JSON: { status, files_written, quality_scores, issues }`
})

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate API module specs",
  prompt: `Agent: productspecs-api-module-specifier
    Read: .claude/agents/productspecs-api-module-specifier.md
    SYSTEM: {SystemName}
    SCOPE: {filtered_scope}

    Generate API/backend module specifications.

    RETURN JSON: { status, files_written, quality_scores, issues }`
})

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate NFR specifications",
  prompt: `Agent: productspecs-nfr-generator
    Read: .claude/agents/productspecs-nfr-generator.md
    SYSTEM: {SystemName}

    Generate SMART NFRs (performance, security, reliability, usability).

    RETURN JSON: { status, nfrs_generated, quality_score }`
})
```

**Merge Gate (after all 3 complete):**
- Consolidate `_registry/modules.json`
- If `--quality critical`: spawn VP reviewer for ALL modules
- Update checkpoint progress to CP-4

### Step 5: Contracts Consolidation (CP-5)

Sequential in main session:
- Consolidate API contracts
- Generate `02-api/api-index.md`
- Generate `02-api/data-contracts.md`

### Step 6: Test Generation (CP-6) - PARALLEL AGENTS

**Spawn 4 agents in parallel for test specification:**

```
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Generate unit test specs",
  prompt: `Agent: productspecs-unit-test-specifier
    Read: .claude/agents/productspecs-unit-test-specifier.md
    SYSTEM: {SystemName}
    MODULES: {from _registry/modules.json}

    RETURN JSON: { status, test_cases, coverage }`
})

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate integration test specs",
  prompt: `Agent: productspecs-integration-test-specifier
    Read: .claude/agents/productspecs-integration-test-specifier.md
    SYSTEM: {SystemName}

    RETURN JSON: { status, test_cases, coverage }`
})

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate E2E test specs",
  prompt: `Agent: productspecs-e2e-test-specifier
    Read: .claude/agents/productspecs-e2e-test-specifier.md
    SYSTEM: {SystemName}

    RETURN JSON: { status, scenarios, coverage }`
})

Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Generate PICT combinatorial tests",
  prompt: `Agent: productspecs-pict-combinatorial
    Read: .claude/agents/productspecs-pict-combinatorial.md
    SYSTEM: {SystemName}

    RETURN JSON: { status, pairwise_cases, reduction_ratio }`
})
```

**Merge Gate:**
- Consolidate `_registry/test-cases.json`
- Analyze P0 coverage (must be 100%)

### Step 7: Global Validation (CP-7) - PARALLEL AGENTS (BLOCKING)

**Spawn 3 validators in parallel:**

```
Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Validate traceability chains",
  prompt: `Agent: productspecs-traceability-validator
    Read: .claude/agents/productspecs-traceability-validator.md
    SYSTEM: {SystemName}

    Check: CM → PP → JTBD → REQ → MOD → TC chains
    REQUIRED: P0 coverage = 100%

    RETURN JSON: { valid, p0_coverage, p1_coverage, orphaned_items }`
})

Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Validate cross-references",
  prompt: `Agent: productspecs-cross-reference-validator
    Read: .claude/agents/productspecs-cross-reference-validator.md
    SYSTEM: {SystemName}

    Check: No dangling refs, no circular deps

    RETURN JSON: { valid, dangling_refs, circular_deps }`
})

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Review spec quality",
  prompt: `Agent: productspecs-spec-reviewer
    Read: .claude/agents/productspecs-spec-reviewer.md
    SYSTEM: {SystemName}

    Review: Clarity, completeness, testability

    RETURN JSON: { valid, quality_score, issues }`
})
```

**BLOCKING GATE:**
```
IF p0_coverage < 100% OR dangling_refs > 0 OR quality_score < 70:
  BLOCK → Display fix instructions
  EXIT with error
ELSE:
  CONTINUE to CP-8
```

### Step 8: JIRA Export (CP-8)

Sequential in main session:
- Generate JIRA CSV files
- Create import guide
- Generate summary

---

### Phase 0: Initialize

```bash
# Equivalent to:
/productspecs-init <SystemName>
```

Creates:
- `ProductSpecs_<SystemName>/` folder structure
- `_state/productspecs_config.json`
- `_state/productspecs_progress.json`
- `_state/filtered_scope.json` (from Pre-Phase)

### Phase 1: Validate

```bash
# Equivalent to:
/productspecs-validate <SystemName>
```

Validates:
- Discovery checkpoint 11 passed
- Prototype checkpoint 14 passed
- Required state files exist

### Phase 2: Extract

```bash
# Equivalent to:
/productspecs-extract <SystemName>
```

Creates:
- `_registry/requirements.json`
- Requirements hierarchy (P0/P1/P2)
- Traceability links to Discovery

### Phases 3-4: Modules

```bash
# Equivalent to:
/productspecs-modules <SystemName>
```

Creates:
- `01-modules/module-index.md`
- `01-modules/MOD-*.md` specifications
- `_registry/modules.json`

### Phase 5: Contracts

```bash
# Equivalent to:
/productspecs-contracts <SystemName>
```

Creates:
- `02-api/api-index.md`
- `02-api/NFR_SPECIFICATIONS.md`
- `02-api/data-contracts.md`
- `_registry/nfrs.json`

### Phase 6: Tests

```bash
# Equivalent to:
/productspecs-tests <SystemName>
```

Creates:
- `03-tests/test-case-registry.md`
- `03-tests/e2e-scenarios.md`
- `03-tests/accessibility-checklist.md`
- `_registry/test-cases.json`

### Phase 7: Finalize

```bash
# Equivalent to:
/productspecs-finalize <SystemName>
```

Creates:
- `00-overview/TRACEABILITY_MATRIX.md`
- `00-overview/VALIDATION_REPORT.md`
- Updated `_registry/traceability.json`

### Phase 8: Export

```bash
# Equivalent to:
/productspecs-export <SystemName>
```

Creates:
- `04-jira/full-hierarchy.csv`
- `04-jira/epics-and-stories.csv`
- `04-jira/subtasks-only.csv`
- `04-jira/jira-import.json`
- `04-jira/IMPORT_GUIDE.md`
- `00-overview/GENERATION_SUMMARY.md`

## Checkpoint Validation

Each phase validates its checkpoint before proceeding:

| Checkpoint | Phase | Validation |
|------------|-------|------------|
| 0 | Init | Config and folders exist |
| 1 | Validate | Discovery and Prototype complete |
| 2 | Extract | Requirements registry exists |
| 3 | Modules Core | Module index exists |
| 4 | Modules Extended | All screens have modules |
| 5 | Contracts | API index and NFRs exist |
| 6 | Tests | Test registry exists |
| 7 | Traceability | 100% P0 coverage |
| 8 | Export | JIRA files exist |

## Error Handling

```
ERROR → SKIP → CONTINUE → NEVER RETRY
```

- If a phase fails validation: **BLOCK** and display fix instructions
- If a file fails to read: Log to `FAILURES_LOG.md`, continue
- Never pip install on errors
- Never retry failed operations
- Never ask what to do

### Blocking vs Non-Blocking

| Error Type | Action |
|------------|--------|
| P0 traceability < 100% | **BLOCK** at Checkpoint 7 |
| Broken cross-references | **BLOCK** at Checkpoint 7 |
| Missing Discovery | **BLOCK** at Checkpoint 1 |
| Missing Prototype | **BLOCK** at Checkpoint 1 |
| P1/P2 gaps | **WARN**, continue |
| Optional file missing | **WARN**, continue |

## Output Structure

```
project_root/
├── _state/                              # SHARED (ROOT)
│   ├── productspecs_config.json
│   ├── productspecs_progress.json
│   ├── discovery_summary.json           # From Discovery
│   ├── requirements_registry.json       # From Prototype
│   └── FAILURES_LOG.md
│
├── traceability/                        # SHARED (ROOT)
│   ├── productspecs_traceability_register.json
│   └── spec_registry.json
│
├── ClientAnalysis_<SystemName>/         # Discovery (input)
├── Prototype_<SystemName>/              # Prototype (input)
│
└── ProductSpecs_<SystemName>/           # OUTPUT
    ├── 00-overview/
    │   ├── MASTER_DEVELOPMENT_PLAN.md
    │   ├── GENERATION_SUMMARY.md
    │   ├── TRACEABILITY_MATRIX.md
    │   └── VALIDATION_REPORT.md
    │
    ├── 01-modules/
    │   ├── module-index.md
    │   └── MOD-<APP>-<FEAT>-<NN>.md
    │
    ├── 02-api/
    │   ├── api-index.md
    │   ├── NFR_SPECIFICATIONS.md
    │   └── data-contracts.md
    │
    ├── 03-tests/
    │   ├── test-case-registry.md
    │   ├── e2e-scenarios.md
    │   └── accessibility-checklist.md
    │
    ├── 04-jira/
    │   ├── jira_config.json
    │   ├── IMPORT_GUIDE.md
    │   ├── full-hierarchy.csv
    │   ├── epics-and-stories.csv
    │   ├── subtasks-only.csv
    │   └── jira-import.json
    │
    ├── _registry/
    │   ├── modules.json
    │   ├── requirements.json
    │   ├── nfrs.json
    │   ├── traceability.json
    │   └── test-cases.json
    │
    └── feedback-sessions/
        └── productspecs_feedback_registry.json
```

## Traceability Chain

The full traceability chain maintained throughout:

```
CM-XXX (Client Material)
    ↓
PP-X.X (Pain Point)
    ↓
JTBD-X.X (Job To Be Done)
    ↓
REQ-XXX (Requirement)
    ↓
SCR-XXX (Screen)
    ↓
MOD-XXX (Module)
    ↓
TC-XXX (Test Case)
    ↓
INV-XXX (JIRA Item)
```

## Progress Display

During execution, progress is displayed:

```
═══════════════════════════════════════════════════════════════
  PRODUCTSPECS GENERATION
═══════════════════════════════════════════════════════════════

  System: InventorySystem
  Phase:  3/8 - Generating Modules

  Progress:
  ──────────────────────────────────────────────────────────────
  [✓] Phase 0: Initialize
  [✓] Phase 1: Validate
  [✓] Phase 2: Extract
  [▶] Phases 3-4: Modules ████████░░░░░░░░░░░░ 40%
  [ ] Phase 5: Contracts
  [ ] Phase 6: Tests
  [ ] Phase 7: Finalize
  [ ] Phase 8: Export

  Current: Generating MOD-INV-SEARCH-01...

═══════════════════════════════════════════════════════════════
```

## Completion Summary

```
═══════════════════════════════════════════════════════════════
  PRODUCTSPECS GENERATION COMPLETE
═══════════════════════════════════════════════════════════════

  System:          InventorySystem
  Duration:        45 minutes
  Status:          ✅ ALL CHECKPOINTS PASSED

  Summary:
  ──────────────────────────────────────────────────────────────
  │ Artifact          │ Count │
  │───────────────────│───────│
  │ Module Specs      │ 12    │
  │ Requirements      │ 45    │
  │ NFRs              │ 25    │
  │ Test Cases        │ 107   │
  │ JIRA Items        │ 237   │

  Traceability:     100% P0 Coverage

  Output:           ProductSpecs_InventorySystem/

═══════════════════════════════════════════════════════════════

  Next Steps:
  1. Review 04-jira/IMPORT_GUIDE.md
  2. Import to JIRA
  3. Begin development

═══════════════════════════════════════════════════════════════
```

## Resuming Interrupted Generation

If generation is interrupted, use:

```bash
/productspecs-resume
```

This resumes from the last completed checkpoint.

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/productspecs-status` | Show current progress |
| `/productspecs-resume` | Resume from checkpoint |
| `/productspecs-reset` | Reset state |
| `/productspecs-feedback` | Process change requests |

### Phase Commands

| Command | Phases |
|---------|--------|
| `/productspecs-init` | 0 |
| `/productspecs-validate` | 1 |
| `/productspecs-extract` | 2 |
| `/productspecs-modules` | 3-4 |
| `/productspecs-contracts` | 5 |
| `/productspecs-tests` | 6 |
| `/productspecs-finalize` | 7 |
| `/productspecs-export` | 8 |

### Utility Commands

| Command | Description |
|---------|-------------|
| `/productspecs-jira` | JIRA export only |

## Scope Filtering Examples

### Example 1: Feature-Level with Fuzzy Matching

```bash
# User input: "SEARCH" (exact match)
/productspecs InventorySystem --feature SEARCH
# Output: Modules MOD-INV-SEARCH-01, MOD-INV-SEARCH-02

# User input: "srch" (fuzzy match)
/productspecs InventorySystem --feature srch
# Output: ⚠️ Fuzzy match: 'srch' matched features: SEARCH
#         Modules MOD-INV-SEARCH-01, MOD-INV-SEARCH-02

# User input: "xyz" (no match)
/productspecs InventorySystem --feature xyz
# Output: ❌ No modules found for feature 'xyz'. Try: SEARCH, REPORT, EXPORT
```

### Example 2: Layer-Level Validation

```bash
# Valid layer
/productspecs InventorySystem --layer frontend
# Output: ✅ Scope filtered: 8 modules (layer-level)

# Invalid layer
/productspecs InventorySystem --layer frontend-api
# Output: ❌ Invalid layer 'frontend-api'. Valid layers: frontend, backend, middleware, database
```

### Example 3: Quality Critical Mode

```bash
# Standard mode (default)
/productspecs InventorySystem
# VP reviews: 5 (only P0 modules)

# Quality critical mode
/productspecs InventorySystem --quality critical
# VP reviews: 20 (ALL modules - P0, P1, P2)
# Time: +119%, Cost: +126%, Quality: +28%
```

### Example 4: Module-Level Update

```bash
# Regenerate single module after feedback
/productspecs InventorySystem --module MOD-INV-SEARCH-01
# Output: ✅ Scope filtered: 1 module (module-level)
# Time savings: 80% (2 min vs 10 min for full system)
```

## Scope Validation

The scope filter validates inputs and provides helpful error messages:

| Error Case | Validation | Error Message |
|------------|------------|---------------|
| Invalid module ID | Check module exists | `❌ Module 'MOD-XXX-YYY-01' not found. Available: ...` |
| Invalid feature | Fuzzy match, suggest alternatives | `❌ No modules found for feature 'xyz'. Try: SEARCH, REPORT` |
| Invalid layer | Check against valid layers | `❌ Invalid layer 'api'. Valid layers: frontend, backend, middleware, database` |
| Empty scope | Check filtered result | `❌ No modules found for scope. Adjust filters.` |
| Multiple flags | Validate mutual exclusivity | `❌ Only one entry point flag allowed at a time` |

## Integration with Discovery and Prototype

ProductSpecs is the third stage in the pipeline:

```
Discovery (Stage 1)     Prototype (Stage 2)     ProductSpecs (Stage 3)
─────────────────────   ────────────────────    ─────────────────────
/discovery              /prototype              /productspecs
                            ↓
                    ┌───────────────────┐
                    │  Shared State     │
                    │  _state/          │
                    │  traceability/    │
                    └───────────────────┘
```

All three stages share:
- `_state/` folder at ROOT level
- `traceability/` folder at ROOT level
- Consistent ID formats
- Cross-stage validation

## Performance Impact (7 Entry Points)

| Entry Point | Time Savings | Use Case |
|-------------|--------------|----------|
| System-level | 0% (baseline) | Initial generation, full updates |
| Module-level | 80% | Single module regeneration after feedback |
| Feature-level | 60-70% | Feature iteration, A/B testing |
| Screen-level | 50-60% | UI updates, screen redesigns |
| Persona-level | 40-50% | Persona-specific features |
| Subsystem-level | 30-40% | Subsystem refactoring |
| Layer-level | 40-50% | Frontend/backend separation |

---

## ⚡ WHEN INVOKED: Execution Instructions

**When this command is invoked, you MUST follow these steps:**

### 1. FIRST ACTION (Mandatory - Already Done Above)

The session initialization, logging, and rule loading from the "FIRST ACTION" section at the top.

### 2. Parse Arguments & Initialize

```bash
# Extract system name and options from $ARGUMENTS
SYSTEM_NAME=$(echo "$ARGUMENTS" | awk '{print $1}')

# Run scope filter
python3 .claude/hooks/productspecs_scope_filter.py "$SYSTEM_NAME" $ARGUMENTS --output "_state/filtered_scope.json" 2>/dev/null || true
```

### 3. Execute Checkpoints with Multi-Agent Spawning

**CP-0 through CP-2**: Execute sequentially in main session (init, validate, extract)

**CP-3-4 (Module Generation)**: Spawn agents IN PARALLEL using Task tool:

```javascript
// Spawn these 3 agents in parallel (single message, multiple Task calls)
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate UI module specs",
  prompt: "Agent: productspecs-ui-module-specifier\nRead: .claude/agents/productspecs-ui-module-specifier.md\nSYSTEM: {SystemName}\n..."
})

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate API module specs",
  prompt: "Agent: productspecs-api-module-specifier\nRead: .claude/agents/productspecs-api-module-specifier.md\nSYSTEM: {SystemName}\n..."
})

Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Generate NFR specs",
  prompt: "Agent: productspecs-nfr-generator\nRead: .claude/agents/productspecs-nfr-generator.md\nSYSTEM: {SystemName}\n..."
})
```

**CP-5**: Execute sequentially (contracts consolidation)

**CP-6 (Test Generation)**: Spawn 4 agents IN PARALLEL:

```javascript
Task({ subagent_type: "general-purpose", model: "haiku", description: "Generate unit tests", prompt: "Agent: productspecs-unit-test-specifier..." })
Task({ subagent_type: "general-purpose", model: "sonnet", description: "Generate integration tests", prompt: "Agent: productspecs-integration-test-specifier..." })
Task({ subagent_type: "general-purpose", model: "sonnet", description: "Generate E2E tests", prompt: "Agent: productspecs-e2e-test-specifier..." })
Task({ subagent_type: "general-purpose", model: "haiku", description: "Generate PICT tests", prompt: "Agent: productspecs-pict-combinatorial..." })
```

**CP-7 (Validation - BLOCKING)**: Spawn 3 validators IN PARALLEL:

```javascript
Task({ subagent_type: "general-purpose", model: "haiku", description: "Validate traceability", prompt: "Agent: productspecs-traceability-validator..." })
Task({ subagent_type: "general-purpose", model: "haiku", description: "Validate cross-refs", prompt: "Agent: productspecs-cross-reference-validator..." })
Task({ subagent_type: "general-purpose", model: "sonnet", description: "Review spec quality", prompt: "Agent: productspecs-spec-reviewer..." })
```

**CP-8**: Execute sequentially (JIRA export)

### 4. Progress Tracking

After each checkpoint, update `_state/productspecs_progress.json`:

```bash
python3 -c "
import json
with open('_state/productspecs_progress.json', 'r') as f:
    progress = json.load(f)
progress['checkpoints']['{N}'] = {'status': 'completed', 'timestamp': '...'}
progress['current_checkpoint'] = {N+1}
with open('_state/productspecs_progress.json', 'w') as f:
    json.dump(progress, f, indent=2)
"
```

### 5. Completion

Log command end and display summary:

```bash
python3 .claude/hooks/command_end.py \
  --command-name "/productspecs" \
  --stage "productspecs" \
  --status "completed" \
  --start-event-id "$EVENT_ID" \
  --outputs '{"checkpoints": 8, "modules": N, "tests": M}'
```

---

## CRITICAL: Parallel Agent Spawning

**You MUST spawn agents in parallel when indicated.** To do this, include multiple Task tool calls in a SINGLE message. Example:

```
<message>
I'll now spawn the module generation agents in parallel.

Task({ subagent_type: "general-purpose", model: "sonnet", description: "UI specs", prompt: "..." })
Task({ subagent_type: "general-purpose", model: "sonnet", description: "API specs", prompt: "..." })
Task({ subagent_type: "general-purpose", model: "sonnet", description: "NFR specs", prompt: "..." })
</message>
```

This ensures true parallel execution for maximum performance.
