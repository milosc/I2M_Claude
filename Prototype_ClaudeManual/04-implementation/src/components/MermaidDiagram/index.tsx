'use client';

import React, { useEffect, useRef, useState } from 'react';

export interface MermaidDiagramProps {
  /** Mermaid diagram code */
  code: string;
  /** Theme variant */
  theme?: 'light' | 'dark';
}

// Flag to track if mermaid has been initialized
let mermaidInitialized = false;

export const MermaidDiagram: React.FC<MermaidDiagramProps> = ({
  code,
  theme = 'light',
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [svg, setSvg] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const renderDiagram = async () => {
      if (!code.trim()) {
        setError('No diagram code provided');
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        setError(null);

        // Dynamically import mermaid only when needed
        const mermaid = (await import('mermaid')).default;

        // Initialize mermaid only once
        if (!mermaidInitialized) {
          mermaid.initialize({
            startOnLoad: false,
            theme: theme === 'dark' ? 'dark' : 'default',
            securityLevel: 'loose',
            fontFamily: 'system-ui, -apple-system, sans-serif',
            suppressErrorRendering: true,
          });
          mermaidInitialized = true;
        }

        // Generate unique ID for this diagram
        const id = `mermaid-${Math.random().toString(36).substring(2, 11)}`;

        // Render the diagram
        const { svg: renderedSvg } = await mermaid.render(id, code.trim());
        setSvg(renderedSvg);
      } catch (err) {
        console.error('Mermaid rendering error:', err);
        setError(err instanceof Error ? err.message : 'Failed to render diagram');
      } finally {
        setIsLoading(false);
      }
    };

    renderDiagram();
  }, [code, theme]);

  if (isLoading) {
    return (
      <div className="my-4 p-4 bg-gray-50 rounded-lg border border-gray-200 text-center">
        <div className="animate-pulse text-gray-500">Rendering diagram...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="my-4">
        <div className="p-3 bg-red-50 border border-red-200 rounded-t-lg text-red-600 text-sm">
          Failed to render Mermaid diagram: {error}
        </div>
        <pre className="p-4 bg-gray-50 rounded-b-lg overflow-x-auto text-sm border border-t-0 border-gray-200">
          <code>{code}</code>
        </pre>
      </div>
    );
  }

  return (
    <div
      ref={containerRef}
      className="my-4 p-4 bg-white rounded-lg border border-gray-200 overflow-x-auto"
      dangerouslySetInnerHTML={{ __html: svg }}
    />
  );
};

export default MermaidDiagram;
