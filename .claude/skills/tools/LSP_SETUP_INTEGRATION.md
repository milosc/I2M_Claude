# LSP Setup Integration

## Overview

The LSP (Language Server Protocol) tools specified in `setup_lsp.py` have been fully integrated into the HTEC dependencies installer. These tools are now automatically installed and configured when running `/htec-libraries-init`.

## What Was Changed

### 1. Updated `htec_dependencies_installer.py`

**Added NPM Packages Section:**
```python
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
```

**Added Node.js to System Dependencies:**
- Node.js is now checked as a system dependency
- Required for npm package installation

**Added New Functions:**
- `install_npm_packages()` - Installs npm packages globally
- `update_shell_config()` - Adds `ENABLE_LSP_TOOL=1` to shell config files

**Updated `check_only_mode()`:**
- Now checks npm package installation status
- Verifies shell configuration has LSP flag

**Updated `main()` Function:**
- NPM packages are installed after Playwright
- Shell configuration is updated automatically
- Exit codes handle npm package failures

### 2. Updated `htec-libraries-init.md`

**Added NPM Packages Section:**
```markdown
### NPM Packages (global)

| Package | Description | Used By |
|---------|-------------|---------|
| **typescript** | TypeScript compiler | Prototype code generation, LSP diagnostics |
| **@vtsls/language-server** | TypeScript/JavaScript language server | LSP diagnostics, code intelligence |
| **@anthropic-ai/claude-code** | Claude Code CLI | Enhanced debugging, LSP integration |
```

**Added to System Dependencies:**
- `node` - Node.js runtime (required for npm packages)

**Added Shell Configuration Note:**
- Documents that `ENABLE_LSP_TOOL=1` is automatically added to shell config

### 3. Updated `CLAUDE.md`

**Added LSP Support Note:**
```markdown
**LSP Support**: The installer automatically sets up Language Server Protocol support for enhanced code intelligence during prototype generation and debugging. This provides real-time TypeScript diagnostics, auto-completion, and error detection.
```

## How It Works

### Installation Flow

1. **User runs**: `/htec-libraries-init` or `python3 .claude/skills/tools/htec_dependencies_installer.py`

2. **Installer checks**:
   - Python version
   - System dependencies (including Node.js)
   - Creates `.venv` for Python packages
   - Installs Python packages
   - Installs Playwright browsers

3. **NPM Installation**:
   - Checks if npm is available
   - Installs `typescript` globally
   - Installs `@vtsls/language-server` globally
   - Installs `@anthropic-ai/claude-code` globally

4. **Shell Configuration**:
   - Adds `export ENABLE_LSP_TOOL=1` to `~/.zshrc`
   - Adds `export ENABLE_LSP_TOOL=1` to `~/.bashrc`
   - Notifies user to restart terminal or source config

### Check Mode

```bash
python3 .claude/skills/tools/htec_dependencies_installer.py --check
```

Now includes:
- NPM package installation status
- Shell configuration LSP flag status

### Error Handling

- If npm is not available, skips npm packages with warning
- If individual npm packages fail, continues with others
- Logs all failures with descriptive error messages
- Exit code reflects partial failures

## Usage

### Full Installation

```bash
/htec-libraries-init
```

This will:
1. Install all Python packages in `.venv`
2. Install Playwright browsers
3. Install npm packages globally (TypeScript, LSP server, Claude Code CLI)
4. Update shell configuration for LSP support

### Check Installation Status

```bash
python3 .claude/skills/tools/htec_dependencies_installer.py --check
```

Output includes:
```
[NPM Packages]
  ✅ typescript - already installed
  ✅ @vtsls/language-server - already installed
  ✅ @anthropic-ai/claude-code - already installed

[Shell Configuration]
  ✅ ~/.zshrc - LSP enabled
  ✅ ~/.bashrc - LSP enabled
```

### Manual Installation (if needed)

If npm packages fail during automatic installation:

```bash
# Install TypeScript
npm install -g typescript

# Install VTSLS Language Server
npm install -g @vtsls/language-server

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Add to shell config manually
echo "export ENABLE_LSP_TOOL=1" >> ~/.zshrc
source ~/.zshrc
```

## When LSP Is Used

The LSP tools are automatically available during:

1. **Prototype Code Generation** (Phase 11-12)
   - Real-time TypeScript diagnostics
   - Auto-completion suggestions
   - Type checking

2. **Debugging Sessions**
   - Enhanced error detection
   - Code intelligence
   - Symbol navigation

3. **Code Review** (Implementation Phase)
   - Static analysis
   - Type inference
   - Refactoring support

## Verification

After installation, verify LSP is active:

```bash
# Check npm packages
npm list -g typescript
npm list -g @vtsls/language-server
npm list -g @anthropic-ai/claude-code

# Check shell config
grep "ENABLE_LSP_TOOL" ~/.zshrc

# Check environment variable (in new terminal)
echo $ENABLE_LSP_TOOL
# Should output: 1
```

## Troubleshooting

### Node.js Not Found

```bash
# macOS
brew install node

# Verify
node --version
npm --version
```

### NPM Package Installation Fails

```bash
# Try with sudo (if permissions issue)
sudo npm install -g typescript @vtsls/language-server @anthropic-ai/claude-code

# Or fix npm permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
```

### Shell Config Not Updated

```bash
# Manually add to both files
echo "export ENABLE_LSP_TOOL=1" >> ~/.zshrc
echo "export ENABLE_LSP_TOOL=1" >> ~/.bashrc

# Apply changes
source ~/.zshrc
source ~/.bashrc
```

### LSP Not Active

```bash
# Check if variable is set
echo $ENABLE_LSP_TOOL

# If not set, restart terminal or:
source ~/.zshrc  # or ~/.bashrc

# Verify again
echo $ENABLE_LSP_TOOL
```

## Files Modified

| File | Changes |
|------|---------|
| `.claude/skills/tools/htec_dependencies_installer.py` | Added npm packages, install functions, shell config update |
| `.claude/commands/htec-libraries-init.md` | Added npm packages documentation |
| `CLAUDE.md` | Added LSP support note |
| `~/.zshrc` | Added `export ENABLE_LSP_TOOL=1` (during installation) |
| `~/.bashrc` | Added `export ENABLE_LSP_TOOL=1` (during installation) |

## Benefits

1. **Automatic Setup**: No manual steps required - everything is configured by `/htec-libraries-init`
2. **Type Safety**: TypeScript compiler ensures type correctness during code generation
3. **Code Intelligence**: LSP provides real-time diagnostics and suggestions
4. **Enhanced Debugging**: Better error messages and code navigation
5. **Consistent Environment**: All developers get the same LSP setup

## Next Steps

No action required! The LSP tools will be installed automatically the next time someone runs:

```bash
/htec-libraries-init
```

Or for existing installations, just run the installer again to add LSP support:

```bash
python3 .claude/skills/tools/htec_dependencies_installer.py
```
