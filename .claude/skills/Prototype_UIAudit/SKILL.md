---
name: auditing-ui-compliance
description: Use when you need to perform a visual QA audit of an implemented prototype using automated screenshot capture (Playwright) and comparison reports.
model: haiku
allowed-tools: Read, Grep, Glob, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill auditing-ui-compliance started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill auditing-ui-compliance ended '{"stage": "prototype"}'
---

# Audit UI Compliance

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill auditing-ui-compliance instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_UIAudit
- **Version**: 2.3.1
- **Created**: 2024-12-13
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3

## Description
Visual QA audit of implemented prototype with AUTOMATED screenshot capture. Installs UI testing framework (Playwright), captures screenshots of all screens and modals, generates audit reports with before/after comparisons.

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

Perform visual QA audit of implemented prototype with **automated screenshot capture**. This skill MUST install a UI testing framework and programmatically capture all screenshots.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: Feature names and audit groupings shown below (e.g., "FEAT-001: Recruiter Pipeline") are examples from an ATS domain. Your actual audit features should be derived from your project's screens and requirements.

> **⚠️ AUTOMATED SCREENSHOTS REQUIRED**: This skill MUST install Playwright (or similar) and generate automation scripts to capture screenshots. Claude must NOT expect the user to manually capture screenshots.

## Output Structure (REQUIRED)

This skill MUST generate the following structure:

```
reports/
├── ui-audit/
│   ├── AUDIT_SUMMARY.md              # Overall audit summary
│   ├── {FEAT-NNN}-AUDIT-REPORT.md    # Per-feature audit reports
│   ├── screenshots/
│   │   ├── baseline/                 # BEFORE audit (initial capture)
│   │   │   ├── desktop/
│   │   │   │   ├── {app}--{screen}--default.png
│   │   │   │   ├── {app}--{screen}--{state}.png
│   │   │   │   └── {app}--{screen}--modal-{name}.png
│   │   │   ├── tablet/
│   │   │   └── mobile/
│   │   ├── current/                  # AFTER fixes (re-capture)
│   │   │   ├── desktop/
│   │   │   ├── tablet/
│   │   │   └── mobile/
│   │   └── diff/                     # Visual diff (if changes)
│   │       └── ...
│   └── ui-audit-report.json          # Machine-readable results

prototype/
├── playwright.config.ts              # Playwright configuration
├── tests/
│   └── screenshots/
│       ├── capture-all.spec.ts       # Main screenshot capture script
│       ├── capture-screens.spec.ts   # Screen-by-screen capture
│       └── capture-modals.spec.ts    # Modal/overlay capture
└── package.json                      # Updated with Playwright deps
```

---

## Screenshot Naming Convention (MANDATORY)

All screenshots MUST follow this naming pattern:

```
{app}--{screen}--{state}--{viewport}.png
```

| Part | Description | Examples |
|------|-------------|----------|
| `{app}` | App/portal name | `recruiter`, `candidate`, `admin` |
| `{screen}` | Screen name | `dashboard`, `pipeline`, `profile` |
| `{state}` | State or variant | `default`, `loading`, `empty`, `error`, `hover-card` |
| `{viewport}` | Implied by directory | `desktop/`, `tablet/`, `mobile/` |

### Examples

```
desktop/
├── recruiter--dashboard--default.png
├── recruiter--dashboard--loading.png
├── recruiter--dashboard--empty.png
├── recruiter--pipeline--default.png
├── recruiter--pipeline--drag-active.png
├── recruiter--pipeline--modal-confirm-reject.png
├── recruiter--pipeline--modal-move-stage.png
├── recruiter--profile--default.png
├── recruiter--profile--tab-activity.png
├── recruiter--profile--tab-documents.png
└── candidate--application--default.png
```

### Modal Screenshots

Modals MUST be captured with the naming pattern:
```
{app}--{screen}--modal-{modal-name}.png
```

Examples:
```
recruiter--pipeline--modal-confirm-reject.png
recruiter--pipeline--modal-add-candidate.png
recruiter--profile--modal-schedule-interview.png
admin--settings--modal-confirm-delete.png
```

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ _state/progress.json → verify QA passed
READ 05-validation/VALIDATION_REPORT.md → delivery status
READ 02-screens/SCREEN_SPECIFICATIONS_SUMMARY.md → screens to audit
READ 01-components/COMPONENT_LIBRARY_SUMMARY.md → components to verify
READ _state/screen_requirements_map.json → screen inventory

IF qa.delivery_status != "APPROVED":
  BLOCK: "QA must pass before UI Audit"
  
IF prototype not built:
  BLOCK: "Run CodeGen first"

EXTRACT screen inventory:
  FOR each app directory in 02-screens/:
    FOR each screen.md file:
      ADD to screens_to_audit[]
      EXTRACT modals/dialogs from screen spec
      ADD to modals_to_capture[]
```

### Step 2: Install UI Testing Framework (MANDATORY)
```
DETERMINE technology stack from prototype/:
  IF package.json exists:
    READ package.json
    DETECT framework (React, Vue, vanilla JS, etc.)

INSTALL Playwright:
  
  // Add to package.json devDependencies
  UPDATE prototype/package.json:
    {
      "devDependencies": {
        "@playwright/test": "^1.40.0",
        "playwright": "^1.40.0"
      },
      "scripts": {
        "test:screenshots": "playwright test tests/screenshots/",
        "test:screenshots:update": "playwright test tests/screenshots/ --update-snapshots",
        "screenshots:baseline": "playwright test tests/screenshots/capture-all.spec.ts --project=baseline",
        "screenshots:current": "playwright test tests/screenshots/capture-all.spec.ts --project=current"
      }
    }

  RUN: cd prototype && npm install

  // Install browsers
  RUN: cd prototype && npx playwright install chromium

CREATE prototype/playwright.config.ts:
```typescript
import { defineConfig, devices } from '@playwright/test';

// Port detection: Use environment variable or fallback to Vite default
const PORT = process.env.VITE_PORT || process.env.PORT || 5173;
const BASE_URL = `http://localhost:${PORT}`;

export default defineConfig({
  testDir: './tests/screenshots',
  outputDir: '../reports/ui-audit/screenshots',

  use: {
    baseURL: BASE_URL,
    screenshot: 'only-on-failure',
  },

  projects: [
    // Desktop - 1280x720
    {
      name: 'desktop',
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1280, height: 720 },
      },
    },
    // Tablet - 768x1024
    {
      name: 'tablet',
      use: {
        ...devices['iPad'],
        viewport: { width: 768, height: 1024 },
      },
    },
    // Mobile - 375x667
    {
      name: 'mobile',
      use: {
        ...devices['iPhone 13'],
        viewport: { width: 375, height: 667 },
      },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: BASE_URL,
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000, // 2 minutes for slow starts
  },
});
```
```

### Step 3: Generate Screenshot Capture Scripts (MANDATORY)
```
READ all screen specifications from 02-screens/
EXTRACT:
  - All screens with their routes/URLs
  - All modals/dialogs per screen
  - Key states to capture (loading, empty, error, etc.)
  - Interactive elements requiring hover/focus states

CREATE prototype/tests/screenshots/capture-all.spec.ts:
```typescript
import { test, expect, Page } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

// ES Module compatibility for __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Screenshot output configuration
const BASELINE_DIR = '../../../reports/ui-audit/screenshots/baseline';
const CURRENT_DIR = '../../../reports/ui-audit/screenshots/current';

// Determine output directory based on environment
const OUTPUT_DIR = process.env.SCREENSHOT_MODE === 'current' ? CURRENT_DIR : BASELINE_DIR;

// Screen definitions extracted from specs
const SCREENS = [
  // Recruiter App
  { app: 'recruiter', screen: 'dashboard', route: '/recruiter/dashboard' },
  { app: 'recruiter', screen: 'pipeline', route: '/recruiter/pipeline' },
  { app: 'recruiter', screen: 'profile', route: '/recruiter/candidates/:id', testId: 'cand-001' },
  
  // Candidate Portal
  { app: 'candidate', screen: 'dashboard', route: '/candidate/dashboard' },
  { app: 'candidate', screen: 'application', route: '/candidate/apply/:id', testId: 'pos-001' },
  
  // Hiring Manager App
  { app: 'hiring-manager', screen: 'triage', route: '/hiring-manager/triage' },
  { app: 'hiring-manager', screen: 'team-pipeline', route: '/hiring-manager/pipeline' },
  
  // Admin Panel
  { app: 'admin', screen: 'users', route: '/admin/users' },
  { app: 'admin', screen: 'settings', route: '/admin/settings' },
  
  // ... add all screens from specs
];

// Modal definitions
const MODALS = [
  { 
    app: 'recruiter', 
    screen: 'pipeline', 
    modal: 'confirm-reject',
    trigger: '[data-testid="reject-candidate-btn"]',
    waitFor: '[data-testid="confirm-reject-modal"]'
  },
  { 
    app: 'recruiter', 
    screen: 'pipeline', 
    modal: 'move-stage',
    trigger: '[data-testid="move-stage-btn"]',
    waitFor: '[data-testid="move-stage-modal"]'
  },
  { 
    app: 'recruiter', 
    screen: 'profile', 
    modal: 'schedule-interview',
    trigger: '[data-testid="schedule-interview-btn"]',
    waitFor: '[data-testid="schedule-modal"]'
  },
  // ... add all modals from specs
];

// States to capture for each screen
const STATES = ['default', 'loading', 'empty', 'error'];

// Helper to ensure directory exists
function ensureDir(dir: string) {
  const fullPath = path.join(__dirname, dir);
  if (!fs.existsSync(fullPath)) {
    fs.mkdirSync(fullPath, { recursive: true });
  }
}

// Helper to generate screenshot filename
function screenshotName(app: string, screen: string, state: string): string {
  return `${app}--${screen}--${state}.png`;
}

test.describe('Screenshot Capture - All Screens', () => {
  
  test.beforeAll(async () => {
    // Ensure output directories exist
    ['desktop', 'tablet', 'mobile'].forEach(viewport => {
      ensureDir(`${OUTPUT_DIR}/${viewport}`);
    });
  });

  for (const screenDef of SCREENS) {
    test(`Capture ${screenDef.app}/${screenDef.screen}`, async ({ page }, testInfo) => {
      const viewport = testInfo.project.name; // 'desktop', 'tablet', or 'mobile'
      const outputDir = path.join(__dirname, OUTPUT_DIR, viewport);
      
      // Navigate to screen
      let url = screenDef.route;
      if (screenDef.testId) {
        url = url.replace(':id', screenDef.testId);
      }
      await page.goto(url);
      
      // Wait for page to be fully loaded
      await page.waitForLoadState('networkidle');
      
      // Capture default state
      await page.screenshot({
        path: path.join(outputDir, screenshotName(screenDef.app, screenDef.screen, 'default')),
        fullPage: true,
      });
      
      // Capture loading state (if skeleton exists)
      // This requires triggering a refresh or navigation
      
      // Capture empty state (if data can be cleared)
      // Implementation depends on app architecture
      
      console.log(`✓ Captured: ${screenDef.app}/${screenDef.screen} (${viewport})`);
    });
  }
});

test.describe('Screenshot Capture - Modals', () => {
  
  for (const modalDef of MODALS) {
    test(`Capture modal: ${modalDef.app}/${modalDef.screen}/${modalDef.modal}`, async ({ page }, testInfo) => {
      const viewport = testInfo.project.name;
      const outputDir = path.join(__dirname, OUTPUT_DIR, viewport);
      
      // Navigate to screen containing modal
      const screenDef = SCREENS.find(s => s.app === modalDef.app && s.screen === modalDef.screen);
      if (!screenDef) {
        console.warn(`Screen not found for modal: ${modalDef.app}/${modalDef.screen}`);
        return;
      }
      
      await page.goto(screenDef.route);
      await page.waitForLoadState('networkidle');
      
      // Trigger modal
      const triggerElement = await page.$(modalDef.trigger);
      if (triggerElement) {
        await triggerElement.click();
        
        // Wait for modal to appear
        await page.waitForSelector(modalDef.waitFor, { state: 'visible' });
        await page.waitForTimeout(300); // Allow animations to complete
        
        // Capture modal
        await page.screenshot({
          path: path.join(outputDir, screenshotName(modalDef.app, modalDef.screen, `modal-${modalDef.modal}`)),
          fullPage: false, // Capture viewport only for modals
        });
        
        console.log(`✓ Captured modal: ${modalDef.app}/${modalDef.screen}/modal-${modalDef.modal} (${viewport})`);
        
        // Close modal (press Escape or click close button)
        await page.keyboard.press('Escape');
        await page.waitForTimeout(200);
      } else {
        console.warn(`Modal trigger not found: ${modalDef.trigger}`);
      }
    });
  }
});

test.describe('Screenshot Capture - Interactive States', () => {
  
  test('Capture hover states on pipeline cards', async ({ page }, testInfo) => {
    const viewport = testInfo.project.name;
    const outputDir = path.join(__dirname, OUTPUT_DIR, viewport);
    
    await page.goto('/recruiter/pipeline');
    await page.waitForLoadState('networkidle');
    
    // Hover over first card
    const firstCard = await page.$('[data-testid="candidate-card"]');
    if (firstCard) {
      await firstCard.hover();
      await page.waitForTimeout(200);
      
      await page.screenshot({
        path: path.join(outputDir, screenshotName('recruiter', 'pipeline', 'hover-card')),
        fullPage: true,
      });
    }
  });
  
  test('Capture drag state on pipeline', async ({ page }, testInfo) => {
    const viewport = testInfo.project.name;
    const outputDir = path.join(__dirname, OUTPUT_DIR, viewport);
    
    await page.goto('/recruiter/pipeline');
    await page.waitForLoadState('networkidle');
    
    // Start drag on first card
    const firstCard = await page.$('[data-testid="candidate-card"]');
    if (firstCard) {
      const box = await firstCard.boundingBox();
      if (box) {
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
        await page.mouse.down();
        await page.mouse.move(box.x + 200, box.y); // Drag right
        
        await page.screenshot({
          path: path.join(outputDir, screenshotName('recruiter', 'pipeline', 'drag-active')),
          fullPage: true,
        });
        
        await page.mouse.up();
      }
    }
  });
});
```

LOG to prompt_log.json:
  skill: "Prototype_UIAudit"
  step: "Step 3: Generate Screenshot Scripts"
  desired_outcome: "Generate Playwright scripts for automated screenshot capture"
  target: "prototype/tests/screenshots/*.spec.ts"
```

### Step 4: Run Baseline Screenshot Capture (BEFORE Audit)
```
LOG: "Capturing baseline screenshots (BEFORE audit)..."

RUN automated screenshot capture:
  cd prototype
  
  // Set environment for baseline capture
  SCREENSHOT_MODE=baseline npm run test:screenshots
  
  // Or run with Playwright directly
  npx playwright test tests/screenshots/capture-all.spec.ts \
    --project=desktop \
    --project=tablet \
    --project=mobile

VERIFY screenshots captured:
  COUNT files in reports/ui-audit/screenshots/baseline/desktop/
  COUNT files in reports/ui-audit/screenshots/baseline/tablet/
  COUNT files in reports/ui-audit/screenshots/baseline/mobile/
  
  IF any viewport has 0 screenshots:
    ═══════════════════════════════════════════
    ❌ SCREENSHOT CAPTURE FAILED
    ═══════════════════════════════════════════
    
    No screenshots captured for: {viewport}
    
    Possible issues:
    • Playwright not installed correctly
    • Dev server not running
    • Routes not matching
    
    Debug:
    1. Run: npx playwright test --debug
    2. Check: prototype/playwright.config.ts
    ═══════════════════════════════════════════
    
    WAIT for user response

LOG captured files:
  ✓ Baseline Desktop: {N} screenshots
  ✓ Baseline Tablet: {N} screenshots
  ✓ Baseline Mobile: {N} screenshots
  Total: {N} screenshots captured
```

### Step 5: Define Audit Features
```
GROUP screens into audit features based on app/functionality:

FOR each app directory in 02-screens/:
  CREATE feature:
    {
      "feature_id": "FEAT-{sequence}",
      "name": "{App Name}",
      "app": "{app-slug}",
      "screens": [/* screens in this app */],
      "modals": [/* modals in this app */],
      "screenshot_count": {
        "baseline": N,
        "expected": N
      }
    }

EXAMPLE:
  FEAT-001: Recruiter App
    - recruiter/dashboard
    - recruiter/pipeline
    - recruiter/profile
    - Modals: confirm-reject, move-stage, schedule-interview
    
  FEAT-002: Candidate Portal
    - candidate/dashboard
    - candidate/application
    - Modals: confirm-submit, withdraw-application
```

### Step 6: Perform Visual Audit Against Specs
```
FOR each feature:
  FOR each screen in feature:
    
    READ screen spec from 02-screens/{app}/{screen}.md
    READ baseline screenshot from screenshots/baseline/
    
    VERIFY against spec:
      - Layout matches spec grid
      - Components present as specified
      - Colors match design tokens
      - Typography matches spec
      - Spacing consistent with spec
      - Responsive behavior correct
    
    RECORD findings:
      {
        "screen": "{app}/{screen}",
        "viewport": "desktop|tablet|mobile",
        "checks": [
          { "check": "Layout", "expected": "3-column grid", "actual": "3-column grid", "status": "pass" },
          { "check": "Primary Button Color", "expected": "#3b82f6", "actual": "#3b82f6", "status": "pass" },
          { "check": "Card Spacing", "expected": "16px", "actual": "12px", "status": "fail", "severity": "minor" }
        ],
        "issues": [
          {
            "id": "UI-001",
            "severity": "minor",
            "description": "Card spacing 12px instead of 16px",
            "screenshot": "baseline/desktop/recruiter--pipeline--default.png",
            "line_in_spec": 45
          }
        ]
      }
```

### Step 7: Generate Per-Feature Audit Reports
```
FOR each feature:
  CREATE reports/ui-audit/{FEAT-NNN}-AUDIT-REPORT.md:
    # UI Audit: {Feature Name}
    
    **Feature ID:** {FEAT-NNN}
    **App:** {app-name}
    **Screens:** {screen-count}
    **Screenshots Captured:** {count}
    **Audit Date:** {timestamp}
    
    ---
    
    ## Screenshot Inventory
    
    ### Baseline Screenshots (Before Audit)
    
    | Screen | Desktop | Tablet | Mobile | Modals |
    |--------|---------|--------|--------|--------|
    | dashboard | ✅ | ✅ | ✅ | 0 |
    | pipeline | ✅ | ✅ | ✅ | 3 |
    | profile | ✅ | ✅ | ✅ | 2 |
    
    ### Screenshots by State
    
    | Screen | Default | Loading | Empty | Error | Hover | Drag |
    |--------|---------|---------|-------|-------|-------|------|
    | pipeline | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
    
    ---
    
    ## Visual Compliance Results
    
    ### Design Token Verification
    [... detailed checks ...]
    
    ### Issues Found
    
    #### [UI-001] Card spacing inconsistency
    - **Severity:** Minor
    - **Location:** recruiter/pipeline
    - **Expected:** 16px gap between cards
    - **Actual:** 12px gap
    - **Screenshot:** `baseline/desktop/recruiter--pipeline--default.png`
    - **Status:** Open
    
    ---
    
    ## Screenshots
    
    ### Desktop Views
    
    #### Dashboard
    ![Dashboard](./screenshots/baseline/desktop/recruiter--dashboard--default.png)
    
    #### Pipeline
    ![Pipeline Default](./screenshots/baseline/desktop/recruiter--pipeline--default.png)
    ![Pipeline Drag](./screenshots/baseline/desktop/recruiter--pipeline--drag-active.png)
    
    #### Modals
    ![Confirm Reject](./screenshots/baseline/desktop/recruiter--pipeline--modal-confirm-reject.png)
    
    ### Mobile Views
    [... mobile screenshots ...]
```

### Step 8: Fix Issues and Re-Capture (AFTER Audit)
```
IF issues found that require fixes:
  
  PROMPT user:
    ═══════════════════════════════════════════
    UI AUDIT: {N} Issues Found
    ═══════════════════════════════════════════
    
    Issues requiring attention:
    • UI-001: Card spacing (minor)
    • UI-002: Button color (minor)
    
    After fixes are applied, re-run screenshot capture?
    1. "capture" - Run AFTER screenshot capture
    2. "skip" - Proceed without re-capture
    3. "show issues" - List all issues
    ═══════════════════════════════════════════

  IF user selects "capture":
    
    RUN AFTER screenshot capture:
      cd prototype
      SCREENSHOT_MODE=current npm run test:screenshots
    
    COMPARE baseline vs current:
      FOR each screenshot in baseline/:
        IF corresponding file in current/:
          GENERATE visual diff if changed
          SAVE to screenshots/diff/
    
    UPDATE audit reports with:
      - AFTER screenshots
      - Visual diffs
      - Issue resolution status
```

### Step 9: Generate Audit Summary
```
CREATE reports/ui-audit/AUDIT_SUMMARY.md:
  # UI Audit Summary
  
  **Audit Date:** {timestamp}
  **Prototype Version:** {version}
  
  ---
  
  ## Screenshot Capture Summary
  
  | Phase | Desktop | Tablet | Mobile | Total |
  |-------|---------|--------|--------|-------|
  | Baseline (Before) | {N} | {N} | {N} | {N} |
  | Current (After) | {N} | {N} | {N} | {N} |
  | Diffs Generated | {N} | {N} | {N} | {N} |
  
  ### Screens Captured
  
  | App | Screens | Modals | States | Total Screenshots |
  |-----|---------|--------|--------|-------------------|
  | recruiter | 3 | 5 | 4 | 36 |
  | candidate | 2 | 2 | 3 | 18 |
  | hiring-manager | 3 | 3 | 3 | 27 |
  | admin | 2 | 1 | 2 | 12 |
  | **Total** | **10** | **11** | **-** | **93** |
  
  ---
  
  ## Executive Summary
  
  | Metric | Value | Status |
  |--------|-------|--------|
  | Features Audited | {N} | ✅ |
  | Total Screenshots | {N} | ✅ |
  | Issues Found | {N} | ⚠️ |
  | Critical Issues | 0 | ✅ |
  | **Overall Status** | **APPROVED** | ✅ |
  
  [... rest of summary ...]
```

### Step 10: Generate Machine-Readable Report
```
CREATE reports/ui-audit/ui-audit-report.json:
  {
    "audit_date": "{timestamp}",
    "prototype_version": "1.0.0",
    "status": "APPROVED",
    
    "screenshots": {
      "baseline": {
        "desktop": {N},
        "tablet": {N},
        "mobile": {N},
        "total": {N}
      },
      "current": {
        "desktop": {N},
        "tablet": {N},
        "mobile": {N},
        "total": {N}
      },
      "diffs": {N},
      "naming_convention": "{app}--{screen}--{state}.png"
    },
    
    "features": [...],
    "issues": [...],
    "coverage": {...}
  }
```

### Step 11: Validate Audit Results (REQUIRED)
```
VALIDATE audit completion:
  
  SCREENSHOT CHECKS:
    - [ ] Playwright installed and configured
    - [ ] Baseline screenshots captured for ALL screens
    - [ ] All 3 viewports have screenshots (desktop, tablet, mobile)
    - [ ] All modals have screenshots
    - [ ] Screenshot naming follows convention
  
  AUDIT CHECKS:
    - [ ] All features have audit reports
    - [ ] No critical issues found
    - [ ] No major issues unresolved
    - [ ] Summary report complete
    
IF screenshot capture failed:
  ═══════════════════════════════════════════
  ❌ SCREENSHOT CAPTURE INCOMPLETE
  ═══════════════════════════════════════════
  
  Missing screenshots:
  • {list missing screens}
  
  Run debug mode:
    cd prototype && npx playwright test --debug
  
  ═══════════════════════════════════════════
    
IF critical or major issues found:
  ═══════════════════════════════════════════
  ❌ UI AUDIT FAILED
  ═══════════════════════════════════════════
  
  Critical/Major issues:
  • {issue_id}: {description}
  
  These MUST be resolved before delivery.
  ═══════════════════════════════════════════
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
    progress['phases']['ui_audit']['status'] = 'complete'
    progress['phases']['ui_audit']['completed_at'] = datetime.now().isoformat()
    progress['phases']['ui_audit']['outputs'] = [
        "reports/ui-audit/AUDIT_SUMMARY.md",
        "reports/ui-audit/FEAT-*-AUDIT-REPORT.md",
        "reports/ui-audit/screenshots/baseline/**/*.png",
        "reports/ui-audit/screenshots/current/**/*.png",
        "reports/ui-audit/ui-audit-report.json",
        "prototype/playwright.config.ts",
        "prototype/tests/screenshots/*.spec.ts"
    ]
    progress['phases']['ui_audit']['validation'] = {
        'status': 'passed',
        'screenshots_captured': screenshots_count,
        'issues_critical': 0,
        'issues_major': 0,
        'issues_minor': minor_issues_count
    }
    progress['phases']['ui_audit']['metrics'] = {
        'features_audited': features_count,
        'screens_audited': screens_count,
        'modals_captured': modals_count,
        'screenshots_baseline': baseline_count,
        'screenshots_current': current_count,
        'screenshots_total': total_screenshots
    }
    # Lock released and changes saved automatically here
```

**Benefits**:
- ✅ Prevents progress.json corruption during screenshot capture failures
- ✅ Automatic rollback if exception occurs during UI audit
- ✅ File locking prevents concurrent write conflicts
- ✅ Backup created before each update

### Step 12.5: Auto-Invoke Validation Summary (Phase 4 Enhancement)

> **Phase 4 Enhancement**: Automatically generate comprehensive validation summary after UI Audit completes

```
LOG: "✅ UI Audit complete. Auto-invoking Validation Summary generation..."

// AUTO-INVOKE Validation Summary skill
INVOKE Prototype_ValidationSummary:
  system_name: {SystemName}
  trigger: "auto_after_cp14"

WAIT for completion

READ _state/validation_summary.json → summary_data

LOG: "✅ Validation Summary generated"
LOG: "📄 Report: 05-validation/VALIDATION_SUMMARY.md"
LOG: "📊 Data: _state/validation_summary.json"
LOG: "🎯 Overall Status: {summary_data.overall_status}"

IF summary_data.overall_status == "FAIL":
  ═══════════════════════════════════════════
  ⚠️ VALIDATION SUMMARY: ACTION REQUIRED
  ═══════════════════════════════════════════

  Critical issues found:
  {FOR each recommendation with priority="CRITICAL":}
  • {recommendation.message}
  {END FOR}

  Review full report: 05-validation/VALIDATION_SUMMARY.md
  ═══════════════════════════════════════════
ELSE:
  ═══════════════════════════════════════════
  ✅ VALIDATION SUMMARY: APPROVED FOR DELIVERY
  ═══════════════════════════════════════════

  • Build Status: PASS
  • P0 Coverage: 100%
  • Assembly-First: PASS
  • Test Coverage: {summary_data.test_coverage.unit_coverage_percent}%

  Review full report: 05-validation/VALIDATION_SUMMARY.md
  ═══════════════════════════════════════════
```

---

## Output Files (REQUIRED)

| Path | Purpose | Blocking? |
|------|---------|-----------|
| `playwright.config.ts` | Playwright configuration | ✅ Yes |
| `tests/screenshots/*.spec.ts` | Screenshot automation scripts | ✅ Yes |
| `screenshots/baseline/**/*.png` | BEFORE audit screenshots | ✅ Yes |
| `screenshots/current/**/*.png` | AFTER fixes screenshots | ⚠️ If fixes made |
| `AUDIT_SUMMARY.md` | Overall summary | ✅ Yes |
| `{FEAT-NNN}-AUDIT-REPORT.md` | Per-feature reports | ✅ Yes |
| `ui-audit-report.json` | Machine-readable | ✅ Yes |

---

## Screenshot Requirements

### Mandatory Captures

| Type | Required | Naming |
|------|----------|--------|
| Every screen - default state | ✅ Yes | `{app}--{screen}--default.png` |
| Every screen - loading state | ✅ Yes | `{app}--{screen}--loading.png` |
| Every screen - empty state | ✅ If applicable | `{app}--{screen}--empty.png` |
| Every modal/dialog | ✅ Yes | `{app}--{screen}--modal-{name}.png` |
| Hover states (key elements) | ⚠️ Recommended | `{app}--{screen}--hover-{element}.png` |
| Drag states (if drag-drop) | ⚠️ Recommended | `{app}--{screen}--drag-active.png` |

### Viewports

| Viewport | Width | Height | Directory |
|----------|-------|--------|-----------|
| Desktop | 1280px | 720px | `desktop/` |
| Tablet | 768px | 1024px | `tablet/` |
| Mobile | 375px | 667px | `mobile/` |

---

## Technology Alternatives

If Playwright is not suitable, use one of these alternatives:

| Framework | Install | Config File |
|-----------|---------|-------------|
| **Playwright** (recommended) | `npm i -D @playwright/test` | `playwright.config.ts` |
| **Puppeteer** | `npm i -D puppeteer` | Custom script |
| **Cypress** | `npm i -D cypress` | `cypress.config.ts` |
| **BackstopJS** | `npm i -D backstopjs` | `backstop.json` |

The automation script structure remains the same regardless of framework.

---

## Progress.json Update

```json
{
  "phases": {
    "ui_audit": {
      "status": "complete",
      "completed_at": "2024-12-13T15:30:00Z",
      "outputs": [
        "prototype/playwright.config.ts",
        "prototype/tests/screenshots/*.spec.ts",
        "reports/ui-audit/screenshots/baseline/**/*.png",
        "reports/ui-audit/AUDIT_SUMMARY.md",
        "reports/ui-audit/ui-audit-report.json"
      ],
      "validation": {
        "status": "passed",
        "screenshots_captured": 120,
        "issues_critical": 0,
        "issues_major": 0,
        "issues_minor": 5
      },
      "metrics": {
        "features_audited": 5,
        "screens_audited": 15,
        "modals_captured": 11,
        "screenshots_baseline": 120,
        "screenshots_current": 120,
        "viewports": ["desktop", "tablet", "mobile"]
      }
    }
  }
}
```
