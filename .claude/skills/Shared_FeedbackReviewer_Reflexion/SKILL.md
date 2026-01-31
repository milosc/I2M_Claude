---
name: Shared_FeedbackReviewer_Reflexion
allowed-tools: Bash
description: Reflexion-enhanced post-implementation validation with multi-perspective critical review
context: fork
agent: general-purpose
hooks:
  Stop:
    - hooks:
        - type: command
          command: "uv run $CLAUDE_PROJECT_DIR/.claude/hooks/capture_event.py --event-type Stop"
---

# Shared_FeedbackReviewer_Reflexion

## Purpose

Perform comprehensive validation of feedback implementation with reflexion-powered multi-perspective review to ensure completeness, correctness, and quality.

## Inputs

- `feedback_id`: Feedback identifier
- `stage`: Stage name
- `system_name`: System name
- `stage_folder`: Path to stage output folder
- `implementation_plan_path`: Path to implementation_plan.md
- `implementation_log_path`: Path to implementation_log.md
- `files_changed_path`: Path to files_changed.md

## Outputs

- `VALIDATION_REPORT.md`: Comprehensive validation report with:
  - Plan compliance results
  - Content validation results
  - Traceability validation results
  - Multi-perspective reflexion review
  - Consensus score and recommendation
  - Action items (if any)

## Procedure

### Step 1: Load Implementation Context

```
READ implementation_plan_path
EXTRACT:
   - selected_option
   - planned_steps[]
   - expected_changes[]

READ implementation_log_path
EXTRACT:
   - executed_steps[]
   - step_statuses[]
   - errors_encountered[]

READ files_changed_path
EXTRACT:
   - modified_files[]
   - actual_changes[]

STORE as implementation_context
```

### Step 2: Plan Compliance Validation

```
VALIDATION: Plan Compliance Check

Question: "Were all planned steps executed as specified?"

CHECK execution_completeness:
   planned_steps_count = COUNT(implementation_plan.steps)
   executed_steps_count = COUNT(implementation_log.completed_steps)

   IF executed_steps_count == planned_steps_count:
      execution_completeness = "✓ COMPLETE"
      execution_score = 10
   ELIF executed_steps_count >= 0.8 * planned_steps_count:
      execution_completeness = "⚠ MOSTLY COMPLETE"
      execution_score = 7
      missing_steps = planned_steps - executed_steps
   ELSE:
      execution_completeness = "❌ INCOMPLETE"
      execution_score = 3
      missing_steps = planned_steps - executed_steps

CHECK step_accuracy:
   mismatches = []

   FOR each executed_step:
      planned_step = FIND(implementation_plan.steps, step.step_number)

      IF planned_step:
         IF executed_step.artifact_id != planned_step.artifact_id:
            mismatches.append("Step {N}: Wrong artifact")

         IF executed_step.action != planned_step.action:
            mismatches.append("Step {N}: Wrong action")

   IF len(mismatches) == 0:
      step_accuracy = "✓ ACCURATE"
      accuracy_score = 10
   ELIF len(mismatches) <= 2:
      step_accuracy = "⚠ MINOR DEVIATIONS"
      accuracy_score = 6
   ELSE:
      step_accuracy = "❌ SIGNIFICANT DEVIATIONS"
      accuracy_score = 2

CHECK unexpected_changes:
   planned_files = SET([step.file_path for step in implementation_plan.steps])
   actual_files = SET(files_changed.modified_files)

   unexpected = actual_files - planned_files

   IF len(unexpected) == 0:
      unexpected_status = "✓ NO UNEXPECTED CHANGES"
      unexpected_score = 10
   ELIF len(unexpected) <= 2:
      unexpected_status = "⚠ MINOR UNEXPECTED CHANGES"
      unexpected_score = 6
   ELSE:
      unexpected_status = "❌ MANY UNEXPECTED CHANGES"
      unexpected_score = 2

CALCULATE plan_compliance_score:
   plan_compliance_score = (
      execution_score * 0.4 +
      accuracy_score * 0.4 +
      unexpected_score * 0.2
   )

STORE plan_compliance_results = {
   execution_completeness: {status, score, missing_steps},
   step_accuracy: {status, score, mismatches},
   unexpected_changes: {status, score, unexpected_files},
   total_score: plan_compliance_score
}
```

### Step 3: Content Validation

```
VALIDATION: Content Validation Check

Question: "Do modified files match planned before/after content?"

FOR each modified_file IN files_changed.modified_files:

   READ current_file_content

   planned_step = FIND(implementation_plan.steps, WHERE step.file_path == modified_file)

   IF planned_step:

      CHECK version_update:
         current_version = EXTRACT(current_file_content, "version:")
         planned_new_version = planned_step.version_update.new

         IF current_version == planned_new_version:
            version_valid = true
         ELSE:
            version_errors.append({
               file: modified_file,
               expected: planned_new_version,
               actual: current_version
            })

      CHECK change_history:
         change_history = EXTRACT(current_file_content, "change_history:")
         latest_entry = change_history[0]

         IF feedback_id IN latest_entry:
            history_valid = true
         ELSE:
            history_errors.append({
               file: modified_file,
               missing: feedback_id
            })

      CHECK content_match:
         IF planned_step.after_content:
            expected_content = planned_step.after_content
            actual_content = EXTRACT_SECTION(current_file_content, planned_step.section)

            similarity = CALCULATE_SIMILARITY(expected_content, actual_content)

            IF similarity >= 0.95:
               content_match = true
            ELSE:
               content_errors.append({
                  file: modified_file,
                  section: planned_step.section,
                  similarity: similarity,
                  diff: GENERATE_DIFF(expected_content, actual_content)
               })

      CHECK format_validity:
         IF modified_file.endswith('.yaml') OR modified_file.endswith('.yml'):
            valid = VALIDATE_YAML(current_file_content)
         ELIF modified_file.endswith('.json'):
            valid = VALIDATE_JSON(current_file_content)
         ELIF modified_file.endswith('.md'):
            valid = VALIDATE_MARKDOWN(current_file_content)

         IF NOT valid:
            format_errors.append({
               file: modified_file,
               error: validation_error
            })

CALCULATE content_validation_score:

   version_score = (
      IF len(version_errors) == 0: 10
      ELIF len(version_errors) <= 2: 6
      ELSE: 2
   )

   history_score = (
      IF len(history_errors) == 0: 10
      ELIF len(history_errors) <= 2: 6
      ELSE: 2
   )

   content_score = (
      IF len(content_errors) == 0: 10
      ELIF len(content_errors) <= 2: 6
      ELSE: 2
   )

   format_score = (
      IF len(format_errors) == 0: 10
      ELIF len(format_errors) <= 2: 6
      ELSE: 2
   )

   content_validation_score = (
      version_score * 0.2 +
      history_score * 0.2 +
      content_score * 0.4 +
      format_score * 0.2
   )

STORE content_validation_results = {
   version_updates: {score: version_score, errors: version_errors},
   change_history: {score: history_score, errors: history_errors},
   content_match: {score: content_score, errors: content_errors},
   format_validity: {score: format_score, errors: format_errors},
   total_score: content_validation_score
}
```

### Step 4: Traceability Validation

```
VALIDATION: Traceability Integrity Check

Question: "Are all traceability chains intact after implementation?"

READ all traceability registries for stage

FOR each modified_artifact:

   artifact_id = EXTRACT_ID(modified_artifact)

   CHECK registry_presence:
      registry = FIND_REGISTRY_FOR_ARTIFACT_TYPE(artifact_id)
      entry = FIND(registry, WHERE id == artifact_id)

      IF entry:
         registry_present = true
      ELSE:
         registry_errors.append({
            artifact: artifact_id,
            issue: "Not found in registry"
         })

   CHECK bidirectional_links:
      IF entry.traces_to:
         FOR each linked_artifact IN entry.traces_to:
            linked_entry = FIND_IN_ANY_REGISTRY(linked_artifact)

            IF linked_entry:
               IF artifact_id IN linked_entry.traced_from:
                  bidirectional_valid = true
               ELSE:
                  link_errors.append({
                     from: artifact_id,
                     to: linked_artifact,
                     issue: "Missing reverse link"
                  })
            ELSE:
               link_errors.append({
                  from: artifact_id,
                  to: linked_artifact,
                  issue: "Target artifact not found"
               })

   CHECK chain_completeness:
      FOR each chain IN impact_analysis.traceability_chains:
         IF artifact_id IN chain:
            FOR each node IN chain:
               node_exists = CHECK_ARTIFACT_EXISTS(node)
               IF NOT node_exists:
                  chain_errors.append({
                     chain: chain,
                     missing_node: node
                  })

CHECK orphaned_artifacts:
   all_artifacts = GET_ALL_ARTIFACT_IDS_FROM_REGISTRIES()

   FOR each artifact_id IN all_artifacts:
      entry = FIND_IN_ANY_REGISTRY(artifact_id)

      IF NOT entry.traces_to AND NOT entry.traced_from:
         IF artifact_id was modified in this feedback:
            orphan_errors.append({
               artifact: artifact_id,
               issue: "Orphaned after implementation"
            })

CALCULATE traceability_score:

   registry_score = (
      IF len(registry_errors) == 0: 10
      ELIF len(registry_errors) <= 2: 6
      ELSE: 2
   )

   link_score = (
      IF len(link_errors) == 0: 10
      ELIF len(link_errors) <= 3: 6
      ELSE: 2
   )

   chain_score = (
      IF len(chain_errors) == 0: 10
      ELIF len(chain_errors) <= 2: 6
      ELSE: 2
   )

   orphan_score = (
      IF len(orphan_errors) == 0: 10
      ELIF len(orphan_errors) <= 1: 6
      ELSE: 2
   )

   traceability_score = (
      registry_score * 0.25 +
      link_score * 0.3 +
      chain_score * 0.3 +
      orphan_score * 0.15
   )

STORE traceability_results = {
   registry_presence: {score: registry_score, errors: registry_errors},
   bidirectional_links: {score: link_score, errors: link_errors},
   chain_completeness: {score: chain_score, errors: chain_errors},
   orphaned_artifacts: {score: orphan_score, errors: orphan_errors},
   total_score: traceability_score
}
```

### Step 5: Stage-Specific Validation

```
RUN stage-specific quality gates (if available):

IF stage == "discovery":
   RUN bash:
      python3 .claude/hooks/discovery_quality_gates.py \
         --validate-checkpoint 11 \
         --dir {stage_folder}

ELIF stage == "prototype":
   RUN bash:
      python3 .claude/hooks/prototype_quality_gates.py \
         --validate-feedback {feedback_id} \
         --dir {stage_folder}

   IF code was modified:
      RUN bash:
         cd {stage_folder}/prototype && npm run build

      CHECK build_success:
         IF exit_code == 0:
            build_valid = true
            build_score = 10
         ELSE:
            build_valid = false
            build_score = 0
            build_errors = [build output]

ELIF stage == "productspecs":
   RUN bash:
      python3 .claude/hooks/productspecs_quality_gates.py \
         --validate-feedback {feedback_id} \
         --dir {stage_folder}

ELIF stage == "solarch":
   RUN bash:
      python3 .claude/hooks/solarch_quality_gates.py \
         --validate-feedback {feedback_id} \
         --dir {stage_folder}

ELIF stage == "implementation":
   RUN bash:
      python3 .claude/hooks/implementation_quality_gates.py \
         --validate-traceability \
         --dir {stage_folder}

   RUN tests:
      cd {stage_folder} && npm test

   CHECK test_results:
      IF all_tests_pass:
         test_score = 10
      ELSE:
         test_score = 0
         test_failures = [list failures]

PARSE quality_gate_output

STORE stage_specific_results = {
   quality_gates_passed: true|false,
   details: [...],
   score: X
}
```

### Step 6: Reflexion Multi-Perspective Review

```
REFLEXION MULTI-PERSPECTIVE CRITIQUE

Perspective 1: REQUIREMENTS VALIDATOR

Role: Validate that implementation addresses original feedback intent

Questions:
1. "Does the implementation fully address the original feedback?"
2. "Were the acceptance criteria met?"
3. "Is there any scope creep?"

CHECK original_feedback_addressed:
   original_feedback = READ(FEEDBACK_ORIGINAL.md)
   implementation_summary = READ(files_changed.md)

   key_requirements = EXTRACT_REQUIREMENTS(original_feedback)

   FOR each requirement:
      addressed = CHECK_IF_ADDRESSED(requirement, implementation_summary)

      IF addressed:
         requirements_met.append(requirement)
      ELSE:
         requirements_missed.append(requirement)

   coverage = len(requirements_met) / len(key_requirements)

   IF coverage >= 1.0:
      requirements_status = "✓ FULLY ADDRESSED"
      requirements_score = 10
   ELIF coverage >= 0.8:
      requirements_status = "⚠ MOSTLY ADDRESSED"
      requirements_score = 7
   ELSE:
      requirements_status = "❌ PARTIALLY ADDRESSED"
      requirements_score = 4

CHECK acceptance_criteria:
   criteria_from_plan = implementation_plan.acceptance_criteria

   IF criteria_from_plan:
      FOR each criterion:
         met = VERIFY_CRITERION_MET(criterion, implementation_context)

         IF NOT met:
            criteria_failures.append(criterion)

      IF len(criteria_failures) == 0:
         criteria_status = "✓ ALL MET"
         criteria_score = 10
      ELSE:
         criteria_status = "❌ SOME NOT MET"
         criteria_score = 5

CHECK scope_creep:
   planned_artifacts = implementation_plan.affected_artifacts
   actual_artifacts = files_changed.modified_files

   extra_work = actual_artifacts - planned_artifacts

   IF len(extra_work) == 0:
      scope_status = "✓ NO CREEP"
      scope_score = 10
   ELIF len(extra_work) <= 2:
      scope_status = "⚠ MINOR CREEP"
      scope_score = 7
   ELSE:
      scope_status = "❌ SIGNIFICANT CREEP"
      scope_score = 4

requirements_validator_score = (
   requirements_score * 0.5 +
   criteria_score * 0.3 +
   scope_score * 0.2
)

STORE requirements_validator_perspective = {
   score: requirements_validator_score,
   requirements_addressed: {status, met, missed},
   acceptance_criteria: {status, failures},
   scope_creep: {status, extra_work},
   issues: [...],
   recommendations: [...]
}

---

Perspective 2: SOLUTION ARCHITECT

Role: Validate architectural soundness and pattern adherence

Questions:
1. "Is the implementation approach architecturally sound?"
2. "Does it follow established patterns?"
3. "Is any technical debt introduced?"

CHECK architectural_soundness:
   FOR each modified_file:
      CHECK pattern_adherence:
         IF file violates_architecture_pattern:
            architecture_violations.append({
               file: modified_file,
               violation: description,
               pattern: expected_pattern
            })

   IF len(architecture_violations) == 0:
      architecture_status = "✓ SOUND"
      architecture_score = 10
   ELIF len(architecture_violations) <= 2:
      architecture_status = "⚠ MINOR ISSUES"
      architecture_score = 6
   ELSE:
      architecture_status = "❌ VIOLATIONS"
      architecture_score = 2

CHECK pattern_consistency:
   existing_patterns = IDENTIFY_PATTERNS(stage_folder)

   FOR each modified_file:
      file_patterns = IDENTIFY_PATTERNS_IN_FILE(modified_file)

      FOR each pattern IN file_patterns:
         IF pattern NOT IN existing_patterns:
            new_patterns.append(pattern)
         ELIF pattern.implementation != existing_patterns[pattern]:
            pattern_inconsistencies.append({
               pattern: pattern,
               expected: existing_patterns[pattern],
               actual: pattern.implementation
            })

   IF len(pattern_inconsistencies) == 0:
      pattern_status = "✓ CONSISTENT"
      pattern_score = 10
   ELSE:
      pattern_status = "❌ INCONSISTENT"
      pattern_score = 5

CHECK technical_debt:
   debt_indicators = [
      "TODO comments added",
      "Workarounds implemented",
      "Code duplication introduced",
      "Complexity increased significantly",
      "Missing error handling",
      "Hard-coded values"
   ]

   FOR each indicator:
      IF DETECT(indicator, implementation_context):
         debt_found.append(indicator)

   IF len(debt_found) == 0:
      debt_status = "✓ NO DEBT"
      debt_score = 10
   ELIF len(debt_found) <= 2:
      debt_status = "⚠ MINOR DEBT"
      debt_score = 6
   ELSE:
      debt_status = "❌ SIGNIFICANT DEBT"
      debt_score = 3

solution_architect_score = (
   architecture_score * 0.4 +
   pattern_score * 0.3 +
   debt_score * 0.3
)

STORE solution_architect_perspective = {
   score: solution_architect_score,
   architectural_soundness: {status, violations},
   pattern_consistency: {status, inconsistencies},
   technical_debt: {status, indicators_found},
   issues: [...],
   recommendations: [...]
}

---

Perspective 3: CODE QUALITY REVIEWER

Role: Validate code/content quality and maintainability

Questions:
1. "Is the content clean and maintainable?"
2. "Are conventions followed?"
3. "Is documentation adequate?"

CHECK content_cleanliness:
   quality_issues = []

   FOR each modified_file:
      CHECK readability:
         IF file has long_lines (>120 chars for code, >200 for docs):
            quality_issues.append("Long lines")

         IF file has deep_nesting (>4 levels):
            quality_issues.append("Deep nesting")

         IF file has large_sections (>200 lines):
            quality_issues.append("Large sections")

   IF len(quality_issues) == 0:
      cleanliness_status = "✓ CLEAN"
      cleanliness_score = 10
   ELIF len(quality_issues) <= 3:
      cleanliness_status = "⚠ MINOR ISSUES"
      cleanliness_score = 7
   ELSE:
      cleanliness_status = "❌ QUALITY ISSUES"
      cleanliness_score = 4

CHECK convention_adherence:
   conventions = LOAD_CONVENTIONS_FOR_STAGE(stage)

   FOR each convention:
      adhered = CHECK_CONVENTION(modified_files, convention)

      IF NOT adhered:
         convention_violations.append(convention)

   IF len(convention_violations) == 0:
      convention_status = "✓ FOLLOWED"
      convention_score = 10
   ELSE:
      convention_status = "❌ VIOLATIONS"
      convention_score = 5

CHECK documentation_adequacy:
   FOR each modified_file:
      IF file has frontmatter:
         CHECK frontmatter_complete:
            required_fields = [version, created_at, updated_at, generated_by]

            FOR each field:
               IF field NOT IN frontmatter:
                  documentation_issues.append({
                     file: modified_file,
                     missing: field
                  })

      IF file is code:
         CHECK comments:
            complex_sections = IDENTIFY_COMPLEX_SECTIONS(file)

            FOR each section:
               IF NOT has_comment(section):
                  documentation_issues.append({
                     file: modified_file,
                     location: section,
                     issue: "Complex logic without comment"
                  })

   IF len(documentation_issues) == 0:
      documentation_status = "✓ ADEQUATE"
      documentation_score = 10
   ELIF len(documentation_issues) <= 3:
      documentation_status = "⚠ MINOR GAPS"
      documentation_score = 7
   ELSE:
      documentation_status = "❌ INADEQUATE"
      documentation_score = 4

code_quality_reviewer_score = (
   cleanliness_score * 0.4 +
   convention_score * 0.3 +
   documentation_score * 0.3
)

STORE code_quality_reviewer_perspective = {
   score: code_quality_reviewer_score,
   content_cleanliness: {status, issues},
   convention_adherence: {status, violations},
   documentation_adequacy: {status, issues},
   issues: [...],
   recommendations: [...]
}
```

### Step 7: Calculate Consensus

```
CALCULATE consensus:

   perspective_scores = [
      requirements_validator_score,
      solution_architect_score,
      code_quality_reviewer_score
   ]

   consensus_score = AVG(perspective_scores)
   consensus_score = ROUND(consensus_score, 1)

   std_deviation = STDEV(perspective_scores)

   IF std_deviation > 2.0:
      consensus_confidence = "LOW" # High disagreement
   ELIF std_deviation > 1.0:
      consensus_confidence = "MEDIUM"
   ELSE:
      consensus_confidence = "HIGH" # Strong agreement

GENERATE recommendation:

   IF consensus_score >= 8.0:
      recommendation = "✅ ACCEPT"
      recommendation_label = "PASS"
      recommendation_action = "Implementation meets quality standards. Close feedback."

   ELIF consensus_score >= 6.0:
      recommendation = "⚠ ACCEPT WITH MINOR FIXES"
      recommendation_label = "CONDITIONAL PASS"
      recommendation_action = "Address minor issues identified, then close feedback."

   ELSE:
      recommendation = "❌ REVISE AND REIMPLEMENT"
      recommendation_label = "FAIL"
      recommendation_action = "Significant issues found. Return to Phase 6 with improvements."

AGGREGATE action_items:

   all_issues = (
      plan_compliance_results.issues +
      content_validation_results.errors +
      traceability_results.errors +
      requirements_validator_perspective.issues +
      solution_architect_perspective.issues +
      code_quality_reviewer_perspective.issues
   )

   PRIORITIZE action_items BY severity DESC

   critical_items = FILTER(all_issues, WHERE severity == "CRITICAL")
   high_items = FILTER(all_issues, WHERE severity == "HIGH")
   medium_items = FILTER(all_issues, WHERE severity == "MEDIUM")
```

### Step 8: Generate Output Report

```
CREATE VALIDATION_REPORT.md:

---
document_id: VAL-{feedback_id}
version: 1.0.0
created_at: {YYYY-MM-DD}
updated_at: {YYYY-MM-DD}
generated_by: Shared_FeedbackReviewer_Reflexion
feedback_id: {feedback_id}
stage: {stage}
system_name: {system_name}
---

# Validation Report - {feedback_id}

## Summary

- **Feedback ID**: {feedback_id}
- **Stage**: {stage}
- **System**: {system_name}
- **Validation Date**: {timestamp}
- **Overall Status**: {PASS|CONDITIONAL PASS|FAIL}
- **Consensus Score**: {X.X}/10
- **Consensus Confidence**: {HIGH|MEDIUM|LOW}

---

## Section 1: Plan Compliance Validation

### Execution Completeness: {status} ({score}/10)

- **Planned Steps**: {N}
- **Executed Steps**: {M}
- **Status**: {✓/⚠/❌}

{IF incomplete:}
**Missing Steps**:
- Step {N}: {description}
- Step {M}: {description}

### Step Accuracy: {status} ({score}/10)

{IF mismatches:}
**Deviations**:
- {mismatch_1}
- {mismatch_2}

### Unexpected Changes: {status} ({score}/10)

{IF unexpected:}
**Unexpected Files Modified**:
- {file_1}
- {file_2}

**Plan Compliance Score**: {X.X}/10

---

## Section 2: Content Validation

### Version Updates: {score}/10

{IF errors:}
**Version Errors**:
- {error_1}
- {error_2}

### Change History: {score}/10

{IF errors:}
**Missing Feedback References**:
- {error_1}

### Content Match: {score}/10

{IF errors:}
**Content Mismatches**:
- File: {file}
  - Section: {section}
  - Similarity: {XX}%
  - Diff: [show diff]

### Format Validity: {score}/10

{IF errors:}
**Format Errors**:
- {error_1}

**Content Validation Score**: {X.X}/10

---

## Section 3: Traceability Validation

### Registry Presence: {score}/10

{IF errors:}
**Registry Errors**:
- {error_1}

### Bidirectional Links: {score}/10

{IF errors:}
**Link Errors**:
- {error_1}

### Chain Completeness: {score}/10

{IF errors:}
**Chain Errors**:
- {error_1}

### Orphaned Artifacts: {score}/10

{IF errors:}
**Orphaned**:
- {artifact_1}

**Traceability Score**: {X.X}/10

---

## Section 4: Stage-Specific Validation

{stage_specific_results}

**Stage-Specific Score**: {X.X}/10

---

## Section 5: Reflexion Multi-Perspective Review

### Perspective 1: Requirements Validator ({score}/10)

**Requirements Addressed**: {status}
- Met: {list}
- Missed: {list}

**Acceptance Criteria**: {status}
{IF failures: - {list}}

**Scope Creep**: {status}
{IF extra_work: - {list}}

**Issues**:
- {issue_1}
- {issue_2}

**Recommendations**:
- {rec_1}
- {rec_2}

---

### Perspective 2: Solution Architect ({score}/10)

**Architectural Soundness**: {status}
{IF violations: - {list}}

**Pattern Consistency**: {status}
{IF inconsistencies: - {list}}

**Technical Debt**: {status}
{IF debt: - {list}}

**Issues**:
- {issue_1}

**Recommendations**:
- {rec_1}

---

### Perspective 3: Code Quality Reviewer ({score}/10)

**Content Cleanliness**: {status}
{IF issues: - {list}}

**Convention Adherence**: {status}
{IF violations: - {list}}

**Documentation Adequacy**: {status}
{IF issues: - {list}}

**Issues**:
- {issue_1}

**Recommendations**:
- {rec_1}

---

## Section 6: Consensus and Recommendation

### Consensus Score: {X.X}/10

| Perspective | Score |
|-------------|-------|
| Requirements Validator | {X.X}/10 |
| Solution Architect | {X.X}/10 |
| Code Quality Reviewer | {X.X}/10 |
| **Average (Consensus)** | **{X.X}/10** |

**Consensus Confidence**: {HIGH|MEDIUM|LOW}
{IF LOW: "(Perspectives show significant disagreement)"}

### Recommendation: {recommendation}

**Action**: {recommendation_action}

---

## Section 7: Action Items

{IF critical_items:}
### Critical (Must Fix)
- [ ] {item_1}
- [ ] {item_2}

{IF high_items:}
### High Priority
- [ ] {item_1}
- [ ] {item_2}

{IF medium_items:}
### Medium Priority
- [ ] {item_1}
- [ ] {item_2}

---

## Conclusion

{IF PASS:}
✅ **Implementation validated successfully.** All quality standards met. Feedback can be closed.

{IF CONDITIONAL PASS:}
⚠ **Implementation mostly acceptable.** Address {N} minor issues before closing feedback.

{IF FAIL:}
❌ **Implementation requires revision.** {N} significant issues identified. Return to implementation phase.

---

**Validated at**: {timestamp}
**Validator**: Shared_FeedbackReviewer_Reflexion

SAVE to feedback_sessions/{date}_{id}/VALIDATION_REPORT.md
```

### Step 9: Return Summary

```
RETURN {
   "status": "success",
   "output_file": "path/to/VALIDATION_REPORT.md",
   "validation_result": "PASS|CONDITIONAL PASS|FAIL",
   "consensus_score": X.X,
   "action_items_count": N,
   "critical_issues_count": M
}
```

## Stage-Specific Adaptations

### Discovery
- Focus on documentation quality
- YAML/Markdown format validation
- Traceability registry integrity

### Prototype
- Multi-layer validation (Discovery → Specs → Code)
- Build verification required
- Visual QA considerations

### ProductSpecs
- Module spec completeness
- Test case coverage
- JIRA export synchronization

### SolArch
- ADR consistency across related decisions
- Diagram accuracy
- Quality scenario completeness

### Implementation
- TDD compliance (test-first verification)
- Code coverage maintenance
- Integration test execution

## Return

Validation report with pass/fail status and actionable feedback.
