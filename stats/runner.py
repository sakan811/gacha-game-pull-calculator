# Main execution logic stub

from core.banner_config import BANNER_CONFIGS
from core.banner_stats import BannerStats


def main():
    """Run probability calculations and output for all supported banners and games."""
    for config_key in BANNER_CONFIGS:
        # Parse game and banner type from config key
        if "_" not in config_key:
            continue
        game_type, banner_type = config_key.split("_", 1)
        try:
            stats = BannerStats(game_type=game_type, banner_type=banner_type)
            file_paths = stats.save_statistics_csv()
            print(f"Saved stats for {game_type} {banner_type}:")
            for metric, path in file_paths.items():
                print(f"  {metric}: {path}")
        except Exception as e:
            print(f"Error processing {config_key}: {e}")


if __name__ == "__main__":
    main()
