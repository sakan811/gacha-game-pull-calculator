import { render, screen } from '@testing-library/vue';
import { describe, it, expect } from 'vitest';
import ProbabilityResult from '../../components/ProbabilityResult.vue';
import { mockBannerProps } from '../utils/test-utils';

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

  it('should handle guaranteed rate up state', () => {
    render(ProbabilityResult, {
      props: {
        ...mockBannerProps.limited,
        guaranteed: true,
        result: {
          total_5_star_probability: 1.0,
          rate_up_probability: 1.0
        }
      }
    });

    // Use getAllByText instead of getByText for multiple matches
    const hundredPercent = screen.getAllByText('100.00%');
    expect(hundredPercent).toHaveLength(2);
    expect(screen.getByText('Rate-Up Probability')).toBeTruthy();
  });

  it('should handle edge case probability values', () => {
    render(ProbabilityResult, {
      props: {
        ...mockBannerProps.standard,
        result: {
          total_5_star_probability: 0,
          character_probability: 0,
          light_cone_probability: 0
        }
      }
    });

    const results = screen.getAllByText('0.00%');
    expect(results).toHaveLength(3);
  });

  it('should handle missing probability data gracefully', () => {
    render(ProbabilityResult, {
      props: {
        ...mockBannerProps.standard,
        result: {}
      }
    });

    const results = screen.getAllByText('0.00%');
    expect(results).toHaveLength(3);
  });
});