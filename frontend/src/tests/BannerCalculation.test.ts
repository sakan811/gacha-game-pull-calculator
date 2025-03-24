import { render, fireEvent, screen, waitFor } from '@testing-library/vue';
import { describe, it, expect, vi, beforeEach, beforeAll, afterAll, afterEach } from 'vitest';
import { http, HttpResponse } from 'msw';
import App from '../App.vue';
import { createMockServer, setupResizeObserverMock, mockCalculationResponse } from './utils/test-utils';
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
    await fireEvent.update(screen.getByLabelText('Pulls'), '10');
    
    await waitFor(() => {
      expect(screen.getByTestId('probability-results')).toBeTruthy();
      expect(screen.getByTestId('probability-plots')).toBeTruthy();
      expect(screen.getAllByText('Successful Pull Distribution')).toBeTruthy();
      expect(screen.getAllByText('Cumulative Probability')).toBeTruthy();
    });
  });

  it('should show chart on first calculation', async () => {
    await fireEvent.update(screen.getByLabelText('Pulls'), '10');

    await waitFor(() => {
      expect(screen.getByTestId('probability-plots')).toBeTruthy();
      expect(screen.getAllByText('Successful Pull Distribution')).toBeTruthy();
      expect(screen.getAllByText('Cumulative Probability')).toBeTruthy();
      expect(screen.getByTestId('probability-results')).toBeTruthy();
    });
  });

  it('should handle API errors gracefully', async () => {
    server.use(
      http.post('/api/star_rail/standard', () => {
        return HttpResponse.error();
      })
    );
    
    await fireEvent.update(screen.getByLabelText('Pulls'), '10');
    
    await waitFor(() => {
      const results = screen.getByTestId('probability-results');
      expect(results.textContent).toContain('0.00%');
      expect(results.textContent).toContain('0.00%');
      expect(results.textContent).toContain('0.00%');
      expect(screen.getByTestId('probability-plots')).toBeTruthy();
    });
  });

  it('should validate maximum pulls', async () => {
    await fireEvent.update(screen.getByLabelText('Pulls'), '300');

    await waitFor(() => {
      const pullsInput = screen.getByLabelText('Pulls') as HTMLInputElement;
      expect(pullsInput.value).toBe('90');
    });
  });

  it('should handle pity calculation correctly', async () => {
    server.use(
      http.post('/api/star_rail/standard', () => {
        return HttpResponse.json({
          ...mockCalculationResponse,
          total_5_star_probability: 1.0,
          character_probability: 0.5,
          light_cone_probability: 0.5
        });
      })
    );
    
    await fireEvent.update(screen.getByLabelText('Pulls'), '90');
    
    await waitFor(() => {
      const results = screen.getByTestId('probability-results');
      expect(results.textContent).toContain('100.00%');
    });
  });

  it('should handle successful API submission', async () => {
    let submittedData: CalculateRequest | null = null;
    
    server.use(
      http.post('/api/star_rail/standard', async ({ request }) => {
        submittedData = await request.json();
        return HttpResponse.json(mockCalculationResponse);
      })
    );

    await fireEvent.update(screen.getByLabelText('Pulls'), '10');
    
    await waitFor(() => {
      expect(submittedData).toEqual({
        current_pity: 0,
        planned_pulls: 10,
        guaranteed: false  // Account for guaranteed field
      });
    });
  });
});