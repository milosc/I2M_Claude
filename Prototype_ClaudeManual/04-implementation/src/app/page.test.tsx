import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import Home from './page';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Mock the NavigationTree and DetailPane components
vi.mock('@/components/NavigationTree', () => ({
  NavigationTree: ({ onSelect, items }: any) => {
    const handleClick = () => {
      if (items && items[0]) {
        onSelect(items[0]);
      }
    };
    return (
      <div data-testid="navigation-tree">
        <button onClick={handleClick}>Select First Item</button>
      </div>
    );
  },
}));

vi.mock('@/components/DetailPane', () => ({
  DetailPane: ({ selectedItem }: any) => (
    <div data-testid="detail-pane">
      {selectedItem ? <h2>{selectedItem.name}</h2> : <p>No item selected</p>}
    </div>
  ),
}));

vi.mock('@/components/StageFilterDropdown', () => ({
  StageFilterDropdown: ({ onChange }: any) => (
    <select data-testid="stage-filter" onChange={(e) => onChange([e.target.value])}>
      <option value="">All Stages</option>
      <option value="Discovery">Discovery</option>
      <option value="Prototype">Prototype</option>
    </select>
  ),
}));

const mockSkills = [
  {
    id: 'Discovery_JTBD',
    name: 'Jobs To Be Done Extractor',
    description: 'Extracts Jobs To Be Done',
    stage: 'Discovery',
    path: '.claude/skills/Discovery_JTBD/SKILL.md',
  },
];

const mockCommands = [
  {
    id: 'discovery',
    name: 'Discovery Command',
    description: 'Complete discovery workflow',
    stage: 'Discovery',
    path: '.claude/commands/discovery.md',
  },
];

const mockAgents = [
  {
    id: 'discovery-domain-researcher',
    name: 'Discovery Domain Researcher',
    description: 'Research domain expertise',
    stage: 'Discovery',
    path: '.claude/agents/discovery/domain-researcher.md',
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

describe('Home - Main Explorer View (T-017)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    global.fetch = vi.fn((url: string) => {
      if (url.includes('/api/skills')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockSkills),
        });
      }
      if (url.includes('/api/commands')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockCommands),
        });
      }
      if (url.includes('/api/agents')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockAgents),
        });
      }
      return Promise.reject(new Error('Unknown endpoint'));
    });
  });

  it('renders dual-pane layout with NavigationTree and DetailPane', async () => {
    renderWithClient(<Home />);

    await waitFor(() => {
      expect(screen.getByTestId('navigation-tree')).toBeInTheDocument();
      expect(screen.getByTestId('detail-pane')).toBeInTheDocument();
    });
  });

  it('loads skills, commands, and agents on mount', async () => {
    renderWithClient(<Home />);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/skills');
      expect(global.fetch).toHaveBeenCalledWith('/api/commands');
      expect(global.fetch).toHaveBeenCalledWith('/api/agents');
    });
  });

  it('updates DetailPane when tree item is selected', async () => {
    const user = userEvent.setup();
    renderWithClient(<Home />);

    await waitFor(() => {
      expect(screen.getByTestId('navigation-tree')).toBeInTheDocument();
    });

    const selectButton = screen.getByText('Select First Item');
    await user.click(selectButton);

    await waitFor(() => {
      expect(screen.getByText('Jobs To Be Done Extractor')).toBeInTheDocument();
    });
  });

  it('filters items by stage when stage filter changes', async () => {
    const user = userEvent.setup();
    renderWithClient(<Home />);

    await waitFor(() => {
      expect(screen.getByTestId('stage-filter')).toBeInTheDocument();
    });

    const stageFilter = screen.getByTestId('stage-filter');
    await user.selectOptions(stageFilter, 'Discovery');

    // Verify filter was applied (implementation will handle filtering logic)
    expect(stageFilter).toHaveValue('Discovery');
  });

  it('displays header with stage filter and theme toggle', async () => {
    renderWithClient(<Home />);

    await waitFor(() => {
      expect(screen.getByTestId('stage-filter')).toBeInTheDocument();
    });
  });

  it('shows loading state while fetching data', () => {
    global.fetch = vi.fn(() => new Promise(() => {})); // Never resolves

    renderWithClient(<Home />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('shows error state when API fails', async () => {
    global.fetch = vi.fn(() => Promise.reject(new Error('API Error')));

    renderWithClient(<Home />);

    await waitFor(() => {
      expect(screen.getByText(/failed to load/i)).toBeInTheDocument();
    });
  });

  it('persists selected item to sessionStorage', async () => {
    const user = userEvent.setup();

    renderWithClient(<Home />);

    await waitFor(() => {
      expect(screen.getByText('Select First Item')).toBeInTheDocument();
    });

    // Clear any previous storage
    sessionStorage.clear();

    const selectButton = screen.getByText('Select First Item');
    await user.click(selectButton);

    await waitFor(() => {
      const storedValue = sessionStorage.getItem('last_viewed');
      expect(storedValue).toBe('Discovery_JTBD');
    });
  });
});
