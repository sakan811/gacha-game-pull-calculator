import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import type { HttpHandler } from 'msw';
import type { MockInstance } from 'vitest';
import type { ResizeObserverEntry } from '@juggle/resize-observer';
import type { CalculateRequest } from '../types';

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
  total_5_star_probability: 0.1550,
  character_probability: 0.0775,
  light_cone_probability: 0.0775,
  rate_up_probability: 0.1000,
  standard_char_probability: 0.0775
};

// Create a default handler for all game types and banner types
const defaultHandlers = [
  'star_rail',
  'genshin',
  'zenless'
].flatMap(game => [
  'standard',
  'limited',
  'light_cone',
  'weapon',
  'w_engine',
  'bangboo'
].map(banner => 
  http.post(`/api/${game}/${banner}`, async ({ request }) => {
    const body = await request.json() as CalculateRequest;
    if (!body || typeof body.current_pity !== 'number' || typeof body.planned_pulls !== 'number') {
      return HttpResponse.error();
    }
    return HttpResponse.json(mockCalculationResponse);
  })
));

export function createMockServer(handlers: HttpHandler[] = []) {
  return setupServer(...defaultHandlers, ...handlers);
}

interface MockVitest {
  fn: (...args: any[]) => any;
  stubGlobal: (name: string, value: any) => void;
}

// Mock ResizeObserver for canvas tests
export function setupResizeObserverMock(vi: MockVitest) {
  const ResizeObserverMock = vi.fn(() => ({
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn(),
  }));

  vi.stubGlobal('ResizeObserver', ResizeObserverMock);

  return ResizeObserverMock;
}

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
  },
  // Zenless Zone Zero props
  zenlessStandard: {
    bannerType: 'standard' as const,
    gameType: 'zenless' as const,
    currentPity: 0,
    plannedPulls: 10,
    result: mockCalculationResponse
  },
  zenlessLimited: {
    bannerType: 'limited' as const,
    gameType: 'zenless' as const,
    currentPity: 0,
    plannedPulls: 10,
    result: mockCalculationResponse
  },
  zenlessWEngine: {
    bannerType: 'w_engine' as const,
    gameType: 'zenless' as const,
    currentPity: 0,
    plannedPulls: 10,
    result: mockCalculationResponse
  },
  zenlessBangboo: {
    bannerType: 'bangboo' as const,
    gameType: 'zenless' as const,
    currentPity: 0,
    plannedPulls: 10,
    result: mockCalculationResponse
  }
}; 