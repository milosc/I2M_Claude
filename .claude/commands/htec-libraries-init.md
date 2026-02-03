---
name: htec-libraries-init
description: Install all required dependencies for HTEC framework workflows
argument-hint: None
model: claude-haiku-4-5-20250515
allowed-tools: Read, Write, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-libraries-init started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" command /htec-libraries-init ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run these commands:

```bash
# 1. Update session context
bash "$CLAUDE_PROJECT_DIR/.claude/hooks/session-update.sh" --stage "utility"

# 2. Log command start
bash .claude/hooks/log-lifecycle.sh command /htec-libraries-init instruction_start '{"stage": "utility", "method": "instruction-based"}'
```
## What Gets Installed

### Python Packages (in .venv)

| Category | Packages | Used By |
|----------|----------|---------|
| **Core** | PyPDF2 | PDF splitting (Discovery) |
| **PDF** | pypdf, pdfplumber, reportlab, pdf2image | PDF processing skills |
| **Office** | openpyxl, python-docx, python-pptx | Excel, Word, PowerPoint skills |
| **Data** | pandas, numpy | Data analysis, spreadsheets |
| **Image** | Pillow | Image processing |
| **XML** | lxml, defusedxml | Document parsing |
| **Markitdown** | markitdown[pdf,docx,pptx,xlsx] | Document conversion |
| **AI** | openai | OpenRouter API (markitdown AI) |
| **Playwright** | playwright | Web testing, screenshots |
| **OCR** | pytesseract | Text extraction from images |

### NPM Packages (global)

| Package | Description | Used By |
|---------|-------------|---------|
| **typescript** | TypeScript compiler | Prototype code generation, LSP diagnostics |
| **@vtsls/language-server** | TypeScript/JavaScript language server | LSP diagnostics, code intelligence |
| **@anthropic-ai/claude-code** | Claude Code CLI | Enhanced debugging, LSP integration |

### Playwright Browsers
- Chromium (for webapp-testing, UI audit)

### System Dependencies (manual, via brew)
- `node` - Node.js runtime (required for npm packages)
- `yt-dlp` - YouTube downloads
- `tesseract` - OCR engine
- `poppler` - PDF utilities

### Shell Configuration
- `ENABLE_LSP_TOOL=1` added to `~/.zshrc` and `~/.bashrc` for LSP support

## Usage

### Full Installation (Recommended)
```bash
python3 .claude/skills/tools/htec_dependencies_installer.py
```

### Check What's Installed
```bash
python3 .claude/skills/tools/htec_dependencies_installer.py --check
```

### Python Packages Only
```bash
python3 .claude/skills/tools/htec_dependencies_installer.py --python-only
```

### Skip Playwright Browsers
```bash
python3 .claude/skills/tools/htec_dependencies_installer.py --skip-playwright
```

## Execution Steps

When this command is invoked:

1. **Run the installer script**:
   ```bash
   python3 .claude/skills/tools/htec_dependencies_installer.py
   ```

2. **Verify installation**:
   ```bash
   python3 .claude/skills/tools/htec_dependencies_installer.py --check
   ```

3. **Install system dependencies** (if on macOS and missing):
   ```bash
   brew install yt-dlp tesseract poppler
   ```

## Post-Installation

After installation, scripts can be run using:
```bash
.venv/bin/python <script.py>
```

Or activate the virtual environment:
```bash
source .venv/bin/activate
python <script.py>
```

## Error Handling

| Error | Solution |
|-------|----------|
| `externally-managed-environment` | Script uses .venv (handles this automatically) |
| Package install fails | Logged, continues with other packages |
| Playwright install fails | Manual: `.venv/bin/python -m playwright install chromium` |
| System dep missing | Manual: `brew install <package>` |

## Files Created

- `.venv/` - Python virtual environment with all packages
- Playwright browsers installed in system cache

## Related Commands

- `/discovery` - Uses PDF processing packages
- `/prototype` - Uses Playwright for UI testing

## Troubleshooting

### Virtual environment issues
```bash
# Remove and recreate
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # If you have one
```

### Playwright issues
```bash
# Reinstall browsers
.venv/bin/python -m playwright install chromium

# Install all browsers
.venv/bin/python -m playwright install
```

### Package-specific issues
```bash
# Reinstall a specific package
.venv/bin/pip install --force-reinstall <package>
```
