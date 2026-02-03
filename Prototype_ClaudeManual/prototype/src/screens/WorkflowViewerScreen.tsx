import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  View,
  Heading,
  Text,
  Button,
  Badge,
  Toolbar,
  Slider,
  MenuTrigger,
  Menu,
  MenuItem,
  Switch,
  Link,
} from '@/component-library';
import { DiagramViewer } from '@/components/DiagramViewer';
import { MarkdownRenderer } from '@/components/MarkdownRenderer';
import { useFetch } from '@/hooks/useFetch';
import { useUserPreferences } from '@/hooks/useUserPreferences';
import type { Workflow } from '@/types/data-model';

interface DiagramState {
  zoom: number;
  pan: { x: number; y: number };
  minimapEnabled: boolean;
  exportInProgress: boolean;
}

export function WorkflowViewerScreen() {
  const { workflowId } = useParams<{ workflowId: string }>();
  const navigate = useNavigate();

  // Data fetching
  const {
    data: workflow,
    loading,
    error,
  } = useFetch<Workflow>(`/api/workflows/${workflowId}`);

  const { data: relatedData } = useFetch<{ data: Workflow[] }>(
    `/api/workflows?related=${workflowId}`
  );

  // User preferences
  const { preferences, toggleFavorite } = useUserPreferences();
  const isFavorited = preferences.favorites.includes(workflowId || '');

  // Diagram state
  const [diagramState, setDiagramState] = useState<DiagramState>(() => {
    const stored = localStorage.getItem(`workflow-view-${workflowId}`);
    return stored
      ? JSON.parse(stored)
      : {
          zoom: 100,
          pan: { x: 0, y: 0 },
          minimapEnabled: false,
          exportInProgress: false,
        };
  });

  const diagramRef = useRef<SVGElement | null>(null);

  // Save diagram state to localStorage
  useEffect(() => {
    if (workflowId) {
      localStorage.setItem(
        `workflow-view-${workflowId}`,
        JSON.stringify({
          zoom: diagramState.zoom,
          pan: diagramState.pan,
          minimapEnabled: diagramState.minimapEnabled,
        })
      );
    }
  }, [workflowId, diagramState.zoom, diagramState.pan, diagramState.minimapEnabled]);

  // Handlers
  const handleZoomIn = () => {
    setDiagramState((prev) => ({
      ...prev,
      zoom: Math.min(prev.zoom + 25, 200),
    }));
  };

  const handleZoomOut = () => {
    setDiagramState((prev) => ({
      ...prev,
      zoom: Math.max(prev.zoom - 25, 25),
    }));
  };

  const handleZoomChange = (value: number) => {
    setDiagramState((prev) => ({ ...prev, zoom: value }));
  };

  const handleReset = () => {
    setDiagramState((prev) => ({
      ...prev,
      zoom: 100,
      pan: { x: 0, y: 0 },
    }));
  };

  const handlePanChange = (pan: { x: number; y: number }) => {
    setDiagramState((prev) => ({ ...prev, pan }));
  };

  const handleMinimapToggle = (enabled: boolean) => {
    setDiagramState((prev) => ({ ...prev, minimapEnabled: enabled }));
  };

  const handleExport = async (format: 'png' | 'svg' | 'pdf') => {
    if (!diagramRef.current || !workflow) return;

    setDiagramState((prev) => ({ ...prev, exportInProgress: true }));

    try {
      let blob: Blob;

      if (format === 'png') {
        blob = await exportAsPNG(diagramRef.current);
      } else if (format === 'svg') {
        blob = exportAsSVG(diagramRef.current);
      } else {
        blob = await exportAsPDF(diagramRef.current, workflow.name);
      }

      // Download
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${workflow.id}.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Export failed:', error);
      // TODO: Show toast notification
    } finally {
      setDiagramState((prev) => ({ ...prev, exportInProgress: false }));
    }
  };

  const handleFavoriteToggle = () => {
    if (workflowId) {
      toggleFavorite(workflowId);
    }
  };

  const handleBack = () => {
    navigate('/');
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === '+' || event.key === '=') {
        handleZoomIn();
      } else if (event.key === '-' || event.key === '_') {
        handleZoomOut();
      } else if (event.key === '0') {
        handleReset();
      } else if (event.key === 'Escape') {
        handleBack();
      } else if (event.key === 'f' || event.key === 'F') {
        // TODO: Navigate to Document Preview Modal (SCR-011)
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Loading state
  if (loading) {
    return (
      <View className="flex items-center justify-center min-h-screen bg-canvas">
        <Text>Loading workflow...</Text>
      </View>
    );
  }

  // Error state
  if (error || !workflow) {
    return (
      <View className="flex flex-col items-center justify-center min-h-screen bg-canvas p-8">
        <Heading level={2} className="text-text-primary mb-4">
          Workflow Not Found
        </Heading>
        <Text className="text-text-secondary mb-6">
          {error || `The workflow "${workflowId}" could not be found.`}
        </Text>
        <Button onPress={handleBack} variant="primary">
          Back to Explorer
        </Button>
      </View>
    );
  }

  return (
    <View className="flex flex-col h-screen bg-canvas">
      {/* Header Toolbar */}
      <View className="flex items-center justify-between px-6 py-4 border-b border-border-default bg-surface-1">
        <View className="flex items-center gap-4">
          <Button
            onPress={handleBack}
            variant="secondary"
            className="flex items-center gap-2"
          >
            ← Back to Explorer
          </Button>

          <View className="flex flex-col">
            <Heading level={3} className="text-text-primary">
              Workflow: {workflow.name}
            </Heading>
            <View className="flex items-center gap-2 mt-1">
              <Badge variant="neutral">{workflow.format.toUpperCase()}</Badge>
              {workflow.stage && (
                <Badge variant="info" className={`bg-stage-${workflow.stage.toLowerCase()}`}>
                  {workflow.stage}
                </Badge>
              )}
            </View>
          </View>
        </View>

        <Button
          onPress={handleFavoriteToggle}
          variant="action"
          className={isFavorited ? 'text-accent-default' : 'text-text-secondary'}
          aria-label={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
        >
          {isFavorited ? '★' : '☆'}
        </Button>
      </View>

      {/* Diagram Canvas */}
      <View className="flex-1 relative overflow-hidden">
        <DiagramViewer
          ref={diagramRef}
          format={workflow.format as 'mermaid' | 'plantuml'}
          content={workflow.content?.diagram || ''}
          zoom={diagramState.zoom}
          pan={diagramState.pan}
          minimapEnabled={diagramState.minimapEnabled}
          onPanChange={handlePanChange}
          theme={preferences.theme === 'dark' ? 'dark' : 'light'}
        />

        {/* Floating Controls */}
        <Toolbar
          orientation="horizontal"
          className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-surface-1 border border-border-default rounded-md shadow-lg p-2 flex items-center gap-4"
        >
          <Button
            onPress={handleZoomOut}
            variant="secondary"
            isDisabled={diagramState.zoom <= 25}
            aria-label="Zoom out"
          >
            −
          </Button>

          <Slider
            value={diagramState.zoom}
            onChange={handleZoomChange}
            minValue={25}
            maxValue={200}
            step={25}
            className="w-32"
            aria-label="Zoom level"
          />

          <Text className="text-text-secondary text-sm min-w-[3rem] text-center">
            {diagramState.zoom}%
          </Text>

          <Button
            onPress={handleZoomIn}
            variant="secondary"
            isDisabled={diagramState.zoom >= 200}
            aria-label="Zoom in"
          >
            +
          </Button>

          <Button onPress={handleReset} variant="secondary">
            Reset
          </Button>

          <MenuTrigger>
            <Button variant="secondary" isDisabled={diagramState.exportInProgress}>
              {diagramState.exportInProgress ? 'Exporting...' : 'Export ▾'}
            </Button>
            <Menu onAction={(key) => handleExport(key as 'png' | 'svg' | 'pdf')}>
              <MenuItem key="png">Export as PNG</MenuItem>
              <MenuItem key="svg">Export as SVG</MenuItem>
              <MenuItem key="pdf">Export as PDF</MenuItem>
            </Menu>
          </MenuTrigger>

          <Switch
            isSelected={diagramState.minimapEnabled}
            onChange={handleMinimapToggle}
            aria-label="Toggle minimap"
          >
            Minimap
          </Switch>
        </Toolbar>
      </View>

      {/* Description Section */}
      {workflow.content?.overview && (
        <View className="px-6 py-4 border-t border-border-default bg-surface-1">
          <Heading level={4} className="text-text-primary mb-2">
            Description
          </Heading>
          <MarkdownRenderer content={workflow.content.overview} />
        </View>
      )}

      {/* Related Workflows */}
      {relatedData?.data && relatedData.data.length > 0 && (
        <View className="px-6 py-4 border-t border-border-default bg-surface-1">
          <Heading level={4} className="text-text-primary mb-2">
            Related Workflows
          </Heading>
          <View className="flex gap-3">
            {relatedData.data.map((related) => (
              <Link
                key={related.id}
                href={`/workflows/${related.id}`}
                variant="secondary"
                className="text-accent-default hover:underline"
              >
                {related.name}
              </Link>
            ))}
          </View>
        </View>
      )}
    </View>
  );
}

// Export helpers
function exportAsSVG(svgElement: SVGElement): Blob {
  const svgData = new XMLSerializer().serializeToString(svgElement);
  return new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
}

async function exportAsPNG(svgElement: SVGElement): Promise<Blob> {
  return new Promise((resolve, reject) => {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    if (!ctx) {
      reject(new Error('Could not get canvas context'));
      return;
    }

    const svgData = new XMLSerializer().serializeToString(svgElement);
    const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(svgBlob);

    const img = new Image();
    img.onload = () => {
      canvas.width = img.width * 2; // 2x for retina
      canvas.height = img.height * 2;
      ctx.scale(2, 2);
      ctx.drawImage(img, 0, 0);
      URL.revokeObjectURL(url);

      canvas.toBlob((blob) => {
        if (blob) {
          resolve(blob);
        } else {
          reject(new Error('Failed to create PNG blob'));
        }
      }, 'image/png');
    };

    img.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error('Failed to load SVG as image'));
    };

    img.src = url;
  });
}

async function exportAsPDF(svgElement: SVGElement, workflowName: string): Promise<Blob> {
  // Dynamic import to reduce bundle size
  const { jsPDF } = await import('jspdf');

  const pdf = new jsPDF({
    orientation: 'landscape',
    unit: 'px',
    format: 'a4',
  });

  // Add header
  pdf.setFontSize(16);
  pdf.text(workflowName, 20, 20);

  // Add SVG (simplified - jsPDF SVG support may require plugin)
  // For production, use svg2pdf.js or convert to canvas first
  const svgData = new XMLSerializer().serializeToString(svgElement);
  pdf.text('Diagram:', 20, 40);
  pdf.setFontSize(10);
  pdf.text('(SVG rendering requires additional setup)', 20, 55);

  return pdf.output('blob');
}
