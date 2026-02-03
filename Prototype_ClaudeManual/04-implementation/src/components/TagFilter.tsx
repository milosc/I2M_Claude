'use client'

/**
 * TagFilter Component
 *
 * Multi-select filter for filtering search results by tags.
 * Displays available tags as toggleable buttons.
 *
 * Traceability:
 * - JTBD-1.3: Quickly Find Relevant Framework Tools - "Can tag components"
 * - CF-010: Tagging system
 * - PF-002: Tagging Feature Feedback
 */

import { useMemo } from 'react'

export interface TagFilterProps {
  /** All available tags across all components */
  availableTags: string[]
  /** Currently selected tags for filtering */
  selectedTags: string[]
  /** Callback when selection changes */
  onTagsChange: (tags: string[]) => void
  /** Optional label */
  label?: string
  /** Additional CSS classes */
  className?: string
}

export function TagFilter({
  availableTags,
  selectedTags,
  onTagsChange,
  label = 'Tags',
  className = '',
}: TagFilterProps) {
  // Sort tags alphabetically, with selected ones first
  const sortedTags = useMemo(() => {
    return [...availableTags].sort((a, b) => {
      const aSelected = selectedTags.includes(a)
      const bSelected = selectedTags.includes(b)
      if (aSelected && !bSelected) return -1
      if (!aSelected && bSelected) return 1
      return a.localeCompare(b)
    })
  }, [availableTags, selectedTags])

  const toggleTag = (tag: string) => {
    if (selectedTags.includes(tag)) {
      onTagsChange(selectedTags.filter((t) => t !== tag))
    } else {
      onTagsChange([...selectedTags, tag])
    }
  }

  const clearAll = () => {
    onTagsChange([])
  }

  if (!availableTags || availableTags.length === 0) {
    return null
  }

  return (
    <div className={`tag-filter ${className}`} role="group" aria-label={label}>
      <div className="flex items-center gap-2 mb-2">
        <span className="text-sm font-medium text-slate-600 dark:text-slate-400">
          {label}:
        </span>
        {selectedTags.length > 0 && (
          <button
            onClick={clearAll}
            className="text-xs text-blue-600 dark:text-blue-400 hover:underline focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1 rounded"
            type="button"
          >
            Clear all
          </button>
        )}
      </div>

      <div className="flex flex-wrap gap-2" role="listbox" aria-multiselectable="true">
        {sortedTags.map((tag) => {
          const isSelected = selectedTags.includes(tag)
          return (
            <button
              key={tag}
              onClick={() => toggleTag(tag)}
              role="option"
              aria-selected={isSelected}
              className={`
                px-3 py-1 text-xs font-medium rounded-full border transition-colors
                focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1
                ${
                  isSelected
                    ? 'bg-blue-600 text-white border-blue-600 dark:bg-blue-500 dark:border-blue-500'
                    : 'bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-700'
                }
              `}
              type="button"
            >
              {tag}
              {isSelected && (
                <span className="ml-1" aria-hidden="true">
                  ✓
                </span>
              )}
            </button>
          )
        })}
      </div>

      {selectedTags.length > 0 && (
        <div className="mt-2 text-xs text-slate-500 dark:text-slate-400">
          Showing items with: {selectedTags.join(', ')}
        </div>
      )}
    </div>
  )
}

export default TagFilter
