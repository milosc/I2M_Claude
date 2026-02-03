import React from 'react';
import { cn } from '@/lib/utils';

type ComponentType = 'skill' | 'command' | 'agent' | 'rule' | 'hook';
type Stage = 'discovery' | 'prototype' | 'productspecs' | 'solarch' | 'implementation';

interface ComponentMeta {
  id: string;
  name: string;
  type: ComponentType;
  stage: Stage;
  path: string;
  summary: string;
  isFavorite: boolean;
  lastUpdated?: string;
}

interface ComponentCardProps {
  component: ComponentMeta;
  onClick: (componentId: string) => void;
  onToggleFavorite: (componentId: string) => void;
  onRemove?: (componentId: string) => void;
  variant?: 'grid' | 'list';
  showRemove?: boolean;
}

const stageColors: Record<Stage, string> = {
  discovery: 'bg-purple-100 text-purple-800 border-purple-200',
  prototype: 'bg-blue-100 text-blue-800 border-blue-200',
  productspecs: 'bg-green-100 text-green-800 border-green-200',
  solarch: 'bg-orange-100 text-orange-800 border-orange-200',
  implementation: 'bg-red-100 text-red-800 border-red-200',
};

const typeColors: Record<ComponentType, string> = {
  skill: 'bg-indigo-100 text-indigo-800',
  command: 'bg-cyan-100 text-cyan-800',
  agent: 'bg-pink-100 text-pink-800',
  rule: 'bg-yellow-100 text-yellow-800',
  hook: 'bg-teal-100 text-teal-800',
};

export function ComponentCard({
  component,
  onClick,
  onToggleFavorite,
  onRemove,
  variant = 'grid',
  showRemove = false,
}: ComponentCardProps) {
  const handleCardClick = (e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest('button')) {
      return;
    }
    onClick(component.id);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !(e.target as HTMLElement).closest('button')) {
      onClick(component.id);
    }
  };

  const handleToggleFavorite = (e: React.MouseEvent) => {
    e.stopPropagation();
    onToggleFavorite(component.id);
  };

  const handleRemove = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (onRemove) {
      onRemove(component.id);
    }
  };

  const isListVariant = variant === 'list';

  return (
    <article
      role="article"
      aria-label={`Component card: ${component.name}`}
      className={cn(
        'bg-white rounded-lg border border-gray-200 shadow-sm',
        'hover:shadow-md hover:bg-blue-50 transition-all duration-200',
        'focus:outline-none focus:ring-2 focus:ring-accent-default',
        'cursor-pointer active:scale-98',
        isListVariant ? 'flex items-start gap-4 p-4' : 'p-6'
      )}
      onClick={handleCardClick}
      onKeyDown={handleKeyDown}
      tabIndex={0}
    >
      <div className={cn('flex-1', isListVariant ? 'flex items-start gap-4' : '')}>
        {/* Header */}
        <div className={cn('flex items-start justify-between', isListVariant ? 'flex-1' : 'mb-3')}>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">{component.name}</h3>

            {/* Badges */}
            <div className="flex flex-wrap gap-2 mb-3">
              <span
                className={cn(
                  'inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium',
                  typeColors[component.type]
                )}
              >
                {component.type}
              </span>
              <span
                className={cn(
                  'inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium border',
                  stageColors[component.stage]
                )}
              >
                {component.stage}
              </span>
            </div>
          </div>

          {/* Favorite Button */}
          <button
            type="button"
            onClick={handleToggleFavorite}
            aria-label={component.isFavorite ? 'Remove from favorites' : 'Add to favorites'}
            aria-pressed={component.isFavorite}
            className={cn(
              'flex-shrink-0 p-2 rounded-md transition-colors',
              'hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-accent-default',
              component.isFavorite ? 'text-amber-500' : 'text-gray-400'
            )}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill={component.isFavorite ? 'currentColor' : 'none'}
              stroke="currentColor"
              className="w-5 h-5"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
              />
            </svg>
          </button>
        </div>

        {/* Summary */}
        <p className={cn('text-sm text-gray-600', isListVariant ? 'mb-2' : 'mb-4')}>
          {component.summary}
        </p>

        {/* Path (List variant only) */}
        {isListVariant && (
          <p className="text-xs text-gray-500 font-mono mb-2">{component.path}</p>
        )}

        {/* Last Updated */}
        {component.lastUpdated && (
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              className="w-4 h-4"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                clipRule="evenodd"
              />
            </svg>
            <span>Updated {component.lastUpdated}</span>
          </div>
        )}
      </div>

      {/* Remove Button */}
      {showRemove && onRemove && (
        <button
          type="button"
          onClick={handleRemove}
          aria-label="Remove from favorites"
          className={cn(
            'mt-3 px-3 py-1.5 text-sm font-medium text-red-600 bg-red-50',
            'border border-red-200 rounded-md hover:bg-red-100',
            'focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors'
          )}
        >
          Remove
        </button>
      )}
    </article>
  );
}
