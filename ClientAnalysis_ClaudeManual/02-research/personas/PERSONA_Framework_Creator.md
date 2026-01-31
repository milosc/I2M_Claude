# Persona: The Framework Evangelist

---
persona_id: PER-001
user_type_id: UT-001
priority: Primary
checkpoint: CP-3
source: CM-001
validated: true
---

## Profile

- **Name**: Miloš (Framework Creator)
- **Role**: Framework Creator/Maintainer
- **Experience**: 5+ years in enterprise software development, 2+ years building AI-assisted development frameworks
- **Technical Proficiency**: Expert (Architecture, Node.js, AI tooling, DevOps)
- **Team Responsibility**: Knowledge transfer to 10+ team members across product, engineering, and delivery roles

## Quote

> "I have to spread this knowledge to all my coworkers and just showing dot cloud skills. Folder command folder agents folder rules folder hooks folder et cetera."

## Background

Miloš is the architect and creator of the Claude framework - a comprehensive AI-assisted development system that transforms idea-to-market workflows. After successfully building the framework with 115+ skills, multi-agent orchestration, and sophisticated traceability systems, he now faces his biggest challenge: scaling knowledge transfer.

He's deeply technical but has learned that documentation alone isn't enough. Raw markdown files and folder structures make sense to him, but they create barriers for team members who need to learn by doing, not by reading source code. He values visual communication and believes in enabling self-service learning rather than becoming a bottleneck through manual training sessions.

His vision extends beyond just documenting the framework - he wants to create a learning experience that mirrors how people naturally discover and adopt new tools: through exploration, visual context, and interactive examples.

## Goals

### Primary Goals

1. **Enable Scalable Knowledge Transfer** - Allow team members to learn the framework independently without requiring manual training sessions for each person. (Traces to PP-1.1)
2. **Reduce Onboarding Time** - Cut framework onboarding from 3-4 hours of manual training to 30-60 minutes of self-guided exploration. (Traces to PP-1.1, PP-1.2)
3. **Create Self-Service Documentation** - Build an interactive manual that answers "what can I do?", "how do I use this?", and "when should I use this?" without requiring human intervention. (Traces to PP-1.2)

### Secondary Goals

1. **Improve Framework Adoption Rate** - Increase the percentage of team members who actively use framework tools from 30% to 80%+ within 30 days of introduction.
2. **Establish Best Practice Patterns** - Document and visualize the relationships between skills, commands, agents, and workflow stages so users understand the "right way" to use the framework.
3. **Enable Distributed Contribution** - Make it easy for developers to find and edit source files, fostering a culture of framework improvement and customization. (Traces to PP-1.6)

## Frustrations

### High Priority

- **Knowledge Transfer Complexity** (PP-1.1): Spending 3-4 hours per person doing manual demonstrations of folder structures is not scalable. Each new team member requires the same repetitive explanation of what `.claude/skills/`, `.claude/commands/`, `.claude/agents/`, and `.claude/hooks/` do and how they relate to each other. This creates a bottleneck where framework adoption is limited by Miloš's availability.

- **Lack of Contextual Documentation** (PP-1.2): Individual markdown files exist, but they don't explain relationships, usage patterns, or workflow contexts. Users read a skill definition but don't understand when to use it versus a command, or how it fits into the discovery vs. implementation stage. The documentation is optimized for AI agent consumption (Claude Code), not human learning.

### Medium Priority

- **No Visual Representation** (PP-1.1, PP-1.2): Explaining hierarchies and relationships verbally is inefficient. Users struggle to understand the mental model of how skills compose into workflows, how agents coordinate tasks, and which tools apply to which project stages.

- **Inability to Scale Training** (PP-1.1): Cannot onboard multiple team members in parallel. Each training session requires his direct involvement, preventing him from working on framework improvements or client projects.

## Day in the Life

### Morning (8:00 AM - 12:00 PM)

Miloš starts his day reviewing a Slack message from a new product manager asking, "Which framework tool should I use for generating personas from interview transcripts?" He knows the answer is `/discovery-multiagent` or the `Discovery_GeneratePersona` skill, but explaining this requires a 20-minute video call to show the folder structure, explain the difference between skills and commands, and demonstrate the workflow.

After the call, he gets a similar question from a developer who wants to customize the code review agent. Miloš spends another 15 minutes explaining that agents are in `.claude/agents/`, showing the file path, and walking through the agent definition structure. He realizes this is the third time this week he's explained the same concept.

By 11:00 AM, he's blocked on his actual work - improving the implementation phase orchestrator - because he's spent the morning doing manual knowledge transfer.

### Afternoon (12:00 PM - 6:00 PM)

In the afternoon, Miloš has scheduled a framework onboarding session for three new team members (a developer, a product owner, and a delivery manager). He opens VSCode, shares his screen, and walks through the folder structure:

1. Shows `.claude/skills/` - explains what skills are
2. Shows `.claude/commands/` - explains how commands orchestrate skills
3. Shows `.claude/agents/` - explains multi-agent coordination
4. Shows example workflows for Discovery, Prototype, and Implementation stages

The session takes 3.5 hours. The team members take notes but admit they'll need to reference his recordings because there's too much to remember. Miloš knows that in two weeks, they'll come back with the same questions because the documentation doesn't provide the visual hierarchy and interactive exploration they need.

By 5:00 PM, he's frustrated. He's spent 5+ hours today on knowledge transfer instead of building features. He realizes this doesn't scale.

### Key Moments

- **Peak Stress**: 11:00 AM - Realizes he's answered the same "where is this file?" question three times in one week, blocking his actual work.
- **Peak Satisfaction**: When a team member successfully runs their first framework command without asking for help (rare, but deeply rewarding).
- **System Touchpoints**:
  - Slack (answering framework questions)
  - VSCode (showing file structures during training)
  - Zoom (screen sharing for onboarding sessions)
  - GitHub (reviewing PRs where team members misused framework tools)

## Technology Profile

| Aspect | Details |
|--------|---------|
| **Primary Devices** | MacBook Pro, Terminal-heavy workflow |
| **Preferred Apps** | VSCode, iTerm2, Obsidian (personal notes), Slack, Claude Code |
| **Pain with Tech** | Hates repetitive manual tasks, frustrated by tools that don't scale |
| **Learning Style** | Self-taught, values visual diagrams and interactive exploration over reading documentation |

## Quotes

> "I want to have this very visual" - On documentation approach (CF-003)

> "So there are like two pains. View. Master and Little Pain." - On ideal UI structure for hierarchical content (CF-006)

> "it has multiple sections explaining the front matter, explaining why and for what is this agent skill or command...showing example how to run what are the options high level workflow diagram" - On documentation depth requirements (CF-008)

## Jobs to Be Done

### Functional Jobs

- **When I need to onboard a new team member**, I want to send them a link to an interactive manual, so I can avoid spending 3-4 hours on manual training.
- **When a team member asks "how do I use this?"**, I want to point them to a visual guide with examples, so I don't have to repeat the same explanation.
- **When the framework evolves**, I want documentation to update automatically from source files, so I don't maintain two separate systems.

### Emotional Jobs

- **I want to feel confident** that team members can learn the framework independently without breaking things.
- **I want to feel proud** when I show the framework to external stakeholders, not embarrassed by raw folder structures.
- **I want to feel relief** knowing that framework knowledge is preserved even if I'm unavailable.

### Social Jobs

- **I want to be seen as an enabler**, not a bottleneck, by my team.
- **I want to be recognized** for creating a framework that's easy to adopt, not just powerful.
- **I want the framework to represent professionalism** when demonstrated to clients and executives.

## Behavioral Model (Fogg)

### Motivation
- **Core Driver**: Scale impact beyond his individual capacity. He built a powerful framework but realizes it's useless if others can't adopt it.
- **Pain Avoidance**: Stop being interrupted with the same questions repeatedly.
- **Aspiration**: Create a framework that becomes the standard for AI-assisted development at the company.

### Ability
- **High Technical Skill**: Can build complex systems, write documentation, and design workflows.
- **Time Constraint**: Only has nights/weekends for framework improvements due to client project load.
- **Design Gap**: Strong technical skills but lacks UI/UX design expertise for creating visual documentation.

### Triggers
- **Spark**: When a team member succeeds independently, it proves the value of self-service learning.
- **Facilitator**: Seeing other framework creators publish beautiful documentation sites (like Next.js, React, Tailwind docs).
- **Signal**: Repeated questions in Slack about the same topics - signals that documentation isn't working.

## Product Implications

| Area | Implication |
|------|-------------|
| **UI Complexity** | Must be simple enough for non-technical users (product people, executives) but powerful enough for developers. Dual-pane master-detail interface is critical. |
| **Mobile Priority** | Low - Primary use case is desktop during onboarding sessions or self-guided learning at workstation. |
| **Training Needs** | The product IS the training system. It must be self-explanatory with zero onboarding. |
| **Key Features** | Visual hierarchy (master pane), multi-section documentation (detail pane), search, stage-based filtering, source file paths for developers. |
| **Success Metric** | Reduction in Slack questions about framework usage + increase in successful independent command executions. |

## Design Implications

1. **Visual-First Interface**: Miloš explicitly stated "I want to have this very visual" - diagrams, hierarchies, and workflow visualizations are non-negotiable.
2. **Dual-Pane Layout**: Master pane for navigation, detail pane for content (CF-006).
3. **Multi-Section Documentation**: Each item must show frontmatter, purpose, examples, options, and workflow diagrams (CF-008).
4. **Search is Critical**: Without search, users default to asking Miloš questions (PP-1.3).
5. **Stage-Based Organization**: Discovery, Prototype, Implementation, Utilities must be visually distinct (CF-011).
6. **Modern Minimalistic Terminal Look**: Clean, developer-friendly aesthetic (CF-014).

---

## Traceability

- **User Type**: UT-001 (Framework Creator/Maintainer)
- **Sources**: CM-001 (Interview Lines 2-9)
- **Pain Points**: PP-1.1 (Knowledge Transfer Complexity), PP-1.2 (Lack of Contextual Documentation), PP-1.6 (Developer Friction)
- **Client Facts**: CF-001, CF-002, CF-003, CF-006, CF-008, CF-014
- **Generated**: 2026-01-31
- **Session**: disc-claude-manual-003
- **Checkpoint**: CP-3

---

*This persona represents the primary stakeholder and creator of the Claude framework. His success in scaling knowledge transfer directly determines framework adoption across the organization.*
