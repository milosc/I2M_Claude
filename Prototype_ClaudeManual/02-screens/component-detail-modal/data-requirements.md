# Data Requirements: Component Detail Modal (SCR-006)

---
**Screen**: SCR-006 - Component Detail Modal
**Created**: 2026-01-31
**Agent**: prototype-screen-specifier
**Session**: session-screen-scr006
---

## Overview

This document specifies all data requirements for the Component Detail Modal screen, including API endpoints, data structures, localStorage requirements, and data transformation logic.

---

## API Endpoints

### GET /api/skills/:id

**Purpose**: Fetch skill details by ID

**Request**:
```typescript
interface GetSkillRequest {
  id: string; // Skill ID from URL param
}
```

**Response**:
```typescript
interface GetSkillResponse {
  skill: Skill;
  related_skills: Skill[];
  used_by_commands: Command[];
  used_by_agents: Agent[];
}
```

**Error Codes**:
- `404` - Skill not found
- `500` - Server error

---

### GET /api/commands/:id

**Purpose**: Fetch command details by ID

**Request**:
```typescript
interface GetCommandRequest {
  id: string; // Command ID from URL param
}
```

**Response**:
```typescript
interface GetCommandResponse {
  command: Command;
  invoked_skills: Skill[];
  spawned_agents: Agent[];
}
```

**Error Codes**:
- `404` - Command not found
- `500` - Server error

---

### GET /api/agents/:id

**Purpose**: Fetch agent details by ID

**Request**:
```typescript
interface GetAgentRequest {
  id: string; // Agent ID from URL param
}
```

**Response**:
```typescript
interface GetAgentResponse {
  agent: Agent;
  loaded_skills: Skill[];
  spawned_by_commands: Command[];
}
```

**Error Codes**:
- `404` - Agent not found
- `500` - Server error

---

### GET /api/workflows/:id

**Purpose**: Fetch workflow details by ID

**Request**:
```typescript
interface GetWorkflowRequest {
  id: string; // Workflow ID from URL param
}
```

**Response**:
```typescript
interface GetWorkflowResponse {
  workflow: Workflow;
  related_workflows: Workflow[];
}
```

**Error Codes**:
- `404` - Workflow not found
- `500` - Server error

---

### GET /api/architecture-docs/:id

**Purpose**: Fetch architecture document details by ID

**Request**:
```typescript
interface GetArchitectureDocRequest {
  id: string; // ArchitectureDoc ID from URL param
}
```

**Response**:
```typescript
interface GetArchitectureDocResponse {
  architectureDoc: ArchitectureDoc;
  related_adrs: ArchitectureDoc[];
}
```

**Error Codes**:
- `404` - Architecture document not found
- `500` - Server error

---

### POST /api/preferences/favorites

**Purpose**: Add component to favorites

**Request**:
```typescript
interface AddFavoriteRequest {
  id: string;
  type: 'Skill' | 'Command' | 'Agent' | 'Rule' | 'Hook' | 'Workflow' | 'WaysOfWorking' | 'ArchitectureDoc';
}
```

**Response**:
```typescript
interface AddFavoriteResponse {
  success: boolean;
  favorites: string[];
}
```

---

### DELETE /api/preferences/favorites/:id

**Purpose**: Remove component from favorites

**Request**:
```typescript
interface RemoveFavoriteRequest {
  id: string; // Component ID to remove
}
```

**Response**:
```typescript
interface RemoveFavoriteResponse {
  success: boolean;
  favorites: string[];
}
```

---

## Data Structures

### Modal State

```typescript
interface ComponentDetailModalState {
  // Modal control
  isOpen: boolean;

  // Component identification
  componentId: string | null;
  componentType: 'Skill' | 'Command' | 'Agent' | 'Rule' | 'Hook' | 'Workflow' | 'WaysOfWorking' | 'ArchitectureDoc' | null;

  // Data
  componentData: Skill | Command | Agent | Rule | Hook | Workflow | WaysOfWorking | ArchitectureDoc | null;
  relatedData: {
    skills?: Skill[];
    commands?: Command[];
    agents?: Agent[];
    workflows?: Workflow[];
    adrs?: ArchitectureDoc[];
  };

  // UI state
  selectedTab: 'purpose' | 'examples' | 'options' | 'workflow' | 'traceability';
  loading: boolean;
  error: string | null;

  // User preferences
  isFavorited: boolean;
}
```

### Tab Content Mapping

```typescript
interface TabContentMap {
  purpose: {
    title: string;
    content: string; // Markdown content from content.purpose field
  };
  examples: {
    title: string;
    content: string; // Markdown content from content.example field
  };
  options: {
    title: string;
    content: string; // Markdown content from content.options field
  };
  workflow: {
    title: string;
    content: string; // Markdown content from content.workflow field (Mermaid diagram)
  };
  traceability: {
    title: string;
    content: string; // Generated from relationships
  };
}
```

---

## LocalStorage Requirements

### Favorites List

**Key**: `claudemanual:favorites`

**Data Structure**:
```typescript
interface FavoritesStorage {
  favorites: Array<{
    id: string;
    type: 'Skill' | 'Command' | 'Agent' | 'Rule' | 'Hook' | 'Workflow' | 'WaysOfWorking' | 'ArchitectureDoc';
    timestamp: number; // Unix timestamp when favorited
  }>;
}
```

**Operations**:
- **Add Favorite**: Append to array, deduplicate by id
- **Remove Favorite**: Filter out by id
- **Check Favorited**: Find by id

### Last Viewed Component

**Key**: `claudemanual:last_viewed`

**Data Structure**:
```typescript
interface LastViewedStorage {
  id: string;
  type: 'Skill' | 'Command' | 'Agent' | 'Rule' | 'Hook' | 'Workflow' | 'WaysOfWorking' | 'ArchitectureDoc';
  timestamp: number;
}
```

---

## Data Transformation Logic

### Tab Content Generation

```typescript
function generateTabContent(
  componentType: string,
  componentData: any
): TabContentMap {
  const baseContent = {
    purpose: {
      title: 'Purpose',
      content: componentData.content?.purpose || 'No purpose defined.'
    },
    examples: {
      title: 'Examples',
      content: componentData.content?.example || 'No examples available.'
    },
    options: {
      title: 'Options',
      content: componentData.content?.options || 'No options defined.'
    },
    workflow: {
      title: 'Workflow',
      content: componentData.content?.workflow || 'No workflow diagram available.'
    },
    traceability: {
      title: 'Traceability',
      content: generateTraceabilityContent(componentType, componentData)
    }
  };

  return baseContent;
}
```

### Traceability Content Generation

```typescript
function generateTraceabilityContent(
  componentType: string,
  componentData: any
): string {
  let markdown = `# Traceability\n\n`;
  markdown += `**Component ID**: ${componentData.id}\n`;
  markdown += `**Type**: ${componentType}\n`;
  markdown += `**Path**: \`${componentData.path}\`\n\n`;

  if (componentType === 'Skill') {
    markdown += `## Dependencies\n\n`;
    if (componentData.skills_required?.length > 0) {
      markdown += `**Required Skills**:\n`;
      componentData.skills_required.forEach((skillId: string) => {
        markdown += `- [${skillId}](#)\n`;
      });
    } else {
      markdown += `No skill dependencies.\n`;
    }

    markdown += `\n## Used By\n\n`;
    // Populated from relatedData.commands and relatedData.agents
  }

  if (componentType === 'Command') {
    markdown += `## Invokes Skills\n\n`;
    // Populated from relatedData.skills
    markdown += `\n## Spawns Agents\n\n`;
    // Populated from relatedData.agents
  }

  if (componentType === 'Agent') {
    markdown += `## Loads Skills\n\n`;
    // Populated from relatedData.skills
    markdown += `\n## Spawned By Commands\n\n`;
    // Populated from relatedData.commands
  }

  return markdown;
}
```

---

## Data Validation

### Client-Side Validation

```typescript
import { z } from 'zod';

const modalPropsSchema = z.object({
  componentId: z.string().min(1),
  componentType: z.enum(['Skill', 'Command', 'Agent', 'Rule', 'Hook', 'Workflow', 'WaysOfWorking', 'ArchitectureDoc']),
  isOpen: z.boolean(),
  onClose: z.function(),
});

type ModalProps = z.infer<typeof modalPropsSchema>;
```

### Server Response Validation

```typescript
const skillResponseSchema = z.object({
  skill: skillSchema,
  related_skills: z.array(skillSchema),
  used_by_commands: z.array(commandSchema),
  used_by_agents: z.array(agentSchema),
});

const commandResponseSchema = z.object({
  command: commandSchema,
  invoked_skills: z.array(skillSchema),
  spawned_agents: z.array(agentSchema),
});
```

---

## Caching Strategy

### React Query Configuration

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
    },
  },
});

// Usage in component
const { data, isLoading, error } = useQuery({
  queryKey: ['component', componentType, componentId],
  queryFn: () => fetchComponent(componentType, componentId),
  enabled: isOpen && !!componentId,
});
```

### Cache Invalidation

```typescript
// Invalidate cache when favorite is toggled
const mutation = useMutation({
  mutationFn: toggleFavorite,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['preferences'] });
  },
});
```

---

## Mock Data

### Sample Skill Data

```typescript
const mockSkillData: Skill = {
  id: 'Discovery_JTBD',
  name: 'Discovery JTBD Extractor',
  description: 'Extracts Jobs To Be Done from validated pain points and client facts.',
  stage: 'Discovery',
  path: '.claude/skills/Discovery_JTBD/SKILL.md',
  model: 'sonnet',
  content: {
    purpose: 'Generates structured JTBD document with functional, emotional, and social jobs following When/Want/So-that format.',
    usage: '```bash\n/discovery ClaudeManual Client_Materials/\n```',
    example: '```bash\n# Invoke via Discovery orchestrator\n/discovery ClaudeManual Client_Materials/\n```',
    workflow: '```mermaid\ngraph TD\n  A[Pain Points] --> B[JTBD Extraction]\n  B --> C[JOBS_TO_BE_DONE.md]\n```',
  },
};
```

---

## Performance Optimization

### Lazy Loading

```typescript
// Lazy load Mermaid renderer only when Workflow tab is selected
const MermaidRenderer = lazy(() => import('./MermaidRenderer'));

{selectedTab === 'workflow' && (
  <Suspense fallback={<SkeletonLoader />}>
    <MermaidRenderer content={workflowContent} />
  </Suspense>
)}
```

### Debounced Copy Action

```typescript
import { debounce } from 'lodash';

const debouncedCopyPath = debounce(() => {
  navigator.clipboard.writeText(componentData.path);
  showToast('Path copied to clipboard');
}, 300);
```

---

## Error Handling

### Error States

| Error Type | User-Facing Message | Recovery Action |
|------------|---------------------|-----------------|
| Network Error | "Unable to load component. Check your connection." | Retry button |
| 404 Not Found | "Component not found." | Close modal |
| 500 Server Error | "Something went wrong. Please try again." | Retry button |
| Parse Error | "Unable to render content. Showing raw markdown." | Display raw content |
| Clipboard Error | "Failed to copy to clipboard." | Show inline text field |

### Error Boundaries

```typescript
<ErrorBoundary
  fallback={<ErrorBanner message="Failed to load modal" />}
  onReset={() => setIsOpen(false)}
>
  <ComponentDetailModal {...props} />
</ErrorBoundary>
```

---

**Traceability**: SCR-006, JTBD-1.2, JTBD-2.1, PP-1.2, REQ-021, REQ-022, REQ-023
