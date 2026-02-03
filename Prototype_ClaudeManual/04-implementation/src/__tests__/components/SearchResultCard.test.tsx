import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { SearchResultCard } from '../../components/SearchResultCard';
import type { SearchResult } from '../../components/SearchResultCard';

const mockSearchResult: SearchResult = {
  id: 'skill-001',
  name: 'Discovery_JTBD',
  type: 'skill',
  stage: 'discovery',
  path: '.claude/skills/Discovery_JTBD/SKILL.md',
  summary: 'Extracts Jobs To Be Done from pain points and client facts.',
  relevanceScore: 0.92,
  isFavorite: false,
};

const mockFavoriteResult: SearchResult = {
  ...mockSearchResult,
  id: 'skill-002',
  isFavorite: true,
};

describe('SearchResultCard', () => {
  it('renders result name', () => {
    const handleClick = vi.fn();
    render(<SearchResultCard result={mockSearchResult} query="" onClick={handleClick} />);
    expect(screen.getByText('Discovery_JTBD')).toBeInTheDocument();
  });

  it('renders type badge', () => {
    const handleClick = vi.fn();
    render(<SearchResultCard result={mockSearchResult} query="" onClick={handleClick} />);
    expect(screen.getByText('skill')).toBeInTheDocument();
  });

  it('renders stage badge', () => {
    const handleClick = vi.fn();
    render(<SearchResultCard result={mockSearchResult} query="" onClick={handleClick} />);
    expect(screen.getByText('discovery')).toBeInTheDocument();
  });

  it('renders summary text', () => {
    const handleClick = vi.fn();
    render(<SearchResultCard result={mockSearchResult} query="" onClick={handleClick} />);
    expect(screen.getByText(/Extracts Jobs To Be Done/)).toBeInTheDocument();
  });

  it('renders file path', () => {
    const handleClick = vi.fn();
    render(<SearchResultCard result={mockSearchResult} query="" onClick={handleClick} />);
    expect(screen.getByText('.claude/skills/Discovery_JTBD/SKILL.md')).toBeInTheDocument();
  });

  it('calls onClick when card is clicked', () => {
    const handleClick = vi.fn();
    const { container } = render(
      <SearchResultCard result={mockSearchResult} query="" onClick={handleClick} />
    );

    const card = container.firstChild as HTMLElement;
    fireEvent.click(card);

    expect(handleClick).toHaveBeenCalledWith(mockSearchResult.id);
  });

  it('highlights query text in name', () => {
    const handleClick = vi.fn();
    const { container } = render(
      <SearchResultCard result={mockSearchResult} query="jtbd" onClick={handleClick} />
    );

    const mark = container.querySelector('mark');
    expect(mark).toBeInTheDocument();
    expect(mark?.textContent).toBe('JTBD');
  });

  it('highlights query text in summary', () => {
    const handleClick = vi.fn();
    const { container } = render(
      <SearchResultCard result={mockSearchResult} query="pain" onClick={handleClick} />
    );

    const marks = container.querySelectorAll('mark');
    expect(marks.length).toBeGreaterThan(0);
  });

  it('applies highlighted style when highlighted prop is true', () => {
    const handleClick = vi.fn();
    const { container } = render(
      <SearchResultCard result={mockSearchResult} query="" onClick={handleClick} highlighted={true} />
    );

    const card = container.firstChild as HTMLElement;
    expect(card).toHaveClass('border-blue-500');
  });

  it('does not apply highlighted style by default', () => {
    const handleClick = vi.fn();
    const { container } = render(
      <SearchResultCard result={mockSearchResult} query="" onClick={handleClick} />
    );

    const card = container.firstChild as HTMLElement;
    expect(card).not.toHaveClass('border-blue-500');
  });

  it('shows favorite icon when isFavorite is true', () => {
    const handleClick = vi.fn();
    const { container } = render(
      <SearchResultCard result={mockFavoriteResult} query="" onClick={handleClick} />
    );

    const favoriteIcon = container.querySelector('.favorite-icon');
    expect(favoriteIcon).toBeInTheDocument();
  });

  it('does not show favorite icon when isFavorite is false', () => {
    const handleClick = vi.fn();
    const { container } = render(
      <SearchResultCard result={mockSearchResult} query="" onClick={handleClick} />
    );

    const favoriteIcon = container.querySelector('.favorite-icon');
    expect(favoriteIcon).not.toBeInTheDocument();
  });

  it('renders Copy Path button when onCopyPath is provided', () => {
    const handleClick = vi.fn();
    const handleCopyPath = vi.fn();

    render(
      <SearchResultCard
        result={mockSearchResult}
        query=""
        onClick={handleClick}
        onCopyPath={handleCopyPath}
      />
    );

    expect(screen.getByRole('button', { name: /Copy/i })).toBeInTheDocument();
  });

  it('calls onCopyPath when Copy Path button is clicked', () => {
    const handleClick = vi.fn();
    const handleCopyPath = vi.fn();

    render(
      <SearchResultCard
        result={mockSearchResult}
        query=""
        onClick={handleClick}
        onCopyPath={handleCopyPath}
      />
    );

    const copyButton = screen.getByRole('button', { name: /Copy/i });
    fireEvent.click(copyButton);

    expect(handleCopyPath).toHaveBeenCalledWith(mockSearchResult.path);
  });

  it('renders Favorite button when onToggleFavorite is provided', () => {
    const handleClick = vi.fn();
    const handleToggleFavorite = vi.fn();

    render(
      <SearchResultCard
        result={mockSearchResult}
        query=""
        onClick={handleClick}
        onToggleFavorite={handleToggleFavorite}
      />
    );

    expect(screen.getByRole('button', { name: /Favorite/i })).toBeInTheDocument();
  });

  it('calls onToggleFavorite when Favorite button is clicked', () => {
    const handleClick = vi.fn();
    const handleToggleFavorite = vi.fn();

    render(
      <SearchResultCard
        result={mockSearchResult}
        query=""
        onClick={handleClick}
        onToggleFavorite={handleToggleFavorite}
      />
    );

    const favoriteButton = screen.getByRole('button', { name: /Favorite/i });
    fireEvent.click(favoriteButton);

    expect(handleToggleFavorite).toHaveBeenCalledWith(mockSearchResult.id);
  });

  it('displays relevance score badge for high scores', () => {
    const handleClick = vi.fn();
    const { container } = render(
      <SearchResultCard result={mockSearchResult} query="" onClick={handleClick} />
    );

    const relevanceBadge = container.querySelector('.relevance-badge');
    expect(relevanceBadge).toBeInTheDocument();
    expect(relevanceBadge?.textContent).toContain('92%');
  });

  it('applies hover effect on mouse over', () => {
    const handleClick = vi.fn();
    const { container } = render(
      <SearchResultCard result={mockSearchResult} query="" onClick={handleClick} />
    );

    const card = container.firstChild as HTMLElement;
    expect(card).toHaveClass('hover:shadow-md');
  });

  it('renders as article element for accessibility', () => {
    const handleClick = vi.fn();
    const { container } = render(
      <SearchResultCard result={mockSearchResult} query="" onClick={handleClick} />
    );

    const article = container.querySelector('article');
    expect(article).toBeInTheDocument();
  });

  it('does not trigger onClick when action buttons are clicked', () => {
    const handleClick = vi.fn();
    const handleCopyPath = vi.fn();

    render(
      <SearchResultCard
        result={mockSearchResult}
        query=""
        onClick={handleClick}
        onCopyPath={handleCopyPath}
      />
    );

    const copyButton = screen.getByRole('button', { name: /Copy/i });
    fireEvent.click(copyButton);

    expect(handleClick).not.toHaveBeenCalled();
  });
});
