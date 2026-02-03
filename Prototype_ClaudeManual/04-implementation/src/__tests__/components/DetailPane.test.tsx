import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { DetailPane } from '../../components/DetailPane';
import type { ComponentDetail } from '../../components/DetailPane';

const mockSkillItem: ComponentDetail = {
  id: 'skill-001',
  name: 'Discovery_Domain_Researcher',
  type: 'skill',
  stage: 'discovery',
  path: '.claude/skills/Discovery_Domain_Researcher/SKILL.md',
  description: 'Researches domain models and business rules',
  frontmatter: {
    model: 'sonnet',
    context: 'fork',
    agent: null,
    allowed_tools: ['Read', 'Write', 'Grep'],
    skills_required: ['Discovery_InterviewAnalysis'],
  },
  rawContent: '# Discovery_Domain_Researcher\n\n## Purpose\n\nExtracts domain models from client materials.\n\n## When to Use\n\n- During Discovery phase\n- After interview analysis\n\n## Workflow\n\n1. Read client materials\n2. Extract domain terms\n3. Generate domain model',
  purpose: '# Purpose\n\nExtracts domain models from client materials.',
  examples: [
    {
      title: 'Basic Usage',
      language: 'bash',
      code: '/discovery-domain-research ClientMaterials/',
    },
  ],
  options: [
    {
      parameter: '--output',
      type: 'string',
      required: false,
      defaultValue: './output',
      description: 'Output directory',
    },
  ],
  workflow: {
    format: 'mermaid',
    code: 'graph TD\n  A-->B',
    description: 'Domain research workflow',
  },
  traceability: [
    { type: 'input', id: 'CM-001', label: 'Client Materials' },
    { type: 'output', id: 'DOMAIN-001', label: 'Domain Model' },
  ],
  isFavorite: false,
};

const mockCommandItem: ComponentDetail = {
  id: 'cmd-001',
  name: 'discovery',
  type: 'command',
  stage: 'discovery',
  path: '.claude/commands/discovery.md',
  description: 'Run complete discovery analysis',
  frontmatter: {
    model: 'sonnet',
    argument_hint: '<SystemName> <InputPath>',
    allowed_tools: ['Read', 'Write', 'Bash'],
    invokes_skills: ['Discovery_JTBD', 'Discovery_GeneratePersona'],
    orchestrates_agents: ['discovery-domain-researcher'],
  },
  rawContent: '# /discovery\n\n## Purpose\n\nOrchestrates discovery workflow from client materials to structured documentation.\n\n## Usage\n\n```bash\n/discovery <SystemName> <InputPath>\n```',
  purpose: '# Purpose\n\nOrchestrates discovery workflow.',
  examples: [
    {
      title: 'Full Discovery',
      language: 'bash',
      code: '/discovery SystemName ClientMaterials/',
    },
  ],
  options: [
    {
      parameter: '--resume',
      type: 'boolean',
      required: false,
      description: 'Resume from checkpoint',
    },
  ],
  isFavorite: true,
};

const mockAgentItem: ComponentDetail = {
  id: 'agent-001',
  name: 'discovery-persona-synthesizer',
  type: 'agent',
  stage: 'discovery',
  path: '.claude/agents/discovery/persona-synthesizer.md',
  description: 'Coordinates persona generation from research',
  frontmatter: {
    model: 'sonnet',
    checkpoint: 3,
    color: 'blue',
    loads_skills: ['Discovery_GeneratePersona'],
    spawned_by: ['discovery-multiagent'],
  },
  rawContent: '# discovery-persona-synthesizer\n\n## Role\n\nCoordinates multi-agent persona synthesis from pain points and user research.',
  isFavorite: false,
};

describe('DetailPane', () => {
  it('renders empty state when no item selected', () => {
    render(<DetailPane item={null} />);
    expect(screen.getByText(/Select a component to view details/i)).toBeInTheDocument();
  });

  it('renders loading state', () => {
    render(<DetailPane item={null} loading={true} />);
    expect(screen.getByText(/Loading/i)).toBeInTheDocument();
  });

  it('renders error state', () => {
    render(<DetailPane item={null} error="Failed to load component" />);
    expect(screen.getByText(/Failed to load component/i)).toBeInTheDocument();
  });

  it('renders Purpose tab by default', () => {
    render(<DetailPane item={mockSkillItem} />);
    expect(screen.getByRole('tab', { name: /Purpose/i })).toBeInTheDocument();
    expect(screen.getByText(/Extracts domain models/i)).toBeInTheDocument();
  });

  it('renders rawContent in Purpose tab when available', () => {
    render(<DetailPane item={mockSkillItem} />);
    // rawContent should be rendered, which includes "When to Use" section
    expect(screen.getByText(/When to Use/i)).toBeInTheDocument();
  });

  it('renders all tabs for skill type', () => {
    render(<DetailPane item={mockSkillItem} />);

    expect(screen.getByRole('tab', { name: /Purpose/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /Examples/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /Options/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /Workflow/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /Traceability/i })).toBeInTheDocument();
  });

  it('does not render Traceability tab for command type', () => {
    render(<DetailPane item={mockCommandItem} />);

    expect(screen.getByRole('tab', { name: /Purpose/i })).toBeInTheDocument();
    expect(screen.queryByRole('tab', { name: /Traceability/i })).not.toBeInTheDocument();
  });

  it('switches to Examples tab on click', () => {
    render(<DetailPane item={mockSkillItem} />);

    const examplesTab = screen.getByRole('tab', { name: /Examples/i });
    fireEvent.click(examplesTab);

    expect(screen.getByText(/Basic Usage/i)).toBeInTheDocument();
    expect(screen.getByText(/\/discovery-domain-research/i)).toBeInTheDocument();
  });

  it('switches to Options tab on click', () => {
    render(<DetailPane item={mockSkillItem} />);

    const optionsTab = screen.getByRole('tab', { name: /Options/i });
    fireEvent.click(optionsTab);

    expect(screen.getByText(/--output/i)).toBeInTheDocument();
    expect(screen.getByText(/Output directory/i)).toBeInTheDocument();
  });

  it('switches to Workflow tab on click', () => {
    render(<DetailPane item={mockSkillItem} />);

    const workflowTab = screen.getByRole('tab', { name: /Workflow/i });
    fireEvent.click(workflowTab);

    expect(screen.getByText(/Domain research workflow/i)).toBeInTheDocument();
  });

  it('switches to Traceability tab on click', () => {
    render(<DetailPane item={mockSkillItem} />);

    const traceabilityTab = screen.getByRole('tab', { name: /Traceability/i });
    fireEvent.click(traceabilityTab);

    expect(screen.getByText('CM-001 - Client Materials')).toBeInTheDocument();
    expect(screen.getByText('DOMAIN-001 - Domain Model')).toBeInTheDocument();
  });

  it('calls onTabChange when tab is clicked', () => {
    const handleTabChange = vi.fn();
    render(<DetailPane item={mockSkillItem} onTabChange={handleTabChange} />);

    const examplesTab = screen.getByRole('tab', { name: /Examples/i });
    fireEvent.click(examplesTab);

    expect(handleTabChange).toHaveBeenCalledWith('examples');
  });

  it('renders Copy Path button', () => {
    render(<DetailPane item={mockSkillItem} />);
    expect(screen.getByRole('button', { name: /Copy Path/i })).toBeInTheDocument();
  });

  it('calls onCopyPath when Copy Path button is clicked', () => {
    const handleCopyPath = vi.fn();
    render(<DetailPane item={mockSkillItem} onCopyPath={handleCopyPath} />);

    const copyButton = screen.getByRole('button', { name: /Copy Path/i });
    fireEvent.click(copyButton);

    expect(handleCopyPath).toHaveBeenCalledWith(mockSkillItem.path);
  });

  it('renders Add to Favorites button', () => {
    render(<DetailPane item={mockSkillItem} />);
    expect(screen.getByRole('button', { name: /Add to Favorites/i })).toBeInTheDocument();
  });

  it('renders Remove from Favorites button when item is favorite', () => {
    render(<DetailPane item={mockCommandItem} />);
    expect(screen.getByRole('button', { name: /Remove from Favorites/i })).toBeInTheDocument();
  });

  it('calls onToggleFavorite when favorite button is clicked', () => {
    const handleToggleFavorite = vi.fn();
    render(<DetailPane item={mockSkillItem} onToggleFavorite={handleToggleFavorite} />);

    const favoriteButton = screen.getByRole('button', { name: /Add to Favorites/i });
    fireEvent.click(favoriteButton);

    expect(handleToggleFavorite).toHaveBeenCalledWith(mockSkillItem.id);
  });

  it('displays item metadata badges', () => {
    const { container } = render(<DetailPane item={mockSkillItem} />);
    const badges = container.querySelectorAll('.px-2.py-1');
    expect(badges).toHaveLength(2);
    expect(Array.from(badges).some(badge => badge.textContent?.toLowerCase().includes('skill'))).toBe(true);
    expect(Array.from(badges).some(badge => badge.textContent?.toLowerCase().includes('discovery'))).toBe(true);
  });

  it('renders code examples with syntax highlighting', () => {
    render(<DetailPane item={mockSkillItem} />);

    const examplesTab = screen.getByRole('tab', { name: /Examples/i });
    fireEvent.click(examplesTab);

    const codeBlock = screen.getByText(/\/discovery-domain-research/i);
    expect(codeBlock).toBeInTheDocument();
  });

  it('renders options table with parameter details', () => {
    render(<DetailPane item={mockSkillItem} />);

    const optionsTab = screen.getByRole('tab', { name: /Options/i });
    fireEvent.click(optionsTab);

    expect(screen.getByText(/--output/i)).toBeInTheDocument();
    expect(screen.getByText(/string/i)).toBeInTheDocument();
    expect(screen.getByText(/\.\/output/i)).toBeInTheDocument();
  });

  it('hides tabs with no content', () => {
    const minimalItem: ComponentDetail = {
      ...mockSkillItem,
      examples: undefined,
      options: undefined,
      workflow: undefined,
      traceability: undefined,
    };

    render(<DetailPane item={minimalItem} />);

    expect(screen.getByRole('tab', { name: /Purpose/i })).toBeInTheDocument();
    expect(screen.queryByRole('tab', { name: /Examples/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('tab', { name: /Options/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('tab', { name: /Workflow/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('tab', { name: /Traceability/i })).not.toBeInTheDocument();
  });

  it('respects visibleTabs prop', () => {
    render(
      <DetailPane
        item={mockSkillItem}
        visibleTabs={['purpose', 'examples']}
      />
    );

    expect(screen.getByRole('tab', { name: /Purpose/i })).toBeInTheDocument();
    expect(screen.getByRole('tab', { name: /Examples/i })).toBeInTheDocument();
    expect(screen.queryByRole('tab', { name: /Options/i })).not.toBeInTheDocument();
  });

  it('respects activeTab prop', () => {
    render(<DetailPane item={mockSkillItem} activeTab="examples" />);
    expect(screen.getByText(/Basic Usage/i)).toBeInTheDocument();
  });

  it('renders file path', () => {
    render(<DetailPane item={mockSkillItem} />);
    expect(screen.getByText(mockSkillItem.path)).toBeInTheDocument();
  });

  // Frontmatter display tests
  describe('frontmatter display', () => {
    it('renders frontmatter section for skill with frontmatter', () => {
      render(<DetailPane item={mockSkillItem} />);
      expect(screen.getByText('Frontmatter')).toBeInTheDocument();
    });

    it('displays skill frontmatter attributes', () => {
      render(<DetailPane item={mockSkillItem} />);
      expect(screen.getByText('sonnet')).toBeInTheDocument();
      expect(screen.getByText('fork')).toBeInTheDocument();
      expect(screen.getByText('Read')).toBeInTheDocument();
      expect(screen.getByText('Write')).toBeInTheDocument();
      expect(screen.getByText('Grep')).toBeInTheDocument();
    });

    it('displays command frontmatter attributes', () => {
      render(<DetailPane item={mockCommandItem} />);
      expect(screen.getByText('Frontmatter')).toBeInTheDocument();
      expect(screen.getByText('<SystemName> <InputPath>')).toBeInTheDocument();
      expect(screen.getByText('Discovery_JTBD')).toBeInTheDocument();
      expect(screen.getByText('discovery-domain-researcher')).toBeInTheDocument();
    });

    it('displays agent frontmatter attributes', () => {
      render(<DetailPane item={mockAgentItem} />);
      expect(screen.getByText('Frontmatter')).toBeInTheDocument();
      expect(screen.getByText('3')).toBeInTheDocument();
      expect(screen.getByText('blue')).toBeInTheDocument();
      expect(screen.getByText('Discovery_GeneratePersona')).toBeInTheDocument();
      expect(screen.getByText('discovery-multiagent')).toBeInTheDocument();
    });

    it('does not render frontmatter section when frontmatter is undefined', () => {
      const itemWithoutFrontmatter: ComponentDetail = {
        ...mockSkillItem,
        frontmatter: undefined,
      };
      render(<DetailPane item={itemWithoutFrontmatter} />);
      expect(screen.queryByText('Frontmatter')).not.toBeInTheDocument();
    });
  });

  // rawContent tests
  describe('rawContent rendering', () => {
    it('renders rawContent in Purpose tab when available', () => {
      render(<DetailPane item={mockSkillItem} />);
      // The rawContent contains "When to Use" which is not in purpose
      expect(screen.getByText(/When to Use/i)).toBeInTheDocument();
    });

    it('falls back to purpose when rawContent is undefined', () => {
      const itemWithoutRawContent: ComponentDetail = {
        ...mockSkillItem,
        rawContent: undefined,
      };
      render(<DetailPane item={itemWithoutRawContent} />);
      // Should still show purpose content
      expect(screen.getByText(/Extracts domain models/i)).toBeInTheDocument();
    });

    it('shows fallback message when neither rawContent nor purpose is available', () => {
      const minimalItem: ComponentDetail = {
        id: 'min-001',
        name: 'Minimal Item',
        type: 'skill',
        stage: 'discovery',
        path: '.claude/skills/minimal/SKILL.md',
        description: 'A minimal item',
        isFavorite: false,
      };
      render(<DetailPane item={minimalItem} />);
      expect(screen.getByText(/No content available/i)).toBeInTheDocument();
    });
  });
});
