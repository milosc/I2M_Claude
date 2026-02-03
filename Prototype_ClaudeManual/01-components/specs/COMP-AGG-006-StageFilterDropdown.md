# StageFilterDropdown

**ID**: COMP-AGG-006
**Category**: Filters
**Priority**: P1

## Overview

Multi-select dropdown for filtering framework components by stage (Discovery, Prototype, Implementation, etc.). Combines Adobe Spectrum's Select with ClaudeManual-specific stage filtering logic.

## Props Interface

```typescript
interface StageFilterDropdownProps {
  /** Selected stages */
  selectedStages: Stage[];
  /** Change handler */
  onChange: (stages: Stage[]) => void;
  /** Show badge count */
  showCount?: boolean;
}

type Stage = 'discovery' | 'prototype' | 'productspecs' | 'solarch' | 'implementation' | 'utility' | 'security' | 'grc';
```

## Library Components Used

- **Select** (Spectrum): Multi-select dropdown
- **Badge** (Spectrum): Stage-specific colors
- **Text** (Spectrum): Stage labels

## Usage Examples

```tsx
<StageFilterDropdown
  selectedStages={['discovery', 'prototype']}
  onChange={(stages) => setStageFilter(stages)}
  showCount={true}
/>
```

## Screen Usage

| Screen | Context |
|--------|---------|
| SCR-001 Main Explorer | Header stage filter |
| SCR-003 Stage-Filtered View | Active stage filter |

---

**Traceability**: PP-1.4 (Organizational Chaos), JTBD-1.4 (Stage-appropriate tools), CF-011 (Stage-based organization)
