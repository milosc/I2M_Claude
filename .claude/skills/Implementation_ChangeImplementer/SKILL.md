---
name: Implementation Change Implementer
description: Use when executing change requests using PDCA cycle with TDD implementation and Reflexion self-refinement loops for quality assurance.
model: sonnet
allowed-tools: Read, Write, Edit, Bash
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_ChangeImplementer started '{"stage": "implementation"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Implementation_ChangeImplementer ended '{"stage": "implementation"}'
---

# Implementation Change Implementer

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill Implementation_ChangeImplementer instruction_start '{"stage": "implementation", "method": "instruction-based"}'
```

Executes change requests following the PDCA (Plan-Do-Check-Act) cycle with integrated TDD for implementation and Reflexion for quality verification. Based on scientific research showing 8-21% quality improvement through self-refinement.

---

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:Implementation_ChangeImplementer:started` - When skill begins
- `skill:Implementation_ChangeImplementer:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Prerequisites

1. **Traceability Guard Check**: This skill invokes `Traceability_Guard` before execution.
   - If guard fails, execution stops with guidance to run `/traceability-init`.
   - Required files: `task_registry.json`, `change_request_registry.json`

2. **Analysis Complete**: `ANALYSIS.md` exists with root cause identified
3. **Session Folder Exists**: `change-requests/<YYYY-MM-DD>_CR-<NNN>/`
4. **Root Cause Identified**: No implementation without understanding "why"

## Core Principle

> **PDCA + TDD + Reflexion = Verified Quality**
>
> - PDCA: Structured improvement cycle
> - TDD: Correct implementation
> - Reflexion: Quality verification through self-refinement

## Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CHANGE IMPLEMENTATION WORKFLOW                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   PLAN (PDCA)          DO (TDD)           CHECK (PDCA)              │
│   ┌──────────┐        ┌──────────┐        ┌──────────┐              │
│   │ Baseline │───────→│   RED    │───────→│ Measure  │              │
│   │ Hypothes │        │  GREEN   │        │ Compare  │              │
│   │ Criteria │        │ REFACTOR │        │ Validate │              │
│   └──────────┘        └──────────┘        └────┬─────┘              │
│                                                │                     │
│                           ┌────────────────────┘                     │
│                           ▼                                          │
│              ┌─────────────────────────┐                             │
│              │    REFLECT (Reflexion)   │                            │
│              │  ┌─────────────────────┐ │                            │
│              │  │ Self-Assessment     │ │                            │
│              │  │ Multi-Perspective   │ │                            │
│              │  │ Refinement Planning │ │                            │
│              │  └─────────────────────┘ │                            │
│              └────────────┬─────────────┘                            │
│                           │                                          │
│              ┌────────────┴────────────┐                             │
│              ▼                         ▼                             │
│   ┌─────────────────┐       ┌─────────────────┐                      │
│   │ Score >= 7      │       │ Score < 7       │                      │
│   │ → MEMORIZE      │       │ → ITERATE       │                      │
│   │ → ACT           │       │ (Back to DO)    │                      │
│   └─────────────────┘       └─────────────────┘                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Phase 1: PLAN (PDCA)

Generate structured implementation plan from analysis.

```
PROCEDURE plan_phase:

1. EXTRACT from ANALYSIS.md:
   - Root cause(s)
   - Countermeasures (prioritized)
   - Affected files

2. ESTABLISH BASELINE
   Record current state metrics:

   baseline = {
       test_count: [number of tests],
       test_pass_rate: [% passing],
       coverage: [% coverage],
       failing_tests: [list of failing tests],
       performance_metrics: [if applicable],
       timestamp: [ISO]
   }

3. FORMULATE HYPOTHESIS

   "If we [specific change from countermeasure],
    then [expected measurable outcome]
    because [reasoning from root cause analysis]."

   GOOD hypothesis:
   - Specific and testable
   - Tied to root cause
   - Has measurable outcome

   BAD hypothesis:
   - Vague ("make it better")
   - Not tied to analysis
   - No success criteria

4. DEFINE SUCCESS CRITERIA

   criteria = {
       tests_pass: true,
       no_regressions: true,
       issue_resolved: [how to verify],
       coverage_maintained: [>= baseline],
       performance: [if applicable]
   }

5. PLAN TASKS

   FOR EACH countermeasure:
       CREATE task:
           - Description
           - Files to modify
           - Expected changes
           - Risk level
           - Rollback plan

6. DETERMINE rollback strategy
   - How to revert if things go wrong
   - Checkpoint after each task

OUTPUT: IMPLEMENTATION_PLAN.md
```

### Plan Template

```markdown
# Implementation Plan: CR-<ID>

## Baseline Metrics
| Metric | Current | Target |
|--------|---------|--------|
| Tests Passing | X/Y | All |
| Coverage | X% | >= X% |
| Issue Status | Failing | Fixed |

## Hypothesis
If we [change], then [outcome] because [reasoning].

## Success Criteria
- [ ] Original issue resolved
- [ ] All tests pass
- [ ] No coverage regression
- [ ] No performance regression

## Tasks

### Task 1: [Description]
**Files**: [list]
**Risk**: Low/Medium/High
**Rollback**: [how to revert]

### Task 2: [Description]
...

## Rollback Plan
If validation fails:
1. [Revert step 1]
2. [Revert step 2]
```

## Phase 2: DO (TDD)

Execute implementation using strict TDD protocol.

```
PROCEDURE do_phase:

FOR EACH task IN implementation_plan.tasks:

    1. RED: Write Failing Test
       ─────────────────────────────
       BEFORE any code changes:

       IF task.type == "bug":
           WRITE test that reproduces the bug
           TEST MUST FAIL (proves bug exists)

       IF task.type == "improvement":
           WRITE test for expected new behavior
           TEST MUST FAIL (feature doesn't exist)

       RUN test:
           vitest run <test_file> --reporter=verbose

       VERIFY: Test fails for expected reason

       LOG to IMPLEMENTATION_LOG.md:
           - Test file created
           - Test name
           - Failure reason (expected)

    2. GREEN: Minimal Implementation
       ─────────────────────────────
       IMPLEMENT smallest change to pass test:

       KAIZEN PRINCIPLES:
       - Standardized Work: Follow existing patterns
       - JIT: Only what's needed now
       - Continuous Improvement: Small, verified changes

       NO "while I'm here" changes
       NO premature optimization
       NO scope creep

       RUN test:
           vitest run <test_file>

       VERIFY: Test passes

       IF test still fails:
           DEBUG and fix
           DO NOT proceed until green

       LOG to IMPLEMENTATION_LOG.md:
           - Files modified
           - Changes made
           - Test result

    3. REFACTOR: Clean Up (Optional)
       ─────────────────────────────
       ONLY IF obvious improvements:

       - Remove duplication
       - Improve naming
       - Simplify logic

       AFTER EACH refactor change:
           RUN tests
           VERIFY still green

       STOP when "good enough"
       (Kaizen: diminishing returns)

       LOG any refactoring done

    4. VERIFY: Full Suite
       ─────────────────────────────
       RUN full test suite:
           vitest run --coverage

       CHECK:
           □ All tests pass
           □ No regressions
           □ Coverage maintained
           □ Type check passes (tsc --noEmit)

       IF failures:
           FIX before proceeding
           DO NOT skip failing tests

       LOG results

    CHECKPOINT after each task:
        - Can rollback to here if needed
        - Document state

OUTPUT: IMPLEMENTATION_LOG.md with full execution trace
```

### Implementation Log Template

```markdown
# Implementation Log: CR-<ID>

## Task 1: [Description]

### RED Phase
**Timestamp**: [ISO]
**Test Created**: `tests/unit/[file].test.ts`

```typescript
it('should [expected behavior]', () => {
  // Test code
});
```

**Run Result**: FAIL (expected)
**Failure Reason**: [Why it failed - proves issue exists]

### GREEN Phase
**Timestamp**: [ISO]
**Files Modified**:
- `src/[file].ts`: [What changed]

**Run Result**: PASS
**Test Output**: [Summary]

### REFACTOR Phase
**Changes**: [None / List of refactoring]
**All Tests**: PASS

### Verification
**Full Suite**: X/Y passing
**Coverage**: X%
**Type Check**: PASS

---

## Task 2: [Description]
...
```

## Phase 3: CHECK (PDCA)

Verify implementation against baseline and success criteria.

```
PROCEDURE check_phase:

1. MEASURE RESULTS

   current = {
       test_count: [new count],
       test_pass_rate: [% passing],
       coverage: [% coverage],
       failing_tests: [],
       performance_metrics: [if applicable],
       timestamp: [ISO]
   }

2. COMPARE TO BASELINE

   FOR EACH metric IN baseline:
       delta = current[metric] - baseline[metric]
       status = "improved" | "unchanged" | "regressed"

       IF regressed AND critical:
           FAIL check
           RETURN to DO phase

3. VALIDATE HYPOTHESIS

   hypothesis_confirmed = (
       success_criteria.all_met AND
       root_cause_addressed AND
       no_regressions
   )

   IF NOT hypothesis_confirmed:
       ANALYZE why
       DOCUMENT in IMPLEMENTATION_LOG.md
       DECIDE: iterate or escalate

4. MANUAL VERIFICATION

   □ Reproduce original issue
     → Should be FIXED

   □ Test edge cases
     → Should handle gracefully

   □ Verify in staging (if applicable)
     → Should work in realistic environment

5. REGRESSION CHECK

   RUN: vitest run
   RUN: tsc --noEmit
   RUN: eslint (if configured)

   ALL MUST PASS

OUTPUT: Verification section in IMPLEMENTATION_LOG.md
```

## Phase 4: REFLECT (Reflexion)

Self-refinement loop to verify quality.

```
PROCEDURE reflect_phase:

1. COMPLEXITY TRIAGE
   ─────────────────────────────
   Determine appropriate reflection depth:

   IF change.complexity == "simple":
       reflection_depth = "QUICK"     # 5 minutes
   ELIF change.complexity == "moderate":
       reflection_depth = "STANDARD"  # 15 minutes
   ELSE:
       reflection_depth = "DEEP"      # 30+ minutes

2. QUICK REFLECTION (Simple changes)
   ─────────────────────────────
   Fast verification checklist:

   □ Did the fix address root cause (not just symptom)?
   □ Are there obvious improvements missed?
   □ Any copy-paste or duplication introduced?
   □ Tests cover the actual fix?

   IF all checked:
       reflection_score = 8
       PROCEED to MEMORIZE
   ELSE:
       NOTE issues for iteration

3. STANDARD REFLECTION (Moderate changes)
   ─────────────────────────────
   Self-Assessment against quality criteria:

   COMPLETENESS (0-10):
       - All acceptance criteria met?
       - Edge cases handled?
       - Error cases covered?

   QUALITY (0-10):
       - Code follows patterns?
       - Readable and maintainable?
       - No obvious code smells?

   CORRECTNESS (0-10):
       - Tests verify actual behavior?
       - No false positives?
       - Regression suite complete?

   AVERAGE SCORE = (completeness + quality + correctness) / 3

   IF score < 7:
       GENERATE refinement plan
       RETURN to DO phase
   ELSE:
       PROCEED to MEMORIZE

4. DEEP REFLECTION (Complex changes)
   ─────────────────────────────
   Multi-Perspective Critique with 3 judges:

   JUDGE 1: REQUIREMENTS VALIDATOR
   ─────────────────────────────
   - Does fix align with original request?
   - Are acceptance criteria truly met?
   - Any scope creep?
   - Traceability maintained?

   Score: [1-10]
   Issues: [List]

   JUDGE 2: SOLUTION ARCHITECT
   ─────────────────────────────
   - Is the approach technically sound?
   - Does it follow architecture patterns?
   - Any technical debt introduced?
   - Performance implications?

   Score: [1-10]
   Issues: [List]

   JUDGE 3: CODE QUALITY REVIEWER
   ─────────────────────────────
   - Is the code clean and maintainable?
   - Are tests adequate and meaningful?
   - Documentation updated?
   - Error handling appropriate?

   Score: [1-10]
   Issues: [List]

   CROSS-REVIEW:
   ─────────────────────────────
   Judges review each other's findings:
   - Agreements
   - Disagreements (debate)
   - Consensus items

   FINAL SCORE = Average of 3 judges

   IF score < 7:
       CONSOLIDATE refinement items
       PRIORITIZE by impact
       RETURN to DO phase
   ELSE:
       PROCEED to MEMORIZE

OUTPUT: REFLECTION.md
```

### Reflection Template

```markdown
# Reflection: CR-<ID>

## Reflection Depth: [Quick/Standard/Deep]

## Self-Assessment

### Completeness: [X/10]
- [Assessment details]

### Quality: [X/10]
- [Assessment details]

### Correctness: [X/10]
- [Assessment details]

## Multi-Perspective Critique (if Deep)

### Requirements Validator: [X/10]
- [Findings]

### Solution Architect: [X/10]
- [Findings]

### Code Quality Reviewer: [X/10]
- [Findings]

## Consensus
**Final Score**: [X/10]

**Key Findings**:
1. [Finding]
2. [Finding]

## Decision
- [ ] PASS: Proceed to Memorize (Score >= 7)
- [ ] ITERATE: Return to DO phase (Score < 7)

## Refinement Items (if iterating)
| Priority | Item | Addresses |
|----------|------|-----------|
| 1 | [Item] | [Issue] |
```

## Phase 5: MEMORIZE (Reflexion)

Capture learnings for future benefit.

```
PROCEDURE memorize_phase:

1. HARVEST INSIGHTS
   ─────────────────────────────
   Extract learnings from this change request:

   insights = []

   FROM root_cause_analysis:
       - What went wrong originally?
       - How was it missed?
       - What pattern led to issue?

   FROM implementation:
       - What worked well?
       - What was harder than expected?
       - What shortcuts to avoid?

   FROM reflection:
       - What quality issues found?
       - What improvements made?
       - What to do differently?

2. CURATE INSIGHTS
   ─────────────────────────────
   Apply filters to each insight:

   FOR EACH insight:
       relevant = applies_beyond_this_case?
       non_redundant = not_in_claude_md?
       actionable = can_apply_in_future?
       evidence_based = proven_by_this_experience?

       IF all criteria met:
           curated_insights.append(insight)

3. CATEGORIZE
   ─────────────────────────────
   Group insights by type:

   ERROR_PATTERNS:
       - Patterns that led to issues
       - Anti-patterns discovered

   DEBUGGING_STRATEGIES:
       - Techniques that worked
       - Tools that helped

   CODE_QUALITY_RULES:
       - Standards to follow
       - Checks to add

   PROCESS_IMPROVEMENTS:
       - Workflow changes
       - Review additions

4. UPDATE CLAUDE.md (if significant)
   ─────────────────────────────
   ADD to appropriate section:

   ## Implementation Learnings

   ### Error Patterns to Avoid
   - [Pattern]: [Why problematic] (from CR-XXX)

   ### Debugging Strategies
   - [Technique]: [When to use] (proven in CR-XXX)

   ### Code Quality Rules
   - [Rule]: [Rationale] (learned from CR-XXX)

5. VALIDATE MEMORY UPDATE
   ─────────────────────────────
   Before committing to CLAUDE.md:

   □ Coherent with existing content
   □ Actionable guidance (not vague)
   □ Not duplicating existing rules
   □ Has evidence reference (CR-XXX)

OUTPUT: Updated CLAUDE.md (if applicable)
```

## Phase 6: ACT (PDCA)

Standardize successful changes or iterate.

```
PROCEDURE act_phase:

IF reflection_score >= 7 AND check_passed:

    STANDARDIZE:
    ─────────────────────────────
    1. Merge code changes
       - Commit with descriptive message
       - Reference CR-XXX in commit

    2. Update documentation
       - API docs if changed
       - README if needed
       - Architecture docs if affected

    3. Add to regression tests
       - Ensure fix stays fixed
       - Cover edge cases found

    4. Update registries
       - Mark CR as completed
       - Link to task registry
       - Update traceability

    5. Generate SUMMARY.md
       - Problem summary
       - Solution summary
       - Files changed
       - Learnings captured

ELSE:

    ITERATE:
    ─────────────────────────────
    1. Document why iteration needed
    2. Update plan based on learnings
    3. Return to DO phase
    4. Track iteration count

    IF iterations > 3:
        ESCALATE: May need different approach
        Review root cause analysis

OUTPUT: SUMMARY.md or iteration plan
```

### Summary Template

```markdown
# Change Request Summary: CR-<ID>

## Problem
[Brief description of the issue]

## Root Cause
[From analysis]

## Solution
[What was implemented]

## Files Changed
| File | Change |
|------|--------|
| `src/[file].ts` | [What changed] |

## Tests Added
| Test | Verifies |
|------|----------|
| `[test name]` | [What it tests] |

## Metrics
| Metric | Before | After |
|--------|--------|-------|
| Tests | X | Y |
| Coverage | X% | Y% |

## Learnings Captured
- [Learning 1]
- [Learning 2]

## PDCA Cycles
- Cycles: [1-N]
- Total Duration: [X hours/minutes]

## Timeline
| Phase | Duration |
|-------|----------|
| Plan | X min |
| Do | X min |
| Check | X min |
| Reflect | X min |
| Memorize | X min |
| Act | X min |
| **Total** | **X min** |
```

## Quality Gates

```
BEFORE proceeding from each phase:

PLAN → DO:
    □ Baseline established
    □ Hypothesis formulated
    □ Success criteria defined
    □ Tasks planned

DO → CHECK:
    □ Tests written (RED)
    □ Tests passing (GREEN)
    □ Refactoring complete
    □ Full suite passes

CHECK → REFLECT:
    □ Hypothesis validated
    □ No regressions
    □ Manual verification done

REFLECT → MEMORIZE:
    □ Score >= 7
    □ No blocking issues
    □ Refinement complete (if iterated)

MEMORIZE → ACT:
    □ Insights harvested
    □ CLAUDE.md updated (if applicable)
    □ Ready to standardize
```

## Related Skills

- `Implementation_ChangeAnalyzer` - Root cause analysis (Kaizen)
- `Implementation_Developer` - Core TDD implementation
- `systematic-debugging` - Technical debugging
