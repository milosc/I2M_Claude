---
name: auditing-discovery-facts
description: Strict semantic verification of Discovery artifacts against ground truth client materials for zero hallucination audit.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill auditing-discovery-facts started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill auditing-discovery-facts ended '{"stage": "discovery"}'
---

# Discovery_FactAuditor

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill auditing-discovery-facts instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

## Metadata
- **Skill ID**: Discovery_FactAuditor
- **Version**: 1.0.0
- **Purpose**: Strict semantic verification of Discovery artifacts against ground truth client materials.

## Description
This skill acts as a formal auditor that scrutinizes every claim, persona, and job-to-be-done. It ensures that no "AI assumptions" or "industry standards" are mixed with actual client requirements unless explicitly stated in the source materials.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:auditing-discovery-facts:started` - When skill begins
- `skill:auditing-discovery-facts:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Dependencies
This skill leverages the following framework components:
- `Traceability_Guard`: To verify backbone integrity before auditing.
- `client_facts_registry.json`: Produced by `Discovery_ExtractClientFacts` as ground truth.
- `Trace_Matrix_Manager`: (Internal) To flag broken links in the master matrix.
- `version_history_logger`: To record the audit event in the global history.

## Trigger Conditions
- Invoked by the `/discovery-audit` command.
- Should be run after Phase 9 (Design Specs) but before Phase 11 (Final Validation).

## Input Requirements
| Input | Required | Description |
|-------|----------|-------------|
| `01-analysis/ANALYSIS_SUMMARY.md` | Yes | Ground truth summary of client materials. |
| `traceability/client_facts_registry.json` | Yes | Atomic facts extracted from sources. |
| `02-research/`, `03-strategy/`, `04-design-specs/` | Yes | Directories containing the generated artifacts to be audited. |

## Execution Steps

### 1. Load Ground Truth
Read and index all `CF-` (Client Fact) IDs from `traceability/client_facts_registry.json` and key findings from `ANALYSIS_SUMMARY.md`.

### 2. Scrutinize Artifacts
Iterate through every `.md` and `.json` file in the research, strategy, and design-specs folders.

### 3. Verify Citations & Traceability
- **Check Citations**: Every major assertion (Pain Point, Persona trait, JTBD) MUST have a `(Source: ...)` tag or a reference to a `CF-` ID.
- **Cross-Reference**: Verify that referenced `CF-` IDs actually exist in the registry.
- **Detect "Filler"**: Flag generic statements like "The user wants a seamless experience" if they are not tied to a specific pain point or fact.

### 4. Detect Hallucinations
- **Assumption Check**: Flag claims that use "common knowledge" not found in the ground truth.
- **Missing Link**: Flag any item where the traceability chain is broken (e.g., a JTBD that doesn't map to a Pain Point or Client Fact).

### 5. Remediation & Question Generation
- **Flag for Removal**: Create a list of items that are purely hallucinatory.
- **Clarification Questions**: For items that *might* be true but lack evidence, generate a specific question for the client.

### 6. Update Traceability
Update `traceability/trace_matrix.json` to flag items with "Broken" or "Unverified" status.

### 7. VERIFICATION GATE (MANDATORY)
- Validate that `AUDIT_REPORT.md` lists every file checked.
- Ensure `CLIENT_CLARIFICATION_QUESTIONS.md` is formatted for human readability.

## Output Structure
- `ClientAnalysis_<SystemName>/05-documentation/AUDIT_REPORT.md`
- `ClientAnalysis_<SystemName>/05-documentation/CLIENT_CLARIFICATION_QUESTIONS.md`
- `ClientAnalysis_<SystemName>/05-documentation/HALUCINATIONS_LOG.md` (if errors found)

## Error Handling
- **One Attempt**: If a file is unreadable, log it as a failure in the audit and continue to the next. Do not retry.

## Validation
- Audit passes ONLY if 100% of P0 claims have valid citations.
