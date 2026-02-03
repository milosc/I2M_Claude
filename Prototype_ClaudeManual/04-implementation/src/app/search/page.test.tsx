import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import SearchPage from './page';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Mock components
vi.mock('@/components/SearchResultCard', () => ({
  SearchResultCard: ({ item }: any) => (
    <div data-testid={`result-${item.id}`}>
      <h3>{item.name}</h3>
      <p>{item.description}</p>
    </div>
  ),
}));

vi.mock('@/components/StageFilterDropdown', () => ({
  StageFilterDropdown: ({ onChange }: any) => (
    <select data-testid="stage-filter" onChange={(e) => onChange([e.target.value])}>
      <option value="">All Stages</option>
      <option value="Discovery">Discovery</option>
    </select>
  ),
}));

const mockSearchResults = [
  {
    id: 'Discovery_JTBD',
    name: 'Jobs To Be Done Extractor',
    description: 'Extracts Jobs To Be Done',
    stage: 'Discovery',
    path: '.claude/skills/Discovery_JTBD/SKILL.md',
    type: 'Skill',
  },
  {
    id: 'Discovery_GeneratePersona',
    name: 'Persona Generator',
    description: 'Generates persona documents',
    stage: 'Discovery',
    path: '.claude/skills/Discovery_GeneratePersona/SKILL.md',
    type: 'Skill',
  },
];

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });
}

function renderWithClient(ui: React.ReactElement) {
  const queryClient = createTestQueryClient();
  return render(<QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>);
}

describe('SearchPage (T-018)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    global.fetch = vi.fn((url: string) => {
      if (url.includes('/api/search')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockSearchResults),
        });
      }
      return Promise.reject(new Error('Unknown endpoint'));
    });
  });

  it('renders search results from URL query param', async () => {
    // Mock useSearchParams
    const mockSearchParams = new URLSearchParams('?q=persona');
    vi.mock('next/navigation', () => ({
      useSearchParams: () => mockSearchParams,
      useRouter: () => ({ push: vi.fn() }),
    }));

    renderWithClient(<SearchPage />);

    await waitFor(() => {
      expect(screen.getByTestId('result-Discovery_JTBD')).toBeInTheDocument();
      expect(screen.getByTestId('result-Discovery_GeneratePersona')).toBeInTheDocument();
    });
  });

  it('calls search API with query parameter', async () => {
    const mockSearchParams = new URLSearchParams('?q=persona');
    vi.mock('next/navigation', () => ({
      useSearchParams: () => mockSearchParams,
      useRouter: () => ({ push: vi.fn() }),
    }));

    renderWithClient(<SearchPage />);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/api/search'));
      expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('q=persona'));
    });
  });

  it('displays result count and performance indicator', async () => {
    const mockSearchParams = new URLSearchParams('?q=test');
    vi.mock('next/navigation', () => ({
      useSearchParams: () => mockSearchParams,
      useRouter: () => ({ push: vi.fn() }),
    }));

    renderWithClient(<SearchPage />);

    await waitFor(() => {
      expect(screen.getByText(/2 results/i)).toBeInTheDocument();
    });
  });

  it('filters results by stage', async () => {
    const user = userEvent.setup();
    const mockSearchParams = new URLSearchParams('?q=test');
    vi.mock('next/navigation', () => ({
      useSearchParams: () => mockSearchParams,
      useRouter: () => ({ push: vi.fn() }),
    }));

    renderWithClient(<SearchPage />);

    await waitFor(() => {
      expect(screen.getByTestId('stage-filter')).toBeInTheDocument();
    });

    const stageFilter = screen.getByTestId('stage-filter');
    await user.selectOptions(stageFilter, 'Discovery');

    expect(stageFilter).toHaveValue('Discovery');
  });

  it('shows empty state when no results', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve([]),
      })
    );

    const mockSearchParams = new URLSearchParams('?q=nonexistent');
    vi.mock('next/navigation', () => ({
      useSearchParams: () => mockSearchParams,
      useRouter: () => ({ push: vi.fn() }),
    }));

    renderWithClient(<SearchPage />);

    await waitFor(() => {
      expect(screen.getByText(/no results/i)).toBeInTheDocument();
    });
  });

  it('shows loading state while fetching', () => {
    global.fetch = vi.fn(() => new Promise(() => {})); // Never resolves

    const mockSearchParams = new URLSearchParams('?q=test');
    vi.mock('next/navigation', () => ({
      useSearchParams: () => mockSearchParams,
      useRouter: () => ({ push: vi.fn() }),
    }));

    renderWithClient(<SearchPage />);

    expect(screen.getByText(/searching/i)).toBeInTheDocument();
  });

  it('has Back to Explorer link', async () => {
    const mockSearchParams = new URLSearchParams('?q=test');
    vi.mock('next/navigation', () => ({
      useSearchParams: () => mockSearchParams,
      useRouter: () => ({ push: vi.fn() }),
    }));

    renderWithClient(<SearchPage />);

    await waitFor(() => {
      expect(screen.getByText(/back to explorer/i)).toBeInTheDocument();
    });
  });
});
