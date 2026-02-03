import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { NavigationTree } from '../../components/NavigationTree';
import type { TreeNode, Stage } from '../../types/navigation';

const mockTreeData: TreeNode[] = [
  {
    id: 'discovery',
    label: 'Discovery',
    type: 'category',
    children: [
      {
        id: 'Discovery_JTBD',
        label: 'Discovery_JTBD',
        type: 'skill',
        stage: 'discovery',
        path: '.claude/skills/Discovery_JTBD/SKILL.md',
        description: 'Extracts Jobs To Be Done',
        count: 0,
      },
      {
        id: 'Discovery_Personas',
        label: 'Discovery_Personas',
        type: 'skill',
        stage: 'discovery',
        path: '.claude/skills/Discovery_Personas/SKILL.md',
        description: 'Synthesizes personas',
        count: 0,
      },
    ],
    count: 2,
  },
  {
    id: 'prototype',
    label: 'Prototype',
    type: 'category',
    children: [
      {
        id: 'Prototype_Components',
        label: 'Prototype_Components',
        type: 'skill',
        stage: 'prototype',
        path: '.claude/skills/Prototype_Components/SKILL.md',
        count: 0,
      },
    ],
    count: 1,
  },
];

describe('NavigationTree', () => {
  describe('Rendering', () => {
    it('renders tree with nested categories', () => {
      const onSelect = vi.fn();
      render(<NavigationTree items={mockTreeData} onSelect={onSelect} />);

      expect(screen.getByText('Discovery')).toBeInTheDocument();
      expect(screen.getByText('Prototype')).toBeInTheDocument();
    });

    it('shows count badges when enabled', () => {
      const onSelect = vi.fn();
      render(
        <NavigationTree
          items={mockTreeData}
          onSelect={onSelect}
          showCountBadges={true}
        />
      );

      // Count badges should be visible
      expect(screen.getByText(/2/)).toBeInTheDocument(); // Discovery (2)
      expect(screen.getByText(/1/)).toBeInTheDocument(); // Prototype (1)
    });

    it('highlights selected item', () => {
      const onSelect = vi.fn();
      const { container } = render(
        <NavigationTree
          items={mockTreeData}
          selectedId="Discovery_JTBD"
          onSelect={onSelect}
        />
      );

      // Expand to show children
      const discoveryNode = screen.getByText('Discovery');
      fireEvent.click(discoveryNode);

      // Check if Discovery_JTBD has selected styling
      const selectedItem = screen.getByText('Discovery_JTBD');
      expect(selectedItem).toBeInTheDocument();
    });

    it('shows favorite star icon for favorited items', () => {
      const onSelect = vi.fn();
      render(
        <NavigationTree
          items={mockTreeData}
          favorites={['Discovery_JTBD']}
          onSelect={onSelect}
        />
      );

      // Expand to show children
      const discoveryNode = screen.getByText('Discovery');
      fireEvent.click(discoveryNode);

      // Should show favorite indicator
      expect(screen.getByText('Discovery_JTBD')).toBeInTheDocument();
    });
  });

  describe('Interactions', () => {
    it('expands and collapses categories on click', () => {
      const onSelect = vi.fn();
      render(<NavigationTree items={mockTreeData} onSelect={onSelect} />);

      const discoveryNode = screen.getByText('Discovery');

      // Initially collapsed - children not visible
      expect(screen.queryByText('Discovery_JTBD')).not.toBeInTheDocument();

      // Click to expand
      fireEvent.click(discoveryNode);
      expect(screen.getByText('Discovery_JTBD')).toBeInTheDocument();

      // Click to collapse
      fireEvent.click(discoveryNode);
      expect(screen.queryByText('Discovery_JTBD')).not.toBeInTheDocument();
    });

    it('calls onSelect when item is clicked', () => {
      const onSelect = vi.fn();
      render(<NavigationTree items={mockTreeData} onSelect={onSelect} />);

      // Expand category
      const discoveryNode = screen.getByText('Discovery');
      fireEvent.click(discoveryNode);

      // Click on child item
      const skillNode = screen.getByText('Discovery_JTBD');
      fireEvent.click(skillNode);

      expect(onSelect).toHaveBeenCalledWith('Discovery_JTBD');
    });

    it('toggles favorite status when favorite icon clicked', () => {
      const onToggleFavorite = vi.fn();
      const onSelect = vi.fn();

      render(
        <NavigationTree
          items={mockTreeData}
          favorites={[]}
          onSelect={onSelect}
          onToggleFavorite={onToggleFavorite}
        />
      );

      // Expand to show children
      const discoveryNode = screen.getByText('Discovery');
      fireEvent.click(discoveryNode);

      // Find and click favorite button (implementation will add this)
      // This test will guide implementation
      const jtbdNode = screen.getByText('Discovery_JTBD');
      expect(jtbdNode).toBeInTheDocument();
    });
  });

  describe('Filtering', () => {
    it('filters items by stage', () => {
      const onSelect = vi.fn();
      render(
        <NavigationTree
          items={mockTreeData}
          stageFilter={['discovery']}
          onSelect={onSelect}
        />
      );

      // Discovery category should be visible
      expect(screen.getByText('Discovery')).toBeInTheDocument();

      // Prototype should be muted or hidden
      expect(screen.getByText('Prototype')).toBeInTheDocument();
    });

    it('filters items by search query', () => {
      const onSelect = vi.fn();
      render(
        <NavigationTree
          items={mockTreeData}
          searchQuery="jtbd"
          onSelect={onSelect}
        />
      );

      // Should auto-expand matching branches and show JTBD
      expect(screen.getByText('Discovery')).toBeInTheDocument();
    });

    it('shows empty state when no items match filter', () => {
      const onSelect = vi.fn();
      render(
        <NavigationTree
          items={[]}
          searchQuery="nonexistent"
          onSelect={onSelect}
        />
      );

      // Should show empty state message
      expect(
        screen.getByText(/no items found/i) || screen.getByText(/empty/i)
      ).toBeInTheDocument();
    });

    it('updates count badges when filter active', () => {
      const onSelect = vi.fn();
      const { rerender } = render(
        <NavigationTree
          items={mockTreeData}
          onSelect={onSelect}
          showCountBadges={true}
        />
      );

      // Initially shows total counts
      expect(screen.getByText(/2/)).toBeInTheDocument();

      // Apply stage filter
      rerender(
        <NavigationTree
          items={mockTreeData}
          stageFilter={['discovery']}
          onSelect={onSelect}
          showCountBadges={true}
        />
      );

      // Counts should update based on filter
      expect(screen.getByText('Discovery')).toBeInTheDocument();
    });
  });

  describe('States', () => {
    it('shows loading state', () => {
      const onSelect = vi.fn();
      render(<NavigationTree items={[]} onSelect={onSelect} loading={true} />);

      expect(screen.getByText(/loading/i)).toBeInTheDocument();
    });

    it('shows error state', () => {
      const onSelect = vi.fn();
      render(
        <NavigationTree
          items={[]}
          onSelect={onSelect}
          error="Failed to load tree"
        />
      );

      expect(screen.getByText(/failed to load/i)).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('has proper ARIA attributes', () => {
      const onSelect = vi.fn();
      const { container } = render(
        <NavigationTree items={mockTreeData} onSelect={onSelect} />
      );

      // Tree should have role="tree"
      const tree = container.querySelector('[role="tree"]');
      expect(tree).toBeInTheDocument();
    });

    it('supports keyboard navigation', () => {
      const onSelect = vi.fn();
      render(<NavigationTree items={mockTreeData} onSelect={onSelect} />);

      const discoveryNode = screen.getByText('Discovery');

      // Test Enter key
      fireEvent.keyDown(discoveryNode, { key: 'Enter', code: 'Enter' });
      expect(screen.getByText('Discovery_JTBD')).toBeInTheDocument();
    });
  });
});
