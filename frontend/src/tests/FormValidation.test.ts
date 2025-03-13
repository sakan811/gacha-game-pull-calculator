import { render, fireEvent, screen } from '@testing-library/vue';
import { describe, it, expect, beforeEach, beforeAll, afterAll, afterEach, vi } from 'vitest';
import { nextTick } from 'vue';
import App from '../App.vue';
import { createMockServer, setupResizeObserverMock } from './test-utils';

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
    const pityInput = screen.getByLabelText('Current Pity') as HTMLInputElement;
    const pullsInput = screen.getByLabelText('Planned Pulls') as HTMLInputElement;

    // Test invalid values
    await fireEvent.update(pityInput, '-1');
    // Wait for Vue reactivity
    await nextTick();
    expect(pityInput.value).toBe('0');

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
    const pityInput = screen.getByLabelText('Current Pity') as HTMLInputElement;
    const pullsInput = screen.getByLabelText('Planned Pulls') as HTMLInputElement;

    // Test values above maximum
    await fireEvent.update(pityInput, '100');
    await nextTick();
    expect(pityInput.value).toBe('89'); // Max pity is 89

    await fireEvent.update(pullsInput, '1000');
    await nextTick();
    expect(pullsInput.value).toBe('200'); // Max planned pulls is 200
  });
}); 