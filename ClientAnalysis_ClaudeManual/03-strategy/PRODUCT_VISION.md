# Product Vision - ClaudeManual

---
system_name: ClaudeManual
checkpoint: CP-5
vision_horizon: 2 years
date_created: 2026-01-31
session: disc-claude-manual-005
created_by: discovery-vision-generator
---

## Vision Statement

Transform the Claude framework from a powerful but opaque collection of files into an interactive knowledge platform that enables every team member to independently discover, understand, and confidently apply AI-assisted development tools.

---

## For Statement (Geoffrey Moore Template)

**For** product managers, developers, and delivery teams building AI-assisted solutions

**Who** struggle to learn and apply the Claude framework due to fragmented documentation, poor discoverability, and dependency on manual training sessions

**The** ClaudeManual **is a** visual, interactive documentation platform

**That** enables self-service learning through hierarchical navigation, contextual examples, searchable content, and stage-based organization

**Unlike** raw markdown files in folder structures or static documentation sites

**Our product** provides a dual-pane interface where users can visually explore framework components, understand their purpose and relationships, and immediately access source files for customization - reducing onboarding time from 3-4 hours to 30-60 minutes.

---

## Value Proposition Canvas

### Customer Profile

**Jobs**:
1. Enable self-service framework learning without manual training sessions (JTBD-1.1)
2. Understand framework component context with examples and workflow diagrams (JTBD-1.2)
3. Navigate framework hierarchies visually with expand/collapse controls (JTBD-1.7)
4. Feel confident using the framework with validated examples (JTBD-2.1)

**Pains**:
1. Knowledge transfer complexity - showing raw folder structures lacks visual context (PP-1.1)
2. Lack of contextual documentation - individual files don't explain relationships or usage patterns (PP-1.2)
3. Discoverability challenge - finding relevant skills/commands/agents without search (PP-1.3)

**Gains**:
- 80% reduction in trainer time per new team member
- 90% post-training retention rate after 1 week
- 70% reduction in onboarding time
- 60% decrease in support ticket volume

### Value Map

**Products & Services**:
- Interactive web application with dual-pane master-detail interface
- Visual hierarchy showing skills, commands, agents, and their relationships
- Search engine with stage-based filtering and capability tagging
- Multi-section documentation (purpose, examples, options, workflow diagrams)
- One-click file path copy for source customization
- Favorites system for frequently-used tools
- Modern minimalistic terminal-inspired design

**Pain Relievers**:
- Eliminates manual training sessions through self-service exploration (addresses PP-1.1)
- Provides unified view with purpose, examples, and workflow context (addresses PP-1.2)
- Instant search and stage-based filtering for tool discovery (addresses PP-1.3)
- Visual organization by workflow stages prevents organizational chaos (addresses PP-1.4)
- File path references with copy-paste reduce developer friction (addresses PP-1.6)

**Gain Creators**:
- New team members explore framework independently within first hour
- Users answer 90% of framework questions without asking colleagues
- Developers locate and edit source files within 10 seconds
- Product managers confidently recommend framework tools to clients
- Framework adoption rate increases from 30% to 80%+ within 30 days

---

## North Star Metric

**Time-to-Independent-Productivity**: Hours from first framework exposure to successfully executing a complete workflow (discovery/prototype/implementation) without assistance.

**Target**: Reduce from 16 hours (manual training + trial-and-error) to 2 hours (self-guided exploration).

**Why this metric**: Directly measures the vision of enabling self-service learning and reducing dependency on manual knowledge transfer.

---

## Strategic Pillars

### 1. Visual-First Learning Experience
Transform file-system-based documentation into an interactive, hierarchical navigation experience that mirrors how humans naturally learn and explore complex systems.

**Key Initiatives**:
- Dual-pane master-detail interface (master pane: hierarchical tree, detail pane: multi-section documentation)
- Expand/collapse controls for category exploration
- Stage-based visual organization (Discovery, Prototype, ProductSpecs, SolArch, Implementation, Utilities)
- High-level workflow diagrams showing component relationships

**Traces to**: PP-1.1, PP-1.2, PP-1.4, JTBD-1.1, JTBD-1.2, JTBD-1.7

**Success Criteria**:
- 90% of users can locate a tool within 2 minutes without search
- Visual hierarchy reduces cognitive load by 70% (measured by user testing)
- 85%+ user satisfaction score for "ease of navigation"

---

### 2. Intelligent Discovery & Search
Enable users to find the right tool for their task through powerful search, tagging, and filtering capabilities that surface relevant content by capability, stage, or keyword.

**Key Initiatives**:
- Full-text search across skill/command/agent names, descriptions, and keywords
- Stage-based filtering (Discovery, Prototype, Implementation, Utilities)
- Capability tagging (e.g., "personas", "compliance", "code generation", "testing")
- Related component suggestions ("See also: /discovery-multiagent")
- Search result ranking by relevance and usage frequency

**Traces to**: PP-1.3, JTBD-1.3, JTBD-1.4

**Success Criteria**:
- Search results appear within 2 seconds of typing query
- 95% of searches result in finding the correct tool within first 3 results
- Product managers can answer "can the framework do X?" within 30 seconds
- 60% reduction in Slack questions about "which tool should I use?"

---

### 3. Developer-Centric Extensibility
Empower developers to quickly customize and extend framework components by providing instant access to source files, clear contribution guidelines, and personalization features.

**Key Initiatives**:
- One-click file path copy for every skill/agent/command
- Full file paths shown in detail view (e.g., `.claude/skills/Discovery_JTBD/SKILL.md`)
- Favorites system for bookmarking frequently-used tools
- Contribution guidelines (when to fork vs. edit shared components)
- Code examples for advanced customization scenarios

**Traces to**: PP-1.5, PP-1.6, JTBD-1.5, JTBD-1.6

**Success Criteria**:
- Developers locate and open source files within 10 seconds (down from 10-15 minutes)
- 50% of active developers use favorites feature regularly
- 3x increase in framework contributions (PRs, custom agents shared with team)
- Developer satisfaction score > 85% for "ease of customization"

---

### 4. Contextual Confidence Building
Provide rich contextual information (examples, workflow diagrams, use case guidance, comparison tables) that enables users to confidently select and apply framework tools without fear of mistakes.

**Key Initiatives**:
- Multi-section detail pane with tabs: Purpose | Examples | Options | Workflow | Traceability
- Real-world usage examples showing command syntax, expected output, and common pitfalls
- Decision guidance for similar tools ("Use X when..., Use Y when...")
- Side-by-side comparison tables for related components
- Workflow diagrams clarifying when to use component in overall process

**Traces to**: PP-1.2, JTBD-1.2, JTBD-1.8, JTBD-2.1

**Success Criteria**:
- Every component has at least one real-world usage example
- Users can answer "when to use X vs Y" within 30 seconds
- User confidence score > 80% (measured by post-training survey)
- 70% reduction in framework misuse incidents

---

## Success Vision (2-Year Horizon)

In 2028, the ClaudeManual is the **de facto standard for interactive framework documentation** across HTEC and client organizations. Every new team member completes self-guided onboarding in under 2 hours, confidently running their first discovery or implementation workflow without assistance.

Product managers present framework capabilities to clients using the visual interface, instantly searching for compliance tools or prototype features and demonstrating examples in real-time. Developers customize agents and skills with a single click to copy file paths, reducing time-to-customization from 25 minutes to under 2 minutes.

The framework creator (Miloš) spends zero time on manual training sessions. Instead, he focuses on building new features and improving the framework itself. Slack questions about "how do I use this?" decrease by 80%, replaced by self-service exploration and peer knowledge sharing.

Framework adoption reaches 90%+ across teams. The ClaudeManual becomes a case study in how to transform complex technical systems into accessible, self-service platforms. Other framework creators inside and outside HTEC adopt the ClaudeManual approach for their own documentation.

**Quantitative Success Indicators**:
- Onboarding time: 16 hours → 2 hours (87.5% reduction)
- Time-to-first-successful-workflow: 1 week → 1 day (85% reduction)
- Trainer hours per team member: 3-4 hours → 0 hours (100% reduction)
- Framework adoption rate: 30% → 90% within 30 days of introduction
- Slack support questions: Baseline → -80% reduction
- Developer time-to-source-file: 10-15 minutes → 10 seconds (98% reduction)
- Framework contributions (PRs, custom agents): Baseline → +300%
- User confidence score: Unknown → 85%+
- User satisfaction (ease of navigation): Unknown → 85%+

**Qualitative Success Indicators**:
- Executives confidently present framework capabilities in client pitches
- Product managers independently run discovery workflows without developer support
- Developers contribute custom agents and share them with the team
- Framework creator shifts focus from training to feature development
- ClaudeManual cited in external case studies and conference talks

---

## Anti-Goals (What We Won't Do)

### 1. Build a Code Execution Environment
We will **not** provide in-browser command execution or sandboxed framework runtime. ClaudeManual is a **documentation and learning platform**, not a development environment. Users will still execute commands in their local Claude Code environment.

**Rationale**: Building a secure execution environment would require significant infrastructure investment, introduce security risks, and distract from the core learning mission. Users already have Claude Code installed - we don't need to replicate it.

### 2. Replace Source Files with a GUI Editor
We will **not** create a visual editor for modifying skills, agents, or commands. Users will copy file paths and edit source files in their preferred IDE (VSCode, Cursor, etc.).

**Rationale**: Developers prefer editing code in their own environments with familiar tools, version control, and extensions. A GUI editor would be slower, more limited, and less familiar than VSCode.

### 3. Become a Framework Management Platform
We will **not** build features for version control, deployment, team permissions, or multi-tenant framework management. ClaudeManual is a **read-only documentation interface**, not a framework administration tool.

**Rationale**: These features belong in git, CI/CD systems, and project management tools. Adding them would introduce complexity and distract from the core discoverability mission.

### 4. Support Non-Claude Frameworks
We will **not** attempt to become a generic documentation platform for any framework. ClaudeManual is purpose-built for the Claude AI-assisted development framework's specific structure (skills, commands, agents, stages).

**Rationale**: Trying to be generic would dilute focus and require abstraction layers that complicate the user experience. If other frameworks want similar documentation, they can fork ClaudeManual and adapt it.

### 5. Provide Framework Analytics or Usage Tracking
We will **not** track which users use which commands, how often they run workflows, or aggregate framework usage data across teams.

**Rationale**: Privacy concerns, infrastructure overhead, and unclear value proposition. Users want to learn the framework, not be monitored. If analytics are needed later, they should be opt-in and separate from the core documentation platform.

---

## Strategic Risks & Mitigation

### Risk 1: Low Adoption Due to Inertia
**Risk**: Team members continue asking questions on Slack instead of using ClaudeManual because old habits are hard to break.

**Mitigation**:
- Framework creator redirects Slack questions to ClaudeManual links ("Check ClaudeManual: [link]")
- Add ClaudeManual link to all command help text and error messages
- Include ClaudeManual tour in first-time user onboarding
- Gamify adoption: Badge for "completed self-guided onboarding"

### Risk 2: Maintenance Burden
**Risk**: ClaudeManual becomes outdated as framework evolves, requiring manual updates to documentation.

**Mitigation**:
- Auto-generate documentation from source file frontmatter (parse `.claude/skills/*/SKILL.md`)
- Build hot-reload capability to reflect framework changes instantly
- Version framework and ClaudeManual together (e.g., framework v3.0 → ClaudeManual v3.0)
- Use git hooks to trigger ClaudeManual updates when framework files change

### Risk 3: Feature Creep
**Risk**: Users request execution, editing, analytics, version control, and other features that bloat the product.

**Mitigation**:
- Strict adherence to Anti-Goals (reject scope expansion requests)
- User research focused on "learning and discovery" use cases only
- Product roadmap reviews every quarter to validate alignment with vision
- "No" is the default answer to new feature requests unless they directly support learning

---

## Alignment with Business Goals

### HTEC Enterprise Goals

**Goal 1: Accelerate Client Time-to-Market**
- **ClaudeManual Impact**: Faster framework adoption → teams deliver discovery, prototyping, and implementation faster → clients see results sooner
- **Metric**: Client project timeline reduction by 20-30% due to improved framework utilization

**Goal 2: Scale AI-Assisted Development Practice**
- **ClaudeManual Impact**: Self-service learning enables more teams to use framework → scales beyond Miloš's capacity → more projects use AI-assisted workflows
- **Metric**: Number of teams using framework increases from 3 → 15+ within 12 months

**Goal 3: Increase Framework ROI**
- **ClaudeManual Impact**: Higher adoption rate + faster learning → framework delivers value across more projects → ROI on framework investment increases
- **Metric**: Framework utilization rate (% of eligible projects using framework) increases from 30% → 80%+

**Goal 4: Establish Thought Leadership**
- **ClaudeManual Impact**: ClaudeManual becomes a case study for interactive framework documentation → HTEC presents at conferences → builds reputation as AI-assisted development leader
- **Metric**: 3+ external presentations/blog posts about ClaudeManual and framework approach

---

## User Type Coverage

### Primary User Types (Highest Impact)

**UT-001: Framework Creator/Maintainer** (Miloš)
- **Jobs Served**: JTBD-1.1 (self-service learning), JTBD-1.7 (visual navigation), JTBD-1.5 (source file editing)
- **Pains Addressed**: PP-1.1 (knowledge transfer complexity), PP-1.2 (contextual documentation)
- **Value Delivered**: Eliminates manual training sessions, scales knowledge transfer

**UT-002: Product People** (Ana)
- **Jobs Served**: JTBD-1.2 (component context), JTBD-1.3 (find relevant tools), JTBD-2.1 (feel confident)
- **Pains Addressed**: PP-1.3 (discoverability challenge), PP-1.4 (organizational chaos)
- **Value Delivered**: Independent framework usage, faster client discovery work

**UT-003: Developers** (Stefan)
- **Jobs Served**: JTBD-1.5 (edit source files), JTBD-1.6 (bookmark tools), JTBD-1.4 (stage filtering)
- **Pains Addressed**: PP-1.6 (developer friction), PP-1.5 (personalization)
- **Value Delivered**: 10-second access to source files, personalized workflow

### Secondary User Types

**UT-004: Build/Client Partners**
- **Jobs Served**: JTBD-1.3 (find tools), JTBD-3.1 (perceived competence)
- **Value Delivered**: Professional presentation of framework capabilities to clients

**UT-005: Business Developers**
- **Jobs Served**: JTBD-1.3 (find tools), JTBD-2.2 (autonomous exploration)
- **Value Delivered**: Quick capability lookups for sales conversations

**UT-006: Executives**
- **Jobs Served**: JTBD-1.1 (self-service learning), JTBD-1.7 (visual navigation)
- **Value Delivered**: High-level understanding of framework capabilities without technical deep-dive

---

## Traceability

### Pain Points Addressed
- **PP-1.1**: Knowledge Transfer Complexity (High severity) → Strategic Pillar 1 (Visual-First Learning)
- **PP-1.2**: Lack of Contextual Documentation (High severity) → Strategic Pillar 4 (Contextual Confidence)
- **PP-1.3**: Discoverability Challenge (Medium severity) → Strategic Pillar 2 (Intelligent Discovery)
- **PP-1.4**: Organizational Chaos (Medium severity) → Strategic Pillar 1 (Visual-First Learning)
- **PP-1.5**: Lack of Personalization (Low severity) → Strategic Pillar 3 (Developer Extensibility)
- **PP-1.6**: Developer Friction (Medium severity) → Strategic Pillar 3 (Developer Extensibility)

**Coverage**: 100% of identified pain points addressed by 4 strategic pillars

### Jobs-to-Be-Done Enabled
**P0 Jobs** (Critical):
- JTBD-1.1: Enable Self-Service Framework Learning → Strategic Pillar 1
- JTBD-1.2: Understand Framework Component Context → Strategic Pillar 4
- JTBD-1.7: Navigate Framework Hierarchies Visually → Strategic Pillar 1
- JTBD-2.1: Feel Confident Using the Framework → Strategic Pillar 4

**P1 Jobs** (Important):
- JTBD-1.3: Quickly Find Relevant Framework Tools → Strategic Pillar 2
- JTBD-1.4: Understand Which Tools Apply to Current Workflow Stage → Strategic Pillar 2
- JTBD-1.5: Edit Framework Source Files Efficiently → Strategic Pillar 3
- JTBD-1.8: Compare Similar Framework Components → Strategic Pillar 4
- JTBD-3.1: Be Perceived as Framework-Competent → Strategic Pillar 4

**P2 Jobs** (Nice-to-have):
- JTBD-1.6: Bookmark Frequently-Used Tools → Strategic Pillar 3
- JTBD-2.2: Feel Autonomous in Framework Exploration → Strategic Pillars 1 & 2
- JTBD-3.2: Contribute to Team Framework Efficiency → Strategic Pillar 3

**Coverage**: 100% of identified jobs (12/12) enabled by 4 strategic pillars

### User Types Served
- UT-001: Framework Creator/Maintainer → All 4 strategic pillars
- UT-002: Product People → Pillars 1, 2, 4
- UT-003: Developers → All 4 strategic pillars
- UT-004: Build/Client Partners → Pillars 1, 2, 4
- UT-005: Business Developers → Pillars 1, 2
- UT-006: Executives → Pillars 1, 4

**Coverage**: 100% of user types (6/6) served by strategic pillars

### Client Facts Foundation
- CF-003: "I want to have this very visual" → Strategic Pillar 1
- CF-006: Master-detail pane interface → Strategic Pillar 1
- CF-008: Multi-section documentation → Strategic Pillar 4
- CF-009: Search functionality → Strategic Pillar 2
- CF-010: Tagging system → Strategic Pillar 2
- CF-011: Stage-based organization → Strategic Pillars 1 & 2
- CF-012: Favorites concept → Strategic Pillar 3
- CF-013: File path references → Strategic Pillar 3
- CF-014: Modern minimalistic terminal look → Design language

**Coverage**: 9/16 client facts directly inform strategic pillars (remaining facts are technical constraints or UI preferences handled in design phase)

---

## Next Steps (Post-Vision)

1. **Requirements Definition** (CP-6): Translate strategic pillars into P0/P1/P2 functional requirements
2. **Strategy Document** (CP-7): Define go-to-market, phasing, MVP scope, success metrics
3. **Prototype Design** (Stage 2): Create interactive mockups of dual-pane interface, search, and detail pane
4. **Technical Validation**: Validate feasibility of auto-generating documentation from framework source files
5. **User Testing**: Test navigation and search with 5 users from each primary user type (creator, product person, developer)

---

*This vision document establishes the strategic foundation for transforming the Claude framework's documentation into an interactive, self-service learning platform. It directly addresses all 6 identified pain points, enables all 12 jobs-to-be-done, and serves all 6 user types through 4 strategic pillars focused on visual learning, intelligent discovery, developer extensibility, and contextual confidence building.*
