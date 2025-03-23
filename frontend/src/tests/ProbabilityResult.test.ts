import { render, screen } from '@testing-library/vue';
import { describe, it, expect } from 'vitest';
import ProbabilityResult from '../components/ProbabilityResult.vue';
import { mockBannerProps } from './test-utils';

describe('ProbabilityResult.vue', () => {
  it('should display correct labels for Star Rail standard banner', () => {
    render(ProbabilityResult, {
      props: mockBannerProps.standard
    });

    expect(screen.getByText('Total 5★ Probability')).toBeTruthy();
    expect(screen.getByText('Character Probability')).toBeTruthy();
    expect(screen.getByText('Light Cone Probability')).toBeTruthy();
  });

  it('should display correct labels for Genshin standard banner', () => {
    render(ProbabilityResult, {
      props: {
        ...mockBannerProps.standard,
        gameType: 'genshin'
      }
    });

    expect(screen.getByText('Total 5★ Probability')).toBeTruthy();
    expect(screen.getByText('Character Probability')).toBeTruthy();
    expect(screen.getByText('Weapon Probability')).toBeTruthy();
  });

  it('should display correct labels for Zenless standard banner', () => {
    render(ProbabilityResult, {
      props: mockBannerProps.zenlessStandard
    });

    expect(screen.getByText('Total 5★ Probability')).toBeTruthy();
    expect(screen.getByText('Character Probability')).toBeTruthy();
    expect(screen.getByText('W-Engine Probability')).toBeTruthy();
  });

  it('should display correct labels for Zenless limited banner', () => {
    render(ProbabilityResult, {
      props: mockBannerProps.zenlessLimited
    });

    expect(screen.getByText('Total 5★ Probability')).toBeTruthy();
    expect(screen.getByText('Rate-Up Probability')).toBeTruthy();
  });

  it('should display correct labels for Zenless W-Engine banner', () => {
    render(ProbabilityResult, {
      props: mockBannerProps.zenlessWEngine
    });

    expect(screen.getByText('Total 5★ Probability')).toBeTruthy();
    expect(screen.getByText('Rate-Up Probability')).toBeTruthy();
  });

  it('should format probabilities correctly', () => {
    render(ProbabilityResult, {
      props: {
        ...mockBannerProps.standard,
        result: {
          total_5_star_probability: 0.155,
          character_probability: 0.0775,
          light_cone_probability: 0.0775
        }
      }
    });

    expect(screen.getByText('15.50%')).toBeTruthy();
    expect(screen.getAllByText('7.75%').length).toBe(2);
  });
}); 