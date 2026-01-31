---
name: scanning-documentation-impact
description: Use when you need to perform bidirectional graph traversal on project registries and files to identify dependencies and risks of changes.
model: sonnet
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill scanning-documentation-impact started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill scanning-documentation-impact ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill scanning-documentation-impact instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Scan Documentation Impact

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: ChangeManager_Scanner
- **Version**: 1.1.0
- **Created**: 2024-12-16
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v1.1.0 (2025-12-19): Updated metadata for consistency
  - v1.0.0 (2024-12-16): Initial release

## Description
Performs bidirectional graph traversal on the project's JSON registries and Markdown files to identify dependencies, conflicts, and risks associated with a proposed change.

## Functions

### Function: ScanUpstream(Anchors)
* **Input:** List of Artifact IDs (e.g., `["US-001", "S-02"]`).
* **Logic:**
    1.  Read `traceability.json` and `discovery_summary.json`.
    2.  For each Anchor, find its parent nodes:
        * `US-XXX` -> `JTBD-X.X` -> `PP-XXX` -> `CF-XXX` (Client Fact).
    3.  **Conflict Check:**
        * Retrieve text of `CF-XXX`.
        * Compare text against the Proposed Change Summary using semantic analysis.
        * *Example:* If CF says "Keep it simple" and Change adds "Complex Workflow", flag as **CONFLICT**.
* **Output:** List of `StrategyConflicts` (ID, Description, Severity).

### Function: ScanDownstream(Anchors)
* **Input:** List of Artifact IDs.
* **Logic:**
    1.  Read `traceability.json`, `modules.json`, and `requirements_registry.json`.
    2.  For each Anchor, find its child nodes:
        * `US-XXX` -> `S-XX` (Screen) -> `MOD-XXX` (Module) -> `ADR-XXX` (Architecture).
        * `US-XXX` -> `TC-XXX` (Test Case).
    3.  **Impact Check:**
        * Check `04_Prototype/01-components/`: Do the required UI components exist?
        * Check `06_Solution_Architecture/09-decisions/`: Does the change violate a "Decided" ADR?
* **Output:** List of `TechnicalImpacts` (ID, Type, ActionRequired).
