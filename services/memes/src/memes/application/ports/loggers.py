from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def log_media_is_not_working(self) -> None: ...
