import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ArchitectureViewerPage from './page';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
  },
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
);

describe('ArchitectureViewerPage', () => {
  it('renders architecture viewer', () => {
    render(<ArchitectureViewerPage />, { wrapper });
    expect(screen.getByText(/Architecture Documentation/i)).toBeInTheDocument();
  });

  it('displays loading state initially', () => {
    render(<ArchitectureViewerPage />, { wrapper });
    expect(screen.getByText(/Loading architecture.../i)).toBeInTheDocument();
  });
});
