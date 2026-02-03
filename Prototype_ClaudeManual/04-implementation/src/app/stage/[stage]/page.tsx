'use client';

import { useState } from 'react';
import { useParams, notFound } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { NavigationTree } from '@/components/NavigationTree';
import { DetailPane } from '@/components/DetailPane';
import { ResizableSidebar } from '@/components/ResizableSidebar';
import type { Stage } from '@/types/navigation';

interface FrameworkItem {
  id: string;
  name: string;
  description: string;
  stage: string;
  path: string;
}

interface TreeNode {
  id: string;
  label: string;
  type: 'category' | 'skill' | 'command' | 'agent' | 'rule' | 'hook';
  stage?: string;
  path?: string;
  description?: string;
  children?: TreeNode[];
  count?: number;
}

function transformToTreeNodes(items: FrameworkItem[], stageFilter: string): TreeNode[] {
  const filtered = items.filter(i => i.stage?.toLowerCase() === stageFilter.toLowerCase());
  return [
    {
      id: `${stageFilter}-items`,
      label: `${stageFilter.charAt(0).toUpperCase() + stageFilter.slice(1)} Components`,
      type: 'category' as const,
      count: filtered.length,
      children: filtered.map(item => ({
        id: item.id,
        label: item.name,
        type: 'skill' as const,
        stage: item.stage?.toLowerCase(),
        path: item.path,
        description: item.description,
      })),
    },
  ];
}

const VALID_STAGES = ['discovery', 'prototype', 'productspecs', 'solarch', 'implementation'];

const STAGE_COLORS: Record<string, string> = {
  discovery: 'bg-blue-50',
  prototype: 'bg-green-50',
  productspecs: 'bg-purple-50',
  solarch: 'bg-orange-50',
  implementation: 'bg-red-50',
};

const STAGE_LABELS: Record<string, string> = {
  discovery: 'Discovery',
  prototype: 'Prototype',
  productspecs: 'ProductSpecs',
  solarch: 'Solution Architecture',
  implementation: 'Implementation',
};

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

export default function StagePage() {
  const params = useParams();
  const stage = params.stage as string;

  // Validate stage
  if (!VALID_STAGES.includes(stage)) {
    notFound();
  }

  const [selectedItem, setSelectedItem] = useState<FrameworkItem | null>(null);
  const [expandedNodes, setExpandedNodes] = useState<string[]>([]);

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

  // Combine and filter items by stage
  const allItems = [
    ...(Array.isArray(skills) ? skills : []),
    ...(Array.isArray(commands) ? commands : []),
    ...(Array.isArray(agents) ? agents : []),
  ];

  const stageItems = allItems.filter((item) => item.stage?.toLowerCase() === stage.toLowerCase());
  const treeNodes = transformToTreeNodes(allItems, stage);

  const handleItemSelect = (item: FrameworkItem) => {
    setSelectedItem(item);
  };

  if (isLoading) {
    return (
      <main className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <p>Loading {STAGE_LABELS[stage]} components...</p>
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
      {/* Header with stage theme */}
      <header className={`border-b border-border px-4 py-3 ${STAGE_COLORS[stage]}`}>
        {/* Breadcrumbs */}
        <nav className="mb-2 text-sm" aria-label="Breadcrumb">
          <ol className="flex items-center gap-2">
            <li>
              <a href="/" className="text-accent-default hover:underline">
                Home
              </a>
            </li>
            <li aria-hidden="true">/</li>
            <li>
              <span className="text-gray-600">Stage</span>
            </li>
            <li aria-hidden="true">/</li>
            <li>
              <span className="font-semibold">{STAGE_LABELS[stage]}</span>
            </li>
          </ol>
        </nav>

        <div className="flex-1">
          <h1 className="text-xl font-bold">{STAGE_LABELS[stage]} Components</h1>
          <p className="text-sm text-gray-600 mt-1">
            {stageItems.length} component{stageItems.length === 1 ? '' : 's'}
          </p>
        </div>
      </header>

      {/* Main dual-pane layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Navigation Tree (Sidebar) */}
        <ResizableSidebar
          storageKey="stage-sidebar-width"
          minWidth={240}
          maxWidth={500}
          defaultWidth={320}
        >
          <NavigationTree
            items={treeNodes as any}
            onSelect={(itemId: string) => {
              const item = stageItems.find(i => i.id === itemId);
              if (item) handleItemSelect(item);
            }}
            favorites={[]}
            stageFilter={[stage as Stage]}
          />
        </ResizableSidebar>

        {/* Detail Pane (Main) */}
        <main className="flex-1 overflow-y-auto">
          {stageItems.length === 0 ? (
            <div className="flex items-center justify-center h-full text-gray-500">
              <p>No components found for {STAGE_LABELS[stage]} stage</p>
            </div>
          ) : (
            <DetailPane
              item={selectedItem ? {
                ...selectedItem,
                type: 'skill' as const,
                stage: selectedItem.stage?.toLowerCase() as any,
                isFavorite: false,
              } : null}
            />
          )}
        </main>
      </div>

      {/* Footer */}
      <footer className="border-t border-border px-4 py-2 text-sm text-secondary">
        Version 3.0.0 | Last Updated: 2026-01-31 | © HTEC Framework
      </footer>
    </div>
  );
}
