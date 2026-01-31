---
description: Display global traceability registry status and health
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /traceability-status started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /traceability-status ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /traceability-status instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## Usage

```
/traceability-status              # Full status report
/traceability-status --quick      # Quick pass/fail check
/traceability-status --coverage   # Focus on coverage metrics
```

## Arguments

| Argument | Description |
|----------|-------------|
| `--quick` | Only show pass/fail status, skip detailed report |
| `--coverage` | Include coverage metrics from each registry |

## Procedure

### Step 1: Invoke Guard
   ```
   INVOKE Traceability_Guard
   CAPTURE validation_result
   ```

2. **Gather Metrics** (if not --quick)
   ```
   FOR EACH registry file:
     READ file
     EXTRACT:
       - items count
       - schema_version
       - updated_at
       - summary statistics (if present)
   ```

3. **Generate Report**

### Quick Mode (--quick)

```
✅ Traceability backbone: HEALTHY
   18/18 files present | Schema v1.0.0 | Last updated: 2025-12-23
```

Or:

```
❌ Traceability backbone: UNHEALTHY
   16/18 files present | 2 errors
   Run /traceability-init --repair
```

### Full Mode (default)

```
╔═══════════════════════════════════════════════════════════════╗
║                   TRACEABILITY STATUS                         ║
╠═══════════════════════════════════════════════════════════════╣
║  System: InventorySystem                                      ║
║  Status: ✅ HEALTHY                                           ║
║  Schema Version: 1.0.0                                        ║
║  Last Updated: 2025-12-23T07:35:00Z                          ║
╚═══════════════════════════════════════════════════════════════╝

📁 FILE STATUS
┌─────────────────────────────────────┬────────┬─────────┬──────────┐
│ File                                │ Status │ Items   │ Updated  │
├─────────────────────────────────────┼────────┼─────────┼──────────┤
│ client_facts_registry.json          │ ✅     │ 45      │ 12-22    │
│ pain_point_registry.json            │ ✅     │ 20      │ 12-22    │
│ jtbd_registry.json                  │ ✅     │ 35      │ 12-22    │
│ user_type_registry.json             │ ✅     │ 7       │ 12-21    │
│ requirements_registry.json          │ ✅     │ 12      │ 12-23    │
│ screen_registry.json                │ ✅     │ 18      │ 12-22    │
│ module_registry.json                │ ✅     │ 15      │ 12-23    │
│ component_registry.json             │ ✅     │ 15      │ 12-23    │
│ adr_registry.json                   │ ✅     │ 8       │ 12-23    │
│ epic_registry.json                  │ ✅     │ 12      │ 12-23    │
│ user_story_registry.json            │ ✅     │ 35      │ 12-23    │
│ test_case_registry.json             │ ✅     │ 53      │ 12-23    │
│ trace_links.json                    │ ✅     │ 89      │ 12-21    │
│ traceability_matrix_master.json     │ ✅     │ -       │ 12-23    │
└─────────────────────────────────────┴────────┴─────────┴──────────┘

📊 COVERAGE SUMMARY
┌──────────────────┬───────┬──────────┬──────────┐
│ Artifact         │ Total │ Covered  │ Coverage │
├──────────────────┼───────┼──────────┼──────────┤
│ Pain Points      │ 20    │ 18       │ 90%      │
│ JTBDs            │ 35    │ 32       │ 91%      │
│ Requirements     │ 12    │ 12       │ 100%     │
│ Screens          │ 18    │ 18       │ 100%     │
│ Modules          │ 15    │ 15       │ 100%     │
│ ADRs             │ 8     │ 8        │ 100%     │
└──────────────────┴───────┴──────────┴──────────┘

🔗 TRACEABILITY LINKS: 89 total
   - addresses: 35
   - implements: 42
   - derives: 12

📝 DOCUMENTATION STATUS
   - All 18 files have valid $documentation blocks
   - 0 schema warnings
   - 0 deprecated files

💡 SUGGESTIONS
   - 2 pain points are not addressed by any JTBD
   - Consider running /discovery to fill gaps
```

### Coverage Mode (--coverage)

```
📊 TRACEABILITY COVERAGE REPORT

Discovery Phase:
  Client Facts → Pain Points:     45 facts → 20 pain points (extraction complete)
  Pain Points → JTBDs:            18/20 covered (90%) ⚠️
  User Types defined:             7 personas

Prototype Phase:
  JTBDs → Requirements:           32/35 covered (91%)
  Requirements → Screens:         12/12 covered (100%) ✅
  Screen Specs generated:         18/18 (100%) ✅
  Screen Code generated:          18/18 (100%) ✅

ProductSpecs Phase:
  Screens → Modules:              18 screens → 15 modules
  Modules → Test Cases:           15/15 covered (100%) ✅
  User Stories:                   35 total (P0: 15, P1: 16, P2: 4)

SolutionArchitecture Phase:
  Pain Points → ADRs:             20/20 covered (100%) ✅
  Modules → Components:           15/15 covered (100%) ✅
  ADRs created:                   8 (Accepted: 8)

Overall Traceability:
  End-to-end coverage:            95%
  Orphan artifacts:               2 (PP-6.3, PP-7.1)
```

## Error States

If backbone is missing:
```
❌ Traceability backbone not initialized

The traceability/ folder does not exist or is empty.

Run: /traceability-init {SystemName}
```

If validation fails:
```
⚠️ Traceability backbone has issues

Missing files:
  - jtbd_registry.json

Schema errors:
  - pain_point_registry.json: Missing $documentation.purpose

Run: /traceability-init --repair
```


---

## Related

- `/traceability-init` - Initialize or repair backbone
- `Traceability_Guard` skill - Validation logic
