import { render, screen } from '@testing-library/vue';
import { describe, it, expect, beforeEach } from 'vitest';
import App from '../App.vue';

describe('App Component', () => {
  beforeEach(() => {
    render(App);
  });

  describe('Basic Rendering', () => {
    it('should render initial components', () => {
      expect(screen.getByText('Honkai Star Rail Banner Calculator')).toBeTruthy();
      expect(screen.getByLabelText('Banner Type')).toBeTruthy();
      expect(screen.getByLabelText('Current Pity')).toBeTruthy();
      expect(screen.getByLabelText('Planned Pulls')).toBeTruthy();
    });

    it('should not show plots and results initially', () => {
      expect(screen.queryByTestId('probability-results')).toBeFalsy();
      expect(screen.queryByTestId('probability-plots')).toBeFalsy();
    });
  });
});
