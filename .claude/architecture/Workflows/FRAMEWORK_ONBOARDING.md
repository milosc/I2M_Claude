# HTEC I2M Accelerator Framework: Complete Onboarding Guide

**Version:** 1.0.0
**Date:** January 29, 2026
**Scope:** Framework-wide initialization and Way of Working (WoW)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Prerequisites](#2-prerequisites)
3. [Initial Setup (MANDATORY)](#3-initial-setup-mandatory)
   - 3.1 [Install Dependencies](#31-install-dependencies)
   - 3.2 [Initialize Project Metadata](#32-initialize-project-metadata)
   - 3.3 [Verify Setup](#33-verify-setup)
4. [Understanding Session Management](#4-understanding-session-management)
5. [5-Stage Framework Overview](#5-5-stage-framework-overview)
6. [First-Time Workflow](#6-first-time-workflow)
7. [Troubleshooting](#7-troubleshooting)
8. [Next Steps](#8-next-steps)

---

## 1. Executive Summary

The **HTEC I2M Accelerator Framework** is an AI-powered system that transforms raw client requirements into production-ready implementations through 5 structured stages:

```
Client Materials → Discovery → Prototype → ProductSpecs → Solution Architecture → Implementation
```

**This guide covers**:
- Initial framework setup (`/htec-libraries-init`)
- Project initialization (`/project-init`)
- Session management and validation
- Your first workflow execution

**Time to complete**: 5-10 minutes

[Back to Top](#table-of-contents)

---

## 2. Prerequisites

### System Requirements
- **Claude Code CLI** installed and configured
- **Git** installed (for user context detection)
- **Python 3.8+** (for framework utilities)
- **Node.js 16+** (for Prototype generation)
- **jq** (for JSON processing)

### Directory Setup
```bash
# Your project structure should look like:
project_root/
├── Client_Materials/          # Your raw inputs (interviews, PDFs, etc.)
├── .claude/                   # Framework configuration (auto-managed)
│   ├── hooks/                 # Utilities and lifecycle hooks
│   ├── commands/              # Available slash commands
│   ├── skills/                # Agent capabilities
│   └── agents/                # Specialized agent definitions
├── _state/                    # Session and progress tracking
└── traceability/              # Version history and traceability chains
```

### Access Requirements
- Claude API key configured in Claude Code settings
- Write permissions to project directory

[Back to Top](#table-of-contents)

---

## 3. Initial Setup (MANDATORY)

⚠️ **IMPORTANT**: These steps are required before running ANY framework command.

### 3.1 Install Dependencies

Install all required Python packages, Playwright browsers, and LSP servers:

```bash
/htec-libraries-init
```

**What this does**:
- Creates `.venv/` Python virtual environment
- Installs PDF processing libraries (pypdfium2)
- Installs Office document processors (python-pptx, openpyxl, python-docx)
- Installs Playwright for browser automation
- Installs TypeScript LSP for code intelligence
- Installs image processing libraries (Pillow)

**Expected output**:
```
✅ Virtual environment created at .venv/
✅ Installed pypdfium2 (PDF processing)
✅ Installed python-pptx (PowerPoint processing)
...
✅ Playwright browsers installed
✅ TypeScript LSP server installed
⏱️  Total time: ~2-3 minutes
```

**Troubleshooting**:
- If installation fails, check Python version: `python3 --version` (need 3.8+)
- If Playwright fails, run manually: `.venv/bin/playwright install`

---

### 3.2 Initialize Project Metadata

Capture your project name and user context:

```bash
/project-init
```

**What this does**:
1. **Detects your username** from git config (fallback to OS username)
2. **Prompts for project name** via interactive questions
3. **Updates session.json** with meaningful values
4. **Validates the session** to ensure consistency

**Interactive flow**:

```
✅ Detected user: milosc79

❓ What is the name of the system/project you're building?
   [ ] Use current directory name
   [ ] Specify custom name

❓ Enter the project/system name:
   [ ] InventorySystem
   [ ] ERTriage
   [ ] Other (specify)

✅ Project initialized successfully:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
  "project": "InventorySystem",
  "user": "milosc79",
  "stage": "initialization",
  "updated_at": "2026-01-29T08:53:19+01:00"
}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Next Steps:

  1. Start Discovery analysis:
     /discovery InventorySystem Client_Materials/

  2. Or if Discovery is complete, generate Prototype:
     /prototype InventorySystem

  3. Check status anytime:
     /discovery-status
     /prototype-status
```

**Why this matters**:
- **Traceability**: Version history logs will show YOUR name (not "Claude" or "system")
- **Context**: All generated artifacts will reference the correct project name
- **Collaboration**: Multiple developers can work on the same framework with proper attribution

**Valid project names**:
- ✅ `InventorySystem`, `ERTriage`, `CustomerPortal` (PascalCase recommended)
- ❌ `pending`, `unknown`, `test`, `demo` (reserved/invalid)

---

### 3.3 Verify Setup

Check that initialization succeeded:

```bash
# 1. Verify session is valid
python3 .claude/hooks/validate_session.py

# Expected output:
# ✅ Session validation passed

# 2. Check session contents
cat _state/session.json | jq '.'

# Expected output:
# {
#   "project": "InventorySystem",  ← NOT "pending"
#   "user": "milosc79",            ← NOT "system"
#   "stage": "initialization"
# }

# 3. Verify dependencies
.venv/bin/python --version  # Should show Python 3.8+
.venv/bin/playwright --version  # Should show Playwright version
```

**Success criteria**:
- ✅ `validate_session.py` shows no warnings
- ✅ `session.json` has real project name and username
- ✅ `.venv/` directory exists with installed packages

[Back to Top](#table-of-contents)

---

## 4. Understanding Session Management

### What is `_state/session.json`?

The session file tracks your current context throughout the framework:

```json
{
  "session_id": "1769673199-16732",
  "program": "HTEC Framework",       ← Framework name (constant)
  "project": "InventorySystem",      ← Your system name (variable)
  "stage": "discovery",              ← Current workflow stage
  "user": "milosc79",                ← Your username (not "system")
  "started_at": "2026-01-29T08:00:00",
  "updated_at": "2026-01-29T09:30:00",
  "metadata": {}
}
```

### Session Validation (Automatic)

Every orchestrator command (`/discovery`, `/prototype`, etc.) automatically validates your session:

**If session is valid** (after `/project-init`):
```bash
/discovery InventorySystem Client_Materials/
# ✅ No warnings
# [Command proceeds immediately]
```

**If session is invalid** (before `/project-init`):
```bash
/discovery TestProject Client_Materials/
# ⚠️  SESSION VALIDATION WARNING
# ============================================================
#    Project name is invalid: 'pending'
#    Run /project-init to set a meaningful project name
#    User name is invalid: 'system'
#    Run /project-init to capture user information
#
# 💡 Run /project-init to fix these warnings
# ============================================================
#
# [Command continues executing but logs may show "pending"/"system"]
```

**Key points**:
- ⚠️ Warnings are **non-blocking** - commands continue execution
- ⚠️ Invalid session = meaningless traceability logs ("pending", "system")
- ✅ Valid session = proper attribution and project context

### Session Auto-Update

Commands automatically update the session as you progress:

```bash
/discovery InventorySystem ...  # → stage becomes "discovery"
/prototype InventorySystem      # → stage becomes "prototype"
/productspecs InventorySystem   # → stage becomes "productspecs"
```

### Fixing Invalid Sessions

If you see validation warnings:

```bash
# Option 1: Run interactive initialization
/project-init

# Option 2: Manual fix (advanced)
bash .claude/hooks/session-update.sh --project "YourProject" --stage "discovery"
python3 .claude/hooks/update_session_user.py "YourName"

# Option 3: Reset and start fresh
rm _state/session.json
# (session-init.sh will recreate on next Claude Code start)
```

[Back to Top](#table-of-contents)

---

## 5. 5-Stage Framework Overview

### Stage 1: Discovery (Analysis & Requirements)

**Input**: Raw client materials (interviews, PDFs, screenshots)
**Output**: Personas, JTBD, requirements, wireframes, strategy
**Command**: `/discovery-multiagent <SystemName> Client_Materials/`
**Duration**: ~1.25 hours (parallelized)

**Key deliverables** (21 files across 6 folders):
- Personas (3-5 detailed profiles)
- Jobs-To-Be-Done (JTBD framework)
- Requirements registry (P0/P1/P2 priorities)
- Screen definitions (wireframes)
- Product vision & strategy
- KPIs and success metrics

**Onboarding guide**: `.claude/architecture/Workflows/Discovery Phase/DISCOVERY_ONBOARDING.md`

---

### Stage 2: Prototype (Design & Validation)

**Input**: Discovery outputs (requirements, personas, screens)
**Output**: Working React prototype with design system
**Command**: `/prototype <SystemName>`
**Duration**: ~2-3 hours

**Key deliverables**:
- Design tokens (colors, typography, spacing)
- Component library (buttons, forms, layouts)
- Screen implementations (mapped to requirements)
- Interactive prototype (localhost:3000)
- Playwright visual validation

**Onboarding guide**: `.claude/architecture/Workflows/Idea Shaping and Validation Phase/PROTOTYPE_ONBOARDING.md`

---

### Stage 3: ProductSpecs (Module Specifications)

**Input**: Prototype outputs (screens, components, API contracts)
**Output**: JIRA-ready module specs with test cases
**Command**: `/productspecs <SystemName>`
**Duration**: ~1-2 hours

**Key deliverables**:
- UI module specs (acceptance criteria)
- API module specs (endpoints, validation)
- Integration test specs
- E2E test specs (user journeys)
- Unit test specs (edge cases)

**Onboarding guide**: `.claude/architecture/Workflows/Solution Specification Phase/SOLUTION_SPECIFICATION_ONBOARDING.md`

---

### Stage 4: Solution Architecture (ADRs & C4)

**Input**: ProductSpecs outputs (module specs, NFRs)
**Output**: Architecture Decision Records + C4 diagrams
**Command**: `/solarch <SystemName>`
**Duration**: ~1.5-2 hours

**Key deliverables**:
- Foundation ADRs (tech stack, patterns)
- Communication ADRs (API design, messaging)
- Operational ADRs (deployment, monitoring)
- C4 context/container/component diagrams
- Quality attribute scenarios (performance, security)

---

### Stage 5: Implementation (TDD Development)

**Input**: ProductSpecs + SolArch outputs (specs + ADRs)
**Output**: Production code with full test coverage
**Command**: `/htec-sdd-tasks <SystemName>` → `/htec-sdd-implement <SystemName>`
**Duration**: Variable (depends on scope)

**Key deliverables**:
- Task decomposition (T-001, T-002, etc.)
- RED-GREEN-REFACTOR implementation
- Unit/integration/E2E tests
- Code review reports
- Git commits with traceability

**WoW guide**: `.claude/architecture/Workflows/Implementation Phase/Implementation_Phase_WoW.md`

[Back to Top](#table-of-contents)

---

## 6. First-Time Workflow

### Scenario: Building an Inventory Management System

#### Step 1: Prepare Client Materials

```bash
# Create input directory
mkdir -p Client_Materials

# Add your materials
cp ~/interviews/*.md Client_Materials/
cp ~/designs/*.png Client_Materials/
cp ~/requirements/*.pdf Client_Materials/
```

**What to include**:
- Interview transcripts (`.txt`, `.md`, `.docx`)
- Design mockups (`.png`, `.jpg`, `.pdf`)
- Technical docs (`.pdf`, `.docx`)
- Spreadsheets (`.xlsx`, `.csv`) for data models
- Existing system screenshots

---

#### Step 2: Initialize Framework

```bash
# 1. Install dependencies (one-time setup)
/htec-libraries-init

# 2. Initialize project metadata
/project-init
# → Enter "InventorySystem" when prompted
```

---

#### Step 3: Run Discovery

```bash
# Multi-agent parallelized execution (RECOMMENDED)
/discovery-multiagent InventorySystem Client_Materials/

# Monitor progress
/discovery-status

# Expected output folders:
ClientAnalysis_InventorySystem/
├── 01-inputs/                 # Processed client materials
├── 02-personas/               # User profiles
├── 03-research/               # JTBD, pain points
├── 04-strategy/               # Vision, roadmap, KPIs
├── 05-design-specs/           # Screens, components
└── 06-documentation/          # Consolidated docs + validation
```

**Typical timeline**:
- CP-01 (Input Processing): 5-10 min
- CP-02-04 (Analysis): 15-20 min (parallel)
- CP-05-07 (Strategy): 10-15 min (parallel)
- CP-08-09 (Design): 15-20 min (parallel)
- CP-10 (VP Review): 5-10 min
- CP-11 (Validation): 2-3 min
- **Total**: ~60-75 min

---

#### Step 4: Generate Prototype

```bash
# Automatic sequence: Design Tokens → Components → Screens → Build
/prototype InventorySystem

# Monitor progress
/prototype-status

# Expected output:
Prototype_InventorySystem/
├── 01-design-tokens/          # Foundational design system
├── 02-components/             # Reusable React components
├── 03-screens/                # Full screen implementations
├── 04-api-contracts/          # OpenAPI specs
├── 05-data-models/            # TypeScript interfaces
└── 06-prototype/              # Working app (npm run dev)
```

**Test the prototype**:
```bash
cd Prototype_InventorySystem/06-prototype
npm install
npm run dev
# → Open http://localhost:3000
```

---

#### Step 5: Generate ProductSpecs

```bash
# Full system-level generation
/productspecs InventorySystem

# Or module-level (faster)
/productspecs InventorySystem --module MOD-INV-SEARCH-01

# Expected output:
ProductSpecs_InventorySystem/
├── 01-modules/                # UI/API module specifications
├── 02-tests/                  # Unit/integration/E2E test specs
├── 03-contracts/              # API contracts + data models
└── 04-export/                 # JIRA CSV export + consolidated docs
```

---

#### Step 6: Solution Architecture

```bash
# Generate ADRs + C4 diagrams
/solarch InventorySystem

# Expected output:
SolArch_InventorySystem/
├── 01-decisions/              # Architecture Decision Records
├── 02-diagrams/               # C4 context/container/component
├── 03-quality/                # Quality attribute scenarios
└── 04-documentation/          # Consolidated architecture docs
```

---

#### Step 7: Implementation

```bash
# 1. Decompose into tasks
/htec-sdd-tasks InventorySystem
# → Interactive: Choose PR grouping strategy

# 2. Setup worktrees (optional, for parallel dev)
/htec-sdd-worktree-setup InventorySystem

# 3. Implement (TDD cycle)
/htec-sdd-implement InventorySystem
# → RED: Write failing tests
# → GREEN: Implement minimal code to pass
# → REFACTOR: Improve code quality

# 4. Review (after batch implementation)
/htec-sdd-review
```

**Expected output**:
```
Implementation_InventorySystem/
├── src/                       # Production code
├── tests/                     # Unit/integration/E2E tests
├── docs/                      # Implementation docs
└── _state/                    # Task tracking, locks
```

[Back to Top](#table-of-contents)

---

## 7. Troubleshooting

### Session Validation Warnings

**Problem**:
```
⚠️  SESSION VALIDATION WARNING
   Project name is invalid: 'pending'
   User name is invalid: 'system'
```

**Solution**:
```bash
# Run project initialization
/project-init

# Verify fix
python3 .claude/hooks/validate_session.py
# ✅ Session validation passed
```

---

### Dependencies Not Found

**Problem**:
```
ModuleNotFoundError: No module named 'pypdfium2'
```

**Solution**:
```bash
# Reinstall dependencies
/htec-libraries-init

# Verify installation
.venv/bin/python -c "import pypdfium2; print('✅ pypdfium2 OK')"
```

---

### Git User Not Detected

**Problem**:
```bash
python3 .claude/hooks/get_user_context.py
# Output: unknown
```

**Solution**:
```bash
# Configure git user (if not set)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify
python3 .claude/hooks/get_user_context.py
# Output: Your Name
```

---

### Session File Corrupted

**Problem**:
```
ERROR: Session file missing or corrupted
```

**Solution**:
```bash
# Reset session
rm _state/session.json

# Restart Claude Code (triggers session-init.sh)
# Then run /project-init again
```

---

### Invalid Project Name

**Problem**:
```
❌ Project name 'test' is invalid (reserved keyword)
```

**Solution**:
```bash
# Use meaningful PascalCase names
/project-init
# → Enter "InventorySystem" or "CustomerPortal"

# Avoid: test, demo, pending, unknown, null, system
```

[Back to Top](#table-of-contents)

---

## 8. Next Steps

### After Completing Initial Setup

**Immediate**:
1. ✅ Run your first Discovery workflow
2. ✅ Review generated artifacts (personas, requirements)
3. ✅ Provide feedback via `/discovery-feedback`

**Short term** (1-2 weeks):
1. Complete full pipeline (Discovery → Implementation)
2. Understand traceability chains (PP → JTBD → REQ → MOD → T)
3. Learn manual commands for targeted regeneration

**Long term** (1 month+):
1. Master multi-agent orchestration strategies
2. Customize agent prompts in `.claude/agents/`
3. Extend framework with custom skills in `.claude/skills/`

### Recommended Reading Order

1. **This document** - Framework initialization ✅
2. **DISCOVERY_ONBOARDING.md** - Discovery phase deep-dive
3. **PROTOTYPE_ONBOARDING.md** - Prototype generation
4. **SOLUTION_SPECIFICATION_ONBOARDING.md** - ProductSpecs workflow
5. **Implementation_Phase_WoW.md** - TDD implementation guide

### Key Commands Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/htec-libraries-init` | Install dependencies | First-time setup |
| `/project-init` | Initialize project metadata | Before any workflow |
| `/discovery-status` | Check Discovery progress | During Discovery |
| `/prototype-status` | Check Prototype progress | During Prototype |
| `/productspecs-status` | Check ProductSpecs progress | During ProductSpecs |
| `/integrity-check` | Cross-stage validation | After each stage |
| `/discovery-audit` | Zero-hallucination check | Before finalizing Discovery |

### Support & Resources

**Documentation**:
- Main guide: `CLAUDE.md` (project root)
- Architecture: `.claude/architecture/` (detailed specs)
- Commands: `.claude/commands/` (all slash commands)

**Troubleshooting**:
- Quick reference: `.claude/rules/QUICK_REFERENCE.md`
- Error handling: `.claude/rules/CORE_RULES.md` (Section 2)

**Feedback**:
- Report issues: `https://github.com/anthropics/claude-code/issues`
- Command: `/help` (in Claude Code)

[Back to Top](#table-of-contents)

---

**End of Framework Onboarding Guide**

*Version 1.0.0 | January 29, 2026 | HTEC I2M Accelerator Framework*
