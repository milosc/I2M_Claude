---
description: Generate Discovery analysis summary documentation
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Edit
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-analysis-summary started '{"stage": "discovery"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /discovery-analysis-summary ended '{"stage": "discovery"}'
---


# /discovery-analysis-summary - Generate Analysis Summary

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --project "{SystemName}" --stage "discovery"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /discovery-analysis-summary instruction_start '{"stage": "discovery", "method": "instruction-based"}'
```

## Rules Loading (On-Demand)

This command requires Discovery-specific rules. Load them now:

```bash
# Load Discovery rules (includes PDF handling, input processing, output structure)
/rules-discovery

# Load Traceability rules (includes ID formats, source linking)
/rules-traceability
```

## Arguments

None required - reads configuration from `_state/discovery_config.json`

## Prerequisites

- Materials analyzed (phase 1 complete or in progress)
- `_state/discovery_materials_inventory.json` exists
- Traceability registries have been populated

## Skills Used

- `.claude/skills/Discovery_ExtractPainPoints/Discovery_ExtractPainPoints.md`
- `.claude/skills/Discovery_ExtractUserTypes/Discovery_ExtractUserTypes.md`
- `.claude/skills/Discovery_ExtractWorkflows/Discovery_ExtractWorkflows.md`
- `.claude/skills/Discovery_ExtractQuotes/Discovery_ExtractQuotes.md`
- `.claude/skills/Discovery_ExtractMetrics/Discovery_ExtractMetrics.md`

## Execution Steps

1. **Load State**
   - Read `_state/discovery_config.json` for output_path
   - Read `_state/discovery_materials_inventory.json` for file summary
   - Read all traceability registries for extracted data

2. **Read All Extract Skills**
   - Understand output formats and consolidation approach

3. **Generate Analysis Summary**
   - Create `ClientAnalysis_<SystemName>/01-analysis/ANALYSIS_SUMMARY.md`
   - Include version metadata:
     ```yaml
     ---
     document_id: DISC-ANALYSIS-<SystemName>
     version: 1.0.0
     created_at: <YYYY-MM-DD>
     updated_at: <YYYY-MM-DD>
     generated_by: Discovery_Extract*
     source_files:
       - <list of processed input files>
     ---
     ```

4. **Content Structure**
   ```markdown
   # Analysis Summary - <SystemName>

   ## Executive Summary
   [Brief overview of findings]

   ## Materials Analyzed
   | Type | Count | Files |
   |------|-------|-------|
   | Interviews | N | file1.md, file2.md |
   ...

   ## Pain Points Summary
   | Severity | Count | Key Issues |
   |----------|-------|------------|
   | P0 | N | ... |
   | P1 | N | ... |
   | P2 | N | ... |

   ## User Types Identified
   [List with brief descriptions]

   ## Key Workflows
   [Summary of current-state workflows]

   ## Notable Quotes
   [Top impactful quotes by category]

   ## Metrics & Data
   [Quantified impacts and business metrics]

   ## Data Gaps
   [Missing information, skipped files impact]
   ```

## State Updates

- Update `discovery_progress.json` if this completes phase 2

## Outputs

- `ClientAnalysis_<SystemName>/01-analysis/ANALYSIS_SUMMARY.md`

## Next Command

- Run `/discovery-personas` to generate persona files
- Or run `/discovery-research` for full research phase
