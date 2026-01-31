import os
import subprocess
import shutil

def run_command(command):
    """Runs a shell command and returns the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.return_stdout.strip(), result.returncode
    except Exception:
        return None, 1

def check_npm_package(package_name):
    """Checks if a global npm package is installed."""
    print(f"Checking for {package_name}...")
    _, code = run_command(f"npm list -g {package_name}")
    return code == 0

def update_shell_config(config_file, export_line):
    """Adds the export line to the config file if it doesn't exist."""
    path = os.path.expanduser(config_file)
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()
        
        if export_line not in content:
            print(f"Adding LSP flag to {config_file}...")
            with open(path, "a") as f:
                f.write(f"\n# Claude Code LSP Support\n{export_line}\n")
        else:
            print(f"LSP flag already exists in {config_file}.")
    else:
        print(f"Skipping {config_file} (file not found).")

def main():
    # 1. Check/Install Claude Code CLI
    if not check_npm_package("@anthropic-ai/claude-code"):
        print("Installing Claude Code CLI...")
        run_command("npm install -g @anthropic-ai/claude-code")
    else:
        print("Claude Code CLI is already installed.")

    # 2. Check/Install VTSLS (Language Server)
    if not check_npm_package("@vtsls/language-server"):
        print("Installing VTSLS Language Server...")
        run_command("npm install -g @vtsls/language-server typescript")
    else:
        print("VTSLS is already installed.")

    # 3. Update Shell Profiles
    lsp_export = "export ENABLE_LSP_TOOL=1"
    update_shell_config("~/.zshrc", lsp_export)
    update_shell_config("~/.bashrc", lsp_export)

    print("\n--- Setup Complete ---")
    print("Please restart your terminal or run: source ~/.zshrc (or ~/.bashrc)")

if __name__ == "__main__":
    main()