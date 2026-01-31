# Monitoring and Usage Tracking Implementation

This document describes the pipeline monitoring and usage tracking features implemented for the i2m_accelerators_agentic framework.

## Overview

Two major features have been implemented:

1. **Pipeline Status Awareness**: Real-time logging of all activities (commands, agents, skills) to `pipeline_progress.json` with hierarchical tracking
2. **Usage Monitoring**: Automated tracking of token usage and costs with detailed attribution by model, stage, command, agent, and skill

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   MONITORING SYSTEM                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐        ┌──────────────────┐          │
│  │ PIPELINE LOGGER  │        │ USAGE MONITOR    │          │
│  │                  │        │ DAEMON           │          │
│  │ - Thread-safe    │        │                  │          │
│  │ - Hierarchical   │        │ - Polls /usage   │          │
│  │ - Event-driven   │        │ - 5-min interval │          │
│  │                  │        │ - Attribution    │          │
│  └────────┬─────────┘        └────────┬─────────┘          │
│           │                           │                     │
│           ▼                           ▼                     │
│  ┌────────────────────────────────────────────┐            │
│  │          STATE FILES                       │            │
│  │  - pipeline_progress.json                  │            │
│  │  - usage_stats.json                        │            │
│  │  - usage_pricing.json                      │            │
│  └────────────────────────────────────────────┘            │
│           │                           │                     │
│           ▼                           ▼                     │
│  ┌────────────────────────────────────────────┐            │
│  │          QUERY APIs                        │            │
│  │  - pipeline_query_api.py                   │            │
│  │  - usage_query_api.py                      │            │
│  │  - usage_attribution.py                    │            │
│  └────────────────────────────────────────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Files Implemented

### Core Modules

1. **`_state/pipeline_logger.py`** (400+ lines)
   - Thread-safe event logging with singleton pattern
   - Hierarchical activity tracking
   - Context manager for automatic start/end logging
   - Error and warning logging
   - File rotation at 50MB
   - Statistics tracking

2. **`_state/usage_monitor_daemon.py`** (500+ lines)
   - Background daemon for polling `/usage` command
   - 5-minute polling interval
   - Snapshot tracking with history
   - Hourly and daily aggregation
   - Alert system for cost thresholds
   - PID-based lifecycle management

3. **`_state/usage_attribution.py`** (400+ lines)
   - Correlates usage with pipeline events
   - Provides breakdowns by: model, stage, command, agent, skill
   - Top consumers analysis
   - Report generation

4. **`_state/usage_pricing.json`**
   - Model pricing configuration
   - Alert thresholds
   - Budget limits
   - Optimization recommendations

### Integration Hooks

5. **`.claude/hooks/command_start.py`**
   - Logs command start events
   - CLI interface for command integration

6. **`.claude/hooks/command_end.py`**
   - Logs command end events with results
   - Status tracking (completed/failed/cancelled)

7. **`.claude/hooks/skill_invoke.py`**
   - Logs skill invocation events
   - Context manager for automatic logging
   - Manual logging functions

8. **Updated: `.claude/hooks/pre_agent_spawn.py`**
   - Added pipeline logging integration
   - Logs agent_spawn_start events

9. **Updated: `.claude/hooks/post_task_completion.py`**
   - Added pipeline logging integration
   - Logs agent_spawn_end events with duration

### Utility Scripts

10. **`_state/start_monitors.sh`**
    - Starts all monitoring daemons
    - Verifies daemon status

11. **`_state/stop_monitors.sh`**
    - Gracefully stops all daemons

12. **`_state/pipeline_query_api.py`** (500+ lines)
    - Query pipeline progress data
    - Get active activities, events, hierarchy
    - Generate summary reports

13. **`_state/usage_query_api.py`** (500+ lines)
    - Query usage statistics
    - Get breakdowns, trends, top consumers
    - Generate usage reports

14. **`_state/test_logging.py`**
    - Comprehensive test suite
    - Verifies all logging functionality

## Data Schemas

### pipeline_progress.json

```json
{
  "schema_version": "1.0.0",
  "system_name": "SystemName",
  "stage": "prototype",
  "pipeline_started_at": "2026-01-10T12:00:00Z",
  "pipeline_updated_at": "2026-01-10T12:30:00Z",
  "pipeline_status": "running",
  "current_context": {
    "stage": "prototype",
    "system_name": "SystemName",
    "checkpoint": 5
  },
  "statistics": {
    "total_events": 150,
    "total_commands": 3,
    "total_agents_spawned": 12,
    "total_skills_invoked": 8,
    "total_errors": 0,
    "total_warnings": 2
  },
  "events": [
    {
      "event_id": "evt-abc123",
      "event_type": "command_start",
      "timestamp": "2026-01-10T12:00:00Z",
      "level": "command",
      "parent_event_id": null,
      "activity": {
        "type": "command",
        "name": "/prototype",
        "intent": "Generate prototype from discovery",
        "stage": "prototype"
      },
      "context": {
        "stage": "prototype",
        "system_name": "SystemName"
      },
      "hierarchy": {
        "depth": 0,
        "path": []
      }
    }
  ]
}
```

### usage_stats.json

```json
{
  "schema_version": "1.0.0",
  "monitoring_started_at": "2026-01-10T12:00:00Z",
  "last_updated_at": "2026-01-10T12:30:00Z",
  "poll_interval_seconds": 300,
  "totals": {
    "total_tokens_input": 1000000,
    "total_tokens_output": 500000,
    "total_cost": 45.50,
    "currency": "USD",
    "sessions_tracked": 25
  },
  "by_model": {
    "claude-sonnet-4-5-20250929": {
      "model_name": "Claude Sonnet 4.5",
      "input_tokens": 800000,
      "output_tokens": 400000,
      "cost": 35.00,
      "requests": 20
    }
  },
  "by_stage": {
    "prototype": {
      "input_tokens": 500000,
      "output_tokens": 300000,
      "cost": 25.00,
      "requests": 15
    }
  },
  "hourly_breakdown": [],
  "daily_breakdown": [],
  "snapshots": [],
  "alerts": []
}
```

## Usage

### Starting Monitoring Services

```bash
# Start all monitoring daemons
bash _state/start_monitors.sh

# Check daemon status
python3 _state/usage_monitor_daemon.py status
```

### Stopping Monitoring Services

```bash
# Stop all daemons gracefully
bash _state/stop_monitors.sh
```

### Querying Pipeline Status

```bash
# Get current status
python3 _state/pipeline_query_api.py status

# Get active activities
python3 _state/pipeline_query_api.py active

# Get recent events
python3 _state/pipeline_query_api.py events --recent 60

# Get event hierarchy
python3 _state/pipeline_query_api.py hierarchy --event-id evt-abc123

# Get statistics
python3 _state/pipeline_query_api.py stats

# Generate summary report
python3 _state/pipeline_query_api.py summary

# Get errors and warnings
python3 _state/pipeline_query_api.py errors
```

### Querying Usage Statistics

```bash
# Get overall totals
python3 _state/usage_query_api.py totals

# Get breakdown by category
python3 _state/usage_query_api.py breakdown --by model
python3 _state/usage_query_api.py breakdown --by stage
python3 _state/usage_query_api.py breakdown --by command
python3 _state/usage_query_api.py breakdown --by agent
python3 _state/usage_query_api.py breakdown --by skill

# Get time-series data
python3 _state/usage_query_api.py hourly --hours 24
python3 _state/usage_query_api.py daily --days 30

# Get top consumers
python3 _state/usage_query_api.py top --by model --limit 10
python3 _state/usage_query_api.py top --by agent --limit 10

# Get cost trend
python3 _state/usage_query_api.py trend --days 7

# Get recent alerts
python3 _state/usage_query_api.py alerts

# Generate full report
python3 _state/usage_query_api.py report
```

### Usage Attribution Report

```bash
# Generate attribution report
python3 _state/usage_attribution.py report

# Get breakdowns
python3 _state/usage_attribution.py top-models
python3 _state/usage_attribution.py top-stages
python3 _state/usage_attribution.py top-commands
python3 _state/usage_attribution.py top-agents
python3 _state/usage_attribution.py top-skills
```

### Programmatic Usage

#### Pipeline Logging

```python
from _state.pipeline_logger import get_logger

logger = get_logger()

# Set context
logger.set_context(stage="prototype", system_name="EmergencyTriage")

# Using context manager (recommended)
with logger.activity_context("command", "command", {
    "type": "command",
    "name": "/prototype",
    "intent": "Generate prototype"
}):
    # Your command logic here
    pass
# Automatically logs start and end with duration

# Manual logging
event_id = logger.log_event(
    event_type="command_start",
    level="command",
    activity={"type": "command", "name": "/test"},
    context={"stage": "test"}
)

# Log error
logger.log_error(
    error_type="ValidationError",
    message="Invalid input",
    severity="high",
    recovery={"action": "skip", "fallback": "default"}
)

# Log warning
logger.log_warning(
    warning_type="DeprecationWarning",
    message="Using deprecated API",
    severity="medium"
)

# Get active activities
active = logger.get_active_activities()
```

#### Skill Invocation

```python
from .claude.hooks.skill_invoke import log_skill_execution

# Context manager (automatic start/end)
with log_skill_execution("Prototype_Builder", "Generate prototype") as event_id:
    # Your skill logic here
    pass
```

#### Query APIs

```python
from _state.pipeline_query_api import PipelineQueryAPI
from _state.usage_query_api import UsageQueryAPI

# Pipeline queries
pipeline_api = PipelineQueryAPI()
status = pipeline_api.get_status()
active = pipeline_api.get_active_activities()
hierarchy = pipeline_api.get_event_hierarchy("evt-abc123")
report = pipeline_api.generate_summary_report()

# Usage queries
usage_api = UsageQueryAPI()
totals = usage_api.get_totals()
by_model = usage_api.get_breakdown("model")
trend = usage_api.get_cost_trend(days=7)
top_agents = usage_api.get_top_consumers("agent", limit=10)
report = usage_api.generate_report()
```

## Integration with Commands

Commands should integrate logging by calling the hooks:

```bash
# In your command implementation

# Start command
CMD_EVENT_ID=$(python3 .claude/hooks/command_start.py \
  --command-name "/my-command" \
  --stage "mystage" \
  --system-name "MySystem" \
  --intent "Do something useful")

# ... command logic ...

# End command
python3 .claude/hooks/command_end.py \
  --command-name "/my-command" \
  --stage "mystage" \
  --status "completed" \
  --start-event-id "$CMD_EVENT_ID" \
  --outputs '{"files_created": 10, "checkpoint": 5}'
```

## Event Levels

The logging system supports multiple event levels:

- **command**: Top-level command execution
- **agent**: Agent spawns and completions
- **skill**: Skill invocations
- **checkpoint**: Checkpoint transitions
- **error**: Error events
- **warning**: Warning events
- **info**: Informational events

## Event Types

### Start/End Pairs

- `command_start` / `command_end`
- `agent_spawn_start` / `agent_spawn_end`
- `skill_invoke_start` / `skill_invoke_end`
- `checkpoint_start` / `checkpoint_end`

### Standalone Events

- `error`
- `warning`
- `info`

## Features

### Pipeline Logger Features

- ✅ Thread-safe event logging
- ✅ Hierarchical activity tracking
- ✅ Context manager for automatic start/end logging
- ✅ Error and warning logging with recovery tracking
- ✅ File rotation at 50MB
- ✅ Statistics tracking
- ✅ Active activities monitoring
- ✅ Singleton pattern for global access

### Usage Monitor Features

- ✅ Background daemon polling every 5 minutes
- ✅ Non-blocking execution
- ✅ Snapshot history tracking
- ✅ Hourly and daily aggregation
- ✅ Cost and token tracking
- ✅ Alert system for thresholds
- ✅ PID-based lifecycle management
- ✅ Graceful shutdown

### Usage Attribution Features

- ✅ Correlation with pipeline events
- ✅ Breakdowns by: model, stage, command, agent, skill
- ✅ Top consumers analysis
- ✅ Cost trend analysis
- ✅ Report generation

### Query API Features

- ✅ Programmatic and CLI access
- ✅ Real-time status queries
- ✅ Event hierarchy navigation
- ✅ Time-based filtering
- ✅ Statistics aggregation
- ✅ Report generation

## Testing

Run the comprehensive test suite:

```bash
python3 _state/test_logging.py
```

Expected output:
```
✅ ALL TESTS PASSED

📊 Final Statistics:
   Total events: 13
   Commands: 2
   Agents: 1
   Skills: 2
   Errors: 1
   Warnings: 1
```

## Configuration

### Usage Pricing Configuration

Edit `_state/usage_pricing.json` to update:

- Model pricing (per 1K tokens)
- Alert thresholds
- Budget limits
- Optimization recommendations

### Polling Interval

The usage monitor polls every 5 minutes by default. To change:

```python
# In usage_monitor_daemon.py
POLL_INTERVAL = 300  # Change to desired interval in seconds
```

### Alert Thresholds

Edit `_state/usage_pricing.json`:

```json
{
  "alert_thresholds": {
    "hourly_cost_warning": 10.0,
    "hourly_cost_critical": 25.0,
    "daily_cost_warning": 50.0,
    "daily_cost_critical": 100.0,
    "hourly_tokens_warning": 50000,
    "hourly_tokens_critical": 100000
  }
}
```

## Troubleshooting

### Pipeline Logger Issues

**Problem**: Events not logging
- **Solution**: Check that `_state/pipeline_progress.json` is writable
- **Solution**: Verify logger initialization: `python3 _state/pipeline_logger.py test`

**Problem**: File rotation not working
- **Solution**: Check file size: `ls -lh _state/pipeline_progress.json`
- **Solution**: Verify disk space availability

### Usage Monitor Issues

**Problem**: Daemon not starting
- **Solution**: Check for stale PID file: `rm _state/usage_monitor.pid`
- **Solution**: Verify Python 3 is available: `python3 --version`

**Problem**: /usage command not found
- **Solution**: Ensure running in Claude Code environment
- **Solution**: Verify Claude CLI is installed

**Problem**: Daemon crashes
- **Solution**: Check daemon logs (stdout/stderr)
- **Solution**: Verify file permissions on `_state/` directory

### Query API Issues

**Problem**: API returns empty data
- **Solution**: Verify JSON files exist and are valid
- **Solution**: Run test suite: `python3 _state/test_logging.py`

## Future Enhancements

Potential improvements for future iterations:

1. **Web Dashboard**: Real-time visualization of pipeline status and usage
2. **Export Formats**: CSV, Excel, PDF report exports
3. **Cost Forecasting**: Predict future costs based on trends
4. **Integration Tests**: Automated testing with actual commands
5. **Performance Metrics**: Track execution times and bottlenecks
6. **Anomaly Detection**: Automatic detection of unusual usage patterns
7. **Slack/Email Alerts**: Real-time notifications for critical alerts
8. **Historical Analysis**: Long-term trend analysis and reporting

## Support

For issues or questions about the monitoring system:

1. Run the test suite to verify installation: `python3 _state/test_logging.py`
2. Check daemon status: `python3 _state/usage_monitor_daemon.py status`
3. Review logs in `_state/pipeline_progress.json` and `_state/usage_stats.json`
4. Check file permissions on `_state/` directory

## Implementation Details

- **Total Files Created**: 14
- **Total Lines of Code**: ~3,500+
- **Test Coverage**: Comprehensive test suite with 12 test cases
- **Integration Points**: Commands, agents, skills via hooks
- **Thread Safety**: All file operations use threading locks
- **Error Handling**: Graceful degradation with warnings
- **Performance**: Non-blocking daemon, efficient file I/O

## Summary

This implementation provides complete monitoring and usage tracking infrastructure for the i2m_accelerators_agentic framework with:

- ✅ Real-time pipeline status tracking
- ✅ Hierarchical activity logging
- ✅ Automated usage monitoring
- ✅ Detailed cost attribution
- ✅ Query APIs for programmatic access
- ✅ CLI tools for quick insights
- ✅ Comprehensive testing
- ✅ Production-ready error handling
