---
document_id: PF-OPTIONS-001
version: 1.0.0
created_at: 2026-02-01
feedback_ref: PF-001
---

# Implementation Options - PF-001

## Feedback Summary

Display actual markdown content (name, frontmatter attributes, body content) when selecting skills, commands, or agents in the DetailPane.

---

## Option A: Minimal (Data Structure Only)

**Approach**: Add `frontmatter` and `rawContent` fields to the data interface and test data files only. Display frontmatter as key-value pairs in the header.

### Steps

**Step 1: Update ComponentDetail Interface**

File: `Prototype_ClaudeManual/04-implementation/src/components/DetailPane/index.tsx`
Lines: 33-46

BEFORE:
```typescript
export interface ComponentDetail {
  id: string;
  name: string;
  type: 'skill' | 'command' | 'agent' | 'rule' | 'hook';
  stage: Stage;
  path: string;
  description: string;
  purpose?: string;
  examples?: CodeExample[];
  options?: OptionField[];
  workflow?: WorkflowDiagram;
  traceability?: TraceabilityLink[];
  isFavorite: boolean;
}
```

AFTER:
```typescript
export interface FrontmatterAttributes {
  model?: string;
  context?: string | null;
  agent?: string | null;
  allowed_tools?: string[];
  skills_required?: string[];
  checkpoint?: number | null;
  loads_skills?: string[];
  spawned_by?: string[];
  orchestrates_agents?: string[];
  invokes_skills?: string[];
  argument_hint?: string;
  [key: string]: unknown;
}

export interface ComponentDetail {
  id: string;
  name: string;
  type: 'skill' | 'command' | 'agent' | 'rule' | 'hook';
  stage: Stage;
  path: string;
  description: string;
  frontmatter?: FrontmatterAttributes;
  rawContent?: string;
  purpose?: string;
  examples?: CodeExample[];
  options?: OptionField[];
  workflow?: WorkflowDiagram;
  traceability?: TraceabilityLink[];
  isFavorite: boolean;
}
```

**Step 2: Add Frontmatter Display in Header**

File: `Prototype_ClaudeManual/04-implementation/src/components/DetailPane/index.tsx`
Lines: 162-169 (after metadata badges)

BEFORE:
```typescript
        {/* File Path */}
        <p className="text-xs text-gray-500 font-mono">{item.path}</p>
```

AFTER:
```typescript
        {/* File Path */}
        <p className="text-xs text-gray-500 font-mono">{item.path}</p>

        {/* Frontmatter Attributes */}
        {item.frontmatter && (
          <div className="mt-3 flex flex-wrap gap-2">
            {Object.entries(item.frontmatter).map(([key, value]) => {
              if (value === null || value === undefined) return null;
              const displayValue = Array.isArray(value) ? value.join(', ') : String(value);
              return (
                <span key={key} className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">
                  <span className="font-medium">{key}:</span> {displayValue}
                </span>
              );
            })}
          </div>
        )}
```

**Step 3: Update Purpose Tab to Use rawContent**

File: `Prototype_ClaudeManual/04-implementation/src/components/DetailPane/index.tsx`
Lines: 195-197

BEFORE:
```typescript
        {activeTab === 'purpose' && item.purpose && (
          <MarkdownRenderer content={item.purpose} />
        )}
```

AFTER:
```typescript
        {activeTab === 'purpose' && (
          <MarkdownRenderer content={item.rawContent || item.purpose || 'No content available'} />
        )}
```

**Step 4: Update skills.json Test Data**

File: `Prototype_ClaudeManual/00-foundation/test-data/skills.json`

Add to each skill object:
```json
{
  "frontmatter": {
    "name": "Discovery_JTBD",
    "model": "sonnet",
    "context": null,
    "agent": null,
    "allowed_tools": ["Read", "Write", "Grep"],
    "skills_required": []
  },
  "rawContent": "# Discovery_JTBD\n\n## Purpose\n\nTransform validated pain points into actionable Jobs To Be Done using When/Want/So-that framework.\n\n## When to Use\n\n- **Workflow Stage**: Discovery (Checkpoint 4)\n- **Prerequisites**: Pain points extracted (CP-2), client facts validated\n- **Outputs**: JOBS_TO_BE_DONE.md, jtbd_registry.json\n\n## Example Usage\n\n```bash\n/discovery ClaudeManual Client_Materials/\n```\n\n## Workflow\n\nRead pain points → Map to user types → Generate functional/emotional/social jobs → Validate coverage"
}
```

**Step 5: Update commands.json Test Data**

File: `Prototype_ClaudeManual/00-foundation/test-data/commands.json`

Add to each command object similar frontmatter and rawContent fields.

**Step 6: Update agents.json Test Data**

File: `Prototype_ClaudeManual/00-foundation/test-data/agents.json`

Add to each agent object similar frontmatter and rawContent fields.

### Reflexion Evaluation

| Criterion | Score | Notes |
|-----------|-------|-------|
| Completeness | 7/10 | Addresses core requirement but minimal UI enhancement |
| Consistency | 9/10 | Backward compatible, maintains existing structure |
| Quality | 6/10 | Basic implementation, no special formatting |

**Risk Assessment**:
- Build risk: LOW (additive changes)
- Visual regression risk: LOW (minor UI addition)
- Traceability risk: LOW (no chain changes)

**Effort Estimate**: 30 minutes

**SCORE**: 7.3/10

**RECOMMENDATION**: APPROVE WITH CAUTION - Functional but basic

---

## Option B: Standard (Recommended)

**Approach**: Full implementation with dedicated Frontmatter component, improved Purpose tab with section detection, and comprehensive test data.

### Steps

**Step 1-3**: Same as Option A

**Step 4: Create FrontmatterDisplay Component**

File: `Prototype_ClaudeManual/04-implementation/src/components/FrontmatterDisplay/index.tsx`
(NEW FILE)

```typescript
import React from 'react';
import type { FrontmatterAttributes } from '../DetailPane';

interface FrontmatterDisplayProps {
  frontmatter: FrontmatterAttributes;
  type: 'skill' | 'command' | 'agent' | 'rule' | 'hook';
}

const DISPLAY_ORDER: Record<string, string[]> = {
  skill: ['model', 'context', 'agent', 'allowed_tools', 'skills_required'],
  command: ['model', 'argument_hint', 'allowed_tools', 'invokes_skills', 'orchestrates_agents'],
  agent: ['model', 'checkpoint', 'loads_skills', 'spawned_by'],
  rule: ['model'],
  hook: ['model'],
};

export const FrontmatterDisplay: React.FC<FrontmatterDisplayProps> = ({ frontmatter, type }) => {
  const order = DISPLAY_ORDER[type] || Object.keys(frontmatter);

  const renderValue = (value: unknown): React.ReactNode => {
    if (value === null || value === undefined) return <span className="text-gray-400">null</span>;
    if (Array.isArray(value)) {
      if (value.length === 0) return <span className="text-gray-400">[]</span>;
      return (
        <div className="flex flex-wrap gap-1">
          {value.map((v, i) => (
            <span key={i} className="px-1.5 py-0.5 bg-blue-50 text-blue-700 text-xs rounded">
              {String(v)}
            </span>
          ))}
        </div>
      );
    }
    return <span>{String(value)}</span>;
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4 mt-3 bg-gray-50">
      <h3 className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wide">
        Frontmatter
      </h3>
      <dl className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
        {order.map((key) => {
          const value = frontmatter[key];
          return (
            <div key={key} className="flex flex-col">
              <dt className="text-gray-500 font-medium">{key}</dt>
              <dd className="text-gray-900">{renderValue(value)}</dd>
            </div>
          );
        })}
      </dl>
    </div>
  );
};

export default FrontmatterDisplay;
```

**Step 5: Update DetailPane Header**

File: `Prototype_ClaudeManual/04-implementation/src/components/DetailPane/index.tsx`

BEFORE (lines 162-169):
```typescript
        {/* File Path */}
        <p className="text-xs text-gray-500 font-mono">{item.path}</p>
```

AFTER:
```typescript
        {/* File Path */}
        <p className="text-xs text-gray-500 font-mono">{item.path}</p>

        {/* Frontmatter Attributes */}
        {item.frontmatter && (
          <FrontmatterDisplay frontmatter={item.frontmatter} type={item.type} />
        )}
```

**Step 6: Add Import for FrontmatterDisplay**

File: `Prototype_ClaudeManual/04-implementation/src/components/DetailPane/index.tsx`
Line: 2

ADD:
```typescript
import { FrontmatterDisplay } from '../FrontmatterDisplay';
```

**Step 7-9**: Same as Option A steps 4-6 (test data updates)

**Step 10: Create FrontmatterDisplay Tests**

File: `Prototype_ClaudeManual/04-implementation/src/__tests__/components/FrontmatterDisplay.test.tsx`
(NEW FILE)

```typescript
import { render, screen } from '@testing-library/react';
import { FrontmatterDisplay } from '../../components/FrontmatterDisplay';

describe('FrontmatterDisplay', () => {
  it('renders frontmatter attributes for skill type', () => {
    const frontmatter = {
      model: 'sonnet',
      context: null,
      allowed_tools: ['Read', 'Write'],
    };
    render(<FrontmatterDisplay frontmatter={frontmatter} type="skill" />);

    expect(screen.getByText('Frontmatter')).toBeInTheDocument();
    expect(screen.getByText('model')).toBeInTheDocument();
    expect(screen.getByText('sonnet')).toBeInTheDocument();
    expect(screen.getByText('Read')).toBeInTheDocument();
    expect(screen.getByText('Write')).toBeInTheDocument();
  });

  it('renders empty array as []', () => {
    const frontmatter = { skills_required: [] };
    render(<FrontmatterDisplay frontmatter={frontmatter} type="skill" />);

    expect(screen.getByText('[]')).toBeInTheDocument();
  });

  it('renders null as null text', () => {
    const frontmatter = { context: null };
    render(<FrontmatterDisplay frontmatter={frontmatter} type="skill" />);

    expect(screen.getByText('null')).toBeInTheDocument();
  });
});
```

### Reflexion Evaluation

| Criterion | Score | Notes |
|-----------|-------|-------|
| Completeness | 9/10 | Full implementation with dedicated component |
| Consistency | 9/10 | Follows existing component patterns |
| Quality | 8/10 | Well-structured, tested, extensible |

**Risk Assessment**:
- Build risk: LOW (new file + interface changes)
- Visual regression risk: LOW (isolated new component)
- Traceability risk: LOW (no chain changes)

**Effort Estimate**: 45 minutes

**SCORE**: 8.7/10

**RECOMMENDATION**: APPROVE - Recommended approach

---

## Option C: Comprehensive (Extended)

**Approach**: Full implementation plus section navigation within markdown content, collapsible frontmatter panel, and enhanced styling.

### Additional Steps (on top of Option B)

**Step 11: Add Section Navigation**

Parse rawContent to extract markdown headers and create a mini-table-of-contents for navigation within the Purpose tab.

**Step 12: Collapsible Frontmatter Panel**

Make the frontmatter section collapsible with an expand/collapse button to reduce visual noise.

**Step 13: Syntax Highlighting for Frontmatter**

Add YAML syntax highlighting for the frontmatter display using a code block view.

**Step 14: Responsive Layout**

Add responsive grid for frontmatter display on mobile devices.

### Reflexion Evaluation

| Criterion | Score | Notes |
|-----------|-------|-------|
| Completeness | 10/10 | Exceeds requirements with navigation features |
| Consistency | 8/10 | Additional complexity in component structure |
| Quality | 9/10 | Premium UX but may be over-engineering |

**Risk Assessment**:
- Build risk: MEDIUM (more code to maintain)
- Visual regression risk: MEDIUM (more UI changes)
- Traceability risk: LOW (no chain changes)

**Effort Estimate**: 75 minutes

**SCORE**: 9.0/10

**RECOMMENDATION**: APPROVE - For high-quality requirement

---

## Summary

| Option | Steps | Artifacts | Effort | Score | Recommendation |
|--------|-------|-----------|--------|-------|----------------|
| A: Minimal | 6 | 4 modified | 30 min | 7.3/10 | APPROVE WITH CAUTION |
| B: Standard | 10 | 4 modified + 2 new | 45 min | 8.7/10 | **APPROVE (Recommended)** |
| C: Comprehensive | 14 | 4 modified + 4 new | 75 min | 9.0/10 | APPROVE |

---

**Highest Score**: Option C (9.0/10)
**Recommended Option**: Option B (8.7/10) - Best balance of quality and effort
