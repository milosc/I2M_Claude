import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { DiagramViewer } from './DiagramViewer';

const mockMermaidCode = `graph TD
  A[Start] --> B[Process]
  B --> C[End]`;

const mockPlantUMLCode = `@startuml
Alice -> Bob: Hello
Bob --> Alice: Hi
@enduml`;

describe('DiagramViewer', () => {
  describe('Rendering', () => {
    it('renders diagram container', () => {
      render(<DiagramViewer code={mockMermaidCode} format="mermaid" />);

      expect(screen.getByRole('region', { name: /diagram viewer/i })).toBeInTheDocument();
    });

    it('renders mermaid diagram', async () => {
      render(<DiagramViewer code={mockMermaidCode} format="mermaid" />);

      await waitFor(() => {
        expect(screen.getByTestId('diagram-canvas')).toBeInTheDocument();
      });
    });

    it('renders toolbar with controls', () => {
      render(<DiagramViewer code={mockMermaidCode} format="mermaid" />);

      expect(screen.getByRole('toolbar', { name: /diagram controls/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /zoom in/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /zoom out/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /reset zoom/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /fullscreen/i })).toBeInTheDocument();
    });

    it('shows zoom level indicator', () => {
      render(<DiagramViewer code={mockMermaidCode} format="mermaid" initialZoom={1.5} />);

      const toolbar = screen.getByRole('toolbar', { name: /diagram controls/i });
      expect(toolbar).toHaveTextContent('150%');
    });
  });

  describe('Zoom Controls', () => {
    it('increases zoom when zoom in is clicked', async () => {
      const user = userEvent.setup();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" initialZoom={1.0} />);

      const zoomInButton = screen.getByRole('button', { name: /zoom in/i });
      await user.click(zoomInButton);

      const toolbar = screen.getByRole('toolbar', { name: /diagram controls/i });
      expect(toolbar).toHaveTextContent('110%');
    });

    it('decreases zoom when zoom out is clicked', async () => {
      const user = userEvent.setup();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" initialZoom={1.0} />);

      const zoomOutButton = screen.getByRole('button', { name: /zoom out/i });
      await user.click(zoomOutButton);

      const toolbar = screen.getByRole('toolbar', { name: /diagram controls/i });
      expect(toolbar).toHaveTextContent('90%');
    });

    it('resets zoom to 100% when reset is clicked', async () => {
      const user = userEvent.setup();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" initialZoom={1.5} />);

      const toolbar = screen.getByRole('toolbar', { name: /diagram controls/i });
      expect(toolbar).toHaveTextContent('150%');

      const resetButton = screen.getByRole('button', { name: /reset zoom/i });
      await user.click(resetButton);

      expect(toolbar).toHaveTextContent('100%');
    });

    it('limits maximum zoom to 300%', async () => {
      const user = userEvent.setup();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" initialZoom={2.9} />);

      const toolbar = screen.getByRole('toolbar', { name: /diagram controls/i });
      const zoomInButton = screen.getByRole('button', { name: /zoom in/i });

      await user.click(zoomInButton);
      await user.click(zoomInButton);

      expect(toolbar).toHaveTextContent('300%');

      await user.click(zoomInButton);
      expect(toolbar).toHaveTextContent('300%');
    });

    it('limits minimum zoom to 25%', async () => {
      const user = userEvent.setup();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" initialZoom={0.3} />);

      const toolbar = screen.getByRole('toolbar', { name: /diagram controls/i });
      const zoomOutButton = screen.getByRole('button', { name: /zoom out/i });

      await user.click(zoomOutButton);
      await user.click(zoomOutButton);

      expect(toolbar).toHaveTextContent('25%');

      await user.click(zoomOutButton);
      expect(toolbar).toHaveTextContent('25%');
    });
  });

  describe('Fullscreen Mode', () => {
    it('enters fullscreen when fullscreen button is clicked', async () => {
      const user = userEvent.setup();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" />);

      const fullscreenButton = screen.getByRole('button', { name: /fullscreen/i });
      await user.click(fullscreenButton);

      const container = screen.getByRole('region', { name: /diagram viewer/i });
      expect(container).toHaveClass('fixed', 'inset-0', 'z-50');
    });

    it('exits fullscreen when exit fullscreen button is clicked', async () => {
      const user = userEvent.setup();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" />);

      const fullscreenButton = screen.getByRole('button', { name: /fullscreen/i });
      await user.click(fullscreenButton);

      const exitButton = screen.getByRole('button', { name: /exit fullscreen/i });
      await user.click(exitButton);

      const container = screen.getByRole('region', { name: /diagram viewer/i });
      expect(container).not.toHaveClass('fixed', 'inset-0', 'z-50');
    });

    it('exits fullscreen when escape key is pressed', async () => {
      const user = userEvent.setup();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" />);

      const fullscreenButton = screen.getByRole('button', { name: /fullscreen/i });
      await user.click(fullscreenButton);

      await user.keyboard('{Escape}');

      const container = screen.getByRole('region', { name: /diagram viewer/i });
      expect(container).not.toHaveClass('fixed', 'inset-0', 'z-50');
    });
  });

  describe('Export Functionality', () => {
    it('shows export button when onExport is provided', () => {
      const handleExport = vi.fn();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" onExport={handleExport} />);

      expect(screen.getByRole('button', { name: /export/i })).toBeInTheDocument();
    });

    it('does not show export button when onExport is not provided', () => {
      render(<DiagramViewer code={mockMermaidCode} format="mermaid" />);

      expect(screen.queryByRole('button', { name: /export/i })).not.toBeInTheDocument();
    });

    it('shows export menu when export button is clicked', async () => {
      const user = userEvent.setup();
      const handleExport = vi.fn();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" onExport={handleExport} />);

      const exportButton = screen.getByRole('button', { name: /export/i });
      await user.click(exportButton);

      expect(screen.getByRole('menuitem', { name: /png/i })).toBeInTheDocument();
      expect(screen.getByRole('menuitem', { name: /svg/i })).toBeInTheDocument();
      expect(screen.getByRole('menuitem', { name: /pdf/i })).toBeInTheDocument();
    });

    it('calls onExport with PNG format', async () => {
      const user = userEvent.setup();
      const handleExport = vi.fn();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" onExport={handleExport} />);

      const exportButton = screen.getByRole('button', { name: /export/i });
      await user.click(exportButton);

      const pngOption = screen.getByRole('menuitem', { name: /png/i });
      await user.click(pngOption);

      expect(handleExport).toHaveBeenCalledWith('png');
    });

    it('calls onExport with SVG format', async () => {
      const user = userEvent.setup();
      const handleExport = vi.fn();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" onExport={handleExport} />);

      const exportButton = screen.getByRole('button', { name: /export/i });
      await user.click(exportButton);

      const svgOption = screen.getByRole('menuitem', { name: /svg/i });
      await user.click(svgOption);

      expect(handleExport).toHaveBeenCalledWith('svg');
    });

    it('calls onExport with PDF format', async () => {
      const user = userEvent.setup();
      const handleExport = vi.fn();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" onExport={handleExport} />);

      const exportButton = screen.getByRole('button', { name: /export/i });
      await user.click(exportButton);

      const pdfOption = screen.getByRole('menuitem', { name: /pdf/i });
      await user.click(pdfOption);

      expect(handleExport).toHaveBeenCalledWith('pdf');
    });
  });

  describe('Pan Functionality', () => {
    it('enables pan mode when pan button is clicked', async () => {
      const user = userEvent.setup();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" />);

      const panButton = screen.getByRole('button', { name: /pan/i });
      await user.click(panButton);

      expect(panButton).toHaveAttribute('aria-pressed', 'true');
    });

    it('changes cursor to grab in pan mode', async () => {
      const user = userEvent.setup();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" />);

      const panButton = screen.getByRole('button', { name: /pan/i });
      await user.click(panButton);

      const canvas = screen.getByTestId('diagram-canvas');
      expect(canvas).toHaveClass('cursor-grab');
    });
  });

  describe('Diagram Format', () => {
    it('handles mermaid format', async () => {
      render(<DiagramViewer code={mockMermaidCode} format="mermaid" />);

      await waitFor(() => {
        expect(screen.getByTestId('diagram-canvas')).toBeInTheDocument();
      });
    });

    it('handles plantuml format', async () => {
      render(<DiagramViewer code={mockPlantUMLCode} format="plantuml" />);

      await waitFor(() => {
        expect(screen.getByTestId('diagram-canvas')).toBeInTheDocument();
      });
    });
  });

  describe('Error Handling', () => {
    it('shows error message for invalid mermaid syntax', async () => {
      const invalidCode = 'invalid mermaid code!!!';

      render(<DiagramViewer code={invalidCode} format="mermaid" />);

      await waitFor(() => {
        expect(screen.getByText(/error rendering diagram/i)).toBeInTheDocument();
      });
    });

    it('shows retry button on error', async () => {
      const invalidCode = 'invalid mermaid code!!!';

      render(<DiagramViewer code={invalidCode} format="mermaid" />);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
      });
    });
  });

  describe('Accessibility', () => {
    it('has correct ARIA labels', () => {
      render(<DiagramViewer code={mockMermaidCode} format="mermaid" />);

      expect(screen.getByRole('region', { name: /diagram viewer/i })).toBeInTheDocument();
      expect(screen.getByRole('toolbar', { name: /diagram controls/i })).toBeInTheDocument();
    });

    it('supports keyboard navigation for controls', async () => {
      const user = userEvent.setup();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" initialZoom={1.0} />);

      const toolbar = screen.getByRole('toolbar', { name: /diagram controls/i });
      const zoomInButton = screen.getByRole('button', { name: /zoom in/i });
      zoomInButton.focus();

      await user.keyboard('{Enter}');

      expect(toolbar).toHaveTextContent('110%');
    });

    it('provides status updates for screen readers', async () => {
      const user = userEvent.setup();

      render(<DiagramViewer code={mockMermaidCode} format="mermaid" initialZoom={1.0} />);

      const zoomInButton = screen.getByRole('button', { name: /zoom in/i });
      await user.click(zoomInButton);

      expect(screen.getByRole('status')).toHaveTextContent(/zoom: 110%/i);
    });
  });
});
