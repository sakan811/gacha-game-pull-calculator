import { render, fireEvent, screen, waitFor } from '@testing-library/vue';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import App from '../App.vue';

describe('Banner Calculation', () => {
  beforeEach(() => {
    // Mock fetch for both calculation and visualization
    global.fetch = vi.fn(((url: string) => {
      if (url.includes('/visualization')) {
        return Promise.resolve({
          ok: true,
          status: 200,
          json: () => Promise.resolve({
            rolls: [],
            probability_per_roll: [],
            cumulative_probability: [],
            soft_pity_start: 74,
            hard_pity: 90,
            current_pity: 0,
            planned_pulls: 0
          })
        });
      }
      return Promise.resolve({
        ok: true,
        status: 200,
        json: () => Promise.resolve({
          total_5_star_probability: 15.5,
          character_probability: 7.75,
          light_cone_probability: 7.75,
          rate_up_probability: 10.0,
          standard_char_probability: 10.0
        })
      });
    })) as unknown as typeof fetch;

    render(App);
  });

  it('should show results and plots after calculation', async () => {
    await fireEvent.click(screen.getByRole('button', { name: /calculate/i }));
    
    await waitFor(() => {
      expect(screen.getByTestId('probability-results')).toBeTruthy();
      expect(screen.getByTestId('probability-plots')).toBeTruthy();
    });
  });

  it('should show chart on first calculation with 0 pity', async () => {
    // Set inputs
    const pityInput = screen.getByLabelText('Current Pity') as HTMLInputElement;
    const pullsInput = screen.getByLabelText('Planned Pulls') as HTMLInputElement;
    const calculateButton = screen.getAllByRole('button', { name: /calculate/i })[0];

    await fireEvent.update(pityInput, '0');
    await fireEvent.update(pullsInput, '10');
    await fireEvent.click(calculateButton);

    // Wait for next tick and verify chart appears
    await vi.waitFor(() => {
      expect(screen.getByTestId('probability-plots')).toBeTruthy();
      expect(screen.getByText('Successful Pull Distribution')).toBeTruthy();
      expect(screen.getByText('Cumulative Probability')).toBeTruthy();
    });
  });

  it('should calculate standard banner probabilities', async () => {
    // Set banner type to standard
    await fireEvent.update(screen.getByLabelText('Banner Type'), 'standard');
    await fireEvent.update(screen.getByLabelText('Current Pity'), '70');
    await fireEvent.update(screen.getByLabelText('Planned Pulls'), '10');
    
    await fireEvent.click(screen.getByRole('button', { name: /calculate/i }));

    await waitFor(() => {
      const results = screen.getByTestId('probability-results');
      expect(results.textContent).toContain('15.50%'); // Total probability
      expect(results.textContent).toContain('7.75%'); // Character probability
      expect(results.textContent).toContain('7.75%'); // Light cone probability
    });
  });

  it('should calculate limited banner probabilities', async () => {
    // Set banner type to limited
    await fireEvent.update(screen.getByLabelText('Banner Type'), 'limited');
    await fireEvent.update(screen.getByLabelText('Current Pity'), '80');
    await fireEvent.update(screen.getByLabelText('Planned Pulls'), '10');
    
    await fireEvent.click(screen.getByRole('button', { name: /calculate/i }));

    await waitFor(() => {
      const results = screen.getByTestId('probability-results');
      expect(results.textContent).toContain('15.50%'); // Total probability
      expect(results.textContent).toContain('10.00%'); // Rate-up probability
    });
  });

  it('should calculate light cone banner probabilities', async () => {
    // Set banner type to light cone
    await fireEvent.update(screen.getByLabelText('Banner Type'), 'light_cone');
    await fireEvent.update(screen.getByLabelText('Current Pity'), '65');
    await fireEvent.update(screen.getByLabelText('Planned Pulls'), '10');
    
    await fireEvent.click(screen.getByRole('button', { name: /calculate/i }));

    await waitFor(() => {
      const results = screen.getByTestId('probability-results');
      expect(results.textContent).toContain('15.50%'); // Total probability
      expect(results.textContent).toContain('10.00%'); // Rate-up probability
    });
  });

  it('should handle API errors gracefully', async () => {
    // Mock API error
    global.fetch = vi.fn().mockRejectedValueOnce(new Error('API Error'));
    
    await fireEvent.click(screen.getByRole('button', { name: /calculate/i }));
    
    // Should not show results on error
    expect(screen.queryByTestId('probability-results')).toBeFalsy();
    expect(screen.queryByTestId('probability-plots')).toBeFalsy();
  });
}); 