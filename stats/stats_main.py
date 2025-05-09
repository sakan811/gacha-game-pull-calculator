"""Main script for generating banner statistics visualizations.

This script generates probability distribution and cumulative probability plots
for different banner types across multiple games (Star Rail, Genshin Impact,
and Zenless Zone Zero). The plots are saved in the graph/ directory.
"""


from stats_utils.banner_stats import BannerStats

class StatsRunner:
    """Class to run all banner statistics generation in a modular way."""
    def __init__(self):
        self.banner_jobs = [
            # (game_type, banner_type, output_path)
            ("star_rail", "limited", "graph/hsr_limited_banner_stats"),
            ("star_rail", "standard", "graph/hsr_standard_banner_stats"),
            ("star_rail", "light_cone", "graph/hsr_light_cone_banner_stats"),
            ("genshin", "limited", "graph/genshin_limited_banner_stats"),
            ("genshin", "standard", "graph/genshin_standard_banner_stats"),
            ("genshin", "weapon", "graph/genshin_weapon_banner_stats"),
            ("zenless", "limited", "graph/zenless_limited_banner_stats"),
            ("zenless", "standard", "graph/zenless_standard_banner_stats"),
            ("zenless", "w_engine", "graph/zenless_w_engine_banner_stats"),
            ("zenless", "bangboo", "graph/zenless_bangboo_banner_stats"),
        ]

    def run(self):
        for game_type, banner_type, output_path in self.banner_jobs:
            stats = BannerStats(game_type, banner_type)
            stats.plot_statistics(output_path)


if __name__ == "__main__":
    runner = StatsRunner()
    runner.run()
