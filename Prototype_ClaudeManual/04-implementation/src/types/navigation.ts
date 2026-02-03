export type Stage =
  | 'discovery'
  | 'prototype'
  | 'productspecs'
  | 'solarch'
  | 'implementation'
  | 'utility'
  | 'security'
  | 'grc';

export interface TreeNode {
  id: string;
  label: string;
  type: 'category' | 'skill' | 'command' | 'agent' | 'rule' | 'hook';
  stage?: Stage;
  stages?: Stage[];  // All stages (custom + original) for filtering (PF-003)
  path?: string;
  description?: string;
  children?: TreeNode[];
  count?: number;
  isFavorite?: boolean;
}

export interface NavigationTreeProps {
  /** Tree data structure */
  items: TreeNode[];
  /** Currently selected item ID */
  selectedId?: string;
  /** Active stage filter (Discovery, Prototype, etc.) */
  stageFilter?: Stage[];
  /** Search query for filtering items */
  searchQuery?: string;
  /** Show/hide count badges */
  showCountBadges?: boolean;
  /** Favorites list IDs */
  favorites?: string[];
  /** Selection handler */
  onSelect: (itemId: string) => void;
  /** Favorite toggle handler */
  onToggleFavorite?: (itemId: string) => void;
  /** Collapse/expand handler */
  onExpandChange?: (itemId: string, expanded: boolean) => void;
  /** Loading state */
  loading?: boolean;
  /** Error state */
  error?: string;
}
