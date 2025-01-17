import { render, screen } from '@testing-library/vue';
import { describe, it, expect, beforeEach, beforeAll, afterAll, afterEach, vi } from 'vitest';
import App from '../App.vue';
import { createMockServer, setupResizeObserverMock } from './test-utils';

// Setup MSW server
const server = createMockServer();

describe('App Component', () => {
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

  describe('Basic Rendering', () => {
    it('should render initial components', () => {
      expect(screen.getByText('Honkai Star Rail Banner Calculator')).toBeTruthy();
      expect(screen.getByLabelText('Banner Type')).toBeTruthy();
      expect(screen.getByLabelText('Current Pity')).toBeTruthy();
      expect(screen.getByLabelText('Planned Pulls')).toBeTruthy();
    });

    it('should not show plots and results initially', () => {
      expect(screen.queryByTestId('probability-results')).toBeFalsy();
      expect(screen.queryByTestId('probability-plots')).toBeFalsy();
    });

    it('should show all banner type options', () => {
      const bannerSelect = screen.getByLabelText('Banner Type') as HTMLSelectElement;
      expect(bannerSelect.options.length).toBe(3);
      expect(bannerSelect.options[0].value).toBe('standard');
      expect(bannerSelect.options[1].value).toBe('limited');
      expect(bannerSelect.options[2].value).toBe('light_cone');
    });
  });
});
