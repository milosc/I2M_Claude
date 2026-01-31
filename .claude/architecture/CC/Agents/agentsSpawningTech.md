While the `Task` tool is indeed how Claude Code delegates work to subagents, the specific JSON structure you've provided mixes two different concepts: **Manual tool-calling syntax** (what Claude uses internally) and **Subagent definition syntax** (how you configure them).

Here is the breakdown of the best approach for 2026.

## 1. Defining the Subagent

You shouldn't typically "hard-code" the `Task` tool call yourself in a prompt. Instead, you define the subagent so Claude knows it exists. The "best" way to do this is via a Markdown file, which allows you to check it into Git for your team.

**File:** `.claude/agents/my-agent.md`

```markdown
---
name: my-agent
description: Use this agent to [specific trigger condition]
model: sonnet
color: purple
---

# Role
You are an expert at [description].

# Context
- Base Directory: .
- Session Info: Use the provided environment variables for SESSION/TASK IDs.

# Rules
- Always return a JSON object with { status, files_written, issues }.
- Only edit files within the current scope.

```

## 2. Triggering the Subagent

Once defined, you don't need to write the `Task({...})` JSON. You simply tell Claude:

> *"Use my-agent to review the recent changes and verify the JSON schema."*

Claude will then automatically generate the `Task` tool call. If you are inspecting the logs or trying to force a specific call, the valid internal schema for the `Task` tool in Claude Code looks like this:

### The Correct `Task` Tool Schema

| Field | Description |
| --- | --- |
| **`subagent_type`** | The **name** of the agent you defined (e.g., `"my-agent"`) OR built-in types like `"general-purpose"`. |
| **`task`** | (Required) A clear instruction of what the subagent should do. |
| **`description`** | (Optional) A meta-description for the UI status line. |

> [!IMPORTANT]
> In your example, you used `prompt` inside the `Task` call. In the actual tool schema, the instructions go into the **`task`** field. The "System Prompt" is pulled from the `.md` file definition, not passed as a tool argument.

---

## 3. Dynamic "Ephemeral" Subagents

If you don't want to create a file and want to spawn a subagent via the CLI for a single session, use the `--agents` flag:

```bash
claude --agents '{
  "researcher": {
    "description": "Expert at scanning documentation",
    "prompt": "You are a research assistant. Focus on API specs.",
    "model": "haiku"
  }
}'

```

## Summary Table: Pro-Tips for Subagents

| Feature | Best Practice |
| --- | --- |
| **Model Selection** | Use **Haiku** for simple file-scanning/refactoring and **Sonnet** for logic-heavy tasks. |
| **Tool Access** | By default, subagents inherit all tools. Limit them in the `.md` frontmatter if they should only read (e.g., `tools: [Read, LS, Grep]`). |
| **Recursion** | **Note:** Subagents cannot currently spawn their own subagents (no nested `Task` calls). |
