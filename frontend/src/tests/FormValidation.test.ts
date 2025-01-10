import { render, fireEvent, screen } from '@testing-library/vue';
import { describe, it, expect, beforeEach } from 'vitest';
import { nextTick } from 'vue';
import App from '../App.vue';

describe('Form Validation', () => {
  beforeEach(() => {
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
    expect(screen.queryByTestId('probability-results')).toBeFalsy();
  });
}); 