import logging
import sys


class CustomLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger


custom_logger = CustomLogger()

logger = custom_logger.get_logger()