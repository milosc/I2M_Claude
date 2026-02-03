import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FavoritesPanel } from './FavoritesPanel';

const mockFavorites = [
  {
    id: 'discovery-persona-synthesizer',
    name: 'Persona Synthesizer',
    type: 'agent' as const,
    stage: 'discovery' as const,
    path: '.claude/agents/discovery-persona-synthesizer.md',
    summary: 'Synthesizes user personas from interview data',
    isFavorite: true,
    lastUpdated: '2026-01-15',
  },
  {
    id: 'prototype-screen-specifier',
    name: 'Screen Specifier',
    type: 'agent' as const,
    stage: 'prototype' as const,
    path: '.claude/agents/prototype-screen-specifier.md',
    summary: 'Generates screen specifications',
    isFavorite: true,
    lastUpdated: '2026-01-20',
  },
  {
    id: 'discovery-audit',
    name: 'Discovery Audit',
    type: 'command' as const,
    stage: 'discovery' as const,
    path: '.claude/commands/discovery-audit.md',
    summary: 'Zero hallucination audit for discovery',
    isFavorite: true,
  },
];

describe('FavoritesPanel', () => {
  describe('Rendering', () => {
    it('renders favorites grid', () => {
      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      expect(screen.getByText('Persona Synthesizer')).toBeInTheDocument();
      expect(screen.getByText('Screen Specifier')).toBeInTheDocument();
      expect(screen.getByText('Discovery Audit')).toBeInTheDocument();
    });

    it('shows favorites count', () => {
      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      expect(screen.getByText(/3 favorites/i)).toBeInTheDocument();
    });

    it('shows Clear All button when favorites exist', () => {
      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      expect(screen.getByRole('button', { name: /clear all/i })).toBeInTheDocument();
    });
  });

  describe('Empty State', () => {
    it('shows empty state when no favorites', () => {
      render(
        <FavoritesPanel
          favorites={[]}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      expect(screen.getByRole('heading', { name: /no favorites yet/i })).toBeInTheDocument();
      expect(screen.getByText(/start adding your favorite/i)).toBeInTheDocument();
    });

    it('does not show Clear All button when empty', () => {
      render(
        <FavoritesPanel
          favorites={[]}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      expect(screen.queryByRole('button', { name: /clear all/i })).not.toBeInTheDocument();
    });

    it('shows illustration in empty state', () => {
      render(
        <FavoritesPanel
          favorites={[]}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      const illustration = screen.getByRole('img', { name: /no favorites/i });
      expect(illustration).toBeInTheDocument();
    });
  });

  describe('Interactions', () => {
    it('calls onClick when favorite item is clicked', async () => {
      const user = userEvent.setup();
      const handleClick = vi.fn();

      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={handleClick}
        />
      );

      const firstCard = screen.getByText('Persona Synthesizer').closest('article');
      await user.click(firstCard!);

      expect(handleClick).toHaveBeenCalledWith('discovery-persona-synthesizer');
    });

    it('calls onRemove when remove button is clicked', async () => {
      const user = userEvent.setup();
      const handleRemove = vi.fn();

      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={handleRemove}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      const removeButtons = screen.getAllByText('Remove');
      await user.click(removeButtons[0]);

      expect(handleRemove).toHaveBeenCalledWith('discovery-persona-synthesizer');
    });

    it('shows confirmation dialog when Clear All button is clicked', async () => {
      const user = userEvent.setup();
      const handleClearAll = vi.fn();

      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={handleClearAll}
          onClick={vi.fn()}
        />
      );

      const clearAllButton = screen.getByRole('button', { name: /clear all/i });
      await user.click(clearAllButton);

      expect(screen.getByText(/remove all 3 favorites/i)).toBeInTheDocument();
      expect(handleClearAll).not.toHaveBeenCalled();
    });

    it('shows confirmation before clearing all', async () => {
      const user = userEvent.setup();
      const handleClearAll = vi.fn();

      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={handleClearAll}
          onClick={vi.fn()}
        />
      );

      const clearAllButton = screen.getByRole('button', { name: /clear all/i });
      await user.click(clearAllButton);

      expect(screen.getByText(/remove all 3 favorites/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /confirm/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /cancel/i })).toBeInTheDocument();
    });

    it('cancels clear all when Cancel is clicked', async () => {
      const user = userEvent.setup();
      const handleClearAll = vi.fn();

      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={handleClearAll}
          onClick={vi.fn()}
        />
      );

      const clearAllButton = screen.getByRole('button', { name: /clear all/i });
      await user.click(clearAllButton);

      const cancelButton = screen.getByRole('button', { name: /cancel/i });
      await user.click(cancelButton);

      expect(screen.queryByText(/remove all 3 favorites/i)).not.toBeInTheDocument();
      expect(handleClearAll).not.toHaveBeenCalled();
    });

    it('confirms clear all when Confirm is clicked', async () => {
      const user = userEvent.setup();
      const handleClearAll = vi.fn();

      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={handleClearAll}
          onClick={vi.fn()}
        />
      );

      const clearAllButton = screen.getByRole('button', { name: /clear all/i });
      await user.click(clearAllButton);

      const confirmButton = screen.getByRole('button', { name: /confirm/i });
      await user.click(confirmButton);

      expect(handleClearAll).toHaveBeenCalled();
      expect(screen.queryByText(/remove all 3 favorites/i)).not.toBeInTheDocument();
    });
  });

  describe('Grid Layout', () => {
    it('displays items in grid layout on desktop', () => {
      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      const grid = screen.getByTestId('favorites-grid');
      expect(grid).toHaveClass('grid');
      expect(grid).toHaveClass('lg:grid-cols-3');
    });

    it('displays 2 columns on tablet', () => {
      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      const grid = screen.getByTestId('favorites-grid');
      expect(grid).toHaveClass('md:grid-cols-2');
    });

    it('displays 1 column on mobile', () => {
      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      const grid = screen.getByTestId('favorites-grid');
      expect(grid).toHaveClass('grid-cols-1');
    });
  });

  describe('Type Filtering', () => {
    it('shows type filter buttons', () => {
      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      expect(screen.getByRole('button', { name: /^all$/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /agents/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /commands/i })).toBeInTheDocument();
    });

    it('filters by agent type', async () => {
      const user = userEvent.setup();

      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      const agentsButton = screen.getByRole('button', { name: /agents/i });
      await user.click(agentsButton);

      expect(screen.getByText('Persona Synthesizer')).toBeInTheDocument();
      expect(screen.getByText('Screen Specifier')).toBeInTheDocument();
      expect(screen.queryByText('Discovery Audit')).not.toBeInTheDocument();
    });

    it('filters by command type', async () => {
      const user = userEvent.setup();

      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      const commandsButton = screen.getByRole('button', { name: /commands/i });
      await user.click(commandsButton);

      expect(screen.queryByText('Persona Synthesizer')).not.toBeInTheDocument();
      expect(screen.queryByText('Screen Specifier')).not.toBeInTheDocument();
      expect(screen.getByText('Discovery Audit')).toBeInTheDocument();
    });

    it('shows all items when All filter is selected', async () => {
      const user = userEvent.setup();

      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      const commandsButton = screen.getByRole('button', { name: /commands/i });
      await user.click(commandsButton);

      const allButton = screen.getByRole('button', { name: /^all$/i });
      await user.click(allButton);

      expect(screen.getByText('Persona Synthesizer')).toBeInTheDocument();
      expect(screen.getByText('Screen Specifier')).toBeInTheDocument();
      expect(screen.getByText('Discovery Audit')).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('has proper heading structure', () => {
      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      expect(screen.getByRole('heading', { level: 2, name: /my favorites/i })).toBeInTheDocument();
    });

    it('provides region landmark', () => {
      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      expect(screen.getByRole('region', { name: /favorites panel/i })).toBeInTheDocument();
    });

    it('announces filter changes to screen readers', async () => {
      const user = userEvent.setup();

      render(
        <FavoritesPanel
          favorites={mockFavorites}
          onReorder={vi.fn()}
          onRemove={vi.fn()}
          onClearAll={vi.fn()}
          onClick={vi.fn()}
        />
      );

      const agentsButton = screen.getByRole('button', { name: /agents/i });
      await user.click(agentsButton);

      expect(screen.getByText(/showing 2 agent/i)).toBeInTheDocument();
    });
  });
});
