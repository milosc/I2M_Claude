'use client';

/**
 * AllTagsPanel Component
 *
 * Displays all user-defined tags across components with usage counts.
 * Allows users to click on tags to apply them as filters.
 *
 * Traceability:
 * - PF-002: Tagging Feature
 * - JTBD-1.3: Quickly Find Relevant Framework Tools
 */

import { useState, useMemo } from 'react';
import { cn } from '@/lib/utils';

export interface TagWithCount {
  name: string;
  count: number;
}

export interface AllTagsPanelProps {
  /** All tags with their usage counts */
  tags: TagWithCount[];
  /** Currently selected tags */
  selectedTags: string[];
  /** Callback when a tag is clicked */
  onTagClick: (tag: string) => void;
  /** Callback to clear all selected tags */
  onClearAll?: () => void;
  /** Whether the panel is collapsible */
  collapsible?: boolean;
  /** Initial collapsed state */
  defaultCollapsed?: boolean;
  /** Title for the panel */
  title?: string;
}

export function AllTagsPanel({
  tags,
  selectedTags,
  onTagClick,
  onClearAll,
  collapsible = true,
  defaultCollapsed = false,
  title = 'All Tags',
}: AllTagsPanelProps) {
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed);

  // Sort tags: selected first, then by count (descending), then alphabetically
  const sortedTags = useMemo(() => {
    return [...tags].sort((a, b) => {
      const aSelected = selectedTags.includes(a.name);
      const bSelected = selectedTags.includes(b.name);
      if (aSelected && !bSelected) return -1;
      if (!aSelected && bSelected) return 1;
      if (b.count !== a.count) return b.count - a.count;
      return a.name.localeCompare(b.name);
    });
  }, [tags, selectedTags]);

  if (tags.length === 0) {
    return null;
  }

  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg overflow-hidden">
      {/* Header */}
      <div
        className={cn(
          'flex items-center justify-between px-4 py-3 bg-gray-100',
          collapsible && 'cursor-pointer hover:bg-gray-200'
        )}
        onClick={collapsible ? () => setIsCollapsed(!isCollapsed) : undefined}
        role={collapsible ? 'button' : undefined}
        aria-expanded={collapsible ? !isCollapsed : undefined}
      >
        <div className="flex items-center gap-2">
          {collapsible && (
            <svg
              className={cn('w-4 h-4 text-gray-600 transition-transform', !isCollapsed && 'rotate-90')}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          )}
          <h3 className="font-semibold text-sm text-gray-800">{title}</h3>
          <span className="text-xs text-gray-600 bg-gray-200 px-2 py-0.5 rounded-full">
            {tags.length}
          </span>
        </div>

        {selectedTags.length > 0 && onClearAll && (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onClearAll();
            }}
            className="text-xs text-blue-600 hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500 rounded px-2 py-1"
          >
            Clear ({selectedTags.length})
          </button>
        )}
      </div>

      {/* Tags Grid */}
      {!isCollapsed && (
        <div className="p-4 bg-white">
          {selectedTags.length > 0 && (
            <p className="text-xs text-gray-500 mb-3">
              Click to toggle filter. Selected tags: {selectedTags.join(', ')}
            </p>
          )}

          <div className="flex flex-wrap gap-2">
            {sortedTags.map((tag) => {
              const isSelected = selectedTags.includes(tag.name);
              return (
                <button
                  key={tag.name}
                  onClick={() => onTagClick(tag.name)}
                  className={cn(
                    'inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium rounded-full border transition-all',
                    'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1',
                    'hover:scale-105 active:scale-95',
                    isSelected
                      ? 'bg-blue-600 text-white border-blue-600 shadow-md'
                      : 'bg-gray-100 text-gray-700 border-gray-300 hover:border-blue-400 hover:bg-gray-200'
                  )}
                  aria-pressed={isSelected}
                >
                  <span className="truncate max-w-[150px]">{tag.name}</span>
                  <span
                    className={cn(
                      'text-xs px-1.5 py-0.5 rounded-full',
                      isSelected
                        ? 'bg-white/20 text-white'
                        : 'bg-gray-200 text-gray-600'
                    )}
                  >
                    {tag.count}
                  </span>
                  {isSelected && (
                    <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  )}
                </button>
              );
            })}
          </div>

          {tags.length === 0 && (
            <p className="text-sm text-gray-500 text-center py-4">
              No tags yet. Add tags to components to see them here.
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default AllTagsPanel;
