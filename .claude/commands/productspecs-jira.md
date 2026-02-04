---
name: productspecs-jira
description: Generate JIRA-ready CSV/JSON export with full traceability
model: claude-sonnet-4-5-20250929
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-jira started '{"stage": "productspecs"}'
  Stop:
    - hooks:
        - type: command
          command: >-
            uv run "$CLAUDE_PROJECT_DIR/.claude/hooks/validators/validate_files_exist.py"
            --directory "ProductSpecs_$1/04-jira"
            --requires "*.csv"
            --requires "IMPORT_GUIDE.md"
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /productspecs-jira ended '{"stage": "productspecs"}'
---


# /productspecs-jira - JIRA Export Utility

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "productspecs"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /productspecs-jira instruction_start '{"stage": "productspecs", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires traceability rules for module/test ID management:

```bash
# Load Traceability rules (includes module ID format MOD-XXX-XXX-NN)
/rules-traceability
```

## Description

This is a lightweight utility command for regenerating JIRA exports without running the full ProductSpecs pipeline. Use this when:
- You need to regenerate JIRA files with different configuration
- You want to change the sub-task strategy
- You need to update project key or name
- You want to export a subset of items

## Arguments

- `$ARGUMENTS` - Required: `<SystemName> [options]`

## Options

| Option | Description |
|--------|-------------|
| `--reconfigure` | Force reconfiguration of JIRA settings |
| `--strategy <strategy>` | Override sub-task strategy |
| `--no-subtasks` | Generate without sub-tasks |
| `--epics-only` | Generate only epics |
| `--stories-only` | Generate epics and stories (no sub-tasks) |
| `--priority <P0\|P1\|P2>` | Filter by priority |

## Prerequisites

- ProductSpecs registries must exist:
  - `ProductSpecs_<SystemName>/_registry/modules.json`
  - `ProductSpecs_<SystemName>/_registry/requirements.json`

## Execution Steps

### Step 1: Validate Registries Exist

```python
output_path = f"ProductSpecs_{system_name}"

required_files = [
    f"{output_path}/_registry/modules.json",
    f"{output_path}/_registry/requirements.json"
]

for file in required_files:
    if not exists(file):
        print(f"ERROR: Required registry not found: {file}")
        print("Run /productspecs-modules first to generate registries.")
        exit(1)
```

### Step 2: Load Registries

```python
modules = json.load(f"{output_path}/_registry/modules.json")
requirements = json.load(f"{output_path}/_registry/requirements.json")

# Optional registries (for richer export)
nfrs = json.load(f"{output_path}/_registry/nfrs.json") if exists(...) else None
test_cases = json.load(f"{output_path}/_registry/test-cases.json") if exists(...) else None
traceability = json.load(f"{output_path}/_registry/traceability.json") if exists(...) else None
```

### Step 3: Handle Configuration

```python
jira_config_path = f"{output_path}/04-jira/jira_config.json"

if args.reconfigure or not exists(jira_config_path):
    # Prompt for configuration
    jira_config = collect_jira_config()
    write_json(jira_config_path, jira_config)
else:
    jira_config = json.load(jira_config_path)
    print(f"Using existing configuration: {jira_config_path}")

# Apply command-line overrides
if args.strategy:
    jira_config["subtask_strategy"] = args.strategy
if args.no_subtasks:
    jira_config["generate_subtasks"] = False
```

### Step 4: Apply Filters

```python
# Filter by priority if specified
if args.priority:
    requirements["requirements"] = [
        r for r in requirements["requirements"]
        if r["priority"] == args.priority
    ]
    print(f"Filtered to {len(requirements['requirements'])} {args.priority} requirements")

# Filter modules that have matching requirements
if args.priority:
    req_ids = {r["id"] for r in requirements["requirements"]}
    modules["modules"] = [
        m for m in modules["modules"]
        if any(r in req_ids for r in m.get("requirements", []))
    ]
```

### Step 5: Generate JIRA Hierarchy

```python
# Determine what to generate based on options
if args.epics_only:
    generate_epics_only(modules, jira_config)
elif args.stories_only:
    generate_epics_and_stories(modules, requirements, jira_config)
else:
    generate_full_hierarchy(modules, requirements, jira_config)
```

### Step 6: Write Export Files

Create/update files in `ProductSpecs_<SystemName>/04-jira/`:

```python
# Always generate these
write_csv(f"{output_path}/04-jira/full-hierarchy.csv", hierarchy)
write_json(f"{output_path}/04-jira/jira-import.json", hierarchy)

# Conditional files
if not args.epics_only:
    write_csv(f"{output_path}/04-jira/epics-and-stories.csv", epics_stories)

if jira_config.get("generate_subtasks") and not args.no_subtasks:
    write_csv(f"{output_path}/04-jira/subtasks-only.csv", subtasks)
```

### Step 7: Update Import Guide

Regenerate `IMPORT_GUIDE.md` with current configuration and counts.

### Step 8: Display Summary

```
═══════════════════════════════════════════════════════════════
  JIRA EXPORT GENERATED
═══════════════════════════════════════════════════════════════

  System:          <SystemName>
  Configuration:
  ──────────────────────────────────────────────────────────────
  │ Setting             │ Value                    │
  │─────────────────────│──────────────────────────│
  │ Project Key         │ INV                      │
  │ Sub-task Strategy   │ by-discipline            │
  │ Generate Sub-tasks  │ Yes                      │
  │ Priority Filter     │ All                      │

  Generated Items:
  ──────────────────────────────────────────────────────────────
  │ Type              │ Count │
  │───────────────────│───────│
  │ Epics             │ 12    │
  │ Stories           │ 45    │
  │ Sub-tasks         │ 180   │
  │ Total             │ 237   │

  Files Generated:
  • 04-jira/full-hierarchy.csv
  • 04-jira/epics-and-stories.csv
  • 04-jira/subtasks-only.csv
  • 04-jira/jira-import.json
  • 04-jira/IMPORT_GUIDE.md

═══════════════════════════════════════════════════════════════
```

## Examples

### Basic Usage

```bash
# Generate with existing or new configuration
/productspecs-jira InventorySystem
```

### Reconfigure JIRA Settings

```bash
# Force reconfiguration of project key, name, strategy
/productspecs-jira InventorySystem --reconfigure
```

### Change Sub-task Strategy

```bash
# Use different sub-task strategy
/productspecs-jira InventorySystem --strategy by-component
/productspecs-jira InventorySystem --strategy by-acceptance-criteria
/productspecs-jira InventorySystem --strategy comprehensive
```

### Export Without Sub-tasks

```bash
# Generate only epics and stories
/productspecs-jira InventorySystem --no-subtasks
# OR
/productspecs-jira InventorySystem --stories-only
```

### Export Epics Only

```bash
# Generate only epics (for high-level planning)
/productspecs-jira InventorySystem --epics-only
```

### Filter by Priority

```bash
# Export only P0 items
/productspecs-jira InventorySystem --priority P0

# Export P0 and P1 items (run twice and merge)
/productspecs-jira InventorySystem --priority P0
/productspecs-jira InventorySystem --priority P1
```

## Sub-task Strategies

| Strategy | Description | Use When |
|----------|-------------|----------|
| `by-discipline` | FE, BE, QA, A11Y, DOC, REV | Standard development teams |
| `by-component` | One sub-task per UI component | Component-based development |
| `by-acceptance-criteria` | One sub-task per AC | Acceptance-driven development |
| `comprehensive` | All of the above (deduplicated) | Complex projects |

## Outputs

| File | Description |
|------|-------------|
| `full-hierarchy.csv` | Complete hierarchy for single import |
| `epics-and-stories.csv` | Epics and Stories only |
| `subtasks-only.csv` | Sub-tasks for two-phase import |
| `jira-import.json` | JSON format for API import |
| `IMPORT_GUIDE.md` | Step-by-step import instructions |
| `jira_config.json` | Saved configuration |

## Error Handling

| Error | Action |
|-------|--------|
| Missing modules.json | **BLOCK** - Run /productspecs-modules |
| Missing requirements.json | **BLOCK** - Run /productspecs-extract |
| Invalid strategy | **WARN** - Use default (by-discipline) |
| Empty after filter | **WARN** - Show count, generate empty files |

## Comparison with /productspecs-export

| Feature | /productspecs-jira | /productspecs-export |
|---------|-------------------|---------------------|
| Checkpoint validation | No | Yes (requires CP7) |
| Traceability validation | No | Yes |
| Generation summary | No | Yes |
| Configuration prompt | On first run | Always if missing |
| Speed | Fast | Full pipeline |
| Use case | Quick regeneration | Full export with validation |

## Related Commands

| Command | Description |
|---------|-------------|
| `/productspecs-export` | Full export with validation |
| `/productspecs-modules` | Generate module specs |
| `/productspecs-finalize` | Validate traceability |
| `/productspecs-status` | Show current progress |
