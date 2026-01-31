#!/usr/bin/env python3
"""
HTEC Dependencies Installer
===========================
Installs all dependencies required for HTEC skills to function.

This script:
1. Creates/updates a Python virtual environment (.venv)
2. Installs all required Python packages
3. Installs Playwright browsers
4. Checks for system dependencies (brew packages)
5. Provides clear error messages and manual fallback instructions

Usage:
    python3 .claude/skills/tools/htec_dependencies_installer.py [options]

Options:
    --check         Only check what's installed, don't install anything
    --python-only   Only install Python packages
    --system-only   Only check/install system dependencies
    --skip-playwright  Skip Playwright browser installation
    --verbose       Show detailed output
    --help          Show this help message

Exit codes:
    0 - Success
    1 - Partial success (some optional dependencies failed)
    2 - Critical failure (venv or essential packages failed)
"""

import sys
import os
import subprocess
import shutil
import platform
from pathlib import Path

# Configuration
VENV_DIR = ".venv"
PYTHON_MIN_VERSION = (3, 9)

# Python packages organized by category
PYTHON_PACKAGES = {
    # Core packages (required for basic functionality)
    "core": [
        "PyPDF2",           # PDF splitting (Discovery)
        "tomlkit",          # TOML configuration parsing
    ],
    # PDF processing
    "pdf": [
        "pypdf",            # PDF operations
        "pdfplumber",       # PDF text/table extraction
        "reportlab",        # PDF creation
        "pdf2image",        # PDF to image conversion
    ],
    # Office documents
    "office": [
        "openpyxl",         # Excel operations
        "python-docx",      # Word documents
        "python-pptx",      # PowerPoint
    ],
    # Data & analysis
    "data": [
        "pandas",           # Data analysis
        "numpy",            # Numerical computing
    ],
    # Image processing
    "image": [
        "Pillow",           # Image processing
    ],
    # XML processing
    "xml": [
        "lxml",             # XML processing
        "defusedxml",       # Secure XML parsing
    ],
    # Document conversion (markitdown with extras)
    "markitdown": [
        "markitdown[pdf,docx,pptx,xlsx]",  # Document conversion
    ],
    # AI/API clients
    "ai": [
        "openai",           # OpenAI SDK (for OpenRouter)
    ],
    # Web automation
    "playwright": [
        "playwright",       # Browser automation
    ],
    # Audio (optional, large)
    "audio": [
        "openai-whisper",  # Enabled for Discovery Audio Transcription
    ],
    # OCR (requires tesseract system dependency)
    "ocr": [
        "pytesseract",      # OCR wrapper
    ],
    # Cloud & AWS
    "cloud": [
        "boto3",            # AWS SDK
    ],
    # UI & Dashboards
    "ui": [
        "streamlit",        # Interactive data apps
    ],
    # Testing
    "testing": [
        "pytest",           # Testing framework
        "pytest-playwright",# Playwright integration for pytest
    ],
}

# NPM packages (global installation for LSP and debugging)
NPM_PACKAGES = {
    "typescript": {
        "check_cmd": "npm list -g typescript 2>/dev/null",
        "install_cmd": "npm install -g typescript",
        "description": "TypeScript compiler",
        "required_for": ["prototype code generation", "LSP diagnostics"],
    },
    "@vtsls/language-server": {
        "check_cmd": "npm list -g @vtsls/language-server 2>/dev/null",
        "install_cmd": "npm install -g @vtsls/language-server",
        "description": "TypeScript/JavaScript language server",
        "required_for": ["LSP diagnostics", "code intelligence"],
    },
    "@anthropic-ai/claude-code": {
        "check_cmd": "npm list -g @anthropic-ai/claude-code 2>/dev/null",
        "install_cmd": "npm install -g @anthropic-ai/claude-code",
        "description": "Claude Code CLI",
        "required_for": ["enhanced debugging", "LSP integration"],
    },
}

# System dependencies (brew on macOS)
SYSTEM_DEPS = {
    "node": {
        "check_cmd": "node --version",
        "install_cmd": "brew install node",
        "description": "Node.js runtime (required for npm packages)",
        "required_for": ["LSP", "TypeScript", "code generation"],
    },
    "ffmpeg": {
        "check_cmd": "ffmpeg -version",
        "install_cmd": "brew install ffmpeg",
        "description": "Audio/video processing",
        "required_for": ["audio-transcription-summarization"],
    },
    "yt-dlp": {
        "check_cmd": "yt-dlp --version",
        "install_cmd": "brew install yt-dlp",
        "description": "YouTube video/audio downloader",
        "required_for": ["youtube-transcript", "tapestry"],
    },
    "tesseract": {
        "check_cmd": "tesseract --version",
        "install_cmd": "brew install tesseract",
        "description": "OCR engine for image text extraction",
        "required_for": ["pdf OCR", "markitdown OCR"],
    },
    "poppler": {
        "check_cmd": "pdftotext -v",
        "install_cmd": "brew install poppler",
        "description": "PDF utilities (pdftotext, pdfinfo)",
        "required_for": ["tapestry PDF extraction"],
    },
}


def print_header(text):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_status(name, status, details=""):
    """Print a status line."""
    icons = {"ok": "✅", "fail": "❌", "skip": "⏭️", "warn": "⚠️", "info": "ℹ️"}
    icon = icons.get(status, "•")
    detail_str = f" - {details}" if details else ""
    print(f"  {icon} {name}{detail_str}")


def run_command(cmd, capture=True, check=False, env=None):
    """Run a shell command and return result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture,
            text=True,
            check=check,
            env=env or os.environ.copy()
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, "", str(e)
    except Exception as e:
        return False, "", str(e)


def check_python_version():
    """Check if Python version meets requirements."""
    version = sys.version_info[:2]
    if version < PYTHON_MIN_VERSION:
        print_status(
            f"Python {version[0]}.{version[1]}",
            "fail",
            f"Requires Python {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}+"
        )
        return False
    print_status(f"Python {version[0]}.{version[1]}", "ok")
    return True


def create_venv(venv_path):
    """Create or verify virtual environment."""
    venv_path = Path(venv_path)

    if venv_path.exists():
        # Verify it's a valid venv
        python_path = venv_path / "bin" / "python"
        if python_path.exists():
            print_status("Virtual environment", "ok", f"exists at {venv_path}")
            return True
        else:
            print_status("Virtual environment", "warn", "corrupted, recreating...")
            shutil.rmtree(venv_path)

    print_status("Virtual environment", "info", f"creating at {venv_path}...")
    success, _, stderr = run_command(f"python3 -m venv {venv_path}")

    if success:
        print_status("Virtual environment", "ok", "created")
        return True
    else:
        print_status("Virtual environment", "fail", stderr)
        return False


def get_venv_pip(venv_path):
    """Get the pip command for the virtual environment."""
    venv_path = Path(venv_path)
    pip_path = venv_path / "bin" / "pip"
    return str(pip_path)


def get_venv_python(venv_path):
    """Get the python command for the virtual environment."""
    venv_path = Path(venv_path)
    python_path = venv_path / "bin" / "python"
    return str(python_path)


def upgrade_pip(venv_path):
    """Upgrade pip in the virtual environment."""
    pip = get_venv_pip(venv_path)
    print_status("pip", "info", "upgrading...")
    success, _, stderr = run_command(f"{pip} install --upgrade pip --quiet")
    if success:
        print_status("pip", "ok", "upgraded")
    else:
        print_status("pip", "warn", f"upgrade failed: {stderr[:50]}")
    return success


def install_python_packages(venv_path, categories=None, verbose=False):
    """Install Python packages by category."""
    pip = get_venv_pip(venv_path)

    if categories is None:
        categories = list(PYTHON_PACKAGES.keys())

    results = {"installed": [], "failed": [], "skipped": []}

    for category in categories:
        if category not in PYTHON_PACKAGES:
            continue

        packages = PYTHON_PACKAGES[category]
        if not packages:
            continue

        print(f"\n  [{category}]")

        for package in packages:
            # Handle packages with extras like markitdown[pdf,docx]
            package_name = package.split("[")[0]

            # Check if already installed
            check_cmd = f"{pip} show {package_name} 2>/dev/null"
            installed, _, _ = run_command(check_cmd)

            if installed:
                print_status(package_name, "ok", "already installed")
                results["installed"].append(package)
                continue

            # Install the package
            quiet_flag = "" if verbose else "--quiet"
            install_cmd = f"{pip} install '{package}' {quiet_flag}"
            success, stdout, stderr = run_command(install_cmd)

            if success:
                print_status(package_name, "ok", "installed")
                results["installed"].append(package)
            else:
                error_msg = stderr[:100] if stderr else "unknown error"
                print_status(package_name, "fail", error_msg)
                results["failed"].append((package, error_msg))

    return results


def install_playwright_browsers(venv_path):
    """Install Playwright browser binaries."""
    python = get_venv_python(venv_path)

    print_status("Playwright browsers", "info", "installing chromium...")

    # Install just chromium (smaller than all browsers)
    success, stdout, stderr = run_command(
        f"{python} -m playwright install chromium",
        capture=True
    )

    if success:
        print_status("Playwright browsers", "ok", "chromium installed")
        return True
    else:
        error_msg = stderr[:100] if stderr else "unknown error"
        print_status("Playwright browsers", "fail", error_msg)
        print("\n    Manual installation:")
        print(f"    {python} -m playwright install chromium")
        return False


def install_npm_packages():
    """Install npm packages globally."""
    print_header("NPM Packages (for LSP and Debugging)")

    # Check if npm is available
    npm_available, _, _ = run_command("npm --version")
    if not npm_available:
        print_status("npm", "fail", "npm not found - install Node.js first")
        print("\n  Install Node.js:")
        if platform.system() == "Darwin":
            print("    brew install node")
        else:
            print("    Visit https://nodejs.org/")
        return {"installed": [], "failed": [], "skipped": list(NPM_PACKAGES.keys())}

    results = {"installed": [], "failed": [], "skipped": []}

    for name, info in NPM_PACKAGES.items():
        # Check if already installed
        success, stdout, stderr = run_command(info["check_cmd"])

        if success:
            print_status(name, "ok", "already installed")
            results["installed"].append(name)
            continue

        # Install the package
        print_status(name, "info", f"installing...")
        success, stdout, stderr = run_command(info["install_cmd"])

        if success:
            print_status(name, "ok", "installed")
            results["installed"].append(name)
        else:
            error_msg = stderr[:100] if stderr else "unknown error"
            print_status(name, "fail", error_msg)
            results["failed"].append((name, error_msg))

    return results


def update_shell_config():
    """Add ENABLE_LSP_TOOL=1 to shell configuration files."""
    print_header("Shell Configuration (LSP)")

    lsp_export = "export ENABLE_LSP_TOOL=1"
    config_files = ["~/.zshrc", "~/.bashrc"]
    updated = []

    for config_file in config_files:
        path = os.path.expanduser(config_file)

        if not os.path.exists(path):
            print_status(config_file, "skip", "file not found")
            continue

        try:
            with open(path, "r") as f:
                content = f.read()

            if lsp_export in content:
                print_status(config_file, "ok", "LSP flag already exists")
                updated.append(config_file)
            else:
                with open(path, "a") as f:
                    f.write(f"\n# Claude Code LSP Support (added by htec_dependencies_installer)\n{lsp_export}\n")
                print_status(config_file, "ok", "LSP flag added")
                updated.append(config_file)
        except Exception as e:
            print_status(config_file, "fail", str(e)[:50])

    if updated:
        print("\n  ℹ️  Restart your terminal or run:")
        if "~/.zshrc" in updated:
            print("    source ~/.zshrc")
        if "~/.bashrc" in updated:
            print("    source ~/.bashrc")

    return updated


def check_system_dependencies():
    """Check for system dependencies (brew packages)."""
    print_header("System Dependencies")

    is_macos = platform.system() == "Darwin"
    results = {"installed": [], "missing": []}

    for name, info in SYSTEM_DEPS.items():
        success, stdout, stderr = run_command(info["check_cmd"])

        if success:
            print_status(name, "ok", info["description"])
            results["installed"].append(name)
        else:
            print_status(name, "warn", f"not installed - {info['description']}")
            results["missing"].append(name)

    if results["missing"]:
        print("\n  To install missing system dependencies:")
        if is_macos:
            for name in results["missing"]:
                print(f"    {SYSTEM_DEPS[name]['install_cmd']}")
        else:
            print("    Please install using your system package manager")

    return results


def check_only_mode():
    """Check what's installed without making changes."""
    print_header("Dependency Check (Read-Only)")

    # Check Python
    print("\n[Python]")
    check_python_version()

    # Check venv
    print("\n[Virtual Environment]")
    venv_path = Path(VENV_DIR)
    if venv_path.exists() and (venv_path / "bin" / "python").exists():
        print_status(".venv", "ok", "exists")

        # Check installed packages
        pip = get_venv_pip(VENV_DIR)
        print("\n[Python Packages]")

        for category, packages in PYTHON_PACKAGES.items():
            if not packages:
                continue
            for package in packages:
                package_name = package.split("[")[0]
                check_cmd = f"{pip} show {package_name} 2>/dev/null"
                installed, _, _ = run_command(check_cmd)
                status = "ok" if installed else "warn"
                print_status(package_name, status, "installed" if installed else "not installed")
    else:
        print_status(".venv", "warn", "not created")

    # Check npm packages
    print("\n[NPM Packages]")
    npm_available, _, _ = run_command("npm --version")
    if npm_available:
        for name, info in NPM_PACKAGES.items():
            success, _, _ = run_command(info["check_cmd"])
            status = "ok" if success else "warn"
            print_status(name, status, "installed" if success else "not installed")
    else:
        print_status("npm", "warn", "not available")

    # Check shell config for LSP flag
    print("\n[Shell Configuration]")
    lsp_export = "export ENABLE_LSP_TOOL=1"
    for config_file in ["~/.zshrc", "~/.bashrc"]:
        path = os.path.expanduser(config_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read()
            has_lsp = lsp_export in content
            status = "ok" if has_lsp else "warn"
            print_status(config_file, status, "LSP enabled" if has_lsp else "LSP not configured")

    # Check system deps
    check_system_dependencies()

    print("\n" + "="*60)
    print("  Run without --check to install missing dependencies")
    print("="*60 + "\n")


def main():
    """Main installation routine."""
    args = sys.argv[1:]

    # Parse arguments
    check_mode = "--check" in args
    python_only = "--python-only" in args
    system_only = "--system-only" in args
    skip_playwright = "--skip-playwright" in args
    verbose = "--verbose" in args

    if "--help" in args:
        print(__doc__)
        sys.exit(0)

    if check_mode:
        check_only_mode()
        sys.exit(0)

    print_header("HTEC Dependencies Installer")
    print("  This will install all dependencies required for HTEC skills.\n")

    exit_code = 0

    # Check Python version
    if not check_python_version():
        sys.exit(2)

    # System dependencies (if not python-only)
    if not python_only:
        check_system_dependencies()

    # Python packages (if not system-only)
    if not system_only:
        print_header("Python Environment Setup")

        # Create virtual environment
        if not create_venv(VENV_DIR):
            print("\n❌ Failed to create virtual environment.")
            print("   Try manually: python3 -m venv .venv")
            sys.exit(2)

        # Upgrade pip
        upgrade_pip(VENV_DIR)

        # Install Python packages
        print_header("Installing Python Packages")
        results = install_python_packages(VENV_DIR, verbose=verbose)

        if results["failed"]:
            print(f"\n⚠️  {len(results['failed'])} packages failed to install:")
            for pkg, error in results["failed"]:
                print(f"    - {pkg}")
            exit_code = 1

        # Install Playwright browsers
        if not skip_playwright and "playwright" not in [p for p, _ in results.get("failed", [])]:
            print_header("Playwright Browser Installation")
            if not install_playwright_browsers(VENV_DIR):
                exit_code = 1

    # NPM packages (for LSP and code generation)
    if not python_only:
        npm_results = install_npm_packages()
        if npm_results["failed"]:
            print(f"\n⚠️  {len(npm_results['failed'])} npm packages failed to install:")
            for pkg, error in npm_results["failed"]:
                print(f"    - {pkg}")
            exit_code = 1

        # Update shell configuration for LSP
        if npm_results["installed"]:
            update_shell_config()

    # Summary
    print_header("Installation Summary")

    if exit_code == 0:
        print("  ✅ All dependencies installed successfully!\n")
    else:
        print("  ⚠️  Some dependencies failed to install.")
        print("     The skills may still work with reduced functionality.\n")

    print("  Usage:")
    print("    Activate venv:  source .venv/bin/activate")
    print("    Run scripts:    .venv/bin/python <script.py>")
    print("")
    print("  Example:")
    print("    .venv/bin/python .claude/skills/tools/pdf_splitter.py count file.pdf")
    print("")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
