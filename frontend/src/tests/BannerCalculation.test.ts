import { render, fireEvent, screen, waitFor } from '@testing-library/vue';
import { describe, it, expect, vi, beforeEach, beforeAll, afterAll, afterEach } from 'vitest';
import { http, HttpResponse } from 'msw';
import App from '../App.vue';
import { createMockServer, setupResizeObserverMock, mockCalculationResponse } from './test-utils';
import { CalculateRequest } from '../types';

const server = createMockServer([
  http.post('/api/star_rail/standard', async ({ request }) => {
    const body = await request.json() as CalculateRequest;
    if (!body || typeof body.current_pity !== 'number' || typeof body.planned_pulls !== 'number') {
      return HttpResponse.error();
    }
    return HttpResponse.json(mockCalculationResponse);
  })
]);

describe('Core Banner Calculation', () => {
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
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
      expect(screen.getByText('Successful Pull Distribution')).toBeTruthy();
      expect(screen.getByText('Cumulative Probability')).toBeTruthy();
    });
  });

  it('should show chart on first calculation with 0 pity', async () => {
    const pityInput = screen.getByLabelText('Current Pity') as HTMLInputElement;
    const pullsInput = screen.getByLabelText('Planned Pulls') as HTMLInputElement;
    const calculateButton = screen.getAllByRole('button', { name: /calculate/i })[0];

    await fireEvent.update(pityInput, '0');
    await fireEvent.update(pullsInput, '10');
    await fireEvent.click(calculateButton);

    await waitFor(() => {
      expect(screen.getByTestId('probability-plots')).toBeTruthy();
      expect(screen.getByText('Successful Pull Distribution')).toBeTruthy();
      expect(screen.getByText('Cumulative Probability')).toBeTruthy();
      expect(screen.getByTestId('probability-results')).toBeTruthy();
    });
  });

  it('should handle API errors gracefully', async () => {
    server.use(
      http.post('/api/star_rail/standard', () => {
        return HttpResponse.error();
      })
    );
    
    await fireEvent.click(screen.getByRole('button', { name: /calculate/i }));
    
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