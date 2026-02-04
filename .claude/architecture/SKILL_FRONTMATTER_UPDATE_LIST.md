# Files Needing Skills Frontmatter Update

**Generated**: 2026-02-04
**Purpose**: Track agents and commands that need `skills:` field added to frontmatter

---

## Frontmatter Schema

Add this to YAML frontmatter of agents and commands:

```yaml
---
name: agent-or-command-name
description: Brief description
skills:
  required:
    - skill-name-1        # Skills that MUST be used
    - skill-name-2
  optional:
    - skill-name-3        # Skills that MAY be used
---
```

---

## Priority 1: Orchestrators (High Impact)

These orchestrators coordinate multiple skills and should be updated first:

### Discovery Orchestrators
- [ ] `agents/discovery-orchestrator.md`
  - Required: `Discovery_InterviewAnalyst`, `Discovery_DataAnalyst`, `Discovery_DesignAnalyst`, `Discovery_PdfAnalyst`, `Discovery_PainPointValidator`, `Discovery_PersonaGenerator`, `Discovery_JTBDExtractor`, `Discovery_CrossReferenceValidator`
  - Optional: `flowchart-creator`, `dashboard-creator`

### Prototype Orchestrators
- [ ] `agents/prototype-orchestrator.md`
  - Required: (extract from Available Skills section)
  - Optional: `flowchart-creator`, `dashboard-creator`, `architecture-diagram-creator`, `technical-doc-creator`

### ProductSpecs Orchestrators
- [ ] `agents/productspecs-orchestrator.md`
  - Required: `ProductSpecs_UIModuleSpecifier`, `ProductSpecs_APIModuleSpecifier`, `ProductSpecs_NFRGenerator`, `ProductSpecs_UnitTestSpecifier`, `ProductSpecs_IntegrationTestSpecifier`, `ProductSpecs_E2ETestSpecifier`, `ProductSpecs_PICTTester`, `ProductSpecs_TraceValidator`, `ProductSpecs_CrossRefValidator`, `ProductSpecs_SpecReviewer`
  - Optional: `flowchart-creator`, `dashboard-creator`, `technical-doc-creator`

### SolArch Orchestrators
- [ ] `agents/solarch-orchestrator.md`
  - Required: (extract from prose)
  - Optional: `architecture-diagram-creator`, `flowchart-creator`, `technical-doc-creator`, `dashboard-creator`

---

## Priority 2: Agents with "Available Skills" Sections (13 agents)

These agents already document skills in prose - just need frontmatter:

- [ ] `agents/discovery-kpis-generator.md` - Has Available Skills section
- [ ] `agents/implementation-developer.md` - Has Available Skills section
- [ ] `agents/implementation-test-automation-engineer.md` - Has Available Skills section
- [ ] `agents/productspecs-api-module-specifier.md` - Has Available Skills section
- [ ] `agents/solarch-c4-component-generator.md` - Has Available Skills section
- [ ] `agents/solarch-c4-container-generator.md` - Has Available Skills section
- [ ] `agents/solarch-c4-context-generator.md` - Has Available Skills section
- [ ] `agents/solarch-c4-deployment-generator.md` - Has Available Skills section
- [ ] `agents/quality-bug-hunter.md` - Has Available Skills section

---

## Priority 3: Agents with Frontmatter Skills (Already Have - Verify Format)

These already have `skills:` in frontmatter but may need format update:

- [x] `agents/discovery-persona-generator.md` - Has: `skills: jobs-to-be-done, fogg-behavior-model, hooked-model, loss-aversion-psychology`
  - **Action**: Convert to `required/optional` format
- [x] `agents/discovery-vp-pm-reviewer.md` - Has: `skills: thinking-critically, project-orchestration, business-model-canvas, game-theory-tit-for-tat, cognitive-biases, what-not-to-do-as-product-manager`
  - **Action**: Convert to `required/optional` format

---

## Priority 4: Commands with Explicit Skill Invocations (High Value)

Commands that invoke specific skills via Skill tool:

### Discovery Commands
- [ ] `commands/discovery.md` - Main orchestrator, invokes 20+ skills
- [ ] `commands/discovery-analyze.md` - Invokes Discovery_Analyze* skills
- [ ] `commands/discovery-feedback.md` - Invokes Shared_Feedback*_Reflexion skills
- [ ] `commands/discovery-personas.md` - Invokes Discovery_GeneratePersona
- [ ] `commands/discovery-jtbd.md` - Invokes Discovery_GenerateJTBD
- [ ] `commands/discovery-kpis.md` - Invokes Discovery_GenerateKPIs
- [ ] `commands/discovery-screens.md` - Invokes Discovery_SpecScreens
- [ ] `commands/discovery-components.md` - Invokes Discovery_SpecComponents
- [ ] `commands/discovery-data-fields.md` - Invokes Discovery_SpecDataModel

### Prototype Commands
- [ ] `commands/prototype.md` - Main orchestrator
- [ ] `commands/prototype-build.md` - Invokes Prototype_Builder, Prototype_CodeGen
- [ ] `commands/prototype-components.md` - Invokes Prototype_Components
- [ ] `commands/prototype-screens.md` - Invokes Prototype_Screens
- [ ] `commands/prototype-feedback.md` - Invokes Shared_Feedback*_Reflexion skills

### ProductSpecs Commands
- [ ] `commands/productspecs.md` - Main orchestrator
- [ ] `commands/productspecs-modules.md` - Invokes ProductSpecs_Generator
- [ ] `commands/productspecs-tests.md` - Invokes ProductSpecs_TestSpecGenerator
- [ ] `commands/productspecs-feedback.md` - Invokes Shared_Feedback*_Reflexion skills

### SolArch Commands
- [ ] `commands/solarch.md` - Main orchestrator
- [ ] `commands/solarch-blocks.md` - Invokes SolutionArchitecture_C4Generator
- [ ] `commands/solarch-decisions.md` - Invokes SolutionArchitecture_AdrGenerator
- [ ] `commands/solarch-feedback.md` - Invokes Shared_Feedback*_Reflexion skills

### GRC/Compliance Commands
- [ ] `commands/compliance-check.md` - Invokes GRC_* skills
- [ ] `commands/grc-assess-gdpr.md` - Invokes GRC_gdpr-compliance
- [ ] `commands/grc-assess-hipaa.md` - Invokes GRC_hipaa-compliance
- [ ] `commands/grc-assess-pci.md` - Invokes GRC_pci-dss-compliance

---

## Priority 5: Remaining Agents (95 agents)

Lower priority - these may not explicitly reference skills but could benefit from skill associations:

### Discovery Agents
- [ ] `agents/discovery-interview-analyst.md`
- [ ] `agents/discovery-data-analyst.md`
- [ ] `agents/discovery-design-analyst.md`
- [ ] `agents/discovery-pdf-analyst.md`
- [ ] `agents/discovery-pain-point-validator.md`
- [ ] `agents/discovery-jtbd-extractor.md`
- [ ] `agents/discovery-cross-reference-validator.md`
- [ ] `agents/discovery-fact-auditor-reviewer.md`
- [ ] `agents/discovery-screen-specifier.md`
- [ ] `agents/discovery-data-fields-specifier.md`
- [ ] `agents/discovery-interaction-specifier.md`
- [ ] `agents/discovery-navigation-specifier.md`
- [ ] `agents/discovery-roadmap-generator.md`
- [ ] `agents/discovery-strategy-generator.md`
- [ ] `agents/discovery-vision-generator.md`
- [ ] `agents/discovery-competitor-analyst.md`

### Prototype Agents
- [ ] `agents/prototype-screen-specifier.md`
- [ ] `agents/prototype-component-specifier.md`
- [ ] `agents/prototype-data-model-specifier.md`
- [ ] `agents/prototype-api-contract-specifier.md`
- [ ] `agents/prototype-design-token-generator.md`
- [ ] `agents/prototype-developer.md`
- [ ] `agents/prototype-tester.md`
- [ ] `agents/prototype-planner.md`
- [ ] `agents/prototype-ux-validator.md`
- [ ] `agents/prototype-visual-qa-tester.md`
- [ ] `agents/prototype-accessibility-auditor.md`
- [ ] `agents/prototype-component-validator.md`
- [ ] `agents/prototype-screen-validator.md`

### ProductSpecs Agents
- [ ] `agents/productspecs-ui-module-specifier.md`
- [ ] `agents/productspecs-nfr-generator.md`
- [ ] `agents/productspecs-unit-test-specifier.md`
- [ ] `agents/productspecs-integration-test-specifier.md`
- [ ] `agents/productspecs-e2e-test-specifier.md`
- [ ] `agents/productspecs-pict-combinatorial.md`
- [ ] `agents/productspecs-traceability-validator.md`
- [ ] `agents/productspecs-cross-reference-validator.md`
- [ ] `agents/productspecs-spec-reviewer.md`
- [ ] `agents/productspecs-vp-reviewer.md`
- [ ] `agents/productspecs-self-validator.md`
- [ ] `agents/productspecs-module-orchestrator.md`
- [ ] `agents/productspecs-test-orchestrator.md`
- [ ] `agents/productspecs-validation-orchestrator.md`

### SolArch Agents
- [ ] `agents/solarch-arch-evaluator.md`
- [ ] `agents/solarch-adr-foundation-writer.md`
- [ ] `agents/solarch-adr-communication-writer.md`
- [ ] `agents/solarch-adr-operational-writer.md`
- [ ] `agents/solarch-adr-validator.md`
- [ ] `agents/solarch-adr-board-orchestrator.md`
- [ ] `agents/solarch-tech-researcher.md`
- [ ] `agents/solarch-cost-estimator.md`
- [ ] `agents/solarch-risk-scorer.md`
- [ ] `agents/solarch-integration-analyst.md`
- [ ] `agents/solarch-performance-scenarios.md`
- [ ] `agents/solarch-reliability-scenarios.md`
- [ ] `agents/solarch-security-scenarios.md`
- [ ] `agents/solarch-usability-scenarios.md`
- [ ] `agents/solarch-architect-pragmatist.md`
- [ ] `agents/solarch-architect-perfectionist.md`
- [ ] `agents/solarch-architect-skeptic.md`
- [ ] `agents/solarch-board-consensus.md`
- [ ] `agents/solarch-self-validator.md`
- [ ] `agents/solarch-validation-orchestrator.md`

### Implementation Agents
- [ ] `agents/implementation-test-designer.md`
- [ ] `agents/implementation-documenter.md`
- [ ] `agents/implementation-pr-preparer.md`
- [ ] `agents/implementation-task-orchestrator.md`

### Planning Agents
- [ ] `agents/planning-tech-lead.md`
- [ ] `agents/planning-code-explorer.md`

### Quality Agents
- [ ] `agents/quality-code-quality.md`
- [ ] `agents/quality-security-auditor.md`
- [ ] `agents/quality-test-coverage.md`
- [ ] `agents/quality-contracts-reviewer.md`
- [ ] `agents/quality-accessibility-auditor.md`
- [ ] `agents/quality-spec-reviewer.md`
- [ ] `agents/quality-cross-validator.md`

### Process Integrity Agents
- [ ] `agents/process-integrity-traceability-guardian.md`
- [ ] `agents/process-integrity-checkpoint-auditor.md`
- [ ] `agents/process-integrity-state-watchdog.md`
- [ ] `agents/process-integrity-playbook-enforcer.md`

### Reflexion Agents
- [ ] `agents/reflexion-actor.md`
- [ ] `agents/reflexion-evaluator.md`
- [ ] `agents/reflexion-self-refiner.md`

### GRC Agents
- [ ] `agents/compliance-analyst.md`
- [ ] `agents/privacy-officer.md`
- [ ] `agents/security-auditor.md`

### Utility Agents
- [ ] `agents/project-orchestrator.md`
- [ ] `agents/agent-expert.md`
- [ ] `agents/test-demo-agent.md`
- [ ] `agents/trace-audit-consolidator.md`
- [ ] `agents/trace-audit-registry-scanner.md`
- [ ] `agents/trace-audit-state-analyzer.md`
- [ ] `agents/trace-audit-json-discovery.md`

---

## Validation Script

Run validation after updates:

```bash
# Check all skill references are valid
python3 .claude/hooks/validate_skill_references.py

# Generate detailed report
python3 .claude/hooks/validate_skill_references.py --report

# List files still needing updates
python3 .claude/hooks/validate_skill_references.py --list-needed

# JSON output for CI/CD
python3 .claude/hooks/validate_skill_references.py --json
```

---

## Progress Tracking

| Priority | Total | Updated | Remaining |
|----------|-------|---------|-----------|
| P1: Orchestrators | 4 | 0 | 4 |
| P2: With Available Skills | 9 | 0 | 9 |
| P3: Format Update | 2 | 0 | 2 |
| P4: Commands | 25 | 0 | 25 |
| P5: Remaining Agents | 95 | 0 | 95 |
| **Total** | **135** | **0** | **135** |

---

## Notes

1. **Keep prose sections**: The frontmatter supplements, not replaces, the prose documentation
2. **Required vs Optional**:
   - `required`: Skills that MUST be invoked when conditions apply
   - `optional`: Skills that MAY enhance output but aren't mandatory
3. **Validation**: Run `validate_skill_references.py` after each batch of updates
4. **Skill names**: Must match folder names in `.claude/skills/` exactly
