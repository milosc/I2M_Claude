'use client'

/**
 * StageSelector Component
 *
 * Multi-select component for assigning stages to a component.
 * A component can belong to multiple stages.
 *
 * Traceability:
 * - JTBD-1.3: Quickly Find Relevant Framework Tools
 * - CF-010: Flexible categorization
 * - PF-003: Multi-Stage Feature
 */

import { Stage } from '@/types'

// All available stages with display info
const ALL_STAGES: { value: Stage; label: string; color: string }[] = [
  { value: Stage.Discovery, label: 'Discovery', color: 'bg-blue-100 text-blue-800 border-blue-300' },
  { value: Stage.Prototype, label: 'Prototype', color: 'bg-green-100 text-green-800 border-green-300' },
  { value: Stage.ProductSpecs, label: 'ProductSpecs', color: 'bg-yellow-100 text-yellow-800 border-yellow-300' },
  { value: Stage.SolArch, label: 'SolArch', color: 'bg-orange-100 text-orange-800 border-orange-300' },
  { value: Stage.Implementation, label: 'Implementation', color: 'bg-purple-100 text-purple-800 border-purple-300' },
  { value: Stage.Utility, label: 'Utility', color: 'bg-gray-100 text-gray-800 border-gray-300' },
  { value: Stage.Security, label: 'Security', color: 'bg-red-100 text-red-800 border-red-300' },
  { value: Stage.GRC, label: 'GRC', color: 'bg-pink-100 text-pink-800 border-pink-300' },
]

// Helper to normalize stage strings to enum values
function normalizeStage(stage: string | Stage): Stage | null {
  const lower = String(stage).toLowerCase()
  const found = ALL_STAGES.find(s => s.value.toLowerCase() === lower || s.label.toLowerCase() === lower)
  return found?.value || null
}

export interface StageSelectorProps {
  /** Currently selected stages */
  selectedStages: Stage[]
  /** Original stage from the component (shown as default if no custom stages) */
  originalStage?: Stage | string
  /** Callback when stages change */
  onStagesChange: (stages: Stage[]) => void
  /** Label for the component */
  label?: string
  /** Additional CSS classes */
  className?: string
}

export function StageSelector({
  selectedStages,
  originalStage,
  onStagesChange,
  label = 'Stages',
  className = '',
}: StageSelectorProps) {
  // Normalize originalStage to enum value
  const normalizedOriginalStage = originalStage ? normalizeStage(originalStage) : null

  const handleToggle = (stage: Stage) => {
    if (selectedStages.includes(stage)) {
      onStagesChange(selectedStages.filter((s) => s !== stage))
    } else {
      onStagesChange([...selectedStages, stage])
    }
  }

  const handleReset = () => {
    onStagesChange([])
  }

  // Determine which stages to show as "active"
  // If user has custom stages, show those; otherwise show the original stage
  const activeStages = selectedStages.length > 0 ? selectedStages : (normalizedOriginalStage ? [normalizedOriginalStage] : [])
  const hasCustomStages = selectedStages.length > 0

  return (
    <div className={`stage-selector ${className}`}>
      <div className="flex items-center gap-2 mb-2">
        <span className="text-xs font-medium text-gray-500">{label}:</span>
        {hasCustomStages && (
          <button
            onClick={handleReset}
            className="text-xs text-blue-600 hover:underline focus:outline-none"
            type="button"
          >
            Reset to original
          </button>
        )}
      </div>

      <div className="flex flex-wrap gap-2" role="group" aria-label={label}>
        {ALL_STAGES.map(({ value, label: stageLabel, color }) => {
          const isActive = activeStages.includes(value)
          const isOriginal = value === normalizedOriginalStage && !hasCustomStages

          return (
            <button
              key={value}
              onClick={() => handleToggle(value)}
              type="button"
              className={`
                px-2 py-1 text-xs font-medium rounded border transition-all
                focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1
                ${isActive
                  ? `${color} border-current`
                  : 'bg-white text-gray-400 border-gray-200 hover:border-gray-300 hover:text-gray-600'
                }
                ${isOriginal ? 'ring-1 ring-blue-400' : ''}
              `}
              aria-pressed={isActive}
              title={isOriginal ? 'Original stage (click to customize)' : (isActive ? 'Click to remove' : 'Click to add')}
            >
              {stageLabel}
              {isActive && (
                <span className="ml-1" aria-hidden="true">✓</span>
              )}
            </button>
          )
        })}
      </div>

      {!hasCustomStages && normalizedOriginalStage && (
        <p className="mt-1 text-xs text-gray-400 italic">
          Click stages to customize. Currently showing original stage.
        </p>
      )}
    </div>
  )
}

export default StageSelector
