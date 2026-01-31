---
document_id: DOC-FEEDBACK-README
version: 1.0.0
created_at: 2025-12-22
updated_at: 2025-12-22
generated_by: Claude Code
source_files:
  - User requirements
change_history:
  - version: "1.0.0"
    date: "2025-12-22"
    author: "Claude Code"
    changes: "Initial documentation creation"
---

# Discovery Feedback Management System

## Overview

The Discovery Feedback Management System is a comprehensive workflow for processing stakeholder feedback on discovery artifacts. It provides structured impact analysis, implementation planning, change execution with full traceability, and validation.

## Components Created

### 1. Slash Command

| File | Description |
|------|-------------|
| `.claude/commands/discovery-feedback.md` | Main command orchestrating the feedback workflow |

### 2. Skills (5 Total)

| Skill | Location | Description |
|-------|----------|-------------|
| Discovery_FeedbackAnalyzer | `.claude/skills/Discovery_FeedbackAnalyzer/SKILL.md` | Analyzes feedback impact across discovery artifacts |
| Discovery_FeedbackRegister | `.claude/skills/Discovery_FeedbackRegister/SKILL.md` | Manages feedback registry with unique IDs |
| Discovery_FeedbackPlanner | `.claude/skills/Discovery_FeedbackPlanner/SKILL.md` | Generates implementation plans |
| Discovery_FeedbackImplementer | `.claude/skills/Discovery_FeedbackImplementer/SKILL.md` | Executes changes with traceability |
| Discovery_FeedbackValidator | `.claude/skills/Discovery_FeedbackValidator/SKILL.md` | Validates implementation against plan |

### 3. Data Files

| File | Description |
|------|-------------|
| `traceability/feedback_sessions/discovery/discover_feedback_register.json` | Central registry for all feedback items |

### 4. Folder Structure

```
traceability/
└── feedback_sessions/
    └── discovery/
        ├── discover_feedback_register.json    # Central registry
        └── <YYYY-MM-DD>_Feedback_<NNN>/       # Session folders (created per feedback)
            ├── FEEDBACK_ORIGINAL.md
            ├── IMPACT_ANALYSIS.md
            ├── IMPLEMENTATION_PLAN.md
            ├── IMPLEMENTATION_LOG.md
            ├── VALIDATION_REPORT.md
            └── FEEDBACK_SUMMARY.md
```

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    DISCOVERY FEEDBACK WORKFLOW                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1: INPUT COLLECTION                                       │
│  ├── Receive feedback (text or file)                            │
│  ├── Identify target system (ClientAnalysis_<Name>)             │
│  └── Collect metadata (source, inputter, timestamp)             │
│                                                                  │
│  Phase 2: IMPACT ANALYSIS                                        │
│  ├── Scan all discovery outputs                                 │
│  ├── Classify by category (Persona, JTBD, Strategy, etc.)      │
│  ├── Calculate priority score (0-30)                            │
│  └── Generate impact matrix                                     │
│                                                                  │
│  Phase 3: REGISTRATION                                           │
│  ├── Assign unique ID (FB-001, FB-002...)                       │
│  ├── Create session folder                                      │
│  └── Log to discover_feedback_register.json                     │
│                                                                  │
│  Phase 4: APPROVAL GATE                                          │
│  ├── Present impact summary                                     │
│  └── User decision: [Approve] [Reject] [Modify]                 │
│      │                                                          │
│      ├─[Reject]─→ Log rejection → END                           │
│      │                                                          │
│      └─[Approve]─→ Continue                                     │
│                                                                  │
│  Phase 5: IMPLEMENTATION PLANNING                                │
│  ├── Generate 2+ plan options                                   │
│  ├── User selects plan OR provides custom                       │
│  ├── Evaluate custom plan completeness                          │
│  └── Plan confirmation gate                                     │
│                                                                  │
│  Phase 6: IMPLEMENTATION                                         │
│  ├── Execute plan step-by-step                                  │
│  ├── Update file versions (MAJOR/MINOR/PATCH)                   │
│  ├── Add FB reference to change_history                         │
│  ├── Update traceability registries                             │
│  └── Handle partial failures (resume capability)                │
│                                                                  │
│  Phase 7: VALIDATION                                             │
│  ├── Verify plan compliance                                     │
│  ├── Check version integrity                                    │
│  ├── Validate traceability completeness                         │
│  ├── Run Discovery_Validate                                     │
│  └── Rebuild traceability                                       │
│                                                                  │
│  Phase 8: COMPLETION                                             │
│  ├── Generate FEEDBACK_SUMMARY.md                               │
│  ├── Update registry status                                     │
│  └── Report results                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Feedback Registry Schema

```json
{
  "id": "FB-001",
  "status": "pending|approved|rejected|in_progress|implemented|validated|failed",
  "metadata": {
    "source_person": "Who provided feedback",
    "inputter_person": "Who entered it",
    "received_at": "ISO timestamp",
    "logged_at": "ISO timestamp",
    "last_updated": "ISO timestamp"
  },
  "content": {
    "summary": "Brief summary",
    "full_text": "Full content",
    "source_file": "Path if from file"
  },
  "classification": {
    "category": "CAT-PER|CAT-PP|CAT-JTBD|CAT-VIS|CAT-STR|etc.",
    "priority": "P0|P1|P2",
    "effort_estimate": "S|M|L|XL",
    "confidence": "High|Medium|Low"
  },
  "impact": {
    "files_affected": 5,
    "high_impact_count": 2,
    "traceability_ids": ["PP-001", "JTBD-2.1"],
    "priority_score": 18
  },
  "lifecycle": {
    "approved_at": null,
    "approved_by": null,
    "rejected_at": null,
    "rejected_by": null,
    "rejection_reason": null,
    "implemented_at": null,
    "validated_at": null
  }
}
```

## Impact Categories

| Category ID | Description | Affected Areas |
|-------------|-------------|----------------|
| CAT-PER | Persona changes | `02-research/personas/` |
| CAT-PP | Pain point changes | `01-analysis/PAIN_POINTS.md` |
| CAT-JTBD | Jobs-to-be-done changes | `02-research/JOBS_TO_BE_DONE.md` |
| CAT-VIS | Vision changes | `03-strategy/PRODUCT_VISION.md` |
| CAT-STR | Strategy changes | `03-strategy/PRODUCT_STRATEGY.md` |
| CAT-RDM | Roadmap changes | `03-strategy/PRODUCT_ROADMAP.md` |
| CAT-KPI | KPI changes | `03-strategy/KPIS_AND_GOALS.md` |
| CAT-SCR | Screen design changes | `04-design-specs/screen-definitions.md` |
| CAT-NAV | Navigation changes | `04-design-specs/navigation-structure.md` |
| CAT-DAT | Data model changes | `04-design-specs/data-fields.md` |
| CAT-GEN | General/cross-cutting | Multiple areas |

## Version Control Integration

All modified files follow VERSION_CONTROL_STANDARD.md:

```yaml
---
document_id: <ID>
version: X.Y.Z              # Incremented based on change type
updated_at: 2025-12-22      # Today's date
change_history:
  - version: "X.Y.Z"
    date: "2025-12-22"
    author: "Discovery_FeedbackImplementer"
    changes: "FB-001: <description>"   # FB reference included
---
```

### Version Bump Rules

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Structure change | MAJOR | 1.0.0 → 2.0.0 |
| New content added | MINOR | 1.0.0 → 1.1.0 |
| Content modified | PATCH | 1.0.0 → 1.0.1 |

## Usage Examples

### Process Direct Feedback

```
/discovery-feedback "The warehouse operator needs mobile access for cycle counting"
```

### Process Feedback from File

```
/discovery-feedback ./client_feedback_20251222.md
```

### Interactive Mode

```
/discovery-feedback
```
Then follow prompts.

### Resume Failed Implementation

```
/discovery-feedback resume FB-003
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| File read failure | Skip file, continue analysis |
| File write failure | Log failure, save resume point |
| Partial implementation | Keep successful changes, mark for resume |
| Validation failure | Report issues, suggest remediation |

## Integration Points

### Receives From
- User input (text or file)
- Discovery outputs (`ClientAnalysis_<Name>/`)

### Feeds Into
- Discovery_Validate (re-run after implementation)
- Traceability_Manager (registry updates)
- All discovery artifact files (version updates)

## Design Decisions

### 1. Sequential IDs (FB-001)
Chosen over UUID for human readability and easy tracking.

### 2. Session Folders
Each feedback creates a dedicated folder for complete audit trail.

### 3. Partial Failure Handling
Successful changes are preserved; resume capability for failures.

### 4. Two-Gate Approval
- Gate 1: Approve/Reject feedback
- Gate 2: Confirm implementation plan

### 5. Automatic Traceability
FB-NNN reference automatically added to all modified file headers.

## Plugins Considered

The following plugins were installed but not specifically integrated:
- `kaizen@NeoLabHQ/context-engineering-kit`
- `reflexion@NeoLabHQ/context-engineering-kit`
- `git@NeoLabHQ/context-engineering-kit`
- `sadd@NeoLabHQ/context-engineering-kit`
- `sdd@NeoLabHQ/context-engineering-kit`
- `tech-stack@NeoLabHQ/context-engineering-kit`

These plugins may provide additional capabilities for future enhancements.

## Files Modified

### Created
- `.claude/commands/discovery-feedback.md`
- `.claude/skills/Discovery_FeedbackAnalyzer/SKILL.md`
- `.claude/skills/Discovery_FeedbackRegister/SKILL.md`
- `.claude/skills/Discovery_FeedbackPlanner/SKILL.md`
- `.claude/skills/Discovery_FeedbackImplementer/SKILL.md`
- `.claude/skills/Discovery_FeedbackValidator/SKILL.md`
- `traceability/feedback_sessions/discovery/discover_feedback_register.json`
- `.claude/skills/Discovery_Feedback_README.md` (this file)

### Updated
- `CLAUDE.md` - Added Feedback Management section and commands

---

**Documentation Version**: 1.0.0
**Created**: 2025-12-22
**Author**: Claude Code
