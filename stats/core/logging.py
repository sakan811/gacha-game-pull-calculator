import logging


class Logger:
    def __init__(self, level: int = logging.INFO) -> None:
        self.logger = logging.getLogger(__name__)
        if not self.logger.hasHandlers():  
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
