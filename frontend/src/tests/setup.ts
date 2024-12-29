import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';

// Mock fetch globally
global.fetch = vi.fn();

// Reset all mocks before each test
beforeEach(() => {
  vi.resetAllMocks();
});

// Clean up after each test
afterEach(() => {
  vi.clearAllMocks();
}); 