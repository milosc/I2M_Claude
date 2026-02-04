#!/usr/bin/env python3
"""
Data collectors for Phase Execution Time Analytics.

Parses timing data from:
- _state/pipeline_progress.json
- _state/{stage}_progress.json
- _state/lifecycle.json
- traceability/{system}_version_history.json
"""

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any


@dataclass
class EventTiming:
    """Represents a single event with timing information."""
    event_id: str
    event_type: str
    timestamp: datetime
    duration_seconds: Optional[float]
    level: str  # command, agent, skill, checkpoint
    name: str
    parent_event_id: Optional[str]
    stage: Optional[str] = None
    system_name: Optional[str] = None


class PipelineParser:
    """Parses _state/pipeline_progress.json for timing data."""

    def __init__(self, state_dir: Path):
        self.state_dir = Path(state_dir)
        self.pipeline_file = self.state_dir / "pipeline_progress.json"

    def parse(self) -> List[EventTiming]:
        """Extract all events with timing information."""
        if not self.pipeline_file.exists():
            return []

        try:
            with open(self.pipeline_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

        events = []
        start_events: Dict[str, datetime] = {}  # Map event_id to start timestamp

        for event in data.get("events", []):
            event_type = event.get("event_type", "")
            event_id = event.get("event_id", "")
            timestamp_str = event.get("timestamp", "")

            if not timestamp_str:
                continue

            # Parse timestamp
            try:
                timestamp = self._parse_timestamp(timestamp_str)
            except ValueError:
                continue

            # Track start events for duration calculation
            if event_type.endswith("_start") or event_type == "command_start":
                start_events[event_id] = timestamp

            # Calculate duration for end events
            duration = None
            if event_type.endswith("_end") or event_type == "command_end":
                related_start = event.get("related_start_event_id")
                if related_start and related_start in start_events:
                    duration = (timestamp - start_events[related_start]).total_seconds()

            activity = event.get("activity", {})
            context = event.get("context", {})

            events.append(EventTiming(
                event_id=event_id,
                event_type=event_type,
                timestamp=timestamp,
                duration_seconds=duration,
                level=event.get("level", "unknown"),
                name=activity.get("name", "unknown"),
                parent_event_id=event.get("parent_event_id"),
                stage=context.get("stage"),
                system_name=context.get("system_name")
            ))

        return events

    def get_statistics(self) -> Dict[str, Any]:
        """Get pipeline statistics."""
        if not self.pipeline_file.exists():
            return {}

        try:
            with open(self.pipeline_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("statistics", {})
        except (json.JSONDecodeError, IOError):
            return {}

    def get_current_context(self) -> Dict[str, Any]:
        """Get current pipeline context."""
        if not self.pipeline_file.exists():
            return {}

        try:
            with open(self.pipeline_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("current_context", {})
        except (json.JSONDecodeError, IOError):
            return {}

    def _parse_timestamp(self, ts: str) -> datetime:
        """Parse ISO 8601 timestamp to datetime."""
        # Handle various formats
        ts = ts.replace("Z", "+00:00")
        if "+" not in ts and "-" not in ts[10:]:
            ts += "+00:00"
        return datetime.fromisoformat(ts)


class StageProgressParser:
    """Parses stage-specific progress files."""

    STAGE_FILES = {
        "discovery": "discovery_progress.json",
        "prototype": "prototype_progress.json",
        "productspecs": "productspecs_progress.json",
        "solarch": "solarch_progress.json",
        "implementation": "implementation_progress.json"
    }

    def __init__(self, state_dir: Path):
        self.state_dir = Path(state_dir)

    def parse_stage(self, stage: str) -> Optional[Dict[str, Any]]:
        """Parse a specific stage progress file."""
        filename = self.STAGE_FILES.get(stage)
        if not filename:
            return None

        filepath = self.state_dir / filename
        if not filepath.exists():
            return None

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

        # Extract checkpoint timings - handle both "checkpoints" and "phases" keys
        checkpoints = []
        checkpoint_data = data.get("checkpoints", data.get("phases", {}))

        if isinstance(checkpoint_data, dict):
            for cp_id, cp_data in checkpoint_data.items():
                if not isinstance(cp_data, dict):
                    continue

                checkpoint = {
                    "checkpoint_id": cp_id,
                    "name": cp_data.get("name", cp_id),
                    "status": cp_data.get("status"),
                    "started_at": cp_data.get("started_at"),
                    "completed_at": cp_data.get("completed_at")
                }

                # Calculate duration if both timestamps exist
                if checkpoint["started_at"] and checkpoint["completed_at"]:
                    try:
                        start = self._parse_timestamp(checkpoint["started_at"])
                        end = self._parse_timestamp(checkpoint["completed_at"])
                        checkpoint["duration_seconds"] = (end - start).total_seconds()
                    except (ValueError, TypeError):
                        checkpoint["duration_seconds"] = None

                checkpoints.append(checkpoint)

        return {
            "system_name": data.get("system_name"),
            "stage": stage,
            "started_at": data.get("started_at", data.get("pipeline_started_at")),
            "updated_at": data.get("updated_at", data.get("last_updated")),
            "current_checkpoint": data.get("current_checkpoint"),
            "checkpoints": sorted(checkpoints, key=lambda x: str(x.get("checkpoint_id", ""))),
            "metrics": data.get("metrics", {}),
            "tasks": data.get("tasks", {}),
            "agents_spawned": data.get("agents_spawned", [])
        }

    def parse_all_stages(self) -> Dict[str, Dict[str, Any]]:
        """Parse all available stage progress files."""
        results = {}
        for stage in self.STAGE_FILES:
            parsed = self.parse_stage(stage)
            if parsed and parsed.get("system_name"):
                results[stage] = parsed
        return results

    def find_stage_for_system(self, system_name: str) -> Optional[Dict[str, Any]]:
        """Find the most recent stage data for a system."""
        all_stages = self.parse_all_stages()

        for stage_name in ["implementation", "solarch", "productspecs", "prototype", "discovery"]:
            stage_data = all_stages.get(stage_name)
            if stage_data and stage_data.get("system_name") == system_name:
                return stage_data

        return None

    def _parse_timestamp(self, ts: str) -> datetime:
        """Parse ISO 8601 timestamp to datetime."""
        ts = ts.replace("Z", "+00:00")
        if "+" not in ts and "-" not in ts[10:]:
            ts += "+00:00"
        return datetime.fromisoformat(ts)


class LifecycleParser:
    """Parses lifecycle.json for detailed tool timing."""

    def __init__(self, state_dir: Path):
        self.state_dir = Path(state_dir)
        self.lifecycle_file = self.state_dir / "lifecycle.json"

    def parse_tool_timings(self, limit: int = 50000) -> Dict[str, List[float]]:
        """Extract tool execution times from lifecycle events.

        Returns: Dict mapping tool_name to list of durations in seconds.
        """
        if not self.lifecycle_file.exists():
            return {}

        tool_timings: Dict[str, List[float]] = {}
        pending_starts: Dict[str, Dict] = {}  # tool_use_id -> {tool_name, start_time}

        try:
            with open(self.lifecycle_file, 'r', encoding='utf-8') as f:
                count = 0
                for line in f:
                    if count >= limit:
                        break
                    count += 1

                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    event_type = event.get("event_type")
                    payload = event.get("payload", {})
                    tool_use_id = payload.get("tool_use_id")
                    tool_name = payload.get("tool_name")
                    timestamp_str = event.get("timestamp")

                    if not all([event_type, tool_use_id, timestamp_str]):
                        continue

                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    except ValueError:
                        continue

                    if event_type == "PreToolUse" and tool_name:
                        pending_starts[tool_use_id] = {
                            "tool_name": tool_name,
                            "start_time": timestamp
                        }
                    elif event_type == "PostToolUse" and tool_use_id in pending_starts:
                        start_info = pending_starts.pop(tool_use_id)
                        duration = (timestamp - start_info["start_time"]).total_seconds()

                        tool_name = start_info["tool_name"]
                        if tool_name not in tool_timings:
                            tool_timings[tool_name] = []
                        tool_timings[tool_name].append(duration)

        except IOError:
            return {}

        return tool_timings

    def get_agent_timings(self, limit: int = 50000) -> Dict[str, List[float]]:
        """Extract agent execution times from lifecycle events."""
        if not self.lifecycle_file.exists():
            return {}

        agent_timings: Dict[str, List[float]] = {}
        pending_agents: Dict[str, Dict] = {}

        try:
            with open(self.lifecycle_file, 'r', encoding='utf-8') as f:
                count = 0
                for line in f:
                    if count >= limit:
                        break
                    count += 1

                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    event_type = event.get("event_type")
                    timestamp_str = event.get("timestamp")
                    payload = event.get("payload", {})

                    if not timestamp_str:
                        continue

                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
                    except ValueError:
                        continue

                    # Track Task tool calls (agent spawns)
                    if event_type == "PreToolUse":
                        tool_name = payload.get("tool_name")
                        if tool_name == "Task":
                            tool_input = payload.get("tool_input", {})
                            agent_type = tool_input.get("subagent_type", "unknown")
                            tool_use_id = payload.get("tool_use_id")
                            if tool_use_id:
                                pending_agents[tool_use_id] = {
                                    "agent_type": agent_type,
                                    "start_time": timestamp
                                }

                    elif event_type == "PostToolUse":
                        tool_use_id = payload.get("tool_use_id")
                        if tool_use_id in pending_agents:
                            start_info = pending_agents.pop(tool_use_id)
                            duration = (timestamp - start_info["start_time"]).total_seconds()
                            agent_type = start_info["agent_type"]

                            if agent_type not in agent_timings:
                                agent_timings[agent_type] = []
                            agent_timings[agent_type].append(duration)

        except IOError:
            return {}

        return agent_timings


class VersionHistoryParser:
    """Parses traceability version history for file change timing."""

    def __init__(self, traceability_dir: Path):
        self.traceability_dir = Path(traceability_dir)

    def parse(self, system_name: str) -> List[Dict[str, Any]]:
        """Parse version history for a system."""
        history_file = self.traceability_dir / f"{system_name}_version_history.json"

        if not history_file.exists():
            return []

        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("history", [])
        except (json.JSONDecodeError, IOError):
            return []

    def get_changes_by_stage(self, system_name: str) -> Dict[str, List[Dict]]:
        """Group version history changes by stage."""
        history = self.parse(system_name)

        by_stage: Dict[str, List[Dict]] = {}
        for entry in history:
            stage = entry.get("stage", "unknown")
            if stage not in by_stage:
                by_stage[stage] = []
            by_stage[stage].append(entry)

        return by_stage
