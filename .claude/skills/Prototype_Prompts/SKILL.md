---
name: generating-codegen-prompts
description: Use when you need to generate structured code generation prompts for external AI coding assistants based on prototype specifications.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-codegen-prompts started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-codegen-prompts ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-codegen-prompts instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

# Prompts Generator

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_Prompts
- **Version**: 2.3.1
- **Created**: 2024-12-13
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3

## Description
Generate structured prompts for code generation. Follows OUTPUT_STRUCTURE.md for deterministic folder structure.

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

Generate structured prompts for code generation. Follows OUTPUT_STRUCTURE.md for deterministic folder structure.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: App names and implementation details shown in prompts (e.g., "recruiter", "candidate", "hiring-manager") are examples from an ATS domain. Your actual prompts should reference your project's apps, components, and screens.

## Execution Logging (MANDATORY)

This skill logs all execution to the global pipeline progress registry. Logging is automatic and requires no manual configuration.

### How Logging Works

Every execution of this skill is logged to `_state/lifecycle.json`:

- **start_event**: Logged when skill execution begins
- **end_event**: Logged when skill execution completes

Events include:
- skill_name, intent, stage, system_name
- start/end timestamps
- status (completed/failed)
- output files created (code generation prompts)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "generating-codegen-prompts"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "generating-codegen-prompts" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## Output Structure (REQUIRED)

This skill MUST generate the following structure:

```
04-implementation/
├── prompts/
│   ├── component-development.md      # Component implementation prompts
│   ├── foundation-setup.md           # Project setup prompts
│   ├── screen-implementation.md      # Screen implementation prompts
│   └── {phase-name}.md               # Additional phase-specific prompts
└── MASTER_IMPL_PROMPT.md             # Master prompt combining all
```

Note: The sequence/ directory is handled by the Sequencer skill.

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ _state/implementation_sequence.json → phases and order
READ 00-foundation/DESIGN_TOKENS.md → token references
READ 01-components/COMPONENT_LIBRARY_SUMMARY.md → component list
READ 02-screens/SCREEN_SPECIFICATIONS_SUMMARY.md → screen list
READ 00-foundation/data-model/DATA_MODEL.md → entity list

IF implementation_sequence missing:
  BLOCK: "Run Sequencer first"
```

### Step 2: Generate Foundation Setup Prompt
```
CREATE 04-implementation/prompts/foundation-setup.md:
  # Foundation Setup Prompt
  
  ## Context
  
  You are setting up the foundation layer for {Product Name}, an ATS 
  (Applicant Tracking System) prototype.
  
  ## Technology Stack
  
  - **Framework:** React 18 with Vite
  - **Styling:** Tailwind CSS with custom design tokens
  - **State:** React Context + useState/useReducer
  - **Data:** IndexedDB via Dexie.js (local-first)
  - **Routing:** React Router v6
  - **Build:** Vite 5.x
  
  ## Project Structure
  
  Create the following structure:
  
  ```
  prototype/
  ├── index.html
  ├── package.json
  ├── vite.config.ts
  ├── tsconfig.json
  ├── tailwind.config.js
  ├── postcss.config.js
  ├── public/
  │   └── assets/
  └── src/
      ├── main.tsx
      ├── App.tsx
      ├── index.css
      ├── components/
      │   ├── primitives/
      │   ├── data-display/
      │   ├── feedback/
      │   ├── navigation/
      │   ├── overlays/
      │   └── patterns/
      ├── screens/
      │   ├── recruiter/
      │   ├── hiring-manager/
      │   ├── interviewer/
      │   ├── candidate/
      │   └── admin/
      ├── db/
      │   ├── database.ts
      │   ├── schema.ts
      │   └── seed.ts
      ├── services/
      │   └── api.ts
      ├── hooks/
      │   └── useDatabase.ts
      ├── utils/
      │   └── helpers.ts
      └── styles/
          └── tokens.css
  ```
  
  ## Design Tokens
  
  Reference the design tokens from:
  - 00-foundation/DESIGN_TOKENS.md
  - 00-foundation/colors.md
  - 00-foundation/typography.md
  - 00-foundation/spacing-layout.md
  
  Create `src/styles/tokens.css` with all CSS custom properties.
  
  ## Database Schema
  
  Reference the data model from:
  - 00-foundation/data-model/DATA_MODEL.md
  - 00-foundation/data-model/entities/*.schema.json
  
  Create Dexie.js schema in `src/db/schema.ts`.
  
  ## Initial Setup Tasks
  
  1. Initialize Vite project with React + TypeScript template
  2. Install dependencies:
     ```bash
     npm install react-router-dom dexie tailwindcss postcss autoprefixer
     npm install -D @types/react @types/react-dom typescript
     ```
  3. Configure Tailwind with design tokens
  4. Create base layout component with:
     - Header (64px height)
     - Sidebar (240px width, collapsible)
     - Main content area
  5. Set up routing structure
  6. Initialize IndexedDB with schema
  7. Create seed data from test-data
  
  ## Validation
  
  After setup, verify:
  - [ ] `npm run dev` starts successfully
  - [ ] `npm run build` completes without errors
  - [ ] Base layout renders with header and sidebar
  - [ ] Database initializes with seed data
  - [ ] Routes navigate correctly
```

### Step 3: Generate Component Development Prompt
```
CREATE 04-implementation/prompts/component-development.md:
  # Component Development Prompt
  
  ## Context
  
  Implement the component library for {Product Name} following the 
  specifications in `01-components/`.
  
  ## Component Categories
  
  1. **Primitives** (implement first)
     - Button, Input, Select, Checkbox, Radio, Switch, Textarea, Label
     
  2. **Data Display**
     - Avatar, Badge, Card, EmptyState, List, Progress, Skeleton, 
       Stat, Table, Tag, Timeline, KanbanColumn
     
  3. **Feedback**
     - Alert, Toast, Tooltip
     
  4. **Navigation**
     - Breadcrumb, CommandPalette, Header, Pagination, Sidebar, 
       Stepper, Tabs
     
  5. **Overlays**
     - ContextMenu, Dialog, Drawer, Dropdown, Menu, Popover
     
  6. **Patterns** (implement last, uses primitives + data display)
     - CandidateCard, InterviewSlot, PositionCard
  
  ## For Each Component
  
  1. **Read the spec** from `01-components/{category}/{component}.md`
  
  2. **Implement all variants:**
     ```tsx
     // Example: Button variants
     <Button variant="primary" />
     <Button variant="secondary" />
     <Button variant="danger" />
     <Button variant="ghost" />
     ```
  
  3. **Implement all sizes:**
     ```tsx
     <Button size="sm" />
     <Button size="md" />
     <Button size="lg" />
     ```
  
  4. **Implement all states:**
     - default, hover, focus, active, disabled, loading
  
  5. **Use design tokens:**
     ```css
     .button {
       background: var(--color-primary-500);
       padding: var(--space-2) var(--space-4);
       border-radius: var(--radius-md);
       font-size: var(--text-sm);
     }
     ```
  
  6. **Add accessibility:**
     - Keyboard navigation (Tab, Enter, Space, Escape)
     - Focus indicators (visible focus ring)
     - ARIA attributes where needed
     - Screen reader support
  
  ## File Structure
  
  ```
  src/components/
  ├── primitives/
  │   ├── Button.tsx
  │   ├── Button.css (if needed)
  │   ├── Input.tsx
  │   └── index.ts (re-exports)
  ├── data-display/
  │   ├── Card.tsx
  │   └── index.ts
  ...
  └── index.ts (main export)
  ```
  
  ## Component Template
  
  ```tsx
  import React from 'react';
  import './Component.css';
  
  interface ComponentProps {
    variant?: 'primary' | 'secondary';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    children: React.ReactNode;
  }
  
  export const Component: React.FC<ComponentProps> = ({
    variant = 'primary',
    size = 'md',
    disabled = false,
    children,
  }) => {
    return (
      <div
        className={`component component--${variant} component--${size}`}
        aria-disabled={disabled}
      >
        {children}
      </div>
    );
  };
  ```
  
  ## Validation
  
  For each component, verify:
  - [ ] All variants render correctly
  - [ ] All sizes render correctly
  - [ ] Hover state works
  - [ ] Focus state visible (keyboard)
  - [ ] Disabled state prevents interaction
  - [ ] Loading state shows indicator
  - [ ] Keyboard navigation works
  - [ ] Screen reader announces correctly
```

### Step 4: Generate Screen Implementation Prompt
```
CREATE 04-implementation/prompts/screen-implementation.md:
  # Screen Implementation Prompt
  
  ## Context
  
  Implement the screens for {Product Name} following the specifications 
  in `02-screens/`.
  
  ## Screen Organization
  
  ### By App
  
  1. **Recruiter App** (`/recruiter/...`)
     - Dashboard: `/recruiter/dashboard`
     - Pipeline: `/recruiter/pipeline`
     - Candidate Profile: `/recruiter/candidates/:id`
     - Position Management: `/recruiter/positions`
     - Interview Scheduling: `/recruiter/scheduling`
     - Messaging: `/recruiter/messages`
  
  2. **Hiring Manager App** (`/hiring-manager/...`)
     - Triage Queue: `/hiring-manager/triage`
     - Team Pipeline: `/hiring-manager/team`
     - Offer Decisions: `/hiring-manager/offers`
  
  3. **Interviewer Portal** (`/interviewer/...`)
     - Dashboard: `/interviewer/dashboard`
     - Availability: `/interviewer/availability`
  
  4. **Candidate Portal** (`/candidate/...`)
     - Dashboard: `/candidate/dashboard`
     - Application: `/candidate/application`
  
  5. **Admin Panel** (`/admin/...`)
     - User Management: `/admin/users`
     - Roles: `/admin/roles`
  
  ## For Each Screen
  
  1. **Read the spec** from `02-screens/{app}/{screen}.md`
  
  2. **Implement layout:**
     - Use the grid structure defined in spec
     - Position components as shown in ASCII diagram
     - Respect responsive breakpoints
  
  3. **Connect data:**
     - Import from IndexedDB via hooks
     - Handle loading states
     - Handle empty states
     - Handle error states
  
  4. **Implement interactions:**
     - All user actions from spec
     - Form submissions
     - Navigation
     - Filters/search
  
  5. **Add responsive behavior:**
     - Desktop: Full layout
     - Tablet: Adapted layout
     - Mobile: Simplified layout
  
  ## Screen Template
  
  ```tsx
  import React, { useState, useEffect } from 'react';
  import { useDatabase } from '../../hooks/useDatabase';
  import { Header, Sidebar, Card, Table } from '../../components';
  
  export const ScreenName: React.FC = () => {
    const { data, loading, error } = useDatabase('entity');
    const [filter, setFilter] = useState('');
    
    if (loading) return <ScreenSkeleton />;
    if (error) return <ErrorState message={error} />;
    if (!data.length) return <EmptyState />;
    
    return (
      <div className="screen-layout">
        <Header />
        <div className="screen-content">
          <Sidebar />
          <main className="screen-main">
            {/* Screen content */}
          </main>
        </div>
      </div>
    );
  };
  ```
  
  ## Data Integration
  
  ```tsx
  // hooks/useDatabase.ts
  import { useLiveQuery } from 'dexie-react-hooks';
  import { db } from '../db/database';
  
  export function useCandidates(filter?: CandidateFilter) {
    return useLiveQuery(async () => {
      let query = db.candidates;
      if (filter?.status) {
        query = query.where('status').equals(filter.status);
      }
      return query.toArray();
    }, [filter]);
  }
  ```
  
  ## Validation
  
  For each screen, verify:
  - [ ] Layout matches spec
  - [ ] All components render
  - [ ] Data loads correctly
  - [ ] Loading state shows skeleton
  - [ ] Empty state shows CTA
  - [ ] Error state shows message
  - [ ] Interactions work
  - [ ] Responsive layout works
```

### Step 5: Generate Additional Phase Prompts
```
FOR each phase in implementation_sequence:
  IF phase needs specific prompt:
    CREATE 04-implementation/prompts/{phase-name}.md:
      # {Phase Name} Implementation Prompt
      
      ## Context
      [Phase-specific context]
      
      ## Prerequisites
      [What must be done before]
      
      ## Tasks
      [Specific implementation tasks]
      
      ## Validation
      [How to verify completion]
```

### Step 6: Update Master Implementation Prompt
```
UPDATE 04-implementation/MASTER_IMPL_PROMPT.md:
  # Master Implementation Prompt
  
  ## Project: {Product Name}
  
  This prompt guides the complete implementation of the prototype.
  
  ---
  
  ## Quick Start
  
  1. Start with [foundation-setup.md](prompts/foundation-setup.md)
  2. Implement components with [component-development.md](prompts/component-development.md)
  3. Build screens with [screen-implementation.md](prompts/screen-implementation.md)
  4. Follow phase sequence in `sequence/` directory
  
  ---
  
  ## Resource Locations
  
  | Resource | Location |
  |----------|----------|
  | Design Tokens | 00-foundation/DESIGN_TOKENS.md |
  | Color System | 00-foundation/colors.md |
  | Typography | 00-foundation/typography.md |
  | Spacing | 00-foundation/spacing-layout.md |
  | Data Model | 00-foundation/data-model/ |
  | API Contracts | 00-foundation/api-contracts/ |
  | Test Data | 00-foundation/test-data/ |
  | Components | 01-components/ |
  | Screens | 02-screens/ |
  | Interactions | 03-interactions/ |
  
  ---
  
  ## Implementation Order
  
  ### Phase 0: Foundation Setup
  - [ ] Project scaffolding
  - [ ] Design tokens integration
  - [ ] Database setup
  - [ ] Routing configuration
  
  ### Phase 1: Primitives
  - [ ] Button, Input, Select, Checkbox
  - [ ] Radio, Switch, Textarea, Label
  
  ### Phase 2: Data Display Components
  - [ ] Card, Badge, Avatar, Tag
  - [ ] Table, List, Timeline
  - [ ] Skeleton, EmptyState, Progress
  
  ### Phase 3: Feedback & Navigation
  - [ ] Alert, Toast, Tooltip
  - [ ] Header, Sidebar, Tabs
  - [ ] Breadcrumb, Pagination
  
  ### Phase 4: Overlays
  - [ ] Dialog, Drawer, Dropdown
  - [ ] Menu, Popover, ContextMenu
  
  ### Phase 5: Pattern Components
  - [ ] CandidateCard, PositionCard
  - [ ] InterviewSlot, KanbanColumn
  
  ### Phase 6: Core Screens
  - [ ] Recruiter Dashboard
  - [ ] Candidate Pipeline
  - [ ] Candidate Profile
  
  ### Phase 7: Secondary Screens
  - [ ] Hiring Manager screens
  - [ ] Interviewer screens
  - [ ] Candidate portal
  
  ### Phase 8: Polish
  - [ ] Animations (03-interactions/)
  - [ ] Loading states
  - [ ] Error handling
  
  ---
  
  ## Checkpoints
  
  | Checkpoint | After | Criteria |
  |------------|-------|----------|
  | 1 | Phase 2 | Build works, components render |
  | 2 | Phase 5 | All components complete |
  | 3 | Phase 7 | All screens functional |
  | 4 | Phase 8 | Production ready |
  
  ---
  
  ## Prompts Index
  
  - [Foundation Setup](prompts/foundation-setup.md)
  - [Component Development](prompts/component-development.md)
  - [Screen Implementation](prompts/screen-implementation.md)
```

### Step 7: Validate Outputs (REQUIRED)
```
VALIDATE prompts:
  FILE CHECKS:
    - prompts/foundation-setup.md exists
    - prompts/component-development.md exists
    - prompts/screen-implementation.md exists
    - MASTER_IMPL_PROMPT.md updated
    
  CONTENT CHECKS:
    - All prompts reference correct spec files
    - Technology stack consistent
    - Implementation order logical
    
IF any validation fails:
  PROMPT with mitigation options
```

### Step 8: Update Progress
```
UPDATE _state/progress.json:
  phases.prompts.status = "complete"
  phases.prompts.completed_at = timestamp
  phases.prompts.outputs = [
    "04-implementation/MASTER_IMPL_PROMPT.md",
    "04-implementation/prompts/foundation-setup.md",
    "04-implementation/prompts/component-development.md",
    "04-implementation/prompts/screen-implementation.md"
  ]
  phases.prompts.metrics = {
    prompts_generated: count,
    phases_covered: count
  }
```

---

## Output Files (REQUIRED)

| Path | Purpose | Blocking? |
|------|---------|-----------|
| `MASTER_IMPL_PROMPT.md` | Master prompt | ✅ Yes |
| `prompts/foundation-setup.md` | Project setup | ✅ Yes |
| `prompts/component-development.md` | Component guide | ✅ Yes |
| `prompts/screen-implementation.md` | Screen guide | ✅ Yes |

---

## Progress.json Update

```json
{
  "phases": {
    "prompts": {
      "status": "complete",
      "completed_at": "2024-12-13T13:30:00Z",
      "outputs": [
        "04-implementation/MASTER_IMPL_PROMPT.md",
        "04-implementation/prompts/*.md"
      ],
      "metrics": {
        "prompts_generated": 4,
        "phases_covered": 8
      }
    }
  }
}
```
