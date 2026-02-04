# Plan: Enhanced Search with Content Search, Grouped Results, and Full-Screen Modal

## Task Description
Enhance the `/search` API endpoint and search page to support:
1. **Filename search** - Search by file names (already partially exists)
2. **Content search** - Search within file contents (markdown body text)
3. **Grouped results** - Display results grouped by folder category (skills, commands, agents, hooks, workflows, architecture)
4. **Full-screen modal viewer** - When clicking a search result, show a full-screen modal displaying the file content
5. **Persistent search state** - When closing the modal, search results remain visible
6. **Type filters** - Filter by skills, commands, hooks, agents, or show all
7. **Tag-based search** - Search and filter by frontmatter tags

## Objective
When this plan is complete, users will be able to:
- Search across all framework components by filename AND file content
- See results organized by category (Skills, Commands, Agents, Hooks, Workflows, Architecture)
- Click any result to view full file content in a beautiful full-screen modal
- Close the modal and continue browsing search results
- Apply type filters (Skills only, Commands only, etc.)
- Search by tags defined in frontmatter

## Problem Statement
The current search implementation only searches:
- Skills (from `.claude/skills/*/SKILL.md`)
- Commands (from `.claude/commands/*.md`)
- Agents (from `.claude/agents/*.md`)

It does NOT:
- Search file content (only name, description, stage)
- Include hooks (`.claude/hooks/*.py`)
- Include workflows (`.claude/architecture/Workflows/**/*.md`)
- Include architecture docs (`.claude/architecture/**/*.md`)
- Group results by folder type
- Provide a full-screen file viewer modal
- Support tag-based filtering from frontmatter

## Solution Approach
1. **Extend API to scan more directories**: Add hooks, workflows, and architecture to searchable items
2. **Add content search**: Read file content and include in search matching
3. **Add tags extraction**: Parse `tags:` from YAML frontmatter
4. **Create TypeFilter component**: Chip-based filter for Skills/Commands/Agents/Hooks/Workflows/Architecture/All
5. **Group results by category**: Transform flat results into grouped structure
6. **Create FileContentModal component**: Full-screen modal using `MarkdownRenderer` to display file content
7. **Fetch file content on demand**: New API endpoint to read file content by path

## Relevant Files
Use these files to complete the task:

### Existing Files to Modify
- `src/app/api/search/route.ts` - Extend to search more directories, add content search, extract tags
- `src/app/search/page.tsx` - Add TypeFilter, grouped results display, modal integration
- `src/components/StageFilterDropdown/index.tsx` - Reference for filter component pattern
- `src/components/DetailModal.tsx` - Reference for modal pattern

### New Files
- `src/components/TypeFilter/index.tsx` - Chip-based type filter (Skills, Commands, Agents, Hooks, Workflows, Architecture, All)
- `src/components/FileContentModal/index.tsx` - Full-screen modal for viewing file content
- `src/app/api/file-content/route.ts` - API endpoint to fetch file content by path

## Implementation Phases

### Phase 1: Foundation
- Extend search API to include hooks, workflows, and architecture directories
- Add content search capability (search within file body)
- Extract tags from YAML frontmatter
- Add `category` field to search results (skill, command, agent, hook, workflow, architecture)

### Phase 2: Core Implementation
- Create TypeFilter component for filtering by type
- Update search page to display grouped results by category
- Create FileContentModal component for full-screen file viewing
- Create file-content API endpoint for fetching file content

### Phase 3: Integration & Polish
- Integrate TypeFilter into search page
- Wire up modal to open on search result click
- Ensure search state persists when modal closes
- Add loading states and error handling
- Test all filter combinations

## Team Orchestration

- You operate as the team lead and orchestrate the team to execute the plan.
- You're responsible for deploying the right team members with the right context to execute the plan.
- IMPORTANT: You NEVER operate directly on the codebase. You use `Task` and `Task*` tools to deploy team members to to the building, validating, testing, deploying, and other tasks.
  - This is critical. You're job is to act as a high level director of the team, not a builder.
  - You're role is to validate all work is going well and make sure the team is on track to complete the plan.
  - You'll orchestrate this by using the Task* Tools to manage coordination between the team members.
  - Communication is paramount. You'll use the Task* Tools to communicate with the team members and ensure they're on track to complete the plan.
- Take note of the session id of each team member. This is how you'll reference them.

### Team Members

- Builder
  - Name: API-Developer
  - Role: Implement backend API enhancements (search route, file-content route)
  - Agent Type: implementation-developer
  - Resume: true

- Builder
  - Name: UI-Developer
  - Role: Implement frontend components (TypeFilter, FileContentModal, search page updates)
  - Agent Type: implementation-developer
  - Resume: true

- Builder
  - Name: Test-Designer
  - Role: Design test specifications for new functionality
  - Agent Type: implementation-test-designer
  - Resume: true

- Builder
  - Name: Code-Reviewer
  - Role: Review completed code for quality and best practices
  - Agent Type: quality-code-quality
  - Resume: false

## Step by Step Tasks

- IMPORTANT: Execute every step in order, top to bottom. Each task maps directly to a `TaskCreate` call.
- Before you start, run `TaskCreate` to create the initial task list that all team members can see and execute.

### 1. Extend Search API - Add Hooks Directory
- **Task ID**: api-add-hooks
- **Depends On**: none
- **Assigned To**: API-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- In `src/app/api/search/route.ts`, add scanning for `.claude/hooks/*.py` files
- Extract name from filename, description from first docstring or comment
- Set `type: 'Hook'` and determine stage from naming convention
- Add to `loadAllItems()` function

### 2. Extend Search API - Add Workflows Directory
- **Task ID**: api-add-workflows
- **Depends On**: api-add-hooks
- **Assigned To**: API-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- In `src/app/api/search/route.ts`, add recursive scanning for `.claude/architecture/Workflows/**/*.md`
- Parse YAML frontmatter for name, description, tags
- Set `type: 'Workflow'` and extract stage from parent folder name
- Add to `loadAllItems()` function

### 3. Extend Search API - Add Architecture Directory
- **Task ID**: api-add-architecture
- **Depends On**: api-add-workflows
- **Assigned To**: API-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- In `src/app/api/search/route.ts`, add recursive scanning for `.claude/architecture/**/*.md` (excluding Workflows subfolder)
- Parse YAML frontmatter for name, description, tags
- Set `type: 'Architecture'` and extract category from folder structure
- Add to `loadAllItems()` function

### 4. Extend Search API - Add Content Search
- **Task ID**: api-content-search
- **Depends On**: api-add-architecture
- **Assigned To**: API-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- Modify `loadAllItems()` to include `content` field (markdown body after frontmatter)
- Truncate content to first 500 chars for search preview
- Update search filter to match against `content` field
- Add relevance score boost for content matches (lower than name/description)

### 5. Extend Search API - Add Tags Extraction
- **Task ID**: api-add-tags
- **Depends On**: api-content-search
- **Assigned To**: API-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- Enhance `parseYamlFrontmatter()` to extract `tags` field as array
- Add `tags: string[]` to `SearchableItem` interface
- Include tags in search matching with appropriate relevance score

### 6. Create File Content API Endpoint
- **Task ID**: api-file-content
- **Depends On**: api-add-tags
- **Assigned To**: API-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- Create new file `src/app/api/file-content/route.ts`
- Accept `path` query parameter (relative path like `.claude/skills/xyz/SKILL.md`)
- Validate path is within allowed directories (security check)
- Return full file content as markdown
- Handle 404 for missing files

### 7. Create TypeFilter Component
- **Task ID**: ui-type-filter
- **Depends On**: none
- **Assigned To**: UI-Developer
- **Agent Type**: implementation-developer
- **Parallel**: true (can run parallel with API tasks 1-6)
- Create `src/components/TypeFilter/index.tsx`
- Implement chip-based filter with options: All, Skills, Commands, Agents, Hooks, Workflows, Architecture
- Support single selection (radio-style) or multi-select mode
- Use similar styling to existing `StageFilterDropdown`
- Export `TypeFilter` and `TypeFilterProps` interface

### 8. Create FileContentModal Component
- **Task ID**: ui-file-modal
- **Depends On**: ui-type-filter
- **Assigned To**: UI-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- Create `src/components/FileContentModal/index.tsx`
- Full-screen modal using portal (reference `DetailModal.tsx`)
- Use `MarkdownRenderer` to display file content
- Header with file name, path, and close button
- Loading state while fetching content
- Escape key and backdrop click to close
- Animated enter/exit transitions

### 9. Update Search Results Interface
- **Task ID**: ui-search-interface
- **Depends On**: api-add-tags
- **Assigned To**: UI-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- Update `SearchResult` interface in search page to include:
  - `tags: string[]`
  - `content?: string` (preview snippet)
  - `type: 'Skill' | 'Command' | 'Agent' | 'Hook' | 'Workflow' | 'Architecture'`
- Update type definitions to match new API response

### 10. Implement Grouped Results Display
- **Task ID**: ui-grouped-results
- **Depends On**: ui-search-interface
- **Assigned To**: UI-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- Create helper function `groupResultsByType(results)` that returns `Record<string, SearchResult[]>`
- Update search page to render results in collapsible sections by type
- Each section header shows type name and count (e.g., "Skills (12)")
- Sections are expandable/collapsible, all expanded by default

### 11. Integrate TypeFilter into Search Page
- **Task ID**: ui-integrate-type-filter
- **Depends On**: ui-type-filter, ui-grouped-results
- **Assigned To**: UI-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- Import and add `TypeFilter` to search page header
- Add state for `selectedTypes: string[]`
- Filter grouped results based on selected types
- "All" selection shows all types

### 12. Integrate FileContentModal into Search Page
- **Task ID**: ui-integrate-modal
- **Depends On**: ui-file-modal, api-file-content
- **Assigned To**: UI-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- Add state for `selectedFilePath: string | null` and `modalOpen: boolean`
- On result click, set `selectedFilePath` and open modal
- Fetch file content using `/api/file-content?path=...`
- On modal close, clear modal state but KEEP search results and filters
- Search results should remain visible and scrolled to same position

### 13. Add Tag Search Support to UI
- **Task ID**: ui-tag-search
- **Depends On**: ui-integrate-modal
- **Assigned To**: UI-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- Display tags on each search result card
- Add tag filter section (use existing `TagFilter` component pattern)
- Allow filtering by multiple tags (AND/OR logic)
- Show "Available tags" based on current results

### 14. Write Unit Tests for API Changes
- **Task ID**: test-api-unit
- **Depends On**: api-file-content
- **Assigned To**: Test-Designer
- **Agent Type**: implementation-test-designer
- **Parallel**: false
- Write tests for extended `loadAllItems()` function
- Test hooks directory scanning
- Test workflows directory scanning
- Test architecture directory scanning
- Test content search matching
- Test tags extraction
- Test file-content API endpoint

### 15. Write Component Tests
- **Task ID**: test-ui-unit
- **Depends On**: ui-tag-search
- **Assigned To**: Test-Designer
- **Agent Type**: implementation-test-designer
- **Parallel**: false
- Write tests for `TypeFilter` component
- Write tests for `FileContentModal` component
- Write tests for grouped results rendering
- Write tests for search page integration

### 16. Code Quality Review
- **Task ID**: review-code
- **Depends On**: test-api-unit, test-ui-unit
- **Assigned To**: Code-Reviewer
- **Agent Type**: quality-code-quality
- **Parallel**: false
- Review all new and modified files
- Check for SOLID principles adherence
- Verify error handling is comprehensive
- Check for potential security issues (path traversal)
- Ensure consistent code style

### 17. Final Validation
- **Task ID**: validate-all
- **Depends On**: review-code
- **Assigned To**: API-Developer
- **Agent Type**: implementation-developer
- **Parallel**: false
- Run all validation commands
- Verify acceptance criteria met
- Test end-to-end flow manually
- Ensure build passes without errors

## Acceptance Criteria

1. **Search includes all directories**: Skills, Commands, Agents, Hooks, Workflows, and Architecture files are all searchable
2. **Content search works**: Searching for text that only appears in file body (not name/description) returns results
3. **Tags are searchable**: Files with matching tags appear in results when searching by tag
4. **Results are grouped**: Search results display in collapsible sections by type (Skills, Commands, etc.)
5. **Type filter works**: Selecting "Skills only" shows only skill results
6. **Modal displays content**: Clicking a result opens full-screen modal with complete file content rendered as markdown
7. **Modal close preserves state**: Closing modal keeps search results, filters, and scroll position intact
8. **Tag filter works**: Can filter results by one or more tags
9. **No regressions**: Existing search functionality continues to work
10. **Performance acceptable**: Search returns results within 500ms for typical queries

## Validation Commands

Execute these commands to validate the task is complete:

- `npm run type-check` - Verify TypeScript compiles without errors
- `npm run lint` - Verify no linting errors
- `npm run test` - Run all unit tests
- `npm run build` - Verify production build succeeds
- `curl "http://localhost:3000/api/search?q=discovery"` - Test API returns results from all directories
- `curl "http://localhost:3000/api/search?q=function"` - Test content search returns results
- `curl "http://localhost:3000/api/file-content?path=.claude/skills/slidev/SKILL.md"` - Test file content API

## Notes

### Directory Structure for Search
```
.claude/
├── skills/          # SKILL.md files -> type: Skill
├── commands/        # *.md files -> type: Command
├── agents/          # *.md files -> type: Agent
├── hooks/           # *.py files -> type: Hook
└── architecture/
    ├── Workflows/   # **/*.md -> type: Workflow
    └── **/*.md      # type: Architecture
```

### Security Considerations
The file-content API must validate that requested paths are within the allowed `.claude/` directory to prevent path traversal attacks. Use `path.normalize()` and verify the resolved path starts with the allowed base path.

### Performance Considerations
- Limit content preview to 500 characters to keep response size manageable
- Consider caching `loadAllItems()` result with short TTL if performance becomes an issue
- Use virtualization for large result sets (>100 items)

### Type Definitions
```typescript
interface SearchableItem {
  id: string;
  name: string;
  description: string;
  stage: string;
  path: string;
  type: 'Skill' | 'Command' | 'Agent' | 'Hook' | 'Workflow' | 'Architecture';
  tags?: string[];
  content?: string; // First 500 chars of body for search preview
}
```
