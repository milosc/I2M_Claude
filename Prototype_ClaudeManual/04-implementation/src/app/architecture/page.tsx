'use client';

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { MarkdownRenderer } from '@/components/MarkdownRenderer';
import { ResizableSidebar } from '@/components/ResizableSidebar';

interface ArchitectureFile {
  id: string;
  name: string;
  path: string;
  type: 'file' | 'folder';
  category: string;
  children?: ArchitectureFile[];
}

interface ArchitectureHierarchy {
  architecturePath: string;
  defaultPath: string;
  items: ArchitectureFile[];
}

interface ArchitectureContent {
  id: string;
  name: string;
  path: string;
  content: string;
  category: string;
}

// Category color mapping
const categoryColors: Record<string, string> = {
  'Claude Code': 'bg-blue-500',
  'Workflows': 'bg-purple-500',
  'Hooks': 'bg-green-500',
  'LSP': 'bg-orange-500',
  'Traceability': 'bg-red-500',
  'To Be Solved': 'bg-yellow-500',
};

async function fetchArchitectureHierarchy(architecturePath?: string): Promise<ArchitectureHierarchy> {
  const url = architecturePath
    ? `/api/architecture?architecturePath=${encodeURIComponent(architecturePath)}`
    : '/api/architecture';
  const response = await fetch(url);
  if (!response.ok) throw new Error('Failed to load architecture');
  return response.json();
}

async function fetchArchitectureContent(filePath: string): Promise<ArchitectureContent> {
  const response = await fetch(`/api/architecture?file=${encodeURIComponent(filePath)}`);
  if (!response.ok) throw new Error('Failed to load file content');
  return response.json();
}

// Recursive tree component
function ArchitectureTree({
  items,
  expandedFolders,
  onToggleFolder,
  onSelectFile,
  selectedFilePath,
  level = 0,
}: {
  items: ArchitectureFile[];
  expandedFolders: Set<string>;
  onToggleFolder: (path: string) => void;
  onSelectFile: (item: ArchitectureFile) => void;
  selectedFilePath: string | null;
  level?: number;
}) {
  return (
    <ul className={`space-y-1 ${level > 0 ? 'ml-4 border-l border-border pl-2' : ''}`}>
      {items.map((item) => (
        <li key={item.id}>
          {item.type === 'folder' ? (
            <div>
              <button
                onClick={() => onToggleFolder(item.path)}
                className="flex items-center gap-2 w-full text-left px-2 py-1.5 rounded hover:bg-surface-2"
              >
                <span className="text-sm">
                  {expandedFolders.has(item.path) ? '📂' : '📁'}
                </span>
                <span className="font-medium">{item.name}</span>
                {item.category && categoryColors[item.category] && (
                  <span
                    className={`text-xs px-1.5 py-0.5 rounded text-white ${categoryColors[item.category]}`}
                  >
                    {item.category}
                  </span>
                )}
              </button>
              {expandedFolders.has(item.path) && item.children && (
                <ArchitectureTree
                  items={item.children}
                  expandedFolders={expandedFolders}
                  onToggleFolder={onToggleFolder}
                  onSelectFile={onSelectFile}
                  selectedFilePath={selectedFilePath}
                  level={level + 1}
                />
              )}
            </div>
          ) : (
            <button
              onClick={() => onSelectFile(item)}
              className={`flex items-center gap-2 w-full text-left px-2 py-1.5 rounded hover:bg-surface-2 ${
                selectedFilePath === item.path ? 'bg-accent-default/10 border-l-2 border-accent-default' : ''
              }`}
            >
              <span className="text-sm">📄</span>
              <span className="text-sm truncate">{item.name}</span>
            </button>
          )}
        </li>
      ))}
    </ul>
  );
}

export default function ArchitectureViewerPage() {
  const [selectedFile, setSelectedFile] = useState<ArchitectureFile | null>(null);
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());
  const [architecturePath, setArchitecturePath] = useState<string>('.claude/architecture');

  // Load architecture path from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('user_preferences');
    if (saved) {
      const prefs = JSON.parse(saved);
      if (prefs.architecturePath) {
        setArchitecturePath(prefs.architecturePath);
      }
    }
  }, []);

  // Fetch architecture hierarchy
  const {
    data: hierarchy,
    isLoading: hierarchyLoading,
    error: hierarchyError,
  } = useQuery({
    queryKey: ['architecture-hierarchy', architecturePath],
    queryFn: () => fetchArchitectureHierarchy(architecturePath),
  });

  // Fetch selected file content
  const {
    data: fileContent,
    isLoading: contentLoading,
    error: contentError,
  } = useQuery({
    queryKey: ['architecture-content', selectedFile?.path],
    queryFn: () => fetchArchitectureContent(selectedFile!.path),
    enabled: !!selectedFile,
  });

  const handleToggleFolder = (path: string) => {
    setExpandedFolders((prev) => {
      const next = new Set(prev);
      if (next.has(path)) {
        next.delete(path);
      } else {
        next.add(path);
      }
      return next;
    });
  };

  const handleSelectFile = (item: ArchitectureFile) => {
    setSelectedFile(item);
  };

  // Expand all folders by default on first load
  useEffect(() => {
    if (hierarchy?.items && expandedFolders.size === 0) {
      const allFolderPaths = new Set<string>();
      const collectFolders = (items: ArchitectureFile[]) => {
        for (const item of items) {
          if (item.type === 'folder') {
            allFolderPaths.add(item.path);
            if (item.children) {
              collectFolders(item.children);
            }
          }
        }
      };
      collectFolders(hierarchy.items);
      setExpandedFolders(allFolderPaths);
    }
  }, [hierarchy]);

  if (hierarchyLoading) {
    return (
      <div className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <p>Loading architecture...</p>
      </div>
    );
  }

  if (hierarchyError) {
    return (
      <div className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-2">Failed to load architecture</p>
          <p className="text-sm text-secondary">
            Make sure the architecture path is correct in Settings
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-background text-foreground flex flex-col" style={{ height: 'calc(100vh - 52px)' }}>
      <header className="flex-shrink-0 border-b border-border px-4 py-3">
        <h1 className="text-xl font-bold">Architecture Documentation</h1>
        <p className="text-sm text-secondary">
          Path: {hierarchy?.architecturePath || architecturePath}
        </p>
      </header>

      <div className="flex flex-1 min-h-0">
        {/* Sidebar - File Tree */}
        <ResizableSidebar
          storageKey="architecture-sidebar-width"
          minWidth={240}
          maxWidth={500}
          defaultWidth={320}
          className="p-3"
        >
          <h2 className="flex-shrink-0 text-sm font-semibold text-secondary mb-3 uppercase tracking-wide">
            Architecture Files
          </h2>
          {hierarchy?.items && hierarchy.items.length > 0 ? (
            <ArchitectureTree
              items={hierarchy.items}
              expandedFolders={expandedFolders}
              onToggleFolder={handleToggleFolder}
              onSelectFile={handleSelectFile}
              selectedFilePath={selectedFile?.path || null}
            />
          ) : (
            <p className="text-sm text-secondary">No architecture files found</p>
          )}
        </ResizableSidebar>

        {/* Main Content - File Viewer */}
        <main
          className="flex-1 overflow-y-auto p-6"
          style={{ overscrollBehavior: 'contain' }}
        >
          {selectedFile ? (
            <div>
              <div className="flex items-center gap-3 mb-4">
                <h2 className="text-lg font-semibold">{selectedFile.name}</h2>
                {selectedFile.category && categoryColors[selectedFile.category] && (
                  <span
                    className={`text-xs px-2 py-1 rounded text-white ${categoryColors[selectedFile.category]}`}
                  >
                    {selectedFile.category}
                  </span>
                )}
              </div>
              <p className="text-sm text-secondary mb-4">
                {selectedFile.path}
              </p>

              {contentLoading && (
                <div className="border border-border rounded-lg p-8 text-center">
                  <p>Loading content...</p>
                </div>
              )}

              {contentError && (
                <div className="border border-red-300 bg-red-50 rounded-lg p-4">
                  <p className="text-red-600">Failed to load file content</p>
                </div>
              )}

              {fileContent && (
                <div className="border border-border rounded-lg p-6 bg-surface-1">
                  <MarkdownRenderer content={fileContent.content} />
                </div>
              )}
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-center">
              <div>
                <p className="text-lg text-secondary mb-2">
                  Select an architecture file to view
                </p>
                <p className="text-sm text-secondary">
                  Choose a markdown file from the sidebar to see its contents
                </p>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
