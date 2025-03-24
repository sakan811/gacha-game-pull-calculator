import { render, fireEvent, screen } from '@testing-library/vue';
import { describe, it, expect, beforeEach, beforeAll, afterAll, afterEach, vi } from 'vitest';
import { nextTick } from 'vue';
import App from '../../App.vue';
import { createMockServer, setupResizeObserverMock } from '../utils/test-utils';

// Setup MSW server
const server = createMockServer();

describe('Form Validation', () => {
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

  it('should validate form inputs', async () => {
    const pullsInput = screen.getByLabelText('Pulls') as HTMLInputElement;

    // Test invalid values
    await fireEvent.update(pullsInput, '0');
    // Wait for Vue reactivity
    await nextTick();
    expect(pullsInput.value).toBe('1');

    // Verify no results shown
    const results = screen.getByTestId('probability-results');
    expect(results.textContent).toContain('0.00%');
    expect(results.textContent).toContain('0.00%');
    expect(results.textContent).toContain('0.00%');
  });

  it('should validate maximum values', async () => {
    const pullsInput = screen.getByLabelText('Pulls') as HTMLInputElement;

    // Test values above maximum
    await fireEvent.update(pullsInput, '1000');
    await nextTick();
    expect(pullsInput.value).toBe('90'); // Match actual max pulls value
  });
});