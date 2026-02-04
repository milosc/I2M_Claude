'use client';

import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { MarkdownRenderer } from '../MarkdownRenderer';

export interface FileContentModalProps {
  /** File path to display */
  filePath: string | null;
  /** Called when modal should close */
  onClose: () => void;
}

interface FileContent {
  path: string;
  fileName: string;
  extension: string;
  content: string;
  size: number;
  modifiedAt: string;
}

// Extract frontmatter and body from markdown content
function extractFrontmatter(content: string): { frontmatter: string | null; body: string } {
  const match = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (match) {
    return {
      frontmatter: match[1].trim(),
      body: match[2].trim()
    };
  }
  return { frontmatter: null, body: content };
}

export function FileContentModal({ filePath, onClose }: FileContentModalProps) {
  const overlayRef = useRef<HTMLDivElement>(null);
  const [fileContent, setFileContent] = useState<FileContent | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch file content when path changes
  useEffect(() => {
    if (!filePath) {
      setFileContent(null);
      setError(null);
      return;
    }

    const fetchContent = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`/api/file-content?path=${encodeURIComponent(filePath)}`);
        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.error || 'Failed to load file');
        }
        const data = await response.json();
        setFileContent(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load file');
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, [filePath]);

  // Handle Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    if (filePath) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = '';
    };
  }, [filePath, onClose]);

  // Handle backdrop click
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === overlayRef.current) {
      onClose();
    }
  };

  if (!filePath) {
    return null;
  }

  if (typeof window === 'undefined') {
    return null;
  }

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const formatDate = (isoDate: string): string => {
    return new Date(isoDate).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return createPortal(
    <div
      ref={overlayRef}
      onClick={handleBackdropClick}
      className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-4"
      style={{
        animation: 'fadeIn 200ms ease-out',
      }}
    >
      <style jsx global>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slideIn {
          from { transform: scale(0.95); opacity: 0; }
          to { transform: scale(1); opacity: 1; }
        }
      `}</style>

      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="file-modal-title"
        className="bg-background rounded-lg shadow-2xl w-full max-w-6xl h-[90vh] overflow-hidden flex flex-col"
        style={{
          animation: 'slideIn 200ms ease-out',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-border bg-surface">
          <div className="flex-1 min-w-0">
            <h2 id="file-modal-title" className="text-xl font-bold text-foreground truncate">
              {fileContent?.fileName || filePath.split('/').pop()}
            </h2>
            <p className="text-sm text-secondary truncate mt-1">
              {filePath}
              {fileContent && (
                <span className="ml-3 text-xs">
                  {formatFileSize(fileContent.size)} · Modified {formatDate(fileContent.modifiedAt)}
                </span>
              )}
            </p>
          </div>

          <div className="flex items-center gap-2 ml-4">
            {/* Copy path button */}
            <button
              onClick={() => {
                navigator.clipboard.writeText(filePath);
              }}
              className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              title="Copy path"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
              </svg>
            </button>

            {/* Close button */}
            <button
              onClick={onClose}
              aria-label="Close modal"
              className="p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors focus:outline-none focus:ring-2 focus:ring-accent-default"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-auto p-6">
          {loading && (
            <div className="flex items-center justify-center h-full">
              <div className="flex items-center gap-3 text-secondary">
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Loading file content...</span>
              </div>
            </div>
          )}

          {error && (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <div className="text-red-500 mb-2">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <p className="text-red-500 font-medium">{error}</p>
                <button
                  onClick={onClose}
                  className="mt-4 px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 rounded transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          )}

          {!loading && !error && fileContent && (
            <div className="prose dark:prose-invert max-w-none">
              {fileContent.extension === 'md' ? (
                (() => {
                  const { frontmatter, body } = extractFrontmatter(fileContent.content);
                  return (
                    <>
                      {frontmatter && (
                        <div className="mb-6">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="text-xs font-semibold uppercase tracking-wider text-secondary">Frontmatter</span>
                            <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-0.5 rounded">YAML</span>
                          </div>
                          <pre className="bg-gray-900 dark:bg-gray-950 p-4 rounded-lg overflow-auto border border-gray-700">
                            <code className="text-sm text-gray-100 font-mono">{frontmatter}</code>
                          </pre>
                        </div>
                      )}
                      {body && (
                        <div>
                          {frontmatter && (
                            <div className="flex items-center gap-2 mb-2">
                              <span className="text-xs font-semibold uppercase tracking-wider text-secondary">Content</span>
                            </div>
                          )}
                          <MarkdownRenderer content={body} />
                        </div>
                      )}
                    </>
                  );
                })()
              ) : fileContent.extension === 'py' ? (
                <pre className="bg-gray-900 dark:bg-gray-950 p-4 rounded-lg overflow-auto border border-gray-700">
                  <code className="text-sm text-gray-100 font-mono">{fileContent.content}</code>
                </pre>
              ) : (
                <pre className="bg-gray-900 dark:bg-gray-950 p-4 rounded-lg overflow-auto border border-gray-700">
                  <code className="text-sm text-gray-100 font-mono">{fileContent.content}</code>
                </pre>
              )}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-border bg-surface flex items-center justify-between text-sm text-secondary">
          <span>Press ESC or click outside to close</span>
          <div className="flex items-center gap-4">
            {fileContent && (
              <span className="text-xs bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">
                .{fileContent.extension}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>,
    document.body
  );
}

export default FileContentModal;
