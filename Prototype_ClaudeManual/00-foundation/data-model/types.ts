/**
 * ClaudeManual Data Model - TypeScript Types
 *
 * Generated: 2026-01-31
 * Session: session-data-model-claudemanual
 * Agent: prototype-data-model-specifier
 *
 * Entities: 9
 * Total Fields: 122
 * Relationships: 8
 */

// ============================================================================
// ENUMS
// ============================================================================

export enum Stage {
  Discovery = 'Discovery',
  Prototype = 'Prototype',
  ProductSpecs = 'ProductSpecs',
  SolArch = 'SolArch',
  Implementation = 'Implementation',
  Utility = 'Utility',
  GRC = 'GRC',
  Security = 'Security',
}

export enum Model {
  Sonnet = 'sonnet',
  Opus = 'opus',
  Haiku = 'haiku',
}

export enum Context {
  Fork = 'fork',
}

export enum Theme {
  Light = 'light',
  Dark = 'dark',
  System = 'system',
}

export enum Format {
  Markdown = 'md',
  Mermaid = 'mermaid',
  PlantUML = 'plantuml',
}

export enum WorkflowCategory {
  Process = 'process',
  Integration = 'integration',
  Decision = 'decision',
  DataFlow = 'data-flow',
}

export enum WaysOfWorkingCategory {
  Practices = 'practices',
  Guidelines = 'guidelines',
  Processes = 'processes',
  Checklists = 'checklists',
}

export enum ArchitectureCategory {
  C4 = 'c4',
  ADR = 'adr',
  Patterns = 'patterns',
  Infrastructure = 'infrastructure',
  DataModel = 'data-model',
}

export enum C4Level {
  Context = 'context',
  Container = 'container',
  Component = 'component',
  Code = 'code',
}

export enum ADRStatus {
  Proposed = 'proposed',
  Accepted = 'accepted',
  Deprecated = 'deprecated',
  Superseded = 'superseded',
}

export enum HookType {
  PreToolUse = 'PreToolUse',
  PostToolUse = 'PostToolUse',
  Stop = 'Stop',
  Lifecycle = 'lifecycle',
}

export enum Language {
  Python = 'python',
  Bash = 'bash',
}

export enum Audience {
  Developers = 'developers',
  Product = 'product',
  All = 'all',
  Leads = 'leads',
}

export enum RuleCategory {
  Core = 'core',
  StageSpecific = 'stage-specific',
  Quality = 'quality',
  Process = 'process',
}

export enum SubagentType {
  GeneralPurpose = 'general-purpose',
  Explore = 'Explore',
  Plan = 'Plan',
  Bash = 'Bash',
}

export enum AgentColor {
  Blue = 'blue',
  Green = 'green',
  Purple = 'purple',
  Orange = 'orange',
  Red = 'red',
}

export type EntityType =
  | 'Skill'
  | 'Command'
  | 'Agent'
  | 'Rule'
  | 'Hook'
  | 'Workflow'
  | 'WaysOfWorking'
  | 'ArchitectureDoc';

// ============================================================================
// CONTENT SECTIONS
// ============================================================================

export interface SkillContent {
  purpose: string;
  usage: string;
  options?: string;
  example: string;
  workflow?: string;
  related?: string;
}

export interface CommandContent {
  usage: string;
  arguments?: string;
  options?: string;
  example: string;
  execution?: string;
  related?: string;
}

export interface AgentContent {
  expertise: string;
  approach?: string;
  skills_to_load?: string;
  output_format: string;
  related?: string;
}

export interface RuleContent {
  overview: string;
  rules: string;
  examples?: string;
  related?: string;
}

export interface WorkflowContent {
  overview?: string;
  diagram: string;
  steps?: string;
  related?: string;
}

export interface WaysOfWorkingContent {
  overview: string;
  guidelines?: string;
  examples?: string;
  checklist?: string;
}

export interface ArchitectureDocContent {
  overview: string;
  diagram?: string;
  context?: string;
  decision?: string;
  consequences?: string;
  related?: string;
}

// ============================================================================
// ENTITY INTERFACES
// ============================================================================

/**
 * ENT-001: Skill
 *
 * Reusable AI prompt template for specific tasks
 * Location: .claude/skills/{skill-id}/SKILL.md
 * Traces To: CF-001, CF-008, JTBD-1.2, JTBD-1.3
 */
export interface Skill {
  // Core fields
  id: string;
  name: string;
  description: string;
  stage: Stage;
  path: string;
  model?: Model;
  context?: Context | null;
  agent?: string;
  allowed_tools?: string[];
  skills_required?: string[];
  hooks?: Record<string, any>;

  // Derived fields
  stage_prefix?: string;
  category?: string;
  file_size?: number;
  last_modified?: Date;
  content_hash?: string;

  // Content sections
  content?: SkillContent;
}

/**
 * ENT-002: Command
 *
 * Slash command executable in Claude Code
 * Location: .claude/commands/{command-id}.md
 * Traces To: CF-001, CF-007, JTBD-1.1, JTBD-1.4
 */
export interface Command {
  // Core fields
  id: string;
  name: string;
  description: string;
  stage: Stage;
  path: string;
  model?: string;
  allowed_tools?: string[];
  argument_hint?: string;

  // Derived fields
  invocation_syntax?: string;
  requires_system_name?: boolean;
  has_options?: boolean;

  // Content sections
  content?: CommandContent;
}

/**
 * ENT-003: Agent
 *
 * Specialized AI persona with specific skills and model configuration
 * Location: .claude/agents/{agent-id}.md
 * Traces To: CF-001, CF-008, JTBD-1.2
 */
export interface Agent {
  // Core fields
  id: string;
  name: string;
  description: string;
  model: Model;
  checkpoint?: number;
  path: string;
  tools?: string[];
  color?: AgentColor;
  stage: Stage;

  // Derived fields
  stage_prefix?: string;
  role?: string;
  subagent_type?: SubagentType;

  // Content sections
  content?: AgentContent;
}

/**
 * ENT-004: Rule
 *
 * Framework rules and conventions
 * Location: .claude/rules/{rule-id}.md
 * Traces To: CF-001, JTBD-1.2
 */
export interface Rule {
  // Core fields
  id: string;
  name: string;
  description: string;
  path: string;
  auto_load_paths?: string[];
  version?: string;
  category?: RuleCategory;

  // Derived fields
  applies_to_stages?: Stage[];

  // Content sections
  content?: RuleContent;
}

/**
 * ENT-005: Hook
 *
 * Lifecycle hooks for commands, skills, and agents
 * Location: .claude/hooks/{hook-id}.(py|sh)
 * Traces To: CF-001, JTBD-1.5
 */
export interface Hook {
  // Core fields
  id: string;
  name: string;
  description: string;
  path: string;
  type: HookType;
  language: Language;

  // Derived fields
  executable?: boolean;
  has_shebang?: boolean;
}

/**
 * ENT-006: UserPreferences
 *
 * Per-user settings stored in browser localStorage
 * Location: Browser localStorage
 * Traces To: CF-003, CF-012, CF-016, JTBD-1.6
 */
export interface UserPreferences {
  theme: Theme;
  favorites: string[];
  collapsed_nodes: string[];
  last_viewed?: string | null;
  search_history: string[];
  stage_filter: Stage[];
  type_filter: EntityType[];
}

/**
 * ENT-007: Workflow
 *
 * Process and workflow diagrams
 * Location: .claude/ or project folders
 * Traces To: CF-001, JTBD-1.9, JTBD-1.2
 */
export interface Workflow {
  // Core fields
  id: string;
  name: string;
  description: string;
  format: Format;
  path: string;
  stage?: Stage;
  category?: WorkflowCategory;
  tags?: string[];

  // Content sections
  content?: WorkflowContent;
}

/**
 * ENT-008: WaysOfWorking
 *
 * Team practices, guidelines, and process documentation
 * Location: Documentation folders
 * Traces To: CF-001, JTBD-1.9, JTBD-1.1
 */
export interface WaysOfWorking {
  // Core fields
  id: string;
  name: string;
  description: string;
  path: string;
  category?: WaysOfWorkingCategory;
  audience?: Audience;
  tags?: string[];

  // Content sections
  content?: WaysOfWorkingContent;
}

/**
 * ENT-009: ArchitectureDoc
 *
 * Architecture diagrams and documentation (C4, ADRs, patterns)
 * Location: architecture/ folder
 * Traces To: CF-001, JTBD-1.9, JTBD-1.2, JTBD-2.1
 */
export interface ArchitectureDoc {
  // Core fields
  id: string;
  name: string;
  description: string;
  format: Format;
  path: string;
  category?: ArchitectureCategory;
  c4_level?: C4Level;
  adr_status?: ADRStatus;
  tags?: string[];
  related_adrs?: string[];

  // Content sections
  content?: ArchitectureDocContent;
}

// ============================================================================
// INPUT TYPES (Create/Update)
// ============================================================================

export type CreateSkillInput = Omit<Skill, 'file_size' | 'last_modified' | 'content_hash' | 'stage_prefix' | 'category'>;
export type UpdateSkillInput = Partial<CreateSkillInput>;

export type CreateCommandInput = Omit<Command, 'invocation_syntax' | 'requires_system_name' | 'has_options'>;
export type UpdateCommandInput = Partial<CreateCommandInput>;

export type CreateAgentInput = Omit<Agent, 'stage_prefix' | 'role' | 'subagent_type'>;
export type UpdateAgentInput = Partial<CreateAgentInput>;

export type CreateRuleInput = Omit<Rule, 'applies_to_stages'>;
export type UpdateRuleInput = Partial<CreateRuleInput>;

export type CreateHookInput = Omit<Hook, 'executable' | 'has_shebang'>;
export type UpdateHookInput = Partial<CreateHookInput>;

export type UpdatePreferencesInput = Partial<UserPreferences>;

export type CreateWorkflowInput = Omit<Workflow, 'content'>;
export type UpdateWorkflowInput = Partial<CreateWorkflowInput>;

export type CreateWaysOfWorkingInput = Omit<WaysOfWorking, 'content'>;
export type UpdateWaysOfWorkingInput = Partial<CreateWaysOfWorkingInput>;

export type CreateArchitectureDocInput = Omit<ArchitectureDoc, 'content'>;
export type UpdateArchitectureDocInput = Partial<CreateArchitectureDocInput>;

// ============================================================================
// API REQUEST TYPES
// ============================================================================

export interface BaseQueryParams {
  page?: number;           // Default: 1
  pageSize?: number;       // Default: 20, Max: 100
  search?: string;         // Full-text search
  sortBy?: string;         // Field to sort by
  sortOrder?: 'asc' | 'desc'; // Default: 'asc'
}

export interface SkillQueryParams extends BaseQueryParams {
  stage?: Stage[];
  model?: Model[];
  has_example?: boolean;
  favorited?: boolean;
}

export interface CommandQueryParams extends BaseQueryParams {
  stage?: Stage[];
  requires_system_name?: boolean;
  has_options?: boolean;
}

export interface AgentQueryParams extends BaseQueryParams {
  stage?: Stage[];
  model?: Model[];
  checkpoint?: number;
}

export interface WorkflowQueryParams extends BaseQueryParams {
  stage?: Stage[];
  category?: WorkflowCategory[];
  format?: Format[];
  tags?: string[];
}

export interface ArchitectureDocQueryParams extends BaseQueryParams {
  category?: ArchitectureCategory[];
  c4_level?: C4Level[];
  adr_status?: ADRStatus[];
  format?: Format[];
  tags?: string[];
}

export interface SearchRequest {
  query: string;
  types?: EntityType[];
  stage?: Stage[];
  limit?: number;
}

// ============================================================================
// API RESPONSE TYPES
// ============================================================================

export interface PaginationMeta {
  page: number;
  pageSize: number;
  totalItems: number;
  totalPages: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: PaginationMeta;
}

export type SkillListResponse = PaginatedResponse<Skill>;
export type CommandListResponse = PaginatedResponse<Command>;
export type AgentListResponse = PaginatedResponse<Agent>;
export type WorkflowListResponse = PaginatedResponse<Workflow>;
export type ArchitectureDocListResponse = PaginatedResponse<ArchitectureDoc>;

export interface SkillDetailResponse {
  skill: Skill;
  related_skills: Skill[];
  used_by_commands: Command[];
  used_by_agents: Agent[];
}

export interface CommandDetailResponse {
  command: Command;
  invoked_skills: Skill[];
  spawned_agents: Agent[];
}

export interface AgentDetailResponse {
  agent: Agent;
  loaded_skills: Skill[];
  spawned_by_commands: Command[];
}

export interface SearchResult {
  id: string;
  type: EntityType;
  name: string;
  description: string;
  stage?: Stage;
  score: number;
}

export interface SearchResponse {
  results: SearchResult[];
  total: number;
}

export interface ErrorResponse {
  error: string;
  message: string;
  code: string;
  details?: Record<string, any>;
}

// ============================================================================
// RELATIONSHIP TYPES
// ============================================================================

export interface Relationship {
  from_entity: EntityType;
  from_id: string;
  to_entity: EntityType;
  to_id: string;
  relationship_type:
    | 'uses_skill'
    | 'invokes_skill'
    | 'orchestrates_agents'
    | 'loads_skill'
    | 'favorites'
    | 'referenced_in'
    | 'related_adrs';
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

export type AnyEntity =
  | Skill
  | Command
  | Agent
  | Rule
  | Hook
  | UserPreferences
  | Workflow
  | WaysOfWorking
  | ArchitectureDoc;

export interface EntityMap {
  Skill: Skill;
  Command: Command;
  Agent: Agent;
  Rule: Rule;
  Hook: Hook;
  UserPreferences: UserPreferences;
  Workflow: Workflow;
  WaysOfWorking: WaysOfWorking;
  ArchitectureDoc: ArchitectureDoc;
}

export type EntityOfType<T extends EntityType> = EntityMap[T];

// ============================================================================
// VALIDATION TYPES
// ============================================================================

export interface ValidationError {
  rule_id: string;
  field: string;
  message: string;
  value?: any;
}

export interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
}

// ============================================================================
// INDEX TYPES
// ============================================================================

export interface SearchIndex {
  entity_type: EntityType;
  entity_id: string;
  field_name: string;
  field_value: string;
  weight: number;
}

export interface FilterConfig {
  id: string;
  name: string;
  type: 'multi-select' | 'boolean' | 'single-select';
  values?: string[];
  default?: any;
}
