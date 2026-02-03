/**
 * ClaudeManual Data Model - Zod Validation Schemas
 *
 * Generated: 2026-01-31
 * Session: session-data-model-claudemanual
 * Agent: prototype-data-model-specifier
 *
 * Validation Rules: 27
 */

import { z } from 'zod';
import {
  Stage,
  Model,
  Context,
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
// ENUM SCHEMAS
// ============================================================================

export const stageSchema = z.nativeEnum(Stage);
export const modelSchema = z.nativeEnum(Model);
export const contextSchema = z.nativeEnum(Context).nullable().optional();
export const themeSchema = z.nativeEnum(Theme);
export const formatSchema = z.nativeEnum(Format);
export const workflowCategorySchema = z.nativeEnum(WorkflowCategory);
export const waysOfWorkingCategorySchema = z.nativeEnum(WaysOfWorkingCategory);
export const architectureCategorySchema = z.nativeEnum(ArchitectureCategory);
export const c4LevelSchema = z.nativeEnum(C4Level);
export const adrStatusSchema = z.nativeEnum(ADRStatus);
export const hookTypeSchema = z.nativeEnum(HookType);
export const languageSchema = z.nativeEnum(Language);
export const audienceSchema = z.nativeEnum(Audience);
export const ruleCategorySchema = z.nativeEnum(RuleCategory);
export const agentColorSchema = z.nativeEnum(AgentColor);
export const entityTypeSchema = z.enum([
  'Skill',
  'Command',
  'Agent',
  'Rule',
  'Hook',
  'Workflow',
  'WaysOfWorking',
  'ArchitectureDoc',
]);

// ============================================================================
// CONTENT SECTION SCHEMAS
// ============================================================================

export const skillContentSchema = z.object({
  purpose: z.string(),
  usage: z.string(),
  options: z.string().optional(),
  example: z.string(),
  workflow: z.string().optional(),
  related: z.string().optional(),
});

export const commandContentSchema = z.object({
  usage: z.string(),
  arguments: z.string().optional(),
  options: z.string().optional(),
  example: z.string(),
  execution: z.string().optional(),
  related: z.string().optional(),
});

export const agentContentSchema = z.object({
  expertise: z.string(),
  approach: z.string().optional(),
  skills_to_load: z.string().optional(),
  output_format: z.string(),
  related: z.string().optional(),
});

export const ruleContentSchema = z.object({
  overview: z.string(),
  rules: z.string(),
  examples: z.string().optional(),
  related: z.string().optional(),
});

export const workflowContentSchema = z.object({
  overview: z.string().optional(),
  diagram: z.string(),
  steps: z.string().optional(),
  related: z.string().optional(),
});

export const waysOfWorkingContentSchema = z.object({
  overview: z.string(),
  guidelines: z.string().optional(),
  examples: z.string().optional(),
  checklist: z.string().optional(),
});

export const architectureDocContentSchema = z.object({
  overview: z.string(),
  diagram: z.string().optional(),
  context: z.string().optional(),
  decision: z.string().optional(),
  consequences: z.string().optional(),
  related: z.string().optional(),
});

// ============================================================================
// ENTITY SCHEMAS
// ============================================================================

/**
 * VR-SKL-001: ID must match folder name
 * VR-SKL-002: File must exist at path
 * VR-SKL-003: Stage must be valid enum
 * VR-SKL-004: Must have Purpose and Usage sections
 * VR-SKL-005: Referenced skills must exist
 */
export const skillSchema = z.object({
  id: z
    .string()
    .regex(/^[a-zA-Z0-9_-]+$/, 'Invalid skill ID format (VR-SKL-001)')
    .min(1, 'Skill ID cannot be empty'),
  name: z
    .string()
    .min(2, 'Skill name must be at least 2 characters')
    .max(100, 'Skill name must not exceed 100 characters'),
  description: z
    .string()
    .min(10, 'Description must be at least 10 characters')
    .max(500, 'Description must not exceed 500 characters'),
  stage: stageSchema,
  path: z
    .string()
    .regex(/^\.claude\/skills\/[^/]+\/SKILL\.md$/, 'Invalid skill path (VR-SKL-002)'),
  model: modelSchema.optional(),
  context: contextSchema,
  agent: z.string().optional(),
  allowed_tools: z.array(z.string()).optional(),
  skills_required: z.array(z.string()).optional(),
  hooks: z.record(z.any()).optional(),

  // Derived fields (optional, computed)
  stage_prefix: z.string().optional(),
  category: z.string().optional(),
  file_size: z.number().optional(),
  last_modified: z.date().optional(),
  content_hash: z.string().optional(),

  // Content sections
  content: skillContentSchema.optional(),
});

/**
 * VR-CMD-001: ID must match filename
 * VR-CMD-002: Stage must be valid enum
 * VR-CMD-003: Must have Usage and Example sections
 */
export const commandSchema = z.object({
  id: z
    .string()
    .regex(/^[a-z0-9-]+$/, 'Invalid command ID format (VR-CMD-001)')
    .min(1, 'Command ID cannot be empty'),
  name: z.string().min(2).max(100),
  description: z.string().min(10).max(500),
  stage: stageSchema,
  path: z
    .string()
    .regex(/^\.claude\/commands\/[^/]+\.md$/, 'Invalid command path (VR-CMD-001)'),
  model: z.string().optional(),
  allowed_tools: z.array(z.string()).optional(),
  argument_hint: z.string().optional(),

  // Derived fields
  invocation_syntax: z.string().optional(),
  requires_system_name: z.boolean().optional(),
  has_options: z.boolean().optional(),

  // Content sections
  content: commandContentSchema.optional(),
});

/**
 * VR-AGT-001: ID must follow {stage}-{role} naming
 * VR-AGT-002: Model must be valid enum
 * VR-AGT-003: Must have Expertise and Output Format sections
 */
export const agentSchema = z.object({
  id: z
    .string()
    .regex(/^[a-z0-9-]+$/, 'Invalid agent ID format (VR-AGT-001)')
    .min(1, 'Agent ID cannot be empty'),
  name: z.string().min(2).max(100),
  description: z.string().min(10).max(500),
  model: modelSchema,
  checkpoint: z.number().int().min(1).max(20).optional(),
  path: z
    .string()
    .regex(/^\.claude\/agents\/[^/]+\.md$/, 'Invalid agent path (VR-AGT-001)'),
  tools: z.array(z.string()).optional(),
  color: agentColorSchema.optional(),
  stage: stageSchema,

  // Derived fields
  stage_prefix: z.string().optional(),
  role: z.string().optional(),
  subagent_type: z.enum(['general-purpose', 'Explore', 'Plan', 'Bash']).optional(),

  // Content sections
  content: agentContentSchema.optional(),
});

/**
 * VR-RUL-001: File must exist
 * VR-RUL-002: Auto-load paths must be valid glob patterns
 */
export const ruleSchema = z.object({
  id: z
    .string()
    .regex(/^[a-zA-Z0-9_-]+$/, 'Invalid rule ID format')
    .min(1, 'Rule ID cannot be empty'),
  name: z.string().min(2).max(100),
  description: z.string().min(10).max(500),
  path: z
    .string()
    .regex(/^\.claude\/rules\/[^/]+\.md$/, 'Invalid rule path (VR-RUL-001)'),
  auto_load_paths: z.array(z.string()).optional(),
  version: z
    .string()
    .regex(/^\d+\.\d+\.\d+$/, 'Invalid version format (must be semantic versioning)')
    .optional(),
  category: ruleCategorySchema.optional(),

  // Derived fields
  applies_to_stages: z.array(stageSchema).optional(),

  // Content sections
  content: ruleContentSchema.optional(),
});

/**
 * VR-HKS-001: File must exist and be executable
 * VR-HKS-002: Language must match file extension
 */
export const hookSchema = z.object({
  id: z
    .string()
    .regex(/^[a-z0-9_-]+$/, 'Invalid hook ID format')
    .min(1, 'Hook ID cannot be empty'),
  name: z.string().min(2).max(100),
  description: z.string().min(10).max(500),
  path: z
    .string()
    .regex(/^\.claude\/hooks\/[^/]+\.(py|sh)$/, 'Invalid hook path (VR-HKS-001, VR-HKS-002)'),
  type: hookTypeSchema,
  language: languageSchema,

  // Derived fields
  executable: z.boolean().optional(),
  has_shebang: z.boolean().optional(),
});

/**
 * VR-USR-001: Theme must be valid enum
 * VR-USR-002: Referenced items must exist
 * VR-USR-003: Search history max 20 items
 */
export const userPreferencesSchema = z.object({
  theme: themeSchema,
  favorites: z.array(z.string()),
  collapsed_nodes: z.array(z.string()),
  last_viewed: z.string().nullable().optional(),
  search_history: z
    .array(z.string())
    .max(20, 'Search history exceeds limit (VR-USR-003)'),
  stage_filter: z.array(stageSchema),
  type_filter: z.array(entityTypeSchema),
});

/**
 * VR-WFL-001: File must exist
 * VR-WFL-002: File extension must match format
 * VR-WFL-003: Must have Diagram section for mermaid/plantuml
 */
export const workflowSchema = z.object({
  id: z
    .string()
    .regex(/^[a-z0-9-]+$/, 'Invalid workflow ID format')
    .min(1, 'Workflow ID cannot be empty'),
  name: z.string().min(2).max(100),
  description: z.string().min(10).max(500),
  format: formatSchema,
  path: z.string().min(1, 'Path cannot be empty (VR-WFL-001)'),
  stage: stageSchema.optional(),
  category: workflowCategorySchema.optional(),
  tags: z.array(z.string()).optional(),

  // Content sections
  content: workflowContentSchema.optional(),
});

/**
 * VR-WOW-001: File must exist
 * VR-WOW-002: Must have Overview section
 */
export const waysOfWorkingSchema = z.object({
  id: z
    .string()
    .regex(/^[a-z0-9-]+$/, 'Invalid WaysOfWorking ID format')
    .min(1, 'WaysOfWorking ID cannot be empty'),
  name: z.string().min(2).max(100),
  description: z.string().min(10).max(500),
  path: z
    .string()
    .endsWith('.md', 'Path must end with .md (VR-WOW-001)')
    .min(1, 'Path cannot be empty'),
  category: waysOfWorkingCategorySchema.optional(),
  audience: audienceSchema.optional(),
  tags: z.array(z.string()).optional(),

  // Content sections
  content: waysOfWorkingContentSchema.optional(),
});

/**
 * VR-ARC-001: File must exist
 * VR-ARC-002: File extension must match format
 * VR-ARC-003: C4 diagrams should specify c4_level
 * VR-ARC-004: ADRs should specify adr_status
 */
export const architectureDocSchema = z.object({
  id: z
    .string()
    .regex(/^[a-zA-Z0-9-_]+$/, 'Invalid ArchitectureDoc ID format')
    .min(1, 'ArchitectureDoc ID cannot be empty'),
  name: z.string().min(2).max(100),
  description: z.string().min(10).max(500),
  format: formatSchema,
  path: z.string().min(1, 'Path cannot be empty (VR-ARC-001)'),
  category: architectureCategorySchema.optional(),
  c4_level: c4LevelSchema.optional(),
  adr_status: adrStatusSchema.optional(),
  tags: z.array(z.string()).optional(),
  related_adrs: z.array(z.string()).optional(),

  // Content sections
  content: architectureDocContentSchema.optional(),
});

// ============================================================================
// INPUT SCHEMAS (Create/Update)
// ============================================================================

export const createSkillSchema = skillSchema.omit({
  file_size: true,
  last_modified: true,
  content_hash: true,
  stage_prefix: true,
  category: true,
});

export const updateSkillSchema = createSkillSchema.partial();

export const createCommandSchema = commandSchema.omit({
  invocation_syntax: true,
  requires_system_name: true,
  has_options: true,
});

export const updateCommandSchema = createCommandSchema.partial();

export const createAgentSchema = agentSchema.omit({
  stage_prefix: true,
  role: true,
  subagent_type: true,
});

export const updateAgentSchema = createAgentSchema.partial();

export const createRuleSchema = ruleSchema.omit({
  applies_to_stages: true,
});

export const updateRuleSchema = createRuleSchema.partial();

export const createHookSchema = hookSchema.omit({
  executable: true,
  has_shebang: true,
});

export const updateHookSchema = createHookSchema.partial();

export const updatePreferencesSchema = userPreferencesSchema.partial();

export const createWorkflowSchema = workflowSchema.omit({ content: true });
export const updateWorkflowSchema = createWorkflowSchema.partial();

export const createWaysOfWorkingSchema = waysOfWorkingSchema.omit({ content: true });
export const updateWaysOfWorkingSchema = createWaysOfWorkingSchema.partial();

export const createArchitectureDocSchema = architectureDocSchema.omit({ content: true });
export const updateArchitectureDocSchema = createArchitectureDocSchema.partial();

// ============================================================================
// API REQUEST SCHEMAS
// ============================================================================

export const baseQueryParamsSchema = z.object({
  page: z.number().int().min(1).default(1).optional(),
  pageSize: z.number().int().min(1).max(100).default(20).optional(),
  search: z.string().optional(),
  sortBy: z.string().optional(),
  sortOrder: z.enum(['asc', 'desc']).default('asc').optional(),
});

export const skillQueryParamsSchema = baseQueryParamsSchema.extend({
  stage: z.array(stageSchema).optional(),
  model: z.array(modelSchema).optional(),
  has_example: z.boolean().optional(),
  favorited: z.boolean().optional(),
});

export const commandQueryParamsSchema = baseQueryParamsSchema.extend({
  stage: z.array(stageSchema).optional(),
  requires_system_name: z.boolean().optional(),
  has_options: z.boolean().optional(),
});

export const agentQueryParamsSchema = baseQueryParamsSchema.extend({
  stage: z.array(stageSchema).optional(),
  model: z.array(modelSchema).optional(),
  checkpoint: z.number().int().min(1).max(20).optional(),
});

export const workflowQueryParamsSchema = baseQueryParamsSchema.extend({
  stage: z.array(stageSchema).optional(),
  category: z.array(workflowCategorySchema).optional(),
  format: z.array(formatSchema).optional(),
  tags: z.array(z.string()).optional(),
});

export const architectureDocQueryParamsSchema = baseQueryParamsSchema.extend({
  category: z.array(architectureCategorySchema).optional(),
  c4_level: z.array(c4LevelSchema).optional(),
  adr_status: z.array(adrStatusSchema).optional(),
  format: z.array(formatSchema).optional(),
  tags: z.array(z.string()).optional(),
});

export const searchRequestSchema = z.object({
  query: z.string().min(1, 'Search query cannot be empty'),
  types: z.array(entityTypeSchema).optional(),
  stage: z.array(stageSchema).optional(),
  limit: z.number().int().min(1).max(100).default(20).optional(),
});

// ============================================================================
// VALIDATION UTILITIES
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

/**
 * Validate entity against schema
 */
export function validateEntity<T>(
  schema: z.ZodSchema<T>,
  data: unknown
): ValidationResult {
  const result = schema.safeParse(data);

  if (result.success) {
    return { valid: true, errors: [] };
  }

  const errors: ValidationError[] = result.error.errors.map((err) => ({
    rule_id: err.code,
    field: err.path.join('.'),
    message: err.message,
    value: (data as any)?.[err.path[0]],
  }));

  return { valid: false, errors };
}

/**
 * Extract rule ID from error message
 */
export function extractRuleId(message: string): string | null {
  const match = message.match(/\(VR-[A-Z]+-\d+\)/);
  return match ? match[0].slice(1, -1) : null;
}

/**
 * Validate skill dependencies exist
 * VR-SKL-005: Referenced skills must exist
 */
export function validateSkillDependencies(
  skill: any,
  allSkills: Set<string>
): ValidationError[] {
  const errors: ValidationError[] = [];

  if (skill.skills_required) {
    for (const depId of skill.skills_required) {
      if (!allSkills.has(depId)) {
        errors.push({
          rule_id: 'VR-SKL-005',
          field: 'skills_required',
          message: `Dependent skill not found: ${depId}`,
          value: depId,
        });
      }
    }
  }

  return errors;
}

/**
 * Validate user preferences favorites exist
 * VR-USR-002: Referenced items must exist
 */
export function validateFavorites(
  favorites: string[],
  allItemIds: Set<string>
): ValidationError[] {
  const errors: ValidationError[] = [];

  for (const favId of favorites) {
    if (!allItemIds.has(favId)) {
      errors.push({
        rule_id: 'VR-USR-002',
        field: 'favorites',
        message: `Favorite item not found: ${favId}`,
        value: favId,
      });
    }
  }

  return errors;
}

/**
 * Validate C4 diagrams have c4_level
 * VR-ARC-003: C4 diagrams should specify c4_level
 */
export function validateC4Level(doc: any): ValidationError[] {
  const errors: ValidationError[] = [];

  if (doc.category === 'c4' && !doc.c4_level) {
    errors.push({
      rule_id: 'VR-ARC-003',
      field: 'c4_level',
      message: 'C4 diagrams should specify c4_level',
    });
  }

  return errors;
}

/**
 * Validate ADRs have adr_status
 * VR-ARC-004: ADRs should specify adr_status
 */
export function validateADRStatus(doc: any): ValidationError[] {
  const errors: ValidationError[] = [];

  if (doc.category === 'adr' && !doc.adr_status) {
    errors.push({
      rule_id: 'VR-ARC-004',
      field: 'adr_status',
      message: 'ADRs should specify adr_status',
    });
  }

  return errors;
}
