import { render, fireEvent, screen, waitFor } from '@testing-library/vue';
import { describe, it, expect, vi, beforeEach, beforeAll, afterAll, afterEach } from 'vitest';
import { http, HttpResponse } from 'msw';
import App from '../App.vue';
import { createMockServer, setupResizeObserverMock, mockCalculationResponse } from './test-utils';
import { CalculateRequest } from '../types';

const server = createMockServer([
  http.post('/api/zenless/standard', async ({ request }) => {
    const body = await request.json() as CalculateRequest;
    if (!body || typeof body.current_pity !== 'number' || typeof body.planned_pulls !== 'number') {
      return HttpResponse.error();
    }
    return HttpResponse.json(mockCalculationResponse);
  }),
  http.post('/api/zenless/limited', async ({ request }) => {
    const body = await request.json() as CalculateRequest;
    if (!body || typeof body.current_pity !== 'number' || typeof body.planned_pulls !== 'number') {
      return HttpResponse.error();
    }
    return HttpResponse.json(mockCalculationResponse);
  }),
  http.post('/api/zenless/w_engine', async ({ request }) => {
    const body = await request.json() as CalculateRequest;
    if (!body || typeof body.current_pity !== 'number' || typeof body.planned_pulls !== 'number') {
      return HttpResponse.error();
    }
    return HttpResponse.json(mockCalculationResponse);
  })
]);

describe('Zenless Zone Zero Banner Calculations', () => {
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());

  beforeEach(() => {
    setupResizeObserverMock(vi);
    render(App);
  });

  it('should calculate standard banner probabilities', async () => {
    await fireEvent.update(screen.getByLabelText('Game'), 'zenless');
    await fireEvent.update(screen.getByLabelText('Banner Type'), 'standard');
    await fireEvent.update(screen.getByLabelText('Current Pity'), '70');
    await fireEvent.update(screen.getByLabelText('Planned Pulls'), '10');
    
    await waitFor(() => {
      const results = screen.getByTestId('probability-results');
      expect(results.textContent).toContain('15.50%');
      expect(results.textContent).toContain('7.75%');
      expect(results.textContent).toContain('W-Engine');
      expect(results.textContent).toContain('7.75%');
      expect(screen.getByTestId('probability-plots')).toBeTruthy();
    });
  });

  it('should calculate limited banner probabilities', async () => {
    await fireEvent.update(screen.getByLabelText('Game'), 'zenless');
    await fireEvent.update(screen.getByLabelText('Banner Type'), 'limited');
    await fireEvent.update(screen.getByLabelText('Current Pity'), '70');
    await fireEvent.update(screen.getByLabelText('Planned Pulls'), '10');
    
    await waitFor(() => {
      const results = screen.getByTestId('probability-results');
      expect(results.textContent).toContain('15.50%');
      expect(results.textContent).toContain('10.00%');
      expect(screen.getByTestId('probability-plots')).toBeTruthy();
    });
  });

  it('should calculate W-Engine banner probabilities', async () => {
    await fireEvent.update(screen.getByLabelText('Game'), 'zenless');
    await fireEvent.update(screen.getByLabelText('Banner Type'), 'w_engine');
    await fireEvent.update(screen.getByLabelText('Current Pity'), '70');
    await fireEvent.update(screen.getByLabelText('Planned Pulls'), '10');
    
    await waitFor(() => {
      const results = screen.getByTestId('probability-results');
      expect(results.textContent).toContain('15.50%');
      expect(results.textContent).toContain('10.00%');
      expect(screen.getByTestId('probability-plots')).toBeTruthy();
    });
  });

  it('should switch banner types correctly when changing game to Zenless', async () => {
    await fireEvent.update(screen.getByLabelText('Game'), 'star_rail');
    await fireEvent.update(screen.getByLabelText('Banner Type'), 'light_cone');
    
    await fireEvent.update(screen.getByLabelText('Game'), 'zenless');
    
    const bannerTypeSelect = screen.getByLabelText('Banner Type') as HTMLSelectElement;
    expect(bannerTypeSelect.value).toBe('w_engine');
  });
}); 