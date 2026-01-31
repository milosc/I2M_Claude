---
name: generating-product-roadmap
description: Use when you need to translate strategic pillars and prioritized user needs into a phased development roadmap with epics and milestones.
model: sonnet
allowed-tools: AskUserQuestion, Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-product-roadmap started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-product-roadmap ended '{"stage": "discovery"}'
---

# Generate Product Roadmap

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-product-roadmap instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Discovery_GenerateRoadmap
- **Version**: 4.0.0
- **Created**: 2025-01-15
- **Updated**: 2026-01-16
- **Change History**:
  - v4.0.0 (2026-01-16): Added PRODUCT_ROADMAP_TEMPLATE.md reference and product_roadmap.json generation
  - v3.0.0 (2025-12-21): Major update: UPPERCASE file naming (PRODUCT_ROADMAP.md), Release/Epic structure
  - v2.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v2.0.0 (2025-01-15): Initial skill version for Discovery Skills Framework v2.0

## Description
Translates strategic pillars and JTBD priorities into a phased development roadmap. Creates a structured epic breakdown with dependencies, milestones, and timeline estimates organized into release phases. Generates both markdown documentation and JSON traceability files.

**Role**: You are a product roadmap specialist who excels at sequencing features, managing dependencies, and creating realistic development timelines that align with strategic goals.

## Execution Logging

This skill uses **deterministic lifecycle logging** via frontmatter hooks.

**Events logged automatically:**
- `skill:generating-product-roadmap:started` - When skill begins
- `skill:generating-product-roadmap:ended` - When skill finishes

**Log file:** `_state/lifecycle.json`

---

## Trigger Conditions

- User requests "create roadmap", "generate product roadmap", "plan development phases"
- Discovery Orchestrator invokes after strategy development (Checkpoint 7)
- User needs to sequence features into development phases
- Request involves epic planning or release scheduling

## System Role Statement

```
You are a Product Roadmap Specialist with expertise in agile planning 
and release management.

Your responsibilities:
1. Translate JTBD into 10-15 development epics
2. Sequence epics based on value and dependencies
3. Assign epics to development phases
4. Create realistic timeline estimates
5. Identify milestones and decision points
6. Generate traceability JSON for downstream tools

You understand that:
- Roadmaps are living documents
- Dependencies drive sequencing
- Early phases should reduce risk
- User value must be demonstrated incrementally
- Traceability enables impact analysis and change management
```

## Input Requirements

| Input | Required | Source |
|-------|----------|--------|
| PRODUCT_STRATEGY.md | Yes | 03-strategy/ |
| JOBS_TO_BE_DONE.md | Yes | 02-research/ |
| persona-*.md files | Yes | 02-research/ |
| jtbd_registry.json | Yes | traceability/ |
| requirements_registry.json | Recommended | traceability/ |

## CRITICAL OUTPUT REQUIREMENTS

### File Name (MANDATORY)

```
[output_path]/03-strategy/PRODUCT_ROADMAP.md
[output_path]/traceability/product_roadmap.json
```

**File naming**: 
- Markdown: UPPERCASE with underscores - `PRODUCT_ROADMAP.md`
- JSON: lowercase with underscores - `product_roadmap.json`

## Output Specification

### Template Reference

**IMPORTANT**: Use the comprehensive template located at:
`.claude/skills/Discovery_GenerateRoadmap/PRODUCT_ROADMAP_TEMPLATE.md`

**JSON Template**: The JSON structure template is located at:
`.claude/templates/traceability/init/product_roadmap.init.json`

This template provides a complete, real-world example of a product roadmap with:
- Detailed epic structure with all required sections
- JTBD mapping and requirements traceability
- Dependency visualization and critical path analysis
- Resource allocation and milestone planning
- Comprehensive acceptance criteria and risk mitigation

**Study this template carefully** before generating your roadmap. Follow its structure, level of detail, and formatting conventions.

### Primary Output: `03-strategy/PRODUCT_ROADMAP.md`

Generate a markdown file following the template structure with these key sections:

1. **Frontmatter**: Document metadata with version control
2. **Roadmap Overview**: Timeline visualization and phase summary
3. **Phase Details**: For each phase (typically 3-4 phases):
   - Phase objectives (measurable)
   - Epic breakdown with:
     - Priority (P0/P1/P2)
     - Estimated effort and duration
     - Description and user value statement
     - JTBD addressed (with IDs from jtbd_registry.json)
     - Key features table
     - Acceptance criteria checklist
     - Dependencies (requires/enables)
     - Requirements (REQ-XXX IDs)
     - Risks and mitigation strategies
   - Phase milestone with exit criteria
4. **Epic Dependency Map**: Visual diagram and dependency matrix
5. **Feature Prioritization**: P0/P1/P2 breakdown with JTBD coverage
6. **Milestone Schedule**: Timeline with key deliverables
7. **Future Considerations**: Backlog and decision points
8. **Resource Allocation**: By phase and critical path analysis
9. **Requirements Summary**: Total count and breakdown by epic

### Secondary Output: `traceability/product_roadmap.json`

**CRITICAL**: After generating the markdown file, create a structured JSON representation and save it to the traceability folder.

The JSON file should contain:

```json
{
  "document_id": "ROADMAP-[PROJECT]",
  "version": "1.0.0",
  "created_at": "[YYYY-MM-DD]",
  "updated_at": "[YYYY-MM-DD]",
  "generated_by": "Discovery_GenerateRoadmap",
  "source_files": [
    "03-strategy/PRODUCT_STRATEGY.md",
    "02-research/JOBS_TO_BE_DONE.md",
    "02-research/personas/*.md",
    "traceability/jtbd_registry.json"
  ],
  "roadmap_metadata": {
    "product_name": "[Product Name]",
    "planning_horizon": "[Timeframe]",
    "total_phases": 3,
    "total_epics": 12,
    "roadmap_date": "[YYYY-MM-DD]"
  },
  "phases": [
    {
      "phase_id": "phase-1",
      "phase_number": 1,
      "name": "[Phase Name]",
      "timeline": "Week 1-12",
      "duration_weeks": 12,
      "theme": "[Phase focus]",
      "target_users": ["[Persona 1]", "[Persona 2]"],
      "status": "not_started",
      "objectives": [
        "[Objective 1 - measurable]",
        "[Objective 2 - measurable]"
      ],
      "epics": [
        {
          "epic_id": "epic-1.1",
          "epic_number": "1.1",
          "name": "[Epic Name]",
          "priority": "P0",
          "estimated_effort": "L",
          "story_points": "8-10",
          "duration_weeks": 4,
          "description": "[2-3 sentences]",
          "user_value": "As a [persona], I will be able to [capability], which means [benefit]",
          "jtbd_addressed": ["JTBD-2.1", "JTBD-4.1"],
          "requirements": ["REQ-001", "REQ-002", "REQ-003"],
          "features": [
            {
              "name": "[Feature 1]",
              "description": "[What it does]",
              "priority": "Must Have"
            }
          ],
          "acceptance_criteria": [
            "[Criterion 1]",
            "[Criterion 2]"
          ],
          "dependencies": {
            "requires": [],
            "enables": ["epic-1.2", "epic-1.3"]
          },
          "risks": [
            {
              "risk": "[Risk description]",
              "mitigation": "[Mitigation strategy]"
            }
          ]
        }
      ],
      "milestone": {
        "name": "[Milestone Name]",
        "target_date": "[YYYY-MM-DD]",
        "validation_method": "[How we validate completion]",
        "exit_criteria": [
          "[Criterion 1]",
          "[Criterion 2]"
        ]
      }
    }
  ],
  "dependency_map": {
    "critical_path": ["epic-1.1", "epic-1.2", "epic-1.3", "epic-1.4"],
    "critical_path_duration_weeks": 22,
    "dependencies": [
      {
        "epic_id": "epic-1.1",
        "depends_on": [],
        "blocks": ["epic-1.2", "epic-1.3", "epic-1.4"],
        "phase": 1
      }
    ]
  },
  "feature_prioritization": {
    "p0_must_have": [
      {
        "epic_id": "epic-1.1",
        "feature": "[Feature name]",
        "jtbd_coverage": ["JTBD-2.1", "JTBD-4.1"]
      }
    ],
    "p1_should_have": [],
    "p2_nice_to_have": []
  },
  "milestones": [
    {
      "milestone_id": "M1",
      "name": "[Milestone Name]",
      "target_date": "[YYYY-MM-DD]",
      "phase": 1,
      "key_deliverables": ["[Deliverable 1]", "[Deliverable 2]"]
    }
  ],
  "future_considerations": {
    "backlog": [
      {
        "item": "[Feature name]",
        "rationale_for_deferral": "[Why not now]",
        "potential_phase": "Phase 4+"
      }
    ],
    "decision_points": [
      {
        "decision": "[Decision to be made]",
        "by_when": "[YYYY-MM-DD]",
        "inputs_needed": ["[Input 1]", "[Input 2]"]
      }
    ]
  },
  "resource_allocation": {
    "by_phase": [
      {
        "phase": 1,
        "dev_fte": 2.0,
        "design_fte": 0.5,
        "qa_fte": 0.5,
        "devops_fte": 0.5,
        "total_fte": 3.5
      }
    ],
    "critical_path_sequence": "Epic 1.1 (4 weeks) → Epic 1.2 (3 weeks) → Epic 1.3 (3 weeks) → Epic 1.4 (5 weeks)"
  },
  "requirements_summary": {
    "total_requirements": 67,
    "by_epic": [
      {
        "epic_id": "epic-1.1",
        "requirements": ["REQ-001", "REQ-002", "REQ-003", "REQ-004"],
        "count": 4
      }
    ],
    "by_priority": {
      "p0_count": 39,
      "p0_percentage": 58,
      "p1_count": 18,
      "p1_percentage": 27,
      "p2_count": 10,
      "p2_percentage": 15
    }
  }
}
```

## Roadmap Creation Process

### Step 1: Study the Template
```markdown
1. Open and review PRODUCT_ROADMAP_TEMPLATE.md
2. Understand the level of detail required for each epic
3. Note the structure of dependencies, risks, and acceptance criteria
4. Observe how JTBD IDs and requirements are referenced
```

### Step 1.5: Select Roadmap Phasing Strategy (REQUIRED)

Determine how the roadmap should be structured before identifying epics.

```
USE AskUserQuestion:
  question: "How should the roadmap be structured?"
  header: "Phases"
  options:
    - label: "MVP + Iterations (Recommended)"
      description: "Core features first, then enhancements"
    - label: "User Journey Phases"
      description: "Complete journey 1, then journey 2, etc."
    - label: "Technical Layers"
      description: "Foundation first, then features"

STORE selected strategy in _state/discovery_config.json:
  {
    "roadmap_phasing_strategy": "{selected_option}",
    "roadmap_phasing_rationale": "{option_description}"
  }
```

### Step 2: Epic Identification
```markdown
1. Review all P0 and P1 JTBDs from jtbd_registry.json
2. Group related JTBDs into epics (10-15 total)
3. Name epics clearly (noun + verb structure)
4. Estimate relative size (S/M/L/XL)
```

### Step 3: Dependency Mapping
```markdown
For each epic:
1. What must be built first?
2. What does this enable?
3. Are there circular dependencies? (Resolve)
```

### Step 4: Phase Assignment
```markdown
Phase 1 criteria:
- Foundation capabilities
- Highest risk items (validate early)
- Dependencies for later phases
- Core P0 JTBDs

Phase 2 criteria:
- Core feature expansion
- P1 JTBDs
- User feedback incorporation

Phase 3 criteria:
- Enhancement and optimization
- P2 JTBDs
- Scale considerations
```

### Step 5: Timeline Estimation
```markdown
For each phase:
1. Sum epic estimates
2. Add buffer (20-30%)
3. Identify parallelization opportunities
4. Set milestone dates
```

### Step 6: Generate JSON Traceability
```markdown
1. Extract all structured data from the markdown
2. Create product_roadmap.json with complete epic details
3. Ensure all IDs match (epic-X.Y format)
4. Validate JSON structure before saving
```

## Quality Criteria

- [ ] 10-15 epics defined
- [ ] All P0 JTBDs covered in Phase 1
- [ ] Dependencies clearly mapped
- [ ] No circular dependencies
- [ ] Each epic has acceptance criteria
- [ ] Each epic has requirements (REQ-XXX IDs)
- [ ] Milestones have exit criteria
- [ ] Timeline is realistic
- [ ] Markdown follows template structure
- [ ] JSON file generated in traceability folder
- [ ] All epic IDs consistent between markdown and JSON
- [ ] JTBD IDs match jtbd_registry.json

## Integration Points

### Receives From
- Discovery_GenerateStrategy: Phase structure, priorities
- Discovery_GenerateJTBD: Features to implement
- traceability/jtbd_registry.json: JTBD IDs and priorities

### Provides To
- Discovery_GenerateKPIs: Phase targets
- Discovery_SpecScreens: Feature inventory
- traceability/product_roadmap.json: Epic and phase data for downstream tools

---

**Skill Version**: 4.0
**Framework**: Discovery Skills Framework v2.0
**Output Locations**: 
- 03-strategy/PRODUCT_ROADMAP.md
- traceability/product_roadmap.json
