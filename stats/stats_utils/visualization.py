"""Visualization module for HSR Warp Statistics."""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


class BannerVisualizer:
    """Class for visualizing banner statistics."""
    
    def __init__(self):
        """Initialize the visualizer with style settings."""
        sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3

    def create_distribution_plot(self, data, game_type, banner_type, save_path=None):
        """Create distribution plot.
        
        Args:
            data (pd.DataFrame): DataFrame containing roll numbers and probabilities
            game_type (str): Type of game ('star_rail', 'genshin', or 'zenless')
            banner_type (str): Type of banner ('standard', 'limited', 'light_cone', 'weapon', or 'w_engine')
            save_path (str, optional): Path to save the plot. If None, plot is not saved.
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        fig = plt.figure(figsize=(7.5, 8.75))  # 4:5 exact ratio 
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
        
        # Determine soft pity start based on banner type
        soft_pity_start = 0
        if game_type == 'star_rail':
            if banner_type == 'light_cone':
                soft_pity_start = 65
            else:
                soft_pity_start = 73
        elif game_type == 'genshin':
            if banner_type == 'weapon':
                soft_pity_start = 62
            else:
                soft_pity_start = 73
        elif game_type == 'zenless':
            if banner_type == 'w_engine':
                soft_pity_start = 64
            else:
                soft_pity_start = 73
                
        ax.axvline(soft_pity_start, color=colors[2], linestyle=':',
                  label=f'Soft Pity Start ({soft_pity_start})')
        
        # Add annotation for soft pity
        soft_pity_prob = data.loc[data['Roll Number'] == soft_pity_start, 'Probability per Roll'].values[0] if soft_pity_start in data['Roll Number'].values else 0
        if soft_pity_prob > 0:
            ax.annotate(f'Soft Pity: {soft_pity_prob:.1%}',
                       xy=(soft_pity_start, soft_pity_prob),
                       xytext=(10, -30), textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8))
        
        ax.annotate(f'Peak: {max_prob:.1%}',
                   xy=(most_likely_pull, max_prob),
                   xytext=(10, 10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8))
        
        # Set appropriate title based on game type
        game_titles = {
            'star_rail': 'Honkai: Star Rail',
            'genshin': 'Genshin Impact',
            'zenless': 'Zenless Zone Zero'
        }
        
        game_title = game_titles.get(game_type, game_type.replace('_', ' ').title())
        banner_title = banner_type.replace('_', ' ').title()
        
        ax.set_title(f"{game_title}\n{banner_title} Banner\nPull Distribution",
                    fontsize=16, pad=20)
        ax.set_xlabel("Roll Number")
        ax.set_ylabel("Probability per Roll")
        ax.legend(loc='upper left')

        if save_path:
            # Ensure directory exists before saving
            os.makedirs(os.path.dirname(f"{save_path}_distribution.jpg"), exist_ok=True)
            plt.savefig(f"{save_path}_distribution.jpg", dpi=300, bbox_inches='tight')
            plt.close()
        return fig

    def create_cumulative_plot(self, data, game_type, banner_type, save_path=None):
        """Create cumulative probability plot.
        
        Args:
            data (pd.DataFrame): DataFrame containing roll numbers and probabilities
            game_type (str): Type of game ('star_rail', 'genshin', or 'zenless')
            banner_type (str): Type of banner ('standard', 'limited', 'light_cone', 'weapon', or 'w_engine')
            save_path (str, optional): Path to save the plot. If None, plot is not saved.
            
        Returns:
            matplotlib.figure.Figure: The created figure
        """
        fig = plt.figure(figsize=(7.5, 8.75))  # 4:5 exact ratio
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
        
        # Determine hard pity based on banner type
        hard_pity = 0
        if game_type in ['star_rail', 'genshin']:
            if banner_type in ['light_cone', 'weapon']:
                hard_pity = 80
            else:
                hard_pity = 90
        elif game_type == 'zenless':
            if banner_type == 'w_engine':
                hard_pity = 80
            else:
                hard_pity = 90
                
        ax.axvline(hard_pity, color=colors[1], linestyle='--', label='Hard Pity')
        
        ax.annotate(f'50% at pull {int(fifty_percent_pull)}',
                   xy=(fifty_percent_pull, 0.5),
                   xytext=(10, -10), textcoords='offset points',
                   bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8))
        
        # Set appropriate title based on game type
        game_titles = {
            'star_rail': 'Honkai: Star Rail',
            'genshin': 'Genshin Impact',
            'zenless': 'Zenless Zone Zero'
        }
        
        game_title = game_titles.get(game_type, game_type.replace('_', ' ').title())
        banner_title = banner_type.replace('_', ' ').title()
        
        ax.set_title(f"{game_title}\n{banner_title} Banner\nCumulative Probability",
                    fontsize=16, pad=20)
        ax.set_xlabel("Roll Number")
        ax.set_ylabel("Cumulative Probability")
        ax.legend(loc='lower right')

        if save_path:
            # Ensure directory exists before saving
            os.makedirs(os.path.dirname(f"{save_path}_cumulative.jpg"), exist_ok=True)
            plt.savefig(f"{save_path}_cumulative.jpg", dpi=300, bbox_inches='tight')
            plt.close()
        return fig

    def create_plots(self, data, game_type, banner_type, save_path):
        """Create all plots for a banner type.
        
        Args:
            data (pd.DataFrame): DataFrame containing roll numbers and probabilities
            game_type (str): Type of game ('star_rail', 'genshin', or 'zenless')
            banner_type (str): Type of banner ('standard', 'limited', 'light_cone', 'weapon', or 'w_engine')
            save_path (str, optional): Path to save the plots. If None, plots are not saved.
        """
        # Ensure the directory exists for all plots
        os.makedirs(os.path.dirname(f"{save_path}_distribution.jpg"), exist_ok=True)
        
        self.create_distribution_plot(data, game_type, banner_type, save_path)
        self.create_cumulative_plot(data, game_type, banner_type, save_path)