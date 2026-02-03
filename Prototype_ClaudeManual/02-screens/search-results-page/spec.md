# Search Results Page

**ID**: SCR-002
**Discovery ID**: S-2 (from screen-definitions.md)
**Application**: Web
**Priority**: P0 (MVP)
**Primary Persona**: PER-002 (Product People), PER-003 (Developers)

## Overview

The Search Results Page provides instant keyword search across all framework components (skills, commands, agents, rules, hooks, workflows, architecture docs) with relevance ranking, filtering, and quick actions. It enables users to find relevant tools in under 2 seconds, addressing the discoverability challenge (PP-1.3) and supporting autonomous exploration (JTBD-2.2).

## Layout

### Wireframe

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

### Grid Structure

| Region | Layout | Components |
|--------|--------|------------|
| Header | Fixed top, 64px height | AppHeader (from SCR-001) |
| Back Button | Absolute left, 16px margin | Link with icon |
| Results Header | Full width, 80px | Heading, performance indicator |
| Filters Bar | Full width, 56px | StageFilterDropdown, TypeFilter, SortDropdown |
| Results List | Full width, scrollable | SearchResultCard (repeated) |
| Load More Button | Full width, centered | Button |

## Components Used

| Component | Instance | Props |
|-----------|----------|-------|
| SearchResultCard | Repeated per result | `id`, `name`, `description`, `type`, `stage`, `path`, `isFavorite`, `onFavorite`, `onViewDetails`, `onCopyPath` |
| StageFilterDropdown | Single | `selectedStages`, `onChange` |
| TypeFilter | Single | `selectedTypes`, `onChange` |
| SortDropdown | Single | `sortBy`, `onChange` |
| Badge | Multiple (type, stage) | `variant`, `color`, `children` |
| Button | Multiple (actions) | `variant`, `size`, `onPress`, `children` |
| Link | Back button, result links | `href`, `children` |
| Heading | Results header | `level`, `children` |
| Text | Performance indicator | `children` |

## Data Requirements

### Page Load Data

| Field | Source | Type | Required |
|-------|--------|------|----------|
| searchQuery | URL query param `?q=` | string | Yes |
| results | POST /api/search | SearchResult[] | Yes |
| userPreferences | localStorage | UserPreferences | No |
| favorites | localStorage favorites array | string[] | No |

### User Input Data

| Field | Component | Validation |
|-------|-----------|------------|
| searchQuery | SearchInput (from header) | min: 2 chars, debounced 300ms |
| stageFilter | StageFilterDropdown | enum: Discovery, Prototype, etc. |
| typeFilter | TypeFilter | enum: Skill, Command, Agent, Rule, Hook, Workflow, etc. |
| sortBy | SortDropdown | enum: relevance, alphabetical, recent |

## State Management

### Local State

```typescript
interface SearchResultsScreenState {
  query: string;
  results: SearchResult[];
  filteredResults: SearchResult[];
  loading: boolean;
  error: string | null;
  filters: {
    stages: string[];
    types: string[];
    sortBy: 'relevance' | 'alphabetical' | 'recent';
  };
  pagination: {
    page: number;
    pageSize: number;
    totalResults: number;
    hasMore: boolean;
  };
  performanceMetrics: {
    executionTime: number;
    resultCount: number;
  };
}
```

### Global State Dependencies

| Store | Slice | Usage |
|-------|-------|-------|
| userPreferences | favorites | Highlight favorited results |
| userPreferences | stage_filter | Pre-populate stage filter |
| userPreferences | search_history | Add query to history |

## Navigation

### Entry Points

| From | Trigger | Params |
|------|---------|--------|
| SCR-001 (Main Explorer) | Type in search bar | `?q={query}` |
| SCR-001 (Main Explorer) | Press Cmd+K | `?q=` (empty, autofocus) |
| Browser URL | Direct URL | `?q={query}&stage={stage}&type={type}` |

### Exit Points

| To | Trigger | Data Passed |
|----|---------|-------------|
| SCR-001 (Main Explorer) | Click "Back to Explorer" | - |
| SCR-001 (Main Explorer) | Click result "View Details" | `selectedId={result.id}` |
| SCR-006 (Detail Modal) | Click result card | `itemId={result.id}` |

## Interactions

### User Actions

| Action | Component | Handler | Result |
|--------|-----------|---------|--------|
| Type query | SearchInput (header) | onSearch | POST /api/search, update results |
| Apply stage filter | StageFilterDropdown | onChange | Filter results locally |
| Apply type filter | TypeFilter | onChange | Filter results locally |
| Change sort | SortDropdown | onChange | Re-sort results locally |
| Click result | SearchResultCard | onClick | Navigate to SCR-001 or SCR-006 |
| Copy path | Button (in card) | onPress | Copy to clipboard, show toast |
| Add to favorites | Button (in card) | onPress | Update localStorage, update state |
| Load more | Button (bottom) | onPress | Fetch next page |

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `/` | Focus search input |
| `Esc` | Clear search, return to SCR-001 |
| `↓` / `↑` | Navigate results with keyboard |
| `Enter` | Open selected result |
| `Cmd+K` / `Ctrl+K` | Focus search input |

## Responsive Behavior

| Breakpoint | Changes |
|------------|---------|
| Desktop (>1024px) | Full layout as wireframed, 3-column filter bar |
| Tablet (768-1024px) | Filters stack to 2 rows, results full width |
| Mobile (<768px) | Filters drawer (hamburger), single-column results |

## Accessibility

- **Page Title**: "Search Results: {query} - ClaudeManual"
- **Landmarks**: `<main role="main">`, `<nav role="navigation">` for filters
- **Skip Link**: "Skip to search results"
- **Focus Management**: Focus first result on load, trap focus in result cards
- **Announcements**: "Loaded {count} results for '{query}' in {time}s" via aria-live
- **Keyboard Navigation**: Full arrow key navigation, Enter to select

## Error States

| State | Display | Recovery |
|-------|---------|----------|
| Search API error | "Search unavailable. Try browsing by stage instead." | Link to SCR-003 |
| No results | "No results for '{query}'. Try different keywords or browse by stage." | Suggestions, link to SCR-001 |
| Empty query | "Type to search skills, commands, agents, or rules..." | Placeholder text |
| Network timeout | "Search timed out. Check your connection." | Retry button |

## Performance Indicators

| Indicator | Display | Traceability |
|-----------|---------|--------------|
| Execution time | "{count} results in <{time}s" | JTBD-1.3 (2-second threshold) |
| Result count | Shown in results header | - |
| Performance color | Green if <1s, Yellow if 1-2s, Red if >2s | Visual confidence (JTBD-2.1) |

## User Flows

### Flow 1: Product Manager Searching for GDPR Compliance Tools

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

### Flow 2: Developer Searching for TDD Implementation Tools

1. Developer (PER-003) needs test automation tools
2. Opens app → types "TDD" in search bar
3. Sees 8 results: "Implementation_Developer" (skill), "/htec-sdd-implement" (command), "test-automation-engineer" (agent)
4. Applies "Stage: Implementation" filter → narrows to 5 results
5. **UX Psychology - Hicks Law**: Filtering reduces choices from 8 to 5, making decision easier
6. Clicks "test-automation-engineer" agent → views detail pane
7. Reads Examples tab → sees code for running Vitest tests
8. Clicks "Add to Favorites" → bookmarks for future use
9. **Success Metric**: Developer adds 3+ tools to favorites within first week (JTBD-1.6)

## Acceptance Criteria

- [ ] Search returns results within 2 seconds of query (JTBD-1.3 success criteria)
- [ ] Search indexes skill/command/agent names, descriptions, and frontmatter tags
- [ ] Results show title, one-sentence summary, file path, type badge, stage badge
- [ ] Type filter includes: All, Skill, Command, Agent, Rule, Hook, Workflow, WaysOfWorking, ArchitectureDoc
- [ ] Stage filter includes: All, Discovery, Prototype, ProductSpecs, SolArch, Implementation, Utility
- [ ] Sort options: Relevance (default), Alphabetical A-Z, Recently Updated
- [ ] Fuzzy search tolerates typos (e.g., "personna" matches "persona")
- [ ] Empty query state shows helpful placeholder text
- [ ] No results state suggests alternative actions (browse by stage)
- [ ] Back to Explorer button returns to SCR-001 with previous selection preserved
- [ ] Keyboard navigation: Arrow keys to select results, Enter to view details
- [ ] Performance indicator shows execution time and result count
- [ ] Results are paginated (20 per page, Load More button)

## UX Psychology Summary

| Principle | Application | User Benefit |
|-----------|-------------|--------------|
| **Instant Feedback** | Results appear in <2 seconds, performance indicator shown | Reduces uncertainty, builds confidence (JTBD-2.1) |
| **Hicks Law** | Filters reduce visible choices from 115+ to ~10-20 | Faster decision-making, less overwhelm (JTBD-1.3) |
| **Cognitive Load** | One-sentence summaries in cards prevent needing to click every result | Users scan efficiently, save time (PP-1.2) |
| **Progressive Disclosure** | Preview in cards → full details on click → deep dive in tabs | Users control information depth (JTBD-2.2) |

## Traceability

### Addresses Pain Points
- **PP-1.3**: Discoverability Challenge - 2-second search vs. 30+ minutes manual browsing
- **PP-1.2**: Lack of Contextual Documentation - One-sentence summaries in cards

### Enables JTBD
- **JTBD-1.3**: Find relevant tools quickly (2-second threshold)
- **JTBD-2.2**: Autonomous exploration without developer assistance

### Client Facts
- **CF-009**: Search page requirement
- **CF-010**: Tagging system for filtering

### Roadmap Features
- **F-005**: Basic search functionality
- **F-007**: Search results ranking by relevance

---

**Traceability**: S-2, JTBD-1.3, JTBD-2.2, PP-1.2, PP-1.3, CF-009, CF-010, F-005, F-007
**Components**: SearchResultCard, StageFilterDropdown, TypeFilter, Badge, Button, Link, Heading, Text
