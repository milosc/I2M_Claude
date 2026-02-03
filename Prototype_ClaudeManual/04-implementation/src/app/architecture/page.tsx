'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { DiagramViewer } from '@/components/DiagramViewer';
import { MarkdownRenderer } from '@/components/MarkdownRenderer';
import { ResizableSidebar } from '@/components/ResizableSidebar';

interface ArchitectureDoc {
  id: string;
  name: string;
  description: string;
  format: 'md' | 'mermaid' | 'plantuml';
  category: 'c4' | 'adr' | 'patterns' | 'infrastructure';
  c4_level?: 'context' | 'container' | 'component' | 'code';
  adr_status?: 'proposed' | 'accepted' | 'deprecated' | 'superseded';
  content: {
    overview?: string;
    diagram?: string;
    decision?: string;
  };
  related_adrs?: string[];
}

async function fetchArchitectureDocs(): Promise<ArchitectureDoc[]> {
  const response = await fetch('/api/architecture-docs');
  if (!response.ok) throw new Error('Failed to load architecture docs');
  return response.json();
}

export default function ArchitectureBrowserPage() {
  const [selectedCategory, setSelectedCategory] = useState<string>('c4');
  const [selectedDoc, setSelectedDoc] = useState<ArchitectureDoc | null>(null);
  const [expandedCategories, setExpandedCategories] = useState<string[]>(['c4', 'adr']);

  const { data: docs, isLoading, error } = useQuery({
    queryKey: ['architecture-docs'],
    queryFn: fetchArchitectureDocs,
  });

  const toggleCategory = (category: string) => {
    setExpandedCategories((prev) =>
      prev.includes(category) ? prev.filter((c) => c !== category) : [...prev, category]
    );
  };

  const categories = {
    c4: docs?.filter((d) => d.category === 'c4') || [],
    adr: docs?.filter((d) => d.category === 'adr') || [],
    patterns: docs?.filter((d) => d.category === 'patterns') || [],
    infrastructure: docs?.filter((d) => d.category === 'infrastructure') || [],
  };

  const currentDoc = selectedDoc || categories[selectedCategory as keyof typeof categories]?.[0];

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <p>Loading architecture documentation...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background text-foreground flex items-center justify-center">
        <p className="text-red-500">Failed to load architecture documentation</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <header className="border-b border-border px-4 py-3">
        <h1 className="text-xl font-bold">Architecture Browser</h1>
      </header>

      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar - Category Tree */}
        <ResizableSidebar
          storageKey="architecture-sidebar-width"
          minWidth={240}
          maxWidth={500}
          defaultWidth={320}
          className="p-4"
        >
          <div className="space-y-2">
            {/* C4 Diagrams */}
            <div>
              <button
                onClick={() => {
                  toggleCategory('c4');
                  setSelectedCategory('c4');
                }}
                className="flex items-center justify-between w-full px-3 py-2 rounded hover:bg-surface-2"
              >
                <span className="font-medium">
                  {expandedCategories.includes('c4') ? '▼' : '▶'} C4 Diagrams
                </span>
                <span className="text-xs text-secondary">({categories.c4.length})</span>
              </button>
              {expandedCategories.includes('c4') && (
                <div className="ml-4 mt-1 space-y-1">
                  {categories.c4.map((doc) => (
                    <button
                      key={doc.id}
                      onClick={() => setSelectedDoc(doc)}
                      className={`block w-full text-left px-3 py-1 rounded text-sm ${
                        currentDoc?.id === doc.id ? 'bg-accent-default text-white' : 'hover:bg-surface-2'
                      }`}
                    >
                      {doc.name}
                      {doc.c4_level && (
                        <span className="ml-2 text-xs opacity-70">[{doc.c4_level}]</span>
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* ADRs */}
            <div>
              <button
                onClick={() => {
                  toggleCategory('adr');
                  setSelectedCategory('adr');
                }}
                className="flex items-center justify-between w-full px-3 py-2 rounded hover:bg-surface-2"
              >
                <span className="font-medium">
                  {expandedCategories.includes('adr') ? '▼' : '▶'} ADRs
                </span>
                <span className="text-xs text-secondary">({categories.adr.length})</span>
              </button>
              {expandedCategories.includes('adr') && (
                <div className="ml-4 mt-1 space-y-1">
                  {categories.adr.map((doc) => (
                    <button
                      key={doc.id}
                      onClick={() => setSelectedDoc(doc)}
                      className={`block w-full text-left px-3 py-1 rounded text-sm ${
                        currentDoc?.id === doc.id ? 'bg-accent-default text-white' : 'hover:bg-surface-2'
                      }`}
                    >
                      {doc.name}
                      {doc.adr_status && (
                        <span
                          className={`ml-2 text-xs px-1 rounded ${
                            doc.adr_status === 'accepted'
                              ? 'bg-green-500 text-white'
                              : doc.adr_status === 'proposed'
                              ? 'bg-yellow-500 text-white'
                              : 'bg-gray-500 text-white'
                          }`}
                        >
                          {doc.adr_status}
                        </span>
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Patterns */}
            <div>
              <button
                onClick={() => {
                  toggleCategory('patterns');
                  setSelectedCategory('patterns');
                }}
                className="flex items-center justify-between w-full px-3 py-2 rounded hover:bg-surface-2"
              >
                <span className="font-medium">
                  {expandedCategories.includes('patterns') ? '▼' : '▶'} Patterns
                </span>
                <span className="text-xs text-secondary">({categories.patterns.length})</span>
              </button>
              {expandedCategories.includes('patterns') && (
                <div className="ml-4 mt-1 space-y-1">
                  {categories.patterns.map((doc) => (
                    <button
                      key={doc.id}
                      onClick={() => setSelectedDoc(doc)}
                      className={`block w-full text-left px-3 py-1 rounded text-sm ${
                        currentDoc?.id === doc.id ? 'bg-accent-default text-white' : 'hover:bg-surface-2'
                      }`}
                    >
                      {doc.name}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Infrastructure */}
            <div>
              <button
                onClick={() => {
                  toggleCategory('infrastructure');
                  setSelectedCategory('infrastructure');
                }}
                className="flex items-center justify-between w-full px-3 py-2 rounded hover:bg-surface-2"
              >
                <span className="font-medium">
                  {expandedCategories.includes('infrastructure') ? '▼' : '▶'} Infrastructure
                </span>
                <span className="text-xs text-secondary">({categories.infrastructure.length})</span>
              </button>
              {expandedCategories.includes('infrastructure') && (
                <div className="ml-4 mt-1 space-y-1">
                  {categories.infrastructure.map((doc) => (
                    <button
                      key={doc.id}
                      onClick={() => setSelectedDoc(doc)}
                      className={`block w-full text-left px-3 py-1 rounded text-sm ${
                        currentDoc?.id === doc.id ? 'bg-accent-default text-white' : 'hover:bg-surface-2'
                      }`}
                    >
                      {doc.name}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </ResizableSidebar>

        {/* Main - Document Viewer */}
        <main className="flex-1 overflow-y-auto p-6">
          {currentDoc ? (
            <div className="space-y-4">
              <div>
                <h2 className="text-2xl font-bold">{currentDoc.name}</h2>
                <p className="text-secondary mt-1">{currentDoc.description}</p>
                <div className="flex gap-2 mt-2">
                  {currentDoc.category && (
                    <span className="inline-block px-2 py-1 text-xs bg-accent-default text-white rounded">
                      {currentDoc.category.toUpperCase()}
                    </span>
                  )}
                  {currentDoc.c4_level && (
                    <span className="inline-block px-2 py-1 text-xs bg-blue-500 text-white rounded">
                      {currentDoc.c4_level}
                    </span>
                  )}
                </div>
              </div>

              {/* Diagram */}
              {currentDoc.content.diagram && (
                <div className="border border-border rounded-lg p-4">
                  <DiagramViewer format={currentDoc.format as 'mermaid' | 'plantuml'} code={currentDoc.content.diagram} />
                </div>
              )}

              {/* Overview */}
              {currentDoc.content.overview && (
                <div className="border border-border rounded-lg p-4">
                  <h3 className="text-lg font-semibold mb-2">Overview</h3>
                  <MarkdownRenderer content={currentDoc.content.overview} />
                </div>
              )}

              {/* Decision (for ADRs) */}
              {currentDoc.content.decision && (
                <div className="border border-border rounded-lg p-4">
                  <h3 className="text-lg font-semibold mb-2">Decision</h3>
                  <MarkdownRenderer content={currentDoc.content.decision} />
                </div>
              )}

              {/* Related ADRs */}
              {currentDoc.related_adrs && currentDoc.related_adrs.length > 0 && (
                <div className="border border-border rounded-lg p-4">
                  <h3 className="text-lg font-semibold mb-2">Related ADRs</h3>
                  <div className="flex gap-2">
                    {currentDoc.related_adrs.map((relatedId) => {
                      const related = docs?.find((d) => d.id === relatedId);
                      return related ? (
                        <button
                          key={relatedId}
                          onClick={() => setSelectedDoc(related)}
                          className="px-3 py-1 border border-border rounded hover:bg-surface-2"
                        >
                          {related.name}
                        </button>
                      ) : null;
                    })}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-secondary">
              Select a document to view
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
