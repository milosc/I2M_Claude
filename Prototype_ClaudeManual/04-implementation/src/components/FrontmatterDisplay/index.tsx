import React, { useState } from 'react';
import type { FrontmatterAttributes } from '../DetailPane';

interface HookEntry {
  type: string;
  command: string;
}

interface HookMatcher {
  matcher?: string;
  once?: boolean;
  hooks: HookEntry[];
}

interface ParsedHooks {
  [key: string]: HookMatcher[] | undefined;
}

interface FrontmatterDisplayProps {
  /** Frontmatter attributes object */
  frontmatter: FrontmatterAttributes;
  /** Component type for display ordering */
  type: 'skill' | 'command' | 'agent' | 'rule' | 'hook';
}

const DISPLAY_ORDER: Record<string, string[]> = {
  skill: ['model', 'context', 'agent', 'allowed_tools', 'skills_required'],
  command: ['model', 'argument_hint', 'allowed_tools', 'skills_required', 'skills_optional', 'orchestrates_agents'],
  agent: ['model', 'checkpoint', 'color', 'loads_skills', 'spawned_by'],
  rule: ['model'],
  hook: ['model'],
};

// Keys to exclude from main display (shown in separate sections)
const EXCLUDED_KEYS = ['name', 'description', 'hooks'];

export const FrontmatterDisplay: React.FC<FrontmatterDisplayProps> = ({ frontmatter, type }) => {
  const [hooksExpanded, setHooksExpanded] = useState(false);
  const order = DISPLAY_ORDER[type] || Object.keys(frontmatter);

  // Filter to only show keys that exist in frontmatter (excluding hooks)
  const keysToDisplay = order.filter(key => key in frontmatter && !EXCLUDED_KEYS.includes(key));

  // Add any remaining keys not in the predefined order (excluding hooks)
  const remainingKeys = Object.keys(frontmatter).filter(
    key => !order.includes(key) && !EXCLUDED_KEYS.includes(key)
  );
  const allKeys = [...keysToDisplay, ...remainingKeys];

  // Get hooks data
  const hooks = frontmatter.hooks as ParsedHooks | undefined;

  const renderValue = (value: unknown, key?: string): React.ReactNode => {
    if (value === null || value === undefined) {
      return <span className="text-gray-400 italic">null</span>;
    }
    if (Array.isArray(value)) {
      if (value.length === 0) {
        return <span className="text-gray-400 italic">[]</span>;
      }
      // Use different colors for required vs optional skills
      const isRequired = key === 'skills_required';
      const isOptional = key === 'skills_optional';
      const badgeClass = isRequired
        ? 'px-1.5 py-0.5 bg-green-50 text-green-700 text-xs rounded font-mono border border-green-200'
        : isOptional
        ? 'px-1.5 py-0.5 bg-gray-50 text-gray-600 text-xs rounded font-mono border border-gray-200'
        : 'px-1.5 py-0.5 bg-blue-50 text-blue-700 text-xs rounded font-mono';
      return (
        <div className="flex flex-wrap gap-1">
          {value.map((v, i) => (
            <span key={i} className={badgeClass}>
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

  const renderHooks = (hooks: ParsedHooks) => {
    return (
      <div className="space-y-3">
        {Object.entries(hooks).map(([hookType, matchers]) => (
          <div key={hookType} className="border-l-2 border-purple-300 pl-3">
            <div className="font-medium text-purple-700 text-sm mb-1">{hookType}</div>
            {matchers?.map((matcher, mIdx) => (
              <div key={mIdx} className="ml-2 mb-2">
                {matcher.matcher && (
                  <div className="text-xs text-gray-500">
                    <span className="font-medium">matcher:</span>{' '}
                    <code className="bg-gray-100 px-1 rounded">{matcher.matcher}</code>
                    {matcher.once && <span className="ml-2 text-orange-600">(once)</span>}
                  </div>
                )}
                <div className="mt-1 space-y-1">
                  {matcher.hooks.map((hook, hIdx) => (
                    <div key={hIdx} className="text-xs bg-gray-100 rounded p-2">
                      <span className="text-gray-500">type:</span>{' '}
                      <span className="text-blue-600">{hook.type}</span>
                      {hook.command && (
                        <div className="mt-1 font-mono text-gray-700 break-all text-[11px]">
                          {hook.command}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ))}
      </div>
    );
  };

  if (allKeys.length === 0 && !hooks) {
    return null;
  }

  return (
    <div className="border border-gray-200 rounded-lg p-4 mt-4 bg-gray-50">
      <h3 className="text-sm font-semibold text-gray-700 mb-3 uppercase tracking-wide">
        Frontmatter
      </h3>
      {allKeys.length > 0 && (
        <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-3 text-sm">
          {allKeys.map((key) => {
            const value = frontmatter[key];
            return (
              <div key={key} className="flex flex-col">
                <dt className="text-gray-500 font-medium text-xs uppercase tracking-wide mb-0.5">
                  {key.replace(/_/g, ' ')}
                </dt>
                <dd className="text-gray-900">{renderValue(value, key)}</dd>
              </div>
            );
          })}
        </dl>
      )}

      {/* Collapsible Hooks Section */}
      {hooks && Object.keys(hooks).length > 0 && (
        <div className="mt-4 border-t border-gray-200 pt-3">
          <button
            onClick={() => setHooksExpanded(!hooksExpanded)}
            className="flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
          >
            <svg
              className={`w-4 h-4 transition-transform ${hooksExpanded ? 'rotate-90' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
            <span className="uppercase tracking-wide text-xs">Hooks</span>
            <span className="text-xs text-gray-400">({Object.keys(hooks).length} type{Object.keys(hooks).length !== 1 ? 's' : ''})</span>
          </button>
          {hooksExpanded && (
            <div className="mt-3 pl-6">
              {renderHooks(hooks)}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default FrontmatterDisplay;
