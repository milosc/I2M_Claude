import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import WorkflowViewerPage from './page';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
  },
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
);

describe('WorkflowViewerPage', () => {
  it('renders workflow viewer with diagram', () => {
    render(<WorkflowViewerPage />, { wrapper });
    expect(screen.getByText(/Workflow Viewer/i)).toBeInTheDocument();
  });

  it('displays zoom controls', () => {
    render(<WorkflowViewerPage />, { wrapper });
    expect(screen.getByRole('button', { name: /zoom in/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /zoom out/i })).toBeInTheDocument();
  });

  it('shows export options', () => {
    render(<WorkflowViewerPage />, { wrapper });
    expect(screen.getByText(/Export/i)).toBeInTheDocument();
  });
});
