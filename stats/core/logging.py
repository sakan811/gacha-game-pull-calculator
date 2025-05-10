import logging

class Logger:
    def __init__(self, level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        self._setup_logging()

    def _setup_logging(self):
        formatter = logging.Formatter(
            '%(asctime)s - %(module)s - %(levelname)s - %(lineno)d - %(message)s'
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger
