# HTEC Framework: Quick Start Guide

**Version**: 1.0.0
**Date**: January 29, 2026
**Reading Time**: 3 minutes

---

## 🚀 30-Second Setup

```bash
# 1. Install dependencies (~3 minutes)
/htec-libraries-init

# 2. Initialize project (~1 minute)
/project-init

# 3. Run your first workflow
/discovery-multiagent <YourProjectName> Client_Materials/
```

**Done!** You're now running the HTEC I2M Accelerator Framework.

---

## ⚡ First-Time User Flow

### Prerequisites
- Claude Code CLI installed
- Git configured (for user detection)
- Raw client materials ready (interviews, PDFs, screenshots)

### Step-by-Step

**1️⃣ Install Dependencies (ONE TIME)**

```bash
/htec-libraries-init
```

**What this installs**:
- Python packages (PDF processing, Office docs)
- Playwright browsers (visual testing)
- TypeScript LSP (code intelligence)
- Image processing libraries

**Duration**: 2-3 minutes

---

**2️⃣ Initialize Project Metadata (REQUIRED)**

```bash
/project-init
```

**Interactive prompts**:
```
✅ Detected user: milosc79

❓ What is the name of your project?
   [ ] Use current directory name
   [ ] Specify custom name

❓ Enter project name:
   InventorySystem
```

**Why this matters**:
- ✅ Traceability logs show YOUR name (not "Claude" or "system")
- ✅ All artifacts reference correct project name
- ✅ Session validation passes (no warnings)

**Duration**: 1 minute

---

**3️⃣ Prepare Client Materials**

```bash
mkdir -p Client_Materials
cp ~/interviews/*.md Client_Materials/
cp ~/designs/*.png Client_Materials/
cp ~/requirements/*.pdf Client_Materials/
```

**Supported formats**:
- Text: `.md`, `.txt`, `.docx`
- PDFs: `.pdf` (auto-chunked if >10 pages)
- Images: `.png`, `.jpg`, `.jpeg`
- Spreadsheets: `.xlsx`, `.csv`

---

**4️⃣ Run Discovery Analysis**

```bash
/discovery-multiagent InventorySystem Client_Materials/
```

**What happens**:
- ⚡ 7+ agents run in parallel (interview-analyst, pdf-analyst, etc.)
- 📊 11 checkpoints (CP-01 → CP-11)
- ⏱️ ~60-75 minutes (vs. 2.5 hours sequential)
- ✅ 21 deliverables generated

**Monitor progress**:
```bash
/discovery-status
```

**Output**:
```
ClientAnalysis_InventorySystem/
├── 01-inputs/          # Processed materials
├── 02-personas/        # User profiles
├── 03-research/        # JTBD, pain points
├── 04-strategy/        # Vision, roadmap
├── 05-design-specs/    # Screens, components
└── 06-documentation/   # Consolidated docs
```

---

**5️⃣ Generate Prototype (Optional)**

```bash
/prototype InventorySystem
```

**Output**: Working React app at `Prototype_InventorySystem/prototype/`

**Test it**:
```bash
cd Prototype_InventorySystem/prototype
npm install
npm run dev
# → Open http://localhost:3000
```

---

**6️⃣ Generate ProductSpecs (Optional)**

```bash
/productspecs InventorySystem
```

**Output**: JIRA-ready module specs at `ProductSpecs_InventorySystem/`

---

## 🆘 Troubleshooting

### "Session validation warning"

**Problem**:
```
⚠️  PROJECT NAME IS INVALID: 'pending'
Run /project-init to fix
```

**Solution**:
```bash
/project-init
```

---

### "ModuleNotFoundError: pypdfium2"

**Problem**: Dependencies not installed

**Solution**:
```bash
/htec-libraries-init
```

---

### "User: unknown"

**Problem**: Git not configured

**Solution**:
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## 📖 Next Steps

### Immediate
1. ✅ Complete your first Discovery workflow
2. ✅ Review generated personas and requirements
3. ✅ Provide feedback via `/discovery-feedback`

### This Week
1. Complete full pipeline (Discovery → Prototype → ProductSpecs)
2. Understand traceability chains
3. Learn manual commands for targeted updates

### This Month
1. Master multi-agent orchestration
2. Customize agent prompts
3. Extend framework with custom skills

---

## 📚 Documentation

### Essential Reading (in order)

1. **FRAMEWORK_ONBOARDING.md** (15 min) ← START HERE
   - Complete framework initialization guide
   - Session management
   - 5-stage overview

2. **DISCOVERY_ONBOARDING.md** (30 min)
   - Discovery phase deep-dive
   - Multi-agent architecture
   - Command reference

3. **PROTOTYPE_ONBOARDING.md** (25 min)
   - Prototype generation
   - Design system workflow
   - Visual validation

4. **SOLUTION_SPECIFICATION_ONBOARDING.md** (30 min)
   - ProductSpecs workflow
   - Module specifications
   - JIRA export

5. **Implementation_Phase_WoW.md** (40 min)
   - TDD implementation
   - Task decomposition
   - Code review process

### Quick References

| Guide | Time | Focus |
|-------|------|-------|
| **QUICK_START_GUIDE.md** | 3 min | This document |
| **CLAUDE.md** (project root) | 10 min | Command reference |
| **CORE_RULES.md** | 5 min | Essential rules |

---

## 🎯 Success Criteria

After completing this guide, you should be able to:

- ✅ Run `/htec-libraries-init` successfully
- ✅ Run `/project-init` and see valid session
- ✅ Execute `/discovery-multiagent` and generate 21 artifacts
- ✅ Understand session validation (no "pending"/"system" warnings)
- ✅ Navigate generated outputs (personas, JTBD, requirements)
- ✅ Check progress with status commands (`/discovery-status`)

---

## 🔗 Related Documentation

**In `.claude/architecture/Workflows/`**:
- `FRAMEWORK_ONBOARDING.md` - Complete onboarding (15 min)
- `Discovery Phase/DISCOVERY_ONBOARDING.md` - Discovery deep-dive
- `Idea Shaping and Validation Phase/PROTOTYPE_ONBOARDING.md` - Prototype guide
- `Solution Specification Phase/SOLUTION_SPECIFICATION_ONBOARDING.md` - ProductSpecs guide
- `Implementation Phase/Implementation_Phase_WoW.md` - Implementation WoW

**In project root**:
- `CLAUDE.md` - Command reference + workflow overview
- `SESSION_INIT_IMPLEMENTATION_SUMMARY.md` - Technical details on session management

**In `.claude/rules/`**:
- `CORE_RULES.md` - Framework rules (error handling, traceability)
- `QUICK_REFERENCE.md` - Rule system overview

---

**End of Quick Start Guide**

*Version 1.0.0 | January 29, 2026 | HTEC I2M Accelerator Framework*
