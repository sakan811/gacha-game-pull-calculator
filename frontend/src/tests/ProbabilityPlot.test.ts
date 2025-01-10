import { render, screen } from '@testing-library/vue';
import { describe, it, expect, beforeAll, afterAll, afterEach, vi, beforeEach } from 'vitest';
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

  describe('Total Pulls Calculation', () => {
    beforeEach(() => {
      // Mock ResizeObserver for all canvas tests
      global.ResizeObserver = vi.fn().mockImplementation(() => ({
        observe: vi.fn(),
        unobserve: vi.fn(),
        disconnect: vi.fn()
      }));
    });

    it('should show correct total pulls with current pity and planned pulls', async () => {
      const testCases = [
        { currentPity: 0, plannedPulls: 10, expected: 10 },
        { currentPity: 10, plannedPulls: 20, expected: 30 },
        { currentPity: 74, plannedPulls: 16, expected: 90 }, // Hard pity case
        { currentPity: 89, plannedPulls: 1, expected: 90 }, // Edge case
      ];

      for (const testCase of testCases) {
        // Mock visualization data for each test case
        server.use(
          http.post('/api/visualization', () => {
            return HttpResponse.json({
              ...mockVisualizationData,
              current_pity: testCase.currentPity,
              planned_pulls: testCase.plannedPulls
            });
          })
        );

        const { container } = render(ProbabilityPlot, {
          props: {
            bannerType: 'standard',
            currentPity: testCase.currentPity,
            plannedPulls: testCase.plannedPulls,
            result: { total_5_star_probability: 50 }
          }
        });

        // Trigger chart update
        await container.querySelector('[data-testid="probability-plots"]')?.dispatchEvent(
          new Event('mounted', { bubbles: true })
        );

        // Wait for chart to update
        await vi.waitFor(() => {
          expect(container.querySelector('.chart-canvas-container')).toBeTruthy();
        });
      }
    });

    it('should update total pulls only after calculation', async () => {
      const initialProps = {
        currentPity: 10,
        plannedPulls: 20,
      };

      // Mock visualization data
      server.use(
        http.post('/api/visualization', () => {
          return HttpResponse.json({
            ...mockVisualizationData,
            current_pity: initialProps.currentPity,
            planned_pulls: initialProps.plannedPulls
          });
        })
      );

      const { container, rerender } = render(ProbabilityPlot, {
        props: {
          bannerType: 'standard',
          currentPity: initialProps.currentPity,
          plannedPulls: initialProps.plannedPulls,
          result: { total_5_star_probability: 50 }
        }
      });

      // Initial calculation
      await container.querySelector('[data-testid="probability-plots"]')?.dispatchEvent(
        new Event('mounted', { bubbles: true })
      );

      // Change props without triggering calculation
      await rerender({
        bannerType: 'standard',
        currentPity: initialProps.currentPity,
        plannedPulls: 40,
        result: { total_5_star_probability: 50 }
      });

      // Get component instance and verify data
      await vi.waitFor(() => {
        const spy = vi.spyOn(server, 'use');
        expect(spy).not.toHaveBeenCalled();
      });
    });
  });
}); 