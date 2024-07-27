from dataclasses import dataclass
from enum import Enum


class Bucket(Enum):
    images = "images"


@dataclass(kw_only=True)
class File:
    name: str
    content: bytes

    @property
    def extension(self) -> str | None:
        segments = self.name.split('.')
        return None if len(segments) == 0 else segments[-1]

    @property
    def is_image(self) -> bool:
        image_extensions = ("svg", "bmp", "webp", "gif", "png", "jpg", "jpeg")
        return self.extension in image_extensions
