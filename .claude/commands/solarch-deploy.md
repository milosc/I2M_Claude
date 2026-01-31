---
description: Generate deployment view from infrastructure requirements
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-deploy started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-deploy ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-deploy instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

This command generates the deployment view documenting infrastructure, environments, and operations guides including runbooks. This is Checkpoint 7 of the pipeline.

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` (auto-detected from config if not provided)

## Usage

```bash
/solarch-deploy InventorySystem
```

## Prerequisites

- Checkpoint 6 passed (`/solarch-quality` completed)
- Architecture decisions (ADRs) available

## Skills Used

Read BEFORE execution:
- `.claude/skills/SolutionArchitecture_Arc42Generator/SKILL.md`

## Execution Steps

### Step 1: Execute

```
LOAD _state/solarch_config.json
SYSTEM_NAME = config.system_name

READ existing ADRs:
  - 09-decisions/ADR-001-architecture-style.md
  - 09-decisions/ADR-002-technology-stack.md
  - 09-decisions/ADR-009-observability.md

READ ProductSpecs materials:
  - ProductSpecs_X/_registry/nfrs.json (availability, scalability)

GENERATE 08-deployment/deployment-view.md:
  USE Arc42Generator Section 07 template:

    Infrastructure Overview:
      - Reference C4 deployment diagram
      - Deployment strategy summary

    Infrastructure Elements:
      | Element | Technology | Purpose | Scaling |
      | Load Balancer | ALB/NGINX | Traffic distribution | Horizontal |
      | Application | Docker/K8s | App hosting | Auto-scale |
      | Database | PostgreSQL | Data storage | Read replicas |
      | Cache | Redis | Caching | Cluster |

    Environments:
      | Environment | Purpose | URL | Configuration |
      | Development | Local dev | localhost | Docker Compose |
      | Staging | Integration | staging.domain | K8s |
      | Production | Live | app.domain | K8s HA |

    Network Topology:
      - Security zones
      - Network boundaries
      - Access patterns

GENERATE 08-deployment/operations-guide.md:
  Operational Procedures:
    - Deployment process
    - Rollback procedures
    - Health checks

  Monitoring:
    - Key metrics
    - Alerting thresholds
    - Dashboard locations

  Incident Response:
    - Escalation paths
    - On-call procedures
    - Communication channels

CREATE runbooks directory:
  08-deployment/runbooks/

GENERATE 08-deployment/runbooks/README.md:
  Index of all runbooks

GENERATE standard runbooks:
  - RB-001-high-error-rate.md
  - RB-002-database-issues.md
  - RB-003-performance-degradation.md
  - RB-004-authentication-issues.md
  - RB-005-signalr-connectivity.md (if real-time)

CREATE 09-decisions/ADR-010-deployment-strategy.md:
  IF NOT exists:
    - Deployment approach (Blue/Green, Canary, Rolling)
    - Container strategy
    - Infrastructure as Code

UPDATE _registry/decisions.json:
  ADD ADR-010 if created

UPDATE _state/solarch_progress.json:
  phases.deploy.status = "completed"
  phases.deploy.completed_at = NOW()
  current_checkpoint = 7

RUN quality gate:
  python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 7 --dir {OUTPUT_PATH}/

DISPLAY checkpoint 7 summary
```

### Step 2: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-deploy" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Output Files

### 08-deployment/

| File | Content |
|------|---------|
| `deployment-view.md` | Infrastructure, environments, network |
| `operations-guide.md` | Procedures, monitoring, incidents |
| `runbooks/README.md` | Runbook index |
| `runbooks/RB-001-high-error-rate.md` | Error rate runbook |
| `runbooks/RB-002-database-issues.md` | Database runbook |
| `runbooks/RB-003-performance-degradation.md` | Performance runbook |
| `runbooks/RB-004-authentication-issues.md` | Auth runbook |
| `runbooks/RB-005-signalr-connectivity.md` | Real-time runbook |

### 09-decisions/

| File | Content |
|------|---------|
| `ADR-010-deployment-strategy.md` | Deployment strategy decisions |

## Template Examples

### Deployment View Structure

```markdown
---
document_id: SA-08-DEPLOY
version: 1.0.0
arc42_section: 7
---

# Deployment View

## Infrastructure Overview

See: [C4 Deployment Diagram](../diagrams/c4-deployment.mermaid)

### Deployment Strategy

- **Approach**: Blue/Green deployment
- **Orchestration**: Kubernetes
- **Container Registry**: AWS ECR / Azure ACR

## Infrastructure Elements

| Element | Technology | Purpose | Scaling |
|---------|------------|---------|---------|
| Load Balancer | AWS ALB | Traffic distribution | Managed |
| Web Application | Docker + K8s | Frontend hosting | HPA |
| API Application | Docker + K8s | Backend services | HPA |
| Database | PostgreSQL RDS | Data persistence | Read replicas |
| Cache | Redis ElastiCache | Session/data cache | Cluster mode |
| Message Queue | RabbitMQ | Event messaging | Cluster |

## Environments

| Environment | Purpose | URL | Configuration |
|-------------|---------|-----|---------------|
| Development | Local development | http://localhost:3000 | Docker Compose |
| Staging | Integration testing | https://staging.inventory.example.com | K8s Staging |
| Production | Live system | https://inventory.example.com | K8s Production |

### Environment Differences

| Aspect | Development | Staging | Production |
|--------|-------------|---------|------------|
| Database | Local PostgreSQL | RDS Single | RDS Multi-AZ |
| Cache | Local Redis | ElastiCache | ElastiCache Cluster |
| Replicas | 1 | 2 | 3+ |
| Logging | Console | CloudWatch | CloudWatch + Alerts |

## Network Topology

### Security Zones

| Zone | Contains | Access |
|------|----------|--------|
| Public | Load Balancer, CDN | Internet |
| Application | API servers, Web servers | LB only |
| Data | Database, Cache | App tier only |
| Management | CI/CD, Monitoring | VPN only |

## Traceability

- ADR: [ADR-010](../09-decisions/ADR-010-deployment-strategy.md)
- NFR: NFR-AVAIL-001 (99.5% uptime)
```

### Runbook Template

```markdown
---
document_id: RB-001
version: 1.0.0
created_at: 2025-12-22
severity: High
---

# RB-001: High Error Rate

## Overview

This runbook addresses scenarios where the API error rate exceeds normal thresholds.

## Symptoms

- Error rate > 5% in the last 5 minutes
- Increased 5xx responses
- Alert: "High Error Rate Detected"

## Diagnostic Steps

1. **Check Dashboard**
   - Open Grafana: [Link to dashboard]
   - Review error rate trend

2. **Check Logs**
   ```bash
   kubectl logs -l app=inventory-api --tail=100 | grep ERROR
   ```

3. **Check Dependencies**
   - Database connectivity
   - Redis connectivity
   - External API status

## Resolution Steps

### Scenario A: Database Issues

1. Check database connections
2. Review slow query log
3. Scale read replicas if needed

### Scenario B: Memory Pressure

1. Check pod memory usage
2. Scale horizontally if needed
3. Restart pods if OOM

### Scenario C: External Dependency

1. Enable circuit breaker
2. Use cached responses
3. Notify integration team

## Escalation

| Level | Contact | When |
|-------|---------|------|
| L1 | On-call engineer | Immediate |
| L2 | Senior engineer | > 15 min |
| L3 | Tech lead | > 30 min |

## Post-Incident

1. Document root cause
2. Create follow-up ticket
3. Update runbook if needed
```

## Output Format

```
═══════════════════════════════════════════════════════════════
 CHECKPOINT 7: DEPLOYMENT VIEW - COMPLETED
═══════════════════════════════════════════════════════════════

Generated Files:
├─ 08-deployment/
│   ├─ deployment-view.md ✅
│   ├─ operations-guide.md ✅
│   └─ runbooks/
│       ├─ README.md ✅
│       ├─ RB-001-high-error-rate.md ✅
│       ├─ RB-002-database-issues.md ✅
│       ├─ RB-003-performance-degradation.md ✅
│       ├─ RB-004-authentication-issues.md ✅
│       └─ RB-005-signalr-connectivity.md ✅
└─ 09-decisions/
    └─ ADR-010-deployment-strategy.md ✅

Deployment Documentation:
├─ Environments: 3 documented
├─ Infrastructure Elements: 6 documented
└─ Runbooks: 5 created

ADRs Registered: 8 total (1 new)

Quality Gate: ✅ PASSED

Next: /solarch-decisions InventorySystem
═══════════════════════════════════════════════════════════════
```

## Checkpoint Validation

```bash
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 7 --dir SolArch_InventorySystem/
```

**Required for Checkpoint 7:**
- `08-deployment/deployment-view.md` exists with content
- `08-deployment/operations-guide.md` exists with content

## Error Handling

| Error | Action |
|-------|--------|
| NFRs missing | Use standard availability targets |
| Technology stack unclear | Use generic K8s/Docker examples |

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch-quality` | Previous phase (Checkpoint 6) |
| `/solarch-decisions` | Next phase (Checkpoint 8) |
