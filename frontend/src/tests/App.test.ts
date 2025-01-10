import { render, fireEvent, screen } from '@testing-library/svelte';
import { describe, it, expect, beforeEach } from 'vitest';
import App from '../App.svelte';

describe('App Component', () => {
  beforeEach(() => {
    render(App);
  });

  describe('Basic Rendering', () => {
    it('should render initial components', () => {
      expect(screen.getByText('Honkai Star Rail Banner Calculator')).toBeTruthy();
      expect(screen.getByLabelText('Banner Type')).toBeTruthy();
      expect(screen.getByLabelText('Current Pity')).toBeTruthy();
      expect(screen.getByLabelText('Planned Pulls')).toBeTruthy();
    });

    it('should not show plots initially', () => {
      const plotsWrapper = document.querySelector('.plots-wrapper-hidden');
      expect(plotsWrapper).toBeTruthy();
    });
  });

  describe('Banner Type Interactions', () => {
    it('should show/hide guaranteed checkbox based on banner type', async () => {
      const select = screen.getByLabelText('Banner Type');
      
      await fireEvent.change(select, { target: { value: 'limited' } });
      expect(screen.getByText('Guaranteed Rate-Up (Lost previous 50/50)')).toBeTruthy();
      
      await fireEvent.change(select, { target: { value: 'standard' } });
      expect(screen.queryByText('Guaranteed Rate-Up (Lost previous 50/50)')).toBeFalsy();
    });

    it('should adjust max pity based on banner type', async () => {
      const select = screen.getByLabelText('Banner Type') as HTMLSelectElement;
      const pityInput = screen.getByLabelText('Current Pity') as HTMLInputElement;
      
      await fireEvent.change(select, { target: { value: 'light_cone' } });
      await fireEvent.change(pityInput, { target: { value: '85' } });
      expect(pityInput.value).toBe('79'); // Should be capped at 79 for light cone

      await fireEvent.change(select, { target: { value: 'standard' } });
      await fireEvent.change(pityInput, { target: { value: '95' } });
      expect(pityInput.value).toBe('89'); // Should be capped at 89 for character banners
    });
  });
});
