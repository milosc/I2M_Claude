# Screen Definitions - ClaudeManual

---
system_name: ClaudeManual
checkpoint: CP-9
total_screens: 11
date_created: 2026-01-31
session: disc-claude-manual-009a
created_by: discovery-screen-specifier
---

## Screen Inventory

| Screen ID | Screen Name | Priority | Phase | Primary JTBD | Target Personas |
|---|---|---|---|---|
| SCR-001 | Main Explorer View | P0 | MVP | JTBD-1.7, JTBD-1.1, JTBD-1.2 | PER-001, PER-002, PER-003 |
| SCR-002 | Search Results Page | P0 | MVP | JTBD-1.3, JTBD-2.2 | PER-002, PER-003 |
| SCR-003 | Stage-Filtered View | P1 | Phase 2 | JTBD-1.4 | PER-002, PER-003 |
| SCR-004 | Favorites Page | P1 | Phase 2 | JTBD-1.6 | PER-003 |
| SCR-005 | Comparison View | P1 | Phase 2 | JTBD-1.8 | PER-002, PER-003 |
| SCR-006 | Component Detail Modal | P0 | MVP | JTBD-1.2, JTBD-2.1 | All personas |
| SCR-007 | Settings Panel | P1 | Phase 2 | CF-016 | All personas |
| SCR-008 | Mobile Explorer View | P2 | Phase 3 | JTBD-3.1 | PER-002, PER-004 |
| SCR-009 | Workflow Viewer | P1 | Phase 2 | JTBD-1.9, JTBD-1.2 | All personas |
| SCR-010 | Architecture Browser | P1 | Phase 2 | JTBD-1.9, JTBD-1.2 | All personas |
| SCR-011 | Document Preview Modal | P1 | Phase 2 | JTBD-1.9, JTBD-1.2 | All personas |

---

## SCR-001: Main Explorer View

### Overview

- **Purpose**: Primary interface for framework exploration with dual-pane master-detail layout enabling self-service learning
- **Layout**: Dual-pane (master-detail) with collapsible navigation tree and tabbed detail content
- **JTBD**: JTBD-1.7 (Navigate hierarchies visually), JTBD-1.1 (Self-service learning), JTBD-1.2 (Component context)
- **User Types**: All (PER-001, PER-002, PER-003)
- **Entry Points**: Home page, direct URL, app launch
- **Exit Points**: Search page (SCR-002), Stage filter view (SCR-003), Favorites (SCR-004)

### Wireframe Description

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Header                                                                       │
│ ┌───────────┐ ┌────────────────────────┐ ┌──────┐ ┌────────┐ ┌─────────┐   │
│ │ Logo      │ │ Search Bar (Cmd+K)     │ │ Light│ │ Stage  │ │Favorites│   │
│ │ ClaudeMan │ │ "Search skills, cmds..." │ │ /Dark│ │ Filter │ │  (icon) │   │
│ └───────────┘ └────────────────────────┘ └──────┘ └────────┘ └─────────┘   │
├──────────────────────────────────┬───────────────────────────────────────────┤
│                                  │                                           │
│ Navigation Tree (Master Pane)    │ Detail Pane                               │
│ ────────────────────────────────│ ──────────────────────────────────────── │
│                                  │                                           │
│ ▼ Skills (85)              [i]   │ [Tabs: Purpose | Examples | Options |    │
│   ▼ Discovery (29)          ↓    │        Workflow | Traceability]          │
│     ├ Discovery_JTBD       ⭐    │                                           │
│     ├ Discovery_Persona         │ # Discovery_JTBD                          │
│     ├ Discovery_Vision          │                                           │
│     └ ...                        │ **Path**: `.claude/skills/Discovery_JTBD/ │
│   ▼ Prototype (14)               │ SKILL.md`                                │
│     ├ Prototype_DesignSystem     │ [Copy Path] [Add to Favorites]           │
│     ├ Prototype_CodeGenerator    │                                           │
│     └ ...                        │ ## Purpose                                │
│   ▼ ProductSpecs (10)            │ Extracts Jobs To Be Done from pain        │
│   ▼ Implementation (5)           │ points, client facts, and user research.  │
│   ▼ Security (10)                │ Generates structured JTBD document...     │
│   ▼ GRC (22)                     │                                           │
│                                  │ ## Example                                │
│ ▼ Commands (30)             [i]  │ ```bash                                   │
│   ├ /discovery                   │ # Invoke skill directly                   │
│   ├ /discovery-multiagent   ⭐   │ # Or via command orchestrator             │
│   ├ /prototype                   │ /discovery ClaudeManual Client_Materials  │
│   └ ...                          │ ```                                       │
│                                  │                                           │
│ ▼ Agents (25)               [i]  │ ## Options                                │
│   ▼ Discovery (6)                │ | Parameter | Type | Required | Default | │
│   ▼ Quality (4)                  │ |-----------|------|----------|----------│ │
│   └ ...                          │ | input_dir | Path | Yes      | -        | │
│                                  │                                           │
│ ▼ Rules (5)                 [i]  │ [Workflow Diagram Placeholder - Mermaid]  │
│                                  │                                           │
│ ▼ Hooks (8)                 [i]  │                                           │
│                                  │                                           │
│ [Collapse All] [Expand All]      │                                           │
│                                  │                                           │
├──────────────────────────────────┴───────────────────────────────────────────┤
│ Footer: Version 3.0.0 | Last Updated: 2026-01-31 | © HTEC Framework         │
└──────────────────────────────────────────────────────────────────────────────┘
```

### UI Components

| Component | Type | Behavior | UX Psychology Applied |
|---|---|---|---|
| **Navigation Tree** | Hierarchical tree view | Expand/collapse categories, click item to select, show count badges | **Cognitive Load Reduction**: Collapsed by default to prevent overwhelm. Count badges (e.g., "Skills (85)") provide scent of information without forcing users to expand every category. |
| **[i] Info Icons** | Tooltip trigger | Hover to show category description | **Progressive Disclosure**: Hide category descriptions until needed. Reduces visual clutter for frequent users while supporting newcomers. |
| **Search Bar** | Text input with autocomplete | Focus on Cmd+K, instant results dropdown | **Hicks Law**: Single search entry point reduces decision paralysis. Keyboard shortcut enables power users to avoid mouse navigation. |
| **Detail Pane Tabs** | Tabbed interface | Purpose (default), Examples, Options, Workflow, Traceability | **Progressive Disclosure**: Default to "Purpose" tab (most common need). Advanced users can access Options/Traceability without cluttering initial view. |
| **Copy Path Button** | Icon button | Click to copy file path to clipboard, show toast notification | **Friction Reduction (Developer UX)**: Single-click copy eliminates 10-15 minutes of manual file navigation (PP-1.6). |
| **Add to Favorites (⭐)** | Toggle button | Click to add/remove from favorites, persist to localStorage | **Personalization**: Reduces repeated search effort for frequently-used tools (JTBD-1.6). |
| **Stage Filter Dropdown** | Multi-select filter | Filter tree by Discovery, Prototype, Implementation, etc. | **Hicks Law**: Reduces visible choices from 115+ items to ~20-30 items per stage (JTBD-1.4). |
| **Light/Dark Theme Toggle** | Switch button | Toggle theme, persist preference, detect system preference | **Visual Comfort**: Reduces eye strain for extended documentation reading (CF-016). |

### States

| State | Condition | UI Behavior |
|---|---|---|
| **Default** | First load | Navigation tree collapsed except first category, first item selected, Purpose tab active |
| **Loading** | Fetching markdown content | Skeleton loader in detail pane, tree shows loading spinner |
| **Empty Selection** | No item clicked | Detail pane shows "Select a component to view details" placeholder |
| **Search Active** | User typing in search bar | Tree hidden, search results overlay visible |
| **Favorites Mode** | Favorites button clicked | Navigate to SCR-004 (Favorites Page) |
| **Stage Filtered** | Stage filter applied | Tree shows only matching items, count badges update |
| **Error** | Markdown parsing failure | Error message in detail pane with "Retry" button and fallback text |

### User Flows

#### Flow 1: Framework Creator Onboarding a New Team Member
1. Framework creator shares app URL with new team member
2. New team member opens app → sees Main Explorer View (SCR-001)
3. **UX Psychology - Cognitive Load**: Tree is collapsed by default to prevent overwhelm. User sees high-level categories (Skills, Commands, Agents) without 115+ items.
4. User expands "Skills" → sees categories (Discovery, Prototype, Implementation)
5. User expands "Discovery" → sees 29 discovery skills
6. User clicks "Discovery_JTBD" → detail pane updates with Purpose, Examples, Options
7. **UX Psychology - Progressive Disclosure**: Purpose tab shows "what this does" immediately. Advanced users can click "Options" or "Workflow" tabs if needed.
8. User clicks "Copy Path" → clipboard notification confirms copy → user opens file in VSCode
9. **Success Metric**: User completes onboarding exploration in 30-60 minutes vs. 3-4 hours manual training (JTBD-1.1)

#### Flow 2: Product Manager Finding Discovery Tools for New Project
1. Product manager (PER-002) needs persona generation tools for healthcare project
2. Opens app → sees Main Explorer View (SCR-001)
3. Clicks "Stage Filter" dropdown → selects "Discovery"
4. **UX Psychology - Hicks Law**: Tree now shows only Discovery skills/commands/agents (reduces 115+ items to ~40 items)
5. Scrolls through Discovery skills → clicks "Discovery_GeneratePersona"
6. Detail pane shows Purpose: "Generates persona documents from interview transcripts"
7. Clicks "Examples" tab → sees command syntax and expected output
8. **UX Psychology - Confidence Building**: Real-world example reduces uncertainty about correct usage (JTBD-2.1)
9. User copies command, runs it in terminal, generates personas successfully
10. **Success Metric**: Time to find tool reduced from 20-30 minutes (manual folder browsing) to 2-3 minutes (JTBD-1.3)

#### Flow 3: Developer Bookmarking Frequently-Used Tools
1. Developer (PER-003) uses TDD implementation skills daily
2. Opens app → navigates to "Skills → Implementation → Implementation_Developer"
3. Clicks "Add to Favorites" (⭐) → item added to favorites list
4. Repeats for "quality-security-auditor" agent and "/htec-sdd-implement" command
5. Clicks "Favorites" icon in header → navigates to SCR-004 (Favorites Page)
6. **UX Psychology - Personalization**: Favorites reduce repeated search from 5+ searches/week to 0 searches (JTBD-1.6)
7. Future sessions: User clicks "Favorites" → instant access to bookmarked tools
8. **Success Metric**: 60%+ of developers have 3+ favorites within 4 weeks (Phase 2 success criteria)

### Acceptance Criteria

- [ ] Navigation tree displays all 115+ skills, 30+ commands, 25+ agents, 5+ rules, 8+ hooks
- [ ] Tree supports expand/collapse with visual indentation (2-level hierarchy minimum)
- [ ] Clicking item updates detail pane within 200ms
- [ ] Detail pane renders markdown with syntax highlighting for code blocks
- [ ] Copy Path button copies full file path to clipboard with toast notification
- [ ] Add to Favorites toggles favorite status and persists to localStorage
- [ ] Search bar triggers SCR-002 (Search Results Page) on input
- [ ] Stage Filter dropdown filters tree items by selected stages
- [ ] Theme toggle switches between light/dark mode and persists preference
- [ ] Keyboard shortcut Cmd+K focuses search bar
- [ ] Tree count badges show accurate item counts (e.g., "Skills (85)")
- [ ] Responsive layout: master pane collapses to drawer on mobile (<768px)

### UX Psychology Summary

| Principle | Application | User Benefit |
|---|---|---|
| **Hicks Law (Simplify Choices)** | Collapsed tree by default, stage filtering reduces visible items from 115+ to ~20-30 | Reduces decision paralysis, faster tool discovery (JTBD-1.3, JTBD-1.4) |
| **Cognitive Load Reduction** | Progressive disclosure via tabs (Purpose → Examples → Options), info icons for category descriptions | Users see only what they need, reducing mental effort (PP-1.2, JTBD-1.2) |
| **Progressive Disclosure** | Advanced tabs (Options, Workflow, Traceability) hidden by default, tree categories collapsed | Newcomers not overwhelmed, power users can access deep details (JTBD-2.1) |
| **Visual Cues** | Count badges, ⭐ favorites icon, [i] info icons, stage color-coding | Faster navigation, clearer mental model (JTBD-1.7) |

### Traceability

- **Addresses Pain Points**: PP-1.1 (Knowledge Transfer), PP-1.2 (Contextual Documentation), PP-1.4 (Organizational Chaos), PP-1.6 (Developer Friction)
- **Enables JTBD**: JTBD-1.1, JTBD-1.2, JTBD-1.7, JTBD-2.1, JTBD-2.2
- **Client Facts**: CF-006 (Dual-pane), CF-008 (Multi-section detail), CF-013 (File paths), CF-014 (Minimalistic terminal look)
- **Roadmap Features**: F-001 (Master-detail UI), F-002 (Hierarchical navigation), F-004 (Multi-section detail pane), F-006 (File path references), F-017 (Light/dark theme)

---

## SCR-002: Search Results Page

### Overview

- **Purpose**: Instant keyword search across all framework components with relevance ranking
- **Layout**: Full-width search results with filters and preview cards
- **JTBD**: JTBD-1.3 (Find relevant tools quickly), JTBD-2.2 (Autonomous exploration)
- **User Types**: PER-002 (Product People), PER-003 (Developers)
- **Entry Points**: Search bar in SCR-001 header, Cmd+K keyboard shortcut
- **Exit Points**: Click result → navigates to SCR-001 with item selected, Back to Explorer button

### Wireframe Description

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Header (Same as SCR-001)                                                     │
│ ┌───────────┐ ┌────────────────────────┐ ┌──────┐ ┌────────┐ ┌─────────┐   │
│ │ Logo      │ │ [Active: "persona"]    │ │ Light│ │ Stage  │ │Favorites│   │
│ └───────────┘ └────────────────────────┘ └──────┘ └────────┘ └─────────┘   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ [← Back to Explorer]                                                         │
│                                                                              │
│ Search Results for "persona" (12 results in <0.8s)                           │
│                                                                              │
│ Filters: [All Types ▾] [All Stages ▾] [Sort: Relevance ▾]                   │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐  │
│ │ ⭐ Discovery_GeneratePersona                          [Skill] [Discovery]│  │
│ │ Generates rich persona documents from interview transcripts...          │  │
│ │ Path: .claude/skills/Discovery_GeneratePersona/SKILL.md                 │  │
│ │ [View Details] [Copy Path] [Add to Favorites]                           │  │
│ └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐  │
│ │ discovery-persona-synthesizer                       [Agent] [Discovery] │  │
│ │ Multi-agent coordinator for persona synthesis from pain points...       │  │
│ │ Path: .claude/agents/discovery/persona-synthesizer.md                   │  │
│ │ [View Details] [Copy Path] [Add to Favorites]                           │  │
│ └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐  │
│ │ PERSONA_Framework_Creator.md                        [Example] [Client] │  │
│ │ Example persona document for framework creator (Miloš)...               │  │
│ │ Path: ClientAnalysis_ClaudeManual/02-research/personas/...              │  │
│ │ [View Details] [Copy Path]                                              │  │
│ └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│ ... (9 more results)                                                         │
│                                                                              │
│ [Load More Results]                                                          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### UI Components

| Component | Type | Behavior | UX Psychology Applied |
|---|---|---|---|
| **Search Input** | Text field (autofocus) | Real-time results as user types (debounced 300ms) | **Instant Feedback**: Results appear within 2 seconds of typing (JTBD-1.3 success criteria). Reduces uncertainty. |
| **Result Cards** | Clickable cards | Preview title, description, path, metadata (type, stage) | **Cognitive Load**: One-sentence summary visible without clicking (PP-1.2). Users scan quickly. |
| **Filters** | Dropdown menus | Type (Skill/Command/Agent), Stage (Discovery/Prototype/etc.), Sort (Relevance/Alphabetical) | **Hicks Law**: Reduce results from 115+ to ~10-20 by filtering. Prevents overwhelming choice. |
| **Performance Indicator** | Text label | "12 results in <0.8s" shown after search completes | **Confidence Building**: Fast results validate tool responsiveness (JTBD-2.1). |
| **Copy Path Button** | Icon button | Same as SCR-001, copies path to clipboard | **Developer UX**: One-click access to source file (PP-1.6). |
| **View Details Button** | Link button | Navigates to SCR-001 with item selected and detail pane open | **Progressive Disclosure**: Users decide if preview is enough or if they need full documentation. |

### States

| State | Condition | UI Behavior |
|---|---|---|
| **Empty Query** | No search text entered | Show placeholder: "Type to search skills, commands, agents, or rules..." |
| **Loading** | Search executing | Show skeleton cards, "Searching..." indicator |
| **Results Found** | Query matches items | Display result cards with filters and sort options |
| **No Results** | Query returns 0 matches | "No results for '[query]'. Try different keywords or browse by stage." |
| **Filtered Results** | User applies type/stage filter | Update result count and cards, maintain scroll position |
| **Error** | Search engine failure | "Search temporarily unavailable. Try browsing by category instead." |

### User Flows

#### Flow 1: Product Manager Searching for GDPR Compliance Tools
1. Product manager (PER-002) needs GDPR compliance tools for healthcare project
2. Opens app → presses Cmd+K → search bar focuses
3. Types "GDPR" → results appear in <1 second
4. **UX Psychology - Instant Feedback**: Results show immediately, reducing uncertainty
5. Sees 5 results: "GRC_gdpr-dsgvo-expert" (skill), "/grc-assess-gdpr" (command), "compliance-analyst" (agent)
6. Clicks "Type: Skill" filter → narrows to 2 skill results
7. Clicks "GRC_gdpr-dsgvo-expert" → navigates to SCR-001 with skill selected
8. Reads Purpose tab → understands this skill handles DPIA, data subject rights, lawful basis
9. Clicks "Copy Path" → opens file in VSCode → customizes for healthcare context
10. **Success Metric**: Found GDPR tool in 2 minutes vs. 30+ minutes of manual folder browsing (JTBD-1.3)

#### Flow 2: Developer Searching for TDD Implementation Tools
1. Developer (PER-003) needs test automation tools
2. Opens app → types "TDD" in search bar
3. Sees 8 results: "Implementation_Developer" (skill), "/htec-sdd-implement" (command), "test-automation-engineer" (agent)
4. Applies "Stage: Implementation" filter → narrows to 5 results
5. **UX Psychology - Hicks Law**: Filtering reduces choices from 8 to 5, making decision easier
6. Clicks "test-automation-engineer" agent → views detail pane
7. Reads Examples tab → sees code for running Vitest tests
8. Clicks "Add to Favorites" → bookmarks for future use
9. **Success Metric**: Developer adds 3+ tools to favorites within first week (JTBD-1.6)

### Acceptance Criteria

- [ ] Search returns results within 2 seconds of query (JTBD-1.3 success criteria)
- [ ] Search indexes skill/command/agent names, descriptions, and frontmatter tags
- [ ] Results show title, one-sentence summary, file path, type badge, stage badge
- [ ] Type filter includes: All, Skill, Command, Agent, Rule, Hook
- [ ] Stage filter includes: All, Discovery, Prototype, ProductSpecs, SolArch, Implementation, Utility
- [ ] Sort options: Relevance (default), Alphabetical A-Z, Recently Updated
- [ ] Fuzzy search tolerates typos (e.g., "personna" matches "persona")
- [ ] Empty query state shows helpful placeholder text
- [ ] No results state suggests alternative actions (browse by stage)
- [ ] Back to Explorer button returns to SCR-001 with previous selection preserved
- [ ] Keyboard navigation: Arrow keys to select results, Enter to view details

### UX Psychology Summary

| Principle | Application | User Benefit |
|---|---|---|
| **Instant Feedback** | Results appear in <2 seconds, performance indicator shown | Reduces uncertainty, builds confidence (JTBD-2.1) |
| **Hicks Law** | Filters reduce visible choices from 115+ to ~10-20 | Faster decision-making, less overwhelm (JTBD-1.3) |
| **Cognitive Load** | One-sentence summaries in cards prevent needing to click every result | Users scan efficiently, save time (PP-1.2) |
| **Progressive Disclosure** | Preview in cards → full details on click → deep dive in tabs | Users control information depth (JTBD-2.2) |

### Traceability

- **Addresses Pain Points**: PP-1.3 (Discoverability Challenge), PP-1.2 (Contextual Documentation)
- **Enables JTBD**: JTBD-1.3 (Find relevant tools), JTBD-2.2 (Autonomous exploration)
- **Client Facts**: CF-009 (Search page requirement), CF-010 (Tagging system)
- **Roadmap Features**: F-005 (Basic search), F-007 (Search results ranking)

---

## SCR-003: Stage-Filtered View

### Overview

- **Purpose**: Show only tools relevant to current workflow stage (Discovery, Prototype, Implementation, etc.)
- **Layout**: Same dual-pane layout as SCR-001, but with filtered navigation tree
- **JTBD**: JTBD-1.4 (Understand stage-appropriate tools)
- **User Types**: PER-002 (Product People), PER-003 (Developers), PER-006 (Executives)
- **Entry Points**: Stage Filter dropdown in SCR-001 header, stage landing pages
- **Exit Points**: Clear filter → returns to SCR-001, Search → navigates to SCR-002

### Wireframe Description

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Header                                                                       │
│ ┌───────────┐ ┌────────────────────────┐ ┌──────┐ ┌────────────────┐       │
│ │ Logo      │ │ Search Bar             │ │Theme │ │Stage: Discovery│ ← ACTIVE│
│ └───────────┘ └────────────────────────┘ └──────┘ └────────────────┘       │
├──────────────────────────────────┬───────────────────────────────────────────┤
│ Active Filter: Discovery         │ Detail Pane                               │
│ [Clear Filter]                   │                                           │
│                                  │ [Tabs: Purpose | Examples | Options]      │
│ ────────────────────────────────│                                           │
│                                  │ # Discovery_JTBD                          │
│ Showing 40 of 115 components     │                                           │
│                                  │ **Stage**: Discovery                      │
│ ▼ Skills (29)               [i]  │ **Path**: `.claude/skills/...`            │
│   ├ Discovery_JTBD          ⭐   │                                           │
│   ├ Discovery_Persona            │ ## Purpose                                │
│   ├ Discovery_Vision             │ Extracts Jobs To Be Done from validated  │
│   └ ... (26 more)                │ pain points and client facts...           │
│                                  │                                           │
│ ▼ Commands (8)              [i]  │ ## Workflow Context                       │
│   ├ /discovery                   │ **When to use**: After pain point         │
│   ├ /discovery-multiagent   ⭐   │ extraction (CP-4), before vision strategy│
│   ├ /discovery-audit             │ definition (CP-6).                        │
│   └ ... (5 more)                 │                                           │
│                                  │ **Inputs Required**: pain_points.md,      │
│ ▼ Agents (6)                [i]  │ client_facts_registry.json                │
│   ├ discovery-domain-researcher  │                                           │
│   ├ discovery-jtbd-extractor     │                                           │
│   └ ... (4 more)                 │                                           │
│                                  │                                           │
│ [Collapse All] [Expand All]      │                                           │
│                                  │                                           │
├──────────────────────────────────┴───────────────────────────────────────────┤
│ Footer: Filtered View | 40 Discovery Components | Version 3.0.0             │
└──────────────────────────────────────────────────────────────────────────────┘
```

### UI Components

| Component | Type | Behavior | UX Psychology Applied |
|---|---|---|
| **Stage Filter Dropdown** | Multi-select dropdown | Select one or more stages, updates tree in real-time | **Hicks Law**: Reduces visible items from 115+ to ~20-40 per stage. Decision paralysis eliminated. |
| **Active Filter Indicator** | Text label + badge | Shows "Active Filter: Discovery" with stage color-coding | **Visual Clarity**: Users always know context (JTBD-1.4). |
| **Clear Filter Button** | Link button | Removes all filters, returns to full tree view | **Escape Hatch**: Users can reset if filter is too narrow. |
| **Item Count Badge** | Numeric badge | "Showing 40 of 115 components" updates dynamically | **Transparency**: Users understand scope of filter impact. |
| **Workflow Context Panel** | Collapsible section in detail pane | Shows "When to use this stage", inputs required, outputs produced | **Contextual Learning**: Users understand stage relationships (JTBD-1.4, JTBD-2.1). |

### States

| State | Condition | UI Behavior |
|---|---|---|
| **Single Stage Filtered** | One stage selected (e.g., Discovery) | Tree shows only skills/commands/agents tagged with that stage |
| **Multi-Stage Filtered** | Multiple stages selected (e.g., Discovery + Prototype) | Tree shows items from any selected stage |
| **No Filter** | No stage selected | Same as SCR-001 (full tree visible) |
| **Empty Filter Result** | Selected stage has 0 items | "No components found for this stage. Try clearing the filter." |

### User Flows

#### Flow 1: Product Manager Finding Discovery Tools
1. Product manager (PER-002) starting client discovery project
2. Opens app → sees 115+ components (overwhelming)
3. Clicks "Stage Filter" dropdown → selects "Discovery"
4. **UX Psychology - Hicks Law**: Tree collapses to 40 items (29 skills, 8 commands, 6 agents)
5. User scans collapsed categories → expands "Skills (29)"
6. **UX Psychology - Cognitive Load**: Smaller list is easier to scan and understand
7. Clicks "Discovery_JTBD" → detail pane shows "Workflow Context" section
8. Reads "When to use: After pain point extraction (CP-4)"
9. User understands where this tool fits in workflow (JTBD-1.4)
10. **Success Metric**: User can identify relevant tools without developer assistance (JTBD-2.2)

### Acceptance Criteria

- [ ] Stage filter dropdown includes: Discovery, Prototype, ProductSpecs, SolArch, Implementation, Utilities, Security, GRC
- [ ] Selecting stage filters tree to show only matching items
- [ ] Count badges update to show filtered counts (e.g., "Skills (29 of 85)")
- [ ] Detail pane shows "Workflow Context" section for stage-specific tools
- [ ] Clear filter button resets to full tree view
- [ ] Multi-select allows combining stages (e.g., Discovery + Prototype)
- [ ] Filter persists across sessions (localStorage)

### UX Psychology Summary

| Principle | Application | User Benefit |
|---|---|---|
| **Hicks Law** | Filtering reduces choices from 115+ to 20-40 | Faster tool discovery, less overwhelm (JTBD-1.4) |
| **Cognitive Load** | Smaller item lists, contextual "When to use" guidance | Users understand workflow stage relationships (PP-1.4) |
| **Visual Cues** | Stage color-coding, active filter indicator | Clear mental model of current context (JTBD-1.4) |

### Traceability

- **Addresses Pain Points**: PP-1.4 (Organizational Chaos)
- **Enables JTBD**: JTBD-1.4 (Stage-appropriate tools)
- **Client Facts**: CF-011 (Stage-based organization)
- **Roadmap Features**: F-008 (Stage-based filters), F-009 (Stage badges), F-010 (Stage landing pages)

---

## SCR-004: Favorites Page

### Overview

- **Purpose**: Quick access panel for bookmarked frequently-used tools
- **Layout**: Grid view of favorited items with drag-and-drop reordering
- **JTBD**: JTBD-1.6 (Bookmark tools)
- **User Types**: PER-003 (Developers), PER-001 (Framework Creators)
- **Entry Points**: Favorites icon in header, keyboard shortcut Cmd+B
- **Exit Points**: Click item → navigates to SCR-001 with item selected

### Wireframe Description

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Header (Same as SCR-001)                                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ [← Back to Explorer]                                                         │
│                                                                              │
│ My Favorites (5 items)                                           [Clear All] │
│                                                                              │
│ ┌─────────────────────────┐ ┌─────────────────────────┐ ┌────────────────┐ │
│ │ ⭐ Discovery_JTBD        │ │ ⭐ /htec-sdd-implement   │ │ ⭐ quality-    │ │
│ │ [Skill] [Discovery]     │ │ [Command] [Implement]   │ │ security-auditor│ │
│ │                         │ │                         │ │ [Agent] [Quality]│ │
│ │ Extracts Jobs To Be...  │ │ TDD implementation...   │ │ Security checks...│ │
│ │                         │ │                         │ │                │ │
│ │ [View] [Copy Path] [×]  │ │ [View] [Copy Path] [×]  │ │ [View] [×]     │ │
│ └─────────────────────────┘ └─────────────────────────┘ └────────────────┘ │
│                                                                              │
│ ┌─────────────────────────┐ ┌─────────────────────────┐                     │
│ │ ⭐ Prototype_DesignSystem│ │ ⭐ /discovery-multiagent │                     │
│ │ [Skill] [Prototype]     │ │ [Command] [Discovery]   │                     │
│ │                         │ │                         │                     │
│ │ Generates design tokens │ │ Multi-agent discovery   │                     │
│ │                         │ │ 60% faster...           │                     │
│ │ [View] [Copy Path] [×]  │ │ [View] [Copy Path] [×]  │                     │
│ └─────────────────────────┘ └─────────────────────────┘                     │
│                                                                              │
│ Drag to reorder favorites                                                   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### UI Components

| Component | Type | Behavior | UX Psychology Applied |
|---|---|---|
| **Favorites Grid** | Responsive grid (3 columns desktop, 1 mobile) | Click card to view details, drag to reorder | **Personalization**: Users control layout, reducing search time (JTBD-1.6). |
| **Remove Button (×)** | Icon button | Removes item from favorites with confirmation toast | **Low-stakes Actions**: Easy to add/remove without fear of permanent loss. |
| **Clear All Button** | Destructive action button | Removes all favorites with confirmation modal | **Safety**: Confirmation prevents accidental data loss. |
| **Drag Handles** | Visual indicator | Shows 6-dot drag handle on hover | **Discoverability**: Visual cue that cards are reorderable. |

### States

| State | Condition | UI Behavior |
|---|---|---|
| **Empty Favorites** | No items bookmarked | "No favorites yet. Click ⭐ on any component to add it here." |
| **Populated** | 1+ items bookmarked | Show grid of favorite cards with reorder capability |
| **Reordering** | User dragging card | Show drop zones, update order on drop, persist to localStorage |

### User Flows

#### Flow 1: Developer Creating Personal Toolkit
1. Developer (PER-003) uses TDD tools daily
2. Over first week, bookmarks 5 tools: "Implementation_Developer", "/htec-sdd-implement", "quality-security-auditor", "test-automation-engineer", "GRC_gdpr-dsgvo-expert"
3. Presses Cmd+B → opens Favorites page (SCR-004)
4. **UX Psychology - Personalization**: Sees 5 bookmarked items in grid layout
5. Drags "/htec-sdd-implement" to top position (most frequently used)
6. Clicks "Copy Path" on "quality-security-auditor" → copies path → opens in VSCode
7. **Success Metric**: Developer reduces tool search time from 5+ searches/week to 0 (JTBD-1.6)
8. **Phase 2 Success Criteria**: 60%+ of developers have 3+ favorites within 12 weeks

### Acceptance Criteria

- [ ] Favorites persist to localStorage across sessions
- [ ] Grid layout: 3 columns on desktop, 2 on tablet, 1 on mobile
- [ ] Drag-and-drop reordering with smooth animations
- [ ] Remove button removes item with toast notification
- [ ] Clear All button shows confirmation modal before deleting all
- [ ] Empty state shows helpful message with ⭐ icon
- [ ] Clicking card navigates to SCR-001 with item selected
- [ ] Keyboard shortcut Cmd+B opens favorites page

### UX Psychology Summary

| Principle | Application | User Benefit |
|---|---|---|
| **Personalization** | User-controlled bookmarks and ordering | Reduces repeated search effort (JTBD-1.6) |
| **Low-stakes Actions** | Easy add/remove, confirmation for destructive actions | Users feel confident customizing (JTBD-2.2) |
| **Visual Cues** | Drag handles, ⭐ icons | Clear affordances for interaction |

### Traceability

- **Addresses Pain Points**: PP-1.5 (Lack of Personalization)
- **Enables JTBD**: JTBD-1.6 (Bookmark tools)
- **Client Facts**: CF-012 (Favorites feature)
- **Roadmap Features**: F-015 (Favorites system), F-016 (Favorites sidebar)

---

## SCR-005: Comparison View

### Overview

- **Purpose**: Side-by-side comparison of similar tools with decision guidance
- **Layout**: Two-column table comparing features, performance, use cases
- **JTBD**: JTBD-1.8 (Compare similar components)
- **User Types**: PER-002 (Product People), PER-003 (Developers)
- **Entry Points**: "Compare" button in detail pane (when related components exist)
- **Exit Points**: Select tool → navigates to SCR-001, Back button

### Wireframe Description

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Header (Same as SCR-001)                                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ [← Back to Explorer]                                                         │
│                                                                              │
│ Comparison: /discovery vs /discovery-multiagent                             │
│                                                                              │
│ ┌─────────────────────────────────┬─────────────────────────────────────┐   │
│ │ /discovery                      │ /discovery-multiagent               │   │
│ │ [Command] [Discovery]           │ [Command] [Discovery]               │   │
│ ├─────────────────────────────────┼─────────────────────────────────────┤   │
│ │ **Execution Model**             │                                     │   │
│ │ Sequential orchestrator         │ Parallel multi-agent (12 agents)    │   │
│ ├─────────────────────────────────┼─────────────────────────────────────┤   │
│ │ **Performance**                 │                                     │   │
│ │ 50-60 minutes (20 deliverables) │ 18-22 minutes (60-70% faster) ✓     │   │
│ ├─────────────────────────────────┼─────────────────────────────────────┤   │
│ │ **Reliability**                 │                                     │   │
│ │ Higher (single-thread, no coord)│ Medium (agent coordination needed)  │   │
│ ├─────────────────────────────────┼─────────────────────────────────────┤   │
│ │ **Use When**                    │                                     │   │
│ │ - First-time users              │ - Experienced users                 │   │
│ │ - Small projects (<10 interviews)│ - Large projects (10+ interviews)  │   │
│ │ - Simplicity over speed         │ - Speed critical                    │   │
│ ├─────────────────────────────────┼─────────────────────────────────────┤   │
│ │ **Tradeoffs**                   │                                     │   │
│ │ ✓ Easier to debug               │ ✗ Complex debugging (12 agents)     │   │
│ │ ✗ Slower                        │ ✓ 60-70% faster                     │   │
│ │ ✓ Lower memory usage            │ ✗ Higher memory (parallel agents)   │   │
│ └─────────────────────────────────┴─────────────────────────────────────┘   │
│                                                                              │
│ **Recommendation**: For your first discovery project, use /discovery to     │
│ learn the workflow. Switch to /discovery-multiagent for production projects.│
│                                                                              │
│ [Select /discovery] [Select /discovery-multiagent]                          │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### UI Components

| Component | Type | Behavior | UX Psychology Applied |
|---|---|---|
| **Comparison Table** | Two-column responsive table | Highlights key differences (✓ checkmarks, ✗ marks) | **Cognitive Load**: Visual comparison easier than reading two separate docs (JTBD-1.8). |
| **Decision Guidance** | Recommendation panel | Shows "Use X when..., Use Y when..." with user context | **Confidence Building**: Reduces decision paralysis (JTBD-2.1). |
| **Select Button** | Primary action button | Navigates to SCR-001 with selected tool in detail pane | **Clear CTA**: Single-click decision after comparison. |

### States

| State | Condition | UI Behavior |
|---|---|---|
| **Two-Item Comparison** | Default | Show side-by-side table with recommendation |
| **Multi-Item Comparison** | Future enhancement | Allow 3+ items in carousel layout |

### User Flows

#### Flow 1: Product Manager Choosing Between Discovery Commands
1. Product manager (PER-002) preparing for client project
2. Opens "/discovery" command → detail pane shows "Related: /discovery-multiagent"
3. Clicks "Compare" button → navigates to SCR-005
4. **UX Psychology - Cognitive Load Reduction**: Table format easier than reading two separate docs
5. Reads "Performance" row → sees "/discovery-multiagent is 60-70% faster"
6. Reads "Use When" row → sees "First-time users → /discovery"
7. **UX Psychology - Decision Guidance**: Clear recommendation based on user context (JTBD-2.1)
8. User selects "/discovery" (first project, simplicity preferred)
9. **Success Metric**: Decision made in 2 minutes vs. 10+ minutes of trial-and-error (JTBD-1.8)

### Acceptance Criteria

- [ ] Comparison view supports 2 similar components
- [ ] Table rows: Execution Model, Performance, Reliability, Use When, Tradeoffs
- [ ] Visual indicators: ✓ for advantages, ✗ for disadvantages
- [ ] Recommendation panel shows context-aware guidance
- [ ] Select buttons navigate to SCR-001 with chosen item selected
- [ ] Related components automatically linked in detail pane

### UX Psychology Summary

| Principle | Application | User Benefit |
|---|---|---|
| **Cognitive Load** | Side-by-side table vs. reading two docs | Faster decision-making (JTBD-1.8) |
| **Decision Guidance** | "Use X when..." recommendations | Reduces uncertainty (JTBD-2.1) |
| **Visual Cues** | ✓ and ✗ indicators | Quick scanning of tradeoffs |

### Traceability

- **Addresses Pain Points**: PP-1.2 (Lack of Contextual Documentation)
- **Enables JTBD**: JTBD-1.8 (Compare components), JTBD-2.1 (Confidence)
- **Roadmap Features**: F-013 (Related components), F-014 (Side-by-side comparison), F-020 (Decision guidance)

---

## SCR-006: Component Detail Modal

### Overview

- **Purpose**: Full-screen modal for deep-dive into component documentation
- **Layout**: Tabbed interface with sticky header and scrollable content
- **JTBD**: JTBD-1.2 (Understand component context), JTBD-2.1 (Confidence)
- **User Types**: All personas
- **Entry Points**: Click "View Details" in search results, comparison view, favorites
- **Exit Points**: Close button, Esc key

### Wireframe Description

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────────────────────┐  │
│ │ [×]                              Discovery_JTBD                     [⭐]│  │
│ ├─────────────────────────────────────────────────────────────────────────┤  │
│ │ [Purpose] [Examples] [Options] [Workflow] [Traceability]               │  │
│ ├─────────────────────────────────────────────────────────────────────────┤  │
│ │                                                                         │  │
│ │ # Discovery_JTBD                                                        │  │
│ │                                                                         │  │
│ │ **Path**: `.claude/skills/Discovery_JTBD/SKILL.md`                     │  │
│ │ [Copy Path to Clipboard]                                               │  │
│ │                                                                         │  │
│ │ ## Purpose                                                              │  │
│ │ Extracts Jobs To Be Done from validated pain points and client facts.  │  │
│ │ Generates structured JTBD document with functional, emotional, and     │  │
│ │ social jobs following When/Want/So-that format.                        │  │
│ │                                                                         │  │
│ │ ## When to Use                                                          │  │
│ │ **Workflow Stage**: Discovery (Checkpoint 4)                            │  │
│ │ **Prerequisites**: Pain points extracted (CP-2), client facts validated│  │
│ │ **Outputs**: JOBS_TO_BE_DONE.md, jtbd_registry.json                    │  │
│ │                                                                         │  │
│ │ ## Example Usage                                                        │  │
│ │ ```bash                                                                 │  │
│ │ # Invoke via Discovery orchestrator                                    │  │
│ │ /discovery ClaudeManual Client_Materials/                              │  │
│ │ ```                                                                     │  │
│ │                                                                         │  │
│ │ [Workflow Diagram - Mermaid]                                            │  │
│ │                                                                         │  │
│ │ ... (scrollable content)                                                │  │
│ │                                                                         │  │
│ └─────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### UI Components

| Component | Type | Behavior | UX Psychology Applied |
|---|---|---|
| **Tabbed Navigation** | Tab bar (sticky header) | Switch between Purpose/Examples/Options/Workflow/Traceability | **Progressive Disclosure**: Default to Purpose, advanced users access Options/Traceability (JTBD-1.2). |
| **Workflow Diagram** | Mermaid rendering | Shows visual workflow with input/output relationships | **Visual Learning**: Diagrams clarify complex workflows (CF-008, JTBD-2.1). |
| **Code Blocks** | Syntax-highlighted pre tags | Copy-to-clipboard button on hover | **Developer UX**: Easy command copying (PP-1.6). |

### Acceptance Criteria

- [ ] Modal opens in full-screen overlay with backdrop
- [ ] Tabs: Purpose (default), Examples, Options, Workflow, Traceability
- [ ] Workflow tab renders Mermaid diagrams if defined in markdown
- [ ] Code blocks have syntax highlighting and copy buttons
- [ ] Esc key or Close button dismisses modal
- [ ] Mobile: Modal takes 100% viewport height with scrollable content

### UX Psychology Summary

| Principle | Application | User Benefit |
|---|---|---|
| **Progressive Disclosure** | Tabbed interface hides advanced sections | Users see only what they need (JTBD-1.2) |
| **Visual Learning** | Workflow diagrams supplement text | Builds confidence in tool usage (JTBD-2.1) |

### Traceability

- **Addresses Pain Points**: PP-1.2 (Contextual Documentation)
- **Enables JTBD**: JTBD-1.2 (Component context), JTBD-2.1 (Confidence)
- **Client Facts**: CF-008 (Multi-section documentation)
- **Roadmap Features**: F-004 (Multi-section detail pane), F-018 (Workflow diagrams), F-019 (Usage examples)

---

## SCR-007: Settings Panel

### Overview

- **Purpose**: User preferences (theme, display options, keyboard shortcuts)
- **Layout**: Drawer panel from right side
- **JTBD**: CF-016 (Light/dark theme)
- **User Types**: All personas
- **Entry Points**: Settings icon in header
- **Exit Points**: Close button, click outside drawer

### Wireframe Description

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                 [Settings ⚙]│
│                                                                              │
│                                                   ┌──────────────────────┐   │
│                                                   │ Settings             │   │
│                                                   ├──────────────────────┤   │
│                                                   │ **Theme**            │   │
│                                                   │ ○ Light              │   │
│                                                   │ ● Dark               │   │
│                                                   │ ○ System             │   │
│                                                   │                      │   │
│                                                   │ **Display**          │   │
│                                                   │ ☑ Show file paths    │   │
│                                                   │ ☑ Show count badges  │   │
│                                                   │ ☐ Compact mode       │   │
│                                                   │                      │   │
│                                                   │ **Keyboard**         │   │
│                                                   │ Cmd+K: Search        │   │
│                                                   │ Cmd+B: Favorites     │   │
│                                                   │ Esc: Close modals    │   │
│                                                   │                      │   │
│                                                   │ [Reset to Defaults]  │   │
│                                                   └──────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Theme options: Light, Dark, System (auto-detect)
- [ ] Theme preference persists to localStorage
- [ ] Display toggles: Show file paths, Show count badges, Compact mode
- [ ] Keyboard shortcuts documented with live bindings
- [ ] Reset button restores defaults

### Traceability

- **Client Facts**: CF-016 (Light/dark theme)
- **Roadmap Features**: F-017 (Light/dark theme)

---

## SCR-008: Mobile Explorer View

### Overview

- **Purpose**: Responsive mobile layout for iPad/phone browsing during meetings
- **Layout**: Collapsible drawer for navigation, full-width detail view
- **JTBD**: JTBD-3.1 (Perceived competence during presentations)
- **User Types**: PER-002 (Product People), PER-004 (Build Partners)
- **Entry Points**: Same as SCR-001 on mobile devices
- **Exit Points**: Same as desktop version

### Wireframe Description

```
Mobile (<768px):

┌────────────────────────┐
│ ☰ ClaudeManual  [⚙][⭐]│
├────────────────────────┤
│                        │
│ # Discovery_JTBD       │
│                        │
│ **Path**: .claude/...  │
│ [Copy Path]            │
│                        │
│ ## Purpose             │
│ Extracts Jobs To...    │
│                        │
│ [Tabs: Purpose | Ex...] │
│                        │
│ (Scrollable content)   │
│                        │
└────────────────────────┘

Drawer Open:
┌────────────────────────┐
│ [×] Navigation         │
│ ▼ Skills (85)          │
│   ▼ Discovery (29)     │
│     ├ Discovery_JTBD   │
│     └ ...              │
│ ▼ Commands (30)        │
│ ▼ Agents (25)          │
└────────────────────────┘
```

### Acceptance Criteria

- [ ] Hamburger menu (☰) toggles navigation drawer
- [ ] Detail pane takes full width on mobile
- [ ] Touch-friendly tap targets (44×44px minimum)
- [ ] Swipe gestures: Swipe left to close drawer, swipe right to open
- [ ] Responsive typography: Readable on 320px width screens

### Traceability

- **Roadmap Features**: F-025 (Mobile optimization)

---

## SCR-009: Workflow Viewer

### Overview

- **Purpose**: Display and interact with workflow diagrams (Mermaid, PlantUML) with zoom/pan controls
- **Layout**: Full-width diagram viewer with floating toolbar
- **JTBD**: JTBD-1.9 (Visualize Process and Architecture Diagrams), JTBD-1.2 (Component Context)
- **User Types**: All personas
- **Entry Points**: Click workflow in navigation tree, search results, related links
- **Exit Points**: Back to Explorer, navigate to related workflows

### Wireframe Description

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Header (Same as SCR-001)                                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ [← Back to Explorer]   Workflow: Discovery Process Flow                      │
│                        [Mermaid] [Discovery] ⭐                              │
│                                                                              │
│ ┌────────────────────────────────────────────────────────────────────────┐  │
│ │                                                                        │  │
│ │                      ┌─────────────┐                                   │  │
│ │                      │   Start     │                                   │  │
│ │                      └──────┬──────┘                                   │  │
│ │                             │                                          │  │
│ │                      ┌──────▼──────┐                                   │  │
│ │                      │ Input Files │                                   │  │
│ │                      └──────┬──────┘                                   │  │
│ │                             │                                          │  │
│ │              ┌──────────────┼──────────────┐                           │  │
│ │              │              │              │                           │  │
│ │       ┌──────▼──────┐ ┌─────▼─────┐ ┌─────▼─────┐                     │  │
│ │       │ Pain Points │ │  JTBDs    │ │ Personas  │                     │  │
│ │       └─────────────┘ └───────────┘ └───────────┘                     │  │
│ │                                                                        │  │
│ │                                                                        │  │
│ │ ┌──────────────────────────────────────────────────────────────────┐  │  │
│ │ │ [−] [100%] [+]  [Reset]  [Export ▾]       [Minimap ☐]           │  │  │
│ │ └──────────────────────────────────────────────────────────────────┘  │  │
│ └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│ ## Description                                                               │
│ This workflow shows the Discovery phase process flow from client             │
│ materials input through to deliverable generation.                           │
│                                                                              │
│ ## Related Workflows                                                         │
│ [Prototype Process] [ProductSpecs Flow] [Implementation Cycle]               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### UI Components

| Component | Type | Behavior | UX Psychology Applied |
|---|---|---|---|
| **Diagram Canvas** | SVG/Canvas container | Render Mermaid/PlantUML diagrams, support zoom/pan | **Visual Learning**: Diagrams communicate complex processes faster than text (JTBD-1.9). |
| **Zoom Controls** | Floating toolbar | +/- buttons, percentage display, reset button | **Progressive Disclosure**: Controls appear on hover, don't clutter initial view. |
| **Export Button** | Dropdown menu | PNG, SVG, PDF export options | **Developer UX**: Enable sharing diagrams in presentations and documentation. |
| **Format Badge** | Tag/chip | Show Mermaid or PlantUML format | **Transparency**: Users know what rendering engine is used. |
| **Minimap Toggle** | Checkbox | Show/hide thumbnail navigation for large diagrams | **Navigation Aid**: Large diagrams need spatial context. |

### States

| State | Condition | UI Behavior |
|---|---|---|
| **Loading** | Diagram rendering | Skeleton placeholder with shimmer animation |
| **Success** | Diagram rendered | Show interactive SVG with zoom/pan enabled |
| **Error** | Rendering failed | Show code block with syntax highlighting and error message |
| **Zoomed** | Zoom > 100% or < 100% | Show zoom percentage, enable pan mode |
| **Exporting** | Export in progress | Show spinner in export button |

### User Flows

#### Flow 1: Developer Explores Discovery Workflow
1. Developer (PER-003) clicks "Workflows" in navigation
2. Expands "Process" category → sees "discovery-process"
3. Clicks workflow → SCR-009 loads with Mermaid diagram
4. **UX Psychology - Visual Learning**: Diagram shows process at a glance
5. Uses scroll wheel to zoom into "Pain Points" step
6. Clicks related "prototype-process" workflow → navigates to that diagram
7. **Success Metric**: User understands workflow in < 2 minutes

### Acceptance Criteria

- [ ] Mermaid diagrams render correctly with theme support
- [ ] PlantUML diagrams render via Kroki or configured server
- [ ] Zoom controls work with mouse wheel and buttons
- [ ] Pan works with click-and-drag
- [ ] Export generates PNG, SVG, PDF files
- [ ] Format badge shows "Mermaid" or "PlantUML"
- [ ] Related workflows link to other workflow documents
- [ ] Loading state shows skeleton placeholder
- [ ] Error state shows code block with error message

### UX Psychology Summary

| Principle | Application | User Benefit |
|---|---|---|
| **Visual Learning** | Diagrams over text for process understanding | Faster comprehension (JTBD-1.9) |
| **Progressive Disclosure** | Zoom controls appear on interaction | Clean initial view, power features accessible |
| **Spatial Navigation** | Minimap for large diagrams | Maintain orientation in complex workflows |

### Traceability

- **Addresses Pain Points**: PP-1.2 (Lack of Contextual Documentation)
- **Enables JTBD**: JTBD-1.9 (Visualize Diagrams), JTBD-1.2 (Component Context)
- **Roadmap Features**: F-NEW-01 (Workflow Visualization)

---

## SCR-010: Architecture Browser

### Overview

- **Purpose**: Navigate and view architecture documentation including C4 diagrams and ADRs
- **Layout**: Dual-pane with category navigation and diagram/document viewer
- **JTBD**: JTBD-1.9 (Visualize Architecture), JTBD-1.2 (Component Context), JTBD-2.1 (Confidence)
- **User Types**: All personas
- **Entry Points**: Click "Architecture" in navigation, search results, related links
- **Exit Points**: Back to Explorer, navigate to related ADRs/diagrams

### Wireframe Description

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Header (Same as SCR-001)                                                     │
├──────────────────────────────────┬───────────────────────────────────────────┤
│                                  │                                           │
│ Architecture                     │ Context Diagram - ClaudeManual            │
│ ────────────────────────────────│ ──────────────────────────────────────── │
│                                  │                                           │
│ ▼ C4 Diagrams (4)           [i]  │ [C4] [Context] [Mermaid]                  │
│   ├ Context Diagram         ←    │                                           │
│   ├ Container Diagram            │ ┌──────────────────────────────────────┐ │
│   ├ Component Diagram            │ │                                      │ │
│   └ Code Diagram                 │ │      [Person]                        │ │
│                                  │ │     Framework                        │ │
│ ▼ ADRs (12)                 [i]  │ │      User                            │ │
│   ├ ADR-001: Architecture Style  │ │        │                             │ │
│   ├ ADR-002: Data Storage        │ │        ▼                             │ │
│   ├ ADR-003: API Design          │ │ ┌─────────────┐                      │ │
│   └ ...                          │ │ │ClaudeManual │                      │ │
│                                  │ │ │   System    │                      │ │
│ ▼ Patterns (8)              [i]  │ │ └─────────────┘                      │ │
│   ├ Repository Pattern           │ │                                      │ │
│   ├ Event Sourcing               │ │                                      │ │
│   └ ...                          │ └──────────────────────────────────────┘ │
│                                  │                                           │
│ ▼ Infrastructure (3)        [i]  │ ## Context                                │
│   ├ Deployment Diagram           │ Shows ClaudeManual system in context     │
│   ├ Network Topology             │ with external actors and systems.        │
│   └ ...                          │                                           │
│                                  │ ## Related                                │
│                                  │ [Container Diagram] [ADR-001]            │
│                                  │                                           │
│ [Collapse All] [Expand All]      │ [Copy Path] [Export]                     │
│                                  │                                           │
└──────────────────────────────────┴───────────────────────────────────────────┘
```

### UI Components

| Component | Type | Behavior | UX Psychology Applied |
|---|---|---|---|
| **Category Tree** | Hierarchical navigation | Expand/collapse C4, ADRs, Patterns, Infrastructure | **Cognitive Load Reduction**: Organize by architecture type (JTBD-1.7). |
| **C4 Level Badge** | Tag/chip | Show Context/Container/Component/Code level | **Visual Cues**: Quick identification of diagram scope. |
| **ADR Status Badge** | Tag/chip | Show Proposed/Accepted/Deprecated/Superseded | **Decision Context**: Users see current status immediately (JTBD-2.1). |
| **Diagram Viewer** | Mermaid/PlantUML renderer | Render C4 diagrams with zoom/pan | **Visual Learning**: Architecture diagrams clarify system structure. |
| **ADR Viewer** | Markdown renderer | Show Context, Decision, Consequences sections | **Progressive Disclosure**: ADR structure reveals decision rationale. |

### States

| State | Condition | UI Behavior |
|---|---|---|
| **Category View** | No item selected | Show category overview with document counts |
| **Diagram View** | C4 diagram selected | Show rendered diagram with zoom/pan controls |
| **ADR View** | ADR selected | Show ADR content with Context/Decision/Consequences tabs |
| **Empty Category** | Category has no documents | "No documents in this category" message |

### User Flows

#### Flow 1: Developer Reviews Architecture Before Implementation
1. Developer (PER-003) starting new feature
2. Clicks "Architecture" in navigation
3. Expands "C4 Diagrams" → selects "Container Diagram"
4. **UX Psychology - Visual Learning**: Sees system components at a glance
5. Notes relevant container for feature
6. Clicks "ADR-003: API Design" in related links
7. Reads Decision section → understands API patterns to follow
8. **Success Metric**: Developer finds relevant architecture docs in < 5 minutes

### Acceptance Criteria

- [ ] Category tree shows C4, ADRs, Patterns, Infrastructure
- [ ] C4 diagrams render with level badge (Context/Container/Component/Code)
- [ ] ADRs show status badge (Proposed/Accepted/Deprecated/Superseded)
- [ ] Diagram zoom/pan works consistently with SCR-009
- [ ] ADR viewer shows Context, Decision, Consequences sections
- [ ] Related links connect diagrams to related ADRs
- [ ] Copy Path button copies file path for editing
- [ ] Export button generates PNG/SVG/PDF

### Traceability

- **Addresses Pain Points**: PP-1.2 (Lack of Contextual Documentation)
- **Enables JTBD**: JTBD-1.9 (Visualize Architecture), JTBD-2.1 (Confidence)
- **Roadmap Features**: F-NEW-02 (Architecture Documentation)

---

## SCR-011: Document Preview Modal

### Overview

- **Purpose**: Full-screen modal for viewing diagrams and documents with maximum canvas space
- **Layout**: Full-screen overlay with floating toolbar
- **JTBD**: JTBD-1.9 (Visualize Diagrams), JTBD-3.1 (Professional Presentation)
- **User Types**: All personas
- **Entry Points**: "Expand" button on any diagram, double-click diagram
- **Exit Points**: Close button, Esc key, click outside modal

### Wireframe Description

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────────────────────┐  │
│ │ [×]                           Discovery Process Flow                [⭐] │  │
│ ├─────────────────────────────────────────────────────────────────────────┤  │
│ │                                                                         │  │
│ │                                                                         │  │
│ │                         ┌─────────────┐                                 │  │
│ │                         │   Start     │                                 │  │
│ │                         └──────┬──────┘                                 │  │
│ │                                │                                        │  │
│ │                         ┌──────▼──────┐                                 │  │
│ │                         │ Input Files │                                 │  │
│ │                         └──────┬──────┘                                 │  │
│ │                                │                                        │  │
│ │                 ┌──────────────┼──────────────┐                         │  │
│ │                 │              │              │                         │  │
│ │          ┌──────▼──────┐ ┌─────▼─────┐ ┌─────▼─────┐                   │  │
│ │          │ Pain Points │ │  JTBDs    │ │ Personas  │                   │  │
│ │          └─────────────┘ └───────────┘ └───────────┘                   │  │
│ │                                                                         │  │
│ │                                                                         │  │
│ │                                                                         │  │
│ │                                                                         │  │
│ │                                                                         │  │
│ │ ┌───────────────────────────────────────────────────────────────────┐  │  │
│ │ │ [−] [150%] [+]  [Fit]  [Export ▾]  [Copy]                         │  │  │
│ │ └───────────────────────────────────────────────────────────────────┘  │  │
│ └─────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

### UI Components

| Component | Type | Behavior | UX Psychology Applied |
|---|---|---|---|
| **Full-Screen Canvas** | SVG/Canvas container | Maximum viewport for diagram viewing | **Focus**: Remove distractions for detailed analysis. |
| **Floating Toolbar** | Fixed bottom toolbar | Zoom, export, copy controls | **Accessibility**: Controls always visible regardless of zoom level. |
| **Close Button** | Icon button | Dismiss modal, return to previous view | **Escape Hatch**: Easy way to exit full-screen mode. |
| **Fit Button** | Icon button | Fit diagram to viewport | **Quick Reset**: Restore optimal view after zooming. |
| **Copy Button** | Icon button | Copy diagram as image to clipboard | **Sharing**: Easy copying for presentations and documentation. |

### States

| State | Condition | UI Behavior |
|---|---|---|
| **Open** | Modal visible | Dark backdrop, full-screen diagram |
| **Zoomed** | User has zoomed | Show zoom percentage, enable pan |
| **Exporting** | Export in progress | Show spinner in export button |
| **Copying** | Copy in progress | Show "Copied!" toast notification |

### Acceptance Criteria

- [ ] Modal opens with 200ms fade-in animation
- [ ] Esc key closes modal
- [ ] Click outside modal closes modal
- [ ] Zoom/pan controls work in modal view
- [ ] Fit button returns to optimal zoom level
- [ ] Export button generates PNG/SVG/PDF
- [ ] Copy button copies diagram as PNG to clipboard
- [ ] Mobile: Full viewport, swipe down to close

### Traceability

- **Enables JTBD**: JTBD-1.9 (Visualize Diagrams), JTBD-3.1 (Professional Presentation)
- **Roadmap Features**: F-NEW-03 (Full-Screen Document Preview)

---

## Cross-Screen UX Psychology Summary

### Hicks Law (Simplify Choices) Application Across Screens

| Screen | Hicks Law Implementation | Result |
|---|---|---|
| **SCR-001** | Collapsed tree by default, count badges | 115+ items → visible 5-10 categories |
| **SCR-002** | Type/Stage filters | 115+ results → 10-20 filtered results |
| **SCR-003** | Stage filtering | 115+ items → 20-40 stage-specific items |
| **SCR-004** | Favorites curation | 115+ items → user's 3-10 favorites |

**Outcome**: Users make faster decisions, reduced choice paralysis (JTBD-1.3, JTBD-1.4).

### Cognitive Load Reduction Application Across Screens

| Screen | Cognitive Load Technique | User Benefit |
|---|---|---|
| **SCR-001** | Progressive disclosure via tabs (Purpose → Examples → Options) | Users see only what they need immediately |
| **SCR-002** | One-sentence summaries in search result cards | Users scan without clicking every result |
| **SCR-003** | Filtered item counts ("Showing 40 of 115") | Users understand scope without mental math |
| **SCR-006** | Tabbed modal with sticky header | Users navigate complex docs efficiently |

**Outcome**: Reduced mental effort, faster comprehension (JTBD-1.2, JTBD-2.1).

### Progressive Disclosure Application Across Screens

| Screen | Progressive Disclosure Layer | User Experience |
|---|---|---|
| **SCR-001** | Default: Purpose tab → Advanced: Options/Traceability tabs | Newcomers not overwhelmed, power users access deep details |
| **SCR-002** | Preview cards → Click for detail modal → Tabs for deep dive | Users control information depth |
| **SCR-003** | Collapsed categories → Expand on demand → Select item for details | Users explore at their own pace |
| **SCR-006** | Default tab (Purpose) → Workflow diagrams → Traceability chains | Learning curve managed incrementally |

**Outcome**: Supports both newcomers and experts without compromising either (JTBD-2.2).

### Visual Cues & CTA Psychology Application Across Screens

| Screen | Visual Cues | User Action Triggered |
|---|---|---|
| **SCR-001** | ⭐ Favorites icon, [i] info icons, count badges | Clear affordances for interaction |
| **SCR-002** | Performance indicator ("12 results in <0.8s") | Confidence in tool responsiveness |
| **SCR-004** | Drag handles (6-dot icon) | Discoverable reordering feature |
| **SCR-005** | ✓ and ✗ indicators in comparison table | Quick scanning of tradeoffs |

**Outcome**: Intuitive navigation, reduced learning curve (JTBD-2.1).

---

## Traceability Summary

### Pain Point Coverage

| Pain Point | Addressed By Screens | Coverage |
|---|---|---|
| PP-1.1 (Knowledge Transfer Complexity) | SCR-001 (Self-service UI), SCR-002 (Search), SCR-006 (Deep docs) | 100% |
| PP-1.2 (Lack of Contextual Documentation) | SCR-001 (Multi-section detail), SCR-006 (Workflow diagrams) | 100% |
| PP-1.3 (Discoverability Challenge) | SCR-002 (Search), SCR-003 (Stage filters), SCR-005 (Comparison) | 100% |
| PP-1.4 (Organizational Chaos) | SCR-003 (Stage-filtered view) | 100% |
| PP-1.5 (Lack of Personalization) | SCR-004 (Favorites) | 100% |
| PP-1.6 (Developer Friction) | SCR-001 (Copy Path), SCR-002 (File paths in results) | 100% |

**Total Coverage**: 6/6 pain points (100%) + 1 user feedback (FB-001)

### JTBD Coverage

| JTBD | Addressed By Screens | Coverage |
|---|---|---|
| JTBD-1.1 (Self-service learning) | SCR-001, SCR-006 | 100% |
| JTBD-1.2 (Component context) | SCR-001, SCR-006 | 100% |
| JTBD-1.3 (Find relevant tools) | SCR-002, SCR-003 | 100% |
| JTBD-1.4 (Stage-appropriate tools) | SCR-003 | 100% |
| JTBD-1.5 (Edit source files) | SCR-001 (Copy Path) | 100% |
| JTBD-1.6 (Bookmark tools) | SCR-004 | 100% |
| JTBD-1.7 (Navigate hierarchies) | SCR-001 | 100% |
| JTBD-1.8 (Compare components) | SCR-005 | 100% |
| JTBD-2.1 (Confidence) | SCR-006 (Workflow diagrams, examples) | 100% |
| JTBD-2.2 (Autonomous exploration) | SCR-001, SCR-002 | 100% |
| JTBD-3.1 (Perceived competence) | SCR-008 (Mobile for presentations) | 100% |
| JTBD-1.9 (Visualize diagrams) | SCR-009, SCR-010, SCR-011 | 100% |

**Total Coverage**: 12/13 JTBD (92.3%) - JTBD-3.2 (Contribution workflow) deferred to Phase 3

### Client Facts Coverage

| Client Fact | Addressed By Screens | Implementation |
|---|---|---|
| CF-006 (Master-detail UI) | SCR-001 | Dual-pane layout with navigation tree and detail pane |
| CF-008 (Multi-section documentation) | SCR-001, SCR-006 | Tabbed interface with Purpose/Examples/Options/Workflow/Traceability |
| CF-009 (Search page) | SCR-002 | Full-text search with filters and ranking |
| CF-010 (Tagging system) | SCR-002, SCR-003 | Stage badges, type filters |
| CF-011 (Stage-based organization) | SCR-003 | Stage filter dropdown and filtered views |
| CF-012 (Favorites) | SCR-004 | Bookmarking with reordering |
| CF-013 (File path references) | SCR-001, SCR-002 | Copy Path buttons throughout |
| CF-016 (Light/dark theme) | SCR-007 | Theme toggle in settings |

**Total Coverage**: 8/16 client facts (50%) - Remaining facts are technical constraints (Node.js, React) or covered in implementation phase

---

## Next Steps

1. **Wireframe Refinement**: Convert ASCII wireframes to high-fidelity Figma mockups
2. **Interaction Prototyping**: Create clickable prototypes for user testing (SCR-001, SCR-002, SCR-004)
3. **User Testing**: Validate UX psychology assumptions with framework team (3-5 users)
4. **Component Library**: Define React components for navigation tree, detail pane, search results
5. **Accessibility Audit**: Ensure WCAG 2.1 AA compliance (keyboard navigation, screen reader support)
6. **Workflow Diagram Integration**: Implement Mermaid rendering for workflow visualization (SCR-006)

---

*11 screens defined with comprehensive UX psychology principles applied. 100% pain point coverage, 92.3% JTBD coverage. All screens trace to validated client facts and roadmap features. SCR-009, SCR-010, SCR-011 added via feedback FB-001 to support workflow, ways of working, and architecture document visualization.*
