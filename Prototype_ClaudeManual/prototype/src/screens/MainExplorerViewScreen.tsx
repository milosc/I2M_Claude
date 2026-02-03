import { useState, useEffect, useMemo } from 'react';
import { View, Flex, Button, TextField, Switch, Text } from '@adobe/react-spectrum';
import { NavigationTree } from '@/components/NavigationTree';
import { DetailPane } from '@/components/DetailPane';
import { StageFilterDropdown } from '@/components/StageFilterDropdown';
import Star from '@spectrum-icons/workflow/Star';
import Search from '@spectrum-icons/workflow/Search';
import { useNavigate } from 'react-router-dom';
import { useLocalStorage } from '@/hooks/useLocalStorage';
import { useAPICache } from '@/hooks/useAPICache';
import type { Skill, Command, Agent, Rule, Hook, UserPreferences } from '@/types';

/**
 * Main Explorer View Screen (SCR-001)
 *
 * Primary interface for framework exploration with dual-pane master-detail layout.
 *
 * Features:
 * - Hierarchical navigation tree (115+ items: skills, commands, agents, rules, hooks)
 * - Tabbed detail pane with Purpose/Examples/Options/Workflow/Traceability
 * - Stage filtering (Discovery, Prototype, Implementation, etc.)
 * - Favorites bookmarking with localStorage persistence
 * - Light/dark theme toggle
 * - Responsive layout (desktop: dual-pane, mobile: drawer navigation)
 *
 * Traceability:
 * - Screen: SCR-001
 * - Discovery: S-1.1
 * - JTBD: JTBD-1.1, JTBD-1.2, JTBD-1.4, JTBD-1.5, JTBD-1.6, JTBD-1.7
 * - Requirements: REQ-021, REQ-022, REQ-023, REQ-024, REQ-025, REQ-026
 * - Pain Points: PP-1.1, PP-1.2, PP-1.4, PP-1.6
 * - Client Facts: CF-006, CF-008, CF-013, CF-014, CF-016
 *
 * Assembly-First: Uses Adobe Spectrum React components (View, Flex, Button, TextField, Switch)
 * Combined with aggregate components (NavigationTree, DetailPane, StageFilterDropdown)
 */
export function MainExplorerViewScreen() {
  const navigate = useNavigate();

  // ========================================
  // STATE MANAGEMENT
  // ========================================

  // User preferences (localStorage)
  const [preferences, setPreferences] = useLocalStorage<UserPreferences>('userPreferences', {
    theme: 'system',
    favorites: [],
    collapsed_nodes: [],
    last_viewed: null,
    search_history: [],
    stage_filter: [],
    type_filter: [],
  });

  // API data (with sessionStorage caching)
  const {
    data: skills,
    isLoading: skillsLoading,
    error: skillsError,
    refetch: refetchSkills,
  } = useAPICache<Skill[]>('/api/skills', 'skills');

  const {
    data: commands,
    isLoading: commandsLoading,
    error: commandsError,
  } = useAPICache<Command[]>('/api/commands', 'commands');

  const {
    data: agents,
    isLoading: agentsLoading,
    error: agentsError,
  } = useAPICache<Agent[]>('/api/agents', 'agents');

  const {
    data: rules,
    isLoading: rulesLoading,
  } = useAPICache<Rule[]>('/api/rules', 'rules');

  const {
    data: hooks,
    isLoading: hooksLoading,
  } = useAPICache<Hook[]>('/api/hooks', 'hooks');

  // Local state
  const [selectedItem, setSelectedItem] = useState<Skill | Command | Agent | Rule | Hook | null>(null);
  const [expandedNodes, setExpandedNodes] = useState<string[]>([]);
  const [isDarkMode, setIsDarkMode] = useState<boolean>(
    preferences.theme === 'dark' || (preferences.theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)
  );

  // ========================================
  // DERIVED STATE (Memoized)
  // ========================================

  const allItems = useMemo(() => {
    return [
      ...(skills || []),
      ...(commands || []),
      ...(agents || []),
      ...(rules || []),
      ...(hooks || []),
    ];
  }, [skills, commands, agents, rules, hooks]);

  const filteredItems = useMemo(() => {
    if (preferences.stage_filter.length === 0) {
      return allItems;
    }
    return allItems.filter((item) => preferences.stage_filter.includes(item.stage));
  }, [allItems, preferences.stage_filter]);

  const isLoading = skillsLoading || commandsLoading || agentsLoading || rulesLoading || hooksLoading;
  const hasError = skillsError || commandsError || agentsError;

  // ========================================
  // EFFECTS
  // ========================================

  // Auto-select last viewed item on mount
  useEffect(() => {
    if (preferences.last_viewed && allItems.length > 0) {
      const lastItem = allItems.find((item) => item.id === preferences.last_viewed);
      if (lastItem) {
        setSelectedItem(lastItem);
      }
    }
  }, [preferences.last_viewed, allItems]);

  // Apply theme to document
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDarkMode]);

  // ========================================
  // EVENT HANDLERS
  // ========================================

  const handleItemSelect = (item: Skill | Command | Agent | Rule | Hook) => {
    setSelectedItem(item);
    setPreferences({
      ...preferences,
      last_viewed: item.id,
    });
  };

  const handleToggleFavorite = (itemId: string) => {
    const isFavorite = preferences.favorites.includes(itemId);
    setPreferences({
      ...preferences,
      favorites: isFavorite
        ? preferences.favorites.filter((id) => id !== itemId)
        : [...preferences.favorites, itemId],
    });
  };

  const handleStageFilterChange = (selectedStages: string[]) => {
    setPreferences({
      ...preferences,
      stage_filter: selectedStages,
    });
  };

  const handleThemeToggle = (isSelected: boolean) => {
    setIsDarkMode(isSelected);
    setPreferences({
      ...preferences,
      theme: isSelected ? 'dark' : 'light',
    });
  };

  const handleSearchFocus = () => {
    navigate('/search');
  };

  const handleFavoritesClick = () => {
    navigate('/favorites');
  };

  const handleTreeExpand = (nodeIds: string[]) => {
    setExpandedNodes(nodeIds);
    setPreferences({
      ...preferences,
      collapsed_nodes: allItems
        .map((item) => item.id)
        .filter((id) => !nodeIds.includes(id)),
    });
  };

  // ========================================
  // ERROR STATE
  // ========================================

  if (hasError) {
    return (
      <View padding="size-500">
        <Flex direction="column" gap="size-200" alignItems="center">
          <Text>Failed to load framework components.</Text>
          <Button variant="primary" onPress={() => refetchSkills()}>
            Retry
          </Button>
        </Flex>
      </View>
    );
  }

  // ========================================
  // LOADING STATE
  // ========================================

  if (isLoading) {
    return (
      <View padding="size-500">
        <Flex direction="column" gap="size-200" alignItems="center">
          <Text>Loading framework components...</Text>
        </Flex>
      </View>
    );
  }

  // ========================================
  // MAIN RENDER
  // ========================================

  return (
    <View height="100vh" UNSAFE_className="bg-canvas text-text-primary">
      {/* Header */}
      <View
        backgroundColor="surface-1"
        borderBottomWidth="thin"
        borderBottomColor="border-default"
        height="size-800"
      >
        <Flex
          direction="row"
          alignItems="center"
          justifyContent="space-between"
          height="100%"
          paddingX="size-300"
          gap="size-200"
        >
          {/* Logo */}
          <Text UNSAFE_className="font-mono font-bold text-xl">ClaudeManual</Text>

          {/* Search Bar */}
          <TextField
            placeholder="Search (Cmd+K)"
            onFocus={handleSearchFocus}
            width="size-4600"
            aria-label="Search framework components"
            UNSAFE_className="flex-1 max-w-md"
          />

          {/* Theme Toggle */}
          <Switch isSelected={isDarkMode} onChange={handleThemeToggle} aria-label="Toggle dark mode">
            {isDarkMode ? 'Dark' : 'Light'}
          </Switch>

          {/* Stage Filter */}
          <StageFilterDropdown
            value={preferences.stage_filter}
            onChange={handleStageFilterChange}
          />

          {/* Favorites Button */}
          <Button
            variant="ghost"
            onPress={handleFavoritesClick}
            aria-label="View favorites"
          >
            <Star />
          </Button>
        </Flex>
      </View>

      {/* Main Content: Dual-Pane Layout */}
      <Flex direction="row" height="calc(100vh - 64px)">
        {/* Navigation Tree (Master Pane) */}
        <View
          width="size-3600"
          borderEndWidth="thin"
          borderEndColor="border-default"
          UNSAFE_className="overflow-y-auto"
        >
          <NavigationTree
            items={filteredItems}
            selectedItem={selectedItem}
            onSelect={handleItemSelect}
            expandedNodes={expandedNodes}
            onExpand={handleTreeExpand}
            favorites={preferences.favorites}
            onToggleFavorite={handleToggleFavorite}
          />
        </View>

        {/* Detail Pane */}
        <View flex UNSAFE_className="overflow-y-auto">
          {selectedItem ? (
            <DetailPane
              item={selectedItem}
              isFavorite={preferences.favorites.includes(selectedItem.id)}
              onToggleFavorite={() => handleToggleFavorite(selectedItem.id)}
            />
          ) : (
            <Flex
              direction="column"
              alignItems="center"
              justifyContent="center"
              height="100%"
            >
              <Text UNSAFE_className="text-text-secondary">
                Select a component to view details
              </Text>
            </Flex>
          )}
        </View>
      </Flex>

      {/* Footer */}
      <View
        backgroundColor="surface-1"
        borderTopWidth="thin"
        borderTopColor="border-default"
        height="size-600"
        UNSAFE_className="fixed bottom-0 left-0 right-0"
      >
        <Flex
          direction="row"
          alignItems="center"
          justifyContent="center"
          height="100%"
          gap="size-200"
        >
          <Text UNSAFE_className="text-text-secondary text-sm">
            Version 3.0.0 | Last Updated: 2026-01-31 | © HTEC Framework
          </Text>
        </Flex>
      </View>
    </View>
  );
}
