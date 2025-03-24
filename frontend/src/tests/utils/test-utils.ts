import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import type { HttpHandler } from 'msw';
import type { CalculateRequest } from '../../types';
import { fireEvent, screen, waitFor } from '@testing-library/vue';
import { beforeAll, afterAll, afterEach, beforeEach, vi, expect } from 'vitest';

// Common mock data moved to separate file
import { mockVisualizationData, mockCalculationResponse } from './mock-data';
export { mockVisualizationData, mockCalculationResponse };

// Simplified handlers with common validation
const createApiHandler = (endpoint: string) => 
  http.post(endpoint, async ({ request }) => {
    const body = await request.json() as CalculateRequest;
    if (!isValidRequest(body)) {
      return HttpResponse.error();
    }
    return HttpResponse.json(mockCalculationResponse);
  });

const isValidRequest = (body: any): body is CalculateRequest => 
  body && typeof body.current_pity === 'number' && typeof body.planned_pulls === 'number';

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
].map(banner => createApiHandler(`/api/${game}/${banner}`)));

export function createMockServer(handlers: HttpHandler[] = []) {
  return setupServer(...defaultHandlers, ...handlers);
}

// Mock ResizeObserver for canvas tests
// Update the setupResizeObserverMock function to use proper typing
export function setupResizeObserverMock(vitest: typeof vi) {
  const ResizeObserverMock = vitest.fn(() => ({
    observe: vitest.fn(),
    unobserve: vitest.fn(),
    disconnect: vitest.fn(),
  }));

  vitest.stubGlobal('ResizeObserver', ResizeObserverMock);
  return ResizeObserverMock;
}

// Common test setup helper
export const setupBannerTest = () => {
  const server = createMockServer();
  
  beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
  afterEach(() => server.resetHandlers());
  afterAll(() => server.close());
  beforeEach(() => setupResizeObserverMock(vi));

  return server;
};

// Banner test helpers
export const updateBannerInputs = async (
  game: string, 
  bannerType: string, 
  pulls: string
) => {
  await fireEvent.update(screen.getByLabelText('Game'), game);
  await fireEvent.update(screen.getByLabelText('Banner Type'), bannerType);
  await fireEvent.update(screen.getByLabelText('Pulls'), pulls);
};

interface ProbabilityExpectations {
  total?: string;
  rateUp?: string;
  character?: string;
  equipment?: string;
}

export const assertProbabilityResults = async (expectations: ProbabilityExpectations) => {
  await waitFor(() => {
    const results = screen.getByTestId('probability-results');
    Object.entries(expectations).forEach(([, value]) => {
      if (value) {
        expect(results.textContent).includes(value);
      }
    });
    expect(screen.getByTestId('probability-plots')).toBeTruthy();
  }, { timeout: 3000 });
};

// Simplified test props creation
const createBannerProps = (bannerType: string, gameType: string) => ({
  bannerType,
  gameType,
  currentPity: 0,
  plannedPulls: 10,
  result: mockCalculationResponse
});

export const mockBannerProps = {
  standard: createBannerProps('standard', 'star_rail'),
  limited: createBannerProps('limited', 'star_rail'),
  lightCone: createBannerProps('light_cone', 'star_rail'),
  zenlessStandard: createBannerProps('standard', 'zenless'),
  zenlessLimited: createBannerProps('limited', 'zenless'),
  zenlessWEngine: createBannerProps('w_engine', 'zenless'),
  zenlessBangboo: createBannerProps('bangboo', 'zenless')
};