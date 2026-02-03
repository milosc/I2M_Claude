'use client';

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { MarkdownRenderer } from '@/components/MarkdownRenderer';
import { ResizableSidebar } from '@/components/ResizableSidebar';

interface WorkflowFile {
  id: string;
  name: string;
  path: string;
  type: 'file' | 'folder';
  stage: string;
  children?: WorkflowFile[];
}

interface WorkflowHierarchy {
  workflowPath: string;
  defaultPath: string;
  items: WorkflowFile[];
}

interface WorkflowContent {
  id: string;
  name: string;
  path: string;
  content: string;
  stage: string;
}

// Stage color mapping
const stageColors: Record<string, string> = {
  Discovery: 'bg-blue-500',
  Prototype: 'bg-purple-500',
  ProductSpecs: 'bg-green-500',
  SolArch: 'bg-orange-500',
  Implementation: 'bg-red-500',
  ChangeManagement: 'bg-gray-500',
};

async function fetchWorkflowHierarchy(workflowPath?: string): Promise<WorkflowHierarchy> {
  const url = workflowPath
    ? `/api/workflows?workflowPath=${encodeURIComponent(workflowPath)}`
    : '/api/workflows';
  const response = await fetch(url);
  if (!response.ok) throw new Error('Failed to load workflows');
  return response.json();
}

async function fetchWorkflowContent(filePath: string): Promise<WorkflowContent> {
  const response = await fetch(`/api/workflows?file=${encodeURIComponent(filePath)}`);
  if (!response.ok) throw new Error('Failed to load file content');
  return response.json();
}

// Recursive tree component
function WorkflowTree({
  items,
  expandedFolders,
  onToggleFolder,
  onSelectFile,
  selectedFilePath,
  level = 0,
}: {
  items: WorkflowFile[];
  expandedFolders: Set<string>;
  onToggleFolder: (path: string) => void;
  onSelectFile: (item: WorkflowFile) => void;
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
                <span
                  className={`text-xs px-1.5 py-0.5 rounded text-white ${stageColors[item.stage] || 'bg-gray-400'}`}
                >
                  {item.stage}
                </span>
              </button>
              {expandedFolders.has(item.path) && item.children && (
                <WorkflowTree
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

export default function WorkflowViewerPage() {
  const [selectedFile, setSelectedFile] = useState<WorkflowFile | null>(null);
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());
  const [workflowPath, setWorkflowPath] = useState<string>('.claude/architecture/Workflows');

  // Load workflow path from localStorage
  useEffect(() => {
    const saved = localStorage.getItem('user_preferences');
    if (saved) {
      const prefs = JSON.parse(saved);
      if (prefs.workflowPath) {
        setWorkflowPath(prefs.workflowPath);
      }
    }
  }, []);

  // Fetch workflow hierarchy
  const {
    data: hierarchy,
    isLoading: hierarchyLoading,
    error: hierarchyError,
  } = useQuery({
    queryKey: ['workflow-hierarchy', workflowPath],
    queryFn: () => fetchWorkflowHierarchy(workflowPath),
  });

  // Fetch selected file content
  const {
    data: fileContent,
    isLoading: contentLoading,
    error: contentError,
  } = useQuery({
    queryKey: ['workflow-content', selectedFile?.path],
    queryFn: () => fetchWorkflowContent(selectedFile!.path),
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

  const handleSelectFile = (item: WorkflowFile) => {
    setSelectedFile(item);
  };

  // Expand all folders by default on first load
  useEffect(() => {
    if (hierarchy?.items && expandedFolders.size === 0) {
      const allFolderPaths = new Set<string>();
      const collectFolders = (items: WorkflowFile[]) => {
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
        <p>Loading workflows...</p>
      </div>
    );
  }

  if (hierarchyError) {
    return (
      <div className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-2">Failed to load workflows</p>
          <p className="text-sm text-secondary">
            Make sure the workflow path is correct in Settings
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <header className="border-b border-border px-4 py-3">
        <h1 className="text-xl font-bold">Workflow Documentation</h1>
        <p className="text-sm text-secondary">
          Path: {hierarchy?.workflowPath || workflowPath}
        </p>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar - File Tree */}
        <ResizableSidebar
          storageKey="workflow-sidebar-width"
          minWidth={240}
          maxWidth={500}
          defaultWidth={320}
          className="p-3"
        >
          <h2 className="text-sm font-semibold text-secondary mb-3 uppercase tracking-wide">
            Workflow Files
          </h2>
          {hierarchy?.items && hierarchy.items.length > 0 ? (
            <WorkflowTree
              items={hierarchy.items}
              expandedFolders={expandedFolders}
              onToggleFolder={handleToggleFolder}
              onSelectFile={handleSelectFile}
              selectedFilePath={selectedFile?.path || null}
            />
          ) : (
            <p className="text-sm text-secondary">No workflow files found</p>
          )}
        </ResizableSidebar>

        {/* Main Content - File Viewer */}
        <main className="flex-1 overflow-y-auto p-6">
          {selectedFile ? (
            <div>
              <div className="flex items-center gap-3 mb-4">
                <h2 className="text-lg font-semibold">{selectedFile.name}</h2>
                <span
                  className={`text-xs px-2 py-1 rounded text-white ${stageColors[selectedFile.stage] || 'bg-gray-400'}`}
                >
                  {selectedFile.stage}
                </span>
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
                  Select a workflow file to view
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
