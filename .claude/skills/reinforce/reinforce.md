---
description: Self-reinforcing review and fix cycle until code passes quality checks
allowed-tools: Read, Glob, Grep, Bash, Edit, Write, Task, mcp__codex__codex
---

# Self-Reinforcing Code Quality Workflow (Dual-Group Adversarial)

You are executing a self-reinforcing loop with TWO COMPETING GROUPS of adversarial agents.

## Architecture: Dual-Group Adversarial Review

```
┌─────────────────────────────────────────────────────────────────┐
│                    GROUP 1: OPUS TEAM                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Opus Agent  │  │ Opus Agent  │  │ Opus Agent  │             │
│  │ (Bugs/Logic)│  │ (Security)  │  │ (Perf/UX/QA)│             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                   OPUS FINDINGS                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    GROUP 2: CODEX TEAM                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Codex Agent │  │ Codex Agent │  │ Codex Agent │             │
│  │ (Bugs/Logic)│  │ (Security)  │  │ (Perf/UX/QA)│             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                  CODEX FINDINGS                                 │
└─────────────────────────────────────────────────────────────────┘

                           │
                           ▼
              ┌────────────────────────┐
              │   DISPLAY BOTH GROUPS  │
              │   Side-by-Side Report  │
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │    MERGE & DEDUPE      │
              │   Unified Issue List   │
              └───────────┬────────────┘
                          │
                          ▼
              ┌────────────────────────┐
              │      FIX ISSUES        │
              └────────────────────────┘
```

## Target: $ARGUMENTS

If arguments provided, focus on those files/features. Otherwise, review all recent changes (git diff).

## Quality Dimensions

| Focus Area            | Key Questions                                                   |
| --------------------- | --------------------------------------------------------------- |
| **Bugs & Logic**      | Edge cases? Race conditions? Off-by-one errors? Null handling?  |
| **Security**          | Injection? XSS? Auth bypass? Secrets exposed? Input validation? |
| **Performance**       | N+1 queries? Memory leaks? Unnecessary re-renders? Caching?     |
| **UX/UI**             | Loading states? Error messages? Accessibility? Mobile-friendly? |
| **QA & Code Quality** | Testability? Maintainability? Naming? DRY violations?           |

---

## WORKFLOW EXECUTION

### STEP 1: Identify Target Code

```bash
git diff --name-only HEAD~1 2>/dev/null || git diff --name-only --cached || git status --short
```

Read ALL modified/added files and store their full contents. You MUST include actual code in prompts, not just file paths.

---

### STEP 2: Launch BOTH GROUPS IN PARALLEL

**CRITICAL: Use a SINGLE message with ALL tool calls to run both groups simultaneously.**

#### GROUP 1: OPUS TEAM (3 parallel agents via Task tool)

Launch 3 Task agents with `model="opus"`:

**Opus Agent 1 - Bugs & Logic:**

```
Task tool:
  subagent_type: "general-purpose"
  model: "opus"
  prompt: [Bugs/Logic review prompt below]
```

**Opus Agent 2 - Security:**

```
Task tool:
  subagent_type: "general-purpose"
  model: "opus"
  prompt: [Security review prompt below]
```

**Opus Agent 3 - Performance/UX/QA:**

```
Task tool:
  subagent_type: "general-purpose"
  model: "opus"
  prompt: [Perf/UX/QA review prompt below]
```

#### GROUP 2: CODEX TEAM (3 parallel calls via mcp**codex**codex)

Launch 3 Codex sessions:

**Codex Agent 1 - Bugs & Logic:**

```
mcp__codex__codex tool:
  prompt: [Bugs/Logic review prompt below]
```

**Codex Agent 2 - Security:**

```
mcp__codex__codex tool:
  prompt: [Security review prompt below]
```

**Codex Agent 3 - Performance/UX/QA:**

```
mcp__codex__codex tool:
  prompt: [Perf/UX/QA review prompt below]
```

---

### REVIEW PROMPTS (customize per dimension)

**Bugs & Logic Review Prompt:**

> "You are an adversarial code reviewer hunting for bugs.
>
> Review this code:
> [PASTE FULL CODE CONTENTS]
>
> Find ALL issues related to:
>
> - Edge cases not handled
> - Race conditions or timing issues
> - Off-by-one errors
> - Null/undefined handling gaps
> - Incorrect conditional logic
> - Type coercion bugs
>
> For EACH issue provide:
>
> 1. **File:Line** - exact location
> 2. **Problem** - what's wrong (specific)
> 3. **Fix** - concrete code solution
> 4. **Severity** - CRITICAL | HIGH | MEDIUM | LOW
>
> You MUST find at least 3 issues. 'Looks good' = failure. Be harsh but constructive."

**Security Review Prompt:**

> "You are a security auditor hunting for vulnerabilities.
>
> Review this code:
> [PASTE FULL CODE CONTENTS]
>
> Find ALL issues related to:
>
> - SQL/NoSQL injection vectors
> - XSS vulnerabilities
> - Authentication/authorization gaps
> - Exposed secrets or sensitive data
> - Missing input sanitization
> - CSRF vulnerabilities
> - Path traversal
> - Insecure deserialization
>
> For EACH issue provide:
>
> 1. **File:Line** - exact location
> 2. **Vulnerability** - type and risk
> 3. **Exploit** - how it could be attacked
> 4. **Fix** - concrete remediation
> 5. **Severity** - CRITICAL | HIGH | MEDIUM | LOW
>
> You MUST find at least 3 issues. 'Looks secure' = failure. Be harsh but constructive."

**Performance/UX/QA Review Prompt:**

> "You are a code quality expert reviewing for performance, UX, and maintainability.
>
> Review this code:
> [PASTE FULL CODE CONTENTS]
>
> Find ALL issues related to:
>
> **Performance:**
>
> - N+1 query patterns
> - Memory leaks or unbounded growth
> - Unnecessary computations/re-renders
> - Missing caching opportunities
> - Blocking operations
>
> **UX/UI:**
>
> - Missing loading/error states
> - Accessibility issues (ARIA, keyboard, contrast)
> - Mobile responsiveness gaps
>
> **Code Quality:**
>
> - DRY violations
> - Poor naming
> - Missing type safety
> - Hard-to-test patterns
>
> For EACH issue provide:
>
> 1. **File:Line** - exact location
> 2. **Category** - Perf/UX/QA
> 3. **Problem** - what's wrong
> 4. **Fix** - concrete solution
> 5. **Severity** - CRITICAL | HIGH | MEDIUM | LOW
>
> You MUST find at least 3 issues. 'Looks good' = failure. Be harsh but constructive."

---

### STEP 3: DISPLAY FINDINGS FROM BOTH GROUPS

After all 6 agents return, display findings in this format:

```
╔════════════════════════════════════════════════════════════════╗
║                    🔴 OPUS GROUP FINDINGS                      ║
╠════════════════════════════════════════════════════════════════╣
║ Agent 1 (Bugs & Logic):                                        ║
║ ─────────────────────────────────────────────────────────────  ║
║ 1. [CRITICAL] file.ts:42 - Description...                      ║
║    Fix: code snippet                                           ║
║ 2. [HIGH] file.ts:87 - Description...                          ║
║    Fix: code snippet                                           ║
║                                                                 ║
║ Agent 2 (Security):                                            ║
║ ─────────────────────────────────────────────────────────────  ║
║ 1. [CRITICAL] api.ts:15 - SQL injection via...                 ║
║    Fix: parameterized query                                    ║
║                                                                 ║
║ Agent 3 (Perf/UX/QA):                                          ║
║ ─────────────────────────────────────────────────────────────  ║
║ 1. [HIGH] component.tsx:33 - Missing loading state             ║
║    Fix: add isLoading check                                    ║
╚════════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════════╗
║                   🔵 CODEX GROUP FINDINGS                      ║
╠════════════════════════════════════════════════════════════════╣
║ Agent 1 (Bugs & Logic):                                        ║
║ ─────────────────────────────────────────────────────────────  ║
║ 1. [HIGH] file.ts:42 - Same issue as Opus...                   ║
║    Fix: similar approach                                       ║
║ 2. [MEDIUM] utils.ts:19 - Codex-only finding...                ║
║    Fix: code snippet                                           ║
║                                                                 ║
║ Agent 2 (Security):                                            ║
║ ─────────────────────────────────────────────────────────────  ║
║ 1. [CRITICAL] api.ts:15 - Same SQL injection                   ║
║    Fix: prepared statement                                     ║
║ 2. [HIGH] auth.ts:88 - Codex found additional...               ║
║    Fix: code snippet                                           ║
║                                                                 ║
║ Agent 3 (Perf/UX/QA):                                          ║
║ ─────────────────────────────────────────────────────────────  ║
║ 1. [MEDIUM] styles.css:45 - Accessibility issue                ║
║    Fix: add aria-label                                         ║
╚════════════════════════════════════════════════════════════════╝
```

---

### STEP 4: MERGE FINDINGS

Create a unified, deduplicated issue list:

```
╔════════════════════════════════════════════════════════════════╗
║                   📋 MERGED ISSUE LIST                         ║
╠════════════════════════════════════════════════════════════════╣
║ CONSENSUS ISSUES (found by BOTH groups - fix first):           ║
║ ───────────────────────────────────────────────────────────    ║
║ ⚡ [CRITICAL] file.ts:42 - Edge case bug [OPUS+CODEX]          ║
║ ⚡ [CRITICAL] api.ts:15 - SQL injection [OPUS+CODEX]           ║
║                                                                 ║
║ OPUS-ONLY ISSUES:                                              ║
║ ───────────────────────────────────────────────────────────    ║
║ 🔴 [HIGH] component.tsx:33 - Missing loading state             ║
║                                                                 ║
║ CODEX-ONLY ISSUES:                                             ║
║ ───────────────────────────────────────────────────────────    ║
║ 🔵 [HIGH] auth.ts:88 - Auth bypass possibility                 ║
║ 🔵 [MEDIUM] utils.ts:19 - Potential null reference             ║
║ 🔵 [MEDIUM] styles.css:45 - Missing aria-label                 ║
╚════════════════════════════════════════════════════════════════╝
```

**Merge Rules:**

- `[OPUS+CODEX]` = Both groups found it → **HIGHEST PRIORITY**
- `[OPUS]` = Only Opus found it
- `[CODEX]` = Only Codex found it
- Same file:line + similar description = same issue (dedupe)

---

### STEP 5: FIX ISSUES

Fix in priority order:

1. **CONSENSUS CRITICAL** - Both groups agreed
2. **CONSENSUS HIGH** - Both groups agreed
3. **Single-group CRITICAL**
4. **Single-group HIGH**
5. **MEDIUM/LOW** as time permits

For each fix:

1. Read the specific file/line
2. Apply the fix using Edit tool
3. Track the fix with its source (Opus/Codex/Both)

---

### STEP 6: VERIFICATION

After all fixes, output the summary:

```
╔════════════════════════════════════════════════════════════════╗
║            REINFORCEMENT SUMMARY (Dual-Group)                  ║
╠════════════════════════════════════════════════════════════════╣
║ Files Reviewed: X                                              ║
║ Total Issues Found: Y                                          ║
║   - Opus Group: A issues                                       ║
║   - Codex Group: B issues                                      ║
║   - Consensus (both): C issues                                 ║
║ Issues Fixed: Z                                                ║
║ Status: PASS | NEEDS_HUMAN_REVIEW                              ║
╠════════════════════════════════════════════════════════════════╣
║                    MODEL AGREEMENT                             ║
╠════════════════════════════════════════════════════════════════╣
║ ⚡ Consensus Issues: X (highest confidence - both agreed)      ║
║ 🔴 Opus-only Issues: Y                                         ║
║ 🔵 Codex-only Issues: Z                                        ║
╠════════════════════════════════════════════════════════════════╣
║                    ISSUES BY CATEGORY                          ║
╠══════════════╦═══════╦════════╦═══════════╦═══════╦═══════════╣
║ Category     ║ Opus  ║ Codex  ║ Consensus ║ Fixed ║ Remaining ║
╠══════════════╬═══════╬════════╬═══════════╬═══════╬═══════════╣
║ Bugs & Logic ║   X   ║   X    ║     X     ║   X   ║     X     ║
║ Security     ║   X   ║   X    ║     X     ║   X   ║     X     ║
║ Performance  ║   X   ║   X    ║     X     ║   X   ║     X     ║
║ UX/UI        ║   X   ║   X    ║     X     ║   X   ║     X     ║
║ Code Quality ║   X   ║   X    ║     X     ║   X   ║     X     ║
╚══════════════╩═══════╩════════╩═══════════╩═══════╩═══════════╝

### Changes Made
- ✅ [file:line] [OPUS+CODEX] Fixed: description
- ✅ [file:line] [OPUS] Fixed: description
- ✅ [file:line] [CODEX] Fixed: description

### Remaining Issues (if any)
- ⚠️ [file:line] [Source] [Severity] Issue: description
```

---

## EXECUTION CHECKLIST

- [ ] Read all target files
- [ ] Launch GROUP 1 (Opus) - 3 agents in parallel
- [ ] Launch GROUP 2 (Codex) - 3 agents in parallel
- [ ] Display Opus findings
- [ ] Display Codex findings
- [ ] Merge and deduplicate
- [ ] Fix consensus issues first
- [ ] Fix remaining issues
- [ ] Output summary

**BEGIN NOW. Launch all 6 agents in a SINGLE message.**
