import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import type { HttpHandler } from 'msw';
import type { MockInstance } from 'vitest';

// Common mock data
export const mockVisualizationData = {
  rolls: [0, 1, 2],
  probability_per_roll: [0.1, 0.2, 0.3],
  cumulative_probability: [0.1, 0.3, 0.6],
  soft_pity_start: 74,
  hard_pity: 90,
  current_pity: 0,
  total_pulls: 90
};

export const mockCalculationResponse = {
  total_5_star_probability: 15.5,
  character_probability: 7.75,
  light_cone_probability: 7.75,
  rate_up_probability: 10.0,
  standard_char_probability: 10.0
};

// Mock server setup helper
export const createMockServer = (customHandlers: HttpHandler[] = []) => {
  const defaultHandlers = [
    http.post('/api/visualization', () => {
      return HttpResponse.json(mockVisualizationData);
    }),
    http.post('/api/standard', () => {
      return HttpResponse.json(mockCalculationResponse);
    }),
    http.post('/api/limited', () => {
      return HttpResponse.json(mockCalculationResponse);
    }),
    http.post('/api/light_cone', () => {
      return HttpResponse.json(mockCalculationResponse);
    })
  ];

  return setupServer(...defaultHandlers, ...customHandlers);
};

interface MockVitest {
  fn: () => MockInstance;
}

// Mock ResizeObserver for canvas tests
export const setupResizeObserverMock = (vi: MockVitest) => {
  const mockResizeObserver = vi.fn().mockImplementation(() => ({
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn()
  }));

  // @ts-ignore - ResizeObserver is available in jsdom environment
  window.ResizeObserver = mockResizeObserver;
  return mockResizeObserver;
};

// Common test props
export const mockBannerProps = {
  standard: {
    bannerType: 'standard' as const,
    gameType: 'star_rail' as const,
    currentPity: 0,
    plannedPulls: 10,
    result: mockCalculationResponse
  },
  limited: {
    bannerType: 'limited' as const,
    gameType: 'star_rail' as const,
    currentPity: 0,
    plannedPulls: 10,
    result: mockCalculationResponse
  },
  lightCone: {
    bannerType: 'light_cone' as const,
    gameType: 'star_rail' as const,
    currentPity: 0,
    plannedPulls: 10,
    result: mockCalculationResponse
  }
}; 