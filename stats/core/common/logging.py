"""Centralized logging configuration."""
import logging
from typing import Optional


def get_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """Get a configured logger instance.
    
    Args:
        name: Logger name, typically __name__
        level: Logging level, defaults to INFO
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name or __name__)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(module)s - %(levelname)s - %(lineno)d - %(message)s"
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
    
    return logger
