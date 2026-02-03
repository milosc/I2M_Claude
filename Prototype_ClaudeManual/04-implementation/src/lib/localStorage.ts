import { UserPreferences, Theme, Stage, EntityType } from '@/types'

const STORAGE_KEY = 'claudemanual-preferences'

const defaultPreferences: UserPreferences = {
  theme: Theme.System,
  favorites: [],
  collapsed_nodes: [],
  last_viewed: null,
  search_history: [],
  stage_filter: [],
  type_filter: [],
  component_tags: {},  // PF-002: User-added tags per component
  tag_filter: [],      // PF-002: Active tag filters in search
  component_stages: {},  // PF-003: User-modified stages per component
}

/**
 * Get user preferences from localStorage
 */
export function getPreferences(): UserPreferences {
  if (typeof window === 'undefined') {
    return defaultPreferences
  }

  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (!stored) {
      return defaultPreferences
    }

    const parsed = JSON.parse(stored)
    return { ...defaultPreferences, ...parsed }
  } catch (error) {
    console.error('Failed to parse preferences:', error)
    return defaultPreferences
  }
}

/**
 * Save user preferences to localStorage
 */
export function savePreferences(preferences: Partial<UserPreferences>): void {
  if (typeof window === 'undefined') {
    return
  }

  try {
    const current = getPreferences()
    const updated = { ...current, ...preferences }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
  } catch (error) {
    console.error('Failed to save preferences:', error)
  }
}

/**
 * Add item to favorites
 */
export function addFavorite(id: string): void {
  const prefs = getPreferences()
  if (!prefs.favorites.includes(id)) {
    savePreferences({ favorites: [...prefs.favorites, id] })
  }
}

/**
 * Remove item from favorites
 */
export function removeFavorite(id: string): void {
  const prefs = getPreferences()
  savePreferences({ favorites: prefs.favorites.filter(fav => fav !== id) })
}

/**
 * Toggle favorite status
 */
export function toggleFavorite(id: string): void {
  const prefs = getPreferences()
  if (prefs.favorites.includes(id)) {
    removeFavorite(id)
  } else {
    addFavorite(id)
  }
}

/**
 * Check if item is favorited
 */
export function isFavorited(id: string): boolean {
  const prefs = getPreferences()
  return prefs.favorites.includes(id)
}

/**
 * Add search query to history
 */
export function addSearchHistory(query: string): void {
  const prefs = getPreferences()
  const history = [query, ...prefs.search_history.filter(q => q !== query)].slice(0, 10)
  savePreferences({ search_history: history })
}

/**
 * Clear search history
 */
export function clearSearchHistory(): void {
  savePreferences({ search_history: [] })
}

/**
 * Toggle collapsed node
 */
export function toggleCollapsedNode(nodeId: string): void {
  const prefs = getPreferences()
  const collapsed = prefs.collapsed_nodes.includes(nodeId)
    ? prefs.collapsed_nodes.filter(id => id !== nodeId)
    : [...prefs.collapsed_nodes, nodeId]
  savePreferences({ collapsed_nodes: collapsed })
}

/**
 * Set last viewed item
 */
export function setLastViewed(id: string): void {
  savePreferences({ last_viewed: id })
}

/**
 * Set theme
 */
export function setTheme(theme: Theme): void {
  savePreferences({ theme })
}

/**
 * Toggle stage filter
 */
export function toggleStageFilter(stage: Stage): void {
  const prefs = getPreferences()
  const filters = prefs.stage_filter.includes(stage)
    ? prefs.stage_filter.filter(s => s !== stage)
    : [...prefs.stage_filter, stage]
  savePreferences({ stage_filter: filters })
}

/**
 * Toggle type filter
 */
export function toggleTypeFilter(type: EntityType): void {
  const prefs = getPreferences()
  const filters = prefs.type_filter.includes(type)
    ? prefs.type_filter.filter(t => t !== type)
    : [...prefs.type_filter, type]
  savePreferences({ type_filter: filters })
}

/**
 * Clear all filters
 */
export function clearFilters(): void {
  savePreferences({ stage_filter: [], type_filter: [], tag_filter: [] })
}

// ============================================================================
// TAG MANAGEMENT (PF-002: Tagging Feature)
// ============================================================================

/**
 * Get tags for a specific component
 */
export function getComponentTags(componentId: string): string[] {
  const prefs = getPreferences()
  return prefs.component_tags[componentId] || []
}

/**
 * Add a tag to a component
 */
export function addComponentTag(componentId: string, tag: string): void {
  const prefs = getPreferences()
  const currentTags = prefs.component_tags[componentId] || []
  if (!currentTags.includes(tag)) {
    savePreferences({
      component_tags: {
        ...prefs.component_tags,
        [componentId]: [...currentTags, tag],
      },
    })
  }
}

/**
 * Remove a tag from a component
 */
export function removeComponentTag(componentId: string, tag: string): void {
  const prefs = getPreferences()
  const currentTags = prefs.component_tags[componentId] || []
  savePreferences({
    component_tags: {
      ...prefs.component_tags,
      [componentId]: currentTags.filter((t) => t !== tag),
    },
  })
}

/**
 * Get all unique tags across all components
 */
export function getAllUserTags(): string[] {
  const prefs = getPreferences()
  const allTags = Object.values(prefs.component_tags).flat()
  return [...new Set(allTags)].sort()
}

/**
 * Toggle tag filter
 */
export function toggleTagFilter(tag: string): void {
  const prefs = getPreferences()
  const filters = prefs.tag_filter.includes(tag)
    ? prefs.tag_filter.filter((t) => t !== tag)
    : [...prefs.tag_filter, tag]
  savePreferences({ tag_filter: filters })
}

/**
 * Set tag filters (replace all)
 */
export function setTagFilter(tags: string[]): void {
  savePreferences({ tag_filter: tags })
}

/**
 * Clear tag filters
 */
export function clearTagFilter(): void {
  savePreferences({ tag_filter: [] })
}

// ============================================================================
// STAGE MANAGEMENT (PF-003: Multi-Stage Feature)
// ============================================================================

/**
 * Get stages for a specific component (user-modified)
 * Returns empty array if no custom stages set (use original stage)
 */
export function getComponentStages(componentId: string): Stage[] {
  const prefs = getPreferences()
  return prefs.component_stages[componentId] || []
}

/**
 * Set stages for a component (replaces all)
 */
export function setComponentStages(componentId: string, stages: Stage[]): void {
  const prefs = getPreferences()
  if (stages.length === 0) {
    // Remove entry if empty
    const { [componentId]: _, ...rest } = prefs.component_stages
    savePreferences({ component_stages: rest })
  } else {
    savePreferences({
      component_stages: {
        ...prefs.component_stages,
        [componentId]: stages,
      },
    })
  }
}

/**
 * Add a stage to a component
 */
export function addComponentStage(componentId: string, stage: Stage): void {
  const prefs = getPreferences()
  const currentStages = prefs.component_stages[componentId] || []
  if (!currentStages.includes(stage)) {
    savePreferences({
      component_stages: {
        ...prefs.component_stages,
        [componentId]: [...currentStages, stage],
      },
    })
  }
}

/**
 * Remove a stage from a component
 */
export function removeComponentStage(componentId: string, stage: Stage): void {
  const prefs = getPreferences()
  const currentStages = prefs.component_stages[componentId] || []
  const newStages = currentStages.filter((s) => s !== stage)
  if (newStages.length === 0) {
    const { [componentId]: _, ...rest } = prefs.component_stages
    savePreferences({ component_stages: rest })
  } else {
    savePreferences({
      component_stages: {
        ...prefs.component_stages,
        [componentId]: newStages,
      },
    })
  }
}

/**
 * Toggle a stage for a component
 */
export function toggleComponentStage(componentId: string, stage: Stage): void {
  const prefs = getPreferences()
  const currentStages = prefs.component_stages[componentId] || []
  if (currentStages.includes(stage)) {
    removeComponentStage(componentId, stage)
  } else {
    addComponentStage(componentId, stage)
  }
}

/**
 * Check if component has custom stages set
 */
export function hasCustomStages(componentId: string): boolean {
  const prefs = getPreferences()
  return (prefs.component_stages[componentId]?.length || 0) > 0
}

/**
 * Reset preferences to defaults
 */
export function resetPreferences(): void {
  if (typeof window === 'undefined') {
    return
  }

  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch (error) {
    console.error('Failed to reset preferences:', error)
  }
}
