import { render, fireEvent, screen, waitFor } from '@testing-library/vue';
import { describe, it, expect, vi, beforeEach, beforeAll, afterAll, afterEach } from 'vitest';
import { http, HttpResponse } from 'msw';
import App from '../App.vue';
import { createMockServer, setupResizeObserverMock, mockCalculationResponse } from './test-utils';

interface CalculateRequest {
  banner_type: 'standard' | 'limited' | 'light_cone';
  current_pity: number;
  planned_pulls: number;
}

// Setup MSW server with both endpoints
const server = createMockServer([
  http.post('/api/standard', async ({ request }) => {
    const body = await request.json() as CalculateRequest;
    // Validate request body
    if (!body || typeof body.current_pity !== 'number' || typeof body.planned_pulls !== 'number') {
      return HttpResponse.error();
    }
    return HttpResponse.json(mockCalculationResponse);
  })
]);

describe('Banner Calculation', () => {
  // Start server before all tests
  beforeAll(() => server.listen());
  
  // Reset handlers after each test
  afterEach(() => server.resetHandlers());
  
  // Clean up after all tests
  afterAll(() => server.close());

  beforeEach(() => {
    setupResizeObserverMock(vi);
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
    server.use(
      http.post('/api/standard', () => {
        return HttpResponse.error();
      })
    );
    
    await fireEvent.click(screen.getByRole('button', { name: /calculate/i }));
    
    // Should not show results on error
    expect(screen.queryByTestId('probability-results')).toBeFalsy();
    expect(screen.queryByTestId('probability-plots')).toBeFalsy();
  });

  it('should validate maximum planned pulls', async () => {
    const pullsInput = screen.getByLabelText('Planned Pulls') as HTMLInputElement;
    await fireEvent.update(pullsInput, '300');
    await fireEvent.click(screen.getByRole('button', { name: /calculate/i }));

    await waitFor(() => {
      expect(pullsInput.value).toBe('200');
    });
  });
}); 