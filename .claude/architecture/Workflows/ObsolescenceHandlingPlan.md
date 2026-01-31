# Obsolescence Handling Plan

**Version**: 1.0.0
**Created**: 2025-12-26
**Status**: ✅ IMPLEMENTED
**Completed**: 2025-12-26
**Author**: HTEC ClaudeCode Accelerators Team

---

## Executive Summary

This plan introduces **Smart Obsolescence Handling** - a mechanism that allows the HTEC ClaudeCode Accelerators framework to intelligently determine when specific artifacts are not applicable to a given project domain, while maintaining full framework integrity, traceability, and validation.

### Problem Statement

The current framework assumes all projects require all artifacts:
- Screen definitions
- UI components
- Navigation structures
- Design tokens
- React prototypes

This assumption fails for:
- **Integration/Middleware projects** - No UI, just APIs and data flows
- **Database-only brownfield projects** - Schema changes, ETL, no application layer
- **Backend services** - APIs, workers, schedulers without frontend
- **Data pipelines** - ETL, analytics, no user-facing screens
- **Infrastructure projects** - DevOps, cloud setup, no application code

### Solution: NOT_APPLICABLE Artifacts

Instead of skipping artifacts (which breaks traceability), we produce **placeholder artifacts** with:
1. Clear `NOT_APPLICABLE` status
2. Reasoning for the decision
3. Full traceability metadata
4. Valid structure that passes quality gates

---

## Design Principles

### 1. Determinism
Every skill MUST produce its expected output file, regardless of applicability.

### 2. Traceability Preservation
NOT_APPLICABLE artifacts maintain full traceability chains:
```
CM-XXX → PP-X.X → JTBD-X.X → [artifact marked N/A with reason]
```

### 3. Quality Gate Compliance
NOT_APPLICABLE is a valid status. Quality gates PASS if:
- File exists
- Has proper NOT_APPLICABLE structure
- Has documented reasoning
- Has traceability metadata

### 4. State Management Consistency
Progress tracking treats N/A artifacts as completed:
```json
{
  "checkpoint": 9,
  "status": "completed",
  "artifacts": {
    "screen-definitions.md": "not_applicable",
    "navigation-structure.md": "not_applicable",
    "data-fields.md": "completed"
  }
}
```

### 5. Explicit Over Implicit
Never silently skip. Always document WHY something is not applicable.

---

## Architecture

### Project Type Classification

During Discovery Phase 1 (Analyze), classify the project:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT TYPE DETECTION                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Signals from Client Materials → Project Type Classification    │
│                                                                  │
│  ┌─────────────────┐     ┌─────────────────────────────────┐   │
│  │ UI Screenshots  │ ──▶ │ FULL_STACK (default)            │   │
│  │ Screen mentions │     │ - All artifacts applicable       │   │
│  │ User workflows  │     └─────────────────────────────────┘   │
│  └─────────────────┘                                            │
│                                                                  │
│  ┌─────────────────┐     ┌─────────────────────────────────┐   │
│  │ API specs       │ ──▶ │ BACKEND_ONLY                    │   │
│  │ No UI mentions  │     │ - UI artifacts → N/A             │   │
│  │ Service docs    │     │ - API/Data artifacts → active    │   │
│  └─────────────────┘     └─────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────┐     ┌─────────────────────────────────┐   │
│  │ DB schemas      │ ──▶ │ DATABASE_ONLY                   │   │
│  │ Migration docs  │     │ - UI/API artifacts → N/A         │   │
│  │ ETL mentions    │     │ - Data model artifacts → active  │   │
│  └─────────────────┘     └─────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────┐     ┌─────────────────────────────────┐   │
│  │ Integration     │ ──▶ │ INTEGRATION                     │   │
│  │ Middleware      │     │ - UI artifacts → N/A             │   │
│  │ Event-driven    │     │ - API/Event artifacts → active   │   │
│  └─────────────────┘     └─────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────┐     ┌─────────────────────────────────┐   │
│  │ Infra docs      │ ──▶ │ INFRASTRUCTURE                  │   │
│  │ Cloud setup     │     │ - App artifacts → N/A            │   │
│  │ DevOps focus    │     │ - Infra artifacts → active       │   │
│  └─────────────────┘     └─────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Artifact Applicability Matrix

| Artifact | FULL_STACK | BACKEND_ONLY | DATABASE_ONLY | INTEGRATION | INFRASTRUCTURE |
|----------|------------|--------------|---------------|-------------|----------------|
| screen-definitions.md | ✅ | ❌ N/A | ❌ N/A | ❌ N/A | ❌ N/A |
| navigation-structure.md | ✅ | ❌ N/A | ❌ N/A | ❌ N/A | ❌ N/A |
| ui-components.md | ✅ | ❌ N/A | ❌ N/A | ❌ N/A | ❌ N/A |
| design-tokens.json | ✅ | ❌ N/A | ❌ N/A | ❌ N/A | ❌ N/A |
| interaction-patterns.md | ✅ | ❌ N/A | ❌ N/A | ❌ N/A | ❌ N/A |
| data-fields.md | ✅ | ✅ | ✅ | ✅ | ❌ N/A |
| api-contracts.json | ✅ | ✅ | ❌ N/A | ✅ | ❌ N/A |
| data-model.md | ✅ | ✅ | ✅ | ✅ | ❌ N/A |
| PRODUCT_VISION.md | ✅ | ✅ | ✅ | ✅ | ✅ |
| PRODUCT_STRATEGY.md | ✅ | ✅ | ✅ | ✅ | ✅ |
| JOBS_TO_BE_DONE.md | ✅ | ✅ | ✅ | ✅ | ✅ |
| PAIN_POINTS.md | ✅ | ✅ | ✅ | ✅ | ✅ |
| personas/ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## NOT_APPLICABLE File Template

### Markdown Artifacts

```markdown
---
document_id: [ARTIFACT_ID]
version: 1.0.0
created_at: [TIMESTAMP]
updated_at: [TIMESTAMP]
generated_by: [SKILL_NAME]
status: NOT_APPLICABLE
---

# [Artifact Title]

## Status: NOT APPLICABLE

This artifact has been marked as **NOT APPLICABLE** for the current project.

### Reason

[Clear explanation of why this artifact is not needed]

### Project Classification

- **Project Type**: [BACKEND_ONLY | DATABASE_ONLY | INTEGRATION | INFRASTRUCTURE]
- **Detected Signals**:
  - [Signal 1 from client materials]
  - [Signal 2 from client materials]
  - [Signal 3 from client materials]

### Decision Metadata

| Field | Value |
|-------|-------|
| Decision Date | [TIMESTAMP] |
| Deciding Skill | [SKILL_NAME] |
| Checkpoint | [CHECKPOINT_NUMBER] |
| Confidence | [HIGH | MEDIUM] |

### Traceability

This decision traces to:
- **Analysis Summary**: [Link to ANALYSIS_SUMMARY.md section]
- **Project Type Detection**: [Link to project_classification in config]

### Override Instructions

If this artifact becomes applicable in the future:

1. Update `_state/discovery_config.json` → `project_type`
2. Re-run: `/discovery-specs-all`
3. Or manually create the artifact following the template

---

*This placeholder maintains framework integrity while acknowledging that not all artifacts apply to every project type.*
```

### JSON Artifacts

```json
{
  "$documentation": {
    "purpose": "[Original purpose]",
    "stage": "[Stage]",
    "status": "NOT_APPLICABLE"
  },
  "status": "NOT_APPLICABLE",
  "reason": "[Clear explanation]",
  "project_type": "[PROJECT_TYPE]",
  "detected_signals": [
    "Signal 1",
    "Signal 2"
  ],
  "decision_metadata": {
    "decision_date": "[TIMESTAMP]",
    "deciding_skill": "[SKILL_NAME]",
    "checkpoint": "[N]",
    "confidence": "HIGH"
  },
  "traceability": {
    "analysis_summary_ref": "[Section reference]",
    "config_ref": "_state/discovery_config.json#project_type"
  },
  "items": []
}
```

---

## Registry Entry Format for N/A Items

### screen_registry.json (when N/A)

```json
{
  "$documentation": {
    "purpose": "Registry of screen definitions",
    "stage": "Prototype",
    "status": "NOT_APPLICABLE"
  },
  "schema_version": "1.0.0",
  "status": "NOT_APPLICABLE",
  "reason": "Project classified as BACKEND_ONLY - no user-facing screens",
  "project_type": "BACKEND_ONLY",
  "items": [],
  "summary": {
    "total_screens": 0,
    "status": "not_applicable"
  }
}
```

### Traceability Links for N/A

```json
{
  "id": "SCR-N/A-001",
  "status": "not_applicable",
  "reason": "Project type BACKEND_ONLY has no UI screens",
  "upstream_refs": ["REQ-001", "REQ-002"],
  "note": "Requirements addressed through API endpoints instead"
}
```

---

## State Management Updates

### discovery_config.json

Add project classification:

```json
{
  "system_name": "IntegrationProject",
  "project_classification": {
    "type": "INTEGRATION",
    "detected_at": "2025-12-26T10:00:00Z",
    "confidence": "HIGH",
    "signals": [
      "No UI screenshots in client materials",
      "API specification documents present",
      "Integration diagrams found",
      "No user workflow descriptions"
    ],
    "artifact_applicability": {
      "screen-definitions": false,
      "navigation-structure": false,
      "ui-components": false,
      "design-tokens": false,
      "data-fields": true,
      "api-contracts": true,
      "data-model": true
    }
  }
}
```

### discovery_progress.json

Track N/A status:

```json
{
  "checkpoints": {
    "9": {
      "status": "completed",
      "artifacts": {
        "screen-definitions.md": {
          "status": "not_applicable",
          "reason": "INTEGRATION project type"
        },
        "data-fields.md": {
          "status": "completed",
          "path": "04-design-specs/data-fields.md"
        }
      }
    }
  }
}
```

---

## Quality Gate Updates

### Validation Rules for N/A

Quality gates must accept N/A artifacts. Update validation logic:

```python
def validate_artifact(file_path: str) -> ValidationResult:
    content = read_file(file_path)

    # Check for NOT_APPLICABLE status
    if is_not_applicable(content):
        return validate_not_applicable_format(content)

    # Normal validation
    return validate_active_artifact(content)

def validate_not_applicable_format(content: str) -> ValidationResult:
    """Validate that N/A artifact has required structure."""
    required_fields = [
        "status: NOT_APPLICABLE",
        "reason",
        "project_type" or "Project Classification",
        "Decision Metadata" or "decision_metadata"
    ]

    for field in required_fields:
        if field not in content:
            return ValidationResult(
                valid=False,
                error=f"N/A artifact missing required field: {field}"
            )

    return ValidationResult(valid=True, status="not_applicable")
```

### Checkpoint Validation

```python
def validate_checkpoint(checkpoint: int, artifacts: dict) -> bool:
    for artifact_name, artifact_info in artifacts.items():
        if artifact_info["status"] == "not_applicable":
            # N/A is valid - check format only
            if not validate_na_format(artifact_info["path"]):
                return False
        else:
            # Normal validation
            if not validate_artifact(artifact_info["path"]):
                return False
    return True
```

---

## Skill Updates Pattern

Every skill that produces potentially-N/A artifacts must follow this pattern:

```python
# Pseudo-code for skill execution

def execute_skill():
    # 1. Load project configuration
    config = load_config("_state/discovery_config.json")
    project_type = config.get("project_classification", {}).get("type", "FULL_STACK")

    # 2. Check applicability
    applicable = check_artifact_applicability(
        artifact_type=ARTIFACT_TYPE,
        project_type=project_type
    )

    # 3. Branch based on applicability
    if applicable:
        # Normal execution - generate full artifact
        content = generate_artifact_content()
    else:
        # Generate N/A placeholder
        content = generate_na_placeholder(
            artifact_type=ARTIFACT_TYPE,
            reason=get_na_reason(project_type),
            project_type=project_type
        )

    # 4. Write output (ALWAYS - never skip)
    write_artifact(OUTPUT_PATH, content)

    # 5. Update state (ALWAYS)
    update_progress(
        checkpoint=CHECKPOINT,
        artifact=ARTIFACT_NAME,
        status="not_applicable" if not applicable else "completed"
    )

    # 6. Update traceability (ALWAYS)
    update_registry(
        registry=REGISTRY_NAME,
        status="not_applicable" if not applicable else "active",
        reason=get_na_reason(project_type) if not applicable else None
    )
```

---

## Implementation Phases

### Phase 1: Foundation ✅ COMPLETE

1. **Add project classification to Discovery Phase 1** ✅
   - Created `na_validation_utils.py` shared utility
   - Added `project_classification` support to all config files
   - Created `ARTIFACT_APPLICABILITY` matrix

2. **Create N/A templates** ✅
   - Markdown and JSON templates embedded in skills
   - Consistent format across all stages

3. **Update quality gates** ✅
   - Added N/A validation to all 5 quality gate scripts
   - Added `--validate-na-file`, `--show-classification`, `--list-na-artifacts` flags

### Phase 2: Discovery Skills ✅ COMPLETE

4. **Update Discovery design spec skills** ✅
   - All Discovery_Spec* skills have Applicability Check sections
   - N/A placeholder templates for non-UI projects

5. **Update state management** ✅
   - Progress tracking treats N/A as valid completion
   - Registry entries support NOT_APPLICABLE status

### Phase 3: Prototype Skills ✅ COMPLETE

6. **Update Prototype skills** ✅
   - `Prototype_DesignTokens`, `Prototype_Components`, `Prototype_Screens` updated
   - API-only code generation mode for non-UI projects

7. **Update Prototype quality gates** ✅
   - Accept N/A screen registry
   - Accept N/A component specs

### Phase 4: Downstream Stages ✅ COMPLETE

8. **ProductSpecs handling** ✅
   - `ProductSpecs_Generator` v4.0.0 - Module Applicability Matrix
   - `ProductSpecs_JIRAExporter` v3.0.0 - Skips [FE]/[A11Y] sub-tasks for non-UI

9. **SolArch handling** ✅
   - `SolutionArchitecture_Generator` v2.0.0 - Architecture Artifact Matrix
   - `SolutionArchitecture_C4Generator` v2.0.0 - Backend-only diagram templates
   - `SolutionArchitecture_AdrGenerator` v2.0.0 - ADR-008 N/A for non-UI

10. **Implementation handling** ✅
    - `Implementation_TaskDecomposer` v2.0.0 - Skips component/screen tasks
    - `Implementation_CodeReview` v2.0.0 - Skips accessibility-auditor
    - `Implementation_Integrator` v2.0.0 - Skips E2E UI tests

---

## Testing Strategy

### Test Scenarios

1. **FULL_STACK project** (baseline)
   - All artifacts generated normally
   - No N/A placeholders

2. **BACKEND_ONLY project**
   - UI artifacts → N/A
   - API/Data artifacts → Normal
   - Verify quality gates pass

3. **DATABASE_ONLY project**
   - UI + API artifacts → N/A
   - Data model artifacts → Normal

4. **INTEGRATION project**
   - UI artifacts → N/A
   - API + Event artifacts → Normal

5. **Mixed signals**
   - Partial UI mentions → Prompt for clarification
   - Confidence < HIGH → Ask user

### Validation Tests

```bash
# Test N/A file passes validation
python3 .claude/hooks/discovery_quality_gates.py \
  --validate-file ClientAnalysis_API/04-design-specs/screen-definitions.md

# Test checkpoint with N/A artifacts passes
python3 .claude/hooks/discovery_quality_gates.py \
  --validate-checkpoint 9 --dir ClientAnalysis_API/

# Test integrity check handles N/A
python3 .claude/hooks/integrity_checker.py
```

---

## Risk Mitigation

### Risk 1: False N/A Classification

**Mitigation**:
- Require HIGH confidence for automatic N/A
- MEDIUM confidence → Ask user
- Add `--force-full-stack` flag to override

### Risk 2: Incomplete N/A Templates

**Mitigation**:
- Quality gates validate N/A format
- Missing fields → Validation failure

### Risk 3: Traceability Gaps

**Mitigation**:
- N/A items still have IDs
- Upstream links preserved
- Explicit "addressed by alternative" notes

### Risk 4: Downstream Stage Confusion

**Mitigation**:
- `discovery_summary.json` includes project_type
- Downstream stages read classification first
- Clear N/A propagation

---

## Success Criteria

1. **Framework Integrity**: `/integrity-check` passes with N/A artifacts
2. **Quality Gates**: All checkpoints pass with proper N/A files
3. **Traceability**: Full chain maintained even for N/A items
4. **Determinism**: Same inputs → Same N/A decisions
5. **Testability**: N/A handling can be unit tested
6. **Maintainability**: Single template source for N/A format

---

## Appendix: Project Type Detection Signals

### FULL_STACK Signals
- Screenshots of UI in materials
- "User clicks", "User sees", "Screen shows" language
- Wireframes or mockups
- User story format with UI acceptance criteria

### BACKEND_ONLY Signals
- API specification documents (OpenAPI, Swagger)
- "Endpoint", "Request/Response" language
- No UI screenshots
- Service-to-service communication focus

### DATABASE_ONLY Signals
- Schema diagrams
- "Table", "Column", "Migration" language
- ETL documentation
- No application layer mentions

### INTEGRATION Signals
- "Integrate with", "Connect to" language
- Event/message documentation
- Multiple system mentions
- Middleware focus

### INFRASTRUCTURE Signals
- Cloud provider documentation
- "Deploy", "Scale", "Monitor" language
- Infrastructure diagrams
- No application logic focus

---

*Document Version: 1.0.0*
*Last Updated: 2025-12-26*
