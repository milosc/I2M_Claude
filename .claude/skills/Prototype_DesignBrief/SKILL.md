---
name: generating-design-briefs
description: Use when you need to generate design direction, principles, and visual strategy based on discovery materials.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-design-briefs started '{"stage": "prototype"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-design-briefs ended '{"stage": "prototype"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-design-briefs instruction_start '{"stage": "prototype", "method": "instruction-based"}'
```

---

# Spec Design Briefs

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

## Metadata
- **Skill ID**: Prototype_DesignBrief
- **Version**: 2.3.1
- **Created**: 2024-12-13
- **Updated**: 2025-12-19
- **Author**: Milos Cigoj
- **Change History**:
  - v2.3.1 (2025-12-19): Added version control metadata per VERSION_CONTROL_STANDARD.md
  - v2.3.0 (2024-12-13): Initial skill version for Prototype Skills Framework v2.3

## Description
Generate design direction, principles, and visual strategy from discovery. Creates the foundational design documentation.

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning

Generate design brief and principles from discovery materials. Follows OUTPUT_STRUCTURE.md for deterministic folder structure.

## Execution Logging (MANDATORY)

This skill logs all execution to the global pipeline progress registry. Logging is automatic and requires no manual configuration.

### How Logging Works

Every execution of this skill is logged to `_state/lifecycle.json`:

- **start_event**: Logged when skill execution begins
- **end_event**: Logged when skill execution completes

Events include:
- skill_name, intent, stage, system_name
- start/end timestamps
- status (completed/failed)
- output files created (design briefs)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '"skill_name": "generating-design-briefs"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill "generating-design-briefs" --stage prototype
```

Logging is handled automatically by the skill framework. No user action required.

---

## Output Structure (REQUIRED)

This skill MUST generate the following files in `00-foundation/`:

```
00-foundation/
├── DESIGN_BRIEF.md                   # Visual direction and strategy
├── DESIGN_PRINCIPLES.md              # UX/UI design principles
└── ... (other foundation files)
```

---

## Procedure

### Step 1: Validate Inputs (REQUIRED)
```
READ discovery/01-stakeholder-interviews/ → brand guidelines, preferences
READ discovery/02-user-research/ → user needs, pain points
READ discovery/03-competitive-analysis/ → market positioning
READ _state/requirements_registry.json → requirements to address

IDENTIFY requirements this skill MUST address:
  - PP-XXX pain points (visual solutions)
  - UX-XXX user experience requirements
  - Brand requirements (if any)
  
IF discovery materials missing:
  ═══════════════════════════════════════════
  ⚠️ INPUT VALIDATION FAILED
  ═══════════════════════════════════════════
  
  Cannot generate design brief without discovery:
  • Missing: [list missing files]
  
  How would you like to proceed?
  1. "use defaults" - Generate with sensible defaults
  2. "provide: [path]" - Point to alternate source
  3. "abort" - Stop and gather discovery
  ═══════════════════════════════════════════
  
  WAIT for user response
```

### Step 2: Extract Design Inputs
```
FROM stakeholder interviews:
  - Brand personality
  - Color preferences
  - Existing brand assets
  - Target aesthetic
  
FROM user research:
  - User demographics
  - Device usage patterns
  - Accessibility needs
  - Mental models
  
FROM competitive analysis:
  - Market positioning
  - Differentiation opportunities
  - Industry conventions
```

### Step 3: Generate Design Brief
```
CREATE 00-foundation/DESIGN_BRIEF.md:
  # Design Brief
  
  ## Project Overview
  
  ### Product
  **Name:** {Product Name}
  **Type:** {Web Application / Mobile App / etc.}
  **Primary Users:** {Personas}
  
  ### Design Goals
  1. [Goal derived from discovery]
  2. [Goal derived from pain points]
  3. [Goal derived from requirements]
  
  ---
  
  ## Brand Direction
  
  ### Personality
  | Attribute | Description | Expression |
  |-----------|-------------|------------|
  | Professional | Trustworthy, competent | Clean layouts, consistent spacing |
  | Efficient | Fast, productive | Minimal clicks, quick actions |
  | Approachable | Friendly, not intimidating | Warm colors, helpful guidance |
  
  ### Voice & Tone
  - **Headlines:** Clear, action-oriented
  - **Body:** Conversational, helpful
  - **Errors:** Constructive, solution-focused
  - **Success:** Celebratory but brief
  
  ---
  
  ## Visual Strategy
  
  ### Color Direction
  | Role | Direction | Rationale |
  |------|-----------|-----------|
  | Primary | Blue family | Trust, professionalism |
  | Secondary | Teal/Green | Growth, success |
  | Accent | Orange/Amber | Attention, action |
  | Semantic | Standard | Error=red, Success=green |
  
  ### Typography Direction
  | Element | Direction | Rationale |
  |---------|-----------|-----------|
  | Headings | Sans-serif, bold | Clarity, hierarchy |
  | Body | Sans-serif, regular | Readability |
  | Data | Monospace (optional) | Alignment in tables |
  
  ### Layout Direction
  | Aspect | Direction | Rationale |
  |--------|-----------|-----------|
  | Density | Comfortable | Reduce cognitive load |
  | White space | Generous | Breathing room |
  | Grid | 12-column | Flexibility |
  
  ---
  
  ## User Experience Strategy
  
  ### Pain Points Addressed
  | Pain Point | Design Solution |
  |------------|-----------------|
  | PP-001: Manual tracking | Visual pipeline, drag-drop |
  | PP-002: Information scattered | Unified dashboard |
  | PP-003: Slow workflows | Quick actions, shortcuts |
  
  ### Key Interactions
  | Interaction | Approach |
  |-------------|----------|
  | Navigation | Persistent sidebar, breadcrumbs |
  | Data entry | Inline editing, auto-save |
  | Feedback | Toast notifications, inline validation |
  
  ---
  
  ## Accessibility Commitment
  
  ### WCAG Level Target: AA
  
  | Requirement | Commitment |
  |-------------|------------|
  | Color contrast | 4.5:1 minimum for text |
  | Focus indicators | Visible on all interactive |
  | Keyboard | Full functionality |
  | Screen readers | Semantic HTML, ARIA |
  
  ---
  
  ## Device Strategy
  
  ### Primary Platform: Desktop Web
  
  | Breakpoint | Target | Priority |
  |------------|--------|----------|
  | Desktop (1280px+) | Primary workflow | P0 |
  | Tablet (768px-1279px) | On-the-go review | P1 |
  | Mobile (< 768px) | Quick actions only | P2 |
  
  ---
  
  ## Success Metrics
  
  | Metric | Target | Measurement |
  |--------|--------|-------------|
  | Task completion | 95% | Usability testing |
  | Time on task | -30% vs current | Baseline comparison |
  | Error rate | < 5% | Analytics |
  | User satisfaction | 4.5/5 | Survey |
  
  ---
  
  ## Requirements Addressed
  
  | Req ID | Description | Design Solution |
  |--------|-------------|-----------------|
  | PP-001 | Manual tracking | Visual Kanban pipeline |
  | PP-002 | Scattered info | Unified candidate profile |
  | UX-001 | Easy navigation | Persistent sidebar |
```

### Step 4: Generate Design Principles
```
CREATE 00-foundation/DESIGN_PRINCIPLES.md:
  # Design Principles
  
  These principles guide all design decisions for {Product Name}.
  
  ---
  
  ## 1. Clarity Over Cleverness
  
  **Principle:** Users should understand the interface immediately without explanation.
  
  **Application:**
  - Use familiar patterns over novel interactions
  - Label buttons with verbs (Save, Delete, Send)
  - Show, don't tell—use visual hierarchy
  
  **Anti-patterns:**
  - Mystery icons without labels
  - Hidden functionality
  - Jargon in UI copy
  
  ---
  
  ## 2. Reduce Cognitive Load
  
  **Principle:** Minimize the mental effort required to complete tasks.
  
  **Application:**
  - Progressive disclosure—show only what's needed
  - Smart defaults—pre-fill when possible
  - Chunking—group related information
  
  **Anti-patterns:**
  - Information overload
  - Too many choices at once
  - Requiring memorization
  
  ---
  
  ## 3. Speed of Interaction
  
  **Principle:** Respect users' time—every click should be intentional.
  
  **Application:**
  - Minimize clicks for common actions
  - Keyboard shortcuts for power users
  - Optimistic UI updates
  
  **Anti-patterns:**
  - Unnecessary confirmation dialogs
  - Multi-page wizards for simple tasks
  - Loading states that block interaction
  
  ---
  
  ## 4. Consistent Patterns
  
  **Principle:** Same action = same result, everywhere.
  
  **Application:**
  - Reuse components across screens
  - Consistent placement of common actions
  - Unified visual language
  
  **Anti-patterns:**
  - Different edit patterns on different screens
  - Inconsistent button placement
  - Mixed interaction models
  
  ---
  
  ## 5. Accessible by Default
  
  **Principle:** Accessibility is not an afterthought—it's built in.
  
  **Application:**
  - Semantic HTML first
  - Keyboard navigation always
  - Color is never the only indicator
  
  **Anti-patterns:**
  - Color-only status indicators
  - Mouse-only interactions
  - Missing focus states
  
  ---
  
  ## 6. Graceful Feedback
  
  **Principle:** The system should always communicate its state clearly.
  
  **Application:**
  - Immediate feedback on actions
  - Clear error messages with solutions
  - Progress indication for long operations
  
  **Anti-patterns:**
  - Silent failures
  - Generic error messages
  - No feedback on success
  
  ---
  
  ## 7. Forgiving Interactions
  
  **Principle:** Users make mistakes—help them recover easily.
  
  **Application:**
  - Undo for destructive actions
  - Confirmation for irreversible operations
  - Auto-save drafts
  
  **Anti-patterns:**
  - Permanent deletion without warning
  - Lost work on navigation
  - No way to reverse actions
  
  ---
  
  ## Principle Checklist
  
  Before shipping any feature, verify:
  
  - [ ] Can a new user understand this without help?
  - [ ] Is cognitive load minimized?
  - [ ] Can the task be completed faster?
  - [ ] Does it follow existing patterns?
  - [ ] Is it fully accessible?
  - [ ] Does it provide appropriate feedback?
  - [ ] Can mistakes be easily corrected?
```

### Step 5: Link to Requirements
```
UPDATE _state/requirements_registry.json:
  FOR each pain point addressed:
    ADD "design_brief: DESIGN_BRIEF.md" to addressed_by[]
```

### Step 6: Validate Outputs (REQUIRED)
```
VALIDATE design documentation:
  FILE CHECKS:
    - 00-foundation/DESIGN_BRIEF.md exists
    - 00-foundation/DESIGN_PRINCIPLES.md exists
    
  CONTENT CHECKS:
    - Design brief has all required sections
    - Pain points mapped to solutions
    - Accessibility commitment defined
    - Principles are actionable
    
IF any validation fails:
  PROMPT with mitigation options
```

### Step 7: Update Progress
```
UPDATE _state/progress.json:
  phases.design_brief.status = "complete"
  phases.design_brief.completed_at = timestamp
  phases.design_brief.outputs = [
    "00-foundation/DESIGN_BRIEF.md",
    "00-foundation/DESIGN_PRINCIPLES.md"
  ]
  phases.design_brief.validation = {
    status: "passed"
  }
  phases.design_brief.metrics = {
    pain_points_addressed: count,
    principles_defined: 7
  }
```

---

## Output Files (REQUIRED)

| Path | Purpose | Blocking? |
|------|---------|-----------|
| `DESIGN_BRIEF.md` | Visual direction, strategy | ✅ Yes |
| `DESIGN_PRINCIPLES.md` | UX/UI guiding principles | ✅ Yes |

---

## Progress.json Update

```json
{
  "phases": {
    "design_brief": {
      "status": "complete",
      "completed_at": "2024-12-13T10:15:00Z",
      "outputs": [
        "00-foundation/DESIGN_BRIEF.md",
        "00-foundation/DESIGN_PRINCIPLES.md"
      ],
      "validation": {
        "status": "passed"
      },
      "metrics": {
        "pain_points_addressed": 8,
        "principles_defined": 7
      }
    }
  }
}
```
