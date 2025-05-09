# Genshin game-specific module
from stats.core.banner import BaseBanner, BannerConfig
from stats.core.calculator import ProbabilityCalculator

class GenshinBanner(BaseBanner):
    """Genshin Impact-specific banner implementation."""
    pass

class GenshinProbabilityCalculator(ProbabilityCalculator):
    """Probability calculator for Genshin Impact banners."""
    pass
