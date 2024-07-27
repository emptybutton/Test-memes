from abc import ABC, abstractmethod
from enum import Enum, auto

from memes.domain.vos import Image


class RemovingFailures(Enum):
    media_is_not_working = auto()


class AdditionFailures(Enum):
    media_is_not_working = auto()
    unsupported_image_extension = auto()


class ReceivingFailures(Enum):
    media_is_not_working = auto()
    no_image = auto()


class Gateway(ABC):
    @abstractmethod
    async def add_image(self, image: Image) -> AdditionFailures | None: ...

    @abstractmethod
    async def update_image(self, image: Image) -> AdditionFailures | None: ...

    @abstractmethod
    async def get_image_by_name(self, name: str) -> Image| ReceivingFailures: ...

    @abstractmethod
    async def remove_by_name(self, name: str) -> RemovingFailures | None: ...
