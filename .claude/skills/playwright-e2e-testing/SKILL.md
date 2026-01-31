---
name: playwright-e2e-testing
description: Automate end-to-end testing with Playwright, AI-powered test generation, and comprehensive browser coverage for modern web applications.
model: sonnet
allowed-tools: Read, Write, Edit, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill playwright-e2e-testing started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill playwright-e2e-testing ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill playwright-e2e-testing instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Playwright E2E Testing Automation Skill

## What This Skill Enables

Claude can write, execute, and maintain end-to-end tests using Playwright, the modern browser automation framework that has overtaken Cypress in npm downloads as of 2025. This skill enables cross-browser testing (Chrome, Firefox, Safari/WebKit), AI-powered test generation with GitHub Copilot integration, and official MCP (Model Context Protocol) support for structured DOM interactions.

## Prerequisites

**Required:**
- Claude Pro subscription or Claude Code CLI
- Node.js 18+ installed
- Basic understanding of your application's user flows

**What Claude handles automatically:**
- Installing Playwright and browser binaries
- Generating test files with proper TypeScript types
- Setting up test configurations and reporters
- Writing selectors using accessibility snapshots
- Debugging test failures with traces and screenshots
- Optimizing tests for parallel execution

## How to Use This Skill

### Basic Test Generation

**Prompt:** "Create a Playwright test that logs into my application at localhost:3000, navigates to /dashboard, and verifies the welcome message appears."

Claude will:
1. Install Playwright if not present (`npm init playwright@latest`)
2. Generate a test file with proper page object patterns
3. Use accessibility-first selectors (role, label, text)
4. Include assertions with auto-retry logic
5. Add screenshot capture on failure

### AI-Powered Test Creation from User Stories

**Prompt:** "I have a checkout flow: user adds product to cart, enters shipping info, selects payment method, and completes order. Write comprehensive Playwright tests covering happy path and error cases."

Claude will:
1. Break down the user story into discrete test scenarios
2. Generate test files organized by feature
3. Include data-driven tests with fixtures
4. Add network mocking for payment gateway
5. Implement custom assertions for order confirmation
6. Set up test retry logic for flaky network calls

### Cross-Browser Testing Suite

**Prompt:** "Set up Playwright to test my application across Chrome, Firefox, and Safari with parallel execution. Include mobile viewport testing for iOS and Android."

Claude will:
1. Configure `playwright.config.ts` with multiple projects
2. Define desktop and mobile browser contexts
3. Set up parallel worker configuration
4. Configure test sharding for CI/CD
5. Add HTML reporter with trace viewer
6. Include screenshot comparison for visual regression

### API Testing Integration

**Prompt:** "Write Playwright tests that verify my REST API endpoints before running UI tests. Mock the API responses for offline testing."

Claude will:
1. Use Playwright's `request` context for API calls
2. Create API test fixtures for reusable setup
3. Implement request/response interception
4. Generate mock data with realistic values
5. Set up contract testing with schema validation
6. Add performance timing assertions

## Tips for Best Results

1. **Use Accessibility Selectors**: Playwright's MCP support leverages accessibility snapshots. Ask Claude to use `getByRole()`, `getByLabel()`, and `getByText()` instead of CSS selectors for more resilient tests.

2. **Parallel Execution**: Playwright's native parallelism is a key advantage. Request test organization that maximizes parallel worker usage with proper test isolation.

3. **Auto-Wait Smart Defaults**: Playwright automatically waits for elements to be actionable. Avoid explicit waits unless dealing with specific timing requirements.

4. **Trace on Failure**: Enable trace recording for CI environments to debug failures without reproducing locally: `--trace on-first-retry`.

5. **Codegen for Complex Flows**: For intricate user interactions, ask Claude to generate tests using `npx playwright codegen` output as a starting point.

6. **Test Sharding**: For large test suites in CI, request sharding configuration: `--shard=1/4` to split tests across multiple jobs.

## Common Workflows

### Complete E2E Test Suite Setup
```
"Set up a production-ready Playwright test suite for my Next.js app with:
1. Authentication flow tests with session storage
2. Visual regression testing with screenshot comparison
3. API mocking for external services
4. CI/CD integration with GitHub Actions
5. HTML report with trace viewer
6. Parallel execution across 4 workers"
```

### AI-Assisted Test Maintenance
```
"My application's login form changed from using email to username.
Update all Playwright tests that interact with the login form,
using accessibility selectors instead of data-testid attributes."
```

### Performance Testing
```
"Write Playwright tests that measure:
1. First Contentful Paint (FCP)
2. Largest Contentful Paint (LCP)
3. Time to Interactive (TTI)
4. Total Blocking Time (TBT)
Fail tests if any metric exceeds Web Vitals thresholds."
```

### Mobile-First Testing
```
"Create Playwright tests for mobile web experience:
1. Test on iPhone 13 and Pixel 5 viewports
2. Verify touch interactions (swipe, pinch-to-zoom)
3. Test offline mode with service worker
4. Validate responsive image loading
5. Check mobile-specific navigation menu"
```

## Troubleshooting

**Issue:** Tests are flaky and fail intermittently
**Solution:** Ask Claude to add explicit `waitForLoadState('networkidle')` calls, increase timeout for specific actions with `{ timeout: 10000 }`, or implement custom wait conditions with `page.waitForFunction()`.

**Issue:** Selectors break when UI changes
**Solution:** Request migration to accessibility selectors (`getByRole`, `getByLabel`) which are more resilient to DOM structure changes. Playwright's MCP integration makes this the preferred approach.

**Issue:** Tests run too slowly in CI
**Solution:** Ask Claude to implement test sharding across multiple GitHub Actions jobs, optimize test setup with global authentication fixtures, and enable trace recording only on failure.

**Issue:** Cannot test third-party authentication (OAuth, SSO)
**Solution:** Request implementation of authentication state storage with `storageState` option, bypassing the login flow for most tests while keeping one dedicated authentication test.

**Issue:** Screenshot comparison fails due to font rendering differences
**Solution:** Ask Claude to configure Playwright's `maxDiffPixels` or `threshold` options, or use textual assertions instead of visual regression for text-heavy areas.

## Learn More

- [Playwright Official Documentation](https://playwright.dev/)
- [Playwright MCP Integration Guide](https://github.com/microsoft/playwright/blob/main/docs/src/mcp.md)
- [Playwright vs Cypress 2025 Comparison](https://playwright.dev/docs/why-playwright)
- [AI-Powered Testing with Playwright](https://playwright.dev/docs/codegen)
- [Playwright Test Best Practices](https://playwright.dev/docs/best-practices)


## Key Features

- Cross-browser testing: Chrome, Firefox, Safari (WebKit)
- AI-powered test generation with GitHub Copilot
- MCP support for accessibility-driven interactions
- Native parallel execution and test sharding

## Use Cases

- End-to-end testing for web applications
- Visual regression testing with screenshots
- API testing and contract validation

## Examples

### Example 1: Basic E2E Test with Authentication

```typescript
import { test, expect } from '@playwright/test';

test.describe('Dashboard Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('http://localhost:3000/login');
    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Sign In' }).click();
    await page.waitForURL('**/dashboard');
  });

  test('displays welcome message', async ({ page }) => {
    const heading = page.getByRole('heading', { name: /welcome/i });
    await expect(heading).toBeVisible();
  });

  test('loads user profile data', async ({ page }) => {
    await page.getByRole('link', { name: 'Profile' }).click();
    await expect(page.getByText('user@example.com')).toBeVisible();
  });
});
```

### Example 2: API Testing with Request Context

```typescript
import { test, expect } from '@playwright/test';

test.describe('API Tests', () => {
  test('GET /api/users returns valid data', async ({ request }) => {
    const response = await request.get('http://localhost:3000/api/users');
    expect(response.ok()).toBeTruthy();
    
    const users = await response.json();
    expect(users).toHaveLength(10);
    expect(users[0]).toHaveProperty('email');
  });

  test('POST /api/users creates new user', async ({ request }) => {
    const response = await request.post('http://localhost:3000/api/users', {
      data: {
        name: 'Test User',
        email: 'test@example.com'
      }
    });
    expect(response.status()).toBe(201);
    
    const user = await response.json();
    expect(user.id).toBeDefined();
  });
});
```

### Example 3: Parallel Test Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: [['html'], ['json', { outputFile: 'test-results.json' }]],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 13'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Troubleshooting

### Browser binaries not found

Run 'npx playwright install' to download Chromium, Firefox, and WebKit binaries.

### Tests timeout in CI

Increase timeout in config: use: { actionTimeout: 10000, navigationTimeout: 30000 }

### Selectors not found

Use accessibility selectors (getByRole, getByLabel) instead of CSS selectors. Enable MCP integration for better selector generation.

## Learn More

For additional documentation and resources, visit:

https://playwright.dev/
