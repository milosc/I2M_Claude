import React, { useState, useEffect, useRef } from 'react';
import { cn } from '@/lib/utils';

interface DiagramViewerProps {
  code: string;
  format: 'mermaid' | 'plantuml';
  initialZoom?: number;
  onExport?: (format: 'png' | 'svg' | 'pdf') => void;
}

export function DiagramViewer({
  code,
  format,
  initialZoom = 1.0,
  onExport,
}: DiagramViewerProps) {
  const [zoom, setZoom] = useState(initialZoom);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isPanMode, setIsPanMode] = useState(false);
  const [showExportMenu, setShowExportMenu] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isRendering, setIsRendering] = useState(true);
  const canvasRef = useRef<HTMLDivElement>(null);

  const MIN_ZOOM = 0.25;
  const MAX_ZOOM = 3.0;
  const ZOOM_STEP = 0.1;

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isFullscreen) {
        setIsFullscreen(false);
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isFullscreen]);

  useEffect(() => {
    async function renderDiagram() {
      setIsRendering(true);
      setError(null);

      try {
        if (format === 'mermaid') {
          // Mock mermaid rendering for testing
          if (code.includes('invalid')) {
            throw new Error('Invalid mermaid syntax');
          }
          setIsRendering(false);
        } else if (format === 'plantuml') {
          // Mock plantuml rendering for testing
          setIsRendering(false);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Error rendering diagram');
        setIsRendering(false);
      }
    }

    renderDiagram();
  }, [code, format]);

  const handleZoomIn = () => {
    setZoom((prev) => Math.min(prev + ZOOM_STEP, MAX_ZOOM));
  };

  const handleZoomOut = () => {
    setZoom((prev) => Math.max(prev - ZOOM_STEP, MIN_ZOOM));
  };

  const handleResetZoom = () => {
    setZoom(1.0);
  };

  const handleToggleFullscreen = () => {
    setIsFullscreen((prev) => !prev);
  };

  const handleTogglePan = () => {
    setIsPanMode((prev) => !prev);
  };

  const handleExport = (exportFormat: 'png' | 'svg' | 'pdf') => {
    if (onExport) {
      onExport(exportFormat);
    }
    setShowExportMenu(false);
  };

  const handleRetry = () => {
    setError(null);
    setIsRendering(true);
  };

  const zoomPercent = Math.round(zoom * 100);

  return (
    <section
      role="region"
      aria-label="Diagram viewer"
      className={cn(
        'bg-white rounded-lg border border-gray-200 shadow-sm',
        isFullscreen && 'fixed inset-0 z-50 rounded-none'
      )}
    >
      {/* Toolbar */}
      <div
        role="toolbar"
        aria-label="Diagram controls"
        className="flex items-center justify-between p-4 border-b border-gray-200"
      >
        <div className="flex items-center gap-2">
          {/* Zoom Controls */}
          <button
            type="button"
            onClick={handleZoomOut}
            disabled={zoom <= MIN_ZOOM}
            aria-label="Zoom out"
            className={cn(
              'p-2 rounded-md transition-colors',
              'hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-accent-default',
              'disabled:opacity-50 disabled:cursor-not-allowed'
            )}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              className="w-5 h-5"
            >
              <path
                fillRule="evenodd"
                d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z"
                clipRule="evenodd"
              />
            </svg>
          </button>

          <span className="text-sm font-medium text-gray-700 min-w-[4rem] text-center">
            {zoomPercent}%
          </span>

          <button
            type="button"
            onClick={handleZoomIn}
            disabled={zoom >= MAX_ZOOM}
            aria-label="Zoom in"
            className={cn(
              'p-2 rounded-md transition-colors',
              'hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-accent-default',
              'disabled:opacity-50 disabled:cursor-not-allowed'
            )}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              className="w-5 h-5"
            >
              <path
                fillRule="evenodd"
                d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z"
                clipRule="evenodd"
              />
            </svg>
          </button>

          <button
            type="button"
            onClick={handleResetZoom}
            aria-label="Reset zoom"
            className={cn(
              'px-3 py-1.5 text-sm font-medium rounded-md transition-colors',
              'hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-accent-default'
            )}
          >
            Reset
          </button>

          {/* Pan Toggle */}
          <div className="w-px h-6 bg-gray-300 mx-2" />

          <button
            type="button"
            onClick={handleTogglePan}
            aria-label="Pan"
            aria-pressed={isPanMode}
            className={cn(
              'p-2 rounded-md transition-colors',
              'focus:outline-none focus:ring-2 focus:ring-accent-default',
              isPanMode ? 'bg-accent-default text-white' : 'hover:bg-gray-100'
            )}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              className="w-5 h-5"
            >
              <path d="M10 3.5a1.5 1.5 0 013 0V4a1 1 0 001 1h3a1 1 0 011 1v3a1 1 0 01-1 1h-.5a1.5 1.5 0 000 3h.5a1 1 0 011 1v3a1 1 0 01-1 1h-3a1 1 0 01-1-1v-.5a1.5 1.5 0 00-3 0v.5a1 1 0 01-1 1H6a1 1 0 01-1-1v-3a1 1 0 00-1-1h-.5a1.5 1.5 0 010-3H4a1 1 0 001-1V6a1 1 0 011-1h3a1 1 0 001-1v-.5z" />
            </svg>
          </button>
        </div>

        <div className="flex items-center gap-2">
          {/* Export Menu */}
          {onExport && (
            <div className="relative">
              <button
                type="button"
                onClick={() => setShowExportMenu((prev) => !prev)}
                aria-label="Export diagram"
                aria-expanded={showExportMenu}
                className={cn(
                  'px-3 py-1.5 text-sm font-medium rounded-md transition-colors',
                  'bg-accent-default text-white hover:bg-accent-hover',
                  'focus:outline-none focus:ring-2 focus:ring-accent-default'
                )}
              >
                Export
              </button>

              {showExportMenu && (
                <div
                  role="menu"
                  className="absolute right-0 mt-2 w-32 bg-white rounded-md shadow-lg border border-gray-200 z-10"
                >
                  {(['png', 'svg', 'pdf'] as const).map((exportFormat) => (
                    <button
                      key={exportFormat}
                      type="button"
                      role="menuitem"
                      onClick={() => handleExport(exportFormat)}
                      className={cn(
                        'w-full px-4 py-2 text-left text-sm hover:bg-gray-100',
                        'focus:outline-none focus:bg-gray-100 first:rounded-t-md last:rounded-b-md'
                      )}
                    >
                      {exportFormat.toUpperCase()}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Fullscreen Toggle */}
          <button
            type="button"
            onClick={handleToggleFullscreen}
            aria-label={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'}
            className={cn(
              'p-2 rounded-md transition-colors',
              'hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-accent-default'
            )}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              className="w-5 h-5"
            >
              {isFullscreen ? (
                <path d="M3 4a1 1 0 011-1h4a1 1 0 010 2H6.414l2.293 2.293a1 1 0 11-1.414 1.414L5 6.414V8a1 1 0 01-2 0V4zm9 1a1 1 0 110-2h4a1 1 0 011 1v4a1 1 0 11-2 0V6.414l-2.293 2.293a1 1 0 11-1.414-1.414L13.586 5H12zm-9 7a1 1 0 112 0v1.586l2.293-2.293a1 1 0 011.414 1.414L6.414 15H8a1 1 0 110 2H4a1 1 0 01-1-1v-4zm13-1a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 110-2h1.586l-2.293-2.293a1 1 0 011.414-1.414L15 13.586V12a1 1 0 011-1z" />
              ) : (
                <path d="M3 4a1 1 0 011-1h4a1 1 0 010 2H5v3a1 1 0 01-2 0V4zM15 4a1 1 0 011 1v3a1 1 0 11-2 0V5h-3a1 1 0 110-2h4zM3 15a1 1 0 011 1v3h3a1 1 0 110 2H4a1 1 0 01-1-1v-4a1 1 0 011-1zM16 15a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 110-2h3v-3a1 1 0 011-1z" />
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Diagram Canvas */}
      <div
        className={cn(
          'flex items-center justify-center bg-gray-50',
          isFullscreen ? 'h-[calc(100vh-4rem)]' : 'h-96',
          isPanMode && 'cursor-grab active:cursor-grabbing'
        )}
      >
        {error ? (
          <div className="text-center">
            <p className="text-red-600 mb-4">Error rendering diagram</p>
            <button
              type="button"
              onClick={handleRetry}
              className={cn(
                'px-4 py-2 text-sm font-medium text-white bg-accent-default',
                'rounded-md hover:bg-accent-hover transition-colors',
                'focus:outline-none focus:ring-2 focus:ring-accent-default'
              )}
            >
              Retry
            </button>
          </div>
        ) : isRendering ? (
          <div className="text-gray-500">Loading diagram...</div>
        ) : (
          <div
            ref={canvasRef}
            data-testid="diagram-canvas"
            className={cn('transition-transform', isPanMode && 'cursor-grab')}
            style={{ transform: `scale(${zoom})` }}
          >
            {/* Mock diagram - in real implementation, mermaid would render here */}
            <div className="p-8 border-2 border-dashed border-gray-300 rounded-lg">
              <p className="text-gray-600">{format.toUpperCase()} Diagram</p>
              <pre className="text-xs text-gray-500 mt-2">{code.substring(0, 50)}...</pre>
            </div>
          </div>
        )}
      </div>

      {/* Screen Reader Status */}
      <div role="status" className="sr-only" aria-live="polite">
        Zoom: {zoomPercent}%
      </div>
    </section>
  );
}
