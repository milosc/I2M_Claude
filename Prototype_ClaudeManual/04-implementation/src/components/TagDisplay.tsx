'use client'

/**
 * TagDisplay Component
 *
 * Displays tags as badges with optional remove capability.
 * Used in DetailPane to show component tags.
 *
 * Traceability:
 * - JTBD-1.3: Quickly Find Relevant Framework Tools
 * - CF-010: Tagging system
 * - PF-002: Tagging Feature Feedback
 */

// X icon component (inline to avoid lucide-react dependency)
function XIcon({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
      strokeWidth={2}
    >
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  )
}

export interface TagDisplayProps {
  /** Array of tag strings to display */
  tags: string[]
  /** Callback when user clicks remove on a tag */
  onRemove?: (tag: string) => void
  /** If true, hide remove buttons (default: false) */
  readonly?: boolean
  /** Additional CSS classes */
  className?: string
}

export function TagDisplay({
  tags,
  onRemove,
  readonly = false,
  className = '',
}: TagDisplayProps) {
  if (!tags || tags.length === 0) {
    return null
  }

  return (
    <div
      className={`flex flex-wrap gap-1 ${className}`}
      role="list"
      aria-label="Tags"
    >
      {tags.map((tag) => (
        <span
          key={tag}
          role="listitem"
          className="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700"
        >
          {tag}
          {!readonly && onRemove && (
            <button
              onClick={() => onRemove(tag)}
              className="ml-0.5 p-0.5 rounded-full hover:bg-slate-200 dark:hover:bg-slate-700 focus:outline-none focus:ring-2 focus:ring-offset-1 focus:ring-blue-500"
              aria-label={`Remove ${tag} tag`}
              type="button"
            >
              <XIcon className="h-3 w-3" aria-hidden="true" />
            </button>
          )}
        </span>
      ))}
    </div>
  )
}

export default TagDisplay
