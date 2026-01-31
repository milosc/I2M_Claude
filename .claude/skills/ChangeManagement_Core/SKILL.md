---
name: orchestrating-change-management
description: Use when you need to orchestrate the formal Integrated Change Management Protocol (ICMP) to manage the lifecycle of change requests.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill orchestrating-change-management started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill orchestrating-change-management ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill orchestrating-change-management instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Orchestrate Change Management

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: ChangeManagement_Core
- **Version**: 1.1.0
- **Created**: 2024-12-16
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v1.1.0 (2025-12-19): Updated metadata for consistency
  - v1.0.0 (2024-12-16): Initial release

## Description
Orchestrates the formal Integrated Change Management Protocol (ICMP) for the Inventory Management System. It manages the lifecycle of a change request from Handshake to Closure, ensuring strict traceability and integrity across the documentation graph.

## Usage
- **Trigger:** "Start a change request", "I need to change a requirement", "Update feature X", "Process CR"
- **Input:** Natural language description of the change + External ID (Jira/AzureDevOps/Asana).
- **Output:** Orchestrates the scan, proposal, mutation, and reporting phases.

## Dependencies
- `ChangeManager_Scanner` (for impact analysis)
- `ChangeManager_Mutator` (for execution)
- `Discovery_AnalyzeDesign` (for strategic context)
- `Prototype_Requirements` (for requirement context)

## Protocol: The 6-Phase Loop

### Phase 1: Handshake & Initiation
1.  **Prompt for External ID:**
    * **Instruction:** Ask the user: "Please provide the External Change Request ID (e.g., JIRA-123, ADO-4590) and a brief summary of the change."
    * **Validation:** Ensure `VAR_EXT_ID` is provided. If not, re-prompt.
2.  **Generate Internal ID:**
    * Format: `CR-[YYYYMMDD]_[VAR_EXT_ID]` (e.g., `CR-20251219_JIRA-8842`).
3.  **Initialize Log:**
    * **Action:** Call `ChangeManager_Mutator.InitializeLog(VAR_EXT_ID, VAR_INTERNAL_ID)`.

### Phase 2: Impact Scan (Analysis)
1.  **Identify Anchors:**
    * **Action:** Analyze the user's summary to find matching Artifact IDs (e.g., `US-001`, `S-02`, `MOD-INV-ADJUST`) in `discovery_summary.json` and `modules.json`.
2.  **Execute Tracing:**
    * **Action:** Call `ChangeManager_Scanner.ScanUpstream(Anchors)` to check for Strategic Conflicts (Pain Points, Client Facts).
    * **Action:** Call `ChangeManager_Scanner.ScanDownstream(Anchors)` to check for Technical Impact (Screens, Tests, ADRs).
3.  **Constraint Check:**
    * **Action:** Verify if any `ADR-XXX` or `CF-XXX` (Client Constraint) is flagged in the scan.

### Phase 3: Proposal & Risk Gate
1.  **Present Proposal:**
    * **Output:** Display a "Change Impact Matrix" to the user.
        * **Columns:** Artifact ID | Type | Impact Nature | Risk Level
        * **Conflict Warning:** Highlight any ADR violations in **BOLD RED**.
2.  **Await Confirmation:**
    * Ask: "Do you want to PROCEED with these changes, AMEND the request to avoid conflicts, or OVERRIDE the architecture (New ADR required)?"

### Phase 4: Execution (Cascade Update)
*Triggered only if User says "PROCEED" or "OVERRIDE"*
1.  **Action:** Call `ChangeManager_Mutator.ExecuteCascade(VAR_EXT_ID, Impact_Matrix)`.
    * This will update Registries, Screens, Specs, and Tests in the correct order.

### Phase 5: Integrity Verification
1.  **Action:** Call `ChangeManager_Mutator.RunIntegrityTests(VAR_EXT_ID)`.
    * **Test 1:** Registry Consistency.
    * **Test 2:** Master Matrix Alignment.
    * **Test 3:** Orphan Check.
2.  **Logic:**
    * **If Pass:** Proceed to Phase 6.
    * **If Fail:** Output the "Fix List" and wait for user to authorize corrections.

### Phase 6: Closure & Handoff
1.  **Generate Report:**
    * **Action:** Create `05_Product_Specifications_InventorySystem/change-requests/reports/[VAR_INTERNAL_ID]_Report.md`.
2.  **Generate Plan:**
    * **Action:** Create `05_Product_Specifications_InventorySystem/change-requests/plans/PLAN_[VAR_INTERNAL_ID].md`.
3.  **Final Output:**
    * Display a summary of actions taken and links to the generated files.
