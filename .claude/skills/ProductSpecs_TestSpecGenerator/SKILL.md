---
name: generating-test-specifications
description: Use when you need to generate comprehensive test specifications (unit, integration, E2E, accessibility) with full traceability to requirements.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-test-specifications started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-test-specifications ended '{"stage": "productspecs"}'
---

# ProductSpecs_TestSpecGenerator

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-test-specifications instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

**Purpose**: Generate comprehensive test specifications with full traceability.

**Version**: 1.0.0
**Created**: 2025-12-22
**Phase**: 6 of ProductSpecs pipeline (Tests)

---

## Overview

This skill generates test specifications covering:
- Unit tests for components
- Integration tests for API flows
- E2E tests for user journeys
- Accessibility tests for WCAG compliance
- Performance tests for NFRs

All tests are traced back to requirements and modules.

---

## Prerequisites

### Required State Files

Location: `_state/` (at PROJECT ROOT)

| File | Purpose |
|------|---------|
| `productspecs_config.json` | ProductSpecs configuration |
| `productspecs_progress.json` | Phase tracking |
| `discovery_summary.json` | Discovery data |
| `requirements_registry.json` | Requirements |

### Required Registry Files

Location: `traceability/` (ROOT level - single source of truth)

| File | Purpose |
|------|---------|
| `module_registry.json` | Module specifications |
| `requirements_registry.json` | Enriched requirements |
| `nfr_registry.json` | Non-functional requirements |
| `productspecs_traceability_register.json` | Traceability chains |

### Checkpoint 5 Must Pass

Run `productspecs-contracts` first.

---

## Execution Flow

### Phase 6.1: Load Source Data

```python
# Load from shared _state/
config = json.load("_state/productspecs_config.json")
discovery_summary = json.load("_state/discovery_summary.json")
requirements_registry = json.load("_state/requirements_registry.json")

# Load from ROOT traceability/ folder (single source of truth)
modules = json.load("traceability/module_registry.json")
requirements = json.load("traceability/requirements_registry.json")
nfrs = json.load("traceability/nfr_registry.json")
traceability = json.load("traceability/productspecs_traceability_register.json")

# Load prototype components
components = load_component_specs(f"{config['prototype_path']}/01-components/")
screens = load_screen_specs(f"{config['prototype_path']}/02-screens/")
```

### Phase 6.2: Generate Unit Test Specs

For each component:

```python
unit_tests = []

for component in components:
    test_spec = {
        "id": f"TC-UNIT-{next_id()}",
        "type": "unit",
        "component": component["name"],
        "file_path": f"src/components/{component['name']}/{component['name']}.test.tsx",
        "coverage_target": 80,
        "scenarios": []
    }

    # Render tests
    test_spec["scenarios"].append({
        "name": f"{component['name']} renders without crashing",
        "priority": "P0",
        "gherkin": f"""
Feature: {component['name']} Component Rendering

  Scenario: Component renders with default props
    Given the component is imported
    When rendered with default props
    Then no errors should be thrown
    And the component should be in the document
"""
    })

    # Props tests
    for prop in component.get("props", []):
        test_spec["scenarios"].append({
            "name": f"{component['name']} handles {prop['name']} prop",
            "priority": "P1",
            "gherkin": f"""
  Scenario: Component handles {prop['name']} prop
    Given the component is rendered
    When {prop['name']} is set to a valid value
    Then the component should reflect the prop value
"""
        })

    # State tests
    for state in component.get("states", []):
        test_spec["scenarios"].append({
            "name": f"{component['name']} displays {state} state",
            "priority": "P0" if state in ["error", "loading"] else "P1"
        })

    unit_tests.append(test_spec)
```

### Phase 6.3: Generate Integration Test Specs

For each API endpoint:

```python
integration_tests = []

for endpoint in api_endpoints:
    test_spec = {
        "id": f"TC-INT-{next_id()}",
        "type": "integration",
        "endpoint": endpoint["path"],
        "method": endpoint["method"],
        "scenarios": []
    }

    # Happy path
    test_spec["scenarios"].append({
        "name": f"{endpoint['method']} {endpoint['path']} - Success",
        "priority": "P0",
        "gherkin": f"""
Feature: {endpoint['method']} {endpoint['path']} API

  Scenario: Successful {endpoint['method']} request
    Given a valid authentication token
    And valid request payload
    When {endpoint['method']} request is sent to {endpoint['path']}
    Then response status should be {200 if endpoint['method'] == 'GET' else 201}
    And response should match expected schema
"""
    })

    # Auth failure
    test_spec["scenarios"].append({
        "name": f"{endpoint['method']} {endpoint['path']} - Unauthorized",
        "priority": "P0",
        "gherkin": f"""
  Scenario: Unauthorized request
    Given no authentication token
    When {endpoint['method']} request is sent to {endpoint['path']}
    Then response status should be 401
"""
    })

    # Validation failure
    if endpoint["method"] in ["POST", "PUT", "PATCH"]:
        test_spec["scenarios"].append({
            "name": f"{endpoint['method']} {endpoint['path']} - Validation Error",
            "priority": "P1",
            "gherkin": f"""
  Scenario: Invalid request payload
    Given a valid authentication token
    And invalid request payload
    When {endpoint['method']} request is sent to {endpoint['path']}
    Then response status should be 400
    And response should contain validation errors
"""
        })

    integration_tests.append(test_spec)
```

### Phase 6.4: Generate E2E Test Specs

For each user journey/workflow:

```python
e2e_tests = []

for workflow in discovery_summary.get("workflows", []):
    test_spec = {
        "id": f"TC-E2E-{next_id()}",
        "type": "e2e",
        "workflow": workflow["name"],
        "screens": workflow.get("screens", []),
        "duration_estimate": workflow.get("target_time", "5 minutes"),
        "priority": "P0" if workflow.get("priority") == "P0" else "P1",
        "requirements_traced": workflow.get("requirements", []),
        "gherkin": ""
    }

    # Build Gherkin scenario
    steps = []
    for i, screen in enumerate(workflow.get("screens", [])):
        if i == 0:
            steps.append(f"Given the user is on the {screen} screen")
        else:
            steps.append(f"And navigates to {screen} screen")

    for action in workflow.get("actions", []):
        steps.append(f"When the user {action}")

    steps.append(f"Then the workflow completes successfully")
    steps.append(f"And all data is persisted correctly")

    test_spec["gherkin"] = f"""
Feature: {workflow['name']}

  @e2e @{workflow.get('priority', 'P1')}
  Scenario: Complete {workflow['name']} workflow
    {chr(10).join('    ' + s for s in steps)}
"""

    e2e_tests.append(test_spec)

# Generate E2E for each P0 requirement
for req in requirements["requirements"]:
    if req["priority"] == "P0":
        test_spec = {
            "id": f"TC-E2E-{next_id()}",
            "type": "e2e",
            "requirement": req["id"],
            "title": req["title"],
            "screens": req.get("screen_refs", []),
            "priority": "P0",
            "gherkin": req.get("acceptance_criteria", [""])[0]
        }
        e2e_tests.append(test_spec)
```

### Phase 6.5: Generate Accessibility Test Specs

```python
a11y_tests = []

for screen in screens:
    test_spec = {
        "id": f"TC-A11Y-{next_id()}",
        "type": "accessibility",
        "screen": screen["id"],
        "priority": "P0",
        "scenarios": [
            {
                "name": f"{screen['id']} - axe-core automated scan",
                "tool": "axe-core",
                "wcag_level": "AA",
                "gherkin": f"""
Feature: {screen['name']} Accessibility

  @a11y @automated
  Scenario: Automated accessibility scan passes
    Given the {screen['name']} screen is rendered
    When axe-core accessibility scan is run
    Then no violations should be detected at WCAG 2.1 AA level
"""
            },
            {
                "name": f"{screen['id']} - Keyboard navigation",
                "tool": "manual",
                "gherkin": f"""
  @a11y @manual
  Scenario: Keyboard navigation works correctly
    Given the {screen['name']} screen is rendered
    When using only keyboard navigation
    Then all interactive elements should be reachable
    And focus indicators should be visible
"""
            }
        ]
    }
    a11y_tests.append(test_spec)
```

### Phase 6.6: Generate Performance Test Specs

```python
perf_tests = []

for nfr in nfrs["nfrs"]:
    if nfr["category"] == "Performance":
        test_spec = {
            "id": f"TC-PERF-{next_id()}",
            "type": "performance",
            "nfr_ref": nfr["id"],
            "metric": nfr["metric"],
            "threshold": nfr.get("threshold", {}),
            "tool": nfr.get("test_method", "lighthouse"),
            "priority": nfr.get("priority", "P1"),
            "gherkin": f"""
Feature: {nfr['title']}

  @performance @nfr:{nfr['id']}
  Scenario: {nfr['title']} meets threshold
    Given the system is under normal load
    When measuring {nfr['metric']}
    Then the result should be within threshold
    | metric | threshold |
    | {nfr.get('threshold', {}).get('unit', 'ms')} | {nfr.get('threshold', {}).get('target', 2000)} |
"""
        }
        perf_tests.append(test_spec)
```

### Phase 6.7: Build Test Case Registry

```python
all_tests = unit_tests + integration_tests + e2e_tests + a11y_tests + perf_tests

test_registry = {
    "$schema": "productspecs-tests-v1",
    "$metadata": {
        "created_at": timestamp,
        "updated_at": timestamp,
        "source": "ProductSpecs_TestSpecGenerator"
    },
    "test_cases": all_tests,
    "by_type": {
        "unit": [t["id"] for t in unit_tests],
        "integration": [t["id"] for t in integration_tests],
        "e2e": [t["id"] for t in e2e_tests],
        "accessibility": [t["id"] for t in a11y_tests],
        "performance": [t["id"] for t in perf_tests]
    },
    "by_priority": {
        "P0": [t["id"] for t in all_tests if t.get("priority") == "P0"],
        "P1": [t["id"] for t in all_tests if t.get("priority") == "P1"],
        "P2": [t["id"] for t in all_tests if t.get("priority") == "P2"]
    },
    "coverage": {
        "components_covered": len(unit_tests),
        "components_total": len(components),
        "endpoints_covered": len(integration_tests),
        "endpoints_total": len(api_endpoints),
        "requirements_p0_covered": count_p0_covered,
        "requirements_p0_total": count_p0_total,
        "screens_a11y_covered": len(a11y_tests),
        "screens_total": len(screens)
    },
    "statistics": {
        "total": len(all_tests),
        "by_type": {
            "unit": len(unit_tests),
            "integration": len(integration_tests),
            "e2e": len(e2e_tests),
            "accessibility": len(a11y_tests),
            "performance": len(perf_tests)
        },
        "by_priority": {
            "P0": len([t for t in all_tests if t.get("priority") == "P0"]),
            "P1": len([t for t in all_tests if t.get("priority") == "P1"]),
            "P2": len([t for t in all_tests if t.get("priority") == "P2"])
        }
    }
}
```

### Phase 6.8: Update Traceability

Add test case links to traceability chains:

```python
for chain in traceability["chains"]:
    # Find tests that trace to this chain's requirements
    chain_tests = []
    for req_id in chain["requirements"]:
        for test in all_tests:
            if req_id in test.get("requirements_traced", []) or \
               test.get("requirement") == req_id:
                chain_tests.append(test["id"])

    chain["tests"] = list(set(chain_tests))
    chain["complete"] = len(chain["tests"]) > 0 and len(chain["modules"]) > 0
```

### Phase 6.9: Write Output Files

#### `traceability/test_case_registry.json` (ROOT level - single source of truth)

```json
{
  "$schema": "productspecs-tests-v1",
  "$metadata": {
    "created_at": "<TIMESTAMP>",
    "updated_at": "<TIMESTAMP>",
    "source": "ProductSpecs_TestSpecGenerator"
  },
  "test_cases": [...],
  "by_type": {...},
  "by_priority": {...},
  "coverage": {...},
  "statistics": {...}
}
```

#### `03-tests/test-case-registry.md`

```markdown
# Test Case Registry

**System**: <SystemName>
**Generated**: <TIMESTAMP>
**Total Test Cases**: <N>

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

## Coverage

| Metric | Covered | Total | Percent |
|--------|---------|-------|---------|
| Components | 28 | 28 | 100% |
| API Endpoints | 12 | 12 | 100% |
| P0 Requirements | 18 | 18 | 100% |
| Screens (A11Y) | 15 | 15 | 100% |

---

## Test Cases by Module

### MOD-INV-SEARCH-01

| Test ID | Type | Scenario | Priority |
|---------|------|----------|----------|
| TC-UNIT-001 | Unit | SearchInput renders | P0 |
| TC-INT-001 | Integration | GET /items - Success | P0 |
| TC-E2E-001 | E2E | Search and view item | P0 |
| TC-A11Y-001 | Accessibility | Search screen scan | P0 |

...
```

#### `03-tests/e2e-scenarios.md`

```markdown
# E2E Test Scenarios

**System**: <SystemName>
**Generated**: <TIMESTAMP>

---

## Critical Paths (P0)

### TC-E2E-001: Search and View Item

**Priority**: P0
**Screens**: M-01 → M-02
**Duration**: ~2 minutes
**Requirements**: REQ-001, REQ-002

```gherkin
Feature: Item Search and View

  @e2e @P0
  Scenario: User searches for and views an item
    Given the user is logged in as Warehouse Operator
    And is on the Search screen
    When the user enters "ABC123" in the search field
    And taps the Search button
    Then search results should display
    And at least one result should match "ABC123"
    When the user taps on the first result
    Then the Item Detail screen should display
    And the item code should be "ABC123"
```

...
```

#### `03-tests/accessibility-checklist.md`

```markdown
# Accessibility Compliance Checklist

**System**: <SystemName>
**Generated**: <TIMESTAMP>
**Standard**: WCAG 2.1 Level AA

---

## Screen-by-Screen Checklist

### M-01: Search Screen

| Criterion | Description | Status | Test ID |
|-----------|-------------|--------|---------|
| 1.1.1 | Non-text Content | ⬜ | TC-A11Y-001 |
| 1.3.1 | Info and Relationships | ⬜ | TC-A11Y-001 |
| 1.4.3 | Contrast (Minimum) | ⬜ | TC-A11Y-001 |
| 2.1.1 | Keyboard | ⬜ | TC-A11Y-001 |
| 2.4.3 | Focus Order | ⬜ | TC-A11Y-001 |
| 4.1.2 | Name, Role, Value | ⬜ | TC-A11Y-001 |

...
```

---

## Outputs

| File | Location | Purpose |
|------|----------|---------|
| `test_case_registry.json` | `traceability/` (ROOT) | Test registry (single source of truth) |
| `test-case-registry.md` | `ProductSpecs_<SystemName>/03-tests/` | Test summary |
| `e2e-scenarios.md` | `ProductSpecs_<SystemName>/03-tests/` | E2E scenarios |
| `accessibility-checklist.md` | `ProductSpecs_<SystemName>/03-tests/` | A11Y checklist |
| `productspecs_traceability_register.json` | `traceability/` (ROOT) | Updated with tests |

---

## Test ID Generation

```
Format: TC-{TYPE}-{NNN}
Examples:
- TC-UNIT-001 (Unit test)
- TC-INT-015 (Integration test)
- TC-E2E-042 (End-to-end test)
- TC-A11Y-008 (Accessibility test)
- TC-PERF-003 (Performance test)
```

---

## Error Handling

| Error | Action |
|-------|--------|
| Missing component spec | **WARN** - Skip unit tests |
| Missing API spec | **WARN** - Skip integration tests |
| P0 req without test | **ERROR** - Flag for manual creation |
| Incomplete Gherkin | **WARN** - Use template |

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `ProductSpecs_NFRGenerator` | Previous phase |
| `ProductSpecs_Finalize` | Next phase - traceability validation |
