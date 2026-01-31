# Persona: The Product Explorer

---
persona_id: PER-002
user_type_id: UT-002
priority: Secondary
checkpoint: CP-3
source: CM-001
validated: true
---

## Profile

- **Name**: Ana (Product Manager)
- **Role**: Product Manager / Product Owner
- **Experience**: 4 years in product management, background in business analysis, limited coding experience
- **Technical Proficiency**: Medium (Understands workflows and technical concepts, but doesn't write code regularly)
- **Team Context**: Works with developers, designers, and stakeholders to define product requirements and prioritize features

## Quote

> "I want this to have a search page. I want this to have text so I can take skills for myself that are useful"

*Synthesized from user type goals and interview context (CF-009, CF-010)*

## Background

Ana is a product manager who recently joined a team using the Claude framework for client discovery and prototyping projects. She comes from a traditional product management background where she used tools like JIRA, Figma, and Confluence, but the Claude framework is new territory.

She's excited about the framework's potential - she's heard it can transform raw client interviews into personas, generate prototypes, and create comprehensive product specs. However, when she tried to explore the framework on her own, she got lost in the folder structure. She opened `.claude/skills/` and saw 115+ markdown files but couldn't quickly identify which ones were relevant for her discovery work.

Ana learns best through examples and visual walkthroughs. She's comfortable with technical concepts when they're explained in context, but she needs the "why" and "when to use this" before diving into "how." She's not intimidated by the framework - she just needs a better map to navigate it.

## Goals

### Primary Goals

1. **Understand Framework Capabilities** - Quickly grasp what the framework can do for product discovery, prototyping, and specification generation without reading 100+ markdown files. (Traces to PP-1.3, PP-1.4)
2. **Find Relevant Tools for Her Workflow** - Identify which skills and commands apply to the discovery phase (personas, JTBD, pain points) versus implementation phase (code generation, testing). (Traces to PP-1.3, PP-1.4)
3. **Learn When to Use Each Tool** - Understand the conditions that trigger using `/discovery-multiagent` vs. `/discovery-audit` vs. `/discovery-feedback`. (Traces to PP-1.2)

### Secondary Goals

1. **Confidently Recommend Framework to Stakeholders** - Articulate the framework's value proposition to clients and executives without requiring deep technical expertise.
2. **Collaborate Effectively with Developers** - Speak the same language as engineers who are implementing framework-generated specs.
3. **Customize Discovery Workflows** - Adapt framework tools to specific client needs (e.g., medical device compliance discovery vs. e-commerce discovery).

## Frustrations

### High Priority

- **Discoverability Challenge** (PP-1.3): With 115+ skills and dozens of commands, finding the right tool feels like searching for a needle in a haystack. She opens the `.claude/skills/` folder and sees `Discovery_GeneratePersona`, `Discovery_JTBDExtractor`, `Discovery_VisionStrategy`, `Prototype_DesignSystem`, `Implementation_TDD`, but has no way to filter by "just show me discovery tools" or search for "persona generation."

- **Organizational Chaos** (PP-1.4): Framework components aren't visually organized by workflow stage. She doesn't immediately understand which tools belong to discovery (her focus area) versus implementation (her developer teammates' focus). This creates decision paralysis - she's afraid of picking the wrong tool and wasting time.

### Medium Priority

- **Lack of Contextual Documentation** (PP-1.2): When she opens a skill file like `Discovery_GeneratePersona`, she sees markdown with frontmatter and instructions, but no clear explanation of "when to use this vs. the persona synthesizer agent" or "what inputs do I need to prepare before running this?" She needs more context than just the technical documentation.

- **No Quick Reference** (PP-1.3): She can't quickly answer stakeholder questions like "Can the framework generate wireframes from user stories?" or "Does it support GDPR compliance checks?" without digging through multiple files or asking the framework creator.

## Day in the Life

### Morning (8:00 AM - 12:00 PM)

Ana starts her day preparing for a client discovery workshop. The client is a healthcare startup that wants to build a patient portal. She knows the Claude framework has discovery tools (the team used it on a previous project), but she's not sure which ones apply to healthcare compliance.

She opens her laptop, navigates to the `.claude/skills/` folder, and starts scrolling. She sees `Discovery_GeneratePersona`, which sounds relevant. She clicks on it and reads the markdown:

```
---
name: Discovery_GeneratePersona
description: Generates rich persona documents...
context: fork
---
```

The frontmatter doesn't tell her if this is the right tool for healthcare personas specifically. She opens five more skill files, trying to piece together the workflow. After 20 minutes, she messages the framework creator on Slack: "Which discovery skill should I use for healthcare compliance personas?"

### Afternoon (12:00 PM - 6:00 PM)

In the afternoon, Ana runs the `/discovery-multiagent` command (as recommended by the framework creator). It works beautifully - generating personas, pain points, and JTBD from client interviews. But now she has a new problem: the client asked if they can add GDPR compliance checks to the discovery phase.

She searches the `.claude/skills/` folder for "GDPR" or "compliance" but doesn't find anything with those exact names. She opens 10+ files hoping to find something related but eventually gives up and asks the developer team if compliance skills exist. They tell her about `GRC_gdpr-dsgvo-expert`, which she never would have found on her own because she didn't know to search in the "GRC" category.

By 4:00 PM, she's frustrated. The framework is powerful, but she feels like she's always one Slack message away from using it effectively. She wishes there was a search interface where she could type "GDPR compliance" and see all related tools, or filter by "Discovery stage" to see only the tools relevant to her current project phase.

### Key Moments

- **Peak Stress**: 10:30 AM - Spending 30 minutes searching for the right tool when she has a client meeting in 2 hours.
- **Peak Satisfaction**: When she successfully runs a discovery command and sees the automated persona generation work perfectly, validating the framework's power.
- **System Touchpoints**:
  - VSCode (browsing `.claude/` folders)
  - Slack (asking framework questions)
  - JIRA (tracking discovery deliverables)
  - Client meeting tools (Zoom, Miro) where she presents framework outputs

## Technology Profile

| Aspect | Details |
|--------|---------|
| **Primary Devices** | MacBook Air, iPad for client presentations |
| **Preferred Apps** | JIRA, Figma, Miro, Notion, Slack, Google Docs |
| **Pain with Tech** | Gets overwhelmed by complex file systems, prefers visual interfaces over terminal commands |
| **Learning Style** | Learns by example, values video tutorials and step-by-step guides, needs "why" before "how" |

## Quotes

> "I want this to have a search page. I want this to have text so I can take skills for myself that are useful" - On discoverability needs (CF-009, CF-010)

> "they could be organized visually into stages like we have in discovery, prototyping, implementation and utilities" - On stage-based organization (CF-011)

*Synthesized from interview analysis (Lines 6, CF-011)*

## Jobs to Be Done

### Functional Jobs

- **When I'm starting a new client project**, I want to quickly find all discovery-phase tools, so I can plan the right workflow without asking for help.
- **When a client asks "can the framework do X?"**, I want to search for capabilities by keyword, so I can confidently answer within seconds instead of minutes.
- **When I need to explain framework value to stakeholders**, I want to access high-level summaries and examples, so I don't have to read technical documentation.

### Emotional Jobs

- **I want to feel competent** when using the framework, not constantly dependent on developers or the framework creator.
- **I want to feel confident** when recommending framework tools to clients, knowing I've chosen the right approach.
- **I want to feel empowered** to explore new framework features without fear of breaking things or wasting time.

### Social Jobs

- **I want to be seen as knowledgeable** about the framework by my team and clients, not as the "non-technical person who needs hand-holding."
- **I want to be recognized** for leveraging the framework to deliver high-quality discovery work faster than competitors.
- **I want to represent the framework professionally** when presenting to clients, with polished outputs and clear explanations.

## Behavioral Model (Fogg)

### Motivation
- **Core Driver**: Deliver exceptional product discovery work for clients while reducing manual effort. The framework promises to automate personas, JTBD, and requirements generation - if she can figure out how to use it.
- **Pain Avoidance**: Stop asking repetitive questions on Slack and looking incompetent in front of developers.
- **Aspiration**: Become a framework power user who can confidently guide clients through discovery without technical assistance.

### Ability
- **Medium Technical Skill**: Understands product workflows and can use command-line tools when guided, but not comfortable exploring raw file systems.
- **Time Constraint**: Client projects move fast - she needs answers in minutes, not hours.
- **Learning Preference**: Visual interfaces and search tools are 10x more effective for her than reading markdown files.

### Triggers
- **Spark**: When a colleague shows her a beautifully automated discovery output (personas, JTBD) that would have taken weeks to create manually.
- **Facilitator**: A searchable, stage-organized manual that answers "what tools exist for my current project phase?"
- **Signal**: Client asks "can you do X?" and she knows the framework can, but can't remember which tool to use.

## Product Implications

| Area | Implication |
|------|-------------|
| **UI Complexity** | Must prioritize discoverability over power-user features. Search and stage-based filtering are critical for Ana to find tools without developer help. |
| **Mobile Priority** | Medium - She may browse framework docs on her iPad during client meetings to quickly look up capabilities. |
| **Training Needs** | Needs "quick start" guides and visual workflow diagrams showing which tools apply to which project phases. |
| **Key Features** | Search (PP-1.3), stage-based organization (PP-1.4), tagging by capability (e.g., "compliance", "personas", "prototyping"), examples showing outputs. |
| **Success Metric** | Reduction in time spent searching for tools + increase in independent tool usage without asking developers. |

## Design Implications

1. **Search is Non-Negotiable**: Ana explicitly needs search functionality (CF-009, PP-1.3). She should be able to type "GDPR" or "personas" and see all relevant tools.
2. **Stage-Based Filtering**: Organize tools by Discovery, Prototype, Implementation, Utilities (CF-011). Ana wants to see "just discovery tools" when working on that phase.
3. **Tagging System**: Skills should be tagged with capabilities (e.g., "compliance", "personas", "testing") so she can find tools by intent, not by filename (CF-010).
4. **Visual Hierarchy**: Master pane showing stage categories, detail pane showing tool documentation with examples and "when to use this" guidance.
5. **Quick Reference**: Each tool should have a one-sentence summary visible in search results, so she doesn't have to open files to understand basic purpose.

---

## Traceability

- **User Type**: UT-002 (Product People)
- **Sources**: CM-001 (Interview Lines 6, 8-9)
- **Pain Points**: PP-1.3 (Discoverability Challenge), PP-1.4 (Organizational Chaos), PP-1.2 (Lack of Contextual Documentation)
- **Client Facts**: CF-009 (Search Functionality), CF-010 (Tagging System), CF-011 (Stage-Based Organization)
- **Generated**: 2026-01-31
- **Session**: disc-claude-manual-003
- **Checkpoint**: CP-3

---

*This persona represents the non-developer user who needs framework knowledge for client-facing product work. Her success depends on discoverability and visual organization, not technical documentation depth.*
