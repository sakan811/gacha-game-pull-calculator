from stats_utils.hsr_warp_stats import WarpStats

# Star Rail banners
stats = WarpStats("star_rail", "limited")
stats.plot_statistics("graph/hsr_limited_banner_stats")

stats = WarpStats("star_rail", "standard")
stats.plot_statistics("graph/hsr_standard_banner_stats")

stats = WarpStats("star_rail", "light_cone")
stats.plot_statistics("graph/hsr_light_cone_banner_stats")

# Genshin banners
stats = WarpStats("genshin", "limited")
stats.plot_statistics("graph/genshin_limited_banner_stats")

stats = WarpStats("genshin", "standard")
stats.plot_statistics("graph/genshin_standard_banner_stats")

stats = WarpStats("genshin", "weapon")
stats.plot_statistics("graph/genshin_weapon_banner_stats")

# Zenless Zone Zero banners
stats = WarpStats("zenless", "limited")
stats.plot_statistics("graph/zenless_limited_banner_stats")

stats = WarpStats("zenless", "standard")
stats.plot_statistics("graph/zenless_standard_banner_stats")

stats = WarpStats("zenless", "w_engine")
stats.plot_statistics("graph/zenless_w_engine_banner_stats")

stats = WarpStats("zenless", "bangboo")
stats.plot_statistics("graph/zenless_bangboo_banner_stats")
