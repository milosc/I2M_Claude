---
description: Review Discovery audit results and validate zero-hallucination compliance
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-audit-review started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-audit-review ended '{"stage": "discovery"}'
---


````markdown
# /discovery-audit-review - Chef Product Manager Review Gate

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-audit-review instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Discovery-specific rules. Load them now:

```bash
# Load Discovery rules (includes PDF handling, input processing, output structure)
/rules-discovery

# Load Traceability rules (includes ID formats, source linking)
/rules-traceability
```

## Usage

```
/discovery-audit-review <SystemName>
```

## Arguments

- `SystemName`: Name of the system (e.g., InventorySystem, ERTriage)

## Prerequisites

- `ClientAnalysis_<SystemName>/` folder exists with complete analysis outputs
- Phase 9 (Design Specs) has been completed
- All discoverable artifacts exist:
  - `01-analysis/ANALYSIS_SUMMARY.md` (or equivalent)
  - `02-research/PAIN_POINTS.md`
  - `02-research/personas/PERSONA_*.md`
  - `02-research/JOBS_TO_BE_DONE.md`
  - `03-strategy/PRODUCT_STRATEGY.md`, `PRODUCT_VISION.md`, `PRODUCT_ROADMAP.md`, `KPIS_AND_GOALS.md`
  - `04-design-specs/` (all design specification files)
  - `traceability/client_facts_registry.json`
  - `traceability/trace_matrix.json`

## Agent Used

- **Agent ID**: `discovery-fact-auditor-reviewer` (Chef Product Manager Reviewer)
- **Model**: claude-3.5-sonnet
- **Checkpoint**: CP-9.5 (Post-Design-Specs Validation)
- **Blocking**: YES - Pipeline gates on results

## Skills Used

- `.claude/skills/Discovery_FactAuditor/SKILL.md` (Fact verification and hallucination detection)
- `.claude/skills/traceability/Traceability_Guard.md` (Registry integrity validation)

## Procedure

### 1. Initialize Audit
- ⏳ Starting fact-check audit and product manager review for `<SystemName>`...
- Load agent: `discovery-fact-auditor-reviewer`
- Invoke `Traceability_Guard` to ensure registry backbone is healthy
- Validate all input artifacts are readable and complete

### 2. Execute Auditor Agent
- **Load Ground Truth**: Index all CF-* IDs from `client_facts_registry.json` with source materials
- **Scan Artifacts**: Iterate through all ClientAnalysis outputs (02-research/, 03-strategy/, 04-design-specs/)
- **Verify Claims**: For each major assertion, verify against source client materials
  - Pain Point claims → Interview quotes, client facts
  - Persona traits → User behavior evidence from materials
  - JTBD steps → Workflow evidence from screenshots or interviews
  - Strategy statements → Client-stated business goals
  - Design specs → Requirements traceable to pain points/JTBDs
- **Check Citations**: Ensure all P0 claims have `(Source: CF-XXX)` tags or client material references
- **Detect Hallucinations**: Flag statements using "industry standards" not found in ground truth
- **Validate Registries**: Cross-check pain_point_registry → jtbd_registry → traceability chains

### 3. Generate Reports

The agent produces four output files:

#### **AUDIT_REPORT.md** (Comprehensive Findings)
```
Executive Summary:
  - Total claims reviewed: 247
  - Claims with valid citations: 235 (95%)
  - Hallucinations found: P0 = 0, P1 = 5, P2 = 8
  - Recommendation: PASS

By Category:
  - Pain Points: 12 verified, 0 flagged
  - Personas: 5 verified, 1 flagged
  - JTBDs: 18 verified, 2 flagged
  - Strategy: 25 verified, 2 flagged
  - Design Specs: 60 verified, 3 flagged

Detailed Findings:
  [Lists every flagged claim with quote, location, severity]

Summary Statistics:
  - Files scanned: 15
  - Broken trace links: 0
  - Claims lacking any citation: 2
```

#### **CLIENT_CLARIFICATION_QUESTIONS.md** (User-Facing Questions)
```
Q1. Pain Points: You mentioned "3-5 minute triage time constraint" in PAIN_POINTS.md,
    but interviews show range from 2-8 minutes. What is the realistic target?
    
Q2. Personas: The "Nurse Manager" persona includes "staff scheduling" responsibility.
    Is this truly in scope, or is it a future phase capability?
    
Q3. JTBD: "Real-time collaboration" mentioned in JTBD-1.5, but only 2/5 interviewees
    raised this. Should it be core or secondary job?
```

#### **AUDIT_SUMMARY.json** (Machine-Readable Results)
```json
{
  "audit_id": "AUD-2025-12-29-001",
  "system_name": "ER_Triage",
  "audit_timestamp": "2025-12-29T14:30:00Z",
  "auditor": "discovery-fact-auditor-reviewer",
  "results": {
    "total_claims_reviewed": 247,
    "verified_with_citations": 235,
    "hallucinations_p0": 0,
    "hallucinations_p1": 5,
    "hallucinations_p2": 8,
    "unresolved_trace_links": 0,
    "recommendation": "PASS"
  },
  "files_scanned": 15,
  "blocking_issues": [],
  "timestamp": "2025-12-29T14:30:00Z"
}
```

#### **HALUCINATIONS_LOG.md** (If Issues Found)
```
### P0 Blocking Issues (Pipeline Block)
[Lists any P0 hallucinations found with evidence]

### P1 Quality Issues (Requires Clarification)
ISSUE-001: Unverified inference
  - Claim: "Emergency physicians need real-time collaboration"
  - Evidence: Only mentioned by 2/5 interviewees
  - Action: Add CLIENT_CLARIFICATION_QUESTION

### P2 Information Issues (Logged, Allow Progression)
[Lists P2-severity issues for reference]
```

### 4. Make GO/NO-GO Decision

#### **PASS Decision** ✅
- 100% of P0 claims have valid citations
- No factual contradictions with client materials
- All registries validated with no broken links
- **Action**: Allow progression to next stage (Prototype)

#### **BLOCK Decision** ❌
- Any P0 hallucination detected
- Factual contradiction with client materials
- Missing critical prerequisites
- **Action**: Stop pipeline. Present report to user. Request fixes before re-audit.

#### **CONDITIONAL PASS Decision** ⚠️
- P1 issues exist (unverified but plausible)
- P0 criteria all met
- Clarification questions generated
- **Action**: Allow progression with CLIENT_CLARIFICATION_QUESTIONS logged for client follow-up

### 5. Update Traceability

- Mark audit completion in `trace_matrix.json`
- Record audit ID in `discovery_progress.json`
- Update `_state/discovery_progress.json` with CP-9.5 checkpoint status

### 6. Log to History

- Execute version history logger to record the audit action
- Store AUDIT_SUMMARY.json in discovery state for future reference

## Output Files

All outputs placed in: `ClientAnalysis_<SystemName>/05-documentation/`

| File | Purpose | Size | Audience |
|------|---------|------|----------|
| `AUDIT_REPORT.md` | Technical audit findings | 2-5 pages | Technical review |
| `CLIENT_CLARIFICATION_QUESTIONS.md` | Questions for client | 1-2 pages | Client/PM |
| `AUDIT_SUMMARY.json` | Machine-readable results | <1 KB | Tooling/automation |
| `HALUCINATIONS_LOG.md` | Error details (if needed) | 1-3 pages | Technical review |

## Quality Gates

### Pre-Audit Checks
- ✓ All input artifacts readable
- ✓ client_facts_registry.json contains ≥ 10 CF entries
- ✓ At least one source material file referenced

### During-Audit Checks
- ✓ Every paragraph scanned (100% artifact coverage)
- ✓ All assertions classified (Factual/Analytical/Prescriptive)
- ✓ All citations validated against registry

### Post-Audit Checks
- ✓ AUDIT_REPORT.md lists all scanned files
- ✓ CLIENT_CLARIFICATION_QUESTIONS.md is grammatically correct
- ✓ AUDIT_SUMMARY.json passes schema validation
- ✓ Recommendation is one of: PASS, BLOCK, CONDITIONAL_PASS

## Error Handling

### Missing Inputs
- Missing `client_facts_registry.json`: **BLOCK** - Cannot audit without ground truth
- Missing ClientAnalysis folder: **BLOCK** - Nothing to audit
- Missing individual artifact files: **LOG** - Continue with available files, note gaps

### Unreadable Files
- PDF parsing error: **SKIP** - Log failure, continue with other files
- JSON parse error in registry: **BLOCK** - Cannot establish ground truth

### Contradictory Evidence
- Two quotes supporting opposite claims: **FLAG** as P0 - Requires client clarification
- Claim contradicted by multiple sources: **BLOCK** - Factual error

### Ambiguous Citations
- Claim could refer to multiple CF entries: **FLAG** as P1 - Request clarification
- Inference that could be verified further: **CONDITIONAL** - Allow with question

## Success Criteria

The audit is successful when:

1. ✓ All ClientAnalysis artifact files are scanned (100% coverage)
2. ✓ Every major claim is classified (Factual/Analytical/Prescriptive/Filler)
3. ✓ All citations are validated against `client_facts_registry.json`
4. ✓ AUDIT_REPORT.md contains complete evidence trails
5. ✓ CLIENT_CLARIFICATION_QUESTIONS.md is ready for PM review
6. ✓ Recommendation decision is made with clear rationale
7. ✓ traceability/trace_matrix.json updated with audit status
8. ✓ No unresolved broken links in registries

## Integration with Pipeline

```
Stage 1: DISCOVERY
├─ CP-0: Initialize
├─ CP-1: Analyze Materials
├─ CP-1.5: PDF Deep Analysis
├─ CP-2: Extract Pain Points
├─ CP-3: Generate Personas
├─ CP-4: Extract JTBD
├─ CP-5-8: Generate Strategy Documents
├─ CP-9: Generate Design Specs
│   ▼
├─ CP-9.5: FACT AUDIT REVIEW ◄──── /discovery-audit-review <SystemName>
│   │     discovery-fact-auditor-reviewer agent
│   │     [BLOCKING CHECKPOINT]
│   │
│   ├─ PASS   ──────► Continue to CP-10
│   ├─ BLOCK  ──────► HALT (request fixes, re-audit)
│   └─ CONDITIONAL ─► Continue with questions logged
│   ▼
├─ CP-10: Documentation
├─ CP-11: Final Validation
│
└─► Ready for PROTOTYPE stage (Stage 2)
```

## Examples

### Example 1: Complete Pass
```
/discovery-audit-review InventorySystem

✅ Audit Complete: InventorySystem
   Total Claims: 180 | Verified: 180 (100%)
   Hallucinations: P0=0, P1=0, P2=0
   ✓ PASS - All systems go for Prototype stage
```

### Example 2: Conditional Pass with Questions
```
/discovery-audit-review ERTriage

⚠️ Audit Complete: ERTriage
   Total Claims: 247 | Verified: 235 (95%)
   Hallucinations: P0=0, P1=5, P2=8
   ⚠️ CONDITIONAL PASS - 5 items need client clarification
   → Review: ClientAnalysis_ERTriage/05-documentation/CLIENT_CLARIFICATION_QUESTIONS.md
```

### Example 3: Blocking Issues
```
/discovery-audit-review PatientPortal

❌ Audit Failed: PatientPortal
   Total Claims: 156 | Verified: 142 (91%)
   Hallucinations: P0=3, P1=4, P2=6
   ❌ BLOCK - 3 P0 hallucinations found
   → Review: ClientAnalysis_PatientPortal/05-documentation/HALUCINATIONS_LOG.md
   → Fix issues before re-audit
```

## Related Commands

- `/discovery-audit` - Older fact audit (triggers the underlying skill directly)
- `/discovery-validate` - General validation across discovery materials
- `/discovery-export` - Export Discovery outputs for next stage (only if audit passes)

## Notes

- This is a **Chef Product Manager Review** - acts as final quality gate before downstream stages
- Runs at **CP-9.5**, between Design Specs and Documentation generation
- Uses existing `Discovery_FactAuditor` and `Traceability_Guard` skills as foundation
- Adds product management layer reasoning (severity, strategic impact, client communication)
- **One Attempt Pattern**: If audit fails, stop and report. No auto-retry loops.

````
