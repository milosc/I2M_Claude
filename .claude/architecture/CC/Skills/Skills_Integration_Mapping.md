# Skills Integration Mapping

**Version**: 1.0.0
**Purpose**: Document where visual documentation and utility skills should be referenced across agents, commands, and skills

---

## Skill Summaries

### Visual Documentation Skills

| Skill | Purpose | Use Cases |
|-------|---------|-----------|
| **architecture-diagram-creator** | Create HTML architecture diagrams with data flows, business context, system layers | System overviews, technical specs, high-level documentation |
| **dashboard-creator** | Create HTML dashboards with KPI cards, charts, progress indicators | Metrics displays, KPI visualizations, monitoring interfaces |
| **flowchart-creator** | Create HTML flowcharts with decision trees, process flows, swimlanes | Process diagrams, workflow visualizations, decision trees |
| **technical-doc-creator** | Create HTML technical docs with code blocks, API references, syntax highlighting | API documentation, developer docs, technical references |

### Utility Skills

| Skill | Purpose | Use Cases |
|-------|---------|-----------|
| **systematic-debugging** | Four-phase debugging framework (root cause → pattern → hypothesis → implementation) | Any bug, test failure, unexpected behavior |
| **using-htec-accelerators** | Mandatory skill discovery and usage enforcement | Starting any conversation, ensuring skills are properly used |
| **using-superpowers** | Alias/duplicate of using-htec-accelerators | Same as above |

---

## Integration Map by Agent Category

### SolArch Agents

#### solarch-c4-context-generator
**Should reference**: `architecture-diagram-creator`
**Why**: Creates C4 context diagrams - can use HTML architecture diagrams as alternative/supplement to Mermaid
**Integration point**: After generating Mermaid diagram, mention architecture-diagram-creator as alternative format

#### solarch-c4-container-generator
**Should reference**: `architecture-diagram-creator`
**Why**: Creates container-level diagrams
**Integration point**: Same as context generator

#### solarch-c4-component-generator
**Should reference**: `architecture-diagram-creator`
**Why**: Creates component-level diagrams
**Integration point**: Same as context generator

#### solarch-c4-deployment-generator
**Should reference**: `architecture-diagram-creator`
**Why**: Creates deployment diagrams
**Integration point**: Same as context generator

#### solarch-adr-foundation-writer, solarch-adr-communication-writer, solarch-adr-operational-writer
**Should reference**: `technical-doc-creator`, `flowchart-creator`
**Why**: Creates technical documentation with decision records
**Integration point**: Use technical-doc-creator for HTML versions of ADRs, flowchart-creator for decision flows

#### solarch-orchestrator
**Should reference**: `architecture-diagram-creator`, `flowchart-creator`, `dashboard-creator`
**Why**: Coordinates overall architecture generation
**Integration point**: Mention these skills for generating supplementary documentation

---

### ProductSpecs Agents

#### productspecs-api-module-specifier
**Should reference**: `technical-doc-creator`, `flowchart-creator`
**Why**: Creates API specifications
**Integration point**: Use technical-doc-creator for API documentation, flowchart-creator for API workflows

#### productspecs-nfr-generator
**Should reference**: `dashboard-creator`
**Why**: Generates non-functional requirements with metrics
**Integration point**: Use dashboard-creator for NFR metrics visualization

#### productspecs-orchestrator
**Should reference**: `flowchart-creator`, `dashboard-creator`
**Why**: Coordinates ProductSpecs generation
**Integration point**: Use flowchart-creator for process visualization, dashboard-creator for progress tracking

---

### Implementation Agents

#### implementation-developer
**Should reference**: `systematic-debugging`, `using-htec-accelerators`
**Why**: Core TDD implementation agent that will encounter bugs and test failures
**Integration point**:
- Frontmatter: Add systematic-debugging to recommended skills
- Instructions: Reference systematic-debugging when tests fail or bugs occur

#### implementation-test-automation-engineer
**Should reference**: `systematic-debugging`, `using-htec-accelerators`
**Why**: Creates tests that may fail, needs debugging workflow
**Integration point**: Same as implementation-developer

#### implementation-documenter
**Should reference**: `technical-doc-creator`, `architecture-diagram-creator`
**Why**: Creates technical documentation
**Integration point**: Use these skills for generating HTML documentation formats

---

### Quality Agents

#### quality-bug-hunter
**Should reference**: `systematic-debugging`, `using-htec-accelerators`
**Why**: Detects bugs and needs systematic investigation approach
**Integration point**: Frontmatter and instructions should reference systematic-debugging

#### quality-security-auditor
**Should reference**: `systematic-debugging`
**Why**: Security issues require systematic investigation
**Integration point**: Reference when investigating security vulnerabilities

#### quality-code-quality
**Should reference**: `systematic-debugging`
**Why**: Code quality issues may require debugging
**Integration point**: Reference for investigating quality violations

---

### Discovery Agents

#### discovery-roadmap-generator
**Should reference**: `flowchart-creator`, `dashboard-creator`
**Why**: Roadmaps can be visualized as flowcharts or dashboards
**Integration point**: Mention these as alternative visualization formats

#### discovery-kpis-generator
**Should reference**: `dashboard-creator`
**Why**: KPIs are naturally suited for dashboard visualization
**Integration point**: Generate HTML dashboard versions of KPI documents

#### discovery-orchestrator
**Should reference**: `flowchart-creator`, `dashboard-creator`
**Why**: Orchestrates overall discovery process
**Integration point**: Use flowchart-creator for process visualization, dashboard-creator for progress tracking

---

### Prototype Agents

#### prototype-api-contract-specifier
**Should reference**: `technical-doc-creator`, `flowchart-creator`
**Why**: Creates API contracts that can be documented
**Integration point**: Use technical-doc-creator for API documentation

#### prototype-orchestrator
**Should reference**: `flowchart-creator`, `dashboard-creator`
**Why**: Coordinates prototype generation
**Integration point**: Use flowchart-creator for process visualization, dashboard-creator for progress tracking

---

### Planning Agents

#### planning-tech-lead
**Should reference**: `flowchart-creator`, `architecture-diagram-creator`
**Why**: Creates implementation plans that can be visualized
**Integration point**: Use flowchart-creator for task flow visualization

#### planning-code-explorer
**Should reference**: `architecture-diagram-creator`
**Why**: Explores and documents codebase architecture
**Integration point**: Use architecture-diagram-creator for codebase architecture visualization

---

### Process Integrity Agents

#### process-integrity-checkpoint-auditor
**Should reference**: `dashboard-creator`, `flowchart-creator`
**Why**: Validates checkpoints and progress
**Integration point**: Use dashboard-creator for checkpoint status visualization

---

### Reflexion Agents

#### reflexion-actor
**Should reference**: `using-htec-accelerators`
**Why**: Generates initial solutions
**Integration point**: Ensure proper skill discovery

#### reflexion-evaluator
**Should reference**: `systematic-debugging`, `using-htec-accelerators`
**Why**: Critiques solutions and identifies issues
**Integration point**: Use systematic-debugging for investigating issues

#### reflexion-self-refiner
**Should reference**: `using-htec-accelerators`
**Why**: Polishes solutions
**Integration point**: Ensure proper skill discovery

---

## Integration Map by Command

### Discovery Commands

#### /discovery, /discovery-multiagent
**Should mention**: `flowchart-creator`, `dashboard-creator`
**Why**: Can generate process visualizations and progress dashboards

#### /discovery-roadmap
**Should mention**: `flowchart-creator`, `dashboard-creator`
**Why**: Roadmap visualization

#### /discovery-kpis
**Should mention**: `dashboard-creator`
**Why**: KPI dashboard generation

---

### ProductSpecs Commands

#### /productspecs
**Should mention**: `technical-doc-creator`, `flowchart-creator`, `dashboard-creator`
**Why**: Can generate technical docs and process visualizations

---

### SolArch Commands

#### /solarch
**Should mention**: `architecture-diagram-creator`, `technical-doc-creator`, `flowchart-creator`
**Why**: Core architecture documentation generation

---

### Implementation Commands

#### /htec-sdd-implement
**Should mention**: `systematic-debugging`, `using-htec-accelerators`
**Why**: Core implementation command where debugging is critical

#### /htec-sdd-changerequest
**Should mention**: `systematic-debugging`
**Why**: Change requests often involve debugging

---

## Integration Map by Skill

### Discovery Skills

#### Discovery_GenerateRoadmap
**Should mention**: `flowchart-creator`, `dashboard-creator`

#### Discovery_GenerateKPIs
**Should mention**: `dashboard-creator`

---

### ProductSpecs Skills

#### ProductSpecs_NFRGenerator
**Should mention**: `dashboard-creator`

---

### SolutionArchitecture Skills

#### SolutionArchitecture_C4Generator
**Should mention**: `architecture-diagram-creator`

#### SolutionArchitecture_AdrGenerator
**Should mention**: `technical-doc-creator`, `flowchart-creator`

---

### Implementation Skills

#### Implementation_Developer
**Should mention**: `systematic-debugging`, `using-htec-accelerators`

#### Implementation_CodeReview
**Should mention**: `systematic-debugging`

#### Implementation_ChangeAnalyzer
**Should mention**: `systematic-debugging`

---

## Frontmatter Integration Pattern

For agents that should reference these skills, add to frontmatter:

```yaml
---
name: agent-name
description: Agent description
model: sonnet
recommended_skills:
  - systematic-debugging  # When encountering bugs or test failures
  - architecture-diagram-creator  # For creating architecture visualizations
  - technical-doc-creator  # For generating technical documentation
  - flowchart-creator  # For process flow visualization
  - dashboard-creator  # For metrics and KPI visualization
hooks:
  # ... existing hooks
---
```

**Note**: Use `recommended_skills` field (not `skills` or `required_skills`) to suggest skills without making them mandatory.

---

## Instruction Integration Pattern

For agents that should reference these skills, add to instructions section:

```markdown
## Available Skills

When [specific situation]:
- Use `/systematic-debugging` for any bug, test failure, or unexpected behavior
- Use `/architecture-diagram-creator` for generating HTML architecture diagrams
- Use `/technical-doc-creator` for generating technical documentation
- Use `/flowchart-creator` for visualizing process flows
- Use `/dashboard-creator` for visualizing metrics and KPIs

See skill documentation for detailed usage instructions.
```

---

## Priority Integration Order

1. **HIGH PRIORITY** (Critical workflows):
   - implementation-developer → systematic-debugging
   - quality-bug-hunter → systematic-debugging
   - implementation-test-automation-engineer → systematic-debugging
   - All orchestrators → using-htec-accelerators

2. **MEDIUM PRIORITY** (Enhances functionality):
   - solarch-c4-* agents → architecture-diagram-creator
   - productspecs-api-module-specifier → technical-doc-creator
   - discovery-kpis-generator → dashboard-creator
   - All orchestrators → flowchart-creator, dashboard-creator

3. **LOW PRIORITY** (Nice to have):
   - planning-tech-lead → flowchart-creator
   - discovery-roadmap-generator → flowchart-creator
   - productspecs-nfr-generator → dashboard-creator

---

## Implementation Checklist

- [ ] Update HIGH PRIORITY agents (4 agents)
- [ ] Update HIGH PRIORITY orchestrators (4 agents)
- [ ] Update MEDIUM PRIORITY solarch agents (4 agents)
- [ ] Update MEDIUM PRIORITY productspecs agents (2 agents)
- [ ] Update MEDIUM PRIORITY discovery agents (1 agent)
- [ ] Update MEDIUM PRIORITY orchestrators (4 agents)
- [ ] Update LOW PRIORITY agents (3 agents)
- [ ] Update relevant commands (8 commands)
- [ ] Update relevant skills (8 skills)
- [ ] Verify all integrations
- [ ] Test agent invocations with new skill references

---

## Validation

After integration:
1. Verify frontmatter YAML is valid
2. Check that skill names match exactly (case-sensitive)
3. Confirm hooks section is not affected
4. Test agent invocations with new references
5. Verify using-htec-accelerators properly enforces skill usage

---

## Notes

- **using-superpowers** appears to be a duplicate of **using-htec-accelerators** - consider deprecating or merging
- Some agents may already reference these skills in their instructions - check before adding duplicates
- Consider adding skill autocomplete/suggestion feature to agent invocation process
- Monitor usage metrics to validate integration effectiveness

---

**Last Updated**: 2026-01-26
**Maintained By**: Framework Coordination Team
