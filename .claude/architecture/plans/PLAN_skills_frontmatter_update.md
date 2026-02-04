# Execution Plan: Skills Frontmatter Update

**Plan ID**: PLAN-SKILLS-FM-001
**Created**: 2026-02-04
**Status**: PENDING
**Estimated Files**: 135 (4 orchestrator agents + 9 agents with Available Skills + 25 key commands + 97 remaining)

---

## Overview

Add `skills:` field to frontmatter of all agents and commands that reference skills. This enables:
- Machine-readable skill dependencies
- Automated validation
- Registry synchronization
- IDE autocomplete

---

## Schema

### Frontmatter Format

```yaml
---
name: <agent-or-command-name>
description: <existing description>
skills:
  required:
    - skill-name-1    # MUST be invoked when conditions apply
    - skill-name-2
  optional:
    - skill-name-3    # MAY be used for enhanced output
    - skill-name-4
# ... other existing frontmatter fields
---
```

### Rules

1. **Skill names must match** folder names in `.claude/skills/` exactly
2. **required**: Skills that are explicitly invoked or mandatory for the agent/command
3. **optional**: Skills mentioned as "may use", "when needed", or for enhanced output
4. **Keep prose sections**: Frontmatter supplements, not replaces, existing documentation
5. **Position**: Add `skills:` after `description:` field

---

## Batch 1: Orchestrator Agents (Priority 1)

### File: `agents/discovery-orchestrator.md`

**Current frontmatter**: Has `name`, `description`, etc. - NO `skills:` field

**Add after description**:
```yaml
skills:
  required:
    - Discovery_InterviewAnalyst
    - Discovery_DataAnalyst
    - Discovery_DesignAnalyst
    - Discovery_PdfAnalyst
    - Discovery_PainPointValidator
    - Discovery_PersonaGenerator
    - Discovery_JTBDExtractor
    - Discovery_CrossReferenceValidator
  optional:
    - flowchart-creator
    - dashboard-creator
    - using-htec-accelerators
```

---

### File: `agents/prototype-orchestrator.md`

**Add after description**:
```yaml
skills:
  required:
    - Prototype_DataModelSpecifier
    - Prototype_APIContractSpecifier
    - Prototype_DesignTokenGenerator
    - Prototype_ComponentSpecifier
    - Prototype_ScreenSpecifier
    - Prototype_Planner
    - Prototype_Developer
    - Prototype_Tester
    - Prototype_ComponentValidator
    - Prototype_ScreenValidator
    - Prototype_UXValidator
    - Prototype_AccessibilityAuditor
    - Prototype_VisualQATester
  optional:
    - flowchart-creator
    - dashboard-creator
    - architecture-diagram-creator
    - technical-doc-creator
    - using-htec-accelerators
```

---

### File: `agents/productspecs-orchestrator.md`

**Add after description**:
```yaml
skills:
  required:
    - ProductSpecs_UIModuleSpecifier
    - ProductSpecs_APIModuleSpecifier
    - ProductSpecs_NFRGenerator
    - ProductSpecs_UnitTestSpecifier
    - ProductSpecs_IntegrationTestSpecifier
    - ProductSpecs_E2ETestSpecifier
    - ProductSpecs_PICTTester
    - ProductSpecs_TraceValidator
    - ProductSpecs_CrossRefValidator
    - ProductSpecs_SpecReviewer
    - ProductSpecs_JIRAExporter
    - ProductSpecs_ExtractRequirements
  optional:
    - flowchart-creator
    - dashboard-creator
    - technical-doc-creator
    - using-htec-accelerators
```

---

### File: `agents/solarch-orchestrator.md`

**Add after description**:
```yaml
skills:
  required:
    - SolutionArchitecture_TechResearcher
    - SolutionArchitecture_IntegrationAnalyst
    - SolutionArchitecture_CostEstimator
    - SolutionArchitecture_ADRFoundationWriter
    - SolutionArchitecture_ADRBoardOrchestrator
    - SolutionArchitecture_C4ContextGenerator
    - SolutionArchitecture_C4ContainerGenerator
    - SolutionArchitecture_C4ComponentGenerator
    - SolutionArchitecture_C4DeploymentGenerator
    - SolutionArchitecture_PerformanceScenarios
    - SolutionArchitecture_SecurityScenarios
    - SolutionArchitecture_ReliabilityScenarios
    - SolutionArchitecture_UsabilityScenarios
    - SolutionArchitecture_ADRCommunicationWriter
    - SolutionArchitecture_ADROperationalWriter
    - SolutionArchitecture_ADRValidator
    - SolutionArchitecture_ArchEvaluator
    - SolutionArchitecture_RiskScorer
    - SolutionArchitecture_ValidationOrchestrator
  optional:
    - architecture-diagram-creator
    - flowchart-creator
    - technical-doc-creator
    - dashboard-creator
    - using-htec-accelerators
```

---

## Batch 2: Agents with Available Skills Sections (Priority 2)

### File: `agents/implementation-developer.md`

**Add after description**:
```yaml
skills:
  required:
    - systematic-debugging
    - using-htec-accelerators
  optional:
    - test-driven-development
```

---

### File: `agents/implementation-test-automation-engineer.md`

**Add after description**:
```yaml
skills:
  required:
    - systematic-debugging
    - using-htec-accelerators
  optional: []
```

---

### File: `agents/quality-bug-hunter.md`

**Add after description**:
```yaml
skills:
  required:
    - systematic-debugging
  optional: []
```

---

### File: `agents/discovery-kpis-generator.md`

**Add after description**:
```yaml
skills:
  required:
    - Discovery_GenerateKPIs
  optional:
    - dashboard-creator
```

---

### File: `agents/productspecs-api-module-specifier.md`

**Add after description**:
```yaml
skills:
  required:
    - ProductSpecs_APIModuleSpecifier
  optional:
    - technical-doc-creator
    - flowchart-creator
```

---

### File: `agents/solarch-c4-context-generator.md`

**Add after description**:
```yaml
skills:
  required:
    - SolutionArchitecture_C4Generator
  optional:
    - architecture-diagram-creator
```

---

### File: `agents/solarch-c4-container-generator.md`

**Add after description**:
```yaml
skills:
  required:
    - SolutionArchitecture_C4Generator
  optional:
    - architecture-diagram-creator
```

---

### File: `agents/solarch-c4-component-generator.md`

**Add after description**:
```yaml
skills:
  required:
    - SolutionArchitecture_C4Generator
  optional:
    - architecture-diagram-creator
```

---

### File: `agents/solarch-c4-deployment-generator.md`

**Add after description**:
```yaml
skills:
  required:
    - SolutionArchitecture_C4Generator
  optional:
    - architecture-diagram-creator
```

---

## Batch 3: Format Update (Priority 3)

### File: `agents/discovery-persona-generator.md`

**Current**:
```yaml
skills: jobs-to-be-done, fogg-behavior-model, hooked-model, loss-aversion-psychology
```

**Change to**:
```yaml
skills:
  required:
    - Discovery_GeneratePersona
  optional:
    - jobs-to-be-done
    - fogg-behavior-model
    - hooked-model
    - loss-aversion-psychology
```

---

### File: `agents/discovery-vp-pm-reviewer.md`

**Current**:
```yaml
skills: thinking-critically, project-orchestration, business-model-canvas, game-theory-tit-for-tat, cognitive-biases, what-not-to-do-as-product-manager
```

**Change to**:
```yaml
skills:
  required: []
  optional:
    - thinking-critically
    - project-orchestration
    - business-model-canvas
    - game-theory-tit-for-tat
    - cognitive-biases
    - what-not-to-do-as-product-manager
```

---

## Batch 4: Key Commands (Priority 4)

### File: `commands/discovery.md`

**Add after description**:
```yaml
skills:
  required:
    - Discovery_Orchestrator
    - Discovery_ClassifyProject
    - Discovery_AnalyzeDocument
    - Discovery_AnalyzeSpreadsheet
    - Discovery_AnalyzePresentation
    - Discovery_AnalyzeScreenshot
    - Discovery_AnalyzeAudioVideo
    - Discovery_AnalyzeData
    - Discovery_AnalyzeInterview
    - Discovery_ExtractPainPoints
    - Discovery_ExtractUserTypes
    - Discovery_ExtractWorkflows
    - Discovery_ExtractQuotes
    - Discovery_ExtractMetrics
    - Discovery_GeneratePersona
    - Discovery_GenerateJTBD
    - Discovery_GenerateVision
    - Discovery_GenerateStrategy
    - Discovery_GenerateRoadmap
    - Discovery_GenerateKPIs
    - Discovery_SpecScreens
    - Discovery_SpecNavigation
    - Discovery_SpecDataModel
    - Discovery_SpecSampleData
    - Discovery_SpecComponents
    - Discovery_SpecInteractions
    - Discovery_DocIndex
    - Discovery_DocSummary
    - Discovery_Validate
  optional: []
```

---

### File: `commands/prototype.md`

**Add after description**:
```yaml
skills:
  required:
    - Prototype_ValidateDiscovery
    - Prototype_Requirements
    - Prototype_DataModel
    - Prototype_ApiContracts
    - Prototype_TestData
    - Prototype_DesignBrief
    - Prototype_DesignTokens
    - Prototype_Components
    - Prototype_Screens
    - Prototype_Interactions
    - Prototype_Sequencer
    - Prototype_CodeGen
    - Prototype_QA
    - Prototype_UIAudit
  optional: []
```

---

### File: `commands/productspecs.md`

**Add after description**:
```yaml
skills:
  required:
    - ProductSpecs_Generator
    - ProductSpecs_ExtractRequirements
    - ProductSpecs_JIRAExporter
    - ProductSpecs_TestSpecGenerator
    - ProductSpecs_Validate
  optional: []
```

---

### File: `commands/solarch.md`

**Add after description**:
```yaml
skills:
  required:
    - SolutionArchitecture_Generator
    - SolutionArchitecture_C4Generator
    - SolutionArchitecture_AdrGenerator
    - SolutionArchitecture_Arc42Generator
    - SolutionArchitecture_InformationDesignGenerator
    - SolutionArchitecture_E2ETraceabiliyAnalyzer
  optional: []
```

---

### File: `commands/discovery-feedback.md`

**Add after description**:
```yaml
skills:
  required:
    - Shared_FeedbackImpactAnalyzer_Reflexion
    - Shared_FeedbackPlanGenerator_Reflexion
    - Shared_FeedbackReviewer_Reflexion
  optional: []
```

---

### File: `commands/prototype-feedback.md`

**Add after description**:
```yaml
skills:
  required:
    - Shared_FeedbackImpactAnalyzer_Reflexion
    - Shared_FeedbackPlanGenerator_Reflexion
    - Shared_FeedbackReviewer_Reflexion
  optional: []
```

---

### File: `commands/productspecs-feedback.md`

**Add after description**:
```yaml
skills:
  required:
    - Shared_FeedbackImpactAnalyzer_Reflexion
    - Shared_FeedbackPlanGenerator_Reflexion
    - Shared_FeedbackReviewer_Reflexion
  optional: []
```

---

### File: `commands/solarch-feedback.md`

**Add after description**:
```yaml
skills:
  required:
    - Shared_FeedbackImpactAnalyzer_Reflexion
    - Shared_FeedbackPlanGenerator_Reflexion
    - Shared_FeedbackReviewer_Reflexion
  optional: []
```

---

### File: `commands/compliance-check.md`

**Add after description**:
```yaml
skills:
  required: []
  optional:
    - GRC_quality-manager-qms-iso13485
    - GRC_gdpr-dsgvo-expert
    - GRC_data-privacy-compliance
    - GRC_fda-consultant-specialist
    - GRC_mdr-745-specialist
    - GRC_information-security-manager-iso27001
    - GRC_risk-management-specialist
```
**Note**: GRC skills are conditional based on `--standard` argument, so marked as optional.

---

### File: `commands/discovery-analyze.md`

**Add after description**:
```yaml
skills:
  required:
    - Discovery_AnalyzeDocument
    - Discovery_AnalyzeSpreadsheet
    - Discovery_AnalyzePresentation
    - Discovery_AnalyzeScreenshot
    - Discovery_AnalyzeAudioVideo
    - Discovery_AnalyzeData
    - Discovery_AnalyzeInterview
    - Discovery_AnalyzePDF
  optional: []
```

---

### File: `commands/discovery-personas.md`

**Add after description**:
```yaml
skills:
  required:
    - Discovery_GeneratePersona
  optional: []
```

---

### File: `commands/discovery-jtbd.md`

**Add after description**:
```yaml
skills:
  required:
    - Discovery_GenerateJTBD
  optional: []
```

---

### File: `commands/discovery-kpis.md`

**Add after description**:
```yaml
skills:
  required:
    - Discovery_GenerateKPIs
  optional: []
```

---

### File: `commands/discovery-screens.md`

**Add after description**:
```yaml
skills:
  required:
    - Discovery_SpecScreens
  optional: []
```

---

### File: `commands/discovery-components.md`

**Add after description**:
```yaml
skills:
  required:
    - Discovery_SpecComponents
  optional: []
```

---

### File: `commands/discovery-data-fields.md`

**Add after description**:
```yaml
skills:
  required:
    - Discovery_SpecDataModel
  optional: []
```

---

### File: `commands/prototype-build.md`

**Add after description**:
```yaml
skills:
  required:
    - Prototype_Builder
    - Prototype_Sequencer
    - Prototype_CodeGen
  optional: []
```

---

### File: `commands/prototype-components.md`

**Add after description**:
```yaml
skills:
  required:
    - Prototype_Components
  optional: []
```

---

### File: `commands/prototype-screens.md`

**Add after description**:
```yaml
skills:
  required:
    - Prototype_Screens
  optional: []
```

---

### File: `commands/productspecs-modules.md`

**Add after description**:
```yaml
skills:
  required:
    - ProductSpecs_Generator
  optional: []
```

---

### File: `commands/productspecs-tests.md`

**Add after description**:
```yaml
skills:
  required:
    - ProductSpecs_TestSpecGenerator
  optional: []
```

---

### File: `commands/solarch-blocks.md`

**Add after description**:
```yaml
skills:
  required:
    - SolutionArchitecture_C4Generator
    - SolutionArchitecture_Arc42Generator
  optional: []
```

---

### File: `commands/solarch-decisions.md`

**Add after description**:
```yaml
skills:
  required:
    - SolutionArchitecture_AdrGenerator
  optional: []
```

---

## Batch 5: Remaining Files

For remaining agents and commands, follow this pattern:

1. **Read the file** to identify skill references
2. **Check for patterns**:
   - `Skill tool` invocations
   - `.claude/skills/` references
   - `Discovery_*`, `Prototype_*`, `ProductSpecs_*`, `SolutionArchitecture_*`, `GRC_*`, `Shared_*` patterns
3. **Add frontmatter** using the schema above
4. **Run validation** after each batch

### Template for agents without explicit skill references:

```yaml
skills:
  required: []
  optional: []
```

---

## Execution Steps

### Step 1: Backup
```bash
# Create backup of agents and commands
cp -r .claude/agents .claude/agents.bak
cp -r .claude/commands .claude/commands.bak
```

### Step 2: Execute Batch 1 (Orchestrators)
- Edit 4 files
- Run validation

### Step 3: Execute Batch 2 (Available Skills agents)
- Edit 9 files
- Run validation

### Step 4: Execute Batch 3 (Format updates)
- Edit 2 files
- Run validation

### Step 5: Execute Batch 4 (Key commands)
- Edit 25 files
- Run validation

### Step 6: Execute Batch 5 (Remaining)
- Edit remaining files incrementally
- Run validation after each sub-batch

### Step 7: Final Validation
```bash
python3 .claude/hooks/validate_skill_references.py --report > VALIDATION_REPORT.md
```

---

## Verification

After each batch, run:
```bash
python3 .claude/hooks/verify_skills_frontmatter.py --batch N
```

After all batches:
```bash
python3 .claude/hooks/verify_skills_frontmatter.py --full
```

---

## Rollback

If issues occur:
```bash
# Restore from backup
rm -rf .claude/agents
mv .claude/agents.bak .claude/agents

rm -rf .claude/commands
mv .claude/commands.bak .claude/commands
```

---

## Progress Tracking

| Batch | Files | Status | Validated |
|-------|-------|--------|-----------|
| 1 - Orchestrators | 4 | ⬜ PENDING | ⬜ |
| 2 - Available Skills | 9 | ⬜ PENDING | ⬜ |
| 3 - Format Update | 2 | ⬜ PENDING | ⬜ |
| 4 - Key Commands | 25 | ⬜ PENDING | ⬜ |
| 5 - Remaining | 95 | ⬜ PENDING | ⬜ |
| **Total** | **135** | | |

---

## Success Criteria

1. All files have `skills:` field in frontmatter
2. All referenced skills exist in `.claude/skills/`
3. Validation script passes with 0 errors
4. Format is consistent (required/optional structure)
