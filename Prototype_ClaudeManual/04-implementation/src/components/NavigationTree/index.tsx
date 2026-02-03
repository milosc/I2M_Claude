import React, { useState, useMemo, useCallback, useEffect } from 'react';
import type { NavigationTreeProps, TreeNode, Stage } from '../../types/navigation';

export function NavigationTree({
  items,
  selectedId,
  stageFilter = [],
  searchQuery = '',
  showCountBadges = false,
  favorites = [],
  onSelect,
  onToggleFavorite,
  onExpandChange,
  loading = false,
  error,
}: NavigationTreeProps) {
  const [expandedKeys, setExpandedKeys] = useState<Set<string>>(new Set());
  const [nodesToExpand, setNodesToExpand] = useState<string[]>([]);

  // Filter tree by stage - checks stages[] array if available (PF-003)
  const filterByStage = useCallback((nodes: TreeNode[], stages: Stage[]): TreeNode[] => {
    if (stages.length === 0) return nodes;

    return nodes
      .map((node) => {
        // Check if any of the node's stages match the filter
        // Use stages[] if available, otherwise fall back to stage
        const nodeStages = node.stages || (node.stage ? [node.stage] : []);
        const matchesStage = nodeStages.length === 0 || nodeStages.some(s => stages.includes(s));

        const filteredChildren = node.children
          ? filterByStage(node.children, stages)
          : [];

        return {
          ...node,
          children: filteredChildren,
          count: filteredChildren.length,
        };
      })
      .filter((node) => {
        const nodeStages = node.stages || (node.stage ? [node.stage] : []);
        const matchesStage = nodeStages.length === 0 || nodeStages.some(s => stages.includes(s));
        return matchesStage || (node.children && node.children.length > 0);
      });
  }, []);

  // Filter tree by search query
  const searchTree = useCallback((nodes: TreeNode[], query: string): { filtered: TreeNode[], toExpand: string[] } => {
    if (!query) return { filtered: nodes, toExpand: [] };

    const lowerQuery = query.toLowerCase();
    const result: TreeNode[] = [];
    const toExpand: string[] = [];

    for (const node of nodes) {
      const matchesLabel = node.label.toLowerCase().includes(lowerQuery);
      const matchesDescription = node.description?.toLowerCase().includes(lowerQuery);
      const matchesPath = node.path?.toLowerCase().includes(lowerQuery);

      const childResult = node.children
        ? searchTree(node.children, query)
        : { filtered: [], toExpand: [] };

      if (matchesLabel || matchesDescription || matchesPath || childResult.filtered.length > 0) {
        result.push({
          ...node,
          children: childResult.filtered,
        });

        // Mark for expansion
        if (node.children && node.children.length > 0) {
          toExpand.push(node.id, ...childResult.toExpand);
        }
      }
    }

    return { filtered: result, toExpand };
  }, []);

  // Apply filters
  const { filteredItems, toExpand } = useMemo(() => {
    let result = items;

    if (stageFilter.length > 0) {
      result = filterByStage(result, stageFilter);
    }

    let nodesToExpand: string[] = [];
    if (searchQuery) {
      const searchResult = searchTree(result, searchQuery);
      nodesToExpand = searchResult.toExpand;
      result = searchResult.filtered;
    }

    return { filteredItems: result, toExpand: nodesToExpand };
  }, [items, stageFilter, searchQuery, filterByStage, searchTree]);

  // Auto-expand nodes based on search
  useEffect(() => {
    if (toExpand.length > 0) {
      setExpandedKeys(new Set(toExpand));
    }
  }, [toExpand]);

  // Toggle expansion
  const toggleExpand = useCallback((nodeId: string) => {
    setExpandedKeys((prev) => {
      const next = new Set(prev);
      const isExpanding = !next.has(nodeId);

      if (next.has(nodeId)) {
        next.delete(nodeId);
      } else {
        next.add(nodeId);
      }

      onExpandChange?.(nodeId, isExpanding);
      return next;
    });
  }, [onExpandChange]);

  // Render tree items recursively
  const renderTreeItems = (nodes: TreeNode[], level: number = 0): React.ReactNode => {
    return nodes.map((node) => {
      const isFavorite = favorites.includes(node.id);
      const isSelected = selectedId === node.id;
      const isExpanded = expandedKeys.has(node.id);
      const hasChildren = node.children && node.children.length > 0;

      return (
        <li
          key={node.id}
          role="treeitem"
          aria-selected={isSelected}
          aria-expanded={hasChildren ? isExpanded : undefined}
          style={{ listStyle: 'none', paddingLeft: level > 0 ? '1rem' : 0 }}
        >
          <div
            onClick={() => {
              if (hasChildren) {
                toggleExpand(node.id);
              } else {
                onSelect(node.id);
              }
            }}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                if (hasChildren) {
                  toggleExpand(node.id);
                } else {
                  onSelect(node.id);
                }
              }
            }}
            tabIndex={0}
            style={{
              padding: '0.5rem',
              cursor: 'pointer',
              backgroundColor: isSelected ? '#dbeafe' : 'transparent',
              fontWeight: isSelected ? 600 : 400,
            }}
          >
            {isFavorite && <span>⭐ </span>}
            <span>{node.label}</span>
            {showCountBadges && node.count !== undefined && node.count > 0 && (
              <span style={{ marginLeft: '0.5rem', fontSize: '0.875rem', color: '#6b7280' }}>
                {node.count}
              </span>
            )}
          </div>
          {hasChildren && isExpanded && (
            <ul role="group" style={{ paddingLeft: 0 }}>
              {renderTreeItems(node.children!, level + 1)}
            </ul>
          )}
        </li>
      );
    });
  };

  // Loading state
  if (loading) {
    return <div style={{ padding: '1rem' }}>Loading...</div>;
  }

  // Error state
  if (error) {
    return <div style={{ padding: '1rem' }}>Failed to load tree: {error}</div>;
  }

  // Empty state
  if (filteredItems.length === 0) {
    return <div style={{ padding: '1rem' }}>No items found</div>;
  }

  return (
    <div style={{ padding: '1rem', fontFamily: 'monospace', fontSize: '0.875rem' }}>
      <ul role="tree" aria-label="Framework navigation" style={{ paddingLeft: 0 }}>
        {renderTreeItems(filteredItems)}
      </ul>
    </div>
  );
}

export { NavigationTree as default };
