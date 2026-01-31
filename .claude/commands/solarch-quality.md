---
description: Perform quality review of Solution Architecture documentation
argument-hint: None
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-quality started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-quality ended '{"stage": "solarch"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-quality instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for architecture decisions:

```bash
# Load Traceability rules (includes ADR ID format, building blocks)
/rules-traceability
```

## Description

This command generates quality requirements documentation, quality scenarios, and cross-cutting concerns including security, error handling, logging, and caching. This is Checkpoint 6 of the pipeline.

## Arguments

- `$ARGUMENTS` - Optional: `<SystemName>` (auto-detected from config if not provided)

## Usage

```bash
/solarch-quality InventorySystem
```

## Prerequisites

- Checkpoint 5 passed (`/solarch-runtime` completed)
- NFR specifications available from ProductSpecs

## Skills Used

Read BEFORE execution:
- `.claude/skills/SolutionArchitecture_Arc42Generator/SKILL.md`

## Execution Steps

### Step 1: Execute

```
LOAD _state/solarch_config.json
SYSTEM_NAME = config.system_name

READ ProductSpecs materials:
  - ProductSpecs_X/_registry/nfrs.json
  - ProductSpecs_X/02-api/NFR_SPECIFICATIONS.md
  - ProductSpecs_X/01-modules/MOD-*.md (RBAC, error handling)

READ Prototype materials:
  - Prototype_X/03-interactions/accessibility-spec.md

GENERATE 07-quality/quality-requirements.md:
  USE Arc42Generator Section 10 template:

    Quality Tree:
      Quality
      ├── Performance
      │   ├── Response Time
      │   └── Throughput
      ├── Security
      │   ├── Authentication
      │   └── Authorization
      ├── Usability
      │   └── Accessibility
      └── Reliability
          └── Availability

    Quality Scenarios:
      | ID | Category | Scenario | Stimulus | Response | Measure | Source |
      | QS-PERF-001 | Performance | Page load | User navigates | Page displays | < 2s | NFR-PERF-001 |

GENERATE 07-quality/testing-strategy.md:
  Testing pyramid:
    - Unit tests (80% coverage)
    - Integration tests (70% coverage)
    - E2E tests (critical paths)

  Testing approaches:
    - Component testing
    - API contract testing
    - Performance testing
    - Security testing
    - Accessibility testing

UPDATE 05-building-blocks/cross-cutting.md:
  IF NOT complete:
    ADD sections:
      - Error Handling patterns
      - Logging & Monitoring
      - Caching strategy
      - Validation layers

CREATE 09-decisions/ADR-008-caching-strategy.md:
  USE AdrGenerator template:
    - Cache layers (Browser, CDN, Application, Database)
    - Cache invalidation strategy
    - TTL policies

CREATE 09-decisions/ADR-009-observability.md:
  USE AdrGenerator template:
    - Logging standards
    - Metrics collection
    - Distributed tracing
    - Alerting strategy

UPDATE _registry/decisions.json:
  ADD ADR-008, ADR-009

UPDATE _state/solarch_progress.json:
  phases.quality.status = "completed"
  phases.quality.completed_at = NOW()
  current_checkpoint = 6

RUN quality gate:
  python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 6 --dir {OUTPUT_PATH}/

DISPLAY checkpoint 6 summary
```

### Step 2: Log Command End (MANDATORY)

```bash
# Log command completion - MUST RUN LAST
  --command-name "/solarch-quality" \
  --stage "solarch" \
  --status "completed" \

echo "✅ Logged command completion"
```

## Output Files

### 07-quality/

| File | Content |
|------|---------|
| `quality-requirements.md` | Quality tree, scenarios, requirements |
| `testing-strategy.md` | Testing pyramid, approaches |

### 05-building-blocks/ (Update)

| File | Content |
|------|---------|
| `cross-cutting.md` | Error handling, logging, caching, validation |

### 09-decisions/

| File | Content |
|------|---------|
| `ADR-008-caching-strategy.md` | Caching decisions |
| `ADR-009-observability.md` | Observability decisions |

## Template Examples

### Quality Requirements Structure

```markdown
---
document_id: SA-07-QUALITY
version: 1.0.0
arc42_section: 10
---

# Quality Requirements

## Quality Tree

```
Quality
├── Performance
│   ├── Response Time (< 500ms P95)
│   ├── Throughput (1000 req/s)
│   └── Resource Usage (< 70% CPU)
├── Security
│   ├── Authentication (JWT, MFA)
│   ├── Authorization (RBAC)
│   └── Audit (Complete trail)
├── Usability
│   ├── Accessibility (WCAG 2.1 AA)
│   └── Efficiency (< 3 clicks)
└── Reliability
    ├── Availability (99.5%)
    └── Recoverability (< 15min RTO)
```

## Quality Scenarios

### Performance Scenarios

| ID | Scenario | Stimulus | Response | Measure | Source |
|----|----------|----------|----------|---------|--------|
| QS-PERF-001 | Search response | User searches items | Results displayed | < 500ms | NFR-PERF-001 |
| QS-PERF-002 | Concurrent users | 100 users simultaneously | System responsive | < 1s avg | NFR-PERF-002 |

### Security Scenarios

| ID | Scenario | Stimulus | Response | Measure | Source |
|----|----------|----------|----------|---------|--------|
| QS-SEC-001 | Unauthorized access | Invalid token | Request rejected | 401 response | NFR-SEC-001 |
| QS-SEC-002 | Permission violation | User without role | Access denied | 403 response | NFR-SEC-002 |

### Accessibility Scenarios

| ID | Scenario | Stimulus | Response | Measure | Source |
|----|----------|----------|----------|---------|--------|
| QS-A11Y-001 | Screen reader | User navigates | Content announced | WCAG 2.1 AA | A11Y-001 |

## Traceability

| NFR | Quality Scenario | ADR |
|-----|------------------|-----|
| NFR-PERF-001 | QS-PERF-001 | ADR-008 |
| NFR-SEC-001 | QS-SEC-001 | ADR-007 |
```

### Cross-cutting Concepts Structure

```markdown
---
document_id: SA-05-CROSSCUT
version: 1.0.0
arc42_section: 8
---

# Cross-cutting Concepts

## Error Handling

### Error Categories

| Category | HTTP Status | User Message | Logging |
|----------|-------------|--------------|---------|
| Validation | 400 | Field-specific | Debug |
| Authentication | 401 | Generic | Warning |
| Authorization | 403 | Generic | Warning |
| Not Found | 404 | Resource-specific | Debug |
| Conflict | 409 | Action-specific | Info |
| Server Error | 500 | Generic | Error + Alert |

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "User-friendly message",
    "details": [...]
  },
  "timestamp": "ISO8601"
}
```

## Logging & Monitoring

### Log Levels

| Level | Usage | Example |
|-------|-------|---------|
| Debug | Development details | Query parameters |
| Info | Business events | Adjustment created |
| Warning | Recoverable issues | Retry attempted |
| Error | Failures | Connection lost |

### Structured Log Format

```json
{
  "timestamp": "ISO8601",
  "level": "info",
  "correlationId": "uuid",
  "userId": "user_id",
  "action": "adjustment.create",
  "message": "Adjustment created",
  "data": {...}
}
```

## Caching

See [ADR-008](../09-decisions/ADR-008-caching-strategy.md)

### Cache Layers

| Layer | Technology | TTL | Invalidation |
|-------|------------|-----|--------------|
| Browser | HTTP Cache | 1h | Cache-Control |
| Application | Redis | 5m | Event-based |
| Database | Query Cache | 1m | Write-through |

## Validation

### Validation Layers

| Layer | Type | Implementation |
|-------|------|----------------|
| Client | Immediate feedback | Form validation |
| API | Request validation | FluentValidation |
| Domain | Business rules | Domain services |
| Database | Integrity | Constraints |
```

## Output Format

```
═══════════════════════════════════════════════════════════════
 CHECKPOINT 6: QUALITY & CROSS-CUTTING - COMPLETED
═══════════════════════════════════════════════════════════════

Generated Files:
├─ 07-quality/
│   ├─ quality-requirements.md ✅
│   └─ testing-strategy.md ✅
├─ 05-building-blocks/
│   └─ cross-cutting.md ✅ (updated)
└─ 09-decisions/
    ├─ ADR-008-caching-strategy.md ✅
    └─ ADR-009-observability.md ✅

Quality Documentation:
├─ Quality Scenarios: 12 documented
├─ NFRs Mapped: 15
└─ Cross-cutting Concepts: 4 sections

ADRs Registered: 7 total (2 new)

Quality Gate: ✅ PASSED

Next: /solarch-deploy InventorySystem
═══════════════════════════════════════════════════════════════
```

## Checkpoint Validation

```bash
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 6 --dir SolArch_InventorySystem/
```

**Required for Checkpoint 6:**
- `07-quality/quality-requirements.md` exists with content
- `06-runtime/security-architecture.md` exists with content
- `05-building-blocks/cross-cutting.md` exists with content

## Error Handling

| Error | Action |
|-------|--------|
| NFRs missing | Generate generic quality scenarios |
| Accessibility spec missing | Use WCAG defaults |

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch-runtime` | Previous phase (Checkpoint 5) |
| `/solarch-deploy` | Next phase (Checkpoint 7) |
