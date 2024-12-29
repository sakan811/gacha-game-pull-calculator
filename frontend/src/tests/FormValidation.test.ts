import { render, fireEvent, screen } from '@testing-library/svelte';
import { describe, it, expect, beforeEach } from 'vitest';
import App from '../App.svelte';

describe('Form Validation', () => {
  beforeEach(() => {
    render(App);
  });

  async function testPityRangeValidation() {
    const pityInput = screen.getByLabelText('Current Pity') as HTMLInputElement;
    
    // Test invalid values
    await fireEvent.change(pityInput, { target: { value: '-1' } });
    expect(pityInput.value).toBe('0');
    
    await fireEvent.change(pityInput, { target: { value: '90' } });
    expect(pityInput.value).toBe('89');
  }

  async function testPlannedPullsValidation() {
    const pullsInput = screen.getByLabelText('Planned Pulls') as HTMLInputElement;
    
    // Test invalid values
    await fireEvent.change(pullsInput, { target: { value: '0' } });
    expect(pullsInput.value).toBe('1');
    
    await fireEvent.change(pullsInput, { target: { value: '-5' } });
    expect(pullsInput.value).toBe('1');
  }

  it('should validate current pity range', testPityRangeValidation);
  it('should validate planned pulls minimum value', testPlannedPullsValidation);
}); 