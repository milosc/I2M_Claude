---
name: productspecs-modules
description: Generate module specifications from prototype screens
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-modules started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-modules ended '{"stage": "productspecs"}'
---


# /productspecs-modules - Generate Module Specifications

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs-modules instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for module ID management:

```bash
# Load Traceability rules (includes module ID format MOD-XXX-XXX-NN)
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Required: `<SystemName>`

## Prerequisites

- `/productspecs-extract <SystemName>` completed (Checkpoint 2 passed)

## Skills Used

Read BEFORE execution:
- `.claude/skills/ProductSpecs_Generator/SKILL.md`

## Execution Steps

### Step 1: Verify Checkpoint 2

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 2 --dir ProductSpecs_<SystemName>/
```

If not passed, show error and exit.

### Step 2: Load Configuration

```python
# From shared _state/ at ROOT level
config = json.load("_state/productspecs_config.json")
system_name = config["system_name"]
prototype_path = config["prototype_path"]
output_path = config["output_path"]

# Load registries
requirements = json.load(f"{output_path}/_registry/requirements.json")
traceability = json.load(f"{output_path}/_registry/traceability.json")
discovery_summary = json.load("_state/discovery_summary.json")
screen_registry = json.load("traceability/screen_registry.json")
```

### Step 2.5: NFR Conflict Resolution

Check for conflicting non-functional requirements (e.g., Security vs. Performance):

```python
conflicts = detect_nfr_conflicts(nfrs)

if conflicts:
    USE AskUserQuestion:
      question: "These non-functional requirements may conflict. Which should take priority?"
      header: "NFR Priority"
      options:
        - label: "Performance first"
          description: "Optimize for speed, may require security tradeoffs"
        - label: "Security first (Recommended)"
          description: "Prioritize security, accept performance overhead"
        - label: "Balanced"
          description: "Compromise on both, moderate tradeoffs"
    
    STORE selection in _state/productspecs_config.json
```

### Step 3: Derive Module Structure

Group screens into logical modules based on:

| Criteria | Description |
|----------|-------------|
| Workflow | Screens sharing same workflow |
| Entity | Screens with shared primary entity |
| Persona | Screens for same persona/role |
| Navigation | Screens with sequential navigation |

```python
module_map = {}
for screen in screens:
    # Determine module assignment
    module_id = derive_module_id(screen)

    if module_id not in module_map:
        module_map[module_id] = {
            "id": module_id,
            "name": derive_module_name(screen),
            "app": screen["app"],
            "screens": [],
            "primary_entity": None,
            "primary_persona": None,
            "workflows": [],
            "requirements": [],
            "priority": "P1"  # Default, upgraded to P0 if any P0 req
        }

    module_map[module_id]["screens"].append(screen["id"])
```

### Step 4: Generate Module Index

Write `ProductSpecs_<SystemName>/01-modules/module-index.md`:

```markdown
# Module Index

**System**: <SystemName>
**Generated**: <TIMESTAMP>
**Total Modules**: <N>

---

## Modules by Priority

### P0 - Must Have

| Module ID | Name | App | Screens | Requirements |
|-----------|------|-----|---------|--------------|
| MOD-INV-SEARCH-01 | Inventory Search | Mobile | 3 | 5 P0, 2 P1 |
| ... | ... | ... | ... | ... |

### P1 - Should Have

| Module ID | Name | App | Screens | Requirements |
|-----------|------|-----|---------|--------------|
| ... | ... | ... | ... | ... |

### P2 - Nice to Have

| Module ID | Name | App | Screens | Requirements |
|-----------|------|-----|---------|--------------|
| ... | ... | ... | ... | ... |

---

## Modules by App

### Mobile App (INV)

| Module ID | Name | Screens | Priority |
|-----------|------|---------|----------|
| MOD-INV-SEARCH-01 | Inventory Search | M-01, M-02 | P0 |
| ... | ... | ... | ... |

### Desktop App (DSK)

| Module ID | Name | Screens | Priority |
|-----------|------|---------|----------|
| ... | ... | ... | ... |

---

## Traceability Summary

| Metric | Count |
|--------|-------|
| Total Modules | <N> |
| P0 Modules | <N> |
| Screens Covered | <N>/<N> |
| Requirements Traced | <N>/<N> |
```

### Step 5: Generate Core Module Specs (Phase 3)

For each P0 module, generate full specification:

```markdown
---
document_id: MOD-<APP>-<FEAT>-<NN>
version: 1.0.0
created_at: <TIMESTAMP>
updated_at: <TIMESTAMP>
generated_by: ProductSpecs_Generator
---

# Module Specification: <Module Name>

| **Meta Field** | **Value** |
|:---|:---|
| **Module ID** | `MOD-<APP>-<FEAT>-<NN>` |
| **Priority** | P0 |
| **App** | <App Name> |
| **Owner** | <Primary Persona> |
| **Status** | 🟡 Pending Dev |

---

## 1. Traceability & Context

### 1.1 Trace Map

| Level | ID | Description |
|:---|:---|:---|
| **Client Material** | `CM-<NNN>` | "<Quote>" |
| **Pain Point** | `PP-<N.N>` | "<Pain point>" |
| **JTBD** | `JTBD-<N.N>` | "<Job statement>" |
| **Requirement** | `REQ-<NNN>` | "<Requirement title>" |
| **Screen** | `SCR-<xxx>` | [Link] |

### 1.2 Module Scope

```mermaid
useCaseDiagram
    actor Warehouse_Operator as "Warehouse Operator"
    ...
```

---

## 2. Screen Specifications

### Screen A: <Screen Name>

* **Screen ID:** `SCR-<APP>-<NAME>-<NN>`
* **Route:** `/<route>`
* **Primary User:** <Persona>

#### 2.A.1 UI Component Dictionary

| Component | testID | Type | Props |
|:---|:---|:---|:---|
| Search Input | `input_search` | TextInput | placeholder, onSubmit |
| ... | ... | ... | ... |

#### 2.A.2 User Stories & Acceptance Criteria

**User Story A1:** <Title>
* **Req ID:** `REQ-<NNN>`
* **Priority:** P0

```gherkin
Feature: <Feature>

  Scenario: <Happy path>
    GIVEN <precondition>
    WHEN <action>
    THEN <result>
```

---

## 3. Access Control

### 3.1 Permission Matrix

| Action | Resource | Warehouse Op | Supervisor | Admin |
|:---|:---|:---|:---|:---|
| READ | Items | ✅ | ✅ | ✅ |
| CREATE | Adjustments | ✅ | ✅ | ✅ |
| APPROVE | Adjustments | ❌ | ✅ | ✅ |

---

## 4. Non-Functional Requirements

| ID | Category | Requirement | Metric |
|:---|:---|:---|:---|
| NFR-001 | Performance | Screen load time | < 2s at 95th percentile |
| ... | ... | ... | ... |

---

## 5. API Contracts

| Method | Endpoint | Purpose |
|:---|:---|:---|
| GET | /api/v1/items | List items |
| POST | /api/v1/adjustments | Create adjustment |

---

## 6. Test Specifications

| Test ID | Type | Scenario | Priority |
|:---|:---|:---|:---|
| TC-E2E-001 | E2E | Search and view item | P0 |
| ... | ... | ... | ... |
```

### Step 6: Validate Checkpoint 3

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 3 --dir ProductSpecs_<SystemName>/
```

### Step 7: Generate Extended Module Specs (Phase 4)

For remaining P1 and P2 modules, generate specifications following same template.

Track progress:
```python
for module in p1_modules + p2_modules:
    generate_module_spec(module)
    # Log progress
```

### Step 8: Update Module Registry

Write `ProductSpecs_<SystemName>/_registry/modules.json`:

```json
{
  "$schema": "productspecs-modules-v1",
  "$metadata": {
    "created_at": "<TIMESTAMP>",
    "updated_at": "<TIMESTAMP>",
    "source": "ProductSpecs_Generator"
  },
  "modules": [
    {
      "id": "MOD-INV-SEARCH-01",
      "name": "Inventory Search",
      "app": "INV",
      "priority": "P0",
      "screens": ["M-01", "M-02"],
      "requirements": ["REQ-001", "REQ-002"],
      "pain_points": ["PP-1.1"],
      "jtbds": ["JTBD-1.1"],
      "spec_file": "01-modules/MOD-INV-SEARCH-01.md",
      "status": "complete"
    }
  ],
  "by_priority": {
    "P0": ["MOD-INV-SEARCH-01", ...],
    "P1": [...],
    "P2": [...]
  },
  "by_app": {
    "INV": [...],
    "DSK": [...]
  },
  "statistics": {
    "total": 12,
    "by_priority": { "P0": 5, "P1": 5, "P2": 2 },
    "screens_covered": 15,
    "screens_total": 15,
    "coverage_percent": 100
  }
}
```

### Step 9: Update Traceability

Update `ProductSpecs_<SystemName>/_registry/traceability.json`:

```python
# Add module references to traceability chains
for chain in traceability["chains"]:
    chain["modules"] = find_modules_for_requirements(chain["requirements"])
    chain["complete"] = len(chain["modules"]) > 0
```

### Step 10: Update Progress

Update `_state/productspecs_progress.json`:

```python
# After Phase 3 (Core modules)
progress["phases"]["modules_core"]["status"] = "completed"
progress["phases"]["modules_core"]["completed_at"] = timestamp
progress["phases"]["modules_core"]["outputs"] = ["01-modules/module-index.md", ...]

# After Phase 4 (Extended modules)
progress["phases"]["modules_extended"]["status"] = "completed"
progress["phases"]["modules_extended"]["completed_at"] = timestamp
progress["current_phase"] = 5
```

### Step 11: Validate Checkpoint 4

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 4 --dir ProductSpecs_<SystemName>/
```

### Step 12: Display Summary

```
═══════════════════════════════════════════════════════
  MODULE SPECIFICATIONS GENERATED
═══════════════════════════════════════════════════════

  System:          <SystemName>

  Modules Generated: 12 total
  ────────────────────────────────────────────────────
  │ Priority │ Count │ Screens │ Requirements │
  │──────────│───────│─────────│──────────────│
  │ P0       │ 5     │ 8       │ 18           │
  │ P1       │ 5     │ 5       │ 15           │
  │ P2       │ 2     │ 2       │ 5            │

  Coverage:
  • Screens:         15/15 (100%)
  • Requirements:    38/45 (84%)
  • Traceability:    All P0 modules traced ✅

  Checkpoint 3:    ✅ PASSED
  Checkpoint 4:    ✅ PASSED

═══════════════════════════════════════════════════════

  Next Steps:
  • /productspecs-contracts    - Generate API contracts
  • /productspecs              - Continue full generation

═══════════════════════════════════════════════════════
```

## Module ID Generation

```
Format: MOD-{APP}-{FEATURE}-{NN}
Example: MOD-INV-ADJUST-01

Where:
- APP: 3-4 letter app abbreviation (INV, DSK, WEB)
- FEATURE: 3-6 letter feature abbreviation (SEARCH, ADJUST, REPORT)
- NN: Sequential number starting at 01
```

## Outputs

| File | Location |
|------|----------|
| `module-index.md` | `ProductSpecs_<SystemName>/01-modules/` |
| `MOD-*.md` | `ProductSpecs_<SystemName>/01-modules/` |
| `modules.json` | `ProductSpecs_<SystemName>/_registry/` |
| `traceability.json` | `ProductSpecs_<SystemName>/_registry/` (updated) |

## Error Handling

| Error | Action |
|-------|--------|
| Checkpoint 2 not passed | **BLOCK** - Run /productspecs-extract |
| Screen without module | **WARN** - Create standalone module |
| Module without P0 req | **WARN** - Log, continue |
| Missing component spec | **WARN** - Use placeholder |

## Outputs

| Command | Description |
|---------|-------------|
| `/productspecs-extract` | Previous phase |
| `/productspecs-contracts` | Next phase |
| `/productspecs` | Full generation |
