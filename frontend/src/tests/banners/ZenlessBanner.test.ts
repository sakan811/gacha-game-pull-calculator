import { render } from '@testing-library/vue';
import { describe, it } from 'vitest';
import App from '../../App.vue';
import { setupBannerTest, updateBannerInputs, assertProbabilityResults } from '../utils/test-utils';

describe('Zenless Zone Zero Banner Calculations', () => {
  setupBannerTest();

  beforeEach(() => {
    render(App);
  });

  it('should calculate standard banner probabilities', async () => {
    await updateBannerInputs('zenless', 'standard', '10');
    await assertProbabilityResults({
      total: '15.50%',
      character: '7.75%',
      equipment: '7.75%'
    });
  });

  // ...remaining test cases using helpers...
});