#!/usr/bin/env python3
"""
Playwright Visual QA Tool

A CLI utility for capturing screenshots, running visual regression tests,
and generating visual comparison reports for prototype validation.

Usage:
    python playwright_visual_qa.py capture <url> <output_dir> [--screens <file>]
    python playwright_visual_qa.py compare <baseline_dir> <current_dir> <output_dir>
    python playwright_visual_qa.py report <comparison_dir> <output_file>
    python playwright_visual_qa.py full <url> <output_dir> [--screens <file>]

Requirements:
    pip install playwright pillow
    playwright install chromium
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import subprocess

# Check for required packages
try:
    from PIL import Image, ImageChops
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

try:
    from playwright.sync_api import sync_playwright, Page, Browser
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


@dataclass
class ScreenConfig:
    """Configuration for a screen to capture."""
    name: str
    url: str
    wait_selector: Optional[str] = None
    wait_timeout: int = 5000
    full_page: bool = True
    states: Optional[List[Dict]] = None  # Interactive states to capture


@dataclass
class ViewportConfig:
    """Viewport configuration."""
    name: str
    width: int
    height: int


@dataclass
class ScreenshotResult:
    """Result of a screenshot capture."""
    screen: str
    viewport: str
    path: str
    success: bool
    error: Optional[str] = None
    timestamp: str = ""


@dataclass
class ComparisonResult:
    """Result of comparing two screenshots."""
    screen: str
    viewport: str
    baseline_path: str
    current_path: str
    diff_path: Optional[str]
    diff_percentage: float
    passed: bool
    threshold: float


# Default viewports matching the validation agents
DEFAULT_VIEWPORTS = [
    ViewportConfig("desktop", 1920, 1080),
    ViewportConfig("tablet", 768, 1024),
    ViewportConfig("mobile", 375, 812),
]

# Default screens if none provided
DEFAULT_SCREENS = [
    ScreenConfig("/", "Dashboard", wait_selector="[data-testid='dashboard']"),
]


def ensure_dir(path: str) -> None:
    """Ensure directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)


def load_screens_config(config_path: str) -> List[ScreenConfig]:
    """Load screen configurations from JSON file."""
    with open(config_path, 'r') as f:
        data = json.load(f)

    screens = []
    for item in data.get('screens', []):
        screens.append(ScreenConfig(
            name=item['name'],
            url=item['url'],
            wait_selector=item.get('wait_selector'),
            wait_timeout=item.get('wait_timeout', 5000),
            full_page=item.get('full_page', True),
            states=item.get('states'),
        ))
    return screens


def capture_screenshot(
    page: Page,
    screen: ScreenConfig,
    viewport: ViewportConfig,
    output_dir: str,
    state_suffix: str = ""
) -> ScreenshotResult:
    """Capture a single screenshot."""
    timestamp = datetime.now().isoformat()

    # Generate filename
    state_part = f"-{state_suffix}" if state_suffix else ""
    filename = f"{screen.name}-{viewport.name}{state_part}.png"
    filepath = os.path.join(output_dir, viewport.name, filename)
    ensure_dir(os.path.dirname(filepath))

    try:
        # Set viewport
        page.set_viewport_size({"width": viewport.width, "height": viewport.height})

        # Navigate
        page.goto(screen.url, wait_until="networkidle")

        # Wait for selector if specified
        if screen.wait_selector:
            page.wait_for_selector(screen.wait_selector, timeout=screen.wait_timeout)

        # Additional wait for animations
        page.wait_for_timeout(500)

        # Capture
        page.screenshot(path=filepath, full_page=screen.full_page)

        return ScreenshotResult(
            screen=screen.name,
            viewport=viewport.name,
            path=filepath,
            success=True,
            timestamp=timestamp,
        )
    except Exception as e:
        return ScreenshotResult(
            screen=screen.name,
            viewport=viewport.name,
            path=filepath,
            success=False,
            error=str(e),
            timestamp=timestamp,
        )


def capture_interactive_states(
    page: Page,
    screen: ScreenConfig,
    viewport: ViewportConfig,
    output_dir: str
) -> List[ScreenshotResult]:
    """Capture interactive states (hover, focus, active) for a screen."""
    results = []

    if not screen.states:
        return results

    for state_config in screen.states:
        state_name = state_config.get('name', 'state')
        selector = state_config.get('selector')
        action = state_config.get('action', 'hover')  # hover, focus, click

        if not selector:
            continue

        try:
            element = page.query_selector(selector)
            if not element:
                continue

            # Perform action
            if action == 'hover':
                element.hover()
            elif action == 'focus':
                element.focus()
            elif action == 'click':
                element.click()

            page.wait_for_timeout(300)  # Wait for state transition

            # Capture
            result = capture_screenshot(
                page, screen, viewport, output_dir,
                state_suffix=f"{state_name}-{action}"
            )
            results.append(result)

            # Reset state
            page.mouse.move(0, 0)
            page.wait_for_timeout(100)

        except Exception as e:
            results.append(ScreenshotResult(
                screen=screen.name,
                viewport=viewport.name,
                path="",
                success=False,
                error=f"State capture failed ({state_name}): {str(e)}",
                timestamp=datetime.now().isoformat(),
            ))

    return results


def capture_all_screenshots(
    base_url: str,
    output_dir: str,
    screens: List[ScreenConfig],
    viewports: List[ViewportConfig] = None,
    browsers: List[str] = None,
    include_states: bool = True,
) -> Dict:
    """Capture screenshots for all screens across all viewports."""
    if not HAS_PLAYWRIGHT:
        print("Error: Playwright not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    viewports = viewports or DEFAULT_VIEWPORTS
    browsers = browsers or ["chromium"]

    results = {
        "capture_date": datetime.now().isoformat(),
        "base_url": base_url,
        "output_dir": output_dir,
        "screenshots": [],
        "summary": {
            "total": 0,
            "success": 0,
            "failed": 0,
        }
    }

    with sync_playwright() as p:
        for browser_name in browsers:
            browser_type = getattr(p, browser_name)
            browser = browser_type.launch(headless=True)

            for viewport in viewports:
                context = browser.new_context(
                    viewport={"width": viewport.width, "height": viewport.height}
                )
                page = context.new_page()

                for screen in screens:
                    # Prepend base URL
                    screen_with_url = ScreenConfig(
                        name=screen.name,
                        url=f"{base_url}{screen.url}",
                        wait_selector=screen.wait_selector,
                        wait_timeout=screen.wait_timeout,
                        full_page=screen.full_page,
                        states=screen.states,
                    )

                    # Capture default state
                    result = capture_screenshot(
                        page, screen_with_url, viewport, output_dir
                    )
                    results["screenshots"].append(asdict(result))
                    results["summary"]["total"] += 1
                    if result.success:
                        results["summary"]["success"] += 1
                        print(f"  Captured: {screen.name} ({viewport.name})")
                    else:
                        results["summary"]["failed"] += 1
                        print(f"  Failed: {screen.name} ({viewport.name}) - {result.error}")

                    # Capture interactive states
                    if include_states and screen.states:
                        state_results = capture_interactive_states(
                            page, screen_with_url, viewport, output_dir
                        )
                        for sr in state_results:
                            results["screenshots"].append(asdict(sr))
                            results["summary"]["total"] += 1
                            if sr.success:
                                results["summary"]["success"] += 1
                            else:
                                results["summary"]["failed"] += 1

                context.close()
            browser.close()

    return results


def compare_images(
    baseline_path: str,
    current_path: str,
    diff_path: str,
    threshold: float = 0.01
) -> ComparisonResult:
    """Compare two images and generate a diff image."""
    if not HAS_PILLOW:
        print("Error: Pillow not installed. Run: pip install pillow")
        sys.exit(1)

    try:
        baseline = Image.open(baseline_path).convert('RGB')
        current = Image.open(current_path).convert('RGB')

        # Resize if dimensions don't match
        if baseline.size != current.size:
            current = current.resize(baseline.size, Image.Resampling.LANCZOS)

        # Calculate difference
        diff = ImageChops.difference(baseline, current)

        # Calculate diff percentage
        diff_data = list(diff.getdata())
        total_pixels = len(diff_data)
        diff_pixels = sum(1 for pixel in diff_data if sum(pixel) > 30)  # Threshold for "different"
        diff_percentage = (diff_pixels / total_pixels) * 100

        # Save diff image if there are differences
        if diff_percentage > 0:
            ensure_dir(os.path.dirname(diff_path))
            # Enhance diff visibility
            diff = diff.point(lambda x: min(x * 10, 255))
            diff.save(diff_path)

        passed = diff_percentage <= (threshold * 100)

        return ComparisonResult(
            screen=os.path.basename(baseline_path).replace('.png', ''),
            viewport=os.path.basename(os.path.dirname(baseline_path)),
            baseline_path=baseline_path,
            current_path=current_path,
            diff_path=diff_path if diff_percentage > 0 else None,
            diff_percentage=round(diff_percentage, 2),
            passed=passed,
            threshold=threshold * 100,
        )
    except Exception as e:
        return ComparisonResult(
            screen=os.path.basename(baseline_path).replace('.png', ''),
            viewport="unknown",
            baseline_path=baseline_path,
            current_path=current_path,
            diff_path=None,
            diff_percentage=100.0,
            passed=False,
            threshold=threshold * 100,
        )


def compare_directories(
    baseline_dir: str,
    current_dir: str,
    diff_dir: str,
    threshold: float = 0.01
) -> Dict:
    """Compare all screenshots in two directories."""
    results = {
        "comparison_date": datetime.now().isoformat(),
        "baseline_dir": baseline_dir,
        "current_dir": current_dir,
        "diff_dir": diff_dir,
        "threshold": threshold * 100,
        "comparisons": [],
        "summary": {
            "total": 0,
            "passed": 0,
            "failed": 0,
        }
    }

    # Find all baseline images
    baseline_images = []
    for root, dirs, files in os.walk(baseline_dir):
        for file in files:
            if file.endswith('.png'):
                baseline_images.append(os.path.join(root, file))

    for baseline_path in baseline_images:
        # Construct corresponding current and diff paths
        rel_path = os.path.relpath(baseline_path, baseline_dir)
        current_path = os.path.join(current_dir, rel_path)
        diff_path = os.path.join(diff_dir, rel_path)

        if not os.path.exists(current_path):
            results["comparisons"].append({
                "screen": rel_path,
                "error": "Current screenshot missing",
                "passed": False,
            })
            results["summary"]["total"] += 1
            results["summary"]["failed"] += 1
            continue

        comparison = compare_images(baseline_path, current_path, diff_path, threshold)
        results["comparisons"].append(asdict(comparison))
        results["summary"]["total"] += 1

        if comparison.passed:
            results["summary"]["passed"] += 1
            print(f"  PASS: {rel_path} ({comparison.diff_percentage}%)")
        else:
            results["summary"]["failed"] += 1
            print(f"  FAIL: {rel_path} ({comparison.diff_percentage}% > {threshold * 100}%)")

    return results


def generate_report(results: Dict, output_path: str) -> None:
    """Generate a markdown report from comparison results."""
    report_lines = [
        "# Visual QA Report",
        "",
        f"**Generated:** {datetime.now().isoformat()}",
        "",
        "## Summary",
        "",
        "| Metric | Value | Status |",
        "|--------|-------|--------|",
        f"| **Total Screenshots** | {results['summary']['total']} | - |",
        f"| **Passed** | {results['summary']['passed']} | {':white_check_mark:' if results['summary']['passed'] == results['summary']['total'] else ':warning:'} |",
        f"| **Failed** | {results['summary']['failed']} | {':x:' if results['summary']['failed'] > 0 else ':white_check_mark:'} |",
        f"| **Diff Threshold** | {results.get('threshold', 1)}% | - |",
        "",
        f"## Overall Status: {'PASS' if results['summary']['failed'] == 0 else 'FAIL'}",
        "",
        "---",
        "",
        "## Comparison Results",
        "",
    ]

    # Group by viewport
    by_viewport = {}
    for comp in results.get('comparisons', []):
        viewport = comp.get('viewport', 'unknown')
        if viewport not in by_viewport:
            by_viewport[viewport] = []
        by_viewport[viewport].append(comp)

    for viewport, comparisons in by_viewport.items():
        report_lines.append(f"### {viewport.title()}")
        report_lines.append("")
        report_lines.append("| Screen | Diff % | Threshold | Status |")
        report_lines.append("|--------|--------|-----------|--------|")

        for comp in comparisons:
            status = ":white_check_mark: PASS" if comp.get('passed', False) else ":x: FAIL"
            diff_pct = comp.get('diff_percentage', 'N/A')
            threshold = comp.get('threshold', 1)
            screen = comp.get('screen', 'unknown')
            report_lines.append(f"| {screen} | {diff_pct}% | {threshold}% | {status} |")

        report_lines.append("")

    # Failed comparisons detail
    failed = [c for c in results.get('comparisons', []) if not c.get('passed', True)]
    if failed:
        report_lines.append("## Failed Comparisons")
        report_lines.append("")
        for comp in failed:
            report_lines.append(f"### {comp.get('screen', 'Unknown')}")
            report_lines.append("")
            report_lines.append(f"- **Viewport:** {comp.get('viewport', 'unknown')}")
            report_lines.append(f"- **Diff Percentage:** {comp.get('diff_percentage', 'N/A')}%")
            report_lines.append(f"- **Threshold:** {comp.get('threshold', 1)}%")
            if comp.get('diff_path'):
                report_lines.append(f"- **Diff Image:** [{os.path.basename(comp['diff_path'])}]({comp['diff_path']})")
            report_lines.append("")

    report_lines.extend([
        "---",
        "",
        "*Generated by playwright_visual_qa.py*",
    ])

    ensure_dir(os.path.dirname(output_path))
    with open(output_path, 'w') as f:
        f.write('\n'.join(report_lines))

    print(f"\nReport generated: {output_path}")


def cmd_capture(args):
    """Handle capture command."""
    print(f"\nCapturing screenshots from {args.url}")
    print(f"Output directory: {args.output}")

    # Load screens config
    if args.screens:
        screens = load_screens_config(args.screens)
    else:
        # Try to find screen-index.md or similar
        screens = DEFAULT_SCREENS
        print("Using default screen configuration. Specify --screens for custom config.")

    print(f"\nScreens to capture: {len(screens)}")
    print(f"Viewports: {', '.join(v.name for v in DEFAULT_VIEWPORTS)}")
    print("")

    results = capture_all_screenshots(
        args.url,
        args.output,
        screens,
        include_states=not args.no_states,
    )

    # Save results JSON
    results_path = os.path.join(args.output, "capture-results.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nCapture complete!")
    print(f"  Total: {results['summary']['total']}")
    print(f"  Success: {results['summary']['success']}")
    print(f"  Failed: {results['summary']['failed']}")
    print(f"\nResults saved to: {results_path}")


def cmd_compare(args):
    """Handle compare command."""
    print(f"\nComparing screenshots")
    print(f"Baseline: {args.baseline}")
    print(f"Current: {args.current}")
    print(f"Output: {args.output}")
    print(f"Threshold: {args.threshold * 100}%")
    print("")

    results = compare_directories(
        args.baseline,
        args.current,
        args.output,
        args.threshold,
    )

    # Save results JSON
    results_path = os.path.join(args.output, "comparison-results.json")
    ensure_dir(args.output)
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nComparison complete!")
    print(f"  Total: {results['summary']['total']}")
    print(f"  Passed: {results['summary']['passed']}")
    print(f"  Failed: {results['summary']['failed']}")
    print(f"\nResults saved to: {results_path}")

    # Generate report
    report_path = os.path.join(args.output, "visual-qa-report.md")
    generate_report(results, report_path)


def cmd_report(args):
    """Handle report command."""
    print(f"\nGenerating report from {args.comparison_dir}")

    results_path = os.path.join(args.comparison_dir, "comparison-results.json")
    if not os.path.exists(results_path):
        print(f"Error: No comparison results found at {results_path}")
        print("Run 'compare' command first.")
        sys.exit(1)

    with open(results_path, 'r') as f:
        results = json.load(f)

    generate_report(results, args.output)


def cmd_full(args):
    """Handle full workflow: capture baseline, capture current, compare, report."""
    print(f"\n=== Full Visual QA Workflow ===")
    print(f"URL: {args.url}")
    print(f"Output: {args.output}")

    baseline_dir = os.path.join(args.output, "baseline")
    current_dir = os.path.join(args.output, "current")
    diff_dir = os.path.join(args.output, "diff")

    # Check if baseline exists
    if not os.path.exists(baseline_dir) or args.update_baseline:
        print("\n--- Step 1: Capturing Baseline ---")
        # Load screens
        screens = load_screens_config(args.screens) if args.screens else DEFAULT_SCREENS
        capture_all_screenshots(args.url, baseline_dir, screens)

        if not args.compare_only:
            print("\nBaseline captured. Run again to compare.")
            return

    print("\n--- Step 2: Capturing Current State ---")
    screens = load_screens_config(args.screens) if args.screens else DEFAULT_SCREENS
    capture_all_screenshots(args.url, current_dir, screens)

    print("\n--- Step 3: Comparing Screenshots ---")
    results = compare_directories(
        baseline_dir,
        current_dir,
        diff_dir,
        args.threshold,
    )

    # Save results
    results_path = os.path.join(args.output, "comparison-results.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

    print("\n--- Step 4: Generating Report ---")
    report_path = os.path.join(args.output, "visual-qa-report.md")
    generate_report(results, report_path)

    print("\n=== Visual QA Complete ===")
    print(f"  Status: {'PASS' if results['summary']['failed'] == 0 else 'FAIL'}")
    print(f"  Report: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Playwright Visual QA Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Capture screenshots
  python playwright_visual_qa.py capture http://localhost:3000 ./screenshots

  # Compare screenshots
  python playwright_visual_qa.py compare ./baseline ./current ./diff

  # Full workflow
  python playwright_visual_qa.py full http://localhost:3000 ./visual-qa
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Capture command
    capture_parser = subparsers.add_parser("capture", help="Capture screenshots")
    capture_parser.add_argument("url", help="Base URL of the prototype")
    capture_parser.add_argument("output", help="Output directory for screenshots")
    capture_parser.add_argument("--screens", help="JSON file with screen configurations")
    capture_parser.add_argument("--no-states", action="store_true", help="Skip interactive state captures")

    # Compare command
    compare_parser = subparsers.add_parser("compare", help="Compare screenshots")
    compare_parser.add_argument("baseline", help="Baseline screenshots directory")
    compare_parser.add_argument("current", help="Current screenshots directory")
    compare_parser.add_argument("output", help="Output directory for diffs")
    compare_parser.add_argument("--threshold", type=float, default=0.01, help="Diff threshold (0-1)")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate report")
    report_parser.add_argument("comparison_dir", help="Directory with comparison results")
    report_parser.add_argument("output", help="Output report path (.md)")

    # Full workflow command
    full_parser = subparsers.add_parser("full", help="Full visual QA workflow")
    full_parser.add_argument("url", help="Base URL of the prototype")
    full_parser.add_argument("output", help="Output directory")
    full_parser.add_argument("--screens", help="JSON file with screen configurations")
    full_parser.add_argument("--threshold", type=float, default=0.01, help="Diff threshold (0-1)")
    full_parser.add_argument("--update-baseline", action="store_true", help="Update baseline screenshots")
    full_parser.add_argument("--compare-only", action="store_true", help="Skip baseline capture")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "capture": cmd_capture,
        "compare": cmd_compare,
        "report": cmd_report,
        "full": cmd_full,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
