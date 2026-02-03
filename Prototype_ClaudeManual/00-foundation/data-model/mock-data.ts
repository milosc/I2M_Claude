/**
 * ClaudeManual Data Model - Mock Data Schemas
 *
 * Generated: 2026-01-31
 * Session: session-data-model-claudemanual
 * Agent: prototype-data-model-specifier
 *
 * Mock Data Generators using Faker.js
 */

import { faker } from '@faker-js/faker';
import {
  Skill,
  Command,
  Agent,
  Rule,
  Hook,
  UserPreferences,
  Workflow,
  WaysOfWorking,
  ArchitectureDoc,
  Stage,
  Model,
  Theme,
  Format,
  WorkflowCategory,
  WaysOfWorkingCategory,
  ArchitectureCategory,
  C4Level,
  ADRStatus,
  HookType,
  Language,
  Audience,
  RuleCategory,
  AgentColor,
  EntityType,
} from './types';

// ============================================================================
// MOCK DATA GENERATORS
// ============================================================================

/**
 * Generate mock Skill
 */
export const mockSkill = (): Skill => {
  const stagePrefix = faker.helpers.arrayElement([
    'Discovery',
    'Prototype',
    'ProductSpecs',
    'Implementation',
  ]);
  const category = faker.helpers.arrayElement([
    'JTBD',
    'Personas',
    'Vision',
    'DataModel',
    'Component',
    'Screen',
  ]);
  const skillName = `${stagePrefix}_${category}`;

  return {
    id: faker.helpers.slugify(skillName),
    name: skillName,
    description: faker.lorem.sentence({ min: 10, max: 30 }),
    stage: stagePrefix as Stage,
    path: `.claude/skills/${faker.helpers.slugify(skillName)}/SKILL.md`,
    model: faker.helpers.arrayElement([Model.Sonnet, Model.Opus, Model.Haiku]),
    context: faker.helpers.maybe(() => 'fork' as const, { probability: 0.3 }),
    agent: faker.helpers.maybe(() => faker.word.noun(), { probability: 0.2 }),
    allowed_tools: faker.helpers.arrayElements(
      ['Bash', 'Edit', 'Read', 'Write', 'Glob', 'Grep'],
      { min: 2, max: 5 }
    ),
    skills_required: faker.helpers.maybe(
      () => faker.helpers.multiple(() => faker.helpers.slugify(faker.word.words(2)), { count: { min: 0, max: 3 } }),
      { probability: 0.4 }
    ),
    hooks: faker.helpers.maybe(
      () => ({ pre: 'validate_inputs.py', post: 'log_completion.py' }),
      { probability: 0.3 }
    ),

    // Derived fields
    stage_prefix: stagePrefix,
    category,
    file_size: faker.number.int({ min: 500, max: 50000 }),
    last_modified: faker.date.recent({ days: 30 }),
    content_hash: faker.string.hexadecimal({ length: 64, prefix: '' }),

    // Content sections
    content: {
      purpose: faker.lorem.paragraph(),
      usage: `/${faker.helpers.slugify(skillName)} [options]`,
      options: faker.helpers.maybe(() => faker.lorem.lines(3), { probability: 0.7 }),
      example: `/${faker.helpers.slugify(skillName)} --system MyApp`,
      workflow: faker.helpers.maybe(() => 'graph TD\n  A[Start] --> B[Process]', { probability: 0.5 }),
      related: faker.helpers.maybe(() => faker.word.words(3), { probability: 0.6 }),
    },
  };
};

/**
 * Generate mock Command
 */
export const mockCommand = (): Command => {
  const commandName = faker.helpers.slugify(faker.word.words({ count: { min: 1, max: 3 } }));
  const stage = faker.helpers.arrayElement([
    Stage.Discovery,
    Stage.Prototype,
    Stage.ProductSpecs,
    Stage.Implementation,
    Stage.Utility,
  ]);

  return {
    id: commandName,
    name: commandName
      .split('-')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' '),
    description: faker.lorem.sentence({ min: 10, max: 30 }),
    stage,
    path: `.claude/commands/${commandName}.md`,
    model: faker.helpers.arrayElement(['claude-sonnet-4-5-20250929', 'claude-haiku-4-5-20250515', 'sonnet', 'haiku']),
    allowed_tools: faker.helpers.arrayElements(['Bash', 'Edit', 'Read', 'Write'], { min: 1, max: 4 }),
    argument_hint: faker.helpers.maybe(() => '<SystemName> [options]', { probability: 0.7 }),

    // Derived fields
    invocation_syntax: `/${commandName} <SystemName>`,
    requires_system_name: faker.datatype.boolean({ probability: 0.7 }),
    has_options: faker.datatype.boolean({ probability: 0.6 }),

    // Content sections
    content: {
      usage: `/${commandName} <SystemName> [options]`,
      arguments: faker.helpers.maybe(() => '- SystemName: Name of the system', { probability: 0.7 }),
      options: faker.helpers.maybe(() => '- --stage: Filter by stage\n- --verbose: Verbose output', { probability: 0.6 }),
      example: `/${commandName} InventorySystem --stage Discovery`,
      execution: faker.helpers.maybe(() => faker.lorem.lines(5), { probability: 0.5 }),
      related: faker.helpers.maybe(() => faker.word.words(3), { probability: 0.6 }),
    },
  };
};

/**
 * Generate mock Agent
 */
export const mockAgent = (): Agent => {
  const stage = faker.helpers.arrayElement([
    'discovery',
    'prototype',
    'productspecs',
    'implementation',
  ]);
  const role = faker.helpers.arrayElement([
    'domain-researcher',
    'persona-synthesizer',
    'screen-specifier',
    'developer',
    'test-engineer',
  ]);
  const agentId = `${stage}-${role}`;

  return {
    id: agentId,
    name: role
      .split('-')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' '),
    description: faker.lorem.sentence({ min: 10, max: 30 }),
    model: faker.helpers.arrayElement([Model.Sonnet, Model.Opus, Model.Haiku]),
    checkpoint: faker.helpers.maybe(() => faker.number.int({ min: 1, max: 20 }), { probability: 0.8 }),
    path: `.claude/agents/${agentId}.md`,
    tools: faker.helpers.arrayElements(
      ['Bash', 'Edit', 'Read', 'Write', 'Glob', 'Grep', 'WebFetch'],
      { min: 2, max: 6 }
    ),
    color: faker.helpers.arrayElement([
      AgentColor.Blue,
      AgentColor.Green,
      AgentColor.Purple,
      AgentColor.Orange,
      AgentColor.Red,
    ]),
    stage: stage.charAt(0).toUpperCase() + stage.slice(1) as Stage,

    // Derived fields
    stage_prefix: stage,
    role,
    subagent_type: faker.helpers.arrayElement(['general-purpose', 'Explore', 'Plan', 'Bash']),

    // Content sections
    content: {
      expertise: faker.lorem.paragraph(),
      approach: faker.helpers.maybe(() => faker.lorem.lines(3), { probability: 0.7 }),
      skills_to_load: faker.helpers.maybe(() => faker.word.words(3), { probability: 0.6 }),
      output_format: 'JSON { status, files_written, issues }',
      related: faker.helpers.maybe(() => faker.word.words(3), { probability: 0.5 }),
    },
  };
};

/**
 * Generate mock Rule
 */
export const mockRule = (): Rule => {
  const ruleName = faker.helpers.slugify(faker.word.words({ count: { min: 1, max: 2 } }));

  return {
    id: ruleName,
    name: ruleName
      .split('-')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' '),
    description: faker.lorem.sentence({ min: 10, max: 30 }),
    path: `.claude/rules/${ruleName}.md`,
    auto_load_paths: faker.helpers.maybe(
      () => faker.helpers.arrayElements(
        ['ClientAnalysis_*/**/*', 'Prototype_*/**/*', 'Implementation_*/**/*'],
        { min: 1, max: 2 }
      ),
      { probability: 0.7 }
    ),
    version: `${faker.number.int({ min: 1, max: 3 })}.${faker.number.int({ min: 0, max: 9 })}.${faker.number.int({ min: 0, max: 9 })}`,
    category: faker.helpers.arrayElement([
      RuleCategory.Core,
      RuleCategory.StageSpecific,
      RuleCategory.Quality,
      RuleCategory.Process,
    ]),

    // Derived fields
    applies_to_stages: faker.helpers.arrayElements([Stage.Discovery, Stage.Prototype, Stage.Implementation]),

    // Content sections
    content: {
      overview: faker.lorem.paragraph(),
      rules: faker.lorem.lines(5),
      examples: faker.helpers.maybe(() => faker.lorem.lines(3), { probability: 0.7 }),
      related: faker.helpers.maybe(() => faker.word.words(3), { probability: 0.5 }),
    },
  };
};

/**
 * Generate mock Hook
 */
export const mockHook = (): Hook => {
  const hookName = faker.helpers.slugify(faker.word.words({ count: { min: 1, max: 3 } }));
  const language = faker.helpers.arrayElement([Language.Python, Language.Bash]);
  const extension = language === Language.Python ? 'py' : 'sh';

  return {
    id: hookName,
    name: hookName
      .split('-')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' '),
    description: faker.lorem.sentence({ min: 10, max: 30 }),
    path: `.claude/hooks/${hookName}.${extension}`,
    type: faker.helpers.arrayElement([
      HookType.PreToolUse,
      HookType.PostToolUse,
      HookType.Stop,
      HookType.Lifecycle,
    ]),
    language,

    // Derived fields
    executable: faker.datatype.boolean({ probability: 0.95 }),
    has_shebang: faker.datatype.boolean({ probability: 0.95 }),
  };
};

/**
 * Generate mock UserPreferences
 */
export const mockUserPreferences = (): UserPreferences => {
  const allItemIds = faker.helpers.multiple(() => faker.string.uuid(), { count: 50 });

  return {
    theme: faker.helpers.arrayElement([Theme.Light, Theme.Dark, Theme.System]),
    favorites: faker.helpers.arrayElements(allItemIds, { min: 0, max: 10 }),
    collapsed_nodes: faker.helpers.arrayElements(allItemIds, { min: 0, max: 15 }),
    last_viewed: faker.helpers.maybe(() => faker.helpers.arrayElement(allItemIds), { probability: 0.8 }),
    search_history: faker.helpers.multiple(() => faker.word.words({ count: { min: 1, max: 3 } }), {
      count: { min: 5, max: 20 },
    }),
    stage_filter: faker.helpers.arrayElements([
      Stage.Discovery,
      Stage.Prototype,
      Stage.ProductSpecs,
      Stage.Implementation,
    ]),
    type_filter: faker.helpers.arrayElements(['Skill', 'Command', 'Agent', 'Rule', 'Hook'] as EntityType[]),
  };
};

/**
 * Generate mock Workflow
 */
export const mockWorkflow = (): Workflow => {
  const workflowName = faker.helpers.slugify(faker.word.words({ count: { min: 2, max: 4 } }));
  const format = faker.helpers.arrayElement([Format.Markdown, Format.Mermaid, Format.PlantUML]);
  const extension = format === Format.Markdown ? 'md' : format === Format.Mermaid ? 'mermaid' : 'plantuml';

  return {
    id: workflowName,
    name: workflowName
      .split('-')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' '),
    description: faker.lorem.sentence({ min: 10, max: 30 }),
    format,
    path: `workflows/${workflowName}.${extension}`,
    stage: faker.helpers.maybe(
      () => faker.helpers.arrayElement([Stage.Discovery, Stage.Prototype, Stage.Implementation]),
      { probability: 0.7 }
    ),
    category: faker.helpers.maybe(
      () => faker.helpers.arrayElement([
        WorkflowCategory.Process,
        WorkflowCategory.Integration,
        WorkflowCategory.Decision,
        WorkflowCategory.DataFlow,
      ]),
      { probability: 0.8 }
    ),
    tags: faker.helpers.maybe(
      () => faker.helpers.arrayElements(['automation', 'manual', 'review', 'approval'], { min: 1, max: 3 }),
      { probability: 0.6 }
    ),

    // Content sections
    content: {
      overview: faker.helpers.maybe(() => faker.lorem.paragraph(), { probability: 0.7 }),
      diagram: format === Format.Markdown ? faker.lorem.lines(10) : 'graph TD\n  A[Start] --> B[Process] --> C[End]',
      steps: faker.helpers.maybe(() => faker.lorem.lines(5), { probability: 0.6 }),
      related: faker.helpers.maybe(() => faker.word.words(3), { probability: 0.5 }),
    },
  };
};

/**
 * Generate mock WaysOfWorking
 */
export const mockWaysOfWorking = (): WaysOfWorking => {
  const docName = faker.helpers.slugify(faker.word.words({ count: { min: 2, max: 4 } }));

  return {
    id: docName,
    name: docName
      .split('-')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' '),
    description: faker.lorem.sentence({ min: 10, max: 30 }),
    path: `docs/${docName}.md`,
    category: faker.helpers.maybe(
      () => faker.helpers.arrayElement([
        WaysOfWorkingCategory.Practices,
        WaysOfWorkingCategory.Guidelines,
        WaysOfWorkingCategory.Processes,
        WaysOfWorkingCategory.Checklists,
      ]),
      { probability: 0.8 }
    ),
    audience: faker.helpers.maybe(
      () => faker.helpers.arrayElement([Audience.Developers, Audience.Product, Audience.All, Audience.Leads]),
      { probability: 0.7 }
    ),
    tags: faker.helpers.maybe(
      () => faker.helpers.arrayElements(['best-practices', 'team', 'process', 'quality'], { min: 1, max: 3 }),
      { probability: 0.6 }
    ),

    // Content sections
    content: {
      overview: faker.lorem.paragraph(),
      guidelines: faker.helpers.maybe(() => faker.lorem.lines(5), { probability: 0.7 }),
      examples: faker.helpers.maybe(() => faker.lorem.lines(3), { probability: 0.6 }),
      checklist: faker.helpers.maybe(() => faker.lorem.lines(4), { probability: 0.5 }),
    },
  };
};

/**
 * Generate mock ArchitectureDoc
 */
export const mockArchitectureDoc = (): ArchitectureDoc => {
  const docName = faker.helpers.slugify(faker.word.words({ count: { min: 2, max: 4 } }));
  const category = faker.helpers.arrayElement([
    ArchitectureCategory.C4,
    ArchitectureCategory.ADR,
    ArchitectureCategory.Patterns,
    ArchitectureCategory.Infrastructure,
    ArchitectureCategory.DataModel,
  ]);
  const format = faker.helpers.arrayElement([Format.Markdown, Format.Mermaid, Format.PlantUML]);
  const extension = format === Format.Markdown ? 'md' : format === Format.Mermaid ? 'mermaid' : 'plantuml';

  return {
    id: docName,
    name: docName
      .split('-')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' '),
    description: faker.lorem.sentence({ min: 10, max: 30 }),
    format,
    path: `architecture/${docName}.${extension}`,
    category,
    c4_level:
      category === ArchitectureCategory.C4
        ? faker.helpers.arrayElement([C4Level.Context, C4Level.Container, C4Level.Component, C4Level.Code])
        : undefined,
    adr_status:
      category === ArchitectureCategory.ADR
        ? faker.helpers.arrayElement([ADRStatus.Proposed, ADRStatus.Accepted, ADRStatus.Deprecated, ADRStatus.Superseded])
        : undefined,
    tags: faker.helpers.maybe(
      () => faker.helpers.arrayElements(['microservices', 'api', 'database', 'security'], { min: 1, max: 3 }),
      { probability: 0.7 }
    ),
    related_adrs: faker.helpers.maybe(
      () => faker.helpers.multiple(() => faker.helpers.slugify(faker.word.words(2)), { count: { min: 1, max: 3 } }),
      { probability: 0.4 }
    ),

    // Content sections
    content: {
      overview: faker.lorem.paragraph(),
      diagram: faker.helpers.maybe(() => 'graph TD\n  A[Component] --> B[Database]', { probability: 0.7 }),
      context: faker.helpers.maybe(() => faker.lorem.paragraph(), { probability: 0.6 }),
      decision: faker.helpers.maybe(() => faker.lorem.paragraph(), { probability: 0.6 }),
      consequences: faker.helpers.maybe(() => faker.lorem.lines(3), { probability: 0.6 }),
      related: faker.helpers.maybe(() => faker.word.words(3), { probability: 0.5 }),
    },
  };
};

// ============================================================================
// BULK GENERATORS
// ============================================================================

/**
 * Generate multiple entities
 */
export const mockSkills = (count: number = 10): Skill[] =>
  faker.helpers.multiple(mockSkill, { count });

export const mockCommands = (count: number = 5): Command[] =>
  faker.helpers.multiple(mockCommand, { count });

export const mockAgents = (count: number = 8): Agent[] =>
  faker.helpers.multiple(mockAgent, { count });

export const mockRules = (count: number = 5): Rule[] =>
  faker.helpers.multiple(mockRule, { count });

export const mockHooks = (count: number = 6): Hook[] =>
  faker.helpers.multiple(mockHook, { count });

export const mockWorkflows = (count: number = 7): Workflow[] =>
  faker.helpers.multiple(mockWorkflow, { count });

export const mockWaysOfWorkingDocs = (count: number = 5): WaysOfWorking[] =>
  faker.helpers.multiple(mockWaysOfWorking, { count });

export const mockArchitectureDocs = (count: number = 10): ArchitectureDoc[] =>
  faker.helpers.multiple(mockArchitectureDoc, { count });

// ============================================================================
// COMPLETE DATASET GENERATOR
// ============================================================================

export interface MockDataset {
  skills: Skill[];
  commands: Command[];
  agents: Agent[];
  rules: Rule[];
  hooks: Hook[];
  workflows: Workflow[];
  waysOfWorking: WaysOfWorking[];
  architectureDocs: ArchitectureDoc[];
  userPreferences: UserPreferences;
}

/**
 * Generate complete mock dataset
 */
export const generateMockDataset = (options?: {
  skillCount?: number;
  commandCount?: number;
  agentCount?: number;
  ruleCount?: number;
  hookCount?: number;
  workflowCount?: number;
  waysOfWorkingCount?: number;
  architectureDocCount?: number;
}): MockDataset => {
  return {
    skills: mockSkills(options?.skillCount ?? 10),
    commands: mockCommands(options?.commandCount ?? 5),
    agents: mockAgents(options?.agentCount ?? 8),
    rules: mockRules(options?.ruleCount ?? 5),
    hooks: mockHooks(options?.hookCount ?? 6),
    workflows: mockWorkflows(options?.workflowCount ?? 7),
    waysOfWorking: mockWaysOfWorkingDocs(options?.waysOfWorkingCount ?? 5),
    architectureDocs: mockArchitectureDocs(options?.architectureDocCount ?? 10),
    userPreferences: mockUserPreferences(),
  };
};
