import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ComponentCard } from './ComponentCard';

const mockComponent = {
  id: 'discovery-persona-synthesizer',
  name: 'Persona Synthesizer',
  type: 'agent' as const,
  stage: 'discovery' as const,
  path: '.claude/agents/discovery-persona-synthesizer.md',
  summary: 'Synthesizes user personas from interview data',
  isFavorite: false,
  lastUpdated: '2026-01-15',
};

describe('ComponentCard', () => {
  describe('Grid Variant', () => {
    it('renders component metadata in grid layout', () => {
      render(
        <ComponentCard
          component={mockComponent}
          variant="grid"
          onClick={vi.fn()}
          onToggleFavorite={vi.fn()}
        />
      );

      expect(screen.getByText('Persona Synthesizer')).toBeInTheDocument();
      expect(screen.getByText('agent')).toBeInTheDocument();
      expect(screen.getByText('discovery')).toBeInTheDocument();
      expect(screen.getByText(/Synthesizes user personas/)).toBeInTheDocument();
    });

    it('shows favorite star when isFavorite is true', () => {
      const favoriteComponent = { ...mockComponent, isFavorite: true };

      render(
        <ComponentCard
          component={favoriteComponent}
          variant="grid"
          onClick={vi.fn()}
          onToggleFavorite={vi.fn()}
        />
      );

      const favoriteButton = screen.getByRole('button', { name: /favorite/i });
      expect(favoriteButton).toHaveAttribute('aria-pressed', 'true');
    });

    it('calls onClick when card is clicked', async () => {
      const user = userEvent.setup();
      const handleClick = vi.fn();

      render(
        <ComponentCard
          component={mockComponent}
          variant="grid"
          onClick={handleClick}
          onToggleFavorite={vi.fn()}
        />
      );

      const card = screen.getByRole('article');
      await user.click(card);

      expect(handleClick).toHaveBeenCalledWith('discovery-persona-synthesizer');
    });

    it('calls onToggleFavorite when star is clicked', async () => {
      const user = userEvent.setup();
      const handleToggle = vi.fn();

      render(
        <ComponentCard
          component={mockComponent}
          variant="grid"
          onClick={vi.fn()}
          onToggleFavorite={handleToggle}
        />
      );

      const favoriteButton = screen.getByRole('button', { name: /favorite/i });
      await user.click(favoriteButton);

      expect(handleToggle).toHaveBeenCalledWith('discovery-persona-synthesizer');
    });

    it('shows remove button when showRemove is true', () => {
      render(
        <ComponentCard
          component={mockComponent}
          variant="grid"
          showRemove={true}
          onClick={vi.fn()}
          onToggleFavorite={vi.fn()}
          onRemove={vi.fn()}
        />
      );

      expect(screen.getByRole('button', { name: /remove/i })).toBeInTheDocument();
    });

    it('calls onRemove when remove button is clicked', async () => {
      const user = userEvent.setup();
      const handleRemove = vi.fn();

      render(
        <ComponentCard
          component={mockComponent}
          variant="grid"
          showRemove={true}
          onClick={vi.fn()}
          onToggleFavorite={vi.fn()}
          onRemove={handleRemove}
        />
      );

      const removeButton = screen.getByRole('button', { name: /remove/i });
      await user.click(removeButton);

      expect(handleRemove).toHaveBeenCalledWith('discovery-persona-synthesizer');
    });

    it('prevents onClick when clicking favorite button', async () => {
      const user = userEvent.setup();
      const handleClick = vi.fn();
      const handleToggle = vi.fn();

      render(
        <ComponentCard
          component={mockComponent}
          variant="grid"
          onClick={handleClick}
          onToggleFavorite={handleToggle}
        />
      );

      const favoriteButton = screen.getByRole('button', { name: /favorite/i });
      await user.click(favoriteButton);

      expect(handleToggle).toHaveBeenCalled();
      expect(handleClick).not.toHaveBeenCalled();
    });
  });

  describe('List Variant', () => {
    it('renders component metadata in list layout', () => {
      render(
        <ComponentCard
          component={mockComponent}
          variant="list"
          onClick={vi.fn()}
          onToggleFavorite={vi.fn()}
        />
      );

      expect(screen.getByText('Persona Synthesizer')).toBeInTheDocument();
      expect(screen.getByText('agent')).toBeInTheDocument();
      expect(screen.getByText('discovery')).toBeInTheDocument();
    });

    it('shows path in list variant', () => {
      render(
        <ComponentCard
          component={mockComponent}
          variant="list"
          onClick={vi.fn()}
          onToggleFavorite={vi.fn()}
        />
      );

      expect(screen.getByText('.claude/agents/discovery-persona-synthesizer.md')).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('has correct ARIA role', () => {
      render(
        <ComponentCard
          component={mockComponent}
          variant="grid"
          onClick={vi.fn()}
          onToggleFavorite={vi.fn()}
        />
      );

      expect(screen.getByRole('article')).toHaveAttribute('aria-label', 'Component card: Persona Synthesizer');
    });

    it('supports keyboard navigation', async () => {
      const user = userEvent.setup();
      const handleClick = vi.fn();

      render(
        <ComponentCard
          component={mockComponent}
          variant="grid"
          onClick={handleClick}
          onToggleFavorite={vi.fn()}
        />
      );

      const card = screen.getByRole('article');
      card.focus();
      await user.keyboard('{Enter}');

      expect(handleClick).toHaveBeenCalledWith('discovery-persona-synthesizer');
    });

    it('has visible focus indicator', () => {
      render(
        <ComponentCard
          component={mockComponent}
          variant="grid"
          onClick={vi.fn()}
          onToggleFavorite={vi.fn()}
        />
      );

      const card = screen.getByRole('article');
      card.focus();

      expect(card).toHaveClass('focus:ring-2', 'focus:ring-accent-default');
    });
  });

  describe('Stage Colors', () => {
    const stages = ['discovery', 'prototype', 'productspecs', 'solarch', 'implementation'] as const;

    stages.forEach((stage) => {
      it(`applies correct color for ${stage} stage`, () => {
        const componentWithStage = { ...mockComponent, stage };

        render(
          <ComponentCard
            component={componentWithStage}
            variant="grid"
            onClick={vi.fn()}
            onToggleFavorite={vi.fn()}
          />
        );

        const stageBadge = screen.getByText(stage);
        expect(stageBadge).toBeInTheDocument();
      });
    });
  });

  describe('Component Types', () => {
    const types = ['skill', 'command', 'agent', 'rule', 'hook'] as const;

    types.forEach((type) => {
      it(`displays ${type} type badge`, () => {
        const componentWithType = { ...mockComponent, type };

        render(
          <ComponentCard
            component={componentWithType}
            variant="grid"
            onClick={vi.fn()}
            onToggleFavorite={vi.fn()}
          />
        );

        expect(screen.getByText(type)).toBeInTheDocument();
      });
    });
  });

  describe('Last Updated Indicator', () => {
    it('shows last updated date when provided', () => {
      render(
        <ComponentCard
          component={mockComponent}
          variant="grid"
          onClick={vi.fn()}
          onToggleFavorite={vi.fn()}
        />
      );

      expect(screen.getByText(/2026-01-15/)).toBeInTheDocument();
    });

    it('does not show last updated when not provided', () => {
      const componentWithoutDate = { ...mockComponent, lastUpdated: undefined };

      render(
        <ComponentCard
          component={componentWithoutDate}
          variant="grid"
          onClick={vi.fn()}
          onToggleFavorite={vi.fn()}
        />
      );

      expect(screen.queryByText(/Updated/)).not.toBeInTheDocument();
    });
  });
});
