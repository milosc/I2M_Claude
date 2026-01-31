---
description: Process feedback on Solution Architecture with reflexion-enhanced ADR consistency and component alignment validation
argument-hint: [feedback-text] | --feedback-id <ID> | resume <ID> | status | list
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Skill
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-feedback started '{"stage": "solarch"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /solarch-feedback ended '{"stage": "solarch"}'
---

# /solarch-feedback - Process Solution Architecture Feedback

**Version**: 2.0.0 (Reflexion-Enhanced)
**Stage**: Solution Architecture (Stage 4)
**Last Updated**: 2026-01-25

---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "solarch"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /solarch-feedback instruction_start '{"stage": "solarch", "method": "instruction-based"}'
```

---

## Overview

This command provides a **reflexion-enhanced workflow** for processing feedback and change requests on Solution Architecture artifacts (ADRs, components, C4 diagrams, quality scenarios). It integrates critical self-assessment, hierarchical traceability visualization, and ADR consistency validation.

### What's New in v2.0.0

1. **Reflexion Integration**: Critical self-assessment at Impact Analysis, Planning, and Validation phases
2. **AskUserQuestion Integration**: Structured decision prompts at all gates
3. **Hierarchical Chain Visualization**: Tree-structured traceability with before/after content (PP → JTBD → REQ → ADR → Components)
4. **ADR Consistency Checking**: Validate cross-ADR references and decision alignments
5. **Confidence Scoring**: Weighted scoring (40% completeness + 35% accuracy + 25% downstream) producing LOW/MEDIUM/HIGH
6. **Before/After Content Specification**: Exact content snippets for every change
7. **Component Alignment Validation**: Ensure components match ADR decisions
8. **C4 Diagram Impact Assessment**: Track diagram regeneration needs

---

## Arguments

- `$ARGUMENTS` - Optional: `[feedback_text | file.md | resume SF-NNN | status | list]`

## Usage

| Command | Description |
|---------|-------------|
| `/solarch-feedback` | Interactive mode - prompts for feedback |
| `/solarch-feedback "<text>"` | Process inline feedback text |
| `/solarch-feedback <file.md>` | Process feedback from file |
| `/solarch-feedback resume SF-NNN` | Resume failed/partial implementation |
| `/solarch-feedback validate SF-NNN` | Run validation on implemented feedback |
| `/solarch-feedback status` | Show current feedback processing status |
| `/solarch-feedback list` | List all registered feedback items |

---

## Prerequisites

1. **SolArch Completion**: Solution Architecture at least checkpoint 3 completed
2. **Folder Structure**: `SolArch_<SystemName>/` folder exists with:
   - `09-decisions/*.md` (ADR files)
   - `05-building-blocks/` (Component definitions)
   - `06-runtime-view/` (C4 diagrams)
   - `07-quality/` (Quality scenarios)
   - `_registry/*.json` (Registries)
   - `traceability/*.json` (Traceability chains)

---

## Skills Used

These skills are invoked automatically during workflow execution:

1. **Shared_FeedbackImpactAnalyzer_Reflexion**: Phase 2 - Impact analysis with critical self-assessment
2. **Shared_FeedbackPlanGenerator_Reflexion**: Phase 5 - Plan generation with X/10 scoring
3. **Shared_FeedbackReviewer_Reflexion**: Phase 7 - Multi-perspective validation

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│             SOLARCH FEEDBACK WORKFLOW (v2.0.0)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: Input Collection                                      │
│  ├── Receive feedback (text/file)                              │
│  ├── Identify target SolArch                                   │
│  └── Collect metadata (source, date, priority)                 │
│                                                                 │
│  Phase 2: Impact Analysis (REFLEXION)                           │
│  ├── Scan ADRs, components, diagrams, quality scenarios       │
│  ├── Trace hierarchical chains (PP → JTBD → REQ → ADR → COMP) │
│  ├── Check ADR consistency and cross-references               │
│  ├── Assess component alignment with decisions                 │
│  ├── Determine C4 diagram regeneration needs                   │
│  ├── Generate before/after content previews                    │
│  └── Self-Critique: Completeness, Accuracy, Downstream         │
│      → Confidence Level: HIGH (85%+) | MEDIUM (60-84%) | LOW (<60%) │
│                                                                 │
│  Phase 3: Registration                                          │
│  ├── Assign unique ID (SF-NNN)                                 │
│  ├── Create session folder                                     │
│  ├── Save FEEDBACK_ORIGINAL.md, impact_analysis.md            │
│  └── Log to solarch_feedback_registry.json                    │
│                                                                 │
│  Phase 4: Approval Gate (ASKUSERQUESTION)                       │
│  ├── Present impact summary with reflexion context            │
│  ├── Show ADR consistency impacts                              │
│  ├── Show component alignment impacts                          │
│  ├── Show C4 diagram regeneration needs                        │
│  └── Options: Approve | Reject | Modify Scope | Request Deeper Analysis │
│                                                                 │
│  Phase 5: Implementation Planning (REFLEXION)                   │
│  ├── Generate 2-3 plan options with scoring                   │
│  ├── Each option: Steps, Effort, Risk, ADR Impact, X/10 score │
│  └── User selects via AskUserQuestion                          │
│                                                                 │
│  Phase 6: Implementation                                        │
│  ├── Execute plan steps sequentially                           │
│  ├── Update ADRs, components, diagrams                         │
│  ├── Update registries (decisions.json, components.json)      │
│  ├── Handle partial failures (resumable checkpoints)          │
│  └── Log all changes to implementation_log.md                 │
│                                                                 │
│  Phase 7: Validation (REFLEXION)                                │
│  ├── Verify plan compliance (100% steps executed)             │
│  ├── Check ADR consistency (no conflicting decisions)         │
│  ├── Validate component alignment (components match ADRs)     │
│  ├── Validate traceability chains (all intact)                │
│  └── Multi-Perspective Review: Requirements, Architecture, Quality │
│      → Consensus Score: 0-10 (PASS ≥ 7.0)                      │
│                                                                 │
│  Phase 8: Completion                                            │
│  ├── Generate FEEDBACK_SUMMARY.md                             │
│  ├── Update registry status → "closed"                         │
│  └── Display completion summary with confidence metrics        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase-by-Phase Procedures

### Phase 1: Input Collection

```bash
# Parse arguments
IF $ARGUMENTS contains "resume":
   GOTO Resume Mode (see Resume Capability section)

IF $ARGUMENTS contains "status":
   GOTO Status Mode (see Status Mode section)

IF $ARGUMENTS contains "list":
   GOTO List Mode (see List Mode section)

# Input source detection
IF feedback provided as inline text:
   feedback_content = $ARGUMENTS
   source = "inline"

ELIF feedback provided as file path:
   READ file at $ARGUMENTS
   feedback_content = file_contents
   source = file_path

ELSE:
   # Interactive mode
   PROMPT: "Please describe your feedback or change request:"
   feedback_content = user_input
   source = "interactive"

# Metadata collection via AskUserQuestion
USE AskUserQuestion:
   question: "What is the source of this feedback?"
   header: "Source"
   multiSelect: false
   options:
     - label: "Architecture Review"
       description: "Feedback from architecture review board"
     - label: "Technical Lead"
       description: "Feedback from tech lead or senior engineer"
     - label: "Security Team"
       description: "Feedback from security review"
     - label: "Stakeholder"
       description: "Feedback from business stakeholders"
     - label: "External Consultant"
       description: "Feedback from external architecture consultant"

STORE feedback_source

USE AskUserQuestion:
   question: "What is the priority level for this feedback?"
   header: "Priority"
   multiSelect: false
   options:
     - label: "Critical (Recommended for Blockers)"
       description: "Blocking architectural issue - must fix immediately"
     - label: "High"
       description: "Important architectural concern - should address soon"
     - label: "Medium (Recommended for Enhancements)"
       description: "Moderate importance - address in current iteration"
     - label: "Low"
       description: "Nice-to-have - can defer if needed"

STORE feedback_priority

# Identify target SolArch
SEARCH for SolArch_* folders in project root

IF no SolArch folders found:
   ❌ ERROR: "No Solution Architecture found. Run /solarch first."
   EXIT

IF multiple SolArch folders found:
   USE AskUserQuestion:
      question: "Multiple architectures found. Which system does this feedback apply to?"
      header: "System"
      multiSelect: false
      options: [List each SolArch_* as option]

   STORE selected_system
ELSE:
   selected_system = single SolArch folder

SET SOLARCH_DIR = "SolArch_{selected_system}/"
EXTRACT system_name from folder name
```

---

### Phase 2: Impact Analysis (REFLEXION)

**Purpose**: Identify all affected artifacts across SolArch layers with ADR consistency and component alignment validation.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 2: IMPACT ANALYSIS (REFLEXION-ENHANCED)
═══════════════════════════════════════════════════════════════

STEP 1: INVOKE SHARED IMPACT ANALYZER

Skill({
  skill: "Shared_FeedbackImpactAnalyzer_Reflexion",
  args: JSON.stringify({
    feedback_content: feedback_content,
    stage: "solarch",
    system_name: system_name,
    stage_folder: SOLARCH_DIR
  })
})

# The skill performs:
# 1. Parse feedback for artifact mentions (ADR-XXX, COMP-XXX, QS-XXX)
# 2. Scan all SolArch artifacts:
#    - 09-decisions/ADR-*.md (Architecture Decision Records)
#    - 05-building-blocks/*.md (Component definitions)
#    - 06-runtime-view/*.mmd (C4 diagrams)
#    - 07-quality/*.md (Quality scenarios)
#    - _registry/decisions.json, components.json
#    - traceability/solarch_traceability_register.json
# 3. Match feedback to artifacts (exact ID, title similarity, keyword match)
# 4. Trace traceability chains:
#    - Backwards: ADR → REQ → JTBD → PP
#    - Forwards: ADR → Components → Quality Scenarios
# 5. Build hierarchical chains with before/after content
# 6. Check ADR consistency (cross-ADR references, decision conflicts)
# 7. Assess component alignment (components match ADR decisions)
# 8. Determine C4 diagram regeneration needs
# 9. Reflexion self-critique (Completeness, Accuracy, Downstream)
# 10. Calculate confidence score (0-100%)

READ impact_analysis.md output from skill

EXTRACT from impact_analysis.md:
- chains_affected (number)
- artifacts_affected (number)
- change_types (CREATE, MODIFY, DELETE counts)
- confidence_level (HIGH, MEDIUM, LOW)
- confidence_percentage (0-100)
- adr_consistency_issues (list)
- component_alignment_issues (list)
- c4_diagram_regeneration_required (boolean)
- diagrams_affected (list)
- reflexion_warnings (list)
- reflexion_recommendations (list)

STEP 2: GENERATE 5-LAYER IMPACT SUMMARY

## 5-Layer Impact Summary

| Layer | Artifacts Affected | Details |
|-------|-------------------|---------|
| 1. ADRs | {X} | {ADR-XXX files in 09-decisions/} |
| 2. Components | {Y} | {Component definitions in 05-building-blocks/} |
| 3. Diagrams | {Z} | {C4 diagrams in 06-runtime-view/ (regeneration: YES/NO)} |
| 4. Quality Scenarios | {Q} | {Quality scenarios in 07-quality/} |
| 5. Registries | {R} | {decisions.json, components.json, traceability registers} |
| **TOTAL** | **{N}** | - |

STEP 3: DISPLAY HIERARCHICAL CHAINS

For each chain in impact_analysis.md:

### Chain N: ROOT → NODE1 → NODE2 → ... → LEAF

├─ **{ARTIFACT_ID}**: "{Title}"
│  └─ Change: {CREATE|MODIFY|DELETE} - {Description}
│     File: {file_path}:{line_range}
│     Before:
│     ```
│     {content_snippet_before}
│     ```
│     After:
│     ```
│     {expected_content_after}
│     ```
│     Reasoning: {Why this change addresses feedback}
│     Complexity: {SIMPLE|MODERATE|COMPLEX}
│     ADR Impact: {If modifying ADR, note decision consistency implications}
│
├─ **{NEXT_ARTIFACT_ID}**: "{Title}"
│  └─ Change: ...
│
└─ **{LEAF_ARTIFACT_ID}**: "{Title}"
   └─ Change: ...

STEP 4: ADR CONSISTENCY ASSESSMENT

IF adr_consistency_issues found:

   ═══════════════════════════════════════════════════════════════
   🔗 ADR CONSISTENCY IMPACT
   ═══════════════════════════════════════════════════════════════

   Affected ADRs: {adr_count}

   Consistency Issues:
   {For each issue:}
   ├─ ADR-XXX ↔ ADR-YYY
   │  └─ Conflict: {description of decision conflict}
   │     Current State: {current decision in ADR-XXX}
   │     Proposed Change: {how feedback changes decision}
   │     Impact on ADR-YYY: {how ADR-YYY must change to maintain consistency}
   │     Resolution Strategy: {proposed approach to resolve conflict}

   Cross-References to Update:
   {List ADRs that reference affected ADRs}

   Risk Assessment:
   - Decision conflicts: {YES/NO} - {Details}
   - Superseded decisions: {YES/NO} - {Details}
   - Missing justifications: {YES/NO} - {Details}

   ═══════════════════════════════════════════════════════════════

STEP 5: COMPONENT ALIGNMENT ASSESSMENT

IF component_alignment_issues found:

   ═══════════════════════════════════════════════════════════════
   🧩 COMPONENT ALIGNMENT IMPACT
   ═══════════════════════════════════════════════════════════════

   Affected Components: {component_count}

   Alignment Issues:
   {For each issue:}
   ├─ COMP-XXX: "{Component Name}"
   │  └─ Alignment Gap: {description}
   │     ADR Decision: {decision from ADR}
   │     Component Implementation: {current component design}
   │     Required Change: {how component must change to align with ADR}
   │     Rationale: {why alignment is necessary}

   Components Requiring Updates:
   - COMP-XXX: {description}
   - COMP-YYY: {description}

   Risk Assessment:
   - Architecture violations: {YES/NO} - {Details}
   - Component refactoring needed: {YES/NO} - {Details}

   ═══════════════════════════════════════════════════════════════

STEP 6: C4 DIAGRAM REGENERATION ASSESSMENT

IF c4_diagram_regeneration_required == true:

   ═══════════════════════════════════════════════════════════════
   📊 C4 DIAGRAM REGENERATION IMPACT
   ═══════════════════════════════════════════════════════════════

   Affected Diagrams: {diagram_count}

   Diagrams to Regenerate:
   - 06-runtime-view/c4-context.mmd ({level 1 - System context})
   - 06-runtime-view/c4-container.mmd ({level 2 - Containers})
   - 06-runtime-view/c4-component-{xxx}.mmd ({level 3 - Components})

   Regeneration Scope:
   - Full: All diagrams regenerated from updated component definitions
   - Partial: Only affected container/component diagrams regenerated

   Timeline Impact: {estimate based on diagram_count}
   - < 3 diagrams: Low (< 5 minutes)
   - 3-6 diagrams: Medium (5-10 minutes)
   - > 6 diagrams: High (10+ minutes)

   Risk Assessment:
   - Diagram consistency: {YES/NO} - {Will diagrams match new ADR decisions}
   - Manual adjustments needed: {YES/NO} - {Details}

   ═══════════════════════════════════════════════════════════════

STEP 7: DISPLAY REFLEXION CRITIQUE

READ reflexion section from impact_analysis.md

DISPLAY:

═══════════════════════════════════════════════════════════════
🤔 REFLEXION SELF-CRITIQUE
═══════════════════════════════════════════════════════════════

Completeness Check: {✓ Complete | ⚠ Possibly incomplete | ❌ Gaps found}
Reasoning: {detailed reasoning from reflexion}
Missing: {list any potentially missed artifacts}

Accuracy Check: {✓ Accurate | ⚠ Minor issues | ❌ Major issues}
Reasoning: {detailed reasoning from reflexion}
Issues: {list any inaccuracies}

Downstream Impact: {✓ All impacts identified | ⚠ Possible additional | ❌ Missed major impacts}
Reasoning: {detailed reasoning from reflexion}
Additional: {list any additional impacts}

Risk Assessment:
- Traceability chain breaks: {Y/N} - {Details}
- ADR consistency risk: {LOW|MEDIUM|HIGH} - {Why}
- Component alignment risk: {LOW|MEDIUM|HIGH} - {Why}
- Diagram sync risk: {LOW|MEDIUM|HIGH} - {Why}
- Timeline impact: {None|Sprint|Release} - {Reasoning}
- Breaking changes: {Y/N} - {What breaks}

SEVERITY: {CRITICAL|HIGH|MEDIUM|LOW}
MITIGATION: {Recommended mitigations}

Confidence Level: {HIGH|MEDIUM|LOW} ({percentage}%)
Reasoning: {Detailed explanation of confidence level}

Warnings:
{List each warning from reflexion}

Recommendations:
{List each recommendation from reflexion}

═══════════════════════════════════════════════════════════════

PROCEED to Phase 3: Registration
```

**Example Output (Phase 2)**:

```markdown
═══════════════════════════════════════════════════════════════
⏳ PHASE 2: IMPACT ANALYSIS (REFLEXION-ENHANCED)
═══════════════════════════════════════════════════════════════

## 5-Layer Impact Summary

| Layer | Artifacts Affected | Details |
|-------|-------------------|---------|
| 1. ADRs | 2 | ADR-001 (Architecture Style), ADR-003 (Data Storage) |
| 2. Components | 3 | COMP-CORE (Core Services), COMP-DATA (Data Layer), COMP-API (API Gateway) |
| 3. Diagrams | 4 | c4-context.mmd, c4-container.mmd, c4-component-core.mmd, c4-component-data.mmd (regeneration: YES) |
| 4. Quality Scenarios | 2 | QS-PERF-001 (Response Time), QS-SCALE-002 (Horizontal Scaling) |
| 5. Registries | 2 | decisions.json, components.json |
| **TOTAL** | **13** | - |

## Hierarchical Traceability Chains Affected

### Chain 1: PP-1.1 → JTBD-2.1 → REQ-015 → ADR-001 → COMP-CORE

├─ **ADR-001**: "Architecture Style - Monolithic vs Microservices"
│  └─ Change: MODIFY - Strengthen justification for monolith choice with scaling analysis
│     File: 09-decisions/ADR-001-architecture-style.md:15-45
│     Before:
│     ```markdown
│     ## Context
│
│     The system needs an architectural approach. We considered:
│     - Monolithic architecture
│     - Microservices architecture
│
│     ## Decision
│
│     We will use a modular monolithic architecture.
│
│     ## Consequences
│
│     **Positive:**
│     - Simpler deployment
│     - Easier development
│
│     **Negative:**
│     - Limited scalability
│     ```
│     After:
│     ```markdown
│     ## Context
│
│     The system needs an architectural approach that balances current team capabilities
│     with future scaling needs (projected 10x growth over 3 years).
│
│     We analyzed:
│     - **Monolithic architecture**: Single deployable unit, shared data model
│     - **Microservices architecture**: Distributed services, independent scaling
│
│     Key factors influencing decision:
│     - Team size: 5 developers (limited microservices expertise)
│     - Expected load: 10K users initially, 100K in 3 years
│     - Operational complexity budget: Medium
│
│     ## Decision
│
│     We will use a **modular monolithic architecture** with **future microservices extraction plan**.
│
│     Rationale:
│     1. Matches current team capabilities (no microservices experience)
│     2. Adequate for projected 3-year load (100K users achievable with vertical scaling)
│     3. Lower operational overhead (single deployment pipeline, shared monitoring)
│     4. Modules designed with bounded contexts for future extraction if needed
│
│     ## Consequences
│
│     **Positive:**
│     - Simpler deployment (single application, no service mesh)
│     - Easier development (shared codebase, no distributed debugging)
│     - Lower infrastructure cost (single server tier initially)
│     - Faster feature delivery (no cross-service coordination)
│
│     **Negative:**
│     - **Scaling limitations**: Vertical scaling only (max ~100K concurrent users)
│     - **Deployment coupling**: All modules deploy together (longer deployment windows)
│     - **Technology coupling**: Single technology stack for all modules
│
│     **Future Evolution Path:**
│     If load exceeds 100K users or specific modules become bottlenecks:
│     1. Extract high-traffic modules to separate services (e.g., Search, Notifications)
│     2. Maintain monolith for core business logic
│     3. See ADR-XXX (future) for microservices extraction strategy
│     ```
│     Reasoning: Feedback explicitly requested stronger justification for monolith vs microservices,
│                especially for scaling. Added load analysis, team capability assessment, and
│                future evolution path.
│     Complexity: COMPLEX
│     ADR Impact: Must update ADR-003 (Data Storage) to align with scaling limitations
│
├─ **ADR-003**: "Data Storage - Single Database vs Multiple Databases"
│  └─ Change: MODIFY - Add reference to ADR-001 scaling limitations, note future sharding plan
│     File: 09-decisions/ADR-003-data-storage.md:25-35
│     Before:
│     ```markdown
│     ## Decision
│
│     We will use a single PostgreSQL database for all data storage.
│     ```
│     After:
│     ```markdown
│     ## Decision
│
│     We will use a single PostgreSQL database for all data storage, with future sharding plan
│     if load exceeds ADR-001 scaling threshold (100K users).
│
│     This aligns with ADR-001 (Modular Monolith) and supports vertical scaling to 100K users.
│     If future microservices extraction occurs (see ADR-001 evolution path), database will be
│     partitioned accordingly.
│     ```
│     Reasoning: ADR consistency - ADR-003 must reference ADR-001's scaling limitations
│     Complexity: MODERATE
│
├─ **COMP-CORE**: "Core Services Component"
│  └─ Change: MODIFY - Update component rationale to reference ADR-001's bounded context design
│     File: 05-building-blocks/COMP-CORE.md:10-15
│     Before:
│     ```markdown
│     Rationale: Core business logic centralized for simplicity.
│     ```
│     After:
│     ```markdown
│     Rationale: Core business logic centralized per ADR-001 (Modular Monolith).
│                Designed with bounded contexts for potential future extraction
│                if scaling needs exceed monolith capacity (see ADR-001 evolution path).
│     ```
│     Reasoning: Component alignment - component must reference ADR decision
│
└─ (Additional components COMP-DATA, COMP-API similarly updated)

### Chain 2: REQ-020 → ADR-003 → COMP-DATA → QS-PERF-001

(Similar structure for Chain 2...)

═══════════════════════════════════════════════════════════════
🔗 ADR CONSISTENCY IMPACT
═══════════════════════════════════════════════════════════════

Affected ADRs: 2

Consistency Issues:
├─ ADR-001 ↔ ADR-003
│  └─ Conflict: ADR-003 (Single Database) doesn't mention ADR-001's scaling limitations
│     Current State: ADR-003 states "single database for all data" without qualification
│     Proposed Change: ADR-001 now specifies "adequate for 100K users, vertical scaling only"
│     Impact on ADR-003: Must add reference to ADR-001's 100K user threshold and future sharding plan
│     Resolution Strategy: Add cross-reference in ADR-003 Decision section + note future partitioning

Cross-References to Update:
- ADR-007 (Caching Strategy): References ADR-001, may need updated scaling context
- ADR-010 (Deployment Strategy): References monolith deployment, already consistent

Risk Assessment:
- Decision conflicts: NO - Changes strengthen consistency, don't conflict
- Superseded decisions: NO - Monolith decision still valid, just better justified
- Missing justifications: RESOLVED - Feedback addressed missing scaling justification

═══════════════════════════════════════════════════════════════
🧩 COMPONENT ALIGNMENT IMPACT
═══════════════════════════════════════════════════════════════

Affected Components: 3

Alignment Issues:
├─ COMP-CORE: "Core Services Component"
│  └─ Alignment Gap: Rationale doesn't reference ADR-001's bounded context design
│     ADR Decision: "Modules designed with bounded contexts for future extraction"
│     Component Implementation: "Core business logic centralized for simplicity"
│     Required Change: Update rationale to mention bounded contexts per ADR-001
│     Rationale: Ensures component documentation aligns with architectural decision
│
├─ COMP-DATA: "Data Layer Component"
│  └─ Alignment Gap: Design doesn't mention ADR-003's future sharding plan
│     ADR Decision: "Future sharding plan if load exceeds 100K users"
│     Component Implementation: "Single database access layer"
│     Required Change: Add note about future partitioning capability
│     Rationale: Prepares component for future scaling evolution
│
└─ COMP-API: "API Gateway Component"
   └─ Alignment Gap: Minor - API design mentions microservices readiness but ADR-001 now specifies extraction plan
      ADR Decision: "Future extraction of high-traffic modules if needed"
      Component Implementation: "API designed for future service decomposition"
      Required Change: Update to reference specific ADR-001 extraction strategy
      Rationale: Maintains consistency with updated ADR

Components Requiring Updates:
- COMP-CORE: Update rationale section (bounded contexts)
- COMP-DATA: Add future evolution note (sharding plan)
- COMP-API: Align service decomposition strategy with ADR-001

Risk Assessment:
- Architecture violations: NO - Components already follow monolith pattern
- Component refactoring needed: NO - Only documentation updates required

═══════════════════════════════════════════════════════════════
📊 C4 DIAGRAM REGENERATION IMPACT
═══════════════════════════════════════════════════════════════

Affected Diagrams: 4

Diagrams to Regenerate:
- 06-runtime-view/c4-context.mmd (Level 1 - System context: No changes needed, external view unchanged)
- 06-runtime-view/c4-container.mmd (Level 2 - Containers: Update annotations with scaling context)
- 06-runtime-view/c4-component-core.mmd (Level 3 - Core component internal structure)
- 06-runtime-view/c4-component-data.mmd (Level 3 - Data component internal structure)

Regeneration Scope: Partial (3 diagrams - skip c4-context.mmd)

Timeline Impact: Medium (5-8 minutes)

Changes Required:
1. **c4-container.mmd**: Add annotations about vertical scaling capability (100K user threshold)
2. **c4-component-core.mmd**: Add bounded context boundaries within Core Services container
3. **c4-component-data.mmd**: Add note about future sharding capability

Risk Assessment:
- Diagram consistency: YES - All diagrams will match updated ADR decisions
- Manual adjustments needed: NO - Automated regeneration sufficient

═══════════════════════════════════════════════════════════════
🤔 REFLEXION SELF-CRITIQUE
═══════════════════════════════════════════════════════════════

Completeness Check: ✓ COMPLETE

Re-scanned with terms: ["monolith", "microservices", "scaling", "architecture style", "modular"]
- Found all primary references (ADR-001, ADR-003, COMP-CORE, COMP-DATA, COMP-API)
- Checked for orphaned ADR references: Found ADR-007, ADR-010 (cross-checked, no updates needed)
- Verified all traceability chains complete (2 chains, 13 artifacts total)

Reasoning: Comprehensive scan found all artifacts directly and indirectly affected by ADR-001 enhancement.
          No orphaned references detected. ADR cross-reference analysis complete.

Accuracy Check: ✓ ACCURATE

- All MODIFY artifacts verified to exist at specified paths
- Before/after content matches current file states
- ADR frontmatter format compliance verified (status, date, supersedes fields)
- Component definition format compliance verified

Reasoning: All artifact paths validated. Content snippets match current files. Proposed changes maintain
          ADR and component specification formats. ADR consistency checks passed.

Downstream Impact: ⚠ POSSIBLE ADDITIONAL

Checked downstream:
- Components: Existing (3 require documentation updates)
- C4 Diagrams: Existing (3 require regeneration)
- Quality Scenarios: Existing (2 may need updated performance targets)

**Potential additional impacts**:
- Implementation stage tasks may reference ADR-001 and need context updates
- Performance testing plans may need updated targets (100K user threshold)
- Capacity planning documentation may need scaling timeline updates

Reasoning: While primary architectural artifacts identified, downstream implementation materials
          (task descriptions, test plans, capacity docs) may need updates. Flagged for consideration
          during planning.

Risk Assessment:
- **Traceability chain breaks**: NO - All chains remain intact after changes
- **ADR consistency risk**: LOW - Changes strengthen consistency, resolve existing gaps
- **Component alignment risk**: LOW - Documentation updates only, no design changes
- **Diagram sync risk**: LOW - Automated regeneration handles all updates
- **Timeline impact**: Sprint-level - Moderate effort, can fit in current sprint
- **Breaking changes**: NO - Additive enhancements to existing decisions

**SEVERITY**: MEDIUM (Documentation enhancement, no design changes)
**MITIGATION**:
- Review implementation tasks for ADR-001 references during planning
- Update performance test targets to reflect 100K user threshold
- Schedule architecture review session to present strengthened justifications

Confidence Level: HIGH (90%)

Reasoning:
- Completeness: Thorough multi-pass scan found all direct and indirect impacts (✓) → +40 points
- Accuracy: All artifact paths validated, content verified, format checked (✓) → +35 points
- Downstream: Primary impacts identified, secondary impacts flagged (⚠) → +15 points
- Total: 90 points

Warnings:
- Implementation tasks may reference ADR-001 - check during validation
- Performance testing targets may need updates for 100K user threshold
- Capacity planning timeline may need adjustment

Recommendations:
1. During planning, review all implementation tasks referencing ADR-001
2. Update performance test suite with 100K user load tests
3. Schedule architecture review to present enhanced justifications to stakeholders
4. Consider documenting microservices extraction criteria in new ADR (future)

═══════════════════════════════════════════════════════════════
```

---

### Phase 3: Registration

**Purpose**: Assign unique ID and create session folder structure.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 3: REGISTRATION
═══════════════════════════════════════════════════════════════

STEP 1: GENERATE FEEDBACK ID

READ {SOLARCH_DIR}/feedback-sessions/solarch_feedback_registry.json

IF file does not exist:
   CREATE empty registry:
   {
     "schema_version": "2.0.0",
     "system_name": "{system_name}",
     "stage": "solarch",
     "feedback_items": {}
   }

EXTRACT existing IDs (SF-001, SF-002, ...)
GENERATE next_id = SF-{max_id + 1} (zero-padded to 3 digits)

STEP 2: CREATE SESSION FOLDER

SET session_date = YYYY-MM-DD
SET session_folder = "{SOLARCH_DIR}/feedback-sessions/{session_date}_SolArchFeedback-{next_id}/"

CREATE session_folder

STEP 3: SAVE ARTIFACTS

WRITE {session_folder}/FEEDBACK_ORIGINAL.md:
---
feedback_id: {next_id}
created_at: {ISO8601 timestamp}
source: {feedback_source}
priority: {feedback_priority}
---

# Original Feedback - {next_id}

{feedback_content}

COPY impact_analysis.md from Shared_FeedbackImpactAnalyzer_Reflexion output
  TO {session_folder}/impact_analysis.md

STEP 4: UPDATE REGISTRY

ADD to solarch_feedback_registry.json:

{
  "feedback_items": {
    "{next_id}": {
      "title": "{brief_summary_from_feedback}",
      "type": "{ADREnhancement|ComponentChange|DiagramUpdate|QualityScenario|TraceabilityGap}",
      "severity": "{Critical|High|Medium|Low}",
      "status": "analyzing",
      "source": {
        "origin": "{feedback_source}",
        "priority": "{feedback_priority}",
        "submitted_by": "{source person if available}",
        "submitted_at": "{ISO8601 timestamp}"
      },
      "categories": ["{CAT-ADR}", "{CAT-COMP}", ...],
      "impact": {
        "chains_affected": {chains_affected},
        "artifacts_affected": {artifacts_affected},
        "layer_1_adrs": {X},
        "layer_2_components": {Y},
        "layer_3_diagrams": {Z},
        "layer_4_quality": {Q},
        "layer_5_registries": {R},
        "adr_consistency_issues": {count},
        "component_alignment_issues": {count},
        "c4_regeneration_required": {true|false},
        "diagrams_affected": {count},
        "confidence_level": "{HIGH|MEDIUM|LOW}",
        "confidence_percentage": {0-100},
        "reflexion_score": {confidence_percentage}
      },
      "lifecycle": {
        "created_at": "{ISO8601}",
        "updated_at": "{ISO8601}",
        "phase": "registration",
        "session_folder": "{session_folder}"
      }
    }
  }
}

✅ Registration complete: {next_id}
   Session folder: {session_folder}

PROCEED to Phase 4: Approval Gate
```

---

### Phase 4: Approval Gate (ASKUSERQUESTION)

**Purpose**: Present impact analysis with reflexion context and get user approval.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 4: APPROVAL GATE
═══════════════════════════════════════════════════════════════

STEP 1: PREPARE APPROVAL CONTEXT

READ impact_analysis.md from session folder
EXTRACT:
- impact_summary (artifact counts, layer breakdown)
- reflexion_context (confidence level, warnings, recommendations)
- risk_context (severity, ADR consistency, component alignment)
- adr_consistency_impact (consistency issues, cross-references)
- component_alignment_impact (alignment issues, required changes)
- c4_diagram_impact (regeneration needed, diagrams affected, timeline)

STEP 2: PRESENT TO USER VIA ASKUSERQUESTION

USE AskUserQuestion:
   question: "
   ═══════════════════════════════════════════════════════════════
   FEEDBACK IMPACT ANALYSIS: {next_id}
   ═══════════════════════════════════════════════════════════════

   {impact_summary}

   {adr_consistency_impact}

   {component_alignment_impact}

   {c4_diagram_impact}

   {reflexion_context}

   {risk_context}

   ═══════════════════════════════════════════════════════════════

   Review the detailed impact analysis above. How should we proceed?"

   header: "Approval"
   multiSelect: false
   options:
     - label: "Approve (Recommended)"
       description: "Proceed to implementation planning. C4 diagram regeneration timeline: {estimate}. ADR consistency and component alignment will be validated. Effort will be calculated during option generation with reflexion scoring."
     - label: "Reject"
       description: "Mark feedback as rejected. No changes will be made to architecture. Requires rejection reason."
     - label: "Modify Scope"
       description: "Adjust which artifacts/layers to change before proceeding to planning. Allows selective implementation (e.g., skip diagram regeneration, focus on ADR updates only)."
     - label: "Request Deeper Analysis"
       description: "Reflexion confidence is {confidence_level} ({confidence_percentage}%) - request more investigation before deciding. Recommended if confidence < 85% or critical ADR consistency issues exist."

STORE user_decision

STEP 3: PROCESS DECISION

IF user_decision == "Approve":
   UPDATE registry:
      status = "approved"
      lifecycle.phase = "approval_gate"
      lifecycle.updated_at = NOW()

   ✅ Feedback approved for implementation
   PROCEED to Phase 5: Implementation Planning

ELIF user_decision == "Reject":
   PROMPT: "Please provide a rejection reason:"
   rejection_reason = user_input

   UPDATE registry:
      status = "rejected"
      lifecycle.phase = "approval_gate"
      lifecycle.rejection_reason = rejection_reason
      lifecycle.updated_at = NOW()
      lifecycle.closed_at = NOW()

   WRITE {session_folder}/REJECTION_REASON.md:
   ---
   feedback_id: {next_id}
   rejected_at: {ISO8601}
   rejected_by: User
   ---

   # Rejection Reason

   {rejection_reason}

   ❌ Feedback rejected: {next_id}
   EXIT

ELIF user_decision == "Modify Scope":
   USE AskUserQuestion:
      question: "Which layers should be modified?"
      header: "Scope"
      multiSelect: true
      options:
        - label: "ADRs (Layer 1)"
          description: "Modify Architecture Decision Records (09-decisions/)"
        - label: "Components (Layer 2)"
          description: "Modify component definitions (05-building-blocks/)"
        - label: "C4 Diagrams (Layer 3)"
          description: "Regenerate C4 diagrams (06-runtime-view/)"
        - label: "Quality Scenarios (Layer 4)"
          description: "Modify quality scenarios (07-quality/)"
        - label: "Registries (Layer 5)"
          description: "Update registries (decisions.json, components.json)"

   STORE selected_layers

   # Filter artifacts by selected layers
   FILTER impact_analysis artifacts by selected_layers
   UPDATE registry with filtered scope

   ✅ Scope modified - proceeding with selected layers only
   PROCEED to Phase 5: Implementation Planning

ELIF user_decision == "Request Deeper Analysis":
   PROMPT: "What specific areas should be investigated further?"
   investigation_areas = user_input

   UPDATE registry:
      status = "investigating"
      lifecycle.investigation_request = investigation_areas
      lifecycle.updated_at = NOW()

   # Re-run impact analyzer with focused investigation
   Skill({
     skill: "Shared_FeedbackImpactAnalyzer_Reflexion",
     args: JSON.stringify({
       feedback_content: feedback_content,
       stage: "solarch",
       system_name: system_name,
       stage_folder: SOLARCH_DIR,
       investigation_focus: investigation_areas
     })
   })

   ⚠️ Deeper analysis requested - re-running impact analyzer
   GOTO Phase 2 (with investigation focus)
```

---

### Phase 5: Implementation Planning (REFLEXION)

**Purpose**: Generate multiple implementation options with X/10 scoring and get user selection.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 5: IMPLEMENTATION PLANNING (REFLEXION-ENHANCED)
═══════════════════════════════════════════════════════════════

STEP 1: INVOKE SHARED PLAN GENERATOR

Skill({
  skill: "Shared_FeedbackPlanGenerator_Reflexion",
  args: JSON.stringify({
    feedback_id: next_id,
    stage: "solarch",
    system_name: system_name,
    impact_analysis_path: "{session_folder}/impact_analysis.md",
    session_folder: session_folder
  })
})

# The skill performs:
# 1. Read impact_analysis.md and affected artifacts
# 2. Generate 2-3 implementation options:
#    - Option A: Comprehensive (all layers, full ADR consistency, C4 regeneration)
#    - Option B: Focused (ADR updates only, minimal component changes)
#    - Option C: Custom (user-defined)
# 3. For each option:
#    - Define steps with specific file operations
#    - Estimate effort (LOW, MEDIUM, HIGH)
#    - Assess risk (LOW, MEDIUM, HIGH)
#    - Calculate ADR consistency impact
#    - Calculate component alignment impact
#    - Calculate C4 diagram regeneration scope
#    - Specify before/after content for key changes
#    - Score with reflexion (X/10 based on completeness, correctness, risk)
# 4. Recommend best option based on scoring
# 5. Save to implementation_options.md

READ implementation_options.md output from skill

STEP 2: PRESENT OPTIONS VIA ASKUSERQUESTION

DISPLAY implementation_options.md content to user

USE AskUserQuestion:
   question: "
   ═══════════════════════════════════════════════════════════════
   IMPLEMENTATION OPTIONS FOR {next_id}
   ═══════════════════════════════════════════════════════════════

   {Display full implementation_options.md content here}

   ═══════════════════════════════════════════════════════════════

   Which implementation plan should we use for this architecture change?"

   header: "Plan"
   multiSelect: false
   options:
     - label: "Plan A: Comprehensive Update (Recommended)" (if score >= 8/10)
       description: "{scope} scope, {N} artifacts affected, {effort} effort, Score: {score}/10"
     - label: "Plan B: Focused Update"
       description: "{scope} scope, {N} artifacts affected, {effort} effort, Score: {score}/10"
     - label: "Plan C: Custom Plan"
       description: "Provide your own implementation plan with specific ADR, component, and diagram changes"

STORE selected_plan

STEP 3: HANDLE CUSTOM PLAN

IF selected_plan == "Plan C":
   PROMPT: "Please provide your custom implementation plan. Include:
   1. List of ADR files to modify
   2. Specific sections to change in each ADR
   3. Component definition updates needed
   4. C4 diagram regeneration requirements
   5. Traceability updates needed"

   custom_plan = user_input

   # Parse custom plan and validate
   PARSE custom_plan for:
   - ADR file paths and sections
   - Component changes
   - Diagram regeneration scope
   - Traceability implications

   VALIDATE:
   - All mentioned ADR files exist
   - Changes maintain ADR consistency
   - Component alignment preserved
   - Traceability chains remain intact

   IF validation fails:
      ❌ Custom plan validation failed: {issues}
      PROMPT to revise or select Plan A/B
   ELSE:
      ✅ Custom plan validated
      SAVE custom_plan to implementation_plan.md

ELIF selected_plan == "Plan A" OR selected_plan == "Plan B":
   COPY selected option from implementation_options.md
     TO {session_folder}/implementation_plan.md

UPDATE registry:
   status = "planning_complete"
   lifecycle.phase = "planning"
   lifecycle.selected_plan = "{selected_plan}"
   lifecycle.updated_at = NOW()

✅ Implementation plan finalized: {selected_plan}

PROCEED to Phase 6: Implementation
```

---

### Phase 6: Implementation

**Purpose**: Execute the selected implementation plan with resumable checkpoints.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 6: IMPLEMENTATION
═══════════════════════════════════════════════════════════════

STEP 1: INITIALIZE IMPLEMENTATION LOG

WRITE {session_folder}/implementation_log.md:
# Implementation Log - {next_id}

Plan: {selected_plan}
Started: {ISO8601 timestamp}

## Steps

UPDATE registry:
   status = "implementing"
   lifecycle.phase = "implementation"
   lifecycle.implementation_started_at = NOW()
   lifecycle.updated_at = NOW()

STEP 2: EXECUTE PLAN STEPS

READ implementation_plan.md
PARSE steps from plan

FOR each step IN steps:
   step_number = index + 1

   APPEND to implementation_log.md:
   ### Step {step_number}: {step.title}
   Started: {timestamp}

   TRY:
      # Execute step based on type

      IF step.type == "update_adr":
         READ {SOLARCH_DIR}/09-decisions/{step.adr_file}
         PARSE ADR frontmatter and sections
         APPLY changes from step.changes
         UPDATE version in frontmatter (increment patch)
         UPDATE date in frontmatter
         WRITE updated ADR

      ELIF step.type == "update_component":
         READ {SOLARCH_DIR}/05-building-blocks/{step.component_file}
         APPLY changes from step.changes
         WRITE updated component

      ELIF step.type == "regenerate_c4_diagrams":
         IF step.scope == "partial":
            # Partial regeneration (specific diagrams)
            FOR each diagram IN step.diagrams:
               Skill({
                 skill: "SolArch_C4DiagramGenerator",
                 args: JSON.stringify({
                   system_name: system_name,
                   diagram_type: diagram.type,
                   diagram_name: diagram.name
                 })
               })
         ELIF step.scope == "full":
            # Full regeneration
            bash .claude/commands/solarch-diagrams.md --system {system_name}

      ELIF step.type == "update_quality_scenario":
         READ {SOLARCH_DIR}/07-quality/{step.scenario_file}
         APPLY changes from step.changes
         WRITE updated scenario

      ELIF step.type == "update_registry":
         READ {SOLARCH_DIR}/_registry/{step.registry_file}
         IF step.registry_file == "decisions.json":
            UPDATE ADR entry (version, status, date)
         ELIF step.registry_file == "components.json":
            UPDATE component entry
         WRITE updated registry

      ELIF step.type == "update_traceability":
         READ {SOLARCH_DIR}/traceability/solarch_traceability_register.json
         ADD or UPDATE links from step.links
         WRITE updated traceability

      # Log version history
      python3 .claude/hooks/version_history_logger.py \
        "traceability/" \
        "{system_name}" \
        "solarch" \
        "Claude" \
        "{version}" \
        "Feedback {next_id}: {step.title}" \
        "{artifact_ids_comma_separated}" \
        "{file_path}" \
        "modification"

      APPEND to implementation_log.md:
      Status: ✅ SUCCESS
      Completed: {timestamp}
      Files modified: {list files}

      UPDATE registry:
         lifecycle.last_completed_step = step_number
         lifecycle.updated_at = NOW()

   CATCH error:
      APPEND to implementation_log.md:
      Status: ❌ FAILED
      Error: {error.message}
      Failed at: {timestamp}

      UPDATE registry:
         status = "failed"
         lifecycle.phase = "implementation"
         lifecycle.failed_step = step_number
         lifecycle.error = error.message
         lifecycle.resume_point = step_number
         lifecycle.updated_at = NOW()

      ❌ Implementation failed at step {step_number}
      ERROR: {error.message}

      USE AskUserQuestion:
         question: "Implementation failed at step {step_number}: {step.title}. How should we proceed?"
         header: "Failure"
         multiSelect: false
         options:
           - label: "Retry Step"
             description: "Retry the failed step immediately"
           - label: "Skip Step"
             description: "Skip this step and continue (may break ADR consistency)"
           - label: "Abort"
             description: "Stop implementation, save resume point for later"
           - label: "Debug"
             description: "Investigate the error before deciding"

      STORE failure_action

      IF failure_action == "Retry Step":
         RETRY current step (max 2 retries)
      ELIF failure_action == "Skip Step":
         LOG skip to FAILURES_LOG.md
         CONTINUE to next step
      ELIF failure_action == "Abort":
         ⚠️ Implementation aborted - resume point saved
         EXIT
      ELIF failure_action == "Debug":
         DISPLAY error details, file paths, stack trace
         GOTO failure_action prompt (allow retry/skip/abort after debug)

STEP 3: GENERATE FILES CHANGED REPORT

WRITE {session_folder}/files_changed.md:
# Files Changed - {next_id}

## Summary
- Total files modified: {N}
- ADRs updated: {X}
- Components updated: {Y}
- C4 Diagrams regenerated: {Z}
- Quality Scenarios updated: {Q}
- Registries updated: {R}

## Detailed Changes

{For each file modified, list:}
### {file_path}
- Change type: {MODIFY|CREATE|DELETE}
- Sections affected: {section_names}
- Artifact IDs: {list IDs}
- Summary: {brief description}

UPDATE registry:
   status = "implemented"
   lifecycle.phase = "implementation"
   lifecycle.implementation_completed_at = NOW()
   lifecycle.updated_at = NOW()

✅ Implementation complete - all steps executed

PROCEED to Phase 7: Validation
```

---

### Phase 7: Validation (REFLEXION)

**Purpose**: Verify implementation correctness with multi-perspective review including ADR consistency and component alignment checks.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 7: VALIDATION (REFLEXION-ENHANCED)
═══════════════════════════════════════════════════════════════

STEP 1: INVOKE SHARED REVIEWER

Skill({
  skill: "Shared_FeedbackReviewer_Reflexion",
  args: JSON.stringify({
    feedback_id: next_id,
    stage: "solarch",
    system_name: system_name,
    session_folder: session_folder,
    implementation_plan_path: "{session_folder}/implementation_plan.md",
    files_changed_path: "{session_folder}/files_changed.md"
  })
})

# The skill performs:
# 1. Read implementation_plan.md and files_changed.md
# 2. Verify plan compliance (all steps executed)
# 3. Check ADR integrity:
#    - Valid ADR format (frontmatter, sections)
#    - No conflicting decisions
#    - Cross-ADR references valid
#    - Status fields correct
# 4. Check component alignment:
#    - Components match ADR decisions
#    - Rationales reference correct ADRs
#    - No architecture violations
# 5. Validate C4 diagrams (if regenerated):
#    - Diagrams match component definitions
#    - Consistency across diagram levels
# 6. Validate traceability chains:
#    - All chains intact (no broken links)
#    - ADR → Component links valid
#    - Quality scenario → ADR links valid
# 7. Multi-perspective review:
#    - Requirements Validator: Check ADR traceability to requirements
#    - Architecture Validator: Check ADR consistency and component alignment
#    - Quality Validator: Check quality scenario alignment with ADRs
# 8. Calculate consensus score (0-10)
# 9. Generate VALIDATION_REPORT.md

READ VALIDATION_REPORT.md output from skill

STEP 2: DISPLAY VALIDATION RESULTS

DISPLAY VALIDATION_REPORT.md content

EXTRACT from VALIDATION_REPORT.md:
- validation_passed (boolean)
- plan_compliance (percentage)
- adr_consistency_valid (boolean)
- component_alignment_valid (boolean)
- c4_diagrams_valid (boolean)
- traceability_valid (boolean)
- consensus_score (0-10)
- critical_issues (list)
- warnings (list)

IF validation_passed == true AND consensus_score >= 7.0:
   ✅ VALIDATION PASSED
   Consensus Score: {consensus_score}/10

   UPDATE registry:
      status = "validated"
      lifecycle.phase = "validation"
      lifecycle.validation_passed = true
      lifecycle.validation_score = consensus_score
      lifecycle.updated_at = NOW()

   PROCEED to Phase 8: Completion

ELSE:
   ❌ VALIDATION FAILED
   Consensus Score: {consensus_score}/10

   DISPLAY critical_issues and warnings

   USE AskUserQuestion:
      question: "Validation failed with score {consensus_score}/10. How should we proceed?"
      header: "Validation"
      multiSelect: false
      options:
        - label: "Fix Issues"
          description: "Review validation report and fix critical issues before re-validating (recommended for ADR consistency or component alignment failures)"
        - label: "Accept Anyway"
          description: "Accept implementation despite validation failures (not recommended for architectural issues)"
        - label: "Re-Implement"
          description: "Revert changes and re-run implementation with corrected plan"

   STORE validation_action

   IF validation_action == "Fix Issues":
      DISPLAY fix instructions from VALIDATION_REPORT.md
      PROMPT user to make manual fixes
      WAIT for user confirmation
      RETRY validation (GOTO STEP 1)

   ELIF validation_action == "Accept Anyway":
      ⚠️ Validation bypassed - proceeding with warnings
      UPDATE registry:
         status = "validated_with_warnings"
         lifecycle.validation_bypassed = true
         lifecycle.validation_warnings = warnings
      PROCEED to Phase 8: Completion

   ELIF validation_action == "Re-Implement":
      UPDATE registry:
         status = "re_implementing"
         lifecycle.phase = "implementation"
      GOTO Phase 6: Implementation
```

---

### Phase 8: Completion

**Purpose**: Finalize feedback processing and close the session.

```bash
═══════════════════════════════════════════════════════════════
⏳ PHASE 8: COMPLETION
═══════════════════════════════════════════════════════════════

STEP 1: GENERATE FEEDBACK SUMMARY

WRITE {session_folder}/FEEDBACK_SUMMARY.md:
---
feedback_id: {next_id}
status: validated
closed_at: {ISO8601 timestamp}
---

# Feedback Summary - {next_id}

## Original Feedback

{feedback_content}

## Impact Analysis Summary

- Chains Affected: {chains_affected}
- Artifacts Affected: {artifacts_affected}
- ADRs: {X} modified
- Components: {Y} modified
- C4 Diagrams: {Z} regenerated
- Quality Scenarios: {Q} modified
- Registries: {R} updated
- Confidence Level: {confidence_level} ({confidence_percentage}%)

## ADR Consistency Summary

- Consistency Issues Resolved: {count}
- Cross-References Updated: {count}
- Decision Conflicts: {none/resolved}

## Component Alignment Summary

- Alignment Issues Resolved: {count}
- Components Updated: {list}
- Architecture Violations: {none/resolved}

## Implementation Summary

- Plan Selected: {selected_plan}
- Steps Executed: {total_steps} / {total_steps}
- Files Modified: {total_files}
- Implementation Time: {duration}

## Validation Summary

- Validation Status: PASSED
- Consensus Score: {consensus_score}/10
- ADR Consistency: {valid/invalid}
- Component Alignment: {valid/invalid}
- Critical Issues: {critical_count}
- Warnings: {warning_count}

## Files Modified

{List all files from files_changed.md}

## Traceability Impact

{List affected traceability chains}

## Reflexion Insights

**Confidence Metrics**:
- Impact Analysis: {confidence_percentage}%
- Validation Score: {consensus_score}/10

**Key Recommendations**:
{List reflexion recommendations from impact and validation}

---

**Session Folder**: {session_folder}
**Completed**: {ISO8601 timestamp}

STEP 2: UPDATE REGISTRY

UPDATE solarch_feedback_registry.json:
   {
      "{next_id}": {
         "status": "closed",
         "lifecycle": {
            ...existing lifecycle fields,
            "closed_at": "{ISO8601}",
            "total_duration_seconds": {duration},
            "validation_score": {consensus_score},
            "files_modified": {total_files}
         }
      }
   }

STEP 3: DISPLAY COMPLETION SUMMARY

═══════════════════════════════════════════════════════════════
✅ FEEDBACK PROCESSING COMPLETE: {next_id}
═══════════════════════════════════════════════════════════════

Status: CLOSED
Validation: PASSED ({consensus_score}/10)

Impact:
├─ ADRs: {X} modified
├─ Components: {Y} modified
├─ C4 Diagrams: {Z} regenerated
├─ Quality Scenarios: {Q} modified
└─ Registries: {R} updated

ADR Consistency: ✅ VALIDATED
Component Alignment: ✅ VALIDATED

Files Modified: {total_files}
Duration: {duration}

Session Folder: {session_folder}
Summary: {session_folder}/FEEDBACK_SUMMARY.md

═══════════════════════════════════════════════════════════════

DONE
```

---

## Resume Capability

If implementation fails or is interrupted, resume from the last checkpoint:

```bash
/solarch-feedback resume SF-003
```

**Resume Procedure**: (Same as productspecs-feedback)

---

## Status Mode

Check current feedback processing status:

```bash
/solarch-feedback status
```

**Status Output**: (Similar to productspecs-feedback with SolArch-specific phase names)

---

## List Mode

List all registered feedback items:

```bash
/solarch-feedback list
```

**List Output**: (Similar to productspecs-feedback with SolArch feedback types)

---

## Feedback Types

| Type | Code | Description | Typical Artifacts Affected |
|------|------|-------------|----------------------------|
| **ADREnhancement** | ADR-ENH | Enhancement to existing ADR | ADRs, decisions.json, components |
| **ComponentChange** | COMP-CHG | Change to component definition | Components, ADRs (alignment), C4 diagrams |
| **DiagramUpdate** | DIAG-UPD | Update to C4 diagrams | C4 diagrams, components |
| **QualityScenario** | QUAL-SCN | Change to quality scenario | Quality scenarios, ADRs, components |
| **TraceabilityGap** | TRC-GAP | Missing traceability link or broken chain | Traceability registries |
| **ADRConsistency** | ADR-CON | ADR consistency issue or decision conflict | ADRs (multiple), decisions.json |

---

## Impact Categories

| Category | Code | Artifacts | Files |
|----------|------|-----------|-------|
| **ADR** | CAT-ADR | Architecture Decision Records | 09-decisions/ADR-*.md, _registry/decisions.json |
| **Component** | CAT-COMP | Building blocks | 05-building-blocks/*.md, _registry/components.json |
| **Diagram** | CAT-DIAG | C4 diagrams | 06-runtime-view/*.mmd |
| **Quality** | CAT-QUAL | Quality scenarios | 07-quality/*.md |
| **Traceability** | CAT-TRACE | Traceability links | traceability/solarch_traceability_register.json |

---

## Session Folder Structure

```
SolArch_<SystemName>/feedback-sessions/
├── solarch_feedback_registry.json
└── <YYYY-MM-DD>_SolArchFeedback-<ID>/
    ├── FEEDBACK_ORIGINAL.md              # Original feedback text
    ├── impact_analysis.md                # Reflexion-enhanced impact analysis
    ├── implementation_options.md         # Generated plan options with X/10 scoring
    ├── implementation_plan.md            # Selected implementation plan
    ├── implementation_log.md             # Step-by-step execution log
    ├── files_changed.md                  # Detailed file change report
    ├── VALIDATION_REPORT.md              # Multi-perspective validation results
    └── FEEDBACK_SUMMARY.md               # Final completion summary
```

---

## Registry Schema

```json
{
  "schema_version": "2.0.0",
  "system_name": "{SOLARCH_NAME}",
  "stage": "solarch",
  "feedback_items": {
    "SF-001": {
      "title": "{brief_summary}",
      "type": "{ADREnhancement|ComponentChange|DiagramUpdate|QualityScenario|TraceabilityGap|ADRConsistency}",
      "severity": "{Critical|High|Medium|Low}",
      "status": "{analyzing|approved|planning_complete|implementing|implemented|validated|validated_with_warnings|closed|rejected|failed}",
      "source": {
        "origin": "{Architecture Review|Technical Lead|Security Team|Stakeholder|External Consultant}",
        "priority": "{Critical|High|Medium|Low}",
        "submitted_by": "{name}",
        "submitted_at": "{ISO8601}"
      },
      "categories": ["{CAT-ADR}", "{CAT-COMP}", "{CAT-DIAG}", "{CAT-QUAL}", "{CAT-TRACE}"],
      "impact": {
        "chains_affected": N,
        "artifacts_affected": M,
        "layer_1_adrs": X,
        "layer_2_components": Y,
        "layer_3_diagrams": Z,
        "layer_4_quality": Q,
        "layer_5_registries": R,
        "adr_consistency_issues": K,
        "component_alignment_issues": L,
        "c4_regeneration_required": true|false,
        "diagrams_affected": D,
        "confidence_level": "{HIGH|MEDIUM|LOW}",
        "confidence_percentage": 0-100,
        "reflexion_score": {confidence_percentage}
      },
      "lifecycle": {
        "created_at": "{ISO8601}",
        "updated_at": "{ISO8601}",
        "approved_at": "{ISO8601}",
        "implementation_started_at": "{ISO8601}",
        "implementation_completed_at": "{ISO8601}",
        "validation_passed": true|false,
        "validation_score": 0-10,
        "validation_bypassed": true|false,
        "closed_at": "{ISO8601}",
        "phase": "{input_collection|impact_analysis|registration|approval_gate|planning|implementation|validation|completion}",
        "selected_plan": "{Plan A|Plan B|Plan C}",
        "last_completed_step": N,
        "failed_step": N,
        "resume_point": N,
        "error": "{error_message}",
        "session_folder": "{path}",
        "files_modified": N,
        "total_duration_seconds": N
      }
    }
  }
}
```

---

## Error Handling

| Error | Action |
|-------|--------|
| No SolArch found | ❌ Show error, suggest running `/solarch` |
| Registry corrupt | Attempt recovery, create new if needed |
| Multiple SolArch found | Use AskUserQuestion to select target system |
| Implementation step fails | Save resume point, offer Retry/Skip/Abort via AskUserQuestion |
| Validation fails (ADR consistency) | Display issues, offer Fix/Accept/Re-Implement via AskUserQuestion |
| Validation fails (component alignment) | Display issues, offer Fix/Accept/Re-Implement via AskUserQuestion |
| C4 diagram regeneration fails | Log to FAILURES_LOG.md, mark diagram validation as failed, continue |
| File not found during implementation | Log skip to implementation_log.md, mark step as failed |
| JSON parse error in registry | ❌ BLOCK - registry must be manually fixed before proceeding |

---

## Integration with Other Stages

Changes to Solution Architecture may propagate to downstream stages:

```
SolArch Change
       ↓
   [Impact Analysis]
       ↓
┌──────┴──────┐
│             │
↓             ↓
Upstream?     Downstream?
(Discovery,   (Implementation)
 Prototype,
 ProductSpecs)
       ↓             ↓
 [Flag for      [Automatic
  manual        propagation
  review]       if possible]
```

### Upstream Impact (Discovery/Prototype/ProductSpecs)
If feedback affects upstream artifacts (Pain Points, JTBD, Requirements, Modules), the system **flags this for manual review** but does **not automatically modify** those stages. Use stage-specific feedback commands instead.

### Downstream Impact (Implementation)
If Implementation stage exists and references affected ADRs or components:
- **Implementation tasks may become outdated**
- **Code may not match updated architecture**
- The system **logs warnings** in VALIDATION_REPORT.md
- Use `/htec-sdd-changerequest` to propagate changes to implementation

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/solarch` | Generate Solution Architecture |
| `/solarch-status` | Show SolArch generation progress |
| `/solarch-decisions` | Review/regenerate ADRs |
| `/solarch-trace` | Validate traceability chains |
| `/discovery-feedback` | Process feedback on Discovery artifacts |
| `/prototype-feedback` | Process feedback on Prototype artifacts |
| `/productspecs-feedback` | Process feedback on ProductSpecs artifacts |
| `/htec-sdd-changerequest` | Process change requests on Implementation |

---

## Examples

### Example 1: Process Inline Feedback (ADR Enhancement)

```bash
/solarch-feedback "ADR-001 needs stronger justification for monolith choice with scaling analysis"
```

**Output**: (See Phase 2 example output above - full workflow with ADR-001 enhancement)

---

### Example 2: Component Alignment Issue

```bash
/solarch-feedback feedback/component_alignment.md
```

**(component_alignment.md content)**:
```markdown
# Component Alignment Issue

## Summary
COMP-CORE rationale doesn't mention ADR-001's bounded context design.

## Details
- ADR-001 states "Modules designed with bounded contexts for future extraction"
- COMP-CORE says "Core business logic centralized for simplicity"
- Need alignment

## Priority: Medium
## Source: Architecture Review
```

**Output**: (Similar to Example 1 with component alignment focus)

---

## Reflexion Integration Summary

This command integrates reflexion at **3 critical phases**:

### Phase 2: Impact Analysis
- **Skill**: Shared_FeedbackImpactAnalyzer_Reflexion
- **Self-Assessment**: Completeness, Accuracy, Downstream Impact, ADR Consistency, Component Alignment
- **Output**: Confidence Level (HIGH/MEDIUM/LOW), Confidence Percentage (0-100%)
- **Purpose**: Ensure all affected ADRs, components, and diagrams identified before approval

### Phase 5: Implementation Planning
- **Skill**: Shared_FeedbackPlanGenerator_Reflexion
- **Self-Assessment**: Completeness, Correctness, Risk Management, ADR Consistency Preservation
- **Output**: X/10 Score per option (recommend ≥ 8/10)
- **Purpose**: Generate high-quality implementation plans that maintain architectural integrity

### Phase 7: Validation
- **Skill**: Shared_FeedbackReviewer_Reflexion
- **Multi-Perspective Review**: Requirements (ADR traceability), Architecture (ADR consistency + component alignment), Quality (quality scenario alignment)
- **Output**: Consensus Score 0-10 (PASS ≥ 7.0)
- **Purpose**: Verify implementation correctness from multiple architectural perspectives

---

## Success Criteria

Feedback processing is considered successful when:

1. ✅ **Impact Analysis**: Confidence ≥ 85% (HIGH) OR user accepts MEDIUM/LOW with justification
2. ✅ **Approval Gate**: User explicitly approves (not rejected or deferred)
3. ✅ **Implementation**: All plan steps executed successfully (100% completion)
4. ✅ **Validation**: Consensus Score ≥ 7.0/10 (PASS)
5. ✅ **ADR Consistency**: All cross-ADR references valid, no decision conflicts
6. ✅ **Component Alignment**: All components match ADR decisions, no architecture violations
7. ✅ **Traceability**: All chains intact, ADR → Component links valid
8. ✅ **C4 Diagrams**: If regeneration required, all diagrams consistent with updated components

---

**END OF COMMAND**
