# Error Handling Patterns for Prototype Skills

> **CRITICAL**: All Prototype skills MUST follow these patterns to prevent loops.

---

## 🔴 ABSOLUTE RULE #1: NEVER LOOP

**When you see ANY of these errors, SKIP and CONTINUE:**

```
"file not found"
"ModuleNotFoundError"
"command not found"
"Exit code 1"
"Exit code 127"
"Timeout"
"Permission denied"
"Cannot read file"
"Parse error"
"Invalid JSON"
"Build failed"
```

**DO NOT:**
- ❌ Retry the same operation
- ❌ Try a different library
- ❌ Try pip install
- ❌ Ask user what to do
- ❌ Wait for user input
- ❌ Try alternative approaches

**DO:**
- ✅ Log: `⛔ SKIPPED: [item] - [reason]`
- ✅ Add to `_state/FAILURES_LOG.md`
- ✅ Continue to next skill/step
- ✅ Complete build with available data

---

## 🔴 ABSOLUTE RULE #2: One Attempt Per Item

```
TRY:
    result = process(item)
    IF success: log_success, CONTINUE
CATCH:
    log_failure to FAILURES_LOG.md
    CONTINUE  ← ALWAYS do this, no exceptions
```

---

## 🟢 Legitimate Blocks (OK to stop and ask)

These situations ARE valid reasons to stop:

| Situation | Why It's Valid |
|-----------|----------------|
| Missing discovery_summary.json | Cannot proceed without discovery |
| Missing requirements_registry.json | Screens need requirements |
| P0 coverage < 100% at QA | Blocking quality gate |
| Skill specifies "BLOCK:" | Designed stopping point |
| User explicitly says "pause" | User-initiated |

---

## Error Handling by Skill

### Prototype_ValidateDiscovery

| Error | Action |
|-------|--------|
| Discovery folder missing | BLOCK - ask for path |
| File read fails | Log skip, use available files |
| Parse error | Log skip, continue |
| Missing persona | Warn, can continue |
| Missing entity | Warn, can continue |

### Prototype_Requirements

| Error | Action |
|-------|--------|
| discovery_summary.json missing | BLOCK - run ValidateDiscovery |
| Parse error | Log skip, use discovery directly |

### Prototype_DataModel

| Error | Action |
|-------|--------|
| Missing input | Use entities from discovery_summary |
| Schema generation fails | Log skip, continue |
| Relationship error | Log skip, continue |

### Prototype_Components

| Error | Action |
|-------|--------|
| Design tokens missing | BLOCK - run DesignTokens |
| Component generation fails | Log skip, continue to next |
| Template error | Use minimal spec |

### Prototype_Screens

| Error | Action |
|-------|--------|
| Components missing | BLOCK - run Components |
| Screen generation fails | Log skip, continue to next |
| Layout error | Use default layout |

### Prototype_CodeGen

| Error | Action |
|-------|--------|
| Build fails | Log error, continue to QA |
| npm install fails | Log error, skip |
| TypeScript error | Log error, continue |
| Single file fails | Log skip, continue to next |

### Prototype_QA

| Error | Action |
|-------|--------|
| P0 < 100% | BLOCK - ask user for resolution |
| Test fails | Log failure in report |
| Screenshot fails | Log skip, continue |

---

## FAILURES_LOG.md Format

```markdown
# ⛔ Prototype Build Failures Log

**Build Started**: {timestamp}
**Discovery Source**: {path}

## Skipped Items

| Timestamp | Phase | Item | Reason | Impact |
|-----------|-------|------|--------|--------|
| 10:30:00 | ValidateDiscovery | workflows.md | File not found | No workflows extracted |
| 10:45:00 | DataModel | Interview.schema | Parse error | Using minimal schema |
| 11:00:00 | Components | data-table.md | Template error | Skipped component |

## Impact Summary

- **Critical**: 0 items (would block build)
- **Major**: 2 items (reduced functionality)
- **Minor**: 1 item (cosmetic impact)

## Recovery Recommendations

1. **workflows.md**: Create workflows document or add workflow data manually
2. **Interview.schema**: Review entity definition in discovery
3. **data-table.md**: Can be added post-build
```

---

## Progress.json Error Tracking

```json
{
  "phases": {
    "validate_discovery": {
      "status": "complete",
      "errors": [],
      "skipped": ["workflows.md"]
    },
    "data_model": {
      "status": "complete_with_warnings",
      "errors": ["Interview.schema parse failed"],
      "skipped": ["Interview.schema"]
    },
    "components": {
      "status": "complete",
      "errors": [],
      "skipped": ["data-table.md"],
      "generated": 42
    }
  }
}
```

---

## What "Continue" Means

When user says "continue", "skip", or "move on":

```
CORRECT:
  current_skill = components
  error_on = table.md
  user_says = "continue"
  action = process NEXT component (card.md)

WRONG:
  current_skill = components
  error_on = table.md
  user_says = "continue"
  action = retry table.md ← NEVER DO THIS
```

---

## Summary

```
┌─────────────────────────────────────────┐
│                                         │
│   ERROR OCCURS                          │
│        ↓                                │
│   LOG TO FAILURES_LOG.md                │
│        ↓                                │
│   CONTINUE TO NEXT ITEM                 │
│        ↓                                │
│   COMPLETE BUILD WITH AVAILABLE DATA    │
│                                         │
│   No retries. No alternatives.          │
│   No pip install. No asking.            │
│                                         │
└─────────────────────────────────────────┘
```

---

**Version**: 1.0
**Key Principle**: Never loop. Always continue.
