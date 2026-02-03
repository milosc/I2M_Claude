import { Skill, Command, Agent, Stage, Model, Context, AgentColor, SubagentType } from '@/types'

export const mockSkills: Skill[] = [
  {
    id: 'Discovery_JTBD',
    name: 'Jobs To Be Done Extractor',
    description:
      'Extracts Jobs To Be Done from pain points, client facts, and user research. Generates structured JTBD document with functional, emotional, and social jobs.',
    stage: Stage.Discovery,
    path: '.claude/skills/Discovery_JTBD/SKILL.md',
    model: Model.Sonnet,
    context: null,
    agent: undefined,
    allowed_tools: ['Read', 'Write', 'Grep'],
    skills_required: [],
    tags: ['jtbd-extraction', 'user-research', 'analysis'],  // PF-002: Tags
    content: {
      purpose:
        'Transform validated pain points into actionable Jobs To Be Done using When/Want/So-that framework',
      usage: 'Invoked by /discovery command during JTBD extraction phase',
      example: 'Read pain points → Map to user types → Generate functional/emotional/social jobs → Validate coverage',
      workflow:
        'Read pain points → Map to user types → Generate functional/emotional/social jobs → Validate coverage',
    },
  },
  {
    id: 'Discovery_GeneratePersona',
    name: 'Persona Generator',
    description:
      'Generates rich persona documents from interview transcripts with demographics, goals, pain points, and workflow patterns',
    stage: Stage.Discovery,
    path: '.claude/skills/Discovery_GeneratePersona/SKILL.md',
    model: Model.Sonnet,
    context: Context.Fork,
    agent: undefined,
    allowed_tools: ['Read', 'Write'],
    skills_required: ['Discovery_InterviewAnalysis'],
    tags: ['persona', 'user-research', 'analysis'],  // PF-002: Tags
    content: {
      purpose: 'Create detailed persona profiles from user research',
      usage: 'Used by /discovery command during persona synthesis phase',
      example:
        'Analyze interview data → Extract demographics → Identify goals and pain points → Generate persona document',
      workflow:
        'Analyze interview data → Extract demographics → Identify goals and pain points → Generate persona document',
    },
  },
  {
    id: 'Prototype_DesignSystem',
    name: 'Design System Generator',
    description:
      'Generates comprehensive design token system with colors, typography, spacing, and component patterns',
    stage: Stage.Prototype,
    path: '.claude/skills/Prototype_DesignSystem/SKILL.md',
    model: Model.Sonnet,
    context: null,
    agent: undefined,
    allowed_tools: ['Read', 'Write'],
    skills_required: [],
    tags: ['design-tokens', 'ui', 'code-generation'],  // PF-002: Tags
    content: {
      purpose: 'Create design tokens and component library specifications',
      usage: 'Used by /prototype command during design foundation phase',
      example:
        'Read design specs → Generate color palette → Create typography scale → Define spacing system',
      workflow:
        'Read design specs → Generate color palette → Create typography scale → Define spacing system',
    },
  },
  {
    id: 'Implementation_TDD_Developer',
    name: 'TDD Developer',
    description: 'Implements features using strict Test-Driven Development (RED-GREEN-REFACTOR cycle)',
    stage: Stage.Implementation,
    path: '.claude/skills/Implementation_TDD_Developer/SKILL.md',
    model: Model.Sonnet,
    context: null,
    agent: undefined,
    allowed_tools: ['Read', 'Write', 'Edit', 'Bash'],
    skills_required: [],
    tags: ['tdd', 'testing', 'code-generation'],  // PF-002: Tags
    content: {
      purpose: 'Implement code following TDD methodology with 100% test coverage',
      usage: 'Used by /htec-sdd-implement command during development phase',
      example: 'Write failing test (RED) → Implement code (GREEN) → Refactor (REFACTOR)',
      workflow: 'Write failing test (RED) → Implement code (GREEN) → Refactor (REFACTOR)',
    },
  },
]

export const mockCommands: Command[] = [
  {
    id: 'discovery',
    name: '/discovery',
    description:
      'Complete end-to-end discovery analysis from client materials to structured documentation (20+ deliverables)',
    stage: Stage.Discovery,
    path: '.claude/commands/discovery.md',
    model: 'sonnet',
    allowed_tools: ['Read', 'Write', 'Bash', 'Skill'],
    argument_hint: '<SystemName> <InputPath>',
    invocation_syntax: '/discovery <SystemName> <InputPath>',
    requires_system_name: true,
    has_options: false,
    tags: ['orchestrator', 'analysis', 'documentation'],  // PF-002: Tags
    content: {
      usage: '/discovery <SystemName> <InputPath>',
      arguments: 'SystemName: Project name\nInputPath: Path to client materials folder',
      example: '/discovery InventorySystem ./InventorySystem/',
      execution:
        'Processes client materials through 10 checkpoints: interviews → pain points → JTBD → requirements → design specs',
      related: '/discovery-multiagent, /discovery-resume, /discovery-audit',
    },
  },
  {
    id: 'prototype',
    name: '/prototype',
    description:
      'Generate working React prototype from Discovery outputs with design tokens, components, and screens',
    stage: Stage.Prototype,
    path: '.claude/commands/prototype.md',
    model: 'sonnet',
    allowed_tools: ['Read', 'Write', 'Bash', 'Skill'],
    argument_hint: '<SystemName>',
    invocation_syntax: '/prototype <SystemName>',
    requires_system_name: true,
    has_options: false,
    tags: ['orchestrator', 'code-generation', 'ui'],  // PF-002: Tags
    content: {
      usage: '/prototype <SystemName>',
      arguments: 'SystemName: Project name (must have completed Discovery)',
      example: '/prototype InventorySystem',
      execution:
        'Creates design tokens → generates components → builds screens → runs validation',
      related: '/prototype-resume, /prototype-feedback, /presentation-slidev',
    },
  },
  {
    id: 'htec-sdd-implement',
    name: '/htec-sdd-implement',
    description:
      'Execute TDD implementation of tasks with granular control (task-level or PR-group-level)',
    stage: Stage.Implementation,
    path: '.claude/commands/htec-sdd-implement.md',
    model: 'sonnet',
    allowed_tools: ['Read', 'Write', 'Edit', 'Bash', 'Skill'],
    argument_hint: '<SystemName> [--task T-001] [--pr-group PR-003]',
    invocation_syntax: '/htec-sdd-implement <SystemName> [OPTIONS]',
    requires_system_name: true,
    has_options: true,
    tags: ['tdd', 'code-generation', 'orchestrator'],  // PF-002: Tags
    content: {
      usage: '/htec-sdd-implement <SystemName> [OPTIONS]',
      arguments: 'SystemName: Project name\n--task: Single task ID\n--pr-group: PR group ID',
      options:
        '--task T-001: Execute single task\n--pr-group PR-003: Execute all tasks in PR group\n--isolate-tasks: Spawn agent per task (default: true)\n--batch=N: Max concurrent agents (default: 2)',
      example: '/htec-sdd-implement ERTriage --pr-group PR-003',
      execution:
        'Phase 1: Plan → Phase 2: Design → Phase 3: Test Spec → Phase 4: TDD Cycle → Phase 5: PR Prep',
      related: '/htec-sdd-tasks, /htec-sdd-review, /htec-sdd-changerequest',
    },
  },
]

export const mockAgents: Agent[] = [
  {
    id: 'discovery-persona-synthesizer',
    name: 'Persona Synthesizer',
    description:
      'Analyzes interview transcripts and user research to generate comprehensive persona documents',
    model: Model.Sonnet,
    checkpoint: 3,
    path: '.claude/agents/discovery-persona-synthesizer.md',
    tools: ['Read', 'Write', 'Grep'],
    color: AgentColor.Blue,
    stage: Stage.Discovery,
    stage_prefix: 'discovery',
    role: 'persona-synthesizer',
    subagent_type: SubagentType.GeneralPurpose,
    tags: ['persona', 'user-research', 'synthesis'],  // PF-002: Tags
    content: {
      expertise:
        'User research analysis, persona development, demographic extraction, goal identification',
      approach:
        'Read interview transcripts → Extract demographics → Map pain points → Identify goals → Generate persona profile',
      skills_to_load: 'Discovery_GeneratePersona, Discovery_InterviewAnalysis',
      output_format: 'JSON with persona fields + Markdown persona document',
      related: 'discovery-domain-researcher, discovery-jtbd-extractor',
    },
  },
  {
    id: 'prototype-code-generator',
    name: 'Code Generator',
    description: 'Generates React components and screens from design specs using TDD',
    model: Model.Sonnet,
    checkpoint: 12,
    path: '.claude/agents/prototype-code-generator.md',
    tools: ['Read', 'Write', 'Edit', 'Bash'],
    color: AgentColor.Green,
    stage: Stage.Prototype,
    stage_prefix: 'prototype',
    role: 'code-generator',
    subagent_type: SubagentType.GeneralPurpose,
    tags: ['code-generation', 'react', 'tdd'],  // PF-002: Tags
    content: {
      expertise: 'React development, TypeScript, Tailwind CSS, TDD, component architecture',
      approach: 'Write failing test → Implement component → Refactor → Validate accessibility',
      skills_to_load: 'Prototype_ComponentGenerator, Prototype_TestGenerator',
      output_format: 'TypeScript React components + Vitest test files',
      related: 'prototype-screen-specifier, prototype-validation-engineer',
    },
  },
  {
    id: 'implementation-developer',
    name: 'Implementation Developer',
    description:
      'Implements production code using strict TDD methodology with 100% test coverage',
    model: Model.Sonnet,
    checkpoint: 4,
    path: '.claude/agents/implementation-developer.md',
    tools: ['Read', 'Write', 'Edit', 'Bash'],
    color: AgentColor.Purple,
    stage: Stage.Implementation,
    stage_prefix: 'implementation',
    role: 'developer',
    subagent_type: SubagentType.GeneralPurpose,
    tags: ['tdd', 'testing', 'code-generation'],  // PF-002: Tags
    content: {
      expertise: 'TDD, unit testing, integration testing, code quality, refactoring',
      approach:
        'RED (failing test) → GREEN (minimal implementation) → REFACTOR (improve code)',
      skills_to_load: 'Implementation_TDD_Developer, Implementation_TestAutomation',
      output_format: 'Production code + comprehensive test suite',
      related: 'implementation-test-automation-engineer, quality-bug-hunter',
    },
  },
]
