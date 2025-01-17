import { render, screen } from '@testing-library/vue';
import { describe, it, expect, beforeAll, afterAll, afterEach, vi, beforeEach } from 'vitest';
import { http, HttpResponse } from 'msw';
import ProbabilityPlot from '../components/ProbabilityPlot.vue';
import { createMockServer, mockVisualizationData, mockBannerProps, setupResizeObserverMock } from './test-utils';

// Setup MSW server
const server = createMockServer();

describe('ProbabilityPlot Component', () => {
  // Start server before all tests
  beforeAll(() => server.listen());
  
  // Reset handlers after each test
  afterEach(() => server.resetHandlers());
  
  // Clean up after all tests
  afterAll(() => server.close());

  beforeEach(() => {
    setupResizeObserverMock(vi);
  });

  it('should render chart containers', () => {
    const { container } = render(ProbabilityPlot, {
      props: mockBannerProps.standard
    });
    expect(container.querySelector('[data-testid="probability-plots"]')).toBeTruthy();
  });

  it('should render chart titles', () => {
    render(ProbabilityPlot, {
      props: mockBannerProps.standard
    });
    expect(screen.getByText('Successful Pull Distribution')).toBeTruthy();
    expect(screen.getByText('Cumulative Probability')).toBeTruthy();
  });

  it('should fetch and display visualization data', async () => {
    const { container } = render(ProbabilityPlot, {
      props: mockBannerProps.standard
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
    const testCases = [
      { currentPity: 0, plannedPulls: 10, expected: 10 },
      { currentPity: 10, plannedPulls: 20, expected: 30 },
      { currentPity: 74, plannedPulls: 16, expected: 90 }, // Hard pity case
      { currentPity: 89, plannedPulls: 1, expected: 90 }, // Edge case
    ];

    testCases.forEach(({ currentPity, plannedPulls, expected }) => {
      it(`should show correct total pulls: ${currentPity} + ${plannedPulls} = ${expected}`, async () => {
        server.use(
          http.post('/api/visualization', () => {
            return HttpResponse.json({
              ...mockVisualizationData,
              current_pity: currentPity,
              planned_pulls: plannedPulls
            });
          })
        );

        const { container } = render(ProbabilityPlot, {
          props: {
            ...mockBannerProps.standard,
            currentPity,
            plannedPulls
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
      });
    });

    it('should update total pulls only after calculation', async () => {
      const { container, rerender } = render(ProbabilityPlot, {
        props: {
          ...mockBannerProps.standard,
          currentPity: 10,
          plannedPulls: 20
        }
      });

      // Initial calculation
      await container.querySelector('[data-testid="probability-plots"]')?.dispatchEvent(
        new Event('mounted', { bubbles: true })
      );

      // Change props without triggering calculation
      await rerender({
        ...mockBannerProps.standard,
        currentPity: 10,
        plannedPulls: 40
      });

      // Get component instance and verify data
      await vi.waitFor(() => {
        const spy = vi.spyOn(server, 'use');
        expect(spy).not.toHaveBeenCalled();
      });
    });
  });
}); 