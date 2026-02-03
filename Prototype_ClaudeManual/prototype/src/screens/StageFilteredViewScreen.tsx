import React, { useState, useMemo, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { View, Heading, Text, Button } from '@adobe/react-spectrum';
import { NavigationTree } from '@/components/NavigationTree';
import { DetailPane } from '@/components/DetailPane';
import { StageFilterDropdown } from '@/components/StageFilterDropdown';
import { useItems } from '@/hooks/useItems';
import { usePreferences } from '@/hooks/usePreferences';
import type { Skill, Command, Agent, Rule, Hook } from '@/types';

type Item = Skill | Command | Agent | Rule | Hook;

const VALID_STAGES = [
  'Discovery',
  'Prototype',
  'ProductSpecs',
  'SolArch',
  'Implementation',
  'Utility',
  'Security',
  'GRC',
] as const;

type Stage = typeof VALID_STAGES[number];

/**
 * Stage-Filtered View Screen (SCR-003)
 *
 * Displays framework components filtered by workflow stage to reduce choice paralysis.
 * Uses Hicks Law to reduce visible items from 115+ to 20-40 stage-specific components.
 *
 * Traceability:
 * - Screen: SCR-003, S-3.0
 * - JTBD: JTBD-1.4 (Stage-appropriate tools), JTBD-1.3 (Find relevant tools)
 * - Pain Points: PP-1.4 (Organizational Chaos), PP-1.3 (Discoverability)
 * - Requirements: REQ-022, REQ-025
 */
export function StageFilteredViewScreen() {
  // URL params for deep linking
  const [searchParams, setSearchParams] = useSearchParams();

  // Fetch all items (skills, commands, agents, rules, hooks)
  const { items: allItems, loading, error } = useItems();

  // User preferences (localStorage)
  const { preferences, updatePreferences } = usePreferences();

  // Initialize selectedStages from URL params or localStorage
  const initialStages = useMemo(() => {
    const urlStages = searchParams.get('stage')?.split(',').filter(Boolean) || [];
    if (urlStages.length > 0) {
      return urlStages.filter(s => VALID_STAGES.includes(s as Stage));
    }
    return preferences.stage_filter || ['Discovery'];
  }, [searchParams, preferences.stage_filter]);

  const [selectedStages, setSelectedStages] = useState<string[]>(initialStages);
  const [selectedItem, setSelectedItem] = useState<Item | null>(null);

  // Filter items by selected stages (memoized for performance)
  const filteredItems = useMemo(() => {
    if (selectedStages.length === 0) return allItems;
    return allItems.filter(item => selectedStages.includes(item.stage));
  }, [allItems, selectedStages]);

  // Category counts
  const counts = useMemo(() => {
    const skills = filteredItems.filter(item => 'skills_required' in item);
    const commands = filteredItems.filter(item => 'argument_hint' in item);
    const agents = filteredItems.filter(item => 'checkpoint' in item);
    const rules = filteredItems.filter(item => 'auto_load_paths' in item);
    const hooks = filteredItems.filter(item => 'type' in item);

    return {
      total: allItems.length,
      filtered: filteredItems.length,
      skills: skills.length,
      commands: commands.length,
      agents: agents.length,
      rules: rules.length,
      hooks: hooks.length,
    };
  }, [allItems, filteredItems]);

  // Update URL and localStorage when selectedStages changes
  useEffect(() => {
    // Update URL params
    const params = new URLSearchParams(searchParams);
    if (selectedStages.length > 0) {
      params.set('stage', selectedStages.join(','));
    } else {
      params.delete('stage');
    }
    setSearchParams(params, { replace: true });

    // Update localStorage
    updatePreferences({ stage_filter: selectedStages });
  }, [selectedStages, setSearchParams, updatePreferences]);

  // Auto-select first item if none selected
  useEffect(() => {
    if (!selectedItem && filteredItems.length > 0) {
      setSelectedItem(filteredItems[0]);
    }
  }, [filteredItems, selectedItem]);

  const handleStageChange = (stages: string[]) => {
    setSelectedStages(stages);
    setSelectedItem(null); // Reset selection when filter changes
  };

  const handleClearFilter = () => {
    setSelectedStages([]);
    setSelectedItem(null);
  };

  const handleItemSelect = (item: Item) => {
    setSelectedItem(item);
  };

  if (loading) {
    return (
      <View padding="size-400">
        <Text>Loading framework components...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View padding="size-400">
        <Heading level={2}>Error Loading Components</Heading>
        <Text>{error}</Text>
      </View>
    );
  }

  return (
    <View
      minHeight="100vh"
      backgroundColor="bg-canvas"
      UNSAFE_className="stage-filtered-view"
    >
      {/* Header */}
      <View
        paddingX="size-300"
        paddingY="size-200"
        borderBottomWidth="thin"
        borderBottomColor="border-default"
        UNSAFE_className="flex items-center justify-between"
      >
        <Heading level={1} margin={0}>
          ClaudeManual
        </Heading>
        <View UNSAFE_className="flex items-center gap-4">
          <StageFilterDropdown
            selectedStages={selectedStages}
            onChange={handleStageChange}
            aria-label="Filter by workflow stage"
          />
        </View>
      </View>

      {/* Active Filter Indicator */}
      {selectedStages.length > 0 && (
        <View
          paddingX="size-300"
          paddingY="size-150"
          backgroundColor="bg-surface-1"
          borderBottomWidth="thin"
          borderBottomColor="border-default"
          UNSAFE_className="flex items-center justify-between"
        >
          <View UNSAFE_className="flex items-center gap-2">
            <Text>Active Filter:</Text>
            <Text UNSAFE_className="font-semibold text-accent-default">
              {selectedStages.join(', ')}
            </Text>
          </View>
          <View UNSAFE_className="flex items-center gap-4">
            <Text UNSAFE_className="text-secondary">
              Showing {counts.filtered} of {counts.total} components
            </Text>
            <Button
              onPress={handleClearFilter}
              variant="secondary"
              aria-label="Clear stage filter"
            >
              Clear Filter
            </Button>
          </View>
        </View>
      )}

      {/* Main Content */}
      <View UNSAFE_className="flex flex-1">
        {/* Sidebar - Navigation Tree */}
        <View
          width="size-3600"
          borderEndWidth="thin"
          borderEndColor="border-default"
          backgroundColor="bg-surface-1"
          UNSAFE_className="overflow-y-auto"
        >
          <NavigationTree
            items={filteredItems}
            selectedItem={selectedItem}
            onItemSelect={handleItemSelect}
            filteredStage={selectedStages.join(', ')}
            counts={{
              skills: counts.skills,
              commands: counts.commands,
              agents: counts.agents,
              rules: counts.rules,
              hooks: counts.hooks,
            }}
          />
        </View>

        {/* Main - Detail Pane */}
        <View flex UNSAFE_className="overflow-y-auto">
          {selectedItem ? (
            <DetailPane item={selectedItem} />
          ) : (
            <View
              padding="size-600"
              UNSAFE_className="flex flex-col items-center justify-center h-full"
            >
              <Heading level={3}>No Item Selected</Heading>
              <Text>
                {selectedStages.length === 0
                  ? 'Select a stage filter to view components.'
                  : `Select a component from the ${selectedStages.join(', ')} items.`}
              </Text>
            </View>
          )}
        </View>
      </View>

      {/* Footer */}
      <View
        paddingX="size-300"
        paddingY="size-150"
        borderTopWidth="thin"
        borderTopColor="border-default"
        backgroundColor="bg-surface-1"
        UNSAFE_className="flex items-center justify-between"
      >
        <Text UNSAFE_className="text-secondary">
          Filtered View | {counts.filtered} {selectedStages.join(', ')} Components
        </Text>
        <Text UNSAFE_className="text-secondary">Version 3.0.0</Text>
      </View>
    </View>
  );
}
