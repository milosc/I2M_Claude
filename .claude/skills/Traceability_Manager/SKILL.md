---
name: Traceability_Manager
description: Manages the central "Memory" of the project by updating the traceability registries. Supports full lifecycle tracing from Discovery to Specification.
model: sonnet
allowed-tools: Bash, Edit, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Traceability_Manager started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Traceability_Manager ended '{"stage": "utility"}'
---

# Traceability Manager Skill

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill Traceability_Manager instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

## Purpose
Acts as the **Memory Keeper** for the project. Ensures 100% traceability from raw client facts to code modules and tests.

## Available Actions

### 1. Initialize Memory
Resets or creates the `traceability/` directory structure and 12 core registries.
```bash
python .claude/skills/tools/traceability_manager.py init
```

### 2. Register Item
Adds or Updates an item in a registry.
```bash
python .claude/skills/tools/traceability_manager.py add <category> '<json_data>'
```

**Categories**:
- `client_facts`: Raw facts from discovery
- `pain_points`: Identified pain points (PP-*)
- `jtbd`: Jobs to be Done (JTBD-*)
- `requirements`: User Stories/Functional Reqs (US-*, FR-*)
- `screens`: UI Screen IDs (S-*)
- `modules`: Code Modules (MOD-*)
- `adrs`: Architectural Decisions (ADR-*)
- `components`: Stage 2 Prototype components
- `test_cases`: Stage 3 Test cases

### 3. Link Items
Creates a directional traceability link in `trace_links.json`.
```bash
python .claude/skills/tools/traceability_manager.py link <source_id> <target_id> <type>
```

### 4. Smart Gap Analysis
Analyzes registries for missing upstream or downstream links.
```bash
python .claude/skills/tools/traceability_manager.py analyze-gaps
```

### 5. Visualize
Generates high-quality Markdown visualizations and updates `helperFiles/`.
```bash
python .claude/skills/tools/traceability_manager.py visualize
```

## Outputs
- `traceability/*.json`: The 12 core registries.
- `traceability/*.md`: Visual reports (PROTOTYPE, SPECIFICATION, GAP_ANALYSIS, etc.).
- `helperFiles/*.md`: Project-level reports updated stage-by-stage.
