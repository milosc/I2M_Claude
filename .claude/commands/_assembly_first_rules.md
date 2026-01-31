# Assembly-First Enforcement Rules (Embedded)

**Core Principle**: *Compose, Don't Generate* - Use library components, focus on glue code.

## 🔴 FORBIDDEN Practices (BLOCKING)

### ❌ No Raw HTML Elements
**NEVER use**: `<button>`, `<input>`, `<select>`, `<textarea>`, `<a>` (for navigation)
**USE**: Library components - `Button`, `TextField`, `Select`, `TextArea`, `Link`
**Exception**: `<div>`, `<span>`, `<section>` for LAYOUT ONLY

### ❌ No Manual ARIA Attributes
**DO NOT add**: `role`, `aria-label`, `aria-pressed`, `tabIndex` manually
**Components handle this automatically**
**Exception**: Icon-only buttons need `aria-label`

### ❌ No Custom CSS for Component Internals
**DO NOT**: Custom hover/focus/active styles with arbitrary classes
**USE**: Render props pattern with state-driven styling

### ❌ No Reimplementing Component Logic
**DO NOT**: Manual state for open/closed, selected, disabled
**USE**: Built-in component state management

---

## ✅ REQUIRED Practices

### ✅ Read Component Manifest FIRST (BLOCKING)
```
READ .claude/templates/component-library/manifests/components.json
READ .claude/templates/component-library/SKILL.md
READ .claude/templates/component-library/INTERACTIONS.md
```

### ✅ Import from Library Only
```tsx
import { Button, TextField, Form } from '@/component-library';
import { useAsyncList } from 'react-stately';
```

### ✅ Use Render Props for State
```tsx
<Button
  className={({ isPressed, isHovered, isPending }) =>
    `px-4 py-2 ${isPressed ? 'bg-accent-active' : 'bg-accent-default'}`
  }
>
```
**States**: `isHovered`, `isPressed`, `isFocused`, `isFocusVisible`, `isDisabled`, `isPending`, `isSelected`

### ✅ Use Design Tokens Only
```tsx
// ✅ CORRECT
<div className="bg-surface-1 text-text-primary border-border-default">

// ❌ WRONG
<div className="bg-gray-100 text-gray-900 border-gray-300">
```
**Tokens**: `canvas`, `surface-1`, `surface-2`, `text-primary`, `accent-default`, `border-default`

### ✅ Focus on Glue Code
Your job: **Data fetching + business logic**, NOT UI implementation
```tsx
// ✅ CORRECT - Data integration focus
const { data, isLoading, error } = useQuery('/api/users');
return (
  <ListBox items={data} aria-label="Users">
    {(user) => <Item key={user.id}>{user.name}</Item>}
  </ListBox>
);
```

---

## Component Mapping Quick Reference

| Requirement | Library Component |
|-------------|------------------|
| Text/password input | `TextField` |
| Dropdown/select | `Select`, `ComboBox` |
| Search with autocomplete | `Autocomplete` |
| Checkbox/toggle | `Checkbox`, `Switch` |
| Radio buttons | `RadioGroup` |
| Number input | `NumberField` |
| Date/time picker | `DatePicker`, `TimeField` |
| Data table | `Table` |
| List view | `ListBox`, `GridList` |
| Menu/dropdown | `Menu` |
| Button | `Button` |
| File upload | `FileTrigger` |
| Tabs | `Tabs` |
| Breadcrumbs | `Breadcrumbs` |
| Modal dialog | `Dialog`, `Modal` |
| Tooltip | `Tooltip` |
| Loading | `ProgressBar` |
| Status badge | `Badge` |

---

## Aggregate Component Rules

**Only create custom components when**:
1. Combining 2+ library components with business logic
2. Repeated pattern across multiple screens
3. No single library component matches

**Valid Aggregates**:
- `KPICard` - Combines `Meter`, `Heading`, `Text`, `Badge` + calculation logic
- `UserProfileCard` - Combines `Avatar`, `Heading`, `Text`, `Badge`
- `TaskListItem` - Combines `Checkbox`, `Text`, `Button`, `Menu`

**Invalid** (use library instead):
- ❌ `CustomButton` - Use `Button`
- ❌ `SearchInput` - Use `SearchField`
- ❌ `DataGrid` - Use `Table`

---

## Validation Checklist

**Before code generation**:
- [ ] Component manifest read
- [ ] All requirements mapped to library components
- [ ] Aggregates identified and justified

**After code generation**:
- [ ] No raw HTML elements (`<button>`, `<input>`, etc.)
- [ ] All imports from `@/component-library`
- [ ] No manual ARIA (except icon-only buttons)
- [ ] Tailwind theme tokens used
- [ ] Render props for state-driven styling

---

**Full Documentation**: `.claude/templates/component-library/SKILL.md`
