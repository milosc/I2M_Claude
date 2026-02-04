#!/usr/bin/env python3
"""
HTML Dashboard generator for Phase Execution Time Analytics.

Generates interactive dashboards with Chart.js visualizations.
"""

import json
from datetime import datetime
from typing import Dict, List, Any


class HTMLDashboard:
    """Generates interactive HTML dashboard with Chart.js."""

    def generate(self, system_name: str, benchmark: Dict[str, Any]) -> str:
        """Generate complete HTML dashboard."""

        stages = benchmark.get("stages", {})
        history = benchmark.get("history", [])
        agents = benchmark.get("agents", {})
        commands = benchmark.get("commands", {})

        # Prepare chart data
        stage_labels = []
        stage_values = []
        stage_colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']

        stage_order = ["discovery", "prototype", "productspecs", "solarch", "implementation"]
        for stage in stage_order:
            if stage in stages and stages[stage].get("avg_duration_seconds", 0) > 0:
                stage_labels.append(stage.capitalize())
                stage_values.append(round(stages[stage].get("avg_duration_seconds", 0) / 60, 2))

        # Trend data
        trend_data = self._prepare_trend_data(history)

        # Agent data (top 10)
        sorted_agents = sorted(
            agents.items(),
            key=lambda x: x[1].get("total_invocations", 0),
            reverse=True
        )[:10]
        agent_labels = [a[0][:30] for a in sorted_agents]  # Truncate long names
        agent_values = [a[1].get("avg_duration_seconds", 0) for a in sorted_agents]

        # Command data (top 10)
        sorted_commands = sorted(
            commands.items(),
            key=lambda x: x[1].get("total_invocations", 0),
            reverse=True
        )[:10]
        command_labels = [c[0] for c in sorted_commands]
        command_values = [c[1].get("avg_duration_seconds", 0) / 60 for c in sorted_commands]  # in minutes

        # Calculate summary stats
        total_runs = sum(s.get("runs_count", 0) for s in stages.values())
        total_avg_time = sum(s.get("avg_duration_seconds", 0) for s in stages.values())

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{system_name} - Execution Time Analytics</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --primary: #3498db;
            --secondary: #2ecc71;
            --warning: #f39c12;
            --danger: #e74c3c;
            --purple: #9b59b6;
            --bg: #1a1a2e;
            --card: #16213e;
            --card-hover: #1f2b47;
            --text: #eee;
            --text-muted: #aaa;
            --border: rgba(255,255,255,0.1);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: var(--bg);
            color: var(--text);
            padding: 20px;
            min-height: 100vh;
        }}

        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
        }}

        .header h1 {{
            font-size: 1.8rem;
            font-weight: 600;
        }}

        .header .meta {{
            color: var(--text-muted);
            font-size: 0.9rem;
        }}

        .stat-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}

        .stat {{
            background: var(--card);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: transform 0.2s, background 0.2s;
        }}

        .stat:hover {{
            transform: translateY(-2px);
            background: var(--card-hover);
        }}

        .stat .value {{
            font-size: 2rem;
            font-weight: bold;
            color: var(--primary);
            margin-bottom: 5px;
        }}

        .stat .label {{
            font-size: 0.85rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .stat.improving .value {{ color: var(--secondary); }}
        .stat.warning .value {{ color: var(--warning); }}
        .stat.danger .value {{ color: var(--danger); }}

        .dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
            gap: 20px;
            max-width: 1800px;
            margin: 0 auto;
        }}

        .card {{
            background: var(--card);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}

        .card h2 {{
            margin-bottom: 20px;
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .card h2 .icon {{
            font-size: 1.2rem;
        }}

        .card.wide {{
            grid-column: span 2;
        }}

        @media (max-width: 1000px) {{
            .card.wide {{
                grid-column: span 1;
            }}
        }}

        canvas {{
            max-height: 300px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}

        th, td {{
            padding: 12px 10px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}

        th {{
            color: var(--primary);
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        td {{
            font-size: 0.95rem;
        }}

        tr:hover {{
            background: rgba(255,255,255,0.03);
        }}

        .trend-up {{ color: var(--secondary); }}
        .trend-down {{ color: var(--danger); }}
        .trend-stable {{ color: var(--warning); }}

        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }}

        .badge.improving {{ background: rgba(46, 204, 113, 0.2); color: var(--secondary); }}
        .badge.degrading {{ background: rgba(231, 76, 60, 0.2); color: var(--danger); }}
        .badge.stable {{ background: rgba(243, 156, 18, 0.2); color: var(--warning); }}

        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>\U0001F4CA {system_name} - Execution Time Analytics</h1>
        <div class="meta">
            Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            Last data: {benchmark.get('last_updated', 'N/A')[:19]}
        </div>
    </div>

    <div class="stat-grid">
        <div class="stat">
            <div class="value">{total_runs}</div>
            <div class="label">Total Runs</div>
        </div>
        <div class="stat">
            <div class="value">{len(stages)}</div>
            <div class="label">Stages</div>
        </div>
        <div class="stat">
            <div class="value">{len(agents)}</div>
            <div class="label">Unique Agents</div>
        </div>
        <div class="stat">
            <div class="value">{len(commands)}</div>
            <div class="label">Commands</div>
        </div>
        <div class="stat">
            <div class="value">{self._format_duration(total_avg_time)}</div>
            <div class="label">Total Avg Time</div>
        </div>
    </div>

    <div class="dashboard">
        <div class="card">
            <h2><span class="icon">\u23F1\uFE0F</span> Stage Execution Times (Avg)</h2>
            <canvas id="stageChart"></canvas>
        </div>

        <div class="card">
            <h2><span class="icon">\U0001F4C8</span> Execution Time Trend</h2>
            <canvas id="trendChart"></canvas>
        </div>

        <div class="card">
            <h2><span class="icon">\U0001F916</span> Agent Performance (Avg Duration)</h2>
            <canvas id="agentChart"></canvas>
        </div>

        <div class="card">
            <h2><span class="icon">\u2318</span> Command Performance</h2>
            <canvas id="commandChart"></canvas>
        </div>

        <div class="card wide">
            <h2><span class="icon">\U0001F4CB</span> Stage Details</h2>
            <table>
                <thead>
                    <tr>
                        <th>Stage</th>
                        <th>Runs</th>
                        <th>Avg</th>
                        <th>Min</th>
                        <th>Max</th>
                        <th>Std Dev</th>
                        <th>Trend</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_stage_rows(stages)}
                </tbody>
            </table>
        </div>

        <div class="card wide">
            <h2><span class="icon">\U0001F916</span> Top Agents by Usage</h2>
            <table>
                <thead>
                    <tr>
                        <th>Agent</th>
                        <th>Invocations</th>
                        <th>Avg Time</th>
                        <th>Total Time</th>
                    </tr>
                </thead>
                <tbody>
                    {self._generate_agent_rows(agents)}
                </tbody>
            </table>
        </div>
    </div>

    <div class="footer">
        HTEC Phase Execution Time Analytics v1.0.0 |
        System: {system_name}
    </div>

    <script>
        // Color palette
        const colors = {{
            primary: '#3498db',
            secondary: '#2ecc71',
            warning: '#f39c12',
            danger: '#e74c3c',
            purple: '#9b59b6',
            stages: ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
        }};

        // Chart defaults
        Chart.defaults.color = '#aaa';
        Chart.defaults.borderColor = 'rgba(255,255,255,0.1)';

        // Stage Chart
        new Chart(document.getElementById('stageChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(stage_labels)},
                datasets: [{{
                    label: 'Avg Duration (minutes)',
                    data: {json.dumps(stage_values)},
                    backgroundColor: colors.stages.slice(0, {len(stage_labels)}),
                    borderRadius: 6
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{ display: true, text: 'Minutes' }}
                    }}
                }}
            }}
        }});

        // Trend Chart
        const trendData = {json.dumps(trend_data)};
        new Chart(document.getElementById('trendChart'), {{
            type: 'line',
            data: {{
                labels: trendData.labels,
                datasets: trendData.datasets
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                interaction: {{
                    intersect: false,
                    mode: 'index'
                }},
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{ display: true, text: 'Minutes' }}
                    }}
                }}
            }}
        }});

        // Agent Chart
        new Chart(document.getElementById('agentChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(agent_labels)},
                datasets: [{{
                    label: 'Avg Duration (seconds)',
                    data: {json.dumps(agent_values)},
                    backgroundColor: colors.primary,
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    x: {{
                        title: {{ display: true, text: 'Seconds' }}
                    }}
                }}
            }}
        }});

        // Command Chart
        new Chart(document.getElementById('commandChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(command_labels)},
                datasets: [{{
                    label: 'Avg Duration (minutes)',
                    data: {json.dumps(command_values)},
                    backgroundColor: colors.secondary,
                    borderRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                plugins: {{
                    legend: {{ display: false }}
                }},
                scales: {{
                    x: {{
                        title: {{ display: true, text: 'Minutes' }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>'''

        return html

    def _prepare_trend_data(self, history: List[Dict]) -> Dict:
        """Prepare trend data for Chart.js."""
        if not history:
            return {'labels': [], 'datasets': []}

        # Group by stage
        by_stage: Dict[str, List[Dict]] = {}
        for run in history:
            stage = run.get('stage', 'unknown')
            if stage not in by_stage:
                by_stage[stage] = []
            by_stage[stage].append({
                'date': run.get('captured_at', '')[:10],
                'duration': run.get('duration_seconds', 0) / 60  # Convert to minutes
            })

        # Get all unique dates (last 15)
        all_dates = sorted(set(r.get('captured_at', '')[:10] for r in history if r.get('captured_at')))
        recent_dates = all_dates[-15:]

        # Build datasets
        colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
        datasets = []

        stage_order = ["discovery", "prototype", "productspecs", "solarch", "implementation"]
        color_idx = 0

        for stage in stage_order:
            if stage not in by_stage:
                continue

            runs = by_stage[stage]
            date_to_duration = {r['date']: r['duration'] for r in runs}

            data = []
            for d in recent_dates:
                val = date_to_duration.get(d)
                data.append(round(val, 2) if val is not None else None)

            # Only include if there's data
            if any(v is not None for v in data):
                datasets.append({
                    'label': stage.capitalize(),
                    'data': data,
                    'borderColor': colors[color_idx % len(colors)],
                    'backgroundColor': colors[color_idx % len(colors)] + '20',
                    'fill': False,
                    'tension': 0.3,
                    'spanGaps': True
                })
                color_idx += 1

        return {'labels': recent_dates, 'datasets': datasets}

    def _generate_stage_rows(self, stages: Dict) -> str:
        """Generate HTML table rows for stages."""
        rows = []
        stage_order = ["discovery", "prototype", "productspecs", "solarch", "implementation"]

        for stage_name in stage_order:
            data = stages.get(stage_name, {})
            if not data or data.get('runs_count', 0) == 0:
                continue

            trend = data.get('trend', 'stable')
            trend_class = 'improving' if trend == 'improving' else 'degrading' if trend == 'degrading' else 'stable'
            trend_text = '\U0001F4C8 Faster' if trend == 'improving' else '\U0001F4C9 Slower' if trend == 'degrading' else '\u27A1\uFE0F Stable'

            rows.append(f'''
                <tr>
                    <td><strong>{stage_name.capitalize()}</strong></td>
                    <td>{data.get('runs_count', 0)}</td>
                    <td>{self._format_duration(data.get('avg_duration_seconds', 0))}</td>
                    <td>{self._format_duration(data.get('min_duration_seconds', 0))}</td>
                    <td>{self._format_duration(data.get('max_duration_seconds', 0))}</td>
                    <td>{self._format_duration(data.get('stddev_seconds', 0))}</td>
                    <td><span class="badge {trend_class}">{trend_text}</span></td>
                </tr>
            ''')

        return ''.join(rows) if rows else '<tr><td colspan="7">No stage data available</td></tr>'

    def _generate_agent_rows(self, agents: Dict) -> str:
        """Generate HTML table rows for agents."""
        if not agents:
            return '<tr><td colspan="4">No agent data available</td></tr>'

        rows = []
        sorted_agents = sorted(
            agents.items(),
            key=lambda x: x[1].get('total_invocations', 0),
            reverse=True
        )[:15]

        for name, data in sorted_agents:
            total_time = data.get('avg_duration_seconds', 0) * data.get('total_invocations', 0)
            rows.append(f'''
                <tr>
                    <td><code>{name}</code></td>
                    <td>{data.get('total_invocations', 0)}</td>
                    <td>{self._format_duration(data.get('avg_duration_seconds', 0))}</td>
                    <td>{self._format_duration(total_time)}</td>
                </tr>
            ''')

        return ''.join(rows)

    def _format_duration(self, seconds: float) -> str:
        """Format seconds as human-readable."""
        if seconds is None or seconds == 0:
            return '-'
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}m"
        else:
            return f"{seconds/3600:.1f}h"
