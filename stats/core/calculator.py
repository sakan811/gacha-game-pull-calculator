"""Base calculator module for banner probability calculations.

This module provides the base abstract class for calculating banner probabilities.
It handles the core probability calculations for gacha banners including pity systems.
"""
from abc import ABC, abstractmethod
from typing import Optional
import numpy as np
from numpy.typing import NDArray

from core.banner import BannerConfig
from core.common.errors import ConfigurationError, CalculationError
from core.common.logging import get_logger

logger = get_logger(__name__)

# Type aliases for improved readability
ProbabilityArray = NDArray[np.float64]
RollArray = NDArray[np.int64]


class ProbabilityCalculator(ABC):
    """Base class for calculating banner probabilities.
    
    This class handles the core probability calculations for gacha banners,
    including pity systems, rate-up mechanics, and cumulative probabilities.
    
    Attributes:
        config: Banner configuration parameters
        rolls: Array of roll numbers from 1 to hard pity
        probabilities: Raw probabilities for each roll
        p_first_5_star: Probability of getting first 5-star on each roll
        cumulative_prob: Cumulative probability of getting 5-star by each roll
    """

    def __init__(self, config: Optional[BannerConfig] = None) -> None:
        """Initialize the calculator with optional banner config.

        Args:
            config: Banner configuration parameters. If provided, calculations
                   will be initialized immediately.

        Raises:
            ConfigurationError: If the provided config is invalid
        """
        self.config: Optional[BannerConfig] = config

        # Initialize arrays with proper types
        self.rolls: RollArray = np.array([], dtype=np.int64)
        self.probabilities: ProbabilityArray = np.array([], dtype=np.float64)
        self.p_first_5_star: ProbabilityArray = np.array([], dtype=np.float64)
        self.cumulative_prob: ProbabilityArray = np.array([], dtype=np.float64)

        if self.config:
            try:
                self._initialize_calculations()
            except Exception as e:
                logger.error(f"Failed to initialize calculations: {str(e)}")
                raise ConfigurationError(f"Invalid banner configuration: {str(e)}")

    def _initialize_calculations(self) -> None:
        """Initialize all probability calculations.
        
        This method sets up the basic arrays and calculates all probabilities
        based on the current configuration.

        Raises:
            ConfigurationError: If config is not set or invalid
        """
        if not self.config:
            logger.error("Cannot initialize calculations without config")
            raise ConfigurationError("Configuration must be set before calculation")

        try:
            self.rolls = np.arange(1, self.config.hard_pity + 1, dtype=np.int64)
            self.probabilities = self._calculate_raw_probabilities()
            self.p_first_5_star = self._calculate_first_5star_prob_from_raw(
                self.probabilities
            )
            self.cumulative_prob = self._calculate_cumulative_prob_from_raw(
                self.probabilities
            )
        except Exception as e:
            logger.error(f"Calculation initialization failed: {str(e)}")
            raise CalculationError(f"Failed to initialize calculations: {str(e)}")

    def _calculate_raw_probabilities(self) -> ProbabilityArray:
        """Calculate raw probabilities for each roll.
        
        Calculates the base probability of getting a 5-star on each roll,
        taking into account soft pity and hard pity mechanics.

        Returns:
            Array of probabilities for each roll number

        Raises:
            ConfigurationError: If config is not set
            ValueError: If probability calculations yield invalid values
        """
        if self.config is None:
            logger.error("Config must be set to calculate raw probabilities")
            raise ConfigurationError("Config must be set to calculate raw probabilities")

        try:
            rolls = self.rolls
            base_rate = self.config.base_rate
            soft_pity = self.config.soft_pity_start_after
            hard_pity = self.config.hard_pity
            rate_increase = self.config.rate_increase

            # Initialize probabilities array with base rate
            probs = np.full_like(rolls, base_rate, dtype=np.float64)
            
            # Apply soft pity
            soft_mask = (rolls >= soft_pity) & (rolls < hard_pity)
            probs[soft_mask] = np.minimum(
                1.0, base_rate + (rolls[soft_mask] - soft_pity + 1) * rate_increase
            )
            
            # Apply hard pity
            probs[rolls == hard_pity] = 1.0

            # Validate probabilities
            if not np.all((probs >= 0) & (probs <= 1)):
                raise ValueError("Invalid probability values calculated")

            return probs

        except Exception as e:
            logger.error(f"Raw probability calculation failed: {str(e)}")
            raise CalculationError(f"Failed to calculate raw probabilities: {str(e)}")

    def _calculate_first_5star_prob_from_raw(
        self, raw_probabilities: ProbabilityArray
    ) -> ProbabilityArray:
        """Calculate probability of getting first 5-star on each roll.
        
        Args:
            raw_probabilities: Array of raw probabilities for each roll

        Returns:
            Array of probabilities for getting first 5-star on each roll

        Raises:
            CalculationError: If calculations fail
        """
        try:
            p_first_5_star = np.zeros_like(raw_probabilities)
            prob_no_5star_so_far = 1.0
            
            for i, p_roll in enumerate(raw_probabilities):
                p_first_5_star[i] = prob_no_5star_so_far * p_roll
                prob_no_5star_so_far *= (1 - p_roll)

            return p_first_5_star

        except Exception as e:
            logger.error(f"First 5-star probability calculation failed: {str(e)}")
            raise CalculationError(f"Failed to calculate first 5-star probabilities: {str(e)}")

    def _calculate_cumulative_prob_from_raw(
        self, raw_probabilities: ProbabilityArray
    ) -> ProbabilityArray:
        """Calculate cumulative probability of getting a 5-star by each roll.
        
        Args:
            raw_probabilities: Array of raw probabilities for each roll

        Returns:
            Array of cumulative probabilities for each roll

        Raises:
            CalculationError: If calculations fail
        """
        try:
            cumulative = np.zeros_like(raw_probabilities)
            prob_no_5star_at_all = 1.0
            
            for i, p_roll in enumerate(raw_probabilities):
                prob_no_5star_at_all *= (1 - p_roll)
                cumulative[i] = 1 - prob_no_5star_at_all

            return cumulative

        except Exception as e:
            logger.error(f"Cumulative probability calculation failed: {str(e)}")
            raise CalculationError(f"Failed to calculate cumulative probabilities: {str(e)}")

    @abstractmethod
    def calculate(self, params: dict) -> dict:
        """Calculate complete probability statistics for the banner.
        
        This method must be implemented by concrete calculator classes
        to provide specific calculation logic for different banner types.

        Args:
            params: Dictionary of calculation parameters

        Returns:
            Dictionary containing calculation results

        Raises:
            NotImplementedError: If not implemented by concrete class
        """
        raise NotImplementedError("Concrete calculators must implement calculate()")
