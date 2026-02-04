#!/usr/bin/env python3
"""
Analytics engine for Phase Execution Time Analytics.

Provides:
- TimeAggregator: Aggregates timing data across dimensions
- TrendCalculator: Calculates performance trends over time
- Comparator: Compares runs within the same system
- Benchmarker: Manages benchmark data
"""

from dataclasses import dataclass, field
from datetime import datetime
from statistics import mean, stdev
from typing import Dict, List, Optional, Tuple, Any

# Handle both direct execution and module import
try:
    from .collectors import EventTiming
except ImportError:
    from collectors import EventTiming


@dataclass
class AggregatedTiming:
    """Aggregated timing statistics for a category."""
    name: str
    invocations: int
    total_seconds: float
    avg_seconds: float
    min_seconds: float
    max_seconds: float
    stddev_seconds: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "invocations": self.invocations,
            "total_seconds": round(self.total_seconds, 3),
            "avg_seconds": round(self.avg_seconds, 3),
            "min_seconds": round(self.min_seconds, 3),
            "max_seconds": round(self.max_seconds, 3),
            "stddev_seconds": round(self.stddev_seconds, 3)
        }


class TimeAggregator:
    """Aggregates timing data across multiple dimensions."""

    def aggregate_by_level(self, events: List[EventTiming]) -> Dict[str, AggregatedTiming]:
        """Aggregate timings by event level (command, agent, skill)."""
        by_level: Dict[str, List[float]] = {}

        for event in events:
            if event.duration_seconds is None:
                continue

            level = event.level
            if level not in by_level:
                by_level[level] = []
            by_level[level].append(event.duration_seconds)

        results = {}
        for level, durations in by_level.items():
            results[level] = self._calculate_stats(level, durations)

        return results

    def aggregate_by_name(self, events: List[EventTiming], level: str) -> Dict[str, AggregatedTiming]:
        """Aggregate timings by name within a level (e.g., by agent name)."""
        filtered = [e for e in events if e.level == level and e.duration_seconds is not None]

        by_name: Dict[str, List[float]] = {}
        for event in filtered:
            name = event.name
            if name not in by_name:
                by_name[name] = []
            by_name[name].append(event.duration_seconds)

        results = {}
        for name, durations in by_name.items():
            results[name] = self._calculate_stats(name, durations)

        return results

    def aggregate_by_stage(self, events: List[EventTiming]) -> Dict[str, AggregatedTiming]:
        """Aggregate timings by stage."""
        by_stage: Dict[str, List[float]] = {}

        for event in events:
            if event.duration_seconds is None or not event.stage:
                continue

            stage = event.stage
            if stage not in by_stage:
                by_stage[stage] = []
            by_stage[stage].append(event.duration_seconds)

        results = {}
        for stage, durations in by_stage.items():
            results[stage] = self._calculate_stats(stage, durations)

        return results

    def aggregate_tool_timings(self, tool_timings: Dict[str, List[float]]) -> Dict[str, AggregatedTiming]:
        """Aggregate pre-computed tool timings."""
        results = {}
        for tool_name, durations in tool_timings.items():
            if durations:
                results[tool_name] = self._calculate_stats(tool_name, durations)
        return results

    def _calculate_stats(self, name: str, durations: List[float]) -> AggregatedTiming:
        """Calculate statistics for a list of durations."""
        if not durations:
            return AggregatedTiming(
                name=name,
                invocations=0,
                total_seconds=0,
                avg_seconds=0,
                min_seconds=0,
                max_seconds=0,
                stddev_seconds=0
            )

        return AggregatedTiming(
            name=name,
            invocations=len(durations),
            total_seconds=sum(durations),
            avg_seconds=mean(durations),
            min_seconds=min(durations),
            max_seconds=max(durations),
            stddev_seconds=stdev(durations) if len(durations) > 1 else 0
        )


class TrendCalculator:
    """Calculates performance trends over time."""

    def calculate_trend(self, history: List[Dict[str, Any]]) -> Tuple[str, float]:
        """
        Calculate trend direction and slope.

        Returns: (trend_direction, slope)
            trend_direction: "improving" | "degrading" | "stable" | "insufficient_data"
            slope: negative = improving (faster), positive = degrading (slower)
        """
        if len(history) < 2:
            return ("insufficient_data", 0.0)

        # Sort by timestamp
        sorted_history = sorted(history, key=lambda x: x.get("captured_at", ""))

        # Extract durations
        durations = [h.get("duration_seconds", 0) for h in sorted_history if h.get("duration_seconds")]

        if len(durations) < 2:
            return ("insufficient_data", 0.0)

        # Simple linear regression for trend
        n = len(durations)
        x = list(range(n))
        x_mean = mean(x)
        y_mean = mean(durations)

        # Calculate slope
        numerator = sum((x[i] - x_mean) * (durations[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return ("stable", 0.0)

        slope = numerator / denominator

        # Determine trend based on slope relative to average
        slope_threshold = y_mean * 0.05  # 5% of average as threshold

        if slope < -slope_threshold:
            return ("improving", slope)
        elif slope > slope_threshold:
            return ("degrading", slope)
        else:
            return ("stable", slope)

    def generate_trend_data(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate data points for trend visualization."""
        sorted_history = sorted(history, key=lambda x: x.get("captured_at", ""))

        return [
            {
                "date": h.get("captured_at", "")[:10],  # YYYY-MM-DD
                "duration_seconds": h.get("duration_seconds", 0),
                "duration_minutes": round(h.get("duration_seconds", 0) / 60, 2),
                "run_id": h.get("run_id", ""),
                "stage": h.get("stage", "")
            }
            for h in sorted_history
        ]

    def calculate_moving_average(self, history: List[Dict[str, Any]], window: int = 3) -> List[float]:
        """Calculate moving average of durations."""
        sorted_history = sorted(history, key=lambda x: x.get("captured_at", ""))
        durations = [h.get("duration_seconds", 0) for h in sorted_history]

        if len(durations) < window:
            return durations

        moving_avg = []
        for i in range(len(durations)):
            start = max(0, i - window + 1)
            window_values = durations[start:i + 1]
            moving_avg.append(mean(window_values))

        return moving_avg


class Comparator:
    """Compares runs within the same system."""

    def compare_to_benchmark(self, benchmark: Dict[str, Any], current_run: Dict[str, Any]) -> Dict[str, Any]:
        """Compare current run against benchmark averages."""
        stage = current_run.get("stage")
        stage_benchmark = benchmark.get("stages", {}).get(stage, {})

        current_duration = current_run.get("timing", {}).get("total_duration_seconds", 0)
        avg_duration = stage_benchmark.get("avg_duration_seconds", 0)

        if avg_duration == 0:
            delta_percent = 0
            comparison = "first_run"
        else:
            delta_percent = ((current_duration - avg_duration) / avg_duration) * 100
            if delta_percent < -10:
                comparison = "faster"
            elif delta_percent > 10:
                comparison = "slower"
            else:
                comparison = "similar"

        return {
            "stage": stage,
            "current_duration_seconds": current_duration,
            "benchmark_avg_seconds": avg_duration,
            "benchmark_min_seconds": stage_benchmark.get("min_duration_seconds", 0),
            "benchmark_max_seconds": stage_benchmark.get("max_duration_seconds", 0),
            "delta_seconds": current_duration - avg_duration,
            "delta_percent": round(delta_percent, 2),
            "comparison": comparison,
            "runs_in_benchmark": stage_benchmark.get("runs_count", 0)
        }

    def compare_agents(self, benchmark: Dict[str, Any], current_agents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compare agent performance against benchmarks."""
        agent_benchmarks = benchmark.get("agents", {})
        comparisons = []

        for agent in current_agents:
            agent_name = agent.get("agent_name")
            agent_bench = agent_benchmarks.get(agent_name, {})

            current_avg = agent.get("avg_duration_seconds", 0)
            benchmark_avg = agent_bench.get("avg_duration_seconds", 0)

            if benchmark_avg == 0:
                delta_percent = 0
                comparison = "new_agent"
            else:
                delta_percent = ((current_avg - benchmark_avg) / benchmark_avg) * 100
                if delta_percent < -10:
                    comparison = "faster"
                elif delta_percent > 10:
                    comparison = "slower"
                else:
                    comparison = "similar"

            comparisons.append({
                "agent_name": agent_name,
                "current_avg_seconds": current_avg,
                "benchmark_avg_seconds": benchmark_avg,
                "current_invocations": agent.get("invocations", 0),
                "benchmark_invocations": agent_bench.get("total_invocations", 0),
                "delta_percent": round(delta_percent, 2),
                "comparison": comparison
            })

        return comparisons

    def compare_commands(self, benchmark: Dict[str, Any], current_commands: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compare command performance against benchmarks."""
        command_benchmarks = benchmark.get("commands", {})
        comparisons = []

        for cmd in current_commands:
            cmd_name = cmd.get("command_name")
            cmd_bench = command_benchmarks.get(cmd_name, {})

            current_duration = cmd.get("total_duration_seconds", 0)
            benchmark_avg = cmd_bench.get("avg_duration_seconds", 0)

            if benchmark_avg == 0:
                delta_percent = 0
                comparison = "new_command"
            else:
                delta_percent = ((current_duration - benchmark_avg) / benchmark_avg) * 100
                if delta_percent < -10:
                    comparison = "faster"
                elif delta_percent > 10:
                    comparison = "slower"
                else:
                    comparison = "similar"

            comparisons.append({
                "command_name": cmd_name,
                "current_duration_seconds": current_duration,
                "benchmark_avg_seconds": benchmark_avg,
                "delta_percent": round(delta_percent, 2),
                "comparison": comparison
            })

        return comparisons

    def find_bottlenecks(self, agents: List[Dict[str, Any]], commands: List[Dict[str, Any]],
                         threshold_percent: float = 20) -> Dict[str, List[Dict[str, Any]]]:
        """Identify performance bottlenecks (items taking longest time)."""
        bottlenecks = {
            "agents": [],
            "commands": []
        }

        # Sort agents by total duration
        sorted_agents = sorted(agents, key=lambda x: x.get("total_duration_seconds", 0), reverse=True)

        # Get total time
        total_agent_time = sum(a.get("total_duration_seconds", 0) for a in agents)

        # Find agents taking more than threshold_percent of total time
        for agent in sorted_agents:
            agent_time = agent.get("total_duration_seconds", 0)
            if total_agent_time > 0:
                percent = (agent_time / total_agent_time) * 100
                if percent >= threshold_percent:
                    bottlenecks["agents"].append({
                        **agent,
                        "percent_of_total": round(percent, 2)
                    })

        # Same for commands
        sorted_commands = sorted(commands, key=lambda x: x.get("total_duration_seconds", 0), reverse=True)
        total_cmd_time = sum(c.get("total_duration_seconds", 0) for c in commands)

        for cmd in sorted_commands:
            cmd_time = cmd.get("total_duration_seconds", 0)
            if total_cmd_time > 0:
                percent = (cmd_time / total_cmd_time) * 100
                if percent >= threshold_percent:
                    bottlenecks["commands"].append({
                        **cmd,
                        "percent_of_total": round(percent, 2)
                    })

        return bottlenecks
