import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import SettingsPage from './page';

describe('SettingsPage', () => {
  it('renders settings page', () => {
    render(<SettingsPage />);
    expect(screen.getByText(/Settings/i)).toBeInTheDocument();
  });

  it('displays theme toggle', () => {
    render(<SettingsPage />);
    expect(screen.getByText(/Theme/i)).toBeInTheDocument();
  });

  it('shows version information', () => {
    render(<SettingsPage />);
    expect(screen.getByText(/Version/i)).toBeInTheDocument();
  });
});
