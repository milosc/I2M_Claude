import React, { useState, useEffect } from 'react';
import {
  Tree,
  TreeItem,
  TreeItemContent,
  Badge,
  Tooltip,
  View,
  Button,
  Toolbar,
  Slider,
  Heading,
  Text,
  Link,
  IllustratedMessage,
} from '@adobe/react-spectrum';
import type { Selection } from '@adobe/react-spectrum';

// ═══════════════════════════════════════════════════════════════════
// ASSEMBLY-FIRST: Using Adobe Spectrum React Components
// ═══════════════════════════════════════════════════════════════════
// This screen combines library components with ClaudeManual-specific
// business logic for architecture documentation browsing.
//
// Library Components Used:
// - Tree (category navigation)
// - Badge (C4 level, ADR status, format indicators)
// - Tooltip (category descriptions)
// - View (layout containers)
// - Button (actions)
// - Toolbar (diagram controls)
// - Slider (zoom control)
// - Heading, Text, Link (content display)
// - IllustratedMessage (empty states)
// ═══════════════════════════════════════════════════════════════════

// ───────────────────────────────────────────────────────────────────
// Type Definitions (from DATA_MODEL.md ENT-009)
// ───────────────────────────────────────────────────────────────────

interface ArchitectureDoc {
  id: string;
  name: string;
  description: string;
  format: 'md' | 'mermaid' | 'plantuml';
  path: string;
  category?: 'c4' | 'adr' | 'patterns' | 'infrastructure' | 'data-model';
  c4_level?: 'context' | 'container' | 'component' | 'code';
  adr_status?: 'proposed' | 'accepted' | 'deprecated' | 'superseded';
  tags?: string[];
  related_adrs?: string[];
  content?: {
    overview: string;
    diagram?: string;
    context?: string;
    decision?: string;
    consequences?: string;
    related?: string;
  };
}

interface ArchitectureBrowserState {
  categories: {
    c4: ArchitectureDoc[];
    adrs: ArchitectureDoc[];
    patterns: ArchitectureDoc[];
    infrastructure: ArchitectureDoc[];
  };
  selectedDoc: ArchitectureDoc | null;
  loading: boolean;
  error: string | null;
  zoomLevel: number;
  expandedKeys: Set<string>;
}

// ───────────────────────────────────────────────────────────────────
// Helper Functions
// ───────────────────────────────────────────────────────────────────

function groupByCategory(docs: ArchitectureDoc[]): ArchitectureBrowserState['categories'] {
  return {
    c4: docs.filter(d => d.category === 'c4'),
    adrs: docs.filter(d => d.category === 'adr'),
    patterns: docs.filter(d => d.category === 'patterns'),
    infrastructure: docs.filter(d => d.category === 'infrastructure'),
  };
}

function getBadgeColor(doc: ArchitectureDoc): 'blue' | 'green' | 'red' | 'orange' | 'gray' {
  if (doc.category === 'adr' && doc.adr_status) {
    switch (doc.adr_status) {
      case 'accepted': return 'green';
      case 'deprecated': return 'red';
      case 'proposed': return 'orange';
      default: return 'gray';
    }
  }
  if (doc.category === 'c4') return 'blue';
  return 'gray';
}

function getBadgeLabel(doc: ArchitectureDoc): string {
  if (doc.category === 'c4' && doc.c4_level) {
    return doc.c4_level.toUpperCase();
  }
  if (doc.category === 'adr' && doc.adr_status) {
    return doc.adr_status.toUpperCase();
  }
  return doc.format.toUpperCase();
}

// ───────────────────────────────────────────────────────────────────
// Mock Data (Development)
// ───────────────────────────────────────────────────────────────────

const mockArchitectureDocs: ArchitectureDoc[] = [
  {
    id: 'context-diagram',
    name: 'Context Diagram - ClaudeManual',
    description: 'Shows ClaudeManual system in context with external actors',
    format: 'mermaid',
    path: 'architecture/c4/context-diagram.md',
    category: 'c4',
    c4_level: 'context',
    tags: ['c4', 'system-context'],
    related_adrs: ['ADR-001'],
    content: {
      overview: 'This C4 Context diagram shows the ClaudeManual system in context with external actors and systems.',
      diagram: `graph TD
  A[Framework User] --> B[ClaudeManual System]
  B --> C[File System]
  B --> D[Git Repository]`,
      related: '[Container Diagram](container-diagram), [ADR-001](ADR-001)',
    },
  },
  {
    id: 'container-diagram',
    name: 'Container Diagram - ClaudeManual',
    description: 'Shows high-level containers (web app, API, file system)',
    format: 'mermaid',
    path: 'architecture/c4/container-diagram.md',
    category: 'c4',
    c4_level: 'container',
    tags: ['c4', 'containers'],
    related_adrs: ['ADR-001', 'ADR-002'],
  },
  {
    id: 'ADR-001',
    name: 'Architecture Style',
    description: 'Decision on using component-based architecture with React',
    format: 'md',
    path: 'architecture/adrs/ADR-001-architecture-style.md',
    category: 'adr',
    adr_status: 'accepted',
    tags: ['architecture', 'design'],
    related_adrs: [],
    content: {
      overview: 'ADR for selecting component-based architecture pattern',
      context: 'We needed to choose an architecture style for the ClaudeManual UI.',
      decision: 'Use component-based architecture with React and Adobe Spectrum components.',
      consequences: 'Positive: Rapid development, maintained accessibility. Negative: Learning curve for Spectrum.',
    },
  },
  {
    id: 'ADR-002',
    name: 'Data Storage Strategy',
    description: 'Decision on using file system as primary data source',
    format: 'md',
    path: 'architecture/adrs/ADR-002-data-storage.md',
    category: 'adr',
    adr_status: 'accepted',
    tags: ['data', 'storage'],
    related_adrs: ['ADR-001'],
  },
  {
    id: 'repository-pattern',
    name: 'Repository Pattern',
    description: 'Data access pattern for file system operations',
    format: 'md',
    path: 'architecture/patterns/repository-pattern.md',
    category: 'patterns',
    tags: ['patterns', 'data-access'],
    related_adrs: ['ADR-002'],
  },
];

// ───────────────────────────────────────────────────────────────────
// Main Screen Component
// ───────────────────────────────────────────────────────────────────

export function ArchitectureBrowserScreen() {
  const [state, setState] = useState<ArchitectureBrowserState>({
    categories: { c4: [], adrs: [], patterns: [], infrastructure: [] },
    selectedDoc: null,
    loading: true,
    error: null,
    zoomLevel: 100,
    expandedKeys: new Set(['c4', 'adrs']),
  });

  const [selectedKeys, setSelectedKeys] = useState<Selection>(new Set());

  // ─────────────────────────────────────────────────────────────────
  // Data Fetching (Mock)
  // ─────────────────────────────────────────────────────────────────

  useEffect(() => {
    // Simulate API call: GET /api/architecture-docs
    setTimeout(() => {
      const categories = groupByCategory(mockArchitectureDocs);
      setState(prev => ({
        ...prev,
        categories,
        loading: false,
        selectedDoc: categories.c4[0] || null, // Default to first C4 diagram
      }));
      if (categories.c4.length > 0) {
        setSelectedKeys(new Set([categories.c4[0].id]));
      }
    }, 500);
  }, []);

  // ─────────────────────────────────────────────────────────────────
  // Event Handlers
  // ─────────────────────────────────────────────────────────────────

  const handleSelectionChange = (keys: Selection) => {
    setSelectedKeys(keys);
    if (keys !== 'all' && keys.size > 0) {
      const docId = Array.from(keys)[0] as string;
      const allDocs = [
        ...state.categories.c4,
        ...state.categories.adrs,
        ...state.categories.patterns,
        ...state.categories.infrastructure,
      ];
      const doc = allDocs.find(d => d.id === docId);
      if (doc) {
        setState(prev => ({ ...prev, selectedDoc: doc }));
      }
    }
  };

  const handleZoomChange = (value: number) => {
    setState(prev => ({ ...prev, zoomLevel: value }));
  };

  const handleResetZoom = () => {
    setState(prev => ({ ...prev, zoomLevel: 100 }));
  };

  const handleCopyPath = () => {
    if (state.selectedDoc) {
      navigator.clipboard.writeText(state.selectedDoc.path);
      // TODO: Show toast notification
    }
  };

  const handleExport = () => {
    // TODO: Implement export functionality (PNG/SVG/PDF)
    console.log('Export diagram');
  };

  // ─────────────────────────────────────────────────────────────────
  // Render Helpers
  // ─────────────────────────────────────────────────────────────────

  const renderCategoryTree = () => {
    const { c4, adrs, patterns, infrastructure } = state.categories;

    return (
      <Tree
        aria-label="Architecture categories"
        selectionMode="single"
        selectedKeys={selectedKeys}
        onSelectionChange={handleSelectionChange}
        UNSAFE_className="w-full"
      >
        {c4.length > 0 && (
          <TreeItem key="c4" textValue="C4 Diagrams">
            <TreeItemContent>
              <Text>C4 Diagrams</Text>
              <Badge variant="neutral">{c4.length}</Badge>
            </TreeItemContent>
            {c4.map(doc => (
              <TreeItem key={doc.id} textValue={doc.name}>
                <TreeItemContent>
                  <Text>{doc.name}</Text>
                  <Badge variant={getBadgeColor(doc)}>{getBadgeLabel(doc)}</Badge>
                </TreeItemContent>
              </TreeItem>
            ))}
          </TreeItem>
        )}

        {adrs.length > 0 && (
          <TreeItem key="adrs" textValue="ADRs">
            <TreeItemContent>
              <Text>ADRs</Text>
              <Badge variant="neutral">{adrs.length}</Badge>
            </TreeItemContent>
            {adrs.map(doc => (
              <TreeItem key={doc.id} textValue={doc.name}>
                <TreeItemContent>
                  <Text>{doc.name}</Text>
                  <Badge variant={getBadgeColor(doc)}>{getBadgeLabel(doc)}</Badge>
                </TreeItemContent>
              </TreeItem>
            ))}
          </TreeItem>
        )}

        {patterns.length > 0 && (
          <TreeItem key="patterns" textValue="Patterns">
            <TreeItemContent>
              <Text>Patterns</Text>
              <Badge variant="neutral">{patterns.length}</Badge>
            </TreeItemContent>
            {patterns.map(doc => (
              <TreeItem key={doc.id} textValue={doc.name}>
                <TreeItemContent>
                  <Text>{doc.name}</Text>
                  <Badge variant={getBadgeColor(doc)}>{getBadgeLabel(doc)}</Badge>
                </TreeItemContent>
              </TreeItem>
            ))}
          </TreeItem>
        )}

        {infrastructure.length > 0 && (
          <TreeItem key="infrastructure" textValue="Infrastructure">
            <TreeItemContent>
              <Text>Infrastructure</Text>
              <Badge variant="neutral">{infrastructure.length}</Badge>
            </TreeItemContent>
            {infrastructure.map(doc => (
              <TreeItem key={doc.id} textValue={doc.name}>
                <TreeItemContent>
                  <Text>{doc.name}</Text>
                  <Badge variant={getBadgeColor(doc)}>{getBadgeLabel(doc)}</Badge>
                </TreeItemContent>
              </TreeItem>
            ))}
          </TreeItem>
        )}
      </Tree>
    );
  };

  const renderDocumentViewer = () => {
    const { selectedDoc } = state;

    if (!selectedDoc) {
      return (
        <IllustratedMessage>
          <Heading>No Document Selected</Heading>
          <Text>Select an architecture document from the tree to view details.</Text>
        </IllustratedMessage>
      );
    }

    return (
      <View UNSAFE_className="flex flex-col gap-4 h-full">
        {/* Document Header */}
        <View UNSAFE_className="flex items-center justify-between border-b border-border-default pb-4">
          <View UNSAFE_className="flex items-center gap-2">
            <Heading level={2} UNSAFE_className="text-text-primary">
              {selectedDoc.name}
            </Heading>
            <Badge variant={getBadgeColor(selectedDoc)}>{getBadgeLabel(selectedDoc)}</Badge>
            {selectedDoc.category && (
              <Badge variant="neutral">{selectedDoc.category.toUpperCase()}</Badge>
            )}
            <Badge variant="neutral">{selectedDoc.format.toUpperCase()}</Badge>
          </View>
        </View>

        {/* Diagram Viewer or Markdown Content */}
        {selectedDoc.format === 'mermaid' || selectedDoc.format === 'plantuml' ? (
          <View UNSAFE_className="flex flex-col gap-4 flex-1">
            {/* Diagram Controls Toolbar */}
            <Toolbar aria-label="Diagram controls">
              <Button onPress={handleResetZoom}>Reset Zoom</Button>
              <Button onPress={handleCopyPath}>Copy Path</Button>
              <Button onPress={handleExport}>Export</Button>
              <Slider
                label="Zoom"
                value={state.zoomLevel}
                onChange={handleZoomChange}
                minValue={50}
                maxValue={200}
                step={25}
                UNSAFE_className="w-48"
              />
              <Text>{state.zoomLevel}%</Text>
            </Toolbar>

            {/* Diagram Canvas (Placeholder for Mermaid/PlantUML renderer) */}
            <View UNSAFE_className="flex-1 border border-border-default rounded-md p-4 overflow-auto">
              {selectedDoc.content?.diagram ? (
                <pre
                  className="font-mono text-sm text-text-primary"
                  style={{ transform: `scale(${state.zoomLevel / 100})`, transformOrigin: 'top left' }}
                >
                  {selectedDoc.content.diagram}
                </pre>
              ) : (
                <Text>No diagram content available.</Text>
              )}
            </View>
          </View>
        ) : (
          // Markdown Content Viewer
          <View UNSAFE_className="flex flex-col gap-4 flex-1 overflow-auto">
            {selectedDoc.content?.overview && (
              <View>
                <Heading level={3}>Overview</Heading>
                <Text>{selectedDoc.content.overview}</Text>
              </View>
            )}

            {selectedDoc.content?.context && (
              <View>
                <Heading level={3}>Context</Heading>
                <Text>{selectedDoc.content.context}</Text>
              </View>
            )}

            {selectedDoc.content?.decision && (
              <View>
                <Heading level={3}>Decision</Heading>
                <Text>{selectedDoc.content.decision}</Text>
              </View>
            )}

            {selectedDoc.content?.consequences && (
              <View>
                <Heading level={3}>Consequences</Heading>
                <Text>{selectedDoc.content.consequences}</Text>
              </View>
            )}

            {selectedDoc.content?.related && (
              <View>
                <Heading level={3}>Related</Heading>
                <Text>{selectedDoc.content.related}</Text>
              </View>
            )}
          </View>
        )}

        {/* Document Footer */}
        <View UNSAFE_className="border-t border-border-default pt-4">
          <Text UNSAFE_className="text-text-secondary text-sm">
            <strong>Path:</strong> {selectedDoc.path}
          </Text>
          {selectedDoc.description && (
            <Text UNSAFE_className="text-text-secondary text-sm mt-2">
              {selectedDoc.description}
            </Text>
          )}
        </View>
      </View>
    );
  };

  // ─────────────────────────────────────────────────────────────────
  // Loading & Error States
  // ─────────────────────────────────────────────────────────────────

  if (state.loading) {
    return (
      <View UNSAFE_className="flex items-center justify-center h-screen">
        <IllustratedMessage>
          <Heading>Loading Architecture Documents...</Heading>
        </IllustratedMessage>
      </View>
    );
  }

  if (state.error) {
    return (
      <View UNSAFE_className="flex items-center justify-center h-screen">
        <IllustratedMessage>
          <Heading>Error Loading Documents</Heading>
          <Text>{state.error}</Text>
          <Button onPress={() => window.location.reload()}>Retry</Button>
        </IllustratedMessage>
      </View>
    );
  }

  // ─────────────────────────────────────────────────────────────────
  // Main Layout (Dual-Pane)
  // ─────────────────────────────────────────────────────────────────

  return (
    <View UNSAFE_className="flex h-screen bg-canvas">
      {/* Sidebar: Category Tree */}
      <View UNSAFE_className="w-1/4 border-r border-border-default p-4 overflow-auto">
        <Heading level={2} UNSAFE_className="mb-4">Architecture</Heading>
        {renderCategoryTree()}
      </View>

      {/* Main: Document Viewer */}
      <View UNSAFE_className="flex-1 p-6 overflow-auto">
        {renderDocumentViewer()}
      </View>
    </View>
  );
}
