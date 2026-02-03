---
name: htec-sdd-changerequest
description: Process change requests using Kaizen PDCA and Reflexion loop
argument-hint: <change-description>
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion, Skill
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-changerequest started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-sdd-changerequest ended '{"stage": "utility"}'
---

# /htec-sdd-changerequest

**Version**: 2.0.0 (Reflexion-Enhanced)
**Stage**: Implementation
**Feedback ID Format**: CR-{SystemName}-NNN

## Philosophy

> **"Fix the system, not just the symptom"** - Toyota Production System

This command integrates four powerful methodologies:

1. **Kaizen**: Root cause analysis (5 Whys, Fishbone, A3) before ANY fix
2. **PDCA**: Plan → Do → Check → Act for iterative improvement
3. **Reflexion**: Self-refinement loops with critical thinking
4. **TDD**: Test-Driven Development (Red → Green → Refactor)

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "implementation"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /htec-sdd-changerequest instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Implementation stage rules:

```bash
# Load TDD and quality gate rules (path-specific auto-load if working with Implementation_*)
/rules-process-integrity

# Load multi-agent coordination rules (if spawning agents)
/rules-agent-coordination

# Load Traceability rules for task IDs
/rules-traceability
```

## Usage

```bash
/htec-sdd-changerequest <SystemName> [OPTIONS]

# OPTIONS:
#   --type=bug|improvement|feedback   # Change request type (default: auto-detect)
#   --id=CR-NNN                       # Resume existing change request
#   --status                          # Show current CR status
#   --list                            # List all CRs for system
```

## Arguments

- `SystemName`: Name of the system (e.g., InventorySystem)
- `--type`: Change request type (default: auto-detect)
- `--id`: Resume existing change request (e.g., CR-INV-042)
- `--status`: Show status of current/specified CR
- `--list`: List all CRs with status summary

## 8-Phase Workflow Overview

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                    CHANGE REQUEST WORKFLOW (8 PHASES)                          │
├───────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  PHASE 1: Input Collection & Triage                                           │
│           ├─ Gather change request details                                    │
│           ├─ Classify type (Bug/Improvement/Feedback)                         │
│           ├─ Assess severity & complexity                                     │
│           └─ Determine analysis method (Quick/5 Whys/Fishbone/A3)            │
│                                                                                │
│  PHASE 2: Impact Analysis with Reflexion  ← KAIZEN + REFLEXION               │
│           ├─ Root cause analysis (5 Whys/Fishbone/A3)                        │
│           ├─ Trace impact through 6-layer architecture                        │
│           ├─ Identify affected artifacts (T-NNN → Code → Tests)              │
│           ├─ Reflexion: Critical self-assessment                              │
│           └─ Generate impact_analysis.md with confidence scoring              │
│                                                                                │
│  PHASE 3: Session Registration                                                │
│           ├─ Create CR-XXX-NNN ID                                             │
│           ├─ Initialize session folder                                        │
│           ├─ Register in change_request_registry.json                         │
│           └─ Create CHANGE_REQUEST.md                                         │
│                                                                                │
│  PHASE 4: Approval Gate  ← USER INTERACTION                                   │
│           ├─ Present hierarchical impact chains with before/after             │
│           ├─ Show 6-layer impact summary                                      │
│           ├─ Display reflexion confidence score                               │
│           ├─ AskUserQuestion: Proceed? / Need More Info / Reject             │
│           └─ Handle user decision                                             │
│                                                                                │
│  PHASE 5: Implementation Planning with Reflexion  ← PDCA PLAN + REFLEXION    │
│           ├─ Generate detailed implementation plan                            │
│           ├─ Define TDD tasks (Red → Green → Refactor)                       │
│           ├─ Specify success criteria (measurable)                            │
│           ├─ Plan rollback strategy                                           │
│           ├─ Reflexion: Validate plan completeness                            │
│           └─ Generate IMPLEMENTATION_PLAN.md                                  │
│                                                                                │
│  PHASE 6: Implementation Execution  ← TDD + PDCA DO                           │
│           ├─ Execute TDD cycle for each task                                  │
│           │  ├─ RED: Write failing test                                       │
│           │  ├─ GREEN: Implement minimal fix                                  │
│           │  ├─ REFACTOR: Clean up                                            │
│           │  └─ VERIFY: Run test suite                                        │
│           ├─ Log each step to IMPLEMENTATION_LOG.md                           │
│           ├─ Track TDD compliance                                             │
│           └─ Build verification (npm run build)                               │
│                                                                                │
│  PHASE 7: Validation with Reflexion  ← PDCA CHECK + REFLEXION                │
│           ├─ Measure results vs. success criteria                             │
│           ├─ Validate hypothesis (PDCA Check)                                 │
│           ├─ Regression testing                                               │
│           ├─ Manual verification                                              │
│           ├─ Multi-perspective critique (Requirements/Arch/Quality)           │
│           ├─ Reflexion: Self-assessment (completeness/quality/correctness)    │
│           ├─ Consensus scoring (0-10, PASS ≥ 7.0)                            │
│           └─ Generate VALIDATION_REPORT.md                                    │
│                                                                                │
│  PHASE 8: Completion & Documentation  ← PDCA ACT + MEMORIZE                  │
│           ├─ PDCA ACT: Standardize if successful, iterate if not             │
│           ├─ MEMORIZE: Harvest insights → Update CLAUDE.md                   │
│           ├─ Update registries (task_registry.json, traceability)            │
│           ├─ Generate SUMMARY.md                                              │
│           ├─ Mark CR as completed                                             │
│           └─ Log completion                                                   │
│                                                                                │
└───────────────────────────────────────────────────────────────────────────────┘
```

## 6-Layer Implementation Architecture

The command validates impact across 6 architectural layers:

```
┌──────────────────────────────────────────────────────────────────┐
│                   6-LAYER ARCHITECTURE                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  LAYER 1: Discovery/Prototype Sources                            │
│           ├─ Requirements (REQ-XXX)                              │
│           ├─ Screens (SCR-XXX)                                   │
│           ├─ JTBD (JTBD-X.X)                                     │
│           └─ Pain Points (PP-X.X)                                │
│                                                                   │
│  LAYER 2: Tasks (Implementation)                                 │
│           ├─ T-NNN definitions                                   │
│           ├─ Task status tracking                                │
│           └─ Task dependencies                                   │
│                                                                   │
│  LAYER 3: Code (Implementation Files)                            │
│           ├─ src/ implementation files                           │
│           ├─ Components, hooks, utils                            │
│           └─ Configuration files                                 │
│                                                                   │
│  LAYER 4: Tests (Verification)                                   │
│           ├─ Unit tests (*.test.ts)                              │
│           ├─ Integration tests                                   │
│           └─ E2E tests (if applicable)                           │
│                                                                   │
│  LAYER 5: Registries (Metadata)                                  │
│           ├─ task_registry.json                                  │
│           ├─ traceability registers                              │
│           └─ change_request_registry.json                        │
│                                                                   │
│  LAYER 6: Documentation (Knowledge)                              │
│           ├─ CLAUDE.md learnings                                 │
│           ├─ Implementation docs                                 │
│           └─ README files                                        │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Kaizen Analysis Methods

This command uses four analysis methods based on severity and complexity:

| Method | When to Use | Duration | Depth |
|--------|-------------|----------|-------|
| **Quick Check** | Simple, low-risk changes | 10-15 min | Shallow |
| **5 Whys** | Standard complexity | 30-60 min | Medium |
| **Fishbone** | Multi-factor issues | 60-90 min | Deep |
| **A3 Full** | Critical issues | 2-4 hours | Comprehensive |

### Triage Decision Matrix

```
Severity + Complexity → Analysis Method

| Impact | Urgency | Complexity | Severity  | Analysis Method |
|--------|---------|------------|-----------|-----------------|
| High   | High    | COMPLEX    | CRITICAL  | A3_FULL         |
| High   | High    | MODERATE   | CRITICAL  | FIVE_WHYS       |
| High   | Low     | COMPLEX    | HIGH      | FISHBONE        |
| High   | Low     | MODERATE   | HIGH      | FIVE_WHYS       |
| Low    | High    | SIMPLE     | MEDIUM    | FIVE_WHYS       |
| Low    | Low     | SIMPLE     | LOW       | QUICK_CHECK     |
```

## Procedure

---

### PHASE 1: Input Collection & Triage

**Objective**: Gather change request details and determine analysis approach.

#### Step 1.1: Detect Execution Mode

```bash
CHECK arguments:

IF --status flag:
    READ Implementation_{SYSTEM_NAME}/change-requests/change_request_registry.json

    IF --id provided:
        FIND CR-{id} entry
        DISPLAY:
            - Title, Type, Severity
            - Status (registered/planned/implementing/validating/completed)
            - Created date, Completed date (if done)
            - Root cause summary
            - Files changed count
            - Current phase (if in progress)
        EXIT
    ELSE:
        # Show latest CR status
        FIND most recent CR
        DISPLAY status as above
        EXIT

IF --list flag:
    READ change_request_registry.json
    DISPLAY table:
        | ID | Title | Type | Severity | Status | Created | Completed |

    CALCULATE summary:
        - Total CRs: {count}
        - By Type: Bug ({N}), Improvement ({M}), Feedback ({K})
        - By Status: Completed ({X}), In Progress ({Y}), Failed ({Z})
        - Average duration: {duration}
    EXIT

IF --id=CR-XXX-NNN:
    MODE = "RESUME"
    LOAD existing session from Implementation_{SYSTEM_NAME}/change-requests/{date}_CR-{NNN}/
    READ current phase from registry
    SKIP to that phase
    EXIT to appropriate phase

ELSE:
    MODE = "NEW"
    CONTINUE to Step 1.2
```

#### Step 1.2: Collect Change Request Details

```bash
IF user provided description as argument:
    description = <argument>
ELSE:
    AskUserQuestion:
        question: "Please provide details about the change request. What needs to be fixed or improved?"
        header: "CR Details"
        options: [
            {
                label: "Bug Report (Recommended)",
                description: "Something is broken or not working as expected. Requires reproduction steps and root cause analysis."
            },
            {
                label: "Improvement",
                description: "Enhancement to existing functionality. Requires impact assessment and planning."
            },
            {
                label: "Stakeholder Feedback",
                description: "Change requested by stakeholder. Requires traceability back to requirements."
            }
        ]

    description = user_input["answer"]
    type_hint = user_input["selected_option"]

COLLECT required information:
    - Description: {what happened / what's needed}
    - Reporter context: {who reported, when, where}

    IF type == "Bug":
        - Reproduction steps: {step-by-step}
        - Expected behavior: {what should happen}
        - Actual behavior: {what actually happens}
        - Error messages / logs: {evidence}
        - Screenshots: {if available}

    IF type == "Improvement":
        - Current behavior: {how it works now}
        - Desired behavior: {how it should work}
        - User story / justification: {why this matters}
        - Acceptance criteria: {how to verify success}

    IF type == "Feedback":
        - Stakeholder: {who provided feedback}
        - Original requirement: {REQ-XXX or JTBD-X.X}
        - Feedback content: {what needs to change}
        - Priority: {urgency}
```

#### Step 1.3: Classify Type

```bash
IF user explicitly specified type:
    cr_type = <specified_type>
ELSE:
    ANALYZE description using keywords:
        - "broken", "error", "crash", "doesn't work" → Bug
        - "should", "could", "improve", "enhance" → Improvement
        - "client said", "stakeholder", "feedback" → Feedback

    IF ambiguous:
        AskUserQuestion:
            question: "What type of change request is this?"
            header: "CR Type"
            multiSelect: false
            options: [
                {
                    label: "Bug - Something is broken",
                    description: "Requires reproduction, debugging, and root cause analysis."
                },
                {
                    label: "Improvement - Enhancement",
                    description: "Adding functionality or improving existing behavior."
                },
                {
                    label: "Feedback - Stakeholder Request",
                    description: "Change requested by client/stakeholder with traceability."
                }
            ]

        cr_type = user_answer
```

#### Step 1.4: Assess Severity & Complexity

```bash
ASSESS severity using Kaizen priority matrix:

AskUserQuestion:
    question: "What is the impact and urgency of this change?"
    header: "Severity"
    multiSelect: false
    options: [
        {
            label: "CRITICAL - High Impact, High Urgency",
            description: "Production down, data loss, security breach. Immediate response (hours)."
        },
        {
            label: "HIGH - High Impact, Low Urgency",
            description: "Major functionality broken, no workaround. Fix this sprint."
        },
        {
            label: "MEDIUM - Low Impact, High Urgency",
            description: "Minor issue but blocking workflow. Fix next sprint."
        },
        {
            label: "LOW - Low Impact, Low Urgency",
            description: "Nice to have, cosmetic issue. Backlog."
        }
    ]

severity = user_answer

ASSESS complexity by scanning codebase:

SEARCH for affected files:
    IF cr_type == "Bug":
        # Find files related to error message/component
        SEARCH error message in logs
        SEARCH component name in src/
        COUNT affected files

    IF cr_type == "Improvement":
        # Find files related to feature area
        SEARCH feature keywords in src/
        COUNT related components

    IF affected_files == 1:
        complexity = "SIMPLE"
    ELIF affected_files <= 5:
        complexity = "MODERATE"
    ELSE:
        complexity = "COMPLEX"

DISPLAY:
    ┌────────────────────────────────────────┐
    │         TRIAGE ASSESSMENT              │
    ├────────────────────────────────────────┤
    │  Type:       {cr_type}                 │
    │  Severity:   {severity}                │
    │  Complexity: {complexity}              │
    │  Affected:   {affected_files} files    │
    └────────────────────────────────────────┘
```

#### Step 1.5: Determine Analysis Method

```bash
DETERMINE analysis depth based on triage:

IF severity == "CRITICAL" OR complexity == "COMPLEX":
    IF cr_type == "Bug":
        analysis_method = "A3_FULL"  # Comprehensive
    ELSE:
        analysis_method = "FISHBONE"  # Multi-factor

ELIF severity == "HIGH" OR complexity == "MODERATE":
    analysis_method = "FIVE_WHYS"  # Standard

ELSE:
    analysis_method = "QUICK_CHECK"  # Fast path

DISPLAY:
    📊 Analysis Method: {analysis_method}
    ⏱️  Expected Duration: {duration_estimate}

OUTPUT Phase 1:
    - cr_type, severity, complexity
    - analysis_method
    - affected_files list
```

---

### PHASE 2: Impact Analysis with Reflexion (KAIZEN + REFLEXION)

**Objective**: Perform root cause analysis and trace impact through 6 layers using Kaizen methods and reflexion.

**Reflexion Integration**: This phase uses reflexion for critical self-assessment of the analysis.

#### Step 2.1: Root Cause Analysis (KAIZEN)

```bash
EXECUTE analysis based on selected method:

═══════════════════════════════════════════════════════════════
              KAIZEN ROOT CAUSE ANALYSIS
═══════════════════════════════════════════════════════════════

METHOD 1: QUICK CHECK (Simple changes)
──────────────────────────────────────

FOR simple, low-risk changes:

    REPRODUCE the issue:
        - Follow reproduction steps (if bug)
        - Verify current behavior (if improvement)
        - Confirm observation matches description

    IDENTIFY immediate cause:
        - Which file/function is involved?
        - What line of code causes the behavior?
        - What's the obvious fix?

    CONFIRM fix location:
        - Where should the change go?
        - Are there other places needing update?
        - Any dependencies to check?

    DOCUMENT briefly:
        - Immediate cause: {description}
        - Fix location: {file}:{line}
        - Confidence: HIGH (simple case)

Duration: 10-15 minutes

─────────────────────────────────────────────────────────────

METHOD 2: FIVE WHYS (Standard analysis)
──────────────────────────────────────

FOR moderate complexity:

    Problem Statement: {observable symptom}

    Why 1: {immediate technical cause}
           "What code/condition triggered this?"
           → {answer}

    Why 2: {deeper cause}
           "Why did that code behave that way?"
           → {answer}

    Why 3: {design cause}
           "Why was it written/configured that way?"
           → {answer}

    Why 4: {process cause}
           "Why wasn't this caught earlier?"
           → {answer}

    Why 5: {systemic cause}
           "What systemic issue allowed this?"
           → {answer}

    Root Cause: {fundamental issue, usually process/design}

BRANCHING RULES:
    - If multiple causes emerge at any Why, explore each branch
    - Stop when you reach process/systemic issues (not always 5)
    - If "human error" appears, ask WHY error was possible
    - Document each branch's root cause

EXAMPLE (Bug):
    Problem: "Barcode scanner times out on slow networks"

    Why 1: HTTP request times out after 5 seconds
    Why 2: No retry logic implemented
    Why 3: Initial design assumed fast local network
    Why 4: Network variability not considered in requirements
    Why 5: No performance testing on slow networks during QA

    Root Cause: Requirements didn't specify network resilience,
                and QA test plan lacked slow-network scenarios

Duration: 30-60 minutes

─────────────────────────────────────────────────────────────

METHOD 3: FISHBONE ANALYSIS (Complex, multi-factor)
──────────────────────────────────────────────────

FOR issues with multiple contributing factors:

    Problem (Effect): {specific symptom at "head"}

    PEOPLE (Who)
    ├─ {Knowledge gaps identified}
    ├─ {Communication issues}
    └─ {Training needs}

    PROCESS (How)
    ├─ {Workflow gaps}
    ├─ {Review failures}
    └─ {Missing standards}

    TECHNOLOGY (What)
    ├─ {Tool limitations}
    ├─ {Infrastructure issues}
    └─ {Dependency problems}

    ENVIRONMENT (Where)
    ├─ {Config differences prod/dev}
    ├─ {External factors}
    └─ {Resource constraints}

    METHODS (Why)
    ├─ {Architectural issues}
    ├─ {Pattern violations}
    └─ {Design decisions}

    MATERIALS (Inputs)
    ├─ {Data quality issues}
    ├─ {Third-party API problems}
    └─ {Input validation gaps}

ANALYZE each bone:
    - Identify 2-3 contributing factors per category
    - Rank by impact (High/Medium/Low)
    - Mark primary vs. secondary causes

PRIMARY ROOT CAUSES:
    - {Cause 1 from category X}
    - {Cause 2 from category Y}

SECONDARY CONTRIBUTING FACTORS:
    - {Factor 1}
    - {Factor 2}

EXAMPLE (Bug):
    Problem: "User data corruption in high-concurrency scenarios"

    TECHNOLOGY:
    ├─ No database transaction isolation
    ├─ Race condition in state updates
    └─ No optimistic locking

    PROCESS:
    ├─ Code review didn't catch concurrency issue
    ├─ No concurrent user load testing
    └─ Missing concurrency design checklist

    PRIMARY ROOT CAUSES:
    - Missing database transactions (TECHNOLOGY)
    - No concurrency testing in QA process (PROCESS)

Duration: 60-90 minutes

─────────────────────────────────────────────────────────────

METHOD 4: A3 FULL ANALYSIS (Critical issues)
────────────────────────────────────────────

FOR critical or complex issues requiring comprehensive documentation:

    ═══════════════════════════════════════════════════
                  A3 PROBLEM ANALYSIS
    ═══════════════════════════════════════════════════

    TITLE: {Concise, descriptive title}
    OWNER: {Responsible party / team}
    DATE: {YYYY-MM-DD}
    CR-ID: CR-{SYSTEM}-{NNN}

    1. BACKGROUND
       • Why this matters (business impact)
       • Who is affected (users, teams, systems)
       • Urgency factors (deadlines, dependencies)
       • Context (how we got here)

    2. CURRENT CONDITION
       • What's happening (facts, not opinions)
       • Data and metrics (error rates, response times)
       • Reproduction evidence (logs, screenshots)
       • Scope (frequency, affected users, environments)

    3. GOAL/TARGET
       • Specific success criteria (measurable)
       • Measurable outcomes (numbers, percentages)
       • Timeline (when must this be fixed)
       • Acceptable vs. ideal outcomes

    4. ROOT CAUSE ANALYSIS
       [Use Five Whys OR Fishbone here - embed full analysis]

       Primary Root Cause(s):
       • {Root cause 1}
       • {Root cause 2}

       Contributing Factors:
       • {Factor 1}
       • {Factor 2}

    5. COUNTERMEASURES

       IMMEDIATE FIX (Hours):
       • {Quick patch to stop the bleeding}
       • {Workaround to unblock users}

       SHORT-TERM PREVENTION (Days):
       • {Fix the immediate root cause}
       • {Add monitoring/alerts}

       LONG-TERM SYSTEMIC FIX (Weeks):
       • {Address systemic issues}
       • {Process improvements}
       • {Prevent recurrence}

    6. IMPLEMENTATION PLAN

       Task 1: {Description}
               Owner: {Person}
               Duration: {Estimate}
               Dependencies: {List}

       Task 2: {Description}
               Owner: {Person}
               Duration: {Estimate}
               Dependencies: {List}

       Timeline:
       ├─ Week 1: {Milestones}
       ├─ Week 2: {Milestones}
       └─ Week 3: {Milestones}

    7. FOLLOW-UP

       Verification Method:
       • {How to verify fix works}
       • {Metrics to track}

       Monitoring Plan:
       • {What to monitor ongoing}
       • {Alert thresholds}

       Review Dates:
       • {1 week review}
       • {1 month review}
       • {Quarterly retrospective}

    ═══════════════════════════════════════════════════

Duration: 2-4 hours

═══════════════════════════════════════════════════════════════

SPECIAL: GEMBA WALK (For unfamiliar code)
─────────────────────────────────────────

IF you're analyzing code you're not familiar with:

    SCOPE: {Code area to explore}

    STEP 1: State Assumptions
    ASSUMPTIONS (what you think it does):
    • {Assumption 1}
    • {Assumption 2}
    • {Assumption 3}

    STEP 2: Read and Observe
    OBSERVATIONS (what it actually does):
    • Entry points: {functions, routes, hooks}
    • Actual data flow: {trace execution path}
    • Surprises: {differs from assumptions}
    • Hidden dependencies: {imports, external calls}

    STEP 3: Identify Gaps
    GAPS (reality vs. expectations):
    • Documentation vs. reality: {discrepancies}
    • Expected vs. actual behavior: {differences}
    • Missing pieces: {what's not there that should be}

    STEP 4: Document Findings
    • What I learned about this code
    • Key insights for analysis
    • Areas of uncertainty

═══════════════════════════════════════════════════════════════
```

#### Step 2.2: Trace Impact Through 6 Layers

```bash
TRACE impact through 6-layer architecture:

LAYER 1: Discovery/Prototype Sources
─────────────────────────────────────

READ traceability registers to find upstream sources:
    - Implementation_{SYSTEM}/traceability/implementation_traceability_register.json
    - ProductSpecs_{SYSTEM}/registry/traceability.json

IDENTIFY source requirements/JTBDs:
    IF change affects Task T-042:
        TRACE backwards: T-042 → REQ-015 → JTBD-2.1 → PP-1.1

        RECORD affected sources:
        {
            "PP-1.1": {
                "title": "Slow barcode scanning in low network conditions",
                "file": "ClientAnalysis_{SYSTEM}/01-pain-points/warehouse-operators.md",
                "change_type": "VALIDATE_STILL_APPLIES",
                "reason": "Fix addresses network resilience mentioned in pain point"
            },
            "JTBD-2.1": {
                "title": "Scan items efficiently in any network condition",
                "file": "ClientAnalysis_{SYSTEM}/03-jtbd/operational-efficiency.md",
                "change_type": "VERIFY_SUCCESS_CRITERIA",
                "reason": "Success criteria must reflect network resilience"
            },
            "REQ-015": {
                "title": "Barcode scanner network resilience",
                "file": "ProductSpecs_{SYSTEM}/registry/requirements.json",
                "change_type": "MARK_AS_ADDRESSED",
                "reason": "Requirement now fully implemented with retry logic"
            }
        }

LAYER 2: Tasks
──────────────

IDENTIFY affected task(s):
    - Which T-NNN is this change related to?
    - Is this fixing an incomplete task?
    - Does this create a new task?

    READ Implementation_{SYSTEM}/registry/task_registry.json

    SEARCH for affected task:
        - By task ID (if known)
        - By file path (which task owns affected files)
        - By description keywords

    EXAMPLE:
    {
        "T-042": {
            "title": "Implement barcode scanner hook",
            "status": "completed",
            "files_affected": [
                "src/hooks/use-barcode-scanner.ts"
            ],
            "change_type": "MODIFY",
            "reason": "Add retry logic for network timeouts"
        }
    }

LAYER 3: Code (Implementation Files)
─────────────────────────────────────

SCAN affected implementation files:

    IF analysis identified specific file:
        READ file
        IDENTIFY affected functions/classes

    IF analysis identified component area:
        GLOB "Implementation_{SYSTEM}/src/**/{pattern}*"
        READ matching files
        IDENTIFY functions that need changes

    FOR each affected file:
        EXTRACT:
            - File path
            - Functions/classes affected
            - Current implementation (code snippet)
            - Proposed change (what needs to change)
            - Line range (start:end)

    EXAMPLE:
    {
        "src/hooks/use-barcode-scanner.ts": {
            "functions_affected": ["useBarcodeScanner", "fetchBarcodeData"],
            "change_type": "MODIFY",
            "line_range": "45-67",
            "before_snippet": `
                const response = await fetch(apiUrl, {
                  method: 'POST',
                  body: JSON.stringify({ barcode }),
                  signal: AbortSignal.timeout(5000)
                });
            `,
            "after_snippet": `
                const response = await fetch(apiUrl, {
                  method: 'POST',
                  body: JSON.stringify({ barcode }),
                  signal: AbortSignal.timeout(5000)
                });

                // Retry logic for network timeouts
                if (!response.ok && response.status === 0) {
                  // Network timeout - retry with exponential backoff
                  return retryWithBackoff(() =>
                    fetch(apiUrl, {...}),
                    { maxRetries: 3, baseDelay: 1000 }
                  );
                }
            `,
            "reasoning": "Add retry logic with exponential backoff for network timeouts"
        }
    }

LAYER 4: Tests
──────────────

IDENTIFY affected test files:

    FOR each affected code file:
        # Find corresponding test file
        IF src/hooks/use-barcode-scanner.ts affected:
            LOOK FOR:
                - tests/unit/use-barcode-scanner.test.ts
                - src/hooks/__tests__/use-barcode-scanner.test.ts

        IF test exists:
            change_type = "MODIFY"
            READ test file
            IDENTIFY test cases that need updating
        ELSE:
            change_type = "CREATE"
            PLAN new test file

    PLAN new test cases:
        - Test for retry logic
        - Test for exponential backoff
        - Test for max retries exceeded
        - Test for success after retry

    EXAMPLE:
    {
        "tests/unit/use-barcode-scanner.test.ts": {
            "change_type": "MODIFY",
            "new_test_cases": [
                {
                    "name": "should retry on network timeout",
                    "description": "Verify retry logic triggers on network timeout (status 0)",
                    "test_type": "unit",
                    "red_phase": "Write test that expects retry on timeout",
                    "green_phase": "Implement retry logic to make test pass",
                    "refactor_phase": "Extract retry logic to utility function"
                },
                {
                    "name": "should use exponential backoff",
                    "description": "Verify retry delays follow exponential backoff pattern",
                    "test_type": "unit",
                    "red_phase": "Write test that verifies delay increases exponentially",
                    "green_phase": "Implement exponential backoff",
                    "refactor_phase": "None needed"
                },
                {
                    "name": "should stop after max retries",
                    "description": "Verify function gives up after 3 retries",
                    "test_type": "unit",
                    "red_phase": "Write test that expects failure after 3 retries",
                    "green_phase": "Implement max retry limit",
                    "refactor_phase": "Extract maxRetries to config"
                }
            ],
            "existing_tests_to_update": [
                "should fetch barcode data successfully"
            ]
        }
    }

LAYER 5: Registries
────────────────────

IDENTIFY registry updates needed:

    task_registry.json:
        - Update T-042 status if fixing incomplete task
        - Add new task entry if creating new work
        - Update files_affected list
        - Update test_coverage references

    traceability registers:
        - Update implementation_traceability_register.json
        - Add new trace entries for code → tests
        - Update task → requirement traces

    change_request_registry.json:
        - Will be updated in Phase 3 (Registration)

LAYER 6: Documentation
──────────────────────

IDENTIFY documentation updates needed:

    CLAUDE.md:
        - IF significant learning → add to "Implementation Learnings"
        - IF new pattern → document in "Code Quality Rules"
        - IF debugging insight → add to "Debugging Strategies"

    README files:
        - IF new functionality → update feature list
        - IF API change → update usage examples
        - IF dependency change → update installation steps

    Component _readme.md files:
        - IF component behavior changed → update inline docs
        - Follow _readme.md convention from .claude/rules/inline-docs.md
```

#### Step 2.3: Build Hierarchical Traceability Chains

```bash
BUILD hierarchical chains showing end-to-end impact:

IDENTIFY root artifacts (no incoming traces):
    - Usually Pain Points (PP-X.X) or Client Materials (CM-XXX)

IDENTIFY leaf artifacts (no outgoing traces):
    - Usually Code files or Test files

FOR each affected artifact:
    BUILD chain recursively:
        chain = []
        current = root_artifact

        WHILE current has outgoing traces:
            chain.append(current)
            next = get_next_in_chain(current)
            current = next

        chain.append(current)  # Add leaf

    STORE chain with full details

VISUALIZE chains as tree structure:

═══════════════════════════════════════════════════════════════
         HIERARCHICAL TRACEABILITY CHAINS AFFECTED
═══════════════════════════════════════════════════════════════

Chain 1: PP-1.1 → JTBD-2.1 → REQ-015 → T-042 → CODE → TESTS

├─ **PP-1.1**: "Slow barcode scanning in low network conditions"
│  └─ Change: VALIDATE_STILL_APPLIES
│     File: ClientAnalysis_{SYSTEM}/01-pain-points/warehouse-operators.md:23-28
│     Before:
│     ```markdown
│     **PP-1.1**: Warehouse operators experience slow barcode scanning,
│     especially in areas with poor WiFi signal. This causes delays during
│     peak hours.
│     ```
│     After: No change needed - fix addresses this pain point
│     Reasoning: Root cause analysis confirms this pain point is valid and
│                now being addressed with retry logic.
│
├─ **JTBD-2.1**: "Scan items efficiently in any network condition"
│  └─ Change: VERIFY_SUCCESS_CRITERIA
│     File: ClientAnalysis_{SYSTEM}/03-jtbd/operational-efficiency.md:45-52
│     Before:
│     ```yaml
│     success_criteria:
│       - "Scan completes within 2 seconds on average"
│       - "95% success rate"
│     ```
│     After:
│     ```yaml
│     success_criteria:
│       - "Scan completes within 2 seconds on average (with retries)"
│       - "95% success rate in good network conditions"
│       - "90% success rate in poor network conditions (with 3 retries)"
│     ```
│     Reasoning: Success criteria must account for retry behavior and
│                network variability.
│
├─ **REQ-015**: "Barcode scanner network resilience"
│  └─ Change: MARK_AS_ADDRESSED
│     File: ProductSpecs_{SYSTEM}/registry/requirements.json:145-167
│     Before:
│     ```json
│     "acceptance_criteria": [
│       "Barcode scanning works on stable network",
│       "Timeout after 5 seconds"
│     ]
│     ```
│     After:
│     ```json
│     "acceptance_criteria": [
│       "Barcode scanning works on stable network",
│       "Timeout after 5 seconds",
│       "Automatic retry with exponential backoff on network timeout",
│       "Maximum 3 retry attempts",
│       "User-visible loading indicator during retries"
│     ]
│     ```
│     Reasoning: Requirement now fully specifies retry behavior.
│
├─ **T-042**: "Implement barcode scanner hook"
│  └─ Change: MODIFY
│     File: Implementation_{SYSTEM}/registry/task_registry.json:89-112
│     Before:
│     ```json
│     "status": "completed",
│     "verification": "Tests passing, no retry logic"
│     ```
│     After:
│     ```json
│     "status": "modified_for_cr",
│     "verification": "Tests passing, retry logic added for network resilience",
│     "change_request_ref": "CR-{SYSTEM}-042"
│     ```
│     Reasoning: Task status updated to reflect CR-driven modification.
│
├─ **CODE**: src/hooks/use-barcode-scanner.ts
│  └─ Change: MODIFY - Add retry logic with exponential backoff
│     Line Range: 45-67
│     Before:
│     ```typescript
│     const response = await fetch(apiUrl, {
│       method: 'POST',
│       body: JSON.stringify({ barcode }),
│       signal: AbortSignal.timeout(5000)
│     });
│
│     if (!response.ok) {
│       throw new Error('Barcode fetch failed');
│     }
│     ```
│     After:
│     ```typescript
│     const response = await fetch(apiUrl, {
│       method: 'POST',
│       body: JSON.stringify({ barcode }),
│       signal: AbortSignal.timeout(5000)
│     });
│
│     // Retry logic for network timeouts
│     if (!response.ok && response.status === 0) {
│       // Network timeout - retry with exponential backoff
│       return retryWithBackoff(
│         () => fetch(apiUrl, {
│           method: 'POST',
│           body: JSON.stringify({ barcode }),
│           signal: AbortSignal.timeout(5000)
│         }),
│         { maxRetries: 3, baseDelay: 1000 }
│       );
│     }
│
│     if (!response.ok) {
│       throw new Error('Barcode fetch failed');
│     }
│     ```
│     Complexity: MODERATE (adds new utility function retryWithBackoff)
│
└─ **TESTS**: tests/unit/use-barcode-scanner.test.ts
   └─ Change: MODIFY - Add retry test cases
      New Test Cases: 3
      - "should retry on network timeout"
      - "should use exponential backoff"
      - "should stop after max retries"
      Existing Tests to Update: 1
      - "should fetch barcode data successfully" (add network mock)

═══════════════════════════════════════════════════════════════
```

#### Step 2.4: Generate 6-Layer Impact Summary

```bash
GROUP affected artifacts by layer:

CALCULATE counts:
    layer_1_count = count(PP-X.X, JTBD-X.X, REQ-XXX, SCR-XXX)
    layer_2_count = count(T-NNN)
    layer_3_count = count(src/ implementation files)
    layer_4_count = count(test files)
    layer_5_count = count(registry files)
    layer_6_count = count(documentation files)

CREATE summary table:

═══════════════════════════════════════════════════════════════
              6-LAYER IMPACT SUMMARY
═══════════════════════════════════════════════════════════════

| Layer | Artifacts Affected | Details |
|-------|-------------------|---------|
| 1. Discovery/Prototype | {X} | {PP-1.1, JTBD-2.1, REQ-015} |
| 2. Tasks | {Y} | {T-042} |
| 3. Code | {Z} | {src/hooks/use-barcode-scanner.ts} |
| 4. Tests | {T} | {tests/unit/use-barcode-scanner.test.ts} |
| 5. Registries | {R} | {task_registry.json, implementation_traceability_register.json} |
| 6. Documentation | {D} | {CLAUDE.md (learnings section)} |
| **TOTAL** | **{N}** | - |

Breakdown by Change Type:
- CREATE: {count} artifacts
- MODIFY: {count} artifacts
- DELETE: {count} artifacts (rare)
- VALIDATE: {count} artifacts (verify still applies)

═══════════════════════════════════════════════════════════════
```

#### Step 2.5: Reflexion Self-Critique

```bash
REFLEXION CRITICAL SELF-ASSESSMENT:

═══════════════════════════════════════════════════════════════
              REFLEXION SELF-CRITIQUE
═══════════════════════════════════════════════════════════════

Question 1: Completeness - "Did I identify ALL affected artifacts?"
─────────────────────────────────────────────────────────────────

STEP 1: Re-scan with alternative keywords
    - Use synonyms for key terms from change request
    - Use related terminology (e.g., "scanner" → "barcode", "scan", "reader")
    - Check for indirect references

STEP 2: Check for orphaned references
    - Search for artifact IDs in all registries
    - Identify artifacts referencing affected ones
    - Verify bidirectional links complete

STEP 3: Verify no missing chains
    - For each chain, verify all intermediate nodes present
    - Check for broken or dangling links
    - Validate against traceability registries

RESULT: ✓ Complete | ⚠ Possibly incomplete | ❌ Gaps found
REASONING: {Explain findings}
MISSING: {List any potentially missed artifacts, or "None identified"}

─────────────────────────────────────────────────────────────────

Question 2: Root Cause Accuracy - "Is the root cause correct?"
─────────────────────────────────────────────────────────────────

VERIFY root cause identification:
    ✓ Did analysis reach systemic/process level?
    ✓ Or did it stop at symptom/technical level? (BAD)

    IF stopped at technical level:
        ⚠ WARNING: May not be TRUE root cause
        RECOMMENDATION: Go deeper with Why analysis

CHECK consistency:
    ✓ Does root cause explain ALL symptoms?
    ✓ Does root cause align with evidence?
    ✓ Are there contradicting observations?

VALIDATE countermeasures:
    ✓ Do countermeasures address root cause (not just symptom)?
    ✓ Will countermeasures prevent recurrence?
    ✓ Are there unintended side effects?

RESULT: ✓ Accurate | ⚠ Minor issues | ❌ Major issues
REASONING: {Explain findings}
ISSUES: {List any inaccuracies, or "None identified"}

─────────────────────────────────────────────────────────────────

Question 3: TDD Compliance - "Are test changes properly planned?"
─────────────────────────────────────────────────────────────────

CHECK test planning:
    ✓ Are new test cases clearly defined?
    ✓ Is RED-GREEN-REFACTOR cycle specified?
    ✓ Are test names descriptive and specific?

VERIFY test coverage:
    ✓ Do tests cover all new code paths?
    ✓ Do tests cover edge cases?
    ✓ Do tests cover error conditions?

VALIDATE TDD order:
    ✓ Is it clear tests must be written BEFORE implementation?
    ✓ Are tests designed to FAIL initially (RED phase)?
    ✓ Is refactor phase optional/conditional?

RESULT: ✓ Properly planned | ⚠ Minor gaps | ❌ Insufficient planning
REASONING: {Explain findings}
GAPS: {List any test coverage gaps, or "None identified"}

─────────────────────────────────────────────────────────────────

Question 4: Risk Assessment - "What could go wrong?"
─────────────────────────────────────────────────────────────────

IDENTIFY risks:

    Traceability chain breaks: [YES/NO]
        IF YES: {Which chains? How to prevent?}

    Regression risk: [LOW/MEDIUM/HIGH]
        {Why? What existing functionality might break?}

    Build risk: [LOW/MEDIUM/HIGH]
        {Will changes compile? Dependencies okay?}

    Test risk: [LOW/MEDIUM/HIGH]
        {Will existing tests still pass?}

    Timeline impact: [None/Sprint/Release]
        {How much time will this take?}

    Breaking changes: [YES/NO]
        IF YES: {What breaks? Migration path?}

SEVERITY: [CRITICAL|HIGH|MEDIUM|LOW]

MITIGATION STRATEGIES:
    - {Strategy 1}
    - {Strategy 2}
    - {Strategy 3}

─────────────────────────────────────────────────────────────────

CALCULATE Confidence Level:
──────────────────────────

confidence_score = 0

IF completeness == "✓ Complete":
    confidence_score += 40
ELIF completeness == "⚠ Possibly incomplete":
    confidence_score += 25
ELSE:
    confidence_score += 10

IF accuracy == "✓ Accurate":
    confidence_score += 35
ELIF accuracy == "⚠ Minor issues":
    confidence_score += 20
ELSE:
    confidence_score += 5

IF tdd_compliance == "✓ Properly planned":
    confidence_score += 25
ELIF tdd_compliance == "⚠ Minor gaps":
    confidence_score += 15
ELSE:
    confidence_score += 5

confidence_level =
    IF confidence_score >= 85: "HIGH"
    ELIF confidence_score >= 60: "MEDIUM"
    ELSE: "LOW"

confidence_percentage = confidence_score

═══════════════════════════════════════════════════════════════

OUTPUT Reflexion Summary:

**Reflexion Self-Critique Summary**

Completeness Check: {✓/⚠/❌} {Reasoning}
Root Cause Accuracy: {✓/⚠/❌} {Reasoning}
TDD Compliance: {✓/⚠/❌} {Reasoning}

Risk Assessment:
- Traceability: {risk details}
- Regression: {risk level} - {why}
- Build: {risk level} - {why}
- Timeline: {impact}
- Breaking Changes: {YES/NO} - {details}

**Confidence Level: {level} ({percentage}%)**

Reasoning: {Detailed explanation of confidence level}

Warnings:
- {Warning 1 if any}
- {Warning 2 if any}

Recommendations:
- {Recommendation 1}
- {Recommendation 2}

═══════════════════════════════════════════════════════════════
```

#### Step 2.6: Generate ANALYSIS.md

```bash
CREATE analysis document:

WRITE Implementation_{SYSTEM_NAME}/change-requests/_working/ANALYSIS.md:

---
document_id: ANALYSIS-CR-{NNN}
version: 1.0.0
created_at: {YYYY-MM-DD HH:MM:SS}
generated_by: htec-sdd-changerequest (Phase 2)
cr_id: CR-{SYSTEM}-{NNN}
analysis_method: {method}
---

# Root Cause Analysis - CR-{SYSTEM}-{NNN}

## Change Request Summary

- **ID**: CR-{SYSTEM}-{NNN}
- **Type**: {Bug/Improvement/Feedback}
- **Severity**: {CRITICAL/HIGH/MEDIUM/LOW}
- **Complexity**: {SIMPLE/MODERATE/COMPLEX}
- **Reporter**: {name/context}
- **Date**: {YYYY-MM-DD}

## Problem Statement

{Clear, concise description of the issue or improvement needed}

## Root Cause Analysis ({Method Name})

{Full output from Step 2.1 - the selected analysis method}

## Hierarchical Traceability Chains Affected

{Full output from Step 2.3 - tree-structured chains with before/after}

## 6-Layer Impact Summary

{Full output from Step 2.4 - table showing impact across all layers}

## Reflexion Self-Critique

{Full output from Step 2.5 - reflexion critical self-assessment}

## Recommended Countermeasures

Based on root cause analysis:

### Immediate Fix (Hours)
- {Quick patch to stop the bleeding}

### Short-Term Prevention (Days)
- {Fix the immediate root cause}
- {Add monitoring/alerts}

### Long-Term Systemic Fix (Weeks)
- {Address systemic issues}
- {Process improvements}

---

**Analysis completed at**: {timestamp}
**Confidence Level**: {level} ({percentage}%)
**Next Phase**: Session Registration (Phase 3)

OUTPUT Phase 2:
    - ANALYSIS.md (comprehensive analysis document)
    - Hierarchical chains data structure
    - 6-layer impact summary
    - Reflexion confidence score
```

---

### PHASE 3: Session Registration

**Objective**: Create session folder and register change request.

#### Step 3.1: Generate CR ID

```bash
READ Implementation_{SYSTEM_NAME}/change-requests/change_request_registry.json

IF not exists:
    CREATE registry:
    {
        "schema_version": "1.0.0",
        "system_name": "{SYSTEM_NAME}",
        "change_requests": {}
    }

FIND next available ID:
    existing_crs = list(registry["change_requests"].keys())

    IF existing_crs empty:
        next_id = "CR-{SYSTEM}-001"
    ELSE:
        max_num = max(extract_number(cr_id) for cr_id in existing_crs)
        next_id = f"CR-{SYSTEM}-{max_num + 1:03d}"

cr_id = next_id
```

#### Step 3.2: Create Session Folder

```bash
CREATE session folder structure:

session_folder = Implementation_{SYSTEM_NAME}/change-requests/{YYYY-MM-DD}_CR-{NNN}/

CREATE directories:
    {session_folder}/
    ├── CHANGE_REQUEST.md         # Original request (Step 3.3)
    ├── ANALYSIS.md               # Root cause analysis (from Phase 2)
    ├── IMPLEMENTATION_PLAN.md    # PDCA plan (Phase 5)
    ├── IMPLEMENTATION_LOG.md     # Execution log (Phase 6)
    ├── VALIDATION_REPORT.md      # Reflexion validation (Phase 7)
    └── SUMMARY.md                # Final summary (Phase 8)

COPY ANALYSIS.md from _working/ to session folder:
    cp Implementation_{SYSTEM_NAME}/change-requests/_working/ANALYSIS.md \
       {session_folder}/ANALYSIS.md
```

#### Step 3.3: Create CHANGE_REQUEST.md

```bash
WRITE {session_folder}/CHANGE_REQUEST.md:

---
document_id: CR-{SYSTEM}-{NNN}
version: 1.0.0
created_at: {YYYY-MM-DD HH:MM:SS}
cr_type: {Bug/Improvement/Feedback}
severity: {CRITICAL/HIGH/MEDIUM/LOW}
complexity: {SIMPLE/MODERATE/COMPLEX}
status: registered
---

# Change Request - CR-{SYSTEM}-{NNN}

## Description

{User-provided description from Phase 1}

## Reporter Context

- **Reporter**: {who reported this}
- **Date**: {when reported}
- **Environment**: {where observed - dev/staging/prod}

## Details

{IF Bug:}
### Reproduction Steps

1. {Step 1}
2. {Step 2}
3. {Step 3}

### Expected Behavior

{What should happen}

### Actual Behavior

{What actually happens}

### Error Messages / Logs

```
{Error messages or log excerpts}
```

{IF Improvement:}
### Current Behavior

{How it works now}

### Desired Behavior

{How it should work}

### Justification

{Why this matters - user story, business value}

### Acceptance Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

{IF Feedback:}
### Stakeholder

{Who provided feedback}

### Original Requirement

{REQ-XXX or JTBD-X.X reference}

### Feedback Content

{What needs to change}

### Priority

{Urgency and importance}

## Triage Assessment

- **Severity**: {CRITICAL/HIGH/MEDIUM/LOW}
- **Complexity**: {SIMPLE/MODERATE/COMPLEX}
- **Analysis Method**: {Quick Check/5 Whys/Fishbone/A3 Full}
- **Estimated Duration**: {from Phase 1 triage}

## Affected Files (Preliminary)

{List from Phase 1 scan - will be refined in Phase 2}

---

**Status**: Registered
**Created**: {timestamp}
**Next Phase**: Approval Gate (Phase 4)
```

#### Step 3.4: Register in change_request_registry.json

```bash
UPDATE Implementation_{SYSTEM_NAME}/change-requests/change_request_registry.json:

ADD entry:
{
    "CR-{SYSTEM}-{NNN}": {
        "title": "{Brief title from description}",
        "type": "{Bug/Improvement/Feedback}",
        "severity": "{CRITICAL/HIGH/MEDIUM/LOW}",
        "complexity": "{SIMPLE/MODERATE/COMPLEX}",
        "status": "registered",
        "created_at": "{ISO timestamp}",
        "analysis_method": "{Quick Check/5 Whys/Fishbone/A3 Full}",
        "session_folder": "{YYYY-MM-DD}_CR-{NNN}",
        "root_cause": "{Brief summary from ANALYSIS.md}",
        "confidence_level": "{HIGH/MEDIUM/LOW}",
        "confidence_percentage": {score},
        "affected_layers": {
            "layer_1": {count},
            "layer_2": {count},
            "layer_3": {count},
            "layer_4": {count},
            "layer_5": {count},
            "layer_6": {count}
        },
        "current_phase": 3,
        "phases_completed": ["input_collection", "impact_analysis", "registration"]
    }
}

LOG registration:
    ✅ CR-{SYSTEM}-{NNN} registered successfully
    📁 Session folder: Implementation_{SYSTEM_NAME}/change-requests/{date}_CR-{NNN}/
```

OUTPUT Phase 3:
    - cr_id (e.g., CR-INV-042)
    - session_folder path
    - Registry updated
```

---

### PHASE 4: Approval Gate (USER INTERACTION)

**Objective**: Present analysis to user and get approval to proceed.

**AskUserQuestion Integration**: This is the primary user decision point.

#### Step 4.1: Prepare Approval Summary

```bash
PREPARE summary for user presentation:

READ from Phase 2 outputs:
    - Hierarchical chains (from ANALYSIS.md)
    - 6-layer impact summary (from ANALYSIS.md)
    - Reflexion confidence score (from ANALYSIS.md)
    - Root cause summary (from ANALYSIS.md)

FORMAT approval summary:

═══════════════════════════════════════════════════════════════
           CHANGE REQUEST APPROVAL SUMMARY
═══════════════════════════════════════════════════════════════

**CR-{SYSTEM}-{NNN}**: {Title}

**Root Cause**: {One-sentence summary}

**Impact**: {N} artifacts across {M} layers

**Confidence**: {level} ({percentage}%)

{IF confidence < 70%:}
⚠️ WARNING: Confidence level below 70%. Review analysis carefully.
{ENDIF}

═══════════════════════════════════════════════════════════════

{Include full hierarchical chains from ANALYSIS.md}

═══════════════════════════════════════════════════════════════

{Include 6-layer impact summary from ANALYSIS.md}

═══════════════════════════════════════════════════════════════

{Include reflexion critique summary from ANALYSIS.md}

═══════════════════════════════════════════════════════════════
```

#### Step 4.2: User Decision (AskUserQuestion)

```bash
PRESENT analysis and request decision:

AskUserQuestion:
    question: "Based on the impact analysis above, how would you like to proceed with CR-{SYSTEM}-{NNN}?"
    header: "Approval"
    multiSelect: false
    options: [
        {
            label: "Proceed with Implementation (Recommended)",
            description: "Impact analysis looks good. Continue to planning and implementation phases."
        },
        {
            label: "Need More Information",
            description: "Analysis is incomplete or unclear. Provide additional details or re-analyze with different method."
        },
        {
            label: "Modify Scope",
            description: "Impact is too broad. Reduce scope or split into multiple CRs."
        },
        {
            label: "Reject / Defer",
            description: "Do not proceed with this change request at this time."
        }
    ]

decision = user_answer
```

#### Step 4.3: Handle Decision

```bash
HANDLE user decision:

IF decision == "Proceed with Implementation":
    LOG:
        ✅ CR-{SYSTEM}-{NNN} approved for implementation

    UPDATE registry status:
        status = "approved"
        approved_at = {ISO timestamp}

    CONTINUE to Phase 5 (Planning)

ELIF decision == "Need More Information":
    AskUserQuestion:
        question: "What additional information do you need?"
        header: "Info Needed"
        options: [
            {
                label: "Re-analyze with different method",
                description: "Use a deeper analysis method (e.g., Fishbone or A3 instead of 5 Whys)."
            },
            {
                label: "Clarify root cause",
                description: "Root cause is unclear or seems incorrect."
            },
            {
                label: "Expand impact analysis",
                description: "Some affected artifacts may be missing."
            },
            {
                label: "Provide reproduction steps",
                description: "Need clearer reproduction or evidence."
            }
        ]

    info_needed = user_answer

    IF info_needed == "Re-analyze with different method":
        AskUserQuestion:
            question: "Which analysis method should we use?"
            header: "Method"
            options: [
                {label: "5 Whys", description: "Standard depth, 30-60 min"},
                {label: "Fishbone", description: "Multi-factor, 60-90 min"},
                {label: "A3 Full", description: "Comprehensive, 2-4 hours"}
            ]

        new_method = user_answer

        LOG:
            🔄 Re-analyzing with {new_method}

        # Go back to Phase 2 Step 2.1 with new method
        analysis_method = new_method
        RETURN to Phase 2 Step 2.1

    ELIF info_needed == "Clarify root cause":
        LOG:
            🔄 Refining root cause analysis

        # Go back to Phase 2 Step 2.1, focus on deeper Why analysis
        RETURN to Phase 2 Step 2.1 with note: "User requested clarification"

    ELIF info_needed == "Expand impact analysis":
        LOG:
            🔄 Expanding impact analysis

        # Go back to Phase 2 Step 2.2, do more thorough scan
        RETURN to Phase 2 Step 2.2 with note: "User suspects missing artifacts"

    ELSE: # Provide reproduction steps
        AskUserQuestion (free text):
            question: "Please provide detailed reproduction steps:"
            header: "Reproduction"
            options: [] # Free text input

        reproduction_steps = user_input

        # Append to CHANGE_REQUEST.md
        APPEND reproduction_steps to CHANGE_REQUEST.md

        LOG:
            ✅ Reproduction steps added

        # Go back to Phase 2 Step 2.1 with new info
        RETURN to Phase 2 Step 2.1

ELIF decision == "Modify Scope":
    AskUserQuestion (free text):
        question: "How should the scope be modified? Describe what to include/exclude:"
        header: "Scope Change"
        options: [] # Free text input

    scope_modification = user_input

    LOG:
        📝 Scope modification requested: {scope_modification}

    # Manual intervention needed
    DISPLAY:
        ⚠️ Scope modification requires manual intervention.
        Please review ANALYSIS.md and adjust affected artifacts list.
        Then run: /htec-sdd-changerequest {SYSTEM} --id=CR-{NNN}

    UPDATE registry:
        status = "scope_modification_needed"
        notes = scope_modification

    EXIT (user must manually adjust and resume)

ELIF decision == "Reject / Defer":
    AskUserQuestion (free text):
        question: "Please provide reason for rejection/deferral:"
        header: "Reason"
        options: [] # Free text input

    rejection_reason = user_input

    UPDATE registry:
        status = "rejected"
        rejected_at = {ISO timestamp}
        rejection_reason = rejection_reason

    LOG:
        ❌ CR-{SYSTEM}-{NNN} rejected
        Reason: {rejection_reason}

    EXIT with message:
        Change request CR-{SYSTEM}-{NNN} has been rejected and will not be implemented.
        Registry updated with rejection reason.
```

OUTPUT Phase 4:
    - User decision captured
    - Registry status updated (approved/rejected/modification_needed)
    - If approved: Continue to Phase 5
    - If rejected: Exit
    - If modification needed: Manual intervention or return to Phase 2
```

---

### PHASE 5: Implementation Planning with Reflexion (PDCA PLAN + REFLEXION)

**Objective**: Generate detailed implementation plan with TDD specifications and reflexion validation.

**PDCA Integration**: This is the PLAN phase of the PDCA cycle.
**Reflexion Integration**: Plan validation through reflexion.

#### Step 5.1: Extract Countermeasures from Analysis

```bash
READ Implementation_{SYSTEM_NAME}/change-requests/{date}_CR-{NNN}/ANALYSIS.md

EXTRACT countermeasures section:
    - Immediate fixes
    - Short-term prevention
    - Long-term systemic fixes

EXTRACT affected artifacts:
    - From hierarchical chains
    - From 6-layer impact summary

PREPARE context for planning:
    context = {
        "cr_id": "CR-{SYSTEM}-{NNN}",
        "root_cause": "{from ANALYSIS.md}",
        "countermeasures": "{extracted countermeasures}",
        "affected_artifacts": "{list of all affected artifacts}",
        "code_files": "{list from Layer 3}",
        "test_files": "{list from Layer 4}",
        "tdd_required": true,  # Always true for Implementation stage
        "reflexion_enabled": true
    }
```

#### Step 5.2: Generate Detailed Implementation Plan

```bash
GENERATE implementation plan:

CREATE IMPLEMENTATION_PLAN.md:

---
document_id: PLAN-CR-{NNN}
version: 1.0.0
created_at: {YYYY-MM-DD HH:MM:SS}
generated_by: htec-sdd-changerequest (Phase 5)
cr_id: CR-{SYSTEM}-{NNN}
pdca_phase: PLAN
---

# Implementation Plan - CR-{SYSTEM}-{NNN}

## Hypothesis (PDCA)

**IF** we implement the following countermeasures:
- {Countermeasure 1}
- {Countermeasure 2}

**THEN** we expect:
- {Outcome 1}
- {Outcome 2}

**MEASURABLE SUCCESS CRITERIA**:
- ✓ {Specific, measurable criterion 1}
- ✓ {Specific, measurable criterion 2}
- ✓ {Specific, measurable criterion 3}

## Rollback Plan

**IF** implementation fails or causes regressions:

1. **Immediate Rollback**:
   - Revert commits: `git revert <commit-hash>`
   - Restore from backup: {backup location}

2. **Verification**:
   - Run test suite to confirm rollback successful
   - Check production metrics

3. **Analysis**:
   - Document what went wrong
   - Return to Phase 2 (Analysis) with learnings

## TDD Task Breakdown

{FOR each affected code file:}

### Task {N}: {Description}

**File**: {file_path}
**Change Type**: {MODIFY/CREATE}
**Complexity**: {SIMPLE/MODERATE/COMPLEX}

#### RED Phase: Write Failing Test

Test File: {test_file_path}

```typescript
describe('{Component/Function name}', () => {
  it('{should behavior description}', () => {
    // Arrange
    {setup code}

    // Act
    {action that triggers behavior}

    // Assert
    expect({result}).{assertion}
  });
});
```

**Expected Result**: Test FAILS (because functionality not yet implemented)

#### GREEN Phase: Implement Minimal Fix

Implementation File: {code_file_path}

```typescript
{Proposed implementation - minimal code to make test pass}
```

**Expected Result**: Test PASSES

#### REFACTOR Phase: Clean Up (Optional)

{IF refactoring needed:}
- Extract duplicated code to utility function
- Rename variables for clarity
- Simplify complex conditionals

{ELSE:}
- No refactoring needed - implementation is clean

**Expected Result**: Tests still PASS after refactor

#### Verification Checklist

- [ ] Test written and FAILS initially
- [ ] Implementation makes test PASS
- [ ] Refactoring maintains GREEN state
- [ ] No existing tests broken
- [ ] Code follows project patterns
- [ ] No new linting errors

---

{REPEAT for each affected file}

---

## Execution Order

**Dependencies**: Tasks must be executed in this order:

1. Task {N} (no dependencies)
2. Task {M} (depends on Task N)
3. Task {K} (depends on Task M)

**Parallelizable**: Tasks {X}, {Y}, {Z} can be done in parallel

## Estimated Timeline

| Task | Estimated Duration |
|------|-------------------|
| Task 1 | {X} minutes |
| Task 2 | {Y} minutes |
| Task 3 | {Z} minutes |
| **Total** | **{sum} minutes** |

## Registry Updates

After implementation, update:

1. **task_registry.json**:
   - Mark T-{NNN} as "modified_for_cr"
   - Add CR reference

2. **implementation_traceability_register.json**:
   - Add new code → test traces
   - Update task → code traces

3. **change_request_registry.json**:
   - Update status to "implementing"
   - Add implementation_started timestamp

## Documentation Updates

After implementation, update:

{IF significant learning:}
- **CLAUDE.md** - Add to "Implementation Learnings" section

{IF new pattern:}
- **Component _readme.md** - Document new behavior

---

**Plan Generated**: {timestamp}
**Next Phase**: Implementation Execution (Phase 6)
```

#### Step 5.3: Reflexion Plan Validation

```bash
REFLEXION PLAN VALIDATION:

═══════════════════════════════════════════════════════════════
         REFLEXION: PLAN VALIDATION
═══════════════════════════════════════════════════════════════

Question 1: Completeness - "Does the plan cover all changes?"
────────────────────────────────────────────────────────────────

CHECK coverage:
    ✓ All affected files from Layer 3 have TDD tasks?
    ✓ All test files from Layer 4 are specified?
    ✓ Registry updates planned?
    ✓ Documentation updates planned?

RESULT: ✓ Complete | ⚠ Minor gaps | ❌ Major gaps
REASONING: {Explain}
GAPS: {List gaps or "None"}

────────────────────────────────────────────────────────────────

Question 2: TDD Compliance - "Is TDD properly specified?"
────────────────────────────────────────────────────────────────

CHECK TDD specs:
    ✓ RED phase clearly defined (failing test)?
    ✓ GREEN phase clearly defined (minimal implementation)?
    ✓ REFACTOR phase specified (optional)?
    ✓ Test-first order enforced?

RESULT: ✓ Compliant | ⚠ Minor issues | ❌ Non-compliant
REASONING: {Explain}
ISSUES: {List issues or "None"}

────────────────────────────────────────────────────────────────

Question 3: Success Criteria - "Are criteria measurable?"
────────────────────────────────────────────────────────────────

EVALUATE success criteria:
    ✓ Are criteria specific (not vague)?
    ✓ Are criteria measurable (can verify pass/fail)?
    ✓ Are criteria realistic (achievable)?

EXAMPLE GOOD:
    "✓ All tests pass with >80% code coverage"
    "✓ Response time < 500ms under load"

EXAMPLE BAD:
    "✓ Code works well" (not measurable)
    "✓ Performance is good" (vague)

RESULT: ✓ Measurable | ⚠ Some vague | ❌ Not measurable
REASONING: {Explain}
ISSUES: {List issues or "None"}

────────────────────────────────────────────────────────────────

Question 4: Risk Mitigation - "Is rollback plan adequate?"
────────────────────────────────────────────────────────────────

EVALUATE rollback plan:
    ✓ Clear rollback steps?
    ✓ Rollback verification specified?
    ✓ Data backup/restore considered?

RESULT: ✓ Adequate | ⚠ Needs improvement | ❌ Inadequate
REASONING: {Explain}
ISSUES: {List issues or "None"}

────────────────────────────────────────────────────────────────

CALCULATE Confidence Level:
──────────────────────────

confidence_score = 0

IF completeness == "✓": confidence_score += 30
ELIF completeness == "⚠": confidence_score += 20
ELSE: confidence_score += 5

IF tdd_compliance == "✓": confidence_score += 30
ELIF tdd_compliance == "⚠": confidence_score += 20
ELSE: confidence_score += 5

IF success_criteria == "✓": confidence_score += 25
ELIF success_criteria == "⚠": confidence_score += 15
ELSE: confidence_score += 5

IF risk_mitigation == "✓": confidence_score += 15
ELIF risk_mitigation == "⚠": confidence_score += 10
ELSE: confidence_score += 5

confidence_level =
    IF confidence_score >= 85: "HIGH"
    ELIF confidence_score >= 60: "MEDIUM"
    ELSE: "LOW"

═══════════════════════════════════════════════════════════════

**Reflexion Plan Validation Summary**

Completeness: {✓/⚠/❌} - {reasoning}
TDD Compliance: {✓/⚠/❌} - {reasoning}
Success Criteria: {✓/⚠/❌} - {reasoning}
Risk Mitigation: {✓/⚠/❌} - {reasoning}

**Plan Confidence: {level} ({percentage}%)**

{IF confidence < 60%:}
⚠️ WARNING: Plan confidence below 60%. Review and refine before execution.

Refinement Recommendations:
- {Recommendation 1}
- {Recommendation 2}
{ENDIF}

═══════════════════════════════════════════════════════════════
```

#### Step 5.4: Refine Plan if Needed

```bash
IF plan_confidence < 60%:
    LOG:
        ⚠️ Plan requires refinement (confidence {percentage}%)

    AskUserQuestion:
        question: "Plan validation identified issues. How would you like to proceed?"
        header: "Plan Issues"
        options: [
            {
                label: "Refine Plan Automatically",
                description: "Address reflexion recommendations and regenerate plan."
            },
            {
                label: "Manual Review",
                description: "Review IMPLEMENTATION_PLAN.md manually and make edits."
            },
            {
                label: "Proceed Anyway",
                description: "Accept current plan despite low confidence (not recommended)."
            }
        ]

    decision = user_answer

    IF decision == "Refine Plan Automatically":
        # Regenerate plan addressing reflexion issues
        LOG:
            🔄 Refining implementation plan...

        # Go back to Step 5.2 with reflexion feedback incorporated
        RETURN to Step 5.2 with note: "Address reflexion issues: {issues}"

    ELIF decision == "Manual Review":
        DISPLAY:
            📝 Please review and edit:
            {session_folder}/IMPLEMENTATION_PLAN.md

            When ready, run:
            /htec-sdd-changerequest {SYSTEM} --id=CR-{NNN}

        UPDATE registry:
            status = "plan_review_needed"

        EXIT (user must manually edit and resume)

    ELSE: # Proceed anyway
        LOG:
            ⚠️ Proceeding with low-confidence plan ({percentage}%)

        CONTINUE to Phase 6

ELSE:
    LOG:
        ✅ Plan validated with {level} confidence ({percentage}%)

    APPEND reflexion validation to IMPLEMENTATION_PLAN.md

    CONTINUE to Phase 6
```

OUTPUT Phase 5:
    - IMPLEMENTATION_PLAN.md (detailed TDD task breakdown)
    - Reflexion plan validation
    - Plan confidence score
    - If confidence < 60%: Refinement or manual review
    - If confidence ≥ 60%: Ready for execution
```

---

### PHASE 6: Implementation Execution (TDD + PDCA DO)

**Objective**: Execute TDD tasks following RED-GREEN-REFACTOR cycle.

**PDCA Integration**: This is the DO phase of the PDCA cycle.
**TDD Enforcement**: Strict RED-GREEN-REFACTOR compliance required.

#### Step 6.1: Initialize Execution Log

```bash
CREATE IMPLEMENTATION_LOG.md:

---
document_id: LOG-CR-{NNN}
version: 1.0.0
created_at: {YYYY-MM-DD HH:MM:SS}
cr_id: CR-{SYSTEM}-{NNN}
pdca_phase: DO
---

# Implementation Log - CR-{SYSTEM}-{NNN}

## Execution Started

**Timestamp**: {ISO timestamp}
**Executor**: Claude (htec-sdd-changerequest)
**Plan**: IMPLEMENTATION_PLAN.md

---

## Task Execution Log

{Will be populated as tasks execute}

---

## TDD Compliance Tracking

| Task | RED ✓ | GREEN ✓ | REFACTOR ✓ | Tests Pass ✓ |
|------|-------|---------|------------|--------------|
| {Task names will be added dynamically} |

---

## Issues Encountered

{Will be populated if issues occur}

---
```

#### Step 6.2: Execute TDD Tasks

```bash
READ IMPLEMENTATION_PLAN.md

EXTRACT task list in execution order

FOR each task in plan:

    LOG to IMPLEMENTATION_LOG.md:
        ═══════════════════════════════════════════════════════════
        TASK {N}: {Description}
        ═══════════════════════════════════════════════════════════

        **File**: {code_file}
        **Test**: {test_file}
        **Started**: {timestamp}

    # ═══════════════════════════════════════════════════════════
    # RED PHASE: Write Failing Test
    # ═══════════════════════════════════════════════════════════

    LOG:
        🔴 RED PHASE: Writing failing test...

    READ test specification from plan

    IF test_file not exists:
        # Create new test file
        WRITE {test_file}:
            {Test template with imports}
            {Test case from plan}
    ELSE:
        # Append to existing test file
        EDIT {test_file}:
            ADD test case from plan

    LOG to IMPLEMENTATION_LOG.md:
        🔴 RED: Test written

        Test Case:
        ```typescript
        {test code}
        ```

    # RUN TEST - must FAIL
    RUN: npm test {test_file}

    LOG test output to IMPLEMENTATION_LOG.md:
        Test Output (Expected: FAIL):
        ```
        {test output}
        ```

    IF test PASSES:
        ❌ ERROR: Test passed in RED phase (should fail!)

        APPEND to IMPLEMENTATION_LOG.md:
            ❌ TDD VIOLATION: Test passed without implementation
            This indicates test is not correctly validating the requirement.

        # Block execution - this is a quality gate failure
        DISPLAY:
            ❌ TDD Protocol Violation

            Test passed without implementation. This is invalid.

            Possible causes:
            1. Test is too lenient
            2. Test is testing wrong thing
            3. Implementation already exists

            Action: Fix test to properly fail, then resume.

        UPDATE registry:
            status = "tdd_violation"
            issue = "Test passed in RED phase"

        EXIT

    ELSE: # Test FAILED (correct)
        ✓ RED phase complete

        LOG to IMPLEMENTATION_LOG.md:
            ✓ RED: Test correctly fails

        UPDATE TDD tracking table:
            | Task {N} | ✓ | - | - | - |

    # ═══════════════════════════════════════════════════════════
    # GREEN PHASE: Implement Minimal Fix
    # ═══════════════════════════════════════════════════════════

    LOG:
        🟢 GREEN PHASE: Implementing minimal fix...

    READ implementation specification from plan

    IF code_file not exists:
        WRITE {code_file}:
            {Implementation from plan}
    ELSE:
        EDIT {code_file}:
            {Apply changes from plan}

    LOG to IMPLEMENTATION_LOG.md:
        🟢 GREEN: Implementation added

        Code Changes:
        ```typescript
        {implementation code}
        ```

    # RUN TEST - must PASS now
    RUN: npm test {test_file}

    LOG test output to IMPLEMENTATION_LOG.md:
        Test Output (Expected: PASS):
        ```
        {test output}
        ```

    IF test FAILS:
        ❌ ERROR: Test still fails after implementation

        APPEND to IMPLEMENTATION_LOG.md:
            ❌ GREEN PHASE FAILED: Test still fails

            Possible causes:
            1. Implementation incomplete
            2. Implementation incorrect
            3. Test expectations wrong

            Debug Output:
            {error message}

        # Allow retry or manual intervention
        AskUserQuestion:
            question: "GREEN phase failed. How to proceed?"
            header: "Test Failure"
            options: [
                {
                    label: "Debug and Retry",
                    description: "Analyze failure, fix implementation, retry."
                },
                {
                    label: "Manual Fix Required",
                    description: "Pause for manual debugging and code review."
                },
                {
                    label: "Skip This Task",
                    description: "Log failure and continue to next task (not recommended)."
                }
            ]

        decision = user_answer

        IF decision == "Debug and Retry":
            LOG:
                🔍 Debugging implementation...

            # Analyze test failure
            READ test output
            IDENTIFY failure reason

            # Adjust implementation
            EDIT {code_file}:
                {Fix implementation based on failure}

            # Retry GREEN phase
            GOTO GREEN PHASE retry

        ELIF decision == "Manual Fix Required":
            UPDATE registry:
                status = "manual_intervention_needed"
                current_task = task_id

            DISPLAY:
                ⏸️ Paused for manual intervention

                Please debug and fix:
                - Test: {test_file}
                - Code: {code_file}

                When fixed, run:
                /htec-sdd-changerequest {SYSTEM} --id=CR-{NNN}

            EXIT

        ELSE: # Skip task
            LOG to IMPLEMENTATION_LOG.md:
                ⚠️ SKIPPED: Task {N} skipped due to test failure

            UPDATE TDD tracking:
                | Task {N} | ✓ | ❌ | - | ❌ |

            CONTINUE to next task

    ELSE: # Test PASSED (correct)
        ✓ GREEN phase complete

        LOG to IMPLEMENTATION_LOG.md:
            ✓ GREEN: Test passes

        UPDATE TDD tracking table:
            | Task {N} | ✓ | ✓ | - | ✓ |

    # ═══════════════════════════════════════════════════════════
    # REFACTOR PHASE: Clean Up (Optional)
    # ═══════════════════════════════════════════════════════════

    READ refactor specification from plan

    IF refactor_needed:
        LOG:
            🔧 REFACTOR PHASE: Cleaning up code...

        EDIT {code_file}:
            {Apply refactorings from plan}

        LOG to IMPLEMENTATION_LOG.md:
            🔧 REFACTOR: Code cleaned up

            Refactorings:
            - {Refactoring 1}
            - {Refactoring 2}

        # RUN TESTS AGAIN - must still PASS
        RUN: npm test {test_file}

        IF test FAILS:
            ❌ ERROR: Refactoring broke tests!

            LOG to IMPLEMENTATION_LOG.md:
                ❌ REFACTOR FAILED: Tests broken by refactoring

            # Rollback refactoring
            REVERT {code_file} to GREEN phase state

            LOG:
                ⚠️ Refactoring rolled back, keeping GREEN implementation

            UPDATE TDD tracking:
                | Task {N} | ✓ | ✓ | ❌ | ✓ |

        ELSE: # Tests still PASS
            ✓ REFACTOR phase complete

            LOG to IMPLEMENTATION_LOG.md:
                ✓ REFACTOR: Tests still pass

            UPDATE TDD tracking:
                | Task {N} | ✓ | ✓ | ✓ | ✓ |

    ELSE:
        LOG to IMPLEMENTATION_LOG.md:
            🔧 REFACTOR: Skipped (not needed)

        UPDATE TDD tracking:
            | Task {N} | ✓ | ✓ | N/A | ✓ |

    # ═══════════════════════════════════════════════════════════
    # VERIFY: Run Full Test Suite
    # ═══════════════════════════════════════════════════════════

    LOG:
        🧪 VERIFY: Running full test suite...

    RUN: npm test

    LOG to IMPLEMENTATION_LOG.md:
        🧪 Full Test Suite:
        ```
        {test output}
        ```

    IF any test FAILS:
        ❌ REGRESSION DETECTED

        LOG to IMPLEMENTATION_LOG.md:
            ❌ REGRESSION: Changes broke existing tests

            Failed Tests:
            {list of failed tests}

        # Rollback this task
        REVERT changes from this task

        LOG:
            ⚠️ Task {N} rolled back due to regression

        MARK task as failed in tracking

        # Continue or stop based on severity
        IF failure_count > 3:
            DISPLAY:
                ❌ Too many failures ({failure_count})
                Stopping execution for review.

            UPDATE registry:
                status = "execution_failed"

            EXIT

    ELSE:
        ✓ All tests pass

        LOG to IMPLEMENTATION_LOG.md:
            ✓ VERIFY: No regressions, all tests pass

        LOG:
            ✅ Task {N} complete

    # ═══════════════════════════════════════════════════════════
    # LOG VERSION HISTORY
    # ═══════════════════════════════════════════════════════════

    RUN version history hook:
        python3 .claude/hooks/version_history_logger.py \
            "traceability/" \
            "{SYSTEM_NAME}" \
            "implementation" \
            "Claude" \
            "{version}" \
            "CR-{NNN} Task {N}: {description}" \
            "{related_artifact_ids}" \
            "{code_file}" \
            "modification"

    LOG to IMPLEMENTATION_LOG.md:
        📝 Version history updated

        ---

        **Task {N} Complete**
        **Timestamp**: {ISO timestamp}
        **Duration**: {elapsed_time}

        ═══════════════════════════════════════════════════════════

ENDFOR

LOG:
    ✅ All tasks executed
```

#### Step 6.3: Build Verification

```bash
LOG:
    🔨 BUILD VERIFICATION: Running build...

RUN: npm run build

LOG to IMPLEMENTATION_LOG.md:
    🔨 Build Output:
    ```
    {build output}
    ```

IF build FAILS:
    ❌ BUILD FAILED

    LOG to IMPLEMENTATION_LOG.md:
        ❌ BUILD FAILURE

        Build Errors:
        {error messages}

    DISPLAY:
        ❌ Build failed after implementation

        Review build errors in IMPLEMENTATION_LOG.md

        Action: Fix build errors and run:
        /htec-sdd-changerequest {SYSTEM} --id=CR-{NNN}

    UPDATE registry:
        status = "build_failed"

    EXIT

ELSE:
    ✓ Build successful

    LOG to IMPLEMENTATION_LOG.md:
        ✓ BUILD SUCCESS

        All changes compiled successfully.

LOG:
    ✅ Implementation phase complete
```

OUTPUT Phase 6:
    - IMPLEMENTATION_LOG.md (complete execution log)
    - TDD compliance tracking table
    - Code changes applied
    - Tests written and passing
    - Build verification passed
    - Version history updated
```

---

### PHASE 7: Validation with Reflexion (PDCA CHECK + REFLEXION)

**Objective**: Verify implementation meets success criteria and perform multi-perspective validation.

**PDCA Integration**: This is the CHECK phase of the PDCA cycle.
**Reflexion Integration**: Multi-perspective critique and self-assessment.

#### Step 7.1: Measure Results vs. Success Criteria

```bash
READ IMPLEMENTATION_PLAN.md

EXTRACT success criteria

LOG:
    📊 VALIDATION: Checking success criteria...

CREATE VALIDATION_REPORT.md:

---
document_id: VALIDATION-CR-{NNN}
version: 1.0.0
created_at: {YYYY-MM-DD HH:MM:SS}
cr_id: CR-{SYSTEM}-{NNN}
pdca_phase: CHECK
---

# Validation Report - CR-{SYSTEM}-{NNN}

## Success Criteria Verification

{FOR each criterion in plan:}

### Criterion {N}: {criterion_text}

**Verification Method**: {how to check}

{IF measurable metric:}
    **Expected**: {expected_value}
    **Actual**: {actual_value}
    **Status**: {✓ PASS | ❌ FAIL}

{IF test-based:}
    **Test**: {test_name}
    **Status**: {✓ PASS | ❌ FAIL}

{IF manual verification:}
    **Checked**: {what was checked}
    **Status**: {✓ PASS | ❌ FAIL}

**Evidence**:
{screenshot, log excerpt, test output, etc.}

{ENDFOR}

---

## Overall Success Criteria: {✓ ALL PASS | ❌ SOME FAILED}

{IF any failed:}
    Failed Criteria:
    - {Criterion 1} - {reason}
    - {Criterion 2} - {reason}
{ENDIF}

---
```

#### Step 7.2: Validate Hypothesis (PDCA Check)

```bash
READ hypothesis from IMPLEMENTATION_PLAN.md:
    "IF we implement X, THEN we expect Y"

APPEND to VALIDATION_REPORT.md:

## Hypothesis Validation (PDCA)

**Original Hypothesis**:
IF {countermeasures}
THEN {expected outcomes}

**Validation**:

{FOR each expected outcome:}

Outcome {N}: {outcome_text}

{CHECK if outcome achieved:}
    **Expected**: {what we expected to happen}
    **Actual**: {what actually happened}
    **Match**: {✓ YES | ❌ NO}

{IF mismatch:}
    **Analysis**: {Why didn't outcome match expectation?}
    **Learning**: {What does this tell us?}
{ENDIF}

{ENDFOR}

---

**Hypothesis Result**: {✓ CONFIRMED | ⚠ PARTIALLY CONFIRMED | ❌ REJECTED}

{IF rejected or partially confirmed:}
    **Action Required**: Return to PLAN phase with learnings

    Learnings:
    - {Learning 1}
    - {Learning 2}

    Recommended Adjustments:
    - {Adjustment 1}
    - {Adjustment 2}
{ENDIF}

---
```

#### Step 7.3: Regression Testing

```bash
LOG:
    🧪 REGRESSION TESTING: Full test suite...

RUN: npm test -- --coverage

APPEND to VALIDATION_REPORT.md:

## Regression Testing

**Test Suite**: Full suite
**Coverage**: {coverage_percentage}%

```
{test output}
```

**Results**:
- Total Tests: {total}
- Passed: {passed}
- Failed: {failed}
- Skipped: {skipped}

**Coverage**:
- Statements: {statements}%
- Branches: {branches}%
- Functions: {functions}%
- Lines: {lines}%

{IF failed > 0:}
    ❌ REGRESSIONS DETECTED

    Failed Tests:
    {list failed tests}

    **Status**: ❌ REGRESSION FAILURE
{ELSE:}
    ✓ NO REGRESSIONS

    **Status**: ✓ REGRESSION PASS
{ENDIF}

---
```

#### Step 7.4: Manual Verification

```bash
APPEND to VALIDATION_REPORT.md:

## Manual Verification

{IF Bug fix:}

### Bug Reproduction Test

**Original Issue**: {from CHANGE_REQUEST.md}

**Reproduction Steps**:
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Before Fix**:
{What happened before}

**After Fix**:
{What happens now}

**Status**: {✓ FIXED | ❌ NOT FIXED}

{IF Improvement:}

### Feature Verification

**New Behavior**: {what was added/changed}

**Verification Steps**:
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Observed Behavior**:
{What actually happens}

**Status**: {✓ WORKS AS EXPECTED | ❌ ISSUES FOUND}

---
```

#### Step 7.5: Multi-Perspective Reflexion Critique

```bash
REFLEXION MULTI-PERSPECTIVE CRITIQUE:

APPEND to VALIDATION_REPORT.md:

═══════════════════════════════════════════════════════════════
         REFLEXION: MULTI-PERSPECTIVE VALIDATION
═══════════════════════════════════════════════════════════════

Validator 1: REQUIREMENTS VALIDATOR
────────────────────────────────────────────────────────────────

PERSPECTIVE: Does implementation align with original request?

✓ CHECKLIST:
    □ Does fix address the root cause identified?
    □ Are all acceptance criteria met?
    □ Is there any scope creep (unrelated changes)?
    □ Does implementation follow plan?

EVALUATION:
    {For each checklist item, provide detailed evaluation}

    Alignment Score: {score}/10

    Issues Found:
    - {Issue 1 or "None"}
    - {Issue 2 or "None"}

    Recommendations:
    - {Recommendation 1 or "None"}

────────────────────────────────────────────────────────────────

Validator 2: SOLUTION ARCHITECT
────────────────────────────────────────────────────────────────

PERSPECTIVE: Is the technical approach sound?

✓ CHECKLIST:
    □ Does implementation follow architecture patterns?
    □ Is the solution scalable/maintainable?
    □ Are there better alternatives?
    □ Is technical debt introduced?

EVALUATION:
    {For each checklist item, provide detailed evaluation}

    Architecture Score: {score}/10

    Technical Debt Introduced:
    - {Debt 1 or "None"}

    Alternative Approaches:
    - {Alternative 1 or "None - current approach is optimal"}

    Recommendations:
    - {Recommendation 1 or "None"}

────────────────────────────────────────────────────────────────

Validator 3: CODE QUALITY REVIEWER
────────────────────────────────────────────────────────────────

PERSPECTIVE: Is the code clean and well-tested?

✓ CHECKLIST:
    □ Is code readable and maintainable?
    □ Are tests comprehensive?
    □ Is documentation updated?
    □ Are there code smells or anti-patterns?

EVALUATION:
    {For each checklist item, provide detailed evaluation}

    Code Quality Score: {score}/10

    Code Smells Found:
    - {Smell 1 or "None"}

    Test Coverage Assessment:
    - Adequate coverage: {YES/NO}
    - Edge cases tested: {YES/NO}
    - Error paths tested: {YES/NO}

    Documentation Status:
    - Inline comments: {ADEQUATE/INSUFFICIENT}
    - README updated: {YES/NO/N/A}
    - CLAUDE.md updated: {YES/NO/N/A}

    Recommendations:
    - {Recommendation 1 or "None"}

────────────────────────────────────────────────────────────────

CROSS-VALIDATOR CONSENSUS
────────────────────────────────────────────────────────────────

**Individual Scores**:
- Requirements: {score1}/10
- Architecture: {score2}/10
- Code Quality: {score3}/10

**Consensus Score**: {average}/10

**Consensus Rating**:
{IF average >= 7.0: "✓ PASS - Implementation approved"}
{ELIF average >= 5.0: "⚠ CONDITIONAL PASS - Improvements recommended"}
{ELSE: "❌ FAIL - Significant issues require fixing"}

**Unanimous Concerns** (all validators agree):
{List concerns all validators mentioned, or "None"}

**Divergent Opinions** (validators disagree):
{List areas where validators have different assessments, or "None"}

**Final Recommendation**:

{IF consensus >= 7.0:}
    ✓ Implementation is production-ready.
    Proceed to completion phase.

{ELIF consensus >= 5.0:}
    ⚠ Implementation is functional but could be improved.

    DECISION NEEDED:
    - Option A: Accept as-is and document technical debt
    - Option B: Iterate to address recommendations

    Recommended Option: {A or B with reasoning}

{ELSE:}
    ❌ Implementation has significant issues.

    REQUIRED ACTION:
    Return to Phase 6 (Implementation) and address:
    {List critical issues that must be fixed}
{ENDIF}

═══════════════════════════════════════════════════════════════
```

#### Step 7.6: User Decision on Validation Results

```bash
IF consensus_score < 7.0:

    AskUserQuestion:
        question: "Validation identified issues (consensus score: {score}/10). How to proceed?"
        header: "Validation"
        multiSelect: false
        options: [
            {
                label: "Iterate and Fix Issues",
                description: "Return to implementation phase and address validation concerns."
            },
            {
                label: "Accept with Technical Debt",
                description: "Accept current implementation and document technical debt for future improvement."
            },
            {
                label: "Manual Review Required",
                description: "Pause for manual code review before proceeding."
            }
        ]

    decision = user_answer

    IF decision == "Iterate and Fix Issues":
        LOG:
            🔄 Returning to implementation phase to address issues...

        UPDATE registry:
            status = "iterating"
            pdca_cycles += 1

        # Go back to Phase 6 with validation feedback
        RETURN to Phase 6 with note: "Address validation issues: {issues}"

    ELIF decision == "Accept with Technical Debt":
        LOG:
            ⚠️ Accepting implementation with technical debt

        APPEND to VALIDATION_REPORT.md:

            ---

            ## TECHNICAL DEBT ACCEPTED

            **Decision**: User accepted implementation despite validation score < 7.0
            **Reason**: {user can provide reason}

            **Technical Debt Items**:
            {List all issues flagged by validators}

            **Future Work**:
            - Create follow-up CR for improvements
            - Document in CLAUDE.md

        CONTINUE to Phase 8

    ELSE: # Manual review
        UPDATE registry:
            status = "manual_review_needed"

        DISPLAY:
            ⏸️ Paused for manual review

            Please review:
            - VALIDATION_REPORT.md
            - Implementation code changes
            - IMPLEMENTATION_LOG.md

            When ready, run:
            /htec-sdd-changerequest {SYSTEM} --id=CR-{NNN}

        EXIT

ELSE:
    LOG:
        ✅ Validation passed (consensus score: {score}/10)

    CONTINUE to Phase 8
```

OUTPUT Phase 7:
    - VALIDATION_REPORT.md (comprehensive validation)
    - Success criteria verification
    - Hypothesis validation (PDCA Check)
    - Regression test results
    - Multi-perspective reflexion critique
    - Consensus score (0-10)
    - User decision if issues found
```

---

### PHASE 8: Completion & Documentation (PDCA ACT + MEMORIZE)

**Objective**: Finalize CR, standardize if successful, and capture learnings.

**PDCA Integration**: This is the ACT phase of the PDCA cycle.
**Reflexion Integration**: MEMORIZE phase - harvest insights and update CLAUDE.md.

#### Step 8.1: PDCA ACT - Standardize or Iterate

```bash
READ VALIDATION_REPORT.md

EXTRACT consensus_score

IF consensus_score >= 7.0 OR user_accepted_with_debt:
    # STANDARDIZE (PDCA ACT)

    LOG:
        ✅ PDCA ACT: Standardizing successful implementation

    ACTIONS:
        1. Merge code changes (already done in Phase 6)
        2. Update documentation (Step 8.2)
        3. Update registries (Step 8.3)
        4. Capture learnings (Step 8.4)
        5. Generate summary (Step 8.5)

ELSE:
    # ITERATE (PDCA ACT)

    LOG:
        🔄 PDCA ACT: Implementation unsuccessful, planning next cycle

    UPDATE registry:
        status = "pdca_cycle_failed"
        pdca_cycles += 1

        pdca_history: [
            {
                "cycle": {current_cycle},
                "plan": "IMPLEMENTATION_PLAN.md",
                "result": "Failed validation",
                "consensus_score": {score},
                "learnings": "{learnings}"
            }
        ]

    # Do NOT standardize unverified changes
    # User must decide whether to iterate or abandon CR

    AskUserQuestion:
        question: "Implementation failed validation. Next steps?"
        header: "Failed PDCA"
        options: [
            {
                label: "Start New PDCA Cycle",
                description: "Return to planning with learnings and try different approach."
            },
            {
                label: "Abandon Change Request",
                description: "Mark CR as failed and document why."
            }
        ]

    decision = user_answer

    IF decision == "Start New PDCA Cycle":
        LOG:
            🔄 Starting new PDCA cycle with learnings

        # Return to Phase 5 (Planning) with validation feedback
        RETURN to Phase 5 with note: "PDCA Cycle {cycle} learnings: {learnings}"

    ELSE: # Abandon
        LOG:
            ❌ Change request abandoned after failed PDCA cycle

        UPDATE registry:
            status = "abandoned"
            abandoned_at = {ISO timestamp}
            reason = "Failed validation after implementation"

        # Generate failure summary
        GOTO Step 8.5 (but mark as failure summary)

        EXIT
```

#### Step 8.2: Update Documentation

```bash
IF standardize:

    LOG:
        📝 Updating documentation...

    # ──────────────────────────────────────────────────────────
    # CLAUDE.md - Implementation Learnings
    # ──────────────────────────────────────────────────────────

    READ VALIDATION_REPORT.md
    READ ANALYSIS.md
    READ IMPLEMENTATION_LOG.md

    IDENTIFY significant learnings:
        - Error patterns encountered
        - Debugging strategies used
        - Code quality insights
        - Process improvements

    HARVEST insights using criteria:
        RELEVANT: Applies beyond this specific case
        NON-REDUNDANT: Not already in CLAUDE.md
        ACTIONABLE: Can be applied in future work
        EVIDENCE-BASED: Proven by this experience

    IF significant learnings exist:

        READ CLAUDE.md

        APPEND to "## Implementation Learnings" section:

        ### Error Patterns to Avoid

        {IF new error pattern identified:}
        - **{Pattern Name}**: {Description of pattern}
          - **Why Problematic**: {Explanation}
          - **Evidence**: CR-{SYSTEM}-{NNN} - {what went wrong}
          - **Prevention**: {How to avoid}

        ### Debugging Strategies

        {IF new debugging strategy proven effective:}
        - **{Strategy Name}**: {Description of strategy}
          - **When to Use**: {Situation}
          - **How to Apply**: {Steps}
          - **Evidence**: CR-{SYSTEM}-{NNN} - {how it helped}

        ### Code Quality Rules

        {IF new quality rule learned:}
        - **{Rule Name}**: {Description of rule}
          - **Rationale**: {Why this matters}
          - **Evidence**: CR-{SYSTEM}-{NNN} - {lesson learned}
          - **Application**: {How to apply in future}

        LOG:
            ✅ CLAUDE.md updated with learnings from CR-{NNN}

    ELSE:
        LOG:
            ℹ️ No significant learnings to add to CLAUDE.md

    # ──────────────────────────────────────────────────────────
    # README / Component Documentation
    # ──────────────────────────────────────────────────────────

    FOR each affected file:

        IF new functionality added:
            # Update README if public API changed
            IF file in public API:
                READ README.md
                UPDATE feature list or usage examples
                LOG:
                    ✅ README.md updated for {file}

        IF component behavior changed:
            # Update _readme.md (inline docs pattern)
            component_readme = "{component_dir}/{component_name}_readme.md"

            IF component_readme exists:
                UPDATE component_readme with new behavior
            ELSE:
                # Follow inline-docs.md convention
                CREATE component_readme following template

            LOG:
                ✅ Component documentation updated for {component}
```

#### Step 8.3: Update Registries

```bash
LOG:
    📋 Updating registries...

# ──────────────────────────────────────────────────────────────
# task_registry.json
# ──────────────────────────────────────────────────────────────

READ Implementation_{SYSTEM_NAME}/registry/task_registry.json

FOR each task affected by CR:

    UPDATE task entry:
    {
        "T-{NNN}": {
            ...existing fields...
            "status": "modified_for_cr",  # or keep existing if just related
            "change_requests": ["CR-{SYSTEM}-{NNN}"],
            "modified_at": "{ISO timestamp}",
            "verification": "{updated verification notes}"
        }
    }

WRITE task_registry.json

LOG:
    ✅ task_registry.json updated

# ──────────────────────────────────────────────────────────────
# implementation_traceability_register.json
# ──────────────────────────────────────────────────────────────

READ Implementation_{SYSTEM_NAME}/traceability/implementation_traceability_register.json

FOR each new code → test trace:

    ADD trace entry:
    {
        "trace_id": "TRACE-{NNN}",
        "source": {
            "type": "code",
            "id": "{file_path}",
            "function": "{function_name}"
        },
        "target": {
            "type": "test",
            "id": "{test_file_path}",
            "test_case": "{test_name}"
        },
        "created_by": "CR-{SYSTEM}-{NNN}",
        "created_at": "{ISO timestamp}"
    }

WRITE implementation_traceability_register.json

LOG:
    ✅ implementation_traceability_register.json updated

# ──────────────────────────────────────────────────────────────
# change_request_registry.json
# ──────────────────────────────────────────────────────────────

READ Implementation_{SYSTEM_NAME}/change-requests/change_request_registry.json

UPDATE CR entry:
{
    "CR-{SYSTEM}-{NNN}": {
        ...existing fields...
        "status": "completed",
        "completed_at": "{ISO timestamp}",
        "files_changed": ["{list of files}"],
        "tests_added": ["{list of test files}"],
        "task_refs": ["{T-NNN references}"],
        "learnings_captured": {true/false},
        "pdca_cycles": {cycle_count},
        "validation_score": {consensus_score},
        "duration_minutes": {total_duration}
    }
}

WRITE change_request_registry.json

LOG:
    ✅ change_request_registry.json updated

# ──────────────────────────────────────────────────────────────
# Version History (already logged in Phase 6, but summarize)
# ──────────────────────────────────────────────────────────────

READ traceability/{SYSTEM_NAME}_version_history.json

VERIFY all changes from Phase 6 are logged

LOG:
    ✅ All registries and version history updated
```

#### Step 8.4: MEMORIZE - Harvest Insights (REFLEXION)

```bash
REFLEXION MEMORIZE PHASE:

═══════════════════════════════════════════════════════════════
         REFLEXION: MEMORIZE (HARVEST INSIGHTS)
═══════════════════════════════════════════════════════════════

Step 1: HARVEST insights from this CR
──────────────────────────────────────────────────────────────

REVIEW all CR documents:
    - CHANGE_REQUEST.md
    - ANALYSIS.md
    - IMPLEMENTATION_PLAN.md
    - IMPLEMENTATION_LOG.md
    - VALIDATION_REPORT.md

EXTRACT insights:

1. What went wrong (root cause)?
   {Root cause from analysis}

2. How was it missed originally?
   {Why 4 and Why 5 from analysis}

3. What patterns should be avoided?
   {Anti-patterns identified during implementation}

4. What patterns worked well?
   {Successful techniques from implementation}

5. Process improvements identified?
   {Gaps in workflow, missing quality gates, etc.}

Step 2: CURATE insights
──────────────────────────────────────────────────────────────

FOR each insight:

    EVALUATE against criteria:
        ✓ RELEVANT: Applies beyond this specific case?
        ✓ NON-REDUNDANT: Not already documented in CLAUDE.md?
        ✓ ACTIONABLE: Can be applied in future work?
        ✓ EVIDENCE-BASED: Proven by this experience?

    IF all criteria met:
        MARK as significant learning
    ELSE:
        DISCARD (too specific or already documented)

Step 3: CATEGORIZE significant learnings
──────────────────────────────────────────────────────────────

Error Patterns to Avoid:
- {Pattern 1}: {Description} (from CR-{NNN})
- {Pattern 2}: {Description} (from CR-{NNN})

Debugging Strategies:
- {Technique 1}: {When to use} (proven in CR-{NNN})
- {Technique 2}: {When to use} (proven in CR-{NNN})

Code Quality Rules:
- {Rule 1}: {Rationale} (learned from CR-{NNN})
- {Rule 2}: {Rationale} (learned from CR-{NNN})

Process Improvements:
- {Improvement 1}: {How to apply}
- {Improvement 2}: {How to apply}

Step 4: VALIDATE memory update
──────────────────────────────────────────────────────────────

CHECK coherence:
    ✓ Do new learnings contradict existing content in CLAUDE.md?
    ✓ Are new learnings actionable guidance?
    ✓ Are new learnings not duplicating existing rules?

IF validation passes:
    UPDATE CLAUDE.md as shown in Step 8.2

    LOG:
        ✅ Insights captured and CLAUDE.md updated

ELSE:
    LOG:
        ℹ️ No significant new insights to memorize
        (CR-specific details remain in session folder)

═══════════════════════════════════════════════════════════════
```

#### Step 8.5: Generate SUMMARY.md

```bash
LOG:
    📄 Generating summary...

CREATE {session_folder}/SUMMARY.md:

---
document_id: SUMMARY-CR-{NNN}
version: 1.0.0
created_at: {YYYY-MM-DD HH:MM:SS}
cr_id: CR-{SYSTEM}-{NNN}
status: {completed/abandoned}
---

# Change Request Summary - CR-{SYSTEM}-{NNN}

## Problem

**Type**: {Bug/Improvement/Feedback}
**Severity**: {CRITICAL/HIGH/MEDIUM/LOW}
**Reporter**: {name}
**Date**: {YYYY-MM-DD}

{Brief description of the problem from CHANGE_REQUEST.md}

## Root Cause

**Analysis Method**: {Quick Check/5 Whys/Fishbone/A3 Full}

{Root cause summary from ANALYSIS.md}

{IF 5 Whys:}
    **5 Whys Summary**:
    - Why 1: {immediate cause}
    - Why 2: {deeper cause}
    - Why 3: {design cause}
    - Why 4: {process cause}
    - Why 5: {systemic cause}
{ENDIF}

{IF Fishbone:}
    **Primary Root Causes**:
    - {Cause 1}
    - {Cause 2}
{ENDIF}

## Solution

**Approach**: {Brief description of solution}

**Countermeasures Implemented**:
- Immediate: {immediate fix}
- Short-term: {prevention}
- Long-term: {systemic fix (if applicable)}

## Files Changed

{FOR each file:}
- **{file_path}**: {what changed}
  - Lines: {line_range}
  - Change Type: {MODIFY/CREATE}
{ENDFOR}

**Total Files**: {count}

## Tests Added

{FOR each test:}
- **{test_file_path}**: {what it verifies}
  - Test Cases: {count}
  - Coverage: {coverage_percentage}%
{ENDFOR}

**Total Test Files**: {count}
**Total Test Cases**: {count}

## Validation Results

**Success Criteria**: {✓ ALL PASS | ⚠ SOME FAILED}

{IF passed:}
- {Criterion 1}: ✓ PASS
- {Criterion 2}: ✓ PASS
- {Criterion 3}: ✓ PASS
{ENDIF}

**Hypothesis**: {✓ CONFIRMED | ⚠ PARTIALLY CONFIRMED | ❌ REJECTED}

**Regression Testing**: {✓ NO REGRESSIONS | ❌ REGRESSIONS FOUND}

**Multi-Perspective Validation**:
- Requirements: {score}/10
- Architecture: {score}/10
- Code Quality: {score}/10
- **Consensus**: {average}/10 - {✓ PASS | ⚠ CONDITIONAL | ❌ FAIL}

## Learnings Captured

{IF learnings_captured:}

**Error Patterns Identified**:
- {Pattern 1}

**Debugging Strategies**:
- {Strategy 1}

**Code Quality Insights**:
- {Insight 1}

**CLAUDE.md Updated**: {YES/NO}
{ENDIF}

{IF NOT learnings_captured:}
No significant learnings to memorize (CR-specific details remain in session folder).
{ENDIF}

## Timeline

| Phase | Duration |
|-------|----------|
| Input Collection & Triage | {duration} |
| Impact Analysis (Kaizen) | {duration} |
| Registration | {duration} |
| Approval Gate | {duration} |
| Planning (PDCA Plan) | {duration} |
| Implementation (TDD + PDCA Do) | {duration} |
| Validation (PDCA Check + Reflexion) | {duration} |
| Completion (PDCA Act + Memorize) | {duration} |
| **Total** | **{total_duration}** |

## PDCA Cycles

**Cycles**: {pdca_cycles}

{IF pdca_cycles > 1:}
    **Cycle History**:
    {FOR each cycle:}
    - Cycle {N}: {result} - {learnings}
    {ENDFOR}
{ENDIF}

## Registry Updates

✓ task_registry.json updated
✓ implementation_traceability_register.json updated
✓ change_request_registry.json updated
✓ version history updated

## Related Artifacts

**Traceability Chain**:
{Root cause chain from ANALYSIS.md}

**Source Requirements**:
- {REQ-XXX}: {title}
- {JTBD-X.X}: {title}
- {PP-X.X}: {title}

**Implementation Tasks**:
- {T-NNN}: {title}

---

**Status**: {✅ COMPLETED | ❌ ABANDONED}
**Completed**: {timestamp}
**Total Duration**: {duration}

{IF technical_debt_accepted:}
⚠️ **Technical Debt Accepted**
See VALIDATION_REPORT.md for details.
{ENDIF}

---

## Session Folder Contents

All artifacts for this CR are in:
`Implementation_{SYSTEM_NAME}/change-requests/{date}_CR-{NNN}/`

- CHANGE_REQUEST.md - Original request
- ANALYSIS.md - Kaizen root cause analysis
- IMPLEMENTATION_PLAN.md - PDCA plan with TDD tasks
- IMPLEMENTATION_LOG.md - Execution log
- VALIDATION_REPORT.md - Reflexion validation
- SUMMARY.md - This file

LOG:
    ✅ SUMMARY.md generated
```

#### Step 8.6: Final Logging and Cleanup

```bash
LOG:
    ✅ COMPLETION PHASE FINISHED

# ──────────────────────────────────────────────────────────────
# Log command end
# ──────────────────────────────────────────────────────────────

RUN:
    bash .claude/hooks/log-lifecycle.sh command /htec-sdd-changerequest ended '{"stage": "implementation", "status": "completed"}'

# ──────────────────────────────────────────────────────────────
# Display completion message
# ──────────────────────────────────────────────────────────────

DISPLAY:

═══════════════════════════════════════════════════════════════
           CHANGE REQUEST COMPLETED
═══════════════════════════════════════════════════════════════

✅ CR-{SYSTEM}-{NNN} successfully completed

**Root Cause**: {brief_summary}
**Solution**: {brief_summary}
**Files Changed**: {count}
**Tests Added**: {count}
**Validation Score**: {consensus_score}/10
**Duration**: {total_duration}

**Session Folder**:
Implementation_{SYSTEM_NAME}/change-requests/{date}_CR-{NNN}/

**Key Documents**:
- ANALYSIS.md - Root cause analysis
- IMPLEMENTATION_PLAN.md - What was done
- VALIDATION_REPORT.md - Quality assessment
- SUMMARY.md - Complete summary

{IF learnings_captured:}
**Learnings**: Captured in CLAUDE.md
{ENDIF}

{IF technical_debt_accepted:}
⚠️ **Technical Debt**: See VALIDATION_REPORT.md
{ENDIF}

═══════════════════════════════════════════════════════════════

NEXT STEPS:
- Review summary in SUMMARY.md
- Merge changes if not already merged
- Deploy to staging for final verification
- Close related tickets/issues

═══════════════════════════════════════════════════════════════
```

OUTPUT Phase 8:
    - PDCA ACT decision (standardize or iterate)
    - Documentation updated (CLAUDE.md, README, component docs)
    - Registries updated (task, traceability, change request)
    - Insights harvested and memorized
    - SUMMARY.md generated
    - CR marked as completed in registry
    - Final completion message displayed
```

---

## Output Structure

```
Implementation_{SYSTEM_NAME}/change-requests/
├── change_request_registry.json       # All CRs with status
├── _working/                          # Temporary working folder
│   └── ANALYSIS.md                    # Analysis in progress
└── {YYYY-MM-DD}_CR-{NNN}/             # Completed CR session
    ├── CHANGE_REQUEST.md              # Original request
    ├── ANALYSIS.md                    # Kaizen root cause analysis
    ├── IMPLEMENTATION_PLAN.md         # PDCA plan with TDD tasks
    ├── IMPLEMENTATION_LOG.md          # Execution log
    ├── VALIDATION_REPORT.md           # Reflexion validation
    └── SUMMARY.md                     # Final summary
```

## Example: Complete CR Session

See the end of this document for a comprehensive example of all phases for a real bug fix.

---

## Related Commands

- `/htec-sdd-implement` - For new feature implementation (not change requests)
- `/htec-sdd-review` - Code review after changes
- `/htec-sdd-status` - Check overall implementation progress
- `/integrity-check` - Cross-stage validation

---

## Appendix: Complete Example

**Example CR**: Barcode scanner timeout bug

{This section would contain a full example showing all 8 phases, all documents generated, and the complete workflow from initial bug report through to completion with learnings captured}

{Full example omitted here for brevity but would follow the exact pattern specified above}

---

**Command Version**: 2.0.0 (Reflexion-Enhanced)
**Last Updated**: 2026-01-25
**Methodology**: Kaizen + PDCA + Reflexion + TDD
