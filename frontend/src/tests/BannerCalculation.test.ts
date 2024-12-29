import { render, fireEvent, screen, waitFor } from '@testing-library/svelte';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import type { Mock } from 'vitest';
import App from '../App.svelte';
import '@testing-library/jest-dom';

describe('Banner Calculation', () => {
  beforeEach(() => {
    global.fetch = vi.fn() as unknown as typeof fetch;
    render(App);
  });

  async function testStandardBannerCalculation() {
    // Mock successful API response
    (global.fetch as Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        total_5_star_probability: 15.5,
        character_probability: 7.75,
        light_cone_probability: 7.75
      })
    });

    // Fill form
    await fireEvent.change(screen.getByLabelText('Current Pity'), { 
      target: { value: '70' } 
    });
    await fireEvent.change(screen.getByLabelText('Planned Pulls'), { 
      target: { value: '10' } 
    });
    
    // Submit form
    const calculateButton = screen.getByRole('button', { name: /calculate/i });
    await fireEvent.click(calculateButton);

    // Wait for and verify results using data-testid attributes
    await waitFor(() => {
      expect(screen.getByTestId('total-probability'))
        .toHaveTextContent('15.50%');
      expect(screen.getByTestId('character-probability'))
        .toHaveTextContent('7.75%');
      expect(screen.getByTestId('light-cone-probability'))
        .toHaveTextContent('7.75%');
    });
  }

  async function testLimitedBannerCalculation() {
    // Switch to limited banner
    await fireEvent.change(screen.getByLabelText('Banner Type'), {
      target: { value: 'limited' }
    });

    // Mock successful API response
    (global.fetch as Mock).mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({
        total_5_star_probability: 20.0,
        rate_up_probability: 10.0,
        standard_char_probability: 10.0
      })
    });

    // Fill form
    await fireEvent.change(screen.getByLabelText('Current Pity'), {
      target: { value: '80' }
    });
    await fireEvent.change(screen.getByLabelText('Planned Pulls'), {
      target: { value: '5' }
    });
    await fireEvent.click(screen.getByLabelText('Guaranteed Rate-Up (Lost previous 50/50)'));
    
    // Submit form
    const calculateButton = screen.getByRole('button', { name: /calculate/i });
    await fireEvent.click(calculateButton);

    // Wait for and verify results using data-testid attributes
    await waitFor(() => {
      expect(screen.getByTestId('total-probability'))
        .toHaveTextContent('20.00%');
      expect(screen.getByTestId('rate-up-probability'))
        .toHaveTextContent('10.00%');
      expect(screen.getByTestId('standard-probability'))
        .toHaveTextContent('10.00%');
    });
  }

  it('should calculate standard banner probabilities correctly', testStandardBannerCalculation);
  it('should calculate limited banner probabilities correctly', testLimitedBannerCalculation);
}); 