import React, { useState, useRef, useEffect } from 'react';

export type Stage =
  | 'discovery'
  | 'prototype'
  | 'productspecs'
  | 'solarch'
  | 'implementation'
  | 'utility'
  | 'security'
  | 'grc';

export interface StageFilterDropdownProps {
  /** Selected stages */
  selectedStages: Stage[];
  /** Change handler */
  onChange: (stages: Stage[]) => void;
  /** Show badge count */
  showCount?: boolean;
}

const STAGE_LABELS: Record<Stage, string> = {
  discovery: 'Discovery',
  prototype: 'Prototype',
  productspecs: 'ProductSpecs',
  solarch: 'SolArch',
  implementation: 'Implementation',
  utility: 'Utility',
  security: 'Security',
  grc: 'GRC',
};

const STAGE_COLORS: Record<Stage, string> = {
  discovery: 'bg-blue-100 text-blue-800',
  prototype: 'bg-purple-100 text-purple-800',
  productspecs: 'bg-green-100 text-green-800',
  solarch: 'bg-orange-100 text-orange-800',
  implementation: 'bg-red-100 text-red-800',
  utility: 'bg-gray-100 text-gray-800',
  security: 'bg-yellow-100 text-yellow-800',
  grc: 'bg-pink-100 text-pink-800',
};

const ALL_STAGES: Stage[] = [
  'discovery',
  'prototype',
  'productspecs',
  'solarch',
  'implementation',
  'utility',
  'security',
  'grc',
];

export const StageFilterDropdown: React.FC<StageFilterDropdownProps> = ({
  selectedStages,
  onChange,
  showCount = true,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleToggleStage = (stage: Stage) => {
    if (selectedStages.includes(stage)) {
      onChange(selectedStages.filter((s) => s !== stage));
    } else {
      onChange([...selectedStages, stage]);
    }
  };

  const handleClear = () => {
    onChange([]);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Filter by stage"
        className="px-4 py-2 bg-white border border-gray-300 rounded hover:bg-gray-50 flex items-center gap-2"
      >
        <span>Filter by stage</span>
        {showCount && selectedStages.length > 0 && (
          <span className="px-2 py-0.5 text-xs bg-blue-500 text-white rounded count-badge">
            {selectedStages.length} selected
          </span>
        )}
        <svg
          className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute top-full left-0 mt-2 w-64 bg-white border border-gray-200 rounded shadow-lg z-10">
          {/* Header */}
          <div className="p-3 border-b border-gray-200 flex justify-between items-center">
            <label className="text-sm font-semibold text-gray-700">Filter by stage</label>
            <button
              onClick={handleClear}
              className="text-xs text-blue-600 hover:text-blue-800"
            >
              Clear
            </button>
          </div>

          {/* Stage List */}
          <div className="p-2 max-h-96 overflow-y-auto">
            {ALL_STAGES.map((stage) => (
              <label
                key={stage}
                className="flex items-center px-3 py-2 hover:bg-gray-50 cursor-pointer rounded"
              >
                <input
                  type="checkbox"
                  value={stage}
                  checked={selectedStages.includes(stage)}
                  onChange={() => handleToggleStage(stage)}
                  className="mr-3 w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                />
                <span className={`px-2 py-1 text-xs rounded stage-${stage} ${STAGE_COLORS[stage]}`}>
                  {STAGE_LABELS[stage]}
                </span>
              </label>
            ))}
          </div>

          {/* Hidden select for testing compatibility */}
          <select
            className="hidden"
            aria-label="Filter by stage"
            multiple
            value={selectedStages}
            onChange={(e) => {
              const selected = Array.from(e.target.selectedOptions).map(
                (opt) => opt.value as Stage
              );
              onChange(selected);
            }}
          >
            {ALL_STAGES.map((stage) => (
              <option key={stage} value={stage}>
                {STAGE_LABELS[stage]}
              </option>
            ))}
          </select>
        </div>
      )}
    </div>
  );
};

export default StageFilterDropdown;
