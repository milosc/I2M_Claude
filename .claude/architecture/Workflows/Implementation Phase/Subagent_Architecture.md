# Subagent Architecture

## Overview

The HTEC ClaudeCode Accelerators framework uses a multi-agent architecture where specialized subagents handle different aspects of implementation tasks. This document explains how subagents are spawned, coordinated, and how they collaborate to deliver high-quality results.

**Updated**: Now includes Stage 1 Discovery agents and the Chef Product Manager Reviewer quality gate.

## Agent Taxonomy

```
┌───────────────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                                  │
│  /discovery, /prototype, /htec-sdd commands spawn agents                  │
└───────────────────────────────────────────────────────────────────────────┘
                                          │
                                          │ Task Isolation Mode (v2.1+)
                                          ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                      TASK ORCHESTRATOR LAYER (NEW in v2.1)                │
│  implementation-task-orchestrator (1 per task, isolated context)          │
│  • Spawned by /htec-sdd-implement for each task                          │
│  • Runs full 8-phase workflow in isolated context                         │
│  • Prevents context memory rot across multiple tasks                      │
│  • Saves results to Implementation_<System>/01-tasks/<T-ID>/results/      │
└───────────────────────────────────────────────────────────────────────────┘
                                          │
            ┌─────────────────────────────┼──────────────────────────┐
            ▼                             ▼                          ▼
┌──────────────────────┐ ┌─────────────────────────────┐ ┌───────────────────┐
│  PLANNING AGENTS     │ │IMPLEMENTATION               │ │  QUALITY AGENTS   │
│                      │ │   AGENTS                    │ │                   │
├──────────────────────┤ ├─────────────────────────────┤ ├───────────────────┤
│ • tech-lead          │ │ • developer                 │ │ • bug-hunter      │
│ • product-researcher │ │   (1 per task in v2.1+)     │ │ • security-auditor│
│ • hfe-ux-researcher  │ │ • test-automation-engineer  │ │ • code-quality    │
│ • code-explorer      │ │ • test-designer             │ │ • test-coverage   │
│ • interview-analyst  │ │                             │ │ • contracts-rev   │
│ • pdf-analyst        │ │                             │ │ • a11y-auditor    │
│ • data-analyst       │ │                             │ │ • fact-auditor    │
│ • design-analyst     │ │                             │ │   -reviewer       │
└──────────────────────┘ └─────────────────────────────┘ └───────────────────┘
                                          │
                    ┌─────────────────────┴─────────────────────┐
                    ▼                                           ▼
┌───────────────────────────────────────┐ ┌───────────────────────────────────┐
│  PROCESS INTEGRITY AGENTS             │ │  REFLEXION JUDGES                 │
│  (Continuous Monitoring)              │ │  (Multi-Perspective Critique)     │
├───────────────────────────────────────┤ ├───────────────────────────────────┤
│ • traceability-guardian               │ │ • requirements-validator          │
│ • state-watchdog                      │ │ • solution-architect              │
│ • checkpoint-auditor                  │ │ • code-quality-reviewer           │
│ • playbook-enforcer                   │ │                                   │
└───────────────────────────────────────┘ └───────────────────────────────────┘
```

### 0. Task Orchestrator Agent (NEW in v2.1)

| Agent | Purpose | Spawned By | Context |
|-------|---------|------------|---------|
| `implementation-task-orchestrator` | Full 8-phase workflow per task in isolated context | `/htec-sdd-implement` dispatcher | Isolated (prevents context rot) |

**Key Features**:
- Spawned for each task when `--isolate-tasks=true` (default)
- Runs complete workflow: Research → Planning → Test Design → TDD → Test Automation → Quality Review → Documentation → PR Prep
- Saves all outputs to `Implementation_<System>/01-tasks/<T-ID>/results/`
- Returns compact JSON summary to parent dispatcher
- Maximum concurrent agents controlled by `--batch` (default: 2)

**Agent Definition**: `.claude/agents/implementation-task-orchestrator.md`

**Results Structure** (per task):
```
Implementation_<System>/01-tasks/<T-ID>/results/
├── execution.json          # Full execution record with all phases
├── implementation_plan.md  # Phase 2 output
├── test_spec.md            # Phase 3 output
├── build.log               # Phase 4 build output
├── test.log                # Phase 4 test output
├── e2e_test.log            # Phase 5 E2E output
├── quality_report.json     # Phase 6 findings
└── pr_description.md       # Phase 7 PR prep
```

**Invocation Pattern** (by dispatcher):
```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Orchestrate implementation for T-018",
  run_in_background: true,
  prompt: `Agent: implementation-task-orchestrator
Read: .claude/agents/implementation-task-orchestrator.md
TASK_ID: T-018
SYSTEM_NAME: ERTriage
PR_GROUP: PR-005
...
RETURN: JSON { task_id, status, duration_seconds, phases_completed, ... }`
})
```

---

### 1. Planning Agents

| Agent | Purpose | When Used |
|-------|---------|-----------|
| `tech-lead` | Breaks stories into technical tasks, defines build order | Task decomposition (Stage 5) |
| `product-researcher` | Conducts market analysis, competitive research, industry trends via web research | Discovery, Prototype, SolArch |
| `hfe-ux-researcher` | Studies human-system interactions, researches UX best practices | Discovery, Prototype |
| `researcher` | Investigates unknown technologies, libraries | Research phase |
| `code-explorer` | Analyzes existing codebase features, maps architecture | Code understanding |
| `interview-analyst` | Analyzes interview transcripts, extracts insights and quotes | Discovery (Stage 1) |
| `pdf-analyst` | Deep PDF analysis with chunking and concept extraction | Discovery (Stage 1) |
| `data-analyst` | Analyzes spreadsheets and structured data | Discovery (Stage 1) |
| `design-analyst` | Analyzes screenshots, wireframes, and visual materials | Discovery (Stage 1) |
| `software-architect` | Designs feature architectures, provides blueprints | Architecture design |
| `business-analyst` | Transforms business needs into requirements | Requirements phase |

### 2. Implementation Agents

| Agent | Purpose | Concurrency |
|-------|---------|-------------|
| `developer` | Executes TDD implementation with strict acceptance criteria | Up to 3 parallel |
| `test-automation-engineer` | Builds E2E testing framework, integration tests after developers complete TDD cycles | Sequential (post-TDD) |

### 3. Quality Agents (Code Review & Specification Review)

**Stage 5 - Code Review**:

| Agent | Focus | Severity Weight |
|-------|-------|-----------------|
| `code-review-bug-hunter` | Logic errors, edge cases, null safety | HIGH |
| `code-review-security-auditor` | OWASP Top 10, injection, auth | CRITICAL |
| `code-review-code-quality` | SOLID, DRY, complexity, patterns | MEDIUM |
| `code-review-test-coverage` | Missing tests, edge cases, mocking | HIGH |
| `code-review-contracts` | API compliance, type safety | HIGH |
| `accessibility-auditor` | WCAG, a11y patterns | MEDIUM |

**Stages 1-4 - Specification Review**:

| Agent | Focus | Stage(s) |
|-------|-------|----------|
| `fact-auditor-reviewer` | **Factuality, hallucination detection, citation enforcement** | **Discovery (CP-9.5)** |
| `spec-reviewer` | Specification clarity, completeness, consistency | All |
| `cross-validator` | Cross-artifact relationships, traceability | All |
| `accessibility-auditor` | A11y requirements in specs (not code) | Prototype, ProductSpecs |
| `security-auditor` | PII, auth flows, data handling in specs | Discovery, ProductSpecs, SolArch |

**New in v3.1**: `fact-auditor-reviewer` is the Chef Product Manager Reviewer agent (Agent ID: `discovery:fact-auditor-reviewer`). It validates ClientAnalysis materials for factuality and blocks pipeline if P0 hallucinations are found.

### 4. Reflexion Judges (Multi-Perspective Critique)

Used during the REFLECT phase for deep analysis:

| Judge | Evaluation Focus |
|-------|------------------|
| **REQUIREMENTS VALIDATOR** | Alignment with original request, acceptance criteria, scope creep, traceability |
| **SOLUTION ARCHITECT** | Technical soundness, architecture patterns, technical debt, performance |
| **CODE QUALITY REVIEWER** | Clean code, test adequacy, documentation, error handling |

### 5. Process Integrity Agents (Continuous Monitoring)

Ensure all agents follow the playbook and maintain artifact consistency:

| Agent | Focus | Trigger | Scope |
|-------|-------|---------|-------|
| `traceability-guardian` | Validates ID chains (PP→JTBD→REQ→SCR→MOD→T), ensures cross-references exist | After each artifact creation | All Stages |
| `state-watchdog` | Monitors `_state/*.json` files, validates progress tracking, detects stale state | Continuous, every phase transition | All Stages |
| `checkpoint-auditor` | Validates checkpoint requirements before allowing phase progression | Before each checkpoint gate | All Stages |
| `playbook-enforcer` | Ensures agents follow defined workflows, detects process violations | Continuous, on agent output | Stages 4-5 |

**Operating Mode:** These agents run as background monitors with veto power over phase transitions.

---

## Spawning Subagents

### The Task() Function

Subagents are spawned using the `Task()` tool with specific parameters:

```
Task(
    subagent_type: string,     # Type of specialized agent
    prompt: string,            # Task instructions
    run_in_background: bool,   # true for parallel execution
    model: string              # "sonnet" | "opus" | "haiku"
)
```

### Example: Spawning a Single Agent

```
agent = Task(
    subagent_type="developer",
    prompt="Implement the inventory item validation using TDD...",
    run_in_background=false,
    model="sonnet"
)
```

### Example: Spawning Parallel Agents

```
# Spawn 6 code review agents simultaneously
AGENTS = []

FOR EACH agent_type IN ["bug-hunter", "security-auditor", "code-quality",
                        "test-coverage", "contracts-reviewer", "accessibility-auditor"]:
    agent = Task(
        subagent_type=f"code-review-{agent_type}",
        prompt=generate_agent_prompt(agent_type, FILES),
        run_in_background=true,
        model="sonnet"
    )
    AGENTS.append(agent)
```

### Waiting for Completion

```
# Wait for all agents to complete
RESULTS = []
FOR EACH agent IN AGENTS:
    result = TaskOutput(agent.id, block=true)
    RESULTS.append(result)
```

---

## Parallel Execution Model

### Execution Rules

```
PARALLEL EXECUTION RULES:

1. MAX_CONCURRENT_AGENTS = 4 (for implementation, 3 developers, 1 test automation engineer)
2. NO_LIMIT for read-only agents (code review)
3. FILE_LOCKING prevents concurrent writes to same file
4. SHARED_CONTEXT via traceability/ and _state folders folder
```

### Task Markers

Tasks are marked with execution mode indicators:

| Marker | Meaning |
|--------|---------|
| `[P]` | Parallel - Can run concurrently |
| `[S]` | Sequential - Must wait for predecessors |
| `[B]` | Blocking - Stops pipeline on failure |
| `[C]` | Continuous - Background monitoring throughout execution |

### Phase Execution Pattern

```
PHASE EXECUTION:

╔═══════════════════════════════════════════════════════════════════════════╗
║  PROCESS INTEGRITY LAYER (Continuous Background Monitoring)               ║
║  [C] traceability-guardian: Validate ID chains on every artifact write    ║
║  [C] state-watchdog: Monitor _state/*.json for drift/corruption           ║
║  [C] playbook-enforcer: Ensure agents follow workflow rules               ║
╚═══════════════════════════════════════════════════════════════════════════╝
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
1. PARALLEL PHASE (Research & Planning)
   [P] tech-lead: Break down task
   [P] code-explorer: Analyze codebase
   [P] researcher: Research unknowns
   [P] product-researcher: Market/competitive analysis (web)
   [P] hfe-ux-researcher: UX best practices research (web)

   BARRIER: Wait for all planning agents
   INTEGRITY CHECK: checkpoint-auditor validates planning outputs

2. SEQUENTIAL PHASE (Implementation)
   [S] developer-1: Implement Module A (TDD)
        └─ playbook-enforcer: Verify TDD compliance (RED→GREEN→REFACTOR)
   [S] developer-2: Implement Module B (TDD, after A)
        └─ playbook-enforcer: Verify TDD compliance
   [S] developer-3: Implement Module C (TDD, after B)
        └─ playbook-enforcer: Verify TDD compliance

   INTEGRITY CHECK: traceability-guardian validates all T-XXX → MOD-XXX links

3. SEQUENTIAL PHASE (Test Automation)
   [S] test-automation-engineer: Integration tests (after each TDD cycle)
   [S] test-automation-engineer: E2E test suite (after feature complete)

   INTEGRITY CHECK: checkpoint-auditor validates test coverage

4. PARALLEL PHASE (Quality)
   [P] bug-hunter: Find bugs
   [P] security-auditor: Find vulnerabilities
   [P] code-quality: Check patterns
   [P] test-coverage: Verify tests
   [P] contracts-reviewer: Check APIs
   [P] accessibility-auditor: Check a11y

   BARRIER: Wait for all quality agents
   INTEGRITY CHECK: state-watchdog validates review_registry.json

5. BLOCKING GATE
   [B] IF any CRITICAL findings → STOP
   [B] IF any HIGH findings (>80% confidence) → STOP
   [B] IF integration tests fail → STOP
   [B] IF E2E critical journeys fail → STOP
   [B] IF process integrity violations (CRITICAL) → STOP
   [B] IF traceability coverage < 100% (P0) → STOP
```

---

## Agent Context Inheritance

Each subagent receives context from multiple sources:

```
┌──────────────────────────────────────────────────────────────┐
│                    CONTEXT LAYERS                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. PROJECT CONTEXT (from CLAUDE.md)                         │
│     ├─ Project overview                                      │
│     ├─ Directory structure                                   │
│     └─ Error handling rules                                  │
│                                                              │
│  2. TASK CONTEXT (from task_registry.json)                   │
│     ├─ Current task details                                  │
│     ├─ Acceptance criteria                                   │
│     └─ Dependencies                                          │
│                                                              │
│  3. CODE CONTEXT (from source files)                         │
│     ├─ Files to analyze/modify                               │
│     ├─ Existing patterns                                     │
│     └─ Test examples                                         │
│                                                              │
│  4. TRACEABILITY CONTEXT (from traceability/)                │
│     ├─ Requirements mapping                                  │
│     ├─ Screen registry                                       │
│     ├─ Change request history                                │
│     └─ Client Facts (Quotes/Transcripts)                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Context Passing Example

```
agent_prompt = f"""
## Task Context
Task ID: {task.id}
Description: {task.description}
Acceptance Criteria:
{task.acceptance_criteria}

## Code Context
Files to review:
{file_list}

## Traceability
Requirement: {task.requirement_ref}
Screen: {task.screen_ref}

## Instructions
{agent_specific_instructions}
"""

Task(
    subagent_type="code-review-bug-hunter",
    prompt=agent_prompt,
    run_in_background=true
)
```

---

## Confidence Thresholds

Each agent finding includes a confidence score. Thresholds determine blocking:

| Severity | Confidence Threshold | Action |
|----------|---------------------|--------|
| CRITICAL | 50% | Always blocks |
| HIGH | 65% | Blocks if > 80% |
| MEDIUM | 75% | Review recommended |
| LOW | 85% | Informational |

### Finding Structure

```json
{
    "id": "BH-001",
    "agent": "bug-hunter",
    "severity": "high",
    "confidence": 85,
    "file": "src/hooks/use-inventory.ts",
    "line": 45,
    "code": "const items = result.data.items;",
    "issue": "Potential null access on result.data",
    "suggestion": "Add optional chaining: result.data?.items ?? []",
    "category": "null-safety"
}
```

---

## Agent Specialization Details

### Bug Hunter Agent

**Analysis Dimensions (Fishbone):**

```
                    ┌── TECHNOLOGY
                    │   ├─ Race conditions
                    │   ├─ Memory leaks
                    │   └─ Type coercion
                    │
                    ├── METHODS
                    │   ├─ Algorithm errors
                    │   ├─ Off-by-one
                    │   └─ Boundary conditions
                    │
BUG ◄───────────────┼── PROCESS
                    │   ├─ Missing validation
                    │   ├─ Error handling gaps
                    │   └─ State management
                    │
                    ├── ENVIRONMENT
                    │   ├─ Async timing
                    │   └─ Resource constraints
                    │
                    └── MATERIALS (Data)
                        ├─ Null/undefined
                        ├─ Empty arrays
                        └─ Invalid formats
```

**Detection Categories:**
- NULL SAFETY: Optional chaining, null checks, undefined handling
- ASYNC ISSUES: Missing await, unhandled rejections, race conditions
- LOGIC ERRORS: Off-by-one, incorrect conditionals, type coercion
- EDGE CASES: Empty arrays, zero values, boundary conditions

### Security Auditor Agent

**OWASP Top 10 Coverage:**

| ID | Category | Checks |
|----|----------|--------|
| A01:2021 | Broken Access Control | Auth checks, privilege escalation |
| A02:2021 | Cryptographic Failures | Weak encryption, exposed secrets |
| A03:2021 | Injection | SQL, NoSQL, command, XSS |
| A04:2021 | Insecure Design | Missing threat modeling |
| A05:2021 | Security Misconfiguration | Debug mode, verbose errors |
| A06:2021 | Vulnerable Components | Outdated dependencies |
| A07:2021 | Auth Failures | Weak passwords, session issues |
| A08:2021 | Integrity Failures | Unsigned updates, CI/CD issues |
| A09:2021 | Logging Failures | Missing audit logs |
| A10:2021 | SSRF | Server-side request forgery |

**Security Checklist (20+ items):**
- Hardcoded credentials
- SQL injection vulnerabilities
- XSS attack vectors
- Insecure session handling
- Missing input validation
- PII in logs
- Debug mode enabled
- Verbose error exposure

### Code Quality Agent

**Analysis Focus:**

1. **COMPLEXITY**
   - Functions > 50 lines
   - Cyclomatic complexity > 10
   - Nesting depth > 3

2. **SOLID VIOLATIONS**
   - Single Responsibility
   - Open/Closed
   - Liskov Substitution
   - Interface Segregation
   - Dependency Inversion

3. **DRY VIOLATIONS**
   - Duplicate code blocks
   - Copy-paste patterns
   - Repeated logic

4. **NAMING/CLARITY**
   - Poor variable names
   - Magic numbers
   - Missing comments for complex logic

### Product Researcher Agent

**Research Dimensions:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PRODUCT RESEARCH FRAMEWORK                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  1. MARKET ANALYSIS                                                     │
│     ├─ Market size and growth trends                                    │
│     ├─ Target segments and demographics                                 │
│     ├─ Industry regulations and compliance                              │
│     └─ Emerging market opportunities                                    │
│                                                                         │
│  2. COMPETITIVE ANALYSIS                                                │
│     ├─ Direct competitors (feature comparison)                          │
│     ├─ Indirect competitors (alternative solutions)                     │
│     ├─ Competitive positioning matrix                                   │
│     └─ Pricing strategies and business models                           │
│                                                                         │
│  3. TREND ANALYSIS                                                      │
│     ├─ Technology trends affecting the domain                           │
│     ├─ User behavior shifts                                             │
│     ├─ Regulatory changes on the horizon                                │
│     └─ Innovation opportunities                                         │
│                                                                         │
│  4. BEST PRACTICES                                                      │
│     ├─ Industry standards and benchmarks                                │
│     ├─ Success patterns from market leaders                             │
│     ├─ Common pitfalls and anti-patterns                                │
│     └─ Recommended approaches with evidence                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Output Deliverables:**
- MARKET_ANALYSIS.md - Market size, segments, trends
- COMPETITIVE_LANDSCAPE.md - Competitor matrix with strengths/weaknesses
- TREND_REPORT.md - Industry trends and implications
- RECOMMENDATIONS.md - Strategic recommendations with evidence

**Web Research Strategy:**
- Search industry reports and analyst publications
- Analyze competitor websites and product documentation
- Review industry forums and community discussions
- Extract insights from case studies and whitepapers

### HFE/UX Researcher Agent

**Human Factors Research Framework:**

```
                      ┌── USER COGNITION
                      │   ├─ Mental models
                      │   ├─ Cognitive load analysis
                      │   └─ Decision-making patterns
                      │
                      ├── INTERACTION PATTERNS
                      │   ├─ Task flow optimization
                      │   ├─ Error prevention strategies
                      │   └─ Feedback mechanisms
                      │
UX RESEARCH ◄─────────┼── ACCESSIBILITY
                      │   ├─ WCAG compliance patterns
                      │   ├─ Assistive technology support
                      │   └─ Inclusive design principles
                      │
                      ├── USABILITY HEURISTICS
                      │   ├─ Nielsen's 10 heuristics
                      │   ├─ Fitts's law application
                      │   └─ Hick's law considerations
                      │
                      └── DESIGN SYSTEMS
                          ├─ Component best practices
                          ├─ Responsive design patterns
                          └─ Platform conventions (iOS/Android/Web)
```

**Analysis Categories:**

| Category | Focus Areas | Deliverables |
|----------|-------------|--------------|
| **User Research** | Personas, journey maps, task analysis | UX_PERSONAS.md, JOURNEY_MAPS.md |
| **Interaction Design** | Information architecture, navigation, workflows | INTERACTION_PATTERNS.md |
| **Visual Design** | Layout patterns, typography, color usage | VISUAL_GUIDELINES.md |
| **Accessibility** | WCAG compliance, screen reader support | A11Y_REQUIREMENTS.md |
| **Usability** | Heuristic evaluation, cognitive walkthrough | USABILITY_REPORT.md |

**Proposal Output Format:**
```json
{
    "id": "UX-001",
    "category": "interaction-pattern",
    "problem": "Complex multi-step form with high abandonment",
    "research_sources": ["NN/g study", "Baymard Institute"],
    "options": [
        {
            "name": "Progressive Disclosure",
            "description": "Break form into wizard steps",
            "pros": ["Reduces cognitive load", "Clear progress"],
            "cons": ["More clicks", "Harder to review all fields"],
            "evidence": "23% completion rate improvement (NN/g)"
        },
        {
            "name": "Inline Validation",
            "description": "Real-time field validation with smart defaults",
            "pros": ["Immediate feedback", "Fewer errors"],
            "cons": ["Can feel intrusive", "Implementation complexity"],
            "evidence": "22% error reduction (Baymard)"
        }
    ],
    "recommendation": "Progressive Disclosure",
    "confidence": 85
}
```

### Test Automation Engineer Agent

**Testing Framework Architecture:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    E2E TESTING FRAMEWORK                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  EXECUTION TIMING: After developers complete TDD cycle on each unit    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ DEVELOPER TDD CYCLE                                              │   │
│  │  RED → GREEN → REFACTOR → UNIT TESTS PASS                       │   │
│  └────────────────────────────┬────────────────────────────────────┘   │
│                               │                                         │
│                               ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ TEST AUTOMATION ENGINEER                                         │   │
│  │  Integration Tests → E2E Tests → Performance Tests               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Test Pyramid Coverage:**

```
              ┌───────────┐
              │   E2E     │  ← Critical user journeys (5-10%)
              │   Tests   │     Playwright/Cypress
              ├───────────┤
              │Integration│  ← API contracts, service mesh (20-30%)
              │   Tests   │     Supertest, MSW
              ├───────────┤
              │   Unit    │  ← Component logic (60-70%)
              │   Tests   │     Jest, Vitest (by developers)
              └───────────┘
```

**Responsibilities:**

| Phase | Activity | Output |
|-------|----------|--------|
| **Framework Setup** | Configure test runners, CI integration, reporting | `tests/e2e/`, `playwright.config.ts` |
| **Integration Tests** | API contract validation, service integration | `tests/integration/*.test.ts` |
| **E2E Tests** | Critical user journey automation | `tests/e2e/journeys/*.spec.ts` |
| **Performance Tests** | Load testing, response time validation | `tests/performance/` |
| **Visual Regression** | Screenshot comparison, UI consistency | `tests/visual/` |

**E2E Test Structure:**

```typescript
// tests/e2e/journeys/inventory-management.spec.ts
describe('Inventory Management Journey', () => {
    // Traceability: JTBD-1.1, US-1.1, SCR-001

    beforeAll(async () => {
        await setupTestData('inventory-baseline');
    });

    test('user can add new inventory item', async () => {
        // Given: User is on inventory dashboard
        // When: User clicks "Add Item" and fills form
        // Then: Item appears in inventory list
    });

    test('user can update stock levels', async () => {
        // Given: Existing item with stock level 100
        // When: User adjusts stock to 150
        // Then: Stock level updates and audit log created
    });
});
```

**Coordination with Developers:**

```
HANDOFF PROTOCOL:

1. DEVELOPER completes TDD cycle for Task T-XXX
   - Unit tests: ✅ All passing
   - Coverage: ≥ 80%
   - Status: READY_FOR_INTEGRATION

2. TEST AUTOMATION ENGINEER receives notification
   - Reviews task acceptance criteria
   - Identifies integration points
   - Writes integration/E2E tests

3. INTEGRATION TEST RESULTS
   - Pass → Task moves to code review
   - Fail → Returns to developer with failure details

4. E2E TEST SUITE
   - Runs on full feature completion
   - Validates end-to-end user journeys
   - Reports coverage by requirement
```

**Quality Gates:**

| Gate | Criteria | Blocking |
|------|----------|----------|
| Integration | All API contracts valid | YES |
| E2E Critical | All P0 journeys pass | YES |
| E2E Extended | All P1 journeys pass | NO (warning) |
| Performance | Response time < 2s (P95) | NO (warning) |
| Visual | No unintended UI changes | NO (review required) |

### Process Integrity Agents

**Continuous Monitoring Architecture:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PROCESS INTEGRITY LAYER                              │
│                    (Runs continuously in background)                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐         │
│  │  TRACEABILITY   │  │     STATE       │  │   CHECKPOINT    │         │
│  │    GUARDIAN     │  │    WATCHDOG     │  │    AUDITOR      │         │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘         │
│           │                    │                    │                   │
│           ▼                    ▼                    ▼                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    PLAYBOOK ENFORCER                             │   │
│  │         (Aggregates violations, issues STOP/WARN/INFO)           │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                │                                        │
│                                ▼                                        │
│                    ┌───────────────────────┐                           │
│                    │   INTEGRITY VERDICT   │                           │
│                    │   PASS / BLOCK        │                           │
│                    └───────────────────────┘                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Traceability Guardian

**Validation Rules:**

```
TRACEABILITY CHAIN VALIDATION:

1. FORWARD TRACING (Discovery → Implementation)
   CM-XXX → PP-X.X → JTBD-X.X → REQ-XXX → SCR-XXX → MOD-XXX → T-XXX

   CHECK: Every ID references a valid parent
   CHECK: No orphan artifacts (must trace to client material)
   CHECK: No broken links (referenced IDs must exist)

2. BACKWARD TRACING (Implementation → Discovery)
   T-XXX → MOD-XXX → SCR-XXX → REQ-XXX → JTBD-X.X → PP-X.X → CM-XXX

   CHECK: Every implementation task traces to requirement
   CHECK: Coverage analysis (are all requirements implemented?)

3. CROSS-REFERENCE VALIDATION
   CHECK: traceability/*.json files are consistent
   CHECK: screen_registry.json matches screen-definitions.md
   CHECK: task_registry.json matches TASK_INDEX.md
```

**Violation Severity:**

| Violation | Severity | Action |
|-----------|----------|--------|
| Broken ID reference | CRITICAL | Block phase transition |
| Orphan artifact (no parent) | HIGH | Block + require fix |
| Missing coverage (P0 req) | HIGH | Block phase transition |
| Missing coverage (P1/P2 req) | MEDIUM | Warning, allow proceed |
| Stale reference (deleted parent) | HIGH | Block + require cleanup |

#### State Watchdog

**Monitored Files:**

```
_state/
├── discovery_config.json      ← Config immutability check
├── discovery_progress.json    ← Progress consistency
├── prototype_config.json      ← Cross-stage config alignment
├── prototype_progress.json    ← Checkpoint sequence validation
├── productspecs_config.json   ← Input validation status
├── implementation_config.json ← Task registry sync
└── FAILURES_LOG.md            ← Error accumulation monitoring
```

**Validation Rules:**

| Check | Rule | Trigger |
|-------|------|---------|
| Config drift | Config unchanged after initialization | Every phase |
| Progress monotonicity | Checkpoints only increase, never decrease | Phase transition |
| Cross-stage alignment | Stage N config matches Stage N-1 outputs | Stage start |
| Failure threshold | FAILURES_LOG.md entries < 10% of operations | Continuous |
| Stale state detection | Last modified < 1 hour if agent active | Every 15 min |

**Alert Output:**

```json
{
    "agent": "state-watchdog",
    "timestamp": "2024-01-15T10:30:00Z",
    "severity": "HIGH",
    "violation": "config_drift",
    "file": "_state/prototype_config.json",
    "details": "SYSTEM_NAME changed from 'InventorySystem' to 'InvSystem'",
    "expected": "InventorySystem",
    "actual": "InvSystem",
    "action": "BLOCK",
    "remediation": "Restore original config or re-run /prototype-init"
}
```

#### Checkpoint Auditor

**Pre-Checkpoint Validation:**

```
BEFORE allowing checkpoint N → N+1:

1. REQUIRED FILES CHECK
   - All files listed in checkpoint requirements exist
   - Files are non-empty and valid format (JSON parseable, MD has content)

2. QUALITY GATE CHECK
   - Previous checkpoint quality gates passed
   - No CRITICAL findings unresolved
   - Coverage thresholds met

3. DEPENDENCY CHECK
   - All declared dependencies from previous checkpoints satisfied
   - Input files from upstream stages available

4. CONSISTENCY CHECK
   - Artifact counts match (e.g., # screens in registry = # screen folders)
   - ID sequences are contiguous (no gaps)
```

**Checkpoint Gate Matrix:**

| From CP | To CP | Required Validations |
|---------|-------|---------------------|
| 0 → 1 | | Config exists, folders created |
| 1 → 2 | | Input validation passed, summary generated |
| 2 → 3 | | Requirements extracted, registry populated |
| N → N+1 | | All CP-N files exist + quality gates pass |
| Any → Final | | 100% P0 coverage, all blocking gates passed |

#### Playbook Enforcer

**Workflow Compliance Checks:**

```
PLAYBOOK RULES:

1. PHASE ORDERING
   - Planning must complete before Implementation
   - Implementation must complete before Quality Review
   - Quality Review must pass before Phase Transition
   - VIOLATION: Starting implementation without tech-lead output

2. AGENT OUTPUT COMPLIANCE
   - Agent outputs match expected schema
   - Required sections present in markdown outputs
   - Traceability IDs included where required
   - VIOLATION: Missing traceability footer in PAIN_POINTS.md

3. TDD COMPLIANCE (for developers)
   - Test file created before implementation file
   - Test initially fails (RED phase logged)
   - Implementation makes test pass (GREEN phase logged)
   - VIOLATION: Implementation without failing test

4. ARTIFACT NAMING
   - Files follow naming conventions (UPPERCASE.md, kebab-case.json)
   - IDs follow format (PP-X.X, JTBD-X.X, REQ-XXX)
   - VIOLATION: pain_points.md instead of PAIN_POINTS.md
```

**Enforcement Actions:**

| Violation Type | First Occurrence | Repeated |
|----------------|------------------|----------|
| Phase ordering | WARN + allow | BLOCK |
| Schema mismatch | WARN + auto-fix attempt | BLOCK |
| Missing traceability | WARN + require fix | BLOCK |
| TDD violation | BLOCK immediately | BLOCK |
| Naming convention | AUTO-FIX + INFO | WARN |

**Violation Report Format:**

```markdown
## Process Integrity Report

**Timestamp:** 2024-01-15T10:45:00Z
**Phase:** Implementation (Checkpoint 4)
**Agent Under Review:** developer-2

### Violations Found

| # | Rule | Severity | Details |
|---|------|----------|---------|
| 1 | TDD_RED_PHASE | CRITICAL | No failing test before useInventory.ts |
| 2 | TRACEABILITY_FOOTER | MEDIUM | Missing in inventory-screen.md |

### Verdict: BLOCKED

**Required Actions:**
1. Create failing test for useInventory hook
2. Add traceability footer to inventory-screen.md

**Resume Command:** /htec-sdd-resume --from-checkpoint 4
```

---

## Multi-Perspective Critique (Reflexion)

For complex changes, three judge agents provide independent evaluation:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MULTI-PERSPECTIVE CRITIQUE                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  JUDGE 1: REQUIREMENTS VALIDATOR                                        │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ • Does fix align with original request?                         │    │
│  │ • Acceptance criteria truly met?                                │    │
│  │ • Any scope creep?                                              │    │
│  │ • Traceability maintained?                                      │    │
│  │ Score: [1-10]                                                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  JUDGE 2: SOLUTION ARCHITECT                                            │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ • Technically sound approach?                                   │    │
│  │ • Follows architecture patterns?                                │    │
│  │ • Technical debt introduced?                                    │    │
│  │ • Performance implications?                                     │    │
│  │ Score: [1-10]                                                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  JUDGE 3: CODE QUALITY REVIEWER                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ • Clean and maintainable code?                                  │    │
│  │ • Tests adequate and meaningful?                                │    │
│  │ • Documentation updated?                                        │    │
│  │ • Error handling appropriate?                                   │    │
│  │ Score: [1-10]                                                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  CROSS-REVIEW: Judges review each other's findings                      │
│  FINAL SCORE = Average of 3 judges                                      │
│                                                                         │
│  IF score < 7: ITERATE (return to implementation)                       │
│  IF score >= 7: PROCEED to completion                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Reflexion Scoring

```
COMPLEXITY TRIAGE:

IF change.complexity == "simple":
    reflection_depth = "QUICK"      # 5 minutes, single self-check
ELIF change.complexity == "moderate":
    reflection_depth = "STANDARD"   # 15 minutes, scoring matrix
ELSE:
    reflection_depth = "DEEP"       # 30+ minutes, 3-judge panel
```

---

## Agent Coordination Patterns

### Pattern 1: Sequential with Handoff

```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ ANALYZE │ ──▶ │  PLAN   │ ──▶ │IMPLEMENT│
└─────────┘     └─────────┘     └─────────┘
   tech-lead       tech-lead      developer

   Output A        Output B       Output C
   feeds into      feeds into     uses both
```

### Pattern 2: Parallel Fan-Out

```
              ┌─────────────┐
              │   REVIEW    │
              │ ORCHESTRATOR│
              └──────┬──────┘
                     │
     ┌───────┬───────┼───────┬───────┬───────┐
     ▼       ▼       ▼       ▼       ▼       ▼
  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
  │ BH  │ │ SEC │ │ CQ  │ │ TC  │ │ CR  │ │A11Y │
  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘
     │       │       │       │       │       │
     └───────┴───────┴───────┼───────┴───────┘
                             │
                     ┌───────▼───────┐
                     │  CONSOLIDATE  │
                     │   FINDINGS    │
                     └───────────────┘
```

### Pattern 3: Iterative Refinement (Reflexion)

```
┌──────────────────────────────────────────────────┐
│                                                  │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│   │IMPLEMENT │ ──▶│  VERIFY  │ ──▶│ REFLECT  │   │
│   └──────────┘    └──────────┘    └────┬─────┘   │
│        ▲                               │         │
│        │                               │         │
│        │          score < 7            │         │
│        └───────────────────────────────┘         │
│                                                  │
│              score >= 7                          │
│                  │                               │
│                  ▼                               │
│           ┌──────────┐                           │
│           │ COMPLETE │                           │
│           └──────────┘                           │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

## File-Based Coordination

Agents coordinate through shared files in the `traceability/` folder:

```
traceability/
├── task_registry.json           # Task ownership and status
├── change_request_registry.json # CR tracking
├── review_registry.json         # Code review findings
└── agent_lock.json              # File locking for writes

Implementation_<System>/
├── _state/
│   ├── agent_progress.json      # Per-agent progress
│   └── findings_buffer.json     # Accumulated findings
└── change-requests/
    └── <session>/
        ├── ANALYSIS.md          # Shared analysis output
        ├── IMPLEMENTATION_LOG.md # Execution trace
        └── agent_outputs/
            ├── bug-hunter.json
            ├── security-auditor.json
            └── ...
```

### Locking Protocol

```
BEFORE writing to shared file:
    1. Check agent_lock.json for existing lock
    2. IF locked AND lock_age < 60s:
           WAIT or QUEUE
    3. IF not locked OR lock_expired:
           ACQUIRE lock (write agent_id + timestamp)
           PERFORM write
           RELEASE lock

DEADLOCK PREVENTION:
    - Locks expire after 60 seconds
    - Agents write to their own output files first
    - Consolidation happens after all agents complete
```

---

## Model Selection Guidelines

Different agents benefit from different model capabilities:

| Agent Type | Recommended Model | Rationale |
|------------|-------------------|-----------|
| Planning agents | `opus` | Complex reasoning, architecture decisions |
| Product researcher | `opus` | Deep analysis, synthesis of web research |
| HFE/UX researcher | `opus` | Complex UX reasoning, pattern recognition |
| Implementation agents | `sonnet` | Balance of speed and capability |
| Test automation engineer | `sonnet` | Test framework design, code generation |
| Code review agents | `sonnet` | Fast parallel execution |
| Reflexion judges | `opus` | Nuanced quality assessment |
| Process integrity agents | `haiku` | Fast continuous validation, low overhead |
| Quick checks | `haiku` | Fast, simple validations |

---

## Error Handling in Agents

```
AGENT ERROR HANDLING:

1. TIMEOUT (120s default, 600s max)
   - Log timeout in FAILURES_LOG.md
   - Continue with partial results
   - Mark agent as incomplete

2. CRASH
   - Capture error message
   - Log to agent_outputs/
   - Retry once with exponential backoff
   - Skip if retry fails

3. INVALID OUTPUT
   - Validate against expected schema
   - Log validation errors
   - Use defaults or skip finding

4. BLOCKING FAILURE
   - Critical agent failure stops pipeline
   - Generate error report
   - Require manual intervention
```

---

## Related Documents

- [ChangeRequest_Process.md](./ChangeRequest_Process.md) - Change request workflow
- [Stage5_Implementation_Architecture.md](./Stage5_Implementation_Architecture.md) - Full implementation architecture
- [Implementation_CodeReview SKILL.md](../.claude/skills/Implementation_CodeReview/SKILL.md) - Code review skill
- [systematic-debugging SKILL.md](../.claude/skills/systematic-debugging/SKILL.md) - Debugging framework
