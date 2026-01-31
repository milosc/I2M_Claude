# Quality Gates Reference

**Version**: 1.0.0
**Created**: 2025-01-08
**Status**: Reference Document

This document consolidates checkpoint requirements and quality gate validation for all five HTEC framework stages.

---

## Quality Gate Scripts

| Stage | Validation Script |
|-------|------------------|
| Discovery | `python3 .claude/hooks/discovery_quality_gates.py` |
| Prototype | `python3 .claude/hooks/prototype_quality_gates.py` |
| ProductSpecs | `python3 .claude/hooks/productspecs_quality_gates.py` |
| SolArch | `python3 .claude/hooks/solarch_quality_gates.py` |
| Implementation | `python3 .claude/hooks/implementation_quality_gates.py` |

### Common Commands

```bash
# List all checkpoint requirements
python3 .claude/hooks/<stage>_quality_gates.py --list-checkpoints

# Validate a specific checkpoint
python3 .claude/hooks/<stage>_quality_gates.py --validate-checkpoint N --dir <OutputFolder>/

# Validate traceability
python3 .claude/hooks/<stage>_quality_gates.py --validate-traceability --dir <OutputFolder>/
```

---

## Stage 1: Discovery Checkpoint Requirements

| Checkpoint | Phase | Required Files | Blocking |
|------------|-------|----------------|----------|
| 0 | Initialize | `PROGRESS_TRACKER.md`, `FAILURES_LOG.md` | No |
| 1 | Analyze | `ANALYSIS_SUMMARY.md`, `traceability/client_facts_registry.json` (ROOT) | No |
| 1.5 | PDF Analysis | `PDF_ANALYSIS_INDEX.md`, `PDF_FINDINGS_SUMMARY.md` | No |
| 2 | Pain Points | `PAIN_POINTS.md` | No |
| 3 | Personas | `personas/PERSONA_*.md` | No |
| 4 | JTBD | `JOBS_TO_BE_DONE.md` | No |
| 5 | Vision | `PRODUCT_VISION.md` | No |
| 6 | Strategy | `PRODUCT_STRATEGY.md` | No |
| 7 | Roadmap | `PRODUCT_ROADMAP.md` | No |
| 8 | KPIs | `KPIS_AND_GOALS.md` | No |
| 9 | Design Specs | `screen-definitions.md`, `data-fields.md` | No |
| 10 | Documentation | `INDEX.md`, `README.md` | No |
| 10.5 | Audit | Zero hallucination audit pass | **YES** |
| 11 | Validation | `VALIDATION_REPORT.md` | No |

### Discovery Validation Workflow

1. **After each phase**: Run `--validate-checkpoint N` before proceeding
2. **If validation fails**: Fix the issue, re-run validation
3. **Log evidence**: Record validation output in `PROGRESS_TRACKER.md`
4. **No skipping**: Validation must pass before moving to next phase

### Zero Hallucination Audit (Checkpoint 10.5)

The `/discovery-audit` command acts as a strict semantic validator:
- Ensures every persona trait, JTBD, and requirement is backed by a specific citation `(Source: ...)` or Client Fact ID `(CF-...)`
- Detection of unsupported claims will **BLOCK** the pipeline
- Generates `CLIENT_CLARIFICATION_QUESTIONS.md` to bridge gaps

---

## Stage 2: Prototype Checkpoint Requirements

> **Note**: Paths starting with `_state/` are at the **ROOT level** (shared folder)

| Checkpoint | Phase | Required Outputs | Blocking |
|------------|-------|------------------|----------|
| 0 | Initialize | `_state/prototype_config.json` (ROOT), folder structure | No |
| 1 | Validate Discovery | `_state/discovery_summary.json` (ROOT), `traceability/screen_registry.json` (ROOT) | No |
| 2 | Requirements | `_state/requirements_registry.json` (ROOT) | No |
| 3 | Data Model | `data-model.md` | No |
| 4 | API Contracts | `api-contracts.json` | No |
| 5 | Test Data | `test-data/` folder with fixtures | No |
| 6 | Design Brief | `design-brief.md` | No |
| 7 | Design Tokens | `design-tokens.json`, `color-system.md`, etc. | No |
| 8 | Components | `01-components/component-index.md`, component specs | No |
| 9 | Screens | `02-screens/screen-index.md`, screen folders, **ALL Discovery screens** | No |
| 10 | Interactions | `motion-system.md`, `accessibility-spec.md` | No |
| 11 | Build Sequence | `build-sequence.md` | No |
| 12 | Code Generation | `prototype/` code, **ALL screens have React code** | No |
| 13 | QA | `qa-report.md` | No |
| 14 | UI Audit | `ui-audit-report.md`, **100% screen coverage** | No |

### Prototype-Specific Validations

```bash
# Validate feedback item
python3 .claude/hooks/prototype_quality_gates.py --validate-feedback PF-001 --dir Prototype_X/

# Validate feedback registry structure
python3 .claude/hooks/prototype_quality_gates.py --validate-feedback-registry --dir Prototype_X/

# List all feedback items with status
python3 .claude/hooks/prototype_quality_gates.py --list-feedback --dir Prototype_X/
```

---

## Stage 3: ProductSpecs Checkpoint Requirements

| Checkpoint | Phase | Required Outputs | Blocking |
|------------|-------|------------------|----------|
| 0 | Initialize | `_state/productspecs_config.json`, folder structure | No |
| 1 | Validate | Validation report, discovery_summary available | No |
| 2 | Extract | `traceability/requirements_registry.json` (ROOT) | No |
| 3 | Module Design | Module specifications started | No |
| 4 | Modules | `01-modules/module-index.md`, MOD-*.md files | No |
| 5 | Contracts | `02-api/api-index.md`, `NFR_SPECIFICATIONS.md` | No |
| 6 | Tests | `03-tests/test-case-registry.md`, test specs | No |
| 7 | Traceability | **100% P0 coverage**, traceability matrix | **YES** |
| 8 | Export | `04-jira/full-hierarchy.csv`, IMPORT_GUIDE.md | No |

### ProductSpecs Blocking Gate (CP7)

Checkpoint 7 enforces **100% P0 coverage**:
- All P0 priority requirements must have module specifications
- All P0 modules must have test cases
- Traceability chain must be complete for P0 items
- Missing P0 coverage will **BLOCK** progression

---

## Stage 4: SolArch Checkpoint Requirements

| Checkpoint | Phase | Required Outputs | Blocking |
|------------|-------|------------------|----------|
| 0 | Initialize | Config, folder structure | No |
| 1 | Validate | Input validation (ProductSpecs CP 8+, Prototype CP 14+) | **YES** |
| 2 | Context | Introduction, constraints, context docs | No |
| 3 | Strategy | Solution strategy, ADR-001, ADR-002 | No |
| 4 | Blocks | Building blocks, C4 diagrams | No |
| 5 | Runtime | API design, event communication | No |
| 6 | Quality | Quality requirements, security | No |
| 7 | Deploy | Deployment view, operations guide | No |
| 8 | Decisions | All ADRs (min 9), decisions.json | No |
| 9 | Risks | Risks and technical debt | No |
| 10 | Docs | Glossary | No |
| 11 | Trace | **100% pain point & requirement coverage** | **YES** |
| 12 | Final | Validation report, summary | No |

### SolArch Blocking Gates

**CP1 (Validate Inputs)**:
- ProductSpecs must be at checkpoint 8+
- Prototype must be at checkpoint 14+
- Required registries must exist

**CP11 (Trace)**:
- 100% pain point coverage required
- 100% requirement coverage required
- All ADRs must have requirement references

---

## Stage 5: Implementation Checkpoint Requirements

| Checkpoint | Phase | Required Outputs | Blocking |
|------------|-------|------------------|----------|
| 0 | Initialize | `_state/implementation_config.json`, folder structure | No |
| 1 | Validate | ProductSpecs CP8+, SolArch CP12+, 100% P0 coverage | **YES** |
| 2 | Tasks | `traceability/task_registry.json`, TASK_INDEX.md | No |
| 3 | Infrastructure | All Phase 3 tasks complete | No |
| 4 | Features 50% | 50%+ tasks complete | No |
| 5 | P0 Complete | All P0 priority tasks done | No |
| 6 | Code Review | No CRITICAL findings, coverage > 80% | **YES** |
| 7 | Integration | Integration tests pass, API contracts valid | No |
| 8 | Documentation | API docs, deployment guide, README | No |
| 9 | Validation | Final validation report, traceability complete | No |

### Implementation Blocking Gates

**CP1 (Validate Inputs)**:
- ProductSpecs must be at checkpoint 8+
- SolArch must be at checkpoint 12+
- 100% P0 requirements must be covered in task decomposition
- Required registries must exist

**CP6 (Code Review)**:
- CRITICAL findings == 0
- HIGH findings <= 5 (with remediation plan)
- Test coverage >= 80%
- Security audit PASS
- All P0 tasks completed

### Implementation-Specific Validations

```bash
# Validate a specific task
python3 .claude/hooks/implementation_quality_gates.py --validate-task T-015 --dir Implementation_X/

# Validate TDD compliance
python3 .claude/hooks/implementation_quality_gates.py --validate-tdd --task T-015
```

---

## TDD Protocol (Implementation)

All implementation follows Test-Driven Development:

```
1. RED     - Write failing test for acceptance criterion
2. GREEN   - Write minimal code to pass test
3. REFACTOR - Clean up while keeping green
4. VERIFY  - Run full test suite
5. MARK    - Update task registry
```

### TDD Validation

- Test file MUST exist before implementation
- Test MUST fail initially (proves test works)
- Implementation committed before test -> HIGH violation
- Implementation without test -> CRITICAL (blocks CP6)

---

## Multi-Agent Code Review (Implementation CP6)

Checkpoint 6 uses 6 specialized review agents (run in parallel):

| Agent | Focus | Severity |
|-------|-------|----------|
| `bug-hunter` | Logic errors, null safety, edge cases | HIGH |
| `security-auditor` | OWASP Top 10, injection, auth | CRITICAL |
| `code-quality` | SOLID, DRY, complexity | MEDIUM |
| `test-coverage` | Missing tests, mock issues | HIGH |
| `contracts-reviewer` | API contract compliance | HIGH |
| `accessibility-auditor` | WCAG compliance | MEDIUM |

---

## Integrity Check (Cross-Stage Validation)

The `/integrity-check` command provides comprehensive validation across all stages:

```bash
# Full integrity report
/integrity-check

# Quick summary only
/integrity-check --quick

# Check specific section
/integrity-check --section state           # State files only
/integrity-check --section traceability    # Traceability only
/integrity-check --section artifacts       # Build artifacts only
/integrity-check --section links           # Cross-stage links only
/integrity-check --section drift           # Template drift only

# JSON output for CI/CD
/integrity-check --json

# Include fix instructions
/integrity-check --fix
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | Warnings only |
| 2 | Errors found |
| 3 | Critical errors |

---

## Related Documentation

- **Output Structures**: `architecture/Stage_Output_Structures.md`
- **Traceability System**: `architecture/Traceability_System.md`
- **Process Integrity**: `.claude/rules/process-integrity.md`
- **Command References**: `.claude/commands/*_COMMAND_REFERENCE.md`
