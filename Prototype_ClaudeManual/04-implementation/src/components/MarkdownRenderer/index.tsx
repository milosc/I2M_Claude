'use client';

import React, { useCallback } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import { MermaidDiagram } from '@/components/MermaidDiagram';
import 'highlight.js/styles/github.css';

export interface MarkdownRendererProps {
  /** Markdown content */
  content: string;
  /** Theme variant */
  theme?: 'light' | 'dark';
  /** Enable Mermaid diagram rendering (default: true) */
  enableDiagrams?: boolean;
  /** Code copy handler */
  onCopyCode?: (code: string, language: string) => void;
}

export const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({
  content,
  theme = 'light',
  enableDiagrams = true,
  onCopyCode,
}) => {
  const handleCopyCode = useCallback(
    (code: string, language: string) => {
      if (onCopyCode) {
        onCopyCode(code, language);
      } else {
        navigator.clipboard.writeText(code);
      }
    },
    [onCopyCode]
  );

  return (
    <div
      className={`markdown-renderer ${theme === 'dark' ? 'theme-dark' : 'theme-light'}`}
      style={{
        fontFamily: 'system-ui, -apple-system, sans-serif',
        color: theme === 'dark' ? '#e0e0e0' : '#1a1a1a',
        background: theme === 'dark' ? '#1a1a1a' : '#ffffff',
      }}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[[rehypeHighlight, { plainText: ['mermaid', 'mmd'] }]]}
        components={{
          // Headings with proper spacing
          h1: ({ children }) => (
            <h1 className="text-3xl font-bold mt-8 mb-4 pb-2 border-b border-gray-200">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-2xl font-semibold mt-6 mb-3 pb-1 border-b border-gray-100">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-xl font-semibold mt-5 mb-2">{children}</h3>
          ),
          h4: ({ children }) => (
            <h4 className="text-lg font-medium mt-4 mb-2">{children}</h4>
          ),
          h5: ({ children }) => (
            <h5 className="text-base font-medium mt-3 mb-1">{children}</h5>
          ),
          h6: ({ children }) => (
            <h6 className="text-sm font-medium mt-3 mb-1 text-gray-600">{children}</h6>
          ),

          // Paragraphs with proper spacing
          p: ({ children }) => (
            <p className="my-4 leading-7">{children}</p>
          ),

          // Lists with proper spacing
          ul: ({ children }) => (
            <ul className="my-4 ml-6 list-disc space-y-2">{children}</ul>
          ),
          ol: ({ children }) => (
            <ol className="my-4 ml-6 list-decimal space-y-2">{children}</ol>
          ),
          li: ({ children }) => (
            <li className="leading-7">{children}</li>
          ),

          // Blockquotes
          blockquote: ({ children }) => (
            <blockquote className="my-4 pl-4 border-l-4 border-gray-300 italic text-gray-600">
              {children}
            </blockquote>
          ),

          // Code blocks - handle mermaid here
          code: ({ className, children, node, ...props }) => {
            const match = /language-(\w+)/.exec(className || '');
            const language = match ? match[1] : '';

            // Check if this is inline code (no className means inline in most cases)
            // Also check if parent is pre (block code)
            const isInline = !className;

            // Extract text content
            const codeString = String(children).replace(/\n$/, '');

            // Check if this is a mermaid block
            const isMermaid = enableDiagrams && (language === 'mermaid' || language === 'mmd');

            if (isMermaid && !isInline) {
              // Return mermaid diagram - the pre wrapper will be handled separately
              return <MermaidDiagram code={codeString} theme={theme} />;
            }

            if (isInline) {
              return (
                <code
                  className="px-1.5 py-0.5 bg-gray-100 rounded text-sm font-mono text-red-600"
                  {...props}
                >
                  {children}
                </code>
              );
            }

            // Regular code block
            return (
              <code className={className} {...props}>
                {children}
              </code>
            );
          },

          // Pre wrapper for code blocks
          pre: ({ children, node, ...props }) => {
            // Check if the child is a MermaidDiagram (it will be a div, not code)
            const childArray = React.Children.toArray(children);
            const firstChild = childArray[0];

            // If the child is our MermaidDiagram, don't wrap in pre
            if (React.isValidElement(firstChild) && firstChild.type === MermaidDiagram) {
              return <>{children}</>;
            }

            // Extract code content for copy button
            let codeContent = '';
            let language = '';

            if (React.isValidElement(firstChild)) {
              const childProps = firstChild.props as { children?: React.ReactNode; className?: string };
              codeContent = String(childProps.children || '').replace(/\n$/, '');
              const match = /language-(\w+)/.exec(childProps.className || '');
              language = match ? match[1] : '';
            }

            return (
              <div className="relative my-4 group">
                <pre className="p-4 bg-gray-50 rounded-lg overflow-x-auto text-sm leading-6" {...props}>
                  {children}
                </pre>
                {codeContent && (
                  <button
                    onClick={() => handleCopyCode(codeContent, language)}
                    className="absolute top-2 right-2 px-2 py-1 text-xs bg-gray-200 hover:bg-gray-300 rounded opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    Copy
                  </button>
                )}
              </div>
            );
          },

          // Tables
          table: ({ children }) => (
            <div className="my-4 overflow-x-auto">
              <table className="min-w-full border-collapse border border-gray-200">
                {children}
              </table>
            </div>
          ),
          thead: ({ children }) => (
            <thead className="bg-gray-50">{children}</thead>
          ),
          th: ({ children }) => (
            <th className="px-4 py-2 border border-gray-200 text-left font-semibold">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="px-4 py-2 border border-gray-200">{children}</td>
          ),

          // Horizontal rule
          hr: () => <hr className="my-8 border-gray-200" />,

          // Links
          a: ({ href, children }) => (
            <a
              href={href}
              className="text-blue-600 hover:text-blue-800 underline"
              target={href?.startsWith('http') ? '_blank' : undefined}
              rel={href?.startsWith('http') ? 'noopener noreferrer' : undefined}
            >
              {children}
            </a>
          ),

          // Images
          img: ({ src, alt }) => (
            <img
              src={src}
              alt={alt || ''}
              className="my-4 max-w-full h-auto rounded"
            />
          ),

          // Strong/Bold
          strong: ({ children }) => (
            <strong className="font-semibold">{children}</strong>
          ),

          // Emphasis/Italic
          em: ({ children }) => <em className="italic">{children}</em>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer;
