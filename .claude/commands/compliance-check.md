---
name: compliance-check
description: Run compliance validation against regulatory standards (ISO 13485, GDPR, FDA, etc.)
model: sonnet
allowed-tools: Read, Grep, Glob, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill compliance-check started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill compliance-check ended '{"stage": "utility"}'
---

# /compliance-check Command

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill compliance-check instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

## Usage

```bash
/compliance-check <SystemName> --standard <standard> [--output <path>]
```

## Available Standards

| Standard | GRC Skill Used | Domain |
|----------|---------------|--------|
| `iso13485` | GRC_quality-manager-qms-iso13485 | Medical Device QMS |
| `gdpr` | GRC_gdpr-dsgvo-expert | EU Data Protection |
| `hipaa` | GRC_data-privacy-compliance | Healthcare Data |
| `fda` | GRC_fda-consultant-specialist | FDA 21 CFR Part 11 |
| `mdr` | GRC_mdr-745-specialist | EU Medical Device Regulation |
| `iso27001` | GRC_information-security-manager-iso27001 | Information Security |
| `risk` | GRC_risk-management-specialist | ISO 14971 Risk Management |

## Examples

```bash
# Medical device compliance
/compliance-check MedicalDevice --standard iso13485,mdr,fda

# Healthcare application
/compliance-check HealthApp --standard gdpr,hipaa

# Security-focused application
/compliance-check SecureApp --standard iso27001
```

## Workflow

### Step 1: Parse Arguments

Extract:
- `<SystemName>` - System being evaluated
- `--standard` - Comma-separated list of standards to evaluate
- `--output` - Optional output path (defaults to `{SystemName}_compliance/`)

### Step 2: Load GRC Skills

For each standard specified, load the corresponding GRC skill:

| Standard | Skill Path |
|----------|------------|
| iso13485 | `.claude/skills/GRC_quality-manager-qms-iso13485/SKILL.md` |
| gdpr | `.claude/skills/GRC_gdpr-dsgvo-expert/SKILL.md` |
| hipaa | `.claude/skills/GRC_data-privacy-compliance/SKILL.md` |
| fda | `.claude/skills/GRC_fda-consultant-specialist/SKILL.md` |
| mdr | `.claude/skills/GRC_mdr-745-specialist/SKILL.md` |
| iso27001 | `.claude/skills/GRC_information-security-manager-iso27001/SKILL.md` |
| risk | `.claude/skills/GRC_risk-management-specialist/SKILL.md` |

### Step 3: Analyze Artifacts

Scan and analyze:
1. **ProductSpecs outputs** (if available): `ProductSpecs_{SystemName}/`
2. **SolArch outputs** (if available): `SolArch_{SystemName}/`
3. **Implementation** (if available): `Implementation_{SystemName}/`

### Step 4: Generate Compliance Report

For each loaded standard, evaluate:

1. **Gap Analysis** - What requirements are missing?
2. **Compliance Score** - Percentage of requirements met
3. **Remediation Actions** - Specific steps to achieve compliance
4. **Evidence Matrix** - Map requirements to implementation evidence

### Step 5: Output

Generate compliance report to `{output_path}/`:

```
{SystemName}_compliance/
├── COMPLIANCE_SUMMARY.md       # Executive summary
├── GAP_ANALYSIS.md             # Detailed gaps per standard
├── REMEDIATION_PLAN.md         # Prioritized remediation steps
├── EVIDENCE_MATRIX.md          # Requirement-to-evidence traceability
└── per_standard/
    ├── ISO13485_compliance.md
    ├── GDPR_compliance.md
    └── ...
```

## Report Templates

### COMPLIANCE_SUMMARY.md

```markdown
# Compliance Summary: {SystemName}

**Generated**: {date}
**Standards Evaluated**: {standards_list}

## Overall Score

| Standard | Score | Status |
|----------|-------|--------|
| ISO 13485 | 85% | ⚠️ Partial |
| GDPR | 92% | ✅ Compliant |

## Critical Gaps

1. [GAP-001] Missing data retention policy (GDPR Art. 5)
2. [GAP-002] No risk assessment documentation (ISO 13485 7.3.3)

## Recommended Actions

1. **Priority 1**: Create data retention policy
2. **Priority 2**: Document risk assessment process
```

## Integration with ProductSpecs

When ProductSpecs artifacts exist, the compliance check will:
1. Trace requirements (REQ-*) to compliance mandates
2. Verify NFRs cover compliance-critical areas
3. Check test coverage for compliance scenarios

## Notes

- Compliance checks are advisory, not legal certification
- Always consult qualified regulatory experts for final validation
- GRC skills provide guidance based on HTEC best practices
