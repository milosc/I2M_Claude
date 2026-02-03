import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { FrontmatterDisplay } from '../../components/FrontmatterDisplay';
import type { FrontmatterAttributes } from '../../components/DetailPane';

const skillFrontmatter: FrontmatterAttributes = {
  model: 'sonnet',
  context: 'fork',
  agent: null,
  allowed_tools: ['Read', 'Write', 'Grep'],
  skills_required: ['Discovery_InterviewAnalysis'],
};

const commandFrontmatter: FrontmatterAttributes = {
  model: 'sonnet',
  argument_hint: '<SystemName> <InputPath>',
  allowed_tools: ['Read', 'Write', 'Bash'],
  invokes_skills: ['Discovery_JTBD', 'Discovery_GeneratePersona'],
  orchestrates_agents: ['discovery-domain-researcher'],
};

const agentFrontmatter: FrontmatterAttributes = {
  model: 'sonnet',
  checkpoint: 3,
  color: 'blue',
  loads_skills: ['Discovery_GeneratePersona'],
  spawned_by: ['discovery-multiagent'],
};

describe('FrontmatterDisplay', () => {
  it('renders nothing when frontmatter has no displayable keys', () => {
    const emptyFrontmatter: FrontmatterAttributes = {
      name: 'test',
      description: 'test description',
    };
    const { container } = render(
      <FrontmatterDisplay frontmatter={emptyFrontmatter} type="skill" />
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders frontmatter section header', () => {
    render(<FrontmatterDisplay frontmatter={skillFrontmatter} type="skill" />);
    expect(screen.getByText('Frontmatter')).toBeInTheDocument();
  });

  describe('skill type', () => {
    it('displays model value', () => {
      render(<FrontmatterDisplay frontmatter={skillFrontmatter} type="skill" />);
      expect(screen.getByText('sonnet')).toBeInTheDocument();
    });

    it('displays context value', () => {
      render(<FrontmatterDisplay frontmatter={skillFrontmatter} type="skill" />);
      expect(screen.getByText('fork')).toBeInTheDocument();
    });

    it('displays null values with italic styling', () => {
      render(<FrontmatterDisplay frontmatter={skillFrontmatter} type="skill" />);
      const nullElements = screen.getAllByText('null');
      expect(nullElements.length).toBeGreaterThan(0);
      expect(nullElements[0]).toHaveClass('italic');
    });

    it('displays array values as badges', () => {
      render(<FrontmatterDisplay frontmatter={skillFrontmatter} type="skill" />);
      expect(screen.getByText('Read')).toBeInTheDocument();
      expect(screen.getByText('Write')).toBeInTheDocument();
      expect(screen.getByText('Grep')).toBeInTheDocument();
    });

    it('follows skill display order', () => {
      const { container } = render(
        <FrontmatterDisplay frontmatter={skillFrontmatter} type="skill" />
      );
      const labels = container.querySelectorAll('dt');
      const labelTexts = Array.from(labels).map(l => l.textContent?.toLowerCase());

      // model should appear before context in skill order
      const modelIndex = labelTexts.findIndex(t => t?.includes('model'));
      const contextIndex = labelTexts.findIndex(t => t?.includes('context'));
      expect(modelIndex).toBeLessThan(contextIndex);
    });
  });

  describe('command type', () => {
    it('displays argument_hint', () => {
      render(<FrontmatterDisplay frontmatter={commandFrontmatter} type="command" />);
      expect(screen.getByText('<SystemName> <InputPath>')).toBeInTheDocument();
    });

    it('displays invokes_skills array', () => {
      render(<FrontmatterDisplay frontmatter={commandFrontmatter} type="command" />);
      expect(screen.getByText('Discovery_JTBD')).toBeInTheDocument();
      expect(screen.getByText('Discovery_GeneratePersona')).toBeInTheDocument();
    });

    it('displays orchestrates_agents array', () => {
      render(<FrontmatterDisplay frontmatter={commandFrontmatter} type="command" />);
      expect(screen.getByText('discovery-domain-researcher')).toBeInTheDocument();
    });
  });

  describe('agent type', () => {
    it('displays checkpoint number', () => {
      render(<FrontmatterDisplay frontmatter={agentFrontmatter} type="agent" />);
      expect(screen.getByText('3')).toBeInTheDocument();
    });

    it('displays color value', () => {
      render(<FrontmatterDisplay frontmatter={agentFrontmatter} type="agent" />);
      expect(screen.getByText('blue')).toBeInTheDocument();
    });

    it('displays loads_skills array', () => {
      render(<FrontmatterDisplay frontmatter={agentFrontmatter} type="agent" />);
      expect(screen.getByText('Discovery_GeneratePersona')).toBeInTheDocument();
    });

    it('displays spawned_by array', () => {
      render(<FrontmatterDisplay frontmatter={agentFrontmatter} type="agent" />);
      expect(screen.getByText('discovery-multiagent')).toBeInTheDocument();
    });
  });

  describe('value rendering', () => {
    it('renders empty array with brackets', () => {
      const frontmatter: FrontmatterAttributes = {
        model: 'sonnet',
        allowed_tools: [],
      };
      render(<FrontmatterDisplay frontmatter={frontmatter} type="skill" />);
      expect(screen.getByText('[]')).toBeInTheDocument();
    });

    it('renders boolean true with green color', () => {
      const frontmatter: FrontmatterAttributes = {
        model: 'sonnet',
        enabled: true,
      };
      render(<FrontmatterDisplay frontmatter={frontmatter} type="skill" />);
      const trueElement = screen.getByText('true');
      expect(trueElement).toHaveClass('text-green-600');
    });

    it('renders boolean false with gray color', () => {
      const frontmatter: FrontmatterAttributes = {
        model: 'sonnet',
        enabled: false,
      };
      render(<FrontmatterDisplay frontmatter={frontmatter} type="skill" />);
      const falseElement = screen.getByText('false');
      expect(falseElement).toHaveClass('text-gray-400');
    });

    it('renders number with purple color', () => {
      render(<FrontmatterDisplay frontmatter={agentFrontmatter} type="agent" />);
      const numberElement = screen.getByText('3');
      expect(numberElement).toHaveClass('text-purple-600');
    });

    it('converts underscores to spaces in labels', () => {
      render(<FrontmatterDisplay frontmatter={skillFrontmatter} type="skill" />);
      expect(screen.getByText(/allowed tools/i)).toBeInTheDocument();
      expect(screen.getByText(/skills required/i)).toBeInTheDocument();
    });
  });

  describe('unknown type fallback', () => {
    it('displays all frontmatter keys for unknown type', () => {
      const customFrontmatter: FrontmatterAttributes = {
        custom_field: 'custom value',
        another_field: 'another value',
      };
      render(<FrontmatterDisplay frontmatter={customFrontmatter} type="rule" />);
      expect(screen.getByText('custom value')).toBeInTheDocument();
      expect(screen.getByText('another value')).toBeInTheDocument();
    });
  });
});
