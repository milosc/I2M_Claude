---
name: generating-prototype-code
description: Use when you need to generate runnable prototype code from specifications using Test-Driven Development (TDD) to ensure high quality and reliability.
model: sonnet
allowed-tools: Read, Write, Edit, Bash
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-prototype-code started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-prototype-code ended '{"stage": "prototype"}'
---

# Code Generator (TDD-Enhanced)

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill generating-prototype-code instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning
> **Supports**: Smart Obsolescence Handling for non-UI projects

## Metadata
- **Skill ID**: Prototype_CodeGen
- **Version**: 3.0.0
- **Created**: 2024-12-13
- **Updated**: 2025-12-26
- **Author**: Milos Cigoj
- **Change History**:
  - v3.0.0 (2025-12-26): Added NOT_APPLICABLE handling for non-UI projects
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3

Generate runnable prototype code from specifications using Test-Driven Development. Follows OUTPUT_STRUCTURE.md for deterministic folder structure.

> **TDD ENFORCEMENT**: This skill follows the Iron Law of TDD - NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST. All components and screens are generated test-first.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: The folder names shown below (e.g., `recruiter/`, `candidate/`, `hiring-manager/`) are examples from an ATS domain. Your actual screen folders, component names, and routes should be derived from your project's screen specifications.

## TDD Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**Violating the letter of this rule is violating the spirit of this rule.**

### Red-Green-Refactor Cycle

For EVERY component and screen:

```
┌─────────────────────────────────────────────────────────────────┐
│  RED          │  GREEN           │  REFACTOR                   │
│  Write test   │  Write minimal   │  Clean up, keep tests green │
│  Watch fail   │  code to pass    │                             │
└─────────────────────────────────────────────────────────────────┘
     │                │                      │
     ▼                ▼                      ▼
  VERIFY          VERIFY               VERIFY
  test FAILS      test PASSES          still PASSES
```

### TDD Enforcement Rules

1. **Test First**: Generate test file BEFORE component/screen implementation
2. **Verify Red**: RUN test, CONFIRM it fails for the right reason (missing implementation)
3. **Minimal Green**: Write ONLY enough code to make test pass
4. **Verify Green**: RUN test, CONFIRM it passes
5. **No Skipping**: NEVER generate implementation without corresponding test

### What Happens If You Skip TDD?

```
IF implementation exists without test:
  DELETE the implementation
  START OVER with test first
  NO EXCEPTIONS

IF test passes immediately (never failed):
  Test is INVALID - doesn't prove anything
  REWRITE test to fail first
```

### Test Structure

Tests are placed alongside components in `__tests__/` directories:

```
prototype/
└── src/
    ├── components/
    │   ├── primitives/
    │   │   ├── Button.tsx
    │   │   └── __tests__/
    │   │       └── Button.test.tsx
    │   ├── data-display/
    │   │   ├── Card.tsx
    │   │   └── __tests__/
    │   │       └── Card.test.tsx
    └── screens/
        ├── recruiter/
        │   ├── CandidatePipeline.tsx
        │   └── __tests__/
        │       └── CandidatePipeline.test.tsx
```

---

## Assembly-First Import Requirements (MANDATORY)

> **CRITICAL**: All component imports MUST follow the Assembly-First architecture pattern defined in `.claude/commands/_assembly_first_rules.md`.

### Required Import Pattern

**ALL react-aria-components imports MUST come from `@/component-library`:**

```tsx
// ✅ CORRECT - Import from component library
import { Button, TextField, Form, Text } from '@/component-library';
import { useAuth } from '@/hooks/useAuth';

// ❌ WRONG - Direct import from react-aria-components
import { Button, TextField, Form } from 'react-aria-components';
import { Text } from '@/component-library';
```

### Why This Matters

The `@/component-library` path alias:
1. **Centralizes** all react-aria-components exports in one location
2. **Prevents** runtime import resolution errors
3. **Allows** for custom component overrides (like Text)
4. **Ensures** consistency across the prototype

### Component Library Export Pattern

The `src/component-library.ts` file re-exports ALL react-aria-components:

```typescript
// src/component-library.ts
export {
  // Forms
  Form, TextField, Button, Label, Input,
  Checkbox, RadioGroup, Select, ComboBox,

  // Collections
  Table, TableHeader, TableBody, Row, Cell,
  ListBox, ListBoxItem, Menu, MenuItem,

  // Overlays
  Dialog, Modal, Popover, Tooltip,

  // Status
  ProgressBar, Meter,

  // ... all other components
} from 'react-aria-components';

// Custom overrides
export { Text, TextContext } from './components/Text/Text';
```

### Code Generation Rules

When generating component or screen code:

1. **ALWAYS** import from `@/component-library`
2. **NEVER** import directly from `react-aria-components`
3. **CHECK** that component-library.ts exports the components you need
4. **REFERENCE** assembly-first.md rule for full requirements

### Violation Consequences

If code is generated with direct `react-aria-components` imports:
- ❌ Runtime errors in development
- ❌ Build failures in production
- ❌ Assembly-first validation failure at QA checkpoint
- ❌ Prototype delivery blocked

### Template Example

```tsx
// Screen Template (CORRECT)
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Form,
  TextField,
  Button,
  Label,
  Input,
  Text,
} from '@/component-library';
import { useAuth } from '@/hooks/useAuth';

export function {ScreenName}() {
  // Implementation
}
```

---

## Output Structure (REQUIRED)

> **⚠️ SHARED STATE FOLDER**: The `_state/` folder is at the **PROJECT ROOT level**, NOT inside `Prototype_<SystemName>/`. This folder is SHARED between Discovery and Prototype phases.
>
> ```
> project_root/
> ├── _state/                           ← SHARED state folder (ROOT LEVEL)
> │   ├── screen_registry.json          # Master screen tracking (READ/WRITE)
> │   ├── discovery_summary.json
> │   ├── requirements_registry.json
> │   └── progress.json
> ├── ClientAnalysis_<SystemName>/      ← Discovery outputs
> └── Prototype_<SystemName>/           ← Prototype outputs (prototype/ lives here)
> ```
>
> **Path Resolution**:
> - All paths starting with `_state/` resolve to the **ROOT-LEVEL shared folder**
> - All other paths (e.g., `prototype/`, `00-foundation/`) resolve relative to `Prototype_<SystemName>/`

This skill MUST generate the following structure pattern (inside `Prototype_<SystemName>/`):

```
prototype/
├── .gitignore
├── eslint.config.js
├── index.html
├── package.json
├── package-lock.json
├── public/
│   └── assets/
│       ├── images/
│       └── icons/
├── README.md
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── vite.config.ts
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── index.css
    ├── components/
    │   ├── data-display/
    │   │   ├── Avatar.tsx
    │   │   ├── Badge.tsx
    │   │   ├── Card.tsx
    │   │   └── ...
    │   ├── feedback/
    │   │   ├── Alert.tsx
    │   │   ├── Toast.tsx
    │   │   └── Tooltip.tsx
    │   ├── navigation/
    │   │   ├── Breadcrumb.tsx
    │   │   ├── Header.tsx
    │   │   ├── Sidebar.tsx
    │   │   └── ...
    │   ├── overlays/
    │   │   ├── Dialog.tsx
    │   │   ├── Drawer.tsx
    │   │   └── ...
    │   ├── patterns/
    │   │   ├── CandidateCard.tsx
    │   │   └── ...
    │   ├── primitives/
    │   │   ├── Button.tsx
    │   │   ├── Input.tsx
    │   │   └── ...
    │   └── index.ts
    ├── db/
    │   ├── database.ts
    │   ├── schema.ts
    │   └── seed.ts
    ├── forms/
    │   ├── CandidateForm.tsx
    │   └── PositionForm.tsx
    ├── hooks/
    │   ├── useDatabase.ts
    │   └── useLocalStorage.ts
    ├── pages/
    │   └── ... (if using page-based routing)
    ├── screens/
    │   ├── admin/
    │   │   ├── UserManagement.tsx
    │   │   └── RolesPermissions.tsx
    │   ├── candidate/
    │   │   ├── CandidateDashboard.tsx
    │   │   └── ApplicationForm.tsx
    │   ├── hiring-manager/
    │   │   ├── TriageQueue.tsx
    │   │   ├── TeamPipeline.tsx
    │   │   └── OfferDecisions.tsx
    │   ├── interviewer/
    │   │   ├── InterviewerDashboard.tsx
    │   │   └── Availability.tsx
    │   └── recruiter/
    │       ├── RecruiterDashboard.tsx
    │       ├── CandidatePipeline.tsx
    │       ├── CandidateProfile.tsx
    │       ├── PositionManagement.tsx
    │       ├── InterviewScheduling.tsx
    │       └── MessagingHub.tsx
    ├── services/
    │   ├── api.ts
    │   └── mock-api.ts
    ├── styles/
    │   ├── global.css
    │   └── tokens.css
    ├── utils/
    │   ├── formatters.ts
    │   ├── validators.ts
    │   └── helpers.ts
    └── workflows/
        ├── interview-scheduling.ts
        └── pipeline-management.ts
```

Alternative: Code in `src/` at root if prototype/ not used:

```
src/
├── app.js
├── components/
├── db/
├── forms/
├── index.html
├── pages/
├── screens/
├── services/
├── styles/
├── styles.css
├── utils/
└── workflows/
```

---

## Applicability Check (Smart Obsolescence Handling)

**BEFORE generating prototype code**, check project classification:

```
1. Read _state/prototype_config.json (or _state/discovery_config.json)
2. Check project_classification.type
3. IF type IN [BACKEND_ONLY, DATABASE_ONLY, INTEGRATION, INFRASTRUCTURE]:
   → Generate API-only or minimal prototype (see below)
   → SKIP UI component and screen code generation
4. IF type == FULL_STACK:
   → Proceed with full prototype code generation
```

### Handling Non-UI Project Types

For non-UI projects, generate a **minimal API prototype** instead:

```
prototype/
├── package.json           # Minimal Node.js config
├── tsconfig.json
├── src/
│   ├── index.ts           # Entry point
│   ├── db/
│   │   ├── schema.ts      # Data models (same as UI version)
│   │   ├── database.ts    # Database layer
│   │   └── seed.ts        # Test data seeding
│   ├── api/
│   │   ├── routes.ts      # API route definitions
│   │   └── handlers.ts    # Request handlers
│   └── services/
│       └── mock-api.ts    # Mock service layer
└── tests/
    └── api.test.ts        # API endpoint tests
```

### N/A Placeholder for UI Artifacts

If project type is NOT `FULL_STACK`, the following folders should contain placeholder READMEs:

**For `prototype/src/components/README.md`:**
```markdown
# Components

This folder is NOT APPLICABLE for {type} projects.

UI components are only generated for FULL_STACK projects.

See `../api/` and `../services/` for the relevant artifacts.
```

**For `prototype/src/screens/README.md`:**
```markdown
# Screens

This folder is NOT APPLICABLE for {type} projects.

Screen implementations are only generated for FULL_STACK projects.

See `../api/` and `../services/` for the relevant artifacts.
```

### API-Only Generation Mode

When in non-UI mode, the skill focuses on:
- **Data layer**: Full schema and database implementation
- **API layer**: Route definitions and handlers from api-contracts.json
- **Test data**: Seeding from test-data/ datasets
- **Tests**: API endpoint testing (not UI component tests)

```
IF project_type != FULL_STACK:
  SKIP Step 5 (Generate Components TDD)
  SKIP Step 6 (Generate Screens TDD)
  SKIP Step 6.5 (Validate Screen Coverage)

  EXECUTE:
    - Step 2: Initialize Project (minimal)
    - Step 3: Generate Design Token CSS → SKIP
    - Step 4: Generate Database Layer → EXECUTE
    - NEW: Generate API Layer
    - Step 9: Validate Build & Tests (API tests only)
```

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ 00-foundation/DESIGN_TOKENS.md → tokens
READ 00-foundation/colors.md → color palette
READ 00-foundation/typography.md → type scale
READ 00-foundation/spacing-layout.md → spacing
READ 00-foundation/AESTHETIC_DIRECTION.md → aesthetic (REQUIRED for Phase 2)
READ 00-foundation/data-model/ → entity schemas
READ 00-foundation/test-data/datasets/ → seed data
READ 01-components/ → component specs (with Visual Treatment sections)
READ 02-screens/ → screen specs
READ 03-interactions/ → motion specs
READ 04-implementation/ → implementation plan

// ═══════════════════════════════════════════════════════════
// CRITICAL: Load Screen Registry for Traceability
// ═══════════════════════════════════════════════════════════

LOAD traceability/screen_registry.json → screen_registry

IF screen_registry does NOT exist:
  ═══════════════════════════════════════════
  ❌ BLOCKING: Screen Registry Missing
  ═══════════════════════════════════════════

  Cannot proceed without screen registry.
  Run Prototype_ValidateDiscovery first to generate:
  traceability/screen_registry.json

  This registry tracks ALL screens from Discovery and
  ensures 100% implementation coverage.
  ═══════════════════════════════════════════

  STOP execution
  RETURN error

LOG: "📋 Loaded screen registry: {screen_registry.screen_coverage.discovery_total} screens from Discovery"

IF any critical input missing:
  BLOCK with appropriate message

IF AESTHETIC_DIRECTION.md missing:
  WARNING: "No aesthetic direction found. Components may look generic."
  PROMPT: "Run Components skill first to establish aesthetic direction, or continue with defaults?"

LOAD aesthetic_direction:
  direction_name: aesthetic.direction_name
  display_font: aesthetic.typography.display_font
  body_font: aesthetic.typography.body_font
  signature_color: aesthetic.color_strategy.signature_color
  animation_style: aesthetic.motion.animation_style
  differentiator: aesthetic.differentiator

DETERMINE technology stack:
  framework: React 18 | Vanilla JS
  styling: Tailwind | CSS Custom Properties
  data: IndexedDB via Dexie | localStorage
  routing: React Router | Hash routing
  build: Vite | None (vanilla)
  animations: Motion (framer-motion) | CSS only
```

### Step 1.5: Frontend Design Guidelines (REQUIRED)

> **Phase 2 Enhancement**: Apply frontend-design principles to avoid generic AI aesthetics.

```
DESIGN CODE GENERATION RULES:

  // ═══════════════════════════════════════════════════════════
  // FORBIDDEN: Generic AI Aesthetics
  // ═══════════════════════════════════════════════════════════

  NEVER use:
    - Inter, Roboto, Arial, system-ui as display fonts
    - Purple gradients on white backgrounds
    - Default shadcn/ui styling without customization
    - Generic 8px border-radius everywhere
    - Evenly distributed color palettes
    - Predictable card layouts

  // ═══════════════════════════════════════════════════════════
  // REQUIRED: Distinctive Implementation
  // ═══════════════════════════════════════════════════════════

  FOR typography:
    USE distinctive fonts from AESTHETIC_DIRECTION
    APPLY letter-spacing and line-height intentionally
    CREATE typographic hierarchy with contrast

  FOR colors:
    USE dominant color with sharp accents (not balanced)
    APPLY signature color consistently
    CREATE visual hierarchy through color contrast

  FOR motion:
    IMPORT Motion library for React: import { motion } from 'framer-motion'
    APPLY animation_style from aesthetic direction
    CREATE signature_interaction as memorable moment
    USE staggered reveals for page loads: staggerChildren, delayChildren

  FOR spatial composition:
    VARY spacing intentionally (not uniform)
    CREATE visual rhythm through asymmetry
    USE negative space or controlled density (per aesthetic)

  FOR visual details:
    ADD background treatments (gradient, texture, pattern)
    APPLY shadow style consistently
    INCLUDE decorative elements where appropriate

STORE design_rules for use in component/screen generation
```

### Step 1.6: Technology Stack Selection (Phase 5 Enhancement)

> **web-artifacts-builder Integration**: Option to generate modern React/shadcn/ui prototypes.

```
// ═══════════════════════════════════════════════════════════
// PHASE 5: ADVANCED STACK OPTIONS
// ═══════════════════════════════════════════════════════════

PROMPT user:
  ═══════════════════════════════════════════════════════════════
  🛠️ TECHNOLOGY STACK SELECTION
  ═══════════════════════════════════════════════════════════════

  Choose your prototype technology stack:

  STANDARD STACK (Default):
  ┌─────────────────────────────────────────────────────────────┐
  │  React 18 + TypeScript + Vite + Tailwind CSS                │
  │  • Fast development setup                                    │
  │  • Good for most prototypes                                  │
  │  • Lighter weight                                            │
  └─────────────────────────────────────────────────────────────┘

  ADVANCED STACK (shadcn/ui):
  ┌─────────────────────────────────────────────────────────────┐
  │  React 18 + TypeScript + Vite + Tailwind + shadcn/ui        │
  │  • 40+ pre-built accessible components                       │
  │  • Radix UI primitives for complex interactions             │
  │  • Can bundle to single HTML artifact                        │
  │  • Best for complex, production-like prototypes             │
  └─────────────────────────────────────────────────────────────┘

  Options:
  1. "standard" - Use standard stack (default)
  2. "advanced" - Use shadcn/ui stack
  3. "artifact" - Generate bundled HTML artifact (advanced + bundle)
  ═══════════════════════════════════════════════════════════════

  WAIT for user response

IF user selects "advanced" OR "artifact":

  STACK_CONFIG = {
    type: "shadcn",
    features: [
      "React 18 + TypeScript",
      "Vite for development",
      "Tailwind CSS 3.4.1",
      "shadcn/ui theming system",
      "40+ pre-installed components",
      "Radix UI dependencies",
      "Path aliases (@/)",
      "Parcel bundling for artifacts"
    ],
    components: [
      "accordion", "alert", "alert-dialog", "aspect-ratio", "avatar",
      "badge", "breadcrumb", "button", "calendar", "card", "carousel",
      "chart", "checkbox", "collapsible", "command", "context-menu",
      "data-table", "date-picker", "dialog", "drawer", "dropdown-menu",
      "form", "hover-card", "input", "input-otp", "label", "menubar",
      "navigation-menu", "pagination", "popover", "progress", "radio-group",
      "resizable", "scroll-area", "select", "separator", "sheet", "skeleton",
      "slider", "sonner", "switch", "table", "tabs", "textarea", "toast",
      "toggle", "toggle-group", "tooltip"
    ],
    bundle_to_artifact: user_selected == "artifact"
  }

  LOG: "Using advanced shadcn/ui stack"

ELSE:
  STACK_CONFIG = {
    type: "standard",
    features: ["React 18 + TypeScript", "Vite", "Tailwind CSS"],
    bundle_to_artifact: false
  }

  LOG: "Using standard stack"

STORE STACK_CONFIG for project initialization
```

### Step 2: Initialize Project
```
IF STACK_CONFIG.type == "shadcn":
  // ═══════════════════════════════════════════════════════════
  // ADVANCED STACK: shadcn/ui initialization
  // ═══════════════════════════════════════════════════════════

  CREATE prototype/ using init-artifact workflow:

  RUN: bash scripts/init-artifact.sh {product-slug}

  // This creates a fully configured project with:
  // - React + TypeScript (via Vite)
  // - Tailwind CSS 3.4.1 with shadcn/ui theming
  // - Path aliases (@/) configured
  // - 40+ shadcn/ui components pre-installed
  // - All Radix UI dependencies included
  // - Parcel configured for bundling

  LOG: "✅ shadcn/ui project initialized with 40+ components"

  // Configure for prototype requirements
  UPDATE prototype/src/lib/utils.ts:
    // Add prototype-specific utilities
    import { clsx, type ClassValue } from "clsx"
    import { twMerge } from "tailwind-merge"

    export function cn(...inputs: ClassValue[]) {
      return twMerge(clsx(inputs))
    }

  // Set up component index
  CREATE prototype/src/components/ui/index.ts:
    // Re-export all shadcn/ui components
    export * from "./button"
    export * from "./card"
    export * from "./dialog"
    export * from "./input"
    // ... all components from STACK_CONFIG.components

ELSE:
  // Standard stack initialization (existing flow)
  CREATE prototype/ directory structure

// ═══════════════════════════════════════════════════════════
// DEPENDENCY MANIFEST: Component Library Requirements
// ═══════════════════════════════════════════════════════════
//
// The component library requires specific dependencies to function.
// These are documented in the manifest file:
//
// SOURCE: .claude/templates/component-library/manifests/dependencies.json
//
// When updating dependencies, consult the manifest to ensure:
// • All 'required' dependencies are included
// • Versions match the manifest specifications
// • Optional dependencies are included based on components used
//
// See manifest categories:
// • required: clsx, tailwind-merge, react-aria, react-stately, tailwindcss
// • peer: react, react-dom (usually already present)
// • optional: @internationalized/* (if using date/number components)
//
// ═══════════════════════════════════════════════════════════

CREATE prototype/package.json:
  {
    "name": "{product-slug}",
    "version": "0.1.0",
    "type": "module",
    "scripts": {
      "dev": "vite",
      "build": "tsc && vite build",
      "preview": "vite preview",
      "lint": "eslint .",
      "test": "vitest",
      "test:run": "vitest run",
      "test:coverage": "vitest run --coverage"
    },
    "dependencies": {
      "react": "^18.2.0",
      "react-dom": "^18.2.0",
      "react-router-dom": "^6.20.0",
      "dexie": "^3.2.4",
      "dexie-react-hooks": "^1.1.7",
      "framer-motion": "^10.16.0",
      "clsx": "^2.0.0",
      "tailwind-merge": "^2.0.0"
    },
    "devDependencies": {
      "@testing-library/jest-dom": "^6.1.0",
      "@testing-library/react": "^14.0.0",
      "@testing-library/user-event": "^14.5.0",
      "@types/react": "^18.2.0",
      "@types/react-dom": "^18.2.0",
      "@vitejs/plugin-react": "^4.2.0",
      "autoprefixer": "^10.4.16",
      "jsdom": "^22.1.0",
      "postcss": "^8.4.31",
      "tailwindcss": "^3.3.5",
      "typescript": "^5.3.0",
      "vite": "^5.0.0",
      "vitest": "^1.0.0"
    }
  }

CREATE prototype/vitest.config.ts:
  import { defineConfig } from 'vitest/config';
  import react from '@vitejs/plugin-react';

  export default defineConfig({
    plugins: [react()],
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: ['./src/test/setup.ts'],
      include: ['src/**/*.test.{ts,tsx}'],
    },
    resolve: {
      alias: {
        '@': '/src',
      },
    },
  });

CREATE prototype/src/test/setup.ts:
  import '@testing-library/jest-dom';
  import { cleanup } from '@testing-library/react';
  import { afterEach } from 'vitest';

  // Cleanup after each test
  afterEach(() => {
    cleanup();
  });

CREATE prototype/vite.config.ts:
  import { defineConfig } from 'vite';
  import react from '@vitejs/plugin-react';
  
  export default defineConfig({
    plugins: [react()],
    resolve: {
      alias: {
        '@': '/src',
      },
    },
  });

CREATE prototype/tsconfig.json:
  {
    "compilerOptions": {
      "target": "ES2020",
      "useDefineForClassFields": true,
      "lib": ["ES2020", "DOM", "DOM.Iterable"],
      "module": "ESNext",
      "skipLibCheck": true,
      "moduleResolution": "bundler",
      "resolveJsonModule": true,
      "isolatedModules": true,
      "noEmit": true,
      "jsx": "react-jsx",
      "strict": true,
      "paths": {
        "@/*": ["./src/*"]
      }
    },
    "include": ["src"]
  }
```

### Step 3: Generate Design Token CSS
```
CREATE prototype/src/styles/tokens.css:
  /* Generated from 00-foundation design tokens */
  
  :root {
    /* Colors - Primitives */
    --color-gray-50: #f9fafb;
    --color-gray-100: #f3f4f6;
    /* ... all color tokens from colors.md ... */
    
    /* Colors - Semantic */
    --text-primary: var(--color-gray-900);
    --text-secondary: var(--color-gray-600);
    /* ... all semantic tokens ... */
    
    /* Typography */
    --font-sans: 'Inter', system-ui, sans-serif;
    --text-xs: 0.75rem;
    --text-sm: 0.875rem;
    /* ... all typography tokens ... */
    
    /* Spacing */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    /* ... all spacing tokens ... */
    
    /* Border Radius */
    --radius-sm: 0.125rem;
    --radius-md: 0.375rem;
    /* ... */
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
    /* ... */
    
    /* Z-Index */
    --z-dropdown: 1000;
    --z-modal: 1400;
    /* ... */
    
    /* Layout */
    --sidebar-width: 240px;
    --header-height: 64px;
  }
  
  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    * {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  }
```

### Step 4: Generate Database Layer
```
CREATE prototype/src/db/schema.ts:
  import Dexie, { Table } from 'dexie';
  
  // Entity interfaces from data model
  export interface Candidate {
    id: string;
    firstName: string;
    lastName: string;
    email: string;
    phone?: string;
    status: CandidateStatus;
    createdAt: string;
    updatedAt: string;
  }
  
  export type CandidateStatus = 
    | 'new' 
    | 'screening' 
    | 'interview' 
    | 'offer' 
    | 'hired' 
    | 'rejected';
  
  // ... all entities from data model ...
  
CREATE prototype/src/db/database.ts:
  import Dexie from 'dexie';
  import { Candidate, Position, User, ... } from './schema';
  
  class ATSDatabase extends Dexie {
    candidates!: Table<Candidate>;
    positions!: Table<Position>;
    users!: Table<User>;
    applications!: Table<Application>;
    interviews!: Table<Interview>;
    // ... all tables ...
    
    constructor() {
      super('ats-prototype');
      
      this.version(1).stores({
        candidates: 'id, status, email, createdAt',
        positions: 'id, status, departmentId, hiringManagerId',
        users: 'id, email, role',
        applications: 'id, candidateId, positionId, status',
        interviews: 'id, applicationId, interviewerId, scheduledAt',
        // ... all indexes ...
      });
    }
  }
  
  export const db = new ATSDatabase();

CREATE prototype/src/db/seed.ts:
  import { db } from './database';
  
  // Import seed data from test-data
  import catalogData from '../../00-foundation/test-data/datasets/catalog';
  import coreData from '../../00-foundation/test-data/datasets/core';
  import transactionalData from '../../00-foundation/test-data/datasets/transactional';
  
  export async function seedDatabase() {
    const count = await db.candidates.count();
    if (count > 0) return; // Already seeded
    
    await db.transaction('rw', 
      [db.candidates, db.positions, db.users, ...], 
      async () => {
        // Seed catalog data
        await db.departments.bulkAdd(catalogData.departments);
        await db.roles.bulkAdd(catalogData.roles);
        
        // Seed core data
        await db.users.bulkAdd(coreData.users);
        await db.candidates.bulkAdd(coreData.candidates);
        await db.positions.bulkAdd(coreData.positions);
        
        // Seed transactional data
        await db.applications.bulkAdd(transactionalData.applications);
        await db.interviews.bulkAdd(transactionalData.interviews);
      }
    );
  }
```

### Step 5: Generate Components (TDD)

**IRON LAW: Test first, implementation second.**

```
FOR each component category in 01-components/:
  FOR each component spec:

    LOG_PROMPT:
      skill: "Prototype_CodeGen"
      step: "Step 5: Generate Components"
      desired_outcome: "Generate {component} from spec using TDD"
      category: "generation"

    READ 01-components/{category}/{component}.md

    // ═══════════════════════════════════════════════════════════
    // PHASE 1: RED - Write Failing Test
    // ═══════════════════════════════════════════════════════════

    CREATE prototype/src/components/{category}/__tests__/{Component}.test.tsx:
      import { render, screen } from '@testing-library/react';
      import userEvent from '@testing-library/user-event';
      import { describe, it, expect, vi } from 'vitest';
      import { {Component} } from '../{Component}';

      describe('{Component}', () => {
        // Test rendering
        it('renders with required props', () => {
          render(<{Component} {...requiredProps} />);
          expect(screen.getByRole('{role}')).toBeInTheDocument();
        });

        // Test variants from spec
        it('renders {variant} variant correctly', () => {
          render(<{Component} variant="{variant}" />);
          expect(screen.getByRole('{role}')).toHaveClass('{expected-class}');
        });

        // Test interactions from spec
        it('calls onClick when clicked', async () => {
          const handleClick = vi.fn();
          render(<{Component} onClick={handleClick} />);
          await userEvent.click(screen.getByRole('{role}'));
          expect(handleClick).toHaveBeenCalledTimes(1);
        });

        // Test accessibility
        it('has accessible name', () => {
          render(<{Component} aria-label="Test label" />);
          expect(screen.getByLabelText('Test label')).toBeInTheDocument();
        });

        // Add tests for each variant/size/state from spec
      });

    // ═══════════════════════════════════════════════════════════
    // VERIFY RED: Run test, MUST fail
    // ═══════════════════════════════════════════════════════════

    RUN: npm run test:run -- src/components/{category}/__tests__/{Component}.test.tsx

    VERIFY test fails with expected error:
      Expected: "Cannot find module '../{Component}'" OR
                "Component is not defined" OR
                "Expected element to be in the document"

      IF test PASSES:
        ❌ ERROR: Test passed without implementation
        This means test is INVALID - doesn't test the right thing
        DELETE test, REWRITE to actually test the component

      IF test ERRORS (not fails):
        Fix the test syntax/imports
        Re-run until test FAILS (not errors)

    LOG: "✅ RED phase complete: Test fails as expected"

    // ═══════════════════════════════════════════════════════════
    // PHASE 2: GREEN - Write Minimal Implementation
    // ═══════════════════════════════════════════════════════════

    CREATE prototype/src/components/{category}/{Component}.tsx:
      import React from 'react';

      interface {Component}Props {
        // Props from spec - ONLY what tests require
      }

      export const {Component}: React.FC<{Component}Props> = ({
        // Destructured props with defaults
      }) => {
        return (
          // MINIMAL JSX to pass tests
          // Don't add features tests don't require
        );
      };

    // ═══════════════════════════════════════════════════════════
    // VERIFY GREEN: Run test, MUST pass
    // ═══════════════════════════════════════════════════════════

    RUN: npm run test:run -- src/components/{category}/__tests__/{Component}.test.tsx

    VERIFY test passes:
      IF test FAILS:
        Fix implementation (NOT the test)
        Re-run until pass

      IF test PASSES:
        LOG: "✅ GREEN phase complete: Test passes"

    // ═══════════════════════════════════════════════════════════
    // PHASE 3: REFACTOR - Clean up, stay green
    // ═══════════════════════════════════════════════════════════

    REFACTOR implementation:
      - Add remaining variants from spec
      - Apply design tokens
      - Add accessibility attributes
      - Clean up code structure

    RUN: npm run test:run -- src/components/{category}/__tests__/{Component}.test.tsx

    VERIFY still passes:
      IF test FAILS:
        Refactoring broke something - FIX immediately

      IF test PASSES:
        LOG: "✅ REFACTOR phase complete: Tests still pass"

    // ═══════════════════════════════════════════════════════════
    // RECORD: Track TDD cycle completion
    // ═══════════════════════════════════════════════════════════

    APPEND to tdd_evidence[]:
      {
        component: "{Component}",
        test_file: "src/components/{category}/__tests__/{Component}.test.tsx",
        impl_file: "src/components/{category}/{Component}.tsx",
        red_verified: true,
        green_verified: true,
        refactor_verified: true,
        timestamp: NOW()
      }
```

### Step 6: Generate Screens (TDD)

**IRON LAW: Test first, implementation second.**

```
FOR each app in 02-screens/:
  FOR each screen spec:

    LOG_PROMPT:
      skill: "Prototype_CodeGen"
      step: "Step 6: Generate Screens"
      desired_outcome: "Generate {screen} from spec using TDD"
      category: "generation"

    READ 02-screens/{app}/{screen}.md

    // ═══════════════════════════════════════════════════════════
    // PHASE 1: RED - Write Failing Test
    // ═══════════════════════════════════════════════════════════

    CREATE prototype/src/screens/{app}/__tests__/{Screen}.test.tsx:
      import { render, screen, waitFor } from '@testing-library/react';
      import userEvent from '@testing-library/user-event';
      import { describe, it, expect, vi, beforeEach } from 'vitest';
      import { BrowserRouter } from 'react-router-dom';
      import { {Screen} } from '../{Screen}';

      // Mock database
      vi.mock('../../../db/database', () => ({
        db: {
          {entity}: {
            toArray: vi.fn().mockResolvedValue([/* mock data */]),
            where: vi.fn().mockReturnThis(),
            equals: vi.fn().mockReturnThis(),
          }
        }
      }));

      const renderScreen = () => {
        return render(
          <BrowserRouter>
            <{Screen} />
          </BrowserRouter>
        );
      };

      describe('{Screen}', () => {
        // Test screen renders
        it('renders screen title', async () => {
          renderScreen();
          await waitFor(() => {
            expect(screen.getByRole('heading', { name: /{title}/i })).toBeInTheDocument();
          });
        });

        // Test key UI elements from spec
        it('displays {key_element} section', async () => {
          renderScreen();
          await waitFor(() => {
            expect(screen.getByTestId('{key-element}')).toBeInTheDocument();
          });
        });

        // Test data loading
        it('loads and displays data', async () => {
          renderScreen();
          await waitFor(() => {
            expect(screen.getByText(/{expected_data_text}/)).toBeInTheDocument();
          });
        });

        // Test primary user action from spec
        it('handles {primary_action} action', async () => {
          renderScreen();
          const actionButton = await screen.findByRole('button', { name: /{action}/i });
          await userEvent.click(actionButton);
          // Assert expected behavior
        });

        // Test navigation if applicable
        it('navigates to {destination} on {trigger}', async () => {
          renderScreen();
          // Test navigation flow
        });
      });

    // ═══════════════════════════════════════════════════════════
    // VERIFY RED: Run test, MUST fail
    // ═══════════════════════════════════════════════════════════

    RUN: npm run test:run -- src/screens/{app}/__tests__/{Screen}.test.tsx

    VERIFY test fails with expected error:
      Expected: "Cannot find module '../{Screen}'" OR
                "Screen is not defined" OR
                "Unable to find element"

      IF test PASSES:
        ❌ ERROR: Test passed without implementation
        DELETE test, REWRITE to actually test the screen

    LOG: "✅ RED phase complete: Test fails as expected"

    // ═══════════════════════════════════════════════════════════
    // PHASE 2: GREEN - Write Minimal Implementation
    // ═══════════════════════════════════════════════════════════

    CREATE prototype/src/screens/{app}/{Screen}.tsx:
      import React, { useState, useEffect } from 'react';
      import { useLiveQuery } from 'dexie-react-hooks';
      import { db } from '../../db/database';
      import { /* components */ } from '../../components';

      export const {Screen}: React.FC = () => {
        // MINIMAL state to pass tests
        // MINIMAL data queries
        // MINIMAL event handlers

        return (
          // MINIMAL layout to pass tests
          // Add data-testid for test queries
        );
      };

    // ═══════════════════════════════════════════════════════════
    // VERIFY GREEN: Run test, MUST pass
    // ═══════════════════════════════════════════════════════════

    RUN: npm run test:run -- src/screens/{app}/__tests__/{Screen}.test.tsx

    VERIFY test passes:
      IF test FAILS:
        Fix implementation (NOT the test)
        Re-run until pass

      IF test PASSES:
        LOG: "✅ GREEN phase complete: Test passes"

    // ═══════════════════════════════════════════════════════════
    // PHASE 3: REFACTOR - Complete the screen, stay green
    // ═══════════════════════════════════════════════════════════

    REFACTOR implementation:
      - Complete layout from spec
      - Add all components per spec
      - Implement all interactions
      - Add responsive breakpoints
      - Apply design tokens

    RUN: npm run test:run -- src/screens/{app}/__tests__/{Screen}.test.tsx

    VERIFY still passes after refactor

    // ═══════════════════════════════════════════════════════════
    // RECORD: Track TDD cycle completion
    // ═══════════════════════════════════════════════════════════

    APPEND to tdd_evidence[]:
      {
        screen: "{Screen}",
        app: "{app}",
        test_file: "src/screens/{app}/__tests__/{Screen}.test.tsx",
        impl_file: "src/screens/{app}/{Screen}.tsx",
        red_verified: true,
        green_verified: true,
        refactor_verified: true,
        timestamp: NOW()
      }
```

### Step 6.5: Validate ALL Discovery Screens Have Code (CRITICAL - BLOCKING)

> **CRITICAL**: This step ensures 100% screen implementation coverage from Discovery → Code.

```
// ═══════════════════════════════════════════════════════════
// MANDATORY: Validate All Discovery Screens Have React Code
// ═══════════════════════════════════════════════════════════

LOAD traceability/screen_registry.json → screen_registry
discovery_screens = screen_registry.discovery_screens

// Track screens that have React code
screens_with_code = []
screens_missing_code = []

FOR each screen in discovery_screens:
  screen_id = screen.id  // M-01, D-01, etc.

  // Find React component file
  // Check multiple possible locations based on platform
  IF screen.platform == "mobile":
    search_paths = [
      "prototype/src/screens/mobile/**/*.tsx",
      "prototype/src/screens/operator/**/*.tsx"
    ]
  ELSE:
    search_paths = [
      "prototype/src/screens/desktop/**/*.tsx",
      "prototype/src/screens/supervisor/**/*.tsx",
      "prototype/src/screens/manager/**/*.tsx"
    ]

  // Search for file matching screen ID or name
  found = false
  FOR each path in search_paths:
    files = GLOB(path)
    FOR each file in files:
      IF file_name contains screen.id OR
         file_name contains normalize(screen.name):
        found = true
        BREAK

  IF found:
    APPEND screen to screens_with_code[]
    UPDATE screen_registry.traceability[screen_id].code_status = "complete"
  ELSE:
    APPEND screen to screens_missing_code[]
    UPDATE screen_registry.traceability[screen_id].code_status = "missing"

// Update coverage metrics
screen_registry.screen_coverage.code_generated = screens_with_code.length

// ═══════════════════════════════════════════════════════════
// BLOCKING CHECK: All Discovery screens MUST have React code
// ═══════════════════════════════════════════════════════════

IF screens_missing_code.length > 0:
  ═══════════════════════════════════════════════════════════════
  ❌ BLOCKING: Screen Code Coverage Incomplete
  ═══════════════════════════════════════════════════════════════

  Discovery screens: {discovery_screens.length}
  Screens with code: {screens_with_code.length}
  Screens MISSING code: {screens_missing_code.length}

  ┌─────────────────────────────────────────────────────────────┐
  │  MISSING REACT COMPONENTS                                    │
  ├─────────────────────────────────────────────────────────────┤
  │  ID     │ Name                    │ Priority │ Platform      │
  ├─────────────────────────────────────────────────────────────┤
  FOR each screen in screens_missing_code:
  │  {id}   │ {name}                  │ {prio}   │ {platform}    │
  └─────────────────────────────────────────────────────────────┘

  ACTION REQUIRED:
  Generate React components for ALL missing screens before
  proceeding. Each screen from Discovery MUST have a .tsx file.

  How would you like to proceed?
  1. "generate missing" - Generate React code for missing screens
  2. "show specs" - Display screen specs needing implementation
  3. "abort" - Stop code generation

  ═══════════════════════════════════════════════════════════════

  WAIT for user response
  DO NOT proceed to Step 7 until ALL screens have code

ELSE:
  ═══════════════════════════════════════════════════════════════
  ✅ Screen Code Coverage: 100%
  ═══════════════════════════════════════════════════════════════

  All {discovery_screens.length} Discovery screens have React code:

  Mobile: {mobile_count} screens
  Desktop: {desktop_count} screens

  ═══════════════════════════════════════════════════════════════

// Save updated registry
WRITE screen_registry → traceability/screen_registry.json

LOG: "📊 Screen Code Traceability: {screens_with_code.length}/{discovery_screens.length} (100%)"
```

### Step 7: Generate Routing & App Shell
```
CREATE prototype/src/App.tsx:
  import React from 'react';
  import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
  
  // Import screens
  import { RecruiterDashboard } from './screens/recruiter/RecruiterDashboard';
  import { CandidatePipeline } from './screens/recruiter/CandidatePipeline';
  // ... all screens ...
  
  export const App: React.FC = () => {
    return (
      <BrowserRouter>
        <Routes>
          {/* Default redirect */}
          <Route path="/" element={<Navigate to="/recruiter/dashboard" />} />
          
          {/* Recruiter App */}
          <Route path="/recruiter/dashboard" element={<RecruiterDashboard />} />
          <Route path="/recruiter/pipeline" element={<CandidatePipeline />} />
          <Route path="/recruiter/candidates/:id" element={<CandidateProfile />} />
          
          {/* Hiring Manager App */}
          <Route path="/hiring-manager/triage" element={<TriageQueue />} />
          
          {/* ... all routes ... */}
        </Routes>
      </BrowserRouter>
    );
  };

CREATE prototype/src/main.tsx:
  import React from 'react';
  import ReactDOM from 'react-dom/client';
  import { App } from './App';
  import { seedDatabase } from './db/seed';
  import './styles/tokens.css';
  import './styles/global.css';
  
  // Seed database on first load
  seedDatabase().then(() => {
    ReactDOM.createRoot(document.getElementById('root')!).render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
  });
```

### Step 8: Generate Motion & Interactions
```
READ 03-interactions/motion-system.md
READ 03-interactions/micro-interactions.md

ADD motion tokens to prototype/src/styles/tokens.css:
  :root {
    /* Animation Durations */
    --duration-instant: 0ms;
    --duration-fast: 100ms;
    --duration-normal: 200ms;
    --duration-slow: 300ms;
    
    /* Easings */
    --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
    --ease-in: cubic-bezier(0.4, 0, 1, 1);
    --ease-out: cubic-bezier(0, 0, 0.2, 1);
  }

ADD transitions to components:
  .button {
    transition: 
      background-color var(--duration-fast) var(--ease-default),
      transform var(--duration-instant);
  }
  
  .card {
    transition: box-shadow var(--duration-normal) var(--ease-out);
  }
```

### Step 9: Validate Build & Tests (REQUIRED)

**This step enforces TDD completion and build validation.**

```
RUN in prototype/:

  // ═══════════════════════════════════════════════════════════
  // STEP 9.0: Pre-Flight Dependency Validation
  // ═══════════════════════════════════════════════════════════

  VALIDATE component library dependencies:

  READ manifest = ../.claude/templates/component-library/manifests/dependencies.json
  READ package_json = prototype/package.json

  required_deps = manifest.categories.required.dependencies
  missing_deps = []

  FOR each dep in required_deps:
    IF dep NOT IN package_json.dependencies:
      APPEND dep to missing_deps[]

  IF missing_deps.length > 0:
    ═══════════════════════════════════════════
    ❌ MISSING COMPONENT LIBRARY DEPENDENCIES
    ═══════════════════════════════════════════

    The following required dependencies are missing from package.json:

    FOR each dep in missing_deps:
      • {dep} ({required_deps[dep].version})
        Reason: {required_deps[dep].reason}
        Used in: {required_deps[dep].used_in}

    HOW TO FIX:
    Add these dependencies to prototype/package.json:

    "dependencies": {
      ...existing deps...
      FOR each dep in missing_deps:
        "{dep}": "{required_deps[dep].version}",
    }

    Then re-run this step.

    SOURCE: .claude/templates/component-library/manifests/dependencies.json
    ═══════════════════════════════════════════

    BLOCK further execution
    REQUIRE manual fix

  LOG: "✅ Component library dependencies validated - all required deps present"

  // ═══════════════════════════════════════════════════════════
  // STEP 9.1: Install Dependencies
  // ═══════════════════════════════════════════════════════════

  npm install

  // ═══════════════════════════════════════════════════════════
  // STEP 9.2: Run ALL Tests (TDD Verification)
  // ═══════════════════════════════════════════════════════════

  npm run test:run

  CAPTURE:
    - Total tests
    - Passed tests
    - Failed tests
    - Test coverage (if available)

  IF any tests fail:
    ═══════════════════════════════════════════
    ❌ TESTS FAILED
    ═══════════════════════════════════════════

    {failed_count}/{total_count} tests failed

    Failed tests:
    • {list failed tests with error messages}

    How would you like to proceed?
    1. "fix" - Debug and fix failing tests
    2. "show" - Display full test output
    3. "skip" - Continue without passing tests (NOT RECOMMENDED)
    ═══════════════════════════════════════════

    WAIT for user response

  // ═══════════════════════════════════════════════════════════
  // STEP 9.3: Verify TDD Evidence
  // ═══════════════════════════════════════════════════════════

  FOR each component in 01-components/:
    test_file = "src/components/{category}/__tests__/{Component}.test.tsx"

    IF test_file does NOT exist:
      APPEND to tdd_violations[]:
        "Component {Component} has no test file"

  FOR each screen in 02-screens/:
    test_file = "src/screens/{app}/__tests__/{Screen}.test.tsx"

    IF test_file does NOT exist:
      APPEND to tdd_violations[]:
        "Screen {Screen} has no test file"

  IF tdd_violations.length > 0:
    ═══════════════════════════════════════════
    ❌ TDD VIOLATIONS DETECTED
    ═══════════════════════════════════════════

    The following components/screens lack tests:
    {list violations}

    This violates the TDD Iron Law.

    How would you like to proceed?
    1. "generate tests" - Create missing test files
    2. "show evidence" - Display TDD tracking log
    3. "acknowledge" - Continue with documented violations
    ═══════════════════════════════════════════

    WAIT for user response

  // ═══════════════════════════════════════════════════════════
  // STEP 9.4: TypeScript Check
  // ═══════════════════════════════════════════════════════════

  npx tsc --noEmit

  IF typescript errors:
    LOG errors, WAIT for user decision

  // ═══════════════════════════════════════════════════════════
  // STEP 9.5: Lint Check
  // ═══════════════════════════════════════════════════════════

  npm run lint

  IF lint errors:
    LOG errors, WAIT for user decision

  // ═══════════════════════════════════════════════════════════
  // STEP 9.6: Build
  // ═══════════════════════════════════════════════════════════

  npm run build

  IF build fails:
    ═══════════════════════════════════════════
    ❌ BUILD FAILED
    ═══════════════════════════════════════════

    Error: {error_message}

    How would you like to proceed?
    1. "fix" - Attempt to fix automatically
    2. "show errors" - Display full error log
    3. "continue" - Skip build validation
    ═══════════════════════════════════════════

    WAIT for user response

  // ═══════════════════════════════════════════════════════════
  // STEP 9.7: Record Validation Results
  // ═══════════════════════════════════════════════════════════

  validation_results = {
    tests: {
      total: test_count,
      passed: passed_count,
      failed: failed_count,
      coverage: coverage_percent
    },
    tdd: {
      components_with_tests: count,
      screens_with_tests: count,
      violations: tdd_violations
    },
    typescript: {
      errors: 0
    },
    lint: {
      errors: 0
    },
    build: {
      success: true
    }
  }

VERIFY ALL:
  - All tests pass
  - No TDD violations (or acknowledged)
  - No TypeScript errors
  - No lint errors
  - Build output generated
```

### Step 10: Bundle to HTML Artifact (Phase 5 Enhancement - Optional)

> **web-artifacts-builder Integration**: Bundle prototype to single HTML file for sharing.

```
// ═══════════════════════════════════════════════════════════
// PHASE 5: ARTIFACT BUNDLING (if selected)
// ═══════════════════════════════════════════════════════════

IF STACK_CONFIG.bundle_to_artifact == true:

  LOG: "📦 Bundling prototype to single HTML artifact..."

  // Step 10.1: Run bundle script
  RUN in prototype/:
    bash scripts/bundle-artifact.sh

  // The script performs:
  // 1. Installs bundling dependencies (parcel, html-inline)
  // 2. Creates .parcelrc config with path alias support
  // 3. Builds with Parcel (no source maps)
  // 4. Inlines all assets into single HTML

  // Step 10.2: Verify bundle created
  IF bundle.html exists:
    LOG: "✅ Bundle created: prototype/bundle.html"

    bundle_size = GET file size of bundle.html

    ═══════════════════════════════════════════════════════════════
    📦 ARTIFACT BUNDLE CREATED
    ═══════════════════════════════════════════════════════════════

    File: prototype/bundle.html
    Size: {bundle_size}

    This is a self-contained HTML file with all JavaScript, CSS,
    and dependencies inlined. You can:

    1. Share directly in conversations
    2. Host on any static server
    3. Open locally in a browser

    ═══════════════════════════════════════════════════════════════

    // Copy to outputs
    COPY bundle.html to outputs/prototype-artifact.html

  ELSE:
    ═══════════════════════════════════════════════════════════════
    ⚠️ BUNDLE FAILED
    ═══════════════════════════════════════════════════════════════

    The artifact bundle could not be created.

    Common issues:
    1. Missing index.html in root directory
    2. Build errors in source code
    3. Missing dependencies

    How would you like to proceed?
    1. "debug" - Show bundle error logs
    2. "skip" - Continue without bundle
    3. "retry" - Attempt bundle again
    ═══════════════════════════════════════════════════════════════

    WAIT for user response

ELSE:
  LOG: "Skipping artifact bundling (not selected)"
```

### Step 10.5: Auto-Invoke Decomposition
```
LOG: "Auto-triggering Decomposition (code structure finalized)"

INVOKE Prototype_Decomposition:
  MODE: merge
  TRIGGER: "codegen_completed"
```

### Step 11: Verification Gate (MANDATORY)

> **See: ../VERIFICATION_GATE.md for full pattern**

```
EXECUTE verification_gate:

  // 1. IDENTIFY verification commands
  verification_commands = [
    "test -s prototype/package.json",
    "test -s prototype/src/App.tsx",
    "test -s prototype/src/main.tsx",
    "cd prototype && npm run test:run",
    "cd prototype && npx tsc --noEmit",
    "cd prototype && npm run build"
  ]

  // 2. RUN all verifications
  failures = []

  FOR each command in verification_commands:
    result = EXECUTE(command)
    CAPTURE output and exit_code

    IF exit_code != 0:
      LOG: "VERIFICATION FAILED: {command}"
      APPEND to failures[]

  // 3. READ results
  total_checks = verification_commands.length
  passed_checks = total_checks - failures.length

  // 4. VERIFY success
  IF failures.length > 0:
    ═══════════════════════════════════════════
    ❌ VERIFICATION GATE FAILED
    ═══════════════════════════════════════════

    {passed_checks}/{total_checks} checks passed

    Failures:
    {list failures with outputs}

    CANNOT mark codegen phase complete.

    How would you like to proceed?
    1. "fix: [issue]" - Address specific failure
    2. "retry" - Re-run verification
    3. "investigate" - Show detailed diagnostics
    ═══════════════════════════════════════════

    WAIT for user response
    DO NOT proceed to "Update Progress"

  ELSE:
    LOG: "✅ VERIFICATION PASSED: {total_checks}/{total_checks} checks"

    verification_evidence = {
      checks_run: total_checks,
      checks_passed: total_checks,
      outputs_verified: [
        "prototype/package.json",
        "prototype/src/App.tsx",
        "prototype/src/main.tsx"
      ],
      tests_passed: true,
      typescript_clean: true,
      build_success: true,
      timestamp: NOW()
    }

    // 5. ONLY NOW proceed to Update Progress
    PROCEED to "Update Progress" step
```

### Step 12: Update Progress (Atomic Updates)

> **Phase 4 Enhancement**: Uses ProgressLock for atomic, corruption-proof updates

```python
# IMPORT progress lock utility
from progress_lock import ProgressLock

# UPDATE progress with atomic file locking
with ProgressLock('prototype') as progress:
    # All updates happen atomically
    # Automatically saved on exit, rolled back on exception
    progress['phases']['codegen']['status'] = 'complete'
    progress['phases']['codegen']['completed_at'] = datetime.now().isoformat()
    progress['phases']['codegen']['outputs'] = [
        "prototype/package.json",
        "prototype/src/components/**/*.tsx",
        "prototype/src/components/**/__tests__/*.test.tsx",
        "prototype/src/screens/**/*.tsx",
        "prototype/src/screens/**/__tests__/*.test.tsx",
        "prototype/src/db/*.ts",
        "prototype/src/styles/*.css"
    ]
    progress['phases']['codegen']['validation'] = {
        'status': 'passed',
        'build_success': True,
        'tests_passed': True,
        'typescript_errors': 0,
        'lint_errors': 0
    }
    progress['phases']['codegen']['tdd'] = {
        'components_with_tests': components_with_tests_count,
        'screens_with_tests': screens_with_tests_count,
        'red_green_refactor_verified': True,
        'violations': []
    }
    progress['phases']['codegen']['verification'] = {
        'gate_passed': True,
        'checks_run': checks_run_count,
        'checks_passed': checks_passed_count,
        'verified_at': datetime.now().isoformat()
    }
    progress['phases']['codegen']['metrics'] = {
        'components_generated': components_count,
        'screens_generated': screens_count,
        'tests_generated': tests_count,
        'lines_of_code': loc_count,
        'test_coverage_percent': coverage_percent
    }
    # Lock released and changes saved automatically here
```

**Benefits**:
- ✅ Prevents progress.json corruption on build failure
- ✅ Automatic rollback if exception occurs during code generation
- ✅ File locking prevents concurrent write conflicts
- ✅ Backup created before each update

---

## Output Files (REQUIRED)

| Path | Purpose | Blocking? |
|------|---------|-----------|
| `package.json` | Project config | ✅ Yes |
| `src/styles/tokens.css` | Design tokens | ✅ Yes |
| `src/db/*.ts` | Database layer | ✅ Yes |
| `src/components/**/*.tsx` | All components | ✅ Yes |
| `src/screens/**/*.tsx` | All screens | ✅ Yes |
| `src/App.tsx` | Routing | ✅ Yes |
| `src/main.tsx` | Entry point | ✅ Yes |
| Build succeeds | Validation | ✅ Yes |

---

## Progress.json Update

```json
{
  "phases": {
    "codegen": {
      "status": "complete",
      "completed_at": "2024-12-13T14:30:00Z",
      "outputs": [
        "prototype/**/*"
      ],
      "validation": {
        "status": "passed",
        "build_success": true,
        "typescript_errors": 0,
        "lint_errors": 0
      },
      "metrics": {
        "components_generated": 42,
        "screens_generated": 15,
        "lines_of_code": 8500
      }
    }
  }
}
```
