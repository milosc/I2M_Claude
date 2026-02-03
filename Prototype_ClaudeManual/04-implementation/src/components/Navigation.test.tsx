import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Navigation } from './Navigation';

// Mock Next.js navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/',
}));

describe('Navigation', () => {
  it('renders all navigation links', () => {
    render(<Navigation />);
    expect(screen.getByText('Explorer')).toBeInTheDocument();
    expect(screen.getByText('Search')).toBeInTheDocument();
    expect(screen.getByText('Favorites')).toBeInTheDocument();
    expect(screen.getByText('Workflows')).toBeInTheDocument();
    expect(screen.getByText('Architecture')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
  });

  it('highlights active link', () => {
    render(<Navigation />);
    const explorerLink = screen.getByText('Explorer').closest('a');
    expect(explorerLink).toHaveClass('bg-accent-default');
  });
});
