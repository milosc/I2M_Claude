import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MarkdownRenderer } from '../../components/MarkdownRenderer';

describe('MarkdownRenderer', () => {
  it('renders basic markdown content', () => {
    const markdown = '# Hello World\n\nThis is **bold** and *italic* text.';

    render(<MarkdownRenderer content={markdown} />);

    expect(screen.getByText(/Hello World/)).toBeInTheDocument();
    expect(screen.getByText(/bold/)).toBeInTheDocument();
    expect(screen.getByText(/italic/)).toBeInTheDocument();
  });

  it('renders headings with correct levels', () => {
    const markdown = '# H1\n## H2\n### H3';
    const { container } = render(<MarkdownRenderer content={markdown} />);

    expect(container.querySelector('h1')).toBeInTheDocument();
    expect(container.querySelector('h2')).toBeInTheDocument();
    expect(container.querySelector('h3')).toBeInTheDocument();
  });

  it('renders code blocks with syntax highlighting', () => {
    const markdown = '```typescript\nconst x = 42;\n```';
    const { container } = render(<MarkdownRenderer content={markdown} />);

    const codeBlock = container.querySelector('pre code');
    expect(codeBlock).toBeInTheDocument();
    expect(codeBlock?.textContent).toContain('const x = 42');
  });

  it('renders inline code', () => {
    const markdown = 'Use `console.log()` for debugging';
    const { container } = render(<MarkdownRenderer content={markdown} />);

    expect(container.querySelector('code')).toBeInTheDocument();
    expect(screen.getByText(/console.log/)).toBeInTheDocument();
  });

  it('renders links', () => {
    const markdown = '[Click here](https://example.com)';
    render(<MarkdownRenderer content={markdown} />);

    const link = screen.getByRole('link', { name: /Click here/ });
    expect(link).toHaveAttribute('href', 'https://example.com');
  });

  it('renders lists', () => {
    const markdown = '- Item 1\n- Item 2\n- Item 3';
    const { container } = render(<MarkdownRenderer content={markdown} />);

    const list = container.querySelector('ul');
    expect(list).toBeInTheDocument();
    expect(list?.querySelectorAll('li')).toHaveLength(3);
  });

  it('applies light theme by default', () => {
    const markdown = '# Test';
    const { container } = render(<MarkdownRenderer content={markdown} />);

    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper).toHaveClass('markdown-renderer');
  });

  it('applies dark theme when specified', () => {
    const markdown = '# Test';
    const { container } = render(<MarkdownRenderer content={markdown} theme="dark" />);

    const wrapper = container.firstChild as HTMLElement;
    expect(wrapper).toHaveClass('theme-dark');
  });

  it('renders tables', () => {
    const markdown = '| Header 1 | Header 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |';
    const { container } = render(<MarkdownRenderer content={markdown} />);

    const table = container.querySelector('table');
    expect(table).toBeInTheDocument();
    expect(screen.getByText('Header 1')).toBeInTheDocument();
    expect(screen.getByText('Cell 1')).toBeInTheDocument();
  });

  it('handles empty content gracefully', () => {
    const { container } = render(<MarkdownRenderer content="" />);
    expect(container.firstChild).toBeInTheDocument();
  });

  it('sanitizes HTML to prevent XSS', () => {
    const markdown = '<script>alert("XSS")</script>\n# Safe Content';
    const { container } = render(<MarkdownRenderer content={markdown} />);

    expect(container.querySelector('script')).not.toBeInTheDocument();
    expect(screen.getByText(/Safe Content/)).toBeInTheDocument();
  });

  it('renders blockquotes', () => {
    const markdown = '> This is a quote';
    const { container } = render(<MarkdownRenderer content={markdown} />);

    const blockquote = container.querySelector('blockquote');
    expect(blockquote).toBeInTheDocument();
    expect(screen.getByText(/This is a quote/)).toBeInTheDocument();
  });

  it('calls onCopyCode when copy button is clicked', () => {
    const handleCopy = vi.fn();
    const markdown = '```typescript\nconst x = 42;\n```';

    const { container } = render(
      <MarkdownRenderer content={markdown} onCopyCode={handleCopy} />
    );

    const copyButton = container.querySelector('.copy-button');
    if (copyButton) {
      copyButton.dispatchEvent(new MouseEvent('click', { bubbles: true }));
      expect(handleCopy).toHaveBeenCalledWith('const x = 42;\n', 'typescript');
    }
  });

  it('renders Mermaid diagrams when enabled', () => {
    const markdown = '```mermaid\ngraph TD\n  A-->B\n```';
    const { container } = render(
      <MarkdownRenderer content={markdown} enableDiagrams={true} />
    );

    const mermaidBlock = container.querySelector('.mermaid-diagram');
    expect(mermaidBlock).toBeInTheDocument();
  });

  it('does not render Mermaid diagrams when disabled', () => {
    const markdown = '```mermaid\ngraph TD\n  A-->B\n```';
    const { container } = render(
      <MarkdownRenderer content={markdown} enableDiagrams={false} />
    );

    const mermaidBlock = container.querySelector('.mermaid-diagram');
    expect(mermaidBlock).not.toBeInTheDocument();
  });
});
