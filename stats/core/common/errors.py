"""Common error types for the application."""


class BannerError(Exception):
    """Base error class for banner operations."""

    pass


class ValidationError(BannerError):
    """Error raised when validation fails."""

    pass


class CalculationError(BannerError):
    """Base error for calculation failures."""

    pass


class ConfigurationError(BannerError):
    """Error raised when configuration is invalid."""

    pass


class DataError(BannerError):
    """Error raised when data handling fails."""

    pass
