/**
 * API Types for ClaudeManual
 *
 * Auto-generated from OpenAPI 3.0 specification
 * Generated: 2026-01-31
 * Session: session-api-contracts-claudemanual
 *
 * Traceability:
 * - REQ-036: API endpoint design
 * - REQ-037: Search and filter capabilities
 */

// ============================================================================
// Core Entity Types
// ============================================================================

export type Stage =
  | 'Discovery'
  | 'Prototype'
  | 'ProductSpecs'
  | 'SolArch'
  | 'Implementation'
  | 'Utility'
  | 'GRC'
  | 'Security';

export type Model = 'sonnet' | 'opus' | 'haiku';

export type Theme = 'light' | 'dark' | 'system';

export type HookType = 'PreToolUse' | 'PostToolUse' | 'Stop' | 'lifecycle';

export type Language = 'python' | 'bash';

export type DiagramFormat = 'md' | 'mermaid' | 'plantuml';

export type WorkflowCategory = 'process' | 'integration' | 'decision' | 'data-flow';

export type RuleCategory = 'core' | 'stage-specific' | 'quality' | 'process';

export type WaysOfWorkingCategory = 'practices' | 'guidelines' | 'processes' | 'checklists';

export type Audience = 'developers' | 'product' | 'all' | 'leads';

export type ArchitectureCategory = 'c4' | 'adr' | 'patterns' | 'infrastructure' | 'data-model';

export type C4Level = 'context' | 'container' | 'component' | 'code';

export type ADRStatus = 'proposed' | 'accepted' | 'deprecated' | 'superseded';

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
// Entity Interfaces
// ============================================================================

export interface Skill {
  id: string;
  name: string;
  description: string;
  stage: Stage;
  path: string;
  model?: Model;
  context?: 'fork' | null;
  agent?: string;
  allowed_tools?: string[];
  skills_required?: string[];
  hooks?: Record<string, unknown>;

  // Derived fields
  stage_prefix?: string;
  category?: string;
  file_size?: number;
  last_modified?: Date;
  content_hash?: string;

  // Content sections
  content?: {
    purpose: string;
    usage: string;
    options?: string;
    example: string;
    workflow?: string;
    related?: string;
  };
}

export interface Command {
  id: string;
  name: string;
  description: string;
  stage: Exclude<Stage, 'GRC' | 'Security'>;
  path: string;
  model?: string;
  allowed_tools?: string[];
  argument_hint?: string;

  // Derived fields
  invocation_syntax?: string;
  requires_system_name?: boolean;
  has_options?: boolean;

  // Content sections
  content?: {
    usage: string;
    arguments?: string;
    options?: string;
    example: string;
    execution?: string;
    related?: string;
  };
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  model: Model;
  checkpoint?: number;
  path: string;
  tools?: string[];
  color?: 'blue' | 'green' | 'purple' | 'orange' | 'red';
  stage: Stage;

  // Derived fields
  stage_prefix?: string;
  role?: string;
  subagent_type?: 'general-purpose' | 'Explore' | 'Plan' | 'Bash';

  // Content sections
  content?: {
    expertise: string;
    approach?: string;
    skills_to_load?: string;
    output_format: string;
    related?: string;
  };
}

export interface Rule {
  id: string;
  name: string;
  description: string;
  path: string;
  auto_load_paths?: string[];
  version?: string;
  category?: RuleCategory;

  // Derived fields
  applies_to_stages?: string[];

  // Content sections
  content?: {
    overview: string;
    rules: string;
    examples?: string;
    related?: string;
  };
}

export interface Hook {
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

export interface Workflow {
  id: string;
  name: string;
  description: string;
  format: DiagramFormat;
  path: string;
  stage?: Exclude<Stage, 'GRC' | 'Security'>;
  category?: WorkflowCategory;
  tags?: string[];

  // Content sections
  content?: {
    overview?: string;
    diagram: string;
    steps?: string;
    related?: string;
  };
}

export interface WaysOfWorking {
  id: string;
  name: string;
  description: string;
  path: string;
  category?: WaysOfWorkingCategory;
  audience?: Audience;
  tags?: string[];

  // Content sections
  content?: {
    overview: string;
    guidelines?: string;
    examples?: string;
    checklist?: string;
  };
}

export interface ArchitectureDoc {
  id: string;
  name: string;
  description: string;
  format: DiagramFormat;
  path: string;
  category?: ArchitectureCategory;
  c4_level?: C4Level;
  adr_status?: ADRStatus;
  tags?: string[];
  related_adrs?: string[];

  // Content sections
  content?: {
    overview: string;
    diagram?: string;
    context?: string;
    decision?: string;
    consequences?: string;
    related?: string;
  };
}

export interface UserPreferences {
  theme: Theme;
  favorites: string[];
  collapsed_nodes: string[];
  last_viewed?: string | null;
  search_history: string[];
  stage_filter: string[];
  type_filter: EntityType[];
}

// ============================================================================
// Request Types
// ============================================================================

export interface BaseQueryParams {
  page?: number;
  pageSize?: number;
  search?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export interface ListSkillsRequest extends BaseQueryParams {
  stage?: Stage[];
  model?: Model[];
  has_example?: boolean;
  favorited?: boolean;
}

export interface ListCommandsRequest extends BaseQueryParams {
  stage?: Exclude<Stage, 'GRC' | 'Security'>[];
  requires_system_name?: boolean;
  has_options?: boolean;
}

export interface ListAgentsRequest extends BaseQueryParams {
  stage?: Stage[];
  model?: Model[];
  checkpoint?: number;
}

export interface ListRulesRequest extends BaseQueryParams {
  category?: RuleCategory[];
}

export interface ListHooksRequest extends BaseQueryParams {
  type?: HookType[];
  language?: Language[];
}

export interface ListWorkflowsRequest extends BaseQueryParams {
  stage?: Exclude<Stage, 'GRC' | 'Security'>[];
  category?: WorkflowCategory[];
  format?: DiagramFormat[];
  tags?: string[];
}

export interface ListWaysOfWorkingRequest extends BaseQueryParams {
  category?: WaysOfWorkingCategory[];
  audience?: Audience[];
  tags?: string[];
}

export interface ListArchitectureDocsRequest extends BaseQueryParams {
  category?: ArchitectureCategory[];
  c4_level?: C4Level[];
  adr_status?: ADRStatus[];
  format?: DiagramFormat[];
  tags?: string[];
}

export interface SearchRequest {
  query: string;
  types?: EntityType[];
  stage?: string[];
  limit?: number;
}

export interface UpdatePreferencesRequest {
  theme?: Theme;
  favorites?: string[];
  collapsed_nodes?: string[];
  last_viewed?: string | null;
  stage_filter?: string[];
  type_filter?: EntityType[];
}

// ============================================================================
// Response Types
// ============================================================================

export interface Pagination {
  page: number;
  pageSize: number;
  totalItems: number;
  totalPages: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: Pagination;
}

export type SkillListResponse = PaginatedResponse<Skill>;
export type CommandListResponse = PaginatedResponse<Command>;
export type AgentListResponse = PaginatedResponse<Agent>;
export type RuleListResponse = PaginatedResponse<Rule>;
export type HookListResponse = PaginatedResponse<Hook>;
export type WorkflowListResponse = PaginatedResponse<Workflow>;
export type WaysOfWorkingListResponse = PaginatedResponse<WaysOfWorking>;
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
  stage?: string;
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
  details?: Record<string, unknown>;
}

// ============================================================================
// File Watch Types (SSE)
// ============================================================================

export interface FileChangeEvent {
  type: 'created' | 'modified' | 'deleted';
  path: string;
  entity_type?: EntityType;
  entity_id?: string;
  timestamp: string;
}

// ============================================================================
// Input Types (for create/update operations)
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

export type CreateWorkflowInput = Omit<Workflow, 'content'>;
export type UpdateWorkflowInput = Partial<CreateWorkflowInput>;

export type CreateWaysOfWorkingInput = Omit<WaysOfWorking, 'content'>;
export type UpdateWaysOfWorkingInput = Partial<CreateWaysOfWorkingInput>;

export type CreateArchitectureDocInput = Omit<ArchitectureDoc, 'content'>;
export type UpdateArchitectureDocInput = Partial<CreateArchitectureDocInput>;

// ============================================================================
// API Client Configuration
// ============================================================================

export interface ApiConfig {
  baseUrl: string;
  timeout?: number;
  headers?: Record<string, string>;
}

export const defaultApiConfig: ApiConfig = {
  baseUrl: 'http://localhost:3001/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};
