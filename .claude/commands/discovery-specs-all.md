---
description: Generate all discovery specifications in sequence
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-specs-all started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-specs-all ended '{"stage": "discovery"}'
---


# /discovery-specs-all - Generate All Design Specifications

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-specs-all instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Discovery-specific rules. Load them now:

```bash
# Load Discovery rules (includes PDF handling, input processing, output structure)
/rules-discovery

# Load Traceability rules (includes ID formats, source linking)
/rules-traceability
```

## Arguments

None required - reads configuration from `_state/discovery_config.json`

## Prerequisites

- `/discovery-strategy-all` completed (phases 5-8 complete)
- `_state/discovery_progress.json` shows phases 5-8 complete
- `03-strategy/PRODUCT_ROADMAP.md` exists
- `traceability/requirements_registry.json` populated

## Pre-requisite Skills

- `.claude/skills/Discovery_ClassifyProject/SKILL.md` - **MANDATORY**: Classifies project type

## 🚨 MANDATORY Skills (Must Execute ALL 4)

| # | Skill | Output File | REQUIRED |
|---|-------|-------------|----------|
| 1 | `.claude/skills/Discovery_SpecScreens/Discovery_SpecScreens.md` | `screen-definitions.md` | ✅ YES |
| 2 | `.claude/skills/Discovery_SpecNavigation/Discovery_SpecNavigation.md` | `navigation-flows.md` | ✅ YES |
| 3 | `.claude/skills/Discovery_SpecDataModel/Discovery_SpecDataModel.md` | `data-fields.md` | ✅ YES |
| 4 | `.claude/skills/Discovery_SpecInteractions/Discovery_SpecInteractions.md` | `interaction-patterns.md` | ✅ YES |

## Optional Skills (Execute if time permits)

| # | Skill | Output File |
|---|-------|-------------|
| 5 | `.claude/skills/Discovery_SpecSampleData/Discovery_SpecSampleData.md` | `sample-data.json` |
| 6 | `.claude/skills/Discovery_SpecComponents/Discovery_SpecComponents.md` | `ui-components.md` |

## Execution Steps

### Phase 9: Generate Design Specifications

1. **Load Prerequisites**
   - Read `_state/discovery_config.json` for output_path
   - Read `03-strategy/product-roadmap.md` for features/epics
   - Read `02-research/persona-*.md` for user context
   - Read `traceability/requirements_registry.json`

2. **Update Progress**
   - Set phase `9_specs` status to "in_progress"

3. **Verify Project Classification** (MANDATORY)
   - Read `_state/discovery_config.json`
   - Check if `project_classification` field exists and is populated
   - **IF MISSING**:
     - Read `.claude/skills/Discovery_ClassifyProject/SKILL.md`
     - Run `Discovery_ClassifyProject` to analyze materials and determine project type
     - This will update `_state/discovery_config.json` with type (FULL_STACK, BACKEND_ONLY, etc.)
     - **CONTINUE** only after classification is set

### 9.1: Screen Definitions

4. **Read Discovery_SpecScreens Skill**
   - Understand screen inventory structure
   - Map roadmap features to screens

4. **Generate Screen Definitions**
   - Create `04-design-specs/screen-definitions.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-SCREENS-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_SpecScreens
     source_files:
       - 03-strategy/product-roadmap.md
       - traceability/requirements_registry.json
     ---
     ```
   - Define screen inventory for Phase 1 features
   - Include layout specifications
   - Map screens to roadmap epics/features

5. **Populate Screen Registry**
   - Update `traceability/screen_registry.json`
   - Assign hierarchical IDs: S-1.1, S-1.2, S-2.1...
   - Link screens to features (US-X.Y, FR-X.Y)

### 9.2: Navigation Flows

6. **Read Discovery_SpecNavigation Skill**
   - Understand site map structure
   - Define user flows

7. **Generate Navigation Document**
   - Create `04-design-specs/navigation-flows.md`
   - Include version metadata
   - Define primary navigation
   - Document critical user flows
   - Map navigation to screens (S-X.Y)

### 9.3: Data Model

8. **Read Discovery_SpecDataModel Skill**
   - Identify data entities
   - Define field types and relationships

9. **Generate Data Fields Document**
   - Create `04-design-specs/data-fields.md`
   - Include version metadata
   - Define all data entities
   - Specify field types and constraints
   - Document relationships between entities

### 9.4: Sample Data

10. **Read Discovery_SpecSampleData Skill**
    - Create realistic test data
    - Ensure consistency with data model

11. **Generate Sample Data**
    - Create `04-design-specs/sample-data.json`
    - Include metadata in JSON structure:
      ```json
      {
        "_metadata": {
          "document_id": "DISC-SAMPLEDATA-<SystemName>",
          "version": "1.0.0",
          "generated_by": "Discovery_SpecSampleData"
        },
        "entities": { ... }
      }
      ```
    - Create sample records for each entity
    - Ensure valid foreign key relationships
    - Include edge cases and typical scenarios

### 9.5: UI Components

12. **Read Discovery_SpecComponents Skill**
    - Identify required UI components
    - Define component specifications

13. **Generate Components Document**
    - Create `04-design-specs/ui-components.md`
    - Include version metadata
    - Define component library
    - Map components to screens (S-X.Y)
    - Include variants and states

### 9.6: Interaction Patterns

14. **Read Discovery_SpecInteractions Skill**
    - Define interaction patterns
    - Document micro-interactions

15. **Generate Interactions Document**
    - Create `04-design-specs/interaction-patterns.md`
    - Include version metadata
    - Document interaction patterns
    - Define transitions and animations
    - Include error handling patterns

### Finalize Phase 9

16. **Update Trace Matrix**
    - Update `traceability/trace_matrix.json`
    - Add Feature → Screen links to chains
    - Update coverage statistics for design phase

17. **Update Context Memory**
    - Add key decisions to `discovery_context.json`
    - Record screen count and component decisions
    - Update resumption_context

18. **Update Progress**
    - Set phase `9_specs` to "complete"
    - Update overall_progress
    - Set resumable_from to "10_docs"

## State Updates

### Updated in `_state/`:
- `discovery_config.json` - current_phase, current_checkpoint, updated_at, **project_classification**
- `discovery_progress.json` - phase 9 complete, overall_progress
- `discovery_context.json` - key_decisions, resumption_context

### Updated in `traceability/`:
- `screen_registry.json` - populated with S-X.Y items
- `trace_matrix.json` - Feature→Screen links added, coverage updated

## Outputs (MANDATORY - 4 files minimum)

| File | Required | Validates |
|------|----------|-----------|
| `ClientAnalysis_<SystemName>/04-design-specs/screen-definitions.md` | ✅ YES | Checkpoint 9 |
| `ClientAnalysis_<SystemName>/04-design-specs/navigation-flows.md` | ✅ YES | Checkpoint 9 |
| `ClientAnalysis_<SystemName>/04-design-specs/data-fields.md` | ✅ YES | Checkpoint 9 |
| `ClientAnalysis_<SystemName>/04-design-specs/interaction-patterns.md` | ✅ YES | Checkpoint 9 |
| `ClientAnalysis_<SystemName>/04-design-specs/sample-data.json` | Optional | - |
| `ClientAnalysis_<SystemName>/04-design-specs/ui-components.md` | Optional | - |
| Updated traceability registries | Optional | - |

## 🚨 MANDATORY: Checkpoint Validation

**BEFORE proceeding to Phase 10, you MUST run:**

```bash
python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 9 --dir ClientAnalysis_<SystemName>/
```

**Expected output:**
```
✅ Checkpoint 9 deliverables verified in ClientAnalysis_<SystemName>
```

**If validation FAILS:**
```
❌ QUALITY GATE FAILED: Missing mandatory deliverable for Checkpoint 9: 04-design-specs/data-fields.md
```
→ **FIX the missing file by running the appropriate skill, then re-validate.**

## Error Handling

- If roadmap has no Phase 1 features: Use P0 pain points to infer screens
- If data model unclear: Create minimal entity set from screen analysis
- Continue with available data, note gaps in outputs
- **DO NOT skip validation** - it prevents incomplete deliverables

## State Updates

After `/discovery-specs-all` AND validation passes:
- Run `/discovery-docs-all` to generate documentation
- Or run `/discovery-validate` directly if docs not needed
