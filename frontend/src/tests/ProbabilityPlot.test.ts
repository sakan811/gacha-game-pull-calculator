import { render } from '@testing-library/svelte';
import { describe, it, expect, beforeEach } from 'vitest';
import ProbabilityPlot from '../components/ProbabilityPlot.svelte';

describe('ProbabilityPlot Component', () => {
  const mockProps = {
    bannerType: 'standard',
    currentPity: 0,
    plannedPulls: 10,
    result: {
      total_5_star_probability: 50,
      character_probability: 25,
      light_cone_probability: 25
    }
  };

  beforeEach(() => {
    render(ProbabilityPlot, { props: mockProps });
  });

  it('should render chart containers', () => {
    expect(document.querySelector('.chart-container')).toBeTruthy();
    expect(document.querySelector('.chart-wrapper')).toBeTruthy();
    expect(document.querySelectorAll('canvas')).toHaveLength(2);
  });

  it('should render chart titles', () => {
    expect(document.querySelector('.chart-title')).toBeTruthy();
    expect(document.querySelector('h3')).toBeTruthy();
  });
}); 