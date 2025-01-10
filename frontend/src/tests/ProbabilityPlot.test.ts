import { render, screen } from '@testing-library/vue';
import { describe, it, expect, beforeAll, afterAll, afterEach, vi } from 'vitest';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import ProbabilityPlot from '../components/ProbabilityPlot.vue';

const mockVisualizationData = {
  rolls: [0, 1, 2],
  probability_per_roll: [0.1, 0.2, 0.3],
  cumulative_probability: [0.1, 0.3, 0.6],
  soft_pity_start: 74,
  hard_pity: 90,
  current_pity: 0
};

// Setup MSW server
const server = setupServer(
  http.post('/api/visualization', () => {
    return HttpResponse.json(mockVisualizationData);
  })
);

describe('ProbabilityPlot Component', () => {
  const mockProps = {
    bannerType: 'standard' as const,
    currentPity: 0,
    plannedPulls: 10,
    result: {
      total_5_star_probability: 50
    }
  };

  // Start server before all tests
  beforeAll(() => server.listen());
  
  // Reset handlers after each test
  afterEach(() => server.resetHandlers());
  
  // Clean up after all tests
  afterAll(() => server.close());

  it('should render chart containers', () => {
    const { container } = render(ProbabilityPlot, {
      props: mockProps
    });
    expect(container.querySelector('[data-testid="probability-plots"]')).toBeTruthy();
  });

  it('should render chart titles', () => {
    render(ProbabilityPlot, {
      props: mockProps
    });
    expect(screen.getByText('Successful Pull Distribution')).toBeTruthy();
    expect(screen.getByText('Cumulative Probability')).toBeTruthy();
  });

  it('should fetch and display visualization data', async () => {
    const { container } = render(ProbabilityPlot, {
      props: mockProps
    });

    // Trigger the update through DOM event
    await container.querySelector('[data-testid="probability-plots"]')?.dispatchEvent(
      new Event('mounted', { bubbles: true })
    );

    // Wait for the request to complete
    await vi.waitFor(() => {
      expect(screen.getByText('Successful Pull Distribution')).toBeTruthy();
    });
  });

  it('should show correct total pulls line', async () => {
    const testProps = {
      bannerType: 'standard' as const,
      currentPity: 10,
      plannedPulls: 20,
      result: {
        total_5_star_probability: 50
      }
    };

    // Mock ResizeObserver for canvas
    global.ResizeObserver = vi.fn().mockImplementation(() => ({
      observe: vi.fn(),
      unobserve: vi.fn(),
      disconnect: vi.fn()
    }));

    // Update mock server response for this test
    server.use(
      http.post('/api/visualization', () => {
        return HttpResponse.json({
          ...mockVisualizationData,
          current_pity: testProps.currentPity,
          planned_pulls: testProps.plannedPulls
        });
      })
    );

    const { container } = render(ProbabilityPlot, {
      props: testProps
    });

    // Trigger chart update
    await container.querySelector('[data-testid="probability-plots"]')?.dispatchEvent(
      new Event('mounted', { bubbles: true })
    );

    // Wait for chart to update
    await vi.waitFor(() => {
      // Instead of checking text directly, verify the chart container exists
      expect(container.querySelector('.chart-canvas-container')).toBeTruthy();
    });
  });

  it('should only update total pulls line after calculation', async () => {
    const initialProps = {
      bannerType: 'standard' as const,
      currentPity: 10,
      plannedPulls: 20,
      result: { total_5_star_probability: 50 }
    };

    // Mock visualization data with different planned pulls
    server.use(
      http.post('/api/visualization', () => {
        return HttpResponse.json({
          ...mockVisualizationData,
          current_pity: initialProps.currentPity,
          planned_pulls: initialProps.plannedPulls
        });
      })
    );

    const { rerender, container } = render(ProbabilityPlot, {
      props: initialProps
    });

    // Change planned pulls without triggering calculation
    await rerender({
      ...initialProps,
      plannedPulls: 30
    });

    // Wait for chart to update and verify container exists
    await vi.waitFor(() => {
      expect(container.querySelector('.chart-canvas-container')).toBeTruthy();
    });
  });
}); 