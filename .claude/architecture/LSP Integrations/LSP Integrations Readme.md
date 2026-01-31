
# 📘 Claude Code: LSP Integration Guide

## 1. What is LSP?

The **Language Server Protocol (LSP)** is an open standard that allows a "Server" (an intelligence engine for a specific language) to communicate with a "Client" (like Claude Code, VS Code, or Vim).

Instead of Claude "guessing" where a function is defined using probabilistic patterns, LSP allows Claude to ask a dedicated engine: *"Exactly where is this symbol defined?"* and get a deterministic, compiler-grade answer.

## 2. Benefits in Claude Code

Integrating LSP transforms Claude from a "clever guesser" into a "structural expert":

* **100x Faster Navigation:** Claude can jump to definitions (`goToDefinition`) and find references instantly without running multiple slow `grep` searches.
* **Token Efficiency:** Because Claude gets the exact coordinates of code, it doesn't need to "read" dozens of irrelevant files just to find a class definition, saving you significant API costs.
* **Real-time Diagnostics:** Claude can see linter errors and type-mismatches as they happen, allowing it to fix bugs before you even run the code.
* **Safe Refactoring:** Claude can perform project-wide renames and signature changes with the confidence that it won't miss a single instance.

---

## 3. Installation Guide

Integrating LSP into Claude Code is a **two-step process**:

1. **Install the Binary:** Install the language server on your OS.
2. **Enable the Plugin:** Link the binary to Claude Code.

### Step A: System Binary Installation

Run the command for your specific language:

| Language | Recommended Server | Installation Command |
| --- | --- | --- |
| **TypeScript/JS** | `vtsls` | `npm install -g @vtsls/language-server typescript` |
| **Python** | `pyright` | `npm install -g pyright` |
| **Rust** | `rust-analyzer` | `rustup component add rust-analyzer` |
| **Go** | `gopls` | `go install golang.org/x/tools/gopls@latest` |
| **C#** | `csharp-ls` | `dotnet tool install -g csharp-ls` |
| **C/C++** | `clangd` | `brew install llvm` (macOS) or `sudo apt install clangd` |
| **PHP** | `intelephense` | `npm install -g intelephense` |

### Step B: Claude Code Integration

Once the binaries are in your system `PATH`, enable them in Claude Code:

1. **Open Claude Code** in your project directory.
2. **Add the LSP Marketplace:**
```bash
/plugin marketplace add Piebald-AI/claude-code-lsps

```


3. **Install your Language Plugin:**
```bash
/plugin install typescript-lsp@Piebald-AI/claude-code-lsps
# Replace 'typescript' with your language (python, rust, csharp, etc.)

```


4. **Apply Stability Patch (Recommended):**
Because native LSP support is in active development, many users require the community `tweakcc` patch to stabilize the connection:
```bash
npx tweakcc --apply

```


5. **Restart:** Exit (`/exit`) and restart Claude.

---

## 4. Verifying the Connection

To ensure your LSP is active, try these commands inside a Claude Code session:

* **Hover Intelligence:** *"Hover over the `UserService` class and tell me its type signature."*
* **Definition Lookup:** *"Open the file where `CalculateTax` is defined."*
* **Error Check:** *"Are there any LSP diagnostics or type errors in the current folder?"*

---

## 5. Manual Configuration (Advanced)

If you are using a niche language, you can manually define an LSP in your `.claude/settings.json`:

```json
{
  "lsp": {
    "my-lang": {
      "command": ["my-lang-server", "--stdio"],
      "filetypes": ["mylang"]
    }
  }
}

```

```json
{
  "enabledPlugins": {
    "typescript-lsp@Piebald-AI/claude-code-lsps": true,
    "python-lsp@Piebald-AI/claude-code-lsps": true,
    "csharp-lsp@Piebald-AI/claude-code-lsps": true
  },
  "lsp": {
    "csharp": {
      "command": ["csharp-ls"],
      "filetypes": ["cs"],
      "rootPatterns": ["*.sln", "*.csproj"]
    },
    "typescript": {
      "command": ["vtsls", "--stdio"],
      "filetypes": ["ts", "tsx", "js", "jsx"],
      "rootPatterns": ["package.json", "tsconfig.json"]
    },
    "python": {
      "command": ["pyright-langserver", "--stdio"],
      "filetypes": ["py"],
      "rootPatterns": ["pyproject.toml", "setup.py", "requirements.txt"]
    }
  },
  "experimental": {
    "livenessChecks": true,
    "smartContextRefinement": true
  }
}

```