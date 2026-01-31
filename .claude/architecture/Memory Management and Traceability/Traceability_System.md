# Traceability System

**Version**: 1.0.0
**Created**: 2025-01-08
**Status**: Reference Document

This document defines the traceability ID system, cross-stage linking patterns, and the complete end-to-end traceability chain across all HTEC framework stages.

---

## Traceability ID Formats

All artifacts use hierarchical IDs with consistent prefixes:

| ID Prefix | Artifact Type | Stage | Example |
|-----------|---------------|-------|---------|
| `CM-XXX` | Client Material | Discovery | CM-001 |
| `CF-XXX` | Client Fact | Discovery | CF-042 |
| `PP-X.X` | Pain Point | Discovery | PP-1.1, PP-2.3 |
| `JTBD-X.X` | Job To Be Done | Discovery | JTBD-1.1, JTBD-2.1 |
| `S-X.X` | Screen (Discovery) | Discovery | S-1.1, S-1.2 |
| `REQ-XXX` | Requirement | Prototype | REQ-001 |
| `US-X.X` | User Story | Prototype | US-1.1 |
| `FR-X.X` | Feature Requirement | Prototype | FR-1.1 |
| `SCR-XXX` | Screen (Prototype) | Prototype | SCR-001 |
| `COMP-XXX` | Component | Prototype | COMP-015 |
| `MOD-XXX-XXX-NN` | Module Spec | ProductSpecs | MOD-DSK-DASH-01 |
| `NFR-XXX` | Non-Functional Req | ProductSpecs | NFR-001 |
| `TC-XXX` | Test Case | ProductSpecs | TC-001 |
| `INV-XXX` | JIRA Item | ProductSpecs | INV-001 |
| `ADR-XXX` | Architecture Decision | SolArch | ADR-001 |
| `QS-XXX` | Quality Scenario | SolArch | QS-001 |
| `T-NNN` | Implementation Task | Implementation | T-015 |
| `CR-XXX` | Change Request | Implementation | CR-001 |
| `FB-NNN` | Discovery Feedback | Discovery | FB-001 |
| `PF-NNN` | Prototype Feedback | Prototype | PF-001 |
| `PSF-NNN` | ProductSpecs Feedback | ProductSpecs | PSF-001 |
| `SF-NNN` | SolArch Feedback | SolArch | SF-001 |

---

## Module ID Convention

Module IDs follow the pattern: `MOD-<APP>-<FEAT>-<NN>`

| Segment | Description | Examples |
|---------|-------------|----------|
| `APP` | Application/Platform code | DSK (Desktop), MOB (Mobile), WEB (Web) |
| `FEAT` | Feature area | DASH (Dashboard), INV (Inventory), AUTH (Auth) |
| `NN` | Sequence number | 01, 02, 03... |

Example: `MOD-DSK-DASH-01` = Desktop Dashboard Module #01

---

## End-to-End Traceability Chain

The complete traceability chain connects client materials to implementation:

```
CM-XXX (Client Material)
    ↓ extracted_from
CF-XXX (Client Fact)
    ↓ supports
PP-X.X (Pain Point)
    ↓ addressed_by
JTBD-X.X (Job To Be Done)
    ↓ realized_by
REQ-XXX (Requirement)
    ↓ implemented_in
SCR-XXX (Screen)
    ↓ specified_by
MOD-XXX (Module Spec)
    ↓ decided_in
ADR-XXX (Architecture Decision)
    ↓ executed_by
T-NNN (Implementation Task)
    ↓ produces
src/features/*.ts (Code Location)
    ↓ verified_by
tests/unit/*.test.ts (Test File)
    ↓ tracked_in
INV-XXX (JIRA Item)
```

---

## Stage-to-Stage Traceability Links

### Discovery -> Prototype

| Discovery | Prototype | Link Type |
|-----------|-----------|-----------|
| `PP-X.X` (Pain Point) | `REQ-XXX` | `pain_point_refs` |
| `JTBD-X.X` (Job) | `US-XXX` | `jtbd_refs` |
| `PERSONA_*` | Screen specs | `persona_refs` |
| `S-X.X` (Screen) | `SCR-XXX` | `screen_refs` |
| `data-fields.md` | `data-model.md` | Entity mapping |

### Prototype -> ProductSpecs

| Prototype | ProductSpecs | Link Type |
|-----------|--------------|-----------|
| `REQ-XXX` | Module specs | `requirement_refs` |
| `SCR-XXX` | `MOD-XXX` | `screen_refs` |
| API contracts | Data contracts | Direct mapping |
| Components | Test specs | `component_refs` |

### ProductSpecs -> SolArch

| ProductSpecs | SolArch | Link Type |
|--------------|---------|-----------|
| `MOD-XXX` | Components | `module_refs` |
| `REQ-XXX` | ADRs | `requirement_refs` |
| `NFR-XXX` | Quality scenarios | `nfr_refs` |
| API contracts | API design | Direct mapping |
| Test specs | Testing strategy | `test_refs` |

### SolArch -> Implementation

| SolArch | Implementation | Link Type |
|---------|----------------|-----------|
| `MOD-XXX` | `T-NNN` Tasks | `module_ref` |
| `ADR-XXX` | Code patterns | Pattern compliance |
| `COMP-XXX` | Source files | `component_refs` |
| API design | API implementation | Contract validation |

---

## Traceability Registries

All traceability data is stored in JSON registries at the project root:

| Registry | Location | Created By |
|----------|----------|------------|
| Client Facts | `traceability/client_facts_registry.json` | Discovery |
| Discovery Traceability | `traceability/discovery_traceability_register.json` | Discovery |
| Screen Registry | `traceability/screen_registry.json` | Prototype |
| Requirements Registry | `traceability/requirements_registry.json` | Prototype/ProductSpecs |
| Prototype Traceability | `traceability/prototype_traceability_register.json` | Prototype |
| Module Registry | `traceability/module_registry.json` | ProductSpecs |
| NFR Registry | `traceability/nfr_registry.json` | ProductSpecs |
| Test Case Registry | `traceability/test_case_registry.json` | ProductSpecs |
| ProductSpecs Traceability | `traceability/productspecs_traceability_register.json` | ProductSpecs |
| Component Registry | `traceability/component_registry.json` | SolArch |
| ADR Registry | `traceability/adr_registry.json` | SolArch |
| SolArch Traceability | `traceability/solarch_traceability_register.json` | SolArch |
| Task Registry | `traceability/task_registry.json` | Implementation |
| Review Registry | `traceability/review_registry.json` | Implementation |
| Implementation Traceability | `traceability/implementation_traceability_register.json` | Implementation |

---

## Registry Entry Schemas

### Requirement Entry

```json
{
  "id": "REQ-001",
  "title": "User can login with email",
  "priority": "P0",
  "pain_point_refs": ["PP-1.1", "PP-1.2"],
  "jtbd_refs": ["JTBD-1.1"],
  "screen_refs": ["SCR-001"],
  "status": "implemented"
}
```

### Module Entry

```json
{
  "id": "MOD-DSK-DASH-01",
  "name": "Dashboard Overview Module",
  "requirement_refs": ["REQ-001", "REQ-002"],
  "screen_refs": ["SCR-001", "SCR-002"],
  "test_case_refs": ["TC-001", "TC-002"],
  "status": "specified"
}
```

### Task Entry

```json
{
  "id": "T-015",
  "title": "Implement KPI Card Component",
  "module_ref": "MOD-DSK-DASH-01",
  "requirement_refs": ["REQ-001"],
  "jira_ref": "INV-015",
  "code_files": ["src/components/KPICard.tsx"],
  "test_files": ["tests/unit/KPICard.test.tsx"],
  "status": "completed"
}
```

### ADR Entry

```json
{
  "id": "ADR-001",
  "title": "Microservices Architecture",
  "status": "accepted",
  "requirement_refs": ["REQ-001", "REQ-015"],
  "pain_point_refs": ["PP-1.1"],
  "nfr_refs": ["NFR-001", "NFR-002"]
}
```

---

## Feedback Traceability

Feedback items maintain their own traceability chain:

### Discovery Feedback

```
FB-NNN (Feedback Item)
    ↓ affects
Discovery Artifacts (personas, JTBD, vision)
    ↓ logged_in
traceability/feedback_sessions/discovery/<session>/
```

### Prototype Feedback

```
PF-NNN (Feedback Item)
    ↓ affects
Prototype Artifacts (specs, code, components)
    ↓ analyzed_by
Impact Analysis (with traceability chains)
    ↓ implemented_via
Implementation Plan
    ↓ logged_in
Prototype_<System>/feedback-sessions/<session>/
```

### Change Request Traceability

```
T-NNN (Implementation Task)
    ↓ triggers
CR-XXX (Change Request)
    ↓ analyzed_by
Root Cause Analysis (ANALYSIS.md)
    ↓ fixed_in
Implementation (Code + Tests)
    ↓ documented_in
Learnings (CLAUDE.md updates)
```

---

## Validation Commands

### Check Traceability Integrity

```bash
# Validate cross-stage links
python3 .claude/hooks/<stage>_quality_gates.py --validate-traceability --dir <OutputFolder>/

# Check all cross-stage links
/integrity-check --section links
```

### Verify Coverage

```bash
# P0 coverage check (ProductSpecs)
python3 .claude/hooks/productspecs_quality_gates.py --validate-checkpoint 7 --dir ProductSpecs_X/

# Pain point coverage (SolArch)
python3 .claude/hooks/solarch_quality_gates.py --validate-traceability --dir SolArch_X/
```

---

## Traceability Violations

| Violation | Severity | When Detected |
|-----------|----------|---------------|
| Pain point without client fact | CRITICAL | Discovery |
| JTBD without pain point ref | HIGH | Discovery |
| Screen without requirement refs | CRITICAL | Prototype |
| Module without screen refs | CRITICAL | ProductSpecs |
| P0 requirement without module | HIGH | ProductSpecs CP7 |
| ADR without requirement refs | CRITICAL | SolArch |
| Task without module ref | CRITICAL | Implementation |
| Implementation without test | CRITICAL | Implementation CP6 |

---

## Related Documentation

- **Version Management**: `architecture/Version_and_Traceability_Management.md`
- **Quality Gates**: `architecture/Quality_Gates_Reference.md`
- **Output Structures**: `architecture/Stage_Output_Structures.md`
- **Process Integrity**: `.claude/rules/process-integrity.md`
- **Traceability Guard**: `.claude/rules/traceability-guard.md`
