---
document_id: PF-001
version: 1.0.0
created_at: 2026-02-01
feedback_type: Enhancement
severity: Medium
source_person: User
inputter: User
---

# Original Feedback

"I wanted to see the content of skills, commands, agents. So I expected to see the markdown viewer when I select a skill, command or agent. I see the Skill, command, agent name, the frontmatter attributes and then the content of the skill, command or agent under the Purpose statement."

## Interpretation

The user expects that when selecting a skill, command, or agent in the navigation tree:
1. They should see the **name** of the item
2. They should see **frontmatter attributes** displayed (model, stage, path, tools, etc.)
3. They should see the **actual markdown content** from the source file rendered under the Purpose section

## Current Behavior

The `DetailPane` component currently displays:
- Name and description
- Type and stage badges
- File path
- Purpose tab (shows a short summary string, not actual file content)
- Examples tab (shows structured examples, not markdown)
- Options tab (shows table of options)
- Workflow tab (shows diagram)
- Traceability tab (shows links)

## Expected Behavior

When a user selects a skill/command/agent:
1. Load the actual markdown file content from the source file path
2. Parse frontmatter to extract all attributes
3. Display frontmatter attributes in a structured format (similar to current metadata badges but more comprehensive)
4. Render the actual markdown content (everything after frontmatter) in the Purpose tab using the MarkdownRenderer

## Key Files Involved

- `src/components/DetailPane/index.tsx` - Main detail pane component
- `src/components/MarkdownRenderer/index.tsx` - Markdown rendering component
- `00-foundation/test-data/skills.json` - Test data for skills
- `00-foundation/test-data/commands.json` - Test data for commands
- `00-foundation/test-data/agents.json` - Test data for agents
