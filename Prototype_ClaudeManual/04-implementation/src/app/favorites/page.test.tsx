import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import FavoritesPage from './page';

// Mock localStorage
const mockLocalStorage = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value;
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage,
});

beforeEach(() => {
  mockLocalStorage.clear();
});

describe('FavoritesPage', () => {
  it('displays empty state when no favorites', () => {
    render(<FavoritesPage />);

    const emptyState = screen.getAllByText(/No Favorites Yet/i);
    expect(emptyState.length).toBeGreaterThan(0);
    expect(screen.getByText(/Start adding your favorite/i)).toBeInTheDocument();
  });

  it('loads favorites from localStorage', () => {
    const mockFavorites = [
      {
        id: 'skill-1',
        name: 'Test Skill',
        type: 'skill',
        stage: 'discovery',
        path: '.claude/skills/test',
        summary: 'Test summary',
        isFavorite: true,
      },
    ];

    mockLocalStorage.setItem('favorites', JSON.stringify(mockFavorites));

    render(<FavoritesPage />);

    expect(screen.getByText('Test Skill')).toBeInTheDocument();
    expect(screen.getByText(/1 favorite/i)).toBeInTheDocument();
  });

  it('filters favorites by type', () => {
    const mockFavorites = [
      {
        id: 'skill-1',
        name: 'Test Skill',
        type: 'skill',
        stage: 'discovery',
        path: '.claude/skills/test',
        summary: 'Test summary',
        isFavorite: true,
      },
      {
        id: 'command-1',
        name: 'Test Command',
        type: 'command',
        stage: 'discovery',
        path: '.claude/commands/test',
        summary: 'Test summary',
        isFavorite: true,
      },
    ];

    mockLocalStorage.setItem('favorites', JSON.stringify(mockFavorites));

    render(<FavoritesPage />);

    // Initially shows all
    expect(screen.getByText('Test Skill')).toBeInTheDocument();
    expect(screen.getByText('Test Command')).toBeInTheDocument();

    // Click skill filter
    const skillButton = screen.getByRole('button', { name: /Skills/i });
    fireEvent.click(skillButton);

    // Should show only skill
    expect(screen.getByText('Test Skill')).toBeInTheDocument();
    expect(screen.queryByText('Test Command')).not.toBeInTheDocument();
  });

  it('removes individual favorite', () => {
    const mockFavorites = [
      {
        id: 'skill-1',
        name: 'Test Skill',
        type: 'skill',
        stage: 'discovery',
        path: '.claude/skills/test',
        summary: 'Test summary',
        isFavorite: true,
      },
    ];

    mockLocalStorage.setItem('favorites', JSON.stringify(mockFavorites));

    render(<FavoritesPage />);

    expect(screen.getByText('Test Skill')).toBeInTheDocument();

    // Find and click the Remove button
    const removeButton = screen.getByText('Remove');
    fireEvent.click(removeButton);

    // Should show empty state
    const emptyState = screen.getAllByText(/No Favorites Yet/i);
    expect(emptyState.length).toBeGreaterThan(0);
  });

  it('clears all favorites with confirmation', () => {
    const mockFavorites = [
      {
        id: 'skill-1',
        name: 'Test Skill',
        type: 'skill',
        stage: 'discovery',
        path: '.claude/skills/test',
        summary: 'Test summary',
        isFavorite: true,
      },
    ];

    mockLocalStorage.setItem('favorites', JSON.stringify(mockFavorites));

    render(<FavoritesPage />);

    // Click Clear All button
    const clearButton = screen.getByRole('button', { name: /Clear All/i });
    fireEvent.click(clearButton);

    // Should show confirmation modal
    expect(screen.getByText(/Remove All Favorites/i)).toBeInTheDocument();

    // Click Confirm
    const confirmButton = screen.getByRole('button', { name: /Confirm/i });
    fireEvent.click(confirmButton);

    // Should show empty state
    const emptyState = screen.getAllByText(/No Favorites Yet/i);
    expect(emptyState.length).toBeGreaterThan(0);
  });
});
