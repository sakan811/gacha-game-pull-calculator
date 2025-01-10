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

    def create_plot(self, data, banner_type, save_path=None):
        """Create and save/display the probability plots."""
        # Create figure with 4:5 ratio
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12.5))
        
        # Use a clean color palette
        colors = sns.color_palette("deep")
        
        # Add title
        title = banner_type.replace('_', ' ').title()
        fig.suptitle(f"Honkai: Star Rail\n{title} Banner Analysis", 
                    fontsize=20, y=1.0, fontweight='bold')
        
        # Plot individual roll probabilities (upper)
        sns.lineplot(data=data, x='Roll Number', y='Probability per Roll', 
                    ax=ax1, color=colors[0], linewidth=2,
                    label='Pull Probability')
        
        # Add data labels for important points in probability distribution
        most_likely_pull = data['Roll Number'][data['Probability per Roll'].idxmax()]
        max_prob = data['Probability per Roll'].max()
        
        # Add vertical lines with labels
        ax1.axvline(most_likely_pull, color=colors[1], linestyle='--', linewidth=1.5,
                   label=f'Most Likely Pull ({most_likely_pull})')
        ax1.axvline(74 if banner_type != 'light_cone' else 65, 
                   color=colors[2], linestyle=':', linewidth=1.5,
                   label='Soft Pity Start')
        
        # Add annotation for peak probability
        ax1.annotate(f'Peak: {max_prob:.1%}',
                    xy=(most_likely_pull, max_prob),
                    xytext=(10, 10), textcoords='offset points',
                    ha='left', va='bottom',
                    bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        ax1.legend(loc='upper left', fontsize=10, framealpha=0.9)
        ax1.set_title("Succesful Pull Probability Distribution", fontsize=16, pad=10)
        ax1.set_xlabel("Roll Number", fontsize=12)
        ax1.set_ylabel("Probability", fontsize=12)

        # Plot cumulative probability (lower)
        sns.lineplot(data=data, x='Roll Number', y='Cumulative Probability', 
                    ax=ax2, color=colors[3], linewidth=2,
                    label='Cumulative Rate')
        
        # Add reference lines and labels
        fifty_percent_pull = np.interp(0.5, data['Cumulative Probability'], data['Roll Number'])
        
        ax2.axhline(0.5, color=colors[4], linestyle=':', linewidth=1.5,
                    label='50% Chance')
        ax2.axhline(1.0, color=colors[2], linestyle='-.', linewidth=1.5,
                    label='100% Guarantee')
        ax2.axvline(90 if banner_type != 'light_cone' else 80, 
                    color=colors[1], linestyle='--', linewidth=1.5,
                    label='Hard Pity')
        
        # Add annotation for 50% point
        ax2.annotate(f'50% at pull {int(fifty_percent_pull)}',
                    xy=(fifty_percent_pull, 0.5),
                    xytext=(10, -10), textcoords='offset points',
                    ha='left', va='top',
                    bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        ax2.legend(loc='lower right', fontsize=10, framealpha=0.9,
                  bbox_to_anchor=(0.98, 0.98))
        ax2.set_title("Cumulative Probability", fontsize=16, pad=10)
        ax2.set_xlabel("Roll Number", fontsize=12)
        ax2.set_ylabel("Probability", fontsize=12)

        # Adjust layout
        plt.tight_layout()
        plt.subplots_adjust(top=0.90, hspace=0.3)

        # Save or display the plot
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight', format='jpg')
            plt.close()
        else:
            plt.show()