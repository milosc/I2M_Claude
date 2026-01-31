# Requirements Traceability Format

## Component Spec Format

Each component spec must include:

```markdown
## Requirements Addressed

| Req ID | Type | Description | How Addressed |
|--------|------|-------------|---------------|
| A11Y-001 | Accessibility | Color Contrast | Uses design tokens with 4.5:1 ratio |
| A11Y-002 | Accessibility | Keyboard Accessible | Full keyboard support documented |
| PP-005 | Pain Point | Slow feedback on actions | Immediate visual feedback states |
```

## Screen Spec Format

Each screen spec must include:

```markdown
## Requirements Addressed

### User Stories

| Req ID | Title | Acceptance Criteria Met |
|--------|-------|-------------------------|
| US-xxx | [Title] | [List criteria covered] |

### Jobs To Be Done

| Req ID | Title | How Addressed |
|--------|-------|---------------|
| JTBD-xxx | [Title] | [How this screen fulfills the job] |

### Pain Points Resolved

| Req ID | Title | Solution |
|--------|-------|----------|
| PP-xxx | [Title] | [How this screen solves it] |

### Functional Requirements

| Req ID | Title | Implementation |
|--------|-------|----------------|
| FR-xxx | [Title] | [How implemented in this screen] |
```

## Validation Rules

- ❌ **FAIL**: Missing Requirements Addressed section
- ❌ **FAIL**: P0 User Story with unmet acceptance criteria  
- ❌ **FAIL**: Screen in registry with zero requirements addressed
- ⚠️ **WARN**: P1 requirements not addressed
- ⚠️ **WARN**: Pain point assigned to screen not addressed
