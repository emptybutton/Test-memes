import logging

from memes.application.ports import loggers


class Logger(loggers.Logger):
    def __init__(self, logger: logging.Logger) -> None:
        self.__logger = logger

    def log_media_is_not_working(self) -> None:
        self.__logger.error("media API is not working")
