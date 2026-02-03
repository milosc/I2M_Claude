'use client';

import { useState, useEffect } from 'react';

type Theme = 'light' | 'dark' | 'system';
type FontSize = 'small' | 'medium' | 'large';

interface Preferences {
  theme: Theme;
  fontSize: FontSize;
  workflowPath: string;
}

export default function SettingsPage() {
  const [preferences, setPreferences] = useState<Preferences>({
    theme: 'system',
    fontSize: 'medium',
    workflowPath: '.claude/architecture/workflows',
  });

  // Load preferences from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('user_preferences');
    if (saved) {
      setPreferences(JSON.parse(saved));
    }
  }, []);

  // Save preferences to localStorage
  const savePreferences = (newPreferences: Preferences) => {
    setPreferences(newPreferences);
    localStorage.setItem('user_preferences', JSON.stringify(newPreferences));

    // Apply theme
    if (newPreferences.theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else if (newPreferences.theme === 'light') {
      document.documentElement.classList.remove('dark');
    } else {
      // System preference
      const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      if (isDark) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    }

    // Apply font size
    document.documentElement.style.fontSize =
      newPreferences.fontSize === 'small' ? '14px' :
      newPreferences.fontSize === 'large' ? '18px' : '16px';
  };

  const handleThemeChange = (theme: Theme) => {
    savePreferences({ ...preferences, theme });
  };

  const handleFontSizeChange = (fontSize: FontSize) => {
    savePreferences({ ...preferences, fontSize });
  };

  const handleWorkflowPathChange = (workflowPath: string) => {
    savePreferences({ ...preferences, workflowPath });
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="border-b border-border px-4 py-3">
        <h1 className="text-xl font-bold">Settings</h1>
      </header>

      <div className="max-w-2xl mx-auto p-6 space-y-6">
        {/* Theme Settings */}
        <section className="border border-border rounded-lg p-4">
          <h2 className="text-lg font-semibold mb-4">Theme</h2>
          <div className="space-y-2">
            {(['light', 'dark', 'system'] as Theme[]).map((theme) => (
              <label key={theme} className="flex items-center gap-3 cursor-pointer">
                <input
                  type="radio"
                  name="theme"
                  value={theme}
                  checked={preferences.theme === theme}
                  onChange={() => handleThemeChange(theme)}
                  className="w-4 h-4"
                />
                <span className="capitalize">{theme}</span>
              </label>
            ))}
          </div>
        </section>

        {/* Font Size Settings */}
        <section className="border border-border rounded-lg p-4">
          <h2 className="text-lg font-semibold mb-4">Font Size</h2>
          <div className="space-y-2">
            {(['small', 'medium', 'large'] as FontSize[]).map((size) => (
              <label key={size} className="flex items-center gap-3 cursor-pointer">
                <input
                  type="radio"
                  name="fontSize"
                  value={size}
                  checked={preferences.fontSize === size}
                  onChange={() => handleFontSizeChange(size)}
                  className="w-4 h-4"
                />
                <span className="capitalize">{size}</span>
              </label>
            ))}
          </div>
        </section>

        {/* Workflow Path Settings */}
        <section className="border border-border rounded-lg p-4">
          <h2 className="text-lg font-semibold mb-4">Workflow Documentation</h2>
          <div className="space-y-2">
            <label htmlFor="workflow-path" className="block text-sm text-secondary">
              Workflow Folder Path
            </label>
            <input
              id="workflow-path"
              type="text"
              value={preferences.workflowPath}
              onChange={(e) => handleWorkflowPathChange(e.target.value)}
              placeholder=".claude/architecture/workflows"
              className="w-full px-3 py-2 border border-border rounded bg-surface-1 text-foreground"
            />
            <p className="text-xs text-secondary">
              Path to the folder containing workflow documentation markdown files.
              Default: .claude/architecture/workflows
            </p>
          </div>
        </section>

        {/* Keyboard Shortcuts */}
        <section className="border border-border rounded-lg p-4">
          <h2 className="text-lg font-semibold mb-4">Keyboard Shortcuts</h2>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>Search</span>
              <kbd className="px-2 py-1 bg-surface-2 border border-border rounded">Cmd+K</kbd>
            </div>
            <div className="flex justify-between">
              <span>Focus Navigation Tree</span>
              <kbd className="px-2 py-1 bg-surface-2 border border-border rounded">/</kbd>
            </div>
            <div className="flex justify-between">
              <span>Close Modal</span>
              <kbd className="px-2 py-1 bg-surface-2 border border-border rounded">Esc</kbd>
            </div>
            <div className="flex justify-between">
              <span>Show Shortcuts Help</span>
              <kbd className="px-2 py-1 bg-surface-2 border border-border rounded">?</kbd>
            </div>
          </div>
        </section>

        {/* Version Info */}
        <section className="border border-border rounded-lg p-4">
          <h2 className="text-lg font-semibold mb-4">Version Information</h2>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-secondary">Version</span>
              <span className="font-mono">3.0.0</span>
            </div>
            <div className="flex justify-between">
              <span className="text-secondary">Last Updated</span>
              <span>2026-01-31</span>
            </div>
            <div className="flex justify-between">
              <span className="text-secondary">Framework</span>
              <span>HTEC ClaudeManual</span>
            </div>
          </div>
        </section>

        {/* Reset Button */}
        <div className="pt-4">
          <button
            onClick={() => {
              localStorage.removeItem('user_preferences');
              setPreferences({ theme: 'system', fontSize: 'medium', workflowPath: '.claude/architecture/workflows' });
            }}
            className="px-4 py-2 border border-border rounded hover:bg-surface-2"
          >
            Reset to Defaults
          </button>
        </div>
      </div>
    </div>
  );
}
