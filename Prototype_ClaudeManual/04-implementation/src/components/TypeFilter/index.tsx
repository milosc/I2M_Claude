import React from 'react';

export type ItemType = 'Skill' | 'Command' | 'Agent' | 'Hook' | 'Workflow' | 'Architecture';

export interface TypeFilterProps {
  /** Selected types (empty means "All") */
  selectedTypes: ItemType[];
  /** Change handler */
  onChange: (types: ItemType[]) => void;
  /** Show count per type */
  counts?: Partial<Record<ItemType, number>>;
}

const ALL_TYPES: ItemType[] = ['Skill', 'Command', 'Agent', 'Hook', 'Workflow', 'Architecture'];

const TYPE_COLORS: Record<ItemType | 'All', { base: string; selected: string }> = {
  All: {
    base: 'bg-gray-100 text-gray-800 hover:bg-gray-200',
    selected: 'bg-gray-800 text-white'
  },
  Skill: {
    base: 'bg-blue-100 text-blue-800 hover:bg-blue-200',
    selected: 'bg-blue-600 text-white'
  },
  Command: {
    base: 'bg-green-100 text-green-800 hover:bg-green-200',
    selected: 'bg-green-600 text-white'
  },
  Agent: {
    base: 'bg-purple-100 text-purple-800 hover:bg-purple-200',
    selected: 'bg-purple-600 text-white'
  },
  Hook: {
    base: 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200',
    selected: 'bg-yellow-600 text-white'
  },
  Workflow: {
    base: 'bg-orange-100 text-orange-800 hover:bg-orange-200',
    selected: 'bg-orange-600 text-white'
  },
  Architecture: {
    base: 'bg-red-100 text-red-800 hover:bg-red-200',
    selected: 'bg-red-600 text-white'
  },
};

export const TypeFilter: React.FC<TypeFilterProps> = ({
  selectedTypes,
  onChange,
  counts,
}) => {
  const isAllSelected = selectedTypes.length === 0;

  const handleAllClick = () => {
    onChange([]);
  };

  const handleTypeClick = (type: ItemType) => {
    if (selectedTypes.includes(type)) {
      // Remove type
      const newTypes = selectedTypes.filter((t) => t !== type);
      onChange(newTypes);
    } else {
      // Add type
      onChange([...selectedTypes, type]);
    }
  };

  const totalCount = counts
    ? Object.values(counts).reduce((a, b) => a + (b || 0), 0)
    : undefined;

  return (
    <div className="flex flex-wrap gap-2" role="group" aria-label="Filter by type">
      {/* All chip */}
      <button
        onClick={handleAllClick}
        className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
          isAllSelected
            ? TYPE_COLORS.All.selected
            : TYPE_COLORS.All.base
        }`}
        aria-pressed={isAllSelected}
      >
        All
        {totalCount !== undefined && (
          <span className="ml-1.5 text-xs opacity-70">
            ({totalCount})
          </span>
        )}
      </button>

      {/* Type chips */}
      {ALL_TYPES.map((type) => {
        const isSelected = selectedTypes.includes(type);
        const count = counts?.[type];
        const colors = TYPE_COLORS[type];

        return (
          <button
            key={type}
            onClick={() => handleTypeClick(type)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
              isSelected ? colors.selected : colors.base
            }`}
            aria-pressed={isSelected}
          >
            {type}
            {count !== undefined && (
              <span className="ml-1.5 text-xs opacity-70">({count})</span>
            )}
          </button>
        );
      })}
    </div>
  );
};

export default TypeFilter;
