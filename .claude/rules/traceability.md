---
paths:
  - "traceability/**/*"
  - "ClientAnalysis_*/**/*"
  - "Prototype_*/**/*"
  - "ProductSpecs_*/**/*"
  - "SolArch_*/**/*"
  - "Implementation_*/**/*"
  - "_state/**/*"
---

# Traceability Rules

**Auto-loaded when working with**: Stage output folders, traceability registries, state files

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

## Version History Logging (MANDATORY)

**Every file change (create, modify, delete) MUST be logged.**

**After every Write/Edit/Delete**:

```bash
python3 .claude/hooks/version_history_logger.py \
  "traceability/" \
  "{system_name}" \
  "{stage}" \
  "Claude" \
  "{version}" \
  "{reason}" \
  "{refs_comma_separated}" \
  "{file_path}" \
  "{action}"
```

**Parameters**:
- `system_name`: From `_state/pipeline_config.json` or `_state/discovery_config.json`
- `stage`: `discovery`, `prototype`, `productspecs`, `solarch`, `implementation`
- `version`: From `.claude/version.json` (Major.Minor) + local Patch
- `reason`: Single sentence explaining the change
- `refs_comma_separated`: IDs this change traces to (e.g., `JTBD-1,REQ-003,T-010`)
- `action`: `creation`, `modification`, `deletion`

**Failure to log is a framework integrity violation.** Even deletions must be logged.

---

## Related

- **Full Documentation**: `architecture/Traceability_System.md`
- **Version Management**: `architecture/Version_and_Traceability_Management.md`
- **Quality Gates**: `architecture/Quality_Gates_Reference.md`
