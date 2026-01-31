---
name: mutating-documentation-artifacts
description: Use when you need to execute physical updates to project documentation including versioning, registries, and integrity tests.
model: sonnet
allowed-tools: Read, Write, Edit, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill mutating-documentation-artifacts started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill mutating-documentation-artifacts ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill mutating-documentation-artifacts instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Mutate Documentation Artifacts

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: ChangeManager_Mutator
- **Version**: 1.1.0
- **Created**: 2024-12-16
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v1.1.0 (2025-12-19): Updated metadata for consistency
  - v1.0.0 (2024-12-16): Initial release

## Description
Executes the physical updates to the project documentation. Handles versioning syntax, registry updates, and integrity testing.

## Functions

### Function: InitializeLog(ExternalID, InternalID)
* **Action:**
    1.  Load `05_Product_Specifications_InventorySystem/_registry/change_log.json`.
    2.  Append new entry:
        ```json
        {
          "id": InternalID,
          "externalRef": ExternalID,
          "status": "INITIATED",
          "timestamp": [CurrentTime]
        }
        ```
    3.  Save file.

### Function: ExecuteCascade(ExternalID, ImpactMatrix)
* **Logic:** Iterate through the Impact Matrix in strict order:
    1.  **Strategic:** Update `ANALYSIS_SUMMARY.md` (if Strategy changed). Use `**[MOD ExternalID]**` syntax.
    2.  **Requirements:**
        * Update `requirements_registry.json`: Update text field and append ExternalID to `change_log` array.
    3.  **Screens:**
        * Read target `02-screens/*.md`.
        * Apply regex replacement or append text with `**[MOD ExternalID]**` tags.
    4.  **Tests:**
        * Load `test-cases.json`.
        * Mark impacted tests as `status: "DEPRECATED"` and add `deprecation_reason: ExternalID`.
        * Create NEW test entries with `status: "ACTIVE"` and `origin: ExternalID`.
    5.  **Master Matrix:**
        * Read `TRACEABILITY_MATRIX_MASTER.md`.
        * Update relevant rows (Cells: Stories, Screen, Tests).
        * Append new row if it's a new feature.

### Function: RunIntegrityTests(ExternalID)
* **Logic:**
    1.  **Test 1 (Registry Consistency):**
        * Verify `ExternalID` exists in `requirements_registry.json`.
        * Verify `ExternalID` exists in `change_log.json`.
    2.  **Test 2 (Master Matrix):**
        * Extract all chains from `traceability.json`.
        * Verify every chain ID exists in `TRACEABILITY_MATRIX_MASTER.md`.
    3.  **Test 3 (Orphan Check):**
        * Find all Requirements tagged with `ExternalID`.
        * Verify each has a link to an Active Screen AND an Active Test Case.
* **Output:** `IntegrityResult` (Pass/Fail, List of Errors).

### Function: GenerateArtifacts(InternalID, ImpactMatrix, Risks)
* **Action:**
    1.  Compile data into Markdown using the standard templates defined in the ICMP protocol.
    2.  Write `[InternalID]_Report.md` to `reports/`.
    3.  Write `PLAN_[InternalID].md` to `plans/`.
