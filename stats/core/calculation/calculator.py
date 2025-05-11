"""Base calculator module for banner probability calculations."""

from abc import ABC, abstractmethod
from typing import Optional
import numpy as np
from numpy.typing import NDArray

from ..config.banner import BannerConfig
from ..common.errors import ConfigurationError
from ..common.logging import get_logger

logger = get_logger(__name__)

# Type aliases for improved readability
ProbabilityArray = NDArray[np.float64]


class ProbabilityCalculator(ABC):
    """Base class for calculating banner probabilities."""

    def __init__(self, config: Optional[BannerConfig] = None) -> None:
        self.config: Optional[BannerConfig] = config

    def _initialize_calculations(self) -> None:
        """Initialize calculation parameters.

        Raises:
            ConfigurationError: If configuration is not set
        """
        if not self.config:
            raise ConfigurationError("Calculator configuration not set")

    @abstractmethod
    def _calculate_raw_probabilities(self) -> ProbabilityArray:
        """Calculate raw probabilities for each pull.

        Returns:
            Array of raw probabilities

        Raises:
            ConfigurationError: If configuration is invalid
        """
        pass

    @abstractmethod
    def _calculate_first_5star_prob_from_raw(
        self, raw_probabilities: ProbabilityArray
    ) -> ProbabilityArray:
        """Calculate probability of first 5★ from raw probabilities.

        Args:
            raw_probabilities: Array of raw probabilities

        Returns:
            Array of first 5★ probabilities
        """
        pass

    @abstractmethod
    def _calculate_cumulative_prob_from_raw(
        self, raw_probabilities: ProbabilityArray
    ) -> ProbabilityArray:
        """Calculate cumulative probabilities from raw probabilities.

        Args:
            raw_probabilities: Array of raw probabilities

        Returns:
            Array of cumulative probabilities
        """
        pass
