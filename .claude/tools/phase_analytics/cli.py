#!/usr/bin/env python3
"""
Phase Execution Time Analytics CLI

Command-line interface for capturing, analyzing, and reporting
execution times across HTEC Agentic Accelerator Framework stages.

Usage:
    python3 cli.py capture <system_name>    # Capture current run data
    python3 cli.py report <system_name>     # Generate Markdown report
    python3 cli.py dashboard <system_name>  # Generate HTML dashboard
    python3 cli.py compare <system_name>    # Compare current run to benchmark
    python3 cli.py status                   # Show all systems with data
    python3 cli.py full <system_name>       # Full analysis (capture + report + dashboard)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean, stdev
from typing import Dict, List, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from collectors import PipelineParser, StageProgressParser, LifecycleParser, VersionHistoryParser
from engine import TimeAggregator, TrendCalculator, Comparator
from reports import MarkdownReport, SummaryReport
from dashboard import HTMLDashboard


class AnalyticsCLI:
    """Main CLI class for Phase Execution Time Analytics."""

    def __init__(self, project_root: Path = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.state_dir = self.project_root / "_state"
        self.traceability_dir = self.project_root / "traceability"
        self.analytics_dir = self.project_root / "analytics"

        # Ensure directories exist
        (self.analytics_dir / "runs").mkdir(parents=True, exist_ok=True)
        (self.analytics_dir / "benchmarks").mkdir(parents=True, exist_ok=True)
        (self.analytics_dir / "reports").mkdir(parents=True, exist_ok=True)

    def capture(self, system_name: str) -> Optional[Dict[str, Any]]:
        """Capture current run data and update benchmarks."""
        print(f"\u23F3 Capturing execution data for {system_name}...")

        # Parse data sources
        pipeline_parser = PipelineParser(self.state_dir)
        stage_parser = StageProgressParser(self.state_dir)
        lifecycle_parser = LifecycleParser(self.state_dir)

        events = pipeline_parser.parse()
        statistics = pipeline_parser.get_statistics()
        current_context = pipeline_parser.get_current_context()

        # Find stage data for this system
        stage_data = stage_parser.find_stage_for_system(system_name)

        if not stage_data:
            # Try to find any stage data
            all_stages = stage_parser.parse_all_stages()
            if all_stages:
                print(f"\u26A0\uFE0F  No exact match for '{system_name}'. Available systems:")
                for stage, data in all_stages.items():
                    print(f"   - {data.get('system_name', 'Unknown')} ({stage})")
                return None
            else:
                print(f"\u274C No stage progress data found. Run a stage command first.")
                return None

        current_stage = stage_data.get("stage", "unknown")
        print(f"   Found stage: {current_stage}")

        # Calculate timing
        started_at = stage_data.get("started_at")
        completed_at = stage_data.get("updated_at")
        total_duration = 0

        if started_at and completed_at:
            try:
                start = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
                end = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
                total_duration = (end - start).total_seconds()
            except ValueError:
                pass

        # Aggregate timing data from events
        aggregator = TimeAggregator()

        # Filter events for this system
        system_events = [e for e in events if e.system_name == system_name or not e.system_name]

        agents_agg = aggregator.aggregate_by_name(system_events, "agent")
        commands_agg = aggregator.aggregate_by_name(system_events, "command")
        skills_agg = aggregator.aggregate_by_name(system_events, "skill")

        # Get tool timings from lifecycle
        tool_timings = lifecycle_parser.parse_tool_timings(limit=10000)
        tools_agg = aggregator.aggregate_tool_timings(tool_timings)

        # Get agent timings from lifecycle
        agent_timings = lifecycle_parser.get_agent_timings(limit=10000)
        lifecycle_agents_agg = aggregator.aggregate_tool_timings(agent_timings)

        # Build run snapshot
        run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        snapshot = {
            "schema_version": "1.0.0",
            "run_id": run_id,
            "system_name": system_name,
            "stage": current_stage,
            "captured_at": datetime.now().isoformat(),
            "timing": {
                "started_at": started_at,
                "completed_at": completed_at,
                "total_duration_seconds": round(total_duration, 2),
                "total_duration_human": self._format_duration(total_duration)
            },
            "checkpoints": stage_data.get("checkpoints", []),
            "agents": [
                {
                    "agent_name": name,
                    "invocations": agg.invocations,
                    "total_duration_seconds": round(agg.total_seconds, 2),
                    "avg_duration_seconds": round(agg.avg_seconds, 2)
                }
                for name, agg in {**agents_agg, **lifecycle_agents_agg}.items()
            ],
            "commands": [
                {
                    "command_name": name,
                    "invocations": agg.invocations,
                    "total_duration_seconds": round(agg.total_seconds, 2),
                    "avg_duration_seconds": round(agg.avg_seconds, 2)
                }
                for name, agg in commands_agg.items()
            ],
            "skills": [
                {
                    "skill_name": name,
                    "invocations": agg.invocations,
                    "total_duration_seconds": round(agg.total_seconds, 2),
                    "avg_duration_seconds": round(agg.avg_seconds, 2)
                }
                for name, agg in skills_agg.items()
            ],
            "tools": [
                {
                    "tool_name": name,
                    "invocations": agg.invocations,
                    "total_duration_seconds": round(agg.total_seconds, 2),
                    "avg_duration_seconds": round(agg.avg_seconds, 2)
                }
                for name, agg in tools_agg.items()
            ],
            "metrics": {
                **statistics,
                **stage_data.get("metrics", {}),
                "tasks": stage_data.get("tasks", {})
            }
        }

        # Save run snapshot
        run_file = self.analytics_dir / "runs" / f"{system_name}_{run_id}.json"
        with open(run_file, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)

        print(f"\u2705 Run captured: {run_file.name}")

        # Update benchmarks
        self._update_benchmarks(system_name, snapshot)

        return snapshot

    def _update_benchmarks(self, system_name: str, snapshot: Dict[str, Any]):
        """Update benchmark file with new run data."""
        benchmark_file = self.analytics_dir / "benchmarks" / f"{system_name}_benchmarks.json"

        # Load existing or create new
        if benchmark_file.exists():
            with open(benchmark_file, "r", encoding="utf-8") as f:
                benchmark = json.load(f)
        else:
            benchmark = {
                "schema_version": "1.0.0",
                "system_name": system_name,
                "created_at": datetime.now().isoformat(),
                "stages": {},
                "agents": {},
                "commands": {},
                "skills": {},
                "history": []
            }

        benchmark["last_updated"] = datetime.now().isoformat()

        # Update stage data
        stage = snapshot["stage"]
        duration = snapshot["timing"]["total_duration_seconds"]

        if stage not in benchmark["stages"]:
            benchmark["stages"][stage] = {
                "runs_count": 0,
                "durations": []
            }

        stage_data = benchmark["stages"][stage]
        stage_data["runs_count"] += 1
        stage_data["durations"].append(duration)

        # Calculate statistics
        durations = stage_data["durations"]
        stage_data["avg_duration_seconds"] = round(mean(durations), 2)
        stage_data["min_duration_seconds"] = round(min(durations), 2)
        stage_data["max_duration_seconds"] = round(max(durations), 2)
        stage_data["stddev_seconds"] = round(stdev(durations), 2) if len(durations) > 1 else 0
        stage_data["last_run"] = snapshot["captured_at"]

        # Calculate trend
        trend_calc = TrendCalculator()
        stage_history = [h for h in benchmark["history"] if h.get("stage") == stage]
        stage_history.append({
            "run_id": snapshot["run_id"],
            "stage": stage,
            "duration_seconds": duration,
            "captured_at": snapshot["captured_at"]
        })
        trend, _ = trend_calc.calculate_trend(stage_history)
        stage_data["trend"] = trend

        # Update agent data
        for agent in snapshot.get("agents", []):
            agent_name = agent["agent_name"]
            if agent_name not in benchmark["agents"]:
                benchmark["agents"][agent_name] = {
                    "total_invocations": 0,
                    "durations": []
                }

            agent_data = benchmark["agents"][agent_name]
            agent_data["total_invocations"] += agent["invocations"]
            if agent["avg_duration_seconds"] > 0:
                agent_data["durations"].append(agent["avg_duration_seconds"])
                agent_data["avg_duration_seconds"] = round(mean(agent_data["durations"]), 2)

        # Update command data
        for cmd in snapshot.get("commands", []):
            cmd_name = cmd["command_name"]
            if cmd_name not in benchmark["commands"]:
                benchmark["commands"][cmd_name] = {
                    "total_invocations": 0,
                    "durations": []
                }

            cmd_data = benchmark["commands"][cmd_name]
            cmd_data["total_invocations"] += cmd["invocations"]
            if cmd["avg_duration_seconds"] > 0:
                cmd_data["durations"].append(cmd["avg_duration_seconds"])
                cmd_data["avg_duration_seconds"] = round(mean(cmd_data["durations"]), 2)

        # Update skill data
        for skill in snapshot.get("skills", []):
            skill_name = skill["skill_name"]
            if skill_name not in benchmark.get("skills", {}):
                if "skills" not in benchmark:
                    benchmark["skills"] = {}
                benchmark["skills"][skill_name] = {
                    "total_invocations": 0,
                    "durations": []
                }

            skill_data = benchmark["skills"][skill_name]
            skill_data["total_invocations"] += skill["invocations"]
            if skill["avg_duration_seconds"] > 0:
                skill_data["durations"].append(skill["avg_duration_seconds"])
                skill_data["avg_duration_seconds"] = round(mean(skill_data["durations"]), 2)

        # Update history
        benchmark["history"].append({
            "run_id": snapshot["run_id"],
            "stage": stage,
            "duration_seconds": duration,
            "captured_at": snapshot["captured_at"]
        })

        # Keep only last 100 history entries
        benchmark["history"] = benchmark["history"][-100:]

        # Save benchmark
        with open(benchmark_file, "w", encoding="utf-8") as f:
            json.dump(benchmark, f, indent=2)

        print(f"\u2705 Benchmarks updated: {benchmark_file.name}")

    def report(self, system_name: str) -> Optional[str]:
        """Generate Markdown report."""
        print(f"\u23F3 Generating report for {system_name}...")

        benchmark_file = self.analytics_dir / "benchmarks" / f"{system_name}_benchmarks.json"
        if not benchmark_file.exists():
            print(f"\u274C No benchmarks found for {system_name}. Run 'capture' first.")
            return None

        with open(benchmark_file, "r", encoding="utf-8") as f:
            benchmark = json.load(f)

        report_gen = MarkdownReport()
        report_content = report_gen.generate(system_name, benchmark)

        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.analytics_dir / "reports" / f"{system_name}_report_{timestamp}.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report_content)

        print(f"\u2705 Report generated: {report_file.name}")
        return str(report_file)

    def dashboard(self, system_name: str) -> Optional[str]:
        """Generate HTML dashboard."""
        print(f"\u23F3 Generating dashboard for {system_name}...")

        benchmark_file = self.analytics_dir / "benchmarks" / f"{system_name}_benchmarks.json"
        if not benchmark_file.exists():
            print(f"\u274C No benchmarks found for {system_name}. Run 'capture' first.")
            return None

        with open(benchmark_file, "r", encoding="utf-8") as f:
            benchmark = json.load(f)

        dashboard_gen = HTMLDashboard()
        html_content = dashboard_gen.generate(system_name, benchmark)

        # Save dashboard
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        dashboard_file = self.analytics_dir / "reports" / f"{system_name}_dashboard_{timestamp}.html"
        with open(dashboard_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"\u2705 Dashboard generated: {dashboard_file.name}")
        return str(dashboard_file)

    def compare(self, system_name: str) -> Optional[Dict[str, Any]]:
        """Compare current state against benchmarks."""
        print(f"\u23F3 Comparing current run for {system_name}...")

        # First capture current state
        snapshot = self.capture(system_name)
        if not snapshot:
            return None

        # Load benchmark
        benchmark_file = self.analytics_dir / "benchmarks" / f"{system_name}_benchmarks.json"
        if not benchmark_file.exists():
            print(f"\u274C No benchmarks found. This is the first run.")
            return None

        with open(benchmark_file, "r", encoding="utf-8") as f:
            benchmark = json.load(f)

        # Compare
        comparator = Comparator()
        stage_comparison = comparator.compare_to_benchmark(benchmark, snapshot)
        agent_comparisons = comparator.compare_agents(benchmark, snapshot.get("agents", []))
        command_comparisons = comparator.compare_commands(benchmark, snapshot.get("commands", []))

        # Print comparison summary
        print("\n" + "=" * 60)
        print(f"COMPARISON RESULTS: {system_name}")
        print("=" * 60)

        comp = stage_comparison["comparison"]
        delta = stage_comparison["delta_percent"]

        if comp == "faster":
            print(f"\n\U0001F680 Stage '{snapshot['stage']}' was {abs(delta):.1f}% FASTER than benchmark")
        elif comp == "slower":
            print(f"\n\u26A0\uFE0F  Stage '{snapshot['stage']}' was {abs(delta):.1f}% SLOWER than benchmark")
        elif comp == "similar":
            print(f"\n\u2705 Stage '{snapshot['stage']}' is within normal range ({abs(delta):.1f}%)")
        else:
            print(f"\n\U0001F4CA First run - establishing baseline")

        print(f"\nCurrent: {self._format_duration(stage_comparison['current_duration_seconds'])}")
        print(f"Benchmark Avg: {self._format_duration(stage_comparison['benchmark_avg_seconds'])}")

        return {
            "snapshot": snapshot,
            "stage": stage_comparison,
            "agents": agent_comparisons,
            "commands": command_comparisons
        }

    def full(self, system_name: str):
        """Run full analysis: capture + report + dashboard."""
        print(f"\n{'=' * 60}")
        print(f"FULL ANALYSIS: {system_name}")
        print(f"{'=' * 60}\n")

        # Capture
        snapshot = self.capture(system_name)
        if not snapshot:
            return

        print()

        # Report
        report_path = self.report(system_name)

        print()

        # Dashboard
        dashboard_path = self.dashboard(system_name)

        print(f"\n{'=' * 60}")
        print("ANALYSIS COMPLETE")
        print(f"{'=' * 60}")
        print(f"\nStage: {snapshot['stage']}")
        print(f"Duration: {snapshot['timing']['total_duration_human']}")
        print(f"\nReport: {report_path}")
        print(f"Dashboard: {dashboard_path}")

    def status(self):
        """Show all systems with analytics data."""
        print("\n\U0001F4CA Phase Execution Time Analytics - System Status")
        print("=" * 60)

        benchmarks_dir = self.analytics_dir / "benchmarks"
        if not benchmarks_dir.exists() or not list(benchmarks_dir.glob("*_benchmarks.json")):
            print("\nNo analytics data found. Run 'capture' for a system first.")
            print("\nUsage:")
            print("  python3 cli.py capture <SystemName>")
            return

        for benchmark_file in sorted(benchmarks_dir.glob("*_benchmarks.json")):
            with open(benchmark_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            system = data.get("system_name", "Unknown")
            stages = data.get("stages", {})
            history = data.get("history", [])
            agents = data.get("agents", {})

            print(f"\n\U0001F4C1 {system}")
            print(f"   Stages: {', '.join(stages.keys()) if stages else 'None'}")
            print(f"   Total Runs: {len(history)}")
            print(f"   Unique Agents: {len(agents)}")
            print(f"   Last Updated: {data.get('last_updated', 'N/A')[:19]}")

            # Show stage summaries
            for stage_name, stage_data in stages.items():
                trend = stage_data.get("trend", "stable")
                trend_icon = "\U0001F4C8" if trend == "improving" else "\U0001F4C9" if trend == "degrading" else "\u27A1\uFE0F"
                print(f"   - {stage_name}: {self._format_duration(stage_data.get('avg_duration_seconds', 0))} avg ({stage_data.get('runs_count', 0)} runs) {trend_icon}")

    def _format_duration(self, seconds: float) -> str:
        """Format seconds as human-readable."""
        if seconds is None or seconds == 0:
            return "-"
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"


def main():
    parser = argparse.ArgumentParser(
        description="Phase Execution Time Analytics for HTEC Agentic Accelerator Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 cli.py capture ERTriage       # Capture current run data
  python3 cli.py report ERTriage        # Generate Markdown report
  python3 cli.py dashboard ERTriage     # Generate HTML dashboard
  python3 cli.py full ERTriage          # Full analysis (capture + report + dashboard)
  python3 cli.py compare ERTriage       # Compare current run to benchmark
  python3 cli.py status                 # Show all systems with data
        """
    )
    parser.add_argument(
        "command",
        choices=["capture", "report", "dashboard", "compare", "status", "full"],
        help="Command to execute"
    )
    parser.add_argument(
        "system_name",
        nargs="?",
        help="System name (e.g., ERTriage, InventorySystem)"
    )
    parser.add_argument(
        "--project-root",
        help="Project root directory (default: current directory)",
        default="."
    )

    args = parser.parse_args()

    cli = AnalyticsCLI(Path(args.project_root))

    if args.command == "status":
        cli.status()
    elif not args.system_name:
        print("\u274C System name required for this command")
        print("\nUsage: python3 cli.py <command> <system_name>")
        sys.exit(1)
    elif args.command == "capture":
        cli.capture(args.system_name)
    elif args.command == "report":
        cli.report(args.system_name)
    elif args.command == "dashboard":
        cli.dashboard(args.system_name)
    elif args.command == "compare":
        cli.compare(args.system_name)
    elif args.command == "full":
        cli.full(args.system_name)


if __name__ == "__main__":
    main()
