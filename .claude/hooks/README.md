# HTEC Claude Code Quality Gates (Hooks)

Welcome to the HTEC Quality Framework. This directory contains the "Quality Police" of the system—a set of validation scripts (hooks) that ensure every deliverable meets our rigorous standards for metadata, structure, and traceability.

## 🎯 The "Hook" Philosophy

In this framework, **Speed < Quality**. 

While these are called "hooks," they are primarily **CLI Quality Gates** called at the end of every phase. Claude is strictly forbidden from proceeding to a subsequent phase (e.g., moving from Research to Strategy) unless the gate for the current phase returns a "PASS."

### Why do we use them?
1.  **Consistency**: Ensures all AI-generated files look and feel like they were written by a single senior engineer/architect.
2.  **Traceability**: Validates that every screen traces back to a feature, every feature to a job (JTBD), and every job to a pain point.
3.  **Predictability**: Prevents the "hallucination drift" where the AI forgets project constraints halfway through the workflow.
4.  **Auditability**: Every validation event is logged, creating a trail of quality for human reviewers.

---

## 🛠 Available Quality Gates

| Script | Workflow Stage | Purpose |
|--------|----------------|---------|
| `discovery_quality_gates.py` | **Discovery** | Validates the 11 checkpoints from Analysis to Roadmap and Design Specs. |
| `productspecs_quality_gates.py` | **Product Specs** | Ensures functional/non-functional requirements and test cases are valid. |
| `solarch_quality_gates.py` | **SolArch** | Validates Architecture Decision Records (ADRs) and C4 Diagrams. |
| `prototype_quality_gates.py` | **Prototype** | Checks data models, API contracts, and generated component code. |
| `implementation_quality_gates.py` | **Implementation** | Validates code changes, unit test coverage, and PR descriptions. |
| `integrity_checker.py` | **Cross-Stage** | Ensures that changes in one stage haven't broken traceability in another. |

---

## 🔄 High-Level Procedure

Every stage in the HTEC pipeline follows this "Gate Pattern":

1.  **Execution**: Claude executes a skill (e.g., `Discovery_GeneratePersona`) to create an artifact.
2.  **Invocation**: Claude calls the relevant hook via the CLI.
    *   *Example*: `python3 .claude/hooks/discovery_quality_gates.py --validate-file path/to/file.md`
3.  **Validation**: The script performs three levels of checks:
    *   **L1 (Metadata)**: Does it have the correct YAML frontmatter?
    *   **L2 (Structure)**: Are mandatory headers present? Is the file naming correct (UPPERCASE vs lowercase)?
    *   **L3 (Content)**: Are the IDs (PP-1.1, JTBD-2.2) valid and linked correctly?
4.  **Gating**: 
    *   **PASS**: Claude logs the success in `PROGRESS_TRACKER.md` and moves to the next task.
    *   **FAIL**: Claude is blocked. It must read the error message, fix the artifact, and re-run the hook.

---

## 📏 Enforcement Rules (v6.0)

### 1. The Metadata Mandate
Every Markdown file produced by a skill MUST start with a YAML block. The hooks will fail any file missing this:
```yaml
---
document_id: DISC-PERSONA-001
version: 1.0.0
created_at: 2025-12-28
generated_by: Discovery_GeneratePersona
---
```

### 2. Naming Conventions
- **Discovery (Strategy/Research)**: `UPPERCASE_WITH_UNDERSCORES.md` (e.g., `PRODUCT_VISION.md`)
- **Discovery (Design Specs)**: `lowercase-with-dashes.md` (e.g., `screen-definitions.md`)
- **Prototype**: Follows framework standards (PascalCase for React components).

### 3. Traceability ID Patterns
Hooks scan for these patterns and will error if they are missing or malformed:
- `PP-X.Y`: Pain Points
- `JTBD-X.Y`: Jobs to be Done
- `US-X.Y` / `FR-X.Y`: User Stories / Functional Requirements
- `S-X.Y`: Screens
- `ADR-XXX`: Architecture Decisions

### 4. Smart Obsolescence (NOT_APPLICABLE)
If a project is classified as `BACKEND_ONLY` (via `Discovery_ClassifyProject`), the hooks use `na_validation_utils.py` to allow skipping UI-related checkpoints (like screens) while still requiring data-models and personas.

---

## 🚀 Usage for Newcomers

If you are a human developer or a new sub-agent, you can interact with the gates manually to verify your work:

```bash
# List all required files for Discovery Checkpoints
python3 .claude/hooks/discovery_quality_gates.py --list-checkpoints

# Validate an entire directory for a specific checkpoint
python3 .claude/hooks/discovery_quality_gates.py --validate-checkpoint 4 --dir ClientAnalysis_MyProject/

# Run a global integrity check across the whole codebase
python3 .claude/hooks/integrity_checker.py --full-audit
```

## 📈 Log & Traceability
All validation results are recorded in:
- `.claude/hooks/hook_log.jsonl` (Technical log)
- `_state/discovery_progress.json` (Phase status)
- `_state/lifecycle.json` (Event lifecycle)
- `_state/permission_audit.json` (Permission requests)
- `traceability/trace_matrix.json` (Link validation)

---

## 🛡️ Self-Validating Hooks (New in v2.0)

The framework now includes **self-validating hooks** that enforce quality gates deterministically. Unlike traditional validation that relies on Claude following instructions, these hooks **block** Claude from completing commands until all validators pass.

### Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     HTEC HOOKS ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  LAYER 1: GLOBAL HOOKS (settings.json)                              │
│  ├── PreToolUse: security_gate.py (Bash blocking)                   │
│  ├── PostToolUse: capture_event.py (logging)                        │
│  ├── PermissionRequest: permission_audit.py                         │
│  ├── PostToolUseFailure: capture_failure.py                         │
│  └── SubagentStart: capture_event.py                                │
│                                                                      │
│  LAYER 2: COMMAND HOOKS (frontmatter)                               │
│  ├── Stop: validate_*_output.py (output completeness)               │
│  ├── Stop: validate_file_contains.py (required sections)            │
│  └── Stop: log-lifecycle.sh (lifecycle logging)                     │
│                                                                      │
│  LAYER 3: AGENT HOOKS (frontmatter)                                 │
│  ├── PreToolUse: file_lock_acquire.py (file locking)                │
│  ├── PostToolUse: ruff_validator.py (Python linting)                │
│  ├── PostToolUse: ty_validator.py (Python type checking)            │
│  └── PostToolUse: tdd_compliance_check.py (TDD enforcement)         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Exit Code Protocol

All validators follow this exit code convention:

| Exit Code | Meaning | Hook Behavior |
|-----------|---------|---------------|
| 0 | Validation passed | Allow Claude to continue |
| 1 | Validation failed | Block Claude from stopping |
| 2 | Critical/Security | Force Claude to address |

### Validators Library

Located in `.claude/hooks/validators/`:

| Validator | Type | Purpose |
|-----------|------|---------|
| `security_gate.py` | Security | Block dangerous bash commands |
| `validate_files_exist.py` | Generic | Check file patterns exist |
| `validate_file_contains.py` | Generic | Check required content |
| `validate_frontmatter.py` | Generic | Check YAML metadata |
| `ruff_validator.py` | Code Quality | Python linting |
| `ty_validator.py` | Code Quality | Python type checking |
| `validate_discovery_output.py` | Stage | Discovery completeness |
| `validate_prototype_output.py` | Stage | Prototype completeness |
| `validate_productspecs_output.py` | Stage | ProductSpecs completeness |
| `validate_solarch_output.py` | Stage | SolArch completeness |
| `permission_audit.py` | Audit | Log permission requests |
| `capture_failure.py` | Audit | Log tool failures |

See `.claude/hooks/validators/README.md` for detailed usage.

### Running Tests

```bash
# Run all validator tests
uv run .claude/hooks/tests/test_validators.py

# Run with pytest
uv run pytest .claude/hooks/tests/test_validators.py -v
```

---

## 🔍 Detailed Hook Explanations

### 1. `discovery_quality_gates.py` (Discovery Stage)
Validates the initial phase from initialization to final documentation (11 checkpoints).
- **Key Checks**: Metadata frontmatter, naming conventions (UPPERCASE vs lowercase), traceability IDs (`PP-X.Y`, `JTBD-X.Y`, `US-X.Y`, `S-X.Y`), and smart obsolescence for non-UI projects.

### 2. `prototype_quality_gates.py` (Prototype Stage)
Validates the transition from discovery to a functional prototype (14 checkpoints).
- **Key Checks**: Data models, API contracts (OpenAPI), test data manifests, and critical propagation of `requirements_registry.json` to the root traceability folder. It also verifies React code coverage for all discovery screens.

### 3. `productspecs_quality_gates.py` (Product Specs Stage)
Validates detailed functional and non-functional requirements (8 checkpoints).
- **Key Checks**: Requirement hierarchy, module-to-screen mapping (`MOD-*.md`), JIRA export CSV format/hierarchy, and complete P0 traceability chains (Pain Point -> JTBD -> Requirement -> Screen -> Module -> Test).

### 4. `solarch_quality_gates.py` (Solution Architecture Stage)
Validates the architectural blueprint (12 checkpoints).
- **Key Checks**: ADR mandatory sections (Status, Context, Decision, Consequences, Traceability), C4 diagrams (Context/Container), risk assessment documentation, and deployment architecture completeness.

### 5. `implementation_quality_gates.py` (Implementation Stage)
Validates code changes and task completion (9 checkpoints).
- **Key Checks**: Task-to-requirement linking, code review status (`CODE_REVIEW.md`), 80% unit test coverage, and acceptance criteria verification in `task_registry.json`.

### 6. `integrity_checker.py` (Cross-Stage Auditor)
A global auditor that runs across the entire project root.
- **Key Checks**: Cross-stage orphan references, state file health ($documentation blocks), broken propagation chains, and template drift detection against original framework schemas.

### 7. `na_validation_utils.py` (The Enforcer Logic)
Shared utility library containing core logic for project classification lookups, applicability matrices, and N/A file format enforcement.

---

## 📱 Slack Notifications Setup

The framework supports Slack notifications for hook events (Notification, Stop, SubagentStop). This allows you to receive alerts when Claude needs input or completes tasks.

### Prerequisites

1. **Create a Slack App** at https://api.slack.com/apps
2. **Add Bot Token Scopes** under OAuth & Permissions:
   - `chat:write`
   - `chat:write.public` (for channels the bot isn't in)
3. **Install the app** to your workspace
4. **Copy the Bot Token** (starts with `xoxb-`)

### Configuration

**IMPORTANT**: `uv run` does NOT inherit shell environment variables or auto-load `.env` files. You must export variables in your shell profile.

**Add to `~/.zshrc` (or `~/.bashrc`):**

```bash
export SLACK_BOT_TOKEN="xoxb-your-actual-token-here"
export SLACK_CHANNEL="claude-notifications"  # or "#channel-name" or "C0123456789"
```

**Then reload and restart Claude Code:**

```bash
source ~/.zshrc
# Close and reopen terminal, then start Claude Code
```

### Testing

**1. Verify token is available to uv:**

```bash
cd /path/to/project
uv run python3 -c "import os; print('Token:', 'YES' if os.getenv('SLACK_BOT_TOKEN') else 'NO')"
```

**2. Test notification manually:**

```bash
uv run .claude/hooks/slack_notification_hook.py --event Notification
```

**3. Test via curl (direct):**

```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"claude-notifications","text":"Test from CLI"}'
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| `Token: NO` in uv test | Export in `~/.zshrc`, not just `.env` |
| `"not_authed"` error | Token invalid - regenerate in Slack App settings |
| `"channel_not_found"` | Use channel ID (e.g., `C0123456789`) instead of name |
| No notification sent | Check `_state/logs/slack_notifications.log` |

### Hook Events That Trigger Slack

Configured in `settings.json`:

| Event | When Triggered |
|-------|----------------|
| `Notification` | Claude needs user input |
| `Stop` | Main agent completes |
| `SubagentStop` | Sub-agent completes |

### Adding Custom Slack Hooks

To add Slack notifications for other events (e.g., `AskUserQuestion`), add to `settings.json`:

```json
{
  "PostToolUse": [
    {
      "matcher": "AskUserQuestion",
      "hooks": [
        {
          "type": "command",
          "command": "uv run \"$CLAUDE_PROJECT_DIR/.claude/hooks/slack_notification_hook.py\" --event Notification --quiet"
        }
      ]
    }
  ]
}
```

---

**Note**: If a hook fails, do not try to bypass it. The framework is designed to prevent technical debt from accumulating early in the discovery process. Fix the source artifact instead.