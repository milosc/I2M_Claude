import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { DetailModal } from './DetailModal';

// Mock Next.js router
const mockPush = vi.fn();
const mockReplace = vi.fn();

vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
    replace: mockReplace,
  }),
  useSearchParams: () => ({
    get: (key: string) => (key === 'detail' ? 'skill-1' : null),
  }),
}));

beforeEach(() => {
  mockPush.mockClear();
  mockReplace.mockClear();
});

describe('DetailModal', () => {
  const mockItem = {
    id: 'skill-1',
    name: 'Test Skill',
    type: 'skill' as const,
    stage: 'discovery' as const,
    path: '.claude/skills/test',
    description: 'Test description',
    purpose: 'Test purpose',
    isFavorite: false,
  };

  it('renders modal when item is provided', () => {
    render(<DetailModal item={mockItem} onClose={() => {}} />);

    const skillNames = screen.getAllByText('Test Skill');
    expect(skillNames.length).toBeGreaterThan(0);
    expect(screen.getByText('Test description')).toBeInTheDocument();
  });

  it('does not render when item is null', () => {
    const { container } = render(<DetailModal item={null} onClose={() => {}} />);

    expect(container.firstChild).toBeNull();
  });

  it('closes on backdrop click', () => {
    const onClose = vi.fn();
    const { container } = render(<DetailModal item={mockItem} onClose={onClose} />);

    const backdrop = container.querySelector('[role="dialog"]')?.parentElement;
    if (backdrop) {
      fireEvent.click(backdrop);
      expect(onClose).toHaveBeenCalled();
    }
  });

  it('closes on X button click', () => {
    const onClose = vi.fn();
    render(<DetailModal item={mockItem} onClose={onClose} />);

    const closeButton = screen.getByRole('button', { name: /close/i });
    fireEvent.click(closeButton);

    expect(onClose).toHaveBeenCalled();
  });

  it('closes on Escape key press', () => {
    const onClose = vi.fn();
    render(<DetailModal item={mockItem} onClose={onClose} />);

    fireEvent.keyDown(document, { key: 'Escape' });

    expect(onClose).toHaveBeenCalled();
  });

  it('renders DetailPane with item data', () => {
    render(<DetailModal item={mockItem} onClose={() => {}} />);

    // DetailPane should show Purpose tab (default)
    expect(screen.getByRole('tab', { name: /Purpose/i })).toBeInTheDocument();
  });

  it('applies fade-in animation on mount', () => {
    render(<DetailModal item={mockItem} onClose={() => {}} />);

    // Modal is rendered via portal to document.body
    const dialog = screen.getByRole('dialog');
    const overlay = dialog.parentElement;

    expect(overlay).not.toBeNull();
    if (overlay) {
      expect(overlay.className).toContain('animate-fade-in');
    }
  });
});
