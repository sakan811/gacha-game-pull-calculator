"""Module for calculating gacha banner statistics across multiple games.

This module provides functionality to analyze gacha banner statistics for various games (Star Rail, Genshin Impact, Zenless Zone Zero). It handles probability calculations for different banner types.
"""

# numpy is used by calculator, not directly here
from typing import Dict, Tuple, Any

from core.banner import BannerConfig
from core.calculator import ProbabilityCalculator
from output.csv_handler import CSVOutputHandler
from core.logging import Logger

logger = Logger().get_logger()


class BannerStats:
    def __init__(
        self,
        config: BannerConfig,
        calculator: ProbabilityCalculator,
        output_handler: CSVOutputHandler,
    ):
        if not isinstance(config, BannerConfig):
            raise TypeError("config must be an instance of BannerConfig")
        if not isinstance(calculator, ProbabilityCalculator):
            raise TypeError("calculator must be an instance of ProbabilityCalculator")
        if not isinstance(output_handler, CSVOutputHandler):
            raise TypeError("output_handler must be an instance of CSVOutputHandler")
        self.config = config
        self.calculator = calculator
        self.output_handler = output_handler
        self.game_name = config.game_name
        self.banner_type = config.banner_type
        self.results: Dict[str, Any] = {}

    def calculate_probabilities(self) -> None:
        logger.info(
            f"Calculating probabilities for {self.game_name} - {self.banner_type} banner..."
        )
        self.calculator.config = self.config
        self.calculator._initialize_calculations()
        raw_probs = self.calculator._calculate_raw_probabilities()
        first_5_star_probs = self.calculator._calculate_first_5star_prob_from_raw(
            raw_probs
        )
        cumulative_probs = self.calculator._calculate_cumulative_prob_from_raw(
            raw_probs
        )
        self.results = {
            "rolls": self.calculator.rolls,
            "raw_probabilities": raw_probs,
            "first_5_star_probabilities": first_5_star_probs,
            "cumulative_probabilities": cumulative_probs,
        }
        logger.info(
            f"Finished calculating probabilities for {self.game_name} - {self.banner_type}."
        )

    def get_banner_rows(self) -> Tuple[list[str], list[list[Any]]]:
        header = [
            "Game",
            "Banner Type",
            "Roll Number",
            "Probability per Roll",
            "Cumulative Probability",
            "First 5 Star Probability",
        ]
        cumulative_probs = self.results.get("cumulative_probabilities", [])
        first_5_star_probs = self.results.get("first_5_star_probabilities", [])
        raw_probs = self.results.get("raw_probabilities", [])
        rolls = self.results.get("rolls", [])
        game = self.game_name
        banner_type = self.banner_type

        def _safe_get(lst, idx):
            try:
                return lst[idx]
            except IndexError:
                return None

        rows = []
        for idx, roll in enumerate(rolls):
            row = [
                game,
                banner_type,
                roll,
                _safe_get(raw_probs, idx),
                _safe_get(cumulative_probs, idx),
                _safe_get(first_5_star_probs, idx),
            ]
            rows.append(row)
        return header, rows
