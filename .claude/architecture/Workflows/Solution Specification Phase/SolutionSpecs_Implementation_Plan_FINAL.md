# ProductSpecs Multi-Agent Implementation Plan (FINAL)

**Version**: 2.0 Final
**Date**: 2026-01-27
**Status**: Approved - Ready for Implementation

---

## Executive Summary

**Approved Architecture**: Option B (Hierarchical) + Option C (Reflexion - Hybrid)

**Key Decisions**:
- ✅ Hierarchical orchestration (Master → 3 Sub-Orchestrators → Agents)
- ✅ Self-validation with Haiku (catches errors early)
- ✅ Reflexion using thin wrapper (productspecs-vp-reviewer) over discovery-vp-pm-reviewer
- ✅ Hybrid reflexion: Per-module for P0, per-checkpoint for P1/P2
- ✅ Auto-trigger: Self-validation score < 70
- ✅ 7 entry points (system/module/feature/screen/persona/subsystem/layer)
- ✅ Full hooks integration (logging, validation, version tracking)

**Expected Performance** (20 modules, 5 P0):
| Metric | v1.0 | v2.0 Standard | v2.0 + Auto-Reflexion | v2.0 --quality critical |
|--------|------|---------------|----------------------|------------------------|
| Time | 16 min | 18 min (+12%) | 24 min (+50%) | 35 min (+119%) |
| Cost | $53 | $60 (+13%) | $85 (+60%) | $120 (+126%) |
| Quality | 75 | 85 (+13%) | 92 (+23%) | 96 (+28%) |

---

## 1. Final Architecture

### 1.1 Hierarchical Orchestration (Option B)

```
productspecs.md (Command)
    ↓
productspecs-orchestrator.md (Master, Sonnet)
    ├─ Parse flags (--module/--feature/--screen/--persona/--subsystem/--layer/--quality)
    ├─ Filter scope
    ├─ Load priority map (P0/P1/P2)
    └─ Spawn sub-orchestrators
    ↓
┌─────────────────────────────────────────────────────────┐
│ CP-3-4: Module Generation                                │
│                                                          │
│ productspecs-module-orchestrator.md (Sonnet)            │
│   ├─ Load filtered modules with priority                │
│   ├─ Spawn 3 agents (UI, API, NFR)                      │
│   └─ For each module:                                   │
│       ├─ Agent generates spec                           │
│       ├─ Self-Validator (Haiku) validates               │
│       ├─ [Score < 70] → VP-Reviewer (auto-trigger) ⚠️   │
│       ├─ [Priority = P0] → VP-Reviewer (mandatory) ⚠️   │
│       └─ Return to sub-orchestrator                     │
│   ↓                                                      │
│   Merge Gate: Consolidate module_registry.json          │
│   ├─ [--quality critical] → VP-Reviewer (all) ⚠️        │
│   ├─ [Score < 70 for P1/P2] → VP-Reviewer (batch) ⚠️    │
│   └─ Return to master                                   │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ CP-6: Test Generation                                    │
│                                                          │
│ productspecs-test-orchestrator.md (Sonnet)              │
│   ├─ Spawn 4 agents (Unit, Integration, E2E, PICT)      │
│   ├─ Each agent self-validates                          │
│   └─ Merge gate consolidates                            │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│ CP-7: Global Validation (BLOCKING)                       │
│                                                          │
│ productspecs-validation-orchestrator.md (Sonnet)        │
│   ├─ Spawn 3 validators (parallel)                      │
│   ├─ Check blocking criteria                            │
│   └─ BLOCK if failed                                    │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Reflexion Integration (Option C - Hybrid)

**Agent**: `productspecs-vp-reviewer.md` (Thin wrapper over discovery-vp-pm-reviewer)

**Trigger Rules**:
1. **Auto-trigger (per-module)**:
   - Self-validation score < 70 (any priority)
   - Priority = P0 (always, even if score ≥ 70)

2. **Batch review (per-checkpoint)**:
   - End of CP-3-4: Review all P1/P2 modules with score ≥ 70
   - End of CP-6: Review test coverage gaps

3. **Full review (--quality critical flag)**:
   - ALL modules get VP review (P0, P1, P2)
   - Per-module reviews (not batch)

**Wrapper Prompt** (productspecs-vp-reviewer.md):
```markdown
Read: .claude/agents/discovery-vp-pm-reviewer.md

Load skill: thinking-critically

Context: ProductSpecs Stage
Artifact: {module_id} or {checkpoint_phase}
Priority: {P0/P1/P2}
Self-Validation Score: {score}

Review Focus:
- User needs alignment (Does spec address pain points?)
- Implementation clarity (Can developer implement this?)
- Testability (Are acceptance criteria testable?)
- Edge cases (Are error scenarios handled?)
- Security/privacy (Are considerations addressed?)

Use critical thinking skills:
- Five Whys (root cause of quality gaps)
- Gap analysis (missing requirements, unclear criteria)
- Risk assessment (implementation risks, ambiguities)

RETURN JSON:
{
  "review_type": "per_module" | "per_checkpoint",
  "module_id": "{module_id}",
  "overall_score": 85,
  "critical_issues": [],
  "improvement_areas": [],
  "gap_analysis": "",
  "recommended_actions": [],
  "approval": "approved" | "needs_rework"
}
```

**Integration Points**:
1. **Module-Orchestrator**: After self-validation, check if VP review needed
2. **Module-Orchestrator**: End of checkpoint, batch review P1/P2 with score ≥ 70
3. **Test-Orchestrator**: End of checkpoint, review test coverage gaps

---

## 2. Agent Specifications

### 2.1 New Agents (6 Total)

#### **Orchestrators (4)**

| Agent ID | File | Model | Purpose |
|----------|------|-------|---------|
| `productspecs-orchestrator` | productspecs-orchestrator.md | Sonnet | Master coordinator, scope filtering, lifecycle |
| `productspecs-module-orchestrator` | productspecs-module-orchestrator.md | Sonnet | Module generation, self-validation, VP review coordination |
| `productspecs-test-orchestrator` | productspecs-test-orchestrator.md | Sonnet | Test generation, self-validation |
| `productspecs-validation-orchestrator` | productspecs-validation-orchestrator.md | Sonnet | Global validation, blocking gate |

#### **Validation (1)**

| Agent ID | File | Model | Purpose |
|----------|------|-------|---------|
| `productspecs-self-validator` | productspecs-self-validator.md | Haiku | Per-agent format/checklist validation (15 checks) |

#### **Reflexion (1 - Thin Wrapper)**

| Agent ID | File | Model | Purpose |
|----------|------|-------|---------|
| `productspecs-vp-reviewer` | productspecs-vp-reviewer.md | Sonnet | Wrapper over discovery-vp-pm-reviewer for ProductSpecs review |

**Note**: discovery-vp-pm-reviewer agent is reused (no new agent creation needed, just wrapper).

---

### 2.2 Enhanced Existing Agents (7)

**Add self-validation + VP review integration**:

| Agent ID | Enhancement | Self-Validation | VP Review Trigger |
|----------|-------------|-----------------|-------------------|
| `productspecs-ui-module-specifier` | Add self-validator call + retry logic | ✅ | Score < 70 or P0 |
| `productspecs-api-module-specifier` | Add self-validator call + retry logic | ✅ | Score < 70 or P0 |
| `productspecs-nfr-generator` | Add self-validator call | ✅ | Score < 70 |
| `productspecs-unit-test-specifier` | Add self-validator call, change to Haiku | ✅ | N/A |
| `productspecs-integration-test-specifier` | Add self-validator call | ✅ | N/A |
| `productspecs-e2e-test-specifier` | Add self-validator call | ✅ | N/A |
| `productspecs-pict-combinatorial` | Add self-validator call | ✅ | N/A |

**No changes**:
- productspecs-traceability-validator
- productspecs-cross-reference-validator
- productspecs-spec-reviewer

---

## 3. Hooks Integration

### 3.1 Logging Hooks (Mandatory)

**For ALL agents and commands**:

#### **Agent Execution Logging**

**Before agent starts**:
```bash
EVENT_ID=$(python3 .claude/hooks/skill_invoke.py \
  --skill-name "productspecs-module-orchestrator" \
  --action start \
  --stage "productspecs" \
  --system-name "{SystemName}" \
  --intent "Generate module specifications with self-validation and VP review")
```

**After agent completes**:
```bash
python3 .claude/hooks/skill_invoke.py \
  --skill-name "productspecs-module-orchestrator" \
  --action end \
  --start-event-id "$EVENT_ID" \
  --status "completed" \
  --outputs '{"files_written": ["01-modules/module-index.md"], "modules_generated": 20}'
```

**Logged to**: `_state/pipeline_progress.json`

---

#### **Command Execution Logging**

**Before checkpoint starts**:
```bash
EVENT_ID=$(python3 .claude/hooks/command_start.py \
  --command-name "/productspecs-checkpoint-3" \
  --stage "productspecs" \
  --system-name "{SystemName}" \
  --intent "Generate module specifications")
```

**After checkpoint completes**:
```bash
python3 .claude/hooks/command_end.py \
  --command-name "/productspecs-checkpoint-3" \
  --stage "productspecs" \
  --status "completed" \
  --start-event-id "$EVENT_ID" \
  --outputs '{"checkpoint": 3, "modules": 20, "vp_reviews": 5}'
```

---

### 3.2 Version Logging Hooks (Mandatory)

**After every file write/edit/delete**:

```bash
python3 .claude/hooks/version_history_logger.py \
  "traceability/" \
  "{SystemName}" \
  "productspecs" \
  "Claude" \
  "{version}" \
  "{reason}" \
  "{refs}" \
  "{file_path}" \
  "{action}"
```

**Parameters**:
- `system_name`: From `_state/productspecs_config.json`
- `stage`: `productspecs`
- `version`: From `.claude/version.json` (Major.Minor) + local Patch
- `reason`: "Generated module specification" | "Updated after VP review" | etc.
- `refs`: Comma-separated IDs (e.g., `REQ-015,SCR-003,PP-1.2`)
- `action`: `creation` | `modification` | `deletion`

**Logged to**: `traceability/{SystemName}_version_history.json`

---

### 3.3 Validation Hooks (Mandatory)

**After each checkpoint completes**:

```bash
python3 .claude/hooks/productspecs_quality_gates.py \
  --validate-checkpoint {N} \
  --dir "ProductSpecs_{SystemName}/"
```

**After file creation**:

```bash
python3 .claude/hooks/productspecs_quality_gates.py \
  --validate-file "ProductSpecs_{SystemName}/01-modules/ui/MOD-INV-SEARCH-01.md"
```

**After CP-7 (blocking gate)**:

```bash
python3 .claude/hooks/productspecs_quality_gates.py \
  --validate-traceability \
  --dir "ProductSpecs_{SystemName}/"
```

**Validation outputs**:
- Checkpoint validation: Pass/fail with error details
- File validation: Format/content checks
- Traceability validation: P0 coverage, dangling references

---

### 3.4 Agent Session Tracking (Mandatory)

**Before agent spawns**:
```python
# Log agent session start
session_id = f"productspecs-module-orchestrator-{timestamp}"
register_agent_session(
    agent_id="productspecs-module-orchestrator",
    session_id=session_id,
    status="running",
    checkpoint="3",
    parent_session=master_session_id
)
```

**After agent completes**:
```python
# Update agent session
update_agent_session(
    session_id=session_id,
    status="completed",
    files_written=["01-modules/module-index.md"],
    duration_seconds=120
)
```

**Logged to**: `_state/agent_sessions.json`

---

## 4. Entry Points (7 Types)

### 4.1 Command Syntax

**System-Level** (Default):
```bash
/productspecs InventorySystem
```

**Module-Level**:
```bash
/productspecs InventorySystem --module MOD-INV-SEARCH-01
```

**Feature-Level**:
```bash
/productspecs InventorySystem --feature SEARCH
```

**Screen-Level**:
```bash
/productspecs InventorySystem --screen SCR-003
```

**Persona-Level**:
```bash
/productspecs InventorySystem --persona admin
```

**Subsystem-Level**:
```bash
/productspecs InventorySystem --subsystem middleware
```

**Layer-Level**:
```bash
/productspecs InventorySystem --layer frontend
```

**Quality Flag**:
```bash
/productspecs InventorySystem --quality critical
# Enables: ALL modules get VP review (P0, P1, P2), per-module reviews
```

### 4.2 Scope Filtering Implementation

**Location**: `productspecs-orchestrator.md` (Master)

**Algorithm**:
```python
def filter_scope(system_name, flags):
    # Load registries
    req_registry = load_json("traceability/requirements_registry.json")
    module_registry = load_json("traceability/module_registry.json")

    if flags.module:
        modules = [m for m in module_registry if m["id"] == flags.module]
    elif flags.feature:
        modules = [m for m in module_registry if flags.feature.lower() in m["id"].lower()]
    elif flags.screen:
        modules = [m for m in module_registry if flags.screen in m["sources"]["screens"]]
    elif flags.persona:
        modules = [m for m in module_registry if flags.persona in m["personas"]]
    elif flags.subsystem:
        modules = [m for m in module_registry if m["subsystem"] == flags.subsystem]
    elif flags.layer:
        modules = [m for m in module_registry if m["layer"] == flags.layer]
    else:
        modules = module_registry  # All modules

    # Validate scope
    if len(modules) == 0:
        raise ValueError(f"No modules found for scope: {flags}")

    # Add priority and reflexion flags
    for module in modules:
        module["needs_vp_review"] = (
            flags.quality_critical or  # --quality critical
            module["priority"] == "P0"  # Always review P0
        )

    return {
        "type": flags.get_type(),  # "module", "feature", etc.
        "value": flags.get_value(),
        "modules": modules,
        "total_modules": len(modules)
    }
```

---

## 5. Self-Validation Protocol

### 5.1 Checklist (15 Checks)

**Agent**: `productspecs-self-validator.md` (Haiku)

**Checks**:

#### **Frontmatter (5 checks)**
1. `id` field matches format `MOD-{APP}-{FEATURE}-{NN}`
2. `title` field exists and descriptive
3. `type` field is `ui`, `api`, or `integration`
4. `layer` field is `frontend`, `backend`, `middleware`, or `database`
5. `priority` field is `P0`, `P1`, or `P2`

#### **Traceability (4 checks)**
6. `sources.requirements` all IDs exist in requirements_registry.json
7. `sources.screens` all IDs exist in Prototype screens
8. `sources.pain_points` IDs exist (optional)
9. No dangling references

#### **Content Completeness (4 checks)**
10. "Acceptance Criteria" section with ≥3 criteria
11. "User Stories" section with format "As a... I want... So that..."
12. "Technical Requirements" section
13. "Dependencies" section (list of other modules)

#### **Naming & Format (2 checks)**
14. File path matches ID (MOD-INV-SEARCH-01.md)
15. ID format correct (MOD-{APP}-{FEATURE}-{NN})

**Output**:
```json
{
  "valid": true,
  "errors": [],
  "warnings": ["No security considerations section"],
  "quality_score": 87,
  "checked_items": 15,
  "failed_items": 0,
  "needs_vp_review": false  // true if score < 70
}
```

### 5.2 Retry Logic (in parent agent)

```python
retry_count = 0
max_retries = 2

while retry_count <= max_retries:
    generate_module_spec(module_id)
    result = spawn_self_validator(module_id)

    if result["valid"] and result["quality_score"] >= 70:
        # Success - check if VP review needed
        if module["priority"] == "P0" or result["quality_score"] < 70:
            vp_result = spawn_vp_reviewer(module_id, result)
            if vp_result["approval"] == "needs_rework":
                retry_count += 1
                continue
        return {"status": "completed", "quality_score": result["quality_score"]}
    else:
        retry_count += 1
        if retry_count <= max_retries:
            error_context = result["errors"]
        else:
            log_failure(f"Max retries exceeded for {module_id}")
            return {"status": "failed", "errors": result["errors"]}
```

---

## 6. VP Reviewer Integration

### 6.1 Agent: productspecs-vp-reviewer.md

**Purpose**: Thin wrapper over discovery-vp-pm-reviewer for ProductSpecs context

**Trigger Conditions**:
1. **Per-module (auto)**:
   - Self-validation score < 70 (any priority)
   - Module priority = P0 (always)

2. **Per-checkpoint (batch)**:
   - End of CP-3-4: Review all P1/P2 modules with score ≥ 70
   - End of CP-6: Review test coverage gaps

3. **--quality critical flag**:
   - All modules get per-module VP review

**Agent Prompt**:
```markdown
---
name: productspecs-vp-reviewer
description: VP Product Manager review for ProductSpecs artifacts using critical thinking
context: fork
agent: general-purpose
model: sonnet
---

# ProductSpecs VP Reviewer Agent

## Purpose
Perform VP-level critical review of ProductSpecs artifacts (module specs, test specs) using 30 years of PM experience and critical thinking skills.

## Phase 1: Load Discovery VP PM Reviewer

Read: .claude/agents/discovery-vp-pm-reviewer.md

Load skills:
- thinking-critically
- making-product-decisions

## Phase 2: Load Context

**Review Type**: {per_module | per_checkpoint}
**Module ID**: {module_id} (if per_module)
**Checkpoint**: {checkpoint_number} (if per_checkpoint)
**Priority**: {P0 | P1 | P2}
**Self-Validation Score**: {score}

**Artifact Path**: ProductSpecs_{SystemName}/01-modules/{type}/{module_id}.md

Load:
- Module specification file
- traceability/requirements_registry.json (source requirements)
- traceability/module_registry.json (context)
- Prototype screen specs (if UI module)

## Phase 3: Critical Review

Use thinking-critically skill to perform:

### 3.1 Five Whys Analysis
If quality score < 70, use Five Whys to identify root causes:
- Why is acceptance criteria unclear?
- Why are technical requirements vague?
- Why are edge cases missing?
- Why is security not addressed?
- Why is testability unclear?

### 3.2 Gap Analysis
Identify gaps:
- **User Needs**: Does spec address pain points from sources.pain_points?
- **Requirements Coverage**: Are all sources.requirements addressed?
- **Implementation Clarity**: Can developer implement without ambiguity?
- **Testability**: Are acceptance criteria testable?
- **Edge Cases**: Are error scenarios handled?
- **Security/Privacy**: Are considerations addressed?

### 3.3 Risk Assessment
Assess risks:
- **Implementation Risk**: Unclear requirements, missing dependencies
- **Quality Risk**: Vague acceptance criteria, no edge cases
- **Security Risk**: No security considerations, data privacy gaps
- **Testability Risk**: Untestable criteria, missing test scenarios

## Phase 4: Generate Review Report

RETURN JSON:
{
  "review_type": "per_module",
  "module_id": "MOD-INV-SEARCH-01",
  "overall_score": 85,
  "perspective_scores": {
    "user_needs": 90,
    "implementation_clarity": 85,
    "testability": 80,
    "security": 80
  },
  "critical_issues": [
    "Missing error handling for search timeout",
    "No security consideration for PII in search results"
  ],
  "improvement_areas": [
    "Add acceptance criteria for edge case: empty search results",
    "Clarify technical requirement: Search index refresh frequency"
  ],
  "gap_analysis": "Spec addresses 95% of requirements but missing edge cases...",
  "five_whys_insights": [
    "Why unclear? → No examples provided → Need concrete scenarios",
    "Why untestable? → Vague criteria → Need measurable thresholds"
  ],
  "recommended_actions": [
    "Add edge case handling for empty results",
    "Add security section for PII handling",
    "Add performance criteria: Search response time < 500ms"
  ],
  "approval": "approved_with_recommendations",
  "needs_rework": false
}

## Phase 5: Return to Orchestrator

If approval = "needs_rework":
  - Parent agent must regenerate spec with feedback
  - Max 1 VP review rework (to avoid infinite loops)

If approval = "approved" or "approved_with_recommendations":
  - Parent agent logs recommendations
  - Proceeds to next module
```

**Skills Used**:
- `thinking-critically`: Five Whys, gap analysis, root cause analysis
- `making-product-decisions`: Risk assessment, trade-off analysis

---

### 6.2 Integration in Module-Orchestrator

**After self-validation**:
```python
# Self-validation complete
self_val_result = spawn_self_validator(module_id)

# Check if VP review needed
if (module["priority"] == "P0" or
    self_val_result["quality_score"] < 70 or
    flags.quality_critical):

    # Spawn VP reviewer
    vp_result = spawn_vp_reviewer(
        module_id=module_id,
        self_val_score=self_val_result["quality_score"],
        review_type="per_module"
    )

    if vp_result["approval"] == "needs_rework":
        # Regenerate with VP feedback
        regenerate_with_feedback(module_id, vp_result["recommended_actions"])
        # Re-run self-validation + VP review (max 1 rework)
    else:
        log_recommendations(module_id, vp_result["improvement_areas"])
```

**After checkpoint (batch review for P1/P2)**:
```python
# End of CP-3-4
completed_modules = get_completed_modules()
p1_p2_modules = [m for m in completed_modules
                 if m["priority"] in ["P1", "P2"]
                 and m["quality_score"] >= 70]

if len(p1_p2_modules) > 0 and not flags.quality_critical:
    # Batch VP review
    vp_result = spawn_vp_reviewer(
        modules=p1_p2_modules,
        review_type="per_checkpoint"
    )

    # Log recommendations for each module
    for module_id, recommendations in vp_result["module_recommendations"].items():
        log_recommendations(module_id, recommendations)
```

---

## 7. Registry Updates

### 7.1 PRODUCTSPECS_AGENT_REGISTRY.json v2.0

**New Fields**:
- `sub_orchestrator`: Links agent to its orchestrator
- `self_validation`: Boolean flag
- `self_validator_agent`: Agent to call for self-validation
- `vp_review_trigger`: Conditions for VP review
- `reflexion_enabled`: Boolean flag

**Example Entry**:
```json
{
  "agent_id": "productspecs-ui-module-specifier",
  "file": "productspecs-ui-module-specifier.md",
  "category": "specification",
  "model": "sonnet",
  "purpose": "Generate UI module specifications with self-validation and VP review",
  "phases": ["3", "4"],
  "spawn_strategy": "singleton",
  "parallel_group": "module-gen",
  "sub_orchestrator": "productspecs-module-orchestrator",
  "self_validation": true,
  "self_validator_agent": "productspecs-self-validator",
  "vp_review_trigger": {
    "auto": ["score_below_70", "priority_P0"],
    "manual": ["quality_critical_flag"]
  },
  "reflexion_enabled": true,
  "skills_required": [
    "ProductSpecs_Generator",
    "ProductSpecs_Traceability"
  ],
  "expected_outputs": [
    "01-modules/ui/MOD-{APP}-{FEATURE}-{NN}.md",
    "module_registry_{MODULE_ID}.json"
  ],
  "timeout_ms": 120000
}
```

**New Agent Entry** (VP Reviewer):
```json
{
  "agent_id": "productspecs-vp-reviewer",
  "file": "productspecs-vp-reviewer.md",
  "category": "reflexion",
  "model": "sonnet",
  "purpose": "VP PM review using discovery-vp-pm-reviewer with ProductSpecs context",
  "phases": ["3", "4", "6"],
  "spawn_strategy": "per_module_or_per_checkpoint",
  "parallel_group": null,
  "sub_orchestrator": "productspecs-module-orchestrator",
  "self_validation": false,
  "blocking_gate": false,
  "reflexion_enabled": true,
  "reuses_agent": "discovery-vp-pm-reviewer",
  "skills_required": [
    "thinking-critically",
    "making-product-decisions"
  ],
  "expected_outputs": [
    "vp_review_result.json"
  ],
  "timeout_ms": 180000
}
```

---

## 8. Command Updates

### 8.1 productspecs.md Command

**Add flags**:
```bash
/productspecs <SystemName> [OPTIONS]

OPTIONS:
  --module MOD-XXX          Process single module
  --feature FEATURE_NAME    Process all modules in feature
  --screen SCR-XXX          Process all modules linked to screen
  --persona PERSONA_NAME    Process all modules for persona
  --subsystem SUBSYSTEM     Process all modules in subsystem
  --layer LAYER             Process all modules in layer (frontend/backend/db)
  --quality critical        Enable VP review for ALL modules (per-module)
  --from-checkpoint N       Resume from checkpoint N
```

**Updated Orchestration**:
```markdown
## Phase 1: Initialize

Load hooks:
```bash
EVENT_ID=$(python3 .claude/hooks/command_start.py \
  --command-name "/productspecs" \
  --stage "productspecs" \
  --system-name "{SystemName}" \
  --intent "Generate ProductSpecs with hierarchical orchestration and VP review")
```

## Phase 2: Parse Flags and Filter Scope

Parse command flags:
- --module, --feature, --screen, --persona, --subsystem, --layer
- --quality critical
- --from-checkpoint N

Filter scope using master orchestrator:
```python
scope = filter_scope(system_name, flags)
```

## Phase 3: Spawn Sub-Orchestrators

For each checkpoint:
1. Check if resume (--from-checkpoint)
2. Spawn sub-orchestrator with filtered scope
3. Wait for completion
4. Log checkpoint completion

## Phase 4: End

Call command_end.py hook:
```bash
python3 .claude/hooks/command_end.py \
  --command-name "/productspecs" \
  --stage "productspecs" \
  --status "completed" \
  --start-event-id "$EVENT_ID" \
  --outputs '{"checkpoints": 8, "modules": 20, "vp_reviews": 5}'
```
```

---

## 9. Performance Projections (Updated)

### 9.1 Small System (10 Modules, 2 P0)

| Version | Time | Cost | VP Reviews | Quality Score |
|---------|------|------|------------|---------------|
| v1.0 | 12 min | $32 | 0 | 75 |
| v2.0 Standard | 14 min | $36 | 0 | 85 |
| v2.0 Auto-Reflexion | 17 min | $48 | 2 P0 + 0 batch | 92 |
| v2.0 --quality critical | 25 min | $70 | 10 per-module | 96 |

---

### 9.2 Medium System (20 Modules, 5 P0)

| Version | Time | Cost | VP Reviews | Quality Score |
|---------|------|------|------------|---------------|
| v1.0 | 16 min | $53 | 0 | 75 |
| v2.0 Standard | 18 min | $60 | 0 | 85 |
| v2.0 Auto-Reflexion | 24 min | $85 | 5 P0 + 1 batch | 92 |
| v2.0 --quality critical | 35 min | $120 | 20 per-module | 96 |

**Auto-Reflexion Breakdown**:
- 5 P0 modules: 5 × 3 min = 15 min (per-module VP review)
- 15 P1/P2 modules: Self-validation only (0 VP reviews if score ≥ 70)
- Batch VP review at end: 1 × 4 min = 4 min (all P1/P2 modules)
- Total VP overhead: 19 min - 18 min = +6 min
- Total cost: $60 + $25 (5 P0 reviews @ $5 each) = $85

---

### 9.3 Large System (50 Modules, 10 P0)

| Version | Time | Cost | VP Reviews | Quality Score |
|---------|------|------|------------|---------------|
| v1.0 | 21 min | $88 | 0 | 75 |
| v2.0 Standard | 24 min | $100 | 0 | 85 |
| v2.0 Auto-Reflexion | 36 min | $150 | 10 P0 + 1 batch | 92 |
| v2.0 --quality critical | 60 min | $250 | 50 per-module | 96 |

---

## 10. Implementation Tasks

### Phase 1: Core Architecture (Week 1) - 5 Days

**Tasks**:
1. Create master orchestrator (productspecs-orchestrator.md)
2. Create module orchestrator (productspecs-module-orchestrator.md)
3. Create test orchestrator (productspecs-test-orchestrator.md)
4. Create validation orchestrator (productspecs-validation-orchestrator.md)
5. Create self-validator (productspecs-self-validator.md)
6. Update registry (PRODUCTSPECS_AGENT_REGISTRY.json v2.0)

---

### Phase 2: Self-Validation Integration (Week 1-2) - 3 Days

**Tasks**:
7. Enhance productspecs-ui-module-specifier.md (add self-validation)
8. Enhance productspecs-api-module-specifier.md (add self-validation)
9. Enhance productspecs-nfr-generator.md (add self-validation)
10. Enhance productspecs-unit-test-specifier.md (add self-validation, change to Haiku)
11. Enhance productspecs-integration-test-specifier.md (add self-validation)
12. Enhance productspecs-e2e-test-specifier.md (add self-validation)
13. Enhance productspecs-pict-combinatorial.md (add self-validation)

---

### Phase 3: VP Reviewer Integration (Week 2) - 3 Days

**Tasks**:
14. Create productspecs-vp-reviewer.md (thin wrapper)
15. Integrate VP review in module-orchestrator (per-module auto-trigger)
16. Integrate VP review in module-orchestrator (per-checkpoint batch review)
17. Add --quality critical flag handling in master orchestrator

---

### Phase 4: Entry Points (Week 2-3) - 3 Days

**Tasks**:
18. Implement scope filtering in master orchestrator (7 entry point types)
19. Add fuzzy matching for feature names
20. Add scope validation (error handling for invalid scopes)
21. Update productspecs.md command (add 7 flags)

---

### Phase 5: Hooks Integration (Week 3) - 2 Days

**Tasks**:
22. Add command_start/end hooks to master orchestrator
23. Add skill_invoke hooks to all 6 new agents
24. Add version_history_logger hooks to all agents (after file write)
25. Add quality_gates validation hooks to all orchestrators (after checkpoint)
26. Add agent session tracking to all orchestrators

---

### Phase 6: Registry & Documentation (Week 3-4) - 3 Days

**Tasks**:
27. Finalize PRODUCTSPECS_AGENT_REGISTRY.json v2.0
28. Update PRODUCTSPECS_COMMAND_REFERENCE.md (document new flags)
29. Create ProductSpecs_MultiAgent_Architecture.md (workflow docs)
30. Create ProductSpecs_Performance_Benchmarks.md
31. Update CLAUDE.md (ProductSpecs v2.0 section)

---

### Phase 7: Testing & Validation (Week 4) - 2 Days

**Tasks**:
32. Integration test: Discovery → Prototype → ProductSpecs v2.0
33. Test system-level entry point (backward compatibility)
34. Test module-level entry point (--module)
35. Test feature-level entry point (--feature)
36. Test VP review auto-trigger (score < 70)
37. Test VP review P0 modules (mandatory)
38. Test --quality critical flag (all modules)
39. Regression test: v2.0 outputs match v1.0 (same input, standard mode)

---

**Total Duration**: 4 weeks (21 tasks across 7 phases)

**Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 5 → Phase 7

---

## 11. Success Criteria

**Phase 1 Success**:
- ✅ 4 orchestrators created and functional
- ✅ Self-validator created with 15 checks
- ✅ Registry updated to v2.0
- ✅ System-level entry point works (backward compatible)

**Phase 2 Success**:
- ✅ All 7 spec/test agents call self-validator
- ✅ Retry logic works (max 2 retries)
- ✅ Self-validation catches intentional errors

**Phase 3 Success**:
- ✅ VP reviewer wrapper created
- ✅ Auto-trigger works (score < 70 and P0 modules)
- ✅ Batch review works (P1/P2 at end of checkpoint)
- ✅ --quality critical flag works (all modules per-module review)

**Phase 4 Success**:
- ✅ All 7 entry points functional
- ✅ Scope filtering accurate (0 bugs in testing)
- ✅ Module-level entry point = 80% time savings

**Phase 5 Success**:
- ✅ All agents log to pipeline_progress.json
- ✅ All file writes log to version_history.json
- ✅ All checkpoints validate via quality_gates.py

**Phase 6 Success**:
- ✅ Registry complete with all new fields
- ✅ Documentation complete (3 new docs)
- ✅ Command reference updated

**Phase 7 Success**:
- ✅ End-to-end test passes (Discovery → Prototype → ProductSpecs v2.0)
- ✅ Regression test passes (v2.0 outputs match v1.0)
- ✅ All 8 test cases pass

---

## 12. Appendix

### 12.1 File Checklist

**New Files (9)**:
- `.claude/agents/productspecs-orchestrator.md`
- `.claude/agents/productspecs-module-orchestrator.md`
- `.claude/agents/productspecs-test-orchestrator.md`
- `.claude/agents/productspecs-validation-orchestrator.md`
- `.claude/agents/productspecs-self-validator.md`
- `.claude/agents/productspecs-vp-reviewer.md`
- `.claude/architecture/workflows/ProductSpecs Phase/ProductSpecs_MultiAgent_Architecture.md`
- `.claude/architecture/workflows/ProductSpecs Phase/ProductSpecs_Performance_Benchmarks.md`
- `.claude/architecture/SolutionSpecs_Implementation_Plan_FINAL.md` (this file)

**Updated Files (11)**:
- `.claude/skills/PRODUCTSPECS_AGENT_REGISTRY.json` (v1.0 → v2.0)
- `.claude/commands/productspecs.md`
- `.claude/commands/PRODUCTSPECS_COMMAND_REFERENCE.md`
- `.claude/agents/productspecs-ui-module-specifier.md`
- `.claude/agents/productspecs-api-module-specifier.md`
- `.claude/agents/productspecs-nfr-generator.md`
- `.claude/agents/productspecs-unit-test-specifier.md`
- `.claude/agents/productspecs-integration-test-specifier.md`
- `.claude/agents/productspecs-e2e-test-specifier.md`
- `.claude/agents/productspecs-pict-combinatorial.md`
- `CLAUDE.md`

---

## 13. Conclusion

This finalized implementation plan delivers:

✅ **Hierarchical orchestration** (4 orchestrators)
✅ **Self-validation** (15-check Haiku validator)
✅ **VP review integration** (hybrid: per-module P0, per-checkpoint P1/P2)
✅ **Auto-trigger** (score < 70 or P0)
✅ **7 entry points** (80% time savings for module-level)
✅ **Full hooks integration** (logging, validation, version tracking)
✅ **Backward compatible** (v2.0 standard mode ≈ v1.0 performance)

**Expected Benefits**:
- +30% reduction in merge gate failures (self-validation)
- +13% quality improvement (score 75 → 85 standard, 92 with auto-reflexion)
- +80% time savings for single-module updates (module-level entry point)
- -33% context reduction (15k → 10k peak)

**Acceptable Trade-Offs**:
- +12% time overhead (16 min → 18 min standard)
- +13% cost increase ($53 → $60 standard)
- +50% time with auto-reflexion (18 min → 24 min for 5 P0 modules)

---

**Status**: Ready for Implementation
**Next Step**: Create implementation tasks and begin Phase 1
