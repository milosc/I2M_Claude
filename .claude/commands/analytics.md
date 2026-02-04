---
name: analytics
description: "Generate phase execution time analytics and reports for comparing Discovery, Prototype, ProductSpecs, SolArch, and Implementation execution times"
aliases: ["phase-analytics", "timing-report", "execution-times"]
stage: utility
---

# /analytics Command

Generate execution time analytics for HTEC Agentic Accelerator Framework phases.

## Usage

```bash
# Capture current run data and update benchmarks
/analytics capture <SystemName>

# Generate Markdown report with charts and trends
/analytics report <SystemName>

# Generate interactive HTML dashboard
/analytics dashboard <SystemName>

# Compare current run against historical benchmarks
/analytics compare <SystemName>

# Show all systems with analytics data
/analytics status

# Full analysis (capture + report + dashboard)
/analytics full <SystemName>
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `command` | Yes | One of: `capture`, `report`, `dashboard`, `compare`, `status`, `full` |
| `SystemName` | For most commands | The system name (e.g., ERTriage, InventorySystem) |

## Commands

### `capture`
Captures timing data from the current pipeline state and updates benchmarks.

**Sources**:
- `_state/pipeline_progress.json` - Event timestamps and hierarchy
- `_state/{stage}_progress.json` - Checkpoint timing
- `_state/lifecycle.json` - Tool and agent execution times

**Outputs**:
- `analytics/runs/{SystemName}_run_{timestamp}.json` - Run snapshot
- `analytics/benchmarks/{SystemName}_benchmarks.json` - Updated benchmarks

### `report`
Generates a comprehensive Markdown report with:
- Executive summary
- Stage execution times with ASCII bar charts
- Agent and command performance tables
- Trend analysis with Mermaid charts
- Bottleneck identification

**Output**: `analytics/reports/{SystemName}_report_{timestamp}.md`

### `dashboard`
Generates an interactive HTML dashboard with Chart.js visualizations:
- Stage execution time bar chart
- Trend line chart
- Agent performance horizontal bar chart
- Command performance chart
- Detailed tables

**Output**: `analytics/reports/{SystemName}_dashboard_{timestamp}.html`

### `compare`
Compares the current run against historical benchmarks and shows:
- Performance delta (faster/slower/similar)
- Percentage difference from average
- Agent and command comparison

### `status`
Shows all systems with analytics data:
- Number of runs
- Stages tracked
- Last update time
- Trend direction per stage

### `full`
Runs complete analysis workflow:
1. Captures current run data
2. Generates Markdown report
3. Generates HTML dashboard

## Examples

```bash
# After completing a Discovery run
/analytics capture ERTriage

# View analytics status
/analytics status

# Generate full analysis after Implementation
/analytics full InventorySystem

# Compare current run to history
/analytics compare ERTriage
```

## Output Structure

```
analytics/
├── runs/                           # Historical run snapshots
│   ├── ERTriage_run_20260203_143052.json
│   └── InventorySystem_run_20260202_091530.json
├── benchmarks/                     # Aggregated benchmark data
│   ├── ERTriage_benchmarks.json
│   └── InventorySystem_benchmarks.json
└── reports/                        # Generated reports
    ├── ERTriage_report_20260203_143100.md
    ├── ERTriage_dashboard_20260203_143100.html
    └── ...
```

## Benchmark Data

Benchmarks include:
- **Per-stage statistics**: runs, avg/min/max duration, trend
- **Per-agent statistics**: invocations, avg duration
- **Per-command statistics**: invocations, avg duration
- **History**: Last 100 runs for trend calculation

## Trend Detection

Trends are calculated using linear regression:
- **Improving**: Execution time decreasing (getting faster)
- **Degrading**: Execution time increasing (getting slower)
- **Stable**: Within 5% of average (consistent)

## Integration

This command integrates with the existing logging infrastructure:
- `command_start.py` / `command_end.py` hooks
- `skill_invoke.py` hooks
- Stage progress files
- Lifecycle event tracking

---

## Implementation

```bash
# Parse arguments
COMMAND="$1"
SYSTEM_NAME="$2"
PROJECT_ROOT="${3:-.}"

# Run analytics CLI
python3 .claude/tools/phase_analytics/cli.py "$COMMAND" "$SYSTEM_NAME" --project-root "$PROJECT_ROOT"
```
