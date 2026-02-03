import React from 'react';
import type { FrontmatterAttributes } from '../DetailPane';

interface FrontmatterDisplayProps {
  /** Frontmatter attributes object */
  frontmatter: FrontmatterAttributes;
  /** Component type for display ordering */
  type: 'skill' | 'command' | 'agent' | 'rule' | 'hook';
}

const DISPLAY_ORDER: Record<string, string[]> = {
  skill: ['model', 'context', 'agent', 'allowed_tools', 'skills_required'],
  command: ['model', 'argument_hint', 'allowed_tools', 'invokes_skills', 'orchestrates_agents'],
  agent: ['model', 'checkpoint', 'color', 'loads_skills', 'spawned_by'],
  rule: ['model'],
  hook: ['model'],
};

export const FrontmatterDisplay: React.FC<FrontmatterDisplayProps> = ({ frontmatter, type }) => {
  const order = DISPLAY_ORDER[type] || Object.keys(frontmatter);

  // Filter to only show keys that exist in frontmatter
  const keysToDisplay = order.filter(key => key in frontmatter);

  // Add any remaining keys not in the predefined order
  const remainingKeys = Object.keys(frontmatter).filter(
    key => !order.includes(key) && !['name', 'description'].includes(key)
  );
  const allKeys = [...keysToDisplay, ...remainingKeys];

  const renderValue = (value: unknown): React.ReactNode => {
    if (value === null || value === undefined) {
      return <span className="text-gray-400 italic">null</span>;
    }
    if (Array.isArray(value)) {
      if (value.length === 0) {
        return <span className="text-gray-400 italic">[]</span>;
      }
      return (
        <div className="flex flex-wrap gap-1">
          {value.map((v, i) => (
            <span
              key={i}
              className="px-1.5 py-0.5 bg-blue-50 text-blue-700 text-xs rounded font-mono"
            >
              {String(v)}
            </span>
          ))}
        </div>
      );
    }
    if (typeof value === 'boolean') {
      return (
        <span className={value ? 'text-green-600' : 'text-gray-400'}>
          {String(value)}
        </span>
      );
    }
    if (typeof value === 'number') {
      return <span className="text-purple-600 font-mono">{value}</span>;
    }
    return <span className="text-gray-900">{String(value)}</span>;
  };

  if (allKeys.length === 0) {
    return null;
  }

  return (
    <div className="border border-gray-200 rounded-lg p-4 mt-4 bg-gray-50">
      <h3 className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wide">
        Frontmatter
      </h3>
      <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-3 text-sm">
        {allKeys.map((key) => {
          const value = frontmatter[key];
          return (
            <div key={key} className="flex flex-col">
              <dt className="text-gray-500 font-medium text-xs uppercase tracking-wide mb-0.5">
                {key.replace(/_/g, ' ')}
              </dt>
              <dd className="text-gray-900">{renderValue(value)}</dd>
            </div>
          );
        })}
      </dl>
    </div>
  );
};

export default FrontmatterDisplay;
