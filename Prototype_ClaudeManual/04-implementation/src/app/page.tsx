'use client';

import { useState, useEffect, useCallback, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { NavigationTree } from '@/components/NavigationTree';
import { DetailPane } from '@/components/DetailPane';
import { StageFilterDropdown } from '@/components/StageFilterDropdown';
import { ResizableSidebar } from '@/components/ResizableSidebar';
import { getComponentStages, getPreferences, toggleFavorite } from '@/lib/localStorage';

interface FrontmatterAttributes {
  model?: string | null;
  context?: string | null;
  agent?: string | null;
  allowed_tools?: string[];
  skills_required?: string[];
  argument_hint?: string | null;
  invokes_skills?: string[];
  orchestrates_agents?: string[];
  checkpoint?: number | null;
  color?: string;
  loads_skills?: string[];
  spawned_by?: string[];
  [key: string]: unknown;
}

interface FrameworkItem {
  id: string;
  name: string;
  type: 'skill' | 'command' | 'agent';
  description: string;
  stage: string;
  path: string;
  frontmatter?: FrontmatterAttributes;
  rawContent?: string;
}

interface TreeNode {
  id: string;
  label: string;
  type: 'category' | 'skill' | 'command' | 'agent' | 'rule' | 'hook';
  stage?: string;
  stages?: string[];  // All stages (custom or original) for filtering
  path?: string;
  description?: string;
  children?: TreeNode[];
  count?: number;
}

// Helper to get effective stages for a component (custom if set, otherwise original)
function getEffectiveStages(id: string, originalStage: string): string[] {
  const customStages = getComponentStages(id);
  if (customStages.length > 0) {
    // Custom stages are stored as enum values (e.g., "Discovery"), convert to lowercase
    return customStages.map(s => s.toLowerCase());
  }
  return [originalStage.toLowerCase()];
}

function transformToTreeNodes(skills: FrameworkItem[], commands: FrameworkItem[], agents: FrameworkItem[]): TreeNode[] {
  return [
    {
      id: 'skills',
      label: 'Skills',
      type: 'category' as const,
      count: skills.length,
      children: skills.map(s => {
        const stages = getEffectiveStages(s.id, s.stage);
        return {
          id: s.id,
          label: s.name,
          type: 'skill' as const,
          stage: stages[0],  // Primary stage for display
          stages,            // All stages for filtering
          path: s.path,
          description: s.description,
        };
      }),
    },
    {
      id: 'commands',
      label: 'Commands',
      type: 'category' as const,
      count: commands.length,
      children: commands.map(c => {
        const stages = getEffectiveStages(c.id, c.stage);
        return {
          id: c.id,
          label: c.name,
          type: 'command' as const,
          stage: stages[0],
          stages,
          path: c.path,
          description: c.description,
        };
      }),
    },
    {
      id: 'agents',
      label: 'Agents',
      type: 'category' as const,
      count: agents.length,
      children: agents.map(a => {
        const stages = getEffectiveStages(a.id, a.stage);
        return {
          id: a.id,
          label: a.name,
          type: 'agent' as const,
          stage: stages[0],
          stages,
          path: a.path,
          description: a.description,
        };
      }),
    },
  ];
}

async function fetchSkills(): Promise<FrameworkItem[]> {
  const response = await fetch('/api/skills');
  if (!response.ok) throw new Error('Failed to load skills');
  return response.json();
}

async function fetchCommands(): Promise<FrameworkItem[]> {
  const response = await fetch('/api/commands');
  if (!response.ok) throw new Error('Failed to load commands');
  return response.json();
}

async function fetchAgents(): Promise<FrameworkItem[]> {
  const response = await fetch('/api/agents');
  if (!response.ok) throw new Error('Failed to load agents');
  return response.json();
}

export default function Home() {
  const [selectedItem, setSelectedItem] = useState<FrameworkItem | null>(null);
  const [selectedStages, setSelectedStages] = useState<string[]>([]);
  const [expandedNodes, setExpandedNodes] = useState<string[]>([]);
  // Trigger tree refresh when stages are modified (PF-003)
  const [stagesVersion, setStagesVersion] = useState(0);
  // Favorites state
  const [favoriteIds, setFavoriteIds] = useState<string[]>([]);

  const {
    data: skills,
    isLoading: skillsLoading,
    error: skillsError,
  } = useQuery({
    queryKey: ['skills'],
    queryFn: fetchSkills,
  });

  const {
    data: commands,
    isLoading: commandsLoading,
    error: commandsError,
  } = useQuery({
    queryKey: ['commands'],
    queryFn: fetchCommands,
  });

  const {
    data: agents,
    isLoading: agentsLoading,
    error: agentsError,
  } = useQuery({
    queryKey: ['agents'],
    queryFn: fetchAgents,
  });

  const isLoading = skillsLoading || commandsLoading || agentsLoading;
  const error = skillsError || commandsError || agentsError;

  // Transform to tree nodes - re-runs when stagesVersion changes (PF-003)
  const treeNodes = useMemo(() => {
    return transformToTreeNodes(skills || [], commands || [], agents || []);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [skills, commands, agents, stagesVersion]);

  // Callback to refresh tree when stages are modified in DetailPane
  const handleStagesUpdated = useCallback(() => {
    setStagesVersion(v => v + 1);
  }, []);

  // Load favorites on mount
  useEffect(() => {
    const prefs = getPreferences();
    setFavoriteIds(prefs.favorites);
  }, []);

  // Handle favorite toggle
  const handleToggleFavorite = useCallback((itemId: string) => {
    toggleFavorite(itemId);
    const prefs = getPreferences();
    setFavoriteIds(prefs.favorites);
  }, []);

  // Combine all items (flat)
  const allItems = [
    ...(skills || []),
    ...(commands || []),
    ...(agents || []),
  ];

  // Load last viewed item from sessionStorage
  useEffect(() => {
    const lastViewed = sessionStorage.getItem('last_viewed');
    if (lastViewed && allItems.length > 0) {
      const item = allItems.find((i) => i.id === lastViewed);
      if (item) setSelectedItem(item);
    }
  }, [allItems.length]);

  // Save selected item to sessionStorage
  useEffect(() => {
    if (selectedItem) {
      sessionStorage.setItem('last_viewed', selectedItem.id);
    }
  }, [selectedItem]);

  const handleItemSelect = (item: FrameworkItem) => {
    setSelectedItem(item);
  };

  const handleStageChange = (stages: string[]) => {
    setSelectedStages(stages);
  };

  if (isLoading) {
    return (
      <main className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <p>Loading framework components...</p>
      </main>
    );
  }

  if (error) {
    return (
      <main className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-4">Failed to load framework components</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-accent-default text-white rounded hover:bg-accent-hover"
          >
            Retry
          </button>
        </div>
      </main>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      {/* Header */}
      <header className="border-b border-border px-4 py-3 flex items-center gap-4">
        <div className="flex-1">
          <h1 className="text-xl font-bold">ClaudeManual</h1>
        </div>
        <StageFilterDropdown
          selectedStages={selectedStages as any}
          onChange={(stages) => setSelectedStages(stages as string[])}
        />
      </header>

      {/* Main dual-pane layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Navigation Tree (Sidebar) */}
        <ResizableSidebar
          storageKey="main-sidebar-width"
          minWidth={240}
          maxWidth={500}
          defaultWidth={320}
        >
          <NavigationTree
            items={treeNodes as any}
            onSelect={(itemId: string) => {
              const item = allItems.find(i => i.id === itemId);
              if (item) handleItemSelect(item);
            }}
            stageFilter={selectedStages as any}
            favorites={favoriteIds}
          />
        </ResizableSidebar>

        {/* Detail Pane (Main) */}
        <main className="flex-1 overflow-y-auto">
          <DetailPane
            item={selectedItem ? {
              ...selectedItem,
              type: selectedItem.type || 'skill',
              stage: selectedItem.stage.toLowerCase() as any,
              frontmatter: selectedItem.frontmatter,
              rawContent: selectedItem.rawContent,
              isFavorite: favoriteIds.includes(selectedItem.id),
            } : null}
            onStagesUpdated={handleStagesUpdated}
            onToggleFavorite={handleToggleFavorite}
          />
        </main>
      </div>

      {/* Footer */}
      <footer className="border-t border-border px-4 py-2 text-sm text-secondary">
        Version 3.0.0 | Last Updated: 2026-01-31 | © HTEC Framework
      </footer>
    </div>
  );
}
