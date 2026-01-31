# Implementation Stage Change Request System

## Overview

The change request process combines three methodologies:
1. **Kaizen** (Toyota Production System) - Root cause analysis before any fix
2. **PDCA** (Plan-Do-Check-Act) - Structured improvement cycle
3. **Reflexion** - AI self-refinement through quality verification loops

## Command

```bash
/htec-sdd-changerequest <SystemName> [--type=bug|improvement|feedback] [--id=CR-NNN]
```

## Skills Used

| Skill | Purpose | Phase |
|-------|---------|-------|
| `Implementation_ChangeAnalyzer` | Kaizen root cause analysis (5 Whys, Fishbone, A3, Gemba Walk) | 1-3 |
| `Implementation_ChangeImplementer` | PDCA execution with TDD and Reflexion | 4-9 |
| `systematic-debugging` | Four-phase technical debugging framework | 3 |
| `root-cause-tracing` | Data flow tracing for deep call stack issues | 3 |
| `Implementation_Developer` | TDD implementation (RED-GREEN-REFACTOR) | 5 |

---

## Complete Workflow (9 Phases)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CHANGE REQUEST WORKFLOW                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. RECEIVE        Intake change request, classify type                  │
│        ↓                                                                 │
│  2. TRIAGE         Assess severity, complexity, impact                   │
│        ↓                                                                 │
│  3. ANALYZE        ← KAIZEN: 5 Whys / Fishbone / Gemba Walk             │
│        ↓                                                                 │
│  4. PLAN           ← KAIZEN: PDCA Plan phase, A3 documentation           │
│        ↓                                                                 │
│  5. IMPLEMENT      ← TDD: RED-GREEN-REFACTOR cycle                       │
│        ↓                                                                 │
│  6. VERIFY         ← KAIZEN: PDCA Check phase                            │
│        ↓                                                                 │
│  7. REFLECT        ← REFLEXION: Self-refinement, multi-perspective       │
│        ↓                                                                 │
│  8. MEMORIZE       ← REFLEXION: Update CLAUDE.md with learnings          │
│        ↓                                                                 │
│  9. CLOSE          Update registries, generate summary                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: RECEIVE (Intake)

Collects change request details and creates tracking infrastructure:

**Input Collected:**
- Description (what happened / what's needed)
- Reproduction steps (if bug)
- Expected vs. actual behavior
- Screenshots / logs

**Classification:**
- `BUG`: Something broken that was working
- `IMPROVEMENT`: Enhancement to existing feature
- `FEEDBACK`: Stakeholder input requiring change

**Tracking:**
- Assigns ID: `CR-<SystemName>-NNN`
- Creates session folder structure

---

## Phase 2: TRIAGE (Impact Analysis)

Determines severity and appropriate analysis depth:

### Severity Assessment (Priority Matrix)
| Impact | Urgency | Severity | Response Time |
|--------|---------|----------|---------------|
| High | High | **CRITICAL** | Immediate (hours) |
| High | Low | **HIGH** | This sprint |
| Low | High | **MEDIUM** | Next sprint |
| Low | Low | **LOW** | Backlog |

### Complexity Assessment
- **SIMPLE**: Single file, isolated change
- **MODERATE**: 2-5 files, local impact
- **COMPLEX**: 6+ files, cross-cutting concern

### Analysis Method Selection
```
IF severity == CRITICAL OR complexity == COMPLEX:
    analysis_method = "A3_FULL"        # Comprehensive (2-4 hours)
ELIF severity == HIGH OR complexity == MODERATE:
    analysis_method = "FIVE_WHYS"       # Standard (30-60 min)
ELIF type == "bug" AND unfamiliar_code:
    analysis_method = "GEMBA_THEN_FIVE_WHYS"
ELSE:
    analysis_method = "QUICK_CHECK"     # Fast path (10-15 min)
```

---

## Phase 3: ANALYZE (Root Cause - Kaizen)

**Iron Law**: No fix without root cause identification.

### 5 Kaizen Analysis Methods

#### Method 1: Quick Check (10-15 min)
For simple, low-risk changes with obvious cause:
```
1. VERIFY reproduction
2. IDENTIFY immediate cause
3. CONFIRM fix location
4. DOCUMENT briefly
```

#### Method 2: Five Whys (30-60 min)
For moderate complexity:
```
Problem: [Observable symptom]

Why 1: [What code triggered it?]
    Evidence: [How you know]
Why 2: [Why did that code behave that way?]
    Evidence: [How you know]
Why 3: [Why was it written that way?]
    Evidence: [How you know]
Why 4: [Why wasn't this caught earlier?]
    Evidence: [How you know]
Why 5: [What systemic issue allowed this?]
    Evidence: [How you know]

Root Cause: [Fundamental issue - usually process/design]
```

**Branching Rules:**
- If multiple causes emerge → explore each branch
- Stop when you reach process/systemic issues
- If "human error" appears → ask WHY error was possible
- Not always exactly 5 levels (usually 3-7)

#### Method 3: Fishbone Analysis (60-90 min)
For complex issues with multiple contributing factors:

```
                    ┌── PEOPLE
                    │   ├─ Skills/training gaps?
                    │   ├─ Communication issues?
                    │   └─ Knowledge silos?
                    │
                    ├── PROCESS
                    │   ├─ Workflow gaps?
                    │   ├─ Review failures?
                    │   └─ Missing standards?
                    │
EFFECT ◄────────────┼── TECHNOLOGY
(Problem)           │   ├─ Tool limitations?
                    │   ├─ Infrastructure issues?
                    │   └─ Dependency problems?
                    │
                    ├── ENVIRONMENT
                    │   ├─ Dev/prod differences?
                    │   └─ Resource constraints?
                    │
                    ├── METHODS
                    │   ├─ Architectural issues?
                    │   └─ Technical debt?
                    │
                    └── MATERIALS
                        ├─ Data quality?
                        └─ Third-party issues?
```

#### Method 4: A3 Full Analysis (2-4 hours)
For critical issues requiring comprehensive documentation:

```
═══════════════════════════════════════════════════
                A3 PROBLEM ANALYSIS
═══════════════════════════════════════════════════

1. BACKGROUND      - Why this matters, business impact
2. CURRENT STATE   - Facts, data, reproduction evidence
3. GOAL/TARGET     - Specific success criteria
4. ROOT CAUSE      - [Embed Five Whys or Fishbone]
5. COUNTERMEASURES - Immediate / Short-term / Long-term
6. IMPLEMENTATION  - Tasks, owners, dependencies
7. FOLLOW-UP       - Verification, monitoring

═══════════════════════════════════════════════════
```

#### Method 5: Gemba Walk (30-60 min)
For unfamiliar code areas - "Go and see" before analyzing:

```
1. SCOPE: Define code area to explore
2. ASSUMPTIONS: Document what you THINK it does
3. OBSERVATIONS: Read actual code, document reality
4. SURPRISES: What differs from assumptions?
5. GAPS: Documentation vs. implementation
6. RECOMMEND: What to fix/update?
```

### Integration with systematic-debugging

For bugs, the `systematic-debugging` skill enforces:

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST

Phase 1: Root Cause Investigation
  - Read error messages completely
  - Reproduce consistently
  - Check recent changes
  - Trace data flow

Phase 2: Pattern Analysis
  - Find working examples
  - Compare differences

Phase 3: Hypothesis Testing
  - Form single hypothesis
  - Test minimally
  - One variable at a time

Phase 4: Implementation (only after understanding)
```

**Output:** `ANALYSIS.md` with root cause, evidence, countermeasures

---

## Phase 4: PLAN (PDCA Plan Phase)

Generates structured implementation plan from analysis:

### Plan Components

```
1. BASELINE METRICS
   baseline = {
       test_count: X,
       test_pass_rate: Y%,
       coverage: Z%,
       failing_tests: [...],
       timestamp: [ISO]
   }

2. HYPOTHESIS
   "If we [specific change],
    then [expected outcome]
    because [reasoning from root cause]"

3. SUCCESS CRITERIA
   - tests_pass: true
   - no_regressions: true
   - issue_resolved: [verification method]
   - coverage_maintained: >= baseline

4. COUNTERMEASURE TASKS
   | Order | Task | Type | Files | Risk |
   |-------|------|------|-------|------|
   | 1 | [task] | fix | [...] | low |
   | 2 | [task] | prevent | [...] | med |

5. ROLLBACK PLAN
   - How to revert if things go wrong
   - Checkpoints for validation
```

**Output:** `IMPLEMENTATION_PLAN.md`

---

## Phase 5: IMPLEMENT (TDD Execution)

Strict TDD protocol for each countermeasure task:

```
FOR EACH task:

    ┌─────────────────────────────────────┐
    │  1. RED: Write Failing Test         │
    │     - Test reproduces bug (for bug) │
    │     - Test verifies new behavior    │
    │     - MUST FAIL before fix          │
    ├─────────────────────────────────────┤
    │  2. GREEN: Minimal Implementation   │
    │     - Smallest change to pass       │
    │     - Follow existing patterns      │
    │     - NO "while I'm here" changes   │
    │     - NO scope creep                │
    ├─────────────────────────────────────┤
    │  3. REFACTOR: Clean Up (Optional)   │
    │     - Remove duplication            │
    │     - Improve naming                │
    │     - Keep tests GREEN              │
    │     - Stop when "good enough"       │
    ├─────────────────────────────────────┤
    │  4. VERIFY: Full Suite              │
    │     - All tests pass                │
    │     - No regressions                │
    │     - Coverage maintained           │
    │     - Type check passes             │
    └─────────────────────────────────────┘

    CHECKPOINT after each task
```

**Output:** `IMPLEMENTATION_LOG.md` with full execution trace

---

## Phase 6: VERIFY (PDCA Check Phase)

Validates implementation against baseline:

```
1. MEASURE RESULTS
   current = {
       test_count: [new],
       test_pass_rate: [%],
       coverage: [%]
   }

2. COMPARE TO BASELINE
   FOR EACH metric:
       delta = current - baseline
       status = improved | unchanged | regressed

3. VALIDATE HYPOTHESIS
   IF hypothesis NOT confirmed:
       ANALYZE why
       RETURN to PLAN phase

4. MANUAL VERIFICATION
   □ Reproduce original issue → Should be FIXED
   □ Test edge cases
   □ Verify in staging

5. REGRESSION CHECK
   - Full test suite passes
   - Type check passes
   - Lint passes
```

---

## Phase 7: REFLECT (Reflexion Self-Refinement)

Quality verification through self-assessment:

### Complexity Triage
```
IF change.complexity == "simple":
    reflection_depth = "QUICK"      # 5 minutes
ELIF change.complexity == "moderate":
    reflection_depth = "STANDARD"   # 15 minutes
ELSE:
    reflection_depth = "DEEP"       # 30+ minutes
```

### Quick Reflection (Simple Changes)
```
□ Did the fix address root cause (not just symptom)?
□ Are there obvious improvements missed?
□ Any copy-paste or duplication introduced?
□ Tests cover the actual fix?
```

### Standard Reflection (Moderate Changes)
Self-Assessment Scoring:
```
COMPLETENESS (0-10): All acceptance criteria met? Edge cases?
QUALITY (0-10): Follows patterns? Readable? Maintainable?
CORRECTNESS (0-10): Tests verify behavior? No false positives?

AVERAGE SCORE = (completeness + quality + correctness) / 3

IF score < 7: Return to IMPLEMENT phase
IF score >= 7: Proceed to MEMORIZE
```

### Deep Reflection (Complex Changes)
Multi-Perspective Critique with 3 Judges:

```
JUDGE 1: REQUIREMENTS VALIDATOR
- Does fix align with original request?
- Acceptance criteria truly met?
- Any scope creep?
- Traceability maintained?
Score: [1-10]

JUDGE 2: SOLUTION ARCHITECT
- Technically sound approach?
- Follows architecture patterns?
- Technical debt introduced?
- Performance implications?
Score: [1-10]

JUDGE 3: CODE QUALITY REVIEWER
- Clean and maintainable code?
- Tests adequate and meaningful?
- Documentation updated?
- Error handling appropriate?
Score: [1-10]

CROSS-REVIEW: Judges review each other's findings
FINAL SCORE = Average of 3 judges

IF score < 7: ITERATE (return to DO phase)
IF score >= 7: PROCEED to MEMORIZE
```

**Output:** `REFLECTION.md`

---

## Phase 8: MEMORIZE (Reflexion Memory Update)

Captures learnings for future benefit:

```
1. HARVEST INSIGHTS
   FROM root_cause_analysis:
       - What went wrong originally?
       - How was it missed?
       - What pattern led to issue?

   FROM implementation:
       - What worked well?
       - What was harder than expected?

   FROM reflection:
       - What quality issues found?
       - What improvements made?

2. CURATE INSIGHTS (Filters)
   FOR EACH insight:
       □ RELEVANT: Applies beyond this case?
       □ NON-REDUNDANT: Not already in CLAUDE.md?
       □ ACTIONABLE: Can apply in future?
       □ EVIDENCE-BASED: Proven by this experience?

3. UPDATE CLAUDE.md (if significant)

   ## Implementation Learnings

   ### Error Patterns to Avoid
   - [Pattern]: [Why problematic] (from CR-XXX)

   ### Debugging Strategies
   - [Technique]: [When to use] (proven in CR-XXX)

   ### Code Quality Rules
   - [Rule]: [Rationale] (learned from CR-XXX)
```

This creates a **persistent memory** that improves future implementations.

---

## Phase 9: CLOSE (PDCA Act Phase)

Standardizes successful changes:

```
IF reflection_score >= 7 AND check_passed:

    STANDARDIZE:
    1. Merge code changes (commit with CR-XXX reference)
    2. Update documentation
    3. Add to regression tests
    4. Update registries:
       - change_request_registry.json (mark completed)
       - task_registry.json (link tasks)
       - Traceability chains

    GENERATE SUMMARY.md

ELSE:

    ITERATE:
    1. Document why iteration needed
    2. Update plan based on learnings
    3. Return to DO phase
    4. Track iteration count (max 3 before escalation)
```

---

## Tracking & Registry

### Session Folder Structure
```
Implementation_<System>/change-requests/
├── change_request_registry.json       # All CRs with status
└── <YYYY-MM-DD>_CR-<NNN>/
    ├── CHANGE_REQUEST.md              # Original request
    ├── ANALYSIS.md                    # Kaizen root cause analysis
    ├── IMPLEMENTATION_PLAN.md         # PDCA plan
    ├── IMPLEMENTATION_LOG.md          # TDD execution log
    ├── REFLECTION.md                  # Reflexion output
    └── SUMMARY.md                     # Final summary
```

### Registry Format
```json
{
  "schema_version": "1.0.0",
  "system_name": "InventorySystem",
  "change_requests": {
    "CR-INV-001": {
      "title": "Fix barcode scanner timeout",
      "type": "bug",
      "severity": "high",
      "status": "completed",
      "created_at": "2025-01-15T10:00:00Z",
      "completed_at": "2025-01-15T14:30:00Z",
      "root_cause": "Missing retry logic for network timeouts",
      "analysis_method": "five_whys",
      "files_changed": ["src/hooks/use-barcode-scanner.ts"],
      "tests_added": ["tests/unit/barcode-scanner-timeout.test.ts"],
      "task_refs": ["T-015"],
      "learnings_captured": true,
      "pdca_cycles": 1
    }
  }
}
```

### Traceability Chain
```
Implementation Task (T-NNN)
    ↓
Change Request (CR-XXX)
    ↓
Root Cause Analysis (ANALYSIS.md)
    ↓
Implementation (Code + Tests)
    ↓
Learnings (CLAUDE.md updates)
```

---

## Summary: Integration Points

| Methodology | Phase | Technique | Purpose |
|-------------|-------|-----------|---------|
| **Kaizen** | Triage | Priority Matrix | Severity assessment |
| **Kaizen** | Analyze | 5 Whys | Root cause drilling |
| **Kaizen** | Analyze | Fishbone | Multi-factor analysis |
| **Kaizen** | Analyze | Gemba Walk | Code exploration |
| **Kaizen** | Analyze | A3 | Comprehensive docs |
| **PDCA** | Plan | Baseline + Hypothesis | Structured planning |
| **TDD** | Implement | RED-GREEN-REFACTOR | Correct implementation |
| **PDCA** | Verify | Measure vs. Baseline | Validation |
| **Reflexion** | Reflect | Self-Assessment | Quality verification |
| **Reflexion** | Reflect | Multi-Agent Critique | Multiple perspectives |
| **Reflexion** | Memorize | Context Harvesting | Extract insights |
| **Reflexion** | Memorize | Memory Update | Persist to CLAUDE.md |
| **PDCA** | Close | Standardize | Make permanent |

---

## Related Documents

- [Stage5_Implementation_Traceability_Map.md](./Stage5_Implementation_Traceability_Map.md) - Full traceability architecture
- [HTEC_SDD_COMMAND_REFERENCE.md](../.claude/commands/HTEC_SDD_COMMAND_REFERENCE.md) - All implementation commands
- [Implementation_ChangeAnalyzer](../.claude/skills/Implementation_ChangeAnalyzer/SKILL.md) - Kaizen analysis skill
- [Implementation_ChangeImplementer](../.claude/skills/Implementation_ChangeImplementer/SKILL.md) - PDCA + Reflexion skill
- [systematic-debugging](../.claude/skills/systematic-debugging/SKILL.md) - Technical debugging framework
