import numpy as np
import seaborn as sns
import pandas as pd  # Add pandas for data handling
import os
import matplotlib.pyplot as plt  # Add this import


class WarpStats:
    def __init__(self, banner_type="standard"):
        """Initialize warp statistics calculator.

        Args:
            banner_type (str): 'standard', 'limited', or 'light_cone'
        """
        self.banner_type = banner_type.lower()

        # Set banner-specific parameters
        if self.banner_type == "standard":
            self.base_rate = 0.003  # Base rate 0.3% for 5★ Character
            self.four_star_rate = 0.051  # Base rate 5.1% for 4★
            self.pity_start = 74  # Soft pity starts at 74
            self.hard_pity = 90  # Guaranteed 5★
            self.rate_increase = 0.06  # Rate increase per pull during soft pity
            self.guarantee_featured = False
        elif self.banner_type == "limited":
            self.base_rate = 0.006  # Base rate 0.6% for 5★ Character
            self.four_star_rate = 0.051  # Base rate 5.1% for 4★
            self.pity_start = 74  # Soft pity starts at 74
            self.hard_pity = 90  # Guaranteed 5★
            self.rate_increase = 0.06  # Rate increase per pull during soft pity
            self.guarantee_featured = True
            self.featured_rate = 0.5  # 50% chance for featured character
        elif self.banner_type == "light_cone":
            self.base_rate = 0.008  # Base rate 0.8% for 5★ Light Cone
            self.four_star_rate = 0.066  # Base rate 6.6% for 4★
            self.pity_start = 65  # Soft pity starts at 65
            self.hard_pity = 80  # Guaranteed 5★
            self.rate_increase = 0.07  # Rate increase per pull during soft pity
            self.guarantee_featured = True
            self.featured_rate = 0.75  # 75% chance for featured Light Cone
        else:
            raise ValueError(
                "banner_type must be 'standard', 'limited', or 'light_cone'"
            )

        self.spark = 300  # Spark system guarantee for all banners
        self.rolls = np.arange(1, self.hard_pity + 1)
        self.probabilities = self._calculate_probabilities()
        self.p_first_5_star = self._calculate_first_5star_prob()
        self.cumulative_prob = self._calculate_cumulative_prob()

    def _calculate_probabilities(self):
        """Calculate base probabilities for each roll."""
        probabilities = []
        for roll in self.rolls:
            if roll < self.pity_start:
                probabilities.append(self.base_rate)
            elif roll < self.hard_pity:
                # Increased rate after soft pity
                increased_rate = (
                    self.base_rate + (roll - self.pity_start + 1) * self.rate_increase
                )
                probabilities.append(min(1.0, increased_rate))
            else:
                probabilities.append(1.0)  # Guaranteed
        return probabilities

    def _calculate_first_5star_prob(self):
        """Calculate probability of getting first 5★ on each roll."""
        p_first_5_star = []
        cumulative_no_5_star = 1.0

        for p in self.probabilities:
            p_n = cumulative_no_5_star * p
            p_first_5_star.append(p_n)
            cumulative_no_5_star *= 1 - p

        return p_first_5_star

    def _calculate_cumulative_prob(self):
        """Calculate cumulative probability of getting 5★."""
        return [
            sum(self.p_first_5_star[: i + 1]) for i in range(len(self.p_first_5_star))
        ]

    def plot_statistics(self, save_path=None):
        """Create and display probability plots optimized for Instagram (4:5 ratio)."""
        # Set the style for better visuals
        sns.set_theme(style="whitegrid", context="paper", font_scale=1.2)
        plt.rcParams["axes.grid"] = True
        plt.rcParams["grid.alpha"] = 0.3

        most_likely_roll = self.rolls[np.argmax(self.p_first_5_star)]

        # Create figure with 4:5 ratio using matplotlib with more space for title
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12.5))

        # Use a clean color palette
        colors = sns.color_palette("deep")

        # Create title with adjusted position
        title = self.banner_type.replace("_", " ").title()
        fig.suptitle(
            f"Honkai: Star Rail\n{title} Banner Analysis",
            fontsize=20,
            y=1.0,
            fontweight="bold",
        )

        # Create DataFrame for plotting
        plot_data = pd.DataFrame(
            {
                "Roll Number": self.rolls,
                "Probability per Roll": self.p_first_5_star,
                "Cumulative Probability": self.cumulative_prob,
            }
        )

        # Plot individual roll probabilities (upper third)
        sns.lineplot(
            data=plot_data,
            x="Roll Number",
            y="Probability per Roll",
            ax=ax1,
            color=colors[0],
            linewidth=2,
        )

        # Add vertical lines with offset labels
        ax1.axvline(
            most_likely_roll,
            color=colors[1],
            linestyle="--",
            linewidth=1.5,
            label=f"Most Likely Roll: {most_likely_roll}",
        )
        ax1.axvline(
            self.pity_start,
            color=colors[2],
            linestyle=":",
            linewidth=1.5,
            label=f"Soft Pity Start ({self.pity_start})",
        )

        # Move legend to upper left for first plot
        ax1.legend(loc="upper left", fontsize=10, framealpha=0.9)
        ax1.set_title("Pull Probability Distribution", fontsize=16, pad=10)
        ax1.set_xlabel("")
        ax1.set_ylabel("Probability", fontsize=12)

        # Plot cumulative probability (middle third)
        sns.lineplot(
            data=plot_data,
            x="Roll Number",
            y="Cumulative Probability",
            ax=ax2,
            color=colors[3],
            linewidth=2,
        )

        # Add horizontal and vertical lines
        ax2.axhline(
            0.5, color=colors[4], linestyle=":", linewidth=1.5, label="50% Chance"
        )
        ax2.axhline(
            1.0, color=colors[2], linestyle="-.", linewidth=1.5, label="100% Guarantee"
        )
        ax2.axvline(
            self.hard_pity,
            color=colors[1],
            linestyle="--",
            linewidth=1.5,
            label=f"Hard Pity ({self.hard_pity})",
        )

        # Keep legend to upper left for second plot
        ax2.legend(loc="upper left", fontsize=10, framealpha=0.9)
        ax2.set_title("Cumulative Probability", fontsize=16, pad=10)
        ax2.set_xlabel("Roll Number", fontsize=12)
        ax2.set_ylabel("Probability", fontsize=12)

        # Adjust layout with more space for title
        plt.tight_layout()
        plt.subplots_adjust(top=0.90, hspace=0.3)

        # Save the plot if path is provided
        if save_path:
            # Create graphs subdirectory inside stats
            graph_dir = os.path.join(save_path, "graph")
            os.makedirs(graph_dir, exist_ok=True)

            filename = os.path.join(
                graph_dir, f"hsr_{self.banner_type}_banner_stats.jpg"
            )
            plt.savefig(filename, dpi=300, bbox_inches="tight", format="jpg")
            plt.close()
        else:
            plt.show()

    def calculate_expected_pulls(self, guaranteed=False):
        """Calculate expected number of pulls needed for featured item.

        Args:
            guaranteed (bool): Whether next 5★ is guaranteed to be featured
        """
        if not hasattr(self, "guarantee_featured"):
            return None

        # Calculate average pulls for one 5★
        avg_pulls_for_5star = sum(i * p for i, p in enumerate(self.p_first_5_star, 1))

        if guaranteed:
            return avg_pulls_for_5star
        else:
            # For Light Cones: 75% chance to get it first try, 25% chance to need second pity
            # For Limited Characters: 50% chance to need second pity
            second_pity_chance = 0.25 if self.banner_type == "light_cone" else 0.5
            return avg_pulls_for_5star * (1 + second_pity_chance)


# Example usage
if __name__ == "__main__":
    # Create stats directory
    stats_dir = "stats"

    # Analyze all banner types
    for banner_type in ["standard", "limited", "light_cone"]:
        stats = WarpStats(banner_type)
        stats.plot_statistics(save_path=stats_dir)
