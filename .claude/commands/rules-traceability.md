---
name: rules-traceability
description: Load detailed traceability rules (ID formats, source linking, version logging)
---

# Traceability Rules (On-Demand)

**Loaded when needed**: Creating/modifying artifacts, validating chains, troubleshooting references

---

## ID Formats by Stage

### Discovery (Stage 1)

| Artifact | ID Format | Example |
|----------|-----------|---------|
| Client Materials | `CM-XXX` | `CM-001` |
| Client Facts | `CF-XXX` | `CF-042` |
| Pain Points | `PP-X.X` | `PP-1.2` |
| Jobs To Be Done | `JTBD-X.X` | `JTBD-2.1` |
| User Types | `UT-[Role]` | `UT-Manager` |
| Requirements | `REQ-XXX` | `REQ-015` |
| Screens | `SCR-XXX` | `SCR-003` |

### Prototype (Stage 2)

| Artifact | ID Format | Example |
|----------|-----------|---------|
| Screens | `SCR-XXX` | `SCR-003` |
| Components | `CMP-XXX` | `CMP-045` |
| Interactions | `INT-XXX` | `INT-012` |

### ProductSpecs (Stage 3)

| Artifact | ID Format | Example |
|----------|-----------|---------|
| Modules | `MOD-XXX-XXX-NN` | `MOD-DSK-AUTH-01` |
| Test Cases | `TC-XXX` | `TC-142` |
| NFRs | `NFR-XXX` | `NFR-007` |

### SolArch (Stage 4)

| Artifact | ID Format | Example |
|----------|-----------|---------|
| ADRs | `ADR-XXX` | `ADR-003` |
| Building Blocks | `BB-XXX` | `BB-015` |

### Implementation (Stage 5)

| Artifact | ID Format | Example |
|----------|-----------|---------|
| Tasks | `T-NNN` | `T-042` |

---

## Source Linking (Discovery Only)

Every insight, requirement, or feature extracted from client materials MUST reference its source:

**Formats**:
- PDF: `(Source: filename.pdf, p. 12)`
- Interview: `(Source: interview-transcript.md:45)`
- Screenshot: `(Source: screenshot-03.png)`
- Spreadsheet: `(Source: data.xlsx, Sheet1:A5)`

**In markdown files**:
```markdown
## Pain Point: Inventory visibility issues
**Severity**: High
**Source**: ClientMaterials/interviews/manager-interview.md:78

"We have no idea what's in stock until we physically check the warehouse."
```

---

## Traceability Chains

### Complete Chain (All Stages)

```
CM-XXX → CF-XXX → PP-X.X → JTBD-X.X → REQ-XXX → SCR-XXX →
MOD-XXX → ADR-XXX → T-NNN → Code → Tests
```

### Stage-Specific Requirements

**Discovery**: Link pain points → client facts, JTBD → pain points
**Prototype**: Link screens → requirements, components → screens
**ProductSpecs**: Link modules → screens/requirements, tests → modules
**SolArch**: Link ADRs → requirements, building blocks → ADRs
**Implementation**: Link tasks → modules, code → tasks, tests → code

---

## Validation

### Check Traceability Integrity

```bash
# Full traceability chain validation
python3 .claude/hooks/implementation_quality_gates.py --validate-traceability

# Stage-specific validation
python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 10
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 14
```

### Common Violations

| Violation | Severity | Fix |
|-----------|----------|-----|
| Artifact without ID | CRITICAL | Assign ID using stage format |
| Missing source link (Discovery) | HIGH | Add source reference |
| Broken ID reference | CRITICAL | Fix reference or create target |
| Orphaned artifact | HIGH | Link to parent or justify standalone |
| Version history not logged | CRITICAL | Log immediately |

---

## Related

- **Full Documentation**: `architecture/Traceability_System.md`
- **Version Management**: `architecture/Version_and_Traceability_Management.md`
- **Quality Gates**: `architecture/Quality_Gates_Reference.md`
