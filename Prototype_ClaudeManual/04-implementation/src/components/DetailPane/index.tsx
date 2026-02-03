import React, { useState, useEffect } from 'react';
import { MarkdownRenderer } from '../MarkdownRenderer';
import { FrontmatterDisplay } from '../FrontmatterDisplay';
import { TagDisplay } from '../TagDisplay';
import { TagInput } from '../TagInput';
import { StageSelector } from '../StageSelector';
import { Stage as StageEnum } from '@/types';
import {
  getComponentTags,
  addComponentTag,
  removeComponentTag,
  getAllUserTags,
  getComponentStages,
  setComponentStages,
} from '@/lib/localStorage';

export type TabId = 'purpose' | 'examples' | 'options' | 'workflow' | 'traceability';
export type Stage = 'discovery' | 'prototype' | 'productspecs' | 'solarch' | 'implementation';

export interface CodeExample {
  title: string;
  language: 'bash' | 'typescript' | 'json' | 'yaml';
  code: string;
}

export interface OptionField {
  parameter: string;
  type: string;
  required: boolean;
  defaultValue?: string;
  description: string;
}

export interface WorkflowDiagram {
  format: 'mermaid' | 'plantuml';
  code: string;
  description?: string;
}

export interface TraceabilityLink {
  type: 'input' | 'output' | 'dependency' | 'related';
  id: string;
  label: string;
}

export interface FrontmatterAttributes {
  model?: string | null;
  context?: string | null;
  agent?: string | null;
  allowed_tools?: string[];
  skills_required?: string[];
  checkpoint?: number | null;
  loads_skills?: string[];
  spawned_by?: string[];
  orchestrates_agents?: string[];
  invokes_skills?: string[];
  argument_hint?: string | null;
  color?: string;
  [key: string]: unknown;
}

export interface ComponentDetail {
  id: string;
  name: string;
  type: 'skill' | 'command' | 'agent' | 'rule' | 'hook';
  stage: Stage;
  path: string;
  description: string;
  /** Frontmatter attributes parsed from source file */
  frontmatter?: FrontmatterAttributes;
  /** Raw markdown content (everything after frontmatter) */
  rawContent?: string;
  purpose?: string;
  examples?: CodeExample[];
  options?: OptionField[];
  workflow?: WorkflowDiagram;
  traceability?: TraceabilityLink[];
  /** User-defined tags (PF-002) */
  tags?: string[];
  isFavorite: boolean;
}

export interface DetailPaneProps {
  /** Selected item data */
  item: ComponentDetail | null;
  /** Loading state */
  loading?: boolean;
  /** Error state */
  error?: string;
  /** Active tab */
  activeTab?: TabId;
  /** Tab change handler */
  onTabChange?: (tabId: TabId) => void;
  /** Copy path handler */
  onCopyPath?: (path: string) => void;
  /** Favorite toggle handler */
  onToggleFavorite?: (itemId: string) => void;
  /** Show/hide specific tabs */
  visibleTabs?: TabId[];
  /** Callback when stages are modified (PF-003) */
  onStagesUpdated?: () => void;
}

function getVisibleTabs(item: ComponentDetail, visibleTabs?: TabId[]): TabId[] {
  const baseTabs: TabId[] = ['purpose'];

  if (item.examples?.length) {
    baseTabs.push('examples');
  }

  if (item.options?.length) {
    baseTabs.push('options');
  }

  if (item.workflow) {
    baseTabs.push('workflow');
  }

  if (item.traceability?.length && item.type === 'skill') {
    baseTabs.push('traceability');
  }

  if (visibleTabs) {
    return baseTabs.filter(tab => visibleTabs.includes(tab));
  }

  return baseTabs;
}

export const DetailPane: React.FC<DetailPaneProps> = ({
  item,
  loading = false,
  error,
  activeTab: controlledActiveTab,
  onTabChange,
  onCopyPath,
  onToggleFavorite,
  visibleTabs,
  onStagesUpdated,
}) => {
  const [internalActiveTab, setInternalActiveTab] = useState<TabId>('purpose');
  const activeTab = controlledActiveTab ?? internalActiveTab;

  // Tag state management (PF-002)
  const [componentTags, setComponentTags] = useState<string[]>([]);
  const [allTags, setAllTags] = useState<string[]>([]);

  // Stage state management (PF-003)
  const [componentStages, setComponentStagesState] = useState<StageEnum[]>([]);

  // Load tags and stages when item changes
  useEffect(() => {
    if (item) {
      const tags = getComponentTags(item.id);
      setComponentTags(tags);
      setAllTags(getAllUserTags());

      const stages = getComponentStages(item.id);
      setComponentStagesState(stages);
    }
  }, [item?.id]);

  const handleAddTag = (tag: string) => {
    if (item) {
      addComponentTag(item.id, tag);
      setComponentTags(getComponentTags(item.id));
      setAllTags(getAllUserTags());
    }
  };

  const handleRemoveTag = (tag: string) => {
    if (item) {
      removeComponentTag(item.id, tag);
      setComponentTags(getComponentTags(item.id));
      setAllTags(getAllUserTags());
    }
  };

  const handleStagesChange = (stages: StageEnum[]) => {
    if (item) {
      setComponentStages(item.id, stages);
      setComponentStagesState(stages);
      // Notify parent to refresh tree (PF-003)
      onStagesUpdated?.();
    }
  };

  if (loading) {
    return (
      <div className="p-6 text-center">
        <p className="text-gray-600">Loading...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-center">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!item) {
    return (
      <div className="p-6 text-center">
        <p className="text-gray-500">Select a component to view details</p>
      </div>
    );
  }

  const tabs = getVisibleTabs(item, visibleTabs);

  const handleTabClick = (tabId: TabId) => {
    setInternalActiveTab(tabId);
    onTabChange?.(tabId);
  };

  return (
    <div className="detail-pane bg-white h-full flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">{item.name}</h2>
            <p className="text-gray-600 text-sm">{item.description}</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => onCopyPath?.(item.path)}
              className="px-3 py-1.5 text-sm bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Copy Path
            </button>
            <button
              onClick={() => onToggleFavorite?.(item.id)}
              className="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
            >
              {item.isFavorite ? 'Remove from Favorites' : 'Add to Favorites'}
            </button>
          </div>
        </div>

        {/* Type Badge */}
        <div className="flex gap-2 mb-3">
          <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded">{item.type}</span>
        </div>

        {/* Stage Selector (PF-003) */}
        <div className="mb-3">
          <StageSelector
            selectedStages={componentStages}
            originalStage={item.stage}
            onStagesChange={handleStagesChange}
            label="Stages"
          />
        </div>

        {/* Tags Section (PF-002) */}
        <div className="mb-3">
          <div className="flex items-center gap-3 flex-wrap">
            <span className="text-xs font-medium text-gray-500">Tags:</span>
            {componentTags.length > 0 ? (
              <TagDisplay
                tags={componentTags}
                onRemove={handleRemoveTag}
              />
            ) : (
              <span className="text-xs text-gray-400 italic">No tags</span>
            )}
          </div>
          <div className="mt-2">
            <TagInput
              currentTags={componentTags}
              suggestedTags={allTags}
              onAddTag={handleAddTag}
              placeholder="Add a tag..."
              label="Add tag"
            />
          </div>
        </div>

        {/* File Path */}
        <p className="text-xs text-gray-500 font-mono">{item.path}</p>

        {/* Frontmatter Attributes */}
        {item.frontmatter && (
          <FrontmatterDisplay frontmatter={item.frontmatter} type={item.type} />
        )}
      </div>

      {/* Tabs */}
      <div role="tablist" className="flex border-b border-gray-200 px-6">
        {tabs.map((tabId) => (
          <button
            key={tabId}
            role="tab"
            aria-selected={activeTab === tabId}
            onClick={() => handleTabClick(tabId)}
            className={`
              px-4 py-3 text-sm font-medium border-b-2 transition-colors
              ${activeTab === tabId
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-600 hover:text-gray-900'
              }
            `}
          >
            {tabId.charAt(0).toUpperCase() + tabId.slice(1)}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="flex-1 overflow-auto p-6">
        {activeTab === 'purpose' && (
          <MarkdownRenderer content={item.rawContent || item.purpose || 'No content available'} />
        )}

        {activeTab === 'examples' && item.examples && (
          <div className="space-y-6">
            {item.examples.map((example, index) => (
              <div key={index}>
                <h3 className="text-lg font-semibold mb-2">{example.title}</h3>
                <MarkdownRenderer content={`\`\`\`${example.language}\n${example.code}\n\`\`\``} />
              </div>
            ))}
          </div>
        )}

        {activeTab === 'options' && item.options && (
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-2 px-4 text-sm font-semibold">Parameter</th>
                  <th className="text-left py-2 px-4 text-sm font-semibold">Type</th>
                  <th className="text-left py-2 px-4 text-sm font-semibold">Required</th>
                  <th className="text-left py-2 px-4 text-sm font-semibold">Default</th>
                  <th className="text-left py-2 px-4 text-sm font-semibold">Description</th>
                </tr>
              </thead>
              <tbody>
                {item.options.map((option, index) => (
                  <tr key={index} className="border-b border-gray-100">
                    <td className="py-2 px-4 text-sm font-mono">{option.parameter}</td>
                    <td className="py-2 px-4 text-sm font-mono text-gray-600">{option.type}</td>
                    <td className="py-2 px-4 text-sm">{option.required ? 'Yes' : 'No'}</td>
                    <td className="py-2 px-4 text-sm font-mono text-gray-600">{option.defaultValue || '-'}</td>
                    <td className="py-2 px-4 text-sm">{option.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'workflow' && item.workflow && (
          <div>
            {item.workflow.description && (
              <p className="mb-4 text-gray-700">{item.workflow.description}</p>
            )}
            <MarkdownRenderer
              content={`\`\`\`${item.workflow.format}\n${item.workflow.code}\n\`\`\``}
              enableDiagrams={true}
            />
          </div>
        )}

        {activeTab === 'traceability' && item.traceability && (
          <div className="space-y-4">
            {['input', 'output', 'dependency', 'related'].map((linkType) => {
              const links = item.traceability!.filter(link => link.type === linkType);
              if (links.length === 0) return null;

              return (
                <div key={linkType}>
                  <h3 className="text-sm font-semibold text-gray-700 mb-2 uppercase">
                    {linkType}s
                  </h3>
                  <ul className="space-y-1">
                    {links.map((link, index) => (
                      <li key={index}>
                        <button className="text-blue-600 hover:text-blue-800 text-sm">
                          {link.id} - {link.label}
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default DetailPane;
