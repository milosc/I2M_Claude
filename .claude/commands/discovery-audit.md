---
name: discovery-audit
description: Perform zero-hallucination audit on Discovery artifacts
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-audit started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-audit ended '{"stage": "discovery"}'
---


# /discovery-audit - Verify Fact Accuracy

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-audit instruction_start '{"stage": "discovery", "method": "instruction-based"}'
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
/discovery-audit <SystemName>
```

## Arguments

- `SystemName`: Name of the system (e.g., InventorySystem)

## Prerequisites

- `ClientAnalysis_<SystemName>/` folder exists.
- Phase 9 (Design Specs) has been attempted.

## Skills Used

- `.claude/skills/Discovery_FactAuditor/SKILL.md`
- `.claude/skills/traceability/Traceability_Guard.md`

## Procedure

1. **Initialize Audit**
   - ⏳ Starting fact-check audit for `<SystemName>`...
   - Invoke `Traceability_Guard` to ensure backbone is healthy.

2. **Execute Auditor**
   - INVOKE `Discovery_FactAuditor` with target directories.
   - Scan for `(Source: ...)` tags and `CF-` ID references.

3. **Handle Results**
   - IF hallucinations detected:
     - ❌ **Audit Failed**: Hallucinations found in artifacts.
     - Log issues to `HALUCINATIONS_LOG.md`.
     - **BLOCK PIPELINE**: Do not allow export to Prototype stage.
     - Present `CLIENT_CLARIFICATION_QUESTIONS.md` to the user.
   - ELSE:
     - ✅ **Audit Passed**: All claims verified against client materials.

4. **Log to History**
   - Execute `version_history_logger.py` to record the audit action.

## Output

- `AUDIT_REPORT.md`
- `CLIENT_CLARIFICATION_QUESTIONS.md`
- Updated `trace_matrix.json`

## Error Handling

- One Attempt, No Looping. If the auditor fails, stop and report.
