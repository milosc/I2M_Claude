---
paths:
  - "Implementation_*/**/*"
  - "**/*.test.{ts,tsx,js,jsx}"
  - "**/*.spec.{ts,tsx,js,jsx}"
---

# Process Integrity & TDD Rules

**Auto-loaded when working with**: Implementation outputs, test files

---

## Purpose

Enforces continuous monitoring by Process Integrity agents across all stages. Ensures traceability, checkpoint validation, and quality requirements.

**Agents:**
- `traceability-guardian` - Trace link validation (all stages)
- `state-watchdog` - Lock and session health (all stages)
- `checkpoint-auditor` - Gate validation (all stages)
- `playbook-enforcer` - TDD compliance (Stage 5 only)

---

## Traceability Requirements

### Stage-Specific Chains

| Stage | Chain | CRITICAL Violations |
|-------|-------|---------------------|
| Discovery | `client_materials → client_facts → pain_points → jtbd → user_types` | Pain point without client_fact_ref, JTBD without pain_point_ref |
| Prototype | `discovery → requirements → screens → components → code` | Screen without requirement_refs, Discovery screen not mapped |
| ProductSpecs | `prototype → modules → tests → nfrs → jira` | Module without screen_refs, P0 requirement without module |
| SolArch | `productspecs → adrs → components → diagrams` | ADR without requirement_refs, Component without ADR |
| Implementation | `solarch → tasks → code → tests` | Task without module_ref, P0 requirement without task, Implementation without test |

### Implementation Tasks (Stage 5)

**MUST HAVE:**
- `module_ref`: MOD-XXX-XXX-NN
- `requirement_refs`: [REQ-NNN, ...]
- `code_files`: Implementation files list

**ON COMPLETION:**
- `test_files`: Test files list
- `output_verified`: true

---

## TDD Compliance (Stage 5 Only)

### RED-GREEN-REFACTOR Cycle

| Phase | Requirements | Commit Message |
|-------|-------------|----------------|
| RED | Test file exists before implementation, Test fails initially | `RED: Add failing test for {feature}` |
| GREEN | Minimal implementation to pass test | `GREEN: Implement {feature}` |
| REFACTOR | Clean up, no behavior changes | `REFACTOR: Clean up {feature}` |

**Validation:** playbook-enforcer checks git history, test timestamp < implementation timestamp

**Violations:** Implementation without test (CRITICAL, blocks CP6), Implementation before test (HIGH)

---

## Checkpoint Gate Requirements

### Blocking Gates

| Checkpoint | Requirements |
|------------|-------------|
| **CP1** (Validate Inputs) | ProductSpecs CP ≥ 8, SolArch CP ≥ 12, 100% P0 coverage, Required registries exist |
| **CP6** (Code Review) | CRITICAL findings = 0, HIGH ≤ 5 (with plan), Test coverage ≥ 80%, Security audit PASS, P0 tasks complete |
| **CP9** (Final Validation) | All tasks complete, Integration tests PASS, E2E tests PASS, Traceability 100%, Documentation complete |

**Non-blocking gates**: Warn on failures, allow transition, track technical debt

---

## Veto Protocol

### When Process Integrity Detects CRITICAL Violation:

1. **RECORD** in `_state/integrity_status.json`:
   ```json
   {
     "veto": {
       "active": true,
       "agent": "playbook-enforcer",
       "checkpoint": "CP6",
       "reason": "TDD violation: implementation without test",
       "violations": [...]
     }
   }
   ```

2. **NOTIFY** orchestrator immediately
3. **BLOCK** further task spawning
4. **REQUIRE** resolution: Fix → Re-validate → Clear veto

**Veto-capable agents**: traceability-guardian, playbook-enforcer, checkpoint-auditor

---

## Enforcement Points

### Task Claim
```
CHECK: Task has required traceability, No active veto
IF issues: BLOCK claim → REPORT → REQUIRE fix
```

### Task Completion
```
INVOKE: playbook-enforcer for TDD validation
CHECK: Git history, Test files exist/pass
UPDATE: Traceability with output files
IF violations: REVERT to in_progress → RECORD → REQUIRE compliance
```

### Phase Transition
```
INVOKE: checkpoint-auditor
CHECK: Active vetos, All integrity agents vote
BLOCKING gates (CP1/CP6/CP9): ALL must pass, ANY veto blocks
NON-BLOCKING gates: WARN but allow, TRACK technical debt
```

---

## Monitoring

### Commands

```bash
# Overall integrity status
python3 .claude/hooks/agent_coordinator.py --status

# Validate checkpoint
python3 .claude/hooks/implementation_quality_gates.py --validate-checkpoint <N>

# Check TDD compliance
python3 .claude/hooks/implementation_quality_gates.py --validate-tdd --task <T-ID>

# Validate traceability chains
python3 .claude/hooks/implementation_quality_gates.py --validate-traceability
```

### Automatic Monitoring

| Agent | Trigger | Frequency |
|-------|---------|-----------|
| traceability-guardian | Registry changes | On file change |
| state-watchdog | Timer | Every 30 seconds |
| checkpoint-auditor | Phase transition | On request |
| playbook-enforcer | Task completion | Per task |

---

## Integration with Agents

### Manual Invocation

```javascript
Task({
  subagent_type: "general-purpose",
  model: "haiku",  // Checklist-based validation
  description: "Validate traceability",
  prompt: `Agent: process-integrity-traceability-guardian
    Read: .claude/agents/process-integrity-traceability-guardian.md
    REGISTRIES: traceability/*.json
    OUTPUT: Validation report with violations`
})
```

**Available Agents:**
- `process-integrity-traceability-guardian` - Trace validation
- `process-integrity-playbook-enforcer` - TDD compliance
- `process-integrity-checkpoint-auditor` - Gate validation
- `process-integrity-state-watchdog` - Lock/session health

---

## State Files

| File | Purpose |
|------|---------|
| `_state/integrity_status.json` | Current integrity state, active vetos |
| `_state/agent_lock.json` | Current file locks |
| `_state/agent_sessions.json` | Active/completed sessions |

---

## Related

- **Agent Definitions**: `.claude/agents/process-integrity-*.md`
- **Quality Gates**: `.claude/hooks/implementation_quality_gates.py`
- **Traceability**: Traceability rules auto-load when working with stage outputs
- **Architecture**: `architecture/Process_Integrity_Architecture.md`
