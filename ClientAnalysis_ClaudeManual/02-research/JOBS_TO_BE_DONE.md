# Jobs To Be Done - ClaudeManual

---
system_name: ClaudeManual
checkpoint: CP-4
total_jobs: 12
p0_jobs: 4
p1_jobs: 5
p2_jobs: 3
date_created: 2026-01-31
session: disc-claude-manual-004
created_by: discovery-jtbd-extractor
---

## Executive Summary

This document outlines **12 jobs** derived from 6 validated pain points across the ClaudeManual project. The primary functional jobs center on **knowledge transfer, framework discovery, and developer self-service**. Two critical P0 jobs (JTBD-1.1, JTBD-1.2) address the core challenge: transforming file-system-based documentation into an interactive, human-friendly manual.

**Job Distribution**:
- **Functional Jobs**: 8 jobs (learning, searching, organizing, editing)
- **Emotional Jobs**: 2 jobs (confidence, autonomy)
- **Social Jobs**: 2 jobs (perceived competence, team efficiency)

**Priority Breakdown**:
- **P0 (Critical)**: 4 jobs - Block primary knowledge transfer and onboarding goals
- **P1 (Important)**: 5 jobs - Significantly improve efficiency and user experience
- **P2 (Nice-to-have)**: 3 jobs - Enhance personalization and workflow optimization

---

## Functional Jobs

### JTBD-1.1: Enable Self-Service Framework Learning (P0)

**Statement**: When I need to onboard new team members to the Claude framework, I want to provide an interactive documentation platform with visual hierarchy and integrated examples, so I can enable self-service learning without manual training sessions.

**Context**:
- **User Types**: UT-001 (Framework Creator/Maintainer), UT-006 (Executives)
- **Traces From**: PP-1.1 (Knowledge Transfer Complexity)
- **Frequency**: Daily - every new team member onboarding
- **Importance**: Blocks scalable knowledge transfer and team productivity

**Success Criteria**:
1. New team members can explore framework structure independently within first hour
2. Trainer time reduced by 80% per new team member
3. All framework components are discoverable without file system navigation
4. Post-training retention rate > 90% after 1 week (measured by ability to locate tools)

**Current vs. Desired State**:
- **Current**: Manual demonstrations of .claude/skills/, .claude/commands/, .claude/agents/ folders
- **Desired**: Interactive web interface with hierarchical navigation, collapsible sections, and search

---

### JTBD-1.2: Understand Framework Component Context (P0)

**Statement**: When I'm exploring a framework skill, command, or agent, I want to see purpose, usage examples, options, and workflow diagrams in a unified view, so I can understand when and how to use it correctly.

**Context**:
- **User Types**: UT-002 (Product People), UT-003 (Developers), UT-004 (Build/Client Partners)
- **Traces From**: PP-1.2 (Lack of Contextual Documentation)
- **Frequency**: Multiple times per day during active framework usage
- **Importance**: Prevents tool misuse and reduces learning curve

**Success Criteria**:
1. Every component shows purpose, examples, and workflow in one view
2. Users can answer "when to use X vs Y" within 30 seconds
3. Example usage patterns are visible without reading source code
4. High-level workflow diagrams show component relationships

**Current vs. Desired State**:
- **Current**: Reading individual markdown files, mentally piecing together context
- **Desired**: Multi-section detail pane with tabs: Purpose | Examples | Options | Workflow | Traceability

---

### JTBD-1.3: Quickly Find Relevant Framework Tools (P1)

**Statement**: When I have a specific product discovery or implementation task, I want to search and filter framework components by capability, stage, or tag, so I can find the right tool without browsing folder structures.

**Context**:
- **User Types**: UT-002 (Product People), UT-003 (Developers), UT-004 (Build/Client Partners), UT-005 (Business Developers)
- **Traces From**: PP-1.3 (Discoverability Challenge)
- **Frequency**: 3-5 times per week when starting new tasks
- **Importance**: Significantly reduces time-to-productivity

**Success Criteria**:
1. Search results appear within 2 seconds of typing query
2. Can filter by stage (Discovery, Prototype, Implementation, Utility)
3. Can tag components (e.g., "JTBD extraction", "code generation")
4. Search includes skill/command/agent names, descriptions, and keywords

**Current vs. Desired State**:
- **Current**: Manually browsing .claude/skills/ folder tree
- **Desired**: Search bar with instant results and multi-faceted filters

---

### JTBD-1.4: Understand Which Tools Apply to Current Workflow Stage (P1)

**Statement**: When I'm in a specific workflow phase (e.g., Discovery, Prototype, Implementation), I want to visually filter framework components by stage, so I can focus only on relevant tools without mental mapping.

**Context**:
- **User Types**: UT-002 (Product People), UT-003 (Developers), UT-004 (Build/Client Partners), UT-006 (Executives)
- **Traces From**: PP-1.4 (Organizational Chaos)
- **Frequency**: Daily - every time user switches workflow phases
- **Importance**: Reduces cognitive load and prevents using wrong-stage tools

**Success Criteria**:
1. Components are visually grouped by Discovery, Prototype, ProductSpecs, SolArch, Implementation stages
2. Can toggle stage filter to hide irrelevant tools
3. Stage badges are visible on every component card
4. Stage-specific landing pages show only phase-appropriate tools

**Current vs. Desired State**:
- **Current**: Mentally mapping file names (Discovery_*, Prototype_*) to workflow stages
- **Desired**: Visual stage filters with color-coded badges and grouped layouts

---

### JTBD-1.5: Edit Framework Source Files Efficiently (P1)

**Statement**: When I want to customize or extend a framework component, I want to copy the file path with one click, so I can open it in my editor without navigating the file system.

**Context**:
- **User Types**: UT-003 (Developers), UT-001 (Framework Maintainers)
- **Traces From**: PP-1.6 (Developer Friction)
- **Frequency**: 2-3 times per week for active framework contributors
- **Importance**: Reduces friction for framework extension and customization

**Success Criteria**:
1. Every component has a "Copy Path" button showing full file path
2. Clicking copies path to clipboard with visual confirmation
3. Paths are shown in detail view (e.g., `.claude/skills/Discovery_JTBD/SKILL.md`)
4. Developer can open file in editor within 10 seconds

**Current vs. Desired State**:
- **Current**: Manually navigating to .claude/skills/, .claude/commands/, .claude/agents/ folders
- **Desired**: One-click path copy from documentation interface

---

### JTBD-1.6: Bookmark Frequently-Used Tools (P2)

**Statement**: When I repeatedly use certain framework commands or skills, I want to save them as favorites, so I can access them instantly without searching.

**Context**:
- **User Types**: UT-003 (Developers), UT-001 (Framework Maintainers)
- **Traces From**: PP-1.5 (Lack of Personalization)
- **Frequency**: Weekly for power users
- **Importance**: Nice-to-have optimization for frequent users

**Success Criteria**:
1. Every component has "Add to Favorites" toggle
2. Favorites appear in a persistent sidebar or quick-access panel
3. Favorites persist across sessions (local storage or user profile)
4. Can reorder and remove favorites

**Current vs. Desired State**:
- **Current**: Manually remembering file paths or creating personal bookmarks
- **Desired**: Built-in favorites system with quick-access shortcuts

---

### JTBD-1.7: Navigate Framework Hierarchies Visually (P0)

**Statement**: When I'm learning the framework structure, I want to see a visual tree of skills → commands → agents with expand/collapse controls, so I can understand organizational hierarchy without reading folder names.

**Context**:
- **User Types**: UT-001 (Framework Creators), UT-002 (Product People), UT-006 (Executives)
- **Traces From**: PP-1.1 (Knowledge Transfer Complexity), PP-1.4 (Organizational Chaos)
- **Frequency**: First-time learning and periodic reference
- **Importance**: Essential for mental model formation

**Success Criteria**:
1. Hierarchical tree shows Skills, Commands, Agents with nested categories
2. Can expand/collapse categories (e.g., Discovery Skills, Prototype Skills)
3. Visual indentation and icons clarify parent-child relationships
4. Clicking tree node shows detail view

**Current vs. Desired State**:
- **Current**: Reading folder structure in terminal or IDE
- **Desired**: Interactive tree widget with expand/collapse, icons, and click navigation

---

### JTBD-1.8: Compare Similar Framework Components (P1)

**Statement**: When I'm deciding between similar skills or commands (e.g., `/discovery` vs `/discovery-multiagent`), I want to see side-by-side comparisons of features and use cases, so I can choose the right tool for my context.

**Context**:
- **User Types**: UT-002 (Product People), UT-003 (Developers), UT-004 (Build/Client Partners)
- **Traces From**: PP-1.2 (Lack of Contextual Documentation)
- **Frequency**: 1-2 times per project when choosing workflow approaches
- **Importance**: Prevents suboptimal tool selection

**Success Criteria**:
1. Related components are linked in detail view (e.g., "See also: /discovery-multiagent")
2. Can open comparison view showing features, performance, use cases
3. Comparison highlights key differences (e.g., "60% faster", "requires agent coordination")
4. Decision guidance: "Use X when..., Use Y when..."

**Current vs. Desired State**:
- **Current**: Reading multiple skill files separately and mentally comparing
- **Desired**: Side-by-side comparison table with decision criteria

---

## Emotional Jobs

### JTBD-2.1: Feel Confident Using the Framework (P0)

**Statement**: When I'm applying the framework to a real project, I want to see validated examples and workflow diagrams, so I can trust that I'm using tools correctly and avoid costly mistakes.

**Context**:
- **User Types**: UT-002 (Product People), UT-003 (Developers), UT-004 (Build/Client Partners)
- **Traces From**: PP-1.2 (Lack of Contextual Documentation)
- **Frequency**: Daily during active framework usage
- **Importance**: User confidence drives adoption and reduces support requests

**Success Criteria**:
1. Every component has at least one real-world usage example
2. Examples show command syntax, expected output, and common pitfalls
3. Workflow diagrams clarify when to use component in overall process
4. User confidence score > 80% (measured by post-training survey)

**Current vs. Desired State**:
- **Current**: Reading raw skill files, uncertainty about correct usage
- **Desired**: Confidence-building examples, diagrams, and decision trees

---

### JTBD-2.2: Feel Autonomous in Framework Exploration (P2)

**Statement**: When I want to learn a new framework capability, I want to explore documentation independently without asking colleagues, so I can maintain productivity and avoid dependency on experts.

**Context**:
- **User Types**: UT-002 (Product People), UT-003 (Developers), UT-005 (Business Developers)
- **Traces From**: PP-1.1 (Knowledge Transfer Complexity), PP-1.3 (Discoverability Challenge)
- **Frequency**: Weekly when encountering new use cases
- **Importance**: Reduces expert bottlenecks and empowers users

**Success Criteria**:
1. Can answer 90% of framework questions without asking colleagues
2. Search + documentation covers common questions
3. Onboarding time reduced by 70%
4. Support ticket volume decreases by 60%

**Current vs. Desired State**:
- **Current**: Asking framework experts for guidance
- **Desired**: Self-service documentation with comprehensive search

---

## Social Jobs

### JTBD-3.1: Be Perceived as Framework-Competent (P1)

**Statement**: When I present framework capabilities to clients or stakeholders, I want to quickly access professional examples and diagrams, so I can demonstrate expertise and build credibility.

**Context**:
- **User Types**: UT-004 (Build/Client Partners), UT-005 (Business Developers), UT-006 (Executives)
- **Traces From**: PP-1.1 (Knowledge Transfer Complexity), PP-1.3 (Discoverability Challenge)
- **Frequency**: Monthly during client presentations
- **Importance**: Affects sales and client trust

**Success Criteria**:
1. Can generate presentation-ready examples within 5 minutes
2. Documentation includes visual diagrams suitable for stakeholder demos
3. Can export component descriptions for client-facing materials
4. Professional appearance (not raw markdown files)

**Current vs. Desired State**:
- **Current**: Manually creating slides from raw files
- **Desired**: One-click export of component diagrams and descriptions

---

### JTBD-3.2: Contribute to Team Framework Efficiency (P2)

**Statement**: When I customize or improve a framework component, I want to share my changes with the team through the same documentation interface, so I can contribute to collective knowledge without separate communication.

**Context**:
- **User Types**: UT-003 (Developers), UT-001 (Framework Maintainers)
- **Traces From**: PP-1.6 (Developer Friction)
- **Frequency**: Quarterly for active contributors
- **Importance**: Encourages knowledge sharing and framework evolution

**Success Criteria**:
1. Can annotate components with team-specific notes
2. Can submit documentation improvements via interface
3. Changes are visible to team members
4. Contribution activity is tracked and recognized

**Current vs. Desired State**:
- **Current**: Separate communication channels (Slack, email) for sharing improvements
- **Desired**: Built-in contribution workflow with versioning

---

## Jobs Priority Matrix

| ID | Job Title | Priority | User Types | Pain Points | Category |
|---|---|---|---|---|---|
| JTBD-1.1 | Enable Self-Service Framework Learning | P0 | UT-001, UT-006 | PP-1.1 | Functional |
| JTBD-1.2 | Understand Framework Component Context | P0 | UT-002, UT-003, UT-004 | PP-1.2 | Functional |
| JTBD-1.7 | Navigate Framework Hierarchies Visually | P0 | UT-001, UT-002, UT-006 | PP-1.1, PP-1.4 | Functional |
| JTBD-2.1 | Feel Confident Using the Framework | P0 | UT-002, UT-003, UT-004 | PP-1.2 | Emotional |
| JTBD-1.3 | Quickly Find Relevant Framework Tools | P1 | UT-002, UT-003, UT-004, UT-005 | PP-1.3 | Functional |
| JTBD-1.4 | Understand Which Tools Apply to Current Workflow Stage | P1 | UT-002, UT-003, UT-004, UT-006 | PP-1.4 | Functional |
| JTBD-1.5 | Edit Framework Source Files Efficiently | P1 | UT-003, UT-001 | PP-1.6 | Functional |
| JTBD-1.8 | Compare Similar Framework Components | P1 | UT-002, UT-003, UT-004 | PP-1.2 | Functional |
| JTBD-3.1 | Be Perceived as Framework-Competent | P1 | UT-004, UT-005, UT-006 | PP-1.1, PP-1.3 | Social |
| JTBD-1.6 | Bookmark Frequently-Used Tools | P2 | UT-003, UT-001 | PP-1.5 | Functional |
| JTBD-2.2 | Feel Autonomous in Framework Exploration | P2 | UT-002, UT-003, UT-005 | PP-1.1, PP-1.3 | Emotional |
| JTBD-3.2 | Contribute to Team Framework Efficiency | P2 | UT-003, UT-001 | PP-1.6 | Social |

---

## Traceability Summary

### Pain Point → JTBD Coverage

| Pain Point | JTBD Jobs | Coverage |
|---|---|---|
| PP-1.1 (Knowledge Transfer Complexity) | JTBD-1.1, JTBD-1.7, JTBD-2.2, JTBD-3.1 | 4 jobs |
| PP-1.2 (Lack of Contextual Documentation) | JTBD-1.2, JTBD-1.8, JTBD-2.1 | 3 jobs |
| PP-1.3 (Discoverability Challenge) | JTBD-1.3, JTBD-2.2, JTBD-3.1 | 3 jobs |
| PP-1.4 (Organizational Chaos) | JTBD-1.4, JTBD-1.7 | 2 jobs |
| PP-1.5 (Lack of Personalization) | JTBD-1.6 | 1 job |
| PP-1.6 (Developer Friction) | JTBD-1.5, JTBD-3.2 | 2 jobs |

**Total Coverage**: All 6 pain points addressed by 12 jobs.

### User Type → JTBD Mapping

| User Type | Primary Jobs | Job Count |
|---|---|---|
| UT-001 (Framework Creators) | JTBD-1.1, JTBD-1.5, JTBD-1.6, JTBD-1.7, JTBD-3.2 | 5 jobs |
| UT-002 (Product People) | JTBD-1.2, JTBD-1.3, JTBD-1.4, JTBD-1.7, JTBD-1.8, JTBD-2.1, JTBD-2.2 | 7 jobs |
| UT-003 (Developers) | JTBD-1.2, JTBD-1.3, JTBD-1.4, JTBD-1.5, JTBD-1.6, JTBD-1.8, JTBD-2.1, JTBD-2.2, JTBD-3.2 | 9 jobs |
| UT-004 (Build/Client Partners) | JTBD-1.2, JTBD-1.3, JTBD-1.4, JTBD-1.8, JTBD-2.1, JTBD-3.1 | 6 jobs |
| UT-005 (Business Developers) | JTBD-1.3, JTBD-2.2, JTBD-3.1 | 3 jobs |
| UT-006 (Executives) | JTBD-1.1, JTBD-1.4, JTBD-1.7, JTBD-3.1 | 4 jobs |

---

## Validation Notes

✅ **All jobs use When/Want/So-that format**
✅ **All jobs trace to specific pain points**
✅ **All jobs map to identified user types**
✅ **Success criteria are measurable**
✅ **Current vs. Desired state specified for all functional jobs**
✅ **Priority assignments based on pain point severity and user impact**

---

## Traceability

- **Source Material**: CM-001 (Client_Materials/Interviews/ClaudeManual.txt)
- **Pain Points**: ClientAnalysis_ClaudeManual/01-analysis/PAIN_POINTS.md
- **Pain Points Registry**: traceability/pain_points_registry.json
- **User Types Registry**: traceability/user_types_registry.json
- **Checkpoint**: CP-4
- **Session**: disc-claude-manual-004
- **Created By**: discovery-jtbd-extractor
- **Date**: 2026-01-31

---

*12 jobs derived from 6 validated pain points. 100% pain point coverage. All jobs follow When/Want/So-that framework.*
