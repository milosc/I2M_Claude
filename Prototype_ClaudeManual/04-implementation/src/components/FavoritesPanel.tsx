import React, { useState } from 'react';
import { ComponentCard } from './ComponentCard';
import { cn } from '@/lib/utils';

type ComponentType = 'skill' | 'command' | 'agent' | 'rule' | 'hook';
type Stage = 'discovery' | 'prototype' | 'productspecs' | 'solarch' | 'implementation';

export interface ComponentMeta {
  id: string;
  name: string;
  type: ComponentType;
  stage: Stage;
  path: string;
  summary: string;
  isFavorite: boolean;
  lastUpdated?: string;
}

interface FavoritesPanelProps {
  favorites: ComponentMeta[];
  onReorder: (newOrder: string[]) => void;
  onRemove: (componentId: string) => void;
  onClearAll: () => void;
  onClick: (componentId: string) => void;
}

type FilterType = 'all' | 'agent' | 'command' | 'skill' | 'rule' | 'hook';

export function FavoritesPanel({
  favorites,
  onReorder,
  onRemove,
  onClearAll,
  onClick,
}: FavoritesPanelProps) {
  const [filter, setFilter] = useState<FilterType>('all');
  const [showClearConfirm, setShowClearConfirm] = useState(false);

  const filteredFavorites =
    filter === 'all' ? favorites : favorites.filter((f) => f.type === filter);

  const handleClearAll = () => {
    setShowClearConfirm(true);
  };

  const confirmClearAll = () => {
    onClearAll();
    setShowClearConfirm(false);
  };

  const cancelClearAll = () => {
    setShowClearConfirm(false);
  };

  const getFilterLabel = (type: FilterType): string => {
    if (type === 'all') return 'All';
    return type.charAt(0).toUpperCase() + type.slice(1) + 's';
  };

  const getFilterCount = (type: FilterType): number => {
    if (type === 'all') return favorites.length;
    return favorites.filter((f) => f.type === type).length;
  };

  return (
    <section role="region" aria-label="Favorites panel" className="w-full">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">My Favorites</h2>
          <p className="text-sm text-gray-600 mt-1">
            {favorites.length === 0
              ? 'No favorites yet'
              : `${favorites.length} favorite${favorites.length === 1 ? '' : 's'}`}
          </p>
        </div>

        {favorites.length > 0 && (
          <button
            type="button"
            onClick={handleClearAll}
            className={cn(
              'px-4 py-2 text-sm font-medium text-red-600 bg-red-50',
              'border border-red-200 rounded-md hover:bg-red-100',
              'focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors'
            )}
          >
            Clear All
          </button>
        )}
      </div>

      {/* Type Filters */}
      {favorites.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-6" role="toolbar" aria-label="Filter favorites by type">
          {(['all', 'agent', 'command', 'skill', 'rule', 'hook'] as FilterType[]).map((type) => {
            const count = getFilterCount(type);
            if (count === 0 && type !== 'all') return null;

            return (
              <button
                key={type}
                type="button"
                onClick={() => setFilter(type)}
                className={cn(
                  'px-4 py-2 text-sm font-medium rounded-md transition-colors',
                  'focus:outline-none focus:ring-2 focus:ring-accent-default',
                  filter === type
                    ? 'bg-accent-default text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                )}
                aria-pressed={filter === type}
              >
                {getFilterLabel(type)}
                {type !== 'all' && count > 0 && (
                  <span className="ml-1.5 text-xs opacity-75">({count})</span>
                )}
              </button>
            );
          })}
        </div>
      )}

      {/* Active Filter Announcement */}
      {filter !== 'all' && filteredFavorites.length > 0 && (
        <div className="sr-only" role="status" aria-live="polite">
          Showing {filteredFavorites.length} {filter}
          {filteredFavorites.length === 1 ? '' : 's'}
        </div>
      )}

      {/* Empty State */}
      {favorites.length === 0 && (
        <div className="flex flex-col items-center justify-center py-16 px-4 text-center">
          <div
            role="img"
            aria-label="No favorites illustration"
            className="w-24 h-24 mb-6 text-gray-300"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
              />
            </svg>
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No Favorites Yet</h3>
          <p className="text-gray-600 max-w-md">
            Start adding your favorite components, commands, and agents to quickly access them here.
          </p>
        </div>
      )}

      {/* Favorites Grid */}
      {filteredFavorites.length > 0 && (
        <div
          data-testid="favorites-grid"
          className={cn(
            'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'
          )}
        >
          {filteredFavorites.map((favorite) => (
            <ComponentCard
              key={favorite.id}
              component={favorite}
              variant="grid"
              showRemove={true}
              onClick={onClick}
              onToggleFavorite={() => {}}
              onRemove={onRemove}
            />
          ))}
        </div>
      )}

      {/* Clear All Confirmation Modal */}
      {showClearConfirm && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          role="dialog"
          aria-modal="true"
          aria-labelledby="clear-all-title"
        >
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4 shadow-xl">
            <h3 id="clear-all-title" className="text-lg font-semibold text-gray-900 mb-2">
              Remove All Favorites?
            </h3>
            <p className="text-gray-600 mb-6">
              Remove all {favorites.length} favorite{favorites.length === 1 ? '' : 's'}? This action
              cannot be undone.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                type="button"
                onClick={cancelClearAll}
                className={cn(
                  'px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100',
                  'border border-gray-300 rounded-md hover:bg-gray-200',
                  'focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors'
                )}
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={confirmClearAll}
                className={cn(
                  'px-4 py-2 text-sm font-medium text-white bg-red-600',
                  'border border-red-600 rounded-md hover:bg-red-700',
                  'focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors'
                )}
              >
                Confirm
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
