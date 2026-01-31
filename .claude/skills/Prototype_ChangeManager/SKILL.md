---
name: managing-prototype-changes
description: Use when you need to manage controlled changes to a prototype based on feedback, including impact analysis, variant proposals, and systematic debugging.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill managing-prototype-changes started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill managing-prototype-changes ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill managing-prototype-changes instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

# Manage Prototype Changes

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_ChangeManager
- **Version**: 2.3.1
- **Created**: 2024-12-13
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3

## Description
Manage controlled changes to a built prototype based on user feedback. Provides structured analysis, impact assessment, implementation variants, and maintains full traceability through requirements, progress tracking, and decomposition updates.

> **DEBUGGING ENFORCEMENT**: For Bug-type changes, this skill follows the Iron Law of Debugging - NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST. Random fixes waste time and create new bugs.

## Execution Logging (MANDATORY)

This skill logs all execution to the global pipeline progress registry. Logging is automatic and requires no manual configuration.

### How Logging Works

Every execution of this skill is logged to `_state/lifecycle.json`:

- **start_event**: Logged when skill execution begins
- **end_event**: Logged when skill execution completes

Events include:
- skill_name, intent, stage, system_name
- start/end timestamps
- status (completed/failed)
- output files created (change management reports)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "managing-prototype-changes"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "managing-prototype-changes" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## Roles & Responsibilities

This skill embodies multiple expert perspectives:

| Role | Responsibilities |
|------|------------------|
| **Project Manager** | Session tracking, change batching, planning, progress |
| **Product Expert** | Requirements analysis, user need alignment |
| **Risk Manager** | Impact analysis, dependency chains, risk scoring |
| **QA Specialist** | Regression scope, validation, acceptance criteria |
| **UX Designer** | Interaction improvements, user flow optimization |
| **UI Expert** | Component/screen changes, visual consistency |
| **Technology Lead** | Technical feasibility, implementation approach |

---

## Procedure

### Phase 1: Feedback Session Initialization

#### Step 1.1: Create or Resume Feedback Session
```
CHECK _state/feedback_sessions.json exists:
  IF not exists:
    CREATE {
      version: "1.0",
      sessions: [],
      change_requests: [],
      summary: { total_sessions: 0, total_changes: 0 }
    }

PROMPT user:
  ═══════════════════════════════════════════
  📋 FEEDBACK SESSION
  ═══════════════════════════════════════════
  
  Starting new feedback session or resuming?
  
  1. "new session" - Start fresh feedback session
  2. "resume [session_id]" - Continue existing session
  3. "list sessions" - Show all sessions
  ═══════════════════════════════════════════

IF new session:
  CREATE session = {
    session_id: "FS-{YYYY-MM-DD}-{seq}",
    created_at: timestamp,
    status: "active",
    feedback_items: [],
    change_requests: [],
    metrics: {
      items_received: 0,
      changes_implemented: 0,
      changes_pending: 0
    }
  }
  
  LOG: "Created feedback session: {session_id}"
```

#### Step 1.2: Create Backup Before Any Changes
```
CREATE backup:
  backup_id: "BK-{session_id}-{timestamp}"
  backup_path: "_backups/{backup_id}/"
  
  COPY:
    - _state/ → _backups/{backup_id}/_state/
    - outputs/ → _backups/{backup_id}/outputs/
    - src/ → _backups/{backup_id}/src/
    
  RECORD in _state/backups.json:
    {
      backup_id: backup_id,
      session_id: session_id,
      created_at: timestamp,
      files_backed_up: count,
      size_mb: size
    }

LOG: "Backup created: {backup_id}"
DISPLAY: "Rollback available via: rollback to {backup_id}"
```

### Phase 2: Feedback Capture & Structuring

#### Step 2.1: Load Feedback Input
```
EXPECT structured feedback in discovery format:
  READ discovery/feedback/FEEDBACK_SESSION_{date}.md
  
  OR accept inline structured input:
    ═══════════════════════════════════════════
    📝 FEEDBACK INPUT
    ═══════════════════════════════════════════
    
    Please provide feedback in this format:
    
    ## Feedback Item 1
    **Type**: [Bug | Enhancement | New Feature | UX Issue | Visual Issue]
    **Screen/Component**: [affected area]
    **Description**: [what was observed]
    **User Quote**: [verbatim if available]
    **Severity**: [Critical | High | Medium | Low]
    **Suggested Solution**: [if user proposed one]
    
    ## Feedback Item 2
    ...
    ═══════════════════════════════════════════
```

#### Step 2.2: Parse & Structure Feedback Items
```
FOR each feedback item:
  CREATE feedback_entry = {
    item_id: "FI-{session}-{seq}",
    type: parsed_type,
    affected_area: parsed_screen_or_component,
    description: parsed_description,
    user_quote: parsed_quote,
    severity: parsed_severity,
    suggested_solution: parsed_suggestion,
    status: "new",
    created_at: timestamp
  }
  
  ADD to session.feedback_items[]
  
LOG: "Parsed {count} feedback items"
```

#### Step 2.3: Group Related Feedback
```
ANALYZE feedback items for relationships:
  - Same screen → group
  - Same component → group
  - Same user flow → group
  - Conflicting feedback → flag for clarification
  
CREATE feedback_groups[]:
  {
    group_id: "FG-{session}-{seq}",
    theme: "Pipeline screen usability",
    items: [FI-001, FI-003, FI-007],
    combined_severity: highest_in_group
  }

DISPLAY grouping for confirmation:
  ═══════════════════════════════════════════
  📊 FEEDBACK GROUPING
  ═══════════════════════════════════════════
  
  Group 1: Pipeline Screen Usability
  ├─ FI-001: Drag-drop not intuitive (High)
  ├─ FI-003: Stage names confusing (Medium)
  └─ FI-007: Can't see candidate count (Low)
  
  Group 2: Candidate Card Design
  ├─ FI-002: Cards too small on mobile (High)
  └─ FI-005: Missing status indicator (Medium)
  
  Ungrouped:
  └─ FI-004: Want dark mode (Low) - New Feature
  
  Is this grouping correct?
  1. "confirm" - Proceed with grouping
  2. "merge [G1] [G2]" - Combine groups
  3. "split [G1] [item]" - Move item to own group
  4. "regroup" - Let me redefine groups
  ═══════════════════════════════════════════
  
  WAIT for user response
```

### Phase 3: Change Request Creation

#### Step 3.1: Convert Feedback Groups to Change Requests
```
FOR each feedback_group (or ungrouped item):
  
  LOG_PROMPT:
    skill: "Prototype_ChangeManager"
    step: "Step 3.1: Create Change Request"
    desired_outcome: "Convert feedback group to structured change request"
    category: "analysis"
    
  CREATE change_request = {
    cr_id: "CR-{YYYY-MM-DD}-{seq}",
    session_id: session_id,
    title: derived_from_feedback,
    description: consolidated_description,
    source_feedback: [item_ids],
    type: Bug | Enhancement | NewFeature | UXImprovement | VisualFix,
    requested_by: "User Feedback Session",
    created_at: timestamp,
    status: "draft"
  }
```

#### Step 3.2: Auto-Classify Change Size
```
ANALYZE change_request for size classification:

  FACTORS:
    - Number of screens affected
    - Number of components affected
    - Data model changes required
    - API changes required
    - New requirements needed
    - Estimated effort
    
  CLASSIFICATION RULES:
    SMALL:
      - Affects ≤1 screen
      - Affects ≤2 components
      - No data model changes
      - No API changes
      - Effort < 2 hours
      
    MEDIUM:
      - Affects 2-4 screens
      - Affects 3-5 components
      - Minor data model changes
      - Minor API changes
      - Effort 2-8 hours
      
    LARGE:
      - Affects 5+ screens
      - Affects 6+ components
      - Significant data model changes
      - New API endpoints
      - Effort > 8 hours
      - OR introduces new feature

  ASSIGN size_classification with confidence score

DISPLAY for confirmation:
  ═══════════════════════════════════════════
  📏 CHANGE SIZE CLASSIFICATION
  ═══════════════════════════════════════════
  
  CR-2024-12-14-001: "Improve Pipeline Drag-Drop"
  
  Auto-classification: MEDIUM (confidence: 85%)
  
  Reasoning:
  ├─ Screens affected: 2 (Pipeline, Dashboard)
  ├─ Components affected: 3 (KanbanBoard, CandidateCard, DropZone)
  ├─ Data model: No changes
  ├─ API: No changes
  └─ Estimated effort: 4-6 hours
  
  Is this classification correct?
  1. "confirm" - Accept MEDIUM
  2. "small" - Reclassify as SMALL
  3. "large" - Reclassify as LARGE
  4. "details" - Show more analysis
  ═══════════════════════════════════════════
  
  WAIT for user response
  UPDATE change_request.size = confirmed_size
```

### Phase 4: Impact Analysis (Full Regression Scope)

#### Step 4.1: Direct Impact Analysis
```
LOG_PROMPT:
  skill: "Prototype_ChangeManager"
  step: "Step 4.1: Direct Impact Analysis"
  desired_outcome: "Identify all artifacts directly touched by this change"
  category: "analysis"

READ all relevant state files:
  - _state/requirements_registry.json
  - _state/data_model.json
  - outputs/02-components/COMPONENT_INDEX.md
  - outputs/03-screens/SCREEN_INDEX.md
  - outputs/05-sequence/sequence.json

FOR change_request:
  IDENTIFY direct_impact:
    affected_components: [list with reasons]
    affected_screens: [list with reasons]
    affected_requirements: [list - which reqs touch this area]
    data_model_changes: [entities/fields affected]
    api_changes: [endpoints affected]
    
  CREATE direct_impact_map
```

#### Step 4.2: Cascading Impact Analysis
```
FOR each item in direct_impact:
  TRACE dependencies:
    - Components that USE this component
    - Screens that USE this component
    - Requirements that DEPEND on this
    - Data entities that REFERENCE this
    - API endpoints that USE this entity
    
  BUILD cascading_impact_tree:
    {
      "KanbanBoard": {
        "direct": true,
        "used_by_screens": ["Pipeline", "Dashboard"],
        "used_by_components": ["BoardContainer"],
        "requirements": ["PP-001", "US-003"]
      }
    }
```

#### Step 4.3: Full Regression Scope
```
ANALYZE cascading_impact_tree:
  IDENTIFY all potentially affected areas:
    - All screens in cascade
    - All components in cascade  
    - All requirements in cascade
    - All test scenarios affected
    
  CALCULATE regression_scope:
    {
      must_test: [critical paths],
      should_test: [related paths],
      optional_test: [tangentially related]
    }

CALCULATE risk_score:
  FACTORS:
    - Number of P0 requirements affected
    - Number of critical screens affected
    - Data integrity risk
    - User flow disruption potential
    
  SCORE: Low (1-3) | Medium (4-6) | High (7-8) | Critical (9-10)
```

#### Step 4.4: Display Full Impact Report
```
DISPLAY:
  ═══════════════════════════════════════════════════════════════
  🎯 IMPACT ANALYSIS: CR-2024-12-14-001
  ═══════════════════════════════════════════════════════════════
  
  ## Direct Impact
  
  | Type | Affected | Reason |
  |------|----------|--------|
  | Component | KanbanBoard | Drag-drop logic changes |
  | Component | CandidateCard | Drop target indicators |
  | Component | DropZone | New component needed |
  | Screen | Pipeline | Primary location |
  | Screen | Dashboard | Mini-pipeline widget |
  
  ## Cascading Impact
  
  KanbanBoard
  └─► Used by: Pipeline, Dashboard
      └─► Requirements: PP-001, US-003, JTBD-001
          └─► Tests: 12 scenarios affected
  
  ## Regression Scope
  
  | Priority | Area | Scenarios |
  |----------|------|-----------|
  | MUST TEST | Pipeline drag-drop | 5 |
  | MUST TEST | Dashboard widget | 2 |
  | SHOULD TEST | Candidate flow | 3 |
  | OPTIONAL | Search/filter | 2 |
  
  ## Risk Assessment
  
  | Factor | Score | Notes |
  |--------|-------|-------|
  | P0 Requirements | 3/10 | 2 P0 reqs affected |
  | Critical Screens | 4/10 | Pipeline is core |
  | Data Integrity | 1/10 | No data changes |
  | User Flow | 5/10 | Core interaction |
  | **Overall Risk** | **MEDIUM (4.2)** | |
  
  ## Effort Estimate
  
  | Phase | Hours | Notes |
  |-------|-------|-------|
  | Design | 1-2 | UX refinement |
  | Implementation | 3-4 | Component updates |
  | Testing | 1-2 | Regression suite |
  | **Total** | **5-8 hours** | |
  
  ═══════════════════════════════════════════════════════════════
  
  Proceed with implementation planning?
  1. "plan" - Generate implementation variants
  2. "clarify: [question]" - Need more information
  3. "defer" - Move to backlog
  4. "reject: [reason]" - Won't implement
  ═══════════════════════════════════════════════════════════════
  
  WAIT for user response
```

### Phase 4.5: Systematic Debugging (FOR BUGS ONLY)

> **MANDATORY FOR BUG-TYPE CHANGES**: This phase MUST be completed before proposing any fix variants.

#### The Debugging Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 4.5, you cannot propose fix variants for bugs.

#### Step 4.5.1: Determine if Debugging Required
```
IF change_request.type == "Bug":

  LOG: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  LOG: "🔍 SYSTEMATIC DEBUGGING REQUIRED"
  LOG: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  debugging_required = TRUE
  fix_attempts = 0

ELSE:
  debugging_required = FALSE
  SKIP to Phase 5
```

#### Step 4.5.2: Root Cause Investigation (Phase 1 of Debugging)
```
IF debugging_required:

  DISPLAY:
    ═══════════════════════════════════════════════════════════════
    🔍 ROOT CAUSE INVESTIGATION: CR-{cr_id}
    ═══════════════════════════════════════════════════════════════

    Bug Report:
    • Screen/Component: {affected_area}
    • Description: {description}
    • User Quote: "{user_quote}"

    ═══════════════════════════════════════════════════════════════

  // 1. READ ERROR MESSAGES CAREFULLY
  GATHER error_details:
    - Console errors (if available)
    - Error messages shown to user
    - Stack traces (if available)
    - Browser/environment details

  LOG: "Step 1: Reading error messages..."

  IF error_details available:
    ANALYZE error messages:
      - Note exact error text
      - Note line numbers, file paths
      - Note error codes
      - Check if error message suggests solution

  // 2. REPRODUCE CONSISTENTLY
  LOG: "Step 2: Attempting reproduction..."

  CREATE reproduction_steps:
    1. Start from: {starting_state}
    2. Navigate to: {screen}
    3. Perform: {action}
    4. Expected: {expected_result}
    5. Actual: {actual_result}

  VERIFY:
    - Can trigger bug reliably?
    - What are exact steps?
    - Does it happen every time?
    - If not reproducible → gather more data, DO NOT GUESS

  // 3. CHECK RECENT CHANGES
  LOG: "Step 3: Checking recent changes..."

  ANALYZE change_history:
    - Last code changes to affected area
    - Recent dependency updates
    - Recent configuration changes
    - Environmental differences

  IF recent change found:
    correlation_strength: HIGH | MEDIUM | LOW
    correlation_reason: "{explanation}"

  // 4. TRACE DATA FLOW
  LOG: "Step 4: Tracing data flow..."

  TRACE from symptom backwards:
    symptom: "{what user observed}"
    immediate_cause: "{what code directly causes this}"

    KEEP asking "What called this?" until source found:
      level_1: {function/component} → called by
      level_2: {function/component} → called by
      level_3: {function/component} → THIS IS THE SOURCE

  RECORD root_cause_investigation = {
    error_messages: [...],
    reproduction: {steps, consistency},
    recent_changes: [...],
    data_flow_trace: [...],
    suspected_root_cause: "{description}",
    confidence: HIGH | MEDIUM | LOW
  }
```

#### Step 4.5.3: Pattern Analysis (Phase 2 of Debugging)
```
LOG: "Step 5: Analyzing patterns..."

// Find working examples
SEARCH codebase for:
  - Similar working code
  - Same pattern used elsewhere
  - Reference implementations

IF working_examples found:
  COMPARE:
    - What's different between working and broken?
    - List every difference, however small
    - Don't assume "that can't matter"

  differences[] = [
    { aspect: "...", working: "...", broken: "...", significance: HIGH|MED|LOW }
  ]

// Understand dependencies
IDENTIFY:
  - What other components does this need?
  - What settings, config, environment?
  - What assumptions does it make?

RECORD pattern_analysis = {
  working_examples: [...],
  differences: [...],
  dependencies: [...],
  pattern_violations: [...] // if any
}
```

#### Step 4.5.4: Hypothesis Formation (Phase 3 of Debugging)
```
LOG: "Step 6: Forming hypothesis..."

BASED on investigation + pattern analysis:

  CREATE hypothesis = {
    statement: "I think {X} is the root cause because {Y}",
    evidence: [...supporting evidence...],
    confidence: HIGH | MEDIUM | LOW,
    testable: true/false,
    test_method: "To verify, I would..."
  }

DISPLAY:
  ═══════════════════════════════════════════════════════════════
  🎯 ROOT CAUSE HYPOTHESIS
  ═══════════════════════════════════════════════════════════════

  Statement:
  "{hypothesis.statement}"

  Supporting Evidence:
  • {evidence_1}
  • {evidence_2}
  • {evidence_3}

  Confidence: {confidence}

  To Verify:
  {test_method}

  ═══════════════════════════════════════════════════════════════

  Is this hypothesis correct?
  1. "confirm" - Proceed with fix based on this root cause
  2. "test" - Let me verify the hypothesis first
  3. "different: [theory]" - I think the cause is something else
  4. "investigate more" - Need more information
  ═══════════════════════════════════════════════════════════════

  WAIT for user response

IF hypothesis rejected or needs more investigation:
  RETURN to Step 4.5.2 with new information
```

#### Step 4.5.5: Record Debugging Evidence
```
CREATE debugging_evidence = {
  cr_id: cr_id,
  bug_type: classification,

  investigation: {
    error_messages: root_cause_investigation.error_messages,
    reproduction: root_cause_investigation.reproduction,
    data_flow_trace: root_cause_investigation.data_flow_trace
  },

  analysis: {
    working_examples: pattern_analysis.working_examples,
    differences: pattern_analysis.differences,
    pattern_violations: pattern_analysis.pattern_violations
  },

  hypothesis: {
    statement: hypothesis.statement,
    evidence: hypothesis.evidence,
    confidence: hypothesis.confidence,
    confirmed_by_user: true/false
  },

  root_cause_identified: true,
  root_cause_description: "{clear description of root cause}",

  timestamp: NOW()
}

SAVE to change_request.debugging_evidence

LOG: "✅ Root cause investigation complete"
LOG: "Root cause: {root_cause_description}"
```

#### Step 4.5.6: Prevent Fix Thrashing
```
// Track fix attempts to prevent endless fix cycles

IF this change_request has previous fix attempts:
  fix_attempts = change_request.fix_history.length

  IF fix_attempts >= 3:
    ═══════════════════════════════════════════
    ⚠️ ARCHITECTURAL REVIEW REQUIRED
    ═══════════════════════════════════════════

    This bug has had {fix_attempts} fix attempts:
    • Fix 1: {description} - Result: {failed_reason}
    • Fix 2: {description} - Result: {failed_reason}
    • Fix 3: {description} - Result: {failed_reason}

    Pattern indicates ARCHITECTURAL problem, not bug.

    Each fix revealed new issues in different places.
    This suggests fundamental design flaw.

    Options:
    1. "redesign: [area]" - Propose architectural change
    2. "escalate" - Flag for technical review
    3. "workaround" - Implement workaround with tech debt note
    4. "defer" - Move to backlog for major refactor
    ═══════════════════════════════════════════

    WAIT for user response

    DO NOT attempt Fix #4 without architectural discussion
```

---

### Phase 5: Clarification (If Needed)

#### Step 5.1: Generate Clarification Questions
```
IF change_request has ambiguity OR user requested clarification:
  
  ANALYZE for gaps:
    - Unclear user intent
    - Multiple interpretations possible
    - Missing technical details
    - Conflicting requirements
    - Edge cases undefined
    
  GENERATE questions as each expert role:
    
    AS Product Expert:
      - "Should this apply to all candidate types or only active?"
      
    AS UX Designer:
      - "Preferred drop indicator: highlight zone or ghost preview?"
      
    AS Technology Lead:
      - "Real-time sync needed or batch update acceptable?"
      
    AS QA Specialist:
      - "What's the expected behavior for invalid drops?"

DISPLAY:
  ═══════════════════════════════════════════
  ❓ CLARIFICATION NEEDED
  ═══════════════════════════════════════════
  
  Before proposing solutions, please clarify:
  
  1. [Product] Should drag-drop work for archived 
     candidates too, or only active pipeline?
     
  2. [UX] When dragging, should we show:
     a) Highlighted drop zone
     b) Ghost preview of card
     c) Both
     
  3. [Tech] If user's connection drops mid-drag:
     a) Auto-retry when reconnected
     b) Show error, require manual retry
     c) Optimistic update (assume success)
     
  4. [QA] If card is dropped on invalid stage:
     a) Snap back with error message
     b) Show "not allowed" cursor, prevent drop
     c) Allow drop but show warning
  
  Please answer: "1a, 2c, 3b, 4b" or provide details
  ═══════════════════════════════════════════
  
  WAIT for user response
  RECORD clarifications in change_request.clarifications[]
```

### Phase 6: Implementation Variants (For MEDIUM/LARGE Changes)

#### Step 6.1: Generate Three Variants
```
IF change_request.size in [MEDIUM, LARGE]:
  
  LOG_PROMPT:
    skill: "Prototype_ChangeManager"
    step: "Step 6.1: Generate Variants"
    desired_outcome: "Create 3 distinct implementation approaches"
    category: "generation"
  
  GENERATE variants based on change type:
  
  FOR UX/Interaction changes:
    - Variant A: Conservative (minimal UI change, behavior focus)
    - Variant B: Enhanced (improved UX with moderate changes)
    - Variant C: Redesigned (optimal UX, more extensive changes)
    
  FOR Bug fixes:
    // REQUIRES: Phase 4.5 debugging evidence must exist
    IF NOT change_request.debugging_evidence:
      ═══════════════════════════════════════════
      ❌ CANNOT GENERATE FIX VARIANTS
      ═══════════════════════════════════════════

      Root cause investigation (Phase 4.5) was not completed.

      You MUST identify the root cause before proposing fixes.
      Random fixes waste time and create new bugs.

      Action: Return to Phase 4.5 and complete debugging.
      ═══════════════════════════════════════════

      BLOCK - DO NOT PROCEED

    // Generate variants based on CONFIRMED root cause
    root_cause = change_request.debugging_evidence.root_cause_description

    - Variant A: Quick fix (address symptom at point of failure)
      - Fixes: where bug manifests
      - Risk: root cause remains, may recur
      - Use when: time-critical, temporary solution

    - Variant B: Proper fix (address confirmed root cause)
      - Fixes: {root_cause} at source
      - Risk: low - addresses actual problem
      - Use when: standard approach, recommended

    - Variant C: Preventive fix (fix root cause + add defenses)
      - Fixes: {root_cause} at source
      - PLUS: validation at each layer (defense-in-depth)
      - PLUS: regression test covering this case
      - Risk: lowest - prevents recurrence
      - Use when: critical paths, recurring issues
    
  FOR New features:
    - Variant A: MVP (minimum viable implementation)
    - Variant B: Standard (full feature as requested)
    - Variant C: Enhanced (feature + related improvements)
    
  FOR Visual changes:
    - Variant A: Minimal (targeted visual fix)
    - Variant B: Consistent (fix + align related elements)
    - Variant C: Systematic (update design system if needed)
```

#### Step 6.2: Detail Each Variant
```
FOR each variant:
  CREATE variant_spec = {
    variant_id: "V{A|B|C}",
    name: descriptive_name,
    approach: description,
    
    changes: {
      components: [
        { name: "KanbanBoard", action: "modify", details: "..." },
        { name: "DropZone", action: "create", details: "..." }
      ],
      screens: [
        { name: "Pipeline", action: "modify", details: "..." }
      ],
      requirements: {
        new: ["FR-NEW-001: Drag-drop feedback"],
        modified: ["PP-001: Enhanced with drag-drop"],
        linked: ["US-003", "JTBD-001"]
      },
      data_model: [],
      api: []
    },
    
    pros: [list],
    cons: [list],
    
    effort: {
      design: hours,
      implementation: hours,
      testing: hours,
      total: hours
    },
    
    risk_delta: "Reduces overall risk by X" | "Increases risk by Y",
    
    skills_to_invoke: ["Components", "Screens", "CodeGen"],
    
    implementation_steps: [ordered list]
  }
```

#### Step 6.3: Present Variants for Selection
```
DISPLAY:
  ═══════════════════════════════════════════════════════════════
  🔀 IMPLEMENTATION VARIANTS: CR-2024-12-14-001
  ═══════════════════════════════════════════════════════════════
  
  ## Variant A: "Quick Enhancement"
  
  **Approach**: Add visual feedback to existing drag-drop without 
  restructuring. Uses CSS transitions and existing event handlers.
  
  **Changes**:
  ├─ Modify: KanbanBoard (add drop highlighting)
  ├─ Modify: CandidateCard (add dragging state)
  └─ No new components
  
  **Requirements**:
  └─ Link: PP-001, US-003 (enhanced)
  
  | Pros | Cons |
  |------|------|
  | Fast to implement (3h) | Limited UX improvement |
  | Low risk | Doesn't address all feedback |
  | No new dependencies | May need revisiting |
  
  **Effort**: 3 hours | **Risk**: Low ↓
  
  ─────────────────────────────────────────────────────────────────
  
  ## Variant B: "Proper Solution" ⭐ RECOMMENDED
  
  **Approach**: Create dedicated DropZone component with proper 
  visual states. Implement ghost preview during drag. Add 
  keyboard support for accessibility.
  
  **Changes**:
  ├─ Modify: KanbanBoard (integrate DropZone)
  ├─ Modify: CandidateCard (draggable wrapper)
  ├─ Create: DropZone (new component)
  └─ Modify: Pipeline screen (updated interactions)
  
  **Requirements**:
  ├─ New: FR-2024-12-001 "Drag-drop visual feedback"
  ├─ New: A11Y-NEW-001 "Keyboard drag-drop"
  └─ Link: PP-001, US-003, JTBD-001
  
  | Pros | Cons |
  |------|------|
  | Addresses all feedback | Moderate effort (6h) |
  | Accessible | New component to maintain |
  | Reusable pattern | Requires testing |
  
  **Effort**: 6 hours | **Risk**: Medium →
  
  ─────────────────────────────────────────────────────────────────
  
  ## Variant C: "Full Redesign"
  
  **Approach**: Redesign Kanban interaction model. Add multi-select
  drag, bulk operations, undo/redo support, and real-time 
  collaboration indicators.
  
  **Changes**:
  ├─ Major Modify: KanbanBoard (new interaction model)
  ├─ Create: DropZone, SelectionManager, UndoStack
  ├─ Modify: Pipeline, Dashboard screens
  └─ API: New endpoint for bulk moves
  
  **Requirements**:
  ├─ New: FR-2024-12-001 through FR-2024-12-005
  ├─ New: A11Y-NEW-001, A11Y-NEW-002
  └─ Link: PP-001, PP-002, US-003, JTBD-001
  
  | Pros | Cons |
  |------|------|
  | Best UX | High effort (16h) |
  | Future-proof | Scope creep risk |
  | Power user features | Requires API changes |
  
  **Effort**: 16 hours | **Risk**: High ↑
  
  ═══════════════════════════════════════════════════════════════
  
  Select variant:
  1. "A" - Quick Enhancement
  2. "B" - Proper Solution (recommended)
  3. "C" - Full Redesign
  4. "compare [A] [B]" - Detailed comparison
  5. "customize" - Mix elements from variants
  ═══════════════════════════════════════════════════════════════
  
  WAIT for user response
  RECORD selected_variant in change_request
```

### Phase 7: Requirements Management

#### Step 7.1: Create/Link Requirements
```
BASED on selected_variant:
  
  FOR each new requirement identified:
    IF truly new feature:
      CREATE new requirement:
        id: "FR-{YYYY-MM}-{seq}" or "A11Y-{YYYY-MM}-{seq}"
        type: derived from change type
        description: from variant spec
        priority: inherit from change_request severity
        source: "CR-{cr_id}"
        addressed_by: [] (will be populated during implementation)
        
      ADD to _state/requirements_registry.json
      
    IF enhancement to existing:
      FIND existing requirement
      CREATE sub-requirement or enhancement note:
        parent_id: existing_id
        enhancement: description
        source: "CR-{cr_id}"
        
      UPDATE existing requirement.enhancements[]
      
  FOR each existing requirement affected:
    LINK change_request to requirement:
      ADD cr_id to requirement.change_history[]
      
LOG: "Created {new_count} requirements, linked {link_count} existing"

DISPLAY:
  ═══════════════════════════════════════════
  📋 REQUIREMENTS UPDATES
  ═══════════════════════════════════════════
  
  New Requirements Created:
  ├─ FR-2024-12-001: Drag-drop visual feedback (P1)
  └─ A11Y-2024-12-001: Keyboard drag-drop support (P0)
  
  Existing Requirements Enhanced:
  ├─ PP-001: Added "with visual feedback" to acceptance
  └─ US-003: Added drag-drop scenario
  
  Requirements Linked:
  └─ JTBD-001: Linked to CR-2024-12-14-001
  
  Registry updated ✓
  ═══════════════════════════════════════════
```

### Phase 8: Implementation Planning

#### Step 8.1: Generate Implementation Plan
```
CREATE implementation_plan = {
  plan_id: "IP-{cr_id}",
  variant: selected_variant,
  
  steps: [
    {
      step: 1,
      action: "Create DropZone component spec",
      skill: "manual" | "Components",
      surgical: true,
      target: "outputs/02-components/DropZone.md",
      estimated_time: "30min",
      requirements: ["FR-2024-12-001", "A11Y-2024-12-001"]
    },
    {
      step: 2,
      action: "Update KanbanBoard spec",
      skill: "manual",
      surgical: true,
      target: "outputs/02-components/KanbanBoard.md",
      changes: ["Add DropZone integration", "Update states"],
      estimated_time: "20min"
    },
    {
      step: 3,
      action: "Update Pipeline screen spec",
      skill: "manual",
      surgical: true,
      target: "outputs/03-screens/Pipeline.md",
      changes: ["Update interactions section"],
      estimated_time: "15min"
    },
    {
      step: 4,
      action: "Implement DropZone component",
      skill: "CodeGen",
      surgical: true,
      target: "src/components/DropZone.jsx",
      estimated_time: "1h"
    },
    {
      step: 5,
      action: "Update KanbanBoard implementation",
      skill: "CodeGen",
      surgical: true,
      target: "src/components/KanbanBoard.jsx",
      estimated_time: "1.5h"
    }
  ],
  
  total_steps: count,
  total_time: sum_of_estimates,
  
  rollback_point: backup_id
}
```

#### Step 8.2: Display Implementation Plan
```
DISPLAY:
  ═══════════════════════════════════════════════════════════════
  📝 IMPLEMENTATION PLAN: CR-2024-12-14-001 (Variant B)
  ═══════════════════════════════════════════════════════════════
  
  Backup created: BK-FS-2024-12-14-001-1702567890
  Rollback command: "rollback to BK-FS-2024-12-14-001-1702567890"
  
  ## Steps
  
  | # | Action | Method | Target | Time |
  |---|--------|--------|--------|------|
  | 1 | Create DropZone spec | Manual edit | components/DropZone.md | 30m |
  | 2 | Update KanbanBoard spec | Manual edit | components/KanbanBoard.md | 20m |
  | 3 | Update Pipeline spec | Manual edit | screens/Pipeline.md | 15m |
  | 4 | Implement DropZone | CodeGen (surgical) | src/components/DropZone.jsx | 1h |
  | 5 | Update KanbanBoard impl | CodeGen (surgical) | src/components/KanbanBoard.jsx | 1.5h |
  | 6 | Run targeted regression | QA (partial) | affected areas | 30m |
  | 7 | Update decomposition | Decomposition | OPML files | auto |
  | 8 | Generate change report | ChangeManager | CR_REPORT.md | auto |
  
  **Total Estimated Time**: 4 hours 45 minutes
  
  ## Requirements Traceability
  
  | Requirement | Step(s) | Status |
  |-------------|---------|--------|
  | FR-2024-12-001 | 1, 4 | Pending |
  | A11Y-2024-12-001 | 1, 4 | Pending |
  | PP-001 (enhanced) | 2, 5 | Pending |
  
  ═══════════════════════════════════════════════════════════════
  
  Ready to implement?
  1. "implement" - Execute all steps
  2. "implement step [N]" - Execute single step
  3. "modify step [N]" - Change a step
  4. "abort" - Cancel (backup preserved)
  ═══════════════════════════════════════════════════════════════
  
  WAIT for user response
```

### Phase 9: Implementation Execution

#### Step 9.1: Execute Implementation Steps
```
FOR each step in implementation_plan.steps:
  
  LOG: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  LOG: "Step {N}: {action}"
  LOG: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  
  IF step.surgical == true:
    ATTEMPT surgical edit:
      READ target file
      IDENTIFY specific sections to change
      APPLY minimal changes preserving rest
      PRESERVE user customizations
      
    IF merge conflict or cannot surgically edit:
      PROMPT user:
        ═══════════════════════════════════════════
        ⚠️ SURGICAL EDIT NOT POSSIBLE
        ═══════════════════════════════════════════
        
        Cannot cleanly merge changes into: {target}
        
        Reason: {conflict_description}
        
        Options:
        1. "regenerate" - Regenerate file from spec
        2. "manual" - I'll edit manually, show me what to change
        3. "skip" - Skip this step
        ═══════════════════════════════════════════
        
        WAIT for user response
  
  IF step.skill != "manual":
    INVOKE skill with surgical scope:
      skill_name: step.skill
      mode: "surgical"
      target: step.target
      changes: step.changes
      
  LOG_PROMPT:
    skill: "Prototype_ChangeManager"
    step: "Step 9.1: Execute {step.action}"
    desired_outcome: "{step.action}"
    category: "implementation"
    
  UPDATE step.status = "complete"
  UPDATE step.completed_at = timestamp
  
  DISPLAY progress:
    "✓ Step {N}/{total} complete: {action}"
```

#### Step 9.2: Update Requirements Traceability
```
FOR each step completed:
  IF step affects requirements:
    UPDATE _state/requirements_registry.json:
      FOR each requirement in step.requirements:
        ADD to addressed_by[]:
          "CR-{cr_id}: {step.target}"
        UPDATE last_modified: timestamp
```

### Phase 10: Post-Implementation Validation

#### Step 10.1: Run Targeted Regression
```
BASED on impact_analysis.regression_scope:
  
  FOR each area in must_test:
    INVOKE QA skill in targeted mode:
      scope: area
      requirements: affected_requirements
      
    RECORD results
    
  IF any test fails:
    DISPLAY:
      ═══════════════════════════════════════════
      ❌ REGRESSION TEST FAILED
      ═══════════════════════════════════════════
      
      Failed tests:
      • {test_name}: {failure_reason}
      
      Options:
      1. "fix" - Address the failure
      2. "rollback" - Restore from backup
      3. "ignore" - Document as known issue
      ═══════════════════════════════════════════
      
      WAIT for user response
```

#### Step 10.2: Update Decomposition OPML
```
INVOKE Prototype_Decomposition:
  MODE: merge
  TRIGGER: "change_implemented"
  CHANGES: {
    components_modified: [...],
    components_added: [...],
    screens_modified: [...],
    requirements_added: [...]
  }

LOG: "✓ Decomposition OPML updated"
```

#### Step 10.3: Generate Change Report
```
CREATE change_report:
  path: "outputs/change-reports/CR-{cr_id}_REPORT.md"
  
  content:
    # Change Report: CR-2024-12-14-001
    
    ## Summary
    | Field | Value |
    |-------|-------|
    | Title | Improve Pipeline Drag-Drop |
    | Session | FS-2024-12-14-001 |
    | Size | MEDIUM |
    | Variant | B - Proper Solution |
    | Status | IMPLEMENTED |
    
    ## Source Feedback
    - FI-001: Drag-drop not intuitive
    - FI-003: Stage names confusing
    
    ## Impact Analysis
    [summary of impact]
    
    ## Changes Made
    | File | Action | Details |
    |------|--------|---------|
    | components/DropZone.md | Created | New component spec |
    | components/KanbanBoard.md | Modified | Added DropZone integration |
    
    ## Requirements
    | Req ID | Action | Status |
    |--------|--------|--------|
    | FR-2024-12-001 | Created | Addressed |
    | A11Y-2024-12-001 | Created | Addressed |
    | PP-001 | Enhanced | Verified |
    
    ## Regression Results
    | Area | Tests | Passed | Failed |
    |------|-------|--------|--------|
    | Pipeline drag-drop | 5 | 5 | 0 |
    | Dashboard widget | 2 | 2 | 0 |
    
    ## Rollback Information
    Backup: BK-FS-2024-12-14-001-1702567890
    Command: rollback to BK-FS-2024-12-14-001-1702567890
```

#### Step 10.4: User Acceptance Checklist
```
DISPLAY:
  ═══════════════════════════════════════════════════════════════
  ✅ USER ACCEPTANCE CHECKLIST: CR-2024-12-14-001
  ═══════════════════════════════════════════════════════════════
  
  Please verify the following:
  
  ## Functional Acceptance
  - [ ] Drag-drop shows visual feedback during drag
  - [ ] Drop zones highlight when card hovers
  - [ ] Card snaps to new position on drop
  - [ ] Invalid drops show clear feedback
  - [ ] Works on Pipeline screen
  - [ ] Works on Dashboard widget
  
  ## Accessibility Acceptance
  - [ ] Can reorder using keyboard (Tab + Arrow + Enter)
  - [ ] Screen reader announces drag state
  - [ ] Focus visible during keyboard navigation
  
  ## Visual Acceptance
  - [ ] Drop zone highlight matches design system
  - [ ] Animation timing feels natural
  - [ ] No visual glitches during drag
  
  ## Edge Cases
  - [ ] Works with 50+ cards in column
  - [ ] Works when scrolled
  - [ ] Handles rapid drag-drops
  
  ═══════════════════════════════════════════════════════════════
  
  Verification:
  1. "accept" - All checks pass, close change request
  2. "issue: [description]" - Found an issue
  3. "defer: [items]" - Accept with noted exceptions
  ═══════════════════════════════════════════════════════════════
  
  WAIT for user response
```

### Phase 11: Change Request Closure

#### Step 11.1: Close Change Request
```
IF user accepts:
  UPDATE change_request:
    status: "implemented"
    implemented_at: timestamp
    acceptance: "full" | "with_exceptions"
    exceptions: [if any]
    
  UPDATE session:
    metrics.changes_implemented += 1
    metrics.changes_pending -= 1
    
  UPDATE progress.json:
    change_management.last_change: cr_id
    change_management.changes_implemented: count
    
  LOG: "✓ CR-{cr_id} closed successfully"

DISPLAY:
  ═══════════════════════════════════════════
  ✅ CHANGE REQUEST CLOSED
  ═══════════════════════════════════════════
  
  CR-2024-12-14-001: Improve Pipeline Drag-Drop
  Status: IMPLEMENTED & ACCEPTED
  
  Artifacts updated:
  ├─ 2 component specs
  ├─ 1 screen spec
  ├─ 2 code files
  ├─ 2 new requirements
  └─ 1 decomposition OPML
  
  Report: outputs/change-reports/CR-2024-12-14-001_REPORT.md
  
  Remaining in session: {pending_count} changes
  
  Next: "next change" | "session summary" | "close session"
  ═══════════════════════════════════════════
```

### Phase 12: Session Management

#### Step 12.1: Session Summary
```
WHEN user requests or session complete:
  
  GENERATE session summary:
    
    ═══════════════════════════════════════════════════════════════
    📊 FEEDBACK SESSION SUMMARY: FS-2024-12-14-001
    ═══════════════════════════════════════════════════════════════
    
    ## Overview
    | Metric | Value |
    |--------|-------|
    | Started | 2024-12-14 09:00 |
    | Duration | 4 hours 30 minutes |
    | Feedback Items | 12 |
    | Change Requests | 8 |
    | Implemented | 6 |
    | Deferred | 1 |
    | Rejected | 1 |
    
    ## Changes by Size
    | Size | Count | Total Effort |
    |------|-------|--------------|
    | Small | 3 | 4 hours |
    | Medium | 2 | 10 hours |
    | Large | 1 | 16 hours |
    
    ## Requirements Impact
    | Action | Count |
    |--------|-------|
    | Created | 8 |
    | Enhanced | 5 |
    | Linked | 12 |
    
    ## Artifacts Modified
    | Type | Created | Modified |
    |------|---------|----------|
    | Components | 2 | 5 |
    | Screens | 0 | 3 |
    | Code files | 2 | 8 |
    
    ## Backups Created
    - BK-FS-2024-12-14-001-xxx (before first change)
    
    ## Change Reports Generated
    - CR-2024-12-14-001_REPORT.md
    - CR-2024-12-14-002_REPORT.md
    - [...]
    
    ═══════════════════════════════════════════════════════════════
```

---

## Commands Reference

### Session Commands
| Command | Action |
|---------|--------|
| `new session` | Start new feedback session |
| `resume [session_id]` | Continue existing session |
| `list sessions` | Show all sessions |
| `session summary` | Show current session summary |
| `close session` | Complete and archive session |

### Change Commands
| Command | Action |
|---------|--------|
| `next change` | Process next pending change |
| `list changes` | Show all change requests |
| `show CR-xxx` | Show specific change request |
| `defer CR-xxx` | Move to backlog |
| `reject CR-xxx: [reason]` | Reject with reason |

### Implementation Commands
| Command | Action |
|---------|--------|
| `implement` | Execute full implementation plan |
| `implement step [N]` | Execute single step |
| `skip step [N]` | Skip a step |
| `pause` | Pause implementation |

### Rollback Commands
| Command | Action |
|---------|--------|
| `rollback to [backup_id]` | Restore from backup |
| `list backups` | Show available backups |
| `delete backup [id]` | Remove old backup |

### Variant Commands
| Command | Action |
|---------|--------|
| `compare [A] [B]` | Detailed variant comparison |
| `customize` | Mix variant elements |
| `regenerate variants` | Create new variants |

### Debugging Commands (Bug-type changes)
| Command | Action |
|---------|--------|
| `investigate` | Start/resume root cause investigation |
| `reproduce` | Define reproduction steps |
| `trace` | Trace data flow from symptom |
| `hypothesis: [theory]` | Propose root cause hypothesis |
| `confirm hypothesis` | Accept current hypothesis |
| `reject hypothesis` | Reject and investigate more |
| `show debugging` | Display debugging evidence |
| `fix attempt [N]` | Track fix attempt number |
| `escalate` | Flag for architectural review |

---

## State Files

### feedback_sessions.json
```json
{
  "version": "1.0",
  "sessions": [
    {
      "session_id": "FS-2024-12-14-001",
      "created_at": "2024-12-14T09:00:00Z",
      "status": "active",
      "feedback_items": [...],
      "change_requests": ["CR-2024-12-14-001", ...],
      "metrics": {
        "items_received": 12,
        "changes_implemented": 6,
        "changes_pending": 2
      }
    }
  ],
  "summary": {
    "total_sessions": 3,
    "total_changes": 25
  }
}
```

### backups.json
```json
{
  "backups": [
    {
      "backup_id": "BK-FS-2024-12-14-001-1702567890",
      "session_id": "FS-2024-12-14-001",
      "created_at": "2024-12-14T09:05:00Z",
      "files_backed_up": 156,
      "size_mb": 12.4,
      "status": "available"
    }
  ]
}
```

---

## Integration with Other Skills

| Skill | Integration Point | Purpose |
|-------|-------------------|---------|
| Components | Phase 9 | Surgical component updates |
| Screens | Phase 9 | Surgical screen updates |
| CodeGen | Phase 9 | Surgical code generation |
| QA | Phase 10 | Targeted regression testing |
| Decomposition | Phase 10 | OPML update |
| PromptLog | All phases | Log all prompts |
| Requirements | Phase 7 | Create/link requirements |

---

## Validation Rules

| Rule | Enforcement |
|------|-------------|
| Backup before changes | REQUIRED |
| Size classification confirmed | REQUIRED for proceed |
| **Root cause identified (bugs)** | **REQUIRED before fix variants** |
| Variant selected (M/L changes) | REQUIRED for implement |
| Requirements created/linked | REQUIRED before implement |
| Regression passed | REQUIRED for acceptance |
| User acceptance | REQUIRED for closure |
| **Max 3 fix attempts before escalation** | **ENFORCED for bugs** |

---

## Quality Checklist

### Before Implementation
- [ ] Feedback properly structured
- [ ] Impact analysis complete
- [ ] **Debugging completed (if Bug type)**
- [ ] **Root cause hypothesis confirmed (if Bug type)**
- [ ] Clarifications resolved
- [ ] Variant selected (if M/L)
- [ ] Requirements created/linked
- [ ] Backup created

### During Implementation (Bugs)
- [ ] **Fix addresses root cause, not symptom**
- [ ] **Defense-in-depth added (if Variant C)**
- [ ] **Regression test created for this bug**
- [ ] Each step logged
- [ ] Surgical edits attempted first
- [ ] Merge conflicts resolved
- [ ] Progress tracked

### During Implementation (Other)
- [ ] Each step logged
- [ ] Surgical edits attempted first
- [ ] Merge conflicts resolved
- [ ] Progress tracked

### After Implementation
- [ ] Regression tests passed
- [ ] **Bug regression test passes (if Bug type)**
- [ ] Decomposition updated
- [ ] Change report generated
- [ ] User acceptance obtained
- [ ] Change request closed
