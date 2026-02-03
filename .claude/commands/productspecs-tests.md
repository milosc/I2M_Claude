---
name: productspecs-tests
description: Generate comprehensive test specifications (unit, integration, E2E)
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-tests started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-tests ended '{"stage": "productspecs"}'
---


# /productspecs-tests - Generate Test Specifications

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs-tests instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for module/test ID management:

```bash
# Load Traceability rules (includes module ID format MOD-XXX-XXX-NN)
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Required: `<SystemName>`

## Prerequisites

- `/productspecs-contracts <SystemName>` completed (Checkpoint 5 passed)

## Skills Used

Read BEFORE execution:
- `.claude/skills/ProductSpecs_TestSpecGenerator/SKILL.md`

## Execution Steps

### Step 1: Verify Checkpoint 5

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 5 --dir ProductSpecs_<SystemName>/
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
modules = json.load(f"{output_path}/_registry/modules.json")
requirements = json.load(f"{output_path}/_registry/requirements.json")
nfrs = json.load(f"{output_path}/_registry/nfrs.json")
traceability = json.load(f"{output_path}/_registry/traceability.json")

# Load prototype components and screens
components = load_components(f"{prototype_path}/01-components/")
screens = load_screens(f"{prototype_path}/02-screens/")
api_contracts = load_api_contracts(f"{output_path}/02-api/")
```

### Step 3: Generate Unit Test Specs

For each component in prototype:

```python
unit_tests = []

for component in components:
    test_spec = {
        "id": f"TC-UNIT-{next_id()}",
        "type": "unit",
        "component": component["name"],
        "priority": "P0" if component.get("used_in_p0_screen") else "P1",
        "scenarios": [
            {"name": "Renders without crashing", "priority": "P0"},
            {"name": "Handles all props correctly", "priority": "P1"},
            {"name": "Displays all states", "priority": "P1"},
            {"name": "Fires callbacks correctly", "priority": "P1"}
        ]
    }
    unit_tests.append(test_spec)
```

### Step 4: Generate Integration Test Specs

For each API endpoint:

```python
integration_tests = []

for endpoint in api_contracts:
    test_spec = {
        "id": f"TC-INT-{next_id()}",
        "type": "integration",
        "endpoint": endpoint["path"],
        "method": endpoint["method"],
        "priority": "P0" if endpoint.get("used_in_p0_flow") else "P1",
        "scenarios": [
            {"name": "Success response", "priority": "P0"},
            {"name": "Unauthorized request", "priority": "P0"},
            {"name": "Validation error", "priority": "P1"},
            {"name": "Not found", "priority": "P1"}
        ]
    }
    integration_tests.append(test_spec)
```

### Step 5: Generate E2E Test Specs

For each workflow and P0 requirement:

```python
e2e_tests = []

# From workflows
for workflow in discovery_summary.get("workflows", []):
    e2e_tests.append({
        "id": f"TC-E2E-{next_id()}",
        "type": "e2e",
        "workflow": workflow["name"],
        "screens": workflow.get("screens", []),
        "priority": workflow.get("priority", "P1"),
        "requirements_traced": workflow.get("requirements", [])
    })

# From P0 requirements
for req in requirements["requirements"]:
    if req["priority"] == "P0":
        e2e_tests.append({
            "id": f"TC-E2E-{next_id()}",
            "type": "e2e",
            "requirement": req["id"],
            "title": req["title"],
            "priority": "P0"
        })
```

### Step 6: Generate Accessibility Test Specs

For each screen:

```python
a11y_tests = []

for screen in screens:
    a11y_tests.append({
        "id": f"TC-A11Y-{next_id()}",
        "type": "accessibility",
        "screen": screen["id"],
        "priority": "P0",
        "wcag_level": "AA",
        "scenarios": [
            {"name": "axe-core automated scan", "tool": "axe-core"},
            {"name": "Keyboard navigation", "tool": "manual"},
            {"name": "Screen reader compatibility", "tool": "VoiceOver/NVDA"}
        ]
    })
```

### Step 7: Generate Performance Test Specs

For each Performance NFR:

```python
perf_tests = []

for nfr in nfrs["nfrs"]:
    if nfr["category"] == "Performance":
        perf_tests.append({
            "id": f"TC-PERF-{next_id()}",
            "type": "performance",
            "nfr_ref": nfr["id"],
            "metric": nfr["metric"],
            "threshold": nfr.get("threshold"),
            "tool": nfr.get("test_method", "lighthouse"),
            "priority": nfr.get("priority", "P1")
        })
```

### Step 8: Write Test Case Registry

Write `ProductSpecs_<SystemName>/_registry/test-cases.json`:

```json
{
  "$schema": "productspecs-tests-v1",
  "$metadata": {
    "created_at": "<TIMESTAMP>",
    "updated_at": "<TIMESTAMP>",
    "source": "ProductSpecs_TestSpecGenerator"
  },
  "test_cases": [...],
  "by_type": {
    "unit": ["TC-UNIT-001", ...],
    "integration": ["TC-INT-001", ...],
    "e2e": ["TC-E2E-001", ...],
    "accessibility": ["TC-A11Y-001", ...],
    "performance": ["TC-PERF-001", ...]
  },
  "by_priority": {
    "P0": [...],
    "P1": [...],
    "P2": [...]
  },
  "coverage": {
    "components_covered": 28,
    "components_total": 28,
    "endpoints_covered": 14,
    "endpoints_total": 14,
    "requirements_p0_covered": 18,
    "requirements_p0_total": 18,
    "screens_a11y_covered": 15,
    "screens_total": 15
  },
  "statistics": {
    "total": 107,
    "by_type": {...},
    "by_priority": {...}
  }
}
```

### Step 9: Write Test Documentation

#### `03-tests/test-case-registry.md`

```markdown
# Test Case Registry

**System**: <SystemName>
**Generated**: <TIMESTAMP>
**Total Test Cases**: 107

---

## Summary

| Type | Count | P0 | P1 | P2 |
|------|-------|----|----|-----|
| Unit | 45 | 15 | 25 | 5 |
| Integration | 24 | 12 | 10 | 2 |
| E2E | 15 | 10 | 4 | 1 |
| Accessibility | 15 | 15 | 0 | 0 |
| Performance | 8 | 4 | 3 | 1 |
| **Total** | **107** | **56** | **42** | **9** |

---

## Coverage Matrix

| Metric | Covered | Total | Percent |
|--------|---------|-------|---------|
| Components | 28 | 28 | 100% |
| API Endpoints | 14 | 14 | 100% |
| P0 Requirements | 18 | 18 | 100% |
| Screens (A11Y) | 15 | 15 | 100% |
| NFRs (Perf) | 8 | 8 | 100% |

---

## Test Cases by Module

### MOD-INV-SEARCH-01

| Test ID | Type | Scenario | Priority | Status |
|---------|------|----------|----------|--------|
| TC-UNIT-001 | Unit | SearchInput renders | P0 | ⬜ |
| TC-INT-001 | Integration | GET /items | P0 | ⬜ |
| TC-E2E-001 | E2E | Search workflow | P0 | ⬜ |
| TC-A11Y-001 | Accessibility | Search screen | P0 | ⬜ |

...
```

#### `03-tests/e2e-scenarios.md`

```markdown
# E2E Test Scenarios

**System**: <SystemName>
**Generated**: <TIMESTAMP>

---

## Critical Paths (P0)

### TC-E2E-001: Inventory Search Workflow

**Priority**: P0
**Screens**: M-01 → M-02
**Duration**: ~2 minutes
**Requirements**: REQ-001, REQ-002

```gherkin
Feature: Inventory Search

  @e2e @P0
  Scenario: User searches for and views an item
    Given the user is logged in as "Warehouse Operator"
    And is on the Search screen
    When the user enters "ABC123" in the search field
    And taps the Search button
    Then search results should display
    When the user taps on the first result
    Then the Item Detail screen should display
```

...
```

#### `03-tests/accessibility-checklist.md`

```markdown
# Accessibility Compliance Checklist

**System**: <SystemName>
**Standard**: WCAG 2.1 Level AA
**Generated**: <TIMESTAMP>

---

## Screen Checklist

### M-01: Search Screen

| WCAG | Criterion | Status | Notes |
|------|-----------|--------|-------|
| 1.1.1 | Non-text Content | ⬜ | |
| 1.3.1 | Info and Relationships | ⬜ | |
| 1.4.3 | Contrast (Minimum) | ⬜ | |
| 2.1.1 | Keyboard | ⬜ | |
| 2.4.3 | Focus Order | ⬜ | |
| 4.1.2 | Name, Role, Value | ⬜ | |

...
```

### Step 10: Update Traceability

Update `ProductSpecs_<SystemName>/_registry/traceability.json`:

```python
# Add test references to chains
for chain in traceability["chains"]:
    chain_tests = []
    for req_id in chain["requirements"]:
        # Find tests for this requirement
        matching_tests = [t for t in all_tests
                        if req_id in t.get("requirements_traced", [])]
        chain_tests.extend([t["id"] for t in matching_tests])

    chain["tests"] = list(set(chain_tests))
    chain["complete"] = (
        len(chain["modules"]) > 0 and
        len(chain["tests"]) > 0
    )

# Update coverage
traceability["coverage"]["tests_p0"] = count_p0_tests
traceability["coverage"]["tests_total"] = len(all_tests)
```

### Step 11: Update Progress

Update `_state/productspecs_progress.json`:

```python
progress["phases"]["tests"]["status"] = "completed"
progress["phases"]["tests"]["completed_at"] = timestamp
progress["phases"]["tests"]["outputs"] = [
    "03-tests/test-case-registry.md",
    "03-tests/e2e-scenarios.md",
    "03-tests/accessibility-checklist.md",
    "_registry/test-cases.json"
]
progress["current_phase"] = 7
```

### Step 12: Validate Checkpoint 6

```bash
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 6 --dir ProductSpecs_<SystemName>/
```

### Step 13: Display Summary

```
═══════════════════════════════════════════════════════
  TEST SPECIFICATIONS GENERATED
═══════════════════════════════════════════════════════

  System:          <SystemName>

  Test Cases Generated: 107 total
  ────────────────────────────────────────────────────
  │ Type          │ Count │ P0  │ P1  │ P2  │
  │───────────────│───────│─────│─────│─────│
  │ Unit          │ 45    │ 15  │ 25  │ 5   │
  │ Integration   │ 24    │ 12  │ 10  │ 2   │
  │ E2E           │ 15    │ 10  │ 4   │ 1   │
  │ Accessibility │ 15    │ 15  │ 0   │ 0   │
  │ Performance   │ 8     │ 4   │ 3   │ 1   │

  Coverage:
  • Components:       28/28 (100%)
  • API Endpoints:    14/14 (100%)
  • P0 Requirements:  18/18 (100%)
  • Screens (A11Y):   15/15 (100%)

  Traceability:
  • Chains with tests: 12/12 (100%)

  Checkpoint 6:    ✅ PASSED

═══════════════════════════════════════════════════════

  Next Steps:
  • /productspecs-finalize   - Validate traceability
  • /productspecs            - Continue full generation

═══════════════════════════════════════════════════════
```

## Outputs

| File | Location |
|------|----------|
| `test-case-registry.md` | `ProductSpecs_<SystemName>/03-tests/` |
| `e2e-scenarios.md` | `ProductSpecs_<SystemName>/03-tests/` |
| `accessibility-checklist.md` | `ProductSpecs_<SystemName>/03-tests/` |
| `test-cases.json` | `ProductSpecs_<SystemName>/_registry/` |
| `traceability.json` | `ProductSpecs_<SystemName>/_registry/` (updated) |

## Error Handling

| Error | Action |
|-------|--------|
| Checkpoint 5 not passed | **BLOCK** - Run /productspecs-contracts |
| P0 requirement without test | **ERROR** - Create placeholder, flag |
| Missing component spec | **WARN** - Skip unit tests for component |
| Missing API spec | **WARN** - Skip integration tests |

## Related Commands

| Command | Description |
|---------|-------------|
| `/productspecs-contracts` | Previous phase |
| `/productspecs-finalize` | Next phase |
| `/productspecs` | Full generation |
