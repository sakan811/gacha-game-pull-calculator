from stats_utils.hsr_warp_stats import WarpStats

stats = WarpStats("limited")
stats.plot_statistics("stats/graph/hsr_limited_banner_stats.jpg")

stats = WarpStats("standard")
stats.plot_statistics("stats/graph/hsr_standard_banner_stats.jpg")

stats = WarpStats("light_cone")
stats.plot_statistics("stats/graph/hsr_light_cone_banner_stats.jpg")

