# Discovery_GenerateRoadmap Skill

## Overview

This skill generates comprehensive product roadmaps that translate strategic pillars and JTBD priorities into phased development plans with epics, milestones, and dependencies.

## Template

The skill uses two templates:

1. **PRODUCT_ROADMAP_TEMPLATE.md** - Markdown template in this folder
2. **product_roadmap.init.json** - JSON template at `.claude/templates/traceability/init/product_roadmap.init.json`

The markdown template is based on a real-world Emergency Triage System roadmap and demonstrates:

- **Comprehensive Epic Structure**: Each epic includes priority, effort estimation, user value statements, JTBD mapping, features, acceptance criteria, dependencies, requirements, and risk mitigation
- **Phase Organization**: 3-phase structure (Foundation, Pilot Go-Live, Optimization) with clear objectives and milestones
- **Dependency Management**: Visual dependency maps and matrices showing critical path
- **Resource Planning**: FTE allocation by phase and role
- **Traceability**: Requirements mapping (REQ-XXX IDs) and JTBD coverage analysis

## Outputs

### 1. PRODUCT_ROADMAP.md
Location: `03-strategy/PRODUCT_ROADMAP.md`

A comprehensive markdown document containing:
- Roadmap overview with timeline visualization
- Detailed phase breakdowns with epics
- Epic dependency maps
- Feature prioritization (P0/P1/P2)
- Milestone schedule
- Future considerations and decision points
- Resource allocation and critical path

### 2. product_roadmap.json
Location: `traceability/product_roadmap.json`

A structured JSON file for downstream tools containing:
- Roadmap metadata
- Phase and epic details
- Dependency graph
- Feature prioritization
- Milestones
- Resource allocation
- Requirements summary

## Usage

The skill is typically invoked by:
- Discovery Orchestrator after strategy development (Checkpoint 7)
- Manual invocation: "generate product roadmap"
- Command: `/roadmap` (if configured)

## Template Customization

When using the template:

1. **Study the structure**: Review PRODUCT_ROADMAP_TEMPLATE.md to understand the level of detail
2. **Adapt to context**: Adjust number of phases and epics based on project scope
3. **Maintain consistency**: Keep the same section structure for all epics
4. **Reference traceability**: Use JTBD IDs from jtbd_registry.json
5. **Create requirements**: Generate REQ-XXX IDs for each epic's features

## Key Sections Explained

### Epic Structure
Each epic must include:
- **Priority**: P0 (Must Have), P1 (Should Have), P2 (Nice to Have)
- **Estimated Effort**: S/M/L/XL with story points
- **User Value**: "As a [persona], I will be able to [capability], which means [benefit]"
- **JTBD Addressed**: List of JTBD IDs this epic satisfies
- **Requirements**: List of REQ-XXX IDs for traceability
- **Features Table**: Feature name, description, priority (Must/Should/Nice to Have)
- **Acceptance Criteria**: Measurable, testable criteria
- **Dependencies**: What this epic requires and what it enables
- **Risks**: Potential issues and mitigation strategies

### Phase Structure
Each phase should have:
- **Timeline**: Start-end dates and duration
- **Theme**: High-level focus
- **Target Users**: Primary personas
- **Objectives**: 3-5 measurable objectives
- **Epics**: 3-5 epics per phase
- **Milestone**: Exit criteria and validation method

## JSON Schema

The product_roadmap.json follows this structure:
```
{
  document_id, version, created_at, updated_at, generated_by,
  source_files[],
  roadmap_metadata{},
  phases[]{
    phase_id, name, timeline, duration_weeks, theme, target_users[], status,
    objectives[],
    epics[]{
      epic_id, name, priority, estimated_effort, story_points, duration_weeks,
      description, user_value,
      jtbd_addressed[], requirements[], features[], acceptance_criteria[],
      dependencies{requires[], enables[]},
      risks[]
    },
    milestone{}
  },
  dependency_map{},
  feature_prioritization{},
  milestones[],
  future_considerations{},
  resource_allocation{},
  requirements_summary{}
}
```

## Version History

- **v4.0.0** (2026-01-16): Added template reference and JSON generation
- **v3.0.0** (2025-12-21): UPPERCASE file naming, Release/Epic structure
- **v2.1.0** (2025-12-19): Version control metadata
- **v2.0.0** (2025-01-15): Initial Discovery Skills Framework v2.0
