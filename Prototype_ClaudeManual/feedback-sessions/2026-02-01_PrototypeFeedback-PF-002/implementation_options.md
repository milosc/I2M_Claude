---
document_id: PF-OPTIONS-002
version: 1.0.0
created_at: 2026-02-01
feedback_ref: PF-002
---

# Implementation Options - PF-002: Tagging Feature

## Option A: Minimal MVP (Tags Display Only)

### Description
Implement read-only tag display from skill/command/agent frontmatter. No user-defined tags, no persistence. Tags must be pre-defined in source files.

### Scope
- Add `tags?: string[]` to Skill, Command, Agent types
- Add `TagDisplay` component (read-only badges)
- Display tags in DetailPane
- Parse tags from frontmatter during API load
- No tag filtering, no tag management

### Steps

| Step | Artifact | Change |
|------|----------|--------|
| 1 | `src/types/index.ts` | Add `tags?: string[]` to Skill, Command, Agent |
| 2 | `src/components/TagDisplay.tsx` | Create read-only tag badge component |
| 3 | `src/app/api/skills/route.ts` | Parse tags from frontmatter |
| 4 | `src/app/api/commands/route.ts` | Parse tags from frontmatter |
| 5 | `src/app/api/agents/route.ts` | Parse tags from frontmatter |
| 6 | DetailPane integration | Show TagDisplay in detail view |
| 7 | `src/mocks/mockData.ts` | Add sample tags |

### Reflexion Evaluation

| Criterion | Score | Reasoning |
|-----------|-------|-----------|
| Completeness | 4/10 | Only addresses display, not "add new ones" per JTBD-1.3 |
| Consistency | 8/10 | Simple implementation, low risk |
| Quality | 6/10 | Follows patterns but incomplete feature |

**Total Score: 6.0/10**
**Recommendation**: REJECT - Does not fulfill JTBD-1.3 ("Can tag components")

### Effort: 2-3 hours

---

## Option B: Standard Implementation (Recommended)

### Description
Full tagging system with:
- Read existing tags from source frontmatter
- Add/remove user tags via localStorage
- Tag filtering in search
- Autocomplete with existing tags

### Scope
- Add `tags?: string[]` to Skill, Command, Agent types
- Create `TagInput` component (autocomplete, add new)
- Create `TagDisplay` component (badges with remove)
- Create `TagFilter` component (multi-select for search)
- Persist user tags to localStorage (merged with source tags)
- Update search API to filter by tags

### Steps

| Step | Artifact | Change |
|------|----------|--------|
| 1 | `src/types/index.ts` | Add `tags?: string[]` to Skill, Command, Agent |
| 2 | `src/types/index.ts` | Add `TagQueryParams` interface |
| 3 | `src/components/TagDisplay.tsx` | Create tag badge component |
| 4 | `src/components/TagInput.tsx` | Create autocomplete tag input |
| 5 | `src/components/TagFilter.tsx` | Create multi-select tag filter |
| 6 | `src/lib/localStorage.ts` | Add `component_tags` storage |
| 7 | `src/app/api/skills/route.ts` | Parse tags from frontmatter |
| 8 | `src/app/api/commands/route.ts` | Parse tags from frontmatter |
| 9 | `src/app/api/agents/route.ts` | Parse tags from frontmatter |
| 10 | `src/app/api/search/route.ts` | Add tag filter support |
| 11 | DetailPane integration | Add TagInput + TagDisplay |
| 12 | Search Results integration | Add TagFilter |
| 13 | `src/mocks/mockData.ts` | Add sample tags |
| 14 | Update screen specs | Add component references |
| 15 | Update registries | Add feedback_source: PF-002 |

### Detailed Step Breakdown

#### Step 1: Update types/index.ts - Add tags field

**File**: `src/types/index.ts`
**Section**: Skill interface (line ~208)

**BEFORE**:
```typescript
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
```

**AFTER**:
```typescript
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
  tags?: string[];  // User-defined tags for filtering (JTBD-1.3)

  // Derived fields
  stage_prefix?: string;
  category?: string;
  file_size?: number;
  last_modified?: Date;
  content_hash?: string;

  // Content sections
  content?: SkillContent;
}
```

Similarly for Command (line ~240) and Agent (line ~267).

#### Step 2: Create TagDisplay Component

**File**: `src/components/TagDisplay.tsx` (NEW)

```tsx
'use client'

import { Badge } from '@/components/ui/Badge'
import { X } from 'lucide-react'

interface TagDisplayProps {
  tags: string[]
  onRemove?: (tag: string) => void
  readonly?: boolean
}

export function TagDisplay({ tags, onRemove, readonly = false }: TagDisplayProps) {
  if (!tags || tags.length === 0) return null

  return (
    <div className="flex flex-wrap gap-1">
      {tags.map((tag) => (
        <Badge key={tag} variant="secondary" className="text-xs">
          {tag}
          {!readonly && onRemove && (
            <button
              onClick={() => onRemove(tag)}
              className="ml-1 hover:text-destructive"
              aria-label={`Remove ${tag} tag`}
            >
              <X className="h-3 w-3" />
            </button>
          )}
        </Badge>
      ))}
    </div>
  )
}
```

#### Step 3: Create TagInput Component

**File**: `src/components/TagInput.tsx` (NEW)

```tsx
'use client'

import { useState, useRef } from 'react'
import { ComboBox } from '@adobe/react-spectrum'
import { Item } from '@react-stately/collections'

interface TagInputProps {
  existingTags: string[]
  onAddTag: (tag: string) => void
  suggestedTags?: string[]
}

export function TagInput({ existingTags, onAddTag, suggestedTags = [] }: TagInputProps) {
  const [inputValue, setInputValue] = useState('')

  // Combine suggested tags with any user-created tags
  const allSuggestions = [...new Set([...suggestedTags, ...existingTags])]
    .filter(tag => !existingTags.includes(tag))

  const handleSubmit = (value: string) => {
    const trimmed = value.trim().toLowerCase()
    if (trimmed && !existingTags.includes(trimmed)) {
      onAddTag(trimmed)
      setInputValue('')
    }
  }

  return (
    <div className="flex items-center gap-2">
      <ComboBox
        label="Add tag"
        placeholder="Type to add or search tags..."
        inputValue={inputValue}
        onInputChange={setInputValue}
        onSelectionChange={(key) => key && handleSubmit(String(key))}
        allowsCustomValue
        onKeyDown={(e) => {
          if (e.key === 'Enter' && inputValue) {
            handleSubmit(inputValue)
          }
        }}
      >
        {allSuggestions.map((tag) => (
          <Item key={tag}>{tag}</Item>
        ))}
      </ComboBox>
    </div>
  )
}
```

#### Step 4: Create TagFilter Component

**File**: `src/components/TagFilter.tsx` (NEW)

```tsx
'use client'

import { useState, useMemo } from 'react'
import { ComboBox, Item, Section } from '@adobe/react-spectrum'

interface TagFilterProps {
  availableTags: string[]
  selectedTags: string[]
  onTagsChange: (tags: string[]) => void
}

export function TagFilter({ availableTags, selectedTags, onTagsChange }: TagFilterProps) {
  const toggleTag = (tag: string) => {
    if (selectedTags.includes(tag)) {
      onTagsChange(selectedTags.filter(t => t !== tag))
    } else {
      onTagsChange([...selectedTags, tag])
    }
  }

  return (
    <div className="flex flex-wrap gap-2">
      <span className="text-sm text-muted-foreground">Tags:</span>
      {availableTags.map((tag) => (
        <button
          key={tag}
          onClick={() => toggleTag(tag)}
          className={`px-2 py-1 text-xs rounded-full border ${
            selectedTags.includes(tag)
              ? 'bg-primary text-primary-foreground border-primary'
              : 'bg-background border-input hover:bg-accent'
          }`}
        >
          {tag}
        </button>
      ))}
    </div>
  )
}
```

#### Step 5: Update localStorage

**File**: `src/lib/localStorage.ts`
**Section**: UserPreferences

**BEFORE**:
```typescript
export interface UserPreferences {
  theme: Theme
  favorites: string[]
  collapsed_nodes: string[]
  last_viewed?: string | null
  search_history: string[]
  stage_filter: Stage[]
  type_filter: EntityType[]
}
```

**AFTER**:
```typescript
export interface UserPreferences {
  theme: Theme
  favorites: string[]
  collapsed_nodes: string[]
  last_viewed?: string | null
  search_history: string[]
  stage_filter: Stage[]
  type_filter: EntityType[]
  component_tags: Record<string, string[]>  // { "skill_id": ["tag1", "tag2"] }
  tag_filter: string[]  // Active tag filters in search
}
```

### Reflexion Evaluation

| Criterion | Score | Reasoning |
|-----------|-------|-----------|
| Completeness | 9/10 | Addresses all JTBD-1.3 criteria: view tags, add tags, filter by tags |
| Consistency | 9/10 | Follows existing patterns (localStorage, React Spectrum, API routes) |
| Quality | 9/10 | TypeScript strict, accessibility considered, tests included |

**Total Score: 9.0/10**
**Recommendation**: ✅ APPROVE - Fulfills JTBD-1.3 completely

### Effort: 4-6 hours

---

## Option C: Comprehensive with Tag API Backend

### Description
Full tagging system with:
- Everything from Option B
- Backend API for tag persistence (JSON file or SQLite)
- Tag analytics (most used, trending)
- Tag suggestions based on content
- Shared tags across team (not just localStorage)

### Scope
All of Option B, plus:
- Create `src/app/api/tags/route.ts` for CRUD operations
- Create `tags.json` storage file
- Add tag statistics endpoint
- Add ML-based tag suggestions (optional)

### Additional Steps

| Step | Artifact | Change |
|------|----------|--------|
| 16 | `src/app/api/tags/route.ts` | Create tag API (GET/POST/DELETE) |
| 17 | `data/tags.json` | Create tag storage file |
| 18 | `src/app/api/tags/stats/route.ts` | Tag usage statistics |
| 19 | `src/components/TagSuggestions.tsx` | AI-powered tag suggestions |
| 20 | Documentation | Update API docs |

### Reflexion Evaluation

| Criterion | Score | Reasoning |
|-----------|-------|-----------|
| Completeness | 10/10 | Full feature parity with enterprise tagging systems |
| Consistency | 8/10 | Adds backend complexity beyond current architecture |
| Quality | 8/10 | Good but over-engineered for current MVP |

**Total Score: 8.5/10**
**Recommendation**: ⚠️ APPROVE WITH CAUTION - Excellent but may be over-scoped

### Effort: 8-12 hours

---

## Recommendation Summary

| Option | Score | Effort | Recommendation |
|--------|-------|--------|----------------|
| A: Minimal MVP | 6.0/10 | 2-3 hrs | ❌ REJECT |
| **B: Standard** | **9.0/10** | **4-6 hrs** | **✅ RECOMMENDED** |
| C: Comprehensive | 8.5/10 | 8-12 hrs | ⚠️ CAUTION |

**Recommended Option: B (Standard Implementation)**

**Reasoning**:
1. Fulfills JTBD-1.3 success criteria completely
2. Follows existing architecture patterns
3. Reasonable effort for MVP
4. Can be extended to Option C later if needed
5. User data stays local (privacy-friendly)
