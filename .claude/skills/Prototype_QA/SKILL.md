---
name: validating-prototype-quality
description: Use when you need to validate prototype implementation against requirements, ensuring P0 coverage and generating traceability reports.
model: haiku
allowed-tools: Bash, Glob, Grep, Read
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-prototype-quality started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill validating-prototype-quality ended '{"stage": "prototype"}'
---

# QA Validation

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh skill validating-prototype-quality instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_QA
- **Version**: 1.1.0
- **Created**: 2025-01-15
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v1.1.0 (2025-12-19): Added version control metadata to skill and output templates per VERSION_CONTROL_STANDARD.md
  - v1.0.0 (2025-01-15): Initial skill version

Validate prototype against requirements registry. Follows OUTPUT_STRUCTURE.md for deterministic folder structure.

> **💡 EXAMPLES ARE ILLUSTRATIVE**: Requirement IDs and traceability examples shown below (e.g., "US-001", "PP-002", "JTBD-003") are examples. Your actual requirements will come from your project's requirements registry.

## Output Structure (REQUIRED)

> **⚠️ SHARED STATE FOLDER**: The `_state/` folder is at the **PROJECT ROOT level**, NOT inside `Prototype_<SystemName>/`. This folder is SHARED between Discovery and Prototype phases.
>
> ```
> project_root/
> ├── _state/                           ← SHARED state folder (ROOT LEVEL)
> │   ├── screen_registry.json          # Master screen tracking
> │   ├── requirements_registry.json
> │   ├── progress.json
> │   └── discovery_summary.json
> ├── traceability/                      ← SHARED traceability folder (ROOT LEVEL)
> │   └── prototype_traceability_register.json
> ├── ClientAnalysis_<SystemName>/      ← Discovery outputs
> └── Prototype_<SystemName>/           ← Prototype outputs (05-validation/ lives here)
> ```
>
> **Path Resolution**:
> - All paths starting with `_state/` resolve to the **ROOT-LEVEL shared folder**
> - All paths starting with `traceability/` resolve to the **ROOT-LEVEL shared folder**
> - All other paths (e.g., `05-validation/`) resolve relative to `Prototype_<SystemName>/`

This skill MUST generate the following structure (inside `Prototype_<SystemName>/`):

```
05-validation/
├── README.md                         # Folder overview and process
├── QA_CHECKLIST.md                   # Manual QA checklist
├── REQUIREMENTS_COVERAGE.md          # P0/P1/P2 coverage report
├── TRACEABILITY_MATRIX.md            # Full requirement-to-implementation mapping
├── VALIDATION_REPORT.md              # Current validation results
├── VALIDATION_REPORT_FINAL.md        # Final QA sign-off (after approval)
└── accessibility/
    ├── a11y-audit-results.md         # Accessibility audit findings
    └── wcag-compliance.md            # WCAG compliance status
```

---

## Procedure

### Step 0: Generate Folder README (REQUIRED)
```
CREATE 05-validation/README.md:
  # 05-validation/ - QA & Traceability

  > **Purpose**: Verify prototype meets all requirements before delivery
  > **Dependencies**: `_state/requirements_registry.json`, `prototype/`
  > **Consumed By**: Delivery decision, `06-change-requests/`

  ---

  ## What Is This?

  The `05-validation/` directory contains **QA results and traceability documentation** that proves the prototype meets its requirements:

  1. **Validation Report** - Overall QA status and findings
  2. **Traceability Matrix** - Requirement → Implementation mapping
  3. **Requirements Coverage** - P0/P1/P2 coverage percentages
  4. **QA Checklist** - Manual testing checklist
  5. **Accessibility Audit** - WCAG compliance results

  **Critical Rule:** P0 coverage must be 100% before delivery is approved.

  ---

  ## Directory Structure

  ```
  05-validation/
  │
  ├── README.md                      # This file
  ├── VALIDATION_REPORT.md           # Current validation status
  ├── TRACEABILITY_MATRIX.md         # Req → Implementation mapping
  ├── REQUIREMENTS_COVERAGE.md       # Coverage analysis
  ├── QA_CHECKLIST.md                # Manual testing checklist
  │
  └── accessibility/
      ├── a11y-audit-results.md      # Accessibility audit findings
      └── wcag-compliance.md         # WCAG conformance status
  ```

  ---

  ## File Descriptions

  ### VALIDATION_REPORT.md

  Executive summary of QA status including:
  - Overall pass/fail status
  - P0/P1/P2 coverage percentages
  - Screen/Component implementation counts
  - Build status and critical defects

  ### TRACEABILITY_MATRIX.md

  Maps every requirement to its implementation:
  - P0 requirements with screens, components, and services
  - Screen-to-requirement mapping
  - Component-to-requirement mapping
  - Service/Hook mappings
  - Critical path verification

  ### REQUIREMENTS_COVERAGE.md

  Coverage analysis by priority level with detailed breakdown by category.

  ### QA_CHECKLIST.md

  Manual testing checklist for testers organized by screen and functionality.

  ### accessibility/

  WCAG compliance documentation and audit results.

  ---

  ## Validation Process

  ```
  ┌─────────────────────────────────────────────────────┐
  │                  QA VALIDATION                       │
  ├─────────────────────────────────────────────────────┤
  │                                                     │
  │  1. Build Verification                              │
  │     └─ Does `npm run build` succeed?                │
  │                                                     │
  │  2. Traceability Check                              │
  │     └─ Is every P0 requirement mapped?              │
  │                                                     │
  │  3. Coverage Analysis                               │
  │     └─ Is P0 coverage = 100%?                       │
  │                                                     │
  │  4. Accessibility Audit                             │
  │     └─ Does it pass WCAG AA?                        │
  │                                                     │
  │  5. Manual Spot Check                               │
  │     └─ Do critical workflows work?                  │
  │                                                     │
  │           ┌──────────────────────┐                  │
  │           │ P0 Coverage < 100%?  │                  │
  │           └─────────┬────────────┘                  │
  │                     │                               │
  │          ┌──────────┴──────────┐                    │
  │          │                     │                    │
  │    [BLOCKED]              [APPROVED]                │
  │    List gaps              Proceed to                │
  │    Request fix            delivery                  │
  │                                                     │
  └─────────────────────────────────────────────────────┘
  ```

  ---

  ## Blocking Gate

  **If P0 coverage < 100%, delivery is BLOCKED.**

  The validation report will list:
  - Which P0 requirements are not addressed
  - Which screens/components need updates
  - Recommended actions

  ---

  ## Post-Validation

  After validation passes:
  1. `VALIDATION_REPORT.md` shows PASSED
  2. `_state/qa_validation_state.json` updated
  3. `_state/progress.json` shows qa: complete
  4. Prototype can be delivered or change requests processed
```

### Step 1: Validate Inputs (REQUIRED)
```
READ _state/requirements_registry.json → all requirements
READ _state/progress.json → completed phases
READ 02-screens/SCREEN_SPECIFICATIONS_SUMMARY.md → implemented screens
READ 01-components/COMPONENT_LIBRARY_SUMMARY.md → implemented components

// ═══════════════════════════════════════════════════════════
// CRITICAL: Load Screen Registry for Traceability Validation
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

IF requirements_registry missing:
  BLOCK: "Run Requirements first"

LOAD all requirements:
  p0_requirements = filter(priority == "P0")
  p1_requirements = filter(priority == "P1")
  p2_requirements = filter(priority == "P2")

LOG: "Validating against {p0} P0, {p1} P1, {p2} P2 requirements"
```

### Step 2: Build Traceability Matrix
```
FOR each requirement in registry:
  SCAN all outputs for addressed_by entries:
    - Component specs (01-components/)
    - Screen specs (02-screens/)
    - Data model (00-foundation/data-model/)
    - Test data stories (00-foundation/test-data/)
    
  RECORD:
    requirement_id
    description
    priority
    addressed_by: [list of artifacts]
    validation_status: addressed | partial | unaddressed
    evidence: [specific file:section references]
```

### Step 3: Generate Traceability Matrix
```
CREATE 05-validation/TRACEABILITY_MATRIX.md:
  ---
  document_id: QA-TRACE-001
  version: 1.0.0
  created_at: {YYYY-MM-DD}
  updated_at: {YYYY-MM-DD}
  generated_by: Prototype_QA
  source_files:
    - _state/requirements_registry.json
    - _state/progress.json
    - 02-screens/SCREEN_SPECIFICATIONS_SUMMARY.md
    - 01-components/COMPONENT_LIBRARY_SUMMARY.md
  change_history:
    - version: "1.0.0"
      date: "{YYYY-MM-DD}"
      author: "Prototype_QA"
      changes: "Initial traceability matrix generation"
  ---

  # Requirements Traceability Matrix

  ## Overview

  | Priority | Total | Addressed | Partial | Unaddressed |
  |----------|-------|-----------|---------|-------------|
  | P0 | 15 | 15 | 0 | 0 |
  | P1 | 25 | 23 | 2 | 0 |
  | P2 | 18 | 12 | 4 | 2 |
  | **Total** | **58** | **50** | **6** | **2** |
  
  ---
  
  ## P0 Requirements (MUST BE 100%)
  
  | Req ID | Description | Status | Addressed By | Evidence |
  |--------|-------------|--------|--------------|----------|
  | PP-001 | Manual tracking inefficient | ✅ | candidate-pipeline.md | Kanban board replaces spreadsheet |
  | PP-002 | Information scattered | ✅ | candidate-profile.md | Unified profile view |
  | US-001 | View all candidates | ✅ | candidate-pipeline.md | Pipeline screen with filters |
  | US-003 | Move candidates | ✅ | candidate-pipeline.md | Drag-drop between stages |
  | JTBD-001 | Quick assessment | ✅ | CandidateCard component | Score visible on card |
  | FR-003 | Store candidates | ✅ | Candidate.schema.json | Entity defined |
  | A11Y-001 | Keyboard navigation | ✅ | All interactive components | Tab order documented |
  | A11Y-003 | Focus indicators | ✅ | Design tokens | focus-ring token |
  ...
  
  **P0 Coverage: 15/15 (100%)** ✅
  
  ---
  
  ## P1 Requirements
  
  | Req ID | Description | Status | Addressed By | Notes |
  |--------|-------------|--------|--------------|-------|
  | FR-010 | Filter candidates | ✅ | candidate-pipeline.md | Filter bar component |
  | FR-011 | Search candidates | ⚠️ | - | Partial - basic only |
  ...
  
  **P1 Coverage: 23/25 (92%)**
  
  ---
  
  ## P2 Requirements
  
  | Req ID | Description | Status | Notes |
  |--------|-------------|--------|-------|
  | FR-050 | Export to CSV | ❌ | Deferred to v2 |
  ...
  
  **P2 Coverage: 12/18 (67%)**
  
  ---
  
  ## Unaddressed Requirements
  
  ### P1 (Action Required)
  | Req ID | Description | Recommendation |
  |--------|-------------|----------------|
  | FR-011 | Advanced search | Add to next sprint |
  
  ### P2 (Documented Gaps)
  | Req ID | Description | Reason |
  |--------|-------------|--------|
  | FR-050 | CSV export | Scope reduction, deferred |

  ---

  ## Screen-to-Requirement Mapping

  | Screen | Route | P0 Requirements |
  |--------|-------|-----------------|
  [FOR each screen from 02-screens/]:
  | {screen_name} | {route} | {comma-separated P0 req IDs} |

  ---

  ## Component-to-Requirement Mapping

  | Component | Requirements Addressed |
  |-----------|------------------------|
  [FOR each component from 01-components/]:
  | {component_name} | {comma-separated req IDs} |

  ---

  ## Service-to-Requirement Mapping

  | Service | Function | Requirements |
  |---------|----------|--------------|
  [FOR each service from data-model and api-contracts]:
  | {service_name} | {function} | {req IDs} |

  ---

  ## Hook-to-Requirement Mapping

  | Hook | Purpose | Requirements |
  |------|---------|--------------|
  [FOR each hook identified in screen/component specs]:
  | {hook_name} | {purpose} | {req IDs} |

  ---

  ## Critical Path Verification

  ### {Critical Requirement 1} ({Req ID})
  - **Component:** {implementing component}
  - **Service:** {implementing service}
  - **Status:** VERIFIED - {verification notes}

  ### {Critical Requirement 2} ({Req ID})
  - **Screens:** {flow description}
  - **Flow:** {step by step}
  - **Status:** VERIFIED - {verification notes}

  [ADD all P0 critical path items]

  ---

  ## Change Request Implementations

  [This section tracks changes made via change requests]

  ### CR-{NNN}: {Title} ({Date})

  | Requirement | Description | Implementation | Status |
  |-------------|-------------|----------------|--------|
  | {Req ID} | {description} | {implementation notes} | IMPLEMENTED |

  **Files Added/Modified:**
  - {file path} (NEW/MODIFIED)

  ---

  ## Traceability Complete

  All {total} requirements have been mapped to implementation artifacts.
```

### Step 4: Generate Requirements Coverage Report
```
CREATE 05-validation/REQUIREMENTS_COVERAGE.md:
  ---
  document_id: QA-COVERAGE-001
  version: 1.0.0
  created_at: {YYYY-MM-DD}
  updated_at: {YYYY-MM-DD}
  generated_by: Prototype_QA
  source_files:
    - _state/requirements_registry.json
    - 05-validation/TRACEABILITY_MATRIX.md
  change_history:
    - version: "1.0.0"
      date: "{YYYY-MM-DD}"
      author: "Prototype_QA"
      changes: "Initial requirements coverage report generation"
  ---

  # Requirements Coverage Report

  ## Executive Summary

  | Metric | Value | Status |
  |--------|-------|--------|
  | P0 Coverage | 100% | ✅ PASS |
  | P1 Coverage | 92% | ⚠️ ACCEPTABLE |
  | P2 Coverage | 67% | ℹ️ AS PLANNED |
  | Overall | 86% | ✅ PASS |
  
  ---
  
  ## Coverage by Category
  
  ### Functional Requirements
  | ID Range | Category | Addressed | Total | Coverage |
  |----------|----------|-----------|-------|----------|
  | FR-001-020 | Core CRUD | 18 | 20 | 90% |
  | FR-021-040 | Workflows | 15 | 20 | 75% |
  | FR-041-060 | Reporting | 8 | 20 | 40% |
  
  ### User Stories
  | Category | Addressed | Total | Coverage |
  |----------|-----------|-------|----------|
  | Recruiter | 12 | 12 | 100% |
  | Hiring Manager | 8 | 10 | 80% |
  | Interviewer | 5 | 6 | 83% |
  
  ### Accessibility
  | Category | Addressed | Total | Coverage |
  |----------|-----------|-------|----------|
  | WCAG 2.1 AA | 8 | 8 | 100% |
  
  ---
  
  ## Gap Analysis
  
  ### Critical Gaps (None)
  No P0 requirements unaddressed.
  
  ### Important Gaps
  | Req ID | Gap | Impact | Mitigation |
  |--------|-----|--------|------------|
  | FR-011 | Advanced search | Medium | Basic search available |
  
  ### Accepted Gaps
  | Req ID | Reason | Documented |
  |--------|--------|------------|
  | FR-050 | Scope reduction | Yes |
```

### Step 5: Generate QA Checklist
```
CREATE 05-validation/QA_CHECKLIST.md:
  # QA Checklist
  
  ## Pre-Flight Checks
  
  ### Build Verification
  - [ ] `npm run build` completes without errors
  - [ ] `npm run lint` passes
  - [ ] `npm run test` all tests pass
  - [ ] No console errors in browser
  
  ### Functional Testing
  
  #### Authentication
  - [ ] Login with valid credentials
  - [ ] Login with invalid credentials shows error
  - [ ] Logout clears session
  - [ ] Protected routes redirect to login
  
  #### Recruiter App
  - [ ] Dashboard loads with metrics
  - [ ] Pipeline shows all stages
  - [ ] Cards display candidate info
  - [ ] Drag-drop moves candidates
  - [ ] Filter by stage works
  - [ ] Search finds candidates
  - [ ] Candidate profile loads
  - [ ] Edit candidate saves
  
  #### Hiring Manager App
  - [ ] Triage queue shows candidates
  - [ ] Can approve/reject candidates
  - [ ] Team view shows positions
  
  #### Interviewer Portal
  - [ ] Availability calendar loads
  - [ ] Can set available slots
  - [ ] Interview schedule visible
  
  ---
  
  ### Accessibility Testing
  
  #### Keyboard Navigation
  - [ ] All interactive elements focusable
  - [ ] Tab order is logical
  - [ ] Focus visible at all times
  - [ ] Escape closes modals
  - [ ] Enter activates buttons
  
  #### Screen Reader
  - [ ] Headings properly nested
  - [ ] Images have alt text
  - [ ] Forms have labels
  - [ ] Errors announced
  - [ ] Status changes announced
  
  #### Visual
  - [ ] Text readable at 200% zoom
  - [ ] No horizontal scroll at 320px
  - [ ] Color not only indicator
  - [ ] Contrast meets 4.5:1
  
  ---
  
  ### Cross-Browser Testing
  
  | Browser | Version | Status |
  |---------|---------|--------|
  | Chrome | Latest | [ ] |
  | Firefox | Latest | [ ] |
  | Safari | Latest | [ ] |
  | Edge | Latest | [ ] |
  
  ---
  
  ### Responsive Testing
  
  | Breakpoint | Width | Status |
  |------------|-------|--------|
  | Mobile | 375px | [ ] |
  | Tablet | 768px | [ ] |
  | Desktop | 1280px | [ ] |
  | Wide | 1536px | [ ] |
  
  ---
  
  ## Sign-Off
  
  | Role | Name | Date | Status |
  |------|------|------|--------|
  | QA Lead | | | |
  | Tech Lead | | | |
  | Product Owner | | | |
```

### Step 5.5: Automated Playwright Testing (Phase 3 Enhancement)

> **webapp-testing Integration**: Run automated functional tests using Playwright.

```
// ═══════════════════════════════════════════════════════════
// PHASE 3: AUTOMATED TESTING WITH PLAYWRIGHT
// ═══════════════════════════════════════════════════════════

LOG: "Setting up automated testing with Playwright..."

// Step 5.5.1: Create test infrastructure
CREATE 05-validation/playwright/:

CREATE 05-validation/playwright/setup.py:
  """
  Playwright test setup and utilities.
  """
  from playwright.sync_api import sync_playwright, Page
  import os

  # Screenshot directory
  SCREENSHOT_DIR = '05-validation/playwright/screenshots'
  os.makedirs(SCREENSHOT_DIR, exist_ok=True)

  def capture_screenshot(page: Page, name: str):
      """Capture screenshot for visual QA"""
      path = f"{SCREENSHOT_DIR}/{name}.png"
      page.screenshot(path=path, full_page=True)
      return path

  def wait_for_app_ready(page: Page):
      """Wait for app to be fully loaded"""
      page.wait_for_load_state('networkidle')
      page.wait_for_timeout(500)  # Additional buffer for React

// Step 5.5.2: Generate P0 requirement tests
FOR each P0_requirement in requirements_registry:

  CREATE test file for requirement:

CREATE 05-validation/playwright/test_p0_requirements.py:
  """
  Automated tests for P0 requirements.
  Generated from requirements registry.
  """
  from playwright.sync_api import sync_playwright, expect
  import json

  BASE_URL = 'http://localhost:5173'

  def test_p0_pipeline_view():
      """
      P0: PP-001 - Manual tracking inefficient
      Verifies: Kanban pipeline replaces spreadsheet tracking
      """
      with sync_playwright() as p:
          browser = p.chromium.launch(headless=True)
          page = browser.new_page()

          # Navigate to pipeline
          page.goto(f'{BASE_URL}/recruiter/pipeline')
          page.wait_for_load_state('networkidle')

          # Verify pipeline stages exist
          stages = page.locator('[data-testid="pipeline-stage"]').all()
          assert len(stages) >= 3, "Pipeline must have at least 3 stages"

          # Verify candidates are visible
          cards = page.locator('[data-testid="candidate-card"]').all()
          assert len(cards) > 0, "Pipeline must show candidate cards"

          # Capture evidence
          page.screenshot(path='05-validation/playwright/screenshots/p0-pipeline.png')

          browser.close()
          print("✅ P0-001: Pipeline view validated")

  def test_p0_candidate_profile():
      """
      P0: PP-002 - Information scattered
      Verifies: Unified candidate profile view
      """
      with sync_playwright() as p:
          browser = p.chromium.launch(headless=True)
          page = browser.new_page()

          page.goto(f'{BASE_URL}/recruiter/candidates/1')
          page.wait_for_load_state('networkidle')

          # Verify profile sections
          expect(page.locator('[data-testid="candidate-header"]')).to_be_visible()
          expect(page.locator('[data-testid="candidate-details"]')).to_be_visible()
          expect(page.locator('[data-testid="candidate-timeline"]')).to_be_visible()

          page.screenshot(path='05-validation/playwright/screenshots/p0-profile.png')

          browser.close()
          print("✅ P0-002: Candidate profile validated")

  def test_p0_drag_drop():
      """
      P0: US-003 - Move candidates between stages
      Verifies: Drag-drop functionality
      """
      with sync_playwright() as p:
          browser = p.chromium.launch(headless=True)
          page = browser.new_page()

          page.goto(f'{BASE_URL}/recruiter/pipeline')
          page.wait_for_load_state('networkidle')

          # Find a candidate card
          card = page.locator('[data-testid="candidate-card"]').first
          source_stage = card.locator('..').get_attribute('data-stage')

          # Find target stage
          target = page.locator('[data-testid="pipeline-stage"]').nth(1)

          # Perform drag-drop
          card.drag_to(target)
          page.wait_for_timeout(500)

          # Verify move
          page.screenshot(path='05-validation/playwright/screenshots/p0-dragdrop.png')

          browser.close()
          print("✅ P0-003: Drag-drop validated")

  # Add test for each P0 requirement...

  if __name__ == '__main__':
      test_p0_pipeline_view()
      test_p0_candidate_profile()
      test_p0_drag_drop()
      print("\\n✅ All P0 automated tests passed")

// Step 5.5.3: Generate screen screenshot tests
CREATE 05-validation/playwright/capture_all_screens.py:
  """
  Capture screenshots of all screens for visual QA.
  """
  from playwright.sync_api import sync_playwright
  import os

  BASE_URL = 'http://localhost:5173'
  SCREENSHOT_DIR = '05-validation/playwright/screenshots'

  SCREENS = [
      # Format: (name, path, wait_selector)
      ('login', '/login', '[data-testid="login-form"]'),
      ('dashboard', '/recruiter/dashboard', '[data-testid="dashboard"]'),
      ('pipeline', '/recruiter/pipeline', '[data-testid="pipeline"]'),
      ('candidate-list', '/recruiter/candidates', '[data-testid="candidate-list"]'),
      ('candidate-profile', '/recruiter/candidates/1', '[data-testid="candidate-header"]'),
      # Add all screens from 02-screens/
  ]

  def capture_all_screens():
      os.makedirs(SCREENSHOT_DIR, exist_ok=True)

      with sync_playwright() as p:
          browser = p.chromium.launch(headless=True)
          page = browser.new_page()
          page.set_viewport_size({'width': 1280, 'height': 720})

          for name, path, selector in SCREENS:
              try:
                  page.goto(f'{BASE_URL}{path}')
                  page.wait_for_load_state('networkidle')
                  if selector:
                      page.wait_for_selector(selector, timeout=5000)

                  page.screenshot(
                      path=f'{SCREENSHOT_DIR}/{name}.png',
                      full_page=True
                  )
                  print(f'✅ Captured: {name}')
              except Exception as e:
                  print(f'❌ Failed: {name} - {e}')

          browser.close()

  if __name__ == '__main__':
      capture_all_screens()

// Step 5.5.4: Generate run script
CREATE 05-validation/playwright/run_tests.sh:
  #!/bin/bash
  # Run all Playwright tests with server management

  echo "🚀 Starting prototype server..."
  cd prototype && npm run dev &
  SERVER_PID=$!
  sleep 5  # Wait for server to start

  echo "🧪 Running P0 requirement tests..."
  python 05-validation/playwright/test_p0_requirements.py

  echo "📸 Capturing screen screenshots..."
  python 05-validation/playwright/capture_all_screens.py

  echo "🛑 Stopping server..."
  kill $SERVER_PID

  echo "✅ All tests complete. Screenshots in 05-validation/playwright/screenshots/"

// Step 5.5.5: Execute tests and capture results
RUN automated tests:
  cd {project_root}
  bash 05-validation/playwright/run_tests.sh

CAPTURE test results:
  - Test pass/fail counts
  - Screenshot paths
  - Error messages (if any)

CREATE 05-validation/AUTOMATED_TEST_RESULTS.md:
  # Automated Test Results

  ## Summary

  | Category | Total | Passed | Failed |
  |----------|-------|--------|--------|
  | P0 Requirements | {p0_count} | {passed} | {failed} |
  | Screen Captures | {screen_count} | {captured} | {missing} |

  ## P0 Requirement Tests

  | Req ID | Test | Status | Evidence |
  |--------|------|--------|----------|
  | PP-001 | Pipeline View | ✅ Pass | [screenshot](playwright/screenshots/p0-pipeline.png) |
  | PP-002 | Candidate Profile | ✅ Pass | [screenshot](playwright/screenshots/p0-profile.png) |
  | US-003 | Drag-Drop | ✅ Pass | [screenshot](playwright/screenshots/p0-dragdrop.png) |

  ## Screen Captures

  | Screen | Status | Screenshot |
  |--------|--------|------------|
  | Login | ✅ | [login.png](playwright/screenshots/login.png) |
  | Dashboard | ✅ | [dashboard.png](playwright/screenshots/dashboard.png) |
  | Pipeline | ✅ | [pipeline.png](playwright/screenshots/pipeline.png) |

  ## Test Execution Log

  ```
  {test_output}
  ```

  ---

  Generated: {timestamp}

IF any tests fail:
  ═══════════════════════════════════════════
  ⚠️ AUTOMATED TESTS FAILED
  ═══════════════════════════════════════════

  {failed_count} test(s) failed:
  {list failed tests with errors}

  How would you like to proceed?
  1. "investigate" - Show detailed failure info
  2. "fix" - Attempt to fix failing tests
  3. "continue" - Continue with manual QA
  4. "block" - Block QA completion until fixed
  ═══════════════════════════════════════════

  WAIT for user response

LOG: "✅ Automated testing complete"
```

### Step 6: Generate Accessibility Audit
```
CREATE 05-validation/accessibility/:

CREATE a11y-audit-results.md:
  # Accessibility Audit Results
  
  ## Summary
  
  | Category | Issues | Critical | Major | Minor |
  |----------|--------|----------|-------|-------|
  | Keyboard | 0 | 0 | 0 | 0 |
  | Screen Reader | 2 | 0 | 1 | 1 |
  | Visual | 1 | 0 | 0 | 1 |
  | **Total** | **3** | **0** | **1** | **2** |
  
  ---
  
  ## Issues Found
  
  ### Major
  
  #### [A11Y-01] Missing aria-label on icon buttons
  - **Location:** Header notification button
  - **Impact:** Screen readers announce "button" only
  - **Fix:** Add aria-label="Notifications"
  - **Status:** Open
  
  ### Minor
  
  #### [A11Y-02] Placeholder text disappears
  - **Location:** Search input
  - **Impact:** Label not persistent
  - **Fix:** Add visible label
  - **Status:** Open
  
  ---
  
  ## Components Audited
  
  | Component | Keyboard | Focus | ARIA | Status |
  |-----------|----------|-------|------|--------|
  | Button | ✅ | ✅ | ✅ | Pass |
  | Input | ✅ | ✅ | ✅ | Pass |
  | Select | ✅ | ✅ | ✅ | Pass |
  | Dialog | ✅ | ✅ | ⚠️ | Minor |
  | Table | ✅ | ✅ | ✅ | Pass |

CREATE wcag-compliance.md:
  # WCAG 2.1 AA Compliance
  
  ## Conformance Level: AA
  
  ### Level A (Required)
  
  | Criterion | Status | Notes |
  |-----------|--------|-------|
  | 1.1.1 Non-text Content | ✅ | All images have alt |
  | 1.3.1 Info and Relationships | ✅ | Semantic HTML |
  | 1.4.1 Use of Color | ✅ | Icons accompany color |
  | 2.1.1 Keyboard | ✅ | Full keyboard access |
  | 2.1.2 No Keyboard Trap | ✅ | Focus moves freely |
  | 2.4.1 Bypass Blocks | ✅ | Skip link present |
  | 4.1.1 Parsing | ✅ | Valid HTML |
  | 4.1.2 Name, Role, Value | ✅ | ARIA implemented |
  
  ### Level AA (Required)
  
  | Criterion | Status | Notes |
  |-----------|--------|-------|
  | 1.4.3 Contrast (Minimum) | ✅ | 4.5:1 verified |
  | 1.4.4 Resize Text | ✅ | Works at 200% |
  | 2.4.7 Focus Visible | ✅ | Focus ring present |
  | 3.1.2 Language of Parts | ✅ | lang attributes |
  | 3.3.3 Error Suggestion | ✅ | Helpful messages |
```

### Step 7: Validate P0 Coverage (CRITICAL - BLOCKING)
```
CALCULATE p0_coverage:
  addressed = count where status == "addressed"
  total = count where priority == "P0"
  coverage = addressed / total * 100

IF p0_coverage < 100:
  ═══════════════════════════════════════════
  ❌ QA VALIDATION FAILED - DELIVERY BLOCKED
  ═══════════════════════════════════════════
  
  P0 Coverage: {coverage}% (MUST BE 100%)
  
  Unaddressed P0 Requirements:
  • {req_id}: {description}
  
  This BLOCKS prototype delivery.
  
  How would you like to proceed?
  1. "resolve: [REQ-ID]" - Address specific requirement
  2. "reassign: [REQ-ID] to P1" - Reclassify (requires justification)
  3. "show details" - Full unaddressed list
  4. "abort" - Stop and fix
  ═══════════════════════════════════════════
  
  WAIT for user response
  LOOP until p0_coverage == 100
  
ELSE:
  LOG: "✅ P0 Coverage 100% - Delivery APPROVED"
  delivery_status = "APPROVED"
```

### Step 7.5: Validate Screen Implementation Coverage (CRITICAL - BLOCKING)

> **CRITICAL**: This step ensures ALL screens from Discovery were implemented.

```
// ═══════════════════════════════════════════════════════════
// MANDATORY: Validate All Discovery Screens Have React Code
// ═══════════════════════════════════════════════════════════

LOAD traceability/screen_registry.json → screen_registry
discovery_screens = screen_registry.discovery_screens
screen_coverage = screen_registry.screen_coverage

// Count screens by status
screens_with_specs = []
screens_with_code = []
screens_missing = []

FOR each screen in discovery_screens:
  traceability = screen_registry.traceability[screen.id]

  IF traceability.spec_status == "complete":
    APPEND screen to screens_with_specs[]

  IF traceability.code_status == "complete":
    APPEND screen to screens_with_code[]
  ELSE:
    APPEND screen to screens_missing[]

// Calculate coverage percentages
spec_coverage_percent = (screens_with_specs.length / discovery_screens.length) * 100
code_coverage_percent = (screens_with_code.length / discovery_screens.length) * 100

// ═══════════════════════════════════════════════════════════
// BLOCKING CHECK: ALL Discovery screens MUST have React code
// ═══════════════════════════════════════════════════════════

IF screens_missing.length > 0:
  ═══════════════════════════════════════════════════════════════
  ❌ BLOCKING: Screen Implementation Incomplete
  ═══════════════════════════════════════════════════════════════

  Screen Coverage Summary:
  • Discovery screens: {discovery_screens.length}
  • Screens with specs: {screens_with_specs.length} ({spec_coverage_percent}%)
  • Screens with code: {screens_with_code.length} ({code_coverage_percent}%)
  • Screens MISSING: {screens_missing.length}

  ┌─────────────────────────────────────────────────────────────┐
  │  MISSING SCREEN IMPLEMENTATIONS                              │
  ├─────────────────────────────────────────────────────────────┤
  │  ID     │ Name                    │ Priority │ Platform      │
  ├─────────────────────────────────────────────────────────────┤
  FOR each screen in screens_missing:
  │  {id}   │ {name}                  │ {prio}   │ {platform}    │
  └─────────────────────────────────────────────────────────────┘

  QA CANNOT APPROVE delivery with missing screens.

  All {discovery_screens.length} screens from Discovery Phase MUST
  have React component implementations before delivery.

  How would you like to proceed?
  1. "generate missing" - Go back and generate missing screens
  2. "show details" - Show full screen traceability
  3. "abort" - Stop QA and return to CodeGen phase

  ═══════════════════════════════════════════════════════════════

  WAIT for user response
  DO NOT proceed to Step 8 until ALL screens have code
  delivery_status = "BLOCKED"

ELSE:
  ═══════════════════════════════════════════════════════════════
  ✅ Screen Implementation Coverage: 100%
  ═══════════════════════════════════════════════════════════════

  All {discovery_screens.length} Discovery screens have implementations:

  Mobile: {mobile_count} screens
  Desktop: {desktop_count} screens

  Traceability Chain: COMPLETE
  Discovery → Specs → Code ✅

  ═══════════════════════════════════════════════════════════════

// Update traceability register
UPDATE traceability/prototype_traceability_register.json:
  screen_traceability.coverage = {
    discovery_total: discovery_screens.length,
    specs_generated: screens_with_specs.length,
    code_generated: screens_with_code.length,
    tests_generated: screens_with_tests.length
  }

// Add screen coverage to validation report
screen_validation_result = {
  status: screens_missing.length == 0 ? "PASS" : "FAIL",
  discovery_screens: discovery_screens.length,
  implemented_screens: screens_with_code.length,
  coverage_percent: code_coverage_percent,
  missing_screens: screens_missing
}

LOG: "📊 Screen Traceability: {screens_with_code.length}/{discovery_screens.length} (100%)"
```

### Step 8: Generate Validation Report
```
CREATE 05-validation/VALIDATION_REPORT.md:
  ---
  document_id: QA-VALIDATION-001
  version: 1.0.0
  created_at: {YYYY-MM-DD}
  updated_at: {YYYY-MM-DD}
  generated_by: Prototype_QA
  source_files:
    - _state/requirements_registry.json
    - _state/progress.json
    - 05-validation/TRACEABILITY_MATRIX.md
    - 05-validation/REQUIREMENTS_COVERAGE.md
  change_history:
    - version: "1.0.0"
      date: "{YYYY-MM-DD}"
      author: "Prototype_QA"
      changes: "Initial validation report generation"
  ---

  # Validation Report

  **Generated:** {timestamp}

  ---

  ## Executive Summary
  
  | Metric | Value | Status |
  |--------|-------|--------|
  | **Delivery Status** | {APPROVED/BLOCKED} | {icon} |
  | P0 Coverage | {x}% | {status} |
  | P1 Coverage | {x}% | {status} |
  | P2 Coverage | {x}% | {status} |
  | A11Y Issues (Critical) | {count} | {status} |
  | Build Status | {pass/fail} | {status} |
  
  ---
  
  ## Requirements Validation
  
  [Summary from traceability matrix]
  
  ---
  
  ## Functional Validation
  
  | Area | Tests | Passed | Failed |
  |------|-------|--------|--------|
  | Authentication | 4 | 4 | 0 |
  | Recruiter App | 8 | 8 | 0 |
  | Hiring Manager | 4 | 4 | 0 |
  | Interviewer | 3 | 3 | 0 |
  
  ---
  
  ## Accessibility Validation
  
  [Summary from a11y audit]
  
  ---
  
  ## Recommendation
  
  {APPROVED FOR DELIVERY / BLOCKED - REQUIRES FIXES}
  
  ### Outstanding Items
  [List if any]
  
  ---
  
  ## Sign-Off
  
  | Role | Approval | Date |
  |------|----------|------|
  | QA | Pending | |
  | Tech | Pending | |
  | Product | Pending | |
```

### Step 9: Auto-Invoke Decomposition
```
LOG: "Auto-triggering Decomposition (QA complete)"

INVOKE Prototype_Decomposition:
  MODE: merge
  TRIGGER: "qa_completed"
```

### Step 9.5: Verification Gate (MANDATORY)

> **See: ../VERIFICATION_GATE.md for full pattern**

```
EXECUTE verification_gate:

  // 1. IDENTIFY verification commands
  verification_commands = [
    "test -s 05-validation/VALIDATION_REPORT.md",
    "test -s 05-validation/TRACEABILITY_MATRIX.md",
    "test -s 05-validation/REQUIREMENTS_COVERAGE.md",
    "test -s 05-validation/QA_CHECKLIST.md",
    "jq '.summary.p0_coverage' 05-validation/coverage.json",  // Must be "100%"
    "validate_component_library_dependencies()"  // Component library deps check
  ]

  // 2. RUN all verifications
  FOR each command:
    EXECUTE and CAPTURE result

  // 3. CRITICAL CHECK: P0 coverage must be 100%
  IF p0_coverage != "100%":
    ═══════════════════════════════════════════
    ❌ VERIFICATION GATE FAILED
    ═══════════════════════════════════════════

    P0 Coverage: {actual}% (REQUIRED: 100%)

    Unaddressed P0 Requirements:
    {list unaddressed P0 requirements}

    CANNOT mark QA phase complete.

    How would you like to proceed?
    1. "address: [req_id]" - Implement missing requirement
    2. "investigate" - Show detailed gap analysis
    3. "escalate" - Flag for product decision
    ═══════════════════════════════════════════

    DO NOT proceed to "Update Progress"

  // 4. VERIFY outputs exist
  IF any output missing:
    LOG failures
    WAIT for user response

  // 5. ONLY THEN proceed
  LOG: "✅ VERIFICATION PASSED: P0=100%, all outputs exist"
  PROCEED to "Update Progress"

// ═══════════════════════════════════════════════════════════
// DEPENDENCY VALIDATION: Component Library Requirements
// ═══════════════════════════════════════════════════════════

FUNCTION validate_component_library_dependencies():
  """
  Validates that prototype package.json includes all required
  component library dependencies.

  SOURCE: .claude/templates/component-library/manifests/dependencies.json

  BLOCKING: Missing 'required' dependencies will FAIL verification
  WARNING: Missing 'optional' dependencies will warn if components detected
  """

  // 1. Load dependency manifest
  READ manifest = .claude/templates/component-library/manifests/dependencies.json

  // 2. Load prototype package.json
  READ package_json = prototype/package.json

  // 3. Validate required dependencies
  missing_required = []
  FOR each dep in manifest.categories.required.dependencies:
    IF dep NOT IN package_json.dependencies:
      APPEND dep to missing_required[]

  // 4. Check version compatibility
  version_mismatches = []
  FOR each dep in manifest.categories.required.dependencies:
    IF dep IN package_json.dependencies:
      required_version = manifest.categories.required.dependencies[dep].version
      actual_version = package_json.dependencies[dep]
      IF NOT compatible(required_version, actual_version):
        APPEND {dep, required_version, actual_version} to version_mismatches[]

  // 5. Check for optional dependencies (non-blocking warnings)
  optional_warnings = []
  IF screens use DatePicker/DateField/Calendar components:
    IF "@internationalized/date" NOT IN package_json.dependencies:
      APPEND "@internationalized/date required for date components" to optional_warnings[]

  IF screens use NumberField components:
    IF "@internationalized/number" NOT IN package_json.dependencies:
      APPEND "@internationalized/number required for number formatting" to optional_warnings[]

  // 6. Report results
  IF missing_required.length > 0 OR version_mismatches.length > 0:
    ═══════════════════════════════════════════
    ❌ DEPENDENCY VALIDATION FAILED
    ═══════════════════════════════════════════

    Missing Required Dependencies:
    FOR each dep in missing_required:
      • {dep} ({manifest.categories.required.dependencies[dep].version})
        Reason: {manifest.categories.required.dependencies[dep].reason}

    Version Mismatches:
    FOR each mismatch in version_mismatches:
      • {mismatch.dep}
        Required: {mismatch.required_version}
        Actual: {mismatch.actual_version}

    HOW TO FIX:
    1. Update prototype/package.json to include missing dependencies
    2. Run: cd prototype && npm install
    3. Re-run: /prototype-qa

    SOURCE: .claude/templates/component-library/manifests/dependencies.json
    ═══════════════════════════════════════════

    RETURN FAILED

  IF optional_warnings.length > 0:
    ═══════════════════════════════════════════
    ⚠️ OPTIONAL DEPENDENCY WARNINGS
    ═══════════════════════════════════════════

    FOR each warning in optional_warnings:
      • {warning}

    These are non-blocking but recommended for full functionality.
    ═══════════════════════════════════════════

  LOG: "✅ Component library dependencies validated"
  RETURN PASSED
```

### Step 9.6: Root Cause Tracing (Phase 4 Enhancement)

> **root-cause-tracing Integration**: When validation fails, systematically trace to root cause.

```
// ═══════════════════════════════════════════════════════════
// PHASE 4: ROOT CAUSE TRACING FOR VALIDATION FAILURES
// ═══════════════════════════════════════════════════════════

IF verification_gate_failed OR p0_coverage < 100%:

  LOG: "🔍 Initiating root cause tracing for validation failure..."

  // CORE PRINCIPLE: Trace backward through the call chain until you
  // find the original trigger, then fix at the source.

  // Step 1: OBSERVE THE SYMPTOM
  ═══════════════════════════════════════════
  🔍 ROOT CAUSE ANALYSIS - Step 1: Observe Symptom
  ═══════════════════════════════════════════

  Validation Failure Detected:
  - Failed Check: {which validation failed?}
  - Expected: {expected value}
  - Actual: {actual value}
  - Error Message: {error details}

  ═══════════════════════════════════════════

  // Categorize the failure
  FAILURE_TYPES = {
    "missing_output": "Required output file does not exist",
    "incomplete_output": "Output exists but is incomplete",
    "unaddressed_requirement": "P0 requirement not covered",
    "invalid_reference": "Output references non-existent artifact",
    "coverage_gap": "Coverage below required threshold"
  }

  IDENTIFY failure_type from FAILURE_TYPES

  // Step 2: FIND IMMEDIATE CAUSE
  ═══════════════════════════════════════════
  🔍 ROOT CAUSE ANALYSIS - Step 2: Immediate Cause
  ═══════════════════════════════════════════

  Tracing immediate cause of: {failure_type}

  CASE failure_type:

    "missing_output":
      ANALYZE:
        - Which skill should have generated this output?
        - Was that skill run? CHECK _state/progress.json
        - Did it complete successfully? CHECK skill status
        - What was the skill's output? CHECK prompt_log.json

      IMMEDIATE_CAUSE = {
        missing_file: "{file_path}",
        responsible_skill: "{skill_name}",
        skill_status: "{status}",
        skill_outputs: ["{actual outputs}"]
      }

    "unaddressed_requirement":
      ANALYZE:
        - Which requirement is unaddressed? {req_id}
        - What type of requirement? {functional/a11y/user_story}
        - Which artifact should address it?
        - Was the artifact generated?

      IMMEDIATE_CAUSE = {
        requirement_id: "{req_id}",
        requirement_type: "{type}",
        expected_artifact: "{artifact}",
        artifact_exists: true/false,
        artifact_mentions_req: true/false
      }

    "coverage_gap":
      ANALYZE:
        - Which requirements are unaddressed?
        - Which skills generate addressing artifacts?
        - Were those skills run completely?

      IMMEDIATE_CAUSE = {
        gap_count: N,
        unaddressed_reqs: ["{req_ids}"],
        responsible_skills: ["{skills}"]
      }

  ═══════════════════════════════════════════

  // Step 3: TRACE BACKWARDS (CRITICAL)
  ═══════════════════════════════════════════
  🔍 ROOT CAUSE ANALYSIS - Step 3: Trace Backwards
  ═══════════════════════════════════════════

  Building trace chain from symptom to source...

  TRACE_CHAIN = []

  // Level 1: What failed?
  TRACE_CHAIN.push({
    level: 1,
    what: "Validation check failed",
    detail: "{failure description}",
    file: "05-validation/{file}"
  })

  // Level 2: What was supposed to produce it?
  responsible_skill = identify_skill(failure_type)

  TRACE_CHAIN.push({
    level: 2,
    what: "Expected output from {responsible_skill}",
    detail: "Skill should generate {expected_output}",
    file: "skills/{responsible_skill}/SKILL.md"
  })

  // Level 3: Was the skill run?
  READ _state/progress.json
  skill_phase = progress.phases[responsible_skill]

  IF skill_phase.status != "complete":
    TRACE_CHAIN.push({
      level: 3,
      what: "Skill not completed",
      detail: "Status: {skill_phase.status}",
      ROOT_CAUSE: "Skill {responsible_skill} was not run or failed"
    })
  ELSE:
    // Level 4: Did it produce the expected output?
    READ _state/prompt_log.json
    skill_prompts = filter(skill == responsible_skill)

    IF skill_prompts are empty:
      TRACE_CHAIN.push({
        level: 3,
        what: "No prompt log entries",
        detail: "Skill claims complete but no logged prompts",
        ROOT_CAUSE: "Skill completed without generating content"
      })
    ELSE:
      // Level 5: Check specific step that should address requirement
      FOR each prompt in skill_prompts:
        IF prompt.should_address(failure_item):
          IF prompt.result.status != "success":
            TRACE_CHAIN.push({
              level: 4,
              what: "Step failed",
              detail: prompt.step + ": " + prompt.result.error,
              ROOT_CAUSE: "Specific step failed during generation"
            })
          ELSE:
            // Step succeeded but output doesn't address requirement
            TRACE_CHAIN.push({
              level: 4,
              what: "Step succeeded but incomplete",
              detail: "Output generated but doesn't address {req_id}",
              ROOT_CAUSE: "Generation logic missed requirement"
            })

  // Display trace chain
  ═══════════════════════════════════════════
  TRACE CHAIN:
  ═══════════════════════════════════════════

  FOR each trace in TRACE_CHAIN:
    Level {trace.level}: {trace.what}
    └─ {trace.detail}
    └─ File: {trace.file}
    {IF trace.ROOT_CAUSE: ">>> ROOT CAUSE IDENTIFIED <<<"}

  ═══════════════════════════════════════════

  // Step 4: ADD INSTRUMENTATION IF NEEDED
  IF root_cause unclear:
    ═══════════════════════════════════════════
    🔧 INSTRUMENTATION NEEDED
    ═══════════════════════════════════════════

    Unable to determine root cause from logs.

    Adding debug instrumentation:
    1. Enable verbose logging in {responsible_skill}
    2. Add checkpoint captures
    3. Re-run skill with instrumentation

    Command:
    "build only {responsible_skill} --verbose"
    ═══════════════════════════════════════════

  // Step 5: FIX AT SOURCE
  ═══════════════════════════════════════════
  🔧 ROOT CAUSE ANALYSIS - Step 5: Fix at Source
  ═══════════════════════════════════════════

  ROOT CAUSE: {root_cause_description}

  Recommended fix:

  CASE root_cause_type:

    "skill_not_run":
      ACTION: "Run missing skill"
      COMMAND: "build only {skill_name}"

    "skill_failed":
      ACTION: "Re-run failed skill with fixes"
      COMMAND: "build only {skill_name}"
      DETAILS: "Check skill inputs, review error logs"

    "generation_incomplete":
      ACTION: "Re-generate specific output"
      COMMAND: "build only {skill_name} --from step_{N}"
      DETAILS: "Ensure requirement {req_id} is addressed"

    "requirement_not_linked":
      ACTION: "Update artifact to address requirement"
      MANUAL_FIX: "Add 'Requirements Addressed' section to {artifact}"

    "data_propagation_error":
      ACTION: "Trace data from source"
      MANUAL_FIX: "Verify {data_item} flows correctly through pipeline"

  ═══════════════════════════════════════════

  // Offer fix options
  ═══════════════════════════════════════════
  How would you like to proceed?

  1. "auto-fix" - Attempt automatic fix: {recommended_action}
  2. "manual" - I'll fix it manually
  3. "investigate" - Show more details
  4. "skip" - Accept this gap (document why)
  ═══════════════════════════════════════════

  WAIT for user response

  IF user selects "auto-fix":
    EXECUTE recommended_action
    LOG: "Applied fix. Re-running validation..."
    GOTO Step 9.5 (re-run verification gate)

  IF user selects "investigate":
    DISPLAY detailed logs:
      - Full prompt_log.json entries for responsible_skill
      - File contents of expected output
      - requirements_registry entry for unaddressed req
      - Diff between expected and actual output

  IF user selects "skip":
    REQUIRE justification
    LOG: "Gap accepted with justification: {justification}"
    ADD to validation_report: "Accepted Gap: {req_id} - {justification}"

// DEFENSE IN DEPTH: Add validation at each layer
// (Prevents future occurrences of this root cause)

IF root_cause identified:
  ═══════════════════════════════════════════
  🛡️ DEFENSE IN DEPTH RECOMMENDATION
  ═══════════════════════════════════════════

  To prevent recurrence, consider adding validation at:

  Layer 1 (Source Skill):
    - Add output validation in {responsible_skill}
    - Check requirement addressing before marking complete

  Layer 2 (Pipeline):
    - Add inter-skill dependency check
    - Verify expected outputs exist before next phase

  Layer 3 (QA):
    - Already catching via this validation
    - Consider adding earlier smoke test

  Would you like to implement defense-in-depth? (y/n)
  ═══════════════════════════════════════════
```

### Step 10: Update Progress (Atomic Updates)

> **Phase 4 Enhancement**: Uses ProgressLock for atomic, corruption-proof updates

```python
# IMPORT progress lock utility
from progress_lock import ProgressLock

# UPDATE progress with atomic file locking
with ProgressLock('prototype') as progress:
    # All updates happen atomically
    # Automatically saved on exit, rolled back on exception
    progress['phases']['qa']['status'] = 'complete'
    progress['phases']['qa']['completed_at'] = datetime.now().isoformat()
    progress['phases']['qa']['outputs'] = [
        "05-validation/VALIDATION_REPORT.md",
        "05-validation/TRACEABILITY_MATRIX.md",
        "05-validation/REQUIREMENTS_COVERAGE.md",
        "05-validation/QA_CHECKLIST.md",
        "05-validation/accessibility/a11y-audit-results.md",
        "05-validation/accessibility/wcag-compliance.md"
    ]
    progress['phases']['qa']['validation'] = {
        'status': 'passed',
        'delivery_status': 'APPROVED',
        'p0_coverage': '100%',
        'p1_coverage': '92%',
        'p2_coverage': '67%',
        'a11y_issues_critical': 0
    }
    progress['phases']['qa']['metrics'] = {
        'total_requirements': total_reqs_count,
        'requirements_addressed': addressed_count,
        'p0_addressed': p0_addressed_count,
        'p0_total': p0_total_count
    }
    # Lock released and changes saved automatically here
```

**Benefits**:
- ✅ Prevents progress.json corruption during validation failures
- ✅ Automatic rollback if exception occurs during QA
- ✅ File locking prevents concurrent write conflicts
- ✅ Backup created before each update

---

## Output Files (REQUIRED)

| Path | Purpose | Blocking? |
|------|---------|-----------|
| `README.md` | Folder overview and process | ✅ Yes |
| `VALIDATION_REPORT.md` | Main validation results | ✅ Yes |
| `TRACEABILITY_MATRIX.md` | Requirement mapping with all sections | ✅ Yes |
| `REQUIREMENTS_COVERAGE.md` | Coverage summary | ✅ Yes |
| `QA_CHECKLIST.md` | Manual testing | ✅ Yes |
| `accessibility/a11y-audit-results.md` | A11Y findings | ✅ Yes |
| `accessibility/wcag-compliance.md` | WCAG status | ✅ Yes |
| `VALIDATION_REPORT_FINAL.md` | Sign-off document | ⚠️ After approval |

---

## Validation Rules

| Rule | Condition | Action |
|------|-----------|--------|
| P0 Coverage | Must be 100% | BLOCKS if < 100% |
| Critical A11Y | Must be 0 | BLOCKS if > 0 |
| Build | Must pass | BLOCKS if fails |
| P1 Coverage | Should be > 80% | WARNING if < 80% |

---

## Progress.json Update

```json
{
  "phases": {
    "qa": {
      "status": "complete",
      "completed_at": "2024-12-13T14:00:00Z",
      "outputs": [
        "05-validation/VALIDATION_REPORT.md",
        "05-validation/TRACEABILITY_MATRIX.md",
        "05-validation/REQUIREMENTS_COVERAGE.md",
        "05-validation/QA_CHECKLIST.md",
        "05-validation/accessibility/*.md"
      ],
      "validation": {
        "status": "passed",
        "delivery_status": "APPROVED",
        "p0_coverage": "100%",
        "p1_coverage": "92%",
        "p2_coverage": "67%"
      },
      "metrics": {
        "total_requirements": 58,
        "requirements_addressed": 50,
        "p0_addressed": 15,
        "p0_total": 15
      }
    }
  }
}
```
