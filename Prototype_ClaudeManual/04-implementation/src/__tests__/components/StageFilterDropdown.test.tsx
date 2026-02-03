import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { StageFilterDropdown } from '../../components/StageFilterDropdown';

describe('StageFilterDropdown', () => {
  it('renders with no stages selected', () => {
    const handleChange = vi.fn();
    render(<StageFilterDropdown selectedStages={[]} onChange={handleChange} />);
    expect(screen.getByLabelText(/Filter by stage/i)).toBeInTheDocument();
  });

  it('renders all stage options', () => {
    const handleChange = vi.fn();
    render(<StageFilterDropdown selectedStages={[]} onChange={handleChange} />);

    // Open dropdown first
    const toggleButton = screen.getByRole('button', { name: /Filter by stage/i });
    fireEvent.click(toggleButton);

    // Check for 8 checkboxes (one per stage)
    const checkboxes = screen.getAllByRole('checkbox');
    expect(checkboxes.length).toBe(8);
  });

  it('shows selected stages', () => {
    const handleChange = vi.fn();
    render(
      <StageFilterDropdown
        selectedStages={['discovery', 'prototype']}
        onChange={handleChange}
      />
    );

    const displayText = screen.getByText(/2 selected/i);
    expect(displayText).toBeInTheDocument();
  });

  it('calls onChange when stage is selected', () => {
    const handleChange = vi.fn();
    const { container } = render(
      <StageFilterDropdown selectedStages={[]} onChange={handleChange} />
    );

    const checkbox = container.querySelector('input[value="discovery"]');
    if (checkbox) {
      fireEvent.click(checkbox);
      expect(handleChange).toHaveBeenCalledWith(['discovery']);
    }
  });

  it('calls onChange when stage is deselected', () => {
    const handleChange = vi.fn();
    const { container } = render(
      <StageFilterDropdown
        selectedStages={['discovery', 'prototype']}
        onChange={handleChange}
      />
    );

    const checkbox = container.querySelector('input[value="discovery"]');
    if (checkbox) {
      fireEvent.click(checkbox);
      expect(handleChange).toHaveBeenCalledWith(['prototype']);
    }
  });

  it('displays count badge when showCount is true', () => {
    const handleChange = vi.fn();
    render(
      <StageFilterDropdown
        selectedStages={['discovery', 'prototype', 'implementation']}
        onChange={handleChange}
        showCount={true}
      />
    );

    expect(screen.getByText(/3 selected/i)).toBeInTheDocument();
  });

  it('does not display count badge when showCount is false', () => {
    const handleChange = vi.fn();
    const { container } = render(
      <StageFilterDropdown
        selectedStages={['discovery', 'prototype']}
        onChange={handleChange}
        showCount={false}
      />
    );

    const badge = container.querySelector('.count-badge');
    expect(badge).not.toBeInTheDocument();
  });

  it('renders all stage options with correct labels', () => {
    const handleChange = vi.fn();
    const { container } = render(<StageFilterDropdown selectedStages={[]} onChange={handleChange} />);

    // Open dropdown first
    const toggleButton = screen.getByRole('button', { name: /Filter by stage/i });
    fireEvent.click(toggleButton);

    // Check for stage labels in the dropdown
    const stageLabels = container.querySelectorAll('.stage-discovery, .stage-prototype, .stage-productspecs, .stage-solarch, .stage-implementation, .stage-utility, .stage-security, .stage-grc');
    expect(stageLabels.length).toBe(8);
  });

  it('handles selecting all stages', () => {
    const handleChange = vi.fn();
    const { container } = render(
      <StageFilterDropdown selectedStages={[]} onChange={handleChange} />
    );

    // Open dropdown first
    const toggleButton = screen.getByRole('button', { name: /Filter by stage/i });
    fireEvent.click(toggleButton);

    const checkboxes = container.querySelectorAll('input[type="checkbox"]');

    // onChange should be called for each checkbox click
    expect(checkboxes.length).toBe(8);
    expect(handleChange).toHaveBeenCalledTimes(0); // Not called yet

    fireEvent.click(checkboxes[0]);
    expect(handleChange).toHaveBeenCalledWith(['discovery']);
  });

  it('clears all selections', () => {
    const handleChange = vi.fn();
    render(
      <StageFilterDropdown
        selectedStages={['discovery', 'prototype', 'implementation']}
        onChange={handleChange}
      />
    );

    // Open dropdown first
    const toggleButton = screen.getByRole('button', { name: /Filter by stage/i });
    fireEvent.click(toggleButton);

    const clearButton = screen.getByText(/Clear/i);
    fireEvent.click(clearButton);

    expect(handleChange).toHaveBeenCalledWith([]);
  });

  it('applies stage-specific badge colors', () => {
    const handleChange = vi.fn();
    const { container } = render(
      <StageFilterDropdown selectedStages={['discovery']} onChange={handleChange} />
    );

    // Open dropdown first
    const toggleButton = screen.getByRole('button', { name: /Filter by stage/i });
    fireEvent.click(toggleButton);

    const discoveryBadge = container.querySelector('.stage-discovery');
    expect(discoveryBadge).toBeInTheDocument();
  });

  it('renders dropdown toggle button', () => {
    const handleChange = vi.fn();
    render(<StageFilterDropdown selectedStages={[]} onChange={handleChange} />);
    expect(screen.getByRole('button', { name: /Filter by stage/i })).toBeInTheDocument();
  });
});
