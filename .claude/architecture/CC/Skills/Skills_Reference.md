# Skills Reference

**Version**: 2.0.0
**Created**: 2025-01-08
**Updated**: 2026-01-08
**Status**: Reference Document

This document provides a comprehensive reference for all skills and agents in the HTEC framework.

---

## Skills Location

All skills are in `.claude/skills/` with naming conventions:
- Stage-specific: `{Stage}_*` (e.g., `Discovery_*`, `Prototype_*`)
- Feedback: `{Stage}_Feedback*`
- Cross-stage: Descriptive names (e.g., `systematic-debugging`)

---

## Stage 1: Discovery Skills (29 core + 5 feedback)

| Skill | Purpose |
|-------|---------|
| `Discovery_AnalyzePDF` | Deep PDF extraction with gap analysis |
| `Discovery_ExtractPainPoints` | Extract and categorize user pain points |
| `Discovery_GeneratePersona` | Synthesize personas from research |
| `Discovery_GenerateJTBD` | Transform pain points to JTBD |
| `Discovery_SpecScreens` | Define screen inventory and layout |
| `Discovery_FactAuditor` | Zero hallucination audit |
| `Discovery_FeedbackAnalyzer` | Impact analysis across artifacts |
| `Discovery_FeedbackImplementer` | Change execution with traceability |

---

## Stage 2: Prototype Skills (14+ core + 5 feedback)

| Skill | Purpose |
|-------|---------|
| `Prototype_ValidateDiscovery` | Validate discovery completeness |
| `Prototype_DataModel` | Generate data model from specs |
| `Prototype_DesignTokens` | Generate design tokens and color system |
| `Prototype_Components` | Generate component specifications |
| `Prototype_Screens` | Generate screen specifications |
| `Prototype_CodeGen` | Generate React prototype code |
| `Prototype_QA` | Run QA validation |
| `Prototype_UIAudit` | Visual QA audit with screenshots |
| `Prototype_FeedbackAnalyzer` | Impact analysis with traceability chains |

---

## Stage 3: ProductSpecs Skills (10 core + 4 feedback)

| Skill | Purpose |
|-------|---------|
| `ProductSpecs_Modules` | Generate module specifications |
| `ProductSpecs_Tests` | Generate test specifications |
| `ProductSpecs_JIRAExporter` | Generate JIRA import files |
| `ProductSpecs_FeedbackAnalyzer` | Impact analysis across specs |

---

## Stage 4: SolArch Skills (6 core + 4 feedback)

| Skill | Purpose |
|-------|---------|
| `SolutionArchitecture_Generator` | Main orchestration and arc42 generation |
| `SolutionArchitecture_C4Generator` | C4 diagrams |
| `SolutionArchitecture_AdrGenerator` | Architecture Decision Records |
| `SolutionArchitecture_E2ETraceabilityAnalyzer` | End-to-end traceability validation |

---

## Stage 5: Implementation Skills (5 core + 2 change mgmt)

| Skill | Purpose |
|-------|---------|
| `Implementation_TaskDecomposer` | Module -> Task breakdown with TDD specs |
| `Implementation_Developer` | TDD implementation (RED-GREEN-REFACTOR) |
| `Implementation_CodeReview` | Multi-agent code review orchestration |
| `Implementation_Integrator` | Integration testing and API validation |
| `Implementation_ChangeAnalyzer` | Kaizen root cause analysis |
| `Implementation_ChangeImplementer` | PDCA + TDD + Reflexion execution |

---

## Cross-Stage Utility Skills

| Skill | Purpose |
|-------|---------|
| `systematic-debugging` | Four-phase debugging framework |
| `root-cause-tracing` | Data flow tracing for debugging |
| `executing-plans` | Controlled batch execution |
| `test-driven-development` | TDD protocol |
| `code-review-bug-hunter` | Logic errors, null safety |
| `code-review-code-quality` | SOLID, DRY, complexity |
| `markitdown` | Convert documents to Markdown |
| `theme-factory` | Apply styling themes |

---

## Security Skills (10 skills, Added 2026-01-30)

| Skill | Purpose |
|-------|---------|
| `SECURITY_vulnerability-scanner` | OWASP 2025 vulnerability scanning |
| `SECURITY_api-security-best-practices` | API security patterns and guidelines |
| `SECURITY_top-web-vulnerabilities` | OWASP Top 10 detection |
| `SECURITY_broken-authentication` | Authentication bypass and weakness detection |
| `SECURITY_sql-injection-testing` | SQL injection pattern detection |
| `SECURITY_xss-html-injection` | XSS and HTML injection vulnerability scanning |
| `SECURITY_idor-testing` | Insecure Direct Object Reference testing |
| `SECURITY_file-uploads` | File upload security validation |
| `SECURITY_api-fuzzing-bug-bounty` | API fuzzing and bug bounty patterns |
| `SECURITY_webapp-testing` | Web application security testing toolkit |

**Integrated into**: `quality-security-auditor` agent (Implementation stage)

---

## GRC Compliance Skills (13 skills, Added 2026-01-30)

For regulated industries (Medical Devices, Healthcare, Finance).

| Skill | Domain | Standard |
|-------|--------|----------|
| `GRC_quality-manager-qms-iso13485` | Medical Device QMS | ISO 13485 |
| `GRC_gdpr-dsgvo-expert` | Data Privacy | GDPR/DSGVO |
| `GRC_data-privacy-compliance` | Healthcare Data | HIPAA |
| `GRC_fda-consultant-specialist` | FDA Compliance | 21 CFR Part 11 |
| `GRC_mdr-745-specialist` | EU Medical Devices | MDR 2017/745 |
| `GRC_information-security-manager-iso27001` | Information Security | ISO 27001 |
| `GRC_risk-management-specialist` | Risk Management | ISO 14971 |
| `GRC_capa-officer` | Corrective Actions | CAPA Process |
| `GRC_quality-documentation-manager` | Quality Documentation | QMS Docs |
| `GRC_quality-manager-qmr` | Quality Management | QMR Role |
| `GRC_qms-audit-expert` | QMS Auditing | Internal Audits |
| `GRC_isms-audit-expert` | ISMS Auditing | Security Audits |
| `GRC_regulatory-affairs-head` | Regulatory Strategy | Cross-standard |

**Command**: `/compliance-check <SystemName> --standard iso13485,gdpr,fda`

---

## Design Enhancement Skills (Added 2026-01-30)

| Skill | Purpose |
|-------|---------|
| `ui-design-system` | Design system patterns and component standards |
| `ui-ux-pro-max` | Advanced UX design intelligence (50+ style guides) |
| `mobile-design` | Mobile-first UI patterns |
| `tailwind-patterns` | Tailwind CSS v4 best practices |
| `web-design-guidelines` | Web interface design standards |

**Integrated into**: `prototype-component-specifier`, `prototype-screen-specifier` agents

---

## Skill Frontmatter

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (letters, numbers, hyphens) |
| `description` | Yes | When to use and what it does |
| `context` | No | `fork` for isolated sub-agent |
| `agent` | No | `general-purpose`, `Explore`, `Plan`, `Bash` |

Skills are **hot-reloaded** - changes take effect instantly without restart.

---

## Multi-Agent System

The framework supports specialized agents for parallel execution of complex tasks. Agents are spawned via Claude Code's native Task tool.

### Agent Categories

| Category | Naming Pattern | Purpose |
|----------|----------------|---------|
| Discovery | `discovery-*` | Material analysis, persona synthesis |
| Prototype | `prototype-*` | Specs, validation, code generation |
| Implementation | `implementation-*` | TDD development |
| Planning | `planning-*` | Task decomposition, research |
| Quality | `quality-*` | Code review (6 specialized reviewers) |
| Process Integrity | `process-integrity-*` | Traceability, TDD compliance |
| Reflexion | `reflexion-*` | Self-improvement loop |
| Utility | Descriptive names | Cross-stage utilities (e.g., `agent-expert`) |

### Agent Invocation

All agents use Claude Code's native `subagent_type` values:

```javascript
Task({
  subagent_type: "general-purpose",  // Native Claude Code type
  model: "sonnet",                   // or "haiku" for structured tasks
  description: "Brief description",
  prompt: `Agent: {agent-name}
    Read: .claude/agents/{agent-name}.md
    [compact instructions]
    RETURN: JSON { status, outputs }`
})
```

**Native subagent_type values**: `general-purpose`, `Explore`, `Plan`, `Bash`

### Model Allocation

| Model | Use Cases |
|-------|-----------|
| `sonnet` | Complex reasoning, code generation, security analysis |
| `haiku` | Structured validation, checklists, templated outputs |

**Full documentation**: `architecture/Agent_Spawning_Architecture.md`

---

## Related Documentation

### Authoring Commands
- **Agent Creation**: `/create-agent <description>` - Spawns agent-expert to create new agents
- **Skill Authoring**: `/create-skill` - Create new skills with TDD approach
- **Command Authoring**: `/create-command` - Create new slash commands
- **Hook Authoring**: `/create-hook` - Create new validation hooks

### Reference Documentation
- **Agent Expert**: `.claude/agents/agent-expert.md`
- **Skill Frontmatter**: `.claude/skills/SKILL_FRONTMATTER_REFERENCE.md`
- **Skill Invocation**: `.claude/skills/SKILL_INVOCATION.md`
- **Agent Definitions**: `.claude/agents/`
- **Agent Spawning Architecture**: `architecture/Agent_Spawning_Architecture.md`
- **Agent Coordination Rules**: `.claude/rules/agent-coordination.md`
