import { render } from '@testing-library/vue';
import { describe, it } from 'vitest';
import App from '../../App.vue';
import { setupBannerTest, updateBannerInputs, assertProbabilityResults } from '../utils/test-utils';

describe('Star Rail Banner Calculations', () => {
  setupBannerTest();

  beforeEach(() => {
    render(App);
  });

  it('should calculate standard banner probabilities', async () => {
    await updateBannerInputs('star_rail', 'standard', '10');
    await assertProbabilityResults({
      total: '15.50%',
      character: '7.75%',
      equipment: '7.75%'
    });
  });

  it('should calculate limited banner probabilities', async () => {
    await updateBannerInputs('star_rail', 'limited', '10');
    await assertProbabilityResults({
      total: '15.50%',
      character: '10.00%'
    });
  });

  it('should calculate light cone banner probabilities', async () => {
    await updateBannerInputs('star_rail', 'light_cone', '10');
    await assertProbabilityResults({
      total: '15.50%',
      character: '10.00%'
    });
  });

  it('should handle invalid banner type gracefully', async () => {
    await updateBannerInputs('star_rail', 'invalid_banner', '10');
    await assertProbabilityResults({
      total: '0.00%',
      character: '0.00%',
      equipment: '0.00%'
    });
  });
});