---
description: Run comprehensive QA testing with Playwright and validation
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-qa started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /prototype-qa ended '{"stage": "prototype"}'
---


# /prototype-qa - QA Testing & UI Audit (Phases 13-14)

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "prototype"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /prototype-qa instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Assembly-First and traceability rules:

```bash
# Assembly-First rules (loaded automatically in Prototype stage)
/_assembly_first_rules

# Traceability rules for ID management
/rules-traceability
```

## Arguments

- `$ARGUMENTS` - Required: `<SystemName>` or path to `Prototype_<SystemName>/`

## Prerequisites

- Phase 12 completed: Working prototype exists
- Checkpoint 12 passed (or with documented issues)

## Skills Used

Read BEFORE execution:
- `.claude/skills/Prototype_QA/SKILL.md` (Phase 13)
- `.claude/skills/Prototype_UIAudit/SKILL.md` (Phase 14)

## Execution Flow

---

### Phase 13: QA Testing (Checkpoint 13)

#### Step 13.1: Load Inputs

Read:
- `_state/requirements_registry.json` (acceptance criteria)
- `02-screens/screen-index.md` (screen list)
- `02-screens/*/interactions.md` (expected behaviors)

#### Step 13.2: Update Progress

```json
{
  "current_phase": 13,
  "phases": {
    "qa": {
      "status": "in_progress",
      "started_at": "<timestamp>"
    }
  }
}
```

#### Step 13.3: Execute Prototype_QA Skill

1. **Verify Build Status**:

   ```bash
   cd Prototype_<SystemName>/prototype
   npm run build
   ```

   If build fails, document errors.

2. **Start Development Server**:

   ```bash
   npm run dev &
   # Wait for server to start
   ```

3. **Run Functional Tests**:

   For each screen and requirement:

   | Test | Check |
   |------|-------|
   | Page Loads | No console errors |
   | Navigation | All routes accessible |
   | Components Render | No missing elements |
   | Data Display | Mock data shows correctly |
   | Forms | Submit without errors |
   | Modals | Open and close correctly |
   | Responsive | Works at all breakpoints |

4. **Test User Flows**:

   Test each critical user flow from requirements:

   | Flow | Steps | Expected Result |
   |------|-------|-----------------|
   | View Dashboard | Navigate to / | Stats and activity visible |
   | View Inventory | Click Inventory nav | List loads with items |
   | View Item Detail | Click item row | Detail page shows |
   | Move Stock | Click Move button | Form opens |

5. **Accessibility Testing**:

   ```bash
   # Run axe-core via Playwright (if available)
   npx playwright test --grep accessibility
   ```

   Or manual checks:
   - Keyboard navigation works
   - Focus indicators visible
   - Screen reader announces correctly

6. **Document Issues**:

   For each issue found:
   ```markdown
   ### Issue QA-001

   - **Severity:** Critical / Major / Minor
   - **Screen:** Dashboard
   - **Component:** Stat Card
   - **Description:** Value not displaying correctly
   - **Steps to Reproduce:**
     1. Navigate to dashboard
     2. Observe stat cards
   - **Expected:** Shows "150 items"
   - **Actual:** Shows "undefined"
   - **Requirement:** US-001
   ```

#### Step 13.4: Generate QA Report

Create `05-validation/qa-report.md`:

```markdown
# QA Report

## Overview

| Metric | Value |
|--------|-------|
| Date | <YYYY-MM-DD> |
| Prototype | Prototype_<SystemName> |
| Build Status | ✅ Success / ❌ Failed |
| Tests Run | N |
| Passed | N |
| Failed | N |
| Pass Rate | N% |

## Build Summary

```
Build Status: Success
Build Time: 12.3s
Warnings: 3
Errors: 0
```

## Test Results by Screen

### Dashboard (SCR-001)

| Test | Status | Notes |
|------|--------|-------|
| Page Loads | ✅ Pass | |
| Stats Display | ✅ Pass | |
| Activity Feed | ✅ Pass | |
| Low Stock Table | ✅ Pass | |
| Navigation | ✅ Pass | |

### Inventory List (SCR-002)

| Test | Status | Notes |
|------|--------|-------|
| Page Loads | ✅ Pass | |
| Table Renders | ✅ Pass | |
| Pagination | ⚠️ Warn | Jumps on click |
| Search | ✅ Pass | |
| Filter | ❌ Fail | Filter dropdown not opening |

## Requirements Coverage

| Requirement | Screen | Status |
|-------------|--------|--------|
| US-001 | Dashboard | ✅ Verified |
| US-002 | Dashboard | ✅ Verified |
| US-003 | Inventory List | ⚠️ Partial |
| US-004 | Inventory List | ❌ Blocked |

## Issues Found

### Critical (0)

None

### Major (2)

#### QA-001: Filter dropdown not opening
- Screen: Inventory List
- Component: Filter
- Requirement: US-003

#### QA-002: Pagination state not persisting
- Screen: Inventory List
- Component: Pagination
- Requirement: US-004

### Minor (3)

...

## Accessibility Results

| Check | Status |
|-------|--------|
| Keyboard Navigation | ✅ Pass |
| Focus Indicators | ✅ Pass |
| Color Contrast | ✅ Pass |
| Screen Reader | ⚠️ Minor issues |

## Recommendations

1. Fix filter dropdown click handler
2. Add pagination state to URL
3. Review screen reader announcements

## Conclusion

**Overall Status:** ⚠️ Pass with Issues

The prototype is functional for primary user flows. Two major issues require attention before handoff.
```

#### Step 13.5: Validate Checkpoint 13

```bash
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 13 --dir Prototype_<SystemName>/
```

**Validation Criteria**:
- `05-validation/qa-report.md` exists
- Report has test results
- Pass rate documented
- Issues categorized by severity

#### Step 13.6: Update Progress

Mark phase 13 completed, move to phase 14.

---

### Phase 14: UI Audit (Checkpoint 14)

#### Step 14.1: Update Progress

```json
{
  "current_phase": 14,
  "phases": {
    "ui_audit": {
      "status": "in_progress",
      "started_at": "<timestamp>"
    }
  }
}
```

#### Step 14.2: Execute Prototype_UIAudit Skill

1. **Capture Screenshots**:

   Use Playwright to capture screenshots at key breakpoints:

   ```javascript
   // capture-screenshots.js
   const { chromium } = require('playwright');

   const screens = [
     { path: '/', name: 'dashboard' },
     { path: '/inventory', name: 'inventory-list' },
     { path: '/inventory/1', name: 'inventory-detail' },
     // ...
   ];

   const breakpoints = [
     { width: 375, height: 812, name: 'mobile' },
     { width: 768, height: 1024, name: 'tablet' },
     { width: 1280, height: 800, name: 'desktop' },
   ];

   async function captureScreenshots() {
     const browser = await chromium.launch();

     for (const bp of breakpoints) {
       const context = await browser.newContext({
         viewport: { width: bp.width, height: bp.height }
       });
       const page = await context.newPage();

       for (const screen of screens) {
         await page.goto(`http://localhost:5173${screen.path}`);
         await page.screenshot({
           path: `screenshots/${screen.name}-${bp.name}.png`,
           fullPage: true
         });
       }

       await context.close();
     }

     await browser.close();
   }
   ```

   Save to `05-validation/screenshots/`.

2. **Compare Against Specs**:

   For each screen, compare:
   - Layout matches `layout.md`
   - Components match `components.md`
   - Spacing follows design tokens
   - Colors match design system
   - Typography matches spec

3. **Document Visual Issues**:

   ```markdown
   ### Visual Issue UI-001

   - **Screen:** Dashboard
   - **Breakpoint:** Mobile
   - **Element:** Header
   - **Expected:** Logo and hamburger only
   - **Actual:** Search bar overlapping
   - **Screenshot:** screenshots/dashboard-mobile.png
   ```

4. **Generate Traceability Matrix**:

   Link all artifacts from pain points to tests.

#### Step 14.3: Generate Folder README

Create `05-validation/README.md`:

```markdown
# 05-validation/ - Validation & Quality Assurance

## Purpose

This folder contains all quality assurance artifacts for the prototype validation process.

## Contents

| File | Purpose |
|------|---------|
| `qa-report.md` | Functional testing results and issue log |
| `ui-audit-report.md` | Visual compliance and accessibility audit |
| `TRACEABILITY_MATRIX.md` | End-to-end requirement traceability |
| `screenshots/` | Visual regression captures at all breakpoints |

## Validation Process

1. **Build Verification** - Confirm prototype compiles without errors
2. **Functional Testing** - Test all P0 requirements against acceptance criteria
3. **Accessibility Audit** - WCAG AA compliance verification
4. **Visual Audit** - Design token and layout compliance
5. **Traceability Verification** - End-to-end chain validation

## Related Artifacts

- Requirements: `_state/requirements_registry.json`
- Screens: `02-screens/screen-index.md`
- Components: `01-components/component-index.md`
```

#### Step 14.4: Generate UI Audit Report

Create `05-validation/ui-audit-report.md`:

```markdown
# UI Audit Report

## Overview

| Metric | Value |
|--------|-------|
| Date | <YYYY-MM-DD> |
| Screens Audited | N |
| Breakpoints Tested | 3 |
| Visual Issues | N |

## Screenshot Inventory

| Screen | Mobile | Tablet | Desktop |
|--------|--------|--------|---------|
| Dashboard | ✅ | ✅ | ✅ |
| Inventory List | ✅ | ✅ | ✅ |
| Inventory Detail | ✅ | ✅ | ✅ |

Screenshots location: `05-validation/screenshots/`

## Design Compliance

### Color System

| Check | Status |
|-------|--------|
| Primary color usage | ✅ Correct |
| Semantic colors | ✅ Correct |
| Neutral palette | ✅ Correct |
| Contrast ratios | ✅ 4.5:1+ |

### Typography

| Check | Status |
|-------|--------|
| Font family | ✅ Inter |
| Heading sizes | ✅ Per spec |
| Body text | ✅ 16px |
| Line heights | ✅ Per spec |

### Spacing

| Check | Status |
|-------|--------|
| Component padding | ✅ Per tokens |
| Section margins | ⚠️ Minor variance |
| Grid alignment | ✅ Per spec |

### Components

| Component | Visual Match | Notes |
|-----------|--------------|-------|
| Button | ✅ | |
| Input | ✅ | |
| Card | ✅ | |
| Table | ⚠️ | Border color slightly off |
| Modal | ✅ | |

## Responsive Audit

### Mobile (375px)

| Screen | Status | Issues |
|--------|--------|--------|
| Dashboard | ⚠️ | Header overflow |
| Inventory | ✅ | |

### Tablet (768px)

| Screen | Status | Issues |
|--------|--------|--------|
| Dashboard | ✅ | |
| Inventory | ✅ | |

### Desktop (1280px)

| Screen | Status | Issues |
|--------|--------|--------|
| Dashboard | ✅ | |
| Inventory | ✅ | |

## Visual Issues

### Issue UI-001: Header overflow on mobile
- Severity: Minor
- Screenshot: `dashboard-mobile.png`
- Fix: Reduce padding, hide search

## Recommendations

1. Fix mobile header overflow
2. Adjust table border color to match tokens
3. Review section spacing on inventory page
```

#### Step 14.4: Generate Final Reports

Create `reports/ARCHITECTURE.md`:

```markdown
# Architecture Overview

## System: <SystemName>

## Technology Stack

| Layer | Technology |
|-------|------------|
| Framework | React 18 |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| Routing | React Router v6 |
| State | React Query |
| UI Components | Custom + Headless UI |

## Folder Structure

```
prototype/
├── src/
│   ├── components/     # Reusable UI components
│   ├── pages/          # Route components
│   ├── hooks/          # Custom React hooks
│   ├── lib/            # Utilities
│   ├── styles/         # Global styles
│   └── data/           # Mock data
```

## Key Decisions

1. **React + TypeScript**: Type safety and IDE support
2. **Tailwind CSS**: Rapid styling with design tokens
3. **Headless UI**: Accessible primitives for complex components
4. **React Query**: Server state management

## Data Flow

```
User Action → Component → Hook → API (mock) → State → Re-render
```
```

Create `reports/README.md`:

```markdown
# Prototype README

## Quick Start

```bash
cd prototype
npm install
npm run dev
```

Open http://localhost:5173

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Production build
- `npm run preview` - Preview production build

## Project Structure

See `ARCHITECTURE.md` for details.

## Design System

Design tokens and specifications are in `00-foundation/`.

## Testing

QA report: `05-validation/qa-report.md`
UI audit: `05-validation/ui-audit-report.md`
```

Create `reports/TRACEABILITY_MATRIX.md`:

```markdown
# Traceability Matrix

## Pain Point → Requirement → Screen → Test

| Pain Point | JTBD | Requirement | Screen | Component | Test |
|------------|------|-------------|--------|-----------|------|
| PP-1.1 | JTBD-1.1 | US-001 | Dashboard | Stat Card | QA-T001 |
| PP-1.2 | JTBD-1.2 | US-002 | Dashboard | Activity | QA-T002 |
| PP-2.1 | JTBD-2.1 | US-003 | Inventory | Data Table | QA-T003 |

## Screen-to-Requirement Mapping

| Screen | Route | P0 Requirements |
|--------|-------|-----------------|
| Dashboard | `/` | US-001, US-002, US-005 |
| Inventory List | `/inventory` | US-003, US-006 |
| Inventory Detail | `/inventory/:id` | US-004, US-007 |

## Component-to-Requirement Mapping

| Component | Category | Requirements Addressed |
|-----------|----------|------------------------|
| Button | primitives | Core interaction (all) |
| StatCard | data-display | US-001 |
| DataTable | patterns | US-003, US-006 |

## Service-to-Requirement Mapping

| Service | Function | Requirements |
|---------|----------|--------------|
| inventoryService | getAll, getById, update | US-003, US-004 |
| stockMovementService | create, getHistory | US-007 |
| dashboardService | getStats, getActivity | US-001, US-002 |

## Hook-to-Requirement Mapping

| Hook | Purpose | Requirements |
|------|---------|--------------|
| useInventory | Fetch inventory data | US-003 |
| useStockMovement | Manage stock transactions | US-007 |
| useDashboardStats | Dashboard metrics | US-001 |

## Critical Path Verification

| Critical Path | Requirements | Status |
|---------------|--------------|--------|
| View Dashboard Stats | US-001, US-002 | ✅ Verified |
| List Inventory | US-003 | ✅ Verified |
| Stock Movement | US-007 | ✅ Verified |

## Change Request Implementations

| CR ID | Description | Requirements Affected | Status |
|-------|-------------|----------------------|--------|
| (none yet) | | | |

## Coverage Summary

| Category | Covered | Total | Percent |
|----------|---------|-------|---------|
| Pain Points | N | M | X% |
| JTBDs | N | M | X% |
| Requirements | N | M | X% |

## Traceability Complete

All P0 requirements have been traced from Pain Points → JTBD → User Stories → Screens → Components → Tests.
```

#### Step 14.5: Validate Checkpoint 14

```bash
python3 .claude/hooks/prototype_quality_gates.py --validate-checkpoint 14 --dir Prototype_<SystemName>/
```

**Validation Criteria**:
- `05-validation/ui-audit-report.md` exists
- `05-validation/screenshots/` has files
- `reports/ARCHITECTURE.md` exists
- `reports/README.md` exists
- `reports/TRACEABILITY_MATRIX.md` exists

#### Step 14.6: Update Progress

Mark phase 14 completed.

---

## Final Summary

```
═══════════════════════════════════════════════════════
  VALIDATION PHASES COMPLETE (13-14)
═══════════════════════════════════════════════════════

  Phase 13 - QA Testing:
  ├── Tests Run:           N
  ├── Pass Rate:           X%
  ├── Critical Issues:     N
  ├── Major Issues:        N
  └── Output:              05-validation/qa-report.md

  Phase 14 - UI Audit:
  ├── Screenshots:         N images
  ├── Visual Issues:       N
  ├── Design Compliance:   X%
  └── Outputs:
      • 05-validation/ui-audit-report.md
      • 05-validation/screenshots/
      • reports/ARCHITECTURE.md
      • reports/README.md
      • reports/TRACEABILITY_MATRIX.md

  Checkpoints:             13 ✅  14 ✅

═══════════════════════════════════════════════════════

  PROTOTYPE COMPLETE

  Output: Prototype_<SystemName>/

  To run: cd Prototype_<SystemName>/prototype && npm run dev

  Next Steps:
  • /prototype-export - Package for ProductSpecs
  • /prototype-feedback - Process change requests

═══════════════════════════════════════════════════════
```

## Outputs

| File/Folder | Phase | Purpose |
|-------------|-------|---------|
| `05-validation/qa-report.md` | 13 | QA test results |
| `05-validation/ui-audit-report.md` | 14 | Visual audit results |
| `05-validation/screenshots/` | 14 | Screen captures |
| `reports/ARCHITECTURE.md` | 14 | Technical overview |
| `reports/README.md` | 14 | Quick start guide |
| `reports/TRACEABILITY_MATRIX.md` | 14 | End-to-end tracing |

## Error Handling

| Error | Action |
|-------|--------|
| Prototype not building | Document in QA report, continue |
| Screenshot capture fails | Log, skip to next screen |
| Server won't start | Document, provide manual steps |

## Related Commands

| Command | Description |
|---------|-------------|
| `/prototype-build` | Run Phases 11-12 |
| `/prototype-export` | Package for ProductSpecs |
| `/prototype-feedback` | Process change requests |
| `/prototype` | Run full prototype |
