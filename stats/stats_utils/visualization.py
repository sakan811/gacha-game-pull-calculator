"""Visualization module for HSR Warp Statistics."""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class BannerVisualizer:
    def __init__(self):
        """Initialize the visualizer with style settings."""
        sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3

    def create_distribution_plot(self, data, banner_type, save_path=None):
        """Create distribution plot."""
        fig = plt.figure(figsize=(8, 10))  # 4:5 aspect ratio
        ax = fig.add_subplot(111)
        
        colors = sns.color_palette("deep")
        
        # Plot probability distribution
        sns.lineplot(data=data, x='Roll Number', y='Probability per Roll', 
                    ax=ax, color=colors[0], linewidth=2,
                    label='Pull Probability')
        
        # Add markers and annotations
        most_likely_pull = data['Roll Number'][data['Probability per Roll'].idxmax()]
        max_prob = data['Probability per Roll'].max()
        
        ax.axvline(most_likely_pull, color=colors[1], linestyle='--',
                  label=f'Most Likely Pull ({most_likely_pull})')
        ax.axvline(74 if banner_type != 'light_cone' else 65, 
                  color=colors[2], linestyle=':',
                  label='Soft Pity Start')
        
        ax.annotate(f'Peak: {max_prob:.1%}',
                   xy=(most_likely_pull, max_prob),
                   xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8))
        
        ax.set_title(f"Honkai: Star Rail\n{banner_type.replace('_', ' ').title()} Banner\nPull Distribution",
                    fontsize=16, pad=20)
        ax.set_xlabel("Roll Number")
        ax.set_ylabel("Probability per Roll")
        ax.legend(loc='upper left')

        if save_path:
            plt.savefig(f"{save_path}_distribution.jpg", dpi=300, bbox_inches='tight')
            plt.close()
        return fig

    def create_cumulative_plot(self, data, banner_type, save_path=None):
        """Create cumulative probability plot."""
        fig = plt.figure(figsize=(8, 10))  # 4:5 aspect ratio
        ax = fig.add_subplot(111)
        
        colors = sns.color_palette("deep")
        
        # Plot cumulative probability
        sns.lineplot(data=data, x='Roll Number', y='Cumulative Probability',
                    ax=ax, color=colors[3], linewidth=2,
                    label='Cumulative Rate')
        
        # Add reference lines
        fifty_percent_pull = np.interp(0.5, data['Cumulative Probability'], data['Roll Number'])
        
        ax.axhline(0.5, color=colors[4], linestyle=':', label='50% Chance')
        ax.axhline(1.0, color=colors[2], linestyle='-.', label='100% Guarantee')
        ax.axvline(90 if banner_type != 'light_cone' else 80,
                  color=colors[1], linestyle='--', label='Hard Pity')
        
        ax.annotate(f'50% at pull {int(fifty_percent_pull)}',
                   xy=(fifty_percent_pull, 0.5),
                   xytext=(10, -10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8))
        
        ax.set_title(f"Honkai: Star Rail\n{banner_type.replace('_', ' ').title()} Banner\nCumulative Probability",
                    fontsize=16, pad=20)
        ax.set_xlabel("Roll Number")
        ax.set_ylabel("Cumulative Probability")
        ax.legend(loc='lower right')

        if save_path:
            plt.savefig(f"{save_path}_cumulative.jpg", dpi=300, bbox_inches='tight')
            plt.close()
        return fig

    def create_plots(self, data, banner_type, save_path=None):
        """Create all plots for a banner type."""
        self.create_distribution_plot(data, banner_type, save_path)
        self.create_cumulative_plot(data, banner_type, save_path)