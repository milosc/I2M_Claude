import React from 'react';
import { TagDisplay } from '../TagDisplay';

export type Stage =
  | 'discovery'
  | 'prototype'
  | 'productspecs'
  | 'solarch'
  | 'implementation'
  | 'utility'
  | 'security'
  | 'grc';

export interface SearchResult {
  id: string;
  name: string;
  type: 'skill' | 'command' | 'agent' | 'rule' | 'hook';
  stage: Stage;
  path: string;
  summary: string;
  relevanceScore: number;
  /** User-defined tags (PF-002) */
  tags?: string[];
  isFavorite: boolean;
}

export interface SearchResultCardProps {
  /** Search result data */
  result: SearchResult;
  /** Search query for highlighting */
  query: string;
  /** Click handler */
  onClick: (resultId: string) => void;
  /** Copy path handler */
  onCopyPath?: (path: string) => void;
  /** Favorite toggle handler */
  onToggleFavorite?: (resultId: string) => void;
  /** Highlighted variant */
  highlighted?: boolean;
}

function highlightQuery(text: string, query: string): React.ReactNode {
  if (!query) return text;

  const regex = new RegExp(`(${query})`, 'gi');
  const parts = text.split(regex);

  return parts.map((part, index) => {
    if (part.toLowerCase() === query.toLowerCase()) {
      return (
        <mark
          key={index}
          style={{ backgroundColor: '#fef3c7', fontWeight: 600, padding: '0 2px' }}
        >
          {part}
        </mark>
      );
    }
    return <React.Fragment key={index}>{part}</React.Fragment>;
  });
}

function getRelevanceBadgeVariant(score: number): string {
  if (score >= 0.8) return 'bg-green-100 text-green-800'; // High relevance
  if (score >= 0.5) return 'bg-blue-100 text-blue-800'; // Medium relevance
  return 'bg-gray-100 text-gray-600'; // Low relevance
}

export const SearchResultCard: React.FC<SearchResultCardProps> = ({
  result,
  query,
  onClick,
  onCopyPath,
  onToggleFavorite,
  highlighted = false,
}) => {
  const handleCardClick = (e: React.MouseEvent) => {
    // Prevent onClick if clicking on action buttons
    if ((e.target as HTMLElement).tagName === 'BUTTON') {
      return;
    }
    onClick(result.id);
  };

  const handleCopyPath = (e: React.MouseEvent) => {
    e.stopPropagation();
    onCopyPath?.(result.path);
  };

  const handleToggleFavorite = (e: React.MouseEvent) => {
    e.stopPropagation();
    onToggleFavorite?.(result.id);
  };

  return (
    <article
      onClick={handleCardClick}
      className={`
        bg-white rounded-lg border-2 p-4 cursor-pointer transition-all
        hover:shadow-md hover:bg-blue-50
        ${highlighted ? 'border-blue-500 shadow-md' : 'border-gray-200'}
      `}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {highlightQuery(result.name, query)}
          </h3>

          {/* Badges */}
          <div className="flex gap-2 flex-wrap">
            <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">
              {result.type}
            </span>
            <span className="px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded">
              {result.stage}
            </span>
            <span className={`px-2 py-1 text-xs rounded relevance-badge ${getRelevanceBadgeVariant(result.relevanceScore)}`}>
              {Math.round(result.relevanceScore * 100)}%
            </span>
          </div>

          {/* Tags (PF-002) */}
          {result.tags && result.tags.length > 0 && (
            <div className="mt-2">
              <TagDisplay tags={result.tags} readonly />
            </div>
          )}
        </div>

        {/* Favorite Icon */}
        {result.isFavorite && (
          <span className="favorite-icon text-amber-500 text-xl ml-2">★</span>
        )}
      </div>

      {/* Summary */}
      <p className="text-sm text-gray-600 mb-3">
        {highlightQuery(result.summary, query)}
      </p>

      {/* Path */}
      <p className="text-xs text-gray-500 font-mono mb-3">{result.path}</p>

      {/* Actions */}
      {(onCopyPath || onToggleFavorite) && (
        <div className="flex gap-2">
          {onCopyPath && (
            <button
              onClick={handleCopyPath}
              className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
            >
              Copy
            </button>
          )}
          {onToggleFavorite && (
            <button
              onClick={handleToggleFavorite}
              className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
            >
              {result.isFavorite ? 'Unfavorite' : 'Favorite'}
            </button>
          )}
        </div>
      )}
    </article>
  );
};

export default SearchResultCard;
