---
name: generating-nfr-specifications
description: Use when you need to generate SMART Non-Functional Requirements (NFRs) with full traceability to business requirements.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-nfr-specifications started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-nfr-specifications ended '{"stage": "productspecs"}'
---

# ProductSpecs_NFRGenerator

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-nfr-specifications instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

**Purpose**: Generate SMART Non-Functional Requirements with full traceability.

**Version**: 1.0.0
**Created**: 2025-12-22
**Phase**: 5 of ProductSpecs pipeline (Contracts)

---

## Overview

This skill generates comprehensive Non-Functional Requirements (NFRs) that are:
- **S**pecific: Exact metrics and conditions
- **M**easurable: Quantifiable thresholds
- **A**chievable: Realistic targets based on prototype
- **R**elevant: Traced to business requirements
- **T**ime-bound: Clear validation timeframes

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

Location: `traceability/` (ROOT level)

| File | Purpose |
|------|---------|
| `module_registry.json` | Module specifications |
| `requirements_registry.json` | Enriched requirements |

### Checkpoint 4 Must Pass

Run `productspecs-modules` first.

---

## Execution Flow

### Phase 5.1: Load Source Data

```python
# Load from shared _state/
config = json.load("_state/productspecs_config.json")
discovery_summary = json.load("_state/discovery_summary.json")

# Load from ROOT traceability/ folder (single source of truth)
modules = json.load("traceability/module_registry.json")
requirements = json.load("traceability/requirements_registry.json")

# Extract existing NFRs
existing_nfrs = [r for r in requirements_registry.get("requirements", [])
                 if r.get("type") == "non_functional"]
```

### Phase 5.2: Define NFR Categories

| Category | Code | Examples |
|----------|------|----------|
| Performance | PERF | Response time, throughput, latency |
| Availability | AVAIL | Uptime, failover, recovery time |
| Scalability | SCALE | Concurrent users, data volume |
| Security | SEC | Authentication, encryption, audit |
| Accessibility | A11Y | WCAG compliance, assistive tech |
| Usability | USAB | Error rate, task completion |
| Reliability | REL | Error handling, data integrity |
| Maintainability | MAINT | Code coverage, documentation |

### Phase 5.3: Generate Performance NFRs

```python
performance_nfrs = []

# For each screen/module
for module in modules["modules"]:
    for screen_id in module["screens"]:
        nfr = {
            "id": f"NFR-PERF-{next_id()}",
            "category": "Performance",
            "title": f"{screen_id} Load Time",
            "description": f"Screen {screen_id} must load within acceptable time",
            "metric": "Page load time < 2s at 95th percentile",
            "measurement": "Lighthouse performance audit",
            "test_method": "Run lighthouse --preset=desktop",
            "threshold": {
                "target": 2000,
                "unit": "ms",
                "percentile": 95
            },
            "priority": "P0" if module["priority"] == "P0" else "P1",
            "module_refs": [module["id"]],
            "screen_refs": [screen_id]
        }
        performance_nfrs.append(nfr)

# API response time
for endpoint in api_endpoints:
    nfr = {
        "id": f"NFR-PERF-{next_id()}",
        "category": "Performance",
        "title": f"{endpoint['method']} {endpoint['path']} Response Time",
        "metric": "API response time < 500ms at 95th percentile",
        "threshold": {
            "target": 500,
            "unit": "ms",
            "percentile": 95
        }
    }
    performance_nfrs.append(nfr)
```

### Phase 5.4: Generate Availability NFRs

```python
availability_nfrs = [
    {
        "id": "NFR-AVAIL-001",
        "category": "Availability",
        "title": "System Uptime",
        "description": "System must maintain high availability",
        "metric": "99.9% uptime measured over rolling 30 days",
        "measurement": "Monitoring system (e.g., DataDog, New Relic)",
        "threshold": {
            "target": 99.9,
            "unit": "percent",
            "period": "30 days"
        },
        "priority": "P0"
    },
    {
        "id": "NFR-AVAIL-002",
        "category": "Availability",
        "title": "Recovery Time Objective",
        "description": "System must recover from failures quickly",
        "metric": "RTO < 4 hours for critical failures",
        "threshold": {
            "target": 4,
            "unit": "hours"
        },
        "priority": "P1"
    }
]
```

### Phase 5.5: Generate Security NFRs

```python
security_nfrs = [
    {
        "id": "NFR-SEC-001",
        "category": "Security",
        "title": "Authentication Required",
        "description": "All API endpoints require authentication",
        "metric": "100% of non-public endpoints require valid JWT",
        "test_method": "API security scan + manual review",
        "priority": "P0"
    },
    {
        "id": "NFR-SEC-002",
        "category": "Security",
        "title": "Data Encryption",
        "description": "All data in transit must be encrypted",
        "metric": "TLS 1.2+ for all connections",
        "test_method": "SSL/TLS scan",
        "priority": "P0"
    },
    {
        "id": "NFR-SEC-003",
        "category": "Security",
        "title": "Input Validation",
        "description": "All user inputs must be validated",
        "metric": "Zero XSS/SQL injection vulnerabilities",
        "test_method": "OWASP ZAP scan",
        "priority": "P0"
    }
]
```

### Phase 5.6: Generate Accessibility NFRs

```python
accessibility_nfrs = []

# From accessibility requirements in discovery
for a11y_req in discovery_summary.get("accessibility_requirements", []):
    nfr = {
        "id": f"NFR-A11Y-{next_id()}",
        "category": "Accessibility",
        "title": a11y_req.get("title"),
        "description": a11y_req.get("description"),
        "metric": f"WCAG 2.1 {a11y_req.get('level', 'AA')} compliant",
        "test_method": "axe-core automated scan + manual review",
        "wcag_criteria": a11y_req.get("wcag_criteria", []),
        "priority": "P0"
    }
    accessibility_nfrs.append(nfr)

# Default accessibility NFRs
default_a11y = [
    {
        "id": "NFR-A11Y-001",
        "category": "Accessibility",
        "title": "Keyboard Navigation",
        "description": "All interactive elements must be keyboard accessible",
        "metric": "100% of interactive elements reachable via Tab/Enter/Space",
        "test_method": "Manual keyboard testing",
        "wcag_criteria": ["2.1.1", "2.1.2"],
        "priority": "P0"
    },
    {
        "id": "NFR-A11Y-002",
        "category": "Accessibility",
        "title": "Screen Reader Support",
        "description": "All content must be accessible via screen reader",
        "metric": "All images have alt text, all forms have labels",
        "test_method": "VoiceOver/NVDA testing",
        "wcag_criteria": ["1.1.1", "1.3.1"],
        "priority": "P0"
    },
    {
        "id": "NFR-A11Y-003",
        "category": "Accessibility",
        "title": "Color Contrast",
        "description": "Text must have sufficient color contrast",
        "metric": "Minimum 4.5:1 contrast ratio for normal text",
        "test_method": "axe-core color contrast check",
        "wcag_criteria": ["1.4.3"],
        "priority": "P0"
    }
]
```

### Phase 5.7: Generate Scalability NFRs

```python
scalability_nfrs = [
    {
        "id": "NFR-SCALE-001",
        "category": "Scalability",
        "title": "Concurrent Users",
        "description": "System must support expected concurrent users",
        "metric": "100 concurrent users per tenant without degradation",
        "test_method": "Load testing with k6/JMeter",
        "threshold": {
            "target": 100,
            "unit": "concurrent_users"
        },
        "priority": "P1"
    },
    {
        "id": "NFR-SCALE-002",
        "category": "Scalability",
        "title": "Data Volume",
        "description": "System must handle expected data volume",
        "metric": "Support 1M records per entity with < 10% performance degradation",
        "threshold": {
            "target": 1000000,
            "unit": "records",
            "degradation_max": 10
        },
        "priority": "P1"
    }
]
```

### Phase 5.8: Generate SMART Validation Table

For each NFR, ensure SMART compliance:

| NFR ID | Specific | Measurable | Achievable | Relevant | Time-bound |
|--------|----------|------------|------------|----------|------------|
| NFR-PERF-001 | Load time < 2s | 95th percentile | Based on prototype | P0 user flow | Per request |
| NFR-AVAIL-001 | 99.9% uptime | Monitoring | Industry standard | Business critical | 30 days |

### Phase 5.9: Write NFR Registry

Write `traceability/nfr_registry.json` (ROOT level, single source of truth):

```json
{
  "$schema": "productspecs-nfrs-v1",
  "$metadata": {
    "created_at": "<TIMESTAMP>",
    "updated_at": "<TIMESTAMP>",
    "source": "ProductSpecs_NFRGenerator"
  },
  "nfrs": [
    {
      "id": "NFR-PERF-001",
      "category": "Performance",
      "title": "Screen Load Time",
      "description": "All screens must load quickly",
      "metric": "Page load < 2s at 95th percentile",
      "measurement": "Lighthouse audit",
      "test_method": "lighthouse --preset=desktop",
      "threshold": {
        "target": 2000,
        "unit": "ms",
        "percentile": 95
      },
      "priority": "P0",
      "module_refs": ["MOD-INV-SEARCH-01"],
      "screen_refs": ["M-01", "M-02"],
      "smart_validation": {
        "specific": true,
        "measurable": true,
        "achievable": true,
        "relevant": true,
        "time_bound": true
      }
    }
  ],
  "by_category": {
    "Performance": ["NFR-PERF-001", ...],
    "Availability": [...],
    "Security": [...],
    "Accessibility": [...],
    "Scalability": [...]
  },
  "by_priority": {
    "P0": [...],
    "P1": [...],
    "P2": [...]
  },
  "statistics": {
    "total": 25,
    "by_category": {
      "Performance": 8,
      "Availability": 3,
      "Security": 5,
      "Accessibility": 6,
      "Scalability": 3
    },
    "smart_compliant": 25,
    "smart_compliant_percent": 100
  }
}
```

### Phase 5.10: Write NFR Documentation

Write `ProductSpecs_<SystemName>/02-api/NFR_SPECIFICATIONS.md`:

```markdown
# Non-Functional Requirements Specification

**System**: <SystemName>
**Generated**: <TIMESTAMP>
**Total NFRs**: 25

---

## Summary

| Category | Count | P0 | P1 | P2 |
|----------|-------|----|----|-----|
| Performance | 8 | 4 | 3 | 1 |
| Availability | 3 | 2 | 1 | 0 |
| Security | 5 | 5 | 0 | 0 |
| Accessibility | 6 | 6 | 0 | 0 |
| Scalability | 3 | 0 | 2 | 1 |

---

## Performance Requirements

### NFR-PERF-001: Screen Load Time

| Attribute | Value |
|-----------|-------|
| **ID** | NFR-PERF-001 |
| **Priority** | P0 |
| **Metric** | Page load time < 2s at 95th percentile |
| **Measurement** | Lighthouse performance audit |
| **Test Method** | `lighthouse --preset=desktop` |
| **Threshold** | 2000ms |

**Affected Modules**: MOD-INV-SEARCH-01, MOD-INV-ADJUST-01

**Acceptance Criteria**:
```gherkin
Scenario: Screen loads within acceptable time
  Given the user navigates to any screen
  When the page finishes loading
  Then the total load time should be less than 2 seconds
```

...

---

## SMART Compliance Matrix

All NFRs validated against SMART criteria:

| NFR ID | S | M | A | R | T |
|--------|---|---|---|---|---|
| NFR-PERF-001 | ✅ | ✅ | ✅ | ✅ | ✅ |
| NFR-AVAIL-001 | ✅ | ✅ | ✅ | ✅ | ✅ |
| ... | ... | ... | ... | ... | ... |
```

---

## SMART Metric Templates

### Performance

```
"{Action} completes in < {N}{unit} at {percentile}th percentile under {load} concurrent users"
```

### Availability

```
"{Component} achieves {N}% uptime measured over {period}"
```

### Accessibility

```
"{Screen|Component} passes {standard} {level} with {tool} automated scan"
```

### Security

```
"{Security control} enforced with < {N}ms latency overhead"
```

### Scalability

```
"System supports {N} {resource} per {scope} with < {degradation}% degradation"
```

---

## Outputs

| File | Location | Purpose |
|------|----------|---------|
| `nfr_registry.json` | `traceability/` (ROOT) | NFR registry (single source of truth) |
| `NFR_SPECIFICATIONS.md` | `ProductSpecs_<SystemName>/02-api/` | Human-readable doc |

---

## Error Handling

| Error | Action |
|-------|--------|
| Missing discovery data | **WARN** - Use defaults |
| NFR not SMART compliant | **WARN** - Flag for review |
| Missing module reference | **WARN** - Log, continue |

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `ProductSpecs_Generator` | Previous phase |
| `ProductSpecs_TestSpecGenerator` | Next phase - generates tests |
