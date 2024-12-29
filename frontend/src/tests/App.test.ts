import { render, fireEvent, screen } from '@testing-library/svelte';
import { describe, it, expect, beforeEach } from 'vitest';
import App from '../App.svelte';

describe('App Component Basic Rendering', () => {
  beforeEach(() => {
    render(App);
  });

  async function testInitialRendering() {
    expect(screen.getByText('HSR Banner Calculator')).toBeTruthy();
    expect(screen.getByLabelText('Banner Type')).toBeTruthy();
    expect(screen.getByLabelText('Current Pity')).toBeTruthy();
    expect(screen.getByLabelText('Planned Pulls')).toBeTruthy();
  }

  async function testBannerTypeSwitch() {
    const select = screen.getByLabelText('Banner Type');
    await fireEvent.change(select, { target: { value: 'limited' } });
    expect(screen.getByText('Guaranteed Rate-Up (Lost previous 50/50)')).toBeTruthy();
    
    await fireEvent.change(select, { target: { value: 'standard' } });
    expect(screen.queryByText('Guaranteed Rate-Up (Lost previous 50/50)')).toBeFalsy();
  }

  it('should render initial components', testInitialRendering);
  it('should show/hide guaranteed checkbox based on banner type', testBannerTypeSwitch);
});
