import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ArchitectureBrowserPage from './page';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
  },
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
);

describe('ArchitectureBrowserPage', () => {
  it('renders architecture browser', () => {
    render(<ArchitectureBrowserPage />, { wrapper });
    expect(screen.getByText(/Architecture Browser/i)).toBeInTheDocument();
  });

  it('displays category tree', () => {
    render(<ArchitectureBrowserPage />, { wrapper });
    expect(screen.getByText(/C4 Diagrams/i)).toBeInTheDocument();
    expect(screen.getByText(/ADRs/i)).toBeInTheDocument();
  });
});
