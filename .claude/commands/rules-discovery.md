---
name: rules-discovery
description: Load Discovery-specific rules (input processing, output structure, validation)
---

# Discovery Rules (On-Demand)

**Loaded when needed**: Discovery Stage 1 execution, client material processing

---

## 1. Traceability

**See**: `/rules-traceability` for ID formats, source linking, and version history logging.

---

## 2. Input Processing

### PDF Handling
- **Always check page count** before processing
- **>10 pages MUST use** `pdf_splitter.py` for chunking

```bash
# Check page count FIRST
.venv/bin/python .claude/skills/tools/pdf_splitter.py count <file.pdf>

# If >10 pages, convert to Markdown
.venv/bin/python .claude/skills/tools/pdf_splitter.py automd <file.pdf> [OUTPUT_DIR]/
```

### Validation
- Verify input files (Interviews, Manuals) are readable before starting deep analysis
- If corrupt or unreadable: Log to `_state/skipped_files.log` and CONTINUE

### Skipping
- If an input file cannot be processed, log the failure and continue
- Never retry failed operations (see CORE_RULES.md error handling)

---

## 3. Output Structure

### Strict Compliance
- Outputs MUST be placed in `ClientAnalysis_<SystemName>/[Phase]/`
- Use `kebab-case` for filenames unless otherwise specified
- All text outputs should be Markdown

### Folder Structure

```
ClientAnalysis_<SystemName>/
├── 01_Research/
│   ├── personas/
│   └── jobs-to-be-done/
├── 02_Documentation/
│   ├── vision/
│   ├── product-strategy/
│   └── roadmap/
├── 03_Strategy/
│   ├── kpis/
│   └── goals/
├── 04_UX/
│   ├── interaction-patterns/
│   └── navigation/
├── 05_Design/
│   ├── screens/
│   ├── components/
│   └── data-fields/
└── 06_Support/
    ├── analysis-summary/
    ├── getting-started/
    └── progress-tracker/
```

---

## 4. State Management

### Checkpoints
- Before starting a phase, check `_state/progress.json` to resume
- Store checkpoint progress in `_state/discovery_config.json`

### Idempotency
- Re-running a completed phase should verify existing outputs
- Ask user if they want to regenerate (unless `--force` flag)

---

## 5. Quality Guardrails (MANDATORY)

### Predictability Gate
No phase is complete without proof of validation:

```bash
# End of every phase
python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint <N>
```

### Deliverable Integrity
Every newly created or modified markdown file MUST be validated:

```bash
# Validate file metadata and traceability IDs
python3 .claude/hooks/discovery_quality_gates.py --validate-file <Path>
```

### Self-Correction
If validation fails:
1. **ANALYZE** the error
2. **FIX** the root cause
3. **RETRY** validation
4. Only then mark progress as complete

---

## 6. Source Linking (Critical)

Every Discovery artifact MUST trace back to source materials:

**Required Formats:**
- PDF: `(Source: filename.pdf, p. 12)`
- Interview: `(Source: interview-transcript.md:45)`
- Screenshot: `(Source: screenshot-03.png)`
- Spreadsheet: `(Source: data.xlsx, Sheet1:A5)`

**Example in Pain Point:**
```markdown
## PP-1.2: Manual inventory tracking
**Severity**: High
**Source**: ClientMaterials/interviews/warehouse-manager.md:78

"We still use clipboards and paper to track inventory movements."
```

---

## 7. Discovery Checkpoints

| CP | Phase | Requirements |
|----|-------|-------------|
| 1 | Initial Scan | All client materials catalogued |
| 2 | Pain Points | All pain points extracted with sources |
| 3 | JTBD | All JTBD mapped to pain points |
| 4 | Personas | All personas have evidence |
| 5 | Vision | Vision aligned with pain points |
| 6 | Strategy | Strategy mapped to personas |
| 7 | Roadmap | Roadmap linked to JTBD |
| 8 | Screens | All screens mapped to requirements |
| 9 | Components | Components linked to screens |
| 10 | Validation | All deliverables validated |
| 10.5 | Zero Hallucination Audit | Every claim has source citation |

---

## 8. Zero Hallucination Audit

**Command**: `/discovery-audit`

**Requirements**:
- Every persona trait → Quote or client fact
- Every JTBD → Pain point reference
- Every requirement → JTBD or pain point
- Every screen → Requirement reference

**Violations**:
- Unsupported claim (no source) → CRITICAL
- Weak evidence (inferred, not cited) → HIGH
- Missing client fact ID → MEDIUM

---

## 9. Common Validation Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Missing metadata | File header incomplete | Add required frontmatter |
| Orphaned artifact | No parent references | Link to parent ID |
| Missing source | No citation in Discovery | Add source reference |
| Invalid ID format | Wrong naming pattern | Use correct format (PP-X.X, JTBD-X.X) |
| Empty deliverable | File <100 bytes | Generate proper content |

---

## 10. Discovery Commands Quick Reference

| Command | Phase | Purpose |
|---------|-------|---------|
| `/discovery-init` | Setup | Initialize Discovery session |
| `/discovery-analyze` | CP 1-4 | Extract pain points, JTBD, personas |
| `/discovery-research` | CP 4 | Generate personas and JTBD docs |
| `/discovery-specs-all` | CP 5-9 | Generate all design specs |
| `/discovery-docs-all` | CP 5-7 | Generate vision, strategy, roadmap |
| `/discovery-audit` | CP 10.5 | Zero hallucination audit |
| `/discovery-export` | Final | Export for Prototype stage |

---

## Related

- **Full checkpoint list**: `python3 .claude/hooks/discovery_quality_gates.py --list-checkpoints`
- **Quality gates**: `architecture/Quality_Gates_Reference.md`
- **Stage outputs**: `architecture/Stage_Output_Structures.md`
- **Discovery orchestrator**: `.claude/agents/discovery-orchestrator.md`
