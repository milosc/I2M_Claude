---
description: Generate risk assessment and mitigation strategies
argument-hint: None
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-risks started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-risks ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-risks instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

This command generates the risks and technical debt documentation, capturing known risks, their mitigations, and technical debt items. This is Checkpoint 9 of the pipeline.

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` (auto-detected from config if not provided)

## Usage

```bash
/solarch-risks InventorySystem
```

## Prerequisites

- Checkpoint 8 passed (`/solarch-decisions` completed)
- ADRs available with consequences sections

## Skills Used

Read BEFORE execution:
- `.claude/skills/SolutionArchitecture_Arc42Generator/SKILL.md`

## Execution Steps

### Step 1: Execute

```
LOAD _state/solarch_config.json
SYSTEM_NAME = config.system_name

READ ADR consequences:
  FOR each ADR in 09-decisions/ADR-*.md:
    EXTRACT negative consequences
    IDENTIFY technical debt items
    Note risk implications

### Risk Acceptance Decision

FOR EACH high_severity_risk (Impact = High OR Probability = High):
  USE AskUserQuestion:
    question: "Risk: {risk_description}. How should we handle this?"
    header: "Risk: {risk_id}"
    options:
      - label: "Mitigate (Recommended)"
        description: "Implement mitigation strategy: {mitigation_summary}"
      - label: "Accept"
        description: "Document and proceed, no mitigation"
      - label: "Avoid"
        description: "Change approach to eliminate risk"
      - label: "Transfer"
        description: "Assign ownership to another party/system"

  STORE risk_decision in:
    - State file: _state/solarch_config.json
    - Key: risk_decisions.{risk_id}
    - Value: { choice: "[selected]", timestamp: "[ISO]", source: "user" }

READ ProductSpecs materials:
  - ProductSpecs_X/00-overview/MASTER_DEVELOPMENT_PLAN.md (risk section if exists)
  - ProductSpecs_X/_registry/requirements.json (P2 items as potential debt)

GENERATE 10-risks/risks-technical-debt.md:
  USE Arc42Generator Section 11 template:

    Technical Risks:
      | ID | Risk | Probability | Impact | Mitigation | Owner |
      | TR-001 | Integration complexity | Medium | High | Staged rollout | Tech Lead |

    Risk Matrix:
      |          | Low Impact | Medium Impact | High Impact |
      | High Prob | TR-005 | TR-002 | - |
      | Med Prob | TR-004 | TR-001 | TR-003 |
      | Low Prob | - | TR-006 | - |

    Technical Debt:
      | ID | Debt Item | Reason | Impact | Remediation |
      | TD-001 | Manual config | Time constraints | Deployment friction | Automate CI/CD |

    Debt from ADR Tradeoffs:
      | ADR | Tradeoff | Debt Created | When to Address |
      | ADR-001 | Monolith chosen | Future scaling limits | When >100 users |

    Monitoring Plan:
      | Risk/Debt | Indicator | Threshold | Action |
      | TR-001 | Integration errors | > 5% | Investigate |

UPDATE _state/solarch_progress.json:
  phases.risks.status = "completed"
  phases.risks.completed_at = NOW()
  current_checkpoint = 9

RUN quality gate:
  python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 9 --dir {OUTPUT_PATH}/

DISPLAY checkpoint 9 summary
```

### Step 2: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-risks" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Output Files

### 10-risks/

| File | Content |
|------|---------|
| `risks-technical-debt.md` | Complete risks and debt documentation |

## Template Structure

```markdown
---
document_id: SA-10-RISKS
version: 1.0.0
arc42_section: 11
---

# Risks and Technical Debt

## 1. Technical Risks

### Risk Register

| ID | Risk | Category | Probability | Impact | Score | Status |
|----|------|----------|-------------|--------|-------|--------|
| TR-001 | Integration with legacy WMS may have undocumented behaviors | Integration | Medium | High | 6 | Active |
| TR-002 | Performance under peak load untested | Performance | Medium | Medium | 4 | Active |
| TR-003 | Real-time propagation latency | Integration | Low | High | 3 | Monitoring |
| TR-004 | Team unfamiliar with event-driven patterns | Knowledge | Medium | Low | 2 | Mitigating |
| TR-005 | Database migration complexity | Data | High | Low | 2 | Active |
| TR-006 | Third-party service availability | External | Low | Medium | 2 | Accepted |

### Risk Matrix

|            | Low Impact | Medium Impact | High Impact |
|------------|------------|---------------|-------------|
| **High**   | TR-005     | -             | -           |
| **Medium** | TR-004     | TR-002        | TR-001      |
| **Low**    | -          | TR-006        | TR-003      |

### Risk Details

#### TR-001: Integration with Legacy WMS

**Description**: The existing Warehouse Management System has limited documentation and may exhibit undocumented behaviors.

**Probability**: Medium (50%)
**Impact**: High (System malfunction, data inconsistency)

**Mitigation Strategy**:
1. Comprehensive integration testing phase
2. Staged rollout with fallback capability
3. Detailed logging at integration points
4. On-call support during initial deployment

**Owner**: Integration Lead
**Review Date**: Weekly during integration phase

**Traceability**:
- Pain Point: PP-1.1 (Current system reliability)
- ADR: ADR-006 (Event-driven communication chosen to decouple)

---

## 2. Technical Debt

### Debt Register

| ID | Debt Item | Type | Reason | Impact | Priority | Remediation |
|----|-----------|------|--------|--------|----------|-------------|
| TD-001 | Manual deployment configuration | Process | Time constraints | Deployment friction | P2 | Automate CI/CD |
| TD-002 | Incomplete API documentation | Documentation | Rapid development | Integration difficulty | P3 | OpenAPI generation |
| TD-003 | Test coverage below target | Quality | MVP scope | Regression risk | P1 | Add tests post-MVP |
| TD-004 | Hardcoded configuration values | Code | Quick fixes | Environment issues | P2 | Extract to config |

### Debt from ADR Tradeoffs

| ADR | Tradeoff Made | Debt Created | Trigger to Address |
|-----|---------------|--------------|-------------------|
| ADR-001 | Monolith over microservices | Future scaling limitations | User count > 1000 |
| ADR-002 | Single database | Performance ceiling | Response time > 1s |
| ADR-004 | Synchronous queries | Cascade failures possible | Integration count > 5 |
| ADR-008 | Simple caching | Cache invalidation complexity | Cache miss rate > 20% |

### Debt Burndown Plan

| Sprint | Focus Area | Items | Estimate |
|--------|------------|-------|----------|
| S1 | Testing | TD-003 | 8 pts |
| S2 | Automation | TD-001, TD-004 | 13 pts |
| S3 | Documentation | TD-002 | 5 pts |

---

## 3. Monitoring Plan

### Risk Monitoring

| Risk | Indicator | Threshold | Monitoring | Action |
|------|-----------|-----------|------------|--------|
| TR-001 | Integration error rate | > 5% | Grafana dashboard | Page on-call |
| TR-002 | P95 latency | > 500ms | APM | Scale resources |
| TR-003 | Propagation delay | > 2s | Event metrics | Investigate queue |
| TR-004 | Bug count in event code | > 3/sprint | Jira | Training session |

### Debt Monitoring

| Debt Item | Health Indicator | Current | Target | Trend |
|-----------|------------------|---------|--------|-------|
| TD-003 | Test coverage | 65% | 80% | Improving |
| TD-001 | Deployment time | 45min | 15min | Stable |
| TD-004 | Config errors/month | 3 | 0 | Decreasing |

---

## 4. Review Schedule

| Type | Frequency | Participants | Output |
|------|-----------|--------------|--------|
| Risk Review | Weekly | Tech Lead, PM | Updated register |
| Debt Review | Bi-weekly | Dev Team | Sprint planning input |
| Full Assessment | Quarterly | All stakeholders | Risk report |

## Traceability

| Risk/Debt | Pain Points | ADRs | Requirements |
|-----------|-------------|------|--------------|
| TR-001 | PP-1.1 | ADR-006 | REQ-009 |
| TR-002 | PP-2.1 | ADR-008 | REQ-011 |
| TD-001 | - | ADR-010 | - |
| TD-003 | PP-4.1 | - | REQ-Quality |
```

## Output Format

```
═══════════════════════════════════════════════════════════════
 CHECKPOINT 9: RISKS & TECHNICAL DEBT - COMPLETED
═══════════════════════════════════════════════════════════════

Generated Files:
└─ 10-risks/
    └─ risks-technical-debt.md ✅

Risk Assessment:
├─ Technical Risks: 6 identified
├─ High Impact: 2
├─ Active Mitigations: 4
└─ Accepted Risks: 2

Technical Debt:
├─ Debt Items: 4 logged
├─ ADR Tradeoff Debt: 4 noted
└─ Remediation Plan: Created

Quality Gate: ✅ PASSED

Next: /solarch-docs InventorySystem
═══════════════════════════════════════════════════════════════
```

## Checkpoint Validation

```bash
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 9 --dir SolArch_InventorySystem/
```

**Required for Checkpoint 9:**
- `10-risks/risks-technical-debt.md` exists with content

## Error Handling

| Error | Action |
|-------|--------|
| No ADR consequences | Generate generic integration risks |
| Risk section empty | Note as "No significant risks identified" |

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch-decisions` | Previous phase (Checkpoint 8) |
| `/solarch-docs` | Next phase (Checkpoint 10) |
