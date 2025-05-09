
"""Main script for generating banner statistics CSVs.

This script generates statistics CSVs for different banner types across multiple games (Star Rail, Genshin Impact, and Zenless Zone Zero).
"""

from stats_utils.banner_stats import BannerStats


class StatsRunner:
    """Class to run all banner statistics generation in a modular way."""

    def __init__(self):
        self.banner_jobs = [
            # (game_type, banner_type)
            ("star_rail", "limited"),
            ("star_rail", "standard"),
            ("star_rail", "light_cone"),
            ("genshin", "limited"),
            ("genshin", "standard"),
            ("genshin", "weapon"),
            ("zenless", "limited"),
            ("zenless", "standard"),
            ("zenless", "w_engine"),
            ("zenless", "bangboo"),
        ]

    def run(self):
        for game_type, banner_type in self.banner_jobs:
            stats = BannerStats(game_type, banner_type)
            stats.save_statistics_csv()


if __name__ == "__main__":
    runner = StatsRunner()
    runner.run()
