# Assembly-First Prototype Architecture

## Overview

The Assembly-First approach transforms prototype generation from **code generation** to **component orchestration**. Instead of generating raw HTML, CSS, and accessibility attributes, Claude acts as a Senior UI Engineer who composes pre-built, accessible components from a production-ready library.

**Key Principle:** *"Compose, Don't Generate"*

---

## Architecture Components

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      DISCOVERY OUTPUTS (Stage 1)                        │
│  Personas, JTBD, Screen Definitions, Data Fields, Interaction Patterns  │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                   COMPONENT LIBRARY (.claude/templates/)                 │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐            │
│  │ 62 Components  │  │ Accessibility  │  │ Design Tokens  │            │
│  │ React Aria     │  │ WAI-ARIA Built │  │ Tailwind Theme │            │
│  └────────────────┘  └────────────────┘  └────────────────┘            │
│                                                                          │
│  manifests/components.json → Component Registry                         │
│  SKILL.md → LLM Usage Protocol                                          │
│  INTERACTIONS.md → State Patterns                                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                  PROTOTYPE GENERATION (Stage 2)                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Phase 8: Component Specifications                              │    │
│  │  - Read manifests/components.json                               │    │
│  │  - Map Discovery requirements to library components             │    │
│  │  - Define screen-specific aggregate components                  │    │
│  └────────────────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Phase 9: Screen Specifications                                 │    │
│  │  - Compose screens using library components                     │    │
│  │  - Define data requirements and API integration points          │    │
│  └────────────────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  Phase 11-12: Code Generation                                   │    │
│  │  - Import from component library                                │    │
│  │  - Focus on data fetching and business logic                    │    │
│  │  - FORBIDDEN: Raw HTML elements (div, button, input)            │    │
│  └────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│                       WORKING PROTOTYPE                                 │
│  - All components accessible by default (React Aria)                    │
│  - Consistent styling (Tailwind theme tokens)                           │
│  - Focus on business logic, not boilerplate                             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Library Structure

The component library is located at `.claude/templates/component-library/` and follows this structure:

```
component-library/
├── manifests/
│   └── components.json           # 62 components organized by category
├── src/                          # Component implementations
│   ├── Button/
│   │   ├── Button.tsx
│   │   └── Button_readme.md     # API documentation
│   ├── TextField/
│   ├── ComboBox/
│   └── ... (60+ components)
├── stories/                      # Storybook examples
│   ├── Button.stories.tsx        # Visual variants and interactions
│   └── ...
├── themes/                       # Tailwind theme plugin
│   └── index.js                  # Design tokens
├── templates/                    # Starter configurations
│   └── tailwind.config.js
├── examples/                     # Reference implementations
├── SKILL.md                      # LLM usage protocol
├── INTERACTIONS.md               # State patterns and async handling
└── README.md                     # Overview
```

---

## Component Categories

The library provides 62 components across 10 categories:

| Category | Components | Use Cases |
|----------|------------|-----------|
| **Forms** | TextField, Checkbox, RadioGroup, Switch, Slider, NumberField, SearchField, TextArea | User input, data collection |
| **Buttons** | Button, ActionGroup, FileTrigger, ToggleButton | Actions, file uploads |
| **Pickers** | Autocomplete, ComboBox, Select | Searchable dropdowns, selections |
| **Collections** | Table, GridList, ListBox, Menu, TagGroup, Tree, Card, CardView | Data display, navigation |
| **Date & Time** | Calendar, DateField, DatePicker | Scheduling, date selection |
| **Color** | ColorArea, ColorField, ColorPicker, ColorSlider, ColorSwatch, ColorWheel | Color selection |
| **Navigation** | Breadcrumbs, Link, Tabs | Site navigation |
| **Overlays** | Dialog, Modal, Popover, Tooltip | Contextual information |
| **Layout** | Disclosure, Flex, Grid, Group, Separator, Toolbar, View, Well | Page structure |
| **Status** | Badge, Meter, ProgressBar, StatusLight | Loading, status indicators |

---

## Token Optimization Strategy

### **Traditional Approach (Token Expensive)**

```tsx
// ~800 tokens for a single accessible button
<button
  className="px-4 py-2 bg-blue-500 hover:bg-blue-700 text-white rounded"
  onClick={handleClick}
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
  onFocus={() => setIsFocused(true)}
  onBlur={() => setIsFocused(false)}
  role="button"
  aria-label="Submit form"
  aria-pressed={isPressed}
  tabIndex={0}
>
  Submit
</button>
```

### **Assembly-First Approach (Token Efficient)**

```tsx
// ~50 tokens - accessibility and styling built-in
<Button onPress={handleClick}>Submit</Button>
```

**Savings:** ~15x token reduction per component

---

## Discovery → Component Mapping

During prototype generation, Discovery outputs are mapped to component library elements:

| Discovery Artifact | Component Library Mapping |
|--------------------|---------------------------|
| `screen-definitions.md` | Decomposed into component compositions |
| `data-fields.md` | Mapped to Form components (TextField, Select, etc.) |
| `navigation-structure.md` | Mapped to Tabs, Breadcrumbs, Link |
| `interaction-patterns.md` | Mapped to state patterns in INTERACTIONS.md |

### **Example Mapping**

**Discovery: screen-definitions.md**
```markdown
## S-1.1: User Login Screen
- Email input field (required, validation)
- Password input field (required, masked)
- Remember me checkbox
- Submit button
- Forgot password link
```

**Assembly-First Component Spec:**
```tsx
import { Form, TextField, Checkbox, Button, Link } from '@/component-library';

<Form onSubmit={handleLogin}>
  <TextField name="email" type="email" label="Email" isRequired />
  <TextField name="password" type="password" label="Password" isRequired />
  <Checkbox>Remember me</Checkbox>
  <Button type="submit">Sign In</Button>
  <Link href="/forgot-password">Forgot password?</Link>
</Form>
```

---

## Prototype Generation Workflow

### **Phase 8: Component Specifications**

**Input:**
- Discovery `screen-definitions.md`
- Discovery `data-fields.md`
- Component library `manifests/components.json`

**Process:**
1. **Read Component Manifest**: Load available components and their categories
2. **Map Requirements**: Match Discovery requirements to library components
3. **Identify Gaps**: Determine which aggregate components need to be created
4. **Generate Specs**: Create component specifications in `01-components/`

**Output:**
```
Prototype_<SystemName>/01-components/
├── component-index.md              # Maps Discovery screens to components
├── primitives/
│   └── library-components.md       # References to component library
├── aggregates/
│   ├── UserProfileCard.md          # Custom aggregate component
│   └── TaskList.md                 # Custom aggregate component
```

**Key Rule:** Only create aggregate components when multiple library components need to be combined with custom logic. Single library components are referenced, not duplicated.

---

### **Phase 9: Screen Specifications**

**Input:**
- Component specifications from Phase 8
- Component library INTERACTIONS.md (state patterns)

**Process:**
1. **Compose Screens**: Use library components and aggregates
2. **Define Data Flow**: Specify API integration points
3. **State Management**: Use React Aria render props for state

**Output:**
```
Prototype_<SystemName>/02-screens/
├── screen-index.md
└── login-screen/
    ├── specification.md
    ├── component-usage.md          # Lists library components used
    └── data-requirements.md
```

---

### **Phase 11-12: Code Generation**

**Input:**
- Screen specifications from Phase 9
- Component library SKILL.md (usage protocol)

**Process:**
1. **Import Library Components**: `import { Button, TextField } from '@/component-library'`
2. **Write Glue Code**: Data fetching, state management, business logic
3. **Compose UI**: Assemble library components with Tailwind for layout
4. **NO Raw HTML**: Forbidden to use `<div>`, `<button>`, `<input>` if library component exists

**Output:**
```
Prototype_<SystemName>/prototype/src/
├── screens/
│   └── LoginScreen.tsx             # Composes library components
├── components/
│   └── UserProfileCard.tsx         # Custom aggregates only
└── hooks/
    └── useAuth.ts                  # Data fetching logic
```

**Example Generated Code:**
```tsx
// LoginScreen.tsx
import { Form, TextField, Button, Link } from '@/component-library';
import { useAuth } from '@/hooks/useAuth';

export function LoginScreen() {
  const { login, isPending } = useAuth();

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-full max-w-md p-8">
        <Form onSubmit={login} className="flex flex-col gap-4">
          <TextField
            name="email"
            type="email"
            label="Email"
            isRequired
          />
          <TextField
            name="password"
            type="password"
            label="Password"
            isRequired
          />
          <Button type="submit" isPending={isPending}>
            Sign In
          </Button>
          <Link href="/forgot-password">Forgot password?</Link>
        </Form>
      </div>
    </div>
  );
}
```

---

## Accessibility by Default

All components are built on **React Aria Components**, which provide:

### **Automatic ARIA Attributes**
- `role`, `aria-label`, `aria-labelledby`, `aria-describedby`
- `aria-required`, `aria-invalid`, `aria-disabled`
- `aria-expanded`, `aria-selected`, `aria-pressed`

### **Keyboard Navigation**
- Tab navigation with focus management
- Arrow keys for collections (ListBox, Menu, Table)
- Enter/Space for activation
- Escape for dismissing overlays

### **Screen Reader Support**
- Live region announcements for dynamic content
- Proper focus order and semantic structure
- Form validation messages announced

### **Focus Management**
- `isFocusVisible` for keyboard-only focus rings
- Focus restoration after overlay dismissal
- Focus trapping in modals

**No Manual ARIA Required:** The LLM does NOT need to add accessibility attributes—they're handled by the components.

---

## Styling Strategy

### **Design Tokens (Tailwind Theme)**

The library defines semantic tokens in `tailwind.config.js`:

```js
colors: {
  canvas: 'var(--bg-canvas)',
  surface: { 1: 'var(--bg-surface-1)', 2: 'var(--bg-surface-2)' },
  text: {
    primary: 'var(--text-primary)',
    secondary: 'var(--text-secondary)',
    muted: 'var(--text-muted)',
    inverse: 'var(--text-inverse)',
    link: 'var(--text-link)',
  },
  accent: {
    DEFAULT: 'var(--accent-default)',
    hover: 'var(--accent-hover)',
    active: 'var(--accent-active)',
  },
  border: { subtle: 'var(--border-subtle)', DEFAULT: 'var(--border-default)' },
  focusRing: 'var(--focus-ring)',
  success: 'var(--success)', warning: 'var(--warning)',
  danger: 'var(--danger)', info: 'var(--info)',
}
```

### **Render Props Pattern**

Components accept a function for `className` that receives render state:

```tsx
<Button
  className={({ isPressed, isHovered, isFocusVisible }) =>
    `px-4 py-2 rounded ${isPressed ? 'bg-accent-active' : 'bg-accent-default'}
     ${isFocusVisible ? 'ring-2 ring-focusRing' : ''}`
  }
>
  Press Me
</Button>
```

**Common Render States:**
- `isHovered` - Pointer over element
- `isPressed` - Mouse down / touch start
- `isFocused` - Keyboard or pointer focus
- `isFocusVisible` - Keyboard focus only (accessibility)
- `isDisabled` - Non-interactive state
- `isSelected` - Toggle/selection state
- `isPending` - Async operation in progress

### **Layout with Tailwind Only**

Use Tailwind utility classes for layout and spacing:

```tsx
<div className="flex flex-col gap-4 p-8 max-w-md mx-auto">
  <TextField label="Email" />
  <TextField label="Password" />
  <Button>Submit</Button>
</div>
```

**Do NOT write custom CSS classes** unless absolutely necessary.

---

## Advanced Patterns

### **Async Data Loading**

Use React Stately hooks for complex data management:

```tsx
import { useAsyncList } from 'react-stately';
import { ComboBox, Item, Label, Input, Popover, ListBox } from '@/component-library';

export function UserSearch() {
  const list = useAsyncList({
    async load({ filterText }) {
      const res = await fetch(`/api/users?q=${filterText}`);
      const json = await res.json();
      return { items: json.users };
    }
  });

  return (
    <ComboBox
      items={list.items}
      inputValue={list.filterText}
      onInputChange={list.setFilterText}
    >
      <Label>Search Users</Label>
      <Input />
      <Popover>
        <ListBox>
          {(item) => <Item key={item.id}>{item.name}</Item>}
        </ListBox>
      </Popover>
    </ComboBox>
  );
}
```

### **Form Validation**

Use `validationState` and `FieldError`:

```tsx
import { TextField, Form, FieldError } from '@/component-library';

<Form>
  <TextField
    name="email"
    label="Email"
    validationState={emailError ? 'invalid' : 'valid'}
  >
    {emailError && <FieldError>{emailError}</FieldError>}
  </TextField>
</Form>
```

### **Pending States**

Use `isPending` prop for async operations:

```tsx
<Button
  onPress={handleSave}
  isPending={isSaving}
>
  {isSaving ? 'Saving...' : 'Save'}
</Button>
```

---

## Quality Gates

### **Component Usage Validation**

Before generating code, the system validates:

1. **Component Availability Check**: All referenced components exist in `manifests/components.json`
2. **No Raw HTML**: No `<button>`, `<input>`, `<select>`, `<textarea>` elements
3. **Import Validation**: All imports resolve to component library
4. **Accessibility**: No manual ARIA attributes (handled by library)

### **Checkpoint Integration**

| Checkpoint | Validation |
|------------|------------|
| CP 8 (Components) | Component manifest read, aggregate specs generated |
| CP 9 (Screens) | All screens reference library components |
| CP 12 (Build) | No raw HTML elements, all imports valid |
| CP 14 (QA) | Accessibility audit passes (WCAG 2.1 AA) |

---

## Benefits

### **Token Efficiency**
- **15-20x reduction** in generated code per screen
- Focus tokens on business logic, not boilerplate
- Faster generation, lower API costs

### **Consistency**
- All components follow same design language
- Predictable behavior across screens
- No style drift between iterations

### **Accessibility**
- WCAG 2.1 AA compliance by default
- No manual ARIA attribute management
- Proper keyboard navigation and focus management

### **Maintainability**
- Single source of truth for component behavior
- Updates to library propagate to all screens
- Clear separation: library (reusable) vs. glue code (custom)

### **Determinism**
- Same Discovery inputs → Same component choices
- Reduced LLM variability
- Reproducible prototypes

---

## Integration with CLAUDE.md

See **CLAUDE.md** sections:
- **Prototype Commands** - Commands that enforce assembly-first approach
- **Prototype Skills** - Skills that read component manifests
- **Assembly-First Rule** - `.claude/commands/_assembly_first_rules.md`

---

## References

- **Component Library**: `.claude/templates/component-library/`
- **SKILL.md**: LLM usage protocol
- **INTERACTIONS.md**: State patterns and async handling
- **manifests/components.json**: Component registry (62 components)
- **React Aria Documentation**: https://react-spectrum.adobe.com/react-aria/
- **Tailwind CSS**: https://tailwindcss.com/
