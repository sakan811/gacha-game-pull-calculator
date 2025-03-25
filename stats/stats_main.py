"""Main script for generating banner statistics visualizations.

This script generates probability distribution and cumulative probability plots
for different banner types across multiple games (Star Rail, Genshin Impact,
and Zenless Zone Zero). The plots are saved in the graph/ directory.
"""

from stats_utils.banner_stats import BannerStats

# Star Rail banners
stats = BannerStats("star_rail", "limited")
stats.plot_statistics("graph/hsr_limited_banner_stats")

stats = BannerStats("star_rail", "standard")
stats.plot_statistics("graph/hsr_standard_banner_stats")

stats = BannerStats("star_rail", "light_cone")
stats.plot_statistics("graph/hsr_light_cone_banner_stats")

# Genshin banners
stats = BannerStats("genshin", "limited")
stats.plot_statistics("graph/genshin_limited_banner_stats")

stats = BannerStats("genshin", "standard")
stats.plot_statistics("graph/genshin_standard_banner_stats")

stats = BannerStats("genshin", "weapon")
stats.plot_statistics("graph/genshin_weapon_banner_stats")

# Zenless Zone Zero banners
stats = BannerStats("zenless", "limited")
stats.plot_statistics("graph/zenless_limited_banner_stats")

stats = BannerStats("zenless", "standard")
stats.plot_statistics("graph/zenless_standard_banner_stats")

stats = BannerStats("zenless", "w_engine")
stats.plot_statistics("graph/zenless_w_engine_banner_stats")

stats = BannerStats("zenless", "bangboo")
stats.plot_statistics("graph/zenless_bangboo_banner_stats")
