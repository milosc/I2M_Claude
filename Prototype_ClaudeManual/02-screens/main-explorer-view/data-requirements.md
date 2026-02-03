# Data Requirements: Main Explorer View (SCR-001)

**Screen**: Main Explorer View
**Screen ID**: SCR-001
**Created**: 2026-01-31
**Agent**: prototype-screen-specifier

---

## Data Flow Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     DATA FLOW DIAGRAM                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [API Endpoints]          [LocalStorage]          [SessionStorage]  │
│         │                      │                         │          │
│         │                      │                         │          │
│         ▼                      ▼                         ▼          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    React Component State                     │  │
│  │  - items: Skill[] | Command[] | Agent[] | Rule[] | Hook[]   │  │
│  │  - selectedItem: Item | null                                 │  │
│  │  - expandedNodes: string[]                                   │  │
│  │  - selectedStages: string[]                                  │  │
│  │  - isLoading: boolean                                        │  │
│  │  - error: string | null                                      │  │
│  └──────────────────────────────────────────────────────────────┘  │
│         │                                                            │
│         ▼                                                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  Child Components                            │  │
│  │  - NavigationTree (items, expandedNodes, selectedStages)     │  │
│  │  - DetailPane (selectedItem)                                 │  │
│  │  - StageFilterDropdown (selectedStages)                      │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## API Data Sources

### Endpoint: GET /api/skills

**Purpose**: Load all framework skills with metadata

**Request**:
```http
GET /api/skills?include=content&fields=id,name,description,stage,path,model
```

**Response Schema**:
```typescript
interface SkillListResponse {
  data: Skill[];
  pagination: {
    page: number;
    pageSize: number;
    totalItems: number;
    totalPages: number;
  };
}
```

**Response Example**:
```json
{
  "data": [
    {
      "id": "Discovery_JTBD",
      "name": "Discovery_JTBD",
      "description": "Extracts Jobs To Be Done from pain points",
      "stage": "Discovery",
      "path": ".claude/skills/Discovery_JTBD/SKILL.md",
      "model": "sonnet",
      "content": {
        "purpose": "Extracts Jobs To Be Done...",
        "usage": "Invoke via /discovery command...",
        "example": "```bash\n/discovery...\n```"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 100,
    "totalItems": 85,
    "totalPages": 1
  }
}
```

**Error Handling**:
- 500 Internal Server Error → Show ErrorBanner with Retry button
- Network timeout (>5s) → Show offline indicator, cache last successful response
- Partial response (missing fields) → Fill with defaults, log warning

**Caching Strategy**:
- Cache in sessionStorage for 5 minutes
- Invalidate on user-triggered refresh
- Revalidate on window focus if cache older than 5 min

---

### Endpoint: GET /api/commands

**Purpose**: Load all slash commands

**Request**:
```http
GET /api/commands
```

**Response Schema**:
```typescript
interface CommandListResponse {
  data: Command[];
  pagination: {
    page: number;
    pageSize: number;
    totalItems: number;
    totalPages: number;
  };
}
```

**Response Example**:
```json
{
  "data": [
    {
      "id": "discovery",
      "name": "/discovery",
      "description": "Complete end-to-end discovery analysis",
      "stage": "Discovery",
      "path": ".claude/commands/discovery.md"
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 50,
    "totalItems": 30,
    "totalPages": 1
  }
}
```

**Error Handling**: Same as /api/skills

---

### Endpoint: GET /api/agents

**Purpose**: Load all agent definitions

**Request**:
```http
GET /api/agents
```

**Response Schema**:
```typescript
interface AgentListResponse {
  data: Agent[];
  pagination: {
    page: number;
    pageSize: number;
    totalItems: number;
    totalPages: number;
  };
}
```

**Response Example**:
```json
{
  "data": [
    {
      "id": "discovery-domain-researcher",
      "name": "Domain Researcher",
      "description": "Researches domain terminology and patterns",
      "model": "sonnet",
      "stage": "Discovery",
      "path": ".claude/agents/discovery/domain-researcher.md",
      "color": "blue"
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 50,
    "totalItems": 25,
    "totalPages": 1
  }
}
```

**Error Handling**: Same as /api/skills

---

### Endpoint: GET /api/rules

**Purpose**: Load all framework rules

**Request**:
```http
GET /api/rules
```

**Response Schema**:
```typescript
interface RuleListResponse {
  data: Rule[];
  pagination: {
    page: number;
    pageSize: number;
    totalItems: number;
    totalPages: number;
  };
}
```

**Response Example**:
```json
{
  "data": [
    {
      "id": "CORE_RULES",
      "name": "CORE_RULES",
      "description": "Core framework rules always loaded",
      "path": ".claude/rules/CORE_RULES.md",
      "category": "core"
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 5,
    "totalPages": 1
  }
}
```

**Error Handling**: Same as /api/skills

---

### Endpoint: GET /api/hooks

**Purpose**: Load all lifecycle hooks

**Request**:
```http
GET /api/hooks
```

**Response Schema**:
```typescript
interface HookListResponse {
  data: Hook[];
  pagination: {
    page: number;
    pageSize: number;
    totalItems: number;
    totalPages: number;
  };
}
```

**Response Example**:
```json
{
  "data": [
    {
      "id": "command_start",
      "name": "command_start.py",
      "description": "Logs command start event",
      "path": ".claude/hooks/command_start.py",
      "type": "PreToolUse",
      "language": "python"
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 8,
    "totalPages": 1
  }
}
```

**Error Handling**: Same as /api/skills

---

## LocalStorage Data

### Key: userPreferences

**Schema**:
```typescript
interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  favorites: string[];
  collapsed_nodes: string[];
  last_viewed: string | null;
  search_history: string[];
  stage_filter: string[];
  type_filter: ('Skill' | 'Command' | 'Agent' | 'Rule' | 'Hook')[];
}
```

**Example**:
```json
{
  "theme": "dark",
  "favorites": ["Discovery_JTBD", "discovery-multiagent", "quality-security-auditor"],
  "collapsed_nodes": ["Skills", "Commands.Discovery"],
  "last_viewed": "Discovery_JTBD",
  "search_history": ["persona", "TDD", "GDPR"],
  "stage_filter": ["Discovery", "Prototype"],
  "type_filter": ["Skill", "Command"]
}
```

**Read Operations**:
- On page load: Parse JSON, apply defaults if missing
- On theme toggle: Read current value, toggle, write back
- On favorites add/remove: Read array, mutate, write back
- On tree expand/collapse: Read collapsed_nodes, update, write back

**Write Operations**:
- On every state change: JSON.stringify + localStorage.setItem
- On quota exceeded: Degrade gracefully, clear search_history first

**Default Values** (if localStorage empty):
```json
{
  "theme": "system",
  "favorites": [],
  "collapsed_nodes": [],
  "last_viewed": null,
  "search_history": [],
  "stage_filter": [],
  "type_filter": []
}
```

---

## SessionStorage Data

### Key: api_cache

**Purpose**: Cache API responses for 5 minutes to reduce server load

**Schema**:
```typescript
interface APICache {
  skills: {
    data: Skill[];
    timestamp: number; // Unix timestamp
  };
  commands: {
    data: Command[];
    timestamp: number;
  };
  agents: {
    data: Agent[];
    timestamp: number;
  };
  rules: {
    data: Rule[];
    timestamp: number;
  };
  hooks: {
    data: Hook[];
    timestamp: number;
  };
}
```

**Cache Invalidation**:
- Timestamp older than 5 minutes → Re-fetch from API
- User clicks "Refresh" button → Clear cache, re-fetch
- Window focus after 5+ minutes → Revalidate cache

**Cache Miss Behavior**:
- If sessionStorage empty, fetch from API
- If timestamp invalid, fetch from API
- If data malformed, log error, fetch from API

---

## Data Transformations

### Filtering by Stage

**Input**: `items: (Skill | Command | Agent | Rule | Hook)[]`, `selectedStages: string[]`

**Output**: Filtered array

**Logic**:
```typescript
const filteredItems = selectedStages.length === 0
  ? items
  : items.filter(item => selectedStages.includes(item.stage));
```

**Performance**: O(n) where n = total items (115+). Use useMemo to avoid recalculating on every render.

---

### Tree Hierarchy Construction

**Input**: `items: Item[]`

**Output**: Hierarchical tree structure

**Logic**:
```typescript
interface TreeNode {
  id: string;
  label: string;
  children?: TreeNode[];
  item?: Item;
  count: number;
}

const buildTree = (items: Item[]): TreeNode[] => {
  const categories = {
    Skills: items.filter(i => i.type === 'Skill'),
    Commands: items.filter(i => i.type === 'Command'),
    Agents: items.filter(i => i.type === 'Agent'),
    Rules: items.filter(i => i.type === 'Rule'),
    Hooks: items.filter(i => i.type === 'Hook'),
  };

  return Object.entries(categories).map(([label, categoryItems]) => ({
    id: label.toLowerCase(),
    label: `${label} (${categoryItems.length})`,
    count: categoryItems.length,
    children: groupByStage(categoryItems), // Group Skills/Commands/Agents by stage
  }));
};
```

**Performance**: O(n log n) for sorting by stage. Cache result in useMemo.

---

### Count Badges Calculation

**Input**: `items: Item[]`, `selectedStages: string[]`

**Output**: Count per category

**Logic**:
```typescript
const getCounts = (items: Item[], selectedStages: string[]) => {
  const filtered = selectedStages.length === 0
    ? items
    : items.filter(i => selectedStages.includes(i.stage));

  return {
    skills: filtered.filter(i => i.type === 'Skill').length,
    commands: filtered.filter(i => i.type === 'Command').length,
    agents: filtered.filter(i => i.type === 'Agent').length,
    rules: filtered.filter(i => i.type === 'Rule').length,
    hooks: filtered.filter(i => i.type === 'Hook').length,
  };
};
```

**Performance**: O(n). Update only when selectedStages changes.

---

## Data Validation

### Client-Side Validation (Zod)

```typescript
import { z } from 'zod';

const skillSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(2).max(100),
  description: z.string().min(10).max(500),
  stage: z.enum(['Discovery', 'Prototype', 'ProductSpecs', 'SolArch', 'Implementation', 'Utility', 'GRC', 'Security']),
  path: z.string().regex(/^\.claude\/skills\/.+\/SKILL\.md$/),
});

const validateSkills = (data: unknown): Skill[] => {
  const parsed = z.array(skillSchema).safeParse(data);
  if (!parsed.success) {
    console.error('Skill validation failed:', parsed.error);
    return [];
  }
  return parsed.data;
};
```

**Validation Points**:
- After API response: Validate all fields match schema
- Before rendering: Ensure required fields exist
- Before localStorage write: Validate user preferences schema

---

## Data Synchronization

### Favorites Sync

**Trigger**: User clicks "Add to Favorites" or "Remove from Favorites"

**Flow**:
1. Read `userPreferences.favorites` from localStorage
2. Add/remove item.id from array
3. Write updated array to localStorage
4. Update React state immediately (optimistic update)
5. Re-render NavigationTree to show/hide ⭐ icon

**Conflict Resolution**: LocalStorage is single-threaded, no conflicts possible.

---

### Stage Filter Sync

**Trigger**: User selects/deselects stages in StageFilterDropdown

**Flow**:
1. Update `selectedStages` in React state
2. Write to `userPreferences.stage_filter` in localStorage
3. Recalculate filtered items (useMemo dependency)
4. Update tree count badges
5. Re-render NavigationTree with filtered items

**Debounce**: 300ms debounce on filter changes to avoid excessive re-renders.

---

## Performance Optimizations

### Data Loading

| Optimization | Implementation | Benefit |
|--------------|----------------|---------|
| **Parallel Fetches** | `Promise.all([fetchSkills(), fetchCommands(), ...])` | Reduce total load time from 2s to <1s |
| **Progressive Loading** | Load tree structure first, detail content on-demand | Faster initial render |
| **Lazy Content** | Only fetch markdown content when item selected | Reduce initial payload size |
| **Response Compression** | Enable gzip/brotli on server | Reduce network transfer time |

### Data Caching

| Cache Layer | Duration | Invalidation Trigger |
|-------------|----------|---------------------|
| SessionStorage | 5 minutes | User refresh, window focus after 5 min |
| React Query | Stale after 5 min | Background refetch on window focus |
| Browser HTTP Cache | 1 hour | Cache-Control headers |

### Rendering Optimizations

| Technique | Implementation | Benefit |
|-----------|----------------|---------|
| **Memoization** | `useMemo` for filtered items, tree hierarchy | Avoid recalculating on every render |
| **Virtualization** | `react-window` for tree with 115+ items | Render only visible items |
| **Code Splitting** | Lazy load DetailPane tabs | Reduce initial bundle size |
| **Debouncing** | Debounce stage filter changes 300ms | Reduce re-render frequency |

---

## Error Scenarios & Recovery

| Scenario | Detection | User Feedback | Recovery Action |
|----------|-----------|---------------|-----------------|
| **Network Failure** | API fetch throws NetworkError | ErrorBanner: "Connection lost. Retrying..." | Auto-retry with exponential backoff |
| **API 500 Error** | Response status 500 | ErrorBanner: "Server error. Retry?" | [Retry] button re-fetches |
| **Malformed Response** | Zod validation fails | Warning: "Some items failed to load." | Filter out invalid items, show valid ones |
| **localStorage Quota** | QuotaExceededError thrown | Warning: "Preferences not saved." | Clear search_history, retry |
| **Missing Content** | item.content is null | "Content unavailable" in DetailPane | Show [Copy Path] button as fallback |

---

## Traceability

### Data Fields → Requirements

| Data Field | Requirement | Entity | Validation |
|------------|-------------|--------|------------|
| `items[]` | REQ-021 (Browse components) | Skill, Command, Agent, Rule, Hook | Zod schema |
| `selectedStages` | REQ-022 (Stage filtering) | UserPreferences.stage_filter | Enum validation |
| `favorites` | REQ-024 (Favorites) | UserPreferences.favorites | Array of valid IDs |
| `selectedItem.path` | REQ-023 (File path access) | Skill.path, Command.path, etc. | Regex validation |

### API Endpoints → Data Model

| Endpoint | Entity | Fields Used |
|----------|--------|-------------|
| GET /api/skills | Skill (ENT-001) | id, name, description, stage, path, model, content |
| GET /api/commands | Command (ENT-002) | id, name, description, stage, path |
| GET /api/agents | Agent (ENT-003) | id, name, description, model, stage, path, color |
| GET /api/rules | Rule (ENT-004) | id, name, description, path, category |
| GET /api/hooks | Hook (ENT-005) | id, name, description, path, type, language |

---

**Summary**: Main Explorer View loads 115+ items from 5 API endpoints, caches responses in sessionStorage for 5 minutes, persists user preferences (theme, favorites, filters) to localStorage, and applies client-side validation using Zod schemas. Data transformations include stage filtering, tree hierarchy construction, and count badge calculation. Performance optimizations include parallel fetches, response caching, and virtualized rendering.

**Created**: 2026-01-31
**Agent**: prototype-screen-specifier
**Traceability**: ENT-001 to ENT-006, REQ-021 to REQ-026
