import logging


class Logger:
    def __init__(self, level: int = logging.INFO) -> None:
        self.logger = logging.getLogger(__name__)
        # Only configure the logger (set level and add handlers) if it hasn't been configured already.
        # This prevents duplicate handlers if Logger() is instantiated multiple times
        # for the same logger (which is logging.getLogger(__name__) here, i.e., 'stats.core.logging').
        if not self.logger.hasHandlers():  # Check if handlers are already present
            self.logger.setLevel(level)
            self._setup_logging()

    def _setup_logging(self) -> None:
        formatter = logging.Formatter(
            "%(asctime)s - %(module)s - %(levelname)s - %(lineno)d - %(message)s"
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self) -> logging.Logger:
        return self.logger
