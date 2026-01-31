# HTEC Framework Core Rules

**Version**: 3.0.0 (Path-specific auto-loading)
**Always Loaded**: Yes
**Token Budget**: ~2.5k tokens

---

## 1. Interaction Style

**Conciseness**: When running slash commands, minimize conversational text.
- ❌ Bad: "I will now proceed to run the discovery analysis. This involves..."
- ✅ Good: "🚀 Starting Discovery Analysis..."

**Progress Indicators**:
- ⏳ Processing
- ✅ Success
- ⚠️ Warning
- ❌ Error

**Error Reporting**: Provide exact command to fix or specific file that caused the error. No stack traces unless requested.

**Proactiveness**: After command completion, suggest logical next command based on workflow.

---

## 2. Error Handling (Critical)

### One Attempt Rule
When encountering ANY error during file processing or command execution:
1. **Log the failure** (to `_state/FAILURES_LOG.md` or console)
2. **SKIP the item** immediately
3. **CONTINUE** to the next item/phase

**NEVER**:
- ❌ Retry the same operation (unless explicitly prompted by user)
- ❌ Try a different library (no `pdfplumber`, `pypdf`, `markitdown` swaps)
- ❌ Try `pip install` or system modifications
- ❌ Ask the user what to do (unless it's a BLOCKING error)
- ❌ Wait for user input

### Skip Triggers (Technical - Non-recoverable)
Skip immediately if you see technical IO errors:
- "PDF too large" (or >30 pages without chunking support)
- "ModuleNotFoundError" / "command not found"
- "Exit code 1" / "Exit code 127" (Technical error)
- "Timeout" / "Permission denied"
- "Parse error" (Technical)

### Correction Triggers (Quality - RECOVERABLE)
DO NOT skip if the error is a **Quality Violation**. You MUST fix and retry:
- "❌ QUALITY ERROR": Missing deliverable, metadata, or IDs
- "Traceability gap": Orphaned requirements or screens
- "Empty/Placeholder file": Detected by size checks (<100 bytes)
- **Rule**: Fix the artifact → Rerun quality gates → Only then proceed

### Legitimate Blocks (Stop and Ask)
Only stop for:
1. **Critical Missing Inputs**: `discovery_summary.json`, `requirements_registry.json`
2. **Quality Gates**: P0 test coverage < 100%
3. **User Instruction**: User explicitly says "pause" or "stop"
4. **Explicit Block**: Skill logic specifies "BLOCK: [reason]"

---

## 3. Traceability (Lightweight)

### MANDATORY: Version History Logging

**Every file change (create, modify, delete) MUST be logged.**

**After every Write/Edit/Delete**:

```bash
python3 .claude/hooks/version_history_logger.py \
  "traceability/" \
  "{system_name}" \
  "{stage}" \
  "Claude" \
  "{version}" \
  "{reason}" \
  "{refs_comma_separated}" \
  "{file_path}" \
  "{action}"
```

**Parameters**:
- `system_name`: From `_state/pipeline_config.json` or `_state/discovery_config.json`
- `stage`: `discovery`, `prototype`, `productspecs`, `solarch`, `implementation`
- `version`: From `.claude/version.json` (Major.Minor) + local Patch
- `reason`: Single sentence explaining the change
- `refs_comma_separated`: IDs this change traces to (e.g., `JTBD-1,REQ-003,T-010`)
- `action`: `creation`, `modification`, `deletion`

**Failure to log is a framework integrity violation.** Even deletions must be logged.

### Automatic Loading

Detailed traceability rules auto-load when working with stage output folders or traceability registries. See `.claude/rules/traceability.md` for full details.

---

## 3.5. Session Initialization (VALIDATION)

### Validation Before Orchestrators

**All main orchestrator commands include session validation.**

**Pattern** (already integrated in commands):
```bash
# Before running /discovery, /prototype, /productspecs, /solarch, /htec-sdd-*
python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/validate_session.py" --warn-only || true
```

**Invalid values** (trigger validation warnings):
- `project: "pending"`, `"unknown"`, `"system"`, `""`, `null`
- `user: "system"`, `"unknown"`, `"Claude"`, `""`, `null`

**Behavior**: Warnings are displayed but execution continues. This is non-blocking to avoid disrupting existing workflows.

### User Context Extraction

**NEVER hardcode "Claude" or "system" for author/user fields.**

**Always use**:
```bash
# In bash scripts
USER_NAME=$(python3 .claude/hooks/get_user_context.py)

# In Python scripts
from get_user_context import get_operator_name
user = get_operator_name()
```

**Fallback chain**: git user.name → git user.email → OS username → "unknown"

### Project Initialization Flow

**New project workflow**:
1. User runs `/project-init` (captures project name + user context)
2. Session validated: `validate_session.py` passes
3. User runs orchestrator: `/discovery <ProjectName> ...`
4. Orchestrator validates session and proceeds

**Existing project workflow**:
1. User runs orchestrator directly: `/discovery <ProjectName> ...`
2. Orchestrator shows validation warnings if session is invalid
3. User runs `/project-init` to fix warnings (optional but recommended)
4. Future commands show no warnings

**Fix invalid session**:
```bash
/project-init
```

---

## 4. Execution Logging (MANDATORY)

### Command Execution Pattern

```bash
# 1. BEFORE command starts - capture event_id
EVENT_ID=$(python3 .claude/hooks/command_start.py \
  --command-name "/<command>" \
  --stage "<stage>" \
  --system-name "<SystemName>" \
  --intent "<description>")

# 2. Execute command logic...

# 3. AFTER command completes
python3 .claude/hooks/command_end.py \
  --command-name "/<command>" \
  --stage "<stage>" \
  --status "completed" \
  --start-event-id "$EVENT_ID" \
  --outputs '{"files_created": N}'
```

### Skill Execution Pattern

```bash
# 1. BEFORE skill starts
SKILL_EVENT=$(python3 .claude/hooks/skill_invoke.py \
  --skill-name "<SkillName>" \
  --action start \
  --stage "<stage>" \
  --system-name "<SystemName>" \
  --intent "<description>")

# 2. Execute skill logic...

# 3. AFTER skill completes
python3 .claude/hooks/skill_invoke.py \
  --skill-name "<SkillName>" \
  --action end \
  --start-event-id "$SKILL_EVENT" \
  --status "completed" \
  --outputs '{"output_files": ["file1.md", "file2.md"]}'
```

**NEVER Skip Logging** - Logging is BLOCKING, do not proceed without it.

---

## 5. Path-Specific Rules (Auto-Loading)

Rules automatically load based on **which files you're working with**:

| Rule File | Auto-Loads When Working With |
|-----------|------------------------------|
| **traceability.md** | Stage output folders, traceability registries, _state files |
| **discovery.md** | ClientAnalysis_* folders, Client_Materials |
| **process-integrity.md** | Implementation_* folders, test files (*.test.ts, *.spec.ts) |
| **agent-coordination.md** | .claude/agents/, .claude/skills/ |
| **inline-docs.md** | *_readme.md files, agent/skill definitions, implementation code |

**How it works**: Claude Code detects file paths and loads matching rules automatically. No manual loading needed.

### Manual Loading (Optional)

If you need to load rules explicitly, skill commands are still available:

```bash
/rules-traceability         # ID formats, chains, validation
/rules-discovery            # Discovery input/output structure
/rules-process-integrity    # TDD, quality gates
/rules-agent-coordination   # Multi-agent coordination
/rules-inline-docs          # Documentation standards
```

---

## 6. Quick ID Reference

### Common ID Formats

| Artifact | Format | Example |
|----------|--------|---------|
| Client Materials | CM-XXX | CM-001 |
| Pain Points | PP-X.X | PP-1.2 |
| JTBD | JTBD-X.X | JTBD-2.1 |
| Requirements | REQ-XXX | REQ-015 |
| Screens | SCR-XXX | SCR-003 |
| Modules | MOD-XXX-XXX-NN | MOD-DSK-AUTH-01 |
| ADRs | ADR-XXX | ADR-003 |
| Tasks | T-NNN | T-042 |

For complete ID formats and traceability chains, see `.claude/rules/traceability.md` (auto-loads when working with stage outputs).

---

## 7. File Operations Best Practices

### Before Editing
- ALWAYS use Read tool before Edit/Write
- NEVER edit files you haven't read
- Understand existing code before suggesting modifications

### Prefer Edit Over Write
- ALWAYS prefer editing existing files
- NEVER write new files unless explicitly required
- Use Write only for genuinely new files

### Documentation
- Do NOT create documentation files (`*.md`, `README.md`) unless explicitly requested
- Use inline documentation pattern (`{unit_name}_readme.md`) - see `.claude/rules/inline-docs.md` (auto-loads when working with documentation)

---

## 8. Quality Guardrails

### Validation Commands

```bash
# Validate checkpoint (Discovery)
python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint N

# Validate checkpoint (Implementation)
python3 .claude/hooks/implementation_quality_gates.py --validate-checkpoint N

# Validate traceability chains
python3 .claude/hooks/implementation_quality_gates.py --validate-traceability

# Check file integrity
python3 .claude/hooks/discovery_quality_gates.py --validate-file <Path>
```

### Self-Correction Protocol
If validation fails:
1. **ANALYZE** the error
2. **FIX** the root cause
3. **RETRY** validation
4. Only then mark progress as complete

---

## 9. PDF Handling (10-Page Threshold)

```bash
# Check page count FIRST
.venv/bin/python .claude/skills/tools/pdf_splitter.py count <file.pdf>

# If >10 pages, convert to Markdown
.venv/bin/python .claude/skills/tools/pdf_splitter.py automd <file.pdf> [OUTPUT_DIR]/
```

---

## 10. Path-Specific Rules Reference

Detailed rules in `.claude/rules/` auto-load based on file paths:

| File | Contents | Auto-Loads When |
|------|----------|-----------------|
| **traceability.md** | ID formats, chains, version logging | Working with stage outputs, traceability/* |
| **discovery.md** | Input processing, output structure, checkpoints | Working with ClientAnalysis_*, Client_Materials |
| **process-integrity.md** | TDD cycle, quality gates, veto protocol | Working with Implementation_*, test files |
| **agent-coordination.md** | Spawning, locks, sessions, monitoring | Working with .claude/agents/, .claude/skills/ |
| **inline-docs.md** | _readme.md convention, documentation standards | Working with *_readme.md, implementation code |

**No manual loading needed** - rules appear automatically when relevant. Skill commands (`/rules-*`) available for explicit loading if needed.

---

## Related Documentation

- **Path-Specific Rules**: `.claude/rules/*.md` (auto-load based on file paths)
- **CLAUDE.md**: Project overview, workflows, commands
- **architecture/**: Full architecture documentation
- `.claude/agents/`: Agent definitions
- `.claude/commands/`: Command definitions
- `.claude/skills/`: Skill definitions

---

**Context Efficiency**: This core rules file is ~2.5k tokens. Path-specific rules (~14k tokens) auto-load only when working with relevant files, providing 72% context savings for simple tasks.
